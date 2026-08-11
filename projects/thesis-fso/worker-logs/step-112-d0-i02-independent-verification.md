# Step 112 — D0 I02 fresh independent verification

> 2026-08-10 | T066 / D011 / V005 / CP012 / epoch 12 | INDEPENDENT VERIFIER
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `FAIL / P0/P1/P2=0/3/0`

## 1. Frozen input and authority

All six T066 frozen hashes matched before verification:

```text
contract.py=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
test_d0_contract_views.py=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
step-111=17bc5ac48d2350826ee6b40a43e291bfa54a633d3127086b956730d07ce9a2d0
step-110=efbb860af0711228e9e15f5918ab16e0071d51f0e7bdb19eeb3d0ed4f91f8760
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

The task is within CP012 `D0_UNIT_TEST`. No benchmark, scientific seed, C1
adapter/policy, web/search/download, commit, or push was authorized or run.

## 2. Fresh six-test run

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest `
  -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

Fresh result:

```text
......                                                                   [100%]
6 passed in 0.25s
exit_code=0
failed=0
errors=0
skipped=0
xfail=0
warnings=0
normalized_utf8_lf_stdout_stderr_sha256=0b0f944787b74eb2f646db3fee5e1b26b43ab1bdfd66a7442728b825a538f187
```

The output hash exactly reproduces step-111's recorded complete-file GREEN
hash. This proves the frozen current candidate passes its six current tests;
it does not cover the independent alias/object-array mutation matrix below.

## 3. Static contract audit

### Accepted static properties

- `ReceiverView`, `TruthView`, `CodeLayout`, `WaveformLayout`, `CostLedger`,
  and `ResolvedDevFreeze` are frozen, slotted dataclasses. Receiver and truth
  field names are disjoint.
- Ordinary numeric ndarrays are defensively copied and marked read-only.
  Mapping/list/set/frozen-dataclass nesting is copied into
  mapping-proxy/tuple/frozenset/frozen-dataclass form for the tested ordinary
  containers.
- `_normalized_name` catches case and punctuation variants of names already in
  `_TRUTH_ALIASES`; `_assert_receiver_truth_free` uses an identity `seen` set
  for recursive mapping/sequence/dataclass traversal.
- `TruthView` under a benign mapping key is rejected by recursive dataclass
  inspection. All 29 currently registered aliases are rejected at arbitrary
  depth.
- The production module has no `sys.path` mutation, runner/main guard, writer,
  subprocess/network call, benchmark invocation, or scientific estimand. Its
  sole path I/O is `Path.open` inside explicit `load_contract`; import has no
  repository I/O.

### Non-gating robustness note

`_deep_freeze` has no cycle memo. A safe self-referential mapping is rejected
by `RecursionError` rather than a normalized `ContractError`; a cyclic mapping
that also carries `true_phase` is rejected by the truth guard first. This does
not accept mutable state, so it is not counted separately from the three gate
findings, but the error surface is not normalized.

## 4. OS-temp/inline mutation matrix

The matrix was piped directly to `python -B -`; it created no repository or OS
temporary file. It loaded the frozen candidate and owner, then exercised deep
nested aliases, `TruthView`, object/structured ndarrays, defensive copies,
safe names, action classes, and identity/permission mutations.

```text
total=81
passed=65
failed=16
exit_code=1
normalized_utf8_lf_stdout_stderr_sha256=1fb16584f91c75de02785e7d1564939fa6e804dbbc04ec18816171c8d48af0e3
```

Passed controls included: all 29 registered aliases rejected; nested
`TruthView` rejected; ordinary source array/list/dict/set/dataclass mutations
did not affect stored values; numeric arrays were non-writeable; the safe keys
`common_cpr_phase_trace`, `source_sha256`, `code_sha256`, and
`content_sha256` were accepted; the exact five CP012 engineering actions were
accepted; scientific/unknown/case/whitespace action mutations were rejected;
and schema/epoch/CP/action-class/D/V plus execution/science-positive identity
mutations returned the empty action set.

### All 16 failed matrix rows

