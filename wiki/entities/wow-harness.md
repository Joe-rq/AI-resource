---
title: "wow-harness"
type: entity
created: 2026-05-22
updated: 2026-05-22
sources: ["raw/articles/2026-05-20-hermes-agent-harness"]
tags: [harness, governance, agent-organization, wow-harness]
---

# wow-harness

## 基本信息

| 属性 | 值 |
|------|-----|
| 作者 | 张晨曦（Nature），通向惊喜科技创始人 |
| 版本 | v3（共 21 个模块，设计文档约 50,000 行，六轮版本迭代） |
| 定位 | 端点 Runtime 位置的治理协议 |
| 体系 | 通爻协议（ToWow Protocol）中面向单组织内部 AI 协作治理的一层 |

## 核心命题

现有 AI 开发工具都在优化"一个人 + 一个 agent"的单次体验，但缺少**跨 session、跨 agent 的长期一致性治理**。wow-harness v3 是面向这个问题的治理协议设计。

> 协议比能力重要，治理比智能重要，长期连贯性比单次质量重要。

## 与现有工具的关系

| 工具 | 关系 |
|------|------|
| [[entities/Dive-into-Claude-Code|Claude Code]] | **地基**，v3 跑在 Claude Code 上面，不竞争 |
| Superpowers | **同层分歧** -- 把 agent 当需要管教的执行者，v3 让 agent 从系统理解推导行为 |
| Hermes Agent | **同层分歧** -- 一个人的助手，v3 假设多 agent 并行 |
| OpenHands | **同层分歧** -- EventStream 是 session 内临时消息总线，v3 事件时间线是永久的 |

## v3 五个核心解决方案

1. **事件时间线** -- 只追加、不可篡改，增量状态推导 + 定期快照压缩
2. **概念节点生命周期** -- 创建 → 修改 → 被替换 → 退役，新颖性检查防止振荡
3. **双层验证** -- agent 自检 + 物理拦截提交检查点 + 独立验证 agent（schema 级无写权限）
4. **自动扩张任务图** -- 事件触发驱动 agent spawn，无状态 session + 上下文胶囊
5. **人机决策分层** -- 工程决策 AI 自做，语义判断升级到人，用产品语言描述

详见 [[concepts/Agent-Harness-治理协议]]。

## 学术验证

### "Dive into Claude Code" 论文

**"Dive into Claude Code"论文**（[[entities/Dive-into-Claude-Code]]，arxiv 2604.14228）通过源码级逆向工程分析，验证了 Claude Code 98.4% 是运行基础设施、1.6% 是 AI 决策逻辑。论文提出的 5 个设计价值和 13 条设计原则（append-only durable state、minimal scaffolding maximal operational harness、isolated subagent boundaries 等）与 v3 治理协议的设计理念高度契合。

### ESAA 论文

**ESAA 论文**（[[entities/ESAA]]，arxiv 2602.23193）将 Event Sourcing + CQRS 原则应用于 LLM agent 生命周期管理，从学术角度验证了 v3 事件时间线的核心理念：

- **Immutable audit trail** -- 与 v3 事件时间线的"只追加、不可篡改"设计一致
- **Deterministic replay** -- v3 增量状态推导 + 定期快照压缩的学术对应
- **Boundary contracts** -- v3 双层验证的 schema 级权限限制与 ESAA 的 boundary contract 机制同构
- **Purified view** -- v3 上下文胶囊与 ESAA 的 purified view 共享同一目标（缓解 lost-in-the-middle）

ESAA 与 v3 的关键差异：ESAA 从软件工程学术角度提出架构模式并通过 case study 验证，v3 从工程实践角度提供完整的组织级治理方案（含概念节点生命周期、新颖性检查、人机决策分层等超出 ESAA 范围的机制）。
