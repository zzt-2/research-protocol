"""Pilot injection + conventional baselines for the Pilot-Jones REPAIR (T004).

THE central pilot fix (V038 defect #3): pilots are injected into the TX frame
BEFORE the channel, then the WHOLE pilot-bearing frame re-runs the atmosphere +
component + SAME-noise chain. Pilot and data therefore traverse the SAME
component operator (memoryless Jones or PMD FIR). T003 instead rebuilt the pilot
RX with a memoryless J@atm and never passed pilots through the PMD FIR.

Conventional baselines:
  B0  no-op / identity diagnostic
  B1  single-tap block pilot LS + frozen EMA09 (historical conventional)
  B2  regularized single-tap / polar inverse (tikhonov)
  B3_pdl  passive-PDL task-matched regularized inverse / whitening
  B3_pmd  TRUE 2x2 tapped pilot-LS, target = KNOWN TX PILOTS (RX window -> TX
          pilot target). This is the V038 defect #4 fix: T003 regressed RX-window
          -> RX-center (near-identity self-prediction).
  B4_fde  conventional frequency-domain/tapped equalizer (if pilot budget allows)
  O       tagged oracle (ceiling/Kill only); implemented in repair_methods.py

Receiver-visible ONLY (pilots + own state). The pilot RX is shared across arms.
"""
from __future__ import annotations
import numpy as np

import semantic_channel as sc


# ---------------------------------------------------------------------------
# Pilot sequences (same T002/T003 dual-QPSK pilots)
# ---------------------------------------------------------------------------

