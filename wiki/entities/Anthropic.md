---
title: Anthropic
type: entity
created: 2026-06-15
updated: 2026-06-15
sources:
  - raw/articles/2026-05-19-anthropic-multi-agent-research-system.md
  - raw/articles/2026-05-19-anthropic-managed-agents-api.md
  - raw/articles/2026-05-19-claude-code-agent-teams.md
tags:
  - company
  - agent-platform
  - anthropic
  - claude
  - multi-agent
---

# Anthropic

Anthropic 是一家 AI 安全公司，由前 OpenAI 成员 Dario Amodei 和 Daniela Amodei 于 2021 年创立。公司以 **safety-first** 为核心定位，旗下 Claude 系列模型在推理、编码、长上下文处理方面位居前沿。在 Agent 平台和 Multi-Agent 架构方面，Anthropic 提供了三套互补的技术方案——Orchestrator-Worker 研究系统、Managed Agents API、Claude Code Agent Teams——覆盖从研究实验到生产 API 再到开发者 CLI 的全场景。2026 年 6 月推出的 Dynamic Workflows 概念进一步将架构哲学提炼为：让 Claude 按任务即时生成定制 harness，将 [[Thin Harness, Fat Skills]] 原则推到极致。

## Agent 平台产品矩阵

### Claude Code

Claude Code 是 Anthropic 面向开发者的 CLI Agent 工具，也是本 wiki 知识体系的核心锚点之一。支持 [[Claude Code Subagent]]（独立上下文工作者）、[[Claude Code Skills]]（动态上下文注入与能力扩展）、Agent Teams（多 Agent 并行协作）三层能力。内置 Explore（Haiku，只读）、Plan（inherit，只读）、General-purpose（inherit，全工具）三种 subagent，并通过 `/agents` 命令支持用户自定义 subagent 的模型、工具集、持久内存。其 **deny-first 权限系统** 在所有工具调用前先拦截，仅在显式 allow 规则匹配时放行，是 Anthropic safety-first 哲学在开发者工具层面的直接体现。2026 年 6 月推出的 Dynamic Workflows 功能（`/ultracode`、`/deep-research` 等 slash command）将 Claude Code 从单 session 工具升级为可动态生成多 agent 编排 harness 的平台。

### Agent SDK

Anthropic 的 Agent SDK（Claude Agent SDK）提供编程化 Agent 构建能力。支持 tool use、extended thinking、computer use 等底层原语，开发者可通过 SDK 定义 Agent 的 system prompt、工具集、模型选择，构建定制化 Agent 应用。与 Claude Code 的 declarative subagent 定义（Markdown frontmatter）形成互补：SDK 面向编程集成，Claude Code 面向交互式开发。

### Managed Agents API

[[Anthropic Managed Agents API]] 提供 **共享容器 + Session Thread 隔离** 的执行模型。所有 agents 共享同一容器和文件系统，但每个 agent 运行在独立的 session thread 中（context-isolated event stream），Coordinator 在 primary thread 中报告活动。Threads 持久化，coordinator 可向之前调用过的 agent 发送 follow-up。适用于并行分发独立 subtask、专业化路由（不同 agent 有不同 system prompt 和工具）、向更强模型升级复杂 subtask 等场景。

### Claude Cowork

Claude Cowork 是 Anthropic 的协作式 Agent 产品，强调人机协同而非全自动执行。与 Managed Agents 的 coordinator/worker 模式不同，Cowork 将人类置于决策回路中心，Agent 主动汇报进度、请求确认关键决策、在不确定时升级给人。

## Multi-Agent 架构方案

Anthropic 提供了三种互补的多 Agent 方案，适用于不同粒度和隔离需求：

### Orchestrator-Worker（研究系统）

