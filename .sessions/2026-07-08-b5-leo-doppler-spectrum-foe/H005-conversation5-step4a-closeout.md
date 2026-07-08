# Handoff: 对话 5 — B5-Q1 Step 4a 收尾（MVE PASS，交主控对话判 Go/Kill）

> 来源: S005（工作对话对话 4）| 交接目标: 主控对话判 Go/Kill + Step 4a 收尾
> 文件名: H005-conversation5-step4a-closeout.md
> 日期: 2026-07-08

## 到哪了（状态）

工作对话对话 4 完成阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency，**MVE 三项全 PASS**，common 转正完成。

**MVE 核心结论**：
- **V3 祖师爷警报未触发**：B5 vs [60] Leven 残频 σ 差 83.8%（B5 12.30MHz / Leven 1.99MHz），机制正交（频域积分 Rp-n vs 时域差分），非同族
- **V4 星历残差扫描 PASS**：残差 [0/50/100]MHz，max σ=10.03MHz << 140MHz 门控（裕度 130MHz）。DEVIATION：σ 不线性增长（B5 迭代吸收 ~50% 星历残差），比预期更鲁棒
- **consistency bit-exact PASS**：三项（B5/fft_foe/leven）全 0 ulp 差异

**MVE 产出**（4 文件落盘 explore/b5-leo-doppler-spectrum-foe/）：
1. `B5-MVE-SPEC.md`（12 节 MVE 契约 + TL-20 理论预期表 + FR-11 架构摘要）
2. `mve_b5_short_time_spectrum.py`（MVE 脚本，复用 sandbox + 3 新实验函数）
3. `_mve_results.json`（V3 警报 + consistency + V1-V6 记录）
4. `_ephemeris_residual_sweep.json`（星历残差扫描 3 点）

**common 转正**（MVE + consistency 双通过）：
- `common/_recovery.py` 新增 4 函数：`short_time_spectrum_foe` + `short_time_spectrum_foe_iterate` + `leven_mthpower_foe` + `leven_capture_range_hz`
- 转正 smoke PASS（import 成功 + B5 迭代收敛残频 163.6MHz + Leven 捕获范围 ±312.5MHz）
- mve 脚本留 explore/（跟 B7 先例一致，MVE 是验证记录非 Formal 脚本）

**V5 主线独立核查全 PASS**（INVARIANT 10，只信原始数字不信归因）：
- V3 relative_diff 重算 = JSON 值 ✓
- 星历残差吸收归因重算：B5 FFT 迭代确实吸收 ~50% ✓
- consistency 三项全 0 ulp ✓
- V3 公平性：两方都完美预补偿到 ~0 测 σ，公平 ✓

## 下一步干什么（主控对话 = Go/Kill 判断 + Step 4a 收尾）

> **守 FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline（范围维度 14.4×）/ Kill 标准=V3 警报或 MVE FAIL 或星历残差崩塌。MVE 三项全 PASS → 建议判 Go。

### 主控对话动作 1：Go/Kill 判断

**Go 标准（FR-25，全成立）**：
- ✅ 范围扩展 14.4× ≥10×（FR-15 目标维度，sandbox S004）
- ✅ B5 > Random（FR-14 先验基线，B5 19/19 vs Random 全失败）
- ✅ 路径 C 湍流下残频 σ max 16.20MHz <140MHz（sandbox S004 + MVE 复核）
- ✅ 星历残差扫描 max σ 10.03MHz <140MHz（MVE 新增）
- ✅ V1-V6 全过（V3/V4 本轮补齐）
- ✅ consistency bit-exact PASS

**Kill 标准（无一触发）**：
- ❌ V3 祖师爷警报（未触发，83.8% >5%）
- ❌ 星历残差崩塌（max 10.03MHz << 140MHz）
- ❌ V1 公式不符（C6 标注完整）
- ❌ consistency FAIL（三项 bit-exact）

**建议判定：Go**（B5-Q1 Step 4a 维度 D PASS，进 Step 5 或跟 B7/B2 统一排优先级）。

**DEVIATION 待主控确认**：星历残差 σ 不线性增长（9.68→10.03MHz，仅 +3.6%），因 B5 迭代吸收 ~50% 星历残差（mean 透传率 48.6%/50.3%）。**比预期更鲁棒非 FAIL**，但主控对话应确认此机制理解（V5 已核查非 bug 是 B5 迭代机制特性）。

### 主控对话动作 2：Step 4a 收尾

MVE PASS 后 B5-Q1 Step 4a 维度 D 闭合。选项：
- (A) B5 进 Step 5（Baseline 选定 + Contract），独立推进
- (B) 跟 B7/B2/NDA-ML 统一排优先级（4 候选横向对比，B5 范围优势 vs B7 BER gain vs B2 fade 鲁棒性）
- (C) 先收 B7/B2 MVE 结果再统一判（B7 对话 7 在跑，B2 阶段 1.5 重设计中）

**建议**：跟用户确认走 (A)/(B)/(C)。B5 是范围维度够格（非 dB 增量），跟 B7（0.6dB BER gain）/B2（fade 鲁棒性）机制正交，可作大论文跨章节统一叙事（S003 阶段 0.4 已定）。

## 纪律（和下一步直接相关的约束）

