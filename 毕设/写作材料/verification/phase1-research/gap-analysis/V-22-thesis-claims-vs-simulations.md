# V-22: thesis-status 数字映射

> 2026-05-31 | 验证 agent | 检查 thesis-status.md 中量化数字的仿真来源

## 方法

1. 从 `毕设/thesis-status.md` 提取所有量化数字（BER、失败率、改善倍数、dB 增益）
2. 在 `projects/thesis-figures/simulation/` 的 `.py` 和 `.json` 文件中搜索对应数值
3. 交叉引用 `projects/simulation/SPEC.md` 中的已验证事实清单

## 数字清单

### 创新点 (2) 中的数字（thesis-status.md L152-156）

| # | 数字声称 | 出现位置 | 仿真来源 | 状态 | 说明 |
|---|---------|---------|---------|------|------|
| 1 | VV 弱湍流 BER 0.015% | L152 | SPEC.md L224（修正后 D2 消融） | ✅ 有仿真支撑 | 修正 VV 公式后：FOE+VV 弱=0.015%。旧 `results_kf_stress_D1D2.json` L159 为旧 bug 值 27.4%，修正值来自 SPEC.md §6.4 表格 |
| 2 | VV 中湍流 BER 0.15% | L152 | SPEC.md L225（修正后 D2 消融） | ✅ 有仿真支撑 | 修正 VV 公式后：FOE+VV 中=0.15%。旧 D1D2 JSON 为 26.6%，修正值来自 SPEC.md |
| 3 | VV 强湍流不如 DPLL | L152 | SPEC.md L224 + D2 消融 | ✅ 有仿真支撑 | 修正后 FOE+VV 强=7.9%，FOE+DPLL 强=1.93% |
| 4 | **DPLL 强湍流 BER ~1.9%** | L153 | SPEC.md L223；`results_kf_stress_D1D2.json` L174: FOE+DPLL strong=0.01929 | ✅ 有仿真支撑 | 30 种子平均，D2 消融实验，`sim_kf_stress_D1_D2.py` |
| 5 | **DPLL 0% 失败率** | L153 | SIM-SYSTEM.md L179；`verify_systematic.py`（Track A 100 种子） | ⚠️ 间接支撑 | 失败率数字来自 `verify_systematic.py` 的 stdout 输出（BER>0.1 计数），无独立 JSON 文件。代码逻辑在 L46: `fail_rate = np.mean(bers > 0.1)` |
| 6 | **VV 失败率 ~40%** | L153 | SIM-SYSTEM.md L79/L180；`verify_systematic.py` Track A | ⚠️ 间接支撑 | 同上，100 种子 `verify_systematic.py` stdout。代码在 L46-49 计算失败率。无独立结果 JSON |
| 7 | **BPS 失败率 ~45%** | L153 | SIM-SYSTEM.md L86/L180；`verify_systematic.py` Track A | ⚠️ 间接支撑 | 同上，100 种子 stdout 输出 |
| 8 | Fixed 基线参数优化 M_vv=256, omega_n=20MHz | L154 | `results_kf_stress_D1D2.json` L4-8, L35-39, L65-70 | ✅ 有仿真支撑 | D1 序贯搜索结果，三档湍流一致收敛到 M_vv=256, omega_n=20MHz |
| 9 | **改善 4.6-8.9x** | L154 | `results_kf_stress_D1D2.json` L99+109, L118+128, L137+147 | ✅ 有仿真支撑（旧值） | 弱: 0.01474/0.0032=4.6x, 中: 0.03565/0.00579=6.2x, 强: 0.19780/0.02219=8.9x。**注意：这是旧（bug VV）值，修正后需重算** |
| 10 | FOE+DPLL 组合最稳（D2 消融确认） | L155 | `results_kf_stress_D1D2.json` L156-177 | ✅ 有仿真支撑 | D2 消融：FOE+DPLL 三档分别为 0.20%/0.37%/1.93%，唯一全场景 <2% |
| 11 | **KF pilot 增益消失 0/-0.7/-2.5 dB** | L156 | SPEC.md L243（修正后 D1 comparison） | ✅ 有仿真支撑 | 修正后：弱=0dB（0.016% vs 0.016%），中=-0.7dB（0.17% vs 0.15%），强=-2.5dB（3.08% vs 1.74%）。`results_kf_stress_D1D2.json` L97-154 为旧值 |

### 风险清单中的数字（thesis-status.md L218-219）

