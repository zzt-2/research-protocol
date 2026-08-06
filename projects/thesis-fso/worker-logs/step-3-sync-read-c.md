# Step 3：Q2 维护与重捕获 CORE 全文精读（C）

> 日期：2026-08-06
> 范围：仅做 Paillier et al. 2020 与 Valjus et al. 2025 的全文事实提取；不进入 Step 3.5、Step 4a、实现或仿真。
> 引用约定：Valjus 全文实际读取自任务书指定的共享库文件，以下统一写 canonical 路径 `papers/doi/10.1002_sat.1553/content.md`。

## 0. 身份与 title abort 自检

| 论文 | 自检结果 | 定位证据 | 处理 |
|---|---|---|---|
| Paillier et al. 2020, *Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop* | `title-unverifiable`：转换稿无论文标题，首行是 IEEEtran 占位文本；但关键词、研究目标与结论均与派遣标题一致 | `papers/doi/10.1109_jlt.2020.3003561/content.md:1-4,17-19,204-206` | 按 `gw-read` 协议人工抽检主题后继续；不是 title mismatch |
| Valjus et al. 2025, *Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links* | PASS：正文 H1 与派遣标题逐字一致 | `papers/doi/10.1002_sat.1553/content.md:11,85-103` | 继续精读 |

## 1. Paillier et al. 2020

### 1.1 标准字段

- **DOI/来源**：`10.1109/JLT.2020.3003561`。
- **源文件路径**：`papers/doi/10.1109_jlt.2020.3003561/content.md`。
- **发表状态/渠道**：正式发表，*IEEE Journal of Lightwave Technology*，2020（派遣身份；本地转换稿未保留标题页）。
- **核心贡献**：论文用 TURANDOT 与闭环 AO 仿真生成相干 LEO 下行的耦合效率和湍流相位噪声时序，再提出串联数字 AGC 与二阶 DPLL 的基带载波同步接收机。AGC 把输入功率拉到单位参考，使 DPLL 的单位相位检测器增益假设更接近成立；DPLL 负责先捕获残余频偏，再跟踪频率和相位变化。`content.md:57-59,83-96,114-145`
- **方法概述**：接收 I/Q 样本先经功率误差驱动的指数增益 AGC，再经 MAP/低 SNR 近似相位检测器、二阶环路滤波器和相位 NCO；设计用阻尼系数、环路带宽和自然频率映射到环路增益，并用 pull-in 公式预测捕获时间。`content.md:120-145`
- **实验设置**：10 GBaud BPSK、符号率采样、残余固定 CFO 100 MHz；先在 AWGN/恒幅下验证 DPLL，再用同一 2 s TURANDOT+AO 耦合效率/相位时序评估 AGC、捕获、稳态相位误差和 BER。`content.md:83-96,106-112,160-173`
- **receiver-visible information**：ADC 后复 I/Q 样本、瞬时样本功率、AGC 单位参考功率、相位检测器误差及环路历史状态；粗频偏预补偿来自轨道知识，但具体粗估计器在范围外。`content.md:106-120,130,138-145`
- **action**：AGC 以 `g(k)=exp(-v(k)/2)` 缩放复样本；DPLL NCO 对下一样本施加相位校正。正文没有 `hold/update/reacquire` 离散状态或共享冻结动作。`content.md:130-141`
- **output**：单位功率附近的复样本、DPLL 相位/频率校正后符号流、BPSK 判决和差分解码比特。`content.md:120-122,177-200`
- **时序/处理顺序**：AO → 相干检测/ADC → AGC → DPLL（先频率捕获、后相位/频率跟踪）→ 符号检测 → 差分解码；理想 timing recovery 是前置假设。`content.md:31-33,110,114-122`
- **Baseline/参照**：没有与另一种载波算法做公平算法对比；参照包括 CRB/含 squaring-loss 理论方差、无湍流恒幅 DPLL、完美频率/相位同步 BER，以及有/无湍流相位噪声的情景切换。`content.md:160-169,190-200`
- **failure condition/适用边界**：无幅度起伏时约低于 -9 dB DPLL 不能锁定并进入非线性不稳定区；fade 使该临界平均 SNR 约恶化 5 dB。正文不研究 timing/SCO；100 MHz 是假设的残余常频偏；仅 BPSK、单一 2 s 场景。`content.md:106-112,138,167,190,206`
- **关键结论**：100 MHz 残余 CFO 在恒幅和湍流时序中均约 1.4 ms 捕获；8 dB 及以上时稳态相位误差接近理论；湍流相位噪声影响可忽略，但幅度起伏造成 BER 罚损（BER=`10^-4` 时约 2.3 dB）并抬高失稳门限。`content.md:162-167,186-200`
- **与 Q2 关系**：直接支撑 carrier loop 在 fade 下的临界 SNR、失稳和捕获时间量化；同时明确承认全文假设理想 timing，实际 timing 会受 Doppler 与 fading 影响。它没有 SCO/timing loop，因此不能证明双环共同失锁或联合重捕获。`content.md:110,167,190,206`
- **实现关键数值**：`P_ref=1`、AGC `G0=0.1`；DPLL `T=0.1 ns`、阻尼 `1/sqrt(2)`、`B_L=5 MHz`、`K1=1.3×10^-3`、`K2=6.7×10^-4`、10 GHz loop frequency；目标 CFO 100 MHz。`content.md:130,143-157`
- **开源代码**：正文未报告代码仓库；TURANDOT 被描述为 ONERA/CNES 的传播代码。`content.md:57`
- **验证状态**：已完成本地全文、系统模型、方法、实验、结果、结论和 title-unverifiable 人工主题核验；未联网。

