from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import math
import sys
import time
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest
import numpy as np


D0_ROOT = Path(__file__).resolve().parents[1] / "explore" / "coded-decoder-feedback"
sys.path.insert(0, str(D0_ROOT))
OWNER_PATH = (Path(__file__).resolve().parents[3] / "projects" / "thesis-fso"
              / "coded-decoder-feedback-groundwork" / "d0-defect-smoke-contract.yaml")

H1 = "1" * 64
H2 = "2" * 64
H3 = "3" * 64
FIXTURES = (
    "B04_K1", "B04_K2", "B04_K3",
    "B08_K1", "B08_K2", "B08_K3",
    "B12_K1", "B12_K2", "B12_K3",
)
CANDIDATES = ("NOOP",) + FIXTURES
S4_KINDS = (
    "no_slip_noiseless_B0_B1_O1_identity",
    "all_rotation_boundary_noiseless_O1_zero_error",
    "mapping_rotation_truth_metamorphic_pass",
    "candidate_isolation_and_empty_decoder_state_pass",
    "all_scores_finite_and_deterministic",
    "no_truth_field_reaches_receiver_view",
    "diagnostic_cost_ledger_complete",
)


def _api():
    import schemas
    return schemas


def _stats():
    path = D0_ROOT / "statistics.py"
    module_name = "coded_decoder_feedback_d0_statistics"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load D0 statistics module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _s1_rows(*, seed_count=20, event_keys=((8100, "cell00", "X"),
                                            (8101, "cell00", "Y"))):
    api = _api()
    rows = []
    event_keys = set(event_keys)
    for seed in range(8100, 8100 + seed_count):
        for cell_index in range(12):
            cell = f"cell{cell_index:02d}"
            for polarization in ("X", "Y"):
                event = (seed, cell, polarization) in event_keys
                rows.append(api.row_from_mapping("s1_trajectory", {
                    "record_type": "S1_TRAJECTORY", "seed": seed,
                    "cell_id": cell, "target_polarization": polarization,
                    "persistent_transition_count": int(event),
                    "persistent_transition_after_symbol": [1536] if event else [],
                    "event_present": event,
                    "trajectory_receipt_sha256": H1,
                }))
    return tuple(rows)


def test_s1_coverage_event():
    stats = _stats()
    point = stats.reduce_s1(_s1_rows())
    assert dataclasses.is_dataclass(point)
    assert point.event_count == 2
    assert point.trajectory_count == 480
    assert point.event_rate == pytest.approx(1 / 240)
    assert point.seed_count == 20
    assert point.cell_count == 12


def _s2_rows():
    api = _api()
    error_by_cell_method_prefix = {
        "hard": {
            api.S2_METHODS[0]: {4: 9, 8: 6, 12: 3},
            api.S2_METHODS[1]: {4: 5, 8: 4, 12: 1},
            api.S2_METHODS[2]: {4: 3, 8: 2, 12: 1},
            "off": {4: 3, 8: 2, 12: 1},
        },
        "mid": {
            api.S2_METHODS[0]: {4: 6, 8: 4, 12: 2},
            api.S2_METHODS[1]: {4: 5, 8: 3, 12: 1},
            api.S2_METHODS[2]: {4: 3, 8: 2, 12: 1},
            "off": {4: 0, 8: 0, 12: 0},
        },
        "clean": {
            api.S2_METHODS[0]: {4: 3, 8: 2, 12: 1},
            api.S2_METHODS[1]: {4: 0, 8: 0, 12: 0},
            api.S2_METHODS[2]: {4: 0, 8: 0, 12: 0},
            "off": {4: 0, 8: 0, 12: 0},
        },
    }
    rows = []
    for seed in range(8150, 8160):
        for cell in ("hard", "mid", "clean"):
            for polarization in ("X", "Y"):
                off_owner = f"off-{seed}-{cell}-{polarization}"
                for fixture in FIXTURES:
                    boundary = int(fixture[1:3])
                    total = 16 - boundary
                    for method in api.S2_METHODS:
                        rows.append(api.row_from_mapping("s2_method", {
                            "record_type": "S2_METHOD", "seed": seed,
                            "cell_id": cell, "target_polarization": polarization,
                            "fixture_id": fixture, "boundary_after_cw": boundary,
                            "rotation_k": int(fixture[-1]), "jump_present": True,
                            "projection_role": "DIRECT_ON",
                            "physical_case_id": f"on-{seed}-{cell}-{polarization}-{fixture}",
                            "computation_id": f"on-{seed}-{cell}-{polarization}-{fixture}-{method}",
                            "method_id": method,
                            "affected_cw_errors": error_by_cell_method_prefix[cell][method][boundary],
                            "affected_cw_total": total, "information_bit_errors": 0,
                            "information_bit_total": 16384,
                            "total_transmitted_symbols_per_polarization": 6240,
                            "result_receipt_sha256": H1,
                        }))
                    rows.append(api.row_from_mapping("s2_method", {
                        "record_type": "S2_METHOD", "seed": seed,
                        "cell_id": cell, "target_polarization": polarization,
                        "fixture_id": fixture, "boundary_after_cw": boundary,
                        "rotation_k": int(fixture[-1]), "jump_present": False,
                        "projection_role": "CACHED_OFF_PROJECTION",
                        "physical_case_id": off_owner, "computation_id": off_owner,
                        "method_id": api.S2_METHODS[0],
                        "affected_cw_errors": error_by_cell_method_prefix[cell]["off"][boundary],
                        "affected_cw_total": total, "information_bit_errors": 0,
                        "information_bit_total": 16384,
                        "total_transmitted_symbols_per_polarization": 6240,
                        "result_receipt_sha256": H2,
                    }))
    return tuple(rows)


def test_s2_off_projection_cell_equal_macro_goldens():
    stats = _stats()
    point = stats.reduce_s2(_s2_rows())
    assert point.damage == pytest.approx(5 / 12)
    assert point.recoverability == pytest.approx(13 / 18)
    assert point.coverage == pytest.approx(13 / 18)
    assert point.damage != pytest.approx(11 / 24)
    assert point.recoverability != pytest.approx(9 / 14)
    assert point.coverage != pytest.approx(2 / 3)
    assert point.physical_off_computations == 60
    assert point.terminals == ()
    assert [cell.cell_id for cell in point.cells] == ["hard", "mid", "clean"]
    assert [(cell.damage, cell.recoverability, cell.coverage)
            for cell in point.cells] == pytest.approx([
                (1 / 2, 2 / 3, 2 / 3),
                (1 / 2, 1 / 2, 1 / 2),
                (1 / 4, 1.0, 1.0),
            ])


def test_bootstrap_paired_pcg64_invalid_boundary_and_unclipped_ci():
    stats = _stats()
    observed = []
    stats.bootstrap_paired(tuple(range(10)), lambda draw: observed.append(list(draw)) or 1.2,
                           draws=2)
    assert observed == [
        [1, 8, 2, 9, 1, 3, 0, 8, 9, 2],
        [5, 7, 3, 1, 8, 3, 1, 2, 8, 4],
    ]

    calls = 0
    def boundary_500(_draw):
        nonlocal calls
        calls += 1
        return None if calls <= 500 else 1.2
    global_before = np.random.get_state()
    accepted = stats.bootstrap_paired(tuple(range(10)), boundary_500,
                                      invalid_terminal="UNSTABLE_HEADROOM")
    global_after = np.random.get_state()
    assert accepted.valid_replicates == 9500 and accepted.invalid_replicates == 500
    assert (accepted.lower, accepted.upper, accepted.terminal) == (1.2, 1.2, None)
    assert all(np.array_equal(left, right) if isinstance(left, np.ndarray) else left == right
               for left, right in zip(global_before, global_after))

    calls = 0
    def boundary_501(_draw):
        nonlocal calls
        calls += 1
        return None if calls <= 501 else 0.5
    rejected = stats.bootstrap_paired(tuple(range(10)), boundary_501,
                                      invalid_terminal="UNSTABLE_DAMAGE_DENOMINATOR")
    assert rejected.valid_replicates == 9499 and rejected.invalid_replicates == 501
    assert (rejected.lower, rejected.upper) == (None, None)
    assert rejected.terminal == "UNSTABLE_DAMAGE_DENOMINATOR"


