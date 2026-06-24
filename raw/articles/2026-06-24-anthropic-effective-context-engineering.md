---
title: "Effective context engineering for AI agents \\ Anthropic"
source: "url"
source_file: "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
created: "2026-06-24T00:00:00Z"
source_url: "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
extract_method: "anysearch-extract"
author: "Anthropic Engineering"
published: "2025-09-29"
---

# Effective context engineering for AI agents

Anthropic 第一方 context engineering 文章。把 context engineering 定位为 prompt engineering 的自然演进。

## 定义

> "Context engineering is the natural progression of prompt engineering."

- **Prompt engineering** — 写好并组织 LLM 指令
- **Context engineering** — 在 LLM 推理时策展并维护最优 token 集（信息），包括 prompt 之外所有可能落入 context 的信息

> agent 在 loop 中运行，生成越来越多"可能相关"的数据，必须循环精炼。context engineering 是从不断演化的可能信息宇宙中策展进有限 context window 的艺术与科学。

## Context rot（context 腐烂）

> needle-in-a-haystack 研究揭示 **context rot**：context window token 数增加 → 模型从中准确 recall 信息的能力下降。所有模型都出现此特性。

attention budget：每个新 token 耗费一些预算。Transformer 每个token attend 每个其他 token → n² pairwise 关系，context 变长关系被拉伸变薄。训练数据短序列多于长序列 → 模型对长程依赖经验/参数更少。

→ **context 是有限资源，边际收益递减**。性能梯度而非硬悬崖。

## The anatomy of effective context

好 context engineering = 找**最小可能**的高信号 token 集，最大化期望结果概率。

- **System prompts** — right altitude（Goldilocks 区）：一端是脆弱的 if-else 硬编码逻辑，另一端是过度泛化、错误假设共享 context；中道是足够具体引导行为、又足够灵活给强启发
- **Tools** — token 高效 + 鼓励高效 agent 行为；自包含、健壮、用途极清晰；**bloated tool set**（覆盖太多/决策歧义）是常见失效——"若人类工程师都说不清该用哪个工具，agent 做不到更好"
- **Examples（few-shot）** — 策展多样、canonical 的例子，而非塞一堆 edge case 规则；例子是"值千言的图"

## Just-in-time context vs pre-inference retrieval

agent 范式从 embedding 预检索转向 "just-in-time"：
- 维护轻量标识符（file paths / stored queries / web links），运行时用 tool 动态加载
- **Claude Code** 实例：写 targeted query、存结果、用 head/tail 分析大库而不全载入 context
- 类比人类认知：不记忆整个语料，而是用文件系统/收件箱/书签按需检索

metadata 提供行为精炼信号（`test_utils.py` 在 `tests/` vs `src/core_logic/` 暗示不同用途）。

## Progressive disclosure

> agent 通过探索增量发现相关 context。每次交互产出 context 告知下一个决策：文件大小暗示复杂度；命名暗示用途；时间戳代理相关性。逐层组装理解，working memory 只保留必要部分。

self-managed context window 让 agent 聚焦相关子集而非淹没在详尽但不相关的信息里。

## Hybrid strategy（Claude Code）

- CLAUDE.md 预加载（up front，naive drop in）
- glob/grep just-in-time 导航检索
- 有效绕过 stale indexing 和复杂语法树问题

trade-off：运行时探索比预检索慢；需 thoughtful engineering 给 LLM 正确 tool + 启发式导航。决策边界依任务而定。

## 与 Context Engineering / wiki 的印证

| Anthropic 概念 | wiki 对应 |
|---|---|
| context rot | [[Agent Reliability vs Capability]] 的 reliability decay 微观机制；context 四失败模式（Distraction）的理论根 |
| just-in-time + 轻量标识符 | Select 策略；[[12-Factor Agents]] Factor 3 |
| progressive disclosure | Isolate 策略；OpenAI "map not manual" 同概念 |
| minimum high-signal token set | Compress 策略的目标函数 |
| CLAUDE.md + glob/grep hybrid | Claude Code 实例 |
| bloated tool set 失效 | Feedforward 过载 → non-guidance（OpenAI 同观察） |

Anthropic 提供 context engineering 的**认知科学地基**（context rot、attention budget、n² attention），Google 提供系统级地基（compiled view），LangChain 提供操作策略（四策略）。三者互补。
