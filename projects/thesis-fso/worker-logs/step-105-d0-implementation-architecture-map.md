# Step 105 — D0 v3 implementation architecture map

> 2026-08-10 | T059 / D011 / V005 / CP012 / epoch 12 | `SOURCE_AUDIT`
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> boundary: static architecture salvage only; no project import, pytest, D0, benchmark, science, owner/governance/source/test/result edit, commit or push

## 1. Findings first / verdict

```text
VERDICT = IMPLEMENTATION_ARCHITECTURE_READY
HARD_BLOCKER = NO
COMMON_OR_LEGACY_EDIT_REQUIRED = NO
TRUTHVIEW_IN_RECEIVER_PATH_REQUIRED = NO
B2_DECODER_FEEDBACK_REQUIRED = NO
SCIENTIFIC_ACTION_AUTHORIZED = NO
```

The frozen D0 v3 contract can be implemented wholly under
`projects/simulation/explore/coded-decoder-feedback/` with a new truth-separated
shell, wrappers around the P08 coded-chain assets, and imported numerical
kernels.  No `common/` or old P08 source edit is required.

The apparent P08-R2 dual-polarization prefix blocker is not inherited.  Its
same-X/Y prefix makes the advertised 2x2 LS regressor rank deficient, but v3
requires no SOP and a scalar per-polarization front end.  D0 therefore does not
import or call `estimate_pre_eq_noise_from_prefix`; it estimates one complex
gain per polarization and uses `RSS/31` for the 32-symbol prefix.

P08's demapper argument is variance per real dimension.  D0's post-BPS
`C_post` is complex residual power, so the only legal adapter call is
`maxlog_soft_demap_16qam(..., sigma2=C_post/2)`.  B2 similarly passes `N0/2` to
the inner P08 max-log metric.  These conversions belong in one codec boundary,
not at callers.

## 2. Exact production file tree

The following tree is authoritative for the implementation plan; no generic
scientific runner is added under CP012.

```text
projects/simulation/explore/coded-decoder-feedback/
  contract.py       # frozen config/types/views/action gate/manifest identities
  waveform.py       # registered prefix/pilots, Gray-16QAM, time/data maps, rotations
  channel.py        # named PCG64 streams, GG/Wiener/AWGN, sole truth-view factory
  receiver.py       # scalar prefix front end, common BPS wrapper, legal 4-state resolve
  codec.py          # P08 LDPC/mapping wrapper, fresh decode, NLL and cost receipts
  methods.py        # B0/B1 deployable paths, controlled fixture, evaluator-only O1
  b2.py             # four-state HMM, exact emissions/LLRs, one-way LDPC
  schemas.py        # strict typed rows/manifests/ledger validation
  freeze.py         # dev selectors and immutable ResolvedDevFreeze load/write boundary
  statistics.py     # deterministic S1/S2/S3 reductions and bootstrap kernels
  artifacts.py      # canonical JSONL, atomic bundle writes, byte hashes, final receipt
  benchmark.py      # ENGINEERING_THROUGHPUT_V1 only; no scientific seed/row/verdict
  verify.py         # S4 evidence/cost/artifact reducer; fail closed, no scientific runner
```

Tests remain exactly the eight files frozen by step 106.  Each test file adds
this D0 root to `sys.path`; production code must not mutate global import paths.

## 3. Public interfaces and ownership boundaries

