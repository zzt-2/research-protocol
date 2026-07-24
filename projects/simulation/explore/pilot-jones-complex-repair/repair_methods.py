"""Proposed methods + arm wiring for the Pilot-Jones REPAIR (T004).

Oracle (V038 defect #5 fix): the tagged oracle must invert the FULL polarization
channel = component op (memoryless Jones + PSP-basis PMD FIR) composed with the
canonical atmosphere sqrt(h) R(theta). T003's FDE oracle only inverted the
component PMD and left the per-symbol SOP rotation R(theta) uncompensated, which
is why receiver-visible B1 beat it on the M3 cells. Here the oracle:
  - frequency-domain-inverts the component (Jones + PSP differential delay), and
  - additionally undoes R(theta) per symbol, and the scalar sqrt(h) fade.
It reads the TRUE Jones, TRUE PSP delays, TRUE theta and TRUE h (tagged). With
exact truth and no noise the recovery error must be < 1e-10 (semantic gate #7).
The oracle is a ceiling / Kill tool ONLY, never a Go opponent (FR-25).

Proposed method candidates (mechanism-distinct; adaptation-scan A1-A6 first).
Each is described by the Phase-4 template in repair-contract.yaml.
"""
from __future__ import annotations
import numpy as np

import semantic_channel as sc
import pilot_and_baselines as pb
from pilot_and_baselines import (estimate_jones_single_tap,
                                 estimate_jones_tapped,
                                 derotate_single_tap, derotate_tapped,
                                 _whitening_inverse, _regularized_inverse)


# ---------------------------------------------------------------------------
# Oracle: invert the FULL polarization channel (component + R(theta) + h).
# Ceiling / Kill ONLY.
# ---------------------------------------------------------------------------

def oracle_full_inverse(realization_imp, *, block_size, gamma_bar,
                        data_only=True, data_mask=None):
    """Tagged frequency-domain MMSE oracle that inverts the component channel
    (Jones + PSP differential delay) AND the canonical per-symbol SOP rotation
    R(theta) AND the scalar sqrt(h) fade. Uses the TRUE Jones, TRUE PSP delays,
    TRUE theta, TRUE h. Upper bound / Kill only.

    For a memoryless model (M0/M1/M2) this reduces to inverting J_b then R(-theta)
    then dividing by sqrt(h). For M3/M4 it additionally deconvolves the PSP-basis
    differential delay in the frequency domain per block.
    """
    n = len(realization_imp["rX"])
    x = np.array(realization_imp["rX"], copy=True)
    y = np.array(realization_imp["rY"], copy=True)
    J = np.asarray(realization_imp["jones_truth"])
    theta = np.asarray(realization_imp["theta"])
    h = np.asarray(realization_imp["h"])
    mp = realization_imp["model_params"]
    dgd_samples = mp["dgd_samples"]
    pmd_enabled = mp["pmd_enabled"]
    nv = 1.0 / (2 * gamma_bar)
    n_blocks = J.shape[0]
    dm = data_mask if data_mask is not None else np.ones(n, dtype=bool)
    for b in range(n_blocks):
        start = b * block_size
        en = min(start + block_size, n)
        L = en - start
        if L <= 0:
            continue
        seg = np.stack((x[start:en], y[start:en]), axis=0)      # (2, L)
        idx = np.arange(start, en)
        if pmd_enabled and dgd_samples > 1e-12:
            # SAME FFT-circular convention as the forward apply_component
            # (pmd_circular_freq), so forward and oracle are exact inverses modulo
            # the block-boundary transient (PMD_GUARD samples, excluded below).
            nfft = L
            Hf, U, sv, Vh = sc.pmd_circular_freq(J[b], dgd_samples, nfft)
            Rf = np.fft.fft(seg, axis=1)             # (2, nfft)
            Xf = np.zeros((2, nfft), dtype=complex)
            for fi in range(nfft):
                Xf[:, fi] = np.linalg.solve(Hf[fi].conj().T @ Hf[fi] + nv * np.eye(2),
                                            Hf[fi].conj().T @ Rf[:, fi])
            post = np.fft.ifft(Xf, axis=1)           # (2, nfft)
        else:
            # memoryless component inverse (MMSE in J)
            Hf = J[b]
            post = np.linalg.solve(Hf.conj().T @ Hf + nv * np.eye(2),
                                   Hf.conj().T @ seg)
        # undo per-symbol SOP rotation R(-theta) and scalar fade sqrt(h)
        ct = np.cos(theta[idx]); st = np.sin(theta[idx])
        sh = np.sqrt(h[idx])
        rot_back = np.stack((ct * post[0] - st * post[1],
                             st * post[0] + ct * post[1]), axis=0)
        rot_back = rot_back / sh[np.newaxis, :]
        m = dm[start:en]
        x[idx[m]] = rot_back[0, m]
        y[idx[m]] = rot_back[1, m]
    return {"rX": x, "rY": y}


