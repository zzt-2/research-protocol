"""Pre-formal Method Factory Sprint 003 — update-granularity CMA family.

EVERY construct in this module acts directly on RAW rX/rY and produces its OWN
equalized z-stream. This is the FUNDAMENTAL difference from sprint-001/002,
whose M1-M5 were z-only post-processing of the block-64 baseline's output. Here
the update GRANULARITY of the equalizer weight itself is the lever.

All constructs share the SAME canonical Godard-with-z gradient identity

    dw ∝ (R² - |z|²) · z · r*                      # contains the z factor

provenance cb1_cell_runner.py:124-129 (block-end averaged form:
``(eX * zx_blk)[:, None] * conj(rX_blk)`` then ``mean``). The per-symbol
analogue drops the ``mean`` and updates immediately after each symbol. The
scalar-error form ``(R² - |z|²) · r*`` (common/_cma.py CMAEqualizer2x2,
_cma.py:161-166, MISSING the z factor) is FORBIDDEN as the comparator.

Constructs
----------
(a) block64_cma_mu0p03 : inherited anchor. Wrapper over
    cb1_cell_runner.standard_cma_godard_with_z(block_size=64, mu=0.03). mu is
    FROZEN, NOT re-tuned here. Reported for context (NOT the Go comparator).
(b) persymbol_cma_godard_with_z : the TRADITIONAL COMPARATOR. Per-symbol
    immediate Godard-with-z update. mu tuned on dev.
(c) blockN_cma_godard_with_z(N=8,16) : block-end averaged Godard-with-z with a
    SMALLER block (more updates per symbol). Same gradient identity as the
    block-64 anchor / comparator; only the block granularity differs.
(d) sliding_window_recursive_cma : per-symbol update rate but accumulates the
    gradient with a recursive (leaky) running mean — block MEMORY on top of the
    per-symbol update rate.

Determinism / causality: every method is a PURE FUNCTION of (rX, rY, frozen
params). No RNG. Re-running on the same raw input yields bit-identical z. The
scored eval suffix never feeds back into the equalizer; only frozen (mu,
granularity) chosen on dev enter the equalizer.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ─── Shared divergence criteria (mirror cb1_cell_runner.py:94-99, _cma.py:132) ──

def _init_weights(n_tap: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Center-tap init (cb1_cell_runner.py:76-80, _cma.py:80-86)."""
    L = int(n_tap)
    center = L // 2
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)
    return wxx, wyy, wxy, wyx


def _wnorm(wxx, wxy, wyx, wyy) -> float:
    return float(np.sqrt(
        np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
        + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)))


def _diverged(cur_norm: float, cur_zamp: float, init_norm: float) -> bool:
    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3
    return (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
            or not np.isfinite(cur_norm))


# ─── (a) Inherited anchor: block-64 CMA, mu FROZEN (thin wrapper) ────────────

def block64_cma_mu0p03(rX: np.ndarray, rY: np.ndarray, *,
                       n_tap: int = 11, mu: float = 3.0e-2,
                       R2: float = 1.32, block_size: int = 64) -> dict[str, Any]:
    """Inherited shared-anchor baseline. Delegates to cb1_cell_runner so the
    z-stream is byte-identical to the validated anchor. mu is inherited
    (frozen-params-b01r-v1.yaml); NOT re-tuned here. NOT the Go comparator."""
    import cb1_cell_runner as runner
    return runner.standard_cma_godard_with_z(
        rX, rY, n_tap=n_tap, mu=mu, R2=R2, block_size=block_size)


# ─── (b) Traditional comparator: per-symbol Godard-with-z CMA ────────────────

