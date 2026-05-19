---
title: "Anthropic Managed Agents API"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["05-anthropic-managed-agents-api"]
tags: [multi-agent, session-thread, anthropic, managed-agents]
---

# 摘要

## 核心架构

**共享容器 + Session Thread 隔离**的执行模型。

- 所有 agents 共享同一个容器和文件系统
- 每个 agent 运行在自己的 **session thread** 中（context-isolated event stream）
- Coordinator 在 **primary thread** 报告活动
- Threads 是持久化的 — coordinator 可以发送 follow-up 给之前调用过的 agent

## Session Thread 模型

| 特性 | 说明 |
|------|------|
| Context isolation | 每个 agent 有独立对话历史 |
| 持久化 | Agent 保留之前所有 turns 的上下文 |
| 工具隔离 | 每个 agent 用自己的配置（model、system prompt、tools、MCP servers） |
| 非共享 | Tools 和 context 不共享 |

## 适用场景

- **并行化**：分发独立 subtasks，同时搜索多个来源或分析不同文件
- **专业化**：路由到有领域专注 system prompt 和 tools 的 agents
- **升级**：咨询更强能力的 agent/model 处理复杂 subtask

## 模式对比

| 方案 | 特点 |
|------|------|
| Anthropic Managed Agents | 共享容器 + Session Thread 隔离，持久化上下文 |
| Anthropic Multi-Agent Research | Lead Agent + 并行 Subagent |
| Mavis | Worker/Verifier 对抗 + Team Engine |