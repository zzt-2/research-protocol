"""Proposed methods + arm wiring for the Pilot-Jones complex-model salvage (T003).

Method candidates (T003 Phase 4) — mechanism-distinct, not lambda grids:
  P1 condition/energy-aware covariance-weighted Jones estimate
     (weight per-pilot LS rows by a receiver-visible reliability proxy =
      received pilot energy; down-weight faded/noisy pilots). Mechanism:
      inverse-variance weighting of the LS normal equations.
  P2 uncertainty-aware temporal tracker (alpha(cond, innov) EMA) [T002's P]
  P3 physics-structured whitening tracker (only if PDL gate holds)

Each method is described by the Phase-4 template:
  legal inputs | state | equation | output | causal timing | complexity |
  mechanism | strongest cheap alternative | falsifier | packaging claim
(see salvage-contract.yaml for the full per-method tables).

Receiver-visible ONLY. Oracle reads true Jones (tagged).
"""
from __future__ import annotations
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from conventional_baselines import (inject_dual_pilots, estimate_jones_blocks,
                                    derotate, derotate_oracle,
                                    _whitening_inverse, _regularized_inverse)


# ---------------------------------------------------------------------------
# Standard complex Godard-z 2x2 CMA core (identical to T002 pilot_jones_methods)
# ---------------------------------------------------------------------------

def _cma_norm(w):
    return float(np.sqrt(sum(np.sum(np.abs(v) ** 2) for v in w.values())))


def run_standard_cma(rX, rY, *, mu, taps, r2, block_size, eval_start, eval_end):
    rX = np.asarray(rX); rY = np.asarray(rY)
    x_win = sliding_window_view(rX, taps)
    y_win = sliding_window_view(rY, taps)
    half = taps // 2
    weights = {n: np.zeros(taps, dtype=complex) for n in ("wxx", "wxy", "wyx", "wyy")}
    weights["wxx"][half] = weights["wyy"][half] = 1.0
    initial_norm = _cma_norm(weights)
    n_blocks = max(0, (len(rX) - taps + 1) // block_size)
    out_x = np.zeros(eval_end - eval_start, dtype=complex)
    out_y = np.zeros_like(out_x)
    valid = np.zeros(len(out_x), dtype=bool)
    diverged = False; div_sym = None
    for block in range(n_blocks):
        s = block * block_size; e = s + block_size; os = s + half
        x, y = x_win[s:e], y_win[s:e]
        z_x = x @ weights["wxx"] + y @ weights["wxy"]
        z_y = x @ weights["wyx"] + y @ weights["wyy"]
        left, right = max(os, eval_start), min(os + block_size, eval_end)
        if left < right:
            src = slice(left - os, right - os); dst = slice(left - eval_start, right - eval_start)
            out_x[dst], out_y[dst] = z_x[src], z_y[src]; valid[dst] = True
        ex = r2 - np.abs(z_x) ** 2; ey = r2 - np.abs(z_y) ** 2
        weights["wxx"] += mu * np.mean((ex * z_x)[:, None] * np.conj(x), axis=0)
        weights["wxy"] += mu * np.mean((ex * z_x)[:, None] * np.conj(y), axis=0)
        weights["wyx"] += mu * np.mean((ey * z_y)[:, None] * np.conj(x), axis=0)
        weights["wyy"] += mu * np.mean((ey * z_y)[:, None] * np.conj(y), axis=0)
        nrm = _cma_norm(weights)
        if (not np.isfinite(nrm)) or nrm > 10 * initial_norm:
            diverged = True; div_sym = int(os + block_size); break
    return {"zX": out_x, "zY": out_y, "valid_mask": valid,
            "diverged": diverged, "divergence_symbol": div_sym}


# ---------------------------------------------------------------------------
# Proposed P1: energy-weighted (inverse-variance) pilot-LS Jones estimate.
# ---------------------------------------------------------------------------

def estimate_jones_blocks_weighted(pilot_rx, *, block_size, energy_power=1.0):
    """Per-block pilot-LS Jones estimate with per-pilot reliability weighting.

    Weight = |received pilot energy|^energy_power (receiver-visible: just the RX
    magnitude at pilot positions). Down-weights faded/noisy pilots. This is a
    standard inverse-variance-weighted LS (weighted normal equations); the
    MECHANISM is reliability-aware estimation, distinct from a single fixed EMA
    (B1) or a post-hoc regularizer (B2). Falsifier: if the channel is
    well-conditioned and all pilots have ~equal energy, weights -> 1 and P1
    degenerates to B0 (no gain)."""
    rx = np.asarray(pilot_rx["rX"]); ry = np.asarray(pilot_rx["rY"])
    mask = np.asarray(pilot_rx["pilot_mask"])
    ps = np.asarray(pilot_rx["pilot_symbols"])
    estimates = []
    for start in range(0, len(rx), block_size):
        idx = np.flatnonzero(mask[start:start + block_size]) + start
        if len(idx) < 2:
            continue
        P = ps[:, idx].T                      # (M,2)
        Y = np.stack((rx[idx], ry[idx]), axis=1)  # (M,2)
        # receiver-visible reliability weight from RX energy
        e = np.abs(rx[idx]) ** 2 + np.abs(ry[idx]) ** 2
        w = e ** energy_power
        w = w / (w.mean() + 1e-12)
        Wd = w[:, None]
        # weighted LS: (P^H W P)^-1 P^H W Y
        PHWP = P.conj().T @ (Wd * P)
        PHWY = P.conj().T @ (Wd * Y)
        H = np.linalg.lstsq(PHWP, PHWY, rcond=None)[0].T
        estimates.append({"block": start, "matrix": H,
                          "cond": float(np.linalg.cond(H))})
    return estimates


def derotate_weighted(pilot_rx, estimates, *, block_size, ema_alpha=None,
                      data_only=True, whitening_kappa=1e3, use_whitening=False):
    """Apply P1's energy-weighted estimate, optionally EMA-smoothed and/or
    whitened. Receiver-visible only."""
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    ema_h = None
    for est in estimates:
        start = est["block"]
        idx = np.arange(start, min(start + block_size, len(x)))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        H = np.asarray(est["matrix"], complex)
        if ema_alpha is not None:
            ema_h = H if ema_h is None else ema_alpha * ema_h + (1 - ema_alpha) * H
            H = ema_h
        inv = _whitening_inverse(H, kappa_cap=whitening_kappa) if use_whitening \
            else _regularized_inverse(H, 0.0, None)
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y}


