---
title: "Claude Code Dynamic Workflows 实践指南"
type: concept
created: 2026-06-11
updated: 2026-06-16
sources: ["raw/articles/2026-06-04-claude-code-dynamic-workflows.md"]
tags: [claude-code, workflows, ultracode, deep-research, practical-guide, best-practices]
---

# Claude Code Dynamic Workflows 实践指南

> 基于 Claude Code 官方文档和社区实践的**使用场景、决策树与操作速查**。与 [[Claude Code 动态工作流（Dynamic Workflows）]] 和 [[A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读]] 互补：那两篇讲"是什么"和"为什么"，这篇讲"什么时候用、用什么、怎么用"。

## 场景选择决策树

| 如果你的任务是... | 推荐命令 | 不推荐的情况 | 预估效果 |
|:---|:---|:---|:---|
| 调研类问题（技术选型、竞品分析） | `/deep-research` | 问题太简单或需要快速迭代探索 | ⭐⭐⭐⭐⭐ 交叉验证质量高 |
| 一次性大规模任务（审计、迁移） | `ultracode: <task>` | 单文件修改或小范围编辑 | ⭐⭐⭐⭐⭐ 远超单代理能力 |
| 会话内多个复杂任务 | `/effort ultracode` | 日常小修改、需要快速响应 | ⭐⭐⭐⭐☆ 自动但耗 token |
| 重复执行的流程 | 保存后 `/<name>` | 一次性任务 | ⭐⭐⭐⭐⭐ 可复用、可参数化 |
| 需要多视角评审的决策 | `ultracode:` + 对抗模式 | 明显简单的修改 | ⭐⭐⭐⭐⭐ 结论更可靠 |

## 命令详细对比

| 命令 | 类型 | 功能 | Claude 写脚本 | 可复用 | 接受参数 | 需要批准 | 成本级别 |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| `/deep-research <question>` | 内置捆绑 | 多角度网络搜索，交叉检查来源，投票过滤，返回引用报告 | ✅ 内置 | ✅ 随时可用 | ✅ 研究问题 | ✅ 首次 | 中高 |
| `ultracode: <task>` | 单次触发 | 提示中关键字触发，Claude 为当前任务编写并执行脚本 | ✅ 自动编写 | ❌ 单次 | ❌ 内嵌描述 | ✅ 首次 | 高（依任务） |
| `/effort ultracode` | 模式切换 | 启用自动工作流模式，所有实质性任务自动规划为工作流 | ✅ 自动编写 | ❌ 会话级 | ❌ | ✅ 每次 | 最高 |
| `/workflows` | 管理 | 列出运行中/已完成的工作流，查看进度、暂停/恢复/停止 | ❌ 仅管理 | ✅ 管理工具 | ❌ | ❌ | 无 |
| `/<name>` | 自定义 | 运行已保存的工作流脚本，支持自动补全 | ❌ 已保存 | ✅ 永久保存 | ✅ `args` 变量 | ✅ 首次 | 中（依脚本） |

## 效果出色的场景推荐

### 🚀 标杆案例：Bun 从 Zig 迁移到 Rust

- 约 **750,000 行** Rust 代码生成
- **99.8%** 测试套件通过
- 从首次提交到合并仅 **11 天**
- **数百个代理**并行工作

四个工作流阶段：生命周期映射 → 逐文件移植（双评审员）→ 构建修复循环 → 夜间优化提 PR。

### 推荐场景速查

| 场景 | 推荐触发方式 | 关键模式 | 最佳实践 |
|:---|:---|:---|:---|
| **代码库范围安全审计** | `ultracode:` / `/deep-research` | Fan-out + 对抗验证 | 先只读扫描确认问题，再分组按严重程度处理 |
| **大规模代码迁移** | `ultracode:` / `/effort ultracode` | Fan-out per callsite + worktree 隔离 + 对抗 review | 先在子目录试运行，确认模式后全量执行 |
| **测试覆盖率生成** | `ultracode:` / 保存的工作流 | Fan-out per module | 按模块拆分代理，最后汇总覆盖率报告 |
| **技术尽职调查 / 深度研究** | `/deep-research` | Fan-out web search + 对抗验证 + 引用合成 | 问题要足够复杂才值得用；简单问题用普通对话 |
| **复杂重构规划** | `ultracode:` 只读分析 | 多代理分别从架构、测试影响、API 兼容性、回滚风险角度评审 | 第一阶段只分析不修改，评审方案后再执行 |
| **多轮对抗性验证** | `ultracode:` / 保存的工作流 | 找问题 → 验证证据 → 尝试推翻 → 修复建议 | 适用于安全审计、事故复盘、性能瓶颈、重要 PR 风险检查 |
| **技术债务系统清理** | `/effort ultracode` / 保存的工作流 | Fan-out per directory | 保存为工作流后定期运行，保持代码库整洁 |
| **PR 批量审查** | 保存的工作流 + gh CLI | Fan-out per PR / per module | 与 `gh pr diff` 配合批量处理 |
| **深度验证（逐条溯源）** | `ultracode:` / 保存的工作流 | 提取声明 → 每条 spin off 验证 agent → 来源质量审查 | 适用于技术白皮书、事故复盘报告、合规文档 |
| **排序与锦标赛筛选** | `ultracode:` / 保存的工作流 | [[Tournament Mode]] / pairwise pipeline / bucket-rank merge | pairwise 比 absolute scoring 更可靠；避免 1000+ 行撑爆上下文 |
| **记忆与规则遵循** | `ultracode:` / 保存的工作流 | 每条规则配 verifier agent + skeptic 反向审查 | 也可反向挖掘：从会话历史提炼规则写回 `CLAUDE.md` |
| **大规模分类处理（Triage）** | 保存的工作流 + `/loop` | 分类 + 去重 + 行动 + **quarantine 模式** | 配合 `/loop` 可持续运行；quarantine 隔离读不可信内容的 agent |
| **探索与品味决策** | `ultracode:` / 保存的工作流 | Generate + rubric review，由 review agent 判定完成 | 适用于 CLI 命名、UI 设计、API 命名、Logo 比选 |
| **评估与智能路由** | 保存的工作流 / `ultracode:` | Worktree 隔离 + 对比 agent 按 rubric 打分 / Classifier 路由 Sonnet/Opus | 适用于 skill 质量评估、模型选型、任务复杂度预估 |

