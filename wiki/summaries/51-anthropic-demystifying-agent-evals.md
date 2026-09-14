---
title: "Demystifying Evals for AI Agents（Anthropic Engineering）"
type: summary
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/articles/2026-01-09-anthropic-demystifying-evals-for-ai-agents.md"
tags: [agent-evals, eval-methodology, agent-harness, task-trial-grader, transcript, outcome, pass-at-k, coding-agents, conversational-agents, research-agents, computer-use, anthropic, swiss-cheese-model]
---

# Demystifying Evals for AI Agents（Anthropic Engineering）

> 原始来源：[anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（作者 Mikaela Grace、Jeremy Hadfield、Rodrigo Olivares、Jiri De Jonghe）
> 发布日期：2026-01-09 · 摄取日期：2026-09-14
> 论点反哺 [[Agent Evaluation Methodology]]（核心素材）、[[Harness Cybernetics]]、[[Worker Verifier 对抗循环]]、[[Building Verification Loops in Claude Code]]（验证机制官方版）、[[Agent Secure Runtime]]、[[Anthropic]] 产品矩阵（Claude Code、Claude for Chrome、alignment auditing agents）。

## 摘要

Anthropic 把 agent eval 视为**长生命周期的基础设施**：eval 不只是单次测试，而是**驱动开发循环 + 跨迭代保持质量 + 跨新模型快速迁移**的核心引擎。文章系统化**元方法论**（task/trial/grader/transcript/outcome/harness 等核心抽象 + 3 类 grader + 4 类 agent 范式 + pass@k/pass^k 非确定性度量 + 8 步 0→1 roadmap + 与其他方法的 swiss cheese model），是 agent eval 领域**最完整的官方框架**。

## 核心抽象（Anthropic 定义）

Anthropic 在文章中给出了**精确词汇表**，本 wiki 用 [[Agent Evaluation Methodology]] 全面继承：

```text
Task (a.k.a problem / test case)
  → Trial（单次 attempt；多次 trials = consistent results）
    → Grader（评分逻辑；可多个；每个含多个 assertion / check）
      → Transcript（a.k.a trace / trajectory；完整记录 = API messages array）
        → Outcome（终态，与 transcript 分离）
          → Evaluation Harness（基础设施：跑任务 / 录步骤 / 评分 / 聚合）
            → Agent Harness（a.k.a scaffold；model + harness 才是被评估的整体）
              → Evaluation Suite（共享大目标的任务集合）
```

**关键提醒**：当评估"agent"时，**评估的是 harness + model 的组合**——Claude Code 既是 product 又是 harness，Anthropic 通过 Agent SDK 复用 Claude Code 的核心 primitives 造了"长时运行 agent harness"（[effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）。

## 为什么必须建 eval？

| 阶段 | 没有 eval 的症状 |
|------|----------------|
| 早期 prototype | 手动测试 + dogfood + 直觉，"够了" |
| Production + scaling | 用户报告"agent 变差" → "瞎飞"模式 → 只能猜 → 真回归 vs 噪声无法区分 |
| 采用新模型 | 无 eval 的团队 = 数周测试；有 eval 的团队 = 数天 tune prompts + 升级 |

**Eval 的复合价值**：failures → test cases → regression tests；quality bar 维护；research 与 product 团队最高带宽沟通通道；token 成本 / 延迟 / cost-per-task / error rates 横向 baseline。

## Grader 三大类

| 类 | 方法 | 优势 | 弱点 |
|----|------|------|------|
| **Code-based** | string match (exact/regex/fuzzy) · binary test · 静态分析 · outcome verification · tool call verification · transcript analysis | fast / cheap / objective / reproducible / easy to debug | brittle / 缺 nuance / limited for subjective |
| **Model-based** | rubric-based scoring · NL assertions · pairwise comparison · reference-based · multi-judge consensus | flexible / scalable / handles open-ended / captures nuance | 非确定 / 贵 / 需 calibration with humans |
| **Human** | SME review · crowdsourced · spot-check · A/B · inter-annotator agreement | gold standard / matches expert / calibrates model grader | 贵 / 慢 / coverage 受限 / 一致性挑战 |

**每任务评分**三种组合：**weighted**（组合分数过阈值）/ **binary**（所有 grader 过）/ **hybrid**。

## Capability vs Regression（核心二分）

| 类型 | 问什么 | 起始通过率 | 目标 |
|------|-------|-----------|------|
| **Capability / quality** | "agent 能把什么做好？" | **低**（失败常态） | 给团队"可攀登的山" |
| **Regression** | "agent 还能处理以前能做的吗？" | **接近 100%** | 防止后退；分数下降 = 坏了 |

**生命周期**：launch 后，capability eval 高通过率后可"毕业"为 regression suite 持续跑——"Can we do this at all?" 过渡到 "Can we still do this reliably?"。

## 4 类 agent 评估范式

### Coding agents（最简单）

**核心评估方法**：well-specified tasks + stable test environment + 通过/失败测试。

**代表 benchmark**：
- **SWE-bench Verified**（GitHub issues + test suite；fix 失败测试且不破坏现有）——LLMs 一年内从 40% 进步到 >80%
- **Terminal-Bench**（端到端技术任务：从源码构建 Linux kernel、训练 ML 模型等）

**Coding eval YAML 模板**（节选）：

```yaml
task:
  id: "fix-auth-bypass_1"
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: state_check
      expect:
        security_logs: {event_type: "auth_blocked"}
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
  tracked_metrics:
    - type: transcript
      metrics: [n_turns, n_toolcalls, n_total_tokens]
    - type: latency
      metrics: [time_to_first_token, output_tokens_per_sec, time_to_last_token]
```

### Conversational agents（多维评估）

**核心挑战**：interaction quality 本身就是评估对象——**需第二个 LLM 模拟用户**。Anthropic 的 [alignment auditing agents](https://alignment.anthropic.com/2025/automated-auditing/) 正是这个模式——通过延长对抗对话压力测试模型。

**代表 benchmark**：𝜏-Bench → τ2-Bench（multi-turn 交互，retail support / airline booking；一个模型演用户，agent 演被测）。

**支持的多维度**：

```text
ticket resolved (state check)
finished in <10 turns (transcript constraint)
tone appropriate (LLM rubric)
```

### Research agents（质量相对性最强）

**核心难点**：expert 间分歧、ground truth 漂移、长 open-ended 输出空间。

**代表 benchmark**：**BrowseComp**（"needle in haystack"——easy to verify, hard to solve）。

**复合策略**：

```text
Groundedness check:  claims 是否被 sources 支持
Coverage check:      good answer 必须包含的关键事实
Source quality check: consulted sources 是否权威（而非"第一个检索到"）
Exact match:         "Q3 营收 = $X" 这种客观题
LLM judge:           flag unsupported + 检查 gaps + 评估 coherence
```

**关键**：LLM rubric 必须**频繁 calibrate against expert human judgment**。

### Computer use agents（GUI 交互）

**核心评估方法**：跑在真实或 sandbox 环境 → 检查 intended outcome。

**代表 benchmark**：
- **WebArena**（browser-based task；URL/page state check + backend state verification）
- **OSWorld**（full OS 控制；inspect 文件系统 / 应用配置 / 数据库 / UI 元素）

**Browser use 的效率 trade-off**（Claude for Chrome 内部发现）：

```text
DOM-based:   快 / token 重
Screenshot:   慢 / token 轻
Wikipedia 摘要 → DOM 提取
Amazon 找笔记本壳 → screenshot（DOM 太重）
```

## 非确定性度量：pass@k vs pass^k

| 度量 | 测什么 | 公式直觉 | 何时用 |
|------|------|---------|-------|
| **pass@k** | *k* 次内至少 1 次成功的概率 | "shots on goal" | coding 等"对一次就行"的场景；k=1 = 首次成功率 |
| **pass^k** | *k* 次全部成功的概率 | per-trial p^k；75% × 3 trial = 42% | 客户面向 agent 等"必须可靠"的场景 |

**两者都重要**——选哪个取决于产品要求。

## 8 步 Roadmap（0 → 1）

### Step 0–3：早期数据集搭建

| 步 | 关键动作 |
|-----|---------|
| **Step 0: Start early** | 不要等"几百个 task"——**20-50 个真实失败的简单 task = 良好起点**；早期 impact 大，小样本足够 |
| **Step 1: Start with what you already test manually** | release 前手动检查 + bug tracker + support queue → 转化为 test cases |
| **Step 2: Write unambiguous tasks with reference solutions** | **两个 domain expert 独立给出相同 pass/fail 判定** = 好 task；每个 task 应有 reference solution（已知 working output），证明 task 可解 + grader 配置正确 |
| **Step 3: Build balanced problem sets** | 单边 eval = 单边优化；class-imbalanced 警惕——Claude.ai 内部 web search eval 同时测"该搜的"（天气查询）和"不该搜的"（"Apple 谁创立"），反复 refine 才平衡 |

### Step 4–5：Harness + Grader 设计

| 步 | 关键动作 |
|-----|---------|
| **Step 4: Build a robust eval harness with stable environment** | 每次 trial = "isolated" 干净环境；共享 state（leftover files / cached data / resource exhaustion）会引入基础设施噪声；警告：agent 通过看 git history 获取不公平优势的 case 已观察到 |
| **Step 5: Design graders thoughtfully** | 推荐顺序：**deterministic > LLM > human**；避免"序列步骤检查"过于 rigid（agent 经常找合法但 eval 设计者没预料的路径）；多 component task 给 partial credit；LLM grader 必须 calibrate with humans；给 LLM "**Unknown**" 出口避免幻觉；per-dimension 独立 LLM judge 优于"一个 judge 评全部" |

**Eval 失真经典案例**：

- **Opus 4.5 在 CORE-Bench**：从 42% 修到 95%——**grading bug** 期望 "96.124991…" 但评分严格等于 "96.12" 的也算错、任务 spec 模糊、任务不可复现
- **METR time horizon benchmark**：misconfigured tasks 要求"超阈值"但模型按指令 optimize 到阈值就被罚分；Claude 因遵循指令被罚，"忽略目标的"模型拿更高分

→ **Make your graders resistant to bypasses**——task + grader 设计要让"通过"真正需要"解决问题"。

### Step 6–8：长期维护

| 步 | 关键动作 |
|-----|---------|
| **Step 6: Check the transcripts** | **失败是否"公平"**——是 agent 真错还是 grader 拒了合法解；不读 transcripts 就不知道 eval 在测什么 |
| **Step 7: Monitor for capability eval saturation** | 100% 通过 = regression only；SWE-Bench Verified 从 30% → >80% 接近饱和 → 后续 improvement 慢 + 大 capability 改善呈现小分提升。Qodo 案例：初被 Opus 4.5 打动不了 → 自建 agentic eval framework 才看清进步 |
| **Step 8: Keep eval suites healthy** | 专门 evals 团队管核心基础设施 + 领域专家 / product teams 贡献 task 并自跑；**对 AI 产品团队，owning + iterating evals 应像维护 unit tests 一样 routine** |

**Anthropic 的内部实践**：**eval-driven development**——capability eval 起始低通过率"暴露产品要求的具体程度"，新模型 release 后快速验证哪些"赌对了"。**"产品人 / CSM / sales 应能通过 Claude Code PR 贡献 eval task"——主动 enable**。

## 与其他方法的 Swiss Cheese Model

无单一方法能 catch 所有问题；多层组合：

| 方法 | 优势 | 弱点 |
|------|------|------|
| **Automated evals** | 快 / 完全可复现 / 无用户影响 / 每个 commit 可跑 / 大规模 | 前置投入 / 需随产品演进维护 / 可能 false confidence |
| **Production monitoring** | 揭示真实用户行为 / 抓合成 eval 漏的 / 真实性能 ground truth | 被动 / 用户先碰到问题 / 信号噪声 / 缺 ground truth |
| **A/B testing** | 真实用户 outcome / 控制混淆 / 可规模化系统化 | 慢 / 只测 deploy 了的 / 不能直接看"why" |
| **User feedback** | 暴露未预料问题 / 真实例子 / 关联产品目标 | 稀疏 / 偏严重问题 / 不解释 why |
| **Manual transcript review** | 培养 failure mode 直觉 / 抓 subtle / 校准"好"标准 | 时耗 / 不 scalable / 覆盖不一致 / reviewer fatigue |
| **Systematic human studies** | gold standard / 处理模糊任务 / 改进 model grader | 贵 / 慢 / 域专长要求 |

**生命周期映射**：

```text
Pre-launch / CI/CD:     Automated evals (首选 + 模型升级第一道防线)
Post-launch:            Production monitoring (drift 检测)
Significant changes:    A/B testing (足够流量后)
Ongoing:                User feedback + transcript review (sample weekly)
Subjective calibration: Systematic human studies (reserve)
```

## 附录：Eval frameworks

| 框架 | 定位 |
|------|------|
| **Harbor** | containerized agent 跑 + 大规模 trial 基础设施 + Terminal-Bench 2.0 标准格式 |
| **Braintrust** | offline eval + production observability + experiment tracking；autoevals library 含 factuality/relevance 等预置 scorer |
| **LangSmith** | tracing + offline/online eval + dataset 管理；LangChain 紧集成 |
| **Langfuse** | self-hosted 开源版（数据驻地要求场景） |
| **Arize Phoenix** | 开源 LLM tracing/debug/offline+online eval；AX 是 SaaS 扩展 |

**关键提醒**：框架只是加速器——**"frameworks are only as good as the eval tasks you run through them"**。快速选个 fit 的，把精力投入 task + grader 本身。

## 与本 Wiki 的关联

| Anthropic 论点 | 反哺 / 对照 Wiki 概念 |
|--------------|---------------------|
| **核心抽象（task/trial/grader/transcript/outcome/harness/suite）** | [[Agent Evaluation Methodology]] 的核心素材；与 [[Stateless Reducer]] 的"(state, event) → new state" 抽象同源（两者都把 agent 当 reducer） |
| **3 类 grader** | 与 [[Worker Verifier 对抗循环]] 的"对抗式 verifier"对照——Verifier 是 agent，Anthropic 的 LLM judge 是 grader，两者都是 model-based 评估 |
| **4 类 agent 范式** | 与 [[Agent Runtime]] 的"四种 agent 类型 benchmark 实证"（Cline 74.2% vs Claude Code 69.4%）互补——Anthropic 文章是元方法论，[[Agent Runtime]] 是定量对比 |
| **Capability vs Regression** | 与 [[Agent Reliability vs Capability]] 的"pass@k vs reliability decay"同源；与 [[Eval-Driven Development]]（Madhuguru）的"ladder 4 类"对应（regression ↔ regression eval, hill-climb ↔ capability eval） |
| **pass@k vs pass^k** | 与 [[Agent Reliability vs Capability]] 的"RDC（reliability decay curve）"正交——pass^k 是固定 k 的 reliability 切片，RDC 是 k → ∞ 的 reliability 极限 |
| **Opus 4.5 CORE-Bench 案例（42 → 95%）** | 与 [[Agent Evaluation Methodology]] "eval 失真经典案例" 段；与 [[Anthropic]] entity 页的产品演化叙事互证 |
| **Browser use DOM vs screenshot 效率** | 与 [[Agent Secure Runtime]] 的"sandbox 隔离 + 权限分级"对照——DOM extraction 是只读，screenshot 是模糊交互 |
| **Swiss cheese model** | 与 [[Harness Cybernetics]] 的"前馈 Guides + 反馈 Sensors 双层对偶"同源——swiss cheese 各层 = harness 各 Sensors |
| **"Eval-driven development = 默认"** | 与 [[Building Verification Loops in Claude Code]] 的"verification loop 三阶段"对应——Anthropic 内部口径一致 |
| **Transcript 不可读 = 不知 eval 在测什么** | 与 [[Trajectory Handoff]] 的"传 context window 不传 plan document"互补——两者都强调"trajectory 是评估的唯一证据" |
| **Eval task = spec stress test** | 与 [[Forward Deployed Engineering]] 的"deploy before spec final" 同向——eval task 比 product spec 更早暴露假设 |

## 关键洞察

1. **"评估 harness + model"而非"评估 model"**——这是 wiki [[Agent Runtime]] 98.4% 基础设施法则的官方呼应：模型只是无状态 completion endpoint，harness 决定行为。
2. **Eval 失真 vs Eval 饱和 是两个独立失败模式**——失真 = grader 误判（Opus 4.5 CORE-Bench 42%→95%）；饱和 = agent 100% 通过（capability eval 渐失效）。两者都需要主动管理。
3. **"Eval-driven development" = 产品团队 + research 团队的共同语言**——Anthropic 让 PM / CSM / sales 能通过 Claude Code PR 贡献 eval task 是社区级别的资源配置；与 [[Finding Your Unknowns]] 的"reduce unknowns" 同源——eval 写下来的过程 = 把隐性 spec 显性化。
4. **Swiss cheese model 在 AI 系统是方法论 + 工程纪律**——本 wiki 自身的 [[Agent Harness 治理协议]] 双层验证 + CI wiki quality gate 都是 swiss cheese 的工程化实现。

## 抓取与限制

- WebFetch markdown 转换保留全部正文；Page chrome（nav/footer/sitemap/social links）已剥离
- inline image 引用 Next.js URL，未下载/嵌入
- ~350 行正文；附录列出 5 个 eval framework
