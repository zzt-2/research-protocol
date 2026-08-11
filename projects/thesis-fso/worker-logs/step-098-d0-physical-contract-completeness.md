# Step 098 — D0 physical/testbed 参数唯一性独立审计

> 2026-08-10 | action class: `SOURCE_AUDIT` | control: CP011 / epoch 11 / T052
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> audited HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`
> discipline: 静态、只读反向穷举；未 import、pytest、运行 D0/仿真、web/search/download，未修改 owner/源码/治理，未 commit/push

## 0. Findings first / verdict

`verdict = PHYSICAL_CONTRACT_AMBIGUITY`

当前 source closure **不能唯一构造**一个 supplied-waveform D0 realization。已冻结的部分包括：`R_s=2.5e9`、`T_s=4e-10 s`、`alpha/beta=1.0/0.7`、四档 SNR、三档线宽数值、`CFO=0`、共享 GG/共享 carrier phase、X/Y 独立 AWGN、square-16QAM BPS kernel/grid，以及 controlled fixture 在 common-BPS 输出后的注入位置。以下四组却仍有两个以上科学上不等价的出口，且现有 owner 没有选择：

1. **GG 时间尺度**：`params.py` 的默认 `f_G=100 Hz`，adaptive-phase-window 实际 GG slice 使用 `500 Hz`，P08-R2 又把 `100/1000 Hz` 当物理轴；D0 的 12 个 cell 没有 `f_G` 维度，也没有固定值。
2. **Wiener 线宽语义**：D0 冻结了 `{10,20,80} kHz` 数字，但没有说明它们是单端激光 linewidth，还是 Tx+LO combined linewidth。`params.py` 把 `LASER_LW` 写成“单端”，adaptive channel 却直接把传入值代入 combined carrier-phase innovation `2*pi*Delta_nu*T_s`。这会产生至少 2 倍 innovation variance 差异，直接改变 S1 natural occurrence。
3. **SOP/prefix/equalizer**：adaptive physical slice 是 scalar/single-pol、无 SOP；P08-R2 使用 `sop_rate=1e-5` 的 2x2 mixing，但其 X/Y prefix 完全相同，使四未知量 LS 只有 rank 2。D0 owner 没有 SOP/Jones/equalizer字段，不能在“加 distinct prefixes 并保留 2x2 mixing”和“identity SOP + per-pol scalar chain”之间静默选择。
4. **receiver noise semantics**：P08 prefix residual 返回的是 `mean(|e|^2)`（complex variance），而 B2 source mapping 明确把 Gaussian likelihood 的 `nu` 定义成每实维 variance；P08 max-log demapper又按 `1/(2*sigma2)` 使用输入。D0 的 `noise_var` 没有冻结 pre/post-equalization、per-real/complex、per-pol/shared 及换算点，存在精确 2 倍尺度分叉。

这些不是运行后才能发现的性能风险，而是 constructor 无法实例化的前置合同歧义。它们尚未证明 `>7D_HARD_BLOCKER`：最小出口仍是 owner 一次性冻结并投影字段；但在该动作发生前，任何实现都会替 owner 做科学选择。

## 1. supplied-waveform realization 的反向 constructor BOM

一个完整 D0 realization 不是只传 `tx` 和 `snr_db`；至少要在构造时闭合下列四层。伪签名只表示信息合同，不建议在本任务建代码：

```text
build_d0_realization(
  waveform_X, waveform_Y, known_X, known_Y, known_mask,
  data_to_time, time_to_data, root_seed, rng_substream_contract,
  R_s, T_s,
  gg_alpha, gg_beta, f_G, tau_c_rule, gg_block, gg_method,
  linewidth_value, linewidth_semantics, phase_innovation_rule, phase_initial_state,
  residual_cfo_hz, phase_shared_XY,
  sop_model, sop_parameters,
  snr_db, awgn_variance_rule, awgn_shared_XY,
  fade_phase_noise_independence,
  prefix_sequence_receipt, periodic_pilot_sequence_receipt,
  pre_eq_estimator, equalizer, post_eq_noise_estimator,
  bps_B, bps_Nw, bps_edge_rule,
  controlled_injection_stage, controlled_suffix_scope,
) -> (ReceiverView, TruthView, CarrierReceipt)
```

### 1.1 Waveform/time support

| Input | Required value/meaning | Status | Evidence |
|---|---|---|---|
| `waveform_X/Y` | 两个 supplied complex arrays；均含 32 prefix、全部 6144 coded data、periodic pilots 和 terminal pilot；不得 replace/puncture coded symbols | `FROZEN` for layout, symbol bytes unresolved | D0 YAML `132-143`; step-095 `50-74` |
| `N_time` | tuple 冻结后分别为 `6860/6501/6240/6208`（`N=10/20/100/200`，均已含 prefix） | `FROZEN` | step-095 `50-72` |
| `known_mask`, `data_to_time`, `time_to_data` | prefix/pilot 为 known；6144 data rank 与 absolute time 双射，pilot 映射为 `-1` | `FROZEN` in structure | D0 YAML `132-143`; step-094 `122-129` |
| `prefix length` | 32 symbols | `FROZEN` | D0 YAML `132-139`; P08 `p08r_chain.py:185-202` |
| `prefix X/Y bytes` | 每个 pol 的实际已知 symbol sequence、seed/algorithm、SHA256、是否相同 | `AMBIGUOUS` | P08 只给单 sequence seed `987654321`，并复制给 X/Y (`p08r_chain.py:195-202,314-317`); D0 YAML未给 bytes/seed |
| `periodic pilot bytes` | pilot constellation、能量、循环序列、X/Y 是否相同及 SHA256 | `AMBIGUOUS` | D0 YAML只给 placement (`132-155`); adaptive channel另有 QPSK 四符号循环 (`channel.py:158-170`)，但 owner 未选择它 |

### 1.2 GG envelope

| Input | Required value/meaning | Status | Evidence |
|---|---|---|---|
| `alpha,beta` | uplink-strong `(1.0,0.7)` | `FROZEN` | D0 YAML `64-71`; `params.py:197-215`; source closure `161-168` |
| amplitude convention | intensity `h=X*Y`，field multiplier `sqrt(h)` | `FROZEN` | `_gg_time.py:16-25,104-157`; adaptive `channel.py:191-197` |
| `f_G` | 一个 population-wide fixed value；不能新增未登记 cell 轴 | `AMBIGUOUS` | D0 12 cells only由 4 SNR × 3 linewidth 构成 (`64-73,98-105`); `params.py:1147-1170` 给 default `100`/sweep `30,100,300,1000`; adaptive `channel.py:50-64,181-187` 用 `500`; P08-R2 `p08r2_phaseA.py:58-63` 用 `100/1000` |
| `tau_c` | `1/(2*pi*f_G)`，不应同时作为独立自由参数 | rule `FROZEN`, value `AMBIGUOUS` with `f_G` | source closure `164-168`; `params.py:1172-1184,1273-1287`; `_gg_time.py:106-144` |
| `gg_block` | 100 symbol 的块内常量 envelope | `IMPLIED_BUT_NEEDS_PROJECTION` | source closure `164-168`; `params.py:490-501`; common config `_config.py:15-17`; adaptive channel调用 `BLOCK` (`channel.py:181-187`) |
| `gg_method` | `gar` exact-Gamma-margin AR(1) | `IMPLIED_BUT_NEEDS_PROJECTION` | `params.py:1235-1245`; common generator resolves default (`_dual_pol_channel.py:95-113`); adaptive channel hardcodes `gar` (`channel.py:181-187`) |
| fade sharing | 同一 `h[n]` 供 X/Y | `FROZEN` | D0 YAML `70-72`; common channel `_dual_pol_channel.py:103-132` |

### 1.3 Carrier phase, CFO, SOP and AWGN

| Input | Required value/meaning | Status | Evidence |
|---|---|---|---|
| `R_s,T_s` | `2.5e9 baud`, `4e-10 s` | `FROZEN` | D0 YAML `64-68`; source closure `152-154`; `params.py:48-72` |
| linewidth numeric grid | `{10000,20000,80000} Hz` | `FROZEN` | D0 YAML `64-68`; source closure `155-160` |
| linewidth identity | 数值究竟是 effective combined `Delta_nu_Tx+Delta_nu_LO`，还是每个单端激光值 | `AMBIGUOUS` | `params.py:84-94` 明写单端；adaptive `_wiener_phase`直接将入参当 phase-process `Delta_nu` (`channel.py:98-108`); D0 YAML只有 `linewidth_hz` |
| Wiener innovation | `epsilon_n ~ N(0, 2*pi*Delta_nu_effective*T_s)`，`theta=cumsum(epsilon)` | `IMPLIED_BUT_NEEDS_PROJECTION` after linewidth identity freezes | adaptive `channel.py:98-108,172-176`; common `_channel.py:35-54` |
| initial phase/indexing | pre-symbol state为 0，symbol 0 已含第一项 innovation（即 `theta[0]=epsilon[0]`）；不另抽 uniform phase | `IMPLIED_BUT_NEEDS_PROJECTION` | 两个现有 phase实现均直接 `cumsum` (`channel.py:105-108`; `_channel.py:50-54`) |
| phase sharing | X/Y 使用同一 physical `theta[n]` | `FROZEN` | D0 YAML `70`; B2 transfer `121-125` |
| residual CFO | primary population固定 0 Hz；无 `f_dot`/100 MHz sweep | `FROZEN`; nonzero CFO `OUT_OF_SCOPE` | D0 YAML `68`; adaptive source `channel.py:19-23,64,175-176` |
| SOP/Jones model | identity/no mixing，或 P08 linear rotation `theta_sop=sop_rate*n`，以及任何 MIMO compensation | `AMBIGUOUS` | adaptive physical source为 scalar channel (`channel.py:142-213`); common DP/P08需要 `sop_rate`并做 2x2 rotation (`_dual_pol_channel.py:56-68,123-132`; `p08r2_phaseA.py:94-95`); D0 YAML无 SOP 字段 |
| SNR definition | `gamma=10^(snr_db/10)`，unit-average pre-fade symbol energy | `FROZEN` | D0 YAML `64-72`; adaptive `channel.py:191-195` |
| physical AWGN variance | 每实/虚维 `nu=1/(2*gamma)`；complex `E|n|^2=1/gamma`；noise在 fade/phase/(若有)mixing 后相加 | `FROZEN` | adaptive `channel.py:191-197`; common DP `_dual_pol_channel.py:123-132`; P08-R2 `p08r2_chain.py:221-228` |
| AWGN X/Y sharing | X/Y 独立噪声，但同一 method-paired realization/no-jump twin必须复用相同数组 | `FROZEN` | D0 YAML `70-73,141-143,221-224`; common DP `_dual_pol_channel.py:126-132` |
| RNG substreams | payload、GG、Wiener、X-noise、Y-noise 的 seed派生和相互独立性；controlled twin只改 jump flag | `IMPLIED_BUT_NEEDS_PROJECTION` | D0只给 root seed ranges (`79-88`); adaptive source把 bits/Wiener/AWGN放同一 stream且 GG另以同 seed起流 (`channel.py:155-158,172-187,193-195`); P08-R2又用 `seed+1000003` 单独画 noise (`p08r2_chain.py:216-228`) |

### 1.4 Receiver front end and controlled fixture

| Input/semantic | Required value/meaning | Status | Evidence |
|---|---|---|---|
| pre-EQ noise estimator | 2x2 LS complex residual，或 no-SOP per-pol scalar residual；variance单位与 degrees-of-freedom | `AMBIGUOUS` | P08 2x2 LS `p08r2_chain.py:77-145`; rank defect见 step-094 `38-43,60-64` |
| equalizer | 是否启用、估计量、block size、MMSE公式、phase是否只留给BPS、`amp_limit=3` 是否继承 | `AMBIGUOUS` | D0只说 `received_and_equalized_samples` (`32-40`); adaptive source无 equalizer；P08使用 block-power h + common MMSE + clip (`p08r2_chain.py:236-277`; `_equalizer.py:5-15`) |
| post-EQ demapper variance | per-pol还是shared；prefix还是prefix+pilots；complex variance到per-real `nu` 的 `/2` 位置 | `AMBIGUOUS` | P08 `estimate_sigma2_from_prefix=mean(|e|^2)` (`p08r_chain.py:205-216`); max-log使用 `1/(2*sigma2)` (`p08_coded_chain.py:83-105`); B2 mapping要求 `nu` 为每实维 (step-095 `112-128`) |
| BPS kernel/grid | common `bps_cpr(...,mod='qam16')`, `B={32,64}`, `Nw={31,61,127}`，dev冻结唯一 pair | `FROZEN` | D0 YAML `90-108`; step-094 `131-137`; `_recovery.py:91-118` |
| BPS edge handling | `np.convolve(metric, ones(Nw)/Nw, mode='same')` 的 implicit zero padding，边缘仍除完整 `Nw`；phase为 `unwrap(4*pe_raw)/4` | `IMPLIED_BUT_NEEDS_PROJECTION` | 精确 implementation asset由D0指向 (`90-93`); kernel `_recovery.py:98-118` |
| controlled injection stage | common BPS 输出后、method前；不是 physical channel input | `FROZEN` | D0 YAML `213-224`; step-094 `122-129` |
| suffix scope | 从 boundary后的第一个 data absolute time起，目标pol的所有后续 physical-time samples均乘 `exp(j*k*pi/2)`，包括后续 periodic/terminal pilots；sentinel pol byte-identical | `IMPLIED_BUT_NEEDS_PROJECTION` | owner给 persistent boundary、target-pol、common-BPS injection (`199-224`); step-094闭合 absolute-time解释 (`122-129`) |
| C1 trigger/fallback/callback | 不属于D0 constructor | `OUT_OF_SCOPE` | D0 YAML `24-30,391-401` |

## 2. `f_G / block / method / tau` 的唯一性判定

1. `block=100` 与 `method=gar` 可以从 source closure → `params.py` → common/adaptive caller形成唯一链，只差在 D0 owner 明示投影，因此是 `IMPLIED_BUT_NEEDS_PROJECTION`，不是科学歧义。
2. `tau_c=1/(2*pi*f_G)` 的函数也唯一；但其数值随 `f_G`，不能单独冻结。
3. `f_G` 没有唯一链。source closure只写“`f_G canonical, frozen`”而未给数值（`source-closure.yaml:164-168`）；其 implementation sibling把 `500` 写成 canonical（`channel.py:50-64`），参数 owner把 `100` 写成 default 并要求 sweep（`params.py:1147-1170`），P08-R2使用 `100/1000`（`p08r2_phaseA.py:58-63`）。D0 owner又只有 12 个 SNR×linewidth cells，没有 fG axis。实现者不能猜 100、500 或1000，也不能擅自扩成 36 cells。

最小修复是 owner 明示一个 `f_G_hz`，同时记录由它导出的 `tau_c_s` 和 `rho_block`；本审计不替 owner选值。

## 3. prefix rank 缺陷的两个出口

### 3.1 出口 A：distinct prefixes + rank-4 2x2 LS

该出口只有在 D0 **明确包含非平凡 SOP/cross-pol mixing** 时才合法。它至少还需要：

- 两条 polarization-distinct/orthogonal known prefix及其 bytes/hash；
- `rank(M)=4`、condition number与 residual degrees-of-freedom；
- SOP/Jones trajectory 的初值、rate/model、是否在prefix内近似常量；
- 实际使用 `H_eff` 的 2x2 equalizer，而不是像 P08-R2那样只返回 `H_eff` 做diagnostic后继续两个 scalar power equalizers。

仅把 prefix 换成distinct无法闭合 MIMO front end。P08-R2 的 `estimate_pre_eq_noise_from_prefix` 能在 rank 4 时估计常量 `H_eff`，但后续 `equalize()`并未用它消除 cross-pol mixing（`p08r2_chain.py:252-277`）。长达约 6208–6860 symbols 的 frame 若继续使用 `sop_rate*n`，prefix常量LS与后续time-varying Jones也不是同一个模型。因此该出口会新增 owner 当前未定义的 physical axis和equalizer action，不是“只修rank”。

### 3.2 出口 B：identity SOP + scalar per-pol estimator

这是与**当前 D0 population 最小且单义相容**的出口：

- D0只冻结共享 scalar GG fade、共享 carrier phase、X/Y独立AWGN和per-pol独立CPR（YAML `64-73`）；
- B2 transfer明确写成“shared physical phase process 后 dual-pol independent processing”（`121-125`）；
- adaptive-phase-window carrier source本身是scalar、无SOP（`channel.py:142-213`）。

因此，若不做 population amendment，owner应投影 `sop_model: identity_no_cross_pol_mixing`，并把prefix calibration定义为每pol scalar、receiver-only估计。此时X/Y使用同一known sequence不再导致identifiability缺陷；仍需分别receipt两条实际序列和估计输出。

**裁决**：当前最小出口是 B，不是 A。但因为 D0 owner目前没有 `sop_model` 字段，本审计只能判“应显式投影 B”，不能把该推断当作已经冻结的事实；这也是总 verdict 保持 `PHYSICAL_CONTRACT_AMBIGUITY` 的原因之一。

## 4. pre/post equalization noise 的必要分名

当前 `noise_var` 一个名字不足以复刻链路。最少要分开：

```text
awgn_var_per_real    = 1/(2*gamma)          # physical draw
awgn_var_complex     = 2*awgn_var_per_real  # E|n|^2
pre_eq_resid_complex = mean(|r-g_hat*s|^2)  # receiver estimate
post_eq_var_per_real = 0.5*mean(|z-s|^2)    # demapper/B2 likelihood input
gamma_vis            = 1/pre_eq_resid_complex  # only if equalizer formula keeps this convention
```

最后两式只有在 owner 选择具体 scalar equalizer后才可冻结；这里仅显示单位关系。若把 P08 `mean(|e|^2)` 直接当 `sigma2` 传给 `1/(2*sigma2)` demapper，LLR magnitude 会再缩小 2 倍。B0/B1/B2必须共享同一个 receiver-visible variance owner，不得分别继承不同factor。

## 5. common front end 与 injection 的最小顺序合同

能够与现有 owner 对齐的唯一顺序骨架是：

```text
supplied coded+prefix+pilot waveform
  -> shared GG field multiplier sqrt(h)
  -> shared Wiener/CFO carrier exp(j*phi)              # CFO=0 in current population
  -> [owner must freeze: identity SOP vs Jones mixing]
  -> independent X/Y AWGN
  -> receiver-only calibration/equalization            # exact algorithm currently ambiguous
  -> per-pol common square-16QAM BPS                    # exact kernel/grid
  -> controlled fixture: target-pol persistent suffix  # S2/S3/S4 only; include later pilots
  -> B0/B1/B2/O1 consumers
