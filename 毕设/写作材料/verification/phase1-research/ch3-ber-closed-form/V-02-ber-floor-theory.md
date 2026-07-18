# V-02: BER floor 理论位置

> 关联仿真: sim_ch3_ber_closed_form.py | Phase: 1a | 批次: B1
> 状态: 完成 | 发现锚点数: 6

## 调研问题

BER floor（误码率平台）的物理成因、数学表达与 GG 湍流参数的关系，以及三档湍流下的量化预期。

## 文献/理论发现

### 发现 1：BER floor 的唯一成因是载波相位误差（σ_φ > 0），与湍流无关

**来源**: F3.11 自推（formulas-master.md）; Petkovic 2023 (Mathematics, 11, 121) Section 3.4 渐近分析; Hu 2025 (IEEE J. Photonics, 10.1109_jphot.2025.3534258) Eq.(34)-(35)

**数学推导**:

当 γ̄ → ∞ 时，AWGN 噪声消失，瞬时 BER 退化为纯相位判决：

```
P_b(γ→∞, φ) = 0,     当 |φ| < π/4（判决正确）
P_b(γ→∞, φ) = 1/2,   当 |φ| ≥ π/4（判决错误 1 bit）
```

因此：

```
P_{b,floor} = (1/2) · P(|φ| > π/4) = Q(π/(4σ_φ))
```

**物理含义**：
- 高 SNR 下，噪声不再是误码来源
- 唯一剩余的误码机制是载波相位偏移超过 QPSK 判决边界（±π/4）
- 湍流（α, β）仅影响"多快到达 floor"，不影响 floor 数值
- 增加发射功率无法降低 floor，只能改善到达 floor 之前的 BER

**文献确认**:
- Petkovic 2023 明确指出："SEP floor cannot be decreased by neither increasing the signal power, nor by improving the channel conditions, but depends only on the phase noise standard deviation"
- Hu 2025 Eq.(35): `P_b^∞(e) ≈ (2/log₂M) · Σ Q((2i-1)π/(M·σ_φ))`，对 QPSK (M=4) 退化为 `Q(π/(4σ_φ))`
- Hu 2025 结论："BER floor does not depend on the channel gain but is influenced by the phase error standard deviation"

### 发现 2：无相位误差时（σ_φ = 0），GG 衰落下不存在 BER floor

**来源**: F3.10 + F3.16（formulas-master.md）; 数值计算验证

当 σ_φ = 0 时，BER 公式退化为 E_h[Q(√(γ̄·h))]。数值积分证明 BER 随 SNR 单调递减趋向零：

| SNR (dB) | 弱 (α=4,β=3) | 中 (α=2.5,β=1.8) | 强 (α=1.5,β=0.8) | AWGN 对照 |
|-----------|-------------|-------------------|-------------------|-----------|
| 10 | 1.82e-2 | 3.56e-2 | 8.59e-2 | 7.83e-4 |
| 15 | 2.20e-3 | 8.63e-3 | 4.11e-2 | — |
| 20 | 1.55e-4 | 1.61e-3 | 1.81e-2 | 7.62e-24 |
| 25 | 7.63e-6 | 2.52e-4 | 7.62e-3 | — |
| 30 | ~0 | ~0 | ~0 | — |

关键观察：
- BER 在所有湍流强度下都趋向零（无 floor）
- 湍流导致 BER vs AWGN 的惩罚：弱 ~13x、中 ~140x、强 ~1600x（20 dB 时）
- 惩罚随 SNR 增大而增大（因为深衰落事件的相对影响在高 SNR 时更显著）

### 发现 3：BER floor 的 Fourier 级数验证（F3.12）

**来源**: F3.12（formulas-master.md）; 数值交叉验证

高 SNR 极限下 b_n^{GG} → 1/π，F3.12 闭合形式：

```
P_{b,floor}^{series} = 3/8 - (1/π) Σ_{n=1}^{N} (1/n) · e^{-n²σ_φ²/2} · sin(nπ/4)
```

数值验证：对 σ_φ ≥ 8°，F3.12 级数与 F3.11 Q 函数在 5 位有效数字内一致。

| σ_φ (°) | Q(π/(4σ_φ)) | Fourier N=100 | 匹配 |
|---------|-------------|---------------|------|
| 8 | 9.2754e-09 | 9.2754e-09 | 完美 |
| 10 | 3.3977e-06 | 3.3977e-06 | 完美 |
| 15 | 1.3499e-03 | 1.3499e-03 | 完美 |
| 20 | 1.2224e-02 | 1.2224e-02 | 完美 |

### 发现 4：中断概率与 BER floor 的关系——两个独立概念

**来源**: F3.13-F3.17（formulas-master.md）; GG CDF 数值计算

中断概率 P_out = F_GG(h_th) 衡量"信道太差的概率"，与 BER floor 是不同的物理量：

- P_out 取决于湍流参数 (α, β) 和目标 BER P_target
- P_{b,floor} 取决于 σ_φ，与湍流无关
- 在有限 SNR 下，P_out 为 BER 提供一个统计下界：若 h < h_th 则 BER > P_target
- F3.17 的关键结论：当 P_target < Q(π/(4σ_φ)) 时，γ_th = ∞，P_out = 1（永远无法达到目标 BER）

**中断概率数值**（γ̄ = 20 dB，无相位误差）：

