"""M5: ISLEnvironment — MDP environment wrapping M1-M4, M6.

Implements the ISL scheduling MDP:
  State:  graph (node features 6-d, edge features 7-d, candidate edges)
  Action: scores ∈ [0,1] per candidate edge → LCT constraint (top-2) → state update
  Reward: w1·R_tput - w2·C_switch - w3·C_setup

ISL state machine per edge:
  inactive → (select) → in_setup → (timer expires) → active
  in_setup → (deselect) → inactive (cancel)
  active   → (deselect) → inactive (teardown)
  active   → (select)   → active  (maintain)
"""

import numpy as np
from collections import defaultdict
import gymnasium as gym
from gymnasium import spaces

from . import config
from .orbit import OrbitPropagator
from .visibility import VisibilityConnectivity
from .channel import ChannelModel
from .traffic import TrafficGenerator
from .router import Router
from .reward import RewardCalculator
from .metrics import MetricsCollector


class ISLEnvironment:
    """ISL scheduling environment (gym-like API without strict gym spaces)."""

    def __init__(self, n_planes=None, sats_per_plane=None, altitude=None,
                 inclination_deg=None, tau=None, episode_steps=None, seed=42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.tau = tau or config.TAU
        self.episode_steps = episode_steps or config.EPISODE_STEPS

        # Modules
        self.orbit = OrbitPropagator(n_planes, sats_per_plane, altitude, inclination_deg)
        self.vis = VisibilityConnectivity()
        self.channel = ChannelModel()
        self.traffic = TrafficGenerator(seed=seed)
        self.router = Router()
        self.reward_calc = RewardCalculator()
        self.metrics = MetricsCollector()

        self.n_sats = self.orbit.n_sats

        # Episode state
        self._t = 0
        self._step = 0
        self._positions = None
        self._candidate_edges = []  # list of (i, j, distance_km)
        self._isl_state = {}       # (min_i, max_j) -> 'inactive'|'in_setup'|'active'
        self._setup_remaining = {} # (min_i, max_j) -> seconds
        self._active_duration = {} # (min_i, max_j) -> seconds
        self._prev_active_count = 0
        self._flows = []

    def reset(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
            self.seed = seed

        self._t = 0
        self._step = 0
        self._isl_state.clear()
        self._setup_remaining.clear()
        self._active_duration.clear()
        self._prev_active_count = 0
        self.metrics.reset()

        # Initial positions and candidate edges
        self._positions = self.orbit.propagate(0)
        self._candidate_edges = self.vis.compute(self._positions)
        for i, j, _ in self._candidate_edges:
            self._isl_state[(min(i, j), max(i, j))] = 'inactive'

        # Initial traffic
        lat, lon, alt = self.orbit.eci_to_lla(self._positions, 0)
        self._flows = self.traffic.generate(lat, lon, alt)

        obs = self._build_obs()
        return obs, {}

    def step(self, scores):
        """Execute one decision step.

        Args:
            scores: (n_candidates,) array in [0,1], one per candidate edge.

        Returns:
            obs, reward, terminated, truncated, info
        """
        # 1. Apply LCT constraint → selected edge set
        selected = self._apply_lct(scores)

        # 2. Update ISL states
        n_new, n_changed, setup_delays = self._update_states(selected)

        # 3. Advance time
        self._t += self.tau
        self._step += 1

        # 4. Recompute positions and candidate edges
        self._positions = self.orbit.propagate(self._t)
        new_candidates = self.vis.compute(self._positions)
        new_set = {(min(i, j), max(i, j)) for i, j, _ in new_candidates}

        # Tear down ISLs no longer in candidate set (orbital mechanics)
        for key in list(self._isl_state.keys()):
            if self._isl_state[key] != 'inactive' and key not in new_set:
                if self._isl_state[key] == 'active':
                    n_changed += 1
                del self._isl_state[key]
                self._setup_remaining.pop(key, None)
                self._active_duration.pop(key, None)

        # Add new candidates as inactive
        for i, j, _ in new_candidates:
            key = (min(i, j), max(i, j))
            if key not in self._isl_state:
                self._isl_state[key] = 'inactive'

        self._candidate_edges = new_candidates

        # 5. Route on active topology
        active_keys = [k for k, v in self._isl_state.items() if v == 'active']

        dist_map = {}
        cap_map = {}
        for key in active_keys:
            # Find distance from candidate edges or stored data
            d = self._find_distance(key)
            cap_gbps, pout, avail = self.channel.compute_single(d)
            dist_map[key] = d
            cap_map[key] = cap_gbps if avail else 0

        lat, lon, alt = self.orbit.eci_to_lla(self._positions, self._t)
        self._flows = self.traffic.generate(lat, lon, alt)

        routing = self.router.route(active_keys, dist_map, cap_map, self._flows, self.n_sats)

        # 6. Reward
        reward_dict = self.reward_calc.compute(
            routing, n_changed, n_new, setup_delays, self._prev_active_count
        )
        reward_dict['_n_changed'] = n_changed
        reward_dict['_n_active'] = len(active_keys)
        self._prev_active_count = len(active_keys)

        # 7. Update active durations
        for key in active_keys:
            self._active_duration[key] = self._active_duration.get(key, 0) + self.tau

        # 8. Build observation
        obs = self._build_obs()

        terminated = self._step >= self.episode_steps
        info = {
            'reward_dict': reward_dict,
            'routing': routing,
            'step': self._step,
            'n_active': len(active_keys),
        }
        self.metrics.record(reward_dict, routing)

        return obs, reward_dict['total'], terminated, False, info

    def _apply_lct(self, scores):
        """LCT constraint: top-N_LCT edges per satellite by score."""
        scores = np.asarray(scores)
        sat_scores = defaultdict(list)

        for idx, (i, j, _) in enumerate(self._candidate_edges):
            s = float(scores[idx]) if idx < len(scores) else 0.0
            sat_scores[i].append((s, j))
            sat_scores[j].append((s, i))

        selected = set()
        for sat, edges in sat_scores.items():
            edges.sort(reverse=True)
            for k in range(min(config.N_LCT, len(edges))):
                _, neighbor = edges[k]
                selected.add((min(sat, neighbor), max(sat, neighbor)))

        return selected

    def _update_states(self, selected):
        """ISL state machine transitions."""
        n_new = 0
        n_changed = 0
        setup_delays = []

        for i, j, _ in self._candidate_edges:
            key = (min(i, j), max(i, j))
            is_sel = key in selected
            state = self._isl_state.get(key, 'inactive')

            if is_sel:
                if state == 'inactive':
                    delay = float(self.rng.uniform(config.SETUP_DELAY_MIN, config.SETUP_DELAY_MAX))
                    self._isl_state[key] = 'in_setup'
                    self._setup_remaining[key] = delay
                    n_new += 1
                    setup_delays.append(delay)
                elif state == 'in_setup':
                    self._setup_remaining[key] -= self.tau
                    if self._setup_remaining[key] <= 0:
                        self._isl_state[key] = 'active'
                        self._active_duration[key] = 0
                        del self._setup_remaining[key]
                # active → active: maintain
            else:
                if state == 'in_setup':
                    self._isl_state[key] = 'inactive'
                    del self._setup_remaining[key]
                    n_changed += 1
                elif state == 'active':
                    self._isl_state[key] = 'inactive'
                    self._active_duration.pop(key, None)
                    n_changed += 1

        return n_new, n_changed, setup_delays

    def _find_distance(self, key):
        """Find distance for an edge key from candidate edges."""
        i, j = key
        for ci, cj, d in self._candidate_edges:
            if (ci == i and cj == j) or (ci == j and cj == i):
                return d
        return 1000.0  # fallback

    def _build_obs(self):
        """Build observation: node features (N,6) + edge features (E,7)."""
        n = self.n_sats
        lat, lon, alt = self.orbit.eci_to_lla(self._positions, self._t)

        # Node features
        supply = np.zeros(n)
        demand = np.zeros(n)
        for src, dst, dem in self._flows:
            if 0 <= src < n and 0 <= dst < n:
                supply[src] += dem
                demand[dst] += dem

        max_sd = max(supply.max(), demand.max(), 1.0)

        n_active = np.zeros(n)
        n_setup = np.zeros(n)
        for (i, j), state in self._isl_state.items():
            if i < n and j < n:
                if state == 'active':
                    n_active[i] += 1
                    n_active[j] += 1
                elif state == 'in_setup':
                    n_setup[i] += 1
                    n_setup[j] += 1

        node_feat = np.stack([
            supply / max_sd,
            demand / max_sd,
            lat / (np.pi / 2),
            lon / np.pi,
            n_active / config.N_LCT,
            n_setup / config.N_LCT,
        ], axis=1)

        # Edge features
        n_cand = len(self._candidate_edges)
        edge_feat = np.zeros((n_cand, 7))

        if n_cand > 0:
            dists = np.array([d for _, _, d in self._candidate_edges])
            caps, pouts, _ = self.channel.compute(dists)
            max_cap = max(caps.max(), 1.0)
            max_dur = max(max(self._active_duration.values(), default=1.0), 1.0)

            for idx, (i, j, d) in enumerate(self._candidate_edges):
                key = (min(i, j), max(i, j))
                state = self._isl_state.get(key, 'inactive')
                edge_feat[idx, 0] = caps[idx] / max_cap
                edge_feat[idx, 1] = d / config.Z_MAX
                edge_feat[idx, 2] = 1.0 if state == 'active' else 0.0
                edge_feat[idx, 3] = 1.0 if state == 'in_setup' else 0.0
                edge_feat[idx, 4] = self._setup_remaining.get(key, 0) / config.SETUP_DELAY_MAX
                dur = self._active_duration.get(key, 0)
                edge_feat[idx, 5] = np.log1p(dur) / np.log1p(max_dur)
                edge_feat[idx, 6] = pouts[idx]

        return {
            'node_features': node_feat,
            'edge_features': edge_feat,
            'candidate_edges': self._candidate_edges,
            'n_candidates': n_cand,
            'positions_eci': self._positions,
            'time': self._t,
        }

    def set_isl_configuration(self, edge_set):
        """Directly set active ISLs to match edge_set.

        Bypasses the score->LCT pipeline. Used by ILP dataset generator
        to create supervised training samples.

        Args:
            edge_set: set of (min_i, max_j) edges to make active.
                      Must be subset of current candidate_edges.
        """
        candidate_set = {(min(i, j), max(i, j)) for i, j, _ in self._candidate_edges}

        for key in edge_set:
            if key not in candidate_set:
                continue
            state = self._isl_state.get(key, 'inactive')
            if state == 'inactive':
                self._isl_state[key] = 'active'
                self._active_duration[key] = 0.0
            elif state == 'in_setup':
                self._isl_state[key] = 'active'
                self._active_duration[key] = 0.0
                self._setup_remaining.pop(key, None)

        for key in list(self._isl_state.keys()):
            if key not in edge_set and self._isl_state[key] != 'inactive':
                self._isl_state[key] = 'inactive'
                self._setup_remaining.pop(key, None)
                self._active_duration.pop(key, None)

    def get_candidate_info(self):
        """Return candidate edges with channel/traffic info for ILP.

        Returns:
            list of dict with keys: i, j, distance, capacity, supply_i,
            demand_i, supply_j, demand_j
        """
        n = self.n_sats
        supply = np.zeros(n)
        demand = np.zeros(n)
        for src, dst, dem in self._flows:
            if 0 <= src < n and 0 <= dst < n:
                supply[src] += dem
                demand[dst] += dem

        result = []
        dists = np.array([d for _, _, d in self._candidate_edges])
        if len(dists) > 0:
            caps, _, _ = self.channel.compute(dists)
        else:
            caps = np.array([])

        for idx, (i, j, d) in enumerate(self._candidate_edges):
            result.append({
                'i': i, 'j': j,
                'distance': d,
                'capacity': float(caps[idx]),
                'supply_i': float(supply[i]),
                'demand_i': float(demand[i]),
                'supply_j': float(supply[j]),
                'demand_j': float(demand[j]),
            })
        return result

    def run_episode(self, policy_fn, verbose=False):
        """Run a full episode with a given policy function.

        Args:
            policy_fn: callable(obs) -> scores array.

        Returns:
            metrics_dict from MetricsCollector.
        """
        obs, _ = self.reset()
        total_reward = 0

        for step in range(self.episode_steps):
            scores = policy_fn(obs)
            obs, reward, terminated, truncated, info = self.step(scores)
            total_reward += reward
            if verbose and step % 10 == 0:
                rd = info['reward_dict']
                print(f"  Step {step}: reward={reward:.4f} "
                      f"R_tput={rd['R_tput']:.3f} C_sw={rd['C_switch']:.3f} "
                      f"C_setup={rd['C_setup']:.3f} n_active={info['n_active']}")
            if terminated:
                break

        return self.metrics.compute(), total_reward
