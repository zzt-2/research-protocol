# 会议论文写法模式库（8 篇 IEEE 会议论文提取）

> 统一化版本 | 2026-07-10
> 来源论文：8 篇英文 IEEE/OFC/OECC 会议论文全文精读
> 每条格式：`> 英文原文摘录（忠实复制）` → `**骨架**：[可替换成分]` → `**用法**：场景说明`
> 摘录标来源论文简称，骨架与用法用中文。
> 段落级骨架查 `writing-patterns-paragraph.md`，句级骨架（学位论文体例）查 `writing-patterns-sentence.md`。
> **本库是「会议论文体例」版的句式库，写英文会议正文时优先查本库；写中文长篇学位论文章节时查 `writing-patterns-sentence.md`。**

## 来源论文清单

| 简称 | 全称 | venue | 本地路径 | 方向相关度 |
|---|---|---|---|---|
| ICSOS 2025 | Z-transform ODPLL modeling for LEO Doppler | ICSOS 2025 | `papers/doi/10.1109_ICSOS66026.2025.11443174/` | 强（FSO 星地） |
| ICSOS 2019 | Coherent RX: AO + DPLL | ICSOS 2019 | `papers/doi/10.1109_icsos45490.2019.8978983/` | 强（FSO 湍流） |
| MWP 2022 | All-digital OPLL for FSO | MWP 2022 | `papers/doi/10.1109_mwp54208.2022.9997784/` | 强（FSO 湍流） |
| OFC 2026 | Gardner TED reuse for FOE | OFC 2026 | `papers/doi/10.1364_ofc.2026.w2a.62/` | 强（FOE 相邻） |
| OECC 2025 | MAP estimator for 256-QAM CPE | OECC/PSC 2025 | `papers/doi/10.23919_oecc-psc62146.2025.11109607/` | 强（CPE 相邻） |
| APCCAS 2022 | BPS-based CPR FPGA implementation | APCCAS 2022 | `papers/doi/10090345.md` | 中（CPR 实现） |
| OECC 2024 | Pilot-tone assisted Costas PLL | OECC 2024 | `papers/doi/10975630.md` | 中（载波恢复） |
| ICUMT 2015 | Nonlinear OPLL analysis for OISL | ICUMT 2015 | `papers/doi/7382400.md` | 中（理论型 OPLL） |

---

## §1 公式引入句式（formula introduction）

### 1.1 "can be approximately derived as"
> the Doppler frequency shift ∆f can be approximately derived as (ICSOS 2025)
**骨架**：[物理量] can be approximately derived as: [公式]
**用法**：引入由近似推导得到的核心物理量公式（多普勒频移），"approximately" 标注精度级别，适合 Intro/背景段的定量铺垫。

### 1.2 "is modeled as:"
> In the presence of carrier phase noise, the discrete-time complex baseband received signal r(k) is modeled as: (OECC 2025)
**骨架**：In the presence of [损伤/条件], the [信号描述] [物理量] is modeled as: [公式]
**用法**：在原理段开头给出接收信号模型的标准起句，先声明损伤背景再引公式。

### 1.3 "We can further express ... as:"
> We can further express the received signal in polar coordinates as: (OECC 2025)
**骨架**：We can further express the [物理量] in [域/坐标] as: [公式]
**用法**：推导链第二步——把已有信号模型转换到另一个域（极坐标），"further" 承接前式。

### 1.4 "is given by"
> the LF transfer function is given by F(z) = K1 + K2/(z−1), where K1, and K2 are the loop filter gains. (MWP 2022)
**骨架**：[物理量] is given by [公式], where [参数A] and [参数B] are [含义].
**用法**：给出某模块（环路滤波器）传递函数，"is given by" 紧跟公式，参数解释在同一句内完成，紧凑。

### 1.5 "is obtained by calculating"
> the TED gain is obtained by calculating the maximum value of the S-curve. (OFC 2026)
**骨架**：[物理量] is obtained by calculating [运算/提取方式].
**用法**：说明某估计量通过何种运算获得，不直接给公式而给"怎么算"，适合 Principle 段。

### 1.6 "the estimated phase error is the following:"
> Then, the estimated phase error is the following: (MWP 2022)
**骨架**：Then, the estimated [物理量] is the following: [公式]
**用法**：算法步骤中引出某一步的输出量公式，"Then" 标记步骤序号，冒号引出公式。

### 1.7 "the phase offset can be estimated using ...:"
> For each block, the phase offset can be estimated using the pilot symbol: (OECC 2025)
**骨架**：For each [处理单元], the [物理量] can be estimated using the [手段]: [公式]
**用法**：说明某估计量借助什么手段（导频符号）估计，"can be estimated using" 同时点明方法和引出公式。

### 1.8 "derives from MAP estimation ... implemented in the form of"
> the signal goes through the following phase detector function which derives from Maximum A Posteriori estimation of an unknown carrier phase offset affecting a BPSK modulated signal, implemented in the form of a closed-loop iterative synchronizer [12]: (ICSOS 2019)
**骨架**：the [模块] function which derives from [估计准则] estimation of [估计目标] affecting a [信号类型] signal, implemented in the form of [实现架构] [引用]: [公式]
**用法**：引入某模块公式时完整交代其理论来源（MAP 估计）、估计对象、信号类型、实现形式与引用，一句到底。

### 1.9 "can be described as"
> The input signal of CPR can be described as 𝑥𝑘 (APCCAS 2022)
**骨架**：[物理量/信号] can be described as [符号]
**用法**：引入核心信号模型时的中性起句，"can be described as" 语气平实，主语直接是待定义的信号。

### 1.10 "can be expressed as"（并列两式）
> the pilot tone modulated at the I-channel can be expressed as (e^iωt − e^−iωt), and the phase offset introduced can be expressed as e^θi (OECC 2024)
**骨架**：[已调制/已处理的信号] can be expressed as [表达式], and [相关物理量] can be expressed as [表达式]
**用法**：连续引入两个相关信号的数学表达，用"and"并列，第二个保持相同句式以求节奏一致。

### 1.11 "are described as follows"
> The local oscillator is controlled by an error signal 𝑥(𝑡) or 𝜀(𝑡) and therefore realized as a voltage controlled oscillator (VCO). The two signals are described as follows: (ICUMT 2015)
**骨架**：[信号A] is controlled by [信号B] and therefore realized as [器件]. The [N] signals are described as follows: [公式组]
**用法**：先一句话交代器件实现和控制关系，再用"are described as follows"冒号引出一组公式，适合多信号同时定义。

### 1.12 "is given as"
> After converting into the electrical domain by the photodiodes and amplification the I- and Q-signal is given as (ICUMT 2015)
**骨架**：After [前置物理操作], the [信号] is given as [公式]
**用法**：描述信号经过一连串物理处理（光电转换、放大）后的输出形式，"is given as" 紧接前文操作链。

