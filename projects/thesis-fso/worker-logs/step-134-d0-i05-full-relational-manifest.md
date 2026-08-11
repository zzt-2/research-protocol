# Step 134 — D0 I05 FULL relational manifest

> 2026-08-10 | T088 / P1-1b | strict TDD
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## 1. Scope

Build `FULL_D0_ARTIFACT` formula expectations from the frozen owner contract, explicit
S1 extent, typed HMM preexecution plan and typed computation plan. No observed rows,
artifact paths, count-only flag, I/O, benchmark or science enter the factory.

## 2. Frozen preflight

~~~text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
schemas.py=fb90d5c36288e226142eeb9464c1109f68db20df41a51575ad985d63514fe682
test_before=03dd5dda11c79a72cc45f768c00b5969acd9834d21b6bbbd040b0409f10c36a4
step-132=40e5bbb4f967b96d75152c86f2a967ff38f5a4be60f5af47e9623be36ae8ad48
step-131=86e4b831e5195c97562d3c16dc8b8fd1c2f1d75e209a6af77274526b040abca8
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-134=ABSENT
~~~

## 3. RED receipt — before production

~~~powershell
cd D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_formula_exact_coverage projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_required_tables_fail_closed projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_rejects_bad_preexecution_plans -q
~~~

~~~text
exit_code=1
executed=3
failed=3
passed=0
duration=0.48s
test_sha256=35bc5d6682b17adeeef0a3aeb7de3bcb91946c5616d422178045f90ee3a0cd97
production_sha256=fb90d5c36288e226142eeb9464c1109f68db20df41a51575ad985d63514fe682
stdout_stderr_sha256=d77197bd0de8f3d0fd4686269883c96c675dcb0b9252f7988aecfe5a1d5cda24
observed_failure=AttributeError: module 'schemas' has no attribute 'HmmPreexecutionPlan'
~~~

All exact nodes reached the new behavior and failed because the FULL preexecution API
was absent; this is not collection/path/dependency RED.

## 4. GREEN and terminal

## 4. GREEN implementation

- Added frozen/slotted `HmmPreexecutionPlan`, `ComputationPlanEntry`, and
  `ComputationPreexecutionPlan` with exact axes, member counts, binding scheme,
  non-empty computation identities, cache-source closure, and phase/operation gates.
- `build_full_relational_manifest` accepts only a typed frozen D0 v3 owner contract,
  literal `FIRST_STAGE`/`MAXIMUM`, and the two typed preexecution plans. Its signature
  accepts no rows, mappings, artifact paths, counts, or completeness boolean.
- FULL and PARTIAL coverage hashes use distinct scope domains. FULL has exactly ten
  table expectations. Every table locks an exact identity projection; HMM additionally
  locks chunk/member/objective/computation-manifest bindings, while ledger identity is
  sourced only from the computation plan.
- `validate_relations` now requires FULL scope, exact table/projection coverage, then
  runs the existing row/PK/FK/group/ledger relations. Cross-scope calls fail closed.

## 5. Formula receipts

~~~text
FIRST_STAGE_coverage_sha256=a66aa0abd6705db2d8ac837f65c7d2d30165a01a6f006040de2c0221fe263edf
MAXIMUM_coverage_sha256=9e5ccc56215575700cdfd69a15a51572981b95d6be752c91e56baecf8de7ac21

FIRST_STAGE counts:
s1_trajectory=480
s2_method=2160
s3_candidate=10800
s3_lambda_freeze=1
s4_check=7
computation_ledger=2 (exact test preexecution plan)
bps_dev_score=7200
b2_hmm_grid_chunk=263520
b2_tuple_clean_dev=1200
b2_tuple_controlled_dev=21600

MAXIMUM delta: s1_trajectory=1200; all other formula counts unchanged
HMM role member counts: CLEAN=10, CONTROLLED_TARGET=90, CONTROLLED_SENTINEL=90
HMM objective: sentinel=false, all others=true
~~~

