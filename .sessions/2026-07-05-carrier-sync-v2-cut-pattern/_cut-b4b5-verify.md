# dB/复杂度核验：B4/B5 Paillier 池 12 篇

> 核验人：子 agent | 日期：2026-07-05 | 任务：abstract 级 → 全文级 dB/复杂度细档
> 来源：`_cut-b4b5-paillier-pool.md` §5 的 12 篇子集
> 纪律：FR-26 证据链（content.md 行号 / 笔记溯源）/ 只核验不重写笔记 / 不脑补 / 不判 Go/Kill

## 核验状态汇总

| # | ID/DOI | 落盘 | dB 形态升级 | 复杂度档升级 |
|---|---|---|---|---|
| 1 L005 | 10.1109/jlt.2023.3281082 | ✅ content.md(精读笔记 100 行) | 细档（+70~100 Gbps 吞吐 vs 固定 80 Gbaud） | 细档（半物理 600 Gbps PCS-64QAM，LO 频偏物理模拟 Doppler ±15 GHz） |
| 2 L008 (B4) | 10.1016/j.optcom.2023.129312 | ⚠ 部分（paywall 摘要+Intro，content.md 225 行 Intro 完整 / 实验节未获取） | 细档（Intro 自陈述全数；范围/资源/速度全；无外部 baseline dB） | 细档（Arria 10 FPGA 型号 + 12-bit 定点 + 9.1K+1.4K ALE + 10 Gbps PM-QPSK 实时） |
| 3 L027 (B5) | 10.1016/j.optcom.2024.130981 | ✅ content.md 252 行（用户 2026-07-04 手动下全文落盘） | 保持粗档（绝对指标维度，无 vs baseline dB） | 细档（Intel Arria 10 FPGA + 5 GSa/s 8bit ADC + 2.5-GBaud PM-QPSK 实时 B2B） |
| 4 L036 | 10.1109/ICSOS66026.2025.11443174 | ✅ content.md（精读笔记 84 行） | 细档（85 MHz/s Doppler + Bode 裕度/3dB 截止；无 BER-vs-SNR） | 细档（Z 域 MATLAB-Simulink behavioral，2 MBaud on 8 MHz carrier，无硬件） |
| 5 L001 | 10.1109/jlt.2022.3164736 (Guiomar 综述) | ❌ 未落盘（DOI 在 papers/doi/ 下不存在；index.json 无此标题） | 保持粗档 | 保持粗档 |
| 6 L010 | JSAC 2024（Zahr/Colavolpe IT） | ❌ 未落盘（无匹配 DOI/作者/标题） | 保持粗档 | 保持粗档 |
| 7 L013 | JLT 2025（Jin/Ding attention NN） | ❌ 未落盘 | 保持粗档 | 保持粗档 |
| 8 L024 | 10.1364/jocn.468220（Liu/Chen RL PAM4） | ✅ content.md 603 行（无单独笔记，本核验直接读 content.md） | 细档（SCD vs DD BER ↓ 1 量级 / GS-SCD vs SCD 再 ↓ 1 量级 / 弱到强湍流 GS 提升 2 量级） | 细档（仿真 20 Gbps PAM4 + IF 20 GHz + Gamma-Gamma/高斯近似湍流 + ROP 扫描 −32~−11 dBm + Cn² 10⁻¹⁷~10⁻¹³） |
| 9 L003 | 10.1038/s41598-026-40704-2 | ⚠ DOI 不匹配（此 DOI 实为 OAM 结构光论文，非 silicon photonic；真 SiPh 论文未落盘） | 保持粗档 | 保持粗档 |
| 10 L041 | LASE 2022（Foy μICR 空间鉴定） | ❌ 未落盘 | 保持粗档 | 保持粗档 |
| 11 L019 | Opt Eng 2022（Dandapathak OPLL chaos） | ❌ 未落盘 | 保持粗档 | 保持粗档 |
| 12 L039 | ICSOS 2023（Maho/Paillier feeder） | ❌ 未落盘 | 保持粗档 | 保持粗档 |

**汇总**：已落盘 **5/12**（L005/L008 部分/L027/L036/L024），未落盘 7/12（含 L003 DOI 不匹配）。
dB 升级到细档 **5/12**（L005/L008/L036/L024 + L027 范围维度细档但无 dB 增量）。
复杂度升级到细档 **5/12**（同上五篇）。
保持粗档 **7/12**（L001/L010/L013/L003/L041/L019/L039 + L027 dB 维度）。