### 1.2 七个结构化子表

#### A. 状态/输入空间

| 维度 | 范围/取值 | 归一化/处理 | 证据 |
|---|---|---|---|
| 复接收样本 | `s_RX,I(k), s_RX,Q(k)`，含 `sqrt(rho(k))`、CFO、BPSK 相位和湍流相位 | 符号率采样；AGC 后目标单位功率 | `content.md:106-112` |
| AGC 功率误差 | `e(k)=|s_agc(k)|^2-P_ref` | `P_ref=1` | `content.md:126-130` |
| DPLL 相位误差 | MAP 检测器；低 SNR 近似 `epsilon=s_I s_Q` | 设计假定平均信号功率 `K_d=1` | `content.md:138-145` |
| 环路记忆 | AGC 一阶积分器；DPLL 二阶滤波器加一阶 NCO | 无显式 lock/hold/reacquire 标签 | `content.md:130,141` |

#### B. 动作空间

| 类型 | 维度 | 合法动作/约束 | 证据 |
|---|---:|---|---|
| 连续 AGC 增益 | 1 | `g(k)=exp(-v(k)/2)`；同时放大信号与噪声 | `content.md:130,177` |
| 连续相位 NCO 校正 | 1 | 每样本闭环更新；`K0=1` | `content.md:141` |
| 状态机动作 | 0 | 正文没有共享 update/hold/reacquire 控制 | `content.md:114-145` |

#### C. 目标/奖励

| 项目 | 内容 | 证据 |
|---|---|---|
| 学习奖励 | N/A：确定性控制环，不是学习方法 | `content.md:124-145` |
| 控制目标 | AGC 维持单位功率；DPLL 最小化残余相位误差并捕获/跟踪频偏 | `content.md:126-145` |
| 评价量 | pull-in time、相位误差方差、临界 SNR、BER | `content.md:160-200` |

#### D. 建模假设

| 假设 | 位置 | 对 Q2 的影响 |
|---|---|---|
| 理想 symbol synchronization | §III-A | 直接排除了 timing/SCO 失锁链 | `content.md:108-112` |
| 大部分 Doppler 已粗补偿，残余 CFO 固定为 100 MHz | §III-A | 不覆盖真实频率轨迹与重捕获触发 | `content.md:106` |
| `rho` 与湍流相位在一个符号内不变 | §III-A | 10 GBaud 下合理的文内时标分离，但不是 fade 事件状态机 | `content.md:112` |
| BPSK、单位 DPLL 输入功率 | §III-D | 相位检测器与环路增益绑定 BPSK/AGC | `content.md:138-145` |
| 单一 20° LEO 下行、2 s 时序、AO 5 kHz | §II | 场景覆盖窄，不给 fade 深度/持续时间分布 | `content.md:37-59,83-96` |

#### E. 网络架构

| 项目 | 内容 |
|---|---|
| 神经网络 | N/A：无学习模型 |
| 优化器/训练 | N/A：解析设计的 AGC/DPLL 闭环 |

#### F. 适配性

| 适配点 | 不适配点 | 可供后续核查的方向（非建议/非方法结论） |
|---|---|---|
| 给出 fade 下 carrier 临界 SNR、1.4 ms 捕获和 BER/相位误差指标；AGC→DPLL 是合法传统 carrier baseline | 理想 timing；无 SCO、无 timing NCO/interpolator、无 post-fade 双环恢复；无共享状态 | 核查把同一 receiver-visible 置信度用于双环门控后，是否有超过“共同冻结+固定重启”的增量 |

#### G. 问题提取（该论文自身）

