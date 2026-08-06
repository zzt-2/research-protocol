# Step 3 Q1 直接竞品 CORE 精读 A

> 任务：T001 Q1 直接竞品 CORE 全文精读
> 日期：2026-08-06
> 边界：仅做 GW Step 3 事实提取；不作 Go/Kill、METHOD_SIGNAL、新颖性闭合或 Step 4a 裁决；未联网。

## 0. 身份门与证据范围

| 论文 | 派遣标题 vs. 正文标题 | 结果 | 定位证据 |
|---|---|---|---|
| Tang et al. 2022 | 完全一致：*Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication* | **TITLE PASS**（人工逐词核验；正文题名完全一致） | `papers/doi/10.1109_jphot.2022.3161795/content.md:1-7` |
| Sun et al. 2025 | 单复数/大小写差异，不改变论文身份：正文为 *...Coherent PONs* | **TITLE PASS**（本地 `metadata.json`：`title_check=match`, `title_overlap=0.875`） | `papers/arxiv/2409.14400/content.md:1-9`；`papers/arxiv/2409.14400/metadata.json` |

证据限制：两篇均完整读取 `content.md`。转换文本中的若干公式/图被标成 omitted；本文对其只引用论文给出的公式号、章节和相邻文字，不臆造缺失的公式像素内容。Sun 的正式发表身份采用本地 metadata 中已经核验的 DOI/venue 信息，不作新的联网验证。

---

## 1. Tang et al. 2022：STSB CFSO frame localization → FOE

### 1.1 标准事实条目

- **题名**：*Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication*（`content.md:5-9`）。
- **DOI/来源**：`10.1109/JPHOT.2022.3161795`（`content.md:17-21`）。
- **源文件路径**：`papers/doi/10.1109_jphot.2022.3161795/content.md`。
- **发表状态/渠道**：正式发表，*IEEE Photonics Journal*, vol. 14, no. 3, June 2022；正文给出 2022-03-23 publication date（`content.md:1-5,17-21`）。
- **核心贡献（事实）**：论文把一个训练周期设计成共轭对称的 `[A, B, A*, B*]` 结构，第一阶段通过对称块相关峰定位训练周期/数据帧起点，第二阶段用已定位训练序列与其原始对称序列作单次乘法去除调制相位并估计 CFO（`content.md:41-47,55-83`）。该设计的论证目标是避免 S&C 型 TSB 在差信道下出现 timing-metric plateau，也避免 QPSK 4th-power FOE 的四次幂运算，从而改善低功率下的帧定位、FOE 误差、估计范围和复杂度（`content.md:27-41,81-105`）。
- **方法概述**：阶段 1 在接收序列上滑动计算 Park 型 timing metric，最大值位置 `d` 即训练序列/帧起点；阶段 2 对定位后的 `R(k)` 执行对称配对，得到 CFO 相位增量，再用估计量校正同一训练周期的数据符号（`content.md:43-57,73-83`）。
- **实验设置**：MATLAB 构建 10-Gbit/s QPSK CFSO 仿真，Tx/LO 激光线宽均 50 kHz、载波频偏 300 MHz；Rx 流程依次含 I/Q balance、timing recovery、polarization demultiplexing、STSB FOE、CPR、判决和 BER（`content.md:107-113`）。另建 10-Gbit/s 单偏振室内 CFSO 实验，SLM 加载两种湍流相位屏、约 55 个随机 phase mask，链路 900 mm 并按 Fresnel scaling 解释为长距离等效；AWG 与示波器共用同步时钟（`content.md:163-183`）。
- **receiver-visible information**：接收端可见的是经过前级 clock synchronization 和 equalization 后的 `r_k`，论文明确标注为 **one sample per symbol**；接收端另已知训练符号 `A/B` 及其共轭对称关系，不需要 payload truth（`content.md:43-57`）。信号仍含 Tx/LO 频差、LO linewidth、湍流相位扰动和 ASE noise（`content.md:45-47,57-83`）。
- **action**：离散滑窗搜索训练周期的起始索引 `d`；随后在已选中的训练块上计算单个 CFO 估计并对该训练周期的数据作频偏校正（`content.md:47-57,73-83`）。论文没有联合优化 fractional-delay 参数。
- **output**：帧/训练序列起始位置 `d`、标量 CFO 估计 `Δf_est`，以及 CFO-corrected data symbols（`content.md:55-83`）。
- **时序/处理顺序**：`clock synchronization + equalization（前级） → STSB frame/training localization → STSB CFO estimation/correction → CPR`；固定训练周期下，首周期定位后，后续周期可跳过 Park 定位计算（`content.md:45-47,81-85,109-111`）。
- **使用的 baseline**：
  - **S&C-based TSB timing/FOE**：引用 [25]/[26]；正文在 55 个 phase mask、-22 dBm 下比较 STSB 与 TSB 的 timing error probability，属于论文内实现的 timing comparator（`content.md:27-39,127-129,251-255`）。
  - **4th-power FOE**：引用 [24]，论文内仿真和实验复现，比较 normalized MSE、估计范围、BER/receiver sensitivity 与复杂度（`content.md:85-105,131-161,185-195,249-251`）。
  - **FFT FOE**：引用 [22]/[23]，仅进入复杂度论述/Table I；正文没有给出与 STSB 的同图性能曲线（`content.md:25,85-105,245-249`）。
