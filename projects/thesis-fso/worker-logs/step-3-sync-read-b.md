# GW Step 3 精读 B：Q1 近邻与系统链 CORE

> 日期：2026-08-06
> 范围：仅事实提取；不作 Go、METHOD_SIGNAL、新颖性闭合或 Step 4a 判断。
> 行号口径：均指 canonical `papers/.../content.md`。三篇实际全文读取自共享主根 `D:/code/study/research-protocol/papers/`。

## 身份与 title-abort 结果

| 论文 | metadata title_check | 正文首个有效标题 | 结果 | 证据 |
|---|---|---|---|---|
| Wang et al., 2023, *Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication* | `unverifiable` | 与派遣标题逐字一致 | **PASS** | `papers/doi/10.1109_jphot.2023.3265847/content.md:11,75-83` |
| Wang et al., 2024, *Enhanced frame synchronization and carrier recovery in coherent FSO communication: a pseudo-random and cyclic QPSK approach* | `unverifiable` | 与派遣标题逐字一致 | **PASS** | `papers/doi/10.1364_oe.520452/content.md:5-16,53` |
| Le Bidan et al., 2023, *Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link* | `match`（0.6667） | 与派遣标题一致 | **PASS** | `papers/doi/10.1109_icsos59710.2023.10490279/content.md:1-6,22-40` |

## 1. Wang et al. 2023 — FSTS

### 1.1 标准条目（14+ 字段）

- **DOI/来源**：10.1109/JPHOT.2023.3265847。
- **源文件路径**：`papers/doi/10.1109_jphot.2023.3265847/content.md`。
- **发表状态**：正式发表。
- **发表渠道**：IEEE Photonics Journal, Vol. 15, No. 3。
- **年份**：2023。
- **核心贡献**：设计双偏振互异、前后共轭对称的 frame-synchronous training sequence（FSTS），先以 Park 型 timing metric 做符号级帧头定位和多分支对齐，再在 MRC、偏振解复用后复用同一 TS 做两级 FOE。两级 FOE 分别利用跨偏振相邻同符号共轭积与相隔块共轭积，目标是兼顾估计范围、精度和复杂度（`content.md:101-119,175-208`）。
- **方法概述**：FS 在各分支上先运行；分支相位校正/MRC、偏振解复用后，粗 FOE 与细 FOE 顺序运行，最终把两级频偏估计相加并补偿整个训练周期（`content.md:119-152,185-214,243`）。
- **receiver-visible information**：接收复采样值、已知 FSTS 结构、双偏振共同 LO、各分支 timing metric；不需要 payload truth。论文称其 FS 不需在接收端备份原 TS，但训练结构本身是预先设计的（`content.md:103-107,142,219-225`）。
- **action**：阈值/峰值式符号起点选择；多分支相对延迟移除；粗频偏估计与细频偏估计；对训练周期作频偏补偿（`content.md:119-152,175-214`）。
- **output**：每分支帧起点、合并前对齐状态、标量 CFO 估计与 CFO-corrected sequence（`content.md:119-152,208-214`）。
- **sample rate / 时序**：FOE 明示 **1 sample/symbol**；因此这里的 FS 是符号起点定位，不是 2-sps 分数定时动作。顺序为 IQ imbalance recovery → FS → branch phase correction → MRC → polarization demultiplexing → FOE → phase-noise estimation（`content.md:183,231-243`）。
- **实验设置**：10 GBaud PM 4/16-QAM；B2B 与 10 km 相位屏 FSO；单分支及 2/4/6 分支 MRC；训练长度 48–960，重点为 320/960（`content.md:231-243,247-267,289-299,339-375`）。
- **Baseline**：4th-power/QPSK partition、4th-FFT、conventional TS FOE；FS/FOE 总复杂度还与 2020 年 training-aided joint frame/frequency synchronization [19] 比较（`content.md:97-101,217-229,289-309`）。
- **关键结论**：320-symbol FSTS 在多种湍流/分支设置下可达到 conventional TS 960-symbol 的相近或更好 BER；同为 320 symbols 时报告 0.7–3.41 dB 不等的接收灵敏度改善，且最优复杂度口径下降约 75%（`content.md:339-385`）。
- **与 Q1 关系**：是低成本 frame+FOE 顺序 comparator；但不包含 fractional timing/SCO action，不能冒充 sample-level 联合获取链。
- **实现关键细节**：320-symbol 设计时 4-QAM 取 `BN=16, BL=20`，16-QAM 取 `BN=8, BL=40`；FS threshold 0.2/0.3；CFO 在 ±1.1 GHz 内随机（`content.md:257-267,289-299,319,339`）。
- **开源代码**：正文未报告。
- **验证状态**：已逐行读取全文；身份 PASS。

