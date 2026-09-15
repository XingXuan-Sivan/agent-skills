# skills.sh 发现指南

## 概述

skills.sh（https://skills.sh）是 Skills 生态的聚合发现平台，汇集了来自 GitHub 的 48,000+ Skills。它是 init-skills 进行实时检索、比对和推荐的核心数据源。本文档说明如何通过 skills.sh 高效发现和评估 Skills。

> **核心理念**：不再维护静态的仓库源清单。所有 Skill 的发现、评估、对比都通过 skills.sh 实时完成，确保推荐始终反映社区最新动态。

## skills.sh 核心功能

### 1. 热榜（Trending）

展示当前社区增长最快、最受关注的 Skills。适合：
- 发现新兴的、正处于上升期的 Skill
- 了解社区当前的热门方向
- 寻找"大家都在用什么"

### 2. 排行榜（Top Rated）

展示长期评分最高、经过大量用户验证的 Skills。适合：
- 寻找成熟稳定的高质量 Skill
- 在多个同类 Skill 之间做选择时的质量参考
- 优先选择经过社区长期检验的 Skill

### 3. 分类浏览

按功能领域浏览 Skills：
- 文档处理（docx、pdf、xlsx、pptx 等）
- 开发技术（前端、后端、API、测试、MCP 等）
- 创意设计（艺术、UI、动图等）
- 通用办公（内部沟通、文档协同等）
- 部署运维（Vercel、CI/CD 等）
- 浏览器自动化
- 数据分析
- 更多…

### 4. 关键词搜索

直接搜索 Skill 名称或功能关键词，快速定位目标 Skill。

## 使用 skills.sh 进行 Skill 评估

在 init-skills 第四层（按需实时推荐）中，应综合以下维度评估候选 Skill：

### 评估维度

| 维度 | 权重 | 数据来源 | 说明 |
|------|------|---------|------|
| 热榜排名 | 中 | skills.sh Trending | 反映当前活跃度和社区兴趣 |
| 综合评分 | 高 | skills.sh Top Rated | 反映长期质量和用户满意度 |
| Star 数 | 高 | skills.sh / GitHub | 社区认可度的直接指标 |
| 更新频率 | 高 | skills.sh / GitHub | 最近 6 个月内有更新为佳 |
| 维护方背景 | 中 | GitHub 仓库信息 | 官方 > 知名团队 > 活跃个人 |
| 文档完整度 | 中 | SKILL.md 内容 | 使用说明、示例、依赖声明是否齐全 |

### 推荐阈值建议

- **强烈推荐**：热榜前 20 且综合评分 ≥ 4.5，或 Star ≥ 1,000
- **推荐**：热榜前 50 且综合评分 ≥ 4.0，或 Star ≥ 500
- **可关注**：热榜前 100 或综合评分 ≥ 3.5，近 3 个月有更新
- **谨慎**：评分 < 3.0 或超过 6 个月未更新

### 交叉比对流程

当用户有具体需求时，应按以下流程交叉比对：

```
1. 在 skills.sh 搜索用户需求关键词
   ↓
2. 提取搜索结果中排名前 10 的 Skill
   ↓
3. 逐个查看：热榜位置、综合评分、Star 数、最近更新时间
   ↓
4. 对照用户场景，筛选出 5-8 个最匹配的候选
   ↓
5. 向用户展示并附上推荐理由
   ↓
6. 用户勾选后执行安装
```

## 与 npx skills CLI 的配合

skills.sh 负责"发现"，`npx skills` CLI 负责"安装"：

```
skills.sh（浏览器）                  npx skills CLI（终端）
─────────────────────────          ───────────────────────
浏览热榜 / 排行榜                   npx skills find <keyword>
按分类筛选                          npx skills add <source>@<name>
查看评分、Star、更新记录            npx skills list
对比候选 Skill                      npx skills init
```

两者可以交替使用：在 skills.sh 上找到目标 Skill 后，记录其 GitHub 仓库路径（owner/repo@name），然后通过 CLI 安装。

## 注意事项

- skills.sh 上的 Skill 来自公开 GitHub 仓库，**不代表官方认证**，安装前仍需进行安全审查（见 `references/security.md`）
- 热榜数据实时变动，同一 Skill 在不同时间的排名可能差异较大，建议以综合评分为主要参考
- 对于特定领域（如中文处理、国内生态），skills.sh 的覆盖可能不如通用领域全面，此时可结合 `npx skills find` 直接搜索补充
- skills.sh 无需 Node.js 环境，浏览器即可访问，是 CLI 不可用时的备选发现渠道
