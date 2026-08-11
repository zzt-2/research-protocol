# Step 094 — D0 coded-chain / common-API asset map

> 2026-08-10 | action class: `SOURCE_AUDIT` | control: CP011 / epoch 11 / T048
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> audited HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`
> discipline: static/read-only evidence mapping; no import probe, pytest, D0/scientific run, web, source/test/result edit, commit or push

## 0. Verdict

`D0_ASSET_MAP_COMPLETE / IMPLEMENTABLE_WITH_WRAPPERS_AND_NEW_D0_SHELL / NO_PREIMPLEMENTATION_>7D_BLOCKER_ESTABLISHED`

The P08-R2 code identity, per-codeword bit/symbol mapping, 16QAM modulator/demapper, receiver-visible scalar-noise estimator, hard LDPC encode/decode kernel, common MMSE/limiter, and square-16QAM BPS kernel are reusable. They are **not** a legal D0 harness as assembled today. D0 still needs a truth-separated carrier/waveform shell, a persistent four-state suffix rotation, the pilot-extension map, a full-restart decoder wrapper, B0/B1/O1 semantics, source receipts, and D0-specific tests/results plumbing.

No frozen-contract hard blocker in `d0-defect-smoke-contract.yaml:423-428` is established by this audit. The items marked `BLOCKER` below block **direct reuse**, not D0 authorization: each has a bounded wrapper/new-code route. The largest newly exposed correctness risk is that P08-R2 sends the **same** 32-symbol prefix on X and Y (`p08r2_chain.py:213-215`) while its 2x2 LS estimator claims four independently identifiable channel coefficients (`p08r2_chain.py:107-131`); that default regressor is rank-deficient and must not be inherited without distinct/orthogonal polarization-known symbols plus a rank assertion.

## 1. Exact implementation BOM

### 1.1 `REUSE_AS_IS` — kernel only, under the stated boundary

| Object / exact signature | Source | Reusable fact and boundary |
|---|---|---|
| `qam16_mod(bits)` | `projects/simulation/common/_modulation.py:24-37` | Gray square-16QAM, `[b0,b1,b2,b3]`, average power 1. TX-side only. |
| `hard_decision(z, mod='qpsk')` with `mod='qam16'` | `_modulation.py:84-91` | Nearest square-16QAM level decision; array/scalar compatible. This is what BPS calls. |
| `_build_qam16_constellation() -> tuple[np.ndarray, np.ndarray]` | `p08_coded_chain.py:52-68` | Exact constellation and bit table matching `qam16_mod`. |
| `maxlog_soft_demap_16qam(z: np.ndarray, sigma2: float, llr_clip: float = 30.0) -> np.ndarray` | `p08_coded_chain.py:83-106` | Returns `[N,4] float32`; positive LLR means bit 1 is more likely. Reuse only with receiver-visible `sigma2`. |
| `_qam16_demod_to_bits(z: np.ndarray) -> np.ndarray` | `p08_coded_chain.py:431-440` | Truth/evaluator hard-bit helper; not a deployable ambiguity resolver. |
| `CodedContractR()` | `p08r_chain.py:88-120` | Frozen `k=1024,n=1536,Qm=4,num_iter=20,llr_max=20,alpha=.75`; `bg` is metadata and must be receipt-asserted against the encoder. |
| `CodecAdapterR.encode(self, info_bits: np.ndarray) -> np.ndarray` | `p08r_chain.py:123-156` | Batch `[B,1024] uint8 -> [B,1536] uint8`, with Sionna output interleaver enabled by `num_bits_per_symbol=4`. |
| `estimate_sigma2_from_prefix(rx_prefix: np.ndarray, tx_prefix: np.ndarray) -> float` | `p08r_chain.py:205-216` | Post-equalization residual scale from known symbols; safe only when the caller passes known prefix/pilots, never payload truth. |
| `split_prefix_data(arr: np.ndarray, n_prefix: int)` | `p08r_chain.py:363-365` | Pure slice helper. |
| `amp_limit(rx, thresh=3.0)` / `mmse_equalize(rx, h, gamma_bar)` | `common/_equalizer.py:5-16` | Numeric kernels only. The D0 wrapper must pass a receiver-visible noise/SNR surrogate, not true SNR. |
| `bps_cpr(rx, B=DEF_B_BPS, Nw=DEF_NW_BPS, mod='qpsk')` | `common/_recovery.py:91-118` | Core BPS kernel; call exactly with `mod='qam16'`. Returns `(corrected, phase_trace)`. It does not legally resolve the global pi/2 state by itself. |

### 1.2 `WRAP_ONLY`

| Object / exact signature | Why direct use is illegal or incomplete | Required wrapper contract |
|---|---|---|
| `CodecAdapterR(contract: CodedContractR)` and `decode(self, llr: np.ndarray)` | `decode` returns only hard information bits + configured-iteration metadata (`p08r_chain.py:126-178`); its tuple branch would mislabel Sionna `msg_v2c` as iterations if state were enabled. It has no shape assertion and no explicit restart receipt. | `D0Codec.decode_fresh(llr_cw, *, cw_ids, candidate_id) -> DecodeBatch`; clamp to 20, no state argument/reuse, assert `[B,1536]`, re-encode, compute normalized NLL, record one full restart and `B*20` BP iterations. |
| `llr_per_cw_from_eq(eq_data: np.ndarray, sigma2, contract: CodedContractR) -> np.ndarray` | Correct demap/reshape (`p08r2_phaseA.py:128-147`) but silently truncates through integer CW count assumptions and imports the old module tree. | Assert exactly `6144` data symbols / `16x1536` logits per polarization and expose data-rank-to-CW ownership. |
| `CalibrationPrefix(n_prefix_symbols=32, seed=987654321).symbols()` | Deterministic known prefix (`p08r_chain.py:185-202`), but P08-R2 copies the same sequence to both polarizations. | Generate two registered, full-rank known sequences or a polarization-orthogonal schedule; receipt their bytes/seed and assert LS rank 4. |
| `estimate_pre_eq_noise_from_prefix(rx_prefix_X, rx_prefix_Y, tx_prefix_X, tx_prefix_Y, floor=1e-9)` | Function is truth-free in isolation (`p08r2_chain.py:77-134`), but P08-R2's equal-prefix caller makes its advertised 4-unknown 2x2 LS rank-deficient. | Check equal lengths, finite inputs, `N>=3`, `matrix_rank(M)==4`; fail fast otherwise. Do not inherit the stated “60 dof” unless rank 4 holds. |
| `gamma_vis_from_prefix(sigma2_pre: float) -> float` | Correct numeric conversion (`p08r2_chain.py:137-145`), but needs finite/positive guard and receipt. | Validate finite positive variance; freeze semantics as receiver-visible equalizer tuning, not physical SNR truth. |
| `generate_shared_realization_dp(N, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None, t_s=None, method=None, modulation='qpsk')` | Produces its own random symbols/noise and only an SOP ramp (`common/_dual_pol_channel.py:56-149`); it cannot accept the coded/pilot waveform and has no linewidth/CFO carrier phase. P08-R2 therefore discards its random symbols/noise and copies the channel equation (`p08r2_chain.py:216-228`). | Reuse its GG envelope/config provenance through a D0 supplied-waveform channel factory; generate one shared carrier phase/fade and independent X/Y AWGN, then construct separate views. Do not call this generator merely to harvest `h/theta` and silently spend unused RNG draws. |
| `source_receipt(contract: CodedContract, adapter: CodecAdapter) -> dict` | Receipt logic hashes Sionna encoder/BG2 source (`p08_coded_chain.py:459-490`), but the exact signature is incompatible with `CodedContractR/CodecAdapterR` (`CodedContractR` has no `to_dict`, R adapter lacks `_bg/_z/_k_ldpc/_n_ldpc`). | D0 receipt wrapper must hash D0 files + Sionna encoder/decoder/BG2 CSV, record versions/device, and assert actual `enc._bg`, `enc._z`, `out_int/out_int_inv`. |
| `save_results(data, filepath, script_name)` | UTF-8 JSON + generic meta (`common/_experiment.py:164-196`), but mutates input, hashes only `_experiment.py`, is non-atomic, and does not emit required raw JSONL rows/source hashes. | D0 atomic JSON/JSONL writer with schema validation, contract/source SHA256, seed/cell/method completeness and no import-time directory creation. |
| `p08r2_verify.py` AST helpers / `p08r2_metamorphic_gate.py` pattern | Useful patterns, but current denylist omits payload/coded bits/boundary/final correctness and the runtime gate flips only `gamma_bar` (`p08r2_verify.py:58-143,208-260`; `p08r2_metamorphic_gate.py:86-118`). | D0-specific type + recursive-AST + metamorphic tests covering every TruthView field and candidate-order/state isolation. |

### 1.3 `NEW_D0_CODE`

1. Immutable `ReceiverView`, `TruthView`, `CodeLayout`, `WaveformLayout`, `CarrierReceipt`, `DecodeBatch`, and `CostLedger` types. No deployable function may accept a `CodedRealizationR2` or `TruthView`.
2. Pilot-extended waveform builder: keep all 6144 coded data symbols; prepend 32 known symbols; insert `pilot, N-1 data` periodically; add terminal pilot; maintain bijective `data_rank <-> absolute_time` maps. Existing `_experiment.insert_pilots()` replaces data in a QPSK frame (`_experiment.py:18-61`) and is not reusable.
3. Supplied-waveform dual-pol carrier/channel factory implementing the frozen shared carrier phase/GG fade, independent AWGN, linewidth/CFO receipt, and receiver/evaluator split. P08-R2 has no carrier phase/CFO/cycle-slip field (`p08r2_chain.py:153-277`).
4. Persistent suffix rotation at the frozen common-BPS output, copy-on-write candidate isolation, legal states `k in {0,1,2,3}` only, plus evaluator-only injected/natural event label.
5. Semantic D0 B0/B1/O1 paths. P08-R2's `method_B1` is only LLR temperature (`p08r2_phaseA.py:164-175`) and its `method_B2` is decoder tuning (`:178-194`); neither is the frozen D0 ladder.
6. Full-restart per-candidate decode/re-encode NLL and cache of unchanged-CW NLL. Soft callbacks/message state remain out of the minimum D0 route per contract line 401.
7. D0 runner/cache/receipt writer. Do not import `p08r2_run.py`: it creates its results directory at import time (`p08r2_run.py:49-50`).

### 1.4 `BLOCKER` — blocks direct reuse, not the D0 mission

| Blocker | Static evidence | Bounded exit |
|---|---|---|
| Receiver/truth co-location | `CodedRealizationR2` stores `r*` next to `s*`, `h`, `theta`, `cw_info_*`, `cw_bits_*`, `gamma_bar` (`p08r2_chain.py:163-186`). Deployable methods receive `real` and read `sX/sY` (`p08r2_phaseA.py:150-194`). | New immutable view factory; deployable signatures accept `ReceiverView` only; oracle/evaluator tree accepts `TruthView`. |
| Rank-deficient default dual-pol prefix LS | Same prefix copied to X/Y (`p08r2_chain.py:213-215`) while LS uses `[sX,sY]` as two columns per output (`:107-126`). | Distinct/orthogonal registered known sequences + rank assertion; otherwise fail before channel construction. |
| Missing carrier/slip/action anchor | Common dual-pol generator exposes only GG `h` and SOP ramp `theta`; P08-R2 has no linewidth/CFO phase trace or persistent slip (`common/_dual_pol_channel.py:103-149`; `p08r2_chain.py:216-277`). | New bounded D0 carrier/channel factory; no `common/` edit. |
| No direct square-16QAM BPS grid proof | Kernel has `mod='qam16'` path, but `test_common.py` tests BPS only on QPSK (`test_common.py:246-256,903-911`). | Parameterized D0 unit test over all 6 `(B,Nw)` pairs, target lengths, constant legal rotations, determinism, finite outputs and pilot-only four-state resolution. |
| Old receipt/results APIs are insufficient | Incompatible receipt signature; generic result writer lacks D0 row schema/atomicity/source chain. | New D0 receipt + atomic writer; unit tests in `tmp_path`. |

## 2. Exact coded-chain facts

### 2.1 Interleaver, CW/symbol ownership and source receipt

- `LDPC5GEncoder(k=1024,n=1536,num_bits_per_symbol=4)` is constructed at `p08r_chain.py:126-145`; `out_int/out_int_inv` are exposed at `:148-150`. There is no outer/cross-codeword interleaver.
- `CodedRealizationR2.realize()` encodes `[16,1024]` per polarization, flattens `[16,1536]` row-major, then calls `qam16_mod` (`p08r2_chain.py:206-215`). Thus one CW owns 384 adjacent **data ranks**.
- For data rank `t in [0,6143]`: `cw=t//384`, local symbol `j=t%384`, on-air CW bit positions `[4j,4j+1,4j+2,4j+3]`. Pilot extension changes absolute time indices, not this ownership.
- The verified current Sionna output-interleaver inverse mapping from step-086 is: pre-interleaver RM positions for local symbol `j` are `[j,384+j,768+j,1152+j]` (`step-086:102-110`). Current auto-selected BG2 receipt is `Z=104,k_ldpc=1040,n_ldpc=5408,filler=16`, with RM-to-VN mapping `208+r` for `r<816`, else `224+r` (`step-086:112-131`). D0 must derive/assert this from the live encoder, not hardcode it as authority.
- `CodedContractR.bg='bg2'` is not passed to the Sionna constructor; actual BG identity must be asserted and written to the receipt.

