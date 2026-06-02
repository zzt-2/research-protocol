# Ch3 (信道估计) + Ch4 (载波同步) 公式提取

> 生成时间: 2026-05-30
> 来源: 参考学位论文(张岱2018, 闫佳欣, 夏兆宇), 期刊论文(Liu 2023, Fernandes 2023), 仿真代码(sim_direction_a.py, sim_ch3_precomp.py, sim_cascade_robustness.py, sim_prototype.py), 内容卡片(material-section-content-cards.md), R016解析公式推导

---

## 第三章 大气湍流信道估计技术

> **部分废弃声明 (2026-05-30, 更新 2026-06-01)**：原第三章"信道估计"已合并至 Ch2 §2.4。
> F3.1 信号模型使用 √h 系数（与新 Ch3 的 √γ 版本归一化约定不同）；
> F3.5 和 F4.5 等已更新为新约定 γ=γ̄·h。新 Ch3 方向为"链路性能分析"，公式见
> `formulas-master.md` Ch3 部分（F3.1-F3.21）。

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
- **与前后公式关系**: 定义了F3.1中h[k]的统计特性，是后续所有信道估计和参数优化方法的统计基础
- **参数**:
  - 弱湍流: $\alpha=4.0, \beta=3.0$
  - 中湍流: $\alpha=2.5, \beta=1.8$
  - 强湍流: $\alpha=1.5, \beta=0.8$
  - $K_{\alpha-\beta}(\cdot)$ 为第二类修正Bessel函数

#### F3.3 块衰落模型

$$h[k] = h_b, \quad k \in [b \cdot B_s, (b+1) \cdot B_s - 1]$$

- **来源**: sim_prototype.py:33-36, sim_direction_a.py:57-62
- **前文**: "由于FSO信道相干时间远大于符号周期，采用块衰落模型"
- **物理意义**: 每个块内归一化辐照度不变（相干时间假设），块间独立变化。块大小 $B_s$ 由相干时间决定
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

#### F3.9K Kalman滤波——状态空间模型

$$h[k] = a \cdot h[k-1] + w[k], \quad w[k] \sim \mathcal{N}(0, Q)$$

$$y[k] = x[k] \cdot h[k] + n[k], \quad n[k] \sim \mathcal{N}(0, R)$$

- **来源**: 标准Kalman滤波理论，F3.8的线性化版本
- **物理意义**: 状态方程描述信道h的一阶自回归演化（$a$为自相关系数），观测方程描述导频位置的线性观测。$Q$为过程噪声方差（信道变化率），$R$为观测噪声方差（与SNR相关）
- **参数**: $a = \rho = e^{-T_s/T_{coh}}$，$Q = (1-a^2)\sigma_h^2$，$R = \sigma_n^2 = 1/\bar\gamma$

#### F3.9L Kalman滤波——预测步骤

$$\hat{h}[k|k-1] = a \cdot \hat{h}[k-1]$$

$$P[k|k-1] = a^2 \cdot P[k-1] + Q$$

- **来源**: Kalman滤波标准预测方程
- **物理意义**: 基于上一时刻估计做一步外推。预测误差协方差$P[k|k-1]$包含模型不确定性($Q$)和上一时刻估计误差的传播($a^2 P[k-1]$)

#### F3.9M Kalman滤波——更新步骤与Kalman增益

$$K[k] = \frac{P[k|k-1] \cdot |x[k]|^2}{|x[k]|^2 \cdot P[k|k-1] + R}$$

$$\hat{h}[k] = \hat{h}[k|k-1] + K[k] \cdot (y[k] - x[k] \cdot \hat{h}[k|k-1])$$

$$P[k] = (1 - K[k] \cdot |x[k]|^2) \cdot P[k|k-1]$$

- **来源**: Kalman滤波标准更新方程
- **物理意义**: Kalman增益$K[k]$平衡预测与观测的置信度——SNR高时$K \to 1$（信任观测），SNR低时$K \to 0$（信任预测）。新息$y[k] - x[k]\hat{h}[k|k-1]$驱动修正
- **与前文关系**: F3.7的MMSE估计可视为KF的稳态特例（$a=1, Q=0$时退化为静态MMSE）

#### F3.9N Kalman滤波——稳态分析

