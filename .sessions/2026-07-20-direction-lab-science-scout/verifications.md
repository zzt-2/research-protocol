# Verification Records — Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

## V001: B01-R 独立 verifier adversarial 复核 — CONFIRM

> status: PASS
> date: 2026-07-21
> 关联：S006 / D009 / H006
> verifier: 独立子 agent（separation of concerns, P6；与本对话主线不同上下文）

### 验证问题

B01-R 纠偏批（`fairness-batch-b01r/`）是否真正修复了 B01 的 10 条审计发现，且无新的科学完整性违规？

### 验证范围（11 项 adversarial checks）

- A. No-leakage（tuning/test seeds 不重叠 + Go/Kill 仅用 held-out）
- B. Comparator 实际运行（fixed_μ CMA 真的被调，非 anchor 复制品）
- C. Detector score 与被调参数有关（非 -min(z2_ratio) 的常数）
- D. 退出判据分母 = 7（held-out cells），5/7 可达
- E. Single-class AUROC = None（不报 0.5）
- F. 真实计算 PR-AUC / recall@5%FPR / false-alarm / lead-time / Brier / ECE
- G. 4-cat 标签：AWGN-dominated 不被误标为 inner-ring
- H. 无 claim overreach（"all long cells" / "Godard-cost deep property"）
- I. Protected history 字节未改（B001-B003 / P03 / CB1 raw / canonical-state / B01 raw）；无 B004；D008/H005 仍在（superseded 不删除）
- J. Contract ↔ runner ↔ artifact 三一致（frozen params、seeds、grid）
- K. Anchor byte regression（QPSK anchor PI-SER=0）

### 发现

- **11/11 checks PASS**。
- **P0 issues: 无**。
- **P1 issues（不阻断）**：
  1. C05 调参 score=-1.0 → fallback 到 grid 首项（已 honest 报告 + 合同授权；synthesis 措辞已收紧为 "default-grid C05"）。
  2. Validation cells 在 test seeds 上也运行（intentional 用于报告覆盖；Go/Kill 仅用 held-out，无泄漏；H006 标注）。
  3. H006/D009 当时未写入（本 V001 写入时已补齐）。

### 结论

**PASS / CONFIRM / HIGH confidence**。B01-R verdict `B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY` 由 raw 数据支撑；10 条审计发现均有 code+artifact 层面的真修复；无 leakage / overreach / protected-history 损伤；anchor byte regression 保持；contract↔runner↔artifact 三一致成立。

### 对决策的影响

支撑 D009 的 VERDICT B 与 B02 ML detector 授权撤回。

---

## V002: B01-R hotfix v2 独立 verifier 复核 — CONFIRM (with P1 text fix)

> status: PASS
> date: 2026-07-21（hotfix）
> 关联：S007 / D010 / H007
> verifier: 独立子 agent（与主线不同上下文；本轮特别加强 skepticism 因 V001 漏掉了 v1 的 7 个 flaw）

### 验证问题

v1 的 7 个实现 flaw（min_z2 NaN、warmup 错位、伪 5% FPR、机械触发 VERDICT B、ambiguous 计数冲突、μ 网格边界、C11 vs anchor 而非 vs fixed_μ）是否全部真正修复？是否引入新 flaw？

### 验证范围（14 项 adversarial checks）

HF1-HF8（每条 flaw 一项）+ protected history 回归 + v1 git history 可恢复 + anchor byte regression + 新增的 verdict 非机械触发核验。

### 发现

- **13/14 checks PASS，1 PARTIAL PASS（P1）**。
- **P0 issues: 无**。
- **P1 issues:**
  1. synthesis §5.1 TOTAL 行 awgn=20 (18.2%) 与列求和 18 (16.4%) 不一致（raw 数据正确；只是 synthesis 文本错误；H030 同步错）。**已在主线修复（awgn 18 / 16.4%）**。

### 关键确认（v1 漏掉的，本轮抓到）

- **HF1 min_z2 不再全 NaN**：110/110 seeds 有实数；2 个 held-out cells two-class。
- **HF2 lead_time warmup-guard 起效**：lead_time 分布 `{−113:1, −4:3, 0:17}`，mean=−5.95；不再统一 +2（v1 artifact）。**实际 lead time 全 ≤ 0，detector 没有真正提前预警**——这点 synthesis §5.2 honest 报告。
- **HF3 5% FPR honest**：snr25-short ACTUAL_FPR=0.25（n_neg=4）；snr20-fg100-short ACTUAL_FPR=0.5（n_neg=2）；note 字段填充。
- **HF4 verdict 非机械触发**：best 方法关闭 3/7 < 5/7 → any_close=False；detector_target_ready=True（2 个 two-class cells per score）→ VERDICT A。逻辑链与 `adjudicate()` 一致。
- **HF6 μ=0.03 interior optimum**：grid 扩到 1e-1；μ=0.1 diverged；μ=0.03 是真正内部最优点（不是新边界）。
- **HF7 C11_fixed_mu vs fixed_μ**：stage1_mu=0.03（unique）；paired CI 在 4/7 held-out cells 显著（CI 排除 0）；best_score=-0.2023 是所有方法中最佳。
- **HF8 forward contract**：`forward_rules_for_corrector_batch` 存在，要求 fixed_μ + blind-affine 双 comparator。

### 结论

**PASS / CONFIRM / HIGH confidence**。v1 的 7 个 flaw 全部真正修复；verdict 从 B 改为 A 是科学得出的（非机械触发）；无新 P0 flaw。P1 awgn 计数文本错误已修。

### 对决策的影响

支撑 D010（修正 D009）：VERDICT 从 B 改为 A；fixed_μ CMA μ=0.03（非 0.01）；C11_fixed_mu 是真阳性 method signal（4/7 cells 显著）；detector target ready 但 thin（min_z2 已 AUROC=1.000 ceiling，ML 必须在 lead time 或 calibration 上赢，不能在 AUROC 上）；forward rule 要求未来 corrector batch 用 fixed_μ + blind-affine 双 comparator。

## V003: C11 legality batch 独立 verifier 复核 — CONFIRM (10/10)

> 关联：D011 / H008 / R001 | 日期: 2026-07-21
> verifier: 独立 subagent context（与实现代码分离，P6 separation）

### 验证范围

10 项独立复核（V1-V10），每项重新执行命令、读原始数据、重算数字，不信任实现方摘要。

### 结果

