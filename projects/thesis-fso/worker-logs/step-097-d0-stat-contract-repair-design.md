# Step 097 — D0 统计合同三项歧义的最小修复设计

> 2026-08-10 | T051 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 范围：只给 B1 raw schema、B2 cached twin、B3 S3 estimand/CI/cost 的静态修复设计；不修改 owner、治理、源码、测试或结果，不执行 D0/仿真/import/pytest。  
> 结论先行：**`verdict=MINIMAL_REPAIR_READY`**。当前 YAML 在修复真正写入并经 fresh verifier 接收前仍是 `CONTRACT_AMBIGUITY`，本日志本身不授权 D0。

## 1. Findings first

1. **B1 可由四张互斥 typed table 闭合。** Natural/clean 行不再用 `null boundary/rotation` 冒充 controlled 行；S1 trajectory、S2 method projection、S3 candidate score、S4 check 各有独立主键和非空字段。rank/top1/RR 是 raw score 的确定性派生量，不作为可互相矛盾的第二份 raw truth。
2. **B2 冻结为 `60 physical off computations -> 540 fixture-aligned logical off projections`。** 每个 `seed×cell×target_pol` 只执行一次 B1-off；九个 off projection 共用同一 `computation_id`，按对应 boundary 的 suffix 取数并与九个 on fixtures 一一配对。统计行可重复投影，decoder/cost 账本按唯一 computation 只计一次。
3. **B3 可在不改任何 seed、threshold、gate 或预算数字下闭合。** S3 的 dev/test 都是每 seed `3 cells×2 pol×9 fixtures=54 cases`；先逐 case 算 pilot/fused RR 与 top1，再逐 cell 求均值、最后三 cell 等权 macro；test CI 按 seed block bootstrap。S3 的 `88 CW/case` 明确定义为 target-polarization candidate-scoring incremental cost，而非整个双偏振链路总成本。
4. **S1 descriptive CI 必须重采样实际观察到的 seed blocks。** first stage 用 20 blocks；发生 escalation 后用完整 50 blocks，不得仍写“ten blocks”，也不得只抽新增 30 blocks。
5. **所有 percentile 显式为 NumPy `method="linear"`。** 每个 stratum 独立新建 `Generator(PCG64(2026081001))`，避免执行顺序改变 RNG stream。
6. **没有 scientific reopen 或 budget blocker。** 本设计只补 schema、estimand 顺序、cache/cost unit；未改变 population、seed、threshold、gate、test-time best-of 禁令或 `4.50/6.50/7.00 d`。静态计数不能证明实际工时必超 7 日。

## 2. 仓库内可复用 pattern 与边界

