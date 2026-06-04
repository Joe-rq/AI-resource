> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用动态工作流大规模编排子代理

> 动态工作流从 Claude 编写的脚本中编排许多子代理，您可以重新运行。用于代码库审计、大型迁移和交叉检查研究。

{/* plan-availability: feature=workflows plans=pro,max,team,enterprise providers=all */}

<Note>
  动态工作流处于研究预览阶段。它们需要 Claude Code v2.1.154 或更高版本，在所有付费计划上可用，具有 Anthropic API 访问权限，以及在 Amazon Bedrock、Google Cloud Vertex AI 和 Microsoft Foundry 上可用。在 Pro 上，从 `/config` 中的"Dynamic workflows"行启用它们。
</Note>

动态工作流是一个 JavaScript 脚本，可大规模编排[子代理](/zh-CN/sub-agents)。Claude 为您描述的任务编写脚本，运行时在后台执行它，同时您的会话保持响应。

当任务需要比一个对话能协调的更多代理时，或当您想将编排编纂为可以读取和重新运行的脚本时，请使用工作流。示例包括代码库范围的错误扫描、500 文件迁移、需要相互交叉检查来源的研究问题，以及在提交一个之前值得从多个独立角度起草的困难计划。

本页涵盖如何：

* 决定[何时使用工作流](#when-to-use-a-workflow)而不是子代理或 skills
* [运行捆绑工作流](#run-a-bundled-workflow)与 `/deep-research`
* [让 Claude 为您的任务编写工作流](#have-claude-write-a-workflow)并保存它
* 理解[工作流如何运行](#how-a-workflow-runs)和[管理运行](#manage-runs)

## 何时使用工作流

[子代理](/zh-CN/sub-agents)、[skills](/zh-CN/skills)、[agent teams](/zh-CN/agent-teams) 和工作流都可以运行多步骤任务。区别在于谁掌握计划：

|            | 子代理           | Skills        | Agent teams  | 工作流          |
| :--------- | :------------ | :------------ | :----------- | :----------- |
| 它是什么       | Claude 生成的工作者 | Claude 遵循的指令  | 监督对等会话的主导代理  | 运行时执行的脚本     |
| 谁决定接下来运行什么 | Claude，逐轮     | Claude，遵循提示   | 主导代理，逐轮      | 脚本           |
| 中间结果在哪里    | Claude 的上下文窗口 | Claude 的上下文窗口 | 共享任务列表       | 脚本变量         |
| 什么是可重复的    | 工作者定义         | 指令            | 团队定义         | 编排本身         |
| 规模         | 每轮几个委派任务      | 与子代理相同        | 少数几个长期运行的对等体 | 每次运行数十到数百个代理 |
| 中断         | 重启轮次          | 重启轮次          | 队友继续运行       | 在同一会话中可恢复    |

工作流将计划移入代码。使用子代理、skills 和 agent teams，Claude 是编排者：它逐轮决定接下来生成或分配什么，每个结果都进入上下文窗口。工作流脚本持有循环、分支和中间结果本身，所以 Claude 的上下文只持有最终答案。

将计划移入代码也让工作流应用可重复的质量模式，而不仅仅是运行更多代理：它可以让独立代理在报告之前对彼此的发现进行对抗性审查，或从多个角度起草计划并相互权衡，所以您获得比单次通过更可信的结果。

## 运行捆绑工作流

查看工作流运行的最快方式是运行 `/deep-research`，这是 Claude Code 包含的[内置工作流](#bundled-workflows)，用于跨许多来源调查问题。您将看到代理在后台通过一组阶段工作，同时您的会话保持空闲，最后获得一份报告而不是逐轮记录。

<Steps>
  <Step title="运行工作流">
    使用您想要调查的问题运行 `/deep-research`。它在多个角度上扇出网络搜索，获取并交叉检查它找到的来源，并综合一份引用的报告。

    ```text theme={null}
    /deep-research What changed in the Node.js permission model between v20 and v22?
    ```
  </Step>

  <Step title="允许工作流">
    Claude Code 询问是否允许工作流。选择**是**继续。确切的提示取决于您的权限模式。有关每种模式的选项，请参阅[在运行前批准计划](#approve-the-plan-before-it-runs)。
  </Step>

  <Step title="观看进度">
    运行在后台启动。运行 `/workflows`，使用箭头键选择运行，然后按 Enter 打开其进度视图：

    ```text theme={null}
    /workflows
    ```

    该视图显示每个阶段及其代理计数、令牌总数和经过的时间。深入任何阶段以查看其代理及每个代理发现的内容。有关完整的控制集，请参阅[观看运行](#watch-the-run)。

    您也可以从输入框下方的任务面板观看：运行进行时会出现一行进度摘要。按向下箭头聚焦它，然后按 Enter 展开。
  </Step>

  <Step title="阅读报告">
    运行完成后，报告进入您的会话。它引用每个声明来自的来源，未通过交叉检查的声明已被过滤掉。
  </Step>
</Steps>

要为您自己的任务运行工作流，[让 Claude 编写一个](#have-claude-write-a-workflow)，一旦运行完成您想要的操作，您可以[保存它](#save-the-workflow-for-reuse)作为您自己的命令。

### 捆绑工作流

Claude Code 包含 `/deep-research` 作为内置工作流：

| 命令                          | 它做什么                                                                                                                                 |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `/deep-research <question>` | 在多个角度上扇出网络搜索问题，获取并交叉检查它找到的来源，对每个声明投票，并返回一份引用的报告，其中未通过交叉检查的声明已被过滤掉。需要[WebSearch 工具](/zh-CN/tools-reference#websearch-tool-behavior)可用 |

[您自己保存的工作流](#save-the-workflow-for-reuse)以相同方式成为命令，并在 `/` 自动完成中与捆绑的工作流一起出现。

### 观看运行

工作流在后台运行，所以会话在代理工作时保持响应。随时运行 `/workflows` 列出运行中和已完成的工作流，然后选择一个打开其进度视图。

```text theme={null}
/workflows
```

进度视图显示每个阶段及其代理计数、令牌总数和经过的时间。页脚列出每个操作的键：

| 键             | 操作                                          |
| :------------ | :------------------------------------------ |
| `↑` / `↓`     | 选择一个阶段或代理                                   |
| `Enter` 或 `→` | 深入选定的阶段，然后进入代理以读取其提示、最近的工具调用和结果             |
| `Esc`         | 返回一个级别                                      |
| `j` / `k`     | 当代理详情溢出时在其中滚动                               |
| `p`           | 暂停或恢复运行                                     |
| `x`           | 停止选定的代理，或当焦点在运行上时停止整个工作流                    |
| `r`           | 重启选定的运行中代理                                  |
| `s`           | [保存](#save-the-workflow-for-reuse)运行的脚本作为命令 |

## 让 Claude 编写工作流

您可以通过两种方式让 Claude 为您的任务编写工作流：

* [在您的提示中请求工作流](#ask-for-a-workflow-in-your-prompt)，使用关键字 `ultracode`，Claude 为任务编写一个。
* [让 Claude 使用 ultracode 决定](#let-claude-decide-with-ultracode)：设置 `/effort ultracode`，Claude 为会话中的每个实质性任务规划工作流。

您也可以运行已存在的工作流命令：一个[捆绑工作流](#bundled-workflows)如 `/deep-research`，或一个您已[保存](#save-the-workflow-for-reuse)的。

### 在您的提示中请求工作流

要在不改变会话的努力级别的情况下将单个任务作为工作流运行，在您的提示中包含关键字 `ultracode`。用您自己的话提问，例如"使用工作流"或"运行工作流"，也可以工作：Claude 将直接请求视为相同的选择加入。在 v2.1.160 之前，字面触发关键字是 `workflow`；自然语言请求在两个版本中都有效。

```text theme={null}
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

Claude Code 在您的输入中突出显示该关键字，Claude 为任务编写工作流脚本，而不是逐轮处理它。如果您不打算启动工作流，在 macOS 上按 `Option+W` 或在 Windows 和 Linux 上按 `Alt+W` 来忽略此提示的突出显示，或在突出显示的关键字后面的光标处按退格键。要完全停止该关键字触发，请在 `/config` 中关闭 Ultracode 关键字触发。

如果运行完成了您想要的操作，您可以之后[将其保存为命令](#save-the-workflow-for-reuse)。

如果您已经用另一种方式构建了编排器，例如子代理提示的文件夹或一个分散工作的技能，您可以指向 Claude 并要求一个执行相同操作的工作流。

### 让 Claude 使用 ultracode 决定

Ultracode 是一个 Claude Code 设置，它结合了 `xhigh` [推理努力](/zh-CN/model-config#adjust-effort-level)与自动工作流编排。启用它后，Claude 为每个实质性任务规划工作流，而不是等待您要求。

```text theme={null}
/effort ultracode
```

启用 ultracode 后，Claude 决定任务何时值得工作流。单个请求可以变成一系列工作流：一个理解代码，一个进行更改，一个验证它。这适用于会话中的每个任务，所以每个请求使用更多令牌并花费比较低努力级别更长的时间。

Ultracode 持续当前会话，当您启动新会话时重置。当您返回日常工作时，使用 `/effort high` 下降。它在支持 `xhigh` [努力](/zh-CN/model-config#adjust-effort-level)的模型上可用；在其他模型上，`/effort` 菜单不提供它。

### 在运行前批准计划

在 CLI 中，每次运行的提示显示计划的阶段和这些选项：

* **是，运行它**：启动运行
* **是，不再为 `<path>` 中的 `<name>` 询问**：启动，并从现在起跳过此项目中此工作流的此提示
* **查看原始脚本**：在决定前读取脚本
* **否**：取消

`Ctrl+G` 在您的编辑器中打开脚本。`Tab` 让您在运行启动前调整提示。

您是否看到此提示取决于您的[权限模式](/zh-CN/permission-modes)：

| 权限模式                       | 何时提示您                                                  |
| :------------------------- | :----------------------------------------------------- |
| 默认，接受编辑                    | 每次运行，除非您已为此项目中的该工作流选择**是，不再询问**                        |
| 自动                         | 仅首次启动。任何**是**在您的用户设置中记录同意，之后启动无需提示。当 ultracode 启用时完全跳过 |
| 绕过权限，`claude -p`，Agent SDK | 从不。运行立即启动                                              |

在桌面应用中，批准卡显示工作流名称、阶段列表和令牌使用警告，带有**一次**、**总是**和**拒绝**操作。进度视图出现在"后台任务"侧窗格中。

您的权限模式仅控制上面的启动提示。工作流生成的子代理始终在 `acceptEdits` 模式下运行，并继承您的[工具允许列表](/zh-CN/settings#permission-settings)，无论您的会话模式如何。文件编辑自动批准。

Shell 命令、网络获取和不在您的允许列表中的 MCP 工具仍然可以在运行中提示您。要在长时间运行中避免这种情况，在启动前将代理需要的命令添加到您的允许列表。

在 `claude -p` 和 Agent SDK 中没有人提示，所以工具调用遵循您配置的权限规则，无需交互式确认。

### 保存工作流以供重用

当 Claude 为您将重复的任务编写工作流时，您可以将该运行的脚本保存为命令。像您在每个分支上运行的审查这样的过程然后每次运行相同的编排。

运行 `/workflows`，选择您想保留的运行，然后按 `s`。在保存对话中，Tab 在两个保存位置之间切换：

* `.claude/workflows/` 在您的项目中：与克隆仓库的每个人共享
* `~/.claude/workflows/` 在您的主目录中：在每个项目中可用，仅对您可见

按 Enter 保存。工作流在未来会话中从任一位置作为 `/<name>` 运行。

如果项目工作流和个人工作流共享名称，项目工作流运行。

### 将输入传递给保存的工作流

保存的工作流可以通过 `args` 参数接受输入。脚本将其读取为名为 `args` 的全局变量。使用此功能在调用时提供研究问题、目标路径列表或配置对象，而不是为每次运行编辑脚本。

以下提示使用问题编号列表运行保存的工作流：

```text theme={null}
> Run /triage-issues on issues 1024, 1025, and 1030
```

Claude 将列表作为结构化数据传递，所以脚本可以直接在 `args` 上调用数组和对象方法，无需先解析它。如果省略 `args`，脚本内的全局变量为 `undefined`。

## 工作流如何运行

工作流运行时在隔离环境中执行脚本，与您的对话分开。中间结果保留在脚本变量中，而不是进入 Claude 的上下文。

每次运行都会将其脚本写入您会话目录下 `~/.claude/projects/` 中的文件。运行开始时 Claude 会收到该路径，因此您可以要求它提供。您可以打开该文件来读取 Claude 编写的编排脚本，将其与之前运行的脚本进行对比，或编辑它并要求 Claude 从编辑后的版本重新启动。

运行时在运行进行时跟踪每个代理的结果，这是使运行在同一会话中[可恢复](#resume-after-a-pause)的原因。

### 行为和限制

运行时应用以下约束：

| 约束                           | 为什么                                      |
| :--------------------------- | :--------------------------------------- |
| 无中途用户输入                      | 仅代理权限提示可以暂停运行。对于阶段之间的签署，将每个阶段作为其自己的工作流运行 |
| 无来自工作流本身的直接文件系统或 shell 访问    | 代理读取、写入和运行命令。脚本协调代理                      |
| 最多 16 个并发代理，在 CPU 核心有限的机器上更少 | 限制本地资源使用                                 |
| 每次运行 1,000 个代理总数             | 防止失控循环                                   |

## 管理运行

运行启动后，您可以从 `/workflows` 视图管理它，或通过展开输入框下方任务面板中的其进度行来管理。

### 暂停后恢复

如果您停止运行，您可以恢复它：已完成的代理返回其缓存结果，其余的实时运行。从 `/workflows` 恢复暂停的运行，选择它并按 `p`，或要求 Claude 使用相同脚本重新启动工作流。

恢复在同一 Claude Code 会话中工作。如果您在工作流运行时退出 Claude Code，下一个会话将从头启动工作流。

### 成本

工作流生成许多代理，所以单次运行可以使用比在对话中处理相同任务更多的令牌。运行计入您的计划使用和速率限制，如任何其他会话。

要在提交大型任务前评估支出，请先在小范围上运行工作流：一个目录而不是整个仓库，或一个狭窄的问题而不是一个宽泛的问题。`/workflows` 视图显示每个代理的令牌使用情况，随着运行进行，您可以随时在那里停止运行而不会丢失已完成的工作。运行时的[代理上限](#behavior-and-limits)限制单次运行可以生成多少个代理，这限制了失控脚本的成本。

工作流中的每个代理使用您的会话模型，除非脚本将阶段路由到不同的模型。要控制模型成本：

* 在大型运行前检查 `/model`，如果您通常为日常工作切换到较小的模型
* 当您描述任务时，要求 Claude 为不需要最强模型的阶段使用较小的模型

### 关闭工作流

工作流在 CLI、桌面应用、IDE 扩展、[非交互模式](/zh-CN/headless)与 `claude -p` 和 [Agent SDK](/zh-CN/agent-sdk/overview) 中可用。相同的禁用设置在每个表面上应用。

要为自己关闭工作流：

* 在 `/config` 中切换"Dynamic workflows"关闭。在会话中持续。
* 在 `~/.claude/settings.json` 中设置 `"disableWorkflows": true`。在会话中持续。
* 设置 `CLAUDE_CODE_DISABLE_WORKFLOWS=1`。在启动时读取，所以它在您设置它的任何地方应用。

要为整个组织关闭工作流，在[托管设置](/zh-CN/server-managed-settings)中设置 `"disableWorkflows": true`，或使用[Claude Code 管理员设置](https://claude.ai/admin-settings/claude-code)页面上的切换。

当工作流被禁用时，捆绑工作流命令不可用，`ultracode` 关键字不再触发运行，`ultracode` 从 `/effort` 菜单中移除。

## 相关资源

* [并行运行代理](/zh-CN/agents)：比较子代理、代理视图、代理团队和工作流
* [创建自定义子代理](/zh-CN/sub-agents)：工作流编排的工作者原语
* [管理成本](/zh-CN/costs)：多代理运行如何计入使用限制
