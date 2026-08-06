# GW Step 1：过采样相干 FSO 联合同步前端检索报告

> 日期：2026-08-06
> 证据层级：本地索引、六份结构化检索 JSON 及其中的题录/摘要/检索片段；**未下载、未全文精读**
> 边界：只做候选问题预判；不声称问题四判据、参数量级或新颖性已闭合

## 1. 检索执行与可重算统计

本轮恰好使用预算内六组 query，覆盖 timing/SCO、feedforward/fractional timing、frame+CFO、burst coarse/fine、fade/reacquisition 和已知基线锚点。每组 query、时间戳、JSON SHA256 和结果数见 `step1-search-receipt.json`。

| 检索组 | 主题 | 结果数 |
|---|---|---:|
| q1 | coherent optical/FSO Gardner、M&M、fractional delay、SCO | 29 |
| q2 | feedforward clock、oversampling、pulse shaping、clock drift | 36 |
| q3 | CFSO frame+CFO、Park/Schmidl-Cox、STSB/FSTS | 13 |
| q4 | burst-mode coarse/fine、preamble、Doppler | 25 |
| q5 | turbulence/fade、loss-of-lock、reacquisition | 21 |
| q6 | Tang/Wang/Fan/Paillier 及 Gardner/M&M/FFT-FOE 锚点 | 16 |

合计 **140 条原始结果**。以小写 DOI 为第一键、arXiv ID 为第二键、否则以去标点规范化标题为键，跨六文件得到 **130 条唯一结果**；其中 2019+ 为 **42 条原始、39 条唯一**。结果记录的 `source_api` 聚合为：Tavily 90、SerpAPI Scholar 35、OpenAlex 6，另有组合/重复来源标记 9。这里的“来源”是结构化 JSON 中每条记录的生成 API，不把一个组合标签拆成多次命中。

## 2. Step 1 五问

### 2.1 timing/frame/SCO 是否真实且量级可溯源？

**Step 1 判断：真实；工程量级存在可追踪锚点，但必须由 Step 2 全文固化。**

- 2019 IEEE Photonics Journal 的 *All-Digital Timing Recovery for Free Space Optical Communication Signals With a Large Dynamic Range and Low OSNR*（DOI `10.1109/JPHOT.2019.2956086`）明确把 timing recovery 作为 FSOC 数字相干接收机的必要功能，比较 Gardner 并提出适应大动态范围/低 OSNR 的实时 FPGA timing recovery。这排除了“只有旧 caller 没实现，所以问题不存在”。
- 2025 卫星相干光 DSP 综述（DOI `10.1002/sat.1553`）把接收 DSP 分为 timing recovery、carrier synchronization、equalization 三个子系统，并以 optical satellite link 为目标场景。
- 本轮命中的 DLR ground-to-GEO timing-recovery 资料片段给出 **25 Gbaud QPSK、2 sps、RRC roll-off≈0.3、clock offset 100 ppm、强湍流 fade 到 -15 dB**，且明确要求在 fade 中跟踪时钟漂移或 fade 后恢复。它是参数候选源，但当前记录只有检索片段、缺稳定 DOI/出版身份，**不能在本阶段作为最终参数真相源**；Step 2 必须获取并核验身份/全文，否则 100 ppm 和 -15 dB 不得进入后续 MVE/claim。
- 2022 Optics Express timing-phase detector（DOI `10.1364/OE.447448`）明确使用 2 samples/symbol、10 Gbaud QPSK 并做实时 FPGA clock recovery，证明 RRC/过采样/插值 timing 链是现实的 coherent-optical 工程对象。Paillier space-ground DPLL 的检索片段给出初始 CFO 100 MHz、锁定约 1.4 ms；2025 inter-satellite carrier work给出最大 frequency-change rate 10 MHz/s。两者仅用于说明 carrier acquisition/tracking 的量级不是拍参，仍需 Step 2 回到正式全文。

因此，关键 impairment 有物理/工程依据；但 fractional timing 的分布、SCO ppm 范围、frame offset 分布、fade duration/coherence 和联合发生模型尚未闭合。

