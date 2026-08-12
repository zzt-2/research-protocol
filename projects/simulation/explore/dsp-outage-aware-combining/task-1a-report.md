# Task 1A report: receiver/truth firewall and deterministic generator

## Files changed

- `test_smoke.py`: six focused tests for the information firewall, 18-cell grid, deterministic replay, physical prefix offsets, truth-copy metamorphism, and absence of defect-injection controls.
- `smoke_core.py`: frozen DTOs, frozen natural-cell grid, local QPSK/FSTS construction, explicitly seeded Gamma-Gamma/Wiener/AWGN channel generation, physical offsets, and receiver-only realization hashing.

## RED evidence

Command, run before `smoke_core.py` existed:

```text
python -m pytest test_smoke.py -q
```

Expected result: collection stopped with `ModuleNotFoundError: No module named 'smoke_core'` (`1 error in 0.37s`). This was the intended missing-feature failure.

## GREEN evidence

Command after the minimal implementation:

```text
python -m pytest test_smoke.py -q
```

Result: `6 passed in 0.67s`; exit code 0; no warnings or NaNs were emitted.

## Design deviations

None within Task 1A. The local QPSK mapping is used as explicitly permitted. No estimator, combining arm, diagnostic, oracle, runner, or proposed method was added.

## Remaining risks

- The Gamma-Gamma triples and deterministic K=4 strong/weak replication remain explicitly labeled `UNVERIFIED_RANGE`.
- Prefix-offset observability is currently checked by direct FSTS correlation at the frozen test realization; production synchronization and guarded peak metrics belong to Task 1B.
- Frozen dataclasses prevent field reassignment and all generated arrays are read-only, but NumPy read-only flags are a runtime guard rather than a cryptographic isolation boundary. Function signatures remain the primary truth firewall.

