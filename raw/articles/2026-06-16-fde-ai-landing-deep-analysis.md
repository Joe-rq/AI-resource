---
title: "FDE：AI 落地时代的前线部署工程师（v4 深读版）"
author: 黄奕彬
source_date: 2026-06-16
source: pdf
source_file: FDE深度信息分析报告v4.pdf
pages: 12
extracted: 2026-06-18 (pdftotext)
---

FDE：AI 落地时代的前线部署工程师
日期：2026-06-16
版本：v4 深读版

作者：黄奕彬
定位：面向组织高层、HR、技术负责人和希望进入 FDE 领域的新人。本版修正 v3 的问题：v3 把证据流
跑通了，但正文停留在框架层；v4 以“为什么这个角色现在出现、它真正改变什么、组织该如何判断、个
人该如何进入”为主线重写。
术语口径：除公司名、产品名、通用缩写和原始资料标题外，本报告采用“中文主词 + 英文括注”的方式处理关
键术语。AI capability overhang 译为“AI 能力悬置（capability overhang）”，指模型能力已经存在，但还没有
被组织流程、工具、治理和人员充分释放。

一页结论
前线部署工程师（Forward Deployed Engineer，FDE）不是一个普通新岗位，也不是旧式咨询、售前或客户
成功换了个名字。更准确地说，它是前沿 AI（frontier AI）公司在企业 AI 落地阶段创造出来的一种“现场工程
组织接口”：一端连接模型、工具、评测（eval）、平台路线图；另一端连接客户的真实工作流、权限、数据、
合规、组织采用和业务指标。
本报告的核心判断是：
1. FDE 的出现，说明企业 AI 的瓶颈已经从“模型有没有能力”转为“组织能否把能力变成日常工作系统”。

OpenAI 自称企业 AI 已经进入 AI 能力悬置（capability overhang）阶段，即模型能力超过多数企业当前使用
能力；DeployCo 的设计就是把模型接入客户数据、工具、控制和业务流程。
2. FDE 的真正价值不是“在客户现场写代码”，而是把一次客户问题翻译成三种资产：可运行系统、可评估证据、
可复用模式。

如果一个 FDE 项目只交付客户定制代码，而没有评测（eval）、复用手册（playbook）、平台反馈（
platform feedback）和可复用组件，它就会退化成高成本专业服务。
3. FDE 是组织能力，不只是岗位说明（JD）。

OpenAI 的 DeployCo、Anthropic 的新企业 AI 服务公司（enterprise AI services company）、
Accenture/Microsoft 和 ServiceNow/Accenture 的 FDE 计划（program）都说明：市场正在把“最后一公里 AI
落地”从零散项目变成可融资、可复制、可扩张的交付系统。
4. 对新人来说，FDE 不是“学会 AI 工具后去客户现场”，而是要训练五类能力：客户工作流建模、AI 系统构建、
评测与治理、跨组织推进、现场经验产品化。
5. 最大的反方风险也很清楚：FDE 可能变成换皮专业服务，留下技术债、客户维护负担和不可复用定制。

因此组织引入类 FDE 能力（FDE-like）时，必须把“可复用资产”和“退出机制”写进项目设计。

读者导航
读者

你最应该关心的问题

先读

组织高层

FDE 是否值得成为组织能力，而不是一阵岗位热词

第 1、2、3、8 节

HR / 组织发展

如何定义、招聘、考核这个角色

第 4、5 节

技术负责人

如何把 FDE 项目管成生产工程，而不是演示（demo）

第 6、7 节

新人 / 转型者

如何建立进入这个领域的能力路径

第9节

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 1 页

读者

你最应该关心的问题

先读

研究者

哪些证据可靠，哪些只能作为线索

第 10、11 节

1. 为什么是现在：FDE 是 AI 能力悬置的组织解法
OpenAI 在 2026 年 4 月的企业 AI（enterprise AI）叙事中提出一个关键判断：AI 模型已经能做的事，超过了
多数企业真实使用的范围。真正的问题不是“模型是否足够强”，而是“如何让模型可信、合规、可控地嵌入日常
工作”。它还明确说，企业现在问的不是如何购买单个副驾驶式工具（copilot），而是如何让 AI 进入整个业务、
成为日常工作的一部分。
这正是 FDE 出现的背景。传统企业 AI 项目常常卡在四个断点：
断点

