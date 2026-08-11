# Step 199 — D0 I20 cache unit-accounting repair

> 2026-08-11 | minimal P1 repair | GREEN

## Scope

- Changed only `benchmark.py`, `test_d0_engineering_benchmark.py`, and this log.
- Did not run formal I20 or S1–S4 science; did not modify `common/`, owner bytes, `.sessions/`, formal output, or `p05_run*.log`; did not stage, commit, or push.
- Step-198 P2 I/O attribution remains deliberately unchanged and nonblocking for this task.

## Root cause and repair

On each of two distinct cache misses, `vector_once(1, best_chunk)` traverses both polarization trajectories. The prior receipt recorded two after-units and added two physical invocations although four trajectory computations actually ran.

The repair counts `miss_output.size` for each executed miss, records the accumulated value as `config.actual_miss_compute_units` and `after_unit_count`, and adds that same value to `physical_api_invocations`. Cache semantics remain exact-content-only: both keys are distinct, so reads stay zero and applicability stays `NOT_APPLICABLE`.

## RED to GREEN

- RED: EB19 `1 failed, 35 deselected in 7.52s`; expected `actual_miss_compute_units`, but the field was absent.
- Focused GREEN: EB19 `1 passed, 35 deselected in 7.10s` (`8.21s` shell wall).
- Fresh whole-file GREEN: `36 passed in 74.05s` (`76.17s` shell wall).

## Temporary CLI evidence

One non-formal run to a unique OS temporary directory completed in `28.62s`:

```text
status=GREATER_THAN_7D_HARD_BLOCKER
physical_api_invocations=92
cache.after_unit_count=4
cache.config.actual_miss_compute_units=4
cache.actual_cache_reads=0
cache.applicability=NOT_APPLICABLE
logical_workload_sha256=635eb9bc718f7ffa52bbaed64c29b009ad87f3af7e5fdd9dd3bbf9bfcfbb84c3
selected_adjustment=checkpoint_chunk_size
projected_D0_days=11.626111515834822
```

The total invocation count reconciles as 46 non-HMM production calls plus 46 measured HMM trajectory computations. Timing-dependent projection changed, but allowed-adjustment semantics, selected-best rule, logical work, decoder state, and science scope did not.

## Hashes and verdict

```text
benchmark.py=5f210c206fac02e322040aa82cb7aa6cd4a654fdef6bb2e531c09c7ac503d11b
test_d0_engineering_benchmark.py=0c38201bb03c664cd9107967e9396a0dd741ba97f3f9262cfe912bca58e7bca6
P0=0
P1=0
```

VERDICT=`AUTHOR_GREEN_READY_FOR_ONE_FRESH_INDEPENDENT_ACCEPTANCE`; formal I20 and science remain closed.
