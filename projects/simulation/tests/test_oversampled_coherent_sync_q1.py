from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import numpy as np
import pytest


PROBE_DIR = (
    Path(__file__).resolve().parents[1]
    / "explore"
    / "oversampled-coherent-sync-q1"
)
sys.path.insert(0, str(PROBE_DIR))

import run_semantic_smoke as smoke_runner  # noqa: E402
import semantic_smoke_core as smoke_core  # noqa: E402

from semantic_smoke_core import (  # noqa: E402
    ReceiverVisible,
    SmokeConfig,
    TruthMetadata,
    acquisition_metrics,
    additive_interaction_residual,
    argmax_lexicographic,
    build_manifest,
    derive_cell_seed,
    estimate_all,
    find_stable_2x2,
    generate_cell,
    make_rrc_taps,
    normalized_glrt,
    reduce_terminal,
    score_cube,
    select_b0,
    select_b1,
    select_b2,
    select_c_grid,
    validate_artifact_references,
    validate_manifest,
    validate_output_dir,
)
from run_semantic_smoke import _method_table, build_parser, run_identity  # noqa: E402


def test_manifest_and_provenance_contract_is_complete() -> None:
    cfg = SmokeConfig()
    manifest = build_manifest(cfg)
    validate_manifest(manifest)
    assert manifest["classification"] == "GROUNDWORK_STEP4A_SEMANTIC_SMOKE"
    assert manifest["waveform"]["symbol_rate_hz"] == 56e9
    assert manifest["waveform"]["sps"] == 2
    assert manifest["waveform"]["rrc_span_symbols"] == 10
    assert manifest["reference_plane"]["d_zero"]
    assert manifest["observation_window"]["length"] == cfg.observation_length
    assert manifest["score"]["formula"] == "abs(x^H r)^2/(||x||^2||r||^2)"
    assert manifest["score"]["tie_tolerance"] == cfg.tie_tolerance
    assert manifest["seeds"]["preamble"] == 20260807
    assert manifest["seeds"]["awgn_master"] == 20260808
    assert manifest["evidence_ceiling"] == "DIAGNOSTIC_ONLY_NOT_PAPER_NUMBER"


def test_visible_and_truth_are_disjoint_immutable_types() -> None:
    visible_fields = {field.name for field in dataclasses.fields(ReceiverVisible)}
    truth_fields = {field.name for field in dataclasses.fields(TruthMetadata)}
    assert visible_fields.isdisjoint({"true_d", "true_tau", "true_cfo_hz", "tx_waveform"})
    assert truth_fields.issuperset({"true_d", "true_tau", "true_cfo_hz"})
    assert ReceiverVisible.__dataclass_params__.frozen
    assert TruthMetadata.__dataclass_params__.frozen


def test_rrc_identity_and_fixed_window() -> None:
    cfg = SmokeConfig()
    taps = make_rrc_taps(cfg.rrc_beta, cfg.rrc_span_symbols, cfg.sps)
    assert np.isclose(np.vdot(taps, taps).real, 1.0, atol=1e-14)
    visible, truth = generate_cell(cfg, 0, 0.0, 0.0, "noiseless", "residual")
    assert len(visible.rx_samples) == cfg.observation_length
    assert truth.true_d == 0 and truth.true_tau == 0 and truth.true_cfo_hz == 0
    assert visible.rx_samples.flags.writeable is False


def test_timing_cfo_and_frame_signs_and_identity_gate() -> None:
    cfg = SmokeConfig()
    for d, tau, cfo in [(0, 0.0, 0.0), (8, 0.2, 50e6), (-8, -0.4, -100e6)]:
        visible, _ = generate_cell(cfg, d, tau, cfo, "noiseless", "residual")
        results = estimate_all(visible, cfg, cfg.residual_cfo_hypotheses_hz)
        assert {result.estimate for result in results.values()} == {(d, tau, cfo)}


def test_normalized_score_bounds_and_tie_break() -> None:
    x = np.array([1 + 1j, 2 - 1j, -0.5 + 0.2j])
    assert normalized_glrt(x, x) == pytest.approx(1.0)
    assert 0.0 <= normalized_glrt(x, x[::-1]) <= 1.0
    candidates = [(1, 0.0, 0.0), (-1, 0.2, 0.0), (-1, -0.2, 0.0)]
    scores = np.array([0.9, 0.9 + 1e-15, 0.9])
    assert argmax_lexicographic(scores, candidates, tolerance=1e-12)[0] == (-1, -0.2, 0.0)


