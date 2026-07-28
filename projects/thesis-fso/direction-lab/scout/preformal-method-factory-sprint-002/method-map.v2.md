# Method Map — Sprint 002 (Corrected-baseline causal constellation-prior family)

> Schema: direction-lab.preformal-method-factory-sprint-002.v2
> Date: 2026-07-28
> Authority: T020 / D027 / V052

## Common information source (all 4 constructs)

All four constructs read ONLY:
1. **calibration prefix** z[eval_start:calibration_end] (128 symbols, receiver-visible)
2. **public 16QAM alphabet geometry**: per-axis amplitudes {-3,-1,+1,+3}/√10,
   avg-power-normalized (E[|s|²]=1); three |s|² shells {0.2, 1.0, 1.8} with
   public occupancy {0.25, 0.50, 0.25}; shell radii {0.4472, 1.0, 1.3416}.
3. **frozen public receiver parameters** (FROZEN_AXES in run_factory.py).

The scored eval suffix z[calibration_end:eval_end] is NEVER read by any
freeze/gate/selection step; it only receives the FROZEN transform at apply time.

---

## M1: Prefix scalar calibration

- **deployable_action**: freeze ONE robust global scale from the prefix
  `scale = E[|s|²] / trimmed_mean(|z_prefix|²)` (trim_frac=0.2, dev-frozen);
  apply `z' = scale · z_suffix` then let the evaluator hard-decide.
- **prefix_input**: prefix |z|² (trimmed mean).
- **frozen_params**: `{trim_frac: 0.2}` (dev-frozen from grid {0.05, 0.1, 0.2}).
- **difference from T019 M5/C15/C14/blind_affine**:
  - T019 M5 remap was a per-symbol nearest-shell rescale of the EVAL suffix
    (collapsed detection used the eval window itself → causality leak, V052).
    M1 estimates a single global scale from the PREFIX only; the suffix is
    only multiplied by the frozen scale.
  - blind_affine fits a 2×2 complex affine (4 complex params) on the prefix;
    M1 fits a single real scalar (1 real param). Far fewer params → more
    robust to prefix→eval distribution shift, but cannot correct phase/rotation.
- **primary_thesis_packaging_draft**: "prefix-estimated robust scalar
  rescaling of block-end CMA output for inner-ring collapse recovery".
- **fallback_thesis_packaging_draft**: "single-parameter closed-form
  rescaling baseline; bounds the recoverable gap that any affine/transport
  method must beat to claim added value".

## M2: Prefix quantile shell transport

- **deployable_action**: build a monotone piecewise-linear map from the prefix
  |z| CDF onto the public 16QAM shell radii at the theoretical
  0.25/0.50/0.25 occupancy. Apply the FROZEN map to suffix |z| (phase preserved).
- **prefix_input**: prefix |z| quantiles at {0.125, 0.375, 0.625, 0.875}.
- **frozen_params**: `{map_x, map_y}` (closed-form from prefix; no grid).
- **difference from T019 M5/C15/C14/blind_affine**:
  - T019 M5 rescaled each suffix symbol to its nearest shell (eval-window
    statistics). M2 builds the map from the PREFIX CDF; the suffix only
    receives the frozen monotone map. Phase is preserved (z' = (r_out/r_in)·z),
    so M2 cannot introduce phase errors; it only redistributes |z|.
  - C14/C15 are equalizer-cost variants (re-run CMA); M2 is a post-proc map.
- **primary_thesis_packaging_draft**: "prefix-quantile optimal-transport
  radius calibration against the public 16QAM shell distribution".
- **fallback_thesis_packaging_draft**: "CDF-matching radius calibration;
  illustrates the recoverable gap that an adaptive equalizer could capture".

## M3: Constrained three-shell mixture calibration

- **deployable_action**: fit a one-knot piecewise-linear monotone map
  constrained by public shell radii on the prefix |z| histogram. Below the
  median knot: rescale onto [0, r_inner]; above: onto [r_inner, r_outer].
- **prefix_input**: prefix |z| histogram (median + 95th percentile).
- **frozen_params**: `{knots, values}` (closed-form; no grid).
- **difference from T019 M5/C15/C14/blind_affine**:
  - M3 uses a single knot (the prefix |z| median) to separate collapsed vs
    healthy symbols; M2 uses 4 quantiles. M3 is a coarser, single-mode
    calibration; M2 is a finer, multi-mode calibration.
- **primary_thesis_packaging_draft**: "prefix-mixture one-knot monotone
  calibration for bimodal collapse recovery".
- **fallback_thesis_packaging_draft**: (negative control; demonstrates that
  a too-coarse single-knot map overshrinks healthy symbols).

## M4: Prefix-gated identity/transport policy

- **deployable_action**: use ONLY prefix features (mean |z|², std |z|
  coefficient-of-variation) to select identity / M2 / M3. Gate frozen on dev
  seeds (collapse_threshold=0.6, spread_threshold=0.1, dev-frozen); test
  unchanged.
- **prefix_input**: prefix scalar features {mean_abs2, spread}.
- **frozen_params**: `{collapse_threshold: 0.6, spread_threshold: 0.1,
  policy_rule}` (dev-frozen from a 3×3 grid).
- **difference from T019 M5/C15/C14/blind_affine**:
  - M4 is the only method that conditionally applies NO correction (identity)
    on healthy prefixes, guaranteeing zero regression on healthy cells.
    M1/M2/M3 always apply their (mildly-shrinking) correction.
  - blind_affine always applies its 2×2 affine; M4 only fires M2/M3 when the
    prefix collapse signature is detected.
- **primary_thesis_packaging_draft**: "prefix-gated selective radius
  calibration: identity on healthy prefixes, optimal-transport on collapsed
  prefixes, for safe inner-ring collapse recovery".
- **fallback_thesis_packaging_draft**: "a receiver-visible collapse detector
  enabling conditional post-processing, bounding the deployable gain of any
  learned corrector that must not regress healthy cells".

---

## Causality discipline (V052 fix)

Each construct is split into `*_freeze(z_prefix)` (returns frozen params) and
`*_apply_continuous(frozen, z_suffix)` (applies the frozen transform). The
freeze step is deterministic given the prefix; the apply step never feeds back
into any selection. Verified by 5/5 TDD tests:
- `test_causality_no_suffix_leakage` — perturbing the suffix does NOT change
  frozen params (any of M1/M2/M3/M4).
- `test_identity_off_bit_identical_to_baseline` — with correction disabled,
  each method is bit-identical to hard_16qam(z_suffix).
- `test_mapping_monotone_m2` / `test_mapping_monotone_m3` — the M2/M3 maps
  are monotone non-decreasing in |z|.
- `test_m4_gate_uses_prefix_only` — M4 gate opens on collapsed prefix and
  closes on healthy prefix.

## Continuous-z evaluation convention

Methods return CONTINUOUS corrected z (not pre-hard-decided symbols); the
evaluator `evaluate_dual_16qam` does its own hard decision + 8-way
rotation/permutation search. This matches the oracle/continuous convention in
`cb1_cell_runner.run_cell` (lines 371-385), ensuring the rotation/permutation
ambiguity is resolved optimally for every method including the new ones.
