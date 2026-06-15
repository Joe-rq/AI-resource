---
title: "创建自定义 subagents"
source: "url"
source_file: "https://code.claude.com/docs/zh-CN/sub-agents"
created: "2026-05-21T01:50:25Z"
source_url: "https://code.claude.com/docs/zh-CN/sub-agents"
extract_method: "readability+md"
---

> ## Documentation Index
> Fetch the complete documentation index at: https://code. claude. com/docs/llms. txt
> Use this file to discover all available pages before exploring further.

# 创建自定义 subagents

> 在 Claude Code 中创建和使用专门的 AI subagents，用于特定任务的工作流和改进的上下文管理。

Subagents 是处理特定类型任务的专门 AI 助手。当一个辅助任务会用搜索结果、日志或文件内容充斥您的主对话，而您不会再次引用这些内容时，请使用一个 subagent：该 subagent 在自己的上下文中完成这项工作，仅返回摘要。当您不断生成相同类型的工作者并使用相同的指令时，定义一个自定义 subagent。

每个 subagent 在自己的 context window 中运行，具有自定义系统提示、特定的工具访问权限和独立的权限。当 Claude 遇到与 subagent 描述相匹配的任务时，它会委托给该 subagent，该 subagent 独立工作并返回结果。要在实践中看到上下文节省，[context window 可视化](/zh-CN/context-window) 演示了一个 subagent 在自己的独立窗口中处理研究的会话。

<Note>
  Subagents 在单个会话中工作。要在并行运行许多独立会话并从一个地方监控它们，请参阅 [background agents](/zh-CN/agent-view)。对于相互通信的会话，请参阅 [agent teams](/zh-CN/agent-teams)。
</Note>

Subagents 帮助您：

- **保留上下文**，通过将探索和实现保持在主对话之外
- **强制执行约束**，通过限制 subagent 可以使用的工具
- **跨项目重用配置**，使用用户级 subagents
- **专门化行为**，为特定领域使用专注的系统提示
- **控制成本**，通过将任务路由到更快、更便宜的模型（如 Haiku）

Claude 使用每个 subagent 的描述来决定何时委托任务。创建 subagent 时，请编写清晰的描述，以便 Claude 知道何时使用它。

Claude Code 包括几个内置 subagents，如 **Explore**、**Plan** 和 **general-purpose**。您也可以创建自定义 subagents 来处理特定任务。本页涵盖：