$$K_\infty = \frac{-R + \sqrt{R^2 + 4R \cdot Q/a^2}}{2}$$

$$P_\infty = K_\infty \cdot R / |x|^2$$

- **来源**: Riccati方程稳态解
- **物理意义**: 当信道统计特性不变时，Kalman增益收敛到固定值，此时KF等效为最优线性时不变滤波器。可用于设计固定系数的低复杂度估计器

#### F3.9P 基于深度学习的信道估计

$$\hat{h} = f_\theta(\mathbf{y}_{\text{pilot}})$$

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} |\hat{h}_i - h_i|^2$$

- **来源**: 通用DL信道估计框架
- **物理意义**: $f_\theta$为参数化神经网络（FC/1D-CNN等），输入为导频位置观测向量，输出为信道估计值。损失函数为MSE。与LS/MMSE/KF不同，DL方法无需显式统计先验，但需要大量训练数据
- **说明**: 正文写作时可简化描述，重点在于与LS/MMSE/KF的性能对比，不展开网络结构细节

### 3.4 估计精度对下游信号处理的影响分析

#### F3.10 信道估计噪声注入模型

$$\hat{h} = |h + n_h|, \quad n_h \sim \mathcal{N}\left(0, |h|^2 \cdot 10^{-\text{NMSE}_{dB}/20}\right)$$

- **来源**: sim_cascade_robustness.py:59-64 (`add_h_noise`)
- **前文**: "为分析估计精度对下游模块的影响，在真实归一化辐照度上叠加可控NMSE的高斯噪声"
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

> **F4.1-F4.14 主从声明**：本文件 F4.1-F4.14 为 `formulas-master.md` 中对应公式的副本，以 `formulas-master.md` 为权威版本。本处保留供 Ch3/Ch4 联合阅读参考。

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

$$\theta_r[k] = \theta_s[k] + \Delta\omega \cdot kT_s + \theta_L[k] + \theta_a[k]$$

- **来源**: 闫佳欣 式(2-24)，符号已统一为本文约定（原文用 $\theta_n$ 表示激光相位噪声，本文统一用 $\theta_L$，见 F4.1）
- **前文**: "接收符号的相位由调制相位、频偏引起的相位、激光相位噪声和其他噪声组成"
- **物理意义**: 将接收相位分解为四个分量：$\theta_s[k]$为QPSK调制相位，$\Delta\omega \cdot kT$为频偏线性相移，$\theta_L$为激光相位噪声（即F4.1中的维纳过程，慢变），$\theta_a$为其他噪声
- **与前后公式关系**: F4.1的QPSK特化形式。四次方运算可消除 $\theta_s$（因为QPSK $s^4 = -1$），共轭差分可消除 $\theta_L$

### 4.3 分湍流条件频偏估计方法

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

### 4.4 分湍流条件载波相位恢复方法

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

$$\hat\phi_\text{raw}[k] = \frac{1}{M}\text{unwrap}\left(\angle\left(\sum_{i=k-M/2}^{k+M/2} r[i]^4\right)\right)$$

$$r_{comp}[k] = r[k] \cdot e^{-j\hat\phi_\text{raw}[k]}$$

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

> **单位说明**：$B_0$ 的量纲为 Hz（$\sqrt{\text{Hz}^2}$），$B_L$ 单位为 Hz。严格来说 $B_L = 0.53 f_n$（$f_n = \omega_n/(2\pi)$ 为自然频率的 Hz 值），代码中 `omega_n` 变量实际存储的是 $f_n$（Hz），因此 `omega_n = B_L/0.53` 在代码内自洽。论文正文中建议写为 $f_{n,opt} = B_{L,opt}/0.53$ 以避免 rad/s 与 Hz 混淆。

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
    │         └──→ 3.4 级联结论: NMSE 0~-20dB 范围内退化 <0.3dB → 载波同步可靠
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

3. **F4.5 SNR₄的完整推导** — 代码和内容卡片给出结论 $\text{SNR}_4 = \bar\gamma \cdot h/8$，但分子"80"和除数"8"的推导过程需补入（来自R016推导1）

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

---

## 第四章补充公式（Task A 缺口补全）

