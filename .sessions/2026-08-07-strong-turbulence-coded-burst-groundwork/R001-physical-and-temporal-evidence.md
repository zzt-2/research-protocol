# [R001] 低仰角强湍流与时间相关 burst 物理证据

> 2026-08-07 | 关联：2026-08-07-strong-turbulence-coded-burst-groundwork / S001

## 调研问题

在不把仿真参数冒充真实 occurrence 的前提下，判断现有本地证据是否足以支持：

1. 低仰角星地 FSO 的合法强湍流、Gamma–Gamma（GG）、闪烁或 Rytov 参数；
2. temporal correlation/coherence/fade duration 接近或跨越约 810-symbol 固定 span；
3. 区分可由时间交织恢复的短 burst 与覆盖整个 coherence block 的 outage。

本记录只给事实、证据分级和未决项，不作方法裁决。

## 检索 receipt

| 组 | 固定 query 语义 | source | 文件级命中数 | 检索输出 |
|---|---|---:|---:|---|
| Q1 | `satellite space-ground FSO low elevation strong turbulence Gamma-Gamma field measurement scintillation` | 本地 `rg`：`search-archive/**` 14；`papers/**/content.md` 5 | 19 | 复用本地索引/全文，未调用 `tools/search`；因此未创建 `search-archive/2026-08-07/strong-turbulence-low-elevation.json` |
| Q2 | `satellite optical link temporal correlation coherence time fade duration burst error turbulence` | 本地 `rg`：`search-archive/**` 31；`papers/**` 8（含 7 个 `content.md`、1 个 metadata） | 39 | 复用本地索引/全文，未调用 `tools/search`；因此未创建 `search-archive/2026-08-07/strong-turbulence-temporal-burst.json` |

- query 总数：**2**；无 Web、无下载、无第 3 组。
- 两个 JSON 路径仅是 T001 对新增检索的指定路径；本轮本地材料已足以暴露承重缺口，且父任务限定唯一产物为 R001，故没有制造额外检索产物。
- 上表是各组**首次执行时**的 receipt。收尾时原样重跑 Q2，文件级命中变为 45（`search-archive/**` 37、`papers/**` 8）；差额来自共享 worktree 在本轮期间并发出现的 2026-08-07 coded/interleaving 检索缓存。本 R001 不吸收该并发新增证据，避免越出 T001 的两组固定证据边界。

## 来源分级

分级只表示与本问题的承重距离，不表示论文总体质量。

