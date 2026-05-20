"""Random and Fixed baseline policies."""

from __future__ import annotations

import numpy as np


class RandomPolicy:
    """Uniformly random phase shifts in [-1, 1]^N."""

    def __init__(self, N: int):
        self.N = N

    def select_action(self, obs: np.ndarray) -> np.ndarray:
        return np.random.uniform(-1, 1, size=self.N).astype(np.float32)


class FixedPolicy:
    """Fixed phase shifts (default: all zeros -> theta = pi)."""

    def __init__(self, N: int, fixed_value: float = 0.0):
        self.action = np.full(N, fixed_value, dtype=np.float32)

    def select_action(self, obs: np.ndarray) -> np.ndarray:
        return self.action.copy()