> 补充时间: 2026-06-01
> 来源: 丁爽(北邮), 张思齐(北邮), 董凡(电子科大), DPLL教材(Gardner/Rice/Robertson), FFT理论(Rife & Boorstyn 1974/Gasior & Gonzalez 2004)

### 4.2 补充 — 激光器相位噪声模型

#### F4.15 激光器相位噪声（Wiener过程）

$$\theta_L[k] = \theta_L[k-1] + w[k], \quad w[k] \sim \mathcal{N}(0, \sigma_{\theta,L}^2)$$

- **来源**: 丁爽 式(4-8), 董凡 式(2-27)
- **前文**: "激光相位噪声可建模为离散时间Wiener过程（随机游走）"
- **物理意义**: 相邻符号间相位噪声增量为零均值高斯，方差由激光线宽决定。这是VVPE均值滤波的理论基础——相邻符号相位近似不变（慢变假设）
- **与前后公式关系**: 定义F4.1中θ_L的统计特性，是DPLL/VV/BPS所有相位恢复算法的共同噪声源
- **参数**: σ_{θ,L}² 由 F4.16 确定

#### F4.16 相位噪声方差与线宽关系

$$\sigma_{\theta,L}^2 = 2\pi \Delta\nu_L \cdot T_s$$

- **来源**: 丁爽 式(4-8), 标准公式（Gardner *Phaselock Techniques*）
- **物理意义**: 相位噪声方差正比于联合线宽和符号周期。Δν_L = Δν_tx + Δν_LO（收发激光线宽之和）
- **参数**: 典型值 Δν_L = 10 kHz, T_s = 0.4 ns (2.5 Gsps) → σ_{θ,L}² ≈ 2.5×10⁻⁵ rad²
- **设计约束**: 块平均长度 M ≤ π/(4σ_{θ,L}) ≈ 157（否则相位漂移超出估计范围）

### 4.3 补充 — FFT频偏估计理论基础

#### F4.17 N点DFT定义

$$S[m] = \sum_{k=0}^{N-1} r[k] \cdot e^{-j 2\pi mk / N}, \quad m = 0, 1, \ldots, N-1$$

- **来源**: 标准DSP（Proakis & Manolakis）, Gasior & Gonzalez 2004 Eq.(2)
- **前文**: "对观测窗口内接收信号做N点DFT，将时域信号分解为N个正交频率分量"
- **物理意义**: 第m个频率bin对应频率 f_m = m·f_s/N。频偏估计通过四次方预处理后DFT峰值位置确定

#### F4.18 频率分辨率与观测窗口

$$\Delta f_{\text{grid}} = \frac{f_s}{N} = \frac{1}{N \cdot T_s}$$

- **来源**: Gasior & Gonzalez 2004 Eq.(3)
- **物理意义**: 相邻DFT bin频率间隔 = 观测时长倒数。N增大 → 分辨率提高但捕获时间增长
- **设计约束**: 要求 Δf_grid < 最小频偏精度需求 → 确定 N 下界

#### F4.19 频偏估计Cramér-Rao下界

$$\mathrm{var}(\hat{\Delta f}) \geq \frac{6}{(2\pi)^2 \cdot \mathrm{SNR} \cdot N(N^2 - 1) \cdot T_s^2}$$

当 $N \gg 1$ 时近似为：

$$\mathrm{var}(\hat{\Delta f}) \geq \frac{6}{(2\pi)^2 \cdot \mathrm{SNR} \cdot N^3 \cdot T_s^2}$$

- **来源**: Rife & Boorstyn 1974, IEEE Trans. Info. Theory
- **物理意义**: 任何无偏频偏估计器的方差下界。随样本数N³和SNR反比下降。ML估计器在高SNR下渐近达到此界
- **使用条件**: 复单频信号 + AWGN, SNR在门限以上（~10-15 dB）

#### F4.20 四次方消除QPSK调制的数学证明

QPSK发送符号 $s[k] \in \{(±1 ± j)/\sqrt{2}\}$，调制相位 $\theta_s[k] \in \{\pi/4, 3\pi/4, 5\pi/4, 7\pi/4\}$。

$$s^4[k] = |s|^4 \cdot e^{j \cdot 4\theta_s[k]} = e^{j \cdot \pi(2n+1)} = -1 \quad (n \in \mathbb{Z})$$

