# Runtime 查询结果 (2026-05-19)

## Wiki 中的 Runtime 相关内容

### 1. 核心概念页：`wiki/concepts/Agent-Runtime.md`

定义单 Agent 执行环境，包含四个组件：
- **Prompt 设计** — system prompt 定义模型角色和行为
- **工具定义** — 参数描述、返回值格式、调用时机
- **上下文管理** — 何时压缩、删什么保什么
- **错误处理** — 错误消息质量决定模型能否自我修正

关键数据：同一模型在不同 runtime 上可差出 **10 个百分点**（Cline 实验）。

### 2. 战场分析：`wiki/summaries/08-agent-runtime-battlefield.md`

核心论点：Agent Runtime 正在成为 AI 行业下一个主战场，行业重心正从"写 prompt"转向"维护控制面"。

关键发现：
- Cline vs Claude Code (同一模型)：74.2% vs 69.4%，差 4.8pp
- Cline hill climbing：opus-4.5 从 47% → 57%，+10pp 全部来自 runtime
- LangChain harness profile：同一模型有无 harness 差 10-20pp

行业信号：DeepSeek 热招 Agent Harness PM、OpenAI 成立 Deployment Co.、Cline 开源内部 Runtime SDK。

### 3. Mavis 中的 Runtime：`wiki/entities/MiniMax-Mavis.md`

Mavis 设计哲学："多 Agent 系统是 runtime，不是 prompt 编排"。核心是 Worker/Verifier 对抗循环 + Team Engine 状态机调度，两个 AI 之间不直接通讯，靠程序中转。

## Promete 评估

**值得 promote 到 `wiki/concepts/`** 的理由：
- Runtime 是 Agent 平台的核心基础设施层，当前仅有 `Agent-Runtime.md` 一个概念页
- 行业正在从"写 prompt"转向"维护控制面"——这是架构层面的重大转变，值得单独提升为概念
- 现有内容深度足够（四个设计决策、25/75 法则、性能数据），但缺少具体实现差异的分析

**建议补充后再 promote**：
- Open Research Questions 中提到"Agent Runtime 的具体实现差异（Prompt 设计/工具定义/上下文管理/错误处理）具体怎么影响性能？"
- 当前页面缺少与 Multi-Agent 架构中 Runtime 角色的对比（单 Agent Runtime vs 多 Agent Team Runtime）

## 文件位置
- 概念页：`D:\AI-resource\wiki\concepts\Agent-Runtime.md`
- 战场分析：`D:\AI-resource\wiki\summaries\08-agent-runtime-battlefield.md`
- Mavis 实体：`D:\AI-resource\wiki\entities\MiniMax-Mavis.md`
- Worker/Verifier 对抗循环：`D:\AI-resource\wiki\concepts\Worker-Verifier-对抗循环.md`