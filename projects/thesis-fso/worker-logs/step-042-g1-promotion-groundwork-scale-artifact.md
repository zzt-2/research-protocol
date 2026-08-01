# step-042: G1 promotion groundwork 一次性重开 — 终态 G1_SIGNAL_INVALID_SCALE_ARTIFACT + P11 降级

> 2026-08-01 | 阶段：G1_PROMOTION_GROUNDWORK（用户授权一次性重开 + P11 纠偏） | 状态：DONE — scale artifact 终态，诚实停止于 GW Step 1 前
> 关联：D057 / V083 / CP048；用户执行指令 13 节计划（voice.md 2026-08-01）
> worktree: D:/code/study/research-protocol/.worktrees/rdl-method-production-v2 @ f13d489

## 目标

在同一对话中完成一次有边界的 G1 promotion workline：纠正 P11 + 对 G1 补齐语义审计/直接竞品/真实传统 comparator + 重走 Groundwork Step 1-3/3.5/4a，仅在全部 Go 后跑一次多切片 confirmation。**必须遵守 Groundwork 硬门，若 Step 3/3.5/4a 失败诚实停止，不得先跑实验再补文献。** plan §99 明文 stop condition：若 G1 只是 post-CMA 输出缩放且收益完全来自固定阈值 detector 尺度敏感，立即判 `G1_SIGNAL_INVALID_SCALE_ARTIFACT`，不进入文献包装或实验。

## 记录

### 1. 启动恢复与 scope change（plan §一）

读取纵向专题 topic-index / mission-log / D039/D041/D053-D056 + G1 harvest + G1 原始代码/raw rows + master-state GW Progress + stages/groundwork.md + gw-read/gw-supplement/gw-feasibility + thesis-lessons 速查 + research-direction-lab/session-governance/sim-preflight 规范。

D057 scope-change 登记（decisions.md）：
- 用户授权一次性 G1 promotion groundwork 重开（推翻 D041/D039"不得第二个 G1 promotion 包"一条）
- D041 旧证据 EVIDENCE_INCOMPLETE 判断继续有效
- 其他禁止轴（CB1 collapse family / NDA_ML_BODY_REOPEN / Pilot-Jones / FOE-residual / A/E/F/G/H_BPS 族 / 所有 forbidden axis）全部不变
- foreground control → G1_PROMOTION_GROUNDWORK；先只允许 GROUNDWORK_CLOSURE/COMPETITOR_CLOSURE/COMPARATOR_BUILD，Step 4a Go 后才允许 SCIENTIFIC_EXPERIMENT
- 纠偏 + Groundwork 不计科学包

### 2. 恢复 G1 真实身份（plan §二）— 语义审计

**不信任 "safe-gated normalization" 名字联想**，沿 caller→callee 独立语义审计（fresh-context 子 agent + 主线程源码复核）：

**实现位置**（`projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/`）：
- 主脚本：`src/run_g1_confirm.py`
- gate+归一化函数：`src/methods.py:158-198`（`gated_scalar_freeze`/`gated_scalar_apply`）
- CMA 调用：`baseline-atlas/cb1_cell_runner.py`（`standard_cma_godard_with_z`）
- 判决器：`projects/simulation/common/_modulation.py:84-91`（`hard_decision` 16QAM）

**11 项问答（逐项 file:line + 精确公式）**：

1. **gate 输入** = CMA **输出**的 128-symbol 校准前缀（`run_g1_confirm.py:173-174` `zpx,zpy = base["zX"][es:cal], base["zY"][es:cal]`）。非 raw RX，非 CMA tap。
2. **gate 时序** = 每个 (cell,seed) realization 冻结一次（`run_g1_confirm.py:214` `gated_scalar_freeze`）。无 per-symbol/per-window 循环。
3. **prefix-only**（`methods.py:165` pooled = concat of prefix slices），不读 history/suffix/whole eval window。因果边界干净。
4. **归一化作用点** = CMA 输出后缀 → 检测器输入（`methods.py:191-198` `return ax*z_suffix_x, ay*z_suffix_y`）。CMA 在 gate 计算前已跑完（`run_g1_confirm.py:170-171`）。
5. **精确公式** = `a_p = sqrt(E_ABS2 / trimmean(|z_prefix_p|², 0.1))`，`z'_p = a_p · z_suffix_p`（`methods.py:182-183,198`）。per-pol 正确 sqrt 缩放，非功率线性比。
6. **阈值** = collapse_threshold=0.6, spread_threshold=0.1，冻结常量（`run_g1_confirm.py:97-98`），T020 dev-set 调谐后冻结，fresh seeds 不再调。
7. **粒度** = per-polarization × per-block。
8. **是否改 CMA tap trajectory？ NO。** CMA 跑完后返回 `base["zX"]/zY`，gate（`:214`）和 apply（`:256`）只读 zX/zY，CMA 权重 wxx/wyy/wxy/wyx 从未被 gate 读写。**零 CMA 反馈。**
9. **是否仅改输出尺度？ YES。** apply 是 per-pol 单复标量乘（或恒等）。无 per-sample/非线性。smoke test `test_g1_identity_branch_bit_identical_to_baseline`（`tests/test_g1_semantic_smoke.py:79-90`）断言恒等分支 bit-identical。
10. **下游检测器 scale-sensitive？ YES 强烈。** `hard_decision` 16QAM slicer（`_modulation.py:84-91`）：`s = z*sqrt(10)`；`di = clip(round((real(s)+3)/2)*2-3, -3, 3)`；**判决边界固定在 0, ±2**（de-norm 轴），**无输入 AGC / 无功率归一化**。contract 自承（`contract.yaml:71`）：evaluator "rotation-only, **cannot undo magnitude scale**"。
11. **信息泄漏？ NONE 进 gate/normalize 路径。** TX truth 只进 `oracle_affine_bound_apply`（KILL-only 工具，独立运行）和离线 label（`_offline_label_pair`，gate 后才算，存 receipt 不回流）。无未来 block 访问。

