---
title: "Eval-Driven Development"
type: concept
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/notes/madhuguru-evals/part-01-2026-08-17.md"
  - "raw/notes/madhuguru-evals/part-02-2026-08-19.md"
  - "raw/notes/madhuguru-evals/part-03-2026-08-20.md"
  - "raw/notes/madhuguru-evals/part-04-2026-08-21.md"
  - "raw/notes/madhuguru-evals/part-05-2026-08-21.md"
  - "raw/notes/madhuguru-evals/part-06-2026-08-22.md"
  - "raw/notes/madhuguru-evals/part-07-2026-08-24.md"
  - "raw/notes/madhuguru-evals/part-08-2026-08-25.md"
  - "raw/notes/madhuguru-evals/part-09-2026-08-26.md"
  - "raw/notes/madhuguru-evals/part-10-2026-09-10.md"
  - "raw/articles/andrew-ng-skills-map/part-02-2026-08-21.md"
  - "raw/articles/andrew-ng-skills-map/part-04-2026-09-04.md"
  - "raw/articles/2026-01-09-anthropic-demystifying-evals-for-ai-agents.md"
tags: [evaluation, eval-methodology, eval-driven-development, failure-modes-taxonomy, hill-climb, discriminatory-property, jobs-to-be-done, eval-roadmap, trajectories, capability-vs-regression, eval-ladder]
---

# Eval-Driven Development

