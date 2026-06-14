# [R002] 可扩展论文方向扫描汇总（新策略）

> 2026-06-10 | 关联：S002, R001
> 策略：从"找空白"转向"找可扩展已有工作" — 3 个搜索 agent 并行执行

## 调研方法

派 3 个 agent 并行搜索 2024-2026 论文：
- **Agent A**：相干 FSO 信号处理论文（载波同步/信道估计/相位恢复）
- **Agent B**：光纤相干检测成熟方法 → FSO 湍流迁移
- **Agent C**：IM/DD FSO 成熟结果 → 相干检测扩展

每个 agent 目标 7-8 个方向，共产出 24 个原始方向，去重后 22 个独立方向。

## 去重与合并说明

| 重复方向 | 来源 | 合并为 |
|---------|------|--------|
| 自适应KF | A1 + B1 | 合并（两agent找到不同论文但同一方向） |
| 多孔径分集 | A4 + C1 + A8(CV-DD-LMS) | 拆为2个：传统MRC vs CV-DD-LMS联合 |
| Doppler+湍流 | A3 + B6 | 拆为2个：ODPLL Z变换 vs Doppler预补偿+湍流后补偿 |
| 编码辅助 | B4 + C5 | 合并（不同侧重但同一方向） |

## 22 个候选方向（按主题分组）

---

### A 组：载波同步改进（6 个方向）

#### A1. 自适应/突发感知 Kalman 滤波器

- **来源**：Agent A 方向1 + Agent B 方向1
- **已有工作**：Zhang 2023 (IEEE Photonics Journal) 自适应 KF + 盲均衡用于无线光相干通信；Peng 2023 FIR-EKF；Lian 2023 AR辅助EKF处理 1/f 噪声；Liu 2025 KF 自适应控制偏振+相位恢复
- **关键论文**：
  - Zhang, Tan, Ma (2023), "Flexible Phase Synchronization for Wireless Optical Coherent Communication System With Adaptive Fractionally-Spaced Blind Equalization Combined With Adaptive Kalman Filter", IEEE Photonics Journal, DOI: 10.1109/JPHOT.2023.3328423
  - Liu, Ji, Tan (2025), "The Optimization Scheme Based on Kalman Filter for Self-Homodyne Coherent Detection System Under Fast RSOP", JLT, DOI: 10.1109/JLT.2025.3580733
- **已有成果**：自适应 KF 处理不同激光线宽和湍流闪烁，MSE/SER 改善 1-2 dB
- **限制**：仅 OOK/BPSK，未考虑 LEO 大 Doppler，Q 矩阵自回归修正范围有限
- **扩展方案**：(1) Q 矩阵从固定值改为 GG 湍流自适应（基于接收功率估计闪烁状态）(2) IMM 框架维护多并行 EKF (3) 突发检测器触发 Q 切换
- **可行性**：HIGH（已有 KF 基线，改造量小）
- **风险**：突发相位跳变可能导致失锁，需重新捕获机制

#### A2. ANN/RNN 自适应载波相位恢复

- **来源**：Agent B 方向2
- **关键论文**：
  - Blatter, Xu, Kaufmann (2025), "Transparent Carrier Phase Recovery Based on an Artificial Neural Network", IEEE PTL, DOI: 10.1109/LPT.2025.3582338
  - Shi, Sun, Chen (2025), "RNN Enabled Adaptive Carrier Phase Recovery for High-Speed Coherent Optical Transmission", SPIE
- **已有成果**：ANN 实现调制格式透明的载波恢复，低 SNR 优于 2S-BPS；RNN 处理 NLPN 和 EEPN
- **扩展方案**：(1) 用 GG 湍流模型生成训练数据（突发相位跳变）(2) 输入特征增加 RSSI (3) 元学习框架适应不同湍流条件
- **可行性**：HIGH（已有 BPS 基线可对比）
- **风险**：RNN 对突发事件响应可能滞后；泛化能力需大量验证

#### A3. 频域导频音联合跟踪

