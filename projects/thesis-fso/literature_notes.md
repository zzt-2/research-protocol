# 文献调研笔记 — 星地激光通信信号处理

> 硕士论文"星地激光通信信号处理关键技术研究"
> 三章：Ch2信道估计 → Ch3信道均衡 → Ch4载波同步
> 技术路线：统一仿真（相干检测 + QPSK + GG大气湍流 + Python全栈）
> 策略：传统方法主线，DL作为对比实验

## 步骤进度

| 步骤 | 状态 | 日期 | 备注 |
|------|------|------|------|
| Step 1 检索+初筛 | ✅ | 2026-05-29 | PROMPT-011，一轮21条+二轮6条验证，全部完成 |
| Step 2 论文获取 | ⬜ | | |
| Step 3 精读 | ⬜ | | |
| Step 3.5 定向补充 | ⬜ | | |

## 搜索统计报告

```
检索轮次：一轮 21 条（Ch2×7 + Ch3×7 + Ch4×7）+ 二轮 6 条定向验证
原始条目：Ch2=94, Ch3=121, Ch4=102, 二轮=326, 合计≈643
去重后有效条目：Ch2=73, Ch3=38, Ch4=82, 二轮补充≈25
必读篇数：Ch2=8(+2二轮), Ch3=8(+0), Ch4=11, 合计≈29
建议读篇数：Ch2=13, Ch3=12, Ch4=13, 合计=38
搜索源：Semantic Scholar, OpenAlex, arXiv, SerpAPI, Exa, CNKI（6源）
覆盖子方向：见下方各章分析
质量门槛：去重≥20/方向 ✓ | ≥3源 ✓ | 必读≥5/方向 ✓ | ≥2子方向 ✓
```

---

## Ch2 信道估计 — 候选论文

### 必读（8篇）

| # | 标题 | 年份 | 期刊/会议 | 引用 | 原因 |
|---|------|------|----------|------|------|
| 1 | Amirabadi et al., "Deep learning for channel estimation in FSO communication system" | 2020 | Optik | 87 | DL信道估计FSO基线论文，GG湍流，含LS/MMSE对比 |
| 2 | Elfiky & Rezki, "Symbol Detection and Channel Estimation for Space Optical Communications Using NN and Autoencoder" | 2024 | IEEE TMLCN | 16 | 唯一直接做LEO+GEO星地光通信信道估计+NN，GG+Lognormal |
| 3 | Dabiri et al., "FSO channel estimation for OOK modulation with APD receiver over atmospheric turbulence and pointing errors" | 2017 | Optics Communications | 64 | 经典FSO信道估计，OOK+APD+湍流+指向误差 |
| 4 | Rustum et al., "Hybrid STA With FNN and CNN Models for Robust Channel Estimation in Turbulent FSO and Doppler-Affected OFDM for LEO Satellite" | 2026 | IET Communications | 0 | 直接LEO FSO OFDM信道估计，湍流+多普勒联合 |
| 5 | Rustum et al., "Clustering-assisted channel estimation for free-space optical satellite communication" | 2026 | Elsevier | 2 | FSO LEO卫星信道估计，聚类辅助 |
| 6 | Mohammed et al., "Free space optical turbulent channel estimation based on deep combined CNN and BiLSTM network" | 2026 | J. Optical Communications | 0 | CNN+BiLSTM GG湍流信道估计，弱中强湍流对比LS/LMMSE/EKF |
| 7 | Ndiaye et al., "Free space optical channel estimation based on deep learning algorithms" | 2023 | IEEE | 4 | DNN/CNN/RNN对比LS/MMSE，强GG湍流 |
| 8 | Chen et al., "Joint estimation model for FSO channel parameters and performance evaluation based on CNNs" | 2024 | Applied Optics | 3 | CNN联合估计检测噪声+湍流参数，含Cn² |

### 建议读（13篇）