| Pattern | 可复用部分 | 不可直接照搬部分 |
|---|---|---|
| `projects/simulation/params.py` Pydantic frozen models | enum、typed field、frozen object | 当前 models 未形成 D0 分层 row/PK；D0 validator 还须 `strict=true, extra=forbid`。 |
| `projects/simulation/explore/b10-source-native-adaptive-rls-cpr/run_all.py::validate_checkpoint_rows` | canonical integer key、duplicate/missing/prefix fail-closed | 其 30-row cell key 是 B10 专属，不能当 D0 四 strata schema。 |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py::bootstrap_ci` | local deterministic RNG、index resampling、percentile骨架 | 只有 trajectory mean、2,000 reps，未声明 `method=linear`，没有 seed-block/cell macro/invalid replicate 语义。 |
| `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/residual_artifact.py` | exact field-set validation、finite check、`allow_nan=False`、canonical SHA256 | 是单一 residual artifact，不含 JSONL row PK、cluster bootstrap 或 computation ledger。 |
| `projects/simulation/explore/b10-source-native-adaptive-rls-cpr/run_all.py::atomic_save_validation` | same-directory temp、file fsync、`os.replace`、directory fsync | 内部仍调用通用 `save_results`；D0 需在写前完成 strict schema/PK/completeness 校验并在写后记录 SHA256。 |

结论：仓库内没有一份可原样复用的 end-to-end D0 pattern；最小合法组合是 **frozen typed model + canonical PK validator + block-bootstrap pure function + canonical/atomic artifact writer**。

## 3. 可直接粘贴进 YAML 的最小字段树

以下作为新的顶层 `statistical_contract_repair` 粘贴；其 `supersedes` 明确取代旧的扁平 `statistics.raw_row_required_fields` 和歧义 cost 解释。已有 scientific fields/thresholds 不删除、不改值。

```yaml
statistical_contract_repair:
  schema_version: coded_decoder_feedback.d0.statistics.v2
  supersedes:
    - statistics.raw_row_required_fields
    - statistics.cluster_block
    - strata.S1_natural_occurrence.uncertainty
    - strata.S2_controlled_damage_recoverability_absorption.cached_no_jump_twins
    - strata.S3_controlled_observability.full_restart_cw_decodes_per_case

  serialization:
    format: jsonl_utf8
    strict_types: true
    extra_fields: forbid
    json_nan_and_infinity: forbid
    internal_missing_value: typed_none
    serialized_missing_value: null
    numeric_finiteness: required_unless_summary_status_is_NA
    canonical_json: {sort_keys: true, separators: [",", ":"], allow_nan: false}

  enums:
    polarization: [X, Y]
    fixture_id: [B04_K1, B04_K2, B04_K3, B08_K1, B08_K2, B08_K3, B12_K1, B12_K2, B12_K3]
    candidate_id: [NOOP, B04_K1, B04_K2, B04_K3, B08_K1, B08_K2, B08_K3, B12_K1, B12_K2, B12_K3]
    s2_method_id:
      - GLOBAL_FOUR_ROTATION_DECODER_SELECTION
      - OFC17_16QAM_EXTFRAME_V1
      - TRUTH_BOUNDARY_ROTATION_CORRECTION
    s4_check_id:
      - no_slip_noiseless_B0_B1_O1_identity
      - all_rotation_boundary_noiseless_O1_zero_error
      - mapping_rotation_truth_metamorphic_pass
      - candidate_isolation_and_empty_decoder_state_pass
      - all_scores_finite_and_deterministic
      - no_truth_field_reaches_receiver_view
      - diagnostic_cost_ledger_complete

  foreign_keys:
    cell_id: population_manifest.cell_id
    seed:
      S1_TRAJECTORY: seed_plan.natural_occurrence
      S2_METHOD: seed_plan.controlled_damage_recovery
      S3_CANDIDATE_DEV: seed_plan.observability_fusion_dev
      S3_CANDIDATE_TEST: seed_plan.controlled_observability
      S4_CHECK: seed_plan.clean_diagnostic

  tables:
    s1_trajectory:
      record_type: {type: string, const: S1_TRAJECTORY, nullable: false}
      primary_key: [record_type, seed, cell_id, target_polarization]
      fields:
        seed: {type: int64, minimum: 0, nullable: false}
        cell_id: {type: string, min_length: 1, nullable: false}
        target_polarization: {type: string, enum_ref: polarization, nullable: false}
        persistent_transition_count: {type: int64, minimum: 0, nullable: false}
        persistent_transition_after_symbol: {type: array_int64, minimum_item: 0, nullable: false}
        event_present: {type: boolean, nullable: false}
        trajectory_receipt_sha256: {type: sha256_lower_hex, nullable: false}
      invariants:
        - event_present_equals_persistent_transition_count_gt_zero
        - array_length_equals_persistent_transition_count
        - boundary_rotation_jump_and_method_fields_absent_not_null

    s2_method:
      record_type: {type: string, const: S2_METHOD, nullable: false}
      primary_key: [record_type, seed, cell_id, target_polarization, fixture_id, jump_present, method_id]
      fields:
        seed: {type: int64, minimum: 0, nullable: false}
        cell_id: {type: string, min_length: 1, nullable: false}
        target_polarization: {type: string, enum_ref: polarization, nullable: false}
        fixture_id: {type: string, enum_ref: fixture_id, nullable: false}
        boundary_after_cw: {type: int64, enum: [4, 8, 12], nullable: false}
        rotation_k: {type: int64, enum: [1, 2, 3], nullable: false}
        jump_present: {type: boolean, nullable: false}
        projection_role: {type: string, enum: [DIRECT_ON, CACHED_OFF_PROJECTION], nullable: false}
        physical_case_id: {type: string, min_length: 1, nullable: false}
        computation_id: {type: string, min_length: 1, nullable: false}
        method_id: {type: string, enum_ref: s2_method_id, nullable: false}
        affected_cw_errors: {type: int64, minimum: 0, nullable: false}
        affected_cw_total: {type: int64, enum: [4, 8, 12], nullable: false}
        information_bit_errors: {type: int64, minimum: 0, nullable: false}
        information_bit_total: {type: int64, const: 16384, nullable: false}
        total_transmitted_symbols_per_polarization: {type: int64, minimum: 6208, nullable: false}
        result_receipt_sha256: {type: sha256_lower_hex, nullable: false}
      invariants:
        - affected_cw_errors_lte_affected_cw_total
        - information_bit_errors_lte_information_bit_total
        - affected_cw_total_equals_16_minus_boundary_after_cw
        - fixture_id_bijection_with_boundary_after_cw_and_rotation_k
        - DIRECT_ON_iff_jump_present_true
        - CACHED_OFF_PROJECTION_iff_jump_present_false
        - on_rows_methods_exactly_B1_B2_O1
        - off_rows_method_exactly_B1
        - each_off_physical_case_has_nine_fixture_projections_and_one_computation_id

    s3_candidate:
      record_type: {type: string, enum: [S3_CANDIDATE_DEV, S3_CANDIDATE_TEST], nullable: false}
      primary_key: [record_type, seed, cell_id, target_polarization, fixture_id, candidate_id]
      fields:
        seed: {type: int64, minimum: 0, nullable: false}
        cell_id: {type: string, enum: [hard, mid, clean], nullable: false}
        target_polarization: {type: string, enum_ref: polarization, nullable: false}
        fixture_id: {type: string, enum_ref: fixture_id, nullable: false}
        truth_candidate_id: {type: string, enum_ref: fixture_id, nullable: false}
        candidate_id: {type: string, enum_ref: candidate_id, nullable: false}
        pilot_score: {type: float64, finite: true, nullable: false}
        decoder_score: {type: float64, finite: true, nullable: false}
        computation_id: {type: string, min_length: 1, nullable: false}
        changed_cw_decodes: {type: int64, enum: [4, 8, 12, 16], nullable: false}
        cached_unchanged_cw_nll_reads: {type: int64, enum: [0, 4, 8, 12], nullable: false}
        result_receipt_sha256: {type: sha256_lower_hex, nullable: false}
      invariants:
        - truth_candidate_id_equals_fixture_id
        - exactly_ten_candidate_rows_per_case
        - NOOP_has_changed16_cached0
        - B04_candidates_have_changed12_cached4
        - B08_candidates_have_changed8_cached8
        - B12_candidates_have_changed4_cached12
        - rank_top1_rr_and_fused_score_are_derived_not_raw

    s3_lambda_freeze:
      record_type: {type: string, const: S3_LAMBDA_FREEZE, nullable: false}
      primary_key: [record_type]
      fields:
        lambda_frozen: {type: float64, enum: [0.25, 0.5, 1.0, 2.0, 4.0], nullable: false}
        dev_rows_sha256: {type: sha256_lower_hex, nullable: false}
        objective: {type: string, const: macro_MRR_then_macro_top1_then_smaller_lambda, nullable: false}
        test_rows_read_during_selection: {type: boolean, const: false, nullable: false}
        freeze_receipt_sha256: {type: sha256_lower_hex, nullable: false}

    s4_check:
      record_type: {type: string, const: S4_CHECK, nullable: false}
      primary_key: [record_type, check_id]
      fields:
        check_id: {type: string, enum_ref: s4_check_id, nullable: false}
        tested_instances: {type: int64, minimum: 1, nullable: false}
        failed_instances: {type: int64, minimum: 0, nullable: false}
        passed: {type: boolean, nullable: false}
        evidence_sha256: {type: sha256_lower_hex, nullable: false}
      invariants:
        - failed_instances_lte_tested_instances
        - passed_iff_failed_instances_equals_zero
        - seed_cell_boundary_rotation_fields_absent_not_null

    computation_ledger:
      record_type: {type: string, const: COMPUTATION, nullable: false}
      primary_key: [computation_id]
      fields:
        computation_id: {type: string, min_length: 1, nullable: false}
        phase: {type: string, enum: [BPS_DEV, B2_DEV, S2, S3_DEV, S3_TEST, S4], nullable: false}
        operation: {type: string, enum: [B1_DECODE, B2_DECODE, O1_DECODE, CANDIDATE_DECODE, HMM_GRID_SCORE, OTHER_S4_CHECK], nullable: false}
        physical_case_id: {type: string, min_length: 1, nullable: false}
        cost_scope: {type: string, enum: [DUAL_POL_METHOD_FRAME, TARGET_POL_INCREMENTAL, NON_DECODER], nullable: false}
        cache_status: {type: string, enum: [EXECUTED, CACHE_READ], nullable: false}
        source_computation_id: {type: string, nullable: true}
        decoder_batch_calls: {type: int64, minimum: 0, nullable: false}
        cw_decodes: {type: int64, minimum: 0, nullable: false}
        bp_iterations: {type: int64, minimum: 0, nullable: false}
        hmm_frame_candidate_evaluations: {type: int64, minimum: 0, nullable: false}
        wall_latency_ms: {type: float64, finite: true, minimum: 0.0, nullable: false}
      invariants:
        - EXECUTED_implies_source_computation_id_is_null
        - CACHE_READ_implies_source_computation_id_is_nonnull_and_all_cost_counts_zero
        - bp_iterations_equals_20_times_cw_decodes
        - cost_totals_sum_EXECUTED_unique_computation_id_only
        - logical_projection_rows_never_duplicate_computation_cost

  cached_twin_contract:
    physical_off_cases: 60
    logical_off_projections: 540
    projections_per_physical_off_case: 9
    alignment_key: [seed, cell_id, target_polarization, fixture_id]
    physical_off_key: [seed, cell_id, target_polarization]
    canonical_computation_owner_projection: B04_K1
    pairing: every_on_fixture_pairs_to_exactly_one_fixture_aligned_off_projection
    random_receipt: same_bits_fade_phase_and_noise
    cost_rule: nine_off_rows_reference_one_B1_off_computation_and_charge_it_once

  uncertainty:
    common:
      method: seed_cluster_bootstrap_percentile
      replicates: 10000
      rng_algorithm: numpy_PCG64
      rng_seed: 2026081001
      rng_scope: reinitialize_an_independent_generator_per_stratum
      percentile: [2.5, 97.5]
      numpy_percentile_method: linear
    S1:
      gate_uses_ci: false
      point: event_trajectories_divided_by_all_observed_trajectories
      observed_seed_block_size: 24
      resample_block_count: actual_unique_seed_count
      allowed_actual_unique_seed_counts: [20, 50]
      first_stage: sample_20_blocks_with_replacement_size_20
      escalated: sample_all_50_blocks_with_replacement_size_50
    S2:
      resample_block_count: 10
      seed_block_contains: 3_cells_x_2_target_polarizations_x_9_on_fixtures_x_fixture_aligned_off
      recompute_order: pooled_affected_cw_counts_per_cell_then_cell_estimand_then_equal_three_cell_macro
      invalid_replicates_and_valid_only_ci: inherit_statistics_zero_denominator
    S3_TEST:
      resample_block_count: 10
      seed_block_contains: 3_cells_x_2_target_polarizations_x_9_cases
      recompute_order: per_case_then_per_cell_mean_then_equal_three_cell_macro
      invalid_replicates: none

  s3_estimands:
    deterministic_candidate_order_for_exact_score_ties: [NOOP, B04_K1, B04_K2, B04_K3, B08_K1, B08_K2, B08_K3, B12_K1, B12_K2, B12_K3]
    rank_direction: descending_score_rank_one_is_best
    per_case:
      pilot_rank_truth: rank_of_truth_candidate_by_pilot_score
      fused_score: pilot_score_plus_lambda_frozen_times_decoder_score
      fused_rank_truth: rank_of_truth_candidate_by_fused_score
      pilot_rr: one_divided_by_pilot_rank_truth
      fused_rr: one_divided_by_fused_rank_truth
      pilot_top1: indicator_pilot_rank_truth_equals_one
      fused_top1: indicator_fused_rank_truth_equals_one
      paired_rr_delta: fused_rr_minus_pilot_rr
    per_cell:
      cases: 10_seeds_x_2_polarizations_x_9_fixtures_equals_180
      fused_top1: arithmetic_mean_of_180_per_case_fused_top1
      pilot_mrr: arithmetic_mean_of_180_per_case_pilot_rr
      fused_mrr: arithmetic_mean_of_180_per_case_fused_rr
      paired_rr_delta: arithmetic_mean_of_180_per_case_paired_rr_delta
    macro:
      fused_top1: equal_mean_of_hard_mid_clean_cell_points
      paired_rr_delta: equal_mean_of_hard_mid_clean_cell_points
    dev_lambda_selection:
      input: S3_CANDIDATE_DEV_only
      evaluate_all_lambda_grid_values: true
      lexicographic: [maximize_macro_fused_MRR, maximize_macro_fused_top1, choose_smaller_lambda]
      output: exactly_one_s3_lambda_freeze_record_before_test
    test_gate_inputs:
      absolute: [macro_fused_top1_point, macro_fused_top1_seed_cluster_CI]
      incremental: [macro_paired_rr_delta_point, macro_paired_rr_delta_seed_cluster_CI, positive_cell_points]

  dev_exposure_and_cost:
    common_bps_freeze:
      seeds: 10
      cells: 12
      legal_waveform_tuples: 5
      bps_grid_pairs: 6
      unique_dual_pol_waveform_realizations: 600
      B1_dual_pol_method_frames: 3600
      per_frame_cost: {decoder_batch_calls: 8, cw_decodes: 128, bp_iterations: 2560}
      totals: {decoder_batch_calls: 28800, cw_decodes: 460800, bp_iterations: 9216000}
    b2_freeze:
      per_tuple_clean_dual_pol_frames: 120
      per_tuple_controlled_dual_pol_frames: 2160
      per_tuple_total_dual_pol_frames: 2280
      legal_tuple_count: 5
      B2_dual_pol_method_frames: 11400
      ps_grid_size: 122
      sigma_e2_grid_size: 6
      statistic_pairs_per_tuple: 732
      hmm_frame_candidate_evaluations: 8344800
      per_frame_decode_cost: {decoder_batch_calls: 2, cw_decodes: 32, bp_iterations: 640}
      totals: {decoder_batch_calls: 22800, cw_decodes: 364800, bp_iterations: 7296000}

  expected_cardinality_and_cost:
    S1_first_stage:
      physical_dual_pol_frames: 240
      logical_polarization_trajectories: 480
      raw_s1_rows: 480
      decoder_cost: {decoder_batch_calls: 0, cw_decodes: 0, bp_iterations: 0}
    S1_maximum:
      physical_dual_pol_frames: 600
      logical_polarization_trajectories: 1200
      raw_s1_rows: 1200
      decoder_cost: {decoder_batch_calls: 0, cw_decodes: 0, bp_iterations: 0}
    S2:
      physical_on_cases: 540
      physical_off_cases: 60
      logical_on_cases: 540
      logical_off_projections: 540
      raw_method_rows: 2160
      unique_method_computations: 1680
      B1: {method_frames: 600, decoder_batch_calls: 4800, cw_decodes: 76800, bp_iterations: 1536000}
      B2: {method_frames: 540, decoder_batch_calls: 1080, cw_decodes: 17280, bp_iterations: 345600}
      O1: {method_frames: 540, decoder_batch_calls: 1080, cw_decodes: 17280, bp_iterations: 345600}
      total: {decoder_batch_calls: 6960, cw_decodes: 111360, bp_iterations: 2227200}
    S3_DEV:
      physical_cases: 540
      truth_cases: 540
      raw_candidate_rows: 5400
      per_case_target_pol_incremental: {decoder_batch_calls: 10, cw_decodes: 88, bp_iterations: 1760, cached_unchanged_cw_nll_reads: 72}
      total_incremental: {decoder_batch_calls: 5400, cw_decodes: 47520, bp_iterations: 950400, cached_unchanged_cw_nll_reads: 38880}
    S3_TEST:
      physical_cases: 540
      truth_cases: 540
      raw_candidate_rows: 5400
      per_case_target_pol_incremental: {decoder_batch_calls: 10, cw_decodes: 88, bp_iterations: 1760, cached_unchanged_cw_nll_reads: 72}
      total_incremental: {decoder_batch_calls: 5400, cw_decodes: 47520, bp_iterations: 950400, cached_unchanged_cw_nll_reads: 38880}
    S4:
      physical_dual_pol_frames: 30
      logical_polarization_trajectories: 60
      raw_check_rows: 7
      decoder_cost: sum_actual_EXECUTED_computation_ledger_rows_no_invented_prefixed_total
    pre_S4_decoder_total:
      includes: [common_bps_freeze, b2_freeze, S2, S3_DEV, S3_TEST]
      decoder_batch_calls: 69360
      cw_decodes: 1032000
      bp_iterations: 20640000
      excludes: [S4_actual, common_CPR_nondecoder_work, HMM_nondecoder_work, cache_reads]

  artifact_contract:
    required_files: [raw_s1.jsonl, raw_s2.jsonl, raw_s3_dev.jsonl, s3_lambda_freeze.json, raw_s3_test.jsonl, raw_s4.jsonl, computation_ledger.jsonl, summary.json, receipt.json]
    validate_before_write: [strict_schema, primary_key_unique, foreign_keys, exact_cardinality, complete_seed_manifest, finite_values, raw_to_summary_recompute]
    write_protocol: same_directory_temp_then_flush_fsync_os_replace_then_directory_fsync
    receipt_hashes: [contract_sha256, source_bundle_sha256, code_bundle_sha256, freeze_sha256, seed_manifest_sha256, each_raw_file_sha256, summary_sha256, computation_ledger_sha256]