- **来源**：Agent B 方向8
- **关键论文**：
  - Yang, Zhuo, Tang (2026), "Polarization-Fading-Free Phase Recovery and Robust RSOP Tracking Using Frequency-Domain Pilot Tones", IEEE Comm. Letters, DOI: 10.1109/LCOMM.2026.3651445
  - Zhou, Zuo, Yang (2026), "Vibration Detection Based on DSP Frame Pilot Symbols Using Integrated Coherent Receivers", Optics Letters, DOI: 10.1364/ol.596189
- **已有成果**：频域导频音联合 FOE+CPE+RSOP 跟踪，无额外开销
- **扩展方案**：(1) FSO 系统插入频域导频音 (2) 导频功率随湍流强度自适应 (3) 导频+DL 混合
- **可行性**：HIGH（2026年 IEEE CL 论文，技术成熟度高）
- **风险**：深衰落时导频本身受损；功率分配需优化

#### A4. 编码辅助迭代载波恢复

- **来源**：Agent B 方向4 + Agent C 方向5
- **关键论文**：
  - Chen, Ding, Zhang (2025), "Error-Threshold Based Joint Phase Estimation and Decoding Method for Non-Pilot-Aided Systems", FCN 2025, DOI: 10.1109/FCN66513.2025.11296777
- **已有成果**：加权归一化校验满足概率的联合载波恢复与迭代解码，低 SNR 改善显著
- **扩展方案**：(1) Turbo 同步：LDPC 外信息反馈相位估计器 (2) 深衰落时额外迭代 (3) 针对突发错误设计交织器
- **可行性**：MODERATE（迭代复杂度高）
- **风险**：FSO 相位噪声带宽远大于光纤，迭代收敛性不确定

#### A5. FDE 内嵌载波相位估计

- **来源**：Agent B 方向7
- **关键论文**：
  - Hu, Gong, Li (2026), "Frequency-Domain Equalizer With Embedded Carrier Phase Estimation in Coherent Optical Receivers", IEEE PTL, DOI: 10.1109/LPT.2025.3634335
- **已有成果**：FDE 内嵌双级 DD-CPE，DD-LMS 联合优化，无额外频偏估计开销
- **扩展方案**：(1) 湍流感知 FDE，相位跳变建模为额外扰动项 (2) 分块处理 (3) 步长与信号功率方差挂钩
- **可行性**：MODERATE（需重新设计目标函数）
- **风险**：非平稳信道下 DD-LMS 收敛困难；深衰落时判决导向失效

#### A6. TTQP 并行频偏估计

- **来源**：Agent A 方向2
- **关键论文**：
  - Zhang, Wang, Liu, Ding (2024), "Low Complexity Parallel Carrier Frequency Offset Estimation Based on Time-Tagged QPSK Partitioning for Coherent FSO", Photonics, DOI: 10.3390/photonics11090885
- **已有成果**：TTQP 并行频偏估计，低复杂度，支持 PM-16QAM
- **扩展方案**：(1) 应用于 LEO 下行大多普勒动态范围 (2) 与 M-th power 算法做性能-复杂度对比 (3) 级联粗/细估计
- **可行性**：HIGH（算法清晰）
- **风险**：多普勒动态范围远大于论文场景

---

### B 组：Doppler + 湍流联合处理（2 个方向）

#### B1. ODPLL Z 变换多普勒-湍流联合建模

- **来源**：Agent A 方向3
- **关键论文**：
  - Pech, Destic, Dion (2025), "Z-Transform Model of a Coherent Receiver for Satellite-to-Ground Laser Links Under High Doppler Rates", IEEE ICSOS 2025, DOI: 10.1109/ICSOS66026.2025.11443174
- **已有成果**：混合光-数字锁相环 Z 变换模型，LEO 下行大多普勒补偿，考虑系统延迟
- **限制**：仅建模多普勒，未联合建模 GG 湍流
- **扩展方案**：在 Z 变换模型中加入 GG 湍流影响，分析联合效应下环路锁定性能和 BER
- **可行性**：HIGH（直接对接"星地湍流信道"主题）
- **风险**：Z 变换建模需控制理论基础

#### B2. Doppler 预补偿 + 湍流后补偿分离架构

