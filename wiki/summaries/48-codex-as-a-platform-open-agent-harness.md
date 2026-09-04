---
title: "Codex as a Platform: Build on the Open Agent Harness"
type: summary
created: 2026-09-04
updated: 2026-09-04
sources: ["raw/articles/48-codex-as-a-platform-open-agent-harness.md"]
tags: [codex, openai, agent-harness, agent-loop, app-server, harness-commoditization, mcp, sandbox, arc-agi-3, compaction, retained-reasoning, arc, platform]
---

# Codex as a Platform: Build on the Open Agent Harness

> 原始来源：[developers.openai.com/blog/codex-as-a-platform](https://developers.openai.com/blog/codex-as-a-platform)（作者 Nicolas Bonamy、Derrick Choi）
> 发布日期：2026-08-19 · 摄取日期：2026-09-04
> 论点反哺 [[Harness Cybernetics]]（inner harness 商品化研究问题的一手回答）、[[Thin Harness, Fat Skills]]、[[Agent Runtime]]（compaction 量化数据）、[[Anthropic]] vs [[OpenAI]] 产品矩阵对照。

## 摘要

OpenAI 把 Codex 的**开源 harness**（github.com/openai/codex）正式定位为平台：**"可复用的部分是 agent loop"**——harness 管理会话状态、流式执行、工具调用、沙箱与审批策略、跨 turn 续接，通过 **Codex app-server** 的文档化 client protocol（threads / turns / events / approval requests）暴露给宿主应用。开发者不必再造 runtime，而是把 agent 嵌进围绕真实工作设计的软件（运维 dashboard、安全调查台、客服控制台）。

**核心论据（harness 设计物质性）**：在 ARC-AGI-3 上，retained reasoning + context compaction 两个 harness 设置把 **GPT-5.6 Sol 从 13.3% 拉到 38.3%，输出 token 降 6 倍**——harness 不是包装纸，是性能变量。

## 分层与归属

| 层 | 归属 | 内容 |
|----|------|------|
| 界面/业务上下文/审批 | **宿主应用** | dashboard、队列、记录、approval flow——界面本身告诉 agent 用户在看什么 |
| Agent loop + 沙箱执行 | **Codex app-server** | 会话状态、流式事件、工具交互、中断、审批请求 |
| 数据与动作 | **应用自有 MCP 服务** | 宿主暴露自己的系统/文档/动作 |

三种集成深度：`codex exec`（脚本/CI 有界任务+结构化输出）→ **Codex SDK**（编程接口）→ **app-server**（agent 即产品本体，直接控制生命周期与 UX）。开源的是 harness 与集成层，模型访问与托管服务另算。

## Relay 示例与真实采用

- **Relay**：货运 dashboard 内嵌 agent；用户不从零写 prompt，而是选中 shipment 点动作（Compare recovery）；应用供上下文、Codex 取数据、**后果性写入必须人工审批**
- 公开采用：GitHub/JetBrains（IDE 工作流）、Cisco（App Builder / Cloud Control）、Thrive Holdings + Crete（报税流程 + 从业者反馈；试点处理 **7,000 份报税单，准备时间降约 1/3**）

## "Build beyond the obvious"

多数工作的本质上下文锚定在 dashboard/timeline/map/系统记录里——机会**不是用通用聊天框取代这些界面**，而是给界面装一个能理解工作、调查上下文、提议下一步、经审批后行动的 agent。

## 对 wiki 研究问题的意义

直接回答 [[Harness Cybernetics]] 域 "inner harness 商品化速率与拐点" 研究问题：拐点正在发生——OpenAI 用"harness"作正式产品词汇并开源平台化，ARC-AGI-3 数据（13.3→38.3%、6×）同时是 [[Context Engineering]] compaction 研究问题的最硬量化证据。与 [[Steering Claude Code: Seven Instruction Mechanisms]]（Anthropic 侧同月讲授同一层）对照：两家都在把 harness 工程产品化。
