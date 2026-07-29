# Worker Log — Step 027: update-granularity CMA method-factory sprint (sprint-003)

> Task: T027 (PREFORMAL_METHOD_FACTORY, epoch 61 / CP025).
> Source decisions: D035 / V061 (problem-bearing testbed preflight, 4-gate pass);
>   V052 REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO (gate-2
>   evidence-grade correction).
> Branch: `codex/rdl-method-production-v2` (worktree
>   `.worktrees/rdl-method-production-v2`).
> Date: 2026-07-29.
> Python: `~/scoop/apps/python311/current/python` (numpy 2.4.3, scipy 1.17.1,
>   pydantic 2.11.10). The AGENTS.md `bin/python` path and the `~/.venvs/torch`
>   venv are unusable here (torch venv lacks pydantic/pip; the channel needs
>   pydantic). Used system python311 instead.

## What was built

Isolated sprint-003 package at
`projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`:

- `factory-contract.v3.yaml` — shared anchor identity, frozen inherited anchor,
  seed split, comparator definition (Godard-with-z, provenance
  `cb1_cell_runner.py:124-129`), comparator-aware signal gate, 5-way claim
  ceiling, update-granularity DOF evidence (file:line), gate-2 evidence-grade
  correction note, mandatory ablation spec.
- `method-map.v3.md` — each construct: deployable_action / update_granularity /
  raw_input / frozen_params / difference_from_sprint001_sprint002_and_rejected_axes
  (dedup vs C04/C09/C12/C14/C15/C16/M1-M5 and the §3.1 rejected frequency-domain
  family).
- `src/methods.py` — (a) block64 anchor, (b) per-symbol Godard-with-z
  comparator, (c) block-8/block-16 Godard-with-z, (d) sliding-window recursive
  CMA. All canonical Godard-with-z gradient (contains z); all act on raw rX/rY.
- `src/run_factory.py` — pipeline (identity / smoke / dev / test / ablation),
  comparator-aware seed-cluster gate, 5-way terminal verdict, smoke NOT
  clobbered (V052 fix).
- `tests/test_gradient_identity_and_causality.py` — 7 TDD tests (gradient
  identity Godard-with-z vs scalar-error, per-symbol semantics, smaller-block
  semantics, eval-window parity, determinism, no-suffix-feedback). 7/7 PASS.
- `artifacts/` — `prefix-receipt.json`, `dev-freeze-receipt.v1.json` (incl.
  comparator mu tuning trace), `raw-rows.v3.csv` (840 rows), `result.v3.json`.

## What was NOT modified

No edits to `common/`, `params.py`, baseline-atlas, B01/B01-R, C11 raw, or any
owner/session file. No push. The pre-existing dirty files in the worktree
(`.agents/skills/.../method-production.md`, `T027-*.md`, `topic-index.md`)
were left untouched by this sprint.

## Execution trace

1. Phase A identity: all 4 gates PASS (QPSK PI-SER=0.0; eval-pop finite;
   freeze invariance bit-identical; gradient Godard-with-z stamped).
2. Phase B smoke: 4 constructs each produce own z distinct from anchor,
   stamp Godard-with-z, deterministic.
3. Phase C1 dev freeze: comparator mu=0.001 (dev-optimal; larger diverges on
   long cells). block8/16 mu=0.003; recursive mu=0.0003, lam=0.9.
4. Phase C2 test (7 cells × 20 seeds, ~22s wall): comparator seed-cluster mean
   PI-SER=0.29685 vs anchor=0.31431. Best candidate block8 Δ=−0.0029 vs
   comparator (CI crosses 0, fails MDE). No candidate signal.
5. Phase E ablation: no winner vs comparator → no matched-budget adjudication
   triggered; field flat across 0.0156 → 1.0 updates/sym.

## Honest-result note

The verdict is `NO_DIAGNOSTIC_SIGNAL`, deliberately NOT
`PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`: the tuned per-symbol comparator
removes the anchor collapse on only **1 of 7** cells (the comparator did NOT
resolve the collapse on 6/7). It is also NOT a manufactured signal: no
candidate beats the comparator. The comparator mu=0.001 was verified to be the
fair dev-optimal (larger mu diverges on long cells) — not an under-fit
artifact. The gate-2 SUSPECTED lever (block-end update geometry) is NOT
confirmed as the collapse cause.

## Outcome

Terminal verdict: **`NO_DIAGNOSTIC_SIGNAL`**. Not a carrier. Diagnostic-only;
no formal MVE, no Step 5, no paper claim, no auto-promotion.
