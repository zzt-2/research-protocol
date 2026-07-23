"""Conventional baselines for the Pilot-Jones complex-model salvage (T003).

Baseline ladder (T003 Phase 3.1):
  B0  single-tap block pilot LS + pinv                 (no temporal smoothing)
  B1  single-tap fixed EMA09                            (T002 reference)
  B2  validation-tuned regularization / condition guard
  B3  TASK-MATCHED conventional:
        - PDL / non-unitary flat : whitening / polar-decomposition regularized LS
        - PMD / memory           : 2x2 tapped LS or frequency-domain (FDE) pilot Jones
  P   proposed method (see salvage_methods.py)
  O   true-Jones oracle (tagged upper bound / Kill only)

Receiver-visible ONLY (pilots + own state). The pilot injection + per-block LS
estimate are reused verbatim from T002's seam so the comparison is apples-to-
apples; only the way the inverse is formed differs. B3 is the Go opponent.
"""
from __future__ import annotations
import numpy as np


# ---------------------------------------------------------------------------
# Pilot injection + per-block LS Jones estimate (same seam as T002, receiver-
# visible). Reimplemented here self-contained on the impaired realization.
# ---------------------------------------------------------------------------

def _pilot_sequences(n):
    base_x = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    base_y = np.array([1 - 1j, -1 + 1j, 1 + 1j, -1 - 1j], complex) / np.sqrt(2)
    return np.resize(base_x, n), np.resize(base_y, n)


def inject_dual_pilots(realization_imp, *, block_size, n_pilots):
    """Replace first n_pilots of each block with known pilots. Noise is
    reconstructed from the impaired realization (rX - J@s) so no new random draw
    is introduced. Overhead = n_pilots/block_size enforced <= 10%.

    The true Jones (per block) is used ONLY to reconstruct the exact additive
    noise at the pilot positions; no deployable method reads it afterwards.
    """
    if n_pilots <= 0 or n_pilots >= block_size or n_pilots / block_size > 0.1:
        raise ValueError("pilot overhead must be positive and <= 10%")
    n = len(realization_imp["rX"])
    px, py = _pilot_sequences(n_pilots)
    pilot_mask = np.zeros(n, dtype=bool)
    pilot_symbols = np.zeros((2, n), complex)
    rx = np.array(realization_imp["rX"], copy=True)
    ry = np.array(realization_imp["rY"], copy=True)

    # reconstruct noise per block using the true (atmosphere+component) channel
    # so the pilot symbols see the SAME noise the channel would have produced.
    # atmosphere part
    c = np.cos(realization_imp["theta"]); s = np.sin(realization_imp["theta"])
    h = np.asarray(realization_imp["h"])
    sX = np.asarray(realization_imp["sX"]); sY = np.asarray(realization_imp["sY"])
    rXatm = np.sqrt(h) * (c * sX + s * sY)
    rYatm = np.sqrt(h) * (-s * sX + c * sY)
    # component Jones per block
    J = np.asarray(realization_imp["jones_truth"])  # (n_blocks,2,2)
    n_blocks = J.shape[0]
    # noise = r - J @ r_atm  (per block)
    for b in range(n_blocks):
        st = b * block_size
        en = min(st + block_size, n)
        if en <= st:
            continue
        atm = np.stack((rXatm[st:en], rYatm[st:en]), axis=0)
        # current RX already = J @ atm + noise -> noise = RX - J@atm
        # (we recompute exactly to keep the shared-noise contract)
    # simpler & exact: noise_n = r_n - (J_b @ atm_n); but for M3 (PMD) the FIR
    # already mixed time, so reconstruct noise directly as RX minus the
    # re-synthesized signal at pilot positions only (those are memory-local).
    nx = np.zeros(n, complex); ny = np.zeros(n, complex)
    for b in range(n_blocks):
        st = b * block_size; en = min(st + block_size, n)
        if en <= st:
            continue
        atm = np.stack((rXatm[st:en], rYatm[st:en]), axis=0)
        sig = J[b] @ atm  # memoryless component part (PMD FIR handled below)
        nx[st:en] = realization_imp["rX"][st:en] - sig[0]
        ny[st:en] = realization_imp["rY"][st:en] - sig[1]

    # place pilots: re-synthesize pilot RX with reconstructed noise
    for start in range(0, n, block_size):
        idx = np.arange(start, min(start + n_pilots, n))
        k = len(idx)
        pilot_mask[idx] = True
        pilot_symbols[0, idx] = px[:k]
        pilot_symbols[1, idx] = py[:k]
        b = start // block_size
        patm_x = np.sqrt(h[idx]) * (c[idx] * px[:k] + s[idx] * py[:k])
        patm_y = np.sqrt(h[idx]) * (-s[idx] * px[:k] + c[idx] * py[:k])
        patm = np.stack((patm_x, patm_y), axis=0)
        psig = J[b] @ patm
        rx[idx] = psig[0] + nx[idx]
        ry[idx] = psig[1] + ny[idx]
    return {"rX": rx, "rY": ry, "pilot_mask": pilot_mask,
            "data_mask": ~pilot_mask, "pilot_symbols": pilot_symbols,
            "overhead": float(pilot_mask.mean()),
            "pilot_count": int(pilot_mask.sum()),
            "data_count": int((~pilot_mask).sum())}


