# NVIDIA Agent Toolkit 架构图

来源：微信聊天分享的两张架构图（2026-05-19）

## 图1：NVIDIA Agent Toolkit 总览

以 NemoClaw（Agent Core）为中心的 hub-and-spoke 架构：

- **输入**：Multimodal Prompt（文本/图像等多模态输入）
- **数据与硬件**：cuDF/cuVS（GPU 加速数据处理与向量搜索）、vGPU、结构化/非结构化文件、Computer Use
- **智能与编排**：LLM 引擎（Nemotron / NeMo / Dynamo / NIM）、Sub Agents（AI-Q Research Agent）、Skills（cuOpt 优化引擎）
- **记忆与工具**：Memory（上下文持久化）、Tools（CLI, MCP）
- **安全层**：OpenShell（安全执行环境/标准化接口）

## 图2：OpenShell Secure Runtime

专注于 Agent 的安全运行时架构：

- **核心安全层**（三层检查点）：
  - Policy Engine — 命令入口，基于预定义规则控制 Agent 权限
  - Network Guardrail — 控制 Agent 对外部网络/ API / 数据源的访问
  - Privacy Router — 数据发送到外部云模型前的隐私保护/脱敏
- **Agent 容器**：
  - OpenClaw：Definition / Memory / Skills / Terminal 四层容器
  - Coding Agents：支持 Claude、ChatGPT、GitHub Copilot 等多模型
- **外部模型**：Nemotron 3 Super Dynamo / TRT-LLM + Cloud Frontier Models（Anthropic, Google, OpenAI, xAI）
- **资源集成**：Filesystem、Web Search、IoT、Isaac Sim、Omniverse、CAD（通过 API / CLI / MCP）
- **输入源**：Dev Machine (CLI)、ClawHub (Unsecure Skills + Sandbox Guardrail)
