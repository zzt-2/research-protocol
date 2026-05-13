"""Gymnasium environment for HGAT satellite DAG task offloading.

Multi-IoTD extension: N_IOTD independent DAGs with global ready task pool,
single-agent MDP assigning one ready task per step.

Node layout: IoTD[0..n_iotd-1], UAV[n_iotd..+n_uav], LEO[..+n_leo], CS[last].
"""

import gymnasium as gym
import numpy as np
import torch
from torch_geometric.data import HeteroData

from channel import ChannelModel
from config import (
    AREA_SIZE,
    FREQ_CS,
    FREQ_IOTD,
    FREQ_LEO_RANGE,
    FREQ_UAV,
    KAPPA_CS,
    KAPPA_IOTD,
    KAPPA_LEO,
    KAPPA_UAV,
    N_IOTD,
    N_LEO,
    N_UAV,
    REWARD_ETA_E,
    REWARD_ETA_T,
    REWARD_LAMBDA_1,
    REWARD_LAMBDA_2,
    REWARD_LAMBDA_3,
    TX_POWER_CS,
    TX_POWER_IOTD,
    TX_POWER_LEO,
    TX_POWER_UAV,
    UAV_HEIGHT_RANGE,
)
from dag import MultiDAGBundle, get_ready_tasks_multi
from orbital import OrbitalMechanics


class SatelliteDAGEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(
        self,
        n_tasks_per_iotd: int = 20,
        n_iotd: int = N_IOTD,
        n_uav: int = N_UAV,
        n_leo: int = N_LEO,
        seed: int | None = None,
        sr_condition: str = "average",
        deterministic_channel: bool = False,
    ):
        super().__init__()
        self._n_tasks_per_iotd = n_tasks_per_iotd
        self._n_iotd = n_iotd
        self.n_uav = n_uav
        self.n_leo = n_leo
        self._total_tasks = n_iotd * n_tasks_per_iotd

        # Node layout offsets
        self._uav_start = n_iotd
        self._leo_start = n_iotd + n_uav
        self._cs_node = n_iotd + n_uav + n_leo
        self.n_nodes = self._cs_node + 1

        self._seed = seed
        self._sr_condition = sr_condition
        self._deterministic_channel = deterministic_channel

        self.action_space = gym.spaces.Discrete(self._total_tasks * self.n_nodes)
        self.observation_space = gym.spaces.Graph(
            node_space=gym.spaces.Box(-np.inf, np.inf, shape=(8,), dtype=np.float32),
            edge_space=gym.spaces.Box(-np.inf, np.inf, shape=(1,), dtype=np.float32),
        )

        # Placeholders populated by reset()
        self._rng: np.random.Generator | None = None
        self._all_tasks: list | None = None
        self._dag_bundle = MultiDAGBundle(
            n_iotd=n_iotd, tasks_per_iotd=n_tasks_per_iotd,
        )
        self._orb: OrbitalMechanics | None = None
        self._cm: ChannelModel | None = None
        self._err_rank: dict[int, float] = {}
        self._completed_mask: np.ndarray | None = None
        self._task_completion_times: np.ndarray | None = None
        self._task_nodes: np.ndarray | None = None
        self._node_available: np.ndarray | None = None
        self._leo_freqs: np.ndarray | None = None
        self._iotd_positions: np.ndarray | None = None
        self._uav_positions: np.ndarray | None = None
        self._uav_heights: np.ndarray | None = None
        # Per-IoTD LEO visibility
        self._iotd_visible_leos: list[list[int]] | None = None
        self._iotd_leo_distances: np.ndarray | None = None
        self._iotd_leo_elevations: np.ndarray | None = None
        self._step_count: int = 0
        self._cumulative_reward: float = 0.0
        self._step_rewards: list[float] = []
        self._e_max: float = 0.0
        self._mean_deadline: float = 1.0
        self._episode_counter: int = 0

    # ------------------------------------------------------------------
    # Gym interface
    # ------------------------------------------------------------------

    def reset(self, seed: int | None = None, options=None):
        super().reset(seed=seed)
        self._rng = np.random.default_rng(seed if seed is not None else self._seed)
        rng = self._rng

        # Multi-DAG generation
        self._all_tasks, self._err_rank = self._dag_bundle.generate(rng)

        # Orbital constellation
        self._orb = OrbitalMechanics(n_leo=self.n_leo)
        self._orb.setup_constellation(seed=int(rng.integers(0, 2**31)))

        # Channel model
        self._cm = ChannelModel(rng=rng, sr_condition=self._sr_condition)
        if self._deterministic_channel:
            self._cm.set_deterministic(True)

        # IoTD positions: random within area
        self._iotd_positions = rng.uniform(0, AREA_SIZE, size=(self._n_iotd, 2))

        # UAVs in a grid layout
        side = int(np.ceil(np.sqrt(self.n_uav)))
        spacing = AREA_SIZE / (side + 1)
        positions = []
        for r in range(side):
            for c in range(side):
                if len(positions) >= self.n_uav:
                    break
                positions.append([
                    spacing * (c + 1) + rng.uniform(-spacing * 0.1, spacing * 0.1),
                    spacing * (r + 1) + rng.uniform(-spacing * 0.1, spacing * 0.1),
                ])
        self._uav_positions = np.array(positions[:self.n_uav])
        self._uav_heights = rng.uniform(*UAV_HEIGHT_RANGE, size=self.n_uav)

        # LEO frequencies
        self._leo_freqs = rng.uniform(*FREQ_LEO_RANGE, size=self.n_leo)

        # Per-IoTD LEO visibility at t=0
        self._update_leo_visibility_all(0.0)

        # State
        self._completed_mask = np.zeros(self._total_tasks, dtype=bool)
        self._task_completion_times = np.zeros(self._total_tasks, dtype=np.float64)
        self._task_nodes = np.full(self._total_tasks, -1, dtype=np.int32)
        self._node_available = np.zeros(self.n_nodes, dtype=np.float64)
        self._step_count = 0
        self._cumulative_reward = 0.0
        self._step_rewards = []

        # Pre-compute normalisation constants
        tasks = self._all_tasks
        self._mean_deadline = np.mean([t.deadline for t in tasks])
        max_kf2 = max(
            KAPPA_IOTD * FREQ_IOTD**2,
            KAPPA_UAV * FREQ_UAV**2,
            KAPPA_LEO * FREQ_LEO_RANGE[1]**2,
            KAPPA_CS * FREQ_CS**2,
        )
        self._e_max = max_kf2 * sum(t.cycles for t in tasks)

        obs = self._build_graph()
        info = {"action_mask": self._get_valid_action_mask()}
        return obs, info

    def step(self, action: int):
        task_id = action // self.n_nodes
        node_id = action % self.n_nodes

        # Validate
        valid_mask = self._get_valid_action_mask()
        if not valid_mask[action]:
            obs = self._build_graph()
            return obs, -100.0, False, False, {"action_mask": valid_mask}

        task = self._all_tasks[task_id]

        # Transfer time
        transfer_time = 0.0
        for pred_id in task.predecessors:
            pred_node = int(self._task_nodes[pred_id])
            if pred_node != node_id:
                rate = self._get_link_rate(pred_node, node_id)
                data_bytes = self._all_tasks[pred_id].output_data
                transfer_time += data_bytes / rate if rate > 0 else 0.0
        # Entry tasks: upload input_data from owning IoTD
        owning_iotd_node = task.owning_iotd
        if not task.predecessors and node_id != owning_iotd_node:
            rate = self._get_link_rate(owning_iotd_node, node_id)
            transfer_time += task.input_data / rate if rate > 0 else 0.0

        # Compute time
        freq = self._get_node_freq(node_id)
        compute_time = task.cycles / freq

        # Completion time
        pred_finish = 0.0
        for pred_id in task.predecessors:
            pred_finish = max(pred_finish, self._task_completion_times[pred_id])
        completion_time = (
            max(self._node_available[node_id], pred_finish)
            + transfer_time
            + compute_time
        )

        # Energy
        kappa = self._get_node_kappa(node_id)
        compute_energy = kappa * freq**2 * task.cycles
        tx_power = self._get_node_tx_power(node_id)
        transfer_energy = tx_power * transfer_time

        # Update state
        self._completed_mask[task_id] = True
        self._task_completion_times[task_id] = completion_time
        self._task_nodes[task_id] = node_id
        self._node_available[node_id] = completion_time

        # Step reward
        md = self._mean_deadline if self._mean_deadline > 0 else 1.0
        task_time_norm = (compute_time + transfer_time) / md
        task_energy_norm = (compute_energy + transfer_energy) / self._e_max if self._e_max > 0 else 0.0
        r_step = -(REWARD_ETA_T * task_time_norm + REWARD_ETA_E * task_energy_norm)

        self._step_rewards.append(r_step)
        self._cumulative_reward += r_step
        self._step_count += 1

        # Done check
        terminated = bool(np.all(self._completed_mask))
        truncated = False
        reward = r_step

        if terminated:
            penalty = self._compute_penalty()
            reward += penalty
            self._cumulative_reward += penalty

        obs = self._build_graph()
        info = {"action_mask": self._get_valid_action_mask()}
        return obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # Link rate, node properties
    # ------------------------------------------------------------------

    def _update_leo_visibility_all(self, t: float):
        self._iotd_visible_leos = []
        self._iotd_leo_distances = np.full((self._n_iotd, self.n_leo), 2500e3)
        self._iotd_leo_elevations = np.zeros((self._n_iotd, self.n_leo))
        for i in range(self._n_iotd):
            lat = self._iotd_positions[i, 1] / 111320.0
            lon = self._iotd_positions[i, 0] / 111320.0
            visible = self._orb.get_visible_sats(lat, lon, t)
            self._iotd_visible_leos.append(visible)
            for j, sat in enumerate(self._orb.satellites):
                elev = self._orb.elevation_angle(sat, lat, lon, t)
                dist = self._orb.distance_to_ground(sat, lat, lon, t)
                self._iotd_leo_elevations[i, j] = elev
                self._iotd_leo_distances[i, j] = dist

    def _node_type(self, node_id: int) -> str:
        if node_id < self._n_iotd:
            return "iotd"
        if node_id < self._leo_start:
            return "uav"
        if node_id < self._cs_node:
            return "leo"
        return "cs"

    def _get_node_freq(self, node_id: int) -> float:
        t = self._node_type(node_id)
        if t == "iotd":
            return FREQ_IOTD
        if t == "uav":
            return FREQ_UAV
        if t == "leo":
            return self._leo_freqs[node_id - self._leo_start]
        return FREQ_CS

    def _get_node_kappa(self, node_id: int) -> float:
        t = self._node_type(node_id)
        return {"iotd": KAPPA_IOTD, "uav": KAPPA_UAV, "leo": KAPPA_LEO, "cs": KAPPA_CS}[t]

    def _get_node_tx_power(self, node_id: int) -> float:
        t = self._node_type(node_id)
        return {"iotd": TX_POWER_IOTD, "uav": TX_POWER_UAV, "leo": TX_POWER_LEO, "cs": TX_POWER_CS}[t]

    def _get_link_rate(self, src_node: int, dst_node: int) -> float:
        src_type = self._node_type(src_node)
        dst_type = self._node_type(dst_node)

        if src_node == dst_node:
            return float("inf")

        if src_type == "cs" and dst_type == "cs":
            return self._cm.cs_rate()

        # CS link (via LEO relay)
        if src_type == "cs" or dst_type == "cs":
            non_cs_type = dst_type if src_type == "cs" else src_type
            non_cs_node = dst_node if src_type == "cs" else src_node
            if non_cs_type == "leo":
                return self._cm.l2c_rate()
            # Relay through visible LEO from the non-CS endpoint
            if non_cs_type == "iotd":
                vis_leos = self._iotd_visible_leos[non_cs_node]
            else:
                vis_leos = self._iotd_visible_leos[0]
            if not vis_leos:
                return 0.0
            relay_leo_node = self._leo_start + vis_leos[0]
            first_hop = self._get_link_rate(non_cs_node, relay_leo_node)
            second_hop = self._cm.l2c_rate()
            return min(first_hop, second_hop)

        # LEO to LEO (ISL)
        if src_type == "leo" and dst_type == "leo":
            src_dist = np.mean(self._iotd_leo_distances[:, src_node - self._leo_start])
            dst_dist = np.mean(self._iotd_leo_distances[:, dst_node - self._leo_start])
            dist = max(abs(src_dist - dst_dist), 1e3)
            return self._cm.isl_rate(dist, TX_POWER_LEO)

        # IoTD to/from LEO
        if (src_type == "iotd" and dst_type == "leo") or (src_type == "leo" and dst_type == "iotd"):
            iotd_node = src_node if src_type == "iotd" else dst_node
            leo_node = src_node if src_type == "leo" else dst_node
            dist = self._iotd_leo_distances[iotd_node, leo_node - self._leo_start]
            return self._cm.g2s_rate(dist, TX_POWER_IOTD)

        # IoTD to/from UAV
        if (src_type == "iotd" and dst_type == "uav") or (src_type == "uav" and dst_type == "iotd"):
            iotd_node = src_node if src_type == "iotd" else dst_node
            uav_node = src_node if src_type == "uav" else dst_node
            uav_idx = uav_node - self._uav_start
            dx = self._uav_positions[uav_idx, 0] - self._iotd_positions[iotd_node, 0]
            dy = self._uav_positions[uav_idx, 1] - self._iotd_positions[iotd_node, 1]
            dist = np.sqrt(dx**2 + dy**2 + self._uav_heights[uav_idx]**2)
            return self._cm.g2u_rate(dist, TX_POWER_IOTD)

        # UAV to/from LEO
        if (src_type == "uav" and dst_type == "leo") or (src_type == "leo" and dst_type == "uav"):
            leo_node = src_node if src_type == "leo" else dst_node
            dist = np.mean(self._iotd_leo_distances[:, leo_node - self._leo_start])
            return self._cm.u2s_rate(dist, TX_POWER_UAV)

        return 0.0

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build_graph(self) -> HeteroData:
        data = HeteroData()
        tasks = self._all_tasks
        md = self._mean_deadline if self._mean_deadline > 0 else 1.0

        max_cycles = max(t.cycles for t in tasks)
        max_input = max(t.input_data for t in tasks)
        max_output = max(t.output_data for t in tasks)
        max_deadline = max(t.deadline for t in tasks)
        max_err = max(self._err_rank.values()) if self._err_rank else 1.0

        # -- task features [cycles, input, output, deadline, is_ready, is_done, deps_remaining, err_rank]
        ready_ids = set(self._get_ready_tasks())
        task_feats = np.zeros((self._total_tasks, 8), dtype=np.float32)
        for t in tasks:
            i = t.task_id
            task_feats[i, 0] = t.cycles / max_cycles
            task_feats[i, 1] = t.input_data / max_input
            task_feats[i, 2] = t.output_data / max_output
            task_feats[i, 3] = t.deadline / max_deadline
            task_feats[i, 4] = 1.0 if i in ready_ids else 0.0
            task_feats[i, 5] = 1.0 if self._completed_mask[i] else 0.0
            task_feats[i, 6] = sum(1 for p in t.predecessors if not self._completed_mask[p]) / max(self._total_tasks, 1)
            task_feats[i, 7] = self._err_rank.get(i, 0.0) / max_err
        data["task"].x = torch.from_numpy(task_feats)

        # -- iotd features [freq/10GHz, load/mean_deadline, pos_x, pos_y]
        iotd_feats = np.zeros((self._n_iotd, 4), dtype=np.float32)
        for i in range(self._n_iotd):
            iotd_feats[i, 0] = FREQ_IOTD / 10e9
            iotd_feats[i, 1] = self._node_available[i] / md
            iotd_feats[i, 2] = self._iotd_positions[i, 0] / AREA_SIZE
            iotd_feats[i, 3] = self._iotd_positions[i, 1] / AREA_SIZE
        data["iotd"].x = torch.from_numpy(iotd_feats)

        # -- uav features [freq/10GHz, load/mean_deadline, pos_x, pos_y, height/60]
        uav_feats = np.zeros((self.n_uav, 5), dtype=np.float32)
        for u in range(self.n_uav):
            node_id = self._uav_start + u
            uav_feats[u, 0] = FREQ_UAV / 10e9
            uav_feats[u, 1] = self._node_available[node_id] / md
            uav_feats[u, 2] = self._uav_positions[u, 0] / AREA_SIZE
            uav_feats[u, 3] = self._uav_positions[u, 1] / AREA_SIZE
            uav_feats[u, 4] = self._uav_heights[u] / 60.0
        data["uav"].x = torch.from_numpy(uav_feats)

        # -- leo features [freq/10GHz, load/mean_deadline, visible, avg_elevation/90, avg_distance/2500e3]
        leo_feats = np.zeros((self.n_leo, 5), dtype=np.float32)
        for l in range(self.n_leo):
            node_id = self._leo_start + l
            is_vis = any(l in vis for vis in self._iotd_visible_leos)
            leo_feats[l, 0] = self._leo_freqs[l] / 10e9
            leo_feats[l, 1] = self._node_available[node_id] / md
            leo_feats[l, 2] = 1.0 if is_vis else 0.0
            leo_feats[l, 3] = max(np.mean(self._iotd_leo_elevations[:, l]), 0.0) / 90.0
            leo_feats[l, 4] = np.mean(self._iotd_leo_distances[:, l]) / 2500e3
        data["leo"].x = torch.from_numpy(leo_feats)

        # -- cs features [freq/10GHz, load/mean_deadline]
        cs_load = self._node_available[self._cs_node]
        data["cs"].x = torch.tensor([[
            FREQ_CS / 10e9,
            cs_load / md,
        ]], dtype=torch.float32)

        # -- edges --
        # task -> task (DAG dependencies)
        dep_src, dep_dst = [], []
        for t in tasks:
            for s in t.successors:
                dep_src.append(t.task_id)
                dep_dst.append(s)
        if dep_src:
            data["task", "dep", "task"].edge_index = torch.tensor(
                [dep_src, dep_dst], dtype=torch.long
            )

        # task -> owning iotd
        t2iotd_src = [t.task_id for t in tasks]
        t2iotd_dst = [t.owning_iotd for t in tasks]
        data["task", "to_iotd", "iotd"].edge_index = torch.tensor(
            [t2iotd_src, t2iotd_dst], dtype=torch.long
        )

        # task -> uav (fully connected)
        t2uav_src, t2uav_dst = [], []
        for t in tasks:
            for u in range(self.n_uav):
                t2uav_src.append(t.task_id)
                t2uav_dst.append(u)
        data["task", "to_uav", "uav"].edge_index = torch.tensor(
            [t2uav_src, t2uav_dst], dtype=torch.long
        )

        # task -> leo (visible from owning IoTD)
        t2leo_src, t2leo_dst = [], []
        for t in tasks:
            for l in self._iotd_visible_leos[t.owning_iotd]:
                t2leo_src.append(t.task_id)
                t2leo_dst.append(l)
        if t2leo_src:
            data["task", "to_leo", "leo"].edge_index = torch.tensor(
                [t2leo_src, t2leo_dst], dtype=torch.long
            )

        # task -> cs (if owning IoTD has visible LEO)
        t2cs_src, t2cs_dst = [], []
        for t in tasks:
            if self._iotd_visible_leos[t.owning_iotd]:
                t2cs_src.append(t.task_id)
                t2cs_dst.append(0)
        if t2cs_src:
            data["task", "to_cs", "cs"].edge_index = torch.tensor(
                [t2cs_src, t2cs_dst], dtype=torch.long
            )

        return data

    # ------------------------------------------------------------------
    # Action masking
    # ------------------------------------------------------------------

    def _get_ready_tasks(self) -> list[int]:
        return get_ready_tasks_multi(self._all_tasks, self._completed_mask)

    def _is_node_valid(self, node_id: int, owning_iotd: int) -> bool:
        t = self._node_type(node_id)
        if t == "iotd" or t == "uav":
            return True
        if t == "leo":
            leo_idx = node_id - self._leo_start
            return leo_idx in self._iotd_visible_leos[owning_iotd]
        if t == "cs":
            return len(self._iotd_visible_leos[owning_iotd]) > 0
        return False

    def _get_valid_action_mask(self) -> np.ndarray:
        mask = np.zeros(self._total_tasks * self.n_nodes, dtype=bool)
        ready = self._get_ready_tasks()
        for task_id in ready:
            owning_iotd = self._all_tasks[task_id].owning_iotd
            for node_id in range(self.n_nodes):
                if self._is_node_valid(node_id, owning_iotd):
                    mask[task_id * self.n_nodes + node_id] = True
        return mask

    # ------------------------------------------------------------------
    # Penalty and reward decomposition
    # ------------------------------------------------------------------

    def _compute_penalty(self) -> float:
        tasks = self._all_tasks
        md = self._mean_deadline

        phi1 = 0.0
        for t in tasks:
            ct = self._task_completion_times[t.task_id]
            if ct > t.deadline:
                phi1 += (ct - t.deadline) / t.deadline
        phi1 /= self._total_tasks

        phi2 = 0.0
        for u in range(self.n_uav):
            node_id = self._uav_start + u
            phi2 += max(0.0, self._node_available[node_id] / md - 1.0)
        phi2 /= self.n_uav

        phi3 = 0.0
        for l in range(self.n_leo):
            node_id = self._leo_start + l
            phi3 += max(0.0, self._node_available[node_id] / md - 1.0)
        phi3 /= self.n_leo

        return -(REWARD_LAMBDA_1 * phi1 + REWARD_LAMBDA_2 * phi2 + REWARD_LAMBDA_3 * phi3)

    def get_episode_reward_decomposition(self) -> dict:
        tasks = self._all_tasks
        md = self._mean_deadline

        t_norm = 0.0
        e_norm = 0.0
        for t in tasks:
            node_id = int(self._task_nodes[t.task_id])
            if node_id < 0:
                continue
            freq = self._get_node_freq(node_id)
            ct = t.cycles / freq
            tt = 0.0
            for pred_id in t.predecessors:
                pn = int(self._task_nodes[pred_id])
                if pn != node_id:
                    rate = self._get_link_rate(pn, node_id)
                    tt += self._all_tasks[pred_id].output_data / rate if rate > 0 else 0.0
            owning_iotd_node = t.owning_iotd
            if not t.predecessors and node_id != owning_iotd_node:
                rate = self._get_link_rate(owning_iotd_node, node_id)
                tt += t.input_data / rate if rate > 0 else 0.0
            t_norm += (ct + tt) / md
            kappa = self._get_node_kappa(node_id)
            ce = kappa * freq**2 * t.cycles
            te = self._get_node_tx_power(node_id) * tt
            e_norm += (ce + te) / self._e_max if self._e_max > 0 else 0.0

        phi1 = 0.0
        for t in tasks:
            ct_val = self._task_completion_times[t.task_id]
            if ct_val > t.deadline:
                phi1 += (ct_val - t.deadline) / t.deadline
        phi1 /= self._total_tasks

        phi2 = 0.0
        for u in range(self.n_uav):
            node_id = self._uav_start + u
            phi2 += max(0.0, self._node_available[node_id] / md - 1.0)
        phi2 /= self.n_uav

        phi3 = 0.0
        for l in range(self.n_leo):
            node_id = self._leo_start + l
            phi3 += max(0.0, self._node_available[node_id] / md - 1.0)
        phi3 /= self.n_leo

        total = -(REWARD_ETA_T * t_norm + REWARD_ETA_E * e_norm
                  + REWARD_LAMBDA_1 * phi1 + REWARD_LAMBDA_2 * phi2 + REWARD_LAMBDA_3 * phi3)
        return {
            "T_norm": t_norm,
            "E_norm": e_norm,
            "Phi1": phi1,
            "Phi2": phi2,
            "Phi3": phi3,
            "total": total,
        }

    # ------------------------------------------------------------------
    # Convenience episode runners
    # ------------------------------------------------------------------

    def run_random_episode(self) -> dict:
        seed = (self._seed or 0) + self._episode_counter
        self._episode_counter += 1
        obs, info = self.reset(seed=seed)
        total_reward = 0.0
        done = False
        while not done:
            mask = info["action_mask"]
            valid_indices = np.where(mask)[0]
            if len(valid_indices) == 0:
                break
            action = int(self._rng.choice(valid_indices))
            obs, reward, terminated, truncated, info = self.step(action)
            total_reward += reward
            done = terminated or truncated
        return {
            "total_reward": total_reward,
            "decomposition": self.get_episode_reward_decomposition(),
        }

    def run_greedy_episode(self) -> dict:
        seed = (self._seed or 0) + self._episode_counter
        self._episode_counter += 1
        obs, info = self.reset(seed=seed)
        total_reward = 0.0
        done = False
        while not done:
            mask = info["action_mask"]
            valid_indices = np.where(mask)[0]
            if len(valid_indices) == 0:
                break
            best_action = None
            best_time = float("inf")
            ready = self._get_ready_tasks()
            for task_id in ready:
                task = self._all_tasks[task_id]
                for node_id in range(self.n_nodes):
                    act = task_id * self.n_nodes + node_id
                    if not mask[act]:
                        continue
                    freq = self._get_node_freq(node_id)
                    ct = task.cycles / freq
                    tt = 0.0
                    for pred_id in task.predecessors:
                        pn = int(self._task_nodes[pred_id])
                        if pn != node_id:
                            rate = self._get_link_rate(pn, node_id)
                            tt += self._all_tasks[pred_id].output_data / rate if rate > 0 else 0.0
                    owning_iotd_node = task.owning_iotd
                    if not task.predecessors and node_id != owning_iotd_node:
                        rate = self._get_link_rate(owning_iotd_node, node_id)
                        tt += task.input_data / rate if rate > 0 else 0.0
                    if ct + tt < best_time:
                        best_time = ct + tt
                        best_action = act
            if best_action is None:
                break
            obs, reward, terminated, truncated, info = self.step(best_action)
            total_reward += reward
            done = terminated or truncated
        return {
            "total_reward": total_reward,
            "decomposition": self.get_episode_reward_decomposition(),
        }
