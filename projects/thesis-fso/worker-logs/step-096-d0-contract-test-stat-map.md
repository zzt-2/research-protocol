# Step 096 — D0 合同到测试、统计与批次架构映射

> 2026-08-10 | T050 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 范围：只读映射冻结 D0 owner 到实现、测试、统计与批次；不重审 step-091 已接受的设计优劣。  
> 禁止动作回执：未运行 import probe、pytest、D0、仿真、web/search/download；未修改 owner、源码、测试、结果、治理文件或 p05；未 commit/push。

## 1. Verdict / findings first

**verdict=`CONTRACT_AMBIGUITY`；blocking ambiguities=`3`；当前没有足够证据判 `BUDGET_BLOCKER`。**

三个 blocker 都会阻止“同一 raw input 得到唯一可复算 verdict”，不是对科学设计优劣的重审：

1. **B1 — raw-row 不是可复算的分层 schema。** YAML 仅列 19 个公共字段（owner `:226-247`），没有类型、nullable、主键或分层扩展。它无法承载 S1 event/seed/cell 计数、S3 truth candidate/10 候选分数/rank/top1/MRR/lambda，也无法承载 S4 check-id/PASS；因此 S1/S3/S4 gate 不能从 owner 指定 raw rows 独立重算。`boundary_after_cw`、`rotation_k`、`jump_present` 对 natural/clean 行如何表示也未定义。
2. **B2 — S2 cached twin 的物理执行数、逻辑投影数和 estimand 权重未闭合。** owner 同时给 `540` injected cases、`60` cached no-jump twins（`:297-302`）、逐行 `fixture_id/boundary/rotation`，以及按 affected-CW pooled counts 的 B1-on−B1-off（`:252-256,304`）。一个 off decode 是只产生 1 行，还是按 9 个 boundary×rotation 产生 9 个 fixture-aligned 逻辑投影未冻结；两种做法改变 off 分母/权重和 raw-row 数。推荐最小修订：冻结为 **60 次物理 off decode + 540 个 fixture-aligned off logical projections**，每个 on fixture 与同 boundary 的 cached off suffix 一一配对；物理成本只计一次。
3. **B3 — S3 test estimand/CI 与 dev/B2 成本单位未闭合。** S3 给 gate 阈值（`:354-360`），但没有冻结 test 上 per-case top1、paired MRR delta、逐 cell→equal-cell macro、seed-block bootstrap 的 raw→aggregate 规则；全局 `cluster_block` 反而写入 S2 的 cached twins。与此同时 B2 的 `calls_per_method_frame=2`（`:161-162`）、S2 target-pol row、S3 `88 CW/case` 和 cached reuse 没有统一“物理执行/逻辑行/增量 candidate cost”单位，故不能从 owner 唯一生成完整 cost ledger 或精确 dev-freeze batch 总数。

非阻塞但应随最小修订关闭：S1 有 20/50 seed blocks，却沿用全局“sample the ten seed blocks”；S1 descriptive CI 应改为重采样实际观察到的 20 或 50 blocks。Percentile 应显式冻结 NumPy `method="linear"`，避免版本默认值漂移。

## 2. 数量复算

| 项 | 复算 | 结论 / 单位边界 |
|---|---:|---|
| population cells | `4 SNR × 3 linewidth = 12` | PASS；其余 physical 字段固定，不增加 cell 轴。 |
| S1 first stage | `20 seeds × 12 cells = 240 dual-pol frames` | PASS；等于 `480` polarization trajectories。 |
| S1 maximum | `50 × 12 = 600 dual-pol frames = 1200 pol trajectories` | PASS。 |
| S2 base clusters | `10 seeds × 3 cells × 2 target pol = 60` | PASS。 |
| S2 injected | `60 × 3 boundaries × 3 rotations = 540` | PASS。 |
| S2 cached off | `60` physical cached twins | PASS as execution count；logical projection/raw-row count属 B2 ambiguity。 |
| S3 candidates | `3 × 3 + noop = 10` | PASS。 |
| S3 work/case | `16(noop) + 3 rotations × (12+8+4 suffix CW) = 88 CW decodes` | PASS，指 target-pol candidate incremental ledger。 |
| S3 test work | `540 × 88 = 47,520 CW decodes` | PASS。dev slice若同样 540 cases，则另有 `47,520`，合计 `95,040`，不能把 test maximum 当全 S3 总量。 |
| S4 | `10 seeds × 3 cells × 2 pol = 60 trajectories` | PASS。 |
| engineering days | D0 `0.25+0.75+0.50+2.00+0.50+0.50=4.50`; post-D0 `2.00`; contingency `0.50` | 算术 PASS：base `6.50`、hard ceiling `7.00`。静态证据不足以判定实际必超 7 日。 |

