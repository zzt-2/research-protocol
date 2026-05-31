"""B1: +Grid/Fixed Baseline — 2 intra-plane + 2 inter-plane ISLs, permanent.

Reference: [L09 §II-B: Fixed LISLs] intra-plane, [L01 §III-A: +Grid] inter-plane.

Each satellite maintains up to 4 permanent ISLs:
  - 2 intra-plane: adjacent neighbors in same orbital plane (wrapping)
  - 2 inter-plane: nearest neighbors in adjacent orbital planes

All ISLs permanently active — no setup delay, no switching cost.
Edges exceeding z_max or losing LoS are temporarily unavailable for routing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from collections import defaultdict

from simulator.orbit import OrbitPropagator
from simulator.channel import ChannelModel
from simulator.traffic import TrafficGenerator
from simulator.router import Router
from simulator.reward import RewardCalculator
from simulator.metrics import MetricsCollector
from simulator import config


class GridFixedBaseline:
    def __init__(self, n_planes=None, sats_per_plane=None, altitude=None,
                 inclination_deg=None, tau=None, episode_steps=None, seed=42,
                 multipath=False, k_paths=4, n_lct=None,
                 failure_prob=None, failure_duration_min=None, failure_duration_max=None):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.tau = tau or config.TAU
        self.episode_steps = episode_steps or config.EPISODE_STEPS
        self.multipath = multipath
        self.k_paths = k_paths
        self.n_lct = n_lct
        self.failure_prob = failure_prob if failure_prob is not None else config.FAILURE_PROB
        self.failure_dur_min = failure_duration_min or config.FAILURE_DURATION_MIN
        self.failure_dur_max = failure_duration_max or config.FAILURE_DURATION_MAX

        self.orbit = OrbitPropagator(n_planes, sats_per_plane, altitude, inclination_deg)
        self.channel = ChannelModel()
        self.traffic = TrafficGenerator(seed=seed)
        self.router = Router()
        self.reward_calc = RewardCalculator()
        self.metrics = MetricsCollector()

        self.n_sats = self.orbit.n_sats
        self.n_planes = self.orbit.n_planes
        self.spp = self.orbit.sats_per_plane

        self._fixed_edges = self._build_grid_topology()
        if self.n_lct is not None:
            self._fixed_edges = self._prune_to_lct(self._fixed_edges)

    def _sat_id(self, plane, pos):
        return plane * self.spp + pos

    def _build_grid_topology(self):
        """Build fixed +Grid topology at t=0. Returns dict {(i,j): type}."""
        positions = self.orbit.propagate(0)
        edges = {}

        # Intra-plane: adjacent neighbors (wrapping)
        for p in range(self.n_planes):
            for s in range(self.spp):
                i = self._sat_id(p, s)
                j = self._sat_id(p, (s + 1) % self.spp)
                edges[(min(i, j), max(i, j))] = 'intra'

        # Inter-plane: 2 nearest in each adjacent plane
        for p in range(self.n_planes):
            p_next = (p + 1) % self.n_planes
            for s in range(self.spp):
                i = self._sat_id(p, s)
                candidates = []
                for s2 in range(self.spp):
                    j = self._sat_id(p_next, s2)
                    d = np.linalg.norm(positions[i] - positions[j])
                    if d < config.Z_MAX:
                        candidates.append((d, j))
                candidates.sort()
                for k in range(min(2, len(candidates))):
                    j = candidates[k][1]
                    key = (min(i, j), max(i, j))
                    if key not in edges:
                        edges[key] = 'inter'

        return edges

    def _prune_to_lct(self, edges):
        """Prune edges so each satellite has at most n_lct connections (keep shortest)."""
        # Build per-satellite edge list with distances
        positions = self.orbit.propagate(0)
        sat_edges = defaultdict(list)
        for (i, j), etype in edges.items():
            d = np.linalg.norm(positions[i] - positions[j])
            sat_edges[i].append((d, (i, j), etype))
            sat_edges[j].append((d, (i, j), etype))

        # Determine which edges to keep
        keep = set()
        for sat, elist in sat_edges.items():
            elist.sort()
            for _, key, etype in elist[:self.n_lct]:
                keep.add(key)

        return {k: v for k, v in edges.items() if k in keep}

    def _get_available_edges(self, positions):
        """Return available fixed edges with distances (vectorized)."""
        edges = list(self._fixed_edges.keys())
        types = list(self._fixed_edges.values())
        n_edges = len(edges)
        if n_edges == 0:
            return {}

        ei = np.array([e[0] for e in edges])
        ej = np.array([e[1] for e in edges])
        seg = positions[ej] - positions[ei]  # (n_edges, 3)
        d = np.linalg.norm(seg, axis=1)

        # Distance filter
        mask = (d < config.Z_MAX) & (d > 1.0)
        if not np.any(mask):
            return {}

        # LoS check (vectorized)
        pi = positions[ei[mask]]
        s = seg[mask]
        ds = d[mask] ** 2
        t = np.clip(-np.sum(pi * s, axis=1) / ds, 0.0, 1.0)
        closest = pi + t[:, np.newaxis] * s
        los = np.sum(closest ** 2, axis=1) > config.RE ** 2

        # Build result
        idx = np.where(mask)[0][los]
        available = {}
        for k in idx:
            available[(int(ei[k]), int(ej[k]))] = (float(d[k]), types[k])
        return available

    def run_episode(self, verbose=False):
        """Run one episode with fixed grid topology. Returns (metrics, total_reward)."""
        self.metrics.reset()
        total_reward = 0.0
        failed_edges = {}  # key -> remaining steps

        for step in range(self.episode_steps):
            t = step * self.tau
            positions = self.orbit.propagate(t)

            available = self._get_available_edges(positions)

            # Inject link failures
            if self.failure_prob > 0:
                # Recover expired
                recovered = [k for k, v in failed_edges.items() if v <= 1]
                for k in recovered:
                    del failed_edges[k]
                for k in list(failed_edges.keys()):
                    if k not in recovered:
                        failed_edges[k] -= 1

                # Fail active edges
                avail_keys = list(available.keys())
                for key in avail_keys:
                    if key not in failed_edges and self.rng.random() < self.failure_prob:
                        dur = self.rng.integers(self.failure_dur_min, self.failure_dur_max + 1)
                        failed_edges[key] = dur

                # Remove failed from available
                available = {k: v for k, v in available.items() if k not in failed_edges}

            dist_map = {}
            cap_map = {}
            for (i, j), (d, _) in available.items():
                cap_gbps, _, avail = self.channel.compute_single(d)
                if avail:
                    dist_map[(i, j)] = d
                    cap_map[(i, j)] = cap_gbps

            lat, lon, alt = self.orbit.eci_to_lla(positions, t)
            flows = self.traffic.generate(lat, lon, alt)

            active_keys = list(cap_map.keys())
            if self.multipath:
                routing = self.router.route_multipath(
                    active_keys, dist_map, cap_map, flows, self.n_sats,
                    k_paths=self.k_paths)
            else:
                routing = self.router.route(active_keys, dist_map, cap_map, flows, self.n_sats)

            reward_dict = self.reward_calc.compute(routing, 0, 0, [], len(active_keys))
            reward_dict['_n_changed'] = 0
            reward_dict['_n_active'] = len(active_keys)
            total_reward += reward_dict['total']
            self.metrics.record(reward_dict, routing)

            if verbose and step % 10 == 0:
                print(f"  Step {step}: reward={reward_dict['total']:.4f} "
                      f"R_tput={reward_dict['R_tput']:.3f} "
                      f"n_active={len(active_keys)}/{len(self._fixed_edges)} "
                      f"n_failed={len(failed_edges)}")

        return self.metrics.compute(), total_reward

    def topology_summary(self):
        """Return topology statistics."""
        n_intra = sum(1 for v in self._fixed_edges.values() if v == 'intra')
        n_inter = sum(1 for v in self._fixed_edges.values() if v == 'inter')
        return {
            'total_edges': len(self._fixed_edges),
            'intra_edges': n_intra,
            'inter_edges': n_inter,
            'edges_per_sat': 2 * len(self._fixed_edges) / self.n_sats,
        }