```

S1在BPS后只由evaluator读取 true phase与BPS trace识别自然state transition，不注入jump。S2 no-jump twin复用同一 waveform/fade/phase/noise/BPS output，只在copy-on-write fixture分支改变suffix。任何在physical channel前注入、只旋转data不旋转后续pilots、或让不同method重画noise的实现都改变estimand。

## 6. 最小 owner 字段树（必须先冻结；本任务未修改）

```yaml
physical_realization:
  model_id: supplied_waveform_flat_dp_v1
  symbol_rate_baud: 2.5e9
  symbol_period_s: 4.0e-10
  waveform:
    prefix:
      length: 32
      x_sequence_id: MUST_FREEZE
      y_sequence_id: MUST_FREEZE
      x_sha256: MUST_FREEZE
      y_sha256: MUST_FREEZE
    periodic_pilot:
      constellation_and_sequence_id: MUST_FREEZE
      x_sha256: MUST_FREEZE
      y_sha256: MUST_FREEZE
    layout_formula_id: d0_extframe_v1
  gamma_gamma:
    alpha: 1.0
    beta: 0.7
    field_multiplier: sqrt_intensity
    f_G_hz: MUST_FREEZE
    tau_c_rule: 1_over_2pi_fG
    block_symbols: 100
    method: gar
    shared_across_polarizations: true
  carrier_phase:
    linewidth_values_hz: [10000, 20000, 80000]
    linewidth_semantics: MUST_FREEZE_COMBINED_OR_PER_ENDPOINT
    innovation_variance_rule: 2pi_effective_linewidth_Ts
    initial_state_rule: zero_before_symbol0_then_first_innovation
    residual_cfo_hz: 0
    shared_across_polarizations: true
  polarization:
    sop_model: MUST_FREEZE  # minimal current-population projection: identity_no_cross_pol_mixing
    sop_parameters: MUST_FREEZE_OR_EMPTY
  awgn:
    snr_db: [10, 14, 18, 22]
    per_real_variance_rule: 1_over_2gamma
    complex_variance_rule: 1_over_gamma
    independent_across_polarizations: true
  rng:
    root_seed_from_seed_plan: true
    named_substream_derivation: MUST_FREEZE
    independent_components: [payload, gg, wiener, awgn_x, awgn_y]
  receiver_front_end:
    pre_eq_estimator_id: MUST_FREEZE
    equalizer_id_and_parameters: MUST_FREEZE
    post_eq_variance_id_and_units: MUST_FREEZE
    bps:
      implementation: common._recovery.bps_cpr
      modulation: qam16
      dev_grid: {B: [32, 64], Nw: [31, 61, 127]}
      edge_rule: numpy_convolve_same_zero_padding_full_Nw_denominator
  controlled_fixture:
    stage: after_common_bps
    suffix_scope: all_target_pol_times_from_boundary_including_later_pilots
    sentinel_pol: byte_identical
