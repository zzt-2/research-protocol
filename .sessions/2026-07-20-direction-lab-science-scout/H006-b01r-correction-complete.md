# Handoff: B01-R 纠偏完成 → rotation 到非 detector 机制族

> 来源: S006 / D009 / V001 | 交接目标: 下一对话决定 rotation 方向（equalizer 学习型校正器 vs 不同信息类）
> 日期: 2026-07-21
> 文件名: H006-b01r-correction-complete.md
> 取代: H005-fairness-batch-b01-complete.md（H005 不删除，标 superseded）

## 到哪了（状态）

S006 在一个连续对话内完成 B01-R 科学纠偏批：

- **10 条审计发现全部独立复现**（`fairness-batch-b01r/artifacts/b01-audit-reproduction.md`）。
- **B01-R 合同冻结 + 运行 + detector 重建**（`fairness-batch-b01r/` 全量新增，未动 B01 raw）。
- **VERDICT B**：`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`。
  - fairness 存活（强证据）：fixed_μ CMA（μ=0.01，B01 从未运行的 comparator）在 7/7 held-out cells 显著优于 frozen-μ anchor；C11 在 4/7 cells 显著小改善；C10 与 anchor 无显著差异；C08 混合。最佳方法只关闭 1/7 cells。
  - detector target NOT ready：4-cat 标签审计显示 B01 的 binary label 把 AWGN 错误误当 collapse；只有 14/110 seeds 是 true inner-ring；held-out 长窗 cell 的 inner-ring 数 = 0；只有 2 个 held-out cells two-class。
- **B02 ML detector batch NOT authorized**（D009 撤回 D008 的授权）。
- **独立 verifier CONFIRM**（V001，11/11 checks PASS，HIGH confidence）。
- **harvest H029-H034**（`harvest-addendum.v3-b01r.yaml`）。

git HEAD：B01-R artifacts + governance 已 stage，待 consolidated commit（Phase 8）。

## 下一步干什么

**用户战略决策点**（H006 是 rotation 入口；VERDICT B 自动 rotation 已授权，但 rotation 方向二选一建议用户拍板）：

1. **路径 1（推荐）— equalizer 侧学习型校正器**：
   - 候选：C04（learned corrector，trace features → z residual correction）或 C09（residual DD-LMS with learned reference）。
   - task-specific comparator：**fixed_μ CMA μ=0.01**（D009 确立的新 baseline reference），**不是** frozen-μ anchor。
   - 假设：C11 已证 4/7 cells 有显著小改善但 |Δ|≤0.026；学习型校正器能否突破 DD-LMS 的 hard-decision 限制，恢复更多残余？
   - claim ceiling：SLICE，narrowed to "learned corrector recovers residual error that DD-LMS (C11) cannot"。
   - **不依赖 collapse detector target**，绕过 B01-R 暴露的 label 问题。

2. **路径 2 — 不同信息类（C13 pilot-aided 或 C12 coded）**：
   - C13：pilot-aided channel estimation，不同信息类（CSI partial）；INFRASTRUCTURE_BLOCKED，需 unblock pilot 插入 + 估计器接口。
   - C12：soft/coded output，不同评估口径；INFRASTRUCTURE_BLOCKED，需 unblock soft-decision evaluator。
   - 假设：不同信息类可能完全改变 headroom 结构（pilot 提供的 CSI 可能让 collapse 不再发生）。
   - 成本：高于路径 1（需 adapter sprint）。

**用户原话（来自 voice.md 2026-07-21）**：
- "本轮不是继续 B02，也不是扩展候选池，而是完成一次有界的 B01-R 科学纠偏批"
- "请连续推进到能够重新裁决"B02 是否 READY"为止" → **本轮已达成**。
- "普通的局部失败、参数不工作或单候选阻断不要停下来问我，按上述 A/B/C 自动收口" → VERDICT B 已自动收口。

**因此**：如无战略变化，下一对话可直接启动路径 1（C04/C09 adapter sprint + 冻结合同 + 运行）。如果用户想换方向，需显式决策。

## 纪律（和下一步直接相关的约束）

