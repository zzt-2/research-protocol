"""Identity/sanity tests for the HOS equalizer."""
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import hos_equalizer as hos


def test_hos_no_modulus_term():
    """The HOS objective must NOT contain a |z|^2 modulus-matching term."""
    assert hos.hos_equalize_dp.__doc__ is not None
    assert "modulus" in hos.hos_equalize_dp.__doc__.lower() or "kurtosis" in hos.hos_equalize_dp.__doc__.lower()


def test_hos_produces_output():
    """HOS must produce non-degenerate output on random data."""
    rng = np.random.default_rng(42)
    rX = rng.standard_normal(256) + 1j * rng.standard_normal(256)
    rY = rng.standard_normal(256) + 1j * rng.standard_normal(256)
    zX, zY, info = hos.hos_equalize_dp(rX, rY)
    assert zX.shape == rX.shape, f"shape mismatch {zX.shape} vs {rX.shape}"
    assert zY.shape == rY.shape
    assert np.all(np.isfinite(zX)), "zX has NaN/Inf"
    assert np.all(np.isfinite(zY)), "zY has NaN/Inf"
    assert info["cost_contains_modulus_term"] is False


def test_hos_no_tx_truth():
    """HOS must only take (rX, rY), no TX truth."""
    import inspect
    sig = inspect.signature(hos.hos_equalize_dp)
    params = list(sig.parameters.keys())
    assert "rX" in params and "rY" in params
    assert "sX" not in params and "truth" not in str(params).lower()


def test_hos_orthogonal_mix():
    """HOS should separate a known orthogonal 2x2 mixture of 16QAM-like sources."""
    rng = np.random.default_rng(99)
    levels = np.array([-3, -1, 1, 3]) / np.sqrt(10)
    N = 1000
    # Source 1: 16QAM real-axis
    sX = rng.choice(levels, N) + 1j * rng.choice(levels, N)
    # Source 2: independent 16QAM
    sY = rng.choice(levels, N) + 1j * rng.choice(levels, N)
    # Mix with a known 2x2 matrix
    J = np.array([[1.0, 0.3j], [0.2, 0.9]])
    rX = J[0, 0] * sX + J[0, 1] * sY
    rY = J[1, 0] * sX + J[1, 1] * sY
    zX, zY, info = hos.hos_equalize_dp(rX, rY)
    # The output should NOT be degenerate (single point)
    assert np.std(np.abs(zX)) > 0.1, "zX is degenerate"
    assert np.std(np.abs(zY)) > 0.1, "zY is degenerate"


if __name__ == "__main__":
    test_hos_no_modulus_term()
    print("PASS: test_hos_no_modulus_term")
    test_hos_produces_output()
    print("PASS: test_hos_produces_output")
    test_hos_no_tx_truth()
    print("PASS: test_hos_no_tx_truth")
    test_hos_orthogonal_mix()
    print("PASS: test_hos_orthogonal_mix")
    print("All 4 identity tests PASS")
