> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/oqJ8yueAL7FL1uVIy8BRNg)

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOz2pJv0EMvIqr83sJCl5PibVibrasT36kFx07CWqIVAARABCzibPjuBt6Vtq0N5zcB7udZY2Xp9ibom8qyc3npFGFibicKicKbYL0OcbE/640?wx_fmt=png&from=appmsg#imgIndex=0)

2026 年 5 月 4 日，OpenAI 和 Anthropic 在同一天各自宣布了一件大事。OpenAI 联合 TPG 等 19 家机构成立了 Deployment Company，砸了 40 亿美元，专门往企业里派工程师帮他们把 AI 塞进核心业务流程。同一天，Anthropic 宣布跟 Blackstone、Goldman Sachs、Hellman & Friedman 合作，投入 15 亿美元成立企业服务实体，把 Claude 部署到中型企业的日常运营中。几天之后，Google Cloud CEO Thomas Kurian 亲自发 LinkedIn 招聘帖，宣布要招数百名 FDE。

**FDE**，Forward Deployed Engineer，前线部署工程师（嵌入式工程师）。 如果你关注 AI 行业，这个词大概不会是第一次听到。2023 年，Palantir 因为接入 LLM 推出 AIP 平台，股价一路暴涨，中文圈掀起了一波研究 Palantir 的热潮。那时候大家发现，支撑 Palantir 从神秘小公司走到千亿市值的，不只是技术，而是一套叫 FDE 的组织打法：把工程师扔到客户现场，跟客户一起把模糊的业务问题变成可落地的系统。一时间所有人都在讨论 Ontology、本体论，侃侃而谈。可 Palantir 的产品不对外公开，大部分讨论者实际上没有接触过它的界面和工作流。

那场讨论最终无疾而终。大部分人可能连一个 FDE 是怎么工作的都没见过，最后浅浅地得出一个结论：这不过是 Palantir 强行给自己加上 AI 叙事讲的故事。FDE？又一个华而不实的硅谷造词。

而在三年后，OpenAI 和 Anthropic 却又同时下重注在这个大家嗤之以鼻的事情上。 关于 FDE 的争论不只是中文圈有。在英文世界，即便这个岗位在两年里暴涨了 42 倍，质疑声依旧刺耳。VC Thomas Otter 在一篇被广泛传播的文章里写道：两年前，风投圈坚持所有 B2B 产品都应该拥抱 PLG（Product-Led Growth），结果大量公司硬套 PLG 翻了车。现在同样的事正在 FDE 身上重演。"当一种策略变得足够性感、足以被奉为'标准打法'时，我总会感到紧张。"

Reddit 上有人直接说这就是 "rebranded sales positions"，换了包装的销售岗。a16z 合伙人 Marc Andrusko 说大部分模仿者不过是 "Accenture with a nicer logo"，换了个好看 logo 的埃森哲。Twitter 上 @profitaboveall_ 的吐槽更直接：

> _"...you get enough small dogs yelling'AI consultancy'and all of a sudden the most credible title in the room is'Forward Deployed Engineer'."_

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOyDXa5YWzelvLVWXWLj0ecYDYYOhAVcibRjjGvgv6JnNYX91CXWH3ea3K168KHuv6UekYxlSkuSUoTZK5ccneRIPVhjqbH9sibcI/640?wx_fmt=png&from=appmsg#imgIndex=1)

所以 FDE 到底是什么？是 Palantir 的不可复制特例？还是所有 AI 公司都该学的方法？是 AI 时代真正的工作岗位，还是咨询公司换了个硅谷味的 title？

这种纠结问题的核心，是市场上叫 "FDE" 的东西，至少有两种完全不同的叙事。把它们混在一起讨论，得出的结论一定是错的。

所以我们必须要有一个定义。

**当说到 FDE 时，我们在讨论什么？**

* * *

FDE 的定义
-------

**FDE 是嵌入客户环境的工程师，背靠一个平台级产品，通过在现场解决客户的真实问题来发现产品应该长什么样。他的工作产物不属于单一客户，而是回流到平台，成为可服务更多客户的产品能力。**

这个定义里有四个要素，少了任何一个，它就变成别的东西：

1.  **有平台。** 没有平台级产品，就没有 FDE。这是前提。产品管理领域的教父级人物 Marty Cagan 说过："真正让 Palantir 如此高效、如此有价值的原因，是他们以 platform product company 的方式来解决这个问题。"

2.  **嵌入客户环境。** Forward Deployed，字面意思就是部署到前线。不是远程支持，不是售后回访，是在客户的工作环境里，从内部理解问题。

