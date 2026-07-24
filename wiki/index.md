---
title: Index — AI Resource Wiki
type: index
created: 2026-05-19
updated: 2026-07-24
sources: []
tags: [index, navigation]
---

# Index — AI Resource Wiki

> Agent 平台与基础设施层研究资料库。涵盖 Runtime、Multi-agent 架构、行业实践。

## Navigation
- [[#Concepts]] · [[#Entities]] · [[#Summaries]] · [[#Open Questions]]

## Concepts

### Agent Platform
- [[Agent Memory]] — Agent 长期记忆：图谱结构、向量检索、自我进化（folder-split: Architecture / Forgetting & Compaction / Self-Evolving Memory）
- [[Multi-Agent 协作模式]] — 四种核心协作模式：Orchestrator/Specialist、Worker/Verifier、Team Engine、自动扩张任务图
- [[Worker Verifier 对抗循环]] — Worker/Verifier 对抗循环是 Mavis 的核心架构机制（收敛模型、死锁检测、升级与降级）
- [[Agentic Code Review]] — agent 产码时代的评审经济学：blast radius 分层 / intent reconstruction / 异构多审稿 / human on the loop
- [[Multi-Model Ensemble]] — 多模型协作四架构谱系（采样投票/分层聚合/随机轮替/多轮辩论）+ 收益三条件（异构性×任务难度×算力公平）
- [[LLM Debate]] — 多模型辩论：society of minds + 四大失效模式（bias reinforcement / diversity collapse / 弱拖垮强 / 算力混淆）
- [[Trajectory Handoff]] — 轨迹交接（/prewalk）：传 context window 不传 plan document（明信片）；swap on first edit + prune planning instruction；O(reads) 成本模型；prefill 原理；与 Multi-Model Ensemble 正交（接力 vs 聚合）
- [[Agent Runtime]] — 单 Agent 执行环境，包含 Prompt/工具定义/上下文管理/错误处理
- [[Agent Secure Runtime]] — Agent 安全运行时：三层安全检查（Policy/Network/Privacy）+ 沙箱隔离
- [[Agent Harness 治理协议]] — 跨 session、跨 agent 的长期一致性治理（事件溯源、概念演化、双层验证、自动扩张任务图）

### Claude Code
- [[Claude Code Subagent]] — Subagent：独立上下文工作者，内置类型、自定义定义、Fork 模式、持久内存、Hooks
- [[Claude Code Skills]] — Skills 扩展机制：SKILL.md 定义、动态上下文注入、Subagent 中运行、调用控制
- [[Claude Code Dynamic Workflows 实践指南]] — 场景选择决策树、命令速查、14 个推荐场景与最佳实践
- [[Claude Code Loops]] — 官方 loop 四分类法（Turn-based/Goal-based/Time-based/Proactive），按 trigger/stop/primitive/task 四维度

### Dynamic Workflows — 失效模式与安全模式
- [[Agentic Laziness]] — 智能体偷懒：走捷径、跳过验证、过早宣布完成
- [[Self-Preferential Bias]] — 自我偏好偏差：坚持自己输出、拒绝有效外部反馈
- [[Goal Drift]] — 目标漂移：逐步偏离原始目标而不自知
- [[Quarantine Mode]] — 隔离模式：读未受信内容 agent 与高权限动作 agent 结构隔离
- [[Tournament Mode]] — 锦标赛模式：pairwise 比较与 transitivity 假设

### Meta Reflection
- [[Meta Reflection Techniques]] — 12 个元反思技巧（按"行动之环"四象限组织：意图/实施/反馈/情境）+ 对齐=补全 + 看门狗模式 + 实体数约束 ≤ 4
- [[Finding Your Unknowns]] — 四象限 Unknowns 框架（Known/Unknown × Knowns/Unknowns）：减少并规划未知即 agentic coding 技能本身；blind spot pass / brainstorm / interview / reference / quiz 技巧工具箱

### Autonomous Systems
- [[Autonomous AI System]] — AI 自主干活系统（阳志平）：人在离场后持续运行的 12 个工程化技巧 + 永不停摆 + 飞轮式自我演化
- [[Heartbeat Watchdog]] — 心跳看门狗三层互检（L0 常驻 shell guard / L1 durable cron / L2 业务自报）：独立守护层对治运行时脆弱与停滞

### Architecture Principles
- [[Thin Harness, Fat Skills]] — Thin Harness, Fat Skills：套具极薄、技能极胖，90% 价值在 markdown 流程文件（skill-as-method-call、resolver、latent vs deterministic、diarization、self-rewriting skill）
- [[AI Capability Overhang]] — AI 能力悬置：模型能力已存在但未被组织充分释放，FDE 的成因，与补偿面互为镜像
- [[Stateless Reducer]] — 无状态归约器：agent = 纯函数 (state,event)→(new state, side-effect descriptors)，LLM 成为唯一非确定节点，pause/resume/replay/time-travel 同源，第五种确定性范式
- [[Harness Cybernetics]] — Harness 控制论：前馈 Guides/反馈 Sensors 对偶 + Computational/Inferential 2×2 + steering loop；inner/outer harness；cybernetic governor；Ashby's Law
- [[Context Engineering]] — 上下文工程：prompt engineering 的演进，write/select/compress/isolate 四策略，context 四失败模式，KV 命中率切入

### Go-to-Market & Product Discovery
- [[Forward-Deployed-Engineering]] — FDE 前置部署工程：四要素精确定义、Echo/Delta/Dev 三角循环、碎石路→柏油路飞轮、与咨询的本质区别、AI 时代复兴的结构性原因

### Evaluation
- [[Agent Macro Evaluation]] — Agent 宏观评估方法论：4 层标签（case_type → run_outcome → eval_finding → behavior_pattern）+ BERTopic 风格聚类 + AgentTrace 风格诊断 + 三个核心公式（impact_score / lift / suspect_score）
- [[Agent Reliability vs Capability]] — capability≠reliability 背离：pass@k、RDC/VAF/GDS/MOP 四指标、MOP paradox（frontier model meltdown 更高）、memory scaffolds 普遍损害长程 reliability

## Entities
- [[MiniMax Mavis]] — MiniMax 的 Agent 产品，MiniMax as a Jarvis
- [[NVIDIA Agent Toolkit]] — NVIDIA Agent 开发工具包，含 OpenShell 安全运行时
- [[wow-harness]] — wow-harness v3 治理协议（事件溯源 + 概念演化 + 双层验证 + 自动扩张任务图）
- [[Dive into Claude Code（论文）]] — Claude Code 源码级逆向工程分析论文（5 设计价值、13 设计原则、7 组件结构、5 层子系统）
- [[ESAA]] — ESAA: Event Sourcing for Autonomous Agents（Event Sourcing + CQRS 应用于 agent 生命周期管理，immutable audit trail + deterministic replay）
- [[NanoClaw]] — NanoClaw：~500行代码的轻量级 Agent 框架，建在 Claude Agent SDK 上
- [[Nous Research]] — Nous Research：硅谷 AI 实验室，Hermes Agent（11万星）
- [[Palantir]] — Palantir Technologies：FDE 模式发明者、Gotham/Foundry/AIP 产品矩阵、Ontology 本体论、反 SaaS 产品哲学
- [[Cline]] — 开源 AI coding agent（VS Code 扩展），Runtime benchmark 核心实证来源（74.2% vs 69.4%, +10pp hill climbing）
- [[Anthropic]] — Claude 模型族、Claude Code/Agent SDK/Managed Agents 产品矩阵、Orchestrator-Worker 架构
- [[OpenAI]] — GPT 模型族、Codex CLI、Handoff 模式、宏观评估方法论
- [[LangChain]] — 开源 LLM 框架（chain-based composition + LangGraph），Agent Runtime benchmark 参考点
- [[nashsu LLM Wiki]] — Karpathy LLM Wiki pattern 的产品化实现（Tauri 桌面应用 + 知识图谱 + MCP），本 wiki 的同 pattern 异途参照

## Summaries (chronological)
- 2026-07-24 — [[/prewalk: Hand off a trajectory, not a fairytale]] — stencil.so/omp 工程博文：/plan 悖论（贵 14%，O(reads) 成本模型）+ /prewalk 三步（swap on first edit + prune planning instruction）+ SWE-Bench Pro 数据（92–97% pass @ 53–61% cost）+ cheating 暴跌（44/72/13%）+ prefill 原理
- 2026-07-14 — [[A Field Guide to Fable: Finding Your Unknowns]] — Anthropic 官方 field guide（Thariq Shihipar）：四象限 Unknowns 框架 + pre/during/post 三阶段技巧工具箱 + Fable 发布视频实战案例
- 2026-07-09 — [[多模型协作如何超过单强模型：正面证据综述]] — 多模型协作 > 单强模型正面证据（MoA 65.1%>GPT-4o / Blending 3×6-13B>175B ChatGPT / More Agents / Du Debate / Self-Consistency）
- 2026-07-09 — [[LLM Debate 失效模式：多 Agent 协作何时翻车（2025 综述）]] — 多 Agent 协作失效模式（Stop Overvaluing MAD 等 6 篇 2025 反面综述；heterogeneity×difficulty×architecture×算力公平）
- 2026-07-07 — [[Getting started with loops（Claude Code 官方 loop 分类法）]] — Claude Code 团队官方 loop 四分类法（Turn-based/Goal-based/Time-based/Proactive）+ 维护代码质量 + 管理 token 用量
- 2026-06-26 — [[Deli AutoResearch 四论文系列总览与生产统计]] — Deli AutoResearch 项目四篇综述（自主研究 Agent / 持续学习 / 长程决策 / 自博弈）的页数、引用、评审分数与生产统计
- 2026-06-26 — [[Deli AutoResearch 第四篇论文诞生记：285B 自博弈实验与诚实的自我评审]] — Paper #4（Self-Play）16 轮评审、285B GRPO 实验、V12 主动降分与 V16 理论加固的故事
- 2026-06-24 — [[Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀]] — Agent Memory 四层架构：规则记忆、常驻画像、历史召回、反思与技能沉淀；证据链治理与 memory 的持久化风险
- 2026-06-23 — [[12-Factor Agents]] — 12-Factor Agents（HumanLayer/Dex Horthy）：好 agent = 大部分确定性软件 + LLM 撒关键点；12 条按五主题；接缝在 selection↔invocation 间；workflow vs agent 术语张力
- 2026-06-21 — [[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）]] — Deli_AutoResearch 协议框架（Victor Chen）：长时间自主任务 3 失效模式（认知循环/停滞/运行时脆弱）+ 5 行为约束 + 三层心跳看门狗 + fresh session over resume + stall 检测/pivot 结构
- 2026-06-18 — [[Agentic Code Review：评审成为软件工程最杠杆的技能]] — Agentic Code Review（Addy Osmani）：四倍代码一成价值、blast radius 分层、intent reconstruction、异构多审稿、human on the loop
- 2026-06-18 — [[Harness Engineering 14 步路线图：从单个 agent 到自我改进系统]] — Harness Engineering 14 步路线图（0xMovez）：三层切分 + 14 步 roadmap + .claude/ 布局
- 2026-06-18 — [[Skills 自我提升闭环：inner loop 用、outer loop 改]] — Skills 自我提升闭环（Zach Lloyd/Warp）：inner loop 用 skill、outer loop 定时改 skill，GitHub issue triage 实例
- 2026-06-18 — [[FDE 深度分析 v4：AI 能力悬置时代的现场工程组织接口]] — FDE 深度分析 v4（黄奕彬）：capability overhang + 四断点 + 双向翻译器 + 三种资产 + DeployCo 组织化扩散 + 最小交付包/技术红线 + 中国语境
- 2026-06-15 — [[当我们谈论 FDE 时，我们在谈论什么？]] — 当我们谈论 FDE 时：四要素精确定义、Echo/Delta/Dev 三角循环、三种"穿新衣的旧角色"、AI 时代 FDE 复兴的结构性原因
- 2026-06-15 — [[前沿部署工程的未来：OpenAI、Ramp、Nominal、Dataland 圆桌]] — FDE 未来圆桌：OpenAI/Ramp/Nominal/Dataland 四家公司如何定义和运作 FDE
- 2026-06-15 — [[OpenAI FDE 访谈录：信任、产品与影响（Colin Jarvis）]] — OpenAI FDE 访谈录：信任、产品与影响（Colin Jarvis）
- 2026-06-15 — [[FDE 实战手册：AI 初创公司的前置部署工程（Bob McGrew）]] — FDE 实战手册：AI 初创公司的前置部署工程（Bob McGrew）
- 2026-06-13 — [[Macro Evals for Agentic Systems：从单次评分到群体行为模式]] — Macro Evals for Agentic Systems：从单次评分到群体行为模式（OpenAI Cookbook，1000 次合成 EV 订单运行 + Promptfoo + BERTopic 风格聚类 + AgentTrace 风格诊断）
- 2026-06-11 — [[Loop Engineering：从 Prompt 到系统设计]] — Loop Engineering：从 Prompt 到系统设计（Addy Osmani，5 模块 + 1 记忆，Claude Code / Codex 通用 loop 架构）
- 2026-06-04 — [[Agent Harness：让 AI 从聊天机器人变成真正的智能体（12 组件 + 7 决策）]] — Agent Harness 12 组件 + 7 决策（TAO 循环、上下文腐烂、脚手架隐喻、TerminalBench 30→5 名实证）
- 2026-06-04 — [[A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读]] — Anthropic 官方动态工作流深度解读（3 失效模式 + 6 编排模式 + 10 用例 + Quarantine 安全模式）
- 2026-06-04 — [[如何实现一个好的 AI 自主干活系统]] — 如何实现一个好的 AI 自主干活系统（阳志平）：12 技巧 × 4 组（任务编排/实际开工/自检评审/自动续航）+ 永不停摆 + 飞轮
- 2026-06-04 — [[分布式 Harness：从 Agent 显形条件到智流网络]] — 分布式 Harness 哲学：Agent 显形条件 + 维度循环 + 智流网络（CGP/IEL、四层循环、四种显形条件）
- 2026-06-04 — [[Hermes Agent 之后：AI 开发需要一层治理协议]] — wow-harness v3 治理协议设计者一手分享（事件时间线、概念演化、双层验证、自动扩张任务图、人机决策分层、上下文胶囊）
- 2026-06-04 — [[Thin Harness, Fat Skills：套具要瘦，技能要胖]] — Thin Harness, Fat Skills 架构原则（五个核心定义 + 三层架构 + YC Startup School self-rewriting skill 案例）
- 2026-06-04 — [[Harness Engineering 综述：14 篇工程文章里的 15 个月]] — Harness Engineering 综述（14 篇工程文章 + Claude Code v2.1.88 源码对账，补偿面迁移与膨胀）
- 2026-06-04 — [[12 个元反思技巧]] — 12 个元反思技巧（按"行动之环"四象限组织）+ 对齐=补全 + 看门狗摆脱人在回路
- 2026-06-04 — [[Claude Code 动态工作流（Dynamic Workflows）]] — Claude Code 动态工作流（JavaScript 脚本在后台大规模编排子代理，捆绑 `/deep-research` + `ultracode` 触发）
- 2026-05-22 — [[新加坡外长的 AI 第二大脑]] — 新加坡外長的 AI 第二大腦（NanoClaw + Raspberry Pi）
- 2026-05-22 — [[Hermes Agent：Nous Research 的开源 Agent 框架]] — Hermes Agent / Nous Research（长期记忆 + 自我进化）
- 2026-05-22 — [[ESAA: Event Sourcing for Autonomous Agents]] — ESAA 论文：Event Sourcing + CQRS 应用于 LLM agent 生命周期（两个 case study 验证）
- 2026-05-22 — [[Dive into Claude Code 论文解读]] — Claude Code 源码级逆向工程分析（98.4% 基础设施、5 设计价值、与 OpenClaw 对比）
- 2026-05-21 — [[09-Claude Subagent 小白入门教程]] — Claude Code Subagent 小白入门教程（内置类型、自定义定义、调用方式）
- 2026-05-19 — [[NVIDIA Agent Toolkit 架构]] — NVIDIA Agent Toolkit 架构图（OpenShell 安全运行时 + 全栈 Agent 平台）
- 2026-05-19 — [[08 - Agent Runtime 主战场]] — Agent Runtime 主战场（4.8pp ≈ 一次模型版本迭代）
- 2026-05-19 — [[单 AI 的四个结构性缺陷]] — 单 AI 的四个结构性缺陷
- 2026-05-19 — [[Anthropic 多 Agent 研究系统]] — Anthropic Orchestrator-Worker 架构
- 2026-05-19 — [[Anthropic Managed Agents API]] — Anthropic 共享容器 + Session Thread 隔离
- 2026-05-19 — [[Claude Code Agent Teams]] — Claude Code Team Lead + Teammates 独立工作
- 2026-05-19 — [[构建 Claude 技能完整指南（中文）]] — Claude Code Skill 开发流程
- 2026-05-19 — [[MiniMax Mavis 技术报告]] — Mavis 详细技术报告
- 2026-05-19 — [[AI Resource 项目介绍]] — AI Resource 项目介绍

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
- 分布式 Harness 的"附着点"概念与 [[Claude Code Subagent]] 的"独立上下文窗口"是同构还是包含？
- CGP/IEL 的 9 件工具组中，ConOps / SDM / CDM / Influence Diagram 在现有 AI 开发工具中有无成熟实现？
- "四层维护存储"（归档/摘要/投影/切片）与 [[Agent Harness 治理协议]] 的"事件时间线 + 快照压缩"是同一思想的不同表述还是不同实现路径？
- "Fork 与胶囊"返回"结构化判断而不是全部细节"与 [[ESAA]] 的 boundary contracts 在数据契约层面是否同源？
- 宏观评估的 `behavior_pattern` 能否反向自动生成新的底层评估 rubric（self-extending eval）？
- BERTopic 风格 vs 直接 LLM 主题归纳在 agent trace 上的稳定性差异如何量化？
- `suspect_score` 的 `0.4/0.3/0.2/0.1` 权重在不同 agent 系统上是否需要重新校准？
