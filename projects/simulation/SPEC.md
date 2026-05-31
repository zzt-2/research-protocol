# 湍流 FSO 载波同步仿真规范

> 创建: 2026-05-31 | 最后更新: 2026-05-31
> **本文件是仿真工作的唯一真相源。新对话启动仿真工作前必须先读本文件。**
> 合并自 SIM-SYSTEM.md（Track A）和 SIMULATION_SPEC.md（Track B），修正已知错误。

---

## 1. 信号模型（锁定，不可修改）

### 1.1 物理模型

相干检测 QPSK 星地激光通信系统。

**接收信号**：
```
r[k] = √h[k] · s[k] · exp(jφ[k]) + n[k]
```

- `h[k]`：归一化辐照度（Gamma-Gamma 分布）
- `s[k]`：QPSK 符号，位于 (±1±j)/√2（π/4 旋转星座）
- `φ[k]`：载波相位（多普勒+激光相位噪声+湍流相位）
- `n[k]`：复高斯白噪声，E[|n|²] = 1

**瞬时 SNR**：`γ[k] = γ̄ · h[k]`（线性关系，不是 h²）

### 1.2 文献依据

- γ=γ̄·h 约定：Petkovic 2023, Hu 2025, Colavolpe（相干 FSO 主流）
- γ=γ̄·h² 是 IM/DD 约定，**不适用于本论文**
- 信号模型错误会导致全盘皆错（TL-01）

### 1.3 系统参数

| 参数 | 符号 | 值 | 来源 |
|------|------|-----|------|
| 符号率 | R_SYM | 2.5 Gsps | Zhao 2025 |
| 符号周期 | T_S | 400 ps | 1/R_SYM |
| 载波频率 | f_c | 1550 nm (1.95e14 Hz) | C波段 |
| 激光线宽 | Δν | 10 kHz | 典型值 |
| 多普勒率 | f_dot | 150 MHz/s | LEO 500km |
| 残余频偏 | f_res | 1 MHz | 预补偿后 |
| 信道块大小 | BLOCK | 100 符号 | 相干时间~2-10ms >> 100·T_S |
| 导频开销 | — | 5% (5/100) | 默认值 |

### 1.4 湍流参数（Gamma-Gamma 分布）

| 等级 | α | β | 物理场景 |
|------|---|---|---------|
| 弱 weak | 4.0 | 3.0 | 夜间/高仰角 |
| 中 moderate | 2.5 | 1.8 | 白天/中仰角 |
| 强 strong | 1.5 | 0.8 | 低仰角/恶劣天气 |

### 1.5 QPSK 星座与 π/4 偏移（关键）

QPSK 符号位于：**(±1 ± 1j) / √2**，即 π/4 + kπ/2 (k=0,1,2,3)

**对 4 次方鉴相器的影响**：
- s⁴ = |s|⁴ · exp(j·4·(π/4+kπ/2)) = exp(jπ) · exp(j2kπ) = -1（恒定）
- VV/DPLL 的 4 次方鉴相器输出 = 真实相位 + π/4
- **π/4 偏移是物理特性，不是 bug**
- π/4 偏移 + π/2 模糊无法通过简单减法消除，需 resolve_qpsk 试旋转解决
- `common.py` 的 `vv_cpr` 和 `dpll_track` 保持原始实现（不强制 π/4 修正）

---

## 2. 系统参数（锁定）

```python
R_SYM = 2.5e9        # 符号率 2.5 Gsps
T_S = 400e-12         # 符号周期 400 ps
LASER_LW = 10e3       # 激光线宽 10 kHz
F_RESIDUAL = 1e6      # 残余频偏 1 MHz（FOE 粗补偿后）
DOPPLER_HIGH = 150e6  # 多普勒变化率 150 MHz/s（LEO 场景）
BLOCK = 100           # 信道块大小（块内 h 恒定）
```

### KF Q 矩阵参数

