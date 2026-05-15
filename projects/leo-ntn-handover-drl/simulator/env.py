"""Gym-like LEO satellite handover environment.

Multi-UE environment where each UE selects a serving satellite at each step.
State per UE: achievable rates, satellite loads, previous satellite, visibility mask.
Reward per UE: α·throughput − β·blocking − γ·switching.
"""

import numpy as np
from numpy.typing import NDArray

from .orbit import WalkerConstellation, compute_visibility, generate_ue_positions
from .channel import ChannelModel, RainFadingModel


class LEOSatHandoverEnv:
    """Multi-UE LEO handover environment with Gym-style interface."""

    def __init__(
        self,
        num_planes: int = 6,
        sats_per_plane: int = 11,
        altitude_km: float = 550.0,
        inclination_deg: float = 53.0,
        num_ues: int = 20,
        sat_capacity: int = 5,
        min_elev_deg: float = 20.0,
        duration_s: float = 3600.0,
        dt_s: float = 10.0,
        freq_hz: float = 20e9,
        bandwidth_hz: float = 250e6,
        eirp_dbw: float = 40.0,
        rx_gain_dbi: float = 0.0,
        rain_std_db: float = 5.0,
        rain_corr_s: float = 30.0,
        reward_alpha: float = 1.0,
        reward_beta: float = 10.0,
        reward_gamma: float = 2.0,
        seed: int = 42,
    ):
        self.num_ues = num_ues
        self.sat_capacity = sat_capacity
        self.min_elev = min_elev_deg
        self.reward_alpha = reward_alpha
        self.reward_beta = reward_beta
        self.reward_gamma = reward_gamma
        self.seed = seed

        # Constellation
        self.constellation = WalkerConstellation(
            num_planes=num_planes,
            sats_per_plane=sats_per_plane,
            altitude_km=altitude_km,
            inclination_deg=inclination_deg,
            duration_s=duration_s,
            dt_s=dt_s,
        )
        self.num_sats = self.constellation.num_sats
        self.num_steps = self.constellation.num_steps - 1

        # Ground UEs
        self.ue_positions = generate_ue_positions(num_ues, seed=seed)

        # Channel model with rain fading
        self.rain_model = RainFadingModel(
            num_sats=self.num_sats,
            std_db=rain_std_db,
            corr_length_s=rain_corr_s,
            dt_s=dt_s,
            seed=seed,
        )
        self.channel = ChannelModel(
            freq_hz=freq_hz,
            bandwidth_hz=bandwidth_hz,
            eirp_dbw=eirp_dbw,
            rx_gain_dbi=rx_gain_dbi,
            rain_model=self.rain_model,
        )

        # State dimensions (for DRL agents)
        self.state_dim = 3 * self.num_sats + 1  # rates + loads + prev_sat_onehot + visible_count
        self.action_dim = self.num_sats

        self._step = 0
        self._prev_sats: NDArray = np.full(num_ues, -1, dtype=int)
        self._sat_loads: NDArray = np.zeros(self.num_sats, dtype=int)
        self._done = False

    def reset(self, seed: int | None = None) -> dict:
        s = seed if seed is not None else self.seed
        self.rain_model.reset(seed=s)
        self._step = 0
        self._prev_sats = np.full(self.num_ues, -1, dtype=int)
        self._sat_loads = np.zeros(self.num_sats, dtype=int)
        self._done = False
        return self._get_obs()

    def step(self, actions: NDArray) -> tuple:
        """Advance one step.

        Parameters
        ----------
        actions : shape (num_ues,), int in [0, num_sats)

        Returns
        -------
        obs, rewards, done, info
        """
        assert not self._done, "Episode ended. Call reset()."
        assert actions.shape == (self.num_ues,)

        self._step += 1
        rain_atten = self.rain_model.step()

        # Compute distances and SNR for all (UE, sat) pairs
        sat_pos = self.constellation.get_positions(self._step)
        rewards = np.zeros(self.num_ues)
        throughput = np.zeros(self.num_ues)
        blocked = np.zeros(self.num_ues, dtype=bool)
        switched = np.zeros(self.num_ues, dtype=bool)

        # Update loads based on actions
        new_loads = np.zeros(self.num_sats, dtype=int)
        for ue in range(self.num_ues):
            new_loads[actions[ue]] += 1

        for ue in range(self.num_ues):
            sat = actions[ue]
            dist = np.linalg.norm(sat_pos[sat] - self.ue_positions[ue])
            snr = self.channel.compute_snr_db(
                np.array([dist]), rain_atten_db=rain_atten[[sat]]
            )
            rate = self.channel.compute_rates(snr)[0]

            # Blocking: satellite over capacity
            is_blocked = new_loads[sat] > self.sat_capacity
            if is_blocked:
                rate = 0.0
                blocked[ue] = True

            # Switching cost
            is_switch = (sat != self._prev_sats[ue]) and (self._prev_sats[ue] >= 0)
            switched[ue] = is_switch

            throughput[ue] = rate
            rewards[ue] = (
                self.reward_alpha * rate
                - self.reward_beta * float(is_blocked)
                - self.reward_gamma * float(is_switch)
            )

        self._sat_loads = new_loads
        self._prev_sats = actions.copy()
        self._done = self._step >= self.num_steps

        info = {
            "throughput": throughput,
            "total_throughput": throughput.sum(),
            "blocking_rate": blocked.mean(),
            "handover_count": switched.sum(),
            "step": self._step,
        }

        obs = self._get_obs()
        return obs, rewards, self._done, info

    def _get_obs(self) -> dict:
        """Return per-UE observations."""
        sat_pos = self.constellation.get_positions(self._step)
        rain_atten = self.rain_model.state.copy()

        obs = {}
        for ue in range(self.num_ues):
            visible = compute_visibility(sat_pos, self.ue_positions[ue], self.min_elev)
            dists = np.linalg.norm(sat_pos - self.ue_positions[ue][np.newaxis, :], axis=1)
            snr = self.channel.compute_snr_db(dists, rain_atten)
            rates = self.channel.compute_rates(snr)
            rates[~visible] = 0.0

            obs[ue] = {
                "rates": rates.astype(np.float32),
                "loads": self._sat_loads.astype(np.float32),
                "prev_sat": self._prev_sats[ue],
                "visible_mask": visible,
                "visible_count": int(visible.sum()),
            }
        return obs

    def get_state_vector(self, ue_idx: int, obs: dict | None = None) -> NDArray:
        """Flat state vector for DRL agent input. Shape: (state_dim,)."""
        if obs is None:
            obs = self._get_obs()
        o = obs[ue_idx]
        prev_onehot = np.zeros(self.num_sats, dtype=np.float32)
        if o["prev_sat"] >= 0:
            prev_onehot[o["prev_sat"]] = 1.0
        state = np.concatenate([
            o["rates"] / 1e9,           # Normalize to Gbps-scale
            o["loads"] / self.sat_capacity,
            prev_onehot,
            np.array([o["visible_count"] / self.num_sats], dtype=np.float32),
        ])
        return state

    def get_valid_actions(self, ue_idx: int, obs: dict | None = None) -> NDArray:
        """Boolean mask of valid (visible) actions for a UE."""
        if obs is None:
            obs = self._get_obs()
        return obs[ue_idx]["visible_mask"]