---

## 逐篇核验

### 篇 1：L005 10.1109/jlt.2023.3281082（PCS+符号率 Doppler）

- **落盘状态**：✅ `papers/doi/10.1016_j.optcom.2023.129312/` 误记 — 实际 `papers/_read_notes/10.1109_JLT.2023.3281082.md`（精读笔记 100 行，源文件 `papers/blit-downloads/2026-06-26/10138358.md`）。content.md 全文 387 行。
- **dB 形态核验**：
  - 数字：**+70~100 Gbps 吞吐增量**（可靠性场景：±15 GHz 极端 Doppler 下 ABR 维持 ~600 Gbps vs 固定 80 Gbaud；最大化吞吐量场景：有效比特率提升 +70 Gbps；Fig.7c L213, Fig.10 L273）
  - 对照：vs **自实现固定 80 Gbaud 符号率 baseline**（同一 600 Gbps 链路 / 同硬件 / 同 DSP 管线 / 都用 PCS-64QAM；对比"符号率是否自适应"，非"用不用 PS"——baseline 对称性 PASS）
  - 条件：500 km LEO 7.8 km/s，20 min 内 Doppler 变 8 GHz（绝对 >4 GHz），Gamma-Gamma 湍流 σ_l²∈{0.03, 0.1, 0.3, 1}，N=10⁶ 衰减样本，η 70~99%
  - 升级判定：**abstract 粗档 → 全文细档**（数字明确 + baseline 对称 + 条件齐全）；但 **dB 维度错位**——这是吞吐 dB 等价（Gbps）非同步 BER/OSNR dB 增量
- **复杂度细档核验**：
  - 档位：**实验室硬件在环 + 半物理半数值**（Doppler 用 LO 频偏物理模拟 / 湍流用 Gamma-Gamma 数值衰减叠加到实测 SNR）
  - 关键参数：600 Gbps 净比特率，DP-64QAM 模板，RRC 0.2 滚降，20% FEC 开销；AWG Keysight M8194A 120 GSps ~45 GHz BW；DP-IQ 调制器 Fujitsu FTM7992HM 35 GHz；相干接收机 FIM24901 40 GHz；4×RTO Tektronix 200 GSps 70 GHz；nano-ITLA ~100 kHz；LO DFB ~100 kHz 调谐模拟 −15~+15 GHz；CMA 51 taps / LMS 51 taps；Rs 测试 65/70/75/80 Gbaud
  - 升级判定：**abstract 粗档 → 全文细档**（硬件型号 + 调制 + 符号率 + 湍流档齐全）

### 篇 2：L008 10.1016/j.optcom.2023.129312（B4 双反馈环本体）

- **落盘状态**：⚠ **paywall 部分获取**——`papers/doi/10.1016_j.optcom.2023.129312/content.md` 225 行（仅 Abstract/Intro 完整 + ScienceDirect 章节片段 + 引用列表；实验节/公式/图表细节不可见）。精读笔记 68 行（注明全文未获取）。
- **dB 形态核验**（Intro line 44 自陈述全数）：
  - 数字：归一化 MSE **2.0×10⁻⁶ → 5.1×10⁻⁷（残频 σ 3.5 → 1.75 MHz @ 2.5-GBaud）**，BER 3.8×10⁻³，线宽 20 kHz；动态跟踪 **285 GHz/s**（满足 LEO 40 MHz/s，余量 7000×）；最大跟踪范围 **±920 MHz @ 接收灵敏度代价 0.5 dB**；12-bit 定点 vs 浮点 **0 dB 灵敏度代价**
  - 对照：vs ① 前馈 FOE（范围限 1/8 baud；B4 反馈结构突破此限）；② MATLAB 浮点（12-bit 定点 0 dB 代价）；③ Paillier [5] JLT 2020 40 MHz/s LEO 上限作需求标定非性能对比。**无与具名外部算法（DPLL/pilot-aided）的 BER/OSNR dB 对比表**
  - 条件：PM-QPSK 10 Gbps 实时 FPGA，1550.32 nm，线宽 20 kHz；**无湍流建模**（Doppler 40 MHz/s 单点 + 激光频偏 + 激光稳频残频）；无过顶轨迹时变曲线、无多普勒率扫描
  - 升级判定：**abstract 粗档 → 全文（Intro）细档**——MSE 4× 改善 + ±920 MHz @ 0.5 dB + 285 GHz/s + 0 dB 定点代价全部从 Intro 坐实。**但"无外部 baseline dB 增量"的判定也从粗档确认到细档（硬伤）**
