# 分章文献清单

> 2026-05-30 | 学位论文v4结构（6章）
> 来源：R004-R007, R012-R016, S006-S010, literature_notes.md
> 上一版38篇严重不足，本版扩展至约80篇
> 说明：一篇论文跨章出现时各算独立条目；Ch6不引用独立文献

---

## Ch1 绪论（25篇）

综述章，需全面覆盖FSO发展、信道建模、估计、均衡/预补偿、载波同步、FPGA实现。

| # | 论文名 | 作者(年份), 期刊 | 引用 | 对应节 | 支撑论点 | 状态 |
|---|--------|-----------------|------|--------|---------|------|
| 1 | Survey on Free Space Optical Communication: A Communication Theory Perspective | Khalighi & Uysal (2014), IEEE COMST | 2378 | 1.1 FSO概述 | FSO通信理论综述标杆，均衡/信道建模/检测全覆盖 | ✅ |
| 2 | Optical communication in space: Challenges and mitigation techniques | Kaushal et al. (2016), JLT | 2304 | 1.1 FSO概述 | 空间光通信挑战与对策全景综述 | ⬚ |
| 3 | 星地相干激光通信大气信道特征及信号处理技术研究 | 张岱 (2018), 国防科技大学硕士 | 8 | 1.2 信道建模 | 星地相干激光通信+大气信道+信号处理，方向高度匹配 | ✅全文 |
| 4 | 大气激光通信数字相干探测关键技术研究 | 李学良 (2018), 中科院长春光机所硕士 | 48 | 1.2 信道建模 | 相干检测+大气激光通信标杆，GG+载波恢复+DL | ⬚ |
| 5 | 星地自由相干光通信系统中信号处理与补偿技术研究 | 闫旭 (2022), 西安电子科技大学博士 | 1 | 1.2 信道建模 | 星地+相干+信号处理+补偿，波前补偿+低复杂度CPE | ⬚ |
| 6 | 空间相干激光通信信道均衡算法研究 | 赵远帆 (2024), 青岛大学硕士 | 1 | 1.3 均衡 | 空间相干激光通信均衡，BP/LSTM DL均衡 | ⬚ |
| 7 | Deep learning for channel estimation in FSO communication system | Amirabadi et al. (2020), Optik | 87 | 1.4 信道估计 | DL信道估计FSO基线，GG湍流，无导频估计接近完美CE | ✅全文 |
| 8 | Symbol Detection and CE for SOC Using NN and Autoencoder | Elfiky & Rezzi (2024), IEEE TMLCN | 16 | 1.4 信道估计 | LEO-GG+NN信道估计+Autoencoder，最接近我们场景 | ✅ |
| 9 | Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics | Paillier et al. (2020), JLT | 35 | 1.5 载波同步 | 星地相干光链路+AO+DPLL端到端模型 | ✅全文 |
| 10 | Carrier recovery for satellite-to-ground coherent laser communication systems | Liu et al. (2023), Optics Communications | 15 | 1.5 载波同步 | VV/BPS在星地相干激光通信中的载波恢复对比 | ⬚ |
| 11 | Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links | Wang et al. (2025), ACP | 0 | 1.5 载波同步 | LEO多普勒实时跟踪FPGA，±8GHz | ✅全文 |
| 12 | Joint Doppler and Phase Noise Compensation for Inter-Satellite Coherent Laser | Zhao et al. (2025), ICCSN | 0 | 1.5 载波同步 | 联合多普勒+相位噪声补偿，QPSK | ✅全文 |
| 13 | 100G FSO field trial with transmitter power adaptability using a LoRa feedback channel | Brandao et al. (2024), JOCN | 7 | 1.6 预补偿 | 100G FSO外场试验+功率预补偿+LoRa反馈 | ✅全文 |
| 14 | Adaptive Channel Coding and Power Control for Practical FSO Under CE Error | Safi et al. (2019), IEEE TVT | 52 | 1.6 预补偿 | 自适应编码+功率控制理论框架，GG中断概率闭式解 | ✅全文 |
| 15 | Satellite-to-ground optical comm under orbital deviations and atmospheric turbulence | Xu et al. (2025), Optics Express | 16 | 1.2 信道建模 | 星地光通信信道建模+指向误差+GG湍流 | ⬚ |
| 16 | Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links | (2025), Int. J. Satellite Comm. | 4 | 1.5 载波同步 | 星地相干光链路DSP算法综述 | ⬚ |
| 17 | Performance improvement of MDM-FSO with DFE | Almogahed et al. (2022), Cogent Engineering | 28 | 1.3 均衡 | DFE-MMSE在FSO中的标杆实现 | ✅子agent |
| 18 | Hybrid STA with FNN/CNN for robust CE in turbulent FSO and Doppler-affected OFDM for LEO | Rustum et al. (2026), IET Communications | 0 | 1.4 信道估计 | LEO-OFDM+DL信道估计+湍流+多普勒联合 | ✅子agent |
| 19 | Digitally mitigating Doppler shift in high-capacity coherent FSO LEO-to-Earth links | Fernandes et al. (2023), JLT | 31 | 1.5 载波同步 | LEO-地面多普勒数字补偿标杆 | ✅ |
| 20 | Digital Pre-Compensation of Doppler Frequency Shift in Coherent Optical Satellite | Almonacil et al. (2020), ECOC | 6 | 1.5 载波同步 | 发射端数字预补偿多普勒±10GHz | ⬚ |
| 21 | Free space optical turbulent channel estimation based on CNN+BiLSTM | Mohammed et al. (2026), J. Optical Communications | 0 | 1.4 信道估计 | CNN+BiLSTM GG湍流信道估计，对比LS/LMMSE/EKF | ⬚ |
| 22 | Robust high-capacity FSO using OAM+DNFIS+DCNN | Ahmad et al. (2026), Scientific Reports | 0 | 1.3 均衡 | DNFIS+DCNN DL均衡vs DFE，BER降低55% | ✅全文 |
| 23 | Enhanced frame synchronization and carrier recovery in coherent FSO communication | Wang et al. (2024), Optics Express | 2 | 1.5 载波同步 | FSO湍流帧同步+载波恢复联合 | ⬚ |
| 24 | 低轨卫星通信系统的时频联合同步算法 | (2026), 中文 | 0 | 1.5 载波同步 | LEO时频联合同步最新方案 | ❌ |
| 25 | 多普勒效应对星间激光通信的影响及对策 | 朱勇等 (2003), 中文 | 6 | 1.5 载波同步 | 多普勒对激光通信影响的经典中文文献 | ❌ |

