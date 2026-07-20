# Handoff: Baseline 裁决完成，条件授权 ML Scout batch（首选 C01）

> 来源: S003 | 交接目标: 在新对话设计并运行针对 inner-ring-collapse 的 bounded ML Scout batch
> 文件名: H003-ml-scout-batch-authorized.md
> 日期: 2026-07-20

## 到哪了（状态）

CB1 baseline adjudication shared batch（H002/D005 任务）**已完成**。裁决结论 = **`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`**：

- 主 comparator MMA（Yang-Werner-Dumont JSAC 2002）已实现 + 来源闭环 + 5/5 sanity tests PASS + 独立 verifier clean-room bit-identical 复现。
- axis 1（11 atlas-v1 cells × 10 seeds）：MMA 在 short cells (N=512) 跟 CMA 统计无差异；在 long cells (N=8192) **比 CMA 更差**且 1/10 diverge。
- axis 2（4 cells × {N=512, N=32768} × 5 seeds）：N=32768 MMA 2-3/5 diverge；CMA headroom 不降反升。
- 两个 cheap 替代解释（task-mismatch + under-convergence）都被排除；gap 稳定存在。
- D006 条件授权 bounded ML Scout（不强制本对话训练；本对话末尾只 commit）。

机制判读（重要 nuance）：headroom 的真因是 **block-end gradient descent (block_size=64) 在 SOP+GG 下的 seed-trajectory-dependent 收敛失败**，~40-60% seeds 坍缩到内环，**length-invariant**。信息可恢复（oracle affine 能恢复坍缩 seeds 到 PI-SER≈0）⇒ ML collapse detector 有机制合理性。

Portfolio 已扩到 C01-C04（`portfolio-refresh.v2-addendum.yaml`）：
- C01（首选，直接机制匹配）：causal collapse-early-warning detector
- C02：SSL anomaly detector
- C03：learned re-init policy（RL）
- C04：learned affine correction

## 下一步干什么

**在新对话（context 干净）**设计并运行 bounded ML Scout batch：

1. **必读优先级**（按顺序）：
   - `topic-index.md`（不变量 + 范围 + 当前位置）
   - `decisions.md` D006（PROBLEM_SURVIVES_CONVENTIONAL_BASELINE 裁决 + ML Scout 授权条件）
   - `baseline-adjudication-batch/artifacts/baseline-adjudication-v1-synthesis.md`（裁决完整论证）
   - `portfolio-refresh.v2-addendum.yaml`（候选 C01-C04 M-C-A 表达 + sequencing）
   - `baseline-adjudication-batch/mma_comparator.py` + `run_baseline_adjudication.py`（复用 comparator + runner）
   - `S003-baseline-adjudication.md` §后续（ML Scout 设计要点）

2. **首选 C01 design**（参 portfolio-refresh.v2-addendum.yaml）：
   - shared input contract: causal CMA-trace features（output_power, weight_norm, |z|²/R² ratio, update_norm per block）— CSI_NONE，receiver-visible only
   - 机制不同的 candidates（不是 model-name 排列组合）：
     - 监督式 collapse classifier（label = per-seed collapse ground truth from oracle affine disagreement，**FR-14 允许 label 但不允许 runtime oracle leakage**）
     - 自监督 anomaly detector（避免 label-derivation 顾虑）
     - 学习型 re-init / fallback trigger
   - 必须包含：no-change baseline (identity)、strongest simple comparator (blind affine)、必要 ablation
   - 禁止：oracle-supervised 方法当贡献；pilot-only mechanism variants；model-name 排列组合当多样性

3. **legal comparator 纪律（CRITICAL）**：
   - **Go baseline = nearest-16QAM AND MMA**（双重！ML 必须赢**两者**才算贡献，不只赢 CMA）
   - **oracle affine = Kill tool only (FR-21)**，不当 Go baseline (FR-25)
   - 同信息量：所有 candidates 和 baseline 用相同 receiver-visible 信息（CMA-trace features + z）

4. **claim ceiling = SLICE**。即使 ML 赢 nearest-16QAM + MMA，不自动晋级 DOMAIN（receiver-CSI / soft-coded axes 仍 blocked）。

5. **独立验证（P6 分离审查）**：必须有独立子 agent 复核 ML 结果。复核至少：公式/参数/identity gate / comparator 信息量一致 / no oracle leakage / claim ceiling。

6. **harvest**：完成后至少一条 harvest（POSITIVE_MECHANISM_SIGNAL if ML wins; LOCAL_NEGATIVE if ML doesn't beat both; SCOPED_NEGATIVE if ML only beats on some cells）。

## 纪律（和下一步直接相关的约束）

- **不修改 protected history**：canonical-state / portfolio/current.v1 / STATUS.v1 / B001-B003 / P03 Atlas / harvest/ledger.v1 / receipts 字节不变。新结果只进 `campaigns/science-scout-2026-07-20/` 和 `scout/cb1-.../ml-scout-batch/`。
- **不创建 legacy B004**：新 batch 用 B005+ ID。
- **复用 MMA comparator 模块**（H020）：`baseline-adjudication-batch/mma_comparator.py` 已 identity-gate + provenance 闭环，不要再重写 MMA。
- **CMA anchor identity gate**：每个 cell/seed 必须验证 `gradient == 'Godard-with-z'`（用 `cb1_cell_runner.standard_cma_godard_with_z`，不用 `_cma.py:CMAEqualizer2x2`——那是 scalar-error，H013 OPEN_ACKNOWLEDGED）。
- **主对话严禁 WebSearch/webReader**；论文精读/web 查询必须子 agent。
- **single consolidated commit at session end, no push**。
- **claim 诚实**：PROBLEM_SURVIVES ≠ ML 会赢。oracle affine 是上界工具，不是 baseline。profile.md "警惕主线急于给方向性结论"。