表面现象

深层原因

试点断点（pilot）

演示好看，上线很慢

演示没有接入真实权限、数据、流程和治理

业务断点

技术团队说能做，业务团队不用

没有把工作流（workflow）重新设计成 AI 可接手的工作单元

信任断点

用户不敢依赖输出

缺评测、回归测试、人工复核和责任边界

复用断点

每个客户都重新做一遍

没有把现场模式沉淀为复用手册、工具和平台反馈

FDE 解决的不是其中某一个断点，而是把四个断点压到同一条交付链里。因此它既不像传统售前，也不像纯
软件工程师；它是一个把客户现场、模型能力、工程系统和产品路线图串起来的角色。
OpenAI 2026 年 5 月发布 DeployCo 更进一步说明了这一点：新公司要把 FDE 嵌入到复杂客户组织中，从价
值诊断、优先工作流选择，到设计、构建、测试、部署生产系统，并连接客户数据、工具、控制和业务流程。
OpenAI 还称将通过收购 Tomoro 带入约 150 名 FDE 和部署专家（deployment specialists），并由 19 家投
资、咨询和系统集成伙伴参与，初始投资超过 40 亿美元。
这意味着：FDE 已经不只是招聘页面上的岗位，而是前沿 AI 公司商业化基础设施的一部分。

2. FDE 的本体：不是“客户现场工程师”，而是“双向翻译器”
如果只把 FDE 理解成“嵌入客户现场写代码的工程师”，仍然太浅。更准确的定义是：
FDE 是把客户工作流翻译成 AI 可交付系统，再把现场经验翻译回产品、研究和平台能力的人。
这个定义包含两个方向。
方向一：客户工作流 -> AI 系统。
客户不会天然提出清晰的 AI 需求。他们提出的是“审批慢”“客服质量不稳”“研究资料太多”“一线员工找不到知识
”“合规审查卡流程”“工程团队被重复任务拖住”。FDE 要把这些含混问题转成：
• 可界定的工作流（workflow）。
• 可调用的数据和工具。
• 可接受的权限边界。
• 可测试的评测。
• 可部署的系统。
• 可观测的采用指标（adoption）。

方向二：现场经验 -> 产品与平台。
FDE 不能只做一个客户的定制项目。OpenAI 岗位页强调把工作模式沉淀为工具（tools）、复用手册（
playbooks）、构件（building blocks），并把现场反馈（field feedback）反馈给研究和产品团队（Research
/ Product）。Anthropic 岗位页也强调把可重复部署模式代码化（codify repeatable deployment patterns），

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 2 页

并把洞见反馈给产品和工程团队（Product / Engineering）。
这就解释了为什么 FDE 比普通专业服务更靠近核心产品：它不只是“帮客户成功”，而是把客户现场变成模型
公司学习企业真实运行状态（enterprise reality）的传感器。

3. OpenAI 与 Anthropic 的差异：同一个 FDE，两个重点
OpenAI 与 Anthropic 的 FDE 岗位说明很像，但重点不同。
维度

OpenAI FDE

Anthropic FDE

组织位置

企业业务模型部署（Model Deployment for Business）

应用 AI（Applied AI）

关键词

研究突破 -> 生产系统（research breakthroughs ->
生产应用（production applications）；MCP 服务器（
production systems）；工作流影响（workflow impact） MCP servers）；子智能体（sub-agents）；智能体技
；评测驱动反馈（eval-driven feedback）
能（agent skills）

经验要求

5+ 年工程或技术部署经验，含客户面对经验

3+ 年技术客户面对经验，或软件工程 + 咨询经验

生产责任

需求发现、范围界定、系统设计、构建、上线推广（
discovery / scoping / system design / build / rollout）

在客户系统内构建 Claude 生产应用（production
applications）

出差

OpenAI 纽约岗位写明最高 50%（up to 50%）

Anthropic 估计 25%

透露出的角色气质

更像“客户现场到产品/研究的双向部署工程师”

更像“应用 AI 中的交付物（artifacts）生产者”

