# Q001 Defect-Only Smoke Design

> Groundwork Step 4a / D007 | approved scope: defect smoke only

## Goal and claim ceiling

Test only whether Wang-style branch-local synchronization/phase correction followed by estimated-channel MRC has a naturally occurring invalid-branch problem that survives tuned fixed SNR discard and SC/GSC. No soft reliability, abstention method, novelty conclusion, Go, Contract entry, or fair method comparison is implemented.

The maximum positive terminal is `DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT`, which restores only `PROBLEM_BEARING_CANDIDATE_WITH_NOVELTY_DEBT`. Sun/Xie/Qiu exact-action debt remains unchanged.

## Why the historical b3 path is not reused end-to-end

Fresh baseline execution reproducibly fails its own BER gate (`m1≈0.4296`, `m2/full≈0.4300`, required `<0.3`). Caller tracing also found: truth `h_branches` enters MRC; Gamma-Gamma draws bypass the per-realization RNG; offsets are metadata but are not applied; the FSTS template is not inserted into TX; the MRC formula consumes intensity as if it were a complex coefficient and behaves like deep-fade-amplifying ZF. The historical files remain unchanged. Only the FSTS structure, project parameter sources, and QPSK mapping are reused as references in a new isolated sandbox.

## Frozen scientific chain

1. `generate_realization(seed, cell)` creates one shared multi-branch receiver frame and a separate truth record. It inserts a 320-symbol known FSTS, periodic known QPSK pilots, payload, physical branch offsets, independent Gamma-Gamma irradiance and AWGN, branch-static phase, and a shared Wiener phase process. No explicit invalid/slip event is injected in primary runs.
2. `estimate_branches(receiver_frame)` uses only samples and known training/pilots. It estimates FS offset, normalized FS peak and a guarded peak margin defined as `winner − max(score outside winner±1 offset)`, complex pilot-LS gain, pilot residual/noise, estimated SNR, and pilot phase coherence. Known periodic pilots provide a branch-local interpolated phase correction before combining; the estimator returns those corrected raw branch payloads and receiver estimates.
3. `combine_subset(estimates, subset)` computes equal-noise estimated-channel MRC:

   `s_hat = sum(conj(g_hat_k) * r_k) / (sum(abs(g_hat_k)**2) + eps)`.

   There is no second post-combine phase interpolation: the only phase correction is receiver-visible and branch-local before MRC. Payload truth is never used inside this function.
4. Arms operate on the same estimates:
   - B0: all branches.
   - B1: branches with `snr_hat_db >= tau`, with `tau` selected on dev from the frozen grid.
   - B2: top-`L(K)` branches by `snr_hat_db`, including SC at `L=1`; `L(K)` is selected on dev.
   - O1: evaluator enumerates non-empty subsets and chooses minimum payload BER. Truth is used only after every deployable arm output exists.
   - D: dev-fitted diagnostic logistic score predicts O1 inclusion from receiver-visible features. It never emits an action.
5. `evaluate_realization` writes normalized long rows containing seed, cell, frame, branch, method, inclusion, fixed pre-FEC payload BER, outage, receiver features, truth-only labels and paired-realization hash.
6. `aggregate_from_raw` is the only headline-number path. It clusters by seed and reports deterministic bootstrap confidence intervals.

## Information firewall

`ReceiverFrame` contains only `branches`, known FSTS/pilot locations and values, payload positions, and sample period. `TruthRecord` contains payload bits/symbols, true branch gains/offsets/phase/SNR/turbulence and is accepted only by the evaluator. B0/B1/B2 signatures cannot accept `TruthRecord`.

Runtime metamorphic gate: generate one realization; keep `ReceiverFrame` fixed and replace every truth field. B0/B1/B2 selected subsets, no-valid flags and complex outputs must remain bit/float exact. A second gate permutes payload truth while receiver samples stay fixed; deployable outputs and features must remain exact.

## Physical grid and provenance

Primary grid has 18 cells: `3 GG × 2 branch counts × 3 heterogeneity settings`.