### 2.2 是否有 2019+ task-matched 顶刊/合法 baseline？

**有 2019+ task-matched、同行评审的合法 baseline，且分为 acquisition 与 maintenance 两条链；但“相干 FSO + 三联任务 + 顶刊”这一更严格交集尚未由元数据闭合。** 顶刊级近邻主要来自 JLT coherent-optical/PON，FSO 同场景基线主要在 IEEE Photonics Journal、Optics Express/Communications；这不触发“无 2019+ 合法 baseline”，但 Step 2 必须核查 venue、任务边界和直接竞争强度。

- timing：Gu et al. 2019, IEEE Photonics Journal, DOI `10.1109/JPHOT.2019.2956086`，FSOC 大动态范围/低 OSNR 下的 all-digital timing recovery；以及 2022 Optics Express DOI `10.1364/OE.447448` 的 2-sps coherent-optical timing baseline。
- frame+CFO：Tang 2022 STSB, IEEE Photonics Journal, DOI `10.1109/JPHOT.2022.3161795`；Wang 2023 FSTS, IEEE Photonics Journal, DOI `10.1109/JPHOT.2023.3265847`；Fan 2024 short-time-spectrum FOE, Optics Communications, DOI `10.1016/J.OPTCOM.2024.130981`；以及 2024 Optics Express frame+carrier recovery, DOI `10.1364/OE.520452`。
- carrier maintenance：Paillier 2020 space-ground AGC+DPLL（本地锚点 DOI `10.1109/JLT.2020.3003561`）和 2025 satellite coherent DSP review（DOI `10.1002/SAT.1553`）。

“task-matched”目前仅由题录/摘要支持；特别是 Wang/Fan/Paillier 的具体输入、动作、truth 使用和湍流设置，必须在 Step 2/3 才能定案。

### 2.3 是否已有直接覆盖联合帧—定时—频率同步的方法？

**存在非常接近的直接竞品，尚未发现元数据层面已在相干 FSO 中闭合 sample-level fractional timing + frame + CFO 三者的同信息/同动作/同任务竞品。**

- Tang 2022 STSB 已用 receiver-known symmetric sequence 同时定位数据帧并估计 CFO；Wang 2023 FSTS 也把 frame synchronization 与 FOE 集成。因此，“把 Tang/Wang 放到 GG-FSO”或仅把 FS+FOE 改名为 joint synchronization，直接碰撞，必须禁止。
- 2024 Optics Express DOI `10.1364/OE.520452` 已在 coherent FSO 中用伪随机+循环 QPSK training 做 frame synchronization 与两级 FOE/carrier recovery，是 acquisition 候选的最强同场景直接竞品之一。
- 2025 JLT coherent-PON preamble（DOI `10.1109/JLT.2025.3533197`）同一 training unit 联合 frame synchronization、FOE 和 channel estimation；2026 JOCN（DOI `10.1364/JOCN.587273`）进一步声称同一 burst preamble 在频域做 clock recovery、在时域做 frame/FOE。后者虽不是 FSO，但在“receiver-known preamble → clock/frame/frequency actions”上高度接近，必须列为跨场景直接竞品。

当前差异只可能成立在 **RRC 过采样 sample-level fractional timing/SCO 与 frame/CFO 的耦合动作**，而不是场景名。若 Step 2/3 证明上述 FSO 或 coherent-PON 方法已使用相同接收信息、联合搜索/更新相同状态并完成相同任务，触发 `EXISTING_ACTION_COLLISION`。

### 2.4 最小 testbed 模块与工程量

静态 BOM 的 full frozen object 包含：统一 waveform/timebase/frame contract、RRC TX/RX、≥2 sps、fractional-delay、fractional timing 与 SCO/drift 注入、frame/preamble 与真实 frame offset、timing detector/loop、CFO/Wiener phase noise、Gamma-Gamma、paired realization、BER/EVM/sync-error 和 baseline runner；合并后约 **11–14 人日**。

