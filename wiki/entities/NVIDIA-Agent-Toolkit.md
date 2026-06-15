---
title: "NVIDIA Agent Toolkit"
type: entity
created: 2026-05-19
updated: 2026-06-15
sources: [raw/notes/nvidia-agent-toolkit.md, raw/articles/nvidia-agent-toolkit.md]
tags: [nvidia, agent-platform, toolkit, security, gpu-accelerated]
---

# NVIDIA Agent Toolkit

NVIDIA 的 Agent 开发与部署工具包，以自身 GPU/CUDA 生态为基础构建完整的 Agent 平台。采用 hub-and-spoke 架构，以 NemoClaw（Agent Core）为中心辐射连接输入、数据、模型、工具、安全各层。底层的 GPU 加速基础设施（cuDF、cuVS、vGPU）为 Agent 的全链路提供硬件级加速。

## 核心组件

### NemoClaw — Agent Core

NemoClaw 是 Agent 的核心编排引擎，作为中央调度器处理多模态输入（文本、图像、结构化/非结构化文件）并协调子 Agent 与技能调用。其内部采用四层容器模型：

- **Definition** — Agent 的身份定义、系统提示、行为约束
- **Memory** — 上下文持久化，支持 Mem0 等外部记忆后端，实现跨会话状态保持
- **Skills** — 可调用能力模块（如 cuOpt 优化引擎、代码生成、数据分析），支持通过 ClawHub 加载不可信第三方 Skills 并经由 Sandbox Guardrail 隔离执行
- **Terminal** — 命令行执行环境，Agent 通过终端与宿主系统交互

NemoClaw 支持多种 Agent 工作流模式：ReAct Agent（推理-行动循环）、Tool-Calling Agent（原生函数调用）、Reasoning Agent（测试时计算增强）、Auto-Memory Agent（自动记忆管理）。子 Agent 通过 Mixture-of-Agents（MoA）模式进行层次化编排：Orchestrator LLM 接收任务后根据能力匹配将子任务路由给专用的 Executor Agent（如数学 Agent、互联网搜索 Agent、数据分析 Agent），各子 Agent 拥有独立的工具集和 LLM 配置。

### OpenShell — 安全运行时

OpenShell 是 Agent 的安全执行环境，在命令执行全链路上设置三层顺序检查点：

1. **Policy Engine**（策略引擎）— 命令入口的第一道关卡。基于预定义规则控制 Agent 的执行权限，包括：可执行命令白名单/黑名单、文件系统访问范围限制（读/写/删除权限按路径粒度的 RBAC）、进程创建与网络绑定的权限控制。Policy Engine 在命令进入操作系统之前完成拦截，防止 Agent 越权执行。

2. **Network Guardrail**（网络护栏）— 控制 Agent 对外部网络资源的访问。检查点包括：出站连接的 IP/域名白名单、API 调用速率限制与节流（rate limiting）、禁止访问内网敏感网段（防止 SSRF 类攻击）、对外部数据源的访问审计日志。Network Guardrail 确保 Agent 即使突破 Policy Engine，也无法在网络上横向移动。

3. **Privacy Router**（隐私路由器）— 数据发送到外部云模型之前的最后一道隐私保护关卡。对输出内容进行 PII/敏感信息检测与脱敏处理，根据数据敏感级别（Output Sensitivity Level, OSL）决定路由策略：低敏感数据可直发云端 Frontier Models（Anthropic、Google、OpenAI、xAI），高敏感数据强制路由到本地 Nemotron 模型或阻断发送。通过 `nvext_prefix_osl` 参数（LOW/MEDIUM/HIGH）控制敏感度阈值。

OpenShell 底层的代码执行在 Docker 容器中隔离运行，具备内存/CPU 资源限制、网络隔离、受控文件系统挂载、每进程独立执行等沙箱特性。

### LLM 引擎栈

NVIDIA 的 LLM 引擎由四层技术栈构成，覆盖从模型研发到推理部署的全流程：

