"""Unlabeled control-domain reconstruction detector and calibration.

The entire supplied training matrix is the reference domain.  No event labels,
BER values, channel state, or symbols are accepted by either public API.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


EPS = 1e-8


def _matrix(x) -> np.ndarray:
    result = np.asarray(x, dtype=float)
    if result.ndim != 2:
        raise ValueError("feature matrix must be two-dimensional")
    if result.shape[0] == 0 or result.shape[1] == 0:
        raise ValueError("feature matrix must be non-empty")
    if not np.all(np.isfinite(result)):
        raise ValueError("feature matrix contains non-finite values")
    return result


def _cells(cell_ids, n: int) -> np.ndarray:
    result = np.asarray(cell_ids).reshape(-1)
    if result.size != n:
        raise ValueError("cell_ids must match feature rows")
    if result.size == 0:
        raise ValueError("cell_ids must be non-empty")
    return result


@dataclass
class _Scaler:
    mean: np.ndarray | None = None
    scale: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> "_Scaler":
        self.mean = np.mean(x, axis=0)
        self.scale = np.std(x, axis=0)
        self.scale = np.where(self.scale > EPS, self.scale, 1.0)
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean is None or self.scale is None:
            raise RuntimeError("scaler is not fitted")
        return (np.asarray(x, dtype=float) - self.mean) / self.scale


class UnlabeledControlReconstructionDetector:
    """Deterministic undercomplete reconstruction detector trained on all rows."""

    status = "UNFIT"

    def __init__(self, seed: int = 0, min_samples: int = 8):
        self.seed = int(seed)
        self.min_samples = int(min_samples)
        if self.min_samples < 1:
            raise ValueError("min_samples must be positive")
        self.scaler = _Scaler()
        self.scaler_mean_: np.ndarray | None = None

    def fit(self, x, cell_ids):
        x = _matrix(x)
        _cells(cell_ids, x.shape[0])
        if x.shape[0] < self.min_samples:
            self.status = "INCONCLUSIVE"
            return self

        self.scaler.fit(x)
        self.scaler_mean_ = self.scaler.mean.copy()
        z = self.scaler.transform(x)
        n, d = z.shape
        hidden = max(1, min(8, d // 2 if d > 1 else 1))
        rng = np.random.default_rng(self.seed)
        w1 = rng.normal(0.0, 0.1, size=(d, hidden))
        b1 = np.zeros(hidden)
        w2 = rng.normal(0.0, 0.1, size=(hidden, d))
        b2 = np.zeros(d)
        for _ in range(320):
            h = np.tanh(z @ w1 + b1)
            recon = h @ w2 + b2
            err = (recon - z) / n
            grad_w2 = h.T @ err + 1e-3 * w2
            grad_b2 = np.sum(err, axis=0)
            grad_h = (err @ w2.T) * (1.0 - h * h)
            grad_w1 = z.T @ grad_h + 1e-3 * w1
            w2 -= 0.04 * grad_w2
            b2 -= 0.04 * grad_b2
            w1 -= 0.04 * grad_w1
            b1 -= 0.04 * np.sum(grad_h, axis=0)
        clean_error = np.mean((np.tanh(z @ w1 + b1) @ w2 + b2 - z) ** 2, axis=1)
        self.w1_, self.b1_, self.w2_, self.b2_ = w1, b1, w2, b2
        self.error_scale_ = max(float(np.median(clean_error) + 3.0 * np.std(clean_error)), 1e-6)
        self.status = "FIT"
        return self

    def predict_proba(self, x):
        if self.status != "FIT":
            return None
        z = self.scaler.transform(_matrix(x))
        recon = np.tanh(z @ self.w1_ + self.b1_) @ self.w2_ + self.b2_
        error = np.mean((recon - z) ** 2, axis=1)
        scores = 1.0 - np.exp(-error / self.error_scale_)
        return np.clip(np.nan_to_num(scores, nan=1.0, posinf=1.0, neginf=0.0), 0.0, 1.0)


def calibrate_unlabeled_cell_threshold(scores, cell_ids, false_alarm_budget):
    """Calibrate from cell-level maxima using scores and cell IDs only."""
    scores = np.asarray(scores, dtype=float).reshape(-1)
    if scores.size == 0:
        raise ValueError("scores must be non-empty")
    if not np.all(np.isfinite(scores)):
        raise ValueError("scores contain non-finite values")
    cell_ids = _cells(cell_ids, scores.size)
    if not 0.0 <= float(false_alarm_budget) <= 1.0:
        raise ValueError("false_alarm_budget must be in [0,1]")
    maxima = np.asarray([np.max(scores[cell_ids == cell]) for cell in np.unique(cell_ids)], dtype=float)
    allowed = int(np.floor(float(false_alarm_budget) * maxima.size + 1e-12))
    ordered = np.sort(maxima)
    if allowed >= ordered.size:
        threshold = float(ordered[0])
    elif allowed == 0:
        threshold = float(np.nextafter(ordered[-1], np.inf))
    else:
        boundary = float(ordered[-allowed])
        if int(np.count_nonzero(maxima >= boundary)) > allowed:
            threshold = float(np.nextafter(boundary, np.inf))
        else:
            threshold = boundary
    control_false_alarm = float(np.mean(maxima >= threshold))
    return {
        "status": "CALIBRATED",
        "threshold": threshold,
        "control_false_alarm": control_false_alarm,
        "control_cell_count": int(maxima.size),
        "allowed_false_alarm_cells": allowed,
    }
