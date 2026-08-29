"""Receiver-local scaled-unitary pilot-LS seam frozen by T068/T069."""

from __future__ import annotations

import struct
from typing import NamedTuple

import numpy as np


class InvalidEstimate(ValueError):
    """Fail-closed request for fallback when the exact estimator is invalid."""


class ProjectionResult(NamedTuple):
    h_projected: np.ndarray
    w: np.ndarray
    g_hat: float
    rho: float
    singular_values: np.ndarray


class ReceiverResult(NamedTuple):
    z: np.ndarray
    g_hat: float
    rho: float
    h_ls: np.ndarray
    h_projected: np.ndarray
    w: np.ndarray
    valid: bool


def _finite_matrix(value: np.ndarray, name: str, columns: int | None = None) -> np.ndarray:
    array = np.asarray(value, dtype=np.complex128)
    if array.ndim != 2 or array.shape[0] != 2:
        raise InvalidEstimate(f"{name} must have shape (2, N)")
    if columns is not None and array.shape[1] != columns:
        raise InvalidEstimate(f"{name} column count mismatch")
    if not np.all(np.isfinite(array)):
        raise InvalidEstimate(f"{name} contains NaN or Inf")
    return array


def plain_ls(x_pilots: np.ndarray, y_pilots: np.ndarray) -> np.ndarray:
    """Return ``Yp Xp^H (Xp Xp^H)^-1`` with exact-invalid fail-closed."""
    x = _finite_matrix(x_pilots, "x_pilots")
    y = _finite_matrix(y_pilots, "y_pilots", x.shape[1])
    gram = x @ x.conj().T
    if np.linalg.det(gram) == 0.0:
        raise InvalidEstimate("pilot Gram matrix is exactly rank deficient")
    cross = y @ x.conj().T
    try:
        estimate = np.linalg.solve(gram.T, cross.T).T
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("pilot Gram solve failed") from error
    if not np.all(np.isfinite(estimate)):
        raise InvalidEstimate("LS estimate is nonfinite")
    return estimate


def project_scaled_unitary(h_ls: np.ndarray) -> ProjectionResult:
    """Project a nonsingular 2x2 estimate onto ``g Q``, ``Q in U(2)``."""
    h = _finite_matrix(h_ls, "h_ls", 2)
    if np.linalg.det(h) == 0.0:
        raise InvalidEstimate("channel estimate is exactly rank deficient")
    try:
        u, singular_values, vh = np.linalg.svd(h, full_matrices=False)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("channel SVD failed") from error
    if singular_values[1] == 0.0:
        raise InvalidEstimate("channel estimate has an exact zero singular value")
    g_hat = float(np.mean(singular_values))
    rho = float(singular_values[0] / singular_values[1])
    unitary = u @ vh
    h_projected = g_hat * unitary
    w = unitary.conj().T / g_hat
    if not (
        g_hat > 0.0
        and np.isfinite(g_hat)
        and np.isfinite(rho)
        and np.all(np.isfinite(h_projected))
        and np.all(np.isfinite(w))
    ):
        raise InvalidEstimate("scaled-unitary projection is nonfinite")
    return ProjectionResult(h_projected, w, g_hat, rho, singular_values.copy())


def direct_balanced_scaled_unitary(
    x_pilots: np.ndarray, y_pilots: np.ndarray
) -> ProjectionResult:
    """Solve the constrained objective directly for balanced pilot rows."""
    x = _finite_matrix(x_pilots, "x_pilots")
    y = _finite_matrix(y_pilots, "y_pilots", x.shape[1])
    gram = x @ x.conj().T
    scale = float(np.trace(gram).real / 2.0)
    if scale == 0.0 or not np.array_equal(gram, scale * np.eye(2)):
        raise InvalidEstimate("direct recipe requires exactly balanced pilots")
    cross = y @ x.conj().T
    if np.linalg.det(cross) == 0.0:
        raise InvalidEstimate("direct cross-covariance is exactly rank deficient")
    try:
        u, singular_values, vh = np.linalg.svd(cross, full_matrices=False)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("direct balanced SVD failed") from error
    g_hat = float(np.sum(singular_values) / (2.0 * scale))
    unitary = u @ vh
    h_projected = g_hat * unitary
    w = unitary.conj().T / g_hat
    rho = float(singular_values[0] / singular_values[1])
    if not np.all(np.isfinite(w)) or not np.isfinite(rho):
        raise InvalidEstimate("direct balanced projection is nonfinite")
    return ProjectionResult(h_projected, w, g_hat, rho, singular_values / scale)


def candidate_receiver(
    x_pilots: np.ndarray, y_pilots: np.ndarray, y_payload: np.ndarray
) -> ReceiverResult:
    """Run the deployable C4 receiver using observations only."""
    payload = _finite_matrix(y_payload, "y_payload")
    h_ls = plain_ls(x_pilots, y_pilots)
    projected = project_scaled_unitary(h_ls)
    z = projected.w @ payload
    if not np.all(np.isfinite(z)):
        raise InvalidEstimate("equalized payload is nonfinite")
    return ReceiverResult(
        z=z,
        g_hat=projected.g_hat,
        rho=projected.rho,
        h_ls=h_ls,
        h_projected=projected.h_projected,
        w=projected.w,
        valid=True,
    )


def deployable_bytes(result: ReceiverResult) -> bytes:
    """Canonical byte snapshot of only the T068 deployable outputs."""
    z = np.ascontiguousarray(result.z, dtype="<c16")
    return z.tobytes(order="C") + struct.pack("<dd", result.g_hat, result.rho)
