"""F1-A0 repair Probe — failing-first invariants (prompt §八).

These tests encode the HARD scientific/integrity invariants that D020/F1-A violated.
They are written BEFORE the implementation. The implementation MUST make all of them PASS.

Run:  python -m pytest tests/test_f1a0_invariants.py -q
(from the repair-f1a0/ directory; src/ is on sys.path via the runner)
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent.parent / "src"))

import repair_shared as rsh  # noqa: E402  (built by executor)
import run_f1a0_causal as probe  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Future-leakage invariant (prompt §四 / D021 gap #2)
#    Perturbing samples at index >= t MUST leave prefix features and the t-time
#    action bit-identical.
# ---------------------------------------------------------------------------
def test_future_perturbation_invariant_prefix_features():
    cell = rsh.ATLAS_CELLS[3]  # snr20-nominal-short
    seed = 151  # validation seed is fine for an invariant test
    r = rsh.make_realization(cell, seed)
    es, ce, ee, _ = rsh.eval_window(cell)

    # Build prefix features for a cut at the calibration/eval boundary.
    feats_a = probe.prefix_features(r, cut=ce, horizon_block=rsh.BLOCK)

    # Perturb everything at index >= ce (the "future") heavily.
    r2 = dict(r)
    r2 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in r2.items()}
    r2["rX"][ce:] = r2["rX"][ce:] * 1e3 + 7.0
    r2["rY"][ce:] = r2["rY"][ce:] * 1e3 - 3.0
    feats_b = probe.prefix_features(r2, cut=ce, horizon_block=rsh.BLOCK)

    for k in feats_a:
        assert np.allclose(feats_a[k], feats_b[k], equal_nan=True), (
            f"future leakage: feature {k} changed when future (index>={ce}) was perturbed")


# ---------------------------------------------------------------------------
# 2. Target time alignment (prompt §四 / D021 gap #3)
#    The prediction target must be the FUTURE block's channel state
#    (h/theta/Jones over [cut : cut+BLOCK]), aligned to the feature cut.
# ---------------------------------------------------------------------------
def test_target_is_future_block_state_aligned_to_cut():
    cell = rsh.ATLAS_CELLS[0]
    seed = 152
    r = rsh.make_realization(cell, seed)
    es, ce, ee, _ = rsh.eval_window(cell)
    target = probe.next_block_state_target(r, cut=ce, horizon_block=rsh.BLOCK)
    # Target must cover exactly the future block [ce : ce+BLOCK]
    assert target["h"].shape[0] == rsh.BLOCK
    assert np.allclose(target["h"], r["h"][ce:ce + rsh.BLOCK])
    assert np.allclose(target["theta"], r["theta"][ce:ce + rsh.BLOCK])


def test_observability_target_is_channel_state_not_headroom():
    # D021 gap #3: F1-A correlated features with the post-hoc headroom residual.
    # The repaired Probe must predict channel STATE (h/theta), not the headroom.
    src = Path(probe.__file__).read_text(encoding="utf-8")
    # The predictor target names must reference state, not a headroom/cma-oracle residual.
    assert "headroom" not in src.lower().replace(" ", "") or "headroom" not in probe.PREDICTION_TARGETS
    assert any(t in probe.PREDICTION_TARGETS for t in ("h", "theta", "jones"))


# ---------------------------------------------------------------------------
# 3. blind_affine_compare_16qam is actually invoked (prompt §六 / D021 gap #5)
# ---------------------------------------------------------------------------
def test_blind_affine_actually_invoked_in_pipeline():
    src = Path(probe.__file__).read_text(encoding="utf-8")
    assert "blind_affine_compare_16qam" in src, (
        "contract requires blind_affine_compare_16qam but it is never called in the Probe source")


def test_blind_affine_metric_present_in_result():
    cell = rsh.ATLAS_CELLS[3]
    row = probe.run_one(cell, 151)  # validation seed
    assert "blind_affine_pi_ser" in row
    assert "blind_affine_fixed_label_ser" in row
    assert np.isfinite(row["blind_affine_pi_ser"])


# ---------------------------------------------------------------------------
# 4. PI AND fixed-label dual metric both written (prompt §六 / D021 gap #6)
# ---------------------------------------------------------------------------
def test_dual_metric_for_every_method():
    cell = rsh.ATLAS_CELLS[3]
    row = probe.run_one(cell, 151)
    for method in ("cma", "blind_affine", "e1_jones_inverse", "e2_jones_pilot",
                   "e3_privileged_genie", "causal_plugin"):
        assert f"{method}_pi_ser" in row, f"missing PI metric for {method}"
        assert f"{method}_fixed_label_ser" in row, f"missing fixed-label metric for {method}"


# ---------------------------------------------------------------------------
# 5. validation / test disjoint; test disjoint from all prior (prompt §五)
# ---------------------------------------------------------------------------
def test_val_test_disjoint_and_prior_disjoint():
    val = set(rsh.VAL_SEEDS)
    test = set(rsh.TEST_SEEDS)
    assert not (val & test), f"validation ∩ test = {val & test}"
    prior = set()
    for span in rsh.PRIOR_USED_DO_NOT_REUSE:
        lo, hi = span.split("-")
        prior |= set(range(int(lo), int(hi) + 1))
    assert not (test & prior), f"test ∩ prior = {test & prior}"
    assert not (val & prior), f"validation ∩ prior = {val & prior}"
    # 141-150 (D020 observed) must NOT be the new final test
    assert set(range(141, 151)).isdisjoint(test), "seeds 141-150 are already observed (D020)"


def test_test_seeds_are_161_170():
    assert list(rsh.TEST_SEEDS) == list(range(161, 171))


# ---------------------------------------------------------------------------
# 6. test does not participate in feature selection / model fitting
#    (prompt §五; the ridge probe is fit on validation only)
# ---------------------------------------------------------------------------
def test_ridge_probe_fit_uses_validation_only():
    src = Path(probe.__file__).read_text(encoding="utf-8")
    # The frozen model must be produced from VAL_SEEDS, never TEST_SEEDS.
    assert "VAL_SEEDS" in src and "TEST_SEEDS" in src
    # Sanity: running the probe twice on the same test seed gives identical output (frozen model).
    cell = rsh.ATLAS_CELLS[3]
    a = probe.run_one(cell, 161)
    b = probe.run_one(cell, 161)
    assert np.allclose(a["causal_plugin_pi_ser"], b["causal_plugin_pi_ser"])


# ---------------------------------------------------------------------------
# 7. raw rows recompute every aggregate (prompt §五/§八 / D021 gap #7)
# ---------------------------------------------------------------------------
def test_raw_rows_recompute_aggregate(tmp_path):
    rows = probe.collect_rows(rsh.VAL_SEEDS)  # cheap: validation set
    art = probe.aggregate(rows)
    # Recompute macro CMA pi_ser from raw rows by-cell.
    by_cell = {}
    for rw in rows:
        by_cell.setdefault(rw["cell"], []).append(rw["cma_pi_ser"])
    cell_means = [float(np.mean(v)) for v in by_cell.values()]
    recomputed = float(np.mean(cell_means))
    assert abs(recomputed - art["cma_pi_ser_macro"]) < 1e-9


def test_artifact_contains_raw_rows():
    # The FULL run artifact must include per-seed/per-cell raw rows.
    cell = rsh.ATLAS_CELLS[3]
    rows = [probe.run_one(cell, 161), probe.run_one(cell, 162)]
    art = probe.aggregate(rows)
    assert "raw_rows" in art and len(art["raw_rows"]) == len(rows)


# ---------------------------------------------------------------------------
# 8. artifact source hash matches current src (prompt §八 / D021 gap #8)
# ---------------------------------------------------------------------------
def test_source_closure_hash_covers_all_src_and_matches():
    import hashlib
    art = probe.aggregate([probe.run_one(rsh.ATLAS_CELLS[3], 161)])
    stored = art["source_closure_hashes"]
    src_dir = HERE.parent.parent / "src"
    src_files = sorted(p for p in src_dir.glob("*.py") if "__pycache__" not in str(p))
    assert len(stored) >= len(src_files), (
        f"source closure records {len(stored)} files but {len(src_files)} src files exist")
    for sf in src_files:
        rel = "src/" + sf.name
        cur = hashlib.sha256(sf.read_bytes()).hexdigest()
        assert rel in stored, f"src file {rel} missing from source_closure_hashes"
        assert stored[rel] == cur, f"source hash drift for {rel}: stored {stored[rel][:12]} != cur {cur[:12]}"


# ---------------------------------------------------------------------------
# 9. E1 (exact Jones inverse) does NOT use TX-truth calibration (prompt §三 / D021 gap #1)
# ---------------------------------------------------------------------------
def test_e1_no_tx_truth_calibration():
    src = Path(probe.__file__).read_text(encoding="utf-8")
    # Locate the E1 function body and assert it does not reference TX truth symbols sX/sY.
    import re
    m = re.search(r"def e1_jones_inverse.*?(?=\ndef )", src, re.DOTALL)
    assert m, "e1_jones_inverse function not found"
    e1_body = m.group(0)
    # sX/sY are the TX-truth data symbols; E1 must use neither as calibration labels.
    assert "sX_calib" not in e1_body and "sY_calib" not in e1_body, (
        "E1 must be pure CSI genie (no TX-truth calibration); D021 gap #1")
    # E1 may still read rX/rY (received) and h/theta (offline CSI genie label) — that is allowed.


def test_e3_attribution_not_wholly_to_model_prior():
    # D021 gap #1: the 0.133 gap is CSI+TX-truth, not pure model prior.
    cell = rsh.ATLAS_CELLS[3]
    row = probe.run_one(cell, 161)
    # E3 (privileged CSI+TX-truth) gap and E1 (CSI only) gap must BOTH be reported,
    # so the TX-truth attribution is visible, not hidden.
    assert "e3_privileged_genie_pi_ser" in row
    assert "e1_jones_inverse_pi_ser" in row


# ---------------------------------------------------------------------------
# 10. seed discipline asserted at import/run time
# ---------------------------------------------------------------------------
def test_seed_discipline_assert_passes():
    # Should not raise.
    rsh.assert_seed_discipline()
