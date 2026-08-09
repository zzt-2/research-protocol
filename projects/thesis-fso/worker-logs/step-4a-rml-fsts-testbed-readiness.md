# RML-FSTS testbed readiness audit

## Status

**NEEDS_BOUNDED_ADAPTER**

判定对象是“能否在不改 `common/` / `params.py` 的前提下，形成可审计的 RML-FSTS Step 4a testbed”，不是对 Q1 作科学 Go/Kill。

- 不是 `READY`：仓库内没有 faithful Wang fixed-lag fine FOE；现有 B3 runner 没有把真实 FSTS 放进信号链，也没有 dev/test freeze、receiver-visible lookup、normalized CFO-MSE/outage 或 raw→aggregate contract。
- 不是 `INVALID`：现有双偏振 QPSK/16QAM、Gamma-Gamma/AWGN、确定性 realization，以及 `oversampled-coherent-sync-q1` 的 visible/truth、hash、artifact-reference、metamorphic pattern 足以支撑一个隔离且有界的 adapter；无需修改公共基础设施。
- 旧 `b3-joint-estimation` 只能当反例和少量工程原语来源，**不能直接作为 Q1 科学 testbed**。

## Asset map

| capability | file:line | status | gap |
|---|---|---|---|
| faithful Wang fine FOE / fixed-lag action | `projects/simulation/explore/b3-joint-estimation/joint_estimation_pipeline.py:48-70`; `projects/simulation/common/_recovery.py:37-56` | **INVALID** | `_two_stage_foe` 是 QPSK 四次幂 FFT 粗估后再次调用同一 `fft_foe` 再除以 `bl`；没有构造 Wang FSTS 跨极化共轭项，没有 lag-indexed statistic，也没有“同一 realization 扫 lag action”的接口。`fft_foe` 本身在 `common/_recovery.py:435-440` 被明确标为 QPSK-only。 |
| 320-symbol TS 长度 sentinel | `projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py:58-78` | **NEEDS_BOUNDED_ADAPTER** | 能返回长度 320 的固定 seed QPSK 序列；但 `bl`/`bn` 参数未参与构造，docstring 明说是单极化简化，缺 X/Y 共轭对称 FSTS、payload/mask 和 4/16QAM frame schema。 |
| FSTS frame synchronization | `projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py:15-55` | **INVALID for Q1 FOE** | 只是已知模板滑动匹配相关；不是 fine CFO estimator。旧 runner 还以 `ts_template=None` 调它的上游管线，见 `b3_joint_mve.py:95-98`，因此连该 FS 分支也没有进入。 |
| PM-4QAM / PM-16QAM symbols | `projects/simulation/common/_dual_pol_channel.py:28-53,56-149`; `projects/simulation/common/_modulation.py:24-61` | **READY** | 作为 symbol primitive，双偏振 generator 支持 `qpsk`（等价 4QAM）和 `qam16`；返回 X/Y bits/symbols。它不能接收 caller-provided FSTS，也没有 CFO/laser phase 输入，完整 Q1 path 仍需薄 adapter。 |
| PM dual-pol GG/SOP/AWGN channel | `projects/simulation/common/_dual_pol_channel.py:95-149`; `projects/simulation/tests/test_dual_pol_shared_channel.py:71-126`; `projects/simulation/tests/test_high_order_cpr_combination.py:557-573` | **READY** | 作为 channel primitive，显式 `alpha/beta/f_g/sop_rate/gamma_bar/t_s/block/modulation/seed` 可注入，same seed 可复现，QPSK/QAM16 共享 `h/theta`。完整 Q1 path 仍缺 custom TS、CFO/PN、component-seed ledger。 |
| weak/strong GG truth source | `projects/simulation/params.py:100-170,220-228`; `projects/simulation/common/_dual_pol_channel.py:95-114` | **READY** | 作为 truth-source primitive，weak=`(11.6,10.1)`、strong=`(4.2,1.4)` 有 literature/OK provenance；必须由本 Probe contract 显式拷入并传到 callee。不能把 KF 的 `sigma2_turb`（`params.py:269-279`, CRITICAL）当本 Q1 physical truth。 |
| receiver power / SNR | `projects/simulation/common/_dual_pol_channel.py:126-132`; `projects/simulation/common/_channel.py:84-93` | **NEEDS_BOUNDED_ADAPTER** | 当前只有 dimensionless average electrical `gamma_bar`，经 `noise variance=1/(2 gamma_bar)` 注入；没有 dBm ROP、photodetector/link-budget 映射，也没有 receiver-visible power estimate。`gamma_bar`/`h` 是 truth，不能直接成为 B2 test-time key。 |
| single-pol shared realization | `projects/simulation/common/_channel.py:57-94`; `projects/simulation/tests/test_common.py:428-451` | **READY** | 作为 single-pol pairing primitive，一次生成并返回 `rx_raw/bits/tx/h/phi`，same seed 有回归；但其 waveform 仅 QPSK/单偏振，不能直接充当 PM-FSTS。 |
| old B3 multi-aperture realization | `projects/simulation/explore/b3-joint-estimation/multi_aperture_channel.py:52-155` | **INVALID** | `gg_block` 用全局 RNG，而函数仅创建局部 `RandomState`，same seed 不保证 `h` 重现；`offset_k` 只写 metadata、未移位 `signal_k`；`cn2` 只决定 Fried/r0，不决定 GG realization。 |
| method pairing | `projects/simulation/explore/b3-joint-estimation/b3_joint_mve.py:74-104` | **NEEDS_BOUNDED_ADAPTER** | 单次调用里各 mode 确实消费同一 `ch['branches']`；但无 realization hash/seed ledger，B3 generator 本身不可完全重现，且 `params` 被塞入 truth `h_branches`。 |
| deployable information boundary | `projects/simulation/explore/b3-joint-estimation/b3_joint_mve.py:82-98`; `joint_estimation_pipeline.py:219-227` | **INVALID** | 多支路 path 把 true `h_branches` 放进 `params._h_branches` 并被 MRC 读取；没有 visible/truth 类型隔离。 |
| visible/truth + metamorphic pattern | `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py:93-119,260-316,579-585,785-790`; `projects/simulation/tests/test_oversampled_coherent_sync_q1.py:66-72,102-116` | **READY** | 作为工程 pattern，可复用数据边界与测试形态；其 QPSK/RRC/acquisition 科学结论不得继承。 |
| raw→aggregate/artifact integrity pattern | `projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py:450-536,637-705,766-787`; `semantic_smoke_core.py:829-847` | **READY** | 作为工程 pattern，已有 observations/truth/method rows、hash、完整 cardinality 与 referential-integrity；需换成本 Q1 metric/schema。 |
| current B3 result writer | `projects/simulation/explore/b3-joint-estimation/b3_joint_mve.py:72-113,126-176` | **INVALID** | 只保留 per-mode BER arrays/mean/std 后裸 `json.dump`；无逐 cell/action raw、split、realization hash、metric numerator/denominator、freeze receipt。 |
| common result writer | `projects/simulation/common/_experiment.py:164-196`; `projects/simulation/tests/INTEGRATION_PLAN.md:238-241` | **NEEDS_BOUNDED_ADAPTER** | `save_results` 能加 script/git/timestamp，但不能自动建立 seed、paired realization、raw→aggregate 或 metric contract；不能把“能保存 JSON”当 testbed ready。 |
| config/verification structure | `code-quality.md:22-29`; `reference/sim-template/config.py:1-13,44-74`; `reference/sim-template/verify.py:317-333` | **READY** | 作为工程 pattern，可用于隔离 config 派生量、seed 和分层验证，不提供本 Q1 科学参数。 |

