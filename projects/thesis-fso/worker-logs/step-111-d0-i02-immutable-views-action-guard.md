# Step 111 — D0 I02 immutable views and CP012 action guard

> 2026-08-10 | T065 / D011 / V005 / CP012 / epoch 12 | TDD IMPLEMENTATION
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Status: `PASS / I02_READY_FOR_INDEPENDENT_VERIFICATION`

## 1. Frozen input and protection preflight

```text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
contract_py_initial=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
test_I01_initial=3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
step_109=c85d1a2e2fd52750519a3cf8bf48c869fa4e9f5614ea53f546aa46ca0c0d430b
step_110=efbb860af0711228e9e15f5918ab16e0071d51f0e7bdb19eeb3d0ed4f91f8760
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
```

Protected p05 hashes matched T065 before RED:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 2. Accepted RED receipt — persisted before production modification

Only the test file was changed. Production remained at the frozen I01 SHA.

```text
test_sha256=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
production_sha256=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
exit_code=1
selected_nodes=3
failed=3
errors=0
collected=3
normalized_utf8_lf_stdout_stderr_sha256=c161b62e79883b49a1bf51ce0624578c83ba6a4f5ebac1d5ddde1123e85fa600
```

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_truth_frozen_disjoint' `
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_rejects_truth_and_extra_fields' `
  'projects/simulation/tests/test_d0_contract_views.py::test_scientific_actions_disabled_cp012' -q
```

Target failures, verbatim:

```text
AssertionError: immutable receiver/truth value types are not implemented
AssertionError: ReceiverView truth guard is not implemented
AssertionError: deterministic CP012 action-set API is not implemented
```

These are target assertions for CV04/CV05/CV09, not collection, path,
fixture, syntax, or missing-import failures. No production modification had
occurred when this section was written.

## 3. GREEN receipts

The test file remained byte-identical to the accepted RED test SHA. The exact
three-node command from section 2 then passed:

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.25s
normalized_utf8_lf_stdout_stderr_sha256=77d92cd56cd64a1a5b65adac4e344cc7fd9699faace17014c0a319c92f46082d
```

The complete file was then run unchanged:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest `
  -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

```text
exit_code=0
passed=6
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.25s
normalized_utf8_lf_stdout_stderr_sha256=0b0f944787b74eb2f646db3fee5e1b26b43ab1bdfd66a7442728b825a538f187
```

I01's three exact nodes were also rerun separately:

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.32s
normalized_utf8_lf_stdout_stderr_sha256=441fa3ff21f91fef6d50280527131685cabe73e90b727fd811df906828be0ab1
```

Final candidate hashes:

```text
contract.py=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
test_d0_contract_views.py=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
```

CV04 stores defensive, read-only ndarray copies and recursively freezes
mappings/sequences. Receiver and truth schemas are disjoint frozen+slots value
types. CV05 rejects exact truth aliases at arbitrary nested mapping/dataclass
keys without rejecting `common_cpr_phase_trace` or source/code/content SHA
receipt names. CV09 exposes one deterministic explicit five-action set; all
scientific/Contract/Execute/unknown classes are deny-by-default and CP/epoch/
D/V/permission mutations fail closed. CV06–CV08 were not created.

## 4. Final protection receipt

Static AST receipt:

```json
{"classes":{"CodeLayout":{"frozen":true,"slots":true},"ControlContract":{"frozen":true,"slots":true},"CostLedger":{"frozen":true,"slots":true},"D0Contract":{"frozen":true,"slots":true},"InclusiveSeedRange":{"frozen":true,"slots":true},"PhysicalCell":{"frozen":true,"slots":true},"PopulationContract":{"frozen":true,"slots":true},"ReceiverView":{"frozen":true,"slots":true},"ResolvedDevFreeze":{"frozen":true,"slots":true},"SeedRegistry":{"frozen":true,"slots":true},"TruthView":{"frozen":true,"slots":true},"WaveformLayout":{"frozen":true,"slots":true}},"main_guards":0,"module_level_calls":["add_constructor"],"path_io":[{"call":"open","line":485}],"sys_path_refs":0}
```

The sole path-I/O call remains inside explicit `load_contract`; import performs
no repository I/O. Production contains no sys.path mutation, runner/main guard,
benchmark invocation, result writer, or scientific estimand. Only the two
candidate files and this log were written under T065.

```text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
commit_created=NO
push_performed=NO
benchmark_run=NO
scientific_run=NO
CV06_CV08_created=NO
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

The cache census is identical to I01 preflight. The same ten pre-existing
tracked dirty cache files remained untouched. Protected p05 hashes remained
4/4 exact:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 5. Terminal

```text
VERDICT=PASS
I01_REGRESSION=3/3
CV04_CV05_CV09_RED=3/3 target assertion failures
CV04_CV05_CV09_GREEN=3/3
COMPLETE_FILE=6/6
P0_P1_P2=0/0/0 (executor self-report; independent verification required)
TERMINAL=I02_READY_FOR_INDEPENDENT_VERIFICATION
```
