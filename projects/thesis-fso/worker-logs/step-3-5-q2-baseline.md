# Q2 baseline adjudication

> 日期：2026-08-06
> 任务：`.sessions/2026-08-06-oversampled-coherent-sync-groundwork/T007-q2-baseline-adjudication.md`
> 边界：仅独立裁决 canonical 判据 1、判据 3 与 cheap comparator 身份；未修改 canonical 状态，未进入 Step 4a、实现、testbed、MVE 或仿真。

## Canonical 判据 1 重判

**PASS。** `stages/glossary.md:28` 对判据 1 的要求是 M/C/A 明确、句子级、可解；没有要求 Step 3 已经用实验、MVE 或正文观察证明 A 为真。Q2 可写成完整且可证伪的 M-C-A：

- **M**：timing loop 与 carrier loop 独立执行 maintenance/reacquisition；明显廉价扩展为 receiver-visible quality threshold 下 shared freeze，并按固定 known-preamble/reference 重启；
- **C**：RRC、≥2 sps coherent OSL，存在 SCO/drift、CFO/Wiener phase noise 与 dynamic deep fade；
- **A**：fade 可能共同退化 TED 与 carrier detector，使两环共同或异步失锁，且固定阈值共同冻结与固定周期重启可能仍不能给出有界、稳定的恢复。

“共同失锁尚未观测”与“cheap comparator 尚未证明不足”是后续 Step 4a 的 problem-truth / headroom 问题，不能反向制造判据 1 FAIL。现有正文只限制 claim ceiling：Paillier 2020 只观察 carrier DPLL，且假设 ideal timing；Valjus 2025 将 timing/CPE/FOE 分开仿真，没有同一 dynamic fade trace 上的双环状态轨迹。证据见 `projects/thesis-fso/worker-logs/step-3-sync-read-c.md:25-31,138-148,245-272`。

## 候选 baseline 表

