# Step 129 — D0 I05 P1-3 overhead identity repair

> 2026-08-10 | T083 / step-124 P1-3 | narrow TDD repair
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## 1. Scope and review disposition

- Accepted finding: P1-3 only. Independent enum validation does not bind tuple/N to
  pilot-count and transmitted-symbol denominators.
- P1-1 required-table/group completeness: `PENDING`.
- P1-2 bidirectional ledger/cache binding: `PENDING`.
- No completeness, ledger, benchmark, science, artifact, web, commit or push work is
  authorized here.

Root cause confirmed against source and step-124: `_local_invariants` checks
`tuple_id -> (M,N)` only; all overhead fields are separately enum-valid, so a count
belonging to another valid N passes and can corrupt goodput/NLL normalization.

## 2. Frozen preflight

~~~text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
schemas.py=c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68
test_before=ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d
step-119=4c47783657870a762d620c54e8c70fcec15d13d81490641119695788df4b3f86
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-129=ABSENT
~~~

## 3. RED receipt — recorded before production modification

Test-first change adds only
`test_tuple_overhead_identities_fail_closed`: all four owner mappings
N10→(684,6860), N20→(325,6501), N100→(64,6240), N200→(32,6208)
are valid across the four table families; each family is then mutated to a count
belonging to another valid N.

~~~powershell
cd D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_schemas_statistics.py::test_tuple_overhead_identities_fail_closed -q
~~~

~~~text
exit_code=1
collected_and_executed=1
failed=1
passed=0
duration=0.10s
test_sha256=0a02fb25cfda4271293e7f964092fc8b0b85e90268e4e26f9a9b93d919592895
production_sha256=c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68
stdout_stderr_sha256=a7fd62ad6ba53b98a988813ae5564c0f192fb93cfc26b1ec49ea6f9acfc53f48
observed_failure=Failed: DID NOT RAISE SchemaError
step124_reproduction=P1-3 wrong-but-enum-valid overhead accepted
~~~

This is a valid behavior RED: the exact test node ran and failed because old production
accepted the forbidden cross-N overhead identity. Production remained at its frozen SHA
until this receipt existed.

## 4. GREEN and terminal

## 4. GREEN implementation

One immutable owner map is the sole identity source:

~~~text
N=10  -> pilot_count=684 -> total_transmitted=6860
N=20  -> pilot_count=325 -> total_transmitted=6501
N=100 -> pilot_count=64  -> total_transmitted=6240
N=200 -> pilot_count=32  -> total_transmitted=6208
~~~

The map is a `MappingProxyType` and drives all four table families in
`_local_invariants`. `bps_dev_score` and `b2_hmm_grid_chunk` use the row N after the
existing tuple/M/N bijection; clean/controlled B2 rows derive N from their tuple id.
B, Nw and other dev-grid dimensions are unchanged. No duplicate per-table N tables
were introduced.

## 5. Fresh verification

All commands used the RED cwd/environment and Python invocation.

| scope | result | duration | stdout/stderr SHA256 |
|---|---:|---:|---|
| new exact node | 1 passed | 0.06s | `5bda4f8fc0165420e8b84a348679234f7bc8cc5532843d7e34d3e0c30ff83f12` |
| original SS01/SS02/SS11 exact nodes | 3 passed | 0.06s | `5ecba242b02ec850da76ffde88104df086be1f7ca54f1fa149c07ad3ca1373e6` |
| full schema test file | 4 passed | 0.07s | `0d36eadd058fb536148ad59358d8048d074200b4801514de0fff2a24683a4c83` |
| frozen I02 regression | 6 passed | 0.29s | `6211d5fcc13d71fe3f3db4f297d973871998383be13a643b6505ee01b736b8f7` |

~~~text
fresh_executions=14 passed
fresh_unique_tests=10/10 passed
new_valid_cases=16 (4 N identities x 4 table families)
new_rejected_mutations=16 (4 N identities x 4 table families)
frozen_rejected_mutations=47
skip=0
xfail=0
warning=0
~~~

The test SHA is unchanged from RED; production alone changed after the receipt.

## 6. Final hashes and protection

~~~text
schemas.py=c07eb027a4a3fd8efa7d49d5885800f9cc55986b6b4e56e6feb4bde3db22e3fb
test_d0_schemas_statistics.py=0a02fb25cfda4271293e7f964092fc8b0b85e90268e4e26f9a9b93d919592895
step-119=4c47783657870a762d620c54e8c70fcec15d13d81490641119695788df4b3f86
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

P1-1 and P1-2 remain explicitly pending and are not covered or claimed by this repair.
Other shared/pre-existing worktree dirt was not modified or cleaned.

## 7. Terminal

`I05_P1_3_REPAIRED_P1_1_P1_2_PENDING`
