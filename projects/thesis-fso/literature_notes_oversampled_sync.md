# 过采样相干 FSO 联合同步前端：Groundwork 文献状态

> 2026-08-06 | GW Step 3 canonical 重判、Step 3.5 与用户全文覆盖处置完成 | terminal: `STEP3_5_COMPLETE_Q1_SURVIVOR_JOCN_FULLTEXT_UNAVAILABLE_NO_CONFIRMED_EXACT_COLLISION`

## 边界

用户已接受 7 篇 CORE 覆盖面；D006 已按 canonical owner 完成 Step 3 重判，Q1 四判据 PASS、Q2 仅
判据 3 FAIL；D007 已完成 Step 3.5。当前不声称 exact-action novelty、Step 4a problem truth 或方法
可行性闭合，且本轮不得进入 Step 4a、实现或仿真。

## GW 进度

| Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| Step 1 search | ✅ | `oversampled-sync-groundwork/step1-search-report.md`；6 query，140 raw / 130 unique，2019+ 39 unique | 两张机制不同预卡存活，允许 Step 2 |
| Step 2 acquire | ✅ 用户已确认 | `oversampled-sync-groundwork/step2-coverage-report.md`；7 CORE 全文通过 identity/SHA/≥50 行门 | D004 接受覆盖面 |
| Step 3 read | ✅（D006 纠偏） | `oversampled-sync-groundwork/step3-deep-read-report.md`；7 篇 CORE 结构化全文精读 | Q1 四判据 PASS；Q2 仅判据 3 FAIL |
| Step 3.5 supplement | ✅ / COVERAGE DECISION HANDLED | `step3-5-supplement-report.md`；Round 2 新增 must/should=0；T013 | Q1 保留 survivor；JOCN limitation 保留 |
| Step 4a | ⬜ 未进入 | 下一会话必须重读 `gw-feasibility.md` | 只允许 preflight discussion，不自动授权 |

## CORE 覆盖

| 文献 | 覆盖角色 | 当前边界 |
|---|---|---|
| Tang 2022, `10.1109/JPHOT.2022.3161795` | CFSO 帧定位 + CFO acquisition | 1 sps；明确以前级时钟同步为前提 |
| Paillier 2020, `10.1109/JLT.2020.3003561` | 星地湍流 + AGC/DPLL maintenance | 支撑 carrier/fade 物理，不含 SCO timing loop |
| Wang 2023, `10.1109/JPHOT.2023.3265847` | FSTS 帧同步 + 两级 FOE | 1 sps；Q1 强近邻 |
| Wang 2024, `10.1364/OE.520452` | coherent FSO 帧同步 + 两级 FOE/carrier recovery | 接收算法下采样后工作；Q1 最强同场景近邻 |
| Valjus 2025, `10.1002/sat.1553` | 卫星相干光 timing/carrier DSP 综述与参数入口 | 参数多为设计/仿真范围，不等于外场测量 |
| Le Bidan 2023, `10.1109/ICSOS59710.2023.10490279` | 56-GBaud GEO、2 sps、frame/timing/CFO 顺序链 | 支撑系统真实性，不构成联合动作先例 |
| Sun 2025, `10.1109/JLT.2025.3533197`, arXiv `2409.14400` | clock recovery + frame synchronization + FOE 的最近直接竞品 | TS-A/Godard 与 TS-B FS/FOE 顺序分区；泛化 preamble claim 已占用，无 SCO |

Gu 2019 timing 与 OE 2022 timing detector 自动获取失败；JOCN 2026 三路径止损后仍无全文，保留为
Q1 `UNRESOLVED_HIGH_RISK`。不以摘要替代 exact collision 判断。逐篇 identity、provenance、SHA256、
行数与失败记录见 Step 2 receipts。

## 可采用的物理锚点

以下数值只作 Step 2 量级锚点，均未冻结为实验参数；“仿真内测得”不等于外场测量。