3.  **目的是产品发现，不是实施。** FDE 去客户现场不是把一个已知方案装上去，而是去发现 "产品应该长什么样"。产品的形态还没有定型，只有在现场解决真实问题的过程中才能被发现。

4.  **产物回流平台。** FDE 在客户现场做出来的东西，不只是留给这个客户的交付物，而是要回流到平台，成为可服务更多客户的产品能力。


去掉平台，你是咨询师。不嵌入客户，你是传统产品团队。只做实施不做发现，你是系统集成商。产物不回流，你是外包。

![](https://mmecoa.qpic.cn/sz_mmecoa_png/afd2uiaVAOOxeyvpGw4DA5ial7iapZiafNHTWoCALD8J0vKouJTXDbxXTszTssk9QvicMG4E1Zp8Ho6fSNFJHDCDVjvm4l3ymUNIdZ8M3OCntyVQ/640?wx_fmt=png&from=appmsg#imgIndex=2)

这个定义解释了 FDE 是什么。但它为什么存在？

Flybridge 的 Daniel 有一个很精准的说法：把 FDE 想象成**一个以人的形式存在的产品发现循环**（a product discovery loop embodied as a person）。他在客户现场梳理工作流，挖掘隐藏的约束，构建一个粗糙但管用的方案，然后把发现的规律反馈回总部，由产品团队固化为可复用的功能。

FDE 存在的原因是：有太多关于产品形态的探索，只能在现场完成。你没法坐在办公室里猜客户需要什么。Bob McGrew 讲过 Palantir 的起源：他们的客户是情报机构，你去问一个间谍 "你的工作流程是什么"，他不会告诉你。唯一的办法是派工程师进去，贴着客户工作，在现场发现产品该长什么样。

### 试金石

那怎么判断一个人到底是 FDE 还是咨询师？

我有一个暴论：**看这个人的成本在公司内部是算产品研发的，还是算项目交付的。** 如果是后者，不管你 title 写的是什么，你就是在做咨询 / 实施。

VC Thomas Otter 说过一句类似的话：

> _"If the FDE is billable, they are working for the project, not the product."_

FDE 一旦按项目计费，他就是在为项目工作，不是为产品工作。

还有一个更直觉的检验：你的第 10 个客户跟第 1 个客户花的精力一样多吗？如果是，你就是在做咨询。FDE 模式下，每一次客户部署都应该让平台变得更强，下一次部署的 effort 应该更少。这是一个飞轮，不是一条直线。

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOyfrg9MT5OXgVgW6k5xjLoj9HQ7TIhDcbwxXaFXU1vGRV2SlmuyfEicT2S0983ORIovSawibWtFbicDYXia8PP48uUVW7oTnv35SFk/640?wx_fmt=png&from=appmsg#imgIndex=3)

用这把尺子量一量
--------

有了这个定义，再看市场上那些叫 "FDE" 的东西，就很清楚了。

McKinsey 在招 "Principal Forward Deployment Engineer"。EY 在英国推出了 FDE 岗位。Accenture 跟 Microsoft、ServiceNow 合作搞 "Forward Deployed Engineering Program"。这些公司有自己的平台产品吗？没有。他们在做的事情是帮客户用别人的工具做 AI 转型。产物属于客户，不会回流到任何平台。每个项目从头来，线性增长。

这就是咨询。或者更准确地说，是三种传统角色穿上了新衣服：

*   **咨询型：** 帮客户规划 "你应该用 AI 做什么"，组合市场上的工具出方案。产出是方案和建议。

*   **实施型：** 帮客户把某个 AI 产品部署上线、配好、跑通。产出是一个配置好的系统。

*   **SE 换标签型：** Pragmatic Engineer 的 Gergely Orosz 观察到，大量公司只是把现有的 Solutions Engineer 或 Solutions Architect 改了个头衔叫 FDE，工作内容没有任何变化。


三种都不是 FDE。因为产物都不回流到任何平台。做完这个客户，下一个客户从零开始。

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOxKCF9S8Rh24x4TlTJIZKJrQt3XFcFXJo3M4QibYZYA3GxyhXGD46TLJgIibGqlmEZQTlCLhuDgFxX4yv3CwMfklEsRTicOvntrlE/640?wx_fmt=png&from=appmsg#imgIndex=4)

a16z 合伙人 Marc Andrusko 的判断很直接：如果你只复制了嵌入式工程师的部分，却没有底下的平台在支撑，最终你不是 "某领域的 Palantir"，你只是 "某领域的 Accenture，换了个更好看的前端界面"。

Flybridge 的分析更具体。他们跟 Palantir 现任 FDE Brian Keohane 做了一次内部讨论后判断，**绝大多数 startup 在错误地使用 FDE 这个角色**。两大典型失败模式：

1.  **把 FDE 派到低价值客户。** 一个 FDE 全年成本 22 万到 40 万美元。如果他大部分时间花在 10 万美元以下的合同上，单位经济直接崩溃。这种活，一个 Solutions Engineer 用三分之一的成本就能干。

2.  **用 FDE 弥补弱平台。** 当核心产品不够模块化的时候，FDE 会被拉去给每个客户做一次性系统。没有任何东西能被复用。时间一长，公司积累了一堆碎片化的部署，悄无声息地变成了一家高投入、低利润的服务公司。


所以那些说 "FDE 不过是 consulting" 的人，没说错。他们看到的就是这种。问题不在于他们的判断，在于他们把所有叫 FDE 的东西都当成了同一种东西。

**真正的 FDE，背后有一个平台。**

接下来我们详细看看，真正的 FDE 是怎么运作的。

* * *

FDE 是怎么运作的
----------

### 起源：Palantir 的 Echo、Delta 和 Dev

FDE 这个模式是 Palantir 发明的。但 FDE 不是一个孤立的岗位，而是一整套协作方式。Palantir 内部有三个核心角色，共同构成了这套体系：

**Echo**（回声团队）是嵌入式分析师。他们来自客户所在的领域：前陆军军官、医疗行业老兵、金融合规专家。但 Bob McGrew 说了一个关键条件：他们必须是**叛逆者**，或者用 Palantir 联合创始人 Shyam Sankar 的话说，是 heretic（异端）。他们理解这个行业现在是怎么运作的，但同时认为现状不够好。如果一个 Echo 觉得 "这个行业挺好的"，他永远找不到那个让新软件必须存在的 3x-10x 的改变机会。

**Delta**（三角洲团队）是前线工程师，也就是狭义上的 FDE。他们的核心能力是快速做原型。Flybridge 与 Palantir 现任 FDE Brian Keohane 的讨论得出一个关键结论："错误的 Delta 画像是匠人"（The wrong profile for a Delta would be someone who's a craftsman）。追求完美抽象、想写能维护十二年的代码，那不是这个角色的任务。Palantir 内部一位 FDE 负责人 Katherine 用了另一个说法：" 我们更像是一个艺术家社群 "（artists' colony）。每个 FDE 的核心能力不同，但共同点是高用户同理心、对商业战略的理解力和创造性解题能力。你要的不是完美代码，而是一个能在客户现场用粗糙但管用的方案快速交付结果的人。

**Dev**（平台工程师）是留在总部的人。他们负责开发和维护 Palantir 的平台产品（Foundry、Gotham）。他们不去客户现场，但他们的工作直接决定了 FDE 在前线有多少产品杠杆可用。Palantir 官方博客对这两种工程师有一个很简洁的总结：Dev 的视角是 "一个能力，多个客户"；Delta 的视角是 "一个客户，多种能力"。

三个角色的关系是：Echo 在客户现场找到正确的问题，Delta 快速构建解决方案，Dev 把前线验证过的方案抽象为平台能力，让下一个 Delta 去下一个客户时有更强的武器。这是一个完整的循环，不是三个独立的岗位。

![](https://mmecoa.qpic.cn/sz_mmecoa_png/afd2uiaVAOOw7WboGdkibK24nJ3U3eG3QqcHQL1qhfQKEb4iczfl4IkkCmKVyyFJ5iaguAjnxCME0OCHnUaEKIpicIRHhSd7EU7ebqPJLEW7rxicQ/640?wx_fmt=png&from=appmsg#imgIndex=5)

Flybridge 的分析指出，这套角色组合要求的核心特质是 "founder 级别的 ownership"，把客户的工作流当自己的产品。这也是为什么 Palantir 出了那么多 startup founder：Kalshi 的 Tarek Mansour、Hex 的 Glen Takahashi、Sourcegraph 的 Quinn Slack、Anduril 的 Matt Grimm、Fern 的 Deep Singhvi，都是前 FDE。

### FDE 每天在做什么

说了这么多角色定义，FDE 在客户现场每天具体干什么活？

Palantir 的一位 FDSE 在官方博客里列过他的典型技术问题：

*   怎么构建、扩展和维护一个 TB 级的数据管道，给关键任务的运营工作流提供数据？

*   怎么根据客户独特的合规要求，配置平台的数据访问权限和工作流控制？方案是否灵活到能承受未来的变化？

*   怎么为一个非技术背景的客户设计一个可视化工作流，让他们能跟高噪声数据交互？怎么把这个功能泛化，让其他 FDE 和客户也能受益？

*   生产环境出了故障，怎么排查根因、部署修复、监控稳定性，同时协调产品团队、部署团队和客户之间的沟通？


注意最后两个问题里反复出现的一个词：**"泛化"**。这就是 FDE 和普通实施工程师的区别。实施工程师解决完问题就完了，FDE 解决完问题之后还要想："这个方案能不能变成平台的一部分，让下一个人不用重来？"

他自己也说了跟咨询师的核心区别：咨询师通常做一次性的分析和建议，Palantir 的 FDE 是跟客户一起构建长期方案，让客户能持续自我改进。而且 FDE 做的工程和技术工作的深度，在传统咨询中是很少见的。

### 什么样的人适合做 FDE

从上面的描述你大概能感觉到，FDE 需要的不是一般的工程师画像。Flybridge 的 Daniel 跟 Palantir 现任 FDE Brian Keohane 讨论后，总结了一个相当一致的人才画像：

*   **极强的 ownership 和韧性。** 这是跟成功关联度最高的特质。他们像 founder 一样对结果负责，把客户的工作流当自己的产品，不惜一切让生产系统跑起来。

*   **偏好行动而非分析。** 先交付一个粗糙但管用的 "碎石路" 方案，快速创造价值，而不是分析到死。

*   **对模糊性感到自在。** 客户说不清需求，环境混乱，真正的问题藏在表面之下。FDE 在这种环境里如鱼得水。

*   **技术 + 沟通双能力。** 能写生产级代码，也能给 CFO 讲架构决策。这个组合极其稀缺。


简单说：像 founder，不像 craftsman。

### 飞轮：从碎石路到铺好的路

FDE 在客户现场做出来的东西，在 Palantir 内部叫 "碎石路"（gravel road）。粗糙、直接、只为这一个客户解决这一个问题。这完全合理，也是 FDE 应该做的事情。

但碎石路不能直接搬进产品。产品团队的工作是把碎石路变成 "铺好的路"（paved road），一条不只经过这一个客户、还能经过后面一堆客户的路。

这就是飞轮：

1.  FDE 在客户 A 的现场发现了一个需求，做了一个碎石路方案

2.  带回总部，产品团队问："这个问题的通用版本是什么？"

3.  拉来客户 B、C 的 FDE 一起讨论，确保通用版本对他们也管用

4.  产品团队构建通用能力，纳入平台

5.  下一个 FDE 去客户 D 的时候，可以直接用这个能力，不用从头来


Palantir 最著名的产品能力 Ontology（本体）就是这么来的。最开始，每个客户都有自己的数据库：人、资金、船只各一张表。部署到第二个客户的时候，表结构就对不上了。产品团队把它抽象成了 "objects + properties + links" 的通用模型，让 FDE 按客户自行定义具体的对象类型。这个抽象化的过程，就是碎石路变成铺好的路。

这个飞轮里有一个容易被忽略的点：**产品团队的用户不只是最终客户，还有 FDE 本身**。产品要给 FDE 提供杠杆，让他们能用更少的 effort 交付更多的价值。如果产品做得对，FDE 应该会主动选择用产品的通用能力，而不是自己 hack 一个一次性方案。如果 FDE 不愿意用你的产品，大概率是产品做错了。Thomas Otter 甚至预判："明年最酷的岗位将是 platform product manager"。飞轮能不能转，关键不在 FDE，而在平台产品团队。

a16z 的 Marc Andrusko 用了一个好比喻：把 FDE 当作**脚手架（scaffolding），而不是建筑本身**。脚手架是临时的，是为了让建筑立起来。建筑立起来之后，脚手架要拆掉。如果你的 "脚手架" 变成了永久结构，你建的就不是产品公司，是服务公司。

![](https://mmecoa.qpic.cn/sz_mmecoa_png/afd2uiaVAOOy0YtgiabMTbrryp8uMMX4vB4ZYl5oEcCTv11LPNXuFO4Kv772uyqda62vNFzEhzvBxwqML0mIhgu1FlrV7OOiazy8uRj1ich81lo/640?wx_fmt=png&from=appmsg#imgIndex=6)

当然，这个飞轮的效率不是文章暗示的那么理想。即使是 Palantir，professional services 收入占比多年来也没有显著下降。飞轮在转，但转得不快。对大多数公司来说，飞轮从启动到产生可见效果需要 1-3 年，这段时间里你看起来就是一家咨询公司。能不能坚持下去，取决于你对 "过渡态" 的信念和资本的耐心。

### 防止退化为咨询

保持飞轮转下去需要极强的组织纪律。Marc Andrusko 说过："The willingness to say'no'to custom work is often what separates a product company from a services company that happens to write code." 拒绝定制的意愿，是产品公司和 "恰好会写代码的服务公司" 之间的分水岭。

比 "沦为咨询" 更容易发生的失败是：**你在现场做了客户要求你做的东西，而不是客户真正需要的东西。** 这两个东西经常不一样。"客户" 不是一个人，是一整个组织。你日常打交道的可能是 CIO 下面好几级的某个中层。他让你解决的往往是对他来说最省事的问题，而不是对整个组织最有价值的问题。

FDE 的纪律是：

*   **做客户需要的，而不是客户要求的。** 这两者的区别是 FDE 和外包的分水岭。

*   **追踪产品杠杆。** FDE 是越来越多地用产品解决问题，还是越来越靠人力？前者是 FDE，后者是咨询。

*   **内部市场检验。** 如果产品做对了，FDE 应该主动选择用产品的通用能力。如果 FDE 宁愿自己 hack，说明产品没做对。


Everest Group 的分析给了一个更长期的视角：Palantir 的目标不是让 FDE 永远驻扎在客户现场，而是帮客户建立 Center of Excellence（卓越中心），让客户最终能自主运营。FDE 的存在应该是一个过渡态，不是终态。

* * *

Palantir 是启发，不是手册
-----------------

如果你听过 Bob McGrew 在 YC Lightcone Podcast 上的那期访谈（"The FDE Playbook for AI Startups"，2025 年 9 月），你会发现他讲了非常多的东西。但如果仔细听，会发现他讲的内容其实有两层，需要分开。

**FDE 本身**是一种产品研发方法：

*   Echo + Delta 团队结构

*   碎石路 → 产品团队抽象 → 铺好的路

*   产物回流平台的飞轮


**Palantir 的 GTM 策略**是另一套东西，经常跟 FDE 一起出现，但不是 FDE 的定义：

*   **Outcome-based pricing**：按结果定价，而不是按 seat 或 usage

*   **Land and expand**：先解决一个问题，再扩展到更多问题，合同越做越大

*   **Demo-driven development**：用一个核心 demo 驱动产品迭代

*   **解决 CEO 的 top 5 问题**：确保有高层 sponsor 来扫清组织阻力

*   **早期承担所有风险**："你付钱，当它 work 的时候"


这两个维度是独立的。你可以用 FDE 但不按 outcome 定价（Stripe 的 FDA 就是内部角色，没有定价问题），也可以按 outcome 定价但不用 FDE。

VC Thomas Otter 说得好："Palantir should be seen as an inspiration, rather than a rule or playbook." Palantir 是启发，不是可以照抄的手册。a16z 的 Marc Andrusko 更明确：Palantirization 有四层含义（嵌入式工程、集成平台、高接触 GTM、按结果定价），FDE 只是其中之一。把四层混在一起当作一个东西来模仿，就是大部分 startup 踩坑的原因。

Palantir 不只是 "软件公司 + 咨询"。它是 "软件公司 + 咨询 + 政治工程 + 极其耐心的资本"。你可以学它的 FDE 方法论，但你不需要复制它的 GTM。

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOxqxle9zGzZu3yNyHSHsNlanibTv9ru8bZVQOqn14uicmHRficcibzMZ8Im3kPMLHDkiaxYuOrjR3BgibcqAriaP38Evg5KNG6G6M2cg0/640?wx_fmt=png&from=appmsg#imgIndex=7)

Marc Andrusko 还给了一组压力测试问题，用来判断一家自称 "Palantir for X" 的公司到底在做什么：

1.  给我看你的平台边界在哪里。共享产品止于何处？定制从哪里开始？

2.  走一遍部署时间线。从签约到生产环境要多少 engineer-months？

3.  第三年的利润率是什么样的？成熟客户的 FDE 投入是否在下降？

4.  如果明年签 50 个客户，什么会先崩？

5.  你如何决定**不做**定制？拒绝客户需求的能力，是产品公司和服务公司的分水岭。


这五个问题比任何定义都更实用。如果答不上来，大概率不是在做 FDE。

![](https://mmecoa.qpic.cn/sz_mmecoa_png/afd2uiaVAOOzXBCtFtpxNOfj5hfRAt8uibxcECH3DZ7fvYq3oiaOR30WwYibFDdfib04JnsxoibeOykNhKYMcZGxYAmEaRTuMhu8aVKzUWjbeK680/640?wx_fmt=png&from=appmsg#imgIndex=8)

Everest Group 的分析说得更直接：Palantir 同时做到了三件事，大多数公司只能做到一两件。第一，它有一个真正的集成平台。第二，它能把顶尖工程师派到客户现场。第三，它的系统从第一天就跑在客户最要命的业务上，反恐、军事指挥、疫情追踪，出了问题是要死人的。这种信任不是靠 pitch deck 建立的，是靠在高压环境下持续交付建立的。

但这不意味着 FDE 方法论本身不可学。Palantir 难复制，是因为这三件事要同时做到。FDE 可以学，是因为核心的东西是可迁移的：有平台、嵌入客户、产物回流、飞轮转起来。这些不需要你服务 CIA，也不需要你有二十年的政治工程经验。

* * *

为什么 AI 时代天然适合 FDE
-----------------

前面我们花了大量篇幅定义 FDE，区分真假，拆解运作方式。但有一个问题还没回答：FDE 这个模式是 Palantir 在 2010 年发明的，为什么到了 2026 年突然所有 AI 公司都在做？

答案不是 "因为 Palantir 成功了所以大家抄"。如果只是抄，前面说了，绝大多数会抄成咨询。

答案是：**AI 这个品类本身的特性，让 FDE 成为了一种结构性需要。**

### AI 是全新品类，价值由使用者定义

传统 SaaS 替换的是已有产品。你做一个更好的 CRM 来替代 Salesforce，市场长什么样，大家都知道。你可以坐在办公室里研究竞品，做出一个更好的版本，然后卖出去。

AI agent 不是在替换任何东西。它是一个全新品类，没有 incumbent 可以参照。Bob McGrew 说得很直接："构建 AI agent" 这件事本身可能包含很多完全不同的东西，我们现在还不知道那些东西是什么。五年后回头看，可能 "AI agent" 这个词根本不存在了。

但 AI 产品跟传统软件的区别不止 "没有 incumbent" 这一层。还有一个更深的特性：**AI 产品的价值往往不是产品团队定义的，是使用者发现的。**

传统软件的逻辑是：产品团队设计功能 → 用户按设计使用 → 价值实现。路径确定。AI 产品反过来了。产品团队提供一个足够开放的能力，但真正的 golden case 是用户自己从实践中 "挖" 出来的。ChatGPT 发布时 OpenAI 工程师自己都没预料到它会成功，结果用户拿它写辞职信、当心理咨询师，5 天 100 万用户。Claude Code 设计目标是 "给开发者用的编程工具"，结果黑客松冠军是一个加州律师，季军是一个比利时心脏科医生。

这意味着 AI 产品天然有一个**价值发现的瓶颈**。能力可能很强，但如果没人找到 killer use case，能力就是空转的。

在个人用户场景下，这个瓶颈可以靠自然传播解决：有人发现了一个用法，发到社交媒体，其他人跟进。但在企业场景下不行。企业有合规要求、有遗留系统、有组织惯性，不会有人在 Twitter 上发帖说 "我发现我们银行的反洗钱流程可以用 Claude 压缩 90%"。你需要有人去现场帮他们发现。

这个人就是 FDE。他的角色不只是 "去客户现场搞清楚需求"，而是**主动制造 golden case**。

Stripe 的 Forward Deployed AI Accelerator（FDA）是最好的企业端案例。Stripe 发现自己的 marketer 已经在自发地用 AI 做出了一些东西：自己搭数据看板，创建能把多天流程压缩的 agent。FDA 团队的工作不是从零开始教人用 AI，而是把这些已经被发现的 golden case 系统化地推广到整个营销组织。他们的成功标准是 "你永久改变了多少个工作流"。

价值是 marketer 自己先发现的，FDA 是去系统化推广已被验证的用法。这跟传统的 "产品团队设计功能然后推给用户" 完全是反过来的。

Anthropic + FIS 的合作也是同一个逻辑。就在这个月（2026 年 5 月），Anthropic 把 FDE 直接嵌入了 FIS，合作开发反洗钱 AI Agent，目标是把调查时间从数小时压缩到数分钟。模型能力（Claude）是现成的，金融合规知识在 FIS 那边，但把两者结合起来、在受监管环境中跑通，需要有人坐在中间。FIS 的 Ferris 说了一句很直接的话："You're not going to innovate around us." 你绕不过我们。

### 能力远超采用，FDE 填的是这个 gap

AI 的能力进步极快，但采用率远远跟不上。Bob McGrew 举了一个例子：你坐在 Uber 里，无人驾驶，没人开车。你的反应是什么？"唉，怎么堵车这么严重。" 技术到了科幻的程度，体验变得越来越平淡。

**AI 需要被采用。** 它不会自动发生。你需要人去搞清楚怎么用它，需要重新设计工作流程，需要说服整个组织接受改变。这些事情不会因为模型更强就自动解决。FDE 填的就是这个 gap。市场数据也在验证这一点：Paraform 的分析显示，FDE 岗位在 2025 年 1-9 月增长了 800%，但合格候选人池只增长了约 50%。59% 的 FDE 招聘公司还处于 Seed 到 Series A 阶段，这些公司连产品都没完全定型，更需要 FDE 去前线探索。

![](https://mmecoa.qpic.cn/mmecoa_png/afd2uiaVAOOyicRU6Jxywgkb3lwQU6UFofFvvk74p9ch2icWnqZgrxApfyA4mjQX6jUGjfFuIjicU8FQNXGpwPxEyRMbFHicROKC61Iib1mDIXWiaU/640?wx_fmt=png&from=appmsg#imgIndex=9)

a16z 合伙人 Joe Schmidt 的类比很到位：企业买 AI 就像你奶奶拿到一台 iPhone，她想用，但需要你帮她设置好。在 platform shift（平台转型期）期间，implementation-heavy 的模式不是缺陷，而是特征。Salesforce IPO 前烧掉了 5200 万美元才产生 2200 万美元收入。但正因为它把复杂实施做到位了，现在市值 2540 亿美元。

Joe Schmidt 还说了一个更深层的判断：软件不再是辅助工人的工具，**软件本身就是工人。** 但软件要成为合格的 "工人"，需要 FDE 帮企业重新设计岗位职能和流程。a16z 的 Alex Rampell 把这个拉到了市场规模的层面：企业软件市场年支出 3000 亿美元，但白领劳动力市场是数万亿美元。FDE 做的事情不是在 3000 亿的市场里分蛋糕，而是在撬动万亿级的新市场。谁先通过 FDE 占领工作流，谁就拥有下一代 system of work 的定义权。

### 窗口期

最后说一个不那么乐观的判断。

Sequoia 合伙人 Julien Bek 提出了一个 Intelligence vs Judgement 的框架。写代码是 intelligence（可编码、可规则化的认知工作），决定下一步做什么是 judgement（需要经验和品味的决策）。AI 正在快速接管 intelligence 型的工作，但 judgement 目前还需要人类。

FDE 目前做的大量工作属于 judgement：判断客户真正需要什么、决定怎么设计工作流、在模糊的环境里定义问题。Sequoia 的框架还有一层：copilot（副驾驶）卖的是工具，autopilot（自动驾驶）卖的是工作成果。FDE 本质上是一种 "人类 copilot"，帮助 AI 产品在客户那里落地。但最终目标是让产品达到 autopilot 状态，不再需要 FDE。

Julien Bek 的关键判断是：**"Today's judgement will become tomorrow's intelligence."** 今天需要 judgement 的事，随着 AI 系统积累足够多的数据，最终也会变成 intelligence。这个窗口会收缩。

所以 FDE 不是一个永恒的角色。它是一个窗口期的角色。但窗口期内的卡位，决定了谁拥有工作流的定义权。

* * *

展望与终局
-----

大部分 AI 项目失败的原因不是模型不好，而是它没法跟客户的遗留系统对话、处理不了 SSO 认证、满足不了数据驻留要求。在沙盒里让 demo 跑起来只占 FDE 工作的 20%，另外 80% 是在企业的现实环境中穿行。这堵 "集成之墙"，是 FDE 存在的直接原因。

但这堵墙不会永远在。

Gartner 分析师 Alex Coqueiro 预测，到 2028 年，70% 的企业将被迫放弃由 FDE 主导的 AI 项目。原因是高成本和内部能力不足。他给了一个判断标准：

> _"如果 FDE 在连续部署中的投入保持不变，这就是一个信号：这段合作产生的是依赖，而非能力。"_

这个标准跟我们前面说的试金石是一回事：第 10 个客户跟第 1 个客户花的精力一样多吗？如果是，飞轮没在转，你做的是咨询。

Thomas Otter 的警告也值得听："对很多公司来说，FDE 不过是一种用来吸引技术人才进入服务岗的营销手段。炒作推高了薪资，但最终很可能让这些 FDE 们大失所望。" 如果你加入的公司没有真正的平台，你做的就不是产品发现，而是项目交付。

70% 被放弃，也意味着 30% 活下来了。活下来的那些，会是真正用 FDE 方法论建起了平台飞轮的公司。它们在窗口期内卡住了位，拥有了工作流的定义权。

Sequoia 的 Julien Bek 给出了一个终局判断：

> _"The next $1T company will be a software company masquerading as a services firm."_

下一个万亿美元公司，将是一家伪装成服务公司的软件公司。

这句话精确地描述了 FDE 模式的终局形态：从外面看，它在做服务（嵌入客户、解决问题、交付结果）；从里面看，它在做产品（每一次服务都让平台更强）。当平台足够强大、用户可以自己跑起来的那一天，FDE 作为角色会消失。但 FDE 作为方法论留下了一个东西：一个被无数次客户部署打磨过的、真正好用的平台。

Palantir 是启发，不是手册。FDE 的定义是清晰的：有平台、嵌入客户、产品发现、产物回流。满足这四条的，不管你叫它什么名字，都在做 FDE。不满足的，不管你 title 写什么，都不是。

* * *

信息来源
----

**访谈与播客**

*   Bob McGrew, "The FDE Playbook for AI Startups", YC Lightcone Podcast, 2025.09 — ycombinator.com


**一手文献**

*   OpenAI, "OpenAI Launches the Deployment Company", 2026.05.11 — openai.com

*   Palantir Blog, "A Day in the Life of a Palantir Forward Deployed Software Engineer" — blog.palantir.com

*   Palantir Blog, "Dev versus Delta: Demystifying Engineering Roles at Palantir" — blog.palantir.com

*   Stripe, "Forward Deployed AI Accelerator, Marketing" Job Listing — stripe.com


**VC 与行业分析**

*   Thomas Otter, "On the Forward Deployed Engineer, Product Led Growth and genuine adoption", 2025.12 — thomasotter.substack.com

*   Daniel (Flybridge), "Why 95%+ of Startups Get the Forward Deployed Engineer Role Completely Wrong", 2025.12 — danielp1.substack.com

*   Joe Schmidt (a16z), "Trading Margin for Moat", 2025.06 — a16z.com

*   Marc Andrusko (a16z), "The Palantirization of Everything", 2026.01 — a16z.com

*   Alex Rampell (a16z), "AI Turns Capital to Labor", 2024.08 — a16z.com

*   Julien Bek (Sequoia), "Services: The New Software", 2026.03 — sequoiacap.com

*   Everest Group, "Palantir: Inside the Category of One — Forward Deployed Software Engineers" — everestgrp.com


**新闻报道**

*   Nicole Casperson (Forbes), "FIS and Anthropic Signal a New Era of AI Infrastructure in Banking", 2026.05.06 — forbes.com

*   Ella Chakarian (Fast Company), "Google and Box CEOs Say This Is the Most In-Demand Job in Tech", 2026.05.13 — fastcompany.com

*   The New Stack, "Forward Deployed Engineer: OpenAI, Google Cloud Race to Hire", 2026.05.16 — thenewstack.io

*   Computerworld, "Here's One Career Emerging from the AI Shift: Forward Deployed Engineers", 2026.05.15 — computerworld.com

*   CIO.com, "Anthropic's Financial Agents Expose Forward Deployed Engineers as New AI Limiting Factor", 2026.05 — cio.com


**数据与报告**

*   LinkedIn, "Building a Future of Work That Works", Labor Market Report, 2026.01 — LinkedIn Economic Graph (PDF)

*   John Kim (Paraform), "Forward-Deployed Engineers: How Demand Grew 10x in 18 Months", 2026.04 — paraform.com

*   Hashnode, "A Complete 2026 Guide to the Forward Deployed Engineer", 2026.02 — hashnode.com


**其他引用**

*   Gergely Orosz (Pragmatic Engineer), "Forward Deployed Engineering Heats Up Again" — newsletter.pragmaticengineer.com

*   @profitaboveall_ (Twitter/X) — FDE 与 AI consultancy 的关系评论

*   Reddit r/EngineeringManagers — "Forward-Deployed Engineer is just a fancy new name for..."
