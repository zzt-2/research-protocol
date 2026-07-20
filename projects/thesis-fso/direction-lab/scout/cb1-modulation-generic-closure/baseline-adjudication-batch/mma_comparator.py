"""Multi-Modulus Algorithm (MMA) comparator for CB1 baseline adjudication.

This module implements the **Multi-Modulus Algorithm of Yang, Werner, Dumont
(JSAC 2002)** as a same-information same-budget Go comparator against the
existing standard-CMA (Godard-with-z) diagnostic anchor.

It is the main Go comparator of the CB1 baseline-adjudication shared batch
(``batch-contract.v1.yaml``). It adjudicates whether the CB1 16QAM Atlas v1
inner-ring collapse headroom (max 0.333, 10/11 cells >= MDE) survives a
widely-adopted, task-appropriate conventional baseline.

Identity gate
-------------
Per Yang-Werner-Dumont 2002 §III-A, the MMA cost is

    J_MMA = E[ (y_R^2 - R_R^2)^2 + (y_I^2 - R_I^2)^2 ]

with dispersion constants

    R_R^2 = E[ s_R^4 ] / E[ s_R^2 ],   R_I^2 = E[ s_I^4 ] / E[ s_I^2 ].

The per-sample gradient w.r.t. the complex equalizer output y = w^H x is

    dJ/dw* = -2 [ (y_R^2 - R_R^2) * y_R + j (y_I^2 - R_I^2) * y_I ] * x*

so the stochastic block-end weight update (blockwise, parallelization=64,
mirroring ``standard_cma_godard_with_z`` for information and budget parity) is

    Delta_w ∝ mu * mean_block{ [ (y_R^2 - R_R^2) * y_R + j (y_I^2 - R_I^2) * y_I ] * conj(x) }

which is exactly the same update structure as the CMA anchor with the scalar
modulus error (R^2 - |z|^2) * z replaced by the per-axis modulus error
(y_R^2 - R_R^2) * y_R + j (y_I^2 - R_I^2) * y_I.

Square 16QAM reduction
----------------------
For the standard square 16QAM constellation with per-axis symbols
{-3,-1,+1,+3}/sqrt(10) (unit average power):

    E[x^2] = (9+1+1+9)/40 = 0.5
    E[x^4] = (81+1+1+81)/400 = 0.41
    R_R^2 = R_I^2 = 0.41/0.5 = 0.82

Verified numerically in this repo; matches Mendes-Filho+SSP2009, Akande-Joya
EURASIP 2016, and "Multi-Modulus Blind Equalizations for QAM" (RROIJ).

Dual-polarisation
-----------------
Per Kikuchi JLT 2016 §IV.B and Fludger OFC 2014 W3K.2, dual-pol MMA applies
the single-pol MMA cost to each polarization with a 2x2 complex MIMO tap
structure (4 filters w_xx, w_xy, w_yx, w_yy). No new cost function — the
same structure as ``standard_cma_godard_with_z`` with per-axis modulus
errors replacing the scalar modulus error.

Why MMA is task-correct for 16QAM
--------------------------------
Single-modulus CMA's single R^2 = 1.32 is incompatible with 16QAM's three
distinct |s|^2 values (0.2 inner, 1.0 mid, 1.8 outer); the Godard cost
surface has spurious local minima where the equalizer collapses to the
inner ring (|z|^2 -> 0.2), which is the CB1 Atlas v1 failure mode (Johnson
PIEEE 1998 §III-IV; Mendes-Filho SSP 2009 intro; Liu 2021 intro). MMA's
split real/imag modulus removes this pathology because R_R^2 = R_I^2 = 0.82
sits between the inner (1^2/10 = 0.1) and outer (3^2/10 = 0.9) per-axis
distances, structurally preventing the per-axis collapse. MMA is the fiber-
coherent standard for DP-16QAM blind demultiplexing (Kikuchi JLT 2016;
Fludger OFC 2014) and has been used in photonics-assisted FSO links (Pang
2022).

Not SOTA: this is the basic MMA without DD-LMS cascade, RLS, or neural
enhancements. Per baseline-adjudication reference, adequacy not prestige.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ─── Multi-Modulus Algorithm (Yang-Werner-Dumont 2002) ────────────────────────

def mma_yang_werner_dumont(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    R_R2: float = 0.82,
    R_I2: float = 0.82,
    block_size: int = 64,
) -> dict[str, Any]:
    """Run dual-pol MMA (Yang-Werner-Dumont 2002) blockwise.

    Blockwise filter with fixed intra-block weights, block-end gradient
    update using the MMA gradient

        Delta_w ∝ mu * mean_block{
            [ (y_R^2 - R_R^2) * y_R + j (y_I^2 - R_I^2) * y_I ] * conj(r)
        }

    Same block structure, initialization, divergence criteria, and trace
    output as ``cb1_cell_runner.standard_cma_godard_with_z`` for information
    and budget parity.

    Returns the full zX/zY traces (length N), divergence flags, the block
    trace, and the identity-gate provenance stamp.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    block_size = int(block_size)

    # Center-tap initialization — IDENTICAL to standard_cma_godard_with_z
    # (information and budget parity; only the cost function differs).
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

    # Divergence criteria — IDENTICAL to standard_cma_godard_with_z.
    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3

    diverged = False
    diverge_idx = None

    rX_win = sliding_window_view(rX, L)
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

        # Intra-block filter with fixed weights (Eq.28 structure, sat.1553).
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        # Write to output aligned at s+half (matches CMA anchor geometry).
        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # MMA per-axis modulus error (Yang-Werner-Dumont 2002 Eq.(12)-(13)).
        # e_per_axis(y) = (y_R^2 - R_R^2) * y_R + j (y_I^2 - R_I^2) * y_I
        # This is the MMA analogue of the CMA scalar error (R^2 - |z|^2) * z.
        def _mma_error(z_blk: np.ndarray) -> np.ndarray:
            zR = z_blk.real
            zI = z_blk.imag
            return (zR ** 2 - R_R2) * zR + 1j * (zI ** 2 - R_I2) * zI

        eX = _mma_error(zx_blk)
        eY = _mma_error(zy_blk)

        # Block-end gradient update — same structure as CMA anchor.
        wxx += mu * np.mean((eX)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))

        # MMA cost trace for diagnostics (per-axis, summed across pols).
        # J_MMA instantaneous = (yR^2 - R_R^2)^2 + (yI^2 - R_I^2)^2
        cost_x = float(np.mean(
            (zx_blk.real ** 2 - R_R2) ** 2 + (zx_blk.imag ** 2 - R_I2) ** 2
        ))
        cost_y = float(np.mean(
            (zy_blk.real ** 2 - R_R2) ** 2 + (zy_blk.imag ** 2 - R_I2) ** 2
        ))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + block_size),
            "mma_cost_x": cost_x,
            "mma_cost_y": cost_y,
            "output_power": float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2)),
            "update_norm": float(np.sqrt(
                np.sum(np.abs(mu * np.mean((eX)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eX)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
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
        # Identity-gate stamp: MMA cost = Yang-Werner-Dumont 2002.
        "provenance": {
            "implementation": "mma_comparator.mma_yang_werner_dumont",
            "entry": "blockwise dual-pol MMA (Yang-Werner-Dumont JSAC 2002 §III-A)",
            "gradient": "Yang-Werner-Dumont MMA",
            "R_R2": float(R_R2),
            "R_I2": float(R_I2),
        },
    }


# ─── Sanity check helpers (used by tests/test_mma_identity.py) ────────────────

def mma_dispersion_constants_sq_qam16() -> tuple[float, float]:
    """Return (R_R^2, R_I^2) for the project's square 16QAM constellation.

    Per-axis amplitudes {-3,-1,+1,+3}/sqrt(10):
        E[x^2] = (9+1+1+9)/40 = 0.5
        E[x^4] = (81+1+1+81)/400 = 0.41
        R_R^2 = E[x^4]/E[x^2] = 0.82

    Equal R_R^2 and R_I^2 because the constellation is square.
    """
    x = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
    E_x2 = float(np.mean(x ** 2))
    E_x4 = float(np.mean(x ** 4))
    R_R2 = E_x4 / E_x2
    R_I2 = R_R2  # square
    return R_R2, R_I2


__all__ = [
    "mma_yang_werner_dumont",
    "mma_dispersion_constants_sq_qam16",
]
