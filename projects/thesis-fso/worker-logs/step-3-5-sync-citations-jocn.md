# Step 3.5 citation chains and JOCN acquisition

> 日期：2026-08-06
> 任务：T006
> 范围：Sun 2025 双向一跳引用链 + JOCN 2026 有界合法获取；不进入 Step 4a，不实现、不仿真、不改 canonical 状态。

## 前向引用链

- 命令：`bash tools/search --citations '10.1109/JLT.2025.3533197' --citations-direction forward --citations-depth 1 --citations-source both --output 'search-archive/2026-08-06/sun-2025-forward-citations.json' --format json`
- 规模：8 条去重记录；OpenAlex 8 条，S2 4 条，union 后仍为 8 条。
- citation provenance：8/8 均含 `openalex_citations`，其中 4 条还含 `s2_citations`；**S2-only=0**。因此本表的 `verified citation=yes` 仅表示 OpenAlex 严格引用图确认“引用 Sun 2025”，不表示已核验各论文的全文动作。
- 存档：`search-archive/2026-08-06/sun-2025-forward-citations.json`，13,336 bytes，SHA256 `95e8e3bed747256c68c3f174d3f60a610cc3730e39020445307a2623fcba6f80`。

| title | year | DOI/arXiv | direction/source | verified citation | action class | relevance |
|---|---:|---|---|---|---|---|
| Partial Transmit Subcarrier Technology Based on m-Sequence for Simplified PAPR Reduction in 400G TFDM Coherent PON | 2025 | `10.1109/JLT.2025.3603788` | forward/OpenAlex | yes | PAPR reduction；非同步动作 | 无关 |
| Polarization-independent preamble design in Alamouti code-based simplified coherent system for PON downstream | 2025 | `10.1364/OE.566136` | forward/OpenAlex | yes | 同一 preamble 支持 FS、FOE、CE；摘要未含 clock/timing | 中高：直接 preamble 邻居，但非 timing/frame/CFO 全动作 |
| Cost-effective and Flexible Coherent Optics for Next-Generation Optical Access Networks | 2025 | `10.1109/ECOC66593.2025.11263143` | forward/OpenAlex+S2 | yes | 综述/系统路线 | 低 |
| Cost-effective and flexible coherent passive optical networks [Invited] | 2026 | `10.1364/JOCN.590228` | forward/OpenAlex+S2 | yes | 综述/成本与灵活性 | 低 |
| Joint time-frequency domain feature exploitation for a single burst-mode preamble in a next-generation coherent optical access network | 2026 | `10.1364/JOCN.587273` | forward/OpenAlex+S2 | yes | single preamble；频域 clock recovery，时域 FS/FOE/SOP；摘要未解析耦合关系 | **最高：exact-action 高风险 blocker** |
| Hardware-Efficient Optical Frequency Comb-Based Self-Homodyne Joint WDM-SDM Reception | 2026 | `10.2139/SSRN.6954091` | forward/OpenAlex | yes | WDM-SDM self-homodyne reception；无同步摘要 | 无关 |
| Short-Preamble DSP for Downstream Alamouti Coherent-Lite PON Using Gear-Shifted LMS Equalization | 2026 | `10.3390/photonics13080695` | forward/OpenAlex+S2 | yes | preamble 后的 equalizer acquisition / warm start | 低：明确假定 preamble synchronization 已完成 |
| Fast-Reconfigurable Metro-Access Networks using SOA-based OADM Node and Burst-Mode Coherent Receiver | 2026 | `10.1364/CLEO_SI.2026.STh4F.2` | forward/OpenAlex | yes | 70 ns preamble 的 burst receiver；摘要无具体同步动作 | 低 |

**前向结论**：没有新增全文级证据证明单一 `(frame, fractional timing/SCO, CFO)` 联合 estimator。JOCN 2026 是最直接的多动作碰撞项；OE 2025 是 FS/FOE/CE 的中高相关邻居，但摘要不含 clock/timing。

## 后向引用链