## 3. owner → implementation → test → consumer → artifact 矩阵

| Owner field/family | 最小 module / pure function | TDD test | Consumer | Artifact field |
|---|---|---|---|---|
| `schema_version/status/control/purpose` | `contract.py::load_frozen_contract/validate_control` | schema、status、D010/V004/CP011 exact match | all | `receipt.contract_sha256/control` |
| `invariants/views` | `chain.py::ReceiverView/TruthView`; `validate_receiver_boundary` | forbidden-field constructor/recursive-call-boundary test | S1–S4 | `receipt.view_boundary_pass` |
| `population.code/physical/provenance` | `chain.py::PopulationCell/factory`; reuse codec/BPS assets | 12-cell Cartesian product、1024/1536/16/384/6144 identity、source exists/hash | all | `manifest.cells/code/source_receipts` |
| all `seed_plan.*` | `contract.py::SeedRegistry` | exact inclusive ranges、pairwise disjoint、stratum membership | dev/S1–S4/post-D0 guard | `manifest.seed_ranges/seed_list` |
| `common_front_end.*` | `chain.py::freeze_common_bps` | 6-grid、12-cell equal macro、B1-only selection、tie-break | B0/B1/B2/O1, S1–S4 | `freeze.common_bps_by_tuple` |
| `b2_primary.source/legal_tuples/waveform` | `b2.py::build_extended_waveform/validate_tuple` | tuple whitelist、pilot formula/count、no replace/puncture、shared support | B0/B1/B2/O1; S2/S3 | `freeze.b2.tuple/pilot_mask/source` |
| `b2_primary.receiver_visible_statistics` | `b2.py::pilot_emission/hmm_posterior/mixture_llr` | ReceiverView-only、log normalization、earlier-pilot tie、clip30/clamp20 | B2; S3 pilot score | `rows.score_meta`, `freeze.b2.ps_sigma` |
| `b2_primary.decoder_interaction/dev_selection` | `b2.py::restart_decode/freeze_b2` | empty state every call、no feedback、test no refit、lexicographic ties | S2/S3/S4 | `freeze.b2`, cost fields |
| `baselines.B0/B1/B2/O1` | `methods.py::run_B0/run_B1/run_B2/run_O1` | semantic IDs、B1 4 legal rotations、O1 evaluator-only、same waveform | S2/S4; S3 caches | `rows.method_id`, error/cost counts |
| `event_definition.*` | `diagnostic.py::detect_persistent_transition` | 28/32 windows、merge≤32、X/Y separate、multi-transition occurrence-only | S1 | `s1_events.*` (missing owner extension) |
| `controlled_fixture.*` | `fixtures.py::make_twin_fixture/project_affected_suffix` | boundaries 4/8/12↔1536/3072/4608、k=1/2/3、one target pol、same random twin | S2/S3/S4 | `rows.fixture_id/boundary/rotation/jump_present` |
| `statistics.raw_row_required_fields` | `schema.py::validate_raw_row/validate_dataset_keys` | types/domains/nullability, uniqueness, error≤total, nonnegative costs, finite latency | S2 + all audit | `raw_rows.jsonl` |
| `statistics.cell_estimands/macro_aggregation` | `stats.py::aggregate_s2_cells/equal_cell_macro` | hand-calculated unequal-denominator fixtures; reject all-cell pooling/mean-of-ratios | S2 | `summary.s2.cell/macro` |
| `statistics.uncertainty/zero_denominator/coverage` | `stats.py::bootstrap_s2` | deterministic PCG64, 10,000 reps, NA boundary cases, unclipped CI/display clip | S2 | `summary.s2.bootstrap/terminals` |
| `S1_*` | `run.py::run_s1`; `stats.py::summarize_s1` | 240→600 escalation、12/4/2 conjunct、no injected rows | S1 gate | `summary.s1` |
| `S2_*` | `run.py::run_s2`; `stats.py::gate_s2` | 60/540/60 physical counts、natural exclusion、damage/recovery/coverage thresholds | S2 gate | `summary.s2` |
| `S3_*` | `diagnostic.py::score_candidates/rank`; `stats.py::aggregate_s3/bootstrap_s3` | 10 candidates、88 CW, same bit support、tie-break、dev-only lambda、paired MRR | S3 gate | `s3_rank_rows.jsonl`, `summary.s3` |
| `S4_*` | `verify.py::run_s4_checks` | seven named requirements independently fail closed | S4 gate | `s4_checks.jsonl`, `cost_ledger.json` |
| `gate_conjunction/post_d0_boundary` | `verify.py::adjudicate_d0` | all-strata conjunct、no pooling、one named terminal、never authorize C1 action | final | `gate.json.terminal_verdict` |
| `engineering_budget_days.*` | `run.py::CostLedger/check_budget_ceiling` | all required line items present；no gate deletion；>7d→blocker | orchestration | `cost_ledger.engineering_days` |