> **Eval-driven development**：把 AI 系统的质量评估从"后置验证"提升为**开发循环的主驱动力**——以评测信号为中心，规划执行→诊断失败→针对性优化→再次评测的方法论。代表来源：[Madhuguru "How to build great evals" 10 篇系列](https://x.com/realmadhuguru)（2026-08-17 ~ 09-10）、Andrew Ng "AI Engineering Skills Map Part 2"、Anthropic "Demystifying evals for AI agents"。

## 定义

Eval-driven development（EDD）= **以评测信号驱动的 AI 系统开发方法论**。它把传统的"build → measure → learn"循环具体化为可操作的评测阶梯、failure mode taxonomy、step-level evaluation 与 roadmap evolution。**核心论断**（Madhuguru Part 1）：

> "The best way to get good at evals is to take a workflow you know really well and figure out how to make its quality measurable."

与"测试驱动开发（TDD）"的区别：**EDD 的目标不是"测试覆盖率"或"先写测试再写代码"，而是"评测信号是否能驱动团队决策"**——这是更宽的范畴，包含失败分类、阶梯化策略、discriminatory power、随产品演进的 roadmap。

## 四大支柱

### 支柱 1：Laddered Eval Strategy（阶梯化策略）

单一 eval 无法同时满足"高质量信号"和"低成本"的需求。Madhuguru（Part 4）给出企业级梯子：

```mermaid
flowchart LR
    H[Hill-climb<br/>长 / 难 / 信号强] --> R[Regression<br/>短 / 稳定 / 必备]
    R --> S[Smoke test<br/>关键安全与基础]
    S --> L[Launch<br/>接近线上真实流量]
```

| 类型 | 目的 | 频率 | 信号特性 | 成本 |
|------|------|------|---------|------|
| **Hill-climb** | 推产品质量前沿 | 持续刷新 | 高 | 高 |
| **Regression** | "今天的产品坏没坏" | 每次改动 | 中（必须稳定） | 中 |
| **Smoke test** | 关键安全与基础（不能错） | 每次改动 | 中（错不起） | 低 |
| **Launch** | 接近线上真实流量 | 上线前 | 中（控制少，最真实） | 中 |

**Anthropic 的平行二分法**（[Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)）：capability eval（起始低通过率，给团队"山"）+ regression eval（接近 100% 通过，防后退）。**生命周期**："launch 后 capability eval 高通过率可'毕业'为 regression suite 持续跑"——能力可变成可靠性。

### 支柱 2：Failure Modes Taxonomy（失败模式分类法）

> ""Bad answer" is not a useful cluster name."（Madhuguru Part 3）

EDD 的核心操作：**从 production traces 中提取具体失败模式，命名、聚类、针对性建 eval**。

操作手册：

1. 抽 500-1000 次 production 交互，研究失败
2. 聚类 + 命名 cluster
3. **必须具体**——示例：
   - `wrong document retrieved`
   - `right document but irrelevant section`
   - `failed to ground to context and hallucinated`
   - `failed to punt and made stuff up`
   - `question ambiguous, made poor assumptions rather than asking`
4. 命名精准后，**针对性建 eval 抓它们**——形成"evals → 改进飞轮"

与 [[Agent Macro Evaluation]] 的 BERTopic 风格聚类同向——**差异**：OpenAI 用算法自动提取关键词 + 人类解释簇；Madhuguru 强迫人类从一开始就**给具体命名**。两种范式正交互补。

### 支柱 3：Discriminatory Property（区分能力差异）

> "**A hill-climbing eval is useful when it can separate AI systems that are meaningfully different.**"（Part 8）

Eval 的核心质量指标 = **区分度**——能否把"真的更好"和"只是噪声差异"分开。

反例：5 个系统跑出 A:94 / B:93 / C:95 / D:94 / E:92——如果你已知 A/C 比 D/E 强很多，**这个 eval 没有区分能力**。"给一群 PhD 出五年级数学题"。

**Sweet spot = realistic + difficult + sensitive to capability differences**。

- 任意难 → 大家都 fail → 没信号
- 任意易 → 大家都 aces → 没信号
- **饱和问题**（Part 8 末问）：好 evals 随 harness / model 改善而饱和，所有题都过——怎么办？（留作研究问题）

### 支柱 4：Step-Level Evaluation（轨迹步骤评分）

> "**Measure the steps, not just the result.**"（Part 10）

两个 trajectory 同样得 42：

```text
A: search right sources → retrieve right doc → 4 clean tool calls → calculate
B: search same thing 3× → 17 calls → recover from 2 errors → eventually get 42
```

显然 A 更好。EDD 要求**对 workflow 的每个 step 建 eval**——读 eval 结果时**先看 steps，再看 final results**。

4 步操作：

1. **Clearly define the whole workflow**
2. **Define tasks at each step**
3. **Decide how to measure each step**（独立 eval 或大 eval 一段）
4. **Define median + hard tasks**——反映到 eval 设计

**与 [[Trajectory Handoff]] 同源**——两者独立提出"trajectory 步骤评分"作为 agent 评估的核心（2026-09 同月）。

## 核心原则

### 原则 1：Quality First, Cost Next（质量前沿先于成本曲线）

> "**Treat evals like frontier models…establish the quality frontier first, then work your way down the cost curve.**"（Part 2）

操作路径：

1. 先用最贵但最强的 evaluator（best LLM judge / 人类 SME / 你的时间）建立**可信信号**
2. 拿到可信信号后，**再降本**——自动化 / 小 judge / 采样 / 确定性检查

**反直觉点**：**不要从便宜的方法开始**——便宜的信号若不可信，之后所有 hill-climb 都建立在沙地上。

### 原则 2：Tyranny of the Average（反对单分数化简）

> "**Stop dumbing down the results from your beautiful, complex eval suite into one single score.**"（Part 5）

触发场景：高级管理者要简化数字做决策。

反例：
> 一个模型在简单摘要 85→89%，基础事实 QA 80→85%，**但在关键复杂财务分析 70→63%**——单分数遮蔽了 frontier use case 退步。

加权分数也没救——给 judgment call 套"数学外衣"反而更糟。

正确做法：
1. **保留 prioritized list of evals**（按阶梯）
2. **找能看细节、不追求抽象简单的人**做决策
3. 深入理解所有关键 eval 的"哪里失败 / 哪里发光"

### 原则 3：Goldilocks Principle（jobs-to-be-done 粒度）

> "**Your evals should measure at the level of the various jobs to be done, not just the final answer.**"（Part 7）

金融分析 agent 的 jobs：

```text
1. Understand client (portfolio / risk / horizon / goals / constraints)
2. Gather evidence (latest data / sector / macro / Fed / news)
3. Analyze data (revenue / valuation / projections → candidates)
4. Make recommendation (ticker / price / timeframe)
```

每个 stage 有独立 eval，错位发现：

```yaml
Client understanding:  92%
Evidence extraction:   92%
Data analysis:         70%  ← 知道哪坏
Recommendation:        75%
```

**Not too granular. Not too coarse. Just right.**——颗粒度以"能诊断能行动"为度。

### 原则 4：Eval Roadmap Evolution（评测随产品演进）

> "**Most evals fail because teams treat them as static artifacts while their users' expectations and behaviors have evolved.**"（Part 9）

金融研究 agent 用例演进：

```text
Week 1:  Summarize 5-page earnings report.
Week 3:  Review last 5 reports; explain growth story.
Month 2: 15 filings + transcripts + research → investment thesis.
Month 3+: Monitor portfolio; alert on material thesis changes.
```

每个阶段需要不同能力 + 不同 evals。

5 步 roadmap：

1. Map 用例演进维度（turns / 文档量 / 工具 / 自主性 / journey 覆盖）
2. 优先级排产品最重要的 use cases × 维度
3. 谈用户 + 挖 production trace 找 shift
4. 下一阶段 usage 的 P0 evals
5. 跑 evals → 找 failure mode（taxonomy）→ hill climb

## Hill Climbing 实操（Part 6 详解）

> "**Hill climbing on evals = pick a dimension that matters and optimize for it.**"

可优化的维度：

- 已有功能的 quality（用最新 production data + 高价值 user journeys）
- 扩展到邻近 use case
- 降本 / 降延迟

**手段集**：

```text
Prompt engineering    →  低成本快速迭代
Context engineering   →  给正确 stage 正确信息
Memory                →  长 session 状态保留
Post-training         →  模型 fine-tune
Deterministic code    →  把不可靠 LLM 调用换为可靠代码
```

**典型例子**：tool calling 失败常见 → 挖下去发现 "20 个 tool 全塞进 context，每个 task 实际只 3-5 个" → **hill climb = context eng 给正确 stage 正确 tool**。

**Madhuguru 的成本建议**：launch with best model first → 拿到质量 → hill climb 到小 model 同质量——同样的 harness + 模型切换即可。

## 与本 Wiki 的关联

| EDD 概念 | 关联 Wiki |
|---------|----------|
| **Eval ladder / Capability vs Regression** | [[Agent Evaluation Methodology]]（Anthropic）——平行二分法；[[Agent Reliability vs Capability]]——RDC 与 capability decay |
| **Failure modes taxonomy** | [[Agent Macro Evaluation]]（OpenAI）——BERTopic 风格聚类，但 OpenAI 是算法聚类，Madhuguru 强迫人类命名 |
| **Discriminatory property** | [[Tournament Mode]]（pairwise + transitivity 假设）——同向（pairwise 是 discriminatory property 的具体实现）；[[Multi-Model Ensemble]] "算力公平"前提 |
| **Goldilocks / step-level eval** | [[Trajectory Handoff]]——同月同论点（"传 trajectory 不传 plan"）；[[Worker Verifier 对抗循环]]——对抗到收敛的 step 粒度 |
| **Hill climbing** | [[Claude Code Loops]]——Goal-based loop 同源（loop until metric improvement）；[[Harness Cybernetics]]——feedback Sensors 的优化对象 |
| **Tyranny of average** | [[Multi-Model Ensemble]]——加权聚合不等于 judgment；与 [[MiniMax-Mavis]] 的 Orchestrator-Worker 评分体系对照 |
| **Eval roadmap** | [[Agent Harness 治理协议]]——概念节点演化是 eval roadmap 的工程版 |
| **Quality-first, cost-next** | [[Building Verification Loops in Claude Code]]——verification loop 是质量前沿的具体机制 |
| **Eval-driven 整体** | [[Andrew Ng AI Engineering Skills Map (5 篇)]]（Part 2 子技能 4）——Ng 自评"最区分优秀 AI 工程师" |

## 落地清单

把 EDD 迁移到自己的 Agent 系统：

1. **画用例演进轨迹**——预测 next 2-3 阶段的 use case 演进，标注每个阶段的 capability 缺口
2. **搭 4 类 eval ladder**——hill-climb / regression / smoke / launch 各有独立 suite
3. **建 production trace 捕获管线**——500-1000 次失败样本是 failure mode taxonomy 的起点
4. **命名 cluster**——拒绝 "bad answer" 类通用名；要求每个 cluster 名可触发独立 fix
5. **建立 step-level eval**——把 workflow 拆成 jobs，每个 job 有独立 eval
6. **先质量后成本**——第一版 eval 用最强 judge 拿可信信号，再自动化
7. **保留 prioritized list**——不要合并成单分数；保留 per-dimension 详细结果
8. **检查 discriminatory power**——确认 eval 能区分能力差异；饱和时升级难度
9. **跨 iteration 维护 eval**——随产品演进追加 P0 evals，防止"周 1 evals 钉死在 week 1"
10. **读 transcripts**——失败是否"公平"靠 transcripts 验证；不读 = 不知 eval 在测什么

## 关键洞察

1. **Eval 是产品 spec 的 stress test**——把"我们以为产品该做什么"变成"可验证的"——这是 [[Forward Deployed Engineering]] 的"deploy before spec final" 在质量层的实现。
2. **"具体 cluster 名"是 EDD 与传统监控的真正差异**——传统监控给 "error rate"; EDD 给 "tool calling 失败中 60% 是 tool over-stuffing"——后者直接指向 fix。
3. **Discriminatory property 是 eval 设计的元指标**——比 pass@k、accuracy 更基础；一个低区分度的 eval 浪费时间。
4. **Eval ladder 是组织能力，不只是技术栈**——它要求团队有"质量评估预算"（花时间在对的 eval 上），不被单分数诱惑，与 [[Finding Your Unknowns]] 的"reduce unknowns" 同源。

## Open Research Questions

- **Eval 饱和后如何继续 hill-climb？** Madhuguru Part 8 末尾提出但未答；与 [[Agent Reliability vs Capability]] 的"reliability decay 是否可被 eval 提前探测" 相关
- **Failure mode taxonomy 的"足够具体"边界在哪？** 过细 → 维护成本爆炸；过粗 → 无法诊断；与 [[Agent Macro Evaluation]] 的 `MACRO_EVALS_DISCOVERY_MIN_CLUSTER_SIZE` 超参同向
- **Step-level eval 的 token 成本如何控制？** trajectory 每步独立 eval 成本爆炸；与 [[Multi Model Ensemble]] "增益扣算力"研究问题相关
- **Eval-driven 与 spec-driven 的边界？** Andrew Ng 强调 spec；Anthropic eval-driven 包含 spec——两者是否可统一？
- **Eval ladder 能否形式化为 schema？** 类似 [[ESAA]] 的 boundary contracts；与 [[Agent Harness 治理协议]] 的"概念节点演化"schema 同源

## Related Concepts

- [[Agent Evaluation Methodology]] — Anthropic 元方法论；与 EDD 的差异在抽象层级（EDD 是策略，方法论是机制）
- [[Agent Macro Evaluation]] — OpenAI 群体诊断视角；EDD 是个体策略视角
- [[Agent Reliability vs Capability]] — pass@k 与 RDC 是 EDD 度量基础
- [[Trajectory Handoff]] — step-level trajectory 评分的同源论据
- [[Harness Cybernetics]] — feedback Sensors 与 eval ladder 同构
- [[Andrew Ng AI Engineering Skills Map (5 篇)]] — Ng 自评 EDD 是"最区分优秀 AI 工程师的技能"