| File | Required public interface | Ownership / forbidden caller path |
|---|---|---|
| `contract.py` | frozen `D0Contract`, `CodeLayout`, `WaveformLayout`, `ReceiverView`, `TruthView`, `CostLedger`, `ResolvedDevFreeze`; `load_contract(path) -> D0Contract`; `assert_action_authorized(action, contract) -> None` | Leaf module. `ReceiverView` contains only receiver-visible arrays/receipts; no `TruthView`, info/coded bits, true fade/phase, injected label, or physical SNR. CP012 rejects `DEFECT_SMOKE`, S1-S4, C1, MVE and held-out actions. |
| `waveform.py` | `registered_prefix() -> PrefixAsset`; `registered_pilots(N) -> PilotAsset`; `build_waveform(data_symbols, *, N) -> WaveformBuild`; `apply_persistent_rotation(view, *, target_pol, boundary_after_data, k) -> ReceiverView` | May import `contract` and Gray-16QAM numerical mapping. Only integer `k in {0,1,2,3}` and `exp(1j*k*pi/2)`; suffix includes later pilots; copy-on-write and clean polarization byte identity. |
| `channel.py` | `spawn_named_streams(root_seed) -> NamedStreams`; `build_views(contract, waveform, *, root_seed, physical_cell, event_fixture=None) -> tuple[ReceiverView, TruthView]` | Sole factory allowed to observe both physical truth and receiver values. Named spawn order is payload-X, payload-Y, GG, Wiener, AWGN-X, AWGN-Y. No receiver/deployable function may call back into its truth branch. |
| `receiver.py` | `estimate_scalar_frontend(rx_prefix, tx_prefix) -> FrontendEstimate`; `equalize_scalar(rx, estimate) -> np.ndarray`; `run_common_bps(rx, *, B, Nw) -> BpsOutput`; `resolve_global_state(eq, known_symbols, even_mask) -> int`; `estimate_cpost(eq, known_symbols, odd_mask) -> float` | Calls common `bps_cpr(..., mod='qam16')` through a validating wrapper. State uses even known samples; `C_post` uses odd known samples and never feeds the equalizer. No TX bits, true event, `resolve_qam16`, 8-state search, 2x2 LS or physical SNR. |
| `codec.py` | `D0Codec(contract)`; `encode(info_bits) -> coded_bits`; `demap(z, *, complex_noise_power) -> llr`; `decode_fresh(llr_cw, *, cw_ids, candidate_id) -> DecodeBatch`; `reencode_nll(c_hat, llr) -> float` | Wraps P08 mapping and `CodedContractR`/`CodecAdapterR`; validates `[B,1536]`, sign and live interleaver/BG receipt. Every candidate is an empty-state, fixed-20-iteration decode; object/kernel caching is allowed, message-state/warm-start caching is forbidden. |
| `methods.py` | `run_b0(view, codec, freeze) -> MethodOutput`; `run_b1(view, codec, freeze) -> MethodOutput`; `inject_controlled_event(view, fixture) -> ReceiverView`; `evaluate_o1(frozen_receiver_output, truth) -> EvaluationOutput` | B0/B1 accept no truth. B1 evaluates exactly four whole-frame rotations, uses re-encode NLL and low-state tie break. O1 is evaluator-only and is absent from every deployable registry/call graph. |
| `b2.py` | `transition_matrix(p_s, distance) -> np.ndarray`; `pilot_posteriors(view, params) -> PosteriorTrace`; `b2_llr(view, posterior, params) -> np.ndarray`; `run_b2(view, codec, params) -> MethodOutput` | State sum is exact logsumexp, symbol inner metric is P08 max-log with corrected per-real variance, V=0 is an exact Dirac branch, and LDPC is one-way once per polarization. No callback, soft-message reuse or re-decode. |
| `schemas.py` | `validate_row(table, row) -> None`; typed row/manifests for all frozen tables; PK/FK/cardinality/finite checks | Pure validation; extra fields and NaN fail closed. No I/O and no selection. |
| `freeze.py` | `fit_bps_dev(...) -> BpsFreeze`; `fit_b2_statistics_dev(...) -> B2StatisticFreeze`; `fit_b2_tuple_dev(...) -> B2TupleFreeze`; `resolve_dev_freeze(...) -> ResolvedDevFreeze`; `load_resolved_freeze(path) -> ResolvedDevFreeze` | Fit APIs reject all non-dev seeds. Evaluators and benchmark accept only `ResolvedDevFreeze`; they cannot import or reach fit APIs. Freeze stores every candidate key/raw hash, not winner only. |
| `statistics.py` | `reduce_s1(rows)`, `reduce_s2(rows)`, `reduce_s3(rows, freeze)`, `bootstrap_paired(blocks, *, seed=2026081001, draws=10000)` | Pure deterministic reducers. S2 pools within cell then weights three cells equally; S3 fits lambda on dev only. HMM winner aggregation is lossless binary64 integer/power-of-two, never ordinary order-dependent float summation. |
| `artifacts.py` | `canonical_json_bytes(obj) -> bytes`; `write_jsonl_atomic(path, rows, schema) -> ArtifactReceipt`; `write_bundle_atomic(root, files) -> BundleReceipt` | Validate before same-directory temp write; flush, file fsync, replace, directory fsync; receipt lands last and hashes exact bytes. No import-time mkdir. |
| `verify.py` | `collect_s4_evidence(receipts, ledger) -> S4Evidence`; `reduce_s4(evidence) -> EngineeringGate` | Seven independent evidence identities required. Current reducer may report engineering diagnostic only; it cannot emit D0 scientific PASS/KILL, C1 or held-out decisions. |
| `benchmark.py` | `run_engineering_benchmark(contract, freeze, *, root_seed=900000001, watchdog_seconds=720, output) -> BenchmarkReceipt`; `main(argv=None) -> int` | Root seed is outside every scientific/dev range. Exercises four decoder batch sizes, six BPS pairs, ten unique B2 views, one HMM primitive/aggregate and real atomic I/O. It writes no S1-S4 row or scientific verdict and never fits. |

