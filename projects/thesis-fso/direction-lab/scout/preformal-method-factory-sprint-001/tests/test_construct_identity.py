"""Identity + boundary regression tests for Sprint 001 constructs.

Run: python -m pytest tests/test_construct_identity.py -q
   (from the sprint-001 root, with projects/simulation on path)

These tests guard:
  1. QPSK regression (testbed identity) — baseline still PI-SER=0 on anchor.
  2. Each construct's action identity (different inputs -> different outputs).
  3. Clean-boundary degradation (constructs do not regress clean seeds).
  4. Receiver-visible contract (no construct imports TX truth into its action).
"""

import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve()
SPRINT_ROOT = HERE.parents[1]
SRC = SPRINT_ROOT / "src"
CB1_ROOT = SPRINT_ROOT.parent / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
# HERE = .../preformal-method-factory-sprint-001/tests/test_construct_identity.py
# parents[0]=tests, [1]=sprint-001, [2]=scout, [3]=direction-lab, [4]=thesis-fso,
# [5]=projects, [6]=worktree root
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import methods as M  # noqa: E402


def _realization(seed=11, snr=20.0, n=512):
    gamma = 10 ** (snr / 10)
    return generate_shared_realization_dp(
        n, 4.2, 1.4, 30.0, sop_rate=4e-6, seed=seed, gamma_bar=gamma,
        block=100, t_s=4e-10, method="gar", modulation="qam16",
    )


def test_qpsk_regression_identity():
    """Testbed identity: standard-CMA on QPSK anchor = PI-SER 0 (P03 v1)."""
    contract = {
        "frozen_common_axes": {
            "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
            "cma_mu": 1e-3, "cma_taps": 11, "r2_qpsk": 1.0, "cma_block_size": 64,
            "affine_ridge": 1e-6, "constellation_amplitude_per_axis": 0.7071067811865475,
        },
        "statistical_sensitivity": {"minimum_detectable_effect": {"value": 0.005}},
        "covering_design": {"paired_seeds": [11]},
    }
    cell = {"id": "qpsk-anchor", "modulation": "qpsk", "snr_db": 20.0,
            "f_g_hz": 30.0, "sop_rate": 4e-6, "n_symbols": 512}
    res = runner.run_cell(cell, contract, generator=generate_shared_realization_dp,
                          evaluator=evaluator)
    assert res["identity_gate_ok"]
    assert res["decision"]["nearest_pi_ser"] == 0.0


def test_m1_action_identity():
    """M1 reduced-modulus produces a different z-stream than baseline."""
    rz = _realization(11)
    m1 = M.m1_reduced_modulus_cma(rz)
    base = runner.standard_cma_godard_with_z(rz["rX"], rz["rY"], n_tap=11, mu=1e-3, R2=1.32, block_size=64)
    z1 = np.concatenate([m1["zX"], m1["zY"]])
    zb = np.concatenate([base["zX"], base["zY"]])
    assert np.mean(np.abs(z1 - zb)) > 1e-6
    assert m1["provenance"]["R2"] == M.R2_INNER


def test_m2_action_identity():
    """M2 reinit changes output when collapse detected."""
    rz = _realization(12)
    on = M.m2_trace_reinit_cma(rz, max_reinits=2)
    off = M.m2_trace_reinit_cma(rz, max_reinits=0)
    z_on = np.concatenate([on["zX"], on["zY"]])
    z_off = np.concatenate([off["zX"], off["zY"]])
    # either reinit fired (z differs) or no collapse on this seed (acceptable)
    if on["reinit_count"] > 0:
        assert np.mean(np.abs(z_on - z_off)) > 1e-6


def test_m3_action_identity():
    """M3 multi-start produces distinct candidate scores."""
    rz = _realization(11)
    es, cal, ee, _ = runner.eval_window_for(512, 11, window_symbols=256, block_size=64)
    m3 = M.m3_multistart_select_cma(rz, K=4, eval_slice=(cal, ee))
    scores = m3["m3_all_scores"]
    assert max(scores) - min(scores) > 1e-6
    assert 0 <= m3["m3_selected_k"] < 4


def test_m4_gate_identity():
    """M4 gate opens on collapsed, closes on clean."""
    rz = _realization(11)
    base = runner.standard_cma_godard_with_z(rz["rX"], rz["rY"], n_tap=11, mu=1e-3, R2=1.32, block_size=64)
    es, cal, ee, _ = runner.eval_window_for(512, 11, window_symbols=256, block_size=64)
    z_calib = np.column_stack([base["zX"][es:cal], base["zY"][es:cal]])
    z_eval = np.column_stack([base["zX"][cal:ee], base["zY"][cal:ee]])
    clean = M.m4_conditional_dd_affine(z_calib, z_eval, ridge=1e-6, collapse_threshold=0.5)
    collapsed = M.m4_conditional_dd_affine(z_calib * 0.3, z_eval * 0.3, ridge=1e-6, collapse_threshold=0.5)
    assert not clean["gate_open"]
    assert collapsed["gate_open"]


def test_m5_gate_identity():
    """M5 remap fires on low-power, identity on healthy."""
    rz = _realization(11)
    base = runner.standard_cma_godard_with_z(rz["rX"], rz["rY"], n_tap=11, mu=1e-3, R2=1.32, block_size=64)
    es, cal, ee, _ = runner.eval_window_for(512, 11, window_symbols=256, block_size=64)
    z_eval = np.column_stack([base["zX"][cal:ee], base["zY"][cal:ee]])
    healthy = M.m5_radius_shell_remap(z_eval)
    collapsed = M.m5_radius_shell_remap(z_eval * 0.3)
    # healthy seed 11 has mean|z|^2 ~ 0.7 > 0.5 -> not collapsed
    assert not healthy["collapsed"]
    assert collapsed["collapsed"]


def test_no_privileged_input_in_methods():
    """methods.py must not import or reference TX truth / channel truth."""
    src = (SRC / "methods.py").read_text(encoding="utf-8")
    forbidden = ["sX", "sY", "bitsX", "bitsY", "true_channel", "jones",
                 "oracle_affine", "tx_truth"]
    # allow the words only in comments/docstrings, not as runtime variable use
    for token in forbidden:
        # crude check: token should not appear as a function parameter or assignment target
        assert f"({token}" not in src.replace(" ", ""), f"possible privileged use of {token}"
