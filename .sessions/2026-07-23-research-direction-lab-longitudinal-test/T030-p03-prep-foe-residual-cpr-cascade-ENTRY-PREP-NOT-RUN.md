# T030 — P03 ENTRY PREP (NOT RUN): FOE-residual → CPR cascade robustness (Family B)

> **STATUS: ENTRY PREPARATION ONLY — DO NOT RUN in this dialog.** Next dialog, user
> relays the P03 execution instruction; only then does an executor implement/run.
> Source: S003 / D039-D040 campaign; A family closed at consecutive=2 (P01+P02);
> P03 MUST switch mechanism family. This prep picks family B and freezes the entry
> contract so the next dialog can execute without re-deriving scope.
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Date: 2026-07-30

## 0. Why family B (sync/estimator interaction), not C/D/E

A family (CPR selector robustness) is closed. Among B/C/D/E, **B = FOE-residual → CPR
cascade** is the strongest problem-bearing entry because:
- **Gate 1 (physical DOF exists):** FOE runs upstream of CPR in the EXISTING frozen
  pipeline (`_a4_branchrouted_30seed.py::fft_foe_m0_omega`, already exercised by the
  anchor). A biased/residual FOE rotates the constellation passed to CPR — a real
  transformation the simulator already applies. No new channel physics needed.
- **Gate 2 (baseline failure aligns with the lever):** CPR selector and DA/NDA
  branches both assume FOE is removed; a residual FOE is a NEW failure condition
  injected into an already-completed method (FR-23 problem-driven, not blank-filling).
  The lever (FOE residual magnitude/phase) acts exactly where CPR decides.
- **Gate 3 (named conventional comparator):** the conventional adapter = a
  receiver-visible FOE-residual detector / guard (e.g. CFO-guard via pilot-phase
  slope, or a residual-rotation clamp) — a specific conventional algorithm, task-matched,
  same blind information, independently tunable. Not a placeholder.
- **Gate 4 (file:line evidence):** `fft_foe_m0_omega` and its consumer in the NDA/DA
  recovery path are in the frozen source; the CPR decide path is `_a4_switch_common768_
  30seed.py::decide`.

C/D/E are viable but weaker at entry: C (turbulence boundary) risks re-touching the
closed channel-physics path (D038); D (modulation/coding) needs a new FEC/APSK-ring
module not yet frozen; E (info/complexity) is more of a parameter sweep than a
mechanism-distinct failure injection.

## 1. P03 package question (frozen, to be confirmed pre-execution next dialog)

Does a residual FOE (rotation left after `fft_foe_m0_omega`) cause SUBSTANTIAL harm
to the frozen DA/NDA CPR selector (the completed method), and can a conventional
FOE-residual adapter resolve it — OR does a robust candidate beat the adapter on
fresh held-out at the operating region where harm is worst?

## 2. Problem-bearing probe design (Phase A, to freeze pre-execution)

- Inject a controlled FOE residual Δf (Hz/sample or rad/sample) AFTER the frozen FOE
  step, holding the receiver's nominal Δf̂ = 0 (mismatch analog to P01's SNR bias).
  True Δf only in signal/eval; the selector sees Δf̂=0.
- Reuse the frozen anchor `ccisp_family1_selector_a_30seed.json` reproduction path
  (P01 already proved byte-exact reproduction at Δf=0).
- Freeze "substantial harm" criterion BEFORE test: e.g. mean paired-seed common-768
  gain drops ≥0.3 dB vs Δf=0 AND CI_high<0, on cells where anchor gain ≥0.5 dB.
- Search Δf over a receiver-plausible residual range (to be fixed from the FOE
  estimator's documented residual floor, NOT cherry-picked).

## 3. Conventional adapter (Phase B, to freeze pre-execution)

Receiver-visible FOE-residual estimator (e.g. pilot-symbol phase slope across the
block, or a second-pass CFO estimate) + original decide rule. δ(Δf)-invariant by
construction; true Δf never in decide. Adapter resolves harm if it recovers ≥ harm
threshold on every harm cell.

## 4. Robust candidates (Phase C, only if adapter leaves residual)

3–5 mechanism-different constructs (e.g. residual-rotation-tolerant CV statistic,
joint FOE/CPR confidence band, FOE-residual-gated branch fallback). Frozen MDE=+0.15 dB
(same as P01/P02 — do NOT lower). Fresh held-out seeds disjoint from all prior
(anchor 0–29, P01 0–9/30–49, P02 dev 50–59/held-out 60–99\{71–80}, pollution 71–80).

## 5. Discipline reminders for next dialog (DO NOT skip)

- Read T029 (P02) + this T030 + the frozen FOE source BEFORE running.
- Re-verify four-gate preflight with file:line (method-production.md); if any gate
  fails on closer reading, route to STRATEGIC_GATE, do NOT force-run.
- New files only; do NOT edit frozen pipeline files.
- Independent executor + independent verifier + controller receipt, one in-package
  fix allowed, unified commit, no push.
- Family B consecutive starts at 1 (this would be P03 = first B-family package).

## 6. Not run this dialog

No code written, no seeds run, no artifacts produced. This is entry selection +
contract freeze only, per user instruction.
