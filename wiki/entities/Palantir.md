---
title: Palantir
type: entity
created: 2026-06-15
updated: 2026-06-15
sources:
  - raw/articles/2025-09-08-fde-playbook-bob-mcgrew.md
  - raw/articles/2025-11-11-alex-karp-palantir-ceo.md
  - raw/articles/2026-06-15-shyam-sankar-mobilize.md
tags:
  - company
  - agent-platform
  - defense
  - fde
  - palantir
---

# Palantir

> **Palantir Technologies** — 由 Peter Thiel、Alex Karp 等 2003 年创立的美国数据分析和 AI 平台公司。发明了 [[Forward-Deployed-Engineering]] 模式，核心产品包括 Gotham（国防/情报）、Foundry（商业）、AIP（AI 平台）、Apollo（持续部署）。

## 核心定位

Palantir 自称"**反剧本公司（anti-playbook company）**"。其核心信念：给美国和盟友提供"不公平的优势"。公司文化以极端精英治理（meritocracy）、极低层级（low hierarchy）、长期主义著称。

Alex Karp 的总结："我们花了二十年，才等到这一刻。FDE——所有人都觉得这套做法会毁掉公司；彻底的精英治理——大家都说你不该这么做；极低层级——几乎没人这么干过。"

## 核心产品矩阵

| 产品 | 领域 | 简介 |
|------|------|------|
| **Gotham** | 国防/情报 | 首个产品，本体论（Ontology）+ 链接分析，反恐/反扩散 |
| **Foundry** | 商业/工业 | 数据操作系统，Ontology + 工作流编排 |
| **AIP**（Artificial Intelligence Platform） | AI 平台 | LLM 编排层，Ontology + Foundry 的组合是核心护城河 |
| **Apollo** | 持续部署 | 跨环境（云/on-prem/边缘）的软件交付系统 |
| **Maven** | 国防 AI | 五角大楼 AI 项目，从地下室白手起家搭建 |

## 核心发明：本体论（Ontology）

Palantir 的本体论是其最基础的抽象层。起源故事：早期为情报界建数据库时，面临是否要为人、钱、船分别建表的选择。关键洞察是**把抽象层级拉高**——不定义具体对象类型，而是让客户自己定义。

本体论的核心概念只有四个：**对象（object）、属性（property）、媒体（media）和对象之间的链接（link）**。所有针对特定客户的专门信息（"这是一个人、一艘船、一笔资金流"）都编码在本体论中。

这成为 Palantir 所有产品的基石，也是 AIP 时代真正的护城河——LLM 是 commodity，orchestration（编排）才是价值核心。

## 核心发明：FDE 模式

参见 [[Forward-Deployed-Engineering]]。Shyam Sankar 在 2005 年前后发明了 FDE 战略，核心洞察：
- 从"个性化产品"转向"可定制平台"
- FDE 承担产品发现角色，填补产品与客户需求之间的鸿沟
- Echo 团队（嵌入式分析师）+ Delta 团队（部署工程师）

FDE 模式使 Palantir 走出了数量惊人的创业者，被称为"创业者的训练场"。

## 反 SaaS 的产品哲学

Alex Karp 区分了三种产品取向：

| 层级 | 做法 |
|------|------|
| 普通创新者 | 客户要什么就给什么 |
| 非常成功的软件公司 | 给客户看起来像 X 的东西，但绑死他们，再雇 5 万销售员收割 |
| **Palantir** | **客户都没意识到自己需要什么，你把它构建进去——告诉他们"应该要这个"** |

核心信念：**"做出客户会上瘾的产品，不是他们需要的产品"**——Palantir 最激进的就是反过来，给客户**应该要**的东西，把客户当作合作伙伴而非收割对象。

## AIP：在"黑夜"里押注未来

2023 年复活节前发布 AIP，Karp 形容这是"完全艺术化的"决定：
- **当时所有人都在说 LLMs 会解决一切**
- Karp 的判断：**LLM 是 commodity，orchestration 才是真正有价值的部分**
- Palantir 同时拥有 Ontology 和 Foundry——只缺把它们组装起来
- "如果你从专家意见和客户要求往回推，你不会发布这个东西"

AIP 发布后，客户心态发生根本翻转：从"这玩意儿到底行不行"变成"我的为什么不行？哪里能找到行的？" 销售周期从五年 vs 九个月压缩到五年 vs 两到三个月。

## 公司文化特征

- **极端精英治理**：Karp 和 Shyam Sankar 之间只隔一层（还是虚构的）
- **反老化**：二十岁公司，四到五岁公司的氛围——"部落感很强，坚守部落知识"
- **异端文化**：体制内异端需要两件事——存在的空间 + 来自高层的少量保护
- **学习型组织**：即使作为非常大的公司，仍然每个人所有时间专注学习

## 关键人物

- **Alex Karp** — CEO，艺术家母亲的儿子，将 Palantir 定位为"像艺术品一样做产品"
- **Shyam Sankar** — CTO / 第 13 号员工 / 美国陆军中校，发明 FDE 战略，著有《Mobilize》
- **Bob McGrew** — 前研究主管，后加入美国陆军预备役 Detachment 201
- **Colonel Drew** — 在五角大楼地下室从零搭建 Maven AI 项目的"内部异端"

## 与新书的关联

Shyam Sankar 的《Mobilize》系统阐述了 Palantir 背后的国防工业哲学：
- 1989 年 94% 的主要武器系统支出流向军民两用企业，冷战后萎缩为纯国防专才
- 国防市场是 monopsony（买方垄断）→ 单一否决点 → 需要异端打破规则
- 真正的威慑不是"库存"，而是"生产库存的能力"
- 美国最大的风险不是他杀（homicide），是自杀（suicide）

## 参考

- [[Forward-Deployed-Engineering]] — FDE 模式的系统阐述
- [[FDE 实战手册：AI 初创公司的前置部署工程（Bob McGrew）]]
