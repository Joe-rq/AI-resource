---
title: "Claude Code Subagent — 调用与上下文管理"
type: concept
created: 2026-05-21
updated: 2026-05-21
sources: ["claude-code-sub-agents"]
tags: [claude-code, subagent, invocation, context, memory, hooks, fork, resume]
parent: "Claude Code Subagent"
---

# 调用与上下文管理

## 自动委托

Claude 根据任务描述、subagent 的 `description` 字段和当前上下文自动委托。在 description 中包含 "use proactively" 等短语可鼓励主动委托。

## 显式调用

三种模式从一次性建议升级到会话范围默认：

1. **自然语言**：命名 subagent，Claude 决定是否委托
2. **@-mention**：`@"code-reviewer (agent)" look at auth changes` — 保证该 subagent 运行
3. **会话范围**：`claude --agent code-reviewer` 或 settings 中 `"agent": "code-reviewer"`

Plugin 提供的 subagent 使用作用域名称：`@agent-my-plugin:code-reviewer`。

## 启动时加载的内容

每个 subagent 以新鲜的隔离上下文窗口开始。它看不到对话历史、已调用的技能或已读取的文件。Claude 编写委托消息来总结任务，subagent 从那里开始工作。

非 fork subagent 的初始上下文包含：

| 内容 | 说明 |
|------|------|
| 系统提示 | 代理自己的提示 + 环境详情（非完整 Claude Code 系统提示） |
| 任务消息 | Claude 在移交时编写的委托提示 |
| CLAUDE.md 和内存 | 主对话加载的内存层次结构的每个级别 |
| Git 状态 | 父会话开始时的快照 |
| 预加载的 skills | `skills` 字段中命名的技能的完整内容 |

**例外**：Explore 和 Plan 跳过 CLAUDE.md 和 git 状态，以保持上下文小且成本低。没有 frontmatter 字段可以改变哪些代理跳过它们。

## 恢复 Subagent

每个 subagent 调用默认创建新实例。要继续现有工作：

```text
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context]
```

恢复的 subagent 保留完整对话历史（所有以前的工具调用、结果和推理）。Claude 使用 `SendMessage` 工具和代理 ID 来恢复。需要启用 agent teams（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`）。

**转录持久性**：
- 主对话压缩时，subagent 转录不受影响
- 转录存储在 `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`
- 根据 `cleanupPeriodDays`（默认 30 天）自动清理

## 持久内存

`memory` 字段为 subagent 提供跨会话的持久目录：

| 范围 | 位置 | 使用时机 |
|------|------|---------|
| `user` | `~/.claude/agent-memory/<name>/` | 所有项目中记住学习 |
| `project` | `.claude/agent-memory/<name>/` | 项目特定，可通过版本控制共享 |
| `local` | `.claude/agent-memory-local/<name>/` | 项目特定但不检入版本控制 |

启用内存时：
- 系统提示包括读取和写入内存目录的说明
- 包含 `MEMORY.md` 的前 200 行或 25KB
- Read、Write、Edit 工具自动启用

**最佳实践**：
- `project` 是推荐的默认范围
- 要求 subagent 在开始前查阅内存："Review this PR, and check your memory for patterns"
- 要求完成后更新内存："Save what you learned to your memory"
- 在 subagent 的 markdown 中包含内存说明，让它主动维护知识库

## Hooks

### Frontmatter Hooks

直接在 subagent 文件中定义，仅在该 subagent 活跃时运行：

```yaml
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

支持的事件：`PreToolUse`（工具使用前）、`PostToolUse`（工具使用后）、`Stop`（subagent 完成时自动转为 `SubagentStop`）。

### 项目级 Hooks

在 `settings.json` 中配置，响应主会话中的 subagent 生命周期事件：

| 事件 | 匹配器输入 | 触发时机 |
|------|----------|---------|
| `SubagentStart` | Agent type name | subagent 开始执行时 |
| `SubagentStop` | Agent type name | subagent 完成时 |

### 条件规则示例

使用 `PreToolUse` hook 实现只读数据库查询：

```yaml
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

验证脚本通过 stdin 接收 JSON，提取命令，以 exit code 2 阻止写入操作。

## 自动压缩

Subagents 支持与主对话相同的自动压缩逻辑（默认 ~95% 容量触发）。可通过 `CLAUDE_AUTOMPACT_PCT_OVERRIDE` 设置更低阈值。压缩事件记录在转录文件中。

## Fork 模式

Fork 继承父对话的完整上下文，而非从头开始。启用：`CLAUDE_CODE_FORK_SUBAGENT=1`。

```text
/fork draft unit tests for the parser changes so far
```

Fork 的工具调用保留在对话之外，只有最终结果返回，主 context window 保持干净。Fork 无法生成进一步的 fork。

### 面板控制

| 按键 | 操作 |
|------|------|
| `↑` / `↓` | 在行之间移动 |
| `Enter` | 打开所选 fork 的转录并发送后续消息 |
| `x` | 关闭完成的 fork 或停止运行中的 fork |
| `Esc` | 将焦点返回到提示输入 |

### Isolation: Worktree

通过 `isolation: worktree` 让 subagent 在临时 git worktree 中运行，获得仓库的隔离副本。如果 subagent 不进行任何更改，worktree 自动清理。Fork 也可通过 Agent 工具传递 `isolation: "worktree"`。

## 选择主对话 vs Subagent

**使用主对话**：
- 任务需要频繁的来回或迭代细化
- 多个阶段共享重要上下文
- 正在进行快速、有针对性的更改
- 延迟很重要（subagent 从头开始收集上下文）

**使用 Subagent**：
- 任务产生不需要在主上下文中的详细输出
- 想强制执行特定的工具限制或权限
- 工作是自包含的，可以返回摘要

对于快速问题，使用 `/btw` 而非 subagent——它看到完整上下文但没有工具访问，答案被丢弃。
