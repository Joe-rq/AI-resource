---
title: Cline
type: entity
created: 2026-06-15
updated: 2026-06-15
sources:
  - "https://docs.cline.bot/cline-overview"
  - "https://cline.bot/blog/introducing-cline-sdk-the-upgraded-agent-runtime"
tags: [coding-agent, vscode-extension, agent-runtime, benchmark, open-source]
---

# Cline

## Overview

Cline is an open-source AI coding agent that lives in the editor and terminal. It reads and writes files, runs terminal commands, uses a browser, and builds features through natural conversation -- every action requires explicit human approval. Originally a VS Code extension, Cline has evolved into a multi-surface platform spanning CLI, Kanban (web-based parallel agent task board), JetBrains plugin, and a standalone SDK (`@cline/sdk`). It supports 30+ LLM providers and is used by over 7 million developers.

Cline's thesis: AI is not the security risk -- poor architectural boundaries are. It runs locally, abstracts providers behind a clean interface, and defaults to human-in-the-loop, making it viable in regulated environments where SaaS-based coding tools are blocked.

## Architecture

Cline 2.0 is a layered TypeScript stack where each layer has a single responsibility and depends only on the layer beneath it. The core is `@cline/sdk`, a pluggable agent runtime that handles the full agent loop: LLM calls, tool orchestration, session persistence, multi-agent coordination, and scheduling. Applications (VS Code, JetBrains, CLI, Kanban) are products built on top of this shared runtime, not monoliths with embedded agent logic.

### Agent Loop

The agent loop is stateless and reusable, orchestrating tool calls, context assembly, and model response processing. Key features include Plan & Act mode (separating information-gathering from action-taking phases), checkpointing, subagents with independent models/tools/prompts, and native agent teams without a separate orchestration layer.

### Provider Abstraction (`@cline/llms`)

Provider logic lives in `@cline/llms`, isolating model catalogs, provider settings, and handler behavior from the agent loop. This layer abstracts all model-specific differences -- token counting, tool call format, streaming behavior -- enabling cross-model runtime reuse. Supported providers include Anthropic, OpenAI, Google, AWS Bedrock, Mistral, LiteLLM, and OpenAI-compatible endpoints. Adding a provider requires implementing an `ApiHandler` and registering it.

### Tool System

Cline exposes file read/write, terminal commands, browser automation, web search, MCP connectors, and CRON jobs. Plugins register custom tools, observe lifecycle events, add rules/commands, and shape agent context without forking the runtime.

## Key Differentiators (vs Claude Code)

| Dimension | Cline | Claude Code |
|-----------|-------|-------------|
| License | Open source (Apache 2.0) | Proprietary |
| Model choice | 30+ providers, BYOK | Anthropic models only |
| Deployment | Local, no cloud dependency | API-based |
| Human-in-the-loop | Default, explicit approval per action | Configurable permission system |
| Multi-surface | VS Code, JetBrains, CLI, Kanban, SDK | CLI + VS Code extension |
| Extensibility | Plugins, MCP, custom tools, hooks, skills | Hooks, MCP, custom slash commands |
| Security posture | Zero external indexing, on-prem inference | Deny-first permission system |

Cline's open-source codebase means security teams can audit directly. Its BYOK model gives enterprises full control over inference location.

## Benchmark Data

On terminal-bench 2.0 (pass@1), Cline CLI achieves **74.2%** with claude-opus-4.7, compared to Claude Code's **69.4%** on the same model -- a 4.8 percentage point gap attributable entirely to runtime differences, since the underlying model is identical.

Cline's hill climbing experiment demonstrates the magnitude of runtime optimization: with claude-opus-4.5, Cline improved from **47% to 57%** (+10pp) purely through harness improvements -- rewriting system prompts, simplifying the agent loop, tightening context management, improving feedback loops and error handling, and rethinking how tools are defined and surfaced to the model. No model retraining, no new tools, no architecture changes.

This data is a primary empirical foundation for the [[Agent Runtime]] concept: the harness matters more than the model, and runtime engineering alone can deliver double-digit percentage point gains.

## Related Concepts

- [[Agent Runtime]] -- Cline's benchmark data (74.2% vs 69.4%, +10pp hill climbing) is the key empirical evidence for the "harness > model" thesis
- [[Dive into Claude Code（论文）]] -- complementary analysis of Claude Code's architecture; together with Cline's SDK blog post, forms a comparative view of two major agent runtime designs
- [[Claude Code Subagent]] -- Cline's subagent/agent-teams feature provides a comparable multi-agent primitive
- [[Thin Harness, Fat Skills]] -- Cline's plugin and skills extension model exemplifies the thin-harness philosophy

## Sources

- Cline official documentation: https://docs.cline.bot/cline-overview
- "Introducing Cline SDK: the upgraded agent runtime" (Cline Blog, 2026-05-13): https://cline.bot/blog/introducing-cline-sdk-the-upgraded-agent-runtime
- "The architecture that gets AI coding tools approved" (Cline Blog, 2026-01-27): https://cline.bot/blog/the-architecture-that-gets-ai-coding-tools-approved
- Cline GitHub: https://github.com/cline/cline
- Cline benchmark data cited in [[Agent Runtime]] and [[08 - Agent Runtime 主战场]]
