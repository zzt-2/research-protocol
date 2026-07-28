# Pre-formal Method Factory Sprint 001 — Method Map v1

> Diagnostic-only. Each construct targets the **same frozen failure mechanism**:
> block-end gradient-descent CMA/MMA inner-ring collapse on 16QAM dual-pol OSL.
> The oracle affine proves the information is recoverable; the failure is in the
> *adaptive trajectory*, not the information. Each construct below attacks a
> *different step* of the receiver pipeline using only receiver-visible, causal
> inputs.

## Shared failure-mechanism model (from baseline-adjudication synthesis)

The standard-CMA block-end update (block_size=64, μ=0.001) collapses ~40-60% of
seeds to an inner-ring local minimum (|z|²≈0.16-0.3, n_unique=4 instead of 16)
on 16QAM. The collapse is:
- **seed-and-trajectory dependent** (not length-dependent; invariant to N);
- **information-recoverable** (oracle affine on TX truth recovers PI-SER≈0);
- **visible in the causal CMA trace** (output_power, w_norm, cm_error,
  update_norm, z_amp_max per block all show the collapse signature).

So there are five receiver-visible lever points, each addressable by a
mechanism-distinct construct **without** touching TX truth, the channel, or the
future window.

## Construct registry

| ID | Mechanism family | Receiver step changed | Deployable action (one line) |
|----|------------------|-----------------------|------------------------------|
| M1 | Robust cost / update law | CMA cost surface | Replace constant-modulus Godard cost with a reduced-modulus cost that has no inner-ring spurious minimum on the 16QAM alphabet |
| M2 | Causal state scheduling | Block-end update trigger | Detect collapse signature in the causal CMA trace and re-initialize the filter from a diversity seed when detected (online, causal) |
| M3 | Multi-start + receiver-visible selection | Initialization + selection | Run K parallel CMA seeds from diverse center-tap perturbations, pick the one whose converged output has the receiver-visible 16QAM-consistency metric closest to the public alphabet |
| M4 | Conditional cascade of conventional modules | Post-equalization refinement | Conditional one-step decision-directed (DD) affine refinement, applied only when the causal trace flags residual modulus mismatch |
| M5 | Low-complexity post-processing | Output remapping | Closed-form radius-aware remap that pushes collapsed inner-ring clusters back toward the nearest valid 16QAM radius shell, using only the public alphabet and the receiver-visible |z| distribution |

All five are **mechanism-distinct** (cost / scheduling / multi-start / cascade /
post-processing), all use only receiver-visible causal inputs, and all share the
frozen (cell, seed) realization via `generate_shared_realization_dp`.

---

## M1 — Reduced-modulus CMA (robust cost / update law)

- **mechanism**: changes the CMA *cost surface*. Standard Godard (R²=1.32) has a
  spurious inner-ring attractor on 16QAM because its single modulus is
  incompatible with the three distinct |s|² shells (0.2, 1.0, 1.8). M1 replaces
  the cost with a *reduced-modulus* variant that targets the **inner** radius
  shell only (R²=R_inner²), removing the inner-ring attractor entirely. This is
  the dual of MMA (which splits real/imag) but acts on the *modulus* axis and
  stays in the constant-modulus update family.
- **deployable_action**: block-end gradient descent with cost
  `J = E[(R_inner² − |z|²)²]`, `R_inner² = E[|s_inner|⁴]/E[|s_inner|²]` derived
  analytically from the public 16QAM alphabet (the inner-shell symbols). Same
  μ, n_tap, block_size, init as frozen baseline. No TX truth.
- **receiver_visible_inputs**: rX, rY, known 16QAM alphabet (for R_inner²).
- **cheap_alternative**: blind_affine_16qam (shared).
- **difference_from_rejected_axes**: NOT MMA (MMA splits real/imag modulus; M1
  keeps constant-modulus but changes R² to the inner shell). NOT adaptive
  phase-window (step-007/008 KILL). NOT pilot→Jones (step-002 KILL). M1 is a
  cost-surface edit on the *same* block-end gradient family as the frozen
  baseline, with an analytically-derived (not tuned) dispersion constant.
