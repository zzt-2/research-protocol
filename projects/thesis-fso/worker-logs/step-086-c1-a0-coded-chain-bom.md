# Step 086 — C1 A0 P08-R2 coded-chain / observability / BOM fresh source audit

> 2026-08-10 | action class: `SOURCE_AUDIT` | control: CP010 / epoch 10
> worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> HEAD at audit start: `715a65884b988ee737f21982f3bbf372860a1da8`
> scope: read-only source/API audit; no web, download, code change, experiment, commit or push

## 0. Verdict and claim ceiling

| Item | Verdict |
|---|---|
| Current decoder evidence | `HARD_INFO_ONLY_FIXED_20_ITER`; channel LLR exists, but decoder posterior/state/convergence is not returned |
| Segment observability | `BOUNDED_CODEWORD_LOCALIZABLE_NOT_BOUNDARY_IDENTIFIABLE` |
| Interleaver effect | Not a fatal blocker: it is deterministic and confined within each 1536-bit codeword; no cross-codeword interleaver exists in P08-R2 |
| Adapter/testbed status | `BOUNDED_DECODER_ADAPTER + CARRIER/SLIP/ACTION_TESTBED_GAP` |
| Estimated minimum build | **6.50 days**, in 0.25-day increments, including identity/truth/cost tests |
| `>7D_BLOCKER` | **`NOT_ESTABLISHED`** under the reduced codeword-owned likelihood route |

The strongest source-backed observability claim is:

> A received-symbol interval can be mapped exactly to its touched codeword(s), on-air bits, pre-interleaver rate-matched bits, and current BG2 mother-code variable-node columns. Decoder/re-encode evidence can therefore be attributed at **touched-codeword / touched-check-set** level. The present chain cannot identify a unique physical slip boundary, nor can it claim a local syndrome at symbol resolution: there is no carrier-slip state, CRC, boundary callback, or exposed full-graph decoder posterior.

This audit did **not** read or inherit `step-061`; all conclusions below were rebuilt from the current P08-R2 sources and the installed Sionna 2.0.1 source.

## 1. Source inventory and caller → callee chain

### 1.1 Audited sources

| Source | Role | Relevant facts |
|---|---|---|
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_run.py:53` | top-level caller | builds one paired realization, equalizes once, dispatches B0/B1/B2/O0/O1/O2 |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_chain.py:153` | frame/channel/equalizer | creates 16 codewords/polarization, prepends 32 known symbols, stores receiver and truth fields together |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py:128` | demap/decoder callers | produces per-codeword channel LLR and calls the decoder once per polarization |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:89` | codec contract/adapter | creates Sionna encoder/decoder, exposes output-interleaver permutation, returns hard information bits |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py:83` | 16QAM demapper | max-log channel logits, `[Nsym,4]`, `float32`, `log(p1/p0)` convention |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_verify.py:210` | current truth gate | recursively denies only `gamma_bar/h_truth/theta`; deliberately whitelists `sX/sY` because the prefix is known |
| `C:/Users/zzt/scoop/apps/python311/current/Lib/site-packages/sionna/phy/fec/ldpc/encoding.py` | installed encoder 2.0.1 | rate matching and per-codeword output interleaver |
| `C:/Users/zzt/scoop/apps/python311/current/Lib/site-packages/sionna/phy/fec/ldpc/decoding.py` | installed decoder 2.0.1 | soft/hard output, per-call iteration override, callbacks, and recurrent message state are available but unused by P08-R2 |

Installed package receipt from `python -B -m pip show sionna`: version `2.0.1`, location `C:\Users\zzt\scoop\apps\python311\current\Lib\site-packages`.

### 1.2 Current call graph