| # | 标题 | 年份 | 期刊 | 引用 | 原因 |
|---|------|------|------|------|------|
| 9 | D'Amico & Morelli, "Symbol-Spaced Feedforward Techniques for Blind Bit Synchronization and Channel Estimation in FSO-OOK" | 2024 | IEEE Trans. Commun. | 7 | OOK盲同步+信道估计 |
| 10 | Selvaraj et al., "SWALNet: A sparse wavelength aware learning framework for robust FSO channel estimation" | 2025 | Scientific Reports | 0 | GG+OFDM+波长感知，对比LMS/Kalman/DNN |
| 11 | Chaudhary et al., "Machine Learning based Channel Estimation for Gamma-Gamma Noise" | 2025 | Optica Preprints | 0 | ML估计GG参数(α,β) |
| 12 | Chaudhary et al., "Data-driven statistical channel estimation for gamma-gamma noise" | 2026 | Applied Optics | 0 | 同组期刊版，含α,β参数估计 |
| 13 | Kim & Yoon, "Moment-based estimation for gamma-gamma fading parameters in FSO links" | 2025 | IEEE | 12 | 矩估计GG参数(α,β) |
| 14 | Xu et al., "Satellite-to-ground optical communication systems under orbital deviations and atmospheric turbulence" | 2025 | Optics Express | 16 | 星地光通信信道建模+指向误差+湍流 |
| 15 | Czerwinski et al., "Optical Downlink Modeling for LEO and MEO Satellites under Atmospheric Turbulence" | 2025 | arXiv | 0 | LEO/MEO光学下行链路预算建模 |
| 16 | Czerwinski, "Atmospheric modeling of free-space optical transmission" | 2025 | Opt. Quantum Electron. | 8 | 统一FSO大气信道建模框架 |
| 17 | Dabiri et al., "Hierarchical Deep Learning for Joint Turbulence and PE Estimation in Multi-Aperture FSO" | 2025 | arXiv | 0 | 分层DL联合估计湍流+指向误差 |
| 18 | Song et al., "Performance evaluation of FSOC terminal with local weather considerations" | 2025 | Optics Express | 3 | 实测FSO终端性能，含Cn²估计 |
| 19 | Tumma & Miriyala, "Deep learning-based pilot-free channel estimation of UAV-FSO system using VAE" | 2025 | ICT Express | 1 | VAE无导频信道估计 |
| 20 | Zhu & Zheng, "Research on FSO channel estimation technology based on machine learning" | 2025 | SPIE | 0 | CNN+Attention+BiLSTM混合 |
| 21 | 武盈等, "基于DNN信道估计的自适应概率整形FSO系统" | 2026 | 空间电子技术 | - | 中文唯一直接做DNN+FSO信道估计 |

### 覆盖子方向

- 传统方法：LS, MMSE/LMMSE, Kalman/EKF — 多篇对比
- DL方法：DNN, CNN, CNN+BiLSTM, VAE, Autoencoder — 覆盖充分
- GG湍流参数估计：α,β估计（#11, #12, #13）
- 星地/LEO信道建模：#4, #5, #14, #15, #16
- **关键空白：相干检测FSO信道估计** — 几乎所有论文假设IM/DD体制，相干场景需估计复信道系数的文献几乎空白

### 二轮补充发现（Ch2）

| # | 标题 | 年份 | 期刊 | 引用 | 原因 |
|---|------|------|------|------|------|
| 22 | "Phase and Channel Estimation for High-Capacity Phase-Asynchronous MDM-MIMO FSO in Strong Turbulent Channels" | 2024 | JLT | 5 | **必读**：相干MDM-MIMO-FSO相位和信道估计，唯一相干体制FSO信道估计方法论文 |
| 23 | 张岱, "星地相干激光通信大气信道特征及信号处理技术研究" | 2018 | 国防科大博士论文 | 8 | **必读**：已精读摘要。五章：偏振变化→波前校正→**多径均衡(CMA变体)**→纠错编码。**关键发现**：(1)用DPSK+自差探测，非我们QPSK+相干检测，有体制差异；(2)Ch5做了SN-BNMCMA均衡但针对大气散射多径，非GG湍流；(3)论文§1.2.3.2明确指出"相位调制序列的信道均衡技术还有待进一步研究"——直接佐证Ch3空白；(4)**没有做信道估计(LS/MMSE/Kalman)和载波同步**——与Ch2/Ch4无重叠。CAJ已转markdown存papers/downloads/2026-05-29/ |

---

## Ch3 信道均衡 — 候选论文

### 必读（8篇）