- **来源**：Agent B 方向6 + Agent A 方向3 补充
- **关键论文**：
  - Hu, Lin, Wu (2025), "A Noise-Tolerant Carrier Phase Recovery Method for Inter-Satellite Coherent Optical Communications", Electronics, DOI: 10.3390/electronics14020265
  - Du, Yu, Wang (2025), "Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems", IEEE PTL, DOI: 10.1109/LPT.2024.3523478
- **已有成果**：噪声容忍载波恢复方法（星间链路），非数据辅助 ML 联合估计
- **扩展方案**：轨道预报 Doppler 预补偿 → 残余频偏 + 湍流相位噪声由 DSP 处理
- **可行性**：HIGH
- **风险**：预补偿精度依赖轨道预报精度

---

### C 组：多天线/分集（3 个方向）

#### C1. 多孔径 MRC 分集接收仿真

- **来源**：Agent A 方向4 + Agent C 方向1
- **关键论文**：
  - Fardoost et al. (2026), "Turbulence-Resilient Coherent Receiver Array on CMOS-Compatible Silicon Photonics for FSO", Nanophotonics, DOI: 10.1002/nap2.70021
  - Liu, Dang, Fu (2025), "Array detector systems for satellite-to-ground atmospheric coherent laser communications", Optics Express
  - Xu et al. (2023), "Real-time low-complexity diversity combining algorithm for free space coherent optical communication systems", Optics Express, DOI: 10.1364/oe.505931
- **已有成果**：4x4 相干接收阵列 MRC，BPSK 下 BER 从 1E-2 降至 1E-15；CV-DD-LMS 联合合并+CPR 的 FPGA 实现
- **限制**：仅 BPSK，未考虑通道相关性，未覆盖不同湍流强度
- **扩展方案**：(1) QPSK 相干检测 + GG 湍流 + 多孔径 MRC/EGC/SC 对比 (2) 推导合并后 SNR 分布闭合式 (3) 相位估计误差对 MRC 性能影响
- **可行性**：MODERATE-HIGH（需扩展仿真框架但算法成熟）
- **风险**：通道相关性建模准确性

#### C2. 双偏振 FSO 偏振跟踪

- **来源**：Agent B 方向5
- **关键论文**：
  - Nasrollahzadeh, Kumar, Bi (2025), "Dual-Polarization Self-Coherent Transceivers for FSO Communications in the Presence of Atmospheric Turbulence", IEEE Access, DOI: 10.1109/ACCESS.2025.3535789
  - Liu, Wissing, Movaghar (2025), "Dual-Polarization Optical Costas Loop for DSP-Free Homodyne Short-Reach Links", JLT, DOI: 10.1109/JLT.2025.3533422
- **已有成果**：直接研究 FSO+湍流场景的双偏振自相干方案；DSP-Free 光学 Costas 环
- **扩展方案**：(1) QPSK 相干检测 + GG 湍流 + 双偏振 (2) 湍流感知偏振跟踪 (3) 联合偏振-相位恢复
- **可行性**：HIGH（论文已在 FSO 场景验证）
- **风险**：偏振旋转速率可能超过光纤场景

#### C3. 联合多维一体化 DSP

- **来源**：Agent B 方向3
- **关键论文**：
  - Yang, Zhuo, Tang (2026), 同 A3 的第一篇
  - Gong, Shi, Hu (2024), "Coherent Optical Transmitter IQ Imbalance Mitigation with Embedded Carrier Phase and Frequency Offset Estimation", Optics Express, DOI: 10.1364/oe.514308
- **已有成果**：4x4 实值均衡器内嵌相位估计器，DD-LMS 联合优化 IQ 不平衡+频偏+相位
- **扩展方案**：FSO 系统中联合偏振+频偏+相位估计，步长与湍流强度挂钩
- **可行性**：MODERATE（联合优化在非平稳信道中收敛性未验证）
- **风险**：突发深衰落导致系数发散

---

### D 组：调制/编码策略（3 个方向）

#### D1. 自适应调制 BPSK/QPSK/16-QAM

- **来源**：Agent C 方向3
- **关键论文**：
  - Chen et al. (2024), "All-in-One BPSK/QPSK Switchable Transmission and Reception for Adaptive FSO Links", Photonics
  - Mouhammad et al. (2026), "Review on Modulation Formats and Channel Coding in FSO", TechRxiv
