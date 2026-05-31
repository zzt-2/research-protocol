"""DAG generation and task management.

daggen-style layered random DAG with ERR priority computation.
Supports MultiDAGBundle for N_IOTD independent DAGs.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import numpy as np

from config import SimConfig


@dataclass
class DAGTask:
    task_id: int
    input_data: float       # bytes
    output_data: float      # bytes
    cycles: float           # CPU cycles
    deadline: float         # seconds
    owning_iotd: int = 0
    predecessors: list[int] = field(default_factory=list)
    successors: list[int] = field(default_factory=list)


@dataclass
class DAG:
    tasks: list[DAGTask]
    n_tasks: int
    topo_order: list[int]
    edges: list[tuple[int, int]]


class DAGGenerator:
    def __init__(self, config: SimConfig):
        self.cfg = config
        self.n_tasks = config.n_tasks
        self.fat = config.daggen_fat
        self.density = config.daggen_density
        self.regular = config.daggen_regular
        self.jump = config.daggen_jump

    def generate(self, rng: np.random.Generator) -> DAG:
        n = self.n_tasks
        if n < 2:
            raise ValueError("Need at least 2 tasks")

        # Layer assignment
        n_layers = max(3, int(round(3 + n * (1 - self.regular) * 0.5)))
        layers: list[list[int]] = [[] for _ in range(n_layers)]
        for i in range(n):
            layers[min(int(i * n_layers / n), n_layers - 1)].append(i)

        # Guarantee source in layer 0, sink in last layer
        for layer_list, required_id, target_layer in [
            (layers[0], 0, 0), (layers[-1], n - 1, n_layers - 1),
        ]:
            if required_id not in layer_list:
                for ll in layers:
                    if required_id in ll:
                        ll.remove(required_id)
                        break
                layers[target_layer].append(required_id)

        # Edge creation
        edges: set[tuple[int, int]] = set()
        for l in range(n_layers - 1):
            for src in layers[l]:
                candidates: list[int] = []
                for dl in range(1, min(self.jump + 1, n_layers - l)):
                    candidates.extend(layers[l + dl])
                for dst in candidates:
                    if rng.random() < self.density:
                        edges.add((src, dst))

        # Every task except id=0 has >= 1 predecessor
        for l in range(n_layers):
            for task in layers[l]:
                if task == 0:
                    continue
                if any(d == task for _, d in edges):
                    continue
                prev = []
                for pl in range(max(0, l - self.jump), l):
                    prev.extend(layers[pl])
                if prev:
                    edges.add((int(rng.choice(prev)), task))
                else:
                    same_earlier = [t for t in layers[l] if t < task]
                    edges.add((same_earlier[-1], task) if same_earlier else (task - 1, task))

        # Every task except id=n-1 has >= 1 successor
        for l in range(n_layers):
            for task in layers[l]:
                if task == n - 1:
                    continue
                if any(s == task for s, _ in edges):
                    continue
                nxt = []
                for nl in range(l + 1, min(n_layers, l + self.jump + 1)):
                    nxt.extend(layers[nl])
                if nxt:
                    edges.add((task, int(rng.choice(nxt))))
                else:
                    same_later = [t for t in layers[l] if t > task]
                    edges.add((task, same_later[0]) if same_later else (task, task + 1))

        edge_list = sorted(edges)

        # Task parameters from config ranges
        tasks: list[DAGTask] = []
        for i in range(n):
            tasks.append(DAGTask(
                task_id=i,
                input_data=float(rng.uniform(*self.cfg.task_input_range)),
                output_data=float(rng.uniform(*self.cfg.task_output_range)),
                cycles=float(rng.uniform(*self.cfg.task_cycles_range)),
                deadline=float(rng.uniform(*self.cfg.task_deadline_range)),
            ))

        for src, dst in edge_list:
            tasks[src].successors.append(dst)
            tasks[dst].predecessors.append(src)

        topo_order = _topological_sort(tasks, n)
        return DAG(tasks=tasks, n_tasks=n, topo_order=topo_order, edges=edge_list)


def _topological_sort(tasks: list[DAGTask], n: int) -> list[int]:
    in_degree = [0] * n
    for t in tasks:
        for s in t.successors:
            in_degree[s] += 1
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for s in tasks[node].successors:
            in_degree[s] -= 1
            if in_degree[s] == 0:
                queue.append(s)
    if len(order) != n:
        raise ValueError(f"Cycle detected: {len(order)}/{n} nodes in topo order")
    return order


def get_ready_tasks(dag: DAG, completed_mask: np.ndarray) -> list[int]:
    return [t.task_id for t in dag.tasks
            if not completed_mask[t.task_id]
            and all(completed_mask[p] for p in t.predecessors)]


def compute_err_priority(dag: DAG, max_freq: float, max_bw: float) -> dict[int, float]:
    """ERR (Expected Relative Residual Workload) rank per task."""
    rank: dict[int, float] = {}
    for tid in reversed(dag.topo_order):
        t = dag.tasks[tid]
        w_i = t.cycles / max_freq
        succ_ranks = [t.output_data / max_bw + rank[s] for s in t.successors]
        rank[tid] = w_i + (max(succ_ranks) if succ_ranks else 0.0)
    return rank


class MultiDAGBundle:
    """N_IOTD independent DAGs with globally unique task IDs."""

    def __init__(self, config: SimConfig):
        self.cfg = config
        self.n_iotd = config.n_iotd
        self.tasks_per_iotd = config.n_tasks
        self.total_tasks = config.total_tasks
        self._gen = DAGGenerator(config)

    def generate(self, rng: np.random.Generator) -> tuple[list[DAGTask], dict[int, float]]:
        all_tasks: list[DAGTask | None] = [None] * self.total_tasks
        err_ranks: dict[int, float] = {}

        for iotd_idx in range(self.n_iotd):
            dag = self._gen.generate(rng)
            offset = iotd_idx * self.tasks_per_iotd
            local_ranks = compute_err_priority(dag, self.cfg.freq_cs, self.cfg.bw_isl)

            for t in dag.tasks:
                global_id = offset + t.task_id
                err_ranks[global_id] = local_ranks[t.task_id]
                t.task_id = global_id
                t.owning_iotd = iotd_idx
                t.predecessors = [offset + p for p in t.predecessors]
                t.successors = [offset + s for s in t.successors]
                all_tasks[global_id] = t

        return all_tasks, err_ranks  # type: ignore[return-value]


def get_ready_tasks_multi(all_tasks: list[DAGTask], completed_mask: np.ndarray) -> list[int]:
    return [t.task_id for t in all_tasks
            if not completed_mask[t.task_id]
            and all(completed_mask[p] for p in t.predecessors)]
