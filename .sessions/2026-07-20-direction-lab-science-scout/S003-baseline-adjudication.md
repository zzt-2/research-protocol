# [S003] Baseline adjudication shared batch — PROBLEM_SURVIVES_CONVENTIONAL_BASELINE

> 2026-07-20 | SCIENCE_SCOUT — CB1 baseline adjudication + Portfolio refresh | 状态: 完成

## 目标

按 H002 在 CB1 16QAM inner-ring collapse headroom 上做一个轻量、共享、来源闭环的传统 baseline 裁决，回答：gap 是欠收敛、单模 baseline 对 16QAM 任务失配，还是经过合理传统 comparator 仍存在？同时准备 2-4 个机制不同、共享基座的 Portfolio 候选。连续推进到一次真正的科学裁决，不每步问用户。

## 记录

### 接收方验证（H002）

- Claim 1（D005 取代 D004 直接 ML 授权）：PASS（decisions.md:115 D004 superseded；decisions.md:154 D005 取代声明）。
- Claim 2（H001 标 superseded）：PASS（H001 顶部"SUPERSEDED by D005 / H002"）。
- Claim 3（主 Skill 路由 baseline-adjudication）：PASS（SKILL.md + references/baseline-adjudication.md 均存在并已读）。
- depends_on 3 项（governance-pilot dormant / system active / dual-pol-osl active）全部稳定；conflicts_with 空。
- 当前范围 = 轻量 baseline 裁决 + Portfolio 维护，未触碰"明确不含"任何项。

### Batch contract 冻结（batch-contract.v1.yaml）

- 主 comparator: MMA (Yang-Werner-Dumont JSAC 2002)，cost `J=E[(y_R²−R_R²)²+(y_I²−R_I²)²]`，R_R²=R_I²=0.82 for square 16QAM。
- 诊断 anchor: standard_cma_godard_z（Atlas v1 不变）。
- Kill tool: oracle affine（仅 scoring）。
- 条件扩展: DD-LMS cascade（pre-loaded 但不触发——MMA 失效模式是 thermal divergence 不是 under-convergence）。
- 决策规则：MMA headroom ≥ MDE on ≥ 2 atlas-v1 cells AND N=32768 CMA headroom ≥ MDE on ≥ 1 cell ⇒ PROBLEM_SURVIVES_CONVENTIONAL_BASELINE。

### 来源闭环（子 agent + 主线）

- MMA 原始：Yang-Werner-Dumont JSAC 2002 Eq.(12)-(13)（修正了之前 Oh-Un 1982 / Wesemann 1998 的误归因）。
- dual-pol 扩展：Kikuchi JLT 2016 §IV.B + Fludger OFC 2014 W3K.2。
- 3 篇独立复现（Mendes-Filho SSP 2009 / Akande-Joya EURASIP 2016 / Liu TSP 2021）逐字复现 cost 形式。
- R_R²=R_I²=0.82 推导 + 数值验证（主线本地 python 完全匹配）。
- MMA 是 16QAM inner-ring collapse 的直接对策（Johnson PIEEE 1998 §III-IV + Mendes-Filho SSP 2009 intro + Liu 2021 intro 三方独立证据）。

### MMA 实现 + identity gate

- 新建 `baseline-adjudication-batch/mma_comparator.py:mma_yang_werner_dumont`，结构对称于 `cb1_cell_runner.standard_cma_godard_with_z`（公平性 parity：相同 block_size=64 / 中心抽头 init / μ=0.001 / n_tap=11 / eval window / paired seeds / CSI_NONE / divergence criteria）。
- 5/5 sanity tests PASS：
  1. R_R²=0.82 数值（mma_dispersion_constants_sq_qam16）
  2. identity gate 梯度戳记
  3. clean QPSK 上 MMA 退化到 identity filter
  4. clean 16QAM 上 MMA 收敛
  5. CMA anchor 仍 byte-identical 到 P03 v1 PI-SER=0.0

### 裁决结果（axis 1 + axis 2）

- **Axis 1（11 atlas-v1 cells × 10 seeds）**：MMA 在 8 short cells (N=512) 跟 CMA 统计无差异（|Δ PI-SER|<0.004）；在 3 long cells (N=8192) **比 CMA 差** 0.04-0.06 + 1/10 diverge。
- **Axis 2（4 cells × {N=512, N=32768} × 5 seeds）**：N=32768 时 MMA **2-3/5 seeds diverge**，near-PI-SER 比 CMA 高 0.2-0.3。CMA 在 N=32768 上 headroom 不降反升（3/4 cells）。
- **决策规则**：10/11 atlas-v1 cells MMA headroom ≥ MDE PASS；4/4 N=32768 cells CMA headroom ≥ MDE PASS；合取 → **PROBLEM_SURVIVES_CONVENTIONAL_BASELINE**。

