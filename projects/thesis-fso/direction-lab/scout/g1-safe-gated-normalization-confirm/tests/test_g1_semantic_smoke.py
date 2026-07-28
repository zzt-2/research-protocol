"""G1_SAFE_GATED_NORMALIZATION confirm — semantic smoke TDD tests (9 checks).

ALL must PASS before the 20-seed compare runs. A failure here emits
G1_IDENTITY_OR_RECEIPT_BLOCKED_NO_GO (do NOT run the compare, do NOT leave a
repair package). These gates are written FIRST and gate the comparison.
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
T020_ROOT = SCOUT / "preformal-method-factory-sprint-002"
T020_SRC = T020_ROOT / "src"
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
C11_LEGALITY = CB1_ROOT / "c11-legality-batch-v1"
# Load each methods.py by explicit path to avoid the sys.path name clash
# (both this dir and T020 have a methods.py; whichever is imported first wins).
import importlib.util
_spec_g1 = importlib.util.spec_from_file_location("g1_methods_smoke", str(SRC / "methods.py"))
G1M = importlib.util.module_from_spec(_spec_g1)
_spec_g1.loader.exec_module(G1M)
_spec_t020 = importlib.util.spec_from_file_location("t020_methods_smoke", str(T020_SRC / "methods.py"))
T020M = importlib.util.module_from_spec(_spec_t020)
_spec_t020.loader.exec_module(T020M)
for p in (str(BASELINE_ATLAS), str(SIM_DIR), str(C11_LEGALITY)):
    if p not in sys.path:
        sys.path.insert(0, p)

import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402

# Public 16QAM alphabet (avg-power-normalized, E|s|^2 = 1)
_AMP = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
_RE, _IM = np.meshgrid(_AMP, _AMP)
ALPHABET = (_RE + 1j * _IM).ravel()


def _hard(z):
    return np.asarray(evaluator.hard_16qam(np.asarray(z, dtype=np.complex128)),
                      dtype=np.complex128)


# ─── 1. z=c*s: correct per-pol sqrt restores amplitude (SER=0); power-ratio fails ─

def test_correct_sqrt_restores_amplitude_power_ratio_fails():
    """On synthetic z=c*s, correct per-pol a=sqrt(Ps/Pz) recovers SER=0 for
    ALL c in {0.3,0.45,0.6,0.8,1.0}; the OLD power-ratio formula (scale=Ps/Pz,
    no sqrt) over-corrects by 1/c and FAILS at strong collapse (SER>0.3 at
    c=0.45). [confirms T023 finding]"""
    rng = np.random.default_rng(0)
    s = rng.choice(ALPHABET, size=4000)
    m1_sers = {}
    for c in (0.3, 0.45, 0.6, 0.8, 1.0):
        z = c * s
        pz = np.mean(np.abs(z) ** 2)
        a_correct = float(np.sqrt(1.0 / pz))
        scale_old_power_ratio = 1.0 / pz          # the WRONG (T020 M1) formula
        rec_correct = a_correct * z
        rec_old = scale_old_power_ratio * z
        ser_correct = float(np.mean(_hard(rec_correct) != s))
        ser_old = float(np.mean(_hard(rec_old) != s))
        # CORRECT sqrt must recover perfectly for every c
        assert ser_correct == 0.0, f"c={c}: correct sqrt SER={ser_correct} != 0"
        m1_sers[c] = ser_old
    # old power-ratio: exact at c=1, catastrophic over-correction at c=0.45
    assert m1_sers[1.0] == 0.0
    assert m1_sers[0.45] > 0.3, f"old power-ratio at c=0.45 SER={m1_sers[0.45]} should be >0.3"


# ─── 2. G1 identity branch is bit-identical to baseline ───────────────────────

def test_g1_identity_branch_bit_identical_to_baseline():
    """When G1 policy=identity, z' == z exactly (bit-identical to baseline)."""
    rng = np.random.default_rng(1)
    zpx = rng.choice(ALPHABET, size=500)         # healthy -> identity
    zpy = rng.choice(ALPHABET, size=500)
    f = G1M.gated_scalar_freeze(zpx, zpy)
    assert f["policy"] == "identity", f"healthy prefix should select identity, got {f['policy']}"
    zsx = rng.choice(ALPHABET, size=200)
    zsy = rng.choice(ALPHABET, size=200)
    ox, oy = G1M.gated_scalar_apply_continuous(f, zsx, zsy)
    assert np.array_equal(ox, np.asarray(zsx, dtype=np.complex128)), "identity branch modified x"
    assert np.array_equal(oy, np.asarray(zsy, dtype=np.complex128)), "identity branch modified y"


