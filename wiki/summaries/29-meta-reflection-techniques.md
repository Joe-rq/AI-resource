---
title: "12 个元反思技巧"
type: summary
created: 2026-06-04
updated: 2026-06-15
sources: ["raw/articles/2026-03-17-meta-reflection-techniques.md"]
tags: [meta-reflection, harness, agent-quality, prompt-engineering, dev-loop, action-loop]
---

# 摘要

> **来源**：阳志平「让 AI 变得更聪明的 12 个元反思技巧」（2026-03-17）。
>
> 完整的 12 技巧体系、行动之环框架、实施指引，见 **[[Meta Reflection Techniques]]**。

## 核心框架："对齐 = 补全"

本文最独特的认知重构是把"对齐"从哲学概念降维到工程动作：

```text
A 不完善，B 来补全 A
B 不完善，A 来补全 B
人类不完善，AI 补全人类
AI 不完善，人类补全 AI
项目 1 不完善，项目 2 来补全
模块 1 不完善，模块 2 来补全
```

**找到相对完善的那点，就是设计整个工作流的起点**。"确认成本"与"确认系数"是判断"完善"的标尺——把"对齐"从抽象目标变成可操作的工程决策。

作者由此推导出 12 个元反思技巧，分属四个象限（通用/意图/实施/反馈），围绕"行动之环"（意图 → 实施 → 反馈 → 情境）组织。其中 AI 的"情境" = 上下文 Context，这成为连接 prompt engineering 与 multi-agent 架构的桥梁。

## 实施建议（给本知识库运营者）

| 实施项 | 对应技巧 | 预期效果 |
| :--- | :--- | :--- |
| 在 ingest 流程中显式加入"自我校验"环节 | 6. 自我校验 | 减少编译/链接错误、frontmatter 不规范 |
| 在 audit 流程中显式加入"同类扫描" | 11. 同类扫描 | 修一个 wikilink 错时，扫描所有 page 的同模式问题 |
| 在每次 ingest 末尾追加"积累飞轮"动作 | 12. 积累飞轮 | 把新发现的 wiki 模式沉淀到 `memory/wiki-patterns.md` |
| 引入"重新定义问题"作为 query 阶段的首步 | 3. 重新定义问题 | 避免在错误的问题上做大量工作 |
| 引入"对齐"作为 compile 阶段的检查项 | 9. 对齐 | 确保结构变化对齐最初的目标 |

## 阅读指引

Read this summary for the original framing of "对齐 = 补全" and practical wiki-operation advice. Read **[[Meta Reflection Techniques]]** for the full 12-technique system, the 4-quadrant breakdown, and implementation paradigms.