| # | 项 | 结果 | 关键证据 |
|---|---|---|---|
| V1 | 测试套件 fresh 重跑 | PASS | 13 tests passed, 0 failed（8 gates + 4 OLD-impl bug 确认 + 1 contract-path） |
| V2 | 手算复数约定 | PASS | r@w = (-6.27+4.33j)，vdot(w,r) = (-9.43-0.71j)，**不等** |
| V3 | dd_step=0 位等价手测 | PASS | max\|ΔzX\| = 0.0；np.array_equal = True |
| V4 | 因果前缀不变动独立重实现 | PASS | safe_prefix=1494 处 zX[:safe_prefix] bit-identical |
| V5 | 3 cells 配对 Δ 独立重算 | PASS | 与 runner 数字 bit-identical（CIs 在 Monte-Carlo 噪声内一致）；macro +0.014453125 完全相同 |
| V6 | OLD 实现三 pass 结构定位 | PASS | b01_candidates.py L220 / L254 / L287 / L290 四个 marker 全在 |
| V7 | v1 路径未覆盖 | PASS | git diff --name-only HEAD 空；B01-R mtime 在本 session 之前 |
| V8 | contract/runner 一致性 | PASS | DD_STEP_GRID 与 contract 完全一致；所有 outputs 在 c11-legality-batch-v1/ 下 |
| V9 | verdict 逻辑应用 | PASS | macro_mean=+0.014 不满足 <0；CI 上限 +0.041 不满足 <0；worst-cell +0.077 不满足 ≤0 → Verdict B 唯一可能 |
| V10 | 无禁止动作 | PASS | 无 fairness-batch-b01* 改动；无 ML/torch/sklearn import |

### 独立重算的数字（核心）

- macro paired Δ = **+0.014453125**（runner 报告值完全相同）
- macro CI 下限 = **−0.000223**（runner 报告值完全相同）；上限 +0.040851（runner +0.041129，Monte-Carlo 噪声 3e-4 内）
- snr10-fg100-long Δ mean = **+0.025000**（完全相同），CI = [+0.000781, +0.051562]（runner 上限 +0.051172，差 4e-4）
- snr15-fg1000-long Δ mean = **+0.076563**（完全相同），CI = [+0.016406, +0.140234]（runner 上限 +0.139063，差 1e-3）
- 所有显著性结论（2 cells CI 下限 > 0；0 cells CI 上限 < 0）与 runner 一致

### 次级观察（非阻塞）

1. 实现方摘要写 "8 gate tests"，实际测试套件是 **13 tests**（8 gates + 4 negative-control + 1 contract-path）。所有 PASS，不影响结论。
2. Contract `outputs.synthesis` 声明的路径 `c11-legality-batch-v1/artifacts/synthesis.v1.md` 在 verifier 运行时尚未存在；contract-path 测试只校验声明的字符串不校验文件存在，所以测试 PASS。（注：synthesis.v1.md 在 verifier 报告后已补写。）

### 结论

**CONFIRM** 实现方 "Verdict B、所有门 PASS、无禁止动作" 的结论。所有数字独立重算一致；OLD 实现的 3 个合法性缺陷（D1/D2/D3）在 b01_candidates.py L220/254/287/290 独立确认。

## V004: S009 三批独立 verifier 复核 — CONFIRM (8/8 PASS, 0 P0, 2 P1 fixed)

> 关联：D012 / D013 / D014 / H009 | 日期: 2026-07-21
> verifier: 独立 subagent context（P6 separation，与三批实现代码不同上下文）

### 验证问题

S009 三批（c11-legality-batch-v1 amendment / corrector-residual-headroom-v1 / c04-c09-shared-corrector-v1）的 verdict 和数字是否忠实于 raw artifact + source？是否有 leakage / protected-history 损伤 / overreach / synthesis 不忠实？

### 验证范围（8 项 adversarial checks）

1. Batch 1 重算 3 个代表性 cells (16qam-snr20-fg100-short / snr10-fg100-long / snr15-fg1000-long, seed 71) PI-SER
2. Batch 1 blind/oracle 信息边界对抗测试（perturbing TX truth）
3. Batch 1 + Batch 2 no-leakage seed check
4. Batch 1 + Batch 2 source-closure SHA-256 比对
5. Batch 2 ceiling check (candidate macro PI-SER ≈ random 0.9375)
6. protected history check (git diff 不触及 B001-B003 / P03 / canonical-state / B01/B01-R raw / c11 result.v1.json)
7. Batch 3 fresh Windows pytest (c11-legality-batch-v1 tests/)
8. Batch 1 + Batch 2 synthesis faithfulness (3 numeric claims each)

### 结果

| # | 项 | 结果 | 关键证据 |
|---|---|---|---|
| 1 | 3 cells PI-SER 重算 | PASS | 与 result.v1.json per_seed[seed=71] bit-identical (Δ ≤ 5e-7) |
| 2 | blind/oracle 边界对抗 | PASS | perturbing TX truth × (0.7+0.7j): blind max\|Δ\|=0.000e+00 (bit-identical); oracle max\|Δ\|=1.279 (changed) |
| 3 | no-leakage seed check | PASS | Batch 1 val[61-65] ∩ test[71-80] = ∅; ∩ prior[11-50] = ∅. Batch 2 train[81-90] ∩ val[91-95] ∩ test[71-80] = ∅ pairwise; train/val ∩ prior[11-65] = ∅ |
| 4 | source-closure SHA-256 | PASS | 14 files (7 per batch), zero mismatches |
| 5 | Batch 2 ceiling check | PASS | C04_mlp macro PI-SER_candidate = 0.927846; C09_gru = 0.927958; both ~0.01 below 16QAM random ceiling 0.9375 |
| 6 | protected history check | PASS | 19 changed/new paths, NONE in protected set (B001-B003 / P03 / canonical-state / B01 raw / B01-R raw / c11 result.v1.json 全未改) |
| 7 | Batch 3 fresh Windows pytest | PASS | 19/19 PASS in 0.58s (Python 3.11.9, pytest 9.1.1, win32) — 13 原 + 6 新 portability/provenance |
| 8 | synthesis faithfulness | PASS | Batch 1: H_total +0.0617, G_blind -0.0084, H_residual +0.0664 全 match raw. Batch 2: C04/C09 macro Δ(cand-blind) +0.624 / worst +0.783 / +0.782 全 match raw |

### 发现