- **复杂度细档核验**：
  - 档位：**FPGA 实时硬件实现**（无湍流建模、无现场实测、实验室 B2B 性质）
  - 关键参数：**Intel Arria 10 FPGA**（型号 10ax066k3f40，Quartus Prime 18.1），**12-bit 定点**，逻辑资源两级反馈 FOE **9.1-K ALE + V–V 1.4-K ALE**（first-stage 7.9K ALMs / 14.9K reg / 0 mult；second-stage 1.2K ALMs / 3.2K reg / 0 mult）；PM-QPSK 10 Gbps（2.5 GBaud），TTX1995 激光，FTM7997 PM-IQ modulator
  - 升级判定：**abstract 粗档 → 全文（Intro+FPGA 资源表）细档**——FPGA 型号 / 定点位宽 / 资源 ALE / 调制齐全；但 PADE 鉴频曲线、环路滤波器系数、IIR/FIR 参数因实验节未获取不可见（标"全文未获取"）

### 篇 3：L027 10.1016/j.optcom.2024.130981（B5 短时谱 CFO 本体）

- **落盘状态**：✅ `papers/doi/10.1016_j.optcom.2024.130981/content.md` 252 行（用户 2026-07-04 手动下全文 2.9 MB PDF 后落盘；原 11 源穷尽失败归档）。`papers/_read_notes/10.1016_j.optcom.2024.130981.md` 25 行原"失败"笔记 + `_B5-short-time-spectrum-cfo-increment.md` 167 行（含全文核验追加段）。
- **dB 形态核验**（content.md 行 23/47/143/149/167 四处一致）：
  - 数字：**捕获范围 ±4.5 GHz**（覆盖 LEO Doppler 全量程，NEO 600 km 轨道）；粗补偿后残频标准差 **<140 MHz**（最大 250 MHz，含激光 250 MHz 抖动 + 算法误差）；精确补偿后残频 **<5 MHz**；精确补偿范围 ±312.5 MHz（=B/8=2.5 GBaud/8）；BER 1e-3 接收灵敏度 **−48 dBm**；接收功率测试区间 −51~−10 dBm；收敛 8 点 FFT 第 4 次迭代 / 16 点 FFT 第 3 次迭代收敛；3 s 周期循环
  - 对照：B5 自定位为 4 类 FOE 算法的第 4 类（谱分析），相对前三类（M-power / 训练序列 / 改进传统估计）的优势是"不依赖 MIMO 等 DSP + 低复杂度 + 无 pilot"——**定性对比，无 vs 某 baseline 给"改善 X dB"**
  - 条件：星地 LEO 下行（NEO 600 km，Doppler ±4.5 GHz @ 最大变化率 56 MHz/s），1550.32 nm 20 kHz 线宽；2.5-GBaud PM-QPSK；**B2B 实验无湍流信道**（全文无 turbulence/scintillation 建模，仅行 29 提"atmospheric turbulence... affect the optical signal"作背景动机）
  - 升级判定：**保持粗档（绝对指标维度）**——本体无"vs baseline 改善 X dB"对比，只给绝对残频/范围指标。但 **范围维度细档可坐实**（±4.5 GHz 覆盖 LEO Doppler 全量程是结构性优势，残频落精估范围 ±312.5 MHz 内保证后续 DSP 可接）。**D005"赢 baseline 几 dB"标尺下不够格**
- **复杂度细档核验**：
  - 档位：**实验室硬件 B2B 实时 demo**（无湍流信道仿真、非现场实测）
  - 关键参数：**Intel Arria 10 FPGA**（Tx 端生成 PM-QPSK + Rx 端 DSP 核 312.5 MHz 时钟驱动）；**5 GSa/s ADC 8-bit** 4 通道；1024 组 16 点 FFT 均值滤波（M=2N 滤波）；Tx 功率 −3 dBm；DSP 链 IQ imbalance / 实值 MIMO 4×4 均衡 3 taps / PADE 反馈精频偏 / V–V 反馈相位恢复；FTM7977 PM-IQ modulator，TTX1995 激光，ICR
  - 升级判定：**abstract 粗档 → 全文细档**——FPGA 型号 / ADC 采样率+位宽 / FFT 点数+组数 / 调制 + 波长 + 线宽齐全