| paper/system | year | DOI | information | action/output | integrated? | task fit |
|---|---:|---|---|---|---|---|
| Gu et al., *All-Digital Timing Recovery for Free Space Optical Communication Signals With a Large Dynamic Range and Low OSNR* | 2019 | `10.1109/JPHOT.2019.2956086` | oversampled CFSO samples、timing-error/loop history | timing NCO/interpolator；clock-corrected samples | **否**：timing only | Q2 的 timing 子系统 baseline；无 carrier loop、dynamic fade 双环状态或 reacquisition |
| Paillier et al., *Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop* | 2020 | `10.1109/JLT.2020.3003561` | symbol-rate I/Q、power、AGC/DPLL state | continuous AGC + DPLL phase NCO；carrier-corrected stream | **否**：正文显式假设 ideal timing | Q2 的 carrier/fade baseline；无 SCO/timing loop、hold 或 post-fade 双环 reacquisition |
| Le Bidan et al., *Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link* | 2023 | `10.1109/ICSOS59710.2023.10490279` | blind 2-sps samples + known headers/pilots | coarse CFO bank → Lee timing/interpolation → FSE/downsample → frame → fine CFO → CPE | **同一 receiver chain 是；Q2 动作否** | 有 SCO 与连续 DSP 链，但未模拟 dynamic fade、lock state 或 post-fade reacquisition；论文明确把 stay-locked/reacquisition 留作未解边界 |
| Valjus et al., *Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links* | 2025 | `10.1002/sat.1553` | oversampled samples、TED/loop history、pilot/preamble、power/SNR | timing NCO/重采样；CPE/FOE correction；FOE 低质量时可停止更新 | **否**：timing/CPE/FOE 分开评估 | 是近期 OSL 算法入口和依赖证据；不是一套已执行的 joint maintenance/reacquisition baseline |
| Sun et al., *Preamble Design for Joint Frame Synchronization, Frequency Offset Estimation, and Channel Estimation in Upstream Burst-Mode Detection of Coherent PONs* | 2025 | `10.1109/JLT.2025.3533197` | receiver-known TS-A/TS-B | Godard clock → frame → CFO → channel/equalizer initialization | **仅 acquisition chain** | 能支撑 Q1；不研究 SCO maintenance、fade-triggered loss/reacquisition 或双环恢复时间 |
| Nguyen et al., *Carrier Frequency Offset Estimation Using Godard Timing Recovery in Coherent Optical Systems* | 2024 | `10.1364/OFC.2024.M1E.5` | conventional timing recovery 已有的 spectrum information | 从 TR 信息估计 CFO；输出 CFO estimate | **跨模块复用，但非双环状态机** | 4-subcarrier 100-GBaud coherent fiber acquisition/estimation；无 FSO fade、持续 timing+carrier maintenance 或 reacquisition。官方 Optica abstract：`https://opg.optica.org/abstract.cfm?uri=OFC-2024-M1E.5` |
| Du et al., *An Optimum Signal Detection Approach to the Joint ML Estimation of Timing Offset, Carrier Frequency and Phase Offset for Coherent Optical OFDM* | 2021 | `10.1109/JLT.2020.3042546` | noisy CO-OFDM block / spectrum replicas | joint ML TO/CFO/CPO estimate；另有 sequential acquisition variant | **联合 acquisition estimator** | JLT 且真正 joint，但波形为 CO-OFDM、任务为一次性 acquisition；不是 RRC single-carrier 双环 maintenance/reacquisition |
| Shi et al., *Joint Timing and Frequency Synchronization for Coherent Optical SEFDM Systems* | 2023 | `10.1109/ACP/POEM59049.2023.10369081` | conjugate-symmetric training symbol | timing metric + closed-form CFO estimate | **联合 acquisition estimator** | SEFDM training acquisition；无 SCO drift、dynamic fade、lock state 或 reacquisition |
| Thomas et al., *Design and validation of a CCSDS O3K synchronization front-end...* | 2025 | `10.1109/ICSOS66026.2025.11443202` | non-coherent O3K GEO optical downlink samples/framing | CDR lock + frame synchronization/reacquisition | **clock/frame 是；carrier 否** | 直接讨论 deep fade、CDR lock 与 reacquisition，但为非相干 OOK/DPSK framing；不能充当 coherent timing+carrier baseline |

证据边界：本地 7 CORE 全文与 read notes 为正文证据；新增候选仅用 DOI/官方 abstract 或双 API 元数据做 task-fit 排除，不把摘要冒充全文的正向 baseline 裁决。`q2-joint-timing-carrier-recovery.json` 中 Nguyen 2024 的 Semantic Scholar 摘要实际与题名不符，故本裁决改用 Optica 官方摘要；该误配条目不得作为方法事实来源。

## 判据 3 verdict

**FAIL（当前证据范围内）。** 没有识别出一篇/一套可引用的 2019+ task-matched baseline，同时满足以下最小身份：

1. 在同一已发表 receiver/system 中承担 timing 与 carrier 的持续 maintenance；
2. 对两环给出合法 receiver-visible information、update/hold/reacquire action 与输出，而不只是把两个独立章节并列；
3. 任务包含 loss-of-lock 后的 reacquisition，或至少可作为该任务的直接同输出 comparator；
4. 不是跨 Gu + Paillier + Valjus 多篇文献拼接后虚构成“已有 integrated baseline”。

三类最接近结果均不能通过：

- **同一 coherent receiver 顺序链**（Le Bidan/Sun）缺 dynamic fade 下的 lock/reacquisition action；
- **真正 joint estimator**（Du/Nguyen/Shi）只做 acquisition/offset estimation，且波形或链路任务不匹配；
- **真正 fade/reacquisition 系统**（Thomas O3K）为非相干 CDR+frame，不包含 coherent carrier loop。

补检索范围：

- `search-archive/2026-08-06/q2-joint-timing-carrier-recovery.json`：S2 + OpenAlex + arXiv，2019+，41 篇；逐题名/摘要筛查后 exact Q2 baseline = 0；
- `search-archive/2026-08-06/q2-fade-reacquisition-lock.json`：同三源，2 篇；仅 Thomas 2025 接近 fade/reacquisition，但 modality/output 不匹配；
- `search-archive/2026-08-06/q2-integrated-timing-carrier-maintenance-reacquisition.json`：过约束 query 返回 0；该零召回只作为 query 诊断，不单独支持 FAIL。

