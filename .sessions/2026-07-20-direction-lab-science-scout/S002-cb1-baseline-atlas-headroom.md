# [S002] CB1 baseline Atlas 发现 16QAM headroom；记录 scoped positive + harvest + handoff

> 2026-07-20 | SCIENCE_SCOUT — CB1 实施 + baseline Atlas + 独立验证 | 状态: 完成（本轮收尾）

## 目标

完成 CB1 modulation-generic closure 的实施、baseline-only Atlas 运行和独立验证。根据 headroom 结果决定是否触发 ML Scout，或记录 scoped positive 并 handoff 到新对话。

## 记录

### CB1 实施完成

- `_dual_pol_channel.py` 参数化 `modulation='qpsk'|'qam16'`；QPSK 路径字节不变（11/11 closure tests PASS + 6/6 existing dual-pol regression PASS）。
- 16QAM 路径走 `_modulation.qam16_mod`（Gray map，/sqrt(10) 归一化）。
- 新增 modulation / bits_per_symbol 字段到返回 dict。
- provenance 硬门 `formula-symbol-parameter-provenance.yaml` 建立：11 公式 / 22 符号 / 14 参数，全部 source-typed（5 PRIMARY_LITERATURE + 4 STANDARD_CONVENTION + 1 DERIVED_IN_PROJECT [R²=1.32] + 1 DEFINED_HERE [PI-SER]）。

### Baseline Atlas 结果（独立验证 CONFIRM）

11 个 16QAM 代表 cells × 10 paired seeds：

| cell | snr | f_g | sop | N | nearest PI-SER | oracle PI-SER | headroom | decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| snr05-nominal-short | 5 | 30 | 4e-6 | 512 | 0.662 | 0.689 | 0.000 | LOCAL_NEGATIVE |
| snr10-nominal-short | 10 | 30 | 4e-6 | 512 | 0.488 | 0.416 | 0.071 | ADVANCE |
| snr15-nominal-short | 15 | 30 | 4e-6 | 512 | 0.365 | 0.144 | 0.221 | ADVANCE |
| snr20-nominal-short | 20 | 30 | 4e-6 | 512 | 0.333 | 0.022 | 0.311 | ADVANCE |
| snr25-nominal-short | 25 | 30 | 4e-6 | 512 | 0.333 | 0.000 | 0.333 | ADVANCE |
| snr20-fg100-short | 20 | 100 | 4e-6 | 512 | 0.334 | 0.022 | 0.313 | ADVANCE |
| snr20-fg1000-short | 20 | 1000 | 4e-6 | 512 | 0.341 | 0.020 | 0.321 | ADVANCE |
| snr20-sop40e-short | 20 | 30 | 4e-5 | 512 | 0.333 | 0.022 | 0.311 | ADVANCE |
| snr10-fg100-long | 10 | 100 | 4e-6 | 8192 | 0.427 | 0.373 | 0.055 | ADVANCE |
| snr15-fg1000-long | 15 | 1000 | 4e-6 | 8192 | 0.322 | 0.174 | 0.148 | NON_DECISIVE |
| snr20-nominal-long | 20 | 30 | 4e-6 | 8192 | 0.306 | 0.073 | 0.232 | NON_DECISIVE |

**SLICE verdict**: LOCAL_HEADROOM_FOUND。10/11 cells headroom ≥ MDE 0.005；max 0.333 (66× MDE)。

**机制诊断**：standard-CMA 在 SNR≥15 dB 时约 50% seeds 坍缩到 16QAM 内环（|z|²→0.2），per-seed PI-SER≈0.67-0.78；oracle affine 能把坍缩的 seeds 恢复到 PI-SER=0.0。headroom 主要来自这个 bimodal collapse。snr=5 dB 是 LOCAL_NEGATIVE（AWGN 主导，oracle 也救不回）。

**QPSK 回归**：P03 v1 anchor cell (snr=20, seed=11) PI-SER=0.0，字节复现 P03 v1。

### 独立验证（CONFIRM）

独立 verifier 子 agent（clean-room，只用 canonical prompt013）独立复现了：
- QPSK anchor PI-SER=0.0（PASS）
- 16QAM snr=20/25/5 三 cell 的 PI-SER 和 headroom（MATCH）
- "collapse to inner ring" 模式真实（snr=25 时 5/10 seeds 坍缩）
- headroom 定义正确（oracle = Kill tool per FR-21，nearest = Go baseline per FR-25）
- CMA 身份发现（_cma.py scalar-error vs prompt013 Godard-with-z）由直接代码检查确认

verifier caveat：R²=1.32 for 16QAM 只在 CB1 closure 中定义，不在 canonical-state 中（scope limitation，不是 bug）。

