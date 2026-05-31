# Ch3 (信道估计) + Ch4 (载波同步) 公式提取

> 生成时间: 2026-05-30
> 来源: 参考学位论文(张岱2018, 闫佳欣, 夏兆宇), 期刊论文(Liu 2023, Fernandes 2023), 仿真代码(sim_direction_a.py, sim_ch3_precomp.py, sim_cascade_robustness.py, sim_prototype.py), 内容卡片(material-section-content-cards.md), R016解析公式推导

---

## 第三章 大气湍流信道估计技术

> **废弃声明 (2026-05-30)**：原第三章"信道估计"已合并至 Ch2 §2.4。
> 以下公式 F3.1-F3.14 中信号模型和 SNR 定义仍使用旧约定（γ=γ̄·|h|²），
> 需结合 D011 决策更新为 γ=γ̄·h。新 Ch3 方向为"链路性能分析"，公式见
> `formulas-ch3-link-performance.md`。

### 3.2 湍流信道估计问题建模

#### F3.1 接收信号模型

$$r[k] = \sqrt{h[k]} \cdot s[k] \cdot e^{j\phi[k]} + n[k]$$

- **来源**: 内容卡片 2.2.2, R016信号模型定义
- **前文**: "在相干检测系统中，接收端信号由发送符号经信道衰落、载波相位偏移和噪声叠加组成"
- **物理意义**: 完整的离散时间接收信号模型。h[k]为归一化辐照度（GG分布），√h[k]为信道幅度系数，s[k]为QPSK发送符号，φ[k]为总载波相位（含频偏+相位噪声），n[k]为AWGN（LO散粒噪声主导，恒定方差）
- **与前后公式关系**: 是Ch3(估计h)和Ch4(估计φ)共同的出发点
- **参数**: $s[k] \in \{(1\pm j)/\sqrt{2}\}$，QPSK符号满足 $s^4 = -1$；$n[k] \sim \mathcal{CN}(0, \sigma_n^2)$，$\sigma_n^2 = 1/(2\bar\gamma)$

#### F3.2 Gamma-Gamma信道模型

$$h = X \cdot Y, \quad X \sim \text{Gamma}(\alpha, 1/\alpha), \quad Y \sim \text{Gamma}(\beta, 1/\beta)$$

$$f_{GG}(I) = \frac{2(\alpha\beta)^{(\alpha+\beta)/2}}{\Gamma(\alpha)\Gamma(\beta)} I^{(\alpha+\beta)/2 - 1} K_{\alpha-\beta}(2\sqrt{\alpha\beta I})$$

- **来源**: Fernandes 2023 式(GG PDF定义), 内容卡片 2.3.2, sim_prototype.py:29-31 (`gg_channel`/`gg_block`)
- **前文**: "大气湍流对接收光功率的影响可用Gamma-Gamma分布描述，该模型覆盖弱到强全范围湍流条件"
- **物理意义**: GG分布将湍流分解为大尺度(X, 衍射效应)和小尺度(Y, 干涉效应)两个独立Gamma过程的乘积。$\alpha$为大尺度涡旋有效数，$\beta$为小尺度涡旋有效数
- **与前后公式关系**: 定义了F3.1中h[k]的统计特性，是后续所有信道估计和自适应算法的统计基础
- **参数**:
  - 弱湍流: $\alpha=4.0, \beta=3.0$
  - 中湍流: $\alpha=2.5, \beta=1.8$
  - 强湍流: $\alpha=1.5, \beta=0.8$
  - $K_{\alpha-\beta}(\cdot)$ 为第二类修正Bessel函数

#### F3.3 块衰落模型

$$h[k] = h_b, \quad k \in [b \cdot B_s, (b+1) \cdot B_s - 1]$$

- **来源**: sim_prototype.py:33-36, sim_direction_a.py:57-62
- **前文**: "由于FSO信道相干时间远大于符号周期，采用块衰落模型"
- **物理意义**: 每个块内信道增益不变（相干时间假设），块间独立变化。块大小 $B_s$ 由相干时间决定
- **与前后公式关系**: 简化F3.2的逐符号衰落为逐块衰落，使导频设计和信道估计可操作
- **参数**: $B_s = 100$ 符号/块（仿真代码硬编码）

#### F3.4 导频辅助信道估计信号模型

$$y_p = h \cdot x_p + n, \quad p \in \mathcal{P}$$

- **来源**: 内容卡片 3.2.1, sim_prototype.py:55-63 (`make_frame`)
- **前文**: "在导频位置插入已知符号，接收端利用导频位置观测估计信道"
- **物理意义**: 导频辅助估计的基本观测方程。$\mathcal{P}$为导频位置集合，$x_p$为已知导频符号
- **与前后公式关系**: F3.1在导频位置的简化形式（载波相位可通过后处理消除）
- **参数**: 导频间距 $D_p = 8$ 符号，导频符号 $x_p = (1+j)/\sqrt{2}$

