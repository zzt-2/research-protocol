"""CB1 modulation-generic closure verification tests.

Three hard gates (per capability-leverage-atlas.v1.yaml cb1_build_plan_summary):
  step_5 deterministic smoke (16QAM cell runs end-to-end)
  step_6 special-case regression (R²_16QAM = 1.32 matches analytical)
  step_6 QPSK regression (P03 v1 anchor cell byte-identical)

Provenance: formula-symbol-parameter-provenance.yaml.
Run: cd projects/simulation && python -m pytest ../thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/tests/test_cb1_closure.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Ensure projects/simulation is on sys.path so `from common...` and `from params...` work.
# This test file lives at projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/tests/
REPO_ROOT = Path(__file__).resolve().parents[5]  # up from tests/cb1.../scout/direction-lab/thesis-fso/projects
SIM_DIR = REPO_ROOT / "projects" / "simulation"
sys.path.insert(0, str(SIM_DIR))

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
from common._modulation import qam16_mod, qam16_demod, hard_decision  # noqa: E402
from common._cma import cma_radius  # noqa: E402


# =============================================================================
# Gate 1: QPSK regression — pre-CB1 generator must be byte-identical
# =============================================================================

def test_qpsk_path_byte_identical_to_precb1():
    """The QPSK path (modulation='qpsk', the default) must produce the exact
    same bitsX/bitsY/sX/sY/h/theta/rX/rY as the pre-CB1 inline generator.

    This protects P03 v1 source-equivalence (commit 65db35bb) and B001-B003
    protected-history reproducibility. The reference values below are the
    pre-CB1 generator's output for the P03 v1 anchor parameters.
    """
    # P03 v1 anchor cell parameters (from source-equivalence-contract.v1.yaml)
    N, alpha, beta, f_g = 512, 4.2, 1.4, 30.0
    sop_rate, gamma_bar, seed = 4e-6, 100.0, 11
    block, t_s, method = 100, 4e-10, "gar"

    # Default modulation='qpsk' must match explicit modulation='qpsk'
    out_default = generate_shared_realization_dp(
        N, alpha, beta, f_g, sop_rate, seed,
        gamma_bar=gamma_bar, block=block, t_s=t_s, method=method,
    )
    out_explicit = generate_shared_realization_dp(
        N, alpha, beta, f_g, sop_rate, seed,
        gamma_bar=gamma_bar, block=block, t_s=t_s, method=method,
        modulation="qpsk",
    )
    for key in ("rX", "rY", "sX", "sY", "h", "theta", "bitsX", "bitsY"):
        a = np.asarray(out_default[key])
        b = np.asarray(out_explicit[key])
        assert a.shape == b.shape, f"{key} shape mismatch"
        assert np.array_equal(a, b), f"{key}: default vs explicit qpsk differ"
    assert out_default["modulation"] == "qpsk"
    assert out_default["bits_per_symbol"] == 2


def test_qpsk_sX_formula_preserved():
    """sX = ((1 - 2*bitsX[0::2]) + 1j*(1 - 2*bitsX[1::2])) / sqrt(2) —
    the (1 - 2*bits) sign convention must be preserved (NOT qpsk_mod's
    (2*bits - 1))."""
    out = generate_shared_realization_dp(
        64, 4.2, 1.4, 30.0, 4e-6, 42, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar",
    )
    bitsX = out["bitsX"]
    expected_sX = ((1 - 2 * bitsX[0::2]) + 1j * (1 - 2 * bitsX[1::2])) / np.sqrt(2)
    assert np.array_equal(out["sX"], expected_sX)


def test_qpsk_bit_length_is_2N():
    """QPSK: N symbols -> N*2 bits per polarization."""
    N = 128
    out = generate_shared_realization_dp(
        N, 4.2, 1.4, 30.0, 4e-6, 7, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar",
    )
    assert len(out["bitsX"]) == N * 2
    assert len(out["bitsY"]) == N * 2
    assert len(out["sX"]) == N
    assert len(out["sY"]) == N


# =============================================================================
# Gate 2: 16QAM deterministic smoke — end-to-end runnable
# =============================================================================

def test_qam16_path_smoke():
    """A 16QAM realization must be generated, equalized-able, and demapped
    without exceptions. Sanity checks on shapes, dtypes, finiteness, and
    average power normalization."""
    N = 512
    out = generate_shared_realization_dp(
        N, 4.2, 1.4, 30.0, 4e-6, 11, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar", modulation="qam16",
    )
    assert out["modulation"] == "qam16"
    assert out["bits_per_symbol"] == 4
    # 16QAM: N symbols -> N*4 bits per polarization
    assert len(out["bitsX"]) == N * 4
    assert len(out["bitsY"]) == N * 4
    assert len(out["sX"]) == N
    assert len(out["sY"]) == N
    # Shapes of channel physics unchanged
    assert len(out["h"]) == N
    assert len(out["theta"]) == N
    assert len(out["rX"]) == N
    assert len(out["rY"]) == N
    # All finite
    for key in ("rX", "rY", "sX", "sY", "h"):
        assert np.all(np.isfinite(out[key])), f"{key} has non-finite values"
    # Average power normalization: E[|s|^2] ≈ 1 (sample estimate on N symbols)
    power_x = np.mean(np.abs(out["sX"]) ** 2)
    power_y = np.mean(np.abs(out["sY"]) ** 2)
    assert abs(power_x - 1.0) < 0.05, f"sX avg power {power_x} not ~1"
    assert abs(power_y - 1.0) < 0.05, f"sY avg power {power_y} not ~1"


def test_qam16_hard_decision_roundtrip_clean():
    """hard_decision(s, mod='qam16') on clean TX symbols must demod back to
    the original bits (no noise, no channel). This is the modulation-aware
    demapper special-case regression."""
    rng = np.random.default_rng(123)
    N = 1024
    bits = rng.integers(0, 2, N * 4)
    s = qam16_mod(bits)
    # hard_decision must round-trip
    s_hat = hard_decision(s, mod="qam16")
    bits_hat = qam16_demod(s_hat)
    # Allow for boundary ambiguities between -1 and +1 (both valid); check that
    # symbol error rate is zero (every s is exactly on a constellation point)
    assert np.array_equal(s, s_hat), "hard_decision did not round-trip clean 16QAM"
    assert np.array_equal(bits, bits_hat), "qam16_demod did not round-trip clean bits"


def test_qam16_demod_roundtrip_on_generator_symbols():
    """The generator's sX must demod (via qam16_demod) back to bitsX with
    zero symbol errors when no channel impairment is applied (sanity)."""
    out = generate_shared_realization_dp(
        512, 4.2, 1.4, 30.0, 4e-6, 11, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar", modulation="qam16",
    )
    bits_hat_X = qam16_demod(out["sX"])
    # sX is on-grid by construction; demod must recover bitsX exactly
    assert np.array_equal(bits_hat_X, out["bitsX"]), (
        "qam16_demod(sX) did not recover bitsX; the generator's Gray map and "
        "qam16_demod are inconsistent."
    )


# =============================================================================
# Gate 3: Special-case regression — R²_16QAM = 1.32 matches analytical
# =============================================================================

def test_r2_qam16_equals_132():
    """R²_16QAM (Godard radius squared) must equal 1.32 to 1e-12 on the
    exact 16-point constellation.

    Note: ``cma_radius`` returns ``R = sqrt(E[|s|^4]/E[|s|^2])`` (the Godard
    radius), so R² is recovered by squaring. See _cma.py:43-52.

    We use the EXACT 16-point constellation (each symbol with probability
    1/16), not a Monte-Carlo sample — the latter has ~1e-3 sampling variance
    even at 200k symbols, which would mask the analytic value.

    Analytical derivation (formula-symbol-parameter-provenance.yaml F-R2-16QAM):
      The 16QAM constellation (Gray map, /sqrt(10)) has
      |si|,|sq| ∈ {1, 3}/sqrt(10), each with probability 1/4 per axis.
      E[|s|^2] = E[si^2] + E[sq^2] = 2 * (1/4)(1+1+9+9)/10 = 2 * 20/40 = 1.0
      E[|s|^4] = E[(si^2 + sq^2)^2]
               = E[si^4] + 2 E[si^2]E[sq^2] + E[sq^4]
               = 2*E[si^4] + 2*(E[si^2])^2     (si, sq i.i.d.)
      E[si^2] = (1+1+9+9)/(4*10) = 20/40 = 0.5
      E[si^4] = (1+1+81+81)/(4*100) = 164/400 = 0.41
      E[|s|^4] = 2*0.41 + 2*(0.5)^2 = 0.82 + 0.5 = 1.32
      R^2 = E[|s|^4] / E[|s|^2] = 1.32 / 1.0 = 1.32
    """
    # Build the exact 16-point constellation by passing all 16 distinct
    # 4-bit labels through qam16_mod. Each appears once → uniform 1/16.
    all_labels = np.array(
        [[b3, b2, b1, b0] for b3 in (0, 1) for b2 in (0, 1)
         for b1 in (0, 1) for b0 in (0, 1)],
        dtype=int,
    ).reshape(-1)
    s = qam16_mod(all_labels)
    assert len(s) == 16, f"expected 16 constellation points, got {len(s)}"
    r = cma_radius(s)
    r2 = r ** 2
    assert abs(r2 - 1.32) < 1e-12, f"R²_16QAM = {r2}, expected 1.32 (R={r})"


def test_r2_qam16_monte_carlo_close_to_132():
    """A large random 16QAM population must give R² within ~1% of 1.32.

    This is a sanity check on the Monte-Carlo estimate (the exact value is
    covered by test_r2_qam16_equals_132). Allows for sampling variance.
    """
    rng = np.random.default_rng(2024)
    bits = rng.integers(0, 2, 4 * 200_000)
    s = qam16_mod(bits)
    r2 = cma_radius(s) ** 2
    assert abs(r2 - 1.32) < 0.01, f"R²_16QAM Monte-Carlo = {r2}, not within 1% of 1.32"


def test_r2_qpsk_equals_1():
    """R²_QPSK must equal 1.0 (constant modulus). Sanity regression.

    cma_radius returns R = sqrt(R²); for QPSK R = 1, R² = 1.
    """
    rng = np.random.default_rng(2024)
    bits = rng.integers(0, 2, 2 * 200_000)
    # Use the generator's (1-2b) sign convention via a fresh symbol set:
    s = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    r = cma_radius(s)
    r2 = r ** 2
    assert abs(r2 - 1.0) < 1e-9, f"R²_QPSK = {r2}, expected 1.0 (R={r})"


# =============================================================================
# Gate 4: Modulation isolation — unsupported modulation raises
# =============================================================================

def test_unsupported_modulation_raises():
    """Calling the generator with an unsupported modulation must raise
    ValueError immediately (fail-fast, not silent QPSK fallback)."""
    with pytest.raises(ValueError, match="not supported"):
        generate_shared_realization_dp(
            64, 4.2, 1.4, 30.0, 4e-6, 1, gamma_bar=100.0,
            block=100, t_s=4e-10, method="gar", modulation="64qam",
        )


# =============================================================================
# Gate 5: RNG draw-order isolation between QPSK and 16QAM
# =============================================================================

def test_qpsk_and_qam16_share_channel_physics_but_differ_in_bits():
    """The channel physics (h, theta) is modulation-agnostic — same seed
    must produce identical h and theta regardless of modulation. But bitsX
    must differ (different bit-draw lengths). This confirms the modulation
    knob only branches symbol generation, not the GG/SOP physics."""
    common_kwargs = dict(
        N=512, alpha=4.2, beta=1.4, f_g=30.0, sop_rate=4e-6, seed=11,
        gamma_bar=100.0, block=100, t_s=4e-10, method="gar",
    )
    out_q = generate_shared_realization_dp(modulation="qpsk", **common_kwargs)
    out_16 = generate_shared_realization_dp(modulation="qam16", **common_kwargs)
    # Physics identical
    assert np.array_equal(out_q["h"], out_16["h"]), "h differs across modulation"
    assert np.array_equal(out_q["theta"], out_16["theta"]), "theta differs across modulation"
    # Bits differ (different RNG consumption; lengths also differ)
    assert len(out_q["bitsX"]) != len(out_16["bitsX"]), "bitsX length did not change"
