# Step 184 — D0 I18 deterministic/unit integration

> 2026-08-11 | independent final-byte verifier | PASS

## Scope and handoff verification

- Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`.
- Read I18 in `d0-implementation-plan.md`, H005, topic index, master state, step-171 and step-175–183 receipts; also checked step-172–174 to verify H005 rather than trusting its summary.
- H005 claim 1 PASS: step-171 records the only I05 fresh five-file chain as `71 passed in 686.12s`, 118 negative/mutation cases, wrong accept/reject `0/0`.
- H005 claim 2 PASS: step-172/174 record I07 final focused author gate as `10/10`.
- H005 claim 3 PASS: step-173 records I08 author gate as `19/19` (`15` AC core + `4` narrow regressions).
- Topic boundary remained CP012 Groundwork D0 implementation/unit only; registry `conflicts_with=[]`. No science, real benchmark, adapter, MVE, BER/goodput/method-gain evaluation, or I05 long-chain rerun occurred.
- This verifier did not modify production, tests, owner/session/common/P05, staging, commits, or git history. Its only write is this receipt.

## Fresh focused aggregate

Environment:

```text
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
flags=-B -p no:cacheprovider
```

Exact PowerShell command shape:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
$py='C:\Users\zzt\scoop\apps\python311\current\python.exe'
$nodes=@(
  'projects/simulation/tests/test_d0_contract_views.py::test_contract_control_is_cp012_implementation_only',
  'projects/simulation/tests/test_d0_contract_views.py::test_population_manifest_has_exact_twelve_cells',
  'projects/simulation/tests/test_d0_contract_views.py::test_seed_registry_exact_and_pairwise_disjoint',
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_truth_frozen_disjoint',
  'projects/simulation/tests/test_d0_contract_views.py::test_receiver_rejects_truth_and_extra_fields',
  'projects/simulation/tests/test_d0_contract_views.py::test_cv06_real_deployable_seal_is_truth_invariant',
  'projects/simulation/tests/test_d0_contract_views.py::test_cv06_registry_evaluator_rejects_truth_before_authenticated_seal',
  'projects/simulation/tests/test_d0_contract_views.py::test_cv07_recursive_callable_truth_scan_covers_real_signatures_annotations_and_closures',
  'projects/simulation/tests/test_d0_contract_views.py::test_cv08_phase_freeze_and_registry_binding_fail_closed',
  'projects/simulation/tests/test_d0_contract_views.py::test_cv08_forged_object_new_and_tampered_seals_are_rejected',
  'projects/simulation/tests/test_d0_contract_views.py::test_scientific_actions_disabled_cp012',
  'projects/simulation/tests/test_d0_receiver_codec_methods.py',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_s1_coverage_event',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_s2_off_projection_cell_equal_macro_goldens',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_bootstrap_paired_pcg64_invalid_boundary_and_unclipped_ci',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_statistics_fresh_negatives_fail_closed',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_s3_exact_candidates_tie_rank_and_cost_vector',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_s3_lambda_dev_only_chronology_and_tie_break',
  'projects/simulation/tests/test_d0_schemas_statistics.py::test_s3_cell_macro_paired_delta_and_fresh_negatives',
  'projects/simulation/tests/test_d0_artifacts_cost_s4.py',
  'projects/simulation/tests/test_d0_dev_freeze.py',
  'projects/simulation/tests/test_d0_b2_math.py',
  'projects/simulation/tests/test_d0_engineering_benchmark.py'
)
& $py -B -m pytest -p no:cacheprovider @nodes -q
```

Coverage: affected CV04–CV09 including CV06–CV08 final integration seal, RM01–RM12, SS03–SS10, AC01–AC12, DF01–DF12, B201–B212, and EB01–EB11. The 23 node arguments expanded to `133` pytest cases. `test_d0_ordinary_identity.py` and the I05 HMM/FULL/authority nodes in `test_d0_schemas_statistics.py` were deliberately excluded; the 11-minute I05 five-file chain was not rerun.

Result:

```text
133 passed in 30.00s
process wall=31.731617s
exit=0
captured UTF-8 stdout SHA256=30fddffc78e712f00750013fd2dd459d68a4f3ca212a486dddd6d77b1eb3b474
```

## Independent static call-graph/import guards

Fresh Python 3.11 `ast` scan parsed all 13 production modules. It inspected import nodes, top-level statements excluding function/class bodies, deployable function signatures/bodies, benchmark/evaluator calls, receiver imports/calls, write-call literal targets, and the engineering diagnostic field.

```json
{"files_parsed":13,"imports_scanned":138,"legacy_import_hits":0,"import_time_io_hits":0,"protected_write_hits":0,"truth_identifier_hits":0,"fit_or_dynamic_hits":0,"receiver_o1_hits":0,"scientific_writer_verdict_hits":0,"gated_evaluator_calls":["TypeError","_authenticate_deployment_seal","contract_module.finalize_truth_view","type"]}
```

