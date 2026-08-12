"""Focused tests for the Q001 receiver/truth firewall and paired generator."""

from dataclasses import fields, replace
import csv
import inspect
import json
from pathlib import Path

import numpy as np
import pytest
import smoke_core

from run_smoke import (
    B1_THRESHOLDS_DB,
    DEV_SEEDS,
    TEST_SEEDS,
    aggregate_from_raw,
    evaluate_terminal,
    merge_raw,
    rank_auc,
    run_split,
    tune_dev,
    validate_freeze_receipt,
    write_freeze_receipt,
    write_raw_rows,
)

from smoke_core import (
    ArmOutput,
    BranchEstimate,
    CellSpec,
    ReceiverFrame,
    TruthRecord,
    audit_deployable_information_boundary,
    build_primary_cells,
    combine_subset,
    estimate_branches,
    evaluate_subsets,
    generate_realization,
    guarded_sync_peak_margin,
    payload_ber,
    receiver_realization_hash,
    run_b0,
    run_b1,
    run_b2,
    COMPLEX_NOISE_VARIANCE,
)


def _unsafe_evaluator_leaf():
    truth_type = TruthRecord
    return evaluate_subsets, truth_type


def _innocent_named_deployable_root():
    return _unsafe_evaluator_leaf()


FORBIDDEN_RECEIVER_FIELDS = {
    "payload_bits",
    "payload_symbols",
    "offsets",
    "branch_gains",
    "branch_snr_db",
    "turbulence",
    "true_phase",
    "true_cfo",
    "cell_id",
    "turbulence_label",
    "heterogeneity",
}


def _cell(turbulence: str = "weak", n_branches: int = 2, heterogeneity: str = "H0") -> CellSpec:
    return next(
        cell
        for cell in build_primary_cells()
        if cell.turbulence == turbulence
        and cell.n_branches == n_branches
        and cell.heterogeneity == heterogeneity
    )


def test_receiver_truth_dtos_are_frozen_and_disjoint() -> None:
    receiver_fields = {field.name for field in fields(ReceiverFrame)}
    truth_fields = {field.name for field in fields(TruthRecord)}

    assert ReceiverFrame.__dataclass_params__.frozen
    assert TruthRecord.__dataclass_params__.frozen
    assert receiver_fields.isdisjoint(FORBIDDEN_RECEIVER_FIELDS)
    assert {"payload_bits", "payload_symbols", "offsets", "branch_gains"} <= truth_fields
    assert "nominal_snr_offset_db" in truth_fields
    assert "instantaneous_snr_db" in truth_fields
    assert "branch_snr_db" not in truth_fields
    assert all(field.type is not str for field in fields(ReceiverFrame))

    frame, _, _ = generate_realization(seed=1, cell=_cell(), payload_symbols=128)
    assert not any(isinstance(getattr(frame, field.name), str) for field in fields(frame))
    hash_source = inspect.getsource(receiver_realization_hash).lower()
    assert not any(label in hash_source for label in ("cell_id", "weak", "moderate", "strong", "h0", "h1", "h2"))


def test_primary_grid_has_exactly_eighteen_natural_cells() -> None:
    cells = build_primary_cells()

    assert len(cells) == 18
    assert len({cell.cell_id for cell in cells}) == 18
    assert {(cell.turbulence, cell.gg_alpha, cell.gg_beta) for cell in cells} == {
        ("weak", 11.6, 10.1),
        ("moderate", 4.0, 1.9),
        ("strong", 4.2, 1.4),
    }
    assert {(cell.n_branches, cell.heterogeneity) for cell in cells} == {
        (n, h) for n in (2, 4) for h in ("H0", "H1", "H2")
    }
    assert all(cell.parameter_status == "UNVERIFIED_RANGE" for cell in cells)
    assert _cell(n_branches=2, heterogeneity="H0").branch_snr_db == (0.0, 0.0)
    assert _cell(n_branches=2, heterogeneity="H1").branch_snr_db == (0.0, -1.0)
    assert _cell(n_branches=2, heterogeneity="H2").branch_snr_db == (0.0, -6.0)
    assert _cell(n_branches=4, heterogeneity="H2").branch_snr_db == (0.0, 0.0, -6.0, -6.0)


