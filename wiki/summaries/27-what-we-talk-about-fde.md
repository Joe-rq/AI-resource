---
title: 当我们谈论 FDE 时，我们在谈论什么？
type: summary
created: 2026-06-15
updated: 2026-06-15
sources:
  - raw/articles/2026-05-04-what-we-talk-about-fde.md
tags:
  - fde
  - palantir
  - agent-platform
  - go-to-market
  - platform-product
---

# 当我们谈论 FDE 时，我们在谈论什么？

> 一篇中文圈罕见的 FDE 深度分析：用四个要素精确定义 FDE，区分真 FDE 与三种"穿新衣的旧角色"，拆解 Echo/Delta/Dev 三角循环，揭示 AI 时代 FDE 复兴的结构性原因。

## 一句话定义

**FDE 是嵌入客户环境的工程师，背靠一个平台级产品，通过在现场解决客户的真实问题来发现产品应该长什么样。他的工作产物不属于单一客户，而是回流到平台，成为可服务更多客户的产品能力。**

## 四个要素（缺一不可）

| 要素 | 含义 | 缺失则变成 |
|------|------|-----------|
| **有平台** | 平台级产品是前提 | 咨询师 |
| **嵌入客户环境** | 在客户工作环境里从内部理解问题 | 传统产品团队 |
| **目的是产品发现** | 去现场发现"产品应该长什么样"，不是实施已知方案 | 系统集成商 |
| **产物回流平台** | 工作成果成为可服务更多客户的产品能力 | 外包 |

> Flybridge 的 Daniel 的精炼表述：**FDE 是一个以人的形式存在的产品发现循环**（a product discovery loop embodied as a person）。

## 真假 FDE 试金石

- **成本归属检验**：FDE 的成本在公司内部是算产品研发的，还是算项目交付的？后者就是咨询/实施。
- **Thomas Otter 法则**：*"If the FDE is billable, they are working for the project, not the product."*
- **第 10 个客户检验**：第 10 个客户跟第 1 个客户花的精力一样多吗？如果是，就是在做咨询。

## 三种"穿新衣的旧角色"

市场上大量自称 FDE 的岗位本质上是：

1. **咨询型**：帮客户规划"你应该用 AI 做什么"，产出是方案和建议（McKinsey、EY）
2. **实施型**：帮客户把某个 AI 产品部署上线，产出是配置好的系统（Accenture）
3. **SE 换标签型**：把 Solutions Engineer 改个 title 叫 FDE，工作内容不变

三种都不是 FDE——因为产物都不回流到任何平台。

## FDE 的运作：Echo/Delta/Dev 三角循环

| 角色 | 定位 | 画像 |
|------|------|------|
| **Echo**（回声团队） | 嵌入式分析师，找到正确的问题 | 领域老兵 + **异端**（heretic）——理解现状但认为不够好 |
| **Delta**（三角洲团队） | 前线工程师，快速构建方案 | 快速原型能力，不是匠人——更像**艺术家社群** |
| **Dev**（平台工程师） | 留在总部，开发维护平台 | "一个能力，多个客户"的视角 |

> Palantir 官方博客总结：Dev 的视角是"一个能力，多个客户"；Delta 的视角是"一个客户，多种能力"。

## 飞轮：碎石路 → 铺好的路

1. FDE 在客户 A 现场发现需求 → 做碎石路方案
2. 带回总部 → 产品团队问"通用版本是什么？"
3. 拉来客户 B、C 的 FDE 共同设计 → 确保通用
4. 产品团队构建通用能力 → 纳入平台
5. 下一个 FDE 去客户 D 时直接使用 → 不用从头来

> a16z 的 Marc Andrusko：**把 FDE 当作脚手架（scaffolding），而不是建筑本身。** 脚手架是临时的，建筑立起来后要拆掉。

## Palantir 是启发，不是手册

文章区分了两个独立维度：

- **FDE 方法论本身**：Echo+Delta 结构、碎石路→铺好的路、产物回流飞轮
- **Palantir 的 GTM 策略**：Outcome-based pricing、Land and expand、Demo-driven development、解决 CEO top-5 问题、早期承担所有风险

> Palantir 不只是"软件公司 + 咨询"。它是"软件公司 + 咨询 + 政治工程 + 极其耐心的资本"。

