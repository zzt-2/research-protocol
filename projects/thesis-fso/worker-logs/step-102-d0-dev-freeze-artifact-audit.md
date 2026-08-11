# Step 102 — D0 dev-freeze artifact 与 estimand fresh-context 窄审

> 2026-08-10 | T056 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 证据 worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> 边界：只审 common BPS / B2 statistic / B2 tuple 的 dev freeze 与持久 artifact；未重审 scientific gates

## 1. Findings first / verdict

```text
VERDICT = MINIMAL_ADDITIVE_REPAIR_REQUIRED
SCIENTIFIC_REOPEN = NO_SCIENTIFIC_REOPEN
DEV_FREEZE_EXACTLY_RECOMPUTABLE_NOW = NO
HARD_BLOCKER = NO
TEST_TIME_REFIT_PREVENTED_BY_ARTIFACT_AND_API_CONTRACT_NOW = NO
```

1. **v2 已冻结搜索空间，但没有冻结可复算的 dev 证据面。** common BPS 明列五个 tuple 各自的六格、12-cell equal macro、objective 与 tie-break；B2 明列 732 个 statistic pairs、clean/controlled `0.5/0.5`、五 tuple 与 test-time best-of 禁令。但 `artifact_contract.required_files` 仍只有 S1–S4 raw、S3 lambda、总 ledger、summary 与 receipt；没有 BPS dev raw、HMM grid score、B2 tuple dev raw或三阶段 freeze artifact。仅凭最终 `freeze_sha256` 名称不能反推出 winner。
2. **net-goodput estimand 仍不唯一。** owner 只有 `information_bit_errors/total` 与 `total_transmitted_symbols_per_polarization`，没有“成功交付 CW”或 `delivered_information_bits`；所以合法实现既可用 `information_total-information_errors`，也可用“仅零错误 CW 的 1024 payload bits”，并可能冻结不同 tuple。
3. **controlled sentinel 若进入 objective，会破坏显式 strata 权重。** clean 已占 `0.5`；controlled dual-pol frame 中若 target 与 clean sentinel 都等权进入 controlled half，则总权重实际成为 `0.75 clean + 0.25 controlled-target`。唯一与 `clean:0.5 / controlled:0.5` 一致的解释是：clean 用 X/Y 两行；controlled 只用被注入的 target-pol 行；sentinel 仍完整执行、持久化/缓存并计入 logical/materialized ledger，但 `objective_included=false`。
4. **BPS tie error 字段写错了统计身份。** BPS dev 是 clean/no-injection population，没有 `affected` suffix；`lower_affected_cw_error_rate` 不可从该 population 唯一求值。应 additive 地命名为 `lower_full_frame_cw_error_rate`。B2 tuple tie 则保留 `lower_controlled_affected_cw_error_rate`，只从 controlled target-pol rows 的 affected suffix counts 求值。
5. **HMM 不必持久化 16,689,600 条逐 trajectory score，但普通浮点 chunk sum 也不够。** statistic objective 在“每 trajectory 先除 pilot count”之后只做线性均值；因此按 `tuple × statistic pair × stratum-role × cell × pol × chunk` 保存 exact binary64 superaccumulator、count 与 member-manifest hash，是对 winner 的 lossless sufficient statistic。若实现只存普通 `float64 sum`，则必须退回逐 trajectory normalized-loss raw。
6. **修复是纯 additive artifact/estimand closure。** 不改变 seed、12 cells、五 tuple、六 BPS pairs、732 statistic pairs、阈值、scientific gate、test-time best-of 禁令或 owner 的 logical/materialized exposure。现有 HMM/B2 sentinel work继续记账，只明确不进入 selection objective；故不需要 scientific reopen，也没有静态 hard blocker。

证据锚：v2 owner `common_front_end` 在 `d0-defect-smoke-contract.yaml:224-242`，B2 fit/selection 在 `:244-381`，typed tables/ledger 在 `:491-811`，而 required files 仅见 `:812-818`。step-096 首次识别 dev-freeze exposure/estimand缺口；step-097/100 已闭合 scientific raw/cost与 logical/materialized 双账，但未补 dev selection artifacts。

