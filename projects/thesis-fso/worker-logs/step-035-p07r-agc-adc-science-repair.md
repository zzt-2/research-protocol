# step-035 — P07-R F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG 科学完整性修复（F 族，修正重判）

> 2026-07-31 | campaign P07-R | family F（修复后关闭）| executor: 主线程内独立实现
> 上游：D046（binding decision，冻结旧 P07 科学结论）+ 用户 P07-R 执行指令
> 验收：V072 PART 1（根因复现）+ V072 PART 2（修复后独立 verifier 10/10 ACCEPT）

## 任务

用户 P07-R 执行指令：旧 P07 科学结论（`NO_DIAGNOSTIC_METHOD_SIGNAL` + Phase A/B/C 数字 +
"clipping–resolution 折中真实存在"声称）不得继续使用。systematic-debugging 流程：
根因复现（保存修复前证据）→ 最小修复 → fresh 重跑 → 独立 verifier → 治理纠偏 → 单次 commit。
不修改旧 p07_* 文件隐藏错误，新建 `p07r_*` 版本化路径。

## 三根因复现（修复前，证据 `p07r_prefail_evidence.json`）

- **H1 SCALE（致命）**：`_p07_adapters.quantize_iq` 返回 `q=Q(g·z)`，但 `_p07_runner`/`_p07_batch`
  把 `q` **直接**喂给冻结接收链（`_p07_runner.py:118`、`_p07_batch.py:86`），**未除以 g**。
  下游 `estimate_h_blind_perblock`（`sc_nda_ml_sim.py:108` 加性 1/(2γ) 噪声底）、`amp_limit`
  （`_equalizer.py:5` 固定 thresh=3.0）、`decide`（`_a4_switch_common768_30seed.py:106`
  含 1/(2·gamma_lin)）是 scale-DEPENDENT。复现：g=2.0@13dB OLD 链 selected_errors 偏差 +44/+62、
  selector choice da→nda；corrected 链 q/g 精确恢复 g=1 参考（mismatch=0/0）。旧 Phase-0 G3
  float-bypass 门**只在 g=1 测过**。
- **H2 CONTROL**：`CausalRMSAGC.update`（`_p07_adapters.py:182`）`g_next=clamp(target/rms(q_past))`
  **漏乘 g_current**。正确增量形式 `g_next=clip(g_current·target/rms(q_past),...)`。两形式常数输入
  定点不同（CURRENT √(target/r0) vs CORRECTED target/r0）。
- **H3 LIFECYCLE**：`_p07_runner.py:101-103` 每 window 独立 seed 独立 gg_block，经验 lag-1/2/5/10
  ACF = −0.04/+0.003/−0.06/−0.08 ≈ 0，与时间相关 ρ 矛盾。

V071 10/10 ACCEPT 漏审：只查 consistency（g=1 float-bypass、raw→aggregate），未查物理正确性
（命中 sim-preflight rules/mve-validation.md "consistency≠correctness"）。

## 修复实现（新建 p07r_* 文件，旧文件不动）

- `p07r_adapters.py`：`quantize_iq_gainaware` 返回 receiver-input = q/g（scale 恢复）；
  corrected incremental AGC（CausalRMSAGC/AttackReleaseAGC/LogDomainAGC，update 收 q/g 故
  rms 直接是 input scale）；四路分解原语（scale_only/clip_only/quant_only/full_adc）；
  3 候选（CensoredMoment/UpperQuantile/TwoRangePGA）。
- `p07r_trajectory.py`：shared stateful AR(1) GG（`_gg_time._gamma_ar1_exact`），
  ρ=exp(-window_dt/τ_c)，τ_c=1/(2π·f_G)，所有方法共享同一 trajectory（TL-13）。
- `p07r_runner.py` / `p07r_batch_run.py`：cell evaluator + MP batch。
- `p07r_unit_verify.py`（5 unit gates 全 PASS）、`p07r_verify.py`（V072 PART2 10/10）、
  `p07r_adjudicate.py`（终态裁决）。

## fresh-seed 重跑（dev 300-309，与 campaign 历史零重叠）

Phase A（450 cells = 3 fG × 3 scene × 5 SNR × 10 seed × 3 W × 9 gain，ρ 0.99/0.97/0.70）：

| ρ (f_G) | W6 best regret | W8 best regret | W10 best regret | deployable 问题? |
|---|---|---|---|---|
| 0.99 (30Hz)  | +0.256 (6 cell) | **+0.035** (0) | **+0.016** (1) | 否 |
| 0.97 (100Hz) | +0.270 (8 cell) | **+0.042** (0) | **+0.025** (0) | 否 |
| 0.70 (1000Hz)| +0.259 (9 cell) | **+0.067** (2) | **+0.045** (1) | 否 |

deployable 位宽 W8/W10 dev-best fixed-gain g=0.5 regret **+0.03~+0.07 dB ≪ MDE=0.15**，
全 rho deployable_problem=False。旧 P07 "+0.91 dB" 完全是 H1 SCALE artifact。

四路分解（W=8, g=1.0）：scale_only=0.0000（H1 修复验证）/ quant_only=0.0000（宽 rail 无 clip）/
clip_only=+2.03~+2.51 dB / full_adc≈clip_only。W8 gain 扫描：g=0.5 clip 2.2% regret +0.048dB；
g≥1.0 clip>30% regret>+2.3dB。**折中真实单调但单侧：静态低增益即解决，无方法空间**。

## 终态 verdict

**`PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION`**（D046 §VII 终态 A）。counts_as_valid_package=True，
**campaign accepted_valid 恢复 6→7**。Phase B/C 不运行（Phase A 门未过=问题不存在，同 P04/P06
gate 顺序）。F 族关闭（静态低增益即解决，无方法空间）。

## 独立 verifier V072 PART 2（10/10 ACCEPT）

沿调用链查物理正确性（不止 consistency）：W1 q/g 数学 / W2 下游 scale（V071 漏审项）/ W3 AGC 递推 /
W4 trajectory lifecycle（ACF 非零匹配 ρ）/ W5 四路分解隔离 / W6 信息边界 AST / W7 fresh seed 隔离 /
W8 raw→aggregate / W9 verdict 唯一 / W10 frozen 文件未改。全 PASS。
（W6 一处 false positive：CausalRMSAGC 增量 blend 参数原名 `alpha` 与信道真值 `alpha` 撞名，
已重命名 `blend` 消除歧义；非信息泄漏。）

## 治理纠偏

- D046 取代 D045 科学有效性部分（入口裁决部分仍 active）。
- V072 PART 1+2 取代 V071 科学层结论；V071 保留标"合同一致性通过但物理正确性漏审"。
- 旧 P07 artifacts 加 `INVALIDATED_BY_P07R.md` 保留不删。
- topic-index control block：epoch 73，accepted_valid 7/10，current=P08（准备不运行），
  F 族关闭，新增 forbidden `F_AGC_ADC_DYNAMIC_RANGE_FAMILY_REOPEN`。

## 产物

- 脚本：`p07r_{adapters,trajectory,runner,batch_run,unit_verify,verify,adjudicate,reproduce_rootcauses}.py`
- artifacts：`results/p07r_agc_adc_repair/`（p07r_prefail_evidence / p07r_unit_verify /
  p07r_phaseA_dev / p07r_fourway_decomp / p07r_terminal_verdict / p07r_verifier_result .json）
- 治理：D046 / V072-PART1+2 / topic-index control block epoch 73 / INVALIDATED_BY_P07R.md
- 无 push、无 protected owner/formal/Skill/thesis framework 改动、frozen 文件未改。
