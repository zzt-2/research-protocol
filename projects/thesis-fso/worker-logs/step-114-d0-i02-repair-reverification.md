# Step 114 — D0 I02 repair fresh re-verification

> 2026-08-10 | T068 / D011 / V005 / CP012 / epoch 12 | FRESH RE-VERIFIER
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `FAIL / P0/P1/P2=0/1/0`

## 1. Scope, authority, and frozen input

This re-verification stayed inside CP012 `D0_UNIT_TEST`. It did not run a
benchmark, a scientific seed/estimand, DEFECT_SMOKE, S1–S4, a C1 adapter or
policy, web/search/download, commit, or push. No candidate or test repair was
attempted.

All T068 frozen identities matched before testing:

```text
contract.py=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
test_d0_contract_views.py=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
step-113=2f170dce2da26871a96033fe2ab952f5dd6a562ae665a64242dd37d361556470
step-112=9f906374838236e9d2ac95b52f23b936a9cad92e6af3c5508bb824c8dd7b6342
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

The owner boundary is explicit: ReceiverView may expose received/equalized
samples, common CPR trace, known prefix/pilots, receiver noise estimate,
frozen code/B2 parameters and non-truth receipts; TX information/data,
true phase/CFO/channel/SNR/fade, event labels and final correctness remain in
evaluator-only TruthView.

## 2. Fresh complete-file test run

Exact command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest `
  -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

Fresh result:

```text
......                                                                   [100%]
6 passed in 0.32s
exit_code=0
failed=0
errors=0
skipped=0
xfail=0
warnings=0
normalized_utf8_lf_stdout_stderr_sha256=4b4745ab015b850ce8a676a147e4f8195e772f647bded79bba21d982a287ba42
```

This proves the repaired candidate passes its current six tests. It does not
close the semantic category claim because the independent unseen matrix below
finds a same-class bypass.

## 3. Static audit

Accepted properties:

- `_assert_plain_ndarray` rejects object-dtype, structured-dtype and every
  non-plain numeric/bool ndarray. Both `_assert_receiver_truth_free` and
  `_deep_freeze` call this boundary; plain numeric/bool arrays are copied and
  marked read-only.
- Mapping/list/set/frozen-dataclass traversal remains recursive. A TruthView
  nested under an otherwise benign safe key is rejected.
- The repair's normalization catches case and punctuation for names whose
  category predicate already matches. Exact safe names for common CPR and
  source/code/content receipts remain explicit.
- `authorized_action_classes` first checks schema/epoch/CP/action-class/D/V
  plus execution/science false. The three positive permissions then select a
  monotonic subset; static/source audit remain independent frozen capabilities.

Open semantic gap:

- `_is_truth_alias_name` rejects literal aliases, tokens `truth`/`payload`,
  SNR/CFO/fade/slip/event/correctness, selected channel qualifiers, and
  TX/transmitted data qualifiers. It does not generalize the owner categories
  to abbreviations (`info`), unqualified owner data (`data_symbols`),
  true/physical channel names, channel realizations, injected/natural labels,
  or final codeword error truth. Normalization cannot help when the normalized
  token category itself is absent.

## 4. Independent inline category matrix

The matrix was piped directly to Windows Python `-B -`; it wrote no repository
or OS temporary file. It tested 29 original literal aliases, the nine step-112
aliases, eight unseen owner-equivalent aliases with raw/uppercase/hyphenated
forms at arbitrary nested depth, benign-key TruthView, four unsafe ndarray
cases, two plain-array controls, ten safe-name controls, and the complete
action/identity/permission matrix.

```text
total=110
passed=86
failed=24
exit_code=1
normalized_utf8_lf_stdout_stderr_sha256=72a3b6abcf9b51fb29a8aa68887c7b6dce807cab760a5834c88e7b44693ff021
```

All failures are unseen owner-category aliases accepted by ReceiverView:

