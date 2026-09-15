---
title: Git 分支与提交规范
type: standard
status: active
summary: 提交格式、分支模型、版本与发布流程、仓库卫生，以及 AI 协作下的约束。
applies_when: 项目使用 Git 管理版本
---

# Git 分支与提交规范

## 1. 提交信息

```
<type>(<scope>): <subject>

<body>
```

- `type`：`feat` / `fix` / `docs` / `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `revert`
- `scope`：受影响的模块或包，可省略
- `subject`：中文，动词开头，不超过 50 字，结尾不加句号
- 示例：`feat(core): 增加流式输出支持`、`fix(ui): 修复多显示器下窗口偏移`

若项目已有稳定的提交惯例，沿用现有惯例，不要强行改写历史风格。

## 2. 分支模型

- `main`：可发布分支。有远程协作者时禁止直接推送，经 PR 合入；纯本地单人项目可直接合并，但**仍须在工作分支上开发**
- 特性分支 `feat/<topic>`；修复分支 `fix/<topic>`
- PR 合并使用 squash，在主干上保留一个清晰提交
- 默认不引入 `develop` / `release` 长期分支；发布打 tag

## 3. 版本

- 遵循语义化版本
- **公共契约的破坏性变更必须走 major**，严禁把破坏性变更混入 minor
- 版本号与 CHANGELOG 由工具生成；具体工具由项目选择

## 4. 发布流程

1. 更新版本号与 CHANGELOG
2. 构建 + 全量测试
3. 打包并生成校验和
4. 发布，并把自动更新配置指向发布源
5. 发布前完成依赖与素材的授权盘点

## 5. 仓库卫生

- `.gitignore` 必须覆盖：依赖目录、构建产物、日志、`.env*`、密钥类配置、本地数据目录
- 密钥类文件**只能**在用户数据目录生成，仓库内只放 `*.example` 模板
- 提交必须经过 hooks 校验，不使用 `--no-verify` 等绕过方式

## 6. AI 协作约束

- **未经用户同意，禁止擅自提交**
- **不要直接在主分支上开发**
- 未经明确授权，不推送、不开 PR、不合入主干、不 force push
- 一个提交一件事，不混入无关的格式化改动
- 不使用会毁掉未提交工作的命令：`git reset --hard`、`git clean -fd`、`git checkout .`

## 项目可覆盖点

以下内容由项目在 `docs/development/workflow.md` 中声明，声明后以项目为准：

- 更重的分支模型（如需要 `develop` 或发布分支）
- `scope` 的具体取值集合
- 版本号与 CHANGELOG 的生成工具
- 发布产物的形态与分发渠道
