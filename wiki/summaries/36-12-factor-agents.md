---
title: "12-Factor Agents"
type: summary
created: 2026-06-23
updated: 2026-06-23
sources: ["raw/articles/2026-06-23-anthropic-building-effective-agents.md", "raw/articles/2026-06-23-openai-agents-sdk-human-in-the-loop.md", "raw/articles/2026-06-23-stateless-reducer-agent-pattern.md", "raw/articles/2026-06-23-karpathy-context-engineering.md"]
tags: [12-factor-agents, humanlayer, harness, agent-engineering, deterministic, context-engineering, hitl, reducer, dex-horthy]
---

# 12-Factor Agents

> 可靠 LLM 应用的工程原则。原始作者：Dex Horthy（@dexhorthy，HumanLayer）。仓库 humanlayer/12-factor-agents，仿 12-Factor Apps 体例，给出构建"可交付生产客户"的 LLM 应用的 12 条原则。

> 原始作者：Dex Horthy（@dexhorthy，HumanLayer）。仓库 humanlayer/12-factor-agents，仿 12-Factor Apps 体例，给出构建"可交付生产客户"的 LLM 应用的 12 条原则。

## 一句话主论点

> "Most products billing themselves as 'AI Agents' are not all that agentic. A lot of them are mostly deterministic code, with LLM steps sprinkled in at just the right points to make the experience truly magical."

**好 agent = 大部分确定性软件 + LLM 撒在关键点**，不是"一个 prompt + 一袋工具 + 循环到完成"。12 条都是这个论点的展开：把 LLM 之外的东西全部夺回来自己拥有。

## 80% 墙（为何需要这些原则）

作者观察到的 builder 通用路径：

1. 决定建 agent
2. 产品设计
3. 抓 `$FRAMEWORK` 快速开干
4. 做到 70-80% 质量线
5. 发现 80% 对面向客户的功能不够
6. 越过 80% 需要逆向工程框架的 prompt/flow
7. 从头重来

**80% 墙不是能力不够，是接缝失控**——见 [[Agent-Reliability-vs-Capability]]，capability 与 reliability 在此系统性背离。

## 12 条按五主题重组

原文编号是叙述顺序，非逻辑结构。这里按主题重组：

### 主题一：接缝定义

| Factor | 主张 |
|---|---|
| **1. Natural Language to Tool Calls** | LLM 的活就是输出"下一步是什么"的结构化 JSON。agent loop = `determine_next_step → execute → append to context → repeat` |
| **4. Tools are Structured Outputs** | 工具调用 = LLM 输出 JSON 触发确定性代码。"LLM 决定做什么，你的代码决定怎么做"——**接缝就在 selection 与 invocation 之间** |

### 主题二：夺回非 LLM 部分

| Factor | 主张 |
|---|---|
| **2. Own Your Prompts** | 别把 prompt 工程外包给框架。prompt 是一等公民代码，可测可迭代；框架的 role/goal/personality 黑盒难调到精确 token |
| **3. Own Your Context Window** | 不必用标准 message 格式喂上下文。自建 XML/YAML 格式可提升信息密度与 token 效率。即 context engineering——Karpathy 公开背书的术语 |
| **8. Own Your Control Flow** | 别让框架藏起循环。关键：在 tool **selection** 与 **invocation** 之间能打断 |

### 主题三：状态合一

| Factor | 主张 |
|---|---|
| **5. Unify Execution & Business State** | 执行状态（当前步/重试计数）和业务状态（消息历史/工具结果）别分开管，执行状态能从 context window 推导。一份 state → 可序列化/可 fork/可恢复 |
| **12. Make Your Agent a Stateless Reducer** | agent = `(context, event) → (context, action)` 纯 fold。非确定性隔离在唯一 LLM 调用里，其余全是确定性折叠。见 [[Stateless Reducer]] |

### 主题四：持久化 + 人在环

| Factor | 主张 |
|---|---|
| **6. Launch/Pause/Resume** | agent 就是个程序，要能简单启停续。webhook 续跑，不依赖 orchestrator 深度集成 |
| **7. Contact Humans with Tools** | 把"找人"也做成工具调用。`request_human_input` 和 `deploy_backend` 是同构 intent；Agent→Human 而非只有 Human→Agent |
| **11. Trigger from Anywhere** | slack/email/sms/cron 都能触发。outer-loop agent，跑 5–90 分钟到关键点再找人 |