### 1.13 "can be expressed as a Gaussian noise process with variance"
> The phase noise between two subsequent phase values with time difference τ can be expressed as a Gaussian noise process with variance (ICUMT 2015)
**骨架**：The [噪声/随机量] between [采样描述] can be expressed as a [分布名] with variance [公式]
**用法**：不直接给公式而先声明统计模型，"can be expressed as a ... process" 将物理噪声映射到概率过程。

### 1.14 "It can be modelled as ... with variance"
> It can be modelled as zero-mean Gaussian random process with variance (ICUMT 2015)
**骨架**：It can be modelled as [均值描述] [分布名] with variance [公式]
**用法**：对噪声的统计建模声明，"modelled as" 强调这是模型假设而非精确等式。

### 1.15 "the resulting control signal can be described as"
> and the resulting control signal can be described as (ICUMT 2015)
**骨架**：and the resulting [推导产物] can be described as [公式]
**用法**：推导链中引出"前几步运算的结果量"，"resulting" 标记该量是前面运算的产物。

---

## §2 参数解释句式（symbol/parameter explanation）

### 2.1 "where [符号] denotes ..."
> where α(k) denotes the transmitted 256-QAM symbol at time index k. θ is an unknown deterministic initial carrier phase offset, while θ(k) represents the time-varying Wiener phase noise [6]. (OECC 2025)
**骨架**：where [变量A] denotes [含义A]. [变量B] is [含义B], while [变量C] represents [含义C] [引用].
**用法**：公式后逐符号解释的标准格式，"denotes / is / represents" 交替使用避免重复，附引用支撑模型。

### 2.2 "is a sequence of ... Gaussian random variables with zero mean and variance"
> θ(k) is the Wiener phase noise process with θ(k)−θ(k−1)=πη(k), θ(0)=0, where η(k) is a sequence of independent and identically distributed (i.i.d.) Gaussian random variables with zero mean and variance σΔν²Ts. (OECC 2025)
**骨架**：[变量] is the [过程名] process with [递推式], where [子变量] is a sequence of i.i.d. Gaussian random variables with zero mean and variance [表达式].
**用法**：对随机过程（维纳相噪）给出递推定义和增量分布，含均值与方差表达式，紧凑而完整。

### 2.3 "Here, [符号] represents the AOPN arising from ..."
> Here, ϵ(k) denotes the AOPN arising from AWGN. (OECC 2025)
**骨架**：Here, [变量] denotes the [噪声名] arising from [来源].
**用法**："Here" 替代 "where" 引出参数解释，"arising from" 说明噪声的物理来源。

### 2.4 "where v is ... and λ = ... is ..." + 近似有效性
> where v is the relative satellite-OGS speed and λ = 1550 nm is the original laser wavelength. The approximation is valid considering that v << c, with c ≈ 3 × 10⁸ m/s the celerity of light. (ICSOS 2025)
**骨架**：where [变量A] is [含义A] and [变量B] = [值] is [含义B]. The approximation is valid considering that [近似条件], with [变量C] ≈ [值] [含义C].
**用法**：参数解释后紧跟近似有效性声明（"is valid considering that"），把变量定义和近似条件合并说明。

### 2.5 "where R is ... in A/W, Ps the received optical power in W and q the elementary charge in C."（带单位密集列举）
> where R is the photoreceiver responsivity in A/W, Ps the received optical power in W and q the elementary charge in C. (ICSOS 2025)
**骨架**：where [变量A] is [含义A] in [单位A], [变量B] the [含义B] in [单位B] and [变量C] the [含义C] in [单位C].
**用法**：带物理单位的密集参数列举，省略重复的 "is"，每项后标 SI 单位，工程化表达。

### 2.6 "represents the modulation order. For QPSK M = 2ᵇ = 4"
> M represents the modulation order. For QPSK M = 2ᵇ = 4, where b is the number of bits/symbol. (MWP 2022)
**骨架**：[变量] represents [含义]. For [调制格式] [变量] = [表达式], where [子变量] is [含义].
**用法**：先解释通用变量，再限定具体调制格式下的取值，"For QPSK" 框定适用范围。

### 2.7 "where we assume unit gain K0=1"
> where we assume unit gain K0=1. (ICSOS 2019)
**骨架**：where we assume [参数]=[值].
**用法**：在给出公式的同时声明归一化/单位增益假设，"where we assume" 一句带过简化条件。

### 2.8 "where ... represent ... respectively"（双符号并列）
> where ω and θ represent the angular frequency of pilot tone and optical phase offset respectively. (OECC 2024)
**骨架**：where [符号A] and [符号B] represent the [含义A] and [含义B] respectively.
**用法**：双符号并列解释的标准格式，"respectively" 保证一一对应，简短紧凑。

### 2.9 "where ... denote ..., ... [省略动词] the ..."（6+ 符号密集列举）
> where 𝑠̂₁,₂ denote the signal amplitudes, 𝜔₀ the carrier frequency, Δ𝜔(𝑡) the time varying frequency offset due to the Doppler shift, 𝐾₀ the frequency gain of the VCO in Hz/V, 𝜙𝑀(𝑡) the phase modulation, 𝜙₁,₀ and 𝜙₂,₀ a constant phase offset. (ICUMT 2015)
**骨架**：where [符号1] denote(s) the [含义1], [符号2] the [含义2], [符号3] the [含义3] due to [来源], [符号4] the [含义4] in [单位], ...
**用法**：密集参数解释格式——首项给动词"denote"，其后所有项省略动词，仅"符号 + the + 含义"并列，适合公式后一次解释 6+ 个符号。

### 2.10 "where [符号] = [展开式] denotes the [含义全称]"
> where 𝐾𝐷 = (𝐺𝑅𝑠̂₁𝑠̂₂)/2 denotes the phase discriminator gain. (ICUMT 2015)
**骨架**：where [符号] = [展开式] denotes the [含义全称].
**用法**：同时给出符号的定义式和物理含义，"denotes" 为最正式的解释动词。

### 2.11 "Here we determine the value of ... to be ..."
> where 𝑏 is between ... , B determines the number of test phases. Here we determine the value of test phases to be 16, and then improve the estimation effect by ... (APCCAS 2022)
**骨架**：where [变量] determines the [参数]. Here we determine the value of [参数] to be [数值], and then ...
**用法**：先解释某变量的作用（决定数量），再用"Here we determine ... to be"给出本文采用的具体取值，"Here" 标志从抽象定义转向具体配置。

---

## §3 数值嵌入句式（embedding numbers in prose）

### 3.1 "achieves a ... range 1.9 times that of ..."
> the proposed algorithm achieves a Doppler-shift estimation range 1.9 times that of conventional algorithms. (OFC 2026)
**骨架**：the proposed [方法] achieves a [指标] [倍数] times that of [对比方法].
**用法**：用倍数关系嵌入核心性能数字，"X times that of" 是相对增益的标准表达。

### 3.2 "enhances receiver sensitivity by 0.6 dB"
> Providing noise-robust estimation enhances receiver sensitivity by 0.6 dB and enables successful demodulation even under a low optical signal-to-noise ratio of 10 dB. (OFC 2026)
**骨架**：[特性] enhances receiver sensitivity by [数值] dB and enables [能力] even under [极端条件] of [数值] dB.
**用法**：一句话嵌入两个数字（灵敏度增益 + 极端 OSNR），"enhances ... by X dB" 后接"enables ... even under" 强化亮点。