| # | 标题 | 年份 | 期刊/会议 | 引用 | 原因 |
|---|------|------|----------|------|------|
| 1 | Khalighi & Uysal, "Survey on Free Space Optical Communication: A Communication Theory Perspective" | 2014 | IEEE COMST | 2378 | FSO通信理论综述标杆，含均衡方法综述 |
| 2 | Almogahed et al., "MDM-FSO improvement through various atmospheric conditions with DFE" | 2022 | Cogent Engineering | 37 | FSO中MMSE-DFE完整实现，含抽头数配置 |
| 3 | Almogahed & Amphawan, "Design of 7x2.5 Gbps DFE scheme for MDM-FSO" | 2022 | Optical Engineering | 12 | 扩展DFE-MMSE配置 |
| 4 | Almogahed & Amphawan, "Mitigation of atmospheric turbulences using MDM based on DFE for FSO" | 2020 | J. Optical Communications | 29 | DFE-MMSE在FSO中的原始研究 |
| 5 | Zhang et al., "DPSK and channel equalization in FSO communication system" (SM-BNMCMA) | 2018 | Optical Engineering | 4 | 相干FSO中CMA变体均衡 |
| 6 | 赵远帆, "空间相干激光通信信道均衡算法研究" | 2024 | 青岛大学硕士论文 | 1 | 空间相干激光通信均衡系统 |
| 7 | 夏煜, "空空信道高速激光通信均衡技术研究及实现" | 2024 | 电子科技大学硕士论文 | 1 | 空空激光通信均衡实现 |
| 8 | 郭兴兰, "空间光通信大气湍流信道自适应均衡算法研究" | 2016 | 北京邮电大学硕士论文 | 2 | 空间光通信湍流信道自适应均衡 |

### 建议读（12篇）

| # | 标题 | 年份 | 期刊 | 引用 | 原因 |
|---|------|------|------|------|------|
| 9 | Ahmad et al., "Robust high-capacity FSO using OAM-based structured light and intelligent adaptive signal processing" | 2026 | Scientific Reports | 0 | DL均衡(DNFIS+DCNN)与DFE对比 |
| 10 | Nasr et al., "ANN-Based Equalization of Polarization Mixing for DP-SC in FSO" | 2026 | IEEE Access | 0 | DL均衡FSO应用 |
| 11 | Zhang et al., "LDPC coded OAM-FSO system with ZF/MMSE equalization" | 2018 | Optics Express | 28 | MMSE/ZF均衡在OAM-FSO中对比 |
| 12 | Fernandes et al., "High-capacity coherent FSO" | 2024 | Springer Book Chapter | 4 | 相干FSO的DSP综述 |
| 13 | Zhang et al., "Blind Equalization Using ICA" | 2013 | JLT | 23 | ICA盲均衡替代CMA |
| 14 | Huang, "DSP for coherent optical communication with advanced modulation" | 2020 | CEECT | 3 | CMA+DD-LMS完整DSP流程 |
| 15 | Yu et al., "PDL and CD insensitive low complexity equalizer for short reach coherent" | 2021 | Optics Express | 5 | CMA低成本变体，含抽头数设计 |
| 16 | 佟欣等, "空间激光通信中变步长CMA-LMS均衡算法" | 2020 | 光通信技术 | 10 | CMA-LMS变步长方案，参数参考 |
| 17 | 曹明静等, "激光通信系统的波特间隔均衡器设计" | 2023 | 激光杂志 | 1 | 波特间隔均衡器参数设计 |
| 18 | 周超, "基于LMS算法的光通信自适应数字均衡技术研究" | 2018 | 电子科技大学硕士论文 | 14 | LMS自适应均衡系统研究 |
| 19 | 张异凡, "光通信系统中的信道均衡与补偿算法研究" | 2018 | 北京邮电大学硕士论文 | 8 | 信道均衡与补偿全面研究 |
| 20 | 陈昊, "短距高速相干光通信系统中自适应均衡技术研究" | 2022 | 华中科技大学硕士论文 | 2 | 相干光自适应均衡 |

### 覆盖子方向

- 传统均衡：CMA, LMS, RLS, MMSE-DFE, ZF — 覆盖良好
- DL均衡：ANN, CNN, BiLSTM — 有代表性论文
- 相干检测均衡：偏振解复用、载波恢复联合均衡 — 有覆盖
- 中文文献：空间激光通信均衡国内研究 — 8篇直接相关
- **关键空白：星地/卫星链路的后均衡文献极度稀缺** — 多数FSO均衡聚焦地面链路或OAM模分复用

### 二轮补充发现（Ch3）

