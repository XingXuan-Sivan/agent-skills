---
title: 版本与发布记录的生成（通用）
type: standard
status: active
summary: 用 git-cliff 基于约定式提交在任意技术栈生成 CHANGELOG。
applies_when: 项目使用 Git，且提交信息遵循约定式格式
---

# 版本与发布记录的生成（通用）

适用于没有原生版本工具链的技术栈——Python、Java、Rust、Go 或纯脚本项目。

## 原则

CHANGELOG **从提交历史生成**，不手写。前提是提交信息遵循约定式格式，
因此这条规范依赖 `git.md` 中的提交格式约定。

## 工具选择

**git-cliff** 是单文件可执行程序，不绑定技术栈，用 Rust 编写但不需要 Rust 环境：

```bash
cargo install git-cliff        # 有 Rust 工具链时
brew install git-cliff         # macOS
scoop install git-cliff        # Windows
```

也可以直接下载对应平台的二进制放进项目工具目录。选它的理由是**零运行时依赖**——
不需要为了生成 CHANGELOG 而在 Java 项目里引入 Node。

## 初始化

```bash
git-cliff --init          # 生成 cliff.toml
```

把 `cliff.toml` 提交进仓库。默认配置按约定式提交的 type 分组（feat / fix / perf 等），
一般只需要调整分组标题为中文。

## 生成

```bash
# 全量重新生成
git-cliff -o CHANGELOG.md

# 追加未发布的部分，并指定本次版本号
git-cliff --unreleased --tag v0.2.0 --prepend CHANGELOG.md
```

## 与发布流程的衔接

放到发布流程的第 1 步之前：

1. 确定本次版本号（遵循 semver；**公共契约的破坏性变更走 major**）
2. `git-cliff --unreleased --tag <版本号> --prepend CHANGELOG.md`
3. 人工审阅生成的条目——生成器只能汇总提交，无法判断表述是否对使用者有意义
4. 提交 CHANGELOG，再进入构建与打包

**第 3 步不能省。** 生成器的输出质量取决于提交信息质量；审阅是唯一能拦住
「fix: 修了个 bug」这类无信息量条目的环节。

## 与 docs/releases/ 的关系

`docs/releases/` 只放发布说明、升级事项与验收证据，**通用开发与发布流程不放进版本目录**。
若 CHANGELOG 已经能表达清楚，就不要重复启用 `docs/releases/`——两者二选一。