## 2. 当前 owner 能与不能复算

| Freeze stage | 已唯一的输入空间 | 当前缺失 | 当前是否可从持久 artifact 复算 |
|---|---|---|---|
| 每 tuple common BPS pair | tuples=5；`B={32,64}`；`Nw={31,61,127}`；10 dev seeds；12 cells；B1；tie 后两项 `B,Nw` | BPS dev raw、delivered-bit公式、pol顺序、合法 full-frame error tie字段、per-tuple freeze JSON | **NO** |
| 每 tuple `(p_s,sigma_e2)` | `122×6=732`；uniform prior；per-pilot normalization；smaller-`p_s/sigma` tie | clean/controlled/target/sentinel inclusion、cell/pol顺序、持久 HMM losses或lossless sufficient aggregates、grid显式 float identity | **NO** |
| 最终唯一 B2 tuple | 五 tuple；clean/controlled `0.5/0.5`；pilot fraction→controlled ACWER→M→legal order | delivered-bit公式、sentinel权重、exact aggregation order、raw tuple outcomes、tie numerator/denominator、final freeze JSON | **NO** |

现有 `computation_ledger` 能复算成本，不能替代 selection raw：它保存 decode/HMM工作计数和 content hash，却不保存 B1/B2 goodput numerator、error tie counts或 HMM objective loss。

## 3. 独立冻结的唯一 estimand

### 3.1 Delivered bits、symbol denominator 与 net goodput

对每个 polarization frame、每个 decoded CW：

```text
successful_cw_i := 1[decoded 1024 information bits exactly equal truth]
delivered_information_bits := 1024 * sum_i successful_cw_i
full_frame_cw_errors := 16 - sum_i successful_cw_i

total_transmitted_symbols_per_polarization
  := 32 prefix + 6144 coded-data symbols + periodic_pilot_count(N)

row_net_goodput
  := delivered_information_bits / total_transmitted_symbols_per_polarization
```

`information_bit_total-information_bit_errors` **不等于 delivered bits**：含错误的 CW 不是成功交付的 payload block。denominator 包含 prefix、所有 periodic pilots（含 terminal pilot）和全部 data；不按 puncture/replacement 扣除，因为 owner 明确 no puncture/no replacement。tuple 的精确 denominator 为：

| tuple | pilots | symbols/pol | periodic-pilot fraction（tie） |
|---|---:|---:|---:|
| `(2,100)` | 64 | 6240 | `64/6240 = 2/195` |
| `(3,10)` | 684 | 6860 | `684/6860 = 171/1715` |
| `(3,20)` | 325 | 6501 | `325/6501` |
| `(3,100)` | 64 | 6240 | `2/195` |
| `(3,200)` | 32 | 6208 | `32/6208 = 1/194` |

pilot-fraction numerator只计 OFC17 periodic pilots；32-symbol common prefix对所有 tuple相同，不冒充 tuple pilot overhead，但仍进入 transmitted-symbol denominator。

### 3.2 Inclusion 与 aggregation order

所有 selection 都先验证 exact PK coverage；缺行不得通过“剩余行重归一化”。固定顺序为：

```text
integer counts / per-trajectory normalized loss
  -> within (stratum, cell, polarization) aggregate over seed/fixture
  -> equal mean of X and Y
  -> equal mean of 12 cells
  -> where applicable: 0.5 * clean + 0.5 * controlled-target
```

- **BPS freeze**：只用 common dev seed 的 clean/no-controlled-injection rows；X/Y 都进入，12 cells 等权。每 tuple 独立选择 `(B,Nw)`。
- **HMM statistic freeze**：clean 使用每个 base 的 X/Y；controlled 只使用该 fixture 的 target polarization。sentinel score仍有 artifact/ledger row但 `objective_included=false`。
- **B2 tuple freeze**：clean 使用 X/Y；controlled只使用 target polarization的 full-frame delivered bits；sentinel输出持久化、做 byte/content receipt 和成本记账，但不进 goodput或controlled ACWER。