候选特定最小切片不同：acquisition slice（RRC/2-sps/fractional timing/frame/CFO/最小 truth+runner）约 **5.5–7.5 日**；maintenance slice（RRC/2-sps/Gardner/SCO/GG/carrier/truth+runner）约 **7–9 日**。两者都复用现有调制、carrier recovery、GG 和 BER 资产，不等于重建完整通信平台，因此当前不满足 `TESTBED_SCOPE_EXCESSIVE` 的合取停止条件。分类、逐项证据与风险见 `testbed-bom.md`。

### 2.5 能否形成至少两个机制不同的 Q#？

能。下列两个候选分别是 **preamble-aided acquisition** 与 **fade-aware stateful maintenance/reacquisition**，信息、动作与失败机制不同；它们是预卡，不是已确认问题。

## 3. 候选问题预卡

### Q1 — 过采样 burst CFSO 的 sample-level 帧—分数定时—CFO acquisition

- **M-C-A**：M = 先以 STSB/FSTS/相关峰做整数帧定位和 CFO，再由独立 Gardner/插值器做定时；C = QPSK/16QAM、RRC、≥2 sps、未知 frame offset + fractional timing + CFO 的 coherent FSO burst；A = off-grid sampling 使 preamble correlation/相位差统计偏离峰值，顺序估计把 timing 不确定性传给 frame/CFO，可能造成旁瓣误锁或 residual CFO。
- **recent baseline**：Tang 2022 STSB、Wang 2023 FSTS、2024 OE pseudo-random/cyclic-QPSK frame+carrier，以及 Gu 2019/Gardner timing 链的顺序组合。
- **deployable input → action → output**：receiver-known preamble 的 ≥2-sps 复样本（不读 payload truth）→ 在有限 frame index / fractional-delay / CFO 网格上联合或 coarse-to-fine 估计并补偿 → 对齐、重采样、粗频偏已校正的符号流及 lock/confidence。
- **与 CCISP 独立性**：动作是单接收前端的时基/帧/CFO 状态估计与校正；不选择空间分支、不做 branch scheduling、不改变 CCISP select-before-execute 动作。
- **strongest cheap alternative**：matched filter + fixed polyphase/Farrow bank，逐候选相位运行 STSB/FSTS，选最大 normalized correlation 后用 FFT-FOE/Gardner 微调；必须作为先验强基线。
- **物理参数来源**：Gu 2019 FSOC timing；DLR ground-to-GEO 片段（2 sps、β≈0.3、100 ppm，仅待核）；Tang/Wang/2024 OE 的 frame/CFO；Paillier/卫星 DSP 综述的 CFO/Doppler。Step 2 前不得拍范围。
- **testbed 模块**：统一 sample/frame contract、RRC TX/RX、2-sps、fractional delay/offset、preamble/frame builder 与真实 offset、CFO/PN、paired realization、frame/timing/CFO error、BER、最小 runner。
- **基础设施工作量**：acquisition slice **5.5–7.5 日**；若全文要求把 SCO 长时维护/GG reacquisition 同时纳入，则需重新审计，不能偷算进该切片。
- **可能章节方法形态**：一节“receiver-known preamble 的 coarse integer frame/CFO + fractional timing refinement”，再加复杂度/overhead 与 sequential baseline 对照；不是把 STSB 换场景。
- **否决条件**：全文发现 Tang/Wang/2024 OE 或 2025–26 coherent-PON 方法已在相同接收信息下完成同等 sample-level frame+fractional timing+CFO 动作；cheap polyphase-bank sequential baseline 无可测不足；星地参数下 fractional timing 对 frame/CFO 的增量影响不可辨；或 faithful baseline 需要 full platform 11–14 日且候选无法裁剪。

### Q2 — GG fade 与 SCO 下 timing/carrier 联合 lock maintenance 和有界 reacquisition