Lead Agent（规划者）将任务分解后分发给多个并行 Subagent，每个 Subagent 在独立 context window 中探索不同方向，压缩关键 token 回报给 Lead 汇总。该方案在 BrowseComp 基准上实现 **+90.2%** 性能提升（Opus Lead + Sonnet Subagent vs 单 Opus），但 token 消耗是单 agent 的 4 倍。核心发现：多 Agent 系统的性能增益主要来自花费足够 token 彻底探索问题空间，模型升级比加倍 token 预算更高效。

### Managed Agents Isolation（API 层）

基于 Session Thread 的持久化隔离模型。每个 agent 有独立的对话历史、工具配置、MCP 服务器、模型选择，tools 和 context 不共享。与 Orchestrator-Worker 的关键区别：agent 保留之前所有 turns 的上下文（持久化），而非每次调用重新开始。

### Agent Teams（Claude Code 内置）

[[Claude Code Agent Teams]] 在 Claude Code 内部实现：Team Lead 协调 + Teammates 独立工作 + 共享任务队列 + 直接互相通讯。Teammates 可 claim 任务、直接互发消息（不经 lead），区别于 subagent 的单向回报模式。适用于研究审查、跨层协调、并行调试竞争假设等场景。目前为实验性功能（v2.1.32+）。

## 设计哲学

Anthropic 的 Agent 设计贯穿三条原则：

1. **Safety-first** — deny-first 权限系统、Quarantine 模式（读不可信内容的 agent 与执行高权限操作的 agent 结构隔离）、三层安全护栏，安全是架构约束而非事后补丁。Anthropic 的安全哲学不仅体现在产品层面，也深刻影响了其 Agent 架构设计：Managed Agents 的 Session Thread 隔离本质上是一种安全边界，Dynamic Workflows 的 Quarantine 模式将不可信输入的处理与高权限操作强制分离在两个 agent 中执行。
2. **Minimal scaffolding** — 与 [[Thin Harness, Fat Skills]] 理念高度一致。Anthropic 倾向于让 Agent 自身判断何时委派、如何协作，而非用繁重的编排框架预设所有交互路径。Dynamic Workflows 将这一原则推到极致：harness 按任务即时生成，不预设任何固定工作流模板。这与 [[MiniMax Mavis]] 的"多 Agent 系统是 runtime"形成有趣的张力——Anthropic 选择让 Agent 自己写 harness，Mavis 选择用确定性状态机管理 Agent 生命周期。
3. **Token as key resource** — 将 token 视为核心资源来设计架构。并行 Subagent 的上下文隔离既保护了主对话的精简性，又让每个子任务有足够的 token 预算深入探索。[[Claude Code Dynamic Workflows 实践指南]] 中识别的三种失效模式（Agentic laziness、Self-preferential bias、Goal drift）本质上都是 token 分配不当导致的结构性问题。

## Related concepts

- [[Claude Code Subagent]] — Claude Code 的独立上下文工作者机制
- [[Claude Code Skills]] — Skills 扩展机制，可与 Subagent 组合使用
- [[Claude Code Agent Teams]] — Claude Code 内置的多 Agent 协作模式
- [[Claude Code Dynamic Workflows 实践指南]] — 按任务即时生成定制 harness
- [[Anthropic Managed Agents API]] — Session Thread 隔离的托管 Agent 服务
- [[Multi-Agent 协作模式]] — Orchestrator-Worker 等通用协作模式
- [[Thin Harness, Fat Skills]] — 与 Anthropic minimal scaffolding 哲学同源
- [[Worker Verifier 对抗循环]] — 与 Anthropic 方案的对比参照（Mavis 方案）

## Sources

- [[Anthropic 多 Agent 研究系统]] — (2026-05-19) Orchestrator-Worker 架构与 BrowseComp 基准数据
- [[Anthropic Managed Agents API]] — (2026-05-19) Session Thread 隔离模型与模式对比
- [[Claude Code Agent Teams]] — (2026-05-19) Team Lead + Teammates 架构与 token 消耗分析
- [[A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读]] — (2026-06-05) Dynamic Workflows 三种失效模式与 6 种编排模式
