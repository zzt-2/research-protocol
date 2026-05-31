"""Free space path loss, SINR computation, and interference graph."""
import numpy as np

from .config import SimConfig


def free_space_path_loss_db(distance_km: float, frequency_hz: float) -> float:
    """Free space path loss in dB.

    L_fs = 20*log10(4πd/λ) where d in meters.
    """
    wavelength_m = 3e8 / frequency_hz
    d_m = distance_km * 1000.0
    return 20.0 * np.log10(4.0 * np.pi * d_m / wavelength_m)


def compute_sinr(
    gain_matrix: np.ndarray,
    active_beams: np.ndarray | list,
    config: SimConfig,
    fading: np.ndarray | None = None,
) -> np.ndarray:
    """Compute SINR per beam in linear scale.

    SINR_i = (P_i * G[i,i]) / (Σ_{j∈active, j≠i} P_j * G[j,i] + N_0 * B)

    All beams use equal power P/K. Returns array of length len(active_beams).
    """
    active = np.asarray(active_beams)
    n_active = len(active)
    if n_active == 0:
        return np.array([])

    power_per_beam = config.p_max_linear / n_active  # equal power split
    # -97 dBm is total noise power (not PSD), do NOT multiply by bandwidth
    noise_power_w = config.noise_power_linear

    # Free space path loss — use orbit height (nadir) not slant range
    # Cells are near sub-satellite point, range ≈ 550 km (not 2704 km to horizon)
    l_fs_db = free_space_path_loss_db(config.orbit_height_km, config.frequency_hz)
    l_fs_linear = 10 ** (l_fs_db / 10)

    # G_sub[i,j] = gain of active beam j towards active cell i
    g_sub = gain_matrix[np.ix_(active, active)]  # (n_active, n_active)

    # Apply fading to diagonal (desired signal)
    if fading is not None:
        signal_gains = g_sub[np.arange(n_active), np.arange(n_active)] * fading[active]
    else:
        signal_gains = g_sub[np.arange(n_active), np.arange(n_active)]

    # Received signal power = P * G / L_fs (path loss same for all beams)
    signal = power_per_beam * signal_gains / l_fs_linear

    # Interference: sum of off-diagonal received powers
    interference = np.zeros(n_active)
    for i in range(n_active):
        interf_gains = np.delete(g_sub[i], i)
        interference[i] = power_per_beam * interf_gains.sum() / l_fs_linear

    sinr = signal / (interference + noise_power_w)
    return sinr


def compute_interference_graph(
    gain_matrix: np.ndarray,
    threshold_db: float,
) -> np.ndarray:
    """Compute adjacency matrix where edge (i,j) means beam j interferes with cell i.

    Edge exists if interference contribution exceeds threshold in dB.
    """
    n = gain_matrix.shape[0]
    threshold_linear = 10 ** (threshold_db / 10)
    adj = (gain_matrix > threshold_linear).astype(np.float64)
    np.fill_diagonal(adj, 0)
    return adj
