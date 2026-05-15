"""Simulation parameters with source traceability."""
import numpy as np
from dataclasses import dataclass


@dataclass
class SimConfig:
    # === Geometry (L03: Walker-Delta 550km) ===
    orbit_height_km: float = 550.0        # L03
    cell_radius_km: float = 25.0          # L07: 25km

    # === Frequency (L01: Ku 11.45GHz) ===
    frequency_hz: float = 11.45e9         # L01

    # === Beam layout (L01: 19-beam hexagonal) ===
    n_rings: int = 2                      # 2-ring = 19 beams
    n_beams: int = 0                      # computed from n_rings
    k_active: int = 5                     # [ASSUMPTION] L05:K=4, MVE:K=5

    # === BH scheduling ===
    t_slots: int = 20                     # L04: T=13~29, mid=20

    # === Power (L01) ===
    p_max_dbm: float = 40.0              # L01: p_max=40dBm
    noise_power_dbm: float = -97.0       # L01: σ_n²=-97dBm

    # === Bandwidth (L04) ===
    bandwidth_hz: float = 30e6           # L04: B=30MHz

    # === Antenna (L07: Bessel) ===
    antenna_max_gain_dbi: float = 48.7   # L07: A_max=48.7dBi
    beam_width_3db_deg: float = 1.4      # L07: θ_3dB=1.4°

    # === Traffic (L03: compound Poisson) ===
    demand_min_mbps: float = 20.0        # L03
    demand_max_mbps: float = 700.0       # L03

    # === Reward weights (user confirmed Step 6) ===
    reward_alpha: float = 0.6            # throughput
    reward_beta: float = 0.3             # fairness
    reward_gamma: float = 0.1            # interference penalty

    # === SINR threshold for interference penalty ===
    sinr_threshold_db: float = 10.0      # [ASSUMPTION] reasonable for Ku

    # === Queue ===
    queue_capacity_mbps: float = 1000.0  # max queue backlog per beam

    # === Channel fading ===
    fading_alpha: float = 0.3            # EMA coefficient for Rayleigh fading

    # === Derived (computed in __post_init__) ===
    wavelength_m: float = 0.0
    p_max_linear: float = 0.0
    noise_power_linear: float = 0.0
    slant_range_km: float = 0.0
    ka_factor: float = 0.0

    def __post_init__(self):
        self.wavelength_m = 3e8 / self.frequency_hz
        self.p_max_linear = 10 ** (self.p_max_dbm / 10) / 1000  # dBm to Watts
        self.noise_power_linear = 10 ** (self.noise_power_dbm / 10) / 1000
        # Slant range: satellite to cell edge (conservative)
        earth_radius = 6371.0
        self.slant_range_km = np.sqrt(
            (earth_radius + self.orbit_height_km) ** 2 - earth_radius ** 2
        )
        if self.n_beams == 0:
            self.n_beams = self._count_hex_nodes(self.n_rings)
        # ka factor from 3dB beamwidth
        # u_3dB = ka * sin(θ_3dB/2) ≈ 1.6166 for first 3dB point of Airy pattern
        theta_3db_rad = np.deg2rad(self.beam_width_3db_deg)
        self.ka_factor = 1.6166 / np.sin(theta_3db_rad)

    @staticmethod
    def _count_hex_nodes(n_rings: int) -> int:
        return 3 * n_rings * (n_rings + 1) + 1