## 4. Dependency DAG and forbidden edges

```text
contract
├── waveform ──┐
│              ├── channel
├── codec      ├── receiver
│              └── methods ──┐
├── schemas ── freeze         ├── verify
│          └── statistics ────┤
└────────────── artifacts ─────┘

waveform + receiver + codec ── methods
waveform + receiver + codec ── b2
all engineering kernels + artifacts + verify ── benchmark
```

Allowed legacy edges are one-way: `codec -> p08_coded_chain/p08r_chain`,
`receiver -> common._recovery.bps_cpr`, and numerical modulation/equalizer
kernels only.  Legacy modules never import D0.  `channel` must not import
`p08r2_chain`; `receiver`, `codec`, `methods`, `b2`, `freeze`, `statistics`,
`verify` and `benchmark` must not import `TruthView`-consuming evaluator code.
There is no `verify -> benchmark`, `benchmark -> fit_*`, or production-module
import of old run/metamorphic scripts.

## 5. Reuse / wrapper / new-code matrix

| Classification | Asset | D0 treatment |
|---|---|---|
| `REUSE_AS_IS` | `qam16_mod`, square-16QAM `hard_decision`, `_build_qam16_constellation`, `maxlog_soft_demap_16qam`, `amp_limit`, `mmse_equalize`, `bps_cpr` numerical kernel | Import behind the owning D0 module; assert exact shapes/dtypes/sign/variance and source receipt. No scientific conclusion is inherited. |
| `WRAP_ONLY` | `CodedContractR`, `CodecAdapterR.encode/decode`, `CalibrationPrefix.symbols`, `estimate_sigma2_from_prefix`, `split_prefix_data`, old source-receipt logic | Add shape, live BG/interleaver, no-state, complex-to-per-real variance, exact prefix divisor, cost and provenance checks. Do not expose the legacy realization object. |
| `DO_NOT_REUSE` | `CodedRealizationR/R2`, `estimate_pre_eq_noise_from_prefix`, P08-R2 equalizer assembly, oracle sigma helpers, `resolve_qam16`, old `save_results`, old run/metamorphic modules | They co-locate truth, assume the rank-deficient 2x2 prefix, leak oracle scale, search illegal states, or have insufficient/import-time I/O semantics. |
| `NEW_D0_CODE` | all `contract` views/types, pilot extension/map, scalar supplied-waveform channel, persistent rotation, B0/B1/O1 semantics, B2 HMM, typed schemas/freezes/reducers, atomic artifacts, S4 reducer and engineering benchmark | Implement only through the RED/GREEN slices below; no common/legacy edits. |

## 6. Atomic TDD slices

| Slice / dependency | RED seam (step-106 IDs) | Minimum GREEN | Independent completion gate |
|---|---|---|---|
| A. Contract/types | none | `contract.py` dataclasses, frozen arrays, action/seed gates and truth denylist only | `test_d0_contract_views.py` CV01-CV09 all green; no I/O/import side effect. |
| B1. Waveform/RNG | A | registered hashes, pilot extension, bijection, named streams and copy-on-write rotation | `test_d0_waveform_channel.py` WC01-WC05/WC08 green. |
| B2. Physical channel | A+B1 | shared GG/Wiener, independent AWGN and deterministic receipts; scalar per-pol model | WC06-WC07 green; old 2x2 LS is unreachable. |
| B3. Receiver/BPS | A+B1 | RSS/31 scalar front end, six-grid wrapper, legal global state, odd-only `C_post` | RM01-RM07 green; no eight-state/TX truth path. |
| C1. Codec | A | Gray mapping, live P08 wrapper, fresh fixed-20 LDPC, corrected demapper and NLL | RM08-RM10 green; order/state-reset receipt and exact BP ledger. |
| C2. Methods | B3+C1 | B0, four-candidate B1 and evaluator-only O1 | RM11-RM12 green; candidate order invariant and O1 absent from Receiver callers. |
| D1. Schemas/statistics | A | strict rows/PK/FK plus S1-S3 pure reducers/bootstrap | SS01-SS11 green. This is schema/reducer engineering, not scientific execution. |
| D2. Freeze | A+D1 | complete dev manifests, exact HMM aggregates, five/five/one selection, immutable receipt | DF01-DF12 green; non-dev refit and evaluator-to-fit call paths fail closed. |
| D3. Artifact/cost/S4 | A+D1 | canonical bytes, atomic bundle, dual cost ledger and seven-evidence reducer | AC01-AC11 green; receipt last and no scientific verdict. |
| E. B2 | A+B1+B3+C1 | corrected transition/emission/posterior/LLR and one-way decode | B201-B212 green including symmetry/Dirac/variance negative controls. |
| F. Integration | C2+D2+D3+E | `verify.py` composition and engineering-only `benchmark.py` manifest/watchdog/projection | AC12 + EB01-EB11 green; all eight test files green; independent code review before any benchmark. |

