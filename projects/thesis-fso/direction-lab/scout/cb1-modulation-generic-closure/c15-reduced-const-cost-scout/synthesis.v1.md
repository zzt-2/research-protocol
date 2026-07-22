# C15 Reduced-Constellation / Ring-Aware Cost Scout — Synthesis v1

**Candidate:** C15 (reduced_constellation_ring_aware_cost)
**Batch:** c15-reduced-const-cost-scout v1
**Mechanism / metric:** COST-FUNCTION (equalizer) / PI-SER (hard-decision) + collapse_rate.
  This is the FIRST candidate to change the EQUALIZER COST FUNCTION itself.
  Every prior candidate (C04/C09/C11/C12 post-equalizer; C08 adaptive-mu same
  cost; MMA D006/D040 quadrant-aware) left the Godard cost untouched.
**Claim ceiling:** LOCAL_SLICE / DIAGNOSTIC
**Status:** EXECUTED (11 cells × 10 seeds × 3 costs, 4.6 s total wall time)
**Verdict:** **C15_RING_AWARE_DOES_NOT_REDUCE_COLLAPSE** (LOCAL_NEGATIVE). The
  ring-aware cost does not reduce collapse — it **INCREASES** it, and worsens
  PI-SER. This STRENGTHENS the "deep Godard-cost property" thesis.

---

## 1. Scientific question

The 16QAM inner-ring collapse has been attributed (baseline Atlas synthesis
§6; C12 synthesis §6) to a **deep property of the Godard cost** on this
channel: the single-global-R² modulus cost `e = R² − |z|²` is mismatched to
16QAM's three rings (squared radii 0.2 / 1.0 / 1.8), pulling every symbol
toward one circle. **Does a ring-aware cost that assigns each symbol to its
nearest ring** (`R²(z) = nearest-ring squared radius, from |z| alone`)
**eliminate or reduce the collapse**? Secondary: does reduced-constellation
CMA (RCCMA, outer-ring-only, Sato 1975 style) do the same?

This is mechanism-distinct from MMA (Yang-Werner-Dumont, tested D006/D040,
FAILED): MMA decomposes 16QAM by **quadrant** (angle); C15 decomposes by
**ring** (radius). MMA rotates the constellation; C15 does modulus matching.

## 2. Semantic smoke — PASS (all 3 frozen checks)

| check | result |
|---|---|
| Godard reproduces collapse (snr20, seed 71) | collapsed=**True**, E\|z\|²=0.294 ✓ |
| ring-aware does not diverge on clean (snr25, seed 71) | div=**False** ✓ |
| ring-aware PI-SER < random ceiling 0.9375 on clean | **0.7305** ✓ |

**Note (diagnostic, not a gate failure):** seed 71 collapses under Godard on
*every* SNR cell tested (snr20 AND snr25), so there is no "clean seed 71"
— the collapse is seed-driven, not SNR-driven. The smoke still passes because
ring-aware is finite and below the random ceiling. The ring-aware cost is
numerically well-defined and converges (the cost surface is bounded); the
question is whether it *rescues* collapse.

## 3. Results — collapse_rate and PI-SER (mean over 10 seeds)

| cell | GOD col | RA col | RC col | GOD pi | RA pi | RC pi |
|---|---|---|---|---|---|---|
| snr05-nominal-short   | 0.00 | 0.00 | 0.00 | 0.586 | 0.582 | 0.604 |
| snr10-nominal-short   | 0.20 | 0.20 | 0.20 | 0.316 | 0.321 | 0.322 |
| snr15-nominal-short   | 0.20 | 0.20 | 0.20 | 0.176 | 0.180 | 0.181 |
| snr20-nominal-short   | 0.20 | 0.20 | 0.20 | 0.153 | 0.153 | 0.153 |
| snr25-nominal-short   | 0.20 | 0.20 | 0.20 | 0.148 | 0.148 | 0.148 |
| snr20-fg100-short     | 0.20 | 0.20 | 0.20 | 0.153 | 0.153 | 0.153 |
| snr20-fg1000-short    | 0.20 | 0.20 | 0.20 | 0.153 | 0.153 | 0.153 |
| snr20-sop40e-short    | 0.20 | 0.20 | 0.20 | 0.153 | 0.153 | 0.153 |
| snr10-fg100-long      | 0.10 | **0.30** | 0.20 | 0.429 | **0.547** | **0.636** |
| snr15-fg1000-long     | 0.10 | **0.30** | **0.40** | 0.261 | **0.379** | **0.456** |
| snr20-nominal-long    | 0.30 | 0.30 | 0.30 | 0.230 | **0.350** | **0.439** |

(GOD=Godard anchor, RA=ring-aware, RC=RCCMA. col = collapse_rate per cell.)

## 4. Macro adjudication (paired bootstrap, 110 cell×seed points)

