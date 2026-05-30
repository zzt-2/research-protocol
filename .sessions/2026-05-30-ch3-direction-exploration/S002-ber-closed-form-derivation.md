# [S002] GG + 高斯相位误差 + QPSK 平均 BER 闭合解推导

> 2026-05-30 | 推导阶段 | 已完成

## 目标

推导 Gamma-Gamma 湍流 + 高斯相位误差 + QPSK 相干检测的平均 BER 闭合级数解、BER floor 和中断概率。

## 方法论来源

- **Petkovic 2023** (DOI: 10.3390/math11010121)：Fourier 级数法，Málaga + Tikhonov → SEP。GG 是 Málaga 的 ρ=0 特例，$b_n^{GG}$ 已有闭合 Meijer-G 形式。
- **Hu 2025** (DOI: 10.1109/JPHOT.2025.3534258)：EGG + 高斯相位误差 → BER。EGG≠GG，但 φ 积分闭合方法 100% 可迁移。

## 推导

### 1. 系统模型

**接收信号**（QPSK 相干检测）：
$$r = \sqrt{\gamma} \cdot s \cdot e^{j\phi} + n$$

- $\gamma = \bar\gamma \cdot h$：瞬时 SNR（相干检测，$\gamma \propto$ 辐照度）
- $h \sim \text{GG}(\alpha, \beta)$，$E[h]=1$
- $\phi \sim \mathcal{N}(0, \sigma_\phi^2)$：载波相位误差
- $s \in \{(1\pm j)/\sqrt{2}\}$：QPSK 符号
- $n \sim \mathcal{CN}(0, 1)$：AWGN

**为什么 $\gamma = \bar\gamma \cdot h$ 而非 $\gamma = \bar\gamma \cdot h^2$**：相干检测中，接收光功率 $P_r \propto h$（辐照度），光电转换后信号电流 $i \propto \sqrt{P_r P_{LO}}$，信号功率 $i^2 \propto P_r \propto h$。因此 SNR $\propto h$（线性）。$h^2$ 模型适用于直接检测（IM/DD），不适用于相干检测。

**三档湍流参数**：
| 湍流 | $\alpha$ | $\beta$ |
|------|---------|---------|
| 弱 | 4.0 | 3.0 |
| 中 | 2.5 | 1.8 |
| 强 | 1.5 | 0.8 |

### 2. 条件 BER

QPSK (Gray coding) 在瞬时 SNR $\gamma$ 和相位误差 $\phi$ 下的每比特 BER：

$$P_b(\gamma, \phi) = \frac{1}{2}\left[Q(\sqrt{2\gamma}\cos(\phi+\pi/4)) + Q(\sqrt{2\gamma}\cos(\phi-\pi/4))\right]$$

- 因子 1/2：QPSK 每符号 2 bit，BER = 总 bit 错误数 / 总 bit 数
- 无相位误差时（$\phi=0$）：$P_b = Q(\sqrt{\gamma})$（标准 QPSK BER）

### 3. 平均 BER：Fourier 级数法

#### 3.1 接收相位 PDF 的 Fourier 展开

接收信号的总相位误差 $\psi_{total} = \psi_{AWGN} + \phi$，其中 $\psi_{AWGN}$ 是 AWGN 引起的相位噪声，$\phi$ 是载波相位误差。

AWGN 相位 $\psi$ 的条件 PDF（给定 SNR $\gamma$）在 $[-\pi, \pi]$ 上展开为 Fourier 级数：

$$f_\psi(\psi|\gamma) = \frac{1}{2\pi} + \sum_{n=1}^{\infty} a_n(\gamma) \cos(n\psi)$$

其中 $a_n(\gamma)$ 是已知函数（Petkovic 2023 Eq.14），涉及 confluent hypergeometric 函数。

#### 3.2 信道平均 Fourier 系数

对 GG 信道取平均：

$$b_n = \int_0^{\infty} a_n(\gamma) \cdot f_\gamma(\gamma) \, d\gamma$$

**GG 下的闭合结果**（Petkovic 2023 Eq.19）：