- **已有成果**：BPSK/QPSK 切换实验验证；自适应 OOK/PPM/PAM-4 阈值策略
- **扩展方案**：(1) 三档切换 BPSK→QPSK→16-QAM (2) 每档匹配最优载波恢复 (3) 推导平均频谱效率闭合式
- **可行性**：HIGH（common.py 已有 QPSK+16QAM+三种载波恢复）
- **风险**：调制切换瞬间同步保持；之前否决过类似方向（循环依赖风险）

#### D2. 概率整形 PS+残余载波调制 RCM

- **来源**：Agent A 方向5
- **关键论文**：
  - Deng et al. (2026), "Probabilistic Shaping and Residual Carrier Modulation for FSO Turbulent Channels", IEEE PTL, DOI: 10.1109/LPT.2025.3647750
- **已有成果**：PS+RCM 混合方案，残余载波实现无导频相位恢复，PS 抑制闪烁
- **扩展方案**：(1) 移植到 LEO 场景 (2) 不同湍流强度下最优整形深度 (3) 均匀 QPSK vs PS-QPSK/PS-16QAM
- **可行性**：MODERATE（需新增 PS 模块）
- **风险**：LEO 场景下残余载波 SNR 不足；PS 增加实现复杂度

#### D3. FEC/LDPC 编码增益在相干 FSO 中

- **来源**：Agent C 方向5
- **关键论文**：
  - AlQahtani & El-Nahal (2025), "WDM-PON FSO System Utilizing LDPC Decoding", Photonics
  - Taricco (2025), "HARQ Performance Limits for FSO Systems", Entropy
- **已有成果**：LDPC 在 IM/DD FSO 中 5-8 dB 增益；HARQ 吞吐量-延迟权衡
- **扩展方案**：(1) 集成 LDPC 到 common.py (2) 对比有/无相位估计误差时编码增益 (3) 交织深度与湍流块长度匹配
- **可行性**：MODERATE（需集成外部 LDPC 库）
- **风险**：编码增益分析本身不够新颖

---

### E 组：性能分析与建模（3 个方向）

#### E1. 湍流时间相关性对载波跟踪的影响

- **来源**：Agent C 方向7（推荐度最高）
- **关键论文**：
  - Sun & Noh (2025), "End-to-End Performance Analysis of CCSDS O3K Optical Communication System Under Atmospheric Turbulence", Aerospace
  - Ahmad et al. (2026), "Robust high-capacity FSO using OAM-based structured light and intelligent adaptive signal processing", Scientific Reports
- **核心洞察**：**IM/DD 完全不涉及载波跟踪，这是相干检测独有的问题空间**
- **已有成果**：湍流相干时间 τ_c ≈ √(λ·z)/(2·v_wind)，块衰落模型
- **扩展方案**：(1) 连续时间衰落模型 h(t) (2) h(t) 导数对载波跟踪的影响 (3) KF/DPLL 在不同衰落速率下跟踪误差方差 (4) "衰落速率-跟踪误差-BER"定量关系 (5) 不同湍流条件下最优环路带宽设计准则
- **可行性**：HIGH（common.py 已有 KF/DPLL，直接扩展）
- **风险**：连续时间模型参数需气象数据；实验验证困难

#### E2. 性能界（outage probability / ergodic capacity）

- **来源**：Agent C 方向4
- **关键论文**：
  - Chen et al. (2024), "Performance of free-space optical coherent detection systems under imprecise channels", Optical Engineering
  - Shinde (2026), "Adaptive transmit power control for FSO under gamma-gamma turbulence"
  - Phuchortham & Sabit (2026), "A Review of the Structure of Free-Space Optical Channel Models", Photonics
- **已有成果**：IM/DD GG 信道 outage/capacity 闭合式（Meijer-G 函数），几乎全部基于 h²·γ̄
- **扩展方案**：(1) 推导相干检测 h·γ̄ 的 outage/capacity (2) QPSK 平均 BER 闭合式 (3) 对比 IM/DD vs 相干性能界差异
- **可行性**：HIGH（纯数学推导）
- **风险**：Meijer-G 函数数值计算可能需近似；heterodyne vs homodyne 差异需仔细区分