```python
Q_TURB_PARAMS = {
    'weak':     {'sigma2_turb': 1e-6,  'kappa': 1.56e-6},
    'moderate': {'sigma2_turb': 1e-4,  'kappa': 9.80e-5},
    'strong':   {'sigma2_turb': 1e-3,  'kappa': 3.79e-4},
}
```

### Fixed 基线参数

```python
# 默认参数（不公平，仅作对照）:
FIXED_CFG = {'N_fft': 1024, 'M_vv': 64, 'omega_n': 8e6, 'zeta': √2/2}

# 最优参数（D1 序贯搜索结果，必须用这个做公平对比）:
FIXED_CFG_OPTIMAL = {
    'weak':     {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6},
    'moderate': {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6},
    'strong':   {'N_fft': 2048, 'M_vv': 256, 'omega_n': 20e6},
}
```

---

## 3. 载波同步方法

| 方法 | 原理 | π/4 偏移 | 湍流下表现 |
|------|------|---------|-----------|
| **FOE (FFT-FOE)** | 4th-power FFT 频偏估计 | N/A | 所有场景有效（粗补偿基础） |
| **VV (Viterbi-Viterbi)** | 4th-power 滑动窗平均 | 有（已修正） | 强湍流失败率~40% |
| **BPS (Blind Phase Search)** | 候选相位+最小距离 | 无（公式正确处理） | 强湍流失败率~45% |
| **DPLL** | 4th-power 鉴相+二阶环路 | 有（已修正） | 强湍流 0% 灾难性失败 |
| **KF pilot** | 2状态KF+导频辅助h估计 | 无（不做4次方） | 弱/中有效，强湍流不如DPLL |

### 方法选择指南

```
弱湍流:   FOE + DPLL + KF_pilot  → BER ~0.02%
中等湍流: FOE + DPLL + KF_pilot  → BER ~0.2%
强湍流:   FOE + DPLL (不需要 KF)  → BER ~1.9%
```

---

## 4. 评估方法（统一标准）

### 4.1 BER 计算方法

| 方法 | 代码 | 机制 | 适用场景 |
|------|------|------|---------|
| `ber_count` | 直接解调 | sign(real)>0, sign(imag)>0 | KF pilot（不做 4 次方） |
| `resolve_qpsk` | 旋转优化 | 尝试 8 个旋转(0~2π,π/4步)，选 BER 最低 | VV/DPLL/Fixed（4 次方方法） |

### 4.2 为什么 VV/DPLL 必须用 resolve_qpsk

4 次方鉴相器引入**两个问题**：
1. **π/4 恒定偏移**：QPSK 符号在 π/4+kπ/2，s⁴=-1，angle/4 = 真实相位 + π/4
2. **π/2 相位模糊**：angle() 返回 [-π,π]，除以 4 后有 4 个等价解

`resolve_qpsk` 通过尝试 8 个旋转（覆盖 π/2 步进）找到正确解。它**是 oracle**（用 TX bits），但对所有方法一致使用。对 VV/DPLL 而言，它同时也是**必要配套**（4 次方方法的 π/2 模糊必须通过试旋转解决）。

`ber_count` 无法直接用于 VV/DPLL 输出（BER≈25%，相当于随机猜测）。

### 4.3 统一标准

**所有方法统一用 `resolve_qpsk`（oracle，但一致使用，不影响公平性）。** `ber_eval()` 函数提供统一入口：
- `ber_eval(tx_bits, rx, mode='oracle')` — 默认，所有方法适用
- `ber_eval(tx_bits, rx, mode='direct')` — 仅适用于 KF pilot

### 4.4 历史评估方法使用情况（已纠正）

> **错误声称（已证伪）**：之前的 SIM-SYSTEM.md 和 H024 handoff 声称
> "D1/D2 压力测试中 KF pilot 用 ber_count，Fixed 用 resolve_qpsk"。
> **代码验证（2026-05-31）**：`sim_kf_stress_D1_D2.py:95,98` 显示两者都用 resolve_qpsk。
> D1/D2 的评估方法**实际是一致的**，不存在不公平。

