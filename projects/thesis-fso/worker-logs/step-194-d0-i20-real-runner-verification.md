# Step 194 — D0 I20 real-runner final-byte independent verification

> 2026-08-11 | independent merged acceptance | FAIL | bounded non-scientific verification only

## Verdict

```text
VERDICT=FAIL
P0=0
P1=3
P2=0
FORMAL_I20_OPEN=NO
D0_SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
BER_CONCLUSION=NONE
GOODPUT_CONCLUSION=NONE
METHOD_GAIN_CONCLUSION=NONE
```

The final bytes execute and land the requested representative files, but the
runtime measurements do not preserve the owner workload units. The resulting
`ENGINEERING_THROUGHPUT_PASS` receipt therefore cannot yet open formal I20.

## Fresh execution evidence

### EB full file

```text
command=C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest projects\simulation\tests\test_d0_engineering_benchmark.py -q --durations=5
result=30 passed in 45.85s
shell_wall_seconds=47.0267661
exit_code=0
slowest=EB12 real runner 16.36s
```

The 30 passing pytest nodes contain 27 explicit reject/INCOMPLETE controls
(including 17 invalid owner-record value cases). Node-level expected outcomes
were 30/30 and embedded negative controls were 27/27; wrong accept/reject was
`0/0` for the assertions that exist.

### One non-formal direct-script run

The direct script was run once against a unique OS temp directory, with a
60-second external hard watchdog. The frozen inner CLI authority remained
exactly 720 seconds; the formal repository output path was not used.

```text
temp_root=C:\Users\zzt\AppData\Local\Temp\d0-i20-verify-7c0fb0e920e54658bf0f87f342de40bb
process_exit=0
process_wall_seconds=16.2801068
outer_watchdog_timeout=false
reported_status=ENGINEERING_THROUGHPUT_PASS
reported_operation_elapsed_seconds=0.5630000000237487
decoder_batches=4 [4,8,12,16]
bps_pairs=6
bps_unique_waveform_sha=1
b2_views=10
b2_unique_result_sha=10
hmm_primitive_aggregate_rows=1
atomic_jsonl=1
atomic_receipt=1
slice_rows=21
slice_sha256=c53cb7c82d0e4aeef2af64ba9131cd10370771d8d90a5872e79af27235903e4e
receipt_sha256=947ff32b8a9dd9761a6cfb6a694e95fd3b9406c244dd07a647027526fc3c6dec
```

EB07 independently exercised the Windows spawn watchdog and verified that a
late worker is terminated before its marker can be written. Worker
construction also preserved the parent interpreter path exactly:

```text
sys.path before == sys.path after: true
simulation-root occurrences before/after: 0/0
watchdog_call default: 720
build_benchmark_receipt default: 720
CLI exact authority: 720
```

## Slice and owner/budget receipt

The landed temp receipt was bound to the real owner bytes:

```text
owner_budget_sha256=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
workload_manifest_sha256=635eb9bc718f7ffa52bbaed64c29b009ad87f3af7e5fdd9dd3bbf9bfcfbb84c3
physical_api_invocations=24
logical_batches=4
reported_cache_hits=5
wall_time=0.5630000000237487
peak_memory=2791081
projected_full_D0_time=353667.75052387756s
```

The six owner work IDs formed a complete, disjoint `5 completed + 1 remaining`
partition. The receipt computed:

```text
consumed_engineering_days=4.0
projected_remaining_D0_days=0.0933767421745084
projected_D0_days=4.093376742174509
post_D0_C1_days=2.0
contingency_consumed_days=0.0
required_remaining_contingency_days=0.5
projected_mission_days=6.593376742174509
```

No `raw_s1`-`raw_s4`, estimand, gate, science-writer, fit, or seed-registration
path was present in `benchmark.py`; no scientific seed or S1-S4 path ran.

## P1 findings

### P1-1 — Throughput units are smaller surrogates than the owner workload

The required slice counts exist, but their timed units are not the units used
by the projection:

- BPS times one 512-symbol synthetic waveform, while the owner waveform keeps
  6144 coded data symbols plus prefix/pilots. The code multiplies the six-pair
  time by 480 without a full-waveform length factor (minimum visible ratio
  `6208/512 = 12.125`, before tuple-dependent periodic pilots).
- Each B2 view evaluates only `self._waveform_samples[:8]` with a fabricated
  fixed four-state posterior. The production `run_b2` contract requires two
  polarizations of exactly 6144 symbols and 6144 state posteriors per
  polarization. The projection multiplies the eight-symbol timing by 11,400
  views without the structural `6144/8 = 768` factor and without timing the
  production B2 call.
- The HMM slice calls `emission_log_weight` four times for one symbol. The owner
  unit is one per-polarization trajectory/parameter-pair score over 32-684
  pilots. This run measured the HMM row as exactly `0.0s`, then multiplied that
  zero by 7,027,200 materialized trajectory scores.

Therefore `projected_remaining_D0_days=0.093376742...` is not an owner-bound
projection and the emitted PASS is a wrong acceptance outside the currently
implemented pytest oracle.

### P1-2 — `peak_memory` is Python-trace memory, not process/device peak memory

`tracemalloc` excludes NumPy/Sionna/Torch native allocations and CUDA/device
memory. The receipt's `2,791,081` bytes cannot serve as the owner-required peak
memory record for the actual decoder/BPS/B2 kernels. A process RSS and, when
applicable, accelerator peak measurement are required.

### P1-3 — `cache_hits=5` reports shared input reuse as cache hits

All six distinct `(B,Nw)` BPS calls execute. The code nevertheless records
`len(bps_slices)-1 = 5` cache hits because they share one waveform object. No
cached BPS result is read, so the owner record overstates actual content-cache
hits.

## Protection

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
benchmark.py=4f49fa9f81d05b0af5a4a55ad9fd07cc5a69a7c2cc7ddc2be7cac01dbd45c040
test_d0_engineering_benchmark.py=1bdd8dd5ab98f6d8e54bb92fe04dec13f2635c1f6e2093aa705861147bbc6c7e
owner=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
staged_entries=0
common_diff_entries=0
formal_output_path_used=false
```

Protected P05 hashes remained exact:

```text
p05_run.log  7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log 735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log 95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## Next legal code task

One bounded I20 repair should replace the BPS/B2/HMM surrogate timing units
with owner-sized production-kernel units, record real process/device peak
memory, and count only actual cache reads. Then run one fresh EB full-file plus
one temp-output direct-script acceptance. Formal output and science remain
closed until that single re-verification reaches `P0=0, P1=0`.
