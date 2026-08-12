# Task 2 bounded repair report

## Review findings verified

The review issues reproduced in the current files: receipt validation accepted an empty hash map and partial frozen state; raw validation did not own the exact split/grid/candidate schema; O1 reused estimated-channel MRC; G2/G3 bootstrapped an already filtered event table; O1 ran before deployable arms; and raw output could be overwritten.

## RED evidence

After adding the review regression tests and before repair:

```text
python -m pytest test_smoke.py -q
9 failed, 26 passed in 0.35s
```

Failures covered the truth-channel oracle, explicit unit-validation API, strict DEV coverage, receipt manifest/frozen validation, and raw overwrite refusal.

A focused bootstrap test then failed with `valid_replicates == 20`, proving G2 was still sampling only event seeds. The synthetic fixture contained two event and two no-event seeds. After changing the sampler to draw all seed clusters and filter events inside each replicate, the fixed-seed test reports fewer than 20 valid replicates as required.

## Repairs

- Receipt writer and validator now require the exact seven-key manifest: design, implementation plan, core, runner, tests, dev raw, and dev aggregate. Every file and digest is checked. Frozen B1, exact K2/K4 top-L keys/ranges, strongest family, finite dev means, exact diagnostic feature schemas, dimensions, and finite coefficients are fail-closed.
- Strict mode is now the default. Dev tuning requires exact `DEV_SEEDS × 18 cells`; final aggregation requires test split and exact `TEST_SEEDS × 18 cells`. Unit mode relaxes only global cardinality, not row schema, branch counts, candidate completeness, uniqueness, or pair identity.
- Merge validates each part internally and rejects duplicate/missing branch or method candidates as well as cross-part duplicate/missing seed-cell pairs.
- O1 now enumerates subsets with actual complex branch gains and equal-noise truth-channel MRC weights. Receiver-visible branch pilot correction has already removed the estimated shared phase; `truth.shared_phase` is therefore not applied a second time. It remains evaluator-only.
- Every deployable B0/B1/B2 output is constructed before O1 is called.
- G2/G3 resample all test seed clusters, reconstruct event membership inside each replicate, mark no-event replicas invalid/NaN, and expose `valid_replicates`.
- Raw CSV creation refuses any existing target.

## GREEN evidence

```text
python -W error -m pytest test_smoke.py -q
35 passed in 0.31s

python -m py_compile smoke_core.py run_smoke.py test_smoke.py
exit 0
```

No dev or held-out execution was started. No commit was made.

## Residual risk

The strict scientific cardinality path is contract-tested through negative/unit fixtures but remains intentionally unexecuted until the controller starts dev. Large finite coefficients from near-separated dev logistic data remain a review item for the freeze receipt, not a reason to tune on held-out data.

## Second bounded pre-dev repair

### RED

The new equal-noise contract tests failed at collection with:

```text
ImportError: cannot import name 'COMPLEX_NOISE_VARIANCE' from 'smoke_core'
1 error in 0.27s
```

This directly confirmed the generator had no explicit common-noise convention. Inspection also confirmed the prior code implemented branch SNR offsets by changing each branch's noise variance, which contradicted the equal-noise MRC premise.

### Repair

- Defined complex AWGN variance as `E[|n|²]=1` for every branch (`I/Q` variance 0.5 each).
- Moved H0/H1/H2 offsets entirely into the effective complex gain through `10^(offset_dB/20)`. Truth now records both unscaled Gamma-Gamma gain and effective gain; instantaneous SNR is exactly `10log10(|effective_gain|² / noise_variance_complex)`.
- Added analytic checks for the −6 dB effective-gain factor and truth-channel equal-noise O1 output.
- Raw validation now requires one receiver hash per seed-cell pair, enforces canonical `cell_id ↔ turbulence/K/heterogeneity`, and validates frozen GG/SNR/status metadata whenever present; strict generated rows require that metadata.
- `run_split` checks for an existing `raw.csv` before receipt validation or realization generation.
- Freeze receipt creation refuses an existing target.
- Updated `design.md` to state the common-noise and signal-amplitude offset convention.

### Final GREEN

```text
python -W error -m pytest test_smoke.py -q
39 passed

python -m py_compile smoke_core.py run_smoke.py test_smoke.py
exit 0
```

No dev/held-out realization was run and no commit was made.

## Runtime repair: strict dev Cartesian validation

A complete synthetic `20 DEV_SEEDS × 18 canonical cells` raw fixture reproduced the strict tuning failure:

```text
ValueError: raw does not cover exact DEV_SEEDS/TEST_SEEDS x 18 cells
1 failed in 0.28s
```

Root cause: `tune_dev` passed a generator of canonical cell IDs into a nested seed×cell comprehension. The first seed exhausted it, so the expected set omitted cells for the remaining 19 seeds. The repair materializes the 18 IDs once as a tuple before validation; no tuning or scientific behavior changed.

Final verification:

```text
python -W error -m pytest test_smoke.py -q
40 passed in 0.61s
python -m py_compile smoke_core.py run_smoke.py test_smoke.py
exit 0
```

Existing `artifacts/dev/raw.csv` was not read, modified, or rerun. No held-out execution or commit occurred.
