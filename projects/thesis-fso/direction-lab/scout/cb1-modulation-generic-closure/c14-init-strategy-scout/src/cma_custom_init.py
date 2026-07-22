"""C14 custom-init Godard-with-z runner + data-driven init estimators.

This is the C14 init-strategy scout's core. It is a COPY-AND-ADAPT of
``baseline-atlas/cb1_cell_runner.standard_cma_godard_with_z``: the blockwise
Godard-with-z update (prompt013:301-306) is reproduced VERBATIM, with ONE
change — the four filter vectors ``wxx, wxy, wyx, wyy`` are seeded from a
caller-provided ``w_init`` instead of the hard-coded center-tap. When
``w_init`` is the center-tap, this function is BYTE-FOR-BYTE IDENTICAL to the
baseline-atlas anchor (identity gate: ``max |Δz| == 0.0``).

The CMA cost, gradient, μ, taps, block_size, R², and divergence criteria are
UNCHANGED from the anchor. The ONLY thing varied is the starting point. This
isolates the scientific question: is the inner-ring collapse init-dependent?

Init estimators (all consume ONLY the received signal r, never the CMA output
z — using z to init the CMA that produces z would be circular):
  * ``center_tap_init``             — the anchor (data-independent).
  * ``whitening_init``              — dominant eigenvector of the received-signal
                                      dual-pol covariance (receiver-visible).
  * ``oracle_wiener_init``          — principal direction of the TX-truth Wiener
                                      (MMSE) filter (Kill bound; uses truth).
  * ``random_multistart_init``      — best-of-K unit-norm starts by warmup Godard
                                      cost (receiver-visible).

Identity-gate rationale: the baseline anchor's body is copied line-for-line so
that the center-tap path produces identical bits; the divergence thresholds and
trace bookkeeping are also preserved so per-seed collapse/divergence flags are
comparable across inits.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ─── Standard-CMA (Godard-with-z) blockwise equalizer, CUSTOM INIT ────────────

def standard_cma_godard_with_z_custom_init(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    R2: float = 1.0,
    block_size: int = 64,
    w_init: dict[str, np.ndarray] | None = None,
) -> dict[str, Any]:
    """Run standard-CMA (Godard-with-z) blockwise with a CUSTOM initialization.

    This is a byte-for-byte copy of
    ``cb1_cell_runner.standard_cma_godard_with_z`` with the four filter
    vectors seeded from ``w_init`` instead of the hard-coded center tap.

    Parameters
    ----------
    rX, rY : (N,) complex
        Dual-polarization received streams.
    n_tap, mu, R2, block_size : CMA hyperparameters (identical to the anchor).
    w_init : dict with keys ``wxx, wxy, wyx, wyy`` each (n_tap,) complex.
        If ``None`` (default), the center-tap init is used and the result is
        byte-identical to the baseline-atlas anchor (identity gate).

    Returns
    -------
    dict with the SAME keys as ``standard_cma_godard_with_z``: ``zX, zY,
    diverged, divergence_symbol, final_w_norm, init_w_norm, trace,
    provenance``, plus ``w_init`` (the init used) for provenance.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    block_size = int(block_size)

    # --- Initialization -------------------------------------------------------
    if w_init is None:
        # Center-tap (the anchor): identical to baseline-atlas:76-80.
        wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
        wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
        wxy = np.zeros(L, dtype=complex)
        wyx = np.zeros(L, dtype=complex)
    else:
        # Custom init: copy so the caller's vectors are not mutated by the update.
        wxx = np.array(w_init["wxx"], dtype=complex).copy()
        wxy = np.array(w_init["wxy"], dtype=complex).copy()
        wyx = np.array(w_init["wyx"], dtype=complex).copy()
        wyy = np.array(w_init["wyy"], dtype=complex).copy()
        if not (len(wxx) == len(wxy) == len(wyx) == len(wyy) == L):
            raise ValueError(
                f"w_init vectors must each have length n_tap={L}; got "
                f"{len(wxx)},{len(wxy)},{len(wyx)},{len(wyy)}"
            )

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    init_norm = _wnorm()

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)
    trace: list[dict[str, Any]] = []

    # Divergence criteria (identical to baseline-atlas:95-97, TL-20).
    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3

    diverged = False
    diverge_idx = None

    rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // block_size

    for blk in range(n_blocks):
        s = blk * block_size
        e = s + block_size
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]

        # Intra-block filter with fixed weights (prompt013:377-378, Eq.28).
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        # Write to output aligned at s+half (prompt013:369, _cma.py:155).
        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # Godard-with-z block-end gradient (prompt013:301-306).
        eX = R2 - np.abs(zx_blk) ** 2
        eY = R2 - np.abs(zy_blk) ** 2
        wxx += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + block_size),
            "cm_error": float(np.mean((R2 - np.abs(zx_blk) ** 2) ** 2
                                      + (R2 - np.abs(zy_blk) ** 2) ** 2)),
            "output_power": float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2)),
            "update_norm": float(np.sqrt(
                np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
            )),
            "w_norm": cur_norm,
            "z_amp_max": cur_zamp,
        })

        if not diverged:
            if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                    or not np.isfinite(cur_norm)):
                diverged = True
                diverge_idx = idx + block_size - 1
                break

    return {
        "zX": zX,
        "zY": zY,
        "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(),
        "init_w_norm": init_norm,
        "trace": trace,
        "w_init": {"wxx": wxx, "wxy": wxy, "wyx": wyx, "wyy": wyy},
        # Identity-gate stamp: matches the baseline-atlas provenance string so a
        # center-tap run is verifiably the same algorithm.
        "provenance": {
            "implementation": "cma_custom_init.standard_cma_godard_with_z_custom_init",
            "entry": "blockwise standard-CMA (mode='standard', prompt013:301-306) with custom init",
            "gradient": "Godard-with-z",
        },
    }


