# Topic Index: 有界多假设固定滞后相位解缠 Groundwork

> 状态: active | 创建: 2026-08-12 | 最后更新: 2026-08-12（V002 PASS，GW Step 2 ready for confirmation）

## 专题信息

- **slug**: `2026-08-12-multi-hypothesis-phase-unwrapping`
- **title**: coherent FSO 有界多假设固定滞后相位解缠 Groundwork
- **depends_on**:
  - `2026-08-08-ch4-reference-method-extension`（继承 K2 published defect、reference-entry 边界和 D007 scope change）
  - `2026-07-09-thesis-writing`（继承 Ch4 方法章槽位、章节 authority 与 claim 约束）
- **conflicts_with**: 无

## 范围边界

**原始目标**：以 Wang TSP 2022 single-tone joint ML/MAP 为成熟 reference method，研究其 phase-unwrapping suffix-pollution defect 在 coherent FSO residual CFO + laser Wiener phase noise 条件下的低复杂度、任务适配扩展；目标研究形态是 bounded multi-hypothesis phase-unwrapping / fixed-lag commit，并以 full Tikhonov-mixture tracker 和 fixed order-2/3 tracker 为强对手做性能—复杂度比较。

**当前范围**：D003 已接受 Step 1 coverage，只执行 Groundwork Step 2 acquisition：从 R003 shortlist 筛选 8–12 篇，复用或合法获取高价值全文，闭合 identity/provenance/SHA/content-quality 与三路线 coverage。设计形态不是方法卡；本轮不做动作级精读或 collision 裁决。

**明确不含**：

- 不进入 Step 3；Step 2 只获取/转换/质量核验，不做动作级全文精读。
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

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. Reference method 为 Wang TSP 2022 single-tone joint ML/MAP；published defect 是单路径 unwrap error 对 suffix 的传播与 failed-run exclusion，不得扩写为 target FSO defect 已成立。
2. 研究条件必须区分 residual CFO、laser Wiener PN、AWGN/AOPN 与 atmospheric turbulence；只使用 receiver-visible input 形成未来 deployable action。
3. Shayovitz–Raphaeli TCOM 2016 full mixture 与 fixed order 2/3 是 mandatory comparator；多轨迹、likelihood、merge/prune、bounded order、pilot recovery 均不是可独占动作原子。
4. 未来可区分 delta 只可落在 task-adapted bounded contract：decoder-free single-tone input、固定 hypothesis/lag/内存/最坏时延、unwrapped sequence 输出，以及可选 receiver-visible trigger。
5. 单方向公平比较预计 5–9 天只是在后续合法通过时可接受；本轮未授权消耗该预算。

### 其他结论

1. 三条路线均有 2019+ 正式发表候选：unwrap/cycle-slip、Tikhonov mixture/fixed-lag、coherent optical/FSO carrier recovery/low complexity。
2. 2016 tracker 是 `FULL_GENERAL_SUPERSET / MANDATORY_COMPARATOR`，不是 Step 1 已确认 exact collision。
3. 2019 CSSC-CPE、reduced-rate Kalman、pilot-UKF/reset、DPLL 与 original/improved unwrap/LMMSE-WPA 是 strongest cheap alternatives，后续不能使用弱 strawman。
4. D1/D2 只是设计空间边界，不是方法：D1=bounded 3-hypothesis fixed-lag unwrap；D2=receiver-visible reliability-triggered expansion。

## GW Progress

| Step | 状态 | 日期 | 证据 | 下游门控 |
|---|---|---|---|---|
| 1 search | ✅ COMPLETE / VERIFIED | 2026-08-12 | S001/R001–R003/D002/V001/H001 + 11 JSON | terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION` |
| 2 acquire | ✅ COMPLETE / PENDING CONFIRMATION | 2026-08-12 | D003/S002/R004/V002/H002 + machine receipt | terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；Step 3 未授权 |
| 3 read | ⬜ FORBIDDEN | — | — | Step 2 未完成前禁止 |
| 3.5 supplement | ⬜ FORBIDDEN | — | — | Step 3 未完成前禁止 |
| 4a feasibility | ⬜ FORBIDDEN | — | — | Step 3/3.5 未完成前禁止 |

## 进展线索

- **S001 / D001**：registry 查重通过；冻结唯一 K2 对象、原始目标、Step 1 边界与 upstream D007 血缘。
- **R001–R003 / D002**：11 query、2 rounds；278 raw→242 title-dedup→138 semantic，98 formal（71.01%），12 must-read，3 个实际贡献源；三路线齐备，未发现 confirmed exact action。
- **V001 / H001**：fresh-context verifier 初审 PARTIAL（0/3/1），formal 归并、编号和预声明均已修；final fresh verifier PASS（0/0/0），Step 2 仍未授权。
- **S002 / D003**：完成 H001 接收核验并冻结 10 篇 acquisition pool；只开放 Step 2，Step 3 保持禁止。
- **R004 / V002 / H002**：12 篇审计，9 qualified、8 CORE；A/B/C 三路线与 P0 reference/full-mixture 均闭合。C06/C07/C13 保留全文缺口；terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。

## 未决项

- 2016 tracker 与 D1/D2 的 exact/near collision 在全文动作与复杂度层是否仍有可区分 delta。
- 2025 inter-satellite CPR、2019 CSSC-CPE、2021 reduced-rate Kalman 和 2024 optical CPR 是否吸收性能—复杂度主张。
- D1 固定 lag/hypothesis ceiling 与 D2 reliability trigger 的 receiver-visible 定义、merge/prune、fallback 和 commit contract。

## 当前位置

`STEP2_READY_FOR_USER_CONFIRMATION`。当前只有身份/内容/coverage 已闭合的 acquisition corpus；没有 collision/Q#/Go、方法、METHOD_SIGNAL 或论文贡献。Step 3 未授权。
