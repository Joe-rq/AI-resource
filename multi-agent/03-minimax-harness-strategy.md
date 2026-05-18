> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [x.com](https://x.com/AlchainHust/article/2055154019056975973)

> 前几天看姚顺宇在张小珺最近那期 4 小时访谈里说，他在 Google DeepMind 主要做 ML Coding 和 Long Horizon（长程任务）。

前几天看姚顺宇在张小珺最近那期 4 小时访谈里说，他在 Google DeepMind 主要做 ML Coding 和 Long Horizon（长程任务）。后者就是让模型能够连续干好几个小时甚至好几天才能完成的复杂活。他说的是让单个 AI 变得更聪明。

但同样的事情，另一条路径上也在发生。这件事现在像个隐秘的共识，所有头部大模型公司都在做。

OpenAI 从去年起推了让开发者搭多 AI 协作的工具集，又补上了让 AI 跑长任务的能力。Anthropic 做了两套独立的产品，一套在他们的对话产品里、一套在 Claude Code 里的 Agent Teams，都是让一个 AI 带一堆 AI 干活的架构。Google 也推了开发框架，还和一百多家公司一起搞了让不同厂商的 AI 能互相通讯的协议。

这些公司不约而同地造同一个东西，试图回答同一个问题：长程任务该怎么靠谱地交付​。

昨天 MiniMax 发布了 Mavis（MiniMax as a Jarvis），同步出了一份相当详尽的技术报告。读完发现他们在这个问题上走得很远，有了相当成熟的解法。

先讲一条我最近一个月为了让我的 AI 写作工作流更加 Harness 而调整的一条流程规则。

在我的 AI 写作工作流了内容写完之后一直有要求按规则审校的流程存在。但我最近改的规则是：审校必须启动一个独立的 Agent，写内容的 AI 不审自己的内容。这条规矩贴在我所有写作项目的 CLAUDE.md 里。原因是踩过太多次坑。同一个 AI 写完一篇文章，紧接着让它自己检查，它会诚恳地告诉你「我又通读了一遍，没问题」。但它检查的对象，就是它自己刚刚构造出来的现场。

我后来把审校 AI 单独拎出来，写的不审，审的不写​。

[](https://x.com/AlchainHust/article/2055154019056975973/media/2055153170989629440)

[![](https://pbs.twimg.com/media/HIVe65vawAAcaWR?format=jpg&></p></a></section><p>上面这张是我每次写完稿启动三审三校时的截图。两个审校 AI 被丢到后台并行跑，各自只看产出文件，看不到我和写作 AI 之间的过程对话；它们出意见之后由一个编辑 AI 合稿。整个过程从头到尾，写内容的 AI 不参与任何一轮审校。</p><section data-block=)](https://x.com/AlchainHust/article/2055154019056975973/media/2055153170989629440)[](https://x.com/AlchainHust/article/2055154019056975973/media/2055153297397620736)

[![](https://pbs.twimg.com/media/HIVfCQpboAAHaDC?format=jpg&></p></a></section><p>读到 MiniMax 官方对 Mavis 的描述时我笑了一下。这家公司花了一整份技术报告论证一件事：别让 AI 当自己的裁判​。他们的判断是「多 Agent 系统是 runtime，不是 prompt 编排」。意思是让多个 AI 一起干活，关键不是给它们写更好的指令，而是给它们搭一个能长期运行、能管它们的底座。</p><p>这个底座的核心机制叫 Worker 和 Verifier 的对抗循环​。一个 AI 干活，另一个 AI 找茬，两个 AI 心思完全相反。</p><p>我从公众号写作里踩坑摸出来的一条朴素规则，跟一家头部大模型公司从工程严谨性推出的状态机设计，落点完全一样。他们做的事比我深得多，把流程纪律做成了由程序自动调度的对抗循环。</p><p>要看懂为什么需要让两个 AI 互掐，得先看单个 AI 干长活的时候是怎么坏掉的。</p><p>举我熟的场景。我用 AI 辅助写一篇文章时，整个流程不是一步：读 brief、做多源调研、列大纲、写初稿、跑独立审校、按反馈改稿、生成配图、写小标题、做封面图、最后排版发布，前后十几步。</p><p>任何一步只要交给 AI 接着上一步往下走，大概率出现两种情况。要么它把十几步压成两三步草草交付；要么它每做一步就停下来问你「123 已完成，要不要继续做 4」。你说「继续」。它又做了两步停下来。一个晚上下来，你有一半时间在打「继续」、「继续」、「继续」。</p><p>AI 对一个任务什么时候算「做完」的判断是模糊的。它不知道你的真实预期，所以干一半就停下来确认，宁可啰嗦也不冒险。</p><p>姚顺宇在访谈里讲过一个挺贴的哲学，原话是「用短的 context 去训练，但让它能做长的 context 的事」。意思是让 AI 在长任务里不漂移、不停下，关键不在上下文窗口做多大，而在它会不会自己管理上下文：该存的存起来、该扔的扔掉。</p><section data-block=)](https://x.com/AlchainHust/article/2055154019056975973/media/2055153297397620736)[](https://x.com/AlchainHust/article/2055154019056975973/media/2055153410387918848)

[![](https://pbs.twimg.com/media/HIVfI1kawAADggq?format=jpg&></p></a></section><p>第二个症状更隐蔽。AI 干长任务的时候，会逐步漂移。</p><p>我做橙皮书的时候踩过这个坑。让一个 agent 帮我写一整章 AI 技术解读，开头是技术分析的语气，写到第三节能不知不觉变成营销文案的口吻；让它列参考资料，它会把自己之前搜过的二手缓存当成一手来源贴上去。这时候你追问它，它会诚恳地回头自检，但它检查的对象，就是它自己刚刚漂移生成的现场。一个被自己污染过的记忆里，做不出真正的纠偏。</p><p>第三个症状是长任务期间没法快速响应你。在微信、飞书这种 IM 场景下，你发一条消息就期待几秒内有反馈。但很多任务天然需要几分钟甚至更久。AI 要么给一个浅答案应付，要么让你盯着对话框等十几分钟。MiniMax 官方文章里说，「我的 Agent 怎么不回我了」是他们收到的大量用户反馈。我估计很多人不管是用 OpenClaw 还是 Hermes 都感受过这种痛苦。Mavis 的解法是把「秒回用户」和「执行任务」拆开：主 AI 收到消息先快速应一声「收到，5 件事我去拆，完成后回来找你」，然后把任务派到后台并行跑，关键节点主动汇报。整个体验更接近一个能秒回微信、同时后台还在帮你干活的同事。</p><p>第四个症状最容易被忽视，是角色分工这件事其实没真正发生。</p><p>举我自己的例子。我有几十个公众号写作相关的 skill：选题、调研、初稿、审校、配图。看起来分工挺细。但它们全部跑在同一个 Claude 里，用同一套记忆，看同一组文件。本质上还是一个 AI 在轮班。每「换」一次角色，前面那个角色的影子都还在。</p><p>官方公众号里有句话点得很准：「角色扮演不等于角色分工」​。真正的分工得让每个 AI 从一开始就只做一件事，连工具集都不一样。会计用 Excel，设计师用 Figma，他们的工具不重叠，能力边界清晰，长期跑下来才有复利。</p><section data-block=)](https://x.com/AlchainHust/article/2055154019056975973/media/2055153410387918848)[](https://x.com/AlchainHust/article/2055154019056975973/media/2055153508454965249)

[![](https://pbs.twimg.com/media/HIVfOi5bIAElEM6?format=jpg&></p></a></section><p>这四个症状加起来导致的结果就是：单 AI 干长任务越长越不靠谱。倒不是 AI 不够聪明，是结构上就出了问题。</p><p>姚顺宇还说过一句话挺到位：「Coding 是 AI 使用工具和环境交互的一个很好的抽象。它的回馈信号清晰（运行成功或失败）、数据充分。」反过来读这句话我就明白了，写代码这种事最容易让「互相挑刺」机制跑通。因为有外部的、确定性的对错信号：代码能不能跑、测试过没过，机器说了算。在写作、研究、办公文档这些靠主观判断的场景里，光靠 AI 自己说「我检查过了」根本不算数。</p><p>得有个外部的东西来兜底。MiniMax 选的兜底方式，就是让另一个 AI 来挑毛病。</p><p>MiniMax 在公众号文章里把 Mavis 和 OpenAI、Google、Claude Code 的同类方案做了对比。Mavis 的整体架构是 Owner 拆任务、Worker 干活、Verifier 挑刺三角，但他们觉得做得最不一样的，落在两件事上。</p><p>Mavis 架构里，Worker 的目标是把活儿赶紧干完；Verifier 的目标是把活儿挑回去重做。两个 AI 都以「结束」为目标，但一方结束会触发另一方启动。Worker 觉得自己干完了，Verifier 立刻开始挑刺。Verifier 挑出问题，Worker 被自动叫回来修。修完 Verifier 再检查，过了才算真的完成。</p><p>我自己写过一个叫 darwin-skill 的工具，就是干 Verifier 的活。它会读一个 SKILL.md 文件，从结构和效果两个维度 8 个指标打分，挑问题、给优化建议。但我把它做成了一个事后跑的独立工具，跟 skill 的生产过程是脱离的。darwin 能告诉我「这个 skill 哪里写得糙」，但写 skill 的过程本身没有挑刺嵌在里面。Mavis 的 Verifier 是嵌在生产状态机里的，每一步产出立刻挑，挑不过就自动叫回来。这一步差距很关键。</p><p>官方原话里有一句我蛮认同：「​很多框架里的验证环节是可选的附加步骤，在我们这里它是架构的核心。​」</p><p>这话是 Mavis 的设计宣言。对比一下，Anthropic 在 Multi-Agent Research System 博客里讲的方案，是 Lead Agent 给 Subagent 分发任务并基于 outcome 评分，质量主要靠 Lead 的判断；OpenAI Agents SDK 的 Handoff 是接力式的，A 把任务交给 B，B 再交给 C，每一棒都不回头。Mavis 选了一条不一样的路：不要单中心评审，让 Worker 和 Verifier 直接对掐。</p><p>想象一个工厂流水线。工人在工位上做完一件活，按一下绿灯，活就传到检验员那里。检验员要么贴「通过」标签放行，要么贴「打回」标签让工人重做。整个流水线是机器在调度。传送带的速度、检验的时机、什么时候停下叫主管来，都不靠工人自己判断。</p><p>Mavis 就是这种流水线。每个「工人」是一个 AI，每个「检验员」是另一个 AI，但两个 AI 之间不直接说话，全程靠一个叫 Team Engine 的程序在中间调度。这个程序不是 AI，是确定性的代码。这件事很关键：它意味着系统的可靠性不依赖某个 AI 那一刻清醒不清醒，而是写死在程序里。</p><section data-block=)](https://x.com/AlchainHust/article/2055154019056975973/media/2055153508454965249)[](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[![](https://pbs.twimg.com/media/HIVfTW4bgAAWiov?format=jpg&></p></a></section><p>我读这张架构图的时候，觉得最关键的不是流程图本身，是几个被低估的细节：</p><ul data-offset-key=)](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

*   [任务被切成一批一批跑​。同一批里的活儿真的并行，各干各的，互不打扰。下一批要不要启动，看上一批是不是全部通过验证。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [两个 AI 之间不直接通讯​，全程靠程序中转。Worker 完成产出，程序自动把产出推给 Verifier；Verifier 说有问题，程序自动叫 Worker 重做，而且让它从上次失败的状态继续，不用从头来。这点我蛮有共鸣。我做橙皮书 pipeline 时这件事是手动的：哪一章审校没过，我得自己把反馈贴回去跟写章节的 agent 讲「之前哪里有问题、应该怎么改」。每本书十几章，手动衔接的次数不少。MiniMax 把这步做成了 Engine 自动完成的事。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [有重试上限​。两个 AI 万一陷入「改改改改不完」的死循环，程序会自动把决策升级，必要时叫人类来拍板。我的 darwin-skill 里也做过同样的事：自动优化迭代有上限，连续几轮分数不涨就主动停下，不会让 agent 无限消耗 token。区别是 darwin 的上限是给 skill 事后优化兜底的，Mavis 把上限内建到了生产任务的运行时调度里。 ## 对照着看，我自己的 skill 漏在哪](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    

[写到这里我想到了不少我之前做 skill 设计时一些零碎思考的影子。Mavis 文章里点到的几个组件，我自己各做了一两个，但没有一个像他们那样把全套打通。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[第一个是开头讲的写作三审三校​。写作 AI 写完，我自动起两个独立审校 AI 看产出文件，加一个编辑 AI 合稿。Worker-Verifier 的雏形，但是流程纪律，每次手动触发，不是 runtime。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[第二个是 huashu-book-pdf​，前面讲过的橙皮书电子书 skill，已经出版 7 本。每本书都跑了多 Agent 并行写章节加三审三校的流程，再构建 EPUB/PDF 上架微信读书。多 Agent 并行加挑刺这两件事我都做了，但调度是手动的，不是 Engine 在跑。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[第三个是 darwin-skill​。前面讲过它干的就是 Verifier 的活，区别是跟生产过程脱离。它额外做了一件事，是 hill-climbing（山丘攀登）式的优化：改一版、跑测试，分数涨了就保留，跌了就回滚。这是「挑刺加自动迭代」的闭环，但它的对象是 skill 本身，不是任务产出。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[第四个是 huashu-data-pro​，我做数据分析的 skill。收到数据先做一遍理解，然后选 3 到 5 个不同领域的专家角色并行分析，结果汇总后生成报告。我自己用的时候挺爽。但看完 Mavis 我意识到它有结构性缺口：我只做了拆任务和分头干，没有挑刺。多个专家各自的结论谁来核对？我设计的时候默认是用户。这意味着我把质量门禁丢给了人，没丢给系统​。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[把这四个放一起看，Mavis 做的事就清晰了。我手里有审校的纪律、有橙皮书的并行加挑刺 pipeline、有专门给 skill 挑刺的 darwin、有多专家分头干的 data-pro。每个都做对了一两件事，但全是单点​。Mavis 把这些拧成了同一套底座：挑刺嵌进生产过程、调度靠程序、每个 AI 有持续身份。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[而且 Mavis 把每个 AI 做成有持续身份的「同事」。下次再开这个 AI，它能记得上次干到哪里、犯过什么错。这跟我那些零散 skill 的差别本质上是「同事」和「工具箱」的差别。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[这种「我设计漏了一环、看别人补上了」的体感，比任何架构对比都更让我信服多 AI 协作的核心从来不是「开几个进程」，是结构​。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[读完技术报告我自己有个判断：AI 协作的下一个阶段，是把 AI 从「工具」变成「同事」​。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[工具是单次的，用完即弃，下次重新交代一遍背景。我那些零散 skill 大多是工具，能办事，但每次都得手动起来、手动收尾、手动衔接。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[同事是有持续身份的：它知道你之前让它干过什么、犯过什么错，下一次任务能记着上次的反馈接着干。这才是 Mavis 做「每个 AI 自带身份、笔记本、记忆、交付物」这件事的本质，把 AI 拉进一个有历史、有积累的关系里。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[跟「同事」配套的不只是记忆，还得有验收标准、可调度的流水线、可复盘的操作日志。这就是 Mavis 那一整套 Worker-Verifier-Engine 的存在意义。给 AI 协作搭底座比写 Prompt 重得多，但只有这条路才能让 AI 真正进入长期同事的形态。一个有记忆、有技能、有验收标准、能在长任务里复用经验的 AI 团队，比一个无所不能的超级指令更有用​。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[MiniMax 官方在文末也补了一句：「Team 不是默认选项，是策略选项。任务越短、越低风险、越确定，单 Agent 甚至脚本就够了。」](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[MiniMax 这次顺带把订阅做了合并：TokenPlan 和 Agent Plan 合一份，CLI、API、Agent 都打通，M2.7 模型、音乐、视频、语音都包含在内。Credits 额度在 Agent 和 API 之间可以共享，之前同时订阅了两个 Plan 的用户额外送一个月会员。背后逻辑和 Mavis 的整体设计一致：一份用户记忆、一组技能、一套额度，在不同入口都能用。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[回到开头那个观察。四家 AI 实验室都在朝同一个方向走，但每家路径不一样。没有谁的方案是定论，但都在补同一块基础设施。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

[我猜接下来一年，会看到更多人发现自己手里那些零散的「AI 协作小窍门」，被一个个写进产品。](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)

*   [MiniMax 官方 tech blog《MiniMax Agent Team - 为长程任务，持续进化而生》：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [MiniMax 官方公众号文章《一个 AI 还是不够》（Agent Team 自己采访自己的 Q&A 版）：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [Anthropic《How we built our multi-agent research system》：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [Anthropic《Managed Agents》（原话「session is not Claude's context window」）：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [Anthropic《Claude Code on Team and Enterprise》（含 Claude Code Teams 机制）：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    
*   [Google Agent Development Kit (ADK) 官方文档：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
    

*   [张小珺访谈姚顺宇《对姚顺宇的 4 小时访谈：请允许我小疯一下！》（B 站）：](https://x.com/AlchainHust/article/2055154019056975973/media/2055153591128915968)
