---
title: "多模型协作超过单强模型：正面证据合集（MoA / Blending / More Agents / Debate / Self-Consistency）"
kind: paper-collection
created: 2026-07-09
arxiv: ["2406.04692", "2401.02994", "2402.05120", "2305.14325", "2203.11171"]
tags: [multi-model, ensemble, mixture-of-agents, debate, self-consistency, blending]
---

# 多模型协作超过单强模型：正面证据合集

> 命题：多个"中等"或较弱的大模型协作（聚合 / 投票 / 辩论 / blending），能否在性能上超过单个更强的模型（如 GPT-4 / ChatGPT）？
> 本文件汇集 5 篇给出"能"的实证论文。配套反面证据见 `raw/papers/2026-07-09-llm-debate-failure-modes.md`。

## 1. Mixture-of-Agents (MoA) — arXiv:2406.04692

- **出处**：ICLR 2025 Spotlight。Junlin Wang (Duke) / Jue Wang, Ben Athiwaratkun, Ce Zhang (Together AI) / James Zou (Stanford)。
- **官方博客**：<https://www.together.ai/blog/together-moa>；代码 <https://github.com/togethercomputer/moa>。

**核心方法**：分层架构。每层含多个 LLM agent，每个 agent 把上一层所有 agent 的输出作为辅助信息生成回答。角色分两类：
- **Proposers**：生成初始参考回答，提供多样化视角。
- **Aggregators**：把多个 proposer 的回答综合成单一高质量回答。

**关键数据**：仅用开源模型，MoA 在 AlpacaEval 2.0 达 **65.1%**，超过 **GPT-4o 的 57.5%**；在 Arena-Hard / MT-Bench / FLASK 同样超越 GPT-4o。

**核心洞察**：作者提出 **"collaborativeness of LLMs"**——一个 LLM 在看到其他模型（哪怕更弱的）的输出后，倾向于生成更好的回答。6 个模型作为 aggregator 时 LC win rate 均显著提升，即便辅助回答质量低于模型独立水平。

**与命题的关系**：最直接的正面证据。但注意 MoA 的架构是**聚合**（proposer→aggregator 分层），不是简单辩论；其 collaborativeness 现象暗示**异构模型互补**比同质堆叠更有效。

## 2. Blending Is All You Need — arXiv:2401.02994

- **出处**：Marc Pucci 等，Cambridge / UCL。
- **HTML**：<https://arxiv.org/html/2401.02994v3>。

**核心方法**：**Blending**——每一轮**随机均匀**地从一组 chat AI 中选一个生成回答。生成的回答依赖之前所有回答，从而隐式影响后续。理论上近似从真实 ensemble 分布中采样。

**关键数据**：在 CHAI 平台的真实用户 A/B 测试中，**三个 6–13B 参数模型的 blend**，在用户参与度与留存上**超过 OpenAI 175B+ 的 ChatGPT**——而推理成本与显存只是后者的一小部分。

**与命题的关系**：**最贴合"几个中等模型协作超过单强模型"的实证**。而且是开放式对话任务（无明确 ground truth）、靠真实用户留存衡量——与 MoA 的 benchmark 场景互补。机制是"随机轮替近似 ensemble 分布"，而非择优或辩论。

## 3. More Agents Is All You Need — arXiv:2402.05120

- **出处**：TMLR 2024。Junyou Li / Qin Zhang / Yangbin Yu / Qiang Fu / Deheng Ye，Tencent。
- **代码**：<https://github.com/MoreAgentsIsAllYouNeed/More-Agents-Is-All-You-Need>（"Agent Forest"）。

**核心方法**：最简单的 **sampling-and-voting**——对同一 query 让 LLM 生成 N 次，投票取多数。论文称之为"Agent Forest"（致敬 Random Forest）。

**关键数据**：性能随 agent 数量（采样数）**单调提升**，且与现有复杂方法正交。GSM8K 上：**Llama2-13B 在 ensemble size=15 时达到 Llama2-70B 的水平**；Llama2-70B / GPT-3.5-Turbo 在 ensemble=15/20 时追平各自更强的对应版本。

**核心洞察**：**增强程度与任务难度正相关**——任务越难，堆 agent 的边际收益越大；简单任务收益很小。

**与命题的关系**：证明"堆数量"本身（哪怕同一模型多次采样）就能提升，且能缩小弱模型与强模型的差距。关键限制：收益与任务难度绑定，本质是降低随机性而非涌现新能力。

## 4. Improving Factuality and Reasoning through Multiagent Debate — arXiv:2305.14325

- **出处**：ICML 2024。Yilun Du / Shuang Li / Antonio Torralba / Joshua Tenenbaum / Igor Mordatch（MIT / Stanford）。
- **项目页**：<https://composable-models.github.io/llm_debate/>。

**核心方法**：多个 LLM 实例各自生成候选答案，然后**多轮互相批判与修正**，最终收敛到共同答案。灵感来自 Minsky 的"Society of Mind"。

**关键数据**：在 6 个推理 / 事实性 benchmark 上超越 zero-shot CoT、reflection 等单 agent baseline。性能随 agent 数与轮数提升。

**核心洞察**：**ChatGPT + Bard 跨模型辩论**能解出两者单独都解不出的 GSM8K 难题——一个模型的强势领域能补偿另一个的弱势。

**与命题的关系**：辩论架构（非聚合）的奠基性正面证据。跨模型辩论比同模型辩论更强，再次指向**异构互补**。

## 5. Self-Consistency Improves Chain of Thought Reasoning — arXiv:2203.11171

- **出处**：ICLR 2023。Xuezhi Wang / Jason Wei / Dale Schuurmans / Quoc Le / Ed Chi / Sharan Narang / Aakanksha Chowdhery / Denny Zhou，Google Research。
- **PDF**：<https://openreview.net/pdf?id=1PL1NIMMrw>。

**核心方法**：**sample-and-marginalize**——对 CoT prompting 采样多条推理路径，选最一致的答案（多数答案）。取代贪婪解码。

**关键数据**：GSM8K +17.9%、SVAMP +11.0%、AQuA +12.2%、StrategyQA +6.4%、ARC-challenge +3.9%。

**与命题的关系**：奠基性工作，是 More Agents / Debate 的概念前身。核心直觉：复杂问题有多条通往正确答案的路径，多条路径收敛 = 更可信。

---

## 横向归纳（正面证据的共同机制）

| 机制 | 代表论文 | 本质 |
|------|---------|------|
| 多次采样 + 投票 / 取一致 | Self-Consistency, More Agents | 降低单次随机性，**提升可靠性** |
| 多模型聚合 | MoA, Blending | 异构互补，**扩大能力面** |
| 多轮辩论收敛 | Du Debate | 互相纠错，**逼近更优解** |

> 三种机制都成立，但 2025 年的反面证据表明：它们的有效性高度依赖**任务类型、模型异构性、与 test-time compute 的公平比较**。见反面合集。
