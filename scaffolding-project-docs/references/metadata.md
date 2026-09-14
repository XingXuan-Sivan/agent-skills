# 元数据与渐进式披露

> 何时读本文：需要写 `docs/README.md`、目录 `README.md`，或给已有文档补元数据时。

## 三层结构

| 层 | 位置 | 承担什么 |
|---|---|---|
| L1 | 根 `AGENTS.md` | AI 的第一入口。只有路由与硬约束，**不放任何规范正文** |
| L2 | 各目录 `README.md` | 导航。一段职责说明 + 一张清单表 |
| L3 | 单篇文档 | frontmatter 元数据 + 正文 |

AI 的读取路径是 L1 → 按路由直接跳到 1–2 篇 L3 文档；L2 是给人浏览和给 AI 兜底用的。

## L1：AGENTS.md

控制在 20–40 行，结构固定为三段：

1. **必读**：`docs/development/standards/universal.md`（若启用了规范）
2. **按任务类型追加阅读**：每行一个「任务类型 → 路径」
3. **工作约束**：事实源优先级、只改任务范围内、保留已有改动、未经授权不推送不发布不合入主干、改完运行相称的验证

生成时必须按项目实际启用的分片与文档**删减路由行**。写完立刻跑校验，确认引用的路径都存在——`AGENTS.md` 指向不存在的文件是这套体系最伤的一种坏法，因为 AI 会照它去读。

## L2：目录 README

一段该目录职责说明 + 表格：`文档 | 一句话 | 何时读 | 状态`。

**不重复 frontmatter 的 `summary`。** L2 是导航，L3 才是内容；两层都写一遍就是两处要同步维护的冗余。

## L3：frontmatter

必填 4 字段：

```yaml
---
title: 后端编码规范
type: standard        # standard|guide|reference|architecture|adr|rfc|design|requirement|release
status: active        # draft|active|deprecated|superseded|rejected
summary: 后端代码的强制约定——分层、注入、配置、日志与边界检查。
sources:              # 选填：事实源路径，帮 AI 定位代码
  - src/main/java/**/controller
---
```

长周期文档（`adr` / `rfc` / `design` / `architecture`）额外字段：

| 字段 | 适用于 | 含义 |
|---|---|---|
| `related` | 全部长周期 | 相关文档的相对路径 |
| `supersedes` | 仅 `adr` | 被本文替代的 ADR |
| `decided_at` | `adr` / `rfc` | 决策日期 `YYYY-MM-DD` |

取值约定：ADR 的「已接受」用 `active`；被否决的提案用 `rejected`，否决记录本身有价值，不要删除。

**`README.md` 豁免**：所有 `README.md`（含 `docs/README.md` 与各目录 README）是导航文件，不写 frontmatter。它们的元数据由 L1 路由与 L2 表格承担，再写一层是冗余。

## 防腐化规则

- `summary` 必须单行，且与正文首段一致；改正文必须同步改 `summary`。
- **`status` 是唯一允许「只改元数据、不改正文」的字段**，承载 ADR 的决策状态更新。
- `sources` 选填；填就只写最该看的几个路径，不追求全量。
- 禁止把 frontmatter 当元数据仓库堆字段。加字段前先问：它会不会在三个月后变成谎言。

## 事实源优先级（写进 `docs/README.md`）

```
1. 实际代码、配置 Schema 和自动化测试
2. reference / api 中的契约与字段说明
3. architecture 中的当前系统设计
4. 面向任务的指南
5. README 与导航页
6. 历史 ADR 和发布记录
```

发现文档与实现不一致时，修正文档或实现，并补一条能阻止再次偏离的局部验证。

## 旧 frontmatter 字段映射

已有项目可能使用另一套 frontmatter，遇到时不覆盖原值，按映射转换后再补缺：

| 旧字段 | 处理 |
|---|---|
| `description` | → `summary`（直迁） |
| `status: accepted` | → `status: active` |
| `date` | → `decided_at`（仅 `adr` / `rfc`），其余类型丢弃 |
| `name` | 丢弃，文件名即标识 |
| `version` | 丢弃，版本控制历史已覆盖 |
| 缺 `title` | 从 H1 提取 |
| 缺 `type` | 按所在目录与正文判定 |

映射规则按项目实际情况扩展。遇到无法判断的字段，**保留原值并在方案里单独列出**，由用户裁决。
