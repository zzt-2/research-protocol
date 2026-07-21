# [S008] C11 legitimacy batch — Verdict B (signal disappears after legalization)

> 2026-07-21 | 阶段: legality retest / TDD | 状态: 完成（等用户战略决策下一批）

## 目标

回答外部评审问题：在统一复数滤波约定、无未来信息、同 pass/同预算、`dd_step=0` 身份门成立的前提下，合法的 CMA→DD-LMS 是否仍显著优于公平 fixed-μ CMA？连续推进到 A/B/C 最终裁决，不启动任何 ML。

## 记录

### Phase 0：流程与必读

完整读取 superpowers (systematic-debugging / TDD / verification-before-completion) + research-direction-lab + session-governance + sim-preflight + AGENTS.md + evidence-and-claims + baseline-adjudication。在隔离 worktree `direction-lab-capability-atlas`（branch `codex/direction-lab-capability-atlas`，HEAD 57384ed，clean）工作。

### Phase 1：根因调查（systematic-debugging Phase 1-3）

调用链核验：
- **anchor `cb1_cell_runner.standard_cma_godard_with_z`**（line 115）：`zx_blk = rX_blk @ wxx + rY_blk @ wxy` —— bilinear，无共轭。与项目 `common/_cma.py:CMAEqualizer2x2` 完全一致。
- **C11 `b01_candidates.c11_cma_dd_lms_cascade`**：
  - L220 stage-1 = anchor call（一次 full-stream pass）
  - L254-269 stage-1 replay loop（第二次 full-stream pass，仅为恢复 final weights）
  - L287 stage-2 `for i in range(n_valid)`（第三次 full-stream pass，从 i=0 开始用 stage-1 final weights）
  - L290-291 `zx = np.vdot(wxx, rx) + np.vdot(wxy, ry)` —— Hermitian 约定，**与 stage-1 不同**

数值复现：`vdot(w, r) ≠ r @ w`（任意复数 w 下严格不等），dd_step=0 时 max|ΔzX| ≈ 1.97。

数学推导（Wirtinger + 数值 SGD 4 rule 比较）：bilinear z=r@w 下 DD-LMS 正确更新是 `w += mu*(d-z)*conj(r)`（OLD stage-2 用此更新形式没错；错在 z 的约定）。

### Phase 2：写 H1 单一根因假设 + 版本化研究笔记

新建 `c11-legality-batch-v1/R001-c11-legality-root-cause.md`，记录 H1（4/7 阳性来自 D1 约定突变 + D2 未来信息 + D3 多 pass）+ 否决条件（合法实现下信号仍存活 → A）。

### Phase 3：冻结实验合同（运行前）

`c11-legality-batch-v1/batch-contract.v1.yaml`：DD grid 含 0；switch_point policy 物理可解释 + validation 上选 + 冻结；全新 seeds 31-35/41-50 disjoint from B01-R 11-15/21-30；fixed_μ μ=0.03 INHERITED 不重 tune；A/B/C 三选一决策规则。

### Phase 4：TDD RED

13 tests 写入 `tests/test_c11_legality.py`：8 gates + 4 OLD-impl bug 确认 + 1 contract-path。RED 验证：8 gates 全 fail（new module absent），5 negatives PASS。OLD 实现的 no-op identity 违反量化：max|ΔzX| ≈ 1.97。

### Phase 5：TDD GREEN

实现 `c11-legality-batch-v1/c11_causal.py:c11_cma_dd_lms_causal`：UNIFIED bilinear r@w；causal one-pass CMA→DD block switch；identity gate (dd_step=0)。13 tests 全 PASS（修了两个测试期望本身的合理化：mid-stream switch 下 dd_step=0 应使 CMA 权重冻结而非继续演变；stage-switch 是 block-granular）。

### Phase 6：科学运行（85s）

`run_c11_legality_batch.py --tune-and-eval`：Phase 0 自动跑 identity gates（PASS）→ Phase 1 validation tuning（plateau block = 3 所有 cell；best dd=3e-4 offset=+2）→ Phase 2 11 cells × 10 test seeds held-out eval → Phase 3 hierarchical paired bootstrap CI → Phase 4 adjudicate。

**结果**：
- macro paired Δ = **+0.01445**（C11 更差），95% CI = [−0.00022, +0.04113]
- 2/7 long cells 显著更差：snr10-fg100-long +0.025 CI [+0.00078, +0.05117]；snr15-fg1000-long +0.077 CI [+0.017, +0.139]
- 0/7 更好；5/7 short cells 实质 tie
- worst-cell +0.077；divergence 0/0；stage2 max visits/sample = 1（因果 one-pass 验证）
- best_dd_step_size = 3e-4（validation 上不是 0；DD 有微弱作用但 test 上反向）
- Verdict = **B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION**

### Phase 7：只读核验 blind vs oracle affine

`cb1_evaluator.py:106` `blind_affine_compare_16qam`（无 TX truth，receiver-visible）；`:132` `oracle_affine_bound_16qam`（用 TX truth，scoring-only Kill bound）。D010 line 352 forward rule 标错，新 contract 修正。

### Phase 8：独立 verifier subagent（不同 context）

V1-V10 全 CONFIRM。手算复数约定、手跑 dd_step=0 identity、独立重写因果扰动测试、独立重算 3 cells paired Δ（bit-identical means，CIs Monte-Carlo 一致）、定位 OLD 实现行号 L220/254/287/290、git diff 空、contract/runner 一致、verdict 逻辑正确、无禁止动作。两非阻塞观察（test 数 13 非 8；synthesis.md 当时未写——已补）。

### Phase 9：治理与产出

- `R001-c11-legality-root-cause.md`（research note）
- `batch-contract.v1.yaml`（frozen contract）
- `c11_causal.py`（GREEN impl）
- `run_c11_legality_batch.py`（runner）
- `tests/test_c11_legality.py`（13 tests）
- `artifacts/result.v1.json` + `frozen-params.v1.yaml` + `synthesis.v1.md`
- D011（amends D010 第 4 点 + forward rule 第 2 comparator）
- H008（amends H007）
- V003（10/10 CONFIRM）
- topic-index / voice.md / harvest-addendum.v5-c11-legality.yaml（H039-H043）更新

## 决策引用

- D011：C11 legality verdict B；撤回 D010 第 4 点 C11_fixed_mu 4/7 阳性 method signal；forward rule 第 2 comparator 修正（新建）
- D010：amended（fairness-survives / μ=0.03 / min_z2 ceiling 不变；C11 阳性撤回）
- D007 / D008 / D009：保留

## 范围确认

- 本轮是否在 scope boundary 内：**是**。范围 = C11 合法性裁决（A/B/C 三选一）+ 只读 forward-rule 标签核验。未做：训练 ML / 启动 B02 / 修 detector / 扩候选池 / 修改 protected history / 写论文正文 / push。
- 未触发 scope change。

## 后续

**等用户战略决策下一批方向**。三条合法路径：
1. re-rank equalizer by residual headroom over oracle_affine_bound_16qam（Kill bound），corrector 须超越 blind_affine_compare_16qam
2. path 2 detector lead-time maximization（C01/C02/C06，task comparator = min_z2_ratio）
3. rotate 到 C12/C13 或其他 portfolio 项

本轮**没有**为任何下一批做预热实现。下一对话起点 = H008。