- **failure condition / 适用边界**：方法假定 sampling-clock offset 已由前级 clock synchronization 消除，且输入已降至 1 sample/symbol；它的“timing”是训练序列/帧起点定位，不是 fractional timing recovery（`content.md:43-47,85`）。它还依赖固定训练周期及相邻符号上的 LO/turbulence phase 近似相同；论文以湍流 20 Hz–1 kHz、通信速率 GHz 为该近似的依据（`content.md:81-85`）。实验采用 QPSK、同步 AWG/oscilloscope、单偏振和 SLM 等效链路，因此不能直接外推到异步 ≥2-sps、SCO/drift 或 DP-16QAM 联合 acquisition（`content.md:179-191`）。
- **关键结论**：仿真中，FEC threshold `3.8×10^-3` 处，相对 4th-power FOE 的 sensitivity gain 为 strong/weak turbulence 下约 1.92/1.2 dB；实验对应约 1.9/1.0 dB（`content.md:157-161,185-195`）。FOE 理论范围给为 `± symbol rate/2`，归因于不用 4th-power 去调制（`content.md:73-83,193-195`）。
- **与 Q1/Q2 的关系**：对 **Q1** 直接相关，因为它在 CFSO 中把帧定位与 CFO 估计串在同一对称训练结构上；但其输入已完成 clock sync 且为 1 sps，故不覆盖 Q1 的 sample-level fractional timing/frame/CFO 联合动作。对 **Q2** 仅是 acquisition 侧参考；固定训练周期可重复 FOE，但论文不研究 SCO/drift、双环维护、fade-triggered reacquisition 或恢复时间（`content.md:45-47,81-85`）。
- **实现关键数值**：timing 例中训练块从第 31 个 symbol 开始、`N=256`；FOE/BER 主实验取 `N=1024`；CFO=300 MHz；strong/weak turbulence 的 `C_n^2=6.5×10^-14 / 6×10^-16 m^-2/3`；FEC threshold `3.8×10^-3`（`content.md:109-113,127-129,155-161`）。
- **开源代码**：全文未报告代码仓库或下载链接。
- **验证状态**：title/DOI/venue 与全文自洽；method、simulation、experiment、result、conclusion 已逐段核验。未作联网发表状态复核。

### 1.2 七个结构化子表

#### A. 状态/输入空间

| 维度 | 范围/取值 | 归一化/处理 | 证据 |
|---|---|---|---|
| 接收复样本 `r_k` | 1 sample/symbol；QPSK | 前级已做 clock sync/equalization | `content.md:43-47` |
| 滑窗时间索引 `d` | 覆盖接收序列中的候选帧起点 | timing metric `M(d)`；取最大值 | `content.md:47-55`（Eq. 1–3） |
| 训练块 | `[A_{N/4},B_{N/4},A*_{N/4},B*_{N/4}]` | 共轭对称相关；`N=256/1024` 依实验而变 | `content.md:47-57,127-129,155-157` |
| 残余 impairment | 300 MHz CFO；50 kHz Tx/LO linewidth；turbulence phase；ASE | FOE 前不消除这些相位项 | `content.md:57-83,109-113` |

#### B. 动作空间

| 类型 | 维度 | 合法动作约束 | 证据 |
|---|---:|---|---|
| 离散 frame-start 选择 | 1 | `d*=argmax_d M(d)`；只选一个训练周期起点 | `content.md:47-55` |
| 连续 CFO 估计/校正 | 1 | 理论估计范围 `[-1/(2T),+1/(2T)]`；对同周期数据校正 | `content.md:73-83` |
| fractional-delay / SCO action | 0 | **不存在**；由前级 clock synchronization 负责 | `content.md:45-47,85` |

#### C. 目标/奖励

| 项目 | 定义 | 归一化/权重 | 证据 |
|---|---|---|---|
| 学习奖励 | **N/A**：确定性信号处理法，无策略学习/训练目标 | N/A | Section II 全部为解析 metric/estimator（`content.md:43-105`） |
| frame 目标 | 最大化 timing metric peak、降低 timing error probability | Eq. 1–3 的具体像素公式未被 markdown 保留 | `content.md:47-55,127-129` |
| FOE/链路指标 | normalized MSE、BER、达到 FEC threshold 所需 power、硬件复杂度 | 无加权总目标 | `content.md:131-161,185-195` |

#### D. 建模假设

| 假设 | 位置 | 对后续仿真器/比较的影响 |
|---|---|---|
| clock sync 与 equalization 已补偿其他损伤 | Section II | Q1 若含 fractional timing/SCO，不能沿用该输入条件作为公平联合 baseline | `content.md:43-47,85` |
| FOE 输入为 1 sps | Section II | 不呈现 RRC 过采样下 sample-phase 信息 | `content.md:45` |
| 相邻符号的 LO/turbulence phase 近似相同 | Section II | 训练配对跨距与更快 phase dynamics 必须另审 | `content.md:81-83` |
| 固定训练周期；首周期定位后可复用位置 | Section II | burst-to-burst 不规则 frame offset 或 drift 不在论证范围 | `content.md:85` |
| 实验 clock 共源同步 | Section IV | 实验不能验证独立采样钟偏差/漂移 | `content.md:183` |

#### E. 网络架构

| 层类型 | 维度 | 激活/归一化 | 优化器 | 说明 |
|---|---|---|---|---|
| N/A | N/A | N/A | N/A | 非学习法；由相关、乘法、相位差和平均构成，未使用神经网络（`content.md:43-105`） |

