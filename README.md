<div align="center">

# Agent Skills

**理顺开发环境与工程流程的 Agent Skills**

[可用技能](#可用技能) · [快速开始](#快速开始) · [仓库结构](#仓库结构)

</div>

---

每个技能解决一类反复出现的开发问题，并且不绑定特定技术栈——换一门语言照样能用。

## 项目介绍

这里的技能都来自实际开发中反复踩到的坑：同一个问题解释过三遍，就该写成技能。
所以它们偏工程流程而不是领域知识——怎么把环境搭起来、怎么组织文档、怎么定规范、
怎么让 AI 在正确的时机读到正确的东西。

能固化成脚本的，就固化成脚本和模板，而不是留给使用者记性。

## 可用技能

### [init-skills](skills/init-skills/)

为新环境初始化 Skills：检测平台与 CLI 环境，从 skills.sh 实时检索并按四层渐进推荐，逐层确认后安装。

- **元技能**——它负责帮你装好别的技能，建议从这里开始
- 分层推进：核心元技能 → 文档处理 → 开发者必装 → 按需实时推荐
- 不预置固定仓库清单，推荐来自 skills.sh 的实时热榜与排行
- 安装级别首次确认后全程沿用，不重复追问
- 安装前用 `npx skills list` 做重复检查

适用场景：刚装好 Agent 想让环境一次到位，或不确定该装哪些技能的时候。

### [scaffolding-project-docs](skills/scaffolding-project-docs/)

建立或整理项目的文档体系与工程规范：目录结构、元数据、编码与 Git 规范、AI 路由入口。

- 三种模式：新建项目初始化、把散落文档纳入体系、只补规范
- 文档结构是**默认规则而非铁律**，同时支持减法（不建）与加法（新增目录）
- 索引与发布记录**默认交给工具生成**，手写只作兜底
- 自带零依赖校验脚本，可以直接挂 CI

适用场景：新项目起步、第一次让 AI 参与开发、或发现文档已经没人看得懂的时候。

## 快速开始

### 运行环境

- 任一支持 Agent Skills 的代理（Claude Code、Codex、Cursor、OpenCode 等 80 余种）
- 用下面的命令安装时需要 Node（`npx`）；手动复制则不需要

### 安装

```bash
# 装仓库里的全部技能
npx skills add https://gitee.com/XingXuan-Sivan/agent-skills.git -g -y

# 只装其中一个
npx skills add https://gitee.com/XingXuan-Sivan/agent-skills.git -g -y --skill init-skills
```

`-g` 装到全局，不加则装到当前项目。默认用符号链接，之后 `npx skills update` 一键更新。

也可以手动安装——把 `skills/` 下的目录复制进你的技能目录（如 `~/.agents/skills/`）即可：

```bash
git clone <仓库地址>
cp -r <克隆出来的目录>/skills/* ~/.agents/skills/
```

## 仓库结构

```
skills/
└─ <技能名>/          # 一个技能一个目录
   ├─ SKILL.md        # 入口：元数据 + 指令（唯一必需项）
   ├─ references/     # 按需加载的说明文档
   ├─ assets/         # 模板与规范分片
   ├─ resources/      # 数据资源，如清单与配置
   ├─ scripts/        # 可执行脚本
   └─ LICENSE         # 随技能目录一起分发
```

除 `SKILL.md` 外都是可选的，每个技能只带自己需要的东西。

`skills/` 是 Agent Skills 生态约定的技能容器目录，安装工具会在这里自动发现技能。

## 许可

[MIT](LICENSE)。

每个技能目录下也带一份 `LICENSE`——因为安装工具只拷贝技能目录本身，副本里需要一并保留版权声明。