### 独立 verifier

- 子 agent clean-room 重写 MMA（`verifier_mma.py`），未看主线 `mma_comparator.py`。
- 在 16qam-snr20-sop40e-N32768 cell × 5 seeds 上 bit-identical 复现主线 MMA（相同 w_norm、相同 divergence、相同 near_pi_ser）。
- 诊断 w_norm 飙升（最高 17.5 vs CMA 1.2）= 合法 thermal divergence（μ∈(5e-4, 1e-3) 稳定性边界，MMA 三次误差 vs CMA 二次），**非 bug 非不公平**。
- μ=1e-4 sweep 下 MMA 仍比 CMA 差（5 seeds mean=0.60 vs CMA 0.52），结论稳健。

### 机制判读

- **(a) task-mismatch** 排除：MMA（任务适配、内环坍塌的教科书对策）并没更好甚至更差。
- **(b) under-convergence** 排除：N=32768（64× 原长度，在 sat.1553 ~1e5 regime 内）未消除 headroom，3/4 cells 反而更大。
- **真因**：block-end gradient descent (block_size=64) 在 SOP-rotation + GG-fading 下有稳定的 seed-and-trajectory-dependent 收敛失败，~40-60% seeds 坍缩到内环，与 N 无关（per-seed 诊断：N=512 坍缩的 seed 在 N=32768 可能恢复，反之亦然，但坍缩率稳定）。
- **信息可恢复性**：oracle affine 在长 N cells 上能恢复坍缩 seeds 到 PI-SER≈0，说明恢复信息在 receiver-visible z-stream，只是 CMA/MMA trajectory 拿不到 ⇒ ML collapse detector 有机制合理性。

### Portfolio refresh（候选 C01-C04）

- **C01**（首选，直接机制匹配）：causal collapse-early-warning detector（监督式 binary classifier on CMA-trace features）。
- **C02**：SSL anomaly detector（避免 FR-14 label-derivation 顾虑）。
- **C03**：learned re-init policy（RL，action-based 而非 detection）。
- **C04**：learned affine correction（trace-conditioned，机制是 post-hoc correction）。
- 全部共享 CSI_NONE CMA-trace input contract + nearest-16QAM+MMA dual Go comparator + oracle Kill only。

### Harvest H016-H022

- H016 BASELINE_ADJUDICATION: MMA task-correct comparator 来源闭环
- H017 FAILURE_MECHANISM: length-invariant seed-trajectory-dependent collapse
- H018 LOCAL_NEGATIVE: MMA 不优于 CMA（教科书结果在 OSL 不成立）
- H019 EVALUATION_INSIGHT: headroom 对 N 非单调
- H020 REUSABLE_ASSET: MMA comparator 模块
- H021 INFRASTRUCTURE_GAP: block-end protocol 是瓶颈但动不了 CMA anchor identity
- H022 METHOD_SIGNAL (conditional): 信息可恢复性 ⇒ ML collapse detector 机制合理

## 决策引用

- D005：CB1 降为 DIAGNOSTIC/SLICE；先做轻量传统 baseline 裁决（前置）
- D006：新建。裁决 = PROBLEM_SURVIVES_CONVENTIONAL_BASELINE；条件授权 ML Scout（本 session 做出）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。baseline 裁决 + Portfolio 维护全部在 H002 当前范围内。ML Scout 留给下一对话（D006 条件授权但不强制在本对话训练）。

## 后续（下一对话 ML Scout 设计要点）

1. **首选 C01**（直接机制匹配）：causal collapse-early-warning detector。
2. **shared input contract**：CSI_NONE causal CMA-trace features（output_power, weight_norm, |z|²/R² ratio, update_norm per block）。
3. **dual Go comparator**：nearest-16QAM AND MMA。ML 必须赢**两者**，不只赢 CMA。
4. **oracle affine 仅 Kill**（FR-21/FR-25）。
5. **必须包含**：no-change baseline (identity)、blind affine、必要 ablation。
6. **禁止**：oracle-supervised 方法当贡献；pilot-only mechanism variants；model-name 排列组合当多样性。
7. **claim ceiling = SLICE**：不自动晋级 DOMAIN。
8. **独立验证**（P6 分离审查）必须。

**债务清单**：
- H021 OPEN：block_size=64 + block-end protocol 是 collapse 瓶颈但动 CMA anchor identity 会破 parity。Per-symbol 变体是 future infrastructure task。
- 子 agent 创建的 verifier artifacts（`verifier_mma.py`, `verifier_run.py`, `verifier_diag.py`, `verifier_fairness.py`, `verifier_repro.json`）保留在 `baseline-adjudication-batch/` 作独立审查记录，不删除。
