---
title: "The New Rules of Context Engineering for Claude 5 Generation Models"
type: summary
created: 2026-09-02
updated: 2026-09-02
sources: ["raw/articles/46-context-engineering-claude-5-generation.md"]
tags: [context-engineering, claude-code, system-prompt, progressive-disclosure, overconstraint, auto-memory, tool-design, rubric, verifier-agent, anthropic, thariq-shihipar]
---

# The New Rules of Context Engineering for Claude 5 Generation Models

> 原始来源：[claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)（作者 Thariq Shihipar——[[A Field Guide to Fable: Finding Your Unknowns]] 同一作者，本文为其续篇）
> 发布日期：2026-07-24 · 摄取日期：2026-09-02
> 论点反哺 [[Context Engineering]]、[[Agent Memory]]、[[Thin Harness, Fat Skills]]。

## 摘要

Anthropic 对 Claude 5 代模型（Opus 5、Fable 5）**删除了 Claude Code system prompt 的 80% 以上，编码评估无可测量损失**。根因不是"模型变聪明了"这么简单，而是旧的 context engineering 实践对新一代模型已从"最佳实践"退化为"神话"（myths）。核心病症是 **overconstraint**：system prompt、skills、CLAUDE.md 与用户请求互相冲突（如 "DO NOT add comments" 撞上用户要求注释），模型被迫更费力地调和矛盾；而其中许多约束本已无必要。官方提供了 `/doctor` 命令自动 rightsizing skills 与 CLAUDE.md。

## 六组 Then → Now

| Then（旧神话） | Now（新规则） | 原文例子 |
|----------------|---------------|----------|
| 给模型规则 | 让模型用**判断力** | 旧："默认不写注释、绝不写多段 docstring"；新："Write code that reads like the surrounding code" |
| 给模型示例 | **设计工具接口** | Todo 工具用 pending/in_progress/completed 枚举自解释，不必喂示例（示例反而收窄探索空间） |
| 全部前置加载 | **Progressive disclosure** | 验证/代码评审移入独立 skills；部分工具 deferred loading（需 ToolSearch 取全定义）；CLAUDE.md 应是**按需加载的文件树**而非单文件仓库 |
| 重复自己（多处强调） | 简洁的 **tool description** | 工具用法只写进 tool description，从 system prompt 删除重复 |
| 记忆存 CLAUDE.md | **Auto-memory** | 弃用 `#` 手动保存，模型自动持久化与工作和用户相关的记忆 |
| 简单 spec（纯 markdown） | **Rich references** | spec 可以是测试套件、可移植的函数、HTML artifact；**rubric + dynamic workflows 起 verifier agents** 验证品味类目标 |

## 拼装建议（按层）

- **System prompt**：绑定产品角色，自建 harness 时才值得花大力气
- **CLAUDE.md**：轻量，token 花在 codebase 的 gotchas 上，别写"看文件系统就知道"的显见事实
- **Skills**：编码"你/团队/产品特有"的判断与最佳实践；长 skill 拆成多文件渐进加载
- **References**：优先**代码形态**的高保真引用——HTML mockup > 设计描述/截图

## 与 wiki 现有论述的关系

- 直接演进 [[Context Engineering]]：Anthropic 2025-09 的 progressive disclosure/just-in-time 论述在本篇获得**模型代际维度的实证**（80% 删减 + 无评估损失）
- auto-memory + 身份隔离记忆是 [[Agent Memory]] 遗忘机制研究问题的新厂商实现样本
- overconstraint = [[Harness Cybernetics]] 前馈过载：guide 太多反而制造 Context Clash（[[Context Engineering]] 四失败模式之一）
- 与 [[Agent Reliability vs Capability]] 的"memory scaffolds 损害长程 reliability"结论形成有趣张力——Anthropic 的方向是削减 scaffolds、相信模型判断
