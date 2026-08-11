# D0 v3 implementation plan

> 日期：2026-08-10  
> 控制：D011 / V005 / CP012 / epoch 12  
> 当前 lane：`GROUNDWORK_STEP4A_D0_IMPLEMENTATION_PREFLIGHT`  
> 计划状态：`REVISED_AFTER_STEP107_FAIL_PENDING_FRESH_REVIEW`  
> 科学状态：`D0=NOT_RUN / METHOD_SIGNAL=NONE / SCIENTIFIC_S1_S4_AUTHORIZED=NO`

## 1. Goal and current gate

在不修改 `common/`、旧 P08/P08-R/P08-R2 资产和 scientific contract 的前提下，在
`projects/simulation/explore/coded-decoder-feedback/` 建成 v3 冻结的 truth-separated D0 工程壳、B0/B1/B2/O1、typed dev-freeze/artifact/statistics 与 S4 工程验证接口，并完成 deterministic/unit gates、独立代码审查和 12 分钟非科学吞吐门。

本计划**不运行** `DEFECT_SMOKE`、S1–S4、任何 scientific seed/estimand，不建设 adapter/C1 policy/MVE/held-out，也不产生科学 PASS/KILL。工程四门全部 PASS 后，必须另立新的 D/V/CP 才能授权 scientific D0。

进入证据：

- step-103：v3 asset contract `PASS 0/0/0`，两项 step-101 P1 CLOSED，`94/94` 静态断言 PASS。
- step-104：CP012 治理转移 `PASS 0/0/0`；authority matrix=`true/true/true/false/false`。
- step-105：`IMPLEMENTATION_ARCHITECTURE_READY / HARD_BLOCKER=NO`。
- step-106：`TDD_TEST_MAP_READY / UNAUTOMATABLE_FROZEN_INVARIANTS=0 / HARD_BLOCKER=NO`。
- step-107：计划审查 `FAIL 0/4/0`；本版只修复 cross-cutting gate 时序、显式依赖、审查分片和 7 日预算方程，尚未授权实施。
- 预算：`BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`；当前没有建立 `>7D_HARD_BLOCKER`。

## 2. Frozen implementation choices

### 2.1 Runtime and command discipline

唯一已闭合 Sionna 环境是 Windows Python：

```text
C:\Users\zzt\scoop\apps\python311\current\python.exe
Python 3.11.9 / NumPy 2.4.3 / Torch 2.6.0+cu124 / Sionna 2.0.1 / PyYAML 6.0.3
```

WSL `~/.venvs/torch` 当前缺 `sionna`，本计划不安装依赖、不在 WSL 运行 D0 tests。每条测试命令从证据 worktree 执行：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact-node-or-file>
```

每个 executor 在首尾记录解释器/依赖版本、HEAD、staging、目标 diff、pycache/pytest-cache census 和 p05 4/4；禁止自动安装、隐式 skip、pytest cache、`.pyc` 新增、commit 或 push。

### 2.2 Production tree

```text
projects/simulation/explore/coded-decoder-feedback/
  contract.py
  waveform.py
  channel.py
  receiver.py
  codec.py
  methods.py
  b2.py
  schemas.py
  freeze.py
  statistics.py
  artifacts.py
  benchmark.py
  verify.py