- **M-C-A**：M = Gardner/GuCui timing loop 与 AGC+DPLL/VV carrier loop独立、固定带宽/固定阈值运行；C = 2-sps RRC coherent ground-to-satellite link，持续 SCO/drift、Wiener PN/CFO 且有 Gamma-Gamma deep fade；A = fade 同时降低 timing 与 carrier error detector 可信度，独立积分器可能在低置信区间积累错误并异步失锁，fade 后恢复时间/误锁由最慢链主导。
- **recent baseline**：Gu 2019 FSOC timing recovery + Paillier 2020 AGC+DPLL 的合法串联基线；2025 JLT normalized Gardner clock-tone detector作为 timing 对照；固定 power-threshold loop freeze/restart 作为必须加入的廉价先验。
- **deployable input → action → output**：receiver samples、known-pilot/preamble（若使用则计 overhead）、包络/AGC、TED 与 phase-detector innovation、既往 lock state → 对 timing NCO/interpolator 与 carrier loop执行 update/hold/coarse-reacquire 的有限状态动作 → 连续校时校相符号流、显式 lock/loss/reacquisition 状态与失败标记。
- **与 CCISP 独立性**：这里只控制单链路同步环内部状态，不选择/调度多孔径 branch；若动作退化为按功率挑 branch 或 select-before-execute，立即判为 CCISP collision。
- **strongest cheap alternative**：同一个接收功率/normalized-error 门同时冻结两个传统 loop，fade 后以固定 preamble 周期重启 FFT-FOE + Gardner；比任何自适应联合控制先行验证。
- **物理参数来源**：DLR ground-to-GEO timing 资料片段（100 ppm、fade 到 -15 dB，身份待 Step 2）；Gu 2019 大动态范围/低 OSNR；Paillier 2020 的 AGC+DPLL；2025 inter-satellite 10 MHz/s Doppler tracking；Gamma-Gamma 只采用后续全文/现有已溯源参数，不为制造失锁而外推极端值。
- **testbed 模块**：RRC/2-sps、fractional interpolator、stateful SCO/drift truth、Gardner/GuCui loop、GG、CFO/Wiener PN与DPLL/VV、paired realization、timing/SCO/CFO/CPE/reacquisition 指标、最小 runner；不需未知 frame-start 搜索。
- **基础设施工作量**：maintenance slice **7–9 日**，属较重但有界的 stateful DSP extension；不是 full communication platform。
- **可能章节方法形态**：一节“共同置信度驱动的双环 hold/update/reacquire 状态机”，主比较固定独立 loop、共同冻结和周期性 reacquisition；任何复杂模型必须晚于 cheap baseline 失败证据。
- **否决条件**：全文不能给出 SCO/fade 时间尺度与失锁证据；共同冻结+固定重启已消除差距；拟议动作需 payload truth；同信息/动作/任务的 FSO joint timing-carrier maintenance 已存在；或候选必须并入完整 acquisition/full platform 才能成立。

## 4. Step 1 gate

| 停止条件 | 元数据级审查 |
|---|---|
| 关键 timing/SCO/frame 无依据 | 不成立：Gu 2019、卫星 DSP 综述和 ground-to-GEO 参数片段提供工程锚点；参数待全文核验 |
| 旧 caller 不支持且需完整平台重建、明显 >5 日 | 不成立：full object 11–14 日，但 Q1/Q2 最小切片不是完整平台重建 |
| 直接竞品同信息/同动作/同任务 | 尚未闭合；存在强近邻，列为 Step 2 首要核查 |
| 全部只是 Tang/Wang/Fan 换场景 | 不成立：Q1 增加 sample-level fractional timing coupling；Q2 是 stateful timing/carrier maintenance，但二者仍需全文证伪 |
| 无 2019+ baseline | 不成立 |
| 少于两个机制不同候选 | 不成立：acquisition 与 maintenance 两张预卡机制不同 |

**Step 1 terminal 建议：`PROCEED_TO_STEP2_ACQUISITION`。** 这不是用户给定的五个停止终态之一，而是内部继续门；合法下一动作仅是按 `stages/gw-acquire.md` 获取至少五篇 CORE 全文，优先闭合 ground-to-GEO 参数源、Gu 2019、Tang/Wang/2024 OE、Paillier 2020 和最接近的 coherent-PON joint preamble 竞品。Step 2 后必须停在用户覆盖面确认门，不得进入 Step 3。
