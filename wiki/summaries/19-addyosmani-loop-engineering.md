---
title: "Loop Engineering：从 Prompt 到系统设计"
type: summary
created: 2026-06-11
updated: 2026-06-11
sources: ["raw/articles/2026-06-08-addyosmani-loop-engineering"]
tags: [loop-engineering, claude-code, codex, agent-orchestration, automation, subagent, skill, worktree, mcp, token-cost]
---

# Loop Engineering：从 Prompt 到系统设计

> 原始作者：Addy Osmani（@addyosmani），Google Cloud AI / 前 Google Chrome 工程负责人  
> 原始来源：[X/Twitter](https://x.com/addyosmani/status/2064127981161959567)（2026-06-08）  
> 阅读量：1.7M  
> 本 wiki 摄取日期：2026-06-11

## 摘要

**Loop Engineering（循环工程）** 的核心判断：

> **不要再亲自给 coding agent 写 prompt 了。你应该设计一套"循环"系统，让系统自己去驱动 agent。**

过去两年，使用 coding agent 的方式是"你写 prompt → 看结果 → 再写 prompt"，agent 是工具、你是握工具的人。Loop Engineering 认为这个模式正在结束——取而代之的是你**设计一个小型系统**，让它自动发现工作、分发任务、检查结果、记录状态、决定下一步。

一个 loop 需要 **5 个模块 + 1 个外部记忆**。令人惊讶的是，Claude Code 和 Codex 这两个产品如今已经**同时具备了全部五项能力**，而且能力形状几乎相同——这意味着 loop 设计正在从"工具专属"变成"跨工具通用"的抽象层。

---

## 核心论点

### 从 Prompt Engineering 到 Loop Design

@steipete："You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

@bcherny（Anthropic, head of Claude Code）："I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

Addy Osmani 的解读：

> **杠杆点转移了。** 工作没有变容易，变的是你在哪里施加杠杆。Prompt engineering 优化的是单次交互；loop engineering 优化的是整个工作流的自动化结构。

### 五个模块 + 一个记忆

| # | 模块 | 作用 | Codex 实现 | Claude Code 实现 |
|---|------|------|-----------|-----------------|
| 1 | **Automations** | 定时触发、自动发现与分类 | Automations 标签页 + Triage inbox | `/loop` + cron + hooks + GitHub Actions |
| 2 | **Worktrees** | 并行 agent 互不冲突的隔离环境 | 内置多线程 worktree | `git worktree` + `--worktree` flag + `isolation: worktree` |
| 3 | **Skills** | 把项目知识写成文件，避免每次从零解释 | `$skill-name` 调用 + 自动匹配 | `.claude/skills/` 目录 + 动态注入 |
| 4 | **Plugins / Connectors (MCP)** | 让 agent 接入真实工具链（issue tracker、Slack、API） | MCP 连接器 | MCP 连接器 |
| 5 | **Sub-agents** | 写代码的 agent 和审查的 agent 分离 | `.codex/agents/` TOML 定义 | `.claude/agents/` + agent teams |
| 6 | **Memory** | 跨会话持久化状态（markdown / Linear / 状态文件） | 磁盘状态文件 | 磁盘状态文件 |

> 第六项 Memory 虽然听起来"太简单而不重要"，但它是所有长期运行 agent 的命脉——**模型每次运行后遗忘一切，记忆必须在磁盘上，不能在上下文里。**

---

## 模块详解

### 1. Automations — 心跳

Automations 让 loop 成为"循环"而非"一次性运行"。

- **Codex**：在 Automations 标签页创建，指定项目、prompt、频率、本地/后台 worktree。发现问题的运行进入 Triage inbox，无问题的自动归档。OpenAI 内部用来自动化日常 issue 分类、CI 失败摘要、commit briefing、bug 追踪。Automation 可以调用 skill，避免把大段指令硬编码进调度器。
- **Claude Code**：通过 `/loop`（按间隔重跑）、cron 任务、hooks（在 agent 生命周期关键点触发 shell 命令）、或推送到 GitHub Actions（关闭笔记本后继续运行）。

**关键原语**：`/goal` — 不是按时间循环，而是按条件循环。你给出一个可验证的停止条件（如 `"all tests in test/auth pass and lint is clean"`），每轮结束后由**另一个小模型**检查是否达成，写代码的 agent 不负责给自己打分。Codex 也有同名 `/goal` 功能。

### 2. Worktrees — 并行不 chaos

两个 agent 写同一个文件 = 两个工程师没沟通就 commit 到同一行。Git worktree 提供独立的 working directory + 独立 branch，共享 repo history，**物理上隔离碰撞**。

- **Codex**：内置 worktree 支持，多线程同时操作同一 repo。
- **Claude Code**：`git worktree` + `--worktree` flag 开启独立 checkout session + `isolation: worktree` 设置让 subagent 在干净环境中运行并自动清理。

> 人仍是天花板：worktree 消除了机械碰撞，但**你的 review 带宽**决定了你能并行运行多少个 loop。

### 3. Skills — 停止像金鱼一样重复解释

Skill 是**意图债务（intent debt）**的解药。Agent 每次启动都是"冷启动"，会用自信猜测填补你意图中的任何空洞。Skill 把意图写在外部——约定、构建步骤、"那次事故后我们不再这样做"——agent 每次运行都读。

- **格式**：文件夹 + `SKILL.md` + 可选 `scripts/`、`references/`、`assets/`。
- **Codex**：`$skill-name` 或 `/skills` 调用，或根据任务描述自动匹配。
- **Claude Code**：`.claude/skills/` 目录，相同格式。

> Skill 是**创作格式**，plugin 是**分发格式**。要跨 repo 共享或打包多个 skill 时，做成 plugin。Codex 和 Claude Code 都支持。

### 4. Plugins / Connectors — Loop 触碰真实工具

只看文件系统的 loop 是 tiny loop。基于 MCP 的 connectors 让 agent 能读 issue tracker、查数据库、调 staging API、发 Slack 消息。

- Codex 和 Claude Code 都讲 MCP，**为一个写的 connector 通常直接在另一个工作**。
- Plugin 把 connectors + skills 打包，队友一键安装整套 setup。

这是"agent 告诉你 fix 是什么"和"loop 自己开 PR、关联 Linear ticket、CI 绿了就 ping 频道"之间的区别。

### 5. Sub-agents — 让写的人远离检查的人

最有用的结构：**maker / checker 分离**。写代码的模型对自己的作业太宽容，第二个 agent（不同指令、有时不同模型）能抓住第一个 agent 自我说服的盲点。

- **Codex**：`.codex/agents/` 下 TOML 文件定义，每个 agent 有 name、description、instructions、可选 model 和 reasoning effort。安全审查员可以是强模型高 effort，探索员可以是轻量只读模型。
- **Claude Code**：`.claude/agents/` + agent teams，工作流通常是 explore → implement → verify against spec。

> Sub-agents 烧更多 token（每个 agent 独立模型调用 + 工具调用），**只在值得买第二意见的地方花**。

Claude Code 的 `/goal` 底层也是这个机制：一个 fresh model 判断 loop 是否完成，maker/checker 分离应用到停止条件本身。

---

## 一个完整 Loop 的示例

Addy Osmani 描述的日常 loop：

```
每天早上 Automation 扫描 repo
  → Triage skill 读取昨日 CI 失败、open issues、recent commits
  → 发现写入 markdown / Linear board
  → 每个值得做的 finding：
      打开独立 worktree
      → Sub-agent A 起草 fix
      → Sub-agent B 对照 project skills + 现有 tests 审查
  → Connectors 自动开 PR、更新 ticket
  → 搞不定的进入 triage inbox 等人处理
  → 状态文件记住：试了啥、过了啥、还开着啥
明天早上从今天的断点继续
```

> 你**只设计了一次**。你没有 prompt 任何一步。这就是 Steinberger 的观点成真——而且同一个 loop 在 Codex 或 Claude Code 里都能跑，因为模块形状相同。

---

## Loop 不会替你做的事（三个 sharper 的问题）

Loop 越好用，以下三个问题**越尖锐**，不是越容易：

### 1. Verification 仍是你的责任

无人值守运行的 loop = 无人值守犯错的 loop。Verifier sub-agent 让 loop 的"done"有点意义，但 **"done"是 claim 不是 proof**。你的工作是 ship 你确认能工作的代码。

### 2. Comprehension Debt（理解债务）

Loop 越快 ship 你没写的代码，**"代码存在"与"你真正理解"之间的 gap 越大**。Smooth loop 只会让 comprehension debt 增长更快——除非你读 loop 产出的东西。

### 3. Cognitive Surrender（认知投降）

Loop 自己运行时，很容易停止有主见、接受 loop 给的一切。设计 loop 用判断力时是解药，用 loop 逃避思考时是加速器——**同一个动作，相反结果**。

> **Build the loop. Stay the engineer.**

---

## 与现有 Wiki 概念的关联

| 本文概念 | Wiki 对应 |
|---------|----------|
| Sub-agents (maker/checker) | [[Worker Verifier 对抗循环]] — Mavis 核心架构机制的同构实现 |
| Skills 作为意图固化 | [[Claude Code Skills]] — SKILL.md 规范、动态上下文注入 |
| Worktree 隔离 | [[Claude Code Subagent]] — Fork 模式、独立上下文窗口 |
| Loop 的跨 session 一致性 | [[Agent Harness 治理协议]] — 事件溯源 + 概念演化 + 双层验证 |
| Skill 是方法调用 | [[Thin Harness, Fat Skills]] — "套具要瘦、技能要胖"的架构原则 |
| 自主运行 + 人工确认门 | [[Autonomous AI System]] — 阳志平 12 技巧 × 4 组（任务编排/实际开工/自检评审/自动续航） |
| Claude Code 5 层 compaction | [[Dive into Claude Code（论文）]] — 论文识别的 5 层 compaction pipeline 在 loop 长期运行中的触发频率 |
| Memory 必须落盘 | [[ESAA]] — Event Sourcing + CQRS，immutable audit trail，跨会话 deterministic replay |

---

## 关键洞察

1. **工具无关性**：Steinberger 的五模块清单几乎同时映射到 Codex 和 Claude Code——一旦注意到形状相同，就停止争论"哪个工具更好"，转而设计跨工具通用的 loop。

2. **杠杆点转移**：Cherny 的观点不是工作变容易了，是**杠杆点从 prompt 层转移到了系统架构层**。Loop design 比 prompt engineering 更难，因为同一个 loop 给懂行的人加速、给偷懒的人制造 debt。

3. **Token 成本是真实约束**：Loop 的 token 消耗模式在"token rich"和"token poor"场景下差异巨大。Sub-agents 每个都独立计费，只在值得的地方买第二意见。

4. **质量不自动保证**：Loop 不会删除你，只会改变你的工作形态。"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."

5. **直接 prompt 仍有效**：Loop 不是替代直接 prompt，而是补充。关键是找到平衡——对理解深的工作用 loop 加速，对理解浅的工作先理解再 loop。

---

## 术语表

| 术语 | 定义 |
|------|------|
| Loop Engineering | 设计系统自动驱动 agent 完成递归目标，取代人工逐轮 prompt |
| Automation | 定时/条件触发的自主任务，loop 的心跳 |
| Worktree | Git 独立 working directory，隔离并行 agent 的文件冲突 |
| Skill | 封装项目知识的标准化 markdown 文档，agent 每次运行自动读取 |
| Connector (MCP) | 基于 MCP 协议的插件，让 agent 接入外部工具链 |
| Sub-agent | 独立上下文窗口的辅助 agent，通常与主 agent 分工（explore/implement/verify） |
| Memory (外部) | 磁盘上的状态文件，跨会话持久化 loop 进度 |
| Comprehension Debt | 代码存在但你未真正理解的累积差距 |
| Cognitive Surrender | 因 loop 自动化而放弃独立判断的倾向 |
| Slop | 低质量、未经审查的 AI 生成代码 |