def test_statistics_fresh_negatives_fail_closed():
    stats = _stats()
    api = _api()
    s1 = _s1_rows()
    s2 = _s2_rows()
    s1_mutations = [
        s1[:-1],
        (*s1[:-1], s1[0]),
        (dataclasses.replace(s1[0], seed=9999), *s1[1:]),
        (dataclasses.replace(s1[0], cell_id="extra"), *s1[1:]),
        (dataclasses.replace(s1[0], target_polarization="Y"), *s1[1:]),
        (dataclasses.replace(s1[0], event_present=not s1[0].event_present), *s1[1:]),
        (dataclasses.replace(s1[0], persistent_transition_after_symbol=()), *s1[1:]),
    ]
    s2_off_index = next(i for i, row in enumerate(s2) if not row.jump_present)
    s2_on_index = next(i for i, row in enumerate(s2) if row.jump_present)
    s2_mutations = []
    for changes in (
        {"computation_id": "split-off"},
        {"result_receipt_sha256": H3},
    ):
        changed = list(s2)
        changed[s2_off_index] = dataclasses.replace(changed[s2_off_index], **changes)
        s2_mutations.append(tuple(changed))
    changed = list(s2)
    changed[s2_on_index] = dataclasses.replace(changed[s2_on_index], method_id=api.S2_METHODS[1])
    s2_mutations.append(tuple(changed))
    changed = list(s2)
    changed[s2_off_index] = dataclasses.replace(changed[s2_off_index], method_id=api.S2_METHODS[1])
    s2_mutations.append(tuple(changed))

    assert len(s1_mutations) + len(s2_mutations) == 11
    for mutation in s1_mutations:
        with pytest.raises(api.SchemaError):
            stats.reduce_s1(mutation)
    for mutation in s2_mutations:
        with pytest.raises(api.SchemaError):
            stats.reduce_s2(mutation)


def _s3_rows(record_type="S3_CANDIDATE_TEST", *, pattern="ties"):
    api = _api()
    seed0 = 8050 if record_type == "S3_CANDIDATE_DEV" else 8160
    rows = []
    for seed in range(seed0, seed0 + 10):
        for cell in ("hard", "mid", "clean"):
            for polarization in ("X", "Y"):
                for fixture in FIXTURES:
                    for candidate in CANDIDATES:
                        pilot = decoder = 0.0
                        if pattern == "macro":
                            pilot = -10.0
                            if cell == "hard":
                                pilot = 0.0 if candidate == fixture else (1.0 if candidate == "NOOP" else -10.0)
                                decoder = 8.0 if candidate == fixture else 0.0
                            elif cell == "mid":
                                truth_first = polarization == "X"
                                if candidate == fixture:
                                    pilot = 1.0 if truth_first else 0.0
                                elif candidate == "NOOP":
                                    pilot = 0.0 if truth_first else 1.0
                            else:
                                if candidate == fixture:
                                    pilot = 1.0
                                elif candidate == "NOOP":
                                    pilot, decoder = 0.0, 8.0
                        boundary = 0 if candidate == "NOOP" else int(candidate[1:3])
                        identity = f"{record_type}:{seed}:{cell}:{polarization}:{fixture}:{candidate}"
                        rows.append(api.row_from_mapping("s3_candidate", {
                            "record_type": record_type, "seed": seed, "cell_id": cell,
                            "target_polarization": polarization, "fixture_id": fixture,
                            "truth_candidate_id": fixture, "candidate_id": candidate,
                            "pilot_score": pilot, "decoder_score": decoder,
                            "computation_id": identity,
                            "changed_cw_decodes": 16 - boundary,
                            "cached_unchanged_cw_nll_reads": boundary,
                            "result_receipt_sha256": hashlib.sha256(identity.encode()).hexdigest(),
                        }))
    return tuple(rows)


def test_s3_exact_candidates_tie_rank_and_cost_vector():
    stats = _stats()
    api = _api()
    freeze = api.row_from_mapping("s3_lambda_freeze", {
        "record_type": "S3_LAMBDA_FREEZE", "lambda_frozen": 0.25,
        "dev_rows_sha256": H1,
        "objective": "macro_MRR_then_macro_top1_then_smaller_lambda",
        "test_rows_read_during_selection": False,
        "freeze_receipt_sha256": H2,
    })
    result = stats.reduce_s3(_s3_rows(), freeze)
    case = next(item for item in result.cases
                if item.seed == 8160 and item.cell_id == "hard"
                and item.target_polarization == "X" and item.fixture_id == "B08_K2")
    assert (case.pilot_rank_truth, case.fused_rank_truth) == (6, 6)
    assert (case.pilot_rr, case.fused_rr) == pytest.approx((1 / 6, 1 / 6))
    assert (case.pilot_top1, case.fused_top1) == (0.0, 0.0)
    assert (case.changed_cw_decodes, case.cached_unchanged_cw_nll_reads) == (88, 72)
    assert result.case_count == 540 and result.candidate_row_count == 5400
    assert result.bootstrap_seed_blocks == tuple(range(8160, 8170))


def test_s3_lambda_dev_only_chronology_and_tie_break():
    stats = _stats()
    api = _api()
    freeze = stats.select_s3_lambda(
        _s3_rows("S3_CANDIDATE_DEV"),
        dev_rows_sha256=H1, freeze_receipt_sha256=H2,
    )
    assert type(freeze) is api.S3LambdaFreezeRow
    assert freeze.lambda_frozen == 0.25
    assert freeze.dev_rows_sha256 == H1
    assert freeze.freeze_receipt_sha256 == H2
    assert freeze.test_rows_read_during_selection is False


def test_s3_cell_macro_paired_delta_and_fresh_negatives():
    stats = _stats()
    api = _api()
    dev = _s3_rows("S3_CANDIDATE_DEV")
    test = _s3_rows(pattern="macro")
    freeze = stats.select_s3_lambda(dev, dev_rows_sha256=H1,
                                    freeze_receipt_sha256=H2)
    result = stats.reduce_s3(test, freeze)
    assert [cell.cell_id for cell in result.cells] == ["hard", "mid", "clean"]
    assert [cell.fused_top1 for cell in result.cells] == pytest.approx([1.0, 0.5, 0.0])
    assert [cell.paired_rr_delta for cell in result.cells] == pytest.approx([0.5, 0.0, -0.5])
    assert result.fused_top1 == pytest.approx(0.5)
    assert result.paired_rr_delta == pytest.approx(0.0)

    mutations = []
    mutations.append(test[:-1])
    mutations.append((*test[:-1], test[0]))
    for changes in (
        {"candidate_id": "UNKNOWN"},
        {"changed_cw_decodes": 15}, {"cached_unchanged_cw_nll_reads": 1},
        {"record_type": "S3_CANDIDATE_DEV"},
    ):
        mutations.append((dataclasses.replace(test[0], **changes), *test[1:]))
    mutations.append(tuple(
        dataclasses.replace(row, truth_candidate_id="UNKNOWN") if index < 10 else row
        for index, row in enumerate(test)
    ))
    mutations.append((test[0], dataclasses.replace(test[1], computation_id=test[0].computation_id), *test[2:]))
    bad_hash = dataclasses.replace(freeze, dev_rows_sha256="bad")
    bad_lambda = dataclasses.replace(freeze, lambda_frozen=0.3)
    assert len(mutations) == 8
    for rows in mutations:
        with pytest.raises(api.SchemaError):
            stats.reduce_s3(rows, freeze)
    for bad_freeze in (bad_hash, bad_lambda, object()):
        with pytest.raises(api.SchemaError):
            stats.reduce_s3(test, bad_freeze)
    with pytest.raises(api.SchemaError):
        stats.reduce_s3(dev, freeze)
    with pytest.raises(api.SchemaError):
        stats.select_s3_lambda(test, dev_rows_sha256=H1, freeze_receipt_sha256=H2)


def test_authenticated_hmm_runtime_and_full_api_surface():
    api = _api()
    expected = (
        "ResolvedMemberContent", "HmmRuntimeAggregateContent",
        "build_hmm_runtime_aggregate_content", "assert_hmm_runtime_aggregate_content",
        "build_owner_hmm_runtime_plan", "assert_owner_hmm_runtime_plan",
        "build_authenticated_full_authority", "assert_authenticated_full_authority",
    )
    assert [name for name in expected if not hasattr(api, name)] == []


def test_hmm_runtime_exact_sum_owner_golden():
    api = _api()
    manifest = "d6efb6ebf5f4ac5765c2a118f6af17dcbe1cb104a537935584df63cbcab3c1c7"
    members = tuple(
        api.ResolvedMemberContent(
            ordinal,
            hashlib.sha256(f"resolved-member-content-v1:{ordinal}".encode()).hexdigest(),
            123456789 / (2**42) if ordinal == 0 else 0.0,
        )
        for ordinal in range(10)
    )
    content = api.build_hmm_runtime_aggregate_content(
        stratum_role="CLEAN_INCLUDED",
        computation_ids_manifest_sha256=manifest,
        resolved_members=members,
    )
    assert content.normalized_nll_exact_sum_numerator_decimal == "123456789"
    assert content.normalized_nll_exact_sum_denominator_power2 == 42
    assert content.member_count == 10
    assert content.content_sha256 == (
        "9cf9e195032aea53840d164ac36c7c455cfcf997202867c0e6d38864a5b1a0c2"
    )
    api.assert_hmm_runtime_aggregate_content(content, stratum_role="CLEAN_INCLUDED")


