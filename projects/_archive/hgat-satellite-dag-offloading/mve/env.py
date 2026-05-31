"""env.py - Minimal satellite edge DAG task offloading environment for MVE."""
import numpy as np
import torch
from torch_geometric.data import Data, HeteroData

# 5 servers: IoTD, UAV, LEO, LEO, CS
SERVERS = [
    {"type": "iotd", "freq": 0.2e9, "bw": 1e6, "power": 0.5},
    {"type": "uav", "freq": 0.5e9, "bw": 5e6, "power": 2.0},
    {"type": "leo", "freq": 1.5e9, "bw": 10e6, "power": 5.0},
    {"type": "leo", "freq": 1.5e9, "bw": 10e6, "power": 5.0},
    {"type": "cs", "freq": 3.0e9, "bw": 50e6, "power": 10.0},
]

# DAG: diamond-chain hybrid (8 tasks)
#      0
#     / \
#    1   2
#    |   |
#    3   4
#     \ /
#      5
#     / \
#    6   7
DAG_EDGES = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6), (5, 7)]
TOPO_ORDER = [0, 1, 2, 3, 4, 5, 6, 7]

TYPE_MAP = {"iotd": 0, "uav": 1, "leo": 2, "cs": 3}


class SatelliteDAGEnv:
    def __init__(self, n_tasks=8, seed=None):
        self.n_tasks = n_tasks
        self.n_servers = len(SERVERS)
        self.rng = np.random.RandomState(seed)

    def reset(self):
        self.tasks = [
            {
                "data": self.rng.uniform(0.5e6, 2e6),
                "cycles": self.rng.uniform(0.5e9, 3e9),
            }
            for _ in range(self.n_tasks)
        ]
        self.status = [0] * self.n_tasks  # 0=pending, 2=done
        self.assignments = {}
        self.server_load = [0.0] * self.n_servers
        self.total_cost = 0.0
        return self._obs()

    def _ready(self):
        out = []
        for i in TOPO_ORDER:
            if self.status[i] != 0:
                continue
            preds = [p for p, s in DAG_EDGES if s == i]
            if all(self.status[p] == 2 for p in preds):
                out.append(i)
        return out

    def _obs(self):
        ready = self._ready()
        # task feats: [cycles, data, is_ready, is_done, deps_rem]
        tx = torch.zeros(self.n_tasks, 5)
        for i in range(self.n_tasks):
            t = self.tasks[i]
            deps = sum(1 for p, s in DAG_EDGES if s == i and self.status[p] != 2)
            tx[i] = torch.tensor(
                [t["cycles"] / 3e9, t["data"] / 2e6, float(i in ready), float(self.status[i] == 2), deps / 3.0]
            )

        # server feats by type: [freq, bw, power, load]
        by_type = {}
        for idx, s in enumerate(SERVERS):
            st = s["type"]
            by_type.setdefault(st, []).append(
                [s["freq"] / 3e9, s["bw"] / 50e6, s["power"] / 10.0, self.server_load[idx]]
            )
        sbytype = {k: torch.tensor(v, dtype=torch.float32) for k, v in by_type.items()}

        # flat server feats for homo graph: [freq, bw, power, load, 0, type_oh(4)] = 9 dims
        sflat = []
        for idx, s in enumerate(SERVERS):
            oh = [0.0] * 4
            oh[TYPE_MAP[s["type"]]] = 1.0
            sflat.append([s["freq"] / 3e9, s["bw"] / 50e6, s["power"] / 10.0, self.server_load[idx], 0.0, *oh])
        sflat = torch.tensor(sflat, dtype=torch.float32)

        return {"task_x": tx, "server_by_type": sbytype, "server_flat": sflat, "ready": ready}

    def build_hetero(self, obs):
        g = HeteroData()
        g["task"].x = obs["task_x"]
        for stype, x in obs["server_by_type"].items():
            g[stype].x = x

        # dep edges
        if DAG_EDGES:
            s, d = zip(*DAG_EDGES)
            g["task", "dep", "task"].edge_index = torch.tensor([list(s), list(d)], dtype=torch.long)

        # task-to-server-type fully connected
        for stype in ["iotd", "uav", "leo", "cs"]:
            n_local = sum(1 for sv in SERVERS if sv["type"] == stype)
            src, dst = [], []
            for t in range(self.n_tasks):
                for li in range(n_local):
                    src.append(t)
                    dst.append(li)
            g["task", f"to_{stype}", stype].edge_index = torch.tensor([src, dst], dtype=torch.long)

        return g

    def build_homo(self, obs):
        g = Data()
        # pad task feats to match server flat dim (9)
        task_padded = torch.cat([obs["task_x"], torch.zeros(self.n_tasks, 4)], dim=1)
        g.x = torch.cat([task_padded, obs["server_flat"]], dim=0)

        nt = self.n_tasks
        src, dst = [], []
        # dep edges
        for p, s in DAG_EDGES:
            src += [p, s]
            dst += [s, p]
        # task-server bidirectional
        for t in range(nt):
            for si in range(self.n_servers):
                src += [t, nt + si]
                dst += [nt + si, t]
        g.edge_index = torch.tensor([src, dst], dtype=torch.long)
        return g

    def step(self, task_id, server_idx):
        task = self.tasks[task_id]
        srv = SERVERS[server_idx]

        exec_t = task["cycles"] / srv["freq"]
        xfer_t = 0.0
        for p, s in DAG_EDGES:
            if s == task_id and self.status[p] == 2:
                ps = self.assignments.get(p)
                if ps is not None and ps != server_idx:
                    bw = min(srv["bw"], SERVERS[ps]["bw"])
                    xfer_t += self.tasks[p]["data"] / bw

        energy = exec_t * srv["power"] + xfer_t * 0.5
        cost = exec_t + xfer_t + energy * 0.3

        self.status[task_id] = 2
        self.assignments[task_id] = server_idx
        self.server_load[server_idx] += exec_t + xfer_t
        self.total_cost += cost

        done = all(s == 2 for s in self.status)
        self._obs_cache = self._obs() if not done else None
        return self._obs_cache, -cost, done, {"cost": cost}

    def next_task(self):
        ready = self._ready() if not hasattr(self, "_obs_cache") or self._obs_cache is None else self._obs_cache["ready"]
        return ready[0] if ready else None