```text
p08r2_run.build_realization(...)
  -> CodedRealizationR2(...).realize()
       -> CodecAdapterR.encode(info_X)  # one batch call, B=16
       -> CodecAdapterR.encode(info_Y)  # one batch call, B=16
       -> qam16_mod(cw_bits.reshape(-1))
       -> generate_shared_realization_dp(...) + explicit channel/noise draw
  -> CodedRealizationR2.equalize()
       -> estimate_pre_eq_noise_from_prefix(...)
       -> mmse_equalize(...) + amp_limit(...)

p08r2_run.run_method(...)
  -> method_B0 / method_B1 / method_B2 / method_oracle
       -> split_prefix_data(eq_pol, 32)
       -> estimate_sigma2_from_prefix(...) or privileged oracle_sigma2_*(...)
       -> llr_per_cw_from_eq(eq_data, sigma2, contract)
            -> maxlog_soft_demap_16qam(...)
            -> reshape(n_cw,1536)
       -> CodecAdapterR.decode(llr_cw)  # X once, Y once
            -> LDPC5GDecoder(llr_t)
```

### 1.3 Exact shapes, dtypes and decode count

The current default is `n_cw_per_pol=16`, `k=1024`, `n=1536`, Gray 16QAM, 32 known prefix symbols.

| Object | Shape per polarization | dtype / semantics | Source |
|---|---:|---|---|
| `info_X/Y` | `[16,1024]` | NumPy `uint8`, TX truth | `p08r2_chain.py:206-210` |
| `cw_bits_X/Y` | `[16,1536]` | NumPy `uint8`, on-air post-interleaver bits | `p08r_chain.py:152-156` |
| flattened coded bits | `[24576]` | row-major CW0…CW15 | `p08r2_chain.py:211-212` |
| data symbols | `[6144]` | NumPy complex (current modulator arithmetic yields `complex128`) | 384 symbols/CW |
| prefix + data `sX/sY`, `rX/rY` | `[6176]` | complex; `s*` includes known prefix **and TX data truth** | `p08r2_chain.py:213-233` |
| equalized data `eqd` | `[6144]` | complex | prefix removed in `p08r2_phaseA.py:154` |
| raw demapper logits | `[6144,4]` | `float32`, `log(p1/p0)` | `p08_coded_chain.py:83-106` |
| decoder input | `[16,1536]` | NumPy/Torch `float32`, on-air bit order | `p08r2_phaseA.py:128-147` |
| decoder output | `[16,1024]` | NumPy `uint8`, hard information bits only | `p08r_chain.py:158-178` |
| current diagnostics | scalar dict | only `num_iter_configured=20` | no convergence or actual per-CW iteration count |

For **each method on one realization**, decoding is invoked exactly **twice**: once for X and once for Y. Each invocation batches 16 codewords, so it performs 32 codeword decodes at 20 fixed BP iterations. Sionna explicitly has no early stopping in this path. B2 additionally constructs a fresh encoder/decoder object on every `method_B2` call (`p08r2_phaseA.py:178-191`), which must not be counted as method gain and should be cached in a future cost-fair implementation.

`CodecAdapterR.decode()` contains a speculative tuple branch that labels the tuple's second value as `iterations_per_cw`. Under Sionna 2.0.1, if `return_state=True`, that value is **`msg_v2c` decoder state**, not an iteration count. The current decoder has `return_state=False`, so the branch is inactive and no state is returned.

## 2. Exact bit/symbol/interleaver/rate-match mapping

### 2.1 Codeword and symbol ownership

No outer or cross-codeword interleaver exists. `cw_bits.reshape(-1)` preserves row-major codeword order, and 1536 is divisible by four. For a **data** symbol index `t` (prefix already removed):

```text
cw = floor(t / 384)
j  = t mod 384              # local symbol within codeword
on-air bit positions in CW = [4j, 4j+1, 4j+2, 4j+3]
full received-array index   = 32 + t
```

Therefore an interval `[a,b)` touches codewords `floor(a/384)` through `floor((b-1)/384)`. A segment crossing a CW boundary maps to multiple codewords; it is not silently assigned to one.

