# RML-FSTS source-calibration audit

## Verdict

`HARD_BLOCKED_FOR_SCIENTIFIC_TERMINAL`

这一定论只针对**原 Q1 structural `(B_N,B_L)` smoke 能否凭当前本地一手证据下科学 terminal**。结论分两层：

- **Diagnostic 可跑**：可重建 320-symbol action-specific FSTS，给每个 action 复用同一组外生 PRBS/channel/CFO/PN/noise innovations，做公式 identity、range/wrap 和结构 counterfactual 诊断。该诊断必须标 `DIAGNOSTIC_ONLY / TERMINAL_DISABLED`，其接收波形按 action 不同，不能声称 identical rx。
- **Scientific terminal 不可承重**：当前本地 Wang 材料没有给出可唯一复原的 dBm→电噪声映射、Fig. 10 的完整 source power/action/numeric curve、Wang phase-screen 的波长/光束/网格/耦合合同，也没有 structural action 发生前的 receiver-power 观测与发端重配置协议。Gu 的 scalar Gamma-Gamma 只能作 transfer channel，不能替代 Wang phase-screen。

这不只是“补一个本地输入即可恢复”的情形：补到 Wang PDF/图像最多能恢复坐标轴和曲线点；它不能自动补齐未报告的 receiver noise 参数、phase-screen 数值合同，亦不能解决 structural action 必须在当前 FSTS 发射前决定的协议因果问题。因此，缺图是 recoverable gap，但不是唯一 blocker。

本审计未运行 adapter、semantic-smoke 或 performance grid，未修改任何现有文件。

## Wang source condition ledger

### 本地 source 身份

- canonical 目录实测仅有 `content.md` 与 `metadata.json`，没有 `source.pdf` 或本地图像缓存。
- `metadata.json` 记录 `download_method=firecrawl_scrape`、`content_type=html`、`content_quality=good`；因此正文/MathJax 可作一手文字和公式证据，图内坐标不得凭链接或 read-note 臆造。
- 下面把正文可直接确认的内容记为 FACT；只存在于未落地图像中的 tick/value 统一记为 UNKNOWN。

### Receiver-power 点与扫轴