---

## Ch2 星地激光通信系统与信道模型（10篇）

基础章：GG模型、相干检测原理、链路预算、大气衰减。

| # | 论文名 | 作者(年份), 期刊 | 引用 | 对应节 | 支撑论点 | 状态 |
|---|--------|-----------------|------|--------|---------|------|
| 1 | Gamma-Gamma大气湍流下超奈奎斯特光通信系统性能 | 曹明华等 (2020), 中国激光 | 50 | 2.3 GG模型 | GG湍流模型中文高引文献，GG三档参数(α,β,Cn²)权威来源 | ✅ |
| 2 | Gamma-Gamma大气湍流下相干光通信分集接收技术 | 孙晶等 (2018), 光学学报 | 27 | 2.3 GG模型 | 相干检测+GG信道系统参数，中文核心 | ✅ |
| 3 | GG大气湍流下零判决门限差分探测FSO系统误码率 | 李晓燕等 (2017) | 17 | 2.3 GG模型 | GG湍流BER分析 | ❌ |
| 4 | Gamma-gamma大气湍流下自由空间光通信的性能 | 韩立强等 (2011) | 70 | 2.3 GG模型 | GG湍流模型经典中文高引文献 | ❌ |
| 5 | Satellite-to-ground optical comm under orbital deviations and atmospheric turbulence | Xu et al. (2025), Optics Express | 16 | 2.4 链路预算 | 星地链路GG+指向误差建模 | ⬚ |
| 6 | Optical Downlink Modeling for LEO/MEO under turbulence | Czerwinski et al. (2025), arXiv | 0 | 2.4 链路预算 | LEO/MEO光学下行链路预算建模 | ⬚ |
| 7 | Coherent Laser Ground-to-Satellite with atmospheric turbulence | Stotts et al. (2023) | 0 | 2.3 相干检测 | 星地相干激光通信大气湍流影响 | ❌ |
| 8 | Survey on Free Space Optical Communication: A Communication Theory Perspective | Khalighi & Uysal (2014), IEEE COMST | 2378 | 2.1 系统概述 | FSO系统模型+信道模型综述 | ✅ |
| 9 | 大气激光通信中多光束传输性能分析和信道建模 | 马东堂等 (2004) | 94 | 2.3 GG模型 | FSO信道建模经典中文文献 | ❌ |
| 10 | 相干激光通信中零差相干接收及传输信道研究 | 周海军 (2020) | 2 | 2.2 相干检测 | 相干检测信道建模中文研究 | ❌ |