- **primary_packaging** (draft): "Reduced-modulus CMA removes the inner-ring
  spurious minimum of constant-modulus equalization on square QAM by targeting
  the inner radius shell, recovering collapsed seeds without TX truth."
- **fallback_packaging** (draft): "A radius-shell cost selection rule that
  trades one shell's optimality for collapse-robustness on dual-pol OSL."

## M2 — Trace-driven causal re-initialization (causal state scheduling)

- **mechanism**: changes the *update trigger*. The collapse is visible in the
  causal CMA trace (output_power collapses below the inner-shell power,
  cm_error plateaus, w_norm stalls). M2 monitors these causal features online
  and, on detecting the collapse signature, re-initializes the filter weights
  from a diversity perturbation and continues. No look-ahead.
- **deployable_action**: after each block-end update, compute a receiver-visible
  collapse score from the trace (e.g. output_power / R_inner² ratio and
  z-constellation entropy proxy n_unique_clusters); if score crosses a frozen
  threshold for >= T_consecutive blocks, reset w to a center-tap + fixed
  off-center perturbation and continue adapting. Threshold frozen BEFORE running
  from the alphabet's inner-shell power (no tuning to seeds).
- **receiver_visible_inputs**: zX/zY (current), cma_trace (causal history),
  known alphabet (for power ratio threshold).
- **cheap_alternative**: M1 (if M1 removes the attractor, M2's re-init is
  unnecessary — run M1 once, shared where applicable).
- **difference_from_rejected_axes**: NOT adaptive phase-window (different
  observable — trace entropy/power, not phase innovation). NOT B10 source-native
  RLS (different algorithm class — M2 keeps block-end CMA, only adds a causal
  re-init trigger). The *new deployable action* is the causal collapse-detector
  + diversity re-init, not a new equalizer.
- **primary_packaging** (draft): "Causal collapse detection from the CMA trace
  enables online recovery of inner-ring collapsed seeds via diversity re-init,
  using only receiver-internal features."
- **fallback_packaging** (draft): "A receiver-internal health monitor that
  flags convergence-pathology in real time, even when the corrective action is
  conservative."

## M3 — Multi-start CMA with receiver-visible selection (multi-start + selection)

- **mechanism**: changes *initialization + selection*. The collapse is
  trajectory-dependent: a single center-tap init lands ~40-60% of seeds in the
  inner ring. M3 runs K parallel CMA instances from diverse init perturbations
  and picks the converged output whose z-stream best matches the public 16QAM
  alphabet geometry (a receiver-visible consistency score, no TX truth).
- **deployable_action**: K=4 parallel block-end CMA runs (same μ/block/n_tap,
  different init: center-tap, +off-center-X, +off-center-Y, anti-center).
  Selection score = mean squared deviation of |z|² from the public 16QAM
  |s|² distribution moments (receiver-visible, alphabet-derived). Pick argmin.
- **receiver_visible_inputs**: rX, rY (each parallel run), known alphabet
  (for selection score moments).
- **cheap_alternative**: blind_affine_16qam (shared); M1 (shared where applicable).
- **difference_from_rejected_axes**: NOT B1 adaptive window (M3 does not adapt
  window length; it adapts *which trajectory*). The new deployable action is the
  parallel-diversity-init + receiver-visible geometry selection, which is absent
  from all rejected axes.
- **primary_packaging** (draft): "Diversity-initialized multi-start CMA with
  alphabet-geometry selection escapes the inner-ring local minimum that
  single-init block-end CMA falls into on 16QAM dual-pol OSL."
- **fallback_packaging** (draft): "A selection rule showing that the
  information to recover collapsed seeds is present at init time, quantifying
  the cost of single-init brittleness."

## M4 — Conditional DD affine cascade (conditional cascade of conventional modules)