| source panel | 可确认的 condition / axis | 可确认的 anchor | 当前 UNKNOWN |
|---|---|---|---|
| Fig. 5 | 不同 received power 下的 timing metric；TS=48/320，PM-4/16QAM | power 越低，timing peak 越低；48-symbol 低功率时峰可消失，320 可修复 | 所有 power 数值与曲线点 |
| Fig. 6 | x-axis=`received optical power`；四支路 MRC、strong `C_n^2=1e-14`；每点 6400 次 | power 越高 FS accuracy 越高；TS>128 后阈值 0.2/0.3 可保持准确率 | x ticks、各 threshold/length 的数值曲线 |
| Fig. 7 | x-axis=TS length；y=BER `2e-2` 时 receiver sensitivity；strong turbulence | 48→320 时 4/16QAM sensitivity 分别改善 3.47/2.49 dB；320→800 仅 0.48/0.23 dB | absolute receiver-sensitivity dBm、完整 TS ticks |
| Fig. 8 | BER vs normalized CFO-MSE，按多个 received optical powers 分组 | BER-onset NMSE：4QAM `2.5e-7`、16QAM `6.25e-8`；severe：`6.25e-6`、`2.25e-6` | 分组 power 值、各点 BER/MSE |
| Fig. 9 | x-axis=training-symbol length；多个 received powers；proposed `B_L=20`；CFO uniform open `(-1.1,+1.1) GHz` | length>=160 时 proposed 在不同 powers 下对 16QAM 优于三对手；proposed NMSE 约 `1e-7~1e-9`、conventional TS 约 `1e-6~1e-7` | power 值、length ticks、逐点 NMSE |
| Fig. 10 | x-axis=`B_L`；固定 TS length 320/960；4/16QAM | accuracy 随 `B_L` 先改善、到一定值后可能退化；320 defaults=`(16,20)/(8,40)`，960 defaults=`(24,40)/(16,60)` | 每 panel 的 received power、完整 `B_L` ticks、逐点 NMSE/CI；正文没有可冻结的数值容差 |
| Fig. 11(a,c) | 4QAM CFO sweep，received optical power=`-43 dBm`，TS=320/960 | proposed NMSE 文本量级 `1e-8~1e-9`，conventional TS 约 `1e-7`；TS-based range 约为 blind 的 4 倍 | CFO ticks/逐点值；文本量级不是单点精确值 |
| Fig. 11(b,d) | 4QAM x-axis=`average received optical power`，TS=320/960 | low power 时 proposed 可能差于对手；power 增大后显著改善、稳定并优于三对手 | power ticks、转折点、floor 与逐点 NMSE |
| Fig. 12(a,c) | 16QAM CFO sweep，received optical power=`-37 dBm`，TS=320/960 | proposed NMSE 文本量级 `1e-8~1e-9`，conventional TS 约 `1e-7`；每 CFO point 平均 800 次 | CFO ticks/逐点值 |
| Fig. 12(b,d) | 16QAM x-axis=`average received optical power`，TS=320/960 | power sweep 存在；同段说明同 power 下 CFO 随机抽样 800 次后平均 | power ticks、逐点 NMSE、稳定转折点 |
| Fig. 13 | B2B BER vs received optical power | TS=320 时相对 conventional TS 的 FEC-sensitivity gain：4/16QAM=`0.98/1.72 dB`；TS=960 为 `0.25/0.39 dB` | absolute FEC sensitivity 与 power grid |
| Fig. 14/15 | single-branch BER vs average received optical power；weak/strong `C_n^2=1e-16/1e-14` | TS=320 时相对 TS baseline gain：4QAM=`1.12/1.17 dB`，16QAM=`2.23/3.11 dB`（weak/strong） | absolute powers、所有曲线点 |
| Fig. 16/17 | four-branch MRC BER vs average received optical power；weak/strong | TS=320 gain：4QAM=`1.14/0.70 dB`，16QAM=`2.45/2.14 dB`（weak/strong） | absolute powers、所有曲线点 |
| Fig. 18 | x-axis=`average received optical power`；branch count 1/2/4/6，weak/strong，TS=320 | relative gains按 branch 数正文完整给出；证明 branch 条件会改变 sensitivity gain，不给 structural-lag ranking | absolute powers、完整 BER 曲线 |

因此，本地正文可确认的**绝对 receiver-power 点只有** 4QAM `-43 dBm` 与 16QAM `-37 dBm`，且二者是 CFO-sweep 的固定 condition，不是 Fig. 10 structural sweep 的已知 source point。其余 power sweep 的轴名、趋势与部分相对 sensitivity gain 可确认，完整 power ticks/绝对曲线不可恢复。

### Path / aperture / coupling / carrier / noise

| quantity | local FACT | source-use limit |
|---|---:|---|
| symbol rate / formats | 10 GBaud PM-4/16QAM | 可冻结 `T_s=0.1 ns`；320 symbols=`32 ns`（直接计算） |
| propagation | Fourier-transform phase screen；`z=10 km`；outer scale→infinity，inner scale→0 | phase-screen 数值实现仍缺 wavelength、input beam、screen/grid 与 propagation contract |
| turbulence labels | weak `C_n^2=1e-16 m^(-2/3)`；strong `1e-14 m^(-2/3)` | 这是 Wang phase-screen input，不等于 Gu `(alpha,beta)` |
| receiving aperture | `0.2 m` | 只给直径/口径，未给 aperture averaging / fiber-mode overlap 实现 |
| mean coupling | weak `67.3012%`；strong `4.8395%` | 只有均值；无 coupling distribution、phase、branch covariance |
| diversity | 1/2/4/6 branches；各 telescope 接收 independent fading optical signal | 没有生成独立 branch 的数值 seed/space-separation contract |
| CFO | random open `(-1.1,+1.1) GHz` | truth 仅 scorer 使用；可以 source-grounded 地配对生成 |
| Tx laser | ECL linewidth `50 kHz` | wavelength、Tx optical power UNKNOWN |
| per-branch LO | linewidth `50 kHz`，output `15 dBm`，branches share one LO | combined Wiener linewidth 可按 independent Tx/LO 建模为 100 kHz，但是否独立与精确 PN discretization未在 Wang 写明 |
| photodiode | responsivity `0.8 A/W`，BPD coherent receiver | optical hybrid/split/gain、bandwidth、load/TIA UNKNOWN |
| receiver noise | shot + thermal considered；Eq. (3)/(4) 只把总噪声写成 Gaussian `N_x,N_y` | 无 variance/PSD/temperature/bandwidth；不能闭合 dBm→electrical SNR |
| DSP chain | IQ imbalance → FS → branch phase correction → MRC → pol demux → FOE → phase estimator → DD-LMS → demap/BER | 正文未出现 AGC、RSSI、power estimator 或 structural-action feedback |