---

## Ch3 大气湍流信道估计技术（25篇）

主体章之一：估计方法(LS/MMSE/Kalman/DL)、级联影响+预补偿失败分析。

| # | 论文名 | 作者(年份), 期刊 | 引用 | 对应节 | 支撑论点 | 状态 |
|---|--------|-----------------|------|--------|---------|------|
| 1 | Deep learning for channel estimation in FSO communication system | Amirabadi et al. (2020), Optik | 87 | 3.2 DL方法 | DL无导频信道估计FSO标杆，弱/中/强湍流三档参数 | ✅全文 |
| 2 | Symbol Detection and CE for SOC Using NN and Autoencoder | Elfiky & Rezzi (2024), IEEE TMLCN | 16 | 3.2 DL方法 | GG+LEO下NN信道估计，最接近我们场景 | ✅ |
| 3 | Hybrid STA with FNN/CNN for robust CE in turbulent FSO and Doppler-affected OFDM for LEO | Rustum et al. (2026), IET Communications | 0 | 3.2 DL方法 | STA+DL两阶段LEO-OFDM信道估计，NMSE=3×10⁻³ | ✅子agent |
| 4 | Free space optical turbulent channel estimation based on CNN+BiLSTM | Mohammed et al. (2026), J. Optical Communications | 0 | 3.2 DL方法 | CNN+BiLSTM GG湍流信道估计，优于LS/LMMSE/EKF | ⬚ |
| 5 | Meta-learning for estimating atmospheric turbulence in satellite OWC | Zhou et al. (2024), IEEE IoT-J | 3 | 3.2 DL方法 | 元学习信道估计，小样本适应，MSE比MMSE低35% | ⬚ |
| 6 | FSO channel estimation for OOK with APD receiver over atmospheric turbulence and pointing errors | Dabiri et al. (2017), Optics Communications | 64 | 3.1 传统方法 | 经典FSO信道估计，OOK+APD+湍流+指向误差 | ⬚ |
| 7 | Joint estimation model for FSO channel parameters based on CNNs | Chen et al. (2024), Applied Optics | 3 | 3.2 DL方法 | CNN联合估计检测噪声+湍流参数，含Cn² | ⬚ |
| 8 | SWALNet: sparse wavelength aware learning for robust FSO channel estimation | Selvaraj et al. (2025), Scientific Reports | 0 | 3.2 DL方法 | GG+OFDM+波长感知，MSE=0.0037 | ❌ |
| 9 | Moment-based estimation for gamma-gamma fading parameters in FSO links | Kim & Yoon (2025), IEEE | 12 | 3.1 传统方法 | 矩估计GG参数(α,β) | ⬚ |
| 10 | Phase and Channel Estimation for Phase-Asynchronous MDM-MIMO FSO | (2024), JLT | 5 | 3.1 传统方法 | 唯一相干体制FSO信道估计方法论文 | ⬚ |
| 11 | 基于DNN信道估计的自适应概率整形FSO系统 | 武盈等 (2026), 空间电子技术 | - | 3.2 DL方法 | 中文唯一直接做DNN+FSO信道估计 | ❌ |
| 12 | 探测噪声与湍流信道参数联合估计方法研究 | 高悦 (2023) | - | 3.1 传统方法 | 中文信道参数联合估计研究 | ❌ |
| 13 | FSO channel estimation based on DL algorithms (DNN/CNN/RNN对比) | Ndiaye et al. (2023) | 4 | 3.2 DL方法 | DNN/CNN/RNN对比LS/MMSE | ❌ |
| 14 | Robust CE for OWC using Neural Network | Luan & Thompson (2025) | 4 | 3.2 DL方法 | DL-CE泛化性边界（SNR范围外性能退化13×） | ⬚ |
| 15 | 100G FSO field trial with transmitter power adaptability using a LoRa feedback channel | Brandao et al. (2024), JOCN | 7 | 3.4 预补偿分析 | 外场验证功率预补偿+LoRa反馈，可靠性+7% | ✅全文 |
| 16 | Adaptive Channel Coding and Power Control for Practical FSO Under CE Error | Safi et al. (2019), IEEE TVT | 52 | 3.4 预补偿分析 | 自适应功率+编码联合理论框架，GG中断概率闭式解 | ✅全文 |
| 17 | Reciprocity-Driven Power Adaptation (EDFA APC) | Correia et al. (2026), JLT | - | 3.4 预补偿分析 | EDFA APC自适应光功率预补偿实验验证 | ✅ |
| 18 | Adaptive Rate/Power Control with ML Channel Prediction for FSO Satellite | Nguyen et al. (2024), IEEE TAES | 5 | 3.4 预补偿分析 | 卫星FSO自适应功率+ML信道预测解决延迟问题 | ✅ |
| 19 | Pre-compensation Phase for GEO Feeder Uplinks | Lognone et al. (2023), SPIE | - | 3.4 预补偿分析 | GEO上行预补偿相位优化，链路裕度+15dB | ⬚ |
| 20 | Simulated 1000km LEO using 1.8km OWC | Cheng et al. (2025) | 10 | 3.4 预补偿分析 | 地面短距模拟LEO长距缩比方法论 | ⬚ |
| 21 | Beam Power Optimization FSO Using RL+SLM | Seifi & LoPresti (2026) | - | 3.4 预补偿分析 | TD3+SLM优化FSO光束功率，面向LEO | ⬚ |
| 22 | MDM-FSO improvement through various atmospheric conditions with DFE | Almogahed et al. (2022), Cogent Engineering | 28 | 3.3 级联影响 | DFE-MMSE在FSO中BER改善6-26个数量级 | ✅子agent |
| 23 | Deep learning-based pilot-free channel estimation of UAV-FSO system using VAE | Tumma & Miriyala (2025), ICT Express | 1 | 3.2 DL方法 | VAE无导频信道估计(IM/DD) | ❌ |
| 24 | 深度学习辅助的无线光通信联合信道估计与检测技术研究 | 周陆霞 (2025) | - | 3.2 DL方法 | 中文DL信道估计+检测联合研究 | ❌ |
| 25 | Clustering-assisted channel estimation for FSO satellite communication | Rustum et al. (2026), Elsevier | 2 | 3.2 DL方法 | FSO LEO卫星信道估计，聚类辅助 | ⬚ |

