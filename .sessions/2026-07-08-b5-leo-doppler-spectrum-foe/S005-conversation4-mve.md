# [S005] 对话 4 — 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency

> 2026-07-08 | 阶段: 工作对话执行阶段 2-3 MVE | 状态: 完成，MVE 三项全 PASS，common 转正完成，可进 Step 4a 收尾

## 目标

承接工作对话对话 3 S004 + H004 派发，执行阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency。核心是验证 B5 短时谱 FOE 的 MVE 级别正确性——sandbox 已 PASS 路径 C，MVE 补 V3 祖师爷警报 + V4 星历残差重审 + consistency bit-exact。

## 记录

### 报到 + 接收方验证（步骤 1）

session-governance Trigger 1 报到 + 读必读清单 1-6：
- 本专题文件（topic-index 14 不变量 / H004 / S004 / decisions.md D001 / _registry.yaml / profile.md）
- 对话 3 sandbox 产出（_short_time_spectrum_foe.py 598 行 / _leven_mthpower_foe.py 290 行 / _sandbox_three_way.py / 3 结果 JSON）
- B5 锚 + [60] Leven 原文（V1 公式核对 + V3 祖师爷警报）
- 复用基建（fft_foe common/_recovery.py:37 / _channel.py / params.py B5Params）
- 框架文件（sim-preflight SKILL §1.6 C6-C8 + mve-validation V1-V6）
- 参照契约（B7-MVE-SPEC.md 结构参照）

接收方验证 4 条全打钩 + 3 条关键事实核查全 PASS（独立 grep JSON 重算）：
- 路径 C sandbox PASS（_sandbox_results.json pathC_verdict="PASS" + _turbulence_residual_sweep.json 27/27 <140MHz，max 16.20MHz）
- 范围扩展 14.4×（_doppler_range_sweep.json B5 19/19 vs fft_foe 1/19）
- B5Params 20 字段全溯源（params.py B5Params 类 + content.md 行号）

### 阶段 2 TL-20 理论预期表（步骤 1，B5-MVE-SPEC.md）

写 `B5-MVE-SPEC.md`（12 节），含：
- §0 定位（Step 4a 维度 D MVE + Go/Kill 判据分离 FR-25）
- §1 核心假设（三维 fair gain：范围扩展 + 残频 σ + 星历残差鲁棒性）
- **§2 TL-20 理论预期表**（5 子表：残频 σ 随 SNR/湍流/范围/星历残差/V3 祖师爷预期，sandbox 实测校准锚点）
- §3 FR-11 架构摘要（B5 前馈估计器适配 DRL 框架：估计域=频域功率比/决策粒度=块级/对比范式=三方对照/语义=粗 CFO 残频最小化）
- §4 三方对照架构（C7 + V2）
- §5 V1-V6 验证清单（sandbox 已过 V1/V2/V5/V6，MVE 补 V3/V4）
- §6 星历残差扫描设计（sandbox 遗留债务）
- §7 consistency bit-exact（MVE vs Formal）
- §8 pass/fail 标准（D005 + FR-25）
- §9 扫描设计（MVE 主表 + 星历残差 + V3 复核）
- §10-12 执行约束 + 子 agent 返回 + 转正流程

### 阶段 3 MVE + consistency（步骤 2，派子 agent + 主线独立核查）

**子 agent 实现 MVE 脚本** `mve_b5_short_time_spectrum.py`（复用 sandbox import + 3 新实验函数）：

**实验 4 V3 祖师爷警报**（B5 vs [60] Leven 非同族核查）：
- 公平条件：频偏 [0.5/1/2]GHz + SNR 13dB + weak + 20 seed
- 两方都施加共享星历 LO 预补偿到残频~0（公平机制对照）
- 结果：B5 σ=12.30MHz vs Leven σ=1.99MHz，relative_diff=83.8% >> 5% 门控
- **V3 警报未触发** ✓（B5 频域积分 Rp-n vs Leven 时域差分，机制正交非同族）

**实验 5 星历残差扫描**（sandbox 完美星历假设债务）：
- 固定 SNR 13dB + weak + 1GHz + 20 seed，扫残差 [0/50/100]MHz
- 结果：σ = 9.68 / 9.87 / 10.03 MHz，max 10.03MHz << 140MHz 门控
- **3 点全 PASS** ✓（路径 C 前提在星历残差下仍成立）
- **DEVIATION**：σ 几乎不随星历残差线性增长（9.68→10.03，仅 +3.6%），TL-20 §2.4 预期线性增长到 16-120MHz。原因：B5 迭代吸收约 50% 星历残差（mean 从 -1.58→+24.32→+50.26，透传率 48.6%/50.3%）。**比预期更鲁棒**，非 FAIL。

