# Step 115 — D0 I02 owner-taxonomy final denylist repair

> 2026-08-10 | T069 / D011 / V005 / CP012 / epoch 12 | TDD REPAIR ITERATION 2
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Status: `PASS / I02_ITERATION2_READY_FOR_FRESH_REVERIFICATION`

## 1. Iteration boundary and frozen input

```text
iteration=2
route=owner-taxonomy denylist final allowed repair
mandatory_exit=any owner-equivalent alias after fresh re-verification => DENYLIST_ROUTE_REJECTED
contract.py=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
test=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
step-113=2f170dce2da26871a96033fe2ab952f5dd6a562ae665a64242dd37d361556470
step-114=505dc4bc42f37d880e954a85ddc93ef7b085b2718551893aa302c6f11b4f4324
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
```

Protected p05 hashes matched 4/4 before RED.

## 2. Accepted RED receipt

Only the test file changed. It adds the eight step-114 categories in raw,
uppercase and hyphenated forms, eight unseen same-taxonomy combinations, and
twelve explicit receiver-safe controls at nesting depth three.

```text
test_sha256=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
production_sha256=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
exit_code=1
passed=2
failed=1
errors=0
normalized_utf8_lf_stdout_stderr_sha256=15a566895ff4c3db20c58d1b9445609a1e929545dfbc86bc16c94adcc61b54a5
```

CV05's target assertion listed `30` missing rows: all 24 step-114 variants
plus six of eight unseen combinations. Existing rules already rejected
`oracle_channel_gain` and `natural_event_fixture`; this partial coverage is
consistent with the diagnosed category gap. CV04 and CV09 remained GREEN.

## 3. GREEN and taxonomy replay

The RED test file remained byte-identical after production repair. The exact
CV04/CV05/CV09 nodes passed:

```text
exit_code=0
passed=3
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.32s
normalized_utf8_lf_stdout_stderr_sha256=441fa3ff21f91fef6d50280527131685cabe73e90b727fd811df906828be0ab1
```

The unchanged complete file then passed:

```text
exit_code=0
passed=6
failed=0
errors=0
skipped=0
xfail=0
warnings=0
duration=0.31s
normalized_utf8_lf_stdout_stderr_sha256=5707b7c226afa31cdf05b00ea6ace6139bf169b53d9f8ca5d16d7cc61b909f18
```

I01's exact three nodes were separately rerun: `3 passed in 0.32s`.

An independent inline replay at nesting depth three reported:

```text
step114_raw_upper_hyphen_variants=24/24 rejected
additional_unseen_taxonomy_combinations=8/8 rejected
truth_rejected=32/32
safe_accepted=12/12
summary=44/44
exit_code=0
normalized_utf8_lf_stdout_stderr_sha256=0cead578140a0b70b4faa91907f169c296178f6b1985e16042beee1376cb24d4
```

The predicate is an auditable four-family composition, not a list of the new
test spellings: TX payload/data token combinations; physical SNR/CFO/fade and
qualified channel/phase combinations; slip/event and injected/natural event
combinations; and correctness/final-status combinations. Case and punctuation
share one normalization. The priority safe whitelist contains only the twelve
explicit receiver-visible controls required by T069, including
`channel_source_sha256`; there is no broad hash suffix exemption.

The plain ndarray gate and action-set subset implementation were unchanged.

```text
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_d0_contract_views.py=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
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

Fresh AST audit found zero production `sys.path` references, zero main guard,
and zero benchmark/scientific/held-out runner definitions. Only contract, the
existing test file, and this step-115 log were written by T069.

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
iteration=2
RED=CV05 30 missing rows / CV04 and CV09 passed
EXACT_GREEN=3/3
COMPLETE_FILE=6/6
I01_REGRESSION=3/3
TRUTH_TAXONOMY_REPLAY=32/32
SAFE_CONTROL_REPLAY=12/12
P0_P1_P2=0/0/0 (executor self-report; fresh re-verifier required)
TERMINAL=I02_ITERATION2_READY_FOR_FRESH_REVERIFICATION
```
