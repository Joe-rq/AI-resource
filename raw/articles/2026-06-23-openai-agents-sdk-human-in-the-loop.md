---
title: "Human-in-the-loop \\ OpenAI Agents SDK"
source: "url"
source_file: "https://openai.github.io/openai-agents-js/guides/human-in-the-loop/"
created: "2026-06-23T00:00:00Z"
source_url: "https://openai.github.io/openai-agents-js/guides/human-in-the-loop/"
extract_method: "anysearch-extract"
---

# Human-in-the-loop (OpenAI Agents SDK)

OpenAI Agents SDK 官方文档，描述 approval-based HITL 流程。

## 核心机制

> "When a tool call requires approval, the SDK pauses the run, returns `interruptions`, and lets you resume later from the same `RunState`."

工具通过 `needsApproval: true` 或返回 boolean 的 async 函数声明需要审批。审批面是 **run-wide**，不限于当前 top-level agent——通过 handoff 到达的 agent、嵌套 `agent.asTool()` 执行中的工具，都在外层 run 的 `interruptions` 上浮现。

## Approval Flow（关键：selection 与 invocation 之间）

1. tool invocation 即将执行时，SDK 评估 approval rule
2. 若需审批且无已存决策 → **tool call 不执行**，run 记录 `RunToolApprovalItem`
3. turn 结束时 run 暂停，返回所有 pending approvals 到 `result.interruptions`
4. `result.state.approve(interruption)` 或 `.reject(interruption)`；可传 `{ alwaysApprove: true }` 使 sticky
5. `runner.run(agent, state)` 用更新后的 state 续跑，从打断点继续

## RunState 的可序列化性（支撑 stateless reducer）

- `RunState` 可 `toString()` / `fromString()`，跨进程续跑
- Sticky decisions 存在 run state 里，序列化后续跑仍保留
- streaming 与 session 模式下同一 interruption flow 通用

## 程序化审批（非暂停）

`shellTool` / `applyPatchTool` 的 `onApproval`、hosted MCP 的 `requireApproval + onApproval` 可在代码内即时决策，run 不暂停。

## 与 12-factor 的对应

这是 12-factor **Factor 7（contact humans with tools）+ Factor 8（own your control flow，在 tool selection 与 invocation 之间打断）** 的工业级一等公民实现。`RunState` 序列化即 Factor 6（launch/pause/resume）+ Factor 12（stateless reducer）的实例。
