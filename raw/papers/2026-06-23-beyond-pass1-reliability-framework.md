---
title: "Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents"
source: "url"
source_file: "https://arxiv.org/html/2603.29231v1"
created: "2026-06-23T00:00:00Z"
source_url: "https://arxiv.org/abs/2603.29231"
extract_method: "anysearch-extract"
authors: ["Aaditya Khanal", "Yangyang Tao", "Junxiu Zhou"]
affiliation: "School of Computing and Analytics, Northern Kentucky University"
---

# Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents

arXiv:2603.29231v1 [cs.AI] 31 Mar 2026. Northern Kentucky University.

## 核心命题

> "Machine learning benchmarks evaluate *capability* — whether a model succeeds on a single attempt. Production deployments require *reliability* — whether a model *consistently* succeeds across repeated invocations on tasks of varying duration. We show these two properties diverge systematically as task duration increases."

**capability ≠ reliability，且随任务时长系统性背离。**

## 关键实证

- **τ-bench**：GPT-4o 单次 pass@1 = 61%，但 pass@8 = 25% → 跑 8 次至少一次失败概率 75%。同一个 agent，"能力"和"可靠性"是两个数。
- reliability 随 task duration **超线性衰减**，而 pass@1 对此"结构性失明"（structurally blind）
- 实验：396-task benchmark，4 个 duration bucket × 3 domain，10 个开源模型，23,392 episodes，k=3 repeats，两 scaffold（ReAct + memory-augmented）

## 四个形式化指标

1. **Reliability Decay Curve (RDC)** — pass@k 随任务时长如何衰减
2. **Variance Amplification Factor (VAF)** — 时长如何放大随机失败模式
3. **Graceful Degradation Score (GDS)** — agent 部分完成长任务的部分得分
4. **Meltdown Onset Point (MOP)** — 滑动窗口熵 over tool-call 序列检测行为崩溃

## 四个发现

1. **Reliability decay 是 domain-stratified** — SE domain GDS 从 0.90 跌到 0.44（全时长范围），DP 几乎平（0.74→0.71）
2. **VAF 按 capability tier 二分** — frontier VAF ≥ 2.37，mid-tier VAF ≤ 1.26；反直觉地，**高方差放大是 capability signature，不是 instability signature**
3. **Capability 与 reliability 排名大幅背离** — medium 与 very-long horizon 之间出现多 rank inversion
4. **MOP paradox** — frontier models meltdown rate 最高（达 19%），因为它们追求野心勃勃的多步策略
5. **Memory scaffolds 普遍损害长程 reliability** — 10 个模型全部负面或中性，强证反对 naive episodic memory 作为 reliability 干预

## 对评估范式的含义

> "These results motivate reliability as a first-class evaluation dimension alongside capability."

reliability 应成为与 capability 并列的一等评估维度。现有 benchmark（SWE-bench、τ-bench、METR horizon、ReliabilityBench、OdysseyBench）无一同时覆盖：多模型 × duration 维度 × variance-aware 指标 × partial credit。

## 与本 wiki 的关联

- 把"确定性边界/能力评测"命题从工程直觉提升为**学术级形式化**——pass@k、reliability decay 是可量化语言
- 与 [[Agent-Macro-Evaluation]] 互补：macro-eval 是事后群体聚类诊断（找 behavior_pattern），本文是事前 reliability 维度度量（找 decay curve）
- MOP paradox 实证 12-factor Factor 10 的"贴边扩张"风险——能力越强越敢追多步策略，反而更易崩
- memory scaffolds 普遍有害 → 与 [[Agent-Memory]] 的"遗忘机制"open question 呼应