```

当前控制下不创建 scientific runner。`benchmark.py` 只能暴露 `ENGINEERING_THROUGHPUT_V1`。

测试文件固定为：

```text
projects/simulation/tests/test_d0_contract_views.py
projects/simulation/tests/test_d0_waveform_channel.py
projects/simulation/tests/test_d0_receiver_codec_methods.py
projects/simulation/tests/test_d0_b2_math.py
projects/simulation/tests/test_d0_schemas_statistics.py
projects/simulation/tests/test_d0_dev_freeze.py
projects/simulation/tests/test_d0_artifacts_cost_s4.py
projects/simulation/tests/test_d0_engineering_benchmark.py
```

测试通过统一 helper 把 D0 root 加入 `sys.path`；production module 不改全局路径、不在 import 时 mkdir、构造 decoder、写文件或运行任务。

### 2.3 Dependency and information-flow DAG

```text
contract
├── waveform ── channel ── receiver ── methods ──┐
├── codec ───────────────────────────── methods ──┤
├── schemas ── statistics ── freeze ──────────────┤── verify ── benchmark
├── artifacts ────────────────────────────────────┤
└── waveform + receiver + codec ── b2 ────────────┘
```

- `channel.build_views(...)` 是唯一同时见到 physical truth 和 receiver values 的 factory；返回 disjoint immutable `ReceiverView/TruthView`。
- `receiver`、`codec`、`methods`、`b2`、`freeze`、`statistics`、`verify`、`benchmark` 的 deployable path 不得接受/闭包捕获 `TruthView`。
- O1 只在 deployable outputs freeze 后由 evaluator 调用；不进入 registry、candidate score 或 receiver caller graph。
- evaluators/benchmark 只接收 `ResolvedDevFreeze`；不得 import 或调用任何 `fit_*`。
- `benchmark` 不生成 `raw_s1..s4`、CI、gate conjunction 或 C1 terminal。

### 2.4 Reuse boundary

- 只读复用 common 数值 kernel：`qam16_mod`、square-16QAM `hard_decision`、`amp_limit`、`mmse_equalize`、`bps_cpr(..., mod='qam16')`。
- `codec.py` 直接构造 Sionna encoder/decoder，并把 P08 的 Gray table、positive-for-bit-1 max-log、BG/interleaver/fresh-decode 语义作为 source-bound adapter 实现；**不在 runtime import** `p08r_chain.py`、`p08r2_chain.py` 或旧 run scripts，避免其 default-device/sys.path/import-I/O 副作用。
- 禁止复用 `CodedRealizationR/R2`、P08-R2 2×2 LS、oracle sigma helpers、`resolve_qam16`、旧 `save_results` 与旧 run/metamorphic modules。
- 无 SOP、identity polarization、逐偏振 scalar complex gain；32-symbol prefix 的每偏振独立 `RSS/(32-1)`。P08 demapper 的参数是 per-real variance，因此 `sigma2=C_post_complex/2`；B2 inner P08 metric 使用 `N0_complex/2`。

## 3. TDD evidence protocol

每个实现任务严格执行：

1. 先只增加当前 test IDs，运行 exact node/file；有效 RED 必须是目标 assertion、`NotImplementedError`，或新模块首个 `ModuleNotFoundError`。Syntax/fixture/path/dependency/collection error 不算 RED。
2. 在对应 worker log 立即记录：test/source/owner SHA、exact command/cwd、环境、exit code、expected/observed failure、原始输出 SHA 与关键原文。测试变更会使旧 RED 失效。
3. 只实现使当前 tests 通过的最小行为；禁止顺手实现后续 slice。
4. 不改 tests，用同命令取得 GREEN；记录 source bundle SHA 与输出 SHA。
5. 完成一个 test file 后跑整文件；一批完成后跑已存在的全部 `test_d0_*.py`。

每个子 agent 单次≤15分钟。预计接近上限时，实现任务在下列 test-ID 分点停下并落盘 RED/GREEN receipt；无 test-ID 的审查任务必须使用 I19A–I19D 的显式文件/轴分片和 stop point，不得把全量审查塞给一个 agent。后续由新任务续接。实现与审查使用不同 agent。当前对话不作中间 commit。

## 4. Execution plan

### Task I01 — Contract control, population and seed registry

**Files**

- Create: `projects/simulation/explore/coded-decoder-feedback/contract.py`
- Create: `projects/simulation/tests/test_d0_contract_views.py`
- Test IDs: CV01–CV03

**RED → GREEN**

1. 写 CP012 control parse、12-cell population 和八个 disjoint seed ranges tests。
2. RED 后实现 strict duplicate-key YAML loader、frozen contract dataclasses、cell/seed manifest 与 `assert_action_authorized` 基础。
3. CP012 必须允许 implementation/unit/benchmark/source/static，拒绝 execution/science。

**Gate**：CV01–03 GREEN；import 无 I/O；不创建 science runner。

### Task I02 — Immutable ReceiverView/TruthView and chronology guard

**Files**

- Modify: `contract.py`
- Modify: `test_d0_contract_views.py`
- Test IDs: CV04–CV05、CV09
- Depends on: I01

**RED → GREEN**

1. 测 frozen/disjoint fields、extra/truth rejection 和 science action rejection；CV06–08 留到真实 receiver/evaluator/benchmark 全部存在后的 I17A，禁止 placeholder、空 registry 或 missing-module acceptance。
2. 实现 `ReceiverView`、`TruthView`、`CodeLayout`、`WaveformLayout`、`CostLedger`、`ResolvedDevFreeze` 与 recursive truth denylist。

**Gate**：CV01–05/09 GREEN；view/control 本地契约闭合。CV06–08 此时必须仍为未创建，不得用虚假对象提前闭门。

### Task I03 — Registered waveform assets and data/time maps

**Files**

- Create: `waveform.py`
- Create: `test_d0_waveform_channel.py`
- Test IDs: WC01–WC03、WC08
- Depends on: I02

**RED → GREEN**

1. 测 prefix 五个固定 SHA、pilot cycle/四个 N 展开 SHA、pilot counts/total lengths、6144-rank bijection、terminal pilot 与 persistent suffix copy-on-write。
2. 实现 Gray-16QAM registered assets、`build_waveform`、`data_to_time/time_to_data` 和 integer-only four-state rotation。

**Gate**：全部 registered bytes/hash exact；known positions=`-1`；sentinel byte-identical；suffix含 later pilots。

### Task I04 — Codec adapter, mapping and fresh LDPC

**Files**

- Create: `codec.py`
- Create: `test_d0_receiver_codec_methods.py`
- Test IDs: RM07–RM10
- Depends on: I02

**RED → GREEN**

1. 测 16 labels roundtrip/four rotations、one-CW noiseless 1024→1536→1024、每 decode fresh state、B1 exact re-encode NLL。
2. 实现 source-bound Sionna 2.0.1 adapter：lazy construction、live BG/Z/interleaver receipt、positive-for-bit-1 LLR、clip30→decoder clamp20、fixed20 iterations、`complex_noise_power/2` 单一转换。
3. Decoder object 可缓存；message/warm state 永不缓存。每次记录 batch CW、restart 和 `20*CW` BP iterations。

**Gate**：RM07–10 GREEN；候选正反序 bit-identical；环境/私有 metadata 不符即显式 FAIL，不 skip。

### Task I05 — Strict schemas and relational guards

**Files**

- Create: `schemas.py`
- Create: `test_d0_schemas_statistics.py`
- Test IDs: SS01–SS02、SS11
- Depends on: I02

**RED → GREEN**

1. 测 strict fields、extra/NaN rejection、PK/FK/bijection 和 S4 exactly-seven schema。
2. 实现 typed table/manifests 与纯 validation；不得在 schema layer 做 I/O、selection 或 scientific reduction。

**Gate**：SS01/02/11 GREEN；所有 mutation fail closed。

### Task I06 — Named RNG, physical channel and truth split

**Files**

- Create: `channel.py`
- Modify: `test_d0_waveform_channel.py`
- Test IDs: WC04–WC07
- Depends on: I03

**RED → GREEN**

1. 测 SeedSequence 六个 named spawn、stream isolation、shared GG/Wiener、independent AWGN、tau/rho/linewidth equations 和 theta0 rule。
2. 实现 supplied-waveform identity-SOP dual-pol channel；`build_views` 是唯一 truth/receiver split factory。

**Gate**：WC01–08 GREEN；P08-R2 2×2 LS/import 不可达；无 linewidth double-count。

### Task I07 — Pure statistics and uncertainty kernels

**Files**

- Create: `statistics.py`
- Modify: `test_d0_schemas_statistics.py`
- Test IDs: SS03–SS10
- Depends on: I05

**RED → GREEN**

1. 测 S1 cardinality/event、S2 off projection/cost separation/cell-equal macro/zero-denominator terminals、PCG64 bootstrap、S3 ten-candidate cost/lambda chronology/case→cell reduction。
2. 实现纯 reducers/bootstrap；unit fixtures 使用 synthetic rows，不读取 scientific artifacts/seed。

**Gate**：SS01–11 GREEN；同 rows 复算唯一；不同 strata 不池化。

### Task I08 — Canonical JSONL and atomic artifact core

**Files**

- Create: `artifacts.py`
- Create: `test_d0_artifacts_cost_s4.py`
- Test IDs: AC01–AC06
- Depends on: I02、I05

**RED → GREEN**

1. 测七个 dev artifacts、UTF-8 canonical bytes、validate-before-write、same-dir temp/flush/fsync/replace/dir-fsync、failure preservation、receipt-last torn bundle。
2. 实现 generic strict atomic writer；import 不 mkdir，receipt hash exact bytes。

**Gate**：AC01–06 GREEN；old complete target survives injected failure；no partial PASS receipt。

### Task I09 — Scalar receiver, common BPS and global state

**Files**

- Create: `receiver.py`
- Modify: `test_d0_receiver_codec_methods.py`
- Test IDs: RM01–RM06
- Depends on: I04、I06

**RED → GREEN**

1. 测 one-complex-gain `RSS/31` negative control、scalar equalizer/noiseless branch、六格 BPS/edge rule、legal four-state/even subset、odd-only Cpost/no feedback。
2. 实现 common `bps_cpr(...,mod='qam16')` validating wrapper与 receipt；禁止 2×2 LS、eight-state/TX resolver、physical SNR。

**Gate**：RM01–RM10 GREEN；六格 exact；Cpost只到 demapper/B2，永不回 equalizer。

### Task I10 — Dev manifest, BPS selector and exact HMM aggregates

**Files**

- Create: `freeze.py`
- Create: `test_d0_dev_freeze.py`
- Test IDs: DF01–DF06
- Depends on: I07、I08、I11（读取 I11 完成后的最终 artifacts boundary；不得与 I11 并发）

**RED → GREEN**

1. 测 manifest float.hex/grid/membership、7200 BPS keys/duplicate N100、CW-goodput/CWER/B/Nw tie、binary64 lossless aggregate、HMM member completeness、0.5 clean+0.5 target/sentinel exclusion+receipt+cost。
2. 实现 exact integer/power-of-two aggregate；ordinary float summation作为 negative control并拒绝。

**Gate**：DF01–06 GREEN；row/chunk order不改变 objective/winner。

### Task I11 — Ledger, S4 engineering reducer and scope guard

**Files**

- Create: `verify.py`
- Modify: `artifacts.py`
- Modify: `test_d0_artifacts_cost_s4.py`
- Test IDs: AC07–AC12
- Depends on: I07、I08

**RED → GREEN**

1. 测 execution/cache/BP ledger、冻结 logical/materialized/HMM totals、S3 cache no exposure drop、seven independent evidence、S4 fail-closed 与 no-common/p05/source path。
2. 实现 cost ledger与工程 S4 reducer；禁止输出 scientific gate PASS/KILL。

**Gate**：AC01–12 GREEN；logical=`69,360/1,032,000/20,640,000`、materialized=`48,900/704,640/14,092,800`、HMM=`8,344,800/16,689,600/7,027,200` exact。

### Task I12 — B0/B1/O1 semantics

**Files**

- Create: `methods.py`
- Modify: `test_d0_receiver_codec_methods.py`
- Test IDs: RM11–RM12
- Depends on: I04、I09

**RED → GREEN**

1. 测 B1 four-candidate NLL/tie/fresh-decode、O1 nine controlled fixtures/evaluator-only。
2. 实现 B0 one decode、B1 whole-frame four rotations、controlled copy-on-write fixture、outputs-freeze 后的 O1 inverse。

**Gate**：RM01–12 GREEN；O1 无 receiver caller；no trigger/accept/fallback/applied C1 action。

### Task I13 — Tuple selection, freeze cardinality and no-refit chronology

**Files**

- Modify: `freeze.py`
- Modify: `test_d0_dev_freeze.py`
- Test IDs: DF07–DF10、DF12
- Depends on: I10

**RED → GREEN**

1. 测 clean1200/control21600 target+sentinel roles、tuple lexicographic chain、五+五+一、dev-only seed guard、single freeze hash across phases。DF11 延后到真实 benchmark 存在后的 I17A。
2. 实现三个 fit API、`resolve_dev_freeze`、immutable load/write boundary；所有 candidates 的 exact key/raw hash都持久化。

**Gate**：DF01–10/12 GREEN；fit只接受8000–8009；DF11 尚未创建，不以缺失 benchmark 冒充 no-fit 证明。

### Task I14 — B2 transition, variance and emission core

**Files**

- Create: `b2.py`
- Create: `test_d0_b2_math.py`
- Test IDs: B201–B205
- Depends on: I04、I09（使用 synthetic frozen B2 params；不依赖尚未完成的 selector implementation）

**RED → GREEN**

1. 测 transition distance、p_s=0 no-epsilon、`N0=max(0,Cpost-2(1-mu)Ecal)`、`Vx=N0+|x|²(1-mu²)`、P08 `N0/2` factor-2 control 与 exact Dirac。
2. 实现最小 transition/emission primitives；V=0 match 0/nonmatch -inf。

**Gate**：B201–205 GREEN；无 NaN/epsilon/double-count。

### Task I15 — B2 posterior, covariance identities, LLR and one-way decode

**Files**

- Modify: `b2.py`
- Modify: `test_d0_b2_math.py`
- Test IDs: B206–B212
- Depends on: I13、I14

**RED → GREEN**

1. 测 state permutation、received rotation inverse shift、coordinate rotation no shift、uniform-state bit identity、nearest-pilot earlier tie、state exact logsumexp + inner max-log、one-way LDPC spy。
2. 实现 pilot posterior/data LLR/run_b2；每偏振只做一次 fresh decode，无 callback/redecode/message-state reuse。

**Gate**：B201–212 GREEN；all mandatory identities exact。

### Task I16 — Engineering benchmark manifest and required slices

**Files**

- Create: `benchmark.py`
- Create: `test_d0_engineering_benchmark.py`
- Test IDs: EB01–EB06
- Depends on: I11、I12、I13、I15

**RED → GREEN**

1. 测 engineering-only seed900000001/synthetic freeze、decoder batch4/8/12/16、同 waveform 六BPS、十 unique B2 views、HMM primitive/exact aggregate、real atomic I/O。
2. 实现 fake-worker-friendly benchmark orchestration；不执行真实 benchmark。

**Gate**：EB01–06 GREEN；禁止注册 seed、fit、scientific schema/estimand。

### Task I17 — Watchdog, full-work projection and no-science proof

**Files**

- Modify: `benchmark.py`
- Modify: `test_d0_engineering_benchmark.py`
- Test IDs: EB07–EB11
- Depends on: I16

**RED → GREEN**

1. 测 720s watchdog no-partial-pass、完整 frozen workload projection、allowed adjustments 保持 logical manifest、owner line-item partition、7-day threshold/record fields、scientific writer/verdict tripwires。
2. 实现 `BenchmarkReceipt` 与 CLI。receipt 必须记录 owner budget SHA、`86400 s/day`、按 D0 line item 列出的 `consumed_engineering_days` 与 `projected_remaining_D0_days`、互斥的 completed/remaining work IDs、固定 `post_D0_C1_days=2.00`、`contingency_consumed_days`、`required_remaining_contingency_days` 和总式；缺 slice/record/partition/timeout=`INCOMPLETE`。
3. 唯一预算方程冻结为：`projected_D0_days = consumed_engineering_days + projected_remaining_D0_days`；`contingency_consumed_days = max(0, projected_D0_days - 4.50)`；`required_remaining_contingency_days = 0.50 - contingency_consumed_days`；`projected_mission_days = consumed_engineering_days + projected_remaining_D0_days + 2.00 + required_remaining_contingency_days`。completed/remaining work IDs 必须无交、无漏，已耗时间不得再次进入 remaining projection；`required_remaining_contingency_days < 0` 直接超限。

**Gate**：EB01–11 GREEN；unit tests 使用 fake clock，不运行真实 benchmark。

### Task I17A — Real cross-component truth/freeze/no-fit integration seal

**Files**

- Modify: `verify.py`
- Modify only for real binding defects: `benchmark.py` and the already-created D0 production modules
- Modify: `test_d0_contract_views.py`
- Modify: `test_d0_dev_freeze.py`
- Test IDs: CV06–CV08、DF11
- Depends on: I06、I11、I12、I13、I15、I17

**RED → GREEN**

1. 所有真实 receiver/B0/B1/B2/scorer/artifact/evaluator/benchmark callable 已存在后，先增加四个 cross-cutting tests。测试必须对缺 phase、缺 callable、空 registry、missing module fail closed；不得把“不存在”当作无 truth/no-fit。
2. RED seam 是尚未实现的 `verify.DeploymentBoundary.seal(...)` 及实际 benchmark freeze binding；seal 必须枚举并动态/静态检查真实 callable，不得用 mock/placeholder 代替真实 API。
3. CV06 以相同 `ReceiverView` 和两个不同 `TruthView` 运行真实 deployable callable set，要求 output、BPS choice、score、canonical receipt bytes/hash 完全一致；CV07 递归检查实际 signature/annotation/closure/nested type；CV08 对 S1/S2/S3dev/S3test/S4 binding 缺失/wrong `ResolvedDevFreeze` 均拒绝且 receipt 同 hash；DF11 对真实 evaluator 和 `benchmark.py` 做 AST+runtime tripwire，三类 `fit_*` 均不可达且无 dynamic-import bypass。
4. 只实现最小 deployment seal/binding；不得创建 scientific runner、scientific row/estimand 或执行 action。

**Gate**：CV01–09、DF01–12 全部 GREEN；无 placeholder/空 registry/missing-module acceptance；benchmark/evaluator 真实 call graph 不可达 fit。

### Task I18 — Full deterministic/unit integration

**Files**

- Modify only if tests expose a scoped defect: D0 production/test files above
- Verification: all eight test files
- Depends on: I01–I17A

**Steps**

1. Fresh run each file U1–U8；任何 failure 先用 systematic-debugging 建 root-cause evidence，不把修复扩大到 `common/`/legacy/science。
2. Run aggregate:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
$d0Tests = Get-ChildItem -LiteralPath 'projects/simulation/tests' -Filter 'test_d0_*.py' | Select-Object -ExpandProperty FullName
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider @d0Tests -q
```