def test_owner_hmm_plan_full_counts_and_representative_goldens():
    api = _api()
    from contract import load_owner_identity_authority
    owner = load_owner_identity_authority(OWNER_PATH)
    plan = api.build_owner_hmm_runtime_plan(owner_authority=owner)
    assert (plan.trajectory_count, plan.chunk_count) == (22800, 263520)
    assert (plan.executed_count, plan.cache_read_count) == (9600, 13200)
    assert plan.full_ledger_count_with_ordinary == 50287
    assert dict(plan.golden_roots) == {
        "clean10": "d6efb6ebf5f4ac5765c2a118f6af17dcbe1cb104a537935584df63cbcab3c1c7",
        "target90": "4721d075fea7694197385ef5d184a21da09891ec2ad1cf7d98229282e20879e9",
        "sentinel90_to_clean": "25aaaa4e27eb87cde8410a00b8a024660aada636830748411283222106594dd7",
        "M3_N100_direct_to_M2": "0e204f9bebdf4dc4664058540bbb054c0a88ef6e574f10d6b29584aff5169eef",
    }
    api.assert_owner_hmm_runtime_plan(plan, owner_authority=owner)


def _full_ordinary_runtime(api, owner):
    plan = api.build_ordinary_identity_plan(owner_authority=owner)
    zero_bits = np.zeros((16, 1024), dtype=np.uint8)
    first_bits = zero_bits.copy()
    first_bits[0, 0] = 1
    zero = api.build_decoder_hard_output_ref(zero_bits)
    first = api.build_decoder_hard_output_ref(first_bits)
    evidence = "69b9dd696310d530323e4e23dc50c4f98663f3f0c8cbc490e795717f8ed164f7"
    outputs = {}
    for binding in plan.bindings:
        values = {field.name: field.value for field in binding.consumer_primary_key.fields}
        if binding.projection == "S2_off": output = api.S2OffConsumerOutput(zero)
        elif binding.projection == "S2_on": output = api.S2OnConsumerOutput(zero)
        elif binding.projection == "S3": output = api.S3ConsumerOutput(zero, 0.0, 0.0)
        elif binding.projection == "BPS": output = api.BpsConsumerOutput(zero if values["polarization"] == "X" else first, 0, 0.0)
        elif binding.projection == "B2_clean": output = api.B2CleanConsumerOutput(zero if values["polarization"] == "X" else first)
        elif binding.projection == "B2_controlled": output = api.B2ControlledConsumerOutput(zero if values["row_polarization"] == "X" else first)
        else: output = api.S4ConsumerOutput(1, 0, True, evidence)
        outputs[binding.consumer_primary_key] = output
    return api.build_ordinary_runtime_bundle(
        plan=plan, owner_authority=owner, outputs_by_pk=outputs
    )


def test_authenticated_full_positive_actual_50287_ledger_authority(monkeypatch):
    api = _api()
    from contract import load_owner_identity_authority
    owner = load_owner_identity_authority(OWNER_PATH)
    ordinary = _full_ordinary_runtime(api, owner)
    ordinary_recompile_calls = 0

    def counted_legacy_deep_assert(*_args, **_kwargs):
        nonlocal ordinary_recompile_calls
        ordinary_recompile_calls += 1

    monkeypatch.setattr(api, "assert_ordinary_runtime_bundle", counted_legacy_deep_assert)
    hmm = api.build_owner_hmm_runtime_plan(owner_authority=owner)
    roles = {
        "clean10": "CLEAN_INCLUDED", "target90": "CONTROLLED_TARGET_INCLUDED",
        "sentinel90_to_clean": "CONTROLLED_SENTINEL_EXCLUDED",
        "M3_N100_direct_to_M2": "CLEAN_INCLUDED",
    }
    runtime = []
    for name, role in roles.items():
        count = 10 if role == "CLEAN_INCLUDED" else 90
        members = tuple(api.ResolvedMemberContent(
            ordinal, hashlib.sha256(f"{name}:{ordinal}".encode()).hexdigest(), 0.0
        ) for ordinal in range(count))
        runtime.append(api.build_hmm_runtime_aggregate_content(
            stratum_role=role,
            computation_ids_manifest_sha256=hmm.golden_roots[name],
            resolved_members=members,
        ))
    incremental_started = time.perf_counter()
    full = api.build_authenticated_full_authority(
        owner_authority=owner, ordinary_bundle=ordinary,
        hmm_runtime_contents=tuple(runtime),
    )
    assert (full.ordinary_ledger_count, full.hmm_ledger_count,
            full.total_ledger_count) == (27487, 22800, 50287)
    assert len(full.authority_sha256) == 64
    api.assert_authenticated_full_authority(full, owner_authority=owner)
    incremental_elapsed = time.perf_counter() - incremental_started
    print(f"ORDINARY_RECOMPILE_CALLS={ordinary_recompile_calls}")
    print(f"FULL_INCREMENTAL_SECONDS={incremental_elapsed:.6f}")
    print(f"FULL_AUTHORITY_SHA256={full.authority_sha256}")
    assert ordinary_recompile_calls == 0
    assert incremental_elapsed <= 30.0

    rejected = 0

    def reject_mutation(target, field, mutant):
        nonlocal rejected
        original = getattr(target, field)
        object.__setattr__(target, field, mutant)
        try:
            with pytest.raises(api.SchemaError):
                api.assert_authenticated_full_authority(full, owner_authority=owner)
            rejected += 1
        finally:
            object.__setattr__(target, field, original)

    unissued = object.__new__(type(full))
    for field in dataclasses.fields(full):
        object.__setattr__(unissued, field.name, getattr(full, field.name))
    with pytest.raises(api.SchemaError):
        api.assert_authenticated_full_authority(unissued, owner_authority=owner)
    rejected += 1

    record = ordinary.records[0]
    entry = record.entries[0]
    output_entry = next(
        candidate
        for candidate_record in ordinary.records
        for candidate in candidate_record.entries
        if candidate.projection == "S3"
    )
    aggregate = ordinary.aggregate_ledger[0]
    hard_ref = ordinary.hard_output_store[0]
    reject_mutation(record, "ordinary_consumer_provenance_manifest_sha256", "0" * 64)
    reject_mutation(entry, "ordinal", entry.ordinal + 1)
    reject_mutation(output_entry.consumer_output, "pilot_score", 1.0)
    reject_mutation(aggregate, "cache_status", "CACHE_READ")
    reject_mutation(aggregate, "content_sha256", "1" * 64)
    reject_mutation(hard_ref, "_root", "2" * 64)
    reject_mutation(ordinary, "counts", {**ordinary.counts, "records": 27486})
    reject_mutation(full, "owner_sha256", "3" * 64)
    reject_mutation(full, "total_ledger_count", 50286)
    assert rejected == 10
    print(f"FULL_MUTATIONS_REJECTED={rejected}")


@lru_cache(maxsize=1)
def _owner_contract():
    from contract import load_contract
    return load_contract(OWNER_PATH)


def _full_inputs(api):
    contract = _owner_contract()
    hmm_plan = api.HmmPreexecutionPlan(
        tuple_ids=("M2_N100", "M3_N10", "M3_N20", "M3_N100", "M3_N200"),
        p_s_indices=tuple(range(122)), sigma_e2_indices=tuple(range(6)),
        roles=("CLEAN_INCLUDED", "CONTROLLED_TARGET_INCLUDED", "CONTROLLED_SENTINEL_EXCLUDED"),
        cell_ids=tuple(cell.cell_id for cell in contract.population_manifest),
        polarizations=("X", "Y"),
        member_counts=(("CLEAN_INCLUDED", 10), ("CONTROLLED_TARGET_INCLUDED", 90),
                       ("CONTROLLED_SENTINEL_EXCLUDED", 90)),
        binding_scheme="D0_HMM_GROUP_SHA256_V1",
        member_namespace_sha256=H1, computation_namespace_sha256=H2,
    )
    computation_plan = api.ComputationPreexecutionPlan(entries=(
        api.ComputationPlanEntry("hmm-plan", "B2_DEV", "HMM_GRID_SCORE", "EXECUTED", None),
        api.ComputationPlanEntry("s4-plan", "S4", "OTHER_S4_CHECK", "EXECUTED", None),
    ))
    return contract, hmm_plan, computation_plan