| 实验来源 | KF pilot | Fixed/VV/DPLL | 是否一致 |
|---------|----------|---------------|---------|
| S022 Stage 10-11 (sim_ch4_kf_pilot_h.py) | resolve_qpsk | resolve_qpsk | 一致 |
| S023 (sim_ch4_systematic_analysis.py) | — | resolve_qpsk | — |
| S024 D1/D2 (sim_kf_stress_D1_D2.py) | resolve_qpsk | resolve_qpsk | **一致** |
| S024 A-C (sim_kf_stress_A1-C5) | resolve_qpsk | resolve_qpsk | 一致 |

**所有压力测试都用 resolve_qpsk，所有方案被同等对待。D1/D2 结论可靠。**

### 4.5 resolve_qpsk 的影响

resolve_qpsk 使用 TX bits 选最优旋转，在实际系统中不可获得。但它对**所有方法**产生同等影响：
- VV/DPLL：需要 resolve_qpsk 处理 π/2 模糊（必要配套）
- KF pilot：不需要但也不受损（多一次旋转优化是冗余无害的）
- **相对排名不受影响**，绝对 BER 值可能略偏低

---

## 5. 代码文件清单

### 5.1 当前活跃代码（`projects/simulation/`）

| 文件 | 用途 | 状态 |
|------|------|------|
| `common.py` | 公共基础设施（唯一来源） | **活跃** |
| `SPEC.md` | 本文件 | **活跃** |
| `experiments/` | 新实验脚本目录 | **活跃** |
| `results/` | 结果数据 | **活跃** |
| `figures/` | 图表 | **活跃** |
| `archive/README.md` | 旧文件索引 | **活跃** |

### 5.2 旧文件（`projects/thesis-figures/simulation/`，已废弃）

详细索引见 `archive/README.md`。

| 文件 | 用途 | 状态 | 已知问题 |
|------|------|------|---------|
| `sim_kf_stress_common.py` | 旧公共模块 | **已被 common.py 替代** | VV unwrap 公式 |
| `sim_kf_stress_*.py` (8个) | 压力测试 | **参考** | 全用 resolve_qpsk |
| `sim_ch4_systematic_analysis.py` | VV/BPS/DPLL 分析 | **参考** | π/4 被 resolve_qpsk 掩盖 |
| `sim_ch4_kf_pilot_h.py` | 导频辅助 KF | **参考** | 最完整的 KF 实现 |
| `sim_ch4_kf_carrier_sync.py` | 原始 KF | **废弃** | P 矩阵跨块重置 bug(TL-09) |
| `sim_ch4_kf_perblock_h.py` | DD 逐块 h | **废弃** | DD 深衰落崩溃(TL-10) |
| `sim_direction_a.py` | 自适应方案 | **废弃** | 自适应物理上无效(TL-03/06/07) |
| `sim_prototype.py` | 原型验证 | **参考** | 无已知问题 |
| `verify_systematic.py` | 100 种子验证 | **参考** | resolve_qpsk 问题 |

### 5.3 结果文件

所有 `results_*.json` 和 `fig_*.png/pdf` 在旧目录 `projects/thesis-figures/simulation/` 下。完整清单见 `archive/README.md`。

---

## 6. 已验证事实清单

> ⚠️ **2026-05-31 重大修订**：D1/D2 重验发现旧 stress_common.py 的 VV 公式 bug（`unwrap(angle*M)/M`）
> 严重膨胀了 Fixed 基线的 BER，导致 KF 增益数字虚高。以下结论已按修正后 VV 公式更新。
> 详见 `S002-ch4-audit-report.md` §5 "VV 公式修正影响"。

### 6.1 高置信度