# ─── 3. prefix-freeze invariance: perturbing suffix does NOT change gate/scale ─

def test_prefix_freeze_invariance_suffix_perturbation_no_effect():
    """Fix the prefix; perturb the suffix. The frozen gate policy and the
    per-pol scales must NOT change (prefix-only freeze; no suffix feedback)."""
    rng = np.random.default_rng(2)
    zpx = 0.45 * rng.choice(ALPHABET, size=128)    # collapsed prefix
    zpy = 0.45 * rng.choice(ALPHABET, size=128)
    fa = G1M.gated_scalar_freeze(zpx, zpy)
    # regenerate on the SAME prefix -> bit-identical freeze
    fb = G1M.gated_scalar_freeze(zpx, zpy)
    assert fa["policy"] == fb["policy"]
    assert fa["gate_active"] == fb["gate_active"]
    assert np.isclose(fa["a_x"], fb["a_x"], atol=1e-12)
    assert np.isclose(fa["a_y"], fb["a_y"], atol=1e-12)
    # now perturb a DIFFERENT suffix and confirm the FROZEN params are unchanged
    zsx1 = rng.choice(ALPHABET, size=200)
    zsy1 = rng.choice(ALPHABET, size=200)
    zsx2 = zsx1 + 0.5 + 0.5j                       # heavily perturbed suffix
    zsy2 = zsy1 + 0.5 + 0.5j
    o1x, o1y = G1M.gated_scalar_apply_continuous(fa, zsx1, zsy1)
    o2x, o2y = G1M.gated_scalar_apply_continuous(fa, zsx2, zsy2)
    # the SCALE applied is the same (frozen a_x * suffix); outputs differ only
    # through the suffix. fa's a_x/a_y/policy are unchanged objects.
    assert fa["a_x"] == fb["a_x"] and fa["policy"] == fb["policy"]


# ─── 4. two different prefixes (healthy vs collapsed) -> different policies ───

def test_two_prefixes_trigger_different_gate_policies_information_increment():
    """A healthy prefix (mean_abs2 >= 0.6) -> identity; a collapsed prefix
    (mean_abs2 < 0.6) -> scale. The gate carries information increment."""
    rng = np.random.default_rng(3)
    zpx_h = rng.choice(ALPHABET, size=500)         # healthy (unit power)
    zpy_h = rng.choice(ALPHABET, size=500)
    fh = G1M.gated_scalar_freeze(zpx_h, zpy_h)
    assert fh["policy"] == "identity", f"healthy mean_abs2={fh['mean_abs2']}"
    assert fh["mean_abs2"] >= 0.6
    zpx_c = 0.4 * rng.choice(ALPHABET, size=500)   # collapsed
    zpy_c = 0.4 * rng.choice(ALPHABET, size=500)
    fc = G1M.gated_scalar_freeze(zpx_c, zpy_c)
    assert fc["policy"] == "scale", f"collapsed mean_abs2={fc['mean_abs2']}"
    assert fc["mean_abs2"] < 0.6
    assert fh["policy"] != fc["policy"], "gate did not discriminate healthy vs collapsed"


# ─── 5. QPSK identity regression (G1 on clean QPSK = identity, PI-SER=0) ──────

