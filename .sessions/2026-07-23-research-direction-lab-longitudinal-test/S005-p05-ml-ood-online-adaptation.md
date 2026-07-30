# [S005] P05 ML polarization equalizer OOD safe online adaptation 端到端执行 + mid-calibration

> 2026-07-30 | CAMPAIGN_EXPLORATION_DISPATCH (D039 campaign P05, mid-calibration 包) | 状态: closed (CP034/V069)

## 目标

执行 10-package campaign 的 Package 05（mid-calibration 包）。binding decision 撤回 P05-D（FEC/旋转模糊，无真实 codec/threshold eval 非 FEC/TX-bit rotation resolver privileged/pilot resolver 旧线已裁决）与 P05-E（window/complexity，重复 B1/NDA 比 VV 复杂旧担忧不成立/selector 非主计算量/P03 已覆盖定点轴），指定新族 = `D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION`（对象 = ButterflyCNN 双偏振 ML equalizer，**非** NDA-ML CPR selector）。一轮内完成 Phase 0 入口纠偏 → fresh problem gate → 条件式在线适配 factory → 独立验证 → 主控接收 → 第 5 包内部校准，不在校准或问题验证后停下。

## 记录

### Phase 0：身份门 CLOSED（p05_phase0_identity.json）

无磁盘 checkpoint；frozen-ML = `ButterflyCNNEqualizer2x2(n_tap=11)` MSE 监督确定性复现（P0.1 state_hash byte-identical `03e91429dfed74c6`）；corrected StandardCMA2x2 = prompt019 Godard-with-z（P0.2 byte-identical）。provenance = 当前 params.py strong=(4.2,1.4)（D036 已记 1.5/0.8→4.2/1.4 drift，用当前真值保可复现）。in-dist anchor 坐实 D022 修正后不变量 9（ML swap fixed≈0.5、standard-CMA no-swap fixed≈0）。

### Phase A：问题成立（PRIMARY=fixed-label BER，swap-visible）

两 cell（anchor N5M/fg30/20dB + provenance-OOD N5M/fg100/20dB，**不提高 SOP/f_G**）：fixed-label ML−CMA = +0.4990 / +0.4981，CI_low>0，wins=3/3，cma_div_frac=0（CMA 不共同退化）。四混淆分离全通过。**关键**：PI-BER（swap-blind，不变量 10）下 diff≈0；fixed-label（swap-visible）下 diff≈0.5 稳定——这是首次包内 metric-signature 修正（PRIMARY 从 PI-BER 改 fixed-label，D018 + 不变量 10 强制）。

### Phase B：standard-CMA-continuation 恢复 → PROBLEM_RESOLVED

三 comparator（同预算/prefix-only/receiver-visible）：standard-CMA-cont recovered=True 两 cell（mean fixed-BER 0.00018/0.00117 ≪ MDE=0.05）；DD-LMS（~0.45，slicer 在 swap 喂错标签）与 periodic-pilot（~0.499，D032 weak 化身，坐实 D032 KILL）均未恢复。→ **`PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`**。Phase C 不运行。

### 包内确定性修复（3 次，全披露，V069 复核）

1. metric-signature（PI-BER→fixed-label，不变量 10/D018 强制）
2. dtype（complex128→complex64，纯类型）
3. recovered 判据方向（对齐 binding decision「已恢复问题」）

### mid-calibration（第 5 包内部校准，不停线）

- **accepted packages 序列**：P01 NO_SIGNAL / P02 RESOLVED_BY_REGION_RETUNING / P03 RESOLVED_BY_UNIFORM_PRECISION / P04 PROBLEM_ABSENT_ON_CONTINUOUS_GG / **P05 RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER**。
- **已覆盖机制族（4）**：A CPR 选择器鲁棒性（关闭，P01+P02）/ B 定点资源协同（P03）/ C 连续 GG OOD 选择器鲁棒性（P04）/ **D ML polarization equalizer OOD safe online adaptation（P05）**。
- **method signal 数 = 0**：5 包全 honest negative（问题不存在/被常规解决）。但 P05 是首个**换对象**包——前 4 包全在 DA/NDA CPR 选择器，P05 换到 ButterflyCNN ML equalizer，机制距离显著扩大。
- **偏航评估**：P05 验证了"换对象仍 honest negative"——campaign 不是在旧 selector 周围打转（P05 对象不同），但仍 0 signal。趋势：每个新失效条件要么 sub-MDE 要么被常规 comparator 解决。**campaign 5/10 已耗一半预算仍 0 signal，但族覆盖健康（4 族、机制距离递增）**。
- **可写入 thesis 资产**：P05 强化 Ch3/Ch4 双口径警示（ML swap vs standard-CMA no-swap，contract H2/D023 适用边界）；D032 C1 KILL 独立佐证；ML identity freeze + 三阶段门控框架可复用。
- **P06 为什么与前五包机制不同**：P06 需第 5 个机制族（前 4 族 A/B/C/D 已占 4）。候选 = E 信息复杂度边界（窗口长度 vs 估计方差、低复杂度降级），或 D 族第 2 包（连续≤2 允许）。建议 E 以扩大族覆盖至 5（满足 D039 §4 "至少 5 机制族"在 P06 达成）。

### 独立验证

V069 **ACCEPT**（10/10 + 方法身份非混淆全 PASS；raw→aggregate relErr=0；gate 逻辑/预算公平/Phase-C 抑制/verdict 唯一性源码级验证；3 修复全明显非科学变更）。

### 治理更新

D043 / V069 / CP034 写入；topic-index control block 升 epoch 68→69、accepted_valid 4→5、current P05→P06、families_started 追加 D、rolling_queue 追加 P05；mission-log 追加 CP034；新增 S005、worker-log step-032；P06 入口文件准备（不运行）。

## 决策引用

- D043：P05 ML OOD online adaptation → PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER（新建）
- V069：P05 独立验收 10/10 + 非混淆 ACCEPT（新建）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D039 campaign 授权范围内第 5 个有效包 + mid-calibration，problem-first 三阶段门控；binding decision 撤回 P05-D/E 是裁决要求；3 次包内确定性修复已披露；无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施）。

## 后续

- campaign 5/10，仍 0 active carrier，claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。
- P06 需第 5 机制族（建议 E 信息复杂度边界）或 D 族第 2 包（连续≤2）。本轮准备 P06 入口（不运行）。
- D 族（ML equalizer OOD online adaptation）连续=1 未达上限；若 P06 选 D 第 2 包需注入新失效条件（FR-23），但 P05 已证 standard-CMA 解决 swap，D 第 2 包的 ML-specific deployable action 空间窄——**建议 P06 选 E 以扩族覆盖至 5**。
