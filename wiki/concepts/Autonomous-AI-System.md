---
title: "Autonomous AI System"
type: concept
created: 2026-06-04
updated: 2026-06-21
sources: ["raw/articles/2026-06-02-ai-autonomous-system-tips.md", "raw/articles/2026-06-21-deli-auto-research-framework.md"]
tags: [autonomous-ai-system, harness, runtime, watchdog, worktree, state-persistence, yang-zhiping]
---

# Autonomous AI System（AI 自主干活系统）

## 定义

> 「衡量当前 AI 发展到了什么水准，就看一件事：在没有任何人类介入的前提下，它能独立工作多久、能不能交付高质量的成果。」 — 阳志平

**Autonomous AI System**（AI 自主干活系统）= 一种在人类离场（跑步、睡觉、跨日）后，AI 仍能持续运行、按既定编排推进任务、并在卡住时**永不停摆**的系统。与业界通用的 "harness" 同义，但更强调"人 vs AI 双节奏协同"这一本源问题。

来源文章：[[如何实现一个好的 AI 自主干活系统]]（阳志平，2026-06-02）。

## 关键判断标准

| 维度 | 衡量 |
|------|------|
| **持续运行时长** | 当前稳定 3 小时，可达 9 小时，偶发 36 小时+ |
| **交付质量** | 端到端、多样本、真环境压测都能跑通 |
| **永不停摆** | 单条任务卡住时整体推进不被阻塞 |
| **人介入点前置** | 关键决策在开工前对齐，而非返工时纠正 |

## 四个核心设计原则

### 1. 人介入点前置

> **把人介入的点，前置到「开工前」，而不是「返工时」。**

AI 在开工前先自我分流：高确定性任务一句话确认就放手；高不确定性任务先停下来，把关键决策点摆到人面前。这是 [[Agent Harness 治理协议]] "人机决策分层"的执行版——人类只做语义判断类决策，工程实施类决策 AI 自己做。

### 2. 反传统工程的"干了再说"

> 计划永远不是唯一的真相，实际产出才是。

复杂活也写计划，但计划只是一次性脚手架。**需求往往是「干」出来的，靠「想」想不全。** 这与 [[Dive into Claude Code（论文）]] 论文揭示的"minimal scaffolding + maximal operational harness"同源——harness 不是写一份完美的计划，而是让产出会说话。

### 3. 多视角对抗式自检

自检不是"再读一遍"。**有效的自检，是把自己分裂成几个互不相同、互相对抗的视角同时审。** 一个专挑冗余，一个专挑边界，一个专挑"为了实现新目标而破坏了旧功能"。视角越分化，越能逼出单一视角看不见的问题。

与 [[Worker Verifier 对抗循环]] 的"物理拦截 + 跨视角加权"同源。

### 4. 永不停摆（为失败预设绕行路径）

> 规则必须是：**单条卡住，就跳下一条，绝不阻塞整体推进。**

通过**意外处理矩阵**实现——提前预设 if-then 绕行路径：codex 评审超时怎么办、codex 持续 REQUEST_CHANGES 怎么办、测试 fail 修不动怎么办。这一原则在设计 AI 自主系统时几乎处处可见：**为失败预设绕行路径，别让局部的卡顿拖垮整体**。

## 12 个工程化技巧

| 组别 | 技巧 | 核心动作 |
|------|------|---------|
| 一·任务编排 | 1. 合并同类项 | 减少上下文切换；按复杂度从低到高排序；控制在 12h 可完成 |
| 一·任务编排 | 2. 确定性分流 | 开工前自检：上下文、元反思、是否需要重新定义问题 |
| 一·任务编排 | 3. 开工前确认世界没变 | boot 原则——读最新真实状态 |
| 二·实际开工 | 4. 干了再说 | 最小可用版本先跑起来；产出校准意图 |
| 二·实际开工 | 5. worktree 并行分身 | `git worktree` 隔离副本；约束在人类工作记忆以内 |
| 二·实际开工 | 6. 补齐测试 | 端到端、多样本、真环境压测 |
| 三·自检评审 | 7. 对抗性自检 | 多视角互相对抗；沉淀项目专用自检 Skill |
| 三·自检评审 | 8. 跨模型评审 | 干净上下文 + 不同谱系模型（如 `codex exec -m gpt-5.5`） |
| 三·自检评审 | 9. 分级修复 | P0/P1/P2；每轮给"通过/不通过"明确判据 |
| 四·自动续航 | 10. 看门狗 | CronCreate + 定时读状态文件 + "待办就执行" |
| 四·自动续航 | 11. 意外处理矩阵 | if-then 绕行；单条卡住就跳下一条 |
| 四·自动续航 | 12. 状态持久化 | 状态文件 = 唯一真相源；交班时产出"人话"汇报 |

## 长时间运行的工程深化：Deli_AutoResearch 交叉印证

[[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）]]（summary 35）从英文工程实践侧印证并深化了上面的"四·自动续航"组，核心增量：

