"""CB1 modulation-generic closure evaluators — 16QAM versions of the P03 probes.

This module is modulation-aware: it provides the same four probes P03's
``probe_evaluator.py`` provides for QPSK, but for 16QAM. The P03 affine-fit
machinery (``_affine_fit`` / ``_affine_apply``) is reused verbatim by importing
it read-only from the protected P03 evaluator; nothing in P03 is modified.

Comparators (all same-information, no ML):

* ``hard_16qam(z)`` — nearest-16QAM hard decision. Same information as the
  z-stream; the modulation alphabet is public knowledge.
* ``blind_affine_compare_16qam(z_calib, z_eval, ridge)`` — one-step complex
  2x2 affine fit using z-derived 16QAM pseudo-labels only. The strongest legal
  preregistered same-information simple comparator.
* ``oracle_affine_bound_16qam`` — evaluation-only affine upper bound fit to TX
  truth. SCORING-ONLY Kill tool (FR-21); never a runtime comparator and never
  a Go baseline (FR-25). It defines the visible headroom gap.
* ``evaluate_dual_16qam(z_x, z_y, s_x, s_y)`` — permutation- and quadrant-
  invariant dual-pol evaluator. For 16QAM there are 4 quadrant rotations
  {+1, +j, -1, -j} that preserve the square constellation (16QAM has 90-degree
  rotational symmetry), and the 2! stream permutation, giving 8 candidate
  assignments. Picks the min over (BER, SER).

BER is per-bit (4 bits/symbol for 16QAM); SER is per-symbol. Both reported,
plus ``pi_assignment`` and the chosen rotations.

Provenance: campaign-contract.v1.yaml ``statistical_preregistration_template``;
P03 stage-a-contract.v1.yaml ``strongest_legal_non_ml_baseline``.
"""

from __future__ import annotations

import importlib.util
import sys
from itertools import permutations
from pathlib import Path
from typing import Any

import numpy as np


# --- Locate the P03 probe_evaluator.py once (read-only import) ----------------
# We resolve it relative to this file so the import survives regardless of the
# caller's CWD. P03's probe_evaluator.py exposes ``_affine_fit`` / ``_affine_apply``.
_HERE = Path(__file__).resolve()
# _HERE = .../scout/cb1-modulation-generic-closure/baseline-atlas/cb1_evaluator.py
# parents[0]=baseline-atlas, [1]=cb1-modulation-generic-closure, [2]=scout
_SCOUT_ROOT = _HERE.parents[2]
_P03_EVALUATOR_PATH = _SCOUT_ROOT / "P03-U19-residual-headroom" / "probe_evaluator.py"


