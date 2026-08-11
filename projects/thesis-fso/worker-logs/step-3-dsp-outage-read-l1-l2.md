# Step 3 精读证据：Johst 2024 与 Wang 2023

> 执行任务：T007 | 日期：2026-08-11 | 读取方式：fresh-context 全文逐行精读
> 边界：只提取论文事实和候选问题证据；不裁决 Q# terminal，不设计扩展算法，不搜索、下载或仿真。

## 0. 标题门与身份门

| 对象 | brief 指定身份 | 全文实际标题 | 门结果 | 证据 |
|---|---|---|---|---|
| Johst 2024 | Johst et al.; WiSEE 2024; DOI `10.1109/WISEE61249.2024.10850117`；任务明确关注 outage/hard discard | *Data-Aided Multi-Format DSP for Robust Free-Space Coherent Optical Communication* | **PASS**：作者、venue/year、DOI 对象及“低 SNR 稳定 DSP→post-DSP combining”主题实质一致 | Johst 全文 L1-L5、L13-L25 |
| Wang 2023 | Wang et al.; IEEE Photonics Journal 2023; DOI `10.1109/JPHOT.2023.3265847`；任务明确关注 FSTS/MRC reference | *Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication* | **PASS**：标题直接包含 FSTS、spatial diversity、PM coherent FSO；DOI/venue/year 一致 | Wang 全文 L5、L11-L19、L75-L83 |

## 1. L1 — Johst et al., WiSEE 2024

### 1.1 标准字段（15/15）

- **DOI**：`10.1109/WISEE61249.2024.10850117`（brief 绑定；全文为 IEEE WiSEE 2024 论文）。
- **源文件路径**：`papers/doi/10.1109_wisee61249.2024.10850117/content.md`。
- **read status**：全文精读完成；method、simulation、field setup/results、conclusion 均覆盖。
- **发表状态**：正式发表。
- **venue**：2024 IEEE International Conference on Wireless for Space and Extreme Environments (WiSEE)。
- **year**：2024。
- **核心贡献**：论文构造了面向低 SNR、调制格式独立的 data-aided 双偏振相干接收 DSP，以帧同步/粗细 CFO、MIMO channel estimation/equalization、两级 CPE 的已知训练信息链减少低 SNR 锁定失败（L27-L98）。论文以数值仿真和 3.15 km、多日外场试验量化 DSP-outage 边界，并明确指出低于约 `-1 dB` 的 aperture channel 可能产生 DSP-based outage、应从 combining 中丢弃；但论文没有实际研究多孔径合并算法（L100-L138、L140-L207、L209-L211）。
- **方法概览**：每个 32768-symbol frame 含帧同步/CFO header、MIMO CE header、30720 payload 及每 100 个 symbol 一个 4QAM CPE pilot；DSP 顺序为 resampling→frame sync/coarse/fine CFO→data-aided channel estimation/ZF MIMO equalization→pilot CPE+BPS fine CPE→detection/BER（L33-L52、Fig.1）。
- **实验设置**：32 GBd DP-4QAM/DP-16QAM；仿真加入 AWGN、PDL、polarization rotation、固定 CFO 与 Wiener phase noise，每 SNR/condition 100 MC；外场用 3150 m 城市 FSO 链路，DP-4QAM 约 45 h/2600 记录、DP-16QAM 约 59 h/3300 记录（L100-L138、L140-L203）。
- **baseline**：理论 AWGN/M-QAM 与 pure-AWGN DSP 情形；多种 impairment 组合（AWGN+PN、+CFO、+PDL/rotation）。文中定性对照 blind CMA/BPS，并称 ZF 与 MMSE 性能相近，但未给 data-aided DSP 对 blind equalizer 或 alternative combining 的同图定量算法对照（L27-L31、L88、Fig.3 L133-L138）。
- **关键结论**：仿真中 `SNR >= 0 dB` 均可靠；外场 DSP-outage threshold 为 DP-16QAM `-1.2 dB`、DP-4QAM `-1.8 dB`。论文据此给出约 `-1 dB` 的可靠 diversity-combining 使用下界，并明确承认统计证据不完整、实际需 safety margin（L138、L203-L207）。
- **与本专题关系**：直接提供 branch DSP failure 的可观测形状、硬 outage 标记及 discard comparator；不提供 receiver-visible multi-source soft shrinkage，也不执行多孔径 combining（L106、L207-L211）。
- **实现关键细节**：2 samples/symbol 输入；同步 header 为 4 个 `B` block、每个 256 个 4QAM symbols；coarse CFO range `±500 MHz`、fine `±62.5 MHz`；CE header 1024 samples；每 100 个 payload symbol 插入 pilot；总 DSP overhead `≈7.75%`；frame 约 `1 µs`；ZF butterfly filters 用 overlap-and-add 快速卷积（L50-L92）。
- **fit**：对“branch DSP validity 是否会异质失效”高度适配；对“如何连续加权/暂缓接纳”不直接适配，因为本文动作只有通过 BER/SNR 边界识别 outage 并硬丢支路，且没有多支路权重优化实验。
- **code**：全文未报告开源代码或可下载实现。
- **validation**：全文内部 title/author/venue 与 brief 身份一致；证据来自上述 source path。执行合同禁止外部搜索，故未做外部发表状态再检索。

