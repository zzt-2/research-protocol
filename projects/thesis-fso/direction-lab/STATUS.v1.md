# Research Direction Lab Status
# Updated 2026-07-22 S012/D020/V009 — info-source portfolio Probe complete; F1-B Scout pending user authorization.
# IMPORTANT (D017): the prior "5 axes exhausted / collapse is a channel property" global
# narrative from commit e15ae60 is INVALIDATED. Numbers reproducible; scientific semantics
# failed on C12/C14/C15/C16 + seeds 71-80 lost held-out status. See harvest amendments.
# IMPORTANT (D020): info-source Probes ran on FRESH seeds [141-150]. F1-A model-prior oracle
# closes 0.133 macro PI-SER headroom (36x D018's blind-router 0.0037) with receiver-visible
# observability |r|=0.65. F1-B model-based tracker is the first PASSING positive-method candidate;
# needs ~1 day infrastructure investment (user decision). F4-A confirmed C12 scale-artifact.

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
- Exact collapse-aware routing among CMA/MMA/DD-LMS is CLOSED by D018; broader information-source families remain open.
- Full map: portfolio/current.yaml

## 4. Latest Completed Scientific Result

- **S012/D020/V009 (2026-07-22)**: information-source portfolio Probe (3 headroom Probes on fresh seeds [141-150]). F1-A model-prior oracle → PASS: macro PI-SER headroom = 0.1329 (CI [+0.078,+0.196]), 36× D018's blind-router bound; receiver-visible observability |r|=0.651 (z_amp_mean/cm_error_final correlate with headroom). F3-A causal history → PASS: MI increment +0.060 bits, R² increment +0.036. F4-A decoder-soft → BOUNDARY: analytic GMI headroom +0.0089 (smoothing-fragile, verifier P1) + histogram-MI reproduces C12 scale-artifact (−0.021, scale-invariant) + F4-B coded-chain INFRASTRUCTURE_BLOCKED. Independent verifier 9/9 checks (8 PASS + 1 PARTIAL), 0 P0, headline numbers bit-identical. F1-B model-based tracker is the first candidate with legal headroom + observability; needs ~1 day infrastructure (user decision).
- **S011/D018/V007 (2026-07-22)**: hybrid-routing Macro A → VERDICT C (COMPLEMENTARITY_INVALID). Legal FIR experts (MMA fair-μ + cold-start DD-LMS) vs CMA on fresh disjoint test seeds [121-130]: oracle headroom = 0.003693 macro PI-SER, 8× below the 0.03 practical threshold. MMA/DD-LMS fail in the SAME collapse realizations as CMA (correlated failure modes). Independent verifier 8/8 PASS. Macro B (router) NOT run (no headroom). The prior C16 "26/37 complementarity" confirmed as an artifact of illegal expert + contaminated seeds.
- **S011/D017/V006 (2026-07-22)**: bounded reconciliation of commit e15ae60. 7 audit items all CONFIRMED. H060 downgraded from PRIMARY to LOCAL_SLICE weak claim.

## 5. Current Mode

- Mode: SCIENCE_SCOUT info-source Probe complete. D020 found the first PASSING positive-method candidate (F1-B model-based tracker, headroom 0.133 + observability 0.65) but it needs ~1 day infrastructure; awaiting user investment decision (A/B/C/D). F4-A is a BOUNDARY result (do-not-build).

## 6. Thesis Harvest (current view)

- **H060 (DOWNGRADED to LOCAL_SLICE)**: "Godard-cost collapses on the 11-cell slice × seeds 71-80" weak claim ONLY. The global "channel property / 5-axis exhausted / inversion-info-unextractable / publishable negative-boundary" claims are INVALIDATED (D017).
- C04/C09 affine correction: UNRESOLVED because the corrected objective remains self-referential; C09 was not validly rerun.
- H062 (GMI): WITHDRAWN — not a true bound (scale-artifact)
- H063 (init): scope-narrowed — strongest-single-init only
- H064 (ring-aware cost): mechanism claim WITHDRAWN (unequal-step confound)
- H065 (non-modulus HOS): reclassified — paradigm-distinct but task-mismatched (not a legal FIR expert)
- H066 (detector ceiling): valid
- H067-H068: reusable assets (GMI evaluator, HOS equalizer) — valid as assets
- Full: harvest/current.yaml

## 7. Next Automatic Action

D020 — present the F1-B investment decision to the user (recommended: A = ~1 day dual-pol GG/SOP model-based tracker infrastructure + bounded Scout; comparator = fixed-μ CMA + blind_affine_compare_16qam). Do NOT auto-build the tracker without user authorization (material infrastructure investment).

## 8. Strategy Escalation Condition

Escalate only after the information-source map shows either (a) at least one evidence-backed family worth a larger Scout, (b) no source family has usable legal headroom and the thesis should pivot to harvest/formal-goal review, or (c) the best family needs a material infrastructure choice only the user can authorize.

## Detail Pointers

- Recovery handoff: .sessions/2026-07-20-direction-lab-science-scout/H013-info-source-probe-complete-f1b-decision.md
- Current state: projects/thesis-fso/direction-lab/state/current.yaml
- Portfolio: projects/thesis-fso/direction-lab/portfolio/current.yaml
- Harvest: projects/thesis-fso/direction-lab/harvest/current.yaml
- Probes: projects/thesis-fso/direction-lab/probes/p01-p05
- Scouts: projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c*-scout
