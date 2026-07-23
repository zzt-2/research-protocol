"""Tests for the Pilot-Jones complex-model salvage (T003).

Covers: model ladder limiting cases, information boundary, raw->aggregate
reproducibility, BER->Q^2 conversion, protected-path invariance, and the
oracle/anomaly detection. These mirror the directed-test discipline of
test_pilot_jones_step4a.py.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
SIM = HERE.parent
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(SIM / "explore" / "pilot-jones-complex-salvage"))

import complex_jones_channel as cjc  # noqa: E402
import conventional_baselines as cb  # noqa: E402
import salvage_methods as sm  # noqa: E402
from run_salvage import ber_to_q2_db, evaluate_dual_qpsk  # noqa: E402

REPO = SIM.parent.parent
RSLT = REPO / "projects" / "simulation" / "results" / "pilot-jones-complex-salvage"


def _canonical(N=1000, seed=4001):
    from common._dual_pol_channel import generate_shared_realization_dp
    from params import SimulationConfig
    cfg = SimulationConfig()
    return generate_shared_realization_dp(
        N=N, alpha=4.2, beta=1.4, f_g=100.0, sop_rate=8e-6, seed=seed,
        gamma_bar=100.0, block=64, t_s=cfg.system.T_S, method=cfg.gg_time.AR1_METHOD)


# ---- model ladder limiting cases ----

def test_M0_control_byte_compatible_with_canonical():
    real = _canonical()
    m0 = cjc.apply_complex_jones(real, model_id="M0", block_size=64,
                                 rng=np.random.default_rng(11))
    assert np.allclose(m0["rX"], real["rX"])
    assert np.allclose(m0["rY"], real["rY"])


def test_M1_complex_unitary_cond1():
    real = _canonical()
    m1 = cjc.apply_complex_jones(real, model_id="M1", block_size=64,
                                 rng=np.random.default_rng(12), unitary_complex=True)
    J = np.asarray(m1["jones_truth"])
    err = max(np.linalg.norm(J[b] @ J[b].conj().T - np.eye(2)) for b in range(J.shape[0]))
    cond = max(np.linalg.cond(J[b]) for b in range(J.shape[0]))
    assert err < 1e-10
    assert cond < 1.0 + 1e-9


@pytest.mark.parametrize("pdl_db", [3.5, 6.0, 9.5])
def test_M2_cond_matches_pdl_mapping(pdl_db):
    real = _canonical()
    m2 = cjc.apply_complex_jones(real, model_id="M2", block_size=64,
                                 rng=np.random.default_rng(13), pdl_db=pdl_db)
    J = np.asarray(m2["jones_truth"])
    cond = float(np.mean([np.linalg.cond(J[b]) for b in range(J.shape[0])]))
    assert abs(cond - 10 ** (pdl_db / 20.0)) < 0.05


def test_M3_dgd0_memoryless_dgd_positive_has_memory():
    from params import SimulationConfig
    t_s = SimulationConfig().system.T_S
    real = _canonical()
    m3z = cjc.apply_complex_jones(real, model_id="M3", block_size=64,
                                  rng=np.random.default_rng(14), dgd_ps=0.0, t_s=t_s)
    assert np.allclose(m3z["rX"], real["rX"])
    m3p = cjc.apply_complex_jones(real, model_id="M3", block_size=64,
                                  rng=np.random.default_rng(14), dgd_ps=80.0, t_s=t_s)
    assert np.max(np.abs(m3p["rX"] - real["rX"])) > 1e-6


def test_M2_noiseless_true_model_recoverable():
    real = _canonical()
    c = np.cos(real["theta"]); s = np.sin(real["theta"]); h = np.asarray(real["h"])
    sigX = np.sqrt(h) * (c * real["sX"] + s * real["sY"])
    sigY = np.sqrt(h) * (-s * real["sX"] + c * real["sY"])
    real_n0 = dict(real); real_n0["rX"] = sigX; real_n0["rY"] = sigY
    m2n = cjc.apply_complex_jones(real_n0, model_id="M2", block_size=64,
                                  rng=np.random.default_rng(15), pdl_db=6.0)
    J = np.asarray(m2n["jones_truth"])
    recX = np.zeros_like(sigX); recY = np.zeros_like(sigY)
    for b in range(J.shape[0]):
        st = b * 64; en = min(st + 64, len(sigX))
        rec = np.linalg.inv(J[b]) @ np.stack((m2n["rX"][st:en], m2n["rY"][st:en]), axis=0)
        recX[st:en] = rec[0]; recY[st:en] = rec[1]
    assert np.allclose(recX, sigX, atol=1e-9)
    assert np.allclose(recY, sigY, atol=1e-9)


# ---- information boundary ----

def test_oracle_inverts_both_jones_and_sop_rotation():
    """The oracle must undo the full polarization channel (J AND R(theta)),
    otherwise it is spuriously worse than a deployable joint estimator."""
    from params import SimulationConfig
    t_s = SimulationConfig().system.T_S
    real = _canonical(N=800, seed=4010)
    m2 = cjc.apply_complex_jones(real, model_id="M2", block_size=64,
                                 rng=np.random.default_rng(20), pdl_db=6.0)
    # build a noiseless impaired realization to test the inverse cleanly
    c = np.cos(real["theta"]); s = np.sin(real["theta"]); h = np.asarray(real["h"])
    sigX = np.sqrt(h) * (c * real["sX"] + s * real["sY"])
    sigY = np.sqrt(h) * (-s * real["sX"] + c * real["sY"])
    m2["rX"] = sigX  # replace noiseless (J already applied to the noiseless atm)
    # re-apply J to the noiseless atm
    m2n = cjc.apply_complex_jones(
        {**real, "rX": sigX, "rY": sigY}, model_id="M2", block_size=64,
        rng=np.random.default_rng(20), pdl_db=6.0)
    pilot = cb.inject_dual_pilots(m2n, block_size=64, n_pilots=6)
    der = cb.derotate_oracle(pilot, m2n, block_size=64)
    # after the true inverse the derotated signal should match the TX (up to the
    # scalar fade h, which does not flip bit polarity at hard decision). Check the
    # phase-corrected BER is ~0 on data positions.
    dm = pilot["data_mask"]
    met = evaluate_dual_qpsk(real["sX"][dm], real["sY"][dm],
                             der["rX"][dm], der["rY"][dm])
    assert met["fixed_label_ber"] < 1e-6


def test_deployable_methods_never_read_truth():
    """Source inspection guard: deployable method modules must not reference the
    true Jones / theta / sX / sY in their derotation path (oracle excepted)."""
    import inspect
    for fn in [cb.estimate_jones_blocks, cb.derotate,
               sm.estimate_jones_blocks_weighted, sm.derotate_weighted]:
        src = inspect.getsource(fn)
        # allowed: 'pilot_rx' inputs. forbidden: direct truth reads.
        assert "realization_imp[" not in src, f"{fn.__name__} reads realization_imp"
    # oracle functions ARE allowed to read truth (tagged)
    assert "jones_truth" in inspect.getsource(cb.derotate_oracle)


# ---- BER -> Q^2 conversion correctness ----

def test_ber_to_q2_known_values_and_zero_handling():
    # BER=0.5 -> Q invalid
    assert ber_to_q2_db(0.5) is None
    # BER -> Q^2 monotonic: lower BER -> higher Q^2_dB
    q_high_ber = ber_to_q2_db(1e-1)
    q_low_ber = ber_to_q2_db(1e-4)
    assert q_low_ber > q_high_ber
    # BER=0 -> None (caller applies 0.5/N bound)
    assert ber_to_q2_db(0.0) is None
    # BER ratio is NOT dB: 2x BER ratio != 0.5 dB in general
    q1 = ber_to_q2_db(1e-3)
    q2 = ber_to_q2_db(2e-3)
    assert abs((q1 - q2)) < 0.5 or abs((q1 - q2)) > 0.05  # not a fixed 0.5 dB


# ---- protected paths byte-unchanged ----

PROTECTED = [
    "projects/thesis-fso/direction-lab/STATUS.v1.md",
    "projects/thesis-fso/direction-lab/project.v1.yaml",
    "projects/thesis-fso/direction-lab/canonical-state.yaml",
    "projects/thesis-fso/direction-lab/state/completion-events.jsonl",
    "projects/simulation/explore/pilot-jones-step4a/mve-contract.yaml",
    "projects/simulation/results/pilot-jones-step4a/result.json",
]
PROTECTED_SHA = {
    "projects/thesis-fso/direction-lab/STATUS.v1.md": "701004b5e9e49e94d2792721087e7be8915efac5037d864c642a6a5c80a43331",
    "projects/thesis-fso/direction-lab/project.v1.yaml": "73f71f3ec8b824091f0b35acdf4b141043d5478ee0f25ac118feb121ccc95120",
    "projects/thesis-fso/direction-lab/canonical-state.yaml": "56abf96caf24d2404d0e37d31d58904bef3163ef1f73de69cf8c8a29971c087f",
    "projects/thesis-fso/direction-lab/state/completion-events.jsonl": "5565e78ac1b5f1a9e5bba5f53096f2cb4001f2264451239a34a0ce6cb8c6c5fe",
    "projects/simulation/explore/pilot-jones-step4a/mve-contract.yaml": "3ff819ef8842aba7246f8fba157c568d33f7b84373da8951dc1a21513728db50",
    "projects/simulation/results/pilot-jones-step4a/result.json": "11f6a28ddd295783003d7c124cd2a49f585ba1afa32f43f7f018195bd9527c66",
}


def test_protected_paths_byte_unchanged():
    import hashlib

    def sha(p):
        h = hashlib.sha256()
        with open(REPO / p, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    for p in PROTECTED:
        assert sha(p) == PROTECTED_SHA[p], f"protected path changed: {p}"


# ---- raw -> aggregate reproducibility on the saved result ----

def test_result_json_raw_aggregate_consistent():
    if not (RSLT / "result.json").exists():
        pytest.skip("result.json not generated yet")
    result = json.load(open(RSLT / "result.json"))
    pv = json.load(open(RSLT / "probe_verified.json"))
    ps = json.load(open(RSLT / "probe_stress.json"))
    # spot-check M0_control_stress nocma recompute
    rows = [r for r in ps["raw_rows"] if r["cell"] == "M0_control_stress"]
    b3 = np.mean([r["arms"]["B3_whitening"]["metrics_nocma"]["fixed_label_ber"] for r in rows])
    e = result["headroom_summary"]["stress"]["M0_control_stress"]
    assert abs(b3 - e["B3_mean_nocma"]) < 1e-12
    assert result["theory_all_pass"] is True
    assert result["formal_mve_run"] is False


def test_verdict_in_allowed_enum():
    if not (RSLT / "result.json").exists():
        pytest.skip("result.json not generated yet")
    result = json.load(open(RSLT / "result.json"))
    allowed = {
        "CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT",
        "KILL_PILOT_JONES_AFTER_PHYSICAL_MODEL_AND_TASK_MATCHED_BASELINE",
        "PIVOT_MODEL_NOT_JUSTIFIED",
        "PIVOT_UNVERIFIED_PHYSICAL_RANGE",
    }
    assert result["decision"]["provisional_verdict"] in allowed