### 关键基础设施发现（H013）

`_cma.py:CMAEqualizer2x2.equalize` 的 weight update（lines 163-166）是 **scalar-error CMA**（梯度 ∝ (R²−|z|²)·r*，无 z 因子），但其 docstring 和 canonical baseline 身份声明是 "Godard-with-z"。真正的 Godard-with-z 只在 `prompt013.run_cma_diagnostic(mode='standard')`（梯度 ∝ (R²−|z|²)·z·r*）中。这不影响任何 protected history（P03 经 run_b001 用 prompt013），但必须在任何 DOMAIN 级 claim 或 formal 晋级前解决。H013 OPEN_ACKNOWLEDGED。

### 决策（D004）：本轮不触发 ML Scout，记录 scoped positive + harvest + handoff

**决策**：本轮不触发 ML Scout batch。记录 scoped positive（H010-H015）并 handoff 到新对话触发 ML Scout。

**理由**：
1. **上下文预算**：本轮已完成 state recovery + 3 资产盘点 + provenance + closure 实施 + baseline Atlas + 独立验证。ML Scout batch 需要独立、clean-context 的对话（设计机制不同的 candidates、shared contract、ablation）。
2. **科学严谨（user profile "警惕主线急于给方向性结论"）**：headroom 真实，但 "ML 能否在合法 comparator 下利用这个 headroom" 是独立问题。本轮结论是 "headroom found; ML Scout authorized but not yet run"，不是 "ML 会赢"。
3. **机制针对性强**：16QAM headroom 由 inner-ring collapse 驱动，ML Scout 应针对 collapse 设计（causal CMA-state features + 学习型 re-init），不是 generic modeling。设计工作应在 clean context 下做。
4. **user profile "务实可毕业" + "多挑候选保留余地"**：先记录这个 defensible thesis result（16QAM boundary mapping + headroom finding），再决定 ML Scout 还是先扩到其他候选（U24 RC2 cluster）。

这不违反用户 "不要在每个小步骤等待用户确认" —— 本轮在授权内连续推进到了 baseline Atlas + 独立验证 + harvest，handoff 是 campaign 的自然 checkpoint，不是停下问用户。

## 决策引用

- D001：CB1 modulation-generic closure 选为首轮共享能力（新建）
- D002：授权迁移 READ_ONLY_MIGRATION_PREVIEW → SCIENCE_SCOUT（新建）
- D003：16QAM R²=1.32 provenance 硬门（新建）
- D004：本轮不触发 ML Scout，记录 scoped positive + harvest + handoff（新建）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。CB1 实施、baseline Atlas、独立验证、harvest、handoff 全部在本专题"原始目标"和"当前范围"内。ML Scout 留给下一对话也是 campaign contract 的合法 rotation（"If headroom found: batch ML Scout" 不要求同一对话完成）。

## 后续（下一对话 ML Scout 设计要点）

1. **targeted at inner-ring collapse**：candidates 应该有 mechanism 针对 collapse detection（不是 generic classifier）。
2. **shared input contract**：causal CMA trace features（output_power, weight_norm, |z|² vs R² ratio, update_norm）。
3. **legal Go baseline**：nearest-16QAM（不是 oracle affine — 那是 Kill tool）。
4. **必须包含**：no-change baseline（identity），strongest simple comparator（blind affine），必要 ablation。
5. **不要包含**：oracle-supervised 方法（FR-14 先验对照除外，但不能当贡献）；pilot-only mechanism variants。
6. **QPSK 回归**：必须保留 QPSK anchor cell 的 PI-SER=0.0 作为 sanity check。
7. **claim ceiling**：SLICE。即使 ML 赢 nearest-16QAM，不自动晋级 DOMAIN（其他 blocked axes 仍 open）。
8. **independent verifier**：必须有独立子 agent 复核（P6 分离审查）。

**债务清单**（本轮新增，用新 projection 解决）：
- `_cma.py:CMAEqualizer2x2` scalar-error 与 docstring/canonical identity "Godard-with-z" 不一致（H013）。
- `canonical-state.yaml::simulator.sha256=537dce98` 与 worktree 实际 `3d02eaa3`（行尾差异）（已在 authorization-projection.v1.yaml 登记）。
- 16QAM 的 R²=1.32 canonical 化（目前只在 CB1 closure 中定义，不在 canonical-state 中）。
- P03 `test_p03_claim_scope_receipt_binds_exact_assessment_and_validator` 在 base commit `65db4ef` 上就 FAIL（pre-existing，与本轮无关）—— `claim-scope-validation-receipt.v1.yaml` 的 SHA 与 `claim-scope-assessment.v1.yaml` 不匹配；须在专门治理任务中修复。