- [内置 subagents](#built-in-subagents)
- [如何创建您自己的](#quickstart-create-your-first-subagent)
- [完整配置选项](#configure-subagents)
- [使用 subagents 的模式](#work-with-subagents)
- [分叉 subagents](#fork-the-current-conversation)
- [示例 subagents](#example-subagents)

## 内置 subagents

Claude Code 包括内置 subagents，Claude 在适当时自动使用。每个都继承父对话的权限，并有额外的工具限制。

Explore 和 Plan 会跳过您的 CLAUDE. md 文件和父会话的 git 状态，以保持研究快速且成本低廉。所有其他内置和 [自定义 subagent](#configure-subagents) 都会加载两者。有关到达 subagent 的内容的完整分解，请参阅 [启动时加载的内容](#what-loads-at-startup)。

<Tabs>
  <Tab title="Explore">     一个快速的、只读的代理，针对搜索和分析代码库进行了优化。

    - **Model**: Haiku（快速、低延迟）
    - **Tools**: 只读工具（拒绝访问 Write 和 Edit 工具）
    - **Purpose**: 文件发现、代码搜索、代码库探索

    当 Claude 需要搜索或理解代码库而不进行更改时，它会委托给 Explore。这样可以将探索结果保持在主对话上下文之外。

    调用 Explore 时，Claude 指定一个彻底程度级别：**quick** 用于有针对性的查找，**medium** 用于平衡的探索，或 **very thorough** 用于全面分析。
  </Tab>

  <Tab title="Plan">     一个研究代理，在 [plan mode](/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 期间使用，以在呈现计划之前收集上下文。

    - **Model**: 从主对话继承
    - **Tools**: 只读工具（拒绝访问 Write 和 Edit 工具）
    - **Purpose**: 用于规划的代码库研究

    当您处于 plan mode 并且 Claude 需要理解您的代码库时，它会将研究委托给 Plan subagent。这可以防止无限嵌套（subagents 无法生成其他 subagents），同时仍然收集必要的上下文。
  </Tab>

  <Tab title="General-purpose">     一个能够处理复杂、多步骤任务的代理，需要探索和操作。

    - **Model**: 从主对话继承
    - **Tools**: 所有工具
    - **Purpose**: 复杂研究、多步骤操作、代码修改

    当任务需要探索和修改、复杂推理来解释结果或多个依赖步骤时，Claude 会委托给 general-purpose。
  </Tab>

  <Tab title="Other">     Claude Code 包括用于特定任务的其他辅助代理。这些通常会自动调用，因此您不需要直接使用它们。

    | Agent             | Model  | Claude 何时使用它                 |
    | :---------------- | :----- | :--------------------------- |
    | statusline-setup  | Sonnet | 当您运行 `/statusline` 来配置您的状态行时 |
    | claude-code-guide | Haiku  | 当您提出关于 Claude Code 功能的问题时    |
  </Tab> </Tabs>

除了这些内置 subagents，您可以创建自己的，具有自定义提示、工具限制、权限模式、hooks 和 skills。以下部分展示了如何开始和自定义 subagents。

## 快速入门：创建您的第一个 subagent

Subagents 在带有 YAML frontmatter 的 Markdown 文件中定义。您可以 [手动创建它们](#write-subagent-files) 或使用 `/agents` 命令。

本演练指导您使用 `/agents` 命令创建用户级 subagent。该 subagent 审查代码并为代码库建议改进。

<Steps>
  <Step title="打开 subagents 界面">     在 Claude Code 中，运行：

    ```text theme={null}
    /agents
    ```
  </Step>

  <Step title="选择一个位置">     切换到 **Library** 选项卡，选择 **Create new agent**，然后选择 **Personal**。这会将 subagent 保存到 `~/.claude/agents/`，以便在所有项目中可用。
  </Step>

  <Step title="使用 Claude 生成">     选择 **Generate with Claude**。出现提示时，描述 subagent：

    ```text theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude 为您生成标识符、描述和系统提示。
  </Step>

  <Step title="选择工具">     对于只读审查者，取消选择除 **Read-only tools** 之外的所有内容。如果您保持所有工具被选中，subagent 会继承主对话可用的所有工具。
  </Step>

  <Step title="选择模型">     选择 subagent 使用的模型。对于此示例代理，选择 **Sonnet**，它在分析代码模式的能力和速度之间取得平衡。
  </Step>

  <Step title="选择颜色">     为 subagent 选择背景颜色。这有助于您在 UI 中识别哪个 subagent 正在运行。
  </Step>

  <Step title="配置内存">     选择 **User scope** 为 subagent 提供一个 [persistent memory directory](#enable-persistent-memory)，位于 `~/.claude/agent-memory/`。Subagent 使用这个来在对话中积累见解，例如代码库模式和重复出现的问题。如果您不希望 subagent 保留学习，请选择 **None**。
  </Step>

  <Step title="保存并尝试">     查看配置摘要。按 `s` 或 `Enter` 保存，或按 `e` 在编辑器中保存并编辑文件。Subagent 立即可用。尝试它：

    ```text theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude 委托给您的新 subagent，它扫描代码库并返回改进建议。
  </Step> </Steps>

现在您有了一个 subagent，可以在您机器上的任何项目中使用它来分析代码库并建议改进。

您也可以手动创建 subagents 作为 Markdown 文件、通过 CLI 标志定义它们，或通过 plugins 分发它们。以下部分涵盖所有配置选项。

## 配置 subagents

### 使用 /agents 命令

`/agents` 命令打开一个选项卡式界面来管理 subagents。**Running** 选项卡显示实时 subagents，让您打开或停止它们。**Library** 选项卡让您：

- 查看所有可用的 subagents（内置、用户、项目和 plugin）
- 使用引导式设置或 Claude 生成创建新的 subagents
- 编辑现有 subagent 配置和工具访问
- 删除自定义 subagents
- 查看当存在重复时哪些 subagents 是活跃的

这是创建和管理 subagents 的推荐方式。对于手动创建或自动化，您也可以直接添加 subagent 文件。

### 选择 subagent 范围

Subagents 是带有 YAML frontmatter 的 Markdown 文件。根据范围将它们存储在不同的位置。当多个 subagents 共享相同的名称时，更高优先级的位置获胜。

| Location              | Scope         | Priority | 如何创建                                      |
| :-------------------- | :------------ | :------- | :---------------------------------------- |
| 托管设置                  | 组织范围          | 1（最高）   | 通过 [managed settings](/zh-CN/settings) 部署 |
| `--agents` CLI 标志     | 当前会话          | 2        | 启动 Claude Code 时传递 JSON                   |
| `.claude/agents/`     | 当前项目          | 3        | 交互式或手动                                    |
| `~/.claude/agents/`   | 所有您的项目        | 4        | 交互式或手动                                    |
| Plugin 的 `agents/` 目录 | 启用 plugin 的位置 | 5（最低）   | 与 [plugins](/zh-CN/plugins) 一起安装          |

**项目 subagents**（`.claude/agents/`）非常适合特定于代码库的 subagents。将它们检入版本控制，以便您的团队可以协作使用和改进它们。

项目 subagents 通过从当前工作目录向上遍历来发现。使用 `--add-dir` 添加的目录 [仅授予文件访问权限](/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)，不会扫描 subagents。要在项目间共享 subagents，请使用 `~/.claude/agents/` 或 [plugin](/zh-CN/plugins)。

**用户 subagents**（`~/.claude/agents/`）是在所有项目中可用的个人 subagents。

Claude Code 递归扫描 `.claude/agents/` 和 `~/.claude/agents/`，因此您可以将定义组织到子文件夹中，例如 `agents/review/` 或 `agents/research/`。子目录路径不会影响 subagent 的识别或调用方式，因为身份仅来自 `name` frontmatter 字段。在整个树中保持 `name` 值唯一：如果一个范围内的两个文件声明相同的名称，Claude Code 会保留一个并丢弃另一个而不发出警告。

Plugin `agents/` 目录也会被递归扫描。与项目和用户范围不同，plugin 的 `agents/` 目录内的子文件夹成为 [scoped identifier](#invoke-subagents-explicitly) 的一部分：plugin `my-plugin` 中位于 `agents/review/security.md` 的文件注册为 `my-plugin:review:security`。

**CLI 定义的 subagents** 在启动 Claude Code 时作为 JSON 传递。它们仅存在于该会话中，不会保存到磁盘，使其对快速测试或自动化脚本很有用。您可以在单个 `--agents` 调用中定义多个 subagents：

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    claude --agents '{
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }'
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    claude --agents @'
    {
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }
    '@
    ```
  </Tab> </Tabs>

`--agents` 标志接受 JSON，具有与基于文件的 subagents 相同的 [frontmatter](#supported-frontmatter-fields) 字段：`description`、`prompt`、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills`、`initialPrompt`、`memory`、`effort`、`background`、`isolation` 和 `color`。对系统提示使用 `prompt`，等同于基于文件的 subagents 中的 markdown 正文。

**托管 subagents** 由组织管理员部署。在 [managed settings directory](/zh-CN/settings#settings-files) 内的 `.claude/agents/` 中放置 markdown 文件，使用与项目和用户 subagents 相同的 frontmatter 格式。托管定义优先于具有相同名称的项目和用户 subagents。

**Plugin subagents** 来自您已安装的 [plugins](/zh-CN/plugins)。它们与您的自定义 subagents 一起出现在 `/agents` 中。有关创建 plugin subagents 的详细信息，请参阅 [plugin 组件参考](/zh-CN/plugins-reference#agents)。

<Note>
  出于安全原因，plugin subagents 不支持 `hooks`、`mcpServers` 或 `permissionMode` frontmatter 字段。加载来自 plugin 的代理时，这些字段被忽略。如果您需要它们，请将代理文件复制到 `.claude/agents/` 或 `~/.claude/agents/`。您也可以在 `settings.json` 或 `settings.local.json` 中向 [`permissions.allow`](/zh-CN/settings#permission-settings) 添加规则，但这些规则适用于整个会话，而不仅仅是 plugin subagent。
</Note>

来自任何这些范围的 subagent 定义也可用于 [agent teams](/zh-CN/agent-teams#use-subagent-definitions-for-teammates)：当生成一个队友时，您可以引用一个 subagent 类型，队友使用其 `tools` 和 `model`，定义的正文作为额外指令附加到队友的系统提示。有关哪些 frontmatter 字段适用于该路径，请参阅 [agent teams](/zh-CN/agent-teams#use-subagent-definitions-for-teammates)。

### 编写 subagent 文件

Subagent 文件使用 YAML frontmatter 进行配置，然后是 Markdown 中的系统提示：

<Note>
  Subagents 在会话启动时加载。如果您直接在磁盘上添加或编辑 subagent 文件，请重启您的会话以加载它。通过 `/agents` 界面创建的 Subagents 无需重启即可立即生效。
</Note>

```markdown theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter 定义了 subagent 的元数据和配置。正文成为指导 subagent 行为的系统提示。Subagents 仅接收此系统提示（加上基本环境详细信息，如工作目录），而不是完整的 Claude Code 系统提示。

一个 subagent 在主对话的当前工作目录中启动。在 subagent 中，`cd` 命令不会在 Bash 或 PowerShell 工具调用之间持续，也不会影响主对话的工作目录。要给 subagent 一个隔离的存储库副本，请改为设置 [`isolation: worktree`](#supported-frontmatter-fields)。

#### 支持的 frontmatter 字段

以下字段可以在 YAML frontmatter 中使用。只有 `name` 和 `description` 是必需的。

| Field             | Required | Description                                                                                                                                                                                                        |
| :---------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | 使用小写字母和连字符的唯一标识符。[Hooks](/zh-CN/hooks#subagentstart) 将此值作为 `agent_type` 接收。文件名不必匹配                                                                                                                                 |
| `description`     | Yes      | Claude 何时应该委托给此 subagent                                                                                                                                                                                           |
| `tools`           | No       | [Tools](#available-tools) subagent 可以使用。如果省略，继承所有工具。要将 Skills 预加载到上下文中，请使用 `skills` 字段而不是在此处列出 `Skill`                                                                                                             |
| `disallowedTools` | No       | 要拒绝的工具，从继承或指定的列表中删除                                                                                                                                                                                                |
| `model`           | No       | [Model](#choose-a-model) 使用：`sonnet`、`opus`、`haiku`、完整模型 ID（例如，`claude-opus-4-7`）或 `inherit`。默认为 `inherit`                                                                                                         |
| `permissionMode`  | No       | [Permission mode](#permission-modes)：`default`、`acceptEdits`、`auto`、`dontAsk`、`bypassPermissions` 或 `plan`。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略                                                   |
| `maxTurns`        | No       | subagent 停止前的最大代理轮数                                                                                                                                                                                                |
| `skills`          | No       | [Skills](/zh-CN/skills) 在启动时加载到 subagent 的上下文中。注入完整的技能内容，而不仅仅是描述。Subagents 仍然可以通过 Skill 工具调用未列出的项目、用户和 plugin 技能                                                                                                   |
| `mcpServers`      | No       | [MCP servers](/zh-CN/mcp) 对此 subagent 可用。每个条目要么是引用已配置服务器的服务器名称（例如，`"slack"`），要么是内联定义，其中服务器名称为键，完整的 [MCP server config](/zh-CN/mcp#installing-mcp-servers) 为值。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略 |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents) 限定于此 subagent。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略                                                                                                 |
| `memory`          | No       | [Persistent memory scope](#enable-persistent-memory)：`user`、`project` 或 `local`。启用跨会话学习                                                                                                                            |
| `background`      | No       | 设置为 `true` 以始终将此 subagent 作为 [background task](#run-subagents-in-foreground-or-background) 运行。默认：`false`                                                                                                           |
| `effort`          | No       | 此 subagent 活跃时的努力级别。覆盖会话努力级别。默认：从会话继承。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型                                                                                                                             |
| `isolation`       | No       | 设置为 `worktree` 以在临时 [git worktree](/zh-CN/worktrees) 中运行 subagent，为其提供存储库的隔离副本。如果 subagent 不进行任何更改，worktree 会自动清理                                                                                                  |
| `color`           | No       | Subagent 在任务列表和转录中的显示颜色。接受 `red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan`                                                                                                                         |
| `initialPrompt`   | No       | 当此代理作为主会话代理运行时（通过 `--agent` 或 `agent` 设置），自动提交为第一个用户轮次。[Commands](/zh-CN/commands) 和 [skills](/zh-CN/skills) 被处理。前置于任何用户提供的提示                                                                                      |

### 选择模型

`model` 字段控制 subagent 使用的 [AI model](/zh-CN/model-config)：

- **Model alias**: 使用可用的别名之一：`sonnet`、`opus` 或 `haiku`
- **Full model ID**: 使用完整的模型 ID，如 `claude-opus-4-7` 或 `claude-sonnet-4-6`。接受与 `--model` 标志相同的值
- **inherit**: 使用与主对话相同的模型
- **Omitted**: 如果未指定，默认为 `inherit`（使用与主对话相同的模型）

当 Claude 调用 subagent 时，它也可以为该特定调用传递 `model` 参数。Claude Code 按以下顺序解析 subagent 的模型：

1. [`CLAUDE_CODE_SUBAGENT_MODEL`](/zh-CN/model-config#environment-variables) 环境变量，如果设置
2. 每次调用的 `model` 参数
3. Subagent 定义的 `model` frontmatter
4. 主对话的模型

### 控制 subagent 能力

您可以通过工具访问、权限模式和条件规则来控制 subagents 可以做什么。

#### 可用工具

Subagents 可以使用 Claude Code 的任何 [internal tools](/zh-CN/tools-reference)。默认情况下，subagents 继承主对话的所有工具，包括 MCP 工具。

要限制工具，使用 `tools` 字段（允许列表）或 `disallowedTools` 字段（拒绝列表）。此示例使用 `tools` 来专门允许 Read、Grep、Glob 和 Bash。Subagent 无法编辑文件、写入文件或使用任何 MCP 工具：

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

此示例使用 `disallowedTools` 来继承主对话的每个工具，除了 Write 和 Edit。Subagent 保留 Bash、MCP 工具和其他所有内容：

```yaml theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

如果两者都设置，`disallowedTools` 首先应用，然后 `tools` 针对剩余的池进行解析。同时列在两者中的工具被删除。

#### 限制可以生成哪些 subagents

当代理作为主线程运行时，使用 `claude --agent`，它可以使用 Agent 工具生成 subagents。要限制它可以生成的 subagent 类型，在 `tools` 字段中使用 `Agent(agent_type)` 语法。

<Note>在版本 2.1.63 中，Task 工具被重命名为 Agent。设置和代理定义中的现有 `Task(...)` 引用仍然作为别名工作。</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

这是一个允许列表：只有 `worker` 和 `researcher` subagents 可以被生成。如果代理尝试生成任何其他类型，请求失败，代理在其提示中仅看到允许的类型。要在允许所有其他类型的同时阻止特定代理，请改用 [`permissions.deny`](#disable-specific-subagents)。

要允许生成任何 subagent 而不受限制，使用不带括号的 `Agent`：

```yaml theme={null}
tools: Agent, Read, Bash
```

如果 `Agent` 完全从 `tools` 列表中省略，代理无法生成任何 subagents。此限制仅适用于作为主线程运行的代理，使用 `claude --agent`。Subagents 无法生成其他 subagents，因此 `Agent(agent_type)` 在 subagent 定义中无效。

#### 将 MCP 服务器限定于 subagent

使用 `mcpServers` 字段为 subagent 提供对主对话中不可用的 [MCP](/zh-CN/mcp) 服务器的访问。此处定义的内联服务器在 subagent 启动时连接，在完成时断开连接。字符串引用共享父会话的连接。

<Note>
  `mcpServers` 字段适用于代理文件可以运行的两个上下文：

  - 作为 subagent，通过 Agent 工具或 @-mention 生成
  - 作为主会话，使用 [`--agent`](#invoke-subagents-explicitly) 或 `agent` 设置启动

  当代理是主会话时，内联服务器定义与来自 [`.mcp.json`](/zh-CN/mcp) 和设置文件的服务器一起在启动时连接。
</Note>

列表中的每个条目要么是内联服务器定义，要么是引用会话中已配置的 MCP 服务器的字符串：

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

内联定义使用与 `.mcp.json` 服务器条目相同的架构（`stdio`、`http`、`sse`、`ws`），由服务器名称键入。

要将 MCP 服务器保持在主对话之外，并避免其工具描述消耗那里的上下文，请在此处内联定义它，而不是在 `.mcp.json` 中。Subagent 获得工具；父对话不获得。

#### 权限模式

`permissionMode` 字段控制 subagent 如何处理权限提示。Subagents 从主对话继承权限上下文，并可以覆盖模式，除非父模式优先，如下所述。

| Mode                | Behavior                                                                                 |
| :------------------ | :--------------------------------------------------------------------------------------- |
| `default`           | 标准权限检查，带有提示                                                                              |
| `acceptEdits`       | 自动接受文件编辑和工作目录或 `additionalDirectories` 中路径的常见文件系统命令                                      |
| `auto`              | [Auto mode](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)：后台分类器审查命令和受保护目录的写入 |
| `dontAsk`           | 自动拒绝权限提示（显式允许的工具仍然工作）                                                                   |
| `bypassPermissions` | 跳过权限提示                                                                                   |
| `plan`              | Plan mode（只读探索）                                                                         |

<Warning>
  谨慎使用 `bypassPermissions`。它跳过权限提示，允许 subagent 在没有批准的情况下执行操作，包括对 `.git`、`.claude`、`.vscode`、`.idea` 和 `.husky` 的写入。根目录和主目录删除（如 `rm -rf /`）仍然会作为断路器提示。有关详细信息，请参阅 [permission modes](/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)。
</Warning>

如果父级使用 `bypassPermissions` 或 `acceptEdits`，这优先并且无法被覆盖。如果父级使用 [auto mode](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)，subagent 继承 auto mode，其 frontmatter 中的任何 `permissionMode` 被忽略：分类器使用与父会话相同的块和允许规则评估 subagent 的工具调用。

#### 将技能预加载到 subagents

使用 `skills` 字段在启动时将技能内容注入到 subagent 的上下文中。这为 subagent 提供领域知识，而无需在执行期间发现和加载技能。

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

每个列出的技能的完整内容被注入到 subagent 的上下文中。此字段控制哪些技能被预加载，而不是 subagent 可以访问哪些技能：没有它，subagent 仍然可以在执行期间通过 Skill 工具发现和调用项目、用户和 plugin 技能。要防止 subagent 完全调用技能，请从 [`tools`](#available-tools) 列表中省略 `Skill` 或将其添加到 `disallowedTools`。

您无法预加载设置了 [`disable-model-invocation: true`](/zh-CN/skills#control-who-invokes-a-skill) 的技能，因为预加载来自 Claude 可以调用的相同技能集。如果列出的技能缺失或被禁用，Claude Code 会跳过它并向调试日志记录警告。

<Note>
  这与 [在 subagent 中运行技能](/zh-CN/skills#run-skills-in-a-subagent) 相反。使用 subagent 中的 `skills`，subagent 控制系统提示并加载技能内容。使用技能中的 `context: fork`，技能内容被注入到您指定的代理中。两者都使用相同的底层系统。
</Note>

#### 启用持久内存

`memory` 字段为 subagent 提供一个在对话中幸存的持久目录。Subagent 使用此目录随时间积累知识，例如代码库模式、调试见解和架构决策。

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

根据内存应该应用的广泛程度选择范围：

| Scope     | Location                                      | 使用时机                          |
| :-------- | :-------------------------------------------- | :---------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | subagent 应该在所有项目中记住学习         |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | subagent 的知识是特定于项目的并可通过版本控制共享 |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | subagent 的知识是特定于项目的但不应检入版本控制  |

启用内存时：

- Subagent 的系统提示包括读取和写入内存目录的说明。
- Subagent 的系统提示还包括内存目录中 `MEMORY.md` 的前 200 行或 25KB，以先到者为准，以及如果 `MEMORY.md` 超过该限制则策划 `MEMORY.md` 的说明。
- Read、Write 和 Edit 工具会自动启用，以便 subagent 可以管理其内存文件。

##### 持久内存提示

- `project` 是推荐的默认范围。它使 subagent 知识可通过版本控制共享。当 subagent 的知识在项目中广泛适用时使用 `user`，或当知识不应检入版本控制时使用 `local`。
- 要求 subagent 在开始工作前查阅其内存："Review this PR, and check your memory for patterns you've seen before."
- 要求 subagent 在完成任务后更新其内存："Now that you're done, save what you learned to your memory." 随着时间的推移，这会建立一个知识库，使 subagent 更有效。
- 直接在 subagent 的 markdown 文件中包含内存说明，以便它主动维护自己的知识库：

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### 使用 hooks 的条件规则

为了更动态地控制工具使用，使用 `PreToolUse` hooks 在执行前验证操作。当您需要允许工具的某些操作同时阻止其他操作时，这很有用。

此示例创建一个仅允许只读数据库查询的 subagent。`PreToolUse` hook 在每个 Bash 命令执行前运行 `command` 中指定的脚本：

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [通过 stdin 将 hook 输入作为 JSON 传递](/zh-CN/hooks#pretooluse-input) 给 hook 命令。验证脚本读取此 JSON，提取 Bash 命令，并 [以代码 2 退出](/zh-CN/hooks#exit-code-2-behavior-per-event) 以阻止写入操作：

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

有关完整的输入架构，请参阅 [Hook input](/zh-CN/hooks#pretooluse-input)，有关退出代码如何影响行为，请参阅 [exit codes](/zh-CN/hooks#exit-code-output)。在 Windows 上，在 PowerShell 中编写 hook 脚本，并在 hook 条目中添加 `shell: powershell`，如 [在 PowerShell 中运行 hooks](/zh-CN/hooks#windows-powershell-tool) 中所示。

#### 禁用特定 subagents

您可以通过将 subagents 添加到您的 [settings](/zh-CN/settings#permission-settings) 中的 `deny` 数组来防止 Claude 使用特定 subagents。使用格式 `Agent(subagent-name)`，其中 `subagent-name` 与 subagent 的 name 字段匹配。

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

这对内置和自定义 subagents 都有效。您也可以使用 `--disallowedTools` CLI 标志：

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

有关权限规则的更多详细信息，请参阅 [Permissions documentation](/zh-CN/permissions#tool-specific-permission-rules)。

### 为 subagents 定义 hooks

Subagents 可以定义在 subagent 的生命周期中运行的 [hooks](/zh-CN/hooks)。有两种方式来配置 hooks：

1. **在 subagent 的 frontmatter 中**：定义仅在该 subagent 活跃时运行的 hooks
2. **在 `settings.json` 中**：定义在 subagents 启动或停止时在主会话中运行的 hooks

#### Subagent frontmatter 中的 Hooks

直接在 subagent 的 markdown 文件中定义 hooks。这些 hooks 仅在该特定 subagent 活跃时运行，并在完成时清理。

<Note>
  Frontmatter hooks 在代理通过 Agent 工具或 @-mention 作为 subagent 生成时触发，以及当代理通过 [`--agent`](#invoke-subagents-explicitly) 或 `agent` 设置作为主会话运行时触发。在主会话情况下，它们与在 [`settings.json`](/zh-CN/hooks) 中定义的任何 hooks 一起运行。
</Note>

所有 [hook events](/zh-CN/hooks#hook-events) 都被支持。subagents 最常见的事件是：

| Event         | Matcher input | 何时触发                                   |
| :------------ | :------------ | :------------------------------------- |
| `PreToolUse`  | Tool name     | 在 subagent 使用工具之前                      |
| `PostToolUse` | Tool name     | 在 subagent 使用工具之后                      |
| `Stop`        | (none)        | 当 subagent 完成时（在运行时转换为 `SubagentStop`）|

此示例使用 `PreToolUse` hook 验证 Bash 命令，并在文件编辑后使用 `PostToolUse` 运行 linter：

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Frontmatter 中的 `Stop` hooks 会自动转换为 `SubagentStop` 事件。

#### 用于 subagent 事件的项目级 hooks

在 `settings.json` 中配置 hooks，以响应主会话中的 subagent 生命周期事件。

| Event           | Matcher input   | 何时触发             |
| :-------------- | :-------------- | :--------------- |
| `SubagentStart` | Agent type name | 当 subagent 开始执行时 |
| `SubagentStop`  | Agent type name | 当 subagent 完成时   |

两个事件都支持匹配器以按名称针对特定代理类型。此示例仅在 `db-agent` subagent 启动时运行设置脚本，并在任何 subagent 停止时运行清理脚本：

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

有关完整的 hook 配置格式，请参阅 [Hooks](/zh-CN/hooks)。

## 使用 subagents

### 理解自动委托

Claude 根据您请求中的任务描述、subagent 配置中的 `description` 字段和当前上下文自动委托任务。要鼓励主动委托，在您的 subagent 的 description 字段中包含"use proactively"之类的短语。

### 显式调用 subagents

当自动委托不够时，您可以自己请求 subagent。三种模式从一次性建议升级到会话范围的默认值：

- **自然语言**：在提示中命名 subagent；Claude 决定是否委托
- **@-mention**：保证 subagent 为一个任务运行
- **会话范围**：整个会话使用该 subagent 的系统提示、工具限制和模型，通过 `--agent` 标志或 `agent` 设置

对于自然语言，没有特殊语法。命名 subagent，Claude 通常会委托：

```text theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention subagent。** 输入 `@` 并从类型提前中选择 subagent，就像您 @-mention 文件一样。这确保特定 subagent 运行，而不是将选择留给 Claude：

```text theme={null}
@"code-reviewer (agent)" look at the auth changes
```

您的完整消息仍然发送给 Claude，它根据您的要求为 subagent 编写任务提示。@-mention 控制调用哪个 subagent，而不是它接收什么提示。

由启用的 [plugin](/zh-CN/plugins) 提供的 Subagents 在类型提前中显示为其作用域名称，例如 `my-plugin:code-reviewer` 或 `my-plugin:review:security`，当 plugin [将 agents 组织到子文件夹中](#choose-the-subagent-scope)。命名背景 subagents 当前在会话中运行也出现在类型提前中，在名称旁边显示其状态。您也可以手动输入提及而不使用选择器：`@agent-<name>` 用于本地 subagents，或 `@agent-` 后跟 plugin subagents 的作用域名称，例如 `@agent-my-plugin:code-reviewer`。

**将整个会话作为 subagent 运行。** 传递 [`--agent <name>`](/zh-CN/cli-reference) 以启动一个会话，其中主线程本身采用该 subagent 的系统提示、工具限制和模型：

```bash theme={null}
claude --agent code-reviewer
```

Subagent 的系统提示完全替换默认 Claude Code 系统提示，就像 [`--system-prompt`](/zh-CN/cli-reference) 一样。`CLAUDE.md` 文件和项目内存仍然通过正常消息流加载。代理名称在启动标题中显示为 `@<name>`，以便您可以确认它是活跃的。

这适用于内置和自定义 subagents，当您恢复会话时选择会持续。

对于 plugin 提供的 subagent，您可以仅传递代理名称，Claude Code 会找到它：

```bash theme={null}
claude --agent security-reviewer
```

如果多个 plugins 提供具有相同名称的 agents，传递作用域名称以消除歧义：

```bash theme={null}
claude --agent my-plugin:security-reviewer
```

如果 plugin 将 agent 放在其 `agents/` 目录的子文件夹中，请在作用域名称中包含子文件夹，例如 `claude --agent my-plugin:review:security`。

要使其成为项目中每个会话的默认值，在 `.claude/settings.json` 中设置 `agent`：

```json theme={null}
{
  "agent": "code-reviewer"
}
```

如果两者都存在，CLI 标志覆盖设置。

### 在前台或后台运行 subagents

Subagents 可以在前台（阻塞）或后台（并发）运行：

- **前台 subagents** 阻塞主对话直到完成。权限提示会在出现时传递给您。
- **后台 subagents** 在您继续工作时并发运行。它们使用会话中已授予的权限运行，并自动拒绝任何会提示的工具调用。如果后台 subagent 需要提出澄清问题，该工具调用失败，但 subagent 继续。

如果后台 subagent 由于缺少权限而失败，您可以启动一个新的前台 subagent 来执行相同的任务以使用交互式提示重试。

Claude 根据任务决定是否在前台或后台运行 subagents。您也可以：

- 要求 Claude "run this in the background"
- 按 **Ctrl+B** 将运行中的任务放在后台

要禁用所有后台任务功能，请将 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量设置为 `1`。请参阅 [Environment variables](/zh-CN/env-vars)。

当 [fork mode](#fork-the-current-conversation) 启用时，每个 subagent 生成都在后台运行，无论 `background` 字段如何。分叉仍然在您的终端中出现权限提示；命名 subagents 自动拒绝任何会提示的内容，如上所述。

### 常见模式

#### 隔离高容量操作

subagents 最有效的用途之一是隔离产生大量输出的操作。运行测试、获取文档或处理日志文件可能会消耗大量上下文。通过将这些委托给 subagent，详细输出保留在 subagent 的上下文中，而只有相关摘要返回到您的主对话。

```text theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### 运行并行研究

对于独立的调查，生成多个 subagents 以同时工作：

```text theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

每个 subagent 独立探索其区域，然后 Claude 综合这些发现。当研究路径彼此不依赖时，这效果最好。

<Warning>
  当 subagents 完成时，它们的结果返回到您的主对话。运行许多 subagents，每个都返回详细结果，可能会消耗大量上下文。
</Warning>

对于需要持续并行性或超过您的 context window 的任务，[agent teams](/zh-CN/agent-teams) 为每个工作者提供自己的独立上下文。

#### 链接 subagents

对于多步骤工作流，要求 Claude 按顺序使用 subagents。每个 subagent 完成其任务并将结果返回给 Claude，然后将相关上下文传递给下一个 subagent。

```text theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### 在 subagents 和主对话之间选择

在以下情况下使用 **主对话**：

- 任务需要频繁的来回或迭代细化
- 多个阶段共享重要上下文（规划 → 实现 → 测试）
- 您正在进行快速、有针对性的更改
- 延迟很重要。Subagents 从头开始，可能需要时间来收集上下文

在以下情况下使用 **subagents**：

- 任务产生您不需要在主上下文中的详细输出
- 您想强制执行特定的工具限制或权限
- 工作是自包含的，可以返回摘要

当您想要可重用的提示或在主对话上下文中运行的工作流而不是隔离的 subagent 上下文时，请改为考虑 [Skills](/zh-CN/skills)。

对于关于对话中已有内容的快速问题，使用 [`/btw`](/zh-CN/interactive-mode#side-questions-with-%2Fbtw) 而不是 subagent。它看到您的完整上下文但没有工具访问，答案被丢弃而不是添加到历史记录。

<Note>
  Subagents 无法生成其他 subagents。如果您的工作流需要嵌套委托，请使用 [Skills](/zh-CN/skills) 或从主对话 [链接 subagents](#chain-subagents)。
</Note>

### 管理 subagent 上下文

#### 启动时加载的内容

每个 subagent 都以新鲜的隔离上下文窗口开始。它看不到您的对话历史、您已经调用的技能或 Claude 已经读取的文件。Claude 编写一条委托消息来总结任务，subagent 从那里开始工作。例外是 [fork](#fork-the-current-conversation)，它继承父对话而不是从头开始。

非 fork subagent 的初始上下文包含：

- **系统提示**：代理自己的提示加上 Claude Code 附加的环境详情，而不是完整的 Claude Code 系统提示。自定义 subagents 在 [markdown 正文](#write-subagent-files) 或 `prompt` 字段中定义它们。内置代理有预定义的提示。
- **任务消息**：Claude 在移交工作时编写的委托提示。
- **CLAUDE. md 和内存**：主对话加载的 [内存层次结构](/zh-CN/memory#how-claude-md-files-load) 的每个级别，包括 `~/.claude/CLAUDE.md`、项目规则、`CLAUDE.local.md` 和托管策略文件。内置的 Explore 和 Plan 代理跳过这个。
- **Git 状态**：在父会话开始时拍摄的快照。当工作目录不是 Git 存储库或 [`includeGitInstructions`](/zh-CN/settings#available-settings) 为 `false` 时不存在。Explore 和 Plan 无论如何都跳过它。
- **预加载的技能**：代理的 [`skills` 字段](#preload-skills-into-subagents) 中命名的任何技能的完整内容。内置代理不预加载技能。

Explore 和 Plan 是仅有的省略 CLAUDE. md 和 git 状态的 subagents。没有 frontmatter 字段或按代理设置来改变哪些代理跳过它们。

主对话使用完整的 CLAUDE. md 上下文读取 Explore 和 Plan 结果，所以大多数规则不需要到达 subagent 本身。如果规则必须，例如"忽略 `vendor/` 目录"，在您给 Claude 委托时的提示中重新陈述它。

#### 恢复 subagents

每个 subagent 调用都会创建一个具有新鲜上下文的新实例。要继续现有 subagent 的工作而不是重新开始，要求 Claude 恢复它。

恢复的 subagents 保留其完整的对话历史，包括所有以前的工具调用、结果和推理。Subagent 从它停止的地方继续，而不是从头开始。

当 subagent 完成时，Claude 接收其代理 ID。Claude 使用 `SendMessage` 工具，将代理的 ID 作为 `to` 字段来恢复它。`SendMessage` 工具仅在通过 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用 [agent teams](/zh-CN/agent-teams) 时可用。

要恢复 subagent，要求 Claude 继续之前的工作：

```text theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

如果停止的 subagent 接收 `SendMessage`，它会在后台自动恢复，无需新的 `Agent` 调用。

您也可以要求 Claude 提供代理 ID，如果您想明确引用它，或在 `~/.claude/projects/{project}/{sessionId}/subagents/` 的转录文件中找到 ID。每个转录存储为 `agent-{agentId}.jsonl`。

Subagent 转录独立于主对话持久化：

- **主对话压缩**：当主对话压缩时，subagent 转录不受影响。它们存储在单独的文件中。
- **会话持久性**：Subagent 转录在其会话中持久化。您可以通过恢复相同的会话在重启 Claude Code 后 [恢复 subagent](#resume-subagents)。
- **自动清理**：转录根据 `cleanupPeriodDays` 设置（默认：30 天）进行清理。

#### 自动压缩

Subagents 支持使用与主对话相同的逻辑进行自动压缩。默认情况下，自动压缩在大约 95% 容量时触发。要更早触发压缩，请将 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 设置为较低的百分比（例如，`50`）。有关详细信息，请参阅 [environment variables](/zh-CN/env-vars)。

压缩事件记录在 subagent 转录文件中：

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

`preTokens` 值显示压缩发生前使用了多少令牌。

## 分叉当前对话

<Note>
  分叉 subagents 是实验性的，需要 Claude Code v2.1.117 或更高版本。行为和配置可能在未来版本中更改。通过将 [`CLAUDE_CODE_FORK_SUBAGENT`](/zh-CN/env-vars) 环境变量设置为 `1` 来启用它们。该变量在交互模式以及通过 SDK 或 `claude -p` 中被遵守。
</Note>

分叉是一个 subagent，它继承到目前为止的整个对话，而不是从头开始。这消除了 subagents 通常提供的输入隔离：分叉看到与主会话相同的系统提示、工具、模型和消息历史，因此您可以将其交给一个辅助任务而无需重新解释情况。分叉自己的工具调用仍然保持在您的对话之外，只有其最终结果返回，因此您的主 context window 保持干净。当命名 subagent 需要太多背景才能有用时，或当您想从相同的起点并行尝试多种方法时，使用分叉。

启用分叉模式以三种方式改变 Claude Code：

- Claude 在它会使用 [general-purpose](#built-in-subagents) subagent 时生成分叉。命名 subagents 如 Explore 仍然像以前一样生成。
- 每个 subagent 生成都在 [background](#run-subagents-in-foreground-or-background) 中运行，无论它是分叉还是命名 subagent。设置 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 为 `1` 以保持生成同步。
- `/fork` 命令生成分叉而不是充当 [`/branch`](/zh-CN/commands) 的别名。

您可以使用 `/fork` 后跟指令自己启动分叉。Claude Code 从指令的前几个单词命名分叉。以下示例分叉对话以在您继续主会话中的实现时草拟测试用例：

```text theme={null}
/fork draft unit tests for the parser changes so far
```

分叉出现在提示下方的面板中，并在您继续工作时在后台运行。完成后，其结果作为消息到达您的主对话。下一部分涵盖了在分叉运行时观察和引导它们的面板控制。

### 观察和引导运行中的分叉

运行中的分叉出现在提示输入下方的面板中，主会话有一行，每个分叉有一行。使用这些键与面板交互：

| Key       | Action             |
| :-------- | :----------------- |
| `↑` / `↓` | 在行之间移动             |
| `Enter`   | 打开所选分叉的转录并向其发送后续消息 |
| `x`       | 关闭完成的分叉或停止运行中的分叉   |
| `Esc`     | 将焦点返回到提示输入         |

### 分叉与命名 subagents 的区别

分叉继承主会话在生成时拥有的一切。命名 subagent 从自己的定义开始。

|              | 分叉         | 命名 subagent                                                      |
| :----------- | :--------- | :--------------------------------------------------------------- |
| 上下文          | 完整的对话历史    | 新鲜上下文，带有您传递的提示                                                   |
| 系统提示和工具      | 与主会话相同     | 来自 subagent 的 [definition file](#write-subagent-files)           |
| 模型           | 与主会话相同     | 来自 subagent 的 `model` 字段                                         |
| 权限           | 提示在您的终端中出现 | [Auto-denied](#run-subagents-in-foreground-or-background) 在后台运行时 |
| Prompt cache | 与主会话共享     | 单独的缓存                                                            |

因为分叉的系统提示和工具定义与父级相同，其第一个请求重用父级的 [prompt cache](/zh-CN/prompt-caching#subagents-and-the-cache)。这使得分叉比为需要相同上下文的任务生成新 subagent 更便宜。

当 Claude 通过 Agent 工具生成分叉时，它可以传递 `isolation: "worktree"` 以便分叉的文件编辑被写入单独的 git worktree 而不是您的检出。

### 限制

设置 `CLAUDE_CODE_FORK_SUBAGENT=1` 在交互式会话、[non-interactive mode](/zh-CN/headless) 和 Agent SDK 中启用分叉模式。分叉无法生成进一步的分叉。

## 示例 subagents

这些示例演示了构建 subagents 的有效模式。将它们用作起点，或使用 Claude 生成自定义版本。

<Tip>
  **最佳实践：**

  - **设计专注的 subagents：** 每个 subagent 应该在一个特定任务中表现出色
  - **编写详细的描述：** Claude 使用描述来决定何时委托
  - **限制工具访问：** 仅授予必要的权限以确保安全和专注
  - **检入版本控制：** 与您的团队共享项目 subagents
</Tip>

### 代码审查者

一个只读 subagent，审查代码而不修改它。此示例展示了如何设计一个专注的 subagent，具有有限的工具访问（无 Edit 或 Write）和详细的提示，指定确切要查找的内容以及如何格式化输出。

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### 调试器

一个可以分析和修复问题的 subagent。与代码审查者不同，这个包括 Edit，因为修复错误需要修改代码。提示提供了从诊断到验证的清晰工作流。

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### 数据科学家

一个用于数据分析工作的特定领域 subagent。此示例展示了如何为典型编码任务之外的专门工作流创建 subagents。它明确设置 `model: sonnet` 以获得更强大的分析能力。

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### 数据库查询验证器

一个允许 Bash 访问但验证命令以仅允许只读 SQL 查询的 subagent。此示例展示了当您需要比 `tools` 字段提供的更精细的控制时如何使用 `PreToolUse` hooks。

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [通过 stdin 将 hook 输入作为 JSON 传递](/zh-CN/hooks#pretooluse-input) 给 hook 命令。验证脚本读取此 JSON，提取正在执行的命令，并根据 SQL 写入操作列表检查它。如果检测到写入操作，脚本 [以代码 2 退出](/zh-CN/hooks#exit-code-2-behavior-per-event) 以阻止执行，并通过 stderr 向 Claude 返回错误消息。

在您的项目中的任何位置创建验证脚本。路径必须与您的 hook 配置中的 `command` 字段匹配：

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

在 macOS 和 Linux 上，使脚本可执行：

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

在 Windows 上，用 PowerShell 编写验证脚本，并在 hook 条目中添加 `shell: powershell`。请参阅 [在 PowerShell 中运行 hooks](/zh-CN/hooks#windows-powershell-tool)。

Hook 通过 stdin 接收 JSON，Bash 命令在 `tool_input.command` 中。退出代码 2 阻止操作并将错误消息反馈给 Claude。有关退出代码和输出的详细信息，请参阅 [Hooks](/zh-CN/hooks#exit-code-output)，有关完整的输入架构，请参阅 [Hook input](/zh-CN/hooks#pretooluse-input)。

## 后续步骤

现在您了解了 subagents，探索这些相关功能：

- [使用 plugins 分发 subagents](/zh-CN/plugins) 以在团队或项目中共享 subagents
- [以编程方式运行 Claude Code](/zh-CN/headless)，使用 Agent SDK 进行 CI/CD 和自动化
- [使用 MCP 服务器](/zh-CN/mcp) 为 subagents 提供对外部工具和数据的访问
