---
name: scaffolding-project-docs
description: 在需要为项目建立或整理文档与工程规范体系时使用：新项目初始化 docs 目录结构；首次开发任务时补齐 AGENTS.md 与编码、Git 规范；项目中途建立、完善或重整已有文档目录；把散落的 Markdown 纳入统一体系并补元数据与索引。适用于任意技术栈。
---

# 项目文档体系

## 概述

把项目的文档与工程规范整理成一套可被 AI 高效消费的体系：目录结构、元数据、规范分片、AI 路由入口。

三条硬约束贯穿始终：**不覆盖**任何已有正文、**不自动移动**任何文件、**不建**空目录或占位文档。

## 模式判定

| 模式 | 判定条件 | 做什么 |
|---|---|---|
| M1 初始化 | 新项目，或首次开发任务且无 `docs/` | 建立体系 |
| M2 纳管 | 已有 `docs/`，或根目录有散落 Markdown | 盘点出方案，逐项确认后执行 |
| M3 仅规范 | 用户只要编码或 Git 规范 | 只处理 `standards/` |

判不准就先问。M1 与 M2 差别很大，方向做错会浪费一整轮。

## M1：初始化

1. 探测技术栈与项目形态——读 `package.json`、`pom.xml`、`pyproject.toml`、`Cargo.toml` 等
2. 读 `references/structure.md`，算出**必备集**与**按需集**
3. 必备集直接建；按需集整理成「拟建目录 + 启用理由」清单，**一次性请用户确认**
4. 建 `docs/`，用 `assets/templates/_docs-readme.md` 生成 `docs/README.md`，按项目实际情况删减目录表行
5. 用户要规范时：读 `references/standards.md`，按技术栈选分片拷入 `docs/development/standards/`，并**删除 frontmatter 里的 `applies_when`**
6. 用 `assets/templates/_agents.md` 生成根 `AGENTS.md`；已存在则追加合并，**不替换**
7. 启用了 ADR 等长周期文档时，按 `assets/templates/` 建 `docs/templates/`
8. 根 `README.md`、`CHANGELOG.md` 仅缺失时创建
9. 跑自检，然后报告：建了什么、为什么、下一步该写什么

## M2：纳管

完整流程见 `references/retrofit.md`。要点：

1. **只读盘点**——不改任何文件
2. 出四类方案：保留原地 / 建议移动 / 建议合并废弃 / 明确不管
3. **逐项确认**，只执行确认过的
4. 执行：`git mv` → 全局搜索并修复相对链接 → 按映射表补 frontmatter → 建目录 README
5. 旧到新路径映射表写进 `docs/README.md` 末尾
6. 跑自检并报告

**开工前先确认工作区干净。**

## M3：仅规范

1. 读 `references/standards.md`，判断用哪种来源：拷分片 / 从现状反向提取 / 合并
2. 建 `docs/development/standards/`，写入选定的分片
3. 更新 `AGENTS.md` 的路由行；没有 `AGENTS.md` 就从 `assets/templates/_agents.md` 生成

## 安全铁律

1. 不覆盖、不改写任何已有正文
2. 不移动或重命名未确认的文件；移动必须走 `git mv`
3. 已有 `AGENTS.md` / `CLAUDE.md` 一律追加合并，绝不替换
4. 不建空目录、不建占位文档
5. 外部工具目录识别但不动
6. 目标文件已存在就**停下报告**，不静默跳过
7. 迁移前要求工作区干净，不干净就先让用户提交或 stash

违反规则的字面意思就是违反规则的精神。

## 自检

生成或修改完成后必须运行：

```bash
python <skill目录>/scripts/verify_docs.py <项目根目录>
```

- `error` 必须修到清零；`warning` 逐条判断
- `AGENTS.md` 引用的路径必须全部存在——这是最伤的一种坏法，AI 会照它去读
- 校验脚本不修改任何文件，只报告

## 资源导航

| 什么时候读 | 读哪个 |
|---|---|
| 决定要建哪些目录 | `references/structure.md` |
| 写 README 或补 frontmatter | `references/metadata.md` |
| 项目已有文档，要整理 | `references/retrofit.md` |
| 选规范、加分片、回写模板 | `references/standards.md` |
| 加模板或导入外部模板 | `references/resources.md` |
| 写 ADR，或发现 ADR 与实现不符 | `references/adr.md` |

模板在 `assets/templates/`，规范分片在 `assets/standards/`。**先列目录再取用**，不要假设有哪些文件。
