# FSO 相干均衡全谱地勘（landscape）

> 创建: 2026-07-10 | 专题: 2026-07-10-equalization-layer-direction-scouting
> 阶段: GW Step 1 地勘前置（第 1 批，组 1-3）| 产出供阶段 1.5 选地
> 纪律: abstract 层只找候选清单，禁判判据 A（baseline 真失效）。判缝移全文层（阶段 2/3）。
> 本批范围: 组 1（equalization 总览）+ 组 2（偏振）+ 组 3（MIMO/combining）。组 4-6（ISI 深/AO-DSP/湍流补偿）待第 2 批。

## 检索覆盖度（诚实标注）

- 检索组数: 3（组 1 equalization 总览 / 组 2 偏振 / 组 3 MIMO-combining）
- 检索源: `tools/search`（S2/OpenAlex 正常）+ `tools/blit --source ieee`（3 次均≈0 命中）
- **源状况诚实标注**：
  - S2 + OpenAlex 正常工作
  - **Exa 信用额度耗尽**（NO_MORE_CREDITS）→ 本批未用到 Exa 语义搜索
  - **SerpAPI 未安装 / Tavily 连接重置** → 召回源减少
  - **IEEE blit 3 次查询均返回 0 命中**（会话用量 1/50，疑关键词无全文匹配或限速生效）→ venue 字段主要靠 OpenAlex/S2 `container_title`
- 候选论文总数（本批，去重后相关）: **29 篇**（主表）
- 子地带覆盖（本批发现 7 个）: multi-aperture coherent combining / OAM-MIMO 均衡 / 偏振均衡 / ISI 均衡 / OFDM-FSO / DNN-NN 均衡 / AO-DSP 残余补偿
- **未覆盖（诚实）**:
  - 组 4-6 未跑 → ISI 均衡子地带召回薄（仅 1 篇孤证 Zhang 2018），TCOMM 2026 IRS-FSO ISI 未召回
  - AO-DSP 残余补偿 / 湍流信道均衡 专门检索未跑（本批仅组 1 边缘召回 Horst 2023 / Zhang 2021）
  - 纯时域 FSE/DFE 专门对比、Kalman/LMS 自适应专门论文未见专门命中（关键词可能未覆盖，待组 4 补）
  - Exa 语义搜索缺失可能漏掉部分语义相关但关键词不匹配的论文
  - IEEE blit 0 命中 → 可能漏 IEEE 全文库独有论文（PTL/CL 等）

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
| 两表对不上的子地带（重点追对象） | **ISI 均衡**（seed 标 11 篇含 TCOMM 2026，本批仅召回 1 篇孤证）→ **组 4 重点追** |

## 范围出界标注（只标不砍，守 INVARIANT 18 星地）

| 论文 | 出界类型 | 处理 |
|---|---|---|
| Vieira 2023 — Modulation and Signal Processing for LEO-LEO Optical ISL (Access) | ISL 无大气（INVARIANT 18 星地）| 标出界，不入主表 |
| PDM-256QAM OAM satellite (Sensors 2023) | 纯仿真非湍流非均衡创新 | 标出界，不入主表 |
| Tang 2012 MPOLSK (JLT) / MIMO BPOLSK 2015 | 调制层非均衡 | 已归偏振但标 🔴（调制非均衡主线）|

## 偏载波同步排除论文（红线检查）

- 本批检索词未加 `synchronization`，组 1 召回 1 篇 "Synchronization of Distant Optical Clocks at Femtosecond Level" (Phys Rev X 2016) → **偏同步排除**，不入主表。
- 组 2 召回 1 篇 "16Tbit/s High Order QAM DP Coherent" (SYNCHROINFO 2023，发表于信号同步会议) → **偏载波同步语境排除**，且为光纤非 FSO。
- seed.md 标注的 JPhoton 2023 "Flexible phase synchronization" 含 phase synchronization → 本批未召回（合规，组 1-3 检索词不含 sync）。
- **结论**：本批无载波同步论文混入主表，红线检查 PASS。

---

> **本批地勘小结**：7 子地带覆盖（≥3 信噪比合格判据 ✅），29 篇主表 + 死地记忆 + 交叉核完整。**未判 baseline 真失效**（守 INVARIANT 6），缝潜力仅 🟢/🟡/🔴 粗判。组 4-6（ISI 深查 / AO-DSP / 湍流补偿）待第 2 批补检索后进阶段 1.5 选地。
