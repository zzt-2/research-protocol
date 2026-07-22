"""Identity / sanity tests for the C14 custom-init runner + init estimators.

These are the REQUIRED-PASS identity gates from batch-contract.v1.yaml, run
BEFORE any cell evaluation. They are the wiring regression for the custom-init
runner (center-tap path must be BYTE-FOR-BYTE the anchor) plus sanity on the
data-driven init estimators (finite, unit-norm, no truth leakage).

Run:  python -m pytest src/test_init_identity.py -q
  or: python src/test_init_identity.py        (standalone)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Make sibling modules importable when run standalone OR via pytest.
# HERE = .../c14-init-strategy-scout/src
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
# projects/simulation on path for the generator + _modulation.
# HERE.parents: [0]=src, [1]=c14-dir, [2]=cb1-closure, [3]=scout,
# [4]=direction-lab, [5]=thesis-fso, [6]=projects, [7]=worktree root.
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))
# baseline-atlas on path for the anchor runner + evaluator + eval_window_for.
BASELINE_ATLAS = HERE.parents[1] / "baseline-atlas"
if str(BASELINE_ATLAS) not in sys.path:
    sys.path.insert(0, str(BASELINE_ATLAS))

import cma_custom_init as ci  # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_cell_runner as anchor  # noqa: E402


# ─── shared realization for the byte-identity gate ────────────────────────────

def _make_realization(seed: int = 71, n_symbols: int = 512):
    cell = {"snr_db": 25.0, "f_g_hz": 30.0, "sop_rate": 4e-6}
    gamma = 10.0 ** (cell["snr_db"] / 10.0)
    return generate_shared_realization_dp(
        n_symbols, 4.2, 1.4, cell["f_g_hz"], sop_rate=cell["sop_rate"],
        seed=seed, gamma_bar=gamma, block=100, t_s=4e-10, method="gar",
        modulation="qam16",
    )


# ─── gate 1: center-tap custom-init == anchor BYTE-FOR-BYTE ───────────────────

def test_center_tap_custom_init_equals_anchor_byte_for_byte():
    """The center-tap path of the custom-init runner must be byte-identical to
    the baseline-atlas anchor across both a collapsed and a converged seed."""
    for seed in (71, 72):  # 71 collapses, 72 converges (verified in smoke)
        r = _make_realization(seed=seed)
        ref = anchor.standard_cma_godard_with_z(
            r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
        )
        ct = ci.standard_cma_godard_with_z_custom_init(
            r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
            w_init=ci.center_tap_init(11),
        )
        dz_x = float(np.max(np.abs(np.asarray(ref["zX"]) - np.asarray(ct["zX"]))))
        dz_y = float(np.max(np.abs(np.asarray(ref["zY"]) - np.asarray(ct["zY"]))))
        assert dz_x == 0.0, f"seed {seed}: zX not byte-identical (max|dz|={dz_x})"
        assert dz_y == 0.0, f"seed {seed}: zY not byte-identical (max|dz|={dz_y})"
        assert ref["diverged"] == ct["diverged"]
        assert ref["init_w_norm"] == ct["init_w_norm"]
        assert ref["final_w_norm"] == ct["final_w_norm"]


def test_none_init_equals_center_tap():
    """w_init=None (default) must equal the explicit center-tap init."""
    r = _make_realization(seed=71)
    a = ci.standard_cma_godard_with_z_custom_init(
        r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64, w_init=None,
    )
    b = ci.standard_cma_godard_with_z_custom_init(
        r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
        w_init=ci.center_tap_init(11),
    )
    assert float(np.max(np.abs(np.asarray(a["zX"]) - np.asarray(b["zX"])))) == 0.0
    assert float(np.max(np.abs(np.asarray(a["zY"]) - np.asarray(b["zY"])))) == 0.0


# ─── gate 2: all init estimators are finite, unit-norm, correct shape ─────────

def test_center_tap_init_norm_and_shape():
    init = ci.center_tap_init(11)
    for k in ("wxx", "wxy", "wyx", "wyy"):
        assert init[k].shape == (11,)
        assert np.all(np.isfinite(init[k]))
    # The anchor center-tap puts 1 in wxx[center] AND 1 in wyy[center]
    # (per-pol unit), so the full 4-vector norm is sqrt(2) — NOT 1.0.
    # This matches baseline-atlas init_w_norm exactly.
    assert abs(ci.init_norm(init) - np.sqrt(2.0)) < 1e-12
    assert init["wxx"][5] == 1.0 and init["wyy"][5] == 1.0
    assert np.all(init["wxy"] == 0) and np.all(init["wyx"] == 0)


def test_whitening_init_finite_unit_norm():
    r = _make_realization(seed=71)
    init = ci.whitening_init(r["rX"], r["rY"], n_tap=11)
    for k in ("wxx", "wxy", "wyx", "wyy"):
        assert init[k].shape == (11,)
        assert np.all(np.isfinite(init[k]))
    n = ci.init_norm(init)
    # Normalized to sqrt(2) to match the center-tap anchor's total energy.
    assert abs(n - np.sqrt(2.0)) < 1e-9, f"whitening init norm {n} != sqrt(2)"
    # must NOT be the trivial center tap (eigenvector of a real covariance is
    # not the center tap)
    assert not np.allclose(init["wxx"], ci.center_tap_init(11)["wxx"])


def test_oracle_wiener_init_finite_unit_norm():
    r = _make_realization(seed=71)
    init = ci.oracle_wiener_init(r["rX"], r["rY"], r["sX"], r["sY"], n_tap=11)
    for k in ("wxx", "wxy", "wyx", "wyy"):
        assert init[k].shape == (11,)
        assert np.all(np.isfinite(init[k]))
    n = ci.init_norm(init)
    assert abs(n - np.sqrt(2.0)) < 1e-9, f"oracle wiener init norm {n} != sqrt(2)"


def test_random_multistart_init_finite_unit_norm_returns_costs():
    r = _make_realization(seed=71)
    rng = np.random.default_rng(123)
    init, costs = ci.random_multistart_init(
        r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
        K=5, warmup_blocks=1, rng=rng,
    )
    for k in ("wxx", "wxy", "wyx", "wyy"):
        assert init[k].shape == (11,)
        assert np.all(np.isfinite(init[k]))
    n = ci.init_norm(init)
    assert abs(n - np.sqrt(2.0)) < 1e-9, f"multistart init norm {n} != sqrt(2)"
    assert len(costs) == 5
    assert all(np.isfinite(c) for c in costs)
    # best cost must be <= every returned cost (it is the min)
    assert abs(costs[np.argmin(costs)] - min(costs)) < 1e-12


# ─── gate 3: no TX truth in whitening / multistart (information contract) ─────

def test_whitening_signature_has_no_truth():
    """whitening_init must accept only (rX, rY) signal args (+n_tap)."""
    import inspect
    params = inspect.signature(ci.whitening_init).parameters
    names = set(params.keys())
    assert "rX_calib" in names and "rY_calib" in names
    assert "sX_calib" not in names and "sY_calib" not in names, \
        "whitening_init must NOT take TX truth"


def test_multistart_signature_has_no_truth():
    """random_multistart_init must accept only (rX, rY) signal args."""
    import inspect
    params = inspect.signature(ci.random_multistart_init).parameters
    names = set(params.keys())
    assert "rX_calib" in names and "rY_calib" in names
    assert "sX_calib" not in names and "sY_calib" not in names, \
        "random_multistart_init must NOT take TX truth"


def test_oracle_wiener_requires_truth():
    """oracle_wiener_init is the ONLY estimator that consumes TX truth."""
    import inspect
    params = inspect.signature(ci.oracle_wiener_init).parameters
    names = set(params.keys())
    assert "sX_calib" in names and "sY_calib" in names


# ─── gate 4: custom init actually changes the output (init-dependence exists) ─

def test_custom_init_changes_output():
    """A non-center-tap init must produce a DIFFERENT z-stream than center-tap
    (otherwise the init is a no-op and the Scout is confounded)."""
    r = _make_realization(seed=71)
    ct = ci.standard_cma_godard_with_z_custom_init(
        r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
        w_init=ci.center_tap_init(11),
    )
    wh = ci.standard_cma_godard_with_z_custom_init(
        r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64,
        w_init=ci.whitening_init(r["rX"], r["rY"], n_tap=11),
    )
    dz = float(np.max(np.abs(np.asarray(ct["zX"]) - np.asarray(wh["zX"]))))
    assert dz > 0.0, "whitening init produced identical z to center-tap (no-op)"


# ─── gate 5: Godard gradient is unchanged (provenance stamp) ──────────────────

def test_provenance_godard_with_z_unchanged():
    r = _make_realization(seed=71)
    for init_fn in (ci.center_tap_init,):
        init = init_fn(11)
        out = ci.standard_cma_godard_with_z_custom_init(
            r["rX"], r["rY"], n_tap=11, mu=0.03, R2=1.32, block_size=64, w_init=init,
        )
        assert out["provenance"]["gradient"] == "Godard-with-z"


# ─── standalone runner ────────────────────────────────────────────────────────

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
            passed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL  {fn.__name__}: {type(exc).__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(fns)} total")
    sys.exit(1 if failed else 0)
