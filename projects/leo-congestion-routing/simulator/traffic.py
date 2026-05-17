"""Non-uniform traffic generator for LEO constellation routing.

Supports heavy/light flow mix, hotspot destinations, time-varying modulation
(NHPP), and surge bursts.
Extended from mve_env.py _generate_flows().
"""

from __future__ import annotations

import math

import numpy as np

from .config import SimConfig


class TrafficGenerator:
    def __init__(self, config: SimConfig) -> None:
        self._config = config
        self._popular: list[int] | None = None

    def generate(
        self,
        rng: np.random.Generator,
        t: int = 0,
    ) -> list[tuple[int, int, float]]:
        """Generate (src, dst, demand) flow demands.

        Args:
            rng: numpy random generator instance.
            t: current time step (used for time-varying modulation).
        """
        cfg = self._config
        N = cfg.n_nodes

        # Cache hotspot destinations on first call
        if self._popular is None:
            self._popular = rng.choice(N, cfg.n_popular, replace=False).tolist()

        flows: list[tuple[int, int, float]] = []

        # Heavy flows → hotspot destinations
        for _ in range(cfg.n_heavy):
            dst = int(rng.choice(self._popular))
            src = int(rng.integers(0, N))
            while src == dst:
                src = int(rng.integers(0, N))
            demand = float(rng.uniform(*cfg.heavy_demand_range))
            flows.append((src, dst, demand))

        # Light flows → random pairs
        n_light = cfg.n_flows - cfg.n_heavy
        for _ in range(n_light):
            src = int(rng.integers(0, N))
            dst = int(rng.integers(0, N))
            while src == dst:
                dst = int(rng.integers(0, N))
            demand = float(rng.uniform(*cfg.light_demand_range))
            flows.append((src, dst, demand))

        # Time-varying modulation
        if cfg.time_varying and cfg.t_slots > 0:
            modulation = 1.0 + cfg.tv_amplitude * math.sin(
                2.0 * math.pi * t / cfg.t_slots
            )
            flows = [(s, d, dm * modulation) for s, d, dm in flows]

        # Surge burst
        if cfg.surge_factor > 1.0:
            surged: list[tuple[int, int, float]] = []
            for s, d, dm in flows:
                if rng.random() < 0.1:
                    surged.append((s, d, dm * cfg.surge_factor))
                else:
                    surged.append((s, d, dm))
            flows = surged

        rng.shuffle(flows)
        return flows
