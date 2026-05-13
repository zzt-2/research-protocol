"""DAG generation and task management for satellite DAG task offloading.

daggen-style layered random DAG with ERR priority computation.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import numpy as np

from config import (
    BW_ISL,
    DAGGEN_DENSITY,
    DAGGEN_FAT,
    DAGGEN_JUMP,
    DAGGEN_REGULAR,
    FREQ_CS,
    N_TASKS,
    TASK_CYCLES_RANGE,
    TASK_DEADLINE_RANGE,
    TASK_INPUT_RANGE,
    TASK_OUTPUT_RANGE,
)


@dataclass
class DAGTask:
    task_id: int
    input_data: float       # bytes
    output_data: float      # bytes
    cycles: float           # CPU cycles
    deadline: float         # seconds
    predecessors: list[int] = field(default_factory=list)
    successors: list[int] = field(default_factory=list)


@dataclass
class DAG:
    tasks: list[DAGTask]
    n_tasks: int
    topo_order: list[int]
    edges: list[tuple[int, int]]  # parent -> child


class DAGGenerator:
    def __init__(
        self,
        n_tasks: int = N_TASKS,
        fat: float = DAGGEN_FAT,
        density: float = DAGGEN_DENSITY,
        regular: float = DAGGEN_REGULAR,
        jump: int = DAGGEN_JUMP,
    ):
        self.n_tasks = n_tasks
        self.fat = fat
        self.density = density
        self.regular = regular
        self.jump = jump

    def generate(self, rng: np.random.Generator) -> DAG:
        n = self.n_tasks
        if n < 2:
            raise ValueError("Need at least 2 tasks to form a DAG")

        # --- layer assignment ---
        n_layers = max(3, int(round(3 + n * (1 - self.regular) * 0.5)))
        layers: list[list[int]] = [[] for _ in range(n_layers)]
        for i in range(n):
            layer_idx = min(int(i * n_layers / n), n_layers - 1)
            layers[layer_idx].append(i)

        # Guarantee source in layer 0, sink in last layer
        for layer_list, required_id, target_layer in [
            (layers[0], 0, 0),
            (layers[-1], n - 1, n_layers - 1),
        ]:
            if required_id not in layer_list:
                # remove from current layer
                for ll in layers:
                    if required_id in ll:
                        ll.remove(required_id)
                        break
                layers[target_layer].append(required_id)

        # --- edge creation ---
        edges: set[tuple[int, int]] = set()

        for l in range(n_layers - 1):
            for src in layers[l]:
                candidates: list[int] = []
                for dl in range(1, min(self.jump + 1, n_layers - l)):
                    candidates.extend(layers[l + dl])
                for dst in candidates:
                    if rng.random() < self.density:
                        edges.add((src, dst))

        # --- ensure every task except id=0 has >= 1 predecessor ---
        for l in range(n_layers):
            for task in layers[l]:
                if task == 0:
                    continue
                if any(d == task for _, d in edges):
                    continue
                # Try previous layers within jump range
                prev: list[int] = []
                for pl in range(max(0, l - self.jump), l):
                    prev.extend(layers[pl])
                if prev:
                    edges.add((int(rng.choice(prev)), task))
                else:
                    # Same layer: connect to a task with smaller id
                    same_layer_earlier = [t for t in layers[l] if t < task]
                    if same_layer_earlier:
                        edges.add((same_layer_earlier[-1], task))
                    else:
                        # Fallback: connect to the closest preceding task id
                        edges.add((task - 1, task))

        # --- ensure every task except id=n-1 has >= 1 successor ---
        for l in range(n_layers):
            for task in layers[l]:
                if task == n - 1:
                    continue
                if any(s == task for s, _ in edges):
                    continue
                # Try next layers within jump range
                nxt: list[int] = []
                for nl in range(l + 1, min(n_layers, l + self.jump + 1)):
                    nxt.extend(layers[nl])
                if nxt:
                    edges.add((task, int(rng.choice(nxt))))
                else:
                    # Same layer: connect to a task with larger id
                    same_layer_later = [t for t in layers[l] if t > task]
                    if same_layer_later:
                        edges.add((task, same_layer_later[0]))
                    else:
                        # Fallback: connect to the closest succeeding task id
                        edges.add((task, task + 1))

        edge_list = sorted(edges)

        # --- assign task parameters ---
        tasks: list[DAGTask] = []
        for i in range(n):
            tasks.append(DAGTask(
                task_id=i,
                input_data=float(rng.uniform(*TASK_INPUT_RANGE)),
                output_data=float(rng.uniform(*TASK_OUTPUT_RANGE)),
                cycles=float(rng.uniform(*TASK_CYCLES_RANGE)),
                deadline=float(rng.uniform(*TASK_DEADLINE_RANGE)),
            ))

        # --- build adjacency lists ---
        for src, dst in edge_list:
            tasks[src].successors.append(dst)
            tasks[dst].predecessors.append(src)

        topo_order = _topological_sort(tasks, n)

        dag = DAG(tasks=tasks, n_tasks=n, topo_order=topo_order, edges=edge_list)
        return dag

    def generate_fixed(self, seed: int = 42) -> DAG:
        return self.generate(np.random.default_rng(seed))


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _topological_sort(tasks: list[DAGTask], n: int) -> list[int]:
    """Kahn's algorithm (BFS-based topological sort)."""
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
        raise ValueError(f"Cycle detected: only {len(order)}/{n} nodes in topo order")
    return order


def topological_sort(dag: DAG) -> list[int]:
    """Return topological order of task indices."""
    return _topological_sort(dag.tasks, dag.n_tasks)


def get_ready_tasks(dag: DAG, completed_mask: np.ndarray) -> list[int]:
    """Return indices of tasks whose predecessors are all completed."""
    ready: list[int] = []
    for t in dag.tasks:
        if completed_mask[t.task_id]:
            continue
        if all(completed_mask[p] for p in t.predecessors):
            ready.append(t.task_id)
    return ready


def compute_err_priority(dag: DAG) -> dict[int, float]:
    """Compute ERR (Expected Relative Residual Workload) rank for each task.

    rank_u(i) = w_i + max_{j in succ(i)} (c_ij + rank_u(j))
    w_i  = cycles_i / FREQ_CS  (compute time on fastest node)
    c_ij = output_data_i / BW_ISL (transfer time on fastest link)
    """
    max_freq = FREQ_CS   # 10 GHz
    max_bw = BW_ISL      # 1 GHz

    rank: dict[int, float] = {}

    # Process in reverse topological order (sink first)
    for tid in reversed(dag.topo_order):
        t = dag.tasks[tid]
        w_i = t.cycles / max_freq
        succ_ranks: list[float] = []
        for s in t.successors:
            c_ij = t.output_data / max_bw
            succ_ranks.append(c_ij + rank[s])
        rank[tid] = w_i + (max(succ_ranks) if succ_ranks else 0.0)

    return rank
