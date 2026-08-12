# Task 5 report: frozen held-out merge and aggregate

## Scope and preflight

- HEAD: `cbb8a2df7ad5151c4c1a15d3a5e4c4237f20da33`.
- Scoped tests: `43 passed in 0.68s`.
- `audit_deployable_information_boundary()`: `()`.
- Freeze receipt SHA-256: `5d958f8bc64320f0010937c1011d3fb5165d2194bded62f0ad81526e7a95242e`; `test_started=false`; all seven frozen file hashes matched.
- Five inputs each contained 2,520 rows and 360 seed-cell pairs. Their raw SHA-256 values were:
  - part-00: `71f6a787345f215595d3b4601d902421637dafa53401a89f7063f8fe1f9ee7d1`
  - part-01: `1fcca6812d59f77ff1de8c1e4fb92ffb5b9e4c551f7c311a541540e771fe8f02`
  - part-02: `0dc3ba04e00e4bbe87883a3efcb4fd72c5f0cb29a707bd62df4cb602576b5d9e`
  - part-03: `6b12d88b91fa4dd52b172ee8b8b65cb4aa4c992bd6c8270d98f8795401bcb813`
  - part-04: `b17405e752045c2644efc2b44c693149757f90df6b328112d8925070116ac137`
- Metadata and raw were independently checked before merge: exact disjoint seeds 10000..10099; 20 seeds x 18 cells per part; test split only; one receiver hash per seed-cell pair; exact frozen method signatures `B0=all`, `B1=-8.0`, `B2=K`, and `O1=oracle`.

## Commands and bounded validation repair

1. `python -m pytest -q test_smoke.py test_task1b_repair.py`
2. Independent Python receipt/part-hash/schema/seed/cell/method-signature audit.
3. `merge_raw(parts, raw_path, TEST_SEEDS, cell_ids, validation_mode="strict")`.
4. Initial `aggregate_from_raw(raw_path, frozen, bootstrap_replicates=2000, bootstrap_seed=20260811, validation_mode="strict")` failed before metric evaluation with `ValueError: raw does not cover exact DEV_SEEDS/TEST_SEEDS x 18 cells`.
5. Cause: the frozen caller passes `(cell.cell_id for cell in build_primary_cells())`; `_validate_raw_rows` reuses that one-shot iterator inside a seed x cell comprehension, so it is exhausted after the first seed. The only process-local adapter retained the original signature, converted non-null `expected_cells` (and `expected_seeds`) to tuples, then called the original `_validate_raw_rows`. It did not change raw rows, frozen values, metric/bootstrap code, source files, receipt, or hashes.
6. After independent strict raw validation, the official aggregate called the same `aggregate_from_raw(..., 2000, 20260811, "strict")`. A second strict recompute reread raw and deep-cloned the frozen contract; canonical sorted JSON was asserted byte-identical to the official file.

## Merged artifacts

- `artifacts/test/raw.csv`: 12,600 rows = 5,400 branch + 7,200 method; 1,800 exact seed-cell pairs; 1,800 receiver hashes; 100 seeds x 18 cells; SHA-256 `eb964eee9158199c6924a009349cc75060c58321c6d7c33cc7af3d4a64ef063b`.
- `artifacts/test/aggregate.json`: SHA-256 `6719815f626abcb22591faa314936b866179e07968e8a2872488088f12ac5a45`.
- `artifacts/test/terminal.json`: SHA-256 `28cdf26bc3425404bf9a2af1c7c62b2a4c9fe27863be70b5e02ba2be8316c4a1`.
- All confidence intervals used 2,000 valid seed-cluster bootstrap replicates with seed 20260811.

## Frozen gates

- G1 FAIL: event rate `0.03111111111111111` = 56/1,800; 95% CI `[0.023333333333333334, 0.03944444444444444]`; events appeared in 14 cells, but the frozen rate gate was 0.10.
- G2 FAIL: B0 relative BER regret `0.0011139930469593257`; 95% CI `[-0.0037853777588510414, 0.004947078027643515]`; outage excess `0.0`, 95% CI `[0.0, 0.0]`.
- G3 diagnostic FAIL: strongest cheap family `B2`; relative BER regret `0.0011139930469593257`; 95% CI `[-0.0039070138556545125, 0.0050624525100000425]`; outage excess `0.0`, 95% CI `[0.0, 0.0]`.
- G4 diagnostic FAIL: multi-source AUC `0.9932088567005196`, 95% CI `[0.9914536185610157, 0.9948471128134011]`; power-only AUC `0.9927444648753188`, 95% CI `[0.9906925260630407, 0.9944647496355705]`; delta `0.00046439182520086053`, 95% CI `[-0.0006746015744306083, 0.0016916433726503579]`.

## Unique terminal and claim ceiling

The first frozen fail-stop is G1/G2, therefore the unique terminal is `PROBLEM_ABSENT_OR_TOO_SMALL`. Later gates are diagnostic only and cannot change that terminal. The prior-art/novelty debt remains preserved. This result does not establish a problem-bearing candidate, method, novelty, Groundwork Go, or fair-comparison claim.