Interpretation:

- Truth leakage: no truth-bearing identifier in the seven deployable roots; evaluator path is `_gated_evaluator -> _authenticate_deployment_seal -> contract_module.finalize_truth_view`.
- Fit reachability: no call to `fit_common_bps`, `fit_b2_statistics`, or `fit_b2_tuple` from benchmark/verify; no `eval`, `exec`, `__import__`, or `importlib` bypass.
- O1 boundary: `receiver.py` neither imports `methods` nor references `evaluate_o1_inverse`.
- Legacy imports: no P05/P08/CMA/legacy/experiment-runner import; the sole shared receiver kernel remains the intended read-only `common._recovery.bps_cpr` import.
- Writes/import-time I/O: no top-level I/O call and no write call carrying a `common/` or `p05` target.
- Scientific writer/verdict: benchmark has no scientific writer/verdict/raw-S1–S4/gate token; `EngineeringDiagnostic.scientific_verdict` is statically frozen to `None`.

## Hash and protection census

Contract owner:

```text
projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml
f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
```

Production source bundle uses canonical sorted lines `relative/path<TAB>sha256<LF>` over all 13 D0 `.py` files:

```text
SOURCE_BUNDLE_SHA256=5dd1bf092ba02cfca1a070ce37c27980f1686adfcb9f67679747efa0ad956f11
artifacts.py  fe5e51026a319fe401bd8295dcc8238a9d3a2cc104d5ad221b51161fe53cb90f
b2.py         d62c87619a012e0e71843ecf5d88973ab7c77dfe2465924bab39cc6d67b0f864
benchmark.py  82b9e91c68d85a200c99a67cd15862f288dd2a514034a17c264079c71baa8a1d
channel.py    af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6
codec.py      5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331
contract.py   f6e000dcddd8661d2b52ea08de6c2a137cf7fd8f661d2ca415e9b56227ff1aaa
freeze.py     6425836a744d37963f97d3f6df2346f375bb2e78c1889264f3cffb37f882fe49
methods.py    6263cbb721043246772e294ee2aedc6d2d08fa78c5c8729706e6bea650d419a9
receiver.py   67c9d9818b7b8894d35d1a3457476f4ab9dcdb780adf9330c2b1173a13b1d545
schemas.py    d5bb1bbc8e8bfeba1f057ea87f57b2fb4713fdd1f852bbe40df0a531f6cc29db
statistics.py 21723eed90dd6edf2a972f4c785bb0f6952a5bf98eef0e7661612191304c886b
verify.py     0a174c90147266eb2994e25dcca80294427d8383181c02771add71350d717a7e
waveform.py   7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
```

Eight-test-file bundle:

```text
TEST_BUNDLE_SHA256=a82a66e7815200a6953f2554c4014a7694e47b382f29a234c3ab167ca0fa446b
test_d0_contract_views.py             3bf19c6968449cad1fbc6f135c58c4533158e088d6d6ae5ec7117bcb5583cf5d
test_d0_waveform_channel.py           f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
test_d0_receiver_codec_methods.py     efd349b874162af780d9dc5ce10d127786121c79968d86332e2f7f0bddd4b4b5
test_d0_schemas_statistics.py         60261ed4efb54577d0aefbd5468c7de9efdc1c47a969b3383e8e4f50b80f3514
test_d0_artifacts_cost_s4.py          f6b0d5631ac05bf9c15b2cc3c71fcadf1bcb7725ea3d518eb65edeceb5e52815
test_d0_dev_freeze.py                 356a4bc749756026b09bf4910b6f582edfff594aee19a8414f2ef898ed010248
test_d0_b2_math.py                    612b10d775337592388a145e947163b925360f8379f6a2a6cd643f43c3355675
test_d0_engineering_benchmark.py      cb852c61f63572e09186f9e8472ca77b76a294cd35a3cee7c82cb98c1b174815
```

- Latest final-byte author receipt comparison: `18/18` exact matches across I05/I07–I17A production/test files named by the receipts.
- Generated D0 artifact/output census: `0`; no artifact directory, receipt, result, or output was created under the D0 source directory.
- Staging before/after: `0/0`; `common/` status entries: `0`; protected P05 staged entries: `0`.
- Simulation cache census before/after: cache directories `21/21`, `.pyc` files `121/121`; no new cache appeared.
- Protected P05 logs remained the same four untracked files with exact SHA256:

```text
p05_run.log   7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log  735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log  c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log  95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## Verdict

```text
VERDICT=PASS
TESTS=133/133
WALL_SECONDS=31.731617
STATIC_GUARDS=PASS
P0=0
P1=0
FAILURE_POINTS=none
D0_SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
NEXT=I19A/I19B/I19C bounded independent code-review shards; I20 remains unauthorized until I19D PASS
```