**真实 data-flow 表**：

| feature | gate | action | CMA state change | output | metric |
|---|---|---|---|---|---|
| `mean_abs2`, `spread` (cv of \|z\|) on CMA prefix pooled both pols | `mean_abs2≥0.6 AND spread≥0.1`→identity; else→scale | `a_p=sqrt(1/trimmean(|z_pref_p|²,0.1))`; `z'_p=a_p·z_suffix_p` | **none** (CMA converged, gate never touches taps) | per-pol complex scalar × suffix | fixed-threshold 16QAM slicer (boundaries 0, ±2; **scale-sensitive**) → PI-SER |

**SCALE-ARTIFACT 终态裁决**：`G1_SIGNAL_INVALID_SCALE_ARTIFACT`

G1 = post-CMA per-polarization per-block output 复标量乘，零 CMA 反馈；下游 fixed-threshold slicer 无输入 AGC，判决边界不随输入功率归一化——纯幅度 rescale 改变哪些样本跨过 grid。**收益完全来自 fixed-threshold detector 的尺度敏感性，不是 receiver action 增量。** 代码库自己的 smoke test `test_correct_sqrt_restores_amplitude_power_ratio_fails`（`tests:52-74`）证明整个机制：干净 scale collapse `z=c·s` 上正确 sqrt scalar 把 SER 推到 0 纯靠 rescale 回固定 grid。真实部署接收机不会用无 AGC 的 fixed-threshold slicer——它会先把星座自动归一到单位平均功率再 slice，无需"门控归一化方法"。

### 3. 历史信号重新审计（plan §三）— fresh-context 子 agent

从 1120 raw rows（8 method × 7 cell × 20 seed，`artifacts/raw-rows.csv` + `prefix-receipt.csv`）独立重算：
- collapse ΔPI-SER (G1−baseline, 20 collapse pairs) = **−0.5598**（seed-cluster CI [−0.69, −0.41]，12 help/0 hurt）
- healthy worst degradation (G1, 29 pairs) = **0.0000**（28/29 bit-identical identity，1 false-activation helped −0.0313）
- gate 触发率 collapse **19/20** vs healthy **1/29**
- G1 vs Q15 nonlinear map ablation = **−0.0355**（CI [−0.047, −0.024]）
- 旧 GATE6 FAIL（CI_lo=0.50）只在 3 种 defensible bootstrap 定义之一下成立；另两种 cluster-resample/pair-bootstrap 给 CI_lo≈0.88-0.89

**关键解读**：数字"强"恰好因为是 scale artifact——strong recovery 来自 rescale 固定 grid，strong safety 来自 identity 分支不 rescale。这与代码审计的 scale-artifact 终态一致而非矛盾。

### 4-9. Groundwork Step 1-3/3.5/4a — 跳过（plan §99 stop condition）

plan §99 明文："如果G1只是post-CMA输出缩放，而且收益完全来自固定阈值detector尺度敏感，立即判：`G1_SIGNAL_INVALID_SCALE_ARTIFACT`。不进入文献包装或实验。"

语义审计已证明这正是事实。**不进 GW Step 2-3 文献闭包，不实现 comparator B0-B5，不建 freeze receipt，不跑 held-out confirmation。** Groundwork 诚实停止于 Step 1 前：
- GW Step 1 问题定义要求 M-C-A 中 A 是 genuine state-dependent switching（问题 C）
- 代码审计证明 G1 只可能是问题 A（detector scale calibration，平凡常规问题）或问题 B（CMA update normalization，但 G1 不触 tap）的弱化身，**不是问题 C**
- 问题 A 是部署接收机用 AGC 解决的平凡问题（PI-SER evaluator 的不变性缺陷是测量 artifact，非部署问题），不构成研究空白
- **没有过四判据的 Q#**，GW Step 1 不成立，gw-feasibility A0 §0 前置门控直接拦