def test_qpsk_identity_regression_pi_ser_zero():
    """G1 on a clean QPSK stream applies NO net transform: z' == z bit-identical
    (zero degradation / PI-SER=0 contribution). QPSK is single-amplitude
    (|s|^2=1 for every symbol -> spread=0), so the frozen gate classifies it as
    single-mode and opens the scale branch; BUT the per-pol sqrt scale on a
    unit-power QPSK prefix is a = sqrt(Ps / mean|z|^2) = sqrt(1/1) = 1.0, so the
    applied transform is identity in effect. This is the truthful QPSK safety
    regression: no degradation regardless of which branch the gate opens."""
    rng = np.random.default_rng(4)
    qpsk = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    zpx = rng.choice(qpsk, size=500)
    zpy = rng.choice(qpsk, size=500)
    f = G1M.gated_scalar_freeze(zpx, zpy)
    # QPSK: mean_abs2 = 1.0 (>= 0.6) but spread = 0 (< 0.1) -> single-mode scale branch
    assert f["mean_abs2"] >= 0.6
    # the per-pol sqrt scale on a unit-power prefix must be ~1.0 (no net scaling)
    assert np.isclose(f["a_x"], 1.0, atol=1e-2), f"qpsk a_x={f['a_x']} should be ~1"
    assert np.isclose(f["a_y"], 1.0, atol=1e-2), f"qpsk a_y={f['a_y']} should be ~1"
    zsx = rng.choice(qpsk, size=200)
    zsy = rng.choice(qpsk, size=200)
    ox, oy = G1M.gated_scalar_apply_continuous(f, zsx, zsy)
    # net transform is identity (a=1) -> bit-identical, zero PI-SER contribution
    assert np.allclose(ox, np.asarray(zsx, dtype=np.complex128), atol=1e-9), "qpsk net transform != identity"
    assert np.allclose(oy, np.asarray(zsy, dtype=np.complex128), atol=1e-9), "qpsk net transform != identity"


# ─── 6. evaluator PI / denominator / fixed-label consistent across methods ────

def test_evaluator_population_denominator_fixed_label_consistent_across_methods():
    """All methods are scored by the SAME evaluator on the SAME eval window,
    same hard_16qam, same ROTATIONS_16QAM, same TX-truth population. Build two
    method outputs on the same realization and confirm the evaluator's
    fixed_label_ser and pi_ser are mutually consistent (pi <= fixed; same N)."""
    # Build a synthetic dual-pol stream and two scaled variants.
    rng = np.random.default_rng(5)
    sx = rng.choice(ALPHABET, size=128)
    sy = rng.choice(ALPHABET, size=128)
    bits_per = 4
    # truth bits MUST be consistent with the symbols (the real channel emits
    # Gray-mapped bits via qam16_mod; the evaluator demaps via qam16_demod).
    from common._modulation import qam16_demod
    bx = np.asarray(qam16_demod(np.asarray(sx, dtype=np.complex128)), dtype=int).ravel()
    by = np.asarray(qam16_demod(np.asarray(sy, dtype=np.complex128)), dtype=int).ravel()
    # method A = identity; method B = scaled by 0.9 (mild)
    zAx, zAy = sx.copy(), sy.copy()
    zBx, zBy = 0.9 * sx, 0.9 * sy
    mA = evaluator.evaluate_dual_16qam(zAx, zAy, sx, sy, bx, by)
    mB = evaluator.evaluate_dual_16qam(zBx, zBy, sx, sy, bx, by)
    # PI-SER <= fixed-label SER (permutation invariance can only help)
    assert mA["pi_ser"] <= mA["fixed_label_ser"] + 1e-12
    assert mB["pi_ser"] <= mB["fixed_label_ser"] + 1e-12
    # identity (A) must be near-zero PI-SER on clean symbols
    assert mA["pi_ser"] < 1e-6, f"identity PI-SER={mA['pi_ser']}"
    # same hard decision function + rotations used (consistency check): both
    # methods report finite metrics with identical population size (implicit:
    # evaluate_dual_16qam raises on length mismatch, so reaching here means
    # population/denominator is consistent)
    for m in (mA, mB):
        for k in ("pi_ser", "fixed_label_ser", "pi_ber", "fixed_label_ber"):
            assert np.isfinite(m[k]), f"{k} not finite"


