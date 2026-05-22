---
title: "Hermes Agent 之后：AI 开发需要一层治理协议"
type: summary
created: 2026-05-22
updated: 2026-05-22
sources: ["hermes-agent-harness-engineering"]
tags: [harness, governance, wow-harness, event-sourcing, multi-agent]
---

# 摘要

## 核心论点

现有 AI 开发工具（Claude Code、Superpowers、Hermes Agent、OpenHands）都在优化"一个人 + 一个 agent"的单次体验，缺少**跨 session、跨 agent 的长期一致性治理**。wow-harness v3 是面向这个问题的治理协议设计。

## 五个问题及 v3 解决方案

| 问题 | v3 方案 |
|------|---------|
| AI 做过的事怎么不丢 | 事件时间线（只追加、不可篡改）+ 增量状态推导 + 定期快照压缩 |
| 工程概念跨 session 怎么不漂移 | 概念节点生命周期状态机 + 新颖性检查 |
| 怎么确保 AI 产出真的做完了 | 双层验证：自检 + 物理拦截 + 独立验证 agent |
| 怎么让 AI 成为自运转组织 | 自动扩张任务图 + 事件触发 agent spawn + 上下文胶囊 |
| 项目负责人怎么不退化判断权 | 工程决策 AI 自做，语义判断升级到人 |

## 与现有工具的根本区别

- **Claude Code** = v3 的地基（单次 session 高效执行），v3 加跨 session 组织级治理
- **Superpowers** = 把 agent 当需要管教的执行者（prompt 层行为约束），v3 让 agent 从系统理解推导行为
- **Hermes Agent** = 一个人的助手（单用户单 agent），v3 假设多 agent 并行
- **OpenHands** = EventStream 是 session 内临时消息总线，v3 事件时间线是永久的

## 学术验证

### "Dive into Claude Code" 论文

"Dive into Claude Code"论文（[[entities/Dive-into-Claude-Code]]，arxiv 2604.14228）通过源码级逆向工程分析 Claude Code，识别出 5 个设计价值、13 条设计原则、7 组件高层结构、5 层子系统架构。

核心数据与 v3 高度重合：
- **98.4% 运行基础设施，1.6% AI 决策逻辑** -- 套具比模型重要
- **append-only durable state** -- Claude Code 使用 mostly append-only JSONL transcripts
- **minimal scaffolding, maximal operational harness** -- 不约束模型决策，创造让模型做好决策的条件
- **isolated subagent boundaries** -- subagent 隔离上下文窗口 + summary-only 返回

### ESAA 论文

ESAA 论文（[[entities/ESAA]]，arxiv 2602.23193）将 Event Sourcing + CQRS 原则应用于 LLM agent 生命周期管理，从学术角度验证了 v3 事件时间线的核心理念：

- **Immutable audit trail** -- 与 v3 "只追加、不可篡改" 一致，ESAA 的 event store 通过 append-only log 记录所有 agent 行为
- **Deterministic replay** -- v3 增量状态推导 + 快照压缩的学术对应，ESAA 用 SHA-256 hash 验证投影一致性
- **Boundary contracts** -- ESAA 禁止 agent 直接写文件，只能 emit intentions 由 orchestrator 验证后执行，与 v3 的 schema 级权限限制和物理拦截提交检查点同构
- **Purified view** -- ESAA 的 purified view 与 v3 上下文胶囊共享同一目标（缓解 lost-in-the-middle）

ESAA 在两个 case study 中验证：单 agent landing page（49 events）和四 agent 并发 clinical dashboard（86 events），两个 case 均零 `output.rejected`。

v3 在 ESAA 之外额外覆盖：概念节点生命周期状态机、新颖性检查、约束规则独立生命周期、三正交审查方法论、闭合合约驱动的缺陷修复协议。

## 核心判断

> 协议比能力重要，治理比智能重要，长期连贯性比单次质量重要。
