<!-- maturity: accumulation -->
# 学位论文公式推导

> 创建: 2026-05-31 | 与 TERMS.md 符号约定保持一致
> 来源: formulas-ch2-system-model.md + formulas-ch3-link-performance.md + formulas-ch3ch4-sync.md + S002 推导
> 公式总计: Ch2 36条 + 2推导 | Ch3 21条（其中 F3.4-F3.17 归档为旧方向）| Ch4 14条 | Ch5 28条
> 最近更新: 2026-06-01 Ch3/Ch4 章节结构同步 thesis-framework v2

---

## 质量检查清单

- [x] 每个公式有来源标注（引用/自推/教科书）
- [x] 自推公式有验证方式（代码行号/数值对比）
- [x] VV 公式是修正版: unwrap(angle)/M（F4.8 标注旧版错误）
- [x] ω_n 单位统一为 rad/s（TERMS.md §4.4 确认）
- [x] h 是实值归一化辐照度（不是复信道系数）
- [x] 无符号冲突（对照 TERMS.md §10 + symbol-conventions.md §13）
- [x] Ch2 符号消歧已执行：R→𝓡（F4-F16）、K→k_B（F14）、h→h_P（F16）、T→T_K（F14）、α/β→σ_a/σ_s（F18）、L→d_link（F28/F33）、h(海拔)→z（F30/F31）、P_e→P_b（F8/F9）
- [x] Ch5 局部消歧已执行：F5.7 X/Y 蝶形、F5.15 α/β BCPE、F5.18 N_iter 注册
- [x] Ch3→Ch4 衔接: σ_φ 设计目标在 F3.18，DPLL/VV 关系在 F4.7-F4.10
- [x] Ch5 FPGA 公式已补充（28 条，F5.1-F5.28）：定点量化 5 条 + FOE 模块 8 条 + CPE 模块 4 条 + CORDIC/NCO 4 条 + 资源/时序 7 条
- [x] Ch4 交叉验证 2 个 HIGH 已修：(1) ω_n=B_L/0.53 统一 12 个 .py 文件 (2) VV 修正版 unwrap(angle)/M 统一 10 个 .py 文件

---

## 第二章 星地激光通信系统与信道模型

### §2.2 星地激光通信系统模型

#### §2.2.1 相干检测系统组成

#### F1: 接收信号光场表示

$$E_s = \mathbf{p}_s A_s \exp[-i(\omega_s t + \varphi_s)]$$

- **来源**: [引用: 张岱2018 式(2.1)]
- **变量**: E_s → TERMS §10.1 信号光场; A_s → TERMS §10.1 信号光振幅; ω_s → TERMS §10.1 信号载波角频率; ω_LO → TERMS §10.1 本振角频率; p_s = 信号光偏振方向单位矢量; φ_s = 信号光相位
- **验证**: 标准教科书公式
- **适用条件**: 接收信号光为平面波近似
- **章节**: §2.2.1

#### F2: 本振光场表示

$$E_{LO} = \mathbf{p}_{LO} A_{LO} \exp[-i(\omega_{LO} t + \varphi_{LO})]$$

- **来源**: [引用: 张岱2018 式(2.2)]
- **变量**: E_LO → TERMS §10.1 本振光场; A_LO → TERMS §10.1 本振光振幅; ω_LO → TERMS §10.1 本振角频率; p_LO = 本振光偏振方向单位矢量; φ_LO = 本振光相位
- **验证**: 标准教科书公式
- **适用条件**: 本振光为单色平面波
- **章节**: §2.2.1

#### F3: 相干混频光功率

$$P = K\int_U (A_s^2 + A_{LO}^2) dU + 2K\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \cos[\omega_{IF}t + \Delta\varphi(x,y,t)] dU$$

- **来源**: [引用: 张岱2018 式(2.3)]
- **变量**: A_s → TERMS §10.1; A_LO → TERMS §10.1; ω_IF → TERMS §10.1 中频角频率; U = 探测器面积; K = 比例常数; p_s · p_LO = 偏振方向偏差内积; Δφ = 信号光与本振光相位差
- **验证**: 标准教科书公式（光学相干检测基本原理）
- **适用条件**: 两束光在探测器面积 U 上相干叠加；ω_IF=0 为零差，否则为外差
- **章节**: §2.2.1

#### F4: 90°混频器输出（I/Q 信号）

$$E_1 = \frac{1}{2}(E_{rx} + E_{LOx}/\sqrt{2}), \quad E_2 = \frac{1}{2}(E_{rx} - E_{LOx}/\sqrt{2})$$

$$E_3 = \frac{1}{2}(E_{rx} + i \cdot E_{LOx}/\sqrt{2}), \quad E_4 = \frac{1}{2}(E_{rx} - i \cdot E_{LOx}/\sqrt{2})$$

$$I_I(t) = \mathcal{R} \cdot \sqrt{P_{LO} P_{t,V}} \cos(2\pi\Delta f t + \Delta\theta(t))$$

$$I_Q(t) = \mathcal{R} \cdot \sqrt{P_{LO} P_{t,V}} \sin(2\pi\Delta f t + \Delta\theta(t))$$

- **来源**: [引用: 闫佳欣式(2-1)~(2-3); R→𝓡 按 §13 消歧策略]
- **变量**: I_I(t) → TERMS §10.1 同相分量; I_Q(t) → TERMS §10.1 正交分量; P_LO → TERMS §10.1 本振光功率; 𝓡 → TERMS §10.2 探测器响应度; Δf = 频偏; Δθ(t) = 相位噪声
- **验证**: 标准教科书公式（90°光混频器原理）
- **适用条件**: 理想 90°光混频器 + 平衡探测器
- **章节**: §2.2.1

#### F5: 理想接收信号光表达式

$$E_{rx} = \sqrt{P_t} \exp[j(2\pi f_0 t + \theta(t))] \exp(j\pi e_{vI})$$

$$E_{ry} = \sqrt{P_t} \exp[j(2\pi f_0 t + \theta(t))] \exp(j\pi e_{vQ})$$

- **来源**: [引用: 闫佳欣式(2-4)]
- **变量**: P_t → TERMS §10.1 发射光功率; f_0 = 光载频; e_{vI}, e_{vQ} = I/Q 路调制数据
- **验证**: 标准教科书公式
- **适用条件**: 理想情况（无频偏无相噪），双偏振 QPSK 信号
- **章节**: §2.2.1

#### F6: 实际 I/Q 输出（含频偏和相噪）

$$I_I(t) = \mathcal{R}\sqrt{P_{LO}P_{t,V}}[\cos(2\pi\Delta f t + \Delta\theta(t))\cos(\pi e_{vI}) - \sin(2\pi\Delta f t + \Delta\theta(t))\cos(\pi e_{vQ})]$$

$$I_Q(t) = \mathcal{R}\sqrt{P_{LO}P_{t,V}}[\sin(2\pi\Delta f t + \Delta\theta(t))\cos(\pi e_{vI}) + \cos(2\pi\Delta f t + \Delta\theta(t))\cos(\pi e_{vQ})]$$

- **来源**: [引用: 闫佳欣式(2-6)(2-7); R→𝓡 按 §13]
- **变量**: I_I(t) → TERMS §10.1; I_Q(t) → TERMS §10.1; 𝓡 → TERMS §10.2; P_LO → TERMS §10.1; Δf = f_0 − f_LO 频偏; Δθ(t) = 激光线宽导致的相位噪声
- **验证**: 标准推导（由 F4+F5 代入化简）
- **适用条件**: 实际系统存在频偏和相位噪声，需 DSP 补偿
- **章节**: §2.2.1

#### §2.2.2 QPSK 信号模型

#### F7: BPSK 调制信号时域表示

$$s(t) = a_n \cdot g(t-nT_s) \cos(\omega_c t + \varphi_n), \quad a_n \in \{1, -1\}$$

- **来源**: [引用: 张岱2018 式(2.15)]
- **变量**: a_n = 调制数据（±1）; g(t) = 成型脉冲; T_s → TERMS §10.4 符号周期; ω_c = 载波角频率
- **验证**: 标准教科书公式
- **适用条件**: 二进制相移键控，分别用相位 0 和 π 表示 1 和 0
- **章节**: §2.2.2

#### F8: BPSK 误码率

$$P_{b,BPSK} = \frac{1}{2}\text{erfc}(\sqrt{SNR})$$

- **来源**: [引用: 张岱2018 式(2.17); P_e→P_b 统一 BER 符号]
- **变量**: erfc(·) → TERMS §10.6 互补误差函数; SNR = 相干探测输出信噪比
- **验证**: 标准教科书公式（Proakis Ch.5）
- **适用条件**: AWGN 信道下相干解调 BPSK，最佳判决门限
- **章节**: §2.2.2

#### F9: DPSK 误码率

$$P_{b,DPSK} = \frac{1}{2}\exp(-SNR)$$

- **来源**: [引用: 张岱2018 式(2.18); P_e→P_b 统一 BER 符号]
- **变量**: SNR = 相干探测输出信噪比
- **验证**: 标准教科书公式
- **适用条件**: 差分相移键控，利用相邻符号间相位差传递信息
- **章节**: §2.2.2

#### §2.2.3 接收端噪声模型与信噪比定义

#### F10: 零差/外差探测响应电流

$$I_{ZF}(t) = 2\mathcal{R}K\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \cos[\Delta\varphi(x,y,t)] \, dU$$

$$I_{RF}(t) = 2\mathcal{R}K\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \cos[\omega_{IF}t + \Delta\varphi(x,y,t)] \, dU$$

- **来源**: [引用: 张岱2018 式(2.6)~(2.8); r→𝓡 按 §13]
- **变量**: A_s → TERMS §10.1; A_LO → TERMS §10.1; ω_IF → TERMS §10.1; 𝓡 → TERMS §10.2 探测器响应度; U = 探测器面积
- **验证**: 标准教科书公式
- **适用条件**: 零差探测输出基带信号，外差探测输出中频信号（高通滤除直流后）
- **章节**: §2.2.3

#### F11: 信噪比定义

$$SNR = \frac{\langle I^2(t) \rangle}{\sigma^2}$$

$$SNR^0_{ZF} = \frac{4\mathcal{R}^2K^2\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \, dU\right)^2}{\sigma^2}$$

$$SNR^0_{RF} = \frac{2\mathcal{R}^2K^2\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \, dU\right)^2}{\sigma^2}$$

- **来源**: [引用: 张岱2018 式(2.8)~(2.12)]
- **变量**: σ² → TERMS §10.1 噪声方差; A_s → TERMS §10.1; A_LO → TERMS §10.1; ⟨·⟩ → TERMS §10.6 统计期望
- **验证**: 标准教科书公式
- **适用条件**: 噪声主要来源为本振光散粒噪声 + 探测器热噪声；外差比零差低 3 dB
- **章节**: §2.2.3

#### F12: 相干探测效率

$$\eta_{RF} = \frac{\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \cos\Delta\varphi \, dU\right)^2 + \left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \sin\Delta\varphi \, dU\right)^2}{\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \, dU\right)^2}$$

$$\eta_{ZF} = \frac{\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \cos\Delta\varphi \, dU\right)^2}{\left(\int_U \mathbf{p}_s \cdot \mathbf{p}_{LO} A_s A_{LO} \, dU\right)^2}$$

- **来源**: [引用: 张岱2018 式(2.13)~(2.14)]
- **变量**: A_s → TERMS §10.1; A_LO → TERMS §10.1; Δφ = 信号光与本振光相位差
- **验证**: 标准教科书公式
- **适用条件**: 相干探测效率 = 考虑大气信道影响后的输出 SNR / 理想 SNR
- **章节**: §2.2.3

#### F13: 平衡探测输出中频信号功率

$$P_{IF} = 2\mathcal{R}^2 P_S P_{LO}$$

- **来源**: [引用: 王锋式(2.43); R→𝓡 按 §13]
- **变量**: 𝓡 → TERMS §10.2 探测器响应度; P_S = 信号光功率; P_LO → TERMS §10.1 本振光功率
- **验证**: 标准教科书公式
- **适用条件**: 零差探测时 Δω_IF=0 且 Δθ=0；本振光对信号光有放大作用
- **章节**: §2.2.3

#### F14: 散粒噪声 + 热噪声

$$\sigma_{shot}^2 = 2e(i_D + \mathcal{R}(P_S + P_{LO} + P_B))\Delta f$$

$$\sigma_{thermal}^2 = \frac{4k_B T_K \Delta f}{R_L}$$

$$\sigma_{total}^2 = \sigma_{shot}^2 + \sigma_{thermal}^2$$

- **来源**: [引用: 王锋式(2.44)~(2.46); K→k_B 避免 Ch5 冲突，T→T_K 避免 T_s 冲突]
- **变量**: 𝓡 → TERMS §10.2 探测器响应度; P_S = 信号光功率; P_LO → TERMS §10.1; e = 电子电荷; i_D = 暗电流; P_B = 背景光功率; Δf = 噪声带宽; k_B = 玻尔兹曼常数（1.38×10⁻²³ J/K）; T_K = 工作温度（K）; R_L = 负载电阻
- **验证**: 标准教科书公式
- **适用条件**: 散粒噪声与入射光功率成正比，热噪声由负载电阻中电子热运动引起
- **章节**: §2.2.3

#### F15: 相干探测 SNR（王锋版）

$$SNR = \frac{P_{IF}}{\sigma_{total}^2} = \frac{2\mathcal{R}^2 P_S P_{LO}}{2e(i_D + \mathcal{R}(P_S + P_{LO} + P_B))\Delta f + 4k_BT_K\Delta f/R_L}$$

- **来源**: [引用: 王锋式(2.47); R→𝓡, K→k_B, T→T_K 按 §13]
- **变量**: 𝓡 → TERMS §10.2; P_S = 信号光功率; P_LO → TERMS §10.1; η → TERMS §10.2 量子效率
- **验证**: 标准教科书公式；本振功率足够大时 SNR ≈ 𝓡P_S/(eΔf) = ηP_S/(h_PνΔf) 逼近量子极限
- **适用条件**: 散粒噪声极限（本振光功率主导），SNR 仅取决于信号光功率和量子效率
- **章节**: §2.2.3

#### F16: 光电探测器响应度

$$\mathcal{R} = \frac{e\eta}{h_P\nu} = \frac{\eta\lambda}{h_P c/e}$$

- **来源**: [引用: 王锋式(2.42); R→𝓡 按 §13, h→h_P 避免与辐照度混淆]
- **变量**: 𝓡 → TERMS §10.2 探测器响应度; η → TERMS §10.2 量子效率; λ → TERMS §10.2 工作波长; e = 电子电荷; h_P = 普朗克常量（6.626×10⁻³⁴ J·s）; ν = 光频率
- **验证**: 标准教科书公式
- **适用条件**: 每单位光功率产生的光电流，取决于量子效率和工作波长
- **章节**: §2.2.3

---

### §2.3 大气信道传输特性

#### §2.3.1 大气衰减

#### F17: Beer-Lambert 定律（大气透过率）

$$I(H) = I_0 \exp\!\bigl(-(\sigma_a + \sigma_s)\, H \sec\theta\bigr)$$

- **来源**: [引用: 王锋式(2.3); 张岱2018 §2.4.1]
- **变量**: σ_a → TERMS §10.2 大气吸收系数; σ_s → TERMS §10.2 大气散射系数; λ → TERMS §10.2 工作波长; I_0 = 发射光强; I(H) = 接收光强; H = 大气信道垂直高度; θ = 天顶角
- **验证**: 标准教科书公式（大气光学基本定律）
- **适用条件**: 准直光源经大气信道传输的透过率，指数衰减模型
- **章节**: §2.3.1

#### F18: 大气吸收与散射系数分解

$$\sigma_a = \sigma_{a,\text{mol}} + \sigma_{a,\text{ae}}, \quad \sigma_s = \sigma_{s,\text{mol}} + \sigma_{s,\text{ae}}$$

- **来源**: [引用: 王锋式(2.4)~(2.5); 符号按 §13 消歧策略，避免与 GG α,β 冲突]
- **变量**: σ_{a,mol} = 分子吸收系数; σ_{a,ae} = 气溶胶吸收系数; σ_{s,mol} = 分子散射系数; σ_{s,ae} = 气溶胶散射系数
- **验证**: 标准教科书公式
- **适用条件**: 大气衰减为吸收与散射之和，二者分别包含分子和气溶胶四个来源
- **章节**: §2.3.1

#### F19: Rayleigh 散射系数

$$\sigma_{s,\text{Rayleigh}} = C/\lambda^4$$

- **来源**: [引用: 王锋式(2.1)]
- **变量**: λ → TERMS §10.2 工作波长; C = 与散射元密度、退偏振因子相关的常量
- **验证**: 标准教科书公式
- **适用条件**: 散射元直径远小于波长，散射系数与波长四次方成反比
- **章节**: §2.3.1

#### F20: Mie 散射系数（半经验公式）

$$\beta_{Mie} \approx \frac{3.91}{V}\left(\frac{\lambda}{\lambda_0}\right)^{-p}, \quad p = 0.585 V^{1/3}$$

- **来源**: [引用: 王锋式(2.2)]
- **变量**: λ → TERMS §10.2 工作波长; V = 能见度(km); λ_0 = 参考波长(550nm 或 610nm); p = 修正因子
- **验证**: 半经验公式，Kim 模型（FSO 文献通用）
- **适用条件**: 气溶胶粒子尺寸复杂，用能见度表示散射系数；不同天气 p 值不同（浓雾 p=0，晴朗 p=1.3）
- **章节**: §2.3.1

#### F21: Rayleigh 散射相函数

$$P(\theta) = \frac{3}{4}(1 + \cos^2\theta)$$

- **来源**: [引用: 张岱2018 式(2.42)]
- **变量**: θ = 散射角
- **验证**: 标准教科书公式
- **适用条件**: Rayleigh 散射各方向能量分布，前后向对称
- **章节**: §2.3.1

#### F22: Mie 散射相函数

$$P(\theta) = \frac{|S_1(\theta)|^2 + |S_2(\theta)|^2}{2k^2}$$

- **来源**: [引用: 张岱2018 式(2.43)]
- **变量**: k = 激光波数; S_1(θ), S_2(θ) = 复振幅函数（含 Mie 散射参数和角函数）
- **验证**: 标准教科书公式（Mie 散射理论）
- **适用条件**: Mie 散射光强分布无固定模型，主要集中于前向
- **章节**: §2.3.1