这个差异很重要。OpenAI 的叙事更强调“把研究突破变成生产系统”，并把反馈带回产品和研究；Anthropic 的
叙事更强调“把 Claude 以 MCP、子智能体（sub-agents）、智能体技能（agent skills）等形式嵌入生产工作
流”。前者更像部署公司（deployment company）的前线感知器，后者更像应用 AI 的生产交付单元。
但二者共同指向一个结论：FDE 的产出不是建议书，而是生产交付物（production artifacts）。

4. 组织高层：该不该引入类 FDE 能力
高层不应先问“要不要招 FDE”。更好的问题是：
我们的 AI 价值是否卡在“从模型能力到日常工作系统”的中间地带？
如果答案是肯定，类 FDE 能力才有意义。

4.1 四种引入方式
路径

适合谁

何时不适合

自建 FDE 团队

有强工程底座、明确高价值工作流、愿意沉淀内部平台能
力

AI 场景还停在培训和工具试用

购买厂商/模型公司服务

需要快速切入前沿能力（frontier capability），内部缺少
AI 工程能力

涉及核心业务知识和数据，不愿外部深度进
入

咨询/系统集成伙伴

流程复杂、跨部门多、需要变更管理

只想做单点工具，不需要组织重构

混合模式（Hybrid）

有核心负责人（owner），但需要外部加速和技术迁移

内部没有能接住知识转移的人

4.2 引入前的五个诊断问题
1. 组织是否存在跨系统、跨部门、高频或高价值的工作流？
2. 这些工作流是否已经被现有 SaaS 或自动化工具充分解决？
3. AI 失败会不会带来合规、客户信任、运营或法律风险？
4. 组织是否愿意为评测、权限、安全、回滚和采用付出工程成本？
5. 项目结束后，能否留下可复用手册、组件、数据集或平台能力？

如果第 4、5 个问题答案是否定，FDE 会变成昂贵的演示团队。
FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 3 页

4.3 FDE 项目的成功指标
高层不要只看“上线几个智能体（agent）”。更应该看：
• 关键工作流是否真的被改变。
• 用户是否持续使用，而不是发布周（launch week）试用。
• 评测是否覆盖真实失败模式。
• 人工复核是否从临时救火变成制度设计。
• 项目是否沉淀了下一次可复用的模板、工具和判断。
• 现场经验是否影响了平台路线图或组织流程。

5. HR：如何定义、招聘和评价 FDE
FDE 是复合型岗位，但复合不等于“什么都要”。真正的核心是五个能力束。
能力束

具体表现

面试方式

淘汰信号

生产工程能力

能写、审、上线、排障生产系统

讲一个真实系统的故障、回滚和权衡

只会演示，不理解运行时和边界

AI 系统能力

理解智能体（agent）、检索增强生成（RAG）
、工具调用（tool use）、MCP、评测

设计一个带评测的智能体工作流

只会调模型，不会测模型

客户工作流能力

能从业务语言中抽象流程、约束和指标

给一个含混客户需求，让候选人拆范围（
scope）

只复述客户需求，不能重构问题

跨组织推进

能处理安全、法务、IT、业务、工程的冲突

复盘一次多利益相关方（stakeholder）推
进

把阻力都归咎于“业务不懂技术”

产品化沉淀

能把一次项目变成模板、工具和反馈

要求展示从项目到复用资产的例子

每个项目都重新做一遍

5.1 面试题样例
题一：客户发现（discovery）。
一家大型银行希望用 AI 改善投研资料检索。请候选人列出 10 个必须澄清的问题，并区分哪些是业务问题、
数据问题、权限问题、评测问题和采用问题。
题二：评测设计（eval design）。
给定一个会议纪要智能体，要自动生成摘要、行动项、CRM 更新草稿。请候选人设计测试集、评分标准、人
工复核策略和上线门槛。
题三：失败复盘。
如果智能体在 2% 的高风险情境中幻觉，并且业务方已经依赖它，你会如何分阶段降级、回滚、修复、沟通？
题四：复用手册沉淀（playbook）。
项目交付成功后，你会留下哪些可复用资产？理想答案不只是“文档”，还应包括评测集（eval set）、提示词/
模板（prompt/template）、工具模式（tool schema）、权限模板、部署检查表、用户训练材料和反馈机制。

6. 技术负责人：FDE 项目该如何被工程化管理
FDE 项目不能按普通功能需求管理。它更像“高不确定性系统交付 + 组织采用 + 风险治理”的组合。

