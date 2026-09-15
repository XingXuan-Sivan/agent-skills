# 各平台 Skills 适配信息

## 概述

本文档记录主流 AI Agent 软件的 Skills 目录结构、配置方式和探测命令，供 `init-skills` 在初始化时动态适配。所有平台差异信息集中于此，不硬编码到 SKILL.md 中。

> **核心原则**：`npx skills` CLI 是 Skills 生态的标准安装工具，应优先引导用户配置 CLI 环境。仅当用户明确拒绝时才使用手动安装方式。

## npx skills CLI 环境要求与自动配置

### 环境要求

| 组件 | 最低版本 | 说明 |
|------|---------|------|
| Node.js | ≥ 18.0.0 | npx 随 Node.js 一起提供 |
| npm | ≥ 8.0.0（随 Node.js 安装） | 包管理器，npx 的依赖 |
| npx | 随 npm 安装 | 直接执行 npm 包，无需全局安装 |

### 自动配置流程

当检测到环境不满足时，按以下步骤引导用户：

1. **告知当前状态**：列出缺失组件及版本要求
2. **询问是否配置**：给用户选择权，不强制
3. **用户同意后执行**：根据操作系统选择对应的安装方式

#### Windows（PowerShell）

```powershell
# 方式一：使用 winget（Windows 11 / Windows 10 1809+）
winget install OpenJS.NodeJS.LTS

# 方式二：使用 Chocolatey
choco install nodejs-lts

# 方式三：手动下载安装
# 访问 https://nodejs.org/zh-cn/download/ 下载 LTS 版本安装包
# 安装后重新打开终端

# 验证安装
node --version
npm --version
```

#### macOS

```bash
# 方式一：使用 Homebrew（推荐）
brew install node@20

# 方式二：使用 nvm（版本管理器）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# 验证安装
node --version
npm --version
```

#### Linux（Debian/Ubuntu）

```bash
# 使用 NodeSource 官方源
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

#### Linux（CentOS/RHEL/Fedora）

```bash
# 使用 NodeSource 官方源
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs

# 验证安装
node --version
npm --version
```

#### CLI 可用性验证

```bash
# 首次运行会自动下载 skills CLI
npx skills --help
```

## 平台速查表

| Agent 软件 | Skills 全局目录 | Skills 项目目录 | 配置方式 |
|-----------|----------------|----------------|---------|
| Qoder | `~/.qoder/skills/` | `<project>/.qoder/skills/` | SKILL.md 目录 |
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` | SKILL.md 目录 |
| Cursor | `~/.cursor/skills/` | `<project>/.cursor/skills/` | SKILL.md 目录 / Rules |
| GitHub Copilot | N/A（Chat 上下文注入） | `<project>/.github/copilot/` | 通过指令文件 |
| Cline | `~/.cline/skills/` | `<project>/.cline/skills/` | SKILL.md 目录 |
| Windsurf | `~/.windsurf/skills/` | `<project>/.windsurf/skills/` | SKILL.md 目录 |
| Codex (OpenAI) | `~/.codex/skills/` | `<project>/.codex/skills/` | SKILL.md 目录 |
| 通义灵码 | `~/.lingma/skills/` | `<project>/.lingma/skills/` | SKILL.md 目录 |

> 以上路径为通用约定，具体以各软件最新文档为准。

## 路径探测策略

### 自动探测（按优先级）

1. **检查环境变量**：`AGENT_SKILLS_HOME`、`SKILLS_PATH` 等用户自定义变量
2. **检查现有目录**：遍历工作区查找 `.qoder/`、`.claude/`、`.cursor/`、`.cline/`、`.windsurf/` 等
3. **检查 Home 目录**：检查用户 Home 目录下对应平台目录
4. **主动询问**：以上均无法确定时，询问用户使用的 Agent 软件和期望的安装位置

### 安装级别说明

| 级别 | 说明 | 典型场景 |
|------|------|---------|
| 全局 | 安装到用户 Home 目录下的平台 skills 目录 | 所有项目共享的通用 Skills |
| 项目 | 安装到当前项目根目录下的平台 skills 目录 | 仅当前项目使用的专用 Skills |
| 自定义 | 安装到用户指定的任意目录 | 需要集中管理或共享 |

> **重要**：安装级别必须在每个 Skill 安装前由用户确认，不可默认假设。

## 手动安装方式（降级方案）

仅当用户明确拒绝配置 CLI 环境时使用。

### git clone 手动安装

```bash
# 通用流程（${SKILLS_DIR} 替换为实际平台 Skills 目录）
git clone https://github.com/<owner>/<repo>.git /tmp/skills-temp
cp -r /tmp/skills-temp/skills/<skill-name> ${SKILLS_DIR}/
rm -rf /tmp/skills-temp
```

### ZIP 手动安装

```bash
# 1. 浏览器访问 https://github.com/<owner>/<repo>/archive/refs/heads/main.zip
# 2. 下载并解压
# 3. 将需要的 Skill 目录复制到 ${SKILLS_DIR}
```

## 探测命令参考

### CLI 环境探测

```bash
# 检查 Node.js
node --version 2>/dev/null || echo "Node.js 未安装"

# 检查 npm
npm --version 2>/dev/null || echo "npm 未安装"

# 检查 npx skills CLI
npx skills --help 2>/dev/null || echo "npx skills CLI 不可用"
```

### 平台目录探测（bash）

```bash
# 检查 git
git --version 2>/dev/null || echo "git 未安装"

# 列出当前目录下已有的平台目录
ls -d .qoder .claude .cursor .cline .windsurf 2>/dev/null

# 检查 Home 目录下的平台目录
ls -d ~/.qoder ~/.claude ~/.cursor ~/.cline ~/.windsurf 2>/dev/null
```

### 平台目录探测（PowerShell）

```powershell
# 检查 Skills CLI 环境
node --version
npm --version
npx skills --version

# 检查 git
git --version

# 列出当前目录下的平台目录
Get-ChildItem -Directory -Name ".qoder", ".claude", ".cursor", ".cline", ".windsurf" -ErrorAction SilentlyContinue

# 检查 Home 目录下的平台目录
Get-ChildItem -Directory -Name "$env:USERPROFILE\.qoder", "$env:USERPROFILE\.claude" -ErrorAction SilentlyContinue
```
