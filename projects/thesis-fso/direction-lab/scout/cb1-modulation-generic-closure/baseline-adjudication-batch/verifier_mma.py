"""Clean-room MMA (Yang-Werner-Dumont 2002) for independent verification.

Written WITHOUT looking at the main dialog's ``mma_comparator.py``. This is an
independent re-implementation against the JSAC 2002 paper formulas, structured
to be symmetric with ``cb1_cell_runner.standard_cma_godard_with_z`` (same
block-wise update shape, same divergence criteria, same window geometry).

Formulas (Yang-Werner-Dumont, JSAC 2002, Eq. 7-9):

    J   = E[(y_R^2 - R_R^2)^2 + (y_I^2 - R_I^2)^2]

The gradient of J w.r.t. each equalizer weight w can be derived in either
the real-axis error form or, equivalently, the complex-error form. Using the
standard chain rule (see e.g. Yuan-Tsai 2005, Sikdar 2004 derivations):

    dJ/dw* = -[
        (y_R^2 - R_R^2) * y_R          (real-axis error term, multiplied by Re input)
      + j*(y_I^2 - R_I^2) * y_I        (imag-axis error term, multiplied by Im input)
    ] * conj(x)

so the stochastic/block gradient update is

    w <- w + mu * mean_k[ e_k * conj(x_k) ],   with

    e_k = (y_R^2 - R_R^2) * y_R + j * (y_I^2 - R_I^2) * y_I

The minus sign from dJ/dw* is absorbed by the descent direction ``+=``: we
minimize J, so we move opposite the gradient of J (or, equivalently, along the
gradient of -J, which is +e * conj(x)). This matches the Godard-with-z sign
convention used by ``standard_cma_godard_with_z`` which writes ``w += mu *
mean(e * z * conj(r))`` with e = (R2 - |z|^2) (already negated).

For dual-pol 2x2 MIMO we keep four filters (wxx, wxy, wyx, wyy) with the same
output convention as CMA: y_X = wxx*x + wxy*y, y_Y = wyx*x + wyy*y. The X-row
filter is driven by the X-output error, the Y-row filter by the Y-output error
— exactly mirroring CMA's row-wise error assignment.

Square 16QAM (avg-power-normalized) dispersion constants:

    R_R^2 = R_I^2 = E[|Re(s)|^4] / E[|Re(s)|^2]

For the {±1, ±3} per-axis alphabet of avg-power-1 16QAM (each axis takes the
four values ±1, ±3 with equal probability but the constellation is normalized
so the average |s|^2 = 1; per-axis the average Re^2 = 0.5):

    E[Re^2] = 0.5 (since E[|s|^2] = 1 and symmetry splits power half/half)
    E[Re^4] = 0.5 * (1^2 + 3^2 + 1^2 + 3^2) / 4 ... but per the standard MMA
    square-QAM formula:

        R_R^2 = E[Re^4]/E[Re^2]

    For avg-power-1 16QAM, the per-axis alphabet is {±1/√10, ±3/√10}*√10=...
    Actually the canonical derivation for square M-QAM is

        R^2_M = E[|Re(s)|^4] / E[|Re(s)|^2]

    which for 16QAM with avg power 1 evaluates to 1.32 for the modulus-based
    CMA constant (R_CMA^2 = E[|s|^4]/E[|s|^2] = 1.32). For MMA's *per-axis*
    constants, the standard reference value for normalized 16QAM is

        R_R^2 = R_I^2 = 0.82   (Yang-Werner 2002 table; for square QAM)

We adopt R_R^2 = R_I^2 = 0.82 per the task brief.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def mma_yang_werner_dumont_cleanroom(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    R_R2: float = 0.82,
    R_I2: float = 0.82,
    block_size: int = 64,
    norm_thresh_factor: float = 10.0,
    z_amp_thresh: float = 1e3,
) -> dict[str, Any]:
    """Clean-room blockwise MMA (Yang-Werner-Dumont 2002) on dual-pol input.

    Structurally symmetric to ``cb1_cell_runner.standard_cma_godard_with_z``:
    same center-tap init, same sliding-window block grouping, same block-end
    weight update, same divergence criteria, same output alignment. The only
    difference is the cost: MMA minimizes the dispersion of the squared real
    and imaginary parts independently, vs CMA which minimizes the dispersion
    of |y|^2.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    block_size = int(block_size)

    # Center-tap initialization (matches CMA reference exactly)
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    init_norm = _wnorm()

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)
    trace: list[dict[str, Any]] = []

    norm_thresh = norm_thresh_factor * init_norm

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

        # Intra-block filter with fixed weights (same as CMA)
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        # Write to output aligned at s+half (same as CMA)
        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # MMA block-end gradient (Yang-Werner-Dumont 2002)
        #   e_k = (y_R^2 - R_R^2) * y_R  + j * (y_I^2 - R_I^2) * y_I
        # The descent update is w += mu * mean(e_k * conj(x_k)), matching the
        # sign convention of standard_cma_godard_with_z (which uses
        # e = (R^2 - |z|^2) with +=, i.e. the negation is baked into e).
        zx_R = zx_blk.real
        zx_I = zx_blk.imag
        zy_R = zy_blk.real
        zy_I = zy_blk.imag

        eX = (zx_R ** 2 - R_R2) * zx_R + 1j * (zx_I ** 2 - R_I2) * zx_I
        eY = (zy_R ** 2 - R_R2) * zy_R + 1j * (zy_I ** 2 - R_I2) * zy_I

        wxx += mu * np.mean((eX)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + block_size),
            "mma_cost": float(np.mean(
                (zx_R ** 2 - R_R2) ** 2 + (zx_I ** 2 - R_I2) ** 2
                + (zy_R ** 2 - R_R2) ** 2 + (zy_I ** 2 - R_I2) ** 2
            )),
            "output_power": float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2)),
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
        "provenance": {
            "implementation": "verifier_mma.mma_yang_werner_dumont_cleanroom",
            "gradient": "Yang-Werner-Dumont 2002 (per-axis dispersion, squared)",
            "R_R2": R_R2,
            "R_I2": R_I2,
        },
    }


__all__ = ["mma_yang_werner_dumont_cleanroom"]
