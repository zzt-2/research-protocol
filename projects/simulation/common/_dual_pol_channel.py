"""Shared dual-polarization time-varying Gamma-Gamma channel generation."""

import numpy as np

from params import SimulationConfig

from ._gg_time import gg_time_envelope


def generate_shared_realization_dp(
    N,
    alpha,
    beta,
    f_g,
    sop_rate,
    seed,
    gamma_bar=None,
    block=None,
    t_s=None,
    method=None,
):
    """Generate one shared dual-polarization QPSK channel realization.

    Optional physical parameters are resolved from ``SimulationConfig`` at
    call time so callers can override them explicitly without frozen defaults.
    """
    cfg = SimulationConfig()
    gamma_bar = (
        cfg.experiment.GAMMA_BAR_DEFAULT if gamma_bar is None else gamma_bar
    )
    block = cfg.experiment.BLOCK if block is None else block
    t_s = cfg.system.T_S if t_s is None else t_s
    method = cfg.gg_time.AR1_METHOD if method is None else method

    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(
        N,
        alpha,
        beta,
        tau_c,
        block=block,
        t_s=t_s,
        method=method,
        seed=seed,
    )

    bitsX = rng.integers(0, 2, N * 2)
    sX = (
        (1 - 2 * bitsX[0::2]) + 1j * (1 - 2 * bitsX[1::2])
    ) / np.sqrt(2)
    bitsY = rng.integers(0, 2, N * 2)
    sY = (
        (1 - 2 * bitsY[0::2]) + 1j * (1 - 2 * bitsY[1::2])
    ) / np.sqrt(2)

    theta = sop_rate * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * gamma_bar)
    rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) + np.sqrt(nv) * (
        rng.standard_normal(N) + 1j * rng.standard_normal(N)
    )
    rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) + np.sqrt(nv) * (
        rng.standard_normal(N) + 1j * rng.standard_normal(N)
    )

    return {
        "rX": rX,
        "rY": rY,
        "sX": sX,
        "sY": sY,
        "h": h,
        "theta": theta,
        "bitsX": bitsX,
        "bitsY": bitsY,
        # Compatibility aliases: remove only after every downstream consumer
        # has migrated to the canonical bitsX/bitsY names.
        "bitX": bitsX,
        "bitY": bitsY,
    }
