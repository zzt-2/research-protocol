"""Bessel antenna pattern and gain matrix computation."""
import numpy as np
from scipy.special import j1

from .config import SimConfig


def gain_at_angle(theta_rad: float | np.ndarray, config: SimConfig) -> float | np.ndarray:
    """Compute antenna gain at off-boresight angle(s).

    G(θ) = G_max * [2*J1(u)/u]² where u = ka * sin(θ)
    At θ=0: limit is G_max (L'Hôpital).
    Returns linear gain (not dB).
    """
    g_max_linear = 10 ** (config.antenna_max_gain_dbi / 10)
    u = config.ka_factor * np.sin(theta_rad)
    # Handle u≈0 via small-angle limit: 2*J1(u)/u → 1 as u→0
    with np.errstate(divide='ignore', invalid='ignore'):
        pattern = np.where(
            np.abs(u) < 1e-12,
            1.0,
            (2.0 * j1(u) / u) ** 2,
        )
    return g_max_linear * pattern


def hex_grid_positions(n_rings: int) -> np.ndarray:
    """Generate hex grid positions in km (axial → cartesian)."""
    positions = []
    for q in range(-n_rings, n_rings + 1):
        for r in range(max(-n_rings, -q - n_rings), min(n_rings, -q + n_rings) + 1):
            positions.append((q + r * 0.5, r * np.sqrt(3) / 2))
    return np.array(positions, dtype=np.float64)


def compute_gain_matrix(config: SimConfig, beam_positions: np.ndarray | None = None) -> np.ndarray:
    """Compute NxN gain matrix G[i,j] = gain of beam i towards cell j (linear).

    beam_positions: (N, 2) ground positions in grid units. If None, generated from config.
    θ_ij ≈ arctan(d_ij / h) where d_ij is ground distance, h is orbit height.
    """
    if beam_positions is None:
        raw = hex_grid_positions(config.n_rings)
    else:
        raw = np.asarray(beam_positions, dtype=np.float64)

    n = len(raw)
    # Scale grid positions to km: inter-site distance = √3 * cell_radius
    scale_km = np.sqrt(3) * config.cell_radius_km
    pos_km = raw * scale_km

    # Ground distances between all cell pairs in km
    diff = pos_km[:, None, :] - pos_km[None, :, :]  # (N, N, 2)
    ground_dist = np.linalg.norm(diff, axis=2)  # (N, N)

    # Angular separation as seen from satellite
    theta = np.arctan2(ground_dist, config.orbit_height_km)

    gain_matrix = gain_at_angle(theta, config)  # (N, N) linear
    return gain_matrix