6.1 最小交付包
每个 FDE 项目至少要有以下交付物（artifact）：
交付物

作用

工作流地图（Workflow map）

明确 AI 要进入哪个真实工作流，替换或增强哪个步骤

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 4 页

交付物

作用

数据与工具清单（Data and tool inventory）

明确可读/可写的数据、工具、API、权限

风险登记表（Risk register）

列出高风险输出、错误成本和人工复核点

评测集（Eval set）

覆盖常见、边缘、高风险和反例情境

上线推广计划（Rollout plan）

从影子模式（shadow mode）、试点（pilot）、限量发布（limited
release）到全面推广（full rollout）

可观测性计划（Observability plan）

追踪记录（trace）、日志、失败分类、用户反馈、成本

人工复核策略（Human review policy）

哪些动作必须人审，哪些可自动执行

复用手册（Playbook）

下次类似项目如何复用

6.2 技术架构不是重点堆栈，而是责任链
业务工作流
-> 数据与权限
-> 模型 / 智能体 / 工具 / MCP
-> 评测与回归测试
-> 审批与人工复核
-> 生产部署
-> 采用指标
-> 现场反馈
-> 平台 / 产品 / 复用手册

FDE 项目最常见的失败，是只做到中间几步：模型能调用工具、演示能跑，但没有权限边界、评测集、回滚、
用户采用和反馈闭环。

6.3 FDE 项目的技术红线
• 没有评测集，不进入生产。
• 没有明确人工复核策略，不允许写入关键系统。
• 没有追踪记录和失败分类，不允许扩大上线推广。
• 没有回滚策略，不允许接入核心工作流。
• 没有用户采用观测，不算真正上线。

7. 案例深读：哪些材料真正有解释力
7.1 OpenAI DeployCo：把 FDE 从岗位升级成企业部署公司
OpenAI DeployCo 的关键信息不是“融资很多”，而是它给出了 FDE 组织化的模型：
• 它要把 FDE 嵌入复杂客户组织。
• 它从诊断高价值机会开始，而不是从卖工具开始。
• 它选择少数优先工作流。
• 它让 FDE 在客户组织内设计、构建、测试、部署生产系统。
• 它连接客户数据、工具、控制和业务流程。
• 它把 DeployCo 设计成 OpenAI 的延伸，使客户保持与研究、产品和内部部署团队的连接。

这说明 OpenAI 并不把 FDE 视作普通专业服务（professional services），而是视作模型公司学习企业工作流、
沉淀部署模式、扩大采用的组织机器。

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 5 页

但边界也清楚：这是 OpenAI 官方叙事。它证明战略意图强，不证明每个客户都已经获得可审计投资回报（
ROI）。

7.2 Anthropic 企业 AI 服务公司：类 FDE 能力进入中型企业
Anthropic 与 Blackstone、Hellman & Friedman、Goldman Sachs 的新 AI 服务公司，把目标放在中型企业（
mid-sized companies）。Anthropic 说，应用 AI 工程师（Applied AI engineers）会和新公司的工程团队一起
，识别 Claude 最有影响的场景，构建定制解决方案（custom solutions），并长期支持客户。
这补足了 OpenAI DeployCo 的另一面：大型系统集成商覆盖超大型企业，但中型企业同样缺少内部 AI 工程
能力。Anthropic 的判断是，Claude 的企业需求超过单一交付模式的容量，因此需要新的交付能力（delivery
capacity）。
对高层的启发是：类 FDE 能力不只是 AI 实验室（AI lab）招人，而是资本、咨询、系统集成和模型公司共同
争夺“AI 进入真实业务”的通道。

7.3 Accenture / Anthropic：FDE 规模化的咨询版本
Accenture 与 Anthropic 的合作更像“FDE 工业化训练计划”。官方说约 30,000 名 Accenture 专业人员（
Accenture professionals）将接受 Claude 训练，其中包括帮助把 Claude 嵌入客户环境的前线部署/再造部署
工程师（forward deployed / reinvention deployed engineers）。
这条线索很有趣，因为它说明 FDE 不一定只由模型公司雇佣。它也可以变成咨询公司的新能力包：用模型公
司的前沿能力，叠加咨询公司的行业知识、变更管理和客户覆盖。
它也带来风险：当 FDE 被规模化培训后，头衔（title）会被稀释。未来市场上可能出现两种 FDE：
• 高密度 FDE：能写生产系统、做评测、沉淀平台模式。
• 低密度 FDE：主要做客户推进、工具培训和项目包装。