---

## Ch4 低轨星地载波同步算法（18篇）

主体章之一：FOE、CPR(VV/BPS/Pilot)、DPLL、多普勒、湍流自适应。

| # | 论文名 | 作者(年份), 期刊 | 引用 | 对应节 | 支撑论点 | 状态 |
|---|--------|-----------------|------|--------|---------|------|
| 1 | Carrier recovery for satellite-to-ground coherent laser communication systems (双反馈+VV级联) | Liu et al. (2023), Optics Communications | 15 | 4.2 CPR | VV/BPS在星地链路载波恢复对比，双反馈环MSE改善6dB | ⬚ |
| 2 | Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and DPLL | Paillier et al. (2020), JLT | 35 | 4.3 DPLL | 星地相干+DPLL+AO，FOE捕获1.4ms，湍流BER惩罚2.3dB | ✅全文 |
| 3 | Joint Doppler and Phase Noise Compensation for Inter-Satellite Coherent Laser | Zhao et al. (2025), ICCSN | 0 | 4.1 FOE | 联合多普勒+相位噪声，QPSK，±8GHz，<0.5dB损失 | ✅全文 |
| 4 | Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links | Wang et al. (2025), ACP | 0 | 4.5 FPGA先例 | FPGA LEO多普勒实时跟踪，±8GHz，FPGA资源表完整 | ✅全文 |
| 5 | Enhanced frame synchronization and carrier recovery in coherent FSO communication | Wang et al. (2024), Optics Express | 2 | 4.2 CPR | FSO湍流帧同步+载波恢复联合 | ⬚ |
| 6 | A noise-tolerant carrier phase recovery method for inter-satellite coherent optical | Hu et al. (2025), Electronics | 3 | 4.2 CPR | 星间噪声容忍型CPR，二阶反馈+前馈混合 | ⬚ |
| 7 | A low-complexity joint compensation scheme of carrier recovery for coherent FSO | Tang et al. (2023), Photonics | 7 | 4.1 FOE | 联合载波恢复(频偏+相位)低复杂度方案 | ⬚ |
| 8 | Digitally mitigating Doppler shift in high-capacity coherent FSO LEO-to-Earth links | Fernandes et al. (2023), JLT | 31 | 4.1 FOE | LEO-地面多普勒数字补偿标杆 | ✅ |
| 9 | Low-complexity carrier phase estimation algorithms for space coherent optical communication | Yang et al. (2025), SPIE HPCCE | 0 | 4.2 CPR | 空间相干光VV vs BPS直接对比，抗湍流性能好 | ⬚ |
| 10 | Recurrent neural network enabled adaptive carrier phase recovery | Shi et al. (2025), SPIE | 0 | 4.2 DL-CPR | RNN自适应CPR，DL-based CPR最新进展 | ⬚ |
| 11 | Transparent Carrier Phase Recovery Based on ANN | Blatter et al. (2025) | 0 | 4.2 DL-CPR | ANN载波相位恢复，FSO湍流场景空白 | ❌ |
| 12 | Digital pre-compensation of Doppler frequency shift in coherent optical satellite communications | Almonacil et al. (2020), ECOC | 6 | 4.1 FOE | 发射端数字预补偿多普勒±10GHz | ⬚ |
| 13 | Carrier-phase recovery for coherent optical systems: Algorithms, challenges and... | Neves et al. (2023) | 39 | 4.2 CPR综述 | CPR算法综述，VV/BPS/Pilot全覆盖 | ⬚ |
| 14 | 相干光通信载波相位恢复算法研究 | 徐文婧等 (2021) | 10 | 4.2 CPR | 中文CPR综述 | ❌ |
| 15 | 基于数字相位恢复算法的QPSK自由空间相干光通信系统 | 管海军等 (2019) | 8 | 4.2 CPR | QPSK+FSO相干+数字相位恢复直接参考 | ❌ |
| 16 | 空间相干光通信中基于DSP的多普勒频移补偿技术 | 向劲松等 (2011) | 3 | 4.1 FOE | 中文多普勒频移补偿经典文献 | ❌ |
| 17 | Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication | Wang et al. (2023), IEEE Photonics J. | 8 | 4.1 FOE | 空间分集FSO载波频偏估计 | ⬚ |
| 18 | Real-time FPGA prototyping of Doppler frequency shift compensation using DSP-assisted AFC | (2024), Optics Letters | 1 | 4.5 FPGA先例 | FPGA AFC多普勒补偿±8GHz | ⬚ |

