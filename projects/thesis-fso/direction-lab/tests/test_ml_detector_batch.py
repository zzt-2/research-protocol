from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).parents[1] / "tools" / "ml_detector_batch.py"
spec = importlib.util.spec_from_file_location("ml_detector_batch", MODULE_PATH)
ml = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ml)


def test_trace_features_are_causal_and_include_required_statistics():
    trace = {
        "cm_error": np.array([1.0, 2.0, 4.0, 8.0]),
        "output_power": np.array([1.0, 1.0, 2.0, 2.0]),
        "update_norm": np.array([0.5, 0.25, 0.125, 0.0625]),
    }
    x, names = ml.build_trace_features(trace, window=2)
    assert x.shape == (4, 12)
    assert {"cm_error_log", "cm_error_delta", "cm_error_roll_mean", "cm_error_roll_std"}.issubset(names)
    # Changing the future must not change features at t=1.
    changed = {k: v.copy() for k, v in trace.items()}
    for value in changed.values():
        value[2:] = 999.0
    x_changed, _ = ml.build_trace_features(changed, window=2)
    np.testing.assert_allclose(x[:2], x_changed[:2])


def test_supervised_candidates_are_deterministic_and_return_probabilities():
    rng = np.random.default_rng(7)
    x = rng.normal(size=(80, 4))
    y = (x[:, 0] + 0.5 * x[:, 1] > 0.7).astype(int)
    cells = np.repeat(np.arange(20), 4)
    candidates = ml.fit_candidates(x[:60], y[:60], cells[:60], seed=11)
    for name in ("logistic", "mlp", "autoencoder"):
        detector = candidates[name]
        assert detector.status == "FIT"
        scores1 = detector.predict_proba(x[60:])
        scores2 = ml.fit_candidates(x[:60], y[:60], cells[:60], seed=11)[name].predict_proba(x[60:])
        assert np.all(np.isfinite(scores1))
        assert np.all((scores1 >= 0.0) & (scores1 <= 1.0))
        np.testing.assert_allclose(scores1, scores2)


def test_autoencoder_uses_clean_training_samples_only():
    x = np.zeros((12, 3), dtype=float)
    y = np.zeros(12, dtype=int)
    x[0] = 100.0
    y[0] = 1
    cells = np.arange(12)
    detector = ml.CleanReconstructionDetector(seed=2).fit(x, y, cells)
    assert detector.status == "FIT"
    assert detector.clean_train_count == 11
    assert detector.scaler_mean_[0] == 0.0
    assert detector.predict_proba(np.array([[100.0, 0.0, 0.0]]))[0] > detector.predict_proba(np.zeros((1, 3)))[0]


def test_threshold_uses_cell_level_control_false_alarm_budget():
    scores = np.array([0.1, 0.9, 0.8, 0.2, 0.7, 0.6])
    labels = np.array([0, 0, 1, 0, 1, 0])
    cells = np.array([0, 0, 1, 1, 2, 2])
    result = ml.calibrate_threshold(scores, labels, cells, control_false_alarm_budget=0.0)
    assert result["status"] == "CALIBRATED"
    assert result["control_false_alarm"] == 0.0
    assert result["threshold"] > 0.9


def test_threshold_selection_does_not_use_event_scores_or_labels():
    labels = np.array([0, 0, 0, 0, 1, 1])
    cells = np.array([0, 0, 1, 1, 2, 2])
    scores_a = np.array([0.1, 0.2, 0.3, 0.4, 0.9, 0.8])
    scores_b = np.array([0.1, 0.2, 0.3, 0.4, 0.05, 0.06])
    a = ml.calibrate_threshold(scores_a, labels, cells, control_false_alarm_budget=1.0)
    b = ml.calibrate_threshold(scores_b, labels, cells, control_false_alarm_budget=1.0)
    assert a["threshold"] == b["threshold"]


def test_metrics_include_auc_recall_lead_and_ece_without_sklearn():
    scores = np.array([0.05, 0.2, 0.8, 0.9, 0.1, 0.7])
    labels = np.array([0, 0, 1, 1, 0, 1])
    cells = np.array([0, 0, 1, 1, 2, 2])
    threshold = 0.75
    metrics = ml.evaluate_scores(scores, labels, cells, threshold)
    assert 0.0 <= metrics["block_auroc"] <= 1.0
    assert 0.0 <= metrics["block_auprc"] <= 1.0
    assert 0.0 <= metrics["cell_event_recall_before_or_at_oracle"] <= 1.0
    assert metrics["control_false_alarm"] == 0.0
    assert metrics["lead_blocks"] >= 0.0
    assert 0.0 <= metrics["ece"] <= 1.0


def test_event_and_alarm_require_persistent_two_block_runs():
    # Cell 0 has an isolated positive label and isolated alarm score: it is
    # still a control cell. Cell 1 has a persistent event and persistent alarm.
    scores = np.array([0.95, 0.1, 0.2, 0.9, 0.85])
    labels = np.array([0, 1, 0, 1, 1])
    cells = np.array([0, 0, 1, 1, 1])
    metrics = ml.evaluate_scores(scores, labels, cells, 0.75, persistence_blocks=2)
    assert metrics["event_cells"] == 1
    assert metrics["control_cells"] == 1
    assert metrics["cell_event_recall_before_or_at_oracle"] == 1.0
    assert metrics["control_false_alarm"] == 0.0
    assert metrics["lead_blocks"] == 0.0


def test_insufficient_training_returns_inconclusive_without_metrics():
    x = np.ones((5, 2))
    y = np.zeros(5, dtype=int)
    cells = np.arange(5)
    detector = ml.LogisticDetector(seed=1).fit(x, y, cells)
    assert detector.status == "INCONCLUSIVE"
    assert detector.predict_proba(x) is None
