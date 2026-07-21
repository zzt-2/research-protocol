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
