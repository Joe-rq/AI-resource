---
title: "Hermes Agent：Nous Research 的开源 Agent 框架"
type: summary
source_url: https://mp.weixin.qq.com/s/wX7pMuK1rizqjmJqwNbGBQ
source_type: article
date: 2026-05-02
ingested: 2026-05-22
tags: [hermes-agent, nous-research, long-term-memory, self-evolution]
---

# Hermes Agent / Nous Research

**Source**: 动脉网 · 2026-05-02

## Key takeaways

- Nous Research 是硅谷 AI 实验室，Hermes是其开源 Agent 框架，GitHub 11万+星，对标 OpenClaw
- 两大核心特性：**长期记忆**（非无状态，跨会话保持上下文）+ **自我进化**（自动封装透明可查的技能文件）
- 重点落地场景：医疗（慢病管理、医生培训、科研辅助）
- 核心挑战：自我进化特性在现行医疗器械监管框架下难以合规

## Core claims

Hermes 区别于传统 AI 无状态架构，具备跨会话长期记忆能力。自我进化机制能自动将操作封装为技能文件，且透明可查。GitHub 社区热度 11万星说明开发者认可度极高。医疗场景是重点方向，但 FDA/NMPA 对自我进化系统的监管仍是待解决问题。

## Concepts introduced / referenced

- [[Agent Runtime]] — 长期记忆是当前 Runtime 的关键能力缺口
- Memory Agent — Hermes 的长期记忆方向与 wiki 中 Memory Agents 分类相关
