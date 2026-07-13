"""Unit tests for the PROMPT-012 S005 divergence audit helpers."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "explore" / "cma-fade-divergence"
)
sys.path.insert(0, str(SCRIPT_DIR))

from prompt012_divergence_audit import (  # noqa: E402
    build_payload,
    classify_outputs,
    divergence_reasons,
    dual_ber_metrics,
    run_grid,
    summarize_grid,
    validate_divergence_consistency,
)


def _qpsk(values):
    return np.asarray(values, dtype=complex) / np.sqrt(2)


def test_dual_ber_metrics_removes_output_swap_but_preserves_fixed_metric():
    sx = _qpsk([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j] * 16)
    sy = _qpsk([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j] * 16)

    metrics = dual_ber_metrics(sy, sx, sx, sy)

    assert metrics["fixed_ber"]["mean"] > 0.2
    assert metrics["pi_ber"]["mean"] == 0.0
    assert metrics["pi_ber"]["assignment"] == ["Y", "X"]


def test_classification_distinguishes_normal_swap_same_source_collapse_and_mixed():
    sx = _qpsk([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j] * 64)
    sy = _qpsk([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j] * 64)
    noise = np.random.default_rng(4).standard_normal(len(sx)) + 1j * np.random.default_rng(5).standard_normal(len(sx))

    assert classify_outputs(sx, sy, sx, sy)["classification"] == "normal"
    assert classify_outputs(sy, sx, sx, sy)["classification"] == "swap"
    assert classify_outputs(sx, sx, sx, sy)["classification"] == "same-source"
    assert classify_outputs(noise, noise[::-1], sx, sy)["classification"] == "collapse"
    assert classify_outputs(sx + sy, sx - sy, sx, sy)["classification"] == "mixed"


def test_divergence_reasons_are_threshold_based_and_not_ber_based():
    assert divergence_reasons(15.0, 1.0, 2.0) == ["norm>10x"]
    assert divergence_reasons(1.0, 1.0, 1001.0) == ["zamp>1e3"]
    assert divergence_reasons(float("nan"), 1.0, 1.0) == ["nonfinite"]
    assert divergence_reasons(1.0, 1.0, 1.0) == []


def test_grid_summary_excludes_diverged_trials_from_ber_and_classification():
    trials = [
        {
            "diverged": False,
            "classification": "swap",
            "fixed_ber": {"mean": 0.49},
            "pi_ber": {"mean": 0.02},
            "divergence_reasons": [],
        },
        {
            "diverged": True,
            "classification": None,
            "fixed_ber": None,
            "pi_ber": None,
            "divergence_reasons": ["norm>10x"],
        },
    ]

    summary = summarize_grid(trials)

    assert summary["p_div"] == 0.5
    assert summary["n_ber_trials"] == 1
    assert summary["fixed_ber"]["mean"] == 0.49
    assert summary["pi_ber"]["mean"] == 0.02
    assert summary["classification_counts"]["swap"] == 1
    assert summary["divergence_reason_counts"]["norm>10x"] == 1


def test_divergence_flag_must_match_independently_inferred_reasons():
    validate_divergence_consistency(True, ["norm>10x"])
    validate_divergence_consistency(False, [])
    with pytest.raises(RuntimeError, match="divergence inconsistency"):
        validate_divergence_consistency(True, [])
    with pytest.raises(RuntimeError, match="divergence inconsistency"):
        validate_divergence_consistency(False, ["zamp>1e3"])


def test_payload_records_frozen_channel_parameters():
    payload = build_payload([], [1000], 5_000_000, 1.5, 0.8)

    assert payload["parameters"]["gamma_bar"] == 100.0
    assert payload["parameters"]["T_S"] == 4e-10
    assert payload["parameters"]["channel_block"] == 100


def test_payload_records_current_script_sha256():
    script_path = SCRIPT_DIR / "prompt012_divergence_audit.py"
    expected = hashlib.sha256(script_path.read_bytes()).hexdigest()

    payload = build_payload([], [1000], 5_000_000, 1.5, 0.8)

    assert payload["script_sha256"] == expected


def test_run_grid_uses_the_same_requested_seeds_and_summarizes_synthetic_trials():
    seen = []

    def fake_trial(alpha, beta, f_g, mu, seed, n_symbols):
        seen.append((alpha, beta, f_g, mu, seed, n_symbols))
        return {
            "seed": seed,
            "diverged": False,
            "classification": "normal",
            "fixed_ber": {"mean": seed / 10_000},
            "pi_ber": {"mean": seed / 20_000},
            "divergence_reasons": [],
        }

    grid = run_grid(1.5, 0.8, 100.0, 1e-3, [1000, 1001], 128,
                    trial_fn=fake_trial)

    assert [item[4] for item in seen] == [1000, 1001]
    assert [trial["seed"] for trial in grid["trials"]] == [1000, 1001]
    assert grid["summary"]["n_trials"] == 2
    assert grid["summary"]["n_ber_trials"] == 2