- **P0 issues: 无**。无 leakage / hash mismatch / protected-path violation / synthesis 不忠实。
- **P1 issues (2)**:
  1. Batch 1 synthesis §3 与 §0 用了两种 macro 聚合约定（hierarchical paired bootstrap macro_mean vs 简单 aggregate mean with max-floor），数字差 ~0.006（H_total: +0.0557 vs +0.0617）。**已修复**（§3 加 footnote 说明两种约定 + verdict 对选择稳健）。
  2. Batch 2 test 名拼写错误：`test_apply_affile_is_A_times_z_plus_b` → `test_apply_affine_is_A_times_z_plus_b`。**已修复**（cosmetic only；测试逻辑不变，12/12 仍 PASS）。

### 结论

**CONFIRM / HIGH confidence**。三批 verdict 和数字全部忠实于 raw artifact + source；无 leakage / overreach / protected-history 损伤；contract↔runner↔artifact 三一致；所有信息边界测试 PASS。

### 对决策的影响

支撑 D012（C11 scope-narrow amended）、D013（adjudication VERDICT A）、D014（C04/C09 CANDIDATE_BLOWS_UP）三决策。所有数字独立重算一致；三批的 source closure hash 全 match；protected history 全未改；无 P0；2 P1 已修复。

> **Amendment（V005）**：V004 只保留 artifact fidelity、数值重算、seed/hash 和历史保护层面的 PASS。目标函数语义与机制推断由 V005 判定 FAIL。

## V005: S009 外部科学语义复核——FAIL

> 日期：2026-07-21
> 关联：S010 / D013 / D014 / D015 / D016 / V004

### 验证范围

复核 C04/C09 训练目标是否与合同语义一致、坏结果是否能排除更简单的实现解释、D013 的 headroom 分解是否足以授权 learned corrector，以及 V004 是否覆盖科学机制解释。

### 证据

- 目标函数存在输入无关常数解：`A=0`、每个实坐标约 `±0.6075`；一维 loss 约 `0.32710044`，四维约 `1.30840175`，与 artifact `1.3084` plateau 一致。
- runner 实际每个函数类只训练一个硬编码配置；合同/synthesis 所称 8-combo sweep 没有 raw artifact。
- C04/C09 raw PI-SER 约 `0.928`、相对 blind 约 `+0.624`、worst degradation 约 `+0.78` 可复现，但只能支持实现/目标常数塌缩。
- D013 中 signed `fixed-oracle` macro 约 `0.05575`，而 clipped `H_total=0.06172` 是不同聚合；`H_residual=blind-oracle` 包含 blind 自身负贡献。
- V004 的重算、hash、seed、source closure 与 protected-history 检查没有覆盖“训练目标是否代表声称任务”的最小反例。

### 结论

**FAIL**。

- artifact fidelity：PASS（沿用 V004）。
- scientific semantic validity：FAIL。
- D014 exact-mechanism negative：撤回。
- D013 learned-corrector target ready：撤回，降为 truth-assisted local diagnostic。
- C04/C09 candidate science：`UNRESOLVED`。

### 后续验证门

未来 corrector 在进入全量 cells × seeds 前，至少通过：恒等/no-harm、常数输出、输出方差/星座占用、单样本过拟合、简单 comparator 复现、目标函数手算最小反例。实现与科学语义审查继续分离。

---

## V006: e15ae60 七审计项独立核验 + C16 原始数据主线复算

> date: 2026-07-22
> 关联：S011 / D017
> verifier: 独立 explore 子 agent（P6 separation）× 3 + 主线直接读 result.v1.json 复算

### 验证项

- [x] 审计1（C04 O1 目标退化解）：子 agent 读 `c04-c09-o1-corrected-scout/src/run_o1_corrected_scout.py:275-290` + `baseline-atlas/cb1_evaluator.py:106-129` + `:666-688` → O1 训练 loss = `MSE(A·z+b, hard(A·z+b))` self-referential moving target，A=0/b=星座点 = 零损失全局最优；constant-smoke 测的是 fixed-target blind-affine。**CONFIRM**。
- [x] 审计2（C12 oracle）：子 agent 读 `c12.../src/soft_demap.py:315-346`（oracle 仅估全局 σ² line 344 再跑相同 maxlog line 346）+ `gmi.py:50-67`（histogram-MI equi-width bins，公共 LLR 缩放不改变 bin 分配）+ synthesis `:49-51` 自 concession → **CONFIRM**，"零 GMI headroom"非真上界。
- [x] 审计3（C14 cosine）：子 agent 读 `c14.../src/cma_custom_init.py:254-296`（oracle Wiener truth-conditioned，需 sX_calib/sY_calib）+ `test_init_identity.py:168-173`（唯一 truth-using）+ grep "cosine" in src = 0 hit（0.9995 仅 synthesis narrative `:34,151,238`）+ far-orthogonal probe 仅 narrative `:41-44,190,246` 未在 src → **CONFIRM**。
- [x] 审计4（C15 μ 共享）：子 agent 读 `c15.../src/run_cost_scout.py:119-132`（godard/ring_aware/rccma 共 μ=0.03 from FROZEN_AXES line 62）+ `cma_cost_variants.py:201-204`（raw LMS `w+=mu*grad`，无归一化）+ synthesis `:98-114` 自报 19× 梯度比 → **CONFIRM**。
- [x] 审计5（C16 非法专家）：子 agent 读 `c16.../src/hos_equalizer.py:24-37`（2×2 whitening）+ `:66-68`（"real Givens for simplicity"）+ `:96-130`（real θ grid + 单标量 phase）+ `:138`（cost_contains_modulus_term=False）→ 无 n_tap/FIR/sliding-window；vs `_cma.py:57-190`（11-tap 4-filter butterfly block-64）→ **CONFIRM**，task-mismatched 非对齐专家。
- [x] 审计6（seeds 71-80）：子 agent grep 全 campaign → 71-80 在 c04/c09/c14/c15/c16/corrector 6 批 full + c12 子集 71-76 + probes 71-73 重复使用；contract 自承认 "intentional reuse"（c04-c09-shared `batch-contract.v1.yaml:137`、c14 `:141`、c15 `:172`）；仅 c11(41-50)/b01r(21-30)/atlas(11-20) disjoint → **CONFIRM**，失去 held-out 资格。
- [x] 审计7（H060 ceiling）：主线核对 H060 evidence 链 = C04/C09(confounded) + C12(scale-artifact) + C14(scope-narrow) + C15(confounded) + C16(task-mismatch) → 5 轴中 3 轴科学语义失效 → **CONFIRM**，H060 须排除 C12/C16 后降级。

