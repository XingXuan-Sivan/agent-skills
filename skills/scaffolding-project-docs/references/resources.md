# 资源契约

> 何时读本文：需要往 `assets/` 里加模板或分片、或从别处导入模板时。

`assets/` 下的文件是**自描述资源库**：运行时枚举目录、读取文件头部，决定用哪些。因此导入一个模板 = 放一个文件进去，不需要改 `SKILL.md`，也不需要注册表。

代价是必须遵守下面五条约定，否则导进来的模板无法被正确识别和使用。

## 1. 类型化模板：命名即类型

`assets/templates/<type>.md` 的文件名必须与 frontmatter 的 `type` 取值一致。

| 文件名 | frontmatter `type` |
|---|---|
| `adr.md` | `adr` |
| `rfc.md` | `rfc` |
| `design.md` | `design` |
| `guide.md` | `guide` |
| `reference.md` | `reference` |

要换成自己的 ADR 模板，**同名覆盖即可**，零配置。

## 2. 结构性模板：`_` 前缀

这类模板产出的是不带 frontmatter 的结构文件，没法用类型命名，所以用 `_` 前缀区分：

| 文件名 | 产出 |
|---|---|
| `_agents.md` | 根 `AGENTS.md` |
| `_root-readme.md` | 根 `README.md` |
| `_docs-readme.md` | `docs/README.md` |
| `_dir-readme.md` | 各目录 `README.md` |

看到 `_` 前缀就知道：这是结构件，不是文档，不参与元数据检查。

## 3. 分片命名

**规范分片**（`assets/standards/`）——讲规则：

- `universal.md` 必备
- 技术栈分片：`<lang>.md`、`backend-<lang>.md`、`frontend-<framework>.md`
- 领域分片：直接用领域名，如 `git.md`、`testing.md`

**自动化分片**（`assets/automation/`）——讲工具链：

- `index-generation.md`：索引生成，任何项目都适用
- `changelog-<stack>.md`：发布记录生成，按栈选一个（如 `changelog-node.md`、`changelog-generic.md`）

分片都带 `applies_when` 自我声明适用条件。**拷入项目时删掉 `applies_when`**，并**去掉栈后缀**——
一个项目只会启用一份发布记录方案，落为 `docs/development/standards/changelog.md` 即可。

## 4. 占位符

只登记四个：

| 占位符 | 含义 |
|---|---|
| `{{PROJECT_NAME}}` | 项目名 |
| `{{TITLE}}` | 文档标题 |
| `{{DATE}}` | 日期，`YYYY-MM-DD` |
| `{{NUMBER}}` | 编号，如 ADR 序号 |

遇到未登记的占位符：按名称含义填充；判断不了就**保留原文并提醒用户**——这通常意味着模板来自别的体系，硬填会填错。

## 5. 最小结构

- **类型化模板**：H1 标题 + 4 个必填字段的 frontmatter + 正文
- **结构性模板**：H1 标题 + 正文

可以比这多，不能比这少。

## 生成时的行为

- **先列目录再看文件**，不要假设有哪些模板存在
- 类型化模板按文档类型取用；结构性模板按目标文件名取用；分片按 `applies_when` 取用
- 模板里的示例行、示例表格**必须替换成真实内容**。留着示例会同时污染文档和校验结果
- 结构性模板生成后，按项目实际情况删减不适用的段落（例如 `AGENTS.md` 里未启用分片的路由行）

### 模板里不许写死具体值

这是模板编写最容易犯的错：**把参照样本里的具体值当成通用默认值**。

具体平台名（某个代码托管平台）、具体许可证名、具体版本号、具体工具名——这些都不属于模板，
写进去就等于替项目做了决定，而且项目往往不会注意到要改。

```markdown
<!-- 错误：MIT 与这个项目无关，徽章服务也可能不是它 -->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<!-- 正确：示例放进生成指令，由生成方按项目实际替换 -->
<!-- gen-note: 徽章按项目实际填写。示例写法：
     [![License](https://img.shields.io/badge/license-<许可证标识>-blue.svg)](LICENSE) -->
```

放 `gen-note` 里还有一个好处：**残留会被校验抓住**，而写死一个错的值不会——它只是安静地错着。

### 生成指令必须清理

模板里写给生成方看的说明一律写成 `<!-- gen-note: ... -->`：

```markdown
<!-- gen-note: 没有许可与贡献说明就整节删除，不要留空标题 -->
## 许可
```

- **它是生成指令，不是内容**——生成时必须连同它指示的操作一起清除，不留残留
- 清掉后**折叠因此产生的连续空行**（包括文件开头的空行），否则产物里到处是多出来的空白
- 写成普通正文会让指令直接印在产物里；写成普通注释则与「有意保留给维护者的说明」无法区分，会被误清或误留
- 校验脚本会把残留的 `gen-note` 报为 error，所以漏清理不会悄悄溜过去

**反过来**：有意留给项目维护者的说明（例如解释「为什么这里有些条目被注释掉了」）就用普通 HTML 注释，
生成时保留。区分标准是**它是写给生成方的，还是写给日后读这份文件的人的**。

## 6. 生成区不是模板

目录 `README.md` 里的 `<!-- gen:docs:start -->` / `<!-- gen:subdirs:start -->` 区块，
以及目录 `README.md` 与根 `AGENTS.md` 里的 `<!-- gen:nav:start -->` 区块，
**由 `scripts/gen_index.py` 维护，不要手写内容**（`gen:nav` 的条目例外——那部分由人写，生成器只启停）。

生成后立刻跑一次生成器，再跑校验；生成区与源不同步会被 `verify_docs.py` 报为 error。

链接与索引检查会先剔除 HTML 注释，因此在 `gen:nav-off` 里被隐藏的条目不会产生死链告警。
