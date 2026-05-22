---
title: "ESAA: Event Sourcing for Autonomous Agents"
type: summary
created: 2026-05-22
updated: 2026-05-22
sources: ["raw/papers/ESAA-Event-Sourcing-for-Autonomous-Agents"]
tags: [event-sourcing, CQRS, agent-governance, audit-trail, paper]
---

# 摘要

## 论文信息

"ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering"（arxiv 2602.23193）。

将 Event Sourcing + CQRS 原则应用于 LLM agent 生命周期管理，通过 immutable audit trail 和 deterministic replay 解决 state drift、long-horizon consistency、blast radius 问题。

## Core Thesis

Agent 的 source of truth 不是当前仓库快照，而是一条不可变的意图、决策、效果日志。当前状态从这条日志确定性投影。LLM 作为 "intention emitters under contract"，而非拥有无限制写权限的 "developer"。

## Architecture

四个 canonical artifacts:
1. **Event store** (`activity.jsonl`) -- append-only，含 intentions/dispatches/effects/closures
2. **Materialized view** (`roadmap.json`) -- 纯投影 read-model + SHA-256 hash
3. **Boundary contracts** -- 按 task type 定义允许/禁止的 actions
4. **PARCER profiles** -- 6 维 metaprompting，强制 JSON envelope

关键设计：
- Agent 无直接文件写权限，只能 emit structured intentions
- Trace-first: 事件先于不可逆效果记录
- Immutability of done: 完成任务不可回退，缺陷开新 hotfix 路径
- Purified view: orchestrator 选择性注入当前步骤所需信息

## Case Studies

| 指标 | CS1: Landing Page | CS2: Clinic ASR |
|------|-------------------|-----------------|
| Tasks | 9 | 50 (15 phases) |
| Events | 49 | 86 |
| Agents | 3 (composition) | 4 (concurrent) |
| Duration | Single session | ~15 hours |
| `output.rejected` | 0 | 0 |
| `verify_status` | ok | ok (partial 31/50) |

CS2 关键观察：同一分钟内 6 个并发 claim，证明 append-only event store 天然序列化并发。Event vocabulary 从 CS1 的 15 种简化到 CS2 的 5 种（`promote`/`claim`/`complete`/`phase.complete`/`roadmap.version`）。

## Multi-Agent Coordination

Event store 作为天然协调机制，三个涌现属性：
1. **Serialized accountability** -- 尽管并发执行，append-only log 保留全序
2. **Specialization tracking** -- 日志可 forensic 恢复 agent 专业化模式
3. **Phase-gated progression** -- `promote -> claim -> complete -> phase.complete` 序列强制依赖排序，agent 间无需感知彼此

## Results

- 结构合规：两个 case study 均零 `output.rejected`
- 审计能力：time-travel debugging via replay + SHA-256 hash verification
- 上下文效率：purified view 机制缓解 lost-in-the-middle
- 安全性：boundary contracts 限制 blast radius，最小权限原则
- 开销可控：token/latency/storage 开销相对 LLM inference 可忽略

## Threats to Validity

- Internal: n=2 case studies，temperature 0.0 可能不代表 sampling diversity
- External: landing page + clinical POC 不一定泛化到 CI/CD、monorepo
- Construct: `output.rejected`/`verify_status` 不直接衡量设计质量或业务价值

## 与本 Wiki 的关联

- [[entities/ESAA]] -- 论文实体页
- [[concepts/Agent-Harness-治理协议]] -- 治理协议与 ESAA 架构高度对应
- [[entities/wow-harness]] -- v3 事件时间线是 ESAA 理念的工程实践
- [[entities/Dive-into-Claude-Code]] -- Claude Code append-only JSONL 与 ESAA 共享设计哲学
