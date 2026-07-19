# Headroom Atlas Stage A Synthesis — P03/U19 baseline-only multi-domain

> Run date: 2026-07-19
> Stage: A (baseline-only Scout diagnostic; **no ML trained**, no B004, no Queue/Registry, no paper claim)
> Closure artifact: `stage-a-atlas.json` (machine-readable) + this synthesis (human-readable)
> Gate: `headroom-atlas/atlas_gate.py` (the unique Atlas entrypoint; receipt-bound, append-only audit)
> Frozen source closure: P03 v1 source-equivalence contract (`source-equivalence-contract.v1.yaml`) → simulation commit `65db35bb` + run_b001 SHA `26a0e95d…`

## What the Stage A Atlas set out to answer

After the P03 v1 claim-scope correction (S076/D058), the exact QPSK / 20 dB / CSI_NONE / short-sequence slice was adjudicated as `LOCAL_NEGATIVE` only: it could not close DOMAIN/CANDIDATE/FAMILY. The Atlas re-asks the original question across a representative sub-domain:

> On the runnable representative domain of the dual-pol OSL Scout, **does the strongest legal non-ML receiver (standard-CMA Godard-with-z + nearest-QPSK) retain measurable decision headroom**, where "measurable" means above a pre-registered minimum detectable effect?

The strongest legal non-ML comparator set is exactly the one registered for the P03 v1 probe (nearest-QPSK control, same-information blind one-step complex 2×2 affine, and a scoring-only oracle affine upper bound). No stronger comparator and no learned detector were introduced.

## Representative axes — what ran and what was blocked

| axis | in-closure levels | blocked | reason |
|---|---|---|---|
| `modulation_order` | QPSK | **16QAM** | the frozen P03 source closure's channel generator (`common/_dual_pol_channel.py`, SHA-pinned by the source-equivalence contract) hard-codes QPSK. 16QAM gen/eval assets exist in separate unfrozen historical explore scripts (`ber_16qam_vs_fg.py`, `sup_stress_test.py`) but are not hash-bound into the closure; importing them would either mutate the canonical baseline source (forbidden by `anchor.yaml::canonical_baseline.mutable=false`) or require a new source closure (large rebuild of the common simulator). Per the task brief this blocks the 16QAM axis, **not** the candidate. |
| `SNR_or_operating_region` | 5 / 10 / 15 / 20 / 25 dB | — | spans low / waterfall-transition / high |
| `channel_or_state_dynamics` | f_G ∈ {30, 100, 1000} Hz, SOP ∈ {4e-6, 4e-5} | — | slow / nominal / fast turbulence + a 10× faster SOP point |
| `observation_length` | short interface window (512) + long tracking window (8192) | — | long window exposes late-slice SOP accumulation (historical D015/D022 axis) |
| `CSI_or_pilot_access` | CSI_NONE | **receiver-estimated CSI**, **explicit pilot budget** | closure exposes only the CSI_NONE z-window adapter; receiver-estimated CSI needs a new estimator seam; pilot injection seam is partial (E pilot family S061) and not hash-bound |
| `task_output` | uncoded hard decision | **soft information / coded metric (LLR/GMI/FER)** | frozen evaluator is hard-decision QPSK only; coded metrics need a legal CSI contract and same-information coded comparator the closure does not expose (`HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH` counterexample remains open) |

**Design rule applied**: staged representative coverage (covering-array-with-anchors) over the runnable axes, anchored on the P03 v1 cell. 11 cells × 10 paired seeds (seeds 11–20, the same paired seeds as P03 v1). NOT an exhaustive full-factorial grid.

## Statistical sensitivity (pre-registered)

- primary metric: PI-SER (permutation-invariant symbol error rate); fixed-label SER reported alongside as the swap-aware complement
- minimum detectable effect (MDE): **0.005 per-symbol** (0.5 pp). Rationale: below this, a learned residual-aware detector's training/evaluation budget cannot distinguish a real mechanism from implementation noise.
- zero-error confidence: rule-of-three one-sided 95% upper bound `1 − 0.05^(1/n)` over the n paired seeds.
- sequential sampling budget: 10 → 40 paired seeds; INSUFFICIENT_SENSITIVITY fallback if every cell stays zero-error with rule-of-three UB > MDE.

## Per-cell verdicts (10 paired seeds each)

