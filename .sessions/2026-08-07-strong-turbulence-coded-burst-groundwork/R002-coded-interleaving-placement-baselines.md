# [R002] Coded FSO interleaving/placement 与 2019+ baseline 证据

> 2026-08-07 | 关联：2026-08-07-strong-turbulence-coded-burst-groundwork / S001

## 调研问题

在 coded FSO 的 temporal-correlated fading / burst 条件下，核对 fixed/deep interleaving、adaptive depth、channel-aware permutation/codeword mapping、parity/bit placement、frame segmentation/scheduling 的真实 action；区分 2019+ task-matched comparator、adjacent mechanism 与旧方向 collision。本记录只汇总检索/摘要证据，不形成 Go/Kill、METHOD_SIGNAL 或方法卡。

严格 task-matched 判据为同一 **task / condition / deployable information / output**：任务须改变 coded FSO 译码输入的时间错误分布；条件须包含 temporal correlation、burst duration 或 coherence mismatch；信息须与候选在部署时可获得的信息一致；输出须为 interleaving/permutation/placement/segmentation，而非码率、MCS、LLR 标定、译码器或 HARQ 冗余选择。

## 4 组 query receipt

总 query 组数：**4（已达硬封顶；未因第 4 组零命中追加 query）**。全部使用仓库 `tools/search`，source 为 Semantic Scholar（`s2`）与 OpenAlex；Web/API 功能断言只采用两源返回的题录/abstract 或已有本地索引记录，没有下载全文。

| # | query | source/count receipt | 最终 count | 显式输出 |
|---|---|---|---:|---|
| Q1 | `coded free-space optical interleaving correlated turbulence fading burst errors` | S2：发现 50、返回 20；OpenAlex：发现 49、返回 20；原始 40、去重 37、过滤/截断后 20 | 20 | `search-archive/2026-08-07/coded-fso-correlated-interleaving.json` |
| Q2 | `adaptive channel-aware interleaver codeword mapping optical wireless FSO` | S2：0；OpenAlex：19；原始 19、去重 16、过滤后 7 | 7 | `search-archive/2026-08-07/coded-fso-channel-aware-mapping.json` |
| Q3 | `parity bit mapping fading blocks coded modulation burst channel optical wireless` | S2：发现 108、返回 20；OpenAlex：发现 172、返回 20；原始 40、去重 39、过滤/截断后 20 | 20 | `search-archive/2026-08-07/coded-fso-parity-placement.json` |
| Q4 | `coded FSO recent LDPC polar interleaver baseline correlated fading 2019 2026` | S2：0；OpenAlex：0 | 0 | `search-archive/2026-08-07/coded-fso-recent-baselines.json` |

`tools/search` 还按 query slug 自动保存了 4 个内容重复的存档：

- `search-archive/2026-08-07/coded-free-space-optical-interleaving-correlated-turbulence-.json`
- `search-archive/2026-08-07/adaptive-channel-aware-interleaver-codeword-mapping-optical-.json`
- `search-archive/2026-08-07/parity-bit-mapping-fading-blocks-coded-modulation-burst-chan.json`
- `search-archive/2026-08-07/coded-fso-recent-ldpc-polar-interleaver-baseline-correlated-.json`

以上自动存档不计作新增 query，也不作为独立证据条目。

## 发现

### 候选论文与真实 action

