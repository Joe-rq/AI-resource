---
title: "Finding Your Unknowns"
type: concept
created: 2026-07-14
updated: 2026-07-14
sources: ["raw/articles/2026-07-03-field-guide-to-fable-finding-unknowns.md"]
tags: [agentic-coding, prompting, unknowns, blind-spot, prototyping, human-agent-collaboration, anthropic]
---

# Finding Your Unknowns

> Anthropic 官方（Thariq Shihipar）提出的 **agentic coding 方法论核心**：把 Rumsfeld 四象限 Unknowns 框架应用到与 agent 协作上——**减少并规划你的未知，就是 agentic coding 这项技能本身**。与 [[Context Engineering]] 互补：Context Engineering 讲"怎么把 context 喂给模型"，本框架讲"人先要知道自己缺什么 context"。

## 四象限框架

面对一个问题，按"我知不知道 × 我知不知道我知不知道"分为四类：

| 象限 | 定义 | 在 prompt 中的位置 |
|------|------|------------------|
| **Known Knowns** | 我明确知道且能写出来的 | 就是 prompt 本身 |
| **Known Unknowns** | 我知道自己还没想清楚的 | 待澄清项——interview / brainstorm 的对象 |
| **Unknown Knowns** | 显而易见到从不写下、但看到就能认出的 | 隐性标准——prototype "see it to know it" 的对象 |
| **Unknown Unknowns** | 完全没考虑到的知识盲区 | 盲区——blind spot pass 的对象 |

核心论断：**最好的 agentic coder 未知很少**（对 codebase 和模型行为 deeply in-sync），但他们同时**假设未知存在**并为之规划。

## 指令的两难与"地图 vs 领土"

- **过于具体** → 该 pivot 时 Claude 仍死守指令
- **过于模糊** → Claude 按行业最佳实践自行假设，可能不适合你的任务

不管理未知就两头都输：不知道路上何时有障碍，也不知道路明明通畅但你其实想让 Claude 转向。文章标题隐喻"map is not the territory"——prompt 是地图，任务是领土，方法论的目标是让两者匹配。模型越强，正确方法带来的收益越大：**长程任务结果不对，多半是未知定义不足，而非模型不行**。

## 技巧工具箱（按实现阶段）

每个 explainer / brainstorm / interview / prototype / reference 都是"在修复变贵之前，廉价地发现你不知道的事"。

### Pre-implementation

| 技巧 | 对治象限 | 做法 |
|------|---------|------|
| **Blind Spot Pass** | Unknown Unknowns | 直接用字面词 "blind spot pass" / "unknown unknowns" 让 Claude 找盲区并教你，先交代你是谁、知道什么 |
| **Brainstorm & Prototype** | Unknown Knowns | 让 Claude 出多个差异化方案/单文件 HTML mock，靠"看到才认得"提早言语化隐性标准；实现期才发现代价高 |
| **Interview** | Known Unknowns | 让 Claude 一次一个问题采访你，"优先问答案会改变架构的问题" |
| **Reference** | 难以言传的需求 | 最好的 reference 是**源码**——指向实现了你要的语义的库/组件，跨语言也比截图信息密度高 |
| **Implementation Plan** | 结构化残余未知 | 计划把最可能变的部分（数据模型/类型接口/UX 流）放最前供审查，机械重构沉底 |

### During implementation

- **Implementation notes** — 新 session 传入 spec/prototype 等 artifacts（fresh context window + 全部规划信息，cf. [[Deli_AutoResearch：长时间自主任务的协议框架（Victor Chen）|fresh session over resume]]）；让 Claude 维护 `implementation-notes.md`，偏离计划时选保守项、记入 "Deviations" 继续干——承认再多规划也有 unknown unknowns 潜伏。

### Post implementation

- **Pitch / Explainer** — 打包 prototype + spec + implementation notes 成单文档拿 buy-in：评审者往往从你当初的未知出发，专家想看到你覆盖了他们会预期的失败点。
- **Quiz** — 让 Claude 就变更出报告 + 测验，**全对才 merge**。对治"读 diff 只有浅理解"（行为依赖既有代码路径），是 [[Agentic Code Review]] intent reconstruction 的自我版本：先验证人理解了 agent 的产出，再让产出进主干。

## 定位与关联

- 与 [[Context Engineering]]：write/select/compress/isolate 假设你知道该给什么 context；本框架补上游——发现"该给但你不知道要给"的 context（unknown knowns/unknowns）。
- 与 [[Meta Reflection Techniques]]：同属元认知层，行动之环"意图象限"的具体化——开工前先校准意图与盲区。
- 与 [[Claude Code Loops]]：Turn-based loop 中"你交出检查"的质量取决于你的未知多少；quiz 技巧给了人这一侧的验证手段。
- 与 [[Agentic Laziness]] / [[Goal Drift]]：过于模糊的指令给失效模式留出空间；未知管理是前馈端的对治。