| Parameter | Frozen value | Provenance / limitation |
|---|---|---|
| modulation / symbol rate | single-pol QPSK proxy, 10 GBd | Wang 2023 uses PM-4/16QAM at 10 GBd; single-pol is an MVE simplification |
| FSTS | 320 symbols, `BN=16`, `BL=20` | Wang 2023 content lines 257–267, 289–299 |
| pilots | one known QPSK pilot every 100 payload symbols | Johst 2024 lines 95–98, 114–116; hybrid receiver-visible diagnostic, not a Wang reproduction |
| linewidth | 50 kHz shared Wiener phase | Wang 2023 lines 231–243 |
| GG | weak `(11.6,10.1)`, moderate `(4.0,1.9)`, strong `(4.2,1.4)` | current `params.py` truth source; formulas-master contains conflicting older triples, so this is `UNVERIFIED_RANGE` and all three are scanned |
| branches | 2 and 4 | Wang scans 1/2/4/6 branches |
| heterogeneity | H0 `[0,0]`; H1 `[0,-1]`; H2 `[0,-6]` dB signal-power offsets, implemented as deterministic gain factors `10^(offset_dB/20)` and replicated by half for K=4 | All branches use the same complex AWGN variance `E[|n|²]=1` (I/Q variance 0.5); Johst anchors reliable around 0 dB, outage boundary near −1 dB, and high outage around −6 dB; multi-branch construction is `UNVERIFIED_RANGE` |
| offsets | integer 0–7 symbols, independently drawn | MVE search-window range; `UNVERIFIED_RANGE`; scanned symmetrically and not conditioned on outcome |
| payload | 30,720 symbols per seed/cell before pilot exclusion | Johst uses 500k-sample bursts; value is a bounded MVE precision choice, fixed before test |
| dev/test seeds | dev `0..19`; test `10000..10099` | disjoint, frozen before held-out |

No parameter is selected after viewing held-out results. Stress-only injected slips, if ever added, must be separately labeled and cannot enter G1–G4.

## Metric signatures

- `pre_fec_ber_fixed`: payload bit errors / fixed payload-bit denominator; FSTS and pilots excluded; no trial is dropped.
- `outage`: `pre_fec_ber_fixed > 0.02` (Johst SD-FEC operating threshold). Branch DSP-invalid label is `FS offset wrong OR individual branch BER >= 0.44`, following Johst's outage diagnostic.
- `high_power_invalid`: B1 would include the branch under dev-frozen `tau`, but the truth-only DSP-invalid label is true.
- `relative_regret(method,O1) = (BER_method - BER_O1) / max(BER_method, 1/N_payload_bits)`. Primary G2/G3 estimands are evaluated on frames containing at least one `high_power_invalid` branch.
- Power-only and multi-source AUC use held-out O1 subset inclusion labels; diagnostic coefficients and normalization are learned on dev only.

## Frozen gates

- G1 occurrence: event rate `>=0.10` and at least three physical cells with at least one event.
- G2 damage: B0 paired relative BER regret `>=0.10` or outage excess `>=0.05`, with seed-cluster CI lower bound `>0`.
- G3 cheap residual: dev-selected strongest of B1/B2 has relative BER regret `>=0.05` or outage excess `>=0.02`, with seed-cluster CI lower bound `>0`.
- G4 observability: multi-source held-out AUC `>=0.65`, AUC delta over power-only `>=0.05`, AUC CI lower bound `>0.50`, and delta CI lower bound `>0`.

Fail-stop terminals: G1 or G2 failure → `PROBLEM_ABSENT_OR_TOO_SMALL`; G3 failure → `PROBLEM_RESOLVED_BY_CONVENTIONAL_RULE`; G4 failure → `DEFECT_NOT_RECEIVER_OBSERVABLE`; all pass → `DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT`.

## State and reproducibility

Each `(seed, cell)` creates one realization. `SeedSequence` spawns payload, common phase, and per-branch gain/noise/offset streams. All methods consume the same receiver object; method order is immaterial. State resets per realization. Dev and test never share seeds. The freeze receipt hashes the design, source, tests, dev raw/aggregate, selected thresholds, diagnostic coefficients, grid, seeds and MDEs with `test_started=false`; its commit precedes any held-out execution.
