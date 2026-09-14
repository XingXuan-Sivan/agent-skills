# 目录结构与按需启用

> 何时读本文：需要决定一个项目要建立哪些文档目录时。这是"视实际情况而定"的具体判据——不靠感觉，靠条件。

## 必备（不建则体系不成立）

| 路径 | 职责 |
|---|---|
| `README.md` | 项目是什么、如何运行、指向 `docs/` |
| `AGENTS.md` | AI 路由入口，不含规范正文 |
| `docs/README.md` | 文档中心索引 + 目录职责 + 元数据规范 + 事实源优先级 + 不纳入索引的目录清单 |

## 按需（有真实内容才建，空目录不建）

| 路径 | 启用条件 |
|---|---|
| `docs/development/standards/` | 用户要求添加编码或 Git 规范 |
| `docs/guides/user/` | 存在非开发者使用者，需要安装、使用或配置说明 |
| `docs/guides/developer/` | 存在外部接入方，如插件、SDK、扩展开发 |
| `docs/guides/faq/` | 问答累积到 5 条以上，或用户明确要求 |
| `docs/guides/reference/` | 配置项、环境变量、事件或钩子量大到超过一页 |
| `docs/development/architecture/` | 系统有可描述的顶层结构，如多模块、多进程、有状态流 |
| `docs/development/decisions/` | 出现第一个「有取舍、以后会被问为什么」的技术决策 |
| `docs/development/rfcs/` | 需要先讨论再落地的提案；小项目可省，直接写 ADR |
| `docs/development/requirements/` | 需要冻结的需求基线，如验收或多人协作 |
| `docs/development/workflow.md` | 项目分支模型、发布流程或 CI 与默认约定不同时 |
| `docs/operations/testing/` | 测试策略复杂到超出规范里几句话 |
| `docs/operations/performance/` | 有性能指标、压测或调优记录 |
| `docs/api/` | 对外提供的接口契约；内部接口不算 |
| `docs/templates/` | 文档类型多到需要模板；有 ADR 就该有 |
| `docs/assets/` | 文档引用图片、图表或附件 |
| `docs/releases/` | 有对外发布版本，且与根 `CHANGELOG.md` 二选一 |

## 硬规则

1. **不建空目录、不建占位 README。** 一个目录被创建，当且仅当它至少有一篇真实内容。这条同时解决「占位文档腐烂」和「AI 读到空壳」两个问题。
2. 项目内的 `docs/templates/` 是给写文档的人用的模板；本 skill 的 `assets/templates/` 是生成这些模板的来源。两者不混用。
3. `docs/releases/` 与根 `CHANGELOG.md` 二选一：对外发布且需归档验收证据用 `releases/`；纯迭代记录用 `CHANGELOG.md`。
4. 单篇文档不单独建目录。

## 生成时的做法

- **必备集**直接创建。
- **按需集**先算出「拟建目录 + 每条的启用理由」，一次性交给用户确认，确认后才建。
- 项目已有的 `README.md`、`CHANGELOG.md` 只在缺失时创建；已存在则一字不改。
