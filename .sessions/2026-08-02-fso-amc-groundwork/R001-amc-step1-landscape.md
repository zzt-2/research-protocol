# [R001] AMC Step 1 Landscape + 候选问题族地图

> 2026-08-02 | 关联：专题 slug 2026-08-02-fso-amc-groundwork / D001 / S001
> 数据源：search-archive/2026-08-02/ 16 queries × 5 sources（openalex/exa/arxiv/serpapi/cnki）= 209 unique candidates
> 阶段：GW Step 1（搜索级证据，非 Go/No-Go；候选问题假设，未过四判据）

---

## §1 调研问题

Step 1 要回答的问题，逐条对应 §5 八问：

1. 在"星地相干 FSO + Gamma-Gamma 湍流 + 真实编码链/信息不确定性"背景下，存在哪些**真实的 AMC / 链路适配机制族**（即存在跨码率/调制/功率/重传/HARQ-IR 的真实控制动作，而非仅 receiver-side DSP 或 AO 硬件补偿）？
2. 哪些 hit 实际只是 **automatic modulation classification（调制识别 / MFI / OPM）** 或无关资源分配（NOMA/IRS/RIS/路由/TCP/spectrum）？
3. 哪些与旧 9 条 dead-end（ISL AMC prediction / 反馈-相干时间 / MCS 0.09dB / AMC+CPR / 交织·PS·N1 / P08-R2 资产 / DA-NDA CPR 换名 / mod-classification / AMC↔Ch4 BER 循环）碰撞？
4. 哪些方向在**物理时间尺度**上明显危险（反馈 RTT vs 大气相干时间 2–10 ms；LEO 单 pass 不可回传；GEO RTT > 100 ms）？
5. 哪 **8–12 篇**值得进 Step 2 全文获取（shortlist）？
6. 当前最值得精读的 2–3 个候选问题族是哪几个？
7. 为什么它们比直接重开 receiver 小修补更可能形成毕业方法？
8. 若所有方向都高度饱和或物理不成立，需诚实报告。

本轮**仅搜索级**判断（title + abstract + venue + year + cited），不下载/精读全文。170/209 有摘要，38 条 CNKI 摘要为空（低 confidence，靠 title 判）。

---

## §2 检索规模与质量门

证据来自 `search-archive/2026-08-02/_manifest.json` + §3 triage 汇总。

| 指标 | 真实数字 | SLA 阈值 | 判定 |
|---|---|---|---|
| 检索轮次 | 2 轮（r1 axes A/B/C + r2 density/clusters）| — | — |
| queries | 16 去重 query（manifest 32 file 含 dup 文件，r1/r2 双跑）| — | — |
| 源 union | **4 源**：openalex / exa / serpapi / cnki（arxiv 在 manifest 标注但 r1-axA-mcs / mcs-fer-goodput 返回 n=0）| ≥3 源 | **PASS** |
| unique candidates | **209**（_alldigest.json，209 unique L）| ≥20 候选 | **PASS** |
| published | **115/209 = 55.0%**（manifest: published 153 含 r1-digest 重复计数；以 _alldigest unique 计 115 published + 3 preprint + 91 unknown/empty）| 正式发表 ≥50% | **PASS**（按 published 计 55.0%；若含 unknown 真实发表率会更高但保守按 55% PASS）|
| 必读 | **10**（§3 priority=必读）| 必读 ≥5 | **PASS** |
| 建议读 | 17 | — | — |
| 待确认 | 4 | — | — |
| 备选 | 57 | — | — |
| 排除 | 121 | — | — |
| 覆盖 ≥2 机制不同子方向 | F1 鲁棒/CSI-AMC、F2 HARQ-IR+速率、F3 自适应调制+功率、F4 相干物理 AMC，共 4 机制不同族 | ≥2 | **PASS** |
| 无明显空洞 | **有空洞**（见下）| — | **PARTIAL** |

**空洞（§5 Q8 相关）**：
- **0 篇**直接竞品 = "coherent sat-ground FSO + Gamma-Gamma + AMC/MCS + 真实 coded chain + 信息不确定性" 四要素齐全。最接近的 L124（physics-informed adaptive transmission for coherent FSO）摘要偏 6G 通用框架，是否真做星地 GG + coded AMC 待 Step 2 验证；L165 是 feeder link 实验 demo 但 adaptive 动作在 AO 层非 AMC。
- 中文检索 38 条中**有摘要的 0 条**（CNKI cookie/IP 受限，摘要未抓取），全部低 confidence，仅 5 条（L050/L206/L181/L186/L197）标题强相关，需 Step 2 抓全文才能定性。
- 轴 A（coded-goodput/MCS/PS）下"FEC + 概率整形 + AMC"在 GG 湍流星地相干链的直接文献稀薄，PS+FSO 多为 IM/DD 单链分析。

---

## §3 逐条语义审查（209 条全表）

**字段**：`L | pri(必读/建议读/待确认/备选/排除) | true_topic | axis(A/B/C/none) | comp(direct/adjacent/none) | year/venue/cited | title | 排除理由`

**true_topic 枚举**：coherent-FSO-AMC / IM/DD-FSO-AMC / hybrid-FSO/RF-AMC / RF-NTN-AMC / automatic-modulation-CLASSIFICATION / FSO-channel-analysis / FSO-other / unrelated / chinese-FSO-AMC

**排除规则执行**：mod-classification 一律排除（5 条：L087 MFI survey / L188 OAM 模式识别 / L184 涡旋双任务识别 / L207 双参数反演 / L070 borderline demod）；纯 RF/NTN IRS/RIS/NOMA 无 FSO 关联排除（可迁移数学的标 adjacent 备选）；纯容量/BER 分析无 adaptive 动作降级备选；hybrid FSO/RF link-switching 标 adjacent。

### 批次 1（1–70，按 pri→L 排序）