#### E3. 卫星-地面相干 FSO 链路预算分析

- **来源**：Agent C 方向6
- **关键论文**：
  - Czerwiński (2025), "Atmospheric modeling of FSO transmission: satellite downlinks and horizontal channels"
  - Valjus, Wolf, Poliak (2025), "Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links", Int. J. Satellite Comm., DOI: 10.1002/sat.1553
  - Terrasanta et al. (2025), "Photonic Integrated Circuits for Optical Satellite Links"
- **已有成果**：完整大气传播模型，但基于 IM/DD 接收机
- **扩展方案**：(1) 完整相干 FSO 链路预算模型 (2) 对比 IM/DD vs 相干链路余量 (3) 载波恢复误差对链路余量影响
- **可行性**：HIGH
- **风险**：偏工程，学术贡献度可能不足

---

### F 组：新技术引入（3 个方向）

#### F1. 深度学习信道估计

- **来源**：Agent A 方向7
- **关键论文**：
  - Zhu, Zheng (2025), "Research on FSO channel estimation technology based on machine learning", SPIE, DOI: 10.1117/12.3071211
  - Selvaraj et al. (2025), "A sparse wavelength aware learning framework for robust FSO channel estimation", Scientific Reports
- **已有成果**：AT-CNN-BiLSTM R²=95%；SWALNet MSE=0.0037, BER=1.24e-3
- **扩展方案**：(1) 嵌入 common.py 替代导频信道估计 (2) 对比不同湍流强度下性能
- **可行性**：MODERATE（需新增 DL 模块）
- **风险**："为用而用"质疑；FPGA 部署困难

#### F2. 协作中继 → 相干检测

- **来源**：Agent C 方向2
- **关键论文**：
  - Xu et al. (2024), "Cooperative FSO/RF Space-Air-Ground Integrated Network", IEEE TWC, c=46
  - Lin et al. (2025), "Analysis of Outage Probability of Parallel-UAV-Based FSO", Entropy
- **已有成果**：DF/AF 中继 outage/BER 分析（IM/DD）
- **扩展方案**：(1) 两跳 GG 信道相干 DF 中继 BER 分析 (2) AF 噪声累积建模 (3) 每跳独立载波恢复
- **可行性**：MODERATE
- **风险**：几乎无相干 FSO 中继参考；中继节点本振同步棘手

#### F3. RIS 辅助 FSO 相干检测

- **来源**：Agent C 方向8
- **关键论文**：
  - Ata et al. (2024), "RIS-Embedded UAVs Communications for Multi-Hop FSO Backhaul", IEEE TVT, c=15
  - Razali et al. (2026), "Comprehensive Systematic Review of RIS in FSO Systems"
- **已有成果**：RIS 反射增强接收功率（IM/DD）
- **扩展方案**：(1) RIS 辅助相干 FSO 复数信道模型 (2) RIS 相位优化目标变为 Re{h_RIS} (3) RIS 引入的附加相位噪声对载波跟踪影响
- **可行性**：MODERATE
- **风险**：偏离核心主题（硬件辅助 vs 信号处理）

---

### G 组：系统级（2 个方向）

#### G1. 定制化 DSP 链对比

- **来源**：Agent A 方向6
- **关键论文**：
  - Valjus, Wolf, Poliak (2025), 同 E3 的第二篇
- **已有成果**：系统综述定时恢复/载波同步/均衡算法组合
- **扩展方案**：为 QPSK+GG+LEO 场景定制最优 DSP 链，量化各模块性能贡献和复杂度
- **可行性**：HIGH
- **风险**：综述性质，创新性有限

#### G2. 湍流信道建模验证与参数敏感性

- **来源**：跨 agent 综合
- **核心洞察**：几乎所有 FSO 相干检测论文使用简化的 GG 模型，但实际湍流的非 Kolmogorov 谱、孔径平均效应等被忽略
- **扩展方案**：(1) 对比 Kolmogorov vs 非 Kolmogorov 谱对相干检测性能影响 (2) 孔径平均效应对 SNR 模型修正
- **可行性**：MODERATE
- **风险**：偏建模，信号处理贡献不突出