### 1.2 七个结构段

1. **state**：N/A（非 DRL）。接收端显式量包括已同步 frame、两偏振样本、估计 CFO、MIMO channel responses、pilot phase、SNR、BER；论文不定义学习状态。
2. **action**：非 DRL 确定性 DSP action：训练序列相关定位→粗/细 CFO correction→data-aided CE→ZF MIMO equalization→pilot interpolation CPE+BPS→symbol detection。论文结果层的 branch action 是 `BER >= 0.44` 记为 DSP-based outage；约低于 `-1 dB` 的 channel “have to be discarded for combining”（L106、L203-L207）。
3. **reward/objective**：reward=N/A。目标是低 SNR 下保持 DSP lock/valid stream，并使 pre-FEC BER 可被后续 SD-FEC/combining 使用；论文采用 `BER <= 2e-2` 的 SD-FEC threshold（L19-L25）。
4. **model assumptions**：大气信道在约 `1 µs` frame 内静态（scintillation 仅至数 kHz）；reasonable bandwidth 下 frequency-flat，因此 ZF≈MMSE；sample-rate offset 在单帧内近似常数；仿真 phase noise 为 Wiener process（L62、L88-L92、L100-L108）。这些假设把跨帧 tracking/hysteresis 与 branch-dependent rapid DSP state 排除在本文验证外。
5. **network/algorithm**：network=N/A。算法为固定 data-aided signal-processing pipeline；无训练网络、优化器或 learned parameters。
6. **fit**：可直接绑定 hard discard comparator 与 outage-label provenance；不能把 paper 的固定 SNR/BER rule 解释为 soft admission 方法，也不能把后续多孔径研究计划解释为已经验证的 combining method。
7. **problem extraction**（论文自身问题，不是本专题 Q# 裁决）：
   - **M**：常见 blind coherent DSP/equalization（如 CMA、blind BPS chain）。
   - **C**：大气 fading 导致的 very-low-SNR、DP multi-format coherent FSO，且 post-DSP diversity combining 要求支路 DSP 仍保持有效。
   - **A**：blind adaptation 收敛慢、低 SNR 稳定性差、受 modulation format 约束；BPS 在低 SNR 易 cycle slip（L27-L31、L112-L116）。
   - **四判据**：①具体矛盾 **✅**（M/C/A 明确）；②方法产出 **✅**（可复用 data-aided frame/DSP chain）；③近期 baseline **❌/未闭合**（全文只定性引用 blind 方法，未建立近期 task-matched comparator identity）；④量化对标 **❌/局部**（量化了 impairments/AWGN 与 outage boundary，但未直接量化 data-aided vs blind equalizer 或 combining policy）。

### 1.3 精确动作签名