$$b_n^{GG} = \frac{n}{2\pi\Gamma(\alpha)\Gamma(\beta)} G_{2,3}^{3,1}\left(\frac{\alpha\beta}{\bar\gamma} \,\middle|\, \begin{matrix} 1-n/2, & 1+n/2 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

**高 SNR 极限**：$\bar\gamma \to \infty$ 时 $b_n^{GG} \to 1/\pi$（对应无 AWGN 噪声，相位确定）。

**数值验证**（中湍流 $\alpha=2.5, \beta=1.8$）：

| SNR | $b_1$ | $b_2$ | $b_3$ | 极限 $1/\pi$ |
|-----|-------|-------|-------|------------|
| 0 dB | 0.192 | 0.097 | 0.046 | 0.318 |
| 20 dB | 0.315 | 0.308 | 0.297 | 0.318 |
| 40 dB | 0.318 | 0.318 | 0.318 | 0.318 |

#### 3.3 高斯相位误差的 Fourier 系数

高斯 PDF 的 Fourier 系数（在 $[-\pi, \pi]$ 上展开，$\sigma_\phi \ll \pi$ 时截断近似极佳）：

$$c_n^{Gauss} = \frac{1}{\pi}\int_{-\pi}^{\pi} \cos(n\phi) \cdot \frac{e^{-\phi^2/(2\sigma_\phi^2)}}{\sigma_\phi\sqrt{2\pi}} d\phi \approx \frac{1}{\pi} e^{-n^2\sigma_\phi^2/2}$$

**推导**：利用高斯函数的 Fourier 变换 $\int_{-\infty}^{\infty} \cos(n\phi) e^{-\phi^2/(2\sigma^2)} d\phi = \sigma\sqrt{2\pi} e^{-n^2\sigma^2/2}$。当 $\sigma_\phi \ll \pi$（典型值 $\sigma_\phi \leq 15° = 0.26$ rad），截断误差可忽略。

**衰减行为**：$c_n$ 以 $\exp(-n^2\sigma_\phi^2/2)$ 衰减，比 Tikhonov（Bessel $I_n$）衰减更快，级数收敛性更好。

#### 3.4 平均 SEP

Petkovic 的 Fourier 级数法给出平均 SEP（QPSK, $M=4$）：

$$P_s = \frac{3}{4} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

**推导逻辑**：
1. AWGN 相位 PDF → Fourier 展开（系数 $a_n(\gamma)$）
2. 对 GG 信道取平均 → $b_n^{GG}$（Meijer-G 闭合形式）
3. 总相位 PDF = AWGN 相位 $\ast$ 载波相位误差（卷积）
4. Fourier 域：系数相乘 $b_n \cdot c_n$
5. SEP = $1 - \int_{-\pi/4}^{\pi/4} f_{total}(\psi) d\psi$ → 级数求和

**$\sin(n\pi/4)$ 模式**（周期 8）：

| n mod 8 | $\sin(n\pi/4)$ |
|---------|----------------|
| 1 | $\sqrt{2}/2$ |
| 2 | 1 |
| 3 | $\sqrt{2}/2$ |
| 4 | 0 |
| 5 | $-\sqrt{2}/2$ |
| 6 | -1 |
| 7 | $-\sqrt{2}/2$ |
| 0 | 0 |

仅 $n \not\equiv 0 \pmod{4}$ 的项贡献非零值。

#### 3.5 从 SEP 到 BER

**标准近似**：$P_b \approx P_s / 2$（Gray coding，相邻符号错误翻转 1 bit）

$$P_b \approx \frac{3}{8} - \sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

**精度**：中等-高 SNR 下偏差 <10%（MC 验证 median 6.0%）。低 SNR 下对角错误（2 bit 翻转）贡献增大，近似偏差变大。

#### 3.6 精确 BER（I/Q 通道分别积分）

P_s/2 近似在高 SNR 下精确，但低 SNR 下低估 BER（忽略对角错误 2 bit 翻转）。精确推导：

**I 通道错误概率**（以符号 π/4 为例）：
$$P_I = P(\cos(\pi/4 + \psi) < 0) = 1 - \int_{-3\pi/4}^{\pi/4} f_{total}(\psi) \, d\psi$$

利用 Fourier 展开：
$$P_I = \frac{1}{2} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{2} \cos\frac{n\pi}{4}$$

**推导**：$\int_{-3\pi/4}^{\pi/4} \cos(n\psi) d\psi = \frac{1}{n}[\sin(n\pi/4) + \sin(3n\pi/4)] = \frac{2}{n}\sin(n\pi/2)\cos(n\pi/4)$

**Q 通道错误概率**：由 QPSK 星座对称性，$P_Q = P_I$。

**精确 BER**：$P_b = (P_I + P_Q)/2 = P_I$

$$\boxed{P_b^{exact} = \frac{1}{2} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{2} \cos\frac{n\pi}{4}}$$

**与 P_s/2 的区别**：
- P_s/2 近似：$\sin(n\pi/4)$ 加权，偶数 n 有贡献（n=2,6,...）
- 精确公式：$\sin(n\pi/2)\cos(n\pi/4)$ 加权，偶数 n 贡献为零（$\sin(n\pi/2)=0$）

**验证**（MC 仿真，中湍流 σ_φ=10°，500k 符号）：
| 公式 | median 误差 | max 误差 |
|------|-----------|---------|
| P_s/2 近似 | 6.0% | 69.4% |
| 精确 BER | 0.6% | 85.9% |

精确公式在中等-高 SNR（工程关注区域）显著改善，median 误差从 6% 降至 0.6%。

### 4. BER Floor

#### 4.1 直接推导（精确）

当 $\bar\gamma \to \infty$，AWGN 噪声消失，条件 BER 的极限：

$$\lim_{\gamma\to\infty} P_b(\gamma, \phi) = \frac{1}{2}[\mathbb{1}_{\cos(\phi+\pi/4)<0} + \mathbb{1}_{\cos(\phi-\pi/4)<0}]$$

- $\phi \in (-\pi/4, \pi/4)$：两个 cos 均 > 0 → $P_b = 0$
- $\phi \in (\pi/4, 3\pi/4)$：$\cos(\phi+\pi/4) < 0$ → $P_b = 1/2$
- $\phi \in (-3\pi/4, -\pi/4)$：$\cos(\phi-\pi/4) < 0$ → $P_b = 1/2$

$$P_{b,floor} = \frac{1}{2}[P(|\phi| > \pi/4)] = Q\!\left(\frac{\pi}{4\sigma_\phi}\right)$$

**物理含义**：BER floor 完全由 $\sigma_\phi$ 决定，与湍流强度无关。高 SNR 下相位误差是唯一性能瓶颈。

#### 4.2 Fourier 级数验证

高 SNR 时 $b_n \to 1/\pi$：

$$P_{b,floor}^{series} = \frac{3}{8} - \frac{1}{\pi}\sum_{n=1}^{N} \frac{1}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

利用恒等式 $\sum_{n=1}^{\infty} \frac{1}{n}\sin(n\pi/4) = 3\pi/8$（$\sigma_\phi = 0$ 时），得 $P_{b,floor} = 0$（无相位误差无 floor）。

对 $\sigma_\phi \geq 8°$，series 与 $Q(\pi/(4\sigma_\phi))$ 在 5 位有效数字内一致。对更小 $\sigma_\phi$，series 收敛慢但 floor 值极小（无工程意义）。

#### 4.3 关键数值

| $\sigma_\phi$ | $Q(\pi/4\sigma_\phi)$ | 说明 |
|--------------|----------------------|------|
| 5° | 1.13e-19 | 近乎完美 |
| 8° | 9.28e-09 | 优良 |
| 10° | 3.40e-06 | 可接受 |
| 15° | 1.35e-03 | 需改善 |
| 20° | 1.22e-02 | 严重 |

### 5. 中断概率

#### 5.1 定义

$$P_{out} = P(\bar{P}_b(\bar\gamma h, \sigma_\phi) > P_{target})$$

其中 $P_b^{avg}(\gamma, \sigma_\phi) = E_\phi[P_b(\gamma, \phi)]$ 是相位平均 BER。

#### 5.2 阈值 SNR

由于 $P_b^{avg}$ 关于 $\gamma$ 单调递减，存在唯一阈值 $\gamma_{th}$ 满足：

$$P_b^{avg}(\gamma_{th}, \sigma_\phi) = P_{target}$$

对应的信道阈值：

$$h_{th} = \gamma_{th} / \bar\gamma$$

#### 5.3 GG 信道中断概率

$$P_{out} = P(h < h_{th}) = F_{GG}(h_{th})$$

GG 分布的 CDF 闭合形式（Meijer-G）：

$$F_{GG}(h) = \frac{1}{\Gamma(\alpha)\Gamma(\beta)} G_{1,3}^{2,1}\left(\alpha\beta h \,\middle|\, \begin{matrix} 1 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

#### 5.4 无相位误差时的简化

$\sigma_\phi = 0$ 时，$P_b = Q(\sqrt{\gamma})$，阈值 $\gamma_{th} = [Q^{-1}(P_{target})]^2$。

$$P_{out}^{(0)} = F_{GG}\left(\frac{[Q^{-1}(P_{target})]^2}{\bar\gamma}\right)$$

#### 5.5 相位误差对中断概率的影响

相位误差增大 → $\gamma_{th}$ 增大 → $P_{out}$ 增大。

当 $P_{target} < Q(\pi/(4\sigma_\phi))$ 时，$\gamma_{th} = \infty$，$P_{out} = 1$（永远无法达到目标 BER）。这是 BER floor 的另一视角。

#### 5.6 验证结果

阈值 SNR $\gamma_{th}$（数值求解 $P_b^{avg}(\gamma_{th}, \sigma_\phi) = 10^{-3}$）：

| $\sigma_\phi$ | $\gamma_{th}$ (dB) | SNR 惩罚 | 备注 |
|--------------|-------------------|---------|------|
| 0° | 9.8 | 0 dB | 基准（$Q^{-1}(10^{-3})^2$） |
| 5° | 10.2 | +0.4 dB | 轻微 |
| 10° | 12.0 | +2.2 dB | 显著 |
| 15° | $\infty$ | — | Floor $1.35\times10^{-3}$ > $10^{-3}$，永远无法达标 |

### 6. $\sigma_\phi$ 与环路参数的关系（Ch3→Ch4 衔接）

BER floor $Q(\pi/(4\sigma_\phi))$ 为 Ch4 载波同步提供了**设计目标**：

$$Q\!\left(\frac{\pi}{4\sigma_\phi}\right) \leq P_{target} \implies \sigma_\phi \leq \frac{\pi}{4 Q^{-1}(P_{target})}$$

| $P_{target}$ | $\sigma_\phi$ 上限 | 对应角度 |
|-------------|------------------|---------|
| $10^{-3}$ | 0.318 rad | 18.2° |
| $10^{-4}$ | 0.210 rad | 12.0° |
| $10^{-5}$ | 0.158 rad | 9.1° |
| $10^{-6}$ | 0.127 rad | 7.3° |

**Ch4 的任务**：设计载波同步算法使得 $\sigma_\phi$ 满足上述约束。具体关系：

- **DPLL**：$\sigma_\phi^2 \approx B_L T_s / (2\bar\gamma h)$（线性化模型）
- **VV-CPR**：$\sigma_\phi^2 \approx 1/(2M\bar\gamma h)$（$M$ = 窗口长度）

## 决策引用

- D001：方向 G 确认（S001）
- D002：选择 Fourier 级数法（非 Hu 的 erfc 展开法），理由：$b_n^{GG}$ 已有闭合形式（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（方向 G 的核心推导工作）

## 后续

- ~~精确 BER 公式验证~~ ✓（I/Q 通道积分，median 误差 0.6%）
- ~~中断概率仿真验证~~ ✓（γ_th 数值求解 + GG CDF）
- $\sigma_\phi$ 与 $B_L$ 关系链建立（Ch3→Ch4 衔接，需读 formulas-ch3ch4-sync.md）
- 更新 thesis-framework.md Ch3 部分
- 更新开题报告 Ch3 内容

---

## 加强计划（S002 续接）

> 2026-05-30 | 加强阶段 | 已完成

### 问题诊断

当前贡献偏薄：GG 是 Málaga ρ=0 特例，高斯相位是 Tikhonov 简化版。需要加强使 Ch3 不只是"参数替换"。

### 加强 1：分湍流设计准则 ✓

基于中断概率的设计表（$P_{out} = 1\%$, $P_{BER} = 10^{-4}$）：

| 湍流 | SNR(σ_φ=0°) | SNR(σ_φ=5°) | SNR(σ_φ=10°) | 惩罚@10° |
|------|-------------|-------------|--------------|----------|
| 弱 | 22.2 dB | 22.8 dB | 26.2 dB | +4.0 dB |
| 中 | 26.9 dB | 27.4 dB | 30.9 dB | +4.0 dB |
| 强 | 39.6 dB | 40.1 dB | 43.6 dB | +4.0 dB |

**物理发现**：σ_φ 导致的 SNR 惩罚与湍流强度无关（均为 +4.0 dB @ σ_φ=10°）。湍流影响的是绝对 SNR 需求（弱→强差 17.4 dB），但相位误差惩罚是通用的。

不可达边界：σ_φ > 12.1° 时 BER floor > 10⁻⁴，任何 SNR 均无法达标。

### 加强 2：信道估计误差鲁棒性分析 ✓

**模型**：$\hat{h} = h(1+\epsilon)$，$\epsilon \sim \mathcal{N}(0, \text{NMSE})$，DPLL 带宽 $B_L = B_0 \hat{h}$，VV 窗口 $M = K_M(\bar\gamma \hat{h}^2)^{-1/5}$

**关键发现**：DPLL 自适应带宽使 $\sigma_\phi^2$ 与 $h$ 无关（$B_L \propto h$ 与 $\gamma \propto h$ 精确抵消），因此估计误差对平均 BER 的影响可忽略（ratio = 1.000 at NMSE = -5 dB）。

这是一个**正面结果**：自适应载波同步对信道估计误差天然鲁棒，不需要额外的估计精度约束。

**对论文的意义**：Ch3 的"估计误差影响"改为"估计误差鲁棒性证明"——解释了为什么 Ch4 的自适应算法在 Ch2 估计不完美时仍能正常工作（与 sim_cascade_robustness.py 的 6/6 PASS 一致）。

### 加强 3：GG vs EGG 对比 — 砍掉

物理场景不同（EGG 建模指向误差+湍流，GG 纯湍流），不可比。

### 交叉验证结果

**GG CDF Meijer-G vs 数值积分**（12 个测试点，3 湍流 × 4 h 值）：
- 最大相对误差：4.39×10⁻⁹（中湍流 h=0.01）
- **结论：Meijer-G CDF 实现正确**

**SNR 惩罚湍流无关性**（9 组条件：3 P_target × 3 P_out_target，σ_φ=10°）：
- spread = 0.0000 对所有 9 组
- 惩罚值：P_target=10⁻³ → 2.18 dB，10⁻⁴ → 4.04 dB，10⁻⁵ → 6.84 dB
- **结论：代数恒等式被数值完美确认**

**风险清单**：

| 风险项 | 严重度 | 状态 |
|--------|--------|------|
| Meijer-G 参数序错误 | 高 | ✓ 已排除（CDF < 10⁻⁸） |
| b_n Meijer-G 错误 | 高 | ✓ 已排除（b_n → 1/π） |
| SNR 惩罚无关是巧合 | 中 | ✓ 已排除（9 组 spread=0） |
| γ=γ̄·h 模型假设 | 低 | ✓ 文献零争议（Ansari-Alouini 统一框架） |
| 线性化 DPLL 模型局限 | 中 | clip 区域内不成立，论文讨论 |
| "估计误差无影响"过于简化 | 中 | 模型内正确，注明适用范围 |

### 多角度文献审查（H002 执行）

3 个子 agent 并行检索 6 个角度，结论汇总：

| 角度 | 风险 | 核心发现 |
|------|------|---------|
| 1 重复工作 | 中 | 无精确重复。Petkovic 2023 方法相似但场景不同（Málaga+Tikhonov vs GG+Gaussian，SEP vs BER） |
| 2 SNR模型 γ∝h | 低 | 教科书标准。Colavolpe 等明确推导 coherent γ∝h vs IM/DD γ∝h²；Ansari-Alouini 参数 r=1/r=2 统一框架 |
| 3 Fourier 级数法 | 中 | 小众方法，Petkovic 2023 几乎无后续引用。主流是 Meijer-G 直接积分。**不应作为核心创新**，仅作为工具 |
| 4 BER floor Q(π/4σ_φ) | 低-中 | RF 领域经典结果（Proakis 教材、IET 1995/2020）。**不可声称新颖**，应强调 FSO 场景特殊性 |
| 5 B_L∝h 抵消 | 低 | 未见于 FSO 文献，但代数消元"显而易见"。**定位为设计洞察而非理论创新** |
| 6 中断概率+相位误差联合框架 | 低 | **明确新颖**——所有先前工作（Chen 2024, Shishter 2024, Niu 2024, Yang 2024）均不含相位同步损伤。**应作为核心贡献** |

**贡献重新定位建议**：
1. 核心贡献 = 联合分析框架（GG 湍流 + 载波相位误差 → BER 闭合解 + 中断概率），非单一公式
2. Fourier 级数法 = 工具（与 Petkovic 2023 区别：GG 非特例、Gaussian 非 Tikhonov、BER 非 SEP）
3. BER floor = 经典结果在 FSO 场景的应用（重点：湍流使 floor 更难达到，SNR 需求与 floor 的关系）
4. B_L∝h 抵消 = 设计洞察（Ch4 自适应算法鲁棒性的理论支撑）
5. 需引用 Petkovic 2023 并显式区分，避免审稿人认为"只是参数替换"