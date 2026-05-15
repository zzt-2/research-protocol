"""Beam Hopping Gymnasium MDP environment."""
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from .config import SimConfig
from .antenna import hex_grid_positions, compute_gain_matrix
from .channel import compute_sinr
from .traffic import TrafficGenerator


class BHEnv(gym.Env):
    """Beam Hopping Gymnasium Environment.

    State:  (N, 4) array per beam: [demand_norm, queue_norm, channel_gain_norm, interference_agg_norm]
    Action: N-dim scores → top-K selection
    Reward: α*R_throughput + β*R_fairness - γ*P_interference

    Episode: T slots. Each step = one BH slot.
    """

    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig | None = None, seed: int | None = None):
        super().__init__()
        self.config = config or SimConfig()
        self.N = self.config.n_beams
        self.K = self.config.k_active
        self.T = self.config.t_slots

        # Positions and static gain matrix
        self.beam_positions = hex_grid_positions(self.config.n_rings)
        self.gain_matrix = compute_gain_matrix(self.config, self.beam_positions)

        # Action: scores for each beam, top-K selected
        self.action_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.N,), dtype=np.float32
        )
        # Observation: (N, 4) normalized features
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(self.N, 4), dtype=np.float32
        )

        # Traffic generator
        self.traffic = TrafficGenerator(self.config, mode='compound_poisson', seed=seed)

        # RNG
        self._rng = np.random.default_rng(seed)
        self._seed = seed

        # State
        self.queues = np.zeros(self.N, dtype=np.float64)
        self.demands = np.zeros(self.N, dtype=np.float64)
        self.fading = np.ones(self.N, dtype=np.float64)
        self.t = 0

    def reset(self, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)
            self.traffic = TrafficGenerator(self.config, mode='compound_poisson', seed=seed)

        self.t = 0
        self.queues = np.zeros(self.N, dtype=np.float64)
        self.demands = self.traffic.generate(self.beam_positions)
        # Initialize Rayleigh fading
        self.fading = self._sample_rayleigh()
        obs = self._get_obs()
        info = self._get_info()
        return obs, info

    def _sample_rayleigh(self) -> np.ndarray:
        """Sample Rayleigh fading coefficients. Mean ≈ 1 (normalized)."""
        # Rayleigh with σ such that E[|h|²] = 1: use σ=1/√(2), then h=σ*√(X²+Y²)
        # But simpler: exponential with mean 1 gives |h|², take sqrt
        return np.sqrt(self._rng.exponential(1.0, self.N)).astype(np.float64)

    def _update_fading(self):
        """Update fading with EMA for temporal correlation."""
        new_sample = self._sample_rayleigh()
        alpha = self.config.fading_alpha
        self.fading = alpha * new_sample + (1 - alpha) * self.fading

    def _get_obs(self) -> np.ndarray:
        """Build (N, 4) observation array with normalized features."""
        d_max = self.config.demand_max_mbps
        q_max = self.config.queue_capacity_mbps

        # Demand normalized to [0, 1]
        demand_norm = np.clip(self.demands / d_max, 0, 1)

        # Queue normalized to [0, 1]
        queue_norm = np.clip(self.queues / q_max, 0, 1)

        # Channel gain: diagonal of gain matrix * fading → log-normalize to [0,1]
        diag_gains = np.diag(self.gain_matrix) * self.fading
        # Log-normalize: map log-scale gains to [0,1] using tanh
        gain_db = 10 * np.log10(np.maximum(diag_gains, 1e-30))
        gain_norm = np.clip((gain_db + 50) / 100, 0, 1)  # rough [−50, 50] dB → [0, 1]

        # Interference aggregate: for each beam, sum of off-diagonal gains
        off_diag = self.gain_matrix.copy()
        np.fill_diagonal(off_diag, 0)
        interf_agg = off_diag.sum(axis=0) * self.fading
        interf_db = 10 * np.log10(np.maximum(interf_agg, 1e-30))
        interf_norm = np.clip((interf_db + 50) / 100, 0, 1)

        obs = np.stack([demand_norm, queue_norm, gain_norm, interf_norm], axis=1)
        return obs.astype(np.float32)

    def _get_info(self) -> dict:
        return {
            'demands': self.demands.copy(),
            'queues': self.queues.copy(),
            'fading': self.fading.copy(),
        }

    def step(self, action: np.ndarray):
        """Execute one BH slot.

        action: (N,) scores → top-K beams selected as active.
        """
        action = np.asarray(action, dtype=np.float64)

        # Top-K selection
        k = min(self.K, self.N)
        active_beams = np.argsort(action)[-k:]

        # Compute SINR for active beams
        sinr = compute_sinr(self.gain_matrix, active_beams, self.config, self.fading)

        # Shannon capacity per active beam (Mbps)
        capacity = np.zeros(self.N, dtype=np.float64)
        for idx, beam_i in enumerate(active_beams):
            capacity[beam_i] = (
                self.config.bandwidth_hz * np.log2(1.0 + sinr[idx]) / 1e6
            )

        # Throughput: min(capacity, demand+queue)
        total_demand = self.demands + self.queues
        served = np.minimum(capacity, total_demand)

        # Compute reward components
        # R_throughput: fraction of served beams' demand satisfied
        # (not total N-beam demand — that dilutes the signal to ~5%)
        active_demand = total_demand[active_beams].sum()
        r_throughput = served[active_beams].sum() / active_demand if active_demand > 0 else 0.0

        # R_fairness: Jain-like fairness on satisfaction ratio
        satisfaction = np.zeros(self.N)
        for i in active_beams:
            if total_demand[i] > 0:
                satisfaction[i] = served[i] / total_demand[i]
        n_active = len(active_beams)
        if n_active > 0:
            s_sum = satisfaction[active_beams].sum()
            s_sum_sq = (satisfaction[active_beams] ** 2).sum()
            r_fairness = (s_sum ** 2) / (n_active * s_sum_sq) if s_sum_sq > 0 else 1.0
        else:
            r_fairness = 1.0

        # P_interference: penalize beams with SINR below threshold (quality deficit)
        # Low SINR means high mutual interference — bad beam selection
        sinr_threshold_linear = 10 ** (self.config.sinr_threshold_db / 10)
        p_interference = 0.0
        if n_active > 0:
            deficit = np.maximum(sinr_threshold_linear - sinr, 0)
            p_interference = deficit.sum() / (n_active * sinr_threshold_linear)

        # Combined reward
        reward = (
            self.config.reward_alpha * r_throughput
            + self.config.reward_beta * r_fairness
            - self.config.reward_gamma * p_interference
        )

        # Update queues
        self.queues = np.maximum(self.queues + self.demands - served, 0)
        self.queues = np.minimum(self.queues, self.config.queue_capacity_mbps)

        # New demand for next slot
        self.demands = self.traffic.generate(self.beam_positions)

        # Update fading
        self._update_fading()

        self.t += 1
        terminated = self.t >= self.T
        truncated = False

        obs = self._get_obs()
        info = {
            'reward_throughput': r_throughput,
            'reward_fairness': r_fairness,
            'penalty_interference': p_interference,
            'served': served,
            'capacity': capacity,
            'sinr': sinr,
            'active_beams': active_beams,
            'demands': self.demands.copy(),
            'queues': self.queues.copy(),
        }

        return obs, float(reward), terminated, truncated, info
