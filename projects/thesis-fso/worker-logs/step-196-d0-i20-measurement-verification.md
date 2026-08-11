# Step 196 — D0 I20 owner-sized measurement final-byte independent verification

> 2026-08-11 | independent bounded acceptance | FAIL | hard stop within 15 minutes

## Verdict

```text
VERDICT=FAIL
P0=0
P1=1
P2=0
FORMAL_I20_OPEN=NO
EXPECTED_FORMAL_TERMINAL=UNRESOLVED
D0_SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
BER_CONCLUSION=NONE
GOODPUT_CONCLUSION=NONE
METHOD_GAIN_CONCLUSION=NONE
```

The step-195 final bytes close all three step-194 measurement-unit defects:
BPS, B2, HMM, process/device memory, and actual cache-read accounting now use
the required production-sized units.  The remaining blocking defect is not a
slice defect.  The landed temporary receipt labels the unadjusted scalar HMM
extrapolation `GREATER_THAN_7D_HARD_BLOCKER` without any measured before/after
receipt for the four owner-authorized engineering adjustments.  The I20
terminal requires evidence that those adjustments cannot close the budget;
the current bytes do not provide it.

## Fresh execution evidence

### EB full file

```text
command=C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider projects\simulation\tests\test_d0_engineering_benchmark.py -q --durations=10
result=35 passed in 21.69s
shell_wall_seconds=22.6374758
exit_code=0
slowest=EB12 real runner 8.73s
```

### One non-formal direct-script run

The direct script used one unique OS temporary output and a 60-second external
tool watchdog.  Its inner frozen CLI watchdog remained exactly 720 seconds.
The repository formal output path was absent before and after this run.

```text
temp_root=C:\Users\zzt\AppData\Local\Temp\d0-i20-final-verify-a9786696d4a341bba7766a406b0f4209
process_exit=2
process_wall_seconds=8.7857458
outer_watchdog_timeout=false
reported_status=GREATER_THAN_7D_HARD_BLOCKER
reported_operation_elapsed_seconds=2.452999999979511
decoder_batches=4 [4,8,12,16]
bps_pairs=6
b2_views=10
hmm_primitive_aggregate_rows=1
atomic_jsonl=1
atomic_receipt=1
slice_rows=21
slice_sha256=29eb93b35833c913252d2a9c7cf1da7a37578430e32ee97b41be599967d820bb
receipt_sha256=3a8513c6547cd6af2dcd743b787f8acd7c09d27fdacb7cbb144e8578948d51b5
```

## Owner-sized slices and runtime record

```text
BPS input shape per pair=[6860,6860]
BPS composition per polarization=6144 data + 32 prefix + 684 periodic pilots
BPS production calls=2 per pair, 12 total
BPS elapsed per pair=0.05,0.05,0.05,0.08,0.08,0.08 s

B2 production calls=10
B2 samples shape=[2,6144]
B2 posterior shape=[2,6144,4]
B2 codewords=16 unique CW IDs per polarization
B2 decode lifecycle=one fresh decode per polarization per view
B2 elapsed per view=0.14-0.17 s; aggregate=1.57800000003772 s

HMM production trajectories=2 polarizations
HMM pilots per trajectory=684
HMM measured aggregate=0.2809999999590218 s
HMM projection denominator=2 measured primitive polarization trajectories

physical_api_invocations=48
cache_hits=0
peak_memory.process_rss_peak_bytes=739885056
peak_memory.accelerator_backend=torch.cuda
peak_memory.accelerator_peak_bytes=0
```

The API invocation count reconciles as decoder `4` + BPS `12` + B2
`10 * (one run_b2 + two fresh decodes) = 30` + HMM `2` = `48`.  No result
cache is read, so `cache_hits=0` is exact.

## Owner, workload, partition, and budget

