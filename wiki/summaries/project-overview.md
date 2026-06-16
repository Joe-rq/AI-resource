---
title: AI Resource 项目介绍
type: summary
created: 2026-05-19
updated: 2026-06-16
sources: ["README.md"]
tags: [project, meta]
---

# AI Resource Wiki 项目介绍

## 项目性质

**AI Resource** 是一个 Agent 平台与基础设施层研究知识库，以 Markdown wiki 形式组织。覆盖范围：

- **Agent 平台与基础设施层** — Runtime / Multi-agent / Harness / 工具定义
- **Claude Code Skill 开发** — SKILL.md 规范、动态工作流、Subagent 架构
- **多 Agent 协作架构** — Orchestrator/Specialist、Worker/Verifier 对抗循环、Team Engine、自动扩张任务图
- **Agent 治理协议** — 事件溯源、概念演化、双层验证、跨 session 一致性
- **行业研究** — MiniMax、Anthropic、NVIDIA、OpenAI、Cline、LangChain 等公司的 Agent 平台实践

## 当前规模

| 类别 | 页面数 | 说明 |
|------|--------|------|
| Concepts | 19 | 概念页，含 3 个 folder-split 主题（Agent Memory、Claude Code Subagent、Claude Code Skills） |
| Entities | 12 | 公司与项目实体页 |
| Summaries | ~30 | 源文章深度解读 |

## 核心概念

- [[Agent Harness 治理协议]] — 跨 session 长期一致性治理框架
- [[Worker Verifier 对抗循环]] — Multi-agent 核心协作机制
- [[Thin Harness, Fat Skills]] — 架构原则：套具极薄、技能极胖
- [[Forward-Deployed-Engineering]] — FDE 前置部署工程与 Agent 平台的结构性类比

## 维护流程

本项目使用 llm-wiki skill 的五步操作流程：compile / ingest / query / lint / audit。每次操作记录在 `log/YYYYMMDD.md`。
