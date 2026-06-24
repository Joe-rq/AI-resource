---
title: "Harness engineering: leveraging Codex in an agent-first world \\ OpenAI"
source: "url"
source_file: "https://openai.com/index/harness-engineering/"
created: "2026-06-24T00:00:00Z"
source_url: "https://openai.com/index/harness-engineering/"
extract_method: "web-reader"
author: "Ryan Lopopolo"
affiliation: "OpenAI (Member of Technical Staff)"
published: "2026-05-27"
---

# Harness engineering: leveraging Codex in an agent-first world

OpenAI 第一方 harness engineering 文章。Ryan Lopopolo 记录用 Codex 以 0 行手写代码构建并交付内部产品的 5 个月实验。

## 核心数据

- 5 个月，**0 行手写代码**，约百万行代码
- ~1500 PR，3 工程师 → 平均 3.5 PR/engineer/day（团队长到 7 人后吞吐反而上升）
- 估计为手写的 1/10 时间
- 内部每日用户 + 外部 alpha，真实发布/部署/修复

## 核心命题

> "**Humans steer. Agents execute.**"

> 工程师的主要工作不再是写代码，而是"design environments, specify intent, and build feedback loops that allow Codex agents to do reliable work"。

## Redefining the role of the engineer

agent 缺能力时，修法几乎从不是"try harder"，而是问"缺什么能力，如何让它对 agent 既 legible 又 enforceable"。失败时人类介入问：缺什么 capability。

PR 驱动：描述任务 → 跑 agent → 开 PR → Codex 自审 + 请求 agent review（本地+云）+ 响应反馈 + 循环到所有 agent reviewer 满意（**Ralph Wiggum Loop**）。人可 review 但非必须——review 越来越多 agent-to-agent。

## Increasing application legibility

bottleneck 变成人 QA 能力。把 app UI/logs/metrics 做成 Codex 直接可读：
- per-git-worktree bootable（每改动能起一个实例）
- Chrome DevTools Protocol 接入 runtime，DOM snapshots/screenshots/navigation 的 skills
- 可观测性：LogQL 查日志、PromQL 查指标
- 单次 Codex run 可在单任务上工作 6 小时（人睡觉时）

## Context management：map, not manual（核心教训）

> "give Codex a map, not a 1,000-page instruction manual."

- **Context is a scarce resource** —— 巨型指令文件挤占任务/代码/docs
- **Too much guidance becomes non-guidance** —— 当一切"重要"，没有重要的；agent 局部 pattern-match 而非有意导航
- **It rots instantly** —— 单体手册变陈规坟场，agent 分不清真假，人停止维护
- **It's hard to verify** —— 单 blob 无法机械检查（覆盖/新鲜度/归属/交叉链接）

→ AGENTS.md 当**目录**不当百科。~100 行，指向 `docs/` 的更深真相。design docs 带验证状态 + core beliefs；architecture docs 给领域/包分层地图；quality doc 给每域打分追踪 gap。

## Progressive disclosure

agent 从小而稳定入口开始，被教导下一步去哪看，而非 upfront 被淹没。机械执行：专用 linters + CI 验证知识库最新/交叉链接/结构；**recurring "doc-gardening" agent** 扫描陈旧文档开 fix-up PR。

## Enforcing architecture and taste

> "By enforcing invariants, not micromanaging implementations, we let agents ship fast without undermining the foundation."

严格分层架构（每业务域：Types → Config → Repo → Service → Runtime → UI），validated 依赖方向，custom linters + 结构测试机械执行。Cross-cutting（auth/telemetry/feature flags）走单一 Provider 接口。

"taste invariants"：静态强制结构化日志、命名规范、文件大小限制、平台可靠性。**custom lint 的 error message 注入 remediation instructions 进 agent context** —— 一旦编码，处处适用（multiplier）。

## Entropy and garbage collection

agent 复制既有模式（含次优）→ drift。曾每周五花 20% 清理"AI slop"，不可持续。改为编码 "golden principles" + 定期 background Codex 任务扫偏差、更新 quality grade、开针对性 refactor PR（多数 1 分钟内 review + automerge）。

> "Technical debt is like a high-interest loan: better to pay down continuously in small increments." 像 garbage collection。

## 结论

> "Our most difficult challenges now center on **designing environments, feedback loops, and control systems** that help agents accomplish our goal."

明确用 control systems 语言。

## 与 Harness Cybernetics / Context Engineering 的印证

| OpenAI 实践 | 框架位置 |
|---|---|
| AGENTS.md map-not-manual | Context Engineering 的 Isolate + Select |
| strict layered architecture + custom linters | Feedforward（computational） |
| taste invariants | Feedforward（computational） |
| Ralph Wiggum Loop（agent-to-agent review） | Feedback（inferential） |
| lint error 注入 remediation | Feedback（LLM-optimised sensor，Böckeler 的 positive prompt injection） |
| Chrome DevTools / LogQL / PromQL 测试 | Feedback（deterministic sensor） |
| golden principles + doc-gardening | steering loop（人编码 taste → 机械执行） |
| context rots instantly | [[Agent Reliability vs Capability]] 的 reliability decay 微观机制 |
