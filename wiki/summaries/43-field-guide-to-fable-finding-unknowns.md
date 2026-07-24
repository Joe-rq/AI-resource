---
title: "A Field Guide to Fable: Finding Your Unknowns"
type: summary
created: 2026-07-14
updated: 2026-07-14
sources: ["raw/articles/2026-07-03-field-guide-to-fable-finding-unknowns.md"]
tags: [agentic-coding, prompting, unknowns, blind-spot, prototyping, fable, anthropic, thariq-shihipar]
---

# A Field Guide to Fable: Finding Your Unknowns

> 原始作者：Thariq Shihipar（Member of Technical Staff, Anthropic），@trq212
> 原始来源：[Anthropic 官方博客](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns) / [X 帖](https://x.com/trq212/status/2073100352921215386)（2026-07-03）
> 互动：3.7M views · 262 replies · 1.2K reposts · 9.3K likes · 21K bookmarks
> 本 wiki 摄取日期：2026-07-14

## 摘要

Anthropic 配合 Fable 5 发布的官方 field guide。核心论点：**减少并规划你的未知（unknowns），就是 agentic coding 这项技能本身**。文章把 Rumsfeld 四象限（Known Knowns / Known Unknowns / Unknown Knowns / Unknown Unknowns）应用到人-agent 协作，并给出覆盖 pre-implementation / during / post 三阶段的技巧工具箱，每个技巧附可直接抄用的 example prompt。框架抽取为概念页 [[Finding Your Unknowns]]；本页保留原文细节、示例 prompt 与实战案例。

> 观察锚点：最好的 agentic coder（文中点名 Boris、Jarred）未知很少——对 codebase 和模型行为 deeply in-sync——但他们同时**假设未知存在**。

## 四象限 Unknowns

- **Known Knowns** — 本质上就是 prompt 里写的东西
- **Known Unknowns** — 知道自己还没想清楚的
- **Unknown Knowns** — 显而易见到从不写下、但看到就认得的
- **Unknown Unknowns** — 完全没考虑到的；"你知道东西能好到什么程度吗？"

指令的两难：太具体则该 pivot 时 Claude 死守指令；太模糊则 Claude 按业界最佳实践自行假设。不管理未知则两头都输。Claude 能帮你更快发现未知——它搜 codebase 和互联网极快，对平均话题知道得比你多，从失败中迭代也更快。**最重要的是交代你的起点**：你在思考过程的哪一步、你对问题和 codebase 的经验，让它像 thought partner 一样与你工作。

## 技巧与 example prompts

### Pre-implementation

**Blind Spot Pass**（对治 unknown unknowns）— 在新领域/陌生 codebase 开工时，用字面词 "blind spot pass"、"unknown unknowns" 让 Claude 找盲区并教你：

> "I'm working on adding a new auth provider but I know nothing about the auth modules in this codebase. Can you do a blind spot pass to help me figure out my relevant unknown unknowns and help me prompt you better."

> "I don't know what color grading is but I need to grade this video. Can you teach me to understand my unknown unknowns about color grading, so that I can prompt better?"

**Brainstorms & Prototypes**（对治 unknown knowns）— "see it to know it" 的标准要在 prototype 期言语化，实现期才发现代价高（spec 小变动会引发实现巨变，agent 回滚旧改动更难）。作者几乎每个 coding session 都以探索/头脑风暴开场，防止 scope 过窄或过宽：

> "I want a dashboard for this data but I have no visual taste and don't know what's possible. Make me an HTML page with 4 wildly different design directions so I can react to them."

> "Before wiring anything up, make a single HTML file mocking the new editor toolbar with fake data. I want to react to the layout before you touch the real app."

> "Here's my rough problem: users churn after onboarding. Search the codebase and brainstorm 10 places we could intervene, from cheapest to most ambitious. I'll tell you which ones resonate."

**Interviews**（对治 known unknowns）— brainstorm 后仍有未知时让 Claude 采访你：

> "Interview me one question at a time about anything ambiguous, prioritize questions where my answer would change the architecture."

**References** — 说不清楚的需求，最好的 reference 是**源码**：指向实现了你要的语义的库/组件（跨语言也行），比截图信息密度高得多：

> "This Rust crate in vendor/rate-limiter implements the exact backoff behavior I want. Read it and reimplement the same semantics in our TypeScript API client."

**Implementation Plans** — 计划聚焦最可能变的部分（数据模型、类型接口、UX 流），让 Claude 浮出你真正需要改的东西：

> "Write an implementation plan in HTML, but lead with the decisions I'm most likely to tweak with: data model changes, new type interfaces, and anything user-facing. Bury the mechanical refactoring at the bottom, I trust you on that part."

### During implementation

**Implementation notes** — 计划满意后开新 session，把 spec/prototype 等 artifacts 传入 prompt（fresh context window + 全部规划信息）。再多规划也有 unknown unknowns 潜伏，让 Claude 记录偏离：

> "Keep an implementation-notes.md file. If you hit an edge case that forces you to deviate from the plan, pick the conservative option, log it under 'Deviations', and keep going."

### Post implementation

**Pitches & Explainers** — 打包成单文档拿 buy-in；评审者从你当初的未知出发，专家想看到你覆盖了他们会预期的失败点：

> "Package the prototype, the spec, and the implementation notes into a single doc I can drop in Slack to get buy-in. Lead with the demo GIF."

**Quizzes** — 长 session 后 Claude 做的比你意识到的多，读 diff 只有浅理解（行为依赖既有代码路径）。**全对才 merge**：

> "I want to make sure I understand everything that's happened in this change. Give me a HTML report on the changes for me to read and understand with context, intuition, what was done, etc. and a quiz at the bottom on the changes that I must pass."

## 实战案例：Fable 发布视频

Fable launch video 端到端用 Claude Code 剪辑，作者并非视频专家，全程演示方法论：

1. **从 known 出发** — 知道 Claude 能用代码剪视频/转录，但不确定精度 → 让 Claude 讲解 Whisper 类转录原理、ffmpeg 能否精确剪掉 um 和长停顿
2. **prototype 验证可行性** — 不确定"UI 与语音逐词同步"是否可行 → 用 Remotion + 转录先做 prototype video
3. **blind spot pass 学习** — 视频发闷，知道是 color grading 但不懂 color grading → 第一次尝试"做几个变体挑一个"失败（不知道 good 长什么样）→ 改为让 Claude 教 color grading 来发现未知

案例 3 展示了技巧选择的自我纠错：**unknown knowns 的技巧（做变体挑）对 unknown unknowns（不知道 good 长什么样）无效**，要先降维成教学。

## 关键洞察

1. **未知管理是 prompt 质量的上游** — [[Context Engineering]] 的 write/select 假设你知道该给什么 context；本框架补的是"发现该给但你不知道要给的"。四象限给了失败诊断维度：prompt 不 work，先问是哪类未知没处理。

2. **"模型越强，方法越值钱"** — "The better models get, the more you can achieve with the right approach. When a long-horizon task comes back wrong, it's likely you need to spend more time defining your unknowns"——把长程任务失败归因于未知定义不足而非模型能力，与 [[AI Capability Overhang]] 同构：能力已在，释放靠方法。

3. **廉价探测 vs 昂贵修复** — 每个 explainer/brainstorm/interview/prototype/reference 都是"在修复变贵之前廉价发现未知"。这是 [[Harness Cybernetics]] 前馈端的人类侧版本：guides 防患于未然，只是这里被 guide 的是人的认知而非 agent 行为。

4. **Quiz 是反向 verifier** — [[Worker Verifier 对抗循环]] 验证 agent 的产出；quiz 验证**人对产出的理解**，"pass the quiz perfectly" 才 merge 把人的理解也纳入质量门。agent 产码时代 review 瓶颈在人的理解带宽（cf. [[Agentic Code Review]] 四倍代码一成价值）。

5. **fresh session + artifacts 是规划-实现的接缝** — 计划期产物（spec、prototype、plan）作为 artifacts 传入新 session，既拿到干净 context window 又保留全部规划信息。与 [[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）|fresh session over resume]] 一致。

## 与现有 Wiki 概念的关联

| 本文概念 | Wiki 对应 |
|---------|----------|
| 四象限 Unknowns 框架 | [[Finding Your Unknowns]] — 抽取为可复用概念页 |
| context 给足 vs 给对 | [[Context Engineering]] — 本框架是其人类认知侧上游 |
| 意图先行、开工前校准 | [[Meta Reflection Techniques]] — 行动之环意图象限 |
| Quiz 验证人的理解 | [[Agentic Code Review]] — intent reconstruction 的自我版本 |
| 指令过糊 → agent 自行假设 | [[Agentic Laziness]] / [[Goal Drift]] — 失效模式的前馈端对治 |
| 长程任务失败归因于方法 | [[AI Capability Overhang]] — 能力已在，释放靠方法 |
| fresh session + artifacts | [[Stateless Reducer]] — 状态外置、context 可重建 |

## 相关资源

- [Anthropic 官方博客原文](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)
- [示例页面（thariqs.github.io）](https://thariqs.github.io/html-effectiveness/unknowns/)
- [AI Engineer 演讲视频](https://www.youtube.com/watch?v=9fubhllmsBU)
