---
title: "Karpathy: context engineering over prompt engineering"
source: "url"
source_file: "https://x.com/karpathy/status/1937902205765607626"
created: "2026-06-23T00:00:00Z"
source_url: "https://x.com/karpathy/status/1937902205765607626"
extract_method: "anysearch-extract"
---

# Karpathy on context engineering

Andrej Karpathy 推文（2025-06），公开为 "context engineering" 相对 "prompt engineering" 的提法背书。

## 原文

> "+1 for 'context engineering' over 'prompt engineering'. ... context engineering is just one small piece of an emerging thick layer of non-trivial software that coordinates individual LLM calls (and a lot [more])"

## 关键论点

- **context engineering > prompt engineering** — 术语升级，从"写好指令"扩展到"管好整个上下文窗口"
- context engineering 只是"协调单次 LLM 调用（及更多）的厚重软件层"的**一小片**——即 agent harness / 编排层
- 隐含：agent 工程的实质是这层"非平凡软件"，不是单点 prompt 技巧

## 关联

- 12-factor Factor 3（Own your context window）直接引用此推文作为 context engineering 术语的权威背书
- Anthropic 随后发布官方 "Effective context engineering for AI agents"，将 context engineering 定位为 prompt engineering 的自然延伸
- LangChain 也发文将 context engineering 策略归为 write / select / compress / isolate 四类
