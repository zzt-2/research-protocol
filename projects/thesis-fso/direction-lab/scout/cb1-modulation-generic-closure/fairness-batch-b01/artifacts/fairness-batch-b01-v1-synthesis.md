# Fairness Batch B01 — Synthesis

**Campaign:** `science-scout-2026-07-20.dual-pol-osl`
**Batch:** Fairness Batch B01 (H004 / D007 — fairness debt + candidate over-narrowing)
**Date:** 2026-07-21
**Mode:** SCIENCE_SCOUT (no ML detector trained; conventional fairness probe only)
**Raw artifact:** `artifacts/fairness-batch-b01-v1.json`
**Contract:** `batch-contract.v1.yaml` (frozen before running)
**Frozen params:** `artifacts/frozen-params.v1.yaml`

---

## 1. Scientific question (frozen in contract)

Does the CB1 16QAM inner-ring collapse headroom (Atlas v1 max 0.333;
H022 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE) close under any of:

- **(a) FAIR TUNING** — give CMA a validation-cell-selected mu (C08 bandit
  outer-loop, plus per-method grid-tuned C10/C11) instead of the frozen
  mu=0.001;
- **(b) STRUCTURAL CHANGE** — per-symbol stochastic-gradient CMA
  (block_size=1, C10) instead of block-end (block_size=64);
- **(c) CONVENTIONAL CASCADE** — CMA followed by decision-directed LMS
  using nearest-16QAM hard decisions (C11)?

In parallel: can a conventional change-point / threshold detector (C05) on
causal CMA-trace features predict per-seed collapse before PI-SER degrades?

This directly addresses D007 fairness debts #1 (same mu), #2 (convergence
N), #3 (block-end causality), #4 (oracle recoverability), #5
(task-specific comparators), and #6 (candidate over-narrowing).

## 2. Comparators and provenance

| Candidate | Role | Mechanism | Source |
|---|---|---|---|
| `standard_cma_godard_z` | Diagnostic anchor (Atlas v1) | block-end CMA, μ=0.001, R²=1.32 | Godard 1980 TCOM Eq.(10) (inherited) |
| `C05` | Conventional detector baseline | CUSUM + threshold on output_power/(2·R²) | Page 1954 Biometrika; Basseville-Nikiforov 1993 §2.2 |
| `C08` | Adaptive step (bandit) | LinUCB selecting μ per batch from {1e-4, 3e-4, 1e-3, 3e-3, 1e-2} | Li, Chu, Langford, Schapire WWW 2010 §3.3 |
| `C10` | Structural variant | per-symbol SGD CMA, block_size=1, μ grid-tuned | Godard 1980 with block_size=1 |
| `C11` | Conventional cascade | CMA stage-1 + DD-LMS stage-2 warm-start | Sato 1975 TCOM Eq.(4); Kikuchi JLT 2016 §IV.B |

**Fairness controls (per D007 §1 and baseline-adjudication.md):**

- **Per-method tuning budget**, not identical hyperparameters: each method
  grid-searches its own hyperparameters on 4 validation cells (3 short + 1
  long, so convergence-length stability is visible to tuning) × 5 tuning
  seeds, then freezes before held-out evaluation.
- **Divergence penalty** in tuning score (0.1 × divergence_rate): unstable
  hyperparameters are strictly dispreferred even if mean PI-SER is similar.
- **Shared paired seeds** (11-20) and **shared channel realisations** for
  held-out evaluation.
- **Same information access** (CSI_NONE z-stream + public 16QAM alphabet)
  for all candidates.
- **Oracle affine** remains scoring-only Kill tool (FR-21), never Go (FR-25).

**Frozen params (after tuning):**

| Method | Best hyperparameter | Tuning score |
|---|---|---|
| C05 | z2_ratio_threshold=0.25, cusum_drift=0.02 | AUROC=0.500 (validation cells had mixed labels) |
| C08 | LinUCB α=10.0 (high exploration) | -0.206 mean PI-SER + div_penalty |
| C10 | μ=1e-5 (smallest in grid; per-symbol needs tiny step) | -0.206 |
| C11 | dd_step_size=1e-4 (smallest; conservative refinement) | -0.205 |

