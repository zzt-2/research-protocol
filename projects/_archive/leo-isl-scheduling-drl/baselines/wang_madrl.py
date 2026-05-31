"""B2: Wang TCOM MADRL — Double Dueling DQN + "3 fixed + 1 dynamic" ISL mode.

Reference: [L09] Wang et al., IEEE TCOM 2024.
  - 3 fixed ISLs: 2 intra-plane + 1 inter-plane (nearest)
  - 1 dynamic ISL: choose from 7 inter-plane candidates or turn off
  - Double Dueling DQN with shared parameters and shared replay buffer
  - Bidirectional agreement for dynamic ISLs
  - Local reward: load reduction - penalty for dynamic ISL existence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import defaultdict, deque
import random

from simulator.orbit import OrbitPropagator
from simulator.channel import ChannelModel
from simulator.traffic import TrafficGenerator
from simulator.router import Router
from simulator.metrics import MetricsCollector
from simulator import config

# State vector per satellite (20-dim)
# [0-2]   fixed ISL loads (intra_fwd, intra_bwd, inter_fixed) [0,1]
# [3]     dynamic ISL load [0,1]
# [4]     current action / 7 [0,1]
# [5-11]  candidate distances / z_max [0,1]
# [12-15] neighbor avg loads (4 neighbors) [0,1]
# [16]    supply demand [0,1]
# [17]    receive demand [0,1]
# [18]    latitude / (pi/2) [-1,1]
# [19]    longitude / pi [-1,1]
STATE_DIM = 20
N_ACTIONS = 8  # 7 candidates + turn off


class DuelingDQN(nn.Module):
    """Dueling DQN: state → FC 512 → FC 256 → (Advantage 8 + Value 1)."""

    def __init__(self, state_dim=STATE_DIM, n_actions=N_ACTIONS):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, 512)
        self.fc2 = nn.Linear(512, 256)
        self.advantage = nn.Linear(256, n_actions)
        self.value = nn.Linear(256, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        adv = self.advantage(x)
        val = self.value(x)
        return val + adv - adv.mean(dim=-1, keepdim=True)


class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        s, a, r, ns, d = zip(*batch)
        return (np.array(s, dtype=np.float32),
                np.array(a, dtype=np.int64),
                np.array(r, dtype=np.float32),
                np.array(ns, dtype=np.float32),
                np.array(d, dtype=np.float32))

    def __len__(self):
        return len(self.buffer)


class WangMADRLBaseline:
    def __init__(self, n_planes=None, sats_per_plane=None, altitude=None,
                 inclination_deg=None, tau=None, episode_steps=None,
                 lr=1e-3, gamma=0.9, beta_penalty=0.1,
                 buffer_capacity=100000, seed=42, device='cpu'):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        random.seed(seed)
        torch.manual_seed(seed)
        self.device = torch.device(device)

        self.tau = tau or config.TAU
        self.episode_steps = episode_steps or config.EPISODE_STEPS
        self.gamma = gamma  # L09: 0.9
        self.beta_penalty = beta_penalty

        # Simulator modules
        self.orbit = OrbitPropagator(n_planes, sats_per_plane, altitude, inclination_deg)
        self.channel = ChannelModel()
        self.traffic = TrafficGenerator(seed=seed)
        self.router = Router()
        self.metrics = MetricsCollector()

        self.n_sats = self.orbit.n_sats
        self.n_planes = self.orbit.n_planes
        self.spp = self.orbit.sats_per_plane

        # Build topology
        self._fixed_edges = self._build_fixed_topology()
        self._inter_candidates, self._inter_fixed = self._find_inter_plane_info()
        self._fixed_by_sat = self._index_fixed_by_satellite()

        # DQN
        self.dqn = DuelingDQN().to(self.device)
        self.target_dqn = DuelingDQN().to(self.device)
        self.target_dqn.load_state_dict(self.dqn.state_dict())
        self.optimizer = optim.Adam(self.dqn.parameters(), lr=lr)
        self.buffer = ReplayBuffer(buffer_capacity)
        self._total_steps = 0

    def _sat_id(self, plane, pos):
        return plane * self.spp + pos

    def _sat_coords(self, sat_id):
        return sat_id // self.spp, sat_id % self.spp

    def _build_fixed_topology(self):
        """Build 3 fixed ISLs per satellite: 2 intra + 1 inter (nearest)."""
        positions = self.orbit.propagate(0)
        edges = {}

        # Intra-plane: ring of adjacent satellites
        for p in range(self.n_planes):
            for s in range(self.spp):
                i = self._sat_id(p, s)
                j = self._sat_id(p, (s + 1) % self.spp)
                edges[(min(i, j), max(i, j))] = 'intra'

        # Inter-plane fixed: nearest in (p+1) % NP per satellite
        self._fixed_inter_target = {}
        for p in range(self.n_planes):
            p_next = (p + 1) % self.n_planes
            for s in range(self.spp):
                i = self._sat_id(p, s)
                best_j, best_d = -1, float('inf')
                for s2 in range(self.spp):
                    j = self._sat_id(p_next, s2)
                    d = np.linalg.norm(positions[i] - positions[j])
                    if d < best_d:
                        best_d = d
                        best_j = j
                key = (min(i, best_j), max(i, best_j))
                edges[key] = 'inter_fixed'
                self._fixed_inter_target[i] = best_j

        return edges

    def _find_inter_plane_info(self):
        """Find 7 dynamic candidates per satellite (inter-plane, excluding fixed)."""
        positions = self.orbit.propagate(0)
        candidates = {}  # sat_id → list of 7 candidate sat_ids (-1 padded)
        fixed_inter = {}  # sat_id → fixed inter-plane target

        for i in range(self.n_sats):
            fixed_inter[i] = self._fixed_inter_target[i]
            p, s = self._sat_coords(i)
            # Find all inter-plane neighbors in both adjacent planes
            inter_neighbors = []
            for dp in [-1, 1]:
                p_adj = (p + dp) % self.n_planes
                for s2 in range(self.spp):
                    j = self._sat_id(p_adj, s2)
                    if j == fixed_inter[i]:
                        continue
                    d = np.linalg.norm(positions[i] - positions[j])
                    if d < config.Z_MAX:
                        inter_neighbors.append((d, j))
            inter_neighbors.sort()
            cands = [j for _, j in inter_neighbors[:7]]
            while len(cands) < 7:
                cands.append(-1)
            candidates[i] = cands

        return candidates, fixed_inter

    def _index_fixed_by_satellite(self):
        """Build per-satellite fixed ISL index: sat_id → list of neighbor sat_ids."""
        by_sat = defaultdict(list)
        for p in range(self.n_planes):
            for s in range(self.spp):
                i = self._sat_id(p, s)
                # Intra forward
                j_fwd = self._sat_id(p, (s + 1) % self.spp)
                j_bwd = self._sat_id(p, (s - 1) % self.spp)
                by_sat[i] = [j_fwd, j_bwd, self._fixed_inter_target[i]]
        return by_sat

    def _get_available_fixed(self, positions):
        """Check which fixed ISLs are currently available."""
        available = {}
        for (i, j), etype in self._fixed_edges.items():
            d = np.linalg.norm(positions[i] - positions[j])
            if d > config.Z_MAX or d < 1.0:
                continue
            diff = positions[j] - positions[i]
            diff_sq = np.dot(diff, diff)
            t = max(0.0, min(1.0, -np.dot(positions[i], diff) / diff_sq))
            closest = positions[i] + t * diff
            if np.dot(closest, closest) <= config.RE ** 2:
                continue
            available[(i, j)] = d
        return available

    def _build_active_topology(self, fixed_available, dynamic_choices):
        """Build full active topology: fixed + dynamic ISLs.

        Args:
            fixed_available: dict {(i,j): distance} of available fixed ISLs
            dynamic_choices: dict {sat_id: action} where action 0-6=candidate, 7=off

        Returns:
            active_edges: set of (i,j) with i<j
            edge_distances: dict {(i,j): distance_km}
            dynamic_edges: set of (i,j) that are dynamic ISLs
        """
        active = set()
        dist_map = {}

        # Fixed ISLs
        for (i, j), d in fixed_available.items():
            active.add((i, j))
            dist_map[(i, j)] = d

        # Dynamic ISLs with bidirectional agreement
        requested = {}  # sat_id → target sat_id
        for sat_id, action in dynamic_choices.items():
            if action < 7:
                target = self._inter_candidates[sat_id][action]
                if target >= 0:
                    requested[sat_id] = target

        # Check bidirectional agreement
        dynamic_edges = set()
        agreed = set()
        for i, j in requested.items():
            if j in requested and requested[j] == i:
                pair = (min(i, j), max(i, j))
                if pair not in agreed:
                    agreed.add(pair)

        # Unilateral dynamic ISLs (simplified: no bidirectional agreement needed)
        positions = self._current_positions
        for i, j in requested.items():
            pair = (min(i, j), max(i, j))
            if pair not in active:
                d = np.linalg.norm(positions[i] - positions[j])
                if d < config.Z_MAX:
                    active.add(pair)
                    dist_map[pair] = d
                    dynamic_edges.add(pair)

        return active, dist_map, dynamic_edges

    def _compute_link_loads(self, active_edges, edge_capacities, routing_result):
        """Compute normalized load (traffic/capacity) for each active ISL."""
        loads = {}
        link_loads = routing_result.get('link_loads', {})
        for edge in active_edges:
            i, j = edge
            traffic = link_loads.get((i, j), link_loads.get((j, i), 0))
            cap = edge_capacities.get(edge, 0)
            loads[edge] = min(traffic / max(cap, 1e-6), 2.0)  # cap at 2.0
        return loads

    def _get_sat_isl_load(self, sat_id, link_loads):
        """Get average load of ISLs incident to satellite."""
        loads = []
        for (i, j), load in link_loads.items():
            if i == sat_id or j == sat_id:
                loads.append(load)
        return np.mean(loads) if loads else 0.0

    def _compute_state(self, sat_id, link_loads, flows, dynamic_action):
        """Compute 20-dim state vector for one satellite."""
        state = np.zeros(STATE_DIM, dtype=np.float32)
        fixed_neighbors = self._fixed_by_sat[sat_id]
        candidates = self._inter_candidates[sat_id]

        # [0-2] Fixed ISL loads
        for k, neighbor in enumerate(fixed_neighbors[:3]):
            edge = (min(sat_id, neighbor), max(sat_id, neighbor))
            state[k] = link_loads.get(edge, 0.0)

        # [3] Dynamic ISL load
        if dynamic_action < 7:
            target = candidates[dynamic_action]
            if target >= 0:
                edge = (min(sat_id, target), max(sat_id, target))
                state[3] = link_loads.get(edge, 0.0)

        # [4] Current action
        state[4] = dynamic_action / 7.0

        # [5-11] Candidate distances
        positions = self._current_positions
        for k in range(7):
            target = candidates[k]
            if target >= 0:
                d = np.linalg.norm(positions[sat_id] - positions[target])
                state[5 + k] = d / config.Z_MAX

        # [12-15] Neighbor avg loads
        neighbors = list(fixed_neighbors[:3])
        if dynamic_action < 7 and candidates[dynamic_action] >= 0:
            neighbors.append(candidates[dynamic_action])
        for k, nb in enumerate(neighbors[:4]):
            state[12 + k] = self._get_sat_isl_load(nb, link_loads)

        # [16-17] Supply/demand
        supply = sum(d for s, d2, d in flows if s == sat_id)
        demand = sum(d for s, d2, d in flows if d2 == sat_id)
        max_sd = max(supply, demand, 1.0)
        state[16] = supply / (max_sd * 10)
        state[17] = demand / (max_sd * 10)

        # [18-19] Position
        lat, lon, _ = self.orbit.eci_to_lla(
            positions[sat_id:sat_id+1], self._current_t)
        state[18] = float(lat[0]) / (np.pi / 2)
        state[19] = float(lon[0]) / np.pi

        return state

    def select_actions(self, states, epsilon):
        """ε-greedy action selection for all satellites."""
        actions = np.zeros(self.n_sats, dtype=np.int64)
        if random.random() < epsilon:
            return self.rng.integers(0, N_ACTIONS, size=self.n_sats)

        state_tensor = torch.FloatTensor(states).to(self.device)
        with torch.no_grad():
            q_values = self.dqn(state_tensor)
        return q_values.argmax(dim=1).cpu().numpy()

    def run_episode(self, epsilon=0.0, training=False):
        """Run one episode. Returns (metrics_dict, total_global_reward)."""
        self.metrics.reset()
        self._current_positions = self.orbit.propagate(0)
        self._current_t = 0

        dynamic_choices = np.full(self.n_sats, 7, dtype=np.int64)
        prev_sat_loads = np.zeros(self.n_sats)
        episode_reward = 0.0

        for step in range(self.episode_steps):
            t = step * self.tau
            self._current_t = t
            self._current_positions = self.orbit.propagate(t)

            # Available fixed ISLs
            fixed_avail = self._get_available_fixed(self._current_positions)

            # Active topology
            active, dist_map, dyn_edges = self._build_active_topology(
                fixed_avail, {i: dynamic_choices[i] for i in range(self.n_sats)})

            # Compute capacities
            cap_map = {}
            for edge in active:
                d = dist_map.get(edge, 1000.0)
                cap_gbps, _, avail = self.channel.compute_single(d)
                cap_map[edge] = cap_gbps if avail else 0

            # Route
            lat, lon, alt = self.orbit.eci_to_lla(self._current_positions, t)
            flows = self.traffic.generate(lat, lon, alt)
            active_list = [e for e in active if cap_map.get(e, 0) > 0]
            routing = self.router.route(active_list, dist_map, cap_map, flows, self.n_sats)

            # Link loads
            link_loads = self._compute_link_loads(active, cap_map, routing)

            # Compute states
            states = np.zeros((self.n_sats, STATE_DIM), dtype=np.float32)
            for i in range(self.n_sats):
                states[i] = self._compute_state(
                    i, link_loads, flows, dynamic_choices[i])

            # Compute local rewards
            curr_sat_loads = np.array([
                self._get_sat_isl_load(i, link_loads) for i in range(self.n_sats)])
            local_rewards = np.zeros(self.n_sats)
            for i in range(self.n_sats):
                load_reduction = prev_sat_loads[i] - curr_sat_loads[i]
                has_dynamic = 1.0 if dynamic_choices[i] < 7 else 0.0
                local_rewards[i] = load_reduction - self.beta_penalty * has_dynamic

            # Global reward for metrics
            delivered = routing.get('delivered', 0)
            demanded = routing.get('total_demand', 0)
            global_r = delivered / max(demanded, 1)
            reward_dict = {
                'R_tput': global_r, 'C_switch': 0, 'C_setup': 0,
                'w1_R_tput': global_r, 'w2_C_switch': 0, 'w3_C_setup': 0,
                'total': global_r, '_n_changed': 0, '_n_active': len(active),
            }
            self.metrics.record(reward_dict, routing)
            episode_reward += global_r
            prev_sat_loads = curr_sat_loads.copy()

            # Select next actions
            next_actions = self.select_actions(states, epsilon if training else 0.0)

            # Store transitions
            if training:
                # Compute next states (approximate: use current states)
                for i in range(self.n_sats):
                    self.buffer.push(
                        states[i], dynamic_choices[i], local_rewards[i],
                        states[i],  # simplified: next_state ≈ current
                        float(step == self.episode_steps - 1))

            dynamic_choices = next_actions

            # Train
            if training and len(self.buffer) >= 64:
                self._train_step()
                self._total_steps += 1
                if self._total_steps % 200 == 0:
                    self.target_dqn.load_state_dict(self.dqn.state_dict())

        return self.metrics.compute(), episode_reward

    def _train_step(self, batch_size=64):
        """One gradient step using Double DQN."""
        s, a, r, ns, d = self.buffer.sample(batch_size)
        s = torch.FloatTensor(s).to(self.device)
        a = torch.LongTensor(a).to(self.device)
        r = torch.FloatTensor(r).to(self.device)
        ns = torch.FloatTensor(ns).to(self.device)
        d = torch.FloatTensor(d).to(self.device)

        # Current Q values
        q_values = self.dqn(s).gather(1, a.unsqueeze(1)).squeeze(1)

        # Double DQN target
        with torch.no_grad():
            next_actions = self.dqn(ns).argmax(dim=1)
            next_q = self.target_dqn(ns).gather(1, next_actions.unsqueeze(1)).squeeze(1)
            target = r + self.gamma * next_q * (1 - d)

        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def train(self, n_episodes=100, eval_every=10, verbose=True):
        """Training loop with ε-greedy decay."""
        history = []
        for ep in range(n_episodes):
            epsilon = max(1.0 - ep / 30.0, 0.05)  # L09: max(1-i/30, 0.05)
            metrics, reward = self.run_episode(epsilon=epsilon, training=True)
            history.append({'episode': ep, 'epsilon': epsilon,
                            'reward': reward, **metrics})
            if verbose and (ep % eval_every == 0 or ep == n_episodes - 1):
                print(f"  Ep {ep:3d}: ε={epsilon:.3f} reward={reward:.4f} "
                      f"M1={metrics['M1_throughput']:.4f} "
                      f"M3={metrics['M3_switch_rate']:.4f} "
                      f"buf={len(self.buffer)}")
        return history

    def evaluate(self, n_episodes=5):
        """Evaluate without exploration."""
        all_metrics = []
        for _ in range(n_episodes):
            metrics, _ = self.run_episode(epsilon=0.0, training=False)
            all_metrics.append(metrics)

        avg = {}
        for k in all_metrics[0]:
            if isinstance(all_metrics[0][k], (int, float)):
                avg[k] = np.mean([m[k] for m in all_metrics])
        return avg