| 字段 | 提取 |
|---|---|
| M | 既有 FSO Mth-power/open-loop carrier recovery 未专门评估同步组件；既有 OPLL Doppler研究未纳入湍流幅度起伏 `content.md:13-17` |
| C | AO 后仍有残余幅度/相位扰动的 10 GBaud BPSK LEO-to-ground coherent FSO，残余 CFO 100 MHz |
| A | carrier loop 可按恒幅/无真实湍流假设设计与评估；论文用 AGC 使单位幅度假设近似成立并实测该边界 `content.md:138-145,171-190` |
| 失效假设定位 | §I 既有工作边界、§III-D 恒幅设计、§IV fade 结果 `content.md:13-17,138-145,190` |
| 方法产出形态 | AGC+DPLL 接收机架构、环路设计参数和 pull-in 公式/性能曲线族 |
| 判据 1 | ✅：M/C/A 是明确的载波同步矛盾 |
| 判据 2 | ✅：闭环架构与设计公式可复用 |
| 判据 3 | ❌：文内直接算法参照不是 2019+ 的 task-matched 联合 timing/carrier maintenance baseline；本文自身不能充当自身 comparator |
| 判据 4 | ✅（仅 carrier 子问题）：有 pull-in time、相位方差、临界 SNR、BER；不等于 Q2 双环可量化对标 |

### 1.3 通信信道参数

| 链路类型 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| LEO-to-ground coherent FSO | Hufnagel-Valley `C_n^2(h)`（ITU-R P.1621-1）+ Bufton 风场 + 35 层 split-step Fresnel + AO | `lambda=1550 nm`，`C0=10^-13 m^-2/3`，`v_RMS=20 m/s`，`v_G=10 m/s`，`v_T=20 m/s`，`r0=0.039 m`，`L0=5 m`，scintillation index `0.684`，elevation `20°`，satellite transverse velocity `6.5 km/s`，Rx aperture `50 cm` | `content.md:37-57` |
| AO 后相干耦合 | TURANDOT+AO 复场重叠积分时序 | Zernike 至 mode 91（12 radial orders），AO 5 kHz、2-frame delay；平均 flux penalty `-4.5 dB`；2 s correlated series | `content.md:57-85` |
| 电域接收 | shot-noise-dominant AWGN + 上述耦合效率/相位时序 | LO 功率高于信号；10 GBaud BPSK；CFO 100 MHz | `content.md:106-112,143-157` |

### 1.4 实验完备性（≤20 行）

- **声称清单**：C1 AO+AGC+DPLL 可在代表性 LEO 下行湍流时序中捕获/跟踪 100 MHz；C2 湍流相位噪声影响可忽略；C3 幅度 fade 抬高临界 SNR并造成 BER 罚损。`content.md:186-206`
- **声称 scope**：bounded；限定 BPSK、单一 LEO/AO 参数和 2 s 仿真时序。
- **统计规范性**：seeds/独立时序数未报告；无 error bar、置信区间或统计检验。
- **Baseline 矩阵**：算法 comparator=0；理论/情景参照为 CRB/squaring-loss、完美同步 BER、无湍流/无湍流相位噪声。未报告公平调参预算。
- **消融设计**：AO on/off、turbulent phase noise on/off、CFO on/off 属情景切换；没有 timing/carrier 逐模块状态机消融。
- **信道模型**：物理传播+AO 的高真实性数值链，参数有 ITU-R/文献来源；不是 Gamma-Gamma，也不是外场 trace。`content.md:37-59`
- **配置多样性**：单一 LEO-to-ground、20°、单一湍流/AO配置、BPSK。
- **复杂度报告**：无 O()、推理延迟或硬件资源；仅给环路参数和捕获时间。
- **VVUQ**：V=2（理论方差/pull-in 与数值吻合）；V'=2（物理传播/AO链但无外场验证）；U=1（无多 realization/不确定性统计）。

### 1.5 写作架构提取

