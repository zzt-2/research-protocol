# Step 113 — D0 I02 truth-alias and ndarray-container repair

> 2026-08-10 | T067 / D011 / V005 / CP012 / epoch 12 | TDD REPAIR
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Status: `PASS / I02_REPAIR_READY_FOR_FRESH_REVERIFICATION`

## 1. Finding disposition and frozen input

```text
P1-1=ACCEPT — exact literal alias membership misses owner-equivalent categories
P1-2=ACCEPT — ndarray is treated as an opaque outer container, so object references remain mutable/reachable
P1-3=REJECT AS NON-DEFECT — each false positive permission removes only its corresponding capability; the remaining set is a strict least-authority subset, not an authorization expansion
```

```text
contract.py=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
test=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
step-111=17bc5ac48d2350826ee6b40a43e291bfa54a633d3127086b956730d07ce9a2d0
step-112=9f906374838236e9d2ac95b52f23b936a9cad92e6af3c5508bb824c8dd7b6342
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
```

Protected p05 hashes matched 4/4 before RED.

## 2. Root cause and accepted RED receipt

Root cause is localized to two boundaries: `_normalized_name` feeds only exact
membership in a finite literal set, and both `_assert_receiver_truth_free` and
`_deep_freeze` treat every ndarray as an opaque numeric value even when its
dtype contains Python objects or structured fields. The action registry is not
part of either root cause.

Only the test file changed before RED. Exact nodes:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider `
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_truth_frozen_disjoint' `
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_rejects_truth_and_extra_fields' `
  'projects/simulation/tests/test_d0_contract_views.py::test_scientific_actions_disabled_cp012' -q
```

```text
test_sha256=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
production_sha256=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
exit_code=1
passed=2
failed=1
errors=0
normalized_utf8_lf_stdout_stderr_sha256=7e40c64fe7eead3ba8ed0400258c95874dd06b9dda1ceb3bc2c8eeb604f7d420
```

CV05 reported all 13 intended missing rejections in one target assertion:

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
object_array_mutable_list=accepted
structured_array_mutable_list=accepted
```

CV04 and CV09 passed during RED. CV09 now explicitly proves a positive
permission mutation yields exactly the original five-action set minus the one
corresponding capability, locking the accepted monotonic-subset semantics.

## 3. GREEN and matrix receipts

The RED test file remained byte-identical. The exact three-node command from
section 2 then passed:

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.31s
normalized_utf8_lf_stdout_stderr_sha256=d7e4ad4c69bf37e691129daa48aca98483bae4729f72c38e48a1bd111dffb734
```

The complete unchanged test file was run twice after repair. The final fresh
completion run was:

```text
exit_code=0
passed=6
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.27s
normalized_utf8_lf_stdout_stderr_sha256=ede79f995e2f310beccdc9410e7733dc39b02dbefaa16a04f56b0c5951bb8a9f
```

I01's exact three nodes were separately rerun: `3 passed in 0.24s`.

An independent inline replay of the step-112 failing subset returned:

```text
equivalent_aliases=9/9 rejected
object_or_structured_ndarray_checks=4/4 rejected
summary=13/13
exit_code=0
normalized_utf8_lf_stdout_stderr_sha256=6d9201b1bb0f7ca8c0875633c5cb23ea9244879700cb5de9def0212611b15b58
```

Positive controls in CV05 prove ordinary float and bool ndarrays remain
defensively copied and read-only. The safe names `common_cpr_phase_trace`,
`source_sha256`, `code_sha256`, and `content_sha256` remain accepted.

The repair is limited to an auditable category predicate and one shared
plain-ndarray validator. It rejects truth/payload, TX/transmitted data,
SNR/CFO/fade/slip/event/correctness, and physical channel/phase categories
while explicitly preserving the named safe receipts/trace. Any object,
structured, or non-numeric/non-bool ndarray fails with stable `ContractError`
before copy. `authorized_action_classes` was not changed.

```text
contract.py=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
test_d0_contract_views.py=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
```

## 4. Final protection receipt

```text
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
commit_created=NO
push_performed=NO
benchmark_run=NO
scientific_run=NO
CV06_CV08_count=0
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

Fresh AST audit found one unchanged action-set definition, zero production
`sys.path` references, zero main guards, and zero benchmark/scientific/
held-out runner definitions. Only contract, the existing test file, and this
step-113 log were written by T067.

Protected p05 hashes remained 4/4 exact:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 5. Terminal

```text
VERDICT=PASS
P1_1=ACCEPTED_AND_REPAIRED
P1_2=ACCEPTED_AND_REPAIRED
P1_3=REJECTED_AS_NON_DEFECT_AND_ACTION_SET_UNCHANGED
RED=1 failed CV05 with all 13 missing rows / CV04,CV09 passed
EXACT_GREEN=3/3
COMPLETE_FILE=6/6
MATRIX_REPLAY=13/13
I01_REGRESSION=3/3
TERMINAL=I02_REPAIR_READY_FOR_FRESH_REVERIFICATION
```