#### F. 适配性

| 适配点 | 不适配点 | 可供后续方法设计核查的方向（不是建议/裁决） |
|---|---|---|
| CFSO + turbulence 直接实证；receiver-known preamble 同时服务帧定位和 FOE | 1 sps；先验完成 clock sync；无 fractional delay/SCO；QPSK；动作是顺序两阶段 | 后续若声称“联合”，必须把 fractional delay 作为显式 action，并与“独立 clock recovery + STSB”同开销比较；仅共享序列不等于联合动作 |
| 给出 4th-power/TSB 的低复杂度直接比较及 sensitivity 数字 | 实验共源时钟、单偏振、短室内 scaled link | 可把 `clock recovery → STSB frame → STSB FOE` 保留为廉价 CFSO comparator |

#### G. 问题提取（论文自身问题，不是 Q1 终态裁决）

| 字段 | 提取结果 | 证据 |
|---|---|---|
| M | 传统 S&C-based TSB frame localization + 4th-power FOE | `content.md:27-41` |
| C | 低接收功率、weak/strong turbulence 的 QPSK CFSO | `content.md:109-161` |
| A | S&C 重复块 metric 在差信道下仍有单一尖峰；4th-power 去调制的精度、范围和复杂度仍可接受 | `content.md:27-41` |
| M-C-A | 传统 TSB/4th-power 链在低功率湍流 CFSO 下，因 timing plateau 与四次幂相位去除假设而产生定位/FOE 精度和复杂度不足 | `content.md:27-41` |
| 失效假设定位 | Introduction 对 S&C plateau、4th-power 范围/精度/复杂度的陈述 | `content.md:25-41` |
| 方法产出形态 | 可复用的对称训练序列结构 + 两阶段帧定位/FOE 算法 | `content.md:43-105` |
| 判据 1 | ✅ M/C/A 均为具体 DSP 矛盾 | 同上 |
| 判据 2 | ✅ 产出是可复用序列/估计算法，不是一次性曲线 | `content.md:43-105` |
| 判据 3 | ❌ **按本项目 2019+ task-matched 硬口径**：实际结果 comparator 的核心来源是 2006 4th-power、2011 TSB 与 1997/2003 timing；虽引用 2019 sparse-FFT timing/frequency paper，但未作结果 comparator。Tang 2022 本身可作为后续 Q1 的近期 baseline，不反向改变其论文自身 M 的年份 | `content.md:245-255,267-275` |
| 判据 4 | ✅ timing error、FOE MSE/range、BER/sensitivity、复杂度均可量化 | `content.md:127-161,185-195` |
| 四判据 | **未全过（3 FAIL）**；仅记录论文自身问题，不据此裁决 Q1 | — |

### 1.3 通信信道模型参数表

| 链路/层 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| CFSO atmosphere（simulation） | McGlamery active-power-spectrum phase-screen | `z=10 km`；`λ=1550 nm`；inner scale neglected；outer scale infinite；`C_n^2=6×10^-16`（weak）、`6.5×10^-14 m^-2/3`（strong） | `content.md:109-113` |
| Laser/receiver phase | Tx ECL + LO phase noise and CFO | Tx/LO linewidth 50 kHz；CFO 300 MHz；turbulence temporal variation约 20 Hz–1 kHz | `content.md:73-83,109-113` |
| CFSO atmosphere（experiment） | SLM phase-mask turbulence emulator | 1920×1080 SLM；每种状态约 55 random masks；同两组 `C_n^2` | `content.md:163-183` |
| Indoor optical path | Fresnel-scaled free-space link | 900 mm；beam diameter 2.1 mm；focal length 11.29 mm；λ=1550 nm；单偏振 | `content.md:179-183` |

### 1.4 实验完备性（≤20 行）

- **C1/scope**：在 QPSK CFSO、两种 `C_n^2` 和本文功率范围内，STSB 改善 timing/FOE/sensitivity；属于 bounded claim（`content.md:109-195`）。
- **C2/scope**：FOE range `±symbol-rate/2` 且复杂度低于 4th-power/FFT；范围声称受本文 estimator 结构支持，但复杂度表未在 markdown 保留数值（`content.md:81-105,193-195`）。
- **统计规范性**：实验 phase masks≈55；正文没有 seed 声明、error bar、置信区间或显著性检验（`content.md:127-129,179`）。
- **Baseline 矩阵**：结果 comparator 主要为 TSB timing 与 4th-power FOE；FFT 仅复杂度对照；来源均声明，但未报告统一调参预算（`content.md:85-105,127-161`）。
- **消融设计**：扫描 `N`、power、CFO、turbulence strength；不是逐模块删除式消融（`content.md:127-161,185-191`）。
- **信道真实性**：有引用的 phase-screen 模型与 SLM 实验，强/弱 turbulence 均覆盖；但实验单偏振、clock-synchronized、scaled indoor link（`content.md:109-113,163-191`）。
- **配置多样性**：2 个 turbulence strength；simulation + experiment；无多距离、异步时钟、调制阶数或 sampling-rate 多样性。
- **复杂度**：Table I 提供硬件 operation comparison；没有实测 latency/FLOPs（`content.md:85-105`）。
- **VVUQ**：Verification=3/3（仿真与实验趋势互证，且报告约 3 dB 差异）；Validation=2/3（真实硬件但 scaled、单偏振、同步 clock）；Uncertainty=1/3（55 masks 但无误差条/CI/统计检验）（`content.md:179-195`）。

