---
title: "08 - Agent Runtime 主战场"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["08-agent-runtime-battlefield-20260516"]
tags: [agent-runtime, benchmark, harness, cline]
---

# 摘要

## 核心论点

**Agent Runtime 正在成为 AI 行业的下一个主战场**。同样的模型在不同 runtime 上可差出 **4.8-10 个百分点**，这个量级相当于一次模型版本迭代。

## 关键数据

| 发现 | 数据 |
|------|------|
| Cline vs Claude Code (同一模型) | 74.2% vs 69.4%，差 4.8pp |
| Cline hill climbing | opus-4.5 从 47% → 57%，+10pp 全部来自 runtime |
| LangChain harness profile | 同一模型有无 harness 差 10-20pp |

## Runtime 四个设计决策

1. **Prompt 设计** — system prompt 定义模型角色、工具使用、任务完成判断
2. **工具定义** — 参数描述、返回值格式直接影响调用正确率
3. **上下文管理** — 何时 compact、按什么顺序删除、保留什么
4. **错误处理** — 错误消息质量决定模型能否自我修正

## 核心概念

- **Harness** = Agent 执行环境，包含 prompt/工具定义/上下文管理/错误处理
- **Hill climbing** = 每次改一个变量，跑完整 benchmark，用分数判断效果
- **25/75 法则** = 25% 失败是模型天花板，75% 可在 runtime 层修复

## 行业信号

- DeepSeek 热招 Agent Harness PM
- OpenAI 成立 Deployment Co.，40亿美元做全栈 Agent
- Anthropic Claude Cowork + Partner Network
- AWS 把 Runtime、Memory、Identity、Browser 列为 AgentCore 企业级模块
- Cline 开源内部 Runtime SDK（Apache 2.0）

## 结论

行业重心正从"写 prompt"转向"维护控制面"。Agent runtime 不是可选的工程层，而是决定模型在 Agent 场景下能不能跑起来的关键层。