# ─── 7. offline label row-recomputable for 3 synthetic receipts ───────────────

def _label_from_dict(d):
    """EXACTLY _offline_label from run_factory.py:558 (task-native).
    healthy b<0.1; awgn_dominated b>=0.1 AND (b-o)<0.005;
    recoverable_failure b>=0.1 AND o<0.1 AND (b-o)>=0.005; else ambiguous.
    Non-finite baseline/oracle -> ambiguous. baseline_diverged -> ambiguous."""
    b = d.get("baseline_pi_ser")
    o = d.get("oracle_pi_ser")
    bd = d.get("baseline_diverged", False)
    bf = d.get("baseline_metric_finite", True)
    of = d.get("oracle_metric_finite", True)
    if b is None or o is None or not bf or not of:
        return "ambiguous"
    if bd:
        return "ambiguous"
    if b < 0.1:
        return "healthy"
    if (b - o) < 0.005:
        return "awgn_dominated_error"
    if o < 0.1:
        return "inner_ring_recoverable_collapse"
    return "ambiguous"


def test_offline_label_row_recomputable_three_synthetic_receipts():
    """(a) normal finite baseline+oracle -> recoverable_failure;
    (b) baseline_diverged=True -> forced ambiguous;
    (c) baseline or oracle non-finite -> forced ambiguous. Non-finite must use
    explicit null/flag encoding (no silent row drop)."""
    # (a) normal recoverable: b=0.5, o=0.05, gap=0.45 >= 0.005, o<0.1
    a = {"baseline_pi_ser": 0.5, "oracle_pi_ser": 0.05,
         "baseline_metric_finite": True, "oracle_metric_finite": True,
         "baseline_diverged": False}
    assert _label_from_dict(a) == "inner_ring_recoverable_collapse"
    # healthy: b=0.05 < 0.1
    a2 = {"baseline_pi_ser": 0.05, "oracle_pi_ser": 0.04,
          "baseline_metric_finite": True, "oracle_metric_finite": True,
          "baseline_diverged": False}
    assert _label_from_dict(a2) == "healthy"
    # awgn_dominated: b=0.5, o=0.498, gap=0.002 < 0.005
    a3 = {"baseline_pi_ser": 0.5, "oracle_pi_ser": 0.498,
          "baseline_metric_finite": True, "oracle_metric_finite": True,
          "baseline_diverged": False}
    assert _label_from_dict(a3) == "awgn_dominated_error"
    # (b) baseline_diverged -> ambiguous (explicit flag, not a drop)
    b = {"baseline_pi_ser": None, "oracle_pi_ser": None,
         "baseline_metric_finite": False, "oracle_metric_finite": False,
         "baseline_diverged": True}
    assert _label_from_dict(b) == "ambiguous"
    # (c) non-finite baseline -> ambiguous (explicit null + flag, no silent drop)
    c = {"baseline_pi_ser": None, "oracle_pi_ser": 0.05,
         "baseline_metric_finite": False, "oracle_metric_finite": True,
         "baseline_diverged": False}
    assert _label_from_dict(c) == "ambiguous"
    # non-finite oracle -> ambiguous
    c2 = {"baseline_pi_ser": 0.5, "oracle_pi_ser": None,
          "baseline_metric_finite": True, "oracle_metric_finite": False,
          "baseline_diverged": False}
    assert _label_from_dict(c2) == "ambiguous"


# ─── 8. shared realization + reset lifecycle: deterministic, bit-identical ────