| 级别 | 来源 | 场景与证据类型 | 可承载事实 | 不能承载 |
|---|---|---|---|---|
| B1（目标物理推导，abstract） | Andrews et al., *Fade statistics associated with a space/ground laser communication link at large zenith angles*, 1999, DOI `10.1117/12.363622`；S2 abstract：`search-archive/_index/all-papers.jsonl:19228` | space/ground、大天顶角；链路物理推导 | 大天顶角时强度起伏可超出弱起伏理论；计算 fade probability；GG 两参数对应大尺度/小尺度闪烁 | 无本站点、仰角、`α/β`、Rytov、fade duration 数值；不是外场 occurrence |
| B1（目标物理推导，abstract） | Andrews et al., *Impact of scintillation on laser communication systems*, 2002, DOI `10.1117/12.453235`；S2 abstract：`search-archive/_index/all-papers.jsonl:19227` | satellite/ground、大天顶角；物理建模综述/推导 | 大天顶角 uplink/downlink 可进入强起伏；强条件下 GG 比 lognormal 更合适 | 无低仰角站点绑定和可直接采用的数值参数 |
| B2（目标系统分析全文） | Le & Pham, *On the Design of FSO-Based Satellite Systems Using IR-HARQ...*, IEEE TVT 2022, DOI `10.1109/TVT.2021.3127193`；`papers/doi/10.1109_tvt.2021.3127193/content.md:5`、`:21` | LEO satellite-to-ground；HV/Rytov 推导 + FSMC/Monte Carlo | Rytov 随 zenith angle 与地面 `Cn²(0)` 计算；卫星 FSO coherence 为 tens of ms 的二手引用；相关 frame-loss burst 建模 | 文中“strong”数值是仿真设计标签；其自身 HV 计算反而报告 LEO-to-ground Rytov `<1`，不能证明真实强 occurrence |
| B2（外场类比测量全文） | Horst et al., *Tbit/s line-rate satellite feeder links...*, 2023, DOI `10.1038/s41377-023-01201-7`；`papers/doi/10.1038_s41377-023-01201-7/content.md:3-11` | 53.42 km 山地 terrestrial link，作者称模拟 satellite-ground worst case；外场测量 | coherence time 为 few ms；实测 SI 1–4、`r0≈4 cm`；低于 FEC threshold 的序列完全丢失 | 不是实际低仰角星地链路；文中还称典型 GEO-earth worst-case SI `<1`，不能据此移植 SI 1–4 |
| C（目标系统仿真设计） | 同 Le & Pham 2022 | `H=300 km`、`v=21 m/s`、`Cn²(0)=10^-13 m^-2/3`；仿真/优化 | 该设计下数值优化得到 200 blocks/burst | 200 blocks 不是实测 fade span；`Cn²(0)=10^-13` 不是实测 occurrence |
| C（LEO 意图仿真） | Galijasevic et al., *Predicting Channel Conditions for Adaptive LDPC Coding...*, DOI `10.1109/OJCOMS.2024.011100`；`papers/doi/10.1109_ojcoms.2024.011100/content.md:5-19` | 以 LEO 为意图的 correlated lognormal/block-fading 仿真 | 假定 coherence `10 ms`、2.5 Gbaud；给出 codeword 时间 3.6864–31.539 µs | `10 ms` 和 PSI=10 是模型输入；不是低仰角外场测量，也不是 GG 强湍流 occurrence |
| C（非目标外场数据再利用） | Nguyen et al., *Adaptive Rate/Power Control With ML-Based Channel Prediction...*, DOI `10.1109/TAES.2024.3403809`；`papers/doi/10.1109_taes.2024.3403809/content.md:353-383` | 用既有 FSO measurement 数据训练 satellite-system predictor | 数据集 Rytov `0.0075/0.1020`、采样间隔 `1 ms` | 两值均属弱起伏，且原测量场景未在相关段落绑定为低仰角星地；不能支持目标强条件 |
| B3（仅 abstract） | Le et al., *Level Crossing Rate and Average Fade Duration of Satellite-to-UAV FSO Channels*, DOI `10.1109/JPHOT.2021.3057198`；S2/OpenAlex abstract：`search-archive/_index/all-papers.jsonl:18082` | LEO satellite-to-UAV；AFD/LCR 解析推导 | 证明该类链路可解析讨论 AFD/LCR，且同时考虑 turbulence 与 pointing | 本地 abstract 无 AFD 数值；UAV 不是 ground station；不能与 810 symbols 比较 |

说明：B1/B2/B3 不是“外场强 occurrence”等级。当前本地集合中没有一篇同时满足“真实 satellite-ground + 明确低仰角/大天顶角 + 强湍流数值 + 时间持续尺度”的一手外场测量。

## 参数与可追溯事实