## Caller-to-callee paths

### 现有 B3 path（不能直接复用）

```text
b3_joint_mve.run_single_config                         (:65-114)
  -> generate_multi_aperture_realization               (multi_aperture_channel.py:52-155)
       -> TURB[turb_name]                               (:88-90)
       -> qpsk_mod(random payload)                      (:91-93)
       -> local CFO/Doppler/Wiener phase                (:94-102)
       -> gg_block via global RNG                       (:111-120)
       -> AWGN from local branch RNG                    (:126-134)
  -> params._h_branches = truth h                       (b3_joint_mve.py:84-87)
  -> b3_joint_pipeline(..., ts_template=None)           (:95-98)
       -> no frame-sync branch                          (joint_estimation_pipeline.py:149-153)
       -> _two_stage_foe                                (:155-170)
            -> common.fft_foe (fourth-power QPSK)       (_recovery.py:37-56)
       -> true-h MRC for multi-branch                   (:219-227)
  -> resolve_qpsk(tx_bits, rx) scoring                  (b3_joint_mve.py:60-62,99)
```

结论：它实际跑的是“随机 QPSK payload + 伪两级 FFT-FOE”；`320-symbol FSTS`、PM-16QAM、fixed-lag action、receiver-visible power lookup 均未进入 caller→callee 链。

