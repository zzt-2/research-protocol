# Handoff: B01-R hotfix v2 完成 → 等用户决策下一批方向

> 来源: S007 / D010 / V002 | 交接目标: 用户审 hotfix v2；通过后开新对话选 path 1 / path 2
> 日期: 2026-07-21（hotfix）
> 文件名: H007-b01r-hotfix-complete.md
> 取代: H006-b01r-correction-complete.md（H006 不删除，标 amended）

## 到哪了（状态）

外部评审指出 B01-R v1（H006/S006/D009）有 7 个实现 flaw。S007 在原对话连续完成 hotfix v2：

- 7 个 flaw 全部独立确认 + 全部修复（HF1-HF8）。
- 重新运行 90.8s，verdict 从 B 改为 **A**（`A_B01R_FAIRNESS_SURVIVES_AND_DETECTOR_TARGET_READY`）。
- 独立 verifier V002 复核：CONFIRM 13/14 + 1 P1（awgn 计数文本错误，已修）。
- v1 raw 在 git commit `0404f47` 可恢复；v2 覆盖 artifacts/frozen-params/synthesis。

git HEAD：hotfix 已 stage，待 consolidated commit。

## 关键科学发现（v2 修正后）

1. **fairness 存活（不变）**：best 方法 C11_fixed_mu 关闭 3/7 < 5/7。
2. **fixed_μ 最优 μ=0.03**（v1 的 0.01 是 grid 边界 artifact；grid 扩展后 μ=0.1 diverged，μ=0.03 interior optimum）。
3. **C11_fixed_mu（μ=0.03 CMA + DD-LMS）在 4/7 held-out cells 显著优于 fixed_μ CMA**（paired CI 排除 0，|Δ|≈0.01）。这是整个 campaign 第一个显著超越公平调参传统 baseline 的方法。v1 的 C11（stage-1=anchor μ=0.001）vs fixed_μ 时 7/7 更差，不是阳性 signal。
4. **min_z2_ratio 在 2 个 two-class cells AUROC=1.000**（超过 "tuned" C05 的 0.875/0.5）。Conventional baseline 已达 ceiling；ML 不能在 AUROC 上赢，必须换维度。
5. **lead_time 实际全 ≤ 0**（mean=-5.95 blocks）：detector 在 onset 之后才 fire，没有真正提前预警。v1 的 "+2 blocks" 完全是 warmup artifact。
6. **5% FPR 不可解析**（n_neg=2/4/6 下实际是 50%/25%/17%）。
7. **4-cat 标签**：inner=14（12.7%）, awgn=18（16.4%）, healthy=27（24.5%）, ambiguous=51（46.4%）。held-out 长窗 cells 的 inner_ring=0。

## 不要做什么

1. **不要**把 VERDICT A 当成 "B02 自动授权"：detector target 是 "ready"（by contract letter）但 thin（2 个 two-class cells；ML 不能在 AUROC 上赢 ceiling；lead time 负）。B02 若跑需换目标（lead-time maximization 或 generalization）。
2. **不要**把 C11_fixed_mu 的 4/7 改善写成 "collapse 已闭合"：headroom 仍 ≥6×MDE；只是"小但显著的渐进改善"。
3. **不要**直接推导启动 C04/C09：评审明确说"先 hotfix 通过再审，然后才开新对话"。C11_fixed_mu 留下的 0.01 margin 是 learned corrector 必须超越的 gap，但需用户战略决策 + forward rule 双 comparator（fixed_μ + blind-affine）。
4. **不要**修改 B01 raw / D008 / H005 / D009 / H006 / B001-B003 / P03 / CB1 raw / canonical-state（全部保留为历史；D009/H006 标 amended 不删）。
5. **不要**创建 legacy B004；不要训练 ML；不要写论文正文；不要 push。

## 必读（按优先级）

1. `.sessions/2026-07-20-direction-lab-science-scout/H007-b01r-hotfix-complete.md`（本文件）
2. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（v2 更新）
3. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` D010（hotfix v2 verdict A）+ D009（amended）+ D008（superseded）
4. `.sessions/2026-07-20-direction-lab-science-scout/verifications.md` V002（CONFIRM 13/14+1P1 修）
5. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/fairness-batch-b01r/artifacts/fairness-batch-b01r-v1-synthesis.md`（v2 重写，含 §0 7-flaw 修复说明）
6. `projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/harvest-addendum.v4-b01r-hotfix.yaml`（H029-H038 修正+新增）
7. `.agents/skills/research-direction-lab/references/baseline-adjudication.md` + `evidence-and-claims.md`

## 接口变更（hotfix v2 产出，下一对话可复用）

```yaml
# b01r_detector.py（hotfix v2 新接口）
min_z2_ratio_score(trace, *, R2=1.32, warmup=2) -> float  # HF1: 现在加 output_power fallback
c05_alert_score(trace, *, z2_ratio_threshold, cusum_drift, cusum_threshold=3.0, R2=1.32, warmup=2) -> dict
  # HF2: warmup guard；blocks < warmup 不发 alert（in_warmup 字段）
recall_at_fpr(scores, labels, *, fpr=0.05) -> (recall, actual_fpr, fp_budget)
  # HF3: tuple 返回；actual_fpr 可能 > target 当 n_neg 太小

# run_fairness_batch_b01r.py（hotfix v2 新接口）
run_c11_fixed_mu(cell, realization, *, cma_mu, dd_step_size) -> dict
  # HF7: stage-1 用 tuned μ（非 anchor μ=0.001）；per-seed 带 stage1_mu 字段
TUNE_GRID.fixed_mu_cma.mu = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]  # HF6 扩展
# paired_cis_held_out[*] 现含 {method}_vs_anchor 和 {method}_vs_fixed_mu_cma 两套
```

