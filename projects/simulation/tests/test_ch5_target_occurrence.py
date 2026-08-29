"""T066 preregistered single-cell occurrence and reducer tests."""

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


bridge = importlib.import_module("post_ch4_ch3_bridge")
metrics = importlib.import_module("codec_metrics")


def _manifest() -> dict:
    return yaml.safe_load((SEAM / "occurrence_manifest.yaml").read_text(encoding="utf-8"))


def _occurrence():
    return importlib.import_module("occurrence_reducer")


def _t066_config(**overrides):
    manifest = _manifest()
    cell = manifest["cell"]
    pilot_indices = tuple(manifest["ch3"]["pilot_indices"])
    base = bridge.BridgeConfig.correctness_fixture(
        seed=2000,
        n_symbols=cell["observation_symbols"],
        observation_stop=cell["observation_symbols"],
        snr_db=cell["snr_db"],
        turbulence_alpha=cell["turbulence_alpha"],
        turbulence_beta=cell["turbulence_beta"],
        gamma_gamma_block=cell["gamma_gamma_block"],
        f_residual_hz=cell["residual_frequency_hz"],
        f_dot_hz_per_s=cell["frequency_slope_hz_per_s"],
        linewidth_hz=cell["linewidth_hz"],
        ch4_pilot_count=manifest["ch4"]["acquisition_pilots"],
        pilot_indices=pilot_indices,
        pilot_label_shift=manifest["ch3"]["polarization_1_label_shift"],
        cell_id=cell["cell_id"],
        window_id="window-00",
        config_id="t066.target-residual-occurrence.v1",
        source_id="T066/D047/V021",
    )
    return replace(base, **overrides)


def test_manifest_freezes_the_only_authorized_cell_and_terminal_rules():
    manifest = _manifest()

    assert manifest["authority"] == "T066/D047/V021"
    assert manifest["windows"] == {
        "count": 64,
        "seeds": {"start": 2000, "stop_inclusive": 2063},
        "calibration": {"start": 0, "stop_inclusive": 31},
        "evaluation": {"start": 32, "stop_inclusive": 63},
        "independent_windows": True,
        "continuous_acquisition_observation_within_window": True,
    }
    assert manifest["bootstrap"] == {
        "cluster": "evaluation_window",
        "evaluation_clusters": 32,
        "rng": "PCG64",
        "seed": 2026083001,
        "resamples": 2000,
        "confidence": 0.95,
    }
    assert manifest["forbidden"] == [
        "second_cell",
        "parameter_tuning",
        "new_impairment",
        "ldpc_or_fer",
        "performance_grid",
        "C5-1_method_conclusion",
        "skill_or_controller_change",
        "thesis_body_change",
    ]


def test_bridge_constructs_exact_spacing_four_balanced_known_pilots():
    receiver, _ = bridge.generate_correctness_fixture(
        _t066_config(), identity_jones=True, noiseless=True
    )
    expected_indices = np.arange(0, 256, 4, dtype=np.int64)

    np.testing.assert_array_equal(receiver.pilot_indices, expected_indices)
    assert receiver.pilot_indices.size == 64
    for pol in range(2):
        np.testing.assert_array_equal(
            np.bincount(receiver.pilot_labels[pol], minlength=16),
            np.full(16, 4),
        )
        np.testing.assert_array_equal(
            receiver.pilot_symbols[pol],
            metrics.apsk16_table()[0][receiver.pilot_labels[pol]],
        )
        np.testing.assert_array_equal(
            np.flatnonzero(receiver.known_mask[pol]), expected_indices
        )


def test_runner_builds_exactly_64_frozen_configs_without_seed_or_window_mixup():
    runner = importlib.import_module("run_occurrence_smoke")
    manifest = runner.load_occurrence_manifest()
    configs = runner.build_occurrence_configs(manifest)

    assert len(configs) == 64
    assert [config.seed for config in configs] == list(range(2000, 2064))
    assert [config.window_id for config in configs] == [
        f"window-{index:02d}" for index in range(64)
    ]
    assert len({runner.frozen_config_hash(config) for config in configs}) == 1
    frozen = [replace(config, seed=0, window_id="window") for config in configs]
    assert all(config == frozen[0] for config in frozen)
    assert configs[0].scope == (
        "SINGLE_PREREGISTERED_CELL",
        "OCCURRENCE_ONLY",
        "NO_METHOD_OR_PERFORMANCE_CLAIM",
    )


def test_bootstrap_samples_evaluation_windows_as_clusters_and_is_reproducible():
    occurrence = _occurrence()
    first = occurrence.cluster_bootstrap_indices(
        n_clusters=32, resamples=2000, seed=2026083001
    )
    second = occurrence.cluster_bootstrap_indices(
        n_clusters=32, resamples=2000, seed=2026083001
    )

    assert first.shape == (2000, 32)
    assert first.dtype == np.int64
    assert first.min() >= 0 and first.max() < 32
    np.testing.assert_array_equal(first, second)