3. Static call-graph/import scan：truth leakage、fit reachability、O1 receiver reachability、legacy run imports、common/p05 writes、import-time I/O。
4. Recompute contract/artifact/source/test hashes、test counts、protected p05、staging 和 cache census。

**Gate**：all tests GREEN；no new pycache/cache；no source boundary drift；D0 remains NOT_RUN。

### Tasks I19A–I19D — Bounded independent code review

所有 reviewer 必须 fresh、非实现者；单个 task 硬停在 15 分钟内。每个 shard 只读其列明输入并写唯一 review log，统一输出 schema：`VERDICT`、`P0/P1/P2`、`AXES_CLOSED`、`FILES_READ`、`RECEIPT_SHA256S`、`UNRESOLVED`、`STOP_REASON`。到时未闭合即 `INCOMPLETE`，不得由同一 agent 续时。

**I19A — information/physics shard**（owner 相关段、`contract.py/waveform.py/channel.py/receiver.py/methods.py`、CV/WC/RM receipts/tests）：审 truth leakage/O1 boundary、RSS/31、per-real variance、linewidth/no-SOP/scalar units、legal rotations；stop point=上述文件与 axes 1/6/7 全部逐项结论。

**I19B — codec/B2/freeze/statistics shard**（owner 相关段、`codec.py/b2.py/freeze.py/statistics.py/schemas.py`、RM/B2/DF/SS receipts/tests）：审 fresh decoder/exact cost、logical exposure、exact HMM aggregate/no ordinary-float winner、no-refit/non-dev fit、covariance identities；stop point=axes 2–5/7 全部逐项结论。

