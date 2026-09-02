---
title: "Context Engineering"
type: concept
created: 2026-06-24
updated: 2026-09-02
sources: ["raw/articles/2026-06-24-langchain-context-engineering.md", "raw/articles/2026-06-23-karpathy-context-engineering.md", "raw/articles/2026-06-24-bockeler-harness-engineering.md", "raw/articles/2026-06-24-anthropic-effective-context-engineering.md", "raw/articles/2026-06-24-google-adk-context-stack.md", "raw/articles/2026-06-24-openai-harness-engineering-codex.md", "raw/articles/46-context-engineering-claude-5-generation.md"]
tags: [context-engineering, prompt-engineering, context-window, write-select-compress-isolate, kv-cache, context-failure-modes, langchain, karpathy, anthropic, google-adk, openai, context-rot, compiled-view, just-in-time]
---

# Context Engineering（上下文工程）

> **context engineering 是 prompt engineering 的自然演进：不是"写好指令"，而是"管好整个 context window——决定每一步把什么信息放进 LLM 的'工作记忆'"。** LLM = CPU，context window = RAM，context engineering 扮演 OS 管理 RAM 的角色。

## 定义

> "Context engineering is the art and science of filling the context window with just the right information at each step of an agent's trajectory." —— Karpathy

来源：Karpathy（2025-06 公开背书术语）；LangChain *Context Engineering for Agents*（2025-07，四策略一手来源）；Anthropic *Effective context engineering for AI agents*。

## 为何不是 prompt engineering

prompt engineering 关注"写好并组织 LLM 指令"。context engineering 把范围扩到**整个 context window 的所有信息源**：

| Context 类型 | 内容 |
|---|---|
| **Instructions** | prompts、memories、few-shot examples、tool descriptions |
| **Knowledge** | facts、memories、RAG 检索结果 |
| **Tools** | tool call 的 feedback |

> "Context engineering is just one small piece of an emerging thick layer of non-trivial software that coordinates individual LLM calls." —— Karpathy

即：context engineering 是 agent harness 那层"非平凡软件"的一小片——见 [[12-Factor Agents]]、[[Harness Cybernetics]]。

## 四种 context 失败模式

长程 agent 累积 token → context 膨胀 → 四种退化（Drew Breunist）：

| 失败模式 | 含义 |
|---|---|
| **Context Poisoning** | 幻觉混入 context，后续基于错误前提推理 |
| **Context Distraction** | context 信息量压过模型训练，注意力分散 |
| **Context Confusion** | 多余/无关 context 影响响应 |
| **Context Clash** | context 各部分相互矛盾 |

这四种是 [[Agent Reliability vs Capability]] 里 non-determinism 的具体来源——reliability decay 不只是步数累积，也是 context 退化。

## 四策略（核心贡献 · LangChain）

| 策略 | 做什么 | 典型实现 | 本仓库对应 |
|---|---|---|---|
| **Write** | 把信息**保存到 context window 之外**，需要时再调 | 持久化记忆、外部存储、[[Agent Memory]] | [[Agent Memory]] |
| **Select** | 把信息**适时拉进 context window** | RAG、按步检索 | — |
| **Compress** | 只保留执行任务所需 token | 摘要、tool result clearing、自动压缩 | Claude Code 95% 自动压缩 |
| **Isolate** | 拆分 context，子任务用新窗口 | 子 agent 独立 context window | [[Claude Code Subagent]] |

## 三巨头第一方深化（认知地基 / 系统地基 / 操作策略）

LangChain 四策略是**操作层**。Anthropic、Google、OpenAI 各自补了一层更深的基底，三者互补：

### Anthropic：认知科学地基（context rot + attention budget）

Anthropic *Effective context engineering*（2025-09）给四策略一个**为什么**：

- **Context rot**（Chroma 研究）：context window token 数增加 → recall 准确率下降，**所有模型都如此**。context 是有限资源、边际收益递减，性能梯度而非硬悬崖
- 机理：Transformer 每 token attend 每 token → n² pairwise 关系，context 变长关系被拉伸变薄；训练数据短序列多于长序列
- → 好 context engineering = 找**最小可能的高信号 token 集**
- **Just-in-time**：维护轻量标识符（file paths / stored queries / web links），运行时用 tool 动态加载（= Select 策略）。Claude Code 写 targeted query + head/tail 分析大库不全载入
- **Progressive disclosure**：agent 通过探索增量发现 context（文件大小暗示复杂度、命名暗示用途）= Isolate 策略
- **Hybrid**（Claude Code）：CLAUDE.md 预加载 + glob/grep just-in-time

context rot 直接给 [[Agent Reliability vs Capability]] 的 reliability decay 提供微观机制——长程退化不只是步数累积，更是 context 膨胀导致 attention 稀释。

### Google ADK：系统级地基（context as compiled view）

Google *Architecting efficient context-aware multi-agent framework*（2025-12）提出比四策略高一层抽象：

> "Context is a **compiled view** over a richer stateful system."

context 不是 mutable string buffer，而是从 durable state 编译出来的视图。三原则：
- **Separate storage from presentation** — durable state（Session log）vs per-call view（working context），独立演化
- **Explicit transformations** — 命名有序 processors 构建context（非 ad-hoc 拼接），可观测可测试
- **Scope by default** — 每次调用只看最小 context，显式 reach 更多

四层 tiered model：**Working context**（编译视图）/ **Session**（durable log）/ **Memory**（可搜索知识）/ **Artifacts**（大二进制按名+版本寻址，不塞 prompt）。

→ LangChain 四策略是这个 compiler pipeline 里的具体 pass。Google 给四策略一个**系统级容器**。Session as durable log 直接对接 [[Stateless Reducer]] / [[ESAA]]。

