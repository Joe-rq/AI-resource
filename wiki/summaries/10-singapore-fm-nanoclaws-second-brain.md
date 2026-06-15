---
title: "新加坡外长的 AI 第二大脑"
type: summary
source_url: https://www.anduril.tw/second-brain/
source_type: article
date: 2026-05-17
ingested: 2026-05-22
tags: [agent-platform, edge-runtime, nanoclaw, vivian-balakrishnan]
---

# 新加坡外長的 AI 第二大腦：沒親手用過，就無法替國家做對決策

**Source**: [狐說八道 - Fox Hsiao](https://www.anduril.tw/second-brain/) · 2026-05-17

## Key takeaways

- 新加坡外長 Vivian Balakrishnan（眼科外科醫師轉政）在 AI Engineer Singapore 大會展示了他用 **NanoClaw + Raspberry Pi（8GB）** 組裝的個人 AI 助理，三個月日常使用後「不敢關掉」
- **三句核心訊息**：①理解無法外包（AI 可整理資訊，但判斷和決策無法替代）②價值在地面層（落地到每個工作流程，而非模型本身）③入門門檻已塌（工具備好，缺的是動手意願）
- 他引用的那句話：「你沒辦法治理一個你只被簡報過的技術」——這句話點出了決策者親手使用 AI 工具的必要性

## Core claims

NanoClaw 建在 Claude Agent SDK 上，500行程式碼，可容器化，隔離錯誤邊界。他的系統架構：NanoClaw + WhatsApp（Baileys 模擬）+ Mnemon（圖譜記憶）+ Whisper（語音）+ Obsidian（介面）+ 本地 Ollama（語意搜尋），跑在 8GB 樹莓派上。整套系統是「邊做邊學」的產物，他沒有寫任何底層框架。

他對「理解」和「問責」的區分最值得記：把工作授權出去是可以的，但問責的底氣來自你真正懂得工具在發生什麼事。這也解釋了為什麼他堅持自己掃 bash 權限的程式碼。

## Notable quotes

> 「你沒辦法治理一個你只被簡報過的技術。」— Claude 替他生成的話，他特別在演講中引用

> 「他老實講，已經不敢把它關掉了。」

## Concepts introduced / referenced

- [[concepts/Agent-Runtime]] — NanoClaw 是邊緣 Runtime 的典型：容器化隔離、極小程式碼量
- [[concepts/Multi-Agent-协作模式]] — 他的助理是 Single-Agent + 多工具增強的邊緣部署
- [[entities/MiniMax-Mavis]] — 同樣強調個人化 AI 助理，定位不同但方向一致
