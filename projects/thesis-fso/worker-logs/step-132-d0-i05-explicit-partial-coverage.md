# Step 132 — D0 I05 P1-1a explicit partial exact coverage

> 2026-08-10 | T086 / step-124 P1-1 first slice | narrow TDD repair
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## 1. Slice boundary

- This slice owns `EXPLICIT_PARTIAL` typed expectations and exact key/multiplicity
  coverage only.
- Count-only, default boolean scope and observed-row self-manifests are not authority.
- P1-1b `FULL_D0_ARTIFACT` factory/formulas remain `PENDING`.
- P1-2 ledger binding and P1-3 overhead identities remain frozen regressions.
- No artifact filenames/I/O, statistics, benchmark, science, web, commit or push.

## 2. Frozen preflight

~~~text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
schemas.py=7f8ae88dfc141f5259a1b2c3753aeea4071af907a024267575a5d396f1fee60b
test_before=5a9b255654b8460009dc2e5f69a67598887d660697ec53d9dc70c0a9b97d3728
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
step-131=86e4b831e5195c97562d3c16dc8b8fd1c2f1d75e209a6af77274526b040abca8
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-132=ABSENT
~~~

## 3. RED receipt — recorded before production modification

The miniature manifest is now declared from test constants and owner axes: fixtures,
methods, candidate identities, exact seeds/cells and computation ids. It never scans
produced rows to infer expected coverage.

~~~powershell
cd D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_schemas_statistics.py::test_partial_manifest_exact_coverage_fail_closed projects/simulation/tests/test_d0_schemas_statistics.py::test_full_validator_rejects_partial_manifest -q
~~~

~~~text
exit_code=1
collected_and_executed=2
failed=2
passed=0
duration=0.18s
test_sha256=03dd5dda11c79a72cc45f768c00b5969acd9834d21b6bbbd040b0409f10c36a4
production_sha256=7f8ae88dfc141f5259a1b2c3753aeea4071af907a024267575a5d396f1fee60b
stdout_stderr_sha256=3be369c3d35ea0b3e5760f182ee2b2d4d9906fe0a6f3fc990cc8fce6f1e27495
observed_failure=AttributeError: module 'schemas' has no attribute 'build_identity_projection'
~~~

This is valid missing-behavior RED: both exact nodes executed and reached the new API;
production retained its frozen SHA until this receipt existed.

## 4. GREEN and terminal

## 4. GREEN implementation

The schema layer now provides frozen/slotted `CellDomain`, `SeedSet`,
`IdentityProjection`, `TableExpectation`, and `RelationalManifest`. Partial manifests
require the literal `EXPLICIT_PARTIAL` scope; booleans/default scope are invalid.

`build_identity_projection` accepts only caller-supplied non-empty tuples of exact keys.
Canonical key atoms carry explicit type tags (`str/bool/int/float/none`), so sorting and
hashing mixed types is stable and unambiguous. Projections bind unique-key count,
key-set SHA256 and key→multiplicity SHA256. `build_partial_relational_manifest` requires
non-empty typed table expectations and independently checks the coverage digest.

`validate_partial_relations` first checks exact declared table equality and every
projection Counter/hash, then runs the existing row, PK/FK, group, overhead and ledger
relations. The miniature manifest is generated only from test constants/owner axes, not
from produced rows. `validate_relations` rejects partial scope and leaves
`FULL_D0_ARTIFACT` factory/formulas unavailable for the next slice.

## 5. Fresh verification

All commands used the RED cwd/environment and Python invocation.

| scope | result | duration | stdout/stderr SHA256 |
|---|---:|---:|---|
| two new exact nodes | 2 passed | 0.08s | `7994ba6e618c029ed595e4a1809c05158405568a8878bc44db8ba7f30aebd0b5` |
| original SS01/SS02/SS11 | 3 passed | 0.09s | `03452486667ca6c9eacac7f72facde284467673b4afaafb2f393f6265758252e` |
| P1-3 overhead regression | 1 passed | 0.07s | `6cbf72c0b248046877c51c042e0185e937c237fd89f39f0fe22fc23f1d53bdfc` |
| P1-2 ledger regression | 1 passed | 0.09s | `84e0eed98ec19324a3df0de6397f3383390b1f80a178e943c0a12ab064d5d12f` |
| full schema file | 7 passed | 0.11s | `c1054d8db75938435d817dcf900383df3bd171f829a46dd388ae4a23fe2ed49f` |
| frozen I02 regression | 6 passed | 0.32s | `9ba081880e51bdfef80694dbd655cd5b4e5753da3eebefbbe9fc562ba50a56f4` |

~~~text
fresh_executions=20 passed
fresh_unique_tests=13/13 passed
new_partial_rejections=12
new_FULL_partial_rejection=1
prior_schema_rejected_mutations=74
total_schema_rejections=87
skip=0
xfail=0
warning=0
~~~

New rejection coverage includes zero table/projection, observed-row input to the
expected-key helper, count-only fake hashes, empty/delete/extra tables, three
count-preserving whole-group substitutions, one expected→undeclared identity
substitution, and PARTIAL→FULL scope misuse. The test SHA is unchanged from RED.

## 6. Final hashes and protection

~~~text
schemas.py=fb90d5c36288e226142eeb9464c1109f68db20df41a51575ad985d63514fe682
test_d0_schemas_statistics.py=03dd5dda11c79a72cc45f768c00b5969acd9834d21b6bbbd040b0409f10c36a4
step-131=86e4b831e5195c97562d3c16dc8b8fd1c2f1d75e209a6af77274526b040abca8
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

`P1-1a=closed`; `P1-1b FULL factory/formulas=PENDING`. This slice does not claim I05
readiness. Other shared/pre-existing worktree dirt was not modified or cleaned.

## 7. Terminal

`I05_PARTIAL_COVERAGE_CLOSED_FULL_FACTORY_PENDING`
