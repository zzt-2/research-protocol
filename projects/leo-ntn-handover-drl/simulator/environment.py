"""M4: Gymnasium-compatible LEO handover environment.

Multi-UE environment. Each UE selects a serving satellite at each step.
Per-UE observation: normalized SINR, elevation, load, connection status.
Per-UE reward: v2 normalized reward (r = w_r·R + w_l·L - w_b·B - w_h·H).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from .orbit import WalkerConstellation, compute_elevation_batch, compute_visibility, generate_ue_positions
from .channel import ChannelModel, ShadowFadingModel
from .reward import compute_reward, decompose_reward


class LEOSatHandoverEnv:
    """Multi-UE LEO satellite handover environment."""

    def __init__(
        self,
        num_planes: int = cfg.NUM_PLANES,
        sats_per_plane: int = cfg.SATS_PER_PLANE,
        altitude_km: float = cfg.ORBIT_ALTITUDE_KM,
        inclination_deg: float = cfg.INCLINATION_DEG,
        num_ues: int = cfg.NUM_UES,
        sat_capacity: int = cfg.SAT_CAPACITY,
        min_elev_deg: float = cfg.MIN_ELEVATION_DEG,
        duration_s: float = cfg.SIM_DURATION_S,
        dt_s: float = cfg.DT_S,
        freq_hz: float = cfg.CARRIER_FREQ_HZ,
        bandwidth_hz: float = cfg.BANDWIDTH_HZ,
        eirp_dbw: float = cfg.TX_EIRP_DBW,
        rx_gain_dbi: float = cfg.RX_GAIN_DBI,
        seed: int = 42,
    ):
        self.num_ues = num_ues
        self.sat_capacity = sat_capacity
        self.min_elev = min_elev_deg
        self.seed = seed

        # M1: Constellation
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

        # UE positions (fixed)
        self.ue_positions = generate_ue_positions(
            num_ues,
            center_lat_deg=cfg.UE_CENTER_LAT,
            center_lon_deg=cfg.UE_CENTER_LON,
            spread_deg=cfg.UE_SPREAD_DEG,
            seed=seed,
        )

        # M2: Channel model
        self.channel = ChannelModel(
            freq_hz=freq_hz,
            bandwidth_hz=bandwidth_hz,
            eirp_dbw=eirp_dbw,
            rx_gain_dbi=rx_gain_dbi,
        )
        self.shadow_model = ShadowFadingModel(
            num_ues=num_ues,
            num_sats=self.num_sats,
            dt_s=dt_s,
            seed=seed,
        )

        # State
        self._step = 0
        self._prev_sats: NDArray = np.full(num_ues, -1, dtype=int)
        self._sat_loads: NDArray = np.zeros(self.num_sats, dtype=int)
        self._t_conn: NDArray = np.zeros(num_ues, dtype=int)  # connection time in steps
        self._done = False

        # Observation dimensions
        # Per-UE: [sinr_norm(N), elev_norm(N), load_norm(N), is_current(N), t_conn_norm]
        self.obs_dim = 4 * self.num_sats + 1
        self.action_dim = self.num_sats

    def reset(self, seed: int | None = None) -> NDArray:
        """Reset environment. Returns obs array shape (num_ues, obs_dim)."""
        s = seed if seed is not None else self.seed
        self.shadow_model.reset(seed=s + 100 if s else None)
        self._step = 0
        self._prev_sats = np.full(self.num_ues, -1, dtype=int)
        self._sat_loads = np.zeros(self.num_sats, dtype=int)
        self._t_conn = np.zeros(self.num_ues, dtype=int)
        self._done = False
        return self._get_obs()

    def step(self, actions: NDArray) -> tuple[NDArray, NDArray, bool, dict]:
        """Advance one step.

        Parameters
        ----------
        actions : shape (num_ues,), int in [0, num_sats)

        Returns
        -------
        obs: (num_ues, obs_dim), rewards: (num_ues,), done: bool, info: dict
        """
        assert not self._done
        assert actions.shape == (self.num_ues,)

        self._step += 1
        sat_pos = self.constellation.get_positions(self._step)

        # Compute elevation and distance for all (UE, sat) pairs
        elevations = np.zeros((self.num_ues, self.num_sats))
        distances = np.zeros((self.num_ues, self.num_sats))
        for ue in range(self.num_ues):
            d = sat_pos - self.ue_positions[ue][np.newaxis, :]
            distances[ue] = np.linalg.norm(d, axis=1)
            elevations[ue] = compute_elevation_batch(sat_pos, self.ue_positions[ue])

        # Shadow fading step
        shadow_db = self.shadow_model.step(elevations)

        # SNR and normalized rate
        snr_db = np.zeros((self.num_ues, self.num_sats))
        r_norm = np.zeros((self.num_ues, self.num_sats))
        for ue in range(self.num_ues):
            snr_db[ue] = self.channel.compute_snr_db(distances[ue], elevations[ue], shadow_db[ue])
            r_norm[ue] = self.channel.snr_to_rate_normalized(snr_db[ue], cfg.SINR_MAX_DB)

        # Compute new satellite loads based on all UE actions
        new_loads = np.zeros(self.num_sats, dtype=int)
        for ue in range(self.num_ues):
            new_loads[actions[ue]] += 1

        # Per-UE reward computation
        rewards = np.zeros(self.num_ues)
        blocked = np.zeros(self.num_ues, dtype=bool)
        switched = np.zeros(self.num_ues, dtype=bool)
        throughput_bps = np.zeros(self.num_ues)

        for ue in range(self.num_ues):
            sat = actions[ue]
            is_blocked = new_loads[sat] > self.sat_capacity
            is_switch = (sat != self._prev_sats[ue]) and (self._prev_sats[ue] >= 0)

            if is_blocked:
                # B=1: no throughput, no capacity
                ue_r_norm = 0.0
                ue_l_norm = 0.0
                blocked[ue] = True
            else:
                ue_r_norm = r_norm[ue, sat]
                # L_norm = 1 - (load before this UE joins) / capacity
                load_before = new_loads[sat] - 1  # subtract self
                ue_l_norm = max(1.0 - load_before / self.sat_capacity, 0.0)
                throughput_bps[ue] = self.channel.snr_to_rate_bps(
                    snr_db[ue, sat:sat + 1], self.channel.bandwidth_hz
                )[0]

            switched[ue] = is_switch
            rewards[ue] = compute_reward(ue_r_norm, ue_l_norm, is_blocked, is_switch)

            # Update connection time
            if is_switch or self._prev_sats[ue] < 0:
                self._t_conn[ue] = 0
            else:
                self._t_conn[ue] += 1

        # Update loads: for blocked UEs, revert their satellite selection
        # (they stay on previous satellite or have no connection)
        effective_loads = np.zeros(self.num_sats, dtype=int)
        for ue in range(self.num_ues):
            if not blocked[ue] and actions[ue] < self.num_sats:
                effective_loads[actions[ue]] += 1
        self._sat_loads = effective_loads

        self._prev_sats = actions.copy()
        self._done = self._step >= self.num_steps

        info = {
            "throughput_bps": throughput_bps,
            "total_throughput_bps": throughput_bps.sum(),
            "blocking_rate": blocked.mean(),
            "handover_count": switched.sum(),
            "snr_db": snr_db,
            "step": self._step,
            "reward_decomposition": decompose_reward(
                r_norm[np.arange(self.num_ues), actions],
                np.array([max(1.0 - (new_loads[actions[ue]] - 1) / self.sat_capacity, 0.0)
                          if not blocked[ue] else 0.0 for ue in range(self.num_ues)]),
                blocked,
                switched,
            ),
        }

        return self._get_obs(), rewards, self._done, info

    def _get_obs(self) -> NDArray:
        """Per-UE observation array. Shape: (num_ues, obs_dim)."""
        sat_pos = self.constellation.get_positions(self._step)
        obs = np.zeros((self.num_ues, self.obs_dim), dtype=np.float32)

        for ue in range(self.num_ues):
            d = sat_pos - self.ue_positions[ue][np.newaxis, :]
            distances = np.linalg.norm(d, axis=1)
            elevations = compute_elevation_batch(sat_pos, self.ue_positions[ue])

            snr_db = self.channel.compute_snr_db(distances, elevations)
            sinr_norm = self.channel.snr_to_rate_normalized(snr_db, cfg.SINR_MAX_DB)

            # Elevation normalized to [0, 1]
            elev_norm = np.clip(
                (elevations - self.min_elev) / (cfg.ELEV_MAX_DEG - self.min_elev), 0.0, 1.0
            )
            elev_norm[elevations < self.min_elev] = 0.0

            # Load normalized
            load_norm = 1.0 - self._sat_loads / self.sat_capacity

            # Current serving satellite one-hot
            is_current = np.zeros(self.num_sats, dtype=np.float32)
            if self._prev_sats[ue] >= 0:
                is_current[self._prev_sats[ue]] = 1.0

            # Connection time normalized (capped at 100 steps = 1000s)
            t_conn_norm = min(self._t_conn[ue] / 100.0, 1.0)

            obs[ue] = np.concatenate([
                sinr_norm.astype(np.float32),
                elev_norm.astype(np.float32),
                load_norm.astype(np.float32),
                is_current,
                np.array([t_conn_norm], dtype=np.float32),
            ])

        return obs

    def get_valid_actions(self) -> NDArray:
        """Boolean mask of valid actions per UE. Shape: (num_ues, num_sats)."""
        sat_pos = self.constellation.get_positions(self._step)
        mask = np.zeros((self.num_ues, self.num_sats), dtype=bool)
        for ue in range(self.num_ues):
            mask[ue] = compute_visibility(sat_pos, self.ue_positions[ue], self.min_elev)
        return mask

    def get_per_ue_obs(self, ue_idx: int) -> NDArray:
        """Single UE observation. Shape: (obs_dim,)."""
        return self._get_obs()[ue_idx]
