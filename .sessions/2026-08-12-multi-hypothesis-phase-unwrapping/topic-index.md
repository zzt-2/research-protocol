# Topic Index: 有界多假设固定滞后相位解缠 Groundwork

> 状态: closed | 创建: 2026-08-12 | 最后更新: 2026-08-12（R006，GW Step 3.5 cheap absorption terminal）

## 专题信息

- **slug**: `2026-08-12-multi-hypothesis-phase-unwrapping`
- **title**: coherent FSO 有界多假设固定滞后相位解缠 Groundwork
- **depends_on**:
  - `2026-08-08-ch4-reference-method-extension`（继承 K2 published defect、reference-entry 边界和 D007 scope change）
  - `2026-07-09-thesis-writing`（继承 Ch4 方法章槽位、章节 authority 与 claim 约束）
- **conflicts_with**: 无

## 范围边界

**原始目标**：以 Wang TSP 2022 single-tone joint ML/MAP 为成熟 reference method，研究其 phase-unwrapping suffix-pollution defect 在 coherent FSO residual CFO + laser Wiener phase noise 条件下的低复杂度、任务适配扩展；目标研究形态是 bounded multi-hypothesis phase-unwrapping / fixed-lag commit，并以 full Tikhonov-mixture tracker 和 fixed order-2/3 tracker 为强对手做性能—复杂度比较。

**当前范围**：D006/R006 已完成 Groundwork Step 3.5 并科学收口；只保留检索、primary action matrix、comparator 与 claim-ceiling 资产，不再推进 Q001。

**明确不含**：

- 不进入 Step 4a；Step 3.5 只做补充检索、引用链、primary action evidence 与 claim closure。
- 不实现、不仿真、不运行 defect smoke 或公平比较。
- 不声称首次提出 multi-hypothesis、Q#、Go、METHOD_SIGNAL、方法或论文贡献。
- 不把 atmospheric turbulence phase 直接等同为 Wiener laser phase noise。
- 不重开 Q001、coded C1、K1/K3/K4、P1/C3/AMC、fixed-point/selector 旧轴。

**范围变更记录**：

- **[2026-08-12] D001**：由上游 D007 创建唯一 K2 Groundwork 专题，当前仅开放 Step 1。
  - 原因：published suffix defect、FSO transfer 可证伪、近期 baseline、完整 action 可能、强 comparator 与 5–9 天预算六门均通过；TCOM 2016 未被一手证据确认 exact same action。
  - 新范围：三路线、两轮 Step 1 检索和动作/复杂度碰撞初筛。
  - 影响的未决项：Step 2 仍需主控确认；Step 3 才能裁全文 exact/near collision。
- **[2026-08-12] D003**：接受 Step 1 coverage，从 confirmation gate 扩到仅执行 Step 2 acquisition。
  - 原因：主控确认 Step 1，承重不确定性转为 P0/P1 全文可得性和内容质量。
  - 新范围：8–12 篇高价值 acquisition pool；canonical reuse→合法补缺→identity/hash/content 门→coverage terminal。
  - 影响的未决项：Step 3 继续未授权；本轮不得判 exact collision、Q#、方法或 Go。
- **[2026-08-12] D004**：接受 Step 2 coverage，从 confirmation gate 扩到仅执行 Step 3 全文精读。
  - 原因：9 qualified/8 CORE、三路线和 P0 reference/full-mixture 已闭合，承重问题转为动作与复杂度证据。
  - 新范围：9 篇结构化精读、exact action/complexity contract、comparator ladder 与 canonical Q001 四判据。
  - 影响的未决项：Step 3.5/4a 继续未授权；不实现、不仿真、不输出 Go/METHOD_SIGNAL。
- **[2026-08-12] D005**：Step 3 只保留 D1-shaped Q001，D2 降为可选 component/ablation。
  - 原因：Q001 四判据 4/4；C02 task contract 非 exact；C09/C10/C11/C12 已分块吸收 D2 动机。
  - 新范围：停在 `STEP3_Q_SURVIVES_READY_FOR_STEP3_5`，不自动开放下游。
  - 影响的未决项：Step 3.5 需关闭 exact-action/claim debt；Step 4a/实现/仿真仍禁止。