RED receipts must preserve exact command, test/source SHA, non-zero expected
failure and raw output SHA.  A test edit invalidates its prior RED.  Every
subtask above is capped below 15 minutes: if a file slice approaches the cap,
split at the listed test-ID boundary (one RED/GREEN node or a contiguous group
of at most three pure tests), return the receipt, and resume in a new task.

## 7. Parallel boundaries for the implementation plan

1. A is serial and first.
2. After A, B1, C1 and D1 may run in parallel because they share only frozen
   contract interfaces.  They must write disjoint production/test files.
3. After B1, B2 and B3 may run in parallel; B2 owns `channel.py`, B3 owns
   `receiver.py`.  Neither may change waveform/contract interfaces without
   stopping for reintegration.
4. After B3+C1, C2 and E may run in parallel (`methods.py` versus `b2.py`).
5. After D1, D2 and D3 may run in parallel (`freeze.py` versus
   `artifacts.py`/`verify.py`); the typed schemas are frozen before dispatch.
6. F is serial integration.  An independent reviewer, not an implementer,
   checks truth leakage, decoder state, cache exposure, exact aggregation,
   refit reachability, physical units, rotations, atomic provenance, cost and
   scope.  Only its PASS can unlock the separately authorized engineering
   benchmark; benchmark PASS still cannot unlock science without a new D/V/CP.

## 8. Blockers and bounded debts

| Finding | Status | Bounded treatment / exit evidence |
|---|---|---|
| P08-R2 same-prefix 2x2 LS is rank deficient | Closed architecturally; not a mission blocker | Do not import/call it. Scalar per-pol RSS/31 path must pass RM01-RM03 and source call-graph audit. |
| P08 variance convention can introduce factor-of-two error | Open implementation debt | Single codec conversion `complex_noise_power/2`; RM10 plus B203-B204 must fail the wrong-scale negative control. |
| Common BPS lacks full D0 QAM16 grid proof | Open implementation debt | Validating wrapper and RM04-RM07 over all six pairs, legal rotations and target frame lengths. No common edit. |
| Decoder object/private Sionna metadata may drift | Open environment debt | Lazy Windows-only construction, assert version/device/BG/Z/interleaver and fresh-state behavior; fail rather than silently skip. |
| Lossless HMM aggregation and atomic bundle semantics are new | Open implementation debt | DF04-DF06 and AC02-AC06 provide exact adversarial oracles. |
| Full D0 runtime may exceed seven days | Unresolved engineering risk, not a current hard blocker | Only the separately reviewed 720-second engineering benchmark can project the frozen logical workload. Missing/timeout evidence is INCOMPLETE, not `>7d`. |

No denial condition from T059 is established: every required component has a
named owner file, dependency seam, negative oracle and bounded implementation
slice; B2 remains one-way LDPC; receiver paths do not require truth.

## 9. Environment and protection receipt

The implementation/test environment is Windows Python only:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact-node-or-file>
```

Fresh environment fact inherited from step 106: Python 3.11.9, NumPy 2.4.3,
Torch 2.6.0+cu124, Sionna 2.0.1 and CUDA available.  WSL Python is not used
because its observed environment lacks Sionna.  Future commands must run from
the evidence worktree and census pycache/pytest-cache paths before and after.

This audit wrote only this worker log.  It did not import project code or run
pytest, D0, benchmark or science; it did not modify owner/governance/source/test/
result, `common/`, old P08, protected p05 logs or pycache; it did not commit or
push.