#### F3.5 瞬时SNR与NMSE定义

$$\gamma[k] = \bar\gamma \cdot h[k]$$

$$\text{NMSE} = \frac{E[|h - \hat{h}|^2]}{E[|h|^2]}$$

- **来源**: 内容卡片 2.2.3, sim_prototype.py:53 (`nmse`函数)
- **前文**: "定义瞬时SNR和归一化均方误差作为统一的评价指标"
- **物理意义**: $\gamma[k]$ 是瞬时SNR（相干检测：$\gamma = \bar\gamma \cdot h$，$h$为归一化辐照度），NMSE量化信道估计精度
- **与前后公式关系**: $\bar\gamma$是系统设计参数，$\gamma[k]$是Ch4自适应公式的输入；NMSE是3.4级联分析的核心自变量
- **参数**: $\bar\gamma = 100$ (20 dB) 为平均SNR

### 3.3 信道估计方法

#### F3.6 LS信道估计

$$\hat{h}_{LS}[p] = \frac{y_p}{x_p}$$

$$\hat{h}_{LS}[k] = \text{interp}\left(\hat{h}_{LS}[p], p \in \mathcal{P}\right)[k]$$

- **来源**: sim_prototype.py:123-125 (`ls_est`), 内容卡片 3.3.1
- **前文**: "最小二乘估计直接用接收信号除以导频符号，无需信道先验知识"
- **物理意义**: LS估计器在导频位置做除法得到信道估计值，再通过线性插值扩展到全帧。低SNR下噪声被直接放大
- **与前后公式关系**: F3.4的直接求解，是最简单的估计方法，作为所有对比实验的基线
- **参数**: 插值方式为线性插值（`interp1d(kind='linear')`）
- **典型性能**: 弱/中/强湍流 NMSE = -19.6/-17.5/-17.0 dB @20dB SNR (R010数据)

#### F3.7 MMSE信道估计

$$\hat{h}_{MMSE}[p] = c \cdot \hat{h}_{LS}[p], \quad c = \frac{\sigma_h^2}{\sigma_h^2 + \sigma_n^2}$$

- **来源**: sim_prototype.py:127-133 (`mmse_est`), 内容卡片 3.3.1
- **前文**: "MMSE利用信道二阶统计量抑制低SNR下的噪声放大"
- **物理意义**: 对LS估计做软缩放——SNR高时接近LS，SNR低时向零收缩。需要信道方差 $\sigma_h^2$ 的先验知识
- **与前后公式关系**: 在F3.6基础上引入统计加权，是LS的统计最优改进
- **参数**: $\sigma_n^2 = 1/\bar\gamma$，$\sigma_h^2 = \text{Var}(h_{true}[p])$

#### F3.8 AR(1)信道时变模型（Kalman/预测基础）

$$\ln I[k] = \rho \cdot \ln I[k-1] + \sqrt{1 - \rho^2} \cdot \sigma_{\ln} \cdot w[k]$$

$$\rho = e^{-T_{step}/T_{coh}}$$

- **来源**: sim_ch3_precomp.py:52-73 (`correlated_fading`), sim_cascade_robustness.py:158-167
- **前文**: "GG衰落的时间相关性可用AR(1)对数正态过程近似"
- **物理意义**: 对数光强的一阶自回归模型。$\rho$为自相关系数（由相干时间决定），$\sigma_{\ln}^2$为对数光强方差
- **与前后公式关系**: 为Kalman滤波（3.3.2）提供状态空间模型，为AR预测（3.4.2预补偿）提供预报方程
- **参数**:
  - 弱湍流: $T_{coh} = 10$ ms, $\sigma_I^2 = 1/\alpha + 1/\beta$
  - 中湍流: $T_{coh} = 5$ ms
  - 强湍流: $T_{coh} = 2$ ms
  - $T_{step} = 0.1$ ms（采样间隔）
  - $\sigma_{\ln}^2 = \ln(1 + \sigma_I^2)$
  - 均值修正: $I = \exp(\ln I - \sigma_{\ln}^2/2)$，保证 $E[I] = 1$

#### F3.9 AR(1)最优预测（MMSE预测器）

$$\hat{\ln I}(t) = \rho^k \cdot \ln I(t-k)$$

$$\sigma_{pred}^2 = \sigma_{\ln}^2 \cdot (1 - \rho^{2k})$$

$$\hat{I}_{pred} = \exp\left(\hat{\ln I} + \frac{\sigma_{pred}^2}{2} - \frac{\sigma_{\ln}^2}{2}\right)$$