- 命令：`bash tools/search --citations '10.1109/JLT.2025.3533197' --citations-direction backward --citations-depth 1 --citations-source both --output 'search-archive/2026-08-06/sun-2025-backward-citations.json' --format json`
- 规模：35 条去重记录。该方向由 OpenAlex 覆盖，S2 按工具契约跳过；35/35 为 OpenAlex strict reference graph。
- 存档：`search-archive/2026-08-06/sun-2025-backward-citations.json`，53,738 bytes，SHA256 `eb7cd674ce0a9183198918f559996e0fd1c927e672bb86ff055b7ba9d3167792`。
- 本地全文交叉核对：Sun arXiv 全文参考文献明确包含 `10.1364/JOCN.402591`、`10.1109/JLT.2023.3243828`、`10.1109/JLT.2014.2358933`、`10.1109/26.554282`（`papers/arxiv/2409.14400/content.md:447-463`）。OFC 2024 为同一 Sun 工作的会议前身（`:457` 附近）。

| title | year | DOI/arXiv | direction/source | verified citation | action class | relevance |
|---|---:|---|---|---|---|---|
| Phase shift pulse codes with good periodic correlation properties | 1961 | `10.1109/TIT.1961.1057655` | backward/OpenAlex | yes | polyphase perfect periodic correlation / synchronization foundation | 中：序列理论基础，非 estimator 竞品 |
| Data-aided frequency estimation for burst digital transmission | 1997 | `10.1109/26.554282` | backward/OpenAlex + local ref | yes | clock-aided feedforward burst FOE | 高：FOE 的早期技术基础；不联合估计 timing |
| Progress of ITU-T higher speed passive optical network (50G-PON) standardization | 2020 | `10.1364/JOCN.391830` | backward/OpenAlex | yes | 标准化背景 | 无关 |
| Digital subcarrier multiplexing for fiber nonlinearity mitigation in coherent optical communication systems | 2014 | `10.1364/OE.22.018770` | backward/OpenAlex | yes | SCM / nonlinearity | 无关 |
| The Outlook for PON Standardization: A Tutorial | 2019/2020 | `10.1109/JLT.2019.2950889` | backward/OpenAlex | yes | PON 标准综述 | 无关 |
| Beyond 100 Gb/s: Capacity, Flexibility, and Network Optimization | 2017 | `10.1364/JOCN.9.000C12` | backward/OpenAlex | yes | 网络/收发机综述 | 低 |
| 50G-PON: The First ITU-T Higher-Speed PON System | 2022 | `10.1109/MCOM.001.2100441` | backward/OpenAlex | yes | PON 系统背景 | 无关 |
| Coherent Passive Optical Networks for 100G/lambda-and-Beyond Fiber Access: Recent Progress and Outlook | 2022 | `10.1109/MNET.005.2100604` | backward/OpenAlex | yes | coherent PON 综述，提及 burst DSP | 低 |
| Efficient preamble design and digital signal processing in upstream burst-mode detection of 100G TDM coherent-PON | 2020/2021 | `10.1364/JOCN.402591` | backward/OpenAlex + local ref | yes | single designed unit 支持 FS、SOP、FOE | **高：早期多动作 preamble 基线；无 timing** |
| Coherent Passive Optical Networks: Why, When, and How | 2021 | `10.1109/MCOM.010.2100503` | backward/OpenAlex | yes | coherent PON 综述 | 低 |
| Strategies for economical next-generation 50G and 100G passive optical networks [Invited] | 2019/2020 | `10.1364/JOCN.12.000A95` | backward/OpenAlex | yes | PON 路线 | 无关 |
| Flexible Coherent Optical Access: Architectures, Algorithms, and Demonstrations | 2024 | `10.1109/JLT.2024.3355443` | backward/OpenAlex | yes | coherent access 综述/算法图景 | 中低：背景入口，不是直接动作证据 |
| Fast-Convergence Digital Signal Processing for Coherent PON Using Digital SCM | 2023 | `10.1109/JLT.2023.3243828` | backward/OpenAlex + local ref | yes | TS + data-aided DSP 快速收敛；摘要未列各同步输出 | 中：preamble/DSP 机制邻居，exact action 未决 |
| Demonstration of PS-QAM Based Flexible Coherent PON in Burst-Mode with 300G Peak-Rate | 2022 | `10.1109/JLT.2022.3157738` | backward/OpenAlex | yes | flexible PON system | 低 |
| TDM-PON-Based Optical Access Network for Tactile Internet, 5G, and Beyond | 2022 | `10.1109/MNET.008.2100641` | backward/OpenAlex | yes | 网络场景 | 无关 |
| Point-to-Multipoint Coherent Architecture with Joint Resource Allocation for B5G/6G Fronthaul | 2022 | `10.1109/MWC.004.2100528` | backward/OpenAlex | yes | resource allocation；“joint”非同步动作 | 无关 |
| First Real-time Demonstration of 200G TFDMA Coherent PON using Ultra-simple ONUs | 2023 | `10.1364/OFC.2023.M3G.2` | backward/OpenAlex | yes | 系统 demo | 低 |
| CAZAC sequence and its application in LTE random access | 2006 | `10.1109/ITW2.2006.323692` | backward/OpenAlex | yes | CAZAC correlation / preamble detection / time synchronization | 中：序列与检测技术基础 |
| Training-Aided Frequency-Domain Channel Estimation and Equalization for Single-Carrier Coherent Optical Transmission Systems | 2014 | `10.1109/JLT.2014.2358933` | backward/OpenAlex + local ref | yes | CAZAC TS；FD CE/equalization；对 time misalignment 与 FO 鲁棒 | 中高：Sun CE/TS 直接基础，非 joint sync estimator |
| Demonstration of Real-Time Burst-Mode Digital Coherent Reception With Wide Dynamic Range in DSP-Based PON Upstream | 2016 | `10.1109/JLT.2016.2637357` | backward/OpenAlex | yes | frame detection + burst receiver | 中低 |
| Meeting the Traffic Requirements of Residential Users in the Next Decade with Current FTTH Standards | 2019 | `10.1109/MCOM.2018.1800173` | backward/OpenAlex | yes | traffic / upgrade | 无关 |
| Optical Strategies for Economical Next Generation 50 and 100G PON | 2019 | `10.1364/OFC.2019.M2B.1` | backward/OpenAlex | yes | PON strategy | 无关 |
| Flexible and adaptive coherent PON for next-generation optical access network [Invited] | 2022/2023 | `10.1016/J.YOFTE.2022.103190` | backward/OpenAlex | yes | flexible coherent PON 综述 | 低 |
| Rate-Flexible Single-Wavelength TFDM 100G Coherent PON based on Digital Subcarrier Multiplexing Technology | 2020 | `10.1364/OFC.2020.W1E.5` | backward/OpenAlex | yes | TFDM architecture | 无关 |
| Ultra-fast RSOP tracking via 3 pilot tones for short-distance coherent SCM systems | 2021 | `10.1364/OE.419574` | backward/OpenAlex | yes | RSOP + phase noise tracking | 低：carrier/polarization 邻居，无 timing/frame |
| Burst-Mode Digital Signal Processing for Coherent Optical Time-Division Multiple Access | 2025 | `10.1109/JLT.2025.3528909` | backward/OpenAlex | yes | designed preamble fast estimates SOP、FO、sampling-phase offset、sync position、equalizer | **最高的新直接候选**；摘要未说明单一联合 objective/输出耦合 |
| Burst-Mode Signal Reception for 200 G Coherent Time and Frequency Division Multiplexing Passive Optical Network | 2024 | `10.1109/JLT.2024.3431668` | backward/OpenAlex | yes | data-aided burst DSP，粗细滤波 + CE | 中：burst acquisition 邻居，摘要未列 timing/frame/CFO 联合动作 |
| Pilot-Tone Assisted Successive Interference Cancellation for Uplink Power- and Frequency-Division Multiplexing Passive Optical Network | 2022 | `10.1109/JLT.2022.3163160` | backward/OpenAlex | yes | FO + phase-noise estimation for overlapping uplinks | 低 |
| Demonstration of Pilot-Aided Continuous Downstream Digital Signal Processing for Multi-Format Flexible Coherent TDM-PON | 2024 | `10.1109/JLT.2023.3320905` | backward/OpenAlex | yes | pilot tracking SOP/equalizer/carrier phase | 低 |
| Some unique properties and applications of perfect squares minimum phase CAZAC sequences | 1992（OpenAlex 字段误标 2003） | `10.1109/COMSIG.1992.274294` | backward/OpenAlex | yes | CAZAC / ML channel-estimation sequence foundation | 中：序列基础，非同步竞品 |
| Burst-Mode Multi-Level-CPFSK Signal Detection Using DD-LMS Based Adaptive Equalizer for High-Speed TDM-PON Upstream | 2024 | `10.1109/JLT.2024.3368269` | backward/OpenAlex | yes | equalizer handover + short preamble | 低 |
| Preamble Design for Joint Frame Synchronization, Frequency Offset Estimation and Channel Estimation in Burst Mode Coherent PONs | 2024 | `10.1364/OFC.2024.M1I.1` | backward/OpenAlex + local ref | yes | FS + FOE + CE | 高但非新增：Sun 2025 同一工作会议前身 |
| The approaches of coherent technology for TDM-PON | 2019 | `10.1049/CP.2019.0761` | backward/OpenAlex | yes | coherent TDM-PON overview | 低 |
| Joint Power Optimization of PTMP Coherent Architecture for Improving Link Budget in Downlink Transmission | 2020 | `10.1364/ACPC.2020.M4A.316` | backward/OpenAlex | yes | power optimization；“joint”非同步动作 | 无关 |
| Asymmetric point-to-multipoint coherent architecture with a frequency aliasing recovery algorithm for cost-constraint short-reach access networks | 2022 | `10.1364/OE.463944` | backward/OpenAlex | yes | frequency alias recovery | 低 |

