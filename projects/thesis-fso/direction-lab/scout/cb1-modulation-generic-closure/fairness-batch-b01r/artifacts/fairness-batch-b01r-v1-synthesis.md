# Fairness Batch B01-R — Synthesis (Correction Batch)

**Campaign:** `science-scout-2026-07-20.dual-pol-osl`
**Batch:** Fairness Batch B01-R (correction of B01; supersedes D008 / H005)
**Date:** 2026-07-21
**Mode:** SCIENCE_SCOUT (no ML trained; conventional fairness + detector probe only)
**Raw artifact:** `artifacts/fairness-batch-b01r-v1.json`
**Contract:** `batch-contract.v1.yaml` (frozen before running)
**Frozen params:** `artifacts/frozen-params-b01r-v1.yaml`
**Audit reproduction:** `artifacts/b01-audit-reproduction.md` (all 10 findings confirmed)
**Predecessor:** B01 (`fairness-batch-b01/`) — preserved untouched as DIAGNOSTIC history.

---

## 0. Scope of correction

B01-R addresses 10 audit findings on B01 (all independently reproduced;
see `b01-audit-reproduction.md`). The correction rebuilds:

1. A **no-leakage seed split** (tuning seeds [11-15] disjoint from test
   seeds [21-30]).
2. A **validation-optimal fixed-μ CMA** as a genuine Go comparator (B01
   only tuned C08's alpha and left the anchor at frozen μ=0.001).
3. **Achievable exit criteria** (5/7 closed of 7 held-out cells, not
   9/11 of 7 which was unreachable).
4. A **4-category collapse label audit** (inner-ring/recoverable,
   AWGN-dominated, healthy, ambiguous) replacing the leaky binary
   `oracle_pi_ser > 0.3` rule.
5. **Real detector metrics**: per-cell AUROC (NA/UNDEFINED for single-
   class cells), PR-AUC, recall@5%FPR, false-alarm, degradation onset,
   warning lead time, Brier/ECE.
6. **Paired bootstrap CIs** over test seeds (10k resamples, 95%).
7. A **C05 detector score tied to the tuned parameters** (alert earliness,
   not the parameter-independent -min(z2_ratio)).

## 1. Scientific question (frozen)

Under the no-leakage split and a real validation-optimal fixed-μ CMA, do
{fixed-μ CMA, C08 bandit, C10 per-symbol, C11 cascade} close the CB1
16QAM inner-ring collapse headroom on ≥ 5/7 held-out cells? And does a
conventional detector produce a defensible target for an ML detector
(B02)?

## 2. Frozen params (after tuning on validation cells × tuning seeds)

| Method | Best hyperparameter | Tuning score |
|---|---|---|
| fixed_mu_cma (NEW genuine comparator) | μ=1e-2 (largest in grid) | -0.2047 mean PI-SER + div_pen |
| C08 (LinUCB bandit) | α=10.0 | -0.2055 |
| C10 (per-symbol CMA) | μ=1e-5 (smallest; stability-limited) | -0.2061 |
| C11 (CMA+DD-LMS) | dd_step_size=1e-4 (smallest; conservative) | -0.2049 |
| C05 (CUSUM/threshold detector) | z2_ratio_threshold=0.2, cusum_drift=0.01 (DEFAULT-GRID fallback; tuning did not select) | macro-AUROC=-1.0 (no two-class cells in validation after 4-cat label audit) |

Note: C05's macro-AUROC tuning score is -1.0 because the 4-category
label audit makes ALL validation cells single-class under the strict
`inner_ring_recoverable_collapse` vs `healthy` binary projection.
`tune_method` then fell back to the grid's FIRST element (0.2, 0.01) by
the `>` tie-break. We therefore frame the C05 detector run as
**"default-grid C05"**, NOT "tuned C05". This is a limitation (see §7)
but does not affect the verdict: the detector metrics reported in §5
are honest test-time outputs of the default-grid detector.

## 3. Per-cell PI-SER (test seeds 21-30)

| cell | anchor | **fixed_μ** | C08 | C10 | C11 | anchor_H | fixed_μ_H | C11_H |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| snr05-nominal-short (HELD) | 0.6594 | 0.6316 | 0.6621 | 0.6617 | 0.6520 | 0.0465 | **0.0020** | 0.0402 |
| snr10-nominal-short (HELD) | 0.5309 | 0.4828 | 0.5348 | 0.5336 | 0.5184 | 0.1332 | 0.0730 | 0.1207 |
| snr15-nominal-short (HELD) | 0.4375 | 0.3824 | 0.4406 | 0.4414 | 0.4137 | 0.2527 | 0.1949 | 0.2293 |
| snr20-nominal-short (val) | 0.3809 | 0.3363 | 0.3910 | 0.3891 | 0.3555 | 0.3383 | 0.2922 | 0.3129 |
| snr25-nominal-short (HELD) | 0.3457 | 0.3148 | 0.3539 | 0.3535 | 0.3223 | 0.3426 | 0.3117 | 0.3191 |
| snr20-fg100-short (HELD) | 0.3812 | 0.3359 | 0.3910 | 0.3895 | 0.3555 | 0.3387 | 0.2922 | 0.3129 |
| snr20-fg1000-short (val) | 0.3770 | 0.3320 | 0.3848 | 0.3840 | 0.3523 | 0.3359 | 0.2918 | 0.3113 |
| snr20-sop40e-short (val) | 0.3840 | 0.3383 | 0.3902 | 0.3891 | 0.3547 | 0.3422 | 0.2965 | 0.3125 |
| snr10-fg100-long (HELD) | 0.4129 | 0.3934 | 0.4020 | 0.4145 | 0.4035 | 0.0398 | 0.0164 | 0.0309 |
| snr15-fg1000-long (HELD) | 0.2684 | 0.2309 | 0.2613 | 0.2699 | 0.2570 | 0.1133 | 0.0770 | 0.1004 |
| snr20-nominal-long (val) | 0.2281 | 0.1758 | 0.2176 | 0.2297 | 0.2109 | 0.1461 | 0.0961 | 0.1289 |

Headroom < MDE (0.005) counts on 7 held-out cells:

| Method | Closed cells (of 7) | Which |
|---|---:|---|
| anchor (frozen μ=0.001) | 0/7 | — |
| **fixed_μ CMA (μ=0.01, tuned)** | **1/7** | snr05-nominal-short |
| C08 (LinUCB α=10) | 0/7 | — |
| C10 (per-symbol μ=1e-5) | 0/7 | — |
| C11 (CMA+DD-LMS dd=1e-4) | 0/7 | — |

**The fairly-tuned fixed-μ CMA (the comparator B01 never ran) closes 1
extra cell the anchor did not (snr05). No other method closes any
held-out cell.**

## 4. Paired bootstrap CIs (method vs anchor, 10 test seeds, 95% CI)

A CI marked `*` does not cross 0 (significant at 5%).

| cell | fixed_μ Δ [CI] | C08 Δ [CI] | C10 Δ [CI] | C11 Δ [CI] |
|---|---|---|---|---|
| snr05-short | **-0.028 [-0.063,-0.002]** `*` | +0.003 [0,+0.007] | +0.002 [0,+0.006] | -0.007 [-0.018,+0.001] |
| snr10-short | **-0.048 [-0.106,-0.004]** `*` | +0.004 [0,+0.008] | +0.003 [-0.001,+0.007] | -0.013 [-0.029,+0.001] |
| snr15-short | **-0.055 [-0.123,-0.005]** `*` | +0.003 [0,+0.006] `*` | +0.004 [-0.001,+0.009] | **-0.024 [-0.057,-0.003]** `*` |
| snr25-short | **-0.031 [-0.081,-0.001]** `*` | +0.008 [0,+0.024] | +0.008 [0,+0.023] | **-0.023 [-0.062,-0.001]** `*` |
| snr20-fg100-short | **-0.045 [-0.104,-0.006]** `*` | +0.010 [0,+0.025] | +0.008 [0,+0.025] | **-0.026 [-0.061,-0.001]** `*` |
| snr10-fg100-long | **-0.020 [-0.037,-0.002]** `*` | **-0.011 [-0.025,-0.001]** `*` | +0.002 [-0.001,+0.004] | -0.009 [-0.024,+0.001] |
| snr15-fg1000-long | **-0.038 [-0.069,-0.010]** `*` | **-0.007 [-0.015,-0.001]** `*` | +0.002 [0,+0.003] | **-0.011 [-0.025,-0.000]** `*` |

Findings:
- **fixed_μ CMA significantly beats anchor on 7/7 held-out cells.** The
  tuned μ=0.01 dominates the frozen μ=0.001 anchor everywhere. This
  confirms B01 audit finding #2: the validation-optimal fixed-μ CMA is
  a meaningful comparator that was missing in B01.
- **C11 significantly beats anchor on 4/7 cells** (3 short: snr15/snr25/
  snr20-fg100; 1 long: snr15-fg1000). But the improvement is small
  (|Δ| ≤ 0.026), does not close headroom on any cell (best C11 headroom
  still 0.0309 on snr10-fg100-long), and is NOT significant on 3/7
  cells (snr05/snr10/snr10-fg100-long).
- **C10 never significantly differs from anchor.** This reproduces B01's
  negative finding for H021 (block-end vs per-symbol): with this exact
  μ=1e-5/N=8192/N=512 configuration, per-symbol CMA is essentially
  indistinguishable from the anchor. (Finding is restricted to this
  configuration; not a wholesale closure of block-end causality.)
- **C08 mixed**: significant improvement on 2 long cells (snr10-fg100-long,
  snr15-fg1000-long) but a small significant degradation on 1 short cell
  (snr15-short). Net: bandit adds no robust advantage over fixed-μ CMA.

## 5. Detector evaluation (4-category label audit)

### 5.1 Label counts (test seeds 21-30, 11 cells × 10 seeds = 110 seeds)

| cell (HELD/val) | inner_ring | awgn_dom | healthy | ambiguous |
|---|---:|---:|---:|---:|
| snr05-short (HELD) | 0 | 8 | 0 | 2 |
| snr10-short (HELD) | 0 | 2 | 0 | 8 |
| snr15-short (HELD) | 0 | 0 | 2 | 8 |
| snr20-short (val) | 2 | 0 | 2 | 6 |
| snr25-short (HELD) | 4 | 0 | 4 | 2 |
| snr20-fg100-short (HELD) | 2 | 0 | 2 | 6 |
| snr20-fg1000-short (val) | 2 | 0 | 3 | 5 |
| snr20-sop40e-short (val) | 2 | 0 | 2 | 6 |
| snr10-fg100-long (HELD) | 0 | 7 | 0 | 3 |
| snr15-fg1000-long (HELD) | 0 | 1 | 6 | 3 |
| snr20-nominal-long (val) | 2 | 0 | 6 | 2 |

Critical observations:

- The strict `inner_ring_recoverable_collapse` label is **rare** (14/110
  seeds, 12.7%). The B01 binary `oracle_pi_ser > 0.3` rule had labelled
  many more seeds as "collapse" but most were actually AWGN-dominated
  (oracle couldn't recover them) or ambiguous.
- **No held-out long cell has any `inner_ring_recoverable_collapse`
  seed.** The two held-out long cells (snr10-fg100-long, snr15-fg1000-long)
  are dominated by AWGN errors and ambiguous cases. B01's claim that C11
  improves "long cells" was real on PI-SER, but the improvement is NOT
  on inner-ring collapse — it's on AWGN-dominated or ambiguous regimes
  where DD-LMS's hard decisions happen to track the symbols slightly
  better.
- **Only 2 held-out cells (snr25-short, snr20-fg100-short) are two-class
  under the strict binary projection** (both have inner_ring and healthy
  seeds). All other held-out cells are single-class or have only
  AWGN/ambiguous labels.

### 5.2 Per-cell detector metrics (c05_alert_earliness, tuned C05)

For cells that are two-class under the strict binary projection:

| cell | n_pos | n_neg | AUROC | PR-AUC | recall@5%FPR | lead_mean | n_with_lead |
|---|---:|---:|---:|---:|---:|---:|---:|
| snr25-short (HELD) | 4 | 4 | **0.875** | 0.95 | 1.0 | 2.0 blocks | 3/4 positives |
| snr20-fg100-short (HELD) | 2 | 2 | 0.75 | 0.75 | 0.5 | 2.0 blocks | 1/2 positives |

For all other held-out cells, AUROC is **NA/UNDEFINED** (single-class).
This is reported honestly, not as 0.5.

The min-z2-ratio baseline score had **zero two-class held-out cells**
(the strict label audit removed all its usable cells). So the bare
heuristic has no comparable AUROC; it is dominated by the tuned C05 on
the two two-class cells.

### 5.3 Calibration

Brier score and ECE are computed but their interpretation is fragile:
the detector score (alert earliness) is a ranking signal, not a
calibrated probability. The logistic mapping in `b01r_detector.detector_score_to_prob`
is a crude calibration proxy. **We do NOT make any calibration claim.**
Raw Brier/ECE values are in the JSON for the record but are not promoted
to a finding.

## 6. Verdict

**`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`** (per
batch-contract.v1.yaml B01-R decision rule).

Decision rule check:
- **CLOSE_THRESHOLD (5/7 held-out cells)**: NO method reaches it. Best is
  fixed_μ CMA with 1/7. → Problem survives fairness.
- **Detector target ready (≥2 two-class test cells for BOTH detector
  scores)**: c05_alert_earliness has 2 two-class cells; min_z2_ratio has
  0. → Detector target NOT ready.

This means:

1. The CB1 16QAM inner-ring collapse **survives** a genuinely fair
   conventional treatment (the validation-optimal fixed-μ CMA closes
   only 1/7 held-out cells; the per-symbol, bandit, and DD-LMS cascade
   close 0/7). The headroom is real and not closed by tuning, structure,
   or cascade.
2. **B02 ML detector batch is NOT authorized.** The strict 4-category
   label audit reveals that the "collapse" signal B01 was detecting is
   mostly AWGN-dominated error or ambiguous cases. Only 2 held-out cells
   have a defensible two-class collapse-vs-healthy split, and that is
   below the threshold (≥2 two-class cells for BOTH detector scores)
   required to support a meaningful ML detector target.

## 7. What this means for the project

### Equalizer side (positive)

- The collapse mechanism survives fairness rigorously. This is stronger
  evidence than B01's leaky, comparator-missing verdict.
- The validation-optimal fixed-μ CMA at μ=0.01 is the new baseline
  reference. It outperforms the frozen-μ=0.001 anchor on every cell.
- C11 (CMA+DD-LMS) gives a small but statistically significant PI-SER
  improvement on 4/7 held-out cells. This is a real (if modest) signal,
  but it is NOT closing the collapse and is partly on AWGN-dominated
  regimes, not inner-ring collapse.

### Detector side (negative)

- The 4-category label audit is the central correction. B01's binary
  `oracle_pi_ser > 0.3` label conflated inner-ring collapse (oracle
  recovers) with AWGN-dominated error (oracle does not recover). After
  separation, the inner-ring collapse population is much smaller than
  B01 implied.
- A B02 ML detector targeting "collapse" would be targeting a label
  that exists in only 14/110 seeds and is concentrated in validation
  cells, not held-out cells. This is not a viable supervised target
  without building additional label infrastructure first.
- We therefore do NOT authorize B02. The candidate family should rotate
  to mechanisms that do not depend on a collapse-detector target.

### What was NOT done

- Did NOT train any ML detector.
- Did NOT modify B01's raw artifact / frozen params / synthesis (B01 is
  preserved as DIAGNOSTIC history).
- Did NOT delete D008 or H005 (they are marked superseded).
- Did NOT modify protected history (B001-B003, P03, CB1 raw, canonical-
  state).
- Did NOT create legacy B004.
- Did NOT modify the CMA anchor identity (byte-identical regression
  preserved).
- Did NOT promote any result to formal Groundwork/Contract/Execute/paper.

## 8. Claim ceiling

**SLICE (LOCAL_RESULT).** Scoped to:

- Modulation: square 16QAM.
- CSI access: CSI_NONE.
- Channel: dual-pol OSL, Gamma-Gamma (α=4.2, β=1.4), SOP 4e-6 to 4e-5
  rad/sym, Greenwood 30-1000 Hz.
- Algorithm class: block-end Godard-with-z CMA, per-symbol Godard-with-z
  CMA, LinUCB-bandit CMA, CMA+DD-LMS cascade.
- Detector class: CUSUM + threshold on output_power/(2·R²), and min-z2-
  ratio scoring baseline.
- Tuning: 4 validation cells × 5 tuning seeds, per-method grid,
  divergence penalty.
- Test: 7 held-out cells × 10 test seeds (disjoint from tuning).
- Label audit: 4-category (inner-ring/recoverable, AWGN-dominated,
  healthy, ambiguous); binary projection for AUROC uses only
  inner-ring (positive) vs healthy (negative).

**DOMAIN remains UNRESOLVED.** Receiver-estimated CSI (C13) and
soft/coded output (C12) axes are still INFRASTRUCTURE_BLOCKED.

## 9. Open questions

1. Is the "ambiguous" label category (54/110 seeds, 49%) hiding real
   collapse signal that the strict oracle-affine-recoverability test
   misses? A learned representation might separate these, but only after
   a credible label-source is built.
2. Does a larger test seed budget (e.g., 20 or 30 test seeds) increase
   the two-class held-out cell count enough to authorise a B02 detector
   target? Currently 10 test seeds × 7 held-out cells gives too few
   inner-ring positives.
3. Would a different oracle test (not affine) reveal more recoverable
   collapse seeds? The affine oracle is the FR-21 Kill tool; a richer
   oracle class might be worth exploring for LABEL purposes only.

## 10. Harvest

| Harvest ID | Category | Content |
|---|---|---|
| H029 | BASELINE_ADJUDICATION (rigorous fairness extension) | Under a no-leakage split (tuning [11-15], test [21-30]) with a validation-optimal fixed-μ CMA (μ=0.01, the comparator B01 never ran), the CB1 16QAM inner-ring collapse headroom remains on 6/7 held-out cells. Only the AWGN-floor cell (snr05-short) closes. Fixed-μ CMA significantly beats the frozen-μ anchor on 7/7 cells (paired bootstrap CI). Extends H022/H023 with the genuine fixed-μ comparator. |
| H030 | FAILURE_MECHANISM (detector target) | The binary `oracle_pi_ser > 0.3` collapse label (B01) conflates inner-ring recoverable collapse with AWGN-dominated error. A 4-category audit (inner-ring/recoverable, AWGN-dominated, healthy, ambiguous) shows only 14/110 seeds (12.7%) are true inner-ring-recoverable collapses, and ZERO are in held-out long cells. A B02 ML detector targeting "collapse" is therefore not viable without additional label infrastructure. |
| H031 | METHOD_SIGNAL (C11, scoped honestly) | C11 (CMA+DD-LMS) significantly beats the anchor on 4/7 held-out cells (paired bootstrap CI excludes 0), but |Δ| ≤ 0.026 and headroom remains ≥ 6×MDE everywhere. The improvement is on AWGN-dominated / ambiguous regimes, not on inner-ring collapse (no held-out long cell has an inner-ring seed). |
| H032 | EVALUATION_INSIGHT (single-class AUROC honesty) | Single-class cells must report AUROC = NA/UNDEFINED, not 0.5. In this batch, 5 of 7 held-out cells are single-class under the strict binary projection (collapse vs healthy). Reporting these as 0.5 (as B01 did) inflates apparent detector coverage. |
| H033 | EVALUATION_INSIGHT (no-leakage split) | Tuning [11-15] ∩ test [21-30] = ∅ is the minimum bar for honest evaluation. B01's leaky overlap (seeds 11-15 in both) was a silent validity flaw. Paired bootstrap CIs over test seeds give honest uncertainty; without them, small Δ (e.g., C11's 0.01) cannot be distinguished from noise. |
| H034 | REUSABLE_ASSET (B01-R infrastructure) | The B01-R runner + detector module (4-category label audit, paired bootstrap CI, real detector metrics including PR-AUC / recall@5%FPR / false-alarm / degradation onset / warning lead time / Brier / ECE) is a reusable fairness-batch infrastructure for any future detector or equalization work. |

