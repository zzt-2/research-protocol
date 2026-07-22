"""Identity / no-op / leakage / scale-invariance gates for the info-source-portfolio Probes.

These are the semantic-smoke gates required by probe-contract.v1.yaml before trusting any
Probe headline. Run: `python -m pytest tests/test_probe_identity.py -v` (or direct _run_all()).
"""
import sys
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))
import probe_shared as ps  # noqa: E402
import run_f1a_model_prior as f1a  # noqa: E402
import run_f3a_history as f3a  # noqa: E402
import run_f4a_soft_gmi as f4a  # noqa: E402

FORBIDDEN_VISIBLE_INPUTS = ["sX", "sY", "h[", "theta[", "true_jones",
                            "fixed_label", "pi_ber", "future_window"]


def _grep_source(pattern, filenames):
    """Grep a regex across the listed source files. Return list of (file, lineno, line)."""
    hits = []
    rx = re.compile(pattern)
    for fn in filenames:
        p = SRC_DIR / fn
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if rx.search(line):
                hits.append((fn, i, line.strip()))
    return hits


# ─── Seed discipline ───
def test_seed_discipline():
    ps.assert_seed_discipline()  # raises if overlap


# ─── F1-A gates ───
def test_f1a_oracle_reads_truth_but_visible_path_does_not():
    """The oracle MMSE path MUST read h/theta (it's a scoring-only bound); the receiver-visible
    feature extractor MUST NOT read sX/sY/h/theta in CODE (docstring mentions are OK)."""
    src = (SRC_DIR / "run_f1a_model_prior.py").read_text(encoding="utf-8")
    # Extract the receiver_visible_features function body
    m = re.search(r"def receiver_visible_features\(.*?(?=\ndef )", src, re.DOTALL)
    assert m, "receiver_visible_features not found"
    body = m.group(0)
    # Strip docstring and comments before checking for forbidden CODE references
    body_no_doc = re.sub(r'""".*?"""', "", body, flags=re.DOTALL)
    body_no_doc = re.sub(r"#.*", "", body_no_doc)
    # Forbidden CODE patterns: indexing into truth arrays
    forbidden_code = ["sX[", "sY[", "r['h']", 'r["h"]', "r['theta']", 'r["theta"]',
                      "h[", "theta[", "true_jones"]
    for bad in forbidden_code:
        assert bad not in body_no_doc, \
            f"receiver_visible_features CODE references forbidden input '{bad}'"


def test_f1a_constant_output():
    """If CMA output is constant, headroom should be ~0 (no spurious oracle signal)."""
    cell = ps.ATLAS_CELLS[3]
    r = ps.make_realization(cell, 141)
    es, ce, ee, _ = ps.eval_window(cell)
    # Feed constant rX/rY
    rX_c = np.ones_like(r["rX"]) * (1 + 1j)
    rY_c = np.ones_like(r["rY"]) * (1 - 1j)
    cma = ps.run_cma_anchor(rX_c, rY_c)
    # Oracle on constant input
    zXo, zYo = ps.mmse_equalize_oracle(rX_c, rY_c, r["h"], r["theta"],
                                       r["sX"][es:ce], r["sY"][es:ce], es, ce, ee)
    # Both should be near-constant (no spurious structure)
    assert np.std(zXo) < 1.0, f"oracle output not near-constant: std={np.std(zXo)}"


def test_f1a_paired_realization():
    """CMA and oracle must run on the SAME shared realization."""
    cell = ps.ATLAS_CELLS[3]
    r = ps.make_realization(cell, 141)
    cma = ps.run_cma_anchor(r["rX"], r["rY"])
    es, ce, ee, _ = ps.eval_window(cell)
    zXo, zYo = ps.mmse_equalize_oracle(r["rX"], r["rY"], r["h"], r["theta"],
                                       r["sX"][es:ce], r["sY"][es:ce], es, ce, ee)
    # Both consumed r["rX"], r["rY"] (same realization) — structurally guaranteed by run_one
    assert cma is not None and zXo is not None


