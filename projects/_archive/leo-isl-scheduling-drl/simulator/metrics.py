"""M8: MetricsCollector — episode-level metrics M1-M5.

M1: Throughput ratio  = Σq / Σd
M2: Avg e2e delay     = Σ(path_delay × q) / Σq
M3: Link switch rate  = Σ_t n_changed(t) / (T × max(Σ n_active, 1))
M4: Blocking rate     = 1 - M1
M5: Fairness index    = 1 - CV(q_i/d_i)
"""

import numpy as np
from collections import defaultdict


class MetricsCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self._total_delivered = 0.0
        self._total_demanded = 0.0
        self._total_changes = 0
        self._total_active = 0
        self._n_steps = 0
        self._flow_ratios = []
        self._rewards = []

    def record(self, reward_dict, routing_result):
        """Record per-step data."""
        self._total_delivered += routing_result.get('delivered', 0)
        self._total_demanded += routing_result.get('total_demand', 0)
        self._total_changes += reward_dict.get('_n_changed', 0)
        self._total_active += reward_dict.get('_n_active', 0)
        self._n_steps += 1
        self._rewards.append(reward_dict.get('total', 0))

        # Per-flow delivery ratios for fairness
        for fd in routing_result.get('flow_details', []):
            src, dst, delivered, demanded, path = fd
            if demanded > 0:
                self._flow_ratios.append(delivered / demanded)

    def compute(self):
        """Compute episode-level metrics."""
        m1 = self._total_delivered / self._total_demanded if self._total_demanded > 0 else 0
        m3 = self._total_changes / max(self._total_active, 1)
        m4 = 1 - m1

        # Fairness index (Jain's)
        if len(self._flow_ratios) > 0:
            ratios = np.array(self._flow_ratios)
            m5 = (ratios.sum() ** 2) / (len(ratios) * (ratios ** 2).sum() + 1e-30)
        else:
            m5 = 1.0

        avg_reward = np.mean(self._rewards) if self._rewards else 0

        return {
            'M1_throughput': m1,
            'M3_switch_rate': m3,
            'M4_blocking_rate': m4,
            'M5_fairness': m5,
            'avg_reward': avg_reward,
            'total_delivered': self._total_delivered,
            'total_demanded': self._total_demanded,
            'n_steps': self._n_steps,
        }
