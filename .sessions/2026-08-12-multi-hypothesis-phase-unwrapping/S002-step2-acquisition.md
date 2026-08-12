# [S002] Groundwork Step 2 acquisition

> 2026-08-12 | GW Step 2 | 完成，等待 coverage confirmation

## 目标

按 D003 只执行 Step 2：筛选 8–12 篇高价值 acquisition pool，优先复用 canonical 全文，补缺后逐篇闭合 identity、provenance、SHA、bytes、有效行数与内容质量，并给出 coverage terminal；不进入 Step 3。

## 记录

### Handoff Verification

Verified claims:

- Step 1 终点 commit=`215a200`：PASS — `git log -1 --oneline`。
- Step 1 corpus=`11/278/242/138/98/12`：PASS — R002 规则与 11 个 committed JSON 独立复算一致。
- TCOM 2016=`FULL_GENERAL_SUPERSET / MANDATORY_COMPARATOR`，不是 confirmed exact collision：PASS — R001/R003/V001 与本地 fulltext identity 一致。
- Step 2 原为 `NOT_AUTHORIZED`：PASS — D002/topic/master/H001；现由 D003 显式取代 operational gate。

Registry 核验：`2026-08-08-ch4-reference-method-extension` 与 `2026-07-09-thesis-writing` 两项依赖均存在；`conflicts_with=[]`。本轮触及 topic 的“不得进入 Step 2”旧边界，但主控已显式授权，故 D003 与 topic scope-change 同步记录；“不进入 Step 3/不实现/不仿真”等排除项保持。

### Acquisition pool（12 篇）

| ID | Identity | 路线 | 获取理由 |
|---|---|---|---|
| C01 | Wang TSP 2022 `10.1109/TSP.2021.3137966` | A reference/unwrap | P0 reference defect 与原 estimator identity |
| C02 | Shayovitz–Raphaeli TCOM 2016 `10.1109/TCOMM.2015.2506553` / arXiv `1306.3693` | B full mixture | P0 full mixture/fixed-order mandatory comparator |
| C09 | IEEE Access 2019 `10.1109/ACCESS.2019.2934224` | A/C cycle-slip optical | P0 direct cheap absorption neighbor |
| C12 | Electronics 2025 `10.3390/electronics14020265` | C task baseline | P0 recent coherent optical/FSO baseline |
| C10 | Scientific Reports 2021 `10.1038/s41598-020-80822-z` | C complexity | reduced-rate Kalman performance–complexity comparator |
| C05 | Nature Communications 2024 `10.1038/s41467-024-50439-1` | C recent optical | recent low-cost optical phase-noise recovery collision debt |
| C06 | Optics Communications 2024 `10.1016/j.optcom.2024.130326` | C recent optical | improved CPR collision debt |
| C07 | SPIE 2026 `10.1117/12.3107192` | A/C recent slip | latest blind-CPR slip mitigation debt |
| C13 | J. Optical Fiber Technology 2020 `10.1016/j.yofte.2020.102208` | A/C cheap comparator | pilot-UKF/reset 一手 cheap comparator |
| C08 | JLT 2020 `10.1109/JLT.2020.3003561` | C physical/task baseline | space-ground DPLL 与 residual CFO/laser PN/turbulence |
| C11 | Photonics 2023 `10.3390/photonics10121312` | C satellite implementation | shared canonical 的 all-digital OPLL task baseline |
| C14 | Fu–Kam TIT 2013 `10.1109/TIT.2013.2238604` | A cheap comparator | C01 明确引用的 improved unwrap 一手来源 |

初始 10 篇冻结后，在 acquisition 关闭前补入 C11 与 C14，仍位于授权的 8–12 篇范围；原因是用一手全文分别闭合 satellite implementation 与“至少两项 cheap source”覆盖，而不是扩大研究对象。上述池只定义 acquisition priority 和 coverage role，不提取完整动作签名或裁 collision。

### Acquisition 结果

- qualified=`9/12`，其中 CORE=`8`；正式身份=`12/12`，2019+=`10/12`，合格全文中的 preprint source=`2/9`。
- A 路线：C01/C09/C14；B 路线：C02；C 路线：C05/C08/C10/C11/C12。
- C06/C07/C13 经合法通道后仍无全文，作为 coverage limitation；没有 abstract-only 计数。
- terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；Step 3 继续 `NOT_AUTHORIZED`。

## 决策引用

- D003：接受 Step 1 coverage，只授权 Step 2 acquisition（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（旧 Step 2 排除由 D003 显式改变；Step 3 及以后仍禁止）。

## 后续

等待独立 V002 与 H002 收口后停止；下一合法动作只能是主控另行确认 Step 3。
