"""Pilot injection, legal conventional baselines and truth-assisted reference
for the Pilot-Jones component TEMPORAL SEMANTICS adjudication (T005).

Pilot injection INHERITS the T004 defect #3 fix: pilots are injected into the
TX frame BEFORE the channel, then the whole pilot-bearing frame re-runs the
atmosphere + FIXED component + SAME-noise chain so pilot and data traverse the
IDENTICAL fixed component operator.

Legal conventional baselines (deployment-ready, receiver-visible only):
  B1   single-tap block pilot LS + frozen EMA09 (historical conventional).
  B2   single-tap Tikhonov; lambda frozen on VALIDATION only.
  B_static (optional) pooled/cross-block tapped estimate; only if task-matched.

Truth-assisted reference O (ceiling / Kill only, NEVER a Go opponent, FR-25):
  M0/M2  per-symbol TRUE full channel; >=16 joint dual-QPSK symbol-pair exact ML
         so a colored-noise inverse is not passed off as an absolute ceiling.
  M3     exact frequency-domain inverse of the TRUE fixed PSP + verified DGD;
         state the unitary-PMD noise-preservation property.
"""
from __future__ import annotations
import numpy as np

import temporal_channel as tc


# ---------------------------------------------------------------------------
# Pilot sequences (same dual-QPSK pilots as T002/T003/T004)
# ---------------------------------------------------------------------------