---

## 2. Sun et al. 2025：CAZAC shared-unit FS → FOE → CE

### 2.1 标准事实条目

- **题名**：*Preamble Design for Joint Frame Synchronization, Frequency Offset Estimation, and Channel Estimation in Upstream Burst-mode Detection of Coherent PONs*（`content.md:5-9`）。
- **DOI/来源**：arXiv `2409.14400`；正式 DOI `10.1109/JLT.2025.3533197`（本地 `metadata.json`）。
- **源文件路径**：`papers/arxiv/2409.14400/content.md`。
- **发表状态/渠道**：本地 identity metadata 已核验为正式发表，*Journal of Lightwave Technology* (2025)；当前 `content.md` 是保留 manuscript placeholder 的 arXiv PDF 转换稿（`content.md:1-5,23-27`；`metadata.json`）。
- **核心贡献（事实）**：论文设计 CAZAC-based TS-B，每个训练单元含 X/Y 两偏振上的四个变换 CAZAC block 与 guard interval；同一个训练单元可独立支持 frame synchronization、FOE 和 frequency-domain channel estimation，重复 `L` 个单元通过平均/metric multiplication 抗噪（`content.md:119-155,157-251`）。FD-CE 同时估计 RSOP、bandwidth limitation、CD、PMD/DGD、PDL 的总体 transfer matrix，再用 ZF 初始化 FD equalizer，显著压缩 LMS convergence 所需训练长度（`content.md:203-257`）。
- **方法概述**：TS-A 先做粗 frame detection 和 Godard clock recovery；随后 TS-B 先做 FS（四个 polarization-combination metrics 中选最强 peak），再 FOE（已知 CAZAC 去数据、相关相位增量、X/Y 平均），再 matched filter 与 FD-CE/ZF equalizer initialization（`content.md:43-57,135-251`）。payload 用 1/31 pilot 做 coarse phase，残余 phase 由 ML CPR；equalizer 从 training-aided 模式切到 decision-directed LMS（`content.md:253-257`）。
- **实验设置**：仿真是 15-Gbaud DP-16QAM、RRC roll-off 0.1、2-sps CE 输入；选择实验最终配置 `N=64`, `N_GI=2`, `L=2`, 总 preamble 272 symbols（`content.md:231-243,259-293`）。实验用 120 GSa/s AWG、11 km SSMF、100 GSa/s DSO、ECL linewidth <100 kHz、1550 nm；payload `2^15` symbols（`content.md:345-367`）。
- **receiver-visible information**：TS-A/TS-B 均为 receiver-known preamble。FS 观察 `r'_X, r'_Y, r'_X+r'_Y, r'_X-r'_Y` 四路的对称块 timing metric；FOE 观察去掉已知 CAZAC 后的相位相关；CE 观察两偏振、twofold-upsampled known CAZAC 与对应 received sample spectra（`content.md:135-201,227-251`）。
- **action**：先由独立 Godard clock recovery 消除 sampling phase offset；TS-B 再离散选 frame peak、连续估 CFO、估 `2×2` channel transfer matrix并生成 ZF equalizer coefficients（`content.md:43-57,135-251`）。
- **output**：粗 frame position、clock-corrected samples、TS-B frame index、标量 CFO、频域 `2×2 H(ω)` 与初始化 equalizer `W(ω)`，随后输出经 LMS/CPR 恢复的 payload（`content.md:43-57,193-257`）。
- **时序/处理顺序**：`TS-A frame detection → Godard clock recovery → TS-B FS → TS-B FOE → matched filter → TS-B FD-CE/ZF initialization → FD equalizer + pilot CPR/LMS`。论文的“joint”明确指 **shared same training unit**，而接收机动作仍是 sequential modules（`content.md:35-57,133-137,157-205`）。
- **使用的 baseline**：
  - **prior coherent-PON preambles**：2021 JOCN 1792-symbol、2023 JLT 416-symbol、2024 JLT 496-symbol，仅在 related/background 用 reported length 对照，没有统一实验复现（`content.md:31-39,447-457`）。
  - **ordinary 16QAM training blocks for CE**：论文内自实现仿真 comparator，CAZAC CE 明显更优（`content.md:281-291`）。
  - **standard equalizer without CE**：论文内自实现，先用 100 known training blocks 收敛再切 decision-directed；与 CE-initialized equalizer 比较 convergence block count/RMSE（`content.md:317-331,389-393`）。
  - **blind 4th-power FOE**：实验中用作实际 FO 的 reference；不是完整 pipeline baseline（`content.md:369-375`）。
