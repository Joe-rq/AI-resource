---
title: "Building Verification Loops in Claude Code"
type: summary
created: 2026-09-04
updated: 2026-09-04
sources: ["raw/articles/47-building-verification-loops-claude-code.md"]
tags: [verification-loop, agentic-loop, skills, skill-chaining, grader-agent, code-review, spec-validation, rubric, feedback-loop, claude-code, anthropic]
---

# Building Verification Loops in Claude Code

> 原始来源：[claude.com/blog/building-verification-loops-in-claude-code-with-skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)（作者 Delba de Oliveira，Claude Code 团队）
> 发布日期：2026-07-22 · 摄取日期：2026-09-04
> 机制反哺 [[Worker Verifier 对抗循环]]（grader agent 产品实现）、[[Harness Cybernetics]]（反馈 Sensors 官方框架）、[[Claude Code Loops]]、[[Agentic Code Review]]。

## 摘要

Anthropic 官方将 agentic loop 形式化为三阶段循环——**收集上下文 → 执行动作 → 验证结果**。**Verification loop = Claude 检查并尝试修复自己工作的迭代过程**，可打包为 skill，让每个 session 自动跑同样的检查，替代"人肉记得检查"。判断公式：凡是 Claude 无法从 codebase 确定性信号（type checker/linter/test/运行时错误）推断出、需要你手动重复做的检查，都是验证 skill 的捕获对象——包括领域特定的确定性规则（"拒绝任何没有 backfill 步骤就 drop column 的 migration"，通用 linter 覆盖不了，写成 skill 后 agent 可自检）。

## 六种内置验证机制

1. **/verify skill** — 构建、运行、观察应用变更
2. **Toolchain 信号** — Claude 捕获任意工具的错误码/警告；最佳实践是把确切 build/test 命令写进 CLAUDE.md
3. **Code Review**（research preview）— 托管 multi-agent 评审服务，跑 PR 自动评审；`@claude` 评论 finding 即闭环
4. **GitHub Actions** — push/PR 触发同一套验证 skill
5. **Spec validation** — 对照仓库内 markdown spec 校验并修复违规
6. **Rubrics in Managed Agents (beta)** — 独立 grader agent 按 rubric 验证产出，**失败自动回流返工**——[[Worker Verifier 对抗循环]] 在产品层的实现

## 四种调用模式与选择判据

| 模式 | 触发 | 适用 | 升级信号/限制 |
|------|------|------|---------------|
| **Standalone** | 刻意调用 | 跨切面检查（pre-commit 安全扫描、可访问性审计） | 每次改动都跑 → 该 embed 或 chain |
| **Embedded** | 产出型 skill 自动附带 | 检查属于单一 workflow | 只能改自己可控的 SKILL.md；内置/插件 skill 禁改 → 用 chain |
| **Chained** | 一个 skill 结束时调用下一个 | 端到端流水线；给不可改 skill 加验证的 wrapper 模式 | 牺牲灵活性换自动化；**增加 token 消耗，广泛部署前先测试** |
| **On every PR** | CI 触发 | 把个人基础设施变成团队基础设施 | 链条还在变动的阶段不要上 PR 级（每次调整都是团队可见事件） |

**Anthropic 团队内部实例**：`/code-review`（找 bug）→ `/simplify`（清理 diff）→ `/verify`（确认端到端行为）→ 自定义 `/design`（对照 DESIGN.md 校验 UI）。习惯（"我总是跑完 X 再跑 Y"）升格为契约（"X 结束时自动跑 Y"）。

## 对 wiki 现有论述的意义

- 六种内置机制是 [[Harness Cybernetics]] 反馈 Sensors 的官方清单；grader agent 回流返工把反馈闭环产品化
- chaining 的 token 警告是 [[Agentic Code Review]] 评审经济学与 [[Multi-Model Ensemble]] 增益扣算力研究问题的一手官方佐证
- 验证检查写成 skill = "反馈检查可编码化为 sensor" 论点的官方实践（呼应本项目 hooks/CI 双层验证）
