# AI Resource Wiki Knowledge Base

> Schema document — read at the start of every session together with `wiki/index.md`.
> Update after every major compile, ingest batch, or structural change.

## Scope

What this wiki covers:
- **Agent 平台与基础设施层** — Runtime / Multi-agent / Harness / 工具定义
- **Claude Code Skill 开发** — Skill 编写流程、SKILL.md 规范
- **多 Agent 协作架构** — Orchestrator/Specialist、Worker/Verifier 对抗循环、Team Engine、自动扩张任务图
- **Agent 治理协议** — 跨 session 一致性、事件溯源、概念演化、双层验证
- **行业研究** — MiniMax、Anthropic、NVIDIA、Cline、OpenAI、wow-harness 等公司和项目的 Agent 平台实践

What this wiki deliberately excludes:
- 模型训练/微调细节
- 与 Agent 平台无关的纯应用层话题

## Operations

This wiki follows the llm-wiki skill's five operations: `compile`, `ingest`, `query`, `lint`, `audit`.
Every operation appends an entry to `log/YYYYMMDD.md`.

### Log entry template (from 2026-06-04)

```
## [operation] title
- Source: 源路径
- 主题: 1-2 句
- New pages: 列表
- Updated pages: 列表
- Wikilink: 概念列表
- Lint: pass/fail
```

> Legacy files (`log/20260519.md`, `log/20260521.md`) 保留旧格式，不追溯重写。新增条目一律使用上述模板。

## Naming conventions

### Pages
- **Concept pages** (`wiki/concepts/`): Title Case noun phrases. E.g., "Agent Runtime", "Multi-Agent Architecture".
- **Folder-split concepts** (`wiki/concepts/<topic>/`): used when a topic would exceed ~1200 words as a single page. Contains `index.md` + one file per aspect.
- **Entity pages** (`wiki/entities/`): Proper names. E.g., "MiniMax Mavis", "Claude Code", "Cline". Entity 文件名**优先使用品牌官方写法**（如 `MiniMax-Mavis` 保持现状，不简写为 `mavis`），便于与外部引用对齐。
- **Summary pages** (`wiki/summaries/`): kebab-case source slug. E.g., "08-agent-runtime-battlefield".

### Wikilinks
- Always use `[[Page Title]]` — exact page title, case-sensitive.
- For folder-split pages, link to the index: `[[concepts/Foo/index|Foo]]`.
- Link the first mention of every entity or concept. Do not link the same page more than twice per article.

### Frontmatter
Every wiki page has YAML frontmatter:
```yaml
---
title: <Page Title>
type: concept | entity | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [list of raw/ slugs this page draws from]
tags: [relevant tags]
parent: <path-to-index>  # 可选 — folder-split 子页指向 index 页
---
```

> Entity 页面**不**需要 `entity_type` 字段；分类信息通过 `tags` 表达（如 `tags: [company, agent-platform, anthropic]`），保持 frontmatter 简洁。

### Diagrams and formulas
- All diagrams are **mermaid**. No ASCII art.
- All formulas are **KaTeX** (inline `$...$` or block `$$...$$`).

### Raw file policy
- Small text sources → copy into `raw/<subfolder>/`.
- Large binaries → create a pointer file at `raw/refs/<slug>.md` with `kind: ref` frontmatter and an `external_path` field. Do not copy the binary.

## Current articles

### Concepts
- Agent-Runtime — 单 Agent 执行环境
- Agent-Secure-Runtime — Agent 安全运行时（三层安全检查 + 沙箱隔离）
- Agent-Harness-治理协议 — 跨 session、跨 agent 的长期一致性治理（事件溯源、概念演化、双层验证、自动扩张任务图、人机决策分层）
- Multi-Agent-协作模式 — 四种核心协作模式
- Worker-Verifier-对抗循环 — Mavis 核心架构机制
- Agent-Memory — Agent 长期记忆（图谱结构、向量检索、自我进化）
- Claude-Code-Subagent/index — Subagent：独立上下文工作者（内置类型、自定义定义、Fork 模式、持久内存、Hooks）
- Claude-Code-Skills/index — Skills 扩展机制（SKILL.md 定义、动态上下文注入、Subagent 中运行、调用控制）