1. **不要**重启 B02 ML detector batch——D009 已撤回授权，collapse label 基础设施未建。
2. **不要**把 fixed_μ CMA（μ=0.01）的 7/7 显著改善写成"问题已闭合"——只关闭 1/7 cells；改善幅度 |Δ|=0.02-0.06 PI-SER，headroom 仍 ≥6×MDE。
3. **不要**把 C11 的 4/7 显著改善写成"长窗改善"——B01-R 已澄清：held-out 长窗 cells 的 inner-ring 数 = 0，改善发生在 AWGN/ambiguous 区。
4. **不要**修改 B01 原始 raw / D008 / H005 / B001-B003 / P03 / CB1 raw / canonical-state（protected history）。
5. **不要**创建 legacy B004。
6. **不要**训练任何 ML（除非下一对话明确授权 C04/C09 的学习型 corrector，且只在该 batch 范围内）。
7. **不要**写论文正文；不要 push。

## 接口变更（B01-R 产出，下一对话可复用）

```yaml
# b01r_detector.py（detector + label audit）
assign_label_4cat(*, nearest_pi_ser, oracle_pi_ser, mean_z2_ratio, min_z2_ratio, mde=0.005) -> str
  # 返回 "inner_ring_recoverable_collapse" / "awgn_dominated_error" / "healthy" / "ambiguous"
collapse_label_for_auroc(label_4cat: str) -> int | None  # None = exclude from AUROC
min_z2_ratio_score(trace, *, warmup=2) -> float           # 零参数 baseline
c05_alert_score(trace, *, z2_ratio_threshold, cusum_drift, cusum_threshold=3.0, R2=1.32, warmup=2) -> dict
  # 真正与被调参数有关的 detector score（earliness）
degradation_onset_block(trace, *, R2=1.32, collapse_z2_ratio_threshold=0.5, sustained_blocks=2, warmup=2) -> int | None
auroc_or_none(scores, labels) -> float | None  # None if single-class
pr_auc_or_none / recall_at_fpr / false_alarm_rate / brier_score / expected_calibration_error / detector_score_to_prob

# run_fairness_batch_b01r.py 公开接口（C04/C09 batch 可 import 复用）
make_realization(cell, seed) -> dict            # 共享信道 realization（不变）
pi_ser_from_z(zX, zY, realization, *, eval_start, calibration_end, eval_end) -> dict
run_fixed_mu_cma(cell, realization, *, mu) -> dict   # 新 baseline reference（μ=0.01 tuned）
run_anchor(cell, realization) -> dict                # frozen-μ=0.001 anchor（diagnostic）
run_c11(cell, realization, *, dd_step_size) -> dict  # C11 reference（4/7 显著小改善）
paired_bootstrap_ci(deltas, *, n_boot=10000, alpha=0.05) -> dict  # 配对 CI 工具
```

B01-R frozen params（C04/C09 应沿用而非重新 tune）：

```yaml
# fairness-batch-b01r/artifacts/frozen-params-b01r-v1.yaml
fixed_mu_cma: {mu: 0.01}      # 新 baseline reference
C11: {dd_step_size: 0.0001}   # C11 reference（小改善）
# C05 default-grid: {z2_ratio_threshold: 0.2, cusum_drift: 0.01}
```

## 失败数据附录