### 篇 4：L036 10.1109/ICSOS66026.2025.11443174（ODPLL Z 域，Pech/Destic）

- **落盘状态**：✅ `papers/doi/10.1109_ICSOS66026.2025.11443174/content.md`；`papers/_read_notes/10.1109_ICSOS66026.2025.11443174.md` 精读笔记 84 行（含 Z 域 TF 推导全文）。
- **dB 形态核验**：
  - 数字：**85 MHz/s 最大 Doppler 率**（419 km LEO，最大相对速度 7.2 km/s，加速度 131 m/s²，Doppler 频移 ±4.6 GHz）下完成 QPSK 解调，XOR 误差信号 settling 后清零（Config A 即时 / Config B ~0.1 ms）；**量子极限 BER=10⁻⁹ 对应 18 photons/bit, SNR≥18 (12.6 dB)**；Config A（10 GBaud 等效, P_S=0.71 µW=−31.4 dBm）：时间常数 1.3 µs，**增益裕度 16.8 dB / 相位裕度 86.9° / 3 dB 截止 1.12 MHz / 延迟裕度 27 samples**；Config B（2 MBaud, P_S=0.14 nW=−68.4 dBm）：127 µs / 55 dB / 16.4° / 94 kHz / 53 samples；4 µs 内 PLL 本振锁定到主载波
  - 对照：vs ① CT/S 域等效线性 PLL 模型（[8] Panasiewicz 博士论文 / [11] Chen IEICE 2021 homodyne digital OPLL Z 域——方法前身，仅方法学对比无数值）；② 仿真内对比"无跟踪/理想跟踪/PLL 跟踪"三种解调输出。**无与外部发表方法的数值化 BER-vs-SNR 对比 / 无相位误差方差 / 无锁定时间统计表**
  - 条件：419 km LEO 下行，可见窗口 ~10 min；环路更新率 100 MHz（T=10 ns）；FPGA 频率假设 200 MHz 上限（α=4~5，取保守 α=5）；MAF L=8 taps；探测器响应度 R=0.04 A/W（FULFILL 实验台 Neophotonics）；**仿真波特率仅 2 MBaud on 8 MHz carrier**（受限于 Simulink 无法跑光频/10 GBaud）；**不建模湍流**（大气仅作幅度衰减/功率模块，用 1 kHz–1 MHz 正弦近似衰落）
  - 升级判定：**abstract 粗档 → 全文细档**——Bode 裕度 / 3 dB 截止 / 时间常数 / Doppler 率全坐实。但**无数值 BER-vs-SNR 曲线**（仅 XOR 误差清零视觉化），dB 形态偏稳定性裕度非通信 BER dB
- **复杂度细档核验**：
  - 档位：**纯仿真 behavioral model**（标未来 FPGA + photonic 集成，FPGA 硬件已到货但实测结果待出）
  - 关键参数：MATLAB-Simulink 实现；Z 变换离散相位域闭环 TF（HPD=K_D·z^−α / HLF=K1+K2/(1−z^−1) / HOVCO=K0·z^−β/(1−z^−1)，α=5+β=1 总延迟 60 ns）；VV 鉴相整体块化为单一线性比较器 TF（4 次方+atan2+MAF L=8 等价线性化）；继承 [8] Panasiewicz CT 模型 + [11] Chen Z 域方法
  - 升级判定：**abstract 粗档 → 全文细档**——建模工具 + 仿真波特率 + 接收功率两档 + FPGA 频率折线分析齐全。但**未达硬件实测档**（标"仿真档，FPGA 已到货待实测"）

### 篇 5：L001 10.1109/jlt.2022.3164736（Guiomar coherent FSO 综述+实验）

- **落盘状态**：❌ **未落盘**——`papers/doi/10.1109_jlt.2022.3164736` 目录不存在；index.json 中无此 DOI/标题；jlt.2022 系列仅有 `3167035`（Channel Estimation Errors + Pointing）/ `3192068`（空标题），均非 Guiomar 综述。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"48 小时 outdoor demo 800+ Gbps over ~42 m"
  - 对照：无 vs baseline dB 增量（综述+demo 性质）
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级 outdoor 现场实测（42 m 链路，48 小时）
  - 关键参数：未落盘无法细化
  - 升级判定：**保持粗档**
