# Step 127 — D0 I04 codec independent reverification after P1 repair

> 2026-08-10 | T081 / D011 / V005 / CP012 / epoch 12 | fresh non-author verifier
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `PASS / P0-P1-P2 = 0-0-0 / recorded process deviation retained`

## 1. Findings first

### P0

None.

### P1

None. All three step-122 findings now fail closed at the owning public codec
boundary:

1. schema/epoch/checkpoint/decision/verification and execution/science control
   mutations are rejected through the frozen CP012 contract validator;
2. backend hard outputs with value, dtype, finiteness, or shape violations are
   rejected before `D0Codec` casts them to `uint8`;
3. Python and NumPy boolean noise powers are rejected before float conversion.

### P2

None. The repeated-row NLL difference retained from step-122 is one binary64
ULP and remains within the frozen absolute tolerance `1e-15`; it is not
reopened.

## 2. Governance and frozen-input receipt

T081 is inside the active topic's CP012 `D0_UNIT_TEST` authorization. It does
not enter defect smoke/scientific execution, adapter work, MVE, or held-out
experiments. The topic has one S-file, no declared conflict, and the inherited
dependencies remain the accepted CP012 basis.

All frozen identities matched before verification:

```text
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
test=4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348
step-122=2517832d5d31a84ff251bc1520e58b21b49143b825c655c28b23986130064247
step-126=e9fcc41c2bb65a5ae904069f2a5b067734cb9adac08bdeca3a4115b41fa8f313
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
step-127=ABSENT
```

## 3. Fresh exact-node and file regression