### B0 source anchors

1. 320-symbol paper defaults：PM-4QAM `(B_N,B_L)=(16,20)`；PM-16QAM `(8,40)`。
2. 960-symbol defaults：PM-4QAM `(24,40)`；PM-16QAM `(16,60)`。
3. structural qualitative anchor：fixed length 下，proposed accuracy 随 `B_L` 先改善，之后可能因 fine precision/range tradeoff 退化；设计还受 modulation、received power、total TS length 影响。
4. B2B fixed-power anchor：4QAM `-43 dBm`、16QAM `-37 dBm` 下，proposed 文本量级为 `1e-8~1e-9`，conventional TS 约 `1e-7`；不是可逐点校准的完整数据。
5. low-power trend：proposed 在很低 received power 时可能差于对手；power 增加后快速改善、稳定并胜过三对手。

这些 anchor 能检查实现是否方向完全错误，但不足以冻结 scientific calibration tolerance：Fig. 10 的 power、action ticks、逐点 NMSE均 UNKNOWN，且 dBm 无法唯一变成仿真噪声。

## Structural action and paired-latent contract

### 320-symbol structural action set

由 `N_TS=B_N B_L=320`、`B_L` even、`B_N/2` even 得到的 structurally admissible set 为：

| action `B_L` | required `B_N` |
|---:|---:|
| 2 | 160 |
| 4 | 80 |
| 8 | 40 |
| 10 | 32 |
| 16 | 20 |
| 20 | 16 |
| 40 | 8 |
| 80 | 4 |

只有 `(16,20)`（320 PM-4QAM）与 `(8,40)`（320 PM-16QAM）是正文明确的 paper defaults；其余是结构推导点，不得写成 paper-tested actions。

每个 action 必须重新生成 FSTS，不能只改 estimator lag。随 `B_L` 必须联动：

- `B_N=320/B_L`、每 half 的 block 数 `B_N/2`、block boundary 与 adjacent-block pairing；
- X/Y 的 adjacent-block swap、block 内 adjacent-symbol swap、front/back conjugate-symmetry layout；
- coarse/fine 的 `i,j` ranges 与 fine pair indices；总项数可仍为 160，但索引和被乘样值已改变；
- fine divisor `B_L` 与 inferred unambiguous residual interval `[-R_s/(2B_L),+R_s/(2B_L)]`；
- action-specific `tx_x/tx_y` 及其 channel output。

正文未给 PRBS polynomial、initial state、bit→training-symbol mapping。Diagnostic 可固定一个 canonical base-PRBS reservoir 并让所有 actions 确定性消费同一 reservoir；这是公平性工程约定，不是 exact source PRBS reproduction。

### 合法 paired cluster

结构动作的 paired unit 应是**共享外生 latent cluster**，不是共享 received samples：

```text
cluster c = {
  canonical_base_prbs,
  channel/phase-screen-or-transfer latent,
  common CFO,
  Tx/LO phase-noise innovations,
  thermal-noise standard innovations,
  shot-noise primitive innovations
}

tx[a] = build_fsts(base_prbs, B_L=a, B_N=320/a)
rx[a] = receiver_model(tx[a], shared_exogenous_latents)
score[a] = scorer(rx[a], shared_truth)
```

