# Step 107 — D0 v3 implementation plan fresh independent review

> 2026-08-10 | T061 / D011 / V005 / CP012 / epoch 12 | `CONTRACT_STATIC_CHECK`  
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> boundary: full static review only; no project import, pytest, D0, benchmark, science, web/search/download, plan/owner/governance/source/test/result edit, commit or push. The only repository write is this log.

## 1. Findings first / verdict

```text
VERDICT = FAIL
P0/P1/P2 = 0/4/0
TEXTUAL_TEST_ID_ASSIGNMENT = 87/87, DUPLICATE=0, MISSING=0
EXECUTABLE_COVERAGE_CLOSURE = FAIL
TERMINAL = D0_IMPLEMENTATION_PLAN_REQUIRES_MINIMAL_REPAIR_BEFORE_TDD_EXECUTION
D0 = NOT_RUN
METHOD_SIGNAL = NONE
ENGINEERING_BENCHMARK_AUTHORIZED_BY_THIS_REVIEW = NO
SCIENTIFIC_S1_S4_AUTHORIZED = NO
```

The plan is strong on frozen physics, B2 mathematics, typed artifacts, exact
aggregation, atomic receipt-last semantics, environment discipline and the
CP012 no-science boundary.  It is not yet executable as written because three
cross-cutting tests are gated before their production subjects exist, one
future-call-graph test is gated before `benchmark.py` exists, Batch 3 has an
unstable dependency edge, the full independent review has no credible
15-minute split, and the benchmark terminal does not explicitly reconcile the
frozen 2.00-day post-D0 C1 allocation with the 7.00-day mission ceiling.

## 2. Frozen inputs and SHA verification

All required inputs were read in full, not by summary.  Start hashes exactly
match T061:

| Input | Fresh SHA256 | T061 match |
|---|---|---|
| plan | `13d0d5a8242b65f97748446e5caa8f8f7a79b169bf317bfdecc7f97eb5e1bdcd` | PASS |
| v3 owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | PASS |
| step-104 | `6db4a529fa8c9227e68375184636c3c7315a6e5005b62116760311e8d069098d` | PASS |
| step-105 | `e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d` | PASS |
| step-106 | `67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2` | PASS |
| H004 | `f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4` | PASS / current handoff |

HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`, branch=`codex/rdl-method-production-v2`, staging start=`0`.

## 3. Coverage matrix

The ranges in the plan assign every one of the 87 step-106 IDs exactly once.
There is no textual duplicate or missing ID.  “Semantic closure” below asks the
stricter T061 question: can the named owner task create the stated test first,
make it GREEN using its listed production files, and close the stated gate at
that point in the DAG?

| Family | IDs | Owner tasks | Production owner(s) | RED→GREEN / completion gate | Result |
|---|---:|---|---|---|---|
| CV | 01–09 | I01, I02 | `contract.py` | CV01–05/09 are locally closable; CV06–08 inspect downstream receiver/evaluator behavior that does not yet exist at I02 | **GAP** |
| WC | 01–08 | I03, I06 | `waveform.py`, `channel.py` | registered assets first; channel/RNG second; full WC01–08 rerun | PASS |
| RM | 01–12 | I04, I09, I12 | `codec.py`, `receiver.py`, `methods.py` | all IDs have RED→GREEN and final RM01–12 gate; I09 dependency metadata is incomplete (P1-2) | CONDITIONAL |
| B2 | 201–212 | I14, I15 | `b2.py` | core then posterior/LLR/one-way decode; full B201–212 gate | PASS |
| SS | 01–11 | I05, I07 | `schemas.py`, `statistics.py` | strict schemas first, reducers second; full SS01–11 gate | PASS |
| DF | 01–12 | I10, I13 | `freeze.py` | DF01–10/12 are locally closable; DF11 claims benchmark no-fit reachability before `benchmark.py` is created at I16 | **GAP** |
| AC | 01–12 | I08, I11 | `artifacts.py`, `verify.py` | atomic core then ledger/S4/scope guard; AC12 is rerun at I18 and review | PASS |
| EB | 01–11 | I16, I17 | `benchmark.py` | manifest/slices then watchdog/projection/no-science | CONDITIONAL: budget terminal incomplete (P1-4) |

## 4. Actionable findings

### P1-1 — Cross-cutting test gates precede the code they claim to verify

Plan I02 assigns CV06–CV08 and requires CV01–09 GREEN after modifying only
`contract.py` and `test_d0_contract_views.py`.  Step-106 defines those tests as:

- CV06: output, BPS choice, score and receipt bytes/hash must be invariant to
  Truth mutation;
- CV07: inspect deployable APIs and nested types;
- CV08: S1/S2/S3dev/S3test/S4 evaluators must require and bind one resolved
  freeze.

At I02, `receiver.py`, `methods.py`, `b2.py`, `statistics.py`, `freeze.py`,
`verify.py` and `benchmark.py` do not exist.  A dummy or empty-registry test
could turn GREEN but would not prove the frozen oracle.  The same forward
reference occurs at DF11: I13 requires evaluator/**benchmark** no-fit
reachability while `benchmark.py` is not created until I16.

**Required repair:** split the local contract tests from cross-cutting tests.
Keep CV04–05/09 in I02; place CV06–08 in a named post-component integration
slice after their real APIs exist, with explicit production scope and a valid
RED seam.  Move DF11 after I17 (or split its evaluator and benchmark halves)
so its completion gate examines the actual benchmark call graph.  Do not
satisfy these tests with placeholders, empty registries or missing-module
acceptance.

### P1-2 — Dependency metadata and Batch 3 are not stable

- I09 declares only `Depends on: I06` but its gate is RM01–RM10; RM07–RM10 are
  owned by I04.  Batch ordering happens to put I04 earlier, but the explicit
  task DAG is incomplete.
- I10 explicitly depends on I08's artifact boundary, while Batch 3 runs I10 in
  parallel with I11, which modifies `artifacts.py`.  The write sets are
  disjoint, but an I10 reader can observe I11's in-progress file, so the batch
  is not dependency-stable.

**Required repair:** add I04 to I09's explicit dependencies.  Serialize I10
against I11, or freeze the I08 artifact API and make I11 write only a disjoint
module; do not let an executor read a dependency while another executor edits
it.

### P1-3 — I19 has no bounded review split under the 15-minute hard limit

I19 requires one reviewer to read the full owner, step-105/106, all 12
production files, all eight test files, all RED/GREEN receipts and the complete
diff, then close ten review axes.  The global “split at test-ID” rule does not
apply because I19 has no test IDs or review checkpoints.  This is visibly
larger than the same fresh static-review class that already needs bounded task
briefs, so `each subagent <=15 min` is not enforceable as written.

**Required repair:** define bounded review shards with disjoint axes/files and
an independent final integrator, each with an explicit stop point and output
schema; alternatively define a verifiable staged review protocol whose final
reviewer consumes complete shard evidence and rechecks the global diff/scope
guards within 15 minutes.  The final PASS still requires P0=0/P1=0 and all P2
disposed before I20.

### P1-4 — I17/I20 do not preserve the frozen 7-day total-budget equation

The owner freezes D0=`4.50 d`, post-D0 C1=`2.00 d`, contingency=`0.50 d`, and
hard ceiling=`7.00 d`.  The plan's benchmark evidence and terminal instead say
“完整 D0 projection + recorded engineering time <=7.00d” without a receipt
field or equation for the reserved 2.00-day post-D0 C1 work and remaining
contingency.  This can falsely PASS a D0 projection that fits under seven days
alone but leaves no time for the method-bearing C1 work required by the mission.

**Required repair:** make EB08/EB10, `BenchmarkReceipt` and I20 explicitly
reconcile non-overlapping `consumed_engineering_time + projected_remaining_D0
+ 2.00d_post_D0_C1 + required_remaining_contingency` against `7.00d`, with
double-count prevention and the owner line-item identities.  If a different
interpretation of `projected_required_work` is intended, freeze that equation
in the plan before implementation; do not infer it at benchmark time.

## 5. Architecture, environment and CP012 boundary

The following required axes are present and consistent with v3/step-105/106:

- scalar per-polarization front end, prefix `RSS/31`, identity SOP and no 2x2
  LS or P08-R2 realization reuse;
- `C_post` as complex power, `N0=max(0,Cpost-2(1-mu)Ecal)`, P08/B2 per-real
  conversion by `/2`, no phase double count and exact Dirac/no-epsilon branch;
- exactly four legal symmetry states, both covariance identities, exact state
  logsumexp with inner max-log, and one-way fresh LDPC state;
- seven named dev artifacts, five/five/one freeze, all-candidate hashes,
  test-time no-refit, lossless binary64 aggregate, dual logical/materialized
  costs and receipt-last atomic writes;
- Windows Python/Sionna path, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
  `-p no:cacheprovider`, correct PowerShell `@d0Tests` expansion, no install and
  no implicit skip;
- no runtime import of old side-effect run modules, no scientific runner, no
  scientific seed/estimand in the benchmark, and I20 textually ordered after
  I18 plus fresh I19 PASS;
- `DEFECT_SMOKE`, S1–S4, adapter/C1 policy, MVE, held-out, Contract/Execute and
  thesis claims remain forbidden; a new D/V/CP is still required for science.

These PASS findings do not cure the four P1 execution defects above and do not
authorize I01, the engineering benchmark, or any science.

## 6. Protection and final receipt

- Start porcelain excluding this target: 134 entries, canonical SHA256
  `2bb4f9c6935d10fa0088d2625bef89d6593faeed8181dab42dab1ff998c8ba20`.
- Protected p05 start: `4/4 MATCH`; exact hashes are
  `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`,
  `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`,
  `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`,
  `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`.
- Final input SHA, staging, porcelain-excluding-target and p05 checks are
  recorded by the post-write verifier invocation and returned with this log's
  final SHA; no second repository path is written.

## 7. Terminal

```text
VERDICT = FAIL
P0/P1/P2 = 0/4/0
TERMINAL = D0_IMPLEMENTATION_PLAN_REQUIRES_MINIMAL_REPAIR_BEFORE_TDD_EXECUTION
NEXT_LEGAL_ACTION = REPAIR_PLAN_ONLY_AND_RUN_A_NEW_FRESH_PLAN_REVIEW
ENGINEERING_BENCHMARK_AUTHORIZED_BY_THIS_REVIEW = NO
SCIENTIFIC_S1_S4_AUTHORIZED = NO / NEW_D_V_CP_REQUIRED
```