| cell_id | modulation | SNR (dB) | f_G (Hz) | SOP rate | N | status | decision_class | visible headroom | nearest PI-SER | oracle PI-SER | n error events |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qpsk-snr05-nominal-short | QPSK | 5 | 30 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.19805 | 0.19922 | 18 |
| qpsk-snr10-nominal-short | QPSK | 10 | 30 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.04531 | 0.04961 | 16 |
| qpsk-snr15-nominal-short | QPSK | 15 | 30 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00430 | 0.00430 | 4 |
| qpsk-snr20-nominal-short (P03 v1 anchor) | QPSK | 20 | 30 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |
| qpsk-snr25-nominal-short | QPSK | 25 | 30 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |
| qpsk-snr20-fg100-short | QPSK | 20 | 100 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |
| qpsk-snr20-fg1000-short | QPSK | 20 | 1000 | 4e-6 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |
| qpsk-snr20-sop40e-short | QPSK | 20 | 30 | 4e-5 | 512 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |
| qpsk-snr10-fg100-long | QPSK | 10 | 100 | 4e-6 | 8192 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.05039 | 0.05312 | 14 |
| qpsk-snr15-fg1000-long | QPSK | 15 | 1000 | 4e-6 | 8192 | SUB_MDE_HEADROOM | NON_DECISIVE | 0.00039 | 0.00703 | 0.00664 | 4 |
| qpsk-snr20-nominal-long | QPSK | 20 | 30 | 4e-6 | 8192 | NO_VISIBLE_HEADROOM | LOCAL_NEGATIVE | 0.00000 | 0.00000 | 0.00000 | 0 |

## Verdict ladder

| level | status | decision_class | basis |
|---|---|---|---|
| CELL | mixed (see table) | LOCAL_NEGATIVE / NON_DECISIVE | 10/11 cells `NO_VISIBLE_HEADROOM`; 1/11 (`qpsk-snr15-fg1000-long`) `SUB_MDE_HEADROOM` with visible headroom 0.00039 ≈ 13× below MDE |
| SLICE | LOCAL_NEGATIVE | LOCAL_NEGATIVE | every runnable (modulation × SNR × dynamics × length × CSI_NONE × hard-decision) slice is at-or-below MDE for the strongest legal non-ML baseline |
| DOMAIN | UNRESOLVED | NON_DECISIVE | runnable sub-domain is LOCAL_NEGATIVE, but 3 axes (16QAM, receiver-estimated CSI, coded metrics) are INFRASTRUCTURE_BLOCKED and the historical counterexamples (`MODULATION_DYNAMICS_LENGTH_ORDERING_SIGNAL`, `HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH`) live on exactly those blocked axes |
| CANDIDATE | OPEN | NON_DECISIVE | no scope certificate; representative-domain coverage is incomplete |
| FAMILY | OPEN | NON_DECISIVE | no mechanism proof |

## Stage A exit

**`NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`** at the runnable representative sub-domain level.

- 0/11 cells above MDE → no Stage B confirmation is triggered. Per the task brief, Stage B is only for cells that found a headroom region; there is no region here.
- max visible headroom across all cells = 0.00039 (the f_G=1000 / long / SNR-15 cell), which is ~13× below the pre-registered MDE.
- 6/11 cells are sensitivity-limited (zero errors with rule-of-three UB > MDE on 10 seeds): all four SNR-20 short variants, plus SNR-25 short and SNR-20 long. On those cells we cannot rule out an MDE-level effect; the LOCAL_NEGATIVE claim is "no observed headroom", not "baseline perfect".
- 4/11 cells are measured-negative (non-zero errors, oracle affine does not beat nearest-QPSK on PI-SER): SNR-5/10/15 short and SNR-10 f_G=100 long. These are the waterfall / low-SNR region where the historical ordering-signal counterexample lived; in this runnable closure the strongest legal non-ML comparator still does not produce measurable headroom.

## Reading the result honestly

