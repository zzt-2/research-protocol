# V-04: Monte Carlo 验证方法的统计正确性

> 关联仿真: sim_ch3_ber_closed_form.py | Phase: 1a | 批次: B1
> 状态: 完成 | 发现锚点数: 6

## 调研问题

闭合解 vs Monte Carlo (MC) 仿真 BER 对比验证中，MC 仿真的统计精度如何评估？最小样本数应是多少？闭合解与 MC 的偏差在什么范围内算正常？当前代码参数是否足够？

---

## 1. MC BER 的统计模型

### 1.1 基本模型

MC 仿真中，每个比特的传输是一次独立 Bernoulli 试验：错误概率为 p（真实 BER），正确概率为 1-p。N 次传输中观察到 k 次错误，则：

- **点估计**: $\hat{p} = k / N$
- **分布**: $k \sim \text{Binomial}(N, p)$
- **方差**: $\text{Var}(\hat{p}) = p(1-p)/N \approx p/N$（当 $p \ll 1$ 时）

### 1.2 置信区间公式

**方法 1: Clopper-Pearson 精确区间（推荐，小样本 k < 50 时必用）**

基于 Beta 分布：

$$p_L = B(\alpha/2;\; k,\; N-k+1), \quad p_U = B(1-\alpha/2;\; k+1,\; N-k)$$

其中 $B(q;\; a,\; b)$ 是 Beta(a,b) 分布的 q 分位数。此方法保证覆盖率 $\ge 1-\alpha$（保守），是通信仿真文献推荐的标准化方法。

**方法 2: 正态近似（Wald 区间，k >= 50 时可用）**

$$\hat{p} \pm z_{\alpha/2}\sqrt{\hat{p}(1-\hat{p})/N}$$

95% CI 时 $z_{\alpha/2} = 1.96$。此方法在 $N\hat{p} \ge 5$ 且 $N(1-\hat{p}) \ge 5$ 时近似良好，否则低估 CI 宽度。

**方法 3: "Rule of Three"（k=0 时使用）**

当观察到零错误时：$P(k=0|p,N) = (1-p)^N$

95% 上界: $p < 3/N$（由 $-\ln(0.05) \approx 3.0$）

### 1.3 文献依据

- **Jeruchim 1984**: "Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems," IEEE JSAC — 通信仿真 BER 统计的经典参考文献
- **Jeruchim, Balaban, Shanmugan 2000**: *Simulation of Communication Systems*, 2nd ed. — 系统化讨论 BER 置信区间和样本量
- **Tranter et al. 2004**: *Principles of Communication Systems Simulation* — 含详细推导
- **Clopper & Pearson 1934**: "The Use of Confidence or Fiducial Limits," *Biometrika* — 原始精确区间方法

---

## 2. 最小样本数经验法则

### 2.1 "10 错误"法则

通信仿真领域最广泛引用的经验法则（Jeruchim 1984, ITU-T O.150）：

> **MC 仿真 BER 需要观察到至少 10 次错误，才能给出有意义的点估计。**

由此推导最小样本数：

$$N_{\min} = k_{\min} / \text{BER}$$

| 目标 BER | N_min (10 errors) | N_min (50 errors) | N_min (100 errors) |
|-----------|-------------------|-------------------|---------------------|
| 10^-2     | 1,000             | 5,000             | 10,000              |
| 10^-3     | 10,000            | 50,000            | 100,000             |
| 10^-4     | 100,000           | 500,000           | 1,000,000           |
| 10^-5     | 1,000,000         | 5,000,000         | 10,000,000          |
| 10^-6     | 10,000,000        | 50,000,000        | 100,000,000         |

### 2.2 不同错误数下的 CI 宽度（95% Clopper-Pearson）

| 目标 BER | k=10 误差 CI 宽度 | k=50 误差 CI 宽度 | k=100 误差 CI 宽度 |
|-----------|------------------|------------------|-------------------|
| 任意      | 136%             | 58%              | 40%               |

注：CI 宽度 = (p_U - p_L) / p，仅取决于 k 而非 p 本身（当 p << 1 时）。

---

## 3. 闭合解 vs MC 可接受偏差判据

### 3.1 统计学判据

闭合解公式若数学正确，则理论值即为"真值" p。MC 观测值 $\hat{p}$ 的 95% CI 应包含 p。因此：

> **PASS 判据: 闭合解 BER 落在 MC 的 95% Clopper-Pearson CI 内。**

