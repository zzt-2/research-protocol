"""Runner for the Pilot-Jones complex-model salvage MVE (T003).

Pipeline per (model, cell, seed):
  1. generate ONE canonical realization via generate_shared_realization_dp.
  2. apply the complex-Jones/PMD/PDL impairment ONCE -> realization_imp.
  3. inject pilots ONCE (shared pilot RX + data mask for all arms).
  4. estimate per-block pilot-LS Jones ONCE (shared for B0/B1/B2/B3; P1 uses its
     own energy-weighted estimate).
  5. for every arm: build the arm's RX view, run standard blind CMA, evaluate
     BER on the SHARED data mask. Oracle reads true Jones (tagged upper bound).

Paired fairness: every arm consumes the same impaired realization, pilot
injection, estimates, data mask, eval window, CMA config.

Modes:
  theory      : limiting-case tests (M0 control compat, M1 cond==1, M2 cond vs
                PDL, M3 dgd=0 memoryless / dgd>0 memory, noiseless recovery).
  smoke       : tiny deterministic smoke on each model.
  probe       : bounded multi-seed headroom probe (verified + stress ranges).
  mve         : conditional performance MVE on fresh test seeds (only if gate
                passed). Frozen B3/P on validation-selected configs.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(HERE))

from params import SimulationConfig  # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import complex_jones_channel as cjc  # noqa: E402
import conventional_baselines as cb  # noqa: E402
import salvage_methods as sm  # noqa: E402


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_shas():
    root = SIM.parent.parent
    files = {
        "generator": "projects/simulation/common/_dual_pol_channel.py",
        "gg_time": "projects/simulation/common/_gg_time.py",
        "params": "projects/simulation/params.py",
        "channel": "projects/simulation/explore/pilot-jones-complex-salvage/complex_jones_channel.py",
        "baselines": "projects/simulation/explore/pilot-jones-complex-salvage/conventional_baselines.py",
        "methods": "projects/simulation/explore/pilot-jones-complex-salvage/salvage_methods.py",
        "runner": "projects/simulation/explore/pilot-jones-complex-salvage/run_salvage.py",
    }
    return {k: _sha_file(os.path.join(root, rel)) for k, rel in files.items()
            if os.path.exists(os.path.join(root, rel))}


def realization_fingerprint(realization_imp):
    d = hashlib.sha256()
    for key in ("rX", "rY", "sX", "sY", "h", "theta"):
        d.update(np.asarray(realization_imp[key]).tobytes())
    d.update(np.asarray(realization_imp["jones_truth"]).tobytes())
    return d.hexdigest()


# reuse the T002 dual-QPSK BER metric (copied here to keep closure self-contained)
def _ber(tx, rx):
    tx = np.asarray(tx); rx = np.asarray(rx)
    tb = np.stack((np.real(tx) < 0, np.imag(tx) < 0), axis=-1)
    rb = np.stack((np.real(rx) < 0, np.imag(rx) < 0), axis=-1)
    return float(np.mean(tb != rb))


def _phase_ber(tx, rx):
    return min(_ber(tx, rx * np.exp(-1j * p * np.pi / 2)) for p in range(4))


def evaluate_dual_qpsk(tx_x, tx_y, z_x, z_y):
    arr = [np.asarray(a) for a in (tx_x, tx_y, z_x, z_y)]
    fixed = (_phase_ber(arr[0], arr[2]) + _phase_ber(arr[1], arr[3])) / 2
    best = None
    for swapped in (False, True):
        rx0, rx1 = (arr[3], arr[2]) if swapped else (arr[2], arr[3])
        for px in range(4):
            for py in range(4):
                c0 = rx0 * np.exp(-1j * px * np.pi / 2)
                c1 = rx1 * np.exp(-1j * py * np.pi / 2)
                score = (_ber(arr[0], c0) + _ber(arr[1], c1)) / 2
                if best is None or score < best[0]:
                    best = (score, swapped, px, py)
    return {"fixed_label_ber": fixed, "pi_ber": float(best[0]),
            "assignment": ("y", "x") if best[1] else ("x", "y"),
            "phase_x": int(best[2]), "phase_y": int(best[3])}


# ---------------------------------------------------------------------------
# BER -> Q^2_dB conversion (with zero-error handling). QPSK only.
# ---------------------------------------------------------------------------

def ber_to_q2_db(ber):
    """Q = sqrt(2)*erfcinv(2*BER); Q^2_dB = 20*log10(Q).

    BER=0 -> one-sided upper bound from a single-error count convention
    (treat as 0.5 errors on the actual denominator, i.e. BER_ub = 0.5/N_eval).
    BER>=0.5 -> Q invalid (return None)."""
    from math import log10
    from scipy.special import erfcinv
    if ber is None:
        return None
    if ber >= 0.5:
        return None
    if ber <= 0.0:
        return None  # caller must pass denominator for the bound
    q = (2.0 ** 0.5) * erfcinv(2.0 * ber)
    if q <= 0:
        return None
    return 20.0 * log10(q)


# ---------------------------------------------------------------------------
# Arm execution for one impaired realization.
# ---------------------------------------------------------------------------

def run_arms(realization_imp, *, block_size, n_pilots, taps, mu, r2,
             eval_start, eval_end, gamma_bar, arms, n_taps_b3=1):
    pilot = cb.inject_dual_pilots(realization_imp, block_size=block_size,
                                  n_pilots=n_pilots)
    estimates = cb.estimate_jones_blocks(pilot, block_size=block_size, n_taps=1)
    estimates_b3 = cb.estimate_jones_blocks(pilot, block_size=block_size,
                                            n_taps=n_taps_b3) if n_taps_b3 > 1 else estimates
    estimates_p1 = sm.estimate_jones_blocks_weighted(pilot, block_size=block_size)
    dm = pilot["data_mask"]

    def _eval(view):
        res = sm.run_standard_cma(view["rX"], view["rY"], mu=mu, taps=taps,
                                  r2=r2, block_size=block_size,
                                  eval_start=eval_start, eval_end=eval_end)
        mask = res["valid_mask"] & dm[eval_start:eval_end]
        n_eval = int(mask.sum())
        if n_eval > 0:
            met = evaluate_dual_qpsk(
                realization_imp["sX"][eval_start:eval_end][mask],
                realization_imp["sY"][eval_start:eval_end][mask],
                res["zX"][mask], res["zY"][mask])
        else:
            met = {"fixed_label_ber": None, "pi_ber": None,
                   "assignment": None, "phase_x": None, "phase_y": None}
        # NOCMA metric: hard-decision BER directly on the derotated RX (no CMA).
        # This isolates the derotation (Jones-estimate) quality, which is what the
        # Pilot-Jones salvage is actually about. CMA is an active component that can
        # both help (deployable arms, residual) and hurt (oracle on near-clean
        # signals), so the nocma metric is the cleaner derotation-quality score.
        dmask = dm[eval_start:eval_end]
        if int(dmask.sum()) > 0:
            met_nocma = evaluate_dual_qpsk(
                realization_imp["sX"][eval_start:eval_end][dmask],
                realization_imp["sY"][eval_start:eval_end][dmask],
                view["rX"][eval_start:eval_end][dmask],
                view["rY"][eval_start:eval_end][dmask])
        else:
            met_nocma = {"fixed_label_ber": None, "pi_ber": None,
                         "assignment": None, "phase_x": None, "phase_y": None}
        return {"metrics": met, "metrics_nocma": met_nocma,
                "valid_data_samples": n_eval,
                "valid_data_samples_nocma": int(dmask.sum()),
                "diverged": res["diverged"],
                "divergence_symbol": res["divergence_symbol"]}

    arms_out = {}
    for name in arms:
        if name == "B0_pinv":
            der = cb.derotate(pilot, estimates, block_size=block_size, mode="pinv")
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B1_ema09":
            der = cb.derotate(pilot, estimates, block_size=block_size, mode="ema", ema_alpha=0.9)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B2_tikhonov":
            der = cb.derotate(pilot, estimates, block_size=block_size, mode="tikhonov", tikhonov=1e-2)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B3_whitening":
            der = cb.derotate(pilot, estimates, block_size=block_size, mode="whitening", whitening_kappa=1e3)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B3_tapped":
            der = cb.derotate(pilot, estimates_b3, block_size=block_size, mode="tapped", n_taps=n_taps_b3)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P1_energy_weighted":
            der = sm.derotate_weighted(pilot, estimates_p1, block_size=block_size)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P1_energy_whiten":
            der = sm.derotate_weighted(pilot, estimates_p1, block_size=block_size, use_whitening=True)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P1_energy_ema":
            der = sm.derotate_weighted(pilot, estimates_p1, block_size=block_size, ema_alpha=0.9)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "O_jones_oracle":
            der = cb.derotate_oracle(pilot, realization_imp, block_size=block_size)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
            arms_out[name]["info_class"] = "oracle_true_jones"
        elif name == "O_fde_oracle":
            # FDE oracle needs data mask in realization_imp
            ri = dict(realization_imp); ri["data_mask"] = dm
            der = sm.oracle_fde(ri, block_size=block_size, gamma_bar=gamma_bar)
            view = sm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
            arms_out[name]["info_class"] = "oracle_fde_true_jones_pmd"
        else:
            raise ValueError(name)
        arms_out[name].setdefault("info_class",
                                  "oracle_true_jones" if name.startswith("O_") else "receiver_visible")
    conds = [e["cond"] for e in estimates if e.get("cond") is not None]
    diag = {"n_blocks": len(estimates),
            "cond_mean": float(np.mean(conds)) if conds else None,
            "cond_p95": float(np.quantile(conds, 0.95)) if conds else None,
            "cond_max": float(np.max(conds)) if conds else None}
    return {"pilot_overhead": pilot["overhead"],
            "shared_realization_fingerprint": realization_fingerprint(realization_imp),
            "estimate_diagnostics": diag, "arms": arms_out}


def make_realization_imp(seed, *, model_id, alpha, beta, f_g, sop_rate, gamma_bar,
                         block_size, N, pdl_db, dgd_ps, t_s, method):
    cfg = SimulationConfig()
    real = generate_shared_realization_dp(
        N=N, alpha=alpha, beta=beta, f_g=f_g, sop_rate=sop_rate, seed=seed,
        gamma_bar=gamma_bar, block=block_size, t_s=t_s, method=method)
    rng = np.random.default_rng(int(1e6 + seed * 31 + hash(model_id) % 997))
    return cjc.apply_complex_jones(
        real, model_id=model_id, block_size=block_size, rng=rng,
        pdl_db=pdl_db, dgd_ps=dgd_ps, t_s=t_s,
        unitary_complex=(model_id == "M1"))


# ---------------------------------------------------------------------------
# THEORY mode: limiting-case tests (T003 Phase 2 必做理论/语义测试)
# ---------------------------------------------------------------------------

def run_theory(out_path, *, contract_sha, source_shas_map):
    cfg = SimulationConfig()
    results = {}

    # T1: M0 control byte-compatible with canonical (no Jones change)
    real = generate_shared_realization_dp(N=1000, alpha=4.2, beta=1.4, f_g=100.0,
                                          sop_rate=8e-6, seed=4001, gamma_bar=100.0,
                                          block=64, t_s=cfg.system.T_S, method=cfg.gg_time.AR1_METHOD)
    rng = np.random.default_rng(11)
    m0 = cjc.apply_complex_jones(real, model_id="M0", block_size=64, rng=rng)
    results["T1_M0_control_compat"] = {
        "max_abs_diff_rX": float(np.max(np.abs(m0["rX"] - real["rX"]))),
        "max_abs_diff_rY": float(np.max(np.abs(m0["rY"] - real["rY"]))),
        "pass": bool(np.allclose(m0["rX"], real["rX"]) and np.allclose(m0["rY"], real["rY"]))}

    # T2: M1 complex-unitary H^H H = I, cond == 1
    rng = np.random.default_rng(12)
    m1 = cjc.apply_complex_jones(real, model_id="M1", block_size=64, rng=rng, unitary_complex=True)
    J = np.asarray(m1["jones_truth"])
    unitary_err = float(np.max([np.linalg.norm(J[b] @ J[b].conj().T - np.eye(2)) for b in range(J.shape[0])]))
    cond_max = float(np.max([np.linalg.cond(J[b]) for b in range(J.shape[0])]))
    results["T2_M1_complex_unitary"] = {
        "max_unitary_error": unitary_err, "cond_max": cond_max,
        "pass": bool(unitary_err < 1e-10 and cond_max < 1.0 + 1e-9)}

    # T3: M2 cond matches PDL dB mapping
    for pdl_db, expect_cond in [(3.5, 1.496), (6.0, 1.995), (9.5, 2.985)]:
        rng = np.random.default_rng(13)
        m2 = cjc.apply_complex_jones(real, model_id="M2", block_size=64, rng=rng, pdl_db=pdl_db)
        J2 = np.asarray(m2["jones_truth"])
        cond_mean = float(np.mean([np.linalg.cond(J2[b]) for b in range(J2.shape[0])]))
        results[f"T3_M2_cond_vs_pdl_{pdl_db}dB"] = {
            "pdl_db": pdl_db, "cond_mean": cond_mean,
            "expected_cond": 10 ** (pdl_db / 20.0),
            "pass": bool(abs(cond_mean - 10 ** (pdl_db / 20.0)) < 0.05)}

    # T4: M3 dgd=0 -> memoryless (no change vs identity Jones); dgd>0 -> memory
    rng = np.random.default_rng(14)
    m3z = cjc.apply_complex_jones(real, model_id="M3", block_size=64, rng=rng, dgd_ps=0.0, t_s=cfg.system.T_S)
    results["T4a_M3_dgd0_memoryless"] = {
        "max_abs_diff_rX": float(np.max(np.abs(m3z["rX"] - real["rX"]))),
        "pass": bool(np.allclose(m3z["rX"], real["rX"]))}
    # memory test: dgd=80ps -> output should differ from memoryless identity
    rng = np.random.default_rng(14)
    m3p = cjc.apply_complex_jones(real, model_id="M3", block_size=64, rng=rng, dgd_ps=80.0, t_s=cfg.system.T_S)
    results["T4b_M3_dgd80ps_has_memory"] = {
        "max_abs_diff_rX": float(np.max(np.abs(m3p["rX"] - real["rX"]))),
        "pass": bool(np.max(np.abs(m3p["rX"] - real["rX"])) > 1e-6)}

    # T5: noiseless true-model oracle recovery (M2): apply J then exact inverse -> sX
    rng = np.random.default_rng(15)
    # build a noiseless impaired signal: take canonical signal (no noise) and apply M2
    c = np.cos(real["theta"]); s = np.sin(real["theta"]); h = np.asarray(real["h"])
    sigX = np.sqrt(h) * (c * real["sX"] + s * real["sY"])
    sigY = np.sqrt(h) * (-s * real["sX"] + c * real["sY"])
    real_n0 = dict(real); real_n0["rX"] = sigX; real_n0["rY"] = sigY
    m2n = cjc.apply_complex_jones(real_n0, model_id="M2", block_size=64, rng=rng, pdl_db=6.0)
    J2 = np.asarray(m2n["jones_truth"])
    recX = np.zeros_like(sigX); recY = np.zeros_like(sigY)
    for b in range(J2.shape[0]):
        st = b * 64; en = min(st + 64, len(sigX))
        inv = np.linalg.inv(J2[b])
        rec = inv @ np.stack((m2n["rX"][st:en], m2n["rY"][st:en]), axis=0)
        recX[st:en] = rec[0]; recY[st:en] = rec[1]
    results["T5_M2_noiseless_recovery"] = {
        "max_abs_recovery_error": float(np.max(np.abs(recX - sigX) + np.abs(recY - sigY))),
        "pass": bool(np.allclose(recX, sigX, atol=1e-9) and np.allclose(recY, sigY, atol=1e-9))}

    blob = {"label": "theory", "experiment": "T003 model-ladder limiting-case tests",
            "contract_sha256": contract_sha, "source_sha256": source_shas_map,
            "results": results}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(blob, f, indent=1)
    return blob


# ---------------------------------------------------------------------------
# PROBE / MVE mode
# ---------------------------------------------------------------------------

def run_grid(cells, arms, *, alpha, beta, gamma_bar, n_pilots, block_size, N,
             taps, mu, r2, warmup_frac, out_path, contract_sha, source_shas_map,
             label, n_taps_b3=1):
    cfg = SimulationConfig()
    eval_start = int(N * warmup_frac); eval_end = N
    rows = []
    for cell in cells:
        for seed in cell["seeds"]:
            ri = make_realization_imp(
                seed, model_id=cell["model_id"], alpha=alpha, beta=beta,
                f_g=cell["f_g"], sop_rate=cell["sop_rate"], gamma_bar=gamma_bar,
                block_size=block_size, N=N, pdl_db=cell.get("pdl_db", 0.0),
                dgd_ps=cell.get("dgd_ps", 0.0), t_s=cfg.system.T_S,
                method=cfg.gg_time.AR1_METHOD)
            row = run_arms(ri, block_size=block_size, n_pilots=n_pilots,
                           taps=taps, mu=mu, r2=r2, eval_start=eval_start,
                           eval_end=eval_end, gamma_bar=gamma_bar, arms=arms,
                           n_taps_b3=n_taps_b3)
            row.update({"cell": cell["cell"], "seed": int(seed),
                        "model_id": cell["model_id"],
                        "alpha": float(alpha), "beta": float(beta),
                        "f_g": float(cell["f_g"]),
                        "sop_rate": float(cell["sop_rate"]),
                        "gamma_bar": float(gamma_bar),
                        "pdl_db": float(cell.get("pdl_db", 0.0)),
                        "dgd_ps": float(cell.get("dgd_ps", 0.0)),
                        "verified_range": bool(cell.get("verified_range", False)),
                        "n_pilots": int(n_pilots), "block_size": int(block_size),
                        "N": int(N), "taps": int(taps), "mu": float(mu)})
            rows.append(row)
    blob = {"label": label, "experiment": "T003 complex-model salvage",
            "contract_sha256": contract_sha, "source_sha256": source_shas_map,
            "params": {"alpha": alpha, "beta": beta, "gamma_bar": gamma_bar,
                       "n_pilots": n_pilots, "block_size": block_size, "N": N,
                       "taps": taps, "mu": mu, "r2": r2,
                       "warmup_frac": warmup_frac, "n_taps_b3": n_taps_b3},
            "cells": [{"cell": c["cell"], "model_id": c["model_id"],
                       "f_g": c["f_g"], "sop_rate": c["sop_rate"],
                       "pdl_db": c.get("pdl_db", 0.0),
                       "dgd_ps": c.get("dgd_ps", 0.0),
                       "verified_range": c.get("verified_range", False),
                       "seeds": list(c["seeds"])} for c in cells],
            "raw_rows": rows}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(blob, f, indent=1)
    return blob


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["theory", "smoke", "probe", "mve"], required=True)
    p.add_argument("--contract-sha", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    shas = source_shas()

    if args.mode == "theory":
        out = run_theory(args.out, contract_sha=args.contract_sha, source_shas_map=shas)
        print(json.dumps({"label": out["label"], "n_tests": len(out["results"]),
                          "all_pass": all(r.get("pass") for r in out["results"].values())}))
    else:
        raise SystemExit("smoke/probe/mve are driven by the orchestrator script "
                         "run_all.py which selects cells/seeds per the contract.")
