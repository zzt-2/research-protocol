# [S004] Q1 Groundwork Step 4a feasibility

> 2026-08-09 | Groundwork Step 4a | TERMINAL_VERIFIED_INCONCLUSIVE
> 2026-08-09 续接 | T015–T019 blocker 收口与 V007 PASS；未运行 performance grid/MVE

## 目标

在 D009 冻结边界内先过 validity/calibration 起飞门；semantic smoke performance grid 与 bounded MVE 仅在门控通过时运行，并在唯一合法 Step 4a terminal 停止。V007 已独立接收 terminal 5，本轮在该终态停止。

## 记录

- 起点 HEAD=`80a9dc1e5ed9c1a22a0edd7d1172c19372a1ac2b`；tracked/staged diff 为空，仅四个既有未跟踪 `p05_run*.log`，继续保护且不暂存。
- H005 接收 4 项事实验证 PASS：共享 130981 PDF/content 路径、bytes、SHA 与 V005 一致；正文动作是固定分块 FFT/均谱/谱功率比 coarse FOE，不是 condition→lag/`B_L`/window selector；Q1 仅 provisional survivor；Step 4a 启动前为 `NOT_STARTED`；conditioned single-lag lookup 是不可删的最强廉价 comparator。
- registry：本专题 `depends_on=2026-08-08-ch4-reference-method-extension`，依赖专题为稳定 dormant source owner；`conflicts_with=[]`；当前仅 3 个既有 S 文件，未触发 inflation warning。
- `sim-preflight` 阶段路由：本轮属于 GW Step 4a/MVE，不进入 Execute；只继承 C1–C8、参数真相源、paired realization、算法正确性和文档纪律，主流程 owner 为 `stages/gw-feasibility.md`。
- D009 已记录用户对旧“明确不含”Step 4a 的显式 scope approval，并冻结 baseline ladder、门限、stop rules、唯一终态集和 claim ceiling。
- T011/T012/T013 已完成：公式/身份=`PARTIAL`（Wang HTML 公式可用、两篇 PDF 缺失、Enhanced 公式不可恢复）；testbed=`NEEDS_BOUNDED_ADAPTER`；独立 A0=`ALLOW_SEMANTIC_SMOKE`。三者共同排除旧 B3 复用，并允许在隔离目录闭合 Wang-identity adapter。
- D010 冻结同一论文默认 FSTS 上的 receiver-lag adapter、弱/强 GG 与 SNR 语义、dev/test pairing、B0/B1/B2/O1、metric/outage、CI/regret 和 terminal reducer。非默认 lag 不冒充 Wang/Enhanced 原测点。
- V006 在任何 RED/grid 前独立判 D010=`FAIL, P0/P1/P2=2/5/2`：off-default `L_rx` 改变 Q1 方法对象，未验证 SNR/transfer channel 又无 source calibration。executor 已被中断；D010 立即 rejected，未产生科学结果或结果驱动调参。
- T015 source-calibration audit=`HARD_BLOCKED_FOR_SCIENTIFIC_TERMINAL`：structural action-before causality、Wang phase-screen/SMF 与 Gu scalar-GG 非等价、dBm→离散复噪声不可辨识为三类 hard blocker；B0 source numeric calibration gate 亦不可执行。
- T016 figure-axis recovery=`FIGURE_ACCESS_BLOCKED`：Fig. 8/10/11/12 direct GIF 均返回相同 403 HTML；缺轴/ticks/逐点曲线是 recoverable gap，不是上述 hard blocker 的替代解释。
- T017 physical-transfer audit=`SOURCE_CONDITION_ONLY_NO_NOISE_CLOSURE`：带额外波长/平面波假设只能形成 sensitivity table，不能恢复 Wang phase-screen+coupling 或 `ROP[dBm]→E|w[k]|^2`。
- terminal reducer 在第一层 `validity/calibration` 即停止：D011/V007=`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`。ranking crossover、B2 residual、observability/actionability、C1 与 MVE 均未评价。
- 科学产出明确为空：没有 scientific raw rows、paired delta/CI、performance grid 或 bounded MVE；B0/B1/B2/O1/C1 performance 数字统一为 `N/A (NOT_RUN)`。门控跳过不是“实验完成”，也不是“跑了但无结果”。
- T019 fresh-context verifier 独立重放原文、代码、owner、receipt 与保护范围，V007=`PASS, P0/P1/P2=0/0/0`；verifier log SHA-256=`9f855b33e2d5785682e9c4dcea3a8bd7eab9659355d80c12504159e04c9f744d`。

### 假设与否决条件

- H1：有依据的 receiver-visible condition 变化会改变 lag/`B_L` ranking。否决条件：公平扫描和 paired seeds 下无 ranking crossover。
- H2：B2 后仍有稳定的 normalized CFO-MSE/outage residual。否决条件：B2 吸收，或 residual 不能跨条件/seeds 稳定达到 `20% MSE`/`10 pp outage` 门。
- H3：receiver-visible features 能区分并驱动合法动作。否决条件：best-action observability 不高于冻结判据，或 hidden truth 改变会改变 deployable action。
- H4：最小 C1 在 fresh held-out 上相对 B2 产生非伪影增量。否决条件：paired CI/MDE 未过、机制消融不支持、或信息/预算不公平。

### 迭代计数器

- A0/testbed readiness：`1/1`（`ALLOW_SEMANTIC_SMOKE / NEEDS_BOUNDED_ADAPTER`）
- semantic smoke：`0/1`
- bounded MVE：`0/1`（仅条件式）
- pre-run contract rejection：`1/1`（V006；只允许一次 structural/source-calibrated 重构）
- source calibration/physical transfer audit：`1/1`（T015+T017；scientific terminal hard-blocked）
- figure-axis recovery：`1/1`（T016；recoverable gap，未取得原图）
- performance grid：`0/1`（`NOT_RUN`；validity/calibration 起飞门前阻断）
- diagnostic structural run：`0/1`（`NOT_RUN / TERMINAL_DISABLED`）
- repair chain：`0`（未运行科学迭代；禁止结果驱动修补）
- terminal owner sync：`1/1`（T018）
- fresh-context independent terminal verification：`1/1`（T019/V007=`PASS, P0/P1/P2=0/0/0`）

## 决策引用

- D008：Q1 是带全文限制的 provisional survivor。
- D009：Step 4a 连续执行合同与唯一终态集（新建）。
- D010：semantic-smoke receiver-lag adapter 与统计合同（新建）。
- D011：Step 4a terminal 5，经 V007 独立终验 PASS（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D009 与 topic-index 2026-08-09 scope-change record）。

## 后续

本轮在 V007 PASS 与 D011 terminal 5 停止。科学重开必须先取得 authors/source receiver+channel config，并经显式 scope-change 定义 action-before protocol；否则保持 dormant，不运行 performance grid、diagnostic structural run、MVE 或下游阶段。
