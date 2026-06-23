---
title: "Stateless Reducer Agent \\ Agent Patterns Catalog"
source: "url"
source_file: "https://www.agentpatternscatalog.org/patterns/stateless-reducer-agent/"
created: "2026-06-23T00:00:00Z"
source_url: "https://www.agentpatternscatalog.org/patterns/stateless-reducer-agent/"
extract_method: "anysearch-extract"
---

# Stateless Reducer Agent (Agent Patterns Catalog)

agentpatternscatalog.org 模式目录条目，将 12-factor 的 Factor 12 形式化为独立可复用模式。

## Context

团队构建 agent，默认把状态放在进程内存（Python 对象、内存 dict）。暂停、恢复、重放都需要 custom checkpointing 逻辑，且不可避免地不完整。

## Problem

> "In-memory agent state cannot be paused, resumed across processes, or time-travelled. Each capability requires bespoke checkpointing that misses edge cases. Differs from durable-workflow-snapshot (which is a snapshot mechanism) by being a programming-model constraint — the agent is *designed* as a reducer, not made into one after the fact."

关键区分：这不是事后加的 snapshot 机制，而是**编程模型约束**——agent 从一开始就设计成 reducer。

## Forces

- Stateless-reducer discipline 约束 agent 代码结构
- 外部 event log 增加基础设施依赖
- 某些操作天然有状态（cache、connection），需单独处理

## Solution

> "The agent's core is a pure function: takes (current state, next event) → (new state, side-effect descriptors). Side effects are descriptors, not executions — the runtime dispatches them. All events are appended to a durable log."

- **Pause** = stop dispatching
- **Resume** = restart dispatching from current log position
- **Replay** = re-run reducer against earlier log slice
- **Time-travel** = re-run against any log slice

**此模式禁止的**：所有 agent 状态变更绕过 reducer；进程内存里有 hidden state；任何事件不持久化到 durable log。

## 互补/对立模式

- 互补 **Durable Workflow Snapshot** — snapshot 机制
- 互补 **Event-Driven Agent** — webhook/MQ/文件变化触发
- 互补 **Deterministic Control Flow, Not Prompt** — 分支决策在确定性代码里，LLM 在战略点产出结构化信号供代码分支
- 互补 **Own Your Prompts (12-Factor Agents)** — prompt 版本化、测试、自拥
- 反模式 **Hidden State Coupling** — 读写未声明共享状态（cache、env var、process global）
- 反模式 **Orchestrator as Bottleneck** — 单进程 orchestrator 成系统并发上限

## Used in frameworks

- **Temporal** — durable event-sourced workflow + stateless workers，workflow 靠 replay 重建
- **Burr** — 应用建模为状态机，action 为纯 `(state)->(new state)`，state 完全 immutable

## References

- humanlayer/12-factor-agents (Factor 12)