**I19C — artifacts/benchmark/scope shard**（owner budget/artifact/control 段、`artifacts.py/verify.py/benchmark.py`、AC/EB/CV06–08/DF11 receipts/tests、完整 changed-file manifest）：审 atomic bytes/receipt-last、7 日预算方程与 no-science、common/legacy/p05/governance/scientific drift；stop point=axes 8–10 及保护项逐项结论。

**I19D — fresh integration reviewer**（只在 A/B/C 都完成后）：读取三份完整 shard log及其 hash、I18 aggregate receipt、完整 `git diff --name-status`；在 15 分钟内独立重跑 global scope/hash/call-graph/import guards，复核 shard 覆盖无重叠遗漏，并合并 P0/P1/P2。不得仅复制 shard verdict，也不重新承担逐文件全审。

**Gate**：I19A/B/C/D 均非 `INCOMPLETE`；最终 I19D `P0=0、P1=0`，每个 P2 有明确处置。任一 FAIL/超时回到对应最小 task；修复后受影响 shard 与新的 I19D 必须重审。I20 只认 I19D 最终 PASS。

### Task I20 — Authorized 12-minute engineering throughput benchmark

**Precondition**：I18 PASS + I19A/B/C shard 完整 + I19D independent integration review PASS。此前禁止运行。

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B 'projects/simulation/explore/coded-decoder-feedback/benchmark.py' --class ENGINEERING_THROUGHPUT_V1 --root-seed 900000001 --watchdog-seconds 720 --synthetic-resolved-freeze --output 'projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput'
```

**Required evidence**：四 decoder batch sizes、六 BPS、十 unique B2 views、一个 HMM primitive/aggregate、真实 atomic JSONL/receipt；owner 九字段；logical/materialized work reconciliation；peak memory；owner budget SHA；按六个 D0 line item 的 consumed/remaining days 与非重叠 work IDs；固定 post-D0 C1=`2.00d`；contingency consumed/remaining；完整预算方程和允许优化前后 receipt。

**Terminal**：

- complete slices/records/work partition，且 `consumed_engineering_days + projected_remaining_D0_days + 2.00d_post_D0_C1 + required_remaining_contingency_days <= 7.00d`、remaining contingency 非负 → `ENGINEERING_THROUGHPUT_PASS`。
- 同一完整方程保守结果 `>7.00d` 或 remaining contingency<0，且 allowed vectorization/batch/content-cache/chunk adjustments 不能闭合 → `GREATER_THAN_7D_HARD_BLOCKER`。
- watchdog/record/slice incomplete → `INCOMPLETE`，不得冒充 PASS 或 hard blocker。

该 benchmark 不运行科学 seed、不写 S1–S4、不裁 scientific gate。

## 5. Parallel dispatch map

每批最多 3 个 executor；同一文件的任务必须串行。

```text
Batch 0: I01 -> I02
Batch 1: I03 || I04 || I05
Batch 2: I06 || I07 || I08
Batch 3a: I09 || I11
Batch 3b: I10 (after I11; reads the finalized artifacts boundary)
Batch 4: I12 || I13 || I14
Batch 5: I15
Batch 6: I16 -> I17
Batch 6b: I17A cross-component integration seal
Batch 7: I18
Batch 8a: I19A || I19B || I19C bounded fresh review shards
Batch 8b: I19D fresh integration review
Batch 9: I20 benchmark (only after review PASS)
```

如 Batch 内发现 interface drift，停止依赖方，不并行修同一接口；由主控冻结修订后再重派。每个 executor 只写其列明 production/test 文件与独立 worker log。

## 6. Completion and next governance

本计划的完成定义是：

```text
D0_IMPLEMENTATION = PASS
DETERMINISTIC_UNIT_GATES = PASS
INDEPENDENT_CODE_REVIEW = PASS
ENGINEERING_THROUGHPUT = PASS or genuine >7D hard terminal
D0_SCIENTIFIC_STATUS = NOT_RUN
```

若工程四门 PASS，主控必须用新的 D/V/CP 明确授权后，才可编写/运行 scientific S1–S4 execution plan。若工程门形成真实 `>7D` hard blocker，则按用户合同诚实终止 C1，不删 gate、不以 mini scientific run 抢救。

## 7. Repository handoff discipline

- 本对话不做中间 commit；若后续尚未到 held-out，只在终态统一一次提交。
- 四个 p05 日志始终 untracked/unstaged、SHA 4/4 固定。
- `tools/litdownload/__pycache__/*.pyc` 与 `tools/litsearch/__pycache__/*.pyc` 在最终提交前用 `git cat-file blob HEAD:<path>` 恢复 exact HEAD bytes；禁止 `git restore/checkout/reset`。
- 不 push。