- This Stage A finding **extends** P03 v1's exact-slice LOCAL_NEGATIVE to a wider runnable sub-domain (QPSK × SNR sweep × dynamics sweep × short/long observation × CSI_NONE × uncoded hard decision), using the same source closure and the same strongest-legal comparators.
- It does **not** close DOMAIN/CANDIDATE/FAMILY: the historical counterexamples that force DOMAIN-level UNRESOLVED live on exactly the axes the frozen closure cannot exercise (16QAM ordering changes per D008–D014/D023; long-sequence fixed-label BER swap per D015; coded/LLR per U20). Those axes are INFRASTRUCTURE_BLOCKED here, not measured-negative.
- The 6 sensitivity-limited cells mean that on the high-SNR / fast-dynamics cells, 10 paired seeds cannot resolve an MDE-level effect. A Stage A′ extension could double the seed budget to 40 (pre-registered sequential cap), but it cannot unlock the blocked axes.
- No headroom region was found, so **no Stage B is triggered** and **no ML training is authorized**.

## Secondary findings

- **Local negatives (carry forward as LOCAL_NEGATIVE priors for adjacent candidates)**:
  - waterfall/low-SNR QPSK CSI_NONE hard-decision (SNR 5/10/15 dB, short and long): strongest legal non-ML baseline already at-or-near oracle on PI-SER
  - SNR-20/high-SNR QPSK across all dynamics (f_G 30/100/1000, SOP 4e-6/4e-5): zero observed errors at 10 seeds
- **Baseline boundary**: standard-CMA (Godard-with-z) + nearest-QPSK is the strongest legal non-ML receiver on this closure. The same-information blind affine comparator did not beat it on any cell (in several low-SNR cells the affine was slightly worse, because the calibration-z pseudo-labels are themselves noisy at low SNR). This is a baseline-dominance boundary, not a bug.
- **Infrastructure gaps (axis-level blocks, not candidate failures)**:
  - 16QAM: needs either a new source closure or a careful, hash-bound adapter; the historical `ber_16qam_vs_fg.py`/`sup_stress_test.py` assets exist but are not closure-bound
  - receiver-estimated CSI / explicit pilot: needs a new estimator seam (pilot injection is partial per E pilot family S061)
  - soft/coded output (LLR/GMI/FER): needs a legal CSI contract and a same-information coded comparator; `HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH` counterexample remains open
- **Reusable runner / adapter assets**:
  - `headroom-atlas/atlas_gate.py` — the unique receipt-bound Atlas entrypoint, with 19 passing tests (11 functional + 8 adversarial, including cross-type token misuse, schema tampering, hand-edited receipt_id, foreign-workspace token, append-only preservation)
  - `headroom-atlas/stage_a_cell_runner.py` — closure-bound, parameterized over SNR/dynamics/length; reproduces the P03 v1 anchor cell exactly (eval_start=133, calibration_end=261, eval_end=389)
  - `headroom-atlas/run_stage_a.py` — gated driver; emits the machine-readable Atlas + summary
  - `headroom-atlas/stage-a-contract.v1.yaml` — pre-registered contract (axes, MDE, paired seeds, comparator set, verdict schema, exits)
  - `headroom-atlas/atlas-pre-run-assessment.v1.yaml` + receipt — the assessment snapshot the gate binds at authorize-time
- **Implications for adjacent candidates (U20 / U36)**:
  - **U20 (coded LLR)**: Stage A supplies a hard-decision LOCAL_NEGATIVE prior only, not permission to start U20; the coded path remains INFRASTRUCTURE_BLOCKED on this closure
  - **U36 (residual-aware evidence)**: same evidence as P03's exact slice is now extended to a runnable sub-domain; U36 is not globally rejected but the runnable sub-domain has no measurable headroom

## Next legal step

Three honest options (only the first is in-scope for this run; the others are user decisions):

1. **P03 stays UNRESOLVED at the runnable representative sub-domain; return to candidate pool.** Stage A produced a representative-domain LOCAL_NEGATIVE with three INFRASTRUCTURE_BLOCKED axes. A CANDIDATE-level retirement would require (a) building the missing closures (16QAM / receiver-CSI / coded output) and (b) a scope certificate disposing of the historical counterexamples — both are larger infrastructure investments, not Scout work.
2. **Build one of the missing closures** (most leveraged: 16QAM, because D008–D014/D023 explicitly show modulation-driven ordering changes) and re-run Stage A on the expanded domain.
3. **Move to a different candidate family** (e.g. U36 with a different mechanism) rather than continuing to invest in residual-aware detection.

Stage B is **not** triggered because no headroom region was found.
