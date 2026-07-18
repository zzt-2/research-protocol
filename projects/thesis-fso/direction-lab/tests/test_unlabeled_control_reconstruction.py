from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "tools" / "unlabeled_control_reconstruction.py"
spec = importlib.util.spec_from_file_location("unlabeled_control_reconstruction", MODULE_PATH)
detectors = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(detectors)


def _training_data(n: int = 24, d: int = 4):
    rng = np.random.default_rng(13)
    return rng.normal(size=(n, d)), np.repeat(np.arange(n // 4), 4)


def test_public_apis_have_no_event_label_parameter():
    fit_params = list(inspect.signature(detectors.UnlabeledControlReconstructionDetector.fit).parameters)
    threshold_params = list(inspect.signature(detectors.calibrate_unlabeled_cell_threshold).parameters)

    assert fit_params == ["self", "x", "cell_ids"]
    assert threshold_params == ["scores", "cell_ids", "false_alarm_budget"]


def test_fit_and_predict_produce_finite_bounded_scores_without_y():
    x, cell_ids = _training_data()
    detector = detectors.UnlabeledControlReconstructionDetector(seed=7, min_samples=8)

    assert detector.fit(x, cell_ids) is detector
    scores = detector.predict_proba(x)

    assert detector.status == "FIT"
    assert scores is not None
    assert np.all(np.isfinite(scores))
    assert np.all((scores >= 0.0) & (scores <= 1.0))
    with pytest.raises(TypeError):
        detector.fit(x, np.zeros(x.shape[0], dtype=int), cell_ids)


def test_fit_validates_shape_finiteness_and_minimum_samples():
    x, cell_ids = _training_data()
    detector = detectors.UnlabeledControlReconstructionDetector(min_samples=8)

    with pytest.raises(ValueError, match="two-dimensional"):
        detector.fit(x.reshape(-1), cell_ids)
    with pytest.raises(ValueError, match="non-finite"):
        detector.fit(np.vstack([x[:-1], [np.nan] * x.shape[1]]), cell_ids)
    with pytest.raises(ValueError, match="match feature rows"):
        detector.fit(x, cell_ids[:-1])
    assert detector.fit(x[:4], cell_ids[:4]).status == "INCONCLUSIVE"


def test_unlabeled_cell_threshold_uses_cell_maxima_and_budget_boundaries():
    scores = np.array([0.10, 0.20, 0.90, 0.80, 0.30, 0.40, 1.00, 0.70])
    cell_ids = np.repeat(np.arange(4), 2)

    zero = detectors.calibrate_unlabeled_cell_threshold(scores, cell_ids, 0.0)
    quarter = detectors.calibrate_unlabeled_cell_threshold(scores, cell_ids, 0.25)
    one = detectors.calibrate_unlabeled_cell_threshold(scores, cell_ids, 1.0)

    assert zero["status"] == "CALIBRATED"
    assert zero["threshold"] > 1.0
    assert zero["control_false_alarm"] == 0.0
    assert quarter["threshold"] == 1.00
    assert quarter["control_false_alarm"] == 0.25
    assert one["threshold"] == 0.20
    assert one["control_false_alarm"] == 1.0


def test_unlabeled_threshold_never_exceeds_budget_when_boundary_scores_tie():
    scores = np.array([0.90, 0.90, 0.40, 0.20])
    cell_ids = np.arange(4)

    result = detectors.calibrate_unlabeled_cell_threshold(scores, cell_ids, 0.25)

    assert result["allowed_false_alarm_cells"] == 1
    assert result["control_false_alarm"] <= 0.25
    assert result["threshold"] > 0.90


def test_unlabeled_threshold_is_deterministic_and_validates_inputs():
    scores = np.array([0.1, 0.2, 0.3, 0.4])
    cells = np.array([0, 0, 1, 1])

    first = detectors.calibrate_unlabeled_cell_threshold(scores, cells, 0.5)
    second = detectors.calibrate_unlabeled_cell_threshold(scores.copy(), cells.copy(), 0.5)
    assert first == second

    with pytest.raises(ValueError, match=r"\[0,1\]"):
        detectors.calibrate_unlabeled_cell_threshold(scores, cells, -0.1)
    with pytest.raises(ValueError, match="non-finite"):
        detectors.calibrate_unlabeled_cell_threshold([0.1, np.inf], [0, 1], 0.5)
    with pytest.raises(ValueError, match="match feature rows"):
        detectors.calibrate_unlabeled_cell_threshold(scores, cells[:-1], 0.5)