HR 和新人都必须识别这一区分。

7.4 Morgan Stanley：为什么评测是 FDE 的硬门槛
Morgan Stanley 是一个很好的类 FDE 案例，不是因为它用了 OpenAI，而是因为它展示了 AI 进入金融工作流
需要什么。
OpenAI 案例页强调 Morgan Stanley 的成功建立在稳健评测框架（robust evaluation framework）上。它们不
是简单把 GPT-4 接入知识库，而是用评测测试真实用例，结合专家反馈改进输出。Morgan Stanley 后续的
Debrief 工具也不是单纯生成会议摘要，而是在客户同意后生成会议记录（notes）、行动项（action items）、
邮件草稿，并保存到 Salesforce，同时保留顾问复核（advisor review）。
这说明 FDE 项目进入金融服务时，关键交付物不是“模型回答得好不好”，而是：
• 是否能访问正确的知识来源。
• 是否能在专家标准下被评测。
• 是否能融入 CRM 和后续工作。
• 是否保留人工审核。
• 是否以合规方式处理客户数据。

这就是为什么技术负责人不能把 FDE 项目当提示词项目（prompt project）。

7.5 Spotify：内部类 FDE 能力可能先出现在工程平台
Spotify 的 Claude / Honk 相关工程材料说明另一条路线：类 FDE 能力不一定先用于外部客户，也可能先用于
内部工程平台。它的价值在于展示编码智能体（coding agent）如何进入开发者工作流，而不是停留在个人工
具。
FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 6 页

这对新人很重要。你不一定能复刻金融或医疗客户现场，但可以用内部开发流程做缩小版 FDE 项目：从一个
具体工程工作流出发，接入代码库、议题（issue）、持续集成（CI）、文档和评审（review）流程，用评测
约束输出，再把成功模式沉淀为工程复用手册。

7.6 失败案例：FDE 的必要性往往由失败证明
OpenAI 谄媚问题回滚（sycophancy rollback）、Google Gemini 图像生成事件（image generation issue）、
Air Canada 聊天机器人仲裁裁决（chatbot tribunal decision）、FTC 对 DoNotPay 的执法（enforcement）这
些都不是 FDE 成功案例，但它们是 FDE 报告里必须出现的反面证据。
它们共同说明：
• AI 输出不是只影响用户体验，也会影响法律责任和组织信任。
• 上线前评测不足，会把模型行为问题放大为公共事件。
• 人工复核和责任边界不是保守主义，而是企业采用的前提。
• 如果没有回滚机制，AI 系统会在组织里变成不可控黑箱。

因此，FDE 的技术价值不是“更快上线”，而是“让可上线变得可信”。

8. 反方论证：FDE 可能只是专业服务的新包装吗
反方观点必须认真对待。媒体和从业者讨论中已经出现批评：FDE 可能只是高薪专业服务，顶尖工程师未必
愿意离开核心产品去做客户定制；客户最终可能接手难维护的技术债。
这个反方观点虽然目前主要来自媒体、访谈和社交线索，不能作为强证据，但它指出了 FDE 的真实风险。

8.1 FDE 退化的四种路径
退化路径

表现

预防机制

定制外包化

每个客户都做一套，无法复用

强制沉淀复用手册、组件、模板

售前化

只做演示和高管展示

成功指标（success metric）必须绑定生产采用（production adoption）

顾问化

输出建议多，代码和系统少

要求生产交付物（production artifact）和运行证据

平台脱节

现场经验不回流产品

设定现场反馈评审（field feedback review）和产品路线图入口

8.2 判断 FDE 是否有真实价值的三条线
1. 复用率。

一个 FDE 项目完成后，下一次类似项目是否更快？是否留下了评测集、工具、模板、权限模型和培训材料？
2. 采用率。

用户是否在日常工作中持续使用？还是只在发布会上试用？
3. 反馈率。

现场发现的问题是否进入产品、模型、平台和治理路线图？
没有这三条线，FDE 就只是昂贵服务。

