---
title: "Harness engineering for coding agent users \\ Martin Fowler / Birgitta Böckeler"
source: "url"
source_file: "https://martinfowler.com/articles/harness-engineering.html"
created: "2026-06-24T00:00:00Z"
source_url: "https://martinfowler.com/articles/harness-engineering.html"
extract_method: "anysearch-extract"
author: "Birgitta Böckeler"
affiliation: "Thoughtworks (Distinguished Engineer)"
---

# Harness engineering for coding agent users

Birgitta Böckeler, 2026-04-02, 转载于 Martin Fowler 站。这是 agent harness 控制论框架（前馈/反馈）的一手权威来源。

## 信任问题（为何需要 harness engineering）

> "LLMs are non-deterministic, they don't know our context, and they don't really understand the code, they think in tokens."

软件工程师对 AI 生成代码有天然信任壁垒。harness engineering 的目标是建立这种信任。

## Feedforward and Feedback（核心对偶）

> "To harness a coding agent we both anticipate unwanted outputs and try to prevent them, and we put sensors in place to allow the agent to self-correct."

- **Guides (feedforward controls)** — anticipate the agent's behaviour and aim to steer it **before** it acts. Guides increase the probability that the agent creates good results in the first attempt.
- **Sensors (feedback controls)** — observe **after** the agent acts and help it self-correct. Particularly powerful when they produce signals optimised for LLM consumption, e.g. custom linter messages that include instructions for self-correction — a positive kind of prompt injection.

> "Separately, you get either an agent that keeps repeating the same mistakes (feedback-only) or an agent that encodes rules but never finds out whether they worked (feed-forward-only)."

**只有反馈 → 反复犯同样错误；只有前馈 → 编码了规则却不知道是否生效。两者必须结合。**

## Computational vs Inferential（执行类型正交维度）

- **Computational** — deterministic and fast, run by CPU. Tests, linters, type checkers, structural analysis. Milliseconds to seconds; results reliable.
- **Inferential** — Semantic analysis, AI code review, "LLM as judge". GPU/NPU. Slower, expensive, non-deterministic.

### 2×2 矩阵示例

| 规则 | 方向 | 类型 | 实现 |
|---|---|---|---|
| 编码规范 | feedforward | Inferential | AGENTS.md, Skills |
| 项目 bootstrap | feedforward | Both | Skill + bootstrap script |
| Codemods | feedforward | Computational | OpenRewrite recipes |
| 结构测试 | feedback | Computational | pre-commit ArchUnit（模块边界） |
| Review 指南 | feedback | Inferential | Skills |

## The steering loop（人的工作）

> "The human's job in this is to **steer** the agent by iterating on the harness. Whenever an issue happens multiple times, the feedforward and feedback controls should be improved."

问题反复出现 → 改进 feedforward/feedback。coding agent 让构建自定义控制更便宜（agent 帮写结构测试、生成规则草稿、scaffold linter、从代码考古生成 how-to）。

## Timing: Keep quality left

把检查尽量前移到生产路径左侧（早发现 = 便宜修复）：
- 快的、commit 前跑（linter、快测试、基础 code review agent）
- 贵的、集成后 pipeline 跑（mutation testing、大局 code review）

**Continuous drift and health sensors**：持续运行的传感器（死代码检测、测试覆盖质量、依赖扫描）+ 运行时反馈（SLO 退化、响应质量采样、日志异常 AI judge）。

## The agent harness as cybernetic governor

> "The agent harness acts like a **cybernetic governor**, combining feed-forward and feedback to regulate the codebase towards its desired state."

明确用控制论（cybernetics）框架：harness = 前馈+反馈的组合调节器。

### Ashby's Law（必要多样性定律，sidebar）

控制论经典：一个控制系统的复杂度必须匹配被控系统的复杂度。harness 语境：要可靠控制 non-deterministic LLM 的产出，harness 的"调节多样性"必须足够。

## Regulation categories（调节维度）

harness 调节的"期望状态"分维度（harnessability 与复杂度各异）：

1. **Maintainability harness** — 内部代码质量与可维护性。最容易，有大量现成工具
2. **Architecture fitness harness** — 架构特征定义与检查（Fitness Functions）
3. **Behaviour harness** — 行为正确性

### Maintainability 的传感器盲区

- Computational sensors 可靠抓结构问题（重复代码、圈复杂度、覆盖缺口、架构漂移、风格违规）
- LLM 能部分处理语义问题（语义重复、冗余测试、暴力修复、过度工程）但贵且概率性，不能每次 commit 跑
- **高影响问题两者都不可靠抓**：误诊、过度工程/不必要功能、误解指令——会偶尔抓到，但不足以降低监督
- 正确性超出任何传感器能力——若人没先说清想要什么

## Harnessability & Harness templates & The role of the human

（详见原文）harnessability = 代码库被 harness 的难易；harness templates = 可复用 harness 模板；人的角色 = steer + 最终语义判断。

## How does harness engineering relate to context engineering?（sidebar）

把 harness engineering 与 context engineering 关系讲清——前者关注控制结构（前馈/反馈），后者关注信息填充。两者交叉但不等同。
