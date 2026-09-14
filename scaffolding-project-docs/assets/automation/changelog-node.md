---
title: 版本与发布记录的生成（Node 工作区）
type: standard
status: active
summary: 用 changesets 从变更集生成版本号、包级 CHANGELOG 与发布说明。
applies_when: 项目使用 Node，且以 npm / pnpm / yarn 工作区组织
---

# 版本与发布记录的生成（Node 工作区）

## 原则

版本号与 CHANGELOG **由工具从变更集生成**，不手写。手写的 CHANGELOG 会在第三个版本之后
开始说谎。

## 初始化

```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
```

`changeset init` 会生成 `.changeset/` 目录与配置文件。

## 日常流程

1. **改动时**：每完成一项面向使用者的变更，执行 `pnpm changeset`，回答三个问题——
   影响哪些包、是 major / minor / patch、给使用者的说明是什么。生成的变更集文件**随 PR 一起提交**。
2. **发版时**：`pnpm changeset version` 消费全部变更集，自动更新各包版本号并生成包级 `CHANGELOG.md`。
3. **发布**：`pnpm changeset publish` 发布到 registry 并打 tag。

CI 中可以拆成两步：PR 中只校验「有没有带变更集」，合入主干后才执行 `version` 与 `publish`。

## 版本号判定

- **公共契约的破坏性变更走 major**，严禁混入 minor。
- 仅新增能力走 minor；修复与内部改动走 patch。

这条比 semver 规范本身更严格，因为契约破坏在下游是编译期或运行期的硬失败。

## 根 CHANGELOG

changesets 默认生成**每个包**的 `CHANGELOG.md`，不生成仓库根目录的汇总文件。
需要根级汇总时，二选一：

- 用 `@changesets/changelog-github` 之类的生成器，让变更集内容更完整，再写一个脚本汇总到根
- 直接以各包的 `CHANGELOG.md` 为准，根目录不放汇总文件

**不要**为了"看起来完整"而在根目录手写一份汇总——它会立刻与包级记录脱节。

## 与 docs/releases/ 的关系

`docs/releases/` 只放发布说明、升级事项与验收证据，**通用开发与发布流程不放进版本目录**。
若 CHANGELOG 已经能表达清楚，就不要重复启用 `docs/releases/`——两者二选一。