- **建议下载价值**：**中**——综述+demo 性质 dB 增量本就难出，但若需 Guiomar 团队的 outdoor 实测参数（链路长度/持续时间/湍流条件）作 baseline，建议补下。**注：DOI 待核**——pool 文档标 `10.1109/jlt.2022.3164736`，但同团队 Guiomar 综述标题"Coherent FSO Communications: Opportunities and Challenges"在 JLT 2022 卷的具体 DOI 需用户用 IEEE Xplore 重核（可能不是 3164736）。

### 篇 6：L010 JSAC 2024（Zahr/Colavolpe IT coherent vs IM/DD）

- **落盘状态**：❌ **未落盘**——JSAC 2024 系列仅 `3240710`/`3369665`/`3365899`/`3528815`（标题均非 Zahr/Colavolpe IT 比较）。pool 文档标"DOI 待查"。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"coherent vs IM/DD 的 SNR gain 量化 + shaping gain"，具体 dB abstract 未给
  - 对照：vs 内部对照（coherent vs IM/DD）
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级纯理论/仿真
  - 关键参数：未落盘
  - 升级判定：**保持粗档**
- **建议下载价值**：**高**——IT 视角 coherent vs IM/DD 是池中独占角度（pool 文档 §4），且 dB 增量形态最易量化（SNR gain）。建议用户补 DOI 后下。

### 篇 7：L013 JLT 2025（Jin/Ding attention NN 湍流感知）

- **落盘状态**：❌ **未落盘**——index.json 中"Attention"标题仅命中多波束 RF 卫星（OJCOMS）/Traffic Prediction（electronics），均非 FSO attention NN。pool 文档标"DOI 待查"。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"平均有效率提升 58.4% / 平均可靠性 gain 最高 34.2% / 最强 vs 最弱湍流慢衰落差 11 dB"
  - 对照：vs 内部对照（with vs without attention）
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级实验室 10 m FSO 链路 hardware demo（7 级湍流 time-varying）
  - 关键参数：未落盘
  - 升级判定：**保持粗档**
- **建议下载价值**：**高**——abstract 已带"11 dB 衰落差"具体数字，落盘后可坐实 + 拿 attention NN 准则。建议用户补 DOI 后下。

### 篇 8：L024 10.1364/jocn.468220（Liu/Chen RL 几何整形 PAM4）

- **落盘状态**：✅ `papers/doi/10.1364_jocn.468220/content.md` **603 行**（Vol.15 No.1 Jan 2023 JOCN，全文 OA）。无单独 _read_notes 笔记（本核验直接读 content.md）。
- **dB 形态核验**：
  - 数字（content.md L17 摘要 + L446/454/481/510 结果）：
    - **SCD vs DD @ ROP > −25 dBm / Cn²=10⁻¹⁵**：BER ↓ 约 **2 个数量级**（L446"about two orders of magnitude lower"）
    - **GS-SCD vs SCD**：BER 平均再 ↓ **1 个数量级**（L454"on average one order of magnitude lower"）
    - **几何整形 vs 不整形 @ 弱到强湍流**：BER 提升 **2 个数量级**（L17 摘要 + L454"up to one order of magnitude BER performance improvement over SCD"——注：摘要说 2 个量级，结果节单点说 1 个量级，**2 量级是"GS-SCD vs DD"组合**）
    - RL vs 启发式（ACO/PSO/GA）@ 50 实验：RL **~50% 实验 BER < 10⁻⁵**，最差 1.04×10⁻⁵；GA 仅 <25% 实验 BER < 10⁻⁵（L374）
    - 单点最优（无 RL 网格搜）：E2=0.1529, E3=0.3427 → **BER 9.5×10⁻⁶**（vs 等距 E2=0.22/E3=0.472 → BER 5.3×10⁻⁴，**约 1.7 个量级改善**）
    - 系统可满足 FEC 阈值的湍流上限：GS-SCD 推到 **Cn² ≤ 4×10⁻¹⁴ m⁻²/³**（无 GS 仅 SCD 推不到）
  - 对照：vs ① **传统 IM/DD（direct detection）**（L17/L446，BER 量级对比）；② **SCD without geometric shaping**（L454）；③ **传统启发式 ACO/PSO/GA**（L374）
  - 条件：20 Gbps PAM4，1550 nm 发射 / 1549.84 nm LO；IF 中心频 20 GHz + BPF 15 GHz BW；Gamma-Gamma 湍流 + 高斯近似；ROP 扫描 **−32~−11 dBm**（线性区）；Cn² 扫描 **10⁻¹⁷~10⁻¹³ m⁻²/³**（weak/medium/strong）；衰减 7.5 dB/km；接收灵敏度 −35 dBm；背景光 −130 dBm；MZM 插损 5 dB / 消光比 30 dB；统计 262,140 符号；RL 50 episode / 100 episode；step size 0.005/0.01/0.02
  - 升级判定：**abstract 粗档 → 全文细档**——BER 量级改善 vs DD/SCD/启发式三组对照全坐实，条件（ROP/Cn²/衰减/统计样本数）齐全。**BER 量级维度非 dB**（注：pool 文档 §5.8 标"BER 量级维度非 dB"——核验后确认）