def _pilot_sequences(n):
    base_x = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    base_y = np.array([1 - 1j, -1 + 1j, 1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    return np.resize(base_x, n), np.resize(base_y, n)


def inject_pre_channel_pilots(realization, realization_imp, *,
                              block_size, n_pilots):
    """Inject known pilots into the TX frame BEFORE the channel, then re-run the
    SAME atmosphere + component + SAME post-component-noise chain so that pilot
    and data traverse the IDENTICAL component operator (V038 defect #3 fix).

    The realization already carries clean_original (atmosphere, no pilots),
    n_post (the shared post-component noise), and the component truth. We:
      1. replace the first n_pilots TX symbols of each block with pilots
      2. recompute the atmosphere clean signal on the pilot-bearing TX frame
      3. re-apply the SAME component operator (same J/PMD FIR)
      4. add back the SAME n_post

    Because n_post is independent of the TX payload and the atmosphere is a
    memoryless per-symbol transform (sqrt(h) R(theta)), only the pilot positions'
    clean contribution changes; data positions are unchanged and the noise draw
    is identical. The PMD FIR mixes time within a block, so re-running it on the
    pilot-bearing frame is exactly what makes pilots "go through the channel".
    """
    if n_pilots <= 0 or n_pilots >= block_size or n_pilots / block_size > 0.1:
        raise ValueError("pilot overhead must be positive and <= 10%")
    n = len(realization_imp["rX"])
    px, py = _pilot_sequences(n_pilots)
    sX = np.array(realization["sX"], dtype=complex, copy=True)
    sY = np.array(realization["sY"], dtype=complex, copy=True)
    pilot_mask = np.zeros(n, dtype=bool)
    pilot_symbols = np.zeros((2, n), complex)
    for start in range(0, n, block_size):
        idx = np.arange(start, min(start + n_pilots, n))
        k = len(idx)
        pilot_mask[idx] = True
        pilot_symbols[0, idx] = px[:k]
        pilot_symbols[1, idx] = py[:k]
        sX[idx] = px[:k]
        sY[idx] = py[:k]
    # rebuild atmosphere clean signal on the pilot-bearing TX frame
    theta = np.asarray(realization["theta"])
    h = np.asarray(realization["h"])
    c = np.cos(theta); s = np.sin(theta)
    cleanX = np.sqrt(h) * (c * sX + s * sY)
    cleanY = np.sqrt(h) * (-s * sX + c * sY)
    clean_frame = np.stack((cleanX, cleanY), axis=0)            # (2, N)
    # re-apply the SAME component operator on the pilot-bearing clean frame
    mp = realization_imp["model_params"]
    jones = np.asarray(realization_imp["jones_truth"])
    clean_component = sc.apply_component(
        clean_frame, jones, block_size=block_size,
        dgd_samples=mp["dgd_samples"], pmd_enabled=mp["pmd_enabled"])
    # add the SAME post-component noise
    n_post = np.asarray(realization_imp["n_post"])
    r_out = clean_component + n_post
    # guard mask: exclude the block-boundary transient (PMD FIR circular wrap-
    # around) from the metric denominator. Only PMD models produce a transient;
    # for memoryless models the guard is harmless (no wrap-around). Excluded
    # count is reported (T004 §3.3).
    guard = sc.PMD_GUARD
    guard_mask = np.ones(n, dtype=bool)
    for b in range((n + block_size - 1) // block_size):
        s = b * block_size; e = min(s + block_size, n)
        guard_mask[s:s + guard] = False
        guard_mask[e - guard:e] = False
    eval_mask = (~pilot_mask) & guard_mask
    return {
        "rX": r_out[0], "rY": r_out[1],
        "pilot_mask": pilot_mask, "data_mask": ~pilot_mask,
        "guard_mask": guard_mask, "eval_mask": eval_mask,
        "pilot_symbols": pilot_symbols,
        "overhead": float(pilot_mask.mean()),
        "pilot_count": int(pilot_mask.sum()),
        "data_count": int((~pilot_mask).sum()),
        "guard_excluded_count": int((~guard_mask).sum()),
        "eval_count": int(eval_mask.sum()),
        # truth pilots (atmosphere clean, post-component) for oracle/verification
        "clean_pilot_frame": clean_frame,
        "clean_pilot_component": clean_component,
    }


# ---------------------------------------------------------------------------
# Per-block pilot-LS Jones estimates
# ---------------------------------------------------------------------------

def estimate_jones_single_tap(pilot_rx, *, block_size):
    """Per-block single-tap pilot-LS 2x2 Jones estimate H_b = lstsq(P, Y).T.

    P = (M,2) known pilot symbols; Y = (M,2) received pilots. Receiver-visible.
    Returns list of dicts {block, matrix, cond}.
    """
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
        H = np.linalg.lstsq(P, Y, rcond=None)[0].T
        estimates.append({"block": start, "matrix": H,
                          "cond": float(np.linalg.cond(H))})
    return estimates


def estimate_jones_tapped(pilot_rx, *, block_size, n_taps=3):
    """Per-block 2x2 TAPPED pilot-LS estimate, target = KNOWN TX PILOTS
    (V038 defect #4 fix). T003 regressed RX-window -> RX-center, a near-identity
    self-prediction. Here the regression is:

        known TX pilot p  =  sum_t W_t @ RX(window around p)

    i.e. input = receiver window (2*n_taps), output = known TX pilot symbol (2).
    This is the legal task-matched tapped equalizer training target.

    Windows are taken WRAP-AROUND WITHIN THE BLOCK (cyclic) so every pilot
    contributes (with only n_pilots=6 and n_taps=3 -> 6 unknowns per output, the
    6 pilots must all be usable). The window is cyclically indexed inside the
    block, which is consistent with the FFT-circular PMD convention.
    """
    rx = np.asarray(pilot_rx["rX"]); ry = np.asarray(pilot_rx["rY"])
    mask = np.asarray(pilot_rx["pilot_mask"])
    ps = np.asarray(pilot_rx["pilot_symbols"])
    half = n_taps // 2
    N = len(rx)
    estimates = []
    for start in range(0, N, block_size):
        end = min(start + block_size, N)
        idx = np.flatnonzero(mask[start:end]) + start
        n_unknowns = 2 * n_taps       # per output channel
        if len(idx) < n_unknowns:
            # not enough pilots for a tapped fit in this block -> single-tap
            if len(idx) < 2:
                continue
            P = ps[:, idx].T
            Y = np.stack((rx[idx], ry[idx]), axis=1)
            H = np.linalg.lstsq(P, Y, rcond=None)[0].T
            estimates.append({"block": start, "matrix": H, "filter": None,
                              "n_taps": 1, "cond": float(np.linalg.cond(H))})
            continue
        rows_P = []
        rows_Y = []
        for p in idx:
            # cyclic window within the block (consistent w/ FFT-circular PMD)
            local = (np.arange(p - half, p + half + 1) - start) % (end - start) + start
            Pin = np.concatenate((rx[local], ry[local]))   # (2*n_taps,)
            rows_P.append(Pin)
            rows_Y.append(ps[:, p])                         # known TX pilot (2,)
        Pmat = np.array(rows_P)            # (M, 2*n_taps)
        Ymat = np.array(rows_Y)            # (M, 2)   <-- KNOWN TX pilots
        W = np.linalg.lstsq(Pmat, Ymat, rcond=None)[0]   # (2*n_taps, 2)
        estimates.append({"block": start, "filter": W, "matrix": None,
                          "n_taps": n_taps, "cond": float(np.linalg.cond(Pmat))})
    return estimates


# ---------------------------------------------------------------------------
# Inverse formation + derotation / tapped equalization
# ---------------------------------------------------------------------------

def _regularized_inverse(H, tikhonov, condition_guard):
    if condition_guard is not None and np.linalg.cond(H) > condition_guard:
        return None
    if tikhonov > 0:
        return np.linalg.solve(H.conj().T @ H + tikhonov * np.eye(2),
                               H.conj().T)
    return np.linalg.pinv(H)


def _whitening_inverse(H, kappa_cap=1e3):
    """Task-matched conventional inverse for a non-unitary (passive PDL) Jones:
    polar-decomposition / whitening. H = U S Vh; inverse = V S^-1 U^H, capping
    the smallest singular value at 1/kappa_cap. Conventional, NOT a new method."""
    U, sv, Vh = np.linalg.svd(H)
    sv_inv = np.where(sv > 1.0 / kappa_cap, 1.0 / sv, 0.0)
    return (Vh.conj().T) @ np.diag(sv_inv) @ U.conj().T


def estimate_jones_tapped_pooled(pilot_rx, *, block_size, n_taps=3):
    """Cross-block POOLED tapped LS (RX window -> known TX pilot). Aggregates ALL
    pilot equations across the whole frame into one tapped filter, giving many
    more equations than unknowns (generalizes, unlike the per-block n_taps=3
    which exactly interpolates 6 pilots). This is the strongest legal tapped
    conventional baseline under the 6-pilot/64 budget (addresses the science-
    critic fairness point that per-block tapped over-fits). Returns a single
    global filter applied per-block-window."""
    rx = np.asarray(pilot_rx["rX"]); ry = np.asarray(pilot_rx["rY"])
    mask = np.asarray(pilot_rx["pilot_mask"])
    ps = np.asarray(pilot_rx["pilot_symbols"])
    half = n_taps // 2
    N = len(rx)
    n_blocks = (N + block_size - 1) // block_size
    rows_P = []
    rows_Y = []
    for b in range(n_blocks):
        start = b * block_size
        end = min(start + block_size, N)
        idx = np.flatnonzero(mask[start:end]) + start
        for p in idx:
            local = (np.arange(p - half, p + half + 1) - start) % (end - start) + start
            Pin = np.concatenate((rx[local], ry[local]))
            rows_P.append(Pin)
            rows_Y.append(ps[:, p])
    if len(rows_P) < 2 * n_taps:
        return None
    Pmat = np.array(rows_P)
    Ymat = np.array(rows_Y)
    W = np.linalg.lstsq(Pmat, Ymat, rcond=None)[0]   # (2*n_taps, 2) global filter
    # wrap into a per-block estimate list (same filter applied everywhere)
    estimates = []
    for b in range(n_blocks):
        start = b * block_size
        estimates.append({"block": start, "filter": W, "matrix": None,
                          "n_taps": n_taps,
                          "cond": float(np.linalg.cond(Pmat))})
    return estimates


def derotate_single_tap(pilot_rx, estimates, *, block_size, mode,
                        data_only=True, ema_alpha=None, tikhonov=0.0,
                        condition_guard=None, whitening_kappa=1e3):
    """Apply a single-tap estimated Jones inverse to the data symbols.

    mode in {'pinv','ema','tikhonov','guard','whitening'}.
    """
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    ema_h = None
    skipped = 0
    for est in estimates:
        start = est["block"]
        idx = np.arange(start, min(start + block_size, len(x)))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        H = np.asarray(est["matrix"], complex)
        if mode == "ema":
            ema_h = H if ema_h is None else ema_alpha * ema_h + (1 - ema_alpha) * H
            inv = _regularized_inverse(ema_h, 0.0, None)
        elif mode == "tikhonov":
            inv = _regularized_inverse(H, tikhonov, None)
        elif mode == "guard":
            inv = _regularized_inverse(H, 0.0, condition_guard)
        elif mode == "whitening":
            inv = _whitening_inverse(H, kappa_cap=whitening_kappa)
        else:  # pinv
            inv = _regularized_inverse(H, 0.0, None)
        if inv is None:
            skipped += 1
            continue
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y, "skipped_blocks": skipped}


def derotate_tapped(pilot_rx, estimates, *, block_size, data_only=True):
    """Apply the tapped RX->TX equalizer (B3_pmd) to data positions.

    For each block with a tapped filter, slide the window over the WHOLE block,
    apply W (2*n_taps,2), and write data positions back.
    """
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    for est in estimates:
        if est.get("filter") is None:
            # single-tap fallback
            start = est["block"]
            idx = np.arange(start, min(start + block_size, len(x)))
            if data_only:
                idx = idx[dm[idx]]
            if not len(idx):
                continue
            inv = _regularized_inverse(np.asarray(est["matrix"], complex), 0.0, None)
            corr = inv @ np.stack((x[idx], y[idx]), axis=0)
            x[idx], y[idx] = corr[0], corr[1]
            continue
        W = est["filter"]                       # (2*n_taps, 2)
        nt = est["n_taps"]; half = nt // 2
        start = est["block"]
        bs = min(start + block_size, len(x))
        win_x = x[start:bs]; win_y = y[start:bs]
        L = len(win_x)
        out_x = np.zeros(L, complex); out_y = np.zeros(L, complex)
        for i in range(L):
            # cyclic window within the block (matches training convention)
            local = (np.arange(i - half, i + half + 1)) % L
            seg = np.concatenate((win_x[local], win_y[local]))
            out = seg @ W
            out_x[i] = out[0]; out_y[i] = out[1]
        idx = np.arange(start, bs)
        if data_only:
            m = dm[start:bs]
            idx = idx[m]; out_x = out_x[m]; out_y = out_y[m]
        x[idx] = out_x; y[idx] = out_y
    return {"rX": x, "rY": y}


# ---------------------------------------------------------------------------
# FDE tapped baseline (B4) — conventional frequency-domain equalizer using the
# tapped pilot-LS estimate as the per-block channel estimate.
# ---------------------------------------------------------------------------

def derotate_fde(pilot_rx, estimates, *, block_size, data_only=True,
                 gamma_bar=50.0):
    """Conventional per-block FDE MMSE using the single-tap pilot-LS estimate as
    the memoryless channel (B4_fde). For a memoryless Jones (M2) this equals
    whitening; for M3 it is a coarse FDE that does not use PSP delays (a
    conventional deployable that uses only pilot-LS)."""
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    nv = 1.0 / (2 * gamma_bar)
    n = len(x)
    for est in estimates:
        if est.get("matrix") is None:
            continue
        start = est["block"]
        en = min(start + block_size, n)
        L = en - start
        if L <= 0:
            continue
        H = np.asarray(est["matrix"], complex)
        nfft = max(8, 1 << int(np.ceil(np.log2(L))))
        pad = np.zeros((2, nfft), dtype=complex)
        pad[:, :L] = np.stack((x[start:en], y[start:en]), axis=0)
        Rf = np.fft.fft(pad, axis=1)
        Xf = np.linalg.solve(H.conj().T @ H + nv * np.eye(2),
                             H.conj().T @ Rf[:, :, None].squeeze(-1).reshape(2, nfft)
                             ) if False else None
        # per-frequency solve (avoid the broken one-liner above)
        Xf = np.zeros((2, nfft), dtype=complex)
        for fi in range(nfft):
            Xf[:, fi] = np.linalg.solve(H.conj().T @ H + nv * np.eye(2),
                                        H.conj().T @ Rf[:, fi])
        xhat = np.fft.ifft(Xf, axis=1)[:, :L]
        idx = np.arange(start, en)
        if data_only:
            m = dm[start:en]
            idx = idx[m]; xhat = xhat[:, m]
        x[idx] = xhat[0]; y[idx] = xhat[1]
    return {"rX": x, "rY": y}