- **章节结构**：Introduction → coherent LEO-ground 系统/信道模型 → 相干检测与 AGC/DPLL 设计 → AO 后系统性能 → Conclusion；System Model、Receiver Design、Performance 三层职责清晰。`content.md:7-204`
- **参数展示**：两张集中参数表分别冻结湍流/链路参数与 DPLL 参数；公式附近解释物理意义，并把 `B_L, xi, omega_n` 映射回实现增益。`content.md:37-57,143-157`
- **图表模式**：先给端到端链路图和数字接收机/AGC/DPLL 框图，再给耦合效率与相位时序/PDF，最后给 acquisition、phase-error variance 和 BER 曲线；图表按“物理输入→算法→性能”递进。`content.md:23-33,81-98,114-169,171-202`
- **实验组织**：先以 AWGN/恒幅验证解析设计，再逐项加入 AO 后幅度起伏、频偏、湍流相位噪声，最后汇总 BER；这种由理想到真实的递进使每个性能变化有明确归因。`content.md:160-200`
- **Baseline/消融组织**：没有多算法 baseline；主要用理论界、完美同步和 impairment on/off 作参照。
- **叙述模式**：引言从卫星 coherent optical 需求进入 Doppler 与 turbulence 两类困难，再指出既有工作未同时评估 carrier synchronization 与真实幅度扰动，随后声明 AGC+DPLL 方案和章节路线。`content.md:9-19`
- **公式使用**：先定义复耦合、幅度与相位噪声，再定义离散 I/Q，最后给 AGC/DPLL 控制律与 pull-in/方差公式；变量均在公式后解释。`content.md:65-79,106-112,130-167`
- **共同引用线索**：Gardner 的 PLL 设计理论、Simon 的 carrier detector/同步理论，以及开放环 carrier recovery 是该写法的理论锚；本任务不摘录长原文。

## 2. Valjus et al. 2025

### 2.1 标准字段

- **DOI/来源**：`10.1002/sat.1553`。
- **源文件路径**：`papers/doi/10.1002_sat.1553/content.md`。
- **发表状态/渠道**：正式发表，*International Journal of Satellite Communications and Networking*, 43(3), 229–250；online first 2025-02-11。`content.md:3,85-97`
- **核心贡献**：论文把 coherent OSL 数字接收机拆为 timing recovery、carrier synchronization 与 equalization，系统综述候选算法，并在四种 OSL fading 场景下用数值仿真比较 timing、CPE、FOE 与 equalizer 的性能/复杂度权衡。它特别指出低 SNR fade、反馈环延迟、pilot 对齐和各子系统依赖会改变 terrestrial DSP 在 OSL 中的适用性。`content.md:101-111,169-183,385-395,788-790`
- **方法概述**：timing 比较 Gardner/Godard/Gu feedback 与 Lee feedforward 及多种插值；CPE 比较 VV 差分/非差分与 pilot；FOE 比较 blind time/frequency、data-aided、Schmidl-Cox/CRT；所有结果通过 SNR penalty、tracking range 或 MSE 归纳。`content.md:185-382,397-448,468-558`
- **实验设置**：四场景（ISL beta pointing、downlink lognormal scintillation、两种 uplink combined fading），baseline SNR 调到平均 BER `10^-3`；channel 被视为 quasi-static，不建模 fade coherence-time 轨迹。各 DSP 子系统单独仿真，而非完整链联合运行。`content.md:121-167`
- **receiver-visible information**：复样本 `r[n]`、其功率/频域分量、TED 输出、receiver-known training/pilot/preamble、过去样本/块和估计历史；正文没有 TX payload truth 作为部署输入。`content.md:171-183,187-248,399-430,470-508`
- **action**：timing feedback 环驱动 NCO/重采样相位，或 feedforward 估计块时延后重采样；CPE/FOE 施加相位/频率补偿。fade 门控只被明确提到为 FOE 低质量时避免更新（equalizer 也引用低功率停止 tracking），没有 timing+carrier 共享门控状态机。`content.md:171-183,255-304,451-466,548-558,582`
- **output**：重采样且与符号时钟同步的样本、carrier phase/frequency 校正样本、各估计量；性能输出包括 SNR penalty、BER、FOE MSE、可跟踪 ppm/旋转速度。`content.md:349-382,432-448,510-558`
- **时序/处理顺序**：典型链为 static compensation → timing recovery → adaptive equalization → carrier recovery → FEC；pilot CPE 依赖 frame synchronization 和稳定 timing。`content.md:109-111,440,788-790`
- **Baseline/参照**：timing：Gardner/Godard/Gu、Lee；interpolation：FFT、Lagrange、trigonometric、linear；CPE：VV non-differential/differential、pilot；FOE：blind time/frequency、data-aided、Schmidl-Cox、CRT。均为正文实现或公式复现的数值比较。`content.md:349-382,432-448,510-548`
- **failure condition/适用边界**：feedback timing 受并行度/loop latency 限制，feedforward timing 有 noise tolerance 与 SCO tracking range 交换；cycle slip 会令 non-differential VV 等待下一 phase reference；pilot CPE 在 timing/frame alignment 丢失时失败。timing 仿真排除了 clock jitter、carrier phase noise 和 polarization；fading 是准静态分布，未模拟 post-fade 联合恢复。`content.md:279-281,331-353,382-383,408-440`
- **关键结论**：低/中并行度时 Gardner/Godard 等 feedback timing 整体优于 Lee；高并行度和长延迟会压缩可跟踪 SCO。pilot CPE 在深 fade 场景可优于 differential VV；FOE 在信号质量过低时很可能需要停止更新。完整 DSP 链必须在真实条件下联合评估，但本文没有做该联合评估。`content.md:382-383,434-440,548-558,788-790`
- **与 Q2 关系**：它给出 timing/fade/SCO 与 carrier/fade 的分别证据、低 SNR timing 对 pilot carrier 的依赖，以及 carrier FOE 的 threshold-hold 动机；但没有同一 fade trace 下 timing/carrier 共同失锁、共享冻结、固定重启或恢复时间比较。`content.md:167,351-353,440,548-558,788-790`
- **实现关键数值**：timing：RRC roll-off 0.2、`10^7` symbols/SNR、parallelization 64/256、20-cycle loop latency、Lee block 512/1024/2048/4096、4-tap Lagrange（Godard 除外）；CPE：VV window 32/64/256、phase reference every `10^5` symbols、pilot rates 7/8, 15/16, 31/32；FOE：`10^6` estimates/SNR、90% valid range。`content.md:349-355,432-440,510-518`
- **开源代码**：正文未报告代码仓库。
- **验证状态**：已完成本地全文 title、系统模型、timing、carrier phase、carrier frequency、equalizer、实验分析与结论核验；未联网。

