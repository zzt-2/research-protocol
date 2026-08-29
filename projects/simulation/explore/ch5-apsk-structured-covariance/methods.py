"""B1/B2/B3/C1 covariance estimators for T054 correctness smoke.

All estimators share pilot samples, point-centroid rule, and the same numerical
eigenvalue floor.  C1 implements lambda_k = kappa / (n_k + kappa).  Cross-
polarization sample pooling is intentionally absent from this v1 seam.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StructuredDetails:
    counts: np.ndarray
    local_variances: np.ndarray
    ring_targets: np.ndarray
    shrunk_variances: np.ndarray
    covariances: np.ndarray


@dataclass(frozen=True)
class GaussianArm:
    """One covariance arm bound to the shared pilot-estimated centroids."""

    means: np.ndarray
    covariances: np.ndarray


def _validated_inputs(
    pilot_z: np.ndarray, pilot_labels: np.ndarray, constellation: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    z = np.asarray(pilot_z, dtype=np.complex128).reshape(-1)
    labels = np.asarray(pilot_labels)
    constellation = np.asarray(constellation, dtype=np.complex128)
    if labels.shape != z.shape or constellation.shape != (16,):
        raise ValueError("pilot_z/labels must align and constellation must be (16,)")
    if not np.issubdtype(labels.dtype, np.integer):
        raise TypeError("pilot labels must be integer constellation indices")
    labels = labels.astype(np.int64, copy=False)
    if np.any(labels < 0) or np.any(labels >= 16):
        raise ValueError("pilot labels must be in [0,15]")
    counts = np.bincount(labels, minlength=16)
    if np.any(counts < 2):
        raise ValueError("each constellation point needs at least two pilots")
    return z, labels, constellation


def _ring_ids(constellation: np.ndarray) -> np.ndarray:
    radii = np.abs(constellation)
    distinct = np.unique(np.round(radii, decimals=12))
    if distinct.size != 2:
        raise ValueError("T054 requires an (8,8)-16APSK two-ring constellation")
    return np.argmin(np.abs(radii[:, None] - distinct[None, :]), axis=1)


def _rotation(theta: float) -> np.ndarray:
    cosine, sine = np.cos(theta), np.sin(theta)
    return np.array([[cosine, -sine], [sine, cosine]], dtype=np.float64)


def _floor_covariance(covariance: np.ndarray, floor: float) -> np.ndarray:
    if not np.isfinite(floor) or floor <= 0.0:
        raise ValueError("floor must be finite and positive")
    symmetric = 0.5 * (covariance + covariance.T)
    values, vectors = np.linalg.eigh(symmetric)
    values = np.maximum(values, floor)
    return (vectors * values) @ vectors.T


def _point_statistics(
    pilot_z: np.ndarray, pilot_labels: np.ndarray, constellation: np.ndarray
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    tuple[np.ndarray, ...],
    tuple[np.ndarray, ...],
]:
    z, labels, constellation = _validated_inputs(pilot_z, pilot_labels, constellation)
    counts = np.bincount(labels, minlength=16)
    means = np.array([z[labels == point].mean() for point in range(16)])
    residual = z - means[labels]
    local_rt = []
    local_iq = []
    for point in range(16):
        point_residual = residual[labels == point]
        rotated = point_residual * np.exp(-1j * np.angle(constellation[point]))
        local_rt.append(np.column_stack((rotated.real, rotated.imag)))
        local_iq.append(np.column_stack((point_residual.real, point_residual.imag)))
    return labels, counts, means, tuple(local_rt), tuple(local_iq)


def _rt_variances(local_rt: tuple[np.ndarray, ...]) -> np.ndarray:
    return np.array([np.var(samples, axis=0, ddof=1) for samples in local_rt])


def _ring_targets(local_rt: tuple[np.ndarray, ...], ring_ids: np.ndarray) -> np.ndarray:
    target_by_ring = []
    for ring in range(2):
        groups = [local_rt[index] for index in np.flatnonzero(ring_ids == ring)]
        degrees_of_freedom = sum(group.shape[0] - 1 for group in groups)
        sum_squares = sum(np.sum(group * group, axis=0) for group in groups)
        target_by_ring.append(sum_squares / degrees_of_freedom)
    target_by_ring = np.asarray(target_by_ring)
    return target_by_ring[ring_ids]


def _rt_to_iq(
    variances: np.ndarray, constellation: np.ndarray, *, floor: float
) -> np.ndarray:
    covariances = np.empty((16, 2, 2), dtype=np.float64)
    for point in range(16):
        rotation = _rotation(float(np.angle(constellation[point])))
        covariance = rotation @ np.diag(variances[point]) @ rotation.T
        covariances[point] = _floor_covariance(covariance, floor)
    return covariances


def point_local_rt_covariances(
    pilot_z: np.ndarray,
    pilot_labels: np.ndarray,
    constellation: np.ndarray,
    *,
    floor: float,
) -> np.ndarray:
    """Point-local radial/tangential estimator (C1 at kappa=0)."""
    _, _, _, local_rt, _ = _point_statistics(pilot_z, pilot_labels, constellation)
    return _rt_to_iq(_rt_variances(local_rt), np.asarray(constellation), floor=floor)


def estimate_structured_details(
    pilot_z: np.ndarray,
    pilot_labels: np.ndarray,
    constellation: np.ndarray,
    *,
    floor: float,
    kappa: float,
) -> StructuredDetails:
    """Return C1 closed-form components and covariances."""
    if not np.isfinite(kappa) or kappa < 0.0:
        raise ValueError("kappa must be finite and non-negative")
    _, counts, _, local_rt, _ = _point_statistics(pilot_z, pilot_labels, constellation)
    constellation = np.asarray(constellation, dtype=np.complex128)
    ring_ids = _ring_ids(constellation)
    local_variances = _rt_variances(local_rt)
    ring_targets = _ring_targets(local_rt, ring_ids)
    lambdas = kappa / (counts.astype(np.float64) + kappa)
    shrunk = (1.0 - lambdas[:, None]) * local_variances + lambdas[:, None] * ring_targets
    covariances = _rt_to_iq(shrunk, constellation, floor=floor)
    return StructuredDetails(
        counts=counts,
        local_variances=local_variances,
        ring_targets=ring_targets,
        shrunk_variances=shrunk,
        covariances=covariances,
    )


def estimate_covariance_arms(
    pilot_z: np.ndarray,
    pilot_labels: np.ndarray,
    constellation: np.ndarray,
    *,
    floor: float,
    kappa: float,
    b3_shrinkage: float,
) -> dict[str, np.ndarray]:
    """Estimate frozen B1/B2/B3/C1 arms from receiver-visible pilots only."""
    if not np.isfinite(b3_shrinkage) or not 0.0 <= b3_shrinkage <= 1.0:
        raise ValueError("b3_shrinkage must be in [0,1]")
    _, _, _, local_rt, local_iq = _point_statistics(
        pilot_z, pilot_labels, constellation
    )
    constellation = np.asarray(constellation, dtype=np.complex128)
    ring_ids = _ring_ids(constellation)

    ring_targets = _ring_targets(local_rt, ring_ids)
    b2 = _rt_to_iq(ring_targets, constellation, floor=floor)

    b1 = np.empty((16, 2, 2), dtype=np.float64)
    for ring in range(2):
        groups = [local_iq[index] for index in np.flatnonzero(ring_ids == ring)]
        degrees_of_freedom = sum(group.shape[0] - 1 for group in groups)
        scalar = float(
            sum(np.sum(group * group) for group in groups)
            / (2.0 * degrees_of_freedom)
        )
        covariance = _floor_covariance(np.eye(2) * scalar, floor)
        b1[ring_ids == ring] = covariance

    b3 = np.empty((16, 2, 2), dtype=np.float64)
    for point in range(16):
        sample = np.cov(local_iq[point], rowvar=False, ddof=1)
        isotropic = np.eye(2) * (np.trace(sample) / 2.0)
        shrunk = (1.0 - b3_shrinkage) * sample + b3_shrinkage * isotropic
        b3[point] = _floor_covariance(shrunk, floor)

    c1 = estimate_structured_details(
        pilot_z, pilot_labels, constellation, floor=floor, kappa=kappa
    ).covariances
    return {"B1": b1, "B2": b2, "B3": b3, "C1": c1}


def estimate_gaussian_arms(
    pilot_z: np.ndarray,
    pilot_labels: np.ndarray,
    constellation: np.ndarray,
    *,
    floor: float,
    kappa: float,
    b3_shrinkage: float,
) -> dict[str, GaussianArm]:
    """Bind every covariance arm to one shared pilot-estimated mean array."""
    _, _, means, _, _ = _point_statistics(pilot_z, pilot_labels, constellation)
    means.setflags(write=False)
    covariances = estimate_covariance_arms(
        pilot_z,
        pilot_labels,
        constellation,
        floor=floor,
        kappa=kappa,
        b3_shrinkage=b3_shrinkage,
    )
    return {
        name: GaussianArm(means=means, covariances=value)
        for name, value in covariances.items()
    }


__all__ = [
    "StructuredDetails",
    "estimate_covariance_arms",
    "estimate_gaussian_arms",
    "estimate_structured_details",
    "GaussianArm",
    "point_local_rt_covariances",
]