### 3.3 "... are about 4 dB, 5 dB and 7.5 dB, respectively"（三方法对比列举）
> when the baud rate is 100 GBaud and the laser linewidth is 150 kHz, the SNR penalties of the MAP, PA ML and PA estimators are about 4 dB, 5 dB and 7.5 dB, respectively. (OECC 2025)
**骨架**：when [条件], the [指标] of [方法A], [方法B] and [方法C] are about [值A], [值B] and [值C], respectively.
**用法**：三方法对比的列举式数值嵌入，"respectively" 对应排列，前面用 "when" 限定条件。

### 3.4 "reaches 7% HD-FEC limit at SNR = 32 dB"
> The BER of the MAP estimator reaches 7% HD-FEC limit at SNR = 32 dB and 33 dB when baud rate is 100 GBaud and 64 GBaud, respectively. (OECC 2025)
**骨架**：The [指标] of [方法] reaches [门限] at [参数] = [值A] and [值B] when [条件A] and [条件B], respectively.
**用法**：BER 达到 FEC 门限的达标点嵌入，双条件用 "respectively" 对应。

### 3.5 "up to 7.2 km/s ... ±4.6 GHz ... 85 MHz/s"（背景段连续嵌极值）
> Numerical applications yield up to 7.2 km/s in relative speed, and 131 m/s² in maximum acceleration ... The Doppler frequency shift over the pass is ±4.6 GHz, and the maximum Doppler rate reaches 85 MHz/s. (ICSOS 2025)
**骨架**：Numerical applications yield up to [值A] in [量A], and [值B] in [量B]. The [量C] over the pass is [值C], and the maximum [量D] reaches [值D].
**用法**：背景段连续嵌入多个物理量极值，"yield up to / reaches" 引导数值，适合给出系统设计指标。

### 3.6 "the obtained minimum theoretical value is 23 nW or -46.4 dBm"
> For a 10 GBaud (= 20 Gbps) QPSK link, the obtained minimum theoretical value is 23 nW or -46.4 dBm. (ICSOS 2025)
**骨架**：For a [系统配置] link, the obtained minimum theoretical value is [值A] or [值B dBm].
**用法**：理论极限值嵌入，同时给 W 和 dBm 两种单位，"For a ... link" 限定配置。

### 3.7 "a pull-in time shorter than 1s"
> The results demonstrate the possibility to design DPLL with a pull-in time shorter than 1s, thereby offering good additional margin against noise. (ICSOS 2019)
**骨架**：The results demonstrate the possibility to design [方法] with a [指标] shorter than [值], thereby offering [附加优势].
**用法**：Conclusion 段把关键性能数字嵌入"证明可行"句式，"thereby offering" 顺势给出附加收益。

### 3.8 "the quantum limit in QPSK is 18 photons/bit" + That is ...
> we compute that the quantum limit in QPSK is 18 photons/bit [16]. That is the minimum amount of light a perfect photoreceiver, with η = 1, would need to achieve a 10⁻⁹ BER. (ICSOS 2025)
**骨架**：we compute that the [极限名] in [调制格式] is [值] [单位]. That is the minimum [物理量] a [理想条件] would need to achieve a [门限].
**用法**：给出量子极限后立即用"That is"做口语化重述，把抽象数字转化为直观物理含义。

### 3.9 "the clock frequency can reach 620MHz, and the latency ... is 18 clock cycles"（一句双数字+测试条件）
> the clock frequency can reach 620MHz, and the latency of processing 79.3Gbps 16QAM signal is 18 clock cycles. (APCCAS 2022)
**骨架**：the [性能指标A] can reach [数值A], and the [性能指标B] of processing [速率/条件] [调制] signal is [数值B].
**用法**：一句话嵌入两个关键性能数字（频率+延迟），并附上测试条件（速率、调制格式），适合摘要和贡献段。

### 3.10 "can save about 80% of logic resources ... and reach higher ..."（双收益）
> Compared to ordinary MAC, using CC-MAC can save about 80% of logic resources on the multiplier in the PR module and reach higher clock frequency. (APCCAS 2022)
**骨架**：Compared to [基线], using [本方法] can save about [百分比]% of [资源] on the [模块] and reach higher [性能].
**用法**：一句同时给出资源节省百分比和性能提升，"and" 并列两个收益，适合模块优化效果总结。

### 3.11 "can be recovered below 7% FEC threshold at the receiver power of -28 dBm"
> It can be seen that all the tributaries can be recovered below 7% FEC threshold at the receiver power of -28 dBm. (OECC 2024)
**骨架**：It can be seen that all the [信号] can be recovered below [百分比] FEC threshold at the [参数] of [数值].
**用法**：以 FEC 门限为参照嵌入功率数值，"below ... threshold" 是光通信性能表述的固定搭配。

### 3.12 "is more than 23 dB down in the Q-path compared to ..."
> the power of the pilot tone signal is more than 23 dB down in the Q-path compared to the power in the I-path. (OECC 2024)
**骨架**：the [指标] of [信号] is more than [数值] dB down in the [通道A] compared to the [指标] in the [通道B].
**用法**：用"X dB down in A compared to B"表达通道间相对功率差，适合锁相/隔离度类指标的量化。

---

## §4 方法对比句式（method comparison）

### 4.1 "Compared to the [基线], the [对比方法] exhibits a higher ..."
> Compared to the atan2, the sine discriminator exhibits a higher oscillatory characteristic and a higher standard deviation (STD) of the controlled frequency. (MWP 2022)
**骨架**：Compared to the [所提方法], the [对比方法] exhibits a higher [劣性指标A] and a higher [劣性指标B].
**用法**：以所提方法为基准反向衬托对比方法的缺陷，"Compared to ... exhibits a higher" 是定量对比的标准句式。

### 4.2 "... always loses lock during ... while the proposed ... keeps the system locked"
> The sinusoidal discriminator always loses lock during fading regime while the proposed discriminator keeps the system locked. The only condition where the sinusoidal discriminator maintained locking was when the system delay was equal to zero, i.e., an unrealistic condition. (MWP 2022)
**骨架**：The [对比方法] always [失败行为] during [条件] while the proposed [方法] keeps the system [状态]. The only condition where [对比方法] [成功] was when [条件], i.e., an unrealistic condition.
**用法**：用 "while" 强对比 + "The only condition ... i.e., an unrealistic condition" 极端反衬，凸显所提方法的鲁棒性。

### 4.3 "nearly 1.9 times that of ..., which fails beyond 12 GHz. This advantage arises from ..."
> the proposed FOE accurately estimates Doppler shifts within 0 GHz–23 GHz, nearly 1.9 times that of the PSA FOE, which fails beyond 12 GHz. This advantage arises from exploiting ... (OFC 2026)
**骨架**：the proposed [方法] accurately [功能] within [范围], nearly [倍数] times that of the [对比方法], which fails beyond [阈值]. This advantage arises from [机制].
**用法**：对比句后紧跟"This advantage arises from"解释优势来源，对比+归因一步到位。