- **Nemotron** — NVIDIA 自研模型家族（Nano、Super 等规模），针对 NVIDIA GPU 架构深度优化。Nemotron-3-Nano-30B-A3B 等模型可作为本地 Agent 的推理引擎，配合 `enable_thinking` 参数启用推理模式。
- **NeMo** — 模块化模型开发框架，提供数据准备、模型定制（微调/对齐）、评估、部署的全套工具链。NeMo Agent Toolkit（NAT）是上层 Agent 框架，通过 YAML 声明式配置组装 Agent 工作流。
- **Dynamo** — 面向延迟敏感型工作负载的分布式推理引擎，提供 `nvext` 路由提示（inter-arrival time sensitivity 和 output sensitivity level）实现请求级别的智能路由。
- **NIM**（NVIDIA Inference Microservices）— 容器化推理微服务，支持本地部署（Docker + GPU）和云端 API（build.nvidia.com）两种模式。本地 NIM 通过 `nvcr.io` 镜像拉取模型容器，云端通过 `NVIDIA_API_KEY` 鉴权。模型路由策略：低延迟/高隐私场景走本地 NIM + Nemotron；复杂推理/大规模场景走云端 Frontier Models；混合场景由 Dynamo 在两者之间动态负载均衡。

### Sub Agents

支持通过 AI-Q Research Agent 等多 Agent 协作模式。Orchestrator-Specialist 模式中，编排 Agent 持有全局任务视图，将子任务委托给专业 Agent 执行。子 Agent 可嵌套（Agent 作为 Tool 被上层 Agent 调用），每个子 Agent 拥有独立的 LLM 配置、工具集和系统提示，实现关注点隔离。

### Skills 与 Tools

Skills 是 Agent 可调用的能力模块，涵盖 cuOpt（GPU 加速运筹优化）、代码生成（支持 Python 等多语言）、网页查询、计算器等。Tools 通过 CLI 和 MCP（Model Context Protocol）协议连接外部资源，支持 stdio、SSE、streamable-HTTP 三种传输方式，可接入受 OAuth2 保护的远程 MCP 服务。不可信第三方 Skills 从 ClawHub 加载后经 Sandbox Guardrail 隔离执行。

## 关键特性

### Computer Use

Agent 可直接操控计算机而不仅限于对话交互。通过 Terminal 容器执行系统命令、操作文件系统、启动应用程序。Computer Use 能力受 OpenShell 三层安全检查约束：Policy Engine 限制可执行命令范围，Network Guardrail 防止 Agent 通过网络泄露数据，Privacy Router 确保屏幕/文件内容在发送到云端模型前完成脱敏。

### 多模型支持与混合路由

本地部署 Nemotron 系列模型（通过 NIM 容器），云端接入 Anthropic、Google、OpenAI、xAI 等 Frontier Models。Dynamo 推理引擎根据任务延迟要求、数据敏感级别、模型能力匹配度进行请求级路由决策。LiteLLM 适配器提供 100+ 模型提供商的统一接口。

### 工业集成深度

- **Isaac Sim** — NVIDIA 机器人仿真平台，Agent 可在此环境中进行机器人策略学习、传感器仿真、运动规划，将 Agent 的决策能力延伸到物理世界。通过 API/CLI/MCP 与 Agent Toolkit 连接。
- **Omniverse** — 数字孪生与 3D 协作平台，Agent 可在数字孪生环境中进行场景理解、资产操作、协同设计验证。
- **CAD 集成** — Agent 可直接操作 CAD 工具进行参数化设计、模型生成、工程分析，将生成式 AI 能力注入工业设计工作流。
- **IoT 集成** — Agent 通过 API/CLI/MCP 接入物联网设备数据流，实现设备监控、异常检测、预测性维护。

### 安全架构

安全是 NVIDIA Agent Toolkit 的一等公民。除 OpenShell 三层检查外，还包括：Docker 容器级代码执行隔离（内存/CPU 限制、网络隔离、进程隔离）、OAuth2 资源服务器认证保护 MCP 端点、RBAC 权限模型限制 Agent 访问范围、输入/输出内容过滤 Guardrail 防止提示注入与敏感信息泄露。Sandbox Guardrail 对从 ClawHub 加载的不可信第三方 Skills 进行全隔离执行，确保恶意或缺陷 Skill 无法突破容器边界。

## Related concepts

- [[Agent Runtime]] — OpenShell 是 Agent Runtime 的安全运行时实现
- [[Agent Secure Runtime]] — Agent 安全运行时的设计模式，OpenShell 是其工业级参考实现
- [[Multi-Agent 协作模式]] — Sub Agents 体现 Orchestrator/Specialist 模式与 Mixture-of-Agents 层次化编排
- [[Thin Harness, Fat Skills]] — ClawHub + Sandbox Guardrail 的 Skills 生态体现了 Thin Harness 理念

## Sources

- [[NVIDIA Agent Toolkit 架构]] — (2026-05-19) 架构图分析
- NVIDIA NeMo Agent Toolkit 官方文档 — 组件配置、多 Agent 编排、安全考虑
