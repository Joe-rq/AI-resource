---
title: "Agent Secure Runtime"
type: concept
created: 2026-05-19
updated: 2026-06-16
sources: [raw/articles/nvidia-agent-toolkit.md]
tags: [agent-runtime, security, sandbox, guardrail, privacy]
---

# Agent Secure Runtime

## 定义

**Agent Secure Runtime** = 在 [[Agent Runtime]] 基础上增加安全层的执行环境，确保自主 Agent 在安全边界内运行。

核心问题：Agent 需要访问文件系统、网络、外部 API、甚至直接操控计算机（Computer Use），但这些能力也带来了数据泄露、越权操作、不可控行为等风险。Secure Runtime 通过多层护栏在"能力"和"安全"之间取得平衡。

## 三层安全架构

```mermaid
flowchart TB
    subgraph Layer1["Layer 1: Policy Engine（策略引擎）"]
        PE_Check["命令白名单/黑名单"]
        PE_RBAC["路径粒度 RBAC<br/>（读/写/删除权限）"]
        PE_Verify["来源验证<br/>（开发者指令 vs Agent 自主决策）"]
    end

    subgraph Layer2["Layer 2: Network Guardrail（网络护栏）"]
        NG_Filter["出站 IP/域名白名单"]
        NG_Rate["API 速率限制"]
        NG_Audit["访问审计日志"]
        NG_SSRF["内网敏感网段阻断"]
    end

    subgraph Layer3["Layer 3: Privacy Router（隐私路由）"]
        PR_Detect["PII/敏感信息检测"]
        PR_Desensitize["数据脱敏"]
        PR_Route["路由决策<br/>低敏感 → 云端 LLM<br/>高敏感 → 本地模型/阻断"]
    end

    AgentCmd["Agent 命令"] --> Layer1
    Layer1 -->|"通过"| Layer2
    Layer2 -->|"通过"| Layer3
    Layer3 -->|"通过"| External["外部模型/资源"]

    Layer1 -.->|"拦截"| Block1["🚫 阻断"]
    Layer2 -.->|"拦截"| Block2["🚫 阻断"]
    Layer3 -.->|"拦截"| Block3["🚫 阻断/路由到本地"]

    style Layer1 fill:#dbeafe,stroke:#3b82f6
    style Layer2 fill:#fef3c7,stroke:#f59e0b
    style Layer3 fill:#fce7f3,stroke:#ec4899
    style External fill:#dcfce7,stroke:#22c55e
```

三层按顺序执行，每层是独立的检查点：Policy Engine 控制"能做什么"，Network Guardrail 控制"能访问什么"，Privacy Router 控制"能发送什么"。任何一层拦截都会阻断命令执行。

以 [[NVIDIA Agent Toolkit]] 的 OpenShell 为例：

```mermaid
flowchart LR
    Dev[Dev Machine CLI] --> PE[Policy Engine]
    Hub[ClawHub Skills] --> SG1[Sandbox Guardrail]
    SG1 --> PE
    PE --> NG[Network Guardrail]
    NG --> PR[Privacy Router]
    PR --> LLM[External LLMs]
    NG --> Res[Resources: FS/Web/IoT]
    PE --> Agent[OpenClaw Agent]
```

### 1. Policy Engine（策略引擎）

Agent 命令的入口关卡。基于预定义规则决定 Agent 可以执行哪些操作。

- 白名单机制：只允许已授权的操作类型
- 权限分级：不同 Agent/任务授予不同权限集
- 来源验证：区分开发者直接指令和 Agent 自主决策

### 2. Network Guardrail（网络护栏）

控制 Agent 对外部网络、API、数据源的访问。

- 出站过滤：限制 Agent 可访问的域名/IP
- API 调用审计：记录所有外部请求
- 资源隔离：Filesystem / Web Search / IoT 等通过 API/CLI/MCP 统一接入

### 3. Privacy Router（隐私路由）

数据发送到外部云模型前的最后一道关卡。

- 敏感信息检测与脱敏
- 数据分类路由：本地模型处理敏感数据，云端模型处理非敏感数据
- 合规审计：确保数据流向符合隐私政策

## 沙箱隔离

对于不可信的第三方 Skills（如 ClawHub 中的社区贡献），需要额外的 **Sandbox Guardrail**：

- 容器化执行：Skills 在隔离容器中运行
- 资源限制：CPU / 内存 / 网络访问受限
- 终端隔离：Agent 的 Terminal 层与宿主系统分离

## 与其他概念的关系

- [[Agent Runtime]] — Secure Runtime 是 Agent Runtime 的超集，增加了安全约束层
- [[NVIDIA Agent Toolkit]] — OpenShell 是目前最完整的 Secure Runtime 实现之一
- MCP 协议 — 作为工具连接的统一接口，天然适合接入安全检查点

## Open questions

- 三层安全检查的性能开销有多大？对 Agent 响应延迟的影响？
- Privacy Router 如何处理上下文中的隐式敏感信息（如用户在 prompt 中无意透露的私人数据）？
- 不同安全级别（开发/测试/生产）是否需要不同的护栏配置？

## Related Concepts

- [[Agent Runtime]] — Secure Runtime 是 Agent Runtime 的超集，增加了安全约束层
- [[Quarantine Mode]] — 将安全边界从单 agent 内部前移到 agent 之间的结构隔离，是 Secure Runtime 在 multi-agent 场景下的自然延伸
- [[NanoClaw]] — 容器化隔离的轻量级实现，展示了 Secure Runtime 在资源受限环境下的可行形态

## Sources

- [[NVIDIA Agent Toolkit 架构]] — (2026-05-19) OpenShell 架构图分析