### 2.2 LLR sign and decode API

- Demapper formula is `min(bit=0)-min(bit=1)` divided by `2*sigma2`; therefore positive means bit 1 (`p08_coded_chain.py:83-106`). This matches the declared Sionna decoder convention in `CodedContractR.sign_convention` (`p08r_chain.py:103`). Do not negate it.
- Exact current API is `CodecAdapterR.decode(self, llr: np.ndarray)` (`p08r_chain.py:158-178`). Expected input is batched `[B,1536] float32`, on-air/post-interleaver order; it clamps to `[-20,20]`, calls one fixed-20-iteration `LDPC5GDecoder`, and returns `[B,1024] uint8` plus `{'num_iter_configured':20}`.
- Every changed LLR candidate must call the stateless wrapper afresh with no previous `msg_v2c`; decoder object caching is allowed, message-state caching is not. Candidate order must be metamorphically invariant.
- Re-encode score uses receiver-visible channel logits and `c_hat=encode(u_hat)`: `sum(softplus((1-2*c_hat)*Lch))`, normalized by the same total evaluated coded bits for every candidate.
- `resolve_qam16(rx, tx_bits)` is forbidden: it tries eight `pi/4` rotations and selects by TX BER (`common/_modulation.py:63-69`). It is neither a legal four-state receiver action nor a deployable score.