def test_same_cell_and_seed_replay_receiver_and_truth_exactly() -> None:
    cell = _cell(turbulence="moderate", n_branches=4, heterogeneity="H1")
    frame_a, truth_a, hash_a = generate_realization(seed=17, cell=cell, payload_symbols=512)
    frame_b, truth_b, hash_b = generate_realization(seed=17, cell=cell, payload_symbols=512)

    assert hash_a == hash_b == receiver_realization_hash(frame_a)
    assert all(np.array_equal(a, b) for a, b in zip(frame_a.branches, frame_b.branches))
    assert np.array_equal(truth_a.payload_bits, truth_b.payload_bits)
    assert np.array_equal(truth_a.payload_symbols, truth_b.payload_symbols)
    assert truth_a.offsets == truth_b.offsets
    assert np.array_equal(truth_a.branch_gains, truth_b.branch_gains)
    expected_instantaneous = 10.0 * np.log10(
        np.abs(truth_a.branch_gains) ** 2 / truth_a.noise_variance_complex
    )
    assert np.allclose(truth_a.instantaneous_snr_db, expected_instantaneous)


def test_common_noise_variance_and_h2_offset_scale_effective_gain() -> None:
    _, truth, _ = generate_realization(seed=19, cell=_cell(n_branches=4, heterogeneity="H2"), payload_symbols=128)

    assert COMPLEX_NOISE_VARIANCE == truth.noise_variance_complex == 1.0
    ratios = np.abs(truth.branch_gains / truth.unscaled_branch_gains)
    assert np.allclose(ratios[:2], 1.0, rtol=0, atol=1e-14)
    assert np.allclose(ratios[2:], 10.0 ** (-6.0 / 20.0), rtol=0, atol=1e-14)


def test_true_prefix_offsets_are_physically_present_in_receiver_samples() -> None:
    frame, truth, _ = generate_realization(seed=5, cell=_cell(), payload_symbols=512)
    fsts = frame.fsts

    for branch, true_offset in zip(frame.branches, truth.offsets):
        scores = smoke_core._normalized_sync_scores(
            branch, training_length=len(fsts), max_offset=frame.max_search_offset
        )
        assert int(np.argmax(scores)) == true_offset
        assert len(branch) == len(fsts) + 512 + frame.max_search_offset


def test_truth_copy_cannot_change_receiver_or_receiver_hash() -> None:
    frame, truth, digest = generate_realization(seed=31, cell=_cell(), payload_symbols=512)
    copied_truth = replace(
        truth,
        offsets=tuple(reversed(truth.offsets)),
        nominal_snr_offset_db=tuple(value + 99.0 for value in truth.nominal_snr_offset_db),
        instantaneous_snr_db=truth.instantaneous_snr_db + 99.0,
        turbulence="mutated-truth-only",
    )

    assert copied_truth != truth
    assert receiver_realization_hash(frame) == digest
    assert all(branch.flags.writeable is False for branch in frame.branches)


def test_fsts_proxy_has_bn_bl_and_conjugate_symmetric_halves() -> None:
    frame, _, _ = generate_realization(seed=2, cell=_cell(), payload_symbols=512)
    blocks = frame.fsts.reshape(16, 20)

    assert frame.fsts.size == 320
    assert np.array_equal(blocks[8:], np.conj(blocks[:8][::-1, ::-1]))
    assert np.allclose(np.abs(frame.fsts), 1.0)


def test_sync_metric_is_park_style_not_matched_template() -> None:
    parameters = inspect.signature(smoke_core._normalized_sync_scores).parameters

    assert "fsts" not in parameters
    assert "training_length" in parameters