### 可复用的 common DP primitive

```text
generate_shared_realization_dp                         (_dual_pol_channel.py:56-149)
  -> resolve optional runtime config                    (:95-101)
  -> gg_time_envelope(N, alpha, beta, tau_c, ... seed) (:103-114)
  -> QPSK/QAM16 X/Y symbol builders                     (:116-121)
  -> SOP mixing + sqrt(h) + AWGN                        (:123-132)
  -> {rX,rY,sX,sY,h,theta,bitsX,bitsY,...}              (:134-149)
```

这条链能提供 PM 调制和 GG/SOP/AWGN realization，但 API 没有 caller-provided `tsX/tsY`、CFO/phase-noise 参数。Q1 adapter 应留在独立 Probe 目录：复用 `gg_time_envelope`、QAM mapper 与相同 signal formula，或从一次 DP realization 提取固定 `h/theta/noise` 后替换已知 TS；不得改公共 API。

### 要建立的隔离 deployable path

```text
runner.generate_cell(frozen_cell, component_seeds)
  -> (ReceiverVisible, TruthMetadata)       # 物理生成后立即分离

runner.run_method(visible, frozen_policy)
  -> select_lag_B0/B1/B2(visible, receipt)  # O1 单独走 truth scorer
  -> wang_fixed_lag_foe(
         visible.rxX_ts, visible.rxY_ts,
         visible.known_tsX, visible.known_tsY, lag)
  -> EstimateResult                         # 不接收 truth 参数

scorer.score(result, truth)
  -> normalized error / outage              # 唯一允许 join truth 的位置
```

## Parameter injection

| parameter/label | 当前真实注入路径 | 审计结论 |
|---|---|---|
| `r_sym_baud=10e9` | 只存在于 `_b3_params.py:41-44`；B3 pipeline 直接 import common `T_S`（`joint_estimation_pipeline.py:37-38`），其真相源默认 `R_SYM=2.5e9`（`params.py:48-72`） | **未注入**。旧 B3 的 10 Gbaud 标签不能用于单位换算或 CFO-MSE。隔离 config 必须显式冻结 `R_s`，callee 全部从该 config 取。 |
| `ts_total/bl/bn` | `b3_joint_mve.py:89-90` 只用于切段；`_two_stage_foe` 用 `bn*bl`/`bl^2` 决定 FFT window（`joint_estimation_pipeline.py:55-65`） | **没有注入 FSTS 结构**。`build_fsts_template` 中 `bl/bn` 完全未参与样本构造。 |
| `turb_name` | `multi_aperture_channel.py:88-90` 取 `TURB[turb_name]`，随后用于 `gg_block`（`:111-120`） | **确实注入 GG 形状**，但旧 generator seed 生命周期不闭合。 |
| `cn2/z_km` | 仅进入 `_are_branches_independent`/Fried r0（`multi_aperture_channel.py:104-105,150-153`） | **不注入信号的 GG 强度**。不可用 `cn2` 字段存在来声称 weak/strong channel 已改变。 |
| `gamma_bar` | `multi_aperture_channel.py:126-130`、`_dual_pol_channel.py:126-132` 进入 AWGN variance | **确实注入 average electrical SNR**；不是 receiver-visible measurement，也不是 dBm receiver optical power。 |
| `f_res/f_dot/lw` | `multi_aperture_channel.py:94-102` 进入 carrier phase | **确实注入旧单/多 aperture path**；common DP path 完全没有这三个参数，Q1 PM adapter 必须显式补。 |
| `modulation` | 旧 B3 固定 `qpsk_mod`（`multi_aperture_channel.py:30-32,91-93`）；common DP 在 `_dual_pol_channel.py:89-93,116-121` 分派 qpsk/qam16 | 旧 B3 **未注入 modulation sweep**；common DP primitive 可用。 |
| branch offsets | `offset_k` 在 `multi_aperture_channel.py:122-124` 计算并返回，但 `signal_k` 在 `:132-134` 未移位 | **metadata-only**，不能作为 frame-sync 注入证据。 |
| weak/strong α/β | `params.py:100-170` → caller 显式读出 → common DP `alpha/beta` → `gg_time_envelope` | 可闭合，但 Probe contract 必须写明采用的是 Gu-2022 GG 档，而非 Wang `Cn²` 的直接等价。 |

