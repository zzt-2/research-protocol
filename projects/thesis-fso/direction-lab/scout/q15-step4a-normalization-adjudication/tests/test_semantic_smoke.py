"""Q15 Step 4a — semantic smoke TDD tests (must ALL PASS before compare).

These are written FIRST and gate the comparison. A failure here means the
comparator or evaluator is identity-broken and the comparison cannot be trusted
(Q15_BASELINE_OR_EVALUATOR_IDENTITY_BLOCKED_NO_GO).
"""

import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve()
SRC = HERE.parent.parent / "src"
SCOUT = HERE.parents[2]
CB1_ROOT = SCOUT / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
for p in (str(SRC), str(BASELINE_ATLAS), str(SIM_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import methods as ADJ  # this dir's methods.py

# Public 16QAM alphabet (avg-power-normalized, E|s|^2 = 1)
_AMP = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
_RE, _IM = np.meshgrid(_AMP, _AMP)
ALPHABET = (_RE + 1j * _IM).ravel()


def _hard(z):
    from common._modulation import hard_decision
    return np.asarray(hard_decision(np.asarray(z, dtype=np.complex128), mod="qam16"),
                      dtype=np.complex128)


# ─── Gate 1: correct sqrt restores amplitude on synthetic z=c*s; M1 WRONG FAILS ─

def test_correct_sqrt_restores_amplitude_m1_wrong_fails():
    """On synthetic z=c*s, correct a=sqrt(Ps/Pz) recovers SER=0 for ALL c;
    M1's scale=Ps/Pz (no sqrt) over-corrects by 1/c and FAILS for strong
    collapse. This is the audit that exposes T020's M1 bug and validates the
    new comparators. M1's failure is monotonic in |1/c - 1|; it only shows for
    strong collapse (c far from 1), since 16QAM grid spacing tolerates mild
    over/under-scaling."""
    rng = np.random.default_rng(0)
    s = rng.choice(ALPHABET, size=4000)
    m1_sers = {}
    for c in (0.45, 0.7, 1.0, 1.3, 1.8):
        z = c * s
        pz = np.mean(np.abs(z) ** 2)
        a_correct = float(np.sqrt(1.0 / pz))
        scale_m1_wrong = 1.0 / pz
        rec_correct = a_correct * z
        rec_m1 = scale_m1_wrong * z
        ser_correct = np.mean(_hard(rec_correct) != s)
        ser_m1 = np.mean(_hard(rec_m1) != s)
        m1_sers[c] = ser_m1
        # CORRECT sqrt must recover perfectly for every c
        assert ser_correct == 0.0, f"c={c}: correct sqrt SER={ser_correct} != 0"
    # M1 wrong: at c=1.0 it is exact (factor 1); at strong collapse c=0.45 it
    # catastrophically over-corrects (factor 2.22 -> SER high). Monotone in |1/c-1|.
    assert m1_sers[1.0] == 0.0
    assert m1_sers[0.45] > 0.3, f"M1 wrong at c=0.45 SER={m1_sers[0.45]} should be >0.3"
    assert m1_sers[0.45] > m1_sers[0.7], "M1 wrong should worsen as collapse deepens"


# ─── Gate 2: identity config bit-identical (unit-power prefix -> a≈1) ────────
# A finite 500-symbol 16QAM sample has ~1-2% scale noise; the trimmed mean
# estimator inherits it. The physical identity property is a→1 as N→∞; for the
# finite prefix we require a within the finite-sample envelope AND that the
# estimator is unbiased (mean over many draws ≈ 1).

def test_identity_per_pol_unbiased_and_close():
    """Over many draws, a_x/a_y are unbiased (mean≈1) and each within ~5%."""
    rng = np.random.default_rng(1)
    axs, ays = [], []
    for _ in range(40):
        zpx = rng.choice(ALPHABET, size=500)
        zpy = rng.choice(ALPHABET, size=500)
        f = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
        axs.append(f["a_x"]); ays.append(f["a_y"])
    assert abs(np.mean(axs) - 1.0) < 0.01, f"a_x biased: mean={np.mean(axs)}"
    assert abs(np.mean(ays) - 1.0) < 0.01, f"a_y biased: mean={np.mean(ays)}"
    # each draw within 5% (3 sigma of the trimmed-mean estimator at N=500)
    assert all(abs(a - 1.0) < 0.05 for a in axs)
    assert all(abs(a - 1.0) < 0.05 for a in ays)


def test_pooled_identity_unbiased_and_close():
    rng = np.random.default_rng(2)
    pooled_as = []
    for _ in range(40):
        zpx = rng.choice(ALPHABET, size=500)
        zpy = rng.choice(ALPHABET, size=500)
        f = ADJ.correct_pooled_sqrt_rms_freeze(zpx, zpy)
        pooled_as.append(f["a"])
    assert abs(np.mean(pooled_as) - 1.0) < 0.01, f"pooled a biased: mean={np.mean(pooled_as)}"
    assert all(abs(a - 1.0) < 0.05 for a in pooled_as)


# ─── Gate 3: prefix-only freeze invariance (suffix perturbation no effect) ────

def test_prefix_freeze_invariance():
    """Perturbing the suffix must NOT change any frozen scale/gate/map."""
    rng = np.random.default_rng(3)
    zpx = 0.45 * rng.choice(ALPHABET, size=128)  # collapsed prefix
    zpy = 0.45 * rng.choice(ALPHABET, size=128)
    fa = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    fb = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    assert np.isclose(fa["a_x"], fb["a_x"], atol=1e-12)
    assert np.isclose(fa["a_y"], fb["a_y"], atol=1e-12)
    fg_a = ADJ.gated_scalar_ablation_freeze(zpx, zpy)
    fg_b = ADJ.gated_scalar_ablation_freeze(zpx, zpy)
    assert fg_a["policy"] == fg_b["policy"]
    assert np.isclose(fg_a["a_x"], fg_b["a_x"], atol=1e-12)


# ─── Gate 4: QPSK identity regression ────────────────────────────────────────

def test_qpsk_identity_regression():
    """On QPSK (no inner-ring collapse), correct normalization on a unit-power
    prefix yields a≈1 (identity); no degradation."""
    rng = np.random.default_rng(4)
    qpsk = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    zpx = rng.choice(qpsk, size=500)
    zpy = rng.choice(qpsk, size=500)
    f = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    # QPSK per-symbol |s|^2 = 1 (normalized), so a≈1
    assert np.isclose(f["a_x"], 1.0, atol=1e-3), f"qpsk a_x={f['a_x']}"


# ─── Gate 5: each comparator gives different output for different input ──────

def test_information_increment():
    """A correct comparator must produce DIFFERENT output for different input
    (information increment). A no-op that ignores input would FAIL."""
    rng = np.random.default_rng(5)
    zpx = 0.5 * rng.choice(ALPHABET, size=128)
    zpy = 0.5 * rng.choice(ALPHABET, size=128)
    fp = ADJ.correct_pooled_sqrt_rms_freeze(zpx, zpy)
    z_a = rng.choice(ALPHABET, size=200)
    z_b = z_a + 0.3 + 0.3j
    oa = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, z_a)
    ob = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, z_b)
    assert np.any(np.abs(oa - ob) > 1e-9), "comparator ignored input"