def test_generator_has_no_explicit_defect_injection_controls() -> None:
    forbidden = {"slip", "outage", "corrupt", "invalid", "defect", "inject"}
    parameter_names = set(inspect.signature(generate_realization).parameters)
    cell_fields = {field.name for field in fields(CellSpec)}

    assert not any(token in name.lower() for name in parameter_names | cell_fields for token in forbidden)


def _estimate(gain: complex, samples: np.ndarray, snr_db: float) -> BranchEstimate:
    return BranchEstimate(
        estimated_offset=0,
        sync_peak=1.0,
        sync_margin=0.5,
        estimated_channel=gain,
        estimated_snr_db=snr_db,
        estimated_power=float(abs(gain) ** 2),
        pilot_ls_residual=0.01,
        pilot_coherence=0.99,
        cpe_increment_rms=0.01,
        cpe_coherence=0.99,
        phase_corrected_payload=np.asarray(samples, dtype=np.complex128),
    )


def test_branch_estimate_is_receiver_visible_only() -> None:
    names = {field.name for field in fields(BranchEstimate)}
    assert names == {
        "estimated_offset", "sync_peak", "sync_margin", "estimated_channel",
        "estimated_snr_db", "estimated_power", "pilot_ls_residual",
        "pilot_coherence", "cpe_increment_rms", "cpe_coherence",
        "phase_corrected_payload",
    }
    assert names.isdisjoint(FORBIDDEN_RECEIVER_FIELDS)


def test_correct_mrc_matches_hand_computed_complex_example() -> None:
    symbols = np.asarray([1 + 2j, -2 + 0.5j])
    gains = (2 + 1j, -0.5 + 0.75j)
    estimates = tuple(_estimate(g, g * symbols, 10.0) for g in gains)
    expected = sum(np.conj(g) * (g * symbols) for g in gains) / sum(abs(g) ** 2 for g in gains)

    actual = combine_subset(estimates, (0, 1))

    assert np.allclose(actual, expected, rtol=0, atol=1e-14)


def test_fixed_arms_no_valid_and_order_invariance() -> None:
    estimates = (
        _estimate(1 + 0j, np.ones(8, dtype=np.complex128), -4.0),
        _estimate(2 + 0j, 2 * np.ones(8, dtype=np.complex128), 3.0),
    )
    first = (run_b0(estimates), run_b1(estimates, tau_db=9.0), run_b2(estimates, top_l=1))
    second = (run_b2(estimates, top_l=1), run_b0(estimates), run_b1(estimates, tau_db=9.0))

    assert first[0] == second[1]
    assert first[1] == second[2]
    assert first[2] == second[0]
    assert first[1].no_valid and first[1].subset == () and first[1].combined is None
    assert first[2].subset == (1,) and not first[2].no_valid


def test_generated_receiver_estimates_offsets_and_outputs_finite() -> None:
    frame, truth, _ = generate_realization(seed=5, cell=_cell(), payload_symbols=512)
    estimates = estimate_branches(frame)

    assert tuple(item.estimated_offset for item in estimates) == truth.offsets
    assert all(np.all(np.isfinite(item.phase_corrected_payload)) for item in estimates)
    assert all(np.isfinite(item.pilot_ls_residual) for item in estimates)
    assert np.all(np.isfinite(run_b0(estimates).combined))


def test_known_pilot_phase_interpolation_reduces_pilot_residual() -> None:
    fsts = np.ones(8, dtype=np.complex128)
    pilot_mask = np.asarray([True, False, True, False, True, False, True, False])
    pilot_symbols = np.ones(4, dtype=np.complex128)
    payload_mask = ~pilot_mask
    phase = np.linspace(0.0, 1.2, pilot_mask.size)
    gain = 1.7 - 0.4j
    payload = gain * np.exp(1j * phase)
    branch = np.concatenate((gain * fsts, payload))
    frame = ReceiverFrame(
        branches=(branch,), fsts=fsts, pilot_mask=pilot_mask,
        pilot_symbols=pilot_symbols, payload_mask=payload_mask,
        ts=1e-10, max_search_offset=0,
    )
    uncorrected = float(np.mean(np.abs(payload[pilot_mask] - gain * pilot_symbols) ** 2))

    estimate = estimate_branches(frame)[0]

    assert estimate.pilot_ls_residual < uncorrected * 1e-12