## 3. Receiver/Truth views, waveform, rotation and restart ownership

### 3.1 Minimum exact interfaces

```python
@dataclass(frozen=True, slots=True)
class ReceiverView:
    eq_waveform: np.ndarray       # [2, N_time], common-BPS output
    cpr_phase: np.ndarray         # [2, N_time]
    known_symbols: np.ndarray     # [2, N_time], undefined where known_mask=False
    known_mask: np.ndarray        # [N_time] bool (prefix + periodic + terminal)
    noise_var: np.ndarray         # receiver-visible, frozen semantics
    data_to_time: np.ndarray      # [6144]
    time_to_data: np.ndarray      # [N_time], -1 at known-only positions
    code_layout: CodeLayout
    front_end_id: str

@dataclass(frozen=True, slots=True)
class TruthView:
    info_bits: np.ndarray         # [2,16,1024]
    coded_bits: np.ndarray        # [2,16,1536]
    data_symbols: np.ndarray      # [2,6144]
    true_fade: np.ndarray
    true_carrier_phase: np.ndarray
    noise_receipt: object
    event_receipt: object

def build_views(...) -> tuple[ReceiverView, TruthView]: ...
def apply_persistent_rotation(view: ReceiverView, *, target_pol: int,
                              boundary_after_data: int, k: int) -> ReceiverView: ...
def decode_fresh(llr_cw: np.ndarray, *, cw_ids: np.ndarray,
                 candidate_id: str) -> DecodeBatch: ...
```

