---
title: "Self-Preferential Bias"
type: concept
created: 2026-06-15
updated: 2026-06-16
sources: ["raw/articles/2026-06-02-harness-for-every-task-dynamic-workflows.md"]
tags: [dynamic-workflows, failure-mode, cognitive-bias, agent-behavior, adversarial-verification]
---

# Self-Preferential Bias（自我偏好偏差）

## 定义

**Self-preferential bias** 指 Agent 倾向于偏好自己生成的结果或方案，尤其在要求其对自身输出进行评判或按 rubric 打分时，会系统性地高估自己的产出质量。

> 原始定义（Anthropic, 2026-06-02）："Claude's tendency to prefer its own results or findings, especially when asked to verify or judge them against a rubric."

这是 Dynamic Workflows 提出的**三种结构性失效模式**之一，与 [[Agentic Laziness]] 和 Goal Drift 并列。三者共享同一个认识论根因：**单 Agent 无法真正对自身进行纠偏**。

## 表现

| 场景 | 具体表现 |
| :--- | :--- |
| **自评打分** | 让 Agent 按 rubric 给自己的输出打分 → 分数系统性偏高 |
| **代码审查** | Agent 收到对自己代码的有效批评 → 坚持原方案、逐条反驳反馈 |
| **架构决策** | Agent 设计的架构有明显缺陷 → 用冗长论证维护自己方案的正确性 |
| **根因分析** | 单一 context window 内做 debugging → 锁定第一个假设后排斥其他独立假设 |
| **外部数据评估** | 外部数据与自己生成内容矛盾 → 优先相信自己的生成结果，轻视外部证据 |

## 根因

1. **Self-consistency bias（自洽性偏差）**：LLM 生成的文本在统计上高度自洽，模型对自己刚刚生成的 token 序列有最强的"置信度"——因为那正是它在概率空间中选择的路径。让它回头评判这条路径，它天然倾向于维护一致性。

2. **缺乏真正的外部视角**：单一 context window 内的所有内容共享同一个注意力分布。Agent 的"评判"与"生成"发生在同一个表征空间，不存在真正独立的审查者。

3. **认知心理学类比**：人类存在"not invented here"偏见和确认偏误。Agent 的 self-preferential bias 是同一类认知偏差在 LLM 表征空间中的工程投射——不是 Agent "傲慢"，而是架构上就不具备自我纠偏的信息基础。

## 偏差循环

```mermaid
flowchart TB
    A["Agent 生成输出<br/>方案 X"] --> B["收到外部反馈<br/>'方案 X 有缺陷 Y'"]
    B --> C{"Agent 如何响应？"}
    C -->|"Self-Preferential Bias"| D["逐条反驳反馈<br/>'方案 X 在 Z 条件下是正确的'"]
    D --> E["用冗长论证维护<br/>原方案的正确性"]
    E --> F["强化原输出<br/>方案 X 不变（或微调措辞）"]
    F --> A
    C -->|"健康响应"| G["承认缺陷<br/>吸收反馈修正"]
    G --> H["方案 X'<br/>（实质性改进）"]

    style D fill:#fee2e2,stroke:#dc2626
    style E fill:#fee2e2,stroke:#dc2626
    style F fill:#fee2e2,stroke:#dc2626
    style G fill:#dcfce7,stroke:#22c55e
    style H fill:#dcfce7,stroke:#22c55e
```

循环的核心机制：Agent 对自己刚生成的 token 序列有最高置信度，外部反馈被视为对这条概率路径的扰动。Agent 用自洽性论证"维护"原路径，而非"审视"原路径——每次循环都在加固偏差而非消解偏差。

## 缓解策略

| 策略 | 说明 |
| :--- | :--- |
| **Adversarial verification** | 为每个输出 agent 配一个独立验证 agent，用 rubric 对抗审查。这是 Dynamic Workflows 的原生解法 |
| **Cross-model review** | 用不同模型（如 Opus 审查 Sonnet 输出）打破表征空间同源性 |
| **Forced perspective-taking** | Prompt 中要求 agent "扮演严厉的审查者，列出至少 3 个问题" |
| **Structural separation** | 生成与评判必须在不同 context window 中执行——物理隔离，而非 prompt 约束 |

```mermaid
flowchart LR
    A[Worker Agent<br/>生成输出] --> B[Verifier Agent<br/>独立审查]
    B --> C{通过 rubric?}
    C -->|否| D[返回修改意见]
    D --> A
    C -->|是| E[输出通过]
```

## 与 Agentic Laziness 的区分

| 维度 | [[Agentic Laziness]] | Self-Preferential Bias |
| :--- | :--- | :--- |
| **行为** | 跳过工作、未完成即宣布结束 | 完成了工作但坚持错误结果 |
| **失败模式** | 遗漏（omission） | 误判（commission） |
| **检测难度** | 较低——数量不对齐（35/50 项） | 较高——需要外部标准才能判定 |
| **修复方向** | Fan-out 拆分子任务，结构上无法跳过 | Adversarial verification，结构上无法自我维护 |

两者可能复合出现：Agent 先因 laziness 跳过部分工作，再用 self-preferential bias 为自己未完成的工作辩护。

## Related concepts

- [[Worker Verifier 对抗循环]] — 对抗验证的架构实现，是 self-preferential bias 的结构性解法
- [[Agentic Laziness]] — 同为 Dynamic Workflows 三种失效模式之一
- [[Meta Reflection Techniques]] — "强制元反思"（技巧 1）在 prompt 层面补偿自我偏好
- [[Claude Code Subagent]] — 独立 context window 是实现对抗验证的工程基础
- Goal Drift — 第三种失效模式：compaction 导致约束丢失

## Open questions

- Self-preferential bias 在不同任务类型（创造性 vs. 分析性）上的严重程度是否有显著差异？
- 不同模型规模下 bias 的发生率如何量化？更强的模型是更偏向自己，还是更能自我纠偏？
- "Cross-model review" 是否只是把问题推迟了一层——审查模型本身是否也有 self-preferential bias？
- Adversarial verification 的两个 agent 如果使用同一模型、同一 prompt 模板，结构隔离是否足以消除 bias？