### 4.4 "It can be seen from Fig. X that ... performs the best. ... Obviously, ..."
> It can be seen from Fig. 2(b) that the MAP estimator performs the best. ... Obviously, the MAP estimator has better linewidth tolerance and stronger phase noise resistance. (OECC 2025)
**骨架**：It can be seen from Fig. X that the [方法] performs the best. ... Obviously, the [方法] has better [指标A] and stronger [指标B].
**用法**：引图后直接下结论 + "Obviously" 强化定性对比判断，适合 Results 段收束。

### 4.5 "compares the theoretical ... with/without ... computed from (11) and (12), respectively, to the corresponding experimental points"
> the figure compares the theoretical phase error variance with/without BPSK modulation computed from (11) and (12), respectively, to the corresponding experimental points obtained by simulation. (ICSOS 2019)
**骨架**：the figure compares the theoretical [量] with/without [条件] computed from (式X) and (式Y), respectively, to the corresponding experimental points.
**用法**：理论 vs 仿真对比的图引用句，"with/without ... respectively" 并列两组理论曲线与实验点对照。

### 4.6 "Compared to [基线], using [本方法] can save ... and reach higher ..."（双收益对比）
> Compared to ordinary MAC, using CC-MAC can save about 80% of logic resources on the multiplier in the PR module and reach higher clock frequency. (APCCAS 2022)
**骨架**：Compared to [基线方法], using [本方法] can [量化优势1] and [量化优势2].
**用法**：最直接的对比句式，"Compared to" 前置对比对象，主句给出本方法的双重收益。

### 4.7 "Unlike the [基线方案], which [局限], [本方法] also use ... thereby increasing ..."
> Unlike the current four-level pulse amplitude modulation (PAM4) scheme used in datacenter interconnects, which utilizes only amplitude modulation dimension, coherent optical communication systems also use phase and polarization modulation dimensions, thereby increasing the system capacity. (OECC 2024)
**骨架**：Unlike the [基线方案], which [局限描述], [本方法/系统] also use [维度列举], thereby increasing the [指标].
**用法**：用"Unlike ... which"先框定基线的局限，再用"also use ... thereby"展开本方法的多维度优势。

### 4.8 "Compared to our previous work using [旧方法] that ..., this paper proposed ... more accurately"
> Compared to our previous work using power monitor module (PMM) that monitors the minimum of Q-path pilot tone power to dynamically shift the frequency of the AOM ..., this paper proposed pilot tone assisted Costas phase-locked loop acquires the phase error more accurately and thus improve the performance ... (OECC 2024)
**骨架**：Compared to our previous work using [旧方法] that [旧机制描述], this paper proposed [新方法] [优势描述] more accurately and thus improve the [性能].
**用法**：与作者自己前作对比的标准句式，先详述旧方法机制，再点出新方法的改进点。

### 4.9 "The difference is that ... while our ... approach ..."
> The difference is that classical Costas loop is used for carrier frequency recovery from suppressed-carrier modulation signals which relies high-speed analog circuits while our pilot-assisted approach used low-speed circuits. (OECC 2024)
**骨架**：The difference is that [经典方法] is used for [用途] which relies [条件A] while our [本方法] approach used [条件B].
**用法**：用"The difference is that ... while ..."做精确的差异点对比，"while" 标志对比转折。

### 4.10 "Compared to terrestrial ..., [本系统] has several differences. First, ... Second, ..."
> Compared to terrestrial optical communication systems, OISL has several differences. First, ... Second, ... Third, ... Finally, ... (ICUMT 2015)
**骨架**：Compared to [参照系统], [本系统] has several differences. First, [差异1]. Second, [差异2]. Third, [差异3]. Finally, [差异4].
**用法**：系统性对比两类系统，先总述"several differences"再用"First/Second/Third/Finally"逐条列举。

### 4.11 "[方法A] is commonly used in [场景A]. [方法A] provides poor ... for [场景B] since ..."
> M-th power is commonly used in QPSK modulation. M-th power operation provides poor phase noise tolerance for higher-order modulation since an only fraction of constellation points are used for phase noise estimation. (APCCAS 2022)
**骨架**：[方法A] is commonly used in [场景A]. [方法A] provides poor [指标] for [场景B] since [原因].
**用法**：先承认基线在窄场景的适用性，再用"since"点出其推广到更宽场景时的局限。

---

## §5 章引言句式（section/intro opening）

### 5.1 "The deployment of ... is expanding to support ..., thereby requiring ..."
> The deployment of large-scale satellite constellations is expanding to support global broadband connectivity, Earth observation, and other data-intensive applications, thereby requiring reliable and high-capacity inter-satellite links [1]. (OFC 2026)
**骨架**：The deployment of [系统趋势] is expanding to support [应用列表], thereby requiring [需求].
**用法**：Intro 首句——从大趋势切入，用 "thereby requiring" 自然引出技术需求，建立必要性。

### 5.2 "However, the [问题]—caused by [原因]—introduces ... This ... leads to ..., severely degrading ..."
> However, the Doppler shift—caused by relative satellite motion—introduces a time-varying carrier frequency offset. This offset leads to spectral shifts and symbol-phase rotation, severely degrading receiver performance. (OFC 2026)
**骨架**：However, the [问题]—caused by [原因]—introduces [后果A]. This [后果A] leads to [后果B], severely degrading [性能].
**用法**：Intro 问题陈述——破折号插入原因，再用"leads to ... severely degrading"链式展开危害。

### 5.3 "As the [现状] becomes increasingly congested, [本文技术] have seen significant development"
> As the Radio Frequency (RF) spectrum becomes increasingly congested, optical links in satellite communications have seen significant development in the recent years. (ICSOS 2025)
**骨架**：As the [现状/趋势] becomes increasingly [负面], [本文技术] have seen significant development in the recent years.
**用法**：Intro 背景——"As ... becomes increasingly ..." 对比旧技术的瓶颈与新技术的兴起。

### 5.4 "[技术] has recently emerged as a promising ... However, [技术] propagation is affected by ..."
> FSO has recently emerged as a promising communications technology. The need to shift to optical carriers has emerged due to ... However, optical signal propagation is affected by absorption, scattering, and changes in the atmospheric refractive index or turbulence, which causes ... (MWP 2022)
**骨架**：[技术] has recently emerged as a promising [类别]. The need to shift to [新技术] has emerged due to [驱动力]. ... However, [技术] propagation is affected by [损伤列表], which causes [后果].
**用法**：Intro 三段式压缩：兴起 → 动因 → "However" 转折点出挑战，一段内完成。

