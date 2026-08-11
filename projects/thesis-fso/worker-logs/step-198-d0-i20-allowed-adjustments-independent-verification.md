# Step 198 — D0 I20 allowed-adjustments independent verification

> 2026-08-11 | independent verifier | 15-minute hard stop

## Scope

- Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- Read-only review of `benchmark.py` and `test_d0_engineering_benchmark.py`.
- One fresh full engineering-benchmark test file and one direct CLI run to a temporary directory.
- No formal I20 artifact, science run, production/test edit, staging, commit, push, `common/`, or `p05_run*.log` mutation.

## Fresh evidence

- `test_d0_engineering_benchmark.py`: **36 passed in 51.35 s**; wall **52.982 s**.
- Temporary direct CLI: wall **21.529 s**, benchmark elapsed **9.735 s**, exit **2**.
- CLI status: `GREATER_THAN_7D_HARD_BLOCKER`; `incomplete_reasons=[]`.
- Required slices landed: decoder 4, BPS 6, B2 10, HMM aggregate 1, atomic JSONL 1, atomic receipt 1.
- Peak memory: process RSS 738,799,616 bytes; CUDA peak 0 bytes.

## Adjustment evidence

Scalar reference rate was `1.50387860002229 / 6 = 0.2506464333370483` seconds per polarization trajectory.

| Axis | Result | Measured rate | Speedup vs scalar | Evidence assessment |
|---|---:|---:|---:|---|
| vectorization | applicable | 0.10734248333028518 s/unit | 2.3350x | Actual NumPy batched formula; digest identical; manifest/materialized counts unchanged. |
| batch size | applicable, selected=2 | 0.05306490000414973 s/unit | 4.7235x | Candidates 1 and 2 actually measured; digest identical; selected global best. |
| content-addressed cache | N/A, 0 hits | receipt says 0.23346615000627935 s/unit | N/A | Exact sample keys are distinct and hits are correctly zero, but the recorded unit count is not the actual computation count; see P1. |
| checkpoint chunk size | applicable, selected=32 | 0.05346740000337983 s/unit | 4.6878x | Candidates 32, 128, and 684 actually measured; digest identical. |

All four receipts contain config, elapsed fields, digests/equivalence, unchanged logical-manifest SHA, and a materialized-projection source. Three applicable outputs equal the scalar output exactly (`max_abs_error=0`). Cache hits are zero because the two sampled content keys are distinct.

## Independent six-line recomputation

Using the landed atomic rows, receipt-selected HMM rate, frozen materialized counts, and the implementation's six-term equation:

| Term | Projected seconds |
|---|---:|
| setup (receipt-total residual) | 6.813000000081956 |
| decoder | 9,900.191999581642 |
| BPS | 434.88000000827014 |
| B2 | 4,150.740000003716 |
| HMM | 372,897.66530916095 |
| I/O | 19,581.7577999719 |
| **remaining total** | **406,972.04810872657 = 4.710324630888039 days** |

This exactly reproduces `remaining_work_days.bounded_runs_raw_rows_ci_and_receipts`. Together with 4.0 consumed engineering days, projected D0 is 8.710324630888039 days. Required remaining contingency is -3.7103246308880387 days, so the measured best allowed applicable adjustment still cannot close the frozen seven-day gate.

## Findings

### P1 — cache N/A receipt does not record the real after-unit count

For each of two distinct cache keys, the miss path calls `vector_once(1, best_chunk)`. That function traverses both polarization trajectories even at batch size 1, so the two misses perform four trajectory computations. The receipt nevertheless writes `after_unit_count=len(content_keys)=2`, and `physical_api_invocations` likewise adds only 2. Consequently the cache receipt's measured elapsed and unit count do not describe the same actual work. This violates the acceptance requirement that every allowed-adjustment receipt carry a real before/after unit count, even though the cache correctly reports zero hits and is not selected.

Minimal closure: compute only the indexed trajectory on each cache miss (or record the actual four computed trajectory units), then rerun the one focused verifier.

### P2 — I/O term is conservatively misattributed

`projected_compute_seconds()` names its argument `atomic_elapsed_seconds`, but `_run_authorized_operation()` passes whole benchmark elapsed. In this run that produces 19,581.758 projected I/O seconds from 9.735 whole-run seconds divided by 25 rows, rather than measuring the atomic write itself. The overestimate does not change the terminal: eliminating the entire I/O term would still leave about 4.484 days of remaining D0 work, far above the 1.0-day available remainder.

## Verdict

- P0/P1/P2: **0 / 1 / 1**.
- `FORMAL_I20_OPEN=NO` pending the minimal cache unit-accounting repair.
- The current completed temporary run otherwise supports a genuine `GREATER_THAN_7D_HARD_BLOCKER`: selected adjustment is independently correct, output equivalence and logical-manifest invariance hold, and the six-term total recomputes exactly.
