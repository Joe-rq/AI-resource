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

## Hooks

Hooks are configured in `.claude/settings.json`. Three hook event types are used, each with a distinct role:

| Event | Role | Trigger | Can Block? | Max Overhead |
|-------|------|---------|------------|-------------|
| **PreToolUse** | Safety valve | Before matched tool executes | Yes (`exit 1`) | <100ms |
| **PostToolUse** | Quality gate | After matched tool completes | No (warn only) | <500ms |
| **Stop** | Status awareness | Every tool call + end of turn | No (warn only) | <10ms |

### Implemented hooks

**PostToolUse (Write/Edit)** — Wiki quality checks after file modification:
- Guard: `git diff --name-only | grep 'wiki/*.md'` — skip if no wiki changes
- `scripts/lint_frontmatter.py` — validate YAML frontmatter (required fields, types, dates, legacy fields)
- `scripts/lint_redundant_aliases.py` — detect `[[X|X]]` redundant aliases and path-based wikilinks
- `scripts/lint_wikilinks.py` — detect orphan wikilinks pointing to non-existent pages

**Stop (all)** — Lightweight environment checks:
- Detect `.DS_Store` in staging area (single grep, <5ms)

### Planned hooks (priority order)

- **P0 — PreToolUse `Bash(git commit*)`**: Enforce conventional commit format (`feat:`/`fix:`/`docs:`/`chore:`/`refactor:`). Block non-conforming commits with `exit 1`.
- **P1 — PostToolUse (Write/Edit)**: Check CLAUDE.md self-consistency — verify that pages listed under `### Concepts`/`### Entities`/`### Summaries` match actual `wiki/` files.
- **P1 — PreToolUse (Write/Edit)**: Warn when writing to `raw/` directory — "raw/ is for source material. Consider using ingest.py instead." (warn only, `exit 0`)
- **P2 — PostToolUse (Write/Edit)**: Validate log entry format in `log/*.md` — check for `## [operation] title` header and required fields (Source, New pages, Updated pages, Wikilink, Lint).
- **P2 — PreToolUse `Bash(git push*)`**: Check CI status before push — `gh run list --limit 5 --status failure`.
- **P3 — Stop (all)**: Session duration reminder (>30 min) and uncommitted change accumulation warning (>200 lines).

### Hook vs Skill boundary

| Layer | Trigger | Nature | Examples |
|-------|---------|--------|----------|
| **PreToolUse** | Auto (before tool) | Block/warn | Commit format, raw/ write warning, CI check |
| **PostToolUse** | Auto (after Write/Edit) | Mechanical validation | Frontmatter, wikilinks, CLAUDE.md consistency |
| **Stop** | Auto (every tool call) | Lightweight reminder | .DS_Store, session duration, change accumulation |
| **Skill (`llm-wiki`)** | Manual | LLM reasoning | Semantic coherence, content quality, structural review |
| **Skill (`42plugin-skill-reviewer`)** | Manual | LLM reasoning | Skill quality scoring |
| **Script (audit/compile/ingest)** | Manual | LLM-driven or semi-auto | Audit backlog, content creation |

### Design principles

1. **Hooks do not replace Skills.** Hooks run deterministic shell checks; Skills need LLM reasoning.
2. **Stop hooks must stay under 10ms.** They fire on every tool call — any latency multiplies across the session.
3. **PreToolUse is the only place that can say "no".** Use `exit 1` to block; use `exit 0` to warn without blocking.
4. **PostToolUse uses `git diff` as guard, not env vars.** Claude Code's hook context variables are not fully documented; `git diff` is deterministic and always correct.
5. **Non-zero exit = warning, not blocking (PostToolUse/Stop).** Only PreToolUse `exit 1` actually prevents the operation.

### PreToolUse vs PostToolUse: when to block vs when to warn

A recurring design question is whether a check belongs in PreToolUse (block before write) or PostToolUse (warn after write). The decision matrix:

| Factor | Favors PreToolUse (block) | Favors PostToolUse (warn) |
|--------|--------------------------|--------------------------|
| **Severity** | Would cause CI failure, data loss, or broken links | Cosmetic, recoverable, or non-blocking |
| **False positive risk** | Near-zero — the check is deterministic and unambiguous | Some risk — blocking would be too aggressive |
| **Context availability** | All needed info is in the tool arguments (reliably available) | Need to inspect actual file state on disk |
| **Fix cost** | Hard to fix later (e.g., bad commit message) | Easy to fix in a follow-up edit |

