# Task 3 dev-freeze execution report

## Scope and preflight

- Scope: dev split and freeze preparation only; no held-out execution and no commit.
- Pre-existing artifact check: `artifacts/dev/raw.csv`, `artifacts/dev/aggregate.json`, and `freeze_receipt.json` were all absent before execution.
- Strict tests: `python -W error -m pytest projects/simulation/explore/dsp-outage-aware-combining -q` -> `42 passed in 0.34s`.
- Deployable information-boundary audit: `smoke_core.audit_deployable_information_boundary()` -> `()`.

## Dev execution

- Command invoked `run_split('dev', DEV_SEEDS, artifacts/dev, frozen=None)` exactly once.
- Runtime: 13.615 s.
- Produced raw path: `artifacts/dev/raw.csv`.
- Raw size: 1,391,433 bytes.
- Exact raw coverage: 6,480 rows, 360 seed-cell pairs, seeds `0..19`, 18 canonical cells, split only `dev`.
- Independent strict validation with materialized cell IDs (`tuple(cell.cell_id ...)`) passes.

## Freeze blocker

The required direct call `tune_dev(raw_rows)` failed before any tuning output was produced:

```text
ValueError: raw does not cover exact DEV_SEEDS/TEST_SEEDS x 18 cells
```

The raw coverage is complete. The failure is caused by `tune_dev` passing a generator expression as `expected_cells` to `_validate_raw_rows`; the validator builds a nested seed-by-cell Cartesian product, so that one-shot generator is exhausted after the first seed. Materializing the same IDs as a tuple makes the strict validator pass without changing raw data.

Per the task's fail-closed rule, execution stopped here. No threshold, top-L, strongest-cheap family, logistic coefficients, dev AUC, aggregate, or receipt was frozen. No source was edited and the raw split was not rerun or overwritten.

## Chronology state

`HELD_OUT_NOT_STARTED`

- `artifacts/dev/aggregate.json`: absent
- `freeze_receipt.json`: absent
- held-out artifacts: not created
- commit: not created

## Bounded-resume completion

The controller repaired only the generator-exhaustion caller defect. This worker resumed from the existing `raw.csv`; `run_split` was **not** invoked again.

### Raw integrity and renewed preflight

- Raw SHA256: `e509fc7cab49d6858e435f92f1e2920a0a666c06dd5877ce547ed1ee84dc2968`.
- Size/count remained exactly as the first report: 1,391,433 bytes; 6,480 rows; 360 seed-cell pairs; 20 seeds; 18 cells.
- Renewed strict tests: `43 passed in 0.58s`.
- Direct strict `tune_dev(raw_rows)`: PASS.
- Independent second raw read and `tune_dev`: byte-identical canonical sorted JSON for the complete frozen tuning object.

### Frozen dev tuning

- B1 fixed threshold: `tau = -8.0 dB`.
- B2 top-L: `K=2 -> L=2`; `K=4 -> L=4`.
- Strongest cheap family: `B2`.
- Dev mean BER, explicitly NON-TEST/NON-SCIENTIFIC: B1 `0.18675504552296607`; B2 `0.1865809548862291`.
- Dev-only diagnostic AUCs, explicitly NON-TEST/NON-SCIENTIFIC: power-only `0.992680121300847`; multi-source `0.9960665706770485`; delta `0.0033864493762014725`.
- Coefficient/range audit: every coefficient, intercept, mean, scale, and observed feature range finite; minimum fitted scale `0.1515692552726698`; maximum absolute intercept/coefficient `9.26403042097078`; singularity guard PASS.

### Immutable freeze receipt

- Dev aggregate: `artifacts/dev/aggregate.json`; SHA256 `f7bcfb2d1342e3efccfb6cb39489e7cbe62426595f55595170ee1f674df72c80`.
- Receipt: `freeze_receipt.json`; SHA256 `5d958f8bc64320f0010937c1011d3fb5165d2194bded62f0ad81526e7a95242e`.
- Receipt state: `test_started=false`; bootstrap replicates `2000` clustered by seed.
- Validator re-read PASS. Independent SHA256 recomputation matched all seven required entries: design, implementation plan, core, runner, tests, dev raw, and dev aggregate.

Final chronology state: `HELD_OUT_NOT_STARTED`. No commit was created by this worker.
