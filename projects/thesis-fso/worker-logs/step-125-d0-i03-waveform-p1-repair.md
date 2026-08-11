# Step 125 — D0 I03 WaveformBuild relational-gate P1 repair

> 2026-08-10 | T079 / step-123 P1-1 / D011 / V005 / CP012
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `PASS / I03 P1 relational gate GREEN`

## 1. Review verification and root cause

The accepted review finding reproduces against the frozen source. Public
`WaveformBuild.__post_init__` only defensive-copies arrays and marks them
read-only; it does not establish registered N, shapes, maps, schedule, known
references, or finiteness. `apply_persistent_rotation` therefore treats type
identity as proof of a registered layout and consumes forged maps.

Frozen preflight matched:

```text
waveform.py=bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748
test_before=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-123=c899f896ebb7a4d59c7031688295ab26af3f99f16e9a3f72164e508f62778d72
step-123_repro=82146072a89a046d00d90e597c93c8bae850cc1076e9434643ddf811314f53a3
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

## 2. Test-first RED receipt

Only `test_waveform_build_relational_validation_fail_closed` was appended;
the original four tests remain unchanged in the same file. The regression
covers registered N, all array/map shapes, duplicate/out-of-range/inverse and
self-consistent reordered maps, known mask/reference schedule, nonfinite
waveform/reference values, and 24 legal rotated builds.

```text
phase=RED
test_after_append_sha256=f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157
source_sha256=bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
env.PYTHONDONTWRITEBYTECODE=1
env.PYTHONHASHSEED=0
exit_code=1
duration_seconds=0.706
tests_executed=1
failed=1
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=bd969595e0493aefda58c2921c7062146287f10040237b81d029f4eb89be83ff
failure=Failed: DID NOT RAISE any of (TypeError, ValueError)
```

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_waveform_channel.py::test_waveform_build_relational_validation_fail_closed' -q
```

Appending the regression changes the file SHA and supersedes the prior
file-level GREEN receipt. Production was unchanged when this RED was captured.

## 3. Minimum owning-boundary repair

`WaveformBuild.__post_init__` now derives the registered layout from `N` at
the public constructor boundary, after making defensive read-only copies. It
rejects an unregistered period, shape drift, nonfinite complex values, any
map that differs from the exact registered rank/time mapping, and any known
mask/reference that differs from the registered prefix/pilot/terminal
schedule. It does not constrain data-bearing waveform samples, so legal
persistent rotations remain constructible.

```text
source_after_sha256=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
test_after_sha256=f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157
```

## 4. GREEN receipts

Exact new regression node:

```text
phase=GREEN
exit_code=0
duration_seconds=0.735
tests_executed=1
passed=1
failed=0
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=a627885f4b9efaac136d48977c38ccc0cf413d2b07f0c2dca5d54f69518b7604
```

Original WC01/WC02/WC03/WC08 nodes, selected explicitly in one invocation:

```text
exit_code=0
duration_seconds=0.709
tests_executed=4
passed=4
failed=0
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=a63ea0fadf7272aa2b837a64326a182cd8e45fe13dc1ffa16eb297dd8d5638e9
```

Full I03 waveform file:

```text
exit_code=0
duration_seconds=0.756
tests_executed=5
passed=5
failed=0
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=59a98bac772ea432c64e42a38b68bb2d4a26595bebb177d7b28c8a8e0f1bf98a
```

I02 contract-view regression:

```text
exit_code=0
duration_seconds=0.724
tests_executed=6
passed=6
failed=0
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=9896b004c9c93385bb34a636fd47f16c90952ee08d7ebf20ed2cd9445d251baa
```

All GREEN runs used the same frozen cwd, Python, environment, `-B`, and
`-p no:cacheprovider` settings as the RED command above.

## 5. Final combined verification and protection

Fresh combined invocation of the full waveform file and I02 contract views:

```text
exit_code=0
duration_seconds=0.914
tests_executed=11
passed=11
failed=0
errors=0
skipped=0
xfail=0
warnings=0
output_sha256=bed8aa0d23496dc2354186c38f16d24e395ee8d7061b23bd3f262c73596accf8
```

Post-verification protection audit at `2026-08-10T16:30:32.764+08:00`:

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

The T079 write set is exactly the two permitted source/test targets plus this
new step-125 receipt. Ambient unrelated worktree dirt predates T079 and was
not edited. No benchmark, science run, web/search/download, install, commit,
push, or staging operation occurred.

```text
VERDICT=PASS
REGRESSION_RED=VALID 0/1
REGRESSION_GREEN=1/1
ORIGINAL_WC=4/4
WAVEFORM_FILE_GATE=5/5
I02_CONTRACT_REGRESSION=6/6
COMBINED_FINAL=11/11
TERMINAL=I03_REPAIR_READY_FOR_REVERIFICATION
```