## 五道压力测试题（Marc Andrusko）

1. 平台边界在哪里？共享产品止于何处？定制从哪里开始？
2. 从签约到生产环境要多少 engineer-months？
3. 第三年的利润率？成熟客户的 FDE 投入是否在下降？
4. 如果明年签 50 个客户，什么会先崩？
5. 你如何决定**不做**定制？

## 为什么 AI 时代天然适合 FDE

### AI 是全新品类，价值由使用者定义

传统 SaaS 替换已有产品，市场已知。AI agent 不替换任何东西——**价值不是产品团队定义的，是使用者发现的**。ChatGPT 发布时 OpenAI 工程师自己都没预料到它会成功；Claude Code 的黑客松冠军是律师、季军是心脏科医生。

### 能力远超采用，FDE 填的是这个 gap

AI 能力进步极快，但采用率远远跟不上。Bob McGrew 的比喻：你坐在无人驾驶的 Waymo 里，反应是"怎么堵车这么严重"——技术到了科幻程度，体验变得平淡。

### 平台转型期的特征

a16z 的 Joe Schmidt：企业买 AI 就像奶奶拿到 iPhone——她想用，但需要你帮她设置。在 platform shift 期间，implementation-heavy 不是缺陷，是特征。Salesforce IPO 前烧掉 5200 万美元才产生 2200 万美元收入。

## 窗口期与终局

Sequoia 的 Julien Bek 提出 Intelligence vs Judgement 框架：
- 写代码是 intelligence（可编码的认知工作）→ AI 正在快速接管
- 决定下一步做什么是 judgement（需要经验和品味）→ FDE 目前做的大量工作是 judgement

> **"Today's judgement will become tomorrow's intelligence."** 今天需要 judgement 的事，最终也会变成 intelligence。这个窗口会收缩。

### 终局判断

> *"The next $1T company will be a software company masquerading as a services firm."* — Julien Bek (Sequoia)

下一个万亿美元公司，将是一家伪装成服务公司的软件公司。从外面看在做服务，从里面看在做产品。当平台足够强大、用户可以自己跑起来的那一天，FDE 作为角色会消失——但 FDE 作为方法论留下了被无数次客户部署打磨过的平台。

## 与 Agent 基础设施的关系

本文是中文深度分析，对 FDE 的定义和判断框架最系统化，与 Agent 基础设施的关联主要是框架类比：

- **[[Thin-Harness-Fat-Skills]]**：四要素定义（工程能力 + 部署能力 + 产品思维 + 现场存在）与 skill 生态的分工有合理的对应——工程和部署能力对应 thin harness 提供的平台基础设施，产品思维和领域知识对应 fat skills 承载的内容。但"现场存在"在 Agent 语境中没有直接对应物——Agent 的"嵌入"是通过 API/工具集成实现的，与人类物理在场有本质区别。
- **[[Agent-Macro-Evaluation]]**：真假 FDE 判断框架的六个维度（工作地点、交付物、反馈循环、时间尺度、代码深度、责任边界）为 Agent 部署效果评估提供了有价值的思考框架——Agent 系统是否真正融入工作流？是否产生生产级影响？这些问题的评估维度可以从 FDE 判断框架中获得启发。
- **[[Claude-Code-Skills/index|Claude Code Skills]]**：AI-native FDE 用 AI Agent 处理部署、监控、告警等重复性工作，正是 skill 机制的核心应用场景。这是本文与 Agent 平台实践最直接的技术连接点。
- **[[Agent-Harness-治理协议]]**：真假 FDE 中"对结果负责 vs 对交付物负责"的区分，对应治理协议的结果导向治理原则——Agent 治理不应以调用次数或响应时间为指标，而应以任务完成质量为核心。

总体评估：本文对 FDE 的系统化定义和判断框架对 Agent 部署评估有启发价值，但核心内容仍是 FDE 方法论分析而非 Agent 技术。保留价值中等偏高。

## 参考

- [[Forward-Deployed-Engineering]] — FDE 概念系统阐述
- [[Palantir]] — FDE 模式的发明者
- [[FDE 实战手册：AI 初创公司的前置部署工程（Bob McGrew）]]
- [[前沿部署工程的未来：OpenAI、Ramp、Nominal、Dataland 圆桌]]