Every process used the evidence cwd, Windows Python 3.11, environment
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`, plus `-B` and
`-p no:cacheprovider`.

| Scope | Fresh result | Process duration | Output SHA256 |
|---|---:|---:|---|
| P1 contract identity exact | 1 passed | 1.031 s | `db4ce22a81508ccb886f409bf6d5791df57d3810dd37302d8c4c62e5f45a28a3` |
| P1 backend output exact | 1 passed | 0.878 s | `c94f2add614de805d49dc30834f4f3a7b7a290a796a0367ac258887f78c1e786` |
| P1 boolean noise exact | 1 passed | 0.806 s | `88bd8dfdb7a94b6010ba5e505610de7af6f1c0243a48a0fdf1fe146c619a4fa4` |
| RM07 exact | 1 passed | 0.741 s | `d8c86ff2390d5c0b0a3bcad71d7128e77c8592a4448e5ac2e0d3986f26a080d9` |
| RM08 exact | 1 passed | 6.649 s | `40f7ffe78b6c1b30691b0a4187ec79247cbf100d29eaaa8df6a6b2a79d68c0b7` |
| RM09 exact | 1 passed | 0.878 s | `e595c9dd5a9edc1722d0f72303c939afef026f4ec243dac3267b63461a9fa194` |
| RM10 exact | 1 passed | 0.865 s | `188c7d2c78e3347bd0649f49b266c0cd289fd68f9cfe0221f5ea1989c86953ff` |
| Full I04 codec file | 7 passed | 6.403 s | `d2f26f9b378e535d039ffe0b290b90e7822cdef00f802b84817f3ac49413d956` |
| I02 contract-view regression | 6 passed | 0.693 s | `55fe2dfb2e48c49aba1a4c760a643a9b83191fccd68594aadfeb4bdf1dc51335` |

All nine commands exited 0. Exact-node observations were `7/7`, full I04 was
`7/7`, and I02 was `6/6`; no skip, xfail, warning, or hidden failure appeared.

## 4. Independent step-122 replay matrix

A separate no-file Python process exercised every requested mutation and its
legal controls rather than relying only on the repaired tests:

```text
rows=32
pass=32
fail=0
exit_code=0
duration_seconds=0.371
output_sha256=55e7aae61265663f4e866bff243b47d36c79df95e1ad4a4755603d805ed29365
```

Coverage was:

- contract: schema, epoch, CP, D, V, execution, and science mutations;
- backend: integer `2`, float `0.5`, NaN, object, structured dtype, and wrong
  shape; legal binary bool/int64/float64 outputs remained accepted and became
  exact `uint8` bits;
- noise: Python bool and NumPy bool (both values) rejected; legal finite
  `0`, `0.0`, `1`, and `0.5` conversion accepted; negative/NaN/Inf rejected;
- two calls delivered `(message_state, warm_state)=(None,None)`, exact restart,
  batch, BP-iteration, truth-free and candidate receipts, and preclip 30;
- demapper positive-for-bit-1 sign and exactly one complex-to-per-real noise
  conversion matched an independent formula; bool was also rejected through
  `demap`;
- base and repeated-row re-encode NLL matched the frozen `1e-15` oracle.

## 5. Import, live backend, and static evidence

Fresh import probe:

```text
sionna_before=False
torch_before=False
sionna_after=False
torch_after=False
legacy_new=[]
path_unchanged=True
filesystem_unchanged=True
exit_code=0
duration_seconds=0.205
output_sha256=6edd23e7b68b26a4ed246477efb80d74492f71c3af4e15c9c2239247d92c23ba
D0_manifest_before=67b04e3fdfd5232a7157ee5bab3d4f808d525ab3ef594edfc297e05bcb442e83
D0_manifest_after=67b04e3fdfd5232a7157ee5bab3d4f808d525ab3ef594edfc297e05bcb442e83
```

Fresh live Sionna probe:

```text
base_graph=bg2
lifting_size=104
interleaver_length=1536
inverse_permutation=true
metadata_matches_live_encoder=true
roundtrip_1024_1536_1024=true
receipt_restart_truthfree=true
exit_code=0
duration_seconds=5.040
output_sha256=a16f70efe80a77e6338d50b7b17798e11e2d1fcc177b5e8a87aa3a7357050fb5
```

Static inspection found only standard/numpy/contract top-level imports and
nested lazy Sionna/Torch imports. `D0Codec.__init__` reuses
`assert_action_authorized("D0_TESTBED_IMPLEMENTATION", contract)`; that owner
validator checks the v3 schema, epoch 12, CP012, action class, D011, V005, and
both execution/science false gates. No P08/legacy runtime import, test-only
branch, fallback/skip bypass, path mutation, or I/O was introduced. Metadata
is exposed only after live BG/Z/interleaver validation.

## 6. Late-receipt evidence disposition

```text
step-126_receipt_timing=late
step-126_is_receipt_before_production=false
historical_record_rewritten=false
step-122_independent_pre_repair_RED=accepted_anchor
this_step_independent_post_repair_GREEN_negative=complete
process_deviation_disposition=COMPENSATED_NOT_ERASED
```

Step-126 remains an `INCOMPLETE / PROCESS_DEVIATION` historical record. Its
late-persisted executor RED is **not** upgraded to a receipt-before-production.
The repair's technical evidence chain is instead closed by the already frozen
step-122 independent old-source reproduction plus this verifier's fresh
post-repair exact, negative, import, live, and static evidence. This compensates
the verification risk but does not retroactively make the executor process
compliant.

## 7. Protection and terminal

Protection immediately before this sole permitted write:

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

This verifier wrote only this new step-127 log. Production, tests, step-122,
step-126, contract/owner, p05 logs, caches, results, and governance remained
read-only. No benchmark, science execution, web/search/download, dependency
installation, commit, push, or staging action occurred.

```text
VERDICT=PASS
P0_P1_P2=0/0/0
REPAIR_NODES=3/3 GREEN
RM07_RM10=4/4 GREEN
FULL_I04=7/7 GREEN
I02_REGRESSION=6/6 GREEN
INDEPENDENT_MATRIX=32/32 PASS
PROCESS_DEVIATION=RECORDED_AND_COMPENSATED_NOT_ERASED
TERMINAL=I04_VERIFIED_READY_FOR_BATCH1_WITH_RECORDED_PROCESS_DEVIATION
```
