"""Traffic demand generation: compound Poisson, uniform, spatial-correlated."""
import numpy as np

from .config import SimConfig


def compound_poisson_demand(n_beams: int, config: SimConfig, rng: np.random.Generator) -> np.ndarray:
    """Compound Poisson demand per beam in Mbps.

    Number of arrivals per beam ~ Poisson(λ), each arrival ~ Uniform(d_min, d_max).
    λ chosen so mean demand ≈ 360 Mbps (midpoint of 20-700).
    """
    d_mid = (config.demand_min_mbps + config.demand_max_mbps) / 2.0
    d_range = config.demand_max_mbps - config.demand_min_mbps
    target_mean = 360.0
    lam = max(1.0, target_mean / d_mid)  # expected arrivals for target mean

    demands = np.zeros(n_beams)
    for i in range(n_beams):
        n_arrivals = rng.poisson(lam)
        if n_arrivals == 0:
            demands[i] = config.demand_min_mbps
        else:
            demands[i] = np.sum(rng.uniform(config.demand_min_mbps, config.demand_max_mbps, n_arrivals))
            demands[i] = np.clip(demands[i], config.demand_min_mbps, config.demand_max_mbps * 3)
    return demands


def uniform_demand(n_beams: int, config: SimConfig, rng: np.random.Generator) -> np.ndarray:
    """Uniform random demand per beam in [d_min, d_max] Mbps."""
    return rng.uniform(config.demand_min_mbps, config.demand_max_mbps, n_beams)


def spatial_correlated_demand(
    n_beams: int,
    beam_positions: np.ndarray,
    config: SimConfig,
    rng: np.random.Generator,
) -> np.ndarray:
    """Spatially correlated demand using Gaussian kernel on positions.

    Generates correlated noise via Gaussian kernel, then scales to [d_min, d_max].
    """
    from .antenna import hex_grid_positions
    if beam_positions is None:
        beam_positions = hex_grid_positions(config.n_rings)

    # Pairwise distances
    diff = beam_positions[:, None, :] - beam_positions[None, :, :]
    dist = np.linalg.norm(diff, axis=2)

    # Gaussian kernel (bandwidth = 1.5 grid units)
    sigma = 1.5
    K = np.exp(-dist ** 2 / (2 * sigma ** 2))

    # Generate correlated noise via Cholesky
    L = np.linalg.cholesky(K + 1e-6 * np.eye(n_beams))
    noise = L @ rng.standard_normal(n_beams)

    # Normalize to [0, 1] then scale to demand range
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-12)
    return config.demand_min_mbps + noise * (config.demand_max_mbps - config.demand_min_mbps)


class TrafficGenerator:
    """Configurable traffic demand generator."""

    MODES = {
        'compound_poisson': compound_poisson_demand,
        'uniform': uniform_demand,
        'spatial': spatial_correlated_demand,
    }

    def __init__(self, config: SimConfig, mode: str = 'compound_poisson', seed: int | None = None):
        self.config = config
        self.mode = mode
        self.rng = np.random.default_rng(seed)

    def generate(self, beam_positions: np.ndarray | None = None) -> np.ndarray:
        """Generate demand array of shape (n_beams,)."""
        if self.mode == 'spatial':
            if beam_positions is None:
                from .antenna import hex_grid_positions
                beam_positions = hex_grid_positions(self.config.n_rings)
            return spatial_correlated_demand(self.config.n_beams, beam_positions, self.config, self.rng)
        elif self.mode == 'uniform':
            return uniform_demand(self.config.n_beams, self.config, self.rng)
        else:
            return compound_poisson_demand(self.config.n_beams, self.config, self.rng)