The factory is the only function allowed to see channel truth and must return disjoint objects. All deployable B0/B1/B2/S3 functions accept only `ReceiverView`; O1 and scoring accept both only after deployable outputs freeze.

### 3.2 Pilot extension and persistent boundary

- For frozen `N`, construct one periodic known pilot followed by at most `N-1` data symbols, continuing until all 6144 data symbols are placed, then append a terminal pilot. Pilot count is `1 + ceil(6144/(N-1))`: `{10:684,20:325,100:64,200:32}` (`d0 contract:132-143`). No coded symbol is replaced or punctured.
- The 32-symbol calibration prefix remains additional overhead. Known/pilot sequences must be receiver registered and polarization-distinct enough for the pre-EQ LS rank gate.
- Controlled boundaries are expressed in **data rank**: after 1536/3072/4608 data symbols, hence affected CW IDs `4..15`, `8..15`, `12..15` respectively. Map the first suffix data rank to absolute time and rotate the entire persistent physical suffix (including later pilots) on exactly one target polarization.
- Legal rotation factor is exactly `exp(1j*k*pi/2)` for integer `k in {0,1,2,3}`. Reject floats, out-of-range states and any `pi/4`/eight-state resolver.
- Candidate buffers are copy-on-write. The other polarization is the clean sentinel and must remain byte-identical. Injection is evaluator/test-fixture code at the frozen common-BPS output, never a field in `ReceiverView`.
- S3 ownership explains the frozen 88 CW decodes per target-pol case: no-op full frame `16` plus three rotations times suffix CW counts `(12+8+4)=24`, i.e. `16 + 3*24 = 88`. Each candidate's changed CW batch is a full decoder restart; unchanged-CW NLL may be cached read-only.

