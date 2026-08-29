"""T067 preregistered bounded-development tests (test-first)."""

from __future__ import annotations

import importlib
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import yaml


SIM_ROOT = Path(__file__).resolve().parents[1]
SEAM = SIM_ROOT / "explore" / "ch5-apsk-structured-covariance"
for path in (SIM_ROOT, SEAM):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def _modules():
    try:
        reducer = importlib.import_module("development_reducer")
        runner = importlib.import_module("run_development")
    except ModuleNotFoundError as exc:
        pytest.fail(f"T067 development seam is not implemented: {exc}")
    return reducer, runner


def _manifest() -> dict:
    return yaml.safe_load((SEAM / "development_manifest.yaml").read_text(encoding="utf-8"))


def _comparison(gmi_ci, ber_ci, *, gmi=0.01, ber=-0.001):
    return {
        "gmi": {"mean_diff": gmi, "ci": list(gmi_ci), "wins": 20},
        "ber": {"mean_diff": ber, "ci": list(ber_ci), "wins": 20},
    }


def test_manifest_freezes_rounds_splits_grids_and_forbidden_scope():
    manifest = _manifest()
    assert manifest["authority"] == "T067/D048/V022"
    assert manifest["verdict_ceiling"] == "PROVISIONAL"
    assert manifest["round1"]["seeds"] == {"start": 3000, "stop_inclusive": 3063}
    assert manifest["round1"]["tune_window_ids"] == {"start": 0, "stop_inclusive": 31}
    assert manifest["round1"]["evaluation_window_ids"] == {"start": 32, "stop_inclusive": 63}
    assert manifest["round1"]["tuning"]["C1_kappa"] == [0, 1, 4, 16, 64]
    assert manifest["round1"]["tuning"]["B3_shrinkage"] == [0, 0.25, 0.5, 0.75, 1]
    assert [cell["snr_db"] for cell in manifest["round2"]["cells"]] == [14.0, 15.0, 16.0]
    assert "LDPC_or_FER_grid" in manifest["forbidden"]
    assert "third_round" in manifest["forbidden"]
    assert len(manifest["failure_predicates"]) == 7


def test_round1_configs_and_payload_indices_are_exact_and_disjoint():
    _, runner = _modules()
    configs = runner.build_round1_configs(_manifest())
    assert len(configs) == 64
    assert [config.seed for config in configs] == list(range(3000, 3064))
    assert [config.window_id for config in configs] == [f"round1-window-{i:02d}" for i in range(64)]
    pilots = np.arange(0, 256, 4, dtype=np.int64)
    payload = runner.payload_indices(256, pilots)
    assert payload.size == 192
    assert np.intersect1d(pilots, payload).size == 0
    np.testing.assert_array_equal(np.sort(np.concatenate((pilots, payload))), np.arange(256))


def test_bridge_exposes_receiver_observation_without_payload_truth_dependency():
    _, runner = _modules()
    bridge = importlib.import_module("post_ch4_ch3_bridge")
    config = runner.build_round1_configs(_manifest())[0]
    receiver, truth = bridge.generate_correctness_fixture(config, identity_jones=False, noiseless=False)
    arm = runner.frozen_ch4_arm(_manifest())
    first_bundle, first_observation = bridge.run_bridge_with_observation(receiver, arm)
    truth.payload_bits[:] ^= 1
    truth.payload_labels[:] = (truth.payload_labels + 3) % 16
    second_bundle, second_observation = bridge.run_bridge_with_observation(receiver, arm)
    np.testing.assert_array_equal(first_observation, second_observation)
    np.testing.assert_array_equal(first_observation[:, first_bundle.pilot_indices], first_bundle.z_pilot)
    assert first_bundle.bundle_hash == second_bundle.bundle_hash


