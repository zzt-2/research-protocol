# B01 Audit Reproduction — 10 Findings

**Date:** 2026-07-21
**Source:** pasted task 2026-07-21 (10 audit findings from user)
**Method:** Independent reproduction against source code + raw JSON
**Result:** ALL 10 CONFIRMED with concrete evidence below.

## Finding 1: B01 ran 11 cells × 10 seeds (raw numerical data preserved)

**Status:** CONFIRMED.

Evidence (from `fairness-batch-b01-v1.json`):
- `n_cells = 11`
- `seeds_per_cell = {10}` (uniform)
- `total_seeds = 110`

All numerical values in B01's raw JSON are preserved untouched in
B01-R (we will NOT modify the raw artifact).

## Finding 2: validation-optimal fixed-μ CMA was NOT actually run as comparator; C08 only tuned LinUCB alpha

**Status:** CONFIRMED.

Evidence (from `run_fairness_batch_b01.py:200-206` and `TUNE_GRID["C08"]`):

```python
def run_c08(cell, realization, *, alpha):
    return cand.c08_adaptive_mu_bandit(
        ..., mu_candidates=(1e-4, 3e-4, 1e-3, 3e-3, 1e-2), alpha=float(alpha),
    )

TUNE_GRID = {
    "C08": {"alpha": [0.1, 1.0, 10.0]},  # ONLY alpha tuned
    ...
}
```

The `fixed_mu_cma_validation_optimal` comparator listed in `batch-contract.v1.yaml:70` as C08's `task_specific_comparator` was **never implemented**. The CMA anchor (`standard_cma_godard_z`) ran with frozen `μ=0.001`, which is NOT validation-optimal. So C08 was compared against a frozen-μ anchor, not a fairly-tuned fixed-μ CMA.

## Finding 3: C05 AUROC score was `-min(z2_ratio)`, unrelated to threshold/CUSUM drift

**Status:** CONFIRMED.

Evidence (from `run_fairness_batch_b01.py:348-355`):

```python
ratios = [a["z2_ratio"] for a in det["alerts"] if not np.isnan(a["z2_ratio"])]
if not ratios:
    continue
score = -float(np.min(ratios))  # ← the "AUROC" input is just -min ratio
scores.append(score)
labels.append(label)
return _auroc(scores, labels)
```

The `score` is `-min(z2_ratio)` regardless of `z2_ratio_threshold` or `cusum_drift`. The tuned `z2_ratio_threshold` and `cusum_drift` parameters only affect the `alerts` list (used for `alert_any` / `alert_first_block`), NOT the `detector_score`. Hence C05's "AUROC" is mechanically the separability of `-min(z2_ratio)` — it tells us nothing about whether the tuned CUSUM/threshold detector works.

## Finding 4: raw frozen C05 parameters disagree with synthesis/H005

**Status:** CONFIRMED.

Evidence:

| Source | z2_ratio_threshold | cusum_drift |
|---|---|---|
| `frozen-params.v1.yaml` (raw) | 0.2 | 0.01 |
| `fairness-batch-b01-v1-synthesis.md` line 64 | 0.25 | 0.02 |
| `H005-fairness-batch-b01-complete.md` line 66 | 0.25 | 0.02 |

Raw says (0.2, 0.01); synthesis and handoff both say (0.25, 0.02). Neither matches the other.

## Finding 5: tuning seeds 11-15 overlap with evaluation seeds 11-20

**Status:** CONFIRMED.

Evidence (from `run_fairness_batch_b01.py:88-89`):

```python
TUNING_SEEDS = [11, 12, 13, 14, 15]
PAIRED_SEEDS = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
```

`set(TUNING_SEEDS) ∩ set(PAIRED_SEEDS) = {11,12,13,14,15}` — exactly 5 seeds leaked from tuning into evaluation.

## Finding 6: only 7 actual non-validation cells, but contract used "9/11 held-out" criterion

**Status:** CONFIRMED.

Evidence (from raw JSON metadata):

- `validation_cells = ['16qam-snr20-fg1000-short', '16qam-snr20-nominal-long', '16qam-snr20-nominal-short', '16qam-snr20-sop40e-short']` (4)
- Held-out (non-validation) = 7 cells
- `batch-contract.v1.yaml:166-168` decision rule: "≥ 9/11 atlas-v1 held-out cells"

9/7 is **mathematically unreachable** (a method can close at most 7 of 7 held-out cells, never 9). Even on the literal atlas set, "9/11 closed" was unreachable because the validation cells overlapped with atlas cells — but the synthesis framed the result as "1/7 closed" while citing the unreachable 9/11 rule.

## Finding 7: single-class cell AUROC is undefined, not 0.5

**Status:** CONFIRMED.

Evidence (from raw JSON aggregate):