- [x] 主线复算 C16 result.v1.json：直接读 `c16-nonmodulus-jade-scout/artifacts/result.v1.json`（110 realizations = 11 cells × 10 seeds，metadata.test_seeds=[71..80]）。复算：CMA macro=0.2507、HOS macro=0.4664（与 synthesis/线索一致）；CMA>0.3 子集=37、HOS 更好=26/37（与线索一致）；per-realization oracle selector min(CMA,HOS) macro=0.1928、绝对余量 0.0579（线索 ~0.2073/0.0434，同量级）。**数值可复现**。

### 证据

- 子 agent 3 份报告（seeds 重用 / C14+C16 身份 / C04+C12+C15+inventory），含 file:line 指针，见 S011 §1。
- 主线复算脚本输出（PY=~/.venvs/torch/Scripts/python.exe，11 cells flatten 110 rows）：见 S011 §2。

### 结论

**PASS（审计项全部 CONFIRM）+ PARTIAL（数值可复现但科学语义失效）**。

- reproduce-vs-validity 拆分成立：e15ae60 数值可复现，但 C12(scale)/C15(step)/C16(task)/seeds(71-80)/C04(target)/C14(scope) 科学语义均失效或不足。
- 混合路由诊断互补"数值真实但建立于非法专家 + 污染 seeds + 事后 oracle"，仅 DIAGNOSTIC。

### 后续（FAIL/PARTIAL 时）

- H060 降级为 LOCAL_SLICE 弱断言（D017）。
- 混合路由研究必须用合法 FIR 对齐 fallback（MMA 公平 μ 重测 + standalone DD-LMS 新建）+ fresh disjoint test seeds 重测 oracle 互补性。

---

## V007: Macro A 混合路由独立 verifier adversarial 复核 — VERDICT C HOLDS

> date: 2026-07-22
> 关联：S011 / D018
> verifier: 独立 general-purpose 子 agent（P6 separation，与实现 runner 不同上下文，主动攻击非确认）

### 验证问题

Macro A "合法 FIR 专家 oracle 互补性"测试裁决 VERDICT C（headroom 0.0037 << 阈值 0.03）是否在 adversarial 攻击下成立？测试是否被操纵以产出低 headroom（因 verdict C 恰好符合"不继承 5 轴叙述"的意图）？

### 验证范围（8 项 adversarial checks）

1. seed 新鲜度（121-130 / 101-105 与所有 prior 批次 disjoint）
2. 无信息泄漏（MMA/DD-LMS 只收 rX/rY；oracle 才用 TX truth）
3. 专家身份（MMA 真实 YWD per-axis modulus + DD-LMS 真 cold-start；5/5 身份门）
4a. CMA anchor 公平（μ=0.03 是 B01-R validation-optimal interior optimum）
4b. fallback μ-tuning 公平（grid search on validation seeds）
4c. paired comparison（同 shared realization）
5. headline 独立重算
6. 统计稳健性（headroom 是否在 0 的噪声内）
7. 退化解/collapse 检查（CMA 是否被人为做强）
8. scope/overreach（verdict C 是否只关本 contract）

### 证据

独立 verifier 从零读 result.v1.json 重算：
- macro PI-SER: cma=0.39719 / mma=0.50305 / ddlms=0.43189 / oracle=0.21964（与 stored bit-identical）
- selector all3 = 0.39350；**headroom all3 = 0.003693**（与 stored bit-identical）
- complementarity: mma better 6/110 worse 64, ddlms better 23 worse 39（match）
- per-realization headroom: mean 0.00369, SE 0.00067, median 0.00000（76/110 exact tie），仅 34/110 有任何正 headroom
- headroom 是阈值的 12%（~22 SE 低于阈值）

### 结果

| # | 项 | 结果 | 关键证据 |
|---|---|---|---|
| 1 | seed 新鲜度 | PASS | grep 121-130/101-105 在 scout/+probes/ 无命中；与 11-20/21-30/41-50/71-80 全 disjoint |
| 2 | 无信息泄漏 | PASS | run_macro_a_oracle.py:107-135 MMA/DD-LMS 只收 rX/rY；oracle_unmix:88-92 才用 sX/sY（allowed Kill bound） |
| 3 | 专家身份 | PASS | MMA per-axis modulus R_R²=R_I²=0.82 验证（mma_comparator.py:84-181）；DD-LMS 真 cold-start（dd_lms_equalizer.py:37-122）；5/5 身份门 PASS |
| 4a | CMA μ 公平 | PASS | μ=0.03 是 B01-R validation-optimal interior optimum；比 atlas default 0.001 更强（macro 0.397 vs 0.442）—— 偏向 C（低 headroom），不偏向反方向 |
| 4b | fallback μ 公平 | PARTIAL | DD-LMS μ=0.1 是 grid 边界但 5-seed 验证为真 interior min（0.181→0.168→0.178）；MMA 单 seed 选 0.003，真 5-seed 最优 0.001，headroom 差 0.00003 |
| 4c | paired | PASS | make_realization 每 (cell,seed) 调一次，跨专家共享 |
| 5 | headline 重算 | PASS | 全部 bit-identical |
| 6 | 统计稳健 | PASS | median 0, 76/110 exact tie, 22 SE 低于阈值；complementarity fractions 不接近 frequent wins |
| 7 | collapse/degenerate | PASS | 61/110 CMA>0.3，CMA 非均匀好；fallback 在同 61 个 collapse realizations 也失败（correlated failure），非 CMA-looks-good 伪象 |
| 8 | scope | PASS | contract:124-127 显式"close THIS specific hybrid contract, NOT the whole family" |

### 结论

**PASS / HIGH confidence — VERDICT C HOLDS under adversarial attack**。

headline 数字独立重算 bit-identical。verifier 专门测了"convenient conclusion"怀疑论：CMA 给了最强 μ（测试偏向 verdict C），但 headroom 仍 8× 低于阈值——结论稳健。机制真实：MMA/DD-LMS/CMA 共享 correlated failure modes（同 61/110 collapse realizations）。scope 正确限定本 contract。

### 发现的瑕疵（非 verdict-changing）

1. **DD-LMS weight-norm bug**（dd_lms_equalizer.py:105-107 旧版）：算 `sqrt(sum|w|)²`（L1-of-magnitudes）非 `sqrt(sum|w|²)`（L2）。**已在主线修复**（改 L2）。impact nil（test 数据 0 divergence）。
2. **tune_mu 只用 seed 101** 非 5 个 validation seeds：contract 承诺 [101-105]（复数），实现欠交付。impact nil（proper 5-seed 改 headroom 0.00003）。已记录为方法论 caveat。

### 后续

