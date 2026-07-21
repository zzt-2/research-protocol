# [S007] B01-R hotfix v2 — 修复外部评审的 7 个实现 flaw，verdict B→A

> 2026-07-21（hotfix）| SCIENCE_SCOUT / Fairness Correction Hotfix | 完成
> 来源: S006（被本 hotfix 修正）+ 外部评审 2026-07-21（7 个 flaw）

## 目标

外部评审指出 B01-R v1（S006/D009）有 7 个实现 flaw，其中 4 个 P0 机械触发了 VERDICT B，3 个是 claim overreach。评审结论："verdict 被实现问题污染；不要开 B02 也不要直接开 C04/C09；先做 hotfix 再审"。

本轮 hotfix 目标：连续修复全部 7 个 flaw，重新运行 + 重新裁决 + 独立复核 + 更新治理。

## 记录

### 评审 7 个 flaw 全部独立确认

用 raw JSON 直接核验（详见 `fairness-batch-b01r-v1-synthesis.md` §0）：

1. **min_z2_ratio_score 只读 `z2_over_R2_ratio`，anchor trace 只有 `output_power` → 110/110 NaN → adjudicator 机械判 B**。CONFIRMED。
2. **detector 可在 warmup（block 0/1）触发 alert；reported lead_time=+2 实际是 onset(2)-alert(0) 的口径错位**。CONFIRMED。
3. **recall@5%FPR 在 n_neg=2/4/6 下实际是 25%/50%/17%，不是 5%**。CONFIRMED。
4. **（1 的后果）VERDICT B 被机械触发，非科学得出**。CONFIRMED。
5. **ambiguous 计数 synthesis 写 43，S006 写 54，实际 51**。CONFIRMED。
6. **fixed_μ μ=0.01 是 grid 边界（max of [1e-4..1e-2]），真最优可能在更大值**。CONFIRMED。
7. **C11 "4/7 改善" 只 vs 旧 μ=0.001 anchor；vs fixed_μ=0.01 CMA 时 C11 在 7/7 cells 都更差**。CONFIRMED。

### Hotfix 实施

**code 修复（`b01r_detector.py`）：**
- HF1：`min_z2_ratio_score` 加 `output_power → ratio` fallback（与 c05_alert_score 一致）。
- HF2：`c05_alert_score` 加 warmup guard，block < warmup=2 不发 alert。
- HF3：`recall_at_fpr` 改返回 tuple `(recall, actual_fpr, fp_budget)`；caller 报 ACTUAL_FPR + note 当 actual > target。

**runner 修复（`run_fairness_batch_b01r.py`）：**
- HF6：fixed_mu_cma grid 扩展 `[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]`。
- HF7：新增 `C11_fixed_mu`（stage-1 继承 fixed_mu_cma 的 tuned μ）；先 tune fixed_mu_cma，再 tune C11_fixed_mu dd_step_size；paired CI 同时报 `_vs_anchor` 和 `_vs_fixed_mu_cma`。
- HF4：adjudicator 不再机械触发；包含 C11_fixed_mu 在 close-count；detector_target_ready gate 用修复后的 min_z2（不再 0）。
- HF5：ambiguous 计数由 raw 重算 = 51/110（46.4%），统一报。

**contract 修复（`batch-contract.v1.yaml`）：**
- HF8：新增 `forward_rules_for_corrector_batch`，要求任何未来 corrector batch 用 fixed_μ + blind-affine 双 task comparator。
- forbidden 加 5 条 hotfix 专属护栏（report_5pct_FPR_when_not_resolvable 等）。

### 重新运行结果（hf2190.8s）

**Frozen params 变化：**
- fixed_mu_cma: μ=0.01 → **μ=0.03**（HF6 interior optimum）
- 新增 C11_fixed_mu: dd_step_size=1e-4, stage1_mu=0.03, best_score=-0.2023（所有方法最佳）

**VERDICT: B → A**（`A_B01R_FAIRNESS_SURVIVES_AND_DETECTOR_TARGET_READY`）：
- 公平性存活：best 方法 C11_fixed_mu 关闭 3/7 cells < 5/7 threshold。
- detector target ready：min_z2 和 c05_alert_earliness 各有 2 个 two-class held-out cells。

