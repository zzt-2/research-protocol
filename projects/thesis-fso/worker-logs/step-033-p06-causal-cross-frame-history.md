# step-033 — P06 E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION（一次性修复型 PROBLEM_BEARING_PROBE）

> 2026-07-31 | campaign P06 | family E（首包）| executor: 主线程内独立实现
> 上游：D044（绑定裁决，撤回旧 P06 window/complexity 入口）+ 修复旧 F3-A 科学无效性
> 验收：V070（独立 verifier）

## 任务

绑定裁决 D044 撤回旧 P06（E 信息复杂度边界 / window-length，重复 B1/P05-E），指定新 P06 = `E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION`：一次性修复型 PROBLEM_BEARING_PROBE，修复旧 F3-A 的科学无效性（`run_f3a_history.py:195-196` 把边际 MI max-difference 当成 conditional MI；`state/current.yaml:161-170` 已标 INVALIDATED）。不继承旧数值 +0.060 bits / +0.036 R²。本轮失败后关闭 E 族，不允许再开第二个 evaluator-repair 包。

## 冻结问题定义（M-C-A，读测试前冻结，见 FROZEN_CONTRACT.md）

- **M**：`standard_cma_godard_with_z`（mu=0.03, n_tap=11, R2=1.32, block_size=64，Godard-with-z 梯度），冻结传统接收机，只用当前帧可见摘要判断下一帧风险。
- **C**：源闭合 GG 动态 ρ=exp(-Δt/τ_c)，τ_c=1/(2π·f_G)，覆盖 f_G∈{30,100,1000}Hz；强湍流 (α,β)=(4.2,1.4)（params.py 真值）。frame=140k sym（dt=56µs）：ρ_frame = fg30→0.99 / fg100→0.97 / fg1000→0.70。
- **A**：过去若干帧的 receiver-visible 状态是否在 current-only/persistence/EWMA/AR(1) 之外对下一帧失效/性能提供严格因果增量。
- features(t) 仅用 frame≤t 接收机可见量；target(t+1)=冻结接收机下一帧 fixed-label SER/failure。禁 h/α/β truth/未来 trace/TX label/seed/cell-id/target-frame 残差作特征。

## Phase 0：物理与身份门（ALL PASS，6 conditions）

frame-level GG state transition（复用 `_gg_time.py` AR(1) 块级 `gg_time_envelope_blockwise`，frame=140k sym dt=56µs）。6 conditions 全 PASS：
- **GG 边缘**：KS 0.056–0.144（< 0.15 阈值，`gar` 法保精确 Gamma 边缘）。
- **块 ACF**：经验 ACF[lag] 与 ρ^lag 一致，max relerr < 0.2%（fg1000 0.18%）。
- **ρ 一致**：rho_frame fg30=0.9895 / fg100=0.9654 / fg1000=0.7034（与 exp(-Δt/τ_c) 解析一致）。
- **身份**：冻结 CMA 重跑 zX relerr=0（确定性 byte-identical），0 divergence。

## Phase A：问题与严格因果信息门 → `NO_CAUSAL_HISTORY_INCREMENT`

dev fail events 428/1140（frac=0.375，floor=30 MET）。dev 调参（EWMA α=0.9、K=5、ridge λ=10，dev history R² 优势 +0.217）。test（180 trajectory 配对）：

| 模型 | MAE | RMSE | R² |
|---|---|---|---|
| unconditional | 0.19936 | 0.29825 | -0.106 |
| current-only ridge | 0.17629 | 0.27793 | 0.040 |
| **history-expanded ridge** | 0.16527 | 0.23398 | **0.320** |
| **persistence** | 0.05296 | 0.10287 | **0.853** |
| EWMA | 0.05400 | 0.10299 | 0.853 |
| AR(1) | 0.06164 | 0.10489 | 0.848 |

history−current MSE 减少per-traj macro mean=2.25e-02 CI=[4.72e-03, 4.68e-02]（CI_lo>0，history 确实 > current-only，统计显著）。**但 history R²=0.32 ≪ persistence R²=0.85**。

**逐 condition R²（确认 robust，含动态 fg1000）**：fg30{15,20}: persistence 0.95/0.94 vs history 0.48/0.72；fg100{15,20}: persistence 0.94/0.90 vs history 0.56/0.88；**fg1000{15,20}: persistence 0.75/0.68 vs history 0.04/0.37**。所有 condition persistence >> history。

**结论**：严格因果 history 在 current-only 之外有真实（统计显著）预测增量，但**更便宜的常规 temporal baseline（last-value persistence）已经远优解决**（test R² 0.85 vs history 0.32，逐 condition 0.68–0.95 全胜）。无可区分 deployable 方法 → `NO_CAUSAL_HISTORY_INCREMENT`。修复了旧 F3-A 的 conditional-MI 误标（旧 +0.060 bits/+0.036 R² 不继承，仅历史保留）。

## Phase B/C：NOT RUN

Phase A 未过 signal 门（NO_CAUSAL_HISTORY_INCREMENT 非 CAUSAL_HISTORY_INFORMATION_SIGNAL），按冻结合同 Phase B/C 不运行。只 harvest observability boundary（见终态）。

## 终态 verdict

**`NO_CAUSAL_HISTORY_INCREMENT`**（method-production 终态集）。有效 P06（计 6/10），不产 METHOD_SIGNAL，仍 0 active carrier。E 族（因果跨帧历史信息）首包关闭，按绑定裁决不允许再开第二个 evaluator-repair 包。修复了旧 F3-A 科学无效性，旧数值不继承。

**harvest（有界负面 + 可观测性边界）**：
- (a) "冻结 standard-CMA 接收机的下一帧失效/性能被 last-value persistence 以 R²≈0.85 解决；history features 有真实但 sub-persistence 增量"——Ch4/Ch3 receiver-observability 边界证据（跨帧信息被帧间持续性主导，非新方法空间）。
- (b) "旧 F3-A 的 conditional-MI 误标被严格因果 held-out 预测增量取代"——方法论教训（marginal-MI max-difference ≠ conditional-MI），可写入 thesis 方法论附录。
- (c) 物理诚实：deployable frame rate（dt=56µs）≪ τ_c（0.16–5.3ms），只有 fg1000 有非平凡跨帧动力学，仍被 persistence 主导。

## 产物

- 冻结合同：`projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/src/p06/FROZEN_CONTRACT.md`
- 实现：`src/p06/run_p06.py`（Phase 0 + 数据集构建）、`src/p06/build_datasets.py`（分块）、`src/p06/build_all.py`（master）、`src/p06/phaseA_eval.py`（Phase A 评估）、`src/p06/verify_p06.py`（独立 verifier）
- artifacts：`projects/simulation/results/p06_causal_cross_frame_history/`（p06_phase0_physical_identity.json、chunks/、p06_phaseA_result.json、p06_raw_per_frame_rows.json、p06_verifier_result.json、p06_terminal_verdict.json）