**代码级（S002 审计确认）：**
1. **参数完全一致**: 16 个文件核心参数与 SPEC.md 一致，信号模型正确（√h·s）
2. **KF 实现正确**: KF pilot BER 在新旧 common.py 下完全一致（0.0000% 偏差）
3. **resolve_qpsk 对所有方法一致使用**: 不影响相对排名（D1/D2 代码 L95/L98 确认）

**方法性能级（D2 消融，修正 VV 后）：**
4. **DPLL 是强湍流核心**: FOE+DPLL 强湍流 1.93%，优于 FOE+VV（7.9%）和 KF pilot（3.08%）
5. **修正 VV 在弱/中湍流有效**: FOE+VV 弱=0.015%，中=0.15%（旧 bug 版本 27%/27%）
6. **最优 Fixed（FOE+DPLL+VV）与 KF pilot 性能持平**: 弱 0.016% vs 0.016%，中 0.15% vs 0.17%
7. **强湍流 Fixed 优于 KF**: 1.74% vs 3.08%（-2.5 dB）

**KF 内部机制级（不依赖与 Fixed 对比，仍有效）：**
8. **"湍流感知 R 矩阵"无价值**: 4 种 R 计算 BER 差异 <13%，标准 PA-KF 反而更好（B2+D3）
9. **Q[1,1] 是哑参数**: 50x 范围内 BER 完全相同（B1）
10. **P 矩阵初始化不影响稳态**: KF 在导频处快速收敛（B3）
11. **5% 导频开销 near-optimal**: net BER 与最优值之比 <1.5x（B4）
12. **前置式导频放置最优**: 均匀式在中等湍流下差 6.1x（B5）
13. **BLOCK=100 非最优**: BS=20 在强湍流下 net BER 好 1.74x（C4）
14. **KF 对频偏/线宽鲁棒**: 极端条件不崩溃（C1-C3, D5）
15. **线性 KF 对此模型最优**: EKF=KF，UKF 更差（D4）

### 6.2 旧结论状态（VV 修正后需修订）

| 旧结论 | 旧状态 | 新状态 | 说明 |
|--------|--------|--------|------|
| VV 全湍流有害 | "已验证" | ❌ **仅强湍流不如 DPLL** | 旧结论基于 bug VV（27-30%），修正后弱/中湍流 VV 有效 |
| KF 增益 +11/+5/-1.4 dB | "已验证" | ❌ **0/-0.7/-2.5 dB** | 增益来自 bug 拉低 Fixed 基线，非 KF 本身贡献 |
| Fixed 默认参数次优 4.6-8.9x | "已验证" | ⚠️ **数字需修订** | 改善幅度因修正 VV 而缩小 |
| 深衰落块 KF 改善 4.6-13 dB | "已验证" | ⚠️ **对照基线变化** | C5 的对照是 bug Fixed，需用修正 Fixed 重验 |

### 6.3 已证伪

1. ❌ "湍流感知 R 矩阵"是贡献（B2+D3 双重验证）
2. ❌ "导频 h 估计对 R 有价值"（B2）
3. ❌ "KF 全湍流增益"→ 强湍流 KF 输给 Fixed
4. ❌ "D1/D2 评估方法不一致" → 代码验证证实两者都用 resolve_qpsk
5. ❌ "VV 在所有湍流下有害" → 旧结论基于 VV 公式 bug，修正后弱/中湍流 VV 有效
6. ❌ "KF 增益 +11/+5 dB" → 增益来自 Fixed 基线被 VV bug 拉低

### 6.4 VV 公式修正影响记录

**bug 机制**：`sim_kf_stress_common.py` L144 使用 `unwrap(angle(avg)*M)/M`（公式 B），而正确的公式 A 是 `unwrap(angle(avg))/M`（`common.py` L170、`sim_ch4_systematic_analysis.py` L147）。先乘 M 后 unwrap 会扩大相位范围至 [-16π, 16π]，导致 unwrap 产生大量假阳性缠绕修正（数学验证：MSE 恶化最高 28,229 倍）。

