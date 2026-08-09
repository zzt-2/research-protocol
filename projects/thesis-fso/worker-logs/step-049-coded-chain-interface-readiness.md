# Step 049 — Coded-chain interface readiness

> 2026-08-09 | T003 | action class: `TESTBED_READINESS_AUDIT`
>
> Scope: read-only source inspection and API introspection. No scientific experiment, BER/FER run, parameter change, source/owner/artifact mutation, or candidate implementation was performed.

## Caller→callee graph

The current corrected path is a **single-pass coded receiver**, not a decoder-feedback carrier-recovery loop:

```text
p08r2_run.main
  -> build_realization
     -> CodedRealizationR2.realize
        -> CodecAdapterR.encode
        -> qam16_mod
        -> generate_shared_realization_dp
     -> CodedRealizationR2.equalize
        -> estimate_pre_eq_noise_from_prefix
        -> gamma_vis_from_prefix
        -> mmse_equalize + amp_limit
  -> run_method
     -> method_B0 / method_B1 / method_B2
        -> estimate_sigma2_from_prefix
        -> maxlog_soft_demap_16qam
        -> llr.reshape(n_cw, 1536)
        -> CodecAdapterR.decode
           -> LDPC5GDecoder(... hard_out=True, return_infobits=True,
                            return_state=False, callbacks=[])
        -> final info_hat
     -> score_trajectory                      # truth is consumed only here
```

Evidence:

- `p08r2_run.py:53-74,77-96,248-274` constructs one realization, equalizes once, dispatches one method, decodes once, then scores. There is no edge from decoder output back to equalization/CPR.
- `p08r2_phaseA.py:128-194` maps equalized symbols to LLRs and calls `codec.decode(llr)` once. All three deployable methods return after final hard information bits.
- `p08r_chain.py:123-178` is the actual codec adapter used by P08-R2. The decoder is hard-output, information-bit-only, fixed at 20 iterations, with no callbacks or returned state configured.
- `p08r2_chain.py:199-234` generates the whole frame; `:236-277` exposes one parameter-free `equalize()` call. It has no phase hypothesis, CFO estimate, phase tracker state, relock command, rollback command, or recovery action argument.
- `common/_dual_pol_channel.py:103-144` models Gamma-Gamma amplitude, deterministic SOP mixing `theta=sop_rate*n`, and AWGN. It contains no carrier phase-noise/CFO state or carrier-recovery action callee.
- The nearby CCISP route is not a compatible callee: `simulator/run_ccisp_family1_branchrouted_b_30seed.py:11-22` is an uncoded 16APSK single-branch runner and passes `tx`/`bits` into its DA branch and true `snr/gl` into its decision path. It cannot be spliced into the corrected coded receiver without a new signal/action contract and information-boundary repair.

Current causal timing is therefore:

```text
whole-frame rx -> equalize -> demap -> 20 fixed BP iterations -> hard info bits -> offline truth score
```

There is no legal same-frame feedback point and no next-block controller state. `scan_workspace()` rebuilds a realization for each seed/cell and passes no persistent state (`p08r2_run.py:77-96`).

## Decoder capability matrix

Read-only introspection receipt (Python import/`inspect`; no decoder call):

```text
sionna_version 2.0.1
LDPC5GDecoder.__init__(encoder, cn_update='boxplus-phi', vn_update='sum',
  cn_schedule='flooding', hard_out=True, return_infobits=True, num_iter=20,
  llr_max=20.0, v2c_callbacks=None, c2v_callbacks=None, prune_pcm=True,
  return_state=False, harq_mode=False, ...)
LDPC5GDecoder.call(llr_ch, *, rv=None, num_iter=None, msg_v2c=None)
current CodecAdapterR decoder:
  hard_out=True, return_infobits=True, return_state=False, prune_pcm=True,
  num_iter=20, num_vns=1760, num_cns=720, num_edges=5360,
  v2c_callbacks=0, c2v_callbacks=0
out_int.shape=(1536,), out_int[out_int_inv] == arange(1536): True
```

Installed-source evidence is
`C:/Users/zzt/scoop/apps/python311/current/Lib/site-packages/sionna/phy/fec/ldpc/decoding.py:114-136,733-910,1328-1394,1442-1542,1571-1700`.

