# Ch3 大气湍流信道下 QPSK 相干检测链路性能分析 — 公式推导

> 生成时间: 2026-05-30
> 来源: S002 推导, Petkovic 2023 (DOI: 10.3390/math11010121), Hu 2025 (DOI: 10.1109/JPHOT.2025.3534258)
> 仿真验证: sim_ch3_ber_closed_form.py, sim_ch3_strengthening.py

---

## 3.2 系统模型

### F3.1 接收信号模型（含载波相位误差）

$$r = \sqrt{\gamma} \cdot s \cdot e^{j\phi} + n$$

- $\gamma = \bar\gamma \cdot h$：瞬时 SNR（相干检测，$\gamma \propto$ 辐照度）
- $h \sim \text{GG}(\alpha, \beta)$，$E[h]=1$
- $\phi \sim \mathcal{N}(0, \sigma_\phi^2)$：载波相位误差
- $s \in \{(1\pm j)/\sqrt{2}\}$：QPSK 符号
- $n \sim \mathcal{CN}(0, 1)$：AWGN

**来源**: S002 §1, Petkovic 2023 §II
**与前文关系**: Ch2 F3.1 的相位误差显式形式——Ch2 估计 $h$，Ch3 分析 $\phi$ 对性能的影响，Ch4 补偿 $\phi$

### F3.2 SNR 模型说明：$\gamma = \bar\gamma \cdot h$（非 $h^2$）

相干检测中：接收光功率 $P_r \propto h$（辐照度），光电转换后信号电流 $i \propto \sqrt{P_r P_{LO}}$，信号功率 $i^2 \propto P_r \propto h$。因此 SNR $\propto h$（线性）。

- $h^2$ 模型适用于 IM/DD 直接检测，不适用于相干检测
- 文献支撑：Colavolpe 等推导 coherent $\gamma \propto h$ vs IM/DD $\gamma \propto h^2$；Ansari-Alouini 统一框架参数 $r=1$（相干）/ $r=2$（IM/DD）
- H002 确认：零争议，教科书标准

**来源**: S002 §1, Ansari-Alouini 统一框架
**注意**: 与 Ch2 E[1/h²] 发散推导中的约定一致（Ch2 用 $h$ 表示辐照度，非 $h^2$）

### F3.3 湍流参数

| 湍流 | $\alpha$ | $\beta$ | 来源 |
|------|---------|---------|------|
| 弱 | 4.0 | 3.0 | Trinh 2017 |
| 中 | 2.5 | 1.8 | Trinh 2017 |
| 强 | 1.5 | 0.8 | Trinh 2017 |

S019 参数统一确认，与 sim_prototype.py / sim_direction_a.py 一致。

---

## 3.3 条件 BER

### F3.4 QPSK 条件 BER（Gray coding）

$$P_b(\gamma, \phi) = \frac{1}{2}\left[Q(\sqrt{2\gamma}\cos(\phi+\pi/4)) + Q(\sqrt{2\gamma}\cos(\phi-\pi/4))\right]$$

- 因子 1/2：QPSK 每符号 2 bit，BER = 总 bit 错误数 / 总 bit 数
- 无相位误差时（$\phi=0$）：$P_b = Q(\sqrt{\gamma})$（标准 QPSK BER，退化为 Ch2 结果）
- $Q(x) = \frac{1}{2}\text{erfc}(x/\sqrt{2})$

**来源**: S002 §2, Proakis Digital Communications

---

## 3.4 平均 BER：Fourier 级数法

### F3.5 AWGN 相位 PDF 的 Fourier 展开

$$f_\psi(\psi|\gamma) = \frac{1}{2\pi} + \sum_{n=1}^{\infty} a_n(\gamma) \cos(n\psi)$$

其中 $a_n(\gamma)$ 涉及 confluent hypergeometric 函数（Petkovic 2023 Eq.14）。

**来源**: Petkovic 2023 §III-A