| statistic | value | 95% CI | frac < 0 (candidate better) |
|---|---|---|---|
| **ring_aware Δcollapse vs godard** | **+0.0364** | **[+0.0091, +0.0727]** | **0.00** |
| **ring_aware Δpi_ser vs godard** | **+0.0329** | **[+0.0156, +0.0540]** | **0.12** |
| rccma Δcollapse vs godard | +0.0364 | [+0.0091, +0.0727] | 0.00 |
| rccma Δpi_ser vs godard | +0.0583 | [+0.0268, +0.0956] | 0.05 |

Mean collapse rate: Godard **0.173** → ring_aware **0.209** → rccma **0.209**.
Mean PI-SER: Godard **0.251** → ring_aware **0.284** → rccma **0.309**.

## 5. Verdict — MECHANISM NEGATIVE for the ring-aware-cost premise

**The ring-aware cost does NOT reduce collapse. It INCREASES both the collapse
rate and PI-SER.** The decisive evidence:

### 5a. Zero collapse reduction, statistically significant *worsening*
Of 110 paired (cell, seed) points, **0%** show ring-aware collapsing less than
Godard (`frac_pair_collapse_reduced = 0.00`). The macro collapse-rate delta is
**+0.036** with CI **[+0.009, +0.073]** — entirely above zero. The ring-aware
cost makes collapse *more likely*, not less. RCCMA is identical on collapse
rate and worse on PI-SER.

### 5b. The collapse is seed-driven and SNR-invariant (so a cost change has little to act on)
On 8/11 cells the collapse rate is **exactly 0.20** (2/10 seeds) for *all
three* costs — the same two hard-collapse seeds (71, 73) collapse regardless
of cost. This reproduces the baseline-Atlas finding that the collapse is
seed-driven (a per-realization property), not a cost-tuning gap. Where the
costs *do* diverge (the 3 long cells, N=8192) the ring-aware cost is
**strictly worse**: snr10-fg100-long collapse 0.10 → 0.30, PI-SER 0.43 → 0.55.

### 5c. The mechanism: the ring-aware cost is SELF-CONSISTENT with the collapsed state
Direct gradient analysis at init on collapsing seed 71 (all 64 block-0 symbols
at the inner ring, |z|² ≈ 0.14):

| cost | block-0 mean error `e = R²−\|z\|²` | direction | magnitude |
|---|---|---|---|
| Godard (R²=1.32) | **+1.181** | strong OUTWARD pull | large (rescue attempt) |
| ring-aware (R²(z)=0.2 for inner symbols) | **+0.061** | near-zero pull | **19× weaker** |

The Godard cost, despite its ring-mismatch, at least generates a **large
outward gradient** when the output collapses to the inner ring (R²=1.32 ≫
inner |z|²=0.2). The ring-aware cost assigns R²(z)=0.2 to those same symbols,
so its error is ~0 — it **provides almost no restorative gradient**. The
ring-aware cost is *locally consistent* with the inner-ring collapse: once the
output is on the inner ring, the cost sees little wrong with it. It removes
the (admittedly inadequate) Godard rescue pressure without supplying a better
one. **The "mismatch" that ring-matching was meant to remove was actually the
only force pulling the equalizer back out.**

### 5d. RCCMA: cold-start freeze compounds the problem
RCCMA (outer-ring-only) has an additional failure mode: on a collapsing
realization the center-tap-init output never reaches the outer ring
(|z|² < 1.4 on every symbol), so **zero symbols are active** and the weights
freeze at init (verified: `final_w_norm == init_w_norm` exactly on seed 71,
`n_active = 0` on all 7 blocks). This is the classical reduced-constellation
cold-start trap (documented in `test_rccma_cold_start_freeze_on_inner_ring_output`).
RCCMA therefore cannot bootstrap on exactly the realizations that need help.

## 6. What this means for C15 and the portfolio

- **The collapse is NOT a Godard-cost ring-mismatch artifact.** The most
  natural "fix" implied by the ring-mismatch hypothesis — match R²(z) to the
  nearest ring — makes collapse *worse*, because the mismatch was the only
  restorative gradient. This is a **clean refutation of the ring-mismatch
  hypothesis as the collapse cause**.
- **This STRENGTHENS the "deep Godard-cost property" thesis**, but in a
  sharpened form: it is not the single-R² *mismatch* that traps CMA — it is
  that **any purely modulus-based cost (single-R² or multi-ring) is self-
  consistent with the inner-ring collapse**. A modulus cost cannot distinguish
  "all symbols correctly on the inner ring" from "all symbols wrongly collapsed
  onto the inner ring", because both look identical in the |z| distribution.
  Escaping collapse requires information a modulus cost structurally lacks.
- **Mechanism-distinct from MMA (D006/D040).** MMA failed via quadrant
  rotation; C15 failed via radius matching. Together they rule out both
  decompositions of 16QAM geometry (angle AND radius) for a *blind modulus*
  cost. The convergent evidence (C04/C09/C11 post-eq, C12 soft-output, C08
  adaptive-mu, MMA, now C15) is that **no receiver-side modification of a
  modulus-based blind cost / post-processor recovers the collapse**.