| identity | year / venue / DOI / status | deployable information | 真实 action 与输出 | channel lifecycle | metric | 证据指针与分类 |
|---|---|---|---|---|---|---|
| Sun & Noh, *End-to-End Performance Analysis of CCSDS O3K...* | 2025 / Aerospace / `10.3390/aerospace12100869` / published, OA | 固定系统配置；摘要未声称在线 CSI 驱动 | CCSDS O3K **固定 block interleaver/depth**；输出为静态交织后的帧/码字顺序 | Ornstein–Uhlenbeck amplitude scintillation，显式 temporal correlation；扫 coherence time 与 interleaving depth | BER / reliability | Q1 `L002`；S2+OpenAlex abstract。**task-matched fixed baseline；旧 4b#1 collision** |
| Clements et al., *Capacity-based analysis of physical-layer and link-layer techniques...* | 2025 / SPIE LASE / `10.1117/12.3041270` / published | 摘要未给出在线 CSI；按架构与 fade statistics 比较 | physical-layer FEC + codeword interleaving，对比 link-layer erasure coding/ARQ | FSO turbulence/pointing-jitter fading；覆盖 benign/moderate/very strong fluctuations，但 abstract 未闭合 temporal-correlation 生成过程 | Shannon capacity / link-budget advantage（约 3 dB） | Q1 `L006`；S2 abstract。**adjacent：metric/output 不同，不能升为严格 task-matched** |
| Li et al., *Demonstration of 10 Gbps satellite-to-ground laser communications in engineering* | 2024 / The Innovation / `10.1016/j.xinn.2023.100557` / published, OA | 工程链路状态、错误帧检测与上行反馈；未给出 mapper 专用 CSI | payload 打包为 **long interleaved data frames**，错误帧经 ECP 重传；无隔离的 placement 优化输出 | 实际 LEO-to-ground 非平稳信道；scintillation 可达 100 Hz | 10 Gbps；BER `<1e-7`；工程吞吐 | `search-archive/_index/all-papers.jsonl:12191`；OpenAlex abstract/full-record 摘要。**adjacent engineering anchor；系统 bundle 非可归因 comparator** |
| Zhu & Kahn, *Performance bounds for coded FSO...* | 2003 / IEEE TCOM / `10.1109/TCOMM.2003.815052` / published | 离线 channel statistics / weak-turbulence 假设 | 选择 interleaver length；不执行 channel-aware permutation | temporal-correlated turbulence；近似仅对 weak turbulence 有效，strong turbulence 被作者明确判无效 | pairwise codeword-error / BER bounds | Q1 `L001`；S2 abstract。**旧 4b#1 collision；非 2019+** |
| Zhu et al., *Theoretical and experimental studies of TPC with time diversity...* | 2010 / Optics Express / `10.1364/OE.18.026978` / published | 实验 fade statistics；固定设计时信息 | TPC + interleaving，比较并选择 interleaving depth | 实测 turbulence fading / burst errors；time diversity | error performance / optimum depth | Q1 `L009`；S2 abstract。**旧 4b#1 collision；非 2019+** |
| Zhang et al., *Adaptive Interleaving Method...* | 2012 / Advanced Materials Research / `10.4028/www.scientific.net/AMR.571.382` / published | channel estimator 更新的 burst information | **在线切换 interleaving depth**；输出仍是 depth/B，不是固定 B 内 permutation | 11.8 km urban experimental CSI 驱动的 long/deep fades | memory saving；anti-burst cost（相对最大内存可降至 10% 或更小） | Q1 `L017`；S2 abstract。**旧 4b#1 exact collision；非 2019+** |
| Kam et al., *Design of high-speed framing, FEC, and interleaving hardware...* | 2009 / SPIE / `10.1117/12.826309` / published | 固定硬件配置；可调 code/interleaver length | 非标准、可调 interleaver length + FEC/framing | 5.4 km horizontal link；strong scintillation，fade 经常 `>10 ms` | error-free transmission | Q1 `L019`；S2 abstract。**旧 fixed-depth collision；非 2019+** |
| Yamazaki et al., *Performance analysis of polar-code transmission experiments...* | 2021 / ICSO 2020 / `10.1117/12.2599963` / published | receiver estimated CSI | channel equalization 后再做 polar/LDPC decoding；不输出 permutation/placement | 7.8 km terrestrial FSO；scintillation-induced burst errors；abstract 未量化跨码字状态连续性 | BLER | Q1 `L010`；OpenAlex abstract。**P08 collision/action mismatch，不是 placement baseline** |
| Fang et al., *Polar coded probabilistic amplitude shaping...* | 2020 / Optics Express / `10.1364/oe.405241` / published | turbulence distribution / 离线 shaping 设计 | MLC/BICM shaping、labeling 修改、polar-PAS exchange；不是随 temporal CSI 变化的 bit placement | turbulence channel；abstract 未声称 temporal correlation | achievable rate / BLER | Q1 `L011`；S2 abstract。**adjacent coded-modulation；不是 task-matched** |
| Wang et al., *Probabilistically shaped polar-coded MIMO-FSO...* | 2022 / Optics Express / `10.1364/oe.459583` / published | turbulence distribution与空间相关参数；离线 shaping | shaping-bit 数与分布选择；输出不是时间 permutation | **spatially correlated** MIMO fading，不是 temporal correlation | AIR / BER / shaping gain | Q1 `L007`；S2 abstract。**adjacent；不能把 spatial correlation 当 temporal burst** |
| Gupta & Jain, *LDPC coded FSO... correlated GG... SSK* | 2023 / SPIE Photonics Asia / `10.1117/12.2687617` / published | correlation coefficient / receiver count（分析参数） | LDPC on/off 与 SSK receiver diversity；无 interleaver/placement action | receiver-spacing 引起的 **spatial correlation** | ABER / SNR gap | Q1 `L005`；S2 abstract。**adjacent；不是 temporal-burst comparator** |
| Chen et al., *Interleaver Design for Small-Coupling-Length SC-PLDPC-BICM...* | 2020 / IEEE Access / `10.1109/ACCESS.2020.2974002` / published, OA | Rayleigh channel model与 UEP bit-channel reliability；离线 MI 分析 | SPMM：匹配 spatial positions 与调制 bit positions；固定 bit mapper/interleaver | generic Rayleigh fading；非 FSO，未处理 optical temporal coherence | decoding threshold / BER | Q3 `L006`；S2 abstract。**generic RF/block-fading placement prior art，仅 adjacent** |
| Li et al., *Precoding for WER Minimization of LDPC Coded Modulation on Block Fading Channels* | 2012 / IEEE TWC / `10.1109/TWC.2012.051712.111142` / published | transmitter **无 CSI**；离线 fading distribution | 联合选择 precoding matrix、mapping function 与 code | generic block fading；非 FSO | WER / outage proximity | Q3 `L011`；S2 abstract。**generic block-fading prior art，仅 adjacent** |
| Göktepe et al., *Channel-Prediction-Driven Rate Control for LDPC Coding...* | 2025 / IEEE OJ-COMS / `10.1109/ojcoms.2025.3538839` / published | delayed receiver CSI + linear/quadratic prediction | 动态选择 PBRL-LDPC **code rate** | fading FSO；coherence time 5/10 ms，反馈延迟扫至一个 coherence time | throughput | `search-archive/_index/all-papers.jsonl:12831`；S2 abstract。**AMC collision，不是 placement** |
| Al-Hraishawi et al., *Toward Practical HARQ-Based RC-LDPC Design...* | 2024 / IEEE TAES / `10.1109/TAES.2024.3434768` / published | ACK/NACK 与 HARQ 状态 | PBRL-LDPC incremental redundancy / retransmission | LEO FSO turbulence/cloud/pointing；abstract 未闭合 temporal-error placement | goodput / energy efficiency / average frame delay | `search-archive/_index/all-papers.jsonl:13311`；S2+OpenAlex abstract。**HARQ/AMC 邻域，不是 placement** |