公共 raw fields 的最低 validator 规则：enum `stratum/method_id/target_polarization`；`seed` 为合法范围内 int；`cell_id/fixture_id` 非空且在 manifest；errors/totals/decode counts/BP iterations 为非负 int且 errors≤totals；latency finite≥0；controlled on 行 boundary∈{4,8,12}、rotation∈{1,2,3}。内部 NA 用 typed `None`，JSON 写 `null`，禁止 NaN。必须由 owner 增补的分层字段：S1 event fields；S3 candidate/score/rank/top1/MRR/lambda；S4 check-id/status；以及 natural/clean 对 boundary/rotation/jump 的 nullability。

## 4. 纯统计接口与精确规则

```python
def aggregate_s2_cells(rows: tuple[RawRow, ...]) -> S2Point:
    """每 cell 先 pooled affected-CW counts，再 equal-weight 三 cell macro。"""

def bootstrap_s2(
    seed_blocks: tuple[SeedBlock, ...],
    *, n_replicates: int = 10_000,
    rng_seed: int = 2026081001,
    percentile: tuple[float, float] = (2.5, 97.5),
    percentile_method: str = "linear",
) -> S2BootstrapReport:
    """纯函数；内部显式 Generator(PCG64(rng_seed))；无 I/O/全局 RNG。"""

def aggregate_s3_cases(rows: tuple[S3RankRow, ...], lambda_frozen: float) -> S3Point:
    """建议 owner 冻结：per-case top1 与 RR；逐 cell mean；三 cell equal macro。"""
```

每个 S2 replicate 从 10 个 seed blocks 有放回抽 10 个索引；抽中 seed 时复制其三 cells、双 target-pol、九 fixtures及 fixture-aligned cached-off projections。逐 cell 重算：

```text
damage_c  = E(B1_on)/T(B1_on) - E(B1_off)/T(B1_off)
recovery_c= [E(B1_on)-E(O1_on)] / E(B1_on)
coverage_c= [E(B1_on)-E(B2_on)] / [E(B1_on)-E(O1_on)]
macro      = (estimand_hard + estimand_mid + estimand_clean) / 3
```

