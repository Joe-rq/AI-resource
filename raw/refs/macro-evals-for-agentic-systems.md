---
kind: ref
title: "Macro Evals for Agentic Systems"
authors: [Shikhar Kwatra (OpenAI), Will Thieme, Bradley Strauss]
date: 2026-05-19
source_url: "https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems"
external_path: "https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems"
created: 2026-06-13
note: "OpenAI Cookbook 官方示例 notebook。中文改写版已摄入 raw/articles/20-macro-evals-for-agentic-systems-zh.md。原文 notebook 含完整代码（Python pandas + UMAP + HDBSCAN + 网络图诊断），未在 wiki 中复制代码，只摄入方法论与公式。"
---

# Ref: Macro Evals for Agentic Systems

OpenAI Cookbook (Partners): <https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems>

## 主要内容

- 案例：电动车订单处理多 Agent 系统（定价 / 合规 / 供应 / 工厂路由 / 排期 / 客户沟通 / 放行审查）
- 数据：1,000 次合成运行 → 992 个 trace bundle 可用
- 工具：Promptfoo（底层评估）+ BERTopic 风格聚类（UMAP + HDBSCAN）+ AgentTrace 风格诊断
- 关键公式：`impact_score = prevalence × severity_weighted_prevalence`、`lift = slice_share / overall_share`、`suspect_score = 0.4·proximity + 0.3·frequency + 0.2·bridge + 0.1·role`

详见 [[summaries/20-macro-evals-for-agentic-systems]]、[[concepts/Agent-Macro-Evaluation]]。