### Entities
- MiniMax-Mavis — MiniMax 的 Agent 产品
- NVIDIA-Agent-Toolkit — NVIDIA Agent 开发工具包
- wow-harness — wow-harness v3 治理协议（事件溯源 + 概念演化 + 双层验证 + 自动扩张任务图）
- Dive-into-Claude-Code — Claude Code 源码级逆向工程分析论文（5 设计价值、13 设计原则、7 组件结构、5 层子系统）
- ESAA — ESAA: Event Sourcing for Autonomous Agents（Event Sourcing + CQRS、immutable audit trail、deterministic replay、两个 case study 验证）
- NanoClaw — ~500行代码的轻量级 Agent 框架（Claude Agent SDK）
- Nous-Research — 硅谷 AI 实验室，Hermes Agent（11万星）

### Summaries
- 10-singapore-fm-nanoclaws-second-brain — 新加坡外長的 AI 第二大腦（NanoClaw + Raspberry Pi）
- 11-hermes-agent-nous-research — Hermes Agent / Nous Research（长期记忆 + 自我进化）
- 09-claude-subagent-tutorial — Claude Code Subagent 小白入门教程
- nvidia-agent-toolkit — NVIDIA Agent Toolkit 架构图
- 08-agent-runtime-battlefield — Agent Runtime 主战场
- 01-minimax-single-ai-not-enough — 单 AI 的四个结构性缺陷
- 04-anthropic-multi-agent-research-system — Anthropic Orchestrator-Worker 架构
- 05-anthropic-managed-agents-api — Anthropic 共享容器 + Session Thread 隔离
- 06-claude-code-agent-teams — Claude Code Team Lead + Teammates
- 14-building-skill-for-claude — Claude Code Skill 开发流程
- 02-minimax-agent-team-tech-report — Mavis 详细技术报告
- 14-building-skill-for-claude-zh — Skill 开发指南（中文）
- project-overview — AI Resource 项目介绍

## Open research questions

- Agent Runtime 的具体实现差异（Prompt 设计/工具定义/上下文管理/错误处理）具体怎么影响性能？
- Worker/Verifier 对抗循环的收敛条件是什么？何时终止对抗？
- Claude Code Agent Teams 和 Anthropic Managed Agents 的架构有何本质区别？
- Agent Secure Runtime 的三层安全检查（Policy/Network/Privacy）性能开销有多大？
- 自动扩张任务图的收敛和终止条件是什么？事件驱动的 agent spawn 如何避免无限扩张？
- 概念节点的新颖性检查在实践中如何判定？"引入了什么新信息"的边界在哪？
- ESAA 论文的事件溯源 vs wow-harness v3 的事件时间线，在工程实现上有何具体差异？
- "Dive into Claude Code" 论文识别的 5 层 compaction pipeline 在实际使用中的各层触发频率和效果如何？
- Claude Code 的 deny-first 权限系统在 50+ 子命令 fallback 场景下的安全退化程度如何量化？
- ESAA 的 boundary contracts 在企业级 monorepo 场景下是否可扩展？CS2 仅 50 tasks / 86 events
- NanoClaw 的容器化隔離在多租戶場景下的實際安全性如何？
- Hermes 的自我進化機制在醫療監管框架下的合規路徑是什麼？
- Agent Memory 的「遺忘機制」如何設計？全量保留導致上下文膨脹的實際代價
- 分布式 Harness 附着点 vs 独立上下文窗口与现有 Worker/Verifier 概念有何同构/包含关系?
- CGP/IEL 9 件工具组成熟度评估: 哪些工程化已就绪, 哪些仍 PoC?
- 四层维护存储 vs 事件时间线: 分布式 Harness 存储抽象是否可由 wow-harness v3 事件时间线统一表达?

## Research gaps

Sources to ingest:
- [ ] Anthropic Claude Cowork 官方文档
- [ ] Cline SDK 技术博客原文
- [ ] LangChain Deep Agents benchmark 原始数据
- [x] ESAA 论文 (Event Sourcing for Autonomous Agents, arxiv 2602.23193) 原文
- [x] "Dive into Claude Code" 论文 (arxiv 2604.14228) 原文

## Audit backlog

*(none — run `python3 scripts/audit_review.py <wiki-root> --open` to refresh)*

## Notes for the LLM

- Language: **bilingual** (中英文混合)
- Tone: neutral, technical, research-focused
- Depth: deep technical analysis with practical implications
- Handling contradictions: state both positions, cite sources, add to Open Research Questions
