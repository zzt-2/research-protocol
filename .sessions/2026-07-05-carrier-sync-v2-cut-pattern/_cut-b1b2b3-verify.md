# dB/复杂度核验：B1 + B2/B3 池 14 篇

> 核验人：子 agent | 日期：2026-07-05 | 任务：abstract 级 → 全文级 dB/复杂度细档
> 纪律：D018 中性提取（只核验不重写笔记，不改 `_cut-*.md` 也不改 `_B*.md`）；FR-26 证据链（content.md 没明写的数字不编，读不到标"content.md 未提及"）；不判 Go/Kill；每个 dB 数字带"在 X 条件下 vs Y baseline"；复杂度档位精确（FPGA 型号 / 链路长度 / 湍流强度是关键区分点）。

---

## 核验状态汇总

| # | DOI | 池 | 落盘 | dB 形态 | 复杂度档 |
|---|---|---|---|---|---|
| 1 | 10.1109/jlt.2012.2187635（L004） | B1 | ❌ 未落盘 | 保持粗档（无 dB 仅结构性） | 保持粗档（abstract 提 trellis+量化 phase space，无算力） |
| 2 | 10.1109/lpt.2012.2187439（L003） | B1 | ❌ 未落盘 | 保持粗档（abstract 仅"outperforms"无数字） | 保持粗档（abstract 未明说） |
| 3 | 10.1364/oe.27.024654（L008） | B1 | ❌ 未落盘 | 保持粗档（abstract 给 SE 9.3/8.3 bits/s/Hz + 11.9/10.6 Tb/s，dB penalty 在正文） | 部分升级（abstract 已知实测级：51×24 Gbaud PM-64QAM superchannel 1000 km） |
| 4 | 10.1109/lcomm.2016.2542798（L030） | B1 | ❌ 未落盘 | 保持粗档（abstract 仅"compared to PLL directly adapts"，无数字） | 保持粗档（abstract 提仿真，未给算力） |
| 5 | 10.1109/jlt.2019.2959395（L009） | B1 | ❌ 未落盘 | 保持粗档（abstract 给"reducing/eliminating shaping gains"无 dB 数字） | 部分升级（abstract 已知：offline experimental data + noise loading） |
| 6 | 10.1109/jlt.2020.2976166（L035） | B1 | ❌ 未落盘 | 保持粗档（abstract 未明写 SNR penalty 0.25 dB；B1 草稿引用的 0.25 dB/0.38/0.34 pJ/bit 待全文核） | 部分升级（abstract 已知 22 nm CMOS 工艺，pJ/bit 能效维度） |
| 7 | 10.1109/ICCWorkshops59551.2024.10615713（L053） | B1 | ✅ 全文 327 行 | **升级到细档** | **升级到细档** |
| 8 | 10.1002/sat.1553 | B1/B2/B3 共锚 | ✅ 全文 1581 行 | **升级到细档** | **升级到细档** |
| 9 | 10.1117/12.2544050（Matsuda[79]） | B2 锚 | ⚠️ 仅摘要（付费墙穷尽降级失败） | 保持粗档（摘要 +0.6 dB 已有，但无细节） | 保持粗档（摘要已知 FPGA 实时 4 Gbps，无型号/资源） |
| 10 | 10.1109/jlt.2020.3003561（Paillier 2020 JLT） | B2 baseline 分支 | ✅ 全文 + 笔记 | **升级到细档** | **升级到细档** |
| 11 | 张思齐学位论文（无 DOI） | B3 池 | ✅ B3 笔记（无原文） | **升级到细档**（笔记已含 0.67~0.76 dB / 13.8%~47.6% / NMSE 1e-7~1e-10） | **升级到细档**（笔记已含纯仿真，无硬件，章 5.2 自陈局限） |
| 12 | 10.1109/LCOMM.2026.3651445 | B3 锚 | ✅ 全文 + 笔记 | **升级到细档** | **升级到细档** |
| 13 | 10.1109/jphot.2023.3265847 | B3 锚 | ✅ 全文 + 笔记 | **升级到细档** | **升级到细档** |
| 14 | 10.1364/oe.520452 | B3 锚 | ✅ 全文 + 笔记 | **升级到细档** | **升级到细档** |

---

## 逐篇核验

### 篇 1：10.1109/jlt.2012.2187635（L004）— Information Rate Through Wiener Phase Noise Channel

- **落盘状态**：❌ 未落盘。`papers/doi/10.1109_jlt.2012.2187635/` 目录不存在；arxiv/手动/blit-downloads 均无；index.json 无记录；repo 内全文检索无 "spalvieri" 命中（仅 `_cut-b1-spalvieri-pool.md` abstract 级引用）。
- **dB 形态核验**：
  - 数字：无 dB（保持 B1 草稿"无 dB 仅结构性"判定）。
  - 对照：内容是信息率上下界（bits）的收敛性，不是 SNR penalty。
  - 条件：N/A（理论界论文）。
  - 升级判定：**保持粗档**——abstract 级判定"信息率上下界，无 dB"已正确，全文核验未做因未落盘。
- **复杂度细档核验**：
  - 档位：纯理论/计算仿真（abstract 提 trellis + 量化 phase space）。
  - 关键参数：content.md 未提及（未落盘）。
  - 升级判定：**保持粗档**。
- **下载建议**：**中价值**——L004 是信息率界子类的代表，对切法地图"dB 形态分布"统计价值低（理论界类无 dB），但若主线想统计"信息率界 vs pilot rate"的折中曲线细节可补；非优先。

### 篇 2：10.1109/lpt.2012.2187439（L003）— Pilot-Symbols-Aided CPR for 100-G PM-QPSK

