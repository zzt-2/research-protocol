# Step 131 — D0 I05 P1-2 bidirectional ledger/cache repair

> 2026-08-10 | T085 / step-124 P1-2 | narrow TDD repair
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## 1. Scope and root cause

- Accepted P1-2 only: forward raw→ledger existence is insufficient.
- P1-1 required-table/group completeness remains `PENDING`.
- P1-3 overhead identity remains closed by step-129.
- No artifacts/statistics/owner/benchmark/science/web/commit/push work is authorized.

Source tracing confirms the cause: `validate_relations` checks computation existence and
ledger source/content, but does not index raw consumers, compare raw cache provenance to
its ledger, enforce phase/operation compatibility, or require decoder materializations
to have compatible consumers.

## 2. Frozen preflight

~~~text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
schemas.py=c07eb027a4a3fd8efa7d49d5885800f9cc55986b6b4e56e6feb4bde3db22e3fb
test_before=0a02fb25cfda4271293e7f964092fc8b0b85e90268e4e26f9a9b93d919592895
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-131=ABSENT
~~~

## 3. RED receipt — recorded before production modification

The new exact test establishes positive controls first: baseline relations; nine S2 off
rows sharing one B1 computation; a matching controlled cache read; standalone
`HMM_GRID_SCORE` and `OTHER_S4_CHECK`. It then applies eleven fail-closed mutations:
unconsumed S2 ledger, BPS/controlled raw-ledger cache mismatches, ghost source, content
mismatch, five wrong table↔phase/operation mappings, and one incompatible shared
computation.

~~~powershell
cd D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_schemas_statistics.py::test_ledger_bidirectional_binding_fail_closed -q
~~~

~~~text
exit_code=1
collected_and_executed=1
failed=1
passed=0
duration=0.11s
test_sha256=5a9b255654b8460009dc2e5f69a67598887d660697ec53d9dc70c0a9b97d3728
production_sha256=c07eb027a4a3fd8efa7d49d5885800f9cc55986b6b4e56e6feb4bde3db22e3fb
stdout_stderr_sha256=847c49457afdc14fdc0897f11d49cd0bf5c1382f7216b6bdfb9ddced0d3398cd
observed_failure=Failed: DID NOT RAISE SchemaError
step124_reproduction=P1-2 bidirectional ledger/cache mutation accepted
~~~

This is behavior RED, not a collection/path/dependency error. Production retained its
frozen SHA until this receipt existed.

## 4. GREEN and terminal

## 4. GREEN implementation

The repair adds a pure consumer index and exact mappings:

- S2 method → `S2/B1_DECODE`, `S2/B2_DECODE`, or `S2/O1_DECODE` by method id.
- S3 DEV/TEST → matching phase plus `CANDIDATE_DECODE`.
- BPS DEV → `BPS_DEV/B1_DECODE`.
- B2 clean/controlled tuple rows → `B2_DEV/B2_DECODE`.
- Standalone exceptions are enumerated exactly as `B2_DEV/HMM_GRID_SCORE` and
  `S4/OTHER_S4_CHECK`; every other phase/operation pair is deny-by-default.

Every raw computation first passes forward FK, then exact signature compatibility.
Rows carrying cache fields must equal the referenced ledger's cache status and source.
Every decoder-signature ledger requires at least one compatible consumer; compatible
many→one remains legal, including the nine S2 off projections. Existing ledger
source/content reverse binding is retained.

## 5. Fresh verification

All commands used the RED cwd/environment and Python invocation.

| scope | result | duration | stdout/stderr SHA256 |
|---|---:|---:|---|
| new exact ledger node | 1 passed | 0.05s | `d124f9696ed40502b4b30c0104e7d254a7e35a3d854991f72025ba67c7e5c805` |
| original SS01/SS02/SS11 | 3 passed | 0.07s | `603b1a324e6a4775c6100fc0f449b04382e3c38abd43b6e0e0619ed154b34463` |
| P1-3 overhead regression | 1 passed | 0.05s | `d124f9696ed40502b4b30c0104e7d254a7e35a3d854991f72025ba67c7e5c805` |
| full schema file | 5 passed | 0.06s | `eb1e5b6c9bca47fe92a7b691bc12b41ba7b0ab176e173c48ed06987505147c0f` |
| frozen I02 regression | 6 passed | 0.29s | `6211d5fcc13d71fe3f3db4f297d973871998383be13a643b6505ee01b736b8f7` |

~~~text
fresh_executions=16 passed
fresh_unique_tests=11/11 passed
new_positive_bundles=2
new_rejected_mutations=11
P1-3_rejected_mutations=16
original_frozen_rejected_mutations=47
total_schema_rejected_mutations=74
skip=0
xfail=0
warning=0
~~~

The test SHA is unchanged from RED; production alone changed after the receipt.

## 6. Final hashes and protection

~~~text
schemas.py=7f8ae88dfc141f5259a1b2c3753aeea4071af907a024267575a5d396f1fee60b
test_d0_schemas_statistics.py=5a9b255654b8460009dc2e5f69a67598887d660697ec53d9dc70c0a9b97d3728
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d

branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
authorized_target_changes=3
cache_census=12 -> 12
pytest_cache_count=0

p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
commit=none
push=none
~~~

P1-1 remains explicitly pending. This repair does not claim required-table/group
completeness or I05 readiness. Other shared/pre-existing worktree dirt was not modified
or cleaned.

## 7. Terminal

`I05_P1_2_P1_3_REPAIRED_P1_1_PENDING`
