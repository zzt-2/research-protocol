# Ch4 KF 统一载波同步 — 公式推导

> 2026-05-31 | 湍流感知 Kalman 滤波载波同步算法推导
> 与 formulas-ch3ch4-sync.md 衔接，公式编号续 F4.10

---

## 1 信号模型回顾

接收信号（F3.1 / F4.1）：

$$r[k] = \sqrt{h[k]} \cdot s[k] \cdot e^{j\phi[k]} + n[k]$$

- $s[k] \in \{(\pm 1 \pm j)/\sqrt{2}\}$：QPSK 符号
- $h[k]$：GG 湍流信道增益（块衰落，块长 $N_{block}$ = 100 符号）
- $\phi[k] = 2\pi f_{res} kT_s + \pi \dot{f}_D (kT_s)^2 + \theta_L[k]$：载波相位
- $n[k] \sim \mathcal{CN}(0, \sigma^2)$，$\sigma^2 = 1/\gamma_{avg}$

瞬时 SNR（F3.5，相干检测约定）：

$$\gamma[k] = \gamma_{avg} \cdot h[k]$$

---

## 2 KF 状态空间模型

### F4.K1 状态向量定义

$$\mathbf{x}[k] = \begin{bmatrix} \phi[k] \\ \Delta f[k] \end{bmatrix}$$

- $\phi[k]$：载波相位（rad）
- $\Delta f[k]$：瞬时频偏（Hz），包含 Doppler 残余 + 激光频漂

### F4.K2 状态转移方程

$$\mathbf{x}[k+1] = \mathbf{F} \cdot \mathbf{x}[k] + \mathbf{w}[k]$$

$$\mathbf{F} = \begin{bmatrix} 1 & T_s \\ 0 & 1 \end{bmatrix}$$

$$\mathbf{w}[k] \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$$

展开形式：

$$\phi[k+1] = \phi[k] + \Delta f[k] \cdot T_s + w_\phi[k]$$
$$\Delta f[k+1] = \Delta f[k] + w_{\Delta f}[k]$$

物理含义：相位按当前频偏线性累积，频偏自身做随机游走（Doppler 率不确定性 + 激光频漂）。

### F4.K3 观测方程（QPSK 判决导引）

QPSK 四次方去调制后提取相位观测：

$$\hat{s}[k] = \text{decide}(r[k] \cdot e^{-j\hat{\phi}[k|k-1]})$$

$$y[k] = r[k] \cdot \hat{s}^*[k] = \sqrt{h[k]} \cdot e^{j\phi[k]} + n'[k]$$

$$z[k] = \arg(y[k])$$

线性化观测：

$$z[k] = \mathbf{H} \cdot \mathbf{x}[k] + v[k], \quad \mathbf{H} = [1, \; 0]$$

$$v[k] \sim \mathcal{N}(0, R[k])$$

### F4.K4 观测噪声方差

在判决正确的假设下，相位观测噪声方差近似为：

$$R[k] = \frac{1}{2 \gamma_{avg} \cdot h[k]}$$

**关键特性**：$R[k]$ 随瞬时信道增益 $h[k]$ 自适应变化：
- $h[k]$ 大（强信号）→ $R[k]$ 小 → KF 信任观测 → 等效大带宽快速跟踪
- $h[k]$ 小（深衰落）→ $R[k]$ 大 → KF 信任预测 → 等效小带宽抑制噪声

这正是 KF 对比固定参数 DPLL 的核心优势来源——无需显式设计自适应带宽，KF 通过 R 矩阵自然实现。

---

## 3 湍流感知 Q 矩阵设计

### F4.K5 过程噪声协方差结构

$$\mathbf{Q} = \begin{bmatrix} \sigma^2_\phi & 0 \\ 0 & \sigma^2_{\Delta f} \end{bmatrix}$$

### F4.K6 相位过程噪声方差

$$\sigma^2_\phi = \sigma^2_{L} + \sigma^2_{turb}(\alpha, \beta)$$

**激光相位噪声项**：

$$\sigma^2_{L} = 2\pi \cdot \Delta\nu_L \cdot T_s$$

$\Delta\nu_L = 10$ kHz, $T_s = 0.4$ ns → $\sigma^2_L = 2\pi \times 10^4 \times 4 \times 10^{-10} \approx 2.51 \times 10^{-5}$ rad²

**湍流相位噪声项**（GG 矩匹配推导）：

GG 分布的矩：

$$E[h] = 1, \quad \text{Var}[h] = \frac{1}{\alpha} + \frac{1}{\beta} + \frac{1}{\alpha\beta}$$

湍流引起的相位方差与幅度方差的关系（Kolmogorov 模型下对数振幅-相位耦合）：

$$\sigma^2_{turb} = \kappa \cdot \text{Var}[h]$$

其中 $\kappa$ 为幅度-相位耦合系数，取决于传播参数。在 Rytov 近似下，对数振幅方差 $\sigma^2_{\ln I}$ 与相位方差通过结构函数常数 $C_n^2$ 和传播路径 $L$ 关联：

$$\sigma^2_{turb} \approx C_{ph} \cdot D/r_0$$

$D$ 为接收孔径，$r_0$ 为 Fried 参数。对于弱湍流 $D/r_0 < 1$，强湍流 $D/r_0 > 1$。

**简化实用设计**：基于 GG 参数直接设定 $\sigma^2_{turb}$：

