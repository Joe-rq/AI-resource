---
title: "Harness Cybernetics"
type: concept
created: 2026-06-24
updated: 2026-06-24
sources: ["raw/articles/2026-06-24-bockeler-harness-engineering.md", "raw/articles/2026-06-24-outer-harness-inner-harness.md", "raw/articles/2026-06-24-anthropic-effective-harnesses-long-running.md", "raw/articles/2026-06-24-openai-harness-engineering-codex.md"]
tags: [harness, cybernetics, feedforward, feedback, guides, sensors, control-loop, inner-outer-harness, ashbys-law, bockeler, deterministic-feedback, anthropic, openai, initializer-agent]
---

# Harness Cybernetics（Harness 控制论：前馈引导与反馈传感器）

> **agent harness 是一个控制论调节器（cybernetic governor）：用前馈（行动前注入约束）+ 反馈（行动后感知结果）的组合，把 non-deterministic LLM 的产出调节向期望状态。** —— 把本仓库散落的 Quarantine/Agentic-Code-Review/Worker-Verifier 等概念归位到一个统一对偶框架。

## 核心对偶：Feedforward vs Feedback

来源：Birgitta Böckeler（Thoughtworks），*Harness engineering for coding agent users*（martinfowler.com, 2026-04）。

| | Feedforward（前馈 · Guides） | Feedback（反馈 · Sensors） |
|---|---|---|
| **时机** | agent 行动**之前** | agent 行动**之后** |
| **作用** | 预期不想要的输出，尝试预防 | 观察结果，帮 agent 自我纠正 |
| **目标** | 提高首次正确率 | 提供自纠正回路 |
| **本仓库对应** | [[Quarantine Mode]]、tool allowlist、CLAUDE.md、system prompt 约束、[[Claude Code Skills]] | [[Agentic Code Review]]、[[Worker Verifier 对抗循环]]、静态分析、测试、日志 |

> "Separately, you get either an agent that keeps repeating the same mistakes (feedback-only) or an agent that encodes rules but never finds out whether they worked (feed-forward-only)." —— Böckeler

**只有反馈 → 反复犯同样错误；只有前馈 → 编码了规则却不知是否生效。两者必须结合。** 这是本仓库此前缺的正交对偶——Feedback 侧概念丰富（13 处），Feedforward 侧概念存在（[[Quarantine Mode]] 等）却从未被归到"前馈"名下，更没有把两侧对偶成一个框架。

## 正交第二维：Computational vs Inferential

前馈/反馈各自又分两种执行类型，形成 2×2：

| | Computational（确定性 · CPU） | Inferential（语义 · LLM judge） |
|---|---|---|
| **Feedforward** | codemods（OpenRewrite）、bootstrap script | AGENTS.md、Skills、编码规范 |
| **Feedback** | linter、type checker、ArchUnit 结构测试、测试通过率 | AI code review、"LLM as judge" |

- **Computational** — 毫秒到秒，结果可靠，便宜到每次变更都跑
- **Inferential** — 慢、贵、non-deterministic，但能提供丰富引导与语义判断

**选型含义**：能用 Computational 解决就别用 Inferential（可靠性 + 成本）。Inferential 只在需要语义判断时用，且配强模型。

## The Steering Loop（人的工作）

> "The human's job is to **steer** the agent by iterating on the harness. Whenever an issue happens multiple times, the feedforward and feedback controls should be improved."

问题反复出现 → 不是改 prompt，是改 harness：把它变成 feedforward（预防）或 feedback（自纠正）。coding agent 让构建自定义控制更便宜——agent 帮写结构测试、生成规则草稿、scaffold linter、从代码考古生成 how-to。

这与 [[Thin Harness, Fat Skills]] 的 self-rewriting skill loop 同构：harness 本身是被迭代的外部状态。

## Inner Harness vs Outer Harness

来源：codeongrass, *The Outer Harness*。

- **Inner harness** — agent runtime 本身：LLM + tool execution loop + SDK。Claude Code / Codex / Open Code 都是 inner harness，结构快速收敛趋同、**正在商品化**。
- **Outer harness** — 围绕 agent 建的控制面，inner harness 默认不带的一切：

| Outer harness 组件 | 作用 | 本仓库对应 |
|---|---|---|
| Session persistence | 睡眠/断网时保持 alive 且可恢复 | [[Stateless Reducer]] |
| Feedforward controls | 执行前约束 action space | [[Quarantine Mode]]、CLAUDE.md |
| Feedback controls | 执行后/中观察与信号浮现 | [[Agentic Code Review]] |
| Multi-surface dispatch | 不同 surface 访问同一 session | — |

> "The agent layer runs code. It doesn't manage sessions, surface permission requests, persist state across sleep cycles, or dispatch work across surfaces. Those problems live above it."

[[12-Factor Agents]] 的"own your prompts/context/control-flow"系列，own 的正是 outer harness。**价值累积在 outer harness，因为那是你必须自己建的部分。**

### Deterministic feedback（关键子类型）

> "deterministic feedback — output from tool execution rather than LLM interpretation. A bash exit code. A file diff. A test runner pass/fail. The most reliable signals because they **can't be hallucinated**."

完整 outer harness 栈：feedforward 约束 action space → 执行 → **deterministic feedback 验证实际发生** → LLM-synthesized feedback 浮现状态给人。

deterministic feedback 不可幻觉 → 直接对冲 [[Agent Reliability vs Capability]] 的 non-determinism。这也是 [[Worker Verifier 对抗循环]] 里 Verifier 应优先用确定性检查而非 LLM judge 的依据。

