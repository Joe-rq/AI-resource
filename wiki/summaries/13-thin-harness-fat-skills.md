---
title: "Thin Harness, Fat Skills：套具要瘦，技能要胖"
type: summary
created: 2026-06-04
updated: 2026-06-18
sources: ["raw/articles/2026-04-18-thin-harness-fat-skills.md"]
tags: [harness, skill, architecture, judgment, yegge, yc]
---

# 摘要

Steve Yegge 在 YC Startup School 2026 提出的 agent 架构原则：AI 编码 agent 的 10x–1000x 生产力差距不来自模型智能，而来自套具架构。正确的形状是 **Thin Harness, Fat Skills**——把智能向上推到 markdown 流程文件（skill），把执行向下推给确定性工具，把中间层 harness 保持极薄（~200 LOC，只做跑模型循环、读写文件、管理上下文、强制安全四件事）。

> 套具就是产品。模型永远不是瓶颈，瓶颈是模型看到的**上下文质量**。

完整的五定义（Skill/Harness/Resolver/Latent-vs-Deterministic/Diarization）、三层架构 mermaid、Self-rewriting skill 循环，以及 Latent vs Deterministic 判定边界，见 **[[Thin Harness, Fat Skills]]**。

## YC Startup School 案例：6,000 Founder 的生产系统

五定义不是理论——以下是 YC 2026 年 7 月 Chase Center 实际运行的系统。

### Enrichment

`/enrich-founder` skill 拉取所有来源（申请表、问卷、1:1 顾问对话、X 帖、GitHub commits、Claude Code transcripts），跑 diarization，标出 founder **嘴上说的**和**实际在做的**之间的 gap。

> Maria Santos (Contrail)：声称做 "Datadog for AI agents"，但 80% commits 在 billing 模块——她在做伪装成 observability 的 FinOps 工具。
>
> 这个 gap 需要**同时**读 GitHub 历史、申请表、顾问对话，三者同持在心智中。没有任何 embedding 相似度搜索或关键词过滤器找得到。模型必须读完整 profile 然后做判断。

### Matching：skill-as-method-call 闪光

同一份 matching skill，三次调用，三套策略：

| 调用 | 输入 | 策略 | 关键技术 |
|------|------|------|---------|
| `/match-breakout` | 1,200 founder | 按 sector 聚类，30 人/间 | embedding + 确定性分配 |
| `/match-lunch` | 600 founder | 跨 sector 随机，8 人/桌 | LLM 发明主题 → 确定性算法 |
| `/match-live` | 现场任意 200 人 | 最近邻 embedding，1:1 配对 | 排除已见过的人 |

模型还做聚类算法做不到的判断："Santos 和 Oram 都是 AI infra，但不是竞品——Santos 做成本归因，Oram 做编排。放进同一组。""Kim 申请时写 'developer tools'，但 1:1 对话显示他在做 SOC2 合规自动化。移到 FinTech/RegTech。"

### Learning loop

`/improve` skill 读 NPS 调查，对"OK"评级做 diarization，提取模式后**把新规则写回 matching skill 文件**：

```
When attendee says "AI infrastructure"
    but startup is 80%+ billing code:
    → Classify as FinTech, not AI Infra.
```

7 月活动 12% "OK" 评级 → 下次活动 4%（8pp 提升，**0 行代码改写**）。模式普适：retrieve → read → diarize → count → synthesize → survey → investigate → diarize → rewrite the skill。

> Zach Lloyd（Warp）把这个机制命名为 **inner/outer agent loop**：inner loop 用 skill、outer loop 定时观察 inner loop 的运行表现并给 skill 做 diff。因为 skill 就是文件，"改 skill" = 改 markdown。详见 [[Skills 自我提升闭环：inner loop 用、outer loop 改]]。

## Skills 是永久升级

作者给 OpenClaw 下的一条指令被广泛传播：

> 你不被允许做一次性工作。如果我让你做某件事，而它属于"还会再做一次"的类型，你必须先在 3–10 个样本上手动做，给我看输出，我批准后**编纂成 skill 文件**。如果应该自动跑，挂到 cron 上。
>
> **测试：如果我必须第二次向你请求，你失败了。**

被点赞 1000+，被收藏 2500+。人们以为是 prompt engineering 技巧——**不是**。它就是上述架构的应用：你写的每一个 skill 都是系统的永久升级——永不退化、永不遗忘、凌晨 3 点也在跑；下一版模型发布，所有 latent 步骤的判断力瞬间提升，确定性步骤保持完美可靠。

> 系统复利。建一次，永远运行。
