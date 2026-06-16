---
title: Self-Evolving Memory
type: concept
created: 2026-06-15
updated: 2026-06-16
sources:
  - raw/articles/2026-05-02-hermes-agent-nous-research.md
  - raw/articles/2026-05-17-nanoclaws-second-brain.md
tags:
  - agent-memory
  - self-evolution
  - hermes
  - nanoclaws
parent: wiki/concepts/Agent-Memory/index.md
---

# Self-Evolving Memory

自我进化型记忆（Self-Evolving Memory）是 Agent Memory 的最激进形态——Agent 不仅存储和检索记忆，还能从交互中自动提炼模式、生成可复用的技能，并将这些技能写回记忆系统供未来调用。这是 [[Nous Research]] 的 [[Hermes Agent|Hermes]] 和新加坡外长的 [[NanoClaw]] 系统的共同设计目标，但实现路径截然不同。

## Hermes：自动封装操作

[[Hermes Agent|Hermes]] 的自我进化机制核心是 **execute → observe → extract pattern → write to memory** 循环：

1. **Execute**：Agent 执行用户指令，完成任务
2. **Observe**：监控执行过程，识别可复用的操作模式
3. **Extract Pattern**：将模式抽象为结构化的技能文件（skill file），包含步骤、前置条件、预期输出
4. **Write to Memory**：将技能文件写入长期记忆，后续类似任务直接调用

Hermes 生成的技能文件是透明可查的——用户可以看到 Agent "学到了什么"，这对信任构建和审计至关重要。在医疗场景中，这种透明度是监管合规的基本前提。

## NanoClaw：图谱演化

[[NanoClaw]] 的 Mnemon 图谱记忆系统走的是更温和的演化路径：

- 每次交互自动更新图谱：新增实体节点、补充关系边、强化高频路径的权重
- Ollama 本地嵌入模型提供语义搜索，将新信息与已有记忆自动关联
- Obsidian + iCloud 提供人类可读的记忆可视化界面，支持手动策展

与 [[Hermes Agent|Hermes]] 的显式技能生成不同，[[NanoClaw]] 的演化是隐式的——图谱结构随使用自然生长，没有显式的"学到一个技能"的边界。

## 对比

| 维度 | Hermes | NanoClaw |
|------|--------|----------|
| 演化方式 | 显式技能文件生成 | 隐式图谱结构生长 |
| 可审计性 | 高（每步操作封装为文件） | 中（图谱可视化，但无版本边界） |
| 用户介入 | 低（自动化为主） | 高（Obsidian 手动策展） |
| 部署 | 云端 | 本地（树莓派） |

## 监管与隐私挑战

自我进化型记忆在高度监管领域（如医疗）面临根本性挑战：

- **FDA/NMPA 合规**：医疗器械软件要求确定性行为，自我进化意味着每次运行结果可能不同，这与 SaMD（Software as a Medical Device）的验证框架冲突
- **遗忘权**：GDPR 的被遗忘权要求系统能删除特定个人数据，但自我进化后的记忆已融入模型行为，精确删除极其困难
- **隐私边界**：本地部署（NanoClaw 模式）在隐私保护上有天然优势，但代价是可扩展性和协作能力受限