## 4. Square-16QAM BPS API verdict and old-conclusion conflict

### 4.1 Static API verdict

`bps_cpr(rx, B, Nw, mod='qam16')` is statically compatible with `B={32,64}` and `Nw={31,61,127}` for every D0 frame length: neither parameter is hardcoded, `B` controls the phase grid/first array dimension and `Nw` the convolution kernel (`common/_recovery.py:91-118`). The target frames are much longer than 127, avoiding the function's unguarded `Nw>len(rx)` assignment hazard.

This is **not runtime verification**. The common test suite covers QPSK BPS at defaults and `(B=32,Nw=10)` only (`test_common.py:246-256,903-911`). The D0 wrapper must validate `B` as a positive multiple of four, `Nw` as a positive odd integer `<=len(rx)`, finite nonempty complex input, and must run the full 6-pair parametrized unit gate before any D0 seed.

### 4.2 Conflict with `毕设/CONCLUSIONS.md` (do not edit here)

`CONCLUSIONS.md:376-384` says BPS uses `sign(Re/Im)`, assumes QPSK and is incompatible with 16QAM; `:161-162` likewise excludes BPS as 4th-power/QAM-incompatible. Current code contradicts the BPS portion: `bps_cpr(...,mod='qam16')` delegates to `hard_decision`, whose 16QAM branch slices to four amplitude levels per axis (`_recovery.py:91-105`; `_modulation.py:84-91`). A tested 16QAM BPS wrapper also exists elsewhere, but the frozen D0 implementation asset remains the common kernel. This audit does not validate or rewrite the old scientific performance conclusions.

## 5. Proposed D0 file/test responsibility tree and minimum TDD order

Code root is the registered but currently absent `projects/simulation/explore/coded-decoder-feedback/`. Names below are deliverables, not files created by this audit.

| Order | New file | Independently reviewable deliverable | Test file / fail-fast gate |
|---:|---|---|---|
| 1 | `d0_types.py` | Frozen views/layouts/receipts/cost types; no import-time I/O | `projects/simulation/tests/test_d0_types_and_truth_boundary.py`: field denylist, frozen arrays/types, deployable signatures contain no TruthView fields |
| 2 | `d0_coded_chain.py` | P08-R2 contract/encoder wrapper, live interleaver receipt, exact ownership, LLR stack, `decode_fresh`, re-encode NLL | `test_d0_coded_chain.py`: noiseless encode/demap/decode, LLR sign, 16x384 mapping, output-interleaver round-trip, actual BG assertion, candidate-order/state-reset, cost counts |
| 3 | `d0_waveform.py` | prefix + pilot extension and bijective data/time map; legal persistent rotations, copy isolation | `test_d0_waveform.py`: all four N counts/lengths, no replace/puncture, terminal pilot, boundaries/CW sets, 4-state metamorphic mapping, sentinel unchanged |
| 4 | `d0_bps.py` | validated common `bps_cpr` wrapper, `(B,Nw)` grid, pilot-only global four-state resolver and cache key | `test_d0_bps.py`: all 6 pairs, target lengths, finite/deterministic output, constant `k*pi/2`, reject invalid/eight-state/TX-bit routes |
| 5 | `d0_channel.py` | supplied-waveform dual-pol GG + shared carrier phase/CFO + independent AWGN; full-rank known prefix; view split | `test_d0_channel.py`: seed determinism, shared phase/fade, independent noise, rank-4 prefix, receiver truth metamorphics, no-slip/noiseless identity |
| 6 | `d0_baselines.py` | B0/B1/O1 semantic IDs, global four-rotation re-encode selection, affected-CW decode cache; B2 only through T049's frozen interface | `test_d0_baselines.py`: B0/B1/O1 identity, all rotation/boundary O1 zero error, 88 CW ledger, restart/candidate isolation, no `resolve_qam16` |
| 7 | `d0_runner.py` + `d0_io.py` | lazy orchestration, cache, atomic raw JSONL + summary/receipt, no import-time mkdir | `test_d0_runner_io.py`: `tmp_path` atomicity, raw required fields, hashes/version/device, finite deterministic scores, partial-write recovery, no source/result creation on import |

