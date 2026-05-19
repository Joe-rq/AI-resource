# AI Resource Wiki Knowledge Base

> Schema document — read at the start of every session together with `wiki/index.md`.
> Update after every major compile, ingest batch, or structural change.

## Scope

What this wiki covers:
- **Agent 平台与基础设施层** — Runtime / Multi-agent / Harness / 工具定义
- **Claude Code Skill 开发** — Skill 编写流程、SKILL.md 规范
- **多 Agent 协作架构** — Orchestrator/Specialist、Worker/Verifier 对抗循环、Team Engine
- **行业研究** — MiniMax、Anthropic、Cline、OpenAI 等公司的 Agent 平台实践

What this wiki deliberately excludes:
- 模型训练/微调细节
- 与 Agent 平台无关的纯应用层话题

## Operations

This wiki follows the llm-wiki skill's five operations: `compile`, `ingest`, `query`, `lint`, `audit`.
Every operation appends an entry to `log/YYYYMMDD.md`.

## Naming conventions

### Pages
- **Concept pages** (`wiki/concepts/`): Title Case noun phrases. E.g., "Agent Runtime", "Multi-Agent Architecture".
- **Folder-split concepts** (`wiki/concepts/<topic>/`): used when a topic would exceed ~1200 words as a single page. Contains `index.md` + one file per aspect.
- **Entity pages** (`wiki/entities/`): Proper names. E.g., "MiniMax Mavis", "Claude Code", "Cline".
- **Summary pages** (`wiki/summaries/`): kebab-case source slug. E.g., "08-agent-runtime-battlefield".

### Wikilinks
- Always use `[[Page Title]]` — exact page title, case-sensitive.
- For folder-split pages, link to the index: `[[concepts/Foo/index|Foo]]`.
- Link the first mention of every entity or concept. Do not link the same page more than twice per article.

### Frontmatter
Every wiki page has YAML frontmatter:
```yaml
---
title: <Page Title>
type: concept | entity | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [list of raw/ slugs this page draws from]
tags: [relevant tags]
---
```

### Diagrams and formulas
- All diagrams are **mermaid**. No ASCII art.
- All formulas are **KaTeX** (inline `$...$` or block `$$...$$`).

### Raw file policy
- Small text sources → copy into `raw/<subfolder>/`.
- Large binaries → create a pointer file at `raw/refs/<slug>.md` with `kind: ref` frontmatter and an `external_path` field. Do not copy the binary.

## Current articles

### Concepts
*(none yet — run compile after ingest)*

### Entities
*(none yet)*

### Summaries
*(none yet)*

## Open research questions

- Agent Runtime 的具体实现差异（Prompt 设计/工具定义/上下文管理/错误处理）具体怎么影响性能？
- Worker/Verifier 对抗循环的收敛条件是什么？何时终止对抗？
- Claude Code Agent Teams 和 Anthropic Managed Agents 的架构有何本质区别？

## Research gaps

Sources to ingest:
- [ ] Anthropic Claude Cowork 官方文档
- [ ] Cline SDK 技术博客原文
- [ ] LangChain Deep Agents benchmark 原始数据

## Audit backlog

*(none — run `python3 scripts/audit_review.py <wiki-root> --open` to refresh)*

## Notes for the LLM

- Language: **bilingual** (中英文混合)
- Tone: neutral, technical, research-focused
- Depth: deep technical analysis with practical implications
- Handling contradictions: state both positions, cite sources, add to Open Research Questions