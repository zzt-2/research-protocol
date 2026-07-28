# Step 020 — Pre-formal Method Factory Sprint 002 (Corrected-baseline causal constellation-prior family)

> Task: T020 (PREFORMAL_METHOD_FACTORY, CP018)
> Date: 2026-07-28
> Status: `DIAGNOSTIC_METHOD_SIGNAL` | mission_method_delta: `METHOD_SIGNAL`
> Claim ceiling: DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE
> Artifacts: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/`

## 1. Task boundary

Diagnostic-only pre-formal method factory sprint 002 (D027, T020). NOT a
Groundwork Step 4a MVE. Did NOT execute/modify T018/Q14. Did NOT update owner,
mission-log, sessions, registry, or master-state. Did NOT modify common/,
params.py, baseline-atlas, or any B01/B01-R/C11/T019 artifact. Did NOT push.

## 2. Testbed selection (Phase A) — 3 identity gates PASS

- **Selected**: CB1 baseline-atlas (reused, frozen). Same generator
  (`generate_shared_realization_dp`), same evaluator
  (`evaluate_dual_16qam`), same 7 held-out cells, same paired-realization rule.
- **Primary baseline**: fixed-μ CMA **μ=0.03** (B01-R hotfix v2 interior
  optimum, `frozen-params-b01r-v1.yaml` best_score=-0.20390625). NOT the
  stale μ=0.001 anchor that V052 rejected in T019.
- **Legal comparators**: blind_affine_compare_16qam (z-only) and
  C11_legal_causal_one_pass (μ=0.03 stage-1, dd_step=1e-4, switch at the
  26%-of-N convergence plateau).
- **Kill-only bound**: oracle_affine_bound_16qam (TX-truth; NEVER a Go
  baseline; used only for offline 4-category labelling).
- **3 identity gates** (all PASS): QPSK regression PI-SER=0.0; eval-population
  identity (baseline produces finite z); prefix-only freeze invariance (re-
  freezing on the same prefix yields bit-identical params for all 4 methods).

## 3. Constructs built (Phase B, 4 mechanism-distinct, TDD)

TDD: 5/5 causality/identity tests written FIRST and PASS before any comparison:
- `test_causality_no_suffix_leakage` — suffix perturbation does not change
  frozen params (V052 fix for T019 M3/M5);
- `test_identity_off_bit_identical_to_baseline` — identity-off = baseline;
- `test_mapping_monotone_m2/m3` — maps are monotone non-decreasing in |z|;
- `test_m4_gate_uses_prefix_only` — M4 gate opens on collapsed prefix only.

| ID | Lever | Action | Smoke |
|----|-------|--------|-------|
| M1 | prefix scalar calibration | one robust global scale, frozen from prefix trim-mean(|z|²) | PASS |
| M2 | prefix quantile transport | monotone CDF→shell map (4 quantiles), frozen from prefix | PASS |
| M3 | prefix three-shell mixture | one-knot piecewise-linear map, frozen from prefix median/p95 | PASS |
| M4 | prefix-gated policy | identity/M2/M3 selected by prefix features only | PASS |

All four implemented as `*_freeze(z_prefix)` + `*_apply_continuous(frozen,
z_suffix)` split. The freeze step reads ONLY the calibration prefix
z[eval_start:calibration_end] (128 symbols); the apply step receives the
scored eval suffix z[calibration_end:eval_end] and never feeds back into any
selection/gate/normalisation. Continuous corrected z is passed to the
evaluator (matches the oracle/continuous convention in cb1_cell_runner.run_cell
lines 371-385, so the evaluator's 8-way rotation/permutation search is
optimal for every method).

## 4. Fair comparison (Phase C) — fresh dev/test seeds, seed-cluster aggregation

- **Dev freeze (C1)**: 3 short cells × 3 dev subseeds (181-183). Tiny prefix-
  only grids: M1 trim_frac ∈ {0.05, 0.1, 0.2} → frozen 0.2; M4
  collapse_threshold × spread_threshold 3×3 → frozen {0.6, 0.1}. M2/M3
  parameter-free. Receipt: `artifacts/dev-freeze-receipt.v1.json`.
- **Test compare (C2)**: 7 cells × 20 fresh test seeds (201-220) = 140 paired
  realizations; 1120 raw rows (`artifacts/raw-rows.v2.csv`).
- **Aggregation**: seed-cluster (each SEED is one independent cluster; the 7
  cells within a seed are NOT 7 independent samples). Per-seed paired delta =
  mean over cells of (method − baseline); cluster bootstrap 10k resamples,
  95% CI on the per-seed mean.

### Result (paired Δ vs μ=0.03 baseline, negative = improvement)

| Construct | mean Δ | 95% CI | help/hurt/tie | healthy worst Δ | gate |
|-----------|-------:|--------|---------------|-----------------|------|
| **M4_gated_policy** | **−0.0826** | **[−0.138, −0.032]** | **7/0/13** | **0.000** | **DIAGNOSTIC_METHOD_SIGNAL** |
| M1_prefix_scalar | −0.0245 | [−0.050, −0.0004] | 11/9/0 | +0.129 | WEAK (healthy-catastrophe) |
| M2_quantile_transport | −0.0612 | [−0.121, −0.006] | 8/12/0 | +0.133 | NO (help<hurt; healthy-catastrophe) |
| M3_three_shell_mixture | +0.2576 | [+0.161, +0.347] | 4/16/0 | +0.672 | NO (catastrophic) |

Comparator seed-cluster mean PI-SER: baseline=0.3143; blind_affine=0.3183;
C11_legal_causal=0.3222. **M4 mean=0.2317 < blind_affine + MDE (0.318+0.005).**

**M4 passes ALL 5 diagnostic gate conditions**: (a) seed-cluster mean Δ ≤ −0.005;
(b) 95% CI upper < 0; (c) help > hurt; (d) no significant regression vs
strongest legal comparator; (e) no catastrophic regression on healthy cells
(worst Δ = 0.000, because the gate selects identity on healthy prefixes).

## 5. Why M4 wins and M1/M2/M3 do not

- **M4's gate is the key safety property**: identity on healthy prefixes
  (13 tie seeds), M2_transport on collapsed prefixes (7 help seeds, 0 hurt).
  Worst healthy Δ = 0.000 — the transport never fires on a healthy cell.
- **M1 fails the healthy gate**: always applies its scale (no identity branch);
  on healthy streams (mean|z|²≈1.37 → scale≈0.73) it shrinks and introduces up
  to +0.129 PI-SER on clean cells. Unsafe.
- **M2 fails help>hurt**: the 4-quantile map is more aggressive than M4's
  gated version; over-corrects on 12 seeds.
- **M3 catastrophically hurts**: its single-knot map forces the prefix median
  onto r_inner=0.447, overshrinking the dominant healthy mode.

The 7 M4 help seeds are concentrated where the baseline μ=0.03 CMA collapses
to the inner ring (PI-SER 0.4-0.77); M4's M2_transport partially recovers
them (typical Δ ≈ −0.20 to −0.25).

## 6. V052 causality gap closure

- T019 M3 selected using [cal, eval_end] (eval window itself) → causality leak.
- T019 M5 used whole-eval-window power statistics then re-judged that window →
  causality leak.
- Sprint 002 fixes both: every method's freeze step reads ONLY the prefix
  z[eval_start:calibration_end]; the apply step receives the suffix and never
  feeds back. Verified by `test_causality_no_suffix_leakage` (perturbing the
  suffix does not change any method's frozen params).
- Also fixed: smoke results are persisted in the SAME terminal result artifact
  as the comparison (T019's `result.v1.json` had `smoke_results={}` because
  `--compare` clobbered `--smoke`).

## 7. Acceptance check

- [x] control validator PASS; worktree clean at start
- [x] current baseline is μ=0.03 (no historical anchor regression)
- [x] ≥3 new methods actually ran (4 ran)
- [x] prefix/eval causal isolation tests PASS (5/5 TDD)
- [x] dev/test seeds fresh, disjoint, frozen (181-190 dev / 201-220 test)
- [x] raw/aggregate use seed-cluster as the independent unit
- [x] smoke written into terminal result (NOT clobbered)
- [x] 4-category labels used only for offline explanation
- [x] normal-terminal method delta is METHOD_SIGNAL (not NONE)
- [x] no third-package suggestion, no formal/paper overreach
- [x] owner/mission/session files not updated
- [x] only authorized paths committed; no push

## 8. Verdict

`DIAGNOSTIC_METHOD_SIGNAL` (M4_gated_policy). 4 strictly-causal prefix-only
constructs built, fairly compared under the corrected μ=0.03 baseline with
fresh disjoint dev/test seeds; one winner (M4) satisfies all 5 diagnostic gate
conditions. Per D027 this is a legitimate terminal state; M4 is a diagnostic
winner, NOT a formal Groundwork Go (claim ceiling = DIAGNOSTIC_ONLY).

## 9. Caveats (claim ceiling)

1. The baseline μ=0.03 CMA itself collapses on many high-SNR seeds. M4's gain
   is partial recovery of an already-collapsed z-stream, not a fix to the
   equalizer.
2. blind_affine underperforms the baseline (0.318 vs 0.314); the 2×2 complex
   affine overfits the prefix. M4's simpler gated map is more robust, but
   operates in a regime where the "strongest legal comparator" is itself weak.
3. 20 test seeds give a tight CI for M4 but the 7/0/13 help/hurt/tie split is
   seed-clustered; the CI upper bound being clearly negative is the stronger
   evidence.
4. Diagnostic only. To promote M4, formal Groundwork Step 1-3/3.5/4a (full
   literature, novelty check, different testbed) would be required.