def test_paired_realization_truth_metamorphic_and_hashes() -> None:
    cfg = SmokeConfig()
    visible, truth = generate_cell(cfg, 0, 0.2, 50e6, "minus6db", "residual")
    first = estimate_all(visible, cfg, cfg.residual_cfo_hypotheses_hz)
    mutated = dataclasses.replace(truth, true_d=999, true_tau=-99.0, true_cfo_hz=123.0)
    second = estimate_all(visible, cfg, cfg.residual_cfo_hypotheses_hz)
    assert mutated != truth
    assert json.dumps({k: v.to_jsonable() for k, v in first.items()}, sort_keys=True) == json.dumps(
        {k: v.to_jsonable() for k, v in second.items()}, sort_keys=True
    )
    assert {v.realization_id for v in first.values()} == {visible.realization_id}
    assert {v.rx_sha256 for v in first.values()} == {visible.rx_sha256}
    assert len({v.grid_hash for v in first.values()}) == 1
    assert len({v.score_hash for v in first.values()}) == 1
    assert derive_cell_seed(20260808, truth.cell_id) == derive_cell_seed(20260808, truth.cell_id)


def test_b1_c_exact_cube_equivalence_and_b2_monotonicity() -> None:
    cfg = SmokeConfig()
    visible, _ = generate_cell(cfg, 8, 0.4, 100e6, "minus6db", "residual")
    cube, candidates, _ = score_cube(visible, cfg, cfg.residual_cfo_hypotheses_hz)
    b0 = select_b0(cube, cfg.d_hypotheses, cfg.tau_hypotheses, cfg.residual_cfo_hypotheses_hz, cfg.tie_tolerance)
    b1 = select_b1(cube, cfg.d_hypotheses, cfg.tau_hypotheses, cfg.residual_cfo_hypotheses_hz, cfg.tie_tolerance)
    c = select_c_grid(cube, cfg.d_hypotheses, cfg.tau_hypotheses, cfg.residual_cfo_hypotheses_hz, cfg.tie_tolerance)
    b2 = select_b2(cube, cfg.d_hypotheses, cfg.tau_hypotheses, cfg.residual_cfo_hypotheses_hz, cfg.tie_tolerance, b0)
    assert b1.estimate == c.estimate
    assert b1.score == pytest.approx(c.score, abs=cfg.tie_tolerance)
    assert all(b >= a - cfg.tie_tolerance for a, b in zip(b2.trace_scores, b2.trace_scores[1:]))
    assert b2.iterations <= 8
    assert len(candidates) == cube.size


def test_compute_ledger_counts_real_candidate_work() -> None:
    cfg = SmokeConfig()
    visible, _ = generate_cell(cfg, 0, 0.0, 0.0, "noiseless", "residual")
    results = estimate_all(visible, cfg, cfg.residual_cfo_hypotheses_hz)
    for result in results.values():
        ledger = result.compute
        assert ledger["candidate_score_calls"] > 0
        assert ledger["complex_macs"] == ledger["candidate_score_calls"] * cfg.observation_length
        assert ledger["fft_calls"] == 0
        assert ledger["fft_sizes"] == []
        assert ledger["interpolation_calls"] >= 0


def test_traversal_ledger_preserves_repeated_visits_and_full_grid_paths() -> None:
    cfg = SmokeConfig()
    visible, _ = generate_cell(cfg, 0, 0.0, 0.0, "noiseless", "residual")
    results = estimate_all(visible, cfg, cfg.residual_cfo_hypotheses_hz)
    for method, result in results.items():
        row = result.to_jsonable()
        path = [tuple(index) for index in row["visited_candidate_indices"]]
        assert row["visited_candidate_count"] == len(path)
        assert row["compute"]["candidate_score_calls"] == len(set(path))
        assert row["compute"]["complex_macs"] == len(set(path)) * cfg.observation_length
        if method in {"B0", "B2"}:
            assert len(path) > len(set(path))
        else:
            assert len(path) == 735
            assert len(path) == len(set(path))


