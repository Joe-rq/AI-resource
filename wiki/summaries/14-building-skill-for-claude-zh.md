---
title: "构建 Claude 技能完整指南（中文）"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["raw/articles/2026-05-18-building-skill-for-claude-zh.md"]
tags: [claude-code, skill, skill-md, guide-zh]
---

# 摘要

## 核心概念

Skill 是一组打包的指令（文件夹形式），教 Claude 如何处理特定任务或工作流。

## 适用场景

- 根据规格生成前端设计
- 用一致方法论进行研究
- 创建符合团队风格指南的文档
- 编排多步骤流程
- MCP 集成增强

## 两种路径

1. **构建独立技能** — 重点关注"基础"、"规划与设计"
2. **增强 MCP 集成** — "技能 + MCP"部分

## Skill 结构

```
skill-name/
├── SKILL.md          ← 核心文件
├── references/       ← 参考文档
├── scripts/          ← 可执行脚本
└── (其他资源)
```

## 关键要素（SKILL.md）

1. **name** — Skill 标识符
2. **description** — 何时使用此 skill（触发条件）
3. **Commands/Instructions** — 具体工作流程

## 预期时间

使用 skillcreator 构建并测试第一个可用技能约 **15-30 分钟**。