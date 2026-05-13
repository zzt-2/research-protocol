"""Traffic matrix generation: uniform / hotspot / distance-weighted."""
import numpy as np


def generate_traffic(N, mode='uniform', positions=None, total_demand=1.0, rng=None):
    """Generate traffic demand matrix (N, N). Diagonal is zero.

    Modes:
        uniform: equal probability per pair
        hotspot: 10% nodes produce 50% traffic
        distance: probability inversely proportional to node distance
    """
    if rng is None:
        rng = np.random.default_rng()

    if mode == 'uniform':
        tm = rng.random((N, N))
    elif mode == 'hotspot':
        tm = rng.random((N, N))
        n_hot = max(1, int(0.1 * N))
        hot = rng.choice(N, n_hot, replace=False)
        tm[hot, :] *= 3.0
        tm[:, hot] *= 3.0
    elif mode == 'distance':
        if positions is None:
            raise ValueError("distance mode requires satellite positions")
        diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
        dist = np.sqrt((diff ** 2).sum(axis=-1))
        dist = np.maximum(dist, 1.0)
        tm = 1.0 / dist
    else:
        raise ValueError(f"Unknown traffic mode: {mode}")

    np.fill_diagonal(tm, 0.0)
    tm = tm / tm.sum() * total_demand
    return tm


def sample_flows(tm, n_flows, rng=None):
    """Sample source-destination pairs from traffic matrix.

    Returns (n_flows, 2) array of (src, dst) pairs weighted by demand.
    """
    if rng is None:
        rng = np.random.default_rng()
    probs = tm.ravel() / tm.sum()
    indices = rng.choice(len(probs), size=n_flows, replace=True, p=probs)
    src = indices // tm.shape[1]
    dst = indices % tm.shape[1]
    return np.stack([src, dst], axis=-1)
