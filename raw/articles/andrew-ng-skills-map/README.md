# Andrew Ng: AI Engineering Skills Map 系列 (5 篇)

> 抓取于 2026-09-13。源:[The Batch / Andrew's Letters](https://www.deeplearning.ai/the-batch/tag/letters)。
>
> **未 ingest 到 wiki** — 本目录仅作 raw 存档,留待后续 compile/ingest 时引用。

## 系列背景

吴恩达 2026-08-14 至 2026-09-11 间在 DeepLearning.AI "The Batch" 的 [Andrew's Letters](https://www.deeplearning.ai/the-batch/tag/letters) 专栏连发 5 篇 "AI Engineering Skills Map"。基于 10,000+ 招聘数据 + 数十次专家访谈 + 问卷调查,提炼出 AI 工程师的四大技能与每项的子技能。

**四大顶层技能**:
1. **Building and deploying AI applications** (Part 2)
2. **Software engineering fundamentals** (Part 3)
3. **Using coding agents** (Part 4)
4. **Shaping the build** (Part 5)

Part 1 是 5 篇之总览。

## 篇目索引

| Part | 日期 | 标题 | 子技能 |
|------|------|------|--------|
| 1 | 2026-08-14 | The AI Engineering Skills Map (overview) | 四大顶层技能 |
| 2 | 2026-08-21 | AI Applications | LLM foundations · Grounding with data · Agentic systems · Eval-driven development · Production · ML foundations |
| 3 | 2026-08-28 | Software Engineering Fundamentals | Full-stack · Data · System architecture · Secure & reliable · Production |
| 4 | 2026-09-04 | Using Coding Agents | Directing workflow · Agent autonomy · Review · Customization · Foundations |
| 5 | 2026-09-11 | Shaping the Build | Driving build loop · Product decisions · Communicating & leading · High-agency ownership |

> **系列入口推文**(吴恩达 X, 2026-09-11): [https://x.com/AndrewYNg/status/2098459474608672916](https://x.com/AndrewYNg/status/2098459474608672916)

## 与本批其他素材的交汇点

| 主题 | 吴恩达 Part | 其他素材来源 |
|------|------|------|
| Eval-driven development | Part 2 (子技能 4) | Madhu Guru 全系列 / Anthropic Demystifying Evals |
| 测量步骤而非仅结果 | Part 4 (Reviewing the work) | Madhu Guru Part 10 "Measure the steps, not just the result" |
| 规划—执行—监控 | Part 4 (Directing the workflow 三步) | Addy Osmani Loop Engineering |
| Agentic loop coding | Part 2 (Building agentic systems) | Addy Osmani / Claude Code Loops |

## 抓取方法

4 篇通过 DeepLearning.AI 文章直链抓取。Part 2 直链是 typo(`he-` 而非 `the-`),所以从 [letters 索引页](https://www.deeplearning.ai/the-batch/tag/letters) 的列表中定位。

- 直接 curl + WebFetch(markdown 模式)
- 脚本: `scripts/_clean_andrew_ng.py` (清理 nav/footer/分享按钮/Elevenlabs 播放器/订阅区)

## 已知限制

- WebFetch markdown 转换会保留"Dear friends"/"Keep building!" 的信件格式——这是 Andrew Ng 的写作风格,刻意保留
- Part 2 URL 中的 typo (`he-`) 已通过索引页交叉验证,确认是 DeepLearning.AI 自身的链接错误(无 301 重定向)
- 图片仅保留 URL 引用,未下载/嵌入