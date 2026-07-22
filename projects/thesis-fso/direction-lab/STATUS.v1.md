# Research Direction Lab Status
# Updated 2026-07-22 S011/D017/V006 — e15ae60 reconciliation + hybrid-routing study entry.
# IMPORTANT (D017): the prior "5 axes exhausted / collapse is a channel property" global
# narrative from commit e15ae60 is INVALIDATED. Numbers reproducible; scientific semantics
# failed on C12/C14/C15/C16 + seeds 71-80 lost held-out status. See harvest amendments.

## 1. Formal Goal and Authorization

- Goal: identify legal ML information increment in the complete dual-pol ground-to-satellite OSL receiver chain
- Authorization: SCIENCE_SCOUT (continuous multi-mechanism campaign)
- Prohibits: modify protected history, create legacy B004, auto-write Scout numbers into paper, bypass formal promotion, push/merge

## 2. Anchor or Baseline

- Scenario: dual-polarization ground-to-satellite OSL under Gamma-Gamma turbulence and SOP dynamics
- Baseline: baseline.standard_cma.godard_z (with Godard z factor)
- Metrics: fixed_label_ber + permutation_invariant_ber

## 3. Portfolio and Blocked Axes

- 16 candidates (C01-C16) + hybrid-routing family (new, S011)
- **D017 CORRECTION**: the "5 mechanism axes CLOSED / space exhausted" global claim is INVALIDATED. Per-axis validity after V006:
  - C04/C09 affine correction → UNRESOLVED (O1 target still self-referential, constant-collapse optimum)
  - C12 GMI soft-output → scale-artifact (not a true bound); H062 WITHDRAWN
  - C14 init → scope-narrow (proves only strongest-single-init collapses; H063)
  - C15 cost → unequal-step-confounded (19× gradient, shared μ=0.03); H064 WITHDRAWN
  - C16 non-modulus HOS → NOT a legal capability-aligned expert (spatial 2×2, no FIR); H065 reclassified
  - seeds 71-80 → LOST held-out status (reused in ≥6 batches)
- **New open family**: collapse-aware hybrid equalizer routing (legal FIR-aligned experts)
- Full map: portfolio/current.yaml

## 4. Latest Completed Scientific Result

- **S011/D018/V007 (2026-07-22)**: hybrid-routing Macro A → VERDICT C (COMPLEMENTARITY_INVALID). Legal FIR experts (MMA fair-μ + cold-start DD-LMS) vs CMA on fresh disjoint test seeds [121-130]: oracle headroom = 0.0037 macro PI-SER, 8× below the 0.03 practical threshold. MMA/DD-LMS fail in the SAME collapse realizations as CMA (correlated failure modes). Independent verifier 8/8 PASS. Macro B (router) NOT run (no headroom). The prior C16 "26/37 complementarity" confirmed as an artifact of illegal expert + contaminated seeds.
- **S011/D017/V006 (2026-07-22)**: bounded reconciliation of commit e15ae60. 7 audit items all CONFIRMED. H060 downgraded from PRIMARY to LOCAL_SLICE weak claim.

## 5. Current Mode

- Mode: SCIENCE_SCOUT verdict delivered (D018 = C). Hybrid-routing contract closed. No method contribution; a slice-level negative bound + methodology lesson harvested. Algorithm-selection family stays open; only the model-based GG+SOP tracker axis remains as a positive-potential candidate (needs user strategy decision).

## 6. Thesis Harvest (current view)

- **H060 (DOWNGRADED to LOCAL_SLICE)**: "Godard-cost collapses on the 11-cell slice × seeds 71-80" weak claim ONLY. The global "channel property / 5-axis exhausted / inversion-info-unextractable / publishable negative-boundary" claims are INVALIDATED (D017).
- H061 (affine): route CLOSED on sound objective (valid)
- H062 (GMI): WITHDRAWN — not a true bound (scale-artifact)
- H063 (init): scope-narrowed — strongest-single-init only
- H064 (ring-aware cost): mechanism claim WITHDRAWN (unequal-step confound)
- H065 (non-modulus HOS): reclassified — paradigm-distinct but task-mismatched (not a legal FIR expert)
- H066 (detector ceiling): valid
- H067-H068: reusable assets (GMI evaluator, HOS equalizer) — valid as assets
- Full: harvest/current.yaml

## 7. Next Automatic Action

D018 VERDICT C — hybrid-routing contract closed (headroom 0.0037 << 0.03 threshold; correlated failure modes among legal FIR experts). No automatic scientific runner remains in the blind-equalizer expert-routing sub-family. Algorithm-selection family stays open; the only untested positive-potential axis is the receiver-only model-based GG+SOP tracker (needs ~1 day infra + user strategy decision).

## 8. Strategy Escalation Condition

Choose: (a) invest ~1 day in the receiver-only model-based GG+SOP tracker (the last identified positive-potential axis, channel MODEL priors not pilots/modulus); or (b) harvest the accumulated negative material (D017 task-mismatch lesson + D018 correlated-failure bound + LOCAL_SLICE Godard-collapse + C11/MMA/blind-affine negatives) and decide thesis spine direction; or (c) change formal goal/contribution line.

## Detail Pointers

- Current state: projects/thesis-fso/direction-lab/state/current.yaml
- Portfolio: projects/thesis-fso/direction-lab/portfolio/current.yaml
- Harvest: projects/thesis-fso/direction-lab/harvest/current.yaml
- Probes: projects/thesis-fso/direction-lab/probes/p01-p05
- Scouts: projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c*-scout
