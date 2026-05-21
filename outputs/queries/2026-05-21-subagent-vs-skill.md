---
title: "Subagent 和 Skill 的区别是什么？"
type: query
created: 2026-05-21
sources: [[Claude-Code-Subagent]], [[summaries/01-building-skill-for-claude]], [[summaries/09-claude-subagent-tutorial]]
tags: [claude-code, subagent, skill, comparison]
---

# Subagent 和 Skill 的区别是什么？

根据 wiki 中的资料，Subagent 和 Skill 是 Claude Code 中两种不同的机制，它们的核心区别在于**本质**和**运行位置**。

## 核心定义

- **Skill**：是一组打包的指令（文件夹形式），教 Claude 如何处理特定任务或工作流。它解决的问题是避免在每次对话中重复解释偏好、流程和领域专业知识 [[summaries/01-building-skill-for-claude]]。
- **Subagent**：是 Claude Code 中的独立上下文工作者，跑在自己专属的上下文窗口里，完成任务后只把结论汇报回主对话。主对话（项目经理）负责全局决策；Subagent（工程师）负责具体执行 [[Claude-Code-Subagent]]。

## 关键区别

| 维度 | Skill | Subagent |
|------|-------|----------|
| **本质** | 可复用的指令包 | 独立上下文的工作者 |
| **跑在哪** | 主对话上下文内 | 自己独立的上下文窗口 |
| **什么时候用** | 复用一套流程 | 隔离上下文、并行、限权 |

## 使用场景对比

- **Skill 适用场景**：生成遵循规范的前端设计、用一致方法论进行研究、创建遵循团队风格指南的文档、编排多步骤流程、MCP 集成增强 [[summaries/01-building-skill-for-claude]]。
- **Subagent 适用场景**：跑测试/处理日志（避免主对话被大量输出淹没）、并行研究多个模块、链式工作流（前一个的输出当作后一个的输入） [[Claude-Code-Subagent]]。

## 核心差异点

1.  **上下文隔离**：Skill 在主对话上下文中执行，其处理过程中的细节（如读取的文件、产生的日志）会留在主对话中。而 Subagent 在独立的上下文窗口中执行，只将精炼后的结论汇报回主对话，从而保护主对话上下文不被污染 [[Claude-Code-Subagent]]。
2.  **并行能力**：多个 Subagent 可以同时研究不同模块，互不干扰。Skill 则通常按顺序在主对话中执行。
3.  **权限控制**：Subagent 可以通过 `tools` 字段限制其能力范围（例如只读任务不给写权限），构成安全围栏。Skill 本身不提供这种细粒度的权限控制 [[Claude-Code-Subagent]]。
4.  **定义方式**：Skill 是一个包含 `SKILL.md` 文件的文件夹。Subagent 是一个带 YAML 头部的 Markdown 文件，放在 `.claude/agents/` 目录下 [[Claude-Code-Subagent]] [[summaries/01-building-skill-for-claude]]。

## 总结口诀

**要隔离用 Subagent，要复用用 Skill。** [[Claude-Code-Subagent]] [[summaries/09-claude-subagent-tutorial]]