def _valid_rows() -> dict[str, dict]:
    return {
        "s1_trajectory": {
            "record_type": "S1_TRAJECTORY", "seed": 8100, "cell_id": "hard",
            "target_polarization": "X", "persistent_transition_count": 1,
            "persistent_transition_after_symbol": [1536], "event_present": True,
            "trajectory_receipt_sha256": H1,
        },
        "s2_method": {
            "record_type": "S2_METHOD", "seed": 8150, "cell_id": "hard",
            "target_polarization": "X", "fixture_id": "B04_K1",
            "boundary_after_cw": 4, "rotation_k": 1, "jump_present": True,
            "projection_role": "DIRECT_ON", "physical_case_id": "pc-on",
            "computation_id": "s2-on-b1", "method_id": "GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
            "affected_cw_errors": 1, "affected_cw_total": 12,
            "information_bit_errors": 2, "information_bit_total": 16384,
            "total_transmitted_symbols_per_polarization": 6240,
            "result_receipt_sha256": H1,
        },
        "s3_candidate": {
            "record_type": "S3_CANDIDATE_TEST", "seed": 8160, "cell_id": "hard",
            "target_polarization": "X", "fixture_id": "B04_K1",
            "truth_candidate_id": "B04_K1", "candidate_id": "NOOP",
            "pilot_score": 1.0, "decoder_score": -2.0,
            "computation_id": "s3-NOOP", "changed_cw_decodes": 16,
            "cached_unchanged_cw_nll_reads": 0, "result_receipt_sha256": H1,
        },
        "s3_lambda_freeze": {
            "record_type": "S3_LAMBDA_FREEZE", "lambda_frozen": 0.5,
            "dev_rows_sha256": H1,
            "objective": "macro_MRR_then_macro_top1_then_smaller_lambda",
            "test_rows_read_during_selection": False, "freeze_receipt_sha256": H2,
        },
        "s4_check": {
            "record_type": "S4_CHECK", "check_id": S4_KINDS[0],
            "tested_instances": 1, "failed_instances": 0, "passed": True,
            "evidence_sha256": H1,
        },
        "computation_ledger": {
            "record_type": "COMPUTATION", "computation_id": "comp-1",
            "phase": "S2", "operation": "B1_DECODE", "physical_case_id": "pc-1",
            "cost_scope": "DUAL_POL_METHOD_FRAME", "cache_status": "EXECUTED",
            "source_computation_id": None, "content_sha256": H1,
            "logical_decoder_batches": 1, "logical_cw_decodes": 16,
            "logical_bp_iterations": 320, "materialized_decoder_batches": 1,
            "materialized_cw_decodes": 16, "materialized_bp_iterations": 320,
            "physical_api_invocations": 1, "api_batch_cw_count": 16,
            "hmm_dual_pol_frame_parameter_pair_scores": 0,
            "hmm_primitive_pol_trajectory_parameter_pair_scores": 0,
            "selected_pair_symbol_state_evaluations": 0, "wall_latency_ms": 1.0,
        },
        "bps_dev_score": {
            "record_type": "BPS_DEV_SCORE", "tuple_id": "M2_N100", "M": 2, "N": 100,
            "B": 32, "Nw": 31, "seed": 8000, "cell_id": "hard", "polarization": "X",
            "method_id": "GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
            "selected_global_rotation_k": 0, "selected_normalized_reencode_nll": 1.0,
            "successful_cw_count": 16, "delivered_information_bits": 16384,
            "full_frame_cw_errors": 0, "full_frame_cw_total": 16,
            "information_bit_errors": 0, "information_bit_total": 16384,
            "total_transmitted_symbols_per_polarization": 6240,
            "computation_id": "bps-1", "cache_status": "EXECUTED",
            "source_computation_id": None, "result_receipt_sha256": H1,
        },
        "b2_hmm_grid_chunk": {
            "record_type": "B2_HMM_GRID_CHUNK", "tuple_id": "M2_N100", "M": 2, "N": 100,
            "p_s_index": 0, "p_s_float64_hex": "0x0.0p+0",
            "sigma_e2_index": 0, "sigma_e2_float64_hex": "0x0.0p+0",
            "stratum_role": "CLEAN_INCLUDED", "cell_id": "hard", "polarization": "X",
            "chunk_id": "chunk-1", "pilot_count": 64, "member_count": 10,
            "member_key_manifest_sha256": H1,
            "normalized_nll_exact_sum_numerator_decimal": "1",
            "normalized_nll_exact_sum_denominator_power2": 1,
            "objective_included": True, "computation_ids_manifest_sha256": H2,
            "content_sha256": H3,
        },
        "b2_tuple_clean_dev": {
            "record_type": "B2_TUPLE_CLEAN_DEV", "tuple_id": "M2_N100",
            "seed": 8000, "cell_id": "hard", "polarization": "X",
            "bps_freeze_ref": "bps-M2_N100", "statistic_freeze_ref": "stat-M2_N100",
            "successful_cw_count": 16, "delivered_information_bits": 16384,
            "full_frame_cw_errors": 0, "information_bit_errors": 0,
            "total_transmitted_symbols_per_polarization": 6240,
            "computation_id": "b2-clean", "result_receipt_sha256": H1,
        },
        "b2_tuple_controlled_dev": {
            "record_type": "B2_TUPLE_CONTROLLED_DEV", "tuple_id": "M2_N100",
            "seed": 8000, "cell_id": "hard", "target_polarization": "X",
            "row_polarization": "X", "row_role": "TARGET_INCLUDED",
            "fixture_id": "B04_K1", "boundary_after_cw": 4, "rotation_k": 1,
            "bps_freeze_ref": "bps-M2_N100", "statistic_freeze_ref": "stat-M2_N100",
            "successful_cw_count": 15, "delivered_information_bits": 15360,
            "full_frame_cw_errors": 1, "affected_cw_errors": 1,
            "affected_cw_total": 12,
            "total_transmitted_symbols_per_polarization": 6240,
            "computation_id": "b2-control", "cache_status": "EXECUTED",
            "source_computation_id": None, "result_receipt_sha256": H1,
        },
    }


def _ledger(computation_id: str, phase: str, operation: str) -> dict:
    row = deepcopy(_valid_rows()["computation_ledger"])
    row.update(computation_id=computation_id, phase=phase, operation=operation)
    return row


def _explicit_partial_manifest(api, *, include_dev=False):
    def expectation(table, fields, keys):
        projection = api.build_identity_projection(fields=fields, expected_keys=tuple(keys))
        return api.TableExpectation(table=table, projections=(projection,))

    s2_keys = []
    ledger_ids = []
    for fixture in FIXTURES:
        for method in (
            "GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
            "OFC17_16QAM_EXTFRAME_V1",
            "TRUTH_BOUNDARY_ROTATION_CORRECTION",
        ):
            s2_keys.append(("S2_METHOD", 8150, "hard", "X", fixture, True, method))
            ledger_ids.append(f"on-{fixture}-{method}")
        s2_keys.append(("S2_METHOD", 8150, "hard", "X", fixture, False,
                        "GLOBAL_FOUR_ROTATION_DECODER_SELECTION"))
    ledger_ids.append("off-B1")

    s3_keys = []
    for split, seed in (("S3_CANDIDATE_DEV", 8050), ("S3_CANDIDATE_TEST", 8160)):
        for candidate in CANDIDATES:
            s3_keys.append((split, seed, "hard", "X", "B04_K1", candidate))
            ledger_ids.append(f"{split}-{candidate}")
    ledger_ids.extend(("b2-target", "b2-sentinel"))

    tables = [
        expectation("s1_trajectory", ("record_type", "seed", "cell_id", "target_polarization"),
                    (("S1_TRAJECTORY", 8100, "hard", "X"),)),
        expectation("s2_method", ("record_type", "seed", "cell_id", "target_polarization",
                                  "fixture_id", "jump_present", "method_id"), s2_keys),
        expectation("s3_candidate", ("record_type", "seed", "cell_id", "target_polarization",
                                     "fixture_id", "candidate_id"), s3_keys),
        expectation("b2_tuple_controlled_dev",
                    ("record_type", "tuple_id", "seed", "cell_id", "target_polarization",
                     "fixture_id", "row_polarization"),
                    (("B2_TUPLE_CONTROLLED_DEV", "M2_N100", 8000, "hard", "X", "B04_K1", "X"),
                     ("B2_TUPLE_CONTROLLED_DEV", "M2_N100", 8000, "hard", "X", "B04_K1", "Y"))),
    ]
    seed_sets = [
        api.SeedSet("S1_TRAJECTORY", (8100,)), api.SeedSet("S2_METHOD", (8150,)),
        api.SeedSet("S3_CANDIDATE_DEV", (8050,)),
        api.SeedSet("S3_CANDIDATE_TEST", (8160,)),
        api.SeedSet("B2_TUPLE_CONTROLLED_DEV", (8000,)),
    ]
    if include_dev:
        tables.extend((
            expectation("bps_dev_score",
                        ("record_type", "tuple_id", "B", "Nw", "seed", "cell_id", "polarization"),
                        (("BPS_DEV_SCORE", "M2_N100", 32, 31, 8000, "hard", "X"),)),
            expectation("b2_tuple_clean_dev",
                        ("record_type", "tuple_id", "seed", "cell_id", "polarization"),
                        (("B2_TUPLE_CLEAN_DEV", "M2_N100", 8000, "hard", "X"),)),
        ))
        seed_sets.extend((api.SeedSet("BPS_DEV_SCORE", (8000,)),
                          api.SeedSet("B2_TUPLE_CLEAN_DEV", (8000,))))
        ledger_ids.extend(("bps-1", "b2-clean", "hmm-standalone", "s4-standalone"))
    tables.append(expectation("computation_ledger", ("computation_id",),
                              ((item,) for item in ledger_ids)))
    cell_domains = (api.CellDomain("cell_id", ("hard",)),)
    seed_sets = tuple(seed_sets)
    tables = tuple(tables)
    digest = api.partial_coverage_sha256(
        cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
    )
    return api.build_partial_relational_manifest(
        cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
        coverage_sha256=digest,
    )