### collision receipt

| collision 类别 | 可追溯证据 | 判断 |
|---|---|---|
| 旧 4b#1：fixed/deep/adaptive depth | `10.1109/TCOMM.2003.815052`（length）；`10.1364/OE.18.026978`（optimum depth）；`10.4028/www.scientific.net/AMR.571.382`（按 burst information 切换 depth）；`10.1117/12.826309`（可调硬件 length）；`10.3390/aerospace12100869`（CCSDS block depth benchmark） | 只改变 depth/B 的方向已有明确、连续且含在线 adaptive 的先例；必须标作旧 4b#1 collision，不能改名为 channel-aware placement。 |
| P08：receiver calibration/equalization/decoder | `10.1117/12.2599963`（estimated-CSI equalization）；`10.1186/s13638-023-02285-w`（LDPC decoder variant） | action 位于接收端观测/译码，不输出 interleaving/placement；即使改善 burst BLER 也不能算新任务 baseline。 |
| AMC / MCS / code-rate | `10.1109/ojcoms.2025.3538839`（预测 CSI 后选 LDPC rate）；`10.1109/jlt.2023.3242215`（按 CSI 选 modulation、mode power 与 MIMO decoder）；`10.1109/TAES.2024.3434768`（RC-LDPC IR-HARQ） | 输出是 rate/MCS/mode/冗余，不是 permutation/placement；归 AMC/HARQ collision。 |
| generic prior art | `10.1109/ACCESS.2020.2974002`（Rayleigh SPMM bit mapper）；`10.1109/TWC.2012.051712.111142`（block-fading precoding/mapping） | 证明“可靠性匹配 bit mapping / 跨 block precoding”不是空白，但不是 FSO task-matched comparator；只列 adjacent。 |

