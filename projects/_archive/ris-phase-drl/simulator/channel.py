"""Rician block-fading channel generator."""

from __future__ import annotations

import numpy as np

from .config import SimConfig


class ChannelGenerator:
    """Rician block-fading channel generator for BS-RIS-UE links."""

    def __init__(
        self, config: SimConfig, rng: np.random.Generator | None = None
    ):
        self.cfg = config
        self.rng = rng or np.random.default_rng()

    def generate(self) -> tuple[np.ndarray, np.ndarray]:
        """Generate a set of block-fading channels.

        Returns:
            H1: (N, M) complex -- BS->RIS channel
            H2: (N, K) complex -- RIS->User channel
        """
        kappa = 10 ** (self.cfg.kappa_db / 10)
        sqrt_k = np.sqrt(kappa / (kappa + 1))
        sqrt_n = np.sqrt(1 / (kappa + 1))

        # H1: BS->RIS, shape (N, M)
        H1_los = self._ula_response(self.cfg.N, self.cfg.M)
        H1_nlos = (
            self.rng.standard_normal((self.cfg.N, self.cfg.M))
            + 1j * self.rng.standard_normal((self.cfg.N, self.cfg.M))
        ) / np.sqrt(2)
        H1 = sqrt_k * H1_los + sqrt_n * H1_nlos
        H1 *= np.sqrt(self.cfg.pl_bs_ris_linear)

        # H2: RIS->User, shape (N, K)
        H2_los = self._ula_response(self.cfg.N, self.cfg.K)
        H2_nlos = (
            self.rng.standard_normal((self.cfg.N, self.cfg.K))
            + 1j * self.rng.standard_normal((self.cfg.N, self.cfg.K))
        ) / np.sqrt(2)
        H2 = sqrt_k * H2_los + sqrt_n * H2_nlos
        H2 *= np.sqrt(self.cfg.pl_ris_ue_linear)

        return H1, H2

    @staticmethod
    def _ula_response(rows: int, cols: int) -> np.ndarray:
        """ULA array response as LoS component (half-wavelength spacing)."""
        n_idx = np.arange(rows).reshape(-1, 1)
        m_idx = np.arange(cols).reshape(1, -1)
        phase = 2 * np.pi * n_idx * m_idx / max(rows, cols)
        return np.exp(1j * phase)
