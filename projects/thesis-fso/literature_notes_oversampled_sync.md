# 过采样相干 FSO 联合同步前端：Groundwork 文献状态

> 2026-08-06 | 仅完成 GW Step 1–2 | terminal: `STEP2_READY_FOR_USER_CONFIRMATION`

## 边界

本文档只汇总检索与全文覆盖面，不是 Step 3 精读笔记，不声称问题四判据、新颖性或方法可行性已经闭合。
未经用户确认覆盖面，不得进入 Step 3、Step 3.5、Step 4a、实现或仿真。

## GW 进度

| Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| Step 1 search | ✅ | `oversampled-sync-groundwork/step1-search-report.md`；6 query，140 raw / 130 unique，2019+ 39 unique | 两张机制不同预卡存活，允许 Step 2 |
| Step 2 acquire | ✅ 待用户确认 | `oversampled-sync-groundwork/step2-coverage-report.md`；7 CORE 全文通过 identity/SHA/≥50 行门 | 停在用户覆盖面确认门 |
| Step 3 read | ⬜ 禁止自动进入 | 尚无 | 用户明确确认后才可开始 |
| Step 3.5 / Step 4a | ⬜ 禁止 | 尚无 | Step 3 未完成 |

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

## 当前结论

Step 1 六个停止条件均未触发；Step 2 以 7 篇 CORE（含最近直接竞品 JLT 2025）达到覆盖面确认门。
JOCN 2026 全文缺失仍须由用户明确接受或补文。下一合法动作仅是用户确认、
补充或替换 CORE 文献；本轮不产生方法 claim。