- **落盘状态**：❌ 未落盘（同上，无 DOI 目录、无 arxiv、无记录）。
- **dB 形态核验**：
  - 数字：abstract 仅一句 "for homogeneous transmission, the proposed scheme outperforms blind carrier recovery with differential decoding"（**无具体 dB 数字**）。
  - 对照：vs blind + differential decoding（baseline 明确）。
  - 条件："homogeneous transmission"（单跨段/无色散补偿光纤，具体条件在正文）。
  - 升级判定：**保持粗档**——dB 数字待正文（abstract 未给）。
- **复杂度细档核验**：
  - 档位：abstract 提 100-G PM-QPSK（速率已知）；dual-stage 复杂度增加但 abstract 未量化。
  - 关键参数：100-G PM-QPSK（abstract）；其余 content.md 未提及。
  - 升级判定：**保持粗档**。
- **下载建议**：**高价值**——L003 是 Spalvieri 池"vs blind+diff baseline"dB 数字的核心证据之一（与 L053 一起代表"赢传统 baseline 1-2+ dB"类）；abstract 无数字但正文大概率有，建议补。

### 篇 3：10.1364/oe.27.024654（L008）— Overhead-optimization of pilot-based DSP

- **落盘状态**：❌ 未落盘（同上）。
- **dB 形态核验**：
  - 数字：abstract 给 spectral efficiency 9.3 / 8.3 bits/s/Hz 和 throughput 11.9 / 10.6 Tb/s（**这是 SE/吞吐量，非 SNR penalty dB**）；具体 dB penalty 在正文。
  - 对照：abstract 提"back-to-back optimization is sufficient"（vs 不同传输距离对照）。
  - 条件：51×24 Gbaud PM-64QAM superchannel，1000 km 传输。
  - 升级判定：**保持粗档**（dB penalty 维度）——abstract 给的是 SE 数字不是 dB penalty。
- **复杂度细档核验**：
  - 档位：**实测级**（abstract 已知）。
  - 关键参数：51×24 Gbaud PM-64QAM superchannel，1000 km 传输实测（abstract）。
  - 升级判定：**部分升级**——abstract 已能确认实测档 + 关键参数，dB penalty 维度待正文。
- **下载建议**：**中价值**——abstract 已能定档（实测 + superchannel 1000 km），dB 细节非主线必需；如做"pilot overhead 优化的 dB 量级"对比可补。

### 篇 4：10.1109/lcomm.2016.2542798（L030）— Joint Phase Recovery for XPIC using Adaptive Kalman

- **落盘状态**：❌ 未落盘（同上）。
- **dB 形态核验**：
  - 数字：abstract 仅 "compared to a common PLL approach, the proposed Kalman-based algorithm directly adapts its parameters"（**无 dB 数字**）。
  - 对照：vs common PLL approach（baseline 明确）。
  - 条件：XPIC（cross-polar interference cancellation）双极化场景，参数按 Eb/N0 + XPD 自适应。
  - 升级判定：**保持粗档**——dB 待正文。
- **复杂度细档核验**：
  - 档位：abstract 提仿真验证；四状态模型（vs 二状态）。
  - 关键参数：content.md 未提及（未落盘）。
  - 升级判定：**保持粗档**。
- **下载建议**：**高价值**——L030 是 Spalvieri 池"自适应 Kalman 参数调度"角度独占小变体（与 B1 切入点的"参数自适应"思路结构相似），dB 量级对 B1 切入点的"参数自适应能否赢 baseline 几 dB"判断有直接参考价值；建议补。

### 篇 5：10.1109/jlt.2019.2959395（L009）— Phase & Frequency Recovery for Probabilistically Shaped

- **落盘状态**：❌ 未落盘（同上）。
- **dB 形态核验**：
  - 数字：abstract 给 "reducing or even eliminating the expected shaping gains"（**无单一 dB 数字**，是 PS 增益是否被 CPR 损坏的定性判定）。
  - 对照：vs shaping gain 上界 + PS 在中低 SNR 损坏 BPS 的内部对照。
  - 条件：PS（probabilistic shaping）+ laser imperfections + additive noise loading。
  - 升级判定：**保持粗档**——dB 形态偏结构性，正文大概率也是 shaping gain 损坏百分比而非单一 SNR penalty dB。
- **复杂度细档核验**：
  - 档位：**实测级**（abstract 已知：offline processing of experimental data with laser imperfections + noise loading）。
  - 关键参数：content.md 未提及具体调制/符号率/链路长度（未落盘）。
  - 升级判定：**部分升级**——abstract 已能确认实测档 + offline processing，具体参数待正文。
- **下载建议**：**中价值**——abstract 已能定档（实测 + PS 场景），dB 形态偏结构性（与切法地图判断一致）；如做"PS 场景 CPR SNR-driven 切换"细节可补。

### 篇 6：10.1109/jlt.2020.2976166（L035）— VLSI Implementations of CPR for M-QAM

- **落盘状态**：❌ 未落盘（同上）。
- **dB 形态核验**：
  - 数字：B1 草稿引用 "SNR penalty ≈0.25 dB @ BER 1e-2（BPS）" + "pilot-aided 0.38/0.34 pJ/bit（16/256-QAM）"——**这是 B1 草稿 abstract 级引用，content.md 未核验（未落盘）**。
  - 对照：vs 理想算法（硬件实现引入的 penalty）。
  - 条件：22 nm CMOS。
  - 升级判定：**保持粗档（标"待全文核"）**——草稿引用的 0.25 dB / 0.38/0.34 pJ/bit 来源不明（abstract 未明写），需全文核验才能确认；FR-26 警示。
