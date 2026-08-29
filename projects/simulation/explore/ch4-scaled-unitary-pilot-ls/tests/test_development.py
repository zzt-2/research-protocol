from __future__ import annotations

import importlib.util
import inspect
import subprocess
import sys
from pathlib import Path

import numpy as np


SEAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SEAM))


def _load(name: str):
    path = SEAM / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"t069_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_balanced_pilot_gram_is_exactly_frozen():
    d = _load("development")
    for n_pilots in (2, 4):
        x = d.balanced_pilots(n_pilots)
        assert np.array_equal(x @ x.conj().T, n_pilots * np.eye(2))


def test_realization_is_seed_deterministic_and_changes_across_seeds():
    d = _load("development")
    first = d.make_realization(14.0, 2, 6000, 64)
    replay = d.make_realization(14.0, 2, 6000, 64)
    other = d.make_realization(14.0, 2, 6001, 64)

    assert first["realization_hash"] == replay["realization_hash"]
    assert first["observation_hash"] == replay["observation_hash"]
    assert first["realization_hash"] != other["realization_hash"]
    assert first["observation_hash"] != other["observation_hash"]


def test_development_imports_in_standalone_script_context():
    command = (
        "import sys; "
        f"sys.path.insert(0, {str(SEAM)!r}); "
        "import development; print(development.__file__)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", command],
        cwd=SEAM.parents[3],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr


def test_receiver_ladder_is_observation_only_and_zero_regularization_matches_ls():
    d = _load("development")
    realization = d.make_realization(18.0, 4, 6300, 64)
    signature = tuple(inspect.signature(d.receiver_action).parameters)
    assert signature == ("arm", "x_pilots", "y_pilots", "y_payload", "parameter")

    b0 = d.receiver_action(
        "B0", realization["x_pilots"], realization["y_pilots"], realization["y_payload"], None
    )
    b1 = d.receiver_action(
        "B1", realization["x_pilots"], realization["y_pilots"], realization["y_payload"], 0.0
    )
    b2 = d.receiver_action(
        "B2", realization["x_pilots"], realization["y_pilots"], realization["y_payload"], 0.0
    )
    assert np.allclose(b0.w, b1.w, atol=2e-12)
    assert np.allclose(b0.w, b2.w, atol=2e-12)
    assert np.allclose(b0.z, b1.z, atol=2e-12)
    assert np.allclose(b0.z, b2.z, atol=2e-12)


def test_truth_changes_only_offline_scoring_not_deployable_action():
    d = _load("development")
    realization = d.make_realization(14.0, 2, 6002, 64)
    action = d.receiver_action(
        "C4",
        realization["x_pilots"],
        realization["y_pilots"],
        realization["y_payload"],
        None,
    )
    before = d.action_bytes(action)
    score_a = d.score_action(action, realization["bits"], realization["h_true"])
    score_b = d.score_action(action, realization["bits"], 1.3 * realization["h_true"])

    assert before == d.action_bytes(action)
    assert score_a["bit_errors"] == score_b["bit_errors"]
    assert score_a["channel_nmse"] != score_b["channel_nmse"]


def test_tune_selection_uses_pooled_ber_and_stronger_exact_tie():
    r = _load("development_reducer")
    rows = [
        {"parameter": 0.0, "bit_errors": 2, "payload_bits": 100},
        {"parameter": 0.0, "bit_errors": 0, "payload_bits": 10},
        {"parameter": 1.0, "bit_errors": 1, "payload_bits": 100},
        {"parameter": 1.0, "bit_errors": 1, "payload_bits": 10},
    ]
    assert r.select_tuned_parameter(rows, [0.0, 1.0]) == 1.0
    tied = [
        {"parameter": value, "bit_errors": 1, "payload_bits": 100}
        for value in (0.0, 1.0)
    ]
    assert r.select_tuned_parameter(tied, [0.0, 1.0]) == 1.0


def test_paired_bootstrap_is_deterministic_and_candidate_minus_baseline():
    r = _load("development_reducer")
    candidate = [0.01, 0.02, 0.03, 0.04]
    baseline = [0.02, 0.03, 0.04, 0.05]
    first = r.paired_bootstrap(candidate, baseline, seed=2026083003, resamples=2000)
    second = r.paired_bootstrap(candidate, baseline, seed=2026083003, resamples=2000)
    assert first == second
    assert np.isclose(first["mean_diff"], -0.01)
    assert first["ci_upper"] < 0.0