- **failure condition / 适用边界**：TS-B FS/FOE 建立在前级 clock recovery 已消除 sampling phase offset 的条件上；论文没有把 fractional timing 作为与 frame index/CFO 同时估计的变量（`content.md:43-57`）。FS 为避免特定 RSOP 下单路被抵消，必须在四路 metric 中择优；FOE 为避免 odd-`m` 的额外 `π` 相位，只用 two-symbol phase increment，检测范围设为 `(-1/4,+1/4) symbol rate`（`content.md:145-201`）。短 FOE 序列内 phase noise 被近似常量（`content.md:157-179`）。
- **关键结论**：选定 272-symbol preamble 是 `N=64, N_GI=2, L=2` 的开销/CE 精度折中；两单元相对一单元有 1.5 dB SNR gain，而从 2 增至 4 单元额外仅 0.7 dB；在两单元下 `N=32→64` 增益 3.6 dB，而 `64→512` 仅 0.4 dB（`content.md:283-291`）。仿真中 FS 在 CFO -3–3 GHz 保持 PMNR>10 dB，FOE 在 -3.5–3.5 GHz 平均误差 <3 MHz；实验相对 4th-power reference 在 -1.5–1.5 GHz 的平均误差 within 0.4 MHz（`content.md:293-315,369-375`）。CE-initialized equalizer 从首块已收敛，normal equalizer 仿真约需 100 blocks、实验约需 50 blocks（`content.md:317-331,389-393`）。
- **与 Q1/Q2 的关系**：对 **Q1** 是当前两篇中最强近期 task-matched comparator，因为同一 272-symbol receiver-known preamble 支持 frame+CFO 且系统为 RRC、DP-16QAM、CE 使用 2-sps samples；但 fractional timing 已由 TS-A/Godard 模块先消除，故没有覆盖 sample-level timing/frame/CFO 联合 action。对 **Q2** 仅提供 burst acquisition 与后续 LMS/pilot-CPR tracking；没有 SCO/drift、fade-triggered loss/reacquisition 或双环恢复时间模型（`content.md:43-57,253-257`）。
- **实现关键数值**：15 Gbaud DP-16QAM；272-symbol/18.13 ns preamble；`N=64`, `N_GI=2`, `L=2`；payload `2^15`; RRC 0.1；payload pilot overhead 3.125%（每 31 payload symbols 插 1 pilot）；equalizer block 64/taps 128/50% overlap（`content.md:39-43,253-257,317-317,345-349,393`）。
- **开源代码**：全文未报告代码仓库或下载链接。
- **验证状态**：title/author/DOI identity 由本地 metadata 核验；method、simulation、experiment、results、conclusion 已全文逐段核验；未联网复核。

### 2.2 七个结构化子表

#### A. 状态/输入空间

| 维度 | 范围/取值 | 归一化/处理 | 证据 |
|---|---|---|---|
| 两偏振接收序列 | `r'_X,r'_Y` 及加/差组合 | FS metric 含 normalization power factor；四路选 peak 最优者 | `content.md:135-155`（Eq. 17–19） |
| TS-B training unit | 4 个 CAZAC blocks + block 两侧 GI；`L` 个重复单元 | CAZAC constant amplitude/zero autocorrelation/flat spectrum；重复单元平均抗噪 | `content.md:63-133` |
| FOE correlation | known CAZAC 去数据后的序列；X/Y polarization | correlation averaging；two-symbol phase increment；X/Y 结果平均 | `content.md:157-201`（Eq. 20–28） |
| CE spectra | twofold-upsampled CAZAC 和两偏振 received spectra | `2×2` matrix inversion；ZF normalization | `content.md:227-251`（Eq. 34–36） |
| sampling grid | CE 明确 twofold upsampled（2 sps） | sampling phase 已由前级 Godard clock recovery 消除 | `content.md:43-57,227-231` |

#### B. 动作空间

| 类型 | 维度 | 合法动作约束 | 证据 |
|---|---:|---|---|
| 独立 timing/clock correction | 1 | Godard algorithm；发生在 TS-B FS 前 | `content.md:43-57` |
| 离散 TS-B frame index | 1 | 从 X/Y/加/差四个 metric 的 peak 中择 PMNR 最优者 | `content.md:135-155` |
| 连续 CFO | 1 | operational range `(-Rs/4,+Rs/4)`；X/Y average | `content.md:193-201` |
| channel/equalizer matrix | 每 frequency bin 的 `2×2 H(ω)`/`W(ω)` | matrix invertible；ZF criterion；可跨 `L` 次 average | `content.md:203-251` |
| joint `(frame, fractional delay, CFO)` action | 0 | **不存在单个联合搜索/联合目标**；模块按 clock→FS→FOE 顺序执行 | `content.md:43-57` |

#### C. 目标/奖励

| 项目 | 定义 | 归一化/权重 | 证据 |
|---|---|---|---|
| 学习奖励 | **N/A**：解析 preamble/DSP，无 ML/RL 训练 | N/A | Sections II–IV |
| preamble design target | 在 preamble length 与 FS/FOE/CE accuracy/convergence 之间折中 | 无加权总式；通过 `N,L` sweep 选择 | `content.md:259-293` |
| FS metric | PMNR；择四路最高 peak | power-normalized timing metric | `content.md:135-155,293-303` |
| FOE metric | absolute CFO error/range | X/Y average，无 reward weights | `content.md:193-201,311-315` |
| CE metric | post-CE SNR、first-block RMSE、convergence blocks | ZF normalized `W(ω)`；无多目标权重 | `content.md:243-251,283-291,317-343` |

#### D. 建模假设

| 假设 | 位置 | 对后续仿真器/比较的影响 |
|---|---|---|
| 前级 Godard clock recovery 已消除 sampling phase offset | Section II / Fig. 1 | 不能用此文证明 fractional timing 与 frame/CFO 已联合估计 | `content.md:43-57` |
| 短 FOE training 内 phase noise 近似常量 | Section II-D | 更快 linewidth/phase dynamics 需另行验证 | `content.md:157-179` |
| 至少一个 `rX,rY,rX+rY,rX-rY` metric 非零 | Section II-C | FS 需四路并行/择优；单路 metric 在特定 RSOP 可失败 | `content.md:145-155` |
| CAZAC flat spectrum 支撑全带宽 FD-CE | Section II-A/B/E | 若 pulse shaping/notch/硬件破坏训练频谱，CE initialization 性能需另审 | `content.md:85-131,203-251` |
| 线性 optical effects 可乘成 transfer functions | Eq. 29–33 | 非线性、快速时变或 turbulence amplitude/phase 不在本文 channel matrix 实证内 | `content.md:203-227` |

