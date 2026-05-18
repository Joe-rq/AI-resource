# Multi-Agent / Agent Teams

多智能体协作系统的研究资料汇编。

## 主题核心问题

> 一个 AI 不够用的时候，怎么让多个 AI 可靠地协作完成长程任务？

## 文档索引

| # | 文件 | 来源 | 核心视角 |
|---|------|------|---------|
| 01 | [一个 AI 还是不够](01-minimax-single-ai-not-enough.md) | 个人解读 (x.com) | 从写作工作流踩坑出发，对照 MiniMax Mavis 的 Worker-Verifier 架构反思自己的 skill 设计 |
| 02 | [MiniMax Agent Team 技术报告](02-minimax-agent-team-tech-report.md) | MiniMax 官方 (知乎) | 详细技术报告：Leader/Worker/Verifier 架构、Team Engine 状态机、四大落地场景、成本分析 |
| 03 | [Agent 协作的 Harness 策](03-minimax-harness-strategy.md) | MiniMax 官方 (公众号) | Q&A 版本：痛点分析、与 OpenAI/LangGraph/Claude Code 的对比、IM 异步执行设计 |
| 04 | [Anthropic 多 Agent 研究系统](04-anthropic-multi-agent-research-system.md) | Anthropic 工程博客 | Anthropic Research 功能的架构实战：orchestrator-worker 模式、prompt 工程、评估方法、生产可靠性 |
| 05 | [Anthropic Managed Agents API](05-anthropic-managed-agents-api.md) | Anthropic 平台文档 | API 层面的多 agent session 管理：session thread 隔离、事件流、工具权限 |
| 06 | [Claude Code Agent Teams](06-claude-code-agent-teams.md) | Claude Code 文档 | Claude Code 的 agent team 实现：teammate 协作、共享任务列表、直接通讯 |
| 07 | [Cookbook: 协调专家团队](07-anthropic-cookbook-coordinate-specialist-team.md) | Anthropic Cookbook | 可运行的代码示例：coordinator + 3 specialist agents（researcher/librarian/pricer）协作写销售提案 |

## 关键概念速查

| 概念 | 出处 | 含义 |
|------|------|------|
| Worker-Verifier 对抗循环 | MiniMax | Worker 干活，Verifier 挑刺，一方结束触发另一方启动 |
| Team Engine | MiniMax | 确定性代码（状态机），管理 producing → verifying → done 生命周期 |
| Orchestrator-Worker | Anthropic | Lead Agent 协调，Subagent 并行执行，结果返回 Lead 合并 |
| 上下文隔离 | 共识 | 每个 Agent 只看自己需要的信息，不被无关上下文污染 |
| Harness 思想 | 共识 | Agent 不只写代码/做任务，还要跟进全流程：分支、沙箱、diff、测试、审查 |

## 阅读建议

1. 先读 01（个人视角，最易共鸣）
2. 再读 02（MiniMax 完整技术方案）
3. 03 和 02 内容高度重叠，选读即可
4. 04 是 Anthropic 的实战经验，侧重工程落地
5. 05 是 API 参考，按需查阅
6. 06 是 Claude Code 的实现，可直接实践
7. 07 是可运行的代码示例，适合动手跑一遍

## 相关仓库

- [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) — Anthropic 官方 Cookbook，`managed_agents/` 目录下有 10+ 个多 Agent 示例 notebook
