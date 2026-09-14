#!/usr/bin/env python3
"""校验项目文档体系是否符合规范。

零第三方依赖：可能被拷进任意项目并在 CI 中运行，引入 YAML 之类的依赖会
让它在没有包管理器的环境里直接失效。

用法：
    python verify_docs.py [项目根目录]

若同目录下存在 gen_index.py，还会顺带校验索引生成区是否与 frontmatter 同步。

退出码：有 error 返回 1，否则返回 0。
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

TYPES = {
    "standard", "guide", "reference", "architecture",
    "adr", "rfc", "design", "requirement", "release",
}
STATUSES = {"draft", "active", "deprecated", "superseded", "rejected"}
REQUIRED_FIELDS = ("title", "type", "status", "summary")
LONG_FORM_TYPES = {"adr", "rfc", "design", "architecture"}
DATE_FIELD_TYPES = {"adr", "rfc"}

EXEMPT_HEADING = "不纳入索引的目录"
BUILTIN_EXEMPT = {"templates"}  # 模板存放处，不是文档
CODE_PATH_RE = re.compile(r"`([^`\n]+\.(?:md|json|yaml|yml|toml|py|ts|java))`")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")
PLACEHOLDER_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:待补充|待定|待实现|占位|TBD|TODO|Coming soon)\s*$", re.I)
# HTML 注释在渲染时不可见，链接与索引检查必须先剔除，否则隐藏条目会被误判
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# 模板里写给生成方的指令，产物中不应残留
GEN_NOTE_RE = re.compile(r"<!--\s*gen-note:")


@dataclass
class Finding:
    level: str  # "error" | "warning"
    path: str
    message: str


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """解析文件开头的 frontmatter，返回 (meta, body)。

    只支持标量与顶层列表。行内注释仅在值是单个 token 时才剥离，避免误伤
    含空格的正文型值（例如中文 summary 里出现「 # 」）。

    读取一律使用 utf-8-sig：带 BOM 的 Markdown 在 Windows 上很常见
    （记事本、PowerShell 重定向、部分编辑器配置都会产生），若不剥离，
    首行不等于 `---`，整个 frontmatter 会被忽略并报出一堆假错误。
    """
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text

    meta: dict = {}
    list_key = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if raw.lstrip().startswith("- ") and list_key:
            meta.setdefault(list_key, []).append(raw.strip()[2:].strip())
            continue
        if raw[:1].isspace() or ":" not in raw:
            continue  # 嵌套结构不支持，忽略
        key, _, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        if " #" in value:
            head = value.partition(" #")[0].strip()
            if head and " " not in head:
                value = head
        if value == "":
            meta[key] = []
            list_key = key
        else:
            meta[key] = value
            list_key = None
    return meta, "\n".join(lines[end + 1:])


def read_meta(path: Path) -> dict:
    return parse_frontmatter(path.read_text(encoding="utf-8-sig"))[0]


def is_nav(path: Path) -> bool:
    """README 是导航文件，不参与文档级元数据检查。"""
    return path.name == "README.md"


# --- 文档级检查 ---------------------------------------------------------

def check_frontmatter(files, root: Path) -> list:
    out = []
    for f in files:
        if is_nav(f):
            continue
        meta = read_meta(f)
        for field in REQUIRED_FIELDS:
            if not meta.get(field):
                out.append(Finding("error", rel(f, root), f"缺少必填字段：{field}"))
        t = meta.get("type")
        if t and t not in TYPES:
            out.append(Finding("error", rel(f, root), f"type 取值非法：{t}"))
        s = meta.get("status")
        if s and s not in STATUSES:
            out.append(Finding("error", rel(f, root), f"status 取值非法：{s}"))
    return out


def check_summary_single_line(files, root: Path) -> list:
    out = []
    for f in files:
        if is_nav(f):
            continue
        lines = f.read_text(encoding="utf-8-sig").splitlines()
        for i, line in enumerate(lines):
            if line.startswith("summary:") and i + 1 < len(lines) and lines[i + 1][:1].isspace():
                out.append(Finding("error", rel(f, root), "summary 必须为单行"))
                break
    return out


def check_long_form_fields(files, root: Path) -> list:
    out = []
    for f in files:
        if is_nav(f):
            continue
        meta = read_meta(f)
        if meta.get("type") in DATE_FIELD_TYPES and not meta.get("decided_at"):
            out.append(Finding("warning", rel(f, root), "长周期文档缺少 decided_at"))
    return out


def check_placeholders(files, root: Path) -> list:
    """只有标题没有正文判 error；正文含「待补充」一类占位判 warning。

    不用「正文行数下限」是因为短文档是合法的，会误伤。
    """
    out = []
    for f in files:
        if is_nav(f):
            continue
        body = parse_frontmatter(f.read_text(encoding="utf-8-sig"))[1]
        meaningful = [ln for ln in body.splitlines() if ln.strip() and not ln.startswith("#")]
        if not meaningful:
            out.append(Finding("error", rel(f, root), "空占位文档：只有标题没有正文"))
        elif any(PLACEHOLDER_RE.match(ln) for ln in meaningful):
            out.append(Finding("warning", rel(f, root), "正文含占位内容"))
    return out


def check_superseded_adr(files, root: Path) -> list:
    out = []
    for f in files:
        meta = read_meta(f)
        if meta.get("type") == "adr" and meta.get("status") == "superseded":
            body = parse_frontmatter(f.read_text(encoding="utf-8-sig"))[1]
            if not LINK_RE.search(body):
                out.append(Finding("warning", rel(f, root), "superseded 的 ADR 应链接到替代它的 ADR"))
    return out


# --- 结构级检查 ---------------------------------------------------------

def parse_exemptions(text: str) -> set:
    names, inside = set(), False
    for line in text.splitlines():
        if line.startswith("#"):
            inside = line.lstrip("#").strip() == EXEMPT_HEADING
            continue
        if inside:
            m = re.match(r"^\s*[-*]\s+`?([^`\s]+?)`?\s*$", line)
            if m:
                names.add(m.group(1).strip().rstrip("/"))
    return names


def iter_md(docs: Path, exempt: set):
    for f in sorted(docs.rglob("*.md")):
        parts = f.relative_to(docs).parts[:-1]
        if any(p in exempt for p in parts):
            continue
        yield f


def check_dir_readmes(docs: Path, exempt: set, root: Path) -> list:
    """每个非空目录都要有 README。

    只含子目录的中间层也要——否则它在上级目录的索引里不可见（生成器跳过没有 README 的子目录），
    整棵子树会从导航中消失。空目录同样报错。
    """
    out = []
    seen = set()
    for p in sorted(docs.rglob("*")):
        parts = p.relative_to(docs).parts
        if any(part in exempt for part in parts):
            continue
        if p.is_file():
            seen.add(p.parent)
            continue
        if p == docs:
            continue
        seen.add(p)
        if not any(p.iterdir()):
            out.append(Finding("error", rel(p, root), "空目录：不建没有内容的目录"))
    seen.discard(docs)
    for d in sorted(seen):
        if not (d / "README.md").exists():
            out.append(Finding("error", rel(d, root), "目录非空但缺少 README.md"))
    return out


def check_links(files, root: Path) -> list:
    out = []
    for f in files:
        text = COMMENT_RE.sub("", f.read_text(encoding="utf-8-sig"))
        for target in LINK_RE.findall(text):
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (f.parent / target).exists():
                out.append(Finding("error", rel(f, root), f"相对链接目标不存在：{target}"))
    return out


def check_orphans(docs: Path, exempt: set, root: Path) -> list:
    out = []
    for f in iter_md(docs, exempt):
        if is_nav(f):
            continue
        index = f.parent / "README.md"
        if not index.exists():
            continue
        if f.name not in COMMENT_RE.sub("", index.read_text(encoding="utf-8-sig")):
            out.append(Finding("error", rel(f, root), "孤儿文档：未被同目录 README 引用"))
    return out


def check_agents_paths(root: Path) -> list:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return [Finding("error", "AGENTS.md", "缺少 AGENTS.md")]
    out = []
    text = COMMENT_RE.sub("", agents.read_text(encoding="utf-8-sig"))
    for p in CODE_PATH_RE.findall(text):
        if not (root / p).exists():
            out.append(Finding("error", "AGENTS.md", f"引用的路径不存在：{p}"))
    return out


def collect(docs: Path, exempt: set):
    files = list(iter_md(docs, exempt))
    return [f for f in files if not is_nav(f)], files


def check_index_sync(root: Path) -> list:
    """检查由 gen_index.py 生成的索引区是否与 frontmatter 同步。

    gen_index 与 verify_docs 互相引用会成环，所以这里做函数内延迟导入：
    gen_index 在模块级导入 verify_docs，而本函数只在 verify_docs 装载完成后才执行。
    gen_index.py 不存在时静默跳过——只拷贝 verify_docs 的项目仍可正常使用。
    """
    try:
        from gen_index import out_of_sync
    except ImportError:
        return []
    return [Finding("error", path, message) for path, message in out_of_sync(root)]


def check_gen_notes(files, root: Path) -> list:
    """模板里写给生成方的指令不应出现在产物中。

    `<!-- gen-note: ... -->` 是生成指令（例如「这一节没有内容就删掉」），
    生成时必须一并清除。残留说明生成方没做完，而且读代码的人会看到自相矛盾的注释。
    """
    out = []
    for f in files:
        if GEN_NOTE_RE.search(f.read_text(encoding="utf-8-sig")):
            out.append(Finding("error", rel(f, root), "模板生成指令未清理（gen-note）"))
    return out


def run(root: Path) -> list:
    docs = root / "docs"
    readme = docs / "README.md"
    if not readme.exists():
        return [Finding("error", "docs/README.md", "缺少 docs/README.md")]

    exempt = BUILTIN_EXEMPT | parse_exemptions(readme.read_text(encoding="utf-8-sig"))
    doc_files, all_files = collect(docs, exempt)
    # 根 README 与 AGENTS.md 同样是体系的一部分，链接与生成指令一并检查
    root_files = [p for p in (root / "README.md", root / "AGENTS.md") if p.exists()]
    scanned = all_files + root_files

    out: list = []
    out += check_frontmatter(doc_files, root)
    out += check_summary_single_line(doc_files, root)
    out += check_long_form_fields(doc_files, root)
    out += check_placeholders(doc_files, root)
    out += check_dir_readmes(docs, exempt, root)
    out += check_links(scanned, root)
    out += check_orphans(docs, exempt, root)
    out += check_agents_paths(root)
    out += check_superseded_adr(doc_files, root)
    out += check_gen_notes(scanned, root)
    out += check_index_sync(root)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    findings = run(root)
    for f in findings:
        print(f"{f.level.upper()} {f.path}: {f.message}")
    errors = sum(1 for f in findings if f.level == "error")
    warnings = len(findings) - errors
    print(f"\n{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
