"""C15 reduced-constellation / ring-aware CMA cost variants.

This module implements TWO candidate equalizer cost functions for the C15
Scout, plus a Godard wrapper used only as an identity reference. All three
share the EXACT SAME butterfly 2x2 blockwise structure, center-tap init,
divergence criteria, and eval-window geometry as the anchor
``cb1_cell_runner.standard_cma_godard_with_z``. ONLY the cost function differs.

Cost-isolation discipline (contract ``frozen_common_axes.note``):
  The block-end gradient has the Godard-with-z form
      Δw ∝ mean_blk[ (R2(z) - |z|^2) · z · conj(r) ]
  The anchor uses a single global R2. The candidates change ONLY how R2(z)
  (and, for RCCMA, the update mask) is computed from |z|. Nothing else moves.

Concept provenance (contract ``provenance.concept_source_reduced_constellation``):
  * Sato 1975 (IEEE TCOM) — reduced-constellation cost (RCCMA = outer-ring-only).
  * Yang-Werner-Dumont 2002 (IEEE JSAC) — MMA, quadrant-aware (tested D006/D040,
    FAILED). The ring-aware cost here is DISTINCT: radius-decomposed, not angle.
  * Godard 1980 (IEEE TCOM Eq.(10)) — single-global-R2 anchor.

16QAM ring geometry (avg-power-normalized, E[|s|^2]=1):
  inner  ring: |s|^2 = 2/10 = 0.2  (4 corner-of-inner-square symbols)
  middle ring: |s|^2 = 10/10 = 1.0  (8 edge symbols)
  outer  ring: |s|^2 = 18/10 = 1.8  (4 corner symbols)
  Ring boundaries (midpoints in |z|^2): 0.6 (inner/middle), 1.4 (middle/outer).

No TX truth is read by any candidate: the ring assignment and the RCCMA mask
use ONLY |z| (receiver-visible). Verified by test_cost_identity.py.
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ─── 16QAM ring geometry (avg-power-normalized) ──────────────────────────────

# Squared radii of the three 16QAM rings, ascending.
RING_SQ_RADII_16QAM = np.asarray([0.2, 1.0, 1.8], dtype=np.float64)
# Midpoints in |z|^2 between adjacent rings (the nearest-ring decision boundaries).
RING_BOUNDARIES_SQ_16QAM = np.asarray([0.6, 1.4], dtype=np.float64)
# RCCMA outer-ring threshold (symbols with |z|^2 >= this drive the update).
RCCMA_OUTER_THRESHOLD_SQ = 1.4
RCCMA_OUTER_R2 = 1.8


def nearest_ring_sq_radius(z2: np.ndarray) -> np.ndarray:
    """Per-symbol R2(z) = squared radius of the nearest 16QAM ring.

    Receiver-visible: uses only |z|^2. For each entry of ``z2 = |z|^2``:
      z2 < 0.6            -> 0.2  (inner ring)
      0.6 <= z2 < 1.4     -> 1.0  (middle ring)
      z2 >= 1.4           -> 1.8  (outer ring)
    """
    z2 = np.asarray(z2, dtype=np.float64)
    out = np.empty_like(z2)
    # np.select picks the first True condition; order inner/middle/outer.
    out = np.where(z2 < RING_BOUNDARIES_SQ_16QAM[0], RING_SQ_RADII_16QAM[0],
          np.where(z2 < RING_BOUNDARIES_SQ_16QAM[1], RING_SQ_RADII_16QAM[1],
                   RING_SQ_RADII_16QAM[2]))
    return out


def outer_ring_mask(z2: np.ndarray) -> np.ndarray:
    """Boolean mask: True where |z|^2 >= RCCMA outer threshold (outer ring)."""
    z2 = np.asarray(z2, dtype=np.float64)
    return z2 >= RCCMA_OUTER_THRESHOLD_SQ


# ─── Generic blockwise equalizer (faithful generalization of the anchor) ─────
#
# This engine is a faithful generalization of
# ``cb1_cell_runner.standard_cma_godard_with_z``: same init, same sliding-window
# block loop, same intra-block filter, same output alignment, same divergence
# criteria, same trace schema. The ONLY parameterized piece is the per-block
# cost, expressed as (a) a per-symbol R2 array R2(z) and (b) an optional
# per-symbol update mask. With R2(z) = const and mask = None this reproduces the
# Godard anchor byte-for-byte (verified by the identity test
# ``test_godard_wrapper_byte_identical_to_anchor``).

def _blockwise_equalizer(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
    r2_of_z2: Callable[[np.ndarray], np.ndarray],
    mask_of_z2: Callable[[np.ndarray], np.ndarray] | None = None,
    cost_name: str,
    gradient_stamp: str,
) -> dict[str, Any]:
    """Run the blockwise Godard-with-z equalizer with a parameterized cost.

    The per-block cost is defined by ``r2_of_z2`` (per-symbol R2 array) and an
    optional ``mask_of_z2`` (boolean per-symbol update mask; None = all symbols).
    Everything else is identical to the Godard anchor.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    block_size = int(block_size)

    # Center-tap initialization (prompt013:335-337, _cma.py:80-86, Qin 2025 L283)
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

    # Divergence criteria (TL-20, _cma.py:132-134) — IDENTICAL to the anchor.
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

        # Intra-block filter with fixed weights (prompt013:377-378, Eq.28)
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        # Write to output aligned at s+half (prompt013:369, _cma.py:155)
        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # ── COST-SPECIFIC PIECE (the ONLY thing that differs) ────────────────
        # Godard-with-z gradient form: Δw ∝ mean_blk[ (R2(z) - |z|^2) · z · conj(r) ]
        # The anchor uses a single global R2; here R2(z) is per-symbol (and,
        # for RCCMA, the mean is over the masked outer-ring subset only).
        z2x = np.abs(zx_blk) ** 2
        z2y = np.abs(zy_blk) ** 2
        R2x = r2_of_z2(z2x)            # per-symbol R2 array (block,)
        R2y = r2_of_z2(z2y)
        eX = R2x - z2x                  # per-symbol error (block,)
        eY = R2y - z2y

        if mask_of_z2 is None:
            # Standard Godard-with-z block-end mean (anchor form).
            gwxx = np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            gwyx = np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
            gwxy = np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
            gwyy = np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)
            cm_err = float(np.mean(eX ** 2 + eY ** 2))
            n_active_x = n_active_y = int(block_size)
        else:
            # RCCMA: mean over the masked (outer-ring) subset only.
            mx = mask_of_z2(z2x)
            my = mask_of_z2(z2y)
            n_active_x = int(np.sum(mx))
            n_active_y = int(np.sum(my))
            gwxx = (np.mean((eX * zx_blk)[mx, None] * np.conj(rX_blk)[mx], axis=0)
                    if n_active_x > 0 else np.zeros(L, dtype=complex))
            gwxy = (np.mean((eX * zx_blk)[mx, None] * np.conj(rY_blk)[mx], axis=0)
                    if n_active_x > 0 else np.zeros(L, dtype=complex))
            gwyx = (np.mean((eY * zy_blk)[my, None] * np.conj(rX_blk)[my], axis=0)
                    if n_active_y > 0 else np.zeros(L, dtype=complex))
            gwyy = (np.mean((eY * zy_blk)[my, None] * np.conj(rY_blk)[my], axis=0)
                    if n_active_y > 0 else np.zeros(L, dtype=complex))
            # cm_error reported over active symbols (0 if none active this block).
            if n_active_x + n_active_y > 0:
                cm_err = float(np.mean(
                    np.concatenate([eX[mx] ** 2, eY[my] ** 2])
                    if (n_active_x > 0 and n_active_y > 0)
                    else (eX[mx] ** 2 if n_active_x > 0 else eY[my] ** 2)
                ))
            else:
                cm_err = 0.0
        # ─────────────────────────────────────────────────────────────────────

        wxx += mu * gwxx
        wxy += mu * gwxy
        wyx += mu * gwyx
        wyy += mu * gwyy

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + block_size),
            "cost_name": cost_name,
            "cm_error": cm_err,
            "output_power": float(np.mean(z2x + z2y)),
            "update_norm": float(np.sqrt(
                np.sum(np.abs(mu * gwxx) ** 2) + np.sum(np.abs(mu * gwxy) ** 2)
                + np.sum(np.abs(mu * gwyx) ** 2) + np.sum(np.abs(mu * gwyy) ** 2)
            )),
            "w_norm": cur_norm,
            "z_amp_max": cur_zamp,
            "n_active_x": n_active_x,
            "n_active_y": n_active_y,
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
        "cost_name": cost_name,
        "provenance": {
            "implementation": f"cma_cost_variants.{cost_name}",
            "entry": "blockwise Godard-with-z with parameterized cost (c15 engine)",
            "gradient": gradient_stamp,
            "cost": cost_name,
        },
    }