9. 新人路径：从“会 AI”到“能部署 AI”
FDE 新人最容易犯的错，是把能力建设等同于学习模型 API、RAG、智能体框架。真正的路径应按作品集组
织。

9.1 三个必做作品
FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 7 页

作品一：高约束知识工作流智能体（agent）。
选一个真实领域，例如合同审查、投研问答、客服质检、医疗文档、物流异常处理。产出必须包括：
• 工作流地图（workflow map）。
• 数据源和权限说明。
• 智能体/工具（agent/tool）设计。
• 评测集。
• 错误案例。
• 人工复核策略。
• 上线推广计划。

作品二：MCP / 工具集成（tool integration）项目。
不要只调用一个 API。要展示：
• 工具模式（schema）。
• 权限边界。
• 可观测日志。
• 异常处理。
• 回滚策略。
• 安全风险说明。

作品三：从现场到复用手册（field-to-playbook）项目。
找一个真实用户或团队，观察他们如何工作，做一个缩小版 AI 改造，然后写出：
• 原工作流。
• AI 后工作流。
• 用户采用阻力。
• 评测指标。
• 复用模板。
• 下一次如何更快交付。

9.2 适合转 FDE 的背景
背景

优势

需要补

后端 / 全栈工程师

生产系统能力

客户发现、业务语言、评测

解决方案架构师

客户和架构能力

代码所有权（ownership）、模型评测

产品经理 / 技术 PM

工作流和推进能力

工程实现和安全边界

数据 / ML 工程师

模型和数据理解

工具集成、客户交付

咨询顾问

组织和行业理解

可运行系统、代码和评测

9.3 180 天训练路线
时间

目标

产出

1-30 天

熟悉大型语言模型应用（LLM app）、RAG、 一个可运行工具调用演示
工具调用、智能体基础

31-60 天

建立评测思维

一个小型评测框架（eval harness），含失败样本

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 8 页

时间

目标

产出

61-90 天

接入真实工作流

一个带权限、日志、回滚的业务智能体

91-120 天

做用户采用

找 3-5 个真实用户试用，记录阻力

121-150 天

做治理和安全

增加人工复核、风险登记、审计日志

151-180 天

做复用手册

把项目沉淀成模板、文档和复用组件

新人能不能进入 FDE，不看他会不会说“智能体式 AI（Agentic AI）”，而看他能否把一个模糊业务问题变成可
运行、可评估、可采用、可复用的系统。

10. 中国语境：有 FDE 信号，但不要急着套同名岗位市场
本地资料库中最强的国内锚点是字节跳动火山方舟相关岗位，标题直接使用前线部署工程师（Forward
Deployed Engineer，FDE），并要求面向行业头部客户、理解业务场景、识别流程痛点、把挑战转成可落地
AI 技术方案。
但更多国内信号并不叫 FDE，而叫：
• AI 智能体（AI Agent）产品解决方案架构师。
• AI 产品架构师。
• 大模型专家服务。
• AI 解决方案架构师。
• 企业智能体平台交付。
• 从概念验证到生产（POC-to-production）平台或服务。

这说明中国语境中更稳的说法是“类 FDE 能力栈”，而不是“FDE 岗位市场已经成熟”。
国内组织还存在一个更复杂的问题：售前、方案、项目交付、产品迭代和平台运营经常揉在同一个岗位里。因
此写报告时必须拆开能力：
• 谁负责客户发现？
• 谁写生产系统？
• 谁做评测和安全？
• 谁推动采用？
• 谁把项目沉淀回平台？

只有这些问题清楚，类 FDE 才不是新瓶装旧酒。

11. 证据可靠性：哪些能用，哪些只能发现线索
来源

本报告用法

可靠性边界

OpenAI / Anthropic 官方岗位页

定义角色职责、能力、薪酬/年限/出差等公开
要求

不能证明真实日常、团队规模或长期稳
定性

OpenAI DeployCo / Anthropic 服务公司公告

证明组织化部署战略

不能证明客户投资回报

Accenture / Microsoft / ServiceNow / Anthropic 合
作公告

证明类 FDE 动作（motion）向伙伴生态扩散

仍是供给侧叙事

Morgan Stanley / BBVA / Spotify 客户材料

说明真实工作流和采用细节

仍可能选择性呈现

GitHub / docs / SDK

