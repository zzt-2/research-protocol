# P03/U19 Interface Closure Sprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use test-driven development; execute continuously to the final readiness gate.

**Goal:** Close the P03 receiver-output, analytic-comparator, residual-artifact, and readiness interfaces without running a performance batch.

**Architecture:** Three pure candidate-level components consume a real standard-CMA output in sequence: `z_window_adapter` admits only receiver-visible data, `analytic_comparator` applies a same-information QPSK detector, and `residual_artifact` computes explicitly scoped receiver residual diagnostics plus separated evaluation-only fixed/PI BER. `run_interface_smoke` owns the one-cell orchestration and writes only to this Scout directory.

**Tech Stack:** Python 3.11, NumPy, PyYAML, pytest, frozen `run_b001._default_runner` standard-CMA seam.

## Global Constraints

- Do not start B004 or create formal performance cells.
- Do not modify or rerun B002/B003 and do not modify the canonical baseline.
- Do not write smoke output to an evidence ledger, paper, formal material, Queue, or Registry.
- Runtime inputs exclude TX truth, true h/Jones/theta, BER, future windows, and post-hoc labels.
- Every numerical and physical smoke field is explicit in `interface-smoke-contract.v1.yaml`; no hidden defaults.
- `CSI_NONE` must run; receiver-estimated CSI must be schema-valid but cannot use oracle CSI.

## File Structure

- `z_window_adapter.py`: strict receiver-output validation, JSON-safe complex-window schema, CSI access validation, source pointers.
- `analytic_comparator.py`: same-information fixed QPSK comparator and deterministic diagnostics.
- `residual_artifact.py`: comparator-relative residual summaries, explicit tail threshold, separated evaluation-only fixed/PI metrics, stability schema.
- `run_interface_smoke.py`: explicit one-cell generator/CMA call, component orchestration, source hashing, isolated artifact write.
- `interface-smoke-contract.v1.yaml`: all smoke parameters and exact valid domain.
- `readiness-report.yaml`: work-package gates, component identity/fingerprints, remaining Sandbox prerequisites, final verdict.
- `tests/test_p03_*.py`: RED/GREEN boundary, numerical, integration, and history-guard tests.

### Task 1: z-window adapter

- [ ] Write failing tests for authentic standard-CMA output, schema/shape/dtype/range/source pointers, `CSI_NONE`, receiver-estimated CSI validation, and recursive oracle/future/TX rejection.
- [ ] Run only the new adapter tests and confirm failure because the component is absent.
- [ ] Implement the smallest strict adapter and rerun to green.

### Task 2: analytic comparator

- [ ] Write failing tests for `CSI_NONE` nearest canonical-QPSK decisions, optional same-level receiver-estimated CSI, shape/finite output, deterministic equality, and residual-distance monotonicity.
- [ ] Confirm RED, implement the pure comparator, and rerun to green.

### Task 3: residual artifact

- [ ] Write failing tests for comparator-relative residual definition, explicit conditional moments/tail mass, fixed/PI separation, evaluation-only boundary, valid domain, source hashes, causal boundary, single/multi-cell stability schema, and missing-parameter rejection.
- [ ] Confirm RED, implement the pure artifact builder, and rerun to green.

### Task 4: authentic one-cell smoke and readiness

- [ ] Write failing integration tests requiring every smoke parameter, authentic `run_b001._default_runner` output, deterministic repeated artifacts, no ledger/Queue/Registry/B004 writes, and frozen B002/B003 hashes.
- [ ] Confirm RED, implement the isolated smoke runner and contract, run it twice, and compare deterministic payload hashes.
- [ ] Compute candidate-level component IDs/fingerprints only after all component and smoke tests pass.
- [ ] Update the Scout contract and readiness report to exactly one verdict: `P03_SCOUT_CONTRACT_READY` or `P03_BLOCKED`.

## Exit Criterion

`P03_SCOUT_CONTRACT_READY` requires all four work packages PASS, an authentic standard-CMA z-window path, `CSI_NONE` execution, same-information comparator, deterministic one-cell artifact, component fingerprints, and no historical/governance boundary violation. Otherwise write `P03_BLOCKED` with reproduction command, reusable assets, and next-candidate recommendation.