- **复杂度细档核验**：
  - 档位：**纯仿真 + offline Tx/Rx 处理**（content.md L286 标"Tx offline / Rx offline"；无 FPGA 实时、无现场实测；MZM/BPD/SD/LPF 是仿真模块）
  - 关键参数：20 Gbps PAM4 + IF 20 GHz；Gamma-Gamma + 高斯近似湍流（公式 11，方差 σ²_f 随光强增大）；RL = model-based Q-learning（ε-greedy，Q-table 离散有限状态/动作，reward=|log10(BER)|）；状态=(E2,E3) 两 PAM4 内幅，动作=±单位步长；FEC 阈值作正常通信判据；几何整形仅在 ROP −28~−20 dBm + Cn² 1×10⁻¹⁵~4×10⁻¹⁴ 启用（避免不必要复杂度）
  - 升级判定：**abstract 粗档 → 全文细档**——RL 算法结构 + 启用区间 + 信道参数齐全。**未达硬件档**（仿真）

### 篇 9：L003 silicon photonic 自适应接收（Martinez/Cavicchioli/Melloni）

- **落盘状态**：⚠ **DOI 不匹配**——pool 文档标 `10.1038/s41598-026-40704-2`，但此 DOI 实际论文标题是 **"Robust high-capacity free-space optical communication using OAM-based structured light and intelligent adaptive signal processing"**（OAM 结构光 + DCNN+DNFIS+AO+PSO，**非 silicon photonic**）。真 silicon photonic 论文（Martinez/Cavicchioli/Zaneto/Melloni 米兰理工）**未落盘**，需用户核 DOI。
- **dB 形态核验**（基于误匹配 DOI 的 OAM 论文，**不适用于 SiPh 论文**）：
  - OAM 论文数字：DCNN BER 0.0032→0.0014（55%↓）；SNR 18.5→28.5 dB（10 dB↑）；瞄准 σ_p/ω_z=0.5 时无补偿 BER=0.095→混合补偿 0.018（81%↑）；WDM-MDM 功率超 baseline 10 dB
  - 对照：vs DFE [38] / 常规 MDM-FSO [44]
  - **此数字属 OAM 论文非 SiPh 论文——SiPh 论文 dB 待用户核 DOI 后下全文**
  - 升级判定：**保持粗档**（真 SiPh 论文未落盘）
- **复杂度细档核验**：
  - 真SiPh 论文：未落盘。abstract 级（pool 文档）"10 Gbit/s indoor FSO under turbulence stronger than outdoor"
  - 升级判定：**保持粗档**
- **建议下载价值**：**中**——silicon photonic MZI mesh 集成方案在池中独占（pool 文档 §4），但 dB 增量难出（集成化降功耗/成本是结构性优势非 dB）。**注：DOI 错配需用户先核验真 DOI**

### 篇 10：L041 LASE 2022（Foy μICR 空间鉴定）

- **落盘状态**：❌ **未落盘**——index.json 无"Foy/Minch/qualifying/integrated coherent receiver/space"匹配。pool 文档标"DOI 待查"。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"环境测试后 EO 性能无退化"（pass/fail 维度，非 dB gain）
  - 对照：无 dB
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级实验室环境测试（辐照 100 krad / 热循环 −40~70°C / 振动 28 GRMS / 冲击 1201g / 热真空）
  - 关键参数：未落盘
  - 升级判定：**保持粗档**