def test_sync_margin_excludes_adjacent_peak_with_frozen_guard_one() -> None:
    scores = np.asarray([0.20, 0.91, 0.99, 0.94, 0.30, 0.60])

    peak, margin = guarded_sync_peak_margin(scores, winner=2)

    assert peak == 0.99
    assert margin == 0.39  # 0.99 - max(scores[0], scores[4:]); indices 1..3 guarded


def test_truth_metadata_flip_cannot_change_deployable_outputs_or_features() -> None:
    frame, truth, _ = generate_realization(seed=43, cell=_cell(n_branches=4), payload_symbols=512)
    estimates_a = estimate_branches(frame)
    outputs_a = (run_b0(estimates_a), run_b1(estimates_a, -2.0), run_b2(estimates_a, 2))
    changed_truth = replace(
        truth,
        payload_bits=np.bitwise_xor(truth.payload_bits, np.uint8(1)),
        offsets=tuple((value + 3) % 8 for value in truth.offsets),
        branch_gains=-truth.branch_gains,
        nominal_snr_offset_db=tuple(value + 50 for value in truth.nominal_snr_offset_db),
        instantaneous_snr_db=truth.instantaneous_snr_db + 50,
        turbulence="flipped",
        shared_phase=-truth.shared_phase,
    )
    estimates_b = estimate_branches(frame)
    outputs_b = (run_b0(estimates_b), run_b1(estimates_b, -2.0), run_b2(estimates_b, 2))

    assert not np.array_equal(changed_truth.payload_bits, truth.payload_bits)
    assert changed_truth.offsets != truth.offsets
    assert estimates_a == estimates_b
    assert outputs_a == outputs_b


def test_payload_ber_excludes_pilots_and_uses_fixed_denominator_with_pi2_resolution() -> None:
    tx_bits = np.asarray([[0, 0], [1, 1], [0, 1], [1, 0]], dtype=np.uint8)
    tx_symbols = np.asarray([1 + 1j, -1 - 1j, 1 - 1j, -1 + 1j]) / np.sqrt(2)
    payload_mask = np.asarray([False, True, True, True])
    rotated = 1j * tx_symbols

    ber = payload_ber(rotated, tx_bits, payload_mask)

    assert ber == 0.0


def test_oracle_is_evaluator_only_and_deployable_ast_boundary_is_clean() -> None:
    estimates = (
        _estimate(1 + 0j, np.ones(4, dtype=np.complex128), 0.0),
        _estimate(1 + 0j, -np.ones(4, dtype=np.complex128), 0.0),
    )
    bits = np.zeros((4, 2), dtype=np.uint8)
    symbols = np.ones(4, dtype=np.complex128) * (1 + 1j) / np.sqrt(2)
    truth = TruthRecord(
        bits,
        symbols,
        (0, 0),
        np.ones(2, dtype=np.complex128),
        (0.0, 0.0),
        np.asarray((0.0, 0.0)),
        "synthetic",
        np.zeros(4),
    )

    oracle = evaluate_subsets(estimates, truth, np.ones(4, dtype=np.bool_))

    assert oracle.subset in {(0,), (1,), (0, 1)}
    assert 0.0 <= oracle.ber <= 1.0
    assert audit_deployable_information_boundary() == ()
    for fn in (run_b0, run_b1, run_b2):
        assert "truth" not in inspect.signature(fn).parameters


