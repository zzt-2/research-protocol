# Step 144 — D0 I05 FULL authority seal

> 2026-08-10 | T098 | strict TDD, authority-only slice
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## Scope

Close only the forged-FULL authority defect by separating PARTIAL and FULL types and
requiring canonical recompilation from frozen authority inputs. Raw FULL acceptance,
typed HMM per-group/member commitments, and consumer-to-ledger bindings remain outside
this slice.

## Frozen preflight

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
schemas.py=a72bcf273a81db5fd7feba84c72455c2b6f1754e2a57669b87a6de969c064e61
test_before=35bc5d6682b17adeeef0a3aeb7de3bcb91946c5616d422178045f90ee3a0cd97
step-134=81e94ed47c2ac46c7bc9d8b1056f569d8edb5ca17f9661b9e3282d8d6ca6e04c
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
step-143=1470d822ee3570fdeb85fdba58360a7635c403985f1a3ebf72748cb72c181c1e
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
p05=4/4 frozen hashes matched
```

## RED receipt — before production

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider `
  projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_factory_seal_rejects_forged_full `
  projects/simulation/tests/test_d0_schemas_statistics.py::test_full_manifest_authority_recompiles_after_tamper `
  projects/simulation/tests/test_d0_schemas_statistics.py::test_relational_manifest_is_partial_only -q
```

```text
exit_code=1
executed=3
failed=3
passed=0
duration=7.01s
production_sha256=a72bcf273a81db5fd7feba84c72455c2b6f1754e2a57669b87a6de969c064e61
test_sha256=62781c94077bd944a389858507ffc5bc5d71975ab3157dfc475c2bf3f377367e
stdout_stderr_sha256=74833247ca04127912be1f1033ea2a8f1e56724788ae387d7b37c7bb6218ce1f
failure_1=generic RelationalManifest accepted FULL_D0_ARTIFACT
failure_2=assert_full_manifest_authority API absent
failure_3=dataclasses.replace converted PARTIAL to FULL
```

All three exact nodes reached the intended new behavior and failed against frozen
production; this is a valid behavioral RED, not collection/import/path failure.

## GREEN / final protection

### Implementation

- `RelationalManifest` is now exact `EXPLICIT_PARTIAL` only. Construction,
  `dataclasses.replace`, object-field tamper, and cross-validator use cannot promote it
  to FULL.
- Added frozen/slotted `FullManifestSpec` with manifest schema identity, exact frozen
  owner contract, owner SHA, literal S1 extent, and the existing typed HMM/computation
  authority envelopes.
- Added frozen/slotted, `init=False` `FullRelationalManifest`. Its public constructor
  always fails; `build_full_relational_manifest` is the normal creation path.
- Factory and validator both reach `assert_frozen_d0_identity` through the common spec
  gate. The FULL validator first exact-type checks and recompiles the canonical FULL
  structure from stored spec, then compares every spec/domain/seed/table/projection,
  coverage digest, and authority seal before inspecting rows.
- The seal is not a capability or secret. Recomputing public coverage after table
  changes does not pass because canonical recompilation remains authoritative.

### Authority and negative receipts

```text
FIRST_STAGE_coverage_sha256=a66aa0abd6705db2d8ac837f65c7d2d30165a01a6f006040de2c0221fe263edf
FIRST_STAGE_authority_sha256=56462d6f6f80b343b909f340c20a8825c88379e4b39b4b03bfc98353126797c7
MAXIMUM_coverage_sha256=9e5ccc56215575700cdfd69a15a51572981b95d6be752c91e56baecf8de7ac21
MAXIMUM_authority_sha256=050b2832916b1988fcd50d92ff545c6909868620ce1306cb609be8bc28a736a2
authority_receipt_output_sha256=0f296f60da983e7565bd932a8c1d566a45e9ab9e4fd9c9dcc7d2deffe01a0f36
negative_matrix=34
```

The 34 explicit mutations cover generic FULL direct/replace/tamper, opaque FULL direct
construction/replace, scope, FIRST-to-MAX spec exchange, owner contract, owner SHA,
manifest schema, HMM plan field, computation plan, table drop/add/reorder/replace,
projection empty/count/key SHA/multiplicity SHA, domain/seed drop and identity changes,
coverage, authority seal, and changed-table plus publicly recomputed coverage.

### Fresh final-byte pytest

Fixed environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python 3.11
`-B -m pytest -p no:cacheprovider`.

| scope | result | output SHA256 |
|---|---:|---|
| three exact T098 nodes | 3 passed in 7.52s | `179a4c33a9505b950693380725081abb793567724b25da0f6f27716c03848382` |
| complete schema file | 13 passed in 7.54s | `bc9e5b4d31f6922f17f88929d5b5fbe6a679f1e413faa3bf055f3e9a2be998eb` |
| complete contract views regression | 9 passed in 0.35s | `02d8d165595b7db7bf407bc53b600f78f70429fab751013958d9d59475505560` |
| explicit current `test_d0_*.py` aggregate | 46 passed in 14.08s | `5a23bd47eda490b3e3d1513fed8062f6ca70a0acaa6782825c89570b5c43fa43` |

All four final-byte runs have 0 fail/error/skip/xfail/warning.

### Static and protection

```text
static_import=PASS
static_output_sha256=2809449a07feb5d5ef8a41ffb264cf210d8993a6fc6336c51a6e21b92fb855c4
git_diff_check_exit=0
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_d0_schemas_statistics.py=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
step-134=81e94ed47c2ac46c7bc9d8b1056f569d8edb5ca17f9661b9e3282d8d6ca6e04c
step-143=1470d822ee3570fdeb85fdba58360a7635c403985f1a3ebf72748cb72c181c1e
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache (unchanged)
p05=4/4 frozen hashes matched
commit=none
push=none
```

## Step-134 disposition

- P1-1 forged FULL authority: CLOSED by exact opaque type plus canonical recompilation.
- P1-4 raw legal FULL positive oracle: OPEN and explicitly not attempted here.
- Typed HMM per-group/member binding: OPEN.
- Consumer-PK to computation-ledger binding: OPEN.

## Terminal

`FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`
