# Pre-formal Method Factory Sprint 001 — Synthesis v1

> **Status: `NO_DIAGNOSTIC_SIGNAL`** | **mission_method_delta: `FAIR_COMPARISON_RUN`**
> Claim ceiling: **DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE**
> Task: T019 (PREFORMAL_METHOD_FACTORY, CP017)
> Date: 2026-07-28

## 0. TL;DR

Five mechanism-distinct constructs were built and fairly compared against the
frozen traditional baseline (standard-CMA Godard-with-z) on the shared CB1
dual-pol OSL 16QAM testbed, using paired realizations (60 (cell,seed) pairs
across 6 cells × 10 seeds). All five ran and passed their semantic smoke; none
passed the diagnostic signal gate. The negative result is **mechanistically
informative**: it localizes the inner-ring collapse to a structural
attractor that receiver-visible same-information lever points (cost, scheduling,
multi-start, conditional cascade, radius remap) cannot escape, and it
distinguishes the recoverable-by-oracle gap from the recoverable-by-receiver
gap.

## 1. Shared testbed (frozen, reused)

| Field | Value |
|-------|-------|
| Source | `cb1-modulation-generic-closure/baseline-atlas/` (inherited, not rebuilt) |
| Generator | `common._dual_pol_channel.generate_shared_realization_dp` (paired realization) |
| Baseline | `standard_cma_godard_with_z` (R²=1.32, μ=1e-3, n_tap=11, block_size=64, center-tap) |
| Primary metric | PI-SER (permutation-invariant, lower is better), MDE=0.005 |
| QPSK identity regression | PI-SER = 0.0 on anchor (PASS, verified 2026-07-28) |
| Inherited verdict | `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` (CMA headroom 0.31-0.33 on 16QAM, invariant to N and to MMA) |

Selection rationale: the alternative entry (P03-U19-residual-headroom) is
QPSK-only with `LOCAL_NEGATIVE / NO_VISIBLE_HEADROOM`, scout-contract CLOSED,
and explicitly forbids training ML — it is not a usable testbed. CB1 has a
real, adjudicated, runnable headroom.

## 2. Constructs built (5, mechanism-distinct)

| ID | Mechanism lever | Deployable action (one line) | Smoke |
|----|-----------------|------------------------------|-------|
| M1 | Cost surface | Reduced-modulus CMA (R²=0.2, inner shell) | PASS (z differs from baseline) |
| M2 | Update trigger | Causal trace-driven diversity re-init (max 2) | PASS (reinit fires, z changes) |
| M3 | Init + selection | K=4 multi-start + alphabet-geometry pick | PASS (scores distinct, selection active) |
| M4 | Post-eq cascade | Conditional DD affine (gate on cal_power<0.5) | PASS (gate opens collapsed, closes clean) |
| M5 | Output remap | Radius-shell remap (gate on mean\|z\|²<0.5) | PASS (remap fires collapsed, identity clean) |

Each construct targets a **distinct receiver-visible lever** (cost / scheduling
/ init-select / cascade / remap). None consumes TX truth, the true channel, the
future window, or oracle coefficients.

## 3. Fair paired comparison (Phase C-2)

6 cells × 10 seeds = 60 paired (cell,seed) realizations. Every method ran on
the **same** realization object per pair (no per-method channel generation).
420 raw rows saved (`artifacts/raw-rows.v1.csv`).

### Aggregate paired delta vs baseline (negative = improvement)