强制语义：

1. 所有 action 共享 `cluster_id`、CFO、同一时间索引的 channel/PN realization 和 primitive noise innovations；action loop 顺序不得推进 RNG。
2. `tx_sha256[a]` 和 `rx_sha256[a]` **预期不同**。只校验 latent hashes/condition 相同，禁止把 `rx_sha256` 相同当 pairing 要求。
3. thermal AWGN 可复用同一 standard-normal draw；若 shot-noise variance 随 action-specific instantaneous optical power 变化，应复用 primitive draw后按各 action 的 source equation缩放，不能强迫最终 noise arrays 相同。
4. 所有 action 保持相同 total TS length、symbol rate、average transmitted energy、branch count、power condition、CFO distribution 与 scoring population；否则 action effect 与 task change 混叠。
5. paired delta/CI 以 `cluster_id` join；报告应明确是 correlated counterfactual，不是 “same rx”。

该合同足够支撑 formula/diagnostic smoke；只有 channel/noise/source calibration闭合后才可能支撑 performance terminal。

## B2 action-before observability

### 原 chain

Wang 的明确 receiver chain 只有 BPD/ADC 后的 IQ recovery、FS、branch phase correction、MRC、pol-demux、FOE、phase estimator、DD-LMS、demap/BER。全文未出现 AGC、received-power estimator、RSSI、common probe、previous-frame power state、feedback/control signaling。

更关键的是，structural action `(B_N,B_L)` 已写进**发端当前 320-symbol FSTS**。因此，从当前 action-specific FSTS 样值计算的 `mean(|r_X|^2+|r_Y|^2)` 是 action-after observation：它可供 scorer/后续帧使用，不能反过来决定已发出的当前 FSTS structure。

| possible information source | causal status | task / overhead impact | 当前能否合法冻结为原 Q1 B2 |
|---|---|---|---|
| 当前 FSTS 自身 power estimate | action 后才可得，且 proxy可能 action-dependent | 无新增 overhead，但存在时间倒置/泄漏 | **不能** |
| action-independent common probe/preamble | probe 后 receiver 可估 power | 增加 training overhead；还需要 receiver→transmitter feedback、guard/重配置，再发送选定 FSTS | **不能**；这是新 protocol/task |
| previous-frame estimate | 对下一帧因果可得 | 需 frame-to-frame channel continuity、feedback/control message、one-frame latency、fallback与stale-state规则；显式 probe overhead可为零但控制开销非零 | **不能按当前合同**；需 scope change |
| 发端预知 link-budget/predicted power | 发端可先选 action | 不再是 receiver-visible measured-power B2；预测误差/更新源需新定义 | **不能冒充当前 B2** |

Valjus 仅给出一般大气 scintillation/pointing coherence time通常 `>1 ms`；相对 32 ns FSTS，它支持 previous-frame 思路的**物理可讨论性**，但不提供 Wang frame interval、feedback latency、power-estimator 或 action signaling。故 previous-frame B2 不是本地可直接冻结的小修复，而是研究对象从“当前 FSTS condition dependence”变成“带反馈和状态生命周期的跨帧 adaptive FSTS”。

结论：B0/B1 fixed structural action可执行；B2 若只离线按 truth power 分 cell，则是 oracle-like diagnostic comparator，不是 deployable conditioned lookup。原 Q1 的 receiver-visible B2/actionability门目前为 hard blocker。

## Cn2/channel transfer

### 从 Wang 可确认的 inputs

- `C_n^2={1e-16,1e-14} m^(-2/3)`；`L=10 km`；outer→infinity、inner→0；receiver aperture `0.2 m`；weak/strong mean coupling=`67.3012%/4.8395%`。
- wavelength、plane/spherical/Gaussian beam identity、beam waist/curvature、phase-screen count/spacing、grid extent/resolution、subharmonics、transmit field、SMF mode-field radius与 overlap integral均 UNKNOWN。