## 已知债务（续接者必须知道）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| H021 block_size=64 + block-end protocol 是 collapse 瓶颈 | 不能动 CMA anchor identity（会破 parity） | OPEN | future infrastructure task: per-symbol CMA/MMA variant with separate identity |
| H013 `_cma.py:CMAEqualizer2x2` scalar-error vs docstring "Godard-with-z" | canonical baseline identity 严格 | OPEN_ACKNOWLEDGED | DOMAIN 级 claim 或 formal 晋级前必须解决 |
| 16QAM R²=1.32 / R_R²=0.82 未 canonical 化 | baseline identity 完整 | DEFINED_IN_CB1_CLOSURE | 16QAM 正式晋级时进 canonical baseline identity |
| 子 agent verifier artifacts（`verifier_*.py`）保留在 `baseline-adjudication-batch/` | 独立审查记录完整 | KEPT_AS_AUDIT_TRAIL | 不删除；作为本轮 clean-room 验证证据 |

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - 声称1：裁决 = PROBLEM_SURVIVES_CONVENTIONAL_BASELINE → [PASS/FAIL + synthesis.md §6]
  - 声称2：MMA 5/5 sanity tests PASS + 独立 verifier bit-identical → [PASS/FAIL + test_mma_identity.py + verifier_mma.py]
  - 声称3：D006 条件授权 ML Scout（不强制） → [PASS/FAIL + decisions.md D006]
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on（system / governance-pilot / dual-pol-osl）—— 都是 active/dormant，无 conflicts
- [ ] 已确认当前范围未违反"明确不含"（不修改 protected history、不创建 B004、不自动晋级、不 push）

## 接口变更（本轮代码改动）

```yaml
# 新增 baseline-adjudication-batch 模块
type: new_module
location: projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/baseline-adjudication-batch/
files:
  - batch-contract.v1.yaml        # frozen contract
  - mma_comparator.py              # MMA implementation (identity-gated)
  - run_baseline_adjudication.py   # axis1+axis2 driver
  - tests/test_mma_identity.py     # 5/5 sanity tests
  - verifier_mma.py                # independent clean-room verifier (子 agent 产物)
  - verifier_run.py + verifier_diag.py + verifier_fairness.py + verifier_repro.json  # 子 agent 审查 artifacts
  - artifacts/baseline-adjudication-v1.json       # raw results
  - artifacts/baseline-adjudication-v1-synthesis.md  # synthesis
backward_compatible: true  # CB1 closure unchanged; CMA anchor byte-identical
qpsk_regression: PASS  # PI-SER=0.0 reproduces P03 v1
mma_qpsk_degeneracy: PASS  # MMA on QPSK (R_R^2=R_I^2=1.0) reduces to CMA, PI-SER=0.0

# provenance 追加（非 breaking）
type: additive_provenance
file: projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/formula-symbol-parameter-provenance.yaml
added_formulas: [F-MMA-COST, F-MMA-R2-16QAM]
added_symbols: [R_R² (MMA real-axis), R_I² (MMA imag-axis)]
added_parameters: [P-MMA-RR2-16QAM, P-MMA-RI2-16QAM]

# harvest 追加（非 breaking）
type: additive_harvest
file: projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/harvest-addendum.v1.yaml
added_entries: [H016, H017, H018, H019, H020, H021, H022]

# portfolio 追加（非 breaking）
type: additive_portfolio
file: projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/portfolio-refresh.v2-addendum.yaml
added_candidates: [C01, C02, C03, C04]
```

## 失败数据附录

无路线失败。CB1 closure + CMA anchor 全程 byte-identical 通过。MMA 实现一次通过 sanity gate，独立 verifier 复现无 bug。

pre-existing failure（与本轮无关）：`test_p03_claim_scope_receipt_binds_exact_assessment_and_validator` 在 base commit `65db4ef` 上就 FAIL —— P03 receipt SHA 与 assessment SHA 不匹配。

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| MMA R_R²=0.82 | abs(R_R² - 0.82) < 1e-12 | analytical E[x⁴]/E[x²] | PASS this round |
| MMA identity gate | gradient stamp = "Yang-Werner-Dumont MMA" | batch-contract identity | PASS this round |
| MMA clean QPSK converges | best per-symbol MSE < 0.05 | functional sanity | PASS this round |
| MMA clean 16QAM converges | best PI-SER < 0.02 | functional sanity | PASS this round |
| CMA anchor byte regression | PI-SER == 0.0 on P03 v1 cell | P03 v1 LOCAL_NEGATIVE | PASS this round |
| 独立 verifier bit-identical | clean-room MMA == main MMA, all 5 seeds | P6 separation | PASS this round |
| Adjudication decision rule | MMA headroom ≥ MDE on ≥ 2 cells AND N=32768 CMA headroom ≥ MDE on ≥ 1 cell | batch-contract.v1.yaml | 10/11 AND 4/4 PASS |

## 下一轮

在新对话（context 干净）：
1. 读 handoff 必读清单（topic-index → D006 → synthesis → portfolio-refresh.v2-addendum → mma_comparator → S003 §后续）
2. 完成接收方验证清单
3. 设计 ML Scout batch（首选 C01；参 portfolio-refresh.v2-addendum.yaml + S003 §后续 8 点设计要点）
4. 运行 + 独立验证 + harvest
5. 单次 consolidated commit，不 push
