# Index — AI Resource Wiki

> Agent 平台与基础设施层研究资料库。涵盖 Runtime、Multi-agent 架构、行业实践。

## Navigation
- [[#Concepts]] · [[#Entities]] · [[#Summaries]] · [[#Open Questions]]

## Concepts

### Agent Platform
- [[concepts/Agent-Memory]] — Agent 长期记忆：图谱结构、向量检索、自我进化（NanoClaw/Hermes 对比）
- [[concepts/Multi-Agent-协作模式]] — 四种核心协作模式：Orchestrator/Specialist、Worker/Verifier、Team Engine、自动扩张任务图
- [[concepts/Worker-Verifier-对抗循环]] — Worker/Verifier 对抗循环是 Mavis 的核心架构机制
- [[concepts/Agent-Runtime]] — 单 Agent 执行环境，包含 Prompt/工具定义/上下文管理/错误处理
- [[concepts/Agent-Secure-Runtime]] — Agent 安全运行时：三层安全检查（Policy/Network/Privacy）+ 沙箱隔离
- [[concepts/Agent-Harness-治理协议]] — 跨 session、跨 agent 的长期一致性治理（事件溯源、概念演化、双层验证、自动扩张任务图）

### Claude Code
- [[concepts/Claude-Code-Subagent/index|Claude Code Subagent]] — Subagent：独立上下文工作者，内置类型、自定义定义、Fork 模式、持久内存、Hooks
- [[concepts/Claude-Code-Skills/index|Claude Code Skills]] — Skills 扩展机制：SKILL.md 定义、动态上下文注入、Subagent 中运行、调用控制
- [[concepts/Claude-Code-Dynamic-Workflows-Practical-Guide|Claude Code Dynamic Workflows 实践指南]] — 场景选择决策树、命令速查、14 个推荐场景与最佳实践

### Meta Reflection
- [[concepts/Meta-Reflection-Techniques]] — 12 个元反思技巧（按"行动之环"四象限组织：意图/实施/反馈/情境）+ 对齐=补全 + 看门狗模式 + 实体数约束 ≤ 4

### Autonomous Systems
- [[concepts/Autonomous-AI-System]] — AI 自主干活系统（阳志平）：人在离场后持续运行的 12 个工程化技巧 + 永不停摆 + 飞轮式自我演化

### Architecture Principles
- [[concepts/Thin-Harness-Fat-Skills]] — Thin Harness, Fat Skills：套具极薄、技能极胖，90% 价值在 markdown 流程文件（skill-as-method-call、resolver、latent vs deterministic、diarization、self-rewriting skill）

### Evaluation
- [[concepts/Agent-Macro-Evaluation]] — Agent 宏观评估方法论：4 层标签（case_type → run_outcome → eval_finding → behavior_pattern）+ BERTopic 风格聚类 + AgentTrace 风格诊断 + 三个核心公式（impact_score / lift / suspect_score）

## Entities
- [[entities/MiniMax-Mavis]] — MiniMax 的 Agent 产品，MiniMax as a Jarvis
- [[entities/NVIDIA-Agent-Toolkit]] — NVIDIA Agent 开发工具包，含 OpenShell 安全运行时
- [[entities/wow-harness]] — wow-harness v3 治理协议（事件溯源 + 概念演化 + 双层验证 + 自动扩张任务图）
- [[entities/Dive-into-Claude-Code]] — Claude Code 源码级逆向工程分析论文（5 设计价值、13 设计原则、7 组件结构、5 层子系统）
- [[entities/ESAA]] — ESAA: Event Sourcing for Autonomous Agents（Event Sourcing + CQRS 应用于 agent 生命周期管理，immutable audit trail + deterministic replay）
- [[entities/NanoClaw]] — NanoClaw：~500行代码的轻量级 Agent 框架，建在 Claude Agent SDK 上
- [[entities/Nous-Research]] — Nous Research：硅谷 AI 实验室，Hermes Agent（11万星）

## Summaries (chronological)
- 2026-06-13 — [[summaries/20-macro-evals-for-agentic-systems]] — Macro Evals for Agentic Systems：从单次评分到群体行为模式（OpenAI Cookbook，1000 次合成 EV 订单运行 + Promptfoo + BERTopic 风格聚类 + AgentTrace 风格诊断）
- 2026-06-11 — [[summaries/19-addyosmani-loop-engineering]] — Loop Engineering：从 Prompt 到系统设计（Addy Osmani，5 模块 + 1 记忆，Claude Code / Codex 通用 loop 架构）
- 2026-06-04 — [[summaries/18-agent-harness-12-components]] — Agent Harness 12 组件 + 7 决策（TAO 循环、上下文腐烂、脚手架隐喻、TerminalBench 30→5 名实证）
- 2026-06-04 — [[summaries/17-ai-autonomous-system-tips]] — 如何实现一个好的 AI 自主干活系统（阳志平）：12 技巧 × 4 组（任务编排/实际开工/自检评审/自动续航）+ 永不停摆 + 飞轮
- 2026-06-04 — [[summaries/16-distributed-harness]] — 分布式 Harness 哲学：Agent 显形条件 + 维度循环 + 智流网络（CGP/IEL、四层循环、四种显形条件）
- 2026-06-04 — [[summaries/15-wow-harness-v3-governance]] — wow-harness v3 治理协议设计者一手分享（事件时间线、概念演化、双层验证、自动扩张任务图、人机决策分层、上下文胶囊）
- 2026-06-04 — [[summaries/13-thin-harness-fat-skills]] — Thin Harness, Fat Skills 架构原则（五个核心定义 + 三层架构 + YC Startup School self-rewriting skill 案例）
- 2026-06-04 — [[summaries/12-harness-engineering-survey]] — Harness Engineering 综述（14 篇工程文章 + Claude Code v2.1.88 源码对账，补偿面迁移与膨胀）
- 2026-06-04 — [[summaries/11-meta-reflection-techniques]] — 12 个元反思技巧（按"行动之环"四象限组织）+ 对齐=补全 + 看门狗摆脱人在回路
- 2026-06-04 — [[summaries/10-claude-code-dynamic-workflows]] — Claude Code 动态工作流（JavaScript 脚本在后台大规模编排子代理，捆绑 `/deep-research` + `ultracode` 触发）
- 2026-05-22 — [[summaries/10-singapore-fm-nanoclaws-second-brain]] — 新加坡外長的 AI 第二大腦（NanoClaw + Raspberry Pi）
- 2026-05-22 — [[summaries/11-hermes-agent-nous-research]] — Hermes Agent / Nous Research（长期记忆 + 自我进化）
- 2026-05-22 — [[summaries/esaa-paper]] — ESAA 论文：Event Sourcing + CQRS 应用于 LLM agent 生命周期（两个 case study 验证）
- 2026-05-22 — [[summaries/dive-into-claude-code]] — Claude Code 源码级逆向工程分析（98.4% 基础设施、5 设计价值、与 OpenClaw 对比）
- 2026-05-22 — [[summaries/hermes-agent-harness-engineering]] — wow-harness v3 治理协议设计（**已合并至 15-**，见 stub 提示）
- 2026-05-21 — [[summaries/09-claude-subagent-tutorial]] — Claude Code Subagent 小白入门教程（内置类型、自定义定义、调用方式）
- 2026-05-19 — [[summaries/nvidia-agent-toolkit]] — NVIDIA Agent Toolkit 架构图（OpenShell 安全运行时 + 全栈 Agent 平台）
- 2026-05-19 — [[summaries/08-agent-runtime-battlefield]] — Agent Runtime 主战场（4.8pp ≈ 一次模型版本迭代）
- 2026-05-19 — [[summaries/01-minimax-single-ai-not-enough]] — 单 AI 的四个结构性缺陷
- 2026-05-19 — [[summaries/04-anthropic-multi-agent-research-system]] — Anthropic Orchestrator-Worker 架构
- 2026-05-19 — [[summaries/05-anthropic-managed-agents-api]] — Anthropic 共享容器 + Session Thread 隔离
- 2026-05-19 — [[summaries/06-claude-code-agent-teams]] — Claude Code Team Lead + Teammates 独立工作
- 2026-05-19 — [[summaries/14-building-skill-for-claude]] — Claude Code Skill 开发流程
- 2026-05-19 — [[summaries/02-minimax-agent-team-tech-report]] — Mavis 详细技术报告
- 2026-05-19 — [[summaries/14-building-skill-for-claude-zh]] — Skill 开发指南（中文）
- 2026-05-19 — [[summaries/project-overview]] — AI Resource 项目介绍

## Open Research Questions

- 补偿面（Compensation Surface）的形式化定义：能否用公式描述「组件存在价值 = 模型当前做不到的事 - 已实现成本」？
- Cursor 三层架构（Planner-Worker-Judge）在 16+ Agent 扩展时是否会出现「门控本身成为瓶颈」的反例？
- KAIROS 的 15 秒打断阈值在不同任务类型下的最优取值如何确定？
- YOLO Classifier 的「学用户习惯」机制如何避免被用户偶尔的「试一下」操作训练出错误的拒绝模式？
- Hooks 的 8 插槽在企业合规场景下的可观测性（audit trail）如何保证？
- Sprint Contract 在 Generator 和 Evaluator 都是 LLM 时如何防止「默契通过」（双方都对低质量产出达成共识）？
- Cursor 边际影响力排序（Prompt > Harness > 模型）是否在所有任务类型上都成立？对需要长期记忆的任务是否反转？
- Claude Code Team Mode 把上下文利用率控制在 40% 的设计在「需要全局视野的协调任务」上是否反而成为障碍？
- 「补偿面在膨胀」是否会带来难以承受的工程复杂度（KAIROS + YOLO + Hooks + autoDream 同时维护）？
- 分布式 Harness 的"附着点"概念与 [[concepts/Claude-Code-Subagent/index|Claude Code Subagent]] 的"独立上下文窗口"是同构还是包含？
- CGP/IEL 的 9 件工具组中，ConOps / SDM / CDM / Influence Diagram 在现有 AI 开发工具中有无成熟实现？
- "四层维护存储"（归档/摘要/投影/切片）与 [[concepts/Agent-Harness-治理协议|Agent Harness 治理协议]] 的"事件时间线 + 快照压缩"是同一思想的不同表述还是不同实现路径？
- "Fork 与胶囊"返回"结构化判断而不是全部细节"与 [[entities/ESAA|ESAA]] 的 boundary contracts 在数据契约层面是否同源？
- 宏观评估的 `behavior_pattern` 能否反向自动生成新的底层评估 rubric（self-extending eval）？
- BERTopic 风格 vs 直接 LLM 主题归纳在 agent trace 上的稳定性差异如何量化？
- `suspect_score` 的 `0.4/0.3/0.2/0.1` 权重在不同 agent 系统上是否需要重新校准？
