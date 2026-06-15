---
title: "MiniMax Mavis 技术报告"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["raw/articles/2026-05-19-minimax-agent-team-tech-report.md"]
tags: [minimax, mavis, agent-team, single-agent-defects]
---

# 摘要

## 核心观点

> "多 Agent 系统是 runtime，不是 prompt 编排"

让多个 AI 一起干活，关键不是给它们写更好的指令，而是给它们搭一个能长期运行、能管理状态的底座。

## 单 Agent 四个痛点

| 痛点 | 表现 |
|------|------|
| **会在意想不到时停下** | 做完3件事就停，等用户确认"要不要继续" |
| **长任务越跑越笨** | 从"聪明助手"变成"容易分心的人"，风格漂移 |
| **无法秒回** | IM 场景用户耐心短，等分钟级回复体验差 |
| **角色分工虚假** | 同一 Agent 轮班，角色扮演≠角色分工 |

## Agent Team 架构

- **Owner** 拆任务
- **Worker** 干活
- **Verifier** 挑刺
- **Team Engine** 确定性状态机调度（不是 AI 决策）

## Team Engine 特点

- 两个 AI 之间不直接通讯，靠程序中转
- 任务分批并行执行，下一批看上一批是否通过验证
- 有重试上限，陷入死循环自动升级决策

## 关键设计

> "很多框架里的验证环节是可选的附加步骤，在我们这里它是架构的核心。"

验证不是事后的质量检查，而是嵌入在生产状态机里的核心机制。

参见 [[entities/MiniMax-Mavis|MiniMax Mavis]] 产品。