对 goodput/CWER，先在每个 `(stratum,cell,pol)` 内做 ratio-of-sums，再 equal-pol、equal-cell；所有 fraction 用整数 numerator/denominator 精确计算。对 HMM，先把每 trajectory 的 `-logL/pilot_count` 固化为 canonical binary64，再做 exact sum/count。

### 3.3 三个 winner 的 exact lexicographic key

```text
BPS per tuple:
  maximize macro_net_goodput
  -> minimize macro_full_frame_cwer
  -> minimize B
  -> minimize Nw

HMM statistic pair per tuple:
  minimize 0.5*macro_clean_normalized_nll
         + 0.5*macro_controlled_target_normalized_nll
  -> smaller p_s grid index/value
  -> smaller sigma_e2 grid index/value

final B2 tuple:
  maximize 0.5*macro_clean_net_goodput
         + 0.5*macro_controlled_target_net_goodput
  -> minimize periodic_pilot_count/total_symbols_per_pol
  -> minimize macro_controlled_target_affected_cwer
  -> minimize M
  -> earlier legal tuple order
```

HMM objective 用 exact binary64 accumulator后只在 exact objective相等时触发 smaller-value tie；不得以未登记 tolerance把近似相等改写成 tie。

## 4. 缺失的最小 typed tables

### 4.1 `bps_dev_score`

- PK：`[tuple_id, B, Nw, seed, cell_id, polarization]`
- exact cardinality：`5×6×10×12×2 = 7,200`
- fields：`M,N,B,Nw,seed,cell_id,polarization,method_id=B1,selected_global_rotation_k,successful_cw_count,delivered_information_bits,full_frame_cw_errors,full_frame_cw_total=16,information_bit_errors,information_bit_total=16384,total_transmitted_symbols_per_polarization,computation_id,cache_status,source_computation_id,result_receipt_sha256`
- invariants：delivered=`1024*successful`; full-frame errors=`16-successful`; tuple/grid/seed/cell/pol exact cover；`(2,100)/(3,100)` 可共享 content/computation但必须各保留 logical row；无 boundary/affected字段。

### 4.2 `b2_hmm_grid_chunk`

- PK：`[tuple_id,p_s_index,sigma_e2_index,stratum_role,cell_id,polarization,chunk_id]`
- `stratum_role`：`CLEAN_INCLUDED / CONTROLLED_TARGET_INCLUDED / CONTROLLED_SENTINEL_EXCLUDED`
- fields：`M,N,p_s_index,p_s_float64_hex,sigma_e2_index,sigma_e2_float64_hex,pilot_count,member_count,member_key_manifest_sha256,normalized_nll_exact_sum_numerator_decimal,normalized_nll_exact_sum_denominator_power2,objective_included,computation_ids_manifest_sha256,content_sha256`
- membership counts per tuple/stat-pair/cell/pol：clean=`10`，controlled target=`10×9=90`，controlled sentinel=`90`；总 logical primitive score count仍为 `16,689,600`，objective included count为 `8,784,000`，sentinel excluded count为 `7,905,600`。
- invariants：每个 trajectory先算 canonical binary64 `-logL/pilot_count`；chunk exact sum必须等于这些 binary64值的 exact rational sum；member keys不重不漏；sentinel `objective_included=false`；普通顺序相关 float sum不合格。

逐 trajectory rows不是 winner复算的必要条件，因为其后没有非线性统计或CI；exact sum+count是充分统计。若不实现 exact accumulator，则 required artifact必须退回逐 trajectory `normalized_nll_float64_hex` rows，不能只存 rounded cell mean。

### 4.3 `b2_tuple_clean_dev`

- PK：`[tuple_id,seed,cell_id,polarization]`
- exact cardinality：`5×10×12×2 = 1,200`
- fields：tuple与其 `bps_freeze_ref/stat_freeze_ref`、`successful_cw_count,delivered_information_bits,full_frame_cw_errors,information_bit_errors,total_transmitted_symbols_per_polarization,computation_id,result_receipt_sha256`
- invariants：两份 per-tuple freeze ref必须已存在；两 pol 都 included；不含 controlled fixture字段。

### 4.4 `b2_tuple_controlled_dev`