- **建议下载价值**：**低**——空间鉴定 pass/fail 维度本就无 dB 增量，pool 文档已给关键环境测试参数（辐照/热循环/振动/冲击全数值）。除非需 μICR 商用器件具体型号/SWAP，否则可保持粗档。

### 篇 11：L019 Opt Eng 2022（Dandapathak OPLL chaos）

- **落盘状态**：❌ **未落盘**——Opt Eng 系列仅 `10.1117_1.oe.63.1.018103`（标题未匹配 chaos/OPLL）。pool 文档标"DOI 待查"。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"stable synchronous zone estimated analytically + chaotic oscillation via period doubling"——**信息不足 abstract 无 dB**
  - 对照：无 dB
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级纯理论/数值仿真（无 hardware demo）
  - 关键参数：未落盘
  - 升级判定：**保持粗档**
- **建议下载价值**：**低**——OPLL 混沌动力学理论分析本就难出 dB 增量（pool 文档 §5.11 已判 abstract 无 dB），落盘后大概率仍是"稳定区/分岔图"非 BER dB。

### 篇 12：L039 ICSOS 2023（Maho/Paillier feeder link 实测）

- **落盘状态**：❌ **未落盘**——ICSOS 系列仅有 `8978983`（2019 Paillier 自引会议版）/ `11443146`/`11443150`/`11443166`/`11443174`/`11443202`（2025），无 2023 Maho/VERTIGO。pool 文档标"DOI 待查"。
- **dB 形态核验**：
  - 数字：abstract 级（pool 文档）"25 Gbps DPSK 达 state-of-the-art sensitivity + BER 曲线 + detection sensitivity + power penalty"，具体 dB abstract 未全给
  - 对照：vs 传统 baseline
  - 升级判定：**保持粗档**（未落盘）
- **复杂度细档核验**：
  - 档位：abstract 级实验室 + outdoor trial（Jungfraujoch-Zimmerwald 瑞士野外链路）
  - 关键参数：未落盘
  - 升级判定：**保持粗档**
- **建议下载价值**：**高**——feeder link outdoor 实测 + Paillier 自引延伸是池中独占（pool 文档 §4），且 abstract 已带"state-of-the-art sensitivity"+ 具体链路（Jungfraujoch-Zimmerwald）。**注：DOI 待查，可能是 SPIE/ICSOS 2023 会议论文**

---

## 升级统计

- **已落盘**：**5/12**（L005 笔记+全文 / L008 部分 Intro / L027 全文 / L036 全文 / L024 全文）
- **dB 升级到细档**：**5/12**（L005 吞吐 dB 等价 / L008 内部 MSE+范围 dB / L036 Bode 裕度 dB / L024 BER 量级改善 / L027 范围维度细档但无 dB 增量——严格说 4/12 升级 + 1/12 范围维度）
- **复杂度升级到细档**：**5/12**（L005 半物理 600 Gbps / L008 Arria 10 FPGA 实时 / L027 Arria 10 FPGA B2B 实时 / L036 MATLAB-Simulink 仿真 / L024 仿真 + offline）
- **保持粗档（未落盘或全文未提及）**：**7/12**（L001/L010/L013/L003-L003SiPh/L041/L019/L039）+ L027 dB 维度（绝对指标无 baseline dB）
- **DOI 不匹配**：**1/12**（L003 `s41598-026-40704-2` 实为 OAM 论文非 SiPh 论文）

---

## 自评

### 哪些篇核验最有价值（abstract 粗档 → 全文细档跨度大）