### 2.2 七个结构化子表

#### A. 状态/输入空间

| 维度 | 范围/取值 | 归一化/处理 | 证据 |
|---|---|---|---|
| timing 输入 | oversampled complex `r[n]`，时域/频域块 | RRC roll-off 0.2；通常 2 sps，Lee 原始式需 4 sps | `content.md:187-281,349-353` |
| timing 状态 | TED error、NCO/重采样相位、历史 loop state | feedback 滤波；feedforward 直接块估计 | `content.md:171-183` |
| carrier phase 输入 | QPSK samples、pilot/phase reference、窗口历史 | VV M-th power 或 pilot interpolation | `content.md:399-435` |
| carrier frequency 输入 | QPSK samples、known sequence/preamble 或 M-th-power samples | observation window/FFT/lag 参数化 | `content.md:470-518` |
| channel indicator | 接收功率/SNR；论文建议低质量阈值门控 FOE | 没有给 threshold 数值或 lock indicator 定义 | `content.md:548-558` |

#### B. 动作空间

| 类型 | 维度 | 合法动作/约束 | 证据 |
|---|---:|---|---|
| timing NCO/interpolator | 连续相位/频率 | feedback 每环更新或 feedforward 每块更新 | `content.md:171-183,283-347` |
| carrier phase correction | 连续相位 | VV/differential/pilot estimate | `content.md:397-430` |
| carrier frequency correction | 连续频率 | blind/data-aided range受 `fs,M,L,N` 限制 | `content.md:451-508` |
| hold | 二值建议 | 仅明确建议 FOE 在低质量时不更新；未定义共享 timing/carrier hold | `content.md:548-558` |
| reacquire | 固定 reference/preamble | non-differential VV cycle slip 后等待下一 phase reference；未形成双环 reacquire | `content.md:434-440` |

#### C. 目标/奖励

| 项目 | 内容 | 证据 |
|---|---|---|
| 学习奖励 | N/A：非学习方法综述与数值比较 | 全文 §§3–6 |
| timing 目标 | 相对完美同步系统在 BER=`10^-3` 时的 SNR penalty、可跟踪 clock offset | `content.md:349-382` |
| CPE 目标 | 含 overhead 的 SNR penalty、cycle-slip/burst-error 风险 | `content.md:432-448` |
| FOE 目标 | 估计 MSE、frequency range、phase-noise 鲁棒性 | `content.md:510-558` |

#### D. 建模假设

| 假设 | 位置 | 对 Q2 的影响 |
|---|---|---|
| fading 只通过 SNR PDF 平均，channel quasi-static；不建 coherence-time 轨迹 | §2 | 无法观察 fade 进入/退出和 post-fade 恢复时间 `content.md:149-167` |
| timing 仿真只含 RRC、clock offset、AWGN | §3.4 | 明确排除 carrier phase noise、jitter、polarization，不能验证双环共同失锁 `content.md:349-353` |
| CPE/FOE 各自独立仿真 | §§4.2/5.2 | 不传播 timing error/失锁到 carrier 子系统 |
| average BER 使用无限 interleaver 等价 | §2 | 不代表有限帧 fade burst 和重捕获损失 `content.md:167` |
| 四个场景以 beta/lognormal/组合 PDF 表征 | §2 | 不是 Q2 预卡所称 Gamma-Gamma dynamic fade `content.md:121-157` |