#### §2.3.2 大气湍流效应与 Gamma-Gamma 分布模型

#### F23: 大气折射率结构函数（Kolmogorov 2/3 定律）

$$D_n(r) = \langle[n(\mathbf{r}_1+\mathbf{r}) - n(\mathbf{r}_1)]^2\rangle = C_n^2 r^{2/3}, \quad l_0 < r < L_0$$

- **来源**: [引用: 张岱2018 式(2.46); 王锋式(2.8)]
- **变量**: C_n² → TERMS §10.2 折射率结构常数; l_0 → TERMS §10.2 湍流内尺度; L_0 → TERMS §10.2 湍流外尺度; r = 空间两点距离
- **验证**: 标准教科书公式（Kolmogorov 湍流理论核心）
- **适用条件**: 惯性子区 l_0 < r < L_0 内，折射率结构函数服从 2/3 幂律
- **章节**: §2.3.2

#### F24: Kolmogorov 功率谱

$$\Phi_n(\kappa) = 0.033 C_n^2 \kappa^{-11/3}, \quad 2\pi/L_0 < \kappa < 2\pi/l_0$$

- **来源**: [引用: 张岱2018 式(2.49); 王锋式(2.9)]
- **变量**: C_n² → TERMS §10.2; l_0 → TERMS §10.2; L_0 → TERMS §10.2; κ = 空间波数(rad/m)
- **验证**: 标准教科书公式
- **适用条件**: 仅在惯性子区间成立，湍流能量按 −11/3 幂律衰减
- **章节**: §2.3.2

#### F25: Tatarskii 功率谱

$$\Phi_n(\kappa) = 0.033 C_n^2 \kappa^{-11/3} \exp(-\kappa^2/\kappa_m^2), \quad \kappa_m = 5.92/l_0$$

- **来源**: [引用: 王锋式(2.11)]
- **变量**: C_n² → TERMS §10.2; l_0 → TERMS §10.2; κ_m = 5.92/l_0 耗散区临界波数
- **验证**: 标准教科书公式
- **适用条件**: 在 Kolmogorov 谱基础上引入内尺度控制的截断函数，囊括耗散区
- **章节**: §2.3.2

#### F26: Von Karman 功率谱

$$\Phi_n(\kappa) = 0.033 C_n^2 (\kappa^2 + \kappa_0^2)^{-11/6}, \quad \kappa_0 = 2\pi/L_0$$

- **来源**: [引用: 张岱2018 式(2.53); 王锋式(2.12)]
- **变量**: C_n² → TERMS §10.2; L_0 → TERMS §10.2; κ_0 = 2π/L_0
- **验证**: 标准教科书公式
- **适用条件**: 考虑外尺度效应的最简模型，避免原点奇异性
- **章节**: §2.3.2

#### F27: 修正 Von Karman 功率谱（最常用全波数域模型）

$$\Phi_n(\kappa) = 0.033 C_n^2 \frac{\exp(-\kappa^2/\kappa_m^2)}{(\kappa^2 + \kappa_0^2)^{11/6}}, \quad \kappa_0 = \frac{2\pi}{L_0}, \quad \kappa_m = \frac{5.92}{l_0}$$

- **来源**: [引用: 王锋式(2.13)]
- **变量**: C_n² → TERMS §10.2; l_0 → TERMS §10.2; L_0 → TERMS §10.2
- **验证**: 标准教科书公式；仿真中最常用的功率谱模型
- **适用条件**: 同时包含内尺度和外尺度效应；当 l_0→0, L_0→∞ 退化为 Kolmogorov 谱；适用于全波数域
- **章节**: §2.3.2

#### F28: Rytov 方差（平面波）

$$\sigma_R^2 = 1.23 C_n^2 k^{7/6} d_{link}^{11/6}$$

- **来源**: [引用: 王锋式(2.14); 符号 d_link 按 §13 消歧策略]
- **变量**: C_n² → TERMS §10.2; k = 波数; d_link → TERMS §10.2 传播距离
- **验证**: 标准教科书公式
- **适用条件**: 弱湍流条件下 Rytov 求解；σ_R²<1 弱湍流，≈1 中等，>1 强湍流
- **章节**: §2.3.2

#### F29: 闪烁因子

$$\sigma_I^2 = \frac{\langle I^2 \rangle - \langle I \rangle^2}{\langle I \rangle^2}$$

- **来源**: [引用: 王锋式(2.15)]
- **变量**: σ_I² → TERMS §10.2 闪烁指数; ⟨·⟩ → TERMS §10.6 统计期望; I → TERMS §10.2 辐照度
- **验证**: 标准教科书公式
- **适用条件**: 弱湍流时 σ_I² ≈ σ_R²；饱和强湍流时 σ_I² = 1 + 0.86σ_R^{−4/5}
- **章节**: §2.3.2

#### F30: Fried 参数（大气相干长度）

$$r_{0,pw} = \left[0.423 k^2 \sec\theta \int_{z_0}^{z_H} C_n^2(z) \, dz\right]^{-3/5}$$

$$r_{0,sw} = \left[0.423 k^2 \int_{z_0}^{z_H} C_n^2(z) \left(\frac{|z-z_0|}{|z_H-z_0|}\right)^{5/3} dz\right]^{-3/5}$$

- **来源**: [引用: 王锋式(2.16)~(2.17); 符号 z 按 §13 消歧策略，避免与 h(辐照度) 混淆]
- **变量**: r_0 → TERMS §10.2 Fried 参数; C_n² → TERMS §10.2; k = 波数; θ = 天顶角; z_0 = 地面海拔(m); z_H = 传播路径顶端海拔(m)
- **验证**: 标准教科书公式
- **适用条件**: r_0 越大湍流越弱；D/r_0 描述单个望远镜内的相对湍流大小
- **章节**: §2.3.2

#### F31: Hufnagel-Valley (HV) 模型

$$C_n^2(z) = 0.00594(v/27)^2(10^{-5}z)^{10}\exp(-z/1000) + 2.7\times10^{-16}\exp(-z/1500) + A_{HV}\exp(-z/100)$$

- **来源**: [引用: 张岱2018 式(2.55); 王锋式(2.10); 符号 z 按 §13 消歧策略，避免与 h(辐照度) 混淆]
- **变量**: C_n² → TERMS §10.2; z = 海拔高度(m); v = 垂直路径风速(m/s); A_HV = 地面折射率结构常数经验值（典型值 1.7×10⁻¹⁴ m^{−2/3}）
- **验证**: 标准经验模型（大气光学文献通用）
- **适用条件**: 最广泛使用的 C_n² 高度分布模型，适用于预测内陆地区白天的大气条件
- **章节**: §2.3.2

#### F32: Gamma-Gamma 分布模型

$$f(I) = \frac{2(\alpha\beta)^{(\alpha+\beta)/2}}{\Gamma(\alpha)\Gamma(\beta) \bar{I}} \left(\frac{I}{\bar{I}}\right)^{(\alpha+\beta)/2-1} K_{\alpha-\beta}\left(2\sqrt{\frac{\alpha\beta I}{\bar{I}}}\right)$$

- **来源**: [引用: Elfiky 2024 (IEEE TCOMM) §II; 通用 FSO 文献]
- **变量**: f_GG(·) → TERMS §10.2 GG 分布 PDF; I → TERMS §10.2 辐照度; α → TERMS §10.2 GG 大尺度参数; β → TERMS §10.2 GG 小尺度参数; K_ν(·) → TERMS §10.6 第二类修正 Bessel 函数; Γ(·) → TERMS §10.6 Gamma 函数
- **验证**: sim_prototype.py GG 采样验证
- **适用条件**: 适用于从弱到强全范围湍流条件；双参数模型同时包含大尺度和小尺度湍流效应
- **章节**: §2.3.2

#### F33: Gamma-Gamma 参数 α, β 确定（平面波）

$$\alpha = \left[\exp\left(\frac{0.49\sigma_R^2}{(1+0.18d^2+0.56\sigma_R^{12/5})^{7/6}}\right)-1\right]^{-1}$$

$$\beta = \left[\exp\left(\frac{0.51\sigma_R^2}{(1+0.9d^2+0.62d^2\sigma_R^{12/5})^{5/6}}\right)-1\right]^{-1}$$

$$d = \sqrt{kD^2/(4d_{link})}$$

- **来源**: [引用: Andrews & Phillips, "Laser Beam Propagation through Random Media"; 通用 FSO 文献; 符号 d_link 按 §13]
- **变量**: α → TERMS §10.2; β → TERMS §10.2; σ_R² → TERMS §10.2（F28 Rytov 方差）; D → TERMS §10.2 接收孔径直径; d_link → TERMS §10.2 传播距离; k = 波数
- **验证**: sim_prototype.py 三档参数验证（弱/中/强湍流）
- **适用条件**: 平面波近似；将物理湍流参数映射到统计模型分布参数；d 为孔径平滑参数
- **章节**: §2.3.3

#### F33b: Greenwood 频率与湍流闪烁相干时间（时间域模型）

$$f_G = 2.31\,\lambda^{-6/5}\left[\int_0^L C_n^2(h)\,V^{5/3}(h)\,dh\right]^{3/5} \quad \text{(平面波)}$$

$$\tau_c = \frac{1}{2\pi\,f_G} \quad \text{(强度闪烁相干时间)}$$

- **来源**: [Greenwood, D.P. (1977) JOSA 67(3):390-393, f_G 定义]; [Conan, Rousset & Madec (1995) JOSA A 12(7):1559-1570, 时间功率谱转折频率→τ_c=1/(2πf_G)]; [Andrews & Phillips (2005) Laser Beam Propagation through Random Media, SPIE, §10-12]
- **变量**: f_G → Greenwood 频率(Hz); λ → 波长; C_n²(h) → TERMS §10.2 折射率结构常数剖面(F31); V(h) → 横风速度剖面(Bufton 模型); L → 传播路径长度; τ_c → 强度闪烁相干时间(s)
- **验证**: params.py GGTimeParams; common/_gg_time.py 实现; 验证结果 results/cma-fade-divergence/gg_time_validation.json
- **适用条件**: 平面波 Kolmogorov 湍流; τ_c 是强度闪烁相干时间(**非** AO 相位校正时间常数 0.314·r₀/V, Roddier 1999); 与 F3.28/F3.29 AR(1) 时变模型配合(T_coh=τ_c); 典型值 f_G=10-1000Hz, τ_c=0.16-16ms(sat.1553:167 τ_c>1ms; s24248036:872 τ_c 1-100ms)
- **章节**: §2.3.3

#### §2.3.3 Gamma-Gamma 模型参数推导

（参数推导公式见 F33。）

---

### §2.4 星地链路预算分析

#### F34: FSO 链路总信道模型

$$h_{SH} = h_l \cdot h_a$$

$$h_l = \frac{1}{2}(G_T + G_R - A_{FS} - A_{ATM} - L_{loss} - M_S) \quad \text{(dB值，确定性衰减)}$$

- **来源**: [引用: Elfiky 2024 式(Satellite-to-HAP FSO link)]
- **变量**: h_l = 确定性损耗; h_a → TERMS §10.2 归一化辐照度（随机湍流衰落）; G_T = 发射天线增益; G_R = 接收天线增益; A_FS = 自由空间损耗; A_ATM = 大气衰减; L_loss = 镜片损耗; M_S = 系统裕量
- **验证**: 标准链路预算公式
- **适用条件**: FSO 信道由确定性损耗和随机湍流衰落两部分组成
- **章节**: §2.4

#### F35: 接收端电 SNR（FSO 链路）

$$\bar{\gamma}_H = \frac{P_S \eta_{OE}}{N_A N_0} \cdot \bar{h}$$

- **来源**: [引用: Elfiky 2024 式(EGC combined SNR)]
- **变量**: γ̄ → TERMS §10.2 平均 SNR; P_S = 发射光功率; η_OE = 光电转换效率; N_A = 接收孔径数; N_0 = 噪声功率谱密度; h̄ → TERMS §10.2 平均归一化辐照度
- **验证**: 标准链路预算公式
- **适用条件**: N_A 个接收孔径等增益合并后的平均 SNR
- **章节**: §2.4

#### F36: 自由空间损耗

$$A_{FS}(\text{dB}) = 20\log_{10}\left(\frac{4\pi d}{\lambda}\right)$$

- **来源**: [引用: 通用链路预算公式]
- **变量**: d → TERMS §10.2 传播距离; λ → TERMS §10.2 工作波长
- **验证**: 标准教科书公式
- **适用条件**: 光束在自由空间传播的几何扩散损耗；星地距离通常 500~40000 km
- **章节**: §2.4

---

### 参数表汇总

| 参数 | 符号 | 典型值 | 来源 |
|------|------|--------|------|
| 工作波长 | λ | 1550 nm | 王锋、闫佳欣 |
| 大气吸收系数 | σ_a | 与天气/波长相关 | 王锋 |
| 大气散射系数 | σ_s | 与天气/波长相关 | 王锋 |
| 折射率结构常数（地面） | C_n² | 10⁻¹⁶~10⁻¹³ m^{−2/3} | 张岱、王锋 |
| 弱湍流 | C_n² | < 10⁻¹⁶ m^{−2/3} | 张岱 |
| 中等湍流 | C_n² | 10⁻¹⁶~10⁻¹⁴ m^{−2/3} | 张岱 |
| 强湍流 | C_n² | > 10⁻¹⁴ m^{−2/3} | 张岱 |
| HV模型地面值 | A_HV | 1.7×10⁻¹⁴ m^{−2/3} | 张岱 |
| 湍流内尺度 | l_0 | 几 mm ~ 几 cm | 王锋 |
| 湍流外尺度 | L_0 | 几十 m ~ 几百 m | 王锋 |
| Fried 参数 | r_0 | 0.01~0.2 m | 王锋 |
| 探测器响应度 | 𝓡 | ~0.8 A/W (1550nm InGaAs) | 王锋 |
| 量子效率 | η | 0.7~0.9 | 王锋 |
| 星地距离（GEO） | d_link | ~36000 km | 张岱 |
| 星地距离（LEO） | d_link | 500~2000 km | 张岱 |
| 通信速率 | R_b | 1~100 Gbps | 张岱 表2.1 |
| BER 要求 | — | < 10⁻⁵（LCRD项目） | 张岱 |
| 接收孔径 | D | 0.1~2.4 m | 张岱、王锋 |
| 大气窗口衰减 | — | < 0.4 dB/km（0.8/1.06/1.55μm） | 王锋 |

---

### 推导

#### 推导1: E[1/h²] 发散性分析

- **来源**: [自推: 基于 GG PDF 小宗量渐近展开]
- **验证**: 数值积分（截断积分 ε=10⁻⁸ 与解析值一致）
- **适用条件**: GG 分布 min(α,β)>2 时 E[1/h²] 收敛
- **章节**: §2.3.2

**步骤1：积分表达式**

由 F32（Gamma-Gamma PDF，归一化 Ī=1），信道衰落 h 的 PDF 为

$$f(h) = \frac{2(\alpha\beta)^{(\alpha+\beta)/2}}{\Gamma(\alpha)\Gamma(\beta)} \, h^{(\alpha+\beta)/2-1} \, K_{\alpha-\beta}\!\left(2\sqrt{\alpha\beta h}\right), \quad h > 0$$

定义

$$E[h^{-2}] = \int_0^\infty h^{-2}\,f(h)\,dh = \frac{2(\alpha\beta)^{(\alpha+\beta)/2}}{\Gamma(\alpha)\Gamma(\beta)} \int_0^\infty h^{(\alpha+\beta)/2-3}\, K_{\alpha-\beta}\!\left(2\sqrt{\alpha\beta h}\right) dh$$

**步骤2：被积函数在 h→0⁺ 的渐近行为**

利用第二类修正 Bessel 函数的小宗量渐近展开（ν = |α−β| > 0，x → 0⁺）：

$$K_\nu(x) \sim \frac{\Gamma(\nu)}{2}\left(\frac{x}{2}\right)^{-\nu}$$

代入 x = 2√(αβh)：

$$K_{\alpha-\beta}\!\left(2\sqrt{\alpha\beta h}\right) \sim \frac{\Gamma(|\alpha-\beta|)}{2}\,(\alpha\beta h)^{-|\alpha-\beta|/2}$$

因此 GG 分布 PDF 在 h→0⁺ 的渐近行为为

$$f(h) \sim C \cdot h^{(\alpha+\beta)/2-1} \cdot h^{-|\alpha-\beta|/2} = C \cdot h^{\min(\alpha,\beta)-1}$$

被积函数的渐近行为：

$$h^{-2}\,f(h) \sim C \cdot h^{\min(\alpha,\beta)-3}$$

**步骤3：收敛条件**

∫₀^ε h⁻²f(h) dh 在 h=0 附近收敛的充要条件是 min(α,β)−3 > −1，即

$$\boxed{\min(\alpha,\beta) > 2}$$

**步骤4：矩公式交叉验证**

GG 分布的 n 阶矩解析公式为

$$E[h^n] = \frac{\Gamma(\alpha+n)\,\Gamma(\beta+n)}{\Gamma(\alpha)\,\Gamma(\beta)\,(\alpha\beta)^n}$$

令 n=−2，利用 Γ(x+1)=xΓ(x) 化简（当 α>2, β>2 时）：

$$E[h^{-2}] = \frac{(\alpha\beta)^2}{(\alpha-1)(\alpha-2)(\beta-1)(\beta-2)}$$

收敛条件 α>2 且 β>2，即 min(α,β)>2，与步骤3一致。

**步骤5：三档湍流下的具体判断**

| 湍流 | α | β | min(α,β) | E[1/h] | E[1/h²] | 自适应必要性 |
|------|---|---|----------|--------|---------|-------------|
| 弱 | 4.0 | 3.0 | 3.0 | 1.17 | **12.0**（收敛） | 较弱（SNR波动小） |
| 中 | 2.5 | 1.8 | 1.8 | 3.75 | **+∞**（发散） | 强（E[1/h]≈4×退化） |
| 强 | 1.5 | 0.8 | 0.8 | +∞（发散） | **+∞**（发散） | 极强 |

弱湍流解析值：E[h⁻²] = (4×3)²/(3×2×2×1) = 12.0。

