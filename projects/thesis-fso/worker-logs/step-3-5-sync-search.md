# Step 3.5 Q1 keyword-matrix search

> 2026-08-06 | 仅执行 T005 | 未修改 canonical 状态、代码或实验 | 未提交

## 执行环境与命令

- worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- 工具：`bash tools/search`；请求源为 `s2 openalex arxiv`，每源最多 20 条、最终最多 50 条。
- 实际归档结果来源覆盖 `semantic_scholar` 与 `openalex`；arXiv 本轮没有直接返回记录，但已有条目的 arXiv ID 仍由元数据保留。
- 所有指定输出均在 `search-archive/2026-08-06/step35-r1-*.json`。工具另按 query slug 自动生成同日归档并增量维护全局论文索引。
- 执行命令模板：

```bash
bash tools/search "<query>" --sources s2 openalex arxiv --max-per-source 20 --top 50 \
  --output "search-archive/2026-08-06/<archive>.json" --format json
```

- 确定性去重：优先规范化 DOI，其次 arXiv ID，最后规范化标题。六个 JSON 共 100 条 archive rows，跨 query 去重后 80 篇。
- `raw/unique` 下文定义为“该 JSON 中的归档结果行 / 该文件内按上述键去重结果”。provider 原始召回数和低相关过滤前数量未写入 JSON，因此不补猜。
- 15 分钟搜索止损到达后未再发任何搜索请求；Round 2/3 未启动。

## 关键词矩阵

| 方法变体 | burst/frame acquisition | fractional timing + CFO |
|---|---|---|
| joint ML / likelihood | `joint maximum likelihood burst synchronization frame timing frequency offset coherent optical` | `joint maximum likelihood fractional timing carrier frequency offset preamble burst` |
| multidimensional metric / ambiguity search | `multidimensional correlation frame synchronization timing frequency offset coherent optical` | `ambiguity function joint time frequency synchronization burst mode optical communication` |
| training sequence / preamble | `training sequence joint frame clock frequency synchronization coherent optical receiver` | `preamble simultaneous frame timing carrier frequency offset burst synchronization` |

矩阵满足 3 类方法变体、每类 2 个组合，共 6 个组合。这里的关键词只用于召回；标题中的 `joint` 不等于 joint `(frame, τ, CFO)` action。

## Round 1

| query | sources | archive JSON | raw/unique | new must/should |
|---|---|---|---:|---:|
| joint maximum likelihood burst synchronization frame timing frequency offset coherent optical | S2/OpenAlex/arXiv | `step35-r1-ml-frame-timing-cfo.json` | 31/31 | 3/4 |
| joint maximum likelihood fractional timing carrier frequency offset preamble burst | S2/OpenAlex/arXiv | `step35-r1-ml-frac-timing-cfo.json` | 20/20 | 0/0 |
| multidimensional correlation frame synchronization timing frequency offset coherent optical | S2/OpenAlex/arXiv | `step35-r1-corr-frame-timing-cfo.json` | 13/13 | 0/1 |
| ambiguity function joint time frequency synchronization burst mode optical communication | S2/OpenAlex/arXiv | `step35-r1-ambiguity-burst-time-frequency.json` | 2/2 | 0/0 |
| training sequence joint frame clock frequency synchronization coherent optical receiver | S2/OpenAlex/arXiv | `step35-r1-training-frame-clock-cfo.json` | 14/14 | 1/1 |
| preamble simultaneous frame timing carrier frequency offset burst synchronization | S2/OpenAlex/arXiv | `step35-r1-preamble-frame-timing-cfo.json` | 20/20 | 1/0 |
| **Round 1 合计** | 3 requested / 2 actual result APIs | 6 JSON | **100 rows / 80 cross-query unique** | **5/6** |

“新增”按上述 query 顺序首次出现计数，避免同一 DOI 跨 query 重复计入。Round 1 新增必读/建议读不是 0，故不能称收敛。

## Round 2

未启动。15 分钟执行上限到达后，主线明确要求停止所有新搜索请求，仅基于已落盘 JSON 收口。

## Round 3

未启动。同上；没有用无信息增量重试机械消耗轮次。

## 候选表

以下 action 分类只使用归档 abstract；`acquire/read=是` 表示必须取得正文后才能裁 exact-action collision。

