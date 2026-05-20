"""PSO (Particle Swarm Optimization) for RIS phase-shift optimization."""

from __future__ import annotations

import numpy as np


class PSOOptimizer:
    """Particle Swarm Optimization that evolves within each episode.

    Each particle holds a phase-shift vector in [-1, 1]^N.
    At each environment step, particles are updated once and the
    global-best position is returned as the action.
    """

    def __init__(
        self,
        N: int,
        n_particles: int = 30,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        v_max: float = 0.2,
    ):
        self.N = N
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max

        # State initialized in initialize()
        self.positions: np.ndarray | None = None  # (n_particles, N)
        self.velocities: np.ndarray | None = None  # (n_particles, N)
        self.personal_best: np.ndarray | None = None  # (n_particles, N)
        self.personal_best_fitness: np.ndarray | None = None  # (n_particles,)
        self._global_best: np.ndarray | None = None  # (N,)
        self._global_best_fitness: float = -np.inf

    def initialize(self):
        """Randomly initialize swarm at the start of each episode."""
        self.positions = np.random.uniform(-1, 1, (self.n_particles, self.N)).astype(np.float32)
        self.velocities = np.random.uniform(
            -self.v_max, self.v_max, (self.n_particles, self.N)
        ).astype(np.float32)
        self.personal_best = self.positions.copy()
        self.personal_best_fitness = np.full(self.n_particles, -np.inf, dtype=np.float32)
        self._global_best = self.positions[0].copy()
        self._global_best_fitness = -np.inf

    @property
    def best_position(self) -> np.ndarray:
        """Current global-best position in [-1, 1]^N."""
        return self._global_best.copy()

    def step(self, fitness_fn) -> np.ndarray:
        """Execute one PSO iteration and return global-best position.

        Args:
            fitness_fn: callable(phases: (n_particles, N)) -> (n_particles,)
                Evaluates sum-rate for each particle's phase-shift vector.

        Returns:
            Global-best action in [-1, 1]^N.
        """
        # Evaluate all particles
        fitness = fitness_fn(self.positions)  # (n_particles,)

        # Update personal bests
        improved = fitness > self.personal_best_fitness
        self.personal_best[improved] = self.positions[improved]
        self.personal_best_fitness[improved] = fitness[improved]

        # Update global best
        best_idx = np.argmax(self.personal_best_fitness)
        if self.personal_best_fitness[best_idx] > self._global_best_fitness:
            self._global_best = self.personal_best[best_idx].copy()
            self._global_best_fitness = self.personal_best_fitness[best_idx]

        # Velocity update
        r1 = np.random.uniform(0, 1, (self.n_particles, self.N)).astype(np.float32)
        r2 = np.random.uniform(0, 1, (self.n_particles, self.N)).astype(np.float32)
        self.velocities = (
            self.w * self.velocities
            + self.c1 * r1 * (self.personal_best - self.positions)
            + self.c2 * r2 * (self._global_best[np.newaxis, :] - self.positions)
        )
        # Clamp velocities
        self.velocities = np.clip(self.velocities, -self.v_max, self.v_max)

        # Position update
        self.positions = self.positions + self.velocities
        self.positions = np.clip(self.positions, -1.0, 1.0)

        return self.best_position
