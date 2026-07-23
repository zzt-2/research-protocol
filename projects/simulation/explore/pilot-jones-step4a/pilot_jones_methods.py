"""Pilot-Jones methods for GW Step 4a big package.

Baseline ladder + candidate methods, all receiver-visible (no true h / theta /
Jones / TX data used except the explicitly-tagged oracle). The channel's
2x2 polarization mixing is a REAL rotation theta (see source-closure.yaml
known_simplification); the pilot-LS seam estimates a 2x2 COMPLEX matrix and
recovers a near-real rotation.

Information boundary (enforced and tested):
- pilot injection uses the canonical realization ONLY to reconstruct the
  additive noise (so no new random draw is introduced) and to place known
  pilot symbols; the true h / theta / Jones / TX data are NOT used by any
  deployable method.
- The deployable estimators read: pilot RX (rX,rY), pilot symbols, pilot mask,
  and (for the temporal trackers) their own previously-estimated matrices /
  receiver-visible condition / innovation proxies. They never read sX/sY/h/theta.
- oracle (tagged) reads the true theta to compute the ideal inverse.
"""
from __future__ import annotations
import numpy as np

# ---------------------------------------------------------------------------
# Standard complex Godard-z 2x2 CMA core (matches source batch1_fade_methods,
# gradient includes the output factor z: w += mu*(R2-|z|^2)*z*conj(r)).
# ---------------------------------------------------------------------------

def _cma_weights_norm(weights: dict) -> float:
    return float(np.sqrt(sum(np.sum(np.abs(v) ** 2) for v in weights.values())))


