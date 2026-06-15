---
title: "Claude Code Skills — Frontmatter 参考"
type: concept
created: 2026-05-21
updated: 2026-05-21
sources: ["raw/articles/2026-05-21-claude-code-skills.md"]
tags: [claude-code, skills, frontmatter, configuration]
parent: "Claude Code Skills"
---

# Frontmatter 参考

## 完整字段列表

所有字段均为可选，位于 `SKILL.md` 顶部 `---` 标记之间：

| 字段 | 描述 |
|------|------|
| `name` | 显示名称。省略则使用目录名。仅小写字母、数字、连字符（最多 64 字符） |
| `description` | 功能描述。Claude 靠它决定何时自动加载。组合的 `description` + `when_to_use` 截断为 1,536 字符 |
| `when_to_use` | 额外触发上下文（触发短语、示例请求）。附加到 description，计入 1,536 字符上限 |
| `argument-hint` | 自动完成时显示的参数提示，如 `[issue-number]` |
| `arguments` | 命名位置参数列表，用于 `$name` 替换 |
| `disable-model-invocation` | `true` = 仅用户可调用。防止 Claude 自动加载，也防止预加载到 subagent |
| `user-invocable` | `false` = 仅 Claude 可调用。从 `/` 菜单中隐藏 |
| `allowed-tools` | Skill 活动时 Claude 可免批准使用的工具列表 |
| `model` | Skill 活动时使用的模型。覆盖仅持续当前轮，会话模型在下一提示时恢复 |
| `effort` | Skill 活动时的工作量级别：`low`/`medium`/`high`/`xhigh`/`max` |
| `context` | 设为 `fork` 以在分叉的 subagent 上下文中运行 |
| `agent` | 配合 `context: fork` 使用时指定 subagent 类型 |
| `hooks` | 限定于此 skill 生命周期的 hooks |
| `paths` | Glob 模式，限制何时激活。仅处理匹配文件时自动加载 |
| `shell` | 用于 `` !`command` `` 的 shell：`bash`（默认）或 `powershell` |

## 调用控制矩阵

| Frontmatter | 用户可调用 | Claude 可调用 | 何时加载到上下文 |
|-------------|----------|-------------|----------------|
| （默认） | 是 | 是 | 描述始终在上下文，调用时加载完整 skill |
| `disable-model-invocation: true` | 是 | 否 | 描述不在上下文，用户调用时加载完整 skill |
| `user-invocable: false` | 否 | 是 | 描述始终在上下文，调用时加载完整 skill |

**关键区别**：`user-invocable` 仅控制菜单可见性，不控制 Skill 工具访问。使用 `disable-model-invocation: true` 来阻止 Claude 程序调用。

## 工具预先批准

`allowed-tools` 在 skill 活动时授予工具权限，Claude 无需提示即可使用：

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

这不限制哪些工具可用——其他工具仍可调用，受权限设置管理。

## 字符串替换

Skill 内容支持动态值替换：

| 变量 | 描述 |
|------|------|
| `$ARGUMENTS` | 调用时传递的所有参数。若内容中不存在，参数以 `ARGUMENTS: <value>` 追加 |
| `$ARGUMENTS[N]` | 按 0 基索引访问特定参数 |
| `$N` | `$ARGUMENTS[N]` 的简写（`$0` = 第一个参数） |
| `$name` | `arguments` frontmatter 中声明的命名参数，按位置映射 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_EFFORT}` | 当前工作量级别 |
| `${CLAUDE_SKILL_DIR}` | 包含 SKILL.md 的目录路径 |

索引参数使用 shell 风格引用：`/my-skill "hello world"` 使 `$0` 扩展为 `hello world`。

### 命名参数示例

```yaml
---
name: migrate-component
description: Migrate a component between frameworks
arguments: [component, from, to]
---

Migrate the $component component from $from to $to.
Preserve all existing behavior and tests.
```

运行 `/migrate-component SearchBar React Vue` 时 `$component` = `SearchBar`，`$from` = `React`，`$to` = `Vue`。

## Skill 内容生命周期

调用时，`SKILL.md` 内容作为单个消息进入对话，在会话剩余部分保持。Claude Code 不会在后续轮次重新读取 skill 文件。

**自动压缩行为**：当对话被总结以释放上下文时，Claude Code 重新附加每个 skill 的最新调用，保留前 5,000 个 token。重新附加的 skills 共享 25,000 token 的组合预算，从最近调用的 skill 开始填充。较旧的 skills 可能在压缩后完全删除。

如果 skill 在第一个响应后停止影响行为，内容通常仍然存在——模型正在选择其他方法。加强 `description` 和说明，或使用 hooks 确定性地强制行为。

## 从设置覆盖可见性

`skillOverrides` 设置控制 skill 可见性，无需编辑 SKILL.md：

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

| 值 | 列出给 Claude | 在 `/` 菜单中 |
|----|-------------|-------------|
| `"on"` | 名称和描述 | 是 |
| `"name-only"` | 仅名称 | 是 |
| `"user-invocable-only"` | 隐藏 | 是 |
| `"off"` | 隐藏 | 隐藏 |

通过 `/skills` 菜单交互式设置：高亮 skill 按 `Space` 循环状态，`Enter` 保存。

## Skill 描述截断

所有 skill 名称始终加载，但描述受字符预算限制（按模型上下文窗口的 1% 扩展）。预算溢出时，调用最少的 skills 的描述首先被删除。

解决方案：
- 设置 `skillListingBudgetFraction`（如 `0.02` = 2%）扩大预算
- 在 `skillOverrides` 中将低优先级条目设为 `"name-only"`
- 修剪 `description` + `when_to_use`（组合上限 1,536 字符）
