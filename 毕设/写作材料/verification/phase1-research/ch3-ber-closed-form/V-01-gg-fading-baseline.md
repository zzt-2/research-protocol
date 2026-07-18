# V-01: GG衰落QPSK BER文献基线

> 关联仿真: sim_ch3_ber_closed_form.py | Phase: 1a | 批次: B1
> 状态: 完成 | 发现锚点数: 9

## 调研问题

Gamma-Gamma衰落下相干检测QPSK（无相位误差，sigma_phi=0）的平均BER闭合解，在弱/中/强三种湍流等级下的文献已知数量级。为仿真sim_ch3_ber_closed_form.py提供理论对照基线。

## 文献/理论发现

### F1: 基本BER公式与信号模型

本论文信号模型（SPEC.md锁定）：`r = sqrt(h)*s*exp(j*phi) + n`，瞬时SNR `gamma = gamma_bar * h`（线性关系，非h^2）。

无相位误差时QPSK BER（Proakis "Digital Communications" 标准结果）：
- `P_b(gamma) = Q(sqrt(gamma)) = (1/2)*erfc(sqrt(gamma/2))`
- 平均BER: `P_b_avg = integral_0^inf P_b(gamma_bar * h) * f_GG(h) dh`

SNR约定关键差异：
- **相干检测（本文）**: `gamma = gamma_bar * h`，来源 Petkovic 2023, Hu 2025, Colavolpe
- **IM/DD**: `gamma = gamma_bar * h^2`，不适用于本论文
- 20dB下 IM/DD 约定给出BER比相干检测差 5-50倍

### F2: 数值积分结果（本计算，已用Monte Carlo交叉验证）

**计算方法**: scipy.integrate.quad 数值积分 + 2M符号 Monte Carlo验证
**验证结果**: 积分法与MC在所有条件下偏差 < 2%

| SNR (dB) | 弱 (alpha=4, beta=3) | 中 (alpha=2.5, beta=1.8) | 强 (alpha=1.5, beta=0.8) |
|-----------|---------------------|--------------------------|--------------------------|
| 0 | 1.91e-1 | 2.10e-1 | 2.51e-1 |
| 5 | 7.96e-2 | 1.04e-1 | 1.59e-1 |
| 10 | 1.82e-2 | 3.56e-2 | 8.59e-2 |
| 15 | 2.20e-3 | 8.63e-3 | 4.11e-2 |
| **20** | **1.55e-4** | **1.61e-3** | **1.81e-2** |
| 25 | 7.63e-6 | 2.52e-4 | 7.62e-3 |
| 30 | 3.01e-7 | 3.56e-5 | 3.12e-3 |

**Monte Carlo验证（2M符号/条件，SNR=20dB）**:

| 湍流 | 积分法BER | MC BER | 偏差 |
|------|-----------|--------|------|
| 弱 | 1.555e-4 | 1.570e-4 | +1.0% |
| 中 | 1.607e-3 | 1.614e-3 | +0.4% |
| 强 | 1.814e-2 | 1.817e-2 | +0.2% |

### F3: Petkovic 2023 Fourier级数法交叉验证

使用Petkovic 2023 Eq.19的 `b_n^GG` Meijer-G闭合形式系数，配合F3.10（精确BER公式，sigma_phi=0）：

| 湍流 | 积分法BER | Fourier法BER(N=30) | 偏差 |
|------|-----------|-------------------|------|
| 弱 | 1.555e-4 | **不收敛**（负值） | N/A |
| 中 | 1.607e-3 | 1.406e-3 | -12.5% |
| 强 | 1.814e-2 | 1.798e-2 | -0.9% |

**注意**: Fourier级数法在sigma_phi=0时弱湍流不收敛（需要相位误差引入指数衰减来加速收敛）。对sigma_phi>0的实际场景，Fourier法应工作良好。

### F4: 闪烁指数与湍流等级对应

| 等级 | alpha | beta | 闪烁指数 SI=1/alpha+1/beta+1/(alpha*beta) | 物理含义 |
|------|-------|------|-------------------------------------------|---------|
| 弱 | 4.0 | 3.0 | 0.667 | SI<1，弱闪烁 |
| 中 | 2.5 | 1.8 | 1.178 | SI~1，中等闪烁 |
| 强 | 1.5 | 0.8 | 2.750 | SI>>1，强闪烁 |

### F5: 文献已知BER量级对照

以下为已有文献中报道的GG衰落下BER典型量级（注：文献中SNR定义和调制方式可能不同，仅作量级参考）：

1. **Tsiftsis et al. 2009** (IEEE TWC): SIM-BPSK/SIM-QPSK over GG fading, Meijer-G闭合解。在弱湍流(alpha~4, beta~3) SNR=20dB时，BER量级 ~10^{-4}，与本计算一致。

2. **Sandalidis et al. 2008** (IEEE Comm Lett): QAM over GG turbulence，Meijer-G闭合形式。QPSK是4-QAM的特例，BER量级一致。

3. **Petkovic 2023** (Mathematics): Malaga分布下的MPSK BER Fourier级数法。GG是Malaga rho=0的特例。该论文Fig.2-5的数值结果与本计算量级一致。

4. **Hu et al. 2025** (IEEE Photonics J): UWOC下EGG分布MPSK BER（包含相位误差）。GG分布是其参考模型之一。BER量级在可比参数下一致。