### 5.5 "[技术领域] have undergone a revolutionary evolution ..., with [指标] surging from ... to beyond ..."
> Optical communication technologies have undergone a revolutionary evolution over the past decade, with single-wavelength rates surging from 100Gbps to beyond 1.6Tbps. (OECC 2025)
**骨架**：[技术领域] have undergone a revolutionary evolution over the past decade, with [指标] surging from [值A] to beyond [值B].
**用法**：Intro 首句用 "surging from ... to beyond ..." 嵌入速率演进数字，建立升级动机。

### 5.6 "For both [场景A] and [场景B], methods using [本文技术] provide a better ... as compared to ..."
> For both fiber-optics and free-space communication networks, methods using coherent detection which exploit the phase state of the signal provide a better sensitivity and enable the use of higher-order modulation formats as compared to systems based on intensity modulation and direct detection [1][2]. (ICSOS 2019)
**骨架**：For both [场景A] and [场景B], methods using [本文技术] provide a better [指标] and enable the use of [高级特性] as compared to [对比技术].
**用法**：Intro 开篇即用 "as compared to" 对比相干检测 vs 直接检测，确立技术优越性。

### 5.7 "[本文研究对象] is an essential block to [功能] the [损伤] introduced by the [来源]"
> Carrier phase recovery (CPR) is an essential block to estimate and compensate for the phase noise introduced by the free-running lasers in coherent optical communication systems [3]. (APCCAS 2022)
**骨架**：[本文研究的模块] is an essential block to [功能] the [损伤] introduced by the [来源] in [系统] [引用].
**用法**：定位本文研究对象（CPR）的必要性和功能，"is an essential block to" 奠定研究的正当性。

### 5.8 "To solve the above problems, we propose ..."
> To solve the above problems, we propose a BPS-based CPR implementation structure in cartesian coordinates for FPGA. (APCCAS 2022)
**骨架**：To solve the above problems, we propose a [方法] in [坐标系/域] for [平台].
**用法**：Introduction 由"问题→方案"过渡的关键句，"To solve the above problems" 回指前文列举的局限。

### 5.9 "To meet the demand of ..., there has been active research on ..."
> To meet the demand of ever-growing internet traffic from next-generation datacenters, there has been active research on short-reach coherent optical communication systems [1-3]. (OECC 2024)
**骨架**：To meet the demand of [驱动因素], there has been active research on [研究方向] [引用].
**用法**：Introduction 开篇用需求驱动引出研究热度，"there has been active research on" 配连续引用。

### 5.10 "Due to the lower [代价] and higher [收益], [本技术] offer(s) an attractive alternative to ..."
> Due to the lower power consumption and higher data rates, optical intersatellite links (OISL) offer an attractive alternative to conventional RF communication. (ICUMT 2015)
**骨架**：Due to the lower [代价] and higher [收益], [本技术] offer(s) an attractive alternative to [传统技术].
**用法**：用"Due to ... and ..."列举双重优势后，用"offer an attractive alternative to"定位新技术相对传统的价值。

---

## §6 章小结句式（conclusion）

### 6.1 "We discovered ... and leveraged this correlation to propose ..."
> We discovered the periodic correlation between a Doppler shift and the Gardner TED and leveraged this correlation to propose a novel FOE algorithm. The proposed algorithm estimated the frequency offset through TED gain. (OFC 2026)
**骨架**：We discovered the [关系] between [量A] and [量B] and leveraged this correlation to propose a novel [方法]. The proposed [方法] [功能描述].
**用法**：Conclusion 首句重述核心发现 + 方法，"discovered ... and leveraged ... to propose" 串联发现与创新。

### 6.2 "In this paper, we proposed ... The simulation results show that ..."
> In this paper, we proposed a MAP estimator for 256-QAM. The pilots are inserted into the signals, and the calculation will process in blocks in parallel when estimating, which greatly improves the calculation efficiency while achieving high accuracy. The simulation results show that the MAP estimator has good performance under extremely high baud rate and large phase noise. (OECC 2025)
**骨架**：In this paper, we proposed a [方法] for [对象]. [技术特征描述], which greatly improves [指标A] while achieving [指标B]. The simulation results show that [方法] has good performance under [极端条件].
**用法**：Conclusion 单段式——"In this paper, we proposed" 开头 + 技术特征 + "The simulation results show" 收束，紧凑一段。

### 6.3 "A [方法] was presented using a new [核心模块] method, which can ..."
> An all-digital OPLL was presented using a new phase discriminator method, which can track an optical received signal subject to the turbulence effects. The phase discriminator is a digital type that proved capable of tracking ... (MWP 2022)
**骨架**：A [方法] was presented using a new [核心模块] method, which can [功能]. The [模块] proved capable of [能力] under [条件].
**用法**：Conclusion 被动语态开头（"was presented"）重述方法 + 逐项列能力，适合无数字结论的定性收束。

### 6.4 "Future work is underway to ..."
> Future work is underway to implement the hardware of the proposed OPLL. (MWP 2022)
**骨架**：Future work is underway to [下一步工作].
**用法**：Conclusion 末句用 "Future work is underway to" 一句给出未来工作，会议论文最常见的收尾。

### 6.5 "To the best of our knowledge, no ... has been reported yet."
> To the best of our knowledge, no on-orbit demonstration of a coherent LEO-to-ground link in this configuration has been reported yet. (ICSOS 2025)
**骨架**：To the best of our knowledge, no [演示/实现] of [配置] has been reported yet.
**用法**：Conclusion/Prospects 末句用 "To the best of our knowledge ... has been reported yet" 声明工作的新颖性/空白。

### 6.6 "The whole study was conducted here assuming ... However, ... has been investigated in [ref]."
> The whole study was conducted here assuming a constant amplitude signal. However, amplitude variations will remain after the AO system in a practical FSO satellite to earth downlink. The performance of the described digital receiver in the presence of realistic atmospheric turbulence conditions has been investigated in [9]. (ICSOS 2019)
**骨架**：The whole study was conducted here assuming [简化假设]. However, [实际情况] will remain in [场景]. The performance ... has been investigated in [引用].
**用法**：Conclusion 坦诚声明简化假设的局限 + 指向配套论文，体现学术审慎。

### 6.7 "We propose ... It implements ... at low ... without ... It avoids ... and has a low [指标] of [数值]."
> We propose a CPR hardware implementation structure for optical communication that reduces computational complexity and optimizes it on the Xilinx ZCU102 board. It implements an unsimplified BPS-based CPR at low complexity without using coordinate conversion and standard multiplier. ... It avoids coordinate conversion and standard multiplier and has a low latency of 18 clock cycles. (APCCAS 2022)
**骨架**：We propose a [方法] for [应用] that [核心优势1]. It implements [完整功能] at low [代价] without using [排除项]. ... It avoids [排除项] and has a low [指标] of [数值].
**用法**：会议论文 Conclusion 单段式——重述方法+核心设计取舍+关键数字（18 时钟周期），全程散文无分点。