故四次方后调制相位消除，但引入常数 $\pi$ 相位偏移（$s^4 = -1$）：

$$r^4[k] \approx -e^{j(4 \cdot 2\pi \Delta f \cdot kT_s + 4\phi[k])} + \text{噪声项}$$

- **来源**: Proakis *Digital Communications* Ch.6, 丁爽 式(3-11), 董凡 式(2-26)
- **物理意义**: QPSK所有调制相位乘以4后均为 $\pi$ 的奇数倍（$4\theta_s \in \{\pi, 3\pi, 5\pi, 7\pi\}$），$s^4=-1$ 引入常数 $\pi$ 相位。后续 F4.28 块平均相位提取中通过 $-\pi$ 修正消除此偏移。剩余信号频率变为原始频偏的4倍
- **代价**: SNR退化因子 F4.5（SNR₄ ≈ SNR/8），频偏范围缩至1/4

#### F4.21 四次方后频偏估计范围

$$|\Delta f| < \frac{R_s}{2 \cdot 4} = \frac{R_s}{8}$$

- **来源**: Proakis Ch.6, M-PSK载波恢复通用结论（M=4 for QPSK）
- **物理意义**: 四次方使频率乘以4，可无模糊估计的频偏范围相应缩小4倍（类比Nyquist定理：4Δf < R_s/2 → Δf < R_s/8）
- **设计影响**: 需确保实际Doppler频偏不超过此范围，否则需先用粗频偏估计缩小残余

#### F4.22 抛物线插值精细化

设DFT幅度谱最大bin索引为 $m_{\max}$，相邻三个bin幅度 $S_{m-} = |S[m_{\max}-1]|$, $S_{m} = |S[m_{\max}]|$, $S_{m+} = |S[m_{\max}+1]|$，则亚bin频率修正量：

$$\delta = \frac{1}{2} \cdot \frac{S_{m-} - S_{m+}}{S_{m-} - 2S_{m} + S_{m+}}, \quad \delta \in [-1/2, +1/2]$$

$$\hat{\Delta f} = (m_{\max} + \delta) \cdot \frac{\Delta f_{\text{grid}}}{4}$$

（除以4恢复四次方引入的倍频）

- **来源**: Gasior & Gonzalez 2004 Eq.(10)
- **物理意义**: 用DFT峰值附近三个bin拟合抛物线，顶点给出亚bin精度频率估计。Hanning窗下插值增益G≈9.5（误差从Δf/2降至~5%Δf）
- **使用条件**: 需窗函数使主瓣宽度≥3 bin（Hanning窗满足）

#### F4.23 Hanning窗定义

$$w[k] = 0.5\left(1 - \cos\frac{2\pi k}{N-1}\right), \quad k = 0, 1, \ldots, N-1$$

- **来源**: Harris 1978, Proc. IEEE
- **关键指标**: 最高旁瓣 -31.5 dB（vs 矩形窗 -13.3 dB），主瓣宽度4 bins，ENBW = 1.5 bins
- **选择理由**: 四次方后SNR已退化~12 dB，需强旁瓣抑制防止频谱泄漏干扰峰值检测

### 4.4 补充 — 低复杂度Viterbi-Viterbi推导链

> 以下推导链给出VVPE的完整数学过程，使用绝对值近似替代复数乘法以降低计算复杂度。

#### F4.24 信号I/Q分解

$$r[k] = I_k + jQ_k, \quad I_k = |r[k]|\cos\phi_k, \quad Q_k = |r[k]|\sin\phi_k$$

其中 $\phi_k = \theta_s[k] + 2\pi\Delta f \cdot kT_s + \theta_L[k] + \theta_a[k]$ 为总瞬时相位。

- **来源**: 丁爽 式(3-2)

#### F4.25 绝对值近似（二倍角核心）

$$\cos^2\varphi \approx |\cos\varphi|, \quad \sin^2\varphi \approx |\sin\varphi|$$

$$\cos(2\varphi) = \cos^2\varphi - \sin^2\varphi \approx |I_k| - |Q_k|$$

$$\sin(2\varphi) \approx |I_k + Q_k| - |I_k - Q_k|$$