### 1.2 七子表

#### 状态 / 输入

| 状态或输入 | 范围/取值 | 预处理/归一化 | 证据 |
|---|---|---|---|
| 双偏振、多分支复样值 | PM 4/16-QAM；1 sps FOE | coherent front-end；IQ imbalance recovery | `content.md:152-183,231-243` |
| FSTS | 320 或 960 symbols 等；双偏振交错/共轭结构 | timing metric 以接收能量平方归一化 | `content.md:103-142,247-267` |
| CFO | 测试随机值 ±1.1 GHz | 归一化 MSE 使用 `Δf·Ts` | `content.md:279-289,319` |

#### 动作

| 类型 | 维度 | 合法动作约束 | 证据 |
|---|---|---|---|
| 离散定位 | 每分支一个符号索引 | metric 超阈值或全窗最大值 | `content.md:119-148` |
| 连续估计/补偿 | 一个共享 CFO 标量 | 粗估范围 1 sps 下理论 ±Rs/2；细估范围缩小 `BL` 倍 | `content.md:175-208` |

#### 目标 / 奖励

| 项 | 内容 | 说明 |
|---|---|---|
| 优化目标 | FS accuracy、normalized CFO MSE、BER/receiver sensitivity、real-multiplication complexity | 确定性 DSP，不是学习算法 |
| 奖励函数 | N/A | 无训练、无 reward；用上述指标直接评价（`content.md:217-225,257-279`） |

#### 建模假设

| 假设 | 位置 | 对复现/适配的影响 |
|---|---|---|
| 两偏振 CFO 相同且各分支共享 LO | §II-A/B | 允许跨偏振联合 FOE、合并后统一补偿（`content.md:103-105,243`） |
| 激光/湍流相位相对 GHz 符号率慢变 | Eq. (3)–(7) | 相邻符号共轭积可消去其影响（`content.md:152-183`） |
| FS 已准确给出 TS 起点后才做 FOE | §II-B | frame 与 FOE 是复用 TS 的顺序模块，不是同一优化动作（`content.md:119-152`） |
| 相位屏：outer scale→∞、inner scale→0 | §III | 属理想化 Kolmogorov 相位屏边界（`content.md:241`） |

#### 网络架构

| 项 | 结果 | 原因 |
|---|---|---|
| 网络层/激活/优化器 | N/A | 全部为解析 feed-forward DSP，无神经网络或训练过程 |

#### 适配性

| 适配点 | 不适配点 | 可供后续核查的方向（非建议/非 Go） |
|---|---|---|
| receiver-known TS；frame+FOE 复用；明确复杂度口径 | 1 sps；无 fractional timing、SCO/drift；FS 与 FOE 顺序执行 | 检查将独立 2-sps timing 前置后，FSTS 是否已构成廉价完整 comparator |

#### M-C-A + 四判据

| M | C | A | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 证据 |
|---|---|---|---|---|---|---|---|---|
| conventional TS FOE / Cheng 2020 training-aided joint FS+FOE | 短训练、低接收功率、PM coherent FSO | TS 长度决定精度/开销，短序列下 joint FS+FOE 性能不足 | FSTS 结构、阈值 FS、两级 FOE 算法 | ✅ M/C/A 明确 | ✅ 可复用算法 | ✅ Cheng 2020 为 2019+ task-matched；本文自身为 2023 comparator | ✅ FS accuracy、MSE、BER、复杂度均可量化 | `content.md:97-101,217-229,257-339` |

### 1.3 信道模型参数

| 链路类型 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| B2B coherent | AWGN/shot/thermal + laser phase noise | 10 GBaud；ECL/LO linewidth 50 kHz；LO 15 dBm；responsivity 0.8 A/W | `content.md:231-243` |
| 10 km FSO | Fourier phase screen | `Cn²=1e-16`（弱）/`1e-14 m^-2/3`（强）；aperture 0.2 m | `content.md:241-243` |
| 耦合/分集 | 独立 fading branches + MRC | 平均耦合效率 67.3012% / 4.8395%；1/2/4/6 branches | `content.md:243,375` |

### 1.4 实验完备性（≤20 行）

- **C1**：FSTS 在保证 FS 的同时提升 FOE 精度/范围并降低复杂度；**C2**：适配多调制与空间分集（bounded simulation claims）。
- **统计规范性**：FS 点 6400 次平均；FOE 点 800 次平均；未见 seed ledger、显著性检验或 error bars（`content.md:257,319`）。
- **Baseline 矩阵**：4 个 FOE 方法；joint-processing complexity 另与 Cheng 2020 比；未声明公平调参。
- **消融/参数扫描**：TS length、`BL/BN`、threshold、branch count、modulation、turbulence 强度均扫描；无严格模块删除消融。
- **信道模型**：相位屏 + shot/thermal noise；参数有文献引用，但 outer/inner scale 极限化。
- **拓扑多样性**：单/2/4/6 分支，弱/强湍流，4/16-QAM。
- **复杂度**：报告实乘/实加解析计数；无实测 latency。
- **VVUQ**：V=2（公式+多维仿真）；V'=1（无实物/外场）；U=2（重复平均但无统计区间）。

