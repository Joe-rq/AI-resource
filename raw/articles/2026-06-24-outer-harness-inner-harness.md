---
title: "The Outer Harness: Why the Real Work in AI Coding Agents Isn't the LLM \\ codeongrass"
source: "url"
source_file: "https://codeongrass.com/blog/outer-harness-real-work-ai-coding-agents/"
created: "2026-06-24T00:00:00Z"
source_url: "https://codeongrass.com/blog/outer-harness-real-work-ai-coding-agents/"
extract_method: "anysearch-extract"
---

# The Outer Harness: Why the Real Work in AI Coding Agents Isn't the LLM

codeongrass.com。提出 inner harness vs outer harness 区分，论证 outer harness 是价值累积处。

## 核心论点

> "The agent you're running is not the interesting engineering problem. The control plane you build around it is."

> "The inner harness (Claude Code, Codex, Open Code) is commoditizing fast. The outer harness — session persistence, feedforward controls, feedback controls, multi-surface dispatch — is where the durable engineering value accumulates."

## Inner Harness vs Outer Harness

- **Inner harness** — agent runtime 本身：LLM + tool execution loop + SDK。Claude Code、Codex、Open Code 都是 inner harness。共享架构：read context → plan → select/execute tools → stream output。结构模式快速收敛趋同。
- **Outer harness** — 围绕 agent 建的控制面：inner harness 默认不带的一切。

> "The agent layer runs code. It doesn't manage sessions, surface permission requests to humans, persist state across sleep cycles, or dispatch work across surfaces. Those problems live above it."

## Outer harness 四组件

1. **Session persistence** — laptop 睡眠/断网时保持 agent alive 且可恢复
2. **Feedforward controls** — 执行前注入的约束，塑造 agent 被允许尝试什么
3. **Feedback controls** — 执行后/中的观察与信号浮现
4. **Multi-surface dispatch** — 不同 surface 访问同一 agent session，无需重建 workflow

## Feedforward vs Feedback controls（定义）

**Feedforward controls** — shape agent behavior **before** it acts。CLAUDE.md、限定目录的 system prompt、tool allowlist/blocklist、plan-vs-build 模式选择、context injection（repo state/recent diffs/task constraints）都是 feedforward。注入到 agent context，约束 action space。

> "Most teams underinvest in feedforward constraints and then spend engineering time on feedback controls trying to catch what the agent does wrong — when the cleaner fix is bounding what it's allowed to attempt."

**Feedback controls** — observe and respond **after** it acts。通知、状态监控、approval gates、audit logs。不阻止动作——观察执行、浮现信号、让人在 run 中/后介入。

### Deterministic feedback（关键子类型）

> "deterministic feedback — output that comes directly from tool execution rather than LLM interpretation. A bash exit code. A file diff. A test runner pass/fail. These are the most reliable signals in any outer harness because they can't be hallucinated."

完整 outer harness 栈：feedforward 约束 action space → 执行 → deterministic feedback 验证实际发生 → LLM-synthesized feedback 浮现状态给人/自动消费者。

## Convergent independent discovery（抽象真实性的证据）

四个独立开发者同一周在没有共享词汇的情况下各自交付了 outer harness 原语（SSH 进程监督、浏览器/移动 dashboard、tmux 通知/审批插件、持久身份多 agent 框架）→ 抽象被独立发现 = 它是真实的。

> "Agents decide, the control plane governs. They are separate concerns that require separate engineering investment."

## 与本 wiki 的关联

- inner/outer 区分解释 [[12-Factor Agents]] 的"own your X"系列为何重要——own 的就是 outer harness
- deterministic feedback 不可幻觉 → 对冲 [[Agent Reliability vs Capability]] 的 non-determinism
- session persistence ≈ [[Stateless Reducer]] 的可恢复性
- feedforward controls 收纳 [[Quarantine Mode]]、tool allowlist、system prompt 约束
- approval gates = [[Agentic Code Review]] 的 human-on-the-loop
