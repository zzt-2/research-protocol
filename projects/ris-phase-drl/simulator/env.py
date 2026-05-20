"""Gymnasium environment for RIS continuous phase-shift optimization."""

from __future__ import annotations

import numpy as np
import gymnasium
from gymnasium import spaces

from .config import SimConfig
from .channel import ChannelGenerator
from .beamforming import zf_beamforming
from .reward import compute_sum_rate


class RISPhaseEnv(gymnasium.Env):
    """RIS-assisted MU-MISO environment.

    The agent controls RIS phase shifts theta in [0, 2pi)^N.
    The BS uses ZF precoding based on the resulting effective channel.
    Reward is the sum rate (bps/Hz).
    """

    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig):
        super().__init__()
        self.cfg = config
        self.rng: np.random.Generator | None = None
        self.channel = ChannelGenerator(config)

        # State: [Re(H1), Im(H1), Re(H2), Im(H2), cos(theta), sin(theta)]
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(config.obs_dim,),
            dtype=np.float32,
        )
        # Action: phase shift in [-1, 1]^N, mapped to [0, 2pi)
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(config.N,), dtype=np.float32
        )

        # Episode state
        self.H1: np.ndarray | None = None  # (N, M)
        self.H2: np.ndarray | None = None  # (N, K)
        self.theta: np.ndarray | None = None  # (N,)
        self.t: int = 0

    def reset(
        self, *, seed: int | None = None, options: dict | None = None
    ) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        self.rng = np.random.default_rng(seed)
        self.channel.rng = self.rng

        # Generate new block-fading channels
        self.H1, self.H2 = self.channel.generate()

        # Random initial phase
        self.theta = self.rng.uniform(0, 2 * np.pi, self.cfg.N)

        self.t = 0

        obs = self._get_obs()
        info = {"step": 0}
        return obs, info

    def step(
        self, action: np.ndarray
    ) -> tuple[np.ndarray, float, bool, bool, dict]:
        # action in [-1, 1]^N -> theta in [0, 2pi)^N
        self.theta = (action + 1.0) * np.pi  # [0, 2pi)

        # Effective channel: h_eff_k = h2_k^H @ diag(e^{j*theta}) @ H1
        # H_eff shape: (K, M)
        phase_shift = np.exp(1j * self.theta)  # (N,)
        diag_phi = np.diag(phase_shift)  # (N, N)
        H_eff = self.H2.conj().T @ diag_phi @ self.H1  # (K, M)

        # ZF beamforming
        W = zf_beamforming(H_eff, self.cfg.tx_power_linear, self.cfg.K)

        # Sum rate
        sum_rate, sinrs = compute_sum_rate(
            H_eff, W, self.cfg.noise_power_linear
        )

        self.t += 1
        terminated = self.t >= self.cfg.episode_len
        truncated = False

        obs = self._get_obs()
        info = {
            "sum_rate": sum_rate,
            "sinrs": sinrs,
            "step": self.t,
        }
        reward = sum_rate

        return obs, reward, terminated, truncated, info

    def _get_obs(self) -> np.ndarray:
        """Build observation: [Re(H1), Im(H1), Re(H2), Im(H2), cos(theta), sin(theta)]."""
        parts = [
            self.H1.real.ravel(),
            self.H1.imag.ravel(),
            self.H2.real.ravel(),
            self.H2.imag.ravel(),
            np.cos(self.theta),
            np.sin(self.theta),
        ]
        return np.concatenate(parts).astype(np.float32)