def _load_p03_evaluator():
    if not _P03_EVALUATOR_PATH.exists():
        raise FileNotFoundError(f"P03 probe_evaluator.py not found at {_P03_EVALUATOR_PATH}")
    spec = importlib.util.spec_from_file_location("cb1_p03_probe_evaluator", _P03_EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load P03 evaluator from {_P03_EVALUATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["cb1_p03_probe_evaluator"] = module
    spec.loader.exec_module(module)
    return module


_P03 = _load_p03_evaluator()
_affine_fit = _P03._affine_fit
_affine_apply = _P03._affine_apply


# --- Modulation-aware probes -------------------------------------------------

# 16QAM has 90-degree rotational symmetry: rotations {+1, +j, -1, -j} map the
# square constellation onto itself. (Compare QPSK, which has the same four-fold
# symmetry; both are square constellations. 16QAM is NOT invariant under 45
# degree rotation — that would map vertices off the constellation grid.)
ROTATIONS_16QAM = np.asarray([1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j, 0.0 - 1.0j])


def hard_16qam(samples: np.ndarray) -> np.ndarray:
    """Nearest-16QAM hard decision using ``_modulation.hard_decision(mod='qam16')``.

    Returns the on-grid symbol estimate (avg-power-normalized). Same information
    content as the z-stream: only the (public) 16QAM alphabet is used.
    """
    # Import lazily so this module does not require projects/simulation on the
    # path at import time; the cell runner ensures it is present at call time.
    from common._modulation import hard_decision
    return np.asarray(hard_decision(np.asarray(samples, dtype=np.complex128), mod="qam16"), dtype=np.complex128)


def _bits_from_16qam(symbols: np.ndarray, truth_bits: np.ndarray) -> np.ndarray:
    """Demap 16QAM symbols to 4 bits/symbol and return int8 bit vector.

    Used for per-bit BER. The truth bits are the generator's TX bitsX/TX bitsY.
    """
    from common._modulation import qam16_demod
    decided_bits = qam16_demod(np.asarray(symbols, dtype=np.complex128))
    return (decided_bits != np.asarray(truth_bits, dtype=int)).astype(np.int8)


def _ser_16qam(symbols: np.ndarray, truth_symbols: np.ndarray) -> float:
    """Per-symbol error rate against on-grid TX truth (both 16QAM-normalized)."""
    decided = hard_16qam(symbols)
    return float(np.mean(decided != np.asarray(truth_symbols, dtype=np.complex128)))


def blind_affine_compare_16qam(
    z_calibration: np.ndarray, z_evaluation: np.ndarray, *, ridge: float
) -> dict[str, Any]:
    """One-step complex 2x2 affine fit using z-derived 16QAM pseudo-labels only.

    Mirrors P03 ``blind_affine_compare`` exactly, except pseudo-labels are
    ``hard_16qam`` instead of ``hard_qpsk``. The fit is a single closed-form
    ridge-regularized least squares on the calibration slice; the same
    coefficients are then applied to the evaluation slice.

    Runtime inputs: the calibration z, the evaluation z, and the known 16QAM
    alphabet. No TX truth is consumed.
    """
    calibration = np.asarray(z_calibration, dtype=np.complex128)
    pseudo_labels = hard_16qam(calibration)
    coefficients = _affine_fit(calibration, pseudo_labels, ridge)
    corrected = _affine_apply(z_evaluation, coefficients)
    return {
        "corrected": corrected,
        "predicted": hard_16qam(corrected),
        "coefficients": coefficients,
        "runtime_inputs": ["z_calibration", "z_evaluation", "known_16QAM_alphabet"],
        "receiver_state_changed": False,
    }


def oracle_affine_bound_16qam(
    z_calibration: np.ndarray,
    z_evaluation: np.ndarray,
    truth_calibration: np.ndarray,
    *,
    ridge: float,
) -> np.ndarray:
    """Evaluation-only affine upper bound (modulation-agnostic, same as P03).

    Fits a complex 2x2 affine map from calibration z to calibration TX truth
    and applies it to the evaluation z. SCORING ONLY: callers must never expose
    the coefficients at runtime, and this must never be reported as a Go
    baseline (FR-21 Kill tool, FR-25). Defines the visible-headroom gap.
    """
    coefficients = _affine_fit(z_calibration, truth_calibration, ridge)
    return _affine_apply(z_evaluation, coefficients)


def _best_stream_metrics_16qam(
    output: np.ndarray, truth_symbols: np.ndarray, truth_bits: np.ndarray
) -> tuple[float, float, complex]:
    """Pick the quadrant rotation that minimizes (BER, SER) for one stream.

    For 16QAM the four rotations {+1, +j, -1, -j} preserve the square
    constellation, so the receiver must resolve the 4-fold quadrant ambiguity
    (permutation-invariant evaluation).
    """
    out = np.asarray(output, dtype=np.complex128)
    best: tuple[float, float, complex] | None = None
    for rotation in ROTATIONS_16QAM:
        decided = hard_16qam(out * rotation)
        ber = float(np.mean(_bits_from_16qam(decided, truth_bits)))
        ser = float(np.mean(decided != np.asarray(truth_symbols, dtype=np.complex128)))
        candidate = (ber, ser, complex(rotation))
        if best is None or (candidate[0], candidate[1]) < (best[0], best[1]):
            best = candidate
    assert best is not None
    return best


def evaluate_dual_16qam(
    z_x: np.ndarray,
    z_y: np.ndarray,
    s_x: np.ndarray,
    s_y: np.ndarray,
    bits_x: np.ndarray,
    bits_y: np.ndarray,
) -> dict[str, Any]:
    """Permutation- and quadrant-invariant dual-pol 16QAM evaluator.

    Searches the 8 candidates = (2! stream permutations) x (4 quadrant
    rotations per stream) and reports fixed-label and PI (permutation-
    invariant) BER/SER separately, plus the chosen assignment and rotations.

    Parameters
    ----------
    z_x, z_y : (N,) complex
        Receiver-equalized streams for the two polarizations (eval slice).
    s_x, s_y : (N,) complex
        TX truth symbols for the two polarizations (eval slice).
    bits_x, bits_y : (4N,) int
        TX truth bits (4 bits/symbol) for the two polarizations (eval slice).

    Returns
    -------
    dict with keys: ``fixed_label_ber``, ``pi_ber``, ``fixed_label_ser``,
    ``pi_ser``, ``pi_assignment``, ``fixed_rotations``, ``pi_rotations``.
    """
    outputs = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))
    bit_src = (np.asarray(bits_x), np.asarray(bits_y))
    if any(v.ndim != 1 for v in (*outputs, *sources, *bit_src)):
        raise ValueError("dual 16QAM evaluator requires one-dimensional streams")
    n_sym = len(outputs[0])
    if not (len(outputs[1]) == n_sym and len(sources[0]) == n_sym and len(sources[1]) == n_sym):
        raise ValueError("dual 16QAM evaluator streams must have equal length")
    if not (len(bit_src[0]) == 4 * n_sym and len(bit_src[1]) == 4 * n_sym):
        raise ValueError("TX bits must be 4 bits/symbol for 16QAM (len = 4 * N)")

    candidates = []
    for assignment in permutations((0, 1)):
        per_output = [
            _best_stream_metrics_16qam(
                outputs[index],
                sources[assignment[index]],
                bit_src[assignment[index]],
            )
            for index in range(2)
        ]
        candidates.append({
            "assignment": assignment,
            "ber": float(np.mean([row[0] for row in per_output])),
            "ser": float(np.mean([row[1] for row in per_output])),
            "rotations": [[float(row[2].real), float(row[2].imag)] for row in per_output],
        })
    fixed = next(row for row in candidates if row["assignment"] == (0, 1))
    invariant = min(candidates, key=lambda row: (row["ber"], row["ser"], row["assignment"]))
    return {
        "fixed_label_ber": fixed["ber"],
        "pi_ber": invariant["ber"],
        "fixed_label_ser": fixed["ser"],
        "pi_ser": invariant["ser"],
        "pi_assignment": ["sX" if index == 0 else "sY" for index in invariant["assignment"]],
        "fixed_rotations": fixed["rotations"],
        "pi_rotations": invariant["rotations"],
    }


__all__ = [
    "ROTATIONS_16QAM",
    "hard_16qam",
    "blind_affine_compare_16qam",
    "oracle_affine_bound_16qam",
    "evaluate_dual_16qam",
]