| # | 标题 | 年份 | 期刊 | 引用 | 原因 |
|---|------|------|------|------|------|
| 21 | Nasr et al., "ANN-Based Equalization of Polarization Mixing for Self-Coherent Transceivers in FSO" | 2026 | IEEE Access | 0 | 自相干FSO + ANN均衡，最新但非卫星场景 |
| 22 | Flexible phase synchronization with adaptive fractionally-spaced blind equalization for coherent optical | 2023 | IEEE Photonics J. | 4 | 相干体制盲均衡+相位同步，非GG湍流 |

---

## Ch4 载波同步 — 候选论文

### 必读（11篇）

| # | 标题 | 年份 | 期刊/会议 | 引用 | 原因 |
|---|------|------|----------|------|------|
| 1 | Yang et al., "Low-complexity carrier phase estimation algorithms for space coherent optical communication" | 2025 | SPIE HPCCE | 0 | V-V vs BPS空间相干光通信直接对比 |
| 2 | Hu et al., "A noise-tolerant carrier phase recovery method for inter-satellite coherent optical communications" | 2025 | Electronics | 3 | 星间相干载波相位恢复，二阶反馈+前馈混合 |
| 3 | Chen et al., "Multiplier-free QPSK phase recovery for coherent intersatellite optical wireless communication" | 2025 | Chinese Optics Letters | 1 | 星间QPSK相位恢复，与V-V对比灵敏度+1dB |
| 4 | Paillier et al., "Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop" | 2020 | JLT | 35 | 星地相干光链路AO+数字PLL端到端模型 |
| 5 | Wang et al., "Enhanced frame synchronization and carrier recovery in coherent FSO communication" | 2024 | Optics Express | 2 | FSO湍流下帧同步+载波恢复 |
| 6 | Zhang et al., "Flexible Phase Synchronization for Wireless Optical Coherent Communication System" | 2023 | IEEE Photonics Journal | 3 | 自适应Kalman滤波+盲均衡相位同步，与VVPE对比 |
| 7 | Sun et al., "Parallelized and adaptive square-root unscented Kalman filter for carrier recovery in satellite-to-ground coherent optical communications" | 2020 | Optics Communications | 7 | 星地SR-UKF载波恢复 |
| 8 | Wang et al., "Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links" | 2025 | ACP | 0 | LEO星地多普勒实时跟踪，FPGA，±8GHz |
| 9 | Zhao et al., "Joint Doppler and Phase Noise Compensation Method for Inter-Satellite Coherent Laser Communication" | 2025 | ICCSN | 0 | 星间多普勒+相位噪声联合补偿 |
| 10 | Fernandes et al., "Digitally mitigating Doppler shift in high-capacity coherent FSO LEO-to-Earth links" | 2023 | JLT | 31 | LEO-地面多普勒数字补偿 |
| 11 | Sun et al., "Low Complexity Carrier Recovery based on Gradient Descent for Optical Communication" | 2025 | IEEE PTL | 1 | 梯度下降载波恢复，与VV/LKF对比 |

### 建议读（13篇）