| capability | actual API/behavior | evidence | status |
|---|---|---|---|
| Current construction | `LDPC5GDecoder(enc, num_iter=20, cn_update=..., hard_out=True, llr_max=20)`; defaults leave `return_infobits=True`, `return_state=False`, callbacks empty, `prune_pcm=True` | `p08r_chain.py:126-150`; introspection receipt | CURRENT_HARD_ONLY |
| Input | `(B,1536)` on-air/post-interleaver channel logits, convention `log p(1)/p(0)` | `p08r_chain.py:152-164`; Sionna `decoding.py:1370-1388,1642-1652` | READY |
| Hard information output | `(B,1024)` hard information bits | `p08r_chain.py:158-178`; Sionna `decoding.py:1677-1685` | READY |
| Posterior soft output | Library supports `hard_out=False`. With `return_infobits=False`, output is soft logits for all `n=1536` on-air codeword positions | Sionna `decoding.py:896-910,1332-1335,1384-1388,1687-1700` | LIBRARY_READY / ADAPTER_MISSING |
| True extrinsic | Not returned directly. For the same on-air order and logit convention, candidate adapter must freeze and test `L_ext=L_post-L_ch`; posterior alone must not be named extrinsic | Current adapter has no `L_post`; Sionna soft-output behavior above | NEEDS_ADAPTER |
| Decoder message state | `return_state=True` returns `msg_v2c`, and `call(..., msg_v2c=...)` accepts it for IDD | Sionna `decoding.py:133-136,837-910,1359-1362,1571-1593` | LIBRARY_READY / ADAPTER_MISSING |
| Iteration override | `call(..., num_iter=i)` supports externally split iteration budgets | Sionna `decoding.py:837-857,890-894,1571-1588` | LIBRARY_READY / ADAPTER_MISSING |
| v2c callback | Callback receives `(msg_vn, it, x_hat)` and must return same-shaped `msg_vn`. It is called once at `it=0`, then after each VN update at `it=1..N` | Sionna `decoding.py:120-126,779-785,880-894` | LIBRARY_READY / ADAPTER_MISSING |
| c2v callback | Callback receives `(msg_cn, it)` and must return same-shaped `msg_cn`; under flooding it is called once per BP iteration | Sionna `decoding.py:127-132,753-768` | LIBRARY_READY / ADAPTER_MISSING |
| Native early stop / convergence | Sionna explicitly says batching uses **no early stopping**. `return_state` is a message tensor, not convergence or iteration count | Sionna `decoding.py:114-118,1342-1344`; introspection | NOT_AVAILABLE |
| Current iteration diagnostic | Adapter always returns only `num_iter_configured=20`. Its dormant tuple branch would mislabel returned `msg_v2c` as `iterations_per_cw` if `return_state` were enabled | `p08r_chain.py:164-178` versus Sionna `decoding.py:1390-1394` | SEMANTIC_ANOMALY |
| Syndrome trajectory | Sionna does not return a syndrome metric, but v2c callback exposes per-iteration `x_hat` and decoder `pcm`; an observation-only callback can compute a graph-parity weight | Sionna `decoding.py:120-136,578-581,733-786` | NEEDS_ADAPTER |
| Existing syndrome helper | Old `CodecAdapter.syndrome_check()` checks `Hc` only on a **full encoded codeword**. Re-encoding any hard `info_hat` then calling it always produces a valid codeword and cannot diagnose decoder failure | `p08_coded_chain.py:192-215`; `p08_correctness_gate.py:73-83,116-130` | ENCODER_TEST_ONLY |
| CRC | No coded-chain CRC implementation or runtime CRC state was found by repository-wide `rg` | directed repository search | ABSENT; do not add if syndrome suffices |
| Cost/latency | Current contract stores configured 20 iterations; final artifact stores wall time only. No per-call iteration, callback, front-end recompute, or latency ledger exists | `p08r2_run.py:369-386`; raw schema inspection | NEEDS_ADAPTER |

Important semantic correction: `CodecAdapterR.decode()` must not reuse its current tuple-handling code when enabling `return_state`. In Sionna 2.0.1 the second tuple element is the full `msg_v2c` state, not per-codeword iteration counts.

## Mapping and causal timing

### Reversible coded-bit ↔ 16QAM mapping