## 2. Wang et al. 2024 — PRBS + cyclic-QPSK

### 2.1 标准条目（14+ 字段）

- **DOI/来源**：10.1364/OE.520452。
- **源文件路径**：`papers/doi/10.1364_oe.520452/content.md`。
- **发表状态**：正式发表。
- **发表渠道**：Optics Express 32(15), 25560–25580。
- **年份**：2024。
- **核心贡献**：构造 PRBS 前缀 + 周期 QPSK 后缀的混合 TS；PRBS differential metric 负责 frame synchronization，周期 QPSK 的谱峰和跨偏振块共轭处理负责粗/细 FOE。论文还扫描 QPSK 长度与内部 block 长度，给出低开销工作点（`content.md:165-181,185-205,251-325`）。
- **方法概述**：先在下采样后的每分支数据上以接收端保存的 differential PRBS 查帧；帧同步完成后截取 QPSK 后缀，以 FFT 谱峰作粗 FOE，再用跨偏振、跨 block 共轭差分作细 FOE（`content.md:205-253,262-312,345`）。
- **receiver-visible information**：接收复样值、接收端预存 differential PRBS、已知周期 QPSK 结构、双偏振信号；不使用 payload truth（`content.md:231-249,253-268`）。
- **action**：每分支 frame-start peak search；粗 CFO estimate；fine residual CFO estimate；CFO compensation（`content.md:207-253,262-312`）。
- **output**：分支帧起点、粗/细/总 CFO 标量、CFO-corrected samples（`content.md:249-253,294-312`）。
- **sample rate / 时序**：发端 QPSK-TS 的谱构造提到 2×上采样，但接收端 **ADC 后先下采样**，且粗 FOE 明示采样率等于 `Rs`；所以 frame/FOE action 仍是 symbol-rate/downsampled action，不是 2-sps fractional timing（`content.md:189,262-272,334-345`）。
- **实验设置**：20 km、10 G polarization-multiplexed QAM，多分支 phase-screen simulation；另有室内单孔径 QPSK 弱湍流演示（`content.md:334-345,442-493`）。
- **Baseline**：Park frame metric、weighted Park、traditional TS FOE、4th-power、4th-FFT、Wu et al. 2022 QPSK-TS scheme（`content.md:171-181,321-325,349-442`）。
- **关键结论**：frame metric 在部分接收功率下用约少 100 symbols 达到相当精度；FOE 480 symbols 已趋于饱和，较 960 symbols 仅约 0.3 dBm 差异；强湍流时报告相对 TS/FFT 的 1.78/2.46 dBm 等灵敏度差异（`content.md:323-325,349-364,393-464`）。
- **与 Q1 关系**：是 2024 年 frame+FOE 近邻，且比 FSTS 更接近混合 preamble 设计；仍未执行 sample-level fractional timing/SCO。
- **实现关键细节**：QPSK period 16；粗估范围 ±3Rs/8；总 TS 480/960；block length 超过约 50–80 后细估 MSE 稳定在约 1e-9；simulation 每点 800 次（`content.md:189,262-306,393-431`）。
- **开源代码/数据**：代码未报告；数据可向作者索取，未公开（`content.md:503-505`）。
- **验证状态**：已逐行读取全文；身份 PASS。

### 2.2 七子表

#### 状态 / 输入

| 状态或输入 | 范围/取值 | 预处理/归一化 | 证据 |
|---|---|---|---|
| 多分支双偏振接收值 | QPSK/16QAM；接收端先下采样 | 分支 phase precorrection 后 MRC | `content.md:334-345` |
| PRBS + cyclic-QPSK TS | PRBS 用于 FS；QPSK 用于 coarse/fine FOE | timing metric 用 N-symbol energy normalization | `content.md:205-249` |
| CFO | 粗估理论 ±3Rs/8 | normalized MSE | `content.md:262-272,369-375` |

#### 动作

| 类型 | 维度 | 合法动作约束 | 证据 |
|---|---|---|---|
| 离散定位 | 每分支符号索引 | differential PRBS metric peak | `content.md:207-249` |
| 连续估计/补偿 | 一个 CFO 标量 | coarse FFT peak 后 fine block differential | `content.md:251-312` |

#### 目标 / 奖励

