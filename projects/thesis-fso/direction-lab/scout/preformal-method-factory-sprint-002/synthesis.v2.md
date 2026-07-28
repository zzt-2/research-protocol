# Pre-formal Method Factory Sprint 002 — Synthesis

> Schema: `direction-lab.preformal-method-factory-sprint-002.v2`
> Authority: T020 / D027 / V052
> Date: 2026-07-28
> Status: **`DIAGNOSTIC_METHOD_SIGNAL`** | mission_method_delta: **`METHOD_SIGNAL`**
> Claim ceiling: **DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE**
> Winner: **M4_gated_policy** (prefix-gated identity/M2-transport policy)
> Artifacts: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/`

## 0. TL;DR

In one corrected-baseline package, four strictly-causal prefix-only public-
constellation-prior shell-distribution methods were built (TDD: 5/5 causality
+ identity tests PASS first), fairly compared against the current fair baseline
(μ=0.03 fixed-μ CMA, NOT the stale μ=0.001 anchor) and the two legal receiver-
visible comparators (blind-affine, C11-legal-causal), on 7 held-out cells × 20
fresh disjoint test seeds.

**M4 (prefix-gated identity/M2-transport policy) is a DIAGNOSTIC_METHOD_SIGNAL**:
seed-cluster mean ΔPI-SER = −0.0826 vs μ=0.03 CMA, 95% CI = [−0.138, −0.032],
7 help seeds / 0 hurt seeds / 13 tie seeds, no significant regression vs the
strongest legal comparator (blind-affine 0.318 vs M4 0.232), and NO catastrophic
regression on healthy cells (healthy-cluster worst Δ = 0.000).

M1 (prefix scalar calibration) is WEAK: −0.024 mean Δ, CI barely negative
(upper −0.00039), but **fails the healthy-cluster regression gate** (worst
+0.129 on healthy pairs) — it shrinks healthy streams and is unsafe to deploy.

M2 (quantile transport) and M3 (three-shell mixture) are NO_SIGNAL: M2 has a
negative CI but help < hurt (8/12); M3 catastrophically hurts (+0.258 mean Δ)
because its single-knot map overshrinks the dominant mode.

This closes the V052 causality gap (M3/M5 of T019 used eval-window statistics),
fixes the baseline (μ=0.03 not μ=0.001), and produces the first DIAGNOSTIC
winner in the CB1 method-factory campaign.

## 1. Boundary

Diagnostic-only pre-formal method factory sprint (D027). NOT a Groundwork
Step 4a MVE. Did NOT execute/modify T018/Q14, common/, params.py, baseline-
atlas, B01/B01-R/C11 raw, or any owner/session file. Did NOT push.

## 2. Phase A — Testbed identity gates (all PASS)

| Gate | Property | Result |
|---|---|---|
| qpsk_regression | QPSK PI-SER = 0.0 at μ=0.03 | PASS |
| eval_population_identity | baseline produces finite z on held-out cell/seed | PASS |
| prefix_only_freeze_invariance | re-freezing on the same prefix yields bit-identical frozen params for all 4 methods | PASS |

The μ=0.03 fixed-μ CMA implementation (`cb1_cell_runner.standard_cma_godard_with_z`)
is byte-identical to the B01-R hotfix v2 fixed_mu_cma_validation_optimal
comparator; μ is inherited from `frozen-params-b01r-v1.yaml` (best_score=
-0.20390625), NOT re-tuned.

## 3. Phase B — Constructs built (4 mechanism-distinct)

| ID | Lever | Action | Smoke |
|----|-------|--------|-------|
| M1 | prefix scalar calibration | one robust global scale, frozen from prefix trim-mean(|z|²) | PASS |
| M2 | prefix quantile transport | monotone CDF→shell map (4 quantiles), frozen from prefix | PASS |
| M3 | prefix three-shell mixture | one-knot piecewise-linear map, frozen from prefix median/p95 | PASS |
| M4 | prefix-gated policy | identity/M2/M3 selected by prefix features only | PASS |

All four implemented as freeze/apply split (freeze reads prefix only; apply
receives suffix). No `common/`, `params.py`, or baseline-atlas modification.
No privileged/future/TX-truth input at deploy time (oracle used only for
offline 4-category labelling + Kill bound).

## 4. Phase C1 — Dev freeze (prefix-only tiny grid)

Dev pool: 3 short cells × 3 dev subseeds (181-183). Tiny grids:
- M1 trim_frac ∈ {0.05, 0.1, 0.2} → frozen 0.2 (best dev Δ = −0.0230)
- M4 collapse_threshold ∈ {0.4, 0.5, 0.6} × spread_threshold ∈ {0.1, 0.15, 0.2}
  → frozen {0.6, 0.1} (best dev Δ = −0.0152; the gate is closed at ct≤0.5,
  open at ct=0.6 where it picks up the deepest collapse signatures)
- M2/M3 parameter-free (closed-form from prefix)

Receipt: `artifacts/dev-freeze-receipt.v1.json`. Test seeds never observed
during dev.

## 5. Phase C2+D — Test paired comparison (7 cells × 20 test seeds = 140 realizations)

### Result (paired Δ vs μ=0.03 baseline, negative = improvement; seed-cluster)

| Construct | mean Δ | 95% CI | help/hurt/tie | healthy worst Δ | gate |
|-----------|-------:|--------|---------------|-----------------|------|
| **M4_gated_policy** | **−0.0826** | **[−0.138, −0.032]** | **7/0/13** | **0.000** | **DIAGNOSTIC_METHOD_SIGNAL** |
| M1_prefix_scalar | −0.0245 | [−0.050, −0.0004] | 11/9/0 | +0.129 | WEAK (healthy-catastrophe) |
| M2_quantile_transport | −0.0612 | [−0.121, −0.006] | 8/12/0 | +0.133 | NO (help<hurt; healthy-catastrophe) |
| M3_three_shell_mixture | +0.2576 | [+0.161, +0.347] | 4/16/0 | +0.672 | NO (catastrophic) |

Comparator seed-cluster mean PI-SER: baseline (μ=0.03) = 0.3143; blind_affine =
0.3183; C11_legal_causal = 0.3222. **M4 mean = 0.2317 < blind_affine + MDE.**

### Why M4 wins and M1/M2/M3 do not

- **M4's gate is the key safety property**: it selects identity on healthy
  prefixes (13 tie seeds = healthy/clean) and M2_transport on collapsed
  prefixes (7 help seeds). Because identity is bit-identical to the baseline,
  healthy cells NEVER regress (worst Δ = 0.000). The transport only fires when
  the prefix collapse signature is unambiguous (mean|z|² < 0.6 AND spread ≥ 0.1).
- **M1 fails the healthy gate**: it ALWAYS applies its scale (no identity
  branch). On healthy streams mean|z|² ≈ 1.37 → scale ≈ 0.73 → shrinks the
  stream → introduces up to +0.129 PI-SER on clean cells. Unsafe.
- **M2 fails the help>hurt gate**: the 4-quantile map is more aggressive than
  M4's gated version; on 12 seeds it over-corrects and hurts.
- **M3 catastrophically hurts**: its single-knot map forces the prefix median
  onto r_inner=0.447, overshrinking the dominant healthy mode.

### 4-category collapse labels (offline, oracle-only; not deployment)

Across the 7 cells × 20 test seeds, the offline oracle labelling (LABEL ONLY,
never influencing deployment) categorises the population:
- snr15-nominal-short, snr25-nominal-short, snr20-fg100-short → mostly healthy
- snr05-nominal-short, snr10-nominal-short, snr10-fg100-long, snr15-fg1000-long
  → AWGN-dominated / inner-ring-recoverable mix

The 7 M4 help seeds are concentrated in the AWGN/collapse-recoverable cells
where the baseline μ=0.03 CMA collapses to the inner ring (PI-SER 0.4-0.77);
M4's M2_transport partially recovers them (typical Δ ≈ −0.20 to −0.25).

## 6. Acceptance check

- [x] current baseline is μ=0.03 (no historical anchor regression)
- [x] ≥3 new methods actually ran (4 ran: M1/M2/M3/M4)
- [x] prefix/eval causal isolation tests PASS (5/5 TDD tests)
- [x] dev/test seeds fresh, disjoint, frozen (181-190 dev / 201-220 test)
- [x] raw/aggregate use seed-cluster as the independent unit
- [x] smoke written into terminal result (NOT clobbered by compare)
- [x] 4-category labels used only for offline explanation
- [x] normal-terminal method delta is non-NONE (METHOD_SIGNAL)
- [x] no third-package suggestion, no formal/paper overreach
- [x] only authorized paths committed, no push

## 7. Caveats and limits (claim ceiling = DIAGNOSTIC_ONLY)

1. **The baseline μ=0.03 CMA itself collapses on many high-SNR seeds** (e.g.
   snr25 seed 215 → PI-SER 0.75). M4's "gain" is partial recovery of an
   already-collapsed z-stream by a z-only transport. This does NOT fix the
   equalizer; it post-processes its failure. The formal Groundwork must
   re-establish whether the collapse is the real research problem.
2. **blind_affine underperforms the baseline** (0.318 vs 0.314). This means
   the 2×2 complex affine overfits the prefix and generalises poorly to the
   eval slice. M4's simpler gated single-scalar/quantile map is more robust,
   but this also means M4 is operating in a regime where even the "strongest
   legal receiver-visible comparator" is weak. A formal comparator audit
   would be required before any paper claim.
3. **20 test seeds** give a usefully tight CI for M4 ([−0.138, −0.032]), but
   the help/hurt split (7/0/13) is seed-clustered; a different 20 seeds could
   shift the help count. The CI upper bound being clearly negative is the
   stronger evidence.
4. **Diagnostic only**. M4 is NOT a formal Groundwork Go. To promote it,
   one would need to (a) re-establish the research problem (collapse vs
   AWGN), (b) run a formal Step 1-3/3.5/4a with full literature coverage and
   novelty check, (c) verify on a different testbed. Per D027 this is the
   explicit next-formal-action ONLY if M4 is promoted.

## 8. Verdict

`DIAGNOSTIC_METHOD_SIGNAL` (M4_gated_policy). 4 constructs built, fairly
compared under the corrected μ=0.03 baseline with strict prefix-only causality
and fresh disjoint seeds; one winner (M4) satisfies all 5 diagnostic gate
conditions, one weak (M1, fails healthy gate), two no-signal (M2/M3).

Per D027, this is a legitimate terminal state. M4 may be returned to formal
Groundwork Step 1-3/3.5/4a if the diagnostic signal warrants a formalization
investment; otherwise the CB1 z-only/post-processing axis continues with M4
as the new strongest receiver-visible comparator for any future learned
corrector.