**影响范围**：
- stress_common.py + 4 个旧 KF 文件使用公式 B
- common.py + sim_ch4_systematic_analysis.py 使用公式 A
- 所有压力测试（A1-D5）通过 stress_common 导入，受 bug 影响

**修正前后 D2 消融 BER 对比（30 种子平均）**：

| 方案 | 弱(旧/新) | 中(旧/新) | 强(旧/新) |
|------|-----------|-----------|-----------|
| FOE only | 10.9%/10.9% | 10.2%/10.2% | 13.4%/13.4% |
| FOE+VV | **27.4%/0.015%** | **26.6%/0.15%** | **30.5%/7.9%** |
| FOE+DPLL | 0.20%/0.20% | 0.37%/0.37% | 1.93%/1.93% |
| KF pilot | 0.016%/0.016% | 0.17%/0.17% | 3.08%/3.08% |

**结论**：FOE_only、FOE+DPLL、KF 系列不受影响。FOE+VV 受致命影响（弱/中 100-1800x 差异）。Fixed 基线含 VV 因此被连带影响。

---

## 7. 已知限制与未验证项

### 已知限制
- KF pilot 性能与最优 Fixed（FOE+DPLL+VV）持平或略差，无显著性能增益
- KF pilot 在强湍流下不如 FOE+DPLL+VV（3.08% vs 1.74%）
- 当前所有仿真假设 MMSE 均衡用 oracle h（20dB 下影响可忽略）
- 所有仿真用 QPSK，未验证其他调制格式
- 所有结论基于 20dB 单点，未做 SNR 扫描

### 未验证项
- SNR 扫描曲线（BER vs SNR）— 论文必需
- C5 深衰落改善用修正 Fixed 重验
- BPS 作为对比基线
- 信道编码（FEC）下的误码率表现
- resolve_qpsk（oracle）对绝对 BER 值的影响量级

---

## 8. 新对话启动检查清单

开始任何仿真工作前，确认以下事项：

- [ ] 已读本文件（SPEC.md）
- [ ] 信号模型是相干检测: r = √h·s·exp(jφ) + n, γ = γ̄·h
- [ ] 使用 `common.py` 作为基础设施（不从旧文件复制代码）
- [ ] 评估方法默认用 `ber_eval(bits, rx, mode='oracle')`（VV/DPLL 需要；KF pilot 也兼容）
- [ ] Fixed 基线参数使用 `FIXED_CFG_OPTIMAL`（不是默认值）
- [ ] 所有对比方案共用信道实现（TL-13）
- [ ] Python 环境: `~/.venvs/torch/bin/python`
- [ ] 工作目录: `projects/simulation/`

---

## 9. 相关文档

| 文档 | 位置 | 用途 |
|------|------|------|
| 教训积累 | `thesis-lessons.md`（项目根） | 19 条教训，防止重复踩坑 |
| 压力测试报告 | `.sessions/thesis-direction-pivot/S024-kf-stress-test.md` | 20 维度完整结果 |
| 旧代码索引 | `projects/simulation/archive/README.md` | 旧文件状态和可复用部分 |
| KF 开发链 | `.sessions/thesis-direction-pivot/S022-ch4-direction-chain.md` | KF 方案完整演变 |

---

## 10. 变更日志

| 日期 | 变更 |
|------|------|
| 2026-05-31 | 创建。合并 SIM-SYSTEM.md + SIMULATION_SPEC.md。修正 §4.3 评估方法错误声称。 |
| 2026-05-31 | §4 重写：resolve_qpsk 是 oracle（用 TX bits），但对所有方法一致使用不影响公平性；对 VV/DPLL 是必要配套（π/2 模糊）。ber_count 仅适用于 KF pilot。 |
| 2026-05-31 | §6 重大修订：D1/D2 重验发现 VV 公式 bug 严重膨胀旧结论。VV 修正后弱/中湍流有效（非有害）；KF 增益从 +11/+5/-1.4 dB 修正为 0/-0.7/-2.5 dB。新增 §6.4 VV 公式修正影响记录。 |
