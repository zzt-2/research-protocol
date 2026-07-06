# 星地 FSO 主流链路调研：单载波 vs OFDM

> 调研日期: 2026-07-06 | 子 agent 调研笔记 | 决策依据：B11 走 OFDM 频域 ML 还是单载波时域 ML
> 方法：本地 papers/_read_notes 优先 + web 交叉验证（abstract/DOI/标准原文）
> 结论一句话：**星地 FSO 相干链路主流是单载波（DP-QPSK / M-QAM / M-APSK），OFDM 是边缘方案；B11 的 OFDM 是 fiber-CO-OFDM 通用声明，非星地主流。**

---

## 1. 星地 FSO 主流链路：单载波（强证据）

### 1.1 本地 papers/_read_notes 证据（20+ 篇 FSO 笔记 grep）
- **OFDM 仅出现在 2 篇**：(a) B11 本身（10.1109_LPT.2024.3523478，CO-OFDM，声明 FSO 但仿真未建模 FSO 信道）；(b) WiSEE 2024（10.1109_WiSEE61769.2024.10850117）——**关键 nuance**：它的 OFDM 只用于**训练头/信道估计子载波分集**，payload 是 **32 GBd DP-4QAM / DP-16QAM 单载波**（"用已知训练符号（OFDM CE 头 + 4QAM 导频）替代盲均衡，使信道估计与 payload 调制格式解耦"，L31/L65）。
- **其余 ~18 篇全部单载波**：sat.1553 综述（QPSK/M-QAM intradyne 数字载波恢复）、JLT.2023.3281082（coherent FSO LEO 数字多普勒）、LPT.2025.3647750（PS+RCM FSO 湍流）、ICSOS OQAM、ICSOS Z-Transform ODPLL（satellite-to-ground）、Aerospace CCSDS O3K、Photonics ODPLL、oe.553709（Kalman Doppler）、oe.555656（阵列检测 sat-to-ground）、oe.520452 + jphot.3265847（FSO 湍流分集 QPSK/16QAM）、LCOMM.2026.3651445（频域 pilot 但单载波 DSCM）、ACCESS.2025.3535789（自相干 FSO）、app.11219805（PS-QAM FSO Gamma-Gamma）。**无一例 OFDM 作为星地链路主流方案。**

### 1.2 综述级证据
- **sat.1553（Valjus 2025, Int. J. Satellite Commun. Networking）**：2025 年最新 OSL DSP 综述，给出标准 DSP 流水线（定时→均衡→载波恢复→FEC），**调制格式重点 QPSK（也提 DP-QPSK / M-QAM），全文无 OFDM 作为主流方案**。结论是 data-aided（pilot）算法在低 SNR 衰落信道优于 blind。这是卫星链路 DSP 的权威算法地图，单载波为基础。
- **Mouhammad et al. JLT 2025（Vol.44 No.9, pp.3532, DOI 10.1109/JLT.2024/2025，IEEE Xplore 11395528）**："Review on Modulation Formats and Channel Coding in FSO: Selection Criteria, Trade-offs, and Emerging Trends"——abstract（web 抓取 + IEEE Xplore 交叉验证）明确框定为"modulation formats"（单载波 OOK/QAM/PSK/APSK），detection 是 coherent vs IM/DD 的 trade-off，OFDM 仅作 channel coding/emerging trend 提及，**非主流调制范式**。被引 5+。

### 1.3 近期星地 FSO 实际系统（web 交叉验证，均单载波）
1. **Le Bidan et al. 2023, ICSO（hal-04384744, NASA ADS 2023icso.conf...20B）**："Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK link"——**56 GBaud DP-QPSK 单载波**，星地下行链路 custom DSP + frame format。被引 3。
2. **Horst et al. 2023（PMC10282091）**："Tbit/s line-rate satellite feeder links enabled by coherent modulation"——53 km FSO 模拟卫星下行，**1 Tbit/s coherent modulation formats 单载波**。被引 139（高影响力）。
3. **Matuz et al. 2023 DLR（elib.dlr.de/193360）**："Coherent Communications for FSO LEO Satellite Downlinks"——物理层设计，DP-QPSK fading channel。被引 3。
4. **DLR 综述 sat.1553**（同 1.2）。

---

## 2. DVB-S2 / DVB-S2X 标准：单载波（强证据，标准原文）