The mapping is structurally sufficient for receiver-visible soft symbols:

1. `CodecAdapterR.encode()` emits the **on-air, interleaved** `(B,1536)` codeword (`p08r_chain.py:128-156`).
2. `CodedRealizationR2.realize()` flattens each codeword and groups every four adjacent on-air bits into one Gray 16QAM symbol (`p08r2_chain.py:206-215`).
3. `maxlog_soft_demap_16qam()` returns `[b0,b1,b2,b3]` logits in the same symbol order (`p08_coded_chain.py:83-106`); `llr_per_cw_from_eq()` reshapes them back to `(B,1536)` (`p08r2_phaseA.py:128-147`).
4. The decoder internally applies `out_int_inv` on input (`decoding.py:1642-1649`). When `return_infobits=False`, it applies `out_int` before returning the length-1536 codeword logits (`decoding.py:1687-1700`). The introspected permutation round-trip passed.

Therefore the safest C2 interface is the official soft codeword output in on-air order. Manually applying `out_int_inv` again would double-deinterleave and is an identity bug.

For logits `L_ext[k]`, compute `p_k=sigmoid(L_ext[k])` and, per group of four bits, the receiver-only expectation

```text
E[s] = sum_{m=0}^{15} constellation[m]
       * product_k p_k**bit[m,k] * (1-p_k)**(1-bit[m,k])
```

using `_CONST/_CONST_BITS` from `p08_coded_chain.py:52-71`. This mapping needs a focused identity test for all 16 one-hot/high-confidence labels and an uncertainty test (`L=0 -> E[s]≈0`); no TX payload is an input.

### Earliest legal feedback point

- Decoder evidence becomes legal only after a pre-frozen first segment of BP iterations has consumed receiver LLRs.
- Same-frame action is legal only if it reuses the same received arrays, uses no truth/scoring fields, applies one pre-registered action, and re-demaps/re-decodes within a fixed total BP/front-end budget.
- If the action changes the front-end likelihood/LLR, blindly continuing old `msg_v2c` is not identity-safe. The minimal safe contract is to restart the remaining decoder segment and count both segments; state reuse requires a separate verified IDD contract.
- Next-block action is not currently available: there is no streaming block caller, timestamp, continuity contract, or persistent receiver state. A new next-block controller would be a separate testbed, not a flag on `p08r2_run.py`.

## Candidate-specific adapter BOM

All paths below are **future boundaries only**. Existing P08/R/R2 source and artifacts remain unmodified. Proposed files live under `projects/simulation/explore/coded-decoder-feedback/` only after canonical GW gates authorize implementation; focused tests live under `projects/simulation/tests/`.

| candidate | minimal interfaces | files | tests | estimate | blocker |
|---|---|---|---|---|---|
| C1 Decoder-Aided Phase-Hypothesis Feedback | C1-local `decode_hypothesis_score(llr, i1)` using one frozen evidence kind (prefer graph-syndrome; do not build both syndrome and extrinsic); fixed `apply_phase_hypothesis(rx_view, phi)`; outer `i1 -> score frozen H -> keep/one switch -> i2`; C1 receipt with all hypothesis scores and chosen action | New `c1_hypothesis_feedback.py`, `c1_run.py`, `test_coded_decoder_feedback_c1.py`; existing files modified: none | source/schema; feedback-off byte parity; callback count; permutation identity; score independent of truth/final correctness; one-switch limit; same-rx digest; total BP/front-end/latency ledger | decoder evidence + scheduler: 2–3 d; end-to-end estimate cannot be closed | `TESTBED_HARD_BLOCKER`: corrected chain has no compatible phase-hypothesis/relock callee or carrier-phase impairment. Decoder API itself is not the blocker |
| C2 Extrinsic Soft-Symbol Iterative CPR | C2-local soft decoder `hard_out=False, return_infobits=False`; frozen `L_ext=L_post-L_ch`; `soft_symbol_expectation()` in on-air groups of four; one `apply_weighted_phase_frequency_update()`; restart-and-final-decode schedule with fixed `i1+i2=20`; C2 cost receipt | New `c2_extrinsic_cpr.py`, `c2_run.py`, `test_coded_decoder_feedback_c2.py`; existing files modified: none | all 16 label mappings; zero-logit expectation; `posterior != extrinsic` schema; no-feedback parity; hidden-truth metamorphic; exactly one update; matched hard-DD comparator budget; raw `L_ch/L_post/L_ext` summary and latency ledger | decoder/mapping adapter: 2–3 d; end-to-end estimate cannot be closed | `TESTBED_HARD_BLOCKER`: no carrier phase/CFO impairment, estimator state, or phase/frequency update callee exists in P08-R2 |
| C3 Syndrome-Triggered Recovery Control | C3-local observation-only v2c callback returning messages unchanged; per-iteration `pruned_graph_syndrome_weight` (or separately verified full-PCM mapping, not both); fixed early-check iteration; one `recovery_command`; external split decoder; C3 state/trigger receipt | New `c3_syndrome_recovery.py`, `c3_run.py`, `test_coded_decoder_feedback_c3.py`; existing files modified: none | callback lifecycle (`N+1` v2c observations including `it=0`); callback identity; correct-codeword syndrome zero; corrupted hard graph word nonzero; no native early-stop claim; one-trigger/one-recovery; final-CRC-only negative control; latency/iteration ledger | syndrome/callback adapter: 2–3 d; end-to-end estimate cannot be closed | `TESTBED_HARD_BLOCKER`: no compatible relock/hypothesis-switch/reacquisition callee. Old `encode_full_for_syndrome` cannot supply failure trajectory |

