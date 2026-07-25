"""Orchestrator for the T006 high-order CPR combination method package.

Pipeline (all on the canonical star-ground GG link + uniform 16-QAM):
  Phase A  source closure + contract frozen (separate files).
  Phase B  semantic smoke gates (7 gates). Aborts on any failure.
  Phase C  B* selection: scan BPS (B, Nw) + VV Nw + DD-DPLL omega_n on
           VALIDATION; pick B* (strongest legal conventional).
  Phase D  headroom: per primary cell compute B* -> O Q^2 headroom on
           validation + test seeds. If all primary cells have point estimate
           AND CI upper < 0.5 dB -> KILL_NO_LEGAL_HEADROOM (no methods run).
  Phase E  (only if headroom survives): P1/P2/P3 mechanism slice + primary
           paired test. Pre-registered method verdict.
  Phase F  consolidated result + synthesis.

Determinism + closure: real SHA256 of contract + source; N/seed pools/cells
read FROM the frozen contract and asserted to match the runner.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]   # projects/simulation
# Put THIS directory first so flat module names (components, baselines,
# channel_helpers, semantic_gates) resolve here, and SIM so common.* resolves.
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(SIM) not in sys.path:
    sys.path.insert(0, str(SIM))

# Flat imports (directory has dashes -> cannot use package import).
import channel_helpers as ch_pkg
import baselines as B
import semantic_gates as SG
build_realization = ch_pkg.build_single_pol_qam16_with_pilots
ber_on_data = ch_pkg.ber_on_data
import components as components_mod

ROOT = SIM.parent.parent   # research-protocol root
RESULT_DIR = SIM / "results" / "high-order-cpr-combination"
EXPLORE_DIR = SIM / "explore" / "high-order-cpr-combination"

# ---------------------------------------------------------------------------
# Frozen grid (must match contract.yaml — asserted)
# ---------------------------------------------------------------------------

CONDITIONS = {
    "clean_control":     {"alpha": 11.6, "beta": 10.1, "gamma_bar": 100.0, "snr_db": 20.0},
    "operational":       {"alpha": 4.0,  "beta": 1.9,  "gamma_bar": 100.0, "snr_db": 20.0},
    "adversarial_sourced": {"alpha": 4.2, "beta": 1.4, "gamma_bar": 50.0,  "snr_db": 17.0},
    # stress cell (STRESS_ONLY — never sole basis for verdict)
    "stress_cfo_lw":     {"alpha": 4.0, "beta": 1.9, "gamma_bar": 100.0, "snr_db": 20.0,
                          "f_residual_hz": 1.0e7, "laser_lw_hz": 100.0e3},
}
COMMON = dict(
    N=8192, l_pilot_block=64, f_g=100.0, sop_rate=8.0e-6,
    f_residual_hz=1.0e5, f_dot_hz_per_s=0.0, laser_lw_hz=10.0e3,
)
SNR_GRID_DB = [14.0, 17.0, 20.0]    # frozen after validation sweep
VAL_SEEDS = [7600, 7601, 7602, 7603, 7604]
TEST_SEEDS = [7700, 7701, 7702, 7703, 7704, 7705, 7706, 7707, 7708, 7709]

# B* hyperparameter scan grid (validation only)
BPS_SCAN = [(32, 61), (32, 33), (64, 61), (16, 61)]
VV_SCAN = [32, 64, 128]
DDPLL_SCAN = [8e6, 20e6, 40e6]

# Combination method hyperparameters (validation-tuned defaults; can be frozen
# via a separate validation pass if needed)
P_DEFAULTS = dict(lam=0.99, delta=2.0, l_block=64, ml_window=7, innov_thr=0.3,
                  lam_lo=0.90, lam_hi=0.999, innov_scale=5.0)


# ---------------------------------------------------------------------------
# SHA closure (V039-style: real file SHA256, never the filename string)
# ---------------------------------------------------------------------------

def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_shas():
    rels = {
        "generator": "projects/simulation/common/_dual_pol_channel.py",
        "gg_time": "projects/simulation/common/_gg_time.py",
        "modulation": "projects/simulation/common/_modulation.py",
        "recovery": "projects/simulation/common/_recovery.py",
        "params": "projects/simulation/params.py",
        "contract": "projects/simulation/explore/high-order-cpr-combination/contract.yaml",
        "source_closure": "projects/simulation/explore/high-order-cpr-combination/source-closure.yaml",
        "components": "projects/simulation/explore/high-order-cpr-combination/components.py",
        "baselines": "projects/simulation/explore/high-order-cpr-combination/baselines.py",
        "channel_helpers": "projects/simulation/explore/high-order-cpr-combination/channel_helpers.py",
        "semantic_gates": "projects/simulation/explore/high-order-cpr-combination/semantic_gates.py",
        "runner": "projects/simulation/explore/high-order-cpr-combination/run_all.py",
    }
    return {k: _sha_file(os.path.join(ROOT, v)) for k, v in rels.items()
            if os.path.exists(os.path.join(ROOT, v))}


def contract_sha():
    return _sha_file(EXPLORE_DIR / "contract.yaml")


def closure_sha():
    return _sha_file(EXPLORE_DIR / "source-closure.yaml")


def _assert_closure():
    import yaml
    with open(EXPLORE_DIR / "contract.yaml") as f:
        c = yaml.safe_load(f)
    g = c["conditions"]
    for name, vals in CONDITIONS.items():
        if name == "stress_cfo_lw":
            continue   # stress cell not in primary contract grid
        assert name in g, f"contract missing condition {name}"
        assert g[name]["alpha"] == vals["alpha"], f"{name}: alpha mismatch"
        assert g[name]["beta"] == vals["beta"], f"{name}: beta mismatch"
        assert g[name]["gamma_bar"] == vals["gamma_bar"], f"{name}: gamma_bar mismatch"
    sp = c["seed_plan"]
    assert sp["headroom_validation_seeds"] == VAL_SEEDS, "val seeds mismatch"
    assert sp["headroom_test_seeds"] == TEST_SEEDS, "test seeds mismatch"
    excl = set(sp["excluded"])
    assert set(VAL_SEEDS).isdisjoint(excl), "val seeds overlap excluded"
    assert set(TEST_SEEDS).isdisjoint(excl), "test seeds overlap excluded"
    assert c["primary_modulation"]["type"] == "uniform 16-QAM"
    assert c["primary_modulation"]["bits_per_symbol"] == 4


# ---------------------------------------------------------------------------
# BER -> Q^2 (dB)
# ---------------------------------------------------------------------------

from math import erfc, log10, sqrt

def ber_to_q2_db(ber, n_eval=None):
    """BER -> Q^2 factor in dB. BER=0 -> bound by n_eval; BER>=0.5 -> None."""
    if ber is None or ber >= 0.5:
        return None
    if ber <= 0.0:
        if n_eval is None or n_eval <= 0:
            return None
        ber = 0.5 / n_eval   # conservative lower bound
    # invert Q(sqrt(2)*erfcinv(2*BER)); erfcinv via bisection on erfc
    # Q^-1(p) = (1/sqrt(2)) * erfcinv(2p); Q^2_dB = 20*log10(Q)
    target = 2.0 * ber
    # erfcinv: find x s.t. erfc(x) = target, x in [0, ~10]
    lo, hi = 0.0, 30.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if erfc(mid) > target:
            lo = mid
        else:
            hi = mid
    x = 0.5 * (lo + hi)
    Q = x / sqrt(2.0)
    if Q <= 0:
        return None
    return 20.0 * log10(Q)


# ---------------------------------------------------------------------------
# Run one realization through all arms
# ---------------------------------------------------------------------------

def _eval_resolve(rx_out, bits):
    return B.eval_resolve(rx_out, bits)


def run_arms(real, *, snr_db, bstar_cfg, run_methods=True):
    """Run all arms on one realization. Returns dict arm_name -> ber (on data)."""
    rx = real["rx"]
    bits = real["bits_data"]
    pilot_idx = real["pilot_idx"]
    pilot_sym = real["pilot_sym"]
    mask = real["data_mask"]
    phi_true = real["phi_true"]
    linewidth_hz = real["laser_lw_hz"]

    arms = {}
    # O (oracle, Kill only)
    rx_O = components_mod.truth_assisted_reference(rx, phi_true)
    arms["O"] = ber_on_data(_eval_resolve(rx_O, bits), bits, mask)
    # B* candidates
    rx_bps = B.arm_bps(rx, B=bstar_cfg["bps_B"], Nw=bstar_cfg["bps_Nw"])
    arms["BPS"] = ber_on_data(_eval_resolve(rx_bps, bits), bits, mask)
    rx_vv = B.arm_vv(rx, Nw=bstar_cfg["vv_Nw"])
    arms["VV"] = ber_on_data(_eval_resolve(rx_vv, bits), bits, mask)
    rx_dd = B.arm_dd_dpll(rx, omega_n=bstar_cfg["ddpll_omega"])
    arms["DDPLL"] = ber_on_data(_eval_resolve(rx_dd, bits), bits, mask)
    # B10 / B12 standalone
    rx_b10 = B.arm_b10(rx, pilot_idx, pilot_sym, lam=P_DEFAULTS["lam"])
    arms["B10"] = ber_on_data(_eval_resolve(rx_b10, bits), bits, mask)
    rx_b12 = B.arm_b12(rx, pilot_idx, pilot_sym, snr_db=snr_db,
                       linewidth_hz=linewidth_hz, l_block=P_DEFAULTS["l_block"],
                       ml_window=P_DEFAULTS["ml_window"])
    arms["B12"] = ber_on_data(_eval_resolve(rx_b12, bits), bits, mask)
    if run_methods:
        rx_p1 = B.arm_p1_cascade(rx, pilot_idx, pilot_sym, snr_db=snr_db,
                                  linewidth_hz=linewidth_hz,
                                  l_block=P_DEFAULTS["l_block"],
                                  ml_window=P_DEFAULTS["ml_window"], lam=P_DEFAULTS["lam"])
        arms["P1"] = ber_on_data(_eval_resolve(rx_p1, bits), bits, mask)
        rx_p2 = B.arm_p2_confidence_gate(
            rx, pilot_idx, pilot_sym, snr_db=snr_db, linewidth_hz=linewidth_hz,
            l_block=P_DEFAULTS["l_block"], ml_window=P_DEFAULTS["ml_window"],
            lam=P_DEFAULTS["lam"], innov_thr=P_DEFAULTS["innov_thr"])
        arms["P2"] = ber_on_data(_eval_resolve(rx_p2, bits), bits, mask)
        rx_p3 = B.arm_p3_adaptive_forgetting(
            rx, pilot_idx, pilot_sym, lam_lo=P_DEFAULTS["lam_lo"],
            lam_hi=P_DEFAULTS["lam_hi"], innov_scale=P_DEFAULTS["innov_scale"])
        arms["P3"] = ber_on_data(_eval_resolve(rx_p3, bits), bits, mask)
    return arms


# ---------------------------------------------------------------------------
# Phase B: semantic gates
# ---------------------------------------------------------------------------

def phase_b_gates():
    print("[phaseB] running 7 semantic gates...")
    res = SG.run_all_gates(seed=7600)
    print(f"[phaseB] overall_pass={res['overall_pass']}")
    for name, r in res["gates"].items():
        status = "PASS" if r["pass"] else "FAIL"
        print(f"  {name}: {status}")
    if not res["overall_pass"]:
        print("[phaseB] ABORT: a semantic gate failed.")
        return False, res
    return True, res


# ---------------------------------------------------------------------------
# Phase C: B* selection on VALIDATION
# ---------------------------------------------------------------------------

def phase_c_bstar_selection():
    """Scan BPS/VV/DD-DPLL hyperparameters on VALIDATION; pick strongest arm+cfg."""
    print("[phaseC] B* selection on validation (3 conditions x 3 SNR x 5 val seeds)...")
    # default cfg to scan over
    cfg_scores = {}
    for bps_B, bps_Nw in BPS_SCAN:
        cfg_scores[("BPS", bps_B, bps_Nw)] = []
    for vv_Nw in VV_SCAN:
        cfg_scores[("VV", vv_Nw)] = []
    for omega in DDPLL_SCAN:
        cfg_scores[("DDPLL", omega)] = []

    for cond_name, cond in CONDITIONS.items():
        if cond_name == "stress_cfo_lw":
            continue
        for snr_db in SNR_GRID_DB:
            for seed in VAL_SEEDS:
                f_res = cond.get("f_residual_hz", COMMON["f_residual_hz"])
                lw = cond.get("laser_lw_hz", COMMON["laser_lw_hz"])
                real = build_realization(
                    N=COMMON["N"], alpha=cond["alpha"], beta=cond["beta"],
                    gamma_bar=10.0 ** (snr_db / 10.0), f_g=COMMON["f_g"],
                    sop_rate=COMMON["sop_rate"], seed=seed,
                    l_pilot_block=COMMON["l_pilot_block"],
                    f_residual_hz=f_res, laser_lw_hz=lw)
                # BPS scan
                for bps_B, bps_Nw in BPS_SCAN:
                    rx_bps = B.arm_bps(rx=real["rx"], B=bps_B, Nw=bps_Nw)
                    ber = ber_on_data(_eval_resolve(rx_bps, real["bits_data"]),
                                      real["bits_data"], real["data_mask"])
                    cfg_scores[("BPS", bps_B, bps_Nw)].append(ber)
                for vv_Nw in VV_SCAN:
                    rx_vv = B.arm_vv(real["rx"], Nw=vv_Nw)
                    ber = ber_on_data(_eval_resolve(rx_vv, real["bits_data"]),
                                      real["bits_data"], real["data_mask"])
                    cfg_scores[("VV", vv_Nw)].append(ber)
                for omega in DDPLL_SCAN:
                    rx_dd = B.arm_dd_dpll(real["rx"], omega_n=omega)
                    ber = ber_on_data(_eval_resolve(rx_dd, real["bits_data"]),
                                      real["bits_data"], real["data_mask"])
                    cfg_scores[("DDPLL", omega)].append(ber)

    # pick the cfg with lowest mean BER
    means = {k: float(np.mean(v)) for k, v in cfg_scores.items()}
    best = min(means, key=means.get)
    # build a normalized bstar_cfg
    bstar_cfg = {"bps_B": 32, "bps_Nw": 61, "vv_Nw": 64, "ddpll_omega": 20e6}
    if best[0] == "BPS":
        bstar_cfg.update({"bps_B": best[1], "bps_Nw": best[2]})
        bstar_arm = "BPS"
    elif best[0] == "VV":
        bstar_cfg.update({"vv_Nw": best[1]})
        bstar_arm = "VV"
    else:
        bstar_cfg.update({"ddpll_omega": best[1]})
        bstar_arm = "DDPLL"
    print(f"[phaseC] best arm={bstar_arm}, cfg={bstar_cfg}, mean_BER={means[best]:.4e}")
    return bstar_arm, bstar_cfg, means


# ---------------------------------------------------------------------------
# Phase D: headroom gate (B* -> O)
# ---------------------------------------------------------------------------

def _bootstrap_ci(vals, n_boot=2000, seed=12345, stat=np.mean):
    if len(vals) == 0:
        return None
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, float)
    boots = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, len(arr), len(arr))
        boots[i] = stat(arr[idx])
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"mean": float(np.mean(vals)), "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(len(vals))}


def phase_d_headroom(bstar_arm, bstar_cfg):
    """Per primary cell: B* -> O Q^2 headroom on validation + test."""
    print("[phaseD] headroom gate (B* -> O) on 3 conditions x 3 SNR x 5 val + 10 test seeds...")
    rows_val = []
    rows_test = []
    for cond_name, cond in CONDITIONS.items():
        if cond_name == "stress_cfo_lw":
            continue   # stress cell excluded from primary headroom verdict
        for snr_db in SNR_GRID_DB:
            for seed in VAL_SEEDS:
                f_res = cond.get("f_residual_hz", COMMON["f_residual_hz"])
                lw = cond.get("laser_lw_hz", COMMON["laser_lw_hz"])
                real = build_realization(
                    N=COMMON["N"], alpha=cond["alpha"], beta=cond["beta"],
                    gamma_bar=10.0 ** (snr_db / 10.0), f_g=COMMON["f_g"],
                    sop_rate=COMMON["sop_rate"], seed=seed,
                    l_pilot_block=COMMON["l_pilot_block"],
                    f_residual_hz=f_res, laser_lw_hz=lw)
                arms = run_arms(real, snr_db=snr_db, bstar_cfg=bstar_cfg, run_methods=False)
                rows_val.append({
                    "cond": cond_name, "snr_db": snr_db, "seed": seed,
                    "n_eval": int(real["data_mask"].sum() * 4),
                    **arms,
                })
            for seed in TEST_SEEDS:
                f_res = cond.get("f_residual_hz", COMMON["f_residual_hz"])
                lw = cond.get("laser_lw_hz", COMMON["laser_lw_hz"])
                real = build_realization(
                    N=COMMON["N"], alpha=cond["alpha"], beta=cond["beta"],
                    gamma_bar=10.0 ** (snr_db / 10.0), f_g=COMMON["f_g"],
                    sop_rate=COMMON["sop_rate"], seed=seed,
                    l_pilot_block=COMMON["l_pilot_block"],
                    f_residual_hz=f_res, laser_lw_hz=lw)
                arms = run_arms(real, snr_db=snr_db, bstar_cfg=bstar_cfg, run_methods=False)
                rows_test.append({
                    "cond": cond_name, "snr_db": snr_db, "seed": seed,
                    "n_eval": int(real["data_mask"].sum() * 4),
                    **arms,
                })

    # per-cell headroom on TEST seeds (primary)
    primary = {}
    for cond_name in CONDITIONS:
        if cond_name == "stress_cfo_lw":
            continue
        for snr_db in SNR_GRID_DB:
            cell_rows = [r for r in rows_test
                         if r["cond"] == cond_name and r["snr_db"] == snr_db]
            n_eval = cell_rows[0]["n_eval"] if cell_rows else None
            # per-seed paired headroom (Q2_O - Q2_B*) in dB
            per_seed_headroom = []
            for r in cell_rows:
                qO = ber_to_q2_db(r["O"], n_eval)
                qB = ber_to_q2_db(r[bstar_arm], n_eval)
                if qO is not None and qB is not None:
                    per_seed_headroom.append(qO - qB)
            ci = _bootstrap_ci(per_seed_headroom) if per_seed_headroom else None
            key = f"{cond_name}|snr{snr_db}"
            primary[key] = {
                "bstar": bstar_arm,
                "n_seeds": len(cell_rows),
                "n_seeds_paired": len(per_seed_headroom),
                "per_seed_headroom_dB": [float(v) for v in per_seed_headroom],
                "mean_headroom_dB": ci["mean"] if ci else None,
                "bootstrap_95ci": {"lo": ci["ci_lo"], "hi": ci["ci_hi"]} if ci else None,
                "ci_upper_dB": ci["ci_hi"] if ci else None,
            }

    # KILL rule: ALL primary cells have mean < 0.5 AND ci_upper < 0.5
    all_below = all(
        e["mean_headroom_dB"] is not None and e["mean_headroom_dB"] < 0.5
        and e["ci_upper_dB"] is not None and e["ci_upper_dB"] < 0.5
        for e in primary.values()) if primary else False
    # SURVIVES: ANY primary cell has mean >= 0.5 AND ci_upper >= 0.5
    survivors = [k for k, e in primary.items()
                 if e["mean_headroom_dB"] is not None and e["mean_headroom_dB"] >= 0.5
                 and e["ci_upper_dB"] is not None and e["ci_upper_dB"] >= 0.5]
    if all_below:
        verdict = "KILL_NO_LEGAL_HEADROOM"
    elif survivors:
        verdict = "HEADROOM_SURVIVES"
    else:
        verdict = "UNRESOLVED_HEADROOM"
    return {
        "verdict": verdict,
        "primary_headroom": primary,
        "survivors": survivors,
        "rows_val": rows_val,
        "rows_test": rows_test,
        "max_point_dB": max((e["mean_headroom_dB"] or -9) for e in primary.values())
                        if primary else None,
        "max_ci_upper_dB": max((e["ci_upper_dB"] or -9) for e in primary.values())
                           if primary else None,
    }


# ---------------------------------------------------------------------------
# Phase E: method gate (only if headroom survives)
# ---------------------------------------------------------------------------

def phase_e_methods(bstar_arm, bstar_cfg):
    """Run P1/P2/P3 primary paired test. Pre-registered method verdict."""
    print("[phaseE] method gate (P1/P2/P3 vs B* and strongest standalone)...")
    rows_val = []
    rows_test = []
    for cond_name, cond in CONDITIONS.items():
        if cond_name == "stress_cfo_lw":
            continue
        for snr_db in SNR_GRID_DB:
            for seed in VAL_SEEDS + TEST_SEEDS:
                f_res = cond.get("f_residual_hz", COMMON["f_residual_hz"])
                lw = cond.get("laser_lw_hz", COMMON["laser_lw_hz"])
                real = build_realization(
                    N=COMMON["N"], alpha=cond["alpha"], beta=cond["beta"],
                    gamma_bar=10.0 ** (snr_db / 10.0), f_g=COMMON["f_g"],
                    sop_rate=COMMON["sop_rate"], seed=seed,
                    l_pilot_block=COMMON["l_pilot_block"],
                    f_residual_hz=f_res, laser_lw_hz=lw)
                arms = run_arms(real, snr_db=snr_db, bstar_cfg=bstar_cfg, run_methods=True)
                split = "val" if seed in VAL_SEEDS else "test"
                rows_val.append({"split": split, "cond": cond_name,
                                 "snr_db": snr_db, "seed": seed,
                                 "n_eval": int(real["data_mask"].sum() * 4),
                                 **arms})

    # method gate on TEST rows
    test_rows = [r for r in rows_val if r["split"] == "test"]
    primary = {}
    for cond_name in CONDITIONS:
        if cond_name == "stress_cfo_lw":
            continue
        for snr_db in SNR_GRID_DB:
            cell_rows = [r for r in test_rows
                         if r["cond"] == cond_name and r["snr_db"] == snr_db]
            n_eval = cell_rows[0]["n_eval"] if cell_rows else None
            entry = {"bstar": bstar_arm, "n_seeds": len(cell_rows)}
            for P in ("P1", "P2", "P3"):
                # paired Q2 gain over B* and over strongest standalone (max(B10,B12))
                gains_bstar = []
                gains_strong = []
                wins_bstar = 0
                wins_strong = 0
                for r in cell_rows:
                    qP = ber_to_q2_db(r[P], n_eval)
                    qB = ber_to_q2_db(r[bstar_arm], n_eval)
                    q10 = ber_to_q2_db(r["B10"], n_eval)
                    q12 = ber_to_q2_db(r["B12"], n_eval)
                    q_strong = max([q for q in (q10, q12) if q is not None], default=None)
                    if qP is not None and qB is not None:
                        gains_bstar.append(qP - qB)
                        if qP > qB:
                            wins_bstar += 1
                    if qP is not None and q_strong is not None:
                        gains_strong.append(qP - q_strong)
                        if qP > q_strong:
                            wins_strong += 1
                ci_bs = _bootstrap_ci(gains_bstar) if gains_bstar else None
                ci_st = _bootstrap_ci(gains_strong) if gains_strong else None
                entry[P] = {
                    "mean_gain_vs_Bstar_dB": ci_bs["mean"] if ci_bs else None,
                    "ci_lower_vs_Bstar_dB": ci_bs["ci_lo"] if ci_bs else None,
                    "paired_wins_vs_Bstar": wins_bstar,
                    "n_paired_Bstar": len(gains_bstar),
                    "mean_gain_vs_strongest_standalone_dB": ci_st["mean"] if ci_st else None,
                    "ci_lower_vs_strongest_standalone_dB": ci_st["ci_lo"] if ci_st else None,
                    "paired_wins_vs_strongest_standalone": wins_strong,
                    "n_paired_strongest": len(gains_strong),
                }
            primary[f"{cond_name}|snr{snr_db}"] = entry

    # clean_control degradation check (P vs B* must not degrade > 0.1 dB)
    clean_cells = [k for k in primary if k.startswith("clean_control")]
    # method verdict
    go_candidates = []
    for cell_key, entry in primary.items():
        for P in ("P1", "P2", "P3"):
            e = entry[P]
            if (e["mean_gain_vs_Bstar_dB"] is not None
                    and e["mean_gain_vs_Bstar_dB"] >= 0.3
                    and e["ci_lower_vs_Bstar_dB"] is not None
                    and e["ci_lower_vs_Bstar_dB"] > 0.0
                    and e["paired_wins_vs_Bstar"] >= 7
                    and e["mean_gain_vs_strongest_standalone_dB"] is not None
                    and e["mean_gain_vs_strongest_standalone_dB"] >= 0.3
                    and e["ci_lower_vs_strongest_standalone_dB"] is not None
                    and e["ci_lower_vs_strongest_standalone_dB"] > 0.0
                    and e["paired_wins_vs_strongest_standalone"] >= 7):
                go_candidates.append((cell_key, P))
    # clean_control degradation
    clean_degradation_ok = True
    for cell_key in clean_cells:
        entry = primary[cell_key]
        for P in ("P1", "P2", "P3"):
            e = entry[P]
            if e["mean_gain_vs_Bstar_dB"] is not None and e["mean_gain_vs_Bstar_dB"] < -0.1:
                clean_degradation_ok = False

    if go_candidates and clean_degradation_ok:
        verdict = "GO_METHOD"
    elif any(any(entry[P]["mean_gain_vs_Bstar_dB"] is not None
                 and entry[P]["mean_gain_vs_Bstar_dB"] >= 0.3 for P in ("P1", "P2", "P3"))
             for entry in primary.values()):
        verdict = "COMPONENT_REPRO_ONLY"
    else:
        verdict = "PROBLEM_SURVIVES_METHODS_FAIL"

    return {
        "verdict": verdict,
        "primary_method": primary,
        "go_candidates": go_candidates,
        "clean_degradation_ok": clean_degradation_ok,
        "rows_all": rows_val,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    _assert_closure()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    shas = source_shas()
    csha = contract_sha()
    osha = closure_sha()

    t0 = time.time()
    # Phase B: semantic gates (abort on failure)
    gates_ok, gates_res = phase_b_gates()
    with open(RESULT_DIR / "phase_b_gates.json", "w") as f:
        json.dump({"overall_pass": gates_ok, "gates": gates_res}, f, indent=1, default=str)
    if not gates_ok:
        result = {
            "label": "T006 high-order CPR combination (ABORTED at semantic gates)",
            "experiment": "HIGH_ORDER_CPR_COMBINATION_METHOD_PACKAGE",
            "contract_sha256": csha, "source_closure_sha256": osha,
            "source_sha256": shas,
            "verdict": {"verdict": "BLOCKED_SEMANTIC_GATE_FAILED",
                        "reason": "one or more semantic gates failed; no primary run"},
            "elapsed_s": time.time() - t0,
        }
        with open(RESULT_DIR / "result.json", "w") as f:
            json.dump(result, f, indent=1, default=str)
        print(json.dumps({"verdict": result["verdict"]["verdict"]}, indent=1))
        return result

    # Phase C: B* selection on VALIDATION
    bstar_arm, bstar_cfg, bstar_means = phase_c_bstar_selection()
    with open(RESULT_DIR / "phase_c_bstar.json", "w") as f:
        json.dump({"bstar_arm": bstar_arm, "bstar_cfg": bstar_cfg,
                   "mean_ber_by_cfg": {str(k): v for k, v in bstar_means.items()}},
                  f, indent=1, default=str)

    # Phase D: headroom gate
    headroom = phase_d_headroom(bstar_arm, bstar_cfg)
    with open(RESULT_DIR / "phase_d_headroom.json", "w") as f:
        json.dump(headroom, f, indent=1, default=str)
    print(f"[phaseD] verdict={headroom['verdict']} "
          f"max_point={headroom['max_point_dB']:.4f} dB "
          f"max_ci_upper={headroom['max_ci_upper_dB']:.4f} dB")

    method_result = None
    final_verdict_name = headroom["verdict"]
    if headroom["verdict"] == "HEADROOM_SURVIVES":
        # Phase E: method gate
        method_result = phase_e_methods(bstar_arm, bstar_cfg)
        with open(RESULT_DIR / "phase_e_methods.json", "w") as f:
            json.dump(method_result, f, indent=1, default=str)
        final_verdict_name = method_result["verdict"]
        print(f"[phaseE] verdict={method_result['verdict']} "
              f"go_candidates={method_result['go_candidates']}")
    else:
        print("[phaseE] SKIPPED (headroom gate did not survive)")

    result = {
        "label": "T006 high-order CPR combination consolidated",
        "experiment": "HIGH_ORDER_CPR_COMBINATION_METHOD_PACKAGE",
        "contract_sha256": csha,
        "source_closure_sha256": osha,
        "source_sha256": shas,
        "params": {**COMMON, "conditions": CONDITIONS, "snr_grid_db": SNR_GRID_DB,
                   "val_seeds": VAL_SEEDS, "test_seeds": TEST_SEEDS,
                   "bstar_arm": bstar_arm, "bstar_cfg": bstar_cfg,
                   "p_defaults": P_DEFAULTS},
        "phase_b_gates_pass": gates_ok,
        "phase_c_bstar": {"arm": bstar_arm, "cfg": bstar_cfg},
        "phase_d_headroom_verdict": headroom["verdict"],
        "phase_d_headroom_summary": {
            "max_point_dB": headroom["max_point_dB"],
            "max_ci_upper_dB": headroom["max_ci_upper_dB"],
            "survivors": headroom["survivors"],
        },
        "phase_e_method_verdict": method_result["verdict"] if method_result else None,
        "final_verdict": final_verdict_name,
        "ber_to_q2_formula": "Q=sqrt(2)*erfcinv(2*BER); Q^2_dB=20*log10(Q); BER=0 -> 0.5/N_eval bound; BER>=0.5 -> None",
        "bootstrap": "per-cell paired (Q2_O - Q2_B*) or (Q2_P - Q2_opp) across 10 test seeds; 2000 resamples; 95% CI = [2.5%, 97.5%]",
        "elapsed_s": time.time() - t0,
    }
    with open(RESULT_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=1, default=str)
    print(f"\n[final] verdict={final_verdict_name}")
    return result


if __name__ == "__main__":
    main()