- **DVB 官方 White Paper（dvb.org/.../a172_dvb-s2x_highlights）原文**："The DVB-S2 specification defines a satellite transmission system using a **single carrier signal** transmitting a series of physical layer packets."——标准本身是单载波，非 OFDM。
- **ETSI EN 302 307（DVB-S2/S2X 官方标准）**：调制 QPSK, 8PSK, 16APSK, 32APSK（S2X 扩展 64/128/256-APSK），BCH+LDPC FEC。支持 "single carrier per transponder"（主流）与 "multi-carriers per transponder (FDM)"（频分复用，非 OFDM）。
- **本地佐证**：app.11219805（PS-QAM FSO Gamma-Gamma）用 DVB-S2 LDPC 码率 2/3，但调制是 16QAM 单载波 + PS——即 FSO 研究直接复用 DVB-S2 的**单载波 FEC**。
- **结论**：DVB-S2/S2X 是**单载波 APSK/PSK 标准**，FSO 研究借其 FEC + ACM 机制，但调制范式仍是单载波。OFDM 不在 DVB-S2/S2X 内（DVB 的 OFDM 在 DVB-SH/T2 地面/移动，非卫星）。

---

## 3. B11 团队（Kam 团队）定位：fiber+FSO 通用声明，非星地主流

- **B11 增量笔记（本地）已核实**：标题/摘要/结论（行 5/9/191）声明 "fiber + FSO" 适用，但**信号模型行 33 假设湍流/指向/Doppler/CFO 已补偿，仿真行 155 仅 AWGN + 激光线宽 Wiener PN，无 FSO 信道建模**。"FSO" 是论文级声明非验证级结论。
- **Kam 团队 web 检索**：其研究主体是 **CO-OFDM 相位噪声估计**（DCT-based CO-OFDM、SDM multi-level PN、DFT-spread OFDM 等，PubMed/MDPI/Aston/SSRN 多篇）——**fiber CO-OFDM 赛道**，非卫星 FSO。B11 的 OFDM 是该团队 fiber CO-OFDM 相位噪声 ML 系列的延伸（自引 Du 2021 JLT / Liu 2022 OE / Wang 2022 T-SP 单正弦 ML），**"FSO" 是泛化措辞**。
- **团队单位**：港中深 NUSRI + UIC 珠海 + 浙工大——非卫星通信传统强校（对比 DLR/IMT Atlantique/Tesat 等），无卫星链路硬件/信道建模背景，进一步佐证其 OFDM 是 fiber 迁移声明。
- **结论**：B11 团队的 OFDM 是 **fiber+FSO 通用声明**，**不代表星地 FSO 主流**。星地 FSO 实际系统（DLR/IMT Atlantique/Horst/Le Bidan）用单载波。

---

## 4. 顶刊近期星地 FSO 主流调制（3-5 例，均单载波）

| 论文 | 期刊/会议 | 年份 | 调制 | 场景 | 来源 |
|---|---|---|---|---|---|
| sat.1553 Valjus et al.（DLR 综述）| Int. J. Satellite Commun. Netw. | 2025 | QPSK/M-QAM intradyne | OSL ISL/下行/上行 4 场景 | 本地精读 |
| Horst et al. Tbit/s feeder link | Nature/PMC | 2023 | coherent modulation 单载波 | 53 km FSO 模拟卫星下行，1 Tbit/s | web（PMC10282091, 被引 139）|
| Le Bidan et al. 56 GBaud GEO | ICSO | 2023 | DP-QPSK 单载波 | GEO 星地下行 custom DSP + frame | web（hal-04384744, ADS 2023icso...20B）|
| JLT.2023.3281082 Fernandes et al.（U. Aveiro）| JLT Vol.41 No.12 | 2023 | coherent FSO 单载波（数字多普勒治理）| LEO-to-Earth | 本地精读 |
| Mouhammad et al. modulation review | JLT Vol.44 No.9 | 2025 | 单载波 OOK/QAM/PSK/APSK，coherent vs IM/DD | FSO 综述 | web（IEEE 11395528, Optica jlt-44-9-3532）|

**无一例 OFDM 作为星地链路主流。** OFDM 仅在 WiSEE 2024（训练头）与 B11（声明未验证）出现，均为边缘/工具性使用。

---

## 5. 对主线决策的建议

**建议走单载波时域 ML（现有基建），而非 B11 OFDM 频域 ML。**