1. **FR-25 Go/Kill 标准分离**：Go=赢传统 baseline 范围维度 / Kill=V3 警报或 MVE FAIL。MVE 全 PASS → Go，不因"不是 dB 增量"转 Kill（INVARIANT 11 范围维度够格）
2. **D005 务实路线**（INVARIANT 2）：会议门槛放宽，范围/绝对指标算够格（BUPT Arria 10 FPGA demo 会议模板）
3. **不回头救 6 次 Kill**（INVARIANT 明确不含）：B5 路径 C 够格不转 Kill
4. **DEVIATION 处理**（TL-20）：星历残差 σ 不线性增长已解算（B5 迭代吸收），非 bug 不需重跑

## 接口变更（代码改动）

**common/_recovery.py 新增**（MVE 转正）：
- `short_time_spectrum_foe(rx, n_fft, n_blocks, alpha, fs, normalize_mode, ephemeris_pred) -> dict`
- `short_time_spectrum_foe_iterate(rx, n_iter, n_fft, n_blocks, alpha, fs, normalize_mode, ephemeris_pred, precise_range_hz) -> dict`
- `leven_mthpower_foe(rx, M, N_sum, fs, normalize_mode) -> dict`
- `leven_capture_range_hz(fs, M) -> float`

**explore/b5-leo-doppler-spectrum-foe/ 新增**（MVE 验证记录）：
- `B5-MVE-SPEC.md`（MVE 契约）
- `mve_b5_short_time_spectrum.py`（MVE 脚本，留 explore 非 experiments）
- `_mve_results.json` + `_ephemeris_residual_sweep.json`

**未改动**：
- `params.py` B5Params（S004 已落盘，20 字段全溯源）
- explore 探针 `_short_time_spectrum_foe.py` / `_leven_mthpower_foe.py` / `_sandbox_three_way.py`（保留作 sandbox 验证记录，common 已有转正版）

## 失败数据附录（如涉及路线失败）

无新增路线失败。MVE 三项全 PASS，无红线警报。

**B5-Q1 唯一 DEVIATION**（非失败）：星历残差 σ 不线性增长（9.68→10.03MHz），因 B5 迭代吸收 ~50% 星历残差。比预期更鲁棒，不影响 Go 判定。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~星历预测完美假设~~ | sandbox 模拟 ephemeris_pred=f_true | **✅ 已解决（MVE）**：星历残差扫描 max σ 10.03MHz << 140MHz | — |
| ~~short_time_spectrum_foe 待转正~~ | explore 验证通过才进 common | **✅ 已解决（本轮）**：common/_recovery.py 转正 | — |
| [60] Leven 范围差异 | 0.4.2 表 ±1.6GHz vs sandbox ±312.5MHz | sandbox 标注（1-sps 限制）| Formal 用 [60] Leven 最优条件重测（若进 Contract）|
| B5 BER 偏高 | B5 是粗 CFO，BER 交后续 DSP | sandbox 标注 BER 0.23-0.37 | Contract 阶段加后续 DSP（VV/BPS）报完整 BER |
| mve 脚本留 explore | MVE 是验证记录非 Formal 脚本 | 本轮决策（跟 B7 先例一致）| 若 Contract 需要 Formal 实验脚本再转 experiments/ |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| sandbox 三方对照 | 范围扩展 ≥10× + 湍流 σ <140MHz | V2+C7 + INVARIANT 11 | ✅ PASS（14.4× + max 16.2MHz）|
| MVE V3 祖师爷警报 | B5 vs Leven rel_diff >5% | V3 (v1.3.0) | ✅ PASS（83.8%）|
| MVE V4 星历残差扫描 | max σ <140MHz | V4 + INVARIANT 11 | ✅ PASS（10.03MHz）|
| MVE consistency | MVE vs Formal bit-exact | sim-preflight | ✅ PASS（三项 0 ulp）|
| MVE V1-V6 | 全过 | v1.3.0 | ✅ PASS（V1/V2/V5/V6 sandbox + V3/V4 本轮）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B5 特殊）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] MVE V3 警报未触发（核查 `_mve_results.json` V3_grandmaster_alarm.alarm_triggered=false + relative_diff=0.838）
  - [ ] 星历残差扫描 PASS（核查 `_ephemeris_residual_sweep.json` all_pass=true + max_sigma_mhz=10.03）
  - [ ] consistency bit-exact PASS（核查 `_mve_results.json` consistency_check.verdict="PASS" + 三项 relative_error=0.0）
- [ ] 已检查 common/_recovery.py 转正（核查 short_time_spectrum_foe/leven_mthpower_foe 存在）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 Kill / 不判他候选 / 不改框架 / 不跳框架 / 不推翻 D006）

## 下一轮

**主控对话**（本轮 H005 交接）：Go/Kill 判断 + Step 4a 收尾
- 判 Go（MVE 三项全 PASS + sandbox 路径 C PASS）
- 确认 DEVIATION（星历残差吸收机制非 bug）
- 决定 Step 5 路径（A 独立推进 / B 跟 B7/B2 统一排优先级 / C 等 B7/B2 MVE 结果）
- 若进 Step 5：Baseline 选定（传统 FFT FOE 主 + [60] Leven 祖师爷）+ Contract（瓶颈诊断 + 参数溯源 + 动作空间）