`每支路 2-sps DP waveform + 已知 frame/CFO/CE/CPE symbols -> 每帧触发 correlation sync；粗/细 CFO、ZF MIMO equalization、pilot+BPS CPE；若 acquisition BER >= 0.44 则标记 DSP outage，论文结果建议 SNR 约低于 -1 dB 时硬 discard -> 输出已均衡的有效支路 symbol stream，或 outage/discard 标记，供未在本文执行的 post-DSP combining 使用。`

边界解释：Johst 的新贡献是低 SNR data-aided DSP 及其 outage boundary；`discard` 是硬门限处置，不是连续权重，也不是本文验证过的多孔径合并新方法（L19-L25、L106-L138、L203-L211）。

### 1.4 通信参数表

| 链路/模块 | 模型 | 关键参数 | 证据 |
|---|---|---|---|
| 仿真 coherent DP | AWGN + arbitrary polarization rotation + PDL + fixed CFO + Wiener PN | 32 GBd DP-4/16QAM；CFO `400 MHz`（结论覆盖 `±400 MHz`）；linewidth `200 kHz`；PDL `3 dB` | §III, Fig.2-3；L100-L138 |
| frame/DSP | data-aided fixed frame | 32768 symbols；30720 payload；pilot every 100th；2 sps；DSP overhead `≈7.75%` | Fig.1；L33-L52 |
| 外场 FSO | 3150 m urban terrestrial free-space | wavelength `1550.12 nm`；Tx `10 dBm`；32 GBd；Tx RRC roll-off `0.1`；Tx DAC `64 GS/s/8 bit`；Rx ADC `50 GS/s/8 bit` | §IV, Fig.4；L140-L173 |
| 接收前端 | preamplified intradyne coherent receiver | preamp NF `≈4.05 dB`；OPM sensitivity `≈-75 dBm`, bandwidth `>5 kHz`；LO linewidth about `100 kHz` | L151-L171 |
| outage/FEC | empirical decision thresholds | simulation outage=`BER >= 0.44`；SD-FEC threshold=`BER <= 2e-2`；reliable DSP nominally down to `0 dB` simulation / about `-1 dB` field | L23、L106-L138、L203-L207 |

### 1.5 实验完备性（≤20 行）

1. **claims/scope**：bounded 到 data-aided DSP 的 low-SNR stability；结论将 combining 明确留给 follow-up（L209-L211）。
2. **统计**：每 SNR 100 MC/noise seeds；`BER >= 0.44` 样本从 mean BER 排除且单独标记；未报告 CI/显著性检验（L104-L138）。
3. **field volume**：DP-4QAM 约 45 h/2600 recordings；DP-16QAM 约 59 h/3300 recordings；两组在不同日期/环境（L177-L205）。
4. **baseline matrix**：理论 AWGN + pure AWGN + PN/CFO/PDL impairment combinations；没有 task-matched alternative DSP 的定量 baseline。
5. **ablation/sensitivity**：有 impairment 逐项叠加及 PDL rotation cases；无 header/pilot/two-stage component ablation。
6. **channel realism**：simulation 为简化 discrete-time channel；field trial 提供真实 turbulence、PDL、tracking disruption/heavy rain observations。
7. **topology diversity**：仅单链路/单 aperture DSP 数据；没有 multi-aperture combining experiment。
8. **complexity**：无 O()、FLOPs 或实时延迟报告；只说明 COTS/offline processing 和 fast convolution。
9. **VVUQ**：Verification `2/3`（100-MC、多 impairment）；Validation `2/3`（多日真实链路但单 site）；Uncertainty `1/3`（无 CI，作者明确统计不完整）。

## 2. L2 — Wang et al., IEEE Photonics Journal 2023

### 2.1 标准字段（15/15）