def test_truth_channel_oracle_beats_estimated_mrc_when_channel_estimates_are_wrong() -> None:
    samples_a = np.asarray([-.2 + 1j, 1 + 1j]) / np.sqrt(2)
    samples_b = np.asarray([1 + 1j, -.2 + 1j]) / np.sqrt(2)
    estimates = (_estimate(1 + 0j, samples_a, 0.0), _estimate(-1 + 0j, samples_b, 0.0))
    bits = np.zeros((2, 2), dtype=np.uint8)
    truth = TruthRecord(bits, np.ones(2) * (1 + 1j) / np.sqrt(2), (0, 0),
                        np.ones(2, dtype=np.complex128), (0.0, 0.0),
                        np.zeros(2), "synthetic", np.zeros(2))
    estimated_best = min(
        payload_ber(combine_subset(estimates, subset), bits, np.ones(2, dtype=np.bool_))
        for subset in ((0,), (1,), (0, 1))
    )

    oracle = evaluate_subsets(estimates, truth, np.ones(2, dtype=np.bool_))

    assert oracle.subset == (0, 1)
    assert oracle.ber < estimated_best
    expected = (samples_a + samples_b) / 2.0
    assert np.allclose(oracle.combined, expected)


def test_recursive_ast_boundary_audit_rejects_indirect_evaluator_reference() -> None:
    violations = audit_deployable_information_boundary((_innocent_named_deployable_root,))

    assert any("TruthRecord" in item for item in violations)
    assert any("evaluate_subsets" in item for item in violations)
    assert any("_unsafe_evaluator_leaf" in item for item in violations)


def test_recursive_ast_boundary_ignores_unreachable_evaluator_only_functions() -> None:
    assert audit_deployable_information_boundary((run_b0,)) == ()


def _synthetic_raw_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for seed, invalid, label in ((0, 1, 1), (1, 0, 0), (2, 1, 1), (3, 0, 0)):
        receiver_hash = f"hash-{seed}"
        rows.append({
            "row_type": "branch", "split": "dev", "seed": seed,
            "cell": "weak-K2-H0", "turbulence": "weak", "K": 2,
            "heterogeneity": "H0", "receiver_hash": receiver_hash,
            "branch_index": 0, "estimated_snr_db": 2.0 if invalid else -4.0,
            "sync_peak": 0.9, "sync_margin": 0.4 if invalid else 0.1,
            "pilot_ls_residual": 0.2 if invalid else 0.01,
            "pilot_coherence": 0.5 if invalid else 0.99,
            "cpe_increment_rms": 0.4 if invalid else 0.01,
            "cpe_coherence": 0.6 if invalid else 0.99,
            "offset_match": 1 - invalid, "individual_ber": 0.46 if invalid else 0.01,
            "dsp_invalid": invalid, "o1_inclusion": label,
        })
        rows.append({
            "row_type": "branch", "split": "dev", "seed": seed,
            "cell": "weak-K2-H0", "turbulence": "weak", "K": 2,
            "heterogeneity": "H0", "receiver_hash": receiver_hash,
            "branch_index": 1, "estimated_snr_db": -5.0,
            "sync_peak": 0.9, "sync_margin": 0.2,
            "pilot_ls_residual": 0.01, "pilot_coherence": 0.99,
            "cpe_increment_rms": 0.01, "cpe_coherence": 0.99,
            "offset_match": 1, "individual_ber": 0.01,
            "dsp_invalid": 0, "o1_inclusion": 1 - label,
        })
        method_specs = [
            ("B0", "all", 0.20 if invalid else 0.01),
            *[("B1", str(tau), (0.08 if invalid else 0.02) if tau == 0 else (0.18 if invalid else 0.01)) for tau in B1_THRESHOLDS_DB],
            ("B2", "1", 0.07 if invalid else 0.02),
            ("B2", "2", 0.20 if invalid else 0.01),
            ("O1", "oracle", 0.04 if invalid else 0.01),
        ]
        for method, parameter, ber in method_specs:
            rows.append({
                "row_type": "method", "split": "dev", "seed": seed,
                "cell": "weak-K2-H0", "turbulence": "weak", "K": 2,
                "heterogeneity": "H0", "receiver_hash": receiver_hash,
                "method": method, "candidate_parameter": parameter,
                "selected_subset": "0", "no_valid": 0,
                "pre_fec_ber_fixed": ber, "outage": int(ber > 0.02),
                "n_payload_bits": 1000,
            })
    return rows