def build_arm_view(realization_imp, derotated_or_rx):
    return {**realization_imp,
            "rX": derotated_or_rx["rX"], "rY": derotated_or_rx["rY"]}


# ---------------------------------------------------------------------------
# Proposed method candidates (mechanism-distinct). Each is RECEIVER-VISIBLE ONLY.
# ---------------------------------------------------------------------------

# P1 — pilot reliability / covariance-weighted Jones estimate (inverse-variance
# weighting of the LS normal equations by received pilot energy). Mechanism =
# reliability-aware estimation, distinct from fixed EMA (B1) and post-hoc
# regularization (B2). Falsifier: well-conditioned channel + equal pilot energy
# -> weights -> 1 -> degenerates to B0.
def estimate_jones_weighted(pilot_rx, *, block_size, energy_power=1.0):
    rx = np.asarray(pilot_rx["rX"]); ry = np.asarray(pilot_rx["rY"])
    mask = np.asarray(pilot_rx["pilot_mask"])
    ps = np.asarray(pilot_rx["pilot_symbols"])
    estimates = []
    for start in range(0, len(rx), block_size):
        idx = np.flatnonzero(mask[start:start + block_size]) + start
        if len(idx) < 2:
            continue
        P = ps[:, idx].T
        Y = np.stack((rx[idx], ry[idx]), axis=1)
        e = np.abs(rx[idx]) ** 2 + np.abs(ry[idx]) ** 2
        w = e ** energy_power
        w = w / (w.mean() + 1e-12)
        Wd = w[:, None]
        PHWP = P.conj().T @ (Wd * P)
        PHWY = P.conj().T @ (Wd * Y)
        H = np.linalg.lstsq(PHWP, PHWY, rcond=None)[0].T
        estimates.append({"block": start, "matrix": H,
                          "cond": float(np.linalg.cond(H))})
    return estimates


def derotate_weighted(pilot_rx, estimates, *, block_size, ema_alpha=None,
                      data_only=True, whitening_kappa=1e3, use_whitening=False):
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


# P3 — physics-structured joint PDL+PMD tracker: pooled tapped LS estimate
# (handles PMD memory) combined with whitening inverse (handles PDL non-unitary
# conditioning). Mechanism = joint treatment of the two physics (memory from
# pooled taps + conditioning from whitening), distinct from single-tap P1/B2
# (no memory) and from per-block tapped B3_pmd (over-fits, no whitening). This
# is the joint-tracker family the science critic flagged as untested.
def derotate_p3_joint(pilot_rx, *, block_size, n_taps=3, whitening_kappa=1e3,
                      data_only=True):
    """P3 = pooled tapped LS estimate + whitening inverse. Receiver-visible only.
    For M2 (no memory) the pooled taps reduce toward single-tap + whitening; for
    M3/M4 the pooled taps add memory generalization that per-block taps lack."""
    est = pb.estimate_jones_tapped_pooled(pilot_rx, block_size=block_size,
                                          n_taps=n_taps)
    if est is None:
        return None
    # apply the pooled tapped filter, then whitening on the per-block single-tap
    der_taps = pb.derotate_tapped(pilot_rx, est, block_size=block_size,
                                  data_only=data_only)
    # additional whitening pass using the single-tap per-block estimate
    est_single = pb.estimate_jones_single_tap(pilot_rx, block_size=block_size)
    x = np.array(der_taps["rX"], copy=True); y = np.array(der_taps["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    for e in est_single:
        start = e["block"]
        idx = np.arange(start, min(start + block_size, len(x)))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        H = np.asarray(e["matrix"], complex)
        inv = _whitening_inverse(H, kappa_cap=whitening_kappa)
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y}


# P2 — uncertainty-aware temporal tracker: EMA alpha adapts to per-block cond
# (high cond -> MORE smoothing because the per-block estimate is noisier).
# Mechanism = uncertainty-scheduled smoothing, distinct from fixed-alpha EMA (B1)
# and from reliability-weighted estimation (P1, which reweights within a block).
def derotate_cond_adaptive_ema(pilot_rx, estimates, *, block_size,
                               data_only=True, alpha_lo=0.7, alpha_hi=0.95,
                               cond_lo=1.5, cond_hi=4.0):
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
        cond = est.get("cond", 1.0) or 1.0
        # higher cond -> higher alpha (more weight on the smoothed history)
        if cond <= cond_lo:
            a = alpha_lo
        elif cond >= cond_hi:
            a = alpha_hi
        else:
            frac = (cond - cond_lo) / (cond_hi - cond_lo)
            a = alpha_lo + frac * (alpha_hi - alpha_lo)
        ema_h = H if ema_h is None else a * ema_h + (1 - a) * H
        inv = _regularized_inverse(ema_h, 0.0, None)
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y}
