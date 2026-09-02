---
title: "Steering Claude Code: Seven Instruction Mechanisms"
type: summary
created: 2026-09-02
updated: 2026-09-02
sources: ["raw/articles/45-steering-claude-code-instruction-mechanisms.md"]
tags: [claude-code, steering, claude-md, rules, skills, subagents, hooks, output-styles, guardrail, path-scoping, compaction, anthropic]
---

# Steering Claude Code: Seven Instruction Mechanisms

> 原始来源：[claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)（作者 Michael Segner）
> 发布日期：2026-06-18 · 摄取日期：2026-09-02
> 机制反哺 [[Claude Code Skills]]、[[Claude Code Subagent]]、[[Thin Harness, Fat Skills]]；guardrail 论点验证本项目 hooks 分层设计。

## 摘要

Anthropic 官方对 Claude Code **七种指令机制**给出统一选型框架。每种机制在三根轴上取不同的点：**何时加载进 context**、**是否在 compaction 中存活**、**指令权威性（instruction-following weight）多大**。这本质上是 Anthropic 自己的 context engineering 分类学——前馈 Guides（[[Harness Cybernetics]]）的官方选型手册。

## 七机制速查表

| 机制 | 加载时机 | Compaction 行为 | Context 成本 | 适用 |
|------|----------|-----------------|--------------|------|
| CLAUDE.md（根） | session start，全程常驻 | memoized，压缩后重读 | 高（每行恒付 token） | 构建命令、目录结构、团队规范 |
| CLAUDE.md（子目录） | Claude 读到该目录下文件时 | 直到再次触碰该目录 | 低 | 子目录特有约定 |
| Rules（`.claude/rules/`） | session start 或 path-scoped 触发 | 压缩后重注入 | 中（无 scope 即恒付） | 横切约束（`paths:` frontmatter 限定 `src/api/**` 等） |
| Skills | name+description 先行，body 按调用加载 | 已调用 skills 按共享预算重注入，**最旧先丢** | 低 | 程序性流程（部署/发布清单） |
| Subagents | name+description+tool list 先行，body 调用时才载 | **只有 final message 回到主会话** | 低（独立 context window） | 并行/隔离型副任务 |
| Hooks | 生命周期事件触发 | **完全绕过 compaction** | 低（配置在 context 之外） | 确定性自动化（lint、Slack、block 命令） |
| Output styles | session start，注入 system prompt | 永不压缩 | 高，且**覆盖默认 system prompt** | 显著角色变更 |
| append-system-prompt | CLI flag，仅本次调用 | 永不压缩 | 中（缓存后降低） | 格式/风格补充 |

## 三条关键迁移规则（官方判据）

1. **"every time X, do Y" → hook**。模型"选择"跑 formatter ≠ formatter 自动跑。要可靠就用 `settings.json` hook。
2. **"never do X" → 确定性强制，禁止用指令**。模型在长 session、模糊情境或 prompt injection 下会失守；真 guardrail 必须确定性——`PreToolUse` hook 检查调用后 exit 2 阻断；组织级唯一手段是 admin 部署、用户本地配置**无法覆盖**的 **managed settings**。（直接验证本项目 "PreToolUse 是唯一能说 no 的地方" 设计原则）
3. **30 行以上程序 → skill；API 专属规则 → `paths:` scope**。无 scope 的 rule 与塞进 CLAUDE.md 机械等价——恒加载、恒付费。

## 其他要点

- CLAUDE.md **<200 行、指定 owner、像代码一样 review**；monorepo 按团队拆子目录 CLAUDE.md；组织级合规用 MDM 集中下发。
- **Subagent 可嵌套 5 层**；dynamic workflows 可编排数十至数百后台 agent——编排计划与中间结果存于 script 变量而非主 context，规模不损指令保真。
- Subagent vs skill 的分界：**要隔离要摘要 → subagent；要看过程要可干预 → skill**。
- Output style 有**最高指令权重**但会整体替换默认 system prompt（除非 `keep-coding-instructions: true`），优先用内置 Proactive/Explanatory/Learning。
