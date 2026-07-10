# FSO 相干均衡全谱地勘（landscape）

> 创建: 2026-07-10 | 专题: 2026-07-10-equalization-layer-direction-scouting
> 阶段: GW Step 1 地勘前置（第 1+2 批，组 1-6 全部完成）| 产出供阶段 1.5 选地
> 纪律: abstract 层只找候选清单，禁判判据 A（baseline 真失效）。判缝移全文层（阶段 2/3）。
> 批次范围: 第 1 批组 1-3（equalization 总览/偏振/MIMO）+ 第 2 批组 4-6（ISI 深/AO-DSP/湍流补偿）。全部 6 组完成。

## 检索覆盖度（诚实标注）

- 检索组数: 6（第1批组 1-3 + 第2批组 4-6）
- 检索源: `tools/search`（S2/OpenAlex 正常）+ `tools/blit --source ieee`（7 次均≈0 命中，仅组6命中 1 篇 Qin 2026 T-Comm）
- **源状况诚实标注**：
  - S2 + OpenAlex 正常工作（两批主力）
  - **Exa 信用额度耗尽**（NO_MORE_CREDITS，两批都不可用）→ 失去语义搜索，关键词质量更关键
  - **SerpAPI 未安装 / Tavily 连接重置** → 召回源减少
  - **IEEE blit 7 次查询仅 1 命中**（组6 Qin 2026 IEEE T-Comm，余均 0）→ venue 字段主要靠 OpenAlex/S2 `container_title`，可能漏 IEEE 独有论文（PTL/CL 等）
- 候选论文总数（第1批29 + 第2批新增~22，跨批去重后）: **~46 篇**（主表）
- 子地带覆盖（共 8 个）: multi-aperture coherent combining / OAM-MIMO 均衡 / 偏振均衡 / ISI 均衡 / OFDM-FSO / DNN-NN 均衡 / AO-DSP 残余补偿 / 湍流信道均衡（横切）
- **未覆盖（诚实）**:
  - Exa 语义搜索全程缺失 → 可能漏关键词不匹配但语义相关论文
  - IEEE blit 近乎失效 → 可能漏 IEEE 全文库独有论文（PTL/CL 等 Trans/Letters）
  - SerpAPI（Google Scholar）缺失 → 中文/灰色文献召回不足
  - 部分 abstract 补全失败（如 Lee & Kavehrad 2009）→ 老文信息不完整

## 论文主表

> 缝潜力初判说明：🟢=多方法并存可能竞争 / 🟡=不确定待精读 / 🔴=明显饱和。**全部基于 abstract 粗判，未判 baseline 真失效（禁判据 A）**。

### 子地带 1: Multi-aperture coherent combining / MDCC（🟢 活跃，本批核心发现）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 1 | Geisler — Multi-aperture digital coherent combining for FSO receivers | 多小孔径相干检测+数字化合成接收机架构（**MDCC 奠基**）| Trans (OE) | 2016 | 是（3.2km）| 单大孔径终端 | 🟡 |
| 2 | **Liu/Ju — MDCC based on complex-valued MIMO 2N×2 adaptive equalizer** | 复值 MIMO 自适应均衡器做数字合成（**核心工程论文**，引 13）| Trans (JLT) | 2023 | 是 | abstract 未提 | 🟢 |
| 3 | Ju — Blind skew compensation + widely-linear equalizer for MDCC | 抗 I/Q skew/imbalance 的 widely-linear 均衡+合成 | Trans (OE) | 2023 | 是 | 无 skew 补偿 | 🟢 |
| 4 | Ju — Real-time two-aperture CDC with real-valued MIMO equalizer | 实值 massive-array MIMO 均衡器，实时，抗 deep fading（引 6）| Letters (OL) | 2024 | 是（强湍流）| 单孔径 | 🟢 |
| 5 | Zhang — High-speed FSO using mode demux + coherent combining | 模式解复用+相干合成抗湍流，20Gbps/1km | Trans (JLT) | 2025 | 是 | abstract 未提 | 🟢 |
| 6 | Tu — Phase alignment min-complexity for EGC | 低复杂度相位对齐算法 | Trans (JPhoton) | 2020 | 部分 | abstract 未提 | 🟡 |
| 7 | Rao — Practical digital phase alignment for D-CBC | 实时相位对齐 DSP 实现 | 期刊 (Access) | 2020 | 部分 | abstract 未提 | 🟡 |
| 8 | Johst — Data-aided multi-format DSP for robust FSO coherent | 低 SNR（低至 0 dB）数据辅助均衡器，3.2km 实测 DP-16QAM | 会议 (WiSEE) | 2024 | 是 | abstract 未提（自称 custom DSP）| 🟢 |
| 9 | Chen — Blind gradient-ascent phase alignment（BGAPA）| 盲梯度相位对齐，直接最大化合成功率 | preprint | 2026 | 部分 | stochastic 相位对齐 | 🟢 |