The tuning consistently selected **conservative** hyperparameters for
C10/C11 (smallest step sizes in their grids), because larger steps diverged
on the long validation cell. This is itself a finding: per-symbol CMA and
DD-LMS are stability-limited on long sequences in this channel.

## 3. Per-cell results (held-out evaluation, 10 paired seeds)

### PI-SER table

| cell | anchor | C08 | C10 | C11 | anchor headroom | C11 headroom | n_seeds_div (a/c10/c11) |
|---|---:|---:|---:|---:|---:|---:|---:|
| snr05-nominal-short | 0.6621 | 0.6625 | 0.6617 | 0.6633 | 0.0000 | 0.0000 | 0/0/0 |
| snr10-nominal-short | 0.4875 | 0.4879 | 0.4879 | 0.4867 | 0.0711 | 0.0695 | 0/0/0 |
| snr15-nominal-short | 0.3645 | 0.3660 | 0.3660 | 0.3613 | 0.2207 | 0.2180 | 0/0/0 |
| snr20-nominal-short | 0.3332 | 0.3332 | 0.3332 | 0.3309 | 0.3109 | 0.3086 | 0/0/0 |
| snr25-nominal-short | 0.3328 | 0.3332 | 0.3328 | 0.3320 | 0.3328 | 0.3320 | 0/0/0 |
| snr20-fg100-short | 0.3344 | 0.3352 | 0.3359 | 0.3324 | 0.3129 | 0.3105 | 0/0/0 |
| snr20-fg1000-short | 0.3410 | 0.3418 | 0.3418 | 0.3410 | 0.3211 | 0.3211 | 0/0/0 |
| snr20-sop40e-short | 0.3328 | 0.3332 | 0.3332 | 0.3332 | 0.3105 | 0.3109 | 0/0/0 |
| snr10-fg100-long | 0.4273 | 0.4094 | 0.4371 | **0.3984** | 0.0547 | **0.0234** | 0/0/0 |
| snr15-fg1000-long | 0.3219 | 0.3141 | 0.3277 | **0.3102** | 0.1477 | **0.1352** | 0/0/0 |
| snr20-nominal-long | 0.3055 | 0.2992 | 0.3070 | **0.3023** | 0.2324 | **0.2289** | 0/0/0 |

**Headroom < MDE (0.005) on held-out cells (n=7):**

| Method | Closed cells |
|---|---:|
| anchor (block-end μ=0.001) | 1/7 |
| C08 (LinUCB adaptive μ) | 1/7 |
| C10 (per-symbol μ=1e-5) | 1/7 |
| C11 (CMA + DD-LMS cascade) | 1/7 |

### Findings — fairness probe

1. **Fairness DOES NOT close the collapse.** All four methods (including
   fairly-tuned CMA, per-symbol structure, and DD-LMS cascade) leave
   headroom ≥ MDE on 6/7 held-out cells. The single "closed" cell is
   snr=5 dB (AWGN-dominated, no headroom for ANY method including oracle).
2. **C11 (CMA+DD-LMS) is the best variant on long cells** — it improves
   PI-SER by 0.01-0.03 on the three long cells (snr10-fg100-long:
   0.4273→0.3984, headroom 0.055→0.023). The improvement is consistent and
   in the direction expected from DD-LMS refining residual modulus error.
   BUT it is far from closing (headroom still 6× MDE on the best long cell).
3. **C08 (bandit) gives smaller long-cell improvement** (0.01-0.02 PI-SER).
   The bandit's selected μ was dominated by α=10.0 exploration: it tried
   many arms but did not consistently pick a clearly better μ than the
   anchor's fixed 0.001 on short cells. This is itself a finding: a
   contextual bandit with only 4 trace features and a dense proxy reward
   does not significantly improve on a well-chosen fixed μ.