**关键新发现：**
- **C11_fixed_mu 在 4/7 held-out cells 显著优于 fixed_μ CMA**（paired CI 排除 0）：snr15-short / snr25-short / snr20-fg100-short / snr10-fg100-long。|Δ| ≈ 0.01 PI-SER。这是 v1 完全错过的真阳性 method signal。
- **min_z2_ratio 在 2 个 two-class cells 上 AUROC=1.000**，超过 "tuned" C05（0.875 / 0.5）。Conventional baseline 已达 ceiling；ML 不能在 AUROC 上赢，必须在 lead time / calibration / generalization 上赢。
- **lead_time 实际全 ≤ 0**（mean = -5.95 blocks）：detector 在 degradation onset 之后才 fire，没有真正提前预警。v1 的 "+2 blocks lead time" 完全是 warmup artifact。
- **5% FPR 不可解析**：n_neg=4 时 actual=25%，n_neg=2 时 actual=50%。

### 独立 verifier 复核（V002）

子 agent adversarial verifier，特别加强 skepticism（V001 漏掉了 v1 的 7 个 flaw）。结果：**13/14 PASS + 1 PARTIAL PASS（P1 awgn 计数文本错误，已修复）**。CONFIRM HIGH confidence。verifier 抓到了我 synthesis 中 awgn=20 vs 实际 18 的错误（我已修）。

### 评审 flaw 6（C11 不应直接推导 C04/C09）的回应

评审说："C11 的 4/7 显著改善只成立于相对旧 anchor；相对新公平 baseline fixed_μ=0.01 时 7/7 都更差；C11 自身又从旧 anchor warm-start；所以不能直接推导跑 C04/C09"。

我的处理：
- **CONFIRM C11 vs fixed_μ=0.01 时 7/7 更差**（v1 数据已核验）。
- **新增 C11_fixed_mu（stage-1=μ=0.03）**：现在 vs fixed_μ CMA 时 4/7 显著改善。这才是 apples-to-apples。
- **不直接推导 C04/C09**：contract 加 forward rule（HF8），要求双 comparator（fixed_μ + blind-affine）；synthesis §6 明示 "C11_fixed_μ 的 0.01 PI-SER margin 是 learned corrector 必须超越的 gap"，且 "需用户战略决策"。
- **VERDICT A 不自动授权 B02**：synthesis §6 明示 detector target ready 是 "by contract letter" 但 "thin"（2 个 two-class cells，ML 不能在 AUROC 上赢 ceiling，lead time 负）；B02 若跑需换目标（lead-time maximization）。

## 决策引用

- D008：B01 verdict（superseded by D009, amended by D010）
- D009：B01-R v1 VERDICT B（amended by D010 — verdict 改 A；C11/C11_fixed_mu 信号重评；forward rule 加）
- D010：B01-R hotfix v2 VERDICT A（**新建**）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（hotfix 是 B01-R 的有界修复，未扩 Portfolio，未训练 ML，未写论文，未开新方向）。

## 后续

下一入口：H007。VERDICT A → problem survives AND detector target ready → 选最干净的 contribution axis：

1. **路径 1（equalizer 侧 learned corrector C04/C09）**：target C11_fixed_μ 留下的 0.01 PI-SER margin。Task comparators（HF8 forward rule）：fixed_μ CMA μ=0.03（system anchor）+ blind_affine_16qam（task-specific Kill, FR-21）。Go: paired CI 显著超越 C11_fixed_mu on ≥ 4/7 cells。
2. **路径 2（detector 侧 lead-time maximization C01/C02/C06）**：target positive lead time（conventional 是 -1.33）。Task comparator: min_z2_ratio（AUROC=1.000 ceiling）。Go: positive mean lead time on ≥ 2 two-class cells without AUROC regression。

**不自动启动任一路径**——需用户拍板（评审明确说"先 hotfix 通过再审，然后才开新对话进入下一批"）。