| 候选 | 失败模式 | 数据 |
|---|---|---|
| C10 per-symbol | 与 anchor 无显著差异（paired CI 含 0） | snr10-fg100-long: anchor=0.4129, C10=0.4145, Δ(method-anchor)=+0.002 [-0.001,+0.004] |
| C08 bandit | 混合（2 长 cell 微改善 + 1 短 cell 微退化） | snr15-short Δ=+0.003 [0,+0.006] 显著变差；snr10-fg100-long Δ=-0.011 [-0.025,-0.001] 显著改善 |
| C05 detector | strict 4-cat 标签后只有 2 个 held-out cells two-class | snr25-short AUROC=0.875（n=8）；snr20-fg100-short AUROC=0.75（n=4）；其他 held-out NA |
| collapse label infra | inner-ring seeds 太少且不在 held-out 长窗 | 全局 14/110 (12.7%)；held-out 长窗 cells inner-ring 数 = 0 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| D007 #2 convergence N | 长序列闭合 | PARTIALLY_CLOSED（B01-R 在 N=8192 上 paired CI 显著，但未到 ~1e5） | 后续 batch 在 N=32768/65536 上验证 |
| D007 #4 oracle recoverability | receiver-visible 信号 | DOWNGRADED（4-cat 标签揭示 inner-ring 群体远小于预期；oracle affine 不充分区分 collapse vs AWGN） | 更丰富 oracle 类（如 polynomial）或 representation learning |
| C03/C12/C13 action/evaluator hook | runnable 要求 | INFRASTRUCTURE_BLOCKED | 路径 2（不同信息类）触发建设 |
| C05 default-grid fallback | 合同授权但未真调参 | REPORTED（synthesis §2 收紧措辞；contract §tuning_protocol.detector_two_class_only_rule） | 后续 detector batch 在更丰富 label infra 上重 tune |
| Validation cells 在 test seeds 上也运行 | 报告覆盖 vs 严格隔离 | INTENTIONAL（Go/Kill 仅用 held-out；无泄漏） | 若未来要严格隔离，需重设计 evaluate_held_out 只跑 held-out cells |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| B01-R PROBLEM_SURVIVES | ≤ 4/7 closed by any method | batch-contract.v1.yaml B01-R decision_rule | fixed_μ 关闭 1/7，其他 0/7（PASS） |
| Detector target ready | ≥ 2 two-class held-out cells for BOTH detector scores | batch-contract.v1.yaml A 状态条件 | c05_alert_earliness=2, min_z2_ratio=0（FAIL → VERDICT B） |
| 独立 verifier CONFIRM | 11/11 adversarial checks PASS | P6 separation | 11/11（PASS） |
| Anchor byte regression | QPSK anchor PI-SER ≈ 0 | Atlas v1 identity | 0.0000（PASS） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（不变量未变）
- [ ] 已验证 D009、H006、synthesis 至少 3 条关键事实：
  - [ ] fixed_μ CMA μ=0.01 在 7/7 held-out cells 显著优于 anchor（`fairness-batch-b01r-v1.json#paired_cis_held_out`）
  - [ ] held-out 长窗 cells 的 inner-ring seeds = 0（`fairness-batch-b01r-v1.json#cells[*].aggregate.label_4cat_counts`）
  - [ ] VERDICT = `B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`（`fairness-batch-b01r-v1.json#adjudication.verdict`）
- [ ] 已检查 `_registry.yaml` 的 depends_on / conflicts_with（无变化）
- [ ] 已确认 B001-B003 / P03 / CB1 raw / canonical-state / B01 raw 未改（`git status` 无匹配）且 legacy B004 不存在
- [ ] 已确认当前范围未违反"明确不含"（无 ML、无论文正文、无候选池扩展）

## 下一轮

**默认（无用户战略变化）**：路径 1 — equalizer 侧 C04/C09 学习型校正器 batch。

1. 冻结 B01-R2 / B03 合同（模板：`fairness-batch-b01r/batch-contract.v1.yaml`）：
   - 候选：{C04 learned corrector, C09 residual DD-LMS with learned reference}
   - task-specific comparator：**fixed_μ CMA μ=0.01**（D009 新 baseline reference）
   - 共享输入：causal CMA-trace features（沿用 B01-R `_trace`，需 stacker adapter sprint）
   - Go metric：paired-CI 显著改善 over fixed_μ CMA on ≥ 4/7 held-out cells
   - claim ceiling：SLICE，narrowed to "learned corrector recovers residual error that DD-LMS (C11) cannot"
2. 若 B01-R2 PASS → 收获 positive + 考虑 pilot 主线候选晋级
3. 若 B01-R2 FAIL → record LOCAL_NEGATIVE on learned corrector，rotation 到 C13 / C12（路径 2）

**用户战略决策点**（B01-R2 前可问）：
- 路径 1 vs 路径 2（equalizer 学习型校正器 vs 不同信息类）？
- 是否需要重大算力投入（如多 batch 连续跑）？
- 是否切换 thesis route？