def _relational_dataset():
    api = _api()
    rows = _valid_rows()
    s2 = []
    ledger = []
    method_to_operation = {
        "GLOBAL_FOUR_ROTATION_DECODER_SELECTION": "B1_DECODE",
        "OFC17_16QAM_EXTFRAME_V1": "B2_DECODE",
        "TRUTH_BOUNDARY_ROTATION_CORRECTION": "O1_DECODE",
    }
    for fixture in FIXTURES:
        boundary = int(fixture[1:3])
        rotation = int(fixture[-1])
        for method, operation in method_to_operation.items():
            row = deepcopy(rows["s2_method"])
            comp = f"on-{fixture}-{method}"
            row.update(fixture_id=fixture, boundary_after_cw=boundary, rotation_k=rotation,
                       affected_cw_total=16-boundary, method_id=method,
                       physical_case_id=f"pc-on-{fixture}", computation_id=comp)
            s2.append(api.row_from_mapping("s2_method", row))
            ledger.append(api.row_from_mapping("computation_ledger", _ledger(comp, "S2", operation)))
        off = deepcopy(rows["s2_method"])
        off.update(fixture_id=fixture, boundary_after_cw=boundary, rotation_k=rotation,
                   affected_cw_total=16-boundary, jump_present=False,
                   projection_role="CACHED_OFF_PROJECTION",
                   physical_case_id="pc-off", computation_id="off-B1",
                   method_id="GLOBAL_FOUR_ROTATION_DECODER_SELECTION")
        s2.append(api.row_from_mapping("s2_method", off))
    ledger.append(api.row_from_mapping("computation_ledger", _ledger("off-B1", "S2", "B1_DECODE")))

    s3 = []
    for split, seed in (("S3_CANDIDATE_DEV", 8050), ("S3_CANDIDATE_TEST", 8160)):
        for candidate in CANDIDATES:
            row = deepcopy(rows["s3_candidate"])
            changed = 16 if candidate == "NOOP" else 16-int(candidate[1:3])
            cached = 0 if candidate == "NOOP" else int(candidate[1:3])
            comp = f"{split}-{candidate}"
            row.update(record_type=split, seed=seed, candidate_id=candidate,
                       computation_id=comp, changed_cw_decodes=changed,
                       cached_unchanged_cw_nll_reads=cached)
            s3.append(api.row_from_mapping("s3_candidate", row))
            phase = "S3_DEV" if split.endswith("DEV") else "S3_TEST"
            ledger.append(api.row_from_mapping("computation_ledger",
                                                _ledger(comp, phase, "CANDIDATE_DECODE")))

    controlled = []
    for pol, role, comp in (("X", "TARGET_INCLUDED", "b2-target"),
                            ("Y", "SENTINEL_EXCLUDED", "b2-sentinel")):
        row = deepcopy(rows["b2_tuple_controlled_dev"])
        row.update(row_polarization=pol, row_role=role, computation_id=comp)
        controlled.append(api.row_from_mapping("b2_tuple_controlled_dev", row))
        ledger.append(api.row_from_mapping("computation_ledger",
                                            _ledger(comp, "B2_DEV", "B2_DECODE")))
    manifest = _explicit_partial_manifest(api)
    return {
        "s1_trajectory": (api.row_from_mapping("s1_trajectory", rows["s1_trajectory"]),),
        "s2_method": tuple(s2),
        "s3_candidate": tuple(s3),
        "b2_tuple_controlled_dev": tuple(controlled),
        "computation_ledger": tuple(ledger),
    }, manifest


def test_raw_tables_strict_fields():
    api = _api()
    valid = _valid_rows()
    assert set(api.TABLE_MODELS) == set(valid)
    for table, mapping in valid.items():
        assert api.TABLE_FIELDS[table] == tuple(mapping)
        value = api.row_from_mapping(table, mapping)
        assert dataclasses.is_dataclass(value)
        assert value.__dataclass_params__.frozen
        assert hasattr(type(value), "__slots__")
        assert api.row_to_mapping(value) == mapping
        with pytest.raises(api.SchemaError):
            api.row_from_mapping(table, {k: v for k, v in mapping.items() if k != next(iter(mapping))})
        with pytest.raises(api.SchemaError):
            api.row_from_mapping(table, {**mapping, "unknown": 1})

    mutations = [
        ("s1_trajectory", "seed", True), ("s1_trajectory", "seed", "8100"),
        ("s2_method", "boundary_after_cw", 4.0),
        ("s3_candidate", "pilot_score", 1), ("s3_candidate", "pilot_score", math.nan),
        ("s3_candidate", "decoder_score", math.inf),
        ("s3_lambda_freeze", "lambda_frozen", "0.5"),
        ("s4_check", "tested_instances", True),
        ("computation_ledger", "wall_latency_ms", math.nan),
        ("bps_dev_score", "B", "32"),
        ("b2_hmm_grid_chunk", "member_count", 10.0),
        ("b2_tuple_clean_dev", "successful_cw_count", False),
        ("b2_tuple_controlled_dev", "affected_cw_errors", "1"),
    ]
    for table, field, bad in mutations:
        row = deepcopy(valid[table])
        row[field] = bad
        with pytest.raises(api.SchemaError):
            api.row_from_mapping(table, row)


def test_pk_fk_bijection_fail_closed():
    api = _api()
    dataset, manifest = _relational_dataset()
    api.validate_partial_relations(dataset, manifest)

    mutations = []
    duplicate = dict(dataset)
    duplicate["s1_trajectory"] += duplicate["s1_trajectory"]
    mutations.append(duplicate)

    orphan = dict(dataset)
    orphan["computation_ledger"] = orphan["computation_ledger"][1:]
    mutations.append(orphan)

    cross_cell = dict(dataset)
    cross_cell["s2_method"] = (
        dataclasses.replace(cross_cell["s2_method"][0], cell_id="other"),
        *cross_cell["s2_method"][1:],
    )
    mutations.append(cross_cell)

    cross_seed = dict(dataset)
    cross_seed["s3_candidate"] = (
        dataclasses.replace(cross_seed["s3_candidate"][0], seed=8160),
        *cross_seed["s3_candidate"][1:],
    )
    mutations.append(cross_seed)

    missing_method = dict(dataset)
    missing_method["s2_method"] = tuple(
        row for row in missing_method["s2_method"]
        if not (row.fixture_id == "B04_K1" and row.jump_present
                and row.method_id == "OFC17_16QAM_EXTFRAME_V1")
    )
    mutations.append(missing_method)

    missing_candidate = dict(dataset)
    missing_candidate["s3_candidate"] = tuple(
        row for row in missing_candidate["s3_candidate"]
        if not (row.record_type == "S3_CANDIDATE_DEV" and row.candidate_id == "B12_K3")
    )
    mutations.append(missing_candidate)

    missing_sentinel = dict(dataset)
    missing_sentinel["b2_tuple_controlled_dev"] = missing_sentinel["b2_tuple_controlled_dev"][:1]
    mutations.append(missing_sentinel)

    for mutated in mutations:
        with pytest.raises(api.SchemaError):
            api.validate_partial_relations(mutated, manifest)


