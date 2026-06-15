---
title: "Agent Runtime 正在成为 AI 的下一个主战场"
source: "url"
source_file: "https://yage.ai/share/agent-runtime-battlefield-20260516.html"
created: "2026-05-19T01:01:58Z"
source_url: "https://yage.ai/share/agent-runtime-battlefield-20260516.html"
extract_method: "readability"
---

[← 目录](https://yage.ai/share/) [EN](https://yage.ai/share/agent-runtime-battlefield-en-20260516.html)🌙

[Superlinear Academy](https://superlinear.academy/)

如果你每天用 AI 写代码，选模型的流程大概率很认真：看 benchmark、比价格、读评测。选工具的流程大概率很随意：UI 好不好看、免不免费、同事用啥就跟着用。这个优先级排序有一个隐含假设—模型决定了产出的上限，工具只是把模型的能力暴露出来，差别不会太大。

2026 年 5 月，这个假设正在从两个方向同时被打破。

自下而上的方向来自数据。Cline 在 Terminal-Bench 2.0 上跑出了同一个模型在不同 runtime 上的系统性差异—claude-opus-4.7 在 Cline 上是 74.2%，在 Claude Code 上是 69.4%，同一个模型差出 4.8 个百分点。自上而下的方向来自行业信号—DeepSeek 正在招聘 Agent Harness 产品经理，OpenAI 成立了 Deployment Co. 做全栈 Agent 服务，Anthropic 发布了 Claude Cowork 和 Partner Network。模型公司这个品类正在被 Agent 平台这个更大的品类吸收。

这两条线指向同一个结论：agent runtime 不只是被忽视的工程层，它正在成为整个 AI 行业的主要竞争界面。

## 4.8 个百分点是什么量级

要在直觉上把握 4.8pp 的大小，最好把它放进模型版本迭代的尺度里看。

Terminal-Bench 2.0 的公开数据提供了直接的参照。Claude Opus 4.5 到 4.6 是一次版本迭代，在同一个 Claude Code harness 上，得分从 59.8% 提升到 65.4%—增加了 5.6 个百分点。Claude Opus 4.6 到 4.7 是又一次版本迭代，从 65.4% 提升到 69.4%—增加了 4.0 个百分点。

[Cline 靠 runtime 优化在 opus-4.7 上多拿的 4.8pp](https://cline.bot/blog/introducing-cline-sdk-the-upgraded-agent-runtime)，大致相当于从 opus-4.6 换成 opus-4.7 所带来的提升。也就是说，如果 Claude Code 的用户不升模型，但切到 Cline 的 runtime 上，拿到的性能收益和把模型升一个版本差不多。

更极端的例子来自 Cline 自己的 hill climbing 实验。今年 2 月，Cline 团队在不换模型的前提下，只优化 agent harness 的 prompt、工具定义、错误处理和上下文管理，把 claude-opus-4.5 在 Terminal-Bench 上的得分从 47% 拉到了 57%。10 个百分点的提升，全部来自 runtime 工程。这个数字超过了 opus 两次版本迭代在同一 harness 上的提升幅度之和（59.8% → 69.4%，累计 +9.6pp）。

[方法论文章](https://cline.bot/blog/a-practical-guide-to-hill-climbing) 描述了具体的迭代过程：用 Harbor 框架在 Modal 上跑 89 个真实 terminal 任务，每轮 40-50 分钟出结果，每次改一个变量—一条 prompt、一个 bug fix、一个配置参数—分数上升就保留，下降就回滚。Cline 团队对失败模式的分类也值得留意：大约 25% 的失败是模型能力天花板，换什么 harness 都救不了；剩下 75% 可以通过 prompt 调整、工具定义优化、错误处理改进来修复。

这个 25/75 的分配本身就是判断框架。Harness 不是万能的—如果你的模型选错了（用 claude-haiku 跑复杂重构），harness 再强也救不回来。但它也不是可有可无的—75% 的失败都可以在 runtime 层修复。

LangChain 的独立实验也验证了同一点。他们在 [Deep Agents harness profile 测试](https://www.langchain.com/blog/tuning-deep-agents-different-models) 中发现，同样的模型，有无针对性的 harness profile 可以差 10-20 个百分点—GPT-5.3 Codex 在 tau2-bench 上从 33% 提升到 53%，Claude Opus 4.7 从 43% 提升到 53%。Harness 不是可选的性能优化，而是决定模型在 Agent 场景下能不能跑起来的关键层。

## 为什么 runtime 能差出这么多

Cline 官方的表述是”rewrote the prompts, simplified the loop, tightened context management, improved feedback loops and error handling, and rethought how tools are defined and surfaced to the model”。拆开看，是四个相互关联的设计决策。

第一是 prompt 设计。Cline 重写了 system prompt—不是措辞调整，而是重新定义了模型如何理解自己的角色、如何使用工具、如何判断任务完成。在 agent 场景下，模型需要在几十轮工具调用中保持方向感，一个微妙的措辞差异在长 session 中被反复放大。Cline 的迭代方式是每次改一个变量然后跑完整 benchmark，用分数而非直觉来判断 prompt 的有效性。

第二是工具定义和呈现方式。工具定义的详细程度、参数的描述方式、返回值的格式—这些直接影响模型调用工具的正确率。Cline 把 provider 逻辑隔离在 `@cline/llms` 层，agent loop 本身不感知模型差异，工具定义只需要为一套逻辑优化。

第三是上下文管理。agent 的上下文窗口在长任务中持续膨胀，什么时候 compact、按什么顺序删除、哪些信息值得保留—这些决策直接影响任务后期的表现。[Prompt Caching 作为一等约束](https://yage.ai/share/prompt-caching-harness-constraint-20260404.html) 里讨论了一个反直觉的设计原则：为了维持 cache 的 prefix 稳定性，compaction 时应该优先删除尾部的最新内容而非头部的旧内容。因为 prefix 稳定性决定了 cache 命中率—Anthropic 的 cache hit 定价是 miss 的十分之一，DeepSeek 同样。这不是性能优化，是能不能跑得起的 viability constraint。

第四是错误处理和反馈闭环。模型在执行中会犯错—调用了错误的工具、生成了不合法的参数。runtime 怎么把这些错误信息反馈给模型，直接决定了模型能否在下一次尝试中修正。好的错误消息不只是说”出错了”，而是告诉模型具体错在哪、当前状态是什么、有哪些可选路径。

Cline SDK 的四层架构（`@cline/shared` → `@cline/llms` → `@cline/agents` → `@cline/core`）本身是这些设计决策的载体。agent 层是 stateless 的纯执行循环，不绑定 session 存储；core 层负责持久化和编排但不干预 agent loop 的执行。这种分层让 hill climbing 中的 A/B 测试可以精确控制变量：改 prompt 不影响工具定义，改工具定义不影响 session 管理。

## 所有模型公司都在往下走

Cline 的 benchmark 数据是自下而上的证据—用数字证明了 runtime 的重要性。自上而下的信号同样强烈：模型公司自己正在大规模向 Agent 平台迁移。

[DeepSeek 在 Mokahr 招聘页面上](https://app.mokahr.com/social-recruitment/high-flyer/140576)，Agent Harness 产品经理至今排在热招职位的第一位。这不是一个孤立的岗位—同一个页面上还有 Agent 深度学习算法研究员、Agent 数据策略工程师、Agent 全栈开发工程师，四条线构成一个完整的 Agent 产品团队。3 月 25 日 DeepSeek 集中开放了 17 个 Agent 相关岗位，4 月 24 日 DeepSeek V4 Preview 发布当天又密集补充了 Agent 全栈和 Agent 数据策略岗。V4 的官方发布说明第一条就是 Dedicated Optimizations for Agent Capabilities。到 5 月 16 日，Harness PM 仍然挂在热招第一位—人选还没到位，产品方向还在组建中。

OpenAI 的路线最激进。从 Codex CLI（2025 年 5 月）到 Codex App、Codex Security，再到 [Frontier](https://openai.com/index/introducing-frontier/)（2026 年 2 月）—一个整合了 Business Context、Agent Execution、Evaluation & Optimization 的企业 Agent 平台，客户包括 HP、Intuit、Oracle、Uber。2026 年 5 月，OpenAI 更进一步成立了 Deployment Co.，由 TPG、Brookfield 等私募支持，融资超 40 亿美元，向前部署工程师到客户组织提供全栈 Agent 服务。

Anthropic 走的是另一条路。Claude Code 面向开发者，[Claude Cowork](https://www.anthropic.com/news/claude-cowork) 面向非技术用户的桌面端全自主 agent—在 Mac 的 Linux 虚拟机中运行，通过 Chrome MCP 控制宿主机的浏览器和桌面。同时推出了 Claude Partner Network，Blackstone、Goldman Sachs 等各出资 3 亿美元，面向医疗、制造、金融、零售四个行业提供托管 Agent。Anthropic 还在订阅计划中新增了 Agent SDK credits—给第三方的 programmable usage 分配专门配额。

LangChain 在 5 月发布了 [Managed Deep Agents](https://www.langchain.com/blog/introducing-managed-deep-agents) 和 SmithDB—一个为 nested、long-running agent traces 设计的专用可观测性数据库。Cline 把内部 runtime 抽成了 [开源 SDK](https://cline.bot/blog/introducing-cline-sdk-the-upgraded-agent-runtime)（Apache 2.0），从 VS Code 插件和 CLI 的底层引擎变成可供任何人嵌入的独立产品。

这不是一家公司的动作。这是行业级的结构位移。用 [AINews 5 月 13 日的总结](https://news.smol.ai/issues/26-05-13-not-much/) 来说：“Cline, LangChain, Notion, and Cursor all pushed deeper into agent platform territory.”

## 为什么是现在：token 价格归零之后

驱动这场集体迁移的逻辑很清楚：模型 API 的定价竞争已经接近终点。

2026 年 4 月同一周内，三家 lab 发布了前沿模型。Claude Opus 4.7 每百万 token 输出 $25，GPT-5.5 是 $30，DeepSeek V4-Pro 是 $3.48，V4-Flash 是 $0.28—V4-Flash 的推理成本是 GPT-5.5 的 1/107。在中国市场，竞争更激烈：Alibaba 的 Qwen 3.6 Plus 预览期直接免费，Xiaomi 的 MiMo V2 Flash 输入价格 $0.09/M。

当 token 价格趋近于零，纯 API 的收入无法支撑基础模型研发的持续投入。更根本的问题在于护城河：模型层的切换成本极低。一旦你的 harness 或 agent runtime 做得足够好，换一个 LLM provider 往往不需要经过太多适配—改一个环境变量或者配置文件里的 model ID，行为基本一致。OpenCode 现在就是这样：用户可以在不同 LLM provider 之间自由切换，体感上的智能差异被 runtime 层吸收掉了。当切换模型几乎无摩擦时，模型层就没有护城河可言。价值捕获只能向上走—从 API 到平台到服务。Agent 平台创造了完全不同的收入结构：平台费（席位制或包月）、消费加价（平台内的模型调用按平台定价计费）、增值服务（行业模板、定制 skill、forward-deployed engineering）。更重要的是创造了切换成本—system prompt、skill 配置、MCP server 连接、harness 配置—这些一旦在某个平台上建立，迁移的工作量远大于替换一个 API key。

三家的锁定策略各有不同。OpenAI 走全栈锁定—从 ChatGPT Plus 的 770 万订阅用户做分发，Frontier 的 Business Context 层把企业数据和工作流留在 OpenAI 生态里。Anthropic 走开放协议加运维锁定—MCP 协议降低工具集成的切换成本，但 Agent 行为配置、skills、managed agents 的运维知识留在 Anthropic 平台上。DeepSeek 目前没有平台锁定—策略是生态渗透：MIT 开源、OpenAI/Anthropic 双兼容 API、比竞品低一到两个数量级的价格。

这正是 Harness 岗位的紧迫性所在。生态渗透建立的是使用习惯，不是切换成本。LangChain Deep Agents 内置了 DeepSeek V4 的 harness profile，OpenClaw 在 V4 发布当天就将其设为默认模型—但这些是 endpoint 级别的集成，不构成锁定。DeepSeek 需要一个自己的 Agent 平台来创造和 OpenAI、Anthropic 同级别的切换成本。在中国市场，这个需求还有一个额外的紧迫性：竞争对手的 Agent 策略都绑定了自己的生活场景生态—Alibaba 的 Qwen 和淘宝打通，ByteDance 通过抖音和火山引擎做分发，Tencent 有微信的十亿级用户。DeepSeek 是唯一的纯技术型玩家。

## 这对 builder 意味着什么

对于使用 AI 写代码的人—而不是卖 AI 的人—这一层结构位移有几个直接的后果。

第一，选 runtime 和选模型一样需要认真对待。Cline 的 hill climbing 实验和 LangChain 的 harness profile 测试都说明，runtime 可以独立贡献 10-20 个百分点的性能差异。这个量级相当于一次模型版本迭代。

第二，runtime 的选择维度比模型选择更复杂。模型选择主要看 benchmark 和价格。runtime 选择需要考虑：模型支持广度（你的工作流是否需要在不同模型之间切换）、层次化程度（能否只使用需要的部分）、prompt engineering 开放性（能否修改 system prompt 和工具定义）、缓存策略（cache 命中率直接影响成本基线和延迟）。这些维度目前没有标准化的 benchmark 来做跨 runtime 对比—Terminal-Bench 2.0 是唯一给出了跨 harness 数据的测试，但它测的是 terminal 场景，不代表所有 coding 任务。

第三，中国市场有一个特殊的窗口。DeepSeek 的 harness 还没建好—PM 岗位 5 月 16 日还在招。这意味着 DeepSeek V4 目前的性能优势需要通过第三方 runtime（Cline、OpenCode、LangChain Deep Agents）来释放。谁能帮 DeepSeek 解决”有模型没锁定”的问题—做一个针对 DeepSeek V4 优化的 harness profile，或者把 DeepSeek 的模型优势转化为产品化的 Agent 体验—谁就拿到了下一张牌。这不是一个需要等 DeepSeek 自己做完的事，是可以现在就开始做的事。

最后，最可靠的选型方法不变：在自己的代码库上跑 A/B 测试。Terminal-Bench 提供的信号是方向性的—runtime 差异确实存在，量级不小。Harness PM 招聘提供的信号是趋势性的—整个行业都在往这个方向走。但哪个 runtime 在你的具体工作流上表现最好，只能靠你自己在真实代码上实测。用 Harbor 这样的框架，在你自己的 repo 上，用你实际使用的模型，跑 10-20 个代表性任务。这比阅读任何 benchmark 排名都更有参考价值。

“模型公司”这个品类正在消解。OpenAI、Anthropic、DeepSeek 都在做同一件事：把模型能力打包成 Agent 平台和服务，向价值链下游延伸。Agent runtime 层不是锦上添花的工程优化，是这个行业的下一个主战场。它的竞争结果将决定未来五年 AI 的价值到底被哪一层捕获。