因此，Q2 的 **判据 1=PASS、判据 3=FAIL**；canonical 四判据仍未全过，Q2 不是 Step 3 survivor。这里的 FAIL 是“当前检索与证据池未找到合法 baseline”，不是对全领域不存在此文献的普遍性证明。

## Q1 最强廉价 comparator closure

**是，但必须分清“强 fair comparator contract”与“单篇已发表 baseline 身份”。** Q1 最强廉价替代应至少包含：

`fixed polyphase/Farrow fractional-delay bank（或 Le Bidan 的 Lee timing/interpolation + FSE） → downsample → Sun 2025 CAZAC / Wang 2023 FSTS / Tang 2022 STSB frame+FOE`，并保留 Le Bidan 的 coarse-CFO、fine-CFO 与 CPE 顺序链。

理由：

- Le Bidan 2023 已在同一 receiver 中给出 `2 sps coarse CFO → timing/interpolation → FSE/downsample → frame → fine CFO → CPE`；
- Sun 2025、Wang 2023/2024、Tang 2022 已占用 shared/structured preamble 的 frame+FOE 与资源复用表述；
- fixed polyphase/Farrow phase bank 是对 fractional timing 未知最直接、低风险的搜索增强，必须先排除它就能消除候选收益的可能。

这套 exact composite 没有被当前某一篇论文完整实现，故不得伪称“某篇 Q1 baseline”。Q1 判据 3 的近期文献身份分别来自 Le Bidan 2023 的完整 ordered chain 与 Sun/Wang/Tang 的 task-matched acquisition 子链；组合体是后续公平对照合同。证据见 `projects/thesis-fso/worker-logs/step-3-sync-read-b.md:218-228,320-354`、`step-3-sync-read-a.md:133-147,282-288`。

## Q2 cheap comparator contract 边界

Q2 的最强廉价 comparator 应冻结为：

1. Gardner/Gu timing loop（含 NCO/interpolator 与 SCO state）；
2. Paillier 式 AGC+DPLL，或 Valjus 的 FOE + VV/pilot CPE；
3. 仅用 receiver-visible quality metric 的共同 threshold，低质量时同时 freeze 两环更新；
4. fade 后按固定 known-preamble/reference 周期重启 timing fine tracking 与 FOE/CPE；
5. 与任何后续候选使用相同样本、preamble overhead、fade trace、参数调优机会及 lock/recovery 指标。

其边界是：Gu/Paillier/Valjus 分别给出了组件依据，Valjus 还给出 FOE 低质量停止更新与 cycle-slip 后等待固定 phase reference 的相邻做法；但没有一篇论文执行上述完整链。因此它只能称 **主线构造的 fair cheap comparator contract**，不能自动满足 canonical 判据 3，也不能写成“文献已证明有效”或“文献已证明不足”。

## 结论

- **Q2 canonical 判据 1：PASS。** M/C/A 明确、句子级、可解且 A 可证伪；不要求 Step 3 已有 MVE/量化失效证据。
- **Q2 canonical 判据 3：FAIL。** 当前 7 CORE + 有界三源补检索未找到 2019+ integrated、task-matched timing+carrier maintenance/reacquisition baseline。
- **Q2 cheap comparator：仅为 fair comparator contract。** 禁止把 Gu + Paillier + Valjus 拼成一篇/一套“已有 integrated baseline”。
- **Q1 cheap comparator：closure 成立。** polyphase/Farrow（或 Lee/FSE）timing front-end + Le Bidan/Sun/FSTS/STSB sequential chain 是必须排除的最强廉价组合，但 exact composite 同样不能伪称单篇论文身份。
- **总体：Q2 非 Step 3 survivor；本裁决不授权 Step 4a、实现或仿真。**
