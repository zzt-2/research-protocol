"""M2: Channel model — FSPL + atmospheric + shadow fading (TR 38.811) + SNR."""

import numpy as np
from numpy.typing import NDArray

SPEED_OF_LIGHT = 3e8  # m/s


# ── FSPL ───────────────────────────────────────────────────────────

def fspl_db(distances_km: NDArray, freq_hz: float = 12e9) -> NDArray:
    """Free Space Path Loss in dB. Shape-preserving."""
    d_m = np.asarray(distances_km) * 1e3
    d_m = np.maximum(d_m, 1.0)
    lam_m = SPEED_OF_LIGHT / freq_hz
    return 20.0 * np.log10(4.0 * np.pi * d_m / lam_m)


# ── Atmospheric attenuation (ITU-R P.676 simplified) ──────────────

def atmospheric_atten_db(elevation_deg: NDArray, a_zenith_db: float = 0.2) -> NDArray:
    """A_gas(θ) = A_zenith / sin(θ), clamped to min elevation 5°."""
    elev = np.maximum(np.asarray(elevation_deg, dtype=float), 5.0)
    return a_zenith_db / np.sin(np.radians(elev))


# ── Shadow fading (3GPP TR 38.811, LoS) ──────────────────────────

def shadow_fading_sigma_db(elevation_deg: NDArray) -> NDArray:
    """Elevation-dependent σ_SF per TR 38.811 Table 6.6.2-1.

    Piecewise linear: θ=20°→4.0dB, θ=45°→1.5dB, θ=90°→1.0dB.
    Below 20° clamped to 4.0, minimum σ=1.0.
    """
    from config import SHADOW_FADING_PARAMS
    p = SHADOW_FADING_PARAMS
    theta = np.clip(np.asarray(elevation_deg, dtype=float), 1.0, 90.0)
    sigma = np.where(
        theta <= 45,
        p["sigma_20"] + (p["sigma_45"] - p["sigma_20"]) * (theta - 20) / 25.0,
        p["sigma_45"] + (p["sigma_90"] - p["sigma_45"]) * (theta - 45) / 45.0,
    )
    sigma = np.where(theta < 20, p["sigma_20"], sigma)
    return np.maximum(sigma, p["sigma_min"])


class ShadowFadingModel:
    """Per-(UE, satellite) correlated shadow fading.

    Uses an AR(1) process per link with elevation-dependent σ and
    spatial decorrelation across satellites. This provides temporal
    correlation while avoiding the "over-smooth" trap (lag-1 < 0.95).
    """

    def __init__(
        self,
        num_ues: int,
        num_sats: int,
        dt_s: float = 10.0,
        corr_length_s: float = 40.0,
        decorrelation_dist_km: float = 500.0,
        seed: int = 0,
    ):
        self.num_ues = num_ues
        self.num_sats = num_sats
        self.rho = np.exp(-dt_s / corr_length_s)  # temporal AR(1) coefficient
        self.rng = np.random.default_rng(seed)
        # State: (num_ues, num_sats) current shadow fading in dB
        self.state = np.zeros((num_ues, num_sats))
        self._initialized = False

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.state = np.zeros((self.num_ues, self.num_sats))
        self._initialized = False

    def step(self, elevations: NDArray) -> NDArray:
        """Advance one time step.

        Parameters
        ----------
        elevations : shape (num_ues, num_sats) in degrees. Negative or zero
                     means satellite not visible.

        Returns
        -------
        shadow_fading_db : shape (num_ues, num_sats)
        """
        sigma = shadow_fading_sigma_db(np.maximum(elevations, 1.0))
        noise_std = sigma * np.sqrt(1.0 - self.rho ** 2)
        noise = self.rng.normal(0, noise_std)

        if not self._initialized:
            self.state = self.rng.normal(0, sigma)
            self._initialized = True
        else:
            self.state = self.rho * self.state + noise

        # Zero out shadow fading for non-visible satellites
        visible = elevations > 0
        self.state *= visible
        return self.state.copy()

    @property
    def theoretical_lag1(self) -> float:
        return self.rho


# ── Full channel model ─────────────────────────────────────────────

class ChannelModel:
    """FSPL + atmospheric + shadow fading → SNR → Shannon capacity."""

    def __init__(
        self,
        freq_hz: float = 12e9,
        bandwidth_hz: float = 250e6,
        eirp_dbw: float = 45.0,
        rx_gain_dbi: float = 40.0,
        noise_temp_k: float = 290.0,
        noise_figure_db: float = 2.0,
        a_zenith_db: float = 0.2,
    ):
        self.freq_hz = freq_hz
        self.bandwidth_hz = bandwidth_hz
        self.eirp_dbw = eirp_dbw
        self.rx_gain_dbi = rx_gain_dbi
        self.a_zenith_db = a_zenith_db

        self.noise_dbw = (
            -228.6
            + 10.0 * np.log10(noise_temp_k)
            + 10.0 * np.log10(bandwidth_hz)
            + noise_figure_db
        )

    def compute_snr_db(
        self,
        distances_km: NDArray,
        elevation_deg: NDArray,
        shadow_db: NDArray | None = None,
    ) -> NDArray:
        """SNR in dB. All inputs broadcast-compatible."""
        loss = fspl_db(distances_km, self.freq_hz)
        atm = atmospheric_atten_db(elevation_deg, self.a_zenith_db)
        shadow = shadow_db if shadow_db is not None else np.zeros_like(loss)
        snr = self.eirp_dbw + self.rx_gain_dbi - loss - atm - shadow - self.noise_dbw
        return snr

    @staticmethod
    def snr_to_rate_bps(snr_db: NDArray, bandwidth_hz: float) -> NDArray:
        """Shannon capacity: R = B · log₂(1 + SNR)."""
        snr_lin = np.maximum(10.0 ** (snr_db / 10.0), 0.0)
        return bandwidth_hz * np.log2(1.0 + snr_lin)

    @staticmethod
    def snr_to_rate_normalized(snr_db: NDArray, sinr_max_db: float = 22.0) -> NDArray:
        """R_norm = log₂(1+SINR) / log₂(1+SINR_max) ∈ [0, 1]."""
        cap = np.log2(1.0 + np.maximum(10.0 ** (snr_db / 10.0), 0.0))
        cap_max = np.log2(1.0 + 10.0 ** (sinr_max_db / 10.0))
        return np.clip(cap / cap_max, 0.0, 1.0)
