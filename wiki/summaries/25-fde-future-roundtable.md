---
title: 前沿部署工程的未来：OpenAI、Ramp、Nominal、Dataland 圆桌
type: summary
created: 2026-06-15
updated: 2026-06-15
sources:
  - raw/articles/2026-05-28-fde-future-roundtable.md
tags:
  - fde
  - openai
  - ramp
  - nominal
  - dataland
  - agent-platform
---

# 前沿部署工程的未来：OpenAI、Ramp、Nominal、Dataland 圆桌

> South Park Commons 主办的圆桌对谈，四家前沿公司的 FDE 负责人直面一个反直觉问题：模型越来越强，为什么 FDE 反而更值钱？

## 四家公司如何定义 FDE

- **Calvin（Ramp）**：FDE 的 mandate 是拿下企业客户。用"一切必要手段"赢得 upmarket 单子。一个工程师替代 AM-PM-Engineer 传话链。
- **Jason（Nominal，CTO）**：FDE 是"赋能客户的使命"——摸到产品最前沿的边缘，把用户真正需要的东西喂进产品 roadmap。
- **Howard（Dataland）**：FDE 是命脉。卖给客户的是"满足具体业务需求的劳动力"本身，不是大平台。构建的是高度异构的 agent。
- **Colin（OpenAI）**：双 mandate——一边找可复现的问题构建平台（产品线），一边聚焦全球最难的行业（研究线），不管用什么手段。

## 模型变强了，为什么 FDE 反而更值钱

Howard 的答案：AI 拉宽了"可被解决的 B2B 问题域"。以前 SaaS 只能覆盖形状匹配的问题，但全世界在"劳动力"上的花费比那多一个数量级。既然要啃这片异构问题，就必须派真的懂 use case 的工程师上场。

Colin 的补充：**每个软件工程师在 coding 领域天然就是 FDE**——这就是 coding agent 爆发的原因。但要深入能源、半导体，你真的需要派 FDE 进去摸透那个行业的具体性。

## FDE 与咨询的边界

四家公司各有伤疤和教训：

- **Jason**：Palantir 经历过 FDE 团队"造反"的黑暗时代——他们说原产品对客户场景完全没用，自己重做一套。Nominal 刻意把曾搭过平台又被坑过的人放在头四个 FDE 岗。
- **Colin**：OpenAI 的新口径——**"这能做成 Codex 扩展吗？"** 一句话砍掉 80% 候选产品。剩下的两个（合规文档撰写、企业级 workflow 自动化）才勉强站得住。
- **Howard**：核心问题是"你有没有给客户持续交付价值，而且是建立在固定成本之上的"。每个客户身上学到的东西让下一个客户跑得更快——**让学习飞轮把初始固定成本压下来**。

## 如何衡量 FDE 的 ROI

- **Ramp 方式**：企业客户营收 ÷ 员工工资。一个 FDE 扛 5-6 个客户。尽量把改动压到最小，不给后面留维护债。
- **OpenAI 方式**：赌能帮客户省几亿到几十亿美元的问题。单个客户可能吃掉 15 个 FDE。但长期最赚钱的是产品型合作（2-4 个 FDE）。
- **Dataland 方式**：人均几百万 ARR 的杠杆——靠元智能体加速造新智能体的过程，让智能体在外循环里自动跟上业务变化。

## 数据回流到研究的 flywheel

Colin 举了两个案例：

1. **Slide Buddy**：试了 50 种格式化方式，最后找到一种，生成样本丢给 post-training 团队。三个月后新 snapshot 出来，slide 一下好看了。
2. **7 万通电话/天**：实时语音模型在客服场景上线，半年迭代——post-training 让模型变强，FDE 在上面搭自改进平台。

> flywheel 的形状：FDE 跟客户蹲在一起 → 搞清楚怎么把任务表示给模型 → 生成样本 → 研究团队改进模型 → 模型在该任务上变强。

## FDE 人才画像

- **Jason**：FDE 是**未来创始人最好的训练场**——从零到一搭建、站在 AI 最前沿、赢得企业客户信任、摸清组织政治格局。
- **Howard**：需要在 FDE 和核心产品工程之间**轮岗**——避免团队孤岛化。需要谦逊心、愿意跟着节奏变化走的人。
- **Calvin**：招前创始人、在乎营收的人。**"这是一个愿意说'是'的团队"**——因为想帮公司赢下客户。
- **Colin**：**对结果执念，而不是对方案执念**——客户不用你造的东西，就全部拆掉重做。背景多元（BCG、McKinsey、Palantir、前创始人），共同点是极度结果导向。

## 团队结构：Echo/Delta 的演化

OpenAI 在传统 Echo/Delta 基础上新增了**行业专家（industry experts）**角色——芯片验证工程师、生命科学科学家。数量不多，但希望产生超出自身规模的影响——所有通才型 FDE 从他们身上学习。

Dataland 则在尝试 AI 带来的新可能：**radical ownership（彻底的端到端所有权）**——AI 大幅压低编码边际成本后，一个人可以同时做 Echo + Delta，把所有上下文装在脑子里。

## 核心金句

> "服务收入是会上瘾的药。" — Colin

> "FDE 既是剑也是盾——既要去赢下企业 deal，又要保护核心团队不被拖偏。" — Calvin

> "FDE 是你号称是'platform'的那个东西的第一批用户。" — Jason

> "客户其实比公司自己更'上瘾'FDE。你真要把人撤走，他们就甩了你——这是最糟的。" — Howard

## 与 Agent 基础设施的关系

圆桌讨论的核心议题与 Agent 平台演进存在中等程度的关联：

- **[[Thin Harness, Fat Skills]]**："AI 不会取代 FDE，会放大 FDE"的核心结论与 thin harness + fat skills 架构有一致的哲学基础——AI 工具承担 thin harness 层面的重复性工作（部署脚本、监控配置），FDE 聚焦 fat skills 层面的判断力和信任建设。但这个类比是组织层面的，不涉及具体架构设计。
- **[[Agent Harness 治理协议]]**：FDE 团队汇报线之争（工程 vs 销售）映射到 Agent 平台治理中的一个真实问题——Agent 行为策略应由技术团队还是业务团队主导制定？治理协议的人机决策分层框架为这个问题提供了参考思路，但本文并未讨论 Agent 治理本身。
- **[[Multi-Agent 协作模式]]**：FDE 从"部署工程师"到"变革管理者"的角色演变，与 Agent 架构中从执行层到编排层的层级跃迁有类比关系。低层 Agent 处理执行，高层 Orchestrator 处理策略和变革。

总体评估：本文有 FDE 和 AI 交叉的讨论（AI 放大 FDE 能力），但核心内容是 FDE 团队管理和组织设计，与 Agent 基础设施技术的直接关联有限。保留价值中等。

## 参考

- [[Forward-Deployed-Engineering]]
- [[Palantir]]