### 6.8 "We have proposed the [方法], which achieves ... The proposed method has a [数值]. ... provides an attractive solution for ..."
> We have proposed the DSP-free carrier phase recovery based on pilot tone assisted phase compensation in FSON, which achieves the demultiplexing of 100-Gb/s DP-QPSK without using DSP ASICs. ... The proposed method has a 1-MHz frequency compensation range. We also measured 200-Gb/s 16-QAM ... The proposed scheme provides an attractive solution for upgrading traditional PAM-4-based datacenters to coherent datacenter interconnects. (OECC 2024)
**骨架**：We have proposed the [方法], which achieves [核心功能] without using [排除项]. ... The proposed method has a [数值]. We also [扩展验证]. The proposed scheme provides an attractive solution for [应用前景].
**用法**：Conclusion 单段四步——方法重述+条件化数字+扩展能力+应用前景，末句用"provides an attractive solution for"展望落地价值。

### 6.9 "We presented an analysis of ..., which is used for ... Depending on ... will end either in ... or in ..."
> We presented an analysis of the nonlinear OPLL, which is used for carrier recovery in optical intersatellite links. ... Depending on the initial frequency offset as well as the noise influence trajectories will end either in a stable lock point or in a stable but unlocked periodic state. (ICUMT 2015)
**骨架**：We presented an analysis of [研究对象], which is used for [用途]. The [系统] is required for [目的] in order to [功能]. ... Depending on [条件] will end either in [结果A] or in [结果B].
**用法**：理论型论文 Conclusion——重述研究对象→必要性→理论贡献→核心定性结论（二选一结局）。

---

## §7 段落过渡模式（paragraph transition）

### 7.1 "A residual [问题] still remains, due ... It is then the role of the [本文模块] to ..."
> A residual frequency shift still remains, due among other things to the frequency instability of the emitter laser and LO. It is then the role of the DPLL to compensate for this residual frequency mismatch as well as for any additional small phase variation ... (ICSOS 2019)
**骨架**：A residual [问题] still remains, due [原因]. It is then the role of the [本文模块] to compensate for [问题A] as well as for [问题B].
**用法**：节内过渡——先指出"残留问题"，再用"It is then the role of ..." 自然引出本文模块的职责，逻辑链紧密。

### 7.2 "However, a [信号] does not have [属性] since ... Therefore, according to ..., a [措施] is employed to ..."
> However, a digitally modulated signal does not have a carrier since modulation suppresses it. Therefore, according to the modulation scheme, a different circuit is employed to remove the modulation signal, resulting in an unmodulated carrier to track. (MWP 2022)
**骨架**：However, a [信号] does not have [属性] since [原因]. Therefore, according to [方案], a [措施] is employed to [目的], resulting in [结果].
**用法**："However ... since ... Therefore ..." 三段过渡——指出矛盾、给原因、提对策，是节内论证的典型衔接。

### 7.3 "Thus, considering the tradeoff between [维度A] and [维度B], we set [参数] = [值]"
> However, a larger Lblk means higher computational complexity. Thus, considering the tradeoff between performance and complexity, we set Lblk = 128 in the following experiments. (OECC 2025)
**骨架**：However, a larger [参数] means higher [代价]. Thus, considering the tradeoff between [维度A] and [维度B], we set [参数] = [值] in the following experiments.
**用法**：参数选择段的过渡——先点出参数增大的代价，"Thus, considering the tradeoff" 引出折中决策。

### 7.4 "This paper then proposes ..."
> This paper then proposes a discrete-time (DT) modeling of the described coherent receiver, based on a hybrid ODPLL for the homodyne demodulation ... (ICSOS 2025)
**骨架**：This paper then proposes a [方法] of the described [系统], based on [架构] for the [功能] of a [链路类型].
**用法**：Approach 小节末向本文工作的过渡，"This paper then proposes" 由背景转向贡献，衔接自然。

### 7.5 "The paper is organized as follows. Section II introduces ... Section III details ... Lastly, ..."
> The paper is organized as follows. Section II introduces the relevant orbital and Doppler-related data. Section III details the methodology ... The implementation in MATLAB-Simulink is described in Section IV. Simulation results ... are subsequently presented in Section V. Lastly, the conclusion and prospects are given. (ICSOS 2025)
**骨架**：The paper is organized as follows. Section II introduces [内容A]. Section III details [内容B]. [内容C] is described in Section IV. [内容D] are subsequently presented in Section V. Lastly, the conclusion and prospects are given.
**用法**：会议论文少数保留的"结构导航"段（Outlines 小节），逐节概述。注意：**仅 ICSOS 2025/ICUMT 2015 有此类回指段，其余 6 篇均无**——会议论文通常省略。CCISP 短篇建议省略。

### 7.6 "After [前级处理], we use [算法] to refine [估计目标]"
> After coarse phase compensation, we use ML algorithm to refine phase estimation. (OECC 2025)
**骨架**：After [前级处理], we use [算法] to refine [估计目标].
**用法**：级联算法步骤间的极简过渡，"After ... we use ... to refine" 一句衔接两级，无回指。

### 7.7 "According to the [算法] described in section II, the structure of [系统] consists of ..."
> According to the BPS described in section II, the structure of CPR consists of five modules: (a) phase rotation (PR), (b) multi-mode decision (MD), ... (APCCAS 2022)
**骨架**：According to the [算法/方法] described in section [编号], the structure of [系统] consists of [N] modules: (a) [模块1], (b) [模块2], ...
**用法**：章节间过渡——回指前节定义的算法，自然过渡到本节的硬件结构拆分，用"consists of"列举子模块。

### 7.8 "As shown in Fig. X, the [信号] is first input to the [模块A]. After [操作], the result will be [并行输入] [模块B]"
> As shown in Fig. 2, the received signal is first input to the phase rotation module. After multiple rotations, the result will be parallel input [下一模块] ... (APCCAS 2022)
**骨架**：As shown in Fig. [编号], the [信号] is first input to the [模块A]. After [操作], the result will be [并行输入] [模块B] ...
**用法**：信号流过渡——按数据流动方向逐模块描述，"is first input to → After ... → will be input to" 串联处理链。

### 7.9 "In the previously proposed [结构] [引用], [器件] is used as [角色], which is split into ... So the [代价] can be shared by ..."
> In the previously proposed FSON structure [9], one stable narrow linewidth laser is used as source, which is split into many branches and subsequently distribute to all the transmitters (Txs) and receivers (Rxs) ... So the cost of one or a few narrow linewidth lasers can be shared by hundreds of transponders. (OECC 2024)
**骨架**：In the previously proposed [结构] [引用], [器件] is used as [角色], which is split into ... So the [代价] of [器件] can be shared by [数量] [节点].
**用法**：实验设置节开头——先复述已有系统结构，再用"So"引出该结构的成本优势，为本文方案铺垫。

### 7.10 推导链内部过渡动词："Inserting (X) in (Y) results in / Transforming (X) into ... results in / After rearranging (X)"
> Inserting (4) and (11) in (7) results in ... (ICUMT 2015)
> Transforming (6) into time domain results in ... (ICUMT 2015)
> After rearranging (12) the nonlinear differential equation is ... (ICUMT 2015)
> Deriving the phase error gives ... (ICUMT 2015)
**骨架**：[推导动词] ([公式A]) and ([公式B]) in ([公式C]) results in [新公式] / Transforming ([公式]) into [域] results in [新公式] / After rearranging ([公式]) the [产物] is [新公式]
**用法**：公式推导链的标准衔接——每步都用"动词 + 公式编号 + results in/is/gives"结构，公式编号回指保证可追溯。ICUMT 2015 是理论推导型，此类过渡最密集。

