# [R007] Step 3.5 citation semantic-screen ledger

> 2026-08-12 | 关联：R006 / D006 | 只持久化已完成筛查，不新增检索

## 判定口径

- `MUST`：可能承重 exact/cheap/full absorption，必须取得 primary fulltext。
- `SHOULD`：强 comparator/动作邻居，需进入边界矩阵；不能只凭摘要裁 collision。
- `ROUTE`：综述或引用路由，不承担 action verdict。
- `EXCLUDE`：任务、信息源、输出或动作与 Q001 不同，不能承担 collision。
- Round 的 new MUST/SHOULD 以“该轮首次出现的 identity”计；同一 identity 后续再次命中不重复。

## Round 1 — C02 forward citation chain（21）

| ID | title | decision | reason |
|---|---|---|---|
| R1-01 | Feedforward Phase Noise Compensation for Intersymbol Interference Channels | SHOULD | von-Mises/SPA low-complexity sequence neighbor，输出/ISI task 不同 |
| R1-02 | On the Application of Expectation Propagation to Symbol Detection in Phase Noise Channels | MUST | 2025 strong-WPN EP、投影/拒绝/复杂度可能吸收 mixture 叙事 |
| R1-03 | Modeling, Estimation, and Applications of Phase Noise in Wireless Communications: A Survey | ROUTE | 方法分类/引用路由，非 primary action |
| R1-04 | Phase Noise Compensation Techniques for Cellular Systems in Millimeter-Wave Bands | EXCLUDE | mmWave cellular survey/technique family，非 single-tone unwrap |
| R1-05 | Phase Noise Detection via Expectation Propagation and Related Algorithms (arXiv:2404.05344) | ROUTE | R1-02/DOI `10.1109/TCOMM.2025.3538847` 同作者同论文的 preprint lineage；identity alias-dedup，贡献 0 个 new SHOULD |
| R1-06 | Information Rates of Successive Interference Cancellation for Optical Fiber | EXCLUDE | SIC/information-rate task，无 unwrap lifecycle |
| R1-07 | Phase Noise Estimation and Compensation Using FDM Pilot for High-Order QAM Transmission in DFT-Spread OFDM Backhaul Links | EXCLUDE | FDM-pilot OFDM 信息合同不同 |
| R1-08 | Code-Aided Carrier Synchronization with Adjustable Operating Ranges for Satellite Communications | SHOULD | candidate list+cheap score，但 code-aided full-frame |
| R1-09 | The Difficult Road of Expectation Propagation Towards Phase Noise Detection | ROUTE | EP analysis/route，非新的承重 action |
| R1-10 | A Multi-Sample Discrete-Phase BCJR Algorithm for Phase Noise Channels | SHOULD | discrete phase sequence/full-grid benchmark |
| R1-11 | Joint parameter estimation and decoding in a distributed receiver | SHOULD | particle/SIS joint phase/Doppler/decoder neighbor |
| R1-12 | Iterative Joint Parameters Estimation and Decoding in a Distributed Receiver for Satellite Applications and Relevant Cramer-Rao Bounds | EXCLUDE | 与 R1-11 同 lineage，迭代 decoder task，无 fixed-lag unwrap |
| R1-13 | Cycle-Slip Detection and Correction for Carrier Phase Synchronization in Coded Systems | EXCLUDE | coded LLR detector/corrector，decoder information mismatch |
| R1-14 | Parametric Phase Tracking via Expectation Propagation | MUST | one-shot decoder-free claim需全文核 pilot/output/schedule |
| R1-15 | Efficient Low-Complexity Phase Noise Resistant Iterative Joint Phase Estimation and Decoding Algorithm | EXCLUDE | iterative joint decoding，非 decoder-free sequence unwrap |
| R1-16 | Iterative Detection and Phase-Noise Compensation for Coded Multichannel Optical Transmission | EXCLUDE | coded multichannel iterative receiver |
| R1-17 | Iterative Decoding and Phase-Noise Compensation for Multichannel Optical Transmission | EXCLUDE | 与 R1-16 同族/preprint，不新增 action |
| R1-18 | Joint-Polarization Phase-Noise Estimation and Symbol Detection for Optical Coherent Receivers | EXCLUDE | joint-polarization symbol detection，非 single-tone unwrap |
| R1-19 | Tikhonov sum approach for joint carrier phase estimation and decoding in frequency-hopping communications | EXCLUDE | code-aided frequency-hopping task |
| R1-20 | Message Passing-Based Sparse Channel Estimation Under Partially Coherent Wiener Phase Errors | EXCLUDE | sparse channel estimation output不同 |
| R1-21 | Digital PLLs for Phase Noise Channels: A Concept Based on the Tikhonov Distribution | MUST | decoder-free single-carrier cheap Tikhonov baseline |