# ---------------------------------------------------------------------------
# Oracle ceiling for PMD: frequency-domain MMSE (tagged). For memoryless models
# this equals the memoryless oracle; for M3 it additionally removes ISI, giving
# the true headroom ceiling.
# ---------------------------------------------------------------------------

def oracle_fde(realization_imp, *, block_size, gamma_bar, data_only=True):
    """Tagged frequency-domain MMSE oracle per block. Removes both the Jones
    mix AND any ISI (PMD). Uses the true per-block Jones + the true PSP delays.
    Upper-bound / Kill only — NEVER a Go opponent (T003 rule 8)."""
    n = len(realization_imp["rX"])
    x = np.array(realization_imp["rX"], copy=True); y = np.array(realization_imp["rY"], copy=True)
    dm = np.asarray(realization_imp.get("data_mask",
                  np.ones(n, dtype=bool))) if "data_mask" in realization_imp \
        else np.ones(n, dtype=bool)
    J = np.asarray(realization_imp["jones_truth"])
    dgd_ps = realization_imp["model_params"].get("dgd_ps", 0.0)
    t_s = realization_imp["model_params"].get("t_s", 4e-10)
    delay_samples = dgd_ps * 1e-12 / t_s
    n_blocks = J.shape[0]
    for b in range(n_blocks):
        start = b * block_size
        en = min(start + block_size, n)
        L = en - start
        if L <= 0:
            continue
        seg = np.stack((x[start:en], y[start:en]), axis=0)
        # frequency-domain Jones with PSP differential delay
        U, sv, Vh = np.linalg.svd(J[b])
        nfft = max(8, 1 << int(np.ceil(np.log2(L))))
        f = np.fft.fftfreq(nfft)
        # per-frequency Jones: U @ diag(sv_i * exp(-j 2 pi f tau_i)) @ Vh
        tau = delay_samples * np.array([0.5, -0.5])
        Hf = np.zeros((nfft, 2, 2), dtype=complex)
        for fi in range(nfft):
            D = sv * np.exp(-1j * 2 * np.pi * f[fi] * tau)
            Hf[fi] = U @ np.diag(D) @ Vh
        # zero-pad segment, FFT
        pad = np.zeros((2, nfft), dtype=complex)
        pad[:, :L] = seg
        Rf = np.fft.fft(pad, axis=1)  # (2, nfft)
        # MMSE inverse per frequency
        nv = 1.0 / (2 * gamma_bar)
        Xf = np.zeros((2, nfft), dtype=complex)
        for fi in range(nfft):
            Xf[:, fi] = np.linalg.solve(
                Hf[fi].conj().T @ Hf[fi] + nv * np.eye(2),
                Hf[fi].conj().T @ Rf[:, fi])
        xhat = np.fft.ifft(Xf, axis=1)[:, :L]
        # write back data positions only
        idx = np.arange(start, en)
        if data_only:
            m = dm[start:en]
            idx = idx[m]; xhat = xhat[:, m]
        x[idx] = xhat[0]; y[idx] = xhat[1]
    return {"rX": x, "rY": y}


# ---------------------------------------------------------------------------
# Arm wiring
# ---------------------------------------------------------------------------

def build_arm_view(realization_imp, derotated_or_rx):
    return {**realization_imp,
            "rX": derotated_or_rx["rX"], "rY": derotated_or_rx["rY"]}