- **来源**: 丁爽 式(3-3)~(3-7), 张思齐 式(2-6)~(2-12)
- **物理意义**: 利用三角恒等式将复数乘法简化为绝对值+加减法，避免乘法器。这是低复杂度的数学基础
- **精度**: 高SNR下近似误差可忽略；低SNR时绝对值法不引入交叉噪声项（丁爽 式4-9/4-10分析）

#### F4.26 二倍角结果

$$I'_k = \sqrt{2}(|I_k| - |Q_k|), \quad Q'_k = |I_k + Q_k| - |I_k - Q_k|$$

$$r^{(2)}[k] = I'_k + jQ'_k = \sqrt{2} \cdot r[k]^2 / |r[k]|$$

- **来源**: 丁爽 式(3-7)/(3-8), 张思齐 式(2-11)~(2-14)
- **物理意义**: 二倍角操作后信号相位变为2φ_k，幅值乘√2平衡

#### F4.27 四倍角结果（等效四次方去调制）

在二倍角基础上再次应用绝对值近似：

$$I''_k = |I'_k| - |Q'_k|, \quad Q''_k = |I'_k + Q'_k| - |I'_k - Q'_k|$$

$$r^{(4)}[k] = I''_k + jQ''_k \propto e^{j \cdot (4(2\pi\Delta f \cdot kT_s + \theta_L[k] + \theta_a[k]) + \pi)} + \text{噪声}$$

QPSK调制相位已被消除（$4\theta_s[k] = 2\pi n$）。注意 $s^4=-1$ 引入额外的π相位因子。

- **来源**: 丁爽 式(3-9)~(3-11), 张思齐 式(2-15)~(2-17)
- **物理意义**: 两次迭代完成四次方操作，消除QPSK调制。结果仅含4倍频偏、4倍相位噪声、4倍大气扰动和常数π偏移
- **关键性质**: 绝对值法不产生信号-噪声交叉乘法项（丁爽 式4-9/4-10证明），优于传统复数四次方
- **π因子影响**: 该常数偏移在F4.28中产生π/4估计偏移，使QPSK星座旋转π/4（从{π/4,3π/4,5π/4,7π/4}旋转至{0,π/2,π,3π/2}），对判决无害

#### F4.28 块平均相位提取

$$\hat{\phi}_\text{raw} = \frac{1}{4}\left[\arg\left(\frac{1}{M}\sum_{k=0}^{M-1} r^{(4)}[k]\right) - \pi\right]$$

- **来源**: 丁爽 式(3-12)/(3-13), 张思齐 式(2-18), Viterbi & Viterbi 1983
- **物理意义**: M个符号的四次方信号取平均（抑制零均值AWGN），取角度减去s⁴=-1引入的π偏移后除以4。减π消除F4.27中的常数相位偏移
- **参数**: M为平均窗口长度，与F4.9自适应窗口公式对应
- **设计约束**: M受相位噪声方差约束——M太大使相位漂移超出(-π/4, π/4]范围

#### F4.29 相位补偿

$$\hat{r}[k] = r[k] \cdot e^{-j\hat{\phi}_\text{raw}}$$

- **来源**: 丁爽 式(3-14), 张思齐 式(3-29)

### 4.4 补充 — BPS（Blind Phase Search）算法

#### F4.30 BPS测试相位构造

$$\phi_b = \frac{\pi b}{2B}, \quad b = -B/2, \ldots, 0, \ldots, B/2-1$$

B个均匀分布测试相位覆盖范围 $(-\pi/2, \pi/2]$。

- **来源**: 董凡 式(2-30), 丁爽 式(4-1), Pfau 2009
- **参数**: B = 32（董凡推荐值），QPSK时对称区间为π/2（M=4→2π/M = π/2）

#### F4.31 欧氏距离度量

$$|d_{k,b}|^2 = |r[k] \cdot e^{-j\phi_b} - \hat{s}_{k,b}|^2$$

其中 $\hat{s}_{k,b}$ 为补偿后符号对应的最近理想星座点。

- **来源**: 董凡 式(2-32), 丁爽 式(4-2)
- **物理意义**: 对每个测试相位φ_b，计算补偿后符号与最近星座点的欧氏距离。最小距离对应的φ_b为最优相位估计