### 7.11 "The above mentioned statements concerning [结论] can be verified by ..."
> The above mentioned statements concerning lock-in and hold-in range can be verified by looking at the phase plane diagram for different frequency offsets Δω in (15). (ICUMT 2015)
**骨架**：The above mentioned statements concerning [结论] can be verified by [方法] for different [参数] in (公式).
**用法**：从前文结论过渡到图证验证，"The above mentioned statements" 回指前文。

---

## §8 贡献表述模式（contribution statement）

> **会议论文贡献表述核心特征**：Intro 末段散文式 3-4 句带数字，**无 bullet list**，靠副词递进衔接。以下是从 8 篇提取的典型贡献段结构。

### 8.1 "In this work, we discover ... Building on this ..., we propose ... The experimental results ... demonstrate that ..."
> In this work, we discover the periodic correlation between the Doppler shift and the Gardner timing error detector (TED). Building on this correlation, we propose a novel FOE algorithm that estimates the Doppler shift by calculating the Gardner TED gain. The experimental results from a 25-Gbaud dual-polarization quadrature phase shift keying (DP-QPSK) transmission demonstrate that the proposed algorithm achieves a Doppler-shift estimation range 1.9 times that of conventional algorithms. Providing noise-robust estimation enhances receiver sensitivity by 0.6 dB and enables successful demodulation even under a low optical signal-to-noise ratio of 10 dB. (OFC 2026)
**骨架**：In this work, we discover [核心发现]. Building on this [发现], we propose a novel [方法] that [功能] by [机制]. The experimental results from a [系统配置] demonstrate that the proposed [方法] achieves a [指标] [倍数] times that of [对比方法]. [特性] enhances [指标] by [数值] dB and enables [能力] even under [极端条件] of [数值] dB.
**用法**：Intro 末段贡献——散文式 4 句带 3 个数字（倍数、灵敏度增益、OSNR），无 bullet list，"discover → propose → demonstrate → enhances" 四步递进。

### 8.2 "This paper thus proposes ... Unlike the prior work [ref], we extend ... Specifically, ... Simulations demonstrate that ..."
> This paper thus proposes a joint ML/MAP estimation algorithm based on a time-varying Wiener phase noise model. Unlike the prior work [5], we extend this framework to 256-QAM modulation and with the Additive Observed Phase Noise (AOPN) model ... Specifically, the signal phase is modeled as the superposition of ... Simulations demonstrate that the proposed algorithm achieves good performance in high symbol rates for 256-QAM. (OECC 2025)
**骨架**：This paper thus proposes a [方法] based on a [模型]. Unlike the prior work [引用], we extend this framework to [对象] and with [新模型]. Specifically, [建模描述]. Simulations demonstrate that [方法] achieves [性能] in [场景].
**用法**：贡献段——"Unlike the prior work" 明确与前人区别 + "Specifically" 给建模细节 + "Simulations demonstrate" 定性收束。

### 8.3 "Therefore, taking advantage of [技术列表], this study proposes ... Additionally, ... Thus, [方法] will use ... The system, supported by [工具], will be evaluated under ..."
> Therefore, taking advantage of OPLL and DSP techniques, such as real-time data recovery and flexibility of parameters reconfiguration, this study proposes a fully digital OPLL to demodulate a digitally modulated optical signal. Additionally, the optical signal propagating an LEO slant path ... will be considered. Thus, OPLL will use a digital phase detector to handle a fading signal ... The system, supported by simulations using VPIphotonics under a co-simulation technique, will be evaluated under three scenarios of atmospheric turbulence and several wind speed values. (MWP 2022)
**骨架**：Therefore, taking advantage of [技术列表], this study proposes a [方法] to [功能]. Additionally, [场景] will be considered. Thus, [方法] will use [模块] to handle [问题]. The system, supported by [工具], will be evaluated under [条件列表].
**用法**：Intro 末段贡献——"Therefore ... this study proposes" 开头，多个"Additionally / Thus" 展开子贡献，末句交代验证手段与条件。

### 8.4 "In this study, a [方法] based on [架构] for [功能] is proposed. ... The simulated [模型] achieves ... even when submitted to ..."
> In this study, a Z-transform modeling of a coherent receiver based on a hybrid Optical-Digital Phase-Locked Loop (ODPLL) for Doppler compensation and frequency synchronization is proposed. In the envisioned architecture, ... The system latency is taken into account ... The simulated behavioral model achieves successful Quadrature Phase-Shift Keying (QPSK) demodulation even when submitted to strong Doppler rates, and under realistic received power levels. (ICSOS 2025)
**骨架**：In this study, a [方法] based on [架构] for [功能] is proposed. In the envisioned architecture, [细节]. The system [考量] is taken into account. The simulated [模型] achieves successful [功能] even when submitted to [极端条件], and under [现实条件].
**用法**：Abstract 中的贡献压缩版——被动语态 "is proposed" + "achieves ... even when" 带极端条件，摘要式表述。

### 8.5 "We present a [系统] which combines [模块A], to [功能A], with [模块B]. The latter is based on [技术]. As an example, we show that ..."
> We present a coherent receiver architecture which combines adaptive optics correction, to mitigate the atmospheric turbulence detrimental effect, with a digital carrier synchronization system. The latter is based on a phase-locked loop ... We describe the methodology followed to design such a digital phase-locked loop. As an example, we show that the digital PLL is able to compensate a residual frequency mismatch of 300MHz with a convergence time inferior to 1s ... (ICSOS 2019)
**骨架**：We present a [系统] which combines [模块A], to [功能A], with [模块B]. The latter is based on [技术]. We describe the methodology followed to design [模块]. As an example, we show that the [模块] is able to [功能] a [指标] of [数值] with a [指标] inferior to [数值].
**用法**：Abstract 贡献——"We present ... We describe ... As an example, we show that ..." 三句递进，末句嵌入核心数字（300 MHz、<1s）。

