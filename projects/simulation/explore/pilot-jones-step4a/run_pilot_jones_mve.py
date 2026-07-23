"""Runner for the Pilot-Jones GW Step 4a big-package MVE.

Pipeline per (cell, seed):
  1. generate ONE shared realization via the canonical generator (current branch).
  2. inject pilots ONCE (shared pilot RX + shared data mask for all arms).
  3. estimate per-block pilot-LS Jones ONCE (shared estimates for all arms).
  4. for every arm in the baseline ladder (+ oracle): build the arm's RX view,
     run standard blind CMA on that view, evaluate BER on the SHARED data mask.
Paired fairness: every arm consumes the same realization, pilot injection,
pilot-LS estimates, data mask, eval window, CMA config. Oracle reads true theta
(tagged, upper bound only).

This runner is intentionally minimal and single-threaded; grid runs are split
by the caller (smoke -> validation -> frozen -> test).
"""
from __future__ import annotations
import hashlib
import inspect
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]                      # projects/simulation
sys.path.insert(0, str(SIM))

from params import SimulationConfig                          # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
from metrics import evaluate_dual_qpsk                       # noqa: E402
import pilot_jones_methods as m                              # noqa: E402


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_shas():
    files = {
        "generator": "projects/simulation/common/_dual_pol_channel.py",
        "gg_time": "projects/simulation/common/_gg_time.py",
        "params": "projects/simulation/params.py",
        "metrics": str((HERE / "metrics.py").relative_to(SIM.parent.parent)),
        "methods": str((HERE / "pilot_jones_methods.py").relative_to(SIM.parent.parent)),
        "runner": str((HERE / "run_pilot_jones_mve.py").relative_to(SIM.parent.parent)),
    }
    root = SIM.parent.parent  # repo root in this worktree
    return {k: _sha_file(os.path.join(root, rel)) for k, rel in files.items()
            if os.path.exists(os.path.join(root, rel))}


def realization_fingerprint(realization):
    d = hashlib.sha256()
    for key in ("rX", "rY", "sX", "sY", "h", "theta"):
        d.update(np.asarray(realization[key]).tobytes())
    return d.hexdigest()


def run_cell(cell, seed, *, alpha, beta, f_g, sop_rate, gamma_bar,
             n_pilots, block_size, N, taps, mu, r2,
             eval_start, eval_end, arms, include_oracle):
    cfg = SimulationConfig()
    realization = generate_shared_realization_dp(
        N=N, alpha=alpha, beta=beta, f_g=f_g, sop_rate=sop_rate, seed=seed,
        gamma_bar=gamma_bar, block=block_size, t_s=cfg.system.T_S,
        method=cfg.gg_time.AR1_METHOD,
    )
    pilot = m.inject_dual_pilots(realization, block_size=block_size, n_pilots=n_pilots)
    estimates = m.estimate_jones_blocks(pilot, block_size=block_size)
    dm = pilot["data_mask"]

    arms_out = {}
    for name in arms:
        kind, kw = m.ARMS[name]
        if kind == "none":
            view = m.build_arm_view(realization, pilot)
        elif kind == "derotate":
            der = m.derotate(pilot, estimates, block_size=block_size, **kw)
            view = m.build_arm_view(realization, der)
        elif kind == "tracker":
            der = m.derotate_uncertainty_tracker(pilot, estimates, block_size=block_size, **kw)
            view = m.build_arm_view(realization, der)
        elif kind == "oracle":
            if not include_oracle:
                continue
            der = m.derotate_oracle(pilot, realization, block_size=block_size)
            view = m.build_arm_view(realization, der)
        else:
            raise ValueError(kind)
        res = m.run_standard_cma(
            view["rX"], view["rY"], mu=mu, taps=taps, r2=r2,
            block_size=block_size, eval_start=eval_start, eval_end=eval_end)
        mask = res["valid_mask"] & dm[eval_start:eval_end]
        n_eval = int(mask.sum())
        if n_eval > 0:
            metrics = evaluate_dual_qpsk(
                realization["sX"][eval_start:eval_end][mask],
                realization["sY"][eval_start:eval_end][mask],
                res["zX"][mask], res["zY"][mask])
        else:
            metrics = {"fixed_label_ber": None, "pi_ber": None,
                       "assignment": None, "phase_x": None, "phase_y": None}
        arms_out[name] = {
            "metrics": metrics, "valid_data_samples": n_eval,
            "diverged": res["diverged"],
            "divergence_symbol": res["divergence_symbol"],
            "info_class": "oracle_true_theta" if kind == "oracle" else "receiver_visible",
        }

    # receiver-visible diagnostics on the pilot-LS estimate (no truth used)
    conds = [e["cond"] for e in estimates]
    diag = {
        "n_blocks": len(estimates),
        "cond_mean": float(np.mean(conds)) if conds else None,
        "cond_p95": float(np.quantile(conds, 0.95)) if conds else None,
        "cond_max": float(np.max(conds)) if conds else None,
    }
    return {
        "cell": cell, "seed": int(seed),
        "alpha": float(alpha), "beta": float(beta), "f_g": float(f_g),
        "sop_rate": float(sop_rate), "gamma_bar": float(gamma_bar),
        "n_pilots": int(n_pilots), "block_size": int(block_size),
        "N": int(N), "taps": int(taps), "mu": float(mu), "r2": float(r2),
        "eval_start": int(eval_start), "eval_end": int(eval_end),
        "pilot_overhead": pilot["overhead"],
        "shared_realization_fingerprint": realization_fingerprint(realization),
        "estimate_diagnostics": diag,
        "arms": arms_out,
    }