def test_calibration_fit_is_unchanged_when_only_evaluation_residuals_change():
    occurrence = _occurrence()
    windows = occurrence.synthetic_unit_windows(seed=17, anisotropic=True)
    changed = list(windows)
    for index in range(32, 64):
        changed[index] = replace(
            changed[index], e=changed[index].e * (9.0 - 4.0j)
        )

    original_fit = occurrence.fit_calibration_covariances(
        windows, calibration_window_ids=tuple(range(32)), floor=1e-10
    )
    changed_fit = occurrence.fit_calibration_covariances(
        changed, calibration_window_ids=tuple(range(32)), floor=1e-10
    )

    for name in ("b1", "full"):
        np.testing.assert_array_equal(original_fit[name], changed_fit[name])


def test_reducer_rejects_calibration_evaluation_overlap():
    occurrence = _occurrence()
    windows = occurrence.synthetic_unit_windows(seed=19, anisotropic=False)

    with pytest.raises(ValueError, match="disjoint"):
        occurrence.reduce_occurrence(
            windows,
            calibration_window_ids=tuple(range(32)),
            evaluation_window_ids=tuple(range(31, 63)),
            floor=1e-10,
            bootstrap_seed=2026083001,
            bootstrap_resamples=2000,
        )


def test_synthetic_anisotropic_unit_fixture_has_expected_signs_and_detectable_terminal():
    occurrence = _occurrence()
    windows = occurrence.synthetic_unit_windows(seed=23, anisotropic=True)

    result = occurrence.reduce_occurrence(
        windows,
        calibration_window_ids=tuple(range(32)),
        evaluation_window_ids=tuple(range(32, 64)),
        floor=1e-10,
        bootstrap_seed=2026083001,
        bootstrap_resamples=2000,
    )

    assert result["terminal"] == "DETECTABLE_OCCURRENCE"
    assert all(group["estimate"] > 0.0 for group in result["d1"].values())
    assert all(group["estimate"] > 0.0 for group in result["d2"].values())
    assert result["d3"]["estimate"] > 0.0
    assert result["d3"]["ci"][0] > 0.0
    assert result["bootstrap"] == {
        "cluster": "evaluation_window",
        "seed": 2026083001,
        "resamples": 2000,
        "evaluation_clusters": 32,
    }


def test_group_point_counts_include_only_the_named_ring():
    occurrence = _occurrence()
    result = occurrence.reduce_occurrence(
        occurrence.synthetic_unit_windows(seed=29, anisotropic=False),
        calibration_window_ids=tuple(range(32)),
        evaluation_window_ids=tuple(range(32, 64)),
        floor=1e-10,
        bootstrap_seed=2026083001,
        bootstrap_resamples=2000,
    )

    for name in ("pol0_inner", "pol1_inner"):
        assert result["d1"][name]["point_counts"] == [128] * 8 + [0] * 8
    for name in ("pol0_outer", "pol1_outer"):
        assert result["d1"][name]["point_counts"] == [0] * 8 + [128] * 8


def test_report_renders_group_point_counts_and_per_window_sample_counts():
    occurrence = _occurrence()
    runner = importlib.import_module("run_occurrence_smoke")
    aggregate = occurrence.reduce_occurrence(
        occurrence.synthetic_unit_windows(seed=31, anisotropic=True),
        calibration_window_ids=tuple(range(32)),
        evaluation_window_ids=tuple(range(32, 64)),
        floor=1e-10,
        bootstrap_seed=2026083001,
        bootstrap_resamples=2000,
    )
    receipt = {
        "terminal": aggregate["terminal"],
        "completed_windows": 64,
        "bounded_development_allowed": True,
        "manifest_hash": "manifest",
        "config_hash": "config",
        "unique_realization_hashes": 64,
        "unique_bundle_hashes": 64,
        "unique_next_step": "next",
    }

    report = runner._report_markdown(aggregate, receipt)

    assert "每个 evaluation window 每组样本数：`32`" in report
    assert "pol0_inner point_counts：`[128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0]`" in report


def test_terminal_logic_requires_ci_exclusion_not_point_estimate_sign():
    occurrence = _occurrence()
    neutral_groups = {
        name: {"estimate": 0.2, "ci": [-0.1, 0.3]}
        for name in ("pol0_inner", "pol0_outer", "pol1_inner", "pol1_outer")
    }

    assert occurrence.classify_terminal(neutral_groups, neutral_groups, [-0.2, 0.0]) == (
        "NO_DETECTABLE_OCCURRENCE"
    )
    detectable = {name: dict(value) for name, value in neutral_groups.items()}
    detectable["pol1_outer"] = {"estimate": -0.2, "ci": [-0.4, -0.01]}
    assert occurrence.classify_terminal(detectable, neutral_groups, [-0.2, 0.0]) == (
        "DETECTABLE_OCCURRENCE"
    )
    assert occurrence.classify_terminal(neutral_groups, neutral_groups, [0.001, 0.02]) == (
        "DETECTABLE_OCCURRENCE"
    )