- **来源**: sim_ch3_precomp.py:111-156 (`run_trial_ar`), sim_cascade_robustness.py:258-263
- **前文**: "AR(1)最优预测利用延迟观测做MMSE预报，k为延迟对应的采样点数"
- **物理意义**: 延迟k个采样后的MMSE预测。$\rho^k < 1$使估计向均值收缩，延迟越大预测越保守。$\sigma_{pred}^2$为预测误差方差
- **与前后公式关系**: F3.8的预测形式，是3.4.2节"预补偿+AR预测"的核心公式
- **参数**: $k = \tau / T_{step}$，$\tau$为反馈延迟（ms）

### 3.4 估计精度对下游信号处理的影响分析

#### F3.10 信道估计噪声注入模型

$$\hat{h} = |h + n_h|, \quad n_h \sim \mathcal{N}\left(0, |h|^2 \cdot 10^{-\text{NMSE}_{dB}/20}\right)$$

- **来源**: sim_cascade_robustness.py:59-64 (`add_h_noise`)
- **前文**: "为分析估计精度对下游模块的影响，在真实信道增益上叠加可控NMSE的高斯噪声"
- **物理意义**: 构造指定NMSE水平的信道估计值。噪声标准差与h幅度成正比（相对误差模型）
- **与前后公式关系**: 连接Ch3（估计方法输出NMSE）与Ch4（输入含噪h到载波同步），是级联分析的核心接口
- **参数**: NMSE级别: -5, -10, -15, -20 dB（100代表完美估计无噪声）

#### F3.11 MMSE信道补偿（接收端）

$$\tilde{r}[k] = r[k] \cdot \frac{\sqrt{\hat{h}^*[k]}}{\hat{h}[k] + 1/\bar\gamma}$$

- **来源**: sim_direction_a.py:303-304, sim_cascade_robustness.py:197
- **前文**: "载波恢复前做MMSE信道补偿，避免深衰落噪声爆炸"
- **物理意义**: MMSE均衡——对信道系数√h做共轭除法，正则项 $1/\bar\gamma$ 防止深衰落时噪声被过度放大。信道系数为√h，|√h|²=h，所以分母用辐照度h
- **与前后公式关系**: 在F3.1接收信号基础上消除h（信道均衡），残余载波相位留给Ch4处理
- **参数**: 后接幅度限制 $\text{amp\_limit}(\tilde{r}, 3.0)$，防止极端值

#### F3.12 功率预补偿模型（发射端，Ch3.4.2证明不可行）

$$P_{tx}(t) = \min\left(\frac{1}{|\hat{h}_{pred}(t-\tau)|^2}, P_{cap}\right), \quad \bar{P}_{tx} = 1$$

- **来源**: sim_ch3_precomp.py:102-104, sim_cascade_robustness.py:267-269
- **前文**: "发射端根据延迟信道估计做功率预补偿，补偿后平均功率归一化"
- **物理意义**: 发射端功率反转补偿——深衰落时增加发射功率。$P_{cap}$限制峰值功率
- **与前后公式关系**: 与F3.11（接收端MMSE补偿）对比：发射端需要精确的h预测，接收端只需粗略估计。3.4.2节证明此方案在真实估计噪声下全面FAIL
- **参数**: $P_{cap} = 100$（20 dB峰值功率限制）

#### F3.13 QPSK理论BER（级联分析用）

$$\text{BER}(\gamma) = \frac{1}{2}\text{erfc}\left(\sqrt{\frac{\gamma}{2}}\right)$$

$$\bar{\text{BER}} = E_h\left[\text{BER}(\bar\gamma \cdot h)\right]$$

- **来源**: sim_ch3_precomp.py:76-79 (`qpsk_ber_avg`)
- **前文**: "QPSK在AWGN下的理论误码率，对瞬时SNR取统计平均"
- **物理意义**: 给定瞬时SNR的QPSK BER解析表达式，对GG信道h取期望得到平均BER
- **与前后公式关系**: 用于计算3.4节级联灵敏度曲线——不同NMSE水平下的BER退化

### 3.5 仿真参数

#### F3.14 信道估计仿真参数表

| 参数 | 弱湍流 | 中湍流 | 强湍流 | 来源 |
|------|--------|--------|--------|------|
| GG $\alpha$ | 11.6 | 4.0 | 2.0 | sim_prototype.py:24 |
| GG $\beta$ | 10.9 | 1.9 | 1.5 | sim_prototype.py:24 |
| 块大小 $B_s$ | 100 | 100 | 100 | sim_prototype.py:25 |
| 导频间距 $D_p$ | 8 | 8 | 8 | sim_prototype.py:26 |
| 相干时间 $T_{coh}$ | 10 ms | 5 ms | 2 ms | sim_ch3_precomp.py:35-38 |
| 平均SNR $\bar\gamma$ | 20 dB | 20 dB | 20 dB | R010参数 |
| 采样间隔 $T_{step}$ | 0.1 ms | 0.1 ms | 0.1 ms | sim_ch3_precomp.py:46 |
| 功率上限 $P_{cap}$ | 100 (20dB) | 100 | 100 | sim_ch3_precomp.py:43 |
| MLP结构 | - | 3层, 64隐单元 | - | sim_prototype.py:152-153 |

