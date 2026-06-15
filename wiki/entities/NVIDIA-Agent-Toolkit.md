---
title: "NVIDIA Agent Toolkit"
type: entity
created: 2026-05-19
updated: 2026-05-19
sources: [raw/articles/nvidia-agent-toolkit.md]
tags: [nvidia, agent-platform, toolkit, security]
---

# NVIDIA Agent Toolkit

NVIDIA 的 Agent 开发与部署工具包，以自身 GPU/CUDA 生态为基础构建完整的 Agent 平台。

## 核心组件

- **NemoClaw** — Agent Core，处理多模态输入并编排子 Agent 和技能调用
- **OpenShell** — 安全运行时，三层安全检查（Policy Engine → Network Guardrail → Privacy Router）
- **LLM 引擎** — Nemotron / NeMo / Dynamo / NIM，覆盖本地高性能模型与云端大模型
- **Sub Agents** — AI-Q Research Agent，支持多 Agent 协作编排
- **Skills** — cuOpt 优化引擎等可调用能力模块
- **Tools** — 通过 CLI 和 MCP（Model Context Protocol）协议连接外部资源

## 关键特性

- **Computer Use** — Agent 可直接操控计算机，非仅对话
- **多模型支持** — 本地 Nemotron + 云端 Anthropic/Google/OpenAI/xAI
- **工业集成** — Isaac Sim（机器人仿真）、Omniverse（数字孪生）、CAD
- **安全优先** — Sandbox Guardrail 隔离不可信 Skills，三层网络/隐私护栏

## Related concepts

- [[concepts/Agent-Runtime]] — OpenShell 是 Agent Runtime 的安全运行时实现
- [[concepts/Agent-Secure-Runtime]] — Agent 安全运行时的设计模式
- [[concepts/Multi-Agent-协作模式]] — Sub Agents 体现 Orchestrator/Specialist 模式

## Sources

- [[summaries/raw/articles/nvidia-agent-toolkit.md]] — (2026-05-19) 架构图分析
