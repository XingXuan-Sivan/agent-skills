# {{PROJECT_NAME}} 文档中心

这里是本项目的统一文档入口。文档描述当前代码与公开契约；历史决策与发布记录只说明当时发生了什么。

## 我想……

- **安装并使用系统** → [用户指南](guides/user/README.md)
- **开发扩展** → [开发者指南](guides/developer/README.md)
- **参与项目开发** → [开发流程](development/README.md)
- **理解系统设计** → [架构文档](development/architecture/README.md)
- **查精确字段或契约** → [参考资料](guides/reference/README.md)
- **查看某次发布** → [发布资料](releases/README.md)

## 目录职责

| 目录 | 收录什么 |
|---|---|
| `guides/user/` | 面向使用者的安装、使用与配置说明 |
| `guides/developer/` | 面向外部接入方的扩展开发说明 |
| `guides/faq/` | 高频问题 |
| `guides/reference/` | 配置项、环境变量、事件与钩子索引 |
| `development/standards/` | 编码、Git 等强制约定 |
| `development/architecture/` | 当前有效的系统设计 |
| `development/decisions/` | 历史技术决策记录 |
| `development/rfcs/` | 尚未定稿的提案 |
| `development/requirements/` | 已冻结的需求基线 |
| `operations/` | 测试策略与性能记录 |
| `api/` | 对外提供的接口契约 |
| `templates/` | 各类文档的模板 |
| `assets/` | 文档引用的图片与附件 |
| `releases/` | 版本归档 |

> 上表只保留本项目实际启用的目录；未启用的行必须删除。

## 元数据规范

除 `README.md` 外，每篇文档开头必须有 frontmatter：

```yaml
---
title: 文档标题
type: standard        # standard|guide|reference|architecture|adr|rfc|design|requirement|release
status: active        # draft|active|deprecated|superseded|rejected
summary: 一句话说明本文内容，必须单行。
---
```

- `summary` 必须与正文首段一致；改正文时同步修改。
- `status` 是唯一允许「只改元数据、不改正文」的字段。
- 长周期文档（`adr`/`rfc`/`design`/`architecture`）另加 `related`；`adr` 另加 `supersedes`；`adr`/`rfc` 另加 `decided_at`。
- `sources` 选填，用于标注本文对应的代码或配置路径。

## 事实源

发生不一致时依次核对：

1. 实际代码、配置 Schema 和自动化测试
2. 对外契约与字段说明
3. 当前系统设计文档
4. 面向任务的指南
5. README 与导航页
6. 历史 ADR 和发布记录

发现文档与实现不一致时，修正文档或实现，并补一条能阻止再次偏离的局部验证。

## 不纳入索引的目录

以下目录由外部工具维护，不属于本体系，不参与索引与检查：

- `superpowers/`
