# Wiki 治理反哺 Roadmap

> 用 wiki 自己研究的概念，治理 wiki 自己的维护体系。
> **验收标准（防知行脱节 2.0）：每个概念必须落地为可跑的机制，否则是债不是资产。**

## 起因

2026-06-24 一次"检查 wiki 质量"暴露：重复链接积累 80 个、0 字节空文件出现 2 次、CLAUDE.md 声称的 hook 从未配置、引用幽灵脚本。讽刺的是——防治这些错误的概念（[[Harness Cybernetics]]、[[Heartbeat Watchdog]]、[[Stateless Reducer]]、[[Agent-Harness-治理协议]]）全都已写在 wiki 里。**问题不在"AI 又犯错"，而在知行脱节：概念躺在 wiki 里，机制没落在工程里。** 本 roadmap 把概念系统地反哺回 wiki 自身的 compile/ingest/lint/audit/hook 流程。

## 元方法：Ashby 检查

[[Harness Cybernetics]] 的核心操作化——**每个常见失败模式必须有对应的 Feedforward（前馈预防）或 Feedback（反馈自纠），否则 Ashby 违例、该失败模式逃逸。** 本 session 踩的每个坑都是一条违例。下表就是 Ashby 矩阵本身。

## 失败模式 × 控制覆盖矩阵

| wiki 维护失败模式 | 本 session 实例 | Feedforward | Feedback | 现状 | 落地项 |
|---|---|---|---|---|---|
| 机械规则违反积累 | 重复链接 80 个 | — | lint_overlinks hook | ✅ 已做 | — |
| 文档与现实脱节 | 幽灵脚本 / 虚假 hook 声明 | — | consistency check | ❌ 缺 | **#1** |
| 环境污染 / 游离文件 | 0 字节空文件 ×2 | — | 游离文件巡检 | ❌ 缺 | **#2** |
| 工具假设盲区 | guard 漏 untracked | — | 测试驱动验证 | ⚠️ 已修+立范式 | — |
| 覆盖盲区本身（元） | 以上所有逃逸 | Ashby 矩阵脚本 | — | ❌ 缺 | #3 |
| ingest 不可逆 | 手动修 80 链接 | reducer 快照 | replay / 回滚 | ❌ 缺 | #4 |
| 概念振荡 / 死概念 | （未观测但隐患） | 新颖性检查 | — | ❌ 缺 | #5 |

## 落地项

### #1 Consistency Check（对账）— 本期落地
- **概念来源**：[[Stateless Reducer]] 可对账 + [[Agent-Harness-治理协议]] 双层验证
- **机制**：扫描 CLAUDE.md + `.claude/settings.json` 引用的所有 `scripts/*.py`、声明的 wiki 页面，验证真实存在
- **类型**：Computational feedback（确定性、不可幻觉）
- **验收**：构造一个引用不存在脚本的 CLAUDE.md 片段，脚本必须报错
- **自指讽刺**：用 reducer 的对账思想，检查 reducer 概念页引用的脚本是否存在

### #2 游离文件巡检（watchdog）— 本期落地
- **概念来源**：[[Heartbeat Watchdog]] 独立守护层（L1 定时巡检）
- **机制**：检测项目里不在预期目录（`wiki/ raw/ scripts/ log/ audit/ docs/ .claude/`）的 `.md` 文件
- **类型**：Computational feedback
- **验收**：在根目录造一个 `.md`，巡检必须报
- **集成**：并入 `lint_wiki.py`（手动全检）+ 可选 Stop hook

### #3 Coverage Matrix 脚本（Ashby 元方法）— 后续
- **概念来源**：[[Harness Cybernetics]] Ashby's Law
- **机制**：把上面这张矩阵做成数据文件，脚本检查"每个失败模式至少有一个 ✅ 控制"，有 ❌ 无对应时报警
- **价值**：让"盲区发现"本身机械化，而非靠人肉复盘

### #4 可回滚 ingest（reducer）— 后续设计
- **概念来源**：[[Stateless Reducer]] + [[ESAA]] event sourcing
- **机制**：ingest 前自动快照（git stash / tag）+ append-only 事件日志，支持 revert 到 ingest 前
- **为何重要**：最大系统性 gap——当前每次 ingest 不可逆，错了只能手动擦屁股（本 session 修 80 链接即为实例）
- **工程量大，本期只设计**

### #5 概念新颖性检查 — 后续设计
- **概念来源**：[[Agent-Harness-治理协议]] 概念生命周期 + 新颖性检查
- **机制**：compile 时检查概念重命名 / 合并是否带"引入了什么新信息"说明，防振荡（同一设计来回改）

## 原则（从概念反推）

- **Computational 优先**（[[Harness Cybernetics]]）：能用确定性检查（exit code / 文件存在 / diff）就别用 LLM judge
- **steering 而非 prompting**（[[Harness Cybernet]]）：问题反复出现 → 改 harness，不改 prompt
- **防过度防护**（[[Agent-Reliability-vs-Capability]]）：memory scaffolds 普遍损害长程 reliability——防护精准 > 数量
- **deterministic feedback 优先**（[[Harness Cybernetics]]）：Verifier 用 exit code/diff/test，不用 LLM 解释

## 状态

- 本期（2026-06-24）：落地 #1、#2；#3-5 入 roadmap 待续
- 更新约定：每落地一项，把矩阵对应行从 ❌ 改 ✅