- point 或 replicate 中任一 cell `E(B1_on)<=0`：recoverability 为 NA；point fail=`ZERO_PRACTICAL_CODED_DAMAGE`，bootstrap invalid。
- 任一 cell `E(B1_on)-E(O1_on)<=0`：coverage 为 NA；point fail=`ZERO_RECOVERABLE_HEADROOM`，bootstrap invalid。
- NA 保留为 NA，不填 0/1。以 10,000 为 invalid-fraction 分母；`invalid_fraction<=0.05` 且 `valid>=9500` 才计算 valid-only percentile CI。恰好 500 invalid / 9500 valid 可通过。
- recoverability 超限 terminal=`UNSTABLE_DAMAGE_DENOMINATOR`；coverage 超限 terminal=`UNSTABLE_HEADROOM`；二者同时出现时都记录，不采用 first-wins，也不输出该 metric CI。
- coverage CI 用 unclipped ratios；仅展示副本 clip 到 `[0,1]`。damage 无 ratio invalid replicate。
- S3 没有 ratio denominator；推荐每 seed block含 `3 cells×2 pol×9 truth fixtures=54` cases，在 replicate 内重算 per-cell top1/MRR 与 equal-cell macro；paired increment为同一 case的 `RR_fused-RR_pilot`。此规则须写回 owner 才可执行。

## 5. 测试清单

1. raw schema：缺字段、额外/错误 enum、nullability、duplicate primary key、NaN/Inf、errors>total、负 cost 均 fail；artifact reader raw→summary exact recompute。
2. seed：全部 range inclusive、pairwise disjoint；dev/test/S1/S2/S3/S4 cross-use fail；manifest seed 与 raw seed exact cover。
3. twin/no pooling：同一 seed/cell/pol/fixture on-off random receipt相同；自然 rows 进入 S2 fail；跨 cell pooled ratio或跨 stratum pooled summary fail。
4. stats：PCG64 golden index stream；同 input bitwise-stable；10,000/9500/0.05 边界；两个 zero denominators与两个 terminals；equal-cell macro对 cell size 不敏感；coverage CI不裁剪。
5. gates：S1 的 12 AND 4 AND 2、S2 所有子 gate、S3 absolute AND incremental、S4 七项及四 strata总合取；任一缺失/NA不许 PASS。
6. restart/candidate：每 changed LLR 空 state full restart；88 CW exact；相同 full-frame bit denominator；candidate tie固定 noop→earlier boundary→lower k。
7. artifact：先写同目录 temp，flush+fsync，`os.replace`；JSON `allow_nan=False`；写后 SHA256；receipt含 owner/source/code/freeze/seed manifest hashes；中断保留旧完整 artifact；hash/source receipt mismatch fail。

现有 `common/_experiment.py::save_results` 只做直接 `open(...,'w')`、局部 MD5/Git meta，非 atomic，也不生成 artifact SHA/source receipt；`test_experiment_json_encoding.py` 只覆盖 UTF-8。因此 D0 不能把它当完成态 writer，但可复用其 UTF-8行为测试。

## 6. ≤15 分钟 batch 架构与 fail-fast

只读实证锚：现有 P08-R2 gate artifact记录约 `400.9 s`，源码路径约执行 `96,960` CW decodes（workspace/tune/test粗计）；不能外推为正式 SLA，只用于把 D0 job 留出充足余量。**安全上限先设每 job≤30,000 CW decodes且 wall watchdog=12 min，15 min硬杀；首个小样本校准后只能缩 batch，不能删科学 gate。**

| Work | Batch key | 每 job 上界 / job 数 |
|---|---|---|
| static/schema/identity | test group | 无科学 run；先全部通过，否则 0 science jobs |
| S1 | one seed × 12 cells | 12 frames/24 pol trajectories；first 20 jobs，必要时再30 |
| S2 | one seed block | 54 on +6 physical cached off；10 jobs；method rows/logic projections另计，不重复 off decode |
| S3 dev/test | one seed block | `54×88=4,752 CW`；dev 10 + test 10 jobs；lambda grid只消费 cached scores，不重译码 |
| S4 | one seed block | 6 trajectories；10 jobs |
| bootstrap/gates | one pure CPU job per stratum | 10,000 reps，读 frozen raw only；不和生成混在一 job |
| BPS/B2 freeze | `(tuple, grid chunk, seed block)` | 先 cache waveform/pilot emissions；HMM `p_s×sigma` grid按 tuple/chunk并行，decoder只消费冻结候选；因 B3 未冻结总 exposure，当前不得声称 exact job count |
| merge/publish | one writer | 校验 complete manifest→原子合并→hash→receipt；worker不得并发写最终 artifact |

