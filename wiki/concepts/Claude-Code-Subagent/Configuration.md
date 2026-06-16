---
title: "Claude Code Subagent — 配置参考"
type: concept
created: 2026-05-21
updated: 2026-05-21
sources: ["raw/articles/2026-05-21-claude-code-sub-agents.md"]
tags: [claude-code, subagent, configuration, frontmatter, tools, permissions]
parent: wiki/concepts/Claude-Code-Subagent/index.md
---

# 配置参考

## Frontmatter 字段

Subagent 文件使用 YAML frontmatter + Markdown 正文（系统提示）。只有 `name` 和 `description` 是必需的。

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | 是 | 小写字母和连字符的唯一标识符。Hooks 将此值作为 `agent_type` 接收 |
| `description` | 是 | Claude 何时应该委托给此 subagent |
| `tools` | 否 | 允许的工具列表。省略则继承所有工具 |
| `disallowedTools` | 否 | 从继承或指定列表中删除的工具 |
| `model` | 否 | `sonnet`/`opus`/`haiku`/完整模型 ID/`inherit`。默认 `inherit` |
| `permissionMode` | 否 | `default`/`acceptEdits`/`auto`/`dontAsk`/`bypassPermissions`/`plan` |
| `maxTurns` | 否 | subagent 停止前的最大代理轮数 |
| `skills` | 否 | 启动时加载到上下文的 skills 列表 |
| `mcpServers` | 否 | 对此 subagent 可用的 MCP 服务器 |
| `hooks` | 否 | 限定于此 subagent 的生命周期 hooks |
| `memory` | 否 | 持久内存范围：`user`/`project`/`local` |
| `background` | 否 | `true` = 始终作为后台任务运行 |
| `effort` | 否 | 工作量级别：`low`/`medium`/`high`/`xhigh`/`max` |
| `isolation` | 否 | `worktree` = 在临时 git worktree 中运行 |
| `color` | 否 | 显示颜色：`red`/`blue`/`green`/`yellow`/`purple`/`orange`/`pink`/`cyan` |
| `initialPrompt` | 否 | 作为主会话代理运行时自动提交的第一个用户轮次 |

## 模型选择

模型解析优先级：
1. `CLAUDE_CODE_SUBAGENT_MODEL` 环境变量
2. 每次调用的 `model` 参数（Claude 可在调用时传递）
3. Subagent 定义的 `model` frontmatter
4. 主对话的模型

## 工具限制

### 允许列表（tools）

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

### 拒绝列表（disallowedTools）

```yaml
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

两者都设置时，`disallowedTools` 先应用，然后 `tools` 针对剩余池解析。

### 限制可生成的 Subagent 类型

当代理作为主线程运行时（`claude --agent`），使用 `Agent(agent_type)` 语法限制可生成的 subagent：

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

- `Agent(worker, researcher)` = 仅允许这两个 subagent
- `Agent`（不带括号）= 允许生成任何 subagent
- 省略 `Agent` = 无法生成任何 subagent

**注意**：Subagents 无法生成其他 subagents，此限制仅适用于主线程代理。

## MCP 服务器

为 subagent 提供对主对话中不可用的 MCP 服务器的访问：

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
---
```

- 内联定义：仅此 subagent 可用，启动时连接，完成时断开
- 字符串引用：复用父会话的已配置服务器

将 MCP 服务器保持在主对话之外（避免工具描述消耗上下文）的好方法。

## 权限模式

| 模式 | 行为 |
|------|------|
| `default` | 标准权限检查，带有提示 |
| `acceptEdits` | 自动接受文件编辑和常见文件系统命令 |
| `auto` | 后台分类器审查命令和受保护目录的写入 |
| `dontAsk` | 自动拒绝权限提示（显式允许的工具仍工作） |
| `bypassPermissions` | 跳过权限提示（谨慎使用） |
| `plan` | Plan mode（只读探索） |

**继承规则**：
- 父级 `bypassPermissions` 或 `acceptEdits` 优先，无法被覆盖
- 父级 `auto` 模式下，subagent 继承 auto mode，frontmatter 中的 `permissionMode` 被忽略

## Skills 预加载

在启动时将技能内容注入 subagent 上下文：

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
```

每个列出的技能的完整内容被注入。此字段控制预加载哪些技能，不限制 subagent 可以访问哪些技能——它仍然可以通过 Skill 工具发现和调用其他技能。

**注意**：无法预加载设置了 `disable-model-invocation: true` 的技能。

## CLI 定义

启动时通过 JSON 传递，仅存在于该会话中：

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer.",
    "prompt": "You are a senior code reviewer.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

`--agents` 的 JSON 使用与文件相同的字段：`description`、`prompt`（等同于 markdown 正文）、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills`、`initialPrompt`、`memory`、`effort`、`background`、`isolation`、`color`。

## 禁用特定 Subagents

在 settings 的 `deny` 数组中添加：

```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

或 CLI 标志：`claude --disallowedTools "Agent(Explore)"`
