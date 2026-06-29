---
title: "Deli AutoResearch 第四篇论文诞生记：285B 自博弈实验与诚实的自我评审"
type: summary
source_url: https://victorchen96.github.io/blog_self_play_story.html
source_type: article
date: 2026-06-26
ingested: 2026-06-26
tags: [deli-autoresearch, victor-chen, self-play, rl, grpo, peer-review, autonomous-research, long-horizon]
---

# Deli AutoResearch 第四篇论文诞生记：285B 自博弈实验与诚实的自我评审

**Source**: [Victor Chen / Deli Chen](https://victorchen96.github.io/blog_self_play_story.html) · 2026-06-26

## Key takeaways

- 这是 Deli AutoResearch 项目 **第四篇综述**《Self-Play in the Age of Foundation Models》的诞生故事；框架用 **16 轮五人格同行评审**把分数从 7.0 推到 **8.6/10**。
- 分数 **不是单调上涨**：V12 因外部引用核查发现 3 条问题引用，框架主动把分数从 8.5 **降到 8.2**，作者认为这是可信度最关键的一次信号。
- 核心实证是一个 **285B 参数 DeepSeek-V4 上的 GRPO 自博弈实验**：验证器噪声 ε 与改进幅度严格单调相关，KL 锚点可在噪声下形成可量化的缓冲/权衡。
- 理论加固（noise-floor 递推、coupled-floor lemma、匹配下界）是 V15→V16 的最后一公里；由 **单 Agent 串行 loop 通宵完成**，反而比并行多 Agent workflow 更有效。
- 与前三篇相比，这一篇证明了框架不仅能"写"综述，还能跑真实实验、诚实地给自己降分、并用新数学补理论缺口。

## Core claims

论文的核心命题是：**验证信号的质量决定自博弈改进的天花板**。在 18,953 道数学推理题、batch 512、N=16、32K 上下文的 GRPO 设置下：

- 训练分布准确率随 ε ∈ {0, 0.10, 0.30, 0.45} 的变化为 `+4.8 / +0.1 / −4.1 / −6.6` 个百分点，严格单调。
- 固定 ε=0.30，KL 系数 0 / 0.001 / 0.01 对应 `−9.9 / −4.1 / +0.8`；held-out 端点研究显示这是训练分布收益与泛化之间的真实权衡。
- 共 12 个 GRPO run，约 **3,570 GPU 卡时**；5 次提交失败被自主诊断修复，包括一个科学计数法学习率被解析为字符串的反复类型错误。

## Notable quotes

> "An autonomous pipeline that will mark its own work _down_ when the evidence demands it is far more trustworthy than one that only ever climbs."

> "The bottleneck was not more experiments — it was new mathematics."

> "The first three surveys showed an agent framework can _write_ a credible paper. This one showed something harder: it can run a real experiment to test the paper's own claim, score itself honestly (including downward), and close a theory gap with new math."

## Concepts introduced / referenced

- [[Heartbeat Watchdog]]
- [[Autonomous AI System]]
- [[Agent Harness 治理协议]]
- [[Worker Verifier 对抗循环]]
- [[Agentic Laziness]]
- [[Goal Drift]]
- [[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）]]

## Related raw sources

- [raw/articles/2026-06-26-deli-auto-research-self-play-story.md](../../raw/articles/2026-06-26-deli-auto-research-self-play-story.md) — 本文原始文本
- [raw/papers/2026-06-26-deli-self-play-survey-paper4.md](../../raw/papers/2026-06-26-deli-self-play-survey-paper4.md) — Paper #4 全文（pdftotext 提取）
- [raw/papers/2026-06-26-deli-auto-research-survey-paper1.md](../../raw/papers/2026-06-26-deli-auto-research-survey-paper1.md) — Paper #1
- [raw/papers/2026-06-26-deli-continual-learning-survey-paper2.md](../../raw/papers/2026-06-26-deli-continual-learning-survey-paper2.md) — Paper #2
- [raw/papers/2026-06-26-deli-long-horizon-survey-paper3.md](../../raw/papers/2026-06-26-deli-long-horizon-survey-paper3.md) — Paper #3
- [raw/articles/2026-06-26-deli-auto-research-series-overview.md](../../raw/articles/2026-06-26-deli-auto-research-series-overview.md) — 四论文系列总览