### OpenAI：操作信条（map, not manual）

OpenAI *Harness engineering*（2026-05）从实战给出 context 工程的四条反模式：

> "give Codex a map, not a 1,000-page instruction manual."

- **Context is a scarce resource** —— 巨型指令文件挤占任务/代码/docs
- **Too much guidance becomes non-guidance** —— 当一切"重要"，没有重要的；agent 局部 pattern-match 而非有意导航
- **It rots instantly** —— 单体手册变陈规坟场（= context rot 的工程表现）
- **It's hard to verify** —— 单 blob 无法机械检查

→ AGENTS.md 当**目录**（~100 行）不当百科；`docs/` 是 system of record；doc-gardening agent 定期扫陈旧文档。这印证 Anthropic 的 progressive disclosure + Isolate 策略。

### 三者关系

| 层 | 来源 | 贡献 |
|---|---|---|
| 认知地基 | Anthropic | context rot、attention budget、just-in-time、progressive disclosure |
| 系统地基 | Google | compiled view、四层 tiered model、processors pipeline |
| 操作策略 | LangChain | write/select/compress/isolate 四策略 |
| 操作信条 | OpenAI | map-not-manual、四反模式 |

## Anthropic 2026-07：Claude 5 代模型的新规则（模型代际实证）

Anthropic 官方（Thariq Shihipar，[[The New Rules of Context Engineering for Claude 5 Generation Models]]）：对 Claude 5 代模型（Opus 5 / Fable 5）**删除 Claude Code system prompt 的 80%+，编码评估无可测量损失**。核心病症是 **overconstraint**——system prompt、skills、CLAUDE.md 与用户请求互相冲突，模型被迫费力调和（= Context Clash 的官方自认实例）。本篇给 progressive disclosure 补上了**模型代际维度**：上下文策略不是静态最佳实践，而是随模型判断力增长需要持续解约束的动态平衡。

六组 Then→Now：规则→判断力（"match surrounding code"取代注释禁令）；示例→接口设计（工具枚举自解释，示例反而收窄探索空间）；全部前置→progressive disclosure（验证/评审移入独立 skills、工具 deferred loading 需 ToolSearch 取全定义、CLAUDE.md 应为按需加载的文件树）；重复强调→只写 tool description；CLAUDE.md 记忆→auto-memory；简单 markdown spec→rich references（测试套件/HTML artifact/rubric + verifier agents）。配套 `/doctor` 命令自动 rightsizing（见 [[Thin Harness, Fat Skills]]）。

对 memory scaffolds 损害长程 reliability（[[Agent Reliability vs Capability]]）的启示：Anthropic 的方向是**削减 scaffolds、归还判断力**——与"更多记忆结构"路线构成设计张力。

## 与 KV Cache 命中率（scope 边界内的切入）

KV Cache（Transformer 注意力层缓存）本身是模型推理基础设施，**属本仓库 scope 之外**。但 harness 侧的 context engineering 直接影响它——这是正确的切入角度：

- 缓存 token 成本约 $0.30/百万 vs 未缓存 $3/百万（Manus 团队列为最重要成本指标）
- **动态增删工具会破坏前缀缓存** → 应改用 logit masking（见 [[12-Factor Agents]] Factor 4 tools as structured outputs）
- Compress 策略（tool result clearing、上下文压缩）既是 context engineering 也是维持 KV 命中率的手段

即：不建 KV Cache 概念页，但在 context engineering 里以"维持前缀缓存命中率"的角度处理——那是 harness 侧决策，不是模型机理。

## 与 Harness Cybernetics 的交叉

context injection（注入 repo state、recent diffs、task constraints）是 [[Harness Cybernetics]] 的 **feedforward control**——行动前塑造 agent 能看到什么。context engineering 的 Select/Write 策略就是 feedforward 的信息填充手段。

两者关系（Böckeler sidebar）：harness engineering 关注**控制结构**（前馈/反馈），context engineering 关注**信息填充**。交叉但不等同——一个 feedforward guide 可以是纯结构约束（tool allowlist，无信息），也可以是信息注入（context injection）。

## 与现有 wiki 概念的关系

| 关联 | 说明 |
|---|---|
| 12-Factor Agents | Factor 3（own your context window）是 context engineering 的方法论化；Factor 4（tools as structured outputs）兼顾 KV 命中率 |
| Harness Cybernetics | Select/Write 是 feedforward 的信息填充；context 四失败模式是 feedback sensor 要检测的退化 |
| Agent Memory | Write 策略的载体；长程 reliability 要求遗忘机制（见 Agent Reliability vs Capability：memory scaffolds 普遍损害长程 reliability） |
| [[Claude Code Subagent]] | Isolate 策略的实例（独立 context window 避免主上下文污染） |
| Agent Reliability vs Capability | context 四失败模式是 reliability decay 的微观机制 |
| [[Stateless Reducer]] | reducer 的 context 全进 log → Compress/Write 策略可重放 |

## 落地含义

- **优化 tool response 而非 system prompt**：Manus 数据 tool responses 占 67.6% token，system prompt 仅 3.4%——优化前者比后者有效约 20×
- **Isolate 优先于 Compress**：子 agent 隔离比压缩更彻底地解决 Context Distraction/Clash
- **95% 触发自动压缩**：Claude Code 实践，避免硬溢出
- **维持前缀缓存**：别动态增删工具，用 logit masking；定期 tool result clearing
- **写 context 像写代码**：context 是 harness 的一等公民，版本化、测试、迭代（呼应 12-Factor Agents Factor 2/3）