| 参数/量 | 数值与单位 | 目标场景 | 证据类型 | 指针 | 与 810-symbol span 的关系 |
|---|---:|---|---|---|---|
| 大天顶角强起伏 | 无具体数值；定性为可超出 weak-fluctuation limit | space/ground uplink/downlink，大天顶角 | 物理推导 abstract | `search-archive/_index/all-papers.jsonl:19228`，DOI `10.1117/12.363622` | 不可换算 |
| GG 适用性 | 无 `α/β`；两参数物理关联大/小尺度闪烁 | 强起伏 satellite/ground | 物理推导 abstract | `search-archive/_index/all-papers.jsonl:19227-19228` | 不可换算 |
| Rytov 强弱边界 | `σ_R²<1` weak，`≈1` moderate，`>1` strong | satellite-to-ground plane wave 模型 | 物理定义/推导 | `papers/doi/10.1109_tvt.2021.3127193/content.md:161-167` | 不涉及时间 |
| 地面 `Cn²(0)` 探索范围 | `10^-17` 至 `10^-13 m^-2/3` | HV profile 参数范围 | 物理模型输入 | 同上 `:167-177` | 不涉及时间 |
| 同一 HV 模型的 LEO 结论 | 数百 km LEO-to-ground 的 `σ_R²<1` | 模型覆盖的 zenith-angle/ground-turbulence 范围 | 物理推导结果 | 同上 `:177` | 对“合法强 occurrence”构成反证/张力，不给时间 |
| 仿真所谓 weak/moderate/strong | `Cn²(0)=10^-14 / 5×10^-14 / 10^-13 m^-2/3` | LEO IR-HARQ 数值实验 | **仿真设计参数** | 同上 `:393-403` | 不能当 occurrence |
| 优化 burst size | `200 blocks/burst`，条件 `H=300 km`、`v=21 m/s`、`Cn²(0)=10^-13 m^-2/3` | 同一 IR-HARQ 仿真 | **仿真输出** | 同上 `:423-433` | 缺每 block symbols/bits，不能与 810 symbols 等同 |
| satellite FSO coherence | “tens of ms” | LEO satellite-ground，论文二手引用 | 文献陈述/模型依据 | 同上 `:53-55` | 缺目标 symbol rate；仅能判断时间远长于典型高速 codeword |
| 山地类比外场 coherence | few ms | 53.42 km terrestrial satellite-link surrogate | **外场测量** | `papers/doi/10.1038_s41377-023-01201-7/content.md:67-82` | 该实验 126 GBd 时，810 symbols=`6.43 ns`；若 few ms 取 2–5 ms，仅量级换算为 `2.52×10^8–6.30×10^8 symbols`，约为 810 的 `3.11×10^5–7.78×10^5` 倍；场景不可直接移植 |
| 山地类比外场 SI / Fried length | SI 1–4；`r0≈4 cm` | 同上 | **外场测量** | 同上 `:99-101` | 空间/强度指标，不能直接给 burst duration |
| LEO 意图 coherence | `10 ms` | correlated lognormal LEO-intent model | **仿真设计参数** | `papers/doi/10.1109_ojcoms.2024.011100/content.md:152-165` | 在 2.5 Gbaud 下为 `2.5×10^7 symbols`，是 810 的约 `3.09×10^4` 倍；不是实测 |
| codeword occupancy | `3.6864–31.539 µs`；2.5 Gbaud | 同一 LDPC 仿真 | **仿真设计/派生量** | 同上 `:177-179` | 对应约 `9,216–78,848 symbols`；810 symbols 仅 `0.324 µs`，仍短于其最短 codeword |
| Power Scintillation Index | `PSI=10` | 同一 LDPC fading model | **人为 stress 参数** | 同上 `:261-263` | 不能证明低仰角发生率或 fade duration |
| 再利用测量 Rytov | `0.0075`、`0.1020`；采样 `1 ms` | 来源场景未在承重段落绑定为 satellite-ground | **外场数据再利用，但非目标场景** | `papers/doi/10.1109_taes.2024.3403809/content.md:353-383` | Rytov 明确在弱区；采样间隔不是 coherence/fade duration |

所有 symbols 换算均只使用对应论文明确给出的 symbol rate；没有为目标旧仿真臆造数据率。

## Gate

### physical-support gate：UNKNOWN

事实支持到以下边界：

- 大天顶角 space/ground 路径进入强起伏、GG 替代 lognormal 在物理上有同行评审推导支持（DOI `10.1117/12.363622`、`10.1117/12.453235`）。
- 但本地证据没有给出一个可追溯到真实低仰角地面站/时段/路径的 `α/β`、`σ_R²>1`、SI 或 fade occurrence 数值。
- 现有 LEO HV 推导还明确报告其覆盖条件下 `σ_R²<1`；论文随后把 `Cn²(0)=10^-13 m^-2/3` 称为 strong 是数值实验分组，不能覆盖前述缺口。

因此，证据足以支持“值得查具体低仰角强条件”，不足以支持“已有合法数值可直接替换条件 C”；也没有证据证明该条件不可能，故不是 FAIL。

### temporal-span gate：UNKNOWN

- ms 级相关时间有两类证据：53.42 km 类比外场实测 few ms，以及 LEO-intent 仿真假定 10 ms；LEO IR-HARQ 论文另称 tens of ms。
- 在各论文自己的高速率下，ms 级 span 均远大于 810 symbols，而不是“自然接近 810”。
- 但没有来源同时绑定目标低仰角星地强湍流、fade threshold、data/symbol rate 和 AFD 分布；`coherence time` 不能替代 `average fade duration`，采样间隔也不能替代二者。

