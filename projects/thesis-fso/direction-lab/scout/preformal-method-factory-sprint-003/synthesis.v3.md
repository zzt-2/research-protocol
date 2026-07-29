# Pre-formal Method Factory Sprint 003 — Synthesis (update-granularity CMA family)

> Schema: `direction-lab.preformal-method-factory-sprint-003.v3`
> Authority: T027 (PREFORMAL_METHOD_FACTORY, epoch 61 / CP025); D035 / V061;
>   V052 REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO (gate-2
>   evidence-grade correction).
> Date: 2026-07-29
> Terminal verdict: **`NO_DIAGNOSTIC_SIGNAL`**
> Claim ceiling: **DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE**
> Artifacts: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`

## 0. TL;DR

This sprint is the **causality test** of the gate-2 SUSPECTED lever (block-end
update granularity), NOT engineering on a confirmed mechanism. The question:
does **finer CMA update granularity** (acting on raw `rX/rY`, producing its own
z) produce a stable, non-artifactual signal **beyond a tuned per-symbol
Godard-with-z CMA** on the CB1 16QAM shared testbed?

In one closed package, four update-granularity constructs were built (TDD:
7/7 gradient-identity + causality + determinism tests PASS first), each acting
directly on raw `rX/rY` and producing its own z-stream (NOT z-only
post-processing of the block-64 output, unlike sprint-001/002 M1-M5). They
were fairly compared against the tuned **per-symbol Godard-with-z** comparator
(canonical gradient, provenance `cb1_cell_runner.py:124-129`) and the inherited
block-64 anchor, on 7 held-out cells × 20 fresh disjoint test seeds, with a
mandatory granularity × effective-update-budget ablation.

**Verdict: `NO_DIAGNOSTIC_SIGNAL`.** No construct stably beats the tuned
per-symbol comparator, AND the comparator does **NOT** remove the block-64
collapse:

- Tuned per-symbol comparator (mu=0.001) seed-cluster mean PI-SER = **0.29685**
  vs inherited block-64 anchor (mu=0.03) = **0.31431** — only marginally better
  (paired Δ = −0.01747, CI [−0.0452, −0.0001], 11 help / 9 hurt seeds).
- The comparator removes the anchor collapse on only **1 of 7** cells
  (snr15-fg1000-long: 0.158 → 0.090). The other 6 collapse cells stay collapsed.
- Best candidate = block8_cma_godard_with_z: paired Δ vs comparator = **−0.00293**
  (CI [−0.0112, +0.0056], 13/7/0) — **fails the MDE = −0.005 threshold**, CI
  crosses 0. Not a signal.
- Ablation: no winner vs comparator, so no granularity-vs-more-updates
  adjudication was triggered; the candidate field is flat around the comparator.

This is **not** `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` (the comparator
did NOT resolve the collapse on 6/7 cells), and **not** a manufactured signal.
The gate-2 SUSPECTED lever (block-end update geometry) is **not confirmed as
the collapse cause**, and finer update granularity does **not** carry a stable
diagnostic signal beyond the tuned traditional comparator on this slice.

## 1. Boundary

Diagnostic-only pre-formal method factory sprint (T027 / D035 / V061). NOT a
Groundwork Step 4a MVE. Did NOT execute/modify T018/Q14, `common/`,
`params.py`, baseline-atlas, B01/B01-R/C11 raw, or any owner/session file. Did
NOT push. Did NOT use forbidden seeds 71-80. Claim ceiling = DIAGNOSTIC_ONLY.

### 1.1 Gate-2 evidence-grade correction (MANDATORY)

Sprint-001 synthesis §4/§8 attributed the collapse to a "block-end update
geometry + channel time-variation structural attractor" and listed it as a
SUSPECTED bottleneck. **V052 REJECTED that broad causal attribution**
(`REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO`: no basin scan,
overlap with existing candidates). The correct statement used here: block-end
update granularity is a **source-backed, SUSPECTED lever** (a real code-imposed
knob at `cb1_cell_runner.py:106-129` / `_cma.py:100-166`), coincident with the
observed failure location. This sprint is the causality test — it does NOT
assume the lever is the confirmed cause.

## 2. Phase A — Testbed identity gates (all PASS)

| Gate | Property | Result |
|---|---|---|
| qpsk_regression | QPSK PI-SER = 0.0 at inherited mu=0.03 | **PASS** (0.000000) |
| eval_population_identity | all methods finite z on held-out cell/seed | **PASS** |
| prefix_only_freeze_invariance | re-run on same raw → bit-identical z (deterministic) | **PASS** |
| gradient_identity | comparator + all candidates stamp `Godard-with-z` | **PASS** |

The inherited block-64 anchor (`cb1_cell_runner.standard_cma_godard_with_z`,
mu=0.03) is byte-identical to the B01-R hotfix v2 anchor; mu is FROZEN from
`frozen-params-b01r-v1.yaml` (NOT re-tuned here, NOT reverted to 0.001). TDD
gate-4 (`test_persymbol_gradient_is_godard_with_z`) proves the per-symbol
update vector equals `mu·(R²-|z|²)·z·conj(r)` (CONTAINS the z factor) and is
NOT the scalar-error form — guarding against `EXECUTION_INVALID`.

## 3. Phase B — Constructs built (5, mechanism-distinct; all own-z)

| ID | update granularity | updates/sym | dev-frozen mu | role |
|----|---|---|---|---|
| block64_cma_mu0p03 | block_end_averaged (64) | 0.0156 | 0.03 (inherited) | anchor / identity ref |
| persymbol_cma_godard_with_z | per_symbol_immediate | 1.0 | 0.001 | **traditional comparator** |
| block8_cma_godard_with_z | block_end_averaged (8) | 0.125 | 0.003 | candidate |
| block16_cma_godard_with_z | block_end_averaged (16) | 0.0625 | 0.003 | candidate |
| sliding_window_recursive_cma | per_symbol + recursive memory | 1.0 | 0.0003 (lam=0.9) | candidate |

All share the canonical Godard-with-z gradient identity `dw ∝ (R²-|z|²)·z·r*`
(provenance `cb1_cell_runner.py:124-129`). The comparator is the per-symbol
analogue of that formula (drops the block `mean`, applies immediately each
symbol). The forbidden scalar-error `_cma.py CMAEqualizer2x2` (missing z) was
NOT used. Smoke (Phase B) confirms each construct produces its own z distinct
from the anchor z, stamps Godard-with-z, and is deterministic.

## 4. Phase C1 — dev freeze (comparator mu tuned fairly)

Comparator mu was tuned on a dev pool (3 short cells × 3 dev seeds, prefix-only)
over {1e-3, 3e-3, 1e-2, 3e-2, 1e-1}:

| mu | dev mean PI-SER (n finite) |
|---|---|
| 1e-3 | 0.3125 (9) ← frozen |
| 3e-3 | 0.3392 (6) |
| 1e-2 | 0.6569 (6) |
| 3e-2 | 0.7070 (2) |
| 1e-1 | diverged (0) |

mu=0.001 is the dev-optimal AND the largest stable value; larger mu diverges on
the long cells (each per-symbol update is full-strength, no block-mean
attenuation, so the stable per-symbol mu is ~30x smaller than the block-end
mu). A separate test-side check confirmed mu=0.003 diverges on 2/3 of the long
test cells — so mu=0.001 is **not an under-fit artifact**; it is the best
stable per-symbol Godard-with-z CMA on this testbed. Candidates were tuned
analogously (block8/16 mu=0.003; recursive mu=0.0003, lam=0.9).

## 5. Phase C2 — comparator-aware fair comparison (seed-cluster, 7 cells × 20 test seeds)

Reference for the signal gate = the **tuned per-symbol comparator** (NOT the
anchor). Anchor deltas shown for context. MDE = 0.005, 10k cluster-bootstrap,
95% CI.

| construct | ref | seed-cluster mean ΔPI-SER | 95% CI | help/hurt/tie | healthy-worst Δ | gate |
|---|---|---|---|---|---|---|
| persymbol_cma (comparator) | block64 anchor | **−0.01747** | [−0.0452, −0.0001] | 11/9/0 | +0.0469 | COMPARATOR_CONTEXT |
| block8 | comparator | −0.00293 | [−0.0112, +0.0056] | 13/7/0 | +0.0781 | NO_SIGNAL |
| block16 | comparator | +0.00313 | [−0.0068, +0.0135] | 11/9/0 | +0.1133 | NO_SIGNAL |
| sliding_window_recursive | comparator | −0.00103 | [−0.0099, +0.0082] | 12/8/0 | +0.1016 | NO_SIGNAL |

No candidate reaches the MDE = −0.005 threshold vs the comparator; all CIs
cross 0. The comparator itself is only marginally better than the anchor (CI
upper just below 0). All candidates also show healthy-cluster regression
(worst Δ up to +0.11 on healthy cells), so even the directional hints are
unsafe to deploy.

## 6. Why the winner doesn't win / losers don't lose

There is no winner. The mechanism story is uniform and flat:

- **block8** (best candidate, Δ=−0.0029) has 8x more updates/symbol than
  block-64 but the SAME block-end averaged gradient. Its tiny directional edge
  is within noise (CI crosses 0) and below MDE. More updates per se do not
  convert into a granularity signal here.
- **block16** (Δ=+0.0031) is slightly WORSE than the comparator — intermediate
  granularity buys nothing.
- **sliding_window_recursive** (Δ=−0.0010) has the same per-symbol update rate
  as the comparator plus recursive memory; the memory smoothing does not help
  (within noise).
- **The comparator vs anchor** (−0.0175): per-symbol tracking of the
  time-varying channel gives a small, barely-significant edge over block-64,
  but it is NOT a candidate signal (the comparator beating the anchor is
  context, not a new-construct win), and it does NOT remove the collapse.

The flatness around the comparator across very different granularities
(block-8 averaged, block-16 averaged, per-symbol instantaneous, per-symbol +
recursive memory) is itself the finding: on this slice, update granularity is
**not** a productive lever beyond the tuned traditional per-symbol CMA.

## 7. Ablation — granularity vs more-updates vs tuning

No candidate crossed the MDE threshold vs the comparator, so there is no
"winner" to adjudicate. The ablation records the effective-update-budget
fingerprint (updates/sym: block64=0.0156, block16=0.0625, block8=0.125,
per-symbol=1.0, recursive=1.0) and confirms `win_explanation =
no_winner_vs_comparator`. Because the candidate field is flat around the
comparator despite spanning 0.0156 → 1.0 updates/sym, neither "more updates"
nor "granularity" produces a separable advantage — the three explanations
collapse to "no effect at this granularity range." (Had a candidate won, a
matched-budget block-64 mu sweep would have run to separate more-updates from
granularity; it was not triggered.)

## 8. Does the tuned per-symbol comparator already resolve the collapse? — NO

This is the decisive distinction from `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`.

| cell | anchor PI-SER | comparator PI-SER | collapse removed? |
|---|---|---|---|
| snr05-nominal-short | 0.5945 | 0.6061 | no (worse) |
| snr10-nominal-short | 0.3828 | 0.3809 | no |
| snr15-nominal-short | 0.2732 | 0.2652 | no |
| snr25-nominal-short | 0.2252 | 0.2203 | no |
| snr20-fg100-short | 0.2396 | 0.2320 | no |
| snr10-fg100-long | 0.3271 | 0.2830 | no |
| snr15-fg1000-long | 0.1576 | 0.0904 | **yes** (1/7) |

The block-64 anchor collapses on all 7 cells (PI-SER ≥ 0.1). The tuned
per-symbol Godard-with-z comparator removes the collapse on only **1 of 7**
(snr15-fg1000-long). On the other 6 it is statistically indistinguishable from
the anchor. Therefore the collapse is **not** resolved by the conventional
finer-granularity comparator, which is exactly why the verdict is
`NO_DIAGNOSTIC_SIGNAL` and not `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`.

This is also the causal read on the gate-2 SUSPECTED lever: block-end update
granularity is **not** confirmed as the dominant collapse cause — moving to
per-symbol updates does not systematically fix it. The collapse is driven by
something the CMA update granularity does not address on this slice (consistent
with the channel being memoryless/flat except for SOP rotation + GG amplitude +
AWGN, where the residual error is closer to AWGN/SOP-tracking than to an
equalizer-convergence artifact).

## 9. Acceptance check (vs T027 §4)

- [x] action_class = PREFORMAL_METHOD_FACTORY (epoch 61 / CP025); diagnostic-only.
- [x] inherited anchor = corrected mu=0.03 block-end Godard-with-z CMA; no mu=0.001 revert.
- [x] ≥3 constructs ran (anchor + tuned per-symbol comparator + 3 candidates), all prefix-only causal (TDD 7/7 PASS).
- [x] comparator = tuned per-symbol Godard-with-z CMA, provenance `cb1_cell_runner.py:124-129` (canonical, contains z); mu dev-tuned. Scalar-error `_cma.py` NOT used.
- [x] block_size × mu / effective-update-budget ablation done; no winner → no artifact to rule out (field flat).
- [x] seed-cluster aggregation; smoke in terminal result (NOT clobbered); raw→aggregate reproducible (840 raw rows).
- [x] terminal verdict ∈ the 5 allowed; comparator-aware mechanism explanation present.
- [x] no `common/`/`params.py`/baseline-atlas/B01/B01-R/C11/owner/session edits; no push; no forbidden seeds; method-map dedups vs §3.1 rejected frequency-domain family.

## 10. Caveats

1. The per-symbol mu is necessarily small (0.001) because each update is
   full-strength; this is the canonical per-symbol regime, not a tuning defect
   (verified: larger mu diverges on long cells). The comparator is fairly tuned.
2. The candidate field spans 0.0156 → 1.0 updates/sym but is flat around the
   comparator; we did not test even finer mechanisms (e.g. event/innovation-
   triggered immediate update) — those remain untested, but the flatness
   across block/per-symbol/recursive suggests diminishing returns.
3. This is a single slice (CB1 16QAM, 7 cells). The "granularity is not a
   productive lever" read is slice-scoped; it is NOT a general claim about CMA
   update granularity.
4. The collapse is AWGN/SOP-dominated on most cells (oracle-affine labelling,
   offline only): finer equalizer granularity would not be expected to fix
   AWGN-dominated error, which is consistent with the flat result.

## 11. Terminal verdict

**`NO_DIAGNOSTIC_SIGNAL`** — no update-granularity construct stably beats the
tuned per-symbol Godard-with-z conventional comparator, and the comparator did
NOT remove the block-64 collapse (1/7 cells). The gate-2 SUSPECTED lever
(block-end update geometry) is not confirmed as the collapse cause; finer
update granularity carries no stable diagnostic signal beyond the tuned
traditional comparator on this slice. Not a carrier; no formal MVE, no paper
claim, no auto-promotion.
