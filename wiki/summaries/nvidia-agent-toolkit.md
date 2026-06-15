---
title: "NVIDIA Agent Toolkit 架构"
type: summary
created: 2026-05-19
updated: 2026-05-19
sources: ["raw/articles/nvidia-agent-toolkit.md"]
tags: [nvidia, agent-runtime, security, multi-agent, toolkit]
---

# NVIDIA Agent Toolkit 架构

**Source**: 微信分享的架构图 · 2026-05-19

## Key takeaways

- NVIDIA 用自身技术栈（Nemotron、NeMo、cuOpt、Isaac Sim）构建了完整的 Agent 平台，覆盖 Runtime / Multi-Agent / Skills / Tools / Security 全栈
- **OpenShell** 是其安全运行时核心，三层安全检查（Policy → Network → Privacy）确保 Agent 在安全边界内自主运行
- **MCP（Model Context Protocol）** 作为 Agent 与外部资源的统一连接协议，与 Claude Code 生态一致

## Core claims

NVIDIA Agent Toolkit 展示了一个工业级 Agent 平台的完整形态：从底层 GPU 加速（cuDF/cuVS/vGPU）到上层多 Agent 编排（AI-Q Research Agent），中间通过 OpenShell 安全运行时隔离。其设计重点是让 Agent 能**自主执行**（Computer Use、Tools）而非仅对话，同时通过沙箱和护栏保证安全性。

## Concepts introduced / referenced

- [[NVIDIA Agent Toolkit]] — NVIDIA 的 Agent 开发工具包
- [[Agent Secure Runtime]] — Agent 安全运行时设计模式
- [[Agent Runtime]] — 已有概念，本文提供了 NVIDIA 的实现案例
- [[Multi-Agent 协作模式]] — Sub Agents 体现了 Orchestrator/Specialist 模式
