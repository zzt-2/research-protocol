# Handoff: Groundwork Step 3.5 prior-art gate 收口

> 来源: S004 / D006 / R006–R007 / V004 | 交接目标: 保持 Q001 closed，主控另选研究对象
> 日期: 2026-08-12

---

## 到哪了（状态）

Step 3.5 三轮检索已收敛：new MUST/SHOULD=`5/5→4/8→0/0`，60 条 citation records 有逐条 ledger，9 篇新增 primary fulltext 完成动作核验。Ulvog ICASSP 2023 已覆盖 single-tone integer-wrap Viterbi paths、likelihood score、fixed survivor cap 与 unwrapped-sequence output；D1 的 H=3/fixed-lag 只剩既有参数选择和 standard traceback truncation。V004 final PASS 0/0/0；唯一 terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`（具体 cheap absorption），专题 closed。

## 下一步干什么

本专题无下一科学步骤，保持 idle。主控如需继续 Ch4 算法候选，应改变 research object/candidate source；只有新的 published defect 明确导出非平凡 score/commit/fallback 机制时，才可作为新 research object 重新过入口，不能在本专题补字段重开。

## 纪律（续接者必须注意的）

- 不把 ICASSP 2023 写成“逐字段 exact collision”；准确措辞是 direct same-action family + cheap absorption。
- 不以 FSO task label、H=3 或 fixed-lag standard truncation包装可区分动作。
- 不重开 D2 trigger；D005 已将其降为可选 ablation，本专题已经 terminal。
- 不进入 Step 4a、实现、仿真、参数冻结、公平比较；没有 Go、方法、METHOD_SIGNAL 或 Ch4 contribution。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| Access 2026 fulltext | 承重 action 必须 primary fulltext | `UNRESOLVED_NON_BEARING`，publisher HTTP 418 | 仅在它成为新 research object 的承重 prior 时重取；不影响当前 terminal |
| Round3 raw archive | citation ledger应可审计 | 工具未保存逐条 raw；R007 已记录 exact title/DOI/OpenAlex ID，且不承担 terminal | 若未来复用 Round3 identity，再由 DOI/OpenAlex ID核验 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 收敛 | 最后一轮 new MUST/SHOULD=0/0 | gw-supplement / D006 | Round3=0/0 |
| citation audit | ≥10 条且逐条 decision/reason | D006/V004 | 60/60 |
| action evidence | 承重 verdict 有 primary fulltext | D006 | 9 read；Access26 non-bearing |
| fresh verification | P0/P1/P2=0/0/0 | V004 | PASS |

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：三轮 new MUST/SHOULD=`5/5→4/8→0/0` → 待续接方核 R007/receipt
  - 声称2：ICASSP 2023 已有 fixed-S integer-wrap Viterbi sequence action → 待续接方核 `10095456.md:115–147`
  - 声称3：V004 final PASS 0/0/0 → 待续接方核 verifications.md V004
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