因此，目前只能确认“整个 810-symbol span 可能落在同一相关状态内”的风险，不能确认可恢复 burst 的长度分布。

## 不可恢复 outage 风险

1. Horst 外场结果称 ROP 低于 FEC threshold 时，对应测量数据序列完全丢失（`papers/doi/10.1038_s41377-023-01201-7/content.md:99-101`）。这是一手现象，但采样为每 1.5 s 一次的连续测量序列展示，不能据此给出 fade duration。
2. 当 810 symbols 的持续时间远短于 ms 级相关时间时，若深衰落阈值跨越整个该 span，span 内重排不产生时间多样性；这是由尺度关系得到的风险陈述，不是对特定编码器的性能裁决。
3. JPHOT 2021 的 abstract 表明 LCR/AFD 是可计算对象，但本地无数值。没有 AFD CDF/threshold，无法区分“短暂可恢复 burst”与“coherence-block outage”。
4. outage probability 上升、burst loss correlation、coherence time 三者均不等价；当前证据不可把任一者直接替换为 810-symbol burst 长度。

## 候选 CORE 清单

| 优先级 | 候选 | 可承担角色 | 当前缺口 |
|---:|---|---|---|
| 1 | DOI `10.1117/12.363622` | 低仰角/大天顶角强起伏与 GG 的物理起点 | 需获取承重公式/图表中的仰角、站点/profile、`σ_R²`、GG 参数和 fade threshold；本轮不下载/精读 |
| 2 | DOI `10.1117/12.453235` | weak-to-strong satellite/ground GG 合法性补强 | abstract 无目标参数数值 |
| 3 | DOI `10.1109/JPHOT.2021.3057198` | LCR/AFD 与动态 satellite optical link 的直接入口 | satellite-to-UAV，且本地无 AFD 数值/阈值 |
| 4 | DOI `10.1109/TVT.2021.3127193` | LEO burst correlation、zenith/HV/Rytov 公式与反证边界 | strong 标签属于仿真；200 blocks 缺 symbol 映射 |
| 5 | DOI `10.1038/s41377-023-01201-7` | 外场 coherence、SI、FEC-threshold 丢失风险的类比锚点 | terrestrial surrogate，不是实际低仰角 satellite-ground |

`10.1109/OJCOMS.2024.011100` 只宜作为时间尺度换算和 stress-model 反例，不作为物理 occurrence CORE。`10.1109/TAES.2024.3403809` 的再利用测量 Rytov 均为弱区，也不作为强条件 CORE。

## 未决/失败获取清单

- `Characterization of atmospheric turbulence for LEO to ground laser beam propagation at low elevation angles`（2014）在本地仅有题录：`search-archive/_index/all-papers.jsonl:18924`；无 DOI、abstract、全文，不能承重。
- 两篇 SPIE CORE 当前只有 S2 abstract；缺低仰角数值表、GG `α/β`、Rytov 与 fade threshold 的原文指针。
- JPHOT 2021 当前只有 abstract；缺 AFD/LCR 数值、阈值、速度/仰角/路径设定。
- 未获得“真实 satellite-ground 外场 + 明确低仰角 + `σ_R²>1`/SI/GG 数值 + AFD/coherence”四项同源证据。
- 目标旧仿真的 symbol rate、codeword 映射和 fade threshold 未由 T001 提供；因此不能把任何 ms 值合法换算成目标 burst 长度。
- 本轮未调用 Web，故没有 Web 功能断言，也无需新增 S2/DOI 交叉验证条目；两篇 S2 abstract 已在本地索引中带 `source_apis: [semantic_scholar]`。

## 结论

现有本地证据形成的是“**大天顶角强起伏/GG 在物理上成立，但目标 occurrence 与时间持续尺度未闭环**”的证据状态：physical-support gate 与 temporal-span gate 均为 **UNKNOWN**。这足以识别 Step 1 的承重缺口，不足以把任意强湍流参数或 ms 级 coherence 直接写入目标条件 C。

## 对决策的影响

本 R001 不形成 Go/Kill/METHOD_SIGNAL，也不新建 D###。若主线要让 Step 1 承重门变为 PASS，至少需要同源或可审计组合证据补齐：真实低仰角星地场景参数 + 强条件 occurrence + threshold-conditioned AFD/相关尺度 + 目标 symbol-rate 映射。
