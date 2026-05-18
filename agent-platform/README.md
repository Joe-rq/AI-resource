# Agent 平台与基础设施层

> 比模型层高一级，比应用层低一级——Agent 的整个执行平台面。

## 核心命题

单 AI 在长程任务上有四个结构性缺陷：任务压缩草率、逐步漂移、无法秒回、角色分工虚假。多 AI 协 作是解法，但关键不是"写更好的 prompt"，而是**搭一个能长期运行、能管理状态的底座**——即 Agent Platform / Runtime 层。

## 文档索引

| 文件 | 主题 | 核心观点 |
|------|------|----------|
| `01-minimax-single-ai-not-enough.md` | 单 AI 的四个结构性缺陷 | 任务压缩草率 / 逐步漂移 / 无法秒回 / 虚假分工 |
| `02-minimax-agent-team-tech-report.md` | MiniMax Mavis 技术报告 | **「多 Agent 系统是 runtime，不是 prompt 编排」** |
| `03-minimax-harness-strategy.md` | MiniMax Harness 策略 | Worker / Verifier 对抗循环；Harness 是可优化的工程层 |
| `04-anthropic-multi-agent-research-system.md` | Anthropic 多 Agent 研究系统 | 多 Agent 协作的架构设计 |
| `05-anthropic-managed-agents-api.md` | Anthropic Managed Agents API | 共享容器 + session thread 隔离的执行模型 |
| `06-claude-code-agent-teams.md` | Claude Code Agent Teams | 团队协作模式下的任务分发与执行 |
| `07-anthropic-cookbook-coordinate-specialist-team.md` | Anthropic 协调专家团队 | Orchestrator + Specialist 模式 |
| `08-agent-runtime-battlefield-20260516.md` | Agent Runtime 主战场 | **Runtime 可独立贡献 10-20pp；行业竞争重心正在转移** |

## 两个核心概念

### Runtime

单 Agent 的执行环境，包括：
- **Prompt 设计** — system prompt 定义模型角色和行为
- **工具定义** — 参数描述、返回值格式、调用时机
- **上下文管理** — 何时压缩、删什么保什么（影响 cache 命中率）
- **错误处理** — 错误消息质量决定模型能否自我修正

同一模型在不同 runtime 上可以差出 **10 个百分点**（Cline 实验数据）。

### Multi-agent

多 Agent 在 Runtime 之上的协作模式，核心架构：
- **Worker / Verifier 对抗循环** — Worker 干活、Verifier 挑刺，自动打回重做
- **Orchestrator / Specialist** — 中央协调者分发任务，专业 Agent 执行
- **Team Engine** — 确定性的状态机调度程序，不依赖某个 AI 的实时状态

### 关系

```
模型层
  ↓
Agent Platform 层
  ├── Runtime（单 Agent 执行环境）
  │     ├── Prompt
  │     ├── 工具定义
  │     ├── 上下文管理
  │     └── 错误处理
  │
  └── Multi-agent（多 Agent 协作模式）
        ├── Worker / Verifier
        ├── Orchestrator / Specialist
        └── Team Engine
  ↑
应用层
```

## 行业信号

- **DeepSeek** 热招 Agent Harness PM（产品方向仍在组建）
- **OpenAI** 成立 Deployment Co.，40 亿美元融资做全栈 Agent 服务
- **Anthropic** 推出 Claude Cowork + Partner Network（Blackstone、Goldman Sachs 各 3 亿）
- **AWS** 把 Runtime、Memory、Identity、Browser 列为 AgentCore 企业级模块
- **LangChain** 发布 Managed Deep Agents + SmithDB（专用可观测性数据库）
- **Cline** 开源内部 Runtime SDK（Apache 2.0）

行业重心正在从"**写 prompt**"转向"**维护控制面**"。
