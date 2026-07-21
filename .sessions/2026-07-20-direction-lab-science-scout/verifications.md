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