def test_s4_schema_seven():
    api = _api()
    rows = tuple(
        api.row_from_mapping("s4_check", {
            "record_type": "S4_CHECK", "check_id": kind, "tested_instances": 1,
            "failed_instances": 0, "passed": True,
            "evidence_sha256": f"{index + 1:x}" * 64,
        })
        for index, kind in enumerate(S4_KINDS)
    )
    artifact = api.S4Artifact(contract_sha256=H1, receipt_sha256=H2, entries=rows)
    assert dataclasses.is_dataclass(artifact) and artifact.__dataclass_params__.frozen
    assert hasattr(type(artifact), "__slots__")
    known = frozenset(row.evidence_sha256 for row in rows)
    api.validate_s4_schema(
        artifact, expected_contract_sha256=H1,
        expected_receipt_sha256=H2, evidence_sha256s=known,
    )

    invalid_artifacts = [
        dataclasses.replace(artifact, entries=rows[:6]),
        dataclasses.replace(artifact, entries=rows + (rows[0],)),
        dataclasses.replace(artifact, entries=rows[:-1] + (dataclasses.replace(rows[-1], check_id="unknown"),)),
        dataclasses.replace(artifact, entries=(rows[1], rows[0], *rows[2:])),
        dataclasses.replace(artifact, contract_sha256=H3),
        dataclasses.replace(artifact, receipt_sha256=H3),
    ]
    for invalid in invalid_artifacts:
        with pytest.raises(api.SchemaError):
            api.validate_s4_schema(
                invalid, expected_contract_sha256=H1,
                expected_receipt_sha256=H2, evidence_sha256s=known,
            )
    with pytest.raises(api.SchemaError):
        api.validate_s4_schema(
            artifact, expected_contract_sha256=H1,
            expected_receipt_sha256=H2, evidence_sha256s=frozenset(set(known) - {rows[0].evidence_sha256}),
        )


def test_tuple_overhead_identities_fail_closed():
    api = _api()
    bases = _valid_rows()
    cases = (
        ("M3_N10", 3, 10, 684, 6860),
        ("M3_N20", 3, 20, 325, 6501),
        ("M2_N100", 2, 100, 64, 6240),
        ("M3_N200", 3, 200, 32, 6208),
    )
    for index, (tuple_id, m_value, n_value, pilot_count, total) in enumerate(cases):
        rows = {
            "bps_dev_score": {
                **bases["bps_dev_score"], "tuple_id": tuple_id,
                "M": m_value, "N": n_value,
                "total_transmitted_symbols_per_polarization": total,
            },
            "b2_hmm_grid_chunk": {
                **bases["b2_hmm_grid_chunk"], "tuple_id": tuple_id,
                "M": m_value, "N": n_value, "pilot_count": pilot_count,
            },
            "b2_tuple_clean_dev": {
                **bases["b2_tuple_clean_dev"], "tuple_id": tuple_id,
                "total_transmitted_symbols_per_polarization": total,
            },
            "b2_tuple_controlled_dev": {
                **bases["b2_tuple_controlled_dev"], "tuple_id": tuple_id,
                "total_transmitted_symbols_per_polarization": total,
            },
        }
        for table, mapping in rows.items():
            api.row_from_mapping(table, mapping)
            field = ("pilot_count" if table == "b2_hmm_grid_chunk"
                     else "total_transmitted_symbols_per_polarization")
            wrong = cases[(index + 1) % len(cases)][3 if field == "pilot_count" else 4]
            with pytest.raises(api.SchemaError):
                api.row_from_mapping(table, {**mapping, field: wrong})


def test_ledger_bidirectional_binding_fail_closed():
    api = _api()
    dataset, manifest = _relational_dataset()
    base = dict(dataset)
    rows = _valid_rows()

    bps = api.row_from_mapping("bps_dev_score", rows["bps_dev_score"])
    clean = api.row_from_mapping("b2_tuple_clean_dev", rows["b2_tuple_clean_dev"])
    additions = (
        api.row_from_mapping("computation_ledger", _ledger("bps-1", "BPS_DEV", "B1_DECODE")),
        api.row_from_mapping("computation_ledger", _ledger("b2-clean", "B2_DEV", "B2_DECODE")),
        api.row_from_mapping("computation_ledger", _ledger("hmm-standalone", "B2_DEV", "HMM_GRID_SCORE")),
        api.row_from_mapping("computation_ledger", _ledger("s4-standalone", "S4", "OTHER_S4_CHECK")),
    )
    base["bps_dev_score"] = (bps,)
    base["b2_tuple_clean_dev"] = (clean,)
    base["computation_ledger"] += additions
    manifest = _explicit_partial_manifest(api, include_dev=True)

    off = tuple(row for row in base["s2_method"] if not row.jump_present)
    assert len(off) == 9 and len({row.computation_id for row in off}) == 1
    api.validate_partial_relations(base, manifest)

    def ledger_change(bundle, computation_id, **changes):
        mutated = dict(bundle)
        mutated["computation_ledger"] = tuple(
            dataclasses.replace(row, **changes) if row.computation_id == computation_id else row
            for row in bundle["computation_ledger"]
        )
        return mutated

    cache_valid = dict(base)
    cache_valid["b2_tuple_controlled_dev"] = tuple(
        dataclasses.replace(row, cache_status="CACHE_READ", source_computation_id="b2-target")
        if row.computation_id == "b2-sentinel" else row
        for row in base["b2_tuple_controlled_dev"]
    )
    cache_valid = ledger_change(
        cache_valid, "b2-sentinel", cache_status="CACHE_READ",
        source_computation_id="b2-target", materialized_decoder_batches=0,
        materialized_cw_decodes=0, materialized_bp_iterations=0,
        physical_api_invocations=0, selected_pair_symbol_state_evaluations=0,
    )
    api.validate_partial_relations(cache_valid, manifest)

    mutations = []
    extra = dict(base)
    extra["computation_ledger"] += (
        api.row_from_mapping("computation_ledger", _ledger("orphan-s2-extra", "S2", "B1_DECODE")),
    )
    mutations.append(extra)

    for table, computation_id in (("b2_tuple_controlled_dev", "b2-target"),
                                  ("bps_dev_score", "bps-1")):
        mismatch = dict(base)
        mismatch[table] = tuple(
            dataclasses.replace(row, cache_status="CACHE_READ", source_computation_id="ghost-source")
            if row.computation_id == computation_id else row for row in base[table]
        )
        mutations.append(mismatch)

    ghost = dict(cache_valid)
    ghost["b2_tuple_controlled_dev"] = tuple(
        dataclasses.replace(row, source_computation_id="ghost-source")
        if row.computation_id == "b2-sentinel" else row
        for row in cache_valid["b2_tuple_controlled_dev"]
    )
    ghost = ledger_change(ghost, "b2-sentinel", source_computation_id="ghost-source")
    mutations.append(ghost)
    mutations.append(ledger_change(cache_valid, "b2-sentinel", content_sha256=H2))

    s2_first = base["s2_method"][0]
    s3_first = base["s3_candidate"][0]
    mutations.extend((
        ledger_change(base, s2_first.computation_id, operation="O1_DECODE"),
        ledger_change(base, s3_first.computation_id, phase="S2"),
        ledger_change(base, "bps-1", operation="B2_DECODE"),
        ledger_change(base, "b2-target", phase="S2"),
        ledger_change(base, "b2-clean", operation="B1_DECODE"),
    ))

    incompatible = dict(base)
    incompatible["s3_candidate"] = (
        dataclasses.replace(s3_first, computation_id="off-B1"),
        *base["s3_candidate"][1:],
    )
    incompatible["computation_ledger"] = tuple(
        row for row in base["computation_ledger"]
        if row.computation_id != s3_first.computation_id
    )
    mutations.append(incompatible)

    assert len(mutations) == 11
    for mutated in mutations:
        with pytest.raises(api.SchemaError):
            api.validate_partial_relations(mutated, manifest)


