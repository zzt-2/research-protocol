# Task 2 report: dev tuning, raw reconstruction, CIs, and freeze receipt

## Files changed

- `test_smoke.py`: added runner-contract tests for frozen candidate grids, disjoint seeds, deterministic dev tuning, rank AUC, raw-only reconstruction, all four fail-stop exits plus PASS, duplicate/missing merge rejection, within-pair receiver-hash identity, and fail-closed receipt hashes.
- `run_smoke.py`: added import-safe split execution, normalized raw CSV output, dev-only B1/top-L/strongest-family selection, dev-standardized logistic diagnostics, rank AUC, deterministic seed-cluster bootstrap, raw-only G1–G4 aggregation, raw merge validation, and immutable freeze receipt writing/validation.
- `task-2-report.md`: this report.

## RED evidence

Before `run_smoke.py` existed:

```text
python -m pytest test_smoke.py -q
ModuleNotFoundError: No module named 'run_smoke'
1 error in 0.27s
```

After the first GREEN pass, a receiver-pair integrity regression test was added. It failed as intended because aggregation did not yet reject a changed method-row receiver hash:

```text
FAILED test_aggregate_rejects_receiver_hash_mismatch_within_pair
Failed: DID NOT RAISE <class 'ValueError'>
1 failed, 30 passed in 0.35s
```

The same review found that bootstrap duplicate seed draws needed explicit copy identity so G1 frame counts preserve cluster multiplicity. The bounded repair adds `__bootstrap_copy` only to in-memory bootstrap replicas; it never enters raw data.

## GREEN evidence

Final commands:

```text
python -m pytest test_smoke.py -q
python -m py_compile smoke_core.py run_smoke.py test_smoke.py
python -W error -m pytest test_smoke.py -q
```

Results: `31 passed in 0.24s`, compile exit 0, then `31 passed in 0.22s` with warnings promoted to errors. No warning or NaN was emitted by the tests.

## Contract boundary

- No dev grid, held-out seed, or scientific terminal was run.
- The only branch actions are B0, frozen-grid B1, and top-L B2; diagnostic scores are written/evaluated only and never select a subset.
- O1 and invalid labels are evaluator-side. Each generated `(seed, cell)` is created once and its receiver hash is shared by every raw row.
- Test execution validates a still-unstarted receipt before generating any sample. The receipt binds source/design/test and dev raw/aggregate hashes plus seeds, cells, candidate grids, bootstrap settings, metrics, gates, and declared parameter limitations.

## Deviations

None from the Task 2 scope. The CLI exposes aggregate and receipt validation; split, tuning, merge, receipt writing, and validation are also explicit import-safe functions for the controller.

## Remaining risks

- Unit tests use synthetic raw rows and reduced bootstrap replicates; numerical behavior on the 18-cell dev data remains unobserved by design.
- Logistic IRLS uses deterministic weak ridge regularization. Near-complete separation may yield large but finite frozen coefficients and should be inspected in the dev receipt.
- `aggregate_from_raw` validates receiver-hash pairing, while full expected seed/cell coverage is enforced at merge time; the controller must merge/validate before headline aggregation.
- The runner is an MVE proxy, not a Wang DSP reproduction; all previously declared `UNVERIFIED_RANGE` limitations remain unchanged.