No candidate is `READY`. The decoder-side pieces are bounded `NEEDS_ADAPTER`; the end-to-end method-bearing chain is hard-blocked at the carrier-action caller/callee, not by work volume or by Sionna.

## Information-boundary audit

Current positives:

- P08-R2 keeps physical `gamma_bar` in `realize()` and removes it from `equalize()` (`p08r2_chain.py:199-234,236-277`).
- The current metamorphic receipt freezes arrays and flips hidden `gamma_bar` (`p08r2_metamorphic_gate.py:1-16,75-143`).
- V075 recursively checks deployed function bodies for `gamma_bar/h_truth/theta` (`p08r2_verify.py:58-143,208-289`).

Remaining interface risks:

- Candidate functions must not accept the current `real` object. It carries `cw_info_*`, `cw_bits_*`, `sX/sY`, `h`, `theta`, and `gamma_bar` together (`p08r2_chain.py:176-189`). Convention/AST alone is weaker than a restricted receiver-view type.
- `score_trajectory()` consumes payload truth after decode (`p08r2_phaseA.py:219-232`). No action or trigger may receive its outputs, final correctness, BER/FER, or a post-hoc best-hypothesis label.
- The existing metamorphic gate covers hidden SNR but not payload truth, true `h/theta`, or final correctness. Candidate tests must delete/permute those scoring fields while holding receiver input fixed and assert identical evidence, action, callback trace, and output digest.
- Known prefix symbols are legal; scored payload symbols are not. The receiver view must expose `known_prefix` separately and omit `sX/sY` payload arrays.
- Candidate raw receipts must separate `runtime_receiver` fields from `evaluation_truth` fields and record the caller→callee allowlist.

Minimum receiver-view contract:

```text
ReceiverFrameView = {
  frame_id, block_id, rx_X, rx_Y, known_prefix_X, known_prefix_Y,
  frozen_code_contract, frozen_decoder_budget, receiver_clock
}
```

Explicitly absent: TX payload bits/symbols, true phase/CFO/h/SNR, oracle action, final BER/FER/correctness.

## Existing reusable receipt/metric assets

| asset | reusable part | limitation for future decoder feedback |
|---|---|---|
| `p08r2_dev_workspace.json` | frozen-contract and dev-before-test schema | scientific cells/numbers are historical and must not be restored |
| `p08r2_phaseA_raw_rows.json` | paired seed/method rows, receiver-estimate versus `_truth` naming, raw→aggregate pattern | 240 rows are trajectory aggregates; no callback/evidence/action/latency event rows |
| `p08r2_phaseA_gate.json` | explicit terminal and metric-contract envelope | no decoder source identity or feedback budget |
| `p08r2_metamorphic_gate.json` | tolerance-bearing metamorphic receipt pattern | flips only hidden `gamma_bar`; must extend to all forbidden truth and action output |
| `p08r2_v075_result.json` + `p08r2_verify.py` | independent recursive-call-graph verification pattern | result only says 19/19 for old path; does not cover a future candidate caller |
| `p08_coded_chain.source_receipt()` | encoder/module/hash receipt idea | tied to the old non-interleaved adapter; future receipt must add decoder file/hash/signature, callbacks, `out_int/out_int_inv` hashes, and Sionna 2.0.1 flags |
| `p08_correctness_gate.py` | noise-free, all-zero, Gray-label and source-hash test ideas | old adapter identity differs; its “early-stop” check is declarative, not an early-stop test |
| `reference/sim-template/config.py` and `verify.py` | dataclass contract and independent verification structure | must be specialized; no RL/env scaffolding is needed |