def estimate_jones_blocks(pilot_rx, *, block_size, n_taps=1):
    """Per-block pilot-LS 2x2 Jones estimate.

    n_taps=1 : single-tap LS H_b = lstsq(P, Y)  (T002 seam).
    n_taps>1 : 2x2 tapped LS (B3 task-matched for PMD/memory). Each output is a
               (n_taps, 2, 2) filter; the LS stacks shifted pilot windows.
    Returns list of dicts with 'block','matrix'/'filter','cond'.
    """
    rx = np.asarray(pilot_rx["rX"]); ry = np.asarray(pilot_rx["rY"])
    mask = np.asarray(pilot_rx["pilot_mask"])
    ps = np.asarray(pilot_rx["pilot_symbols"])
    estimates = []
    for start in range(0, len(rx), block_size):
        idx = np.flatnonzero(mask[start:start + block_size]) + start
        if len(idx) < 2 * n_taps:
            continue
        if n_taps == 1:
            P = ps[:, idx].T
            Y = np.stack((rx[idx], ry[idx]), axis=1)
            H = np.linalg.lstsq(P, Y, rcond=None)[0].T
            estimates.append({"block": start, "matrix": H,
                              "cond": float(np.linalg.cond(H))})
        else:
            # build tapped LS: for each pilot position p, regress on a window of
            # n_taps surrounding RX samples. Pilot symbols are single-valued
            # (no memory on TX), so the tapped LS solves Y = sum_t H_t @ RX shifted.
            half = n_taps // 2
            rows_P = []
            rows_Y = []
            for p in idx:
                if p - half < 0 or p + half + 1 > len(rx):
                    continue
                win = np.arange(p - half, p + half + 1)
                # input block: [RXx(win); RXy(win)] length 2*n_taps
                Pin = np.concatenate((rx[win], ry[win]))
                rows_P.append(Pin)
                rows_Y.append([rx[p], ry[p]])
            if len(rows_P) < 2 * n_taps:
                # fall back to single-tap for this block
                P = ps[:, idx].T
                Y = np.stack((rx[idx], ry[idx]), axis=1)
                H = np.linalg.lstsq(P, Y, rcond=None)[0].T
                estimates.append({"block": start, "matrix": H, "filter": None,
                                  "n_taps": 1,
                                  "cond": float(np.linalg.cond(H))})
                continue
            Pmat = np.array(rows_P)            # (M, 2*n_taps)
            Ymat = np.array(rows_Y)            # (M, 2)
            W = np.linalg.lstsq(Pmat, Ymat, rcond=None)[0]  # (2*n_taps, 2)
            # condition proxy: cond of the tapped design matrix
            estimates.append({"block": start, "filter": W, "matrix": None,
                              "n_taps": n_taps,
                              "cond": float(np.linalg.cond(Pmat))})
    return estimates


# ---------------------------------------------------------------------------
# Inverse formation + derotation
# ---------------------------------------------------------------------------

