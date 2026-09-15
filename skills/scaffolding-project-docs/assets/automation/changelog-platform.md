---
title: 发布说明的生成（托管平台）
type: standard
status: active
summary: 用代码托管平台自带的发布说明生成能力产出 release notes，零安装。
applies_when: 项目托管在 GitHub 或 GitLab，且以平台 Release 作为发布渠道
---

# 发布说明的生成（托管平台）

## 什么时候用这条

平台自带的生成能力**不需要安装任何东西**，是三条路里成本最低的一条。适用条件：

- 仓库托管在 GitHub 或 GitLab
- 发布以平台 Release 为渠道（使用者从 Release 页下载或查看变更）
- 合并请求 / PR 的标题写得有信息量（生成质量完全取决于它）

不适用的情况：以包管理器为主要分发渠道（npm、PyPI、Maven Central）。那种场景使用者看的是
包页与仓库内文件，仓库内的 `CHANGELOG.md` 才是有意义的那一份。

## GitHub

```bash
gh release create v0.2.0 --generate-notes
```

- 从**上一个 Release 之后**合入的 PR 自动汇总，按贡献者与标签分组
- 用 `--notes-start-tag <tag>` 显式指定起始点
- 用仓库根的 `.github/release.yml` 配置分类规则（按标签分组、排除某些标签或作者）
- `--notes-file` 可以完全接管，用于手工补充

`.github/release.yml` 是这条路的"配置"——相当于 git-cliff 的 `cliff.toml`，
但它是平台侧的，不需要本地工具链。

## GitLab

```bash
glab release create v0.2.0 --notes "..."      # 手工指定
```

GitLab 在 Release 页面提供「生成发布说明」能力，按提交与关联的 issue/MR 汇总，
也可以通过 API 触发。分类规则由 `.gitlab/release.yml` 配置。

## 与仓库内 CHANGELOG 的分工

这两者**互补，不是替代**：

| | 平台 Release notes | 仓库内 `CHANGELOG.md` |
|---|---|---|
| 位置 | 平台，需要联网看 | 随代码走，离线可查 |
| 读者 | 下载者、使用者 | 开发者、审阅者、下游集成方 |
| 生成 | 平台从 PR 汇总 | changesets / git-cliff |
| 适合 | 面向使用者的版本公告 | 面向开发者的完整变更记录 |

判断标准是**分发渠道**：

- 通过平台 Release 分发 → 平台生成即可满足使用者，仓库内 CHANGELOG 可省
- 通过包管理器分发 → 仓库内 CHANGELOG 必须有，平台 notes 是附赠
- 两者都是 → 两条都启用，但要接受它们在措辞上不会完全一致

**不要为了"两边一致"而手工同步。** 它们服务不同读者，措辞本来就该不同。

## 与 docs/releases/ 的关系

`docs/releases/` 存放需要长期归档的发布说明、升级事项与验收证据。
若平台 Release 已经能表达清楚，就不要重复启用 `docs/releases/`——两者二选一。