| 项 | 内容 | 说明 |
|---|---|---|
| 目标 | FS accuracy/peak distinctness、CFO MSE/range、BER/sensitivity、resource count | 解析 DSP |
| 奖励 | N/A | 无学习训练或 reward（`content.md:321-325,347-375`） |

#### 建模假设

| 假设 | 位置 | 影响 |
|---|---|---|
| 两偏振承载可用于交叉处理的共同 CFO 信息 | §2.3 | 支撑跨偏振 fine FOE（`content.md:283-306`） |
| 邻近/相隔短 block 的激光与湍流相位慢变 | §2.2–2.3 | 允许差分/共轭抵消（`content.md:231-245,283`） |
| frame sync 已完成后才截取 QPSK 做 FOE | §2.3 | 明确是顺序链（`content.md:251-253`） |
| 接收端下采样后进入后续算法 | §3 | 排除 sample-level fractional timing action（`content.md:345`） |

#### 网络架构

| 项 | 结果 | 原因 |
|---|---|---|
| 网络层/激活/优化器 | N/A | 无神经网络；解析相关/FFT/共轭积 DSP |

#### 适配性

| 适配点 | 不适配点 | 可供后续核查的方向（非建议/非 Go） |
|---|---|---|
| 2024 近邻；混合 preamble；明确 overhead/complexity | 接收端已下采样；无 SCO/drift；indoor test 几乎 B2B | 与独立 2-sps timing 前端串接后，检查剩余 delta 是否仅模块拼接/排序 |

#### M-C-A + 四判据

| M | C | A | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 证据 |
|---|---|---|---|---|---|---|---|---|
| Park-type FS + Wu 2022 QPSK-TS FOE | 低接收功率、短 training、turbulent PM coherent FSO | Park side peaks、既有 QPSK-TS 未评估序列长度且 second-stage FFT 复杂 | 混合 TS、differential FS、两级 FOE | ✅ | ✅ 可复用序列与算法 | ✅ Wu 2022 为 2019+ task-matched；本文 2024 | ✅ FS accuracy、MSE、sensitivity、complexity | `content.md:171-181,321-325,349-464` |

### 2.3 信道模型参数

| 链路类型 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| 模拟 FSO | 多相位屏；耦合效率 non-central chi-square；相位噪声 normal | 20 km；aperture 0.2 m；10 G PM-QAM；laser linewidth 80 kHz | `content.md:334-345` |
| 湍流仿真 | 弱/强结构常数 | `1e-16` / `1e-14`（正文未在该处完整给单位） | `content.md:442-455` |
| 室内演示 | 单孔径 QPSK 弱湍流 | Tx 13 dBm；作者报结构常数 `6e-11`；Rx sampling 40 G；MATLAB offline | `content.md:466-493` |

### 2.4 实验完备性（≤20 行）

- **C1**：约省 100 FS symbols；**C2**：480-symbol FOE 兼顾精度/复杂度；**C3**：多格式/湍流适配（均为 bounded claim）。
- **统计规范性**：FS 点 3200 次；多数 FOE/BER 点 800 次；Fig. 12 有 error bar/标准差；无统计检验（`content.md:349-351,393-404,431`）。
- **Baseline 矩阵**：Park/weighted Park + TS/4th-power/4th-FFT/Wu 2022；调参公平性说明有限。
- **消融/参数扫描**：PRBS/QPSK length、内部 block、modulation、branch count、turbulence；无严格模块 deletion。
- **信道模型**：相位屏与分布假设有来源；实物验证仅弱湍流单孔径且近 B2B。
- **拓扑多样性**：single/four branch，弱/强湍流，QPSK/16QAM；实验只覆盖单孔径 QPSK。
- **复杂度**：实乘数量/资源节省；无硬件 latency/FLOPs。
- **VVUQ**：V=2；V'=2（有室内演示但条件有限）；U=2（重复与一处 error bar）。

### 2.5 写作架构提取

- **章节结构**：Introduction → Operation principle（TS/FS/FOE/complexity）→ Simulation settings → Simulation results（FS/FOE/experiment）→ Summary（`content.md:142-154,185-185,334-347,495-497`）。
- **论证模式**：先把 FS side-peak、TS length/overhead、second-stage FFT complexity 分成三个具体缺陷，再让一个混合 TS 分别承担对应动作；结果按“先单指标、再端到端 BER、最后室内图”递进。
- **参数展示**：关键长度/范围散在正文与曲线中；复杂度和 timing metric 用 2 个表；页面索引列 20 figures、2 tables、21 equations（`content.md:623-684,808-866`）。
- **实验组织**：先 B2B 建立 MSE↔BER 阈值，再扫描 sequence/block length 和 CFO range，最后进入弱/强湍流与分支数，形成从 estimator 到 system BER 的证据链（`content.md:369-464`）。
- **引言/结尾写法**：引言按传统方法分族并逐项暴露边界；结尾只回收 frame-symbol saving、FEC threshold 下 FOE 对比与多格式适配，没有新增论点（`content.md:171-183,495-497`）。

