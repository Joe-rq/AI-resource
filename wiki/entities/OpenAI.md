---
title: OpenAI
type: entity
created: 2026-06-15
updated: 2026-06-15
sources: [raw/articles/2026-06-13-macro-evals-for-agentic-systems.md, raw/articles/2025-11-26-colin-jarvis-openai-fde.md, raw/refs/macro-evals-for-agentic-systems.md]
tags: [company, agent-platform, openai, gpt, codex, macro-evaluation]
---

# OpenAI

OpenAI 是由 Sam Altman 领导的 AI 研究公司，核心产品包括 GPT 系列模型、ChatGPT 和 API 平台。在 Agent 平台方面，OpenAI 布局三个层面：终端 CLI 工具（Codex CLI）、Agent SDK（Assistants API + Agents SDK）、评估方法论（OpenAI Cookbook）。其 Agent 架构的独特特点在于**接力式 Handoff 模式**——Agent 之间链式传递任务，每棒不回头，无内置对抗验证机制。

## Agent 平台方案

### Codex CLI

Codex CLI 是 OpenAI 于 2025 年发布的开源终端 Agent 工具，支持 o4-mini、GPT-5 等推理模型。它在本地终端环境中运行，将自然语言指令转化为代码执行，内置沙箱安全隔离机制。采用双重许可策略（开源但非完全开放），核心价值在于"自然语言到代码执行"的终端闭环。

### Handoff Pattern

OpenAI Agents SDK 的核心协作模式是接力式 Handoff：每个 Agent 完成任务后交给下一个 Agent，不支持回头修正。与 Anthropic 的 Orchestrator/Worker（Leader 评审、支持并行）和 MiniMax Mavis 的 Worker/Verifier 对抗循环（内置验证、自动打回重做）相比，OpenAI Handoff 追求简洁的链式传递，但天然缺乏并行能力和验证环节。上一棒输出即为下一棒输入，无物理拦截或状态机流转。详见 [[Multi-Agent 协作模式]]。

### Assistants API & Agents SDK

OpenAI 提供托管 Agent 运行时（Assistants API），包括 Code Interpreter（代码执行沙箱）、File Search（向量检索）和 Function Calling（工具调用）。通过 Threads 管理持久化上下文，支持多轮对话状态保持。

Agents SDK 在此基础上增加了 Agent 间 Handoff 原语：每个 Agent 可以定义 `handoff_description`，当编排器判断当前任务超出能力时，自动将上下文和控制权移交给下一个 Agent。Handoff 是单向的——被移交的 Agent 无法将任务退回，只能继续向前或终止。这种设计的哲学基础是"简化状态管理"：双向 Handoff 会引入状态回退、死锁检测和回滚逻辑，复杂度指数级上升。

### Codex 与 Loop Engineering

Codex 在 Addy Osmani 的 [[Loop Engineering：从 Prompt 到系统设计|Loop Engineering]] 框架中被视为与 Claude Code 能力等价的终端 Agent 工具——两者共享相同的 5+1 模块形状（Automations、Worktrees、Skills、MCP、Sub-agents、Memory）。Codex 通过 `.codex/agents/` 下 TOML 文件定义 Sub-agent，内置 `/goal` 条件循环原语（由独立小模型检查停止条件），支持多 worktree 并行操作同一 repo。Codex 的 Automation 功能支持定时触发、Triage inbox 分流和自动归档，OpenAI 内部将其用于 issue 分类、CI 失败摘要、commit briefing 等日常自动化场景。

## 宏观评估方法论

2026 年 5 月，OpenAI Cookbook 发布了"Macro Evals for Agentic Systems"——这是 OpenAI 首次将**评估方法论本身**抬升到 Agent 系统设计层。作者 Shikhar Kwatra (OpenAI)、Will Thieme、Bradley Strauss 提出了从单次评分转向群体行为模式分析的范式：

- **底层评估**：Promptfoo 对每次运行打 5 类 rubric 分（决策质量、政策合规、路由激活、市场感知、复核适当性）
- **宏观聚类**：BERTopic 风格（UMAP 降维 + HDBSCAN 聚类 + class-aware tf-idf）发现反复出现的 `behavior_pattern`
- **诊断回溯**：AgentTrace 风格嫌疑节点评分（$suspect\\_score = 0.4 \\cdot proximity + 0.3 \\cdot frequency + 0.2 \\cdot bridge + 0.1 \\cdot role$）

案例使用 EV 订单处理多 Agent 系统（定价/合规/供应/工厂路由/排期/客户沟通/放行审查），1000 次合成运行产生 992 个可分析 trace bundle。详见 [[Agent Macro Evaluation]]。

## 与其他方案的架构差异

| 方案 | 验证方式 | 协作模式 | 并行能力 |
|------|----------|----------|----------|
| OpenAI Handoff | 无验证环节 | 接力式链式传递 | 天然不支持 |
| Anthropic Multi-Agent | Lead Agent 评审 | Orchestrator/Worker | 支持并行 Subagent |
| MiniMax Mavis | Worker/Verifier 对抗 | Team Engine 状态机调度 | 分组并行+独立验证 |

OpenAI Handoff 的核心取舍：牺牲验证安全换取架构简洁性。在需要严格质量保证的场景（代码审查、合规检查），Handoff 模式缺乏内置纠偏机制；但在线性任务流水线场景（数据预处理 -> 分析 -> 报告生成），链式传递足够高效。Anthropic 和 Mavis 分别通过 Leader 评审和对抗循环解决了验证问题，但引入了额外的协调开销。

更深层看，三种方案代表了三种 Agent 系统哲学：OpenAI 追求"无状态接力"（最小化协调成本），Anthropic 追求"中央评审"（Lead Agent 作为质量闸门），Mavis 追求"对抗制衡"（结构性的质量对抗）。三种哲学没有绝对优劣——OpenAI Handoff 在简单流水线中效率最高，Mavis Worker/Verifier 在高风险场景下安全性最强，Anthropic Orchestrator 在灵活性和可控性之间取中。

OpenAI 也有 FDE（前置部署工程）实践——Colin Jarvis 领导的 FDE 团队强调"信任、产品、影响"三支柱，将 Agent 能力嵌入客户工作流。详见 [[Forward-Deployed-Engineering]]。

## Related concepts

- [[Agent Macro Evaluation]] -- OpenAI Cookbook 宏观评估方法论的完整 concept 页
- [[Multi-Agent 协作模式]] -- Handoff 作为四种核心协作模式之一
- [[Worker Verifier 对抗循环]] -- 对比：Mavis 有内置对抗验证，OpenAI Handoff 无
- [[Forward-Deployed-Engineering]] -- OpenAI FDE 实践（Colin Jarvis 访谈）
- [[ESAA]] -- Event Sourcing 可为 Handoff 链路提供不可变审计追溯

## Sources

- OpenAI Cookbook: [Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems) (2026-05-19)
- OpenAI Codex CLI: [github.com/openai/codex-cli](https://github.com/openai/codex-cli)
- OpenAI Assistants API: [platform.openai.com/docs/assistants](https://platform.openai.com/docs/assistants)