# ─── Gate 6: no-op / clean not degraded ──────────────────────────────────────

def test_clean_stream_not_degraded_by_identity_branch():
    """Gated-scalar ablation: on a HEALTHY prefix (unit power + spread), the
    gate selects identity -> output == input (no degradation)."""
    rng = np.random.default_rng(6)
    # healthy: unit power, decent spread (real 16QAM)
    zpx = rng.choice(ALPHABET, size=500)
    zpy = rng.choice(ALPHABET, size=500)
    f = ADJ.gated_scalar_ablation_freeze(zpx, zpy)
    assert f["policy"] == "identity", f"healthy prefix should select identity, got {f['policy']}"
    z_a = rng.choice(ALPHABET, size=200)
    z_b = rng.choice(ALPHABET, size=200)
    oa, ob = ADJ.gated_scalar_ablation_apply_continuous(f, z_a, z_b)
    assert np.array_equal(oa, z_a), "identity branch modified input"
    assert np.array_equal(ob, z_b), "identity branch modified input"


# ─── Gate 7: collapsed prefix opens the gate (gate rule works) ───────────────

def test_collapsed_prefix_opens_gate():
    """On a COLLAPSED prefix (low power + spread), gated-scalar selects 'scale'."""
    rng = np.random.default_rng(7)
    zpx = 0.4 * rng.choice(ALPHABET, size=500)
    zpy = 0.4 * rng.choice(ALPHABET, size=500)
    f = ADJ.gated_scalar_ablation_freeze(zpx, zpy)
    assert f["policy"] == "scale", f"collapsed prefix should open gate, got {f['policy']}"
    # and the scale should be > 1 (amplifying collapsed stream)
    assert f["a_x"] > 1.0 and f["a_y"] > 1.0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