| 数值 | 全文位置 | 证据类型 | 当前可用范围 |
|---|---|---|---|
| 56 GBaud DP-QPSK、RRC roll-off 0.1、2 sps、128 GSa/s ADC | GEO 2023 `content.md:118-130,190-226` | 设计要求 + 数值仿真设置 | Q1/Q2 waveform 与采样链量级；非外场测量 |
| 时钟漂移容限 ±30 ppm、CFO ±5 GHz、线宽 600 kHz | GEO 2023 `:253-261,358-370` | 接收机设计要求 + 数值仿真设置 | GEO 顺序链测试范围；非实际轨迹分布 |
| 64-symbol 帧头、248 data + 8 pilot、3.6% 开销；捕获 <50 μs、总初始化 <100 μs | GEO 2023 `:420-469,607-652` | frame 设计；仿真内测得 acquisition time | preamble/延迟对照；不得称外场实测 |
| Gardner/Lee 2 sps，Oerder–Meyer 通常 4 sps | Valjus 2025 `content.md:187-220,253-281` | 综述归纳 + 该文数值仿真假设 | timing baseline 的采样率入口 |
| 地面光发端 ±20 ppm | Valjus 2025 `:382-383` | 引用标准的允许偏差 | 标准量级锚点；非星地接收端测量 |
| 最坏反向 LEO ISL Doppler 等效约 50 ppm | Valjus 2025 `:382-383` | 轨道条件推导 | ISL 上界参照；不可直接移植为 GEO/ground truth |
| 部分实现约 60–100 ppm timing 范围 | Valjus 2025 `:382-383` | 该文数值仿真/并行实现假设 | 候选 sweep 上界入口；仍需后续场景裁剪 |
| LEO 总 CFO ±4.5 GHz；预补偿残差 100 MHz | Paillier 2020 `content.md:95-105,143-161` | 系统范围 + 假设的固定残余 CFO | carrier baseline 设置；100 MHz 非外场测量 |
| 10 GBaud DPLL 锁定约 1.4 ms；fade 使临界 SNR 恶化约 5 dB | Paillier 2020 `:174-199` | TURANDOT/AO + DPLL 数值仿真内测得 | Q2 动机/时间尺度；不得称外场实测 |
| 湍流相位相干时间约 1 ms、闪烁指数 0.684、20° 仰角 | Paillier 2020 `:35-57,82-95` | 给定链路模型与数值时序设置 | 单一研究场景锚点；不代表真实 fade 事件分布 |

仍不能冻结：fractional timing 初始分布、随机 frame-offset 分布、GEO/地面 Doppler rate、真实深衰落
事件的深度/持续时间、fade 中 SCO 演化，以及 Gu 2019/OE 2022 的具体实验参数。

## 候选问题预卡状态

### Q1：sample-level 帧—分数定时—CFO acquisition

顺序 baseline 为 STSB/FSTS/相关帧定位与 CFO，再接独立 Gardner/插值定时。候选输入只能是
receiver-known preamble 的 ≥2-sps 样本；候选动作限定为 frame index、fractional delay 与 CFO 的联合或
coarse-to-fine 估计。Tang/Wang/OE 2024 均是强近邻，但已核全文未覆盖相同 sample-level fractional
timing 动作。因此 Q1 暂无 exact collision，但不得声称首创“帧同步+CFO”。最小 testbed 约 5.5–7.5 日。

### Q2：GG fade 与 SCO 下 timing/carrier lock maintenance 与重捕获

顺序 baseline 为 Gardner/GuCui timing loop + AGC/DPLL/VV carrier loop；廉价替代是共同门控冻结并按固定
preamble 周期重启。候选动作是单链路 timing NCO/interpolator 与 carrier loop 的 update/hold/reacquire，
不涉及 CCISP branch selection。物理动机成立，但尚无双环共同失锁、恢复时间或联合状态机增益的量化
全文证据，故仍是预卡。最小 testbed 约 7–9 日。

## Step 3 精读身份与方法分类

| L# | 论文 | title | 方法类别 | 与当前 Q# 的关键边界 | 全局笔记 |
|---|---|---|---|---|---|
| L01 | Tang 2022 STSB | PASS | CFSO frame→FOE | 1 sps；clock recovery 前置 | `papers/_read_notes/10.1109_jphot.2022.3161795.md` |
| L02 | Paillier 2020 AGC+DPLL | title-unverifiable，主题 PASS | carrier maintenance | ideal timing；无双环状态机 | `papers/_read_notes/10.1109_jlt.2020.3003561.md` |
| L03 | Wang 2023 FSTS | PASS | FSO frame→two-stage FOE | 1 sps；无 fractional timing/SCO | `papers/_read_notes/10.1109_jphot.2023.3265847.md` |
| L04 | Wang 2024 mixed TS | PASS | FSO frame→coarse/fine FOE | 接收端先下采样 | `papers/_read_notes/10.1364_oe.520452.md` |
| L05 | Valjus 2025 review | PASS | timing/carrier/equalizer 独立比较 | quasi-static fade；无联合恢复轨迹 | `papers/_read_notes/10.1002_sat.1553.md` |
| L06 | Le Bidan 2023 GEO chain | PASS | 2-sps timing/SCO→frame→carrier 顺序链 | 完整廉价 comparator；无 joint estimator | `papers/_read_notes/10.1109_icsos59710.2023.10490279.md` |
| L07 | Sun 2025 CAZAC preamble | PASS | clock→frame→FOE→CE | joint=training-unit reuse；动作仍顺序 | `papers/_read_notes/2409.14400.md` |