| Construct | n | median Δ | trimmed Δ(10%) | bootstrap 95% CI (median) | help/hurt/tie | dir-A | dir-B | consistent | Gate |
|-----------|--:|---------:|---------------:|--------------------------|---------------|------|------|-----------|------|
| M1 reduced-modulus | 60 | +0.0000 | +0.0076 | [0.000, 0.014] | 2/15/43 | +0.000 | +0.000 | yes | NO_SIGNAL |
| M2 trace reinit | 60 | +0.0000 | +0.0204 | [0.000, 0.039] | 0/29/31 | +0.000 | +0.055 | no | NO_SIGNAL |
| M3 multistart select | 60 | +0.0098 | +0.0231 | [0.000, 0.045] | 2/30/28 | +0.000 | +0.061 | no | NO_SIGNAL |
| M4 conditional DD | 60 | +0.0000 | +0.0041 | [0.000, 0.012] | 2/21/37 | +0.000 | +0.004 | no | NO_SIGNAL |
| M5 radius remap | 60 | +0.0000 | −0.0021 | [−0.012, 0.000] | 15/5/40 | +0.000 | −0.002 | no | NO_SIGNAL |

**No construct passes the diagnostic signal gate** (requires: positive median
improvement AND help>hurt AND direction consistent across seed halves AND
≥2 cells improving AND clean-boundary intact).

### Baseline collapse structure (diagnostic context)

Of 60 (cell,seed) pairs, the frozen baseline collapses (PI-SER > 0.1) on
**30/60** and is clean (PI-SER ≤ 0.1) on **30/60**. The collapse is bimodal
and seed-determined, matching the inherited `H017` failure mechanism.

### Per-construct behavior on collapsed vs clean seeds

On **collapsed** seeds (baseline PI-SER > 0.1):
- **M1** = baseline (cost change does not alter the collapse fate).
- **M2** > baseline by ~0.05-0.09 (reinit triggers but fails to escape; the
  diversity perturbation lands back in the same basin).
- **M3** > baseline by ~0.05-0.09 (the alphabet-geometry selection score is
  fooled by the collapse — a collapsed z-stream's |z|² clusters on one shell,
  which can look alphabet-consistent for the wrong shell).
- **M4** = blind_affine (the conditional DD affine is identical to the shared
  cheap alternative when the gate opens). It recovers **a few** collapsed
  seeds (e.g. snr25 seed17: 0.344 → 0.012) but regresses or ties most.
- **M5** improves **some** collapsed seeds modestly (e.g. snr25 seed16:
  0.707 → 0.496) by correcting pure radius bias, but cannot recover the
  angular/phase distortion.

On **clean** seeds (baseline PI-SER ≤ 0.1): all constructs are ≈ baseline
(median Δ = 0, mostly ties) — the gates correctly keep M4/M5 at identity, and
M1/M2/M3 converge to the same clean solution. **No clean-boundary collapse.**

## 4. Mechanism: why no construct escapes

The inner-ring collapse is a **structural attractor** of block-end
gradient-descent CMA/MMA on this SOP-rotation + Gamma-Gamma-fading channel at
the frozen μ/block/n_tap. Three independent lever families confirm this:

1. **Cost surface (M1)**: pulling the modulus target to the inner shell does
   not remove the attractor — the collapse is driven by the **block-end update
   geometry + channel time-variation**, not by the single-modulus mismatch
   alone (consistent with the inherited `H018`: MMA also fails).
2. **Trajectory (M2, M3)**: causal re-init and multi-start diversity do not
   escape — the diversity perturbations re-enter the same basin within a few
   blocks. This means the collapse basin has a **large attraction radius**
   under the frozen block-end protocol.
3. **Post-processing (M4, M5)**: same-information corrections cannot recover
   the collapse because the collapse corrupts the **pseudo-labels** the
   post-processor relies on. DD affine (M4) fits to collapsed hard decisions;
   radius remap (M5) fixes radius but not angular distortion. The oracle
   affine recovers precisely because it uses TX truth to fit the **full**
   affine (rotation + scaling), which is the privileged information the
   receiver lacks.

This **separates two gaps** that the inherited `H022` (METHOD_SIGNAL scoped)
had conflated:
- **oracle-recoverable gap** (oracle affine → PI-SER ≈ 0): the information is
  in the z-stream, but recovering it requires the TX-truth-calibrated affine.
