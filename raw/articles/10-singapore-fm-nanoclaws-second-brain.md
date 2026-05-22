# 新加坡外長的 AI 第二大腦：沒親手用過，就無法替國家做對決策

**Source**: [狐說八道 - Fox Hsiao](https://www.anduril.tw/second-brain/) · 2026-05-17

## Key takeaways

- 新加坡外長 Vivian Balakrishnan 在 AI Engineer Singapore 大會展示了他用 **NanoClaw + Raspberry Pi（8GB）** 組裝的個人 AI 助理
- 三句核心：①理解無法外包、②價值在地面層、③入門門檻已塌
- 他引用的那句話：「你沒法治理一個只被簡報過的技術」
- 系統跑在邊緣設備（樹莓派）上，日用量極大，已經不敢關掉

## Core claims

新加坡外交部長，同時也是眼科外科醫師背景，用 NanoClaw（建在 Claude Agent SDK 上的開源框架）在樹莓派上跑了三個月的個人 AI 助理。他把整場演講收斂成三個訊息，認為就算忘掉其他東西，記住這三件事就好：

1. **理解無法外包**：AI 可以整理資訊，但把資訊變成判斷、把判斷變成決定，這段路沒人能替你走。有權力的人可以授權工作，但不能授權問責。
2. **價值在地面層**：真正創造價值的不是模型和資料中心，而是一個工作流程接一個工作流程地落地。老師、律師、技師、醫生、部長——這些懂自己這份工作又被工具加持的人，才是替社會創造真實價值的人。
3. **入門門檻已塌**：他不是工程師，三個月的成果全靠組裝。工具早就被備好了，現在缺的是「把手弄濕」的意願。

## System architecture

NanoClaw 提供底層平台，透過 WhatsApp 對話（Baileys 模擬 WhatsApp Web 協議）。記憶系統用 Mnemon（圖譜結構，實體+關係），本機跑 Ollama 做語意搜尋。語音交給 Whisper。介面用 Obsidian + iCloud 做個人雲。整套系統跑在一台 8GB 記憶體的樹莓派上。

## Notable quotes

> 「你沒辦法治理一個你只被簡報過的技術。」— Claude 生成的話，Balakrishnan 在演講中特別引用

> 「他老實講，已經不敢把它關掉了。」— 三個月使用後的感受

## Concepts introduced / referenced

- [[concepts/Agent-Runtime]] — NanoClaw 是邊緣 Runtime 的典型案例
- [[concepts/Multi-Agent-协作模式]] — 他的助理是一套 Single-Agent + 工具增強的架構
- [[entities/NVIDIA-Agent-Toolkit]] — 同樣強調邊緣部署，與他的「地面層」邏輯一致

## Sources

- AIE Singapore Day 1 主題演講（34:05–1:05:00）：https://www.youtube.com/watch?v=_xQnSNlBP_w