def test_plot_case_uses_most_confident_residual_b0_false_lock_and_markers() -> None:
    rows = [
        {"cell_id": "residual|minus6db|a", "method": "B0", "false_lock": True, "estimate": [8, 0.2, 50e6], "top1_top2_margin": 0.1},
        {"cell_id": "residual|minus6db|b", "method": "B0", "false_lock": True, "estimate": [-8, 0.4, 100e6], "top1_top2_margin": 0.4},
        {"cell_id": "stress|noiseless|c", "method": "B0", "false_lock": True, "estimate": [8, 0.4, 5e9], "top1_top2_margin": 0.9},
    ]
    truth = {
        "residual|minus6db|a": {"true_d": 0, "true_tau": 0.0, "true_cfo_hz": 0.0},
        "residual|minus6db|b": {"true_d": 0, "true_tau": -0.2, "true_cfo_hz": -50e6},
    }
    case = smoke_runner.select_b0_plot_case(
        rows,
        truth,
        {"residual|minus6db|a": "surface_1", "residual|minus6db|b": "surface_2"},
        identity_key="surface_0",
    )
    assert case["surface_key"] == "surface_2"
    assert case["truth"] == [0, -0.2, -50e6]
    assert case["top1"] == [-8, 0.4, 100e6]
    assert "Most-confident" in case["title"]
    assert "first" not in case["title"].lower()
    assert case["truth_label"] == "truth"
    assert case["top1_label"] == "B0 top1 / wrong basin"


def test_stress_only_interaction_cannot_change_residual_reducer() -> None:
    recommend = {
        "semantic_gates_pass": True,
        "complete_population": True,
        "b0_false_locks": 2,
        "b1_c_equivalent": False,
        "exact_separable": False,
        "analytic_nonseparable": True,
        "surface_nonseparable": True,
        "stable_region": True,
        "g_c": 0.10,
        "coverage_b1": 0.50,
        "coverage_b2": 0.50,
    }
    residual = {"noiseless": recommend, "minus6db": recommend}
    separable_stress = smoke_core.reduce_residual_layers(
        residual,
        stress_diagnostic={"max_additive_interaction_residual": 0.0, "exact_separable": True},
    )
    nonseparable_stress = smoke_core.reduce_residual_layers(
        residual,
        stress_diagnostic={"max_additive_interaction_residual": 1.0, "exact_separable": False},
    )
    assert separable_stress == nonseparable_stress
    assert separable_stress["terminal"] == "STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE"


def test_tdd_evidence_labels_historical_red_and_hashes_fresh_green() -> None:
    output = b"28 passed in 2.50s\n"
    rows = smoke_runner.build_tdd_evidence(
        command="python -m pytest focused.py -q",
        exit_code=0,
        output=output,
        output_artifact="focused-pytest-green.txt",
    )
    red_rows = [row for row in rows if row["phase"].startswith("RED")]
    green = rows[-1]
    assert red_rows and all(row["evidence_level"] == "executor_report_only" for row in red_rows)
    assert green["phase"] == "GREEN_FRESH"
    assert green["evidence_level"] == "fresh_subprocess_output"
    assert green["output_sha256"] == __import__("hashlib").sha256(output).hexdigest()


def test_false_lock_coverage_and_zero_headroom_arithmetic() -> None:
    truth = [(0, 0.0, 0.0), (0, 0.2, 50e6), (0, 0.4, 100e6), (0, -0.2, -50e6)]
    estimates = {
        "B0": [(9, 0.0, 0.0), (9, 0.0, 0.0), truth[2], truth[3]],
        "B1": [truth[0], (9, 0.0, 0.0), truth[2], truth[3]],
        "B2": [truth[0], (9, 0.0, 0.0), truth[2], truth[3]],
        "C": [truth[0], truth[1], truth[2], truth[3]],
    }
    metrics = acquisition_metrics(truth, estimates)
    assert metrics["methods"]["B0"]["false_lock_count"] == 2
    assert metrics["methods"]["B0"]["miss"] is None
    assert metrics["g_c"] == pytest.approx(1.0)
    assert metrics["coverage"]["B1"] == pytest.approx(0.5)
    zero = acquisition_metrics(truth, {name: truth[:] for name in estimates})
    assert zero["g_c"] == 0.0
    assert zero["coverage"]["B1"] is None