**后向结论**：

1. 发现更直接的**候选**而非已闭合的 joint estimator：Zhou et al. 2025 (`10.1109/JLT.2025.3528909`) 摘要同时覆盖 sampling-phase offset、同步位置与频偏，动作集合比 Sun 2025 更接近 Q1；但摘要没有证明这些量由单一联合目标/估计器输出，必须 acquire→全文精读后才能裁决。
2. 早期技术链清晰：CAZAC/完美周期相关序列（1961/1992/2006）→ clock-aided burst FOE（1997）→ training-aided FD CE（2014）→ preamble FS/SOP/FOE（2020/2021）→ TS/data-aided fast convergence（2023）→ Sun 的共享 training unit（2024/2025）。
3. 当前链中**没有**可据摘要确认的单一 `(frame, fractional timing/SCO, CFO)` joint estimator。

## JOCN 获取 receipt

本轮将三路径上限解释为“最多三条适用且合法的独立路径”，不把 dry-run 计为 acquisition path，不把不支持 Optica 的 `blit` 硬凑成一次请求。

| attempt | command/path | result | access boundary |
|---|---|---|---|
| preflight | `C:\Users\zzt\.venvs\torch\Scripts\python.exe tools/paper_download.py --doi '10.1364/JOCN.587273' --dry-run` | PASS：只打印 canonical 目标目录 | `tools/download` Bash wrapper 在本 Windows worktree 因 CRLF 无法解析；调用其唯一底层入口，参数等价，不绕过下载器通道 |
| 1 | `C:\Users\zzt\.venvs\torch\Scripts\python.exe tools/paper_download.py --doi '10.1364/JOCN.587273'` | `all_failed`；无 source/content | 仅 downloader 的 arXiv/OA/Unpaywall 等既定通道；未 `--force` 循环重试 |
| 2 | `bash tools/search '"Joint time-frequency domain feature exploitation for a single burst-mode preamble in a next-generation coherent optical access network"' --sources arxiv --top 10 --output 'search-archive/2026-08-06/jocn-587273-arxiv-exact.json' --format json` | official arXiv exact-title：0 条 | 只查 arXiv；未扩到 ResearchGate、Scholar、作者聚合站 |
| 3（适用性门） | `tools/blit` source contract inspection | `NOT_APPLICABLE_NOT_RUN`：合法源枚举仅 IEEE/万方/cbpt/CNKI，无 Optica/JOCN | 不把 Optica DOI 伪装成 IEEE 请求；不访问/绕过 publisher paywall |