def test_tuning_uses_only_tune_windows_and_ties_choose_stronger_shrinkage():
    reducer, _ = _modules()
    rows = [
        {"window_id": window_id, "value": value, "gmi": 1.0}
        for window_id in range(64)
        for value in (0.0, 0.25, 0.5, 0.75, 1.0)
    ]
    for row in rows:
        if row["window_id"] >= 32:
            row["gmi"] = 100.0 if row["value"] == 0.0 else -100.0
    selected = reducer.select_tuned_value(
        rows, tune_window_ids=tuple(range(32)), value_key="value", metric_key="gmi", tie_tolerance=1e-12
    )
    assert selected == 1.0


def test_paired_bootstrap_reuses_window_clusters_and_is_reproducible():
    reducer, _ = _modules()
    candidate = np.linspace(0.1, 0.2, 32)
    baseline = candidate - 0.01
    first = reducer.paired_bootstrap_summary(candidate, baseline, seed=2026083002, resamples=2000)
    second = reducer.paired_bootstrap_summary(candidate, baseline, seed=2026083002, resamples=2000)
    assert first == second
    assert first["mean_diff"] == pytest.approx(0.01)
    assert first["ci"][0] > 0.0
    assert first["wins"] == 32


def test_round1_terminal_prefers_c1_only_against_the_strongest_structured_comparator():
    reducer, _ = _modules()
    comparisons = {
        "B2_vs_B1": _comparison((0.001, 0.02), (-0.003, 0.0)),
        "B3_vs_B1": _comparison((0.002, 0.03), (-0.004, -0.0001)),
        "C1_vs_B1": _comparison((0.004, 0.04), (-0.005, -0.0002)),
        "C1_vs_B2": _comparison((0.001, 0.02), (-0.003, 0.0)),
        "C1_vs_B3": _comparison((0.0001, 0.01), (-0.002, 0.0)),
    }
    verdict = reducer.classify_round1(comparisons, strongest_comparator="B3")
    assert verdict == {"terminal": "C1_SIGNAL", "winner": "C1", "strongest_comparator": "B3"}


def test_round1_terminal_routes_simple_gmi_only_and_no_signal_without_round3():
    reducer, _ = _modules()
    neutral = _comparison((-0.01, 0.01), (-0.002, 0.002), gmi=0.0, ber=0.0)
    simple = {
        "B2_vs_B1": _comparison((0.002, 0.02), (-0.003, 0.0)),
        "B3_vs_B1": neutral,
        "C1_vs_B1": neutral,
        "C1_vs_B2": neutral,
        "C1_vs_B3": neutral,
    }
    assert reducer.classify_round1(simple, strongest_comparator="B2")["terminal"] == "SIMPLE_MIGRATION_SIGNAL"
    gmi_only = dict(simple)
    gmi_only["B2_vs_B1"] = _comparison((0.002, 0.02), (-0.001, 0.004))
    assert reducer.classify_round1(gmi_only, strongest_comparator="B2")["terminal"] == "GMI_ONLY_SIGNAL"
    none = {key: neutral for key in simple}
    assert reducer.classify_round1(none, strongest_comparator="B2")["terminal"] == "NO_METHOD_SIGNAL"


def test_provisional_grade_requires_two_of_three_ber_cis_and_gmi_noninferiority():
    reducer, _ = _modules()
    points = [
        {"ber": {"ci": [-0.01, -0.001]}, "gmi": {"ci": [0.001, 0.02]}},
        {"ber": {"ci": [-0.02, -0.002]}, "gmi": {"ci": [-0.001, 0.01]}},
        {"ber": {"ci": [-0.01, 0.002]}, "gmi": {"ci": [0.0, 0.01]}},
    ]
    assert reducer.classify_provisional_grade(points) == "PROVISIONAL_A/B"
    points[1]["ber"]["ci"][1] = 0.001
    assert reducer.classify_provisional_grade(points) == "PROVISIONAL_C"


