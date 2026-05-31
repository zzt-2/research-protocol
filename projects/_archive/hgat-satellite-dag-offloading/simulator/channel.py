"""Channel models for G2U / G2S / U2S / ISL / L2C / CS wired links.

Fading models follow 3GPP TR 38.811 (Rician) and K2/M01 Table IV
(Shadowed-Rician). Carrier frequencies are representative S/Ka-band values.
"""

import numpy as np

from config import SimConfig

C = 3e8  # speed of light (m/s)
FREQ_G2U = 2e9   # S-band
FREQ_G2S = 20e9  # Ka-band
FREQ_U2S = 20e9
FREQ_ISL = 23e9
ATMO_LOSS_DB = 0.5  # atmospheric attenuation for G2S uplink


def free_space_path_loss(distance: float, freq_hz: float) -> float:
    """Free-space path loss in dB."""
    return 20.0 * np.log10(4.0 * np.pi * distance * freq_hz / C)


def rician_fading(rng: np.random.Generator, K: float, size=None) -> float | np.ndarray:
    """Rician fading power gain |h|^2."""
    los = np.sqrt(K / (K + 1.0))
    nlos_scale = np.sqrt(1.0 / (K + 1.0))
    cn = nlos_scale * (rng.standard_normal(size) + 1j * rng.standard_normal(size)) / np.sqrt(2)
    h = los + cn
    return np.abs(h) ** 2


def shadowed_rician_fading(rng: np.random.Generator, params: dict,
                            size=None) -> float | np.ndarray:
    """Shadowed-Rician fading power gain (K2/M01 Table IV)."""
    b0, m, Omega = params["b0"], params["m"], params["Omega"]
    los_power = rng.gamma(m, Omega / m, size=size)
    nlos_power = rng.exponential(2.0 * b0, size=size)
    return los_power + nlos_power


def compute_snr(tx_power_w: float, path_loss_db: float,
                fading_gain: float | np.ndarray, noise_power_w: float) -> float | np.ndarray:
    """Linear SNR from transmit power, path loss, fading, and noise."""
    path_loss_linear = 10.0 ** (-path_loss_db / 10.0)
    return tx_power_w * path_loss_linear * fading_gain / noise_power_w


def shannon_rate(snr_linear: float | np.ndarray, bandwidth_hz: float) -> float | np.ndarray:
    """Shannon capacity in bps."""
    return bandwidth_hz * np.log2(1.0 + snr_linear)


class ChannelModel:
    """Aggregate channel model for all link types."""

    def __init__(self, config: SimConfig, rng: np.random.Generator | None = None):
        self.cfg = config
        self.rng = rng or np.random.default_rng()
        self._deterministic = False

        self._sr_params = {
            "light": config.sr_light,
            "average": config.sr_average,
            "heavy": config.sr_heavy,
        }

    def set_deterministic(self, enabled: bool = True) -> None:
        self._deterministic = enabled

    def _rate(self, distance: float, tx_power: float, freq_hz: float,
              bandwidth: float, fading_fn, extra_loss_db: float = 0.0) -> float:
        pl = free_space_path_loss(distance, freq_hz) + extra_loss_db
        gain = 1.0 if self._deterministic else fading_fn()
        snr = compute_snr(tx_power, pl, gain, self.cfg.noise_power_w)
        return float(shannon_rate(snr, bandwidth))

    def g2u_rate(self, distance: float, tx_power: float) -> float:
        """IoTD-UAV: Rician fading, 20 MHz, S-band."""
        return self._rate(distance, tx_power, FREQ_G2U, self.cfg.bw_g2u,
                          lambda: rician_fading(self.rng, self.cfg.rician_k))

    def g2s_rate(self, distance: float, tx_power: float) -> float:
        """IoTD-LEO: Shadowed-Rician + 0.5 dB atmospheric, 15 MHz, Ka-band."""
        return self._rate(distance, tx_power, FREQ_G2S, self.cfg.bw_g2s,
                          lambda: shadowed_rician_fading(self.rng, self._sr_params[self.cfg.sr_condition]),
                          extra_loss_db=ATMO_LOSS_DB)

    def u2s_rate(self, distance: float, tx_power: float) -> float:
        """UAV-LEO: Shadowed-Rician, 15 MHz, Ka-band."""
        return self._rate(distance, tx_power, FREQ_U2S, self.cfg.bw_u2s,
                          lambda: shadowed_rician_fading(self.rng, self._sr_params[self.cfg.sr_condition]))

    def isl_rate(self, distance: float, tx_power: float) -> float:
        """LEO-LEO inter-satellite: free-space only, 1 GHz."""
        return self._rate(distance, tx_power, FREQ_ISL, self.cfg.bw_isl,
                          lambda: 1.0)

    def l2c_rate(self) -> float:
        """LEO-CS: fixed rate."""
        return self.cfg.bw_l2c

    def cs_rate(self) -> float:
        """CS wired: fixed 1 Gbps."""
        return self.cfg.rate_cs_wired