### 2019+ task-matched baseline 清单与不足

严格口径下，**达到 1 篇，未达到要求判断中的 2 篇**。

1. **Sun & Noh 2025, CCSDS O3K（严格 task-matched fixed baseline）**：同为 coded FSO、显式 time-correlated scintillation、以 block interleaver depth 改变 burst dispersion，并报告 BER/reliability。它提供 fixed/deep interleaving 的近期基线，但不执行在线 channel-aware permutation、parity placement 或 segmentation。

未升格为第 2 篇的近期 near-miss：

- **Clements et al. 2025** 有 FSO codeword interleaving，但摘要层证据只闭合 capacity/link-budget 架构比较，未闭合 temporal lifecycle、同输出和 BER/BLER metric。
- **Li et al. 2024** 有真实非平稳 LEO-to-ground、100 Hz scintillation 与 long interleaved frames，但交织、ECP 重传、AO 等作为工程系统 bundle 出现，缺少可归因的 comparator 设置。
- **Yamazaki et al. 2021** 处理 scintillation burst，但 action 是 CSI equalization（P08），不是 placement。
- **Fang et al. 2020 / Wang et al. 2022 / Gupta & Jain 2023** 分别是 shaping、空间相关 MIMO 或空间相关 receiver analysis；没有 temporal channel-aware placement 输出。
- **Göktepe et al. 2025 / Al-Hraishawi et al. 2024** 处理 coherence/LEO FSO，但 action 是 code-rate/IR-HARQ（AMC/HARQ）。

因此不能把“同为 coded FSO”或“提到 correlation/burst”当作 task match；第二篇严格 comparator 仍缺。

### 三种预卡形态的证据支持度

T002 未给出 A/B/C 的固定名称，以下仅按其三个非 depth 技术面作操作化映射，不改变主线命名：

| 预卡形态（本记录操作化） | 支持度 | 先例 / collision | 证据缺口 |
|---|---|---|---|
| A：固定 B 内、由 causal channel/burst state 驱动的 permutation / codeword mapping | **ADJACENT** | 2012 adaptive interleaving使用 burst information，但真实 action 仅为 depth；2020 SPMM 有 fixed mapping，但为 generic Rayleigh、离线 MI 设计 | 未发现 2019+ FSO 在固定 depth 下按 causal temporal state 输出 permutation 的 exact prior 或 task-matched baseline |
| B：按 code-bit role/reliability 做 parity/systematic/bit placement 到 fade/time slots | **ADJACENT** | 2020 SPMM 与 2012 block-fading precoding/mapping证明 generic reliability-aware mapping prior art；2020 polar-PAS 有 labeling/exchange | 未发现 FSO temporal-burst 条件下，以 parity/systematic placement 为真实输出且信息合法的论文；不能从 BICM/PAS 标题推成 exact support |
| C：按 coherence/burst duration 做 frame segmentation / codeword scheduling | **ADJACENT** | 2024 工程系统使用 long interleaved data frames；2025 capacity work比较 physical interleaving与 link-layer coding | 未发现可归因的、2019+、同信息同输出的 dynamic segmentation/scheduling comparator；现有证据多与 ARQ/架构选择捆绑 |