def test_one_real_window_produces_all_preregistered_arm_rows_with_shared_hashes():
    _, runner = _modules()
    manifest = _manifest()
    window = runner.evaluate_window(
        runner.build_round1_configs(manifest)[0],
        manifest,
        round_name="round1",
        split="tune",
        snr_db=15.0,
    )
    assert len(window["rows"]) == 12
    assert {(row["arm"], row["parameter"]) for row in window["rows"]} == {
        ("B1", None),
        ("B2", None),
        *(("B3", value) for value in [0.0, 0.25, 0.5, 0.75, 1.0]),
        *(("C1", value) for value in [0.0, 1.0, 4.0, 16.0, 64.0]),
    }
    assert window["pilot_symbols_per_polarization"] == 64
    assert window["payload_symbols_per_polarization"] == 192
    assert all(row["payload_bits"] == 1536 for row in window["rows"])
    assert all(0 <= row["bit_errors"] <= row["payload_bits"] for row in window["rows"])
    assert all(np.isfinite(row["gmi"]) and np.isfinite(row["ber"]) for row in window["rows"])
    assert len({window["config_hash"], window["realization_hash"], window["bundle_hash"]}) == 3


def _synthetic_round1_windows():
    windows = []
    for window_id in range(64):
        split = "tune" if window_id < 32 else "evaluation"
        rows = []
        for arm, values in (("B1", [None]), ("B2", [None]), ("B3", [0.0, 0.25, 0.5, 0.75, 1.0]), ("C1", [0.0, 1.0, 4.0, 16.0, 64.0])):
            for value in values:
                base = 2.0
                if arm == "B2":
                    base += 0.02
                elif arm == "B3":
                    base += 0.03 - abs(float(value) - 0.75) * 0.01
                elif arm == "C1":
                    base += 0.05 - abs(float(value) - 16.0) * 0.0001
                rows.append({
                    "arm": arm,
                    "parameter": value,
                    "gmi": base,
                    "ber": 0.1 - (base - 2.0) * 0.5,
                    "bit_errors": int(round((0.1 - (base - 2.0) * 0.5) * 1536)),
                    "payload_bits": 1536,
                    "nll": 1.0 - (base - 2.0),
                    "condition_max": 3.0,
                    "floor_rate": 0.0,
                    "runtime_s": 0.001,
                })
        windows.append({
            "window_id": window_id,
            "window_name": f"round1-window-{window_id:02d}",
            "seed": 3000 + window_id,
            "split": split,
            "snr_db": 15.0,
            "config_hash": "config",
            "realization_hash": f"realization-{window_id}",
            "bundle_hash": f"bundle-{window_id}",
            "pilot_symbols_per_polarization": 64,
            "payload_symbols_per_polarization": 192,
            "per_pol_point_counts": [[4] * 16, [4] * 16],
            "rows": rows,
        })
    return windows


def test_raw_only_round1_reducer_freezes_tuning_and_returns_c1_signal():
    reducer, _ = _modules()
    aggregate = reducer.reduce_round1(_synthetic_round1_windows(), _manifest())
    assert aggregate["tuning"]["C1_kappa"] == 16.0
    assert aggregate["tuning"]["B3_shrinkage"] == 0.75
    assert aggregate["evaluation_windows"] == 32
    assert aggregate["terminal"] == "C1_SIGNAL"
    assert aggregate["winner"] == "C1"
    assert aggregate["comparisons"]["C1_vs_B1"]["gmi"]["ci"][0] > 0.0
    assert aggregate["comparisons"]["C1_vs_B1"]["ber"]["ci"][1] <= 0.0


def test_raw_validator_rejects_split_seed_and_hash_invariant_breaks():
    reducer, _ = _modules()
    windows = _synthetic_round1_windows()
    windows[32] = dict(windows[32], split="tune")
    with pytest.raises(ValueError, match="split"):
        reducer.validate_round1_windows(windows, _manifest())
    windows = _synthetic_round1_windows()
    windows[10] = dict(windows[10], seed=9999)
    with pytest.raises(ValueError, match="seed"):
        reducer.validate_round1_windows(windows, _manifest())
    windows = _synthetic_round1_windows()
    windows[11] = dict(windows[11], realization_hash=windows[10]["realization_hash"])
    with pytest.raises(ValueError, match="realization"):
        reducer.validate_round1_windows(windows, _manifest())