#### E. 网络架构

| 项目 | 内容 |
|---|---|
| 神经网络 | N/A：没有学习网络 |
| 优化器/训练 | N/A：解析 estimator、控制环和数值 sweep |

#### F. 适配性

| 适配点 | 不适配点 | 可供后续核查的方向（非建议/非方法结论） |
|---|---|---|
| 2025 task-matched OSL 综述；给出 timing/CPE/FOE 合法传统算法、SCO范围和低 SNR依赖；明确提示 FOE fade hold | 没有动态 fade trace、Gamma-Gamma、joint chain、lock state、shared freeze 或 recovery-time 实验；timing 排除 carrier impairment | 引用链仅需查“scintillation-tolerant timing recovery”“cross-loop freeze/reacquisition”“loss-of-lock detector”是否已有同信息/动作/任务竞品 |

#### G. 问题提取（该论文自身）

| 字段 | 提取 |
|---|---|
| M | 面向相对稳定 terrestrial fiber 的 timing/carrier/equalizer DSP 及其实现架构 `content.md:107-111,183,395` |
| C | OSL 的低 SNR fade、SCO/Doppler、强并行与 SWaP 约束 |
| A | terrestrial 算法的静态信道、较低反馈延迟和独立子系统假设可直接移植到 OSL |
| 失效假设定位 | timing 动态信道缺口 `content.md:183`；phase 低 SNR缺口 `content.md:395`；完整链依赖 `content.md:788-790` |
| 方法产出形态 | 算法选择/实现准则及跨四场景的性能曲线族；不是新的联合状态机 |
| 判据 1 | ✅：M/C/A 明确，但论文覆盖多个子问题 |
| 判据 2 | ✅：比较曲线与实现权衡可复用为 design rule |
| 判据 3 | ✅（timing 子问题）：含 2019 Gu FSO timing 与 2023 OSL timing comparison；❌（Q2 联合维护）：无 2019+ integrated timing+carrier state-machine baseline `content.md:1019,1140` |
| 判据 4 | ✅（各独立子系统）：SNR penalty/MSE/tracking range 可量化；❌（Q2 联合维护）：没有恢复时间/共同失锁/联合增益对照 |

### 2.3 通信信道参数

| 链路类型 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| ISL | pointing-jitter beta distribution | beam divergence `25 μrad`，jitter RMS `3 μrad` | `content.md:121-139,152-157` |
| satellite-ground downlink | lognormal scintillation，mean=1 | scintillation parameter table value `0.029` | `content.md:141-157` |
| uplink scenario 3 | turbulence + pointing combined PDF | `sigma_p^2=0.15`，`theta0=3 μrad`，`sigma_jitt=1.7 μrad` | `content.md:148-157` |
| uplink scenario 4 | turbulence + pointing combined PDF | `sigma_p^2=0.25`，`theta0=34.5 μrad`，`sigma_jitt=25.6 μrad` | `content.md:148-157` |
| DSP averaging | SNR distribution assumed equal to received-power distribution | baseline SNR chosen for average BER `10^-3`; quasi-static channel; coherence time not simulated | `content.md:149-167` |

### 2.4 实验完备性（≤20 行）

- **声称清单**：C1 比较 OSL timing/CPE/FOE/equalizer 算法；C2 data-aided DSP 在低 SNR和快速 acquisition 上有吸引力；C3完整 DSP chain 的依赖必须联合评估。`content.md:101-111,788-790`
- **声称 scope**：混合；多数数值结论 bounded 到四个理想化场景，结论中的 architecture judgment 较宽但同时承认需真实完整链验证。
- **统计规范性**：timing/CPE `10^7` symbols/SNR；FOE `10^6` estimates/SNR；equalizer部分平均100次。未报告 seeds、error bar或显著性检验。`content.md:351,434,512,755-758`
- **Baseline 矩阵**：timing 4 estimator families+插值器；CPE 3 families；FOE 5 families；来源引用充分。参数“为展示优缺点而选”，并承认可进一步优化，故公平调参不闭合。`content.md:432-440`
- **消融设计**：主要为 block size、parallelization、loop latency、roll-off、pilot rate、phase-noise强度等参数扫描；不是完整链逐模块删除/替换。
- **信道模型**：beta/lognormal/combined PDF，参数引用若干 OSL文献；不含动态 coherence、Gamma-Gamma或外场 trace。`content.md:121-167`
- **配置多样性**：4种链路/衰落场景；timing/CPE/FOE 独立运行。
- **复杂度报告**：有乘法次数、反馈延迟、FFT/并行实现等定性/局部量化；无统一 O()、芯片面积、功耗或端到端延迟。`content.md:283-347,382-383`
- **VVUQ**：V=2（公式与大样本数值比较，未开源复核）；V'=1（无完整链/硬件/外场，动态 fade 未建模）；U=1（无 seeds/error bar/统计检验）。

