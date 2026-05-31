# R014: FPGA选题验证与调制格式全局风险评估

> 2026-05-29 | 关联：PROMPT-017, S005 Q7-Q8

## 调研问题

Q7：哪个模块上FPGA有文献先例？"多普勒+湍流联合FPGA验证"空白是否真实？
Q8：调制格式QPSK vs DP-QPSK不确定性对全局的影响？

## 检索概况

- 6条英文搜索(S2+OpenAlex)，覆盖FPGA carrier sync / DSP FSO / Doppler / clock recovery / CMA / DP-QPSK
- 3条CNKI搜索（均返回0条，CNKI该方向文献可能未被索引或关键词不匹配）
- 总计67条原始结果，去重后约45条独立论文

## 发现

### Q7：FPGA+光通信已有论文的模块覆盖

| 模块 | FPGA文献先例 | 代表论文 | 年份 | 引用 |
|------|-------------|---------|------|------|
| **多普勒频偏补偿** | 有 | Real-time FPGA prototyping of Doppler frequency shift compensation using DSP-assisted AFC (Optics Letters) | 2024 | 1 |
| **多普勒实时跟踪** | 有 | Real-Time Doppler Shift Tracking Scheme for LEO Satellite-Ground Links (ACP) | 2025 | 0 |
| **定时恢复(Gardner类)** | 有 | Real-Time Demonstration of Digital Interpolator-Free Clock Recovery for FPGA-Based PM-QPSK (JLT) | 2025 | 3 |
| **定时恢复(FSO专用)** | 有 | All-Digital Timing Recovery for FSO Signals With Large Dynamic Range (IEEE Photonics Journal) | 2019 | 12 |
| **CMA偏振解复用** | 有 | A real-time CMA-based 10 Gb/s polarization demultiplexing coherent receiver implemented in an FPGA (OFC) | 2008 | 55 |
| **DP-QPSK完整接收端** | 有 | Low-Complexity FPGA Implementation of 106.24Gbps DP-QPSK Coherent Optical Receiver (JLT) | 2023 | 15 |
| **SP-QPSK/16QAM接收端** | 有 | Real-time 15GBaud QPSK and 16QAM Flexible Coherent Optical Receiver on Single FPGA (ICCT) | 2023 | 5 |
| **时钟+均衡联合** | 有 | Real-time FPGA prototyping of 15GBaud SP-16QAM coherent receiver with clock recovery and equalization (OE) | 2022 | 8 |
| **载波相位恢复(CPR)** | 有 | A Low-latency Carrier Phase Recovery Hardware for Coherent Optical Communication (ISCAS) | 2022 | 1 |
| **DQPSK载波同步** | 有 | Research and Implementation of DQPSK Modulation and Carrier Synchronization Based on FPGA | 2023 | 0 |
| **FSO湍流+分集合并** | 有 | Real-time low-complexity diversity combining for free space coherent optical over turbulence (OE) | 2023 | 4 |
| **FSO湍流+MIMO均衡** | 有 | Real-time demonstration of two-aperture coherent digital combining FSO with real-valued MIMO equalizer (OL) | 2024 | 3 |
| **星间相干接收DSP设计** | 有 | Coherent receiver design based on DSP in optical high-speed intersatellite links (M-PSK) | 2016 | 19 |

#### 关键综述

**"Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links"** (2025, Int. J. Satellite Comm., 4引)
- 综述了星地相干光链路的全部DSP算法
- 覆盖：CD补偿、偏振解复用、频偏估计、载波相位恢复、非线性补偿
- **明确指出**：星地链路的多普勒和大气效应是区别于光纤的独特挑战
- 该综述是写Ch5的最佳参考文献

#### "多普勒+湍流联合FPGA验证"空白分析

逐项检查：
- **多普勒FPGA**: 有（2024 OL ±8GHz AFC, 2025 ACP实时跟踪）
- **湍流信道FPGA**: 有但少（2023 OE分集合并, 2024 OL数字合并）
- **联合验证**: **无任何文献**同时处理多普勒和湍流退化的FPGA实时验证
- 2025综述列出的挑战也是分开讨论的

**结论：空白确认。** "多普勒+湍流联合FPGA验证"在文献中确实是空白。

#### 用户Verilog代码复用率评估

| 现有代码 | 文献先例 | 复用评估 |
|---------|---------|---------|
| CMA 16抽头 | 2008 OFC CMA-based 10Gbps, 2023 JLT 106Gbps DP-QPSK | 直接复用，标准结构 |
| FFT+NCO | 2024 OL AFC方案类似（频偏估计+NCO补偿） | 直接复用，FOE核心 |
| Gardner定时同步 | 2025 JLT interpolator-free, 2019 FSO专用 | 直接复用，需调参数 |