### 主题五：错误与范围

| Factor | 主张 |
|---|---|
| **9. Compact Errors into Context** | 错误塞进 context 让 LLM 自愈；连续错误计数器 ~3 次封顶，超了升级给人或确定性接管 |
| **10. Small, Focused Agents** | 单 agent 3–20 步，别造巨石。上下文越长 LLM 越跑偏；agent 只是更大确定性系统里的一块 |

## 三个最深的概念

### 接缝位置被精确化（Factor 8）

接缝在 **tool selection 与 invocation 之间那一格**。能在这一格打断 = 能塞 human approval = 让 LLM 做概率决策、确定性代码做执行、人在中间签收。**OpenAI Agents SDK 官方 HITL** 是这一格的工业级实现：`needsApproval` → run 暂停 → 返回 `interruptions` → `RunState` 序列化 → `runner.run(agent, state)` 续跑。

### 第五种范式：状态确定性（Factor 5 + 12）

四种对付接缝的范式（压概率空间 / Verifier 循环 / 统计签收 / 确定性外移）都是"怎么对付接缝"。Factor 12 补正交一维：**让 LLM 成为整个管线里唯一的非确定节点**。状态全进 context、不藏可变变量 → 可重放 → reducer 是纯函数。见 [[Stateless Reducer]]。

### 贴边扩张（Factor 10）

> NotebookLM 团队："the most magical moments come about when I'm really just close to the edge of the model capability"

"能力评测"在 12-factor 里不是跑 benchmark，是找准这条边界并贴着它 intentional 地扩张 agent scope。但 [[Agent-Reliability-vs-Capability]] 的 MOP paradox 实证了反面：frontier model 追求野心多步策略，meltdown rate 反而最高（达 19%）——贴边走会越界。

## 术语张力：Workflow vs Agent（重要）

12-factor 把"大部分确定性代码 + LLM 撒关键点"称作 agent 的常态。但 **Anthropic 的 *Building Effective Agents* 明确二分**：

- **Workflow** — LLMs 在**预定义代码路径**中被编排
- **Agent** — LLMs **动态主导自身流程**与工具使用

12-factor 的核心论点在 Anthropic 体系里**精确对应 workflow，不是 agent**。Anthropic 认同 12-factor 的反框架立场（直接用 API、理解底层），但不会把"确定性代码为主"称作 agent。Anthropic 对真 agent 持更谨慎态度（"higher costs, potential for compounding errors, extensive testing in sandboxed environments"）。

**ingest 注意**：引用 12-factor 时"agent"一词需标注此滑动，不可当行业共识。

## 成色评估

**强：**
- 主论点清晰，与 [[Thin-Harness-Fat-Skills]]（反框架、自拥零件）、[[Agentic-Code-Review]]（接缝处 human-on-the-loop）、[[Agent-Harness-治理协议]]（事件时间线 ≈ reducer 事件流）强关联
- 接缝位置、stateless reducer、贴边扩张三个概念都 actionable
- 被权威来源交叉验证：OpenAI SDK 证实 Factor 7/8，agentpatternscatalog 形式化 Factor 12，Karpathy 背书 Factor 3 术语

**弱：**
- Factor 12 正文很薄（作者自承"mostly just for fun"，靠图）
- 全是 blog 级观点 + 轶事（"聊了 100 个 founder"），80% 是修辞不是测量
- 强反框架立场（"frameworks are evil"），Claude Code 本身就是框架
- Factor 7/11 带 humanlayer 产品 pitch（作者自承"If you're waiting for the humanlayer pitch, you made it"）
- TypeScript 中心、个人 brand 色彩重

## 关联 wiki

| 关联 | 说明 |
|---|---|
| [[Stateless Reducer]] | Factor 12 的形式化概念页 |
| [[Agent-Reliability-vs-Capability]] | 80% 墙与贴边扩张的学术级深化 |
| [[Thin-Harness-Fat-Skills]] | 同样反框架、主张自拥零件，立场接近 |
| [[Agentic-Code-Review]] | 接缝处 human-on-the-loop = Factor 7/8 |
| [[Agent-Harness-治理协议]] | 事件时间线 ≈ reducer 事件流 |
| [[ESAA]] | Event Sourcing 与 reducer 的 durable log 同构 |
| [[Agent-Macro-Evaluation]] | 事后群体诊断 vs 12-factor 事前贴边设计 |
