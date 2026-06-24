---
title: "Context Engineering for Agents \\ LangChain"
source: "url"
source_file: "https://www.langchain.com/blog/context-engineering-for-agents"
created: "2026-06-24T00:00:00Z"
source_url: "https://www.langchain.com/blog/context-engineering-for-agents"
extract_method: "anysearch-extract"
author: "LangChain Team"
---

# Context Engineering for Agents

LangChain, 2025-07-02。context engineering 四策略（write/select/compress/isolate）的一手来源。

## 核心定义

> "Context engineering is the art and science of filling the context window with just the right information at each step of an agent's trajectory." —— Karpathy

LLM 像新型操作系统：LLM = CPU，context window = RAM（工作记忆）。context engineering 扮演 OS 管理 RAM 的角色。

## Context 类型

context engineering 作为 umbrella，跨三类 context：
- **Instructions** — prompts、memories、few-shot examples、tool descriptions
- **Knowledge** — facts、memories
- **Tools** — feedback from tool calls

## 为何长程 agent 需要 context engineering

agent 交错 LLM 调用与 tool 调用，长程任务 + tool feedback 累积 → 大量 token → 超 context window / 成本延迟膨胀 / 性能退化。

### Drew Breunist 的四种 context 失败模式

- **Context Poisoning** — 幻觉混入 context
- **Context Distraction** — context 压过训练
- **Context Confusion** — 多余 context 影响响应
- **Context Clash** — context 各部分相互矛盾

## 四策略（核心贡献）

1. **Writing context** — 把信息**保存到 context window 之外**，帮助 agent 执行任务（持久化记忆/外部存储）
2. **Selecting context** — 把信息**拉进 context window**，帮助 agent 执行任务（RAG/适时检索）
3. **Compressing context** — 只保留执行任务所需的 token（摘要/tool result clearing）
4. **Isolating context** — 拆分 context（子 agent 用新窗口，避免主上下文污染）

## 行业背书

> "Context engineering … is effectively the #1 job of engineers building AI agents." —— Cognition

> "Agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies." —— Anthropic

## 与本 wiki 的关联

- 四策略对应 [[12-Factor Agents]] Factor 3（own your context window）的工程化
- Isolating = 子 agent 独立 context window（[[Claude Code Subagent]]）
- Compressing = Claude Code 95% 自动压缩、tool result clearing（维持 KV cache 命中率）
- 与 [[Harness Cybernetics]] 的 feedforward 侧交叉：context injection（注入 repo state/constraints）是 feedforward control
- context 四失败模式补充 [[Agent Reliability vs Capability]] 的 non-determinism 来源