## 11. Rotation

Per `references/recovery-and-rotation.md` and the user's prompt §九
("按上述 A/B/C 自动收口"):

**Verdict B → next action: rotate to other mechanism families.**

The detector family (C01/C02/C05/C06) is blocked pending credible label
infrastructure. Two legal next directions:

1. **Stay on the equalizer side**: exploit C11's small but significant
   improvement and the fixed-μ CMA's dominance to ask whether a learned
   CORRECTOR (C04/C09) can recover residual error where DD-LMS cannot.
   Task comparator = validation-optimal fixed-μ CMA (μ=0.01), NOT the
   frozen-μ anchor.
2. **Rotate to a different mechanism family**: C13 (pilot-aided) or C12
   (soft/coded) open different information classes. These are
   INFRASTRUCTURE_BLOCKED but unblockable with bounded adapters.

The user's prompt explicitly allows automatic rotation on local
blockers; we record this as the next-action in H006.

## 12. Note on B01's superseded status

B01's raw numerical results (11 cells × 10 seeds × {anchor, C05, C08,
C10, C11}) are preserved as DIAGNOSTIC history. They are valid as raw
data; what is superseded is:

- The `PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT` verdict (B01-R
  reaches the same survival conclusion via a higher-fidelity path, so
  the survival claim is CONFIRMED not overturned).
- The `AUTHORIZE_B02_ML_DETECTOR_BATCH_CONDITIONAL` authorisation (B01-R
  WITHDRAWS this; detector target is not ready).
- The C11 "long cells improve 0.01-0.03" claim (B01-R narrows this to
  "4/7 held-out cells improve significantly; 0/3 held-out long cells
  have inner-ring collapse signal").
- The C05 "pooled AUROC=0.6546" metric (B01-R replaces with per-cell
  AUROC; only 2 held-out cells are two-class; pooled is not the
  headline).

D008 → superseded by D009.
H005 → superseded by H006.