| 维度 | 阳志平（本页） | Deli 深化 |
|------|---------------|-----------|
| 看门狗 | 技巧 10：CronCreate + 定时读状态文件 | **三层互检**（L0 常驻 shell guard / L1 durable cron / L2 业务自报）——失效链推理：守护层的依赖必须比被守护对象更弱。详见 [[Heartbeat Watchdog]] |
| 状态持久化 | 技巧 12：状态文件 = 唯一真相源 | append-only JSONL + **fresh session over resume**（resume 继承前序 session 的偏见，是认知循环的主因） |
| 停滞对策 | 意外处理矩阵：单条卡住跳下一条（横向绕行） | stall 检测 + **pivot 结构非战术**（纵向改框架）；且"停滞 > 崩溃"是长跑首要敌人 |
| 运行约束 | "永不停摆" | 配套硬约束：零交互（运行期绝不提问）、callback 报活（每轮首行更新 `last_seen`）、guardian/worker 分离（巡检对非己任务只读三权限） |

共同的底层判断：**治理靠结构约束，不靠模型自觉。** 这与 [[Agent Harness 治理协议]]、[[wow-harness]]、[[ESAA]] 的 boundary contracts 一致——纪律要物理化，不能停在 prompt 层"建议自检"。Deli 的 validation 是作者**框架内自评**（4 篇 ICLR 调研自评 8.0–8.6、72h 连续运行零运维介入），为"持续运行时长"提供了一个具体可比样本（对照本页的 3h 稳定 / 9h / 36h+）。

## 与现有 wiki 概念的关联

| Autonomous AI System 元素 | 对应 wiki 概念 |
|--------------------------|---------------|
| 合并同类项、约束任务清单 | [[Agent Runtime]] 上下文管理（"约束实体 ≤ 4" 经验值同源） |
| 干了再说、产出校准意图 | "事件意图 → 提交检查点验证"（参见 Agent Harness 治理协议） |
| worktree 并行分身 | [[Multi-Agent 协作模式]] 并行 Worker |
| 对抗性自检、多视角审查 | [[Worker Verifier 对抗循环]] |
| 跨模型评审 | "双层验证"（验证者与执行者不同上下文/不同模型，参见 Agent Harness 治理协议） |
| 看门狗、定时执行 | [[Meta Reflection Techniques]] 技巧 7；自动扩张任务图（Agent Harness 治理协议） |
| 状态持久化、唯一真相源 | [[ESAA]] Event Sourcing + 当前状态视图 |
| 意外处理矩阵、永不停摆 | [[wow-harness]] "为失败预设绕行路径" 处处可见 |
| 沉淀自检 Skill / 评审教训制度化 | [[Thin Harness, Fat Skills]] 90% 价值在 markdown 流程文件 |
| 三层看门狗 / fresh session / stall 检测 | [[Heartbeat Watchdog]]、[[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）]]（"自动续航"的工程深化） |

## "harness" vs "Autonomous AI System" 视角对比

| 维度 | harness（业界视角） | Autonomous AI System（阳志平视角） |
|------|--------------------|------------------------------------|
| 关注点 | 模型外的套具——prompt、工具、上下文、错误处理 | 人在回路/不在回路的整条运转闭环 |
| 衡量标准 | 同一模型在不同 harness 上差 4.8pp | AI 在无人类介入下能独立工作多久 + 交付质量 |
| 人的位置 | 调试者、优化者 | 关键决策者（在开工前介入） |
| 失败观 | harness 修复 75% 失败 | 永不停摆，单条失败跳下一条 |
| 优化对象 | 单次 session | 跨日、跨 session 的"持续" |

两者不矛盾——harness 是 Autonomous AI System 的实现手段之一（Runtime / 工具定义 / 上下文管理 / 错误处理），但 Autonomous AI System 把视角拉高到"人 vs AI 双节奏协同"的系统层。

## 实践飞轮

```
任务编排（人介入前置）
    ↓
实际开工（产出校准意图）
    ↓
自检评审（对抗 + 跨模型）
    ↓
自动续航（看门狗 + 状态文件）
    ↓
交班"人话"汇报
    ↓
沉淀 Skill 注入下一轮的任务编排
    ↓（飞轮）
```

**把评审中学到的东西制度化，是让 AI 自主干活系统越用越聪明的飞轮。**

## Open research questions

- Autonomous AI System 的"持续运行时长"上限在哪里？是否能无限延伸？
- 跨模型评审的"干净上下文 + 不同谱系"原则能否被自动化（如 ESAA 的 boundary contracts 化）？
- 意外处理矩阵本身是否需要版本控制 / 自我演化（与 Agent Harness 治理协议的约束规则独立生命周期关联）？
- 状态文件 vs ESAA 事件流——一个是扁平快照，一个是事件流，哪个更适合长跑场景？

## Related concepts

- [[Agent Runtime]] — Autonomous AI System 的运行时底座
- Agent Harness 治理协议 — 跨 session 长期一致性的治理层
- [[Meta Reflection Techniques]] — 元反思 = 让 AI 自主系统更聪明的飞轮核心
- [[Thin Harness, Fat Skills]] — 12 技巧制度化为 Skill 文件的理论依据
- wow-harness — 治理协议工程实现参考
- ESAA — 状态持久化的事件溯源学术化版本
- [[如何实现一个好的 AI 自主干活系统]] — 原始来源
- Heartbeat Watchdog — 看门狗的三层互检深化（Deli_AutoResearch）