```text
unseen_owner_category:info_bits:info_bits=accepted
unseen_owner_category:info_bits:INFO_BITS=accepted
unseen_owner_category:info_bits:info-bits=accepted
unseen_owner_category:data_symbols:data_symbols=accepted
unseen_owner_category:data_symbols:DATA_SYMBOLS=accepted
unseen_owner_category:data_symbols:data-symbols=accepted
unseen_owner_category:true_channel:true_channel=accepted
unseen_owner_category:true_channel:TRUE_CHANNEL=accepted
unseen_owner_category:true_channel:true-channel=accepted
unseen_owner_category:physical_channel_receipt:physical_channel_receipt=accepted
unseen_owner_category:physical_channel_receipt:PHYSICAL_CHANNEL_RECEIPT=accepted
unseen_owner_category:physical_channel_receipt:physical-channel-receipt=accepted
unseen_owner_category:channel_realization:channel_realization=accepted
unseen_owner_category:channel_realization:CHANNEL_REALIZATION=accepted
unseen_owner_category:channel_realization:channel-realization=accepted
unseen_owner_category:injected_label:injected_label=accepted
unseen_owner_category:injected_label:INJECTED_LABEL=accepted
unseen_owner_category:injected_label:injected-label=accepted
unseen_owner_category:natural_label:natural_label=accepted
unseen_owner_category:natural_label:NATURAL_LABEL=accepted
unseen_owner_category:natural_label:natural-label=accepted
unseen_owner_category:final_cw_errors:final_cw_errors=accepted
unseen_owner_category:final_cw_errors:FINAL_CW_ERRORS=accepted
unseen_owner_category:final_cw_errors:final-cw-errors=accepted
```

Owner-category judgments are not arbitrary denylist expansion:

```text
info_bits -> tx_payload_or_information_bits
data_symbols -> transmitted_coded_bits_or_data_symbols
true_channel -> true_phase_cfo_channel_snr_or_fade
physical_channel_receipt -> true_phase_cfo_channel_snr_or_fade
channel_realization -> true_phase_cfo_channel_snr_or_fade
injected_label -> injected_or_natural_event_label
natural_label -> injected_or_natural_event_label
final_cw_errors -> true_slip_boundary_rotation_or_final_correctness
```

`physical_channel_receipt` is not treated as a safe non-truth receipt: without
a field-level schema it can carry the true physical realization. The concrete
safe receipt `channel_source_sha256` was tested separately and accepted, so
the finding does not prohibit source identity metadata. Likewise
`data_symbols` is owner-forbidden transmitted data, not an explicitly named
received/equalized sample field.

The following controls all passed:

```text
original_literal_aliases=29/29 rejected
step112_equivalent_aliases=9/9 rejected
object_or_structured_ndarrays=4/4 rejected
truthview_under_benign_key=1/1 rejected
plain_numeric_bool_defensive_copy_readonly=2/2
safe_controls=10/10 accepted
safe_control_names=received_samples,equalized_samples,common_cpr_phase_trace,receiver_noise_estimate,global_rotation_state,bps_state,source_sha256,code_sha256,content_sha256,channel_source_sha256
exact_five_actions=5/5 accepted
positive_permission_false=3/3 exact five-minus-one strict subsets with no new action
identity_execution_science_mutations=8/8 empty action set
scientific_unknown_and_spelling_mutations=14/14 rejected
```

## 5. Step-112 finding disposition

### P1-1 — OPEN

The repair closes the known nine spellings but not their owner-category root.
Eight independently chosen owner-equivalent names, each with case/punctuation
variants and arbitrary-depth nesting, still cross into ReceiverView. This is
a truth-separation bypass, so I02 cannot enter Batch1.

### P1-2 — CLOSED

All four object/structured ndarray cases fail closed with `ContractError`;
ordinary numeric/bool arrays remain detached and read-only. No mutable object
reference was admitted by the tested ndarray boundary.

### P1-3 — DISPOSED_NON_DEFECT

T065 requires a permission mutation's **corresponding action** to fail closed.
For each true-to-false positive permission mutation, the returned set was
exactly the original five minus that action, a strict subset with no new
capability. CP/D/V/epoch/action-class or execution/science drift emptied the
set. This is monotonic least authority, not fail-open, and must not be coupled
into all-or-nothing invalidation.

## 6. Protection receipt and terminal

Pre-log protection state:

```text
target_preexisting=NO
status_excluding_target_line_count=150
status_excluding_target_sha256=95ac301ac5e7133fd318f71b9519c5972a60686b9ff9647e6b4315f30d62d1eb
staging_count=0
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Only this step-114 log is written by T068. Candidate, test, owner, plan,
governance, protected p05 and cache files were not modified. No benchmark or
science was run.

```text
VERDICT=FAIL
FRESH_SIX_TESTS=6/6
INDEPENDENT_MATRIX=86/110
P1_1=OPEN
P1_2=CLOSED
P1_3=DISPOSED_NON_DEFECT
P0_P1_P2=0/1/0
TERMINAL=I02_FAIL_UNSEEN_OWNER_CATEGORY_ALIAS_REPAIR_REQUIRED
I02_VERIFIED_READY_FOR_BATCH1=NO
```