- arXiv receipt：`search-archive/2026-08-06/jocn-587273-arxiv-exact.json`，269 bytes，SHA256 `ac62af697674d40631511d173646aae998940793e707b319e8b41a42dd732651`。
- 本轮失败 metadata：`papers/doi/10.1364_jocn.587273/metadata.json`，`download_status=failed`、`download_method=all_failed`、`content_file=""`，SHA256 `2351ea1d02981f10cbf5a713cece4c1fc9ef727264bc025c9a496608fbd56f51`。
- 历史 receipt 仍在 `projects/thesis-fso/oversampled-sync-groundwork/direct-competitor-acquisition-receipt.json`，记录上一轮 DOI downloader、official arXiv exact-title 与官方 Optica access page 三路径失败。本轮没有重复打开 publisher HTML。

## JOCN identity/content gate

| gate | result | evidence |
|---|---|---|
| DOI/title identity | PASS（既有 primary metadata receipt）；本轮 downloader metadata 没有补回 title | `direct-competitor-acquisition-receipt.json` 的 Crossref/Optica identity；前向 citation JSON 的 DOI、题名、作者、年份一致 |
| lawful source acquired | FAIL | canonical 目录只有 `metadata.json`，没有 `source.*` |
| `content.md` exists | FAIL | `papers/doi/10.1364_jocn.587273/content.md` 不存在 |
| line count >= 50 | N/A/FAIL | 无全文，不执行伪行数门 |
| source/content SHA256 | N/A | 无 source/content；只记录 metadata SHA |