### 10-12. METHOD_SIGNAL / 晋升 / 独立审查 — 不触发（终态非 signal）

终态 `G1_SIGNAL_INVALID_SCALE_ARTIFACT` 非 METHOD_SIGNAL，不产方法卡/不晋升/不建 active carrier。独立验证 V083 由 fresh-context 子 agent（G1 code audit + G1 raw-rows re-audit）+ 主线程 P11 raw 复算共同完成。

### P11 纠偏（plan §一，同时执行）

基于 `p11_phaseA_test_raw.json` 192 rows（4 cell × 8 seed × 6 pilot_frac）逐 cell 复算：

| cell (SNR) | B0 full-label Adam | B2 batch complex LS | B4 blind CMA (zero pilot) |
|---|---|---|---|
| weak_fg30_9dB | **0.0** (perfect) | 4.83e-6 (B2 worse) | 3.82e-5 |
| strong_fg30_11dB | 2.14e-4 | 1.6e-4 (B2 better) | 3.02e-4 |
| moderate_fg100_13dB | 2.35e-4 | 2.3e-4 (≈tie) | 2.83e-4 |
| strong_fg1000_15dB | 1.09e-3 | 8.7e-4 (B2 better) | 9.94e-4 (**B4 < B0**) |

撤回 D056 三项过度措辞：
1. **"B2 严格优于 B0"**：weak_fg30_9dB cell B0 达 BER=0，B2=4.83e-6，B2 在该 cell 劣于 B0。pool 数字 3.10e-4 vs 3.86e-4 掩盖 per-cell 反转。
2. **"跨 SNR"**：4 cell 全部集中在 9-15dB（无 17/20/25dB cell）。
3. **"监督开销不必要 / LS 唯一解决者"**：B4 zero-pilot blind CMA 在 strong_fg1000_15dB cell（BER 9.94e-4）优于 B0 full-label Adam（1.09e-3）。"zero-pilot blind CMA 与监督方法近似持平"是更诚实描述。LS 并非唯一解决者。

保留：chronology 闭合（Commit 1 `4d9c374`）+ linear Butterfly FIR 身份（`common/_ml_equalizer.py:104`）+ 9-15dB raw 数据（局部诊断资产）。

P11 新分类：**`PARTIAL_LOCAL_9to15DB_BASELINE_ASSET`**（用户原话"20dB"是概括，以 raw SNR 范围为准）。`accepted_valid_packages` 8→7；`remaining_valid_packages`=3。不做 P11-R。

## 决策引用

- D057：scope-change G1 promotion groundwork 一次性重开 + P11 降级 + G1_SIGNAL_INVALID_SCALE_ARTIFACT 终态（新建）
- V083：G1 语义审计 11/11 + P11 raw 复算（新建）
- D056：P11 PROBLEM_RESOLVED_BY_COMPLEX_LS（被 D057 取代计数与措辞；chronology + linear FIR 身份保留有效）
- D041：G1 FORMAL CLOSED / EVIDENCE_INCOMPLETE（继续有效，升级为 INVALID_SCALE_ARTIFACT）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。用户授权一次性 G1 promotion groundwork 重开 + P11 纠偏，plan §99 明文允许 scale artifact 终态停止。
- **未恢复 CB1 family / 未做第二三个 G1 repair / 未绕 GW 跑旧 G1 / 未改正式论文结论 / 未升级历史局部结果 / 未重开其他 forbidden axis**。
- Groundwork 诚实停止（Step 1 前，A0 §0 拦），未跳步、未先跑实验。
- 纠偏 + Groundwork 工作不计科学包。

## 后续

- G1 promotion 一次性授权已用尽；G1 safe-gated-normalization scale artifact 加入 forbidden axis（禁换名重开）。
- P11 降级 PARTIAL_LOCAL_9to15DB_BASELINE_ASSET；不做 P11-R。
- campaign accepted_valid=7/10，remaining_valid=3，未终止，0 active carrier。
- **下一合法动作**：用户决定 D039 campaign 后续——(1) P12 继续探索 remaining 3 有效包预算；(2) 论文范围决策（G1 scale-artifact 诚实结论 + 局部负面 harvest + linear FIR 监督开销部分证据[9-15dB only]）；(3) 收尾审计。
- 无 sprint/无 held-out seed/无 method card/无 commit 之外产物。不 push。
