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
                 inclination_deg=None, tau=None, episode_steps=None, seed=42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.tau = tau or config.TAU
        self.episode_steps = episode_steps or config.EPISODE_STEPS

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

    def _get_available_edges(self, positions):
        """Return available fixed edges with distances: {(i,j): (distance, type)}."""
        available = {}
        for (i, j), etype in self._fixed_edges.items():
            diff = positions[j] - positions[i]
            d = np.linalg.norm(diff)
            if d > config.Z_MAX or d < 1.0:
                continue
            # LoS check
            diff_sq = np.dot(diff, diff)
            t = max(0.0, min(1.0, -np.dot(positions[i], diff) / diff_sq))
            closest = positions[i] + t * diff
            if np.dot(closest, closest) <= config.RE ** 2:
                continue
            available[(i, j)] = (d, etype)
        return available

    def run_episode(self, verbose=False):
        """Run one episode with fixed grid topology. Returns (metrics, total_reward)."""
        self.metrics.reset()
        total_reward = 0.0

        for step in range(self.episode_steps):
            t = step * self.tau
            positions = self.orbit.propagate(t)

            available = self._get_available_edges(positions)

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
            routing = self.router.route(active_keys, dist_map, cap_map, flows, self.n_sats)

            reward_dict = self.reward_calc.compute(routing, 0, 0, [], len(active_keys))
            reward_dict['_n_changed'] = 0
            reward_dict['_n_active'] = len(active_keys)
            total_reward += reward_dict['total']
            self.metrics.record(reward_dict, routing)

            if verbose and step % 10 == 0:
                print(f"  Step {step}: reward={reward_dict['total']:.4f} "
                      f"R_tput={reward_dict['R_tput']:.3f} "
                      f"n_active={len(active_keys)}/{len(self._fixed_edges)}")

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