---

## 第四章 低轨星地载波同步算法

### 4.2 载波同步系统模型

#### F4.1 总载波相位模型

$$\phi[k] = 2\pi f_{res} \cdot kT_s + \pi \dot{f}_D \cdot (kT_s)^2 + \theta_L[k]$$

$$\theta_L[k] = \sqrt{2\pi \Delta\nu_L T_s} \cdot \sum_{i=0}^{k} w[i], \quad w[i] \sim \mathcal{N}(0, 1)$$

- **来源**: sim_direction_a.py:97-109 (`doppler_phase`), 内容卡片 4.2
- **前文**: "载波相位由三部分组成：残余频偏引起的线性相移、多普勒率引起的二次相移、激光线宽引起的维纳相位噪声"
- **物理意义**: 三分量物理模型——(1) $f_{res}$: 星历预补偿后的残余频偏；(2) $\dot{f}_D$: 多普勒变化率（频率斜坡）；(3) $\theta_L$: 激光相位噪声（维纳过程，$\Delta\nu_L$为激光线宽）
- **与前后公式关系**: F3.1中 $\phi[k]$ 的展开形式，定义了Ch4需要估计和补偿的全部载波损伤
- **参数**:
  - $T_s = 1/R_{SYM} = 0.4$ ns（符号率 2.5 Gsps）
  - $f_{res} = 1$ MHz（预补偿后残余频偏）
  - $\dot{f}_D = 150$ MHz/s（低仰角）/ 30 MHz/s（高仰角）
  - $\Delta\nu_L = 10$ kHz（激光线宽）

#### F4.2 Doppler频偏物理模型

$$f_{DS} = f_c \cdot \frac{v_r}{c}$$

$$v_r(t) = \omega_F R_E \sin(\omega_F t + \psi_{diff})$$

$$\omega_F \approx \omega_S - \omega_E \cos(i_S)$$

- **来源**: Fernandes 2023 Section II-A
- **前文**: "多普勒频移由卫星与地面站的相对径向速度决定"
- **物理意义**: Doppler频偏 = 载频 x (径向速度/光速)。LEO场景下径向速度随时间变化，产生时变频偏
- **与前后公式关系**: F4.1中 $f_{res}$ 和 $\dot{f}_D$ 的物理来源——Doppler频偏经星历预补偿后残余的部分
- **参数**:
  - LEO 500km高度: $f_{DS,max} \approx \pm 4$ GHz（Fernandes 2023 Fig.1）
  - Zhao 2025参数: $\pm 8$ GHz范围，$\dot{f}_D = 150$ MHz/s
  - 预补偿后残余: $f_{res} \sim 1$ MHz（Zhao 2025）

#### F4.3 接收符号相位分解（四次方FOE基础）

$$\theta_r[k] = \theta_s[k] + \Delta\omega \cdot kT_s + \theta_n[k] + \theta_a[k]$$

- **来源**: 闫佳欣 式(2-24)
- **前文**: "接收符号的相位由调制相位、频偏引起的相位、激光相位噪声和其他噪声组成"
- **物理意义**: 将接收相位分解为四个分量：$\theta_s[k]$为QPSK调制相位，$\Delta\omega \cdot kT$为频偏线性相移，$\theta_n$为激光相位噪声（慢变），$\theta_a$为其他噪声
- **与前后公式关系**: F4.1的QPSK特化形式。四次方运算可消除 $\theta_s$（因为QPSK $s^4 = -1$），共轭差分可消除 $\theta_n$

### 4.3 湍流自适应频偏估计算法

#### F4.4 FFT频偏估计（四次方法）

$$r_4[k] = (r[k])^4, \quad k = 0, \ldots, N-1$$

$$R_4(f) = \text{FFT}\{r_4[k] \cdot w_{Hann}[k]\}$$

$$\hat{f}_{offset} = \frac{1}{4} \cdot \arg\max_f |R_4(f)|$$

