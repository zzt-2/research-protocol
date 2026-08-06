# 过采样相干 FSO 联合同步前端：Groundwork 文献状态

> 2026-08-06 | GW Step 3 已完成 | terminal: `STEP3_NO_VALID_PROBLEM`

## 边界

用户已接受 7 篇 CORE 覆盖面；本文档进入 Step 3 精读。当前仍不声称问题四判据、新颖性或方法可行性
已经闭合；只有至少一个 Q# 全过四判据才进入 Step 3.5，且本轮不得进入 Step 4a、实现或仿真。

## GW 进度

| Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| Step 1 search | ✅ | `oversampled-sync-groundwork/step1-search-report.md`；6 query，140 raw / 130 unique，2019+ 39 unique | 两张机制不同预卡存活，允许 Step 2 |
| Step 2 acquire | ✅ 用户已确认 | `oversampled-sync-groundwork/step2-coverage-report.md`；7 CORE 全文通过 identity/SHA/≥50 行门 | D004 接受覆盖面 |
| Step 3 read | ✅ | `oversampled-sync-groundwork/step3-deep-read-report.md`；7 篇 CORE 结构化全文精读 | Q1/Q2 均未全过 canonical 四判据 |
| Step 3.5 supplement | N/A（门未触发） | Step 3 survivor=0 | 未检索、未重抓 JOCN 2026 |
| Step 4a | ⬜ 禁止 | 无 survivor | 不存在入口 |

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

### 现有方法分类

- **frame+FOE 训练序列链**：Tang STSB、Wang FSTS 与 mixed PRBS/cyclic-QPSK 都以 known preamble
  定位 frame，再做 coarse/fine FOE；它们分别提供 CFSO turbulence、空间分集与低开销证据，但都不把
  fractional timing 放进同一 action。
- **过采样完整顺序前端**：Le Bidan 在 2 sps 下先 coarse CFO、matched filter、Lee timing/interpolation
  与 FSE，再下采样做 frame/fine CFO/CPE，形成 Q1 必须面对的最强廉价系统 comparator。
- **fade 下独立维护**：Paillier 量化 AGC+DPLL carrier 失稳和捕获，Valjus 分别比较 timing/CPE/FOE 并
  提示低质量时停止 FOE 更新；两者没有 dynamic fade 下的双环联合状态轨迹。

### 已知局限

- 当前 CORE 未量化强顺序 acquisition chain 在 simultaneous fractional timing/frame/CFO 下的失效；
- 未提供 GG/dynamic fade+SCO 下 timing/carrier 共同失锁与 post-fade recovery 数据；
- 未对 shared freeze + fixed known-preamble reacquisition 这一明显廉价替代做完整链比较；
- JOCN 2026 全文缺失仍限制任何 Q1 exact-action novelty closure，但不改变本轮更上游的四判据 FAIL。

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
| Q1 | Le Bidan 2-sps 顺序链 + Sun/Wang frame-FOE | RRC ≥2-sps coherent FSO，fractional timing/frame/CFO 同时未知 | 顺序链假设 timing 可先独立恢复；该假设在目标条件下失效 | coupled estimator / design rule | ❌ CORE 未证实顺序链失效 | ✅ 形态可复用 | ✅ GEO 2023、Sun 2025、Wang 2023/2024 | ✅ error/success/BER/overhead/latency | **未过** | L01/L03/L04/L06/L07 |
| Q2 | Gardner/Gu timing + AGC/DPLL/VV/FOE；cheap shared-freeze+fixed-restart | ≥2-sps OSL，SCO/PN/CFO + dynamic deep fade | 双环共同失锁且 cheap comparator 仍不足 | shared-confidence FSM / lock rule | ❌ 共同失锁与 cheap comparator 失效未证实 | ✅ 形态可复用 | ❌ 无 2019+ integrated comparator | ✅ error/slip/BER/recovery time | **未过** | L02/L05 |

### Baseline 交叉验证

| Q# | 最强 comparator | task fit | 当前未决 |
|---|---|---|---|
| Q1 | `2-sps coarse CFO → Lee/Gardner timing/interpolation → FSE/downsample → Sun CAZAC 或 FSTS/STSB frame/FOE` | information/action/output 均与 acquisition task 对齐 | 没有该顺序链失效的正文证据 |
| Q2 | Gardner/Gu timing + AGC/DPLL/VV/FOE + shared quality freeze + fixed preamble/reference restart | 是必须先排除的廉价 conventional extension | 尚无全文完整链与量化结果，不能宣称已解决或已失败 |

## Step 3.5 与 JOCN 处理

Step 3 survivor=0，故未触发 Step 3.5：没有执行定向检索、双向引用链或新一轮 JOCN 2026 获取。
JOCN 2026 继续登记为 `UNRESOLVED_HIGH_RISK`，不得以 abstract 作 exact-action collision/full-text 裁决。

## 当前结论

terminal=`STEP3_NO_VALID_PROBLEM`。Q1、Q2 均未通过 canonical 四判据，唯一 survivor：无；不存在
Step 4a 入口。本轮不产生 METHOD_SIGNAL、Go、论文方法或仿真授权。