Round-1 query records additionally首次产生 `MUST=PAPU 2019, Access 2026` 与 `SHOULD=Zhang 2026 multi-stage CFO`；连同上表 identity 去重后，Round 1 new MUST/SHOULD=`5/5`。R1-05 与 R1-02 alias-dedup，不重复计 SHOULD；这些 query-record evidence 已在 R006 primary/fulltext section 与 receipt 的 acquisition list 闭合。

## Round 2 — C01/C09/C12 forward chains（26）

| ID | title | decision | reason |
|---|---|---|---|
| R2-01 | Pilot-Tone-Based Carrier Phase Recovery in Photonic THz DSCM Communication Systems | SHOULD | pilot-tone cheap alternative，THz/Tx reference mismatch |
| R2-02 | Optical computing and optical signal processing for recovery of spatiotemporally coupled optical communications channels | EXCLUDE | optical-computing/SDM review，无 unwrap action |
| R2-03 | Maximum a Posteriori Probability Phase Recovery for 256-QAM Modulated Signals in Coherent Optical Communications | SHOULD | recent optical MAP CPE comparator，symbol task |
| R2-04 | Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems | SHOULD | direct FSO/NDA estimator neighbor，非 sequence unwrap |
| R2-05 | Modeling, Estimation, and Applications of Phase Noise in Wireless Communications: A Survey | ROUTE | Round1 duplicate，不重复计 new |
| R2-06 | Maximum Likelihood Estimation of Wiener Phase Noise Variance in MPSK Modulated Systems | SHOULD | PN-variance dependency/ablation，非 action carrier |
| R2-07 | Using Monotonic Neural Networks for Accurate and Efficient Passive Localization Performance Modeling | EXCLUDE | localization ML task |
| R2-08 | Efficient FPGA Implementation of Phase Offset Estimation and Compensation for 5G Based LEO Satellite Communication System | SHOULD | fixed-resource realization comparator，reference-signal dependent |
| R2-09 | Viterbi-Viterbi Carrier Phase Estimation for Multi-Ring M-APSK With Wiener Carrier Phase Noise and Its Performance | SHOULD | recent fixed-memory VV cheap comparator |
| R2-10 | Mth Power Carrier Phase Estimation with Wiener Phase Noise for MPSK Modulations | MUST | C01 modulation extension，需核 truth/genie unwrap 与 action |
| R2-11 | Design and Performance Evaluation of Polar Coding for BICM Systems With Phase Noise | EXCLUDE | code design/decoder task |
| R2-12 | Using conditional averaging of delayed signals to measure phase shift angle | EXCLUDE | instrumentation angle measurement，非 unwrap chain |
| R2-13 | Analysis of Full-Duplex Radios With Transceiver Phase Noise on Spectrum-Tight Battlefields | EXCLUDE | full-duplex impairment analysis |
| R2-14 | Phase Unwrapping in Correlated Noise for FMCW Lidar Depth Estimation | MUST | Viterbi integer-wrap/survivor exact-action risk |
| R2-15 | Echo State Network based Noise Detection in Energy Internet Orienting Justice Blockchain Data | EXCLUDE | unrelated application |
| R2-16 | ML/MAP Estimation of Frequency Offset and Linear Phase Noise in Coherent Optical Communications | SHOULD | optical joint parameter-estimation lineage |
| R2-17 | Parameter Estimation of a Single Chirp in the Presence of Wiener Phase Noise With Unknown Variance | MUST | single-tone/chirp/WPN recent joint estimator lineage |
| R2-18 | Fast Fourier Transform and Piecewise Aggregation Approximation-Based Detection and Separation of Dynamic DC and AC Hybrid Interferences on Oil and Gas Pipelines | EXCLUDE | unrelated interference detection |
| R2-19 | A Pipelined FPGA-Based Frame Synchronizer for Gaussian Noise Channels | EXCLUDE | frame-sync state machine，非 carrier unwrap |
| R2-20 | Improved Carrier Phase Recovery for High-Capacity Optical Communication Systems With High-Order Modulation Formats | MUST | no-abstract direct optical CPR，动作必须全文核 |
| R2-21 | A Modified Viterbi Equalization Algorithm for Mitigating Timing Errors in Optical Turbulence Channels | EXCLUDE | Viterbi state是timing/ISI，不是 phase wrap |
| R2-22 | Development of 32-GBaud DP-QPSK Free Space Optical Transceiver Using Homodyne Detection and Advanced DSP | SHOULD | FSO receiver context/cheap pipeline，非承重 action |
| R2-23 | Noncoherent Massive MIMO | EXCLUDE | task/domain mismatch |
| R2-24 | Amplitude-Coherent Detection for Optical Wireless Communications: Opportunities and Limitations | EXCLUDE | amplitude-coherent information/action不同 |
| R2-25 | Scenario-indexed Q/R Selection for EKF-Based Doppler Tracking in Coherent Satellite Laser Links | SHOULD | receiver-visible selector/EKF cheap alternative；Round1 Zhang identity不重复 new |
| R2-26 | Performance Evaluation of DF-Based Cooperative DCSK for Next-Generation Wireless Networks | EXCLUDE | noncoherent cooperative DCSK task |