### 可写出的 GG symbolic transfer

Gu 的 plane-wave、negligible-inner-scale公式为：

\[
k=\frac{2\pi}{\lambda},\qquad
s\equiv\sigma_l^2=1.23 C_n^2 k^{7/6}L^{11/6},
\]

\[
\alpha=\left[\exp\!\left(\frac{0.49s}{(1+1.11s^{6/5})^{7/6}}\right)-1\right]^{-1},
\]

\[
\beta=\left[\exp\!\left(\frac{0.51s}{(1+0.69s^{6/5})^{5/6}}\right)-1\right]^{-1}.
\]

输出是 normalized scalar irradiance `I=X*Y` 的 GG parameters；它不是 spatial complex field。Wang 缺 `lambda` 与 wave identity，故即使 `C_n^2,L` 已知，`s,alpha,beta` 仍不唯一。不得自行补 1550 nm 或其他“典型值”。

Gu 直接给出的 `(alpha,beta,s)`：weak `(11.6,10.1,0.2)`、strong `(4.2,1.4,3.5)`，是 Gu 自己的 plane-wave condition points。`params.py:100-170` 忠实记录了这条 provenance；它们没有由 Wang 的 `C_n^2=1e-16/1e-14`、10 km 算出，只能标：

`GU_PLANE_WAVE_GG_TRANSFER_NOT_WANG_PHASE_SCREEN_EQUIVALENT`。

### Phase-screen替代为何未闭合

Wang 只声明 Fourier-transform phase-screen model，没有给本地可执行方程/参数。一个可复现 phase-screen至少要冻结：

- input complex field `U_0(x,y)`、`lambda` 与 propagation geometry；
- Kolmogorov/von-Karman spectrum normalization、screen count/`Delta z`、FFT grid/extent、high/low-frequency compensation；
- per-screen phase realization与 split-step/Fresnel propagator；
- receiver aperture与 SMF mode overlap，输出 per-branch complex coupling coefficient、irradiance与 phase。

当前 input不足，无法唯一输出 Wang 的 `I,phi,eta` 或其 branch joint distribution。用 scalar GG 替代将丢失：spatial phase、aperture averaging、beam wander/modal distortion、SMF coupling fluctuation、phase-coupling相关性、branch correlation与 Wang 已给的 mean-coupling机制。它最多保留一个 normalized irradiance marginal。

最多只能写出不具 source-calibration 权限的 schematic：

\[
U_{m+1}(x,y)=\mathcal P_{\Delta z_m}\{U_m(x,y)e^{j\phi_m(x,y)}\},
\qquad
\eta_m=\frac{|\iint_A U_m(x,y)u_{SMF}^{*}(x,y)\,dxdy|^2}
{\left(\iint_A|U_m|^2\right)\left(\iint_A|u_{SMF}|^2\right)}.
\]

输入应为 complex field、screen phase与传播/接收配置，输出是 receiver-plane complex field和 SMF coupling；但 `\mathcal P`、`\phi_m` 的 PSD/normalization及 `u_SMF` 均未由当前 Wang local source冻结，所以该 schematic 不能实例化为 Wang-equivalent channel。

即使给 GG 乘上 `67.3012%/4.8395%` 的均值，也只是 moment-matched transfer；它不能验证依赖 phase-screen/coupling机制的 structural-lag ranking，更不能对 no-crossover 发 scientific Kill。

## Power-to-SNR/noise closure

Wang 的可恢复 sample model是：

\[
R_{X/Y}(k)=\gamma\sqrt{\eta I P_{LO}}S_{X/Y}(k)
e^{j(\varphi+\theta_k+\theta_{x/y}+2\pi f kT_s)}+N_{X/Y}(k),
\]

其中 `gamma=0.8 A/W`、`P_LO=15 dBm`，`N` 只被称为 coherent receiver 引入的 Gaussian noise；正文另称 shot/thermal noise 均考虑。若要从 paper power axis建立 electrical SNR，至少还需唯一冻结：

