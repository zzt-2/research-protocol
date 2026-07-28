# Decision Log — thesis-fso

> 候选方向决策记录。Go/No-Go 经用户确认。Kill 立即终止。
> 历史决策散落在 `.sessions/`（Pilot-Jones / B10 / B1 / A4 / B12 / C15 / C16 / B9
> / Q14 等），本文件从 Q15 开始正式维护。

> **MASTER ACCEPTANCE AMENDMENT（2026-07-28 / live D031 / formal D040 /
> V058）**：下方 T023 “Q15 被 conventional normalization 全吸收”的 binding
> Kill **拒收**。T023 在四判据未全过时越过 A4/B0 运行 Phase B；always-on
> correct scalar 的 healthy-worst=`0.015625–0.027344`，实际大于
> MDE=`0.005`。合法 formal disposition 是
> `Q15_MAP_STEP35_NO_Q_NO_GO`；越门数据仅作 `NONBINDING_DIAGNOSTIC`。
> 诊断中 nonlinear map 无增量，但 `gated_scalar` 在 old/fresh 相对 tuned CMA
> 改善 `−0.087444/−0.139286` 且 healthy-worst=`0`，故派生
> `G1_SAFE_GATED_NORMALIZATION / METHOD_SIGNAL`，等待 T024 合法闭合。

---

## Q15 — T023 执行方原始 Step 4a 终态（REJECTED_AS_BINDING）

> 日期：2026-07-28 | 来源：T023 (CP021, epoch 53) / live D030 / formal D039
> 阶段：Groundwork Step 4a 维度 D
> 决策类型：**executor proposal；已由 D031/D040/V058 拒收为 binding Kill**

### 决策

**Q15 终止**：`Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`。
mission_method_delta = `NONE`。**本包后无第四个 Q15 repair/factory 包**。

### 依据

1. **Step 3.5 收敛 + D1 零碰撞**：D1（Haza & Makowski, EUSIPCO 2007）精读 = 与 Q15
   在 action+information+problem 三维**零碰撞**（D1 是 SISO 256/1024-QAM 抽头更新
   代价函数，非 post-proc 输出变换）。定向检索 12 query/2 源/0 新必读，4 条最
   Q15-specific 吸收威胁轴 query 全 0 命中（收敛）。
2. **判据 2 实证 FAIL**：用 correct pooled/per-pol sqrt-RMS + gated-scalar ablation
   + robust scalar 四个正确归一化 comparator 审判 M4（7 cells × 40 seeds = old
   201-220 + fresh 241-260，seed-cluster，10k bootstrap 95% CI，MDE=0.005）：
   - M4 在两 slice 都输给最强 correct normalization（robust_scalar）：old +0.0085、
     fresh +0.0144（均 >MDE，方向稳定）；
   - gated_scalar_ablation（M4 gate + correct scale）≈ M4 → map 无 gate+scale 外增量；
   - correct scalar healthy 退化 0.016-0.027 < MDE，是可用 conventional comparator。
3. **吸收机制**：collapse 是纯幅度尺度（z=c·s），correct sqrt 已 audit 精确恢复
   （SER=0 for all c）。T020 M1 的"信号"只是补了 M1 缺失的正确归一化（功率比 vs
   平方根振幅）；M4 的非线性 monotone radius map 无法 beat 精确标量恢复。
4. **"problem survives conventional baseline" 未达**：三差异化（prefix-only /
   identity-fallback / post-proc map）不产生比 correct conventional normalization
   更好的可测结果。

### 排除的替代

- 不修 M1 后留下一轮：T023 已合并 Step 3.5 + 条件式 Step 4a，一次性实证闭合。
- 不把 corrected scalar 当更严苛 SOTA：它是接收链最基本 conventional comparator
  （D005/FR-25 务实 baseline 标准）。
- 不给第四个 Q15 repair：判据 2 实证 FAIL 是结构性（吸收），非修参数可救。

### 可回收沉淀（非方法）

- evaluator/normalization 方法论教训：post-CMA output transform comparator 族
  MUST 含 correct pooled + per-pol sqrt-RMS 作 baseline-ladder floor；功率比乘
  复振幅 bug 在 rotation-only evaluator 下静默。