---

## 综合推荐排序（Top 10）

| 排名 | 编号 | 方向 | 可行性 | 新颖性 | 与框架契合 | 综合推荐 |
|------|------|------|--------|--------|-----------|---------|
| 1 | E1 | 湍流时间相关性→载波跟踪 | HIGH | **极高** | 极高 | ★★★★★ |
| 2 | A1 | 自适应/突发感知 KF | HIGH | HIGH | 极高 | ★★★★★ |
| 3 | B1 | ODPLL Z 变换 Doppler-湍流联合建模 | HIGH | HIGH | 极高 | ★★★★☆ |
| 4 | C1 | 多孔径 MRC 分集接收 | MOD-HIGH | HIGH | 高 | ★★★★☆ |
| 5 | A3 | 频域导频音联合跟踪 | HIGH | HIGH | 高 | ★★★★ |
| 6 | A2 | ANN/RNN 载波恢复 | HIGH | HIGH | 高 | ★★★★ |
| 7 | B2 | Doppler 预补偿+湍流后补偿 | HIGH | MOD | 高 | ★★★☆ |
| 8 | C2 | 双偏振偏振跟踪 | HIGH | MOD | 中 | ★★★☆ |
| 9 | E2 | 性能界 outage/capacity | HIGH | MOD | 高 | ★★★ |
| 10 | D1 | 自适应调制 BPSK/QPSK/16-QAM | HIGH | MOD | 极高 | ★★★ |

## 跨 agent 核心发现

1. **"光纤 DSP → FSO 湍流迁移" 几乎无人做过**：光纤相干检测 DSP 方法（KF、BPS、编码辅助等）非常成熟，但搬到 FSO 湍流场景的工作极少。这是最大的系统性机会。
2. **相干检测 vs IM/DD 的 SNR 模型差异（h·γ̄ vs h²·γ̄）** 是所有方向的技术基础，决定了扩展的数学路径。
3. **湍流时间相关性对载波跟踪的影响** 是 IM/DD 完全无法触及的问题空间，是最具差异化的方向。
4. **已有直接面向 FSO 的相干检测工作**：Zhang 2023 (IEEE Photonics Journal), Nasrollahzadeh 2025 (IEEE Access), Pech 2025 (ICSOS), Fardoost 2026 (Nanophotonics)，说明迁移路径已被初步验证。
5. **2026 年有多篇最新论文**直接推动 FSO 相干检测 DSP：Yang 2026 (导频音), Hu 2026 (FDE内嵌CPE), Deng 2026 (PS+RCM)，领域正在活跃发展。

## 防坑检查

| 候选方向 | 触碰死胡同? | TL/FR 风险 |
|---------|-----------|-----------|
| E1 时间相关性 | ❌ | 低 — IM/DD 无法覆盖，真差异化 |
| A1 自适应KF | ❌ | 低 — 已有光纤+无线光验证 |
| B1 ODPLL | ⚠️ | 中 — 类似D008但方法不同（Z变换 vs KF） |
| C1 多孔径 | ⚠️ | 中 — 之前否决过多孔径合并？需确认 |
| D1 自适应调制 | ⚠️ | 高 — 之前否决过（循环依赖） |
| F1 DL信道估计 | ⚠️ | 中 — TL-05（分析>算法） |

## 结论

从"找空白"转向"找可扩展已有工作"后，候选方向从 10 个扩展到 22 个，覆盖 7 个主题组。Top 3 推荐：

1. **E1 湍流时间相关性→载波跟踪** — IM/DD 无法触及的独特空间，直接扩展已有 KF/DPLL
2. **A1 自适应/突发感知 KF** — 最小改动量，光纤+无线光已验证，创新点在于 GG 突发感知机制
3. **B1 ODPLL Z 变换 Doppler-湍流联合建模** — 直接对接"星地湍流信道"论文主题

## 对决策的影响

候选方向清单已扩展至 22 个，需用户选择 2-3 个进入 MVE 验证。