| L | pri | true_topic | axis | comp | year/venue/cited | title | 排除理由 |
|---|---|---|---|---|---|---|---|
| L018 | 必读 | IM/DD-FSO-AMC | B | direct | 2017/elib (DLR)/c6 | Adaptive HARQ with Channel State Information in Inter-HAP FSO Links | — |
| L023 | 必读 | IM/DD-FSO-AMC | C | direct | 2023/JLT/c35 | Adaptive Transceiver Design for High-Capacity Multi-Modal FSO With Commercial Devices and Atmospheric Turbulence | — |
| L050 | 必读 | chinese-FSO-AMC | A | direct | 2026/空间电子技术/c0 | DFT-SAMP信道估计与概率整形联合优化的FSO系统 | — |
| L073 | 必读 | IM/DD-FSO-AMC | C | direct | 2025/Entropy/c0 | HARQ Performance Limits for Free-Space Optical Communication Systems | — |
| L096 | 必读 | IM/DD-FSO-AMC | C | direct | 2021/IEEE TVT/c25 | On the Design of FSO-Based Satellite Systems Using IR Hybrid ARQ Protocols With Rate Adaptation | — |
| L097 | 必读 | hybrid-FSO/RF-AMC | A | direct | 2021/IEEE photonics j/c67 | On the Design of Rate Adaptation for Relay-Assisted Satellite Hybrid FSO/RF Systems | — |
| L124 | 必读 | coherent-FSO-AMC | A | direct | 2026/—/c0 | Physics-informed adaptive transmission for coherent FSO: multi-dim amplitude–phase statistics | — |
| L126 | 必读 | hybrid-FSO/RF-AMC | C | direct | 2022/Photonics/c9 | Power Allocation for Reliable and Energy-Efficient Optical LEO-to-Ground Downlinks with HARQ | — |
| L165 | 必读 | coherent-FSO-AMC | A | direct | 2023/LSA/c109 | Tbit/s line-rate satellite feeder links enabled by coherent modulation and full-adaptive optics | — |
| L206 | 必读 | chinese-FSO-AMC | C | direct | 2026/空间电子技术/c0 | 面向快衰落信道的三维概率整形FSO系统研究 | — |
| L007 | 建议读 | hybrid-FSO/RF-AMC | C | adjacent | 2023/Photonics/c8 | A Hybrid mmW+FSO Architecture with Adaptive Diversity Combining and HARQ | — |
| L020 | 建议读 | IM/DD-FSO-AMC | A | adjacent | 2019/—/c0 | Adaptive Modulation Schemes for High-Capacity Free-Space Optics Communications | — |
| L024 | 建议读 | hybrid-FSO/RF-AMC | C | adjacent | 2021/IEEE Access/c83 | Adaptive-Combining-Based Hybrid FSO/RF Satellite Communication With and Without HAPS | — |
| L038 | 建议读 | chinese-FSO-AMC | A | adjacent | 2026/—/c0 | Channel estimation and adaptive coding dynamic control algorithm for satellite laser comm | — |
| L041 | 建议读 | hybrid-FSO/RF-AMC | C | adjacent | 2023/IEEE Access/c3 | Cooperative HARQ-Aided Multiple UAVs in Optical Aerospace Backhaul Networks | — |
| L075 | 建议读 | IM/DD-FSO-AMC | A | direct | 2026/—/c3 | Hybrid deep learning-based adaptive modulation for FSO communication | — |
| L083 | 建议读 | RF-NTN-AMC | B | adjacent | 2023/JSAC/c9 | Link Adaptation for Rate Splitting Systems With Partial CSIT | — |
| L112 | 建议读 | hybrid-FSO/RF-AMC | C | adjacent | 2018/IEEE photonics j/c162 | Performance Analysis of Hybrid FSO Systems Using FSO/RF-FSO Link Adaptation | — |
| L146 | 建议读 | hybrid-FSO/RF-AMC | B | adjacent | 2025/—/c5 | Robust joint opt for efficient and reliable FSO/RF satellite-UAV-terrestrial with imperfect channel | — |
| L159 | 建议读 | IM/DD-FSO-AMC | C | adjacent | 2025/—/c1 | Spectral-spatial coding and turbulence-aware modulation for dense WDM hybrid MIMO-RF FSO | — |
| L173 | 建议读 | IM/DD-FSO-AMC | A | adjacent | 2025/—/c10 | WDM-PON FSO system utilizing LDPC decoding for enhanced cellular C-RAN fronthaul | — |
| L181 | 建议读 | chinese-FSO-AMC | none | adjacent | 2026/光通信技术/c0 | 基于QC-LDPC编码的大气湍流光通信仿真与实验研究 | — |
| L183 | 建议读 | RF-NTN-AMC | C | adjacent | 2026/通信学报/c0 | 基于元深度强化学习的蜂窝网链路自适应方法 | — |
| L186 | 建议读 | chinese-FSO-AMC | C | adjacent | 2026/光学学报/c0 | 基于整形与结构化空间耦合准循环码的星地激光传输方案 | — |
| L195 | 建议读 | RF-NTN-AMC | C | adjacent | 2026/西安邮电大学学报/c0 | 强化学习驱动的低空无人机自适应调制编码方案 | — |
| L197 | 建议读 | chinese-FSO-AMC | none | adjacent | 2026/计算机测量与控制/c0 | 星地激光通信RS-LDPC级联码抗干扰优化 | — |
| L199 | 建议读 | chinese-FSO-AMC | A | adjacent | 2026/光通信研究/c0 | 稀疏双模索引调制光OTFS系统设计与性能分析 | — |
| L003 | 待确认 | chinese-FSO-AMC | C | adjacent | 2026/移动通信/c0 | 5G-LDPC码编码调制重传的交织优化 | — |
| L108 | 待确认 | RF-NTN-AMC | B | adjacent | 2021/—/c71 | Outage-constrained robust beamforming for IRS-aided wireless communication | — |
| L154 | 待确认 | IM/DD-FSO-AMC | C | adjacent | 2025/—/c14 | Self-adaptive all-optical feedback FSO with attention-enhanced turbulence awareness | — |
| L158 | 待确认 | coherent-FSO-AMC | none | adjacent | 2020/JLT/c36 | Space-Ground Coherent Optical Links: Ground Receiver With Adaptive Optics and Digital PLL | — |
| L001 | 备选 | FSO-other | none | none | 2023/—/c11 | 10 Gbauds digital optical link and analog link from/to GEO satellite | — |
| L006 | 备选 | RF-NTN-AMC | A | adjacent | 2025/—/c10 | SLR on AI for error correction and modulation schemes in next-gen satellite comms | — |
| L008 | 备选 | FSO-channel-analysis | none | none | 2020/Alexandria Eng J/c48 | A long-haul 100 Gbps hybrid PDM/CO-OFDM FSO: climate + turbulence impact | — |
| L009 | 备选 | FSO-channel-analysis | none | none | 2023/Int J Optics/c11 | MIMO-Enabled FSO Link under Log-Normal/Gamma-Gamma: optimal modulation scheme | — |
| L025 | 备选 | FSO-other | none | none | 2019/—/c5 | Advanced adaptive compensation system for free-space optical communications | — |
| L034 | 备选 | RF-NTN-AMC | B | adjacent | 2024/IEEE OJ-COMS/c7 | Bandit-Based Learning-Aided FD/HD Mode Selection in 6G Cooperative Relay (statistical CSI) | — |
| L037 | 备选 | FSO-other | none | none | 2025/—/c9 | Challenges and opportunities in free space optical satellite communication | — |
| L039 | 备选 | FSO-channel-analysis | none | none | 2024/—/c7 | Coded-optical improved quadrature spatial modulation over Gamma–Gamma strong turbulence | — |
| L040 | 备选 | FSO-other | none | none | 2024/IET Optoelectronics/c120 | Coding techniques for diversity enhancement of DWDM MIMO-FSO fault protection | — |
| L046 | 备选 | RF-NTN-AMC | B | adjacent | 2018/—/c93 | Delay performance of wireless comms with imperfect CSI and finite-length coding | — |
| L056 | 备选 | FSO-other | none | none | 2021/LNICST/c4 | End-to-End Error Control Coding of NB-IoT in GEO Satellite with Time-Packed Optical Feeder | — |
| L057 | 备选 | FSO-other | none | none | 2022/JLT/c38 | Enhanced Atmospheric Turbulence Resiliency With SIC DSP in MDM-FSO Links | — |
| L058 | 备选 | RF-NTN-AMC | B | adjacent | 2019/—/c17 | Enhanced receiver based on FEC code constraints for uplink NOMA with imperfect CSI | — |
| L059 | 备选 | FSO-channel-analysis | none | none | 2022/IEEE photonics j/c36 | Ergodic Capacity Analysis of Satellite Comm with SAG-FSO/SH-FSO/RF | — |
| L066 | 备选 | FSO-other | none | none | 2020/J Opt Commun/c54 | Free space optics communication system design using iterative optimization | — |
| L068 | 备选 | IM/DD-FSO-AMC | A | adjacent | 2018/IEEE photonics j/c26 | Free-Space Optical Comm Using Coherent Detection and Double Adaptive Detection Thresholds | — |
| L069 | 备选 | FSO-other | none | none | 2022/—/c2 | From fibers to satellites: lessons when optical comms move to long distance free space | — |
| L070 | 备选 | automatic-modulation-CLASSIFICATION | none | none | 2026/光通信技术/c0 | FSO通信系统中AI辅助调制与解调技术的研究进展 | borderline demod/AI-mod survey，靠 classification 边缘 |
| L072 | 备选 | hybrid-FSO/RF-AMC | C | adjacent | 2021/IEEE TAES/c215 | HAPS-Based Relaying for Integrated Space–Air–Ground Networks With Hybrid FSO/RF | — |
| L078 | 备选 | FSO-other | none | none | 2024/Opt Quantum Electron/c84 | OFDM UAV-based FSO with scintillation mitigation | — |
| L080 | 备选 | FSO-channel-analysis | none | none | 2021/IEEE photonics j/c42 | Level Crossing Rate and Average Fade Duration of Satellite-to-UAV FSO Channels | — |
| L081 | 备选 | hybrid-FSO/RF-AMC | none | adjacent | 2026/PLoS ONE/c3 | Line-of-sight stability in UAV relays for hybrid FSO/VLC links | — |
| L084 | 备选 | FSO-channel-analysis | none | none | 2024/—/c0 | Link Handling Due to Atmospheric Turbulence in FSO for Optical Wireless Terrestrial Networks | — |
| L085 | 备选 | FSO-other | none | none | 2022/—/c3 | Link-Layer Retransmission-based Error-Control Protocols in FSO: A Survey | — |
| L090 | 备选 | FSO-other | none | none | 2019/—/c1 | Mitigating Turbulence-Induced Fading in Coherent FSO: An Adaptive Space-Time Code | — |
| L093 | 备选 | hybrid-FSO/RF-AMC | none | adjacent | 2026/LNEE/c2 | Next-Gen IoT Connectivity: FSO-RF Integration with HAPs | — |
| L094 | 备选 | RF-NTN-AMC | B | adjacent | 2025/Int J Comm Syst/c2 | NOMA-Based Satellite-UAV-Terrestrial With Partial Relay and Imperfect CSI/SIC | — |
| L095 | 备选 | RF-NTN-AMC | B | adjacent | 2020/—/c57 | NOMA for hybrid VLC-RF networks with imperfect channel state information | — |
| L099 | 备选 | RF-NTN-AMC | C | none | 2023/Entropy/c5 | On the Secure Performance of IRS-Assisted HARQ Systems | — |
| L100 | 备选 | RF-NTN-AMC | C | adjacent | 2019/IEEE Access/c20 | Throughput of TCP Cubic in mmWave with IR-HARQ + AMC | — |
| L101 | 备选 | FSO-other | none | none | 2019/ICSO 2018/c10 | Optical feeder link architectures for very HTS: issues and possibilities | — |
| L104 | 备选 | hybrid-FSO/RF-AMC | C | adjacent | 2025/EAI/c1 | Optimizing UAV Trajectories in Optical IRS-Aided Hybrid FSO/RF AAN via DRL | — |
| L109 | 备选 | FSO-other | none | none | 2018/—/c29 | Performance analysis of LDPC coded OAM-UCA FSO with linear equalization + channel est | — |
| L110 | 备选 | FSO-other | none | none | 2022/—/c31 | Performance of spatial diversity coherent FSO with optimal branch block phase correction | — |
| L111 | 备选 | FSO-channel-analysis | none | none | 2023/Opt Quantum Electron/c3 | Performance of coherent DPSK SIMO laser sat-ground link over weak-to-strong turbulence | — |
| L113 | 备选 | hybrid-FSO/RF-AMC | none | adjacent | 2022/—/c4 | Performance Analysis of Hybrid SAG-FSO/RF Satellite Communication System | — |
| L114 | 备选 | hybrid-FSO/RF-AMC | C | adjacent | 2024/Photonics/c3 | Performance of Parallel FSO/RF Transmissions in SAGIN with Power Allocation | — |
| L115 | 备选 | FSO-channel-analysis | none | none | 2026/—/c0 | Performance Analysis of Space Satellite Comm Based on Single-Photon Detectors | — |
| L116 | 备选 | FSO-other | none | none | 2019/IEEE Access/c188 | Performance Enhancement of OAM-Multiplexed FSO Using Spatial-Mode Multiplexing + Adaptive MIMO Equalization | — |

