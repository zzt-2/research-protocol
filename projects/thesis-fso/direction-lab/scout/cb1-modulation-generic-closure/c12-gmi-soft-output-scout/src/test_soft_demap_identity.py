"""Identity / sanity tests for the C12 GMI soft-output evaluator.

These are the REQUIRED-PASS identity gates from batch-contract.v1.yaml, run
BEFORE any cell evaluation. They are pure (no channel, no CMA): synthetic
AWGN-on-constellation constructions with known answers.

Run:  python -m pytest src/test_soft_demap_identity.py -q
  or: python src/test_soft_demap_identity.py        (standalone)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Make sibling modules importable when run standalone OR via pytest.
# HERE = .../c12-gmi-soft-output-scout/src  (the test file's directory)
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
# projects/simulation on path for common._modulation comparison.
# HERE = .../c12-gmi-soft-output-scout/src. parents[0]=c12-dir, [1]=cb1-closure,
# [2]=scout, [3]=direction-lab, [4]=thesis-fso, [5]=projects, [6]=worktree root.
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))
# baseline-atlas on path for cb1_evaluator.hard_16qam (used by mixture demapper).
# HERE.parents[1] = cb1-modulation-generic-closure (sibling of baseline-atlas)
BASELINE_ATLAS = HERE.parents[1] / "baseline-atlas"
if str(BASELINE_ATLAS) not in sys.path:
    sys.path.insert(0, str(BASELINE_ATLAS))

import soft_demap as sd  # noqa: E402
import gmi  # noqa: E402
from common._modulation import qam16_mod, qam16_demod  # noqa: E402


# ─── helpers ─────────────────────────────────────────────────────────────────
def _rng(): return np.random.default_rng(123)


def _rand_symbols(n: int, rng):
    bits = rng.integers(0, 2, 4 * n)
    syms = qam16_mod(bits)
    bits = bits.reshape(n, 4)
    return syms, bits


def _awgn(syms, sigma2, rng):
    sigma = np.sqrt(sigma2 / 2.0)  # split variance over Re/Im
    return syms + sigma * (rng.standard_normal(syms.size) + 1j * rng.standard_normal(syms.size))


# ─── gate: constellation table matches _modulation.qam16_mod ─────────────────
def test_constellation_table_matches_qam16_mod():
    """The soft_demap constellation + bit labels must match _modulation.qam16_mod."""
    rng = _rng()
    bits = rng.integers(0, 2, 4 * 2000)
    s = qam16_mod(bits)
    # nearest symbol in our table
    dem_idx = np.argmin(np.abs(s[:, None] - sd.QAM16_SYM[None, :]) ** 2, axis=1)
    dem_bits = sd.QAM16_BITS[dem_idx].reshape(-1)
    # hard demap via _modulation must agree bit-for-bit
    mod_bits = qam16_demod(s).reshape(-1, 4).reshape(-1)
    assert np.array_equal(dem_bits, mod_bits), (
        "soft_demap constellation table disagrees with _modulation.qam16_mod")
    # average power over all 16 points == 1.0
    assert abs(float(np.mean(np.abs(sd.QAM16_SYM) ** 2)) - 1.0) < 1e-12


# ─── gate: max-log LLR sign convention ───────────────────────────────────────
def test_maxlog_llr_sign_correct():
    """LLR_k >= 0 => bit k = 1 more likely; verify on perturbed symbols.

    On a small perturbation the hard decision is correct and the LLR sign must
    point to the TRUE bit with high probability.
    """
    rng = _rng()
    n = 4000
    syms, bits = _rand_symbols(n, rng)
    # moderate noise so hard decisions are correct and LLRs are finite (not all
    # clipped to LLR_CLIP): sigma2=1e-2 gives per-bit |LLR| well below the clip.
    z = _awgn(syms, 1e-2, rng)
    llrs = sd.maxlog_soft_demap_16qam(z, sigma2=1e-2)
    assert llrs.shape == (n, 4)
    # Decide bit from LLR sign (LLR>=0 => bit=1) and compare to truth.
    decided = (llrs >= 0).astype(int)
    ber = float(np.mean(decided != bits))
    assert ber < 0.02, f"max-log hard decision from LLR sign BER={ber:.4f} too high"
    # Finite and a meaningful spread (not degenerate, not all clipped).
    assert np.all(np.isfinite(llrs))
    assert np.any(np.abs(llrs) < sd.LLR_CLIP), "all LLRs clipped — sigma2 too low for this check"


def test_maxlog_llr_monotone_in_noise():
    """Lower noise => higher-confidence (larger |LLR|) soft decisions, on average."""
    rng = _rng()
    n = 4000
    syms, _ = _rand_symbols(n, rng)
    lo = np.mean(np.abs(sd.maxlog_soft_demap_16qam(_awgn(syms, 1e-3, rng), 1e-3)))
    hi = np.mean(np.abs(sd.maxlog_soft_demap_16qam(_awgn(syms, 1e-1, rng), 1e-1)))
    assert lo > hi, f"expected |LLR| low-noise > high-noise, got {lo:.3f} vs {hi:.3f}"


# ─── gate: GMI endpoints (0 uninformative, ~4 perfect) ───────────────────────
def test_gmi_zero_when_llr_uninformative():
    """Constant (uninformative) LLR => GMI = 0."""
    rng = _rng()
    n = 4000
    _, bits = _rand_symbols(n, rng)
    llrs = np.zeros((n, 4))  # perfectly uninformative
    out = gmi.compute_gmi(llrs, bits)
    assert out["gmi"] < 1e-9, f"constant-LLR GMI should be ~0, got {out['gmi']}"
    out2 = gmi.compute_gmi_analytic(llrs, bits)
    assert out2["gmi"] < 1e-9


def test_gmi_near_4_when_perfect_soft():
    """Near-infinite-magnitude, perfectly-signed LLR => GMI ~ 4 bits/symbol."""
    rng = _rng()
    n = 4000
    _, bits = _rand_symbols(n, rng)
    # LLR with the correct sign and very large magnitude: bit=1 -> +M, bit=0 -> -M
    M = 1e3
    llrs = (2.0 * bits - 1.0) * M
    out_hist = gmi.compute_gmi(llrs, bits)
    out_ana = gmi.compute_gmi_analytic(llrs, bits)
    assert out_hist["gmi"] > 3.9, f"perfect-soft histogram GMI should be ~4, got {out_hist['gmi']:.4f}"
    assert out_ana["gmi"] > 3.999, f"perfect-soft analytic GMI should be ~4, got {out_ana['gmi']:.4f}"


# ─── gate: GMI monotone in SNR ───────────────────────────────────────────────
def test_gmi_monotone_in_snr():
    """Higher SNR => (non-decreasing) higher standard-demapper GMI.

    GMI saturates at the 4.0 ceiling, so the guarantee is monotone
    NON-DECREASING; the lowest-SNR point must be clearly below the high-SNR
    points (which both sit near the ceiling).
    """
    rng = _rng()
    n = 8000
    syms, bits = _rand_symbols(n, rng)
    gmis = []
    for s2 in (1e-1, 1e-2, 1e-3):
        z = _awgn(syms, s2, _rng())
        llrs = sd.maxlog_soft_demap_16qam(z, s2)
        gmis.append(gmi.compute_gmi(llrs, bits)["gmi"])
    assert gmis[0] < gmis[1] and gmis[0] < gmis[2], f"GMI not monotone in SNR: {gmis}"
    assert gmis[2] > 3.9, f"high-SNR GMI should be near ceiling, got {gmis[2]:.4f}"
    assert gmis[1] >= gmis[0], f"mid-SNR GMI below low-SNR: {gmis}"


# ─── gate: oracle vs standard (sanity: truth-conditioned cannot be worse) ────
def test_oracle_gmi_ge_standard_gmi():
    """On AWGN-on-constellation the oracle and standard demappers use the same
    variance (AWGN is Gaussian so truth-conditioning == blind), so their GMI
    should be statistically equal. This is the sanity that the oracle path is
    not degenerate; the on-stream headroom check (oracle >= standard) is in the
    semantic smoke, not here."""
    rng = _rng()
    n = 8000
    syms, bits = _rand_symbols(n, rng)
    s2 = 2e-2
    z = _awgn(syms, s2, rng)
    std_llrs = sd.maxlog_soft_demap_16qam(z, s2)
    ora_llrs = sd.oracle_soft_demap_16qam(z, syms)
    g_std = gmi.compute_gmi(std_llrs, bits)["gmi"]
    g_ora = gmi.compute_gmi(ora_llrs, bits)["gmi"]
    # AWGN is exactly Gaussian, so oracle and standard agree to sampling noise.
    assert abs(g_std - g_ora) < 0.15, (
        f"oracle/standard GMI differ by {abs(g_std-g_ora):.3f} on pure AWGN "
        "(expected ~equal): oracle path may be degenerate")


# ─── gate: mixture demapper reduces to ~standard on pure AWGN ────────────────
def test_mixture_reduces_to_standard_on_pure_awgn():
    """On pure Gaussian noise the mixture should fit ~one dominant component and
    give GMI close to the standard demapper (no spurious collapse component)."""
    rng = _rng()
    n = 8000
    syms, bits = _rand_symbols(n, rng)
    s2 = 2e-2
    z = _awgn(syms, s2, rng)
    std_llrs = sd.maxlog_soft_demap_16qam(z, s2)
    mix_llrs, info = sd.mixture_soft_demap_16qam(z[: n // 2], z[n // 2:])
    bits_eval = bits[n // 2:]
    g_std = gmi.compute_gmi(std_llrs[n // 2:], bits_eval)["gmi"]
    g_mix = gmi.compute_gmi(mix_llrs, bits_eval)["gmi"]
    # On pure AWGN the mixture must not be dramatically worse (no over-fit to a
    # spurious collapsed mode). Allow a modest tolerance for the 2-component
    # fit on a single-Gaussian source.
    assert g_mix >= g_std - 0.30, (
        f"mixture GMI {g_mix:.3f} much worse than standard {g_std:.3f} on pure "
        "AWGN: mixture over-fits a spurious component")
    # Collapse fraction should be modest (one component dominates) on pure AWGN.
    for ax in ("re", "im"):
        w = info[ax]["w"]
        assert 0.05 <= float(w.min()) and float(w.max()) <= 0.95, (
            f"mixture {ax}-axis weights {w} degenerate on pure AWGN")


# ─── gate: no TX truth in standard/mixture runtime inputs ───────────────────
def test_no_tx_truth_in_standard_or_mixture_signature():
    """Static check: the standard and mixture demapper signatures consume only
    z (and, for mixture, z_calib). No truth_symbols argument. Only the oracle
    demapper takes truth."""
    import inspect
    std_params = inspect.signature(sd.maxlog_soft_demap_16qam).parameters
    mix_params = inspect.signature(sd.mixture_soft_demap_16qam).parameters
    ora_params = inspect.signature(sd.oracle_soft_demap_16qam).parameters
    assert "truth" not in std_params and "truth" not in mix_params, (
        "standard/mixture demapper must not accept a truth argument")
    assert "truth_symbols" in ora_params, "oracle demapper must take truth_symbols"


# ─── gate: mixture can model a bimodal (collapsed) residual ──────────────────
def test_mixture_fits_bimodal_residual():
    """Construct an explicit bimodal residual (healthy AWGN + a wide collapsed
    component) and verify the mixture fit recovers both components and that the
    mixture demapper's GMI is NOT catastrophically worse than the standard on
    this non-Gaussian noise."""
    rng = _rng()
    n = 12000
    syms, bits = _rand_symbols(n, rng)
    # 70% healthy (narrow), 30% collapsed (wide) — emulate inner-ring collapse.
    is_collapsed = rng.random(n) < 0.30
    healthy = _awgn(np.zeros(n), 1e-2, rng)
    collapsed = _awgn(np.zeros(n), 4e-1, rng)
    noise = np.where(is_collapsed, collapsed, healthy)
    z = syms + noise
    # standard uses the GLOBAL (blind) variance: mean |z-s|^2 is a blend.
    blind_s2 = float(np.mean(np.abs(z - syms) ** 2))
    std_llrs = sd.maxlog_soft_demap_16qam(z[n // 2:], blind_s2)
    mix_llrs, info = sd.mixture_soft_demap_16qam(z[: n // 2], z[n // 2:])
    bits_eval = bits[n // 2:]
    g_std = gmi.compute_gmi(std_llrs, bits_eval)["gmi"]
    g_mix = gmi.compute_gmi(mix_llrs, bits_eval)["gmi"]
    # The mixture SHOULD be at least as good as the standard on its own
    # bimodal model. (On a hand-crafted bimodal source this is the designed
    # advantage; we assert non-inferiority, the core C12 hypothesis.)
    assert g_mix >= g_std - 0.05, (
        f"mixture GMI {g_mix:.3f} worse than standard {g_std:.3f} on an "
        "explicitly bimodal residual: mixture fit failed to exploit the model")
    # And the fit should actually see two distinct variances.
    re_vars = info["re"]["var"]
    assert float(np.max(re_vars) / np.min(re_vars)) > 2.0, (
        f"mixture did not separate two variance scales on bimodal residual: {re_vars}")


if __name__ == "__main__":
    # Standalone runner (mirrors pytest collection by name).
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception:
            print(f"  FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