### Step 3.5 新增全文

| 文献 | identity / 全文 | action-level 分类 | 与 Q1 的边界 | 全局笔记 |
|---|---|---|---|---|
| Zhou 2025 JLT, `10.1109/JLT.2025.3528909`, arXiv `2410.10080v1` | PASS；555 行 | `SEQUENTIAL_MODULAR_ESTIMATION_WITH_PARTITIONED_PREAMBLE_REUSE` | 当前最强直接顺序 comparator；不是 exact three-parameter joint | `papers/_read_notes/2410.10080v1.md` |
| LPT 2017 FRFT, `10.1109/LPT.2017.2759584`, arXiv `1801.01598` | PASS；156 行 | true joint `(integer frame offset,CFO)` | 入口 1 sps、无 fractional τ/SCO | `papers/_read_notes/1801.01598.md` |
| Du 2021 JLT, `10.1109/JLT.2020.3042546` | PASS；712 行 | true joint `(integer τ,CFO,CPO)` | 无 frame output；CP-removed OFDM/fiber task 不匹配 | `papers/_read_notes/10.1109_jlt.2020.3042546.md` |
| JLT 2025 IQ-skew, `10.1109/JLT.2025.3581618` | PASS；344 行；用户提供 | shared-preamble sequential/extra-action | 有 frame/timing/FOE 模块，但无单一三参数 objective | `papers/_read_notes/10.1109_jlt.2025.3581618.md` |

未获取全文的 direct candidate 仅余 JOCN 2026 `10.1364/JOCN.587273`；用户已确认不可得，停止重试，
但不得用摘要裁 exact-action collision。

### 现有方法分类

- **frame+FOE 训练序列链**：Tang STSB、Wang FSTS 与 mixed PRBS/cyclic-QPSK 都以 known preamble
  定位 frame，再做 coarse/fine FOE；它们分别提供 CFSO turbulence、空间分集与低开销证据，但都不把
  fractional timing 放进同一 action。
- **过采样完整顺序前端**：Le Bidan 在 2 sps 下先 coarse CFO、matched filter、Lee timing/interpolation
  与 FSE，再下采样做 frame/fine CFO/CPE，形成 Q1 必须面对的最强廉价系统 comparator。
- **fade 下独立维护**：Paillier 量化 AGC+DPLL carrier 失稳和捕获，Valjus 分别比较 timing/CPE/FOE 并
  提示低质量时停止 FOE 更新；两者没有 dynamic fade 下的双环联合状态轨迹。

### 已知局限

- 当前 CORE 未量化强顺序 acquisition chain 在 simultaneous fractional timing/frame/CFO 下的失效；这是 Step 4a 待证假设，不是 Step 3 判据 1 FAIL；
- 未提供 GG/dynamic fade+SCO 下 timing/carrier 共同失锁与 post-fade recovery 数据；
- 未对 shared freeze + fixed known-preamble reacquisition 这一明显廉价替代做完整链比较；
- JOCN 2026 全文缺失仍限制任何 Q1 exact-action novelty closure，但不改变 D006 已确认的 Q1 四判据 PASS。

### 2–3 年趋势

2022–2025 的近邻工作从单一 FOE 转向短训练结构的 frame/FOE/CE 资源复用，并在系统层显式纳入
2-sps timing、SCO、并行实现与低 SNR acquisition；“joint”越来越常表示共享 preamble/资源，而不必然
表示单一联合 estimator。因此新的 action claim 必须逐一对齐 information、action、output 与时序。

### 研究背景概述

