# {{PROJECT_NAME}} 文档中心

这里是本项目的统一文档入口。文档描述当前代码与公开契约；历史决策与发布记录只说明当时发生了什么。

<!-- 按项目实际的读者角色增删条目；目标尚未启用的条目由生成器自动隐藏，不必手工删 -->

## 我想……

<!-- gen:nav:start -->
- **安装并使用系统** → [用户指南](guides/user/README.md)
- **开发扩展** → [开发者指南](guides/developer/README.md)
- **参与项目开发** → [开发文档](development/README.md)
- **理解系统设计** → [架构文档](development/architecture/README.md)
- **查精确字段或契约** → [参考资料](guides/reference/README.md)
<!-- gen:nav:end -->

## 目录

<!-- gen:subdirs:start -->
<!-- gen:subdirs:end -->

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

各目录 `README.md` 里的索引表**由生成器维护**，不要手写。

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
