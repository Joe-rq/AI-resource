---
title: "How to Build Great Evals（Madhu Guru 10 篇系列）"
type: summary
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
tags: [agent-evals, eval-methodology, eval-driven-development, failure-modes-taxonomy, hill-climb, discriminatory-property, jobs-to-be-done, eval-roadmap, trajectories, madhuguru, eval-ladder, capability-vs-regression]
---

# How to Build Great Evals（Madhu Guru 10 篇系列）

> 原始来源：[Madhu Guru (@realmadhuguru)](https://x.com/realmadhuguru) X 推文系列 · 2026-08-17 ~ 2026-09-10
> 摄取日期：2026-09-14 · 抓取方法：无登录 SSR HTML（不受 280 字截断影响）
> 论点反哺 [[Eval-Driven Development]]（本系列核心方法论的直接素材）、[[Agent Macro Evaluation]]（OpenAI 视角的群体诊断）、[[Agent Evaluation Methodology]]（Anthropic 元方法论）、[[Trajectory Handoff]]（Part 10 "测量步骤不只测结果" ↔ trajectory handoff）。

## 摘要

Madhu Guru（ex-Google DeepMind Gemini 团队）以"日更"节奏连发 10 篇"How to build great evals"，把**企业级 AI 系统评测的实战经验**压缩成可执行方法论。**没读 OpenAI Cookbook 之前这是最好的入门；读完 OpenAI Cookbook 之后这是最贴地的 checklist**。

10 篇主题总览：

| Part | 日期 | 标题 | 核心概念 |
|------|------|------|----------|
| 1 | 08-17 | 开场白 | 把熟悉工作流的可测性 |
| 2 | 08-19 | Eval 成本 | 质量前沿先于成本曲线 |
| 3 | 08-20 | Failure modes taxonomy | trace 聚类 → 命名 → 针对性 eval |
| 4 | 08-21 | Laddered eval strategy | hill-climb / regression / smoke / launch 四层 |
| 5 | 08-21 | Tyranny of the average | 反对单分数化简 |
| 6 | 08-22 | Hill climbing 详解 | 维度优化 + harness/model |
| 7 | 08-24 | Goldilocks principle | jobs-to-be-done 粒度 |
| 8 | 08-25 | Discriminatory property | realistic + difficult + sensitive |
| 9 | 08-26 | Eval roadmap problem | evals 随用户演进 |
| 10 | 09-10 | Measure the steps, not just the result | trajectory 步骤评分 |

## 各篇核心论点

### Part 1 — 开场白（2026-08-17）

> **"The best way to get good at evals is to take a workflow you know really well and figure out how to make its quality measurable."**

学习路径：

1. 看真实 trace——典型用户 prompt 序列、每步与终态的好响应长什么样
2. 看产品哪里失败——创造 trace 捕获失败（messy tool call / missing context 等）
3. 拿到好 eval 后，想**如何让 eval 自动可重复跑**
4. **让 eval 持续镜像 live traffic**——用户模式会变

> 这是个系列。开篇提出"可测性优先"作为入门者训练心法。

### Part 2 — 成本（2026-08-19）

> **"Treat evals like frontier models…establish the quality frontier first, then work your way down the cost curve."**

反直觉：**先把质量打到最高**（最贵 judge / 人工 / 你的时间），拿到可信信号后**再降本**（自动化 / 小 judge / 采样 / 确定性检查）。Quality first. Cost next.

### Part 3 — Failure modes taxonomy（2026-08-20）

> **"Bad answer" 不是一个有用的 cluster name.**

操作手册：

1. 从 production traces 抽 500-1000 次交互，研究失败
2. 聚类 + 命名 cluster
3. **关键要求：必须具体**——例如：
   - "wrong document retrieved"
   - "right document but irrelevant section"
   - "failed to ground to context and hallucinated"
   - "failed to punt and made stuff up"
   - "question ambiguous, made poor assumptions rather than asking"
4. 命名精准后，**针对性建 eval 抓它们**——"evals → 改进飞轮"的桥

> "这些是非常不同的问题"——每种失败需要独立的诊断 + 独立的 fix。

### Part 4 — Laddered eval strategy（2026-08-21）

> "**Laddered eval strategy, with multiple evals on the cost/realism spectrum.**"

| Eval 类型 | 目的 | 频率 | 性质 |
|----------|------|------|------|
| **Hill-climb** | 推产品质量前沿 | 持续刷新 | 长、难、信号强 |
| **Regression** | "今天的产品坏没坏" | 每次改动 | 短、稳定、必备 |
| **Smoke test** | 关键安全与基础（不能错） | 每次改动 | 不一定难，但错不起 |
| **Launch** | 接近线上真实流量 | 上线前 | 控制少，但最真实 |

企业级 AI 系统的失败 → "没有 eval strategy"（Part 4 直接点名）。

### Part 5 — Tyranny of the average（2026-08-21）

> "**Stop dumbing down the results from your beautiful, complex eval suite into one single score.**"

触发场景：高级管理者想要简化数字做决策。Madhu 点名 Gemini 早期就踩过这坑。

反例：
> 一个模型在简单摘要 85→89%，基础事实 QA 80→85%，**但在关键复杂财务分析 70→63%**——单分数遮蔽了"你的 frontier use case 退步"。

加权分数也没救——给 judgment call 套上"数学外衣"反而更糟。

正确做法：
1. **保留 prioritized list of evals**（按 Part 4 梯子）
2. **找能看细节、不追求抽象简单的人**做决策
3. 深入理解所有关键 eval 的"哪里失败 / 哪里发光"

### Part 6 — Hill climbing 详解（2026-08-22）

> "**Hill climbing on evals = pick a dimension that matters and optimize for it.**"

可优化的维度：

- 已有功能的 quality（用最新 production data + 高价值 user journeys）
- 扩展到邻近 use case
- 降本 / 降延迟

**手段集**：prompt eng / context eng / memory / post-training / deterministic old school code。

**Failure mode taxonomy（Part 3）= compass**——告诉团队"产品哪里挣扎需要爱"。

**关键例子**：tool calling 失败常见，挖下去发现 "20 个 tool 全塞进 context，每个 task 实际只 3-5 个"——hill climb = context eng 给正确 stage 正确 tool。

**Madhu 的成本建议**："launch with best model first → 拿到质量 → hill climb 到小 model 同质量"——同样的 harness + 模型切换即可。

### Part 7 — Goldilocks principle（2026-08-24）

> "**Your evals should measure at the level of the various jobs to be done, not just the final answer.**"

反例：金融分析 agent 的终极产出 = 股票推荐。常见错是建 golden set 检查"是不是对的股票"。

问题：推荐之前有一串 meaningful jobs：

```text
1. Understand client（portfolio, risk tolerance, horizon, goals, constraints）
2. Gather evidence（最新数据 / sector / macro / Fed policy / news）
3. Analyze data（revenue growth, valuation, growth projections → 候选股）
4. Make recommendation（ticker / 价格 / timeframe）
```

每个 stage 有中间输出、每个 stage 都可独立 eval。错位发现：

```yaml
Client understanding:  92%
Evidence extraction:   92%
Data analysis:         70%  ← 知道哪坏
Recommendation:        75%
```

**Not too granular. Not too coarse. Just right.**——颗粒度以"能诊断能行动"为度。

### Part 8 — Discriminatory property（2026-08-25）

> "**A hill-climbing eval is useful when it can separate AI systems that are meaningfully different.**"

反例：5 个系统跑出 A:94 B:93 C:95 D:94 E:92——eval 没用，因为你知道 A/C 比 D/E 强很多，它**没区分出来**。"给一群 PhD 出五年级数学题"——大家 aces 你学不到东西。

不是要任意难——大家都 fail 也没用。**Sweet spot = realistic + difficult + sensitive to capability differences**。

警告：好 evals 会随 harness/model 改善而**饱和**（所有题都过）。怎么办？（Madhu 留给评论）

### Part 9 — Eval roadmap problem（2026-08-26）

> "**Most evals fail because teams treat them as static artifacts while their users' expectations and behaviors have evolved.**"

金融研究 agent 的用例演进：

```text
Week 1:  Summarize this 5-page earnings report.
Week 3:  Review the last 5 earnings reports and explain their growth story.
Month 2: 15 filings + transcripts + research reports → build investment thesis.
Month 3+: Monitor my stock portfolio; alert me when something materially changes my thesis.
```

每个阶段需不同能力 + 不同 evals。

演进维度：

```text
short-context → long-context
single-turn QA → multi-turn
passage citations → doc/line citations
simple QA → complex synthesis
reactive chat → proactive agent
```

"**Evals 钉在 week 1 而用户在 week 3——产品 + churn 数据会出卖你**"。

5 步 roadmap：

1. Map 用例演进维度（turns / 文档量 / 工具 / 自主性 / journey 覆盖）
2. 优先级排产品最重要的 use cases × 维度
3. 谈用户 + 挖 production trace 找 shift
4. 下一阶段 usage 的 P0 evals
5. 跑 evals → 找 failure mode（Part 3 taxonomy）→ hill climb（Part 6）

### Part 10 — Measure the steps, not just the result（2026-09-10）

> "**Much like high school math, it isn't sufficient just to get the right answer; the steps to get there are critical.**"

两个 trajectory 同样得 42：

```text
A: search right sources → retrieve right doc → 4 clean tool calls → calculate
B: search same thing 3× → 17 calls → recover from 2 errors → eventually get 42
```

哪个更好不言自明。

4 步操作：

1. **Clearly define the whole workflow**
2. **Define tasks at each step**
3. **Decide how to measure each step**（独立 eval 还是大 eval 一段）
4. **Define median + hard tasks**——把它们反映到 eval 设计

读 eval 结果时：**先看 steps，再看 final results**。

## 与本 Wiki 的关联

| Madhuguru 论点 | 反哺 / 对照 Wiki 概念 |
|--------------|---------------------|
| **Eval ladder（Part 4）** | 与 [[Agent Evaluation Methodology]] 的 "Capability vs Regression" 两分法同源；与 [[Agent Reliability vs Capability]] 的 "reliability decay curve" 互补 |
| **Failure modes taxonomy（Part 3）** | 与 [[Agent Macro Evaluation]] 的 BERTopic 风格聚类同向（Madhuguru 是手动聚类，OpenAI Cookbook 是算法聚类）；"具体 cluster 名 = diagnostic 起点"是双方共识 |
| **Discriminatory property（Part 8）** | 与 [[Tournament Mode]]（pairwise + transitivity 假设）正交；呼应 [[Multi-Model Ensemble]] "收益三条件之一 = 算力公平"（eval 必须能区分能力差异） |
| **Goldilocks principle（Part 7）** | 与 [[Trajectory Handoff]] 的 "trajectory 步骤评分" 同向；与 [[Worker Verifier 对抗循环]] 的"对抗到收敛"互补 |
| **Evaluate the evals（Part 1, Part 8）** | 与 [[Harness Cybernetics]] 的"反馈 Sensors 必须 calibrate"同源 |
| **Eval roadmap（Part 9）** | 与 [[Agent Harness 治理协议]] 的"概念节点演化"同向——两者都是"系统级 artifact 必须随实践演进而非静态定义" |
| **Tyranny of average（Part 5）** | 与 [[Multi-Model Ensemble]] 的"加权分数不等于 judgment"对照（MoA 论文的 aggregator 不主张单分） |
| **Hill climbing（Part 6）** | 与 [[Claude Code Loops]] 的 "Goal-based loop" 同源——loop 直到 metric 上 improvement |

## 关键洞察

1. **Madhuguru 框架与 OpenAI Cookbook 视角互补**：OpenAI 偏群体诊断（聚类 + AgentTrace 回溯），Madhuguru 偏个体策略（ladder + taxonomy + discrimination + roadmap）。两者对同一个 agent 系统的不同生命周期阶段都有用。
2. **"具体 cluster 名" 是设计点**：Madhuguru 反复强调 "**"bad answer" is not a useful cluster name**"——这是 failure mode taxonomy 的真正难点，也是它与 [[Agent Macro Evaluation]] BERTopic 风格聚类的核心差异（后者让算法自动提取关键词，前者强迫人类命名）。
3. **Eval 质量随时间衰减**（Part 9）—— 这是 [[Agent Reliability vs Capability]] 的"reliability decay curve"在 eval 层的对偶；与 [[ESAA]] 的 "deterministic replay" 不直接相关，但揭示了 "**static eval = silent regression 制造者**"。
4. **Trajectory 步骤评分（Part 10）= [[Trajectory Handoff]] 的官方依据**——Madhuguru 用"两个 42 trajectory 的对比"案例把"step-level evaluation"从抽象概念推到实操。两者在同一时间窗口（2026-09）独立提出同一论点，证据强度高。

## 抓取与限制

- 每篇通过 curl 抓取 X SSR HTML，无登录即可拿到 `<h1 class="sr-only">` 中的完整正文（不受 280 字截断影响）
- 书签数（bookmarks）通常为空——未登录态不显示
- 互动数字随时间变化，本快照反映 2026-09-13 抓取瞬间
- Part 1-2 标题为 "prologue"（Madhu 自标），Part 3-10 才是正文
