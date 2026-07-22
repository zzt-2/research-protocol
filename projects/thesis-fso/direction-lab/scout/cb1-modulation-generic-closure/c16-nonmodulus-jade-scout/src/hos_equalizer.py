"""HOS (higher-order-statistics) non-modulus blind equalizer for 2x2 dual-pol.

Paradigm: source separation by kurtosis maximization / 4th-order statistics.
NO modulus term (no |z|^2 cost) — the collapse local minimum of modulus costs
cannot exist in this landscape by construction.

References:
  - Cardoso & Souloumiac 1993, "Blind beamforming for non-Gaussian signals" (JADE)
  - Comon 1994, "Independent component analysis, a new concept?" (ICA)
  - Hyvarinen 1999, "Fast and robust fixed-point algorithms for ICA" (FastICA)

Implementation: simplified 2-source complex ICA via:
  1. Whitening (remove 2nd-order correlations via eigenvalue decomposition)
  2. Givens-rotation search maximizing |kurtosis(zX)| + |kurtosis(zY)|

This is CSI_NONE: only uses (rX, rY) received-sample statistics.
"""

from __future__ import annotations

import numpy as np


def _whiten(rX: np.ndarray, rY: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Whiten the 2-pol data: remove 2nd-order correlations.

    Stack into [2, N], compute covariance, whiten so output has identity covariance.
    """
    data = np.vstack([rX[np.newaxis, :], rY[np.newaxis, :]])  # [2, N]
    cov = np.cov(data)  # [2, 2]
    # Eigen-decomposition of covariance
    eigvals, eigvecs = np.linalg.eigh(cov)
    # Whitening matrix: V = D^{-1/2} E^H
    d_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(eigvals, 1e-12)))
    W_white = d_inv_sqrt @ eigvecs.conj().T  # [2, 2]
    whitened = W_white @ data  # [2, N]
    return whitened[0], whitened[1], W_white


def _kurtosis_abs_sum(zX: np.ndarray, zY: np.ndarray) -> float:
    """Sum of absolute kurtoses — the non-modulus objective.

    kurtosis(x) = E[|x|^4] / E[|x|^2]^2 - 2  (for complex: use both real and imag,
    or the modulus-based kurtosis ratio). We use the modulus kurtosis ratio minus 2,
    which is a standard complex negentropy proxy. Sub-Gaussian (like 16QAM) has
    NEGATIVE excess kurtosis; we maximize the absolute deviation from Gaussian.

    NOTE: This has NO |z|^2 modulus-matching term. It measures the SHAPE of the
    distribution, not its radius.
    """
    for label, z in [("zX", zX), ("zY", zY)]:
        if z.size == 0:
            return -1e10
        p = np.mean(np.abs(z) ** 2)
        if p < 1e-12:
            return -1e10
    kX = np.mean(np.abs(zX) ** 4) / (np.mean(np.abs(zX) ** 2) ** 2)
    kY = np.mean(np.abs(zY) ** 4) / (np.mean(np.abs(zY) ** 2) ** 2)
    # Maximize deviation from Gaussian (kurtosis ratio = 2 for complex Gaussian)
    return abs(kX - 2.0) + abs(kY - 2.0)


def _apply_givens(z: np.ndarray, theta: float) -> np.ndarray:
    """Apply a 2x2 Givens rotation by angle theta to [2, N] data."""
    c, s = np.cos(theta), np.sin(theta)
    rot = np.array([[c, -s], [s, c]])
    # For complex sources, also search a phase. We use real Givens for simplicity;
    # the whitening already handles the complex mixing structure.
    return rot @ z


def hos_equalize_dp(rX: np.ndarray, rY: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict]:
    """Non-modulus HOS blind equalizer for dual-pol.

    Returns (zX, zY, info). The equalizer has NO modulus cost term.

    Steps:
      1. Whiten (rX, rY) to remove 2nd-order structure.
      2. Search over Givens rotation angles (real theta + complex phase phi)
         to maximize |kurtosis deviation| of the two outputs.
      3. Return the separated sources.
    """
    rX = np.asarray(rX, dtype=np.complex128)
    rY = np.asarray(rY, dtype=np.complex128)

    # Step 1: whiten
    wX, wY, W_white = _whiten(rX, rY)
    whitened = np.vstack([wX[np.newaxis, :], wY[np.newaxis, :]])  # [2, N]

    # Step 2: search over rotation angle theta and phase phi
    best_obj = -1e10
    best_zX, best_zY = wX.copy(), wY.copy()
    best_theta, best_phi = 0.0, 0.0

    # Coarse search over theta [0, pi/2) (symmetry) and phi [0, 2pi)
    for theta in np.linspace(0, np.pi / 2, 36, endpoint=False):
        c, s = np.cos(theta), np.sin(theta)
        rot = np.array([[c, -s], [s, c]], dtype=np.float64)
        rotated = rot @ whitened
        for phi in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            phase = np.exp(1j * phi)
            # Apply phase to second output (relative phase search)
            zX_try = rotated[0]
            zY_try = rotated[1] * phase
            obj = _kurtosis_abs_sum(zX_try, zY_try)
            if obj > best_obj:
                best_obj = obj
                best_zX = zX_try.copy()
                best_zY = zY_try.copy()
                best_theta = float(theta)
                best_phi = float(phi)

    # Fine search around best
    for theta in np.linspace(best_theta - 0.1, best_theta + 0.1, 20):
        if theta < 0 or theta >= np.pi / 2:
            continue
        c, s = np.cos(theta), np.sin(theta)
        rot = np.array([[c, -s], [s, c]], dtype=np.float64)
        rotated = rot @ whitened
        for phi in np.linspace(best_phi - 0.5, best_phi + 0.5, 12):
            phase = np.exp(1j * phi)
            zX_try = rotated[0]
            zY_try = rotated[1] * phase
            obj = _kurtosis_abs_sum(zX_try, zY_try)
            if obj > best_obj:
                best_obj = obj
                best_zX = zX_try.copy()
                best_zY = zY_try.copy()
                best_theta = float(theta)
                best_phi = float(phi)

    info = {
        "best_objective": float(best_obj),
        "best_theta": float(best_theta),
        "best_phi": float(best_phi),
        "whitening_matrix": W_white,
        "method": "HOS_kurtosis_maximization",
        "cost_contains_modulus_term": False,
    }
    return best_zX, best_zY, info


def jade_equalize_dp(rX: np.ndarray, rY: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict]:
    """Alias for hos_equalize_dp (JADE-style 4th-order separation)."""
    return hos_equalize_dp(rX, rY)


__all__ = ["hos_equalize_dp", "jade_equalize_dp"]
