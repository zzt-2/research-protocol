# Research Direction Lab Status
# Updated 2026-07-22 after continuous campaign round (4 Probes + 5 Scouts).

## 1. Formal Goal and Authorization

- Goal: identify legal ML information increment in the complete dual-pol ground-to-satellite OSL receiver chain
- Authorization: SCIENCE_SCOUT (continuous multi-mechanism campaign)
- Prohibits: modify protected history, create legacy B004, auto-write Scout numbers into paper, bypass formal promotion, push/merge

## 2. Anchor or Baseline

- Scenario: dual-polarization ground-to-satellite OSL under Gamma-Gamma turbulence and SOP dynamics
- Baseline: baseline.standard_cma.godard_z (with Godard z factor)
- Metrics: fixed_label_ber + permutation_invariant_ber

## 3. Portfolio and Blocked Axes

- 16 candidates (C01-C16); 5 axes now CLOSED (correction, adaptation, cost, init, paradigm)
- Blind-equalization solution space exhausted across all 5 mechanism axes
- Only remaining open axis: model-based tracker (rank-4, requires ~1 day infra + user strategy decision)
- Full map: portfolio/current.yaml

## 4. Latest Completed Scientific Result

- **C16 non-modulus HOS** (2026-07-22): kurtosis-maximization source separation (no modulus term) is WORSE than CMA (macro PI-SER 0.466 vs 0.251; collapse rate 0.791 vs 0.336). The collapse is NOT a modulus-cost local minimum — it's a channel property. Closes the paradigm axis.
- **C15 ring-aware cost** (2026-07-22): ring-matching INCREASES collapse (self-consistent with collapsed state; error drops 19×). Combined with MMA, rules out both geometric decompositions.
- **C14 data-driven init** (2026-07-22): collapse init-independent; oracle Wiener init collapses on all collapsed seeds; data-driven init strictly worse.
- **C04/C09 O1-corrected** (2026-07-22): objective fix confirmed (input-dependent optimum), but context-dependence has no value over ridge-LS; route CLOSED.
- **C12 GMI soft-output** (2026-07-22): zero oracle headroom; GMI loss is equalizer-bound; reusable GMI evaluator produced.

## 5. Current Mode

- Mode: awaiting strategy — blind-eq solution space exhausted; escalation to model-based tracker or accept negative-boundary thesis
- The negative-boundary thesis ("collapse is a fundamental property of blind equalization on this channel") is evidence-backed across 5 axes and publishable

## 6. Thesis Harvest (current view)

- **H060 (PRIMARY)**: collapse is a channel property surviving 5 mechanism axes — complete boundary characterization
- H061-H065: per-axis mechanism negatives (affine, GMI, init, cost, paradigm)
- H066: detector structural ceiling
- H067-H068: reusable assets (GMI evaluator, HOS equalizer)
- Prior: C11 no-benefit, TX-truth bound, blind-affine harmful, MMA<CMA, CB1 deep property
- Full: harvest/current.yaml

## 7. Next Automatic Action

No automatic scientific runner remains in the blind-equalization space. The model-based tracker (rank-4) requires user strategy decision (material compute investment). Alternatively, accept the negative-boundary thesis and move to formal Groundwork/Contract/Execute promotion.

## 8. Strategy Escalation Condition

Choose: (a) invest ~1 day in model-based GG+SOP tracker (only remaining positive-potential axis), or (b) accept negative-boundary thesis as primary contribution and enter formal promotion, or (c) change formal goal/contribution line.

## Detail Pointers

- Current state: projects/thesis-fso/direction-lab/state/current.yaml
- Portfolio: projects/thesis-fso/direction-lab/portfolio/current.yaml
- Harvest: projects/thesis-fso/direction-lab/harvest/current.yaml
- Probes: projects/thesis-fso/direction-lab/probes/p01-p05
- Scouts: projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c*-scout