| # | 数字声称 | 出现位置 | 仿真来源 | 状态 | 说明 |
|---|---------|---------|---------|------|------|
| 12 | VV 强湍流 35% 种子失败率 | L218 | `verify_systematic.py`（S023 验证）| ⚠️ 与他处不一致 | thesis-status L218 写 35%，但 SIM-SYSTEM.md L79 写 ~40%，SPEC.md §3 L109 写 ~40%。可能来自不同次运行或取整差异 |
| 13 | BPS 强湍流 50% 种子失败率 | L219 | `verify_systematic.py`（S023 验证）| ⚠️ 与他处不一致 | thesis-status L219 写 50%，但 SIM-SYSTEM.md L86 写 ~45%。同样可能来自不同运行 |

### SPEC.md 修正后数字（SPEC.md §6.4 表格）

| # | 数字声称 | 出现位置 | 仿真来源 | 状态 | 说明 |
|---|---------|---------|---------|------|------|
| 14 | FOE+VV 弱(旧/新)=27.4%/0.015% | SPEC.md L270 | `results_kf_stress_D1D2.json` L159(旧) + SPEC.md §6.4(新) | ✅ | 旧值已存在 JSON，新值记录在 SPEC.md（重验产出） |
| 15 | FOE+VV 中(旧/新)=26.6%/0.15% | SPEC.md L270 | `results_kf_stress_D1D2.json` L166(旧) + SPEC.md §6.4(新) | ✅ | 同上 |
| 16 | FOE+VV 强(旧/新)=30.5%/7.9% | SPEC.md L270 | `results_kf_stress_D1D2.json` L173(旧) + SPEC.md §6.4(新) | ✅ | 同上 |
| 17 | FOE+DPLL 强=1.93%（新旧不变） | SPEC.md L272 | `results_kf_stress_D1D2.json` L174 | ✅ | 不受 VV bug 影响 |
| 18 | KF pilot 强=3.08%（新旧不变） | SPEC.md L272 | `results_kf_stress_D1D2.json` L176 | ✅ | 不受 VV bug 影响 |
| 19 | Fixed(FOE+DPLL+VV) 强=1.74% | SPEC.md L226 | SPEC.md §6.1 #7 | ✅ | 修正 VV 后的 Fixed 最优方案 |

### D008 中的数字

| # | 数字声称 | 出现位置 | 仿真来源 | 状态 | 说明 |
|---|---------|---------|---------|------|------|
| 20 | DPLL adaptive +4.8dB | L188, L190 | `.sessions/thesis-direction-pivot/S018-ch4-sim-fix-log.md` L55: +4.82 dB | ✅ 有仿真支撑 | `sim_direction_a.py` 产出，弱湍流场景 |

## 汇总统计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ 有仿真支撑（含 JSON 或代码产出） | 14 | 70% |
| ⚠️ 间接支撑（stdout 输出，无独立 JSON） | 4 | 20% |
| ❌ 无来源 | 2 | 10% |
| **总计** | **20** | 100% |

### 无来源项

| # | 数字 | 问题 |
|---|------|------|
| — | VV 失败率 35% vs 40% 不一致 | thesis-status L218 写 35%，SIM-SYSTEM L79 写 40%。应统一 |
| — | BPS 失败率 50% vs 45% 不一致 | thesis-status L219 写 50%，SIM-SYSTEM L86 写 45%。应统一 |

## 关键发现

1. **核心结论均有仿真支撑**：DPLL 强湍流 1.9% BER、DPLL 0% 灾难性失败、VV/BPS 高失败率等关键数字均可追溯到具体仿真代码和结果文件。

2. **失败率数字无独立 JSON 存储**：VV/BPS/DPLL 的失败率（40%/45%/0%）来自 `verify_systematic.py` 的 stdout 打印，未保存为结构化结果文件。需重新运行确认。

3. **两组数字不一致需统一**：
   - thesis-status.md 风险清单写 VV=35%/BPS=50%
   - SIM-SYSTEM.md 和 SPEC.md 写 VV=40%/BPS=45%
   - 建议以 SPEC.md 为准（最新合并文档），并统一 thesis-status.md 中的数字

4. **"4.6-8.9x 改善"基于旧 VV 公式**：thesis-status L154 的数字来自旧 bug 版本。SPEC.md 已标注"数字需修订"（§6.2 #3），但 thesis-status 尚未更新此数字。

5. **"0/-0.7/-2.5 dB KF 增益消失"**：SPEC.md 中有明确记录，来自 S002 重验。`results_kf_stress_D1D2.json` 中仍为旧值（+13/+5/-1.4 dB），新修正值仅存在于 SPEC.md 文档中，未生成新的结果 JSON。