### 2.2 Output-interleaver inverse

Sionna generates the 3GPP output interleaver at `encoding.py:303-340` and encodes with `c_out[..., out_int]` at `encoding.py:791-793`. For `n=1536`, `Qm=4`, local symbol `j` carries pre-interleaver rate-matched indices:

```text
rm(j) = [j, 384+j, 768+j, 1152+j]
```

This spreading is deterministic and stays inside one codeword. It prevents treating four adjacent on-air bit positions as four adjacent parity-graph columns, but it does **not** prevent exact inverse mapping.

### 2.3 Current mother-code VN mapping

`CodedContractR.bg="bg2"` is metadata only; `CodecAdapterR` does not pass `bg` into `LDPC5GEncoder`. For the frozen `k=1024,n=1536` values, Sionna's auto-selection nevertheless selects BG2. Static evaluation of `encoding.py:346-386,458-515` gives:

```text
BG2; Z=104; k_ldpc=1040; n_ldpc=5408; filler=16; first 2Z=208 punctured
RV0 c_out = first 1536 entries of the compressed rate-match buffer
n_sys_rm = k - 2Z = 816
```

For a pre-interleaver rate-matched index `r in [0,1535]`, its full mother-code VN column is:

```text
vn(r) = 208 + r,  if r < 816        # unpunctured systematic region
        224 + r,  if r >= 816       # filler [1024,1039] skipped; parity region
```

Thus each received symbol maps to four exact current VN columns. For `j<48`, it owns three systematic and one parity bit; for `j>=48`, two systematic and two parity bits. The union of nonzero rows in `encoder.pcm[:, VN(segment)]` is the exact **touched-check set**.

This mapping is frozen only for current `(k,n,Qm,RV)=(1024,1536,4,0)`. A future adapter must derive it from encoder properties (`z`, `k_filler`, `out_int/out_int_inv`) and assert it at runtime, not hardcode the numbers. It must also pass `bg=contract.bg` or verify actual BG identity to prevent silent contract drift.

## 3. Decoder evidence capability audit

| Primitive | Current P08-R2 | Installed Sionna 2.0.1 | Minimum disposition |
|---|---|---|---|
| Channel soft LLR | **Present**: `[P,CW,1536] float32` after a thin stack | accepted directly | reuse |
| Decoder posterior logits | absent; decoder is `hard_out=True`, `return_infobits=True` | `hard_out=False`; use `return_infobits=False` for on-air `[B,1536]` alignment | thin decoder adapter |
| Hard info bits | **Present** `[B,1024]` | present | reuse |
| Fixed iteration budget | **Present**, 20 | present | reuse |
| Per-call iteration override | not exposed | `decoder(llr, num_iter=i, msg_v2c=state)` | thin adapter |
| Message state | not exposed | `return_state=True` returns `msg_v2c [B,E]`; it is not an iteration count | thin adapter |
| Per-iteration VN/CN callbacks | not configured | constructor accepts `v2c_callbacks` / `c2v_callbacks`; VN callback sees posterior `x_hat` | thin adapter; callback must return messages unchanged |
| Early stop / convergence flag | absent | explicitly absent for batching | do not claim; build receiver-visible stopping rule externally if needed |
| CRC | absent | not supplied by this LDPC component | unavailable unless a new outer-code contract is authorized |
| Syndrome/parity evidence | absent from `CodecAdapterR` | encoder exposes `pcm`, callbacks expose graph messages | adapter required; exact spatial interpretation is graph-global |
| Re-encode likelihood | pieces present: hard `uhat`, `encode`, channel LLR | no special API needed | thin utility |

Important limitation: the old `CodecAdapter.syndrome_check(encode_full_for_syndrome(uhat))` in `p08_coded_chain.py:192-215` only checks a **re-encoded valid codeword**. Its syndrome is zero by construction and is an identity test, not decoder-failure localization. Useful receiver evidence is instead one of:

1. codeword likelihood of `c_hat=encode(uhat)` against channel logits,
   `NLL_cw = sum softplus((1-2*c_hat_i)*Lch_i)`;
2. posterior/channel disagreement aggregated over the exact touched RM/VN set;
3. soft parity/check reliability captured from decoder callbacks and aggregated over `touched-check-set`.

Route 1 is the minimum robust path. Route 3 is optional higher-resolution evidence; it must not directly interpret edge-state index as a symbol location because Sionna returns pruned active-graph edge messages.

## 4. Observability and localization verdict

### 4.1 What is observable now or with a thin adapter

- Exact touched CW/RM/VN/check ownership for any candidate interval.
- Per-CW channel-logit dispersion, entropy and clipping rate.
- Hard decoded information, re-encoded on-air codeword, and receiver-visible codeword NLL.
- With the decoder adapter: full on-air posterior logits, iteration snapshots, and recurrent `msg_v2c` state.
- A receiver-visible trigger can therefore rank **candidate** intervals/boundaries by the change in touched-codeword likelihood under bounded phase hypotheses.

### 4.2 What cannot be claimed

- A parity failure does not uniquely identify a physical slip boundary; LDPC checks couple dispersed VN columns.
- The current chain has no CRC, so it cannot claim CRC-segment ownership or CRC-confirmed boundaries.
- The current chain has no carrier phase, CFO, cycle-slip event, carrier estimator state, boundary field, or correction action. SOP `theta` is not a substitute for carrier phase slip.
- No current API returns a per-symbol decoder syndrome or a converged/failed flag.
- Boundary resolution cannot be finer than the predeclared candidate grid/window, and a selected boundary remains a receiver-likelihood hypothesis, not ground truth.

**Verdict:** the interleaver does not make localization impossible. The minimum legal metric is **touched-codeword re-encode likelihood**, optionally plus touched-check soft reliability. The claim ceiling is “receiver-visible candidate boundary ranking and bounded recovery,” not “decoder identifies the true slip boundary.”

## 5. Minimum legal interface graph

```text
ReceiverView (truth-free)
  rx/eq data + known prefix + sigma2 + CodeLayout
        |
        v
decode_evidence(llr_cw, num_iter, state=None)
  -> hard u_hat, on-air posterior, msg_v2c, optional read-only iter trace,
     reencoded c_hat, cw_nll, touched-check evidence
        |
        v
trigger(cw evidence) -------------- no trigger --> CLEAN_NO_OP
        |
        v
boundary_candidates(candidate grid; receiver-visible only)
        |
        v
for each {boundary, interval, phase_hypothesis} within budget:
  rotate/remap local or suffix samples -> redemap affected symbols
  -> decode touched CWs -> receiver-visible re-evaluate -> cost ledger
        |
        v
select only if margin/stability rule passes; include no-op in candidate set
        |
        +--> accepted local/suffix action
        +--> no-op / canonical B1 then B2 fallback
```

### 5.1 Field ownership

