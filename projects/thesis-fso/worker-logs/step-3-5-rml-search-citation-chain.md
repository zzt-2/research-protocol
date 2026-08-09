# Step 3.5 RML-FSTS 关键词矩阵与双向引用链

> 2026-08-09 | 来源：`.sessions/2026-08-08-rml-fsts-groundwork/T003-step3-5-search-and-citation-chain.md`
> 边界：仅做检索、引用链和 abstract/metadata 初筛；不进入 Step 4a，不做方法设计或终判。

## 关键词矩阵执行表

下表 `actual sources` 只统计最终 JSON 结果条目的 `source_api/source_apis`，不把配置的 `s2/openalex/serpapi/exa` 当作实际来源。8/8 查询均从目标 worktree 根目录实际运行 `bash tools/search "..." --mode academic`。

| ID | 冻结 query（方法变体 × 场景） | raw JSON | 命中 | actual sources | 错误/降级 |
|---|---|---|---:|---|---|
| Q1A | `FSTS fixed lag BL carrier frequency offset estimation coherent FSO training-aided FOE frame synchronization turbulence spatial diversity` | `search-archive/2026-08-09/rml-fsts-q1a.json` | 1 | SerpAPI + S2 | Exa 402/timeout；OpenAlex 0 |
| Q1B | `FSTS fixed lag BL carrier frequency offset estimation modulation training length received power branch phase reliability online selection lookup` | `search-archive/2026-08-09/rml-fsts-q1b.json` | 5 | SerpAPI | Exa 402；S2/OpenAlex 0 |
| Q2A | `multi-lag CFO estimation correlation distance weighting coherent FSO training-aided FOE frame synchronization turbulence spatial diversity` | `search-archive/2026-08-09/rml-fsts-q2a.json` | 0 | 无 retained source | Exa 402；S2/OpenAlex/SerpAPI 无 retained result |
| Q2B | `multi-lag CFO estimation correlation distance weighting modulation training length received power branch phase reliability online selection lookup` | `search-archive/2026-08-09/rml-fsts-q2b.json` | 1 | SerpAPI | Exa 402；S2/OpenAlex 0 |
| Q3A | `adaptive variable lag window correlation distance frequency offset coherent FSO training-aided FOE frame synchronization turbulence spatial diversity` | `search-archive/2026-08-09/rml-fsts-q3a.json` | 1 | SerpAPI | Exa 402；S2/OpenAlex 0 |
| Q3B | `adaptive variable lag window correlation distance frequency offset modulation training length received power branch phase reliability online selection lookup` | `search-archive/2026-08-09/rml-fsts-q3b.json` | 19 | SerpAPI + OpenAlex | Exa 402；S2 摘要补全限速；大量跨域假阳性 |
| Q4A | `condition-aware reliability-weighted multi-lag carrier recovery coherent FSO training-aided FOE frame synchronization turbulence spatial diversity` | `search-archive/2026-08-09/rml-fsts-q4a.json` | 0 | 无 retained source | Exa 402；S2/OpenAlex/SerpAPI 无 retained result |
| Q4B | `condition-aware reliability-weighted multi-lag carrier recovery modulation training length received power branch phase reliability online selection lookup` | `search-archive/2026-08-09/rml-fsts-q4b.json` | 0 | 无 retained source | OpenAlex 原始 4 条均被相关性门过滤；Exa 402；其余无 retained result |

矩阵共返回 27 条。跨全部矩阵和引用链，实际 retained source family 为 `SerpAPI`、`OpenAlex`、`S2` 三类，满足至少两个实际 source family。并发运行时全局索引临时文件发生一次竞态警告；12 个显式 raw JSON 均正常落盘，不影响本任务 receipt，但本轮不据此宣称全局索引更新完整。

## 搜索轮次

### R1 新增

- **新增必读 3 篇**：Robust multifunctional single-tone TS（2025）、Optimized short-symbol-block FOE（2024）、低接收功率下星地 joint FS/FOE（2026，exact-collision candidate，尚未确认 action）。
- **新增建议读 3 篇**：short-time-spectrum coarse FOE（2024）、low-complexity/robust coherent scheme（2025）、joint OSNR/FO spectrum-correlation（2021）。
- **既有债务再命中 2 篇（不计新增）**：Cheng 2020 low-OSNR direct comparator、Dong 2009 multi-correlation-lag。

