# Step 019 — Pre-formal Method Factory Sprint 001

> Task: T019 (PREFORMAL_METHOD_FACTORY, CP017)
> Date: 2026-07-28
> Status: `NO_DIAGNOSTIC_SIGNAL` | mission_method_delta: `FAIR_COMPARISON_RUN`
> Claim ceiling: DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE
> Artifacts: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-001/`

## 1. Task boundary

Diagnostic-only pre-formal method factory sprint (D026). NOT a Groundwork
Step 4a MVE. Did NOT execute/modify T018 or Q14. Did NOT update owner,
mission-log, sessions, registry, or master-state. Did NOT push.

## 2. Testbed selection (Phase A)

- **Selected**: `cb1-modulation-generic-closure/baseline-atlas/` (CB1).
  - Runnable (QPSK regression PI-SER=0.0 PASS).
  - Frozen traditional baseline (standard-CMA Godard-with-z) with identity gate.
  - Paired realization (`generate_shared_realization_dp`), seeds 11-20.
  - Primary metric PI-SER (lower better), MDE=0.005, direction clear.
  - Inherited verdict `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` (real headroom
    0.31-0.33 on 16QAM, invariant to N and to MMA).
- **Rejected**: `P03-U19-residual-headroom/`. QPSK-only,
  `LOCAL_NEGATIVE / NO_VISIBLE_HEADROOM`, scout-contract CLOSED, explicitly
  forbids ML. Not a usable testbed.
- Frozen contract: `factory-contract.v1.yaml` (testbed source+hashes, frozen
  axes, 6 diagnostic cells, 10 seeds with two non-overlapping halves,
  receiver-visible I/O contract, forbidden privileged inputs, terminal states).

## 3. Constructs built (Phase B, 5 mechanism-distinct)

| ID | Lever | Action | Smoke |
|----|-------|--------|-------|
| M1 | cost surface | reduced-modulus CMA (R²=0.2 inner shell) | PASS |
| M2 | update trigger | causal trace-driven diversity re-init | PASS |
| M3 | init + selection | K=4 multi-start + alphabet-geometry pick | PASS |
| M4 | post-eq cascade | conditional DD affine (gate on cal_power<0.5) | PASS |
| M5 | output remap | radius-shell remap (gate on mean\|z\|²<0.5) | PASS |

All five implemented as adapters over the frozen CB1 runner/evaluator
(`src/methods.py`, `src/run_factory.py`). No `common/` or `params.py`
modification. No privileged input in any deployable action.

## 4. Fair comparison (Phase C)

- 6 cells × 10 seeds = 60 paired realizations; 420 raw rows
  (`artifacts/raw-rows.v1.csv`).
- Every method ran on the same realization per (cell,seed).
- QPSK identity regression PASS; clean-boundary intact (no clean-seed
  regression > MDE on any construct).

### Result (paired Δ vs baseline, negative = improvement)

| Construct | median Δ | help/hurt/tie | dir consistent | gate |
|-----------|---------:|---------------|----------------|------|
| M1 | +0.0000 | 2/15/43 | yes | NO_SIGNAL |
| M2 | +0.0000 | 0/29/31 | no | NO_SIGNAL |
| M3 | +0.0098 | 2/30/28 | no | NO_SIGNAL |
| M4 | +0.0000 | 2/21/37 | no | NO_SIGNAL |
| M5 | +0.0000 | 15/5/40 | no | NO_SIGNAL |

**No construct passes the diagnostic signal gate.**

## 5. Failure mechanism (why no signal)

- Baseline collapses on 30/60 (cell,seed) pairs (bimodal, seed-determined).
- M1 (cost): no change to collapse fate — collapse is not a single-modulus
  pathology alone under the frozen block-end protocol.
- M2/M3 (trajectory): diversity re-init / multi-start cannot escape — collapse
  basin has large attraction radius under block-end updates.
- M4/M5 (post-proc): same-information corrections fail because the collapse
  corrupts the pseudo-labels they rely on. Oracle affine recovers only because
  it uses TX truth (privileged).
- **Net**: separates oracle-recoverable gap (exists) from receiver-recoverable
  gap (~zero for these 5 lever families). Sharper than inherited H017/H022.

## 6. Acceptance check

- [x] control validator PASS; worktree clean at start
- [x] T018/Q14 not executed or modified
- [x] shared testbed, baseline, paired realization have reviewable evidence
- [x] 5 mechanism-distinct constructs, all 5 actually ran (≥3 required)
- [x] no privileged/future/TX-truth deployable input
- [x] raw rows, aggregate, smoke tests, source hashes all present
- [x] normal-terminal method delta is `FAIR_COMPARISON_RUN` (not NONE)
- [x] conclusion explicitly marked diagnostic-only
- [x] owner/mission/session files not updated
- [x] only authorized paths committed; no push

## 7. Verdict

`NO_DIAGNOSTIC_SIGNAL`. 5 constructs built, fairly compared, none passes the
gate. Mechanistically informative negative: localizes the collapse to a
structural attractor unescapable by receiver-visible same-information levers,
and separates oracle-recoverable from receiver-recoverable gaps. Per D026 this
is a legitimate terminal state; no winner to return to formal Groundwork.