```text
equivalent_alias:payload=accepted
equivalent_alias:payload_bits=accepted
equivalent_alias:tx_information_bits=accepted
equivalent_alias:snr_db=accepted
equivalent_alias:channel_gain=accepted
equivalent_alias:phase_truth=accepted
equivalent_alias:cfo=accepted
equivalent_alias:slip_rotation=accepted
equivalent_alias:final_cw_correctness=accepted
object_array_truth_dict=accepted
structured_array_truth_dict=accepted
object_array_mutable_list_recursive_immutable=FAIL stored_type=list stored=[1,2,3,4] detached=false mutation_rejected=false
structured_array_mutable_list_recursive_immutable=FAIL stored_type=list stored=[1,2,3,4] detached=false mutation_rejected=false
permission_mutation_reject_all:implementation_authorized=FAIL remaining=[CONTRACT_STATIC_CHECK,D0_UNIT_TEST,ENGINEERING_THROUGHPUT_BENCHMARK,SOURCE_AUDIT]
permission_mutation_reject_all:unit_test_authorized=FAIL remaining=[CONTRACT_STATIC_CHECK,D0_TESTBED_IMPLEMENTATION,ENGINEERING_THROUGHPUT_BENCHMARK,SOURCE_AUDIT]
permission_mutation_reject_all:engineering_benchmark_authorized=FAIL remaining=[CONTRACT_STATIC_CHECK,D0_TESTBED_IMPLEMENTATION,D0_UNIT_TEST,SOURCE_AUDIT]
```

Each alias in the first nine rows is owner-equivalent, not an arbitrary
expansion: payload/payload-bits/tx-information-bits map to
`tx_payload_or_information_bits`; `snr_db` maps to true SNR;
`channel_gain` to true channel/fade; `phase_truth` to true phase; `cfo` to true
CFO; `slip_rotation` to true slip rotation; and `final_cw_correctness` to final
correctness. Therefore none may be admitted merely because its spelling is
absent from the literal alias set.

## 5. Findings

### P1-1 — Recursive truth denylist is spelling-incomplete

`contract.py:121` enumerates literal aliases, and `contract.py:160` only
compares normalized keys against that finite set. All nine explicit
owner-equivalent spellings required by T066 pass at arbitrary nested depth.
This permits Receiver-side containers to carry owner-forbidden TX truth,
physical truth, slip truth, and final correctness while all six current tests
remain green. CV05 currently tests only twelve literal spellings and therefore
does not establish the semantic denylist claim.

### P1-2 — Object and structured ndarrays bypass both truth traversal and deep immutability

`contract.py:95` copies an ndarray and marks only the ndarray write flag false;
`contract.py:160` does not recurse into ndarray elements or object fields.
Consequently both an object-dtype array and a structured array containing
`{"true_phase": ...}` are accepted. For benign mutable-list payloads, the
stored array retains the same list object: source mutation changes stored
state, and the stored list itself remains appendable. Outer
`writeable=False` is not recursive immutability. This violates both CV04 and
CV05 despite the six-test GREEN.

### P1-3 — Positive permission mutations do not invalidate the frozen CP012 identity

`contract.py:399-414` treats the three positive permission fields as a dynamic
subset selector after the identity check. Flipping any one from its frozen
owner value `true` to `false` removes only its associated action while leaving
three or four other actions authorized. T066 requires CP/D/V/epoch/permission
mutation rejection, and the hypothesis requires the exact CP012 action set;
a permission-mutated contract is not the frozen CP012 identity and must fail
closed rather than authorize a subset. The current test checks only that the
single associated action disappears, so it misses this fail-open remainder.

## 6. TDD receipt reconstruction and evidence level

- step-110 final candidate/test hashes are exactly step-111 initial hashes:
  `a7822872...4775` and `3d411c35...f9e1`.
- step-111 RED test hash is exactly the frozen final test hash
  `c248cda3...437b`; its recorded RED production hash is exactly the step-110
  candidate hash.
- step-111 final candidate/test hashes are exactly the T066 frozen hashes.
- The fresh six-test output reproduces the recorded GREEN output hash exactly.
- `step-109` also hashes to its step-111 reference
  `c85d1a2e2fd52750519a3cf8bf48c869fa4e9f5614ea53f546aa46ca0c0d430b`.

The receipt is internally consistent and its current GREEN is independently
reproduced. Historical RED stdout and the pre-production tree cannot be
independently replayed because no immutable raw RED stream or old source
snapshot is retained; that part remains executor self-report, not independent
proof. Evidence level:
`DOCUMENT_INTERNAL_CONSISTENCY_PLUS_FRESH_GREEN_PLUS_FRESH_NEGATIVE_MATRIX`.

## 7. Protection receipt and terminal

Pre-log protection state:

```text
target_preexisting=NO
status_excluding_target_sha256=1bd530b363e63111bb05cfc226f411799b0e306caf570ccbe43a93f9fa9d084e
status_line_count=146
staging_count=0
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Only this step-112 log is written by T066. Candidate, test, owner, governance,
p05, and cache files were not modified; no repair was attempted.

```text
VERDICT=FAIL
FRESH_SIX_TESTS=6/6
INDEPENDENT_MATRIX=65/81
P0_P1_P2=0/3/0
TERMINAL=I02_FAIL_REPAIR_REQUIRED_BEFORE_BATCH1
I02_VERIFIED_READY_FOR_BATCH1=NO
```