---

## Ch5 接收端信号处理链FPGA设计与实现（9篇）

半章：FPGA实现、DSP链、资源优化。

| # | 论文名 | 作者(年份), 期刊 | 引用 | 对应节 | 支撑论点 | 状态 |
|---|--------|-----------------|------|--------|---------|------|
| 1 | Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links | Wang et al. (2025), ACP | 0 | 5.2 FPGA架构 | FPGA资源表完整(LUT 49%/BRAM 91%/DSP 20%)，AFC闭环 | ✅全文 |
| 2 | Real-time FPGA prototyping of 15GBaud SP-16QAM coherent receiver with clock recovery and equalization | (2022), Optics Express | 8 | 5.3 定时恢复+FPGA | SP-16QAM全链路FPGA先例，含时钟恢复+均衡 | ⬚ |
| 3 | Real-time 15GBaud QPSK and 16QAM Flexible Coherent Optical Receiver on Single FPGA | (2023), ICCT | 5 | 5.2 FPGA架构 | SP-QPSK/16QAM灵活接收单FPGA实现 | ⬚ |
| 4 | Real-time low-complexity diversity combining for free space coherent optical over turbulence | (2023), Optics Express | 4 | 5.4 湍流处理 | FSO湍流分集合并FPGA实时实现 | ⬚ |
| 5 | Low-Complexity FPGA Implementation of 106.24Gbps DP-QPSK Coherent Optical Receiver | (2023), JLT | 15 | 5.2 FPGA架构 | DP-QPSK全链路FPGA资源参考 | ⬚ |
| 6 | A Low-latency Carrier Phase Recovery Hardware for Coherent Optical Communication | (2022), ISCAS | 1 | 5.3 CPR实现 | CPR硬件低延迟实现 | ⬚ |
| 7 | Real-Time Demonstration of Digital Interpolator-Free Clock Recovery for FPGA-Based PM-QPSK | (2025), JLT | 3 | 5.3 定时恢复+FPGA | 插值器无关时钟恢复FPGA | ⬚ |
| 8 | All-Digital Timing Recovery for FSO Signals With Large Dynamic Range | (2019), IEEE Photonics J. | 12 | 5.3 定时恢复+FPGA | FSO专用定时恢复FPGA实现 | ⬚ |
| 9 | Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links | (2025), Int. J. Satellite Comm. | 4 | 5.1 DSP架构综述 | 星地相干光链路DSP全算法综述，架构设计参考 | ⬚ |

---

## 汇总统计