1. **L024（RL PAM4）**：abstract 粗档只说"BER 提升 1-2 量级"，全文核验后坐实三组对照（vs DD 2 量级 / vs SCD 1 量级 / RL vs 启发式 50% vs 25%）+ 完整启用区间（ROP −28~−20 dBm + Cn² 1×10⁻¹⁵~4×10⁻¹⁴）+ 单点最优数值（9.5×10⁻⁶ vs 5.3×10⁻⁴）。**跨度最大**——abstract 给的是模糊量级，全文给的是可复现条件+三对照矩阵。
2. **L027（B5 短时谱）**：原 pool 文档基于穷尽 11 源失败标"待全文核验"，用户 2026-07-04 手动下全文后坐实——**确认无 dB 增量**（绝对指标维度）+ 范围 ±4.5 GHz 覆盖 LEO Doppler 全量程结构性优势 + FPGA 型号/ADC 采样率/FFT 点数齐全。**跨度从"信息不足"到"明确三维判定"**。
3. **L008（B4 双反馈环）**：paywall 仅 Intro，但 Intro line 44 自陈述把所有关键数（MSE 4× / ±920 MHz @ 0.5 dB / 285 GHz/s / 0 dB 定点 / 9.1K+1.4K ALE）一次给全。**跨度从"abstract 无 dB"到"Intro 已坐实全数"**——paywall 但 Intro 信息密度足够支撑细档。
4. **L036（ODPLL Z 域）**：abstract 只说"successful QPSK demodulation under strong Doppler + realistic received power"无 dB，全文核验后坐实 Bode 裕度（16.8 dB/55 dB 增益裕度）+ 3 dB 截止（1.12 MHz/94 kHz）+ 时间常数（1.3 µs/127 µs）+ Doppler 率 85 MHz/s。**但 dB 形态偏稳定性裕度非通信 BER**——细档但仍非"赢 baseline 几 dB"标尺。

### 哪些篇核验后仍信息不足（全文也没写 dB/复杂度）

- **L027（B5）**：全文确认无 vs baseline dB 增量（绝对指标维度硬伤，同门学位论文需 dB 增量对比）
- **L036（ODPLL Z 域）**：全文无数值 BER-vs-SNR 曲线（仅 XOR 误差清零视觉化）
- **L008（B4）**：paywall 实验节未获取，PADE 鉴频曲线/环路滤波器系数/IIR-FIR 参数不可见
- **L024（RL PAM4）**：纯仿真无 hardware demo（虽 dB 细档全但档位偏低）
- **7 篇未落盘**（L001/L010/L013/L003SiPh/L041/L019/L039）：全文未读，dB/复杂度仍 abstract 粗档

### Paillier 池"安全区恰恰是 dB 最难出区"在核验后是否仍成立

**仍成立，且核验后证据更强**：

- **安全区（场景迁移 11 + 硬件实现 10）= dB 难出区**：本批 5 篇落盘中，**L027（B5 场景迁移独占）+ L024（工具借用独占）** 都在或邻近安全区。L027 核验后**确认无 dB 增量**（绝对指标维度硬伤）；L024 虽有 BER 量级改善但**纯仿真非硬件实测**，dB 形态是"BER 量级"非"OSNR dB"。**L008（B4 架构替换）+ L036（ODPLL Z 域架构替换）** 在中等密度区（非安全区），但仍都**无外部 baseline dB 增量**——L008 仅内部 MSE 4× 改善 + ±920 MHz @ 0.5 dB 自报绝对值；L036 仅稳定性裕度非通信 BER dB。
- **唯一例外是 L005（参数调度）**：在中等密度区（参数调度 4 篇之一），有 +70~100 Gbps 吞吐增量——但**维度错位**（吞吐 vs 同步 dB），非同步 BER/OSNR dB 增量。
- **结论**：核验后 5 篇落盘中 **0 篇给出"vs 外部具名 baseline 改善 X dB BER/OSNR"** ——L005 维度错位 / L008 自报绝对值 / L027 绝对指标无 baseline / L036 稳定性裕度非 BER / L024 BER 量级非 dB + 纯仿真。**Paillier 池"安全区恰恰是 dB 最难出区"判定核验后仍坚挺**——这与 B4/B5 本体自身都无外部 baseline dB 增量（pool 文档 §3 已判）一致，**整个 12 篇子集的 dB 形态分布偏散且偏"绝对指标/内部对照/量级改善"**，无一篇落"赢传统 baseline 几 dB"区。
- **独占区被切得少 ≠ dB 易出**：L010（IT coherent vs IM/DD）/L013（attention NN）虽然 abstract 已带 dB 数字（11 dB 衰落差 / SNR gain），但**两篇都未落盘**，无法验证；**理论分析类（L019 OPLL chaos）+ 空间鉴定类（L041）本就难出 dB**（pool 文档已判 abstract 无 dB）。**独占区的 dB 易出性目前仅停留在 abstract 级，未落盘验证**。