Current P08-R2 writers use direct `json.dump` (`p08r2_run.py:212-219,273-274,385-386`). A future authorized implementation must use the project result writer/metadata path and persist raw event receipts rather than copy these direct writers.

## Hard blockers vs bounded work

### Bounded work (not a hard blocker)

- Instantiate a candidate-local soft/stateful Sionna decoder.
- Add observation-only callbacks and a fixed external iteration split.
- Compute posterior, true extrinsic, pruned-graph syndrome weight, and on-air soft-symbol expectation.
- Add restricted receiver-view types, source/schema receipts, identity branches, raw event rows, and cost ledgers.
- Reuse the corrected code/interleaver/Gray mapping without modifying P08/R/R2.

### Hard blocker

The corrected coded chain has **no carrier-recovery action anchor**: no phase/CFO impairment state, no phase/frequency estimator, no hypothesis/relock/reacquisition argument, and no persistent block controller. Consequently, decoder evidence can presently change nothing in the same frame or next block. This is demonstrated by the caller→callee graph, not inferred from implementation effort.

The blocker is lifted only by identifying or creating, after GW authorization, one receiver-only coded carrier-action caller with:

1. an explicit impairment/state definition;
2. one bounded action that changes the same frozen receiver realization (or a documented continuous next block);
3. no TX truth/true phase/CFO/h/SNR inputs;
4. a no-feedback identity path to corrected P08-R2;
5. a conventional same-information action comparator.

The uncoded CCISP runner is not that anchor as currently written.

## Master verification list

These are executable contracts for a future authorized adapter. `NOT_RUN` is intentional in this audit.

| verification | required assertion | current status |
|---|---|---|
| Source identity | record Sionna version/module hashes/signatures, encoder/decoder flags, PCM shape/hash, interleaver hashes, callback source hashes | PARTIAL introspection only; candidate `NOT_RUN` |
| Schema | JSON Schema requires runtime/evaluation separation, evidence kind, callback time, action, state-reset policy, cost ledger, source receipt | MISSING |
| No-feedback parity | feedback disabled calls untouched corrected path; LLR/hard-bit/output digests and 20-iteration budget exactly match | `NOT_RUN` |
| Noise-free/correct-codeword | current interleaved adapter decodes clean codeword; syndrome observer reports zero; no action triggers | old non-interleaved pattern exists; candidate `NOT_RUN` |
| Callback lifecycle | flooding v2c trace is `it=0..N`, callback returns messages unchanged, callback exceptions fail closed | API MAPPED; `NOT_RUN` |
| Hidden-truth metamorphic | delete/permute payload truth, true phase/CFO/h/SNR and final correctness while holding receiver view fixed; evidence/action/output unchanged | current gamma-only receipt PARTIAL; candidate `NOT_RUN` |
| Caller→callee information boundary | recursive AST plus restricted type proves runtime action reaches only receiver-view fields and decoder evidence | old AST PARTIAL; candidate `NOT_RUN` |
| Raw receipt | one row/event contains frame/block/iteration/evidence/action/digests/reset policy and separates evaluation truth | MISSING |
| Iteration/latency/cost ledger | `bp_iter_total`, decoder calls, callback calls, front-end calls, hypotheses evaluated, recovery count, wall/device time; comparator budget matched | MISSING |

## Terminal

`TESTBED_HARD_BLOCKER`

Decoder soft/state/callback and interleaved bit-symbol mapping are adapter-ready in Sionna 2.0.1, but the audited corrected coded chain has no compatible carrier-recovery action caller/callee. No scientific conclusion follows from this readiness terminal.