**MDCC 支撑论文（架构/系统，均衡非主旨，列备查）**：Geisler 2017 (SPIE/IPC)、Yarnall 2015 (ICSOS)、Xiang 2021 (ICECE)、Yang 2017 (OE all-fiber CBC)、Billaud 2020 (SPIE MPLC)、Perlot/VERTIGO 2023 (SPIE 18km GEO feeder)、Arikawa 2018 (SPIE mode-diversity)、Mosnier 2025 (SPIE emulator)、Serra 2025 (ICSOS PIC)

### 子地带 2: OAM-MIMO 均衡（🔴 饱和死地，跨 12 年成熟）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 10 | Ren — FSO comm using OAM multiplexing + MIMO（4×4）| 2×2 孔径 ×2 OAM 模式 + 4×4 MIMO 信号处理，80Gbps（引 92）| Letters (OL) | 2015 | 是 | 无 MIMO | 🟡 |
| 11 | Ren — Atmospheric turbulence mitigation in OAM-MIMO FSO | spatial diversity + MIMO 均衡抗湍流（引 98）| Letters (OL) | 2016 | 是 | abstract 未提 | 🟡 |
| 12 | Yousif — Adaptive OAM-MIMO/SMM | 自适应 MIMO-FSO + 空间模分（引 186）| 期刊 (Access) | 2019 | 是 | 无自适应 | 🟡 |
| 13 | Hu — Adaptive transceiver, multi-modal FSO | 自适应调制+MIMO 解码器选择 | Trans (JLT) | 2023 | 是 | 固定收发 | 🟡 |
| 14 | Wang — OAM and beyond（综述）| OAM 综述，标"mature"（引 340）| 期刊 (Nanophotonics) | 2021 | 是 | — | 🔴 |

### 子地带 3: 偏振均衡 / PolDemux（🟢 升温，2025-2026 集中涌现）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 15 | **Cvijetic/Djordjevic — Polarization-multiplexed optical wireless with coherent detection** | 偏振复用相干 OWC；证 mild-mod 湍流下偏振演化为偏振态旋转（**奠基**，引 93）| Trans (JLT) | 2010 | 是 | abstract 未提（奠基性）| 🔴（奠基思路沿用）|
| 16 | ANN-based equalization of polarization mixing + MZM nonlinearity for DP self-coherent FSO | 用 ANN 替代矩阵求逆(MI) DSP，恢复湍流下偏振混叠符号 | Trans (Access) | 2026 | 是 | 矩阵求逆(MI) 常规 DSP | 🟢（孤证）|
| 17 | **Bootstrapping blind equalizer for DP coherent FSO via modulus-rings VAE** | 两种盲 VAE 均衡器（VAELP/VAEMR），快收敛 bootstrapping | Trans (TCCN) | 2026 | 是 | "现有盲均衡算法"（abstract 未明说）| 🟢（孤证）|
| 18 | DP self-coherent transceivers for FSO in atmospheric turbulence | 仿真分析 DP 自相干 FSO；湍流致偏振旋转/相移，信道矩阵退化 | Trans (Access) | 2025 | 是 | abstract 未提 | 🟢 |
| 19 | Review and analysis of DSP algorithms for coherent optical satellite links | 综述 WDM+偏振复用卫星链路 DSP 算法（CMOS 化路径）| Trans (IJSCN/sat.1553) | 2025 | 部分 | abstract 未提 | 🟡（综述）|

### 子地带 4: ISI 均衡（🟡 待组 4 深查，本批仅孤证）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 20 | Zhang — DPSK and channel equalization in FSO | DPSK 相干 FSO，云散射致高速 ISI，BM-CMA（set-membership）均衡（**孤证**）| 期刊 (Opt Eng) | 2018 | 部分 | abstract 未提 | 🟡（孤证）|