Round 2 首次 identity 汇总：new MUST/SHOULD=`4/8`。`R2-25` 是 Round1 已出现的 Zhang identity，不重复计；survey 同理。

## Round 3 — four-MUST forward chains（13）

Round 3 的 OpenAlex 结果未由工具保存逐条 archive；fresh worker 在单次上下文中完成 14 raw/13 unique 筛查并返回 exact title/DOI/OpenAlex ID。以下 ledger 持久化该既有结果；该轮不以任何一条支撑 terminal，terminal 只由已取得的四篇 MUST primary fulltext承担。

| ID | returned title/task category | decision | reason |
|---|---|---|---|
| OA-R3-01 | On The Foundational Condition for Non-Contact Vibration Measurement Using Phase-Based Microwave Interferometry (`10.1109/ICASSP55912.2026.11463883`, W7155102697) | EXCLUDE | microwave sensing output，非 unwrap receiver |
| OA-R3-02 | Multi-Polynomial Phase Signal Parameter Estimation Using Time-Frequency Decomposition and Time-Series Representations (`10.1109/ICASSP55912.2026.11464849`, W7155053761) | EXCLUDE | polynomial-phase parameter estimator，无 wrap lifecycle |
| OA-R3-03 | Analysis of Transceiver RF Impairments on Artificial Noise Suppression in Frequency-Hopping Systems (`10.1109/TSUSC.2024.3475576`, W4403182255) | EXCLUDE | impairment analysis，无 deployable unwrap action |
| OA-R3-04 | Reconfigurable Intelligent Surface-Assisted Localization in OFDM Systems With Carrier Frequency Offset and Phase Noise (`10.1109/TWC.2025.3557935`, W4409356916) | EXCLUDE | localization output，不是 phase sequence |
| OA-R3-05 | Direction-of-Arrival Estimation for Wideband Chirps via Multi-Line Fitting in the Fractional Fourier Domain (`10.1109/ACCESS.2025.3581843`, W4411472254) | EXCLUDE | DOA/chirp output不同 |
| OA-R3-06 | Maximum Likelihood Estimation of Wiener Phase Noise Variance in MPSK Modulated Systems (`10.1109/WCNC61545.2025.10978631`, W4410227379) | EXCLUDE | PN-variance dependency，已由 R2-06 路由，不是 action |
| OA-R3-07 | Estimating Parameters of Elementary Chirp Model Using Modified Newton-Raphson Algorithm (`10.1007/S00034-025-03165-Y`, W4410540204) | EXCLUDE | continuous parameter refinement，无 integer paths |
| OA-R3-08 | Variance of the Root Mean Square Value of the Residuals of Sine Fitting in the Presence of Additive Noise (`10.1038/S41598-025-32688-2`, W4417529582) | EXCLUDE | residual statistics，不是 tracking action |
| OA-R3-09 | Research on the Influence Mechanism of Angular Misalignment on the Transmission Performance in Inter-Satellite Coherent Laser Communication (`10.1016/J.OPTCOM.2025.131685`, W4408032033) | EXCLUDE | spatial alignment/impact study |
| OA-R3-10 | Sparse Volterra Equalizer for Compensation of Frequency Offset and Laser Phase Noise in Standard Single Mode Fiber (`10.1007/S42979-025-04381-8`, W4414346366) | EXCLUDE | nonlinear equalizer，无 discrete wrap lifecycle |
| OA-R3-11 | Orbit Determination Using Passive Optical Communication Observations (`10.1117/12.3041354`, W4406877911) | EXCLUDE | navigation/orbit output不同 |
| OA-R3-12 | 基于新型主成分分析和联合判决的载波相位恢复 (`10.3788/AOS251886`, W7154944499) | EXCLUDE | CPR neighbor但无 bounded discrete hypotheses/commit完整合同 |
| OA-R3-13 | Joint Timing and Carrier Synchronization with Integrated Modulation Quality Measurement for High-Order QAM Signals (`10.3390/PHOTONICS13060544`, W7163180540) | EXCLUDE | high-order QAM joint acquisition/output不同 |

Round 3 new MUST/SHOULD=`0/0`。该表只审计“为什么没有新增承重论文”；四篇 Round-2 MUST 的 primary action verdict 见 R006 与对应 canonical read notes。

## 确定性汇总

| round | actual citation rows | new MUST | new SHOULD | evidence |
|---|---:|---:|---:|---|
| 1 | 21 | 5 | 5 | C02 forward + Round1 query identities |
| 2 | 26 | 4 | 8 | C01/C09/C12 forward |
| 3 | 13 | 0 | 0 | four-MUST OpenAlex forward worker ledger |
| total | 60 | — | — | 数量门只按 citation rows；priority按identity/round去重 |

因此最后一轮 new MUST/SHOULD=`0/0`，检索收敛；semantic-screen ledger 与 R006/receipt 计数一致。