E[1/h] 公式：E[1/h] = αβ/((α−1)(β−1))，要求 min(α,β) > 1。强湍流 (1.5, 0.8) 的 β = 0.8 < 1，E[1/h] 发散。

**核心结论**：相干检测系统的 VV 载波相位恢复方差 ∝ E[1/h]。弱/中湍流下 E[1/h] 收敛但值较大（1.17 和 3.75），对应约 0.7 dB 和 5.7 dB 的等效 SNR 损失。强湍流下 E[1/h] 发散。瞬时 SNR 的巨大动态范围使得固定参数设计无法在全范围内优化，从性能退化和动态范围两个角度确立了第四章分湍流设计准则的必要性。

**步骤6：数值验证**

(a) 弱湍流（收敛）：截断积分 ∫_ε^∞ h⁻²f(h) dh 在 ε=10⁻⁸ 时收敛至 12.000，与解析值一致。

(b) 中/强湍流（发散）：截断积分随 ε→0 持续增长，不收敛：

| 截断下限 ε | 中湍流 (2.5, 1.8) | 强湍流 (1.5, 0.8) |
|-----------|-------------------|-------------------|
| 10⁻² | 51.1 | 246 |
| 10⁻⁴ | 330 | 73833 |
| 10⁻⁶ | 1077 | — |
| 10⁻⁸ | 2959 | — |

---

#### 推导2: 链路预算闭合公式

- **来源**: [自推: 综合天线增益、自由空间损耗、大气透过率和湍流衰落]
- **验证**: 数值计算与 sim_prototype.py SNR 范围交叉验证
- **适用条件**: LEO 星地链路，散粒噪声极限下
- **章节**: §2.4

**步骤1：端到端信道模型**

$$h_{\text{total}} = h_l \cdot h$$

其中 h_l 为确定性损耗，h 为归一化辐照度（GG 分布，E[h]=1）。

**步骤2：天线增益**

$$G = \frac{4\pi A_e}{\lambda^2} = \eta\left(\frac{\pi D}{\lambda}\right)^2$$

$$G_t = \eta_t\left(\frac{\pi D_t}{\lambda}\right)^2, \quad G_r = \eta_r\left(\frac{\pi D_r}{\lambda}\right)^2$$

**步骤3：自由空间传播损耗**

$$L_{\text{FS}} = \left(\frac{4\pi d}{\lambda}\right)^2, \quad A_{\text{FS}}(\text{dB}) = 20\log_{10}\frac{4\pi d}{\lambda}$$

**步骤4：星地斜距**

$$d = \sqrt{(R_E+H)^2 - (R_E\cos\theta_{\text{elev}})^2} - R_E\sin\theta_{\text{elev}}$$

其中 R_E = 6371 km。

**步骤5：大气透过率**

$$T_{\text{atm}} = \exp(-\gamma\,d_{\text{atm}})$$

其中 d_atm = H_atm/sin(θ_elev) 为大气斜程路径，H_atm ≈ 20 km。

**步骤6：接收端瞬时 SNR 闭合公式**

$$\boxed{\gamma = \frac{\eta_q\,P_t}{h_P\nu\,R_s} \cdot \left(\frac{\pi D_t D_r}{4d\lambda}\right)^2 \cdot \eta_t\,\eta_r \cdot T_{\text{atm}} \cdot h}$$

**步骤7：典型参数**

| 参数 | 符号 | 数值 | 说明 |
|------|------|------|------|
| 波长 | λ | 1550 nm | 大气窗口 |
| 发射功率 | P_t | 1 W (30 dBm) | LEO FSO 终端 |
| 发射孔径 | D_t | 10 cm | 卫星望远镜 |
| 接收孔径 | D_r | 25 cm | 地面站望远镜 |
| 光学效率 | η_t, η_r | 0.7 | 透镜/反射镜损耗 |
| 量子效率 | η_q | 0.8 | InGaAs @ 1550 nm |
| 卫星高度 | H | 500 km | LEO |
| 大气衰减 | γ | 0.2 dB/km | 晴天 |
| 等效大气高度 | H_atm | 20 km | 标准大气 |
| 指向损耗 | L_pt | 3 dB | ATP 残余 |
| 符号速率 | R_s | 10 GBaud | 高速 FSO |
| 发射增益 | G_t | 106.1 dBi | η=1 理想值 |
| 接收增益 | G_r | 114.1 dBi | η=1 理想值 |

**步骤8：链路预算数值结果**

| 仰角 | 斜距 (km) | FSL (dB) | 大气衰减 (dB) | P_rx (dBm) | 晴空 SNR (dB) |
|------|----------|---------|-------------|-----------|-------------|
| 90° (天顶) | 500.0 | 252.2 | 4.0 | -12.0 | 45.9 |
| 60° | 570.5 | 253.3 | 4.6 | -13.8 | 44.2 |
| 45° | 683.1 | 254.9 | 5.7 | -16.4 | 41.6 |
| 30° | 909.4 | 257.4 | 8.0 | -21.2 | 36.7 |

**步骤9：湍流对瞬时 SNR 的影响**

天顶仰角（晴空 SNR = 45.9 dB）下瞬时 SNR 统计分布：

| 湍流强度 | (α,β) | P1 (dB) | P5 (dB) | P50 (dB) | P(SNR<15dB) |
|---------|-------|---------|---------|----------|-------------|
| 弱 | (4.0, 3.0) | 24.3 | 30.7 | 43.8 | 0.07% |
| 中 | (2.5, 1.8) | 15.0 | 24.4 | 42.3 | 1.01% |
| 强 | (1.5, 0.8) | -10.4 | 7.7 | 38.4 | 9.28% |

中强湍流下瞬时 SNR 剧烈波动：强湍流 1% 最差信道将 SNR 拉至 −10 dB。MVE 代码 sim_prototype.py 的 0~25 dB 范围覆盖了中强湍流深衰落场景，物理合理。

---

### 图表汇总

#### 张岱论文

| 编号 | 内容 | 对应章节 |
|------|------|---------|
| 图3.13 | 星地相干激光通信系统原理图 | §2.2.1 |
| 表2.1 | 不同相干探测体制性能比较 | §2.2.1 |
| 图4.6 | AO 自适应光学系统结构示意图 | §2.2.1 |

#### 王锋论文

| 编号 | 内容 | 对应章节 |
|------|------|---------|
| 图2.6 | 电光调制器结构（相位调制器/MZM/IQ调制器） | §2.2.2 |
| 图2.7 | 180°/90°混频器相干接收机 | §2.2.1 |
| 图2.4 | 不同湍流强度下的湍流相位屏 | §2.3.2 |

#### 闫佳欣论文

| 编号 | 内容 | 对应章节 |
|------|------|---------|
| 图2-1 | 相干光通信系统结构框图 | §2.2.1 |
| 图2-2 | 90°光混频器结构图 | §2.2.1 |

---

## 第三章 大气湍流信道估计技术

> **章节结构说明（2026-06-01 同步 thesis-framework v2）**:
> 本章标题已从"QPSK相干检测链路性能分析"更新为"信道估计技术"。
> 公式与新章节的对应关系：
>
> | 新章节 | 对应公式 | 状态 |
> |--------|---------|------|
> | §3.2 湍流信道估计问题建模 | F3.1-F3.3 | ✅ 系统模型通用 |
> | §3.3 信道估计方法（LS/MMSE/KF/DL） | — | ⚠️ 待补充 |
> | §3.4 估计精度对下游影响分析 | F3.18, F3.21 | ✅ σ_φ设计目标+鲁棒性 |
> | §3.5 仿真结果与分析 | F3.19, F3.20 | ✅ 设计准则 |
> | §3.6 本章小结 | — | 无公式 |
> | BER分析（旧方向，待分配） | F3.4-F3.17 | 见末尾归档区 |
>
> 原 §3.3-§3.6 的 BER 性能分析公式已归档至本章末尾"BER性能分析（旧方向）"区域。

### §3.2 湍流信道估计问题建模

#### F3.1: 接收信号模型（含载波相位误差）

$$r = \sqrt{\gamma} \cdot s \cdot e^{j\phi} + n$$

- **来源**: S002 §1; Petkovic 2023 §II
- **变量**: r → TERMS §10.1 接收信号（复基带）; γ → TERMS §10.2 瞬时SNR; s → TERMS §10.1 发射QPSK符号; φ → TERMS §10.4 载波相位偏移; n → TERMS §10.1 复高斯白噪声
- **验证**: 与 Ch2 F3.1 一致，Ch2 估计 h，Ch3 分析 φ 对性能影响，Ch4 补偿 φ
- **适用条件**: 内差相干检测，SNR 模型 γ = γ̄·h（线性，非 h²）；与 Ch2 E[1/h²] 发散推导中的约定一致
- **章节**: §3.2

#### F3.2: SNR 模型说明 γ = γ̄·h（非 h²）

相干检测中：接收光功率 P_r ∝ h（辐照度），光电转换后信号电流 i ∝ √(P_r·P_LO)，信号功率 i² ∝ P_r ∝ h。因此 SNR ∝ h（线性）。

- h² 模型适用于 IM/DD 直接检测，不适用于相干检测
- 文献支撑：Colavolpe 等推导 coherent γ ∝ h vs IM/DD γ ∝ h²；Ansari-Alouini 统一框架参数 r=1（相干）/ r=2（IM/DD）

- **来源**: S002 §1; Ansari-Alouini 统一框架; H002 确认零争议
- **变量**: h → TERMS §10.2 归一化辐照度; γ → TERMS §10.2 瞬时SNR; γ̄ → TERMS §10.2 平均SNR
- **验证**: 教科书标准，文献零争议
- **适用条件**: 相干检测（内差），不适用于 IM/DD 直接检测
- **章节**: §3.2

#### F3.3: 湍流参数

| 湍流 | α | β | 来源 |
|------|---------|---------|------|
| 弱 | 4.0 | 3.0 | Trinh 2017 |
| 中 | 2.5 | 1.8 | Trinh 2017 |
| 强 | 1.5 | 0.8 | Trinh 2017 |

- **来源**: Trinh 2017; S019 参数统一确认
- **变量**: α → TERMS §10.2 GG大尺度参数; β → TERMS §10.2 GG小尺度参数
- **验证**: 与 sim_prototype.py / sim_direction_a.py 一致
- **适用条件**: Gamma-Gamma 湍流衰落模型
- **章节**: §3.2

---

### §3.3 信道估计方法

#### §3.3.1 LS与MMSE信道估计

#### F3.22: 导频观测模型

$$y_p = \sqrt{h} \cdot x_p + n_p$$

其中 $x_p$ 为已知导频符号，$y_p$ 为导频位置接收信号，$h$ 为归一化辐照度（实值，$E[h]=1$），$\sqrt{h}$ 为信道幅度调制系数，$n_p \sim \mathcal{CN}(0, \sigma_n^2)$ 为复高斯白噪声。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §7.3]; [代码: sim_prototype.py L123-125 `h = rx[pidx] / psym`]
- **变量**: y_p → TERMS §10.3 导频位置接收信号; x_p → TERMS §10.3 导频符号; h → TERMS §10.2 归一化辐照度; n_p → TERMS §10.1 复高斯白噪声; σ_n² → TERMS §10.1 噪声方差
- **验证**: 仿真中 h_eff = √h，rx = awgn(tx * h_eff, snr)，与模型一致
- **适用条件**: 内差相干检测，导频符号已知；√h 为电场幅度调制系数（TERMS §10.2）
- **章节**: §3.3.1

#### F3.23: LS信道估计器

$$\hat{h}_\text{LS} = |y_p / x_p|^2$$

标量形式：将导频位置观测除以已知导频符号，取模平方得到辐照度估计。

复信道估计形式（用于后续载波同步）：

$$\hat{h}_\text{LS,complex} = y_p / x_p$$

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §7.3]; [代码: sim_prototype.py L123-124 `h = rx[pidx] / psym`]
- **变量**: ĥ_LS → TERMS §10.3 LS信道估计; x_p → TERMS §10.3 导频符号; y_p → TERMS §10.3 导频位置接收信号
- **验证**: 仿真代码 `ls_est()` 实现 `h = rx[pidx] / psym`，与公式一致
- **适用条件**: 导频符号已知（$x_p \neq 0$）；不利用信道统计先验信息
- **章节**: §3.3.1

#### F3.24: LS估计误差（NMSE理论值）

$$\text{NMSE}_\text{LS} = \frac{\sigma_n^2}{|x_p|^2 \cdot E[h]}$$

单导频时，LS 估计误差方差为 $\text{Var}(\hat{h}_\text{LS}) = \sigma_n^2 / |x_p|^2$。多导频平均时，误差方差按导频数 $N_p$ 缩小：$\text{Var} = \sigma_n^2 / (N_p |x_p|^2)$。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §7.3]; [教科书: Proakis, Digital Communications, §14.1]
- **变量**: σ_n² → TERMS §10.1 噪声方差; x_p → TERMS §10.3 导频符号; N_p → TERMS §10.5 导频个数
- **验证**: 仿真中 LS NMSE@20dB ≈ -3~-6 dB（弱/强湍流），与理论量级一致
- **适用条件**: 单导频或等间距多导频；噪声独立同分布
- **章节**: §3.3.1

#### F3.25: MMSE信道估计器（LMMSE）

$$\hat{h}_\text{MMSE} = \frac{\sigma_h^2}{\sigma_h^2 + \sigma_n^2 / |x_p|^2} \cdot \hat{h}_\text{LS}$$

其中 $\sigma_h^2 = \text{Var}(h)$ 为信道辐照度方差，缩放系数 $c = \sigma_h^2 / (\sigma_h^2 + \sigma_n^2 / |x_p|^2)$ 将 LS 估计向统计均值收缩：高 SNR 时 $c \to 1$（退化为 LS），低 SNR 时 $c \to 0$（退化为均值估计 $E[h]=1$）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §12.4 LMMSE]; [代码: sim_prototype.py L127-132 `c = vh / (vh + nv) ... hm = c * hls`]
- **变量**: ĥ_MMSE → TERMS §10.3 MMSE信道估计; ĥ_LS → TERMS §10.3 LS信道估计; σ_h² → TERMS §10.3 信道方差; σ_n² → TERMS §10.1 噪声方差
- **验证**: 仿真代码 `mmse_est()` 实现 `vh = np.var(h_true_p); c = vh/(vh+nv); hm = c*hls`，与公式精确一致
- **适用条件**: 信道二阶统计量（σ_h²）已知；LMMSE 仅需信道方差，不要求完整分布信息
- **章节**: §3.3.1

#### F3.26: MMSE估计误差（与LS对比）

$$\text{NMSE}_\text{MMSE} = c \cdot \text{NMSE}_\text{LS} = \frac{\sigma_h^2 \cdot \sigma_n^2 / |x_p|^2}{(\sigma_h^2 + \sigma_n^2 / |x_p|^2)^2}$$

MMSE 估计误差恒小于 LS：$\text{NMSE}_\text{MMSE} / \text{NMSE}_\text{LS} = c < 1$。改善因子为 $c = \sigma_h^2 / (\sigma_h^2 + \sigma_n^2 / |x_p|^2)$，低 SNR 时改善显著（$c \to \sigma_h^2 |x_p|^2 / \sigma_n^2$），高 SNR 时改善消失（$c \to 1$）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §12.4]; [代码: sim_prototype.py L127-132]
- **变量**: c → F3.25 缩放系数; σ_h² → TERMS §10.3 信道方差; σ_n² → TERMS §10.1 噪声方差
- **验证**: 仿真中 MMSE NMSE 恒低于 LS NMSE，与 $c < 1$ 一致
- **适用条件**: 与 F3.25 相同
- **章节**: §3.3.1

#### F3.27: NMSE评价指标定义

$$\text{NMSE} = \frac{E\!\left[|h - \hat{h}|^2\right]}{E\!\left[|h|^2\right]}$$

归一化均方误差：估计误差功率与信道功率之比。NMSE = 0 为理想估计，NMSE = 1 为估计误差与信道功率同量级。仿真中以样本均值替代统计期望。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §6.2]; [代码: sim_prototype.py L53 `def nmse(est, true): return np.mean(np.abs(est-true)**2) / np.mean(np.abs(true)**2)`]
- **变量**: NMSE → TERMS §10.3 归一化均方误差; h → TERMS §10.2 归一化辐照度; ĥ → TERMS §10.3 通用信道估计
- **验证**: 仿真代码 `nmse()` 实现与公式精确一致
- **适用条件**: 通用评价指标，适用于 LS/MMSE/KF/DL 等所有估计方法
- **章节**: §3.3.1

#### §3.3.2 基于卡尔曼滤波的信道估计

#### F3.28: AR(1)信道时变模型

$$\ln h[k] = \rho \cdot \ln h[k-1] + \sqrt{1 - \rho^2} \cdot \sigma_{\ln I} \cdot w[k], \quad w[k] \sim \mathcal{N}(0, 1)$$

其中自相关系数 $\rho = e^{-T_\text{step} / T_\text{coh}}$，$T_\text{coh}$ 为信道相干时间，$T_\text{step}$ 为采样间隔，$\sigma_{\ln I}^2 = \ln(1 + 1/\alpha + 1/\beta)$ 为对数辐照度方差。

归一化保证：$E[h] = 1$ 由中心化 $E[\exp(\sigma_{\ln I}^2/2)]$ 补偿实现（代码中减去 $\sigma_{\ln I}^2/2$）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §13.4 AR models]; [代码: sim_ch3_precomp.py L52-73 `rho = np.exp(-T_step / T_coh)`]
- **变量**: h → TERMS §10.2 归一化辐照度; ρ → TERMS §10.3 AR(1)自相关系数; T_coh → 信道相干时间; σ_lnI → 对数辐照度标准差; α, β → TERMS §10.2 GG参数
- **验证**: 仿真代码 `correlated_fading()` 实现 AR(1) on ln(I)，`rho = exp(-T_step/T_coh)`，与公式一致；TURB 表给出 weak/moderate/strong 的 (α,β,T_coh) 参数
- **适用条件**: 对数正态近似 Gamma-Gamma 信道；ρ ∈ (0,1) 保证因果稳定性；信道相干时间远大于符号周期（$T_\text{coh} \gg T_s$）
- **章节**: §3.3.2