- **receiver-recoverable gap** (these 5 constructs → no improvement): with
  receiver-visible, causal, same-information inputs, the collapse is **not**
  recoverable by cost/scheduling/multi-start/cascade/remap levers under the
  frozen protocol.

The receiver-recoverable gap is effectively **zero** for these five mechanism
families. The oracle-recoverable gap remains, but it is gated behind
privileged information.

## 5. Diagnostic signal gate result

| Gate condition | M1 | M2 | M3 | M4 | M5 |
|----------------|----|----|----|----|----|
| positive median (Δ<0) | ✗ | ✗ | ✗ | ✗ | ✗ (0) |
| help > hurt | ✗ | ✗ | ✗ | ✗ | ✓ (15>5) |
| direction consistent across halves | ✓ | ✗ | ✗ | ✗ | ✗ |
| ≥2 cells improving | ✗ | ✗ | ✗ | ✗ | partial |
| clean-boundary intact | ✓ | ✓ | ✓ | ✓ | ✓ |
| **overall** | NO_SIGNAL | NO_SIGNAL | NO_SIGNAL | NO_SIGNAL | NO_SIGNAL |

M5 is the closest to a weak signal (help>hurt on every cell, but median Δ=0
because most pairs are ties, and direction inconsistent across halves). It is
recorded as `WEAK_DIAGNOSTIC_SIGNAL` flavor but does not pass the gate.

## 6. Claim ceiling and what this is NOT

- **NOT a formal Go/Kill.** This is a diagnostic factory sprint. The
  inherited `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` verdict is unchanged.
- **NOT a paper number.** No construct is promoted.
- **NOT a domain closure.** The headroom still exists; this sprint shows five
  receiver-visible lever families do not capture it.
- **NOT a reopening of rejected axes.** All five constructs are new deployable
  actions distinct from the step-002~009 rejected families (see method-map §
  `difference_from_rejected_axes` per construct).

## 7. What this DOES establish (diagnostic value)

1. **The collapse is not a cost-surface pathology alone** (M1 rules out
   single-modulus mismatch as the dominant driver under the frozen block-end
   protocol — corroborates H018's MMA finding from a different lever).
2. **The collapse basin has a large attraction radius** under block-end
   updates (M2/M3 diversity cannot escape) — this is a new, sharper
   characterization than H017's "seed-and-trajectory dependent".
3. **The oracle-recoverable gap ≠ the receiver-recoverable gap.** The
   information-recoverability (H022) holds only with TX-truth calibration;
   receiver-visible same-information post-processing (M4/M5) cannot harvest it.
   This is a **negative refinement of H022** that any future ML Scout must
   respect: the scout's features must carry more than z-derived pseudo-labels
   to beat the receiver-recoverable gap (e.g. multi-block trace dynamics, not
   single-slice hard decisions).

## 8. Open questions / next legal actions (for the master, NOT this sprint)

- The frozen block-end protocol (block_size=64, μ=1e-3) is the inherited
  identity and the suspected bottleneck (H021). Adjudicating per-symbol
  stochastic-gradient variants would break the baseline identity parity and is
  out of scope here, but is the most informative next lever **if** a future
  sprint is authorized to relax the identity parity (requires master decision).
- A sixth mechanism family not tested here: **frequency-domain / sub-band**
  equalization (a different receiver step entirely). Not in this sprint's 5.
- These results do NOT authorize an ML Scout. The pre-method gate
  (`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`) still holds, but the receiver-
  recoverable gap being ~zero for these five families is new evidence the
  master should weigh before any ML Scout.

## 9. Verdict

**`NO_DIAGNOSTIC_SIGNAL`** — 5 mechanism-distinct constructs built and fairly
compared; none passes the diagnostic signal gate. `mission_method_delta =
FAIR_COMPARISON_RUN`. Per D026/method-production, this is a legitimate terminal
state. The sprint produced a mechanistically informative negative that
sharpens the failure characterization and separates oracle-recoverable from
receiver-recoverable gaps.