def _pilot_sequences(n):
    base_x = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    base_y = np.array([1 - 1j, -1 + 1j, 1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    return np.resize(base_x, n), np.resize(base_y, n)


def inject_pre_channel_pilots(realization, realization_imp, *, block_size,
                              n_pilots):
    """Inject known pilots into the TX frame BEFORE the channel and re-run the
    SAME atmosphere + FIXED component + SAME post-component-noise chain so pilot
    and data traverse the IDENTICAL fixed component operator (T004 defect #3 fix,
    inherited). Because the component is FIXED, this is exact: only the pilot
    positions' clean contribution changes; data positions are unchanged and the
    noise draw is identical.
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
    theta = np.asarray(realization["theta"])
    h = np.asarray(realization["h"])
    c = np.cos(theta); s = np.sin(theta)
    cleanX = np.sqrt(h) * (c * sX + s * sY)
    cleanY = np.sqrt(h) * (-s * sX + c * sY)
    clean_frame = np.stack((cleanX, cleanY), axis=0)
    mp = realization_imp["model_params"]
    jones_fixed = np.asarray(realization_imp["jones_truth_fixed"])
    psp = realization_imp["psp_truth_fixed"]
    clean_component = tc.apply_component_fixed(
        clean_frame, jones_fixed, block_size=block_size,
        dgd_samples=mp["dgd_samples"], psp=psp)
    n_post = np.asarray(realization_imp["n_post"])
    r_out = clean_component + n_post
    guard = tc.PMD_GUARD
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
        "clean_pilot_frame": clean_frame,
        "clean_pilot_component": clean_component,
    }


# ---------------------------------------------------------------------------
# Per-block single-tap pilot-LS Jones estimate (receiver-visible)
# ---------------------------------------------------------------------------

def estimate_jones_single_tap(pilot_rx, *, block_size):
    """Per-block single-tap pilot-LS 2x2 Jones estimate H_b = lstsq(P, Y).T."""
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


def _regularized_inverse(H, tikhonov):
    if tikhonov > 0:
        return np.linalg.solve(H.conj().T @ H + tikhonov * np.eye(2),
                               H.conj().T)
    return np.linalg.pinv(H)


# ---------------------------------------------------------------------------
# Single-tap derotation (B1 EMA09, B2 Tikhonov)
# ---------------------------------------------------------------------------

def derotate_single_tap(pilot_rx, estimates, *, block_size, mode,
                        data_only=True, ema_alpha=None, tikhonov=0.0):
    """mode in {'pinv','ema','tikhonov'}."""
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
            inv = _regularized_inverse(ema_h, 0.0)
        elif mode == "tikhonov":
            inv = _regularized_inverse(H, tikhonov)
        else:  # pinv
            inv = _regularized_inverse(H, 0.0)
        if inv is None:
            skipped += 1
            continue
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y, "skipped_blocks": skipped}


# ---------------------------------------------------------------------------
# OPTIONAL pooled tapped estimate (B_static) — only used if task-matched.
# n_pilots in {4,6}: pooled aggregates across the whole frame so the equation
# count >> unknown count (generalizes; NOT the per-block over-fit of T004).
# ---------------------------------------------------------------------------

def estimate_jones_tapped_pooled(pilot_rx, *, block_size, n_taps=3):
    """Cross-block POOLED tapped LS (RX window -> known TX pilot). One global
    filter trained on every pilot in the frame. Receiver-visible only."""
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
        L = end - start
        for p in idx:
            local = (np.arange(p - half, p + half + 1) - start) % L + start
            Pin = np.concatenate((rx[local], ry[local]))
            rows_P.append(Pin)
            rows_Y.append(ps[:, p])
    if len(rows_P) < 2 * n_taps:
        return None
    Pmat = np.array(rows_P)
    Ymat = np.array(rows_Y)
    W = np.linalg.lstsq(Pmat, Ymat, rcond=None)[0]
    estimates = []
    for b in range(n_blocks):
        start = b * block_size
        estimates.append({"block": start, "filter": W, "matrix": None,
                          "n_taps": n_taps,
                          "cond": float(np.linalg.cond(Pmat))})
    return estimates


def derotate_tapped(pilot_rx, estimates, *, block_size, data_only=True):
    """Apply a tapped RX->TX equalizer to data positions."""
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    for est in estimates:
        if est.get("filter") is None:
            start = est["block"]
            idx = np.arange(start, min(start + block_size, len(x)))
            if data_only:
                idx = idx[dm[idx]]
            if not len(idx):
                continue
            inv = _regularized_inverse(np.asarray(est["matrix"], complex), 0.0)
            corr = inv @ np.stack((x[idx], y[idx]), axis=0)
            x[idx], y[idx] = corr[0], corr[1]
            continue
        W = est["filter"]
        nt = est["n_taps"]; half = nt // 2
        start = est["block"]
        bs = min(start + block_size, len(x))
        win_x = x[start:bs]; win_y = y[start:bs]
        L = len(win_x)
        out_x = np.zeros(L, complex); out_y = np.zeros(L, complex)
        for i in range(L):
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
# Truth-assisted reference O (ceiling / Kill ONLY, never a Go opponent; FR-25)
# ---------------------------------------------------------------------------

QPSK_GRID = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j], complex) / np.sqrt(2)


def _sym_pairs(n_pairs=16):
    """Enumerate >=16 ordered (sx, sy) dual-QPSK symbol pairs (4x4=16)."""
    pairs = []
    for a in QPSK_GRID:
        for b in QPSK_GRID:
            pairs.append((a, b))
    return pairs


def reference_m0_m2(realization_imp, pilot_rx, *, block_size, gamma_bar,
                    data_only=True, n_pairs=16):
    """Truth-assisted reference for M0/M2: per-symbol TRUE full channel exact ML.

    Forward channel (matches apply_component_fixed / build_impaired_realization):
        clean_atm_n   = sqrt(h_n) * R(theta_n) @ s_n           (rotation first)
        r_n           = J_fixed @ clean_atm_n + n_post_n       (component second)
    i.e. the full per-symbol channel is C_n = J_fixed @ diag(sqrt(h_n)) @ R(theta_n).
    The reference uses the TRUE h_n, theta_n and TRUE fixed J_fixed to build C_n
    exactly, then performs a joint ML search over >=16 ordered dual-QPSK symbol
    pairs (choose the pair minimizing |r_n - C_n @ s_pair|^2). This is a genuine
    ceiling on what a deployable single-tap conventional estimator could approach;
    it is NOT a method Go opponent. Colored-noise inverse shortcuts are NOT used.
    """
    n = len(realization_imp["rX"])
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    theta = np.asarray(realization_imp["theta"])
    h = np.asarray(realization_imp["h"])
    J = np.asarray(realization_imp["jones_truth_fixed"])
    dm = pilot_rx["data_mask"] if data_only else np.ones(n, dtype=bool)
    c = np.cos(theta); s = np.sin(theta)
    sh = np.sqrt(h)
    pairs = _sym_pairs(n_pairs)
    P = np.array([p for p in pairs])              # (M,2)
    # per-symbol channel C_n = J @ diag(sqrt(h_n)) @ R(theta_n)
    # first apply R(theta_n) to each candidate pair, then scale by sqrt(h_n),
    # then apply J.
    j00, j01 = J[0]; j10, j11 = J[1]
    out_x = np.zeros(n, complex); out_y = np.zeros(n, complex)
    for k in range(n):
        if not dm[k]:
            continue
        rxk = x[k]; ryk = y[k]
        # R(theta_k) @ [sx,sy]: atm_x = c*sx+s*sy, atm_y = -s*sx+c*sy
        atm_x = c[k] * P[:, 0] + s[k] * P[:, 1]
        atm_y = -s[k] * P[:, 0] + c[k] * P[:, 1]
        # scale by sqrt(h_k), then apply J
        cx = j00 * (sh[k] * atm_x) + j01 * (sh[k] * atm_y)
        cy = j10 * (sh[k] * atm_x) + j11 * (sh[k] * atm_y)
        err = np.abs(rxk - cx) ** 2 + np.abs(ryk - cy) ** 2
        best = int(np.argmin(err))
        out_x[k] = P[best, 0]; out_y[k] = P[best, 1]
    return {"rX": out_x, "rY": out_y}


def reference_m3(realization_imp, pilot_rx, *, block_size, gamma_bar,
                 data_only=True):
    """Truth-assisted reference for M3: exact frequency-domain inverse of the
    TRUE fixed PSP + verified DGD, then undo R(-theta) and /sqrt(h).

    The PSP-basis PMD operator J(f) = U diag(exp(-j2pi f tau)) Vh is UNITARY
    (sigma=[1,1]) -> noise-preserving up to the MMSE regularization. Uses the
    SAME FFT-circular convention as the forward apply_component_fixed, so forward
    and reference are exact inverses modulo the block-boundary transient
    (PMD_GUARD, excluded from the metric denominator).
    """
    n = len(realization_imp["rX"])
    x = np.array(realization_imp["rX"], copy=True); y = np.array(realization_imp["rY"], copy=True)
    theta = np.asarray(realization_imp["theta"])
    h = np.asarray(realization_imp["h"])
    psp = realization_imp["psp_truth_fixed"]
    mp = realization_imp["model_params"]
    dgd_samples = mp["dgd_samples"]
    dm = pilot_rx["data_mask"] if data_only else np.ones(n, dtype=bool)
    nv = 1.0 / (2 * gamma_bar)
    for b in range((n + block_size - 1) // block_size):
        start = b * block_size
        en = min(start + block_size, n)
        L = en - start
        if L <= 0:
            continue
        seg = np.stack((x[start:en], y[start:en]), axis=0)
        idx = np.arange(start, en)
        U, Vh = psp
        Hf = tc._pmd_freq_operator(U, Vh, dgd_samples, L)
        Rf = np.fft.fft(seg, axis=1)
        Xf = np.zeros((2, L), dtype=complex)
        for fi in range(L):
            Xf[:, fi] = np.linalg.solve(Hf[fi].conj().T @ Hf[fi] + nv * np.eye(2),
                                        Hf[fi].conj().T @ Rf[:, fi])
        post = np.fft.ifft(Xf, axis=1)
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
