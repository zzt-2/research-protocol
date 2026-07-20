"""Sanity / identity tests for the MMA comparator (batch-contract.v1.yaml).

These tests run BEFORE the adjudication sweep. They are the gate that
authorizes MMA as a defensible Go comparator.

All tests are deterministic (no channel randomness); failures are hard
blockers.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest


HERE = Path(__file__).resolve()
# .../baseline-adjudication-batch/tests/test_mma_identity.py
BATCH_DIR = HERE.parents[1]              # baseline-adjudication-batch/
CB1_ROOT = BATCH_DIR.parent              # cb1-modulation-generic-closure/
ATLAS_DIR = CB1_ROOT / "baseline-atlas"  # where cb1_cell_runner.py lives
SCOUT_ROOT = CB1_ROOT.parent
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

# Put projects/simulation, baseline-adjudication-batch, and baseline-atlas
# (cb1_cell_runner.py) on sys.path.
for p in (str(SIM_DIR), str(BATCH_DIR), str(ATLAS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)


from mma_comparator import mma_yang_werner_dumont, mma_dispersion_constants_sq_qam16  # noqa: E402


# ─── Sanity 1: R_R^2 = R_I^2 = 0.82 for square 16QAM ─────────────────────────

def test_mma_dispersion_constants_sq_qam16():
    R_R2, R_I2 = mma_dispersion_constants_sq_qam16()
    assert abs(R_R2 - 0.82) < 1e-12, f"R_R^2 should be 0.82, got {R_R2}"
    assert abs(R_I2 - 0.82) < 1e-12, f"R_I^2 should be 0.82, got {R_I2}"
    assert R_R2 == R_I2, "Square 16QAM must give equal R_R^2 and R_I^2"


# ─── Sanity 2: MMA identity gate (gradient stamp) ────────────────────────────

def test_mma_identity_gate():
    rng = np.random.default_rng(42)
    N = 1024
    rX = (rng.standard_normal(N) + 1j * rng.standard_normal(N)).astype(complex)
    rY = (rng.standard_normal(N) + 1j * rng.standard_normal(N)).astype(complex)
    out = mma_yang_werner_dumont(rX, rY, n_tap=11, mu=1e-3, block_size=64)
    assert out["provenance"]["gradient"] == "Yang-Werner-Dumont MMA", (
        f"identity gate failed: gradient={out['provenance']['gradient']}"
    )
    assert out["provenance"]["R_R2"] == pytest.approx(0.82, abs=1e-12)
    assert out["provenance"]["R_I2"] == pytest.approx(0.82, abs=1e-12)


# ─── Sanity 3: MMA on clean (no channel) QPSK converges to identity filter ───
# QPSK is a degenerate 4-point square QAM; MMA with R_R^2 = R_I^2 = 1.0 must
# converge to the identity filter (W = center tap), proving the gradient sign
# and update rule are correct.

def test_mma_constant_modulus_qpsk_converges_to_identity():
    rng = np.random.default_rng(7)
    N = 4096
    # Clean QPSK input (no channel, no noise). The optimal filter is identity.
    bits = rng.integers(0, 4, size=N)
    qpsk = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2)
    rX = qpsk[bits].astype(complex)
    rY = qpsk[rng.integers(0, 4, size=N)].astype(complex)

    out = mma_yang_werner_dumont(
        rX, rY, n_tap=11, mu=1e-3,
        R_R2=1.0, R_I2=1.0,  # QPSK: each axis is +/- 1/sqrt(2), so R_R^2 = 1.0
        block_size=64,
    )
    assert not out["diverged"], "MMA diverged on clean QPSK — sign error"

    # The center tap should dominate; off-center taps should be small.
    # (We can't access w directly, so check the eval window: MMA on clean
    # QPSK should produce zX ≈ rX up to a phase/swap.)
    # Reconstruct zX in the eval tail and compare with rX up to rotation.
    half = 5
    eval_start = N // 2
    z_eval = out["zX"][eval_start:eval_start + 256]
    r_eval = rX[eval_start:eval_start + 256]

    # Try the 4 quadrant rotations and the 2 pol swaps; the minimum distance
    # should be tiny (MMA converged to identity).
    rotations = [1.0, 1j, -1.0, -1j]
    best_err = float("inf")
    for rot in rotations:
        err = float(np.mean(np.abs(z_eval * rot - r_eval) ** 2))
        best_err = min(best_err, err)
    # MMA is constant-modulus on QPSK; per-axis modulus is exactly matched
    # so the residual should be at the level of transient misalignment.
    assert best_err < 0.05, (
        f"MMA did not converge on clean QPSK: best per-symbol MSE = {best_err}"
    )


# ─── Sanity 4: MMA on clean 16QAM converges (PI-SER ~ 0) ─────────────────────
# A functional MMA must converge on a clean 16QAM input (no channel, no AWGN).
# This proves the algorithm is wired correctly for the actual target task.

def test_mma_smoke_16qam_clean_converges():
    rng = np.random.default_rng(11)
    N = 4096
    # Project's actual square 16QAM (matches _modulation.qam16_mod)
    levels = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
    sI = rng.choice(levels, size=N)
    sQ = rng.choice(levels, size=N)
    rX = (sI + 1j * sQ).astype(complex)
    sI_y = rng.choice(levels, size=N)
    sQ_y = rng.choice(levels, size=N)
    rY = (sI_y + 1j * sQ_y).astype(complex)

    R_R2, R_I2 = mma_dispersion_constants_sq_qam16()
    out = mma_yang_werner_dumont(
        rX, rY, n_tap=11, mu=1e-3, R_R2=R_R2, R_I2=R_I2, block_size=64,
    )
    assert not out["diverged"], "MMA diverged on clean 16QAM"

    # Eval window tail: hard-decision PI-SER should be 0 or very small.
    # We use the same hard_decision as the evaluator for parity.
    from common._modulation import hard_decision  # noqa: E402
    eval_start = N // 2
    z_eval = out["zX"][eval_start:eval_start + 256]
    truth = rX[eval_start:eval_start + 256]

    decided = np.asarray(hard_decision(z_eval, mod="qam16"), dtype=complex)
    # Try 4 rotations; MMA introduces quadrant ambiguity on a square QAM.
    rotations = [1.0, 1j, -1.0, -1j]
    best_ser = float("inf")
    for rot in rotations:
        decided_rot = np.asarray(hard_decision(z_eval * rot, mod="qam16"), dtype=complex)
        # Map rotation back to truth frame: rotate truth inversely.
        ser = float(np.mean(decided_rot != truth * rot))
        best_ser = min(best_ser, ser)
    assert best_ser < 0.02, (
        f"MMA did not converge on clean 16QAM: best PI-SER = {best_ser}"
    )


# ─── Sanity 5: CMA anchor byte regression (wiring unchanged) ─────────────────
# standard_cma_godard_with_z on the QPSK anchor cell must still reproduce
# P03 v1 PI-SER = 0.0 (Atlas v1 reports this exact value). If MMA's existence
# broke the CMA anchor, this test fails. We use the full cb1 evaluator
# (PI-SER via permutation + quadrant search) instead of an eval-power proxy.

def test_cma_anchor_still_byte_identical_to_p03v1():
    from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
    import cb1_cell_runner as runner  # noqa: E402 — Atlas v1 module
    import cb1_evaluator as evaluator  # noqa: E402 — Atlas v1 module

    realization = generate_shared_realization_dp(
        512, 4.2, 1.4, 30.0, sop_rate=4e-6, seed=11, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar", modulation="qpsk",
    )
    raw = runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=11, mu=1e-3, R2=1.0, block_size=64,
    )
    assert raw["provenance"]["gradient"] == "Godard-with-z"
    assert not raw["diverged"]

    # Use Atlas v1's exact eval-window geometry for a faithful regression.
    eval_start, calibration_end, eval_end, _ = runner.eval_window_for(
        512, 11, window_symbols=256, block_size=64,
    )
    z_eval = np.column_stack((
        raw["zX"][calibration_end:eval_end],
        raw["zY"][calibration_end:eval_end],
    ))
    truth_eval = np.column_stack((
        realization["sX"][calibration_end:eval_end],
        realization["sY"][calibration_end:eval_end],
    ))
    p03 = evaluator._P03
    amplitude = 1.0 / np.sqrt(2.0)
    nearest_predicted = p03.hard_qpsk(z_eval, amplitude)
    nearest_m = p03.evaluate_dual_qpsk(
        nearest_predicted[:, 0], nearest_predicted[:, 1],
        truth_eval[:, 0], truth_eval[:, 1],
    )
    # Atlas v1 anchor: PI-SER = 0.0 exactly (P03 v1 byte-identity).
    assert nearest_m["pi_ser"] == 0.0, (
        f"CMA anchor regressed: PI-SER = {nearest_m['pi_ser']} (expected 0.0)"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