# ─── Init estimators (consume ONLY the received signal r; never z) ────────────

def center_tap_init(n_tap: int) -> dict[str, np.ndarray]:
    """The anchor init: w[center]=1, rest=0 (baseline-atlas:76-80)."""
    L = int(n_tap)
    center = L // 2
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)
    return {"wxx": wxx, "wxy": wxy, "wyx": wyx, "wyy": wyy}


def _stack_dual_pol_windows(rX: np.ndarray, rY: np.ndarray, L: int) -> np.ndarray:
    """Dual-pol received-signal window stack, shape (M, 2L).

    Row i is [rX_win[i, :], rY_win[i, :]] so the covariance is the full
    (2L)x(2L) cross-pol covariance. This is the receiver-visible statistic
    the init estimators consume.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
    rY_win = sliding_window_view(rY, L)
    return np.concatenate([rX_win, rY_win], axis=1)  # (M, 2L)


def whitening_init(rX_calib: np.ndarray, rY_calib: np.ndarray, *, n_tap: int) -> dict[str, np.ndarray]:
    """Dominant-eigenvector init from the received-signal covariance.

    Receiver-visible: consumes ONLY rX_calib, rY_calib (no TX truth, no CMA
    output z). Forms the (2L)x(2L) dual-pol covariance C = E[w w^H] over the
    calibration window and takes its principal (largest-eigenvalue) eigenvector.
    The principal eigenvector "points" the filter at the strongest received
    signal direction (the dominant spatial/temporal mode) instead of the
    trivial center tap.

    Mapping to the 4 filter vectors: the 2L principal-eigenvector components
    are split as [wxx (L taps on rX), wxy (L taps on rY)] for the X-output
    row and [wyx, wyy] for the Y-output row. We use the SAME eigenvector for
    both rows (the dominant received mode is pol-symmetric in expectation),
    then normalize the full 4-vector stack to unit norm so the divergence
    thresholds are comparable to the center-tap anchor.
    """
    L = int(n_tap)
    W = _stack_dual_pol_windows(rX_calib, rY_calib, L)  # (M, 2L)
    if W.shape[0] < 2:
        raise ValueError("whitening_init needs >= 2 calibration windows")
    # Hermitian covariance (2L x 2L).
    C = (W.conj().T @ W) / float(W.shape[0])
    C = (C + C.conj().T) / 2.0  # enforce Hermitian for eigh
    evals, evecs = np.linalg.eigh(C)  # ascending
    principal = evecs[:, -1]  # (2L,) dominant mode
    v_x = principal[:L]
    v_y = principal[L:]
    wxx = np.array(v_x, dtype=complex)
    wxy = np.array(v_y, dtype=complex)
    wyx = np.array(v_x, dtype=complex)
    wyy = np.array(v_y, dtype=complex)
    return _normalize_init({"wxx": wxx, "wxy": wxy, "wyx": wyx, "wyy": wyy})


def oracle_wiener_init(
    rX_calib: np.ndarray,
    rY_calib: np.ndarray,
    sX_calib: np.ndarray,
    sY_calib: np.ndarray,
    *,
    n_tap: int,
) -> dict[str, np.ndarray]:
    """TX-truth Wiener (MMSE) init direction. Kill bound ONLY (uses truth).

    Computes the dual-pol Wiener filter W = R_rr^{-1} R_rs, where R_rs is the
    cross-covariance between received windows and the TX truth symbol at the
    center tap. We solve the MMSE filter for each output (zx, zy) and use its
    principal direction as the init. Because it uses TX truth this is a
    diagnostic bound on how good init can be — never a runtime comparator.

    The truth symbol is aligned at the center of the L-tap window (the same
    alignment the CMA uses for its output write, prompt013:369).
    """
    L = int(n_tap)
    half = L // 2
    rX = np.asarray(rX_calib, dtype=complex)
    rY = np.asarray(rY_calib, dtype=complex)
    sX = np.asarray(sX_calib, dtype=complex)
    sY = np.asarray(sY_calib, dtype=complex)
    rX_win = sliding_window_view(rX, L)  # (M, L)
    rY_win = sliding_window_view(rY, L)
    M = rX_win.shape[0]
    # Truth aligned at the center tap (the window's middle sample).
    sXc = sX[half:half + M]
    sYc = sY[half:half + M]
    # Full dual-pol received window stack: [rX_win | rY_win], shape (M, 2L).
    R = np.concatenate([rX_win, rY_win], axis=1)  # (M, 2L)
    # R_rr = E[r r^H] (2L x 2L), regularized for invertibility.
    Rrr = (R.conj().T @ R) / float(M) + 1e-9 * np.eye(2 * L)
    # Solve for the two output rows (zx targets sXc, zy targets sYc).
    W_x = np.linalg.solve(Rrr, (R.conj().T @ sXc) / float(M))  # (2L,)
    W_y = np.linalg.solve(Rrr, (R.conj().T @ sYc) / float(M))  # (2L,)
    wxx = W_x[:L]
    wxy = W_x[L:]
    wyx = W_y[:L]
    wyy = W_y[L:]
    return _normalize_init({"wxx": wxx, "wxy": wxy, "wyx": wyx, "wyy": wyy})


def random_multistart_init(
    rX_calib: np.ndarray,
    rY_calib: np.ndarray,
    *,
    n_tap: int,
    mu: float,
    R2: float,
    block_size: int,
    K: int = 5,
    warmup_blocks: int = 1,
    rng: np.random.Generator | None = None,
) -> tuple[dict[str, np.ndarray], list[float]]:
    """Best-of-K random unit-norm init by warmup Godard cost.

    Receiver-visible: consumes ONLY rX_calib, rY_calib. Generates K random
    unit-norm complex weight vectors, runs each for a SHORT warmup
    (``warmup_blocks`` blocks) via the Godard-with-z update, scores each start
    by the mean Godard cost (R²-|z|²)² over the warmup, and returns the
    lowest-cost start. This tests whether collapse is init-SPECIFIC (some
    random starts escape the center-tap basin).

    Returns (best_init, list_of_K_warmup_costs).
    """
    if rng is None:
        rng = np.random.default_rng(0)
    L = int(n_tap)
    rX = np.asarray(rX_calib, dtype=complex)
    rY = np.asarray(rY_calib, dtype=complex)
    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = rX_win.shape[0]
    wb = max(1, int(warmup_blocks))
    n_blk = min(wb, n_valid // int(block_size))
    if n_blk < 1:
        raise ValueError("random_multistart_init: calibration too short for warmup")
    bs = int(block_size)

    costs: list[float] = []
    best_cost = np.inf
    best_init: dict[str, np.ndarray] | None = None
    for _ in range(int(K)):
        # Random complex init (4 filter vectors). Normalized to target_norm
        # = sqrt(2) to match the center-tap anchor's total filter energy, so
        # the Godard cost scale is comparable across inits.
        a = (rng.standard_normal(L) + 1j * rng.standard_normal(L))
        b = (rng.standard_normal(L) + 1j * rng.standard_normal(L))
        c = (rng.standard_normal(L) + 1j * rng.standard_normal(L))
        d = (rng.standard_normal(L) + 1j * rng.standard_normal(L))
        stacked = np.concatenate([a, b, c, d])
        stacked = stacked / np.linalg.norm(stacked) * np.sqrt(2.0)
        init = {
            "wxx": stacked[0:L].copy(),
            "wxy": stacked[L:2 * L].copy(),
            "wyx": stacked[2 * L:3 * L].copy(),
            "wyy": stacked[3 * L:4 * L].copy(),
        }
        # Short warmup: replicate the Godard-with-z update for n_blk blocks.
        wxx = init["wxx"].copy(); wxy = init["wxy"].copy()
        wyx = init["wyx"].copy(); wyy = init["wyy"].copy()
        cost_acc = 0.0
        for blk in range(n_blk):
            s = blk * bs; e = s + bs
            rXb = rX_win[s:e]; rYb = rY_win[s:e]
            zx = rXb @ wxx + rYb @ wxy
            zy = rXb @ wyx + rYb @ wyy
            cost_acc += float(np.mean((R2 - np.abs(zx) ** 2) ** 2
                                      + (R2 - np.abs(zy) ** 2) ** 2))
            eX = R2 - np.abs(zx) ** 2
            eY = R2 - np.abs(zy) ** 2
            wxx += mu * np.mean((eX * zx)[:, None] * np.conj(rXb), axis=0)
            wxy += mu * np.mean((eX * zx)[:, None] * np.conj(rYb), axis=0)
            wyx += mu * np.mean((eY * zy)[:, None] * np.conj(rXb), axis=0)
            wyy += mu * np.mean((eY * zy)[:, None] * np.conj(rYb), axis=0)
        mean_cost = cost_acc / n_blk
        costs.append(mean_cost)
        if mean_cost < best_cost:
            best_cost = mean_cost
            best_init = {"wxx": init["wxx"], "wxy": init["wxy"],
                         "wyx": init["wyx"], "wyy": init["wyy"]}
    assert best_init is not None
    return best_init, costs


def _normalize_init(init: dict[str, np.ndarray], target_norm: float = np.sqrt(2.0)) -> dict[str, np.ndarray]:
    """Normalize the full 4-vector filter stack to a target L2 norm.

    Default ``target_norm = sqrt(2)`` matches the center-tap anchor's total
    filter energy (1 in wxx[center] + 1 in wyy[center]). This keeps the
    divergence threshold (10 x init_norm) and the CMA's effective output scale
    directly comparable to the center-tap anchor, so any collapse-rate
    difference is attributable to the init DIRECTION, not its magnitude. The
    Godard cost is scale-sensitive (R² is fixed), so matching init energy is
    the fair comparison."""
    stacked = np.concatenate([init["wxx"], init["wxy"], init["wyx"], init["wyy"]])
    n = np.linalg.norm(stacked)
    if n < 1e-15:
        raise ValueError("init has near-zero norm; cannot normalize")
    stacked = stacked * (float(target_norm) / n)
    L = len(init["wxx"])
    return {
        "wxx": stacked[0:L].copy(),
        "wxy": stacked[L:2 * L].copy(),
        "wyx": stacked[2 * L:3 * L].copy(),
        "wyy": stacked[3 * L:4 * L].copy(),
    }


def init_norm(init: dict[str, np.ndarray]) -> float:
    """Full 4-vector filter L2 norm (matches the CMA _wnorm at init)."""
    return float(np.sqrt(
        np.sum(np.abs(init["wxx"]) ** 2) + np.sum(np.abs(init["wxy"]) ** 2)
        + np.sum(np.abs(init["wyx"]) ** 2) + np.sum(np.abs(init["wyy"]) ** 2)
    ))


__all__ = [
    "standard_cma_godard_with_z_custom_init",
    "center_tap_init",
    "whitening_init",
    "oracle_wiener_init",
    "random_multistart_init",
    "init_norm",
]