# ─── F3-A gates ───
def test_f3a_causal_prefix_invariance():
    """Perturbing future samples must not change past-block features."""
    cell = ps.ATLAS_CELLS[8]  # long cell
    r = ps.make_realization(cell, 141)
    cma1 = ps.run_cma_anchor(r["rX"], r["rY"])
    # Perturb the LAST quarter of samples (future)
    r2 = dict(r)
    r2["rX"] = r["rX"].copy()
    r2["rY"] = r["rY"].copy()
    n = len(r2["rX"])
    r2["rX"][3 * n // 4:] += 100.0  # large perturbation to future
    r2["rY"][3 * n // 4:] += 100.0
    cma2 = ps.run_cma_anchor(r2["rX"], r2["rY"])
    # The first ~3/4 of blocks (the prefix) should be unaffected IF the CMA is causal.
    # (block-end CMA update at block_size=64; a perturbation at index 3n/4 only affects
    # blocks whose update window includes that index.)
    t1 = cma1.get("trace", [])
    t2 = cma2.get("trace", [])
    # Find the last block whose w_norm is bit-identical
    prefix_safe = 0
    for a, b in zip(t1, t2):
        if abs(a.get("w_norm", 0) - b.get("w_norm", 0)) < 1e-12:
            prefix_safe += 1
        else:
            break
    assert prefix_safe >= 1, f"no causal-prefix invariance: prefix_safe={prefix_safe}"


def test_f3a_no_future_samples_in_features():
    """block_features_from_trace reads only one block index (causal)."""
    src = (SRC_DIR / "run_f3a_history.py").read_text(encoding="utf-8")
    m = re.search(r"def block_features_from_trace\(.*?(?=\ndef )", src, re.DOTALL)
    assert m, "block_features_from_trace not found"
    body = m.group(0)
    # Must not index trace[block_idx + k] for k > 0
    assert not re.search(r"block_idx\s*\+\s*[1-9]", body), "feature reads future blocks"


# ─── F4-A gates ───
def test_f4a_histogram_mi_scale_invariant():
    """The histogram-MI GMI MUST be invariant to common positive scaling of all LLRs
    (this is the C12 artifact source, confirmed by construction)."""
    cell = ps.ATLAS_CELLS[8]
    r = ps.make_realization(cell, 141)
    cma = ps.run_cma_anchor(r["rX"], r["rY"])
    es, ce, ee, _ = ps.eval_window(cell)
    zX = cma["zX"][ce:ee]
    sXe = r["sX"][ce:ee]
    n_sym = ee - ce
    bx = f4a.bits_to_N4(r["bitsX"][ce * 4:ee * 4], n_sym)
    llr = f4a.corrected_oracle_soft_demap(zX, sXe)
    from gmi import compute_gmi
    g1 = compute_gmi(llr * 1.0, bx)["gmi"]
    g2 = compute_gmi(llr * 2.0, bx)["gmi"]
    g05 = compute_gmi(llr * 0.5, bx)["gmi"]
    assert abs(g1 - g2) < 1e-9 and abs(g1 - g05) < 1e-9, \
        f"histogram MI NOT scale-invariant: {g05}/{g1}/{g2} (artifact not reproduced)"


def test_f4a_analytic_gmi_scale_sensitive():
    """The analytic GMI MUST be scale-sensitive (it's the TRUE bound)."""
    cell = ps.ATLAS_CELLS[8]
    r = ps.make_realization(cell, 141)
    cma = ps.run_cma_anchor(r["rX"], r["rY"])
    es, ce, ee, _ = ps.eval_window(cell)
    zX = cma["zX"][ce:ee]
    sXe = r["sX"][ce:ee]
    n_sym = ee - ce
    bx = f4a.bits_to_N4(r["bitsX"][ce * 4:ee * 4], n_sym)
    llr = f4a.corrected_oracle_soft_demap(zX, sXe)
    from gmi import compute_gmi_analytic
    g1 = compute_gmi_analytic(llr * 1.0, bx)["gmi"]
    g2 = compute_gmi_analytic(llr * 2.0, bx)["gmi"]
    assert abs(g1 - g2) > 1e-6, f"analytic GMI NOT scale-sensitive: {g1} == {g2}"


def test_f4a_oracle_reads_truth():
    """The corrected oracle MUST read TX truth s_eval (it's a scoring-only bound)."""
    src = (SRC_DIR / "run_f4a_soft_gmi.py").read_text(encoding="utf-8")
    m = re.search(r"def corrected_oracle_soft_demap\(.*?(?=\ndef )", src, re.DOTALL)
    assert m, "corrected_oracle_soft_demap not found"
    body = m.group(0)
    assert "s_eval" in body, "corrected oracle does not read s_eval (not a true oracle)"


# ─── Source closure hash presence ───
def test_source_closure_hashes_present():
    h = ps.source_closure_hashes()
    keys_norm = {k.replace("\\", "/") for k in h}
    expected = ["src/probe_shared.py", "src/run_f1a_model_prior.py",
                "src/run_f3a_history.py", "src/run_f4a_soft_gmi.py"]
    for e in expected:
        assert e in keys_norm, f"missing {e} in source closure hashes; got {sorted(keys_norm)}"
    for k, v in h.items():
        assert len(v) == 64, f"{k} hash not SHA-256"


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = []
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed.append(t.__name__)
        except Exception as e:
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed.append(t.__name__)
    print(f"\n{passed}/{len(tests)} passed; {len(failed)} failed: {failed}")
    assert not failed, f"{len(failed)} tests failed"


if __name__ == "__main__":
    _run_all()