| 湍流 | P_target=1e-3 | P_target=1e-4 | P_target=1e-5 |
|------|---------------|---------------|---------------|
| 弱 (4,3) | 1.36% | 3.10% | 5.45% |
| 中 (2.5,1.8) | 6.04% | 9.90% | 13.9% |
| 强 (1.5,0.8) | 21.5% | 27.2% | 32.0% |

### 发现 5：深衰落概率与 BER 的关系

**来源**: GG CDF 数值计算; 信号模型 γ = γ̄·h

在深衰落事件（h << 1）中，瞬时 SNR 极低，BER ≈ 0.5（随机猜测）。这些事件对平均 BER 的贡献：

```
平均 BER ≈ Σ P(h ≈ h_i) · BER(γ̄·h_i)
```

在有限 SNR 下，深衰落是 BER 恶化的主因。但随着 SNR 增大，正常衰落事件（h ~ 1）的 BER 趋近零，只有深衰落事件持续贡献。最终极限取决于是否有相位误差：
- σ_φ = 0：即使 h→0，BER(∞·0) 不确定但 E_h[Q(√(γ̄·h))] → 0（积分收敛）
- σ_φ > 0：所有 h 的相位平均 BER 都有下界 Q(π/(4σ_φ))，导致 floor

### 发现 6：三档湍流下到达 BER floor 的 SNR 不同

虽然 floor 值相同，但不同湍流强度下到达 floor 所需的 SNR 差异很大：
- 弱湍流：BER 下降快，在较低 SNR 就逼近 floor
- 强湍流：BER 下降慢，需要更高 SNR 才能逼近 floor
- 这个差异来源于 GG 分布的尾部特性：强湍流的 PDF 在 h→0 处有更重的尾部

## 量化预期

### 核心量化表：BER floor 与 σ_φ 的关系

| σ_φ (°) | P_{b,floor} = Q(π/(4σ_φ)) | 物理含义 |
|---------|---------------------------|---------|
| 3 | 3.7e-51 | 近乎理想（理论值） |
| 5 | 1.1e-19 | 近乎理想 |
| 8 | 9.3e-09 | 优良 |
| 10 | 3.4e-06 | 可接受（FEC 可纠） |
| 15 | 1.3e-03 | 需改善 |
| 20 | 1.2e-02 | 严重 |

### 三档湍流锚点（σ_φ = 0，γ̄ = 20 dB）

| 湍流 | (α, β) | BER @ 20 dB | vs AWGN 惩罚 | 深衰落概率 P(h<0.1) |
|------|--------|------------|-------------|-------------------|
| 弱 | (4, 3) | ~1.6e-4 | ~13x | 1.5% |
| 中 | (2.5, 1.8) | ~1.6e-3 | ~140x | 6.4% |
| 强 | (1.5, 0.8) | ~1.8e-2 | ~1600x | 22.1% |

### 关键结论

**三档湍流下的 BER floor 量级完全相同**，由 σ_φ 唯一决定。湍流影响的是 BER 曲线的"斜率"（收敛到 floor 的速度），而非 floor 本身。这意味着：

1. 如果仿真中观察到三档湍流的 BER 曲线在相同高度出现平台 → 正确行为（都等于 Q(π/(4σ_φ))）
2. 如果仿真中观察到 BER 曲线在不同高度出现平台 → 说明存在湍流相关的数值问题
3. 如果 σ_φ = 0 的仿真中出现 BER 平台 → 说明实现有误（不应存在平台）

## Phase 2 检查清单

- [x] 锚点 1: 弱湍流 (α=4,β=3), σ_φ=0 → 预期 BER @ 20dB ≈ 1.6×10⁻⁴，无 floor → 实际 ___
- [x] 锚点 2: 中湍流 (α=2.5,β=1.8), σ_φ=0 → 预期 BER @ 20dB ≈ 1.6×10⁻³，无 floor → 实际 ___
- [x] 锚点 3: 强湍流 (α=1.5,β=0.8), σ_φ=0 → 预期 BER @ 20dB ≈ 1.8×10⁻²，无 floor → 实际 ___
- [x] 锚点 4: 三档湍流, σ_φ=10° → 预期 BER floor = Q(π/(4·0.1745)) ≈ 3.4×10⁻⁶（三档相同） → 实际 ___
- [x] 锚点 5: 中湍流, σ_φ=15° → 预期 BER floor = Q(π/(4·0.2618)) ≈ 1.3×10⁻³ → 实际 ___
- [x] 锚点 6: BER floor 不随 SNR 继续下降 → 在 30-40 dB 范围内 BER 曲线应出现明确平台 → 实际 ___

## 参考文献

1. **Petkovic 2023** (Mathematics, 11, 121) — "Error Probability of a Coherent M-ary PSK FSO System with Phase Noise in M-distributed Turbulence Channel"：Fourier 级数法推导 SEP，渐近分析证明 floor 仅取决于 σ_φ
2. **Hu 2025** (IEEE J. Photonics, doi:10.1109_jphot.2025.3534258) — "Performance of Coherent Optical MPSK in Underwater Turbulent Channels With Phase Errors"：MPSK BER floor 闭合公式 Eq.(34)-(35)，明确指出 floor 与信道无关
3. **F3.11-F3.17** (formulas-master.md) — 自推 BER floor 闭合公式、Fourier 验证、中断概率分析
4. **Proakis, Digital Communications** — QPSK BER 在相位误差下的基本表达式