| 章 | 目标篇数 | 实际篇数 | ✅全文 | ⬚摘要 | ❌未获取 | 全文率 |
|---|---------|---------|-------|-------|---------|--------|
| Ch1 绪论 | 20-25 | **25** | 7 | 12 | 6 | 28% |
| Ch2 系统与信道模型 | 8-10 | **10** | 3 | 2 | 5 | 30% |
| Ch3 信道估计+级联 | 20-25 | **25** | 9 | 8 | 8 | 36% |
| Ch4 载波同步 | 15-20 | **18** | 4 | 10 | 4 | 22% |
| Ch5 FPGA | 8-10 | **9** | 1 | 8 | 0 | 11% |
| **合计** | **~80** | **87** | **23** | **45** | **19** | **26%** |

去重后独立论文约72篇（Ch1与Ch2/3/4有约15篇跨章重复）。

### 状态说明

- ✅ 全文精读或已下载PDF+转markdown（23篇, 26%）：有量化数据可直接引用
- ⬚ 有abstract/检索摘要（45篇, 52%）：已知核心结论但缺精确参数
- ❌ 仅检索结果引用（19篇, 22%）：需获取全文确认

### S016 补充下载（2026-05-30 blit）

以下7篇论文已通过 blit 从 IEEE/CNKI 下载并转换为 markdown：

| 论文 | 来源 | 文件 |
|------|------|------|
| Nguyen 2024 TAES | IEEE | `papers/downloads/2026-05-30/10535712.pdf` + `.md` |
| Elfiky 2024 TMLCN | IEEE | `papers/downloads/2026-05-30/10373105.pdf` + `.md` |
| Correia 2026 JLT | IEEE | `papers/downloads/2026-05-30/11278671.pdf` + `.md` |
| Fernandes 2023 JLT | IEEE | `papers/downloads/2026-05-30/10138358.pdf` + `.md` |
| 曹明华 2020 中国激光 | CNKI | `papers/downloads/2026-05-30/Gamma-Gamma大气湍流下超奈奎斯特光通信系统性能_曹明华.pdf` + `.md` |
| 孙晶 2018 光学学报 | CNKI | `papers/downloads/2026-05-30/Gamma-Gamma大气湍流下相干光通信分集接收技术研究_孙晶.pdf` + `.md` |
| 佟欣 2020 光通信技术 | CNKI | `papers/downloads/2026-05-30/空间激光通信中变步长CMA-LMS均衡算法_佟欣.pdf` + `.md` |

---

## 优先获取TOP10

以下论文对开题报告写作最关键，建议优先下载获取全文：

| 优先级 | 论文 | DOI/来源 | 理由 |
|--------|------|---------|------|
| **P1** | Liu et al. 2023, VV/BPS星地载波恢复对比 | 10.1016/j.optcom.2023.129312 | Ch4核心对照，VV/BPS精确差距数据，Elsevier付费墙未获取 |
| **P2** | Nguyen et al. 2024, FSO卫星自适应功率控制 | 10.1109/TAES.2024.3403809 | Ch3预补偿唯一直接实证，需确认传统方法增益受限程度 | ✅已下载 |
| **P3** | 曹明华 2020, GG+FTN中文高引 | CNKI | GG三档参数(α,β,Cn²)中文权威来源，参数溯源核心缺口 | ✅已下载 |
| **P4** | 孙晶 2018, 相干+GG分集中文核心 | CNKI | 相干检测GG信道系统参数中文文献 | ✅已下载 |
| **P5** | Elfiky 2024, TMLCN NN CE+LEO | IEEE TMLCN | Ch2最强匹配：GG+NN CE+LEO，需确认DL vs MMSE对比数据 | ✅已下载 |
| **P6** | Correia 2026, JLT EDFA APC预补偿 | 10.1109/JLT.2025.3640945 | 功率预补偿最新实验验证 | ✅已下载 |
| **P7** | Paillier 2020, JLT星地相干AO+DPLL | arXiv:1911.11851 | Ch4核心参考，已全文精读但需官方引用格式 |
| **P8** | Review DSP for Coherent Optical Satellite Links 2025 | 10.1002/sat.1553 | Ch4/Ch5写作结构参考，星地DSP全链路综述 |
| **P9** | 佟欣 2020, CMA-LMS空间激光均衡 | CNKI | CMA在空间激光通信中的唯一直接应用，Ch3参数参考 | ✅已下载 |
| **P10** | Fernandes et al. 2023, JLT LEO多普勒数字补偿 | 10.1109/JLT.2023.3322697 | LEO多普勒数字补偿标杆(31引)，Ch4对比参考 | ✅已下载 |