#### F4.32 块内距离累加（窗口平滑）

$$S_{k,b} = \sum_{i=k-N_w}^{k+N_w} |d_{i,b}|^2$$

- **来源**: 董凡 式(2-33), 丁爽 式(4-3)
- **物理意义**: 2N_w+1个符号窗口内累加距离度量，平滑AWGN干扰。窗口长度N_w与BPS性能直接相关
- **参数**: N_w = 32（董凡实测最优值，平衡跟踪速度与估计精度）

#### F4.33 ML精估计（BPS第二级）

$$\hat{\varphi}_\text{ML} = \arg\left(\sum_{k} r[k] \cdot \hat{s}_k^*\right)$$

- **来源**: 董凡 式(2-35)
- **物理意义**: 用BPS粗估计的判决符号$\hat{s}_k$与原始接收信号做相关（决策导向），提取精估计相位。计算量仅相当于BPS中2个测试角度的计算量
- **优势**: 双级结构（BPS粗估计+ML精估计）显著降低总复杂度，同时保持高精度

### 4.4 补充 — 相位模糊消除

#### F4.34 相位跳变检测（π/2模糊消除）

四次方操作引入π/2整数倍相位模糊。消除方法——基于相邻块相位差的跳变检测：

$$\Phi[k] = \begin{cases} \Phi[k-1] + \pi/2, & \text{if } (\hat\phi_\text{raw}[k] - \hat\phi_\text{raw}[k-1]) < -\pi/4 \\ \Phi[k-1] - \pi/2, & \text{if } (\hat\phi_\text{raw}[k] - \hat\phi_\text{raw}[k-1]) > \pi/4 \\ \Phi[k-1], & \text{otherwise} \end{cases}$$

- **来源**: 张思齐 式(3-27), 丁爽 §3.2（FSM模块）, 董凡 式(2-29)/(2-30)
- **物理意义**: 四次方操作使真实相位估计范围缩至(-π/4, π/4]。当真实相位变化超过此范围时产生跳变，通过检测相邻块相位差补偿π/2整数倍偏移
- **初始值**: Φ[1] = 0

#### F4.35 修正后相位估计

$$\hat{\phi}_\text{final}[k] = \hat{\phi}_\text{raw}[k] + \Phi[k]$$

- **来源**: 张思齐 式(3-28)
- **物理意义**: 原始相位估计 + 累计跳变补偿 = 最终无模糊相位估计

### 4.4 补充 — 二阶DPLL稳定性分析

> 以下公式为二阶Type-2 DPLL的标准理论结果，用于§4.4 DPLL部分的深度展开。

#### F4.36 连续时间闭环传递函数