def run_grid(cells, arms, include_oracle, *, alpha, beta, gamma_bar,
             n_pilots, block_size, N, taps, mu, r2, warmup_frac, out_path,
             contract_sha, source_shas_map, label):
    eval_start = int(N * warmup_frac)
    eval_end = N
    rows = []
    for cell in cells:
        for seed in cell["seeds"]:
            row = run_cell(
                cell["cell"], seed, alpha=alpha, beta=beta,
                f_g=cell["f_g"], sop_rate=cell["sop_rate"], gamma_bar=gamma_bar,
                n_pilots=n_pilots, block_size=block_size, N=N, taps=taps,
                mu=mu, r2=r2, eval_start=eval_start, eval_end=eval_end,
                arms=arms, include_oracle=include_oracle)
            rows.append(row)
    blob = {
        "label": label,
        "experiment": "Pilot-Jones Step 4a big-package MVE",
        "contract_sha256": contract_sha,
        "source_sha256": source_shas_map,
        "params": {"alpha": alpha, "beta": beta, "gamma_bar": gamma_bar,
                   "n_pilots": n_pilots, "block_size": block_size, "N": N,
                   "taps": taps, "mu": mu, "r2": r2, "warmup_frac": warmup_frac},
        "cells": [{"cell": c["cell"], "f_g": c["f_g"], "sop_rate": c["sop_rate"],
                   "seeds": list(c["seeds"])} for c in cells],
        "raw_rows": rows,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(blob, f, indent=1)
    return blob


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["smoke", "validation", "test"], required=True)
    p.add_argument("--contract-sha", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--seeds", default="2000,2001,2002")
    args = p.parse_args()

    shas = source_shas()
    base_arms = ["B0_blockLS_pinv", "B1_fixedEMA09", "B2a_tikhonov",
                 "B2b_condition_guard", "P_uncertainty_tracker"]
    if args.mode == "smoke":
        cells = [{"cell": "smoke_clean", "f_g": 100.0, "sop_rate": 4e-6,
                  "seeds": [int(s) for s in args.seeds.split(",")]}]
        arms = base_arms + ["O_true_theta_oracle"]
        out = run_grid(cells, arms, include_oracle=True, alpha=4.2, beta=1.4,
                       gamma_bar=100.0, n_pilots=6, block_size=64, N=10000,
                       taps=11, mu=1e-3, r2=1.0, warmup_frac=0.1,
                       out_path=args.out, contract_sha=args.contract_sha,
                       source_shas_map=shas, label="smoke")
    elif args.mode == "validation":
        cells = [{"cell": f"val_fg{int(fg)}_rate{int(rate*1e6)}", "f_g": fg,
                  "sop_rate": rate,
                  "seeds": [int(s) for s in args.seeds.split(",")]}
                 for fg in (30.0, 100.0, 1000.0) for rate in (4e-6, 8e-6, 1e-5)]
        arms = base_arms
        out = run_grid(cells, arms, include_oracle=False, alpha=4.2, beta=1.4,
                       gamma_bar=100.0, n_pilots=6, block_size=64, N=100000,
                       taps=11, mu=1e-3, r2=1.0, warmup_frac=0.1,
                       out_path=args.out, contract_sha=args.contract_sha,
                       source_shas_map=shas, label="validation")
    else:  # test
        cells = [{"cell": f"test_fg{int(fg)}_rate{int(rate*1e6)}", "f_g": fg,
                  "sop_rate": rate,
                  "seeds": [int(s) for s in args.seeds.split(",")]}
                 for fg in (30.0, 100.0, 1000.0) for rate in (4e-6, 8e-6, 1e-5)]
        arms = base_arms + ["O_true_theta_oracle"]
        out = run_grid(cells, arms, include_oracle=True, alpha=4.2, beta=1.4,
                       gamma_bar=100.0, n_pilots=6, block_size=64, N=100000,
                       taps=11, mu=1e-3, r2=1.0, warmup_frac=0.1,
                       out_path=args.out, contract_sha=args.contract_sha,
                       source_shas_map=shas, label="test")
    print(json.dumps({"label": out["label"], "rows": len(out["raw_rows"]),
                      "arms": list(out["raw_rows"][0]["arms"].keys())}))
