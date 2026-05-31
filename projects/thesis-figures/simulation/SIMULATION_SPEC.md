# 湍流 FSO 载波同步仿真体系规范

> ⚠️ **已废弃** — 合并入 `projects/simulation/SPEC.md`。本文件不再更新。

---

## 1. 信号模型（已锁定，TL-01 验证）

**相干检测 QPSK 星地激光通信系统。**

```
接收信号:  r[k] = √h[k] · s[k] · exp(jφ[k]) + n[k]
瞬时 SNR:  γ = γ̄ · h    （h 是归一化辐照度，GG 分布）
MMSE 均衡: rx_eq = rx · √h / (h + 1/γ̄)
```

**关键约定**（TL-01 来源，曾因 IM/DD vs 相干搞混导致 3 个对话作废）:
- 相干检测: γ ∝ h（不是 h²）
- 信号: tx · √h（不是 tx · h）
- 文献确认: Petkovic 2023, Hu 2025, Colavolpe

---

## 2. 系统参数（已锁定）

```python
R_SYM = 2.5e9        # 符号率 2.5 Gsps
T_S = 400e-12         # 符号周期 400 ps
LASER_LW = 10e3       # 激光线宽 10 kHz
F_RESIDUAL = 1e6      # 残余频偏 1 MHz（FOE 粗补偿后）
DOPPLER_HIGH = 150e6  # 多普勒变化率 150 MHz/s（LEO 场景）
BLOCK = 100           # 信道块大小（块内 h 恒定）
```

### 湍流参数（Gamma-Gamma 分布）

| 等级 | α | β | 物理场景 |
|------|---|---|---------|
| weak | 4.0 | 3.0 | 夜间/高仰角 |
| moderate | 2.5 | 1.8 | 白天/中仰角 |
| strong | 1.5 | 0.8 | 低仰角/恶劣天气 |

### KF Q 矩阵参数

```python
Q_TURB_PARAMS = {
    'weak':     {'sigma2_turb': 1e-6,  'kappa': 1.56e-6},
    'moderate': {'sigma2_turb': 1e-4,  'kappa': 9.80e-5},
    'strong':   {'sigma2_turb': 1e-3,  'kappa': 3.79e-4},
}
# Q[1,1] = (50kHz)²·T_S² — 压力测试证明此参数无影响（B1），可忽略
```

### Fixed 基线最优参数（D1 压力测试结果）

```python
# 默认参数（旧，不公平）:
FIXED_CFG_DEFAULT = {'N_fft': 1024, 'M_vv': 64, 'omega_n': 8e6}

# 最优参数（D1 序贯搜索结果，必须用这个）:
FIXED_CFG_OPTIMAL = {
    'weak':     {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6},
    'moderate': {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6},
    'strong':   {'N_fft': 2048, 'M_vv': 256, 'omega_n': 20e6},
}
```

---

## 3. 仿真文件索引

### 公共基础设施

| 文件 | 用途 | 状态 | 备注 |
|------|------|------|------|
| `sim_kf_stress_common.py` | **公共模块**: 信号生成、KF、基线、共享信道(TL-13修复) | 活跃 | 所有压力测试脚本 import 此文件 |

### 原始仿真文件（逐步迭代产物）

| 文件 | 用途 | 状态 | 已知问题 |
|------|------|------|---------|
| `sim_direction_a.py` | 原始自适应方案（三公式） | **废弃** | 自适应在物理上无效(TL-03/06/07) |
| `sim_ch4_kf_carrier_sync.py` | 最早 KF 仿真 | **废弃** | P 矩阵跨块重置 bug(TL-09) |
| `sim_ch4_kf_perblock_h.py` | DD 逐块 h 估计 | **废弃** | DD 在深衰落正向反馈崩溃(TL-10) |
| `sim_ch4_kf_verification.py` | 6 组公平性对照 | 参考值 | TL-13 违规（各自生成信道） |
| `sim_ch4_kf_pilot_h.py` | 导频辅助 KF（主文件） | **有保留价值** | TL-13 违规；公平性实验部分可用 |
| `sim_ch4_systematic_analysis.py` | VV/BPS/DPLL 系统性分析 | 参考值 | 用了旧信号模型参数 |

### 压力测试文件（S024 产出，结论可靠）

| 文件 | 测试维度 | 关键结论 |
|------|---------|---------|
| `sim_kf_stress_A1_A2_A3.py` | A1共享信道 + A2 100种子 + A3 Wilcoxon | 增益真实(+11/+12/+7dB)，p<2e-18 |
| `sim_kf_stress_A4_A5.py` | A4 SNR扫描 + A5 序列长度 | 无真实floor，Ns≥5000稳定 |
| `sim_kf_stress_B1_B2.py` | B1 Q矩阵 + B2 R矩阵 | Q[1,1]哑参数，**R矩阵导频h无价值(FAIL)** |
| `sim_kf_stress_B3_B4_B5.py` | B3 P初始化 + B4 导频密度 + B5 放置 | P不敏感，5%接近最优，前置式最优 |
| `sim_kf_stress_C1_C2_C3.py` | C1多普勒 + C2线宽 + C3频偏 | 物理参数鲁棒，增益稳定 |
| `sim_kf_stress_C4_C5.py` | C4块大小 + C5深衰落 | **BS=100非最优(FAIL)**，深衰落+3dB(PASS) |
| `sim_kf_stress_D1_D2.py` | D1基线优化 + D2消融 | **强湍流KF输给最优Fixed**，VV有害，DPLL是核心 |
| `sim_kf_stress_D3_D4_D5.py` | D3标准PA-KF + D4 EKF/UKF + D5极端 | **湍流感知被证伪(FAIL)**，线性KF最优 |