可前置 fail-fast：contract/schema/control、source hash、seed disjointness、12-cell/count manifests、pilot-count formulas、ReceiverView boundary、noiseless mapping/rotation/interleaver、decoder empty-state、raw validator、小型 handcrafted stats/NA tests、每 job manifest/cost ceiling。不得提前删减 S1 occurrence、S2 damage/recovery/B2、S3 absolute/incremental或 S4任何 gate；小样本只验证管道，不做科学裁决。

## 7. 最少文件树与 TDD 拆分

```text
projects/simulation/explore/coded-decoder-feedback-d0/
  contract.py      # typed owner + seed/cell/batch manifests
  chain.py         # Receiver/Truth views, population, B0/B1/O1, fixtures
  b2.py            # OFC17 adaptation + dev freeze
  stats.py         # base/stratum schemas, S2/S3 aggregation/bootstrap/gates
  run.py           # resumable workers, cost ledger, atomic artifacts/receipts
  verify.py        # raw→summary recompute, S1–S4 conjunction, terminal
projects/simulation/tests/
  test_d0_contract_schema.py
  test_d0_chain_identity.py
  test_d0_b2_freeze.py
  test_d0_stats.py
  test_d0_artifacts_and_gates.py
```

TDD/task dependency：`contract/schema` 先行；其后 `chain identity`、`stats`、`artifact writer` 可并行；`b2` 依赖 contract+chain；`run` 依赖 contract+chain+b2+stats；`verify` 最后依赖 schema+stats+artifact。S1 runner、S2 fixture/method runner、S3 scorer可在公共 chain/schema冻结后并行；最终 merge/gate不可并行。每个 executor只领上述一个 bounded batch或一个测试文件，watchdog保证≤15分钟。

## 8. 最小 owner 修订（本任务不直接修改）

1. 增加 base raw schema 的 types/nullability/primary key及 S1/S3/S4 extension fields。
2. 明示 S2 `60 physical off decodes → 540 fixture-aligned logical projections`（或选择另一语义并同步冻结 estimand权重）；分别列 physical case、logical row、method row、decode-cost counts。
3. 冻结 S3 test per-case→cell→macro estimand与 seed bootstrap block；冻结 BPS/B2 dev exposure、pol/clean/controlled权重及完整 cost-ledger单位。
4. S1 descriptive bootstrap改为 observed 20/50 blocks；percentile显式 `method=linear`。

在上述三项 blocking contract ambiguity 未关闭前，不应开始 D0；关闭后无需删减任何科学 gate，预计可转为 `EXECUTABLE_AS_FROZEN`。当前也不能仅凭静态材料判 `>7D_HARD_BLOCKER`。

## 9. Protection receipt

- 启动 owner SHA256：D0 YAML=`32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936`；preflight=`63F1D0881FB88CAD4044737091FB0ABAA7AEA27D50B8DEFD48EC6D8C23C3DAF8`。
- p05 启动 SHA256：`p05_run.log=7843B048...4F11`；`p05_run2.log=735E4650...38B`；`p05_run3.log=C76887C6...34D`；`p05_run4.log=95A1D184...21DE`。
- 启动 staging为空；目标文件启动时不存在。
- 唯一写入：`projects/thesis-fso/worker-logs/step-096-d0-contract-test-stat-map.md`。
- 未执行任何 import/pytest/probe/D0/仿真；未触碰 owner、p05、源码、测试、结果或治理文件。
