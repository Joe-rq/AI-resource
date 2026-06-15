---
title: "AI Resource 项目介绍"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["raw/articles/readme.md"]
tags: [project, overview, agent-platform]
---

# 摘要

## 项目性质

**AI 相关主题研究资料库**，以 Markdown 文档为主。

## 目录结构

| 主题 | 说明 | 文档数 |
|------|------|--------|
| `agent-platform/` | Agent 平台与基础设施：Runtime / Multi-agent / Harness / 工具定义 | 8 |
| `claude-code-skills/` | Claude Code Skill 开发 | 3 |

## 外部参考

- [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) — Anthropic 官方 Cookbook，`managed_agents/` 下有 10+ 个多 Agent 示例

## 当前研究方向

**Agent 平台与基础设施层** — 比模型层高一级、比应用层低一级的整个执行平台面。

核心问题：
- 单 AI 在长程任务上的结构性缺陷
- 多 AI 协作的架构模式（Runtime、Worker/Verifier 对抗循环、Orchestrator/Specialist、Team Engine）