---
title: "Architecting efficient context-aware multi-agent framework for production \\ Google"
source: "url"
source_file: "https://share.google/RoIcmUZTg8xckPhuW"
created: "2026-06-24T00:00:00Z"
source_url: "https://cloud.google.com/blog/products/ai-machine-learning/adk-context-engineering"
extract_method: "anysearch-extract"
author: "Hangfei Lin"
affiliation: "Google (Tech Lead, Agent Development Kit)"
published: "2025-12-04"
---

# Architecting efficient context-aware multi-agent framework for production

Google 第一方 context engineering 文章。基于 Google Agent Development Kit (ADK) 的 context stack 设计，提出 "context as a compiled view" 论点。

## 核心论点：Context is a compiled view

> "Context is a compiled view over a richer stateful system."

对比上一代 agent 框架（context = mutable string buffer），ADK 的论点：
- **Sessions / memory / artifacts** = sources（完整结构化状态）
- **Flows / processors** = compiler pipeline（变换状态的有序 passes）
- **Working context** = compiled view（这次调用 ship 给 LLM 的）

→ context engineering 从 "prompt gymnastics" 变成 "systems engineering"。问系统问题：中间表示是什么？在哪压缩？如何让变换可观测？

## 三设计原则

1. **Separate storage from presentation** — durable state（Sessions）vs per-call views（working context），存储 schema 与 prompt format 独立演化
2. **Explicit transformations** — context 由命名、有序的 processors 构建，非 ad-hoc 字符串拼接；compilation 步骤可观测、可测试
3. **Scope by default** — 每次模型调用/子 agent 只看所需最小 context；agent 必须通过 tool 显式 reach 更多信息，而非默认被淹没

## 三支柱：Structure / Relevance / Multi-agent context

### Structure: 四层 tiered model

| 层 | 角色 |
|---|---|
| **Working context** | 这次模型调用的即时 prompt：system instructions、agent identity、selected history、tool outputs、可选 memory results、artifacts 引用 |
| **Session** | 交互的 durable log：每条 user message、agent reply、tool call、tool result、control signal、error，结构化 Event 对象 |
| **Memory** | 长寿命、可搜索知识，跨 session 存活：user preferences、过往对话 |
| **Artifacts** | 大二进制/文本（文件/日志/图像），按名+版本寻址，不塞进 prompt |

### Working context as recomputed view

每次调用从底层 state 重建 working context。ephemeral（调用后丢弃）、configurable（改格式无需迁移存储）、model-agnostic。

### Flows and processors: context as pipeline

LLM Flow 维护有序 processor 列表（request_processors + response_processors），如 basic / auth / instructions / identity / contents / context_cache / planning / code_execution / output_schema。

## 为何 naive "append everything" 崩溃

三重压力：
1. **Cost and latency spirals** — 成本与 time-to-first-token 随 context 尺寸飙升
2. **Signal degradation（lost in the middle）** — 无关日志/陈旧 tool output/废弃 state 分散注意力
3. **Physical limits** — 真实负载（全 RAG 结果、中间产物、长对话 trace）最终溢出最大窗口

> "Throwing more tokens at the problem buys time, but doesn't change the shape of the curve. To scale, we need to change **how context is represented and managed**, not just how much we cram in."

## 与 Context Engineering / wiki 的印证

| Google ADK 概念 | wiki 对应 |
|---|---|
| Session as durable log | [[Stateless Reducer]] 的 durable log / [[ESAA]] event sourcing |
| Working context as compiled view | 比四策略更深的架构层——四策略（write/select/compress/isolate）是操作，compiler thesis 是系统 |
| Artifacts by name+version | Context Engineering 的 Write 策略（存外部） |
| Scope by default | Isolate 策略 + [[Claude Code Subagent]] |
| Flows/processors pipeline | [[12-Factor Agents]] Factor 8 own control flow 的形式化 |

Google 给 LangChain 四策略一个**系统级地基**：四策略是编译 pipeline 里的具体 pass，compiled-view thesis 是它们之上的一层抽象。
