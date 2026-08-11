# Step 121 — D0 I03 waveform GREEN continuation

> 2026-08-10 | T075 / D011 / V005 / CP012 / epoch 12 | D0_TESTBED_IMPLEMENTATION + D0_UNIT_TEST
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `PASS / WC01–WC03/WC08 GREEN`

## 1. Frozen continuation receipt

The T075 continuation began from the valid module-absent RED and did not edit
the frozen test or step-117 receipt.

```text
test_d0_waveform_channel.py=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-117=9dd643651980c812ae7ef1dd4852faf1849b7b5043656b1d4106deb97b936bbb
RED_output=6f15c28fa57ce080fdb4bebd8f27237f3956b5aaad12ec5f3570bba2bf0ab3b6
waveform.py=ABSENT
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
python=3.11.9
numpy=2.4.3
```

Pre-write cache census was unchanged from step-117:

```text
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

## 2. Minimum production implementation

`waveform.py` implements the four frozen public APIs with frozen/slotted value
types and defensive read-only array copies:

- `registered_prefix()` locally constructs `Generator(PCG64(987654321))`,
  generates int64 bits then uint8 canonical bytes, applies owner Gray axis
  `[-3,-1,3,1]`, and derives all registered arrays and energy.
- `registered_pilots(N)` generates the four-symbol unit-energy QPSK cycle and
  expands it by owner count `1 + ceil(6144/(N-1))`; no expected SHA is returned
  or hardcoded by production.
- `build_waveform(data_symbols, *, N)` places 32 prefix samples, then repeated
  pilot + at-most-`N-1` data groups, then the terminal pilot. It preserves all
  6144 data ranks, writes int64 bijective maps, and leaves all known positions
  `-1` in `time_to_data`.
- `apply_persistent_rotation(...)` accepts only the registered target,
  boundary, and integer four-state domains; it copies before rotating the
  target physical suffix from `data_to_time[boundary]`, including later
  pilots. Known references, maps, pre-boundary samples, source build, and the
  sentinel polarization remain byte-identical.

Production SHA256 after implementation:

```text
waveform.py=bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748
```

## 3. Ordered node GREEN receipts

All commands used:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact-node> -q
```

Exact cwd was
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` and the
frozen test SHA remained
`b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d`.

| Order | Exact node suffix | Result | Process duration | stdout/stderr SHA256 |
|---:|---|---|---:|---|
| WC01 | `test_d0_waveform_channel.py::test_registered_prefix_bytes_hashes` | 1 passed / exit 0 | 0.712 s | `420148db9e0b69209165e34674193ac580cc29b79b121aeba98eef98d79c0cbe` |
| WC02 | `test_d0_waveform_channel.py::test_registered_pilot_hashes_counts` | 1 passed / exit 0 | 0.732 s | `2901e9dfa0b5714aa099acfe610f3c4dbfa0c352070d16e8a4538d7da5df8462` |
| WC03 | `test_d0_waveform_channel.py::test_data_time_map_bijective` | 1 passed / exit 0 | 0.727 s | `c650684da631a53569764f5af8f60c3e0d0a19a4321a45fbbac8d3f55d3a7118` |
| WC08 | `test_d0_waveform_channel.py::test_controlled_jump_copy_on_write` | 1 passed / exit 0 | 0.740 s | `a627885f4b9efaac136d48977c38ccc0cf413d2b07f0c2dca5d54f69518b7604` |

No warning, skip, xfail, or hidden failure occurred.

## 4. File and regression GREEN

```text
test_d0_waveform_channel.py: 4 passed in 0.23s
exit_code=0
process_duration_seconds=0.774
stdout_stderr_sha256=9014148bf4cf2566816306a054dca6e4be01a09ee682786ddc706031961aeb96

test_d0_contract_views.py: 6 passed in 0.32s
exit_code=0
process_duration_seconds=0.864
stdout_stderr_sha256=9ba081880e51bdfef80694dbd655cd5b4e5753da3eebefbbe9fc562ba50a56f4
```

An additional no-file inline check returned
`DEFENSIVE_READONLY_AND_VALIDATION_PASS=1`: source mutation did not affect the
built waveform, every public asset/build array was read-only, and unregistered
N/shape/target/boundary/state inputs all failed closed.

## 5. Protection receipt and terminal

Post-test protection state before final log sealing:

```text
test_d0_waveform_channel.py=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-117=9dd643651980c812ae7ef1dd4852faf1849b7b5043656b1d4106deb97b936bbb
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Only `waveform.py` and this step-121 log were written in T075. The frozen test
and step-117 hashes did not move. No benchmark, science, web/search/download,
dependency install, commit, or push occurred.

```text
VERDICT=PASS
WC01=GREEN 1/1
WC02=GREEN 1/1
WC03=GREEN 1/1
WC08=GREEN 1/1
FILE_GATE=GREEN 4/4
CONTRACT_REGRESSION=GREEN 6/6
TERMINAL=I03_READY_FOR_INDEPENDENT_VERIFICATION
```