### 批次 2（71–140）

| L | pri | true_topic | axis | comp | year/venue/cited | title | 排除理由 |
|---|---|---|---|---|---|---|---|
| L117 | 备选 | IM/DD-FSO-AMC | none | none | 2021/Photonics/c44 | Performance Enhancement of DWDM-FSO Based on Hybrid Modulation under Turbulence | — |
| L118 | 备选 | FSO-other | none | none | 2023/Appl Sci/c14 | Performance Monitoring of Hybrid All-Optical Fiber/FSO Communication Systems | — |
| L119 | 备选 | FSO-channel-analysis | none | none | 2023/Photonics/c2 | Performance of HQAM/XQAM Laser Comm in Anisotropic Non-Kolmogorov Ground–HAP–Satellite | — |
| L120 | 备选 | FSO-channel-analysis | none | none | 2020/—/c2 | Performance of Multibeam VHTS Based on FSO Feeder Links with HPA Nonlinearity | — |
| L121 | 备选 | FSO-channel-analysis | none | none | 2019/—/c20 | Performance of OFDM-FSO with Different Modulation Schemes over Gamma-Gamma Turbulence | — |
| L122 | 备选 | hybrid-FSO/RF-AMC | none | adjacent | 2021/arXiv/c0 | Performance of UAV-assisted Multiuser Terrestrial-Satellite over Mixed FSO/RF | — |
| L128 | 备选 | FSO-other | none | none | 2024/Opt Express/c11 | Pre-distortion adaptive optics for optical feeder links: simulations and analyses | — |
| L130 | 备选 | FSO-other | none | none | 2021/—/c18 | Recent trends in coherent free-space optical communications | — |
| L134 | 备选 | FSO-other | A | none | 2026/—/c11 | Review on modulation formats and channel coding in FSO: selection criteria | — |
| L136 | 备选 | hybrid-FSO/RF-AMC | C | adjacent | 2023/IEEE photonics j/c34 | RIS Assisted UAV for Weather-Dependent Satellite Terrestrial Integrated With Hybrid FSO/RF | — |
| L144 | 备选 | RF-NTN-AMC | B | adjacent | 2018/EURASIP JWCN/c8 | Robust full-dimension MIMO transmission based on limited feedback angular-domain CSIT | — |
| L145 | 备选 | FSO-other | A | adjacent | 2026/—/c3 | Robust high-capacity FSO using OAM-based structured light + intelligent adaptive signal processing | — |
| L157 | 备选 | hybrid-FSO/RF-AMC | none | adjacent | 2021/IEEE Access/c4 | Site Diversity in Downlink Optical Satellite Networks Through Ground Station Selection | — |
| L164 | 备选 | FSO-other | none | none | 2023/IEEE TMLCN/c15 | Symbol Detection and Channel Estimation for Space Optical Comm Using NN and Autoencoder | — |
| L168 | 备选 | FSO-other | none | none | 2021/ICSO 2020/c26 | The H2020 VERTIGO project towards tbit/s optical feeder links | — |
| L171 | 备选 | FSO-other | none | none | 2025/—/c2 | Turbulence mitigation in FSO based on turbo coding and equalization | — |
| L180 | 备选 | FSO-other | none | none | 2026/中国激光/c0 | 厄米-高斯模式缺陷态空域并行检测与信息解码（特邀） | — |
| L202 | 备选 | FSO-other | none | none | 2026/光学学报/c0 | 语义光通信：从地面到空天（特邀） | — |
| L002 | 排除 | FSO-other | none | none | 2026/光学与光电技术/c0 | 10 km 1 Gbps APT FSO for power line | APT/pointing, no AMC |
| L004 | 排除 | RF-NTN-AMC | none | none | 2026/中国宽带/c0 | 5G无线通信网络中高频段传输损耗补偿算法研究 | RF only |
| L005 | 排除 | RF-NTN-AMC | none | none | 2020/IEEE Access/c1363 | 6G and Beyond: The Future of Wireless Communications Systems | 6G survey |
| L010 | 排除 | RF-NTN-AMC | A | none | 2026/—/c0 | Quality-Driven ACM Framework for DVB over Satellite | DVB RF, no FSO |
| L011 | 排除 | hybrid-FSO/RF-AMC | none | none | 2022/Entropy/c72 | Survey of Hybrid FSO Communication Networks for 5G Backhauling | hybrid FSO survey |
| L012 | 排除 | RF-NTN-AMC | none | none | 2021/IEEE Access/c135 | Survey on Deep Learning for URLLC on 6G | URLLC 6G survey |
| L013 | 排除 | hybrid-FSO/RF-AMC | none | none | 2025/Sensors/c17 | Survey on FSO Communication with RF Backup | FSO+RF backup survey |
| L014 | 排除 | hybrid-FSO/RF-AMC | none | none | 2019/—/c7 | Survey on Recent Work in Hybrid FSO/RF Communication Link | hybrid FSO/RF survey |
| L015 | 排除 | unrelated | none | none | 2021/IEEE Access/c201 | Techno-Economic Framework for LEO Constellations (Starlink/OneWeb) | unrelated to AMC |
| L016 | 排除 | RF-NTN-AMC | A | none | 2026/—/c0 | Adaptive Coded Modulation Assisted ISAC Based AFDM in SAGIN | AFDM RF, not FSO |
| L017 | 排除 | RF-NTN-AMC | C | none | 2025/—/c7 | Adaptive coding and modulation for sun outage in ultra-dense LEO (DRL) | RF LEO; ISL/deterministic dead-end#1 risk |
| L019 | 排除 | RF-NTN-AMC | A | none | 2025/—/c3 | Adaptive modulation and coding techniques for next-gen wireless | generic wireless, no FSO |
| L021 | 排除 | FSO-other | none | none | 2022/Opto-Electron Adv/c169 | Adaptive optics based on machine learning: a review | AO not AMC |
| L022 | 排除 | FSO-other | none | none | 2021/Nat Rev Methods Primers/c294 | Adaptive optics for high-resolution imaging | AO not AMC |
| L026 | 排除 | RF-NTN-AMC | none | none | 2025/—/c0 | Advancements in Satellite Comm Systems for High-Throughput Earth Stations | NGSO RF |
| L027 | 排除 | unrelated | none | none | 2023/Annu Rev Astron Astrophys/c48 | Advances in Optical/Infrared Interferometry | astronomy |
| L028 | 排除 | FSO-other | none | none | 2021/IET Quantum Comm/c258 | Advances in space quantum communications | quantum survey |
| L029 | 排除 | FSO-other | none | none | 2025/—/c0 | Comprehensive Review of Trends and Opportunities in FSO | FSO trends survey, no AMC |
| L030 | 排除 | FSO-other | none | none | 2025/—/c0 | AI/ML-Enhanced Inter-Satellite OWC and Fiber for 5G/6G | survey, no AMC |
| L031 | 排除 | FSO-other | none | none | 2021/JLT/c42 | Empirical Comparison of Modulation Schemes in Turbulent Underwater OWC | underwater, not sat-ground |
| L032 | 排除 | FSO-other | none | none | 2024/—/c0 | Analogue Homodyne Coherent Optical Receiver for Ground to Satellite | QKD context, no AMC |
| L033 | 排除 | FSO-other | none | none | 2024/New J Phys/c31 | Analysis of satellite-to-ground QKD with adaptive optics | AO+QKD, not AMC |
| L035 | 排除 | FSO-other | none | none | 2022/JLT/c89 | Bridging the Terahertz Gap: Photonics-Assisted Free-Space Communications | THz, not AMC |
| L036 | 排除 | unrelated | none | none | 2020/Physiol Rev/c339 | Cellular Circuits in the Brain and Pain | totally unrelated |
| L042 | 排除 | FSO-other | none | none | 2026/—/c5 | Current status and development trend of satellite laser communication | survey, no AMC |
| L043 | 排除 | unrelated | none | none | 2022/LSA/c673 | Deep learning in optical metrology: a review | metrology |
| L044 | 排除 | FSO-other | none | none | 2023/Electronics/c5 | Deep Learning-Based Small Target Detection for Satellite–Ground FSO | acquisition/pointing |
| L045 | 排除 | RF-NTN-AMC | B | none | 2023/—/c7 | DRL for improving resource utilization of URLLC with imperfect CSI | RF URLLC |
| L047 | 排除 | FSO-other | none | none | 2024/—/c20 | Demonstration of coherent beam combining for atmospheric FSO | AO/hardware, not AMC |
| L048 | 排除 | FSO-other | none | none | 2021/IEEE photonics j/c76 | Design and Analysis of High-Speed FSO for 5G in India | analysis, no AMC |
| L049 | 排除 | unrelated | none | none | 2021/Proc IEEE/c406 | Developments in Video Coding Standardization (VVC) | video coding |
| L051 | 排除 | unrelated | none | none | 2021/Opt Switch Netw/c81 | Disaster resilience of optical networks | disaster, unrelated |
| L052 | 排除 | unrelated | none | none | 2025/—/c59 | Distributed satellite information networks: Architecture and trends | no FSO AMC |
| L053 | 排除 | RF-NTN-AMC | none | none | 2022/Sensors/c85 | Dynamic Routings in Satellite Networks: An Overview | routing, RF |
| L054 | 排除 | RF-NTN-AMC | B | none | 2025/—/c4 | EE maximization with imperfect CSI in BackCom NOMA | RF BackCom |
| L055 | 排除 | unrelated | none | none | 2024/Nat Commun/c307 | Emerging opportunities for reservoir computing | unrelated |
| L060 | 排除 | unrelated | none | none | 2023/Biomed Opt Express/c82 | Evolution of adaptive optics retinal imaging | unrelated (AO imaging) |
| L061 | 排除 | RF-NTN-AMC | none | none | 2025/—/c19 | Evolution of satellite communication systems toward 5G/6G | RF satcomm survey |
| L062 | 排除 | FSO-other | none | none | 2021/npj Quantum Inf/c119 | Feasibility of satellite-to-ground CV-QKD | QKD |
| L063 | 排除 | FSO-other | none | none | 2019/—/c13 | Free space optical communication and laser beam propagation: survey | survey, no AMC |
| L064 | 排除 | FSO-other | none | none | 2025/—/c4 | Free space optical communication and network architecture | survey, no AMC |
| L065 | 排除 | FSO-other | none | none | 2023/Photonics/c46 | Free Space Optical Communication: Enabling Backhaul for 6G NTN | survey |
| L067 | 排除 | FSO-other | none | none | 2026/—/c0 | Free-Space Optical Communication for High-Capacity Satellite Links | survey, no AMC |
| L071 | 排除 | unrelated | none | none | 2019/Remote Sens Environ/c337 | Half a century of satellite remote sensing of sea-surface temperature | totally unrelated |
| L074 | 排除 | unrelated | none | none | 2025/—/c0 | How may signal loss be decreased and encryption improved by quantum entanglement | unrelated |
| L076 | 排除 | RF-NTN-AMC | none | none | 2022/JSAC/c3197 | Integrated Sensing and Communications: Toward Dual-Functional 6G | ISAC survey |
| L077 | 排除 | RF-NTN-AMC | none | none | 2025/—/c3 | Intelligent spectrum management in satellite communications | RF spectrum |
| L079 | 排除 | unrelated | none | none | 2025/—/c0 | IT and Telecommunications Department | book, unrelated |
| L082 | 排除 | RF-NTN-AMC | B | none | 2018/—/c26 | Linear precoding for MU-MISO VLC with noisy CSI | VLC/RF precoding |
| L086 | 排除 | RF-NTN-AMC | none | none | 2023/IEEE COMST/c245 | Low Earth Orbit Satellite Security and Reliability | LEO security survey |
| L087 | 排除 | automatic-modulation-CLASSIFICATION | none | none | 2020/IEEE COMST/c129 | ML Techniques for Optical Performance Monitoring and Modulation Format Identification | MFI = classification, EXCLUDE |
| L088 | 排除 | RF-NTN-AMC | B | none | 2024/—/c13 | Massive wireless energy transfer without CSI via imperfect IRS | RF energy transfer |