- **复杂度细档核验**：
  - 档位：**VLSI 档**（abstract 已知）。
  - 关键参数：22 nm CMOS 工艺（abstract 明说），pJ/bit 能效维度；具体 silicon area / 定点位宽 / averaging window 待正文。
  - 升级判定：**部分升级**——abstract 已能确认 VLSI 档 + 22 nm CMOS，资源/面积细节待正文。
- **下载建议**：**高价值**——L035 是 Spalvieri 池"VLSI 实现"角度独占（B1 草稿判"复杂度最高切法"），dB 形态（硬件 penalty）+ 能效 pJ/bit 双维度，对切法地图"实现复杂度梯度"维有直接价值；建议优先补，特别是核验 B1 草稿引用的 0.25 dB 是否原文存在。

### 篇 7：10.1109/ICCWorkshops59551.2024.10615713（L053）— DLAE ⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1109_iccworkshops59551.2024.10615713/content.md`（327 行全文）。
- **dB 形态核验**：
  - 数字：**abstract vs 正文存在差异，需精确区分**：
    - abstract 报 "DLAE outperforms PSAM by **over 2 dB** at the 10⁻⁶ level across 256-QAM, 1024-QAM, and 4096-QAM"——这是**总 gap**（PSAM gap > 3 dB vs Genie，DLAE 把 gap 缩到 0.8~1.2 dB，所以"赢 PSAM ≥ 2 dB"是间接计算）。
    - 正文 §V-B（line 268）精确："leaving a remaining gap of **approximately 0.8 dB for 256-QAM** and **around 1.2 dB for the other two modulation sizes**"——这是 DLAE 距离 Genie（无 PN）的 gap。
    - 正文同时："the PSAM scheme exhibits a **gap exceeding 3 dB** or faces an error floor"。
    - 结论：**DLAE vs PSAM 在 BER=10⁻⁶ 处的实际差 = (PSAM gap > 3 dB) − (DLAE gap 0.8~1.2 dB) ≈ 2~3 dB**（abstract 的"over 2 dB"是这个差，方向正确）。
  - 对照：vs PSAM（Pilot-Symbol Assisted Modulation，baseline 明确）；副对照 vs Genie PN 估计 + AWGN w/o PN（理论上界）。
  - 条件：256/1024/4096-QAM coded modulation；PN levels −88/−92/−96 dBc/Hz @100 kHz offset（对应 ν=0.27°/0.17°/0.11°）；5G-NR LDPC (7258, 8064) code rate 0.9 + 30 iterations；pilot spacings L=100, 150（256/1024-QAM）和 L=75, 100（4096-QAM）；带宽 28 MHz；AWGN 信道（无线 backhaul，line-of-sight）；Ed=1, Ep=2.5（pilot 能量比）。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 只给"over 2 dB"，全文补出 0.8/1.2 dB 的精确 DLAE-to-Genie gap + PSAM gap > 3 dB，可重算实际差。