- D018 verdict C 登记。Macro B 不运行（无 headroom 可转化）。
- 未来若重启专家路由，必须用机械更多样专家池（model-based + blind 或 pilot-aided + blind），非近共模 FIR 盲均衡。

---

## V008: H012 恢复链与 current views 独立终验

> date: 2026-07-22
> 关联：D019 / H012

### 验证项

- [x] YAML 合法性：独立 verifier 对 `state/current.yaml`、`portfolio/current.yaml`、`harvest/current.yaml` 执行 safe_load → 三者均为 dict，PASS。
- [x] 数字与切分：从 hybrid result/contract 核验 headroom `0.003693`、阈值 `0.03`、test seeds `121–130` → 与 H012/current views 一致，PASS。
- [x] 候选状态：核验 C04/C09/C12/C14/C15 不再作为 family closure → current portfolio 分别为 implementation/metric/step confound 或 partial diagnostic，PASS。
- [x] 恢复入口：核验 STATUS、state、portfolio、harvest、topic-index 均直接指向 D019/H012 → PASS。
- [x] 历史与当前分离：独立 verifier 首轮发现 harvest 旧 closure 叙述虽在 historical 区但未显式失效，结论 PARTIAL；修复后旧条目均标 `invalidated_by_D017` / `amended_scope_narrowed_by_D017`，`current_view` 成为唯一有效投影 → 复核 PASS。

### 证据

```text
current.yaml PASS
current.yaml PASS
current.yaml PASS
_registry.yaml PASS
consistency PASS
independent verifier round 1: PARTIAL
independent verifier round 2: PASS
```

独立 verifier 最终摘要：

```text
PASS。三项修复均已复核通过，YAML 解析正常，未修改文件。
```

### 结论

PASS

---

## V009: 信息来源组合级 Probe 独立 verifier adversarial 复核 — CONFIRM

> date: 2026-07-22
> 关联：S012 / D020
> verifier: 独立 general-purpose 子 agent（P6 separation，与实现代码不同上下文，主动攻击非确认）

### 验证问题

F1-A/F3-A/F4-A 三个 headroom/observability Probe 的 verdict 和数字是否忠实于 raw artifact + source？是否有信息泄漏 / oracle 偷用 eval truth / comparator 不公平 / scale-artifact 未修正 / overreach / blocked 误写成 negative？

### 验证范围（9 项 adversarial checks）

1. 信息源真实存在（channel 暴露 h/θ，Jones 可解析重建）
2. receiver-visible 路径不偷用 eval truth（receiver_visible_features 只读 cma trace）
3. comparator 任务匹配且公平（μ=0.03 是 B01-R interior optimum；paired realization）
4. 物理门限有 provenance（0.03 = MDE scaled，非 comms 阈值）
5. 无退化解/常数解膨胀 headroom（独立重算 3 cells bit-identical）
6. scope/overreach（claim_ceiling 全 LOCAL_SLICE；"authorize considering"非"run"）
7. blocked vs negative 分离（F4-A BOUNDARY 非 Kill；F4-B INFRASTRUCTURE_BLOCKED）
8. 公平性/oracle 不膨胀（oracle scoring-only Kill bound，非 Go criterion）
9. scale-artifact 正确处理（histogram invariant / analytic sensitive / verdict 用 analytic / +0.0089 重算）

### 结果

| # | 项 | 结果 | 关键证据 |
|---|---|---|---|
| 1 | 信息源存在 | PASS | `_dual_pol_channel.py:123-132` SOP = sqrt(h)·[[cos,sin],[-sin,cos]]；reconstruct_jones 匹配 |
| 2 | 无 eval-truth 泄漏 | PASS | receiver_visible_features 代码（去 docstring/comment）无 sX/sY/h/theta；unit test 强制 |
| 3 | 公平 comparator | PASS | μ=0.03 是 decisions.md:390 interior optimum；每 (cell,seed) 一次 make_realization |
| 4 | 门限 provenance | PASS | contract:122-123 "MDE=0.005 scaled"；prohibition no_mde_as_communication_usable |
| 5 | 无退化解膨胀 | PASS | 3 cells (snr20-short/snr05-short/snr20-long) 独立重算 cma/oracle/headroom Δ<1e-9；macro 0.132884 复现 |
| 6 | scope/overreach | PASS | 全 claim_ceiling=*_LOCAL_SLICE；"authorize considering"=Probe-PASS 语义 |
| 7 | blocked vs Kill | PASS | F4-A=BOUNDARY 非 Kill；F4-B=INFRASTRUCTURE_BLOCKED；contract:133-135 禁止 blocked 写 Kill |
| 8 | 公平性 | PASS | probe_shared.py:17-18,127 oracle=scoring-only Kill bound；oracle_only_as:[Kill,headroom_bound] |
| 9 | scale-artifact | PARTIAL | (a)(b)(c) PASS；(d) **PARTIAL**：+0.0089 smoothing-fragile（sm=2:+0.033/sm=8:+0.009/sm=32:+0.002，CI 跨0）；非 verdict-changing（F4-A 已是保守 BOUNDARY） |

### 独立重算数字（核心）

- F1-A macro headroom = **0.132884**（stored bit-identical）；3 cells Δ<1e-9
- F1-A max receiver-visible |r| = **0.651**
- F3-A MI increment = **+0.060 bits**；R² increment = **+0.036**
- F4-A analytic GMI headroom = **+0.008907**（stored bit-identical）；histogram = −0.021（scale-invariant 复现）
- F4-A smoothing 敏感性：sm=2/8/32 macro_X_only = +0.0331/+0.0102/+0.0032（独立复现）

### 发现的瑕疵（非 verdict-changing）

1. **P1（methodological caveat）**：F4-A +0.0089 GMI headroom 对 smoothing 窗口超参数敏感；sm=32 时 CI 跨 0。集中在低 SNR cells。**已写入 F4-A-result.v1.json 的 smoothing_sensitivity_caveat 字段**。不影响 verdict（F4-A 已是保守 BOUNDARY/do-not-build）。
2. **P1（cosmetic）**：contract 引用 `domain-comms.md:164-171` 但该文件行内容与引用字面不完全匹配（实质内容在别处）。不影响。

### 结论

**PASS / HIGH confidence — CONFIRM**。所有 headline 数字独立重算 bit-identical；无 truth 泄漏 / 退化解 / overreach / blocked-as-Kill / oracle-as-Go；scale-artifact 正确诊断（histogram invariant / analytic sensitive / verdict 用 analytic）。1 个 P1（F4-A smoothing 敏感性）已文档化，非 verdict-changing。

### 对决策的影响