### F3.6 GG 信道平均 Fourier 系数 $b_n^{GG}$（Meijer-G 闭合形式）

$$b_n^{GG} = \frac{n}{2\pi\Gamma(\alpha)\Gamma(\beta)} G_{2,3}^{3,1}\left(\frac{\alpha\beta}{\bar\gamma} \,\middle|\, \begin{matrix} 1-n/2, & 1+n/2 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

- GG 是 Málaga 分布 $\rho=0$ 的特例（Petkovic 2023 Eq.19）
- 高 SNR 极限：$\bar\gamma \to \infty$ 时 $b_n^{GG} \to 1/\pi$
- **数值验证**（中湍流，S002）：

| SNR | $b_1$ | $b_2$ | $b_3$ | 极限 $1/\pi$ |
|-----|-------|-------|-------|------------|
| 0 dB | 0.192 | 0.097 | 0.046 | 0.318 |
| 20 dB | 0.315 | 0.308 | 0.297 | 0.318 |
| 40 dB | 0.318 | 0.318 | 0.318 | 0.318 |

**来源**: Petkovic 2023 Eq.19, S002 §3.2
**代码**: sim_ch3_ber_closed_form.py `bn_gg_v2`
**风险**: Meijer-G 参数序已验证（CDF < 10⁻⁸），S002 交叉确认

### F3.7 高斯相位误差的 Fourier 系数

$$c_n^{Gauss} = \frac{1}{\pi}\int_{-\pi}^{\pi} \cos(n\phi) \cdot \frac{e^{-\phi^2/(2\sigma_\phi^2)}}{\sigma_\phi\sqrt{2\pi}} d\phi \approx \frac{1}{\pi} e^{-n^2\sigma_\phi^2/2}$$

**推导**：高斯函数的 Fourier 变换 $\int_{-\infty}^{\infty} \cos(n\phi) e^{-\phi^2/(2\sigma^2)} d\phi = \sigma\sqrt{2\pi} e^{-n^2\sigma^2/2}$。当 $\sigma_\phi \ll \pi$（典型值 $\sigma_\phi \leq 15° = 0.26$ rad），截断误差可忽略。

**衰减行为**：$c_n$ 以 $\exp(-n^2\sigma_\phi^2/2)$ 衰减，比 Tikhoniv（Bessel $I_n$）衰减更快，级数收敛性更好。

**来源**: S002 §3.3, 标准 Fourier 分析

### F3.8 平均 SEP（Fourier 级数法）

$$P_s = \frac{3}{4} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

**推导逻辑**：
1. AWGN 相位 PDF → Fourier 展开（系数 $a_n(\gamma)$）
2. 对 GG 信道取平均 → $b_n^{GG}$（Meijer-G 闭合形式）
3. 总相位 PDF = AWGN 相位 $\ast$ 载波相位误差（卷积）
4. Fourier 域：系数相乘 $b_n \cdot c_n$
5. SEP = $1 - \int_{-\pi/4}^{\pi/4} f_{total}(\psi) d\psi$ → 级数求和

**$\sin(n\pi/4)$ 模式**：周期 8，仅 $n \not\equiv 0 \pmod{4}$ 的项贡献非零值。

**来源**: Petkovic 2023 §III-B, S002 §3.4
**注意**: Fourier 级数法定位为**工具**（非核心创新），H002 文献审查确认此方法小众

### F3.9 BER 近似（$P_s/2$）

$$P_b \approx \frac{P_s}{2} = \frac{3}{8} - \sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

- Gray coding 假设：相邻符号错误翻转 1 bit
- **精度**：中等-高 SNR 下偏差 <10%（MC 验证 median 6.0%）。低 SNR 下对角错误（2 bit 翻转）贡献增大

**来源**: S002 §3.5

### F3.10 精确 BER（I/Q 通道分别积分）

$$\boxed{P_b^{exact} = \frac{1}{2} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{2} \cos\frac{n\pi}{4}}$$

**推导**：
- I 通道错误概率：$P_I = P(\cos(\pi/4 + \psi) < 0) = 1 - \int_{-3\pi/4}^{\pi/4} f_{total}(\psi) d\psi$
- 利用 Fourier 展开：$\int_{-3\pi/4}^{\pi/4} \cos(n\psi) d\psi = \frac{2}{n}\sin(n\pi/2)\cos(n\pi/4)$
- Q 通道由 QPSK 对称性：$P_Q = P_I$
- 精确 BER：$P_b = (P_I + P_Q)/2 = P_I$

**与 F3.9 的区别**：
- F3.9：$\sin(n\pi/4)$ 加权，偶数 n 有贡献（n=2,6,...）
- F3.10：$\sin(n\pi/2)\cos(n\pi/4)$ 加权，偶数 n 贡献为零（$\sin(n\pi/2)=0$）

**验证**（MC，中湍流 $\sigma_\phi=10°$，500k 符号）：

| 公式 | median 误差 | max 误差 |
|------|-----------|---------|
| F3.9 ($P_s/2$) | 6.0% | 69.4% |
| F3.10（精确） | 0.6% | 85.9% |

**来源**: S002 §3.6
**代码**: sim_ch3_ber_closed_form.py `ber_exact`

---

## 3.5 BER Floor

### F3.11 BER Floor 闭合公式

$$P_{b,floor} = Q\!\left(\frac{\pi}{4\sigma_\phi}\right)$$

**推导**：当 $\bar\gamma \to \infty$，AWGN 噪声消失：
- $\phi \in (-\pi/4, \pi/4)$：两个 cos 均 > 0 → $P_b = 0$
- $\phi \in (\pi/4, 3\pi/4)$：$\cos(\phi+\pi/4) < 0$ → $P_b = 1/2$
- $P_{b,floor} = \frac{1}{2}[P(|\phi| > \pi/4)] = Q(\pi/(4\sigma_\phi))$

**物理含义**：BER floor 完全由 $\sigma_\phi$ 决定，与湍流强度无关。高 SNR 下相位误差是唯一性能瓶颈。

**关键数值**：

| $\sigma_\phi$ | $Q(\pi/4\sigma_\phi)$ | 说明 |
|--------------|----------------------|------|
| 5° | 1.13e-19 | 近乎完美 |
| 8° | 9.28e-09 | 优良 |
| 10° | 3.40e-06 | 可接受 |
| 15° | 1.35e-03 | 需改善 |
| 20° | 1.22e-02 | 严重 |

**来源**: S002 §4
**文献定位**: RF 领域经典结果（Proakis 教材、IET 1995/2020）。H002 确认**不可声称新颖**，应强调 FSO 场景特殊性

### F3.12 BER Floor 的 Fourier 级数验证

高 SNR 时 $b_n \to 1/\pi$：

$$P_{b,floor}^{series} = \frac{3}{8} - \frac{1}{\pi}\sum_{n=1}^{N} \frac{1}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

$\sigma_\phi \geq 8°$ 时，series 与 $Q(\pi/(4\sigma_\phi))$ 在 5 位有效数字内一致。

---

## 3.6 中断概率

### F3.13 中断概率定义

$$P_{out} = P(\bar{P}_b(\bar\gamma h, \sigma_\phi) > P_{target}) = F_{GG}(h_{th})$$

其中 $P_b^{avg}(\gamma, \sigma_\phi) = E_\phi[P_b(\gamma, \phi)]$ 是相位平均 BER。

### F3.14 阈值 SNR

由于 $P_b^{avg}$ 关于 $\gamma$ 单调递减，存在唯一阈值 $\gamma_{th}$ 满足：

$$P_b^{avg}(\gamma_{th}, \sigma_\phi) = P_{target}$$

$$h_{th} = \gamma_{th} / \bar\gamma$$

**来源**: S002 §5.2

### F3.15 GG CDF（Meijer-G 闭合形式）

$$F_{GG}(h) = \frac{1}{\Gamma(\alpha)\Gamma(\beta)} G_{1,3}^{2,1}\left(\alpha\beta h \,\middle|\, \begin{matrix} 1 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

**交叉验证**：12 个测试点（3 湍流 × 4 h 值），最大相对误差 4.39×10⁻⁹（中湍流 h=0.01）。Meijer-G CDF 实现正确。

**来源**: S002 §5.3, Andrews & Phillips textbook
**代码**: sim_ch3_ber_closed_form.py `gg_cdf`

### F3.16 无相位误差时的简化

$\sigma_\phi = 0$ 时，$P_b = Q(\sqrt{\gamma})$，阈值 $\gamma_{th} = [Q^{-1}(P_{target})]^2$。

$$P_{out}^{(0)} = F_{GG}\left(\frac{[Q^{-1}(P_{target})]^2}{\bar\gamma}\right)$$

### F3.17 BER floor 对中断概率的影响

当 $P_{target} < Q(\pi/(4\sigma_\phi))$ 时，$\gamma_{th} = \infty$，$P_{out} = 1$（永远无法达到目标 BER）。这是 BER floor 的另一视角。

**验证结果**（$P_{target} = 10^{-3}$）：

| $\sigma_\phi$ | $\gamma_{th}$ (dB) | SNR 惩罚 | 备注 |
|--------------|-------------------|---------|------|
| 0° | 9.8 | 0 dB | 基准 |
| 5° | 10.2 | +0.4 dB | 轻微 |
| 10° | 12.0 | +2.2 dB | 显著 |
| 15° | $\infty$ | — | Floor $1.35\times10^{-3}$ > $10^{-3}$，不可达 |

---

## 3.7 $\sigma_\phi$ 设计目标（Ch3→Ch4 衔接）

### F3.18 相位误差约束

$$Q\!\left(\frac{\pi}{4\sigma_\phi}\right) \leq P_{target} \implies \sigma_\phi \leq \frac{\pi}{4 Q^{-1}(P_{target})}$$

| $P_{target}$ | $\sigma_\phi$ 上限 | 对应角度 |
|-------------|------------------|---------|
| $10^{-3}$ | 0.254 rad | 14.6° |
| $10^{-4}$ | 0.211 rad | 12.1° |
| $10^{-5}$ | 0.184 rad | 10.6° |
| $10^{-6}$ | 0.165 rad | 9.5° |

**数值验证**：$\sigma_{\phi,\max} = \pi / (4 \cdot Q^{-1}(P_{target}))$，使用 scipy `norm.ppf(1-P_target)` 精确计算。

**Ch4 的任务**：设计载波同步算法使得 $\sigma_\phi$ 满足上述约束。具体关系：
- DPLL：$\sigma_\phi^2 \approx B_L T_s / (2\bar\gamma h)$（线性化模型）
- VV-CPR：$\sigma_\phi^2 \approx 1/(2M\bar\gamma h)$（$M$ = 窗口长度）

**来源**: S002 §6, Ch4 formulas F4.7-F4.10

---

## 3.8 设计准则（加强 1）

### F3.19 分湍流中断概率设计表

基于中断概率的设计表（$P_{out} = 1\%$, $P_{BER} = 10^{-4}$）：

| 湍流 | SNR($\sigma_\phi=0°$) | SNR($\sigma_\phi=5°$) | SNR($\sigma_\phi=10°$) | 惩罚@10° |
|------|----------------------|----------------------|-----------------------|----------|
| 弱 | 22.2 dB | 22.8 dB | 26.4 dB | +4.2 dB |
| 中 | 26.9 dB | 27.4 dB | 31.1 dB | +4.2 dB |
| 强 | 39.6 dB | 40.1 dB | 43.8 dB | +4.2 dB |

**数值方法**：$\gamma_{th}$ 通过 `scipy.integrate.quad` 精确积分求解（非梯形近似），积分限 $\pm 5\sigma_\phi$，容差 $10^{-12}$。

### F3.20 SNR 惩罚与湍流无关性

$\sigma_\phi$ 导致的 SNR 惩罚与湍流强度无关（均为 +4.2 dB @ $\sigma_\phi=10°$, $P_{target}=10^{-4}$）。

**数值验证**（9 组条件：3 $P_{target}$ × 3 $P_{out}$，$\sigma_\phi=10°$，精确积分 `scipy.integrate.quad`）：
- 惩罚值：$P_{target}=10^{-3}$ → 2.20 dB，$10^{-4}$ → 4.21 dB，$10^{-5}$ → 8.91 dB
- 同一 $P_{target}$ 下不同湍流条件的惩罚差异 < 0.01 dB
- **结论：SNR 惩罚与湍流无关的代数性质被数值确认**

不可达边界：$\sigma_\phi > 12.1°$ 时 BER floor > $10^{-4}$，任何 SNR 均无法达标。

**来源**: S002 加强 1, sim_ch3_strengthening.py

---

## 3.9 估计误差鲁棒性（加强 2）

### F3.21 自适应 DPLL 带宽的鲁棒性

**模型**：$\hat{h} = h(1+\epsilon)$，$\epsilon \sim \mathcal{N}(0, \text{NMSE})$

**关键发现**：DPLL 自适应带宽 $B_L = B_0 \hat{h}$ 使 $\sigma_\phi^2$ 与 $h$ 无关（$B_L \propto h$ 与 $\gamma \propto h$ 精确抵消），因此估计误差对平均 BER 的影响可忽略（ratio = 1.000 @ NMSE = -5 dB）。

**物理解释**：载波同步对信道估计误差天然鲁棒——$B_L \propto h$ 和 $\gamma \propto h$ 形成对消，$\sigma_\phi$ 与信道状态无关。

**对论文意义**：解释了为什么 Ch4 载波同步算法在 Ch2 估计不完美时仍能正常工作（与 sim_cascade_robustness.py 6/6 PASS 一致）。

**文献定位**: H002 确认：未见于 FSO 文献，但代数消元"显而易见"。定位为**设计洞察而非理论创新**。

**来源**: S002 加强 2, sim_ch3_strengthening.py

---

## 贡献定位（H002 文献审查结论）

1. **核心贡献** = 联合分析框架（GG 湍流 + 载波相位误差 → BER 闭合解 + 中断概率）
2. Fourier 级数法 = 工具（与 Petkovic 2023 区别：GG 非特例、Gaussian 非 Tikhonov、BER 非 SEP）
3. BER floor = 经典结果在 FSO 场景的应用
4. $B_L \propto h$ 抵消 = 设计洞察
5. 需引用 Petkovic 2023 并显式区分

---

## 缺失与风险

| 风险项 | 严重度 | 状态 |
|--------|--------|------|
| Meijer-G 参数序错误 | 高 | ✓ 已排除（CDF < 10⁻⁸） |
| $b_n$ Meijer-G 错误 | 高 | ✓ 已排除（$b_n \to 1/\pi$） |
| SNR 惩罚无关是巧合 | 中 | ✓ 已排除（精确积分确认同 P_target 下惩罚差 <0.01 dB） |
| $\gamma=\bar\gamma \cdot h$ 模型假设 | 低 | ✓ 文献零争议 |
| 线性化 DPLL 模型局限 | 中 | clip 区域内不成立，论文讨论 |
| "估计误差无影响"过于简化 | 中 | 模型内正确，注明适用范围 |

### 待补充

1. **Petkovic 2023 原文引用标注** — F3.6/F3.8 需精确引用原文公式编号
2. **Hu 2025 区分** — 说明 EGG vs GG 差异，为何不直接用 Hu 的结果
3. **Meijer-G 数值稳定性讨论** — 低 SNR 或极端参数下的收敛性