- **来源**: sim_direction_a.py:114-142 (`fft_foe`), 闫佳欣 式(2-25)-(2-27), Liu 2023 Section 2
- **前文**: "对QPSK信号做四次方运算消除调制相位，然后通过FFT峰值检测估计频偏"
- **物理意义**: 利用QPSK的 $s^4 = -1$ 恒等式，四次方后调制信息被消除，残余频偏被放大4倍。FFT峰值位置给出频偏估计
- **与前后公式关系**: 基于F4.3的相位分解——四次方消除 $\theta_s$，FFT平均抑制 $\theta_a$，残余 $\theta_n$ 和频偏体现在峰值位置
- **参数**:
  - FFT窗口 $N$: 固定1024 / 自适应（见F4.6）
  - 零填充: $N_{zp} = 8192$（提高频率分辨率）
  - 窗函数: Hanning窗
  - 抛物线插值提高峰值定位精度

#### F4.5 四次方运算的SNR退化

$$\text{SNR}_4 = \frac{\bar\gamma \cdot h}{8}$$

- **来源**: R016推导1, 内容卡片 4.3.1
- **前文**: "四次方运算在消除调制信息的同时引入了非线性噪声，等效SNR退化"
- **物理意义**: 四次方后等效SNR正比于 $h$——深衰落时SNR下降，导致FFT峰值检测失败。信号功率 = $h \cdot |s|^2$，噪声分析后 $\text{SNR}_4 = \bar\gamma h / 8$
- **与前后公式关系**: 解释了F4.4为什么在h很小时失效，直接推导出F4.6的自适应窗口公式

#### F4.6 [核心公式1] FFT窗口自适应

$$N_{opt}(h) = \frac{80}{\bar\gamma \cdot h^2}$$

$$N_{fft} = \text{clamp}\left(2^{\lceil\log_2 N_{opt}\rceil}, 256, 8192\right)$$

- **来源**: sim_direction_a.py:223-226 (`adaptive_params`), R016推导1, 内容卡片 4.3.2
- **前文**: "深衰落下四次方SNR过低导致FFT峰值检测失败，需增大窗口长度以积累更多信号能量"
- **物理意义**: $h^{-2}$依赖——h越小需要的FFT窗口越长。分子80由虚警概率和检测概率约束推导。取2的幂次便于FFT计算
- **与前后公式关系**: 由F4.5推导——给定目标检测SNR，反推所需的最小FFT点数
- **参数**:
  - 窗口范围: [256, 8192]
  - $h^2$ 下限: 0.001（防止数值发散）
  - h=0.05时 $N_{opt} = 80/(100 \times 0.0025) = 320$（正常）；h=0.3时 $N_{opt} = 80/(100 \times 0.09) = 8.9$（取下限256）
  - 固定配置基准: $N=1024$（Zhao 2025）

### 4.4 湍流自适应载波相位恢复算法

#### F4.7 二阶数字锁相环（DPLL）

$$\text{鉴相器}: \quad e[k] = \frac{1}{4}\angle\left((r[k] \cdot e^{-j\hat\phi[k-1]})^4\right)$$

$$\text{环路滤波器}: \quad \nu[k] = c_1 \cdot e[k] + \Sigma[k]$$

$$\text{积分器}: \quad \Sigma[k] = \Sigma[k-1] + c_2 \cdot e[k]$$

$$\text{VCO}: \quad \hat\phi[k] = \hat\phi[k-1] + \nu[k]$$

$$c_1 = 2\zeta\omega_n T_s, \quad c_2 = (\omega_n T_s)^2$$

- **来源**: sim_direction_a.py:147-192 (`dpll_track`), Liu 2023 Section 2, 闫佳欣 第二章
- **前文**: "二阶DPLL通过QPSK四次方鉴相器提取相位误差，环路滤波器平滑噪声，VCO跟踪相位变化"
- **物理意义**: 经典二阶锁相环的数字实现。$\zeta$为阻尼系数（通常取 $\sqrt{2}/2$），$\omega_n$为自然频率（决定环路带宽 $B_L \approx 0.53\omega_n$，$\zeta=\sqrt{2}/2$ 时）。带宽越大跟踪越快但噪声通过越多
- **与前后公式关系**: FFT-FOE补偿频偏后的细跟踪——FOE处理粗频偏，DPLL跟踪残余频偏和相位噪声
- **参数**:
  - $\zeta = \sqrt{2}/2$（临界阻尼）
  - 固定: $\omega_n = 8 \times 10^6$ rad/s（Zhao 2025配置）
  - 自适应: 见F4.10
  - $\omega_n T_s$ 上限: 0.5（稳定性约束）

#### F4.8 Viterbi-Viterbi载波相位恢复（CPR）

$$\hat\theta}[k] = \frac{1}{M}\text{unwrap}\left(\angle\left(\sum_{i=k-M/2}^{k+M/2} r[i]^4\right)\right)$$

$$r_{comp}[k] = r[k] \cdot e^{-j\hat\theta}[k]}$$

