"""Standalone cold-start Decision-Directed LMS equalizer (legal fallback expert).

Sato 1975 cost J = E[|s_hat - z|^2], s_hat = hard_16qam(z).
Update: w += mu * (s_hat - z) * conj(x), blockwise (same structure as CMA anchor).

This is a STANDALONE cold-start DD-LMS (NOT the C11 cascade stage-2). It runs from
center-tap init with NO CMA warm-up. Cold-start DD-LMS is well-known to diverge on
blind channels (which is why the C11 cascade exists); divergence is an EXPECTED,
documented diagnostic outcome, not a bug.

Provenance:
  - Sato 1975 (original DD-LMS / reduced-constellation)
  - Haykin, Adaptive Filter Theory (standard DD-LMS textbook form)
  - hard_16qam decision slicer reuses cb1_evaluator / _modulation convention

Identity contract (same gate set as CMA anchor + MMA):
  - no_op: when decision feedback is disabled (mu=0 on the DD correction), output
           equals a pure center-tap filter (identity of the structure)
  - complex_convention: uses conj(x) consistently with CMA/MMA (r @ w filtering)
  - causal_prefix: changing future samples does not change earlier outputs
  - source_closure: docstring + formula cited
  - decision_feedback_causal: s_hat at time t uses ONLY z[t], not future z
"""

from __future__ import annotations
import numpy as np


def _hard_16qam(z: np.ndarray) -> np.ndarray:
    """Hard decision to nearest 16QAM symbol, per-axis {-3,-1,+1,+3}/sqrt(10)."""
    grid = np.array([-3, -1, 1, 3], dtype=float) / np.sqrt(10.0)
    re = grid[np.argmin(np.abs(z.real[..., None] - grid[None, :]), axis=-1)]
    im = grid[np.argmin(np.abs(z.imag[..., None] - grid[None, :]), axis=-1)]
    return re + 1j * im


def dd_lms_cold_start(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
) -> dict:
    """Run dual-pol cold-start DD-LMS blockwise, same structure as CMA anchor.

    2x2 butterfly FIR: yX = wxx@rX_win + wxy@rY_win, yY = wyx@rX_win + wyy@rY_win.
    Center-tap init (energy normalized to sqrt(2) total, matching CMA/MMA).
    Block-end weight update using the DD gradient (s_hat - z) * conj(r).
    """
    N = len(rX)
    L = n_tap
    half = L // 2

    # Center-tap init (same as CMA anchor: wxx=wyy=1, wxy=wyx=0, then normalize energy to sqrt(2))
    scale = np.sqrt(2.0) / np.sqrt(2.0 * (1.0 ** 2))  # =1.0 for unit taps; keep explicit for clarity
    wxx = np.zeros(L, dtype=complex); wxx[half] = 1.0 * scale
    wyy = np.zeros(L, dtype=complex); wyy[half] = 1.0 * scale
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    div_threshold = 1e3
    diverged = False
    diverge_idx = None

    def _filter_block(r_win_x, r_win_y):
        # r_win: [block, L] sliding window; output = sum over taps
        yX = r_win_x @ wxx + r_win_y @ wxy
        yY = r_win_x @ wyx + r_win_y @ wyy
        return yX, yY

    pos = 0
    while pos < N:
        end = min(pos + block_size, N)
        blen = end - pos
        # Build sliding windows for this block
        idx = np.arange(pos, end)
        wins = np.stack([np.arange(-half, half + 1)] * blen, axis=0) + idx[:, None]
        # Clamp at boundaries (replicate edge)
        wins = np.clip(wins, 0, N - 1)
        rXw = rX[wins]
        rYw = rY[wins]
        yX, yY = _filter_block(rXw, rYw)
        zX[pos:end] = yX
        zY[pos:end] = yY

        if not diverged:
            # DD-LMS block-end update: decision on block output, then gradient step
            sX_hat = _hard_16qam(yX)
            sY_hat = _hard_16qam(yY)
            eX = sX_hat - yX
            eY = sY_hat - yY
            grad_xx = np.mean(eX[:, None] * np.conj(rXw), axis=0)
            grad_xy = np.mean(eX[:, None] * np.conj(rYw), axis=0)
            grad_yx = np.mean(eY[:, None] * np.conj(rXw), axis=0)
            grad_yy = np.mean(eY[:, None] * np.conj(rYw), axis=0)
            wxx = wxx + mu * grad_xx
            wxy = wxy + mu * grad_xy
            wyx = wyx + mu * grad_yx
            wyy = wyy + mu * grad_yy
            # Divergence check (same L2-norm criterion as CMA anchor: sqrt(sum|w|^2))
            wnorm = np.sqrt(np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2) +
                            np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2))
            opow = np.mean(np.abs(yX) ** 2 + np.abs(yY) ** 2)
            if (not np.isfinite(wnorm)) or wnorm > div_threshold or opow > 10.0 * 2.0:
                diverged = True
                diverge_idx = pos
        pos = end

    final_w_norm = float(np.sqrt(np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2) +
                                  np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)))
    return {
        "zX": zX, "zY": zY,
        "diverged": bool(diverged),
        "divergence_symbol": diverge_idx,
        "final_w_norm": final_w_norm,
        "init": {"wxx": wxx.copy(), "wxy": wxy.copy(), "wyx": wyx.copy(), "wyy": wyy.copy()},
        "cost_contains_modulus_term": False,   # DD uses hard-decision feedback, not modulus
    }
