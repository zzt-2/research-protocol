"""Runner for the Pilot-Jones complex-model SEMANTIC REPAIR (T004).

Pipeline per (model, cell, seed):
  1. generate ONE canonical realization via generate_shared_realization_dp.
  2. build the REPAIRED impaired realization (component op on CLEAN signal +
     SAME n_post; defect #1 fix).
  3. inject pre-channel pilots (pilots traverse the SAME component op; defect #3).
  4. estimate per-block pilot-LS Jones ONCE (shared); per-arm estimates as needed.
  5. for every arm: build the arm's RX view, optional blind CMA, evaluate BER on
     the SHARED data mask. Oracle reads the FULL-channel truth (defect #5 fix).

Paired fairness: every arm consumes the same impaired realization, pilot
injection, estimates, data mask, eval window, CMA config.

This runner is self-contained and does NOT import T003 salvage code (which is
immutable failure evidence). It reuses the verified dual-QPSK BER/Q^2 metrics
(copied) so the metric signature is preserved.
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
import semantic_channel as sc  # noqa: E402
import pilot_and_baselines as pb  # noqa: E402
import repair_methods as rm  # noqa: E402


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
        "semantic_channel": "projects/simulation/explore/pilot-jones-complex-repair/semantic_channel.py",
        "pilot_and_baselines": "projects/simulation/explore/pilot-jones-complex-repair/pilot_and_baselines.py",
        "repair_methods": "projects/simulation/explore/pilot-jones-complex-repair/repair_methods.py",
        "runner": "projects/simulation/explore/pilot-jones-complex-repair/run_repair.py",
    }
    return {k: _sha_file(os.path.join(root, rel)) for k, rel in files.items()
            if os.path.exists(os.path.join(root, rel))}


def realization_fingerprint(realization_imp):
    d = hashlib.sha256()
    for key in ("rX", "rY", "sX", "sY", "h", "theta"):
        d.update(np.asarray(realization_imp[key]).tobytes())
    d.update(np.asarray(realization_imp["jones_truth"]).tobytes())
    d.update(np.asarray(realization_imp["n_post"]).tobytes())
    return d.hexdigest()


# ---- verified dual-QPSK BER metric (copied from T002/T003) ----

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


def ber_to_q2_db(ber):
    """Q = sqrt(2)*erfcinv(2*BER); Q^2_dB = 20*log10(Q). BER>=0.5 -> None.
    BER<=0 -> caller must pass denominator for the 0.5/N_eval bound."""
    from math import log10
    from scipy.special import erfcinv
    if ber is None or ber >= 0.5 or ber <= 0.0:
        return None
    q = (2.0 ** 0.5) * erfcinv(2.0 * ber)
    if q <= 0:
        return None
    return 20.0 * log10(q)


# ---- standard blind CMA (secondary; nocma metric isolates derotation quality) ----

def run_standard_cma(rX, rY, *, mu, taps, r2, block_size, eval_start, eval_end):
    from numpy.lib.stride_tricks import sliding_window_view
    rX = np.asarray(rX); rY = np.asarray(rY)
    x_win = sliding_window_view(rX, taps); y_win = sliding_window_view(rY, taps)
    half = taps // 2
    weights = {n: np.zeros(taps, dtype=complex) for n in ("wxx", "wxy", "wyx", "wyy")}
    weights["wxx"][half] = weights["wyy"][half] = 1.0
    def _norm(w):
        return float(np.sqrt(sum(np.sum(np.abs(v) ** 2) for v in w.values())))
    initial_norm = _norm(weights)
    n_blocks = max(0, (len(rX) - taps + 1) // block_size)
    out_x = np.zeros(eval_end - eval_start, dtype=complex)
    out_y = np.zeros_like(out_x)
    valid = np.zeros(len(out_x), dtype=bool)
    diverged = False; div_sym = None
    for block in range(n_blocks):
        s = block * block_size; e = s + block_size; os = s + half
        x, y = x_win[s:e], y_win[s:e]
        z_x = x @ weights["wxx"] + y @ weights["wxy"]
        z_y = x @ weights["wyx"] + y @ weights["wyy"]
        left, right = max(os, eval_start), min(os + block_size, eval_end)
        if left < right:
            src = slice(left - os, right - os); dst = slice(left - eval_start, right - eval_start)
            out_x[dst], out_y[dst] = z_x[src], z_y[src]; valid[dst] = True
        ex = r2 - np.abs(z_x) ** 2; ey = r2 - np.abs(z_y) ** 2
        weights["wxx"] += mu * np.mean((ex * z_x)[:, None] * np.conj(x), axis=0)
        weights["wxy"] += mu * np.mean((ex * z_x)[:, None] * np.conj(y), axis=0)
        weights["wyx"] += mu * np.mean((ey * z_y)[:, None] * np.conj(x), axis=0)
        weights["wyy"] += mu * np.mean((ey * z_y)[:, None] * np.conj(y), axis=0)
        nrm = _norm(weights)
        if (not np.isfinite(nrm)) or nrm > 10 * initial_norm:
            diverged = True; div_sym = int(os + block_size); break
    return {"zX": out_x, "zY": out_y, "valid_mask": valid,
            "diverged": diverged, "divergence_symbol": div_sym}


# ---------------------------------------------------------------------------
# Make one repaired impaired realization
# ---------------------------------------------------------------------------

def make_realization_imp(seed, *, model_id, alpha, beta, f_g, sop_rate,
                         gamma_bar, block_size, N, pdl_db, dgd_ps, t_s, method):
    real = generate_shared_realization_dp(
        N=N, alpha=alpha, beta=beta, f_g=f_g, sop_rate=sop_rate, seed=seed,
        gamma_bar=gamma_bar, block=block_size, t_s=t_s, method=method)
    rng = np.random.default_rng(int(1e6 + seed * 31 + hash(model_id) % 997))
    return sc.build_impaired_realization(
        real, model_id=model_id, block_size=block_size, rng=rng,
        pdl_db=pdl_db, dgd_ps=dgd_ps, t_s=t_s)


# ---------------------------------------------------------------------------
# Arm execution
# ---------------------------------------------------------------------------

def run_arms(realization_imp, *, block_size, n_pilots, taps, mu, r2,
             eval_start, eval_end, gamma_bar, arms, n_taps_b3=3,
             b2_lambda=1e-2):
    cfg_realization = realization_imp  # canonical carried via dict
    pilot = pb.inject_pre_channel_pilots(
        {"sX": realization_imp["sX"], "sY": realization_imp["sY"],
         "theta": realization_imp["theta"], "h": realization_imp["h"]},
        realization_imp, block_size=block_size, n_pilots=n_pilots)
    estimates_single = pb.estimate_jones_single_tap(pilot, block_size=block_size)
    estimates_tapped = pb.estimate_jones_tapped(pilot, block_size=block_size,
                                                n_taps=n_taps_b3)
    estimates_p1 = rm.estimate_jones_weighted(pilot, block_size=block_size)
    dm = pilot["data_mask"]

    def _eval(view):
        # eval_mask = data AND not guard-transient (T004 §3.3). The guard excludes
        # the PMD FIR circular wrap-around at block boundaries so the metric
        # denominator is theory-justified and identical (paired) across arms.
        dmask = (pilot["eval_mask"])[eval_start:eval_end]
        n_eval = int(dmask.sum())
        if n_eval > 0:
            met_nocma = evaluate_dual_qpsk(
                realization_imp["sX"][eval_start:eval_end][dmask],
                realization_imp["sY"][eval_start:eval_end][dmask],
                view["rX"][eval_start:eval_end][dmask],
                view["rY"][eval_start:eval_end][dmask])
        else:
            met_nocma = {"fixed_label_ber": None, "pi_ber": None,
                         "assignment": None, "phase_x": None, "phase_y": None}
        res = run_standard_cma(view["rX"], view["rY"], mu=mu, taps=taps,
                               r2=r2, block_size=block_size,
                               eval_start=eval_start, eval_end=eval_end)
        mask = res["valid_mask"] & dmask
        n_cma = int(mask.sum())
        if n_cma > 0:
            met = evaluate_dual_qpsk(
                realization_imp["sX"][eval_start:eval_end][mask],
                realization_imp["sY"][eval_start:eval_end][mask],
                res["zX"][mask], res["zY"][mask])
        else:
            met = {"fixed_label_ber": None, "pi_ber": None,
                   "assignment": None, "phase_x": None, "phase_y": None}
        return {"metrics": met, "metrics_nocma": met_nocma,
                "valid_data_samples": n_cma,
                "valid_data_samples_nocma": n_eval,
                "diverged": res["diverged"],
                "divergence_symbol": res["divergence_symbol"]}

    arms_out = {}
    for name in arms:
        if name == "B0":
            view = rm.build_arm_view(realization_imp, pilot); arms_out[name] = _eval(view)
        elif name == "B1":
            der = pb.derotate_single_tap(pilot, estimates_single, block_size=block_size,
                                         mode="ema", ema_alpha=0.9)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B2":
            der = pb.derotate_single_tap(pilot, estimates_single, block_size=block_size,
                                         mode="tikhonov", tikhonov=b2_lambda)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B3_pdl":
            der = pb.derotate_single_tap(pilot, estimates_single, block_size=block_size,
                                         mode="whitening", whitening_kappa=1e3)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B3_pmd":
            der = pb.derotate_tapped(pilot, estimates_tapped, block_size=block_size)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B3_pmd_pool":
            est_pool = pb.estimate_jones_tapped_pooled(pilot, block_size=block_size,
                                                       n_taps=n_taps_b3)
            if est_pool is None:
                view = rm.build_arm_view(realization_imp, pilot); arms_out[name] = _eval(view)
            else:
                der = pb.derotate_tapped(pilot, est_pool, block_size=block_size)
                view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "B4_fde":
            der = pb.derotate_fde(pilot, estimates_single, block_size=block_size,
                                  gamma_bar=gamma_bar)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P1_energy":
            der = rm.derotate_weighted(pilot, estimates_p1, block_size=block_size)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P1_energy_whiten":
            der = rm.derotate_weighted(pilot, estimates_p1, block_size=block_size,
                                       use_whitening=True)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P2_cond_ema":
            der = rm.derotate_cond_adaptive_ema(pilot, estimates_single,
                                                block_size=block_size)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "P3_joint":
            der = rm.derotate_p3_joint(pilot, block_size=block_size, n_taps=n_taps_b3)
            if der is None:
                view = rm.build_arm_view(realization_imp, pilot); arms_out[name] = _eval(view)
            else:
                view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
        elif name == "O":
            der = rm.oracle_full_inverse(realization_imp, block_size=block_size,
                                         gamma_bar=gamma_bar, data_mask=dm)
            view = rm.build_arm_view(realization_imp, der); arms_out[name] = _eval(view)
            arms_out[name]["info_class"] = "oracle_full_channel"
        else:
            raise ValueError(name)
        arms_out[name].setdefault(
            "info_class", "oracle_full_channel" if name == "O" else "receiver_visible")
    conds = [e["cond"] for e in estimates_single if e.get("cond") is not None]
    diag = {"n_blocks": len(estimates_single),
            "cond_mean": float(np.mean(conds)) if conds else None,
            "cond_p95": float(np.quantile(conds, 0.95)) if conds else None,
            "cond_max": float(np.max(conds)) if conds else None}
    return {"pilot_overhead": pilot["overhead"],
            "shared_realization_fingerprint": realization_fingerprint(realization_imp),
            "estimate_diagnostics": diag, "arms": arms_out}


def run_grid(cells, arms, *, alpha, beta, gamma_bar, n_pilots, block_size, N,
             taps, mu, r2, warmup_frac, out_path, contract_sha, source_shas_map,
             label, n_taps_b3=3, b2_lambda=1e-2):
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
                           n_taps_b3=n_taps_b3, b2_lambda=b2_lambda)
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
    blob = {"label": label, "experiment": "T004 semantic repair",
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