def test_partial_manifest_exact_coverage_fail_closed():
    api = _api()
    dataset, manifest = _relational_dataset()
    api.validate_partial_relations(dataset, manifest)

    with pytest.raises(api.SchemaError):
        api.build_partial_relational_manifest(
            cell_domains=(api.CellDomain("cell_id", ("hard",)),),
            seed_sets=(api.SeedSet("S1_TRAJECTORY", (8100,)),),
            tables=(), coverage_sha256=H1,
        )
    with pytest.raises(api.SchemaError):
        api.TableExpectation(table="s1_trajectory", projections=())
    with pytest.raises(api.SchemaError):
        api.build_identity_projection(
            fields=("seed",), expected_keys=dataset["s1_trajectory"],
        )

    count_only_projection = api.IdentityProjection(
        fields=("record_type", "seed", "cell_id", "target_polarization"),
        expected_key_count=1, expected_keys_sha256=H1,
        multiplicity_by_key_sha256=H2,
    )
    count_only_tables = (
        api.TableExpectation("s1_trajectory", (count_only_projection,)),
    )
    count_only_domains = (api.CellDomain("cell_id", ("hard",)),)
    count_only_seeds = (api.SeedSet("S1_TRAJECTORY", (8100,)),)
    count_only = api.build_partial_relational_manifest(
        cell_domains=count_only_domains, seed_sets=count_only_seeds,
        tables=count_only_tables,
        coverage_sha256=api.partial_coverage_sha256(
            cell_domains=count_only_domains, seed_sets=count_only_seeds,
            tables=count_only_tables,
        ),
    )
    with pytest.raises(api.SchemaError):
        api.validate_partial_relations(
            {"s1_trajectory": dataset["s1_trajectory"]}, count_only,
        )

    mutations = [{}, dict(dataset), dict(dataset)]
    mutations[1].pop("s2_method")
    mutations[2]["s2_method"] = ()

    extra = dict(dataset)
    extra["s4_check"] = (api.row_from_mapping("s4_check", _valid_rows()["s4_check"]),)
    mutations.append(extra)

    s2_substitution = dict(dataset)
    s2_substitution["s2_method"] = tuple(
        dataclasses.replace(row, seed=8151) for row in dataset["s2_method"]
    )
    mutations.append(s2_substitution)

    s3_substitution = dict(dataset)
    s3_substitution["s3_candidate"] = tuple(
        dataclasses.replace(row, seed=8051)
        if row.record_type == "S3_CANDIDATE_DEV" else row
        for row in dataset["s3_candidate"]
    )
    mutations.append(s3_substitution)

    controlled_substitution = dict(dataset)
    controlled_substitution["b2_tuple_controlled_dev"] = tuple(
        dataclasses.replace(row, tuple_id="M3_N100")
        for row in dataset["b2_tuple_controlled_dev"]
    )
    mutations.append(controlled_substitution)

    identity_substitution = dict(dataset)
    identity_substitution["s2_method"] = (
        dataclasses.replace(dataset["s2_method"][0], target_polarization="Y"),
        *dataset["s2_method"][1:],
    )
    mutations.append(identity_substitution)

    assert len(mutations) == 8
    for mutated in mutations:
        with pytest.raises(api.SchemaError):
            api.validate_partial_relations(mutated, manifest)


def test_full_validator_rejects_partial_manifest():
    api = _api()
    dataset, manifest = _relational_dataset()
    with pytest.raises(api.SchemaError):
        api.validate_relations(dataset, manifest)


def _unsafe_clone(value, **changes):
    clone = object.__new__(type(value))
    for item in dataclasses.fields(value):
        object.__setattr__(clone, item.name, changes.get(item.name, getattr(value, item.name)))
    return clone


def test_full_manifest_factory_seal_rejects_forged_full():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    partial = api.RelationalManifest(
        api.EXPLICIT_PARTIAL,
        (api.CellDomain("population", ("hard",)),),
        (api.SeedSet("S1_TRAJECTORY", (8100,)),),
        (api.TableExpectation("s1_trajectory", (
            api.IdentityProjection(("record_type",), 1, H1, H2),
        )),),
        H3,
    )
    with pytest.raises((api.SchemaError, TypeError)):
        api.RelationalManifest(
            api.FULL_D0_ARTIFACT, partial.cell_domains, partial.seed_sets,
            partial.tables, partial.coverage_sha256,
        )
    with pytest.raises((api.SchemaError, TypeError)):
        api.FullRelationalManifest()

    canonical = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan,
        computation_preexecution_plan=computation_plan,
    )
    assert type(canonical) is api.FullRelationalManifest
    api.assert_full_manifest_authority(canonical)

    forged = object.__new__(api.FullRelationalManifest)
    for item in dataclasses.fields(canonical):
        object.__setattr__(forged, item.name, getattr(canonical, item.name))
    object.__setattr__(forged, "authority_sha256", H1)
    with pytest.raises(api.SchemaError):
        api.assert_full_manifest_authority(forged)
    with pytest.raises((api.SchemaError, TypeError)):
        dataclasses.replace(canonical, authority_sha256=H1)


def _alternate_full_inputs(api):
    contract, hmm_plan, _ = _full_inputs(api)
    hmm_plan = dataclasses.replace(
        hmm_plan, member_namespace_sha256=H2,
        computation_namespace_sha256=H3,
    )
    computation_plan = api.ComputationPreexecutionPlan(entries=(
        api.ComputationPlanEntry(
            "alternate-hmm", "B2_DEV", "HMM_GRID_SCORE", "EXECUTED", None,
        ),
        api.ComputationPlanEntry(
            "alternate-s4", "S4", "OTHER_S4_CHECK", "EXECUTED", None,
        ),
    ))
    return contract, hmm_plan, computation_plan


def test_full_manifest_cached_canonical_isolation():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    cached = api._compile_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan,
        computation_preexecution_plan=computation_plan,
    )
    original_authority = cached.authority_sha256
    original_coverage = cached.coverage_sha256
    original_count = cached.tables[0].projections[0].expected_key_count

    object.__setattr__(cached, "authority_sha256", H1)
    object.__setattr__(cached.tables[0], "table", "s2_method")
    object.__setattr__(
        cached.tables[0].projections[0], "expected_key_count", original_count + 1,
    )
    with pytest.raises(api.SchemaError):
        api.assert_full_manifest_authority(cached)

    fresh = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan,
        computation_preexecution_plan=computation_plan,
    )
    api.assert_full_manifest_authority(fresh)
    assert fresh.authority_sha256 == original_authority
    assert fresh.coverage_sha256 == original_coverage
    assert fresh.tables[0].table == "s1_trajectory"
    assert fresh.tables[0].projections[0].expected_key_count == original_count
    assert fresh is not cached
    assert fresh.spec is not cached.spec
    assert fresh.tables[0] is not cached.tables[0]
    assert fresh.tables[0].projections[0] is not cached.tables[0].projections[0]


def test_full_manifest_recompile_uses_fresh_authority_graph():
    api = _api()
    input_sets = (
        (*_full_inputs(api), "FIRST_STAGE"),
        (*_full_inputs(api), "MAXIMUM"),
        (*_alternate_full_inputs(api), "FIRST_STAGE"),
    )
    isolation_cases = 0
    for contract, hmm_plan, computation_plan, extent in input_sets:
        left = api._compile_full_relational_manifest(
            owner_contract=contract, s1_extent=extent,
            hmm_preexecution_plan=hmm_plan,
            computation_preexecution_plan=computation_plan,
        )
        right = api._compile_full_relational_manifest(
            owner_contract=contract, s1_extent=extent,
            hmm_preexecution_plan=hmm_plan,
            computation_preexecution_plan=computation_plan,
        )
        api.assert_full_manifest_authority(left)
        api.assert_full_manifest_authority(right)
        pairs = [
            (left, right),
            (left.spec, right.spec),
            (left.spec.owner_contract, right.spec.owner_contract),
            (left.spec.hmm_preexecution_plan, right.spec.hmm_preexecution_plan),
            (left.spec.computation_preexecution_plan,
             right.spec.computation_preexecution_plan),
            *zip(left.cell_domains, right.cell_domains),
            *zip(left.seed_sets, right.seed_sets),
            *zip(left.tables, right.tables),
            *(
                (left_projection, right_projection)
                for left_table, right_table in zip(left.tables, right.tables)
                for left_projection, right_projection in zip(
                    left_table.projections, right_table.projections,
                )
            ),
        ]
        assert all(left_value is not right_value for left_value, right_value in pairs)
        isolation_cases += len(pairs)
    assert isolation_cases >= 24