- **mechanism**: changes *post-equalization refinement*. After CMA converges
  (or collapses), M4 applies a single closed-form decision-directed affine
  refinement, but *only* on blocks where the causal trace flags residual modulus
  mismatch. This is the cheap-extension slot from batch-contract.v1.yaml,
  activated conditionally (the contract noted it was not triggered for MMA
  because MMA's failure was divergence, not under-convergence — but CMA's
  collapse IS an under-convergence-style pathology that DD can address).
- **deployable_action**: on the calibration slice, fit a 2x2 complex affine map
  from z to z's own 16QAM hard decisions (DD), apply to eval. Conditional: only
  fit/apply when the calibration-slice collapse score (receiver-visible) exceeds
  threshold; otherwise pass through (identity = frozen baseline).
- **receiver_visible_inputs**: zX/zY calibration + eval, known alphabet
  (hard decisions are public-knowledge), causal trace (for the condition).
- **cheap_alternative**: blind_affine_16qam (M4 is its conditional DD analogue;
  run blind_affine once, shared).
- **difference_from_rejected_axes**: NOT a unconditional DD-LMS cascade (the
  contract's cheap-extension was unconditional and untriggered). M4's new
  deployable action is the *causal-trace-gated* conditional application — it
  degrades to identity (= frozen baseline) on non-collapsed blocks, so it cannot
  hurt clean cells.
- **primary_packaging** (draft): "Trace-gated decision-directed affine cascade
  recovers collapsed CMA outputs by correcting the residual affine mismatch,
  applied only where the causal trace diagnoses collapse."
- **fallback_packaging** (draft): "A gated post-processor showing the
  information-recoverability of the collapse holds under a same-information
  DD refinement, bounded by a causal health gate."

## M5 — Radius-shell remap (low-complexity post-processing)

- **mechanism**: changes *output remapping*. Collapsed z-streams cluster on an
  inner radius ring (|z|²≈0.16-0.3) instead of the 16QAM shells. M5 computes
  the receiver-visible |z| distribution, identifies the dominant collapsed
  radius, and applies a closed-form per-symbol complex scaling that maps the
  collapsed cluster to the nearest valid 16QAM radius shell before hard
  decision. No adaptive loop, no TX truth.
- **deployable_action**: on the eval slice, estimate the collapsed radius
  r_collapse = median(|z|) (receiver-visible); for each symbol, scale
  z -> z · (r_target / r_collapse) where r_target is the public 16QAM shell
  nearest to |z|·(r_target/r_collapse) (fixed-point iteration, 2 steps); hard
  decision. All from |z| + public alphabet.
- **receiver_visible_inputs**: zX/zY eval, known alphabet (shell radii).
- **cheap_alternative**: blind_affine_16qam (shared).
- **difference_from_rejected_axes**: NOT pilot→Jones (M5 does not invert a
  channel; it remaps the output radius). NOT adaptive window. The new
  deployable action is the receiver-visible radius-shell remap, a non-adaptive
  post-processor absent from all rejected axes.
- **primary_packaging** (draft): "Radius-shell remap corrects inner-ring
  collapsed CMA outputs by re-anchoring the receiver-visible |z| distribution to
  the public 16QAM shell geometry, with no adaptive loop."
- **fallback_packaging** (draft): "A zero-parameter post-processor that
  quantifies how much of the collapse gap is pure radius bias vs angular
  distortion."

---

## Construct-to-lever coverage

| Lever point (receiver-visible) | M1 | M2 | M3 | M4 | M5 |
|--------------------------------|----|----|----|----|----|
| Cost surface (modulus)          | ✓  |    |    |    |    |
| Update trigger (scheduling)     |    | ✓  |    |    |    |
| Initialization + selection      |    |    | ✓  |    |    |
| Post-eq affine (cascade)        |    |    |    | ✓  |    |
| Output radius (post-processing) |    |    |    |    | ✓  |

Every construct occupies a distinct lever; no two share a primary mechanism.
All five are implementable as adapters over `cb1_cell_runner.run_cell` /
`cb1_evaluator`, reusing the frozen generator and evaluator without
modification.