| # | 标题 | 年份 | 期刊 | 引用 | 原因 |
|---|------|------|------|------|------|
| 12 | Tang et al., "A Low-Complexity Joint Compensation Scheme of Carrier Recovery for Coherent FSO" | 2023 | Photonics | 7 | 相干FSO载波恢复联合补偿，10Gbps QPSK |
| 13 | Xu et al., "Real-time low-complexity diversity combining algorithm for free space coherent optical communication" | 2023 | Optics Express | 4 | 分集+CV-DD-LMS载波恢复，FPGA实时 |
| 14 | Wang et al., "Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication" | 2023 | IEEE Photonics Journal | 8 | 空间分集FSO载波频偏估计 |
| 15 | Tang et al., "Symmetric Training Sequence-Based Carrier FOE Scheme for Coherent FSO" | 2022 | IEEE Photonics Journal | 3 | FSO频偏估计训练序列方法 |
| 16 | Almonacil et al., "Digital Pre-Compensation of Doppler Frequency Shift in Coherent Optical Satellite Communications" | 2020 | ECOC | 6 | 发射端数字预补偿多普勒 |
| 17 | Tang et al., "Compensation of Doppler frequency shift based on two-stage FOE algorithm for coherent optical QPSK" | 2024 | AFLC | 0 | 两阶段频偏估计补偿多普勒 |
| 18 | Meng et al., "Two-stage frequency compensation for Doppler shift on BPSK transceiver" | 2023 | Frontiers in Physics | 7 | BPSK两阶段频率补偿 |
| 19 | Zhang & Shu, "Viterbi-Viterbi algorithm based phase recovery for probabilistically shaped signals" | 2021 | JLT | 34 | V-V vs BPS系统性对比，含窗口/线宽/复杂度 |
| 20 | Spatharakis et al., "Frequency offset estimation and carrier phase recovery for high-order QAM using V-V monomial estimator" | 2014 | IEEE | 7 | V-V扩展到高阶QAM |
| 21 | Zhang et al., "Experimental Comparison of Carrier Phase Recovery Algorithms" | 2023 | Photonics | 1 | VV/NVV/BPS/两阶段BPS实验对比 |
| 22 | Pech et al., "Z-Transform Model of a Coherent Receiver for Satellite-to-Ground Laser Links Under High Doppler Rates" | 2025 | ICSOS | 0 | 高多普勒率相干接收机建模 |
| 23 | Konaka et al., "On-Orbit Demonstration of Laser Frequency Sweep at 1550 nm for Doppler Compensation" | 2024 | OECC | 0 | 在轨验证1550nm多普勒补偿 |
| 24 | Yokomura et al., "Real-Time Verification of Transmitter-Side Frequency Shift for Doppler-Shift Compensation" | 2025 | OECC/PSC | 0 | 发射端2GHz多普勒实时补偿验证 |

### 覆盖子方向

- V-V算法（FSO/星间）：#1, #3, #11, #19, #20 — 充分
- BPS算法：#1, #19, #21 — 充分
- V-V vs BPS对比：#1, #19, #21 — 多篇独立对比
- 多普勒频移补偿（LEO星地/星间）：#8, #9, #10, #16, #17, #18 — 充分
- 大气湍流下载波同步：#4, #5, #6, #12, #14 — 充分
- Kalman滤波载波恢复：#6, #7 — 良好
- 低复杂度+FPGA：#8, #11, #13 — 良好
- **空白：FSO载波同步专门综述缺失；中文CNKI"载波同步+激光通信+相干"无结果；多普勒+湍流联合场景论文少**

---

## 研究空白汇总

### 已确认的空白（二轮验证完成 ✅）

| 空白 | 章节 | 验证结论 | 空白类型 | 创新潜力 |
|------|------|----------|----------|----------|
| 相干检测FSO信道估计 | Ch2 | **部分空白**：非绝对零（JLT 2024有1篇MDM-MIMO，张岱2018博士论文需精读），但"GG湍流+相干PSK+导频辅助信道估计"系统性方法论文为零 | 方法空白 | ★★★ 高 |
| 星地/卫星链路后均衡 | Ch3 | **确认空白**：80条去重结果中无一同时满足"卫星/星地"+"后均衡"+"光通信"。现有FSO均衡全聚焦地面/OAM。张岱2018博士论文§1.2.3.2明确指出"相位调制序列的信道均衡技术还有待进一步研究" | 场景空白 | ★★☆ 中高 |
| GG湍流+相干PSK+均衡联合 | Ch2+Ch3 | **确认空白**：240+条去重结果中无一同时涉及三重组合。相干FSO湍流处理主流是AO/OPC，电域后均衡非主流 | 组合空白 | ★★★ 高 |
| FSO载波同步专门综述 | Ch4 | 无专门针对FSO载波同步的综述，但V-V/BPS对比和多普勒补偿研究已充分 | 文献空白 | ★☆☆ 低 |

### 需精读确认的关键论文

1. ~~**张岱(2018国防科大博士论文)**~~ — ✅ 已精读核心章节。DPSK+自差探测体制，与QPSK+相干检测有区分度。论文明确确认"相位调制序列信道均衡"为开放问题
2. **JLT 2024 (5引用)** — "Phase and Channel Estimation for Phase-Asynchronous MDM-MIMO FSO" — 唯一相干FSO信道估计方法论文，需确认与开题方向的区分度
3. **IEEE Access 2026** — "ANN-Based Equalization for Self-Coherent Transceivers in FSO" — 自相干均衡最新工作
4. **孙建锋等(2022/2023专著)** — "空间相干激光通信技术" — 可能系统覆盖信道估计和均衡

