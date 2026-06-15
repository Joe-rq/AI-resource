---
title: "MiniMax Mavis"
type: entity
created: 2026-05-19
updated: 2026-05-19
sources: ["raw/articles/2026-05-19-minimax-agent-team-tech-report.md"]
tags: [minimax, mavis, agent-team, worker-verifier]
---

# MiniMax Mavis

MiniMax 的 Agent 产品，名字含义：MiniMax as a Jarvis，你的 AI 管家。

## 核心功能

- **Agent Teams** — 多个 Agent 并行工作，组成团队协作完成任务
- **TokenPlan 和 Agent Plan 合并** — CLI、API、Agent 全打通

## 技术架构

Mavis 的核心是 **Worker/Verifier 对抗循环** + **Team Engine** 状态机调度。

- Worker 干活，Verifier 挑刺
- Team Engine 是确定性代码，不依赖 AI 实时状态
- 两个 AI 之间不直接通讯，全程靠程序中转

## 设计哲学

> "多 Agent 系统是 runtime，不是 prompt 编排"

意思是让多个 AI 一起干活，关键不是给它们写更好的指令，而是给它们搭一个能长期运行、能管理状态的底座。

## 与其他方案对比

| 方案 | 特点 |
|------|------|
| Mavis | Worker/Verifier 直接对抗，Team Engine 调度 |
| Anthropic | Lead Agent 评审 Subagent 结果 |
| OpenAI | 接力式 Handoff，每棒不回头 |