支撑 D020：F1-A/F3-A PASS 授权考虑 F1-B Scout；F4-A BOUNDARY 不建 F4-B；统一报告投资选择交用户。

---

## V010: F1-A/F3-A/F4-A integrity 独立核验（D021 科学纠偏） — PARTIAL（数值可复现，科学归因/因果性/hash 闭包有缺口）

> date: 2026-07-22
> 关联：S012 / D020 / D021
> verifier: 独立 integrity 子 agent（P6 separation，与 D021 的科学 critic 分工：本 V010 只审 integrity 层——hash/seed/paired/raw-to-aggregate/tests；科学语义归因见 D021 + critic 报告）

### 验证问题

F1-A/F3-A/F4-A artifact 的数值是否可独立重算？source-closure hash 是否与当前源码一致？seed 纪律是否成立？paired realization 是否真共享？raw rows 是否可重算 aggregate？现有 identity test 是否覆盖 D021 列出的缺口？

### 验证项（integrity 层）

- [x] 项1：headline 数字独立重算 → **PASS**。F1-A macro headroom `0.1328835227272727`（stored bit-identical）；fixed-CMA PI-SER `0.331640625`；genie PI-SER `0.19875710227272725`；paired gap `0.1328835227272727`；bootstrap CI `[0.08455255681818183, 0.18269264914772712]`；diagnostic max |r| `0.6510455630919102`。逐项与 `F1-A-result.v1.json` 比对一致（命令：重算 cell_means → macro_aggregate → bootstrap_ci）。
- [x] 项2：seed 纪律 → **PASS**。`probe_shared.assert_seed_discipline()` 校验 validation[131-135] ∩ test[141-150] = ∅；test ∩ prior batches[11-20/21-30/31-35/41-50/61-65/71-80/81-95/101-105/121-130] = ∅。
- [x] 项3：paired realization → **PASS**。`make_realization` 每 (cell,seed) 调用一次，CMA anchor 与 oracle 共用同一 `rX,rY,h,theta`。
- [ ] 项4：source-closure hash 闭包 → **FAIL**。`F1-A-result.v1.json` 与 `F3-A-result.v1.json` 存 `src/run_f4a_soft_gmi.py` = `adf8559556cf...`，当前文件 = `b91731e9c26f...`（D021 缺口 #8）。F1/F3 artifact 录入后 F4 源码被改，闭包已破。F4-A artifact 自身 4 个 hash 全 MATCH（自洽）。
- [ ] 项5：raw rows 可重算 aggregate → **FAIL**。`F1-A-result.v1.json` 无 `rows/per_realization/raw` 字段；仅存 cell_means（已是聚合后）。无法从 artifact 逐 per-seed 重算 macro（只能重算到 cell_means 层）。D021 缺口 #7。
- [ ] 项6：fixed-label metric 双报 → **FAIL**。F1-A artifact 仅存 `pi_ser`，无 `fixed_label_ser`（`probe_shared.metrics()` 返回但 payload 未写入）。D021 缺口 #6。
- [ ] 项7：blind_affine_compare_16qam 实际调用 → **FAIL**。grep `src/{run_f1a_model_prior,probe_shared,run_f3a_history,run_f4a_soft_gmi}.py` 无 `blind_affine` 调用；contract fairness.task_comparator 声明但 Probe 未运行。D021 缺口 #5。
- [ ] 项8：identity test 覆盖度 → **PARTIAL**。现有 `test_probe_identity.py` 10 项覆盖 seed/constant-output/no-eval-truth-leak-into-visible-path/paired/causal-prefix（F3）/scale-invariance（F4）。**未覆盖**：future-leakage invariant（F1 trace 含未来 block）、target-alignment（observability target=headroom 非 state）、comparator-invoked、dual-metric-written、raw-to-aggregate、source-hash-闭包。D021 缺口 #9（V009 漏审科学层）。
- [x] 项9：protected STATUS diff 矛盾 → **CONFIRMED 矛盾**。`git diff bf620b3~1 bf620b3 -- STATUS.v1.md` = +9/-4 行（含 "F1-B 第一个正面候选" 叙述），与 S012/D020/H013 "protected STATUS unchanged" 宣称冲突。D021 缺口 #10。本轮不改 STATUS（提示词禁），仅记录。
- [x] 项10：canonical/project.v1 ownership 冲突 → **CONFIRMED 未解**。`canonical-state.yaml` status=BLOCKED（reasons: master-state/latest-DV drift + Step3.5 未独立闭合）vs `state/current.yaml` SCIENCE_SCOUT 投影（last_recovery_entry=H013）并存。D021 缺口 #11。本轮不静默修改，仅报告。

### 证据

```
项1 重算（F1-A, 3 cells 抽查 snr20-nominal-short/snr05-nominal-short/snr20-nominal-long）：
  cma_pi_ser  cell_means = {0.306640625, 0.651953125, 0.13046875}  == stored
  oracle_pi_ser cell_means = {0.098046875, 0.640625, 0.03984375}  == stored
  headroom cell_means    = {0.20859375, 0.011328125, 0.090625}     == stored
  macro(headroom) = 0.1328835227272727  == stored 0.1328835227272727
  max |r|(z_amp_mean) = 0.6510455630919102  == stored

项4 hash 比对（python3 hashlib.sha256）：
  F1-A artifact:
    src/probe_shared.py         MATCH  7d9d87445650 == cur 7d9d87445650
    src/run_f1a_model_prior.py  MATCH  bf0c65b7feff == cur bf0c65b7feff
    src/run_f3a_history.py      MATCH  7198aac001f6 == cur 7198aac001f6
    src/run_f4a_soft_gmi.py     DIFFER stored adf8559556cf != cur b91731e9c26f
  F4-A artifact: 4/4 MATCH（自洽）
```

### 结论

**PARTIAL**。数值层（项1/2/3）PASS——headline 数字 bit-identical 可复现，seed 纪律与 paired realization 成立。但 integrity 闭包有 4 项 FAIL（项4 hash 闭包破、项5 无 raw rows、项6 无 fixed-label、项7 comparator 未调用）+ 1 项 PARTIAL（项8 identity test 覆盖不足）+ 2 项矛盾确认（项9 STATUS diff、项10 ownership）。

V009 的 CONFIRM 仅覆盖 artifact fidelity，未覆盖科学归因/因果性/comparator 公平性——这些由 D021 科学 critic 报告承担。V009 不删不改，本 V010 补 integrity 层缺口。

### 后续（PARTIAL）