# ─── Candidate 0 (identity reference only): Godard via the generic engine ────

def cma_godard(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    R2: float = 1.0,
    block_size: int = 64,
) -> dict[str, Any]:
    """Godard cost via the generic engine. IDENTITY REFERENCE ONLY.

    With a single global R2 this is byte-identical to the anchor
    ``standard_cma_godard_with_z``. The identity test proves the engine is
    faithful to the anchor; the Scout itself uses the READ-ONLY anchor import
    for the Godard comparator (so the anchor provenance stamp is the protected
    one). This wrapper exists solely to certify the engine.
    """
    r2_of_z2 = lambda z2: np.full_like(np.asarray(z2, dtype=np.float64), float(R2))
    return _blockwise_equalizer(
        rX, rY, n_tap=n_tap, mu=mu, block_size=block_size,
        r2_of_z2=r2_of_z2, mask_of_z2=None,
        cost_name="godard", gradient_stamp="Godard-with-z",
    )


# ─── Candidate 1: ring-aware cost ────────────────────────────────────────────

def cma_ring_aware(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
) -> dict[str, Any]:
    """Ring-aware Godard-with-z: R2(z) = nearest 16QAM ring squared radius.

    The cost is e = R2(z) - |z|^2 where R2(z) is the squared radius of the
    nearest 16QAM ring (receiver-visible, from |z| only). This matches the
    cost to 16QAM's actual three-ring geometry instead of pulling every symbol
    toward one global circle.

    Structure (init, butterfly, block loop, divergence, eval window) is
    IDENTICAL to the Godard anchor; only R2 becomes per-symbol.
    """
    return _blockwise_equalizer(
        rX, rY, n_tap=n_tap, mu=mu, block_size=block_size,
        r2_of_z2=nearest_ring_sq_radius, mask_of_z2=None,
        cost_name="ring_aware",
        gradient_stamp="Godard-with-z (ring-aware R2(z))",
    )


