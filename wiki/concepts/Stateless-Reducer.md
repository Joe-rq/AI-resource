---
title: "Stateless Reducer"
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: ["raw/articles/2026-06-23-stateless-reducer-agent-pattern.md", "raw/articles/2026-06-23-openai-agents-sdk-human-in-the-loop.md", "raw/articles/2026-06-23-anthropic-building-effective-agents.md"]
tags: [reducer, stateless, event-sourcing, agent-architecture, determinism, pause-resume, replay, 12-factor-agents, openai-agents-sdk, temporal]
---

# Stateless Reducer（无状态归约器）

> **把 agent 设计成纯函数 `(state, event) → (new state, side-effect descriptors)`，所有状态进 durable log，LLM 成为管线里唯一的非确定节点。** —— 这是"确定性边界"命题的第五种范式：不是对付接缝，而是让接缝成为唯一的非确定源。

## 定义

agent 的核心是一个纯函数：

```text
reduce(current_state, next_event) → (new_state, side_effect_descriptors)
```

- **状态**全部表示为事件序列（durable log），不藏进程内存的可变变量
- **副作用**是描述符（descriptor），不是直接执行——runtime 负责派发
- **LLM 调用**是这个纯函数里唯一的非确定步骤，其余全是确定性折叠

来源：[Agent Patterns Catalog](https://www.agentpatternscatalog.org/patterns/stateless-reducer-agent/) 将其形式化为独立模式；[[12-Factor Agents]] Factor 12 最早提出；OpenAI Agents SDK 的 `RunState` 是工业实例。

## 与 snapshot 机制的关键区分

> "Differs from durable-workflow-snapshot (which is a snapshot mechanism) by being a programming-model constraint — the agent is *designed* as a reducer, not made into one after the fact."

不是事后加 checkpoint 救出来的可恢复性，而是**从一开始**就按 reducer 约束写代码。区别决定了可恢复性的完整度：事后 checkpoint 不可避免漏 edge case；reducer 设计天然完整。

## 四个能力都从同一机制派生

| 能力 | 实现 |
|---|---|
| **Pause** | 停止派发事件 |
| **Resume** | 从当前 log position 重启派发 |
| **Replay** | 对更早的 log slice 重跑 reducer |
| **Time-travel** | 对任意 log slice 重跑，精确重建该时刻状态 |

这四个能力是 [[12-Factor Agents]] Factor 6（launch/pause/resume）+ Factor 8（own control flow，在 tool selection↔invocation 间打断）的底层支撑。

## 工业实例：OpenAI Agents SDK `RunState`

OpenAI Agents SDK 的 HITL 流程是 reducer 的具体实现：

- `RunState` 可 `toString()` / `fromString()`，跨进程序列化续跑
- tool 需审批时 run 暂停，返回 `interruptions`，`RunState` 持久化
- `runner.run(agent, state)` 用更新后的 state 续跑，从打断点继续
- sticky decisions（`alwaysApprove`）存在 state 里，序列化后保留

→ tool selection 与 invocation 之间那一格的打断，靠的就是 state 可序列化 + reducer 可续跑。

## 此模式禁止什么

- 所有 agent 状态变更绕过 reducer
- 进程内存里有 hidden state（Python 对象、内存 dict）
- 任何事件不持久化到 durable log

违反任一条 → pause/resume/replay/time-travel 之一会漏 edge case。

## 为何是"第五种范式"

[[12-Factor Agents]] 归纳四种对付接缝的范式：压概率空间 / Verifier 循环 / 统计签收 / 确定性外移。这四种都是"怎么对付接缝的失败"。

reducer 是正交的另一维：**不是降低接缝失败率，而是让非确定性被隔离在一个可识别、可重放的唯一节点里**。状态全进 log → 可重放 → 可诊断 → 可续跑。它和四种范式叠加使用，不是替代。

## 与 Event Sourcing 的同构

reducer 的 durable log 就是 Event Sourcing 的 immutable event log：

- [[ESAA]] 把 agent 生命周期建模为 Event Sourcing，source of truth 是 intent 的 immutable log 而非当前快照
- [[Agent-Harness-治理协议]] 的事件时间线 + 双层验证是同一思想在治理层的应用
- Temporal 框架：durable event-sourced workflow + stateless workers，workflow 靠 replay 重建——reducer 的成熟工程实现
- Burr 框架：应用建模为状态机，action 为纯 `(state)->(new state)`，state 完全 immutable

## 反模式（必须避免）

| 反模式 | 为何破坏 reducer |
|---|---|
| **Hidden State Coupling** | 读写未声明共享状态（cache、env var、process global）→ replay 重建的状态与真实运行不一致 |
| **Orchestrator as Bottleneck** | 单进程 orchestrator 成系统并发上限 → stateless worker 的水平扩展被堵死 |
| **Blocking Sync Calls in Agent Loop** | 同步阻塞 I/O 在 agent loop 内 → 并发被 OS 线程数封顶，reducer 的可暂停性被破坏 |

## 与现有 wiki 概念的关系

| 关联 | 说明 |
|---|---|
| [[12-Factor Agents]] | Factor 5（unify state）+ Factor 12（stateless reducer）是本概念的原始表述 |
| [[ESAA]] | Event Sourcing 是 reducer 的 durable log 的学术形式化；两者同构 |
| [[Agent-Harness-治理协议]] | 事件时间线 + 双层验证 = reducer 在治理层的应用 |
| [[Agent-Reliability-vs-Capability]] | reducer 的可重放性是对冲 reliability decay 的工程手段——长任务靠外移 + 重放，不靠模型硬扛 |
| [[Worker Verifier 对抗循环]] | Verifier 是 reducer 里 side-effect 执行前的校验门 |
| [[Agentic-Code-Review]] | human-on-the-loop = reducer 在 selection↔invocation 接缝处插入的 side-effect descriptor（请求人审批） |

## 落地含义

- **状态全部事件化**：current step、retry count、waiting status 都从事件序列推导，不另存执行状态（[[12-Factor Agents]] Factor 5）
- **LLM 调用隔离**：让 `determine_next_step` 成为 reducer 里唯一非确定调用，其余确定性折叠可重放
- **可重放 = 可诊断**：[[Agent Macro Evaluation]] 的 trace 分析、[[Agent-Reliability-vs-Capability]] 的 reliability 诊断都依赖 reducer 的可重放性
- **慎用 hidden state**：cache、connection 等天然有状态的操作需单独处理，不能绕过 reducer