> seed.md 标注 TCOMM 2026 "ISI in IRS-Assisted FSO" 是该子地带最新 Trans，本批未召回（组 4 专门查 ISI 时补）。

### 子地带 5: OFDM-FSO 均衡（🟡 偏理论分析，组 6 待深查）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 21 | Chen — MDPSK-based nonequalization OFDM for coherent FSO | 相干 FSO 用 MDPSK 无均衡(NE)-OFDM（"无均衡"反向角度，引 29）| Letters (PTL) | 2014 | 是 | TD-MDPSK vs FD-MDPSK（内部对比）| 🟡 |
| 22 | Wang — Performance of coherent OFDM systems in FSO | Gamma-Gamma 湍流+相位噪声，SER/中断概率闭式推导 | 期刊 (JPhoton) | 2015 | 是 | abstract 未提 | 🔴（解析性能分析类密集）|
| 23 | Elsayed — OFDM UAV-based FSO with scintillation mitigation | 4-QAM-OFDM UAV-FSO 闪烁缓解 | 期刊 (Opt Quantum Electron) | 2024 | 是 | abstract 未提 | 🟡 |

### 子地带 6: DNN/NN 均衡（🟢 新兴但 Trans 级少，多孤证）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 24 | Kulmer — NN nonlinear mitigation + coherent combining for FSO | 100W 高功率下 ANN 缓解放大器非线性+合成，1Tbit/s，SNR 增益 3.0+0.9dB | Trans (OE) | 2026 | 部分 | conventional single-amplifier | 🟢（孤证）|
| 25 | Qin — Blind MIMO VQ-VAE equalizer for FSO coherent | 盲 MIMO VQ-VAE 均衡，湍流下时变纠错+IQ skew 补偿 | 会议 (OFC) | 2025 | 是 | abstract 未提 | 🟢（孤证）|