def persymbol_cma_godard_with_z(rX: np.ndarray, rY: np.ndarray, *,
                                n_tap: int = 11, mu: float = 1.0e-3,
                                R2: float = 1.32,
                                check_every: int = 64) -> dict[str, Any]:
    """Per-symbol standard-CMA (canonical Godard-with-z) — the TRADITIONAL
    COMPARATOR.

    Each symbol produces a fresh filter output z = W·r, then the four weight
    rows are updated IMMEDIATELY with the canonical per-symbol Godard-with-z
    gradient

        dw = mu · (R² - |z|²) · z · conj(r)        # contains the z factor

    This is the per-symbol analogue of cb1_cell_runner.py:124-129. The runner's
    block-end form is ``mu · mean( (eX*zx_blk)[:,None] * conj(rX_blk) )`` (block-
    averaged Godard-with-z). Dropping the mean and applying the update per
    symbol keeps the gradient IDENTITY identical; only the update GRANULARITY
    changes (block-averaged -> per-symbol immediate). Each update is full-
    strength (no block-mean attenuation), so the per-symbol mu is typically much
    smaller than the block-end mu; it is tuned separately on dev.

    Center-tap init, divergence criteria, and output alignment are identical to
    cb1_cell_runner.standard_cma_godard_with_z. Divergence is checked every
    `check_every` symbols so the per-sample loop is not dominated by checks.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    block_size = 64  # NOT a weight-update granularity here; only a divergence-check stride

    wxx, wyy, wxy, wyx = _init_weights(L)
    init_norm = _wnorm(wxx, wxy, wyx, wyy)

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1

    diverged = False
    diverge_idx = None
    for i in range(n_valid):
        rx = rX_win[i]
        ry = rY_win[i]
        zx = rx @ wxx + ry @ wxy
        zy = rx @ wyx + ry @ wyy
        idx = i + half
        zX[idx] = zx
        zY[idx] = zy

        # Canonical per-symbol Godard-with-z gradient (contains z factor).
        eX = R2 - abs(zx) ** 2
        eY = R2 - abs(zy) ** 2
        gx = eX * zx          # (R^2 - |z|^2) * z  (the z factor is here)
        gy = eY * zy
        wxx += mu * gx * np.conj(rx)
        wxy += mu * gx * np.conj(ry)
        wyx += mu * gy * np.conj(rx)
        wyy += mu * gy * np.conj(ry)

        if (i + 1) % check_every == 0:
            cur_norm = _wnorm(wxx, wxy, wyx, wyy)
            cur_zamp = max(abs(zx), abs(zy))
            if _diverged(cur_norm, cur_zamp, init_norm):
                diverged = True
                diverge_idx = idx
                break

    return {
        "zX": zX, "zY": zY, "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(wxx, wxy, wyx, wyy),
        "init_w_norm": init_norm,
        "provenance": {
            "implementation": "methods.persymbol_cma_godard_with_z",
            "entry": "per-symbol standard-CMA (canonical Godard-with-z)",
            "gradient": "Godard-with-z",
            "update_granularity": "per_symbol_immediate",
            "gradient_provenance": "cb1_cell_runner.py:124-129 (block-averaged -> per-symbol, identity unchanged)",
        },
    }


# ─── (c) Smaller-block Godard-with-z CMA (block-end averaged, block_size=N) ───

def blockN_cma_godard_with_z(rX: np.ndarray, rY: np.ndarray, *,
                             n_tap: int = 11, mu: float, R2: float = 1.32,
                             block_size: int) -> dict[str, Any]:
    """Block-end averaged Godard-with-z CMA with a SMALLER block_size.

    Identical gradient identity and structure to the block-64 anchor
    (cb1_cell_runner.py:106-129): intra-block vectorized filter with fixed
    weights, block-end weight update using the block-AVERAGED Godard-with-z
    gradient ``mu · mean( (eX*zx_blk)[:,None] * conj(rX_blk) )``. The ONLY
    difference is block_size < 64, giving more weight updates per symbol. This
    isolates the "smaller block granularity" mechanism from the per-symbol
    immediate mechanism.

    A separate mu must be tuned per block_size (a smaller block has less
    averaging, so the stable mu differs from the block-64 mu).
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    block_size = int(block_size)
    if block_size < 1:
        raise ValueError("block_size must be >= 1")

    wxx, wyy, wxy, wyx = _init_weights(L)
    init_norm = _wnorm(wxx, wxy, wyx, wyy)

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // block_size

    diverged = False
    diverge_idx = None
    for blk in range(n_blocks):
        s = blk * block_size
        e = s + block_size
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]

        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # Block-end AVERAGED Godard-with-z gradient (identical identity to anchor).
        eX = R2 - np.abs(zx_blk) ** 2
        eY = R2 - np.abs(zy_blk) ** 2
        wxx += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = _wnorm(wxx, wxy, wyx, wyy)
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        if _diverged(cur_norm, cur_zamp, init_norm):
            diverged = True
            diverge_idx = idx + block_size - 1
            break

    return {
        "zX": zX, "zY": zY, "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(wxx, wxy, wyx, wyy),
        "init_w_norm": init_norm,
        "provenance": {
            "implementation": f"methods.blockN_cma_godard_with_z(block_size={block_size})",
            "entry": f"block-{block_size} standard-CMA (canonical Godard-with-z, block-end averaged)",
            "gradient": "Godard-with-z",
            "update_granularity": f"block_end_averaged_block{block_size}",
            "gradient_provenance": "cb1_cell_runner.py:124-129",
        },
    }