- **DOI**：`10.1109/JPHOT.2023.3265847`（Wang 全文 L83）。
- **源文件路径**：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`。
- **read status**：全文精读完成；introduction、TS/FS/FOE equations、complexity、simulation platform/results、conclusion 均覆盖。
- **发表状态**：正式发表、Open Access（CC BY）。
- **venue**：IEEE Photonics Journal, Vol. 15, Issue 3。
- **year**：2023（publication date 2023-04-10）。
- **核心贡献**：论文设计跨 X/Y polarization 的 frame-synchronous training sequence (FSTS)，同一 TS 同时承担 branch frame synchronization/alignment 与两级 FOE，从而在 shared-LO spatial-diversity receiver 中先对齐/MRC、再联合补偿频偏（L95-L105、L117-L219）。它在 10 GBaud PM-4/16QAM、1/2/4/6 支路、强弱 turbulence 仿真中对比 blind/TS FOE，报告 320-symbol FSTS 相比 960-symbol conventional TS 具有相近或更好 BER，并报告最优 real-multiplication complexity 约降 75%（L231-L385）。
- **方法概览**：FSTS 在两偏振上采用交错/共轭对称 block；threshold-based Park metric 给出各支路 frame start 并去除 relative delay。对齐后作 branch phase correction 与 MRC、polarization demultiplexing，再用跨偏振相邻同符号共轭积作 wide-range coarse FOE，用 block-spaced conjugate products 作 noise-reduced fine FOE，最终两阶段估计相加（L103-L219）。
- **实验设置**：10 GBaud PM-4/16QAM B2B 和 spatial-diversity FSO simulation；Fourier phase-screen 10 km channel，`Cn2=1e-16/1e-14 m^(-2/3)`；TS length 48–960（重点 320/960）；frequency offset random in `(-1.1, 1.1) GHz`；spatial branches 1/2/4/6（L231-L243、L245-L385）。
- **baseline**：4th-power/QPSK-partition blind FOE、4th-FFT FOE、conventional TS-based FOE；FS 对照 Park sliding-window concept，complexity 还对比 joint FS/FOE method [19]（L97-L101、L217-L229、L289-L329）。
- **关键结论**：320-symbol proposed FSTS 对 conventional TS 的 sensitivity gain 在 two-branch MRC 达到 PM-4QAM `1.43/2.09 dB`（weak/strong）与 PM-16QAM `2.54/3.41 dB`；320-symbol FSTS 可达到 conventional 960-symbol TS 相近或更好 BER，且 optimal complexity 约降 75%（L375-L385）。
- **与本专题关系**：这是“先 per-branch sync/phase correction，再 MRC，再 pol-demux/FOE”的直接 spatial-diversity receiver reference；其 method 改变训练/FOE estimator，不是 outage-aware branch weighting，也未定义 DSP-invalid branch abstention。
- **实现关键细节**：FS metric `Mm(d)=|Cm(d)|^2/Pm(d)^2`；最终仿真 FS threshold `0.2`；two-stage FOE 用相邻跨偏振共轭积进行 coarse estimate、block spacing `BL` 的共轭积 fine estimate，并用 `Δfest=Δf1+Δf2`；推荐最短 TS 320 symbols；coarse estimate 可 buffer/periodically update（L117-L219、L245-L289、L339）。
- **fit**：对 MRC 数据流、branch alignment、shared-LO assumption 与 estimator-changing competitor 高度适配；对 branch-level DSP outage 的识别/处置不适配，因为 MRC 前没有基于 validity 的 drop/soft weight action。
- **code**：全文未报告开源代码；只给公式、block diagrams 与 simulation results。
- **validation**：全文页面内部 title、authors、DOI、venue/year 一致；证据来自指定 absolute source path。执行合同禁止外部搜索，未做外部引用/代码检索。

### 2.2 七个结构段

1. **state**：N/A（非 DRL）。确定性处理量包括每支路 training samples、timing metric、relative delay、MRC 后 X/Y samples、coarse/fine frequency estimates；论文无学习 state。
2. **action**：threshold FS 对每支路定位和延迟对齐→diversity-branch phase correction→MRC→polarization demux→two-stage FSTS FOE→phase-noise estimation/DD-LMS/demap。coarse FOE 可保存并周期更新（L117-L219、L243）。
3. **reward/objective**：reward=N/A。objective 是在 FS accuracy 不降的条件下最大化 FOE range/accuracy 与 receiver sensitivity，同时降低 training overhead/hardware complexity；指标为 FS accuracy、normalized FOE MSE、BER/sensitivity、real multiplications/additions。
4. **model assumptions**：X/Y 两偏振 frequency offset 相同；各 branch shared LO，因而 MRC 后可 joint compensate；turbulence phase/intensity/coupling fluctuations 与 laser phase noise相对 GHz symbol rate 慢，相邻/块间共轭可消除；phase-screen outer scale→∞、inner scale→0；branch fading independent（L101-L105、L152-L183、L231-L243）。
5. **network/algorithm**：network=N/A。algorithm 为 FSTS design + threshold FS + analytic two-stage FOE；公式核心是 (1)-(2)、(7)-(11)，无 learned model/optimizer。
6. **fit**：可用作 estimator-changing competitor 与 reference MRC ordering；不能把它写成 branch outage-aware admission，因为所有已对齐 branch 进入 MRC，全文没有 validity-driven weight/drop variable。
7. **problem extraction**（论文自身问题，不是本专题 Q# 裁决）：
   - **M**：conventional TS-based FOE（兼及 4th-power/4th-FFT blind FOE）。
   - **C**：短 training sequence、multi-format PM coherent FSO spatial-diversity reception，在 turbulence 下需要 branch FS/alignment 和 low-complexity FOE。
   - **A**：conventional TS FOE accuracy 依赖长 TS，导致 overhead/complexity；short TS 时 joint frame/frequency synchronization 不佳，blind 4th-power/FFT 又受 format/range/resolution/FFT complexity 限制（L95-L101）。
   - **四判据**：①具体矛盾 **✅**；②方法产出 **✅**（FSTS+FS/FOE equations）；③近期 baseline **❌/未闭合**（全文页不提供 refs [18]/[19] 书目信息，无法仅凭本次允许输入核验“近期顶刊”身份）；④量化对标 **✅**（FOE MSE、FS accuracy、BER/sensitivity、complexity 对 conventional TS/4th methods）。

### 2.3 精确动作签名

`m 路 shared-LO PM coherent samples + X/Y 交错共轭 FSTS -> 每帧计算各支路 timing metric，超过 threshold(主仿真 0.2) 时定位/对齐；执行 branch phase correction 后 MRC，pol-demux 后以跨偏振相邻同符号作 coarse FOE、以 BL 间隔同符号作 fine FOE并求和 -> 输出对齐合并后的 X/Y symbols、Δfest、后续 BER；所有已对齐支路进入 MRC，未定义 outage validity weight/drop。`

与 Johst 的关键差别：Wang 改的是 TS/FS/FOE estimator 与 DSP ordering，并把 MRC 置于 FOE 前；Johst 给的是每支路低 SNR DSP 可靠边界与硬 discard 语义。二者都没有 receiver-visible multi-source soft weighting action。

### 2.4 通信参数表

| 链路/模块 | 模型 | 关键参数 | 证据 |
|---|---|---|---|
| PM coherent signal | simulated B2B/FSO | 10 GBaud PM-4QAM/16QAM；ECL linewidth `50 kHz` | §III, Fig.4；L231-L243 |
| turbulence | Fourier-transform phase screen | range `10 km`；outer scale→∞、inner scale→0；weak `Cn2=1e-16 m^-2/3`、strong `1e-14 m^-2/3` | L241 |
| receive apertures | independent fading branches, SMF coupling | telescope aperture `0.2 m`；mean coupling `67.3012%` weak / `4.8395%` strong；branch counts 1/2/4/6 | L243、Fig.18 L375-L381 |
| coherent receiver | shared LO across branches | LO linewidth `50 kHz`, power `15 dBm`; photodiode responsivity `0.8 A/W`; shot+thermal noise | L243 |
| FSTS/FS | threshold Park metric | TS 48–960; shortest selected `320`; FS threshold `0.2` or `0.3` (spatial experiments use `0.2`) | L245-L279、L339 |
| FOE | two-stage analytic estimator | random offset `(-1.1,1.1) GHz`; representative `BL=20`; TS structures vary with format/length | L175-L219、L289-L319 |
| BER/FEC | receiver sensitivity at fixed BER | main FEC threshold `3.8e-3`; FS study also plots sensitivity at BER `2e-2` | L267、L329-L385 |

### 2.5 实验完备性（≤20 行）

1. **claims/scope**：bounded 到 simulation feasibility/generality、receiver sensitivity 和 complexity；没有 field/hardware implementation claim。
2. **统计**：FS accuracy 每点 6400 simulations；FOE MSE 每 point 800 simulations/random offsets；未给 random seeds、CI/error bars 或显著性检验（L257、L319）。
3. **baseline matrix**：4th-power/QPSK partition、4th-FFT、conventional TS；complexity 另比 joint method [19]。
4. **fairness**：按相同 training/estimated symbol length 320/960 做同图比较；另有 proposed-320 vs TS-960 overhead/BER cross-budget comparison。
5. **ablation/sensitivity**：扫描 TS length、`BL/BN` structure、frequency offset、received power、threshold、modulation、turbulence、branch count；没有删除 coarse/fine stage 的组件消融。
6. **channel realism**：physics-inspired phase-screen，显式 strong/weak turbulence、coupling、shot/thermal noise；outer/inner scale 极限化且仅 simulation。
7. **topology diversity**：1/2/4/6 branch，strong/weak turbulence，PM-4/16QAM。
8. **complexity**：Tables I-II 给 real multiplications/additions；无 wall-clock、memory、FPGA resource/latency。
9. **VVUQ**：Verification `2/3`（公式+大批重复 simulation+多轴扫描）；Validation `1/3`（无实验/外场）；Uncertainty `1/3`（重复次数充分但无 CI/seeds/model-form sensitivity）。

### 2.6 写作架构摘要（Wang，15 行以内）

1. Introduction 采用 FSO/turbulence→spatial-diversity complexity→FOE 分类缺陷→FSTS contribution 的漏斗。
2. 方法章先给 TS structure，再按 FS 与 FOE 两个复用职责展开。
3. FS 先给 timing metric 公式/流程图，再解释 threshold 如何换复杂度。
4. FOE 先给接收信号模型，再从 coarse 到 fine 连续列式，最后给合成估计。
5. complexity 独立成节，用两表分别比较 FOE-only 与 joint FS/FOE。
6. simulation platform 用一张系统图串起 turbulence、shared LO、MRC 与 DSP ordering。
7. 结果先验证 FS，再验证 FOE MSE，最后进入 BER/receiver sensitivity。
8. 图组按 B2B→single branch→four branch→1/2/4/6 branch 逐级扩展 scope。
9. 参数展示主要散布在正文/Fig captions，未见集中 parameter table。
10. baseline 以 4th-power、4th-FFT、conventional TS 三类覆盖 blind 与 training-based 路线。
11. complexity 是 analytic operation count；没有 runtime/hardware resource 图。
12. conclusion 回收 320-vs-960 training、two-branch gain 与约 75% complexity 三个量化锚点。

## 3. 跨论文事实对照（仅供主线综合）

| 维度 | Johst 2024 | Wang 2023 |
|---|---|---|
| 论文实际改变的对象 | 整体 data-aided low-SNR DSP/frame chain | FSTS、FS 与 two-stage FOE estimator |
| combining 是否实际执行 | 否；留给 follow-up | 是；FS/branch phase correction 后 MRC |
| branch invalidity 表达 | `BER >= 0.44` outage；约 `<-1 dB` 建议 hard discard | 无 outage/validity variable；对齐后的 branch 进入 MRC |
| MRC 前后顺序 | 论文仅要求有效 post-DSP stream，未执行 MRC | per-branch FS/phase correction→MRC→pol-demux→FOE |
| 最接近本专题的事实角色 | hard-discard mandatory comparator 与 defect shape | estimator-changing competitor 与 FSTS/MRC reference |

## 4. 证据路径清单

- Johst 全文：`papers/doi/10.1109_wisee61249.2024.10850117/content.md`。
- Wang 全文：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`。
- Step 3 规范：`stages/gw-read.md`；问题四判据：`stages/glossary.md`；通信参数要求：`domain-comms.md` §1.1。
- 本日志所有 Johst `Lx` 指针指第一条 source 的全文行号；所有 Wang `Lx` 指针指第二条 source 的全文行号。
