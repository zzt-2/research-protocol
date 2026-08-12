# [R003] Step 1 候选与碰撞矩阵

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D001–D002

## 调研问题

三条路线中的 reference、full-general、cheap 与 recent competitors 分别覆盖什么动作；D1/D2 的 exact action / complexity 字段是否仍需 Step 2–3 闭合？

## 发现

| ID | Identity | Route / role | Step 1 action signature | Collision verdict |
|---|---|---|---|---|
| C01 | Wang et al., TSP 2022, `10.1109/TSP.2021.3137966` | reference + published defect | magnitude/unwrapped phase→single-path O(N) joint ML/MAP；unwrap failure 污染 suffix | `REFERENCE_M`；不是拟议扩展 |
| C02 | Shayovitz–Raphaeli, TCOM 2016, `10.1109/TCOMM.2015.2506553` | mixture / strongest comparator | coded MPSK+pilots+LDPC soft→mixture expand→KL merge/prune→order L=1/2/3→full-sequence posterior/LLR | `FULL_GENERAL_SUPERSET`，非 exact complete chain；mandatory full/order2/3 comparator |
| C03 | Wang et al., TSP 2024, `10.1109/TSP.2024.3421374` | unwrap/WPN neighbor | single chirp parameter estimation under WPN；具体 unwrap/sequence action 待全文 | `NEIGHBOR / ACQUISITION_DEBT` |
| C04 | JLT 2024, `10.1109/JLT.2024.3357289` | optical WPN model/feature | coherent-optical WPN variance estimation；可能改进 prior/score，不等于 unwrap action | `SUPPORTING_NEIGHBOR` |
| C05 | Nature Communications 2024, `10.1038/s41467-024-50439-1` | recent low-cost optical CPR | low-cost optical phase-noise recovery；完整 state/commit/cost 待全文 | `RECENT_COLLISION_DEBT` |
| C06 | Optics Communications 2024, `10.1016/j.optcom.2024.130326` | improved optical CPR | improved carrier phase recovery；摘要不足以裁 fixed-lag/hypothesis action | `RECENT_COLLISION_DEBT` |
| C07 | SPIE 2026, `10.1117/12.3107192` | latest blind CPR/slip | cycle-slip mitigation aided blind CPR；细节待获取 | `RECENT_COLLISION_DEBT` |
| C08 | JLT 2020, `10.1109/JLT.2020.3003561` | space-ground baseline | coarse frequency acquisition→DPLL 跟踪 residual CFO/phase；含 turbulence/laser PN | `TASK_BASELINE / CHEAP_COMPARATOR` |
| C09 | IEEE Access 2019, `10.1109/ACCESS.2019.2934224` | cycle-slip cheap alternative | cumulative CPE-output averages→检测 slip position/direction→self-correction | `CHEAP_ABSORPTION_RISK`；非摘要级 parallel fixed-lag action |
| C10 | Scientific Reports 2021, `10.1038/s41598-020-80822-z` | complexity comparator | reduced-rate 1/2-state Kalman update + interpolation，可自适配 process covariance | `CHEAP_OR_COMPLEXITY_NEIGHBOR` |
| C11 | Photonics 2023, `10.3390/photonics10121312` | satellite implementation | all-digital optical PLL，显式考虑 feedback delay/fading/turbulence | `IMPLEMENTATION_BASELINE` |
| C12 | Electronics 2025, `10.3390/electronics14020265` | closest 2019+ task baseline | second-order feedback loop + feedforward CPR for Doppler FO/laser PN | `CLOSEST_TASK_BASELINE`；abstract 无 bounded winding/fixed-lag signature |
| C13 | J. Optical Fiber Technology 2020, `10.1016/j.yofte.2020.102208` | pilot reset/Bayesian cheap alternative | pilot-assisted UKF phase tracking/reset | `CHEAP_COMPARATOR` |
| C14 | Wang 2022 内对照 / source [31] | original/improved unwrap | adjacent phase-difference single-path unwrap | `STRONGEST_SIMPLE_BASELINE` |
| C15 | Wang 2022 LMMSE-WPA | avoidance comparator | contiguous noisy phase differences→LMMSE frequency estimate，多数条件避免 full unwrap | `STRONGEST_CHEAP_AVOIDANCE` |

### Exact action / complexity contract for later reading

后续每篇 direct candidate 必须逐字段抽取：`input`、`hypothesis state`、`score`、`merge/prune`、`lag/commit`、`fallback`、`output`、`per-symbol/window cost`。缺任一承重字段只能标 `UNRESOLVED`，不能据摘要缺词判 non-exact。

### Design-space boundary

- **D1**：bounded `H=3` fixed-lag unwrap。固定 worst-case state/memory/latency，输出 unwrapped sequence 给 Wang estimator。
- **D2**：receiver-visible reliability-triggered expansion。默认单轨，仅以 normalized innovation、amplitude-informed variance 或 hypothesis margin 等接收端量扩到 `H≤3`；truth metadata 不得进入 trigger。
- **共同红线**：full mixture、fixed order2/3、multi-trajectory likelihood/merge/prune、pilot recovery 已有先例；D1/D2 只有在 task-specific complexity/latency/robustness delta 经 Step 2–4a 证实时才可能继续。

## 结论

Step 1 没有 confirmed exact action collision。C02 是 `FULL_GENERAL_SUPERSET / MANDATORY_COMPARATOR`；C05–C07/C12 保留 recent collision debt；C09–C15 进入 strongest cheap/traditional comparator 集。该结论不等于 non-collision、新颖性或方法成立。

## 对决策的影响

支持 terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`；下一步只允许 acquisition/fulltext 去闭合表中承重字段。R003 取代旧无编号 collision matrix。
