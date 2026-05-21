---
title: "Claude Code Agent Teams"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["06-claude-code-agent-teams"]
tags: [claude-code, agent-teams, task-queue, parallel-work]
---

# 摘要

## 核心架构

Team Lead 协调 + Teammates 独立工作 + 共享任务队列 + 直接互相通讯。

- 一个 session 作为 **team lead**，协调工作、分配任务、综合结果
- Teammates 独立工作，每个有自己的 context window
- Teammates 可以**直接互相通讯**，不经过 lead
- 共享任务列表，teammates 可以 claim work

## Agent Teams vs Subagents

| 特性 | Agent Teams | Subagents |
|------|-------------|-----------|
| 通讯方式 | Teammates 直接互相通讯 | 只回报给主 agent |
| 任务协调 | 共享任务列表，claim work | 主 agent 分发 |
| 独立性 | Teammates 可独立交互 | 依赖主 agent |

详见 [[concepts/Claude-Code-Subagent/index|Claude Code Subagent]]。

## 最佳场景

- **研究与审查**：多 teammates 同时调查不同方向，共享和挑战彼此的发现
- **新模块或功能**：每个 teammate 独立拥有不同部分
- **调试竞争假设**：Teammates 并行测试不同理论，更快收敛
- **跨层协调**：涉及前端、后端和测试的变更

## 限制

- Session 恢复、任务协调、关闭行为的已知限制
- 需要 Claude Code v2.1.32+
- 实验性功能，默认禁用

## Token 消耗

显著高于单 session — agents teams 增加了协调开销