\[
P_{rx}[W]=10^{(P_{rx}[dBm]-30)/10},\qquad
\mathrm{SNR}_{elec}=\frac{E[|A(P_{rx},P_{LO},\gamma)S|^2]}
{\sigma^2_{shot}+\sigma^2_{thermal}+\sigma^2_{other}}.
\]

但 Wang 没有说明 `eta I` 与图中 average received optical power 的精确 accounting，也没有给出 `Var(N)`。缺失量至少包括：

- optical hybrid/BPD splitting factor、per-polarization/per-branch power accounting、BPD/TIA gain；
- electrical equivalent noise bandwidth / matched-filter bandwidth / sampling and integration convention；
- shot-noise PSD所需的 detector convention、dark/background current与 LO/signal contribution factor；
- thermal-noise current PSD或 temperature/load resistance/TIA input-noise density；
- ADC scaling/quantization、MRC weights与 branch noise combination；
- normalized `S_X/S_Y` energy以及 received-power 是 coupling 前还是后的定义。

因此 `responsivity + LO power + “shot/thermal considered”` 不足以唯一恢复 SNR/noise。

现有 common DP channel 在 `projects/simulation/common/_dual_pol_channel.py:126-132` 明确采用 dimensionless contract：`nv=1/(2*gamma_bar)`，然后注入 complex standard Gaussian。focused tests只验证 same-seed reproducibility/legacy equality，不提供 `gamma_bar↔dBm` 物理映射。它可供 diagnostic 使用，不能把 `10/20 dB` 或任意 `gamma_bar` 改名为 Wang receiver optical power。

## B0 calibration gate

最小、非循环的 source calibration gate 应在看 structural ranking 前冻结并同时满足：

1. **Identity gate**：320-symbol PM FSTS、Eq. (7)→coarse compensation→Eq. (8)–(11) noiseless identity、default `(16,20)/(8,40)` 与 range/wrap均通过。这只证明公式实现，不是 performance calibration。
2. **B2B fixed-power gate**：按 source receiver/noise equation，在 10 GBaud、Tx/LO各 50 kHz、CFO uniform `(-1.1,+1.1) GHz`、每 point 800 repeats 下：
   - PM-4QAM、320 default在 `-43 dBm` 的 NMSE量级与 Fig. 11 文本 anchor一致（proposed `1e-8~1e-9`，conventional TS约 `1e-7`）；
   - PM-16QAM、320 default在 `-37 dBm` 同样复现 Fig. 12 的量级/相对次序；
   - truth不能用于 estimator；同一 source noise model作用于 proposed与 conventional baseline。
3. **Structural trend gate**：在 Fig. 10 的**原 source power和原 action ticks**上，复现 `B_L` 先改善、后可能退化的趋势，并让 320 paper-design point为4QAM `(16,20)`、16QAM `(8,40)`；需要预先给出 digitized target/tolerance，不能看结果后选择。
4. **Low-power trend gate**：在 Fig. 11/12 source power axis 上复现“very low power proposed可能落后；power增大后改善、稳定并胜过对手”，且转折位置落入预冻结 tolerance。

当前材料只足以写 gate 1 与 gates 2–4 的文字方向；不能填 gates 2–4 所需的唯一 noise equation、Fig. 10 power/action ticks、逐点 target/tolerance。因此 B0 calibration gate当前=`NOT_EXECUTABLE_FROM_LOCAL_SOURCE`。Noiseless identity或调一个 synthetic SNR使某点“看起来像”均不得替代。

## Recoverable gaps vs hard blockers

### Recoverable gaps（若新增明确本地输入）

| gap | 最小新增输入 | 能关闭什么 |
|---|---|---|
| Wang 图坐标/曲线缺失 | canonical PDF或 Fig. 5–18 原图落到本地；预先登记 digitization方法 | power/action ticks、Fig. 10 curve、B0 numeric tolerance的一部分 |
| exact PRBS缺失 | authors' PRBS polynomial/seed/mapping或 source code | exact source waveform，而非任意 deterministic PRBS |
| phase-screen配置缺失 | Wang/其引用 [30] 对应的完整 simulation config/code | wavelength/beam/grid/screens/SMF coupling与 branch realization |
| receiver noise缺失 | authors' receiver/noise config/code，含 bandwidth/TIA/BPD/ADC accounting | dBm→electrical sample/noise的唯一映射 |