| 湍流强度 | $(\alpha, \beta)$ | $\text{Var}[h]$ | $\sigma^2_{turb}$ (rad²/symbol) |
|----------|-------------------|-----------------|--------------------------------|
| 弱 | (4.0, 3.0) | 0.64 | $10^{-6}$ |
| 中 | (2.5, 1.8) | 1.02 | $10^{-4}$ |
| 强 | (1.5, 0.8) | 2.64 | $10^{-3}$ |

注：具体数值需通过仿真标定（拟合 KF 最优 Q 的网格搜索结果）。

### F4.K7 频偏过程噪声方差

$$\sigma^2_{\Delta f} = \frac{(\dot{f}_{max} \cdot T_s)^2}{3}$$

$\dot{f}_{max} = 150$ MHz/s（低仰角 LEO），$T_s = 0.4$ ns：

$$\sigma^2_{\Delta f} = \frac{(150 \times 10^6 \times 4 \times 10^{-10})^2}{3} = \frac{(0.06)^2}{3} = 1.2 \times 10^{-3} \text{ Hz}^2$$

---

## 4 Kalman 滤波递推方程

### F4.K8 预测步

$$\hat{\mathbf{x}}[k|k-1] = \mathbf{F} \cdot \hat{\mathbf{x}}[k-1|k-1]$$

$$\mathbf{P}[k|k-1] = \mathbf{F} \cdot \mathbf{P}[k-1|k-1] \cdot \mathbf{F}^T + \mathbf{Q}$$

### F4.K9 更新步

**创新（残差）**：

$$\tilde{z}[k] = z[k] - \mathbf{H} \cdot \hat{\mathbf{x}}[k|k-1]$$

**创新协方差**：

$$\mathbf{S}[k] = \mathbf{H} \cdot \mathbf{P}[k|k-1] \cdot \mathbf{H}^T + R[k]$$

**Kalman 增益**：

$$\mathbf{K}[k] = \mathbf{P}[k|k-1] \cdot \mathbf{H}^T / \mathbf{S}[k]$$

**状态更新**：

$$\hat{\mathbf{x}}[k|k] = \hat{\mathbf{x}}[k|k-1] + \mathbf{K}[k] \cdot \tilde{z}[k]$$

**协方差更新**：

$$\mathbf{P}[k|k] = (\mathbf{I} - \mathbf{K}[k] \cdot \mathbf{H}) \cdot \mathbf{P}[k|k-1]$$

### F4.K10 等效环路带宽

KF 的等效单边环路带宽（与 DPLL 的 $B_L$ 对比）：

$$B_{L,KF} \approx \frac{K_\phi}{2 T_s}$$

其中 $K_\phi$ 是 Kalman 增益的相位分量（$\mathbf{K}[k]$ 的第一个元素）。当 $R[k]$ 大（深衰落）时 $K_\phi$ 小 → $B_{L,KF}$ 小（窄带宽）；当 $R[k]$ 小时 $K_\phi$ 大 → $B_{L,KF}$ 大（宽带宽）。

---

## 5 初始化

### F4.K11 初始状态

$$\hat{\mathbf{x}}[0|0] = \begin{bmatrix} \hat{\phi}_0 \\ \hat{\Delta f}_0 \end{bmatrix}$$

- $\hat{\Delta f}_0$：由 FFT-FOE 粗估计提供（F4.4）
- $\hat{\phi}_0$：由 VV 前几个符号或首个导频符号提供

### F4.K12 初始协方差

$$\mathbf{P}[0|0] = \begin{bmatrix} \sigma^2_{\phi,init} & 0 \\ 0 & \sigma^2_{\Delta f,init} \end{bmatrix}$$

- $\sigma^2_{\phi,init} = (2\pi)^2 / 16$（相位不确定度覆盖 QPSK 判决区域）
- $\sigma^2_{\Delta f,init} = (\Delta f_{max})^2$（频偏不确定度覆盖 FFT 分辨率范围）

---

## 6 与 Ch3 的衔接

### F4.K13 σ_φ 准则 → Q 矩阵映射

Ch3 导出的设计准则（F3.xx）：

$$\sigma_\phi < \sigma_{\phi,max}(\text{湍流强度}) \quad \text{以保证 } P_{out} < 10^{-5}$$

在 KF 框架中，稳态跟踪误差 $\sigma_{\phi,KF}$ 由 Q/R 的比值决定：

$$\sigma^2_{\phi,KF} \approx \sqrt{\sigma^2_\phi \cdot R_{avg}}$$

设计约束变为：

$$\sqrt{\sigma^2_\phi \cdot \frac{1}{2\gamma_{avg} \cdot E[h]}} < \sigma_{\phi,max}$$

由此可反推 $\sigma^2_\phi$ 的上界，指导 Q 矩阵中湍流项 $\sigma^2_{turb}$ 的设计。

---

## 7 符号汇总

| 符号 | 含义 | 典型值 |
|------|------|--------|
| $T_s$ | 符号周期 | 0.4 ns |
| $\gamma_{avg}$ | 平均 SNR | 10-30 dB |
| $\Delta\nu_L$ | 激光线宽 | 10 kHz |
| $\dot{f}_{max}$ | Doppler 率 | 150 MHz/s |
| $N_{block}$ | 块衰落块长 | 100 符号 |
| $\kappa$ | 幅度-相位耦合系数 | 仿真标定 |
| $\alpha, \beta$ | GG 分布参数 | (4,3)/(2.5,1.8)/(1.5,0.8) |