## 3. Le Bidan et al. 2023 — 56-GBaud GEO DSP chain

### 3.1 标准条目（14+ 字段）

- **DOI/来源**：10.1109/ICSOS59710.2023.10490279（正文 HAL 引文区出现错误的 Springer DOI 字样，不采用；身份以 metadata/题名/会议记录为准）。
- **源文件路径**：`papers/doi/10.1109_icsos59710.2023.10490279/content.md`。
- **发表状态**：正式会议论文。
- **发表渠道**：IEEE ICSOS 2023。
- **年份**：2023。
- **核心贡献**：为 56-GBaud GEO DP-QPSK feeder link 共同设计 3.6–4.8% overhead frame 与低时延 feed-forward DSP receiver；前端在 2 sps 下依次完成 coarse CFO、matched filtering、Lee blind timing recovery 与 fractionally-spaced equalization，随后在 1 sps 下做 frame acquisition、data-aided fine CFO 与 pilot-aided CPE（`content.md:40-51,310-370,420-480,629-704`）。
- **方法概述**：启动阶段先盲初始化/训练 coarse CFO、timing、adaptive equalizer，随后 frame acquisition；steady state 中 frame header 每帧支持 Mengali-Morelli fine CFO，pilot blocks 支持相位跟踪（`content.md:358-387,629-704`）。
- **receiver-visible information**：启动盲算法只用接收双偏振 samples；frame/fine CFO 使用已知 64-symbol distinct headers；CPE 使用每 248 payload 后的 8 pilots（`content.md:310-348,358-370,619-704`）。
- **action**：六候选 coarse CFO 旋转择能量；matched filter；每 5000-symbol block 的 Lee timing-offset estimate + digital interpolation；2×2 scalar + two fractionally-spaced filters 的 CMA equalization；双偏振独立 header search；每帧 fine CFO；pilot phase interpolation（`content.md:420-579,607-704`）。
- **output**：coarse CFO bin、symbol-epoch corrected 2-sps stream、1-sps polarization-demultiplexed symbols、frame starts、per-frame fine CFO、pilot-interpolated carrier phase、soft LLR（`content.md:469-579,629-708`）。
- **sample rate / 时序**：架构显式区分 2 sps、1 sps、bit-rate；coarse CFO 和 timing 位于 2-sps sample-rate path，timing 用数字插值后才 downsample 到 1 sps；FSE 还吸收 residual fractional delay，之后 frame search 仅处理可能残留的双偏振**整数符号**延迟（`content.md:358-370,420-480,559-579`）。
- **实验设置**：56 GBaud DP-QPSK、RRC roll-off 0.1、最低 -6 dB Es/N0、CFO ±5 GHz、clock drift ±30 ppm、laser linewidth 600 kHz、PDL 5 dB、X-Y skew 0.25 ns；无显式 turbulence trajectory（`content.md:172-205,216-242,245-261`）。
- **Baseline**：DVB-S2/S2X 与 OIF 400ZR 作 frame/receiver system anchors；各 stage 采用 Mengali NDA CFO、Lee timing、modified CMA、Lee 2009 differential frame sync、Mengali-Morelli fine CFO；CPE 比较 VV/BPS 后选择 pilot ML（`content.md:274-308,420-480,559-704`）。
- **关键结论**：仿真在 -6 dB 与现实 impairment 下以 <5% overhead 获取/锁定；初始化+锁定通常 <100 μs；frame acquisition 在 -6 dB/5 dB PDL 下 <50 μs。作者同时指出 fine CFR 在负 SNR 会因 residual CFO 恶化性能，深衰落的 stay-locked/reacquisition 仍未解决（`content.md:380-387,612-649,729-771,779-801`）。
- **与 Q1 关系**：给出真正可复用的 2-sps fractional timing + frame + CFO 完整顺序 comparator；但没有把三者变成一个 joint estimator/action。
- **实现关键细节**：coarse CFO `M=6`, `{±0.025, ±0.075, ±0.125}Rs`, `N0=4096 samples`；Lee timing block ≥5000 symbols；CMA 16 taps、每 32 symbols 更新，training/tracking step `1e-3/5e-4`, `λ=0.7`；header `H=64`, correlation order 32（`content.md:436-469,559-618`）。
- **开源代码**：正文未报告。
- **验证状态**：已逐行读取全文；身份 PASS；OCR 中混入 handbook 文本，但核心论文段落和公式可定位。

### 3.2 七子表

#### 状态 / 输入

