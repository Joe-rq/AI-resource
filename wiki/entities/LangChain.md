---
title: "LangChain"
type: entity
created: 2026-06-15
updated: 2026-06-15
sources: []
tags: [agent-framework, langchain, benchmark, open-source, orchestration]
---

# LangChain

## Overview

**LangChain** 是开源 LLM 应用开发框架，提供 chain-based composition 和 tool integration 的标准范式。其生态包含两个核心组件：

- **LangChain** — 链式组合（chain-based composition），将 LLM 调用、工具、记忆等组件串联为可复用的 pipeline。
- **LangGraph** — 基于有向图的 agent 编排框架，支持条件分支、循环和状态管理，适合构建复杂的 multi-step agent 工作流。

## 在 Wiki 中的位置

LangChain 在本 wiki 中目前作为 **benchmark 数据点** 出现：[[Agent Runtime]] 的性能差异表中引用了一项实验数据 —— 同一模型在 LangChain harness profile 上可产生 **10-20 个百分点**的性能差异。这佐证了 runtime/harness 设计对 agent 性能的决定性影响，而非仅取决于底层模型能力。

## Deep Agents

LangChain 发布了 **Deep Agents** 基准测试，用于评估 multi-agent 系统在复杂任务上的表现。该基准目前列在项目 [[CLAUDE.md]] 的 Research Gaps 中，标注为"待收录"（Sources to ingest）。Deep Agents 的具体方法论、评估维度和结果数据尚未在本 wiki 中展开分析。

## 架构特点

LangChain 的架构围绕以下设计决策：

- **Chain-based composition**：通过 `|` 管道操作符和 LCEL（LangChain Expression Language）组合 prompt、model、parser 等组件，形成声明式调用链。
- **Tool integration**：内置丰富的工具集成（搜索、代码执行、API 调用），通过标准化的 tool schema 接入 LLM 的 function calling 能力。
- **Model-agnostic**：抽象层屏蔽不同 LLM provider 的差异，支持切换底层模型而无需修改 chain 逻辑。
- **Memory management**：提供多种记忆后端（buffer、summary、vector store），管理跨轮次对话状态。

## Related Concepts

- [[Agent Runtime]] — LangChain harness profile 的性能差异数据支撑了 runtime 设计的重要性论述
- [[Thin Harness Fat Skills]] — LangChain 的 chain 抽象与"瘦套具、胖技能"哲学存在架构张力
- [[Agent Harness 治理协议]] — LangChain 作为 harness 实现之一，其设计取舍可与 wow-harness v3 的事件溯源范式对照

## Sources

> **注意**：LangChain 的原始文档、Deep Agents 基准测试报告等一手资料尚未收录进本 wiki。当前页面内容基于 [[Agent Runtime]] 中的引用数据点和对 LangChain 公开架构的概述性了解。完整收录后需更新 `sources` 字段并扩充 Deep Agents 相关内容。
