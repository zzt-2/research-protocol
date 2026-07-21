# Handoff: C11 legality verdict B — D010 C11 阳性撤回

> 来源: S008 / D011 / V003 | 交接目标: 用户审 C11 合法性裁决；通过后开新对话决定下一批方向
> 日期: 2026-07-21
> 文件名: H008-c11-legality-verdict-b.md
> 取代: H007（H007 不删除，标 amended——fairness-survives、μ=0.03、min_z2 ceiling 部分仍有效；C11_fixed_mu 4/7 阳性子结论撤回）

## 到哪了（状态）

外部评审要求：合法化（统一复数约定 / 无未来信息 / 同 pass 预算 / dd_step=0 身份门）前提下重测 C11。S008 连续推进到最终裁决：

- **根因调查完成（systematic-debugging Phase 1-3）**：C11 原实现 3 个合法性缺陷全部独立定位。R001-c11-legality-root-cause.md 记录。
- **TDD RED → GREEN**：13 tests 全 PASS（8 gates + 4 OLD-impl bug 确认 + 1 contract-path），独立 verifier 10 项复核全 CONFIRM。
- **裁决 = `B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`**：
  - macro paired Δ (C11_legal − fixed_μ) = **+0.01445**（C11 更差），95% CI = [−0.00022, +0.04113]
  - 2/7 long cells 显著**更差**（snr10-fg100-long +0.025；snr15-fg1000-long +0.077）
  - 0/7 cells 显著更好；5/7 short cells 实质 tie（|Δ| < 0.001）
  - worst-cell = +0.077（不可接受退化）
  - stage2_max_visits_per_sample_global = 1（因果 one-pass 验证）
- **D010 第 4 点（C11_fixed_mu 4/7 阳性 method signal）撤回**，reclassified as implementation/confound diagnostic。
- **forward rule 第 2 comparator 修正**：`oracle_affine_16qam`（D010 line 352 标 "blind"）→ `blind_affine_compare_16qam`（真正的 receiver-visible）；`oracle_affine_bound_16qam` 是 Kill bound only（FR-21/FR-25）。
- protected history 全部未改；无 ML；无 B004；无 detector；无 push。

git HEAD：c11-legality-batch-v1 待 stage，consolidated commit。

## 关键科学发现

1. **C11 原实现的 4/7 阳性完全是 implementation artifact**。合法化后信号消失甚至反向，long cells 显著更差。
2. **复数约定突变可量化**：stage-2 用 `np.vdot`（Hermitian）vs stage-1 用 `r @ w`（bilinear），dd_step=0 时 max|ΔzX| ≈ 1.97（≈ 16QAM 星座点间距）——"no-op" 不是 no-op。
3. **DD-LMS 对已收敛 fixed-μ 权重的因果 per-symbol update 反而扰动权重**：long cells C11_legal 显著更差；short cells 实质 tie。原 "4/7 改善" 完全靠非因果 full-stream second/third pass 的离线平滑。
4. **fixed-μ CMA μ=0.03（继承 D010 HF6）在合法比较下仍是 winner**，无任何方法超越它。
5. **blind vs oracle affine 代码确认分离**：cb1_evaluator.py:106/132 两个函数签名/输入语义明确不同。Forward rule 已修。

## 不要做什么

1. **不要**把 VERDICT B 解读成 "DD-LMS 在该信道下总是有害"：这是 LOCAL_RESULT_SLICE（7 cells × 10 seeds × 1 switch policy × 1 μ），不能外推。legal C11 在 short cells 与 fixed_μ 实质 tie，DD 没用而非有害。
2. **不要**重启 C04/C09 learned corrector 借口"C11 留下 0.01 margin"：margin 已撤回，corrector 必须超越 `blind_affine_compare_16qam`（receiver-visible），不是超越 C11。
3. **不要**修改 B01 raw / B01-R raw / B001-B003 / P03 / CB1 raw / canonical-state / D010 / H007 / V002（全部保留为历史；D010/H007 标 amended 不删）。
4. **不要**创建 legacy B004；不要训练 ML；不要写论文正文；不要 push；不要扩候选池；不要启动 detector/B02（本轮 brief 明示）。
5. **不要**用 D010 line 352 的 forward rule 原文（已修正）；用 c11-legality-batch-v1/batch-contract.v1.yaml 的新 forward rule。
6. **不要**把裁决 C 当 fallback：所有门 PASS，没有架构阻塞；C 只能用于真正能力缺失。

## 必读（按优先级）

1. `.sessions/2026-07-20-direction-lab-science-scout/H008-c11-legality-verdict-b.md`（本文件）
2. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c11-legality-batch-v1/artifacts/synthesis.v1.md`（含 §0 TL;DR + §4 结果表 + §9 下一步）
3. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` D011（本轮裁决；D010 标 amended）
4. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c11-legality-batch-v1/R001-c11-legality-root-cause.md`（Phase 1-3 根因，含 b01_candidates.py 行号定位）
5. `.sessions/2026-07-20-direction-lab-science-scout/verifications.md` V003（独立 verifier 10 项 CONFIRM）
6. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（D011-amended）
7. `.agents/skills/research-direction-lab/references/evidence-and-claims.md` + `baseline-adjudication.md`（不变）

## 接口变更（本轮新增，下一对话可复用）

```yaml
# c11-legality-batch-v1/c11_causal.py（新模块）
c11_cma_dd_lms_causal(rX, rY, *, n_tap, cma_mu, cma_R2, cma_block_size,
                       dd_step_size, switch_point_block, hard_decision_fn) -> dict
  # UNIFIED bilinear r@w convention; causal one-pass; identity gate at dd_step=0.
  # 返回含: zX, zY, diverged, divergence_symbol, final_w_norm, init_w_norm,
  #         stage_events (per-sample 'CMA'/'DD'/None), stage_1, stage_2, provenance.
