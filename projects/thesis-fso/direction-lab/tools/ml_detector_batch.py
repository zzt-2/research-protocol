"""Deterministic ML-assisted event detectors for Direction Lab B001.

The module deliberately has no simulator or canonical-baseline side effects.  It
consumes receiver/CMA block features and returns scores only; thresholding and
evaluation are explicit, cell-aware operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


EPS = 1e-8
REQUIRED_TRACE_KEYS = ("cm_error", "output_power", "update_norm")


def build_trace_features(trace: Mapping[str, Sequence[float]], window: int = 8):
    """Build causal log/delta/rolling features from receiver traces.

    Every rolling statistic uses ``[max(0,t-window+1), t]`` only.  No future
    sample is consulted, which makes the same function valid for online use.
    """
    if window < 1:
        raise ValueError("window must be positive")
    arrays = {}
    n = None
    for key in REQUIRED_TRACE_KEYS:
        if key not in trace:
            raise ValueError(f"missing required trace key: {key}")
        value = np.asarray(trace[key], dtype=float).reshape(-1)
        if n is None:
            n = value.size
        if value.size != n:
            raise ValueError("trace arrays must have equal length")
        arrays[key] = value
    if n is None or n == 0:
        return np.empty((0, 12), dtype=float), [f"{k}_{s}" for k in REQUIRED_TRACE_KEYS for s in ("log", "delta", "roll_mean", "roll_std")]

    columns, names = [], []
    for key in REQUIRED_TRACE_KEYS:
        log_value = np.log(np.abs(arrays[key]) + EPS)
        delta = np.diff(log_value, prepend=log_value[0])
        roll_mean = np.empty(n, dtype=float)
        roll_std = np.empty(n, dtype=float)
        for t in range(n):
            segment = log_value[max(0, t - window + 1) : t + 1]
            roll_mean[t] = float(np.mean(segment))
            roll_std[t] = float(np.std(segment))
        columns.extend((log_value, delta, roll_mean, roll_std))
        names.extend((f"{key}_log", f"{key}_delta", f"{key}_roll_mean", f"{key}_roll_std"))
    return np.column_stack(columns), names


@dataclass
class _Scaler:
    mean: np.ndarray | None = None
    scale: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> "_Scaler":
        x = _matrix(x)
        self.mean = np.mean(x, axis=0)
        self.scale = np.std(x, axis=0)
        self.scale = np.where(self.scale > EPS, self.scale, 1.0)
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean is None or self.scale is None:
            raise RuntimeError("scaler is not fitted")
        return (np.asarray(x, dtype=float) - self.mean) / self.scale


def _matrix(x: np.ndarray) -> np.ndarray:
    result = np.asarray(x, dtype=float)
    if result.ndim != 2:
        raise ValueError("feature matrix must be two-dimensional")
    if result.shape[0] == 0 or result.shape[1] == 0:
        raise ValueError("feature matrix must be non-empty")
    if not np.all(np.isfinite(result)):
        raise ValueError("feature matrix contains non-finite values")
    return result


def _labels(y: np.ndarray, n: int) -> np.ndarray:
    result = np.asarray(y, dtype=int).reshape(-1)
    if result.size != n or not np.all(np.isin(result, (0, 1))):
        raise ValueError("labels must be binary and match feature rows")
    return result


def _cells(cell_ids: np.ndarray, n: int) -> np.ndarray:
    result = np.asarray(cell_ids).reshape(-1)
    if result.size != n:
        raise ValueError("cell_ids must match feature rows")
    return result


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -40.0, 40.0)
    return 1.0 / (1.0 + np.exp(-x))


class _Detector:
    status = "UNFIT"

    def __init__(self, seed: int = 0, min_samples: int = 8):
        self.seed = int(seed)
        self.min_samples = int(min_samples)
        self.scaler = _Scaler()
        self.scaler_mean_: np.ndarray | None = None

    def _inconclusive(self):
        self.status = "INCONCLUSIVE"
        return self

    def _prepare(self, x, y, cell_ids):
        x = _matrix(x)
        y = _labels(y, x.shape[0])
        _cells(cell_ids, x.shape[0])
        if x.shape[0] < self.min_samples or np.unique(y).size < 2:
            return x, y, False
        return x, y, True

    def _fit_scaler(self, x):
        self.scaler.fit(x)
        self.scaler_mean_ = self.scaler.mean.copy()

    def predict_proba(self, x):
        if self.status != "FIT":
            return None
        return np.asarray(self._predict_scaled(self.scaler.transform(_matrix(x))), dtype=float)


class LogisticDetector(_Detector):
    """Class-balanced supervised logistic linear detector."""

    def fit(self, x, y, cell_ids):
        x, y, ok = self._prepare(x, y, cell_ids)
        if not ok:
            return self._inconclusive()
        self._fit_scaler(x)
        z = self.scaler.transform(x)
        n, d = z.shape
        rng = np.random.default_rng(self.seed)
        w = rng.normal(0.0, 0.01, size=d)
        b = 0.0
        counts = np.bincount(y, minlength=2).astype(float)
        weights = np.where(y == 1, n / (2.0 * max(counts[1], 1.0)), n / (2.0 * max(counts[0], 1.0)))
        for _ in range(350):
            p = _sigmoid(z @ w + b)
            err = (p - y) * weights
            w -= 0.08 * ((z.T @ err) / n + 1e-3 * w)
            b -= 0.08 * float(np.mean(err))
        self.w_, self.b_ = w, float(b)
        self.status = "FIT"
        return self

    def _predict_scaled(self, z):
        return _sigmoid(z @ self.w_ + self.b_)


class ShallowMLPDetector(_Detector):
    """Class-balanced deterministic one-hidden-layer supervised detector."""

    def fit(self, x, y, cell_ids):
        x, y, ok = self._prepare(x, y, cell_ids)
        if not ok:
            return self._inconclusive()
        self._fit_scaler(x)
        z = self.scaler.transform(x)
        n, d = z.shape
        h = max(4, min(24, 2 * d))
        rng = np.random.default_rng(self.seed)
        w1 = rng.normal(0.0, np.sqrt(2.0 / max(d, 1)), size=(d, h))
        b1 = np.zeros(h)
        w2 = rng.normal(0.0, np.sqrt(2.0 / h), size=h)
        b2 = 0.0
        counts = np.bincount(y, minlength=2).astype(float)
        weights = np.where(y == 1, n / (2.0 * max(counts[1], 1.0)), n / (2.0 * max(counts[0], 1.0)))
        for _ in range(260):
            hidden = np.tanh(z @ w1 + b1)
            p = _sigmoid(hidden @ w2 + b2)
            err = (p - y) * weights
            grad2 = hidden.T @ err / n + 1e-3 * w2
            grad_hidden = (err[:, None] * w2[None, :]) * (1.0 - hidden * hidden)
            grad1 = z.T @ grad_hidden / n + 1e-3 * w1
            w2 -= 0.05 * grad2
            b2 -= 0.05 * float(np.mean(err))
            w1 -= 0.05 * grad1
            b1 -= 0.05 * np.mean(grad_hidden, axis=0)
        self.w1_, self.b1_, self.w2_, self.b2_ = w1, b1, w2, float(b2)
        self.status = "FIT"
        return self

    def _predict_scaled(self, z):
        return _sigmoid(np.tanh(z @ self.w1_ + self.b1_) @ self.w2_ + self.b2_)


class CleanReconstructionDetector(_Detector):
    """Linear undercomplete reconstruction detector trained on clean rows only."""

    def fit(self, x, y, cell_ids):
        x = _matrix(x)
        y = _labels(y, x.shape[0])
        _cells(cell_ids, x.shape[0])
        clean = y == 0
        self.clean_train_count = int(np.sum(clean))
        if x.shape[0] < self.min_samples or self.clean_train_count < self.min_samples:
            return self._inconclusive()
        # The scaler is fit strictly on clean rows; anomalous rows cannot alter
        # the representation or the reconstruction reference distribution.
        self._fit_scaler(x[clean])
        z = self.scaler.transform(x[clean])
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

    def _predict_scaled(self, z):
        recon = np.tanh(z @ self.w1_ + self.b1_) @ self.w2_ + self.b2_
        error = np.mean((recon - z) ** 2, axis=1)
        return 1.0 - np.exp(-error / self.error_scale_)


def fit_candidates(x_train, y_train, cell_ids, seed: int = 0):
    """Fit all B001 detector mechanisms on the supplied train split only."""
    return {
        "logistic": LogisticDetector(seed=seed).fit(x_train, y_train, cell_ids),
        "mlp": ShallowMLPDetector(seed=seed).fit(x_train, y_train, cell_ids),
        "autoencoder": CleanReconstructionDetector(seed=seed).fit(x_train, y_train, cell_ids),
    }


def _cell_flags(scores, labels, cell_ids, threshold):
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int).reshape(-1)
    cell_ids = np.asarray(cell_ids).reshape(-1)
    flags = {}
    for cell in np.unique(cell_ids):
        mask = cell_ids == cell
        flags[cell] = (int(np.any(labels[mask] == 1)), np.flatnonzero(mask), np.flatnonzero(scores[mask] >= threshold))
    return flags


def calibrate_threshold(scores, labels, cell_ids, control_false_alarm_budget: float = 0.05):
    """Calibrate a threshold from train/control rows only.

    Callers must pass rows belonging to the control-rate calibration split;
    event labels must not participate in threshold selection.  The returned
    false-alarm rate is still computed at cell level.
    """
    scores = np.asarray(scores, dtype=float).reshape(-1)
    labels = _labels(labels, scores.size)
    cell_ids = _cells(cell_ids, scores.size)
    if not 0.0 <= control_false_alarm_budget <= 1.0:
        raise ValueError("control_false_alarm_budget must be in [0,1]")
    control_cells = [c for c in np.unique(cell_ids) if not np.any(labels[cell_ids == c] == 1)]
    if not control_cells:
        return {"status": "INCONCLUSIVE", "threshold": None, "control_false_alarm": None}
    control_mask = np.isin(cell_ids, np.asarray(control_cells))
    finite_scores = scores[control_mask & np.isfinite(scores)]
    if finite_scores.size == 0:
        return {"status": "INCONCLUSIVE", "threshold": None, "control_false_alarm": None}
    thresholds = [float(np.nextafter(np.max(finite_scores), np.inf))]
    thresholds.extend(float(v) for v in np.unique(finite_scores)[::-1])
    best = None
    for threshold in thresholds:
        control_fa = float(np.mean([np.any(scores[cell_ids == c] >= threshold) for c in control_cells]))
        if control_fa <= control_false_alarm_budget + 1e-12:
            # Choose the lowest threshold satisfying the control-only budget;
            # event scores/labels never participate in this selection.
            candidate = (threshold, control_fa)
            if best is None or candidate[0] < best[0]:
                best = candidate
    if best is None:
        return {"status": "INCONCLUSIVE", "threshold": None, "control_false_alarm": None}
    threshold, control_fa = best
    event_cells = [c for c in np.unique(cell_ids) if np.any(labels[cell_ids == c] == 1)]
    event_recall = float(np.mean([np.any(scores[cell_ids == c] >= threshold) for c in event_cells])) if event_cells else 0.0
    return {"status": "CALIBRATED", "threshold": threshold, "control_false_alarm": control_fa, "cell_event_recall": event_recall}


def _auroc(scores, labels):
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if pos.size == 0 or neg.size == 0:
        return None
    # Pairwise form is deterministic and handles ties exactly.
    return float((np.sum(pos[:, None] > neg[None, :]) + 0.5 * np.sum(pos[:, None] == neg[None, :])) / (pos.size * neg.size))


def _auprc(scores, labels):
    positives = int(np.sum(labels == 1))
    if positives == 0:
        return None
    order = np.argsort(-scores, kind="mergesort")
    y = labels[order]
    cumulative = np.cumsum(y)
    ranks = np.arange(1, y.size + 1)
    return float(np.sum((y == 1) * cumulative / ranks) / positives)


def _ece(scores, labels, bins: int = 10):
    scores = np.clip(np.asarray(scores, dtype=float), 0.0, 1.0)
    labels = np.asarray(labels, dtype=int)
    total = max(scores.size, 1)
    result = 0.0
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        mask = (scores >= lo) & (scores <= hi if i == bins - 1 else scores < hi)
        if np.any(mask):
            result += float(np.sum(mask) / total) * abs(float(np.mean(scores[mask])) - float(np.mean(labels[mask])))
    return result


def _first_persistent_run(values: np.ndarray, persistence_blocks: int):
    """Return the first start index of a true run of the requested length."""
    run = 0
    for index, value in enumerate(np.asarray(values, dtype=bool)):
        run = run + 1 if value else 0
        if run >= persistence_blocks:
            return index - persistence_blocks + 1
    return None


def evaluate_scores(scores, labels, cell_ids, threshold, persistence_blocks: int = 2):
    """Evaluate block and cell metrics with persistent event/alarm semantics.

    A cell is an event only when its labels contain ``persistence_blocks``
    consecutive positive blocks.  An alarm likewise requires a consecutive run
    of scores at or above ``threshold`` of the same length.  Oracle and alarm
    positions are the starts of those runs; cells with no persistent event are
    controls for the cell-level false-alarm calculation.
    """
    scores = np.asarray(scores, dtype=float).reshape(-1)
    labels = _labels(labels, scores.size)
    cell_ids = _cells(cell_ids, scores.size)
    if int(persistence_blocks) != persistence_blocks or persistence_blocks < 1:
        raise ValueError("persistence_blocks must be a positive integer")
    persistence_blocks = int(persistence_blocks)
    if not np.all(np.isfinite(scores)):
        return {"status": "INCONCLUSIVE"}
    event_cells = []
    control_cells = []
    leads = []
    recalled = 0
    for cell in np.unique(cell_ids):
        mask = cell_ids == cell
        oracle = _first_persistent_run(labels[mask] == 1, persistence_blocks)
        alarm = _first_persistent_run(scores[mask] >= threshold, persistence_blocks)
        if oracle is not None:
            event_cells.append(cell)
            if alarm is not None and int(alarm) <= oracle:
                recalled += 1
                leads.append(float(oracle - int(alarm)))
        else:
            control_cells.append(cell)
    control_fa = float(
        np.mean([_first_persistent_run(scores[cell_ids == c] >= threshold, persistence_blocks) is not None for c in control_cells])
    ) if control_cells else None
    return {
        "status": "EVALUATED",
        "block_auroc": _auroc(scores, labels),
        "block_auprc": _auprc(scores, labels),
        "cell_event_recall_before_or_at_oracle": float(recalled / len(event_cells)) if event_cells else None,
        "control_false_alarm": control_fa,
        "lead_blocks": float(np.mean(leads)) if leads else 0.0,
        "ece": _ece(scores, labels),
        "event_cells": len(event_cells),
        "control_cells": len(control_cells),
    }


__all__ = [
    "LogisticDetector",
    "ShallowMLPDetector",
    "CleanReconstructionDetector",
    "build_trace_features",
    "fit_candidates",
    "calibrate_threshold",
    "evaluate_scores",
]
