# 第一章 绪论（选题依据）— 模板测试稿

> 基于 S004 模板结构填充实际内容。每段标注模板功能(P#)，方便对照。
> 引用使用 [Author, Year] 占位，需后续转 GB7714 格式。
> **这不是最终稿，是模板效果测试。** D009原则：用户自己写终稿。

---

## 1.1 研究背景与意义

【P1: 宏观背景 → 卫星通信→激光通信】

随着全球信息化进程加速，卫星通信成为弥补地面网络覆盖不足的关键手段。低轨（LEO）卫星星座凭借低时延和低发射成本优势，已成为天基网络的主流方向。激光通信相较于传统微波通信，具有带宽大（潜在速率超100Gbps）、抗电磁干扰、无需频谱许可等突出优势，被视为下一代星地链路的核心技术[Kaushal, 2016]。近年来，星地激光通信从实验室走向工程验证：NASA的LCRD项目实现了双向激光通信，ESA的EDRS系统已投入业务运行；我国于2024年完成120Gbps星地激光通信试验验证，标志着该技术进入工程化阶段。

【P2: 本文主题 + 整体挑战】

然而，激光信号穿越大气层时受湍流效应影响，导致接收端光强闪烁、相位扰动和光束漂移，严重制约链路可靠性[Xu, 2025]。星地激光通信信号处理旨在从受损接收信号中恢复原始信息，需在信道建模与估计、信道均衡和载波同步三个环节协同应对大气湍流挑战。

【P3: 挑战1 — 信道建模与估计】

首先，大气湍流信道具有随机快变的统计特性。Gamma-Gamma（GG）模型是覆盖弱到强湍流场景的通用统计模型[曹明华, 2020]，但其核心参数随链路仰角、季节动态变化[Xu, 2025]。传统信道估计方法（如最小二乘LS、最小均方误差MMSE）在信道统计先验已知时性能良好，参数失配或非平稳条件下性能显著下降[Amirabadi, 2019]。

【P4: 挑战2 — 信道均衡】

其次，大气湍流引起的多径效应导致严重的码间干扰。常数模算法（CMA）和判决反馈均衡器（DFE）在弱湍流下能有效抑制干扰[佟欣, 2020]，但中强湍流（闪烁指数σ²_I≥1）下，深度衰落使CMA收敛困难、DFE判决错误传播加剧[Almogahed, 2022]。

【P5: 挑战3 — 载波同步】

第三，LEO卫星高速运动产生大多普勒频移（可达±4.6GHz），需发射端预补偿后，接收端仍需处理残余频偏与激光器相位噪声的叠加影响[Yan, 2026]。Viterbi-Viterbi算法和盲相位搜索（BPS）是相干光通信中经典的载波相位恢复方法[Liu, 2023]，但二者在大气湍流强度变化下的性能差异和适用边界尚不明确。

【P6: 过渡 → 本文工作】

上述三个层面——信道估计精度、均衡鲁棒性和载波同步可靠性——共同决定了星地激光通信系统的整体性能，构成信号处理的核心挑战。为解决上述问题，本文从这三个层面开展研究工作。

【P7-9: 三项工作概述】

（1）针对大气湍流信道估计问题，第二章在GG模型框架下系统对比LS、MMSE与深度学习方法的估计精度，量化不同湍流强度下各方法的适用边界。（2）针对湍流信道均衡问题，第三章对比CMA、MMSE-DFE等传统方法与深度学习均衡器在多种湍流场景下的性能。（3）针对载波同步问题，第四章系统分析VV、BPS、导频辅助等方法在不同湍流强度下的性能表现，提出基于湍流强度的自适应切换策略。

---

## 1.2 国内外研究现状

【开篇P1: 大背景缩小到信号处理】

星地激光通信系统的性能受大气信道特性制约。与微波通信不同，激光波长短（1550nm典型），大气湍流对其影响远大于对微波的影响。表1-1对比了卫星微波通信与星地激光通信的关键特征差异。

*（此处插入表1-1：卫星微波 vs 激光通信特征对比）*

【开篇P2: 三个维度挑战】

从信号处理角度，大气湍流对星地激光通信的影响可归纳为三个维度：（1）信道衰落导致接收信号幅度和相位的随机波动，需精确估计信道状态；（2）信道色散引起码间干扰，需有效均衡；（3）载波频率偏移和相位噪声影响相干检测，需精确同步。

【开篇P3: 过渡到具体方向】

以下分别从大气信道建模与估计、信道均衡和载波同步三个方向展开综述。

### 1.2.1 大气信道建模与估计研究现状

【P1: 定义+重要性】

大气信道建模是星地激光通信系统设计的理论基础。信道模型的准确性直接影响后续均衡、同步等信号处理模块的性能上限。在星地链路中，大气湍流导致光束振幅和相位的随机波动，信道建模的核心任务是建立这种随机衰落的统计描述。

【P2: 估计任务】

信道估计的任务是利用已知信号（导频或训练序列）从接收信号中恢复信道状态信息（CSI），为均衡器提供信道先验，为检测器提供判决依据。

【P3: 方法分类 — 归纳句先行】

现有信道估计方法按是否依赖信道统计先验可分为两大类：基于统计模型的方法和基于数据驱动的方法。前者以LS、MMSE和Kalman滤波为代表，后者以各类神经网络为主。

【P4: 传统方法优缺点】

LS估计器结构简单，不依赖信道先验，但低信噪比下噪声放大严重，估计精度受限。MMSE估计器在已知信道协方差矩阵时理论上达到贝叶斯最优，但矩阵求逆计算复杂度为O(N³)，且实际系统中协方差矩阵难以精确获取。Kalman滤波器可跟踪时变信道，但GG信道的非线性使得状态空间模型建立困难。

【P5: DL方法引入+优缺点】

为克服传统方法依赖统计先验的局限，研究者将深度学习应用于FSO信道估计。Amirabadi等[2019]首次在GG信道下验证DNN估计器可达到接近理想CSI的性能，且无需导频序列。然而，DL方法在训练数据分布外的泛化能力存疑，低信噪比下训练不稳定性突出。

【P6: 综述表】

表1-2汇总了近年来FSO信道估计领域的代表性工作。

| 方法 | 架构 | 信道模型 | 湍流范围 | 关键结果 |
|------|------|---------|---------|---------|
| Amirabadi 2019 | DNN | GG | 弱→强 | SER接近理想CSI |
| Elfiky 2023 | NN+AE | GG/Lognormal | LEO/GEO | 端到端优化 |
| Rustum 2026 | STA+SRCNN | GG+多普勒 | LEO OFDM | NMSE≈10⁻³@11dB |
| Mohammed 2026 | CNN+BiLSTM | GG | 弱/中/强 | 优于LS/LMMSE/EKF |
| Zhou 2024 | Meta-CE | GG | 强(4×4 MIMO) | MSE比MMSE低35% |

【P7: 文献例举 — 先归纳后展开】

这些工作均采用神经网络架构，在GG湍流信道下取得了优于传统方法的估计精度。其中，Rustum等[2026]针对LEO-OFDM系统提出STA粗估计与DL细估计的两阶段方案，在64-QAM@11dB SNR下实现NMSE≈10⁻³，EVM仅8%。Mohammed等[2026]采用CNN提取空间特征、BiLSTM建模时序依赖的混合架构，在弱至强湍流范围内均优于LS、LMMSE和EKF。Zhou等[2024]引入元学习策略，仅用8-bit导频在0dB SNR下即实现MSE较MMSE降低35%，展示了小样本适应潜力。

【P8: 本质缺陷 — 从方法论层面】

尽管DL方法在特定场景下展示了优势，现有研究存在两个根本性不足。第一，多数工作假设信道统计特性在观测窗口内平稳，未充分考虑湍流的时变特性。第二，DL方法与物理信道模型的融合不足，网络未显式利用GG分布的统计特性，导致跨湍流条件泛化能力差。

【P9: 缺陷详述】

具体而言，GG信道的闪烁指数σ²_I随仰角和天气变化可跨越3个数量级（从弱湍流<0.1到强湍流>5），训练于特定湍流范围的DL模型在参数漂移时性能退化。此外，现有研究多针对地面水平链路或单一LEO场景，动态仰角导致的湍流参数连续变化尚未被系统研究。在传统方法方面，LS、MMSE和Kalman在GG模型下的系统性对比同样缺失——几乎所有DL论文仅以LS作为简单baseline，未充分比较多种传统方法的性能边界。

【P10: 小结→引出本文Ch2】

因此，当前信道估计方向的核心瓶颈在于时变适应能力和物理模型融合。本课题第二章旨在GG模型框架下系统对比LS、MMSE与DL方法在不同湍流强度下的估计精度，明确各方法的适用边界。

### 1.2.2 信道均衡研究现状

【P1: 定义+重要性】

信道均衡是消除码间干扰（ISI）、恢复信号波形的关键技术。在星地激光通信中，大气湍流引起的光强闪烁和脉冲展宽导致前后码元叠加，均衡器的性能直接影响误码率。

【P2: FSO均衡的特殊性】

与射频通信不同，FSO系统可采用强度调制/直接检测（IM/DD）或相干检测两种体制。IM/DD系统信号为实值，均衡器设计相对简单；相干检测系统信号为复值，需同时处理I/Q两路，均衡器设计更复杂但也更具优势——相干检测可利用信号的幅度和相位信息，在高阶调制下性能更优[李林, 2020]。

【P3: 方法分类】

现有FSO均衡方法按原理可分为四类：线性均衡（MMSE/ZF）、判决反馈均衡（DFE）、盲均衡（CMA）和基于深度学习的均衡。

【P4: 传统方法 — CMA/MMSE-DFE】

CMA算法利用信号的恒模特性实现盲均衡，无需训练序列，在空间激光通信中已有应用[佟欣, 2020]。但CMA收敛速度慢，对相位不敏感，需额外载波恢复模块。MMSE-DFE结合前馈和反馈滤波器，用MMSE准则优化抽头系数，在MDM-FSO系统中已验证有效性[Almogahed, 2022]，BER可达FEC阈值。

【P5: DL方法引入】

深度学习均衡器可自适应学习信道非线性特征，在强湍流下展示出超越传统方法的潜力。Ahmad等[2026]在OAM-FSO系统中采用DNFIS+DCNN方案，BER降低55%，获得10dB功率增益。然而，该工作系统复杂度高（OAM+AO+WDM+DL），简单点对点FSO场景下DL均衡器的增益尚不明确。

【P6: 综述表】

表1-3汇总了FSO信道均衡领域的代表性工作。

| 方法 | 体制 | 信道模型 | 调制 | 关键结果 |
|------|------|---------|------|---------|
| Almogahed 2022 | MDM-FSO | 多径 | OOK | MMSE-DFE达FEC阈值 |
| Ahmad 2026 | OAM-WDM | GG+AO | 多载波 | BER降55%, 10dB增益 |
| Balakrishnan 2026 | OFDM-FSO | GG | 256-QAM | ZF均衡弱湍流BER=10⁻¹² |
| 佟欣 2020 | 空间激光 | 未指定 | — | CMA-LMS变步长收敛 |
| 李林 2020 | 相干FSO | GG | 高阶 | AO+数字联合补偿 |

【P7: 文献例举】

在传统均衡方向，Almogahed等[2022]系统验证了MMSE-DFE在MDM-FSO中的效果，10Gbps传输在多种天气条件下均达FEC阈值。佟欣等[2020]提出变步长CMA-LMS算法，结合CMA的盲均衡能力和LMS的自适应跟踪，在空间激光通信中实现了稳定收敛。Balakrishnan等[2026]在GG湍流模型下分析OFDM-FSO的ZF均衡性能，给出了弱至强湍流下的具体BER数据。

【P8: 本质缺陷】

尽管上述工作分别验证了各类均衡方法的有效性，现有研究存在一个核心不足：缺乏在统一框架下对多种均衡方法的系统性对比。具体表现为，GG湍流+相干PSK+多种均衡方法（CMA/MMSE/DFE/DL）的系统性对比论文几乎找不到。

【P9: 缺陷详述】

Almogahed系列论文仅做DFE，未与CMA或DL对比；Ahmad 2026虽比较了DL与传统DFE，但场景是OAM+WDM复杂系统，结论不能直接推广到简单点对点FSO。CMA在GG湍流信道中的性能分析几乎空白——佟欣2020使用空间激光信道但未采用GG模型，也未分析不同湍流强度下CMA的收敛特性。此外，多数FSO均衡研究采用IM/DD体制，相干检测+PSK的均衡研究明显不足。

【P10: 小结→引出本文Ch3】

因此，当前信道均衡方向的核心瓶颈在于缺乏统一框架下的多方法系统性对比。本课题第三章旨在GG湍流+相干PSK的统一框架下，系统对比CMA、MMSE-DFE等传统方法与DL均衡器在弱、中、强三种湍流条件下的性能。

### 1.2.3 载波同步研究现状

【P1: 定义+重要性】

载波同步是相干检测系统的前提条件。在相干接收机中，本地振荡激光器与接收信号之间的频率偏移和相位噪声必须被精确估计和补偿，否则解调判决将产生大量错误。

【P2: 星地链路特殊挑战】

星地激光通信中的载波同步面临三重挑战：（1）LEO卫星高速运动产生大多普勒频移（±4.6GHz）[Yan, 2026]；（2）激光器线宽（kHz至MHz级）引起相位随机游走；（3）大气湍流导致接收光信号相位的随机扰动。

【P3: 方法分类】

现有载波相位恢复（CPR）方法可分为三类：基于判决的方法（Viterbi-Viterbi、BPS）、导频辅助方法和基于深度学习的方法。

【P4: 传统VV/BPS — 成熟方法】

Viterbi-Viterbi（VV）算法利用PSK信号的相位旋转不变性，通过M次方消除调制信息后估计载波相位，在QPSK系统中性能最优[Neves, 2023]。盲相位搜索（BPS）通过搜索最优相位旋转角实现载波恢复，适用于高阶调制格式，但计算复杂度随调制阶数增长[Liu, 2023]。Liu等[2023]在星地相干激光通信中对比了VV和BPS，结果表明VV适合QPSK、BPS适合高阶调制，残余频偏对二者影响不同。

【P5: DL方法引入】

深度学习载波相位恢复是新兴方向。Shi等[2025]提出基于RNN的自适应CPR算法，在光纤场景中展示了跟踪快速相位变化的能力。Blatter等[2025]用ANN实现透明CPR。然而，这些工作均针对光纤通信场景，FSO湍流信道下的DL-CPR研究几乎空白。

【P6: 综述表】

表1-4汇总了载波同步领域的代表性工作。

| 方法 | 场景 | 调制 | 关键特点 |
|------|------|------|---------|
| Liu 2023 | 星地相干 | QPSK | VV+BPS对比，双反馈环结构 |
| Shi 2025 | 光纤 | QPSK | RNN自适应CPR |
| Blatter 2025 | 光纤 | 通用 | ANN透明CPR |
| 管海军 2019 | FSO相干 | QPSK | 数字相位恢复系统验证 |
| Yan 2026 | 卫星光通信 | — | 多普勒数字估计与补偿 |
| Tang 2023 | FSO相干 | — | 联合频偏+相位低复杂度 |

【P7: 文献例举】

在星地载波恢复方向，Liu等[2023]提出双反馈环与VV前馈级联结构，在星地相干链路中实现了稳健的载波恢复，引用达15次。管海军等[2019]搭建了QPSK自由空间相干光通信系统，验证了数字相位恢复算法的可行性。Tang等[2023]提出联合频偏与相位恢复的低复杂度方案，用于相干FSO通信。Yan等[2026]实现了LEO卫星相干光通信中多普勒频移的数字估计与补偿。

【P8: 本质缺陷】

尽管载波同步在光纤和卫星光通信中均有大量研究，一个重要的研究空白是：大气湍流强度变化对各类CPR算法性能的系统性定量分析。Neves等[2023]的CPR综述论文系统梳理了VV/BPS/导频辅助等算法，但所有文献均在光纤场景，FSO场景下的CPR算法对比几乎空白。

【P9: 缺陷详述】

Liu 2023虽然做了星地链路的VV/BPS对比，但其重点是新算法（双反馈环结构）的提出，而非系统分析湍流对CPR性能的影响。Paillier等[2020]考虑了大气湍流对星地相干接收的影响，但重点是自适应光学而非CPR算法。Wang等[2024]在FSO中做了增强帧同步和载波恢复，但采用的是训练序列辅助方案，不做多种CPR方法的对比分析。湍流强度（从弱Cn²~10⁻¹⁶到强Cn²~10⁻¹³）对不同CPR算法BER性能的系统性影响，尚未找到专门研究。

【P10: 小结→引出本文Ch4】

因此，当前载波同步方向的核心瓶颈在于大气湍流对CPR算法性能的系统性影响分析缺失。本课题第四章旨在系统分析VV、BPS、导频辅助等CPR方法在不同湍流强度下的性能表现，提出基于湍流强度的自适应CPR切换策略。

### 1.2.4 现状总结与启示

综上所述，星地激光通信信号处理在三个方向均面临研究空白：（1）大气信道估计方向，传统方法（LS/MMSE/Kalman）在GG模型下的系统性对比缺失，DL方法缺乏物理模型融合和时变适应能力；（2）信道均衡方向，GG湍流+相干PSK+多种均衡方法的统一对比框架尚未建立；（3）载波同步方向，大气湍流强度对CPR算法性能的系统性定量分析几乎空白。上述三个方向的空白具有内在关联性：信道估计精度直接影响均衡器系数和载波恢复性能，三者需在统一框架下协同设计。

---

## 1.3 论文研究内容与章节安排

本文以星地激光通信系统为研究对象，围绕大气湍流下的信号处理问题，主要研究内容包括大气信道建模与估计、信道均衡和载波同步三个方面。

本文共分五章。第一章阐述了课题研究的背景与意义，综述了国内外研究现状，总结了现有工作的不足，明确了本文的研究内容。

第二章针对大气湍流信道估计问题。首先介绍GG大气湍流信道模型和传统信道估计方法（LS、MMSE）的理论基础；然后设计DNN和LSTM两种深度学习信道估计器；在GG模型下，对比分析传统方法与DL方法在弱、中、强三种湍流条件下的估计精度和误码率性能；最后对本章进行小结。

第三章针对湍流信道均衡问题。首先分析FSO信道均衡的特殊性，介绍CMA和MMSE-DFE等传统均衡方法；然后设计基于CNN和LSTM的深度学习均衡器；在GG湍流+相干QPSK的统一框架下，系统对比多种均衡方法在不同湍流强度下的BER性能和收敛特性；最后对本章进行小结。

第四章针对载波同步问题。首先介绍VV、BPS和导频辅助三种CPR算法的原理；然后在GG湍流+残余频偏+相位噪声的信道模型下，系统分析三种CPR方法在不同湍流强度下的性能边界；探索轻量级DL方法（GRU/LSTM）在湍流场景下的CPR能力；提出基于湍流强度的自适应CPR切换策略；最后对本章进行小结。

第五章对全文进行总结，归纳创新点，并对后续研究方向进行展望。

---

## 参考文献（占位列表）

[Amirabadi, 2019] Amirabadi M A. Deep learning for channel estimation in FSO communication system[J]. Optics Communications, 2019/2020. (61 cites, verified)

[Elfiky, 2023] Elfiky A, Rezki Z. Symbol detection and channel estimation for space optical communications using neural network and autoencoder[J]. 2023. (19 cites, verified, year corrected from 2024)

[Rustum, 2026] Rustum S, et al. Hybrid STA with FNN and CNN models for robust CE in turbulent FSO and Doppler-affected LEO OFDM[J]. IET Communications, 2026. (verified)

[Mohammed, 2026] Mohammed N A, et al. FSO turbulent channel estimation based on deep combined CNN and BiLSTM[J]. JOC, 2026. (verified)

[Zhou, 2024] Zhou, et al. Meta-learning for estimating atmospheric turbulence in satellite OWC[J]. IEEE IoT-J, 2024. (3 cites)

[Xu, 2025] Xu, et al. Satellite-to-ground optical communication under orbital deviations and atmospheric turbulence[J]. Optics Express, 2025. (8 cites, verified)

[曹明华, 2020] 曹明华等. Gamma-Gamma大气湍流下超奈奎斯特光通信系统性能[J]. 中国激光, 2020. (50 cites, pending CNKI verify)

[孙晶, 2018] 孙晶等. Gamma-Gamma大气湍流下相干光通信分集接收技术[J]. 光学学报, 2018. (27 cites, pending CNKI verify)

[Almogahed, 2022] Almogahed A, et al. Performance improvement of MDM-FSO with DFE[J]. Cogent Engineering, 2022. (37 cites, verified)

[Ahmad, 2026] Ahmad M, et al. Robust high-capacity FSO using OAM and intelligent adaptive signal processing[J]. Scientific Reports, 2026. (verified)

[Balakrishnan, 2026] Balakrishnan R, et al. Reliable equalization aided long-distance OFDM-FSO over GG turbulence[J]. 2026. (verified)

[佟欣, 2020] 佟欣等. 空间激光通信中变步长CMA-LMS均衡算法[J]. 光通信技术, 2020. (10 cites, pending CNKI verify)

[周超, 2018] 周超. 基于LMS算法的光通信自适应数字均衡技术[D]. 电子科技大学, 2018. (14 cites, pending CNKI verify)

[李林, 2020] 李林. 大气湍流对高阶自由空间相干光通信影响的补偿研究[D]. 中科院长春光机所, 2020. (15 cites, pending CNKI verify)

[Liu, 2023] Liu N, et al. Carrier recovery for satellite-to-ground coherent laser communication systems[J]. Optics Communications, 2023. (15 cites, verified)

[Shi, 2025] Shi, et al. Recurrent neural network enabled adaptive carrier phase recovery[J]. SPIE, 2025.

[Blatter, 2025] Blatter, et al. Transparent carrier phase recovery based on ANN[J]. 2025.

[管海军, 2019] 管海军等. 基于数字相位恢复算法的QPSK自由空间相干光通信系统[J]. 2019. (8 cites, pending CNKI verify)

[Yan, 2026] Yan, et al. Digital estimation and compensation of Doppler shift for coherent optical satellite communication[J]. 2026. (verified)

[Neves, 2023] Neves, et al. Carrier-phase recovery for coherent optical systems: Algorithms, challenges and...[J]. 2023. (39 cites)

[Paillier, 2020] Paillier, et al. Space-Ground coherent optical links: Ground receiver performance with adaptive optics[J]. JLT, 2020. (35 cites)

[Tang, 2023] Tang, et al. A low-complexity joint compensation scheme of carrier recovery for coherent FSO[J]. 2023. (7 cites)

[Wang, 2024] Wang, et al. Enhanced frame synchronization and carrier recovery in coherent FSO communication[J]. Optics Express, 2024. (2 cites)

[Kaushal, 2016] Kaushal H, et al. Optical communication in space: Challenges and mitigation techniques[J]. 2016. (2304 cites)

[Yang, 2025] Yang, et al. Low-complexity carrier phase estimation algorithms for space coherent optical communication[J]. 2025.

---

## 模板效果自评

### 模板S004在本次测试中的表现

**最有用的模板要素：**
1. **"功能"列**：每段写之前看一眼"这段干什么"，方向明确，不跑题
2. **"衔接(接/传)"列**：P6过渡段、P10小结段衔接自然，各1.2.x之间逻辑通顺
3. **P3分类段**："归纳句先行"的要求有效避免了清单体，三个1.2.x都有分类框架
4. **P7文献例举**：4-6句示例展示了"先归纳后展开"的微节奏

**暴露的模板不足：**
1. **P8/P9(缺陷分析)仍然最难写**：从具体文献上升到"结构性不足"的归纳过程，模板只说了"必须从方法论层面"但没给具体的归纳路径。实际写作时P8-P9花了最多时间反复修改
2. **P5/P7边界模糊**：P5(DL方法引入)和P7(文献例举)在内容上有重叠——P5已经提到了Amirabadi的具体结果，P7再展开显得重复。模板假设P5只做方法概述、P7才展开具体论文，但实际写作时难以严格区分
3. **三个1.2.x的同质化风险**：按同一个P1-P10模式写三遍，容易产生机械重复感。模板没有给出如何避免三个子节"长得太像"的指导

**模板未覆盖的需求：**
1. **综述表的设计指导**：P6要求"有综述表"，但表头如何设计、选哪些论文列入、如何排序，模板没有指导
2. **跨节一致性**：三个1.2.x的P10(小结)需要与1.1的P3-P5(挑战)和1.2.4(总结)呼应，模板未给出对齐检查方法
3. **篇幅控制**：三个1.2.x加起来容易超过4000字，模板没有每段的字数上限约束

**量化评估：**

| 指标 | 评分 | 说明 |
|------|------|------|
| 方向明确性 | 8/10 | "功能"列让每段不跑题 |
| 段间衔接 | 7/10 | P6/P10衔接自然，但1.2.x之间缺乏过渡 |
| 文献综述质量 | 7/10 | P3分类有效防清单体，但P5/P7重叠 |
| 创新空白论证 | 6/10 | P8/P9归纳过程仍是最弱环节 |
| 篇幅控制 | 5/10 | 实际写了约4500字，超出目标 |

### 建议的模板改进方向

1. **P8增加"归纳路径"示例**：从N篇论文→共性缺陷→结构性问题 的具体推理步骤
2. **合并P5和P7**：将DL方法引入和文献例举合并为一段，避免内容重叠
3. **增加"防同质化"指导**：三个1.2.x应各有侧重（如Ch2偏理论、Ch3偏实验、Ch4偏算法对比）
4. **增加每段字数上限**：建议P1-P4每段≤80字，P5-P7每段≤120字，P8-P9每段≤100字
5. **增加综述表设计指南**：列出"方法/信道/调制/核心结果"四列的最小表头要求
