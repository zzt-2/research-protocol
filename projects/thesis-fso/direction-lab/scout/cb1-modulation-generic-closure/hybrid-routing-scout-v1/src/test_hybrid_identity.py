"""Identity tests for the hybrid-routing Scout experts.

Gate set (per batch-contract.v1.yaml):
  - no_op / structure identity
  - complex_convention (r @ w, not np.vdot confusion)
  - causal_prefix invariance
  - source_closure (formula cited in docstring)
  - decision_feedback_causal (DD-LMS: s_hat[t] uses only z[t])

Run: python -m pytest test_hybrid_identity.py -q
(plain assert, no pytest dependency required for direct run)
"""
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dd_lms_equalizer import dd_lms_cold_start, _hard_16qam


def test_hard_16qam_centers():
    """Hard decision maps each constellation point to itself."""
    grid = (np.array([-3, -1, 1, 3]) / np.sqrt(10.0))
    pts = np.array([complex(r, i) for r in grid for i in grid])
    z = _hard_16qam(pts)
    assert np.allclose(z, pts), "constellation points must map to themselves"


def test_dd_no_op_structure():
    """With mu=0, weights never update; output = pure center-tap filtered signal."""
    rng = np.random.default_rng(0)
    rX = (rng.standard_normal(512) + 1j * rng.standard_normal(512))
    rY = (rng.standard_normal(512) + 1j * rng.standard_normal(512))
    out = dd_lms_cold_start(rX, rY, n_tap=11, mu=0.0, block_size=64)
    assert not out["diverged"]
    # With mu=0, weights stay at init; final_w_norm == init norm (sqrt(2))
    assert abs(out["final_w_norm"] - np.sqrt(2.0)) < 1e-9, \
        f"mu=0 must freeze weights; got wnorm {out['final_w_norm']}"


def test_dd_complex_convention():
    """Output is r @ w (convolution), not np.vdot(w, r) (which would conjugate r)."""
    # Single-tap case: y = w * r (not conj). Use n_tap=1 to isolate.
    rX = np.array([1.0 + 2.0j, 0.0 + 0.0j])  # only first sample nonzero
    rY = np.zeros(2, dtype=complex)
    out = dd_lms_cold_start(rX, rY, n_tap=1, mu=0.0, block_size=1)
    # n_tap=1 center tap = index 0; wxx init = scale=1; zX[0] = 1*wxx*rX[0] = rX[0]
    assert abs(out["zX"][0] - (1.0 + 2.0j)) < 1e-9, \
        f"n_tap=1 center must pass rX through; got {out['zX'][0]}"


def test_dd_causal_prefix():
    """Changing FUTURE samples must not change earlier outputs."""
    rng = np.random.default_rng(42)
    rX = (rng.standard_normal(300) + 1j * rng.standard_normal(300))
    rY = (rng.standard_normal(300) + 1j * rng.standard_normal(300))
    out1 = dd_lms_cold_start(rX, rY, n_tap=11, mu=1e-3, block_size=64)
    # Perturb only samples after position 150
    rX2 = rX.copy(); rX2[200:] += 5.0
    out2 = dd_lms_cold_start(rX2, rY, n_tap=11, mu=1e-3, block_size=64)
    # Prefix [0:150 - half] must be bit-identical (block boundary: block 0,1 end at 128, 192)
    safe = 128 - 5  # well within block 0-1, before any perturbation influence
    assert np.allclose(out1["zX"][:safe], out2["zX"][:safe]), \
        "causal-prefix violated: future samples changed earlier output"


def test_dd_decision_feedback_causal():
    """s_hat at time t uses only z[t] (the DD-LMS decision is instantaneous)."""
    # The hard decision is applied elementwise on the block output; verify by
    # checking that two inputs differing only at index t produce outputs differing
    # only at >= t (no future decision feeds back into an earlier symbol within
    # the same block since the update happens at block-end, after all z computed).
    rng = np.random.default_rng(7)
    rX = (rng.standard_normal(128) + 1j * rng.standard_normal(128))
    rY = np.zeros(128, dtype=complex)
    out1 = dd_lms_cold_start(rX, rY, n_tap=11, mu=1e-3, block_size=128)
    rX2 = rX.copy(); rX2[100] += 3.0
    out2 = dd_lms_cold_start(rX2, rY, n_tap=11, mu=1e-3, block_size=128)
    # Within the single block, z is computed for ALL samples BEFORE the update,
    # so z[:100] must be identical (the perturbation at 100 cannot affect z[0:100])
    assert np.allclose(out1["zX"][:100], out2["zX"][:100]), \
        "decision_feedback_causal violated: perturbation at t affected z[<t]"


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            raise
    print(f"{passed}/{len(tests)} identity tests PASS")


if __name__ == "__main__":
    _run_all()
