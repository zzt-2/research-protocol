# Step 108 — D0 v3 implementation plan minimal-repair fresh re-review

> 2026-08-10 | T062 / D011 / V005 / CP012 / epoch 12 | `CONTRACT_STATIC_CHECK`  
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> boundary: frozen-input static review only; no project import, pytest, D0, benchmark, science, web/search/download, plan/owner/governance/source/test/result edit, commit or push. The only repository write is this log.

## 1. Findings first / verdict

```text
VERDICT = PASS
P0/P1/P2 = 0/0/0
STEP107_P1_CLOSED = 4/4
TEXTUAL_TEST_ID_ASSIGNMENT = 87/87
DUPLICATE_TEST_ID_ASSIGNMENT = 0
MISSING_TEST_ID_ASSIGNMENT = 0
TERMINAL = D0_IMPLEMENTATION_PLAN_READY_FOR_TDD_EXECUTION
D0 = NOT_RUN
METHOD_SIGNAL = NONE
ENGINEERING_BENCHMARK_AUTHORIZED_BY_THIS_REVIEW = NO
SCIENTIFIC_S1_S4_AUTHORIZED = NO
```

The revised plan closes all four step-107 P1 findings without changing the
v3 physical, artifact, runtime or CP012 science boundary.  This verdict is a
static plan-entry gate: it permits dispatch of the TDD implementation slices
under CP012, but it does not satisfy I18, I19 or I20 and does not authorize an
actual engineering benchmark or any scientific seed/estimand.

## 2. Frozen inputs

All five required inputs were read in full.  The four hashes frozen by T062
match exactly.

| Input | SHA256 at review start | Frozen match |
|---|---|---|
| revised plan | `52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b` | PASS |
| step-107 | `72b561d7cd69f276113dcf9c866ff85d2fe448890a9a90a27ead5aa09439b4e1` | PASS |
| step-106 | `67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2` | PASS |
| v3 owner `d0-defect-smoke-contract.yaml` | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | PASS |
| T062 | `001376802d8058225bc1f23edcf640693f539a44225bfd0842301aaa49bf49ed` | receipt only |

HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`, branch=`codex/rdl-method-production-v2`, staging at start=`0`.

## 3. Step-107 closure table

| Finding | Revised-plan evidence | Fresh conclusion |
|---|---|---|
| P1-1 cross-cutting gates were premature | I02 owns only CV04–05/09 and explicitly leaves CV06–08 uncreated. I13 owns DF07–10/12 and leaves DF11 uncreated. I17A runs only after I06/I11/I12/I13/I15/I17, when the real receiver, B0/B1/B2, scorer, artifact, evaluator and benchmark callables exist. Missing phase/callable, empty registry and missing module all fail closed. Its RED seam is the absent real `verify.DeploymentBoundary.seal(...)` plus real benchmark-freeze binding, not a placeholder or missing-module pass. | **CLOSED** |
| P1-2 incomplete DAG / unstable Batch 3 | I09 now explicitly depends on I04 and I06. I11 completes its `artifacts.py` write before I10 is dispatched; I10 explicitly depends on I07/I08/I11 and Batch 3b reads the finalized artifact boundary. All same-file writers are serialized and every parallel batch is at most three ways. | **CLOSED** |
| P1-3 unbounded independent review | I19 is split into A/B/C file-and-axis shards followed by fresh I19D. Each shard has a finite production-file set, named evidence families and an explicit stop point; none rereads the complete implementation. Axis 7 is split at the interface: A checks front-end/legal-rotation behavior, B checks codec/B2 mapping and covariance identities. I19D consumes hashed complete shard logs, reruns only global guards, and may not blindly copy verdicts or redo the full per-file review. All four use the same explicit schema; timeout is `INCOMPLETE`; affected shards plus a new I19D are mandatory after repair. | **CLOSED** |
| P1-4 7-day mission equation omitted C1/contingency | I17 freezes consumed/remaining D0 work as an exhaustive disjoint partition, records all six D0 line items, fixes post-D0 C1 at `2.00 d`, and computes contingency consumed/remaining explicitly. EB08 covers full-work/line-item projection, EB10 covers threshold records and terminal behavior, and I20 repeats the same equation and evidence. Recorded engineering work is in the consumed partition and cannot recur in remaining work. | **CLOSED** |

No repair introduced a new P0, P1 or P2 finding.

## 4. Reconstructed 87-ID TDD closure

A deterministic expansion of every `Test IDs:` range in the revised plan gives
87 assignments and 87 unique IDs.  The family totals exactly reproduce
step-106: CV=9, WC=8, RM=12, B2=12, SS=11, DF=12, AC=12, EB=11.

| Task | Unique IDs | Test file / production seam | RED -> GREEN and gate |
|---|---|---|---|
| I01 | CV01–03 | contract views / `contract.py` | CP012 control, population and seed registry; local gate CV01–03 |
| I02 | CV04–05, CV09 | contract views / `contract.py` | real frozen views and action denial; local gate CV01–05/09; cross-cutting IDs explicitly absent |
| I03 | WC01–03, WC08 | waveform/channel / `waveform.py` | registered bytes/maps/copy-on-write; exact asset gate |
| I04 | RM07–10 | receiver/codec/methods / `codec.py` | live mapping and fresh LDPC seam; RM07–10 gate |
| I05 | SS01–02, SS11 | schemas/statistics / `schemas.py` | strict mutation failures and seven-row S4 schema |
| I06 | WC04–07 | waveform/channel / `channel.py` | named RNG and physical truth split; WC01–08 gate |
| I07 | SS03–10 | schemas/statistics / `statistics.py` | pure synthetic reducers/bootstrap; SS01–11 gate |
| I08 | AC01–06 | artifacts/cost/S4 / `artifacts.py` | canonical atomic writer and receipt-last failures |
| I09 | RM01–06 | receiver/codec/methods / `receiver.py` | scalar receiver/BPS/global state; RM01–10 gate |
| I10 | DF01–06 | dev freeze / `freeze.py` | manifest, selector and lossless aggregate after finalized artifact API |
| I11 | AC07–12 | artifacts/cost/S4 / `verify.py`, finalized `artifacts.py` | ledger/S4/scope guards; AC01–12 gate |
| I12 | RM11–12 | receiver/codec/methods / `methods.py` | B0/B1/O1 real methods; RM01–12 gate |
| I13 | DF07–10, DF12 | dev freeze / `freeze.py` | tuple/freeze/no-refit local chronology; DF11 explicitly absent |
| I14 | B201–205 | B2 math / `b2.py` | transition/variance/emission primitives |
| I15 | B206–212 | B2 math / `b2.py` | posterior/covariance/LLR/one-way decode; B201–212 gate |
| I16 | EB01–06 | engineering benchmark / `benchmark.py` | fake-worker manifest and required slices; no actual benchmark |
| I17 | EB07–11 | engineering benchmark / `benchmark.py` | fake-clock watchdog, full projection and no-science receipt |
| I17A | CV06–08, DF11 | contract views + dev freeze / real `verify.py` and benchmark binding | real cross-component seal; final CV01–09 and DF01–12 gate |

Every task states a valid target RED class and a minimal GREEN production seam.
I18 then reruns all eight files plus static call-graph/import/scope guards.  No
ID is closed by placeholder, an empty callable registry or acceptance of a
missing production module.

## 5. Dependency and parallel-read/write audit

The executable order is closed as follows:

```text
I01 -> I02
I02 -> (I03 || I04 || I05)
I03 -> I06; I05 -> I07; I02+I05 -> I08
I04+I06 -> I09
I07+I08 -> I11 -> I10
I04+I09 -> I12 and I14; I10 -> I13
I13+I14 -> I15
I11+I12+I13+I15 -> I16 -> I17
I06+I11+I12+I13+I15+I17 -> I17A -> I18
I18 -> (I19A || I19B || I19C) -> I19D -> I20
```

Batch 3a contains I09 and I11 only; their production and test writes are
disjoint.  I10 is serialized in Batch 3b after I11.  Batch 4 contains I12,
I13 and I14 with disjoint files, and I14 consumes synthetic frozen B2
parameters rather than the in-progress selector.  No batch exceeds three
agents and no reader observes a concurrently edited dependency.

## 6. Bounded-review protocol audit

| Shard | Finite input boundary | Axes / stop point | <=15-minute failure behavior |
|---|---|---|---|
| I19A | 5 production modules plus CV/WC/RM evidence | information, physical units and front-end rotation; every named file and axes 1/6/7 concluded | `INCOMPLETE`; no same-agent overrun |
| I19B | 5 production modules plus RM/B2/DF/SS evidence | decoder/freeze/statistics/exact aggregation and back-end mapping; axes 2–5/7 concluded | `INCOMPLETE`; no same-agent overrun |
| I19C | 3 production modules, focused cross-tests and complete changed-file manifest | atomic/provenance, budget and scope; axes 8–10/protection concluded | `INCOMPLETE`; no same-agent overrun |
| I19D | three hashed complete shard logs, I18 receipt, name-status diff and global guards | reconcile coverage and independently rerun global scope/hash/call-graph/import guards | does not inherit per-file full review; `INCOMPLETE` at limit |

The common output schema is `VERDICT`, `P0/P1/P2`, `AXES_CLOSED`,
`FILES_READ`, `RECEIPT_SHA256S`, `UNRESOLVED`, `STOP_REASON`.  I20 accepts only
a complete final I19D PASS.  Any implementation repair invalidates the affected
shard and requires both that shard and a new I19D review.

## 7. Owner budget recomputation

The owner line items recompute exactly:

```text
D0 = 0.25 + 0.75 + 0.50 + 2.00 + 0.50 + 0.50 = 4.50 d
post-D0 C1 = 0.75 + 0.50 + 0.75 = 2.00 d
contingency = 0.50 d
hard ceiling = 4.50 + 2.00 + 0.50 = 7.00 d
```

Let `d = consumed_engineering_days + projected_remaining_D0_days`, with the
completed and remaining D0 work-ID sets disjoint and exhaustive.  The revised
receipt freezes:

```text
contingency_consumed = max(0, d - 4.50)
required_remaining_contingency = 0.50 - contingency_consumed
projected_mission = d + 2.00 + required_remaining_contingency
```

- For `d <= 4.50`, no contingency is consumed and the full `0.50 d` is
  retained; at `d=4.50`, the mission total is exactly `7.00 d`.
- For `4.50 < d <= 5.00`, the D0 overrun consumes contingency once, the
  remaining contingency decreases by the same amount, and the mission total
  remains exactly `7.00 d`.
- For `d > 5.00`, remaining contingency is negative and the plan explicitly
  declares the hard ceiling exceeded even though algebraic cancellation alone
  would obscure the overrun.

Thus recorded benchmark time is charged once as completed D0 work; no owner
line item can appear in both consumed and remaining partitions; the fixed
`2.00 d` C1 allocation is never projected as D0; contingency is neither
silently discarded nor counted twice.  Missing slices, records or work IDs and
watchdog expiry remain `INCOMPLETE`, not PASS or a false hard blocker.

## 8. Regression and authority audit

The revised plan retains all frozen owner/test-map semantics:

- scalar per-polarization front end, `RSS/31`, identity SOP, no 2x2 LS, no
  physical truth in deployable paths;
- complex `C_post`, `N0=max(0,Cpost-2(1-mu)Ecal)`, `/2` only at the P08
  per-real interface, exact zero-variance/Dirac behavior and no linewidth or
  phase double count;
- four legal rotations, both B2 covariance identities, exact state logsumexp
  with inner max-log, and fresh one-way LDPC state;
- seven typed dev artifacts, five BPS pairs + five statistic pairs + one tuple,
  canonical binary64 lossless aggregation, sentinel score/receipt/cost without
  objective inclusion, dual logical/materialized accounting and atomic
  receipt-last writes;
- Windows Python 3.11/Sionna command discipline, `PYTHONDONTWRITEBYTECODE=1`,
  `PYTHONHASHSEED=0`, `-B`, `-p no:cacheprovider`, no dependency install and
  correct PowerShell array expansion for the aggregate tests.

I16/I17 are fake-worker/fake-clock unit slices.  The actual 720-second
`ENGINEERING_THROUGHPUT_V1` command remains behind I18 plus all four I19 gates.
`DEFECT_SMOKE`, scientific S1–S4, C1 policy/adapter, MVE and held-out remain
forbidden; a new D/V/CP is still required for scientific execution.

## 9. Protection receipt

- Target was absent at review start; the only repository write made by this
  task is this step-108 log.
- Start porcelain excluding this target: 136 entries; canonical SHA256
  `02892c7f3a3dbfc426a05877048c0ab12a4d39f38cbf5cab802f5cdc7722b031`.
- Protected p05 start: `4/4 MATCH`, with SHA256 values
  `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`,
  `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`,
  `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`,
  `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`.
- The post-write verifier must reproduce all five input hashes, p05 4/4,
  staging=0 and the same porcelain-excluding-target digest.  The final log SHA
  is intentionally reported outside this file to avoid a self-referential
  digest.

## 10. Terminal

```text
VERDICT = PASS
P0/P1/P2 = 0/0/0
TERMINAL = D0_IMPLEMENTATION_PLAN_READY_FOR_TDD_EXECUTION
NEXT_LEGAL_ACTION = DISPATCH_I01_UNDER_CP012_TDD_PROTOCOL
ENGINEERING_BENCHMARK_AUTHORIZED_BY_THIS_REVIEW = NO
SCIENTIFIC_S1_S4_AUTHORIZED = NO / NEW_D_V_CP_REQUIRED
```