# ─── (d) Sliding-window recursive CMA (per-symbol rate + recursive memory) ────

def sliding_window_recursive_cma(rX: np.ndarray, rY: np.ndarray, *,
                                 n_tap: int = 11, mu: float = 1.0e-3,
                                 R2: float = 1.32, lam: float = 0.9,
                                 check_every: int = 64) -> dict[str, Any]:
    """Per-symbol update rate with a recursive (leaky) gradient accumulator.

    Mechanism (distinct from pure per-symbol): instead of the pure
    instantaneous per-symbol gradient, maintain a recursive running mean of the
    Godard-with-z gradient with forgetting factor ``lam``:

        g_acc <- lam * g_acc + (1 - lam) * g_inst
        W <- W + mu * g_acc

    where ``g_inst = (R^2 - |z|^2) * z * conj(r)`` is the canonical per-symbol
    Godard-with-z gradient (same identity). This is "block memory on top of the
    per-symbol update rate": it updates every symbol (same update rate as the
    comparator) but smooths the gradient with a recursive window — a distinct
    mechanism from both pure per-symbol and block-end averaged.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2

    wxx, wyy, wxy, wyx = _init_weights(L)
    init_norm = _wnorm(wxx, wxy, wyx, wyy)

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1

    # Recursive gradient accumulators (one per weight row).
    gxx = np.zeros(L, dtype=complex)
    gxy = np.zeros(L, dtype=complex)
    gyx = np.zeros(L, dtype=complex)
    gyy = np.zeros(L, dtype=complex)

    diverged = False
    diverge_idx = None
    one_minus_lam = 1.0 - lam
    for i in range(n_valid):
        rx = rX_win[i]
        ry = rY_win[i]
        zx = rx @ wxx + ry @ wxy
        zy = rx @ wyx + ry @ wyy
        idx = i + half
        zX[idx] = zx
        zY[idx] = zy

        eX = R2 - abs(zx) ** 2
        eY = R2 - abs(zy) ** 2
        gx_inst = eX * zx * np.conj(rx)   # per-symbol Godard-with-z (contains z)
        gy_inst_rx = eX * zx * np.conj(ry)
        gyx_inst = eY * zy * np.conj(rx)
        gyy_inst = eY * zy * np.conj(ry)
        gxx = lam * gxx + one_minus_lam * gx_inst
        gxy = lam * gxy + one_minus_lam * gy_inst_rx
        gyx = lam * gyx + one_minus_lam * gyx_inst
        gyy = lam * gyy + one_minus_lam * gyy_inst

        wxx += mu * gxx
        wxy += mu * gxy
        wyx += mu * gyx
        wyy += mu * gyy

        if (i + 1) % check_every == 0:
            cur_norm = _wnorm(wxx, wxy, wyx, wyy)
            cur_zamp = max(abs(zx), abs(zy))
            if _diverged(cur_norm, cur_zamp, init_norm):
                diverged = True
                diverge_idx = idx
                break

    return {
        "zX": zX, "zY": zY, "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(wxx, wxy, wyx, wyy),
        "init_w_norm": init_norm,
        "provenance": {
            "implementation": "methods.sliding_window_recursive_cma",
            "entry": "sliding-window recursive standard-CMA (canonical Godard-with-z, recursive mean)",
            "gradient": "Godard-with-z",
            "update_granularity": "per_symbol_recursive_running_mean",
            "gradient_provenance": "cb1_cell_runner.py:124-129 (per-symbol + recursive memory)",
        },
    }


# ─── Effective-update-budget helper (for ablation) ────────────────────────────

def updates_per_symbol(granularity: str, block_size: int | None = None) -> float:
    """Number of weight updates per symbol for each granularity.

    block_end_averaged with block_size B -> 1/B updates per symbol.
    per_symbol_* -> 1 update per symbol."""
    if granularity.startswith("per_symbol"):
        return 1.0
    if granularity.startswith("block_end_averaged"):
        if block_size is None or block_size < 1:
            raise ValueError("block_end_averaged needs block_size")
        return 1.0 / float(block_size)
    raise ValueError(f"unknown granularity: {granularity}")


__all__ = [
    "block64_cma_mu0p03",
    "persymbol_cma_godard_with_z",
    "blockN_cma_godard_with_z",
    "sliding_window_recursive_cma",
    "updates_per_symbol",
]