### 5.1 理由（按证据强度）
1. **目标链路对齐**：星地 FSO 相干链路主流是**单载波 DP-QPSK / M-QAM / M-APSK**（DVB-S2X 标准单载波 + DLR 综述 sat.1553 + Horst/Le Bidan 实际系统 + JLT 2025 modulation review）。走 OFDM 等于把 B11 的 fiber-CO-OFDM 算法搬到**目标链路不用**的范式上，迁移价值存疑。
2. **B11 的"FSO"是声明非验证**：B11 仿真无 FSO 信道（行 33 假设已补偿），Kam 团队是 fiber CO-OFDM 赛道。走 OFDM 频域 ML 等于继承一个**未被星地链路验证的算法**到**星地不用的范式**——双重 mismatch。
3. **现有基建复用**：common 基建是单载波时域（B7 Gardner / B6 ODPLL / B4 V–V / B10 pilot-RLS / B5 CFO），走单载波时域 ML 直接复用信道模型、帧结构、评估管线；走 OFDM 需补 DFT/CP/子载波全套基建（参见同目录 `_OFDM_infra_assessment.md`）。
4. **架构性不等价（已有诊断）**：单载波时域升 M₀ 次幂（逐样本 Wiener PN）≠ 频域升 M₀ 次幂（单常 CPE + DFT 处理增益）；STO 模型完全不同。B11 的闭式 ML 解绑定频域特性，无法等价移植到时域。

### 5.2 单载波时域 ML 的可行路径（建议）
- **复用 B11 核心思想（升 M₀ 次幂去调制 + 单正弦/凸优化 ML）**，但落在**时域**：STO 用 Gardner/Mueller-O&M 类时域 TED 或时域 NDA-ML；CPE 用时域 V–V/Mth-power 块平均或时域 NDA-ML。
- 这样既吸收 B11 的"NDA 盲估计 + 频谱效率"卖点，又对齐星地单载波链路与现有基建，避免 OFDM 基建重写。
- 注意：时域升 M₀ 次幂的 ML 推导与 B11 频域**不等价**（需独立推导 + CRLB），这是真实工作量，但比"重写 OFDM 基建 + 迁移到非主流范式"低风险。

### 5.3 仅当以下条件成立才考虑 B11 OFDM
- 若主线**未来目标链路明确是 OFDM**（如某些 OFDM-FSO 论文追踪），或
- 若想**逐字复现 B11**（验证 +2 dB gain）作为对照锚——则可短期补 OFDM 基建做一次 sanity reproduction，但**主线仿真不应以 OFDM 为载体**。

---

## 6. 关键不确定性

1. **OFDM-FSO 子领域的存在**：学术界确有 OFDM-FSO 论文（如 ScienceDirect S003040262300425X "coherent-OFDM for FSO"、MDPI 2022 OFDM-QPSK spatial diversity），主张 OFDM 抗色散/衰落 + 频谱效率。但这是**研究探索**，非星地实际系统主流（DVB-S2X/Horst/Le Bidan/DLR 均单载波）。若用户目标链路特指 OFDM-FSO 研究线，需重新评估。
2. **B11 cited-by 极少**：B11 仅被引 1 次（10.3390_s25164906，HSR 地对车，背景引用），其 OFDM NDA-ML 思想在 FSO 社区**无技术延伸**——佐证其非星地主流方向。
3. **下一代标准动向**：CCSDS O3K（本地 Aerospace.12100869）是星地光通信标准，单载波（DP-QPSK/16QAM）；未见 OFDM 进入标准轨道。

---

## 来源（web 交叉验证）
- DVB-S2X White Paper: https://dvb.org/wp-content/uploads/2020/01/a172_dvb-s2x_highlights_-_white_paper.pdf
- ETSI EN 302 307 (DVB-S2 standard): https://www.etsi.org/deliver/etsi_en/302300_302399/302307/01.02.01_60/en_302307v010201p.pdf
- Mouhammad et al. JLT 2025 modulation review: https://ieeexplore.ieee.org/document/11395528/ ; https://opg.optica.org/jlt/abstract.cfm?URI=jlt-44-9-3532
- sat.1553 Valjus 2025 (DLR OSL DSP review): https://elib.dlr.de/213162/
- Horst et al. 2023 Tbit/s feeder link: https://pmc.ncbi.nlm.nih.gov/articles/PMC10282091/
- Le Bidan et al. 2023 ICSO 56 GBaud DP-QPSK: https://imt-atlantique.hal.science/hal-04384744v1/document
- Matuz et al. 2023 DLR coherent LEO downlink: https://elib.dlr.de/193360/1/Rates_LN_fading_channel%20%286%29.pdf
- 本地精读笔记: papers/_read_notes/{10.1002_sat.1553, _B11-nda-ml-sto-cpe-increment, 10.1109_WiSEE61769.2024.10850117, 10.1109_JLT.2023.3281082, ...}
