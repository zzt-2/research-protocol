# Step 119 — D0 I05 strict schemas and relational guards

> 2026-08-10 | T073 / D011 / V005 / CP012 / epoch 12 | D0_TESTBED_IMPLEMENTATION
> evidence worktree: D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
> scope: I05 SS01/SS02/SS11 only; no statistics, artifacts, benchmark or science

## 1. Frozen inputs and preflight

~~~text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_d0_contract_views.py=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
schemas.py=ABSENT
test_d0_schemas_statistics.py=ABSENT
step-119=ABSENT
local_census_entries_named_pyc_or_pycache=12
~~~

The pre-existing cache census was recorded by path and is protected; I05 commands set PYTHONDONTWRITEBYTECODE=1 and disable pytest cache.

## 2. RED receipt — recorded before production

Test SHA256:

~~~text
test_d0_schemas_statistics.py=ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d
schemas.py=ABSENT
~~~

Exact cwd and command:

~~~powershell
cd D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_schemas_statistics.py::test_raw_tables_strict_fields projects/simulation/tests/test_d0_schemas_statistics.py::test_pk_fk_bijection_fail_closed projects/simulation/tests/test_d0_schemas_statistics.py::test_s4_schema_seven -q
~~~

~~~text
exit_code=1
collected_and_executed=3
failed=3
passed=0
duration=0.10s
stdout_stderr_sha256=a824dc9606b2ee69193bc769665e1fba2e792d8f07e6af3a47da5dad1cda32b6
expected_failure=first module-absent bootstrap RED
observed_failure=ModuleNotFoundError: No module named 'schemas'
SS01_RED=1
SS02_RED=1
SS11_RED=1
~~~

This is a valid behavior RED under T073: all three exact nodes were executed, each failed at its in-test import because the production module was absent, and there was no syntax, fixture, path, collection or third-party dependency error. Production implementation starts only after this receipt.

## 3. Owner interpretation

- The schema layer owns the ten typed owner tables (six statistical/ledger tables plus four dev-freeze evidence tables), exact field sets and local invariants.
- Relational validation owns PK uniqueness, cell/seed/computation FKs and exact S2/S3/B2-controlled reverse bindings. It does not perform statistical reduction or artifact I/O.
- S4 exactly-seven refers to the seven owner check identities in frozen order. Contract/receipt identity lives in a pure S4 artifact envelope because the row schema itself contains only check identity/count/pass/evidence SHA.
- T073's summary phrase “seven typed artifact/table contracts” does not override the owner's ten named table schemas; owner plus step-106 is authoritative.

## 4. GREEN and terminal

### 4.1 Minimal implementation

`schemas.py` contains only immutable value schemas and pure validators: ten owner-bound
table row types, strict exact-field/type/finite-value parsing and lossless mapping,
relational PK/FK/cardinality checks, and the exactly-seven S4 envelope validator. It
contains no I/O, serialization, RNG, selection, statistical reduction, runner, or
scientific computation.

The first post-production attempt executed all three nodes but exposed one runtime
compatibility defect: Python 3.11 does not accept the newer `module=` keyword on
`dataclasses.make_dataclass`. Only that production call was repaired (the test file
was unchanged), after which the same exact nodes were rerun.

### 4.2 Exact-node GREEN

Command/cwd/environment are identical to the RED receipt above.

~~~text
exit_code=0
collected_and_executed=3
failed=0
passed=3
duration=0.08s
stdout_stderr_sha256=f915832b2e56893fe398a33dda2b870de6df131f007756135b181e428cf5de34
SS01_GREEN=1
SS02_GREEN=1
SS11_GREEN=1
~~~

### 4.3 Full-file and frozen-I02 regression

~~~text
test_d0_schemas_statistics.py: exit=0, passed=3, failed=0, duration=0.07s
stdout_stderr_sha256=603b1a324e6a4775c6100fc0f449b04382e3c38abd43b6e0e0619ed154b34463

test_d0_contract_views.py: exit=0, passed=6, failed=0, duration=0.35s
stdout_stderr_sha256=eca7e3a6bc1d3b6f623fa007ed08e6df1f37574cdde3bc30f2d8277a7cc92830
skip=0
xfail=0
warning=0
~~~

Mutation inventory:

- SS01: 33 rejected mutations (10 missing-field + 10 extra-field + 13 explicit
  type/coercion/non-finite mutations).
- SS02: 7 rejected relational mutations (duplicate, orphan, cross-cell,
  cross-seed, missing S2 method, missing DEV candidate, missing B2 sentinel).
- SS11: 7 rejected S4 mutations (6/8, duplicate, unknown, wrong order,
  wrong contract, wrong receipt, missing evidence FK).
- Total: 47 rejected mutations; no test was changed after RED.

### 4.4 Hashes and protection receipt

~~~text
schemas.py=c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68
test_d0_schemas_statistics.py=ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_d0_contract_views.py=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4

p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de

branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
I05_target_changes=3 (schemas.py, test_d0_schemas_statistics.py, step-119)
local_census_entries_named_pyc_or_pycache=12 -> 12
new_local_pyc_or_pycache=0
local_pytest_cache_count=0
commit=none
push=none
~~~

Other pre-existing/shared worktree dirt was outside I05 scope and was neither modified
nor cleaned. The I05-attributable write set is exactly the three authorized targets.

## 5. Terminal

**PASS — `I05_READY_FOR_INDEPENDENT_VERIFICATION`**