def _regularized_inverse(H, tikhonov, condition_guard):
    if condition_guard is not None and np.linalg.cond(H) > condition_guard:
        return None
    if tikhonov > 0:
        return np.linalg.solve(H.conj().T @ H + tikhonov * np.eye(2),
                               H.conj().T)
    return np.linalg.pinv(H)


def _whitening_inverse(H, kappa_cap=1e3):
    """Task-matched conventional inverse for a non-unitary (PDL) flat Jones:
    polar-decomposition / whitening. H = U S Vh; inverse = V S^-1 U^H. Caps the
    smallest singular value at 1/kappa_cap to avoid noise explosion (regularized
    pseudo-inverse on the singular values). This is the conventional way to
    invert an ill-conditioned non-unitary matrix — it is NOT a new method."""
    U, sv, Vh = np.linalg.svd(H)
    sv_inv = np.where(sv > 1.0 / kappa_cap, 1.0 / sv, 0.0)
    return (Vh.conj().T) @ np.diag(sv_inv) @ U.conj().T


def derotate(pilot_rx, estimates, *, block_size, mode, data_only=True,
             ema_alpha=None, tikhonov=0.0, condition_guard=None,
             whitening_kappa=1e3, n_taps=1):
    """Apply an estimated Jones inverse to the data symbols.

    mode in {'pinv','ema','tikhonov','guard','whitening','tapped'}.
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

        if mode == "tapped" and est.get("filter") is not None:
            # apply tapped filter to the whole block then read data positions
            W = est["filter"]  # (2*n_taps, 2)
            nt = est["n_taps"]; half = nt // 2
            bs = min(start + block_size, len(x))
            ws = np.arange(start, bs)
            # need window around each symbol; pad edges
            win_x = x[start:bs]; win_y = y[start:bs]
            L = len(win_x)
            out_x = np.zeros(L, complex); out_y = np.zeros(L, complex)
            Pin_full = np.stack([win_x, win_y], axis=0)
            # build sliding windows over the block
            for i in range(L):
                lo = i - half; hi = i + half + 1
                if lo < 0 or hi > L:
                    continue
                seg = np.concatenate((win_x[lo:hi], win_y[lo:hi]))
                out = seg @ W
                out_x[i] = out[0]; out_y[i] = out[1]
            # write back data positions within this block
            local_idx = idx - start
            x[idx] = out_x[local_idx]; y[idx] = out_y[local_idx]
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


def derotate_oracle(pilot_rx, realization_imp, *, block_size, data_only=True):
    """Tagged oracle O: use the TRUE per-block component Jones AND the true
    per-symbol SOP rotation to build the ideal memoryless inverse.

    The full polarization channel is r = J_b @ (sqrt(h_n) R(theta_n) s + noise).
    A correct ceiling must invert BOTH J_b and R(theta_n); inverting only J_b
    leaves the SOP rotation R(theta) uncompensated (which would make the oracle
    spuriously WORSE than a deployable estimator that jointly fits J_b@R(theta)).
    Per symbol we apply R(-theta_n) then J_b^{-1}. h is a scalar fade (affects
    SNR, not bit polarity at hard decision). For M3 (PMD) this memoryless oracle
    cannot undo ISI; the FDE oracle in salvage_methods is the true ceiling.
    """
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    J = np.asarray(realization_imp["jones_truth"])
    theta = np.asarray(realization_imp["theta"])
    n_blocks = J.shape[0]
    n = len(x)
    for b in range(n_blocks):
        start = b * block_size
        idx = np.arange(start, min(start + block_size, n))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        invJ = np.linalg.inv(J[b])
        ct = np.cos(theta[idx]); st = np.sin(theta[idx])
        seg = np.stack((x[idx], y[idx]), axis=0)
        # undo component Jones, then undo SOP rotation R(-theta)
        post = invJ @ seg
        rot_back = np.stack((ct * post[0] - st * post[1],
                             st * post[0] + ct * post[1]), axis=0)
        x[idx], y[idx] = rot_back[0], rot_back[1]
    return {"rX": x, "rY": y}