- **来源**: sim_direction_a.py:197-210 (`vv_cpr`), sim_prototype.py:284-298 (`vv`), 闫佳欣 式(2-28)-(2-29), Liu 2023 Section 2
- **前文**: "VV算法对QPSK信号四次方取滑动平均，提取载波相位噪声估计"
- **物理意义**: 窗口M内对四次方信号取平均消除调制分量，unwrap保持相位连续性，除以4恢复实际相位。窗口M是噪声抑制（大M）和相位跟踪（小M）的折中
- **与前后公式关系**: DPLL之后的残留相位噪声补偿。DPLL处理频偏/低频相位，VV处理高频相位噪声
- **参数**:
  - QPSK: $M_{order} = 4$（四次方）
  - 固定: $M = 64$（Zhao 2025配置）
  - 自适应: 见F4.9
  - 幅度裁剪: $|r^4| > 10^8$ 时裁剪（防溢出）

#### F4.9 [核心公式2] VV窗口自适应

$$M_{opt}(h) = K_M \cdot (\bar\gamma \cdot h)^{-1/5} \cdot (\Delta f_{res} \cdot T_s)^{-2/5}$$

$$K_M = (3/4)^{1/5} \approx 0.944$$

$$M_{vv} = \text{clamp}\left(\text{odd\_round}(M_{opt}), 9, 255\right)$$

- **来源**: sim_direction_a.py:228-233 (`adaptive_params`), R016推导2, 内容卡片 4.4
- **前文**: "VV窗口M面临噪声抑制和相位跟踪的折中——最优M由SNR和残余频偏共同决定"
- **物理意义**: 5次根号定律——M正比于 $(SNR)^{-1/5}$ 和 $(\Delta f \cdot T_s)^{-2/5}$。高SNR或低残余频偏时可用短窗口（跟踪快），反之需长窗口（噪声抑制）。$h^{-1/5}$ 依赖比FOE的 $h^{-2}$ 温和
- **与前后公式关系**: 由F4.8中VV窗口M的MSE解析最小化推导——MSE = 噪声项 + 频偏漂移项，对M求导=0
- **参数**:
  - 窗口范围: [9, 255]（确保奇数）
  - $\Delta f_{res} \cdot T_s = 10^6 \times 4\times10^{-10} = 4\times10^{-4}$（残余频偏归一化）
  - 代码: `df_norm = F_RESIDUAL * T_S`

#### F4.10 [核心公式3] DPLL带宽自适应

$$B_{L,opt}(h) = B_0 \cdot h$$

$$B_0 = \sqrt{\frac{\pi \Delta\nu_L \bar\gamma}{T_s}}$$

$$\omega_{n,opt} = \frac{B_{L,opt}}{0.53}$$

- **来源**: sim_direction_a.py:236-238 (`adaptive_params`), sim_cascade_robustness.py:145-148, R016推导3, 内容卡片 4.4
- **前文**: "DPLL最优带宽在相位噪声跟踪和噪声抑制间取折中——带宽正比于瞬时SNR的平方根"
- **物理意义**: $B_0$ 是无衰落时的最优带宽基准，$h$ 调制适应瞬时信道条件。$h$ 大（信道好）→带宽大→跟踪快；$h$ 小（深衰落）→带宽小→抑制噪声。线性 $h$ 依赖（最温和的三种自适应之一）。注意：$B_0 \cdot h$ 是设计选择（实现h抵消），非Wiener最优（Wiener给出 $B_0 \cdot \sqrt{h}$）
- **与前后公式关系**: F4.7中 $\omega_n$ 的自适应版本。三种自适应公式分别对应 $h^{-2}$（FOE，阈值效应）、$h^{-1/5}$（VV，平滑调整）、$h^1$（DPLL，线性缩放）
- **参数**:
  - $B_L$ 范围: [0.5, 20] MHz（代码: `B_L = np.clip(B0 * h, 0.5e6, 20e6)`）
  - $B_0$ 典型值: $\sqrt{\pi \times 10^4 \times 100 / 4\times10^{-10}} \approx 8.9 \times 10^7$ Hz（~89 MHz）
  - $B_L \approx 0.53\omega_n$，即 $\omega_n \approx B_L/0.53$（⚠️ 仿真代码误用 $B_L/1.06$，差约2倍）

#### F4.11 完整载波恢复链

**固定参数链**:

$$\hat{f}_{FOE} = \text{FFT-FOE}(r, N=1024)$$
$$\to r_1 = r \cdot e^{-j\hat{f}_{FOE} \cdot k}$$
$$\to r_2 = \text{DPLL}(r_1, \omega_n=8\times10^6, \zeta=\sqrt{2}/2)$$
$$\to r_{out} = \text{VV-CPR}(r_2, M=64)$$

