---
title: "Claude Code Skill 开发"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["01-building-skill-for-claude"]
tags: [claude-code, skill, skill-md, workflow]
---

# 摘要

## 什么是 Skill

Skill 是一组打包的指令，教 Claude 如何处理特定任务或工作流程。

解决的问题：
- 不需要在每次对话中重新解释你的偏好、流程和领域专业知识
- 适用于**可重复的工作流程**：从规格生成前端设计、一致性方法论研究、创建遵循团队风格指南的文档

## Skill 结构

```
skill-name/
├── SKILL.md          ← 核心：描述 skill 用途和何时使用
├── references/       ← 参考文档
├── scripts/          ← 可执行脚本
└── (其他资源)
```

## SKILL.md 关键要素

1. **name** — Skill 标识符
2. **description** — 何时使用此 skill（触发条件）
3. **Commands/Instructions** — 具体工作流程

## Skills 的适用场景

- 生成遵循规范的前端设计
- 用一致方法论进行研究
- 创建遵循团队风格指南的文档
- 编排多步骤流程
- MCP 集成增强

## Skills + MCP

MCP（Model Context Protocol）集成 + Skills = 将原始工具访问转变为可靠、优化的工作流程。