---
title: "Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀"
type: summary
source_url: https://x.com/wquguru/article/2069641926752780384
source_type: article
date: 2026-06-24
ingested: 2026-06-26
tags: [agent-memory, agent-architecture, claude-code, openclaw, hermes-agent, everos, memory-governance, skill-extraction]
---

# Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀

**Source**: [WquGuru (@wquguru)](https://x.com/wquguru/article/2069641926752780384) · 2026-06-24

## Key takeaways

- Agent Memory 不是长上下文的替代品，而是跨会话、跨项目、跨 agent 持久存在的状态层。
- 成熟 memory 系统至少分四层：规则记忆（CLAUDE.md / AGENTS.md）、常驻画像（MEMORY.md / USER.md）、历史召回（session search / daily notes / topic files）、反思与技能沉淀（dreaming / reflection / skills）。
- 记忆的核心价值不在"存得多"，而在分层治理：哪些常驻、哪些搜索、哪些归档、哪些变成可复用技能。
- 证据链与状态治理是 memory 的难点：必须记录来源、置信度、过期性、作用域和可删除性，否则记忆会从资产变成负债。
- Memory 会引入新的系统性风险：错误记忆永久化、过期信息持续影响决策、prompt injection 的持久化污染、隐私与删除的不可逆性。

## Core claims

Context window 解决"这一轮能装下多少"，RAG 是按需调用的外部资料库，而 Memory 解决"下一轮醒来时 agent 还记不记得上一次为什么要那样做"。三者分工清晰。

规则文件应只放"长期稳定、每次都该遵守"的东西，不能把历史细节全塞进去；团队级规则必须进入版本化文件，不能只依赖自动记忆。

常驻记忆每一轮都要付 token 税，应该短、硬、高密度，只保留身份、偏好和不变量。历史记忆应该可搜索、可追溯、可局部读取，而不是全部常驻上下文。

真正的 memory 系统不是"向量库里存对话"。向量库只是召回手段，完整的 memory 要处理状态、来源、权限和演化。

## Notable quotes

> "Memory 解决的是另一个问题：下一轮醒来的时候，agent 还记不记得上一次为什么要那样做。"

> "Memory 的核心价值不在'存得多'，而在把过去的东西分层：哪些该常驻，哪些该搜索，哪些该归档，哪些该变成以后可复用的技能。"

> "常驻 memory 应该短、硬、高密度。历史不应该常驻，只有压缩后的身份、偏好和不变量才值得常驻。"

> "Agent memory 同时也是治理系统。它要管理来源、置信度、过期性、权限和可删除性。"

> "Agent memory 的终局不是'记住更多'，而是少犯同样的错，更快复用做对过的事。"

> "长上下文让 agent 在当前任务里看得更全，Memory 则让 agent 在下一次任务里起点更高。"

## 四层架构对照

| 层级 | 代表实现 | 适合存放 | 设计原则 |
|---|---|---|---|
| 规则记忆 | CLAUDE.md / AGENTS.md | 构建方式、代码风格、业务红线、目录禁区 | 必须遵守的规则进入版本化文件 |
| 常驻画像 | MEMORY.md / USER.md | 身份、偏好、不变量 | 短、硬、高密度，只放下一轮必然有用的东西 |
| 历史召回 | session search / daily notes / topic files | 完整会话、bug postmortem、实验过程 | 可搜索、可追溯、可局部读取 |
| 反思与技能沉淀 | dreaming / reflection / skills | 重复成功路径、策略结论、流程沉淀 | 把历史经验转成未来默认能力 |

## Memory 的新问题

- **错误记忆永久化**：一次误判被写进 memory 后，agent 会更自信地重复它。
- **过期信息继续影响决策**：API 限制、部署拓扑等状态变化后，旧 snapshot 仍左右判断。
- **Prompt injection 的持久化污染**：一次被污染的经验保存后，后续所有 session 都会中招。
- **隐私和删除的不可逆性**：从对话抽取的 profile、facts、skills 不会因聊天记录删除而消失。
- **Summary 把证据变成二手结论**：难以区分"真实发生过的事实"和"模型当时的解释"。

## EverOS 的工程取向

文章以 [EverOS](https://github.com/EverMind-AI/EverOS) 作为该四层架构的落地参考：

- Markdown as source of truth：可读、可改、可 grep、可 Git 版本化。
- SQLite + LanceDB：Markdown 为真源，SQLite 管状态，LanceDB 管向量/BM25/标量过滤。
- Dual-track memory：user memory 与 agent memory 分离，episodes/profile 与 cases/skills 不混。
- Multimodal ingestion：文本、图片、音频、PDF、HTML、email 统一入层。
- Self-evolution：真实使用中的 cases 沉淀为 skills。
- Orthogonal retrieval：按 user_id / agent_id / app_id / project_id / session_id 多维度检索。

## Concepts introduced / referenced

- [[Agent Memory]] — 跨会话持久状态层，本 wiki 的核心概念页
- [[Agent Memory Architecture]] — 记忆系统的技术架构子页面
- [[Agent Runtime]] — Memory 是 Runtime 的关键能力缺口
- [[Claude Code Dynamic Workflows Practical Guide|Claude Code]] — CLAUDE.md / auto memory 的实践来源
- [[NanoClaw]] — Mnemon 图谱记忆 + Ollama 嵌入的本地实现
- [[Nous Research]] — Hermes Agent 的常驻画像与自我进化设计
- [[Context Engineering]] — 与长上下文、RAG 的分工关系
- [[Self-Evolving Memory]] — Agent Memory 子页面：自我进化型记忆
- [[Forgetting & Compaction]] — Agent Memory 子页面：遗忘机制与压缩策略