| title | year | DOI/arXiv | abstract-supported action | class | relevance | acquire/read |
|---|---:|---|---|---|---|---|
| Joint time-frequency domain feature exploitation for a single burst-mode preamble in a next-generation coherent optical access network | 2026 | `10.1364/JOCN.587273` | 同一 preamble：频域 clock recovery；时域 frame sync、FOE、SOP | shared-preamble/resource reuse；clock 与 frame/FOE 分域 | **必读**：最近高风险直接竞品 | 是 |
| Preamble Design for Online IQ-Skew Estimation in Upstream 400G Coherent TFDM-PON | 2025 | `10.1109/JLT.2025.3581618` | training sequence 同时支持 frame detection、timing recovery、FOE、SOP 与 IQ-skew | 同资源多功能；是否单一联合 estimator 摘要不能裁 | **必读**：动作集合最接近 | 是 |
| Discrete FRFT-Based Frame and Frequency Synchronization for Coherent Optical Systems | 2017 | `10.1109/LPT.2017.2759584`; arXiv `1801.01598` | chirp TS + fractional cross-correlation，解 timing offset 与 CFO；题名声称 joint frame/frequency | 可能 direct joint metric；`timing offset` 是否 fractional symbol τ 待正文 | **必读**：潜在 exact-action 先例 | 是 |
| An Optimum Signal Detection Approach to the Joint ML Estimation of Timing Offset, Carrier Frequency and Phase Offset for Coherent Optical OFDM | 2021 | `10.1109/JLT.2020.3042546` | joint ML 输出 TO、CFO、CPO，并与 CFO-first sequential 版本比较 | 真 joint `(τ,CFO,phase)`，但无 frame 输出且 waveform 为 CO-OFDM | **必读**：核心方法先例 | 是 |
| Neural network (ConvNN and CapNN) based joint synchronization of timing and frequency for CO-OFDM system | 2024 | `10.1007/s11082-024-06850-5` | ConvNN/CapNN 联合 timing 与 carrier-frequency offset | 真 joint `(τ,CFO)` 候选；无 frame、QNSC CO-OFDM | **必读**：近期 estimator 先例 | 是 |
| Burst-Mode Synchronization for SOQPSK | 2019 | `10.1109/TAES.2019.2893816` | data-aided ML 联合 frequency、phase、timing；无 joint frame output | 真 joint `(τ,CFO,phase)`，不同调制/信道 | 建议读 | 建议 |
| Timing, Carrier, and Frame Synchronization of Burst-Mode CPM | 2013 | `10.1109/TCOMM.2013.111613.130667`; arXiv `1310.0757` | timing/carrier joint ML；frequency grid 后 timing/phase 闭式；frame detector 另列 | timing/carrier 联合 + frame sequential | 建议读 | 建议 |
| Efficient Timing/Frequency Synchronization Based on Sparse Fast Fourier Transform | 2019 | `10.1109/JLT.2019.2932075` | coarse timing/frequency 后分别 fine timing、fine frequency | sequential/coarse-to-fine optical comparator | 建议读 | 建议 |
| Training-aided joint frame and frequency synchronization for free space optical communication signals with low OSNR | 2020 | `10.1016/j.optcom.2020.126046` | low-OSNR FSO joint frame/frequency synchronization | direct FSO frame+CFO；无 fractional timing | 建议读 | 建议 |
| Efficient preamble scheme for burst-mode detection in coherent TFDM-PON | 2025 | `10.1364/OE.578683` | 同一 training unit 实现 frame、fine FOE、polarization、channel estimation | generic shared-resource；无 timing recovery | 建议读：资源复用边界 | 建议 |
| Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems | 2025 | `10.1109/LPT.2024.3523478` | joint STO+CPE，适用于 fiber/FSO CO-OFDM | FSO joint timing+phase；无 frame/CFO | 建议读：邻近动作 | 建议 |

已知 CORE `10.1109/JLT.2025.3533197` / arXiv `2409.14400` 在多 query 重复出现，但不是新候选；摘要仍只支持同一 training unit 的 frame/FOE/channel reuse，不支持 exact joint `(frame,τ,CFO)`。

## 三类语义边界

1. **generic shared-preamble/resource reuse**：同一 TS/preamble 承载多种估计功能，但各功能可在不同域、不同阶段或不同模块执行。JOCN 2026、OE 2025、Sun 2025 明确落在该类；JLT 2025 IQ-skew 论文仅凭摘要也只能先归此类，不能升级为联合 estimator。
2. **sequential timing/frame/CFO**：一个完整 receiver 依次做 coarse CFO、timing/interpolation、frame、fine CFO，或 coarse joint 后再各自 fine。Le Bidan 2023 与 JLT 2019 S-FFT 是此类代表；CPM 2013 也是 timing/carrier 联合但 frame 另行检测。
3. **真正 joint estimator**：同一 objective/metric 在同一 receiver-known sample set 上直接输出耦合参数。JLT 2021、OQE 2024、TAES 2019 的摘要支持 joint `(τ,CFO[,phase])`，但都没有同时输出 frame；LPT 2017 FRFT 最接近 `(frame/timing,CFO)`，却必须读正文确认其 timing offset 是 burst/frame timing 还是 sample-level fractional symbol τ。当前 abstract 集合**没有足够证据确认**任何同信息、同动作、同任务的 exact joint `(frame,τ,CFO)` estimator。

## 收敛与未覆盖项

- 关键词矩阵：**6/6 完成**。
- 搜索源：请求 3 源；实际有结果的 API 为 S2 与 OpenAlex，满足至少两源。arXiv 本轮无直接命中。
- Round：只执行 **1 轮**；Round 2/3 因 15 分钟止损未启动。
- 收敛：**未收敛**。最后执行轮新增 `must=5 / should=6`，不满足“最后一轮新增必读/建议读=0”。
- 未覆盖：
  - 11 篇 must/should 的正文 action-level 核验，尤其 `10.1364/JOCN.587273`、`10.1109/JLT.2025.3581618`、`10.1109/LPT.2017.2759584`；
  - 最高相关竞品的双向引用链（属于 T006/后续动作，本 T 未启动）；
  - 以正文确认 `timing offset` 是否为 sample-level fractional τ，以及 frame index 是否由同一 metric 直接输出；
  - Round 2/3 的同义词补洞与“新增=0”验证。

## 结论（只陈述检索事实，不做 Step 4a 判断）

Round 1 的 6-query 矩阵从 100 条归档行中得到 80 篇跨 query unique，摘要筛出 5 篇必读、6 篇建议读。现有摘要清楚显示三种不同语义：共享 preamble 多功能复用、顺序/coarse-to-fine 同步链、以及不含 frame 输出的 joint timing/CFO estimator。LPT 2017 FRFT 与 JLT 2025 IQ-skew preamble 是最需要全文核验的潜在动作碰撞；JOCN 2026 摘要则明确支持分域资源复用。由于没有执行到“新增为 0”的最后一轮，本文档不声称竞争闭包，也不声称 exact-action novelty/collision。