#### E. 网络架构

| 层类型 | 维度 | 激活/归一化 | 优化器 | 说明 |
|---|---|---|---|---|
| N/A | N/A | N/A | N/A | 非学习法；DSP 为相关/FFT/matrix inversion/ZF/LMS/ML CPR（`content.md:135-257`） |

#### F. 适配性

| 适配点 | 不适配点 | 可供后续方法设计核查的方向（不是建议/裁决） |
|---|---|---|
| 2019+ 正式 JLT、receiver-known short preamble、RRC、DP-16QAM、2-sps CE；与 Q1 acquisition 很接近 | 场景为 fiber coherent PON 而非 CFSO；clock recovery 先于 TS-B；无 fractional-delay joint action | 后续任何 Q1 方法必须同 `TS-A/Godard → CAZAC FS→FOE` 比总 overhead、success/error、complexity，而不能只比单模块 |
| 同一 training unit 复用三种 DSP，构成很强的 shared-information baseline | “joint”是 training-resource integration，动作仍 sequential | 若新方法只共享 preamble 或重排顺序，delta 属于资源/顺序调整；只有显式联合估计 `(frame,τ,CFO)` 才是 action delta |

#### G. 问题提取（论文自身问题，不是 Q1 终态裁决）

| 字段 | 提取结果 | 证据 |
|---|---|---|
| M | 2021/2023/2024 coherent-PON burst preambles及其 time-domain simple-SOP CE / separated training | `content.md:31-39,447-457` |
| C | upstream burst-mode coherent PON，在短 overhead 下还需容忍 large DGD、CD、PDL、RSOP 并快速收敛 | `content.md:21-39` |
| A | simple SOP-only time-domain CE 足以初始化 equalizer，且多 DSP 使用分离/较长 TS 的 overhead 可接受 | `content.md:31-39` |
| M-C-A | 既有 coherent-PON burst preamble 在严格 overhead 与多线性 impairment 条件下，因 CE 仅建模 simple SOP 且训练资源未充分共享而导致 LMS convergence/preamble length 不足 | `content.md:31-39` |
| 失效假设定位 | Introduction 对 prior preamble、large DGD 与 power-envelope 问题的陈述 | `content.md:31-39` |
| 方法产出形态 | CAZAC preamble design + FS/FOE/FD-CE/ZF initialization DSP chain | `content.md:41-257` |
| 判据 1 | ✅ M/C/A 为具体 burst-DSP 矛盾 | 同上 |
| 判据 2 | ✅ 可复用 preamble、metric、estimator、channel initializer | `content.md:41-257` |
| 判据 3 | ✅ 识别出 2021 JOCN、2023/2024 JLT task-matched preamble baselines；但只引用 reported length，未受控重跑完整链 | `content.md:31-39,447-457` |
| 判据 4 | ✅ preamble symbols/ns、FOE error/range、PMNR、SNR/RMSE、convergence blocks 可量化；完整 pipeline 的公平 head-to-head 证据仍不完整 | `content.md:259-401` |
| 四判据 | **结构上全过；实验 comparator 完备性有限**。这里只供主线综合，不作 Q1 终态裁决 | — |

### 2.3 通信信道模型参数表

| 链路/层 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| pulse shaping | RRC Tx/Rx | roll-off 0.1；15 Gbaud；CE 使用 twofold-upsampled training | `content.md:211-231,265-277` |
| linear fiber channel（simulation） | RSOP + first-order PMD + PDL + CD + bandwidth limitation | random RSOP；DGD 30 ps（sweep 10–90 ps）；PDL 3 dB（sweep 1–7 dB）；CD 340 ps/nm（tolerance test to 1360 ps/nm） | `content.md:203-227,265-281,331-343` |
| noise/offset（simulation） | AWGN + time delay + CFO | SNR 18 dB；configuration table time delay 0/FO 0，完整 robustness runs 另加 random delay、FO（常用 200 MHz） | `content.md:265-283,293-317` |
| optical experiment | 11 km SSMF coherent link | λ=1550 nm；ECL linewidth <100 kHz；Tx launch after EDFA 0 dBm；ROP controlled by VOA；device CFO约 200 MHz | `content.md:345-371` |

### 2.4 实验完备性（≤20 行）

