---
title: "Agent Runtime"
type: concept
created: 2026-05-19
updated: 2026-05-19
sources: ["08-agent-runtime-battlefield-20260516"]
tags: [agent-runtime, harness, prompt, tool-definition]
---

# Agent Runtime

## 定义

**Runtime** = 单 Agent 的执行环境，是比模型层高一级、比应用层低一级的整个执行平台面。

包含四个组件：
- **Prompt 设计** — system prompt 定义模型角色和行为
- **工具定义** — 参数描述、返回值格式、调用时机
- **上下文管理** — 何时压缩、删什么保什么
- **错误处理** — 错误消息质量决定模型能否自我修正

## 性能差异

同一模型在不同 runtime 上可以差出 **10 个百分点**（Cline 实验数据）。

| 发现 | 数据 |
|------|------|
| Cline vs Claude Code (同一模型 opus-4.7) | 74.2% vs 69.4% |
| Cline hill climbing (opus-4.5) | 47% → 57%，+10pp 全部来自 runtime |
| LangChain harness profile | 10-20pp 差异 |

## 四个设计决策

### 1. Prompt 设计

Cline 重写了 system prompt — 不是措辞调整，而是重新定义了模型如何理解自己的角色、如何使用工具、如何判断任务完成。

迭代方式：每次改一个变量然后跑完整 benchmark，用分数而非直觉来判断 prompt 的有效性。

### 2. 工具定义

工具定义的详细程度、参数描述方式、返回值格式直接影响模型调用工具的正确率。

Cline 把 provider 逻辑隔离在 `@cline/llms` 层，agent loop 本身不感知模型差异。

### 3. 上下文管理

什么时候 compact、按什么顺序删除、哪些信息值得保留 — 这些决策直接影响任务后期的表现。

**反直觉设计**：为了维持 cache 的 prefix 稳定性，compaction 时应该优先删除尾部的最新内容而非头部的旧内容。因为 prefix 稳定性决定 cache 命中率。

### 4. 错误处理

好的错误消息不只是说"出错了"，而是告诉模型：
- 具体错在哪
- 当前状态是什么
- 有哪些可选路径

## 25/75 法则

- **25%** 的失败是模型能力天花板，换什么 harness 都救不了
- **75%** 可以通过 prompt 调整、工具定义优化、错误处理改进来修复

## 行业重心转移

行业正在从"**写 prompt**"转向"**维护控制面**"。

> "Harness 不是万能的 — 如果你的模型选错了（用 haiku 跑复杂重构），harness 再强也救不回来。但它也不是可有可无的 — 75% 的失败都可以在 runtime 层修复。"