三形态均没有 **SUPPORTED** 级 exact evidence；也不标 **UNSUPPORTED**，因为每一形态都有相邻机制证据，但均存在 FSO temporal-task 接口缺口。该结论只是检索证据强度，不是保留/淘汰裁决。

### Step 2 CORE 候选与获取风险

| 优先级 | identity | Step 2 用途 | 获取风险（本批不下载） |
|---:|---|---|---|
| 1 | `10.3390/aerospace12100869` | 唯一严格 2019+ fixed/deep task-matched baseline；核对 O3K interleaver mapping、depth、OU lifecycle 与 BER 设置 | **低**：OA；当前 S2/OpenAlex abstract 已闭合核心身份，后续需精读确认具体 permutation 与强湍流参数 |
| 2 | `10.1117/12.3041270` | physical codeword interleaving vs link-layer coding 的近期架构边界/理论 comparator | **中**：SPIE proceedings 可能受限；abstract 不能确认 temporal generator、interleaver 实现和 BER 对比 |
| 3 | `10.1016/j.xinn.2023.100557` | 真实 LEO-to-ground long-interleaved-frame 工程 anchor；核对 frame segmentation、ECP 与可归因性 | **低**：OA；风险主要是系统 bundle 无消融，不是访问 |
| 4 | `10.4028/www.scientific.net/AMR.571.382` | adaptive-depth exact collision；核对 burst estimator、depth switching 与信息时序 | **高**：老会议/出版平台，可能仅摘要可得；但 collision 的真实 action 已由 S2 abstract 明确 |
| 5 | `10.1109/ACCESS.2020.2974002` | generic reliability-aware bit-mapper prior art；限定 novelty wording，不能当 FSO baseline | **低**：IEEE Access OA；任务迁移风险高于访问风险 |

## 结论

1. 四组 query 已闭合，结果为 **20 / 7 / 20 / 0**；第 4 组零命中没有触发第 5 组。
2. 2019+ 严格 task-matched baseline **只有 1 篇，未达到 2 篇**：Sun & Noh 2025 CCSDS O3K fixed block-interleaving benchmark。
3. depth/B 路线存在 2003、2009、2010、2012、2025 的连续 prior art，其中 2012 已是 burst-information-driven adaptive depth，构成旧 4b#1 exact collision。
4. 近期 coded FSO 命中主要落在 channel equalization/decoder（P08）、PAS/空间相关 coding、code-rate/MCS/IR-HARQ（AMC/HARQ）或工程长帧；它们不能替代同任务、同信息、同输出 comparator。
5. A/B/C 三种非 depth 形态当前都只能标 **ADJACENT**：存在 generic 或工程先例，但没有摘要级证据支持 2019+ FSO temporal-correlated 条件下的 exact channel-aware placement comparator。

## 对决策的影响

本记录不新建决策，也不作方法保留/淘汰。它只给 Step 2 提供两个边界：一是固定/depth interleaving 必须纳入 2025 CCSDS O3K baseline 与 2012 adaptive-depth collision；二是若后续需要“至少 2 篇 2019+ task-matched comparator”作为门槛，当前证据尚未满足，不能用 capacity-only、engineering bundle、spatial correlation、P08 或 AMC/HARQ 文献凑数。
