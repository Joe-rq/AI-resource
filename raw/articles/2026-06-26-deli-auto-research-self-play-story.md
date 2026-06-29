---
title: "Self-Play in the Age of Foundation Models — A Comprehensive Survey: The Story of Paper #4"
source: url
source_url: "https://victorchen96.github.io/blog_self_play_story.html"
date: "2026-06-26"
ingested: "2026-06-26"
source_type: article
---

This is the story of **Paper #4** in my AutoResearch project: _Self-Play in the Age of Foundation Models — A Comprehensive Survey from Game-Theoretic Foundations to Open-Ended Learning_. Unlike the first three surveys, this one was not just written by the agent framework — it was **argued with, stress-tested, and experimentally validated** by it over 16 review rounds, ending at a median peer-review score of **8.6/10** (strong accept).

_Disclaimer: This is a personal hobby project. All opinions expressed are my own and do not represent any organization._

## The Score Trajectory: Not a Straight Line

What makes this paper interesting is that its score did **not** climb monotonically. The agent ran a five-persona peer review after each revision, and the median moved up and down honestly:

| Version| Score| What happened|
| ---| ---| ---|
| **V4–V10**| 7.0 → 8.4| Drafting: taxonomy, sections, and three original theorems. Citations grew from 0 to 207.|
| **V11**| 8.5| The 285B GRPO verifier-noise experiment landed in §8 — the paper turned from a pure survey into one with an original large-scale experiment.|
| **V12**| 8.2 ↓| The only decline. An external citation check found three defective references; the score was lowered to the paper's true state, not preserved.|
| **V13**| 8.4| A 2000-step long-horizon run (8.3× the original length) tested the KL-buffering hypothesis; data provenance was corrected.|
| **V14**| 8.4| Seed replication + KL ablation turned "buffering" from a hypothesis into evidence. Bottleneck shifted to theoretical rigor.|
| **V15**| 8.5| Held-out KL-endpoint study; parallel work started on four theoretical sub-problems.|
| **V16**| 8.6 ✓| Theory hardening landed — series best.|

Why V12 is the most important version

When the first external citation check found three submission-blocking references — one nonexistent paper, one with the wrong authors, and one whose arXiv ID pointed to an unrelated paper — the framework lowered its own score from 8.5 to 8.2 rather than quietly keeping the higher number. An autonomous pipeline that will mark its own work _down_ when the evidence demands it is far more trustworthy than one that only ever climbs. All three were fixed in the next iteration.

## The 285B RL Experiment: The Core Differentiator

The key decision was to validate the survey's central claim on a **real 285B-parameter model** (DeepSeek-V4) rather than a small-model demonstration. The setup: GRPO training, batch 512, N=16, 32K context, on 18,953 math-reasoning problems. The verifier flips its reward with probability ε — and the claim is that ε sets the ceiling on self-play improvement.

Two findings carried the paper:

- **Improvement falls monotonically with verifier noise.** Across ε ∈ {0, 0.10, 0.30, 0.45}, the relative change in training-distribution accuracy was `+4.8 / +0.1 / −4.1 / −6.6` percent — strictly monotone, and matching the ordering predicted by the paper's own theorem.
- **A KL anchor buffers against noise.** Holding ε=0.30 and sweeping the KL coefficient gave `−9.9 / −4.1 / +0.8` percent for KL = 0 / 0.001 / 0.01. The held-out KL-endpoint study then showed the buffer is a genuine dial with a sweet spot, not a one-way knob — there is a real tradeoff between training-distribution gains and held-out performance.

Twelve GRPO runs in total, about **3,570 GPU-hours** of compute. Five separate submission failures along the way were all diagnosed and fixed autonomously — including a recurring type error where a learning rate in scientific notation was parsed as a string. After the fourth recurrence, the framework wrote a pre-submission check script and baked the lesson into its own operating constraints.

## Five Personas, One Honest Median

Every review round is scored in parallel by five independent reviewer personas, each with a different bias:

| Persona| Role| What they push on|
| ---| ---| ---|
| **R1**| Experimentalist| Do the numbers in the paper match the raw experiment logs, line by line?|
| **R2**| Theorist| Are the proofs rigorous? _This was the binding constraint for most of the paper's life._|
| **R3**| Perfectionist| Table consistency, abstract accuracy, citation hygiene.|
| **R4**| Synthesizer| Does each addition answer a question the paper itself raised?|
| **R5**| Newcomer| Can a non-expert navigate it? (A reading guide and abbreviations table gave the largest single jump.)|

The median — not the mean — is the reported score, so a single enthusiastic reviewer can't inflate it. For most of the paper's life, the theorist (R2) sat at 8.0 and held the median down. That is exactly the signal that mattered.

## V16: Theory Hardening Was the Last Mile

By V14 the experiments were solid, but R2 kept the median pinned: the noise-floor argument and the KL-ablation sign weren't reconciled with the theory. The fix was not more experiments — it was **new mathematics**. Three sub-problems were solved and integrated:

1. **Noise-floor recurrence.** An exact closed-form re-derivation showing the floor is Θ(ηT) under harmonic coverage (which also caught a dropped-factor error in the paper's own draft), with a genuine constant floor η/ρ under an explicit mixing assumption.
2. **Coupled-floor lemma.** A rigorous Gibbs → Jensen → Pinsker chain bounding the KL-anchor displacement.
3. **Matching lower bound.** A persistence dichotomy proving the floor's order is optimal.

That carried the median from 8.5 to 8.6. Notably, this round was done overnight by a **serial single-agent loop** — two earlier attempts at parallel multi-agent workflows stalled and burned most of the round's tokens before the actual proofs came from the simpler serial approach. That lesson is now part of the framework's memory.

## What I Take Away

The first three surveys showed an agent framework can _write_ a credible paper. This one showed something harder: it can **run a real experiment to test the paper's own claim, score itself honestly (including downward), and close a theory gap with new math** — over six days, largely unattended. The remaining gap to a 9.0 is a single open problem (formalizing the held-out ↔ exploitability map), left as post-publication work.

Stay tuned.

这是我 AutoResearch 项目里 **第四篇论文** 的故事：《基础模型时代的自我博弈：从博弈论基础到开放式学习的综合综述》。和前三篇综述不同，这一篇不只是被 Agent 框架"写出来"——它被框架 **反复质疑、压力测试、并用真实实验验证**，历经 16 轮评审，最终中位分停在 **8.6/10**（strong accept）。

_声明：纯个人兴趣项目，不代表任何组织的立场，所有观点仅代表我个人。_

## 评分轨迹：不是一条直线

这篇论文有意思的地方在于，分数 **不是** 单调上涨的。每次改稿后，Agent 都会跑一轮五人格同行评审，中位分如实地上下波动：

| 版本| 分数| 发生了什么|
| ---| ---| ---|
| **V4–V10**| 7.0 → 8.4| 初稿阶段：三轴分类法、各章节、三个原创定理。引用从 0 累积到 207 条。|
| **V11**| 8.5| 285B GRPO 验证器噪声实验写入 §8——论文由纯综述变为含原创大规模实验。|
| **V12**| 8.2 ↓| 唯一一次下降。外部文献核查发现 3 条问题引用；按论文真实状态据实降分，不保留此前的 8.5。|
| **V13**| 8.4| 2000 步长程实验（原长度的 8.3 倍）检验 KL-buffering 假设；同时修正了数据来源。|
| **V14**| 8.4| 种子复现 + KL 消融把"buffering"从假设变为证据。瓶颈转移到理论严谨性。|
| **V15**| 8.5| KL 端点 held-out 研究；并行启动四个理论子问题的研究。|
| **V16**| 8.6 ✓| 理论加固落地——系列最高分。|

为什么 V12 是最重要的版本

第一次外部文献核查发现了三条投稿阻断级的引用错误——一条不存在的论文、一条作者错配、一条 arXiv ID 指向无关论文——框架选择把自己的分数从 8.5 降到 8.2，而不是悄悄保留高分。一个会在证据要求时把自己的工作 _往下打分_ 的自主流水线，远比一个只会往上爬的流水线可信。这三条都在下一轮迭代中修正了。

## 285B 强化学习实验：核心区分点

关键决策是用一个 **真实的 285B 参数模型**（DeepSeek-V4）来验证综述的核心命题，而不是用小模型做演示。配置：GRPO 训练，batch 512，N=16，32K 上下文，18,953 道数学推理题。验证器以概率 ε 翻转奖励——命题是 ε 决定自博弈改进的上限。

有两个发现撑起了这篇论文：

- **改进随验证器噪声单调下降。** 在 ε ∈ {0, 0.10, 0.30, 0.45} 下，训练分布准确率的相对变化为 `+4.8 / +0.1 / −4.1 / −6.6` 个百分点——严格单调，且与论文自身定理预测的排序一致。
- **KL 锚点能缓冲噪声。** 固定 ε=0.30、扫 KL 系数，KL = 0 / 0.001 / 0.01 时分别为 `−9.9 / −4.1 / +0.8` 个百分点。随后的 KL 端点 held-out 研究表明，这个缓冲是一个有 sweet spot 的真实"旋钮"，而非单向的开关——训练分布收益与 held-out 表现之间存在真实的权衡。

总计 12 个 GRPO run，约 **3,570 GPU 卡时** 的算力。过程中 5 次提交失败全部自主诊断并修复——包括一个反复出现的类型错误：科学计数法写的学习率被解析成了字符串。在第 4 次复现后，框架写了一个提交前检查脚本，并把这条教训固化进了自己的运行约束里。

## 五个人格，一个诚实的中位数

每一轮评审都由五个独立的评审人格并行打分，各有不同的偏好：

| 人格| 角色| 盯什么|
| ---| ---| ---|
| **R1**| 实验家| 论文里的数字是否与原始实验日志逐项对得上？|
| **R2**| 理论家| 证明是否严谨？ _这是论文大半生命周期里的硬约束。_|
| **R3**| 完美主义者| 表格一致性、摘要准确性、引用规范。|
| **R4**| 综合者| 每一项新增是否回答了论文自己提出的问题？|
| **R5**| 新手| 非专家能否读得进去？（一个阅读路线 + 缩写表带来了单轮最大涨幅。）|

报告的是中位数而非平均分，所以单个热情的评审人格无法把分数抬高。在论文大半的生命周期里，理论家（R2）一直停在 8.0，把中位数压住。这恰恰是最该被听见的信号。

## V16：理论加固是最后一公里

到 V14 时实验已经扎实，但 R2 始终压着中位数：noise-floor 的论证和 KL 消融的符号没有和理论自洽。解决办法不是更多实验——而是 **新的数学**。三个子问题被攻下并整合进论文：

1. **噪声地板递推。** 一个精确闭式的重导，证明在 harmonic coverage 下地板是 Θ(ηT)（顺带抓出论文自身初稿里的一处掉因子错误），并在显式 mixing 假设下给出真常数地板 η/ρ。
2. **耦合地板引理。** 用严格的 Gibbs → Jensen → Pinsker 链给出 KL 锚点位移的界。
3. **匹配下界。** 一个持久性二分，证明地板的阶数是最优的。

这把中位数从 8.5 推到了 8.6。值得一提的是，这一轮是由一个 **单 Agent 串行 loop** 通宵完成的——此前两次尝试用并行多 Agent workflow 都 stall 了，烧掉了这一轮大部分 token，真正的证明产出反而来自更简单的串行方式。这条教训现在已经写进框架的记忆里。

## 我的收获

前三篇综述证明了 Agent 框架能 _写_ 出一篇可信的论文。这一篇证明了更难的事：它能 **跑一个真实实验来检验论文自己的命题、诚实地给自己打分（包括往下打）、并用新数学补上理论缺口**——历时六天，基本无人值守。距离 9.0 只剩一个开放问题（把 held-out ↔ exploitability 的映射定理化），留作发表后的工作。

Stay tuned.
