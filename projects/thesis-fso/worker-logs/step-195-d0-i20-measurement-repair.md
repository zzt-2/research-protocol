# Step 195 — D0 I20 measurement repair

> 2026-08-11 | author repair | DONE | bounded non-scientific engineering slice only

## Boundary

- Modified only `benchmark.py` and `test_d0_engineering_benchmark.py`; added this worker log.
- Did not run formal I20 or S1–S4 science. Did not modify `common/`, the owner, sessions, or any `p05_run*.log`; did not stage, commit, or push.
- Input finding: Step 194 `P0=0, P1=3`; formal I20 remained closed.

## Actual code

- Replaced the 512-symbol BPS surrogate with a registered dual-polarization waveform containing `6144 data + 32 prefix + 684 periodic pilots = 6860` samples per polarization. Every `(B,Nw)` slice calls production `receiver.run_common_bps` once per polarization.
- Replaced the eight-symbol/fabricated-posterior B2 surrogate with production `b2.run_b2` on exact `(2,6144)` samples and `(2,6144,4)` posteriors, exact 16 unique CW IDs per polarization, and one fresh decode per polarization.
- Replaced four single-symbol emission calls with two real per-polarization `pilot_state_posterior` trajectory/parameter-pair calls, each spanning the owner-valid 684-pilot schedule. Projection now divides by the two measured trajectory units before multiplying by the frozen `7,027,200` materialized trajectory count.
- Replaced `tracemalloc` with OS process RSS peak (`GetProcessMemoryInfo` on Windows; `getrusage` fallback) and records the applicable `torch.cuda` peak explicitly. `peak_memory` remains one owner field but is now a structured process/device record.
- Added an explicit `cache_hits` counter. Because all six distinct BPS results are executed and no result cache is read, the landed value is `0`.

## RED → GREEN

- Initial focused RED: `4 failed, 1 passed, 30 deselected in 0.38s`; the four failures were missing owner waveform fields, no production `run_b2` call, no measured HMM trajectory units, and no process/device peak API. The initially passing cache node was invalid because its fixture prefilled zero; that fixture assignment was removed and a fresh run produced the expected `AttributeError` RED (`1 failed, 34 deselected in 0.37s`).
- Focused GREEN: `5 passed, 30 deselected in 2.35s`.
- First EB file run exposed an obsolete test oracle that required PASS from every real engineering measurement: `1 failed, 34 passed in 21.78s`; the real owner-sized slice correctly returned the alternative authorized terminal `GREATER_THAN_7D_HARD_BLOCKER`. The test now checks exact CLI/status agreement for either authorized measured terminal.
- Fresh EB full-file GREEN: `35 passed in 21.83s`; shell wall `22.7656096s`; slowest node EB12 `8.81s`.

## Fresh owner-sized temp evidence

This was pytest temporary output, not the formal repository I20 output.

```text
BPS: 6 pairs; each input shape=[6860,6860]; elapsed per pair=0.05–0.09s
B2: 10 production run_b2 calls; samples=[2,6144]; posterior=[2,6144,4]; elapsed per view=0.14–0.19s
HMM: 2 polarization trajectories; 684 pilots each; elapsed aggregate=0.31s
physical_api_invocations=48
cache_hits=0
wall_time=2.6560000000172295s
peak_memory.process_rss_peak_bytes=739340288
peak_memory.accelerator_backend=torch.cuda
peak_memory.accelerator_peak_bytes=0
temp measured status=GREATER_THAN_7D_HARD_BLOCKER
projected_remaining_D0_days=12.824683198045857
```

The temporary status is measurement evidence only; formal I20 remains NOT_RUN pending one fresh independent acceptance of this repair.

## Protection and hashes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
benchmark.py=7862885c3fa88b8f0fda81c9f213c9f002d7a66b70e2cef7d80f7d77a0772b5b
test_d0_engineering_benchmark.py=8879330cf1cece75cfc18c83149af4f7b431aa7a2471062206cd20828c29e68b
git_diff_check=PASS
common_diff_entries=0
protected_p05_diff_entries=0
```

## Author disposition

```text
REPAIR_STATUS=DONE
KNOWN_P0=0
KNOWN_STEP194_P1_REMAINING=0
FORMAL_I20=NOT_RUN
D0_SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
NEXT=one fresh bounded independent acceptance of the affected EB/benchmark axes
```
