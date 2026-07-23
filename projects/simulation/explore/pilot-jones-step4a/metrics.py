"""Metrics for dual-polarization QPSK pilot-Jones evaluation.

Reimplementation (not copy) of the canonical fixed-label / permutation-invariant
BER used by the source worktree `common/_batch_metrics.py`. Kept here so the
closure is self-contained on the current branch and does not depend on the
read-only source worktree.

- fixed_label_ber : per-stream 4-rotation phase-corrected hard-decision BER,
  averaged over X and Y. This is the receiver-visible score BEFORE any
  permutation disambiguation; it counts a polarization swap as BER=0.5.
- pi_ber        : best BER over 2! x 4 x 4 (swap X/Y) x (4 phases) x (4 phases).
  This is the permutation-invariant floor achievable WITH a frame-header /
  stream-identification cost (NOT free -- must be reported alongside fixed).
"""
from __future__ import annotations
import numpy as np


def _ber(tx: np.ndarray, rx: np.ndarray) -> float:
    tx = np.asarray(tx)
    rx = np.asarray(rx)
    tx_bits = np.stack((np.real(tx) < 0, np.imag(tx) < 0), axis=-1)
    rx_bits = np.stack((np.real(rx) < 0, np.imag(rx) < 0), axis=-1)
    return float(np.mean(tx_bits != rx_bits))


def _phase_corrected_ber(tx: np.ndarray, rx: np.ndarray) -> float:
    return min(
        _ber(tx, rx * np.exp(-1j * phase * np.pi / 2)) for phase in range(4)
    )


def evaluate_dual_qpsk(tx_x, tx_y, z_x, z_y) -> dict:
    """Fixed-label and permutation-invariant BER for paired dual-QPSK streams.

    All four inputs must be equal-length 1-D arrays of the SAME evaluation
    window (data mask already applied upstream; pilot positions excluded).
    """
    arrays = [np.asarray(a) for a in (tx_x, tx_y, z_x, z_y)]
    if any(a.ndim != 1 for a in arrays):
        raise ValueError("dual-QPSK streams must be one-dimensional")
    if len({len(a) for a in arrays}) != 1 or len(arrays[0]) == 0:
        raise ValueError("all streams must share the same non-zero length")

    fixed = (
        _phase_corrected_ber(arrays[0], arrays[2])
        + _phase_corrected_ber(arrays[1], arrays[3])
    ) / 2

    best = None
    for swapped in (False, True):
        rx0, rx1 = (arrays[3], arrays[2]) if swapped else (arrays[2], arrays[3])
        for phase_x in range(4):
            for phase_y in range(4):
                c0 = rx0 * np.exp(-1j * phase_x * np.pi / 2)
                c1 = rx1 * np.exp(-1j * phase_y * np.pi / 2)
                score = (_ber(arrays[0], c0) + _ber(arrays[1], c1)) / 2
                cand = (score, swapped, phase_x, phase_y)
                if best is None or cand < best:
                    best = cand
    score, swapped, phase_x, phase_y = best
    return {
        "fixed_label_ber": fixed,
        "pi_ber": float(score),
        "assignment": ("y", "x") if swapped else ("x", "y"),
        "phase_x": int(phase_x),
        "phase_y": int(phase_y),
    }
