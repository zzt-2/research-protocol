"""C1-only deployable B10-family arms; no validation or performance runner."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from common._modulation import hard_decision


PACKAGE_DIR = Path(__file__).resolve().parent
PILOT_COUNT = 128


def _load_source():
    spec = importlib.util.spec_from_file_location("t010_source_for_methods", PACKAGE_DIR / "source_native_rls.py")
    if spec is None or spec.loader is None:
        raise ImportError("cannot load source_native_rls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(
    rx: np.ndarray,
    *,
    mode: str,
    forgetting_factor: float = 0.99,
    threshold: float | None = None,
    lambda_min: float | None = None,
    lambda_max: float | None = None,
    ema_alpha: float = 0.1,
    innovation_scale: float = 1.0,
) -> dict:
    shared_identity = rx
    rx = np.asarray(rx, dtype=complex)
    if len(rx) <= PILOT_COUNT:
        raise ValueError("rx must contain data after the 128 pilots")
    source = _load_source()
    pilots = source._pilot_symbols()
    observed = np.unwrap(np.angle(rx[:PILOT_COUNT] / pilots))
    h = np.zeros(2)
    p = np.eye(2) * 0.5
    corrected = np.empty_like(rx)
    update_mask = np.ones(len(rx), dtype=bool)
    innovation = np.zeros(len(rx))
    lambda_path = np.full(len(rx), forgetting_factor, dtype=float)
    ema = 0.0

    for index in range(PILOT_COUNT):
        x = np.array([1.0, float(index + 1)])
        h, p, error = source._update(h, p, x, float(observed[index]), forgetting_factor)
        innovation[index] = abs(error)
        corrected[index] = rx[index] * np.exp(-1j * np.dot(h, x))
    slope = float(h[1])
    if not np.isfinite(slope) or slope <= 0:
        raise ValueError("C1 methods require the accepted positive-CFO lifecycle")
    period = 2 * np.pi / slope

    for index in range(PILOT_COUNT, len(rx)):
        x = np.array([1.0, np.mod(float(index + 1), period)])
        predicted = float(np.dot(h, x))
        derotated = rx[index] * np.exp(-1j * predicted)
        decision = hard_decision(derotated, mod="qam16")
        residual = source.operational_residual(derotated, decision)
        desired = predicted + residual
        px = p @ x
        normalized = abs(desired - np.dot(h, x)) / np.sqrt(
            max(forgetting_factor + float(np.dot(x, px)), 1e-15)
        )
        innovation[index] = normalized

        lam = forgetting_factor
        do_update = True
        if mode == "innovation":
            do_update = normalized <= float(threshold)
        elif mode == "amplitude":
            do_update = abs(derotated) >= float(threshold)
        elif mode == "adaptive":
            lo, hi = float(lambda_min), float(lambda_max)
            lam = hi - (hi - lo) * np.tanh(innovation_scale * max(ema, 0.0))
            lam = float(np.clip(lam, lo, hi))
        else:
            raise ValueError(f"unknown mode {mode}")
        lambda_path[index] = lam
        update_mask[index] = do_update
        corrected[index] = derotated
        if do_update:
            h, p, _ = source._update(h, p, x, desired, lam)
        if mode == "adaptive":
            ema = (1.0 - ema_alpha) * ema + ema_alpha * normalized

    return {
        "corrected": corrected,
        "update_mask": update_mask,
        "lambda_path": lambda_path,
        "normalized_innovation": innovation,
        "state_finite": bool(
            np.all(np.isfinite(rx))
            and np.all(np.isfinite(corrected))
            and np.all(np.isfinite(innovation))
            and np.all(np.isfinite(lambda_path))
            and np.all(np.isfinite(h))
            and np.all(np.isfinite(p))
        ),
        "shared_rx_identity": shared_identity,
        "period": period,
    }


def run_innovation_freeze(
    rx: np.ndarray, *, forgetting_factor: float, threshold: float
) -> dict:
    """P2: current receiver-visible normalized innovation gates only this update."""
    if not np.isfinite(forgetting_factor) or not 0 < forgetting_factor <= 1:
        raise ValueError("forgetting_factor must be finite and lie in (0,1]")
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("threshold must be finite and nonnegative")
    return _run(
        rx, mode="innovation", forgetting_factor=forgetting_factor, threshold=threshold
    )


def run_adaptive_forgetting(
    rx: np.ndarray,
    *,
    lambda_min: float,
    lambda_max: float,
    ema_alpha: float,
    innovation_scale: float,
) -> dict:
    """P3: lambda[k] depends only on the EMA completed through k-1."""
    if (
        not np.isfinite(lambda_min)
        or not np.isfinite(lambda_max)
        or not 0 < lambda_min <= lambda_max <= 1
    ):
        raise ValueError("lambda bounds must satisfy 0 < min <= max <= 1")
    if not np.isfinite(ema_alpha) or not 0 < ema_alpha <= 1:
        raise ValueError("ema_alpha must be finite and lie in (0,1]")
    if not np.isfinite(innovation_scale) or innovation_scale < 0:
        raise ValueError("innovation_scale must be finite and nonnegative")
    return _run(
        rx,
        mode="adaptive",
        forgetting_factor=lambda_max,
        lambda_min=lambda_min,
        lambda_max=lambda_max,
        ema_alpha=ema_alpha,
        innovation_scale=innovation_scale,
    )


def run_amplitude_freeze(
    rx: np.ndarray, *, forgetting_factor: float, threshold: float
) -> dict:
    """Cheap alternative: current receiver amplitude alone gates DD updates."""
    if not np.isfinite(forgetting_factor) or not 0 < forgetting_factor <= 1:
        raise ValueError("forgetting_factor must be finite and lie in (0,1]")
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("threshold must be finite and nonnegative")
    return _run(
        rx, mode="amplitude", forgetting_factor=forgetting_factor, threshold=threshold
    )