# ─── Candidate 2: reduced-constellation CMA (RCCMA, Sato-style) ──────────────

def cma_rccma(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
) -> dict[str, Any]:
    """Reduced-Constellation CMA (Sato 1975 style) for square 16QAM.

    Only OUTER-ring symbols (|z|^2 >= 1.4) drive the block-end gradient; inner
    and middle symbols contribute ZERO update. The outer ring is constant-
    modulus (|s|^2 = 1.8 for all 4 outer symbols), so the Godard cost on it is
    well-defined with the single R2_outer = 1.8.

    Structure is IDENTICAL to the Godard anchor; only the update is masked to
    the outer-ring subset (and R2 = 1.8 on that subset).
    """
    r2_of_z2 = lambda z2: np.full_like(np.asarray(z2, dtype=np.float64), RCCMA_OUTER_R2)
    return _blockwise_equalizer(
        rX, rY, n_tap=n_tap, mu=mu, block_size=block_size,
        r2_of_z2=r2_of_z2, mask_of_z2=outer_ring_mask,
        cost_name="rccma",
        gradient_stamp="Godard-with-z (RCCMA outer-ring masked)",
    )


__all__ = [
    "RING_SQ_RADII_16QAM",
    "RING_BOUNDARIES_SQ_16QAM",
    "RCCMA_OUTER_THRESHOLD_SQ",
    "RCCMA_OUTER_R2",
    "nearest_ring_sq_radius",
    "outer_ring_mask",
    "cma_godard",
    "cma_ring_aware",
    "cma_rccma",
]