R1 的新增“必读/建议读”合计为 6，不满足“最后一轮新增=0”的收敛条件。因此本记录**不宣称竞争闭包**。需要 bounded R2：优先取得/核验上述 6 篇的全文或至少 DOI/API abstract，判定 SSRN 2026 是否真的执行 condition→lag/`B_L` action、2024 optimized short-block 是否只是 dev-frozen parameter optimization，以及另外 4 篇是否仅为 estimator/TS architecture adjacent。T003 禁止增加第 9 个语义查询，本执行任务在此停止，不自行无限开 R2。

## Citation chain coverage

| Seed | 方向 | raw JSON | 返回（工具去重后） | 本链 screened | OpenAlex provenance | S2 provenance | S2-only |
|---|---|---|---:|---:|---:|---:|---:|
| Wang 2023 `10.1109/JPHOT.2023.3265847` | forward | `rml-fsts-cite-wang2023-forward.json` | 8 | 8 | 8 | 3 | 0 |
| Wang 2023 `10.1109/JPHOT.2023.3265847` | backward | `rml-fsts-cite-wang2023-backward.json` | 30 | 30 | 30 | 0（backward 由工具跳过 S2） | 0 |
| Enhanced 2024 `10.1364/OE.520452` | forward | `rml-fsts-cite-enhanced2024-forward.json` | 2 | 2 | 2 | 2 | 0 |
| Enhanced 2024 `10.1364/OE.520452` | backward | `rml-fsts-cite-enhanced2024-backward.json` | 23 | 23 | 23 | 0（backward 由工具跳过 S2） | 0 |

四链合计 63 条，按 DOI（缺 DOI 时按规范化 title）跨链去重后为 51 条，全部完成 title/DOI/year/source/abstract-or-metadata 初筛。OpenAlex 是严格主链；本次 union 后没有 S2-only 条目，故没有把未交叉验证的 S2-only 召回计作 verified citation。两条 forward 中同时带 OpenAlex+S2 provenance 的条目仍以 OpenAlex 严格链身份使用。

## 候选表（≤10）

`abstract-supported relevance` 只陈述 raw JSON 的 abstract/metadata 能支持的事实；空摘要只按标题召回，不作功能终判。