## 3. 本组 Q2 综合（仅 Step 3 事实裁决）

### 3.1 GG/fade+SCO 下 timing/carrier 共同失锁是否有正文证据？

**正文未证实。**

- Paillier 给出 carrier DPLL 单环失稳：恒幅 AWGN 下约低于 `-9 dB` 无法锁定，加入 fade 后临界平均 SNR约恶化 `5 dB`；但它显式假设 ideal symbol synchronization，结论只说实际 timing “也会”受 Doppler/fading 影响。该句是动机，不是共同失锁观测。`10.1109.../content.md:110,167,190,206`
- Valjus 给出 timing 与 carrier 的依赖：pilot CPE 要求低 SNR时 timing 仍稳定，否则 pilot位置丢失；结论还说 timing/frame alignment 失败会让 data-aided phase/equalization 失败。可是 timing 仿真排除了 carrier phase noise，且 channel 被当成 quasi-static，不产生同一 fade 事件上的双环状态轨迹。`10.1002.../content.md:149-167,349-353,440,788-790`
- 两篇都不是 Gamma-Gamma dynamic fade；因此“GG fade 同时降低 TED 与 phase detector 可信度，并导致异步共同失锁”仍是未验证机制陈述。

### 3.2 独立 loop + shared freeze + fixed reacquisition 是否已被解决或比较？

**没有。**

- Paillier 只有连续更新 AGC+DPLL，无 timing loop、lock indicator、hold 或 reacquire state。`10.1109.../content.md:114-145`
- Valjus 明确提出 FOE 在信号质量低于阈值时可能应避免更新；另在 equalizer 背景引用低功率停止 tracking，并令 non-differential VV 在 cycle slip 后等待固定 phase reference。这些是三个分散的单子系统做法，不是 timing+carrier shared freeze，也没有与“共同冻结+固定 preamble 重启”比较。`10.1002.../content.md:434-440,548-558,582`
- 因而不能把这些段落拼接后写成“现有文献已解决”或“现有方法已失效”；廉价替代的性能仍未检验。

### 3.3 可量化状态机输出候选是否有文献支撑？

| 候选输出 | 支撑程度 | 正文证据边界 |
|---|---|---|
| carrier lock/pull-in time | 支撑 | Paillier 100 MHz 捕获约 `1.4 ms`，但这是初始 acquisition，不是 post-fade reacquisition `10.1109...:162,186` |
| carrier lock-loss threshold | 支撑 | 无 fade约 `-9 dB`失稳；fade 抬高临界 SNR约 `5 dB` `10.1109...:167,190` |
| phase-error variance/BER | 支撑 | Paillier 给稳态 phase variance 和 BER；Valjus给各算法 SNR penalty `10.1109...:190-200`; `10.1002...:432-448` |
| cycle slip / frame loss | 定性支撑 | Valjus说明错误 phase estimate会产生 cycle slip，直到新 reference；未给可靠 slip probability，且指出软件估计可能过于乐观 `10.1002...:408-440` |
| timing tracking range/SNR penalty | 支撑 | Valjus给 clock ppm、并行/延迟与 SNR penalty曲线 `10.1002...:349-383` |
| lock indicator | 未定义 | 两篇均没有 deployable lock indicator 的公式/阈值/误检漏检指标 |
| hold/update/reacquire 状态序列 | 未定义 | 只有 FOE “低质量不更新”的文字建议；无统一动作标签 `10.1002...:548-558` |
| 双环 post-fade recovery time | 正文未证实 | 无动态 fade 进入/退出轨迹，无 timing+carrier联合恢复实验 |

### 3.4 最强 comparator

当前能从正文合法组装、但**尚未被任一论文作为完整链测试**的最强廉价 comparator 是：

1. Gardner 或 Godard feedback timing loop（明确冻结 parallelization/loop latency/插值器）；
2. Paillier 式 AGC+DPLL，或 Valjus 的 blind FOE + VV/pilot CPE；
3. 同一个 receiver-visible power/normalized-error threshold 同时冻结两个传统 loop；
4. fade 后按固定 receiver-known preamble/reference 周期重启 timing fine tracking 与 FOE/CPE。

