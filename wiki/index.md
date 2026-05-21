# Index — AI Resource Wiki

> Agent 平台与基础设施层研究资料库。涵盖 Runtime、Multi-agent 架构、行业实践。

## Navigation
- [[#Concepts]] · [[#Entities]] · [[#Summaries]] · [[#Open Questions]]

## Concepts

### Multi-Agent Architecture
- [[concepts/Multi-Agent-协作模式]] — 三种核心协作模式：Orchestrator/Specialist、Worker/Verifier、Team Engine
- [[concepts/Worker-Verifier-对抗循环]] — Worker/Verifier 对抗循环是 Mavis 的核心架构机制
- [[concepts/Agent-Runtime]] — 单 Agent 执行环境，包含 Prompt/工具定义/上下文管理/错误处理
- [[concepts/Agent-Secure-Runtime]] — Agent 安全运行时：三层安全检查（Policy/Network/Privacy）+ 沙箱隔离

### Claude Code
- [[concepts/Claude-Code-Subagent/index|Claude Code Subagent]] — Subagent：独立上下文工作者，内置类型、自定义定义、Fork 模式、持久内存、Hooks
- [[concepts/Claude-Code-Skills/index|Claude Code Skills]] — Skills 扩展机制：SKILL.md 定义、动态上下文注入、Subagent 中运行、调用控制

## Entities
- [[entities/MiniMax-Mavis]] — MiniMax 的 Agent 产品，MiniMax as a Jarvis
- [[entities/NVIDIA-Agent-Toolkit]] — NVIDIA Agent 开发工具包，含 OpenShell 安全运行时

## Summaries (chronological)
- 2026-05-21 — [[summaries/09-claude-subagent-tutorial]] — Claude Code Subagent 小白入门教程（内置类型、自定义定义、调用方式）
- 2026-05-19 — [[summaries/nvidia-agent-toolkit]] — NVIDIA Agent Toolkit 架构图（OpenShell 安全运行时 + 全栈 Agent 平台）
- 2026-05-19 — [[summaries/08-agent-runtime-battlefield]] — Agent Runtime 主战场（4.8pp ≈ 一次模型版本迭代）
- 2026-05-19 — [[summaries/01-minimax-single-ai-not-enough]] — 单 AI 的四个结构性缺陷
- 2026-05-19 — [[summaries/04-anthropic-multi-agent-research-system]] — Anthropic Orchestrator-Worker 架构
- 2026-05-19 — [[summaries/05-anthropic-managed-agents-api]] — Anthropic 共享容器 + Session Thread 隔离
- 2026-05-19 — [[summaries/06-claude-code-agent-teams]] — Claude Code Team Lead + Teammates 独立工作
- 2026-05-19 — [[summaries/01-building-skill-for-claude]] — Claude Code Skill 开发流程
- 2026-05-19 — [[summaries/02-minimax-agent-team-tech-report]] — Mavis 详细技术报告
- 2026-05-19 — [[summaries/01-building-skill-for-claude-zh]] — Skill 开发指南（中文）
- 2026-05-19 — [[summaries/readme]] — AI Resource 项目介绍
