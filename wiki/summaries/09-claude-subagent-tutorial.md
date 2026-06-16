---
title: "09-Claude Subagent 小白入门教程"
type: summary
created: 2026-05-21
updated: 2026-05-21
sources: ["raw/articles/2026-05-21-claude-subagent-tutorial-zh.md"]
tags: [claude-code, subagent, agent-definition, context-isolation]
---

# 摘要

## 核心观点

Subagent 是 Claude Code 中跑在独立上下文窗口里的任务执行单元。主对话是项目经理，Subagent 是被派去做具体活的工程师——独立工作，只把结论汇报回来。

## Subagent 的三个价值

1. **保护主对话上下文** — Subagent 在自己那边处理大量文件，主对话只接收精炼结论
2. **并行执行** — 多个 Subagent 同时研究不同模块，互不干扰
3. **权限隔离** — 通过 `tools` 字段限制 Subagent 只能读不能写，构成安全围栏

## 三个内置 Subagent

- **Explore** — 只读搜索专家，默认跑在 Haiku 上（便宜、快），处理"读大量文件但不写"的任务
- **Plan** — 只规划不动手的架构方案生成器，审过再执行
- **General-purpose** — 什么都能干的兜底款

## 自定义 Agent 定义

一个带 YAML 头部的 Markdown 文件，放在 `.claude/agents/`（项目级）或 `~/.claude/agents/`（全局）。

关键字段：
- `description` — 最关键，决定 Claude 何时自动委托，必须包含触发条件
- `tools` — 权限闸门，只读任务只给 Read/Grep/Glob
- `model` — 按需分级，探索用 Haiku，深度审查用 Sonnet/Opus

## 调用方式

| 方式 | 保险程度 | 场景 |
|------|---------|------|
| 自然语言描述 | 不保险，Claude 可能选错 | 日常使用 |
| `@agent-name` 提及 | 一定会用 | 确保调用特定 agent |
| `claude --agent name` CLI | 整个会话绑定 | 只做一件事的场景 |

## Skill vs Subagent

| 维度 | Skill | Subagent |
|------|-------|----------|
| 本质 | 可复用的指令包 | 独立上下文的工作者 |
| 跑在哪 | 主对话上下文内 | 自己独立的上下文窗口 |
| 用途 | 复用流程 | 隔离上下文、并行、限权 |

记忆口诀：要隔离用 Subagent，要复用用 Skill。

## Agent Memory

Subagent 可以积累项目记忆——把发现的模式、踩过的坑、架构约定记下来，下次调用时已经"认识"项目。

## 常见错误

- `description` 写得太抽象（如"general purpose helper"），Claude 不知道何时调用
- 试图让 Subagent 再派 Subagent（不支持递归）

## 相关概念

- [[Claude Code Subagent]] — Subagent 概念总览与配置参考
- [[Claude Code Skills]] — Skill 与 Subagent 互补：要隔离用 Subagent，要复用用 Skill
