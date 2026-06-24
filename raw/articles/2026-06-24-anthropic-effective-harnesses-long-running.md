---
title: "Effective harnesses for long-running agents \\ Anthropic"
source: "url"
source_file: "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
created: "2026-06-24T00:00:00Z"
source_url: "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
extract_method: "anysearch-extract"
author: "Anthropic Engineering"
published: "2025-11-26"
---

# Effective harnesses for long-running agents

Anthropic 第一方 harness 文章。明确把 Claude Agent SDK 称为 "agent harness"，给出跨多 context window 的长程 agent harness 设计。

## 核心问题：跨 context window 的一致性

> "The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before."

比喻：换班工程师，每个新工程师对上一班无记忆。context window 有限 + 复杂项目无法单窗口完成 → 需要桥接 session 的机制。

> compaction（上下文压缩）不足以解决——即使 Opus 4.5 在 Claude Agent SDK 上跨多窗口循环，仅给高层 prompt 也无法产出生产级 web app。

## 两种失效模式

1. **One-shot 倾向**：agent 试图一次做太多，context 耗尽留下半成品、未文档化的功能；下一 session 要猜、花时间恢复
2. **提前宣布完成**：后期 agent 环顾看到有进度，就宣称任务完成

## 两部分方案

1. **Initializer agent**（首 session）：建 `init.sh`、`claude-progress.txt`（日志）、初始 git commit
2. **Coding agent**（后续 session）：做增量进度，留下结构化更新

关键洞察：agent 用 `claude-progress.txt` + git history 快速理解工作状态——来自"高效软件工程师每天做什么"的启发。

### Feature list（deterministic feedback 实例）

initializer 写全面 feature 需求文件（claude.ai clone 超 200 features），初始全标 `passes: false`，给后续 agent 清晰的完整功能轮廓。

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": ["Navigate to main interface", "Click the 'New Chat' button", ...],
  "passes": false
}
```

coding agent 只能改 `passes` 字段，**强指令禁止删除/编辑测试**。用 JSON 而非 Markdown——模型更不易不当修改/覆盖 JSON。

### Incremental progress + clean state

一次只做一个 feature。要求每次留下 **clean state**（可 merge 到 main：无大 bug、有序、文档齐全）：
- commit 到 git + 描述性 commit message
- progress file 写摘要
- 用 git 回退坏改动、恢复可用状态

### Testing（deterministic feedback sensor）

agent 倾向不做端到端测试就标记完成。**显式 prompt 用浏览器自动化工具（Puppeteer MCP）像人类用户一样测试** → 大幅改善（能发现代码看不出的 bug）。

## Getting up to speed（每 session 起手式）

1. `pwd` 看目录
2. 读 git logs + progress files
3. 读 feature list，选最高优先级未完成项

## 与 Harness Cybernetics 的印证

| Anthropic 实践 | 控制论位置 |
|---|---|
| feature_list.json 的 feature 清单 | Feedforward（约束做什么） |
| `passes` 字段 + 禁止编辑测试 | Feedback（deterministic sensor） |
| git 回退坏改动 | Feedback（自纠正） |
| Puppeteer MCP 端到端测试 | Feedback（deterministic sensor，不可幻觉） |
| init.sh + 起手式 | Feedforward（环境设定） |
| clean state 要求 | Feedback 的质量门 |

Anthropic 的整个方案就是 feedforward（initializer 设环境+feature 清单）+ feedback（passes 字段、git 回退、Puppeteer 测试）的控制论组合。**第一方实证 Böckeler 框架。**