说明可实现路径

不能证明业务有效

X.com / YouTube / 媒体

发现人物、反方观点、热度和待查线索

不进入主结论

失败案例 / 监管材料

说明风险机制和治理需求

不是 FDE 有效性的直接证明

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 9 页

12. 本报告的三个“内行应该会点头”的洞见
洞见一：FDE 的核心不是“更懂客户的工程师”，而是“把客户现场变成模型公司学习系统
的一部分”。
这解释了为什么 FDE 靠近产品（Product）、研究（Research）、治理风险合规（GRC）、安全（Security）
、合作伙伴（Partnerships），而不是只在销售（Sales）或客户成功（Customer Success）下。

洞见二：DeployCo / AI 服务公司的本质不是服务公司，而是前沿 AI 的经济扩散机制。
模型公司如果只卖 API，会被客户的组织摩擦挡住；如果只做产品，会被复杂行业需求拖慢；如果有类 FDE
组织，就能把客户工作流转成可复制部署模式。

洞见三：FDE 的成败不在第一批客户，而在第二批客户是否更快。
如果第二批客户仍然从零开始，说明 FDE 没有产品化；如果第二批客户复用了评测、工具、权限模板和复用
手册，FDE 才开始变成组织资产。

13. 必须补深后的证据状态
本轮已经对 v4 中列出的四类深证据做了第一轮补强。最重要的变化不是材料变多，而是证据状态变清楚了：
哪些能进入主结论，哪些只能作为线索，哪些必须等登录态补取。

13.1 YouTube / 访谈文字稿：已定位，待授权补字幕
已定位 5 个高相关视频，包括 Colin Jarvis 的 Altimeter 访谈、Bob McGrew 的 YC FDE Playbook、Inside
OpenAI Enterprise 等。但 YouTube 字幕抓取被反爬拦截，使用本机 Chrome cookies 仍未成功。因此本报告
不能把视频内容写成强证据，只能使用公开可访问的播客摘要（Podcast summary）、媒体报道和 LinkedIn
转述作为线索。
已经可用的访谈线索是：Colin Jarvis 访谈的公开摘要和二级转述共同指向一个关键机制，即 FDE 大量工作并
不只是“接 MCP 或接工具”，而是在原始数据和业务逻辑之间建立一个翻译层，让模型知道数据是什么意思、
动作边界在哪里、业务规则如何进入推理。这个判断很有解释力，但需要拿到原始字幕后才能写成强结论。

13.2 X.com 具名线索：已建清单，暂不进主结论
X.com 公开页面返回空内容，只能通过搜索片段看到 Colin Jarvis、Aakash Gupta、中文从业者等关于 FDE
的线索。当前这些都只能算 E 级线索，不能支撑报告判断。下一步要用登录态打开原帖，保存截图、作者身
份、发布时间、上下文和外链。

13.3 客户侧深案例：已补强四条案例线
Morgan Stanley：评测和信任工程。 OpenAI 官方案例显示，Morgan Stanley Wealth Management 的 AI
Assistant 在顾问团队中达到 98%+ 采用，文档访问覆盖从 20% 提升到 80%；案例还强调零数据留存（zero
data retention）和评测框架（eval framework）。Business Insider 对 Colin Jarvis 访谈的转述补了一个关键
细节：技术脚手架只需 6-8 周，但让财务顾问信任、试点、评测和迭代又花了约 4 个月。这说明 FDE 不是“把
系统接上”就结束，而是要把评测、信任和采用做成工程。
BBVA：组织化采用。 OpenAI 官方案例显示，BBVA 有约 100,000 名员工使用 ChatGPT Enterprise，70%+
周活跃使用率（weekly active usage），约每人每周节省 3 小时，员工已创建 20,000+ GPTs，其中约 4,000
个被频繁使用。BBVA 官网的早期扩容新闻则显示，其许可从 3,300 扩到 11,000，当时 83% 许可用户每日使
用。BBVA 的价值不在证明 FDE 岗位，而在证明 AI 落地需要信任（trust）、治理（governance）、结构化
学习（structured learning）、AI 推广者（AI champion）和 AI 达人（AI wizard）这类采用基础设施。

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 10 页