### 批次 3（141–209）

| L | pri | true_topic | axis | comp | year/venue/cited | title | 排除理由 |
|---|---|---|---|---|---|---|---|
| L089 | 排除 | RF-NTN-AMC | none | none | 2019/IEEE Access/c61 | Mission-Critical Machine-Type Communication: Overview | MTC overview |
| L091 | 排除 | FSO-other | none | none | 2026/—/c4 | Model-free adaptive optics for FSO: a comprehensive survey | AO not AMC |
| L092 | 排除 | unrelated | none | none | 2023/Materials/c74 | Multifunctional Integration of Optical Fibers and Nanomaterials for Aircraft | unrelated |
| L098 | 排除 | RF-NTN-AMC | B | none | 2024/—/c28 | Uplink power-domain NOMA with imperfect CSI and SIC in 6G | RF NOMA |
| L102 | 排除 | FSO-other | none | none | 2022/Opto-Electron Adv/c163 | Optical multiplexing techniques review | multiplexing review |
| L103 | 排除 | FSO-other | none | none | 2020/IEEE COMST/c344 | Optical Wireless Hybrid Networks: Trends and Directions | OWC hybrid survey |
| L105 | 排除 | FSO-other | none | none | 2021/Nanophotonics/c343 | Orbital angular momentum and beyond in free‐space optical communications | OAM review |
| L106 | 排除 | RF-NTN-AMC | B | none | 2023/—/c28 | Outage constrained robust transmission for IRS-aided secure comms | RF IRS |
| L107 | 排除 | RF-NTN-AMC | B | none | 2024/—/c1 | Outage constrained transmit optimization for spatially correlated RIS MIMO | RF RIS |
| L123 | 排除 | RF-NTN-AMC | B | none | 2022/—/c19 | Physical layer security in OFDM time reversal SISO with imperfect CSI | RF PLS |
| L125 | 排除 | RF-NTN-AMC | none | none | 2021/IEEE OJ-COMS/c149 | Point-to-Point Communication in Integrated Satellite-Aerial 6G | P2P survey |
| L127 | 排除 | FSO-other | none | none | 2025/—/c2 | Pre-distortion adaptive optics for FSO | AO not AMC |
| L129 | 排除 | unrelated | none | none | 2019/IEEE Access/c653 | Quantum Machine Learning for 6G Communication Networks | quantum ML survey |
| L131 | 排除 | FSO-other | none | none | 2020/IEEE Access/c73 | Relay-Assisted Technology in Optical Wireless Communications: A Survey | relay survey |
| L132 | 排除 | hybrid-FSO/RF-AMC | none | none | 2021/arXiv/c0 | Retrofitting FSO Systems in Existing RF Infrastructure: Non-Zero Sum Game | dup of L133 preprint |
| L133 | 排除 | hybrid-FSO/RF-AMC | none | none | 2021/IEEE OJ-COMS/c2 | Retrofitting FSO Systems in Existing RF Infrastructure: Non-Zero-Sum Game | game theory, no AMC mechanism |
| L135 | 排除 | FSO-other | none | none | 2024/Sensors/c70 | Revolutionizing Free-Space Optics: Survey of Enabling Technologies | FSO survey (dup fam L176) |
| L137 | 排除 | FSO-other | none | none | 2024/IEEE COMST/c100 | RIS-Assisted Physical Layer Security in RF and Optical Wireless | RIS PLS survey |
| L138 | 排除 | FSO-other | none | none | 2019/J Opt/c203 | Roadmap on all-optical processing | all-optical roadmap |
| L139 | 排除 | FSO-other | none | none | 2024/J Opt/c97 | Roadmap on optical communications | broad survey, no AMC |
| L140 | 排除 | RF-NTN-AMC | B | none | 2022/—/c13 | Robust and outage-constrained EE optimization in RIS-assisted NOMA | RF RIS NOMA |
| L141 | 排除 | RF-NTN-AMC | B | none | 2023/—/c26 | Robust beamforming for IRS-aided NOMA with CSI uncertainty | RF IRS NOMA |
| L142 | 排除 | RF-NTN-AMC | B | none | 2024/—/c18 | Robust beamforming for integrated sensing and communication | RF ISAC |
| L143 | 排除 | RF-NTN-AMC | B | none | 2025/—/c17 | Robust communication design in RIS-assisted THz channels | RF RIS THz |
| L147 | 排除 | RF-NTN-AMC | B | none | 2021/—/c31 | Robust power allocation in covert communication: Imperfect CDI | RF covert |
| L148 | 排除 | RF-NTN-AMC | B | none | 2025/—/c4 | Robust secure resource optimization for RIS-aided backscatter with HWIs | RF RIS BackCom |
| L149 | 排除 | RF-NTN-AMC | none | none | 2020/IEEE COMST/c1382 | Satellite Communications in the New Space Era: A Survey | satcom survey |
| L150 | 排除 | RF-NTN-AMC | none | none | 2023/IEEE Access/c69 | Satellite Swarm-Based Antenna Arrays for 6G Direct-to-Cell | RF antenna arrays |
| L151 | 排除 | RF-NTN-AMC | none | none | 2022/Comput Netw/c165 | Satellite-based communications security: A survey | satcom security survey |
| L152 | 排除 | FSO-other | none | none | 2018/IEEE COMST/c166 | Satellite-Based Continuous-Variable Quantum Communications | CV-QKD survey |
| L153 | 排除 | FSO-other | none | none | 2024/arXiv/c0 | Secrecy Performance Analysis of Space-to-Ground Optical Satellite | PLS, not AMC |
| L155 | 排除 | unrelated | none | none | 2021/IEEE Access/c87 | SWIPT With Cooperative Relaying: A Review | SWIPT review |
| L156 | 排除 | RF-NTN-AMC | B | none | 2020/—/c20 | SINR-outage minimization of robust beamforming for non-orthogonal downlink | RF beamforming |
| L160 | 排除 | RF-NTN-AMC | none | none | 2023/IEEE OJ-COMS/c116 | Spectrum Options and Allocations for 6G: Regulatory Review | RF spectrum |
| L161 | 排除 | FSO-other | none | none | 2022/Commun Phys/c30 | Statistical verifications and DL predictions for satellite-to-ground quantum channels | quantum |
| L162 | 排除 | FSO-other | none | none | 2020/IEEE JSTQE/c170 | Structured Light in Turbulence | structured light review |
| L163 | 排除 | FSO-other | none | none | 2020/Prog Quantum Electron/c60 | Survey of energy-autonomous solar cell receivers for SAGO OWC | solar cell survey |
| L166 | 排除 | hybrid-FSO/RF-AMC | none | none | 2021/IEEE Access/c28 | TCP Performance Over Satellite-Based Hybrid FSO/RF Vehicular Networks | transport layer |
| L167 | 排除 | FSO-other | none | none | 2022/IEEE COMST/c482 | The Evolution of Quantum Key Distribution Networks: Qinternet | QKD survey |
| L169 | 排除 | RF-NTN-AMC | none | none | 2020/Sci China Inf Sci/c1960 | Towards 6G wireless communication networks: vision | 6G survey |
| L170 | 排除 | FSO-other | none | none | 2025/—/c5 | Towards 6G: review of optical transport challenges for intelligent comms | survey, no AMC |
| L172 | 排除 | RF-NTN-AMC | none | none | 2021/IEEE Access/c127 | URLLC for 5G and Beyond: Requirements and Enabling Technologies | URLLC survey |
| L174 | 排除 | FSO-other | none | none | 2023/IEEE Access/c101 | Wireless and Optical Convergent Access Technologies Toward 6G | convergent access survey |
| L175 | 排除 | RF-NTN-AMC | none | none | 2019/IEEE Access/c2515 | Wireless Communications and Applications Above 100 GHz for 6G | THz survey |
| L176 | 排除 | FSO-other | none | none | 2024/—/c105 | …free-space optics: Survey of enabling technologies for beyond 5G FSO | FSO survey (dup fam L135) |
| L177 | 排除 | FSO-other | none | none | 2026/光通信研究/c0 | 专利视角下卫星激光通信技术发展研究 | patent review |
| L178 | 排除 | unrelated | none | none | 2026/自动化仪表/c0 | 具备链路诊断功能和通信周期自适应机制的现场总线设计 | fieldbus, unrelated |
| L179 | 排除 | FSO-channel-analysis | none | none | 2026/大气与环境光学学报/c0 | 利用测风激光雷达对近海岸边界层光学湍流特性的研究 | channel measurement |
| L182 | 排除 | RF-NTN-AMC | none | none | 2026/现代电子技术/c0 | 基于业务优先级的星载VDES时隙分配算法 | RF resource alloc |
| L184 | 排除 | automatic-modulation-CLASSIFICATION | none | none | 2026/光学学报/c0 | 基于动态权重的涡旋光束斜程传输双任务识别 | pattern recognition, EXCLUDE |
| L185 | 排除 | unrelated | none | none | 2026/音视频工程与应用/c0 | 基于声频感知技术的应急广播全域覆盖接收优化设计 | broadcasting |
| L187 | 排除 | FSO-other | none | none | 2026/光学学报/c0 | 基于本振光编码的后调制多模相干探测鬼成像激光雷达的研究 | lidar imaging |
| L188 | 排除 | automatic-modulation-CLASSIFICATION | none | none | 2026/光子学报/c0 | 基于深度学习算法的针状光束增强湍流大气中OAM模式识别 | mod classification/recognition, EXCLUDE |
| L189 | 排除 | FSO-other | none | none | 2026/激光与光电子学进展/c0 | 基于粒子群优化算法的多环变迹镜优化设计 | optics design |
| L190 | 排除 | unrelated | none | none | 2026/科学技术与工程/c0 | 基于蒙特卡洛方法的紫外光波长特性仿真与实验验证 | UV, not FSO IR |
| L191 | 排除 | FSO-channel-analysis | none | none | 2026/大气与环境光学学报/c0 | 基于融合模型估算沿海地区大气光学湍流廓线的研究 | channel measurement, no AMC |
| L192 | 排除 | unrelated | none | none | 2026/计算物理/c0 | 声波作用下的边界层流场及功率谱特性研究 | fluid, unrelated |
| L193 | 排除 | FSO-other | none | none | 2026/激光与光电子学进展/c0 | 复杂湍流下基于DBSCAN与PSO优化的质心定位算法研究 | pointing/centroid |
| L194 | 排除 | unrelated | none | none | 2026/电光与控制/c1 | 多维相位编码调制的可重构MIMO SAR方案 | SAR radar |
| L196 | 排除 | unrelated | none | none | 2026/今日消防/c0 | 强台风灾害条件下消防应急通信可靠性提升策略 | emergency comms |
| L198 | 排除 | unrelated | none | none | 2026/探测与控制学报/c0 | 相位编码调制线性调频连续波无线电引信抗干扰方法 | fuse |
| L200 | 排除 | FSO-other | none | none | 2026/应用光学/c0 | 考虑多波段偏振的星地激光通信系统终端后向杂散光抑制方法 | stray light, no AMC |
| L201 | 排除 | unrelated | none | none | 2026/中国科技信息/c0 | 让智能家居不再"掉线"：AI算法如何让通信链路学会自适应 | pop sci |
| L203 | 排除 | unrelated | none | none | 2026/广播与电视技术/c0 | 调频广播附加信道授时发射的设计和验证 | broadcasting |
| L204 | 排除 | unrelated | none | none | 2026/通讯世界/c0 | 隐蔽通信中的编码、调制和多址技术研究 | covert comms |
| L205 | 排除 | FSO-other | none | none | 2026/通信世界/c0 | 面向6G全域泛在通信的空天地一体化光网络综述 | survey |
| L207 | 排除 | automatic-modulation-CLASSIFICATION | none | none | 2026/光学学报/c0 | 面向畸变涡旋光束的湍流强度与传播距离双参数联合反演模型 | parameter inversion, EXCLUDE |
| L208 | 排除 | RF-NTN-AMC | none | none | 2026/电视电声科学与技术/c0 | 高山微波传输链路衰落信道建模与多维抗干扰策略 | microwave RF |
| L209 | 排除 | FSO-other | none | none | 2026/光通信技术/c0 | 高速可见光通信关键技术 | VLC, not FSO |