| Interface / field | Status | Notes |
|---|---|---|
| `eq_data[P,Nsym]`, known prefix, prefix-derived `sigma2` | existing | must be copied into a truth-free receiver view, not passed through `real` |
| `CodeLayout{cw_n=1536,k=1024,qm=4,sym_per_cw=384,out_int,rm_to_vn,pcm}` | thin adapter | derive/assert from encoder at runtime |
| `llr_ch[P,CW,1536]` | existing + thin stack | current demapper already produces it |
| `DecoderEvidence{u_hat,c_post_logit,state,iter_trace,cw_nll,check_score}` | thin adapter | current adapter returns only `u_hat` |
| `Trigger{cw_ids,score,threshold,reason}` | thin method layer | receiver-visible only |
| `BoundaryCandidate{symbol_index,interval_kind,length,rotation}` | new method/testbed | no true boundary field allowed |
| local/suffix phase rotation and selective redemap | new action | simple array operation, but meaningful only after carrier-slip testbed exists |
| bounded touched-CW decode/re-evaluate | thin method layer | cache decoders; count calls/iterations/CW-symbol work |
| clean no-op identity | new control path | exact baseline output when no action is accepted |
| C1 canonical B1 global finite phase-hypothesis selection | **missing/new** | P08-R2 `method_B1` is only LLR temperature; it is not the topic's B1 |
| strongest cheap B2 | partial | P08-R2 B2 is LLR clip + decoder tuning; final A0 baseline contract must decide whether an additional conventional carrier fallback is required |
| carrier phase/CFO/slip generator and receiver carrier state | **new testbed** | current P08-R2 has none |
| oracle true boundary/correction | evaluator only | may score headroom; never enters deployable candidate generation/selection |

The P08-R2 names `B1/B2` collide with the current C1 baseline ladder. The implementation must use explicit semantic identifiers rather than silently treating P08-R2 temperature-B1 as the canonical global finite-hypothesis B1.

## 6. Caller → callee truth denylist

### 6.1 Denied fields in the deployable path

`TX payload/info bits`, `cw_bits`, TX data symbols, true carrier phase, true CFO, true channel/fade `h`, true SNR/`gamma_bar`, SOP truth `theta`, true slip boundary, oracle correction, and post-hoc/final correctness must not be members of `ReceiverView`, callback closures, trigger inputs, candidate generation, selection, or fallback selection.

Allowed exceptions are narrowly scoped: known calibration/pilot prefix; channel simulator truth used before receiver construction; evaluator/oracle truth used after deployable output is frozen.

### 6.2 Current leakage surfaces

| Surface | Risk | Required fence |
|---|---|---|
| `CodedRealizationR2` stores `sX/sY`, `h`, `theta`, `cw_info_*`, `cw_bits_*`, `gamma_bar` beside `rX/rY` (`p08r2_chain.py:163-186`) | any method receiving `real` can read truth | construct a separate immutable `ReceiverView`; deployable functions must not receive `real` |
| `equalize()` reads `self.sX/self.sY` then slices the prefix (`p08r2_chain.py:248-253`) | logically legal today, structurally exposes TX data | pass `known_prefix_X/Y` as separate arrays; do not retain TX data symbols in receiver object |
| B0/B1/B2 read prefix through `getattr(real,"sX/sY")` (`p08r2_phaseA.py:150-194`) | same structural leak | pass prefix explicitly |
| `method_oracle()` reads true data symbols `sd` (`p08r2_phaseA.py:197-216`) | privileged path shares signature/dispatcher with deployable methods | move oracle into evaluator namespace with a different input type |
| `score_trajectory()` reads `cw_info_*`; `trajectory_evidence()` reads `real.h` (`p08r2_phaseA.py:219-250`) | legal scoring can feed back into online decisions if object reused | freeze action/output first; scoring receives a separate `TruthView` |
| `run_method(method_id, real,...)` dispatches deployable and oracle paths (`p08r2_run.py:65-73`) | string switch is not an information boundary | separate caller trees/types |
| current verifier denylist only checks `gamma_bar/h_truth/theta` and explicitly whitelists `sX/sY` (`p08r2_verify.py:225-258`) | it does not prove payload/bit/boundary isolation for the new method | expand AST + metamorphic denylist to payload, coded bits, data symbols, phase/CFO/boundary/correction/final correctness |

## 7. Minimum 3–7 day BOM

All estimates are implementation-plus-test estimates in 0.25-day increments. They do not authorize implementation or experiment.

