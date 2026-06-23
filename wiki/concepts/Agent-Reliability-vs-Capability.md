---
title: "Agent Reliability vs Capability"
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: ["raw/papers/2026-06-23-beyond-pass1-reliability-framework.md", "raw/articles/2026-06-23-anthropic-building-effective-agents.md"]
tags: [evaluation, reliability, capability, pass-at-k, long-horizon, variance, meltdown, deterministic-boundary, production]
---

# Agent Reliability vs Capability（可靠性与能力的背离）

> **capability 问"能不能做到一次"，reliability 问"能不能次次都做到"。这两件事不是同一个数，且随任务时长系统性背离。** —— 把"确定性边界"命题从工程直觉提升为可量化的评估维度。

## 核心命题

传统 ML benchmark 测的是 **capability**——单次最佳尝试能否成功。生产部署需要的是 **reliability**——跨多次调用、跨不同时长任务能否**一致**成功。

> "These two properties are not the same... reliability degrades *super-linearly* with task complexity... and this degradation is invisible to benchmarks reporting only pass@1 on short, atomic tasks." —— arxiv 2603.29231

来源：Khanal, Tao, Zhou (NKU, 2026-03)，*Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents*。

## capability ≠ reliability 的实证

**τ-bench**：GPT-4o 在零售 agent 任务上

| 指标 | 值 | 含义 |
|---|---|---|
| pass@1 | 61% | 单次能成功 |
| pass@8 | 25% | 跑 8 次全部成功的概率 |

→ 跑 8 次**至少一次失败的概率 ≈ 75%**。同一个 agent，"能力"和"可靠性"是两个数。

实验规模：396-task benchmark × 4 duration bucket × 3 domain × 10 开源模型 × 23,392 episodes × k=3 repeats × 2 scaffold（ReAct + memory-augmented）。

## 四个形式化指标

| 指标 | 全称 | 度量什么 |
|---|---|---|
| **RDC** | Reliability Decay Curve | pass@k 随任务时长如何衰减 |
| **VAF** | Variance Amplification Factor | 时长如何放大随机失败模式 |
| **GDS** | Graceful Degradation Score | agent 部分完成长任务的部分得分 |
| **MOP** | Meltdown Onset Point | 滑动窗口熵 over tool-call 序列检测行为崩溃 |

## 五个发现

1. **Reliability decay 是 domain-stratified** — SE domain GDS 从 0.90 跌到 0.44（全时长），DP 几乎平（0.74→0.71）。衰减不是均匀的。
2. **VAF 按 capability tier 二分** — frontier VAF ≥ 2.37，mid-tier VAF ≤ 1.26。**反直觉：高方差放大是 capability signature，不是 instability signature**——强模型探索面更广。
3. **Capability 与 reliability 排名大幅背离** — medium 与 very-long horizon 之间出现多 rank inversion。capability 榜单不能外推到长程 reliability。
4. **MOP paradox** — frontier models meltdown rate 最高（达 19%），因为它们追求野心勃勃的多步策略。**能力越强反而越容易崩。**
5. **Memory scaffolds 普遍损害长程 reliability** — 10 个模型全部负面或中性。强证反对 naive episodic memory 作为 reliability 干预。

## 为何这是"确定性边界"命题的学术化

工程直觉说：agent 的不可靠性集中在 LLM 与确定性工具的**接缝**，单次评测没意义，要看分布。本文把这直觉形式化：

- **pass@k 是接缝失败率的分布语言**——不是"能不能"，是"k 次里几次"
- **reliability decay 是"接缝随步数累积"的度量**——步数越多，接缝失败概率乘积越大，超线性衰减
- **MOP paradox 是"贴边扩张"的反面**——[[12-Factor Agents]] Factor 10 主张贴着 model capability edge 走，本文实证：贴太紧会 meltdown

## 与四种确定性范式的对应

[[12-Factor Agents]] 归纳的四种对付接缝范式，在本文框架下各有 reliability 含义：

| 范式 | reliability 处理 |
|---|---|
| 压概率空间（schema/structured output） | 降低单步接缝失败率 → 提升 pass@1，但 decay 曲线形状不变 |
| Verifier 循环 | 把单步失败转成重试 → 降低 VAF |
| 统计签收（pass@k） | 不消灭不确定性，接受分布 → 这正是本文的语言 |
| 确定性外移 | 减少接缝数量 → 直接降低 decay 斜率 |

## 评估范式含义

> "reliability as a first-class evaluation dimension alongside capability."

现有 benchmark 的结构性盲区（无一同时覆盖）：

| Work | 多模型 | duration 维度 | variance | partial credit |
|---|---|---|---|---|
| τ-bench | 6 | × | pass@k | × |
| SWE-bench | 20+ | × | × | × |
| METR horizon | 3 | ✓ | × | × |
| ReliabilityBench | 2 | × | ✓ | × |
| **本文** | **10** | **✓** | **✓** | **✓** |

## 与现有 wiki 概念的关系

| 关联 | 说明 |
|---|---|
| 事后诊断 vs 事前度量 | [[Agent Macro Evaluation]] 是运行后群体聚类找 behavior_pattern；本文是事前 reliability 维度度量找 decay curve。两者正交互补 |
| 80% 墙的本质 | [[12-Factor Agents]] 的 80% 墙 = capability 到 80% 后 reliability 接管，pass@1 失明 |
| 记忆的代价 | memory scaffolds 普遍有害 → 直接关联 [[Agent Memory]] 的"遗忘机制"open question |
| 长程自主性 | 衰减超线性 → 长任务必须靠 [[Stateless Reducer]] 的可重放 + 接缝外移，不能靠模型硬扛 |
| Worker/Verifier | [[Worker Verifier 对抗循环]] 是单步降 VAF 的机制；本文给出为何长程必须叠加它 |

## 落地含义

- **模型选择**：不能只看 capability 榜单（SWE-bench pass@1），必须看目标时长桶的 RDC
- **长任务设计**：步数是 reliability 的敌人——拆短、外移确定性、加 Verifier，而不是指望模型扛
- **memory 慎用**：naive episodic memory 损害长程 reliability，[[Agent Memory]] 的遗忘机制不是优化是必需
- **评估改造**：补 duration 维度 + variance-aware 指标 + partial credit，否则对长程部署结构性失明
