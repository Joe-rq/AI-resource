---
title: "如何实现一个好的 AI 自主干活系统"
type: summary
created: 2026-06-04
updated: 2026-06-15
sources: ["raw/articles/2026-06-02-ai-autonomous-system-tips.md"]
tags: [autonomous-ai-system, agent-runtime, harness, watchdog, worktree, self-review, state-persistence, yang-zhiping]
---

# 如何实现一个好的 AI 自主干活系统

> 原始作者：阳志平  
> 原始来源：微信公众号（2026-06-02）  
> 本 wiki 摄取日期：2026-06-04

## 摘要

业界习惯用「harness」一词，阳志平更愿意称之为 **AI 自主系统（Autonomous AI System）**。核心判断标准：

> 「衡量当前 AI 发展到了什么水准，就看一件事：在没有任何人类介入的前提下，它能独立工作多久、能不能交付高质量的成果。」

作者将「让 AI 在你跑步、睡觉时持续干活」的全套技巧拆为四组 12 个，从任务编排到自动续航。**完整的 12 技巧表、四设计原则、harness 视角对比、实践飞轮与交叉引用，见 [[Autonomous AI System]]。**

## 原文独有的洞见

以下内容来自原文叙事，概念页未收录：

### worktree 的历史渊源

worktree 早在 2015 年由 pclouds 主导开发，但一直不是 git 常用命令。如今得益于 AI 进步，成为 AI 自主系统标配。**关键约束不是技术实现，而是工作记忆与认知负荷**——人类大脑极不擅长多线程切换。

### 跨模型评审的隐藏陷阱

> 让两个 AI 一起评审，最大的危险是**它们会互相说服**——干活的那个解读评审结论时，会下意识往「通过」的方向偏。

作者永远不让干活的模型自己解读评审结果，而是另起一个干净上下文、不同谱系、不同训练数据的旗舰模型。例：`codex exec -m gpt-5.5 -c model_reasoning_effort=medium`（在 Claude Code 中直接调用 Codex）。

### 意外处理矩阵（原文实例）

作者将「为 AI 预设执行意图」类比人类心理学中的执行意图（implementation intention）：

| 如果 | 那么 |
|------|------|
| codex 评审超时（> 5 min） | kill 进程 + 记录 + PR 留着不合 + 跳下一个 |
| codex 持续 REQUEST_CHANGES（≥ 2 次） | PR 留着不合 + 评论附输出 + 跳下一个 |
| 测试 fail 修不动 | PR 不开 + 分支保留 + issue 标 BLOCKED + 跳下一个 |
| 调用 /simplify 后测试 fail | 撤改动重新做；仍 fail 标 BLOCKED |
| 任何 unrecoverable | 记 `.claude/notes/autonomous-state.md` + 跳下一个 |

**核心原则：永不停摆。** 单条卡住就跳下一条，绝不阻塞整体推进。

## 核心判断

> 真正的答案也许不在那些确定的、高效的、可被自动化的回答里，而在人类面对 AI 这类快速生长的技术巨物时的恐惧之中，在它所带来的颠覆面前的踌躇之间，在一时不知如何自处的茫然之际。**当 AI 把确定的事越做越快、把不确定留给人类，恰恰是这份恐惧、踌躇与茫然，见证着人类之所以为人类。**

「AI 自主干活系统」的提出，是对「人 vs AI 双节奏协同」这一本源问题的正面回应——哪些事要人亲自做？哪些事可以交给 AI 持续推进？**如何让越来越强的 AI 增强人类，而不是削弱人类的自主感与意义感**。

## 阅读指引

- **技术深度与交叉引用** → [[Autonomous AI System]]（12 技巧、四原则、harness 对比、飞轮、关联概念矩阵）
- **同源文章** → [让 AI 变得更聪明的 12 个元反思技巧](https://mp.weixin.qq.com/s?__biz=MzA3MzM0MjUyMQ==&mid=2652154952&idx=1&sn=a1d6c7cc99eae8d5b18be4fcab5e100c&scene=21#wechat_redirect)（技巧 7 看门狗、技巧 8 完整性、技巧 12 积累飞轮直接对应）