**Triage 汇总**：必读 10 / 建议读 17 / 待确认 4 / 备选 57 / 排除 121。direct competitor 11（其中 coherent-FSO-AMC direct 仅 L124/L165 两篇，IM/DD-HARQ 占多数），adjacent 39，none 159。

---

## §4 候选问题族地图

> **声明**：以下为**候选问题假设，未过四判据**。M-C-A = "现有方法 M 在条件 C 下因假设 A 失效/不足"——仅候选，不伪称成立。dead-end collision 逐条对照 topic-index.md 9 条 ledger。

### F1 鲁棒 / CSI 不确定下的 AMC（outage / delayed / statistical CSI）

**候选 M-C-A 假设**（未验证）：现有 FSO AMC 方法 M（多为 perfect-instantaneous-CSI 假设的 mod+power 切换，代表 L023/L020/L075）在条件 C（星地链 CSI 受大气相干时间 2–10 ms + 反馈 RTT 限制，只能拿到 statistical / delayed / partial CSI）下因假设 A（瞬时 CSI 可用且无差错）失效，导致 outage/掉包。

| 字段 | 内容 |
|---|---|
| family_id | **F1** |
| 暂定 M-C-A | 见上（候选，未过四判据） |
| 系统层真实 action | 调制阶数 / 码率 / 功率在 outage 约束下按 statistical/delayed CSI 鲁棒切换 |
| receiver·transmitter 可见信息 | rx 估统计量（Rytov Cn² / scintillation variance / SNR 长窗统计）→ 反馈统计 CSI 给 tx；rx 不需要瞬时 BER |
| 信道与反馈时间尺度 | **危险区**：依赖统计 CSI（秒级稳定）可绕开 2–10 ms 相干时间；但仍受 LEO 单 pass / GEO RTT 约束 |
| 最强 conventional comparator | L023（JLT 2023，CSI-driven mod+power+MIMO 自适应）/ L018（HARQ code-rate 按 CSI type 自适应） |
| dead-end collision 逐条 | #1 ISL prediction — 不碰（信道含真实湍流不确定性）✓；**#2 反馈-相干时间 — 碰撞风险高**，须 Step 2/3 核算动作周期 vs 相干时间（候选假设核心就是绕开，但未证）；#3 MCS 0.09dB — 不碰（非 oracle 切换窄切片）✓；#4 AMC+CPR — 不碰（独立于跨调制同步参数）✓；#5 交织/PS/N1 — 不碰（非纯 PS）✓；#6 P08-R2 资产 — 不引用为结论 ✓；#7 DA/NDA CPR 换名 — 不碰（不同系统层动作）✓；#8 mod-classification — 不碰 ✓；**#9 AMC↔Ch4 BER 循环 — 须 Step 2 验证用统计量前馈解耦**（候选未证） |
| 文献密度 | **低**（coherent sat-ground FSO + GG + 统计/延迟 CSI + AMC 直接文献 0；最接近 L018 IM/DD inter-HAP、L146 FSO/RF robust、L108 RF IRS 可迁移数学） |
| novelty confidence（搜索级） | **中**（空白存在但需 Step 2/3 验证非物理不可行；统计 CSI 路线物理上可绕相干时间，但增益上界未证） |
| 潜在贡献层级 | THESIS_MAIN_METHOD（潜在，未锁定） |
| Step2 获取全文 | **Y**（L018 / L146 / L108） |
| 当前最大未知量 | 统计 CSI 下 AMC 增益上界是否 > dead-end#3 的 0.09 dB；是否撞 #2 反馈环；GG 下统计 CSI 估计算法的稳态收敛时间 |