这只能称“必须实现并检验的 comparator contract”，不能称已有文献 baseline 的已测性能。Gu 2019 是 2019+ FSO timing baseline，Paillier 2020 是 carrier/fade baseline，Valjus 2025 是 OSL任务匹配综述；但没有一篇 2019+全文对上述 integrated maintenance/reacquisition chain 做对照。

### 3.5 Q2 M-C-A 与 canonical 四判据

| 字段 | Step 3 事实状态 |
|---|---|
| M | Gardner/Gu timing loop 与 AGC+DPLL/VV/FOE carrier loop独立运行；廉价增强为共同阈值冻结+固定 preamble/reference重启 |
| C | ≥2-sps RRC coherent OSL，持续 SCO/drift、CFO/Wiener PN，并经历 dynamic deep fade；本组正文没有 Gamma-Gamma dynamic trace |
| A | fade 同时污染 TED/carrier detector，独立积分器会积错并共同/异步失锁，且廉价 shared freeze+fixed reacquisition仍不足 |
| 判据 1 具体矛盾 | ❌：timing与carrier分别受低 SNR影响有证据，但“共同失锁”及廉价替代仍不足的关键 A 正文未证实 |
| 判据 2 方法产出形态 | ✅（形态层）：共同置信度驱动的 timing/carrier update/hold/reacquire有限状态机、lock indicator与恢复准则可形成可复用算法/设计规则；此项不代表有效性已证实 |
| 判据 3 2019+ task-matched baseline | ❌：Gu 2019、Paillier 2020、Valjus 2025分别覆盖 timing 或 carrier/综述；没有 2019+ integrated joint-maintenance comparator。不能把跨论文串联当作已验证 task-matched baseline |
| 判据 4 可量化对标 | ✅（测量形态层）：可用 timing error/SCO error、carrier phase/frequency error、cycle slip、BER、lock-loss rate与post-fade recovery time；但本组仅前几项有单环数据，联合 recovery 尚无数据 |
| 四判据 | **未全过（1、3未满足）**。这只是 Step 3证据状态，不是 Go/Kill、METHOD_SIGNAL、新颖性闭合或 Step 4a结论 |

## 4. 供 Step 3.5 的本地引用链种子与关键词（只列，不检索）

### 4.1 引用链种子

- Gu et al. 2019, *All-Digital Timing Recovery for Free Space Optical Communication Signals With a Large Dynamic Range and Low OSNR*, IEEE Photonics Journal 11(6)：2019+ FSO timing/低 OSNR 直接种子。`papers/doi/10.1002_sat.1553/content.md:1019`
- Valjus & Wolf 2023, *Comparison of Timing Recovery Algorithms for Optical Feeder Links*：OSL timing、fade/并行延迟直接种子。`content.md:1140`
- Paillier et al. 2020：carrier DPLL/fade/critical-SNR 与 1.4 ms 捕获直接种子。`papers/doi/10.1109_jlt.2020.3003561/content.md:160-206`
- Matsuda et al. 2020, *FPGA Implementation of Scintillation Tolerant Adaptive DSP for 4 Gbps Coherent Reception*：低功率停止 tracking 的相邻子系统种子；动作在 equalizer，不得冒充 timing/carrier竞品。`papers/doi/10.1002_sat.1553/content.md:582,1430`
- Martins et al. 2021, *Hardware Optimization of Dual-Stage Carrier-Phase Recovery for Coherent Optical Receivers*：pilot+blind dual-stage CPE 与硬件链种子。`content.md:1261`
- Vieira et al. 2023, *Modulation and Signal Processing for LEO-LEO Optical Inter-Satellite Links*：Doppler drift/FOE maintenance参数种子。`content.md:1373`

### 4.2 关键词

- `coherent free-space optical timing recovery loss of lock scintillation low OSNR`
- `optical feeder link clock recovery fade reacquisition sampling clock offset`
- `joint timing carrier synchronization fade hold update reacquire state machine`
- `cycle slip detector lock indicator coherent optical deep fade`
- `shared freeze timing NCO carrier loop power threshold preamble reacquisition`
- `scintillation tolerant DSP clock recovery carrier recovery FPGA`
- `post-fade recovery time timing carrier coherent optical satellite`
- `Gamma-Gamma dynamic fading synchronization loop stability SCO`

## 5. 最小事实结论

本组最强事实不是“联合状态机有效”，而是：**Valjus 2025 已明确建立 timing稳定性对 pilot-based carrier处理的依赖，并分别提出 fade 中 FOE停止更新；Paillier 2020则量化了 carrier DPLL 的 fade失稳门限与捕获时间。然而两篇都没有动态联合链实验，所以共同失锁、shared freeze的不足和post-fade双环重捕获仍全部未被正文证实。**