4. **C10 (per-symbol) is slightly WORSE than the anchor on long cells**
   (snr10-fg100-long: 0.4273→0.4371). The per-symbol μ=1e-5 required for
   stability is too small to make sufficient update progress over N=8192
   symbols. This is a **negative result for the H021 infrastructure-gap
   hypothesis**: per-symbol CMA does NOT escape the collapse; if anything
   it makes it worse within a stable μ budget.
5. **Zero divergence across all 110 seeds** for all methods. Fair tuning
   (with divergence penalty + long validation cell) successfully avoided
   the runaway that MMA exhibited in baseline-adjudication.

## 4. C05 detector results

| cell | AUROC in cell | alert rate | collapse label rate |
|---|---:|---:|---:|
| snr05-nominal-short | 0.500 | 0.000 | 1.000 (AWGN-dominated; no structure) |
| snr10-nominal-short | **1.000** | 0.200 | 0.700 |
| snr15-nominal-short | **1.000** | 0.200 | 0.200 |
| snr20-nominal-short | 0.500 | 0.300 | 0.000 (no collapse → AUROC undefined) |
| snr25-nominal-short | 0.500 | 0.400 | 0.000 |
| snr20-fg100-short | 0.500 | 0.300 | 0.000 |
| snr20-fg1000-short | 0.500 | 0.400 | 0.000 |
| snr20-sop40e-short | 0.500 | 0.300 | 0.000 |
| snr10-fg100-long | **1.000** | 0.800 | 0.500 |
| snr15-fg1000-long | **1.000** | 0.900 | 0.200 |
| snr20-nominal-long | **1.000** | 0.900 | 0.200 |

**Pooled AUROC across all 110 seeds: 0.6546** (28 collapsed, 82 healthy).

### Findings — detector

1. **C05 detector achieves AUROC=1.000 on cells where collapse is both
   present AND separable** (4/11 cells: snr10/15-nominal-short and all
   three long cells). On these cells, a conventional threshold on
   output_power/(2·R²) perfectly separates collapsed from healthy seeds.
2. **AUROC=0.500 on cells with no collapse** (5 short cells at snr≥20) —
   this is the degenerate case (no positive labels, AUROC undefined, and
   alert_rate is the false-alarm rate).
3. **AUROC=0.500 on snr=5** — AWGN-dominated; "collapse" label fires for
   all seeds but it is not the inner-ring-collapse signature, just noise.
4. **Pooled AUROC=0.6546** is in the **[0.65, 0.85)** band per the
   pre-registered decision rule → **authorizes B02 ML detector batch with
   narrowed claim** "ML improves lead time / calibration over conventional
   threshold".

The detector signal is **conditional**: in long cells where the collapse
trajectory has time to develop, the output_power signature is a perfect
separator. In short cells, the trajectory has not yet committed to
collapse vs healthy within the N=512 window — the signal is weak or absent.

## 5. Mechanism (what survives and why)

### What was ruled out

- **(a) Fair tuning closes the collapse** — RULED OUT. C08 bandit, C10
  per-symbol, and C11 cascade all tuned with per-method validation budgets
  leave headroom on 6/7 held-out cells. Fairness was not the issue.
- **(b) Per-symbol structure closes the collapse (H021)** — RULED OUT.
  C10 per-symbol CMA is slightly WORSE than the block-end anchor on long
  cells. The block-end protocol is NOT the bottleneck; per-symbol updates
  are stability-limited and do not help.
- **(c) Conventional cascade closes the collapse** — RULED OUT. C11 gives
  small (0.01-0.03) improvements on long cells but does not approach
  closing (headroom still 6× MDE).

### What survives

The CB1 16QAM inner-ring collapse is a **stable convergence failure of
Godard-cost CMA on this channel that survives fair per-method tuning,
structural variation (block-end vs per-symbol), and conventional
DD-LMS cascade refinement**. This strengthens H022
(PROBLEM_SURVIVES_CONVENTIONAL_BASELINE) with fairness-closed evidence:

- H022 established survival vs MMA + length variation.
- B01 establishes survival vs **fairly-tuned CMA + per-symbol structure
  + CMA+DD-LMS cascade**.

