# P06 入口选择（NOT RUN — 本轮仅准备，不执行）

> 2026-07-30 | campaign 5/10 已完成（P05），P06 入口准备 | 状态: ENTRY-PREP-NOT-RUN
> 来源: S005（P05 mid-calibration 结论）+ D043/V069/CP034 + D039 campaign §4

## 背景（campaign 状态）

- accepted_valid=5/10；families_started = [A, B, C, D]（4 族）；同族连续 = D=1。
- P01-P05 verdict 全 honest negative（NO_SIGNAL / RESOLVED_REGION / RESOLVED_UNIFORM / ABSENT / RESOLVED_BY_CONVENTIONAL）：0 method signal。
- **D039 §4 强制**："至少 5 机制族"。当前 4 族，**P06 必须开第 5 族**（或 D 族第 2 包连续≤2，但不增族数，无法满足"≥5 族"）。
- binding decision（P05）："P06 必须再选一个不同机制族，使前六包至少覆盖 5 个家族。"

## P06 候选（按机制距离 + 族覆盖优先级）

### 推荐：E 信息复杂度边界（开第 5 族，P06 达成"≥5 族"）

**问题假设（待 Phase A 冻结验证）**：已完成 DA/NDA CPR 选择器（或 ButterflyCNN ML equalizer）的 **估计方差 vs 观测窗口长度** 权衡——固定窗口长度在短窗口/高动态下产生估计方差 floor，是否存在窗口长度自适应的 deployable regret。

- 机制族 = E_INFORMATION_COMPLEXITY_BOUNDARY（窗口长度 vs Cramér-Rao/估计方差下界、低复杂度降级路径）。与 A/B/C/D 机制正交（A=SNR 失配、B=定点、C=分布形状 OOD、D=在线适配；E=观测信息量/复杂度权衡）。
- 对象：可选 DA/NDA CPR 选择器（stage-1/stage-2 窗口）或 ButterflyCNN（n_tap/window）。两者均有"窗口长度"自由度。
- provenance：选择器 `_a4_switch_common768_30seed.py` stage-1 CV 窗口 + stage-2 噪声扣除窗口；ML `common/_ml_equalizer.py` n_tap/train_frac。
- **不制造问题**：窗口长度扫描须在 provenance 支持范围内，不人为缩短到不可实现。
- comparator：当前冻结窗口长度（P01-P04 用的）作 baseline；低复杂度降级（如块均值/移动平均）作常规 comparator。
- 风险：估计方差 floor 可能是物理 SNR/turbulence 主导非窗口长度（类似 P04 anchor > interior 的非 OOD-specific）；可能 PROBLEM_ABSENT 或 RESOLVED_BY_CONVENTIONAL。
- **预评估**：满足 method-production 四门——(1) 物理自由度存在（窗口长度是真实可调参数）；(2) baseline 失败对齐（短窗口高方差是已知 DSP 权衡）；(3) 命名常规 comparator（固定窗口 + 低复杂度降级）；(4) file:line 证据（选择器窗口 / ML n_tap）。

### 备选：D 族第 2 包（连续≤2 允许，但不增族数，**无法满足 P06 达"≥5 族"**）

- 仅在 E 族 preflight 门1（物理自由度）失败时考虑。
- D 第 2 包需注入新失效条件（FR-23）：P05 已证 standard-CMA 解决 swap，D 第 2 包的 ML-specific deployable action 空间窄（swap 已被常规解决）。**不建议**。

## 入口四门预检（E 族，待下一对话 binding decision 确认）

1. **物理自由度存在**：窗口长度是 CPR 选择器（`_a4_switch_common768_30seed.py` stage-1/stage-2 窗口）与 ButterflyCNN（`_ml_equalizer.py` n_tap）的真实可调参数（file:line 待下一对话核）。
2. **baseline 失败对齐**：短窗口高估计方差是 DSP 已知权衡（Cramér-Rao）；需验证当前冻结窗口在 provenance 短窗口端是否产生 regret。
3. **命名常规 comparator**：固定窗口（当前冻结）+ 低复杂度降级（块均值/移动平均/抽头缩减）—— receiver-visible、task-matched、独立 dev 调谐。
4. **file:line 证据**：待下一对话冻结。

## 不运行（本轮纪律）

本轮（P05 端到端 + mid-calibration + 治理更新 + 单次 commit）**不运行 P06**。下一对话由用户中转 P06 执行指令（binding decision），届时先过入口四门 preflight，通过后端到端跑 Phase 0→A→B→C。

## 候选扫描备注

- 4 族已覆盖的 mechanism space：A=SNR 失配鲁棒性、B=定点资源协同、C=分布形状 OOD、D=在线适配。E=信息复杂度边界 是下一个机制正交轴。
- 前五包趋势（每新失效条件 sub-MDE 或被常规解决）提示 E 也可能 honest negative，但族覆盖价值独立于 signal——P06 开 E 即使 negative 也满足"≥5 族"的 campaign 结构目标。
- 已排除：P05-D（FEC/旋转模糊）、P05-E（window/complexity 重复 B1）——**注意 E 信息复杂度边界 ≠ P05-E window/complexity**：P05-E 撤回原因是"重复 B1 adaptive phase-window + NDA 比 VV 复杂不成立 + selector 非主计算量 + P03 已覆盖定点"；E 信息复杂度边界是**估计方差 vs 观测窗口的信息论权衡**（不同问题，不重复 B1 phase-window）。下一对话需 binding decision 区分二者。
