#!/usr/bin/env python3
"""根据 frontmatter 生成目录 README 的索引区块。

索引表是 frontmatter 的投影——标题、一句话、状态全部取自文档自身，
因此索引永远不会和文档脱节，也不需要人工维护。

生成区用 HTML 注释标记，人写的职责说明留在标记之外：

    <!-- gen:docs:start -->
    | 文档 | 一句话 | 状态 |
    |---|---|---|
    | [通用开发规范](universal.md) | 架构、配置、注释与交付质量 | active |
    <!-- gen:docs:end -->

用法：
    python gen_index.py [项目根目录]           写入所有 README 的生成区
    python gen_index.py [项目根目录] --check   只校验是否同步，不写入

退出码：--check 模式下存在不同步返回 1。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from verify_docs import BUILTIN_EXEMPT, is_nav, parse_exemptions, read_meta

BLOCK_RE = re.compile(
    r"(<!-- gen:(docs|subdirs):start -->)(.*?)(<!-- gen:(?:docs|subdirs):end -->)",
    re.S,
)
NAV_BLOCK_RE = re.compile(
    r"(<!-- gen:nav:start -->)(.*?)(<!-- gen:nav:end -->)",
    re.S,
)
NAV_LINK_RE = re.compile(r"\]\(([^)\s#]+)\)")
NAV_OFF_PREFIX = "<!-- gen:nav-off: "
NAV_OFF_SUFFIX = " -->"
DOCS_HEADER = "| 文档 | 一句话 | 状态 |\n|---|---|---|"
SUBDIRS_HEADER = "| 目录 | 职责 |\n|---|---|"


def read(path: Path) -> str:
    """统一按 utf-8-sig 读取，容忍 Windows 常见的 BOM。"""
    return path.read_text(encoding="utf-8-sig")


def write_preserving_eol(path: Path, text: str) -> None:
    """保留文件原有的换行风格，避免在 Windows 上制造整文件差异。"""
    newline = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
    path.write_bytes(text.replace("\n", newline).encode("utf-8"))


def first_paragraph(readme: Path) -> str:
    """取 README 中标题之后的第一段，作为该目录的一句话职责。"""
    for line in read(readme).splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "<!--", "|", ">", "-")):
            continue
        return s
    return ""


def render_docs(directory: Path) -> str:
    rows = []
    for f in sorted(directory.glob("*.md")):
        if is_nav(f):
            continue
        meta = read_meta(f)
        title = meta.get("title") or f.stem
        rows.append(
            f"| [{title}]({f.name}) | {meta.get('summary', '')} | {meta.get('status', '')} |"
        )
    return DOCS_HEADER + "\n" + "\n".join(rows) if rows else ""


def render_subdirs(directory: Path, exempt: set) -> str:
    rows = []
    for sub in sorted(p for p in directory.iterdir() if p.is_dir()):
        if sub.name in exempt or sub.name.startswith("."):
            continue
        readme = sub / "README.md"
        if not readme.exists():
            continue  # 缺 README 由 verify_docs 报错，这里不重复
        rows.append(f"| [{sub.name}]({sub.name}/README.md) | {first_paragraph(readme)} |")
    return SUBDIRS_HEADER + "\n" + "\n".join(rows) if rows else ""


def nav_targets(line: str) -> list:
    """取出一行里的相对链接目标；外部链接与锚点不参与存在性判断。"""
    return [
        t
        for t in NAV_LINK_RE.findall(line)
        if "://" not in t and not t.startswith(("mailto:", "#"))
    ]


def process_nav(body: str, base: Path) -> str:
    """按目标是否存在，启停导航区的条目。

    导航条目由人写（角色标签是人给的），但目标目录未必已启用。直接留着就是死链，
    直接删掉又会在目录建好后找不回来。所以采取**注释隐藏**而非删除：
    目标不存在时整行包进 `gen:nav-off` 注释，目标一旦出现就自动恢复。
    """
    out = []
    for raw in body.strip("\n").splitlines():
        line = raw.strip()
        hidden = line.startswith(NAV_OFF_PREFIX) and line.endswith(NAV_OFF_SUFFIX)
        inner = line[len(NAV_OFF_PREFIX):-len(NAV_OFF_SUFFIX)].strip() if hidden else line

        if not inner.startswith(("-", "*")):
            out.append(raw)  # 非条目行（标题、说明）原样保留
            continue

        targets = nav_targets(inner)
        alive = all((base / t).exists() for t in targets) if targets else True
        out.append(inner if alive else NAV_OFF_PREFIX + inner + NAV_OFF_SUFFIX)
    return "\n".join(out)


def regenerate(readme: Path, exempt: set) -> str:
    text = read(readme)
    directory = readme.parent

    def replace_block(m: re.Match) -> str:
        start, kind, end = m.group(1), m.group(2), m.group(4)
        body = render_docs(directory) if kind == "docs" else render_subdirs(directory, exempt)
        return f"{start}\n{body}\n{end}" if body else f"{start}\n{end}"

    def replace_nav(m: re.Match) -> str:
        return f"{m.group(1)}\n{process_nav(m.group(2), directory)}\n{m.group(3)}"

    return NAV_BLOCK_RE.sub(replace_nav, BLOCK_RE.sub(replace_block, text))


def nav_hidden(text: str) -> int:
    """统计被隐藏的导航条目数，供报告使用。"""
    return sum(
        line.strip().startswith(NAV_OFF_PREFIX)
        for m in NAV_BLOCK_RE.finditer(text)
        for line in m.group(2).splitlines()
    )


def target_readmes(docs: Path, exempt: set) -> list:
    return [
        p
        for p in sorted(docs.rglob("README.md"))
        if not any(part in exempt for part in p.relative_to(docs).parts[:-1])
    ]


def compute(root: Path):
    """返回 (待更新列表, 缺生成区列表)。待更新列表元素为 (路径, 新内容)。"""
    docs = root / "docs"
    readme = docs / "README.md"
    if not readme.exists():
        return [], []
    exempt = BUILTIN_EXEMPT | parse_exemptions(read(readme))

    updates, missing = [], []
    for rm in target_readmes(docs, exempt):
        old = read(rm)
        if not BLOCK_RE.search(old):
            missing.append(rm)
            continue
        new = regenerate(rm, exempt)
        if new != old:
            updates.append((rm, new))
    return updates, missing


def out_of_sync(root: Path) -> list:
    """供 verify_docs 调用：返回 [(相对路径, 说明)]。"""
    updates, _ = compute(root)
    return [(p.relative_to(root).as_posix(), "索引区与源不同步（文档或导航目标已变）") for p, _ in updates]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    check = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path.cwd()

    updates, missing = compute(root)

    if missing:
        for p in missing:
            print(f"WARN {p.relative_to(root).as_posix()}: 缺少生成区标记，索引无法自动维护")
    for p, new in updates:
        rel = p.relative_to(root).as_posix()
        if check:
            print(f"ERROR {rel}: 索引区与源不同步")
        else:
            write_preserving_eol(p, new)
            print(f"UPDATED {rel}")

    if check:
        print(f"\n{len(updates)} file(s) out of sync, {len(missing)} warning(s)")
        return 1 if updates else 0
    print(f"\n{len(updates)} file(s) updated, {len(missing)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