$$H(s) = \frac{\theta_\text{out}}{\theta_\text{in}} = \frac{2\zeta\omega_n s + \omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

- **来源**: Gardner *Phaselock Techniques* 3rd Ed. §2.2.3, Rice Appendix C.1.3
- **物理意义**: 描述DPLL输出相位跟踪输入相位的能力。分子含一个零点（导致阶跃响应过冲）
- **参数**: ζ（阻尼比）, ω_n（自然频率）。ζ=1/√2为工程标准设计点

#### F4.37 误差传递函数

$$H_e(s) = 1 - H(s) = \frac{s^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

- **来源**: Gardner §2.2.3
- **物理意义**: 分子s²的阶数=2 = PLL类型数。Type-2系统可零稳态误差跟踪相位阶跃和频率阶跃

#### F4.38 环路滤波器系数（PI结构）

比例-积分环路滤波器 $F(z) = \alpha_\text{DPLL} + \beta_\text{DPLL}/(1-z^{-1})$ 的系数：

$$\alpha_\text{DPLL} = \frac{2\zeta\omega_n T_s}{K_p K_\text{nco}}, \quad \beta_\text{DPLL} = \frac{(\omega_n T_s)^2}{K_p K_\text{nco}}$$

- **来源**: Robertson DSPRelated 2016 Eq.(3-4), Rice Appendix C
- **物理意义**: α_DPLL控制跟踪速度（比例增益），β_DPLL消除频率阶跃稳态误差（积分增益）
- **注意**: 下标DPLL避免与GG参数α,β混淆（见symbol-conventions.md §13消歧策略）
- **参数**: K_p为鉴相增益，K_nco为NCO增益，T_s为采样/符号周期

#### F4.39 离散闭环传递函数

$$H_\text{CL}(z) = \frac{G_1(z)}{1+G_1(z)}$$

其中 $G_1(z) = \frac{K_p \alpha_\text{DPLL} K_\text{nco}}{z-1} + \frac{K_p \beta_\text{DPLL} K_\text{nco}}{(z-1)^2}$

- **来源**: Robertson DSPRelated 2016 Eq.(5)
- **使用条件**: ω_n/f_s << 1/(2π)（环路自然频率远小于采样频率）

#### F4.40 噪声带宽与自然频率关系

$$B_L = \frac{\omega_n}{2}\left(\zeta + \frac{1}{4\zeta}\right)$$

ζ = 1/√2 时：

$$B_L \approx 0.53\,\omega_n$$

- **来源**: Gardner *Phaselock Techniques* §2.3（经典公式）
- **物理意义**: B_L是DPLL的等效噪声带宽，决定对输入相位噪声的抑制能力。B_L↓→噪声抑制好但跟踪慢；B_L↑→跟踪快但噪声大
- **单位说明**: 当ω_n以rad/s为单位时，B_L以rad/s为单位；换算为Hz需除以2π。本文后续统一使用Hz单位，即 $f_n = \omega_n/(2\pi)$，$B_L[\text{Hz}] \approx 0.53 f_n = 0.53 \omega_n/(2\pi)$。F4.10中ω_n = B_L/0.53隐含了此约定
- **与自适应公式关系**: F4.10中 $B_{L,opt} = B_0 \cdot h$，代入此式可得 $\omega_n = B_L / 0.53$

#### F4.41 稳态相位误差（频率斜升输入）

$$\theta_e(\infty) = \frac{2\pi \dot{f}_d}{\omega_n^2} \quad \text{(rad)}$$

- **来源**: Georgia Tech ECE 6440 Lecture 090
- **物理意义**: 对频率斜升（Doppler变化率ḟ_d），Type-2二阶环存在有限稳态误差。误差反比于ω_n²
- **设计约束**: 要求 $\theta_e(\infty) < \pi/4$（QPSK判决裕量）→ 确定ω_n下界
- **注**: 对频率阶跃，稳态误差为0（Type-2系统的优势）

#### F4.42 收敛时间常数

$$\tau = \frac{1}{\zeta\omega_n} \quad \text{(s)}, \quad T_L = \frac{2\pi}{\omega_n} \quad \text{(s, 锁定时间)}$$

- **来源**: Gardner §2.2, Georgia Tech ECE 6440
- **物理意义**: 瞬态响应约4τ~5τ后衰减到稳态值2%以内。锁定时间约为一个自然频率周期

#### F4.43 离散稳定性条件

极点位于：$z_{1,2} = e^{-\zeta\omega_n T_s}\left[\cos(\omega_d T_s) \pm j\sin(\omega_d T_s)\right]$，其中 $\omega_d = \omega_n\sqrt{1-\zeta^2}$。

稳定性要求极点模值 $r = e^{-\zeta\omega_n T_s} < 1$（ζ > 0时自动满足），但工程安全裕量要求：

$$\omega_n T_s < 0.1 \sim 0.5 \quad \Longleftrightarrow \quad f_n / f_s < 0.016 \sim 0.08$$

- **来源**: Robertson Appendix C, TI SLYT169
- **物理意义**: 保证s→(z-1)/T_s近似有效，离散化不引入额外不稳定性

### 4.4 补充 — 载波恢复级联流程

#### F4.44 频偏补偿后信号

$$r'[k] = r[k] \cdot \exp\!\left(-j \cdot 2\pi \hat{\Delta f} \cdot kT_s\right)$$

- **来源**: 张思齐 式(2-21)/(3-23), 丁爽 §3.1
- **物理意义**: FOE阶段输出频偏估计后，对接收信号做共轭乘法补偿频偏

#### F4.45 四次方信号频偏补偿（数据复用）

$$r^{(4)'}[k] = r^{(4)}[k] \cdot \exp\!\left(-j \cdot 4 \cdot 2\pi \hat{\Delta f} \cdot kT_s\right)$$

- **来源**: 张思齐 式(3-24)（核心创新点）
- **物理意义**: 频偏阶段产生的四次方信号不丢弃，补偿4倍频偏后直接送入CPR阶段复用。避免CPR阶段重复四次方运算，节省约50%计算量

#### F4.46 完整级联链信号流

$$\underbrace{r[k]}_{\text{接收}} \xrightarrow{\times 4} \underbrace{r^{(4)}[k]}_{\text{四次方}} \xrightarrow{\text{FFT峰值}} \hat{\Delta f} \xrightarrow{\text{补偿}} r'[k],\; r^{(4)'}[k]$$

$$\xrightarrow{\text{块平均}} \hat{\phi}_\text{raw} \xrightarrow{+\Phi[k]} \hat{\phi}_\text{final} \xrightarrow{\text{补偿}} \hat{r}[k] \xrightarrow{\text{判决}} \hat{s}[k]$$

- **来源**: 综合张思齐 §3.2 + 我们的sim_direction_a.py实现
- **物理意义**: 完整的FOE→CPR级联链，核心优化是四次方数据在两个阶段间复用

---

## 补充公式编号索引

| 编号 | 内容 | 来源 | 对应章节 |
|------|------|------|---------|
| F4.15 | 激光器相位噪声Wiener过程 | 丁爽 | §4.2 |
| F4.16 | 相位噪声方差 σ²=2πΔνT_s | 丁爽/标准 | §4.2 |
| F4.17 | N点DFT定义 | 标准DSP | §4.3 |
| F4.18 | 频率分辨率 | Gasior 2004 | §4.3 |
| F4.19 | 频偏估计CRB | Rife & Boorstyn 1974 | §4.3 |
| F4.20 | 四次方消除QPSK调制 | Proakis/丁爽/董凡 | §4.3 |
| F4.21 | 四次方后频偏范围 | Proakis | §4.3 |
| F4.22 | 抛物线插值精细化 | Gasior 2004 | §4.3 |
| F4.23 | Hanning窗定义 | Harris 1978 | §4.3 |
| F4.24 | 信号I/Q分解 | 丁爽 | §4.4 |
| F4.25 | 绝对值近似（二倍角） | 丁爽/张思齐 | §4.4 |
| F4.26 | 二倍角结果 | 丁爽/张思齐 | §4.4 |
| F4.27 | 四倍角（等效四次方） | 丁爽/张思齐 | §4.4 |
| F4.28 | 块平均相位提取 | Viterbi 1983/丁爽 | §4.4 |
| F4.29 | 相位补偿 | 丁爽/张思齐 | §4.4 |
| F4.30 | BPS测试相位构造 | 董凡/Pfau 2009 | §4.4 |
| F4.31 | 欧氏距离度量 | 董凡/丁爽 | §4.4 |
| F4.32 | 块内距离累加 | 董凡/丁爽 | §4.4 |
| F4.33 | ML精估计 | 董凡 | §4.4 |
| F4.34 | 相位跳变检测（π/2模糊） | 张思齐/丁爽 | §4.4 |
| F4.35 | 修正后相位估计 | 张思齐 | §4.4 |
| F4.36 | DPLL闭环传递函数 | Gardner/Rice | §4.4 |
| F4.37 | DPLL误差传递函数 | Gardner | §4.4 |
| F4.38 | DPLL环路滤波器系数 | Robertson/Rice | §4.4 |
| F4.39 | DPLL离散闭环传递函数 | Robertson | §4.4 |
| F4.40 | DPLL噪声带宽 B_L=0.53ωn | Gardner | §4.4 |
| F4.41 | DPLL稳态误差（频率斜升） | Georgia Tech | §4.4 |
| F4.42 | DPLL收敛时间常数 | Gardner | §4.4 |
| F4.43 | DPLL离散稳定性条件 | Robertson/TI | §4.4 |
| F4.44 | 频偏补偿后信号 | 张思齐 | §4.4 |
| F4.45 | 四次方信号频偏补偿（复用） | 张思齐 | §4.4 |
| F4.46 | 完整级联链信号流 | 综合 | §4.4 |

**Ch4公式总量**: F4.1-F4.14（原有）+ F4.15-F4.46（补充）= **46条**
