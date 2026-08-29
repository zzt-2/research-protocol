"""T066 window-cluster occurrence diagnostics; no performance metrics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from codec_metrics import apsk16_table


GROUPS = ("pol0_inner", "pol0_outer", "pol1_inner", "pol1_outer")


@dataclass(frozen=True)
class WindowResidual:
    window_id: int
    seed: int
    e: np.ndarray
    point_labels: np.ndarray
    ring_labels: np.ndarray
    realization_hash: str = "synthetic-unit"
    bundle_hash: str = "synthetic-unit"


def cluster_bootstrap_indices(*, n_clusters: int, resamples: int, seed: int) -> np.ndarray:
    if n_clusters < 2 or resamples < 1:
        raise ValueError("cluster bootstrap needs at least two clusters and one resample")
    rng = np.random.Generator(np.random.PCG64(seed))
    return rng.integers(
        0, n_clusters, size=(resamples, n_clusters), dtype=np.int64
    )


def _floor_covariance(covariance: np.ndarray, floor: float) -> np.ndarray:
    symmetric = 0.5 * (covariance + covariance.T)
    values, vectors = np.linalg.eigh(symmetric)
    return (vectors * np.maximum(values, floor)) @ vectors.T


def _validate_windows(windows: list[WindowResidual] | tuple[WindowResidual, ...]) -> dict[int, WindowResidual]:
    by_id: dict[int, WindowResidual] = {}
    for window in windows:
        if window.window_id in by_id:
            raise ValueError("window_id values must be unique")
        e = np.asarray(window.e, dtype=np.complex128)
        labels = np.asarray(window.point_labels, dtype=np.int64)
        rings = np.asarray(window.ring_labels, dtype=bool)
        if e.ndim != 2 or e.shape[0] != 2 or labels.shape != e.shape or rings.shape != e.shape:
            raise ValueError("each window must contain aligned (2,pilots) residual/label arrays")
        if not np.all(np.isfinite(e)) or np.any(labels < 0) or np.any(labels >= 16):
            raise ValueError("window residuals and labels must be finite and valid")
        if not np.array_equal(rings, labels >= 8):
            raise ValueError("ring labels must match the canonical 8+8 APSK labels")
        by_id[window.window_id] = window
    return by_id


def fit_calibration_covariances(
    windows: list[WindowResidual] | tuple[WindowResidual, ...],
    *,
    calibration_window_ids: tuple[int, ...],
    floor: float,
) -> dict[str, np.ndarray]:
    if not np.isfinite(floor) or floor <= 0.0:
        raise ValueError("floor must be finite and positive")
    by_id = _validate_windows(windows)
    selected = [by_id[index] for index in calibration_window_ids]
    b1 = np.empty((2, 2, 2, 2), dtype=np.float64)
    full = np.empty((2, 16, 2, 2), dtype=np.float64)
    b1_counts = np.empty((2, 2), dtype=np.int64)
    full_counts = np.empty((2, 16), dtype=np.int64)
    for pol in range(2):
        for ring in range(2):
            samples = np.concatenate(
                [
                    window.e[pol][window.ring_labels[pol] == bool(ring)]
                    for window in selected
                ]
            )
            xy = np.column_stack((samples.real, samples.imag))
            scalar = float(np.sum(xy * xy) / (2.0 * xy.shape[0]))
            b1[pol, ring] = _floor_covariance(np.eye(2) * scalar, floor)
            b1_counts[pol, ring] = xy.shape[0]
        for point in range(16):
            samples = np.concatenate(
                [
                    window.e[pol][window.point_labels[pol] == point]
                    for window in selected
                ]
            )
            xy = np.column_stack((samples.real, samples.imag))
            full[pol, point] = _floor_covariance((xy.T @ xy) / xy.shape[0], floor)
            full_counts[pol, point] = xy.shape[0]
    return {
        "b1": b1,
        "full": full,
        "b1_counts": b1_counts,
        "full_counts": full_counts,
    }


def _group_summary(window: WindowResidual, pol: int, ring: int) -> np.ndarray:
    mask = window.ring_labels[pol] == bool(ring)
    samples = window.e[pol, mask]
    symbols, _ = apsk16_table()
    rotated = samples * np.exp(-1j * np.angle(symbols[window.point_labels[pol, mask]]))
    radial = rotated.real
    tangential = rotated.imag
    return np.array(
        [
            radial.size,
            radial.sum(),
            tangential.sum(),
            radial @ radial,
            tangential @ tangential,
            radial @ tangential,
        ],
        dtype=np.float64,
    )


def _d1_d2_from_summaries(summaries: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    total = np.asarray(summaries, dtype=np.float64)
    n, sum_r, sum_t, sum_rr, sum_tt, sum_rt = np.moveaxis(total, -1, 0)
    var_r = (sum_rr - sum_r * sum_r / n) / (n - 1.0)
    var_t = (sum_tt - sum_t * sum_t / n) / (n - 1.0)
    covariance = (sum_rt - sum_r * sum_t / n) / (n - 1.0)
    d1 = np.log(var_r / var_t)
    d2 = covariance / np.sqrt(var_r * var_t)
    return d1, d2


def _nll(samples: np.ndarray, covariances: np.ndarray) -> np.ndarray:
    values = np.asarray(samples, dtype=np.float64)
    sign, logdet = np.linalg.slogdet(covariances)
    if np.any(sign <= 0) or not np.all(np.isfinite(logdet)):
        raise ValueError("covariances must be finite positive-definite")
    solved = np.linalg.solve(covariances, values[..., None])[..., 0]
    return 0.5 * (logdet + np.einsum("ni,ni->n", values, solved))


def _window_nll_improvement(window: WindowResidual, fit: dict[str, np.ndarray]) -> float:
    improvements = []
    for pol in range(2):
        samples = window.e[pol]
        xy = np.column_stack((samples.real, samples.imag))
        labels = window.point_labels[pol]
        rings = window.ring_labels[pol].astype(np.int64)
        nll_b1 = _nll(xy, fit["b1"][pol, rings])
        nll_full = _nll(xy, fit["full"][pol, labels])
        improvements.append(nll_b1 - nll_full)
    return float(np.mean(np.concatenate(improvements)))


def classify_terminal(d1: dict, d2: dict, d3_ci: list[float] | tuple[float, float]) -> str:
    def excludes_zero(entry: dict) -> bool:
        lower, upper = entry["ci"]
        return bool(lower > 0.0 or upper < 0.0)

    detectable = any(excludes_zero(value) for value in d1.values())
    detectable |= any(excludes_zero(value) for value in d2.values())
    detectable |= bool(d3_ci[0] > 0.0)
    return "DETECTABLE_OCCURRENCE" if detectable else "NO_DETECTABLE_OCCURRENCE"


def reduce_occurrence(
    windows: list[WindowResidual] | tuple[WindowResidual, ...],
    *,
    calibration_window_ids: tuple[int, ...],
    evaluation_window_ids: tuple[int, ...],
    floor: float,
    bootstrap_seed: int,
    bootstrap_resamples: int,
) -> dict:
    calibration = tuple(calibration_window_ids)
    evaluation = tuple(evaluation_window_ids)
    if set(calibration) & set(evaluation):
        raise ValueError("calibration and evaluation windows must be disjoint")
    by_id = _validate_windows(windows)
    if not set(calibration + evaluation).issubset(by_id):
        raise ValueError("split references missing windows")
    fit = fit_calibration_covariances(
        windows, calibration_window_ids=calibration, floor=floor
    )
    eval_windows = [by_id[index] for index in evaluation]
    bootstrap = cluster_bootstrap_indices(
        n_clusters=len(eval_windows),
        resamples=bootstrap_resamples,
        seed=bootstrap_seed,
    )

    d1: dict[str, dict] = {}
    d2: dict[str, dict] = {}
    for pol in range(2):
        for ring in range(2):
            name = f"pol{pol}_{'outer' if ring else 'inner'}"
            summaries = np.stack(
                [_group_summary(window, pol, ring) for window in eval_windows]
            )
            point_summary = summaries.sum(axis=0)
            d1_estimate, d2_estimate = _d1_d2_from_summaries(point_summary)
            bootstrap_summaries = summaries[bootstrap].sum(axis=1)
            d1_samples, d2_samples = _d1_d2_from_summaries(bootstrap_summaries)
            point_counts = np.zeros(16, dtype=np.int64)
            for window in eval_windows:
                ring_mask = window.ring_labels[pol] == bool(ring)
                point_counts += np.bincount(
                    window.point_labels[pol, ring_mask], minlength=16
                )
            d1[name] = {
                "estimate": float(d1_estimate),
                "ci": np.quantile(d1_samples, [0.00625, 0.99375]).tolist(),
                "samples": int(point_summary[0]),
                "point_counts": point_counts.tolist(),
            }
            d2[name] = {
                "estimate": float(d2_estimate),
                "ci": np.quantile(d2_samples, [0.00625, 0.99375]).tolist(),
                "samples": int(point_summary[0]),
                "point_counts": point_counts.tolist(),
            }

    window_improvements = np.array(
        [_window_nll_improvement(window, fit) for window in eval_windows]
    )
    d3_bootstrap = window_improvements[bootstrap].mean(axis=1)
    d3_ci = np.quantile(d3_bootstrap, [0.025, 0.975]).tolist()
    d3 = {
        "estimate": float(window_improvements.mean()),
        "ci": d3_ci,
        "window_values": window_improvements.tolist(),
        "calibration_b1_counts": fit["b1_counts"].tolist(),
        "calibration_point_counts": fit["full_counts"].tolist(),
    }
    terminal = classify_terminal(d1, d2, d3_ci)
    return {
        "d1": d1,
        "d2": d2,
        "d3": d3,
        "bootstrap": {
            "cluster": "evaluation_window",
            "seed": int(bootstrap_seed),
            "resamples": int(bootstrap_resamples),
            "evaluation_clusters": len(eval_windows),
        },
        "split": {
            "calibration_window_ids": list(calibration),
            "evaluation_window_ids": list(evaluation),
            "disjoint": True,
        },
        "terminal": terminal,
    }


def synthetic_unit_windows(*, seed: int, anisotropic: bool) -> list[WindowResidual]:
    """Deterministic reducer-only fixture; never used by the scientific runner."""
    rng = np.random.default_rng(seed)
    symbols, _ = apsk16_table()
    windows = []
    base_labels = np.tile(np.arange(16, dtype=np.int64), 4)
    for window_id in range(64):
        labels = np.stack((base_labels, np.roll(base_labels, 3)))
        residual = np.empty((2, 64), dtype=np.complex128)
        for pol in range(2):
            for sample_index, point in enumerate(labels[pol]):
                if anisotropic:
                    radial_std = 0.035 + 0.001 * (point % 4)
                    tangential_std = 0.012 + 0.0005 * ((point // 2) % 3)
                    rho = 0.35 + 0.02 * (point % 2)
                else:
                    radial_std = tangential_std = 0.02
                    rho = 0.0
                covariance = np.array(
                    [
                        [radial_std**2, rho * radial_std * tangential_std],
                        [rho * radial_std * tangential_std, tangential_std**2],
                    ]
                )
                radial, tangential = rng.multivariate_normal([0.0, 0.0], covariance)
                residual[pol, sample_index] = (radial + 1j * tangential) * np.exp(
                    1j * np.angle(symbols[point])
                )
        windows.append(
            WindowResidual(
                window_id=window_id,
                seed=seed + window_id,
                e=residual,
                point_labels=labels.copy(),
                ring_labels=labels >= 8,
            )
        )
    return windows


__all__ = [
    "GROUPS",
    "WindowResidual",
    "classify_terminal",
    "cluster_bootstrap_indices",
    "fit_calibration_covariances",
    "reduce_occurrence",
    "synthetic_unit_windows",
]