1. F1-A0 修复 Probe 必须修齐项4-8：重录所有 artifact 的 4 个 source hash（含 F4 当前 hash）、保存 per-seed/per-cell raw rows、写 fixed-label metric、实际运行 blind_affine_compare_16qam、扩 identity test 至 future-leakage/target-alignment/comparator-invoked/dual-metric/raw-to-aggregate/source-hash-闭包。
2. STATUS.v1.md 的 "protected unchanged vs actual diff" 矛盾与 canonical/project.v1 ownership 冲突交主控裁决（本轮不改）。

---

## V011: F1-A0 修复 Probe 科学 critic 独立复核 — FAIL 结论 HOLDS（但证据基础被重写；2 子结论 OVERTURNED）

> date: 2026-07-22
> 关联：S013 / D021 / V010（与 V010 分工：V010 审 integrity 层，本 V011 审科学语义层）
> verifier: 独立 scientific-critic 子 agent（P6 separation，主动攻击非确认）+ 主线独立复核 critic 的 2 个最强攻击

### 验证问题

F1-A0 修复 Probe 的结论（"F1-A0 FAIL；0.133 headroom 是 CMA-anchor-bad 归因；不建 tracker；转 F2"）是否在信息来源归因、因果性、comparator 公平性、统计独立性和结论强度上站得住？

### 验证范围（6 攻击轴）

1. 信息来源归因（E1 真无 TX-truth 泄漏？E1≈E3 是否真实？TX-truth "无贡献" 是否普适？）
2. 因果性（prefix_features 真只读 <cut？ridge probe 只用 validation？）
3. comparator 公平性（blind_affine 是否被 CMA 输出污染？）
4. 统计独立性/强度（n=11 cells grouped CI 是否够？g0 的 8/13 是否显著？）
5. 结论强度/overclaim（"转 F2"是否真由 FAIL 推出？"CMA 发散"措辞是否准确？）
6. 隐含泄漏/confound（E2 pilot 反而更差是否实现 bug？）

### 结果（5 个 attack landed，3 个 survived；主线复核 critic 2 最强攻击全 CONFIRM）

| # | 攻击 | 落地? | 主线复核 |
|---|------|------|---------|
| L1 | **blind_affine 被 CMA 输出污染 → g1/g2 comparator 失效（最强）** | LANDED | 主线独立复核 CONFIRM：raw-stream blind_affine pi_ser ≈ 0.0000 vs CMA-fed ≈ 0.83（snr15/20-nominal-short seed 161）。causal_plugin "赢" 11/11 cells 是因为对手被废 |
| L2 | **E2 budgeted pilot 实现破损：pilot 在接收端合成、信道从未发送** | LANDED | causal_plugin 读 raw rX/rY，blind_affine 读 CMA z-stream，信息路径不对等；E2=0.76 是噪声放大非 pilot 性能 |
| L3 | **g6（PI vs fixed-label 不反转）空洞：两 metric bit-identical** | LANDED | 主线复核 CONFIRM：110 rows × 7 methods，`pi_ser == fixed_label_ser` 至 1e-12。g6 检查 `x==x` |
| L4 | **"CMA 发散"措辞错误；实际是 μ 调参不当** | LANDED | 主线独立复核 CONFIRM：μ-sweep snr15-short seeds161-163，μ=0.01→0.083 vs μ=0.03→0.369；0/110 rows diverged。blind CMA 仅靠 retune μ 关闭 ~60% gap-to-E1 |
| L5 | **g1 非真 persistence baseline，是 blind_affine 代理（且被 L1 双重污染）** | LANDED | `_persistence_baseline_theta_error` 返回 None |
| N1 | 因果性/未来泄漏 | SURVIVED | 主线复核：future-perturbation invariant 重跑 bit-identical；prefix_features 只读 rX[:cut]/rY[:cut] |
| N2 | E1 TX-truth 泄漏 | SURVIVED | e1_jones_inverse grep 无 sX_calib/sY_calib（仅用 R2_16QAM=1.32 公共星座功率=modulation-format knowledge 非 TX truth） |
| N3 | g0（prediction 无增量）FAIL 真实 | SURVIVED | 主线复核 CONFIRM：8 help/13 hurt/89 tie；binomial p≈0.38（n=21）= 不可区分于 coin flip，比 Probe 声称的还 null |

### 主导 confound（C1，物理非归因）

SOP 旋转在 256-symbol eval window 上仅 **0.06°**（`theta = sop_rate·arange(N)`，sop_rate=4e-6 → 1.02e-3 rad）。de-rotation 近 identity → E1(真θ) ≈ causal_plugin(预测θ) ≈ nopred(θ≡0) 全塌缩到 0.168（差 <0.0005）。**任何 tracker 在此 cell atlas 上都长一样**——F1-A0 是 F1 家族核心问题的弱测试，by cell-atlas construction，非 estimator 选择。

### 独立重算数字（主线 + critic）

- 主线复核 raw_rows 重算：cma_pi_ser_macro = 0.3612571023（diff 0.00e-00 vs stored）；7 method macros 全 match
- 主线复核 L1：raw blind_affine ≈ 0.0000 vs CMA-fed ≈ 0.83（3 cells × seed 161）
- 主线复核 L4：μ=0.01 macro(snr15-short, 3 seeds) = 0.0833 vs μ=0.03 = 0.3685
- critic 复算 g0：8/13/89 split，binomial p≈0.38
- critic 复算 E1 vs E3：E1=0.168, E3=0.179（TX-truth 实际更差 +0.011 macro）；E1<E3 in 38 rows vs E1>E3 in 19
- critic 复算 0/110 CMA diverged（max cma_pi_ser=0.930 < RANDOM_CEILING 0.9375）

### 结论

**HOLDS — FAIL 正确，但证据基础被重写**。headline "0.133 是 fake headroom / 不建 tracker" 存活，但**主导原因是物理（rotation ~0.06° 使预测任务近空）+ CMA μ 调参不当（D005/D007 已 flag 的债）**，**非** Probe 声称的 "CSI/TX-truth/model-prior 无贡献"。两个 Probe 子结论 **OVERTURNED**：(a) "TX-truth 无贡献" 是 near-zero-rotation 的 artifact（LS 无 residual 可消，只能加过拟合噪声）；(b) "budgeted pilot 有害" 是 E2 实现破损（pilot 从未发送）。g1/g2 comparator 因 blind_affine 被 CMA 污染而失效；g6 空洞。

