# Purpose

> 这个 wiki **为什么存在**。区别于 `CLAUDE.md`（怎么运作的 schema），这里是方向意图——目标、核心论点、研究范围、演化方向。LLM 每次 ingest/query 应读此文件获取方向上下文。

## 目标

研究 Agent 平台与基础设施层，并把研究的概念**反哺为可执行的工程机制**。

研究是手段，不是目的——概念若不落地为可跑的脚本/hook/流程，就是文档债。这条原则本身是 2026-06-24 一次质量检查的教训：研究了全套治理概念，却连一个 hook 都没挂上，重复链接静默积累了 80 个。

## 核心论点（evolving thesis）

1. **套具比模型重要** — Claude Code 98.4% 是基础设施、仅 1.6% 是 AI 决策（[[Dive into Claude Code（论文）]]）；Cline 纯靠 harness 优化 +10pp（[[Cline]]）。价值累积在 outer harness。
2. **可靠性 ≠ 能力** — capability 问"能不能做到一次"，reliability 问"能不能次次做到"（[[Agent Reliability vs Capability]]）。frontier model 的 meltdown rate 反而更高（MOP paradox）。
3. **确定性优先** — deterministic feedback（exit code / diff / test）不可幻觉，优先于 LLM judge（[[Harness Cybernetics]]）。
4. **前馈+反馈对偶 / Ashby** — 每个失败模式必须有对应的前馈（预防）或反馈（自纠），否则逃逸（[[Harness Cybernetics]] Ashby's Law）。
5. **治理 > 单次体验** — 工具优化单次体验，治理协议解决跨 session / 跨 agent 的长期一致性（[[Agent Harness 治理协议]]）。

## 研究范围

- Agent 平台与基础设施层（Runtime / Multi-agent / Harness / 工具定义）
- Claude Code Skill 开发
- 多 Agent 协作架构
- Agent 治理协议（跨 session 一致性、事件溯源、概念演化、双层验证）
- 行业实践（MiniMax / Anthropic / NVIDIA / Cline / OpenAI / nashsu 等）

**刻意排除**：模型训练/微调细节、与 Agent 平台无关的纯应用层话题。

## 关键问题（精华，完整版见 CLAUDE.md "Open research questions"）

- Stateless reducer 的可重放性能否量化对冲 reliability decay？（[[Stateless Reducer]]）
- Harness 覆盖率（Ashby's Law）如何操作化为可度量指标？常见失败模式 × {前馈, 反馈} 覆盖矩阵如何系统构建？
- 三层心跳看门狗在真实多租户/容器化部署中，L0 常驻 shell guard 的开销如何量化？（[[Heartbeat Watchdog]]）
- 宏观评估的 `suspect_score` 权重能否跨 agent 系统重新校准？（[[Agent Macro Evaluation]]）

## 演化方向

**从纯研究 → 反哺工程。**

- **早期（2026-05 ~ 06）**：ingest 行业文章与论文，沉淀 concept / entity / summary 页，建立概念图谱。
- **转折（2026-06-24）**：发现"研究了概念却没工程化"的知行脱节——声称的 hook 从未配置、重复链接积累、文档与现实脱节。建立 `docs/wiki-governance-roadmap.md`，把研究的 [[Harness Cybernetics]] / [[Stateless Reducer]] / [[Heartbeat Watchdog]] 概念反哺为 wiki 自身的治理机制（8 个 lint 脚本 + Ashby 覆盖矩阵 + PostToolUse hook + 可回滚 ingest）。

**研究即工程**——这是打破知行脱节循环的唯一方式。判断一个概念是否真被"研究透了"的标准：它有没有变成一个可跑、可验证、防复发的机制。
