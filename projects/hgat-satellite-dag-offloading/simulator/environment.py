"""Gymnasium environment for HGAT satellite DAG task offloading.

Ties together orbital mechanics, channel models, and DAG generation into
a single-agent MDP where each step assigns one ready task to a compute node.
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
from dag import DAGGenerator, compute_err_priority, get_ready_tasks
from orbital import OrbitalMechanics

# Node-type constants used for indexing within the node array
_NODE_IOTD = 0
_NODE_UAV_START = 1
_NODE_LEO_START = 1 + N_UAV
_NODE_CS = 1 + N_UAV + N_LEO


class SatelliteDAGEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(
        self,
        n_tasks: int = 20,
        n_uav: int = N_UAV,
        n_leo: int = N_LEO,
        seed: int | None = None,
        sr_condition: str = "average",
        deterministic_channel: bool = False,
    ):
        super().__init__()
        self.n_tasks = n_tasks
        self.n_uav = n_uav
        self.n_leo = n_leo
        self.n_nodes = 2 + n_uav + n_leo  # IoTD + UAVs + LEOs + CS
        self._seed = seed
        self._sr_condition = sr_condition
        self._deterministic_channel = deterministic_channel

        self.action_space = gym.spaces.Discrete(n_tasks * self.n_nodes)
        self.observation_space = gym.spaces.Graph(
            node_space=gym.spaces.Box(-np.inf, np.inf, shape=(8,), dtype=np.float32),
            edge_space=gym.spaces.Box(-np.inf, np.inf, shape=(1,), dtype=np.float32),
        )

        # Placeholders populated by reset()
        self._rng: np.random.Generator | None = None
        self.dag = None
        self._dag_gen = DAGGenerator(n_tasks=n_tasks)
        self._orb = OrbitalMechanics(n_leo=n_leo)
        self._cm: ChannelModel | None = None
        self._err_rank: dict[int, float] = {}
        self._completed_mask: np.ndarray | None = None
        self._task_completion_times: np.ndarray | None = None
        self._task_nodes: np.ndarray | None = None
        self._node_available: np.ndarray | None = None
        self._leo_freqs: np.ndarray | None = None
        self._iotd_pos: np.ndarray | None = None
        self._uav_positions: np.ndarray | None = None
        self._uav_heights: np.ndarray | None = None
        self._visible_leos: list[int] | None = None
        self._leo_elevations: np.ndarray | None = None
        self._leo_distances: np.ndarray | None = None
        self._step_count: int = 0
        self._cumulative_reward: float = 0.0
        self._step_rewards: list[float] = []
        self._e_max: float = 0.0
        self._mean_deadline: float = 1.0

    # ------------------------------------------------------------------
    # Gym interface
    # ------------------------------------------------------------------

    def reset(self, seed: int | None = None, options=None):
        super().reset(seed=seed)
        self._rng = np.random.default_rng(seed if seed is not None else self._seed)
        rng = self._rng

        # DAG
        self.dag = self._dag_gen.generate(rng)
        self._err_rank = compute_err_rank = compute_err_priority(self.dag)

        # Orbital constellation
        self._orb = OrbitalMechanics(n_leo=self.n_leo)
        self._orb.setup_constellation(seed=int(rng.integers(0, 2**31)))

        # Channel model
        self._cm = ChannelModel(rng=rng, sr_condition=self._sr_condition)
        if self._deterministic_channel:
            self._cm.set_deterministic(True)

        # IoTD at area center
        self._iotd_pos = np.array([AREA_SIZE / 2.0, AREA_SIZE / 2.0])

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
        self._uav_positions = np.array(positions[: self.n_uav])
        self._uav_heights = rng.uniform(*UAV_HEIGHT_RANGE, size=self.n_uav)

        # LEO frequencies (sampled once per episode)
        self._leo_freqs = rng.uniform(*FREQ_LEO_RANGE, size=self.n_leo)

        # LEO visibility at t=0
        self._update_leo_visibility(0.0)

        # State
        self._completed_mask = np.zeros(self.n_tasks, dtype=bool)
        self._task_completion_times = np.zeros(self.n_tasks, dtype=np.float64)
        self._task_nodes = np.full(self.n_tasks, -1, dtype=np.int32)
        self._node_available = np.zeros(self.n_nodes, dtype=np.float64)
        self._step_count = 0
        self._cumulative_reward = 0.0
        self._step_rewards = []

        # Pre-compute normalisation constants
        tasks = self.dag.tasks
        self._mean_deadline = np.mean([t.deadline for t in tasks])
        # E_max: true worst case across all node types (max κ×f²), not just IoTD
        max_kf2 = max(
            KAPPA_IOTD * FREQ_IOTD ** 2,
            KAPPA_UAV * FREQ_UAV ** 2,
            KAPPA_LEO * FREQ_LEO_RANGE[1] ** 2,
            KAPPA_CS * FREQ_CS ** 2,
        )
        self._e_max = max_kf2 * sum(t.cycles for t in tasks)

        obs = self._build_graph()
        info = {"action_mask": self._get_valid_action_mask()}
        return obs, info

    def step(self, action: int):
        task_id = action // self.n_nodes
        node_id = action % self.n_nodes

        # Validate
        ready = self._get_ready_tasks()
        valid_mask = self._get_valid_action_mask()
        if not valid_mask[action]:
            # Invalid action: heavy penalty, don't change state
            obs = self._build_graph()
            return obs, -100.0, False, False, {"action_mask": valid_mask}

        task = self.dag.tasks[task_id]

        # Compute transfer time (sum over completed predecessors on different nodes)
        transfer_time = 0.0
        for pred_id in task.predecessors:
            pred_node = int(self._task_nodes[pred_id])
            if pred_node != node_id:
                rate = self._get_link_rate(pred_node, node_id)
                data_bytes = self.dag.tasks[pred_id].output_data
                transfer_time += data_bytes / rate if rate > 0 else 0.0

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

    def _update_leo_visibility(self, t: float):
        lat, lon = self._iotd_pos[1] / 111320.0, self._iotd_pos[0] / 111320.0
        self._visible_leos = self._orb.get_visible_sats(lat, lon, t)
        self._leo_elevations = np.zeros(self.n_leo)
        self._leo_distances = np.full(self.n_leo, 2500e3)
        for i, sat in enumerate(self._orb.satellites):
            elev = self._orb.elevation_angle(sat, lat, lon, t)
            dist = self._orb.distance_to_ground(sat, lat, lon, t)
            self._leo_elevations[i] = elev
            self._leo_distances[i] = dist

    def _node_type(self, node_id: int) -> str:
        if node_id == _NODE_IOTD:
            return "iotd"
        if node_id < _NODE_LEO_START:
            return "uav"
        if node_id < _NODE_CS:
            return "leo"
        return "cs"

    def _get_node_freq(self, node_id: int) -> float:
        t = self._node_type(node_id)
        if t == "iotd":
            return FREQ_IOTD
        if t == "uav":
            return FREQ_UAV
        if t == "leo":
            return self._leo_freqs[node_id - _NODE_LEO_START]
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

        # CS to CS (same node, but caller should handle this)
        if src_type == "cs" and dst_type == "cs":
            return self._cm.cs_rate()

        # CS link (via LEO relay): CS is always reached through a visible LEO.
        # The rate is the bottleneck of (uplink to LEO) + (LEO-to-CS wired).
        if src_type == "cs" or dst_type == "cs":
            non_cs_type = dst_type if src_type == "cs" else src_type
            non_cs_node = dst_node if src_type == "cs" else src_node

            # If the other end is a LEO, direct l2c_rate
            if non_cs_type == "leo":
                return self._cm.l2c_rate()

            # Otherwise route through the first visible LEO
            if not self._visible_leos:
                return 1.0  # fallback: no visible LEO
            relay_leo_idx = self._visible_leos[0]
            relay_node = _NODE_LEO_START + relay_leo_idx

            # First hop: non_cs -> LEO
            first_hop = self._get_link_rate(non_cs_node, relay_node)
            # Second hop: LEO -> CS (fixed 1 Gbps)
            second_hop = self._cm.l2c_rate()
            # Bottleneck rate
            return min(first_hop, second_hop)

        # LEO to LEO (ISL)
        if src_type == "leo" and dst_type == "leo":
            dist = abs(self._leo_distances[src_node - _NODE_LEO_START]
                       - self._leo_distances[dst_node - _NODE_LEO_START])
            dist = max(dist, 1e3)
            return self._cm.isl_rate(dist, TX_POWER_LEO)

        # IoTD to/from LEO
        if (src_type == "iotd" and dst_type == "leo") or (src_type == "leo" and dst_type == "iotd"):
            leo_node = src_node if src_type == "leo" else dst_node
            dist = self._leo_distances[leo_node - _NODE_LEO_START]
            return self._cm.g2s_rate(dist, TX_POWER_IOTD)

        # IoTD to/from UAV
        if (src_type == "iotd" and dst_type == "uav") or (src_type == "uav" and dst_type == "iotd"):
            uav_node = src_node if src_type == "uav" else dst_node
            uav_idx = uav_node - _NODE_UAV_START
            dx = self._uav_positions[uav_idx, 0] - self._iotd_pos[0]
            dy = self._uav_positions[uav_idx, 1] - self._iotd_pos[1]
            dist = np.sqrt(dx**2 + dy**2 + self._uav_heights[uav_idx]**2)
            return self._cm.g2u_rate(dist, TX_POWER_IOTD)

        # UAV to/from LEO
        if (src_type == "uav" and dst_type == "leo") or (src_type == "leo" and dst_type == "uav"):
            leo_node = src_node if src_type == "leo" else dst_node
            uav_node = src_node if src_type == "uav" else dst_node
            dist = self._leo_distances[leo_node - _NODE_LEO_START]
            return self._cm.u2s_rate(dist, TX_POWER_UAV)

        return 1.0  # fallback

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build_graph(self) -> HeteroData:
        data = HeteroData()
        tasks = self.dag.tasks
        md = self._mean_deadline if self._mean_deadline > 0 else 1.0

        # Normalisation constants
        max_cycles = max(t.cycles for t in tasks)
        max_input = max(t.input_data for t in tasks)
        max_output = max(t.output_data for t in tasks)
        max_deadline = max(t.deadline for t in tasks)
        max_err = max(self._err_rank.values()) if self._err_rank else 1.0

        # -- task features [cycles, input, output, deadline, is_ready, is_done, deps_remaining, err_rank]
        ready_ids = set(self._get_ready_tasks())
        task_feats = np.zeros((self.n_tasks, 8), dtype=np.float32)
        for i, t in enumerate(tasks):
            task_feats[i, 0] = t.cycles / max_cycles
            task_feats[i, 1] = t.input_data / max_input
            task_feats[i, 2] = t.output_data / max_output
            task_feats[i, 3] = t.deadline / max_deadline
            task_feats[i, 4] = 1.0 if i in ready_ids else 0.0
            task_feats[i, 5] = 1.0 if self._completed_mask[i] else 0.0
            task_feats[i, 6] = sum(1 for p in t.predecessors if not self._completed_mask[p]) / self.n_tasks
            task_feats[i, 7] = self._err_rank.get(i, 0.0) / max_err
        data["task"].x = torch.from_numpy(task_feats)

        # -- iotd features [freq/10GHz, load/mean_deadline, pos_x, pos_y]
        iotd_load = self._node_available[_NODE_IOTD]
        data["iotd"].x = torch.tensor([[
            FREQ_IOTD / 10e9,
            iotd_load / md,
            self._iotd_pos[0] / AREA_SIZE,
            self._iotd_pos[1] / AREA_SIZE,
        ]], dtype=torch.float32)

        # -- uav features [freq/10GHz, load/mean_deadline, pos_x, pos_y, height/60]
        uav_feats = np.zeros((self.n_uav, 5), dtype=np.float32)
        for u in range(self.n_uav):
            node_id = _NODE_UAV_START + u
            uav_feats[u, 0] = FREQ_UAV / 10e9
            uav_feats[u, 1] = self._node_available[node_id] / md
            uav_feats[u, 2] = self._uav_positions[u, 0] / AREA_SIZE
            uav_feats[u, 3] = self._uav_positions[u, 1] / AREA_SIZE
            uav_feats[u, 4] = self._uav_heights[u] / 60.0
        data["uav"].x = torch.from_numpy(uav_feats)

        # -- leo features [freq/10GHz, load/mean_deadline, visible, elevation/90, distance/2500e3]
        leo_feats = np.zeros((self.n_leo, 5), dtype=np.float32)
        for l in range(self.n_leo):
            node_id = _NODE_LEO_START + l
            is_vis = 1.0 if l in self._visible_leos else 0.0
            leo_feats[l, 0] = self._leo_freqs[l] / 10e9
            leo_feats[l, 1] = self._node_available[node_id] / md
            leo_feats[l, 2] = is_vis
            leo_feats[l, 3] = max(self._leo_elevations[l], 0.0) / 90.0
            leo_feats[l, 4] = self._leo_distances[l] / 2500e3
        data["leo"].x = torch.from_numpy(leo_feats)

        # -- cs features [freq/10GHz, load/mean_deadline]
        cs_load = self._node_available[_NODE_CS]
        data["cs"].x = torch.tensor([[
            FREQ_CS / 10e9,
            cs_load / md,
        ]], dtype=torch.float32)

        # -- edges --
        # task -> task (DAG dependencies: parent -> child)
        dep_src, dep_dst = [], []
        for src, dst in self.dag.edges:
            dep_src.append(src)
            dep_dst.append(dst)
        if dep_src:
            data["task", "dep", "task"].edge_index = torch.tensor(
                [dep_src, dep_dst], dtype=torch.long
            )

        # task -> iotd (fully connected)
        t2iotd_src = list(range(self.n_tasks))
        t2iotd_dst = [0] * self.n_tasks
        data["task", "to_iotd", "iotd"].edge_index = torch.tensor(
            [t2iotd_src, t2iotd_dst], dtype=torch.long
        )

        # task -> uav (fully connected)
        t2uav_src = []
        t2uav_dst = []
        for t in range(self.n_tasks):
            for u in range(self.n_uav):
                t2uav_src.append(t)
                t2uav_dst.append(u)
        data["task", "to_uav", "uav"].edge_index = torch.tensor(
            [t2uav_src, t2uav_dst], dtype=torch.long
        )

        # task -> leo (only visible)
        t2leo_src, t2leo_dst = [], []
        for t in range(self.n_tasks):
            for l in self._visible_leos:
                t2leo_src.append(t)
                t2leo_dst.append(l)
        if t2leo_src:
            data["task", "to_leo", "leo"].edge_index = torch.tensor(
                [t2leo_src, t2leo_dst], dtype=torch.long
            )

        # task -> cs (only if >= 1 LEO visible)
        if self._visible_leos:
            t2cs_src = list(range(self.n_tasks))
            t2cs_dst = [0] * self.n_tasks
            data["task", "to_cs", "cs"].edge_index = torch.tensor(
                [t2cs_src, t2cs_dst], dtype=torch.long
            )

        return data

    # ------------------------------------------------------------------
    # Action masking
    # ------------------------------------------------------------------

    def _get_ready_tasks(self) -> list[int]:
        return get_ready_tasks(self.dag, self._completed_mask)

    def _is_node_valid(self, node_id: int) -> bool:
        t = self._node_type(node_id)
        if t == "iotd" or t == "uav":
            return True
        if t == "leo":
            leo_idx = node_id - _NODE_LEO_START
            return leo_idx in self._visible_leos
        if t == "cs":
            return len(self._visible_leos) > 0
        return False

    def _get_valid_action_mask(self) -> np.ndarray:
        mask = np.zeros(self.n_tasks * self.n_nodes, dtype=bool)
        ready = self._get_ready_tasks()
        for task_id in ready:
            for node_id in range(self.n_nodes):
                if self._is_node_valid(node_id):
                    mask[task_id * self.n_nodes + node_id] = True
        return mask

    # ------------------------------------------------------------------
    # Penalty and reward decomposition
    # ------------------------------------------------------------------

    def _compute_penalty(self) -> float:
        tasks = self.dag.tasks
        md = self._mean_deadline

        # Phi1: deadline violation
        phi1 = 0.0
        for t in tasks:
            ct = self._task_completion_times[t.task_id]
            if ct > t.deadline:
                phi1 += (ct - t.deadline) / t.deadline
        phi1 /= self.n_tasks

        # Phi2: UAV overload
        phi2 = 0.0
        for u in range(self.n_uav):
            node_id = _NODE_UAV_START + u
            load = self._node_available[node_id]
            phi2 += max(0.0, load / md - 1.0)
        phi2 /= self.n_uav

        # Phi3: LEO overload
        phi3 = 0.0
        for l in range(self.n_leo):
            node_id = _NODE_LEO_START + l
            load = self._node_available[node_id]
            phi3 += max(0.0, load / md - 1.0)
        phi3 /= self.n_leo

        return -(REWARD_LAMBDA_1 * phi1 + REWARD_LAMBDA_2 * phi2 + REWARD_LAMBDA_3 * phi3)

    def get_episode_reward_decomposition(self) -> dict:
        tasks = self.dag.tasks
        md = self._mean_deadline

        # T_norm and E_norm (cumulative across episode)
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
                    tt += self.dag.tasks[pred_id].output_data / rate if rate > 0 else 0.0
            t_norm += (ct + tt) / md
            kappa = self._get_node_kappa(node_id)
            ce = kappa * freq**2 * t.cycles
            te = self._get_node_tx_power(node_id) * tt
            e_norm += (ce + te) / self._e_max if self._e_max > 0 else 0.0

        # Penalties
        phi1 = 0.0
        for t in tasks:
            ct_val = self._task_completion_times[t.task_id]
            if ct_val > t.deadline:
                phi1 += (ct_val - t.deadline) / t.deadline
        phi1 /= self.n_tasks

        phi2 = 0.0
        for u in range(self.n_uav):
            node_id = _NODE_UAV_START + u
            phi2 += max(0.0, self._node_available[node_id] / md - 1.0)
        phi2 /= self.n_uav

        phi3 = 0.0
        for l in range(self.n_leo):
            node_id = _NODE_LEO_START + l
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
        obs, info = self.reset(seed=self._seed)
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
        obs, info = self.reset(seed=self._seed)
        total_reward = 0.0
        done = False
        while not done:
            mask = info["action_mask"]
            valid_indices = np.where(mask)[0]
            if len(valid_indices) == 0:
                break
            # Greedy: pick (task, node) with minimum compute_time + transfer_time
            best_action = None
            best_time = float("inf")
            ready = self._get_ready_tasks()
            for task_id in ready:
                task = self.dag.tasks[task_id]
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
                            tt += self.dag.tasks[pred_id].output_data / rate if rate > 0 else 0.0
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
