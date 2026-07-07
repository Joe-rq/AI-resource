---
title: "Getting started with loops（Claude Code 官方 loop 分类法）"
type: summary
created: 2026-07-07
updated: 2026-07-07
sources: ["raw/articles/2026-07-07-claude-devs-getting-started-with-loops.md"]
tags: [claude-code, loops, agentic-loop, goal, schedule, dynamic-workflows, auto-mode, token-usage, delba-oliveira]
---

# Getting started with loops（Claude Code 官方 loop 分类法）

> 原始作者：@delba_oliveira（published via @ClaudeDevs）
> 原始来源：[X article](https://x.com/ClaudeDevs/article/2074208949205881033)（2026-07-07）
> 互动：203 replies · 1.4K reposts · 10K likes · 23.6K bookmarks · 2.4M views
> 本 wiki 摄取日期：2026-07-07

## 摘要

Claude Code 团队官方给出 loop 的定义与分类：**loops = agents repeating cycles of work until a stop condition is met**，按 trigger / stop / primitive / task 四维度分为 **Turn-based / Goal-based / Time-based / Proactive** 四类。文章逐类给出何时用、用什么原语、如何管理用量，并补充两个横切主题——维护代码质量与管理 token 用量。

> 核心立场：**不是所有任务都需要复杂 loop，从最简单的方案开始，选择性使用这些 pattern。**

类型学抽取为可复用概念页 [[Claude Code Loops]]；本页保留原文细节与示例。

## 四类 Loop 详解

### Turn-based loops — 你交出"检查"

- **触发**：用户 prompt
- **停止**：Claude 判断完成或需更多上下文
- **适合**：短的、非规律性任务
- **管理用量**：写明确 prompt + 用 skills 强化验证减少 turn 数

每个 prompt 启动一个手动 loop，用户主导每轮。Claude 收集上下文 → 行动 → 自检 → 必要时重复 → 回复。例如让 Claude 做一个 like 按钮：读代码 → 编辑 → 跑测试 → 交回它*认为*能用的结果，你手动检查后写下一个 prompt。

验证步骤可编码为 SKILL.md，让 Claude 端到端自检更多工作。skill 应包含让 Claude *看*、*量*、*交互*结果的工具/连接器；检查越量化越易自检。文章给的示例 skill：

```markdown
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---
# Verifying frontend changes
Never report a UI change as complete based on a successful edit alone. Verify it the way a human reviewer would:
1. Start the dev server and open the edited page in the browser.
2. Interact with the change directly. For a new control (button, input, toggle): click it, confirm the expected state change, and screenshot before/after.
3. Check the browser console: zero new errors or warnings.
4. Use the Chrome Devtools MCP, run a performance trace and audit Core Web Vitals.
If any step fails, fix the issue and rerun from step 1 — do not hand back partially verified work.
```

### Goal-based loop (/goal) — 你交出"停止条件"

- **触发**：实时手动 prompt
- **停止**：goal 达成 或 最大 turn 数
- **适合**：有可验证 exit criteria 的任务
- **管理用量**：设明确 completion criteria + 显式 turn cap

单轮不够时，用 `/goal` 定义"done 长什么样"。Claude 每次试图停止时，**evaluator model** 检查条件，未达成打回继续，直到 goal 达成或达到你定义的 turn 数。确定性 criteria（测试通过数、分数阈值）最有效——Claude 不必自行判断"够好了"而过早结束。

```bash
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

### Time-based loop (/loop, /schedule) — 你交出"触发"

- **触发**：时间间隔
- **停止**：取消或工作完成（PR merge、queue 空）
- **适合**：周期性工作、与外部系统交互
- **管理用量**：设较长间隔或基于事件而非时间

两类 agentic 工作适合时间触发：任务不变只换输入（如每天摘要 Slack），以及依赖外部系统（如 PR 可能收到 review 或 CI 失败）。`/loop` 按间隔重跑 prompt，跑在本机、关机即停；`/schedule` 把 routine 移到云端。

```bash
/loop 5m check my PR, address review comments, and fix failing CI
```

### Proactive loops — 你交出"prompt"

- **触发**：事件或 schedule，无实时人工
- **停止**：每任务 goal 达成即退出；routine 本身运行到关闭
- **适合**：周期性 well-defined 工作流（bug report、issue triage、migration、dependency upgrade）
- **管理用量**：routine 路由到小快模型，判断调用最强模型

把上述原语与 **auto mode**、**dynamic workflows**（research preview）组合成长时间运行 loop。处理 incoming feedback 的四件套：

1. `/schedule`（research preview）跑 routine 检查新报告
2. `/goal` 定义 done + skills 文档化验证方式
3. dynamic workflows 编排 triage → fix → review
4. auto mode 让 routine 无需逐次确认

```bash
/schedule every hour: check the project-feedback channel for bug reports. /goal: don't stop until every report found this run is triaged, actioned, and responded to. When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
```

## 横切主题

### Maintaining code quality

loop 输出质量取决于它周围的系统：

- **保持 codebase 干净** — Claude 跟随已有 pattern 与 convention
- **给 Claude 自检手段** — 用 [skills](https://code.claude.com/docs/en/skills) 编码"good 长什么样"
- **让 docs 触手可及** — 框架/库 docs 有最新最佳实践
- **第二个 agent 做 code review** — fresh context 的 reviewer 偏见更少，不受主 agent 推理影响。用内置 `/code-review` skill 或 GitHub 的 [Code Review](https://code.claude.com/docs/en/code-review)

> 单个结果不达标时，不止修单个 issue，尝试编码进系统改善未来所有迭代。

### Managing token usage

loop 需有清晰边界：

- **选对 primitive 与 model** — 小任务不必多 agent/loop，可用更便宜更快的模型
- **定义清晰 success 与 stop criteria** — 具体说 done 长什么样，让 Claude 更快到达（但别太快）
- **大规模跑前先 pilot** — dynamic workflows 可 spawn 数百 agent，先在小切片上估用量
- **确定性工作用 script** — 跑脚本比推理便宜（如 PDF skill 附 form-filling script）
- **间隔匹配变化频率** — 别比所观察事物变化更频繁地跑 routine
- **review usage** — `/usage` 按 skill/subagent/MCP 拆分；`/goal` 无参显示 turn 与 token；`/workflows` 显示每 agent token，可随时停

## Getting started 对照表

| Loop | You hand off | Use it when | Reach for |
|------|-------------|-------------|-----------|
| Turn-based | The check | 你在探索或决策 | Custom verification skills |
| Goal-based | The stop condition | 你知道 done 长什么样 | /goal |
| Time-based | The trigger | 工作发生在项目外、按 schedule | /loop, /schedule |
| Proactive | The prompt | 工作周期性且 well-defined | 以上全部 + dynamic workflows |

> 起步：看手头工作，挑一个你是瓶颈的任务，问能交出哪一块——能写验证 check 吗？goal 够清楚吗？工作按 schedule 到达吗？有想法后跑 loop，观察它哪里 stall 或 over-reach，别怕迭代。

## 关键洞察

1. **"hand off"四层递进** — Turn-based → Goal-based → Time-based → Proactive，人依次交出 check / stop condition / trigger / prompt。每交出一层都需更强验证与治理，否则就是 Agentic Laziness 与 Goal Drift 的温床。

2. **/goal 的 evaluator 是 maker/checker 分离** — 写代码的 agent 不给自己打分，另一个小模型判完成。这是 [[Worker Verifier 对抗循环]] 应用到停止条件本身，直接对治 [[Agentic Laziness]]（提前终止）与 Self-Preferential Bias（偏向自己产出）。

3. **Proactive loop 是组合，不是新原语** — 它没有新 primitive，而是 `/schedule` + `/goal` + skills + dynamic workflows + auto mode 的编排。与 [[Claude Code Dynamic Workflows 实践指南]] 的"结合 /goal 和 /loop"进阶技巧同源，但文章给出了完整组合范式。

4. **verification skill 是 loop 质量的支点** — Turn-based 靠它减少 turn，Goal-based 靠它定义 done，Proactive 靠它文档化验证方式。与 [[Thin Harness, Fat Skills]] 的"skill-as-method-call"一致——确定性验证外移到 skill，Claude 只做判断。

5. **从最简单方案开始** — 文章反复强调"不是所有任务都需要复杂 loop"。与 [[Loop Engineering：从 Prompt 到系统设计]] 的"直接 prompt 仍有效"呼应：loop 补充而非替代直接 prompt。

## 与现有 Wiki 概念的关联

| 本文概念 | Wiki 对应 |
|---------|----------|
| Loop 四分类法 | [[Claude Code Loops]] — 抽取为可复用概念页 |
| /goal evaluator model | [[Worker Verifier 对抗循环]] — maker/checker 分离应用到停止条件 |
| Verification skills | [[Claude Code Skills]] / [[Thin Harness, Fat Skills]] — skill-as-method-call，确定性验证外移 |
| Second agent code review | [[Agentic Code Review]] — fresh context reviewer 减少主 agent 偏见 |
| Proactive loop = 阳志平"自动续航" | [[Autonomous AI System]] — 12 技巧 × 4 组的任务编排/自检/续航 |
| Time-based / Proactive 长期运行守护 | [[Heartbeat Watchdog]] — 独立守护层对治运行时脆弱与停滞 |
| loop 失效模式 | [[Agentic Laziness]] / [[Goal Drift]] / [[Self-Preferential Bias]] — Dynamic Workflows 三失效模式 |
| 通用 loop 模块视角 | [[Loop Engineering：从 Prompt 到系统设计]] — Addy Osmani 5 模块 + 1 记忆 |
| dynamic workflows 原语 | [[Claude Code Dynamic Workflows 实践指南]] / [[Claude Code 动态工作流（Dynamic Workflows）]] |
| loop 可回滚 | [[Stateless Reducer]] — ingest checkpoint 即 reducer 式 snapshot/rollback |