def run_standard_cma(rX, rY, *, mu, taps, r2, block_size,
                     eval_start, eval_end):
    """Standard complex Godard-z 2x2 butterfly CMA, online block updates.

    Returns zX/zY on the eval window and a valid mask. Initialised on the
    diagonal (wxx=wyy=1 at center tap, off-diagonal 0). This is the BLIND
    baseline; it is identical to source `run_method(..., 'baseline')`.
    """
    from numpy.lib.stride_tricks import sliding_window_view
    rX = np.asarray(rX); rY = np.asarray(rY)
    x_win = sliding_window_view(rX, taps)
    y_win = sliding_window_view(rY, taps)
    half = taps // 2
    weights = {n: np.zeros(taps, dtype=complex) for n in ("wxx","wxy","wyx","wyy")}
    weights["wxx"][half] = weights["wyy"][half] = 1.0
    initial_norm = _cma_weights_norm(weights)
    n_blocks = max(0, (len(rX) - taps + 1) // block_size)
    out_x = np.zeros(eval_end - eval_start, dtype=complex)
    out_y = np.zeros_like(out_x)
    valid = np.zeros(len(out_x), dtype=bool)
    diverged = False
    div_sym = None
    for block in range(n_blocks):
        s = block * block_size
        e = s + block_size
        os = s + half
        x, y = x_win[s:e], y_win[s:e]
        z_x = x @ weights["wxx"] + y @ weights["wxy"]
        z_y = x @ weights["wyx"] + y @ weights["wyy"]
        left, right = max(os, eval_start), min(os + block_size, eval_end)
        if left < right:
            src = slice(left - os, right - os)
            dst = slice(left - eval_start, right - eval_start)
            out_x[dst], out_y[dst] = z_x[src], z_y[src]
            valid[dst] = True
        ex = r2 - np.abs(z_x) ** 2
        ey = r2 - np.abs(z_y) ** 2
        weights["wxx"] += mu * np.mean((ex * z_x)[:, None] * np.conj(x), axis=0)
        weights["wxy"] += mu * np.mean((ex * z_x)[:, None] * np.conj(y), axis=0)
        weights["wyx"] += mu * np.mean((ey * z_y)[:, None] * np.conj(x), axis=0)
        weights["wyy"] += mu * np.mean((ey * z_y)[:, None] * np.conj(y), axis=0)
        nrm = _cma_weights_norm(weights)
        if (not np.isfinite(nrm)) or nrm > 10 * initial_norm:
            diverged = True
            div_sym = int(os + block_size)
            break
    return {"zX": out_x, "zY": out_y, "valid_mask": valid,
            "diverged": diverged, "divergence_symbol": div_sym}


# ---------------------------------------------------------------------------
# Pilot injection + per-block pilot-LS Jones estimate (receiver-visible only)
# ---------------------------------------------------------------------------

def _pilot_sequences(n):
    base_x = np.array([1+1j, 1-1j, -1+1j, -1-1j], complex) / np.sqrt(2)
    base_y = np.array([1-1j, -1+1j, 1+1j, -1-1j], complex) / np.sqrt(2)
    return np.resize(base_x, n), np.resize(base_y, n)


def inject_dual_pilots(realization, *, block_size, n_pilots):
    """Replace first n_pilots symbols of each block with known pilots.

    Noise is reconstructed from the canonical realization (noise = rX - signal),
    so no new random draw is introduced. Overhead = n_pilots/block_size,
    enforced <= 10%. The true h/theta are used ONLY to reconstruct the exact
    additive noise that the channel would have produced at the pilot positions;
    no deployable method reads h/theta afterwards.
    """
    if n_pilots <= 0 or n_pilots >= block_size or n_pilots / block_size > 0.1:
        raise ValueError("pilot overhead must be positive and <= 10%")
    n = len(realization["rX"])
    px, py = _pilot_sequences(n_pilots)
    pilot_mask = np.zeros(n, dtype=bool)
    pilot_symbols = np.zeros((2, n), complex)
    rx = np.array(realization["rX"], copy=True)
    ry = np.array(realization["rY"], copy=True)
    c = np.cos(realization["theta"]); s = np.sin(realization["theta"])
    h = np.asarray(realization["h"])
    nx = realization["rX"] - np.sqrt(h) * (c * realization["sX"] + s * realization["sY"])
    ny = realization["rY"] - np.sqrt(h) * (-s * realization["sX"] + c * realization["sY"])
    for start in range(0, n, block_size):
        idx = np.arange(start, min(start + n_pilots, n))
        k = len(idx)
        pilot_mask[idx] = True
        pilot_symbols[0, idx] = px[:k]
        pilot_symbols[1, idx] = py[:k]
        rx[idx] = np.sqrt(h[idx]) * (c[idx] * px[:k] + s[idx] * py[:k]) + nx[idx]
        ry[idx] = np.sqrt(h[idx]) * (-s[idx] * px[:k] + c[idx] * py[:k]) + ny[idx]
    return {"rX": rx, "rY": ry, "pilot_mask": pilot_mask,
            "data_mask": ~pilot_mask, "pilot_symbols": pilot_symbols,
            "overhead": float(pilot_mask.mean()),
            "pilot_count": int(pilot_mask.sum()),
            "data_count": int((~pilot_mask).sum())}


def estimate_jones_blocks(pilot_rx, *, block_size):
    """Per-block pilot-LS 2x2 Jones estimate. H = lstsq(P, Y). Receiver-visible."""
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


def _regularized_inverse(H, tikhonov, condition_guard):
    if condition_guard is not None and np.linalg.cond(H) > condition_guard:
        return None
    if tikhonov > 0:
        return np.linalg.solve(H.conj().T @ H + tikhonov * np.eye(2), H.conj().T)
    return np.linalg.pinv(H)


# ---------------------------------------------------------------------------
# Derotation arms (B0 / B1 / B2 family) + proposed P + oracle
# ---------------------------------------------------------------------------

def derotate(pilot_rx, estimates, *, block_size, tikhonov=0.0,
             condition_guard=None, ema_alpha=None, data_only=True):
    """Apply estimated Jones inverse to data symbols.

    - ema_alpha (B1 EMA): if not None, smooth the matrix estimate
      H_smooth = alpha*H_prev + (1-alpha)*H (alpha=0.9 == EMA09).
    - tikhonov>0 (B2 regularized LS): solve (H^H H + lambda I)^-1 H^H.
    - condition_guard (B2 condition guard): skip derotation when cond(H) too
      large (leave data uncorrected for that block).
    data_only=True restricts the inverse to the data mask (pilots excluded).
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
        if ema_alpha is not None:
            ema_h = H if ema_h is None else ema_alpha * ema_h + (1 - ema_alpha) * H
            H_use = ema_h
        else:
            H_use = H
        inv = _regularized_inverse(H_use, tikhonov, condition_guard)
        if inv is None:
            skipped += 1
            continue
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y, "skipped_blocks": skipped}


def derotate_uncertainty_tracker(pilot_rx, estimates, *, block_size,
                                 alpha_lo=0.5, alpha_hi=0.95,
                                 cond_gate=50.0, sigma2_n_proxy=0.005,
                                 data_only=True):
    """Proposed method P: uncertainty-aware temporal matrix tracker.

    Receiver-visible information ONLY. For each block we maintain a smoothed
    Jones estimate whose EMA factor adapts to a receiver-visible uncertainty
    proxy: when the per-block pilot-LS Gram is well-conditioned and the
    block-to-block matrix innovation is small we TRUST the current block
    (low alpha -> weight the fresh estimate); when conditioning degrades or the
    innovation spikes we fall back to history (high alpha -> trust memory).

    alpha in [alpha_lo, alpha_hi] is selected per block from a logistic map of
    the receiver-visible normalized innovation ||H_b - H_{b-1}||_F / scale and
    the log-condition number log10(cond(H_b)). This is structurally different
    from a fixed-alpha EMA (B1) because the mixing coefficient is a FUNCTION of
    receiver-visible per-block state, not a constant.

    Inputs used: pilot RX, pilot symbols, pilot mask, own previous matrix
    estimate. NOT used: true h/theta/Jones/TX data.
    """
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    ema_h = None
    prev_h = None
    skipped = 0
    alphas = []
    for est in estimates:
        start = est["block"]
        idx = np.arange(start, min(start + block_size, len(x)))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        H = np.asarray(est["matrix"], complex)
        cond = max(est["cond"], 1.0)
        if prev_h is None:
            innov = 1.0
        else:
            innov = float(np.linalg.norm(H - prev_h, "fro"))
        # receiver-visible normalized uncertainty -> alpha in [alpha_lo, alpha_hi]
        # higher uncertainty (innovation, conditioning) -> higher alpha (trust memory)
        z = 0.6 * np.tanh(innov / 0.1) + 0.4 * np.tanh(np.log10(cond) / np.log10(cond_gate))
        alpha = alpha_lo + (alpha_hi - alpha_lo) * (1.0 / (1.0 + np.exp(-3.0 * z)))
        alphas.append(float(alpha))
        ema_h = H if ema_h is None else alpha * ema_h + (1 - alpha) * H
        inv = _regularized_inverse(ema_h, 0.0, None)
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
        prev_h = H
    return {"rX": x, "rY": y, "skipped_blocks": skipped,
            "alpha_mean": float(np.mean(alphas)) if alphas else None}


def derotate_oracle(pilot_rx, realization, *, block_size, data_only=True):
    """Oracle O (tagged): use the TRUE theta to build the ideal inverse.

    ONLY for scoring upper bound (per T002 rule 8 + FR-21). Never a Go opponent.
    """
    x = np.array(pilot_rx["rX"], copy=True); y = np.array(pilot_rx["rY"], copy=True)
    dm = np.asarray(pilot_rx["data_mask"])
    theta = np.asarray(realization["theta"])
    for start in range(0, len(x), block_size):
        idx = np.arange(start, min(start + block_size, len(x)))
        if data_only:
            idx = idx[dm[idx]]
        if not len(idx):
            continue
        th = float(np.mean(theta[idx]))
        c, s = np.cos(th), np.sin(th)
        H = np.array([[c, s], [-s, c]], complex)
        inv = np.array([[c, -s], [s, c]], complex)
        corr = inv @ np.stack((x[idx], y[idx]), axis=0)
        x[idx], y[idx] = corr[0], corr[1]
    return {"rX": x, "rY": y}


# ---------------------------------------------------------------------------
# Arm wiring: build a realization-view per arm, then run standard CMA on it.
# ---------------------------------------------------------------------------

def build_arm_view(realization, derotated_or_rx):
    """Merge derotated RX into a realization-like dict (keeps sX/sY for eval)."""
    return {**realization, "rX": derotated_or_rx["rX"], "rY": derotated_or_rx["rY"]}


ARMS = {
    # label -> (kind, kwargs-for-derotate) ; kind in {none, derotate, tracker, oracle}
    "B0_blockLS_pinv":      ("derotate", {"tikhonov": 0.0, "condition_guard": None, "ema_alpha": None}),
    "B1_fixedEMA09":        ("derotate", {"tikhonov": 0.0, "condition_guard": None, "ema_alpha": 0.9}),
    "B2a_tikhonov":         ("derotate", {"tikhonov": 1e-2, "condition_guard": None, "ema_alpha": None}),
    "B2b_condition_guard":  ("derotate", {"tikhonov": 0.0, "condition_guard": 50.0, "ema_alpha": None}),
    "P_uncertainty_tracker":("tracker",  {}),
    "O_true_theta_oracle":  ("oracle",   {}),
}
