"""M5: Reward calculation — normalized reward function v2."""

import numpy as np
from numpy.typing import NDArray


def compute_reward(
    r_norm: float | NDArray,
    l_norm: float | NDArray,
    blocked: bool | NDArray,
    switched: bool | NDArray,
    w_r: float = 0.6,
    w_l: float = 0.4,
    w_b: float = 0.5,
    w_h: float = 0.1,
) -> float | NDArray:
    """r(t) = w_r·R_norm + w_l·L_norm − w_b·B − w_h·H.

    B and L_norm are mutually exclusive: B=1 implies L_norm≤0.
    """
    return (w_r * r_norm
            + w_l * l_norm
            - w_b * np.asarray(blocked, dtype=float)
            - w_h * np.asarray(switched, dtype=float))


def decompose_reward(
    r_norm: float | NDArray,
    l_norm: float | NDArray,
    blocked: bool | NDArray,
    switched: bool | NDArray,
    w_r: float = 0.6,
    w_l: float = 0.4,
    w_b: float = 0.5,
    w_h: float = 0.1,
) -> dict[str, float]:
    """Return absolute contribution of each term for MDP checkpoint."""
    wr = np.abs(w_r * r_norm).sum()
    wl = np.abs(w_l * l_norm).sum()
    wb = np.abs(w_b * np.asarray(blocked, dtype=float)).sum()
    wh = np.abs(w_h * np.asarray(switched, dtype=float)).sum()
    total = wr + wl + wb + wh + 1e-12
    return {
        "throughput_abs": float(wr),
        "load_abs": float(wl),
        "blocked_abs": float(wb),
        "handover_abs": float(wh),
        "throughput_pct": float(wr / total * 100),
        "load_pct": float(wl / total * 100),
        "blocked_pct": float(wb / total * 100),
        "handover_pct": float(wh / total * 100),
    }
