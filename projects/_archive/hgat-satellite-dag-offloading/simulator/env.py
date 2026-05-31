"""Gymnasium environment for HGAT satellite DAG task offloading.

Multi-IoTD: N_IOTD independent DAGs, single-agent MDP assigning one ready task per step.
Node layout: IoTD[0..n_iotd-1], UAV[n_iotd..+n_uav], LEO[..+n_leo], CS[last].

Key design:
- SimConfig 注入，物理模型构造函数注入
- RewardCalculator 独立计算，info 含奖励分解
- 不可达路径通过 action mask 排除（C3 bug 修复：不再返回 0 rate）
"""

import gymnasium as gym
import numpy as np
import torch
from torch_geometric.data import HeteroData

from channel import ChannelModel
from config import SimConfig
from dag import MultiDAGBundle, DAGTask, get_ready_tasks_multi
from orbital import OrbitalMechanics
from reward import RewardCalculator

# Per-node-type feature dimensions (must match model files)
NODE_FEAT_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}
NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]


class SatelliteDAGEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig | None = None, seed: int | None = None,
                 deterministic_channel: bool = False):
        super().__init__()
        self.cfg = config or SimConfig()
        self._seed = seed
        self._deterministic_channel = deterministic_channel

        c = self.cfg
        self._n_iotd = c.n_iotd
        self.n_uav = c.n_uav
        self.n_leo = c.n_leo
        self.n_nodes = c.n_nodes
        self._total_tasks = c.total_tasks
        self._uav_start = c.uav_start
        self._leo_start = c.leo_start
        self._cs_node = c.cs_node

        self.action_space = gym.spaces.Discrete(self._total_tasks * self.n_nodes)
        self.observation_space = gym.spaces.Graph(
            node_space=gym.spaces.Box(-np.inf, np.inf, shape=(8,), dtype=np.float32),
            edge_space=gym.spaces.Box(-np.inf, np.inf, shape=(1,), dtype=np.float32),
        )

        # Persistent components
        self._dag_bundle = MultiDAGBundle(self.cfg)
        self._reward_calc = RewardCalculator(self.cfg)

        # Episode state (populated by reset)
        self._rng: np.random.Generator | None = None
        self._all_tasks: list[DAGTask] | None = None
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
        self._iotd_visible_leos: list[list[int]] | None = None
        self._iotd_leo_distances: np.ndarray | None = None
        self._iotd_leo_elevations: np.ndarray | None = None
        self._step_count: int = 0
        self._cumulative_reward: float = 0.0
        self._step_decomp: list[dict] = []
        self._episode_counter: int = 0

    # ------------------------------------------------------------------
    # Gym interface
    # ------------------------------------------------------------------

    def reset(self, seed: int | None = None, options=None):
        super().reset(seed=seed)
        self._rng = np.random.default_rng(seed if seed is not None else self._seed)
        rng = self._rng
        c = self.cfg

        # Multi-DAG generation
        self._all_tasks, self._err_rank = self._dag_bundle.generate(rng)

        # Orbital constellation
        self._orb = OrbitalMechanics(c)
        self._orb.setup_constellation(seed=int(rng.integers(0, 2**31)))

        # Channel model
        self._cm = ChannelModel(c, rng=rng)
        if self._deterministic_channel:
            self._cm.set_deterministic(True)

        # IoTD positions: random within area
        self._iotd_positions = rng.uniform(0, c.area_size, size=(self._n_iotd, 2))

        # UAVs in a grid layout
        side = int(np.ceil(np.sqrt(self.n_uav)))
        spacing = c.area_size / (side + 1)
        positions = []
        for r in range(side):
            for col in range(side):
                if len(positions) >= self.n_uav:
                    break
                positions.append([
                    spacing * (col + 1) + rng.uniform(-spacing * 0.1, spacing * 0.1),
                    spacing * (r + 1) + rng.uniform(-spacing * 0.1, spacing * 0.1),
                ])
        self._uav_positions = np.array(positions[:self.n_uav])
        self._uav_heights = rng.uniform(*c.uav_height_range, size=self.n_uav)

        # LEO frequencies
        self._leo_freqs = rng.uniform(*c.freq_leo_range, size=self.n_leo)

        # Per-IoTD LEO visibility at t=0
        self._update_leo_visibility_all(0.0)

        # State
        self._completed_mask = np.zeros(self._total_tasks, dtype=bool)
        self._task_completion_times = np.zeros(self._total_tasks, dtype=np.float64)
        self._task_nodes = np.full(self._total_tasks, -1, dtype=np.int32)
        self._node_available = np.zeros(self.n_nodes, dtype=np.float64)
        self._step_count = 0
        self._cumulative_reward = 0.0
        self._step_decomp = []

        # Reward calculator setup
        self._reward_calc.setup(
            [t.cycles for t in self._all_tasks],
            [t.deadline for t in self._all_tasks],
        )

        obs = self._build_graph()
        info = self._get_info()
        return obs, info

    def step(self, action: int):
        valid_mask = self._get_valid_action_mask()
        if not valid_mask[action]:
            obs = self._build_graph()
            info = self._get_info()
            info["invalid_action"] = True
            return obs, -100.0, False, False, info

        task_id = action // self.n_nodes
        node_id = action % self.n_nodes
        task = self._all_tasks[task_id]
        c = self.cfg

        # Transfer time
        transfer_time = 0.0
        for pred_id in task.predecessors:
            pred_node = int(self._task_nodes[pred_id])
            if pred_node != node_id:
                rate = self._get_link_rate(pred_node, node_id)
                transfer_time += self._all_tasks[pred_id].output_data / rate

        # Entry tasks: upload input_data from owning IoTD
        if not task.predecessors and node_id != task.owning_iotd:
            rate = self._get_link_rate(task.owning_iotd, node_id)
            transfer_time += task.input_data / rate

        # Compute time
        freq = self._get_node_freq(node_id)
        compute_time = task.cycles / freq

        # Completion time
        pred_finish = max(
            (self._task_completion_times[p] for p in task.predecessors), default=0.0
        )
        completion_time = (
            max(self._node_available[node_id], pred_finish)
            + transfer_time + compute_time
        )

        # Energy
        kappa = self._get_node_kappa(node_id)
        compute_energy = kappa * freq ** 2 * task.cycles
        tx_power = self._get_node_tx_power(node_id)
        transfer_energy = tx_power * transfer_time

        # Update state
        self._completed_mask[task_id] = True
        self._task_completion_times[task_id] = completion_time
        self._task_nodes[task_id] = node_id
        self._node_available[node_id] = completion_time

        # Step reward (via RewardCalculator)
        r_step, step_decomp = self._reward_calc.compute_step_reward(
            compute_time, transfer_time, compute_energy, transfer_energy,
        )
        self._step_decomp.append(step_decomp)
        self._cumulative_reward += r_step
        self._step_count += 1

        terminated = bool(np.all(self._completed_mask))
        truncated = False
        reward = r_step

        # Episode-end penalty
        if terminated:
            penalty, pen_decomp = self._reward_calc.compute_episode_penalty(
                self._task_completion_times,
                np.array([t.deadline for t in self._all_tasks]),
                self._node_available,
                self._total_tasks,
                self._uav_start, self.n_uav,
                self._leo_start, self.n_leo,
            )
            reward += penalty
            self._cumulative_reward += penalty
            self._step_decomp.append(pen_decomp)

        obs = self._build_graph()
        info = self._get_info()
        if terminated:
            info["episode_reward_decomp"] = self._get_episode_decomposition()
            info["cumulative_reward"] = self._cumulative_reward
        return obs, float(reward), terminated, truncated, info

    # ------------------------------------------------------------------
    # Info helpers
    # ------------------------------------------------------------------

    def _get_info(self) -> dict:
        info = {"action_mask": self._get_valid_action_mask()}
        if self._step_decomp:
            info["reward_decomp"] = self._step_decomp[-1]
        return info

    def _get_episode_decomposition(self) -> dict:
        """Aggregate decomposition across all steps + penalty."""
        totals: dict[str, float] = {}
        for d in self._step_decomp:
            for k, v in d.items():
                totals[k] = totals.get(k, 0.0) + abs(v)
        total_abs = sum(totals.values()) + 1e-12
        pcts = {k: v / total_abs * 100 for k, v in totals.items()}
        return {"abs": totals, "pct": pcts, "total_reward": self._cumulative_reward}

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
                self._iotd_leo_elevations[i, j] = self._orb.elevation_angle(sat, lat, lon, t)
                self._iotd_leo_distances[i, j] = self._orb.distance_to_ground(sat, lat, lon, t)

    def _node_type(self, node_id: int) -> str:
        if node_id < self._n_iotd: return "iotd"
        if node_id < self._leo_start: return "uav"
        if node_id < self._cs_node: return "leo"
        return "cs"

    def _get_node_freq(self, node_id: int) -> float:
        t = self._node_type(node_id)
        if t == "iotd": return self.cfg.freq_iotd
        if t == "uav": return self.cfg.freq_uav
        if t == "leo": return self._leo_freqs[node_id - self._leo_start]
        return self.cfg.freq_cs

    def _get_node_kappa(self, node_id: int) -> float:
        return {"iotd": self.cfg.kappa_iotd, "uav": self.cfg.kappa_uav,
                "leo": self.cfg.kappa_leo, "cs": self.cfg.kappa_cs}[self._node_type(node_id)]

    def _get_node_tx_power(self, node_id: int) -> float:
        return {"iotd": self.cfg.tx_power_iotd, "uav": self.cfg.tx_power_uav,
                "leo": self.cfg.tx_power_leo, "cs": self.cfg.tx_power_cs}[self._node_type(node_id)]

    def _get_link_rate(self, src_node: int, dst_node: int) -> float:
        src_type, dst_type = self._node_type(src_node), self._node_type(dst_node)
        if src_node == dst_node:
            return float("inf")

        if src_type == "cs" and dst_type == "cs":
            return self._cm.cs_rate()

        if src_type == "cs" or dst_type == "cs":
            non_cs_type = dst_type if src_type == "cs" else src_type
            non_cs_node = dst_node if src_type == "cs" else src_node
            if non_cs_type == "leo":
                return self._cm.l2c_rate()
            # Relay through visible LEO
            if non_cs_type == "iotd":
                vis_leos = self._iotd_visible_leos[non_cs_node]
            else:
                vis_leos = self._iotd_visible_leos[0]
            if not vis_leos:
                return float("inf")  # unreachable → masked out by action mask
            relay_leo_node = self._leo_start + vis_leos[0]
            first_hop = self._get_link_rate(non_cs_node, relay_leo_node)
            second_hop = self._cm.l2c_rate()
            return min(first_hop, second_hop)

        if src_type == "leo" and dst_type == "leo":
            src_dist = np.mean(self._iotd_leo_distances[:, src_node - self._leo_start])
            dst_dist = np.mean(self._iotd_leo_distances[:, dst_node - self._leo_start])
            dist = max(abs(src_dist - dst_dist), 1e3)
            return self._cm.isl_rate(dist, self.cfg.tx_power_leo)

        if (src_type == "iotd" and dst_type == "leo") or (src_type == "leo" and dst_type == "iotd"):
            iotd_node = src_node if src_type == "iotd" else dst_node
            leo_node = src_node if src_type == "leo" else dst_node
            dist = self._iotd_leo_distances[iotd_node, leo_node - self._leo_start]
            return self._cm.g2s_rate(dist, self.cfg.tx_power_iotd)

        if (src_type == "iotd" and dst_type == "uav") or (src_type == "uav" and dst_type == "iotd"):
            iotd_node = src_node if src_type == "iotd" else dst_node
            uav_node = src_node if src_type == "uav" else dst_node
            uav_idx = uav_node - self._uav_start
            dx = self._uav_positions[uav_idx, 0] - self._iotd_positions[iotd_node, 0]
            dy = self._uav_positions[uav_idx, 1] - self._iotd_positions[iotd_node, 1]
            dist = np.sqrt(dx**2 + dy**2 + self._uav_heights[uav_idx]**2)
            return self._cm.g2u_rate(dist, self.cfg.tx_power_iotd)

        if (src_type == "uav" and dst_type == "leo") or (src_type == "leo" and dst_type == "uav"):
            leo_node = src_node if src_type == "leo" else dst_node
            dist = np.mean(self._iotd_leo_distances[:, leo_node - self._leo_start])
            return self._cm.u2s_rate(dist, self.cfg.tx_power_uav)

        return float("inf")  # unknown link → masked out

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build_graph(self) -> HeteroData:
        data = HeteroData()
        tasks = self._all_tasks
        c = self.cfg
        md = self._reward_calc._mean_deadline

        max_cycles = max(t.cycles for t in tasks)
        max_input = max(t.input_data for t in tasks)
        max_output = max(t.output_data for t in tasks)
        max_deadline = max(t.deadline for t in tasks)
        max_err = max(self._err_rank.values()) if self._err_rank else 1.0

        # task features [cycles, input, output, deadline, is_ready, is_done, deps_remaining, err_rank]
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

        # iotd features [freq/10GHz, load/md, pos_x, pos_y]
        iotd_feats = np.zeros((self._n_iotd, 4), dtype=np.float32)
        for i in range(self._n_iotd):
            iotd_feats[i, 0] = c.freq_iotd / 10e9
            iotd_feats[i, 1] = self._node_available[i] / md
            iotd_feats[i, 2] = self._iotd_positions[i, 0] / c.area_size
            iotd_feats[i, 3] = self._iotd_positions[i, 1] / c.area_size
        data["iotd"].x = torch.from_numpy(iotd_feats)

        # uav features [freq/10GHz, load/md, pos_x, pos_y, height/60]
        uav_feats = np.zeros((self.n_uav, 5), dtype=np.float32)
        for u in range(self.n_uav):
            node_id = self._uav_start + u
            uav_feats[u, 0] = c.freq_uav / 10e9
            uav_feats[u, 1] = self._node_available[node_id] / md
            uav_feats[u, 2] = self._uav_positions[u, 0] / c.area_size
            uav_feats[u, 3] = self._uav_positions[u, 1] / c.area_size
            uav_feats[u, 4] = self._uav_heights[u] / 60.0
        data["uav"].x = torch.from_numpy(uav_feats)

        # leo features [freq/10GHz, load/md, visible, avg_elev/90, avg_dist/2500e3]
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

        # cs features [freq/10GHz, load/md]
        data["cs"].x = torch.tensor([[c.freq_cs / 10e9, self._node_available[self._cs_node] / md]],
                                    dtype=torch.float32)

        # Edges
        dep_src, dep_dst = [], []
        for t in tasks:
            for s in t.successors:
                dep_src.append(t.task_id)
                dep_dst.append(s)
        if dep_src:
            data["task", "dep", "task"].edge_index = torch.tensor([dep_src, dep_dst], dtype=torch.long)

        data["task", "to_iotd", "iotd"].edge_index = torch.tensor(
            [[t.task_id for t in tasks], [t.owning_iotd for t in tasks]], dtype=torch.long)

        t2uav_src, t2uav_dst = [], []
        for t in tasks:
            for u in range(self.n_uav):
                t2uav_src.append(t.task_id)
                t2uav_dst.append(u)
        data["task", "to_uav", "uav"].edge_index = torch.tensor([t2uav_src, t2uav_dst], dtype=torch.long)

        t2leo_src, t2leo_dst = [], []
        for t in tasks:
            for l in self._iotd_visible_leos[t.owning_iotd]:
                t2leo_src.append(t.task_id)
                t2leo_dst.append(l)
        if t2leo_src:
            data["task", "to_leo", "leo"].edge_index = torch.tensor([t2leo_src, t2leo_dst], dtype=torch.long)

        t2cs_src, t2cs_dst = [], []
        for t in tasks:
            if self._iotd_visible_leos[t.owning_iotd]:
                t2cs_src.append(t.task_id)
                t2cs_dst.append(0)
        if t2cs_src:
            data["task", "to_cs", "cs"].edge_index = torch.tensor([t2cs_src, t2cs_dst], dtype=torch.long)

        return data

    # ------------------------------------------------------------------
    # Action masking
    # ------------------------------------------------------------------

    def _get_ready_tasks(self) -> list[int]:
        return get_ready_tasks_multi(self._all_tasks, self._completed_mask)

    def _is_node_valid(self, node_id: int, owning_iotd: int) -> bool:
        t = self._node_type(node_id)
        if t in ("iotd", "uav"):
            return True
        if t == "leo":
            return (node_id - self._leo_start) in self._iotd_visible_leos[owning_iotd]
        if t == "cs":
            return len(self._iotd_visible_leos[owning_iotd]) > 0
        return False

    def _get_valid_action_mask(self) -> np.ndarray:
        mask = np.zeros(self._total_tasks * self.n_nodes, dtype=bool)
        for task_id in self._get_ready_tasks():
            owning_iotd = self._all_tasks[task_id].owning_iotd
            for node_id in range(self.n_nodes):
                if self._is_node_valid(node_id, owning_iotd):
                    mask[task_id * self.n_nodes + node_id] = True
        return mask
