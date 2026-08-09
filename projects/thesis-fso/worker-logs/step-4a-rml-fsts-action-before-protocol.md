# RML-FSTS action-before protocol closure

> provenance: T021 parent executor exceeded the bounded stop window and was interrupted; its fresh child completed the delegated 455-line Wang fulltext read and returned the structured semantic result. The master then synthesized this log from that delegated read plus local primary-source line checks. This is not an independent verification; T022/V008 must audit it from fresh context.

## Verdict

`AB1_NOT_CLOSED`

Previous-frame 与 action-independent common-probe 都能写出因果骨架，但当前一手证据不能把任一方案冻结成 D012 所要求的可执行、可证伪 protocol contract。两者共同缺少 action-invariant receiver-power reference/estimator、feedback/ACK implementation、time-series channel lifecycle 与数值 freshness/latency contract；common-probe 还缺 probe waveform/length/MDE，previous-frame 还缺 frame cadence 与跨帧 continuity。故不得把纸面 timeline 当作 deployable B2，也不得恢复 performance grid/MVE。

本结论不否认反馈式 structural FSTS 在另一个、材料闭合的系统中可能可行；它只说明 Wang source object 与当前 target transfer 不能闭合本轮 AB1。

## Evidence boundary

- task-control validator：`PASS`（epoch 37 / CP024 / `NEW_TOPIC_RECOVERY`）；authorization consistency 不等于 protocol correctness。
- Wang canonical HTML 全文由独立子 agent 逐行精读；HTML 无印刷页码，以下使用公式/图/行号。Wang 的 FSTS construction 与 Eq. (7)–(11) 证明 structural `(B_N,B_L)` 在发射前写入 waveform；receiver chain 到 BPD/ADC 后才开始 FS/MRC/pol-demux/FOE。证据：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:107,183-208,231-243`。
- Wang 只把 turbulence phase/intensity/coupling 称为相对 GHz symbol rate slow-varying；没有 frame interval、cross-frame process、RSSI/power estimator、feedback、ACK、action signaling 或 reconfiguration latency。证据：同上 `:160,183,208,241-243`。
- Valjus review 报 atmospheric scintillation/pointing coherence time通常 `>1 ms`，但明确不建模 coherence time、只取 quasi-static channel；因此它只能支持单 FSTS 内慢变，不提供本协议的跨帧 generator/lifecycle。证据：`D:/code/study/research-protocol/papers/doi/10.1002_sat.1553/content.md:167`。
- 相邻一手工作 JLT 2023 明确把 earlier-frame RX CSI 用于后续 frame，并警告 processing+round-trip 超过 channel timescale 会失效；其 ground-to-ground 强湍流例给最大约 10 km，LEO 例给 Greenwood time约 4 ms、最大约 60 km，并明确 receiver-directed adaptive loading 不适合其 satellite application。证据：`papers/doi/10.1109_jlt.2023.3242215/content.md:155-171`。这说明 feedback causality 是真实方案，同时也证明不能把 generic `>1 ms` 当作星地可部署闭环。
- WiSEE 2024 的 32768-symbol/32-GBd frame约 `1 us`、DSP overhead约 `7.75%`，并以 scintillation few-kHz 为由只支持**单 frame 内**静态。它没有 receiver-to-transmitter action feedback。证据：`papers/doi/10.1109_wisee61249.2024.10850117/content.md:33,50,92`。

## Previous-frame option

### Causal skeleton

```text
receive frame n action-independent measurement region
  -> estimate normalized receiver power p_hat[n]
  -> apply dev-frozen power bin and lookup
  -> feedback {frame_id=n+1, measurement_age, action_id, validity}
  -> transmitter freshness/ACK gate
  -> build FSTS for frame n+1 with (B_L, B_N=320/B_L)
  -> signal chosen action and transmit
  -> receiver checks signaled action, then scores frame n+1
```

该顺序满足 `observation < decision < next-FSTS construction`，不会用 frame `n+1` 当前 FSTS 倒置决定自身结构。若 measurement region 是每帧固定、与前一 structural action 无关的 payload/pilot 区，它也可能 action-invariant。

### 未闭合项

1. Wang 未定义固定 measurement region、power estimator、AGC/reference plane；从上一 action-specific FSTS 估功率仍可能被上一动作与 modulation energy影响。
2. Wang 没有 frame cadence、跨帧 phase-screen/coupling state、generator reset/continuity；Valjus 又显式采用 quasi-static而非 time-series。无法执行 stale-state 或 paired trajectory test。
3. 没有 feedback channel、processing/reconfiguration latency、timestamp clock、ACK/CRC 与 action signaling。
4. JLT 2023 的 ground/satellite边界是不同 MDM system；它可反证“反馈总是来得及”，不能替 Wang 冻结 latency。
5. first frame、drop、stale 时可概念性 fallback 到 B1，但缺可计算 freshness gate，无法判断何时触发。

结论：previous-frame 是两个方案中更低 optical overhead 的候选骨架，但不是当前可冻结 primary。

## Common-probe option

### Causal skeleton

```text
transmit fixed action-independent probe
  -> receiver estimates p_hat_probe
  -> feedback action_id/validity
  -> transmitter waits for ACK/freshness gate
  -> build and transmit selected 320-symbol structural FSTS