```

阻断字段是 `f_G_hz`、`linewidth_semantics`、`sop_model`、prefix/pilot sequence、receiver front-end三项及named RNG contract。其余未在D0 YAML显式出现但可从冻结来源唯一投影。

## 7. source receipt

### 7.1 本次静态输入 receipt

| Source | SHA256 | 承重内容 |
|---|---|---|
| `d0-defect-smoke-contract.yaml` | `32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936` | population/front-end/fixture唯一owner现状 |
| `adaptive-phase-window/source-closure.yaml` | `313AC17D759B02D014068EBB8B29137DB476F48E76506535E5975E3FDD20C1EC` | R_s/linewidth/GG parameter provenance |
| `adaptive-phase-window/channel.py` | `0D74F642A4C1E41113B0A8119D0379F10BC31011063968E7C52F83BE7D9BEED7` | actual Wiener/CFO/AWGN/GG caller及500-Hz冲突 |
| `params.py` | `0E87C53364461478EDDCD81426D8E04646270C3EA7AA717E3C3B28C5DD2A99E9` | canonical defaults/provenance |
| `common/_gg_time.py` | `D8E7929D00D885ECCF111EB96D80ECD3822B065CBF3ECA09ED31912C3DA73113` | GG AR(1) formula/method |
| `common/_dual_pol_channel.py` | `5CEFAC97D120E5590905AE36AB20CABC8832A6C556368B1D9F154A2A8091818C` | SOP/DP/AWGN implementation candidate |
| `common/_recovery.py` | `AFB8AED9508CC83EE13D05BFD4346A2E6F0852AF0E9D6A182A85A441FF5D60E2` | BPS kernel/edge behavior |
| `common/_equalizer.py` | `320115D96A6ED7C3B970371F47FC98FB5054510129F556F66D602EF7D38199B9` | optional P08 MMSE/limiter kernel |
| `p08r_chain.py` | `174DAAD20F4FADBB0710CDEE5FAF7D49F360B6A8A6609B9A1EA46CCB41288404` | prefix/post-EQ variance/coded identity |
| `p08r2_chain.py` | `50124850FD31C6CA96A8588C0F414D4187A3370B4682949D944F03E17E321430` | 2x2 LS/pre-EQ chain及rank问题 |
| `step-094-d0-coded-chain-asset-map.md` | `F291DD60A57DEB1238FD087F0113E141F2EA2738590E229AB9123EFCE36D5764` | direct-reuse boundary及D0 shell要求 |

### 7.2 每个未来 realization 必须写的 dynamic receipt

- contract/source hashes与git commit；resolved owner schema version。
- actual `N_time`、waveform/prefix/pilot hashes、data/time map hash。
- `alpha,beta,f_G,tau_c,block,method,rho_block`。
- linewidth raw values、combined/per-endpoint identity、derived innovation variance、initial-state/CFO rule。
- SOP model/parameters；phase/fade/noise X/Y sharing矩阵。
- SNR、per-real/complex physical variance、pre/post-EQ variance单位和数值。
- root seed和每个named substream seed/key；no-jump twin receipt。
- exact equalizer ID/parameters、BPS `(B,Nw)`、edge-rule ID和phase-trace hash。
- controlled fixture stage、target pol、boundary data-rank/absolute-time、rotation及suffix/pilot coverage。

## 8. 最小单测清单（未执行）

1. **constructor completeness**：上树任一 required 字段缺失即fail；禁止从函数default静默补 `f_G/SOP/equalizer/linewidth identity`。
2. **GG identity**：给定receipt重建 `tau_c/rho`；X/Y `h` byte-identical；`block=100`、`method=gar`；切换任一字段必须改变receipt/cache key。
3. **Wiener identity**：固定seed下phase确定；X/Y相同；`diff(theta)`方差目标为owner的 `2*pi*effective_linewidth*T_s`；验证symbol-0 indexing与CFO=0斜率。
4. **linewidth factor-of-two gate**：若owner选combined，禁止再次把Tx/LO求和；若选per-endpoint，receipt必须显式给两端值并只求和一次。
5. **AWGN units/sharing**：每实维/complex variance reference；X/Y cross-correlation≈0且数组不同；fade/Wiener/noise named streams互不复用；paired methods/no-jump twin noise byte-identical。
6. **SOP route gate**：若最小 no-SOP route，X-only impulse不得泄入Y且2x2 LS API不可达；若owner另行选择SOP route，则必须rank4、condition-number、Jones tracking与真正MIMO equalizer测试，不能只修prefix。
7. **prefix/pilot receipt**：实际bytes、seed/algorithm、X/Y relation与hash稳定；known masks和terminal pilot完整；6144 data逐个保留。
8. **variance factor gate**：complex residual到per-real likelihood variance只转换一次；B0/B1/B2在相同receiver output上读取同一variance owner；禁止2倍LLR尺度漂移。
9. **equalizer truth boundary**：API不接受true `h/SNR/phase/payload`；noiseless已知scalar channel恢复identity；block/clip/MMSE参数均由owner/receipt，不靠default。
10. **BPS edge reference**：6个 `(B,Nw)` 对长帧均与显式zero-padding/full-`Nw` reference一致；首尾 phase sample与整个trace finite/deterministic；未来若换edge rule必须合同版本变更。
11. **injection order**：controlled off twin与on case在BPS输出前byte-identical；on只改目标pol的boundary后suffix，包含后续pilots；sentinel pol byte-identical。
12. **natural/controlled separation**：S1路径没有fixture调用；S2/S3/S4 event receipt不会进入ReceiverView；method不得重画carrier/noise。

## 9. Terminal / protection

```text
PHYSICAL_SOURCE_AUDIT = COMPLETE
CONSTRUCTOR_UNIQUENESS = FAIL
PRIMARY_TERMINAL = PHYSICAL_CONTRACT_AMBIGUITY
>7D_HARD_BLOCKER = NOT_ESTABLISHED
MINIMAL_CURRENT_POPULATION_PREFIX_EXIT = NO_SOP_SCALAR_PER_POL / OWNER_PROJECTION_REQUIRED
IMPLEMENTATION_OR_D0_RUN = NOT_AUTHORIZED_BY_THIS_AUDIT
MISSION_METHOD_DELTA = NONE
```

- 本任务只创建本文件；未修改 D0 owner、源码、测试、results 或 `.sessions/`。
- 四个 protected `p05_run*.log` 的审计前 SHA256 分别为 `7843B048...F11`、`735E4650...38B`、`C76887C6...4D`、`95A1D184...1DE`；末尾复核必须保持一致。