- **C1/scope**：272-symbol preamble 在 15-Gbaud DP-16QAM coherent-PON proof-of-concept 中可支持 FS/FOE/CE 并加速 equalizer convergence；bounded to tested setup（`content.md:345-401`）。
- **C2/scope**：仿真分别验证 RSOP/CD/PMD/PDL tolerance；每个 Fig. 7 subplot 只保留一种 optical effect，故不是这些极端 impairment 同时存在的 universal claim（`content.md:331-343`）。
- **统计规范性**：CE/FOE averages over 100 trials，FS over 50 trials；无 seed、error bar、CI 或显著性检验（`content.md:283-295,315`）。
- **Baseline 矩阵**：ordinary 16QAM CE、standard equalizer without CE、4th-power FOE reference；prior 2021/2023/2024 preambles只作 cited-length 对照；无统一调参预算（`content.md:31-39,281-291,317-331,369-393`）。
- **消融设计**：`N∈{32,64,128,256,512}`、`L∈{1,2,4,20}` 参数扫描及 CAZAC vs ordinary 16QAM；没有逐模块删除 FS/FOE/CE 的 end-to-end ablation（`content.md:281-293`）。
- **信道真实性**：仿真采用可解释线性 transfer-function model，实验为 11 km SSMF；未含 CFSO turbulence/fade/SCO（`content.md:203-227,345-367`）。
- **配置多样性**：多 impairment 单因素 sweep + 一个实验 fiber distance/modulation/rate；没有多 baud、调制、距离或 burst-clock distribution。
- **复杂度**：无理论 O()、实测 module latency、FLOPs/operation count；只报告 preamble overhead 和 convergence blocks。
- **VVUQ**：Verification=3/3（解析推导+仿真+硬件实验）；Validation=2/3（真实 coherent link，但单 rate/modulation/distance 且不是 CFSO）；Uncertainty=2/3（50/100 trials averages，但无误差条/CI/显著性检验）（`content.md:259-401`）。

### 2.5 Sun 2025 写作架构

- **章节结构**：I Introduction；II Principles，下分 A CAZAC properties、B TS-B structure、C FS、D FOE、E CE、F FD equalization & pilot-aided CPR；III Simulation Results；IV Experiment（A setup、B results）；V Conclusion（`content.md:13,41-41,63-63,119-119,135-135,157-157,203-203,253-259,345-347,369-369,391-401`）。
- **图表组织**：Fig. 1 frame structure/DSP flow；Fig. 2 sequence properties；Fig. 3 simulation chain + `N/L` selection；Fig. 4 FS；Fig. 5 FOE；Fig. 6–7 CE/convergence/robustness；Fig. 8 hardware setup；Fig. 9–12 measured SNR/FOE/convergence/coefficients。Table I 集中列 simulation parameters（`content.md:43-61,237-315,323-387`）。
- **实验组织**：先用参数扫描选 `N=64,L=2`，再分别验证 FS、FOE、CE，最后用硬件链做 proof-of-concept；这形成“配置选择→模块 robustness→端到端实验”三层证据（`content.md:259-343,345-401`）。
- **叙述模式**：Introduction 按“burst-mode convergence/overhead 问题→既有 preamble 数字与 simple-SOP CE 缺陷→两项设计优势→与 OFC 2024 的扩展关系→272-symbol 实验”推进（`content.md:21-39`）；Conclusion 回收为 FD-CE preconvergence、shared-unit integration、multi-impairment simulation、15-Gbaud experiment 四层（`content.md:391-401`）。
- **公式使用**：先证明 CAZAC zero autocorrelation/flat spectrum/transformation invariance（Eq. 1–13），再给 TS-B construction（Eq. 14–16），随后按 DSP 流程给 FS（17–19）、FOE（20–28）、channel transfer/CE/ZF（29–36）；每组公式前后都有物理解释和边界条件（`content.md:63-251`）。
- **参数展示**：核心 simulation configuration 集中于 Table I；最终 preamble/equalizer/experiment 参数也在正文重复，便于把设计选择与实验对应（`content.md:263-283,317-317,345-349,393`）。
- **共同引用核对**：与 Tang 2022 的参考文献表未发现题名完全相同的共同引用。Sun 对本题最直接的引用种子是 2021 JOCN burst preamble、2023/2024 JLT burst DSP、2014 JLT training-aided FD-CE、1997 data-aided frequency estimator与其 OFC 2024 前身（`content.md:447-465`）。

---

## 3. 本组综合（供主线集成，不作终态裁决）

### 3.1 Q1 collision 表

| 对象 | information | action | output | timing | task |
|---|---|---|---|---|---|
| **Q1 候选定义** | receiver-known preamble + ≥2-sps waveform，保留 fractional sample phase、frame offset、CFO 信息 | 显式联合或 coarse-to-fine 地估计/搜索 `(frame index, fractional delay, CFO)` | 三元 acquisition estimate 或等价 coupled correction | acquisition 前端；不能预先假定 timing 已恢复 | sample-level timing/frame/CFO acquisition in coherent FSO |
| **Tang 2022 STSB** | known symmetric training；**1 sps**；clock sync/equalization 后样本 | 先 `argmax` frame/training index，再单独 CFO | frame index + CFO + corrected symbols | `clock sync → frame localization → FOE → CPR` | QPSK CFSO；直接 frame+CFO，但 timing recovery 被排除（`content.md:43-85`） |
| **Sun 2025 CAZAC** | TS-A/TS-B known preamble；DP samples；CE 时 2 sps | Godard clock correction 后，TS-B 依次 FS、FOE、CE | clock-corrected samples + frame index + CFO + `H/W` | `TS-A detect/clock → TS-B FS → FOE → CE` | DP-16QAM coherent-PON burst acquisition；shared unit，不是联合 action（`content.md:43-57,227-257`） |

碰撞事实：Tang 占用“CFSO 中同一对称训练结构做 frame localization + CFO”的 information/output 组合；Sun 占用“短 CAZAC preamble 共享 FS/FOE/CE，且 2-sps waveform”的 information/resource 组合。两者都没有占用“在 timing 未恢复的 oversampled samples 上联合估计 `(frame, fractional delay, CFO)`”这一 action 定义；这只是本组全文的覆盖事实，不能替代 Step 3.5 的新颖性闭合。

