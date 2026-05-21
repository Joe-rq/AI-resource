---
title: "Claude Code Skills — 动态上下文与 Subagent 执行"
type: concept
created: 2026-05-21
updated: 2026-05-21
sources: ["claude-code-skills"]
tags: [claude-code, skills, dynamic-context, subagent, fork, sharing]
parent: "Claude Code Skills"
---

# 动态上下文与 Subagent 执行

## 动态上下文注入

`` !`<command>` `` 语法在将 skill 内容发送给 Claude 之前运行 shell 命令。命令输出替换占位符，Claude 接收实际数据而非命令本身。

### 内联形式

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

执行流程：
1. 每个 `` !`<command>` `` 立即执行（在 Claude 看到任何内容之前）
2. 输出替换 skill 内容中的占位符
3. Claude 接收带有实际 PR 数据的完整提示

**限制**：替换对原始文件运行一次。命令输出作为纯文本插入，不会重新扫描以查找进一步的占位符。`` ! `` 必须出现在行首或紧跟空白之后才被识别。

### 多行命令

使用 ````!` `` 开头的围栏代码块：

````markdown
## Environment
```!
node --version
npm --version
git status --short
```
````

### 禁用 Shell 执行

设置 `"disableSkillShellExecution": true` 可禁用用户、项目、插件来源 skills 的 shell 执行。每个命令被替换为 `[shell command execution disabled by policy]`。捆绑和托管 skills 不受影响。此设置在托管设置中最有用。

## 在 Subagent 中运行 Skills

在 frontmatter 中添加 `context: fork`，skill 内容变成驱动 subagent 的提示。Subagent 将无法访问对话历史。

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

执行流程：
1. 创建新的隔离上下文
2. Subagent 接收 skill 内容作为其提示
3. `agent` 字段确定执行环境（模型、工具、权限）
4. 结果被总结并返回到主对话

### Skills 与 Subagents 的双向协作

| 方法 | 系统提示 | 任务 | 额外加载 |
|------|---------|------|---------|
| 带 `context: fork` 的 Skill | 来自代理类型 | SKILL.md 内容 | CLAUDE.md（除非 Explore/Plan） |
| 带 `skills` 字段的 Subagent | Subagent 的 markdown 正文 | Claude 的委派消息 | 预加载的 skills + CLAUDE.md |

`agent` 字段可选值：内置代理（`Explore`、`Plan`、`general-purpose`）或 `.claude/agents/` 中的自定义 subagent。省略则使用 `general-purpose`。

**注意**：`context: fork` 仅对具有明确任务说明的 skills 有意义。如果 skill 仅包含指南而没有任务，subagent 会收到指南但没有可操作的提示，返回无有意义的输出。

## 限制 Claude 的 Skill 访问

### 禁用所有 skills

在 `/permissions` 的 deny 规则中添加 `Skill`。

### 允许/拒绝特定 skills

```text
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

权限语法：`Skill(name)` 精确匹配，`Skill(name *)` 前缀匹配。

### 隐藏单个 skills

在 frontmatter 中添加 `disable-model-invocation: true`，从 Claude 的上下文中完全删除该 skill。

## 共享与分发

| 分发方式 | 做法 |
|---------|------|
| 项目 skills | 将 `.claude/skills/` 提交到版本控制 |
| 插件 | 在插件中创建 `skills/` 目录 |
| 托管 | 通过托管设置部署组织范围内 |

### 生成视觉输出

Skills 可以捆绑并运行脚本，为 Claude 提供单个提示中不可能的功能。一个强大模式是生成交互式 HTML 文件。

```yaml
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase.
allowed-tools: Bash(python3 *)
---

# Codebase Visualizer

Run the visualization script from your project root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```
```

`${CLAUDE_SKILL_DIR}` 确保无论 skill 安装在哪个级别，脚本路径都能正确解析。此模式适用于任何视觉输出：依赖关系图、测试覆盖率报告、API 文档等。

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| Skill 未触发 | 检查 description 是否包含用户会自然说的关键字；验证 `/skill-name` 可手动调用 |
| 触发过于频繁 | 使 description 更具体；添加 `disable-model-invocation: true` |
| 描述被截断 | 扩大 `skillListingBudgetFraction`；在 `skillOverrides` 中降低低优先级条目 |
