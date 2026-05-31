"""M3: ChannelModel — Gaussian beam + Rayleigh pointing jitter.

Computes ISL capacity (Shannon) and outage probability for each candidate edge.

Channel model [L01 §II-C Eq.(3)-(5)]:
  1. Gaussian beam radius: w(d) = W₀√(1+(d/z_R)²), z_R = πW₀²/λ
  2. Received power (beam center): P_r0 = 2P₀A/(πw²)
  3. Mean pointing efficiency (Rayleigh jitter σ_J):
     η = 1 / (1 + 2(σ_J·d)²/w²)
  4. Effective SNR = (Ψ·P_r0·η/σ_N)²
  5. Capacity C = B·log₂(1+SNR)
  6. Outage probability: P(SNR_inst < SNR_min) using Rayleigh CDF
"""

import numpy as np
from . import config


class ChannelModel:
    def __init__(self, wavelength=None, w0=None, p_tx=None, bandwidth=None,
                 aperture=None, responsivity=None, sigma_noise=None,
                 sigma_jitter=None, outage_eps=None):
        self.wavelength = wavelength or config.WAVELENGTH  # m
        self.w0 = w0 or config.W0  # m
        self.p_tx = p_tx or config.P_TX  # W
        self.bandwidth = bandwidth or config.BANDWIDTH  # Hz
        self.aperture = aperture or config.APERTURE  # m²
        self.responsivity = responsivity or config.RESPONSIVITY  # A/W
        self.sigma_noise = sigma_noise or config.SIGMA_NOISE  # A
        self.sigma_jitter = sigma_jitter or config.SIGMA_JITTER  # rad
        self.outage_eps = outage_eps or config.OUTAGE_EPS

        self.z_R = np.pi * self.w0 ** 2 / self.wavelength  # Rayleigh range (m)

    def beam_radius(self, d_m):
        """Gaussian beam radius w(d) in meters. d_m in meters."""
        return self.w0 * np.sqrt(1 + (d_m / self.z_R) ** 2)

    def compute(self, distances_km):
        """Compute capacity and outage for an array of distances.

        Args:
            distances_km: 1-D array of distances in km.

        Returns:
            capacities_gbps: (n,) array, Shannon capacity in Gbps.
            outage_probs: (n,) array, outage probability.
            available: (n,) bool array, True if link is usable.
        """
        d_m = np.asarray(distances_km, dtype=float) * 1000.0  # km → m
        d_m = np.maximum(d_m, 1.0)  # avoid division by zero

        w = self.beam_radius(d_m)
        p_r0 = 2 * self.p_tx * self.aperture / (np.pi * w ** 2)

        # Pointing efficiency (Rayleigh jitter)
        sigma_r = self.sigma_jitter * d_m  # pointing error displacement (m)
        eta = 1.0 / (1 + 2 * sigma_r ** 2 / w ** 2)

        # Effective SNR
        i_eff = self.responsivity * p_r0 * eta
        snr_eff = (i_eff / self.sigma_noise) ** 2

        # Peak SNR (no jitter) for outage calculation
        i_peak = self.responsivity * p_r0
        snr_peak = (i_peak / self.sigma_noise) ** 2

        # Capacity (Gbps)
        capacities = self.bandwidth * np.log2(1 + snr_eff) / 1e9

        # Outage probability: P(r > r_th) with r_th from SNR margin
        snr_min = 1.0  # minimum SNR threshold (0 dB)
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = np.maximum(snr_peak / snr_min, 1.0)
            r_th_sq = (w ** 2 / 4) * np.log(ratio)
        # Rayleigh CDF: P(r > r_th) = exp(-r_th²/(2σ²))
        sigma_sq = sigma_r ** 2
        p_out = np.where(sigma_sq > 0, np.exp(-r_th_sq / (2 * sigma_sq + 1e-30)), 0.0)
        p_out = np.clip(p_out, 0, 1)

        available = (p_out < self.outage_eps) & (capacities > 0)
        return capacities, p_out, available

    def compute_single(self, distance_km):
        """Convenience: single distance → (capacity_gbps, p_out, available)."""
        c, p, a = self.compute(np.array([distance_km]))
        return float(c[0]), float(p[0]), bool(a[0])

    def fspl_db(self, distance_km):
        """Free-space path loss in dB (for verification)."""
        d_m = distance_km * 1000.0
        return 20 * np.log10(4 * np.pi * d_m / self.wavelength)