| 状态或输入 | 范围/取值 | 预处理/归一化 | 证据 |
|---|---|---|---|
| 2-sps DP-QPSK samples | 56 GBaud；RRC α=0.1 | coarse CFO pre-rotation、matched filtering | `content.md:245-261,358-370,420-472` |
| timing state | fractional sampling epoch + clock drift ±30 ppm | block-average Lee NDA estimator | `content.md:196,420-480` |
| header/pilot | H=64；8 pilots/248 payload | 双偏振 distinct sequences | `content.md:310-348` |

#### 动作

| 类型 | 维度 | 合法动作约束 | 证据 |
|---|---|---|---|
| 离散 CFO bank | 6 hypotheses | 共享双偏振能量最大者 | `content.md:436-469` |
| 连续 timing | 每偏振一个 block offset | 2 sps digital interpolation；之后 downsample | `content.md:420-480` |
| adaptive FSE | 2 scalar + 2×16-tap filters | CMA unitary regularization | `content.md:559-579` |
| frame/fine CFO/CPE | header indices + per-frame CFO + phase trajectory | frame after timing/FSE；CPE pilot-aided | `content.md:579-704` |

#### 目标 / 奖励

| 项 | 内容 | 说明 |
|---|---|---|
| 目标 | acquisition/lock time、MSE、BER、GMI、overhead、hardware simplicity | feed-forward receiver design |
| 奖励 | N/A | 无 RL；CMA 有解析 cost `J`，但不是 reward（`content.md:577-603,714-732`） |

#### 建模假设

| 假设 | 位置 | 影响 |
|---|---|---|
| turbulence 慢于 frame，且不能由 DSP 单独补偿 | §II-A | 未显式模拟 fades/trajectory；只把 margin 折入最低 SNR（`content.md:172-184,231-242`） |
| CFO 对两偏振相同 | coarse/fine CFO | 可合并双偏振能量/相关提高精度（`content.md:442-450,642-649`） |
| 2 sps feed-forward Lee timing 足以处理 ±30 ppm | timing recovery | 5000-symbol block 对应约 `BLTs≈1e-4`；未加 ADC feedback loop（`content.md:428-448,779-792`） |
| FSE 已处理 fractional delay | frame sync | frame header search 只需处理 polarization integer-symbol skew（`content.md:559-579`） |

#### 网络架构

| 项 | 结果 | 原因 |
|---|---|---|
| 神经网络 | N/A | 无 NN；“architecture”指 DSP pipeline |
| 自适应模块 | 16-tap block CMA FSE | SGD，`μ=1e-3/5e-4`, `λ=0.7`（`content.md:559-603`） |

#### 适配性

| 适配点 | 不适配点 | 可供后续核查的方向（非建议/非 Go） |
|---|---|---|
| 真实 2 sps、fractional timing、SCO、frame、CFO、低 SNR；模块顺序明确 | 无 turbulence/fade trajectory；不是 joint action；timing window 很长 | 作为“独立 timing + frame/CFO”廉价系统 comparator，检查联合化是否有超出重排的可量化 failure |

#### M-C-A + 四判据

| M | C | A | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 证据 |
|---|---|---|---|---|---|---|---|---|
| COTS coherent-fiber 400ZR receiver / DVB-S2 frame chain | -6 dB GEO DP-QPSK、2 sps、±5 GHz CFO、±30 ppm SCO、600 kHz PN | 高-SNR/fiber impairment assumptions and RF-only framing do not meet low-SNR coherent GEO acquisition | custom frame + ordered feed-forward receiver | ✅ | ✅ 可复用 frame/pipeline | ❌ 400ZR 2020 是近期 system anchor，但未给出 2019+、同任务低-SNR GEO end-to-end comparator | ✅ lock time、BER/GMI、overhead | `content.md:85-107,245-308,714-801` |

### 3.3 信道模型参数

| 链路类型 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| GEO coherent feeder | oversampled discrete-time DP-QPSK | 56 GBaud；2 sps；RRC α=0.1；Es/N0 ≥ -6 dB | `content.md:172-205,245-261` |
| oscillator/noise | Wiener PN + white Gaussian ASE | cumulative linewidth 600 kHz；CFO ±5 GHz | `content.md:172-205` |
| front-end/polarization | PDL + SOP + skew + clock drift | PDL 5 dB；X-Y skew 0.25 ns；clock drift ±30 ppm | `content.md:188-225` |
| atmosphere | 不显式模拟 | scintillation/fades 仅通过 SNR margin/FEC-interleaving 语境处理 | `content.md:172-184,231-242` |

### 3.4 实验完备性（≤20 行）