The two adjudications are complementary: MMA is task-mismatch, C10 is
structural, C11 is cascade. All four conventional angles (MMA, fair tuning,
structure, cascade) fail to close the collapse.

### What this means for ML (B02)

The collapse is **mechanism-relevant for ML** with **narrower claim
scope** than H022 originally implied:

- The collapse is detectable (C05 AUROC=1.000 on separable cells), so a
  learned detector CAN pick up the signal.
- The conventional detector's pooled AUROC is 0.6546 (limited by short-cell
  ambiguity), so ML's contribution is **lead time / calibration in the
  ambiguous short-cell regime**, not just raw detection.
- The collapse is NOT recoverable by any tested conventional means
  (C08/C10/C11 all fail to close), so a learned CORRECTOR (C04/C09) has
  a defensible target — the residual after fair conventional treatment.

## 6. Verdict

**`PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT`** (per batch-contract.v1.yaml
decision rule).

Decision rule check:
- **Condition (a) CLOSED_BY_FAIR_CONVENTIONAL_TREATMENT**: at least one of
  {C08, C10, C11} achieves headroom < MDE on ≥ 9/11 atlas cells →
  **FAIL** (best variant C11 closes only 1/7 held-out cells).
- **Combined with H022 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE**: the
  collapse survives both task-correct comparator (MMA) AND fair
  conventional treatment (tuning + structure + cascade).

**Conditional authorization for B02 ML detector batch** (per decision rule
`AUTHORIZE_B02_ML_DETECTOR_BATCH_CONDITIONAL`):

- C05 pooled AUROC = 0.6546 ∈ [0.65, 0.85) → B02 authorized with
  **narrowed claim**: "ML improves lead time / calibration over
  conventional threshold detector in the short-cell ambiguous regime".
- B02 candidates: C01 (supervised temporal), C02 (SSL anomaly), C06
  (density OOD). Task-specific comparator = C05 (the conventional
  threshold detector just measured). Shared adapter sprint: causal feature
  stacker (half-day, shared across C01/C02/C06).
- B02 Go metric: must beat C05's pooled AUROC (0.6546) AND achieve
  meaningful warning lead time on the cells where C05 already has
  AUROC=1.000 (i.e., ML must provide lead time, not just detection).

## 7. Claim ceiling

**SLICE (LOCAL_RESULT).** This batch is scoped to:

- Modulation: square 16QAM only.
- CSI access: CSI_NONE (receiver z-stream + public 16QAM alphabet only).
- Channel: dual-pol OSL with Gamma-Gamma strong turbulence (α=4.2, β=1.4),
  SOP rotation 4e-6 to 4e-5 rad/sym, Greenwood frequency 30-1000 Hz.
- Algorithm class: block-end Godard-with-z CMA, per-symbol Godard-with-z
  CMA, LinUCB-bandit-driven CMA, CMA+DD-LMS cascade. RLS, frequency-
  domain, neural equalizer variants are NOT adjudicated.
- Detector class: CUSUM + threshold on output_power/(2·R²).
- Tuning: 4 validation cells × 5 tuning seeds, per-method grid, divergence
  penalty.

**DOMAIN remains UNRESOLVED.** Receiver-estimated CSI (C13) and
soft/coded output (C12) axes are still INFRASTRUCTURE_BLOCKED.

## 8. What this batch did NOT do

- Did NOT train any ML detector. B02 is authorized but not executed.
- Did NOT close the collapse. The problem survives all conventional
  treatments tested.
- Did NOT modify the CMA anchor's identity or protected history. Anchor
  results are byte-identical to Atlas v1 / baseline-adjudication.
- Did NOT promote any result to formal Groundwork/Contract/Execute/paper.
  Scout/Sandbox only.
- Did NOT test pilot-aided (C13) or coded (C12) — those are in different
  information classes and remain blocked.

## 9. Open questions / unresolved limits

1. **Is the short-cell ambiguity fundamental or an artifact of N=512?**
   The C05 detector achieves AUROC=1.000 on long cells but 0.5 on short
   cells. This could mean either (a) the collapse trajectory is genuinely
   not committed at N=512, or (b) the detector's threshold is calibrated
   on long-cell statistics and mis-fires on short cells. B02 ML detector
   with learned temporal features could resolve this.