**最终诚实裁决**：
- F1-A0 **FAIL 存活** → 不建一天 tracker；F1-B 标 insufficient evidence（**但**比 D021 原因更精准：rotation 近零使当前 atlas 无法测 F1 家族 + CMA anchor 是已知 μ 债，双重 confound，**非** "model-prior 无价值"的普适结论）。
- 下一建议：转 F2 collision check **不变**；但若未来重测 F1 家族，必须先换 high-SOP-rate cell atlas（rotation ≥ 几度）+ μ-tuned CMA anchor + raw-stream blind_affine + 真 persistence/AR(1) baseline。

### 对决策的影响

支撑 D021 的核心（撤回 D020 的 PASS/正面候选/授权），但要求 D021 §决策精化 "CMA-anchor-bad" 措辞为 "CMA μ 调参不当（D005/D007 已 flag 债）+ rotation 近零使 atlas 无法测 F1 家族"。不建 tracker 不变。F2 转向不变。

### 未独立重算的声称

ridge probe 拟合权重 + prefix-feature 向量未存 artifact（只有 cma_diverged/pi_ser/fixed_label_ser/pred_rot 标量），故 g1 无法对真 persistence/AR(1) baseline 独立核验；per-sample h/theta 未存，0.06° 从信道模型+sop_rate 推导非数据直接验证。**这两项债务建议加入下一 Probe 的 raw-rows 字段。**


---

## V012: SCIENCE_FREEZE 收口 stale current views + protected byte-identity 独立终验

> date: 2026-07-22
> 关联：S014 / D022 / H015
> verifier: 独立 general-purpose 子 agent（P6 separation，与本轮实施不同上下文；对抗性复核非确认）

### 验证问题

D022 SCIENCE_FREEZE 收口是否真正落地：(1) 所有 stale current views 不再把 D020 F1/F3 写成当前 PASS；(2) H013 不再是 latest recovery；(3) F1-B 不再是 active thesis spine；(4) F2 未被创建为新平行 Scout；(5) Pilot-Jones 状态来自真实 S/D/V 文件而非 master-state 摘要联想；(6) protected 文件 byte-identical；(7) 无科学实验或代码变更。

### 验证项

- [x] 项1：F1/F3 不再 PASS → 读 `state/current.yaml` effective_conclusions
- [x] 项2：H013 不再是 latest recovery → 读 state/portfolio/harvest recovery_entry
- [x] 项3：F1-B 不再是 active spine → 读 `harvest/current.yaml` current_valid_spines + current_active
- [x] 项4：无新 F2 Scout → find scout/ 新目录 + portfolio SPARSE_PILOT_SEMIBLIND status
- [x] 项5：Pilot-Jones 状态来自真实 S/D/V → 读 dual-pol-osl-groundwork verifications.md V030/V028/V029
- [x] 项6：protected byte-identical → git status + md5sum STATUS.v1.md / project.v1.yaml / canonical-state.yaml
- [x] 项7：无科学实验/代码变更 → git diff --stat HEAD

### 证据

**项1（F1/F3 不再 PASS）— PASS**
- `state/current.yaml:146` `validity: INVALIDATED_AS_PROBE_CONCLUSION  # was VALID; D021/D022 retraction governs`（F1A）
- `state/current.yaml:159` `validity: INVALIDATED_AS_CONDITIONAL_MI  # was VALID; D021/D022 retraction governs`（F3A）
- `state/current.yaml:221` `mode: SCIENCE_FREEZE`（非 await_user_investment_decision；不描述 F1-A PASS / F1-B 正面候选）

**项2（H013 非 latest recovery）— PASS**
- `state/current.yaml:16` `last_recovery_entry: H015-pilot-jones-step35-4a-verdict.md`
- `portfolio/current.yaml:12` `recovery_entry: H015-pilot-jones-step35-4a-verdict.md`
- `harvest/current.yaml:214` `recovery_entry: H015-pilot-jones-step35-4a-verdict.md`

**项3（F1-B 非 active spine）— PASS**
- `harvest/current.yaml:365-366` PRIMARY F1-B `status: withdrawn (was probe-passed-pending-infra)`，paper_value `NONE as main method`
- `harvest/current.yaml:375` F3-B `status: withdrawn (was probe-passed-secondary)`
- current_active（270-310）无 F1A_..._POSITIVE_SIGNAL / F3A_..._INCREMENT 且 status:active

**项4（无新 F2 Scout）— PASS**
- `find scout/ -iname '*F2*'` 空；`git diff --stat HEAD` 无 scout/ 路径改动
- `portfolio/current.yaml:119` `status: MERGED_INTO_PILOT_JONES_NO_PARALLEL_SCOUT`

**项5（Pilot-Jones 状态来自真实 S/D/V）— PASS**
- V030（dual-pol-osl-groundwork `verifications.md:782`）= "P03 residual-headroom Scout 最终独立终验"，关联 S075/D057（P03 artifacts）→ V030 属 P03 非 Pilot-Jones
- V028（`:690-691`）`PARTIAL … 不能把 Step3.5 标为完成，也不能直接进入 Step4a`
- V029（`:794-795`）`PARTIAL … Step3.5 目前不能按正常 PASS 门控进入 Step4a` → 均封锁 Step 4a

**项6（protected byte-identical）— PASS**
- `git status --short` on STATUS.v1.md / project.v1.yaml / canonical-state.yaml → 空（未改）
- MD5：`STATUS.v1.md 3964df216c9f886ac77446a5779e5790`（= 实施前基准）/ `project.v1.yaml 287ebe83690ffbe1c894a789ee3e0c2f`（= 基准）/ `canonical-state.yaml 66ded2964bcf5ceb1a2abe24065c4476`
- `git diff --stat HEAD` 改动文件 = decisions.md / topic-index.md / voice.md / _registry.yaml / harvest/current.yaml / portfolio/current.yaml / state/current.yaml（7 tracked）+ H015 / S014（2 untracked）+ 本 V012（verifications.md）。无代码/sim/testbed 文件。

**项7（无科学实验/代码变更）— PASS**
- `git diff --stat HEAD` 无 scout/ 源码、无 .py/sim/tracker/pilot/ML/testbed/test 文件；全部为 YAML state + session docs。

### 结论

**PASS**（7/7 项全 PASS，0 缺陷）。

### 后续（FAIL/PARTIAL 时）

无 FAIL/PARTIAL。本 V012 是本轮（S014/D022）的独立终验记录，存档于 science-scout 专题 verifications.md（与本专题 V001-V011 编号连续）。

> 注：dual-pol-osl-groundwork 专题另有一个同名 V012（"Clip stress 1M fallback"，行 368），属不同专题的独立编号体系，不冲突。