**Examples from this project:**

| Check | Placement | Reason |
|-------|-----------|--------|
| Redundant `[[X\|X]]` alias | PostToolUse (current) | PreToolUse would be ideal (block before write) but hook context for Write/Edit content is not reliably documented. PostToolUse via `git diff` is the pragmatic choice. |
| Path-based wikilinks | PostToolUse (current) | Same rationale — would benefit from PreToolUse blocking but constrained by context availability. |
| Legacy frontmatter fields | PostToolUse (current) | Correct placement — legacy fields are harmless redundancy. Blocking writes over them would be too aggressive. |
| Empty `sources` field | PostToolUse (current) | Correct placement — `type: index` pages legitimately have empty sources. Blocking would cause false positives. |
| Commit message format | PreToolUse (planned P0) | Correct placement — commit messages are hard to fix after the fact, and the check (conventional commit regex) has near-zero false positive risk. |
| `.DS_Store` in staging | Stop (current) | Correct placement — needs to run after any `git add`, not tied to a specific tool. Must be lightweight (<5ms). |

**When to choose PreToolUse:**
- The check is unambiguous with near-zero false positives
- Fixing the problem after the fact is expensive or impossible (e.g., pushed commits)
- The tool arguments reliably contain the data needed for the check

**When to choose PostToolUse:**
- The check needs to inspect actual file state on disk
- False positives are possible and blocking would be disruptive
- The problem is cosmetic or easily fixed in a follow-up edit
- Hook context for the tool is not reliably documented

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
- Agentic-Code-Review — agent 产码时代的评审经济学（blast radius 分层 / intent reconstruction / 异构多审稿 / human on the loop）
- Agent-Memory — Agent 长期记忆（图谱结构、向量检索、自我进化）
- Claude-Code-Subagent/index — Subagent：独立上下文工作者（内置类型、自定义定义、Fork 模式、持久内存、Hooks）
- Claude-Code-Skills/index — Skills 扩展机制（SKILL.md 定义、动态上下文注入、Subagent 中运行、调用控制）
- Thin-Harness-Fat-Skills — 套具要瘦、技能要胖（5 定义 + 3 反模式 + 三层架构 + Self-rewriting skill 循环）
- Meta-Reflection-Techniques — 阳志平 12 个元反思技巧（行动之环 × 4 象限：意图/实施/反馈/情境）
- Autonomous-AI-System — AI 自主系统 4 组 12 技巧（任务编排/实际开工/自检评审/自动续航；与 harness 视角互补）
- Heartbeat-Watchdog — 心跳看门狗三层互检（L0 常驻 shell guard / L1 durable cron / L2 业务自报）；独立守护层对治运行时脆弱与停滞（来源：Deli_AutoResearch）
- Agent-Macro-Evaluation — Agent 宏观评估方法论（4 层标签 + BERTopic 风格聚类 + AgentTrace 风格诊断 + 3 个核心公式）
- Forward-Deployed-Engineering — FDE 前置部署工程（四要素定义、Echo/Delta/Dev 三角循环、碎石路→柏油路飞轮、AI 时代复兴原因）
- AI-Capability-Overhang — AI 能力悬置（模型能力已存在但未被组织释放；FDE 成因；与补偿面镜像）
- Claude-Code-Dynamic-Workflows-Practical-Guide — Claude Code 动态工作流实践指南（场景选择决策树、命令速查、14 个推荐场景与最佳实践）
- Agentic-Laziness — 智能体偷懒（Dynamic Workflows 失效模式之一：Agent 走捷径、过早宣布完成）
- Self-Preferential-Bias — 自我偏好偏差（Dynamic Workflows 失效模式之一：坚持自己输出、拒绝有效反馈）
- Goal-Drift — 目标漂移（Dynamic Workflows 失效模式之一：逐步偏离原始目标而不自知）
- Quarantine-Mode — 隔离模式（Dynamic Workflows 安全模式：读未受信内容 agent 与高权限动作 agent 结构隔离）
- Tournament-Mode — 锦标赛模式（Dynamic Workflows 评估模式：pairwise 比较与 transitivity 假设）