## 第一方实证：三巨头如何落地这个框架

Böckeler 的控制论框架不是分析师空想——Anthropic、OpenAI 的第一方工程文章各自独立印证，且都明确用 control system 语言。

### Anthropic：initializer + coding agent = feedforward/feedback 分工

Anthropic *Effective harnesses for long-running agents*（2025-11）把 Claude Agent SDK 明确称作 "agent harness"，其长程方案恰好是前馈/反馈的分工：

| Anthropic 实践 | 控制论位置 |
|---|---|
| initializer agent 建 `init.sh` + feature_list.json（>200 features 初始全标 failing） | **Feedforward**（约束做什么） |
| `passes` 字段 + 强指令禁止编辑测试 | **Feedback · deterministic** |
| git 回退坏改动 | **Feedback**（自纠正） |
| Puppeteer MCP 端到端测试 | **Feedback · deterministic**（不可幻觉） |

> 两种失效模式也精准对应：(a) one-shot 倾向 = 缺增量约束（feedforward 不足）；(b) 提前宣布完成 = 缺确定性反馈（feedback 不足）。

### OpenAI："Humans steer. Agents execute." + control systems

OpenAI *Harness engineering: leveraging Codex*（Ryan Lopopolo, 2026-05）记录 0 行手写代码、百万行、1500 PR 的实验，结尾明确：

> "Our most difficult challenges now center on **designing environments, feedback loops, and control systems**."

| OpenAI 实践 | 控制论位置 |
|---|---|
| strict layered architecture + custom linters + taste invariants | **Feedforward · computational** |
| Ralph Wiggum Loop（agent-to-agent review） | **Feedback · inferential** |
| **lint error message 注入 remediation instructions** | **Feedback · LLM-optimised sensor**（= Böckeler 的 positive prompt injection） |
| Chrome DevTools / LogQL / PromQL | **Feedback · deterministic** |
| golden principles + doc-gardening agent | **steering loop**（人编码 taste → 机械持续执行） |

> OpenAI 的关键观察印证 Ashby：agent 复制既有模式（含次优）→ drift，必须把 taste 编码成 mechanical invariants 才能"处处适用"（multiplier）。

### 印证要点

三篇文章（Böckeler 分析框架 + Anthropic/OpenAI 第一方实证）收敛到同一结论：**好 harness = feedforward（约束 action space）+ deterministic feedback（验证实际发生）+ steering loop（人迭代 harness 本身）**。Inferential feedback（LLM judge）是补充而非主力——优先级低于 deterministic。

## Ashby's Law（必要多样性定律）

控制论经典（Böckeler sidebar）：**控制系统的复杂度必须匹配被控系统。** harness 语境——要可靠控制 non-deterministic LLM 的产出空间，harness 的"调节多样性"（feedforward+feedback 的覆盖度）必须足够。

这给出"harness 覆盖率"的操作化定义：常见失败模式是否都有对应的 feedforward（预防）或 feedback（自纠正）？没有 = Ashby 违例 = 该失败模式会逃逸。

## 传感器的盲区（诚实）

Böckeler 指出 maintainability harness 的传感器并非万能：

- Computational sensors 可靠抓**结构**问题（重复代码、圈复杂度、覆盖缺口、架构漂移、风格）
- LLM 能部分处理**语义**问题（语义重复、冗余测试、暴力修复、过度工程）但贵且概率性
- **高影响问题两者都不可靠抓**：误诊、过度工程、不必要功能、误解指令
- **正确性超出任何传感器能力**——若人没先说清想要什么（intent reconstruction，见 [[Agentic Code Review]]）

即：harness 控制论能压缩但不能消除 [[Agent Reliability vs Capability]] 的 reliability gap，尤其语义/意图层。

## 与现有 wiki 概念的关系（归位）

| 本仓库概念 | 在控制论框架中的位置 |
|---|---|
| [[Quarantine Mode]] | Feedforward（行动前结构隔离） |
| [[Agentic Code Review]] | Feedback（Inferential sensor + human-on-the-loop approval gate） |
| [[Worker Verifier 对抗循环]] | Feedback（Verifier 优先 deterministic） |
| [[Claude Code Skills]] | Feedforward（Inferential guide） |
| [[Thin Harness, Fat Skills]] | steering loop 的实例（skill = 可迭代 harness） |
| [[Stateless Reducer]] | outer harness 的 session persistence 底层 |
| [[12-Factor Agents]] | own your outer harness 的方法论 |
| [[Agent Reliability vs Capability]] | harness 控制论要压缩的 gap（但语义层有盲区） |
| [[Context Engineering]] | 与 feedforward 交叉——context injection 是 feedforward control |
| 第一方印证 | Anthropic effective harnesses（initializer/coding 分工）+ OpenAI Codex harness（steer/execute、lint remediation）独立实证此框架 |

## 落地含义

- **别只堆 feedback**：多数团队 underinvest feedforward，靠 feedback 去抓 agent 做错的事；更干净的修法是约束它被允许尝试什么
- **优先 Computational**：能用 linter/type/test 解决别用 LLM judge
- **deterministic feedback 优先**：Verifier 用 exit code/diff/test，不用 LLM 解释
- **steering 而非 prompting**：问题反复出现改 harness，不改 prompt
- **Ashby 检查**：每个常见失败模式都要有对应的 feedforward 或 feedback，否则逃逸
