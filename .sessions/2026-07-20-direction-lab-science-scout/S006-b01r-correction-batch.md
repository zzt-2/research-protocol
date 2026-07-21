# [S006] B01-R 科学纠偏批 — 修复 B01 的 10 条审计发现并重新裁决

> 2026-07-21 | SCIENCE_SCOUT / Fairness Correction | 完成
> 来源: H005（被 H006 取代）+ 用户 2026-07-21 粘贴任务（10 条审计发现）

## 目标

在一个连续对话内完成 B01-R 科学纠偏批：

1. 独立复现用户提出的 10 条 B01 审计发现；
2. 冻结 B01-R 合同（无泄漏切分 + 真实 fixed-μ CMA comparator + 可达退出判据）；
3. 运行纠偏（fixed-μ CMA + C08/C10/C11 + 4 类标签审计的 detector）；
4. 重新裁决 A/B/C 三选一；
5. 独立 verifier 复核；
6. 更新治理（D009 取代 D008；H006 取代 H005；不删除历史）；
7. 单次 consolidated commit，不 push。

不在范围内：训练 ML、修改 B01 原始 JSON、删除 D008/H005、扩展候选池、写论文正文。

## 记录

### 阶段 1：10 条审计发现独立复现 — ALL 10 CONFIRMED

详细证据见 `fairness-batch-b01r/artifacts/b01-audit-reproduction.md`。摘要：

1. **11 cells × 10 seeds = 110 raw**（保留有效）。
2. **validation-optimal fixed-μ CMA 没作为 comparator 运行**：`run_fairness_batch_b01.py:200-206` + `TUNE_GRID["C08"]={"alpha":[...]}` 只调 LinUCB alpha，anchor 用 frozen μ=0.001。
3. **C05 score 实际是 `-min(z2_ratio)`，与 threshold/CUSUM drift 无关**：`run_fairness_batch_b01.py:348-355`。
4. **raw frozen C05 参数与 synthesis/H005 不一致**：raw=(0.2, 0.01), synthesis/H005=(0.25, 0.02)。
5. **tuning seeds 11-15 与 evaluation seeds 11-20 重叠**：5 seeds 泄漏。
6. **真实非 validation cells = 7，但合同写"9/11 held-out"判据**：9/7 不可达。
7. **single-class cell AUROC 应为 undefined，不能按 0.5 报告**：6/11 cells 误报为 0.5。
8. **degradation onset/lead-time/PR-AUC/recall@5%FPR/calibration 没真实计算**：raw JSON 中 C05 aggregate 只有 5 个字段。
9. **`oracle_pi_ser > 0.3` ≠ inner-ring collapse；snr05 AWGN 主导错误必须分开**：snr05 全部 10 seeds 被标 "collapse" 但 oracle 几乎不能恢复（Δ≤0.06）。
10. **C11 真正可靠信号只有 2 个 held-out 长窗 cell**：第 3 个长窗（snr20-nominal-long）是 validation cell。

### 阶段 2：B01-R 合同冻结

`fairness-batch-b01r/batch-contract.v1.yaml`：6 个角色明确分离（diagnostic anchor、validation-optimal fixed-μ CMA、C08/C10/C11、detector scoring baselines）；无泄漏 seed 切分（tuning=[11-15]，test=[21-30]）；退出判据 5/7（可达）；4 类标签审计；真正计算 9 项 detector 指标。

### 阶段 3：运行

`run_fairness_batch_b01r.py --tune-and-eval`，64.5s 完成。Frozen params:
- fixed_mu_cma: μ=0.01（grid 中最大；显著优于 anchor μ=0.001）
- C08: α=10.0
- C10: μ=1e-5
- C11: dd_step_size=1e-4
- C05: (0.2, 0.01) DEFAULT-GRID fallback（4-cat 标签审计让所有 validation cells 在严格二分投影下变 single-class，macro-AUROC tuning score=-1.0；按合同 fallback 到 grid 首项）。

### 阶段 4：detector 重建