- **复杂度细档核验**：
  - 档位：**纯仿真 + DL 训练**（无 FPGA/ASIC/实测）。
  - 关键参数：
    - 仿真：256/1024/4096-QAM，28 MHz 带宽，5G-NR LDPC（7258, 8064），Tensorflow + Sionna 库（line 165），Adam optimizer lr=10⁻⁴，训练 15000 iterations，3 个 SNR 训练范围（14-18/19-23/24-30 dB 对应三种调制）。
    - CNN 架构：2D CNN，filter size (fw, fh) = (3, 8)，Nf=8，3 个 hidden CB layers + 1 output layer；K=20, κ=3.5；M'=50（look-up table 截断）。
    - 复杂度（§IV，line 173-179）：FLOPs/PN sample = (10 + 30M')K + 2T(T+2)(fwfh+1) + K + 1，**与 pilot spacing L 和 constellation size M 都无关**（abstract 已说，正文给完整推导）；memory scales with L。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 只说"CNN size 复杂度独立于 constellation size"，全文补出 FLOPs 公式、CNN 架构参数、训练配置、Tensorflow+Sionna 工具链。
- **下载建议**：已落盘，无需补。

### 篇 8：10.1002/sat.1553（Valjus 2025 OSL DSP 综述）⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1002_sat.1553/content.md`（1581 行全文 + `papers/_read_notes/10.1002_sat.1553.md` 笔记）。
- **dB 形态核验**（综述内部对照，全部 @ BER 1e-3，4 场景：ISL/下行/上行弱湍 σp²=0.15/上行强湍 σp²=0.25）：
  - **定时恢复**（§4.1）：linear interpolation vs Lagrange/trig **penalty 0.2~0.3 dB**（小滚降 0.3 dB @ 场景 1-2，场景 3-4 ~0.2 dB）（content.md L382）；Godard 算法在 parallelization factor 256 + latency 20 cycles 下能 track 到 ~60 ppm clock offset（无 dB penalty，是跟踪范围）。
  - **载波相位估计**（§4.2，关键）：
    - **soft DQPSK penalty ~2.5 dB**（content.md L416，引 [55]）。
    - **hard DQPSK penalty 0.75 dB**（L416，引 [55]）。
    - **Viterbi–Viterbi + differential coding 在 scenario 4 penalty ~1.5 dB**（L440）。
    - **pilot 在 scenario 4 比 VV+diff 好 1 dB**（L440，B1 草稿引用的"1 dB"原文核验通过）。
    - **soft-FEC vs hard-FEC 增益 ~2 dB**（L440，引 [59]），代价是硬件复杂度增加。
  - **自适应 pilot rate**（L440，B1 切入点 open problem 自报）：
    - 综述作者亲口："the same pilot rate performs similarly for all scenarios"（**负向信号**——固定 pilot rate 跨场景差异不大，暗示自适应 pilot rate 增益可能平缓）。
    - "Further research is necessary to identify practical methods for dynamically adjusting the phase estimation window and **to quantify the potential gain**"（**自承未量化**，与 B1 笔记判断一致）。
  - **载波频偏估计**（§5）：blind 时域 ±fs/2ML；blind 频域 ±fs/2M（28 GBaud QPSK → ±3.5 GHz）；data-aided ±fs/2（±14 GHz）；Schmidl-Cox ±fs/2N。**无 dB penalty 数字**（只有估计范围）。
  - **均衡器**（§6）：
    - **two-stage equalizer 在 6 ps DGD 下 1 dB penalty**（L572，引 [76]）；DGD < 1 ps 时 penalty 可忽略。
    - **RSOP 0.03 rad 已 > 1 dB penalty**（L745，Fig.12）。
    - MMSE SOP 跟踪速度 ~10⁻⁷ rad/symbol（≈ 1-10 krad/s @ 28 GBaud）保持 penalty < 1 dB；DA-LMS/CMA 可跟踪 > 10⁻⁵ rad/symbol（≈ 300 krad/s @ 28 GBaud）。
  - **deep fade 冻结**（B2 切口，§5/§7）：L558 "avoid updating the estimate when signal quality degrades"；L582 "turn off tracking when incoming signal power is low [79]"——**无 dB**（仅设计建议，引 Matsuda[79]）。
  - **子系统协同**（B3 切口，Conclusion L790）：open problem 陈述，**无 dB**（仅"P+CPE 可共享 pilot，依赖 timing recovery"结构性陈述）。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 几乎无 dB 数字（综述类），全文补出 8+ 个具体 dB 数字 + B1/B2/B3 三切口的 dB 形态精确定性。
- **复杂度细档核验**：
  - 档位：**纯综述 + 计算机仿真**（无 FPGA/ASIC/实测硬件）。
  - 关键参数：
    - 4 场景仿真：ISL（β 指向误差）/下行（lognormal σp²=0.029）/上行弱湍（σp²=0.15）/上行强湍（σp²=0.25），平均 BER 目标 1e-3，SNR ±3 dB 扫描（content.md L150）。
    - 调制：QPSK 主，提 DP-QPSK/M-QAM；10 GBaud + 28 GBaud；滚降 0.2。
    - **湍流建模（关键简化）**：line 167 明确"we will not model the coherence time ... consider the channel **quasi-static**"——**湍流被当作准静态 SNR 分布，不建模动态相位扰动**；相位噪声专指激光线宽随机游走（式17，σ²=2πΔw·Ts）。
    - CFO 算法配置：blind L=1；频域 FFT 64/4096；data-aided preamble 128/512；Schmidl-Cox N=64；CRT [8,9,72]/[11,12,132]。
    - 定时恢复并行化：64/256 samples/cycle，环延迟 20 cycles。
    - 均衡器：30-40% 接收机 DSP 总功耗（引 [74][75]）；CMA/DA-LMS/MMSE 算法对比。
    - AO 不在 DSP 综述范围（光域，本文不讨论）。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 只说"4 场景仿真 + DSP 算法地图"，全文补出完整参数表 + 准静态假设（B1 gap 核心证据）+ 30-40% 功耗占比 + AO 边界声明。
- **下载建议**：已落盘，无需补。

### 篇 9：10.1117/12.2544050（Matsuda[79]）— FPGA Implementation of Scintillation Tolerant Adaptive DSP

- **落盘状态**：⚠️ 仅摘要（`papers/doi/10.1117_12.2544050/content.md` 60 行，是 web reader 抓取的 SPIE 摘要页 + sat.1553 引用语境核验，**全文 PDF 穷尽降级失败**：Unpaywall is_oa=False、SPIE 直链 JS 挑战、SPIE Playwright 0 字节、NASA ADS Cloudflare 拦截、NICT/CiNii 未收录、ResearchGate 仅题录）。
- **dB 形态核验**：
  - 数字：**摘要报灵敏度提升 0.6 dB**（content.md L21，offline evaluation，FO fluctuation reduction by scintillation，**vs 自身无 freeze baseline**——B2 笔记陷阱 1 已正确标注：0.6 dB 是 [79] 自身相对无冻结 baseline 的增益，不是 B2 候选相对 [79] 的增量）。
  - 对照：vs 无 FO estimator freeze 的 baseline（摘要内部对照）。
  - 条件：scintillation fading 场景（Cn²/湍流强度未在摘要给）；4 Gbps 相干接收。
  - 升级判定：**保持粗档**——0.6 dB 已是摘要级精确数字，全文细节（不同湍流强度下的 dB 变化、freeze 阈值如何选）不可得。
- **复杂度细档核验**：
  - 档位：**FPGA 实时 + offline 双评测**（摘要已知）。
  - 关键参数：
    - FPGA 实现 + 实时 4 Gbps 相干接收（摘要）；**FPGA 型号未给**（摘要级看不到）；资源（LE/DSP/BRAM）/定位点宽/实时时钟频率均**未给**。
    - offline 评测 + 实时测试（offline-generated fading signals）双轨。
    - 湍流条件：摘要只说"scintillation"，**Cn²/Rytov 未给**。
  - 升级判定：**保持粗档**——FPGA 型号/资源/湍流强度全在正文，摘要级不可得。
- **下载建议**：**低价值（已穷尽降级失败）**——付费墙 + 无 OA + 无机构库副本，再投入产出比低；摘要 0.6 dB + FPGA 实时 4 Gbps 已够切法地图定档。如主线要 FPGA 资源数字需通过 SPIE 订阅或馆际互借（非 agent 自动可获）。

### 篇 10：10.1109/jlt.2020.3003561（Paillier 2020 JLT）⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1109_jlt.2020.3003561/content.md` + source.tar.gz（arXiv 1911.11851 LaTeX 源）+ `papers/_read_notes/10.1109_jlt.2020.3003561.md` 笔记。
- **dB 形态核验**：
  - 数字：
    - **湍流 fading 致 2.3 dB BER penalty**（笔记 L36，vs AWGN 理论，@ BER=1e-4）。
    - **幅度起伏致最小临界 SNR 从 −9 dB 升到约 −4 dB（5 dB 退化）**（笔记 L35，DPLL 失稳点）。
    - **AO flux penalty −4.5 dB**（笔记 L37，AO 校正后平均通量损失）。
    - **100 MHz 残频 pull-in ms 量级，无 BER penalty**（笔记 L38）。
    - 加湍流相位 vs 不加：DPLL 输出相位误差方差 **negligible difference**（笔记 L34，"湍流相位噪声对载波同步可忽略"核心结论）。
  - 对照：vs AWGN 理论（BER penalty）+ 内部对照（临界 SNR 退化）+ AO 校正前/后（flux penalty）。
  - 条件：**极强条件性**——BPSK 单一调制 + 10 GBaud + 1550nm + 理想 timing recovery + AGC 维持恒幅（Kd=1）+ AO 校正后残余 piston 相位慢（~1ms 相干时间）+ 总频偏 ~9 GHz（假设主要部分由 coarse frequency estimator 预补偿，DPLL 只 track 残频 100 MHz）。
  - 升级判定：**abstract 粗档 → 全文细档**——笔记已含 4 个精确 dB 数字 + 条件性全公开（D006 复核时的关键证据基础）。
- **复杂度细档核验**：
  - 档位：**纯数值仿真**（无硬件实现）。
  - 关键参数：
    - 链路：LEO-to-ground 下行，BPSK 10 GBaud，1550 nm，intradyne 相干检测。
    - 湍流建模（**最深的信道建模**）：Hufnagel-Valley Cn²(h) 剖面（h_max=20 km）+ Bufton 风剖面 + 数值相位传播 + Fried 参数 r_0 + 闪烁指数 σ²_I；2 秒真实湍流时间序列。
    - AO 系统：Zernike 多项式 up to mode 91（12 radial orders），闭环 5 kHz 采样 + 2 frame loop delay。
    - DPLL：二阶（phase detector + loop filter + NCO）；ωn=9.3 MHz, ξ=1/√2, B_LT=0.0005, Kd=1（AGC 维持），残频 100 MHz；pull-in time Tp=2Δω²/(ξ·ωn³)。
    - 相位检测器：BPSK MAP 最优（ε=s_Q·tanh(s_I)），低 SNR 近似 ε=s_I·s_Q。
    - 多普勒：总频偏 ~9 GHz（Shoji 引用），假设主要部分由 coarse frequency estimator 预补偿。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 级看不到湍流建模深度，全文补出 Hufnagel-Valley + Zernike 91 + Bufton 全套信道参数 + DPLL 完整设计公式。
- **下载建议**：已落盘（arXiv LaTeX 源公开），无需补。

### 篇 11：张思齐学位论文（无 DOI）— B3 池

- **落盘状态**：⚠️ **无原文**，仅在 `papers/_read_notes/_B3-subsystem-coordination-increment.md` 笔记里有结构性 dB/复杂度数据（B3 笔记 §1 张思齐段，行号是笔记内引用，非论文原文页码）。
- **dB 形态核验**：
  - 数字（全部来自 B3 笔记，标记"论文原报，未脑补"，但**未对照原文核验**）：
    - **第二章 FOE 并行化 vs QPSK 分圈：接收机灵敏度 B2B/弱湍/强湍 +0.67/+0.76/+0.71 dB**；复杂度 27.2%（符号块 1024）。
    - **第三章 JCR-IFOE/JCR-AFOE vs 4th-FFT 和 QPSK Partitioning：复杂度仅 13.8%/47.6%（IFOE）、13.7%/47.3%（AFOE）**；NMSE 达 10⁻¹⁰/10⁻⁹（FOE 符号块 320、CPE 符号块 64）。
    - **第四章 vs Cheng 联合 FS+FOE：残余 FOE 复杂度仅 17%**，NMSE 10⁻⁷。
  - 对照：vs QPSK 分圈 / 4th-FFT / QPSK Partitioning / Cheng 联合 FS+FOE（baseline 明确，载波恢复经典算法线）。
  - 条件：FSO/光相干（B2B/弱湍/强湍三档），具体调制/符号率/湍流模型笔记未载。
  - 升级判定：**abstract 粗档 → 笔记级细档**（不是原文级）——B3 笔记已含完整 dB + 复杂度百分比 + NMSE；但 FR-26 警示：**笔记数据未对照原文核验**，张思齐原文不在 papers/ 下。
- **复杂度细档核验**：
  - 档位：**纯仿真，无硬件实现**（张思齐自陈 §5.2，B3 笔记 L23）。
  - 关键参数：FOE 符号块 320/960/1024、CPE 符号块 64；湍流分 B2B/弱湍/强湍三档（Cn² 未载）；调制/符号率/线宽笔记未载。
  - 升级判定：**abstract 粗档 → 笔记级细档**——档位明确（纯仿真无硬件），关键参数部分载（符号块大小、湍流档位），调制/符号率待原文。
- **下载建议**：**中价值（CNKI 学位论文）**——若主线要核验 dB/复杂度百分比的原文准确性，需补 CNKI 全文；当前 B3 笔记数据够切法地图定档用。

### 篇 12：10.1109/LCOMM.2026.3651445（LPT FPT 解耦）⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1109_LCOMM.2026.3651445/content.md` + source.pdf + `papers/_read_notes/10.1109_LCOMM.2026.3651445.md` 笔记。
- **dB 形态核验**：
  - 数字：
    - **Q-factor 较 PTJ（前作）+0.9 dB**（@ OSNR 25 dB）。
    - **相对常规 4×4 MIMO+BPS 仅 −0.1 dB penalty**（PTJ 为 1.0 dB）——即"持平 MIMO+BPS"。
    - **RMSE 4.47° vs PTJ 17.99°**（@ OSNR 25 dB, θ=5°, 200 ns）——相位精度提升 4 倍。
    - **RSOP 跟踪速率 100 Mrad/s**（无迭代，直接算 Jones 矩阵）。
    - **实验 40 km SSMF + 10 krad/s SOP 扰模：LPT 较 PTJ 减少 0.7 dB ROP penalty**（@ 7% HD-FEC 阈值）。
  - 对照：vs PTJ（前作联合矩阵估计）/ PTC（3-FPT）/ 常规 4×4 MIMO+BPS（reference benchmark）/ Wu 双载辅相。
  - 条件：**光纤 DSCM**（40 km SSMF，数据中心短距），DP-16QAM，4 子载波 × 8 GBaud，子载波中心 ±15/±5 GHz，RRC roll-off 0.1；FPT 频率 f1=f2=10 GHz；导频功率比 PSR=−15 dB（导频占 3.16%）；LPF 带宽 200 MHz（LPT）/90 MHz（PTJ）；激光线宽 3 MHz DFB；RSOP 扰模器注入 10 krad/s；OSNR 19-25 dB；静态 RSOP θ=5° 测精度，动态 RSOP 扫描至 10⁵ krad/s。
  - 升级判定：**abstract 粗档 → 全文细档**——笔记已含 5 个精确 dB + RMSE + 跟踪速率 + 实验条件全公开。
- **复杂度细档核验**：
  - 档位：**仿真 + 中等强度实验**（40 km SSMF 实验）。
  - 关键参数：
    - 链路：40 km SSMF，**非星地、非湍流**（光纤 DSCM）。
    - 实验：Keysight 8199A / UXR0594AP（AWG/RTO，64 GSa/s）+ BOX Optronics DFB 激光器 + polarization scrambler 注入 RSOP。
    - 信道模型：RSOP + 激光线宽 + 频偏 + ASE + IQ 失衡；**无大气湍流模型**。
    - 算法：4 个 FPT 功率谱平方合并 → FOE + CPE 解耦 → Jones 矩阵直接解算（无 CMA/MIMO 迭代）。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 级看不到实验硬件 + 子载波架构，全文补出 Keysight 8199A + 4 子载波频谱设计 + PSR=−15 dB。
- **下载建议**：已落盘，无需补。

### 篇 13：10.1109/jphot.2023.3265847（FSTS）⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1109_jphot.2023.3265847/content.md` + `papers/_read_notes/10.1109_jphot.2023.3265847.md` 笔记（CC-BY Open Access）。
- **dB 形态核验**：
  - 数字（vs 传统 TS baseline，@ FEC=3.8e-3，FSO 相位屏仿真）：
    - **单支路强湍 +1.03 dB（960 符号 4-QAM）/ +1.17 dB（320 符号 4-QAM）**。
    - **单支路强湍 +1.24 dB（960 符号 16-QAM）/ +3.11 dB（320 符号 16-QAM）**。
    - 单支路弱湍 +0.46/+0.73 dB（4/16-QAM 960 符号），+1.12/+2.23 dB（320 符号）。
    - **4 支路 MRC 强湍 +2.09 dB（4-QAM 320 符号）/ +3.41 dB（16-QAM 320 符号）**。
    - 4 支路 MRC 弱湍 +1.43/+2.54 dB（4/16-QAM）。
    - **复杂度降 25%（最优，一阶缓存）~ 75%（联合 FS+FOE，320 符号匹配传统 960）**。
    - **MSE 1e-7~1e-9 vs 传统 1e-6~1e-7（提升 ≥1 个数量级）**；MSE 阈值：16-QAM 6.25e-8（开始恶化）/ 2.25e-6（严重恶化），4-QAM 2.5e-7/6.25e-6。
    - FOE 范围：一阶 [−Rs/2, +Rs/2]，二阶缩 BL 倍。
  - 对照：vs 传统 TS-FOE [18] / 4th-FFT [11] / 4th-power/QPSK-partition [10][15] / Cheng 联合 FS+FOE [19]。
  - 条件：FSO，z=10 km 空间光，10 GBaud PM 4/16-QAM；**傅里叶相位屏湍流模型**（Schmidt [30]），外尺度→∞，内尺度→0，Cn²=1e-16 m⁻²/³（弱湍，平均耦合效率 67.3%）/ Cn²=1e-14（强湍，耦合效率仅 4.84%）；ECL 线宽 50 kHz（发射+每支路 LO 共享，LO 输出 15 dBm）；光电二极管响应度 0.8 A/W（含散粒噪声+热噪声）；接收望远镜口径 0.2 m；分集支路 1/2/4/6；FS 阈值 0.2 或 0.3；频偏随机 ∈(−1.1 GHz, 1.1 GHz)；每点 800~6400 次仿真平均。
  - 升级判定：**abstract 粗档 → 全文细档**——笔记已含 8+ 个精确 dB（强/弱湍 × 单支路/MRC × 4/16-QAM × 960/320 符号全矩阵）+ 复杂度百分比 + MSE 数量级 + 湍流建模深度（相位屏 + 耦合效率统计）。
- **复杂度细档核验**：
  - 档位：**纯仿真**（相位屏数值仿真，无硬件实现）。
  - 关键参数：见上方条件；MRC 分集最多 6 支路；FS+FOE 共享 FSTS（X/Y 极化交织共轭对称 TS，TX_1st/TY_1st 共轭，相邻块交错）；优化总长 320 符号（4-QAM: BN=16, BL=20；16-QAM: BN=8, BL=40）。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 级看不到分集矩阵和湍流强度，全文补出 6 支路 × 强弱湍全矩阵 + Cn² 标度 + 耦合效率统计。
- **下载建议**：已落盘，无需补。

### 篇 14：10.1364/oe.520452（PRBS+循环 QPSK Joint TS 升级）⭐ 全文核验

- **落盘状态**：✅ `papers/doi/10.1364_oe.520452/content.md` + `papers/_read_notes/10.1364_oe.520452.md` 笔记（Open Access）。
- **dB 形态核验**：
  - 数字（灵敏度 dBm，**注意单位是 dBm 不是 dB**，vs 传统 TS/FFT baseline，@ FEC=1.5e-3）：
    - **单支路强湍 QPSK +2.9 dBm / 16QAM +3.2 dBm**。
    - 单支路弱湍 QPSK +0.42 dBm（各算法接近）。
    - **4 支路 MRC 强湍 QPSK +1.78 dBm / 16QAM +2.46 dBm**。
    - 4 支路 MRC 弱湍 QPSK +0.61 dBm / 16QAM +1.56 dBm。
    - 4 支路 vs 单支路增益：弱湍 QPSK ~8.1 dBm / 16QAM ~9.5 dBm；强湍 QPSK ~19.45 dBm / 16QAM ~17.62 dBm（**分集在强湍增益巨大**）。
    - **MSE 1e-8~1e-9 vs 传统 1e-6~1e-7（提升 2 个数量级）**。
    - **比 Park 算法节省约 100 符号（≈39% 资源）**；优化总训练符号 N=480（<300 增益明显，>300 边际递减，480 为平衡点）；对比 [21] 用 1024 符号。
    - FOE 范围：一级 [−3Rs/8, +3Rs/8]（FFT 谱峰搜索），二级缩 TL 倍。
    - 复杂度：二级跨极化共轭乘 4N（远低于 [21] 二次 FFT）。
  - 对照：vs 传统 TS / 4th-FFT / [21] QPSK 谱偏移 / Park 加权 Park 帧同步。
  - 条件：FSO，z=20 km 空间光仿真 + 室内 B2B 弱湍实验（Cn²=6e-11，发射 13 dBm）；10 Gbaud PM-QAM；**多随机相位屏湍流模型**（外尺度→∞，内尺度→0，Cn²=1e-16 弱/Cn²=1e-14 强），耦合效率服从非中心卡方分布，相位噪声服从高斯；线宽 80 kHz；接收多望远镜分集（口径 0.2 m，间距 > 空间相干长度）；MRC 合并前加相位预校正；采样率=符号率 Rs；每点 800~3200 次仿真平均。
  - 升级判定：**abstract 粗档 → 全文细档**——笔记已含 8+ 个精确 dBm + 复杂度百分比 + MSE 数量级 + 资源节省百分比 + 室内实验湍流条件。
- **复杂度细档核验**：
  - 档位：**仿真 + 弱硬件**（相位屏数值仿真 + 室内 B2B 弱湍实验）。
  - 关键参数：
    - 链路：FSO，20 km 仿真 + 室内 B2B。
    - 实验硬件：室内 B2B 弱湍（Cn²=6e-11），发射 13 dBm（具体硬件型号笔记未载）。
    - 训练序列：PRBS 前缀（做 FS，差分共轭消线宽与调制相位）+ 循环 QPSK 后缀（做两段 FOE）混合 Joint TS；总长 480 符号（vs [21] 1024 符号）；二级 QPSK 块长 TL（4-QAM 下 TL>64~80 时二级精度才超一级）。
    - 算法：FS 差分共轭度量 M(d)=|C(d)|²/P(d)²；一级 FOE QPSK 段 FFT 找正半轴最大谱峰；二级 FOE 跨极化共轭乘 R1+R2，按 arg{Σ}/BL 得 Δf2。
  - 升级判定：**abstract 粗档 → 全文细档**——abstract 级看不到室内实验 + 训练序列结构，全文补出 PRBS+循环 QPSK 混合 TS + 室内 Cn²=6e-11 弱湍条件。
- **下载建议**：已落盘，无需补。

---

## 升级统计

- **已落盘**：**8/14**（L053 + sat.1553 + Paillier + 张思齐笔记 + LCOMM + jphot + oe + Matsuda 摘要算"部分落盘"）。
- **未落盘**：**6/14**（L004/L003/L008/L030/L009/L035——B1 Spalvieri 池 6 篇全未落盘，仅 L053 落盘）。
- **dB 升级到细档**：**7/14**（L053 + sat.1553 + Paillier + 张思齐笔记 + LCOMM + jphot + oe）。
- **dB 保持粗档**：**7/14**：
  - 未落盘 6 篇（L004/L003/L008/L030/L009/L035）。
  - Matsuda 摘要（0.6 dB 已有，但细节不可得）。
- **复杂度升级到细档**：**7/14**（同 dB 升级的 7 篇）。
- **复杂度部分升级（abstract 已能定档，细节待正文）**：**3/14**（L008 实测级 / L009 实测级 / L035 VLSI 档）。
- **复杂度保持粗档**：**4/14**：
  - L004/L003/L030（未落盘，abstract 未给算力）。
  - Matsuda（FPGA 型号/资源/湍流强度全不可得）。
- **保持粗档（未落盘或全文未提及）**：**7/14**（同 dB 保持粗档的 7 篇）。

---

## 自评

### 哪些篇核验最有价值（abstract 粗档 → 全文细档跨度大）

1. **sat.1553**（跨度最大）：abstract 几乎无 dB 数字（综述类），全文补出 **8+ 个精确 dB**（soft DQPSK 2.5 dB / hard DQPSK 0.75 dB / VV+diff 场景 4 ~1.5 dB / pilot 场景 4 比 VV+diff 好 1 dB / soft vs hard FEC 2 dB / linear interp 0.2-0.3 dB / two-stage DGD 1 dB / RSOP 0.03 rad 1 dB）+ B1/B2/B3 三切口的 dB 形态精确定性（B1 自适应 pilot rate 自承未量化 + "same pilot rate performs similarly" 负向信号；B2 fade 冻结无 dB；B3 open problem 无 dB）。**这是切法地图"dB 形态分布"统计的核心数据源**。
2. **L053 DLAE**（abstract 与正文 dB 数字方向一致但精度升级）：abstract 只说"over 2 dB"，全文精确到"DLAE 距 Genie gap 0.8 dB（256-QAM）/1.2 dB（1024/4096-QAM），PSAM gap > 3 dB"，可重算实际 PSAM-to-DLAE 差 ≈ 2~3 dB。复杂度补出 FLOPs 公式 + CNN 架构（filter (3,8), Nf=8, 3 hidden layers）+ 训练配置（Tensorflow+Sionna, 15000 iterations, Adam lr=1e-4）。**这是切法地图"DL 工具借用"子类的代表**。
3. **Paillier 2020 JLT**（abstract 看不到湍流建模深度）：abstract 只说"DPLL 设计"，全文补出 4 个 dB（湍流 2.3 dB BER penalty / 临界 SNR 5 dB 退化 / AO −4.5 dB flux / 残频无 penalty）+ **湍流建模深度全场最深**（Hufnagel-Valley + Zernike 91 + Bufton + 数值相位传播）。**这是 B2 baseline 分支 + D006 复核证据基础**。
4. **jphot FSTS**（abstract 看不到分集矩阵）：全文补出 6 支路 × 强弱湍 × 4/16-QAM × 960/320 符号全矩阵 dB（强湍 4 支路 MRC +2.09/+3.41 dB 是核心）+ Cn²=1e-16/1e-14 标度 + 强湍耦合效率仅 4.84%。**这是 B3 池"FS+FOE+分集合并"协同的代表**。
5. **LCOMM LPT**（abstract 看不到解耦机制）：全文补出 +0.9 dB Q-factor vs PTJ / RMSE 4.47° vs 17.99° / RSOP 100 Mrad/s / 40 km SSMF 实验 −0.7 dB ROP penalty + Keysight 8199A 硬件。**这是 B3 池"跨子模块解耦"独占角度的代表**。

### 哪些篇核验后仍信息不足（全文也没写 dB/复杂度）

1. **L004（信息率界）**：未落盘，但 B1 草稿判定"无 dB 仅结构性"基于 abstract 已正确——这类理论界论文全文大概率也无 SNR penalty dB（给的是 bits 收敛性），**核验价值低**。
2. **L009（PS 场景 CPR）**：未落盘，abstract 给"reducing/eliminating shaping gains"无单一 dB——这类论文 dB 形态偏结构性（shaping gain 损坏百分比），**全文大概率也无单一 SNR penalty dB**。
3. **Matsuda[79]**：付费墙穷尽降级失败，**摘要 0.6 dB + FPGA 实时 4 Gbps 已够定档**，FPGA 型号/资源/湍流强度细节不可得但**对切法地图判断非必需**。
4. **L008（overhead 优化）**：abstract 给的是 SE 9.3/8.3 bits/s/Hz + 吞吐量 11.9/10.6 Tb/s，**dB penalty 维度待正文**但 abstract 已能定档（实测 + superchannel 1000 km）。

### 关键发现（对切法地图定稿的输入）

1. **B1 Spalvieri 池 6/7 篇未落盘**——dB/复杂度细档依赖 abstract，建议主线汇总时**降权 dB 形态 + 复杂度维**（与 B1 草稿 §5 自评一致），重点保留"大点锚 + 切的角度 + 动机叙事"三维。
2. **L053 的"over 2 dB"是间接计算**——abstract 说"赢 PSAM over 2 dB"实际是 (PSAM gap > 3 dB) − (DLAE gap 0.8~1.2 dB)，**主线引用时应标"DLAE 距 Genie 0.8/1.2 dB，PSAM 距 Genie > 3 dB"**而非笼统"2 dB"，避免 FR-26 风险。
3. **sat.1553 的"pilot 场景 4 比 VV+diff 好 1 dB"是 B1 切入点最关键的 dB 锚**——但 B1 草稿已正确指出"这是 pilot vs VV 的差，不是自适应 N vs 固定 N 的增量"，**主线引用时必须保留这个条件性区分**。
4. **Paillier "湍流相位可忽略"是 D006 Kill 的独立佐证**——条件性极强（BPSK+10 GBaud+理想 timing+AGC 恒幅+AO 校正后活塞慢），主线引用时必须带条件，不能简化为"Paillier 证明分治够用"。
5. **jphot/oe 的 dB 是"灵敏度 dBm"不是"SNR penalty dB"**——单位差异，主线汇总时若做"赢 baseline 几 dB"横向对比需统一口径（dBm 灵敏度 vs dB SNR penalty 不可直接相加）。
6. **张思齐 dB/复杂度未对照原文核验**——B3 笔记数据虽标"论文原报未脑补"，但**原文不在 papers/ 下**，FR-26 警示：如主线要引用具体百分比（13.8%/47.6% 等）需补 CNKI 全文核验。