The computation-ledger count is plan-defined rather than owner-formula invented. The
test plan intentionally uses two legal standalone computations; real execution must
supply its full non-empty preexecution computation plan.

## 6. Fresh verification

| scope | result | duration | stdout/stderr SHA256 |
|---|---:|---:|---|
| three new exact nodes | 3 passed | 8.67s | `a4ef3c3b8cab8c39edaa4355d232a3e9d311c7995abe766f70f6db6fdc04f689` |
| full schema file | 10 passed | 8.70s | `cc0b99aedfe9281a492c4bd5d0c67f86631fd67ce7333174c758eb34fcb422c7` |
| frozen I02 regression | 6 passed | 0.38s | `aab6cf99481d64dd294c1491f37f0597bd8106003ff0ff2dbd2f057b69a770cc` |

~~~text
fresh_executions=19 passed
fresh_unique_tests=16/16 passed
new_required_table_mutations=21 (10 delete + 10 empty + 1 extra)
new_plan_and_extent_mutations=13
new_scope_cross_call=1
new_mutations=35
prior_schema_rejections=87
total_schema_rejections=122
skip=0
xfail=0
warning=0
~~~

The two S1 directions are independently formula-bound by unequal counts and unequal
coverage digests. HMM mutations cover grid, duplicate axis, role, cell, polarization,
member count, binding scheme and member namespace; computation mutations cover empty,
duplicate and orphan-source plans. Existing partial tests retain the S2/S3/controlled
count-preserving identity substitutions and HMM/ledger exact-coverage kernel.

No full scientific row bundle was constructed or executed. The test scope is the
independent formula projections, typed preexecution bindings, fail-fast ten-table/plan
gates, and the already-verified exact-coverage kernel.

## 7. Hashes and protection

~~~text
schemas.py=a72bcf273a81db5fd7feba84c72455c2b6f1754e2a57669b87a6de969c064e61
test_d0_schemas_statistics.py=35bc5d6682b17adeeef0a3aeb7de3bcb91946c5616d422178045f90ee3a0cd97
step-132=40e5bbb4f967b96d75152c86f2a967ff38f5a4be60f5af47e9623be36ae8ad48
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b

branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
authorized_target_changes=3
cache_census=12 -> 12
pytest_cache_count=0
p05_4_of_4=unchanged
commit=none
push=none
~~~

## 8. Independent preview disposition

The post-GREEN independent preview returned `PREVIEW_FAIL, P1=4`. Therefore the test
results above are regression evidence only and do **not** close P1-1b:

1. `RelationalManifest` can be directly instantiated as forged FULL; the validator does
   not possess/rebuild a canonical factory seal.
2. The HMM plan binds canonical axes and derived group projections, but the public plan
   is not a typed per-group commitment including grid float64 hex values; group swaps
   and member replacements lack an independent oracle test.
3. The computation plan binds ledger identities but not consumer-PK→computation
   bindings, so same-phase consumer/computation exchanges are not independently sealed.
4. No legal FULL row bundle reaches validator PASS. The current tests can therefore be
   satisfied by an implementation that always rejects FULL rows; formula projection
   assertions are not an independent positive acceptance oracle.

These require new failing tests before production repair: forged miniature FULL reject,
canonical positive FULL accept, per-group HMM swap/member replacement, consumer-ledger
same-phase exchange, and exact FIRST/MAX seed projections. The remaining 15-minute
boundary is insufficient to add those tests, obtain valid RED receipts, redesign the
typed plans, and rerun the 263,520-group formula verification without weakening scope.

P1-1a remains closed. P1-1b remains open. P1-2/P1-3 regressions remain GREEN, but I05 is
not ready for independent reverification. The current schemas/tests are an unaccepted
T088 draft; no benchmark or scientific execution is authorized.

## 9. Terminal

`INCOMPLETE — T088_PREVIEW_P1_4_CANONICAL_FULL_BINDING_AND_POSITIVE_ORACLE_OPEN`
