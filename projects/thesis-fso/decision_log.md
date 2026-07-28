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