关键语义：本 testbed 若只扫 dimensionless average electrical SNR，必须明确标为 `gamma_bar`/SNR；若要声称 receiver optical power（dBm），现有资产没有 responsivity/noise/link-budget 映射，不能改标签冒充。

## Information access card

### B0/B1/B2 deployable path 可读

- `rxX_ts`, `rxY_ts`：一次生成后冻结的同一组 PM-FSTS 接收样本。
- receiver-known `tsX`, `tsY`、TS mask、sample/symbol rate、配置已知 modulation 和 TS length。
- 冻结 lag action set、B0 paper action、B1 global action、B2 lookup receipt/hash。
- 从接收 TS 直接计算的 feature，例如：
  - `p_rx_hat = mean(|rxX_ts|^2 + |rxY_ts|^2)`（或除以已知 TS energy 的固定归一化版本）；
  - 每个 lag 的 normalized correlation magnitude、peak-to-second margin、cross-pol coherence；
  - 用 known TS 做 receiver-side LS 后的 residual/noise proxy。
- B2 合法 key 只能是 `(modulation, ts_length, dev_frozen_receiver_power_bin)`；power-bin edges 在 dev 冻结，test 只查表。未覆盖 bin 必须使用预注册 fallback（建议 B1），不能看 truth 选 nearest bin。

### 仅 generator / truth / scorer / O1 可读

- `true_cfo_hz`、true lag-optimal action、`h`/attenuation、`gamma_bar`、true instantaneous SNR、noise arrays/component seeds。
- TX payload bits/symbols、payload target labels；known FSTS 不属于 payload truth，接收机合法可知。
- O1 可用 truth 逐 realization 选 lag，只输出 headroom/Kill 参照，不进入 deployable lookup。

### 当前已发现的泄漏

- `b3_joint_mve.py:84-87` 把 true `h_branches` 注入 `params`，`joint_estimation_pipeline.py:219-227` 在 MRC 读取。
- common experiment helpers 默认 `eq_mode='oracle'`、`eval_mode='oracle'`（`common/_experiment.py:125-159`）；这些 helper 不可直接接到 B0/B1/B2。
- common DP 返回值把 `rX/rY` 与 `sX/sY/h/theta/bits` 放在同一 dict（`_dual_pol_channel.py:134-149`）；调用后必须立即拆成 frozen visible/truth 类型，不能把整 dict 传给 estimator。
- `resolve_qpsk/resolve_qam16` 用 TX bits 选旋转，只能是 scorer/oracle；不能作为 deployable CFO estimator 的后处理。

## Metric signature

当前仓库没有本 Q1 的 normalized CFO-MSE 或 CFO-outage contract。建议在任何 test run 前冻结以下 dimensionless 定义；若公式审计/源论文给出不同 normalization，应在 test 前替换并写入 manifest，不能跑后改：

### Per-realization score

令 `R_s` 为本 Probe contract 唯一 symbol-rate，`f_i` 为 truth CFO，`fhat_i` 为 estimator 输出：

```text
e_i_norm  = (fhat_i - f_i) / R_s
se_i_norm = e_i_norm^2
out_i     = 1[abs(e_i_norm) > tau_out_norm]
```

- `tau_out_norm` 必须来自预注册合同/证据并在读 test 前冻结；现有代码和 T012 均没有给数值，本审计不臆造。
- 如果项目最终把 outage 定义成 BER/FEC outage，而不是 CFO estimation outage，必须新建不同字段名/分母；禁止混用。

### Population / numerator / denominator

对每个 frozen `(split, modulation, ts_length, turbulence, SNR cell, lag/method)`：

```text
population N       = 完整 seed cluster 数；不按估计成功与否删样本
NMSE numerator     = sum_i (fhat_i - f_i)^2
NMSE denominator   = N * R_s^2
normalized CFO-MSE = numerator / denominator
outage numerator   = sum_i out_i
outage denominator = N
outage rate        = outage numerator / outage denominator
```

- 每个 raw row 必须落 `cell_id, split, seed_id, realization_id, rx_sha256, method, action_lag, fhat_hz`；truth 与 method row 分文件，scorer 以 `cell_id` join 后产生 `e_i_norm/se_i_norm/out_i`。
- 先按 cell 报告，再对预注册 cell 做 macro aggregation；不得用样本量较大的 cell 偷换 pooled denominator。
- action 比较必须保留 seed-paired delta；至少输出 B2−B1、B2−B0、O1−B2 的 paired raw differences。
- summary 同时保存 numerator、denominator、rate/mean，不能只保存均值；独立 test 必须从 raw 精确重算 summary。