- **C1**：-6 dB 下可建立 GEO link；**C2**：overhead <5%；**C3**：简化 blind equalizer/ordered DSP 具硬件可行性（bounded simulation/proof-of-concept）。
- **统计规范性**：每 SNR 400 training frames + 最多 300 acquisition frames + 512 evaluation frames；无 seeds/error bars/检验（`content.md:729-732`）。
- **Baseline 矩阵**：以 DVB-S2/400ZR 作设计比较，但结果图主要是 receiver stages on/off，不是完整 end-to-end baseline 对比。
- **消融设计**：不同 impairments 与 receiver stages enabled/disabled；较接近模块消融（`content.md:714-749`）。
- **信道模型**：Wiener PN、ASE、PDL/SOP/skew/SCO；turbulence 未显式模拟。
- **拓扑多样性**：单 GEO system configuration，多 impairment combinations；无多链路/多湍流轨迹。
- **复杂度**：强调 feed-forward/parallel/简化 FSE，给 lock latency；无统一 O()/FLOPs。
- **VVUQ**：V=2；V'=1（无硬件/外场）；U=1（固定大样本但无不确定性量化）。

### 3.5 写作架构提取

- **章节结构**：Introduction → Link model and requirements → DSP frame/receiver architecture → DSP algorithms（按处理顺序）→ performance → Summary（`content.md:59-124,188-274,310-373,779-801`）。
- **叙述模式**：以明确工程需求表（SNR/CFO/SCO/PDL/skew/overhead/sps）约束方案，再比较 RF 与 fiber 两套成熟架构，最后按 receiver dataflow 逐模块解释取舍。
- **参数展示**：frame 参数集中成 `H/D/P` 并直接算 3.6% overhead；算法参数紧贴模块；结果用 GMI/BER 与 stages-on/off 图（`content.md:310-352,607-732`）。
- **公式使用**：少量关键 cost/参数公式，重心是 block diagram、frame format、processing order，适合系统设计论文而非 estimator 推导论文。
- **结尾写法**：先收束可达边界，再明确 proof-of-concept 改进项（pilot-refined CFO、ADC feedback、phase tracking）和 turbulence/deep-fade 未覆盖边界（`content.md:764-801`）。

## 4. 三篇综合

### 4.1 五维 collision 表

| 论文 | receiver-visible information | action | output | sample rate / processing order | Q1 collision 边界 |
|---|---|---|---|---|---|
| Wang 2023 FSTS | known FSTS structure + received dual-pol/branches | symbol-start FS；branch alignment；coarse+fine CFO | start index + CFO | **1 sps**；FS → MRC/pol-demux → FOE | 碰撞 frame+FOE preamble reuse；**不碰撞 fractional timing/SCO** |
| Wang 2024 mixed TS | stored differential PRBS + cyclic QPSK + dual-pol received data | frame peak；FFT coarse FOE；block fine FOE | start index + CFO | Tx 谱分析用 2×upsampling；Rx **先 downsample，FOE=Rs**；FS → FOE | 碰撞 mixed-preamble frame+FOE；**不碰撞 sample-level timing** |
| Le Bidan 2023 GEO | blind 2-sps samples + known headers/pilots | CFO bank；Lee timing+interpolation；FSE；header search；fine CFO；CPE | corrected 1-sps symbols + frame/CFO/phase | **2 sps coarse CFO → MF → timing → FSE/downsample → frame → fine CFO → CPE** | 碰撞完整 ordered chain；不碰撞单一 joint estimator/action |

证据：Wang 2023 `content.md:119-183,231-243`；Wang 2024 `content.md:251-272,334-345`；GEO 2023 `content.md:358-480,559-704`。

### 4.2 FSTS/STSB + 独立 timing comparator 证据

1. **FSTS 已有强事实证据**：Wang 2023 给出 1-sps frame + two-stage FOE、TS-length/threshold/complexity/BER 全套可复现 comparator，并且 Cheng 2020 已是 task-matched joint FS+FOE 对手（`Wang 2023 content.md:97-101,117-225,257-385`）。
2. **独立 timing 已有强事实证据**：GEO 2023 在 2 sps 下用 Lee estimator 每 ≥5000 symbols 估 sampling epoch，通过 digital interpolation 校正 SCO/fractional timing；FSE 进一步合成最佳 sampling epoch，随后才进入 frame/fine CFO（`GEO 2023 content.md:420-480,559-579`）。
3. **组合后的廉价 comparator 形态**（事实拼接，不声称论文已实现）：`coarse CFO bank → matched filter → Lee timing/interpolation → FSE/downsample → FSTS/mixed-TS frame+FOE`。两端的 receiver-visible information 都是合法接收信号/known training，不需 payload truth。
4. **STSB 证据上限**：本组三篇正文不含 STSB 方法全文；仅 Wang 2023 页面 related-item 出现题名 *Optimized Frequency Offset Estimation Scheme Using Short Symbol Block...*，没有方法/参数/结果正文，故 **不能**把 STSB 计入已核验 comparator，只能列为 Step 3.5 补全文对象（`Wang 2023 content.md:401-405`）。