## 不适合使用工作流的场景

| 场景 | 原因 | 替代方案 |
|:---|:---|:---|
| 单文件修改 | 开销远大于收益 | 标准对话 |
| 交互式开发（结对编程、需求探索、原型迭代） | 工作流延迟太高，无法中途输入 | 标准对话 |
| 紧密耦合的变更 | 并行反而增加协调成本 | 大上下文窗口顺序处理 |
| 成本敏感的小任务 | token 消耗是单代理的 10-100 倍 | 标准对话 |
| 需要中途人工介入 | 工作流运行中无法输入，只能暂停或停止 | 拆分为多个独立工作流 |
| 常规编码任务 | 大多数传统编码不需要 5 人 reviewer panel | 标准对话，掂量是否真的需要额外算力 |

## 进阶技巧

### 结合 `/goal` 和 `/loop`

对可重复的工作流（分类、研究、验证），用 `/loop` 按固定间隔运行，用 `/goal` 设硬性完成要求：

```text
/goal 修复所有构建错误
/loop 每 5 分钟运行一次修复工作流，直到构建成功
```

### 设置 Token 预算

在提示中直接写明上限：

```text
ultracode: 审计 src/ 目录下的认证问题，token 预算 10000，超出时暂停并报告
```

### 通过 Skills 分发工作流

把 JavaScript 工作流文件放进 skill 文件夹，在 `SKILL.md` 中引用。提示 Claude 把工作流当成**模板**而非逐字照搬的脚本，留出灵活性。

### 分离思考与执行

先用工作流做**分析和规划**，审查方案后再启动**执行工作流**。类似真实的技术设计评审流程。

### 保持干净的 git 状态

每次工作流前提交当前代码，方便审查完整 diff。

### 搭配 Auto 权限模式

长时间无人值守运行时开启 Auto 模式，避免每次批准中断。

## 最佳实践总结

1. **先小范围试运行** — 一个目录而不是整个仓库，评估 token 消耗和效果后再扩大
2. **给足上下文** — 与其说"修复认证模块"，不如说"认证模块有三个已知问题：[列表]。下季度还要加 OAuth，请一并考虑"
3. **分离思考与执行** — 分析规划 → 审查 → 执行
4. **保持干净的 git 状态** — 工作流前提交代码
5. **定期保存工作流** — 完成后按 `s` 保存，变成可复用的团队资产
6. **搭配 Auto 权限模式** — 长时间无人值守时避免中断

## Related Concepts

- [[Agentic Laziness]] — 单 Agent 提前终止，三种结构性失效模式之一
- [[Self-Preferential Bias]] — 单 Agent 偏好自己的结果，三种结构性失效模式之一
- [[Goal Drift]] — 多轮 compaction 导致目标偏离，三种结构性失效模式之一
- [[Tournament Mode]] — pairwise 比较 vs absolute scoring，六种编排模式之一
- [[Quarantine Mode]] — 读不可信内容的 agent 与高权限 agent 的结构性隔离

## 与现有 wiki 概念的关联

- [[Claude Code 动态工作流（Dynamic Workflows）]] — 产品功能文档（"怎么用"的基础）
- [[A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读]] — 官方博客深度解读（"为什么"+ 六种模式 + 十个用例）
- [[Agentic Laziness]] — 单 Agent 在执行复杂多步骤任务时提前终止，三类结构性失效模式之一
- [[Goal Drift]] — 多轮 compaction 导致目标偏离，三类结构性失效模式之一
- [[Self-Preferential Bias]] — 单 Agent 偏好自己的结果，三类结构性失效模式之一
- [[Claude Code Subagent]] — 工作流编排的工作者原语
- [[Claude Code Skills]] — 工作流可通过 skill 分发
- [[Thin Harness, Fat Skills]] — "harness on the fly" 的极致推论
- [[Worker Verifier 对抗循环]] — 对抗验证模式的同构概念
- [[Agent Secure Runtime]] — Quarantine 模式的权限隔离延伸
- Tournament Mode — pairwise 比较 vs absolute scoring 的判断学说
- [[Quarantine Mode]] — 读不可信内容的 agent 与高权限 agent 的结构性隔离