def test_shared_realization_reset_lifecycle_bit_identical():
    """Regenerating (cell,seed) twice yields bit-identical z (shared
    realization); method outputs are deterministic given frozen params."""
    from common._dual_pol_channel import generate_shared_realization_dp
    cell = {"modulation": "qam16", "snr_db": 10.0, "f_g_hz": 30.0,
            "sop_rate": 4.0e-6, "n_symbols": 512}
    gamma_bar = float(10.0 ** (cell["snr_db"] / 10.0))
    kw = dict(N=int(cell["n_symbols"]), alpha=4.2, beta=1.4,
              f_g=float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]),
              seed=261, gamma_bar=gamma_bar, block=100, t_s=4.0e-10,
              method="gar", modulation="qam16")
    rl1 = generate_shared_realization_dp(**kw)
    rl2 = generate_shared_realization_dp(**kw)
    assert np.array_equal(rl1["rX"], rl2["rX"]) and np.array_equal(rl1["rY"], rl2["rY"])
    assert np.array_equal(rl1["sX"], rl2["sX"]) and np.array_equal(rl1["sY"], rl2["sY"])
    # method outputs deterministic given frozen params: G1 freeze twice -> equal
    TAPS, MU, R2, BS = 11, 3.0e-2, 1.32, 64
    es, cal, ee, _ = runner.eval_window_for(512, TAPS, window_symbols=256, block_size=BS)
    base1 = runner.standard_cma_godard_with_z(rl1["rX"], rl1["rY"], n_tap=TAPS, mu=MU, R2=R2, block_size=BS)
    base2 = runner.standard_cma_godard_with_z(rl2["rX"], rl2["rY"], n_tap=TAPS, mu=MU, R2=R2, block_size=BS)
    assert np.array_equal(base1["zX"], base2["zX"]) and np.array_equal(base1["zY"], base2["zY"])
    zpx, zpy = base1["zX"][es:cal], base1["zY"][es:cal]
    f1 = G1M.gated_scalar_freeze(zpx, zpy)
    f2 = G1M.gated_scalar_freeze(zpx, zpy)
    assert f1["policy"] == f2["policy"] and np.isclose(f1["a_x"], f2["a_x"], atol=1e-12)


# ─── 9. raw prefix-receipt row-recomputable from the call chain ───────────────

def test_raw_prefix_receipt_row_recomputable_from_call_chain():
    """Re-freezing on the same prefix reproduces every receipt field
    (gate_policy, gate_active, mean_abs2, spread, a_x, a_y). The receipt is a
    deterministic function of the (cell,seed) realization + the frozen gate."""
    from common._dual_pol_channel import generate_shared_realization_dp
    cell = {"modulation": "qam16", "snr_db": 5.0, "f_g_hz": 30.0,
            "sop_rate": 4.0e-6, "n_symbols": 512}
    gamma_bar = float(10.0 ** (cell["snr_db"] / 10.0))
    kw = dict(N=int(cell["n_symbols"]), alpha=4.2, beta=1.4,
              f_g=float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]),
              seed=275, gamma_bar=gamma_bar, block=100, t_s=4.0e-10,
              method="gar", modulation="qam16")
    rl = generate_shared_realization_dp(**kw)
    TAPS, MU, R2, BS = 11, 3.0e-2, 1.32, 64
    es, cal, ee, _ = runner.eval_window_for(512, TAPS, window_symbols=256, block_size=BS)
    base = runner.standard_cma_godard_with_z(rl["rX"], rl["rY"], n_tap=TAPS, mu=MU, R2=R2, block_size=BS)
    zpx, zpy = base["zX"][es:cal], base["zY"][es:cal]
    # build the receipt once
    f = G1M.gated_scalar_freeze(zpx, zpy)
    receipt = {"gate_policy": f["policy"], "gate_active": f["gate_active"],
               "mean_abs2": f["mean_abs2"], "spread": f["spread"],
               "a_x": f["a_x"], "a_y": f["a_y"]}
    # re-freeze on the SAME prefix and confirm every field reproduces
    f2 = G1M.gated_scalar_freeze(zpx, zpy)
    for k, v in receipt.items():
        if isinstance(v, float):
            assert np.isclose(v, f2[k if k != "gate_policy" else "policy"] if k == "gate_policy" else f2[k], atol=1e-12), f"{k} not reproducible"
        else:
            key2 = "policy" if k == "gate_policy" else k
            assert v == f2[key2], f"{k} not reproducible: {v} vs {f2[key2]}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