### 结果文件

所有 `results_kf_stress_*.json` 和 `fig_kf_stress_*.png` 在同目录下。完整报告见 `.sessions/thesis-direction-pivot/S024-kf-stress-test.md`。

---

## 4. 载波恢复方法状态

| 方法 | 原理 | 湍流下表现 | 推荐度 |
|------|------|-----------|--------|
| **FOE (FFT-FOE)** | 4th-power FFT 频偏估计 | 所有场景有效（粗补偿基础） | ★★★ 必选 |
| **DPLL** | 数字锁相环 | **核心贡献者**，单独达到 0.2-1.9% BER | ★★★ 强湍流首选 |
| **V&V CPR** | 4th-power 滑动平均相位恢复 | **所有湍流下有害**: BER 从 10% 恶化到 27-30% | ★ **禁止使用** |
| **KF oracle-h** | KF + 真实 h (上界) | 性能最好但不可实现 | 仅作参考 |
| **KF frame-h** | KF + 帧级 h 中位数 | 中/强湍流下**有害**: 强湍流 25.8% vs FOE+DPLL 1.93% | ★ 不推荐 |
| **KF pilot-h** | KF + 导频逐块 h 估计 | 弱/中 +5~13dB；**强湍流输给 FOE+DPLL** | ★★ 弱/中可用 |
| **标准 PA-KF** | KF + 固定 R（无湍流感知） | **强湍流优于"湍流感知"KF** 2.3dB | ★★ 弱/中可用 |

### 方法选择指南（压力测试结论）

```
弱湍流:   FOE + DPLL + KF_pilot (或标准PA-KF)  → BER ~0.02%
中等湍流: FOE + DPLL + KF_pilot (或标准PA-KF)  → BER ~0.2%
强湍流:   FOE + DPLL (不需要 KF)                → BER ~1.9%
```

---

## 5. 已验证事实清单

以下结论经过压力测试严格验证，可直接引用：

1. **TL-13 修复影响有限**: 共享信道 vs 各自生成信道，增益差异 ±1.6 dB 以内（A1）
2. **Fixed 基线默认参数严重次优**: M_vv=64→256, omega_n=8→20MHz 改善 4.6-8.9x（D1）
3. **V&V CPR 在湍流 FSO 下有害**: 4th-power 相位展开被块衰落相位跳变破坏（D2 消融）
4. **DPLL 是载波恢复的核心贡献者**: FOE+DPLL 单独即达 0.2-1.9% BER（D2 消融）
5. **"湍流感知 R 矩阵"无价值**: 4 种 R 计算 BER 差异 <13%，标准 PA-KF 反而更好（B2+D3）
6. **Q[1,1] 是哑参数**: 50x 范围内 BER 完全相同（B1）
7. **P 矩阵初始化不影响稳态**: KF 在导频处快速收敛（B3）
8. **5% 导频开销 near-optimal**: net BER 与最优值之比 <1.5x（B4）
9. **前置式导频放置最优**: 均匀式在中等湍流下差 6.1x（B5）
10. **BLOCK=100 非最优**: BS=20 在强湍流下 net BER 好 1.74x（C4）
11. **深衰落块 KF 改善显著**: h<0.1 块改善 4.6-13 dB（C5）
12. **KF 对频偏/线宽鲁棒**: 极端条件 (20MHz频偏, 10MHz线宽) 不崩溃（C1-C3, D5）
13. **线性 KF 对此模型最优**: EKF=KF，UKF 更差（D4）

---

## 6. 已知限制与未验证项

### 已知限制
- KF pilot 在 SNR<5dB + 强湍流下崩溃 (BER>10%)（D5）
- KF pilot 在强湍流下不如 FOE+DPLL（D1）
- 当前所有仿真假设 MMSE 均衡用 oracle h（公平性验证表明 20dB 下影响可忽略）
- 所有仿真用 QPSK，未验证其他调制格式

### 未验证项
- BPS（Blind Phase Search）作为对比基线
- 导频图案对信道时变速度的匹配（仅测了前置/均匀/中心）
- 非 20dB SNR 下的 R 矩阵灵敏度（B2 仅在 20dB 测试）
- 信道编码（FEC）下的误码率表现

---

## 7. 新对话启动检查清单

开始任何仿真工作前，确认以下事项：

- [ ] 信号模型是相干检测: r = √h·s·exp(jφ) + n, γ = γ̄·h
- [ ] 使用 `sim_kf_stress_common.py` 作为基础设施（不要从旧文件复制）
- [ ] Fixed 基线参数使用 `FIXED_CFG_OPTIMAL`（不是默认值）
- [ ] 不使用 V&V CPR（湍流下有害）
- [ ] 所有对比方案共用信道实现（TL-13）
- [ ] 基线方案已做参数优化（TL-14）
- [ ] Python 环境: `~/.venvs/torch/bin/python`
- [ ] 工作目录: `projects/thesis-figures/simulation/`

---

## 8. 相关文档

| 文档 | 位置 | 用途 |
|------|------|------|
| 教训积累 | `thesis-lessons.md` | 19 条教训，防止重复踩坑 |
| 压力测试报告 | `.sessions/thesis-direction-pivot/S024-kf-stress-test.md` | 20 维度完整结果 |
| 压力测试计划 | `.sessions/thesis-direction-pivot/PROMPT-011-kf-stress-test.md` | 原始计划 |
| KF 开发链 | `.sessions/thesis-direction-pivot/S022-ch4-direction-chain.md` | KF 方案完整演变 |
| 公共模块 | `projects/thesis-figures/simulation/sim_kf_stress_common.py` | 信号生成+KF+基线 |
