---
title: "Harness Engineering 14 步路线图：从单个 agent 到自我改进系统"
type: summary
created: 2026-06-18
updated: 2026-06-18
sources: ["raw/articles/2026-06-16-harness-engineering-14-steps.md"]
tags: [harness, claude-code, loop-engineering, subagent, skill, hook, memory, 0xmovez, compensation-surface]
---

# Harness Engineering 14 步路线图：从单个 agent 到自我改进系统

> 原始作者：0xMovez AI（Substack，2026-06-16）
> 本 wiki 摄取日期：2026-06-18

## 薄摄取说明：与综述的关系

> 本文是 [[Harness Engineering 综述：14 篇工程文章里的 15 个月]] 的**入门操作手册视角**，核心观点（三层结构、context/enforcement/procedure/isolation 四分、补偿面）在综述与 [[Loop Engineering：从 Prompt 到系统设计]]、[[Thin Harness, Fat Skills]] 中已有覆盖。本文的增量是 **14 步可执行 roadmap + `.claude/` 文件夹布局 + 三层（harness/loop/system）的清晰切分**。

## 三层切分（本文最清晰的贡献）

| 层 | 定义 | 静态/动态 |
|----|------|-----------|
| **Harness** | 单个 agent 运行的环境：model + tools + permissions + context | 静态配置 |
| **Loop** | 在 harness 之上按定时 prompt agent、spawn helper、自喂 | 动态，定时 |
| **Self-improving system** | loop + memory，每次运行让下次更锋利 | 复利 |

> 关键句：**"loop didn't add intelligence. It re-used everything in the harness."** 一个好 harness 让 loop 变得 trivial——这正是先建地基再上 loop 的全部意义。

## 14 步 roadmap（3 个 Part）

- **Part 1 · What harness is（1-4）**：① harness 四要素（model/tools/permissions/context）② 全部住在 `.claude/` 一个文件夹 ③ harness vs loop vs system 三层别混 ④ 默认 harness 长什么样
- **Part 2 · Configure（5-9）**：⑤ CLAUDE.md 放 standing facts（<500 tokens，事实不是流程）⑥ settings.json 放 permissions/model（按"undo 成本"决定 auto-approve）⑦ Subagents 放隔离上下文 + writer/checker 分离 ⑧ Skills 放可复用流程 ⑨ Hooks 放确定性强制（模型骗不过 exit 2）
- **Part 3 · Make it compound（10-14）**：⑩ 加 loop（`/loop` + `/goal`，独立 grader 判 done）⑪ 加 dynamic workflows（harness 写自己的 orchestration）⑫ 加 memory（write before walking away / read at start / distill into skills）⑬ close the loop（output→lesson→skill→better output）⑭ ship the harness（打包 plugin 共享）

## 实操原则与反模式

- **四分原则**：standing facts → CLAUDE.md；enforcement → hooks；procedures → skills；isolation → subagents。**混淆它们**（把 enforcement 塞进 CLAUDE.md、把流程塞进上下文）= 不一致又昂贵的 agent 的根因。
- **"keep the harness small enough that you can explain why every file exists"**——解释不出某 rule/hook/subagent 干嘛的，就删。
- **8 个 harness 反模式**：跑默认 harness / 臃肿 CLAUDE.md / enforcement 写在 CLAUDE.md / 自己写自己评 / 无 memory / 在烂 harness 上套 loop（=更快产 slop）/ 二十个 hook（一两个锋利的胜过一堆没人懂的）/ 不扫描就 ship（泄露 secret + 过宽权限扩散给所有安装者）。

## 与现有概念

- 三层结构、补偿面迁移 → [[Harness Engineering 综述：14 篇工程文章里的 15 个月]]（上游演化视角）
- loop 复用 harness → [[Loop Engineering：从 Prompt 到系统设计]]
- enforcement→hooks、procedure→skills、writer/checker→subagent → [[Thin Harness, Fat Skills]]、[[Claude Code Skills]]、[[Claude Code Subagent]]
- close the loop（output→lesson→skill）→ [[Skills 自我提升闭环：inner loop 用、outer loop 改]] 的 inner/outer loop 是其工程化