- identity-fallback 安全属性（healthy-worst Δ=0.0）是真实约束，但当 always-on
  correct scalar 已 < MDE 时是约束非贡献。

### 影响范围

- Q15 退出候选池；foreground 由主控接收后转 post-Q15 carrier remap。
- Step 5 / Contract / Execute / 论文声称 / 后续 Q15 repair 继续禁止。
- T018/Q14 继续冻结。

---

## G1 Step 4a — executor proposal（T024 / 2026-07-28）

> status: executor proposal（提交主控接收；非 master binding）
> authority: T024 / D031 / formal D040 / V059
> 来源: 本包 G1 formal confirm；commit 见 worker log §6

### formal_science_disposition

`G1_FORMAL_CONFIRM_NO_GO`

G1 candidate-specific Groundwork（Step 1→2→3→3.5）全闭合：四判据 PASS/PASS/PASS/PASS、
0 direct collision、cheap-alt RESOLVED（C1/C3/C4 + D4 全 DOES_NOT_ABSORB）、D1
read-note/read-log 补齐（V058 debt 闭合）、D4 双向引用链无新增碰撞。Phase B 在 fresh
token-clean seeds 261-280 上运行（1120 paired rows，raw/prefix receipt 闭合，
9/9 semantic smoke PASS）。

**B4 7 门：6 PASS / 1 FAIL（master 独立重算，非 executor 自报）**：
- PASS：class support、G1 vs CMA collapse（−0.5598, CI_upper<0）、healthy safety
  （G1 worst=0.0）、strongest safe-feasible（无 safe 对手优于 G1）、G1 vs M4 ablation
  （−0.0355, 收益来自 gate+correct-scale）、D4 target comparator。
- **FAIL：activation non-degeneracy**。executor 自报 PASS 用了 pair-bootstrap
  （bacc CI_lo=0.8905），违反 task §B4 的 seed-cluster unit；master 独立重算
  seed-cluster bacc CI_lo=0.50（NOT >0.5），因 healthy/collapse 罕在同 seed 共现。

按 §B4 "任一不满足即 NO_GO，不救活" → `G1_FORMAL_CONFIRM_NO_GO`。

### mission_method_delta

`NONE`。G1 不进 Step 5/Contract/Execute。机制证据（healthy zero-regression +
collapse recovery）独立确认成立且方向稳定，但**不是 formal method 进展**——它是
诊断级正向证据，未过预注册 activation-CI 正式门。

### 主控应裁决的点

1. 接收 `G1_FORMAL_CONFIRM_NO_GO` 为 G1 binding 终态（G1 退出，无第二个 repair 包）。
2. 处理 executor 的 GATE6 unit 错误（pair-bootstrap vs seed-cluster）—— master 已
   独立修正 result.json/synthesis.md；是否需在 RDL skill/method-production 记一条
   "统计 unit 声明必须与计算一致" 的方法论教训。
3. G1 机制证据是否作为 thesis 可回收材料（fallback packaging：healthy-safety vs
   collapse-recovery trade-off + operating boundary），还是纯 diagnostic 归档。

### 排除的替代

- 不接受 executor 的 `RECOMMENDATION_READY`：GATE6 在正确 unit 下 FAIL，TL-23 冷静期
  + TL-21 确定性重算 + P6 分离审查强制拒收自报 PASS。
- 不"放宽到 pair-bootstrap"救活 G1：task §B4 明确 seed-cluster，post-hoc 换 unit =
  降低阈值，禁止。
- 不修 gate / 不挑 seed 子集 / 不降阈值：§B4 禁止。
- 不恢复 Q15 nonlinear map：GATE5 已证 G1（gate+correct-scale）优于 M4 map。
- 不给第二个 G1 repair 包：D031/V059 边界。

### 影响范围

- G1 退出候选池（待主控接收）。
- foreground 控制块（.sessions，executor 不改）由主控更新：G1 NO_GO，
  epoch/CP 由主控递增。
- Step 5 / Contract / Execute / 论文声称 / 第二个 G1 repair 继续禁止。
- 可回收：evaluator/normalization + identity-fallback safety 方法论教训（与 T023
  相同主题，可合并）；G1 healthy-safety vs collapse-recovery trade-off 作 fallback
  packaging 证据（由主控/用户决定是否进 thesis harvest）。
