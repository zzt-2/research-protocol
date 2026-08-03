# Figure/Table Plan — Thesis Blueprint

> **SUPERSEDED / PAUSED — D025→D026 (2026-08-03)：旧图表蓝图保留作证据，当前不得作为 Ch4/Ch5 最终章节合同；当前条件式合同见 D026。**

> 2026-08-03 | 关联: conference-to-thesis-map.md
> 按唯一推荐 thesis blueprint（Ch1–Ch6）规划图表。每张图/表标注：来源（复用/重画/新增）、claim ceiling、缺口。

## 复用 vs 新增 总览

| 类别 | 数量 | 说明 |
|---|---|---|
| 复用会议稿（READY） | 5 图 | Fig.1 系统模型 / Fig.2 selector / Fig.3 BER / Fig.4 crossover / Fig.5 BER-ratio |
| 重算重画（RECOMPUTE_ONLY） | 2 表 | headline 复算表 + 统一鲁棒性/边界表 |
| 小验证新增（SMALL_VALIDATION） | 2 图 + 1 表 | branch-compute timing / float-vs-Q / coded FER |
| 不新增（INVALIDATED/未来） | — | G1/P09 不进图；AMC 不进图 |

---

## Ch2 系统模型

| ID | 类型 | 内容 | 来源 | claim ceiling | 缺口 |
|---|---|---|---|---|---|
| F1 | 图（复用） | 系统模型总览：Tx—FSO/GG channel—coherent Rx—DSP，含 (8,8)-16APSK / h_b / φ_k / n_k / r_k / N_ch=100 / N_DSP=256 | `figures/fig1_system_model_v5.pdf`（V024/V025 PARTIAL：用户保留 0.32pt 安全间距债务） | 系统结构 | 无（债务已记录，用户决定） |
| 符号表 | 表 | 信号/信道/selector 符号一览（γ, ρ_p, Δ_p=1.249dB, CV, τ_CV, ĥ_dsp, 13dB 门） | 新建（从 system_model.tex + method.tex 抽取） | — | 无 |

## Ch3 主方法（会议稿主锚）

| ID | 类型 | 内容 | 来源 | claim ceiling | 缺口 |
|---|---|---|---|---|---|
| F2 | 图（复用） | received-power-aware adaptive CPR：CV gate → blind-h/effective-SNR → 13 dB → branch command → 单支执行 → common downstream DSP | `figures/fig2_adaptive_cpr.pdf`（V018 PASS） | select-before-execute 数据流 | 无 |
| F3 | 图（复用） | DA/NDA/oracle data BER（AWGN + 三档 GG，5–35 dB） | `figures/ccisp_fig2_ber.pdf`（V017 PASS） | fixed 分支工作区；高 SNR floor 随湍流上升 | 无 |
| F4 | 图（复用） | DA–NDA data-BER crossover（三档，14.5/16.9/16.0 dB） | `figures/ccisp_fig4_crossover.pdf`（V017） | 诊断性曲线交点（≠13 dB 控制门） | 无 |
| F5 | 图（复用） | common-payload BER-ratio reduction G_C + 95% CI（三档，5–25 dB，9 dB 峰值 0.8–1.5 dB） | `figures/ccisp_fig3_gain.pdf`（V017） | 低-中 SNR 集中，高 SNR 趋零 | 无 |
| T1 | 表（RECOMPUTE_ONLY） | 9 dB paired-seed mean G_C 三档复算（从 `selector_a_30seed.json` raw 确定性复算）+ 与 abstract 0.8–1.5 dB 比对 | 复算自权威 raw | headline 数字 machine-checkable | 无（一行复算） |

## Ch4 鲁棒性 / 边界

| ID | 类型 | 内容 | 来源 | claim ceiling | 缺口 |
|---|---|---|---|---|---|
| T2 | 表（SMALL_VALIDATION，优先） | 统一鲁棒性/边界表：P01 SNR 失配（5 cell 0.32–0.70 dB + adapter 恢复 4/5）+ P02 region retune（+0.454 dB）+ P04 continuous GG（+0.146 dB）+ P11 strong-traditional（20 dB partial） | P01/P02/P04/P11 现有数据 | 边界证据（NO_DIAGNOSTIC / RESOLVED_BY_RETUNE / ABSENT_ON_CONTINUOUS_GG）；非新算法 | 统一口径重算（adapter + continuous GG 统一表）→ 见 bounded-package 推荐包 |

## Ch5 部署实现

| ID | 类型 | 内容 | 来源 | claim ceiling | 缺口 |
|---|---|---|---|---|---|
| F6 | 图（复用 F2 + 增强） | branch router select-before-execute 细节（decide → DA 或 NDA 单支 → selected_rx） | F2 + `_a4_branchrouted_30seed.py:365-402` | code-path 回归（990/990 bit-exact） | 无（语义已在 V016 闭合） |
| F7 | 图（SMALL_VALIDATION） | full-grid branch-compute timing（formal 口径，warm-up + 重复 + 多条件） | 新跑（OLD-params 诊断有 33-cell 但无 authority） | 实现可行性；**非总接收机复杂度** | full-grid formal timing = 新跑（warm-up/重复/多条件） |
| T3 | 表（复用 A07 + 复算） | Q-format regret：Q(8,6) 0/132000 identity + gain-bearing regret +0.027 dB + 混合精度 ≤+0.0166 dB + uniform floor | `results/p03_fixed_point_codesign/phaseA_uniform.json` | **仅数值精度/实现可行性**；无 FPGA 资源 | float-vs-Q BER（formal CCISP grid）= 新跑 |
| T4 | 表（SMALL_VALIDATION，需 freeze） | coded chain FER：B0/B2/O2 + metamorphic gate exact-zero + AST 边界 | `results/p08r2_receiver_info_repair/*` | PARTIAL（无 pre-test freeze receipt） | freeze rerun = 受控新跑 |

## Ch6 结论

无新图。结论复述 9 dB 0.8–1.5 dB + 边界 + 实现验证 + 未来工作（AMC 一句，需用户授权新 GW）。

---

## 图表纪律

- 所有数字必须可溯源到 `asset-claim-matrix.yaml` 的 claim ceiling。
- 复用会议图前确认 V 编号（V017/V018/V024/V025/V026/V027/V028）PASS；PARTIAL 项（V025 Fig.1 0.32pt 债务）按用户决定保留。
- 新增图/表不得声称 INVALIDATED 资产（G1/P09）或 forbidden_revival 口径（26/29、uplink、1.2–1.9/3.1 dB）。
- 小验证图（F7/T4）必须先过 `bounded-package-recommendation.md` 的预注册 PASS/FAIL 才进正文。