## State/seed lifecycle and pairing

### 当前状态

- common DP generator 使用局部 `default_rng(seed)`，GG envelope 也显式接收 seed；同 seed reproducibility 已由 `test_dual_pol_shared_channel.py:111-126` 覆盖。
- 旧 B3 generator 不是这样：bits/phase/noise 用局部 RNG，但 `gg_block` 走全局 RNG（`multi_aperture_channel.py:88-120`），所以 same seed ledger 不闭合。
- 旧 B3 每个 seed 只生成一次 `ch` 后让各 mode 消费同一 arrays（`b3_joint_mve.py:74-104`），局部 pairing 方向正确；但没有 hash/cardinality 校验。
- 旧 B3 只有 `range(n_seeds)`（`:74`），没有 dev/test split，也没有历史 seed exclusion。

### 本 Probe 必须冻结的 lifecycle

1. split 以 seed cluster 为单位；`dev_seeds ∩ test_seeds = ∅`，且两者与历史 observed seeds 的交集为零。
2. `cell_id` 包含 split 之外的全部 frozen condition；由 `master_seed|split|cell_id|component` 派生独立 `ts/gg/carrier/awgn` seed，避免 RNG draw-order 受 action 数量影响。
3. 每个 `(split, cell_id, seed)` **只生成一次** realization，得到 immutable `ReceiverVisible`；所有 lag、B0/B1/B2/O1 都消费同一 `rxX/rxY`。
4. GG、carrier phase 与 AWGN 在一个 320-symbol FSTS 内连续；默认在新 realization/cell reset。若要跨 frame continuity，必须另冻 lifecycle，不能复用旧 state。
5. B0 直接用 paper fixed lag；B1 只在 dev 全局选一个 lag并写 freeze receipt；B2 只在 dev 的合法 visible key 内选一个 lag并冻结 lookup；test runner 先校验 receipt hash，之后禁止更新 bin/action。
6. O1 用同一 paired realization 在 scorer 中逐 realization 选最优 lag；它不向 B2 反哺。
7. 每个 method row 携带同一 `realization_id/rx_sha256`；cardinality check 要求每个 cell 恰有完整 `lag actions + B0/B1/B2/O1`，缺一即 execution invalid。

## Raw-to-aggregate contract

隔离 runner 应沿用 `oversampled-coherent-sync-q1` 的职责分离，而非沿用 B3 裸 `json.dump`：

| artifact | required content |
|---|---|
| `manifest.json` | formula identity/hash、waveform/TS definition、parameter sources、lag set、visible/truth card、metric signature、split/seed derivation、state lifecycle、claim ceiling |
| `freeze-receipt.json` | B0 action、dev-derived B1 action、B2 power-bin edges/lookup/fallback、dev seed hash、`test_started=false/true` latch、receipt SHA256 |
| `observations.jsonl` | one row/realization：visible feature summary、power proxy/bin、realization/rx hashes；不含 true CFO/h/gamma/payload |
| `truth.jsonl` | one row/realization：true CFO、physical truth、component seeds；method API 不读取 |
| `method-results.jsonl` | one row/cell/method：selected lag、estimate Hz、compute ledger、realization/rx/receipt hashes；不含 truth-selected branch |
| `scores.jsonl` | scorer join 后的 `e_norm/se_norm/outage` 和 frozen threshold |
| `summary.json` | 每组 population、两个 numerator/denominator、NMSE/outage、paired deltas；由 raw 确定性重算 |
| `provenance.json` | git head、Python/dependency、script/contract/artifact hashes、exact command、claim ceiling |

校验必须覆盖：observation/truth cell 集完全相等；每 cell method cardinality 完整；所有 method row 的 `realization_id/rx_sha256/receipt_hash` 与 observation 一致；summary 对 raw 重算相对误差为 0（浮点容差仅用于最后一位）；任何失败均为 `EXECUTION_INVALID`，不能进入科学 terminal。

## Runtime metamorphic test

最小 runtime test 应复用 `oversampled` 的“方法只接收 `ReceiverVisible`”模式（`semantic_smoke_core.py:93-119,579-585`）并扩展到完整 caller→callee：

1. generator 构造一个 cell，保存 immutable `visible` 与独立 `truth`。
2. 从 runner 的真实入口分别调用 B0/B1/B2：

   ```text
   run_method(visible, frozen_receipt)
     -> select_lag_*(visible)
     -> wang_fixed_lag_foe(visible.rxX_ts, visible.rxY_ts,
                           visible.known_tsX, visible.known_tsY, lag)
   ```