官方摘要/元数据最多支持以下 action claim：

- receiver-visible information：**single burst-mode preamble**；
- frequency-domain actions：CD estimation、clock recovery；
- time-domain actions：frame synchronization、FOE、SOP estimation；
- experiment scene：32-GBaud DP-16QAM coherent optical access network。

摘要**不能**支持：fractional timing 的状态/分辨率、SCO/ppm/drift、clock recovery 与 frame/FOE 是否共享同一子序列、处理时序、是否有单一联合 objective/estimator、输出耦合、复杂度、合法 comparator、以及 FSO impairment 下的同任务碰撞。因此 `exact-action novelty/collision` 继续保持 `UNRESOLVED_HIGH_RISK`，不得将“同一 preamble 支持多模块”升级成“单一联合 estimator 已占用”。

## 新高相关论文 acquire→read 清单

| priority | paper | current evidence | required next gate |
|---|---|---|---|
| P0 | Xiong et al., JOCN 2026, `10.1364/JOCN.587273` | 前向严格引用；摘要动作集合最接近；本轮仍无全文 | 仅用户提供合法全文或新 OA/preprint 入口后 identity/SHA/≥50 行，再精读 action contract |
| P1 | Zhou et al., JLT 2025, *Burst-Mode Digital Signal Processing for Coherent Optical Time-Division Multiple Access*, `10.1109/JLT.2025.3528909` | 后向严格引用；摘要同时列 sampling-phase offset、sync position、FO、SOP、equalizer；本地无全文 | acquire 后核查各动作是否顺序模块、共享何种 preamble 信息、是否 joint objective/输出 |
| P2 | Jin et al., OE 2025, `10.1364/OE.566136` | 前向严格引用且 OA；摘要为 FS+FOE+CE，无 clock/timing | acquire→浅读；只判定是否出现摘要遗漏的 timing action，不先升 CORE |
| P3 | Zhang et al., JOCN 2020/2021, `10.1364/JOCN.402591` | Sun 本地 reference + OpenAlex；摘要为 FS+SOP+FOE | 若现有 CORE 未覆盖其具体动作，再 acquire→浅读；主要作早期 preamble baseline |

同 lineage 的 OFC 2024 `10.1364/OFC.2024.M1I.1` 被 Sun 2025 全文 supersede，不列为独立必读；其存在只用于技术血缘。

## 结论与 blocker

- 引用链规模：forward 8 + backward 35 = 43 条方向记录；S2-only=0，引用真实性没有靠 S2 单源冒充。
- 新直接竞争信号：JOCN 2026（forward）仍为最高风险；JLT 2025 `10.1109/JLT.2025.3528909`（backward）是新增的高相关多动作候选。两者都**不能仅凭摘要**裁成单一 `(frame,tau,CFO)` joint estimator。
- 早期基础链已定位，但它支持的是序列、burst FOE、CE、FS/SOP/FOE 与 fast-convergence 模块的技术血缘，不自动支持 exact-action collision。
- JOCN 本轮合法获取结果：**失败并止损**。没有全文、没有 source/content SHA/行数，exact-action novelty blocker 保留。
- 未执行 Step 4a、方法实现、testbed 或仿真；未抓 ResearchGate/Google Scholar/IEEE Xplore HTML，未绕过访问控制，未提交。