### 3.2 JLT 2025 是否覆盖 sample-level timing/frame/CFO

**不覆盖。** Sun 2025 的 receiver flow 先做 coarse frame detection，再用 Godard clock recovery **消除 sampling phase offset**，之后才以 TS-B sequentially 执行 FS 和 FOE（`content.md:43-57`）。它在 CE 中使用 twofold-upsampled CAZAC samples（`content.md:227-231`），但没有把 fractional delay 与 frame index/CFO 放进同一个 estimator/action。因此，“2 sps + joint FS/FOE/CE”不能被改写成“sample-level timing/frame/CFO 联合动作”；文中的 joint 是 shared training unit integration（`content.md:35-39,133-137`）。

### 3.3 最强廉价 comparator

1. **跨 coherent receiver、近期 task-matched 的首要 comparator**：Sun 2025 的 `TS-A frame detect + Godard clock recovery → 272-symbol CAZAC TS-B FS→FOE`。它已经覆盖 RRC、DP-16QAM、短 preamble、burst、frame+CFO，并把 clock recovery 明确放入总链；若只与单独 FS 或单独 FOE 比，会漏掉最便宜的顺序链替代解释（`content.md:39-57,345-401`）。
2. **CFSO 域内廉价 comparator**：独立 clock/timing recovery 后接 Tang 2022 STSB frame localization→FOE。其优势是 CFSO turbulence 直接实证；限制是 QPSK、1 sps 与同步采样钟（`content.md:43-47,85,107-195`）。

### 3.4 剩余 delta：真正联合动作还是顺序调整

- 若候选只把 Godard timing、STSB/CAZAC frame metric 与 FOE 调换顺序、复用同一 preamble 或共享中间量，它仍是 **顺序/资源整合 delta**；Sun 已明确覆盖“同一训练单元复用多个 DSP”这一形态（`content.md:35-57,133-137`）。
- 只有当 fractional delay 在未完成 clock recovery 的 ≥2-sps samples 上成为显式待估变量，并与 frame index、CFO 进入同一 coupled likelihood/metric/search 或有可验证的 coarse-to-fine feedback coupling，才构成任务书所指的 **真正联合 action delta**。
- 本组全文只证明上述 baseline 的 action boundary；不证明该 delta 新颖、有效或值得做。

### 3.5 供 Step 3.5 的引用链种子（只列，不检索）

| 种子 | 用途 | 本地证据 |
|---|---|---|
| Li, Wang & Jiang, JLT 2019, *Efficient timing/frequency synchronization based on sparse FFT*，DOI `10.1109/JLT.2019.2932075` | 2019+ timing/frequency direct seed；Tang 引用但未作结果 comparator | Tang `content.md:245-249` |
| Xian et al. 2011, *Wide-range frequency offset estimation ... using training sequence* | Tang 的 TSB/Schmidl-Cox lineage | Tang `content.md:251-255` |
| Park et al. 2003 timing estimator + Schmidl & Cox 1997 | symmetric/conjugate timing-metric lineage | Tang `content.md:253-255` |
| Zhang et al., JOCN 2021, *Efficient preamble design ... upstream burst-mode ... coherent-PON* | 2019+ task-matched burst preamble comparator | Sun `content.md:447-449` |
| Wang et al., JLT 2023, *Fast-Convergence DSP for Coherent PON Using Digital SCM* | 2019+ short-preamble/fast-convergence comparator | Sun `content.md:449-451` |
| Li et al., JLT 2024, *Burst-mode Signal Reception for 200G Coherent TFDMA PON* | 2019+ burst FS/FOE/CE comparator | Sun `content.md:451-453` |
| Pittalà et al., JLT 2014, training-aided FD channel estimation/equalization | CAZAC/FD-CE action lineage | Sun `content.md:453-455` |
| Sun et al., OFC 2024 prior report | JLT 2025 方法前身/版本血缘 | Sun `content.md:457-457` |
| Mengali & Morelli 1997 data-aided frequency estimation | Sun FOE estimator lineage | Sun `content.md:463-465` |

### 3.6 供 Step 3.5 的关键词（只列，不检索）

- `oversampled coherent optical joint timing frequency acquisition preamble`
- `sample-level frame synchronization fractional timing offset carrier frequency offset`
- `joint maximum likelihood timing frame CFO coherent receiver RRC 2 samples per symbol`
- `coarse-to-fine timing frequency synchronization burst-mode coherent optical`
- `fractional delay CFO coupled estimator CAZAC coherent optical`
- `coherent FSO preamble timing recovery frame synchronization frequency offset turbulence`
- `sampling clock offset frame synchronization CFO burst coherent receiver`
- `timing frequency synchronization sparse FFT coherent optical JLT 2019 citations`

## 4. 最小事实结论

本组最关键的可复核事实是：**Tang 2022 的 STSB 输入已被前级 clock synchronization 降为 1 sample/symbol；Sun 2025 则先用 Godard clock recovery 消除 sampling phase offset，再顺序执行 TS-B FS→FOE。** 因此两篇都覆盖强的“独立 timing/clock + frame+CFO”廉价顺序 comparator，却都没有在未定时的 ≥2-sps 样本上执行 `(frame, fractional delay, CFO)` 联合动作（Tang `content.md:43-47,85`；Sun `content.md:43-57,227-231`）。
