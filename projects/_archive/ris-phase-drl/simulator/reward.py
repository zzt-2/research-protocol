"""Sum-rate reward computation."""

from __future__ import annotations

import numpy as np


def compute_sum_rate(
    H_eff: np.ndarray, W: np.ndarray, noise_power: float
) -> tuple[float, np.ndarray]:
    """Compute sum rate and per-user SINR.

    Units: bps/Hz (spectral efficiency), bandwidth B not multiplied.

    Args:
        H_eff: (K, M) complex -- effective channel
        W: (M, K) complex -- beamforming matrix (power-normalized)
        noise_power: noise power (W)

    Returns:
        sum_rate: total sum rate (bps/Hz)
        sinrs: (K,) per-user SINR values
    """
    K = H_eff.shape[0]
    # Received signal model:
    #   y_k = h_eff_k^H @ w_k * s_k + sum_{j!=k} h_eff_k^H @ w_j * s_j + n_k
    # All inner products at once: (K, M) @ (M, K) -> (K, K)
    link_gain = H_eff @ W  # (K, K); [k, j] = h_eff_k^H @ w_j

    # Signal power: diagonal elements
    signal_power = np.abs(np.diag(link_gain)) ** 2  # (K,)

    # Interference: sum of off-diagonal squared magnitudes per row
    interference_power = np.sum(np.abs(link_gain) ** 2, axis=1) - signal_power  # (K,)

    sinrs = signal_power / (interference_power + noise_power)
    rates = np.log2(1 + sinrs)
    return float(np.sum(rates)), sinrs