### 4.3 GEO sample-rate 与 processing order（权威摘录）

```text
2-sps ADC samples
  → coarse CFO hypothesis bank (M=6, N0=4096)
  → matched filter
  → per-polarization Lee timing estimator (block ≥5000) + digital interpolation
  → simplified CMA fractionally-spaced equalizer; synthesize optimum epoch
  → downsample to 1 sps
  → parallel X/Y header search; resolve integer-symbol skew/polarization ambiguity
  → joint dual-pol Mengali–Morelli fine CFO, once/frame + smoothing
  → pilot-ML CPE + interpolation
  → soft detection
```

证据：`GEO 2023 content.md:358-370,420-480,559-579,629-708`。

### 4.4 Q1 剩余 delta：联合动作还是顺序调整

- **全文事实**：两个 Wang 方案已经覆盖“同一/混合 preamble 支撑 frame + CFO”，GEO 方案已经覆盖“2-sps fractional timing/SCO + frame + CFO”的完整 receiver chain。
- **尚未在三篇中出现的动作形态**：同一 sample-level objective/estimator 同时输出 fractional timing、frame start 与 CFO，或利用三者耦合产生不同于串接模块的闭环/联合更新。
- **因此当前证据能支持的最窄表述**：若 Q1 只是把 Lee timing/FSE 放到 FSTS/STSB 前面，或交换既有模块顺序，它是 **ordered-chain composition / implementation reordering**；不能仅凭“统一画在一个框里”称 joint action。要把 delta 记为联合动作，后续证据必须指出串接 comparator 的具体 failure condition，并给出 joint estimator 对相同输入产生不可由顺序模块复现的输出或量化改善。
- **未闭合项**：本组没有 fractional timing distribution、sample-clock/frame/CFO coupling failure 的量化曲线；STSB 全文缺失；因此不作 novelty closure。

### 4.5 供 Step 3.5 的共同引用与关键词

| 类型 | 条目 | 本组角色/证据 |
|---|---|---|
| 共同/邻近引用 | Park et al., 2003 timing metric | Wang 2023/2024 的 FS 起点；side-peak/plateau comparator（Wang 2024 `content.md:171-177,547-549`） |
| 近期 task-matched | Cheng et al., 2020, training-aided joint frame and frequency synchronization | Wang 2023 指出 short training 下不足；Wang 2024 refs 给 DOI（`Wang 2023 content.md:99`; Wang 2024 `content.md:577-579`） |
| 近期 FOE | Wu et al., 2022, QPSK-TS joint OSNR/FO monitoring | Wang 2024 coarse/fine FOE 直接 comparator（`content.md:179-181,585-587`） |
| 2-sps timing | S. J. Lee 2002；Wang/Serpedin/Ciblat 2003 | GEO 2-sps feed-forward timing 与 unbiased variant（`GEO content.md:432-448,842-847`） |
| frame at low SNR | D.-U. Lee et al., 2009 energy-corrected differential correlation | GEO frame header search（`GEO content.md:571-618,856-858`） |
| fine CFO | Mengali & Morelli 1997 | GEO header-reusing per-frame CFO（`GEO content.md:629-652,859-861`） |
| system anchor | OIF 400ZR 2020 + DVB-S2/S2X | 2-sps coherent/RF framing comparison，不是同任务低-SNR baseline（`GEO content.md:274-308,837-839`） |
| 待补全文 | *Optimized Frequency Offset Estimation Scheme Using Short Symbol Block Based on Training Sequence for Coherent FSO Communication* | 当前仅 related-item 题名，不能作方法证据（Wang 2023 `content.md:401-405`） |

定向关键词（不等于已执行检索）：

- `"short symbol block" training sequence frequency offset coherent FSO STSB`
- `"two samples per symbol" frame synchronization frequency offset coherent optical preamble`
- `fractionally spaced timing recovery frame acquisition CFO joint estimator coherent optical`
- `sampling clock offset fractional timing frame synchronization CFO low SNR burst coherent`
- `Lee timing estimator FSTS frame synchronous training sequence`
- `energy-corrected differential correlation polyphase timing CFO preamble`

## 5. 本组事实结论（非阶段裁决）

最重要的事实是：**GEO 2023 已给出 2-sps fractional timing/SCO → downsample → frame → fine CFO 的完整廉价顺序链，而 Wang 2023/2024 已给出 receiver-known preamble 的 frame+FOE；所以 Q1 若无“串接链在何种条件下因何假设失效”的量化证据，其剩余 delta 在当前全文证据下只能描述为顺序组合/重排，不能描述为已证实的 sample-level joint action。**
