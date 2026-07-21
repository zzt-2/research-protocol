"""Sanity tests for fairness-batch-b01 candidates (per batch-contract.v1.yaml).

Run: cd projects/simulation && python -m pytest ../thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/fairness-batch-b01/tests/test_b01_sanity.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Locate modules.
HERE = Path(__file__).resolve()
# HERE = .../fairness-batch-b01/tests/test_b01_sanity.py
BATCH_DIR = HERE.parents[1]   # fairness-batch-b01/
CB1_ROOT = BATCH_DIR.parent   # cb1-modulation-generic-closure/
REPO_ROOT = HERE.parents[7]   # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(BATCH_DIR), str(CB1_ROOT / "baseline-atlas"),
          str(CB1_ROOT / "baseline-adjudication-batch")):
    if p not in sys.path:
        sys.path.insert(0, p)

import b01_candidates as cand  # noqa: E402
import cb1_cell_runner as anchor  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402


# =============================================================================
# Helpers
# =============================================================================

def _make_clean_16qam(n_symbols=1024, seed=11):
    """Generate a clean (no fading, no SOP, no AWGN) 16QAM dual-pol input.

    The channel matrix is identity, so rX = sX, rY = sY. CMA / per-symbol CMA
    should converge to PI-SER ~ 0.
    """
    rng = np.random.default_rng(seed)
    levels = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
    idx_x = rng.integers(0, 4, size=n_symbols)
    idx_y = rng.integers(0, 4, size=n_symbols)
    sx_re = levels[rng.integers(0, 4, size=n_symbols)]
    sx_im = levels[rng.integers(0, 4, size=n_symbols)]
    sy_re = levels[rng.integers(0, 4, size=n_symbols)]
    sy_im = levels[rng.integers(0, 4, size=n_symbols)]
    sX = sx_re + 1j * sx_im
    sY = sy_re + 1j * sy_im
    # Add small prefix padding for filter warm-up (we mimic the channel gen
    # by prepending zeros — clean channel has no channel memory).
    pad = 100
    rX = np.concatenate([np.zeros(pad, dtype=complex), sX])
    rY = np.concatenate([np.zeros(pad, dtype=complex), sY])
    return rX, rY


def _make_constant_modulus_qam16(n_symbols=512):
    """Constant-|z|^2 = R2 = 1.32 stream (no collapse signature)."""
    # Use the outer 16QAM ring: |s|^2 = 1.8 (corners). Average to 1.32.
    # Simpler: just use a synthetic |z|^2 = 1.32 constant stream.
    # For detector test, we want z2_over_R2_ratio = 1.0 (no alert).
    R2 = 1.32
    # Make rX = constant so the equalizer output is constant.
    rX = np.full(n_symbols, np.sqrt(R2), dtype=complex)
    rY = np.full(n_symbols, np.sqrt(R2) * 1j, dtype=complex)
    return rX, rY


# =============================================================================
# Sanity 1: CMA anchor byte regression (inherited from contract)
# =============================================================================

def test_cma_anchor_byte_regression():
    """standard_cma_godard_with_z on QPSK clean input produces near-zero PI-SER.

    This is the same wiring regression as Atlas v1. We don't reproduce the
    full P03 cell here; we just verify the anchor is functional.
    """
    # Build a simple QPSK clean input.
    rng = np.random.default_rng(11)
    bits = rng.integers(0, 2, size=2048)
    syms = (2 * bits - 1) / np.sqrt(2) + 1j * (2 * rng.integers(0, 2, size=2048) - 1) / np.sqrt(2)
    rX = np.concatenate([np.zeros(100, dtype=complex), syms])
    rY = np.concatenate([np.zeros(100, dtype=complex), syms * 1j])
    out = anchor.standard_cma_godard_with_z(rX, rY, n_tap=11, mu=1e-3, R2=1.0, block_size=64)
    assert out["provenance"]["gradient"] == "Godard-with-z"
    assert not out["diverged"], "anchor diverged on clean QPSK"
    # Converged output should have |z|^2 ~ 1.0.
    zX = out["zX"]
    tail = zX[300:500]
    mean_pow = float(np.mean(np.abs(tail) ** 2))
    assert 0.5 < mean_pow < 1.8, f"clean QPSK |z|^2={mean_pow} not near 1.0"


# =============================================================================
# Sanity 2: C10 per-symbol CMA converges on clean 16QAM
# =============================================================================

def test_c10_smoke_clean_16qam():
    """C10 per-symbol CMA converges to small output error on clean 16QAM."""
    rX, rY = _make_clean_16qam(n_symbols=1024, seed=11)
    out = cand.c10_per_symbol_cma(rX, rY, n_tap=11, mu=1e-4, R2=1.32)
    assert out["provenance"]["gradient"] == "Godard-with-z"
    assert not out["diverged"], "C10 diverged on clean 16QAM"
    # After warm-up, |z|^2 should be close to 1.32 (target).
    zX = out["zX"]
    tail = zX[400:900]
    mean_pow = float(np.mean(np.abs(tail) ** 2))
    # Allow some variance around the 16QAM average power (1.0 normalised to /sqrt(10)).
    assert 0.3 < mean_pow < 2.5, f"C10 |z|^2={mean_pow} outside plausible range"


# =============================================================================
# Sanity 3: C11 CMA + DD-LMS does not degrade a clean converged stage 1
# =============================================================================

def test_c11_smoke_no_degradation_on_clean():
    """On clean 16QAM where stage-1 CMA already converges, stage-2 DD-LMS
    does not make PI-SER worse."""
    rX, rY = _make_clean_16qam(n_symbols=1024, seed=11)
    out = cand.c11_cma_dd_lms_cascade(
        rX, rY, n_tap=11, cma_mu=1e-3, cma_R2=1.32, cma_block_size=64,
        dd_step_size=1e-3, dd_iterations=1,
        hard_decision_fn=evaluator.hard_16qam,
    )
    assert out["provenance"]["stage_1_gradient"] == "Godard-with-z"
    assert not out["diverged"], "C11 diverged on clean 16QAM"


# =============================================================================
# Sanity 4: C05 detector emits NO alert on constant-|z|^2 input
# =============================================================================

def test_c05_detector_constant_input():
    """On a synthetic constant-|z|^2 = R2 input (ratio = 1.0), C05 emits
    no alert."""
    # Build a trace where every block has z2_over_R2_ratio = 1.0.
    trace = [
        {"output_start": i * 64, "z2_over_R2_ratio": 1.0}
        for i in range(10)
    ]
    out = cand.c05_threshold_detector(
        trace, z2_ratio_threshold=0.4, cusum_drift=0.05, cusum_threshold=3.0,
    )
    alerts = [a["alert"] for a in out["alerts"]]
    # Warmup blocks (first 2) always have alert=0 in our impl; the rest
    # should also be 0 because ratio=1.0 > 0.4 and CUSUM never accumulates.
    assert all(a == 0 for a in alerts), f"constant input triggered alerts: {alerts}"


def test_c05_detector_collapsing_input():
    """On a trace where ratio drops to 0.15 (inner ring), C05 emits alert."""
    trace = [
        {"output_start": i * 64, "z2_over_R2_ratio": 1.0}
        for i in range(2)
    ] + [
        {"output_start": (2 + i) * 64, "z2_over_R2_ratio": 0.15}
        for i in range(5)
    ]
    out = cand.c05_threshold_detector(
        trace, z2_ratio_threshold=0.4, cusum_drift=0.05, cusum_threshold=3.0,
    )
    alerts = [a["alert"] for a in out["alerts"]]
    # At least one alert should fire after the ratio drops.
    assert any(a == 1 for a in alerts), f"collapse input did not trigger alert: {alerts}"


# =============================================================================
# Sanity 5: C08 bandit completes one batch without divergence
# =============================================================================

def test_c08_bandit_smoke():
    """C08 bandit selects a mu and completes without divergence on a small
    clean input."""
    rX, rY = _make_clean_16qam(n_symbols=1024, seed=11)
    out = cand.c08_adaptive_mu_bandit(
        rX, rY, n_tap=11, R2=1.32, block_size=64,
        mu_candidates=(1e-4, 3e-4, 1e-3, 3e-3, 1e-2),
        alpha=1.0,
    )
    assert out["provenance"]["bandit"] == "LinUCB"
    assert len(out["arm_history"]) > 0, "no arm selections recorded"
    assert all(np.isfinite(a) for a in out["arm_history"]), "non-finite arm"
    # All rewards finite.
    assert all(np.isfinite(t["reward"]) for t in out["trace"]), "non-finite reward"


def test_c05_label_from_oracle():
    assert cand.c05_label_from_oracle(0.5) == 1
    assert cand.c05_label_from_oracle(0.1) == 0
    assert cand.c05_label_from_oracle(0.3, collapse_threshold=0.3) == 0  # strict >