**自适应链（DPLL带宽自适应）**:

$$\hat{f}_{FOE} = \text{FFT-FOE}(r, N=1024)$$
$$\to r_1 = r \cdot e^{-j\hat{f}_{FOE} \cdot k}$$
$$\to B_L = \min(\max(B_0 \cdot h_{est}, 0.5\text{MHz}), 20\text{MHz})$$
$$\to r_2 = \text{DPLL}(r_1, \omega_n = B_L/0.53)$$
$$\to r_{out} = \text{VV-CPR}(r_2, M=64)$$

- **来源**: sim_direction_a.py:245-272 (`carrier_recovery_fixed/adaptive`), 内容卡片 4.2.3
- **前文**: "载波恢复采用FOE+DPLL+VV三级级联结构，自适应版本仅调整DPLL带宽"
- **物理意义**: FFT-FOE做粗频偏估计和补偿 → DPLL跟踪残余频偏和低频相位 → VV补偿高频相位噪声。自适应链仅DPLL带宽随h变化（MVE验证此配置已足够）
- **与前后公式关系**: F4.4+F4.7+F4.8的串联实现
- **参数**: 与F4.1/F4.4/F4.7/F4.8中各参数一致

### 4.5 仿真参数

#### F4.12 载波同步仿真参数表

| 参数 | 值 | 来源 |
|------|-----|------|
| 符号率 $R_{SYM}$ | 2.5 Gsps | Zhao 2025 |
| 符号周期 $T_s$ | 0.4 ns | $1/R_{SYM}$ |
| 光载频 $f_c$ | $1.55 \times 10^{14}$ Hz | ~1550 nm |
| 激光线宽 $\Delta\nu_L$ | 10 kHz | Zhao 2025 |
| Doppler变化率（低仰角） | 150 MHz/s | Zhao 2025 |
| Doppler变化率（高仰角） | 30 MHz/s | Wang 2025 |
| 残余频偏 $f_{res}$ | 1 MHz | Zhao 2025 |
| FFT窗口（固定） | 1024 | Zhao 2025 |
| VV窗口（固定） | 64 | Zhao 2025 |
| DPLL自然频率（固定） | $8 \times 10^6$ rad/s | Zhao 2025 |
| DPLL阻尼系数 $\zeta$ | $\sqrt{2}/2$ | 临界阻尼 |
| 零填充FFT点数 | 8192 | 提高频率分辨率 |
| 幅度限制阈值 | 3.0 | 防止深衰落噪声爆炸 |
| GG湍流参数 | 见F3.2 | 同Ch3 |
| 每帧符号数 | 2000 | MVE配置 |
| 试验次数 | 20 | 统计平均 |
| 仿真场景 | 3湍流 $\times$ 2仰角 = 6种 | 覆盖主要工况 |

#### F4.13 MVE场景配置

| 场景标签 | 湍流 | 仰角 | Doppler率 | GG $(\alpha,\beta)$ |
|----------|------|------|-----------|---------------------|
| weak_low | 弱 | 低 | 150 MHz/s | (4.0, 3.0) |
| weak_high | 弱 | 高 | 30 MHz/s | (4.0, 3.0) |
| moderate_low | 中 | 低 | 150 MHz/s | (2.5, 1.8) |
| moderate_high | 中 | 高 | 30 MHz/s | (2.5, 1.8) |
| strong_low | 强 | 低 | 150 MHz/s | (1.5, 0.8) |
| strong_high | 强 | 高 | 30 MHz/s | (1.5, 0.8) |

### 4.6 三个核心自适应公式交叉验证

#### F4.14 三种h依赖形态对比