### Entities
- MiniMax-Mavis — MiniMax 的 Agent 产品
- NVIDIA-Agent-Toolkit — NVIDIA Agent 开发工具包
- wow-harness — wow-harness v3 治理协议（品牌官方全小写，保持不变）
- Dive-into-Claude-Code — Claude Code 源码级逆向工程分析论文（5 设计价值、13 设计原则、7 组件结构、5 层子系统）（标题：Dive into Claude Code（论文））
- ESAA — ESAA: Event Sourcing for Autonomous Agents（Event Sourcing + CQRS、immutable audit trail、deterministic replay、两个 case study 验证）
- NanoClaw — ~500行代码的轻量级 Agent 框架（Claude Agent SDK）
- Nous-Research — 硅谷 AI 实验室，Hermes Agent（11万星）
- Palantir — Palantir Technologies：FDE 模式发明者、Gotham/Foundry/AIP 产品矩阵、Ontology 本体论、反 SaaS 产品哲学
- Cline — 开源 AI coding agent（VS Code 扩展），Runtime benchmark 实证来源（74.2% vs 69.4%）
- Anthropic — Claude 模型族、Claude Code/Agent SDK/Managed Agents 产品矩阵、Orchestrator-Worker 架构
- OpenAI — GPT 模型族、Codex CLI、Handoff 模式、宏观评估方法论（OpenAI Cookbook）
- LangChain — 开源 LLM 框架（chain-based composition + LangGraph），Agent Runtime benchmark 参考点

### Summaries
- 12-a-harness-for-every-task-dynamic-workflows — Anthropic 官方动态工作流深度解读（3 失效模式 + 6 编排模式 + 10 用例 + Quarantine 安全模式）
- 20-macro-evals-for-agentic-systems — OpenAI Cookbook 宏观评估教程（EV 订单 multi-agent + 1000 次合成运行 + Promptfoo + BERTopic + AgentTrace）
- 28-claude-code-dynamic-workflows — Claude Code 动态工作流官方中文功能文档（v2.1.154+ / ultracode / /deep-research / 触发与运行管理）
- 10-singapore-fm-nanoclaws-second-brain — 新加坡外長的 AI 第二大腦（NanoClaw + Raspberry Pi）
- 11-hermes-agent-nous-research — Hermes Agent / Nous Research（长期记忆 + 自我进化）
- 19-addyosmani-loop-engineering — Loop Engineering：从 Prompt 到系统设计（Addy Osmani，5 模块 + 1 记忆，Claude Code / Codex 通用 loop 架构）
- 18-agent-harness-12-components — Agent Harness 12 组件 + 7 决策 + TAO 循环 + Ralph Loop + 8 框架对比
- 15-wow-harness-v3-governance — wow-harness v3 一手分享（事件溯源 + 概念演化 + 双层验证 + 自动扩张任务图 + 人机决策分层）
- 13-thin-harness-fat-skills — Thin Harness, Fat Skills（5 定义 + 3 反模式 + 三层架构 + YC Startup School 实证）
- 16-distributed-harness — 分布式 Harness 哲学（Agent = 显形 / 附着点 / CGP-IEL / 9 件工具组 / 智流网络）
- 30-harness-engineering-survey — Harness Engineering 综述（14 篇文献 / 15 个月 / 三层结构 / 补偿面）
- 31-addyosmani-agentic-code-review — Agentic Code Review（Addy Osmani：四倍代码一成价值 / blast radius 分层 / intent reconstruction / 异构多审稿 / human on the loop）
- 32-harness-engineering-14-steps — Harness Engineering 14 步路线图（0xMovez：三层切分 + 14 步 roadmap + .claude/ 布局）
- 33-zachlloyd-skill-self-improvement-loop — Skills 自我提升闭环（Zach Lloyd/Warp：inner/outer agent loop + GitHub issue triage 实例）
- 34-fde-deep-analysis-v4 — FDE 深度分析 v4（黄奕彬：capability overhang + 四断点 + 双向翻译器 + 三种资产 + DeployCo + 最小交付包/技术红线 + 中国语境）
- 35-deli-auto-research-framework — Deli_AutoResearch 协议框架（Victor Chen：3 失效模式 + 5 行为约束 + 三层心跳看门狗 + fresh session over resume + stall 检测/pivot 结构 + 4 subagent 调度模式 + 工程约束）
- hermes-agent-harness-engineering — (stub) 已合并至 15-wow-harness-v3-governance
- 17-ai-autonomous-system-tips — 阳志平 AI 自主系统 12 技巧（任务编排 / 实际开工 / 自检评审 / 自动续航）
- 29-meta-reflection-techniques — 阳志平 12 个元反思技巧（4 象限 × 行动之环）
- 09-claude-subagent-tutorial — Claude Code Subagent 小白入门教程
- nvidia-agent-toolkit — NVIDIA Agent Toolkit 架构图
- 08-agent-runtime-battlefield — Agent Runtime 主战场
- dive-into-claude-code — Dive into Claude Code 论文（arxiv 2604.14228 / 5 价值 + 13 原则 + 7 组件 + 5 层子系统）
- esaa-paper — ESAA: Event Sourcing for Autonomous Agents 论文（arxiv 2602.23193 / Event Sourcing + CQRS / 两个 case study）
- 01-minimax-single-ai-not-enough — 单 AI 的四个结构性缺陷
- 04-anthropic-multi-agent-research-system — Anthropic Orchestrator-Worker 架构
- 05-anthropic-managed-agents-api — Anthropic 共享容器 + Session Thread 隔离
- 06-claude-code-agent-teams — Claude Code Team Lead + Teammates
- 02-minimax-agent-team-tech-report — Mavis 详细技术报告
- 14-building-skill-for-claude-zh — Skill 开发指南（中文）
- project-overview — AI Resource 项目介绍
- 21-fde-playbook-bob-mcgrew — Bob McGrew FDE 实战手册（Lightcone Podcast）
- 23-colin-jarvis-openai-fde — OpenAI FDE 访谈录（Colin Jarvis：信任、产品、影响）
- 25-fde-future-roundtable — FDE 未来圆桌（OpenAI/Ramp/Nominal/Dataland）
- 27-what-we-talk-about-fde — 当我们谈论 FDE 时（中文深度分析：四要素定义、真假 FDE）