#### F3.29: AR(1)参数与信道相干时间的关系

$$\rho = e^{-T_\text{step} / T_\text{coh}}, \quad T_\text{coh} = \frac{1}{f_D}$$

其中 $f_D$ 为多普勒扩展频率（由卫星运动引起）。$\rho$ 越接近 1 表示信道变化越慢（相干时间越长）。典型参数：

| 湍流 | T_coh | ρ (T_step=0.1ms) |
|------|-------|------------------|
| 弱 | 10 ms | 0.990 |
| 中 | 5 ms | 0.980 |
| 强 | 2 ms | 0.951 |

- **来源**: [教科书: Proakis, Digital Communications, §14.3]; [代码: sim_ch3_precomp.py L34-38 TURB表, L62 `rho = np.exp(-T_step / T_coh)`]
- **变量**: ρ → TERMS §10.3 AR(1)自相关系数; T_coh → 信道相干时间; T_step → 采样间隔; f_D → 多普勒扩展频率
- **验证**: 代码中 weak: T_coh=10ms → ρ=exp(-0.1/10)=0.990; strong: T_coh=2ms → ρ=exp(-0.1/2)=0.951，与表一致
- **适用条件**: AR(1)模型对信道自相关函数的一阶近似；高阶模型（AR(p), p>1）可提高精度
- **章节**: §3.3.2

#### F3.30: 卡尔曼滤波信道估计——状态方程与观测方程

**状态方程**（信道状态演化）：

$$h[k] = \rho \cdot h[k-1] + q[k], \quad q[k] \sim \mathcal{N}(0, Q)$$

**观测方程**（导频观测）：

$$y_p[k] = \sqrt{h[k]} \cdot x_p + n[k], \quad n[k] \sim \mathcal{CN}(0, \sigma_n^2)$$

其中 $Q = (1 - \rho^2) \sigma_h^2$ 为过程噪声方差，由 AR(1) 模型参数决定。

**注意**：观测方程中 $\sqrt{h[k]}$ 为非线性映射。实际实现中可采用对数域线性化（对 $\ln h$ 做 KF）或扩展卡尔曼滤波（EKF）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §13.4]; [代码: sim_ch3_precomp.py L55-69 AR(1)模型]
- **变量**: h → TERMS §10.2 归一化辐照度; ρ → TERMS §10.3 AR(1)自相关系数; Q → TERMS §8 过程噪声协方差; σ_n² → TERMS §10.1 噪声方差; x_p → TERMS §10.3 导频符号
- **验证**: 仿真代码中 AR(1) 生成 `ln_I[i] = rho * ln_I[i-1] + innov[i]`，innov_std = √((1-ρ²)·σ²_ln)，与 Q 定义一致
- **适用条件**: 信道时间相关性可用 AR(1) 建模；过程噪声和观测噪声独立
- **章节**: §3.3.2

#### F3.31: 卡尔曼滤波预测步骤

$$\hat{h}[k|k-1] = \rho \cdot \hat{h}[k-1|k-1]$$

$$P[k|k-1] = \rho^2 \cdot P[k-1|k-1] + Q$$

其中 $\hat{h}[k|k-1]$ 为基于 $k-1$ 时刻估计对 $k$ 时刻的一步预测，$P[k|k-1]$ 为预测误差方差，$P[k-1|k-1]$ 为上一时刻更新后的误差方差。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §13.4 KF prediction]; [代码: sim_ch4_kf_pilot_h.py L469-470 `x_pred = F_mat @ x; P_pred = F_mat @ P @ F_mat.T + Q_fine`]
- **变量**: ĥ → TERMS §10.3 通用信道估计; P → TERMS §8 误差协方差; ρ → TERMS §10.3 AR(1)自相关系数; Q → TERMS §8 过程噪声协方差
- **验证**: 仿真代码 `P_pred = F_mat @ P @ F_mat.T + Q_fine`，标量退化为 $\rho^2 P + Q$，与公式一致
- **适用条件**: AR(1)状态模型成立；P 的初始值影响收敛速度但不影响稳态精度
- **章节**: §3.3.2

#### F3.32: 卡尔曼滤波更新步骤

**卡尔曼增益**：

$$K[k] = \frac{P[k|k-1]}{P[k|k-1] + R[k]}$$

**状态更新**：

$$\hat{h}[k|k] = \hat{h}[k|k-1] + K[k] \cdot \left(y_p[k] - \sqrt{\hat{h}[k|k-1]} \cdot x_p\right)$$

**误差协方差更新**：

$$P[k|k] = (1 - K[k]) \cdot P[k|k-1]$$

其中 $R[k] = \sigma_n^2 / (2 \bar\gamma \cdot \hat{h}[k|k-1])$ 为等效观测噪声方差（取决于瞬时 SNR），括号内为观测新息（innovation）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §13.4 KF update]; [代码: sim_ch4_kf_pilot_h.py L483-488 `S = H_mat @ P_pred @ H_mat.T + R_val; K_gain = P_pred @ H_mat.T / S; x = x_pred + K_gain.flatten() * innov; P = (np.eye(2) - K_gain @ H_mat) @ P_pred`]
- **变量**: K[k] → 卡尔曼增益; R[k] → TERMS §8 观测噪声协方差; γ̄ → TERMS §10.2 平均SNR; P → TERMS §8 误差协方差
- **验证**: 仿真代码 `K_gain = P_pred @ H_mat.T / S`，其中 `S = P_pred + R_val`，标量退化为 K = P/(P+R)，与公式一致
- **适用条件**: 等效观测噪声方差 R[k] 需要当前信道估计 ĥ 来计算（实际中用预测值 ĥ[k|k-1] 近似）
- **章节**: §3.3.2

#### F3.33: 卡尔曼滤波稳态性能

当 KF 收敛到稳态时，预测误差方差 $P$ 和增益 $K$ 满足 Riccati 方程的稳态解：

$$P_\infty = \frac{-(Q - R + \rho^2 R) + \sqrt{(Q - R + \rho^2 R)^2 + 4 \rho^2 Q R}}{2 \rho^2}$$

稳态卡尔曼增益 $K_\infty = P_\infty / (P_\infty + R)$。高 SNR 时 $R \to 0$，$K_\infty \to 1$（完全信任观测）；低 SNR 时 $R \to \infty$，$K_\infty \to P_\infty / R \to 0$（完全信任预测）。

- **来源**: [教科书: Kay, Fundamentals of Statistical Signal Processing, Vol. I, §13.4 steady-state KF]; [教科书: Anderson & Moore, Optimal Filtering, §4.4]
- **变量**: P_∞ → 稳态误差方差; K_∞ → 稳态卡尔曼增益; Q → TERMS §8 过程噪声协方差; R → TERMS §8 观测噪声协方差; ρ → TERMS §10.3 AR(1)自相关系数
- **验证**: 标量 Riccati 方程的解析解，代入 ρ 和 Q/R 参数可数值验证
- **适用条件**: AR(1)模型参数时不变；初始瞬态衰减后达到稳态
- **章节**: §3.3.2

#### §3.3.3 基于深度学习的信道估计方法

[无公式，方法描述为主]

---

### §3.4 估计精度对下游信号处理的影响分析

#### §3.4.1 估计误差对载波同步性能的影响

#### F3.21: 自适应 DPLL 带宽的鲁棒性

**模型**：ĥ = h(1+ε)，ε ~ N(0, NMSE)

**关键发现**：DPLL 自适应带宽 B_L = B_0·ĥ 使 σ_φ² 与 h 无关（B_L ∝ h 与 γ ∝ h 精确抵消），因此估计误差对平均 BER 的影响可忽略（ratio = 1.000 @ NMSE = -5 dB）。

**物理解释**：载波同步对信道估计误差天然鲁棒——B_L ∝ h 和 γ ∝ h 形成对消，σ_φ 与信道状态无关。

**对论文意义**：解释了为什么 Ch4 载波同步算法在 Ch2 估计不完美时仍能正常工作（与 sim_cascade_robustness.py 6/6 PASS 一致）。

- **文献定位**: H002 确认：未见于 FSO 文献，但代数消元"显而易见"。定位为设计洞察而非理论创新。

- **来源**: [自推: B_L∝h 与 γ∝h 对消分析]; S002 加强 2; sim_ch3_strengthening.py
- **变量**: B_L → TERMS §10.4 环路带宽; h → TERMS §10.2 归一化辐照度; σ_φ → TERMS §10.4 载波相位误差标准差; NMSE → TERMS §10.3 归一化均方误差
- **验证**: sim_ch3_strengthening.py; ratio = 1.000 @ NMSE = -5 dB; sim_cascade_robustness.py 6/6 PASS
- **适用条件**: 自适应 DPLL（B_L = B_0·ĥ）；线性化 DPLL 模型成立范围内
- **章节**: §3.4.1

#### §3.4.2 下游模块灵敏度分析

#### F3.18: 相位误差约束（σ_φ 设计目标，Ch3→Ch4 衔接）

$$Q\!\left(\frac{\pi}{4\sigma_\phi}\right) \leq P_{target} \implies \sigma_\phi \leq \frac{\pi}{4 Q^{-1}(P_{target})}$$

| P_target | σ_φ 上限 | 对应角度 |
|-------------|------------------|---------|
| 10⁻³ | 0.254 rad | 14.6° |
| 10⁻⁴ | 0.211 rad | 12.1° |
| 10⁻⁵ | 0.184 rad | 10.6° |
| 10⁻⁶ | 0.165 rad | 9.5° |

- **数值验证**：σ_{φ,max} = π / (4 · Q⁻¹(P_target))，使用 scipy `norm.ppf(1-P_target)` 精确计算。
- **Ch4 的任务**：设计载波同步算法使得 σ_φ 满足上述约束。具体关系：
  - DPLL：σ_φ² ≈ B_L·T_s / (2γ̄·h)（线性化模型）
  - VV-CPR：σ_φ² ≈ 1/(2M·γ̄·h)（M = VV 平均窗口长度）

- **来源**: [自推: F3.11 取等号反解]; S002 §6; Ch4 formulas F4.7-F4.10
- **变量**: σ_φ → TERMS §10.4 载波相位误差标准差; P_target → 目标BER; Q(·) → TERMS §10.6 Q函数; B_L → TERMS §10.4 环路带宽; T_s → TERMS §10.4 符号周期; M → TERMS §10.4 VV平均窗口长度
- **验证**: scipy `norm.ppf(1-P_target)` 精确计算确认
- **适用条件**: BER floor 约束（F3.11 取等号），Ch4 载波同步算法设计的输入约束
- **章节**: §3.4.2

---

### §3.5 仿真结果与分析

#### §3.5.1 仿真参数设置与评价指标

[待补充] 仿真参数表（符号率、帧长、SNR范围、湍流参数同 F3.3）

#### §3.5.2 各估计方法性能对比

[待补充] LS vs MMSE vs KF vs DL 的 NMSE 对比结果

#### §3.5.3 不同湍流强度下性能分析

[待补充] 弱/中/强湍流下各方法性能

#### §3.5.4 级联灵敏度分析与工程指导

#### F3.19: 分湍流中断概率设计表

基于中断概率的设计表（P_out = 1%, P_BER = 10⁻⁴）：

| 湍流 | SNR(σ_φ=0°) | SNR(σ_φ=5°) | SNR(σ_φ=10°) | 惩罚@10° |
|------|----------------------|----------------------|-----------------------|----------|
| 弱 | 22.2 dB | 22.8 dB | 26.4 dB | +4.2 dB |
| 中 | 26.9 dB | 27.4 dB | 31.1 dB | +4.2 dB |
| 强 | 39.6 dB | 40.1 dB | 43.8 dB | +4.2 dB |

- **数值方法**：γ_th 通过 `scipy.integrate.quad` 精确积分求解（非梯形近似），积分限 ±5σ_φ，容差 10⁻¹²。

- **来源**: S002 加强 1; sim_ch3_strengthening.py
- **变量**: σ_φ → TERMS §10.4 载波相位误差标准差; P_out → TERMS §10.2 中断概率
- **验证**: sim_ch3_strengthening.py; scipy.integrate.quad 精确积分
- **适用条件**: P_out = 1%, P_target = 10⁻⁴; 三种湍流强度
- **章节**: §3.5.4

#### F3.20: SNR 惩罚与湍流无关性

σ_φ 导致的 SNR 惩罚与湍流强度无关（均为 +4.2 dB @ σ_φ=10°, P_target=10⁻⁴）。

- **数值验证**（9 组条件：3 P_target × 3 P_out，σ_φ=10°，精确积分 `scipy.integrate.quad`）：
  - 惩罚值：P_target=10⁻³ → 2.20 dB，10⁻⁴ → 4.21 dB，10⁻⁵ → 8.91 dB
  - 同一 P_target 下不同湍流条件的惩罚差异 < 0.01 dB
  - **结论：SNR 惩罚与湍流无关的代数性质被数值确认**
- 不可达边界：σ_φ > 12.1° 时 BER floor > 10⁻⁴，任何 SNR 均无法达标。

- **来源**: [自推: 数值验证确认]; S002 加强 1; sim_ch3_strengthening.py
- **变量**: σ_φ → TERMS §10.4 载波相位误差标准差; P_target → 目标BER
- **验证**: 9 组条件（3 P_target × 3 湍流），同一 P_target 下惩罚差 < 0.01 dB
- **适用条件**: QPSK 相干检测，GG 湍流信道，SNR 惩罚仅取决于 σ_φ 和 P_target
- **章节**: §3.5.4

---

### §3.6 本章小结

无公式。

---

### BER 性能分析公式（旧方向，待分配至正文具体位置）

> 以下公式属于原 Ch3"QPSK相干检测链路性能分析"方向。方向切换后不再作为 Ch3 主体内容。
> 部分公式可能在 §3.4 级联分析或 Ch4 载波同步分析中作为背景/工具使用。

#### F3.4: QPSK 条件 BER（Gray coding）

$$P_b(\gamma, \phi) = \frac{1}{2}\left[Q(\sqrt{2\gamma}\cos(\phi+\pi/4)) + Q(\sqrt{2\gamma}\cos(\phi-\pi/4))\right]$$

- 因子 1/2：QPSK 每符号 2 bit，BER = 总 bit 错误数 / 总 bit 数
- 无相位误差时（φ=0）：P_b = Q(√γ)（标准 QPSK BER，退化为 Ch2 结果）
- Q(x) = (1/2)erfc(x/√2)

- **来源**: [教科书: Proakis Digital Communications]; S002 §2
- **变量**: P_b → TERMS §10.2 误比特率; γ → TERMS §10.2 瞬时SNR; φ → TERMS §10.4 载波相位偏移; Q(·) → TERMS §10.6 Q函数
- **验证**: φ=0 退化检验：P_b = Q(√γ) 与标准 QPSK BER 一致
- **适用条件**: QPSK 调制，Gray coding 映射，AWGN 信道
- **章节**: 待分配（可能在 §3.4.1 或 Ch4 背景分析）

#### F3.5: AWGN 相位 PDF 的 Fourier 展开

$$f_\psi(\psi|\gamma) = \frac{1}{2\pi} + \sum_{n=1}^{\infty} a_n(\gamma) \cos(n\psi)$$

其中 a_n(γ) 涉及 confluent hypergeometric 函数（Petkovic 2023 Eq.14）。

- **来源**: [引用: Petkovic 2023 §III-A]
- **变量**: γ → TERMS §10.2 瞬时SNR; ψ → AWGN 引起的等效相位误差
- **验证**: Petkovic 2023 原文推导
- **适用条件**: AWGN 信道下的相位条件分布
- **章节**: §3.4

#### F3.6: GG 信道平均 Fourier 系数 b_n^{GG}（Meijer-G 闭合形式）