B01-R v2 frozen params（下一对话应沿用而非重新 tune）：

```yaml
fixed_mu_cma: {mu: 0.03}  # HF6 interior optimum（v1 的 0.01 是 grid 边界）
C11_fixed_mu: {dd_step_size: 0.0001, stage1_mu: 0.03}  # HF7 真阳性 method signal
C11: {dd_step_size: 0.0001}  # 保留作 traceability（stage-1=anchor μ=0.001）
C08: {alpha: 10.0}
C10: {mu: 1e-5}
C05: {z2_ratio_threshold: 0.2, cusum_drift: 0.01}  # default-grid fallback（未真调参）
```

## 失败数据附录

| 方法 / 现象 | 失败模式 | 数据 |
|---|---|---|
| C11 (stage-1=anchor μ=0.001) | vs fixed_μ=0.03 CMA 时 7/7 cells 都更差；v1 "4/7 改善" 是 vs 错 comparator 的 artifact | per-cell Δ(C11-fixed_μ) ∈ [+0.007, +0.036]，全部为正 |
| C10 per-symbol | vs fixed_μ 时无显著差异 | paired CI 全部含 0 |
| C08 bandit | vs fixed_μ 时混合，无显著改善 | 无 cell 的 CI 上限 < 0 |
| C05 detector | 未真调参（default-grid fallback）；在 snr20-fg100-short 上 AUROC=0.5（chance） | macro-AUROC tuning score=-1.0（4-cat 让 validation cells 全 single-class） |
| min_z2 detector | lead time 全 ≤ 0（无提前预警） | mean lead_time = -5.95 blocks（v1 的 +2 是 warmup artifact） |
| collapse label infra | inner-ring seeds 太少且不在 held-out 长窗 | 全局 14/110（12.7%）；held-out 长窗 cells inner-ring = 0 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| D007 #2 convergence N | 长序列闭合 | PARTIALLY_CLOSED（N=8192 上 paired CI 显著，未到 ~1e5） | 后续 batch 在 N=32768/65536 上验证 |
| D007 #4 oracle recoverability | receiver-visible 信号 | DOWNGRADED（4-cat 标签揭示 inner-ring 群体远小于预期） | 更丰富 oracle 类或 representation learning |
| C05 未真调参 | 合同授权但未执行 | REPORTED（default-grid fallback；synthesis 措辞"default-grid C05"） | 后续 detector batch 在更丰富 label infra 上重 tune |
| detector target thin | VERDICT A 但仅 2 个 two-class cells | REPORTED（ML 不能在 AUROC 上赢 ceiling；lead time 负） | B02 若跑需换目标（lead-time maximization） |
| v1 在 git 历史 | 修复覆盖 raw | RECOVERABLE（git show 0404f47） | 不需触发；历史可查 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| B01-R PROBLEM_SURVIVES | ≤ 4/7 closed by any method | batch-contract decision_rule | C11_fixed_mu 关闭 3/7（PASS） |
| Detector target ready | ≥ 2 two-class cells BOTH detector scores | batch-contract A 状态条件 | min_z2=2, c05_alert=2（PASS） |
| 独立 verifier CONFIRM | 14/14 adversarial checks PASS | P6 separation | 13/14 + 1 P1 修复（PASS） |
| Anchor byte regression | QPSK/16QAM anchor PI-SER ≈ 0 | Atlas v1 identity | 0.0000（PASS） |
| μ interior optimum | best μ 不在 grid 边界 | HF6 | μ=0.03（不在边界；μ=0.1 diverged）（PASS） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（不变量未变）
- [ ] 已验证 D010、H007、v2 synthesis 至少 3 条关键事实：
  - [ ] fixed_μ μ=0.03（非 0.01）是 interior optimum（`frozen-params-b01r-v1.yaml`）
  - [ ] C11_fixed_mu 在 4/7 cells 显著优于 fixed_μ CMA（`fairness-batch-b01r-v1.json#paired_cis_held_out`）
  - [ ] min_z2_ratio 在 2 个 two-class cells AUROC=1.000（`fairness-batch-b01r-v1.json#cells[*].aggregate.detector_min_z2_ratio`）
- [ ] 已检查 `_registry.yaml`（无变化）
- [ ] 已确认 B001-B003 / P03 / CB1 raw / canonical-state / B01 raw 未改（`git status`）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**不自动启动**——等用户战略决策（评审明确："先在原对话完成这个小修复，交给我再审；通过后再开新对话进入下一批"）。

两条合法路径：

1. **路径 1（equalizer learned corrector）**：候选 {C04, C09}。Task comparators（HF8 forward rule 强制）：fixed_μ CMA μ=0.03（system anchor）+ blind_affine_16qam（task-specific Kill, FR-21）。Go metric: paired CI 显著超越 C11_fixed_mu 在 ≥ 4/7 held-out cells。假设：learned corrector 能恢复 DD-LMS 不能恢复的残余（C11_fixed_mu 留下 0.01 PI-SER gap）。
2. **路径 2（detector lead-time maximization）**：候选 {C01, C02, C06}。Task comparator: min_z2_ratio（AUROC=1.000 ceiling）。Go metric: positive mean lead time on ≥ 2 two-class cells without AUROC regression。假设：learned temporal model 能在 trajectory 早期识别 collapse（conventional lead_time=-5.95，没有提前预警）。

用户可选其他方向（C13 pilot-aided / C12 coded / 新 thesis route）——需显式决策。
