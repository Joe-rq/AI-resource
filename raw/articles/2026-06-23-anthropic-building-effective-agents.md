---
title: "Building Effective Agents \\ Anthropic"
source: "url"
source_file: "https://www.anthropic.com/research/building-effective-agents"
created: "2026-06-23T00:00:00Z"
source_url: "https://www.anthropic.com/research/building-effective-agents"
extract_method: "anysearch-extract"
---

# Building effective agents

Published Dec 19, 2024. Anthropic 工程团队基于与数十个行业团队合作的经验，总结 LLM agent 的生产实践。

## 核心论点

> "Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

## 关键二分：Workflow vs Agent

- **Workflows** — LLMs and tools are orchestrated through **predefined code paths**（LLM 在预定义代码路径中被编排）
- **Agents** — LLMs **dynamically direct their own processes** and tool usage, maintaining control over how they accomplish tasks（LLM 动态主导自身流程与工具使用）

> "When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale."

## When (and when not) to use agents

- 找最简单的解，需要时再加复杂度，"this might mean not building agentic systems at all"
- Agentic systems 用延迟和成本换任务性能
- "optimizing single LLM calls with retrieval and in-context examples is usually enough"

## When and how to use frameworks

框架（Claude Agent SDK、Strands、Rivet、Vellum）简化低层任务，但：
- "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug"
- "tempting to add complexity when a simpler setup would suffice"
- 建议"start by using LLM APIs directly"；若用框架必须理解底层代码

## 五种 Workflow 模式 + Agent

1. **Prompt chaining** — 任务分解为顺序步骤，中间可加 programmatic gate
2. **Routing** — 分类输入，导向专门处理
3. **Parallelization** — Sectioning（独立子任务并行）/ Voting（同任务多次取多样输出）
4. **Orchestrator-workers** — 中央 LLM 动态分解任务、委派 worker、汇总（subtask 非预定义）
5. **Evaluator-optimizer** — 一个 LLM 生成，另一个评估反馈循环
6. **Agents** — LLM 基于环境反馈在循环中使用工具；"typically just LLMs using tools based on environmental feedback in a loop"

## Agent 的风险

> "higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails."

## 与 12-factor-agents 的术语张力

12-factor 的核心论点"好 agent = 大部分确定性代码 + LLM 撒在关键点"，在 Anthropic 体系里**精确对应 workflow，不是 agent**。Anthropic 的 agent 是 LLM 动态主导、风险更高的那类。Anthropic 认同 12-factor 的"反框架、自拥控制流"（直接用 API、理解底层），但不会把"确定性代码为主"称作 agent 的常态。