> 偏振均衡子地带的 ANN(#16) 和 VAE(#17) 也属 DNN 路线，跨子地带。

### 子地带 7: AO-DSP 残余补偿 / 自相干补偿（🟡 本批边缘召回，组 5 待深查）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 26 | Horst — Tbit/s line-rate satellite feeder links, full-adaptive optics | 53.42km 相干 Tbit/s，全 AO 补偿湍流，full-field DSP（均衡非主旨，引 134）| Trans (Light Sci Appl) | 2023 | 是 | abstract 未提 | 🟡 |
| 27 | Zhang — Turbulence-resilient pilot-assisted self-coherent FSO, auto optoelectronic mixing | 自相干，导频辅助，自动光电子混频克服湍流模式耦合 | Trans (Nature Photon) | 2021 | 是 | abstract 未提 | 🟡（自相干路径）|
| 28 | Zhu — Compensation-free high-dimensional FSO using turbulence-resilient vector beams | 矢量光束 SPDPSK，免补偿抗湍流 | Trans (Nature Commun) | 2021 | 是 | abstract 未提 | 🟡 |

## 🔴 死地记忆（饱和子地带）

### OAM-MIMO 均衡族
- **饱和理由**：①同一架构（多 OAM 模式 + MIMO 信号处理）跨 12 年反复出现（2014–2026）；②增益趋同（Ren 2015/2016 与 Yousif 2019 增益/模式数接近，多在 2×2/4 模式、80Gbps 量级）；③权威综述（Wang 2021 Nanophotonics，340 引）已做总结性收口；④2023 后仅 Hu 一篇自适应收发延伸，新论文稀少。与 seed.md "🔴 跨 12 年成熟饱和" 判断**交叉核一致**。
- **代表论文**：Ren 2015 (OL, 引 92)、Ren 2016 (OL, 引 98)、Wang 2021 综述 (Nanophotonics, 引 340)。
- **下次不重复撞墙**：地勘/精读阶段若再遇 OAM-MIMO 论文，默认归入死地，不投精读资源（除非有明确新角度如"OAM+全新机制"）。

### 偏振均衡（经典外差相干路径，奠基思路沿用）
- **饱和理由**：Cvijetic 2010 (JLT, 93 引) 奠基后"偏振态旋转→well-known 均衡消除 XPI"已成标准范式，经典路径思路趋同。
- **代表论文**：Cvijetic 2010。
- **注意**：偏振均衡**整体不死**——2025-2026 的 DP 自相干 + 湍流致偏振混叠切口（ANN/VAE/DSP）仍活跃（见子地带 3 🟢）。死的只是"经典外差偏振态旋转均衡"这一奠基思路，不是整个偏振均衡子地带。

### OFDM-FSO 解析性能评估类
- **饱和理由**：Gamma-Gamma/Rician 信道下 SER/中断概率闭式推导论文密集，增益趋同，多停留在理论 BER 分析，实验/工程实体偏少。
- **代表论文**：Wang 2015 (JPhoton)。
- **注意**：OFDM-FSO 整体标 🟡（Chen 2014 NE-OFDM 反向角度 + Elsayed 2024 UAV 仍有产出），组 6 深查后再定。

## 新检索 vs seed.md 交叉核（PROMPT-001 要求）

| 核查项 | 结果 |
|---|---|
| seed 的 16 篇 Trans/Letters baseline，新检索命中几篇？ | **核心命中**：JLT 2010 Cvijetic(#15) / JLT 2023 Liu MIMO(#2) / TCCN 2026 VAE(#17) / OL 2024 Ju(#4) / OE 2023 Ju skew(#3) / PTL 2014 MDPSK(#21) / sat.1553 综述(#19) → 7 篇命中 |
| seed 有但新检索没召回的（→ 补进 landscape 或下批补） | TCOMM 2026 ISI IRS-FSO（组 4 补）/ JLT 2020 OAM CNN / OL 2019 OAM / JLT 2025 autoencoder fronthaul / OE 2023 ELM → 多属组 4-6 待补或 OAM 边缘 |
| 新检索补充 seed 没有的 | Geisler 2016 (OE) MDCC 奠基(#1) / Kulmer 2026 (OE) NN+combining(#24) / Tu 2020 + Rao 2020 相位对齐(#6#7) / Zhang 2025 mode demux(#5) / Horst 2023 feeder(#26) / Zhang 2021 Nature Photon pilot(#27) / Zhu 2021 Nature Commun vector beams(#28) → **补进 landscape** |
| seed 🔴 OAM-MIMO，新检索是否确认饱和？ | **确认饱和**（交叉核一致），维持 🔴 |
| seed 🟡 OFDM-FSO，新检索是否确认？ | 部分确认（Wang 2015 证解析类饱和），但 NE-OFDM + UAV 仍有产出 → 维持 🟡 待组 6 |
| seed 🟢 multi-aperture combining，新检索是否确认活跃？ | **强确认活跃**（Geisler 奠基 + Liu/Ju 2023-2024 DSP 进阶 + Johst 2024 + Chen 2026 BGAPA），维持 🟢 |
| 两表对不上的子地带（重点追对象） | **ISI 均衡**（seed 标 11 篇含 TCOMM 2026，第1批仅 1 篇孤证）→ **组 4 重点追**（第2批已补，见下）|

---

# 第 2 批（组 4-6）追加结果

> 第 2 批补检索：组 4（ISI/dispersion 深查）+ 组 5（AO-DSP 残余补偿）+ 组 6（湍流信道均衡）。
> §7.2 核查（主线抽查 3 篇）：TCOMM 2026 Ajam（DOI+seed 三重确认 PASS）/ Senthilkumar sparse wavelength（JSON 命中 PASS）/ Ahmad 2026 OAM "static equalization" gap 点名（JSON 命中 PASS）→ 无造假。

## 论文主表（第 2 批新增）

### 子地带 4 补全: ISI 均衡（🟡 稀疏 + 一个全新切口，组4重点追结果）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 29 | **Ajam — Modeling & Mitigation of ISI in High Rate IRS-Assisted FSO** | 建立 IRS-FSO（PD 接收）端到端模型，推导 IRS 诱导延迟色散 CIR；1m² IRS 最大延迟展宽 ~0.7ns（>10Gbps 致 ISI）；对比 OOK+ZF-LE / OOK+DFE / DCO-OFDM（**seed 标 TCOMM 2026，本批召回**）| Trans (TCOMM) | 2026 | 否（IRS delay）| DCO-OFDM vs OOK+DFE vs OOK+ZF-LE 互为对照 | 🟡（新切口，单篇 Trans）|
| 30 | Rittler — Multipath Interference in 4×4 Mirror-Array IRS for FSO | 4×4 宏镜面阵列 IRS，建模不同 tile 光程差致接收端相对时延→限制调制带宽；几何模型+实验 | 期刊 (Photonics MDPI) | 2026 | 否 | abstract 未提 | 🟡 |
| 31 | Chen — Frequency-Domain Channel Characteristics of IRS-Assisted VLC | IRS 阵列引入时延对 VLC 信道频域特性影响（**VLC 非 FSO，范围出界参考**）| Trans (JLT) | 2023 | 否 | abstract 未提 | 🟡（出界，IRS-delay 同构参考）|
| 32 | Lee & Kavehrad — FSO with channel shortening filter + Viterbi equalizer | channel shortening + Viterbi 均衡 FSO（**孤证老文**，abstract 缺失）| 期刊 (Int J Wirel Inf Networks) | 2009 | abstract 缺失 | abstract 未提 | 🟡（孤证老文）|
| 33 | Lee & Kavehrad — Airborne laser comm with impulse response shortening + Viterbi | cloud 多散射致严重 ISI；channel shortening + ML 序列检测（与 #32 同作者同思路）| 会议 (MILCOM) | 2006 | 部分（cloud/多散射）| abstract 未提 | 🟡（老文非活跃）|

**ISI 子地带第2批观察**：不饱和，呈"稀疏 + 一个全新切口"。经典 channel-shortening/Viterbi（Lee 2006/2009）= 孤证老文 15+ 年未跟进；DPSK-CMA（#20 Zhang 2018）= 孤证；**IRS-induced ISI（Ajam 2026 TCOMM）= 全新切口，仅 1 篇 Trans，多篇 IRS-FSO 论文只建模 delay dispersion 不做均衡对抗**。abstract 层看是"多方法未竞争 + 增益未趋同"，非饱和（**不判 baseline 真失效**）。

### 子地带 7 补全: AO-DSP 残余补偿（🟡 中等，AO 与 DSP 分工三支）

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 34 | **Paillier — Space-Ground Coherent Links: Ground Receiver With AO and Digital PLL** | 星地相干端到端建模，**AO 校正湍流 + 数字 PLL 补 AO 校正后残余载波相位/频偏**（明确分工）⚠ **DSP 残余是载波 PLL 非均衡，靠近载波同步边界** | Trans (JLT) | 2020 | 是 | abstract 未提 | 🟡（边界警示）|
| 35 | Paillier — AO Assisted Space-Ground Coherent Links with Digital PLL（ICSOS 会议先导版）| 同 #34，AO 校正 + 数字载波同步补残余频偏 | 会议 (ICSOS) | 2019 | 是 | abstract 未提 | 🟡（#34 扩写溯源会议版，同边界警示）|
| 36 | Chen — Highly sensitive fiber coupling for FSO based on ACFC | 自适应相干光纤耦合器补偿 AO 校正后残余角抖动（偏光机前端非信号均衡）| 期刊 (Opt Commun) | 2019 | 是 | 传统直接探测光纤耦合 | 🟡（偏光机前端）|
| 37 | Fontaine — Digital turbulence compensation of FSO with multimode optical amplifier | 12 模数字相干接收 + 多模预放，数字相干叠加 12 模补偿湍流，称"≈ ideal lossless AO"，BER 0.1→1e-3 | 会议 (ECOC) | 2019 | 是 | 传统单模检测 | 🟢（DSP 替代 AO 支，与 MDCC 跨子地带）|
| 38 | Kim — Electronic wavefront correction for PSK FSO | **相干检测 + DSP 替代 AO 校正波前畸变**（奠基），10Gbit/s BPSK 实验 | Letters (Electron Lett) | 2007 | 是 | 无波前畸变系统（上界）| 🟡（奠基早，DSP 替代 AO 概念）|
| 39 | Martinez — Self-adaptive integrated photonic receiver for turbulence compensation | 硅光芯片 2D 光天线阵列 + MZI mesh 自适应可编程光处理器，光域补偿闪烁 | 期刊 (Sci Rep) | 2024 | 是 | 多孔径接收机 | 🟡（光域补偿偏光前端）|
| 40 | Li — Enhanced Atmospheric Turbulence Resiliency With SIC-DSP in MDM FSO | 模分复用 FSO，连续干扰消除 DSP + 冗余接收通道增强抗湍流，137.8 Gbit/s/mode | Trans (JLT) | 2022 | 是 | 无 SIC | 🟢（DSP SIC 湍流均衡，跨 MDM）|

**AO-DSP 子地带第2批观察**（abstract 层，**不下方向性结论**）：三支并存——①分工式（AO 校正大尺度 → DSP 补残余，但残余多为载波/光机域，**信号域均衡层残余处理文献稀薄**）②替代式（DSP 替代 AO 硬件，Fontaine/Kim）③融合式（DNN+AO 联合，孤证 Chen 2025 venue 可疑不入主表）。未饱和（与 seed "5 篇"一致，本批 A 支核心 3 篇）。**⚠ 边界警示**：A 支 Paillier 系的 DSP 残余实质是数字 PLL 载波相位恢复，落在本专题"载波同步已完成"边界附近，阶段 2 精读若确认 DSP 残余纯为载波域，应按红线排除。

### 子地带 8: 湍流信道均衡（横切特征，🟡 中等偏高，OAM-DL 补偿趋同）

> 湍流是横切损伤，多作为其他子地带的背景。纯粹"湍流均衡"独立成带的少。本组新增论文中与第1批重复的（Horst 2023/Zhang 2021/Zhu 2021/Kulmer 2026/Qin 系列）不重列。

| # | 标题（简） | 做的事 | 档级 | 年份 | 湍流强相关? | baseline 是谁 | 缝潜力 |
|---|---|---|---|---|---|---|---|
| 41 | Chen — Free-Space Comm Turbulence Compensation by Optical Phase Conjugation | OPC 补偿相干 FSO（QPSK）双跳链路湍流失真，phase screen 仿真 | 期刊 (IEEE Photonics J) | 2020 | 是 | 无 OPC 链路 | 🟡（光学硬件补偿，异层）|
| 42 | Senthilkumar — Sparse wavelength aware learning framework for robust FSO channel estimation | 针对湍流+指向误差+波长特异衰减的稀疏学习信道估计框架 | 期刊 (Sci Rep) | 2025 | 是 | 传统信道估计（abstract 提 severely degrade）| 🟢（信道估计/追踪，非 OAM 专用，潜在通用）|
| 43 | Mohammed — FSO turbulent channel estimation based on deep combined CNN | 组合 CNN 做 FSO 湍流信道估计（**孤证**，abstract 无 baseline 细节）| 期刊 (JOC) | 2026 | 是 | abstract 未提 | 🟡（孤证待核）|
| 44 | San — Mitigating atmosphere turbulence fading by relay selections | DQN 选 relay 把长 FSO 链分段缓解湍流 fading（系统/网络层，非物理层均衡）| 期刊 (Photonics) | 2024 | 是 | abstract 未提 | 🟡（系统层）|
| 45 | Ahmad — Robust high-capacity FSO using OAM-based structured light | 结构光提升鲁棒性，**明确点名 "Gaussian beam / static equalization" 为现有不足** | 期刊 (Sci Rep) | 2026 | 是 | Gaussian beam / 静态均衡（abstract 明确）| 🟢（2026，点名 static equalization 为 gap）|
| 46 | Xiong — CNN Based Atmospheric Turbulence Compensation for OAM | CNN 提取涡旋光束畸变特征补偿湍流致螺旋相位失真（引 69）| Trans (JLT) | 2020 | 是 | abstract 未提 | 🟡（OAM 专用）|
| 47 | Ren — Deep-Learning-Assisted OAM Mode Recovery Under Atmospheric Turbulence | DL 恢复湍流致 OAM 模式串扰 | Trans (JLT) | 2025 | 是 | abstract 未提 | 🟡（OAM 专用）|

**湍流信道均衡子地带第2批观察**（abstract 层，**不判 baseline 真失效**）：横切特征 > 独立子地带。OAM 模式扩散 CNN/DL 补偿（#45-47）趋同密集；纯 Gamma-Gamma 建模老文无均衡创新。相对活跃点：实时 multi-aperture digital combining（第1批 #4 Ju，real-time demo 少）/ 多模数字相干补偿（#37 Fontaine）/ ANN 替代 MI-DSP（第1批 #16，2026 新）。

## 第 2 批新增 vs seed.md 交叉核

| 核查项 | 结果 |
|---|---|
| TCOMM 2026 Ajam ISI-IRS 是否召回？ | **✅ 命中**（DOI 匹配 + seed.md + 2 个 JSON 三重确认），第1批漏召的问题解决 |
| seed 的 16 篇 Trans/Letters，第2批新命中？ | JLT 2020 Xiong OAM CNN（#46）/ JLT 2025 Ren OAM DL（#47）/ JLT 2022 Li SIC-DSP（#40）→ 补 3 篇 |
| seed 🔴 OAM-MIMO，第2批是否仍确认？ | **确认**（OAM 模式扩散 CNN/DL 补偿 #45-47 趋同，维持 🔴）|
| 新检索补充 seed 没有的 | Paillier 2019/2020（AO+DSP 残余分工，JLT/ICSOS）/ Fontaine 2019 ECOC（多模数字补偿）/ Kim 2007 EL（电子波前校正奠基）/ Ahmad 2026 Sci Rep（点名 static equalization gap）/ Senthilkumar 2025（稀疏学习信道估计）|
| 两表对不上的子地带（第1批标重点追的）| **ISI 已补**（第1批孤证 → 第2批 5 篇含 TCOMM 2026 Trans + IRS-delay 新切口）。两表现在对得上 |

## 范围出界标注（两批合并，只标不砍，守 INVARIANT 18 星地）

| 论文 | 出界类型 | 处理 |
|---|---|---|
| Vieira 2023 — Modulation and Signal Processing for LEO-LEO Optical ISL (Access) | ISL 无大气（INVARIANT 18 星地）| 标出界，不入主表 |
| PDM-256QAM OAM satellite (Sensors 2023) | 纯仿真非湍流非均衡创新 | 标出界，不入主表 |
| Tang 2012 MPOLSK (JLT) / MIMO BPOLSK 2015 | 调制层非均衡 | 已归偏振但标 🔴（调制非均衡主线）|
| Patnaik 2023 — Equalized Multiplexed IsOWC DP-QPSK | ISL（IsOWC 星间），非星地 | 标出界，不入主表 |
| Farooq 2025 — DFE/MLD/RDE for 5G mm-Wave A-RoF | 光纤 RoF 非 FSO | 标出界，方法参考 |
| Chen 2023 — IRS-Assisted VLC Frequency-Domain（#31）| VLC 非 FSO | 标出界，IRS-delay 同构参考 |

## 偏载波同步排除论文（两批合并，红线检查）

- 组 1：1 篇 "Synchronization of Distant Optical Clocks" (Phys Rev X 2016) → 偏同步排除
- 组 2：1 篇 "16Tbit/s High Order QAM DP Coherent" (SYNCHROINFO 2023，同步会议) → 偏载波同步语境排除
- 组 4：1 篇 Meng 2023 "Two-stage frequency compensation for Doppler shift on BPSK" (Frontiers in Physics) → 偏载波同步排除
- 组 5：1 篇 Wang 2026 "Symbol-Rate Joint Timing Recovery and Equalization for Short-Reach Coherent"（IEEE blit 唯一命中）→ 偏定时同步排除
- **⚠ 边界警示（非排除但需标注）**：组 5 Paillier 2019/2020（#34#35）DSP 残余处理实质是数字 PLL 载波相位恢复，落"载波同步已完成"边界附近，**保留进主表但标边界警示**，阶段 2 精读若确认 DSP 残余纯为载波域则按红线排除。
- **结论**：主表无载波/定时同步论文混入，红线检查 PASS（4 篇排除 + 2 篇边界警示已标注）。

---

## 🔴 死地记忆（饱和子地带，两批合并定稿）

### OAM-MIMO 均衡族（含 OAM 模式扩散 DL 补偿）
- **饱和理由**：①同一架构跨 12 年（2014-2026）反复；②增益趋同（Ren 2015/2016 与 Yousif 2019 增益/模式数接近）；③权威综述 Wang 2021 (Nanophotonics, 340 引) 已收口；④2023 后新论文稀少（仅 Hu 2023 自适应收发）；⑤OAM 模式扩散的 CNN/DL 补偿（Xiong 2020 / Ren 2025 / Ahmad 2026）趋同密集，coherent 性普遍弱。两批交叉核一致。
- **代表论文**：Ren 2015 (OL, 92 引)、Ren 2016 (OL, 98 引)、Wang 2021 综述 (340 引)、Xiong 2020 (JLT, 69 引)。
- **下次不重复撞墙**：默认归死地，不投精读资源。

### 偏振均衡（经典外差相干奠基思路）
- **饱和理由**：Cvijetic 2010 (JLT, 93 引) 奠基后"偏振态旋转→well-known 均衡消除 XPI"成标准范式。
- **注意**：偏振均衡**整体不死**——2025-2026 DP 自相干+湍流偏振混叠切口（ANN/VAE）仍活跃。死的只是经典外差偏振态旋转均衡这一奠基思路。

### OFDM-FSO 解析性能评估类
- **饱和理由**：Gamma-Gamma/Rician 信道 SER/中断概率闭式推导密集趋同，多理论 BER 分析，实验/工程实体少。
- **注意**：OFDM-FSO 整体 🟡（NE-OFDM 反向角度 + UAV 仍有产出）。

### 纯硬件 AO 校正族（组5排除项）
- **饱和理由**：SPGD/AdamSPGD/NadamSPGD + DM/FSM 级联 + 高单元数 AO，连续多年趋同优化 AO 收敛速度/单元数，纯硬件无 DSP 残余信号处理。
- **代表**：Anzuola-Belmonte 系（2013-2018）、SPGD 三篇、349 单元 AO。

---

## 阶段 1 地勘信噪比合格终判（PROMPT-001 验收）

- [x] 子地带覆盖 ≥3 个不同 → **8 个**（MDCC/OAM-MIMO/偏振/ISI/OFDM-FSO/DNN/AO-DSP/湍流信道）✅
- [x] 候选论文够多 → **~46 篇主表**（第1批29 + 第2批17 新增去重）✅
- [x] 档级标注完整（Trans/Letters/会议/期刊/preprint 分层）✅
- [x] 🔴死地记忆段有理由 + 代表论文 → **4 个死地**（OAM-MIMO/偏振经典/OFDM解析/纯硬件AO）✅
- [x] 无载波同步混入主表（红线 PASS，4 篇排除 + 2 篇边界警示）✅
- [x] 检索覆盖度诚实（列了未覆盖：Exa 全程失效 / IEEE blit 近失效 / SerpAPI 缺失 / 部分 abstract 缺失）✅
- [x] **没有判据 A 结论**（没下"baseline 真失效"，只标 🟢/🟡/🔴 粗判）✅
- [x] §7.2 主线核查（两批各抽 3 篇，6 篇全 PASS 无造假）✅

**信噪比合格 → 阶段 1 地勘收尾，可进阶段 1.5 选地。**

---

> **阶段 1 地勘总结（两批合并）**：8 子地带，~46 篇主表，4 个 🔴死地。**未判 baseline 真失效**（守 INVARIANT 6），缝潜力仅 🟢/🟡/🔴 粗判。
>
> **子地带活跃度初判（abstract 层，供阶段 1.5 选地参考，非方向结论）**：
> - 🟢 **MDCC（multi-aperture coherent combining）最活跃**：Geisler 奠基 → Liu/Ju 2023-2024 DSP 进阶 → Johst/Chen 2026。**Trans 基线池最厚**（JLT/OE/OL 多篇）。
> - 🟢 **偏振均衡升温**（DP 自相干+湍流偏振混叠切口）：Cvijetic 奠基 → ANN/VAE 2026（孤证）。
> - 🟢 **DNN/NN 均衡新兴**：Kulmer/Qin/ANN/VAE（多孤证，Trans 级少）。
> - 🟡 **ISI 均衡**：稀疏 + IRS-induced ISI 全新切口（Ajam 2026 TCOMM 单篇 Trans）。
> - 🟡 **AO-DSP 残余补偿**：三支并存但核心 A 支含载波恢复边界风险。
> - 🔴 **OAM-MIMO**：12 年饱和死地。
>
> **⚠ 守 INVARIANT 6**：以上"活跃/升温/新兴"是 abstract 层观察（多方法并存可能竞争），**不是判 baseline 真失效**。判缝移全文层（阶段 2/3）。阶段 1.5 选地交主控对话 + 用户拍板。