Run order after implementation: pure NumPy types/waveform first; coded/Sionna fixture second; BPS/channel third; baseline integration fourth; runner/receipt last. No scientific seed may start until every unit gate and S4 static/metamorphic gate passes.

## 6. Import, device, runtime, cache and output risks

| Risk | Static evidence | Required fail-fast gate |
|---|---|---|
| Hyphenated source directories and `sys.path` mutation | P08 modules manually insert paths (`p08r_chain.py:47-69`; `p08r2_chain.py:49-70`). | One D0 test loader fixture; no duplicate module names; assert resolved `__file__` belongs to this evidence worktree. |
| Import-time global/device side effects | `torch.set_default_device('cpu')` at `p08r_chain.py:44` and `p08r2_chain.py:47`; `p08r2_run.py`/metamorphic gate mkdir on import. | D0 production modules perform no mkdir/run; lazy adapter construction; receipt `torch/sionna/numpy` versions and actual tensor device; explicit CPU contract or fail. |
| Sionna version/private drift | Adapter depends on `out_int/out_int_inv` and old receipt uses private graph fields. Step-086 observed Sionna 2.0.1. | Fixture imports inside the test, fails with an explicit dependency/version message, instantiates once, asserts shapes, actual BG/Z, permutation inverses, hard-output shape and state-disabled semantics. Do not silently skip required D0 tests. |
| Decoder contamination/cost undercount | Current R adapter has speculative tuple-state labeling; B2 recreates codec per method call (`p08r2_phaseA.py:178-191`). | Cache encoder/decoder object only; never message state; run candidates forward/reverse and compare bit-identically; ledger asserts restart/CW/BP counts, including S3 maximum 47,520 CW decodes. |
| BPS runtime/memory | Kernel materializes `[B,N]` rotated/metric arrays and performs B convolutions (`_recovery.py:98-116`); dev grid has six pairs. | Validate/canonicalize cache key `(waveform_receipt,pol,B,Nw)`; one bounded timing ledger in authorized D0 execution, never during import; abort on nonfinite output or unexpected shape. |
| Pilot/CW index confusion | Existing P08 mapping assumes contiguous 6144 data symbols; D0 extends time support. | Round-trip `time_to_data[data_to_time[t]]==t`; pilots map to -1; boundary tests assert exact affected CW IDs. |
| Pycache/pytest cache pollution | Import/pytest can create `__pycache__`/`.pytest_cache`; T048 forbids it now. | Future controlled command uses `PYTHONDONTWRITEBYTECODE=1`, `python -B`, and `pytest -p no:cacheprovider`; pre/post path census. No such command was run in this audit. |
| Non-atomic/incomplete output | Common `save_results` is generic/non-atomic; P08-R2 uses import-time OUT and `json.dump(...,default=str)` (`p08r2_run.py:369-387`). | Temp-file + `os.replace`, JSON schema validation, raw-row count/cluster completeness, SHA256 receipts, and a deliberate write-failure unit test. |

## 7. Protection summary

- Intended filesystem delta: this file only, `projects/thesis-fso/worker-logs/step-094-d0-coded-chain-asset-map.md`.
- No existing source, test, result, contract, session/governance file or `common/` file was edited.
- No import probe, pytest, D0/scientific execution, web/search/download, commit or push was performed.
- The pre-existing dirty worktree was preserved. The four protected logs had pre-write SHA256 values:
  - `p05_run.log`: `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`: `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`: `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`: `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`