3. 保持 `visible`、receipt 和 receiver-derived power feature byte-identical，只改变 truth metadata：`true_cfo_hz`、`gamma_bar`、`h`、true attenuation、TX payload/labels、component seeds。
4. 重新从 runner 入口调用 B0/B1/B2；要求 selected lag、feature vector、`fhat_hz`、compute ledger 的 canonical bytes 全部相同。测试至少覆盖 `{qpsk,qam16} × {weak,strong}`。
5. O1 不参加“不变”断言；它是预期可依赖 truth 的 headroom path。scorer 的 error/outage 也允许随 `true_cfo_hz` 改变，但 method output 不得变。
6. 加一条反向灵敏度：只改变 receiver-visible TS 样本/测得 power proxy 时，B2 允许按 frozen bin 改 action，证明 lookup 不是常量假通过。

旧 `p08r2_metamorphic_gate.py:47-118` 已展示“固定 arrays，只翻 hidden gamma_bar，从真实 equalize→demap path 比较输出”的 runtime 形态；本 Q1 只复用测试结构，不复用 coded-chain 科学内容。

## Minimal isolated file set

严格不建议修改 `common/` 或 `params.py`。最小新增手写集合为 4 个文件：

1. `projects/simulation/explore/rml-fsts-step4a/contract.yaml`
   - frozen formula/lag identity、PM-FSTS schema、R_s、GG/SNR semantics、seed split、metric/outage threshold、B0/B1/B2/O1、claim ceiling。
2. `projects/simulation/explore/rml-fsts-step4a/rml_fsts_core.py`
   - frozen dataclasses、faithful fixed-lag fine FOE、320-symbol X/Y FSTS builder、isolated PM realization adapter、receiver-visible power/features、selectors/scorer primitives。
3. `projects/simulation/explore/rml-fsts-step4a/run_semantic_smoke.py`
   - generate-once/pair-all-actions、dev freeze→receipt→held-out test、raw/artifact/provenance writer、deterministic aggregator。
4. `projects/simulation/tests/test_rml_fsts_step4a.py`
   - formula identity sentinel、PM-4/16QAM/320 shape、caller→callee injection、same-seed/hash pairing、visible/truth/cardinality、metamorphic、dev/test freeze、raw→aggregate exact recompute。

生成的 artifacts 不算手写 source file。实现时可 import `common._gg_time.gg_time_envelope`、`common._modulation.qam16_mod` 等原语；不得把 adapter 推进公共层。

预计成本（在 formula identity 与 `tau_out_norm` 已由上游冻结后）：**2–3 人日**；其中 faithful estimator/FSTS identity 0.5–1 日、PM realization/信息边界 0.5 日、freeze+raw/aggregate 0.5–1 日、tests/metamorphic 0.5 日。首个 semantic smoke 应设计为 CPU **≤15 分钟**；本审计未运行任何实验。

## Readiness terminal and blockers

**Terminal: NEEDS_BOUNDED_ADAPTER**

必须在任何 semantic smoke 前闭合的真实 blocker：

1. **公式/实现 blocker**：当前没有 faithful Wang fixed-lag fine FOE；`fft_foe(...)/bl` 不能充当它。需要上游 formula-identity audit 给出可执行公式、lag/action 定义和 identity cases。
2. **waveform blocker**：现有 320-template 是单极化 QPSK sentinel，PM X/Y 共轭 FSTS、4/16QAM frame/masks 尚不存在。
3. **物理语义 blocker**：现有 testbed只有 normalized electrical SNR；若本轮要求 dBm receiver optical power，必须先给出独立且可溯源的光电/噪声映射。否则只能诚实标 SNR。
4. **B2 observability blocker**：必须冻结 receiver-derived power feature、dev bin edges、unseen-bin fallback；true `h/gamma_bar` 不能进 key。
5. **metric blocker**：normalized CFO-MSE 的 normalization 与 CFO-outage threshold 尚未冻结；没有 threshold 就只能产出 raw error，不能宣称 outage。
6. **execution-contract blocker**：现有 B3 无 dev/test split、seed ledger、freeze receipt、raw→aggregate/cardinality；必须由隔离 runner 补齐。

一旦上述 6 项通过 4-file adapter 闭合，现有 common primitives 足够支撑 bounded semantic smoke；在此之前，“已有脚本能跑”不等于 scientific testbed ready。