### F2 HARQ-IR + 速率适配（光卫星下行 cross-layer）

**候选 M-C-A 假设**（未验证）：现有光卫星 HARQ 设计 M（代表 L096 stop-and-wait / sliding-window IR-HARQ、L126 power-alloc HARQ）在条件 C（真实 coded chain + GG 湍流 + LEO 短 pass）下因假设 A（理想 FEC + 无重传开销建模 / 固定 power）不足以最大化 coded goodput，需联合 rate+power+HARQ-IR 自适应。

| 字段 | 内容 |
|---|---|
| family_id | **F2** |
| 暂定 M-C-A | 见上（候选，未过四判据） |
| 系统层真实 action | IR-HARQ 重传次数 / 码率 / 发射功率联合适配（coded goodput 目标） |
| receiver·transmitter 可见信息 | rx 做 FEC 解码 + ACK/NACK + 累积 IR；tx 据 NACK 调码率/功率——不需瞬时 CSI，靠 HARQ 闭环 |
| 信道与反馈时间尺度 | **危险区**：HARQ 闭环依赖 ACK RTT，LEO 单 pass 内重传窗口紧（dead-end#2 相关但比纯 CSI 预测宽松，因重传可跨时隙累积）；GEO RTT >100 ms 使 HARQ 几乎不可用 |
| 最强 conventional comparator | L096（IEEE TVT 2021，FSO sat IR-HARQ + rate adapt，cross-layer）/ L126（Photonics 2022，光 LEO HARQ power alloc）/ L073（Entropy 2025，FSO HARQ 极限） |
| dead-end collision 逐条 | #1 — 不碰 ✓；**#2 — 碰撞风险中**（HARQ 闭环仍受 RTT，但 IR 累积可部分缓解，Step 2 须核 LEO pass 时长 vs HARQ round）；#3 — 不碰 ✓；#4 — 不碰 ✓；#5 — 不碰（HARQ 非 PS/交织 repair）✓；#6 — 不引用 ✓；#7 — 不碰 ✓；#8 — 不碰 ✓；#9 — 部分：HARQ 闭环量度（ACK/NACK）解耦于 BER，不撞 #9 ✓ |
| 文献密度 | **高**（L096/L126/L073/L041/L007/L018/L085/L099/L100，IM/DD 与 hybrid FSO/RF 均有） |
| novelty confidence（搜索级） | **低-中**（IM/DD 与 hybrid 文献密集，coherent + GG + 真实 LDPC coded chain 直接竞品少，但机制本身高度成熟，novelty 上界受 dead-end#3 类比限制） |
| 潜在贡献层级 | THESIS_ENGINEERING_COMPONENT / SUPPORTING_MATERIAL（机制成熟，难撑 MAIN_METHOD） |
| Step2 获取全文 | **Y**（L096 / L126 / L073 / L018） |
| 当前最大未知量 | coherent + GG + 真实 LDPC（非 RS/理想 FEC）coded goodput 增益上界；LEO pass 内 HARQ round 数物理可达性；与既有 P08-R2 LDPC 工程资产能否复用 |