FSO 训练序列工作先解决低功率/湍流下 frame 与 FOE；卫星 receiver 设计再把 2-sps timing/SCO、frame、
fine CFO 与 CPE 串成可运行链；最新 coherent-PON 工作进一步压缩并复用 preamble。当前证据缺口不是
“没人联合画过框图”，而是强顺序链在目标 C 下是否真的因明确 A 失效。

### 研究问题清单（canonical 四判据）

| Q# | M | C | A | 方法产出形态 | 判据1 矛盾 | 判据2 产出 | 判据3 2019+ baseline | 判据4 对标 | 四判据 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Le Bidan 2-sps 顺序链 + Sun/Wang frame-FOE | RRC ≥2-sps coherent FSO，fractional timing/frame/CFO 同时未知 | 顺序 timing-first 处理在同时未知状态下可能传播误差或产生错误峰/误锁 | coupled estimator / design rule | ✅ M/C/A 明确、句子级、可解，A 可证伪；不要求已有 MVE | ✅ 形态可复用 | ✅ GEO 2023、Sun 2025、Wang 2023/2024 | ✅ error/success/BER/overhead/latency | **STEP3_SURVIVOR** | L01/L03/L04/L06/L07 |
| Q2 | timing/carrier 独立 maintenance/reacquisition；cheap shared-freeze+fixed-restart | ≥2-sps OSL，SCO/PN/CFO + dynamic deep fade | fade 可能使双环共同/异步失锁且 cheap comparator 可能不足 | shared-confidence FSM / lock rule | ✅ M/C/A 明确、句子级、可解，A 可证伪；共同失锁尚未实证不构成 Step 3 FAIL | ✅ 形态可复用 | ❌ 无 2019+ integrated comparator，跨论文拼接不算 | ✅ error/slip/BER/recovery time | **未过（仅判据 3 FAIL）** | L02/L05 |

### Baseline 交叉验证

| Q# | 最强 comparator | task fit | 当前未决 |
|---|---|---|---|
| Q1 | `polyphase/Farrow timing bank + 2-sps coarse CFO → timing/interpolation → FSE/downsample → Sun CAZAC 或 FSTS/STSB frame/FOE` | information/action/output 均与 acquisition task 对齐 | Step 3.5 需关闭这一最强廉价 comparator；其失效留待 Step 4a，不前移到 Step 3 |
| Q2 | Gardner/Gu timing + AGC/DPLL/VV/FOE + shared quality freeze + fixed preamble/reference restart | 是必须先排除的廉价 conventional extension | 尚无全文完整链与量化结果，不能宣称已解决或已失败 |

## Step 3.5 与 JOCN 处理

- Round 1：6/6 query，100 rows / 80 unique，must=5、should=6；Round 2：3/3 focused query，27 rows /
  25 unique，真正新增 must=0、should=0；收敛，未启动 Round 3。
- Sun 2025 引用链：forward=8、backward=35，S2-only=0。
- 新增全文：Zhou 2025（arXiv `2410.10080v1`）为分区 preamble 顺序链；LPT 2017（arXiv
  `1801.01598`）为 joint integer frame+CFO、1 sps 无 fractional τ；JLT 2021 为 joint τ+CFO+CPO、
  无 frame 且 OFDM/fiber task 不匹配。均非 exact 三参数 collision。
- JLT 2025 IQ-skew 用户全文已裁为 shared-preamble sequential/extra-action，非 exact collision；JOCN
  2026 仍为 `USER_CONFIRMED_FULLTEXT_UNAVAILABLE`，停止重试但保留 claim limitation。
- 最强廉价 comparator 冻结为 polyphase/Farrow timing bank + Zhou/Le Bidan/Sun/FSTS/STSB sequential
  chain；这是公平 comparator contract，不是拼接出来的单篇 baseline identity。

## 当前结论

terminal=`STEP3_5_COMPLETE_Q1_SURVIVOR_JOCN_FULLTEXT_UNAVAILABLE_NO_CONFIRMED_EXACT_COLLISION`。
Q1 是唯一 Step 3 survivor；Q2 仅判据 3 FAIL。当前可得全文池未确认 exact collision，但 JOCN 未读
限制意味着不能声称 exact-action novelty closure。coverage decision 已处理；下一合法动作仅为新会话
Step 4a preflight discussion，本轮不产生 METHOD_SIGNAL、Go、论文方法或仿真授权。
