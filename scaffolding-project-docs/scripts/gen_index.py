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


def regenerate(readme: Path, exempt: set) -> str:
    text = read(readme)
    directory = readme.parent

    def replace(m: re.Match) -> str:
        start, kind, end = m.group(1), m.group(2), m.group(4)
        body = render_docs(directory) if kind == "docs" else render_subdirs(directory, exempt)
        return f"{start}\n{body}\n{end}" if body else f"{start}\n{end}"

    return BLOCK_RE.sub(replace, text)


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
    return [(p.relative_to(root).as_posix(), "索引生成区与 frontmatter 不同步") for p, _ in updates]


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
            print(f"ERROR {rel}: 索引生成区与 frontmatter 不同步")
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