```

固定 probe 可以避免用 action-specific FSTS 估当前 action，并可为所有候选 action 提供相同 observation source。

### 未闭合项

1. Wang 没有 common probe waveform、length、energy、power estimator或 estimator MDE；任意选择都会改变原 training/protocol overhead。
2. probe、reverse feedback、processing/reconfiguration、selected FSTS 必须落在同一有效 channel state；只有“slow relative to symbol rate”与 generic `>1 ms`，没有适用于该 caller path 的 coherence/latency test。
3. 即便以 Wang `L=10 km` 计算真空传播 round trip约 `2L/c = 66.7 us`，这仍未含 receiver processing、feedback PHY、TX reconfiguration与 guard，而且不能外推到星地链路。
4. 缺 payload/frame length，不能把新增 probe symbols与等待时间换成唯一 throughput/duty-cycle cost。

结论：common probe的 observation invariance 更清楚，但它需要更多未报告 protocol资产，不能冻结 primary。

## Frozen primary caller-to-callee contract

`NONE`。当前只保留下面的**future candidate interface**，状态=`NON_AUTHORITATIVE / NOT_EXECUTABLE`：

```text
observe_action_independent_power(frame_or_probe)
  -> normalize_at_frozen_reference_plane()
  -> bin_with_dev_frozen_edges()
  -> lookup_single_structural_action(modulation, ts_length, power_bin)
  -> send_feedback(frame_id, timestamp, action_id, valid, crc)
  -> require_ack_and_freshness()
  -> build_fsts(B_L=action_id, B_N=320/B_L)
  -> signal_action_to_receiver()
  -> execute_and_score_hidden_truth_only_at_scorer()