- PK：`[tuple_id,seed,cell_id,target_polarization,fixture_id,row_polarization]`
- exact cardinality：`5×10×12×2×9×2 = 21,600`
- fields：`M,N,bps_freeze_ref,stat_freeze_ref,target_polarization,row_polarization,row_role={TARGET_INCLUDED,SENTINEL_EXCLUDED},fixture_id,boundary_after_cw,rotation_k,successful_cw_count,delivered_information_bits,full_frame_cw_errors,affected_cw_errors,affected_cw_total,total_transmitted_symbols_per_polarization,computation_id,cache_status,source_computation_id,result_receipt_sha256`
- invariants：`row_role=TARGET_INCLUDED iff row_polarization=target_polarization`；另一 pol严格 sentinel/excluded；每 fixture恰两 row；affected counts只在 target row用于 tie；sentinel仍绑定相同 clean content/source computation并计账。

## 5. Freeze JSON 与 chronology lock

缺失的最小持久文件是：

```text
dev_manifest.json
raw_bps_dev.jsonl
hmm_grid_dev_chunks.jsonl
raw_b2_tuple_clean_dev.jsonl
raw_b2_tuple_controlled_dev.jsonl
dev_freeze.json
dev_freeze_receipt.json
```

`dev_manifest.json` 必须显式列出：10 dev seeds、12 cell IDs及物理值、五 tuple IDs/order、六 BPS pairs、122 个 `p_s` 与6个 `sigma_e2` 的 index+float64-hex、pol/stratum/fixture枚举、expected PK/cardinality、logical/materialized exposure。不能只保留 `numpy.logspace(...)` 生成语句。

`dev_freeze.json` 只保存派生 winner和其证据引用：

```yaml
schema_version: coded_decoder_feedback.d0.dev_freeze.v1
selection_order: [common_bps_by_tuple, b2_statistic_by_tuple, final_b2_tuple]
common_bps_by_tuple:
  <tuple_id>:
    selected: {B: <int>, Nw: <int>}
    macro_net_goodput_exact: {numerator: <int-string>, denominator: <int-string>}
    macro_full_frame_cwer_exact: {numerator: <int-string>, denominator: <int-string>}
    raw_sha256: <sha256>
b2_statistic_by_tuple:
  <tuple_id>:
    selected: {p_s_index: <int>, p_s_float64_hex: <hex>, sigma_e2_index: <int>, sigma_e2_float64_hex: <hex>}
    combined_objective_exact: {numerator: <int-string>, denominator_power2: <int>}
    included_counts: {clean: 240, controlled_target: 2160, controlled_sentinel: 0}
    logical_scored_but_excluded: {controlled_sentinel: 2160}
    grid_chunks_sha256: <sha256>
final_b2_tuple:
  tuple_id: <id>
  selected_B_Nw_ref: <tuple-freeze-ref>
  selected_p_s_sigma_ref: <tuple-freeze-ref>
  macro_net_goodput_exact: {numerator: <int-string>, denominator: <int-string>}
  periodic_pilot_fraction_exact: {numerator: <int>, denominator: <int>}
  macro_controlled_affected_cwer_exact: {numerator: <int-string>, denominator: <int-string>}
  legal_tuple_order_index: <int>
test_lock:
  refit_forbidden: true
  fit_modules_reachable_from_test_runner: false
  required_freeze_sha256: <bound-by-dev_freeze_receipt>
  rejected_seed_ranges: [common_cpr_and_b2_dev, observability_fusion_dev]
```

`dev_freeze_receipt.json` 保存 contract/source/code/dev-manifest、四张 dev table、`dev_freeze.json` 的 SHA256，并保存 `selection_code_sha256`。S1/S2/S3-test/S4 runner必须只接收一个 validated `ResolvedDevFreeze`；其 raw/summary receipt必须反向绑定同一 `dev_freeze_sha256`。静态 test必须证明 test runner import/call graph不可达 `fit_common_bps`、`fit_b2_statistics`、`select_b2_tuple`；只写 `test_time_best_of_forbidden: true` 文本不足以做到 fail-closed。

## 6. owner → implementation → test → consumer → artifact