- **C15 is not promoted.** The ring-aware cost is a *negative mechanism result*.

## 7. Alternative explanations tested (evidence integrity)

| alternative | status |
|---|---|
| evaluator degenerate (smoke) | ruled out — smoke PASS; Godard reproduces known collapse; ring-aware finite & below ceiling |
| cost not actually changed | ruled out — `test_ring_aware_weights_differ_from_godard` PASS; final weights differ from Godard |
| engine not faithful to anchor | ruled out — `test_godard_wrapper_byte_identical_to_anchor` PASS (max\|Δz\|=0.0); Godard uses the protected READ-ONLY anchor import |
| ring boundaries wrong | ruled out — `test_ring_radii_match_16qam_geometry` PASS (verified against `_modulation.qam16_mod`, radii 0.2/1.0/1.8, boundaries 0.6/1.4) |
| RCCMA mask broken | ruled out — `test_rccma_uses_only_outer_ring_symbols_in_trace` PASS (masking active on seed 72); cold-start freeze on seed 71 is a real documented behavior, not a bug |
| TX truth leaked into candidate | ruled out — `test_candidate_modules_have_no_truth_imports` PASS (tokenized executable code scan); ring assignment signature takes `\|z\|²`, not symbols |
| too few seeds / power | 110 paired points, bootstrap CI computed; the *direction* (0% reduction, CI above 0) is cell-uniform, not a power issue |
| collapse definition mis-set | threshold 0.6 sits between healthy (~2.0) and collapsed (~0.3); verified seed 71 E\|z\|²=0.29 |

## 8. Scope, limits, next

- **Executed:** full 11-cell atlas × 10 fresh seeds (71–80), disjoint from all
  prior train/val seeds. 3 costs (Godard anchor, ring-aware, RCCMA) on the
  SAME paired realizations; identical structure (11 taps, block=64, μ=0.03,
  center-tap init) — ONLY the cost function differs.
- **Not executed / blocked:** a *hybrid* cost (e.g. Godard R² during a warm-up
  phase then switch to ring-aware once converged, to avoid the cold-start
  trap); a *decision-directed* cost (uses hard_16qam(z), not modulus — but that
  crosses into DD-LMS territory, C11); softer ring assignment (soft weighting
  rather than hard nearest-ring).
- **Claim ceiling:** LOCAL_SLICE / DIAGNOSTIC. The negative is locally robust
  (0% collapse reduction is cell-uniform; the self-consistent-trap mechanism is
  analytic, not statistical). A wider cell/seed sweep is unlikely to overturn it
  given the mechanism explanation.
- **Next (informative, not a method win):** the convergent negative across MMA
  (angle), C15 (radius), C04/C09/C11 (post-eq), C12 (soft-output) closes the
  "blind modulus / post-processing" axis. The remaining live mechanism line is
  a cost that is **NOT purely modulus-based** — e.g. a decision-directed or
  supervised-on-receiver-visible-features cost — which would need a fresh
  mechanism argument and likely a user strategic decision (it changes the
  equalizer's information class).

## 9. Harvest assessment

- **C15 ring-aware cost (the candidate):** FAILURE_MECHANISM / LOCAL_SLICE —
  does not reduce collapse; increases it. No durable thesis value as a *method*.
- **Mechanism insight — modulus costs are self-consistent with the collapse
  (sharpened "deep Godard-cost" thesis):** EVALUATION_INSIGHT / LOCAL_SLICE.
  The ring-mismatch hypothesis is **refuted** as the collapse cause: matching
  R²(z) to the nearest ring removes the only restorative gradient. The deeper
  finding is that **any purely modulus-based blind cost is locally consistent
  with inner-ring collapse** (it cannot distinguish correct-inner from
  collapsed-inner in the |z| distribution). Combined with MMA (angle), this
  rules out both geometric decompositions for a blind modulus cost. This is
  the strongest single-piece of evidence in the portfolio that the collapse is
  an *information* limit of modulus costs, not a *mismatch* artifact.
- **Reusable asset — ring-aware / RCCMA cost variants + cost-isolation engine:**
  REUSABLE_ASSET. `cma_cost_variants.py` provides a generic blockwise engine
  (certified byte-identical to the Godard anchor) with a parameterized cost;
  any future cost variant can be added by supplying `r2_of_z2` (and an optional
  `mask_of_z2`). The 12 identity tests certify the cost-isolation discipline.

---

*Artifacts: `artifacts/result.v1.json`. Contract: `batch-contract.v1.yaml`.
Code: `src/cma_cost_variants.py`, `src/run_cost_scout.py`,
`src/test_cost_identity.py` (12/12 identity tests GREEN). Concept provenance:
Sato 1975 (IEEE TCOM, reduced-constellation); Yang-Werner-Dumont 2002 (IEEE
JSAC, MMA — distinct, tested D006/D040); Godard 1980 (IEEE TCOM Eq.(10), anchor).*