$$b_n^{GG} = \frac{n}{2\pi\Gamma(\alpha)\Gamma(\beta)} G_{2,3}^{3,1}\left(\frac{\alpha\beta}{\bar\gamma} \,\middle|\, \begin{matrix} 1-n/2, & 1+n/2 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

- GG 是 Málaga 分布 ρ=0 的特例（Petkovic 2023 Eq.19）
- 高 SNR 极限：γ̄ → ∞ 时 b_n^{GG} → 1/π
- **数值验证**（中湍流，S002）：

| SNR | b_1 | b_2 | b_3 | 极限 1/π |
|-----|-------|-------|-------|------------|
| 0 dB | 0.192 | 0.097 | 0.046 | 0.318 |
| 20 dB | 0.315 | 0.308 | 0.297 | 0.318 |
| 40 dB | 0.318 | 0.318 | 0.318 | 0.318 |

- **来源**: [引用: Petkovic 2023 Eq.19]; S002 §3.2
- **变量**: α → TERMS §10.2 GG大尺度参数; β → TERMS §10.2 GG小尺度参数; γ̄ → TERMS §10.2 平均SNR; Γ(·) → TERMS §10.6 Gamma函数; G → TERMS §10.6 Meijer-G函数
- **验证**: sim_ch3_ber_closed_form.py `bn_gg_v2`; Meijer-G 参数序已验证（CDF < 10⁻⁸），S002 交叉确认
- **适用条件**: Gamma-Gamma 湍流衰落模型，GG 为 Málaga 分布 ρ=0 特例
- **章节**: §3.4

#### F3.7: 高斯相位误差的 Fourier 系数

$$c_n^{Gauss} = \frac{1}{\pi}\int_{-\pi}^{\pi} \cos(n\phi) \cdot \frac{e^{-\phi^2/(2\sigma_\phi^2)}}{\sigma_\phi\sqrt{2\pi}} d\phi \approx \frac{1}{\pi} e^{-n^2\sigma_\phi^2/2}$$

- **推导**：高斯函数的 Fourier 变换 ∫_{-∞}^{∞} cos(nφ) e^{-φ²/(2σ²)} dφ = σ√(2π) e^{-n²σ²/2}。当 σ_φ ≪ π（典型值 σ_φ ≤ 15° = 0.26 rad），截断误差可忽略。
- **衰减行为**：c_n 以 exp(-n²σ_φ²/2) 衰减，比 Tikhoniv（Bessel I_n）衰减更快，级数收敛性更好。

- **来源**: [自推: 基于标准 Fourier 分析]; S002 §3.3
- **变量**: σ_φ → TERMS §10.4 载波相位误差标准差; φ → TERMS §10.4 载波相位偏移
- **验证**: σ_φ ≪ π 时截断误差可忽略；与 Tikhonov Bessel I_n 衰减对比
- **适用条件**: 高斯分布相位误差，σ_φ ≪ π（典型值 ≤ 15° = 0.26 rad）
- **章节**: §3.4

#### F3.8: 平均 SEP（Fourier 级数法）

$$P_s = \frac{3}{4} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

- **推导逻辑**：
  1. AWGN 相位 PDF → Fourier 展开（系数 a_n(γ)）
  2. 对 GG 信道取平均 → b_n^{GG}（Meijer-G 闭合形式）
  3. 总相位 PDF = AWGN 相位 ∗ 载波相位误差（卷积）
  4. Fourier 域：系数相乘 b_n · c_n
  5. SEP = 1 − ∫_{-π/4}^{π/4} f_total(ψ) dψ → 级数求和
- **sin(nπ/4) 模式**：周期 8，仅 n ≢ 0 (mod 4) 的项贡献非零值。

- **来源**: [引用: Petkovic 2023 §III-B]; S002 §3.4
- **变量**: P_s → TERMS §10.2 误符号率; b_n^{GG} → F3.6 Fourier系数; σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: H002 文献审查确认此方法小众，定位为工具（非核心创新）
- **适用条件**: Fourier 级数收敛（N 有限项截断）
- **章节**: §3.4

#### F3.9: BER 近似（P_s/2）

$$P_b \approx \frac{P_s}{2} = \frac{3}{8} - \sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

- Gray coding 假设：相邻符号错误翻转 1 bit
- **精度**：中等-高 SNR 下偏差 <10%（MC 验证 median 6.0%）。低 SNR 下对角错误（2 bit 翻转）贡献增大。

- **来源**: [自推: 基于 Gray coding 假设 P_b ≈ P_s/2]; S002 §3.5
- **变量**: P_b → TERMS §10.2 误比特率; P_s → TERMS §10.2 误符号率; b_n^{GG} → F3.6; σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: MC 仿真 500k 符号，中湍流 σ_φ=10°，median 误差 6.0%，max 误差 69.4%
- **适用条件**: 中-高 SNR，Gray coding QPSK；低 SNR 下精度下降（对角错误贡献增大）
- **章节**: §3.4

#### F3.10: 精确 BER（I/Q 通道分别积分）

$$\boxed{P_b^{exact} = \frac{1}{2} - 2\sum_{n=1}^{N} \frac{b_n^{GG}}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{2} \cos\frac{n\pi}{4}}$$

- **推导**：
  - I 通道错误概率：P_I = P(cos(π/4 + ψ) < 0) = 1 − ∫_{-3π/4}^{π/4} f_total(ψ) dψ
  - 利用 Fourier 展开：∫_{-3π/4}^{π/4} cos(nψ) dψ = (2/n)sin(nπ/2)cos(nπ/4)
  - Q 通道由 QPSK 对称性：P_Q = P_I
  - 精确 BER：P_b = (P_I + P_Q)/2 = P_I
- **与 F3.9 的区别**：
  - F3.9：sin(nπ/4) 加权，偶数 n 有贡献（n=2,6,...）
  - F3.10：sin(nπ/2)cos(nπ/4) 加权，偶数 n 贡献为零（sin(nπ/2)=0）

**验证**（MC，中湍流 σ_φ=10°，500k 符号）：

| 公式 | median 误差 | max 误差 |
|------|-----------|---------|
| F3.9 (P_s/2) | 6.0% | 69.4% |
| F3.10（精确） | 0.6% | 85.9% |

- **来源**: [自推: I/Q通道分别积分]; S002 §3.6
- **变量**: P_b → TERMS §10.2 误比特率; b_n^{GG} → F3.6; σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: sim_ch3_ber_closed_form.py `ber_exact`; MC 仿真 500k 符号，median 误差 0.6%
- **适用条件**: Fourier 级数收敛；精确 QPSK BER（不依赖 P_s/2 近似）
- **章节**: §3.4

#### F3.11: BER Floor 闭合公式

$$P_{b,floor} = Q\!\left(\frac{\pi}{4\sigma_\phi}\right)$$

- **推导**：当 γ̄ → ∞，AWGN 噪声消失：
  - φ ∈ (−π/4, π/4)：两个 cos 均 > 0 → P_b = 0
  - φ ∈ (π/4, 3π/4)：cos(φ+π/4) < 0 → P_b = 1/2
  - P_{b,floor} = (1/2)[P(|φ| > π/4)] = Q(π/(4σ_φ))
- **物理含义**：BER floor 完全由 σ_φ 决定，与湍流强度无关。高 SNR 下相位误差是唯一性能瓶颈。

**关键数值**：

| σ_φ | Q(π/4σ_φ) | 说明 |
|--------------|----------------------|------|
| 5° | 1.13e-19 | 近乎完美 |
| 8° | 9.28e-09 | 优良 |
| 10° | 3.40e-06 | 可接受 |
| 15° | 1.35e-03 | 需改善 |
| 20° | 1.22e-02 | 严重 |

- **来源**: [自推: γ̄→∞极限分析]; S002 §4
- **文献定位**: RF 领域经典结果（Proakis 教材、IET 1995/2020）。H002 确认不可声称新颖，应强调 FSO 场景特殊性
- **变量**: P_{b,floor} → TERMS §10.2 BER下界; σ_φ → TERMS §10.4 载波相位误差标准差; Q(·) → TERMS §10.6 Q函数
- **验证**: 与 Fourier 级数极限 F3.12 在 σ_φ ≥ 8° 时 5 位有效数字一致
- **适用条件**: 高 SNR 极限（γ̄ → ∞），BER floor 完全由 σ_φ 决定，与湍流强度无关
- **章节**: §3.5

#### F3.12: BER Floor 的 Fourier 级数验证

高 SNR 时 b_n → 1/π：

$$P_{b,floor}^{series} = \frac{3}{8} - \frac{1}{\pi}\sum_{n=1}^{N} \frac{1}{n} e^{-n^2\sigma_\phi^2/2} \sin\frac{n\pi}{4}$$

- σ_φ ≥ 8° 时，series 与 Q(π/(4σ_φ)) 在 5 位有效数字内一致。

- **来源**: [自推: F3.9 取 γ̄→∞ 极限 b_n→1/π]; S002 §4
- **变量**: σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: σ_φ ≥ 8° 时与 F3.11 闭合公式在 5 位有效数字内一致
- **适用条件**: 高 SNR 极限，Fourier 级数收敛
- **章节**: §3.5

#### F3.13: 中断概率定义

$$P_{out} = P(\bar{P}_b(\bar\gamma h, \sigma_\phi) > P_{target}) = F_{GG}(h_{th})$$

其中 P_b^{avg}(γ, σ_φ) = E_φ[P_b(γ, φ)] 是相位平均 BER。

- **来源**: S002 §5.1
- **变量**: P_out → TERMS §10.2 中断概率; h → TERMS §10.2 归一化辐照度; γ̄ → TERMS §10.2 平均SNR; σ_φ → TERMS §10.4 载波相位误差标准差; F_GG → TERMS §10.2 GG分布CDF; h_th → TERMS §10.2 阈值归一化辐照度
- **验证**: 定义级公式
- **适用条件**: 块衰落模型，信道在块内恒定
- **章节**: §3.6

#### F3.14: 阈值 SNR

由于 P_b^{avg} 关于 γ 单调递减，存在唯一阈值 γ_th 满足：

$$P_b^{avg}(\gamma_{th}, \sigma_\phi) = P_{target}$$

$$h_{th} = \gamma_{th} / \bar\gamma$$

- **来源**: S002 §5.2
- **变量**: γ_th → TERMS §10.2 阈值SNR; h_th → TERMS §10.2 阈值归一化辐照度; γ̄ → TERMS §10.2 平均SNR; σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: P_b^{avg} 关于 γ 单调递减，保证 γ_th 唯一性
- **适用条件**: P_b^{avg}(γ, σ_φ) 关于 γ 单调递减
- **章节**: §3.6

#### F3.15: GG CDF（Meijer-G 闭合形式）

$$F_{GG}(h) = \frac{1}{\Gamma(\alpha)\Gamma(\beta)} G_{1,3}^{2,1}\left(\alpha\beta h \,\middle|\, \begin{matrix} 1 \\ \alpha, & \beta, & 0 \end{matrix}\right)$$

- **交叉验证**：12 个测试点（3 湍流 × 4 h 值），最大相对误差 4.39×10⁻⁹（中湍流 h=0.01）。Meijer-G CDF 实现正确。

- **来源**: [教科书: Andrews & Phillips]; S002 §5.3
- **变量**: F_GG → TERMS §10.2 GG分布CDF; α → TERMS §10.2 GG大尺度参数; β → TERMS §10.2 GG小尺度参数; h → TERMS §10.2 归一化辐照度; Γ(·) → TERMS §10.6 Gamma函数; G → TERMS §10.6 Meijer-G函数
- **验证**: sim_ch3_ber_closed_form.py `gg_cdf`; 12 个测试点（3 湍流 × 4 h 值），最大相对误差 4.39×10⁻⁹
- **适用条件**: Gamma-Gamma 湍流衰落模型
- **章节**: §3.6

#### F3.16: 无相位误差时的简化

σ_φ = 0 时，P_b = Q(√γ)，阈值 γ_th = [Q⁻¹(P_target)]²。

$$P_{out}^{(0)} = F_{GG}\left(\frac{[Q^{-1}(P_{target})]^2}{\bar\gamma}\right)$$

- **来源**: [自推: F3.13 取 σ_φ=0 简化]
- **变量**: F_GG → TERMS §10.2 GG分布CDF; γ̄ → TERMS §10.2 平均SNR; Q(·) → TERMS §10.6 Q函数
- **验证**: F3.15 + σ_φ=0 特例
- **适用条件**: 无载波相位误差（σ_φ = 0），理想载波同步
- **章节**: §3.6

#### F3.17: BER floor 对中断概率的影响

当 P_target < Q(π/(4σ_φ)) 时，γ_th = ∞，P_out = 1（永远无法达到目标 BER）。这是 BER floor 的另一视角。

**验证结果**（P_target = 10⁻³）：

| σ_φ | γ_th (dB) | SNR 惩罚 | 备注 |
|--------------|-------------------|---------|------|
| 0° | 9.8 | 0 dB | 基准 |
| 5° | 10.2 | +0.4 dB | 轻微 |
| 10° | 12.0 | +2.2 dB | 显著 |
| 15° | ∞ | — | Floor 1.35×10⁻³ > 10⁻³，不可达 |

- **来源**: S002 §5.4
- **变量**: P_target → 目标BER; γ_th → TERMS §10.2 阈值SNR; σ_φ → TERMS §10.4 载波相位误差标准差
- **验证**: 数值计算，σ_φ=15° 时 floor 1.35×10⁻³ > P_target=10⁻³ 导致不可达
- **适用条件**: P_target < P_{b,floor} 时中断概率恒为 1
- **章节**: §3.6

---

## 第四章 低轨星地载波同步算法

### §4.2 载波同步系统模型

#### F4.1: 总载波相位模型

$$\phi[k] = 2\pi f_{res} \cdot kT_s + \pi \dot{f}_D \cdot (kT_s)^2 + \theta_L[k]$$

$$\theta_L[k] = \sqrt{2\pi \Delta\nu_L T_s} \cdot \sum_{i=0}^{k} w[i], \quad w[i] \sim \mathcal{N}(0, 1)$$

- **来源**: [代码: sim_direction_a.py L97-109 (`doppler_phase`)] + [内容卡片 4.2]
- **变量**: φ[k] → TERMS §10.4 总载波相位偏移(rad); f_res → TERMS §10.4 残余频偏(Hz); ḟ_D → TERMS §10.4 多普勒变化率(Hz/s); θ_L[k] → TERMS §10.4 激光相位噪声(rad); Δν_L → TERMS §10.4 激光线宽(Hz); T_s → TERMS §10.4 符号周期(s)
- **验证**: sim_direction_a.py L97-109
- **适用条件**: 星历预补偿已完成，残余频偏为常数；激光相位噪声为维纳过程（白频率噪声假设）
- **章节**: §4.2

#### F4.2: Doppler频偏物理模型

$$f_{DS} = f_c \cdot \frac{v_r}{c}$$

$$v_r(t) = \omega_F R_E \sin(\omega_F t + \psi_{diff})$$

$$\omega_F \approx \omega_S - \omega_E \cos(i_S)$$

- **来源**: [引用: Fernandes 2023 Section II-A]
- **变量**: f_DS → TERMS §10.4 多普勒频偏(Hz); f_c → TERMS §10.4 光载频(Hz); v_r → TERMS §10.4 径向速度(m/s); c → TERMS §10.2 光速(m/s)
- **验证**: sim_direction_a.py L97-109 (Doppler参数一致)
- **适用条件**: LEO圆轨道；地球自转效应通过 ω_F 近似；低仰角时 Doppler 变化率最大
- **章节**: §4.2

#### F4.3: 接收符号相位分解

$$\theta_r[k] = \theta_s[k] + \Delta\omega \cdot kT_s + \theta_L[k] + \theta_a[k]$$

- **来源**: [引用: 闫佳欣 式(2-24)]（符号已统一，原文用 $\theta_n$ 表示激光相位噪声，本文统一用 $\theta_L$）
- **变量**: θ_r[k] → 接收符号总相位; θ_s[k] → QPSK 调制相位; Δω → 频偏角频率(rad/s); θ_L → 激光相位噪声（同F4.1）; θ_a → 其他噪声
- **验证**: 与 F4.1 一致（QPSK 特化形式，四次方可消去 θ_s）
- **适用条件**: QPSK 调制，s⁴ = -1；用于推导四次方 FOE 的理论基础
- **章节**: §4.2

---

### §4.3 频偏估计算法

#### F4.4: FFT频偏估计（四次方法）

$$r_4[k] = (r[k])^4, \quad k = 0, \ldots, N-1$$

$$R_4(f) = \text{FFT}\{r_4[k] \cdot w_{Hann}[k]\}$$

$$\hat{f}_{offset} = \frac{1}{4} \cdot \arg\max_f |R_4(f)|$$

- **来源**: [引用: Liu 2023 Section 2] + [引用: 闫佳欣 式(2-25)-(2-27)] + [代码: sim_direction_a.py L114-142 (`fft_foe`)]
- **变量**: r[k] → TERMS §10.1 接收信号; f̂_{offset} → TERMS §10.4 FFT 频偏估计(Hz); N_fft → TERMS §10.4 FFT 窗口长度(符号)
- **验证**: sim_direction_a.py L114-142
- **适用条件**: QPSK 调制（s⁴ = -1 消除调制信息）；FFT 窗口内频偏近似恒定；零填充提高频率分辨率
- **章节**: §4.3

#### F4.5: 四次方运算的SNR退化

$$\text{SNR}_4 = \frac{\bar\gamma \cdot h}{8}$$

- **来源**: [自推: R016推导1] + [内容卡片 4.3.1]
- **变量**: γ̄ → TERMS §10.2 平均 SNR; h → TERMS §10.2 归一化辐照度; SNR₄ → 四次方后等效 SNR
- **验证**: sim_direction_a.py L223-226 (自适应窗口推导起点)
- **适用条件**: QPSK 信号；四次方后信号功率 ∝ h，噪声功率分析后 SNR₄ = γ̄h/8
- **章节**: §4.3

#### F4.6: [核心公式1] FFT窗口自适应

$$N_{opt}(h) = \frac{80}{\bar\gamma \cdot h^2}$$

$$N_{fft} = \text{clamp}\left(2^{\lceil\log_2 N_{opt}\rceil}, 256, 8192\right)$$

- **来源**: [自推: R016推导1] + [代码: sim_direction_a.py L223-226 (`adaptive_params`)]
- **变量**: N_opt → TERMS §10.4 最优 FFT 窗口(符号); h → TERMS §10.2 归一化辐照度; γ̄ → TERMS §10.2 平均 SNR
- **验证**: sim_direction_a.py L223-226; 参考文献交叉验证一致（见 F4.14 交叉验证表）
- **适用条件**: h⁻² 依赖——深衰落时 SNR 急剧下降，需增大窗口积累能量；分子 80 由检测概率 P_d ≥ 0.99 和虚警概率 P_fa ≤ 10⁻³ 约束推导；窗口范围 [256, 8192]
- **章节**: §4.3

---

### §4.4 载波相位恢复算法

#### F4.7: 二阶数字锁相环（DPLL）

$$\text{鉴相器}: \quad e[k] = \frac{1}{4}\angle\left((r[k] \cdot e^{-j\hat\phi[k-1]})^4\right)$$

$$\text{环路滤波器}: \quad \nu[k] = c_1 \cdot e[k] + \Sigma[k]$$

$$\text{积分器}: \quad \Sigma[k] = \Sigma[k-1] + c_2 \cdot e[k]$$

$$\text{VCO}: \quad \hat\phi[k] = \hat\phi[k-1] + \nu[k]$$

$$c_1 = 2\zeta\omega_n T_s, \quad c_2 = (\omega_n T_s)^2$$

- **来源**: [引用: Liu 2023 Section 2] + [引用: 闫佳欣 第二章] + [代码: sim_direction_a.py L147-192 (`dpll_track`)]
- **变量**: e[k] → TERMS §10.4 DPLL 鉴相器输出(rad); ν[k] → TERMS §10.4 环路滤波器输出; Σ[k] → TERMS §10.4 积分器状态; ω_n → TERMS §10.4 环路自然频率(rad/s); ζ → TERMS §10.4 阻尼系数(无量纲); c_1, c_2 → TERMS §10.4 环路滤波器系数; φ̂[k] → TERMS §10.4 DPLL 相位估计(rad)
- **验证**: sim_direction_a.py L147-192
- **适用条件**: 二阶 PLL（临界阻尼 ζ = √2/2）；B_L ≈ 0.53·ω_n（ζ = √2/2 时）；ω_n·T_s 上限 0.5（稳定性约束）
- **章节**: §4.4

#### F4.8: Viterbi-Viterbi载波相位恢复（CPR）

$$\hat\phi_\text{raw}[k] = \frac{1}{M}\text{unwrap}\left(\angle\left(\sum_{i=k-M/2}^{k+M/2} r[i]^4\right)\right)$$

$$r_{comp}[k] = r[k] \cdot e^{-j\hat\phi_\text{raw}[k]}$$

- **来源**: [引用: Liu 2023 Section 2] + [引用: 闫佳欣 式(2-28)-(2-29)] + [代码: sim_direction_a.py L197-210 (`vv_cpr`)]
- **变量**: φ̂_raw[k] → TERMS §10.4 VV 原始相位估计(rad); M → TERMS §10.4 VV 平均窗口长度(符号); r_comp[k] → TERMS §10.1 载波补偿后信号
- **验证**: sim_direction_a.py L197-210; sim_prototype.py L284-298
- **适用条件**: QPSK（M_order = 4）；unwrap(angle)/M 是修正版 —— **旧版代码 unwrap(angle·M)/M 是错误的**; 幅度裁剪: |r⁴| > 10⁸ 时裁剪（防溢出）
- **章节**: §4.4

#### F4.9: [核心公式2] VV窗口自适应

$$M_{opt}(h) = K_M \cdot (\bar\gamma \cdot h)^{-1/5} \cdot (\Delta f_{res} \cdot T_s)^{-2/5}$$

$$K_M = (3/4)^{1/5} \approx 0.944$$

$$M_{vv} = \text{clamp}\left(\text{odd\_round}(M_{opt}), 9, 255\right)$$

- **来源**: [自推: R016推导2] + [代码: sim_direction_a.py L228-233 (`adaptive_params`)]
- **变量**: M_opt → TERMS §10.4 最优 VV 窗口(符号); K_M → TERMS §10.4 VV 窗口系数(≈0.944); Δf_res → TERMS §10.4 残余频偏(Hz); T_s → TERMS §10.4 符号周期(s)
- **验证**: sim_direction_a.py L228-233; 参考文献交叉验证一致（见 F4.14 交叉验证表）
- **适用条件**: h⁻¹/⁵ 依赖——5 次根号定律（平滑折中）；MSE = 噪声项 + 频偏漂移项，对 M 求导 = 0 得最优解；窗口范围 [9, 255]（确保奇数）
- **章节**: §4.4

#### F4.10: [核心公式3] DPLL带宽自适应

$$B_{L,opt}(h) = B_0 \cdot h$$

$$B_0 = \sqrt{\frac{\pi \Delta\nu_L \bar\gamma}{T_s}}$$

$$\omega_{n,opt} = \frac{B_{L,opt}}{0.53}$$

- **来源**: [自推: R016推导3] + [代码: sim_direction_a.py L236-238 (`adaptive_params`)]
- **变量**: B_L → TERMS §10.4 环路带宽(Hz); B_0 → TERMS §10.4 无衰落最优带宽基准(Hz); ω_n → TERMS §10.4 环路自然频率(rad/s); Δν_L → TERMS §10.4 激光线宽(Hz); γ̄ → TERMS §10.2 平均 SNR; T_s → TERMS §10.4 符号周期(s); h → TERMS §10.2 归一化辐照度
- **验证**: sim_direction_a.py L236-238; sim_cascade_robustness.py L145-148
- **适用条件**: h¹ 线性缩放（最温和的三种自适应之一）；B_L ≈ 0.53·ω_n（ζ = √2/2 时）；ω_n 单位 rad/s；B_L 范围 [0.5, 20] MHz；B₀·h 是设计选择（实现 h 抵消），非 Wiener 最优（Wiener 给出 B₀·√h）
- **章节**: §4.4

#### F4.11: 完整载波恢复链

**固定参数链**:

$$\hat{f}_{FOE} = \text{FFT-FOE}(r, N=1024)$$
$$\to r_1 = r \cdot e^{-j\hat{f}_{FOE} \cdot k}$$
$$\to r_2 = \text{DPLL}(r_1, \omega_n=8\times10^6 \text{ rad/s}, \zeta=\sqrt{2}/2)$$
$$\to r_{out} = \text{VV-CPR}(r_2, M=64)$$

**自适应链（DPLL带宽自适应）**:

$$\hat{f}_{FOE} = \text{FFT-FOE}(r, N=1024)$$
$$\to r_1 = r \cdot e^{-j\hat{f}_{FOE} \cdot k}$$
$$\to B_L = \min(\max(B_0 \cdot h_{est}, 0.5\text{MHz}), 20\text{MHz})$$
$$\to r_2 = \text{DPLL}(r_1, \omega_n = B_L/0.53 \text{ rad/s})$$
$$\to r_{out} = \text{VV-CPR}(r_2, M=64)$$

- **来源**: [代码: sim_direction_a.py L245-272 (`carrier_recovery_fixed/adaptive`)] + [内容卡片 4.2.3]
- **变量**: 各变量同 F4.4/F4.7/F4.8 定义
- **验证**: sim_direction_a.py L245-272
- **适用条件**: FFT-FOE 粗频偏 → DPLL 残余频偏/低频相位 → VV 高频相位噪声；自适应链仅 DPLL 带宽随 h 变化（MVE 验证此配置已足够）
- **章节**: §4.4

---

### §4.5 仿真结果与分析

#### F4.12: 载波同步仿真参数表

| 参数 | 值 | 来源 |
|------|-----|------|
| 符号率 R_s | 2.5 Gsps | Zhao 2025 |
| 符号周期 T_s | 0.4 ns | 1/R_s |
| 光载频 f_c | 1.55×10¹⁴ Hz | ~1550 nm |
| 激光线宽 Δν_L | 10 kHz | Zhao 2025 |
| Doppler变化率（低仰角） | 150 MHz/s | Zhao 2025 |
| Doppler变化率（高仰角） | 30 MHz/s | Wang 2025 |
| 残余频偏 f_res | 1 MHz | Zhao 2025 |
| FFT窗口（固定） | 1024 | Zhao 2025 |
| VV窗口（固定） | 64 | Zhao 2025 |
| DPLL自然频率（固定） ω_n | 8×10⁶ rad/s | Zhao 2025 |
| DPLL阻尼系数 ζ | √2/2 | 临界阻尼 |
| 零填充FFT点数 | 8192 | 提高频率分辨率 |
| 幅度限制阈值 | 3.0 | 防止深衰落噪声爆炸 |
| GG湍流参数 | 见 F3.2 | 同 Ch3 |
| 每帧符号数 | 2000 | MVE 配置 |
| 试验次数 | 20 | 统计平均 |
| 仿真场景 | 3湍流 × 2仰角 = 6种 | 覆盖主要工况 |

- **来源**: [引用: Zhao 2025] + [引用: Wang 2025] + [代码: sim_direction_a.py 参数定义]
- **变量**: 各符号见 TERMS §10.2 / §10.4
- **验证**: sim_direction_a.py 全局参数段
- **适用条件**: MVE 级验证参数；正式仿真可调整
- **章节**: §4.5

#### F4.13: MVE场景配置

| 场景标签 | 湍流 | 仰角 | Doppler率 | GG (α, β) |
|----------|------|------|-----------|------------|
| weak_low | 弱 | 低 | 150 MHz/s | (4.0, 3.0) |
| weak_high | 弱 | 高 | 30 MHz/s | (4.0, 3.0) |
| moderate_low | 中 | 低 | 150 MHz/s | (2.5, 1.8) |
| moderate_high | 中 | 高 | 30 MHz/s | (2.5, 1.8) |
| strong_low | 强 | 低 | 150 MHz/s | (1.5, 0.8) |
| strong_high | 强 | 高 | 30 MHz/s | (1.5, 0.8) |

- **来源**: [代码: sim_direction_a.py 场景定义]
- **变量**: α, β → TERMS §10.2 GG 参数; ḟ_D → TERMS §10.4 多普勒变化率
- **验证**: sim_direction_a.py 场景配置段
- **适用条件**: 覆盖弱/中/强湍流 × 低/高仰角共 6 种工况
- **章节**: §4.5

#### F4.14: 三种h依赖形态对比

| 自适应模块 | 公式 | h依赖 | 物理含义 |
|-----------|------|-------|---------|
| FFT-FOE窗口 | N_opt = 80/(γ̄·h²) | h⁻² | 深衰落阈值效应——SNR急剧下降 |
| VV窗口 | M_opt = K_M(γ̄h)⁻¹/⁵(Δf·T_s)⁻²/⁵ | h⁻¹/⁵ | 平滑折中——5次根号定律 |
| DPLL带宽 | B_{L,opt} = B₀·h | h¹ | 线性缩放——最温和的自适应 |

**代码验证** (sim_direction_a.py `adaptive_params`):

```python
# FOE: N_min = 80/(gamma_bar * h^2)
N_fft = int(np.clip(80 / (gamma_bar * h_est**2 + 1e-10), 256, 8192))
N_fft = int(2**np.ceil(np.log2(N_fft)))

# VV: M_opt = K_M * (gamma*h)^{-0.2} * (df_norm)^{-0.4}
K_M = (3/4)**0.2
gamma = gamma_bar * h_est  # h = irradiance
df_norm = F_RESIDUAL * T_S
M_vv = int(np.clip(K_M * gamma**(-0.2) * df_norm**(-0.4), 16, 256))

# DPLL: B_L_opt = B0 * h
B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
B_L = np.clip(B0 * h_est, 0.5e6, 20e6)
omega_n = B_L / 0.53  # ω_n 单位 rad/s
```

**参考文献交叉验证**:

| 公式 | 论文依据 | 代码依据 | 一致性 |
|------|---------|---------|--------|
| N_opt(h) | R016推导1（SNR₄=C阈值反推） | sim_direction_a.py L224 | 一致 |
| M_opt(h) | R016推导2（VV MSE最小化） | sim_direction_a.py L229-232 | 一致 |
| B_{L,opt}(h) | R016推导3（DPLL最优带宽） | sim_direction_a.py L236-238 | 一致 |
| 四次方FOE | 闫佳欣式(2-25)-(2-27), Liu 2023 | sim_direction_a.py L114-142 | 一致 |
| VV CPR | 闫佳欣式(2-28)-(2-29), Liu 2023 | sim_direction_a.py L197-210 | 一致 |
| Doppler模型 | Fernandes 2023, Zhao 2025 | sim_direction_a.py L97-109 | 一致 |

- **来源**: [自推: R016推导1/2/3] + [代码: sim_direction_a.py `adaptive_params`]
- **变量**: 综合见 F4.6/F4.9/F4.10 各条目
- **验证**: 三公式代码实现 + 参考文献双重交叉验证
- **适用条件**: 三种 h 依赖覆盖从激进(h⁻²)到温和(h¹)的完整自适应频谱
- **章节**: §4.5

---

### §4.2 补充 — 激光相位噪声模型

#### F4.15: 激光器相位噪声（Wiener过程）

$$\theta_L[k] = \theta_L[k-1] + w[k], \quad w[k] \sim \mathcal{N}(0, \sigma_{\theta,L}^2)$$

- **来源**: 丁爽 式(4-8), 董凡 式(2-27)

#### F4.16: 相位噪声方差与线宽关系

$$\sigma_{\theta,L}^2 = 2\pi \Delta\nu_L \cdot T_s$$

- **来源**: 丁爽 式(4-8), Gardner *Phaselock Techniques*

---

### §4.3 补充 — FFT频偏估计理论基础

#### F4.17: N点DFT定义

$$S[m] = \sum_{k=0}^{N-1} r[k] \cdot e^{-j 2\pi mk / N}, \quad m = 0, 1, \ldots, N-1$$

- **来源**: Proakis & Manolakis, Gasior & Gonzalez 2004

#### F4.18: 频率分辨率与观测窗口

$$\Delta f_{\text{grid}} = \frac{f_s}{N} = \frac{1}{N \cdot T_s}$$

- **来源**: Gasior & Gonzalez 2004 Eq.(3)

#### F4.19: 频偏估计Cramér-Rao下界

$$\mathrm{var}(\hat{\Delta f}) \geq \frac{6}{(2\pi)^2 \cdot \mathrm{SNR} \cdot N(N^2 - 1) \cdot T_s^2}$$

- **来源**: Rife & Boorstyn 1974, IEEE Trans. Info. Theory

#### F4.20: 四次方消除QPSK调制证明

$$s^4[k] = e^{j \cdot 4\theta_s[k]} = -1 \quad \Rightarrow \quad r^4[k] \approx -e^{j(4 \cdot 2\pi \Delta f \cdot kT_s + 4\phi[k])} + \text{noise}$$

- **来源**: Proakis Ch.6, 丁爽 式(3-11)

#### F4.21: 四次方后频偏估计范围

$$|\Delta f| < \frac{R_s}{2 \cdot 4} = \frac{R_s}{8}$$

- **来源**: Proakis Ch.6

#### F4.22: 抛物线插值精细化

$$\delta = \frac{1}{2} \cdot \frac{S_{m-} - S_{m+}}{S_{m-} - 2S_{m} + S_{m+}}, \quad \hat{\Delta f} = (m_{\max} + \delta) \cdot \frac{\Delta f_{\text{grid}}}{4}$$

- **来源**: Gasior & Gonzalez 2004 Eq.(10)

#### F4.23: Hanning窗定义

$$w[k] = 0.5\left(1 - \cos\frac{2\pi k}{N-1}\right), \quad k = 0, 1, \ldots, N-1$$

- **来源**: Harris 1978, 最高旁瓣 -31.5 dB

---

### §4.4 补充 — 低复杂度VVPE推导链

#### F4.24: 信号I/Q分解

$$r[k] = I_k + jQ_k, \quad I_k = |r[k]|\cos\phi_k, \quad Q_k = |r[k]|\sin\phi_k$$

- **来源**: 丁爽 式(3-2)

#### F4.25: 绝对值近似（二倍角核心）

$$\cos(2\varphi) \approx |I_k| - |Q_k|, \quad \sin(2\varphi) \approx |I_k + Q_k| - |I_k - Q_k|$$

- **来源**: 丁爽 式(3-3)~(3-7), 张思齐 式(2-6)~(2-12)

#### F4.26: 二倍角结果

$$I'_k = \sqrt{2}(|I_k| - |Q_k|), \quad Q'_k = |I_k + Q_k| - |I_k - Q_k|$$

- **来源**: 丁爽 式(3-7)/(3-8)

#### F4.27: 四倍角结果（等效四次方去调制）

$$I''_k = |I'_k| - |Q'_k|, \quad Q''_k = |I'_k + Q'_k| - |I'_k - Q'_k|, \quad r^{(4)}[k] \propto e^{j(4\phi[k] + \pi)}$$

- **来源**: 丁爽 式(3-9)~(3-11)

#### F4.28: 块平均相位提取

$$\hat{\phi}_\text{raw} = \frac{1}{4}\left[\arg\left(\frac{1}{M}\sum_{k=0}^{M-1} r^{(4)}[k]\right) - \pi\right]$$

- **来源**: 丁爽 式(3-12)/(3-13), Viterbi & Viterbi 1983

#### F4.29: 相位补偿

$$\hat{r}[k] = r[k] \cdot e^{-j\hat{\phi}_\text{raw}}$$

- **来源**: 丁爽 式(3-14)

---

### §4.4 补充 — BPS（Blind Phase Search）算法

#### F4.30: BPS测试相位构造

$$\phi_b = \frac{\pi b}{2B}, \quad b = -B/2, \ldots, 0, \ldots, B/2-1$$

- **来源**: 董凡 式(2-30), Pfau 2009

#### F4.31: 欧氏距离度量

$$|d_{k,b}|^2 = |r[k] \cdot e^{-j\phi_b} - \hat{s}_{k,b}|^2$$

- **来源**: 董凡 式(2-32)

#### F4.32: 块内距离累加（窗口平滑）

$$S_{k,b} = \sum_{i=k-N_w}^{k+N_w} |d_{i,b}|^2$$

- **来源**: 董凡 式(2-33)

#### F4.33: ML精估计（BPS第二级）

$$\hat{\varphi}_\text{ML} = \arg\left(\sum_{k} r[k] \cdot \hat{s}_k^*\right)$$

- **来源**: 董凡 式(2-35)

---

### §4.4 补充 — 相位模糊消除

#### F4.34: 相位跳变检测（π/2模糊消除）

$$\Phi[k] = \begin{cases} \Phi[k-1] + \pi/2, & \text{if } (\hat\phi_\text{raw}[k] - \hat\phi_\text{raw}[k-1]) < -\pi/4 \\ \Phi[k-1] - \pi/2, & \text{if } (\hat\phi_\text{raw}[k] - \hat\phi_\text{raw}[k-1]) > \pi/4 \\ \Phi[k-1], & \text{otherwise} \end{cases}$$

- **来源**: 张思齐 式(3-27), 丁爽 §3.2

#### F4.35: 修正后相位估计

$$\hat{\phi}_\text{final}[k] = \hat{\phi}_\text{raw}[k] + \Phi[k]$$

- **来源**: 张思齐 式(3-28)

---

### §4.4 补充 — DPLL稳定性分析

#### F4.36: 连续时间闭环传递函数

$$H(s) = \frac{2\zeta\omega_n s + \omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

- **来源**: Gardner *Phaselock Techniques* §2.2.3

#### F4.37: 误差传递函数

$$H_e(s) = 1 - H(s) = \frac{s^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

- **来源**: Gardner §2.2.3

#### F4.38: 环路滤波器系数（PI结构）

$$\alpha_\text{DPLL} = \frac{2\zeta\omega_n T_s}{K_p K_\text{nco}}, \quad \beta_\text{DPLL} = \frac{(\omega_n T_s)^2}{K_p K_\text{nco}}$$

- **来源**: Robertson DSPRelated 2016, Rice Appendix C

#### F4.39: 离散闭环传递函数

$$H_\text{CL}(z) = \frac{G_1(z)}{1+G_1(z)}, \quad G_1(z) = \frac{K_p \alpha_\text{DPLL} K_\text{nco}}{z-1} + \frac{K_p \beta_\text{DPLL} K_\text{nco}}{(z-1)^2}$$

- **来源**: Robertson DSPRelated 2016

#### F4.40: 噪声带宽与自然频率关系

$$B_L = \frac{\omega_n}{2}\left(\zeta + \frac{1}{4\zeta}\right), \quad \zeta = 1/\sqrt{2} \Rightarrow B_L \approx 0.53\,\omega_n$$

- **来源**: Gardner §2.3

#### F4.41: 稳态相位误差（频率斜升输入）

$$\theta_e(\infty) = \frac{2\pi \dot{f}_d}{\omega_n^2} \quad \text{(rad)}$$

- **来源**: Georgia Tech ECE 6440

#### F4.42: 收敛时间常数

$$\tau = \frac{1}{\zeta\omega_n}, \quad T_L = \frac{2\pi}{\omega_n}$$

- **来源**: Gardner §2.2

#### F4.43: 离散稳定性条件

$$\omega_n T_s < 0.1 \sim 0.5 \quad \Longleftrightarrow \quad f_n / f_s < 0.016 \sim 0.08$$

- **来源**: Robertson Appendix C, TI SLYT169

---

### §4.4 补充 — 载波恢复级联流程

#### F4.44: 频偏补偿后信号

$$r'[k] = r[k] \cdot \exp\!\left(-j \cdot 2\pi \hat{\Delta f} \cdot kT_s\right)$$

- **来源**: 张思齐 式(2-21)/(3-23)

#### F4.45: 四次方信号频偏补偿（数据复用）

$$r^{(4)'}[k] = r^{(4)}[k] \cdot \exp\!\left(-j \cdot 4 \cdot 2\pi \hat{\Delta f} \cdot kT_s\right)$$

- **来源**: 张思齐 式(3-24)（核心创新：跨阶段复用）

#### F4.46: 完整级联链信号流

$$r[k] \xrightarrow{\times 4} r^{(4)}[k] \xrightarrow{\text{FFT}} \hat{\Delta f} \xrightarrow{\text{comp}} r'[k],\; r^{(4)'}[k] \xrightarrow{\text{avg}} \hat{\phi}_\text{raw} \xrightarrow{+\Phi} \hat{\phi}_\text{final} \xrightarrow{\text{comp}} \hat{r}[k]$$

- **来源**: 综合张思齐 §3.2 + sim_direction_a.py

---
### §4.4 补充 — CCISP DA/NDA 切换公式（F4.47-F4.54）
#### F4.47: 强度增益接收模型
$$r_k=\sqrt{h_{b(k)}}s_k e^{j\phi_k}+n_k,\quad b(k)=\lfloor k/N_{\rm ch}\rfloor,\quad N_{\rm ch}=100.$$
- **来源/适用条件**：`projects/simulation/common/_channel.py:10-15,127-138`；Gamma-Gamma 强度块衰落的相干复基带模型，DSP/切换窗另为 256 点。
- **变量/验证**：$h$ 为强度增益、$s_k$ 为 APSK 符号、$n_k$ 为复 AWGN；代码信号项逐字为 `tx * np.sqrt(h) * carrier`。
#### F4.48: 残余频偏、Doppler rate 与 Wiener 相位过程
$$\phi_k=2\pi f_{\rm res}kT_s+\pi\dot f(kT_s)^2+\sum_{i=0}^{k}\Delta\phi_i,\qquad \Delta\phi_i\sim\mathcal N(0,2\pi\Delta\nu T_s).$$
- **来源/适用条件**：`projects/simulation/common/_channel.py:18-37`、`simulator/_b11_params.py:46-58`；单载波 2.5-GBaud、10-kHz 线宽配置。
- **变量/验证**：$f_{\rm res}$ 为残余频偏、$\dot f$ 为频率变化率、$\Delta\nu$ 为线宽；三项分别对应 `phi_fo`、`phi_dot`、`phi_laser`。
#### F4.49: 多导频 phase-time LS
$$\vartheta_\ell=\operatorname{unwrap}\angle(r_{n_\ell}/p_\ell),\quad \widehat{\Delta f}=\frac{\sum_\ell(t_\ell-\bar t)(\vartheta_\ell-\bar\vartheta)}{2\pi\sum_\ell(t_\ell-\bar t)^2},\quad \hat\phi_0=\bar\vartheta-2\pi\widehat{\Delta f}\bar t,\quad t_\ell=n_\ell T_s.$$
- **来源/适用条件**：`projects/simulation/common/_recovery.py:136-168`；已知多导频、窗内相位对时间采用无权线性 LS。
- **变量/验证**：$n_\ell,p_\ell$ 为导频索引/符号；代码以 covariance/variance 求 slope，并由截距同时给出 CFO 与 CPE。
#### F4.50: NDA $M_0$ 次幂相位估计
$$\hat\phi_{\mathcal I}=\frac1{M_0}\angle\!\left(\frac1{|\mathcal I|}\sum_{k\in\mathcal I}r_k^{M_0}\right),\quad M_0=8;\qquad \mathcal I=\{0{:}255\}\ \text{或}\ \mathcal I_q\ (K=8,|\mathcal I_q|=32).$$
- **来源/适用条件**：`projects/simulation/common/_recovery.py:171-237`；湍流路径用 whole-window，AWGN 路径用 8 段估计、段间 unwrap 与线性插值。
- **变量/验证**：$\mathcal I$ 为 256 点 DSP 窗或 32 点子段；对应 `raised.mean()` 与 `intra_block_tracking='segmented'` 两个实现分支。
#### F4.51: blind-$h$ proxy、effective SNR 与两层选择
$$\hat h_{\rm dsp}=\max\!\left\{\overline{|r|^2}-\frac1{2\bar\gamma},10^{-6}\right\},\quad \hat\gamma_{\rm eff,dB}=\bar\gamma_{\rm dB}+10\log_{10}\hat h_{\rm dsp},\quad \mathcal A(r)=\begin{cases}{\rm NDA},&{\rm CV}<\tau_{\rm CV},\\{\rm DA},&{\rm CV}\ge\tau_{\rm CV},\ \hat\gamma_{\rm eff,dB}<13\ {\rm dB},\\{\rm NDA},&\text{otherwise.}\end{cases}$$
- **来源/适用条件**：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py:64-90,191-206`；raw 256-sample 窗、固定预校准决策参数。
- **变量/验证**：$\bar\gamma$ 为传入的 nominal/data SNR，$\hat h_{\rm dsp}$ 为功率代理量；与 `decide()` 分支逐项一致，不作无偏或理论最优声称。
#### F4.52: CV 统计量与 SNR 相关门限
$$ {\rm CV}=\frac{\operatorname{std}(|r_k|^2)}{\operatorname{mean}(|r_k|^2)},\qquad \tau_{\rm CV}=1.10\left(0.74+0.12e^{-\bar\gamma_{\rm dB}/5}\right). $$
- **来源/适用条件**：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py:64-90`；raw decision window 上的预校准第一层门控。
- **变量/验证**：统计对象为接收功率 $|r_k|^2$；公式逐字对应 `cv_awgn_theory()`、`CV_MARGIN=1.10` 和 `decide()`。
#### F4.53: pilot 开销与 total-energy SNR 坐标
$$\rho_p=1/L_p=1/4,\quad \Delta_p=10\log_{10}\frac{L_p}{L_p-1}=1.249\ {\rm dB},\quad \gamma_{\rm tot,NDA,dB}=\gamma_{d,\rm dB},\quad \gamma_{\rm tot,DA,dB}=\gamma_{d,\rm dB}+\Delta_p.$$
- **来源/适用条件**：`projects/simulation/simulator/_b11_params.py:64-68`、`simulator/fair_comparison.py:2-44`；相同信息吞吐量下的公平总能量坐标。
- **变量/验证**：$L_p=4$ 为 pilot spacing、$\rho_p=25\%$ 为密度；`PILOT_OVERHEAD_DB` 与 DA/NDA 映射均由代码直接实现。
#### F4.54: 同 SNR BER reduction 指标
$$G_{\rm BER}^{\rm NDA\rightarrow SW}(\gamma)=10\log_{10}\frac{P_{b,{\rm NDA}}(\gamma)}{P_{b,{\rm SW}}(\gamma)}.$$
- **来源/适用条件**：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py:220-270`；相同 nominal SNR、相同 full-block-bit 分母。
- **变量/验证**：正值表示 switching BER 更低；与 `gain_vs_nda` 精确一致，仅称 BER reduction，不称 SNR gain。
---
### §4.4 补充 — Kalman滤波载波同步（F4.K1-F4.K13）
> KF 13条公式（状态空间模型 F4.K1-K3、噪声设计 F4.K4-K7、递推方程 F4.K8-K9、性能分析 F4.K10-K13）完整推导见 `写作材料/archive/formulas-dedup-backup/formulas-ch4-kf.md`
---
### 跨章依赖图
```
Ch2 系统模型
  F1-F36 信号/噪声/信道/链路预算           ← 全文模型基础
    │
    ├──→ Ch3 信道估计技术（2026-06-01 重构）
    │     §3.2 问题建模: F3.1-F3.3 (系统模型/SNR/湍流参数)
    │     §3.3 估计方法: [待补充 LS/MMSE/KF 公式]
    │     §3.4 级联影响: F3.18 (σ_φ设计目标) + F3.21 (鲁棒性分析)
    │     §3.5 仿真结果: F3.19-F3.20 (设计准则)
    │     归档区: F3.4-F3.17 (BER分析，旧方向)
    │         │
    │         └──→ §3.4 核心结论: NMSE 0~-20dB 范围内退化 <0.3dB → 载波同步可靠
    │
    └──→ Ch4 载波同步算法
          §4.2 系统模型: F4.1-F4.3 (相位/Doppler/分解)
          §4.3 频偏估计: F4.4-F4.6 (FFT-FOE/SNR退化/窗口自适应)
          §4.4 相位恢复: F4.7-F4.11 (DPLL/VV/自适应/完整链)
          §4.5 仿真结果: F4.12-F4.14 (参数/场景/对比)
```

---

## 第五章 接收端信号处理链 FPGA 设计与实现

> **说明**：Ch5 侧重"算法→硬件"映射。Ch4 已给出算法公式（F4.1-F4.14），本章公式聚焦定点量化、并行架构、硬件优化和资源/时序分析。
>
> **符号约定**：所有 FPGA 符号见 TERMS.md §10.5（f_clk, W, LUT, FF, DSP, BRAM, f_max）。
>
> **主要参考**：董凡 2024（低复杂度相干光通信载波恢复算法研究与实现），邹欣航 2025（高速光通信系统的并行定点信号处理技术研究），白佳俊 2024（QPSK 调制解调研究与实现）。

---

### §5.2 前置：定点量化模型

### F5.1 定点数 [W_I, W_F] 格式表示

$$
x_{\text{fixed}} = (-1)^{s} \cdot \left( \sum_{k=0}^{W_I - 2} b_k \cdot 2^k + \sum_{k=1}^{W_F} b_{-k} \cdot 2^{-k} \right), \quad W = 1 + W_I + W_F
$$

**定义**：
- $x_{\text{fixed}}$: 定点数表示的数值（无量纲）
- $s$: 符号位，$s \in \{0, 1\}$（无量纲）
- $W_I$: 整数位宽，含 1 位隐含整数位（bit）
- $W_F$: 小数位宽（bit）
- $W$: 总位宽，$W = 1 + W_I + W_F$（bit）
- $b_k$: 第 $k$ 位的二进制值，$b_k \in \{0, 1\}$（无量纲）

**来源**：通用公式

**适用条件**：二进制补码编码；数据范围 $[-2^{W_I-1},\ 2^{W_I-1} - 2^{-W_F}]$

**验证方式**：取已知十进制数，按 [W_I, W_F] 编码后反算，误差为零

**备注**：本文常用格式：2Q9（$W_I=2, W_F=9, W=12$）用于角度数据，范围覆盖 $(-\pi, \pi]$；6Q9（$W_I=6, W_F=9, W=16$）用于 32 倍频偏值。每增加 1 bit 小数位宽，量化噪声功率降低 6.02 dB。

---

### F5.2 定点量化误差模型（舍入）

$$
\varepsilon_q = Q(x) - x, \quad \varepsilon_q \sim \mathcal{U}\left(-\frac{\Delta}{2},\ \frac{\Delta}{2}\right), \quad \Delta = 2^{-W_F}
$$

**定义**：
- $\varepsilon_q$: 量化误差（无量纲）
- $Q(x)$: 量化后的值（无量纲）
- $x$: 原始值（无量纲）
- $\Delta$: 量化步长，即 LSB 代表的值（无量纲）
- $W_F$: 小数位宽（bit）
- $\mathcal{U}(a, b)$: 区间 $[a, b]$ 上的均匀分布

**来源**：通用公式

**适用条件**：舍入量化（rounding）；输入信号未超出可表示范围（无溢出）

**验证方式**：生成大量随机数，量化后统计误差分布，检验是否服从 $\mathcal{U}(-\Delta/2, \Delta/2)$

**备注**：截断量化（truncation）时误差服从 $\mathcal{U}(-\Delta, 0)$，方差为 $\Delta^2/3$，劣于舍入。FPGA 中乘法器输出截断低位时常见截断量化。

---

### F5.3 量化噪声方差

$$
\sigma_q^2 = \frac{\Delta^2}{12} = \frac{2^{-2W_F}}{12}
$$

**定义**：
- $\sigma_q^2$: 量化噪声方差（无量纲）
- $\Delta = 2^{-W_F}$: 量化步长（无量纲）
- $W_F$: 小数位宽（bit）

**来源**：通用公式

**适用条件**：舍入量化；量化误差与信号不相关

**验证方式**：数值仿真，统计量化误差方差，与 $\Delta^2/12$ 比较

**备注**：每增加 1 bit 小数位宽，量化噪声功率降低 6.02 dB。

---
> F5.4 已归档：见 `_archive/formulas-superseded-2026-07-14.md`。
### F5.5 溢出保护（饱和截断）

$$
\text{sat}(x) = \text{sgn}(x) \cdot \min\left(|x|,\ 2^{W_I - 1} - 2^{-W_F}\right)
$$

**定义**：
- $\text{sat}(x)$: 饱和截断后的值（无量纲）
- $x$: 输入值（无量纲）
- $\text{sgn}(\cdot)$: 符号函数
- $W_I$: 整数位宽（bit）
- $W_F$: 小数位宽（bit）
- $2^{W_I-1} - 2^{-W_F}$: 最大可表示正数

**来源**：通用公式

**适用条件**：补码定点运算中结果超出可表示范围时

**验证方式**：输入超范围值，检查输出是否被限制

**备注**：角度域算法中，角度数据需限制在 $(-\pi, \pi]$ 范围内，等价于对 2Q9 格式数据的饱和截断。

---

### §5.3.1 频偏估计与补偿模块

### F5.6 并行处理时钟频率

$$
f_{\text{clk}} = \frac{R_s}{P}
$$

**定义**：
- $f_{\text{clk}}$: FPGA 系统时钟频率（Hz）
- $R_s$: 符号率（Baud）
- $P$: 并行路数（无量纲整数）

**来源**：董凡 2024 表 3-1；邹欣航 2025 表 3-1

**适用条件**：每个时钟周期处理 $P$ 个并行符号

**验证方式**：$R_s = 2.5$ GBaud, $P = 32$ → $f_{\text{clk}} = 78.125$ MHz，与董凡 2024 一致

**备注**：FPGA 时钟频率一般限制在 50–400 MHz，$P$ 的选取需使 $f_{\text{clk}}$ 落入此范围。

---

### F5.7 基-2 FFT 蝶形运算

$$
X = A + W_N^k \cdot B, \quad Y = A - W_N^k \cdot B, \quad W_N^k = e^{-j 2\pi k / N}
$$

**定义**：
- $X, Y$: 蝶形运算的两个输出（复数，非 GG 大/小尺度分量 $X, Y$）
- $A, B$: 蝶形运算的两个输入（复数）
- $W_N^k$: 旋转因子（twiddle factor），复数
- $N$: FFT 点数（无量纲正整数，为 2 的幂）
- $k$: 旋转因子索引，$k = 0, 1, \ldots, N/2 - 1$

**来源**：通用公式

**适用条件**：基-2 DIT FFT 算法

**验证方式**：取 $N=4$，手动计算全部蝶形运算，与 DFT 定义对比

**备注**：每个蝶形运算需 1 次复数乘法（或 3 次实数乘法）和 2 次复数加法。旋转因子预存在 ROM 中。

---

### F5.8 FFT 运算复杂度

$$
\text{复数乘法次数} = \frac{N}{2} \log_2 N, \quad \text{复数加法次数} = N \log_2 N
$$

**定义**：
- $N$: FFT 点数（无量纲正整数）
- $\log_2 N$: 以 2 为底的对数（无量纲）

**来源**：通用公式

**适用条件**：基-2 FFT；旋转因子乘法计算在内

**验证方式**：$N = 4096$ → $24576$ 次复数乘法，与董凡 2024 表 3-5 一致

**备注**：复数乘法等价于 4 次实数乘法 + 2 次实数加法，或优化后 3 次实数乘法 + 5 次实数加法。

---

### F5.9 线性近似求模运算（替代 CORDIC）

$$
|\hat{z}| = \frac{31}{32} |x| + \frac{13}{32} |y|, \quad \text{max error} \approx 0.05
$$

其中 $|x| \geq |y|$（确保 $|x|$ 为较大分量）。

**定义**：
- $|\hat{z}|$: 近似模值（无量纲）
- $x, y$: 复数的实部和虚部（无量纲）
- $31/32, 13/32$: 近似系数，选取为 2 的幂次组合以支持移位实现

**来源**：董凡 2024 式 3-14

**适用条件**：$|x| \geq |y|$；误差容忍度约 5%

**验证方式**：对 $z = \cos\theta + j\sin\theta$（$\theta$ 均匀取值），比较近似与精确模值

**备注**：$31/32 = 1 - 1/32$ 通过右移 5 位后做减法实现。将求模运算从需要乘法器或 CORDIC 降级为纯移位+加法，极大节省 FPGA 资源。

---

### F5.10 峰值检测（比较器树）

$$
k_{\max} = \arg\max_{k} \ |\text{FFT}[k]|^2, \quad k \in [0, N/2)
$$

三级流水线比较器树：32 个数据分 8 组→8 个局部最大值→2 个半局最大值→1 个全局最大值。跨周期迭代比较：设置最大值寄存器和最大值索引寄存器，128 个周期内持续更新。

**定义**：
- $k_{\max}$: 频谱最大幅值点对应的频率索引（无量纲整数，11 bit）
- $|\text{FFT}[k]|^2$: 第 $k$ 个频率点的功率（无量纲）
- $N$: FFT 点数，本文取 4096

**来源**：董凡 2024 §5.3.5 findmax 模块

**适用条件**：32 路并行 FFT 输出，单边谱搜索；128 个时钟周期完成一帧

**验证方式**：TestBench 中验证 FFT 频谱最大值坐标与 4 倍频偏对应的频率索引一致

**备注**：findmax 模块首先通过 get_modulo 子模块进行线性近似求模（F5.9），然后进行三级流水线比较。输出索引为 11 bit。

---
> F5.11 已归档：见 `_archive/formulas-superseded-2026-07-14.md`。
### F5.12 并行频偏补偿（角度域）

$$
\phi_{\text{nofo},\, i} = \phi_{\text{delay},\, i} - (i \cdot \hat{\phi}_{\text{fo}} + \Phi_{\text{acc}}), \quad i = 0, 1, \ldots, P - 1
$$

$i \cdot \hat{\phi}_{\text{fo}}$ 通过移位+加减实现：$\hat{\phi}_{\text{fo, 16}} = \hat{\phi}_{\text{fo, 32}} \gg 1$, $\hat{\phi}_{\text{fo, 8}} = \hat{\phi}_{\text{fo, 32}} \gg 2$, 其余倍数通过加减组合（如 $\hat{\phi}_{\text{fo, 31}} = \hat{\phi}_{\text{fo, 32}} - \hat{\phi}_{\text{fo, 1}}$）。

**定义**：
- $\phi_{\text{nofo},\, i}$: 第 $i$ 路频偏补偿后的角度（rad，2Q9 格式 12 bit）
- $\phi_{\text{delay},\, i}$: 第 $i$ 路延迟后的原始角度（rad，2Q9 格式 12 bit）
- $i$: 路索引，$0 \leq i \leq 31$
- $\hat{\phi}_{\text{fo}}$: 单路频偏估计值（rad）
- $\hat{\phi}_{\text{fo, 32}}$: 32 倍频偏值（rad，6Q9 格式 16 bit）
- $\Phi_{\text{acc}}$: 前序周期累积的频偏补偿值（rad）
- $P$: 并行路数，取 32
- $\gg$: 右移操作

**来源**：董凡 2024 §5.3.7 fo_comp 模块

**适用条件**：角度域频偏补偿（非复数域）；用移位替代除法节省资源

**验证方式**：TestBench 中检查频偏补偿后星座图是否消除了旋转

**备注**：不使用复数乘法器，通过角度域减法实现补偿。补偿后输出需限制在 $(-\pi, \pi]$ 范围内。

---

### F5.13 迭代平均法（硬件优化）

$$
\hat{\phi}_{\text{est}}^{(n+1)} = \hat{\phi}_{\text{est}}^{(n)} + h \cdot \left(\phi_{\text{input}}^{(n)} - \hat{\phi}_{\text{est}}^{(n)}\right), \quad h = 1 - 2^{-7}
$$

其中 $h \cdot x$ 通过移位实现：$h \cdot x = x - (x \gg 7)$。

**定义**：
- $\hat{\phi}_{\text{est}}^{(n)}$: 第 $n$ 次迭代后的频偏估计值（rad，2Q9 格式）
- $\phi_{\text{input}}^{(n)}$: 第 $n$ 次输入的频偏估计值（rad，1Q9 格式）
- $h$: 迭代步长，$h = 127/128$（无量纲）
- $n$: 迭代次数（无量纲）

**来源**：董凡 2024 §5.3.3 iter_ave 模块

**适用条件**：步长选取为 $1 - 2^{-7}$，可通过一次右移 7 位加一次减法实现，无需 DSP48E

**验证方式**：对比 MATLAB 浮点迭代平均与 RTL 迭代平均输出

**备注**：对 4096 个符号的相偏估计值进行迭代平均后输出。避免 DSP 资源占用，仅需移位器和加法器。

---

### §5.3.2 载波相位恢复模块

### F5.14 输入角度预处理（pre_process）

$$
\phi_{\text{prepro}} = \phi_{\text{in}} - \frac{\pi}{4} \mod \frac{\pi}{2}, \quad \phi_{\text{prepro}} \in \left[0, \frac{\pi}{2}\right)
$$

硬件实现通过比较器+加法器组合完成：

| $\phi_{\text{in}}$ 范围 | 相位调整值 |
|:---|:---|
| $(3\pi/4, \pi]$ | $-3\pi/4$ |
| $(\pi/4, 3\pi/4]$ | $-\pi/4$ |
| $(-\pi/4, \pi/4]$ | $+\pi/4$ |
| $(-3\pi/4, -\pi/4]$ | $+3\pi/4$ |
| $(-\pi, -3\pi/4]$ | $+5\pi/4$ |

**定义**：
- $\phi_{\text{prepro}}$: 预处理后的角度输出（rad，1Q9 格式 11 bit）
- $\phi_{\text{in}}$: 频偏补偿后的输入角度（rad，2Q9 格式 12 bit）

**来源**：董凡 2024 §5.4.1 pre_process 模块

**适用条件**：QPSK 含 $\pi/4$ 偏移的星座映射；输入角度范围 $(-\pi, \pi]$

**验证方式**：取各区间边界值，验证输出是否落在 $[0, \pi/2)$

**备注**：为优化时序，将去调制相位步骤与求余数步骤合并，减少一级加法器延迟。

---

### F5.15 BCPE 树节点运算（硬件优化版）

$$
\mu = \frac{\alpha + \beta}{2} + f(\alpha - \beta)
$$

条件修正函数：

$$
f(\delta) = \begin{cases}
0, & |\delta| \leq \pi/4 \\
\text{sgn}(\delta) \cdot \pi/2, & |\delta| > \pi/4
\end{cases}
$$

优化后每个节点仅需 2 个加法器 + 1 个比较器 + 1 个选择器。

**定义**：
- $\mu$: 节点运算输出角度（rad，1Q9 格式 11 bit）
- $\alpha, \beta$: 输入角度 1 和 2（rad，1Q9 格式 11 bit；非 GG 模型参数 $\alpha, \beta$）
- $f(\cdot)$: 条件修正函数（rad）
- $\delta = \alpha - \beta$: 两个输入的差值（rad）

**来源**：董凡 2024 §5.4.2 tree_node 模块

**适用条件**：输入角度范围 $[0, \pi/2)$（经过 pre_process 后）；32 路并行估计树共 31 个节点

**验证方式**：取已知 $\alpha, \beta$ 值，手动计算节点输出，与 RTL 仿真对比

**备注**：优化前每个 tree_node 需 3 个加法器 + 2 个比较器 + 2 个选择器，优化后节省 25% 加法器和 50% 选择器。31 个节点分 5 层（$16 + 8 + 4 + 2 + 1$），每两层之间插入流水线寄存器。

---

### F5.16 Phase Unwrap 状态机

$$
\hat{\phi}_{\text{unwrap}}[n] = \hat{\phi}_{\text{err}}[n] + \Delta_{\text{state}}[n]
$$

状态转移由相位差判定：

$$
\text{condition} = \begin{cases}
2'b00, & \Delta\hat{\phi} \in [-\pi, -\pi/4) \\
2'b01, & \Delta\hat{\phi} \in [-\pi/4, \pi/4) \\
2'b10, & \Delta\hat{\phi} \in [\pi/4, \pi]
\end{cases}
$$

| 状态 | $\Delta_{\text{state}}$ (rad) |
|:---|:---|
| S0 | $0$ |
| S1 | $-\pi/2$ |
| S2 | $-\pi$ |
| S3 | $+\pi/2$ |
| S4 | $+\pi$ |

**定义**：
- $\hat{\phi}_{\text{unwrap}}[n]$: Phase Unwrap 后的相位误差（rad，2Q9 格式 12 bit）
- $\hat{\phi}_{\text{err}}[n]$: 当前估计得到的相位误差（rad，1Q9 格式 11 bit）
- $\Delta_{\text{state}}[n]$: 当前状态的相位调整值（rad）
- $\Delta\hat{\phi}[n] = \hat{\phi}_{\text{err}}[n] - \hat{\phi}_{\text{err}}[n-1]$: 前后符号的相位差（rad）

**来源**：董凡 2024 §5.4.3 phase_unwrap 模块

**适用条件**：基于激光器相位慢变特性，前后符号相位差超过 $\pi/4$ 则需要展开

**验证方式**：输入含相位跳变的测试序列，验证状态机正确跟踪

**备注**：5 个状态和 3 种转移条件组成的状态机。

---

### F5.17 相位补偿（po_comp）

$$
\phi_{\text{out},\, i} = \text{mod}_{(-\pi, \pi]}\left(\phi_{\text{delay},\, i} - \hat{\phi}_{\text{unwrap}}\right), \quad i = 0, 1, \ldots, 31
$$

**定义**：
- $\phi_{\text{out},\, i}$: 第 $i$ 路相位补偿后的角度输出（rad，2Q9 格式 12 bit）
- $\phi_{\text{delay},\, i}$: 第 $i$ 路延迟后的输入角度（rad，2Q9 格式 12 bit）
- $\hat{\phi}_{\text{unwrap}}$: Phase Unwrap 后的相位误差（rad，2Q9 格式 12 bit）
- $\text{mod}_{(-\pi, \pi]}(\cdot)$: 将结果限制在 $(-\pi, \pi]$ 的取模运算

**来源**：董凡 2024 §5.4.4 po_comp 模块

**适用条件**：每次计算的相位信息对 32 个符号同时补偿

**验证方式**：TestBench 中检查相位补偿后星座图是否清晰

**备注**：与 fo_comp（F5.12）结构相似，均为角度域减法补偿。区别在于 fo_comp 对每路使用不同倍数的频偏值，而 po_comp 对所有 32 路使用相同的相位误差值。

---

### §5.3 补充：CORDIC 算法

### F5.18 CORDIC 旋转模式迭代公式

$$
\begin{aligned}
x_{i+1} &= x_i - d_i \cdot y_i \cdot 2^{-i} \\
y_{i+1} &= y_i + d_i \cdot x_i \cdot 2^{-i} \\
z_{i+1} &= z_i - d_i \cdot \arctan(2^{-i})
\end{aligned}
$$

旋转方向：

$$
d_i = \begin{cases}
+1, & y_i < 0 \\
-1, & y_i \geq 0
\end{cases}
$$

经过 $N_{\text{iter}}$ 次迭代后：$\hat{\theta} = \arctan(y_0/x_0) \approx z_{N_{\text{iter}}}$

**定义**：
- $x_i, y_i$: 第 $i$ 次迭代后的坐标分量（无量纲）
- $z_i$: 第 $i$ 次迭代后的角度残差（rad）
- $d_i$: 旋转方向，$d_i \in \{+1, -1\}$
- $i$: 迭代索引，$i = 0, 1, \ldots, N_{\text{iter}} - 1$
- $N_{\text{iter}}$: 总迭代次数（无量纲正整数）
- $\arctan(2^{-i})$: 预计算的旋转角度表（rad）

**来源**：通用公式；董凡 2024 §5.3.1 arg 模块使用 CORDIC IP 核

**适用条件**：旋转模式下将向量旋转到 $x$ 轴上；每次迭代仅涉及移位和加法运算

**验证方式**：取已知角度的复数输入，验证 CORDIC 输出与 $\arctan(y/x)$ 的误差

**备注**：精度取决于迭代次数，$N_{\text{iter}}$ 次迭代后角度精度约 $2^{-N_{\text{iter}}}$ rad。董凡 2024 中输出为 12 bit 2Q9 格式。

---

### F5.19 NCO 相位累加器

$$
\theta[k] = \left(\theta[k-1] + 2\pi \hat{\Delta f} \cdot T_s\right) \mod 2\pi
$$

**定义**：
- $\theta[k]$: 第 $k$ 个采样点的相位（rad）
- $\hat{\Delta f}$: 估计的频偏值（Hz）
- $T_s = 1/R_s$: 采样周期（s）

**来源**：通用公式；白佳俊 2024 §3.3

**适用条件**：NCO/DDS 实现频偏补偿的核心结构

**验证方式**：设定已知频偏，检查 NCO 输出频率与设定值一致

**备注**：本文采用角度域方案（F5.12），不使用传统 NCO+复数乘法器架构。但复数域方案（如 VVPE）需此结构。并列出以备 Ch5 论述"角度域 vs 复数域"对比时使用。

---

### F5.20 并行 NCO 相位累加

$$
\theta[k+i] = \theta[k] + i \cdot \Delta\theta, \quad i = 0, 1, \ldots, P - 1
$$

其中 $\Delta\theta = 2\pi \hat{\Delta f} \cdot T_s$。

**定义**：
- $\theta[k+i]$: 第 $k+i$ 个采样点的相位（rad）
- $\theta[k]$: 基准相位（rad）
- $i$: 路内偏移索引
- $P$: 并行路数，取 32
- $\Delta\theta$: 每个采样点的相位增量（rad/采样点）

**来源**：通用公式；邹欣航 2025 §3.3.5

**适用条件**：$P$ 路并行 DDS 同时生成 $P$ 个相位值

**验证方式**：检查相邻路相位差是否等于 $\Delta\theta$

**备注**：在角度域实现中等价于 F5.12 中通过移位+加减生成各路的频偏补偿值 $i \cdot \hat{\phi}_{\text{fo}}$。

---

### F5.21 复数乘法器频偏补偿（复数域实现）

$$
r'[k] = r[k] \cdot e^{-j\theta[k]} = (I_r \cos\theta + Q_r \sin\theta) + j(Q_r \cos\theta - I_r \sin\theta)
$$

**定义**：
- $r'[k]$: 补偿后的复数信号（$I' + jQ'$）
- $r[k]$: 输入复数信号（$I_r + jQ_r$）
- $\theta[k]$: NCO 生成的补偿相位（rad）
- $\cos\theta, \sin\theta$: 通过查找表或 CORDIC 获取

**来源**：通用公式；白佳俊 2024 §3.3

**适用条件**：复数域频偏补偿；需 4 次实数乘法 + 2 次实数加法（或 3 乘法器算法）

**验证方式**：设定已知频偏和相位，验证补偿后信号频偏为零

**备注**：本文采用角度域方案不使用此架构。列出以备"本文选择角度域而非复数域"的对比论述。

---

### §5.4 资源利用率与性能验证

### F5.22 复数乘法器资源

直接实现（4 实数乘法 + 2 实数加法）：

$$
(a + jb)(c + jd) = (ac - bd) + j(ad + bc) \quad \Rightarrow \quad 4 \ \text{DSP}
$$

优化实现（3 实数乘法 + 5 实数加法）：

$$
\begin{aligned}
p_1 &= (a - b) \cdot d, \quad p_2 = (c - d) \cdot a, \quad p_3 = (c + d) \cdot b \\
\text{Re} &= p_2 - p_3, \quad \text{Im} = p_1 + p_2
\end{aligned}
$$

需 3 个 DSP。

**定义**：
- $a, b$: 输入复数 1 的实部和虚部（$W$-bit 定点数）
- $c, d$: 输入复数 2 的实部和虚部（$W$-bit 定点数）
- DSP: FPGA 中的 DSP48E 单元

**来源**：通用公式；董凡 2024 §5.5.2

**适用条件**：3 乘法器算法适用于 DSP 资源受限但加法器充足的场景

**验证方式**：取测试数据，对比直接实现和优化实现的输出一致性

**备注**：董凡 2024 中载波恢复模块共使用 352 个 DSP（占 9.78%），主要消耗在 FFT IP 核内部的复数乘法。

---

### F5.23 移位寄存器/延迟链资源

$$
R_{\text{delay}} = P \times W \times D_{\text{cycles}} \ \text{FF}
$$

**定义**：
- $R_{\text{delay}}$: 延迟链所需触发器数量（个）
- $P$: 并行路数，取 32
- $W$: 数据位宽（bit），取 12
- $D_{\text{cycles}}$: 需要延迟的时钟周期数
- FF: FPGA 中的触发器

**来源**：通用公式；董凡 2024 §5.3/§5.4 delay_chain 模块

**适用条件**：用于对齐 FOE/CPE 估计延迟和原始数据流

**验证方式**：检查综合报告中 FF 使用量与理论值一致

**备注**：32 路 12 bit 数据延迟 1 个周期需 $32 \times 12 = 384$ 个 FF。

---
> F5.24-F5.26 已归档：见 `_archive/formulas-superseded-2026-07-14.md`。
### F5.27 系统资源利用率（参考数据）

载波恢复模块（CR）总资源占用（董凡 2024，Xilinx XC7K325T）：

| 资源类型 | CR 总占用 | FOE 占比 | CPE 占比 | 占芯片百分比 |
|:---|---:|:---|:---|:---|
| Slice LUTs | 66,193 | 96.1% | 3.9% | 15.28% |
| Slice Regs | 96,166 | 98.6% | 1.4% | 11.10% |
| BRAM | 20.5 | 100% | 0% | 1.39% |
| DSPs | 352 | 100% | 0% | 9.78% |

**来源**：董凡 2024 表 5-19

**备注**：FOE 模块消耗绝大部分资源。联合频偏估计算法相比两级 ArgFFT 算法减少了 42% LUT 和 50% DSP（表 5-20）。

---

### F5.28 角度差分求余（arg_diff 模块）

$$
\phi_{\text{diff}} = (\phi_0 - \phi_1) \mod \frac{\pi}{2}, \quad \phi_{\text{diff}} \in \left[0, \frac{\pi}{2}\right]
$$

硬件实现：对差值 $\Delta\phi = \phi_0 - \phi_1$ 进行多组常数补偿，通过比较器判断符号位确定所在范围。优化后仅需 3 个加法器（优化前需 7 个，减少 57%）。

**定义**：
- $\phi_{\text{diff}}$: 差分求余后的输出（rad，1Q9 格式 11 bit）
- $\phi_0, \phi_1$: 输入的两路角度信号（rad，2Q9 格式 12 bit）
- $\Delta\phi = \phi_0 - \phi_1$: 原始角度差（rad）

**来源**：董凡 2024 §5.3.2 arg_diff 模块

**适用条件**：输入差值范围 $(-7\pi/4, 9\pi/4]$；输出范围 $[0, \pi/2]$

**验证方式**：取各范围边界值，验证输出落入 $[0, \pi/2]$

**备注**："先选后加"优化思路减少加法器数量。32 路并行共节省 32 个加法器。