ServiceNow / Accenture：FDE 计划工业化。 两家公司 2026 年宣布 FDE 计划（program），目标是把智能
体式 AI（agentic AI）从企业试点（pilot）推到生产规模化；客户可获得 300+ 预构建 AI 智能体技能（AI
agent skills）和智能体工作流（agentic workflows），AI Control Tower 用于治理、保护和管理 AI 智能体（
AI agents）。这个案例说明 FDE 正从模型公司岗位扩散到平台公司与系统集成商的商业交付方法，但目前仍
是供给侧公告，缺少客户投资回报（ROI）。
Moderna：采用基础设施和人审治理。 Moderna 不是 FDE 案例，但它解释了组织采用怎么发生。OpenAI 官
方案例显示，Moderna 的 mChat 采用率超过 80%；ChatGPT Enterprise 两个月内产生 750 个 GPTs，40%
周活跃用户（weekly active users）创建 GPT；Dose ID 用于临床数据分析时保留人类主导复核。这说明
FDE 项目如果要变成组织能力，需要办公时间答疑（office hours）、AI 论坛（AI forum）、领导层牵引、用
户自建模板和高风险情境的人审。

13.4 真人内行评审：已形成评审协议，仍需真实评审
下一步应邀请至少一位 7 年以上企业 AI、解决方案、技术交付或工程管理从业者评审。重点不是让对方“背书”
，而是让对方指出：哪些判断有信息增量，哪些只是供应商叙事，哪些招聘建议不可执行，哪些案例还缺真正
的 ROI 或治理证据。

参考来源
• OpenAI FDE 岗位页： https://openai.com/careers/forward-deployed-engineer-%28fde%29-nyc-new-york-cit
y/
• Anthropic FDE Applied AI 岗位页： https://job-boards.greenhouse.io/anthropic/jobs/4985877008
• OpenAI DeployCo 公告： https://openai.com/index/openai-launches-the-deployment-company/
• OpenAI 企业 AI 叙事： https://openai.com/index/next-phase-of-enterprise-ai/
• Anthropic 企业 AI 服务公司： https://www.anthropic.com/news/enterprise-ai-services-company
• Blackstone / Anthropic 企业 AI 服务公司： https://www.blackstone.com/news/press/anthropic-partners-withblackstone-hellman-friedman-and-goldman-sachs-to-launch-enterprise-ai-services-firm/
• Accenture / Anthropic 合作： https://www.anthropic.com/news/anthropic-accenture-partnership
• Accenture / Microsoft FDE 实践： https://newsroom.accenture.com/news/2026/accenture-launches-microso
ft-forward-deployed-engineering-practice-to-help-organizations-scale-ai-across-the-enterprise
• ServiceNow / Accenture FDE 计划： https://newsroom.accenture.com/news/2026/servicenow-and-accentur
e-launch-forward-deployed-engineering-program-to-scale-agentic-ai-across-the-enterprise
• Accenture 再造部署工程： https://www.accenture.com/us-en/services/cloud/application-transformation/reinv
ention-deployed-engineering
• Morgan Stanley / OpenAI 评测： https://openai.com/index/morgan-stanley/
• Business Insider / Colin Jarvis 访谈转述： https://www.businessinsider.com/openai-forward-deployed-engin
eer-ai-adoption-colin-jarvis-2025-11
• Morgan Stanley Debrief： https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-lau
nch
• Morgan Stanley OpenAI 里程碑： https://www.morganstanley.com/press-releases/key-milestone-in-innovati
on-journey-with-openai
• BBVA / OpenAI 案例： https://openai.com/index/bbva/
• BBVA 扩展 ChatGPT Enterprise 许可： https://www.bbva.com/en/innovation/bbva-expands-its-agreementwith-openai-to-11000-chatgpt-licences-for-the-banks-employees/
• Moderna / OpenAI 案例： https://openai.com/index/moderna/

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 11 页

• Podwise / Colin Jarvis Altimeter 访谈摘要： https://podwise.ai/episodes/6302889
• Y Combinator / Bob McGrew FDE Playbook： https://www.ycombinator.com/library/Mt-the-fde-playbook-forai-startups-with-bob-mcgrew
• SSRN / Forward Deployed Engineering taxonomy： https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6
374660
• Spotify 工程博客： https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-const
raint

FDE 深度信息分析报告 v4 · 作者：黄奕彬 · 第 12 页

