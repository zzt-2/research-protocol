# Step 117 — D0 I03 registered waveform assets (TDD)

> 2026-08-10 | T071 / D011 / V005 / CP012 / epoch 12 | D0_UNIT_TEST
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Status: `INCOMPLETE / VALID_RED_CAPTURED / PRODUCTION_ABSENT`

## 1. Scope and frozen-input preflight

Only I03 WC01–WC03/WC08 is in scope. No benchmark, scientific seed/estimand,
DEFECT_SMOKE, S1–S4, adapter/policy, web/search/download, commit, or push was
run. The only authorized targets are `waveform.py`,
`test_d0_waveform_channel.py`, and this log.

Frozen identities matched before the first target write:

```text
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_d0_contract_views.py=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
waveform.py=ABSENT
test_d0_waveform_channel.py=ABSENT
step-117=ABSENT
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

Protected p05 SHA256 values before the RED run:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 2. TDD RED receipt

```text
receipt_schema=d0.tdd.red.v1
receipt_id=step117-i03-red-wc01-wc03-wc08
phase=RED
time=2026-08-10T16:03+08:00
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
env.PYTHONDONTWRITEBYTECODE=1
env.PYTHONHASHSEED=0
test_sha256=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
production_before=ABSENT
production_after=ABSENT
exit_code=1
duration_seconds=0.688
tests_executed=4
failed=4
errors=0
skipped=0
xfail=0
stdout_stderr_sha256=6f15c28fa57ce080fdb4bebd8f27237f3956b5aaad12ec5f3570bba2bf0ab3b6
expected_failure=new module absent bootstrap RED
observed_failure=ModuleNotFoundError: No module named 'waveform'
```

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_waveform_channel.py::test_registered_prefix_bytes_hashes' `
  'projects/simulation/tests/test_d0_waveform_channel.py::test_registered_pilot_hashes_counts' `
  'projects/simulation/tests/test_d0_waveform_channel.py::test_data_time_map_bijective' `
  'projects/simulation/tests/test_d0_waveform_channel.py::test_controlled_jump_copy_on_write' -q
```

Key raw failure excerpt (all four nodes executed):

```text
FFFF                                                                     [100%]
E   ModuleNotFoundError: No module named 'waveform'
4 failed in 0.23s
```

This is the one explicitly permitted first-module-absent bootstrap RED. It is
not a syntax, fixture, path, collection, or dependency failure. No production
file existed while this test SHA was produced and executed.

## 3. GREEN and terminal

The executor reached the bounded stop after the complete frozen-input read,
preflight census, four-node valid RED, and receipt-before-production write.
Per T071's denial condition and the 15-minute hard limit, production was not
started. This is not a scientific or implementation FAIL: the registered
assets remain unimplemented and untested GREEN.

```text
VERDICT=INCOMPLETE
WC01_WC03_WC08_RED=4/4 expected bootstrap failures
WC01_WC03_WC08_GREEN=0/4 not run
PRODUCTION=ABSENT
TERMINAL=INCOMPLETE_VALID_RED_ONLY_15_MIN_HARD_STOP
NEXT_LEGAL_ACTION=resume I03 from immutable test SHA b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d and this RED receipt; implement production without changing tests
```
