# Step 192 — D0 I20 engineering throughput gate

> 2026-08-11 | bounded non-scientific benchmark | INCOMPLETE | one CLI invocation only

## Terminal

```text
TERMINAL=INCOMPLETE
EXIT_CODE=1
PROCESS_WALL_SECONDS=2.8
WATCHDOG_SECONDS=720
FAILURE_POINT=CLI_MAIN_BEFORE_RUNNER
D0_SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
BER_CONCLUSION=NONE
GOODPUT_CONCLUSION=NONE
METHOD_GAIN_CONCLUSION=NONE
```

The frozen I20 command was invoked exactly once. It failed before starting the
engineering worker because `benchmark.main()` rejected the absent injected
runner:

```text
BenchmarkError: real benchmark runner is unavailable before I20 authorization
```

Per the I20 timebox and failure discipline, no code was repaired, no alternate
entry point was attempted, and the command was not run a second time.

## Precondition evidence

- I19D final integration review: `PASS`, `P0=0`, `P1=0`,
  `I20_AUTHORIZATION=OPEN`.
- I19D receipt path:
  `projects/thesis-fso/worker-logs/step-191-d0-i19d-final-integration-review.md`
- I19D file SHA-256:
  `0c59730387a7010d48bacb73d5fab475a4a519f12ee6fd2d54f4d67ec1fb0854`

## Exact command

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B 'projects/simulation/explore/coded-decoder-feedback/benchmark.py' --class ENGINEERING_THROUGHPUT_V1 --root-seed 900000001 --watchdog-seconds 720 --synthetic-resolved-freeze --output 'projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput'
```

## Required-slice evidence

No benchmark operation started, so all actual slice counts are zero:

| Required evidence | Required | Actual |
|---|---:|---:|
| decoder batch sizes | 4 (`4/8/12/16`) | 0 |
| BPS pairs on one waveform | 6 | 0 |
| unique B2 views | 10 | 0 |
| HMM primitive/aggregate slice | 1 | 0 |
| real atomic JSONL/receipt write | 1 | 0 |

The output path
`projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput`
is absent. No artifact or receipt exists, and therefore there is no artifact or
receipt SHA-256 to report.

## Workload and owner record

The frozen pre-run workload remains unchanged but was not measured:

```text
logical decoder batches=69,360
logical CW decodes=1,032,000
logical BP iterations=20,640,000
materialized decoder batches=48,900
materialized CW decodes=704,640
materialized BP iterations=14,092,800
HMM dual-pol aggregate scores=8,344,800
HMM logical primitive scores=16,689,600
HMM materialized primitive scores=7,027,200
```

Because the runner never started, logical/materialized reconciliation,
physical API invocations, cache hits, wall-time projection, peak memory, and the
nine-field owner record are `NOT_PRODUCED`.

Authoritative owner:

```text
owner_path=projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml
owner_sha256=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
benchmark_sha256=9b314bc23c60165580e687c48e5834200de9cc4287ed1b47b0c53c1274caed2b
```

## Budget evidence

The owner freezes six D0 line items:

| Work ID | Frozen days | Consumed receipt | Remaining receipt |
|---|---:|---|---|
| `contract_source_and_asset_closure` | 0.25 | NOT_PRODUCED | NOT_PRODUCED |
| `receiver_truth_views_and_carrier_realization` | 0.75 | NOT_PRODUCED | NOT_PRODUCED |
| `B0_B1_O1_mapping_and_controlled_fixture` | 0.50 | NOT_PRODUCED | NOT_PRODUCED |
| `source_explicit_B2_adaptation_and_dev_freeze` | 2.00 | NOT_PRODUCED | NOT_PRODUCED |
| `strata_tests_statistics_and_cost_ledger` | 0.50 | NOT_PRODUCED | NOT_PRODUCED |
| `bounded_runs_raw_rows_ci_and_receipts` | 0.50 | NOT_PRODUCED | NOT_PRODUCED |

Frozen D0 subtotal is `4.50 d`, post-D0 C1 is `2.00 d`, contingency is
`0.50 d`, and the hard ceiling is `7.00 d`. The required receipt equation is:

```text
projected_D0_days = consumed_engineering_days + projected_remaining_D0_days
contingency_consumed_days = max(0, projected_D0_days - 4.50)
required_remaining_contingency_days = 0.50 - contingency_consumed_days
projected_mission_days = consumed_engineering_days
                       + projected_remaining_D0_days
                       + 2.00
                       + required_remaining_contingency_days
```

Actual `consumed_engineering_days`, `projected_remaining_D0_days`,
`contingency_consumed_days`, `required_remaining_contingency_days`, and
`projected_mission_days` are all `NOT_PRODUCED`. Completed/remaining work-ID
partitions are also absent, so non-overlap and completeness cannot be claimed.
This is why the terminal is `INCOMPLETE`, not PASS and not a greater-than-seven-day
hard blocker.

## Protection and repository checks

Immediately after the failed invocation and before this log was written:

```text
staged_entries=0
common_status_entries=0
protected_p05_status_entries=4 (all pre-existing untracked)
simulation_pycache_dirs=20
simulation_pyc_files=121
output_entries=0
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

Protected P05 SHA-256 values remained:

```text
p05_run.log  7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log 735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log 95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

No `common/`, production, test, session, owner, or protected P05 file was
modified by this task. No file was staged, committed, or pushed.

## STOP_REASON

`INCOMPLETE_CLI_RUNNER_UNAVAILABLE` — the only authorized command failed at
the CLI boundary in 2.8 seconds, before any slice, record, budget projection,
or atomic artifact could be produced. Science remains `NOT_RUN`; method signal
remains `NONE`.