def test_runner_constants_and_tuning_are_dev_only_and_deterministic() -> None:
    frozen = tune_dev(_synthetic_raw_rows(), validation_mode="unit")

    assert B1_THRESHOLDS_DB == (-8, -6, -4, -2, -1, 0, 1, 2, 4, 6)
    assert set(DEV_SEEDS).isdisjoint(TEST_SEEDS)
    assert frozen["b1_tau_db"] == 0.0
    assert frozen["top_l_by_k"] == {"2": 1}
    assert frozen["strongest_cheap"] in {"B1", "B2"}
    assert set(frozen["diagnostic_models"]) == {"power_only", "multi_source"}


def test_rank_auc_handles_ties_and_single_class() -> None:
    assert rank_auc(np.asarray([0, 0, 1, 1]), np.asarray([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert rank_auc(np.asarray([0, 1]), np.asarray([0.5, 0.5])) == 0.5
    assert np.isnan(rank_auc(np.asarray([1, 1]), np.asarray([0.1, 0.2])))


def test_raw_aggregate_is_reconstructable_and_byte_stable(tmp_path: Path) -> None:
    raw = tmp_path / "raw.csv"
    write_raw_rows(raw, _synthetic_raw_rows())
    frozen = tune_dev(_synthetic_raw_rows(), validation_mode="unit")
    first = aggregate_from_raw(raw, frozen, bootstrap_replicates=20, bootstrap_seed=7, validation_mode="unit")
    second = aggregate_from_raw(raw, frozen, bootstrap_replicates=20, bootstrap_seed=7, validation_mode="unit")

    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(
        second, sort_keys=True, separators=(",", ":")
    )
    assert first["g1"]["event_frames"] == 2
    assert first["g1"]["event_cells"] == ["weak-K2-H0"]
    assert first["g1"]["ci"]["low"] < first["g1"]["ci"]["high"]
    assert first["bootstrap"]["replicates"] == 20
    assert first["g2"]["regret_ci"]["valid_replicates"] < 20
    assert first["terminal"] in {
        "PROBLEM_ABSENT_OR_TOO_SMALL", "PROBLEM_RESOLVED_BY_CONVENTIONAL_RULE",
        "DEFECT_NOT_RECEIVER_OBSERVABLE", "DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT",
    }


@pytest.mark.parametrize(
    ("metrics", "terminal"),
    [
        ({"g1": False, "g2": True, "g3": True, "g4": True}, "PROBLEM_ABSENT_OR_TOO_SMALL"),
        ({"g1": True, "g2": False, "g3": True, "g4": True}, "PROBLEM_ABSENT_OR_TOO_SMALL"),
        ({"g1": True, "g2": True, "g3": False, "g4": True}, "PROBLEM_RESOLVED_BY_CONVENTIONAL_RULE"),
        ({"g1": True, "g2": True, "g3": True, "g4": False}, "DEFECT_NOT_RECEIVER_OBSERVABLE"),
        ({"g1": True, "g2": True, "g3": True, "g4": True}, "DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT"),
    ],
)
def test_terminal_fail_stop_order(metrics: dict[str, bool], terminal: str) -> None:
    assert evaluate_terminal(metrics) == terminal


def test_merge_rejects_duplicate_and_missing_seed_cell_pairs(tmp_path: Path) -> None:
    rows = _synthetic_raw_rows()
    part_a = tmp_path / "a.csv"
    part_b = tmp_path / "b.csv"
    write_raw_rows(part_a, rows)
    write_raw_rows(part_b, rows)

    with pytest.raises(ValueError, match="duplicate"):
        merge_raw((part_a, part_b), tmp_path / "merged.csv", range(4), ("weak-K2-H0",), validation_mode="unit")
    with pytest.raises(ValueError, match="missing"):
        merge_raw((part_a,), tmp_path / "missing.csv", range(5), ("weak-K2-H0",), validation_mode="unit")

    broken = tmp_path / "broken.csv"
    write_raw_rows(broken, rows[1:])
    with pytest.raises(ValueError, match="branch"):
        merge_raw((broken,), tmp_path / "broken-merged.csv", range(4), ("weak-K2-H0",), validation_mode="unit")


def test_aggregate_rejects_receiver_hash_mismatch_within_pair(tmp_path: Path) -> None:
    rows = _synthetic_raw_rows()
    rows[1] = {**rows[1], "receiver_hash": "different-realization"}
    raw = tmp_path / "raw.csv"
    write_raw_rows(raw, rows)

    with pytest.raises(ValueError, match="receiver hash"):
        aggregate_from_raw(raw, tune_dev(_synthetic_raw_rows(), validation_mode="unit"), bootstrap_replicates=10, validation_mode="unit")


def test_tune_rejects_receiver_hash_mismatch_and_cell_identity_mismatch() -> None:
    rows = _synthetic_raw_rows()
    rows[1] = {**rows[1], "receiver_hash": "different-realization"}
    with pytest.raises(ValueError, match="receiver hash"):
        tune_dev(rows, validation_mode="unit")

    rows = _synthetic_raw_rows()
    rows[0] = {**rows[0], "turbulence": "strong"}
    with pytest.raises(ValueError, match="canonical cell"):
        tune_dev(rows, validation_mode="unit")


def _receipt_inputs(tmp_path: Path):
    names = ("design", "implementation_plan", "smoke_core", "run_smoke", "test_smoke")
    sources = {}
    for name in names:
        target = tmp_path / f"{name}.txt"
        target.write_text(name + "\n", encoding="utf-8")
        sources[name] = target
    raw, aggregate = tmp_path / "raw.csv", tmp_path / "aggregate.json"
    raw.write_text("raw\n", encoding="utf-8")
    aggregate.write_text("{}\n", encoding="utf-8")
    frozen = tune_dev(_synthetic_raw_rows(), validation_mode="unit")
    frozen["top_l_by_k"] = {"2": 1, "4": 1}
    return sources, raw, aggregate, frozen


def test_freeze_receipt_fails_closed_on_hash_mismatch(tmp_path: Path) -> None:
    sources, raw, aggregate, frozen = _receipt_inputs(tmp_path)
    receipt = tmp_path / "freeze.json"
    write_freeze_receipt(receipt, sources, raw, aggregate, frozen, bootstrap_replicates=1000)
    assert validate_freeze_receipt(receipt)["test_started"] is False

    sources["smoke_core"].write_text("changed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_freeze_receipt(receipt)


def test_receipt_rejects_missing_manifest_empty_forgery_and_illegal_frozen(tmp_path: Path) -> None:
    sources, raw, aggregate, frozen = _receipt_inputs(tmp_path)
    with pytest.raises(ValueError, match="manifest"):
        write_freeze_receipt(tmp_path / "missing.json", {"design": sources["design"]}, raw, aggregate, frozen)

    receipt = tmp_path / "freeze.json"
    write_freeze_receipt(receipt, sources, raw, aggregate, frozen)
    forged = json.loads(receipt.read_text(encoding="utf-8"))
    forged["hashed_files"] = {}
    receipt.write_text(json.dumps(forged), encoding="utf-8")
    with pytest.raises(ValueError, match="manifest"):
        validate_freeze_receipt(receipt)

    receipt_illegal = tmp_path / "freeze-illegal.json"
    write_freeze_receipt(receipt_illegal, sources, raw, aggregate, frozen)
    forged = json.loads(receipt_illegal.read_text(encoding="utf-8"))
    forged["frozen"]["top_l_by_k"] = {"2": 0, "4": 9}
    receipt_illegal.write_text(json.dumps(forged), encoding="utf-8")
    with pytest.raises(ValueError, match="frozen"):
        validate_freeze_receipt(receipt_illegal)


def test_freeze_receipt_refuses_rewrite(tmp_path: Path) -> None:
    sources, raw, aggregate, frozen = _receipt_inputs(tmp_path)
    receipt = tmp_path / "freeze.json"
    write_freeze_receipt(receipt, sources, raw, aggregate, frozen)
    with pytest.raises(FileExistsError):
        write_freeze_receipt(receipt, sources, raw, aggregate, frozen)


def test_strict_validation_rejects_tiny_or_wrong_split_raw() -> None:
    with pytest.raises(ValueError, match="DEV_SEEDS"):
        tune_dev(_synthetic_raw_rows())


def test_strict_tune_reuses_canonical_cells_for_full_seed_cartesian_product() -> None:
    rows = []
    for seed in DEV_SEEDS:
        for cell in build_primary_cells():
            common = {
                "split": "dev", "seed": seed, "cell": cell.cell_id,
                "turbulence": cell.turbulence, "K": cell.n_branches,
                "heterogeneity": cell.heterogeneity, "receiver_hash": f"{seed}-{cell.cell_id}",
                "gg_alpha": cell.gg_alpha, "gg_beta": cell.gg_beta,
                "branch_snr_db": json.dumps(cell.branch_snr_db),
                "parameter_status": cell.parameter_status,
            }
            for branch_index in range(cell.n_branches):
                label = branch_index % 2
                rows.append({
                    **common, "row_type": "branch", "branch_index": branch_index,
                    "estimated_snr_db": float(branch_index), "sync_peak": 0.9,
                    "sync_margin": 0.2, "pilot_ls_residual": 0.01 + 0.01 * label,
                    "pilot_coherence": 0.99 - 0.1 * label,
                    "cpe_increment_rms": 0.01 + 0.1 * label,
                    "cpe_coherence": 0.99 - 0.1 * label, "offset_match": 1,
                    "individual_ber": 0.01, "dsp_invalid": 0, "o1_inclusion": label,
                })
            method_specs = [
                ("B0", "all"), ("O1", "oracle"),
                *(("B1", str(tau)) for tau in B1_THRESHOLDS_DB),
                *(("B2", str(top_l)) for top_l in range(1, cell.n_branches + 1)),
            ]
            for method, parameter in method_specs:
                rows.append({
                    **common, "row_type": "method", "method": method,
                    "candidate_parameter": parameter, "selected_subset": "0",
                    "no_valid": 0, "pre_fec_ber_fixed": 0.01,
                    "outage": 0, "n_payload_bits": 1000,
                })

    frozen = tune_dev(rows)

    assert set(frozen["top_l_by_k"]) == {"2", "4"}


def test_raw_writer_refuses_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "raw.csv"
    write_raw_rows(target, _synthetic_raw_rows())
    with pytest.raises(FileExistsError):
        write_raw_rows(target, _synthetic_raw_rows())


def test_run_split_refuses_existing_raw_before_generation(tmp_path: Path, monkeypatch) -> None:
    import run_smoke

    raw = tmp_path / "raw.csv"
    raw.write_text("sentinel\n", encoding="utf-8")
    monkeypatch.setattr(run_smoke, "_realization_rows", lambda *args: (_ for _ in ()).throw(AssertionError("generated")))
    with pytest.raises(FileExistsError):
        run_split("dev", [0], tmp_path, None)


def test_no_proposed_soft_method_or_truth_field_enters_arm_schema() -> None:
    import run_smoke

    source = inspect.getsource(run_smoke)
    assert "soft_weight" not in source.lower()
    assert "abstention_method" not in source.lower()
    for function in (run_b0, run_b1, run_b2):
        assert all("truth" not in name.lower() for name in inspect.signature(function).parameters)