等价表述：$|\text{theory} - \text{MC}| / \text{MC} < \text{CI 半宽（单侧）}$

### 3.2 不同 BER 和 N 下的可接受偏差阈值

| BER 量级 | N (bits) | 预期错误数 k | 95% CI 相对半宽 | 可接受 \|theory-MC\|/MC |
|-----------|----------|-------------|----------------|------------------------|
| 10^-2     | 500,000  | 5,000       | 2.8%           | < 3%                   |
| 10^-3     | 500,000  | 500         | 8.9%           | < 9%                   |
| 10^-4     | 500,000  | 50          | 28.8%          | < 29%                  |
| 10^-4     | 2,000,000| 200         | 14.1%          | < 14%                  |
| 10^-5     | 5,000,000| 50          | 28.8%          | < 29%                  |
| 10^-6     | 10,000,000| 10         | 68.0%          | < 68%                  |

### 3.3 实用判据分级

| 分级 | 条件 | 判据 | 说明 |
|------|------|------|------|
| A (严格) | k >= 100 | \|theory-MC\|/MC < 5% | 高 SNR / 强湍流 |
| B (标准) | 10 <= k < 100 | \|theory-MC\|/MC < 20% | 中等 SNR / 中湍流 |
| C (宽松) | 1 <= k < 10 | \|theory-MC\|/MC < 50% | 低 BER 区域，MC 不可靠 |
| D (不适用) | k = 0 | 无法判定 | 需增大 N 或跳过 MC 验证 |

---

## 4. 当前代码 MC 参数评估

### 4.1 代码参数

`sim_ch3_ber_closed_form.py` L36:
```python
N_SYM = 500_000
```

MC 函数 `mc_ber_linear` (L200-206): 对每个 SNR 点独立生成 N_SYM 个符号（每个符号 2 比特，实际 N_bits = 1,000,000），计算条件 BER 后取均值。

**注意**: 代码中 `mc_ber_linear` 实际是对 N_SYM 个**符号**计算条件 BER 再取均值，不是直接统计比特错误数。这是一种"软"MC 方法——每个样本的 BER 取值在 [0, 0.5] 连续分布，等效样本量远大于简单 Bernoulli 计数。因此其统计特性优于简单二项计数，以下分析是保守的。

### 4.2 各典型场景下的统计可靠性

| 场景 | BER | 预期错误数 (k) | 95% CI 宽度 | 评级 |
|------|-----|---------------|------------|------|
| 强湍流 20dB, sigma=10deg | ~2.2e-3 | ~1,100 | 12% | **OK** |
| 中湍流 20dB, sigma=10deg | ~2.2e-3 | ~1,100 | 12% | **OK** |
| 弱湍流 20dB, sigma=10deg | ~5e-5 | ~25 | 83% | **MARGINAL** |
| 弱湍流 20dB, sigma=0 | ~1.5e-4 | ~75 | 47% | **MARGINAL** |
| 弱湍流 25dB, sigma=0 | ~7.6e-6 | ~3.8 | 241% | **INSUFFICIENT** |
| 弱湍流 30dB, sigma=0 | ~3e-7 | ~0.15 | 不可用 | **INSUFFICIENT** |
| BER floor sigma=10deg @40dB | ~3.4e-6 | ~1.7 | 326% | **INSUFFICIENT** |
| BER floor sigma=15deg @40dB | ~1.35e-3 | ~675 | 15% | **OK** |

### 4.3 评估结论

- **N_SYM=500K 对 BER >= 10^-3 完全足够**（k >= 500，CI 宽度 < 18%）
- **对 BER ~ 10^-4 勉强可用**（k ~ 50，CI 宽度 ~ 58%），可做定性验证但不适合精确定量对比
- **对 BER < 10^-5 完全不足**（k < 5），MC 结果不可靠
- BER floor 验证（sigma=10deg, ~3.4e-6）需要 N >= 10M 才有 30+ 错误

### 4.4 改进建议

对于论文验证，建议的修正策略：

1. **BER >= 10^-3**: 保持 N_SYM = 500K，理论 vs MC 应差 < 10%
2. **BER ~ 10^-4**: 增大至 N_SYM = 2M，理论 vs MC 应差 < 15%
3. **BER ~ 10^-5**: 增大至 N_SYM = 5M，理论 vs MC 应差 < 30%
4. **BER < 10^-5**: **不建议用 MC 验证**，改用：
   - 与已知 BER floor 公式 Q(pi/(4*sigma_phi)) 对比
   - 高 SNR 极限下 b_n^GG -> 1/pi 的渐近分析
   - 文献数值对比（如 Petkovic 2023 Fig.2-5）