## Open research questions

### Runtime

- [ ] Agent Runtime 的具体实现差异（Prompt 设计/工具定义/上下文管理/错误处理）具体怎么影响性能？ — blocked by: none
- [ ] "Dive into Claude Code" 论文识别的 5 层 compaction pipeline 在实际使用中的各层触发频率和效果如何？ — blocked by: none

### Multi-Agent

- [ ] Worker/Verifier 对抗循环的收敛条件是什么？何时终止对抗？ — blocked by: none
- [ ] Claude Code Agent Teams 和 Anthropic Managed Agents 的架构有何本质区别？ — blocked by: none

### Security

- [ ] Agent Secure Runtime 的三层安全检查（Policy/Network/Privacy）性能开销有多大？ — blocked by: none
- [ ] Claude Code 的 deny-first 权限系统在 50+ 子命令 fallback 场景下的安全退化程度如何量化？ — blocked by: none
- [ ] NanoClaw 的容器化隔離在多租戶場景下的實際安全性如何？ — blocked by: none

### Governance

- [ ] 自动扩张任务图的收敛和终止条件是什么？事件驱动的 agent spawn 如何避免无限扩张？ — blocked by: none
- [ ] 概念节点的新颖性检查在实践中如何判定？"引入了什么新信息"的边界在哪？ — blocked by: none
- [ ] ESAA 论文的事件溯源 vs wow-harness v3 的事件时间线，在工程实现上有何具体差异？ — blocked by: none
- [ ] ESAA 的 boundary contracts 在企业级 monorepo 场景下是否可扩展？CS2 仅 50 tasks / 86 events — blocked by: none

### Long-Horizon Autonomy

- [ ] 三层心跳看门狗在真实多租户/容器化部署中，L0 常驻 shell guard 的跨平台实现与资源开销如何量化？（对比 [[Agent Secure Runtime]] 沙箱隔离） — blocked by: none
- [ ] 2h/4h 阈值与"连续 3 次 nudge"判据在不同任务复杂度、不同模型规模下如何重新校准？能否用 [[Agent Macro Evaluation]] 的运行模式聚类自动发现最优阈值？ — blocked by: none
- [ ] Guardian/Worker 的三权限边界（liveness-check / restart / nudge）能否形式化为 [[ESAA]] boundary contracts 那样的 schema 级硬约束，而非靠 prompt 纪律？ — blocked by: none
- [ ] L1"依赖一个活着的交互 session"在现代 headless/CI 部署中是否成立？纯后台场景下 L0 是否足以单独兜底？ — blocked by: none

### Memory

- [ ] Hermes 的自我進化機制在醫療監管框架下的合規路徑是什麼？ — blocked by: none
- [ ] Agent Memory 的「遺忘機制」如何設計？全量保留導致上下文膨脹的實際代價 — blocked by: [[Agent-Memory]] folder-split sub-pages