`b01r_detector.py`：4 类标签审计（inner_ring_recoverable / awgn_dominated / healthy / ambiguous）；min-z2-ratio 零参数 baseline；C05 alert earliness score（与被调参数有关）；degradation onset；paired bootstrap CI；real metrics。

4-cat 标签结果（110 seeds）：inner_ring=14（12.7%），awgn=20（18.2%），healthy=33（30%），ambiguous=43（39.1%）。**关键**：held-out 长窗 cell（snr10-fg100-long / snr15-fg1000-long）的 inner_ring 数 = 0。这意味着 B01 所谓"长窗改善"实际发生在 AWGN/ambiguous 区域，不是 inner-ring collapse。

### 阶段 5：重新裁决 — VERDICT B

`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`：

- **公平性存活**：5/7 close threshold 未达。最佳方法 fixed_μ CMA 只关闭 1/7（snr05）。paired bootstrap CI 显示 fixed_μ CMA 在 7/7 held-out cells 显著优于 anchor；C11 在 4/7 显著改善但 |Δ|≤0.026，headroom 仍 ≥6×MDE；C10 与 anchor 无显著差异（confirm B01 H021 否定的 reproducible）；C08 混合（2 长 cell 微改善 + 1 短 cell 微退化）。
- **detector target 不 READY**：严格 4-cat 标签后只有 2 个 held-out cells（snr25-short / snr20-fg100-short）two-class。C05 在这两个 cell 上 AUROC=0.875 / 0.75，lead_time=2 blocks，但样本太少不能支撑 B02 ML detector target。

**B02 ML detector batch NOT authorized**。下一动作：转向其他机制族（equalizer 侧 C04/C09 学习型校正器，task comparator=fixed_μ CMA；或 C13 pilot-aided / C12 coded）。

### 阶段 6：独立 verifier 复核

子 agent adversarial verifier，11/11 checks PASS，CONFIRM HIGH confidence。3 个 P1 issues（均不阻断）：

1. C05 fell back to first-grid params（已 honest 报告 + 合同授权 fallback；synthesis 措辞已收紧为"default-grid C05"）。
2. Validation cells 在 test seeds 上也运行（intentional，用于报告覆盖；Go/Kill 仅用 held-out，无泄漏；H006 标注）。
3. H006/D009 暂未写入（本轮 governance 阶段正在补）。

### 阶段 7：governance 更新

- `decisions.md`：新增 D009，标 D008 为 superseded。
- `topic-index.md`：更新进展线索 / 已确认结论 / 当前位置 / 未决项；范围边界不变。
- `voice.md`：登记用户 2026-07-21 纠偏原话。
- `_registry.yaml`：last_updated 加 S006/D009/H006。
- `verifications.md`（首次创建本专题）：V001 B01-R 独立 verifier CONFIRM。
- `campaigns/science-scout-2026-07-20/harvest-addendum.v3-b01r.yaml`：H029-H034。
- `H006-b01r-correction-complete.md`：取代 H005（不删除）。

### 阶段 8：commit

单次 consolidated commit，不 push。

## 决策引用

- D008：B01 公平闭合 + 条件授权 B02（**新建 superseded by D009**）
- D009：B01-R 纠偏 — VERDICT B；撤回 B02 授权；rotation 转向非 detector 机制族（**新建**）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（B01-R 是 B01 的有界纠偏，未扩 Portfolio，未训练 ML，未写论文）。

## 后续

下一入口：H006。两条合法路径（用户已授权"按 A/B/C 自动收口"，VERDICT B 自动 rotation）：

1. **equalizer 侧**：fixed_μ CMA μ=0.01 是新 baseline reference；C11 在 4/7 cells 有显著小改善；问学习型校正器 C04/C09 能否恢复 DD-LMS 不能恢复的残余（task comparator = fixed_μ CMA，不是 frozen-μ anchor）。
2. **不同机制族**：C13 pilot-aided（不同信息类）或 C12 coded（需 unblock）。

B02 detector 路线 **暂停**，直到建立可信的 collapse label 基础设施（更丰富的 oracle 类、更大 test seed budget、或 representation learning）。