- **[2026-08-12] D006**：接受 Step 3 terminal，从授权门扩到只执行 Step 3.5 mandatory supplement。
  - 原因：9/9 fulltext、Q001 四判据与 V003 已闭合，剩余承重问题为完整动作合同是否 exact/cheap/full absorption。
  - 新范围：四类系统检索、C01/C02/C09/C12 双向引用链、承重全文动作矩阵与最多三轮收敛。
  - 影响的未决项：Step 4a/实现/仿真/参数冻结继续禁止；Step 3.5 不判断 FSO defect occurrence。
  - 收口：三轮检索收敛；ICASSP 2023 占据 D1 承重机制，terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`，无 Step 4a 入口。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. Reference method 为 Wang TSP 2022 single-tone joint ML/MAP；published defect 是单路径 unwrap error 对 suffix 的传播与 failed-run exclusion，不得扩写为 target FSO defect 已成立。
2. 研究条件必须区分 residual CFO、laser Wiener PN、AWGN/AOPN 与 atmospheric turbulence；只使用 receiver-visible input 形成未来 deployable action。
3. Shayovitz–Raphaeli TCOM 2016 full mixture 与 fixed order 2/3 是 mandatory comparator；多轨迹、likelihood、merge/prune、bounded order、pilot recovery 均不是可独占动作原子。
4. 未来可区分 delta 只可落在 task-adapted bounded contract：decoder-free single-tone input、固定 hypothesis/lag/内存/最坏时延、unwrapped sequence 输出，以及可选 receiver-visible trigger。
5. 单方向公平比较预计 5–9 天只是在后续合法通过时可接受；本轮未授权消耗该预算。
6. ICASSP 2023 已占 single-tone integer-wrap paths、likelihood score、fixed survivor pruning 与 unwrapped-sequence output；H=3/fixed-lag standard traceback 不能作为本专题可区分 delta。

### 其他结论

1. 三条路线均有 2019+ 正式发表候选：unwrap/cycle-slip、Tikhonov mixture/fixed-lag、coherent optical/FSO carrier recovery/low complexity。
2. 2016 tracker 在 multi-trajectory primitive capability 上是 `FULL_GENERAL_SUPERSET`，在完整 Q001 task contract 上是 `STRONG_NEIGHBOR / MANDATORY_COMPARATOR`，不是 exact collision。
3. 2019 CSSC-CPE、reduced-rate Kalman、pilot-UKF/reset、DPLL 与 original/improved unwrap/LMMSE-WPA 是 strongest cheap alternatives，后续不能使用弱 strawman。
4. D1/D2 只是设计空间边界，不是方法：D1=bounded 3-hypothesis fixed-lag unwrap；D2=receiver-visible reliability-triggered expansion。
5. Step 3 只保留 D1-shaped Q001；D2 不再作为独立 Q，只可作可选 component/ablation。

## GW Progress

| Step | 状态 | 日期 | 证据 | 下游门控 |
|---|---|---|---|---|
| 1 search | ✅ COMPLETE / VERIFIED | 2026-08-12 | S001/R001–R003/D002/V001/H001 + 11 JSON | terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION` |
| 2 acquire | ✅ COMPLETE / ACCEPTED | 2026-08-12 | D003/S002/R004/V002/H002 + machine receipt | terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；coverage 已由 D004 接受 |
| 3 read | ✅ COMPLETE / VERIFIED | 2026-08-12 | D004–D005/S003/R005/V003/H003 + owner/read-log | terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5` |
| 3.5 supplement | 🛑 COMPLETE / VERIFIED / CHEAP ABSORPTION | 2026-08-12 | D006/S004/R006–R007/V004/H004/receipt | terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION` |
| 4a feasibility | ❌ FORBIDDEN | — | — | Q001 在 Step 3.5 被 prior-art gate 截断 |

## 进展线索

- **S001 / D001**：registry 查重通过；冻结唯一 K2 对象、原始目标、Step 1 边界与 upstream D007 血缘。
- **R001–R003 / D002**：11 query、2 rounds；278 raw→242 title-dedup→138 semantic，98 formal（71.01%），12 must-read，3 个实际贡献源；三路线齐备，未发现 confirmed exact action。
- **V001 / H001**：fresh-context verifier 初审 PARTIAL（0/3/1），formal 归并、编号和预声明均已修；final fresh verifier PASS（0/0/0），Step 2 仍未授权。
- **S002 / D003**：完成 H001 接收核验并冻结 10 篇 acquisition pool；只开放 Step 2，Step 3 保持禁止。
- **R004 / V002 / H002**：12 篇审计，9 qualified、8 CORE；A/B/C 三路线与 P0 reference/full-mixture 均闭合。C06/C07/C13 保留全文缺口；terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。
- **S003 / D004**：完成 H002 接收核验；主控接受 coverage，只开放 Step 3 全文精读，Step 3.5/4a/实现/仿真保持禁止。
- **R005 / D005**：9/9 全文精读；D2 降为可选组件，唯一 Q001 四判据 4/4；C02 仅 primitive 轴 full-general、task contract strong neighbor。
- **V003 / H003**：初审文档schema缺口经一次 bounded repair 后，final fresh verifier PASS 0/0/0；Step 3 verified并停止。
- **S004 / D006**：完成 H003 接收核验；只开放 Step 3.5 mandatory supplement，Step 4a/实现/仿真继续禁止。
- **R006 / receipt**：三轮 new MUST/SHOULD=`5/5→4/8→0/0`；60 条 citation records；ICASSP 2023 direct same-action family 使 D1 落入 cheap absorption terminal。
- **R007 / V004 / H004**：60-row semantic ledger 与 Round1 alias arithmetic 经 bounded repair 后，fresh verifier final PASS 0/0/0；专题 closed。

## 未决项

- Access 2026 fulltext 仍不可得，但不承担 terminal；保留为 claim limitation，不构成重开理由。
- 若未来由新的 published defect 导出非平凡 commit/fallback 机制，必须作为新 research object 重新过入口；不得在本专题补字段重开。

## 当前位置

`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`（D006/R006，具体为 cheap absorption）。Q001 closed；没有 Step 4a 入口、Go、方法、METHOD_SIGNAL 或论文贡献。