### F3 CSI 驱动的自适应调制 + 功率分配（湍流下）

**候选 M-C-A 假设**（未验证）：现有 IM/DD FSO 自适应调制+功率 M（代表 L023 multi-modal transceiver、L020、L075 DL）在条件 C（coherent sat-ground + GG）下因假设 A（IM/DD + 弱湍流 / 商用器件模型）不能直接迁移到相干强湍流场景，需针对相干接收重设 action 空间。

| 字段 | 内容 |
|---|---|
| family_id | **F3** |
| 暂定 M-C-A | 见上（候选，未过四判据） |
| 系统层真实 action | 调制阶数（QAM）/ 功率 / MIMO decoder 模式按动态 CSI 切换 |
| receiver·transmitter 可见信息 | rx 估瞬时/统计 CSI → tx 自适应分配（L023 已实验 demo） |
| 信道与反馈时间尺度 | **危险区高**：动态 CSI 估 + 反馈切换周期 vs 2–10 ms 相干时间，强湍流下瞬时 CSI 几乎不可用（dead-end#2 直接碰撞） |
| 最强 conventional comparator | L023（JLT 2023，实验 demo CSI-driven mod+power+MIMO）/ L075（DL adaptive mod）/ L020（2019 baseline） |
| dead-end collision 逐条 | #1 — 不碰 ✓；**#2 — 碰撞风险极高**（瞬时 CSI 切换正是 dead-end#2 原型），须 Step 2 核 L023 实际反馈周期是否 > 相干时间；#3 — 不碰 ✓；#4 — 须 Step 2 核（若跨调制切 decoder 模式可能撞 AMC+CPR）⚠️；#5 — 不碰 ✓；#6 — 不引用 ✓；#7 — 不碰（不同层）✓；#8 — 不碰 ✓；**#9 — 碰撞风险**（BER-driven 切换门限 ↔ CPR 影响，须前馈解耦） |
| 文献密度 | **中**（IM/DD 侧 L023/L020/L075/L159/L068；coherent 侧仅 L124/L165，且 L165 动作在 AO 层） |
| novelty confidence（搜索级） | **低**（IM/DD 已饱和；coherent 侧迁移工作存在但物理时间尺度危险，dead-end#2/#9 双碰） |
| 潜在贡献层级 | SUPPORTING_MATERIAL / THESIS_ENGINEERING_COMPONENT（不建议作 MAIN_METHOD，时间尺度风险高） |
| Step2 获取全文 | **Y**（L023 / L075 / L020） |
| 当前最大未知量 | coherent 相干接收下瞬时 CSI 估计是否能在 2–10 ms 内收敛并反馈；切换是否解耦于 CPR（#4/#9） |

### F4 相干 FSO 物理信息自适应传输（multi-dim amplitude-phase）

**候选 M-C-A 假设**（未验证）：现有方法 M（多为 6G 通用 / AO 补偿，代表 L124 physics-informed adaptive transmission、L165 feeder link AO demo）在条件 C（coherent sat-ground + GG 强湍流 + coded chain）下因假设 A（通用 6G 框架 / AO 层补偿 ≠ AMC 层）未真正形成 AMC 控制动作，存在把"自适应"做成 AO 或 receiver DSP 的风险。

| 字段 | 内容 |
|---|---|
| family_id | **F4** |
| 暂定 M-C-A | 见上（候选，未过四判据；abstract 偏 6G 通用，**必须 Step 2 全文确认是否真做星地 GG + coded AMC**） |
| 系统层真实 action | 待 Step 2 确认（abstract 含 "physics-informed adaptive transmission"，但 action 层级不清——AMC？AO？DSP？） |
| receiver·transmitter 可见信息 | "multi-dim amplitude-phase statistics" 提示用信道统计量驱动适配 |
| 信道与反馈时间尺度 | 待 Step 2 确认（若用统计量可绕相干时间；若瞬时则撞 #2） |
| 最强 conventional comparator | L124 自身（若它是 coherent+AMC，则是 F4 的现有最优；若不是则 F4 仍是空白） |
| dead-end collision 逐条 | #1 — 不碰 ✓；#2 — 待确认（统计量则安全，瞬时则碰）；#3 — 不碰 ✓；**#4/#7 — 高风险**（若 L124 的 "amplitude-phase" 自适应实质是 CPR/相位恢复换名，则直接撞 dead-end#4/#7，须 Step 2 严查）；#5 — 不碰 ✓；#6 — 不引用 ✓；#8 — 不碰 ✓；#9 — 待确认 |
| 文献密度 | **空-低**（coherent + AMC 直接仅 L124 一篇候选，L165 动作在 AO 层；round-1 也发现 0 direct） |
| novelty confidence（搜索级） | **不确定（待 Step 2）**——若 L124 真做 coherent+GG+coded AMC 则 novelty 低（被占）；若 L124 是 AO/通用框架则 F4 空白但需自建问题 |
| 潜在贡献层级 | 不锁定（取决于 L124 全文定性） |
| Step2 获取全文 | **Y**（L124 / L165） |
| 当前最大未知量 | L124 全文是否真做星地 GG + coded AMC（vs AO / 6G 通用 / CPR 换名）；这是整个 Step 1 最大的单一未知量 |

---

## §5 R001 必答 8 问

**Q1. 搜到了哪些真实 AMC 机制族？**
4 族机制真不同：(F1) 鲁棒/statistical-CSI AMC、(F2) HARQ-IR + 速率/功率适配、(F3) CSI 驱动自适应调制+功率、(F4) 相干物理信息自适应传输。必读 10 篇中 8 篇落在 F2/F3（IM/DD 与 hybrid FSO/RF 主导），2 篇（L124/L165）是仅有的 coherent-FSO-AMC 候选。

**Q2. 哪些只是 automatic modulation classification 或无关资源分配？**
- mod-classification 一律排除 5 条：L087（MFI survey）、L188（OAM 模式识别）、L184（涡旋双任务识别）、L207（双参数反演）、L070（borderline demod）。
- 无关资源分配排除一大批：RF IRS/RIS/NOMA（L098/L106/L107/L140/L141/L142/L143/L148/L156）、RF 路由/spectrum（L053/L077/L160）、TCP/transport（L166）、covert/backscatter（L147/L148/L054）、SWIPT（L155）、VDES 时隙（L182）、紫外/可见光（L190/L209）、应急广播/引信/SAR（L185/L198/L194）等。共 121 排除。

