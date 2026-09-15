# 第三方 Skill 安全评估指南

## 概述

Skill 本质上是给 AI 的操作指令。某些恶意 Skill 可能包含危险操作（如删除文件、发送数据到外部）。在使用任何第三方 Skill 之前，必须进行安全评估。本文档提供评估维度和检查方法。

> **skills.sh 与安全**：skills.sh 聚合平台上的 Skill 来自公开 GitHub 仓库，不代表官方认证。通过 skills.sh 发现 Skill 后，仍需按照本文档进行安全审查。skills.sh 上的排名、评分和 Star 数可作为来源可信度的参考指标，但不能替代实际审查。

## 安全评估维度

### 1. 安全性（首要）

| 检查项 | 具体操作 | 风险等级 |
|--------|---------|---------|
| 危险命令 | 检查 SKILL.md 和 scripts 中是否包含 `rm -rf`、`del /f`、`format` 等删除/格式化命令 | 严重 |
| 网络请求 | 检查是否向外部发送数据（`curl`、`fetch`、`axios` 等） | 高 |
| 文件操作 | 检查是否有超出 Skill 职责范围的文件读写操作 | 中 |
| 环境变量访问 | 检查是否读取或修改敏感环境变量（密钥、Token 等） | 高 |
| 系统命令 | 检查是否执行 `sudo`、管理员权限命令 | 严重 |
| 依赖安装 | 检查 requirements.txt 或 package.json 中的依赖是否来自可信源 | 中 |

### 2. 维护状态

| 指标 | 安全标准 | 风险提示 |
|------|---------|---------|
| 最近更新时间 | 6 个月内 | 超过 6 个月未更新需谨慎 |
| 作者活跃度 | 近期有提交记录 | 长期无维护的仓库可能存在问题 |
| Issue 响应 | 积极处理 Issue 和 PR | Issue 堆积无人处理说明维护不力 |
| 版本稳定性 | 有明确的版本号和变更日志 | 无版本管理的 Skill 质量不可控 |

### 3. 文档完整性

| 必需项 | 说明 |
|--------|------|
| 清晰的 SKILL.md | 包含完整的使用说明、执行步骤和示例 |
| 输入输出说明 | 明确 Skill 的输入要求和输出格式 |
| 依赖声明 | 如需外部工具或 API，应有明确说明 |
| 错误处理 | 说明常见错误及解决方案 |

### 4. 兼容性

| 检查项 | 说明 |
|--------|------|
| 目标平台 | 确认 Skill 是否适配你使用的 Agent 软件 |
| 依赖版本 | 检查所需工具/库的版本是否与你的环境兼容 |
| 操作系统 | 确认 Skill 中的命令在你的 OS 上可正常执行 |

### 5. 来源可信度

| 可信度等级 | 来源类型 | 识别方式 |
|-----------|---------|---------|
| 最高 | 知名组织/企业官方维护 | skills.sh 上标注为官方、Star ≥ 1,000、长期活跃 |
| 高 | 高排名社区仓库 | skills.sh 热榜前 20 或综合评分 ≥ 4.5 |
| 中 | 活跃社区仓库 | Star ≥ 500、近 3 个月有更新 |
| 低 | 个人仓库 | Star < 100、更新不规律 |
| 未知 | 新仓库 / 信息不全 | 无 Star、无文档、无维护记录，建议避免使用 |

> **提示**：通过 skills.sh 热榜和排行榜可以快速筛选出社区认可的高质量 Skill，但安装前仍需进行本文档描述的安全检查。

## 安全检查流程

### 安装前检查

```
1. 查看 skills.sh 上的 Skill 信息
   - 综合评分、热榜排名、Star 数
   - 最近更新时间、维护活跃度
   - 用户评价和社区反馈

2. 查看 GitHub 仓库首页
   - Issue 数量和处理情况
   - 是否有安全相关的 Issue 或讨论
   - 贡献者数量和活跃度

3. 通读 SKILL.md
   - 是否包含文件删除、系统命令执行等操作
   - 步骤描述是否清晰透明
   - 是否有关于数据安全的说明

4. 检查 scripts 目录（如果有）
   - 逐行阅读脚本代码
   - 重点关注网络请求、文件操作、系统调用
   - 检查是否有混淆或加密的代码（高度可疑）

5. 检查依赖文件
   - requirements.txt / package.json
   - 依赖的数量是否合理
   - 是否有来自非官方源的依赖
```

### 安装后验证

```
1. 在测试项目/目录中先试用
   - 不要直接在正式项目中使用
   - 观察 Skill 执行过程中的所有操作

2. 监控行为
   - 检查是否有未声明的网络请求
   - 检查是否有未声明的文件修改
   - 确认操作范围在 Skill 描述范围内

3. 确认安全后再用于正式项目
```

## 快速安全检查命令

```bash
# 检查 SKILL.md 中的危险命令
grep -n -E "(rm -rf|sudo |curl |wget |/dev/null|> /etc/|chmod 777)" SKILL.md

# 检查脚本中的网络请求
grep -n -E "(requests\.|urllib|http\.|fetch\(|axios|curl)" scripts/* 2>/dev/null

# 检查脚本中的文件删除操作
grep -n -E "(os\.remove|shutil\.rmtree|unlink|fs\.unlink)" scripts/* 2>/dev/null

# 检查是否有硬编码的密钥或 Token
grep -n -E "(API_KEY|SECRET|TOKEN|PASSWORD).*=" SKILL.md scripts/* 2>/dev/null
```

Windows PowerShell 中等效命令：

```powershell
# 检查 SKILL.md 中的危险命令
Select-String -Path "SKILL.md" -Pattern "rm -rf|sudo |curl |wget "

# 检查脚本中的网络请求
Select-String -Path "scripts\*" -Pattern "requests\.|urllib|http\.|fetch\(|axios|curl"

# 检查脚本中的文件删除操作
Select-String -Path "scripts\*" -Pattern "os\.remove|shutil\.rmtree|unlink|fs\.unlink"

# 检查是否有硬编码的密钥
Select-String -Path "SKILL.md", "scripts\*" -Pattern "API_KEY|SECRET|TOKEN|PASSWORD"
```

## 红旗警告（应立即停止使用）

出现以下任一情况，**立即停止使用该 Skill**：

1. SKILL.md 或脚本中包含混淆/加密代码
2. 包含删除用户文件或格式化磁盘的命令
3. 在未声明的情况下向外部 URL 发送数据
4. 尝试读取 `.ssh/`、`.aws/`、`.env` 等敏感目录或文件
5. 要求不必要的管理员/sudo 权限
6. 安装来源不可信的二进制文件或脚本
7. 作者要求关闭安全软件或以不安全方式配置系统

## 最佳实践总结

1. **skills.sh 辅助筛选**：优先选择 skills.sh 上排名靠前、评分高、更新活跃的 Skill
2. **先读后用**：安装前必须通读 SKILL.md，确认操作范围在预期之内
3. **脚本审查**：有 scripts 目录的 Skill 要逐行审查
4. **测试隔离**：先在测试项目中试用，确认安全后再用于正式项目
5. **保持更新**：定期检查已安装 Skill 的更新，及时修复安全问题
6. **最小权限**：仅安装真正需要的 Skill，减少攻击面