| Work item | Days | Dependency / acceptance |
|---|---:|---|
| Freeze truth-free `ReceiverView` / `TruthView` / oracle separation and semantic baseline IDs | 0.50 | no deployable function receives `real`; denylist type/AST test |
| Build/assert CW↔symbol↔RM↔VN↔check mapper and touched-CW likelihood primitive | 0.75 | round-trip permutation tests; cross-CW interval tests; no hardcoded mapping without runtime assertion |
| Add cached decoder-evidence adapter: soft on-air output, per-call `num_iter`, state, read-only callbacks, re-encode NLL | 0.75 | state is never mislabeled as iteration count; callback identity test |
| Add minimal carrier phase/CFO/slip channel slice plus receiver-visible carrier state/action anchor | 1.50 | same paired realization for all methods; truth boundary isolated in evaluator |
| Implement trigger → bounded boundary grid → local/suffix rotation/remap → selective redemap/decode/re-evaluate | 1.25 | no-op included; hard decode/iteration/candidate budget |
| Implement canonical global finite-hypothesis B1 and frozen cheap B2 fallback contract | 0.50 | same inputs, action space and tuning opportunity; resolve P08-R2 naming collision |
| Identity, clean no-op, truth metamorphic, callback/state reset, mapping, rollback/candidate isolation and cost-ledger tests | 1.00 | none may be dropped to meet budget |
| Minimal run/receipt plumbing and source/provenance manifest | 0.25 | raw per-candidate/CW/iteration-cost rows; no scientific run included |
| **Total** | **6.50** | within the authorized planning ceiling; actual build remains forbidden at CP010 |

### 7.1 Dependencies

1. A0 must freeze the physical slip/CFO impairment and quantitative kill thresholds before code work.
2. A0 must freeze the semantic B1/B2 contracts; current P08-R2 method names are insufficient.
3. Sionna 2.0.1 and the current 16QAM/LDPC chain are locally available.
4. The minimum route uses public encoder properties plus decoder constructor/call APIs. Exact active-edge-to-original-CN attribution may touch private/pruned graph internals and is not required for the reduced route.

### 7.2 `>7D_BLOCKER` rule

Set `>7D_BLOCKER=YES` before implementation if **any** of the following is established and no listed shrink preserves the method identity:

- the physical defect needs a new full carrier receiver/equalizer rather than the 1.50-day bounded phase/CFO/slip slice;
- the contribution requires exact symbol-level syndrome/CRC boundary ownership, forcing a custom unpruned decoder/outer-code implementation;
- canonical B1 cannot be implemented from the same receiver-visible inputs and phase-action API within 0.50 day;
- receiver/evaluator truth separation or clean no-op cannot pass after one bounded repair;
- callback/state reuse changes the baseline output, or cost/iteration accounting cannot be made method-comparable;
- future interleaving spans codewords, invalidating the current CW-local mapping and pushing the revised tested BOM above 7.00 days.

Current audit result: **none is established**. The principal gap is known and bounded: carrier/slip/action testbed plus thin evidence adapter.

### 7.3 Minimum shrink if the detailed graph route exceeds budget

Preserve all identity/truth/cost tests and shrink only scientific granularity:

1. codeword-aligned boundary grid (384-symbol ownership) before any finer grid;
2. suffix-only `0,π/2,π,3π/2` rotation candidates plus explicit no-op;
3. touched-codeword re-encode NLL only; omit exact CN-message localization and recurrent state from the first slice;
4. decode only touched codewords, with a fixed candidate/iteration budget;
5. fall back to canonical global B1 then frozen cheap B2.

This shrink still tests the complete deployable chain. It may only support a codeword/suffix-recovery claim; it cannot be described as exact decoder-syndrome localization.

## 8. Audit closure

- Task-control validator: `PASS` for T040 against CP010/epoch 10.
- Fresh sources inspected: current P08-R2 caller/chain/demapper/codec/verifier and installed Sionna 2.0.1 encoder/decoder source.
- No web, download, experiment, code execution of the scientific chain, or central/common modification was performed.
- Only this `step-086` worker log is an intended filesystem addition.

