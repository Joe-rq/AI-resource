# Madhu Guru: "How to build great evals" 系列 (10 篇)

> 抓取于 2026-09-13。源:[@realmadhuguru](https://x.com/realmadhuguru) X 推文。
>
> **未 ingest 到 wiki** — 本目录仅作 raw 存档,留待后续 compile/ingest 时引用。

## 系列背景

Madhu Guru 自 2026-08-17 起在 X 上以"日更"节奏发布"How to build great evals"系列,
共 10 篇(第 1 篇是开场白,Part 2-10 是正文)。这是继
[WquGuru Agent Memory 架构](../37-agent-memory-architecture-wquguru.md) 之后,
AI 评测主题的又一组一手素材,可与 [OpenAI Cookbook macro evals](../20-macro-evals-for-agentic-systems.md)
和 [Anthropic Demystifying Evals for AI Agents](../../articles/2026-01-09-anthropic-demystifying-evals.md) 对照阅读。

## 篇目索引

| Part | 日期 | 标题 | 主题 |
|------|------|------|------|
| 1 (序) | 2026-08-17 | The best way to get good at evals | 开场白 — 把一个熟悉工作流的质量"可度量" |
| 2 | 2026-08-19 | — |  |
| 3 | 2026-08-20 | — | 失败模式分类法 (referenced in Part 9) |
| 4 | 2026-08-21 | — |  |
| 5 | 2026-08-21 | — |  |
| 6 | 2026-08-22 | — | 梯度下降 / hill-climb (referenced in Part 9) |
| 7 | 2026-08-24 | — |  |
| 8 | 2026-08-25 | — |  |
| 9 | 2026-08-26 | The Eval Roadmap Problem | 用例随时间演进,evals 必须随产品演进 |
| 10 | 2026-09-10 | Measure the steps, not just the result | 同答案不同轨迹的"步骤评分" |

> 主题列空缺处:Part 2-8 的具体主题尚未梳理,后续 compile/ingest 时补充。

## 抓取方法

每篇通过 `curl` 抓取 `https://x.com/realmadhuguru/status/<id>` 的 SSR HTML,
无登录即可拿到 `<h1 class="sr-only">` 中的完整正文(不受 280 字截断影响),
以及 `aria-label="Reply/Repost/Like/Bookmark/View count"` 后跟的 sidebar 计数。

脚本: `scripts/_fetch_madhuguru_evals.py`

## 已知限制

- 仅以无登录 SSR HTML 为源。X 客户端更新后 `aria-label` 命名可能变化。
- sidebar 计数的顺序是 Reply/Repost/Like/Bookmark/View count;书签数仅在登录态显示,
  本脚本以未登录抓取,因此 `bookmarks` 字段通常为空。
- 互动数字随时间变化,本快照反映 2026-09-13 抓取瞬间。