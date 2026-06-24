---
title: nashsu LLM Wiki
type: entity
created: 2026-06-24
updated: 2026-06-24
sources:
  - "https://github.com/nashsu/llm_wiki"
  - "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
tags: [llm-wiki, karpathy-pattern, knowledge-base, tauri, knowledge-graph, desktop-app, obsidian, mcp]
---

# nashsu LLM Wiki

## Overview

**nashsu/llm_wiki** 是 [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的**产品化桌面应用实现**——一个 Tauri v2（Rust 后端 + React 前端）跨平台应用，把"LLM 增量构建并维护持久 wiki"这个抽象 pattern 做成了带 UI、知识图谱、MCP server 和 Chrome 扩展的完整产品。口号："A personal knowledge base that builds itself."

核心反 RAG 立场与 Karpathy 原文一致：传统 RAG 每次查询重新检索、知识不积累；LLM Wiki 让 LLM 把源**编译进持久 wiki**，知识编译一次、持续更新，而非每次重算。

## 与 Karpathy 原始 pattern 的关系

nashsu 在 README 明确区分了"What We Kept"与"What We Changed & Added"。

**忠实保留**：三层架构（raw 不可变源 / wiki LLM 生成 / schema 规则）、Ingest/Query/Lint 三操作、`index.md` 导航、`log.md` 时间线、wikilink 交叉引用、YAML frontmatter、Obsidian 兼容、"human curates, LLM maintains" 角色分工。

**18 项增强**（从 CLI 抽象文档 → 全栈桌面应用），其中对本 wiki 最有参考价值的是：

| 增强 | 机制 | 对本项目的参考价值 |
|------|------|---------------------|
| **purpose.md** | schema（怎么运作）之外，独加 purpose（为什么存在：目标/关键问题/研究范围/演化论点），LLM 每次 ingest/query 都读 | **结构性缺口**——本 wiki 的 CLAUDE.md 全是 schema，从没显式写过"为什么" |
| **4-signal 知识图谱** | 直接链接 ×3.0 + 源重叠 ×4.0 + Adamic-Adar ×1.5 + 类型亲和 ×1.0；sigma.js + graphology + ForceAtlas2 可视化 | 本 wiki 80+ 页密集 wikilink 只是文本，无图谱计算层 |
| **Louvain 社区检测** | 自动发现知识簇 + 内聚度评分（<0.15 标记稀疏簇）| 呼应 [[Agent Memory]] 图谱记忆思想 |
| **Graph Insights** | 孤立页（degree≤1）/ 桥节点（连 3+ 簇）/ 稀疏社区 自动浮现 + 一键 Deep Research | 本 wiki 的 lint 只查 dead link，无图谱结构洞察 |
| **两步 CoT ingest** | 先分析（结构化分析）→ 后生成（基于分析建页），两次 LLM 调用提升质量 | 本 wiki 的 ingest 是单流程；呼应 [[Worker Verifier 对抗循环]] 分析-生成分离 |
| **Review 系统** | LLM ingest 时标记需人工判断项 + 预生成搜索查询 + 预定义动作（防幻觉）| 呼应 [[Agentic Code Review]] human-on-the-loop |
| **lint 从 gap 自动生成页面** | 检测到缺失页面 → 自动创建（commit `3d66f76`）| 呼应 [[Agent Harness 治理协议]] 自动扩张任务图 |
| **MCP server + HTTP API** | 本地 `127.0.0.1:19828` 把 wiki 操作暴露给任意 agent（Claude Code/Codex）| 本 wiki 靠 Claude Code skill 绑定；MCP 化是跨客户端的路 |
| **级联删除** | 删源 → 3-method 匹配相关页 + 清理 wikilink + 保留共享实体 | 本 wiki 删页靠手工 grep 清理入链 |

## 与本项目的关系：同一 pattern 的两种实现

本 wiki（AI-resource）与 nashsu/llm_wiki 是 **Karpathy pattern 的两条分叉**，不是谁参考谁：

| 维度 | nashsu（重产品）| 本 wiki（轻脚本 + 重治理）|
|------|------------------|------------------------------|
| 形态 | Tauri 全栈应用 | 纯 markdown + Claude Code skill + 脚本 |
| 操作 | Ingest/Query/Lint + Review/DeepResearch | 五操作（+compile/audit）|
| 质量保证 | 应用内 Lint+Review 双系统（Zustand）| 8 个 lint 脚本 + Ashby 覆盖矩阵 + hook |
| 可回滚 | file-sync（无事务回滚）| [[Stateless Reducer]] 式 ingest checkpoint（git tag + 事件流）|
| 治理哲学 | 无（工程堆叠）| [[Harness Cybernetics]] / Ashby / Reducer 框架 |
| 跨客户端 | MCP server + HTTP API | Claude Code skill 绑定 |
| 可移植性 | 应用绑定 | 纯 git markdown，可 diff/可移植 |

**正交取舍**：nashsu 强在体验/图谱洞察/多格式，弱在不可移植、无元治理；本 wiki 强在 git 可移植/agent 原生/治理深度，弱在无 UI/无图谱计算。

**反向参考**：nashsu 能借鉴本 wiki 的治理框架——它是 18 项功能堆叠，但没有"为什么这样组织质量保证"的元层（Ashby 矩阵让覆盖盲区可见、reducer 让 ingest 可回滚、hook 让规则自动执行）。

## 关键判断：nashsu 是本 wiki 研究概念的工程实证

nashsu 的功能并非凭空堆砌，而是**印证了本 wiki 已研究的概念**——Review=human-on-the-loop、两步 ingest=分析-生成分离、知识图谱=图谱记忆、lint 自动建页=自动扩张任务图。参考价值不止"功能多"，而是"本 wiki 研究的概念被产品化实证了"，双向印证。

## Related Concepts

- [[Agent Memory]] — nashsu 的 4-signal 知识图谱 + Louvain 社区检测是图谱记忆思想的产品化
- [[Worker Verifier 对抗循环]] — 两步 CoT ingest（先分析后生成）是分析-生成分离的实例
- [[Agentic Code Review]] — Review 系统（LLM 标记 + 预定义动作 + 人工判断）是 human-on-the-loop
- [[Agent Harness 治理协议]] — lint 从 gap 自动生成页面 = 自动扩张任务图
- [[Harness Cybernetics]] — 本 wiki 用 Ashby 框架组织质量保证，是 nashsu 缺失的元治理层

## Sources

- GitHub: https://github.com/nashsu/llm_wiki
- Karpathy 原始 pattern: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 配套 agent skill: https://github.com/nashsu/llm_wiki_skill