### Hard blockers under current Q1/local-evidence scope

1. **Structural causality**：当前 received-power estimate在 action-specific FSTS 之后；原 chain没有 probe/previous-frame/feedback。修复会改变 protocol、overhead或state lifecycle，不能作为原合同内小补丁。
2. **Source channel non-equivalence**：Gu scalar GG不是 Wang phase-screen/SMF coupling；当前输入无法证明 condition mechanism保真。
3. **Power/noise non-identifiability**：同一 dBm可对应多组未报告 bandwidth/noise/gain，从而给不同 lag ranking；以结果反调 noise是循环校准。
4. **B0 numeric gate不可冻结**：没有 source point + source equation + numeric tolerance的闭环，任何 performance crossover/no-crossover都只能归属于 synthetic diagnostic domain。

即使恢复 PDF/figure，1–3 仍在。因此原 Q1 不能靠“再找一个本地图”升级为 source-calibrated scientific smoke。

## Recommended unique next action

**不要恢复 T014 scientific grid。将原 Q1 交回 owner，按 D009 terminal 5 处理为 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`；任何后续 structural run 只能另标 `DIAGNOSTIC_ONLY / NO_Q1_TERMINAL`。**

只有用户显式 scope-change 到“previous-frame/common-probe + feedback-controlled structural FSTS”，并取得可执行的 Wang receiver/channel source config 后，才能重开 source calibration；在此之前不应运行 performance grid、据 synthetic SNR/GG 下 Kill/Resolved，也不应构造 C1。

## Evidence pointers

- `.sessions/2026-08-08-rml-fsts-groundwork/T015-step4a-source-calibration-audit.md`：问题、唯一 verdict 集与禁止项。
- `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md:130-156`：V006 的 structural-identity 与 source-calibration P0。
- `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:256-305,307-353`：D009 terminal、B2/observability contract，以及被拒 D010。
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`：Wang Eq. (1)–(11)、structural action set、paper defaults与 existing-code gap。
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`：dimensionless SNR、shared-realization assets、information boundary与 raw contract。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/metadata.json`：local HTML provenance；source PDF absent。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:103-107,119-160,175-215`：FSTS structure、receiver stage、Eq. (3)–(11)。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:231-243`：10 GBaud、phase-screen path、`C_n^2`、aperture、coupling、LO/responsivity/noise与 DSP chain。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:247-267`：FS received-power/length trend与 sensitivity相对值。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:279-329`：NMSE thresholds、Fig. 9–13 axes/trends、`-43/-37 dBm` anchors与 paper defaults。
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:339-381`：weak/strong、single/four/multi-branch receiver-power sweeps与 relative gains。
- `D:/code/study/research-protocol/papers/doi/10.3390_app12073331/content.md:90-117`：Gu plane-wave GG equations及其独立 `(alpha,beta,s)` points。
- `D:/code/study/research-protocol/papers/doi/10.1117_1.1386641/content.md:39,55,97-119,145-185`：Al-Habash GG的适用对象、Rytov/wavelength/path依赖、plane/spherical distinction。
- `D:/code/study/research-protocol/papers/doi/10.1002_sat.1553/content.md:111,167,387-395,438-440`：coherent receiver chain、atmospheric coherence time与 linewidth/phase-noise语义；只作 transfer plausibility，不冒充 Wang source。
- `projects/simulation/params.py:100-170`：Gu GG provenance与不可冒充 Wang 的参数血缘。
- `projects/simulation/common/_dual_pol_channel.py:95-132`、`projects/simulation/tests/test_dual_pol_shared_channel.py:71-126`：dimensionless `gamma_bar` channel与 reproducibility evidence；无 dBm mapping。