| Owner family | Pure implementation boundary | 最小 falsifying test | Consumer | Persistent artifact |
|---|---|---|---|---|
| goodput definition / frame length | `metrics.py::delivered_bits_and_symbols` | 1 bit错误使整 CW delivered=0；四 N denominator exact | BPS/B2 selectors；后续 goodput | 两张 score raw + freeze exact fractions |
| per-tuple BPS grid | `freeze.py::select_common_bps_by_tuple` | hand-built 2-cell/pol unequal counts；full-frame error tie；duplicate-N cache不删 logical row | B0/B1/B2/O1 front end | `raw_bps_dev.jsonl` + `dev_freeze.common_bps_by_tuple` |
| HMM pair grid | `freeze.py::select_b2_statistic_by_tuple` | chunking/order变化 winner不变；sentinel加入objective必须 fail；exact tie选小 grid value | B2 posterior/LLR | `hmm_grid_dev_chunks.jsonl` + per-tuple stat freeze |
| clean/controlled row roles | typed constructors `B2CleanDevRow/B2ControlledDevRow` | target/sentinel互换、缺一 pol、sentinel objective=true均 fail | final tuple selector；ledger verifier | clean/control dev raw |
| final tuple selector | `freeze.py::select_final_b2_tuple` | 0.5/0.5 vs错误0.75/0.25 fixture；pilot/CWER/M/order四级 tie | all S1–S4 B2 use；post-D0只读 | `dev_freeze.final_b2_tuple` |
| chronology/no-refit | `freeze.py::load_resolved_freeze_for_test` | test seed触发fit、freeze hash mismatch、fit API reachable均 fail | D0 test runners | `dev_freeze_receipt.json` + all test receipts |
| logical/materialized exposure | existing computation ledger + dev phase coverage | sentinel excluded from objective但logical counts不变；cache charge一次 | budget/runtime gate | computation ledger + dev receipt |

## 7. Owner-ready additive YAML 字段树

以下字段树可直接追加到 `statistical_contract_repair`；旧 scientific threshold、seed、gate与 exposure数字不删除：

```yaml
dev_freeze_artifact_contract:
  schema_version: coded_decoder_feedback.d0.dev_freeze_artifacts.v1
  supersedes:
    - common_front_end.selection.tie_break.lower_affected_cw_error_rate
    - statistical_contract_repair.artifact_contract.required_files
  scientific_contract_change: none
  selection_order: [common_bps_by_tuple, b2_statistic_by_tuple, final_b2_tuple]

  delivered_bit_and_symbol_definition:
    successful_cw: all_1024_decoded_information_bits_equal_truth
    delivered_information_bits: 1024_times_successful_cw_count
    full_frame_cw_errors: 16_minus_successful_cw_count
    total_transmitted_symbols_per_polarization: 32_plus_6144_plus_periodic_pilot_count_for_N
    periodic_pilot_fraction: periodic_pilot_count_divided_by_total_transmitted_symbols_per_polarization
    information_total_minus_information_errors_is_not_goodput: true

  aggregation:
    missing_PK_rows: fail_closed_no_renormalization
    within_cell_pol: ratio_of_integer_sums_for_goodput_and_cwer
    polarization: equal_mean_X_Y_after_complete_coverage
    cells: equal_mean_12_cells
    strata: {clean: 0.5, controlled_target: 0.5}
    clean_rows: both_polarizations
    controlled_objective_rows: target_polarization_only
    controlled_sentinel:
      objective_included: false
      score_output_receipt_and_cost_ledger_required: true

  common_bps:
    table: bps_dev_score
    population: clean_no_controlled_injection
    exact_rows: 7200
    lexicographic: [maximize_macro_net_goodput, minimize_macro_full_frame_cwer, lower_B, lower_Nw]

  b2_statistic:
    table: b2_hmm_grid_chunk
    value: canonical_float64_negative_forward_loglikelihood_per_pilot
    storage: lossless_binary64_exact_sum_and_count_by_chunk
    ordinary_float_chunk_sum_forbidden: true
    objective_included_primitive_scores: 8784000
    logical_primitive_scores_preserved: 16689600
    logical_sentinel_scores_excluded_from_objective: 7905600
    reduction: per_stratum_cell_pol_mean_then_equal_pol_then_equal_12_cells_then_half_clean_half_controlled_target
    lexicographic: [minimize_combined_normalized_nll, smaller_p_s, smaller_sigma_e2]

  b2_tuple:
    tables: [b2_tuple_clean_dev, b2_tuple_controlled_dev]
    exact_rows: {clean: 1200, controlled_all_pol: 21600, controlled_objective_target: 10800, controlled_sentinel_excluded: 10800}
    lexicographic: [maximize_combined_macro_net_goodput, lower_periodic_pilot_fraction, lower_macro_controlled_target_affected_cwer, lower_M, earlier_legal_tuple_order]

  freeze:
    file: dev_freeze.json
    output: exactly_five_BPS_pairs_five_statistic_pairs_and_one_final_tuple
    test_refit_forbidden: true
    test_runner_requires_resolved_freeze: true
    test_runner_fit_call_graph_reachable: false

  artifact_contract_add_required_files:
    - dev_manifest.json
    - raw_bps_dev.jsonl
    - hmm_grid_dev_chunks.jsonl
    - raw_b2_tuple_clean_dev.jsonl
    - raw_b2_tuple_controlled_dev.jsonl
    - dev_freeze.json
    - dev_freeze_receipt.json
  receipt_hashes_add:
    - dev_manifest_sha256
    - each_dev_raw_or_chunk_file_sha256
    - dev_freeze_sha256
    - selection_code_sha256
  all_S1_S2_S3test_S4_receipts_require_same_dev_freeze_sha256: true
```