**Q3. 哪些与旧 AMC/交织/PS/CPR/MCS 路线碰撞？**
- **#2 反馈-相干时间**：F3（CSI 驱动瞬时切换）碰撞风险极高；F1/F2 中-高风险但可绕（统计 CSI / HARQ 累积）；F4 待定。
- **#4 AMC+CPR 联合设计**：F3 跨调制切 decoder 模式、F4 若 "amplitude-phase" 实质是相位恢复换名——都须 Step 2 严查。
- **#7 DA/NDA CPR 换名**：L110（branch phase correction）、L158（digital PLL）、L116（adaptive MIMO equalization）、L057（SIC DSP）、L164（NN channel est）等 receiver-DSP 类虽未排除但标备选/adjacent，禁止当 AMC 方法。
- **#5 交织/PS/N1**：L050/L206（中文 PS+FSO）必须 Step 2 验证是否纯 PS repair 冒充 AMC；L003（5G-LDPC 交织重传）标待确认。
- **#9 AMC↔Ch4 BER 循环**：F1/F3 须用统计量/ACK 前馈解耦；F2 用 ACK/NACK 天然解耦。

**Q4. 哪些方向物理时间尺度明显危险？**
- F3（瞬时 CSI 调制+功率切换）：大气相干时间 2–10 ms，强湍流下瞬时 CSI 估计+反馈几乎不可用，dead-end#2 直接原型——**最危险**。
- F2（HARQ-IR）：LEO 单 pass（数分钟）内 HARQ round 受 ACK RTT（数十 ms）限制，但 IR 累积可部分缓解；**GEO（RTT>100 ms）HARQ 几乎不可用**——L126 明确说"propagation latency is low for LEO"才采用 HARQ。
- 任何依赖瞬时 BER 反馈的门限切换（dead-end#9）：与 CPR 估计耦合且受相干时间限制。
- 相对安全：统计 CSI（秒级稳定）驱动的 F1、ACK-driven 的 F2（LEO 限定）。

**Q5. Step 2 acquisition shortlist（12 篇）**：

| L | title | year | venue | 一句话理由 |
|---|---|---|---|---|
| L018 | Adaptive HARQ with CSI in Inter-HAP FSO Links | 2017 | elib (DLR) | F1/F2 锚：唯一系统对比 perfect/delayed/reciprocal/fixed-mean CSI 下 HARQ code-rate 自适应 |
| L096 | FSO Satellite IR-HARQ with Rate Adaptation | 2021 | IEEE TVT | F2 锚：最完整的光卫星 cross-layer HARQ-IR + 速率适配 |
| L126 | Power Allocation for Optical LEO-to-Ground HARQ | 2022 | Photonics | F2：功率+HARQ 联合动作，LEO 物理时间尺度参考 |
| L073 | HARQ Performance Limits for FSO | 2025 | Entropy | F2 基础：2025 最新 FSO HARQ 性能极限（misalignment+turbulence） |
| L023 | Adaptive Transceiver Multi-Modal FSO | 2023 | JLT | F3 锚：实验 demo CSI-driven mod+power+MIMO decoder 自适应，最强 conventional comparator |
| L075 | Hybrid DL Adaptive Modulation for FSO | 2026 | — | F3：DL AMC 对照（DL 是否真能处理非线性湍流） |
| L020 | Adaptive Modulation Schemes for High-Capacity FSO | 2019 | — | F3 旧 baseline，理解规则式 AMC 局限 |
| L124 | Physics-informed Adaptive Transmission for Coherent FSO | 2026 | — | **F4 锚 + 全 Step1 最大未知量**：唯一直接 coherent+AMC 候选，须全文定性是 AMC 还是 AO/CPR 换名 |
| L165 | Tbit/s Feeder Links Coherent Mod + Full-AO | 2023 | LSA (c109) | F4 上下文：coherent sat-ground demo，adaptive 动作在 AO 层（确认边界） |
| L146 | Robust Joint Opt FSO/RF sat-UAV-terrestrial Imperfect Channel | 2025 | — | F1：FSO/RF robust AMC + imperfect channel，可迁移数学 |
| L050 | DFT-SAMP 信道估计与概率整形联合优化 FSO | 2026 | 空间电子技术 | F3/F5 中文 PS+FSO（round-1 标记），须验证是否纯 PS repair 撞 dead-end#5 |
| L206 | 三维概率整形 FSO for 快衰落信道 | 2026 | 空间电子技术 | F3/F5 中文 PS+FSO 快衰落，dead-end#5 风险，须全文 |

**Q6. 当前最值得精读的 2–3 候选问题族**：
1. **F4（L124 + L165）**——Step 1 最大的单一未知量。L124 是唯一直接 coherent+AMC 候选，全文定性决定整个 coherent AMC 空间是否已被占。
2. **F1（L018 + L146）**——统计/delayed CSI 路线物理上可绕相干时间（dead-end#2），是 novelty 与物理可行性的最佳平衡点，但增益上界未证。
3. **F2（L096 + L126）**——机制最成熟、文献最密、ACK-driven 天然解耦 dead-end#9，但 novelty 上界受 dead-end#3 类比限制，更适合作 ENGINEERING_COMPONENT。

**Q7. 为什么比直接重开 receiver 小修补更可能形成毕业方法？**
F1/F2/F4 都要求**不同系统层的真实控制动作**（modulation/code-rate/power/HARQ-IR 切换），与既有 DA/NDA 自适应 CPR（dead-end#7 主贡献）物理隔离；而 receiver 小修补（新 CPR 算法/均衡器/双偏振 OSL）会直接撞 dead-end#7 换名且无系统层新动作。F1 的统计 CSI 前馈还能解耦 dead-end#9（BER 循环依赖）。但这是"候选假设"，毕业可行性须 Step 2/3/4a 逐门验证。

**Q8. 饱和/物理可行性的诚实结论（关键）**：
- **coherent sat-ground FSO + GG + AMC + 真实 coded chain 四要素齐全的直接竞品：搜索级 0 篇确认**（L124 是唯一候选但 abstract 偏 6G 通用，须 Step 2 全文确认；L165 动作在 AO 层非 AMC）。round-1 71 条也发现 0 direct，本轮 209 条交叉验证一致——**搜索级空白存在**。
- 但**空白不等于问题成立（FR-23）**：空白可能源于（a）真无人做（机会），也可能源于（b）物理不成立（如瞬时 CSI 撞相干时间 dead-end#2 已被领域隐式放弃，故无直接竞品）。Step 2/3 必须区分这两种可能，**不强造方向**。
- F2（HARQ-IR）方向**高度饱和**（IM/DD + hybrid FSO/RF 文献密集），novelty 上界低，更适合 ENGINEERING_COMPONENT。
- F3（瞬时 CSI 调制+功率）**物理时间尺度危险**（dead-end#2/#9 双碰），不建议作 MAIN_METHOD。
- 最有希望但不保证：F1（统计 CSI 鲁棒 AMC，物理可绕相干时间，但增益上界未证）+ F4（待 L124 全文定性）。**若 L124 证实 coherent+GG+coded AMC 已被占，且 F1 增益上界 ≤ dead-end#3 的 0.09 dB 量级，则需诚实报告方向不可行，不强造。**

---

## §6 对决策的影响

Step 1 是**搜索级证据**，按 TL-32 / FR-22 / FR-25：
- **不产生 Go/Kill**（Step 1 无 Go/Kill；Go 判据 = 赢传统未优化 baseline，是 Step 4a 的事）。
- **不产生 METHOD_SIGNAL**，不设计方法，不跑仿真。
- **不新建 D###**：候选问题族只进 R001，不进 decisions.md。除已立 D001（范围与旧轴边界）外，Step 1 阶段不新建方法决策。
- **下一合法动作**（唯一）：主控验收 Step 1 后，进入 **Groundwork Step 2 全文获取**（独立新对话），获取 §5 shortlist 12 篇全文到 `papers/{arxiv|doi}/{id}/content.md`。
- **Step 2 优先级建议**（搜索级，非决策）：L124（F4 单一最大未知量）→ L018/L146（F1 锚）→ L096/L126（F2 锚）→ L023/L075（F3 comparator）→ 其余。

**风险声明**：CNKI 38 条全部无摘要（cookie/IP 受限），其中 L050/L206/L181/L186/L197 仅靠 title 判，Step 2 抓全文前定性低 confidence。