**复用率70%的估计合理**，三个模块均有成熟FPGA先例。

#### 接收端DSP链上FPGA的工作量

文献中的工作量参照：
- 2022 OE: 15GBaud SP-16QAM全链路 → **单FPGA实现**
- 2023 ICCT: 15GBaud QPSK/16QAM灵活接收 → **单FPGA**
- 2023 JLT: 106.24Gbps DP-QPSK全链路 → **单FPGA + 低复杂度DSP**

半章(约5-8页)覆盖：系统架构设计(1页) + 各模块实现要点(3-4页) + 测试结果(1-2页) → **可行**。

### Q8：调制格式不确定性的全局影响

#### 星地FSO中QPSK vs DP-QPSK的文献分布

| 格式 | FSO文献 | 代表论文 |
|------|---------|---------|
| SP-QPSK/SP-16QAM | 多 | 2022 OE 15GBaud SP-16QAM FPGA; 2023 ICCT SP-QPSK/16QAM FPGA |
| DP-QPSK | 中等 | 2023 "Implementation of 10Gbps DP-BPSK/DP-QPSK coherent receiver for FSO"; 2025 IEEE Access "DP self-coherent for FSO with turbulence" |
| PM-QPSK | 有 | 2025 JLT "PM-QPSK FPGA clock recovery"; 2023 JLT 106.24Gbps DP-QPSK |

**观察**：在FSO领域，SP-QPSK和DP-QPSK都有使用，没有明显的主流偏好。DP-QPSK在高速(>40Gbps)场景更常见，SP-QPSK在中等速率和简化实现中更常见。

#### DP-QPSK额外复杂度

来自2023 JLT (106.24Gbps DP-QPSK FPGA)和2008 OFC (CMA-based DP demux)：
- CMA: 1×2 FIR → 2×2 MIMO FIR，**计算量×4**
- 抽头数：单偏振通常7-17抽头，DP需要每个2×2 MIMO的4个FIR滤波器
- 收敛：2×2 CMA收敛更慢，需预处理或初始化策略
- FPGA资源：约2倍LUT/FF/BRAM使用
- ADC：需要2路（双偏振），硬件成本翻倍

#### SP-QPSK vs DP-QPSK对三章的影响

| 章 | SP-QPSK | DP-QPSK | 额外工作量 |
|---|---------|---------|-----------|
| Ch2 信道估计 | GG信道建模+LS/MMSE估计，不变 | GG建模不变，估计需扩展到2×2 | 低 |
| Ch3 预补偿 | 发射端功率自适应预补偿，不变 | 功率预补偿不变，但需声明偏振旋转假设 | 低 |
| Ch4 载波同步 | VV/BPS CPE直接可用 | 需要偏振解复用后的CPE，流程更长 | 中 |
| Ch5 FPGA | 1路处理 | 2路处理+2×2 CMA | 高 |

**关键判断**：SP-QPSK下三章全部成立，各章核心方法不受影响。DP-QPSK主要增加Ch5的FPGA实现复杂度和Ch4的处理链长度。

## 结论

### Q7结论：FPGA选题确认可行

- 结论：接收端DSP链(Gardner+FOE+CPR)上FPGA有充分文献先例，半章篇幅足够
- 证据：13篇FPGA+光通信论文，覆盖所有主要模块；2025综述确认星地DSP链的独特挑战
- 可信度：**高**
- 创新叙事："LEO多普勒+大气湍流联合退化信道下的实时DSP验证"——空白经检索确认真实
- 复用率70%确认合理

### Q8结论：SP-QPSK更稳妥，DP-QPSK可讨论

- 结论：SP-QPSK三章全部成立，且FPGA实现简单；DP-QPSK主要增加复杂度而非创新性
- 证据：SP-QPSK在FSO中等速率场景有充分文献支持；DP-QPSK额外复杂度主要是工程量的增加
- 可信度：**高**
- 建议：**默认用SP-QPSK，与导师确认是否需要DP-QPSK**
- 核心理由：硕士论文半章FPGA，DP-QPSK的额外复杂度(2×2 CMA + 双路处理)在没有对应算法创新的情况下只是工程放大

## 对决策的影响

1. **Ch5 FPGA选题确认**：接收端DSP链(Gardner+FOE+CPR)，故事="多普勒+湍流联合验证"
2. **调制格式建议**：默认SP-QPSK，理由是三章不受影响且FPGA半章工作量可控
3. **需与导师确认**：调制格式（QPSK还是DP-QPSK）——这是全局影响最大的未决项