## 8. Scientific/budget boundary

| 冻结项 | v2值 | additive repair后 | 改变？ |
|---|---|---|---|
| seeds | 8000–8009 dev及既有disjoint ranges | 原样 | NO |
| population | 12 cells、X/Y | 原样；只显式 equal-pol顺序 | NO |
| tuples | 5 | 原样 | NO |
| BPS grid | 6 pairs | 原样 | NO |
| HMM grid | `122×6` | 原样并显式 float identity | NO |
| thresholds / S1–S4 gates | owner当前值 | 原样 | NO |
| test-time best-of | forbidden | artifact+API fail-closed | NO（只强化执行） |
| logical HMM/B2 sentinel exposure | 当前计入 | 仍计入并持久化/缓存；objective排除 | NO |
| logical/materialized decoder totals | `69,360/1,032,000/20,640,000` 与 `48,900/704,640/14,092,800` pre-S4 | 原样 | NO |

sentinel exclusion不是删 exposure，而是把现有 `strata_weight 0.5/0.5` 翻译成唯一 estimand。若坚持让 sentinel进入 controlled objective，必须显式把 scientific strata权重改成 `clean=0.5, controlled-target=0.25, controlled-sentinel=0.25`；那将是 scientific reopen，本报告拒绝该路线。

## 9. Protection / terminal receipt

- owner启动 SHA256：`c3a471f50b770d4f366296aab14034c60f9388ca6d476d9d4fc7458e33b9c0c6`。
- YAML independent parse：`PASS`；schema=`coded_decoder_feedback.d0.v2`；status=`asset_contract_candidate_pending_fresh_verification`。
- required files复核：现有9项中唯一含 dev/freeze字样的是 `raw_s3_dev.jsonl` 与 `s3_lambda_freeze.json`，均不承载 BPS/B2 dev freeze。
- protected p05启动 SHA256：
  - `p05_run.log`=`7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log`=`735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log`=`c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log`=`95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- 启动 staging：`0`；目标文件启动时不存在。
- 末次复核：owner final SHA与启动值一致；p05=`4/4 MATCH`；staging=`0`；本任务唯一写入为本 step-102，状态为新增未暂存。
- 未执行 import项目、pytest、D0、仿真、benchmark、web/search/download、commit/push；未修改 owner、源码、测试、结果、治理或 p05。

```text
TERMINAL = MINIMAL_ADDITIVE_REPAIR_REQUIRED / NO_SCIENTIFIC_REOPEN
```
