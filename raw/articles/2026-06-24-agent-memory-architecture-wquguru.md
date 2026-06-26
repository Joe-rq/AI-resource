---
title: Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀
author: WquGuru
handle: @wquguru
date: Jun 24, 2026
source_url: https://x.com/wquguru/article/2069641926752780384
source_type: article
archived: 2026-06-26
tags: [agent-memory, agent-architecture, claude-code, openclaw, memory-system]
---

# Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀

**Source**: [WquGuru (@wquguru)](https://x.com/wquguru/article/2069641926752780384) · Jun 24, 2026

几个月前我开始用 OpenClaw，发现它带给 Agent 行业的东西里，最让我兴奋的除了定时任务，还有一个看起来平平无奇的文件：MEMORY.md。
这个好奇心驱使我翻了翻本机 ~/.claude/ 目录。结果发现，我经常用 Claude Code 跑 /loop 的那些项目，每个下面都有自己对应的 memory 文件。它们不是日志，不是 README，也不是类似 session 历史的东西：
把几个项目的 memory 放在一起看，一个问题自然浮现：他们都在记录些什么内容。 有的是“以后必须这么做”，有的是“这个项目现在是这个状态”，有的是“上次在这里踩过坑，别再来了”，有的是“我们为什么相信这个结论”，还有的是“下一轮 loop 从这里接着来”。
Agent Memory 其实已经从“存聊天记录”分化成了一整套架构。规则、画像、历史、证据、反思和技能沉淀，各有各的存储方式、加载时机和治理难题。这篇文章想完整讲清楚的，就是截至 2026 年中，这套架构到底长什么样。
本文适合哪些人阅读：
 正使用或者构建Coding Agent、研究Agent、个人AI Agent或任何需要跨 session 持续工作的 LLM 应用的开发者；
对 agent 架构感兴趣但还没想清楚 memory 该怎么分层的技术决策者；
已经在用 Claude Code / Codex / OpenClaw / Hermes 等工具、想理解自己项目里那些 memory 文件到底在干什么的重度用户
一、长上下文解决当前任务，Memory 解决跨任务复利
先说一个很多人都搞混的点：Agent Memory 不是长上下文的替代品。
250K、1M 甚至更长的 context window 已经是标配。长上下文当然重要——它让模型在当前任务里能同时看见更多文件、更多日志、更多证据，避免频繁摘要带来的信息损耗。
但长上下文解决的永远是“这一轮能装下多少”。
Memory 解决的是另一个问题：下一轮醒来的时候，agent 还记不记得上一次为什么要那样做。
Context window 是工作台，当前任务需要的材料全摊在上面；RAG 和搜索是按需调用的外部资料库；Memory 则是跨会话、跨项目、跨 agent 持久存在的状态层。三者分工清晰。
一个 coding agent 只有长上下文没有 memory，下周重开 session 照样踩同一个测试环境的坑。一个 research agent 只有 RAG，它能查到过去的资料，却不知道哪条已经被证伪、哪个来源在这个主题上不可靠。一个交易 agent 只有 transcript，回看得了所有日志，分不清哪些已经升格成不变量、哪些只是一次偶然。
Memory 的核心价值不在“存得多”，而在把过去的东西分层：哪些该常驻，哪些该搜索，哪些该归档，哪些该变成以后可复用的技能。
二、第一层：规则记忆——Agent 的工作宪法
最早被广泛使用的 agent memory，其实比任何自动记忆系统都更早落地。它就是规则文件
Claude Code 叫 CLAUDE.md, Codex 叫 AGENTS.md。本质是一份“工作宪法”：这个项目怎么构建和测试，哪些目录绝对不能碰，哪些命令必须在特定子目录跑，哪些代码风格和提交规则不可破坏，哪些业务红线比完成当前任务本身更重要。
优点一目了然：可读、可改、可审计、可放进 Git。团队能 review，CI 能检查，agent 每次启动都能看到。
但它有明确边界。规则文件适合放“长期稳定、每次都该遵守”的东西，不适合塞所有历史细节。把每个 bug、每次实验、每条日志都往 CLAUDE.md 里堆，最后只会把上下文变成一坨低密度噪声。
Claude Code 官方文档也把 CLAUDE.md 和 auto memory 拆得清清楚楚：前者是人写的指令和规则，后者是 Claude 根据修正和偏好自己积累的学习。Codex 同样强调，团队必须遵守的规则应该放在 AGENTS.md 或 repo 文档里，memories 只是本地 recall layer.
第一条设计原则就此确立：
必须遵守的规则，不要只放在自动记忆里。它们应该进入版本化的规则文件。
规则 memory 是 agent memory 的第一层。它解决的是“以后都按这个方式做”。
三、第二层：常驻画像——每一轮都要付 token 税的东西
规则之后，是一类更微妙的东西：画像。
Hermes Agent 的设计在这一点上很有性格。它内置两个文件：MEMORY.md 存 agent 自己的高密度笔记——环境事实、项目约定、学到的经验；USER.md 存用户画像——偏好、沟通风格、长期期待。这两个文件在 session 启动时直接注入 system prompt，而且有严格的长度限制：超限不是静默压缩，是直接报错，逼着 agent 自己去合并、替换、删除。
这个设计很克制。但正是因为克制，它才有效。
常驻记忆不是越多越好。它每一轮都要付 token 税，而且位置越靠前越容易影响模型判断。如果你把大量未经整理的历史全塞进常驻记忆，agent 会变得又贵又混乱——就像一直对一个人重复十年前的所有对话，指望他从中提取有用的东西。
常驻 memory 应该只放三类东西：身份——这个 agent 是谁，长期职责是什么；偏好——这个用户稳定地喜欢什么、不喜欢什么；不变量——环境中反复成立、下次必然有用的事实。
我自己的 garden memory 就很像这一层。它不记每次写文章的全过程，只记“公开 handle 用 wquguru，不用私有账号”、“AGENTS.md 和 .agents/skills 是 symlink“、”garden deploy 走 Cloudflare Pages + Access“——这些下次必然用得上的事实。
第二条设计原则：
常驻 memory 应该短、硬、高密度。历史不应该常驻，只有压缩后的身份、偏好和不变量才值得常驻。
画像 memory 解决的是“agent 该以什么身份、带着哪些稳定偏好继续工作”。
四、第三层：历史召回——大部分记忆不该常驻，但必须能被找到
那么大多数历史如果不该常驻，放哪？
答案是按需召回。需要的时候搜出来，不需要的时候就安静待在磁盘上。
Hermes 用 SQLite FTS5 保存所有 CLI 和 messaging session，提供 session_search。完整保留原始消息，没有摘要带来的信息折损，还能沿着 session 往前后滚动看上下文。
OpenClaw 把 workspace 设计得更像文件系统记忆：MEMORY.md 是精炼层，memory/YYYY-MM-DD.md 是日常笔记，DREAMS.md 存放离线思考产出。memory_search 和 memory_get 负责召回，配了 embedding provider 之后还能做 vector + keyword 的混合搜索。
Codex 的 Memories 也走这个路子——把旧线程里稳定的偏好、工作流、技术栈、项目约定、已知坑转成本地 memory files，未来任务中按需带入。
一个共识正在形成：把“常驻记忆”和“历史召回”拆开。 常驻记忆像索引页，很短。历史召回像资料库，很大。搜索负责在需要时把资料库里的局部片段精准地拿出来。
回到最开始图片中的 carrywatch——它的 MEMORY.md 就是索引页，十来行，每行指向一个 topic file。binance-funding-interval-bug.md 记录根因、影响范围、修复 commit、验证方式和仍未解决的问题。clock-domain-and-health-freshness.md 记录了 macOS 上 monotonic clock 在 sleep 中冻结而 wall clock 继续前进，导致“数据 stale 了 6.6 小时但健康状态仍显示 green”这种反直觉 bug 的完整分析。
这类文件每次都注入 prompt 是浪费，但完全丢掉的话，下次 agent 又得从零开始查。所以它最适合成为按需召回的历史 memory。
第三条设计原则：
历史 memory 应该可搜索、可追溯、可局部读取，而不是全部常驻上下文。
历史召回解决的是“过去到底发生过什么，以及当时为什么那样判断”。
五、第四层：证据链和状态治理——记住结论不够，得记住凭什么
真正难的 memory，是记住结论的来源。
Agent 太容易把一次总结当事实，把一次猜测当经验，把一次临时 workaround 当长期规则。memory 一旦长期化，错误也跟着长期化——而且是那种越久越难发现、越自信越难纠正的错误。
这就是我越来越在意 memory 文件结构的原因。
一个合格的 bug memory 不应该只写“已修复”，它应该像一份微型的 postmortem：问题是什么，证据在哪（官方字段实际来自 fundingInfo 而非 premiumIndex response），影响了什么（4 小时 symbol APR 低估 2 倍，1 小时低估 8 倍），怎样修的，怎样验证的，以及还有什么没解决的（last-settled 和 predicted funding 语义仍然不一致）。
相比普通笔记，这更像是可审计的工程记忆。
trader 项目的 memory 更说明问题。它不是简单地记“Bitget demo 已接入”，而是把 demo 与真实账户的边界红线、费用符号、结算不变量、deploy 拓扑、Grafana 面板、只 commit 不 push 的授权变化——全部写进 memory。
为什么要记这些？因为它们构成了状态治理。一个长期运行的 agent 如果不知道“哪些改动涉及资金结算必须升级确认”，代码能力再强也会在错误边界上行动。一个自治 loop 如果不知道“只允许本地 commit 不允许 push”，就可能把技术上正确、流程上错误的改动推上远端。
所以 agent memory 里必须有一类东西叫 governance memory：权限边界、风险红线、环境拓扑、部署流程、验证闸门、当前运行状态，以及上一次决策为什么成立。
这类 memory 不能只靠向量召回。它需要清晰的结构、显式的状态和可人工审计的来源。
第四条设计原则：
Agent memory 同时也是治理系统。它要管理来源、置信度、过期性、权限和可删除性。
六、第五层：从 recall 到反思与技能沉淀——memory 的复利在此
到目前为止讨论的仍主要是 recall——记住规则、画像、历史和证据。
但 agent memory 真正的分水岭在下一层：self-evolution。
Recall 只是想起过去发生过什么。Reflection 是总结过去为什么成功或失败。Skill extraction 是把重复成功的路径沉淀成可复用的流程。Dreaming 是在空闲时离线整理，而不是每一轮在线临时往上下文里塞东西。
OpenClaw 的 dreaming、Hermes 的 post-turn self-improvement review、Claude Code 的 auto memory、EverOS 的 agent cases 和 skills，本质上都在朝这个方向走。
trader 项目里那条“回测框架与策略经济性结论”已经接近经验沉淀。它把多个时间窗口、多个标的、多组参数格子的实验结论整理成了策略判断：高换手弱信号结构性地净负，降换手是核心杠杆，窄样本容易误判策略不行，足够宽的标的池和更长窗口才能看到稳定性，回测数据源必须和真实交易所闭环。
这类东西如果只停留在聊天记录里，下次 agent 又会从“跑一次看看”开始。一旦沉淀成 memory，下一轮可以直接从更高层起步——哪些参数值得扫，哪些验证不能省，哪些早期结论已经被后续样本修正。
这才是 memory 真正的复利。
第五条设计原则：
Agent memory 的终局不是“记住更多”，而是少犯同样的错，更快复用做对过的事。
七、四个应用的 memory 架构对照
Claude Code、Codex、OpenClaw 和 Hermes 放在一起看，应用层 memory 正在清晰分化为四层
规则层：CLAUDE.md / AGENTS.md，适合放必须遵守的项目约定
常驻层：MEMORY.md / USER.md，适合放高密度身份、偏好和不变量
历史层：session search、daily notes、topic files，适合放大量事实、证据和过程
进化层：dreaming、reflection、skills，负责把历史经验转成未来行动的默认能力
真正的成熟 agent memory 是这四层的组合。没有一个文件、一个向量库能单独撑起来——就像你不能指望只用一种数据结构管理操作系统的全部状态。
八、EverOS 为什么踩中了这个方向
EverOS 把 memory 设计成了 developer-facing runtime——开发者能直接读写、调试、版本化的结构，而不是隔着 API 猜一个黑盒召回层里到底存了什么。
它的几个设计正好对上前面的分层：
Markdown as source of truth：记忆落盘为可读、可改、可 grep、可 Git 版本化的文件
SQLite + LanceDB: Markdown 是真源，SQLite 管状态，LanceDB 管向量、BM25 和 scalar filters
SQLite + LanceDB：Markdown 是真正的数据源，SQLite 负责管理状态，LanceDB 负责处理向量、BM25 和标量过滤器
Dual-track memory: user memory 和 agent memory 分开，episodes / profile 与 cases / skills 不混在一起
双轨记忆：用户记忆与智能体记忆相互独立，不会将“episode/个人档案”与“case/技能”混在一起。
Multimodal ingestion：文本、图片、音频、PDF、HTML、email 都可以进入统一记忆层
Self-evolution：真实使用中的 cases 可以沉淀为 skills
Orthogonal retrieval：按 user_id、agent_id、app_id、project_id、session_id 维度检索
正交检索：按 user_id、agent_id、app_id、project_id、session_id 等维度进行检索。
如果 memory 只在一个远端黑盒里，开发者永远不知道 agent 记住了什么、为什么召回这条、什么时候该删掉、哪些已经过期。如果 memory 是 Markdown，第一步至少变简单了：你能打开它，读它，diff 它，改它，把它放进 Git，把它交给另一个 agent。
这不是最终答案。但它是目前最好的工程起点。
九、Memory 会带来的新问题
Memory 不是银弹。恰恰因为它会长期存在，它会制造比上下文幻觉更棘手的麻烦。
错误记忆永久化：一次误判被写进 memory，下次 agent 会更自信地重复它，而且因为“这是 memory 里记的”，比从零推理更不容易自我纠正。
过期信息继续影响决策：今天的 API 限制、部署拓扑、账户状态，下个月可能已经面目全非，但 memory 里的旧快照还在默默左右 agent 的判断。
prompt injection 的持久化污染：一次网页内容被 agent 当成“经验”保存，后续所有 session 都会中招——这比单次攻击严重得多。
隐私和删除的不可逆性：聊天记录删了，不代表从中抽取的 profile、facts、skills 也跟着消失。抽取是一个不可逆的信息精炼，但遗忘需要同样的系统性设计。
summary 把证据变成二手结论：二手结论用多了，系统越来越难区分“真实发生过的事实”和“模型当时的解释”。这个边界一旦模糊，memory 就从资产变成了负债。
所以好的 memory 系统必须内置治理：来源、时间、过期性、置信度（事实/推断/偏好）、作用域（用户/项目/agent/组织）、可删除性、可追溯性（能否回到原始 session、文件或 commit）。
我也因此越来越不喜欢把 agent memory 简化成“向量库里存对话”。向量库只是召回手段。真正的 memory 系统要处理的是状态、来源、权限和演化——这些东西，一个 embedding 解决不了。
十、结语：Memory 是 agent 的状态层
回到开头。
本机那些 ~/.claude/projects/*/memory/MEMORY.md 让我确信：当一个 agent 真的开始参与长期项目，它自然会需要一个对话之外的地方来保存状态。
这个状态包括项目怎么运行，哪些 bug 已被证伪，哪些验证方法可靠，哪些风险红线不能碰，哪些实验结论已被后续数据更新，哪些流程下次可以直接复用——以及，最后这条最容易被忽略——下一步该做什么、什么时候触发、哪些承诺还没兑现。
Memory 不只记录过去。任务队列、定时触发、未完成的 loop 状态，都是面向未来的记忆。trader 项目里“巡检-修复-部署 loop”和“下一轮从哪里继续”，本质上就是 agent 对自己的承诺。丢掉它，agent 就会反复从零开始规划已经规划过的事，像一个每天早上醒来都忘记昨天进度的人。
长上下文让 agent 在当前任务里看得更全，Memory 则让 agent 在下一次任务里起点更高。
这就是 Agent Memory 从“小功能”变成“架构层”的原因。它不是一个可选的增强，而是 agent 从单次调用进化到持续运行的基础设施。少了任何一层，agent 都会在某个维度上退化成无状态的 API wrapper。
如果你正在做 coding assistant、research agent、personal AI、browser agent、customer support agent，或者任何需要跨 session 持续工作的 LLM app，不妨试试 EverOS 这个 repo：https://github.com/EverMind-AI/EverOS
