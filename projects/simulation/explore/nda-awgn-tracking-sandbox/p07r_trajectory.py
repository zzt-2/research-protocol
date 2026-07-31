# -*- coding: utf-8 -*-
"""P07-R — stateful time-correlated GG trajectory generator (H3 LIFECYCLE fix).

The OLD runner (`_p07_runner.py`) regenerated an INDEPENDENT GG realization
every window (seed=ws per window; `gg_block` draws independent Gamma RVs) ->
empirical inter-window ACF ~ 0, contradicting a time-correlated GG control
premise. This module generates ONE continuous AR(1) GG amplitude trajectory
shared across all methods, with rho = exp(-window_dt / tau_c), tau_c = 1/(2*pi*f_G).

Each window gets ONE GG amplitude h_w (block-static within the window, AR(1)
across windows), drawn from the exact Gamma(alpha,1/alpha) x Gamma(beta,1/beta)
edges via the 'gar' method (`_gg_time._gamma_ar1_exact`). The signal model is
IDENTICAL to `generate_shared_realization_apsk` (signal = tx*sqrt(h)*carrier +
AWGN, noise_var = 1/(2*gamma)), only the per-window h is now time-correlated.

This is the H3 fix: a real stateful trajectory with rho != 0, shared by all
methods (TL-13 channel sharing), no per-window independent seed reset.

rho levels (P06 precedent, f_G in {30,100,1000} Hz):
  - the window_dt is the AGC update interval; chosen so rho spans ~0.99/0.97/0.70
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

from common._channel import _resolve_turb_params  # noqa: E402
from common._gg_time import _gamma_ar1_exact  # noqa: E402
from common._modulation import m16apsk_mod  # noqa: E402
from common._channel import doppler_phase  # noqa: E402
from params import SimulationConfig  # noqa: E402


def rho_from_fG(f_G, window_dt):
    """rho = exp(-window_dt / tau_c), tau_c = 1/(2*pi*f_G)."""
    tau_c = 1.0 / (2.0 * np.pi * f_G)
    return float(np.exp(-window_dt / tau_c))


def generate_trajectory(n_windows, scene, gamma_bar, f_G, window_dt,
                        n_sym_per_window, mod="m16apsk", seed=0,
                        turb_params=None):
    """Generate ONE continuous time-correlated GG trajectory.

    Returns a list of per-window realization dicts (same schema as
    generate_shared_realization_apsk) but with h drawn from a SHARED AR(1)
    trajectory (rho = exp(-window_dt/tau_c)), so consecutive windows are
    time-correlated. All methods must consume the SAME trajectory (TL-13).

    Within a window, h is constant over its n_sym_per_window symbols (block-
    static physical assumption, tau_c >> symbol period). Across windows, h
    evolves AR(1) with rho.
    """
    a, b = _resolve_turb_params(scene, turb_params)
    rho = rho_from_fG(f_G, window_dt)
    rng = np.random.default_rng(seed)

    # AR(1) exact-Gamma-edge trajectories (one value per window) for big & small
    big = _gamma_ar1_exact(n_windows, a, rho, rng)
    small = _gamma_ar1_exact(n_windows, b, rho, rng)
    h_windows = big * small   # GG envelope, mean ~ 1

    cfg = SimulationConfig()
    f_dot = cfg.doppler.DOPPLER_HIGH
    lw = None   # doppler_phase reads LASER_LW from params (D-007 unified)
    noise_var = 1.0 / (2.0 * gamma_bar)

    windows = []
    for w in range(n_windows):
        h = float(h_windows[w])
        # bits/tx per window (deterministic given the sub-rng stream)
        if mod == "m16apsk":
            bits = rng.integers(0, 2, n_sym_per_window * 4)
            tx = m16apsk_mod(bits)
        else:
            raise ValueError(f"mod must be 'm16apsk', got {mod!r}")
        phi = doppler_phase(n_sym_per_window, f_dot=f_dot, lw=lw)
        carrier = np.exp(1j * phi)
        signal = tx * np.sqrt(h) * carrier
        noise = np.sqrt(noise_var) * (rng.standard_normal(n_sym_per_window)
                                      + 1j * rng.standard_normal(n_sym_per_window))
        rx_raw = signal + noise
        # h_blocks mirror the channel schema: median over blocks (here 1 block)
        windows.append({
            "rx_raw": rx_raw, "bits": bits, "tx": tx,
            "h": np.full(n_sym_per_window, h),
            "h_blocks": np.array([h]),
            "h_med": h, "phi": phi,
            "Ns": n_sym_per_window, "gamma_bar": gamma_bar,
            "turb_name": scene, "f_dot": f_dot, "mod": mod,
            "window_index": w, "f_G": f_G, "rho": rho, "h_scalar": h,
        })
    return windows, {"alpha": float(a), "beta": float(b), "rho": rho,
                     "f_G": float(f_G), "window_dt": float(window_dt),
                     "n_windows": int(n_windows)}


def empirical_acf(x, max_lag=10):
    """Empirical ACF of a 1D series at lags 1..max_lag."""
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    v = np.var(x)
    if v <= 0:
        return {f"lag{k}": 0.0 for k in range(1, max_lag + 1)}
    return {f"lag{k}": float(np.sum(x[:-k] * x[k:]) / ((len(x) - k) * v))
            for k in range(1, max_lag + 1)}