| # | Title | DOI | Year | Source chain | Abstract-supported relevance | Classification | Fulltext needed |
|---:|---|---|---:|---|---|---|---|
| 1 | Robust multifunctional single-tone training sequence for free-space optical communication in strong turbulence | `10.1364/OE.561252` | 2025 | Wang forward / OpenAlex | 摘要支持：强湍流低接收功率下提出 FOE 与单训练序列分支相位校正，并在 10-Gbaud DP-QAM 仿真链验证。未支持 condition-aware lag/`B_L` selection。 | architecture adjacent；新增必读 | 是：确认 estimator、lag/window 与 comparator |
| 2 | Optimized Frequency Offset Estimation Scheme Using Short Symbol Block Based on Training Sequence for Coherent Free-Space Optical Communication | `10.1109/ACP/IPOC63121.2024.10809664` | 2024 | Wang forward / OpenAlex+S2 | 摘要支持：单 short symbol block 完成 FOE，声称 residual FOE complexity 约为 FSTS 的 17%；未说明按 receiver condition 在线选参。 | offline parameter optimization；新增必读 | 是：确认 block length 是否 dev-frozen、比较条件与公式 |
| 3 | Joint frame synchronization and frequency offset estimation for satellite-to-ground optical communication under low received optical power | `10.2139/SSRN.6293357` | 2026 | Wang forward + Q3A / OpenAlex+SerpAPI | 仅标题支持 low received power 下的星地 joint FS/FOE；raw JSON 无 abstract，不能确认是否选择 lag/`B_L`。 | exact-collision candidate（未确认）；新增必读 | **必须**：无 abstract，需全文/正式 metadata 终判 action |
| 4 | Coarse frequency offset estimation and compensation based on short-time spectrum analysis in FSO communication system | `10.1016/J.OPTCOM.2024.130981` | 2024 | Wang forward / OpenAlex+S2 | 仅标题支持 FSO coarse FOE/compensation 的 short-time-spectrum architecture；raw JSON 无 abstract。 | architecture adjacent；新增建议读 | 是：确认与 FSTS 的接口及是否受 condition 驱动 |
| 5 | A coherent communication scheme characterized by low complexity and enhanced robustness | `10.1109/ICAIT66450.2025.11353316` | 2025 | Wang forward / OpenAlex+S2 | 摘要支持：专门训练序列用于 FOE，10-Gbaud PM-QPSK FSO 仿真，报告约 1.9 dB sensitivity improvement；未支持 target action。 | architecture adjacent；新增建议读 | 是：确认 reference methods、TS/FOE 结构和条件扫描 |
| 6 | Joint OSNR and Frequency Offset Estimation Using Signal Spectrum Correlations | `10.1109/JLT.2021.3063251` | 2021 | Enhanced backward / OpenAlex | 摘要支持：spectrum correlation 联合 OSNR/FO，coarse compensation 后用 down-sampling FFT 做 fine FOE；是 fiber B2B，不是 FSO conditioned controller。 | architecture adjacent；新增建议读 | 是：只在需要排除 spectrum-correlation cheap alternative 时读取 |
| 7 | Training-aided joint frame and frequency synchronization for free space optical communication signals with low OSNR | `10.1016/J.OPTCOM.2020.126046` | 2020 | 两 seed backward / OpenAlex | 仅标题支持 low-OSNR FSO joint frame/frequency synchronization；raw JSON 无 abstract。 | architecture adjacent / task-matched debt；既有债务 | **必须**：直接竞品债务，metadata 不足以承重 |
| 8 | Implementation of training-sequence based carrier frequency offset estimator with multi-correlation-lag | `10.1109/CHINACOM.2009.5339877` | 2009 | Q2B / SerpAPI（DOI 由既有 owner identity 补全） | 摘要支持：training-sequence CFO estimator 使用 multiple correlation lags，并突破单 lag 的 length constraint；未支持 condition-aware selection。 | generic multi-lag；既有债务 | **必须**：确认 weighting、lag set、online/offline 与碰撞边界 |

本轮没有 abstract/metadata 足以支持“condition→在线/分区选择 lag、`B_L` 或 correlation distance”的 confirmed exact collision，也没有确认 conditioned lookup equivalent。第 3 条只保留为 exact-collision candidate，不能当作已碰撞。

## 未入选类别统计

90 条 raw records 按 DOI/title 合并为 78 条 unique，候选 8，未入选 70。以下按主排除理由作互斥人工标签：

| 主排除理由 | 数量 | 说明 |
|---|---:|---|
| 矩阵跨域/词面假阳性 | 20 | 电力电子、IoT、声学 OFDM、一般 link adaptation 等，不是 coherent-FSO carrier recovery |
| 经典/通用 estimator 与同步基础、无 target action | 30 | 可作背景引用，但没有 receiver-condition→lag/`B_L` 动作，也非本轮优先直接竞品 |
| FSO turbulence/phase/combining 物理邻接、无 target FOE-lag control | 13 | 支持场景物理，不支持 exact action |
| 已知 seed 或 index artifact | 3 | Wang 2023、Enhanced 2024 与 IEEE Photonics Journal index |
| 近期但更远的 architecture adjacent / 与高优先候选重复 | 4 | 不足以挤入 ≤10 候选，保留在 raw JSON 可追溯 |

分类边界明确：`generic multi-lag` 不等于 conditioned controller；固定 short block/固定参数优化归入 `offline parameter optimization`；只有实际按 receiver-visible condition 选择固定参数表才可归 `conditioned lookup equivalent`；TS、FFT、spectrum 或 estimator 结构变化而没有该动作的归 `architecture adjacent`。

## 边界

- 这是 R1 检索和 citation-screen receipt，不是 Step 3.5 terminal；因为新增 must/should=`3/3`，仍需 bounded R2。
- abstract/metadata 只用于召回和初筛，不用于 exact action、novelty、公式、实现或比较公平性的终判。
- 未进入 Step 4a；未设计方法；未运行 smoke、仿真或 MVE；未触碰 p05 日志、topic、literature、decisions。
- Exa 额度耗尽、SerpAPI 部分 key 无结果/无效、S2 摘要补全限速及并发索引竞态均已写入 receipt；本轮 raw JSON 本身已完成并有 SHA256。