def test_stable_2x2_is_axis_adjacent_and_layer_isolated() -> None:
    records = []
    wrong = (8, 0.4, 100e6)
    for layer in ("noiseless", "minus6db"):
        for tau in (-0.2, 0.0):
            for cfo in (-50e6, 0.0):
                records.append({"d": 0, "tau": tau, "cfo_hz": cfo, "layer": layer, "estimate": wrong if layer == "noiseless" else (0, tau, cfo)})
    found = find_stable_2x2(records, tau_grid=(-0.2, 0.0), cfo_grid=(-50e6, 0.0))
    assert found["found"] is True
    assert found["regions"][0]["layer"] == "noiseless"


def test_interaction_residual_distinguishes_additive_surface() -> None:
    additive = np.add.outer(np.arange(3.0), np.arange(4.0))
    coupled = additive.copy()
    coupled[1, 2] += 1.0
    assert additive_interaction_residual(additive) < 1e-14
    assert additive_interaction_residual(coupled) > 0.01


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"semantic_gates_pass": False}, "SEMANTIC_INVALID"),
        ({"complete_population": False}, "STEP4A_PREFLIGHT_EVIDENCE_GAP"),
        ({"b0_false_locks": 0}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"b1_c_equivalent": True}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"exact_separable": True}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"stable_region": False}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"g_c": 0.049}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"coverage_b1": 0.95}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        ({"coverage_b2": 0.95}, "STEP4A_PREFLIGHT_KILL_OR_PIVOT"),
        (
            {"analytic_nonseparable": True, "surface_nonseparable": True, "stable_region": True, "g_c": 0.05, "coverage_b1": 0.94, "coverage_b2": 0.94, "b0_false_locks": 1},
            "STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE",
        ),
    ],
)
def test_terminal_reducer_boundaries(kwargs: dict, expected: str) -> None:
    base = dict(
        semantic_gates_pass=True,
        complete_population=True,
        b0_false_locks=2,
        b1_c_equivalent=False,
        exact_separable=False,
        analytic_nonseparable=True,
        surface_nonseparable=True,
        stable_region=True,
        g_c=0.10,
        coverage_b1=0.50,
        coverage_b2=0.50,
    )
    base.update(kwargs)
    assert reduce_terminal(**base) == expected


def test_output_dir_and_artifact_referential_integrity(tmp_path: Path) -> None:
    allowed = PROBE_DIR / "artifacts"
    assert validate_output_dir(allowed, PROBE_DIR) == allowed.resolve()
    with pytest.raises(ValueError):
        validate_output_dir(tmp_path, PROBE_DIR)
    obs = [{"cell_id": "c1", "realization_id": "r1", "rx_sha256": "h1"}]
    truth = [{"cell_id": "c1"}]
    methods = [{"cell_id": "c1", "realization_id": "r1", "rx_sha256": "h1", "grid_hash": "g", "score_hash": "s", "method": name} for name in ("B0", "B1", "B2", "C")]
    validate_artifact_references(obs, truth, methods)
    with pytest.raises(ValueError):
        validate_artifact_references(obs, truth, methods[:-1])


def test_runner_cli_is_mutually_exclusive_and_identity_is_semantically_valid() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--identity-only", "--run-grid"])
    identity = run_identity(SmokeConfig())
    assert identity["semantic_gates_pass"] is True
    assert identity["estimates"] == {"B0": [0, 0.0, 0.0], "B1": [0, 0.0, 0.0], "B2": [0, 0.0, 0.0], "C": [0, 0.0, 0.0]}
    assert identity["b1_c_equivalent"] is True


def test_report_table_keeps_stress_population_separate_but_complete() -> None:
    values = {"population": 75, "false_lock_count": 0, "false_lock_rate": 0.0, "acquisition_success": 1.0, "miss": None}
    summary = {
        "primary_by_layer": {"noiseless": {"methods": {method: values for method in ("B0", "B1", "B2", "C")}}},
        "stress_metrics_by_method": {
            method: {"population": 30, "false_lock_count": 2, "false_lock_rate": 2 / 30, "acquisition_success": 28 / 30, "miss": None}
            for method in ("B0", "B1", "B2", "C")
        },
    }
    table = _method_table(summary)
    assert "| stress_noiseless | B0 | 2/30 | 0.066667 | 0.933333 |" in table