### Architecture

- [ ] 分布式 Harness 附着点 vs 独立上下文窗口与现有 Worker/Verifier 概念有何同构/包含关系? — blocked by: none
- [ ] CGP/IEL 9 件工具组成熟度评估: 哪些工程化已就绪, 哪些仍 PoC? — blocked by: none
- [ ] 四层维护存储 vs 事件时间线: 分布式 Harness 存储抽象是否可由 wow-harness v3 事件时间线统一表达? — blocked by: none

### Dynamic Workflows

- [ ] Dynamic Workflows 三种失效模式（Agentic laziness / Self-preferential bias / Goal drift）在不同模型规模与任务长度上的发生率如何量化？ — 概念页已建立（[[Agentic Laziness]], [[Self-Preferential Bias]], [[Goal Drift]]），待定量研究
- [ ] Tournament 模式中 pairwise 比较的 transitivity 假设何时崩溃？(A>B, B>C 但 C>A 的循环判断如何处理？) — 概念页已建立（[[Tournament Mode]]），待定量研究
- [ ] Quarantine 模式（读未受信内容 agent ↮ 高权限动作 agent 结构隔离）在 prompt injection 实际防御中的效果如何？读 agent 能否诱导写 agent 执行隐性指令？ — 概念页已建立（[[Quarantine Mode]]），待定量研究

### Evaluation

- [ ] 宏观评估的 `MACRO_EVALS_DISCOVERY_MIN_CLUSTER_SIZE` 超参数在不同任务规模下如何确定最优值？粒度过粗丢失小众重要模式，过细噪声爆炸 — blocked by: none
- [ ] `suspect_score = 0.4·proximity + 0.3·frequency + 0.2·bridge + 0.1·role` 的权重是 OpenAI 经验值，能否在其他 agent 系统上重新校准的方法论 — blocked by: none
- [ ] 宏观评估发现的 `behavior_pattern` 与 wow-harness v3 概念节点演化结合，能否实现"系统级自我反思循环"？ — blocked by: none

### Summary

| Domain | Count | Blocked | Unblocked |
|--------|-------|---------|-----------|
| Architecture | 3 | 0 | 3 |
| Dynamic Workflows | 3 | 0 | 3 |
| Evaluation | 3 | 0 | 3 |
| Governance | 4 | 0 | 4 |
| Long-Horizon Autonomy | 4 | 0 | 4 |
| Memory | 2 | 1 | 1 |
| Multi-Agent | 2 | 0 | 2 |
| Runtime | 2 | 0 | 2 |
| Security | 3 | 0 | 3 |
| **Total** | **26** | **1** | **25** |

## Research gaps

Sources to ingest (priority order):
- [ ] **P1 — Cline SDK 技术博客原文** — Cline entity 页已建立，但缺少一手架构文档；Cline 是 wiki 中 Agent Runtime benchmark 的核心实证来源
- [ ] **P2 — LangChain Deep Agents benchmark 原始数据** — LangChain entity 页已建立（stub），Deep Agents 方法论和结果数据对 Agent Runtime 性能差异论述有支撑价值
- [ ] **P3 — Anthropic Claude Cowork 官方文档** — Anthropic entity 页已建立，Cowork 是 Anthropic 产品矩阵中唯一缺一手资料的组件
- [x] ESAA 论文 (Event Sourcing for Autonomous Agents, arxiv 2602.23193) 原文
- [x] "Dive into Claude Code" 论文 (arxiv 2604.14228) 原文
- [x] OpenAI Cookbook — Macro Evals for Agentic Systems (2026-05-19)

## Audit backlog

*(none — run `python3 scripts/audit_review.py <wiki-root> --open` to refresh)*

## Notes for the LLM

- Language: **bilingual** (中英文混合)
- Tone: neutral, technical, research-focused
- Depth: deep technical analysis with practical implications
- Handling contradictions: state both positions, cite sources, add to Open Research Questions

## Quality gates

- After every ingest/compile: run `uv run python scripts/lint_wiki.py . && uv run python scripts/check_consistency.py .`. Zero issues before commit.
- Before deleting any wiki page: run `grep -rl "页面标题" wiki/ --include="*.md"` to find and clean inbound wikilinks first.
- Task completion requires state verification, not action reporting: "created the page" ≠ "page has sources and wikilinks".
- After discovering one issue of a type, immediately scan for similar issues (e.g., empty sources, non-wiki wikilinks, wrong parent format).