```text
owner_budget_sha256=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
workload_manifest_sha256=635eb9bc718f7ffa52bbaed64c29b009ad87f3af7e5fdd9dd3bbf9bfcfbb84c3
seconds_per_day=86400

logical.decoder_batches=69360
logical.cw_decodes=1032000
logical.bp_iterations=20640000
logical.hmm_dual_pol_frame_parameter_pair_scores=8344800
logical.hmm_primitive_pol_trajectory_parameter_pair_scores=16689600
logical.materialized_hmm_primitive_pol_trajectory_parameter_pair_scores=7027200

materialized.decoder_batches=48900
materialized.cw_decodes=704640
materialized.bp_iterations=14092800
materialized.hmm_primitive_pol_trajectory_parameter_pair_scores=7027200
```

The six frozen D0 line items form an exact disjoint partition:

```text
completed contract_source_and_asset_closure=0.25d
completed receiver_truth_views_and_carrier_realization=0.75d
completed B0_B1_O1_mapping_and_controlled_fixture=0.50d
completed source_explicit_B2_adaptation_and_dev_freeze=2.00d
completed strata_tests_statistics_and_cost_ledger=0.50d
remaining bounded_runs_raw_rows_ci_and_receipts=11.55639062939125d
```

The complete frozen equation in the temporary receipt is:

```text
consumed_engineering_days=4.0
projected_remaining_D0_days=11.55639062939125
projected_D0_days=4.0+11.55639062939125=15.55639062939125
post_D0_C1_days=2.0
contingency_consumed_days=max(0,15.55639062939125-4.50)=11.05639062939125
required_remaining_contingency_days=0.50-11.05639062939125=-10.55639062939125
projected_mission_days=15.55639062939125+2.0-10.55639062939125=7.000000000000002
```

The negative remaining contingency correctly prevents PASS despite the
algebraic mission-day cancellation.

## P1 finding — allowed-adjustment terminal evidence is absent

Owner-authorized adjustments are `vectorization`, `batch_size`,
`content_addressed_cache`, and `checkpoint_chunk_size`.  The current code has
only `apply_engineering_adjustments(...)` plus EB09's synthetic count mutation.
The production path never calls it; `BenchmarkReceipt` records neither an
adjustment name nor before/after measured units; no adjusted production slice
or adjusted budget receipt exists.

The unadjusted projection decomposes as:

```text
decoder=3294.19199958164 s
BPS=180.0 s
B2=1798.920000043 s
HMM=987321.599856019 s
atomic_IO=5874.00052376046 s
setup=3.43799999995463 s
remaining_total=998472.150379404 s = 11.55639062939125d
HMM_share=98.8832387043396%
```

With 4.0 days already consumed, the remaining work must be at most 1.0 day to
keep the seven-day mission ceiling.  Holding the measured non-HMM work fixed,
the HMM term must fall from `987321.599856019 s` to at most
`75249.4494766149 s`, a `13.1206488116946x` speedup.  HMM vectorization,
batching, and chunking are expressly allowed and are not measured here.  There
is therefore no evidence that they close the gap, but also no evidence that
they cannot close it.  The temporary hard-blocker label is not yet a genuine
I20 terminal and cannot be accepted as PASS or as an established hard blocker.

## Protection

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
benchmark.py=7862885c3fa88b8f0fda81c9f213c9f002d7a66b70e2cef7d80f7d77a0772b5b
test_d0_engineering_benchmark.py=8879330cf1cece75cfc18c83149af4f7b431aa7a2471062206cd20828c29e68b
owner=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
staged_entries=0
common_diff_entries=0
formal_output_path_exists=false
```

The four protected P05 files remained untracked/unstaged with their accepted
hashes unchanged:

```text
p05_run.log  7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log 735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log 95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## Next legal code task

Add the smallest production measurement path that executes and records the
allowed HMM/vectorization-batch-chunk alternatives without changing logical
work, forbidden axes, decoder state, or science scope.  Emit exact before/after
receipts and rerun one affected EB file plus one final independent acceptance.
Formal I20 and S1-S4 remain closed meanwhile.