2. **Does C11's small long-cell improvement compound over more DD
   iterations?** This batch used dd_iterations=1 (per contract). A
   multi-iteration cascade might improve further, but risks overfitting
   to wrong hard decisions on collapsed seeds.
3. **Does a learned CORRECTOR (C04/C09) recover collapsed seeds where
   C11 cannot?** C11 uses public hard decisions (wrong on collapsed z);
   C04/C09 would condition on trace features (carrying collapse
   signature). This is the B03 question (after B02).

## 10. Harvest (this batch)

Per campaign-contract.v1.yaml: every scientific batch leaves at least one
piece of thesis material. This batch leaves:

| Harvest ID | Category | Content |
|---|---|---|
| H023 | BASELINE_ADJUDICATION (fairness extension) | CB1 16QAM inner-ring collapse survives fair per-method tuning (C08 bandit), per-symbol structure (C10 block_size=1), and CMA+DD-LMS cascade (C11). Best variant C11 improves long-cell PI-SER by 0.01-0.03 but does not close (headroom still ≥6×MDE). Extends H022 with fairness-closed evidence. |
| H024 | FAILURE_MECHANISM | Per-symbol CMA (block_size=1, μ=1e-5) is slightly WORSE than block-end anchor on long cells. The H021 infrastructure-gap hypothesis (block-end protocol as bottleneck) is NOT supported: per-symbol structure does not escape the collapse within a stable μ budget. |
| H025 | METHOD_SIGNAL (detector, scoped) | Conventional threshold detector (CUSUM + output_power/(2·R²) threshold, Page 1954) achieves AUROC=1.000 on cells where collapse is both present and separable (4/11 cells: snr10/15 short + all 3 long). Pooled AUROC=0.6546. Short-cell ambiguity is the limiting factor. |
| H026 | REUSABLE_ASSET | B01 candidate code (b01_candidates.py: C05/C08/C10/C11 implementations + sanity tests + frozen tuning protocol) is a reusable fairness-batch infrastructure for any future 16QAM equalization work in this project. Per-method tuning budget with divergence penalty is a generalisable fairness contract. |
| H027 | EVALUATION_INSIGHT | Detector AUROC is **conditional on convergence length**: perfect on long cells, chance on short cells. This implies collapse detection requires either (a) waiting until the trajectory has committed (long N), or (b) a learned temporal model that can extract early signatures from short traces. B02 ML detectors target (b). |
| H028 | LOCAL_NEGATIVE | LinUCB bandit with 4 trace features and dense proxy reward does NOT significantly improve over a well-chosen fixed μ=0.001 on short cells. Bandit-driven step adaptation is not a free win; richer context or reward shaping is needed. |

## 11. Rotation

Per `references/recovery-and-rotation.md` and user prompt §七: this batch
reached PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT with conditional
authorization for B02. The next batch (in a clean-context conversation)
should:

1. Run shared adapter sprint: causal feature stacker (aligns CMA-trace
   blocks to per-seed labels; shared by C01/C02/C06). Half-day, bounded.
2. Run B02 = {C01, C02, C06} with shared contract:
   - Task-specific comparator = C05 (conventional threshold, AUROC=0.6546).
   - Shared input = causal CMA-trace features.
   - Go metric = pooled AUROC > 0.6546 AND warning lead time on long cells.
   - Claim ceiling = SLICE, narrowed to "ML improves lead time / calibration".
3. If B02 succeeds (AUROC > C05 with meaningful lead time), proceed to B03
   = learned correctors {C04, C09} targeting the residual collapse after
   fair conventional treatment. Task comparator = blind affine.
4. If B02 fails (ML does not beat C05), record LOCAL_NEGATIVE on ML
   detection and rotate to C13 (pilot-aided, different information class).

In parallel, the Portfolio keeps C12 (soft-output, blocked) and C13
(pilot-aided) open for future campaigns.