| cell | n_label=1 / n_seeds | auroc reported |
|---|---|---|
| snr05-nominal-short | 10/10 | 0.5000 (all positives — single class) |
| snr20-nominal-short | 0/10 | 0.5000 (all negatives — single class) |
| snr25-nominal-short | 0/10 | 0.5000 |
| snr20-fg100-short | 0/10 | 0.5000 |
| snr20-fg1000-short | 0/10 | 0.5000 |
| snr20-sop40e-short | 0/10 | 0.5000 |

6 of 11 cells have a degenerate single-class label distribution. The AUROC there is **mathematically undefined**, not 0.5. Reporting 0.5 inflates the apparent reliability of the metric (it looks like "chance-level detection" when in fact there is nothing to detect).

## Finding 8: degradation onset, warning lead time, PR-AUC, recall@5%FPR, calibration were never actually computed

**Status:** CONFIRMED.

Evidence (raw JSON C05 aggregate keys):

```
['alert_rate', 'auroc_in_cell', 'collapse_label_rate',
 'n_seeds_with_alert', 'n_seeds_with_label_1']
```

Per-seed C05 keys:

```
['alert_any', 'alert_first_block', 'baseline_ratio',
 'detector_score', 'label', 'n_alerts', 'oracle_pi_ser_for_label']
```

`batch-contract.v1.yaml:58` promised `metric_set: [auroc, pr_auc, recall_at_5pct_fpr, false_alarm_rate, warning_lead_time_blocks]` but the runner only emits AUROC + alert_rate + collapse_label_rate. The other four metrics are absent.

## Finding 9: `oracle_pi_ser > 0.3` does NOT equal inner-ring collapse; SNR=5 AWGN-dominated errors must be separated

**Status:** CONFIRMED.

Evidence (from raw JSON snr05-nominal-short per-seed oracle PI-SER):

| seed | nearest | oracle | oracle - nearest |
|---|---|---|---|
| 11 | 0.6758 | 0.7188 | +0.0430 |
| 12 | 0.8281 | 0.8281 | 0 |
| 13 | 0.4219 | 0.4727 | +0.0508 |
| 14 | 0.4922 | 0.4883 | -0.0039 |
| 15 | 0.6016 | 0.6406 | +0.0390 |
| 16 | 0.7812 | 0.8086 | +0.0274 |
| 17 | 0.7148 | 0.7305 | +0.0157 |
| 18 | 0.5586 | 0.5781 | +0.0195 |
| 19 | 0.6992 | 0.7578 | +0.0586 |
| 20 | 0.8477 | 0.8633 | +0.0156 |

All 10 seeds at snr=5 have `oracle_pi_ser > 0.3` (the B01 collapse-label threshold), so B01 labelled all 10 as "collapse". But oracle-affine barely changes PI-SER (mean Δ ≈ +0.027; in 1 seed oracle is even slightly worse). The label is really capturing **AWGN-dominated error**, not inner-ring collapse. An inner-ring collapse seed would show a large `nearest - oracle` gap (oracle recovers it); these snr=5 seeds do not.

## Finding 10: C11's reliable positive signal is actually only 2 held-out long cells, not "three long windows improve 0.01-0.03"

**Status:** CONFIRMED.

Evidence (C11 vs anchor on long cells):

| cell | anchor | C11 | Δ(anchor-C11) | classification |
|---|---|---|---|---|
| snr10-fg100-long (held-out) | 0.4273 | 0.3984 | +0.0289 | held-out, real improvement |
| snr15-fg1000-long (held-out) | 0.3219 | 0.3102 | +0.0117 | held-out, real improvement |
| snr20-nominal-long (**validation**) | 0.3055 | 0.3023 | +0.0031 | **validation cell, not held-out** |

The synthesis claim "long cells improve 0.01-0.03" aggregates 3 cells, but the third (snr20-nominal-long) is the **validation cell** used for tuning C11. So:

- On **held-out** long cells: C11 improves 2/2, magnitudes +0.029 and +0.012. Honest summary: "C11 improves 2/2 held-out long cells."
- The 0.003 improvement on the validation cell is not independent evidence.

The synthesis overreach is writing "three long cells" as if all three were independent.

---

## Summary

All 10 audit findings reproduce. The B01 verdict `PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT` was reached through:

- a non-comparator (frozen-μ anchor standing in for validation-optimal fixed-μ CMA),
- a tuning metric (C05 score) that was structurally disconnected from the tuned parameters,
- a leaky seed split,
- an unreachable exit criterion,
- single-class AUROC misreported as 0.5,
- four promised detector metrics never computed,
- a binary collapse label that conflated AWGN error with inner-ring collapse,
- and a C11 claim that quietly included a validation cell.

B01-R must re-adjudicate with all 10 fixed.