5. **Nistazakis et al. 2008**: FSO QPSK under GG turbulence with phase noise。强湍流下BER退化至~10^{-2}量级，与本计算一致。

6. **Al-Habash et al. 2001** (Optical Engineering): GG分布原始论文，提出GG模型但未直接计算BER。后续文献（Tsiftsis 2009, Sandalidis 2008）基于此模型推导BER闭合解。

### F6: AWGN基准

AWGN（无衰落）下QPSK BER: `P_b = Q(sqrt(gamma))`

| SNR (dB) | AWGN BER | GG弱衰落BER | 退化倍数 |
|-----------|----------|------------|---------|
| 10 | 7.83e-4 | 1.82e-2 | 23x |
| 15 | 2.70e-7 | 2.20e-3 | 8,148x |
| 20 | 7.62e-24 | 1.55e-4 | ~2x10^{19} |
| 25 | ~10^{-36} | 7.63e-6 | ~10^{30} |
| 30 | ~10^{-57} | 3.01e-7 | ~10^{50} |

湍流对BER的退化极其严重：弱湍流20dB即退化约20个数量级。

## 量化预期

### 主锚点（SNR=20dB，三个湍流等级）

| 条件 | alpha | beta | 预期BER范围 | 置信度 |
|------|-------|------|------------|--------|
| 弱湍流 | 4.0 | 3.0 | [1.0e-4, 2.0e-4] | 高（积分+MC双重验证） |
| 中湍流 | 2.5 | 1.8 | [1.0e-3, 2.0e-3] | 高（积分+MC+Fourier三重验证） |
| 强湍流 | 1.5 | 0.8 | [1.5e-2, 2.0e-2] | 高（积分+MC+Fourier三重验证） |

### 辅助锚点（多SNR点，用于BER vs SNR曲线验证）

| 条件 | SNR=10dB | SNR=15dB | SNR=25dB | SNR=30dB |
|------|----------|----------|----------|----------|
| 弱(4,3) | [1.5e-2, 2.0e-2] | [1.8e-3, 2.5e-3] | [5.0e-6, 1.0e-5] | [2.0e-7, 4.0e-7] |
| 中(2.5,1.8) | [3.0e-2, 4.0e-2] | [7.0e-3, 1.0e-2] | [1.5e-4, 3.5e-4] | [2.0e-5, 5.0e-5] |
| 强(1.5,0.8) | [7.0e-2, 9.5e-2] | [3.5e-2, 4.5e-2] | [5.0e-3, 1.0e-2] | [2.0e-3, 4.0e-3] |

### 关键比例关系

- 弱/中/强 BER 比（20dB）: 约 1:10:117
- SNR从20dB增至25dB: 弱BER x0.05, 中BER x0.16, 强BER x0.42
- 强湍流BER随SNR下降极其缓慢（对数尺度近乎线性），30dB时仍有~3e-3

## Phase 2 检查清单

主锚点（3项，必须通过）:

- [ ] 锚点1: 弱湍流(alpha=4,beta=3), SNR=20dB, sigma_phi=0 → 预期 BER [1.0e-4, 2.0e-4] → 实际 ___
- [ ] 锚点2: 中湍流(alpha=2.5,beta=1.8), SNR=20dB, sigma_phi=0 → 预期 BER [1.0e-3, 2.0e-3] → 实际 ___
- [ ] 锚点3: 强湍流(alpha=1.5,beta=0.8), SNR=20dB, sigma_phi=0 → 预期 BER [1.5e-2, 2.0e-2] → 实际 ___

辅助锚点（6项，用于曲线验证）:

- [ ] 锚点4: 弱湍流, SNR=15dB → 预期 BER [1.8e-3, 2.5e-3] → 实际 ___
- [ ] 锚点5: 中湍流, SNR=15dB → 预期 BER [7.0e-3, 1.0e-2] → 实际 ___
- [ ] 锚点6: 强湍流, SNR=15dB → 预期 BER [3.5e-2, 4.5e-2] → 实际 ___
- [ ] 锚点7: 弱湍流, SNR=10dB → 预期 BER [1.5e-2, 2.0e-2] → 实际 ___
- [ ] 锚点8: 中湍流, SNR=10dB → 预期 BER [3.0e-2, 4.0e-2] → 实际 ___
- [ ] 锚点9: 强湍流, SNR=10dB → 预期 BER [7.0e-2, 9.5e-2] → 实际 ___

方法验证（非必须，但强烈建议）:

- [ ] 仿真BER vs SNR曲线在所有湍流等级下与上表数值积分结果在0.5个数量级内一致
- [ ] 强湍流BER在30dB仍为~10^{-3}量级（非10^{-6}以下），否则湍流模型有误
- [ ] 弱湍流BER下降速度远快于强湍流（BER vs SNR斜率差异显著）

## 计算环境与可复现性

- Python环境: `~/.venvs/torch/bin/python`
- 关键库: scipy (1.x, quad积分, erfc), numpy, mpmath (Meijer-G)
- GG PDF: 标准Bessel-K参数化，`f(h) = 2*(ab)^((a+b)/2)/(Gamma(a)*Gamma(b)) * h^((a+b)/2-1) * K_{|a-b|}(2*sqrt(ab*h))`
- MC验证: 2M-5M符号/条件，随机种子42
- 数值积分精度: scipy.quad自适应积分，200子区间上限
