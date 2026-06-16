---
title: Agent Memory
type: concept
created: 2026-05-22
updated: 2026-06-15
sources:
  - raw/articles/2026-05-02-hermes-agent-nous-research.md
  - raw/articles/2026-05-17-nanoclaws-second-brain.md
tags:
  - agent-memory
  - long-term-memory
  - knowledge-graph
  - agent-runtime
---

# Agent Memory

Agent Memory 是指 AI Agent 在多轮对话和跨会话场景中保持上下文连续性的能力。区别于传统 LLM 的无状态特性，具备记忆能力的 Agent 能累积经验、保留偏好、跨时间线追踪任务状态。

## 为什么需要 Agent Memory

当前大多数 LLM 应用本质是无状态的——每次请求独立，模型不保留会话间的任何信息。Agent Memory 试图解决这个问题，让 AI 能够像人类一样积累和使用经验。在 Multi-Agent 协作场景中，记忆更是跨 Agent 信息传递的关键基础设施。

## 子页面

- [[Agent Memory Architecture|Architecture]] — 记忆系统的技术架构：向量检索、知识图谱、混合模式、更新循环
- [[Forgetting & Compaction]] — 遗忘机制与压缩策略：为什么需要遗忘、当前方法、开放问题
- [[Self-Evolving Memory]] — 自我进化型记忆：Hermes 与 NanoClaw 的实现路径对比

## 核心属性

| 属性 | 说明 |
|------|------|
| **持久性** | 跨会话保留，不随模型调用结束而消失 |
| **可查询** | 语义搜索 + 结构化推理 |
| **可演化** | 随使用累积，自动提炼高价值信息 |
| **隐私边界** | 本地部署 vs 云端存储的权衡 |

## 与其他概念的关系

- [[Agent Runtime]] — Memory 是 Runtime 的关键能力缺口，Hermes 和 NanoClaw 都把记忆作为核心卖点
- [[NanoClaw]] — Mnemon 图谱记忆 + Ollama 嵌入的本地实现
- [[Nous Research]] — Hermes 的自我进化是记忆演化的极端形式
- [[Multi-Agent 协作模式]] — 跨 Agent 信息传递依赖共享记忆基础设施

## Sources

- [[Hermes Agent：Nous Research 的开源 Agent 框架]] — Hermes 自我进化型记忆系统
- [[新加坡外长的 AI 第二大脑]] — Mnemon 图谱记忆 + 边缘部署案例
