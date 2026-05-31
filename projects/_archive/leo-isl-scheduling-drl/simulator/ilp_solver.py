"""ILP-based optimal ISL configuration solver using PuLP + CBC."""

import time

import numpy as np
import pulp

from . import config


class ISLScheduler:
    """ILP solver for optimal ISL configuration.

    Uses PuLP with the CBC backend to find the optimal set of ISL edges
    that maximises total weighted capacity, subject to per-satellite
    laser-terminal count constraints.
    """

    def __init__(self, n_lct=None, time_limit=None, gap_tol=None):
        self.n_lct = n_lct or config.N_LCT
        self.time_limit = time_limit or config.ILP_TIME_LIMIT
        self.gap_tol = gap_tol or config.ILP_GAP_TOL

    def solve(
        self,
        candidate_edges: list[tuple[int, int, float]],  # (i, j, distance_km)
        supply: np.ndarray,      # (n_sats,) normalized supply
        demand: np.ndarray,      # (n_sats,) normalized demand
        capacities: np.ndarray,  # (n_candidates,) Gbps per candidate
        n_sats: int,
    ) -> tuple[set[tuple[int, int]], dict]:
        """Solve for optimal ISL configuration.

        Variables: x_{ij} in {0,1} for each candidate edge
        Objective: max sum (supply_i + supply_j + demand_i + demand_j) * cap_{ij} * x_{ij}
        Constraints:
          - sum_j x_{ij} <= N_LCT for each satellite i
          - x_{ij} = x_{ji} (undirected, use (min_i, max_j) as key)

        Args:
            candidate_edges: list of (sat_i, sat_j, distance_km) tuples.
            supply: normalized supply per satellite, shape (n_sats,).
            demand: normalized demand per satellite, shape (n_sats,).
            capacities: capacity per candidate edge, shape (n_candidates,).
            n_sats: total number of satellites.

        Returns:
            selected_edges: set of (min_i, max_j) optimal edges.
            info: dict with objective_value, solve_time, n_variables,
                  n_constraints, status.
        """
        # --- Normalise edges to canonical (min, max) keys and deduplicate ---
        seen: dict[tuple[int, int], int] = {}  # (i, j) -> index into unique lists
        unique_caps: list[float] = []

        for idx, (i, j, _dist) in enumerate(candidate_edges):
            key = (min(i, j), max(i, j))
            if key in seen:
                # Keep the larger capacity for duplicate edges
                prev_idx = seen[key]
                unique_caps[prev_idx] = max(unique_caps[prev_idx], capacities[idx])
            else:
                seen[key] = len(unique_caps)
                unique_caps.append(float(capacities[idx]))

        canonical_edges = list(seen.keys())  # list of (min_i, max_j)
        n_vars = len(canonical_edges)

        if n_vars == 0:
            return set(), {
                "objective_value": 0.0,
                "solve_time": 0.0,
                "n_variables": 0,
                "n_constraints": 0,
                "status": "Optimal",
            }

        # --- Build ILP ---
        prob = pulp.LpProblem("isl_scheduling", pulp.LpMaximize)

        # Decision variables
        x: dict[tuple[int, int], pulp.LpVariable] = {}
        for a, b in canonical_edges:
            x[(a, b)] = pulp.LpVariable(f"x_{a}_{b}", cat="Binary")

        # Objective: maximise weighted capacity
        # weight_{ij} = supply_i + supply_j + demand_i + demand_j
        obj_terms = []
        for k, (a, b) in enumerate(canonical_edges):
            weight = float(supply[a] + supply[b] + demand[a] + demand[b])
            cap = unique_caps[k]
            obj_terms.append(weight * cap * x[(a, b)])
        prob += pulp.lpSum(obj_terms)

        # LCT degree constraints: each satellite uses at most N_LCT edges
        for s in range(n_sats):
            incident = [x[(a, b)] for (a, b) in canonical_edges if a == s or b == s]
            if incident:
                prob += (
                    pulp.lpSum(incident) <= self.n_lct,
                    f"lct_sat_{s}",
                )

        # --- Solve ---
        t0 = time.perf_counter()
        solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=self.time_limit, gapRel=self.gap_tol)
        prob.solve(solver)
        solve_time = time.perf_counter() - t0

        # --- Extract results ---
        selected_edges: set[tuple[int, int]] = set()
        for key, var in x.items():
            if pulp.value(var) is not None and pulp.value(var) > 0.5:
                selected_edges.add(key)

        status = pulp.LpStatus[prob.status]
        objective_value = pulp.value(prob.objective) or 0.0

        info = {
            "objective_value": float(objective_value),
            "solve_time": round(solve_time, 4),
            "n_variables": n_vars,
            "n_constraints": len(prob.constraints),
            "status": status,
        }

        return selected_edges, info