def test_full_manifest_authority_recompiles_after_tamper():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    manifest = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan,
        computation_preexecution_plan=computation_plan,
    )
    maximum = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="MAXIMUM",
        hmm_preexecution_plan=hmm_plan,
        computation_preexecution_plan=computation_plan,
    )
    api.assert_full_manifest_authority(manifest)
    api.assert_full_manifest_authority(maximum)

    first_table = manifest.tables[0]
    first_projection = first_table.projections[0]
    table_mutations = []
    for index in range(len(manifest.tables)):
        table_mutations.append(_unsafe_clone(
            manifest, tables=manifest.tables[:index] + manifest.tables[index + 1:],
        ))
    table_mutations.extend((
        _unsafe_clone(manifest, tables=(manifest.tables[1], manifest.tables[0], *manifest.tables[2:])),
        _unsafe_clone(manifest, tables=manifest.tables + (manifest.tables[0],)),
        _unsafe_clone(manifest, tables=(
            _unsafe_clone(first_table, table="s2_method"), *manifest.tables[1:],
        )),
        _unsafe_clone(manifest, tables=(
            _unsafe_clone(first_table, projections=()), *manifest.tables[1:],
        )),
        _unsafe_clone(manifest, tables=(
            _unsafe_clone(first_table, projections=(
                _unsafe_clone(first_projection, expected_key_count=481),
            )), *manifest.tables[1:],
        )),
        _unsafe_clone(manifest, tables=(
            _unsafe_clone(first_table, projections=(
                _unsafe_clone(first_projection, expected_keys_sha256=H1),
            )), *manifest.tables[1:],
        )),
        _unsafe_clone(manifest, tables=(
            _unsafe_clone(first_table, projections=(
                _unsafe_clone(first_projection, multiplicity_by_key_sha256=H2),
            )), *manifest.tables[1:],
        )),
    ))

    seed0 = manifest.seed_sets[0]
    domain0 = manifest.cell_domains[0]
    spec = manifest.spec
    public_resealed_tables = (manifest.tables[1], manifest.tables[0], *manifest.tables[2:])
    public_resealed = _unsafe_clone(
        manifest,
        tables=public_resealed_tables,
        coverage_sha256=api.full_coverage_sha256(
            cell_domains=manifest.cell_domains,
            seed_sets=manifest.seed_sets,
            tables=public_resealed_tables,
        ),
    )
    bad_specs = (
        _unsafe_clone(spec, manifest_schema_version="forged"),
        _unsafe_clone(spec, owner_sha256=H1),
        _unsafe_clone(spec, s1_extent="FORGED"),
        _unsafe_clone(spec, owner_contract=_unsafe_clone(
            contract, schema_version="coded_decoder_feedback.d0.forged",
        )),
        _unsafe_clone(spec, hmm_preexecution_plan=_unsafe_clone(
            hmm_plan, member_counts=(("CLEAN_INCLUDED", 9),
                                     ("CONTROLLED_TARGET_INCLUDED", 90),
                                     ("CONTROLLED_SENTINEL_EXCLUDED", 90)),
        )),
        _unsafe_clone(spec, computation_preexecution_plan=_unsafe_clone(
            computation_plan, entries=(),
        )),
    )
    mutations = table_mutations + [
        _unsafe_clone(manifest, scope=api.EXPLICIT_PARTIAL),
        _unsafe_clone(manifest, coverage_sha256=H1),
        _unsafe_clone(manifest, authority_sha256=H2),
        _unsafe_clone(manifest, cell_domains=manifest.cell_domains[1:]),
        _unsafe_clone(manifest, cell_domains=(
            _unsafe_clone(domain0, name="forged"), *manifest.cell_domains[1:],
        )),
        _unsafe_clone(manifest, cell_domains=(
            _unsafe_clone(domain0, exact_values=domain0.exact_values[:-1]),
            *manifest.cell_domains[1:],
        )),
        _unsafe_clone(manifest, seed_sets=manifest.seed_sets[1:]),
        _unsafe_clone(manifest, seed_sets=(
            _unsafe_clone(seed0, record_type="FORGED"), *manifest.seed_sets[1:],
        )),
        _unsafe_clone(manifest, seed_sets=(
            _unsafe_clone(seed0, exact_values=seed0.exact_values[:-1]),
            *manifest.seed_sets[1:],
        )),
        _unsafe_clone(manifest, spec=maximum.spec),
        public_resealed,
        *(_unsafe_clone(manifest, spec=bad_spec) for bad_spec in bad_specs),
    ]
    assert len(mutations) >= 30
    for mutated in mutations:
        with pytest.raises(api.SchemaError):
            api.assert_full_manifest_authority(mutated)
        with pytest.raises(api.SchemaError):
            api.validate_relations({}, mutated)


def test_relational_manifest_is_partial_only():
    api = _api()
    dataset, partial = _relational_dataset()
    api.validate_partial_relations(dataset, partial)

    with pytest.raises((api.SchemaError, TypeError)):
        dataclasses.replace(partial, scope=api.FULL_D0_ARTIFACT)
    tampered = _unsafe_clone(partial, scope=api.FULL_D0_ARTIFACT)
    with pytest.raises(api.SchemaError):
        api.validate_partial_relations(dataset, tampered)
    with pytest.raises(api.SchemaError):
        api.validate_relations(dataset, tampered)


def test_full_manifest_formula_exact_coverage():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    first = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan, computation_preexecution_plan=computation_plan,
    )
    maximum = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="MAXIMUM",
        hmm_preexecution_plan=hmm_plan, computation_preexecution_plan=computation_plan,
    )
    expected_tables = {
        "s1_trajectory", "s2_method", "s3_candidate", "s3_lambda_freeze",
        "s4_check", "computation_ledger", "bps_dev_score", "b2_hmm_grid_chunk",
        "b2_tuple_clean_dev", "b2_tuple_controlled_dev",
    }
    assert first.scope == maximum.scope == api.FULL_D0_ARTIFACT
    assert {item.table for item in first.tables} == expected_tables
    first_counts = {item.table: item.projections[0].expected_key_count for item in first.tables}
    maximum_counts = {item.table: item.projections[0].expected_key_count for item in maximum.tables}
    assert first_counts == {
        "s1_trajectory": 480, "s2_method": 2160, "s3_candidate": 10800,
        "s3_lambda_freeze": 1, "s4_check": 7, "computation_ledger": 2,
        "bps_dev_score": 7200, "b2_hmm_grid_chunk": 263520,
        "b2_tuple_clean_dev": 1200, "b2_tuple_controlled_dev": 21600,
    }
    assert maximum_counts == {**first_counts, "s1_trajectory": 1200}
    hmm_expectation = next(item for item in first.tables if item.table == "b2_hmm_grid_chunk")
    assert len(hmm_expectation.projections) == 2
    assert hmm_expectation.projections[1].expected_key_count == 263520
    assert first.coverage_sha256 != maximum.coverage_sha256
    with pytest.raises(api.SchemaError):
        api.validate_partial_relations({}, first)


def test_full_manifest_required_tables_fail_closed():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    manifest = api.build_full_relational_manifest(
        owner_contract=contract, s1_extent="FIRST_STAGE",
        hmm_preexecution_plan=hmm_plan, computation_preexecution_plan=computation_plan,
    )
    empty = {item.table: () for item in manifest.tables}
    for expectation in manifest.tables:
        deleted = dict(empty)
        deleted.pop(expectation.table)
        with pytest.raises(api.SchemaError):
            api.validate_relations(deleted, manifest)
        rotated_tables = (expectation,) + tuple(
            item for item in manifest.tables if item.table != expectation.table
        )
        rotated = _unsafe_clone(
            manifest, tables=rotated_tables,
            coverage_sha256=api.full_coverage_sha256(
                cell_domains=manifest.cell_domains, seed_sets=manifest.seed_sets,
                tables=rotated_tables,
            ),
        )
        with pytest.raises(api.SchemaError):
            api.validate_relations(empty, rotated)
    extra = dict(empty)
    extra["undeclared"] = ()
    with pytest.raises(api.SchemaError):
        api.validate_relations(extra, manifest)


def test_full_manifest_rejects_bad_preexecution_plans():
    api = _api()
    contract, hmm_plan, computation_plan = _full_inputs(api)
    bad_hmm = (
        {"p_s_indices": tuple(range(121))},
        {"sigma_e2_indices": (0, 1, 2, 3, 4, 4)},
        {"roles": ("CLEAN_INCLUDED", "CONTROLLED_TARGET_INCLUDED")},
        {"cell_ids": hmm_plan.cell_ids[:-1]},
        {"polarizations": ("X",)},
        {"member_counts": (("CLEAN_INCLUDED", 9), ("CONTROLLED_TARGET_INCLUDED", 90),
                           ("CONTROLLED_SENTINEL_EXCLUDED", 90))},
        {"binding_scheme": "UNKNOWN"},
        {"member_namespace_sha256": "bad"},
    )
    for changes in bad_hmm:
        with pytest.raises(api.SchemaError):
            mutated = dataclasses.replace(hmm_plan, **changes)
            api.build_full_relational_manifest(
                owner_contract=contract, s1_extent="FIRST_STAGE",
                hmm_preexecution_plan=mutated,
                computation_preexecution_plan=computation_plan,
            )
    bad_computation_entries = (
        (),
        (computation_plan.entries[0], computation_plan.entries[0]),
        (
            api.ComputationPlanEntry("cache", "B2_DEV", "B2_DECODE",
                                     "CACHE_READ", "ghost"),
        ),
    )
    for entries in bad_computation_entries:
        with pytest.raises(api.SchemaError):
            mutated = api.ComputationPreexecutionPlan(entries=entries)
            api.build_full_relational_manifest(
                owner_contract=contract, s1_extent="FIRST_STAGE",
                hmm_preexecution_plan=hmm_plan,
                computation_preexecution_plan=mutated,
            )
    for extent in ("UNKNOWN", True):
        with pytest.raises(api.SchemaError):
            api.build_full_relational_manifest(
                owner_contract=contract, s1_extent=extent,
                hmm_preexecution_plan=hmm_plan,
                computation_preexecution_plan=computation_plan,
            )