```

### 3.1 口径说明

- `s2_method` 是统计投影表，不是成本表。九个 off rows 允许引用同一 `computation_id`；成本只从 `computation_ledger` 的唯一 `EXECUTED` 行求和。
- S2 的 full-dual-pol method-frame 成本固定：B1 为 `4 rotations×2 pol×16 CW=128 CW`；B2/O1 各为 `2 pol×16 CW=32 CW`。这与 B2 owner 的 `calls_per_method_frame=2` 一致。
- S3 的 88 是 **target-pol incremental**：`16(NOOP)+3×(12+8+4)=88`。每个 changed candidate 都是一次 empty-state full restart；`72=3×(4+8+12)` 个 unchanged-CW NLL 只读 cache，不计新 CW decode。
- S4 owner 只冻结“60 trajectories + ledger complete”，没有冻结七项 check 的统一 decoder 执行图。为避免凭空增加科学数字，修复要求从 executed ledger 唯一复算实际 S4 cost，而不伪造预定 CW 总数。

## 4. raw -> summary 唯一复算

### 4.1 S1

```text
event_i = 1[persistent_transition_count_i > 0]
point_rate = sum(event_i) / (observed_seed_count * 12 cells * 2 pol)
```

- first-stage 完整 raw 必须是 `20×12×2=480` rows；若三个直接计数 gate 已满足则不升级，bootstrap 从 20 个 seed blocks 有放回抽 20。
- 若升级，完整 raw 必须是 `50×12×2=1200` rows；bootstrap 从全部 50 个 blocks 有放回抽 50。
- 每 replicate 重算 pooled trajectory rate；CI 只 descriptive，不进入 `12 AND 4 AND 2` gate。

### 4.2 S2

对每个 cell，先在 fixture-aligned rows 内 pooled affected-CW counts：

```text
damage_c  = E(B1_on)/T(B1_on) - E(B1_off)/T(B1_off)
recovery_c= [E(B1_on)-E(O1_on)] / E(B1_on)
coverage_c= [E(B1_on)-E(B2_on)] / [E(B1_on)-E(O1_on)]
macro     = (metric_hard + metric_mid + metric_clean) / 3
```

- off 的 error/count 可以按九个 fixture 对齐投影进入 pooled estimand，但其 B1 decoder 计算只发生一次；“统计权重复制”与“物理成本复制”严格分离。
- bootstrap 每次抽 10 个 seed blocks；一个 block 同时带入三 cells、双 target-pol、九 on rows、九 aligned off projections及 B1/B2/O1 method rows。
- zero denominator、invalid fraction、valid-only CI、unclipped coverage 均继承现 owner；percentile 只补 `method=linear`。

### 4.3 S3

一个 split 的 case key 为 `seed×cell×target_pol×fixture_id`，恰好 `10×3×2×9=540`。每 case 必须有十个 candidate score rows。

1. dev 对每个 lambda 由 raw `pilot_score/decoder_score` 重算 fused score，按冻结 tie-break 排名；逐 case 算 RR/top1；逐 cell 对 180 cases 取均值；三 cell 等权。按 `macro MRR -> macro top1 -> smaller lambda` 冻结唯一 lambda。
2. test 只读该 lambda。每 case 同法得到 `fused_top1` 与 paired `fused_rr-pilot_rr`；逐 cell 求均值；三 cell 等权得到两项 macro point。
3. test bootstrap 以 seed 为 block，有放回抽 10 个 blocks；每个 block携带 54 cases。每 replicate 重新执行 case→cell→macro；`np.percentile(..., method="linear")` 给 2.5/97.5%。
4. absolute gate 只读 macro fused-top1 point/lower CI；incremental gate 只读 macro paired-RR-delta point/lower CI和三个 cell point 中正值个数。不得把 5,400 candidate rows当独立样本。

## 5. 数量复算

| Scope | 物理实现 / logical | raw rows / computations | decoder cost |
|---|---:|---:|---:|
| S1 first/max | `240/600` dual-pol frames；`480/1200` pol trajectories | `480/1200` S1 rows | 0（event detection 在 common CPR truth evaluator） |
| S2 on/off | `540 on + 60 off physical`；`540 on + 540 aligned off logical` | `2160 method rows`；`1680 unique method computations` | `6,960 calls / 111,360 CW / 2,227,200 BP iter` |
| S3 dev | `540 cases` | `5,400 candidate rows/computations` | `5,400 calls / 47,520 CW / 950,400 BP iter` |
| S3 test | `540 cases` | `5,400 candidate rows/computations` | `5,400 calls / 47,520 CW / 950,400 BP iter` |
| S4 | `30` dual-pol frames=`60` trajectories | `7` check rows + actual computation ledger | owner 无固定 decoder graph；从 ledger 唯一求和 |
| common BPS dev | `600` unique tuple-waveform realizations；`3,600` B1 method frames | `3,600` executed computations | `28,800 calls / 460,800 CW / 9,216,000 BP iter` |
| B2 dev | `11,400` dual-pol method frames | `11,400` decode computations；`8,344,800` HMM frame-pair scores | `22,800 calls / 364,800 CW / 7,296,000 BP iter` |
| pre-S4 total | 不含 S1/S4、CPR与HMM非decoder工作 | — | **`69,360 calls / 1,032,000 CW / 20,640,000 BP iter`** |

算式 spot-check：

- S2 rows：`540×3 on methods + 540×1 off method = 2,160`；computations=`540×3 + 60×1 = 1,680`。
- S2 CW：`600×128(B1) + 540×32(B2) + 540×32(O1) = 111,360`。
- S3：每 split `540×[16+3×(12+8+4)] = 47,520 CW`；dev+test=`95,040 CW`。
- BPS dev：`10×12×5×6=3,600 method frames`；每 frame `4×2×16=128 CW`。
- B2 dev：每 tuple `10×12×[1 clean +2 pol×9 fixtures]=2,280`；五 tuples=`11,400 frames`；`122×6×2,280×5=8,344,800` HMM frame-pair evaluations。
- BP iteration 一律 `CW decodes×20`；cache read 和 logical projection 均乘 0。

## 6. 静态 verifier 断言清单

### B1 / schema

1. `statistical_contract_repair.schema_version`、`supersedes`、四 raw tables、lambda freeze与 computation ledger 全部存在；schema validator `strict/extra-forbid/allow_nan=false`。
2. 四 raw tables 各自 composite PK 无重复；不同 row type 不共享“全字段 nullable”的联合结构。
3. exact row sets：S1=`480 or 1200`；S2=`2160`；S3 dev/test各=`5400`；S4 check IDs=`7/7`。
4. S1 无 boundary/rotation/jump/method 字段；S4 无 seed/cell/fixture 字段；S2/S3 controlled 字段全部 non-null。
5. fixture↔boundary/rotation 双射；S2 on methods恰为 B1/B2/O1，off恰为 B1；S3每 case恰十候选且 truth=fixture。
6. raw score、latency均 finite；JSON 无 NaN/Inf；count非负且 errors≤total。

### B2 / cache 与 S2 estimand

7. `60` unique off physical keys、`540` off projections；每 physical key恰九 fixture、同一 computation ID、同一 random receipt。
8. 每个 on key恰有一个 aligned off key；natural rows计数为0；跨 stratum或跨 cell pooling立即 fail。
9. computation ledger 中 B1-off `EXECUTED` 恰60，off projections不得产生额外 decoder cost；按 logical rows求和成本的实现必须 fail test。
10. handcrafted unequal-denominator fixture同时证明“pooled counts per cell→equal-cell macro”，并拒绝 mean-of-ratios / pooled-all-cells。
11. S2 `10,000` blocks、PCG64 seed、independent stratum generator、`method=linear`、9,500/500边界、双 zero-denominator terminal与unclipped coverage均 exact。

### B3 / S1、S3 与 cost

12. S1 first/max 各用实际20/50 block；尝试抽10或仅抽新增30必须 fail；CI不得参与 occurrence gate。
13. lambda freeze只绑定 dev rows SHA，`test_rows_read_during_selection=false`；test所有 summary绑定同一 freeze SHA。
14. 手算十候选 tie case验证 rank顺序；从 raw score重新得到每 case RR/top1，不信任缓存的派生字段。
15. 每 cell恰180 cases，macro恰三 cell等权；bootstrap每 seed block恰54 cases。把5,400 candidate rows当 cluster、把pol当cluster或全cell pooling均 fail。
16. S3 dev/test各 `540×88=47,520 CW`、`×20=950,400 BP`；每 case changed CW向量为 `[16,12,12,12,8,8,8,4,4,4]`，sum=88；cached unchanged reads=72且decode cost=0。
17. computation ledger PK唯一；`CACHE_READ` cost全0且source非空；`EXECUTED` source为null；所有 phase BP=`20×CW`。S2、dev、test与pre-S4 totals逐项 exact。
18. S4 七 check全 PASS 且 `diagnostic_cost_ledger_complete` 能从 raw ledger重算；缺 computation、孤儿引用或重复 charge 均 fail closed。

### artifact / final gate

19. raw→summary fresh recompute byte/value一致；receipt所有 owner/source/code/freeze/seed/raw/summary/ledger SHA存在且匹配。
20. 写入为同目录 temp→flush/fsync→`os.replace`→directory fsync；注入写失败后旧 artifact保持完整。
21. 四 strata与七 scientific conjunct仍逐项存在，任一 missing/NA/FAIL均不得 PASS；本修复不出现新 threshold、seed或 best-of path。

## 7. Verdict

```text
VERDICT = MINIMAL_REPAIR_READY
SCIENTIFIC_CONTRACT_REOPEN_REQUIRED = NO
BUDGET_BLOCKER = NO_EVIDENCE
CURRENT_OWNER_EXECUTABLE_BEFORE_PATCH_AND_FRESH_VERIFY = NO
```

理由：三项 blocker 均可用上述 additive schema/estimand/cost closure 消除；没有必要改 population、seed、threshold、gate、预算或引入 test-time best-of。`MINIMAL_REPAIR_READY` 只表示补丁设计可直接写回 owner；owner 实际写回、YAML parse、静态断言与 fresh verifier 接收仍是 D0 开跑前置。

## 8. Protection receipt

- 启动 owner SHA256：D0 YAML=`32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936`；step-096=`32218B9CF0C9284362D3B6EFC438DBB23067B7E592E59CDB0FF1A1538E60B107`。
- protected p05 SHA256：`7843B048...4F11` / `735E4650...38B` / `C76887C6...34D` / `95A1D184...21DE`。
- 唯一写入：`projects/thesis-fso/worker-logs/step-097-d0-stat-contract-repair-design.md`。
- 未修改 owner、治理、源码、测试、结果或 p05；未运行 import/pytest/D0/仿真/web/search/download；未 commit/push。