| 自适应模块 | 公式 | h依赖 | 物理含义 |
|-----------|------|-------|---------|
| FFT-FOE窗口 | $N_{opt} = 80/(\bar\gamma \cdot h^2)$ | $h^{-2}$ | 深衰落阈值效应——SNR急剧下降 |
| VV窗口 | $M_{opt} = K_M (\bar\gamma h)^{-1/5}(\Delta f T_s)^{-2/5}$ | $h^{-1/5}$ | 平滑折中——5次根号定律 |
| DPLL带宽 | $B_{L,opt} = B_0 \cdot h$ | $h^{1}$ | 线性缩放——最温和的自适应 |

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
omega_n = B_L / 0.53  # ⚠️ 原代码误用 1.06，正确应为 0.53
```

**参考文献交叉验证**:

| 公式 | 论文依据 | 代码依据 | 一致性 |
|------|---------|---------|--------|
| $N_{opt}(h)$ | R016推导1（SNR₄=C阈值反推） | sim_direction_a.py:224 | 一致 |
| $M_{opt}(h)$ | R016推导2（VV MSE最小化） | sim_direction_a.py:229-232 | 一致 |
| $B_{L,opt}(h)$ | R016推导3（DPLL最优带宽） | sim_direction_a.py:236-238 | 一致 |
| 四次方FOE | 闫佳欣式(2-25)-(2-27), Liu 2023 | sim_direction_a.py:114-142 | 一致 |
| VV CPR | 闫佳欣式(2-28)-(2-29), Liu 2023 | sim_direction_a.py:197-210 | 一致 |
| Doppler模型 | Fernandes 2023, Zhao 2025 | sim_direction_a.py:97-109 | 一致 |

---

## 跨章公式依赖图

```
Ch2 系统模型
  F3.1 r[k] = √h·s·exp(jφ) + n          ← 全文出发点
    │
    ├──→ Ch3 信道估计（估计h）
    │     F3.2 GG分布 h=X·Y
    │     F3.4 导频观测 y_p = h·x_p + n
    │     F3.6 LS估计 ĥ = y/x
    │     F3.7 MMSE估计 ĥ = c·(y/x)
    │     F3.8 AR(1)模型（Kalman基础）
    │     F3.10 噪声注入模型（级联接口）
    │     F3.11 MMSE补偿（接收端均衡）
    │     F3.12 功率预补偿（证明不可行）
    │         │
    │         └──→ 3.4 级联结论: NMSE≥-10dB → 载波同步可靠
    │
    └──→ Ch4 载波同步（估计φ）
          F4.1 φ = 2πf_res·kT + πḟ·(kT)² + θ_L
          F4.2 Doppler物理模型
          F4.3 接收相位分解
          F4.4 FFT-FOE（四次方+FFT峰值）
          F4.5 SNR₄ = γ̄h/8
          F4.6 [核心1] N_opt = 80/(γ̄h²)     ← h⁻²依赖
          F4.7 二阶DPLL
          F4.8 VV-CPR
          F4.9 [核心2] M_opt = K_M(γ̄h)^{-1/5}... ← h⁻¹/⁵平滑折中
          F4.10 [核心3] B_L = B₀·h            ← h¹线性缩放
          F4.11 完整载波恢复链
```

---

## 缺失项列表

### 需要补充的公式

1. **F3.8 Kalman滤波完整状态空间方程** — AR(1)模型已知但Kalman递推方程（预测步+更新步）未在代码中显式实现，需从教科书补入

2. **F3.15 Rytov方差与GG参数的关系** — $\sigma_R^2 = 1.23 C_n^2 k^{7/6} L^{11/6}$，以及 $\alpha, \beta$ 与 $\sigma_R^2$ 的映射（内容卡片 2.3.3 提到但未展开）

3. **F4.5 SNR₄的完整推导** — 代码和内容卡片给出结论 $\text{SNR}_4 = \bar\gamma \cdot h^2/8$，但分子"80"和除数"8"的推导过程需补入（来自R016推导1）

4. **F4.9 M_opt的完整推导** — 5次根号定律的MSE最小化推导过程（来自R016推导2，未展开）

5. **F4.10 B_L_opt的完整推导** — DPLL最优带宽的Wiener滤波推导（来自R016推导3，未展开）

6. **F3.16 信道估计CRB（Cramer-Rao下界）** — 为MMSE性能提供理论下界，内容卡片未提及

7. **F4.14 相位模糊解决** — `resolve_qpsk` 函数尝试8种旋转取最优，但论文正文需给出QPSK $\pi/4$ 相位模糊的解析描述

### 需要确认的参数

1. **GG参数 $(\alpha,\beta)$ 与Rytov方差/物理场景的精确映射** — 目前三档参数为仿真用硬编码值，需确认是否与标准大气条件对应

2. **$B_0 = \sqrt{\pi \Delta\nu_L \bar\gamma / T_s}$ 的量纲和系数** — 代码中计算值约89MHz，需确认DPLL带宽公式的标准化形式

3. **FOE窗口公式中"80"的来源** — 来自检测概率约束 $P_d \geq 0.99$ 和虚警概率 $P_{fa} \leq 10^{-3}$ 的具体推导（R016推导1）

4. **VV窗口 $K_M = (3/4)^{1/5}$ 的推导** — 来自QPSK四次方的特定系数，需确认是否为标准值

### 需要从参考论文补充的内容

1. **Liu 2023 双反馈FOE的PADE算法细节** — 当前仅使用FFT前馈FOE，PADE（Pre-decision Angle Differential Estimator）作为反馈替代方案待评估

2. **闫佳欣 论文中的并行化FOE/VV实现** — FPGA实时实现的结构设计，对Ch5有参考价值

3. **张岱2018 的波前校正+自差探测** — 与本文的零差/外差方案不同，但偏振/相位恢复部分可交叉参考