```

只有外部输入同时闭合 observation reference、time-series source、feedback implementation与 overhead 后，才可重新选择 previous-frame 或 common-probe 为唯一 primary。

## Information-access table

| datum | runtime access | allowed use | current status |
|---|---|---|---|
| modulation / TS length | protocol-known before action | B2 lookup key | allowed |
| action-independent RX complex samples | receiver before feedback | power estimator | required but Wang path未定义 |
| normalized receiver-power estimate + age | receiver-visible | bin/key + freshness | required but estimator/reference/lifecycle未定义 |
| dev-frozen bin edges / lookup | transmitter+receiver config | select one structural action | allowed in principle |
| feedback frame id / timestamp / action id / valid / CRC | control message | causal handoff | required but interface未定义 |
| true SNR / true `h` / turbulence label | hidden truth | generator/scorer/O1 only | forbidden in B2 |
| CFO truth / payload labels / per-action outcome | hidden truth | final scoring only | forbidden in decide path |
| future samples or current action-specific FSTS power | action-after | none for current action | forbidden |

Hidden-truth metamorphic requirement：固定 runtime message与receiver observation，只改变 true SNR/`h`/turbulence/CFO/labels，B2 action与transmitter waveform选择必须逐 bit 不变。当前没有 runnable caller path，故该 test 尚不能执行。

## Lifecycle, freshness and fallback

可接受的 future lifecycle 必须包含：

- initialize：first frame固定 B1；没有历史 observation 时禁止 B2；
- update：只在 measurement、timestamp、feedback CRC、ACK 全有效时更新；
- reset：link reacquisition、frame-id discontinuity、clock reset、feedback loss均清空 state并回 B1；
- stale/drop：`age + remaining_reconfiguration_latency > T_valid` 时回 B1，不沿用旧 action；
- mismatch：receiver signaled action与TX waveform header不一致时 fail closed，不猜 action；
- dev freeze：`T_valid`、bin edges、lookup、estimator normalization均在 dev 上冻结，test不得重估。

但当前 `T_valid` 不可执行：generic coherence number不能替代 target time-series。一个合法 future test至少需要用 receiver-visible power sequence在 dev 上预注册相关性/预测误差 estimand、CI与 threshold，并在 held-out trajectory 复核；当前没有 source-backed trajectory generator、frame cadence或 threshold，因此 lifecycle只有规范草案，无 AB1 authority。

## Overhead accounting

Previous-frame 的最小符号式成本：

```text
b_fb = b_frame + b_timestamp + ceil(log2 K) + b_valid + b_crc
T_fb = T_rx_est + T_encode + T_reverse_prop + T_tx_decode + T_reconfig
extra_optical_probe_symbols = 0
decision_delay = one frame + T_fb
```

Common-probe：

```text
b_fb = b_frame + b_timestamp + ceil(log2 K) + b_valid + b_crc
T_cycle = N_probe/R_s + T_fb + T_guard + 320/R_s
symbol_overhead = N_probe / (N_probe + 320 + N_payload)
```

这些式子不能数值化：`K` 的 paper-tested action grid、frame/timestamp/CRC位宽、`N_probe`、`N_payload`、feedback PHY rate、各 processing/reconfiguration latency均未冻结。结构可行集若取 `{2,4,8,10,16,20,40,80}` 则 `K=8`、action id需 3 bits，但该集合是由 `N_TS=320` 结构推导，不是 Wang Fig.10 已恢复的完整 paper-tested grid；不能据此冒充 source protocol成本。

## Executable semantic tests

当前适用性与结果：

| gate | proposed test | observed status |
|---|---|---|
| action-before causality | trace observation timestamp到 `build_fsts` caller；要求严格先于 waveform build | `FAIL / no caller path` |
| current-action independence | 固定 prior observation，改变当前 action-specific samples；B2 action不变 | `NOT_EXECUTABLE` |
| hidden-truth metamorphic | 固定 deployable inputs，只改变 truth metadata；action/waveform hash不变 | `NOT_EXECUTABLE` |
| state lifecycle | trace init/update/reset/stale/drop across frames | `FAIL / source无trajectory lifecycle` |
| feedback freshness | inject delay around frozen `T_valid`，过期必须回 B1 | `NOT_EXECUTABLE / T_valid unresolved` |
| action signaling | corrupt action id/ACK，TX/RX必须 fail closed | `NOT_EXECUTABLE / interface absent` |
| overhead metamorphic | 增加 `N_probe` 或 feedback delay，measured throughput/latency必须按caller trace变化 | `NOT_EXECUTABLE` |
| paired cluster | 同 cluster共享外生 latent但 action-specific `tx/rx` hashes不同 | conceptual contract only；source trajectory absent |

## AB1 closure matrix

| required field | previous-frame | common-probe |
|---|---|---|
| causal timeline | `CLOSED_CONCEPTUALLY` | `CLOSED_CONCEPTUALLY` |
| legal receiver-visible observation | `NOT_CLOSED` | `NOT_CLOSED` |
| action invariance | `NOT_CLOSED` | `PLAUSIBLE_NOT_EXECUTABLE` |
| feedback/ACK/action signaling | `NOT_CLOSED` | `NOT_CLOSED` |
| coherence/freshness | `NOT_CLOSED` | `NOT_CLOSED` |
| init/update/reset/stale/drop | `SPECIFIABLE_NOT_EXECUTABLE` | `SPECIFIABLE_NOT_EXECUTABLE` |
| numeric overhead/cost | `NOT_CLOSED` | `NOT_CLOSED` |
| caller→callee audit | `ABSENT` | `ABSENT` |
| executable semantic tests | `0 applicable PASS` | `0 applicable PASS` |

AB1 因此为 `NOT_CLOSED`。纸面 causal ordering 或一般慢变物理都不能代替实际 caller、time-series state与cost。

## Rejected alternatives and next legal action

- rejected：用当前 FSTS 的 `mean(|r_X|^2+|r_Y|^2)` 选当前 `(B_N,B_L)`；这是 action-after/time reversal。
- rejected：上一 action-specific FSTS power 不经 action/modulation normalization直接作为下一帧 key；observation可能 action-dependent。
- rejected：用 true `gamma_bar`、true `h`、truth turbulence label或离线 condition cell替 feedback；这是 oracle-like comparator。
- rejected：假设 feedback latency=0，或用 generic `>1 ms` 自动证明任意星地 RTT 可用；JLT 2023给出直接反例边界。
- rejected：任意选 probe length、feedback bits或 freshness threshold后称协议已闭合；这些会改变 overhead与有效 task。
- rejected：把 conditioned lookup deployment wrapper 命名为 C1/controller/METHOD_SIGNAL/novel contribution。

下一合法动作：向主控回传 `AB1_NOT_CLOSED`。结合 T020 的 `SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`，D012 reducer只能得到 `REOPEN_INPUTS_NOT_CLOSED`，保持 D011/V007 terminal 5、恢复专题 dormant并继续禁止 grid/MVE。未来若用户提供 author/source backend，还需同时提供或授权一个可执行 feedback/time-series testbed；单有 source receiver config 也不会自动闭合 AB1。
