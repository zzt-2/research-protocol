# Step 146 — D0 I05 fresh authority graph repair

> 2026-08-10 | T100 / D014 | strict TDD
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## Scope

Repair only the shared object-returning canonical caches identified by step-145. Raw
FULL acceptance and HMM/member or consumer-ledger bindings remain outside this slice.

## Frozen preflight

```text
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_before=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
step-144=05446c08a37258c84de4c53028219eb34805d08f5bc53d3c62442306e8e8b0f4
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
D014=b252a47fa6a5d52b1c906c2fb8f71562c7ab9c0f95f749fac99c1517912e251e
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
```

## RED receipt — before production

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider `
  projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_cached_canonical_isolation `
  projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_recompile_uses_fresh_authority_graph -q
```

```text
exit_code=1
executed=2
failed=2
passed=0
duration=14.12s
production_sha256=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_sha256=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
stdout_stderr_sha256=3db5fdbddbe03ea87046adb56faa18d2527425f150d60afcf46a38a2ba5e98b0
failure_1=poisoned cached canonical was accepted by the authority gate
failure_2=repeated compiler calls shared object identities in the authority graph
```

Both exact nodes reached the intended shared-reference behavior; this is a valid RED.

## GREEN / protection

### Implementation

- Removed the object-returning cache from `_hmm_expectation`.
- Replaced the cached object-returning compiler with
  `_compile_full_relational_manifest_primitives`, whose memoized value is a recursively
  immutable tuple of primitive domain/seed/table/projection fields and digests only.
- `_compile_full_relational_manifest`, public factory, and validator now materialize a
  fresh `FullManifestSpec`, owner/plan copies, `FullRelationalManifest`, every
  `CellDomain`/`SeedSet`/`TableExpectation`, and every `IdentityProjection` on each call.
- No correctness path uses `cache_clear`, call ordering, a token, or a secret.

### Fresh-isolation matrix

The exact tests cover FIRST_STAGE and MAXIMUM with the original legal plan, plus a
second legal HMM/computation plan. Across those three input sets, 105 corresponding
object pairs are asserted non-identical: manifest, spec, owner, both plans, all domain
and seed objects, all ten table objects, and all eleven projection objects.

The step-145 reproduction changes one compiler result's authority SHA, table identity,
and nested projection count. That object is rejected; a later same-spec factory result
retains the original canonical authority/coverage/counts and shares no affected object.

### Fresh final-byte pytest

Fixed environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python 3.11
`-B -m pytest -p no:cacheprovider`.

| scope | result | output SHA256 |
|---|---:|---|
| two T100 exact nodes | 2 passed in 18.08s | `9ff115d82b658e42e7e0ea3524b8a6fc628426fa5c04a7e0e6777681c86df28c` |
| complete schema file | 15 passed in 18.11s | `7b5f72bb063f81736bc543d6affa1f1b83f38b7397802a69111415a807705fde` |
| explicit current `test_d0_*.py` aggregate | 48 passed in 26.33s | `c73829af82dd6cf7cff315d3992ae949d737f0b1bca85f39148b0c732e0d4ae3` |

All final-byte runs have 0 fail/error/skip/xfail/warning. T098's 34-case matrix remains
in the schema suite; no existing test was removed or weakened. Step-145's independent
88-case result remains prior evidence and requires a fresh independent verifier for
final acceptance.

### Static and protection

```text
static=PASS
lru_cached_functions=_compile_full_relational_manifest_primitives
object_returning_lru_cache=0
cache_clear_dependency=0
static_output_sha256=8ded40ab5f6a9f1de22638770f4bc6bd11facefa06496e4f674945d5c12aee29
git_diff_check_exit=0
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
test_d0_schemas_statistics.py=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
p05=4/4 frozen hashes matched
commit=none
push=none
```

The first static receipt used a faulty source-slice boundary that accidentally included
the following primitive-cache decorator and exited 1. The corrected AST-based check
above identifies decorated functions directly and is the valid static evidence; no
source or test changed between the final pytest and corrected static run.

## Open boundaries

- Raw legal FULL positive oracle: OPEN / NOT_RUN.
- Typed HMM per-group/member binding: OPEN.
- Consumer-PK to computation-ledger binding: OPEN.

## Terminal

`FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`
