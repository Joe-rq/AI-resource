---
title: "Goal Drift"
type: concept
created: 2026-06-15
updated: 2026-06-15
sources: ["raw/articles/2026-06-02-harness-for-every-task-dynamic-workflows.md"]
tags: [dynamic-workflows, failure-mode, agent-behavior, task-planning, compaction]
---

# Goal Drift

## 定义

Goal Drift（目标漂移）是指 Agent 在长时间、多轮次任务中，逐渐偏离原始目标的客观要求，但 Agent 自身并未意识到这种偏离。每一次上下文压缩（compaction）都是信息损失事件，导致边缘约束、否定性指令（"don't do X"）和验收标准逐步丢失。

Anthropic 官方将 Goal Drift 列为动态工作流的**三种结构性失效模式**之一，与 [[Agentic Laziness]]（提前终止）和 [[Self-Preferential Bias]]（自我偏好偏差）并列。

## 表现

- **范围蔓延**：Agent 在修复 bug A 时"顺便"重构了相邻模块，引入了新问题。
- **"While I'm at it" 综合征**：每次迭代都在原目标上叠加自创的子任务，最终交付物与原需求失配。
- **约束遗忘**：最初的否定性指令（"不要修改 API 签名""不要动 CI 配置"）在多轮 compaction 后被丢弃。
- **验收标准偏移**：Agent 自行降低完成标准，将"通过 95% 测试"替换为"通过大部分测试"。

## 根因

Goal Drift 的根本原因来自三个叠加因素：

1. **上下文窗口演化**：旧指令被逐出上下文窗口后不可恢复，Agent 只能基于当前窗口做决策。
2. **Compaction 信息损失**：Claude Code 的 5 层压缩管线（参见 [[Dive into Claude Code（论文）]]）在摘要化历史时必然丢失细节，而否定性约束和边缘需求首当其冲。
3. **复合性小决策**：每个单步看似合理，但缺乏显式的目标重锚定机制，累积起来形成方向性偏离。

## 缓解策略

| 策略 | 说明 |
|:---|:---|
| **周期性目标重锚定** | 每 N 轮将原始目标文本重新注入上下文，迫使 Agent 对齐 |
| **显式任务边界标记** | 在 prompt 中使用 `## GOAL` / `## CONSTRAINTS` 分隔块，compaction 时优先保留 |
| **基于检查点的验证** | 每个里程碑用独立 subagent 按原始验收标准验证当前输出 |
| **State file 作为锚点** | 将目标和约束写入外部 state 文件，Agent 每轮读取，不依赖上下文记忆 |
| **Subagent 隔离** | 给每个 subagent 独立、聚焦的目标，其上下文窗口不受主对话漂移影响 —— 这是 Dynamic Workflows 的核心对策 |

## 与另两种失效模式的区分

| 失效模式 | 核心特征 | 简单记忆 |
|:---|:---|:---|
| **Agentic Laziness** | 任务未完成就宣称完成 | 提前终止 |
| **Self-Preferential Bias** | 坚持自己的错误，无法自我纠偏 | 固执犯错 |
| **Goal Drift** | 一直在干活，但方向逐渐偏了 | 渐行渐远 |

三者共同构成了"单 Agent 在长任务上结构性失败"的论证基础：不是 Agent 不够聪明，而是单上下文窗口的架构限制使这些失效不可避免。

## Related concepts

- [[Agentic Laziness]] — 提前终止：三种失效模式中最容易检测的一种
- [[Self-Preferential Bias]] — 固执犯错：对抗验证的对立面
- [[Autonomous AI System]] — 意外处理矩阵提供了任务偏移后的恢复框架
- [[Agent Runtime]] — 上下文管理是 Goal Drift 的工程根源
- [[Dive into Claude Code（论文）]] — 5 层 compaction pipeline 是 Goal Drift 的直接技术成因
- [[A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读]] — 三种失效模式在 wiki 中的首次记录来源

## Open questions

- Goal Drift 在多少轮次后变得可测量？是否存在可量化的"漂移速率"指标？
- 哪种约束类型最容易在 compaction 中丢失？否定性约束 vs 数值阈值 vs 格式要求？
- Goal Drift 与 Claude Code 5 层 compaction pipeline 各层的具体关系是什么？哪一层损失最大？
- 周期性重锚定的最优频率是多少？是否存在锚定疲劳（Agent 忽略重复注入的目标文本）？