### 8.6 "To solve the above problems, we propose ... A [器件] is employed to ... which will significantly reduce ... compared with ... Additionally, [手段B] are employed to ... without using ... Besides, [手段C] also ... Experiments evaluate ... at [配置], [指标A] can reach [数值], and [指标B] is [数值]."
> To solve the above problems, we propose a BPS-based CPR implementation structure in cartesian coordinates for FPGA. A 9-bit constant-coefficient multiplier-accumulator (CC-MAC) array in Cartesian coordinate is employed to implement the phase rotation module, which will significantly reduce computational complexity compared with the standard multiplier and meets the signal-to-noise ratio (SNR) requirement. Additionally, Look-up tables (LUTs) are employed to store square coefficients to complete the calculation of the partial error distance without using the multiplier. ... Besides, the output of phase recovery also uses multiplexing between adjacent clock cycles to reduce latency. ... Experiments evaluate the circuit structure on the Xilinx ZCU102 platform at 32-way parallel, the clock frequency can reach 620MHz, and the latency of processing 79.3Gbps 16QAM signal is 18 clock cycles. (APCCAS 2022)
**骨架**：To solve the above problems, we propose [方法]. A [器件/模块] is employed to [功能], which will significantly reduce [代价] compared with [基线] and meets the [指标] requirement. Additionally, [手段B] are employed to [功能] without using [排除项]. Besides, [手段C] also [功能]. Experiments evaluate [平台] at [配置], [指标A] can reach [数值], and [指标B] is [数值].
**用法**：会议论文 Intro 末段贡献表述的典型散文式——"问题→方案→3个技术手段（Additionally/Besides 递进）→实验数字收束"，全程无分点编号，靠副词衔接。

### 8.7 "In this paper, we propose ... Compared to our previous work ..., this paper proposed ... Additionally, we only use ... to achieve ... without resorting to ... Further, we experimentally demonstrate ... with [数值]. Lastly, we also show ..."
> In this paper, we propose a novel pilot tone assisted Costas phase-locked loop to compensate for LO frequency/phase offsets in coherent systems based on our previously propose concept ... Compared to our previous work using power monitor module (PMM) ..., this paper proposed ... acquires the phase error more accurately and thus improve the performance ... Additionally, we only use low-speed circuits to achieve dual polarization coherent detection without resorting to conventional highspeed DSP ASICs. Further, we experimentally demonstrate the DSP-free demultiplexing of 100-Gb/s DP-QPSK to four 25-Gb/s-tributaries with 1-MHz frequency compensation range and 1-kHz dynamic compensation bandwidth. Lastly, we also show the ability of the proposed scheme to support high order modulation formats. (OECC 2024)
**骨架**：In this paper, we propose [方法] to [功能]. Compared to our previous work using [旧方法], this paper proposed [新方法] [优势]. Additionally, we only use [简化手段] to achieve [功能] without resorting to [昂贵手段]. Further, we experimentally demonstrate [功能] with [数值A] and [数值B]. Lastly, we also show the ability of [方法] to [扩展能力].
**用法**：贡献段用四个递进副词组织（Compared to / Additionally / Further / Lastly），每条带一个量化点或对比点，散文式但层次清晰。

---

## 会议论文写法特点（8 篇综合，vs 学位论文差异）

基于对 8 篇 IEEE/OFC/OECC 会议论文全文的精读，归纳其与中文长篇学位论文在写法上的显著差异：

1. **整体更紧凑，篇幅短**。OFC 2026 仅 90 行（约 2 页正文），Conclusion 几乎都是**单段式**（如 OECC 2025 用 "In this paper, we proposed ... The simulation results show ..." 一段收尾），而非学位论文的七层递进式本章小结。

2. **贡献是散文，不是 bullet list**。8 篇 Intro 末段/Abstract **全部**用连贯散文陈述贡献（如 OFC 2026 的 "discover → propose → demonstrate → enhances" 四句递进；APCCAS 2022 的 "To solve... Additionally... Besides..."；OECC 2024 的 "Compared to... Additionally... Further... Lastly..."），**无一使用** "本文主要贡献如下：(1)...(2)..." 的编号列表。这与学位论文体例截然不同。

3. **几乎无"下一节将…"回指**。仅 ICSOS 2025 和 ICUMT 2015 保留了 "The paper is organized as follows. Section II ..." 的结构导航段，其余 6 篇节间过渡靠 "However / Therefore / After ... we use ... / As shown in Fig. X" 等逻辑词直接衔接，无显式章节预告。会议论文倾向省略 roadmap。

4. **公式少而精，参数解释一句话内完成**。会议论文公式密度低（OFC 2026 正文几乎无编号公式，全靠图+散文；ICUMT 2015 理论型偏密），且参数解释常与公式挤在同一句内（如 MWP 2022 的 "is given by F(z)=..., where K1 and K2 are the loop filter gains"；ICUMT 2015 的密集列举首项给动词其后省略），不另起段落。

5. **Related work 极简**。Intro 中对前人工作的梳理通常只有 3–5 句（如 OECC 2025 用一句概括 "pilot-aided methods ... sacrifice spectral efficiency" 即转向本文方案），无学位论文式的逐方法分小节综述。

6. **数值嵌入更"硬核"，一句话塞多个数字**。如 OFC 2026 一句同时给出 "1.9 times"、"0.6 dB"、"10 dB" 三个性能数字；OECC 2025/APCCAS 2022 用 "respectively" 一次列举多个方法/条件的数值。

7. **方法对比直接用 "while / Compared to / Unlike ... which" 强对比**。如 MWP 2022 "The sinusoidal discriminator always loses lock ... while the proposed discriminator keeps the system locked"；OECC 2024 "Unlike the current PAM4 scheme, which utilizes only amplitude modulation dimension, coherent ... also use phase ..."，对比句式短促有力，不铺陈。

8. **Conclusion 频繁用被动语态开头，单段收尾**。如 MWP 2022 "An all-digital OPLL was presented ..."、ICSOS 2025 "A discrete-time modeling ... was proposed"，且常以 "Future work is underway to ..." 或 "To the best of our knowledge, no ... has been reported yet" 单句收尾，简洁。

9. **副词递进组织贡献/子点**（学位论文罕见）。APCCAS/OECC 常用 "Additionally / Besides / Further / Lastly" 串联 3-4 个技术点或子贡献，不靠分点编号。

### 与学位论文句式库（writing-patterns-sentence.md）的复用关系

会议论文与学位论文在以下句式上**高度通用**，写英文正文时可直接套用本库骨架：

- 公式引入：`can be expressed as / is given by / is modeled as` ↔ 学位论文"可以表示为"
- 参数解释：`where ... denotes/is/represents` ↔ 学位论文"式中，A 为…"
- 方法对比：`Compared with ... the proposed ...` ↔ 学位论文"相比于…本文方法…"
- 近似引入：`can be approximately derived as / The approximation is valid considering that` ↔ 学位论文"由于…可以近似"

**会议论文特有（学位论文句式库没有的）**：
- 贡献散文式递进（discover→propose→demonstrate→enhances / To solve...Additionally...Besides...）
- 倍数+灵敏度+OSNR 一句三数字的硬核嵌入
- "Future work is underway to" / "To the best of our knowledge, no ... has been reported yet" 收尾句
- "Unlike the [基线], which [局限], [本方法] also use ... thereby" 多维度优势展开
- 结构导航段（仅部分会议论文保留，CCISP 短篇建议省略）

### 参考文献

- 8 篇引用数：ICUMT 2015 仅 6 篇、OECC 2024 为 10 篇、APCCAS 2022 为 12 篇，ICSOS/OFC/OECC/MWP 强相关 5 篇多在 6-12 篇区间。**符合会议论文篇幅受限、引用精简的共性**。CCISP 建议 10-15 篇。
