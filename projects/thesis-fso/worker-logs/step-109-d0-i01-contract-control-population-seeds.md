# Step 109 — D0 I01 contract control, population and seed registry

> 2026-08-10 | T063 / D011 / V005 / CP012 / epoch 12 | TDD IMPLEMENTATION
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Status: `PASS / I01_READY_FOR_INDEPENDENT_VERIFICATION`

## 1. Frozen input and protection preflight

```text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
plan_sha256=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step_108_sha256=fdca38d0f52822c10d5debcedc11880ea04e0fe5f2da1e2156de1c32f0507955
step_106_sha256=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
owner_v3_sha256=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
contract_py_initial=ABSENT
test_file_initial=ABSENT
step_109_initial=ABSENT
```

Protected p05 hashes before RED:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Cache census before RED: `202` `.pyc` files, `41` `__pycache__` directories, `4` `.pytest_cache` directories. Ten pre-existing tracked dirty `.pyc` files under `tools/litdownload` and `tools/litsearch` were observed and not touched.

Environment: Windows Python `3.11.9`; NumPy `2.4.3`; Torch `2.6.0+cu124`; Sionna `2.0.1`; PyYAML `6.0.3`; `PYTHONDONTWRITEBYTECODE=1`; `PYTHONHASHSEED=0`; interpreter invoked with `-B`; pytest cache provider disabled.

## 2. Accepted RED receipt — recorded before production creation

Only `projects/simulation/tests/test_d0_contract_views.py` existed when this receipt was written. Its SHA256 was:

```text
3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
```

Exact cwd:

```text
D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
```

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_contract_views.py::test_contract_control_is_cp012_implementation_only' `
  'projects/simulation/tests/test_d0_contract_views.py::test_population_manifest_has_exact_twelve_cells' `
  'projects/simulation/tests/test_d0_contract_views.py::test_seed_registry_exact_and_pairwise_disjoint' -q
```

Receipt:

```text
exit_code=4
selected_nodes=3
collected_tests=0
accepted_red_bootstrap_failures=3 selected nodes blocked by one shared first-import failure
production_contract_py=ABSENT
raw_output_utf8_sha256=e841203f30468244e381242cbb7d8b7c74ef34ee96136efa1a3fc61afffb70da
```

The failure is the one exception explicitly admitted by T063 for a new module bootstrap, not a syntax, fixture, path, or missing third-party dependency defect:

```text
from contract import ContractError, assert_action_authorized, load_contract
E   ModuleNotFoundError: No module named 'contract'
```

No production file was present before this RED receipt was persisted.

## 3. GREEN receipt

The first unchanged-test GREEN attempt exposed one production parsing boundary:
PyYAML `6.0.3` resolves owner spelling `2.5e9` as `str` (whereas `2.5e+9`
resolves as `float`).  Exit was `1`, all three fixtures failed at the same
positive-number check, and raw output SHA256 was
`ea87a786b5a3c2983b2529899f7de0c7af97cf43171ca1252d388c5ab0669a63`.
The owner and tests were not changed.  A single production fix made the
field-local positive-number parser accept finite numeric strings; no other
behavior was changed.

The exact three-node command from section 2 was then rerun without changing
the tests:

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.29s
raw_output_utf8_sha256=acbdd31f1b1f138621aadb92c41002375ac1369c68326336eb9a77d256b86734
```

Key output:

```text
...                                                                      [100%]
3 passed in 0.29s
```

The complete file was then run with:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_contract_views.py' -q
```

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.24s
raw_output_utf8_sha256=430ec0da199d69a9ffa473eaddf821e4bd62563da44baf9dbc613342bb7ad378
```

Final immutable-input and implementation hashes:

```text
contract_py_sha256=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
test_d0_contract_views_py_sha256=3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
owner_v3_sha256=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
```

CV01–CV03 are `GREEN 3/3`.  The accepted bootstrap RED covered the same three
selected nodes through one shared first-import failure before any production
file existed.

## 4. Final protection receipt

```text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
commit_created=NO
push_performed=NO
target_changes=exactly the three T063-listed untracked files
D0_production_tree=contract.py only
scientific_runner_created=NO
benchmark_run=NO
scientific_run=NO
scientific_estimand_computed=NO
```

Import-only diagnostic under `-B` and `PYTHONDONTWRITEBYTECODE=1` left the D0
tree byte-identical; before/after it contained only `contract.py` with SHA256
`a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775`.
The cache census remained exactly `202` `.pyc` files, `41` `__pycache__`
directories and `4` `.pytest_cache` directories.  The same ten pre-existing
tracked dirty `.pyc` files remained the only dirty cache paths.

Protected p05 hashes after GREEN:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 5. Terminal

```text
VERDICT=PASS
CV01_CV03_RED=3 selected nodes / one accepted bootstrap ModuleNotFoundError
CV01_CV03_GREEN=3/3
P0_P1_P2=0/0/0 (executor self-report; independent verification still required)
TERMINAL=I01_READY_FOR_INDEPENDENT_VERIFICATION
```