---

## 5. 量化锚点（Phase 2 检查清单）

### 锚点 1: 强湍流/中湍流 20dB — MC 高精度区域

- **条件**: BER ~ 10^-3 ~ 10^-2, N=500K, k >= 500
- **95% CI 相对宽度**: 5.5% ~ 12.5%
- **PASS 标准**: |闭合解 - MC| / MC < 10%
- **依据**: Clopper-Pearson 精确区间计算

### 锚点 2: 弱湍流 20dB — MC 精度边界

- **条件**: BER ~ 10^-4, N=500K, k ~ 50
- **95% CI 相对宽度**: 57.6%
- **PASS 标准**: |闭合解 - MC| / MC < 30%（或闭合解落在 MC 的 95% CI 内）
- **改进**: 增大 N 至 2M 后 PASS 标准收紧至 < 14%

### 锚点 3: BER floor sigma=15deg — 高 BER floor 区域

- **条件**: BER ~ 1.35e-3, N=500K, k ~ 675
- **95% CI 相对宽度**: 15.2%
- **PASS 标准**: |闭合解 Q(pi/(4*sigma)) - MC@40dB| / MC < 10%

### 锚点 4: 零错误观察 — "Rule of Three"

- **条件**: BER < 3/N 时出现 k=0
- **N=500K**: 若 k=0 则 BER < 6e-6（95% 上界）
- **应用**: 弱湍流 sigma=10deg 25dB+ 时 MC 可能出现零错误，此时只能判定 BER < 6e-6，无法与闭合解定量对比

### 锚点 5: 精确 vs 近似 BER 的 MC 验证精度要求

- **条件**: sigma_phi >= 5deg（Fourier 级数收敛良好）
- **预期**: V-03 已验证 sigma=10deg 时 Fourier vs MC 差 0.1%
- **PASS 标准**: |精确 BER (F3.10) - MC| / MC < 5%（在 k >= 100 条件下）

### 锚点 6: 多种子重复实验的稳定性

- **条件**: 使用不同随机种子（n_seeds >= 5），每个种子独立 N_SYM
- **PASS 标准**: 各种子 MC BER 的变异系数 (CV = std/mean) < CI 半宽的理论预测
- **依据**: 多种子实验可进一步确认 MC 结果的统计可靠性

---

## 6. 关键结论

1. **N_SYM=500K 对 BER >= 10^-3 完全足够**，闭合解 vs MC 偏差应 < 10%（锚点 1）
2. **对 BER ~ 10^-4 需要增大 N 至 2M** 才能达到 < 15% 偏差判据（锚点 2）
3. **BER < 10^-5 不适合 MC 验证**，应依赖 BER floor 公式和文献对照（锚点 4）
4. **闭合解 vs MC 的 PASS 判据**: 理论值落在 MC 的 95% Clopper-Pearson CI 内（锚点 5）
5. **"10 错误法则"是最小要求，100 错误给出可靠验证**: k=10 时 CI 宽 136%，k=100 时仅 40%（锚点 6，量化表 §2.2）
6. **代码使用"软 MC"（条件 BER 均值）而非硬判决计数**，统计特性优于简单 Bernoulli，上述分析是保守的

## 7. 风险提示

- MC 方法无法验证 BER < 10^-6 的闭合解（需要 N >= 100M），需依赖解析方法交叉验证
- 正态近似在 k < 30 时严重低估 CI 宽度，必须使用 Clopper-Pearson 精确区间
- 零错误观察只能给出上界（Rule of Three），不能确认闭合解正确
- 当前代码仅使用单种子（seed=42），建议补充多种子实验确认统计稳定性

## 参考文献

1. M. C. Jeruchim, "Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems," IEEE JSAC, vol. 2, no. 1, pp. 153-170, Jan. 1984.
2. M. C. Jeruchim, P. Balaban, K. S. Shanmugan, *Simulation of Communication Systems*, 2nd ed., Plenum Press, 2000.
3. C. J. Clopper and E. S. Pearson, "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial," *Biometrika*, vol. 26, no. 4, pp. 404-413, 1934.
4. W. H. Tranter et al., *Principles of Communication Systems Simulation*, Prentice Hall, 2004.
5. ITU-T Recommendation O.150, "Digital test patterns for performance measurements on digital transmission equipment."
