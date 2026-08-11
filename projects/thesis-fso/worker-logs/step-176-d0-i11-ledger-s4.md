# Step 176 — D0 I11 ledger / S4 engineering reducer

> 2026-08-11 | implementation author gate | GREEN

## Scope

- Implemented plan Task I11 only: `verify.py`, final I11 additions to `artifacts.py`, and AC07–AC12 in `test_d0_artifacts_cost_s4.py`.
- No scientific S1–S4 execution, BER/goodput/method-gain evaluation, benchmark, adapter, commit, push, staging, `common/`, or `p05_run*.log` write.
- This is an author-side TDD result, not the independent merged acceptance verdict.

## RED

Environment: Windows Python 3.11; `PYTHONDONTWRITEBYTECODE=1`; `PYTHONHASHSEED=0`; `-B`; `-p no:cacheprovider`.

Exact command:

```text
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_ledger_exec_cache_bp projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_ledger_frozen_totals projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_s3_cache_no_exposure_drop projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_s4_evidence_one_to_one projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_s4_reducer_fail_closed projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_no_common_p05_paths
```

Observed: `6 failed in 0.19s`; command elapsed `0.671s`. All six failures were expected missing-I11 API failures (`reduce_cost_ledger`, `assert_s3_cache_exposure`, `S4_CHECK_IDS`, `assert_i11_source_scope`) before production implementation.

## Implementation

- `artifacts.py`: added frozen `EvidenceReceipt` and `build_evidence_receipt()`. Evidence SHA-256 is derived only from non-empty exact bytes; caller-supplied evidence hashes are not accepted.
- `verify.py`: added exact execution/cache/BP ledger validation, direct executed-leaf/content-equality cache binding, frozen logical/materialized/HMM total gate, S3 ten-candidate exposure accounting, seven independent S4 evidence receipt binding, engineering-only fail-closed S4 reduction, and I11 source-scope guard.
- `test_d0_artifacts_cost_s4.py`: added AC07–AC12 with 18 explicit negative mutations. Wrong accept/reject observed by the focused suite: `0/0`.

## GREEN

AC07–AC12 exact nodes: `6 passed in 0.27s`; command elapsed `0.741s`.

AC01–AC12 whole focused file first full run: `21 passed in 0.56s`; command elapsed `1.053s`.

Fresh completion command:

```text
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_artifacts_cost_s4.py
```

Fresh result: `21 passed in 0.47s`; command elapsed `0.926s`; normalized UTF-8 stdout SHA-256 `260e0c71efc6531bc8659d27df14519a95e8df2910a137b2d5d61d2c728f40a0`.

Frozen exact assertions:

- logical decoder batches / CW decodes / BP iterations: `69,360 / 1,032,000 / 20,640,000`
- materialized decoder batches / CW decodes / BP iterations: `48,900 / 704,640 / 14,092,800`
- HMM dual-pol pair / logical primitive / materialized primitive scores: `8,344,800 / 16,689,600 / 7,027,200`

## Evidence hashes and protection

HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`

```text
verify.py                         60efe69fce37dedfeaf4762f49936d3ab6acf97e95f3a801c1fa55c5331971fb
artifacts.py                      0855f57f90fa6db431f55de4e0aa7be8edc98828a7d6004af7f9bfbbe6c68970
test_d0_artifacts_cost_s4.py      0687f3fd44580635f893c28b4836deffcd5a8dacf89dd8e5f2d9f7a75aaeb177
```

The staging area was empty. `common/` had no I11 status entry. The four protected logs remained untracked and unstaged at the final check; observed hashes:

```text
p05_run.log   7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log  735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log  c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log  95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## Result and next interface

- Status: `DONE` (author gate only).
- P0/P1/P2 found during implementation: `0/0/0`.
- Next interface: one independent merged Batch 3a acceptance covering final I09 + I11 bytes; if it has no new P0/P1, continue the next actual implementation batch. Scientific D0 remains `NOT_RUN`; method signal remains `NONE`.

## 2026-08-11 Batch 3a verifier P1 repair

### Root cause and RED

- P1-1: `assert_s3_cache_exposure()` checked only group totals and per-row conservation. Empty input therefore returned an all-zero summary, while balanced fractional or negative mutations survived the aggregate checks.
- P1-2: `EvidenceReceipt` was directly constructible and `assert_independent_s4_evidence()` trusted its public name/SHA fields. Seven forged instances carrying copied fields were accepted without any exact-byte issuance proof.

Added exactly four focused negative nodes: empty S3 rows, balanced fractional counts, balanced negative counts, and seven caller-forged receipts.

Fresh pre-fix result: `4 failed in 0.60s`; wrapper elapsed `1.503s`. All four failures were `DID NOT RAISE`, directly reproducing the reviewer findings.

### Minimal fix

- S3 now rejects empty rows and requires each changed/cache value to be an exact built-in nonnegative `int`; `bool`, float, and negative values are rejected before grouping or summation.
- `EvidenceReceipt` now has a controlled exact-bytes factory. Each issued object is registered by identity plus immutable structural fingerprint; the public constructor fails closed, and S4 validates issuance before accepting receipt fields. `object.__new__` forgeries and post-construction mutation do not acquire authority.

### GREEN and fresh evidence

- Four new negative nodes: `4 passed in 0.52s`; wrapper `1.323s`.
- AC01–AC12 whole file after repair: `25 passed in 0.71s`; wrapper `1.462s`.
- Fresh completion run: `25 passed in 0.72s`; wrapper `1.536s`; normalized UTF-8 stdout SHA-256 `2abafb29e0244d61bca8212b003812e32e9301f743dba4aeedd20a803386527c`.
- Repair P0/P1/P2: `0/0/0` at author gate; independent merged reverification remains required.

Final repair file hashes:

```text
verify.py                         36e21534a94181afa1d049db43f6a7570de5b075457510f00cc32e07967284e5
artifacts.py                      fe5e51026a319fe401bd8295dcc8238a9d3a2cc104d5ad221b51161fe53cb90f
test_d0_artifacts_cost_s4.py      f6b0d5631ac05bf9c15b2cc3c71fcadf1bcb7725ea3d518eb65edeceb5e52815
```

Staging remained empty; `common/` had no status entry; all four protected `p05_run*.log` files remained untracked and unstaged. No science, I05, benchmark, adapter, commit, push, or staging action occurred.
