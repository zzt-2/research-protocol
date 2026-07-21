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