stage1_weights(rX, rY, *, n_tap, cma_mu, cma_R2, cma_block_size)
  -> (wxx, wxy, wyx, wyy)   # 暴露给 stage-1 identity 测试
stage2_filter_output(wxx, wxy, wyx, wyy, r) -> complex   # 暴露给 convention 测试
reset_access_counts() / get_access_counts()  # 访问计数 instrumentation

# c11-legality-batch-v1/run_c11_legality_batch.py（新 runner）
DD_STEP_GRID = [0.0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4]   # frozen，含 0
SWITCH_OFFSETS = [0, 1, 2]
VALIDATION_SEEDS = [31, 32, 33, 34, 35]  # disjoint from B01-R's 11-15
TEST_SEEDS = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]  # disjoint from B01-R's 21-30
FROZEN.cma_mu_fixed = 0.03  # inherited from B01-R HF6, NOT re-tuned
```

下一对话若要复用合法 CMA→DD-LMS 实现，import `c11-legality-batch-v1.c11_causal`，不要再用 `fairness-batch-b01.b01_candidates.c11_cma_dd_lms_cascade`（有 D1+D2+D3 缺陷）。

## 失败数据附录

| 现象 | 失败模式 | 数据 |
|---|---|---|
| C11 原实现 dd_step=0 vs anchor μ=0.03 | "no-op" 不是 no-op（D1 约定突变） | max\|ΔzX\| ≈ 1.97，max\|ΔzY\| ≈ 1.71 |
| C11_legal vs fixed_μ on long cells | 因果 per-symbol DD 反而扰动已收敛权重 | snr10-fg100-long Δ=+0.025 CI [+0.00078, +0.05117]；snr15-fg1000-long Δ=+0.077 CI [+0.017, +0.139] |
| C11_legal vs fixed_μ macro | 无显著优势，CI 含 0 且上界远离 0 | macro = +0.01445, CI = [−0.00022, +0.04113] |
| best_dd_step on validation | DD stage 几乎没用（0 与 3e-4 接近） | val mean PI dd=0: 0.139 (offset +2); dd=3e-4: 0.124（轻微好，但 test 上反向） |
| D010 line 352 forward rule label | oracle_affine_16qam 被错标 "blind" | cb1_evaluator.py:132 oracle_affine_bound_16qam 用 truth_calibration；cb1_evaluator.py:106 blind_affine_compare_16qam 不用 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| D007 #2 convergence N | 长序列闭合 | PARTIALLY_CLOSED（N=8192 上 paired CI 显著，未到 ~1e5） | 后续 batch 在 N=32768/65536 上验证 |
| D007 #4 oracle recoverability | receiver-visible 信号 | DOWNGRADED（4-cat 标签揭示 inner-ring 群体远小于预期） | 更丰富 oracle 类或 representation learning |
| detector target thin | VERDICT A 但仅 2 个 two-class cells | REPORTED（min_z2 AUROC=1.000 ceiling；lead time 负） | B02 若跑需换目标（lead-time maximization） |
| C11 dd_step 与 switch_point 在 long cells 上不稳 | 因果 DD 扰动效应 | NEW（本轮发现） | 若未来要重新评估 DD-LMS，需多 switch policy + 更稳的 dd schedule |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| C11 identity gates (8) | 全 PASS | batch-contract identity_gate_tests | 8/8 PASS（V003 独立复核） |
| C11_legal > fixed_μ macro | CI 上限 < 0 且 mean ≤ −0.005 | batch-contract Verdict A | FAIL（CI +0.041；mean +0.014） → Verdict B |
| C11_legal worst-cell | Δ ≤ 0 | batch-contract Verdict A | FAIL（+0.077） |
| No-leakage seed split | val/test/B01-R 全不相交 | batch-contract forbidden | PASS（代码 assert） |
| Stage2 access budget | max visits/sample = 1 | batch-contract one_pass | PASS（global max=1） |
| Protected history 字节未改 | git diff 在 protected paths 上空 | AGENTS.md / contract | PASS（git diff 空） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（不变量未变）
- [ ] 已验证 D011、synthesis.v1.md、result.v1.json 至少 3 条关键事实：
  - [ ] macro paired Δ = +0.01445（`result.v1.json#adjudication.macro_paired_delta_mean`）
  - [ ] 2/7 long cells CI 下限 > 0（`result.v1.json#adjudication.per_cell_paired_ci_95`）
  - [ ] 13 tests 全 PASS（独立 verifier V003 V1）
- [ ] 已检查 `_registry.yaml`（无变化）
- [ ] 已确认 B001-B003 / P03 / CB1 raw / canonical-state / B01 raw / B01-R raw 未改（`git diff --name-only HEAD` 在 protected paths 上为空）
- [ ] 已确认当前范围未违反 "明确不含"

## 下一轮

**不自动启动**——等用户战略决策。合法的下一批候选：

1. **Re-rank equalizer direction by residual headroom**：用 `oracle_affine_bound_16qam`（Kill bound）的 residual headroom 作为信号——某 affine correction 可能帮助；但 learned corrector 必须超越 `blind_affine_compare_16qam`（receiver-visible），不是超越 C11。这是真正的 open question。
2. **Path 2 — detector lead-time maximization**（H007 已 ready）：候选 C01/C02/C06，task comparator = min_z2_ratio（AUROC=1.000 ceiling），Go metric = positive mean lead time on ≥ 2 two-class cells without AUROC regression。
3. **Rotate 到不同机制 family**：C12 coded、C13 pilot-aided，或其他 portfolio 项。

用户可选其他方向——需显式决策。本轮**没有**为任何下一批做预热实现，只完成 C11 合法性裁决本身。