"""Zero-forcing beamforming."""

from __future__ import annotations

import numpy as np


def zf_beamforming(
    H_eff: np.ndarray, tx_power: float, n_users: int
) -> np.ndarray:
    """Compute ZF precoding matrix.

    Args:
        H_eff: (K, M) complex -- effective channel, row k = user k's channel
        tx_power: transmit power (W)
        n_users: number of users K

    Returns:
        W: (M, K) complex -- beamforming matrix, power-normalized
    """
    K, M = H_eff.shape
    # W = H^H (H H^H + lambda I)^{-1}, shape (M, K)
    HH = H_eff @ H_eff.conj().T  # (K, K)
    reg = 1e-6 * np.eye(K)
    W = H_eff.conj().T @ np.linalg.solve(HH + reg, np.eye(K))  # (M, K)

    # Power normalization: ||W||_F = sqrt(P_t)
    norm = np.linalg.norm(W, "fro")
    if norm > 0:
        W = np.sqrt(tx_power) * W / norm
    return W