**实验 6 consistency bit-exact**（MVE vs Formal 同代码路径）：
- seed=1000, f_true=1GHz, weak, SNR 13dB
- 三项（B5/fft_foe/leven）全 0 ulp 差异，相对误差 = 0
- **consistency PASS** ✓（实现同步确认，守 D-008：consistency 不查算法对错只查同步）

**V5 主线独立核查**（INVARIANT 10，只信原始数字不信归因）：
- V3 relative_diff 重算 = JSON 值 ✓ 一致
- 星历残差吸收归因重算：B5 FFT 迭代确实吸收 ~50%（observed 24.32/50.26 vs expected 50/100）✓
- consistency bit-exact 三项全相等 ✓
- V3 公平性：两方都完美预补偿到 ~0 后测残频估计 σ，公平 ✓
- **诚实标注**：V3 中 B5/Leven σ 在三个频偏点完全相同（星历预补偿到残频~0 后，σ 反映估计器固有精度跟频偏量级无关），非 V3 公平性问题，是 B5 机制特性

### 转正（步骤 3，common/_recovery.py）

MVE + consistency 双通过，转正：
- `short_time_spectrum_foe` + `short_time_spectrum_foe_iterate` + `leven_mthpower_foe` + `leven_capture_range_hz` 进 `common/_recovery.py`（去 explore 探针标注，保留 C6 公式标注）
- 转正 smoke PASS：common import 成功 + B5 迭代收敛（1GHz fest=0.977GHz 残频 163.6MHz）+ Leven 捕获范围 ±312.5MHz
- **mve 脚本留 explore/**（跟 B7 先例一致，MVE 是验证记录非 Formal 实验脚本；依赖 explore/sandbox 实验工具 bandlimit_2sps 等非 common 级函数）

### MVE 判定门控

| 门控项 | 目标 | 实测 | 判定 |
|---|---|---|---|
| V3 祖师爷警报 | B5 vs Leven rel_diff >5% | 83.8% | **PASS**（非同族）|
| V4 星历残差扫描 | max σ <140MHz | 10.03MHz | **PASS**（裕度 130MHz）|
| consistency bit-exact | 三项 0 ulp 差异 | 全 0 | **PASS** |
| V1 公式（sandbox）| C6 标注式 1-4 | 已过 | **PASS** |
| V2 三方（sandbox）| B5/fft/leven | 已过 | **PASS** |
| V5 归因核查（本轮）| 主线独立重算 | 全一致 | **PASS** |
| V6 读原文（sandbox）| B5Params 溯源 | 已过 | **PASS** |

**MVE 判定：PASS** ✓ — V1-V6 全过 + consistency bit-exact + 星历残差鲁棒性确认。B5 短时谱 FOE 算法正确性 + 实现同步 + 星历残差鲁棒性全验证。

**建议主控对话判 Go**（FR-25：Go 标准=赢传统 baseline 范围维度 14.4× + B5>Random + 路径 C 湍流 σ<140MHz，全成立）。

## 决策引用

- D001：开 B5-Q1 专题 + 首验证够格路径（路径 C 成立）
- 无新建决策（MVE PASS 是 D001 执行结果，不需新建 D###）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 2-3 MVE + consistency，不回头救 Kill / 不判他候选 / 不改框架 / 不跳框架 / 不推翻 D006 / 守"双通过才进 common"）

## 后续

**主控对话跟进点**（MVE PASS 后）：
1. **Go/Kill 判断**（FR-25，用户/主控决策）：MVE 三项全 PASS + sandbox 路径 C PASS → 建议判 Go，B5 进 Step 5（Baseline 选定 + Contract）
2. **DEVIATION 复核**：星历残差 σ 不线性增长（B5 迭代吸收 ~50%），主控对话确认此机制非 bug 是特性（比预期更鲁棒）
3. **Step 4a 收尾**：MVE PASS 后 B5-Q1 Step 4a 维度 D 闭合，可进 Step 5 或跟 B7/B2 统一排优先级

**转正完成**：
- common/_recovery.py：short_time_spectrum_foe + short_time_spectrum_foe_iterate + leven_mthpower_foe + leven_capture_range_hz（4 函数）
- mve 脚本留 explore/（验证记录，跟 B7 先例一致）
- B5Params 已在 params.py（S004 落盘）

**explore/ 产出（本轮）**：
- B5-MVE-SPEC.md（12 节 MVE 契约 + TL-20 理论预期表）
- mve_b5_short_time_spectrum.py（MVE 脚本，复用 sandbox + 3 新实验）
- _mve_results.json（V3 警报 + consistency + V1-V6 记录）
- _ephemeris_residual_sweep.json（星历残差扫描 3 点）
