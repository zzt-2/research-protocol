# Handoff: Q1 coverage decision 已处理，等待 Step 4a preflight 讨论

> 来源: S001 | 交接目标: 新会话重读 `gw-feasibility.md`，只讨论是否进入 Step 4a
> 日期: 2026-08-06

## 到哪了（状态）

用户提供的 JLT 2025 IQ-skew 全文已通过 T013 acquire→read：它是 shared-preamble 顺序多模块链，
不是单一 joint `(frame,fractional τ,CFO)` estimator。JLT blocker 已消解；JOCN 2026 由用户确认不可得，
停止获取重试但永久保留 coverage/novelty 限制。D008 terminal=
`STEP3_5_COMPLETE_Q1_SURVIVOR_JOCN_FULLTEXT_UNAVAILABLE_NO_CONFIRMED_EXACT_COLLISION`。
V006 fresh-context closeout 复验已 PASS，blocker=0。

## 下一步干什么

另起会话，先逐字重读 `stages/gw-feasibility.md` 与 formal D006–D008，再讨论是否授权进入 Step 4a。
本 handoff 不授权自动转阶段、方法实现、testbed、MVE 或仿真。

## 纪律

- “JOCN 不可得”是 accepted coverage limitation，不是它与 Q1 不碰撞的证据；
- JLT 2025 必须进入最强 cheap comparator：shared TS-A 顺序执行 frame/IQ-skew/SOP/timing/FOE；
- Q1 survivor 仍不是 Go、METHOD_SIGNAL、novelty closure 或论文方法成立；
- 不修改 `common/`、`params.py`、旧实验/Skill/四个 `p05_run*.log`。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| JOCN 2026 无全文 | exact-action claim 应由全文裁决 | 用户确认不可得；仅接受 coverage gap | 若未来出现合法全文，在任何“首次/无竞品”声称前必须 acquire→read |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：JLT 2025 非 exact collision → T013 worker log/read note/Fig. 2 与 Eq. 16–23
  - 声称2：JOCN 已停止获取但 claim limitation 保留 → D008/voice.md
  - 声称3：当前只允许 Step 4a preflight discussion → RDL D032/control 与 master-state
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