---

## 参数来源表

### GG湍流参数

| 参数 | 值 | 来源论文 | 来源类型 |
|------|-----|---------|---------|
| α,β值(弱/中/强湍流) | 待精读确认 | Mohammed 2026 (#Ch2-6), Ndiaye 2023 (#Ch2-7) | [实证] |
| α,β ML估计 | - | Chaudhary 2025/2026 (#Ch2-11/12) | [实证] |
| α,β 矩估计 | - | Kim & Yoon 2025 (#Ch2-13) | [理论] |
| Cn²估计 | - | Song 2025 (#Ch2-18) | [实测] |
| Cn²剖面 | - | Arvis 2025 | [实测] |

### 链路参数

| 参数 | 值 | 来源论文 | 来源类型 |
|------|-----|---------|---------|
| 星地链路距离/天顶角 | LEO 500-2000km | Czerwinski 2025, Xu 2025 | [建模] |
| 波长 | 1550nm | Konaka 2024 (#Ch4-23), 多篇 | [标准] |
| 符号速率 | 10 Gbps | Ivanov 2022, Tang 2023 (#Ch4-12) | [实验] |

### 均衡器参数

| 参数 | 值 | 来源论文 | 来源类型 |
|------|-----|---------|---------|
| DFE抽头数 | 待精读 | Almogahed 2022系列 (#Ch3-2/3/4) | [实证] |
| CMA步长 | 待精读 | 佟欣2020 (#Ch3-16) | [实证] |
| CMA抽头数 | 待精读 | Yu 2021 (#Ch3-15) | [实证] |
| 波特间隔设计 | 待精读 | 曹明静2023 (#Ch3-17) | [实证] |

### 载波同步参数

| 参数 | 值 | 来源论文 | 来源类型 |
|------|-----|---------|---------|
| V-V窗口长度 | 待精读 | Zhang & Shu 2021 (#Ch4-19) | [理论+实证] |
| Δν·Ts容忍度 | - | Yang 2025 (#Ch4-1), Spatharakis 2014 | [理论] |
| 多普勒频移范围(LEO) | ±8GHz | Wang 2025 (#Ch4-8), Fernandes 2023 (#Ch4-10) | [工程] |
| 激光线宽 | 10kHz | Zhao 2025 (#Ch4-9) | [实验] |

---

## 综合分析

### 领域概况

FSO通信信号处理分为两条技术路线：
1. **IM/DD体制**（强度调制/直接检测）：绝大多数信道估计和均衡研究基于此体制，技术成熟度高
2. **相干检测体制**：载波同步研究充分（V-V/BPS/DPLL等），但信道估计和均衡在FSO场景下研究极少

### 核心挑战

1. **体制错位**：信道估计/均衡研究集中在IM/DD，但论文三章统一用相干检测——相干场景下需估计复信道系数，方法与IM/DD完全不同
2. **场景缺失**：均衡研究多面向地面链路或OAM模分复用，星地/LEO场景的均衡几乎是空白地带
3. **参数获取**：多数论文abstract不含具体参数值（α,β、抽头数、步长等），需精读全文提取

### 研究定位

基于两轮检索（27条搜索命令，643+条原始结果），论文三章的创新点定位：

- **Ch2 信道估计**：填补"GG湍流+相干检测FSO信道估计"的方法空白。现有DL方法（CNN/BiLSTM/VAE）均在IM/DD下验证，迁移到相干检测+GG湍流场景是新贡献。传统方法（LS/MMSE/Kalman）的相干FSO对比也几乎空白。唯一接近的JLT 2024论文面向MDM-MIMO场景，与单载波PSK有区分度。张岱2018博士论文需精读确认。
- **Ch3 信道均衡**：填补"星地场景相干检测后均衡"的场景空白。CMA/MMSE-DFE在FSO中已有基础研究（Almogahed系列），但"GG湍流+相干PSK+电域后均衡"的三重组合经240+条结果验证确认为空白。相干FSO湍流处理主流是AO/OPC（光域），电域后均衡是非主流路线。
- **Ch4 载波同步**：V-V/BPS对比和多普勒补偿已有充分研究（Liu 2023已做过VV/BPS对比，Fernandes 2023做过LEO多普勒数字补偿）。创新空间有限，定位为"系统实现+湍流+多普勒联合场景"。
