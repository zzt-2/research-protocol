# [R003] K2/K3 reference-method 入口重裁

> 2026-08-11 | 关联：2026-08-08-ch4-reference-method-extension / D005

## 调研问题

在 K1/Q001 以 `EVIDENCE_BLOCKED` 暂存、K4 syndrome 早停已 exact collision 的前提下，K2 三假设 phase-unwrapping 与 K3 可靠度 JP-BPS 是否有任一项同时通过 E1–E8 和 strongest-cheap-alternative absorption gate，从而成为唯一新的 Groundwork Step 1 入口？

## 证据恢复

原四卡未写入本专题文件。本轮从主控/执行对话 JSONL 恢复了原始动作签名，再以仓内一手全文、结构化 read note 和 caller path 重新锚定，不把聊天摘要当科学证据：

- 原四卡回执：`C:/Users/zzt/.codex/sessions/2026/08/09/rollout-2026-08-09T21-26-58-019fe6b4-73a0-7ea2-b492-f126d257ed77.jsonl`，K3 详卡在第 17118 行、K2 详卡在第 17125 行、四卡压缩回执在第 17159 行。
- K2 primary：Wang et al., IEEE TSP 2022, DOI `10.1109/TSP.2021.3137966`；`papers/doi/10.1109_tsp.2021.3137966/content.md:1-21,61-75,95-213,331-357,431-449`。
- K2 strongest absorption source：Shayovitz–Raphaeli, IEEE TCOM 2016 / arXiv `1306.3693`；`papers/arxiv/1306.3693/content.md:126-138,223-250,293-329,388-410`。
- K3 primary：Kuschnerov et al., JLT 2009, DOI `10.1109/JLT.2009.2024963`；`papers/doi/10.1109_jlt.2009.2024963/content.md:57-61,761-777,825-849`。
- K3 recent defect neighbor：Zhang et al., JPHOT 2023, DOI `10.1109/JPHOT.2023.3328423`；`papers/downloads/2026-07-08/10301506.md:5-25`。

本轮未新增 query：现有一手全文与索引已经能对承重门作否定裁决；按有界入口合同，没有为填满配额而继续搜索、下载或精读新全文。

## 恢复的动作签名

| 卡 | reference M / published defect | 原 future action | strongest cheap alternative |
|---|---|---|---|
| K2 三假设 phase-unwrapping | TSP 2022 的 single-tone joint ML/MAP 依赖 unwrapped phase；一次 unwrap 错误会累积污染全部后继点，较大 `ω0/N/σp²` 时论文剔除 failed runs | principal phase differences + magnitude/AOPN reliability + prior trajectory → 保留 `m∈{-1,0,+1}` winding 分支 → 累积因果 likelihood、剪枝/合并、固定 lag 后提交一支 → unwrapped phase sequence 送回原 ML/MAP | maximum-order 2/3 Tikhonov-mixture/sequence tracker；另有 LMMSE-WPA、improved unwrap、clipping/pilot reset |
| K3 可靠度 JP-BPS | JP-V&V 证明两偏振共同 phase information 可联合；但没有发表“固定 JP 在 unequal reliability 下失效”的承重 defect | 两偏振固定窗 BPS phase-grid costs + power/margin → reliability normalization → 对同一 phase hypothesis 作一次加权联合评分 → common phase estimate + corrected dual-pol symbols | fixed JP-V&V、等权/固定分段 JP-BPS、ordinary per-pol BPS；Weighted-BPS/RW-BPS/unequal-SNR CPR 仅形成待全文闭合的 collision debt |

## E1–E8 裁决

| 门 | K2 | K3 |
|---|---|---|
| E1 正式 reference | PASS：TSP 2022 | PASS_WITH_RECENCY_DEBT：JLT 2009 是正式 JP reference；但没有 2019+ task-matched JP-BPS baseline，2023 source 是四孔径 FSE+AKF |
| E2 published defect | PASS：suffix pollution 为正文明确事实 | FAIL：仅 generic window/phase-set tradeoff；固定 JP unequal-reliability defect 未发表，且原文称 fixed coupling 可 near-optimal |
| E3 coherent-FSO 迁移 | PASS_INFERENCE：残余 CFO/Wiener PN 可证伪 | PASS_INFERENCE：共同 LO phase + 偏振可靠度差异可证伪 |
| E4 0.5–1 天 smoke | UNRESOLVED：可画 reference smoke，但忠实 Wang identity 曾 FAIL，且缺冻结 MDE/退出阈值 | PASS_SHAPE：shared phase + SNR imbalance 的 defect-only smoke 可构造 |
| E5 一个完整 action | UNRESOLVED：lag/score/merge/fallback 未冻结，名称不足以唯一化动作 | PASS：always-on weighted joint-cost fusion |
| E6 collision/dead-end | UNRESOLVED_HIGH_RISK：order-2/3 mixture tracker 已覆盖多轨迹、likelihood、merge/prune、confidence/reacquisition | UNRESOLVED_HIGH_RISK：unequal-SNR CPR、Weighted/RW-BPS 与 JP-CPE 只有 metadata/二手线索，尚无完整动作对照 |
| E7 Ch4 方法节 | FAIL：与三阶 tracker 的可区分 delta 未形成 | UNRESOLVED：缺 published defect 与 collision closure，只能是窄组件 |
| E8 fair comparison 成本 | FAIL_CONDITIONAL：忠实 baseline + task-matched mixture comparator 后约 5–9 天，存在越过 7 天上限的实质风险 | PASS_CONDITIONAL：约 3–6 天，但上游门已失败 |

## strongest-cheap-alternative absorption

### K2

TCOM 2016 已经执行 `received samples/pilot/soft symbols → per-symbol phase trajectories → likelihood/KL merge-prune + bounded order → confidence/pilot recapture → phase posterior/LLR`，且 order 2/3 接近 DP。它与 K2 的 single-tone input 和最终 estimator target 不同，因此本轮只将其裁为 `UNRESOLVED_HIGH_RISK / STRONG_NEIGHBOR`，不声称 exact collision 或已完全吸收。K2 当前仍没有独立 trigger、output 或复杂度合同形成可区分 delta。

### K3

JP-V&V 已占据双偏振共同相位的 fixed fusion，且论文在高 XPM 降低相关性时仍报告 fixed coupling near-optimal。K3 需要的承重问题不是“joint fusion 有用”，而是“fixed fusion 在 receiver-visible reliability 异质时可测地失效”；现有 primary 不支持该事实。Weighted-BPS、RW-BPS 与 unequal-SNR CPR 目前只构成待一手全文闭合的 collision debt，不能据此声称 exact prior 或动作已被吸收。

## 结论

terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_SHORTAGE`。

- K2 因 E4/E5/E6 未闭合、E7 失败、E8 超预算风险而拒绝入口；published suffix defect 保留为证据资产，不计 research-object scientific failure。
- K3 因 E2 失败、E6 高风险未闭合且 2019+ task-matched baseline 缺位而拒绝入口；不是 JP-BPS family Kill。
- 没有唯一 survivor，故不创建新的 Groundwork 专题、不运行 GW Step 1，也不制造第三张弱卡。
- K1/Q001 继续保持 recoverable `EVIDENCE_BLOCKED`；K4 exact collision、coded C1、P1/C3/AMC、fixed-point/selector 旧轴均不重开。

## 对决策的影响

建立 D006：结束本次自动轮换并确认当前 reference-entry source 的战略短缺。下一次若继续方法生产，必须改变 candidate source 或 research object，并同时带入 task-matched 2019+ reference、明确 published defect 和已闭合的 strongest cheap comparator；不能在 K2/K3 上补命名后重投。
