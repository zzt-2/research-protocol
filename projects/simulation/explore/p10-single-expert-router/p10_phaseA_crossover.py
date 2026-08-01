"""P10 Phase A fresh crossover confirmation (independent executor).

Verdict gate for whether ML/CMA ranking reversal (crossover) reproduces on
fresh dev seeds under the fixed-label BER PRIMARY aperture. Reads ONLY dev
seeds 13000-13005; never touches test seeds 14000-14039.

Two frozen hypothesis cells (from p10_freeze_receipt.json crossover_cells):
  ML_favored_hypothesis   : N=2M, f_G=30,   SNR=20dB, SOP_RATE=1e-7, strong
                            evidence direction (D015 N=2M): small cumulative SOP
                            rotation -> ML fixed-label favored.
  CMA_favored_hypothesis  : N=5M, f_G=1000, SNR=20dB, SOP_RATE=4e-7, strong
                            evidence direction (S020 fg1000 + large SOP): big
                            cumulative SOP rotation / OOD f_G -> CMA fixed-label
                            favored.

Identity (byte-identical with P05):
  channel      = common._gg_time.gg_time_envelope + SOP theta = SOP_RATE*arange
                 + AWGN nv=1/(2*gamma); params.SimulationConfig strong (4.2,1.4).
  ML expert    = common._ml_equalizer.MLChannelEqualizer (n_tap=11, lr=5e-3,
                 batch=1024, n_epochs=15, patience=5), train on first 50% with
                 sX/sY as label, forward full sequence.
  CMA expert   = explore/cma-fade-divergence/prompt019_mu_compress_mve.py
                 StandardCMA2x2 (Godard 1980 with-z, n_tap=11, mu=1e-3, R2=1.0,
                 block=64), equalize entire sequence (no compress).
  fixed-label  = prompt012_longseq_audit.evaluate_outputs(...)
                 ["fixed_label_ber"]["mean"]  (PRIMARY)
  PI-BER       = same evaluate_outputs(...)["permutation_invariant_ber"]["mean"]
                 (secondary, swap-blind invariant 10).
  late slice   = slices(N) late = (nt + int(ntest*0.5), n)  (P05 anchor).

Crossover judgment (frozen, read AFTER results):
  1. ML_favored cell: mean (ML - CMA) fixed < -MDE (0.02), >=4/6 seeds ML<CMA,
     cma_div_frac <= 0.5.
  2. CMA_favored cell: mean (ML - CMA) fixed > +MDE (0.02), >=4/6 seeds CMA<ML,
     cma_div_frac <= 0.5.
  3. direction consistent on BOTH fixed-label (PRIMARY) and PI-BER (secondary).
  -> PASS only if both cells flip in the predicted direction.
  -> FAIL otherwise -> PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE.
"""
from __future__ import annotations
import sys
import json
import time
from pathlib import Path

import numpy as np
import torch

_THIS = Path(__file__).resolve().parent
_SIM = _THIS.parents[1]
_EXPLORE = _SIM / "explore" / "cma-fade-divergence"
for p in (str(_SIM), str(_THIS), str(_EXPLORE)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._ml_equalizer import MLChannelEqualizer
from common._config import BLOCK
from params import SimulationConfig
import ml_long_seq_failure as mlsf
import prompt019_mu_compress_mve as p19
from prompt012_longseq_audit import evaluate_outputs
from common._gg_time import gg_time_envelope

CFG = SimulationConfig()
ALPHA, BETA = CFG.turbulence.as_dict()["strong"]  # (4.2, 1.4)

# ML identity (P05 frozen, n_epochs reduced to 15 for time budget; device CUDA)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
ML_PARAMS = dict(n_tap=11, lr=5e-3, batch_size=1024, n_epochs=15,
                 device=DEVICE, patience=5)
N_TAP = 11
MU = 1e-3
R2 = 1.0

MDE_FIXED_BER = 0.02          # frozen
DEV_SEEDS = list(range(13000, 13006))   # 6 fresh dev trajectories (disjoint)
N_SEEDS_MIN_WINS = 4          # >=4/6 seeds must agree with mean direction
CMA_DIV_FRAC_MAX = 0.5        # co-degradation threshold (cell exclusion)

OUT_PATH = (_SIM / "results" / "p10_single_expert_router"
            / "p10_phaseA_dev_raw.json")
CKPT_PATH = (_SIM / "results" / "p10_single_expert_router"
             / "p10_phaseA_dev_ckpt.json")


# ---------- shared anchors (byte-identical with P05) ----------
def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def train_ml(rx, ry, sx, sy, seed):
    """Frozen-ML training on first 50% prefix (sX/sY as labels); returns model."""
    n = len(rx)
    nt = int(n * 0.5)
    ml = MLChannelEqualizer(**ML_PARAMS)
    set_seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    ml.train(rx[:nt], ry[:nt], sx[:nt], sy[:nt], val_split=0.2, verbose=False)
    return ml.model


def ml_forward(model, rx, ry, device=DEVICE):
    """Feed-forward ML over full sequence; returns zX,zY flattened ndarray."""
    model.eval()
    n = len(rx)
    with torch.no_grad():
        rx_t = torch.from_numpy(rx).to(device)
        ry_t = torch.from_numpy(ry).to(device)
        chunk = torch.cat([rx_t.real.view(1, 1, n).float(),
                           rx_t.imag.view(1, 1, n).float()], dim=1)
        chy = torch.cat([ry_t.real.view(1, 1, n).float(),
                         ry_t.imag.view(1, 1, n).float()], dim=1)
        zX, zY = model(chunk, chy)
    return zX.cpu().numpy().flatten(), zY.cpu().numpy().flatten()


def pi_and_fixed(zx, zy, sx, sy):
    e = evaluate_outputs(zx, zy, sx, sy, diverged=False)
    return (float(e["permutation_invariant_ber"]["mean"]),
            float(e["fixed_label_ber"]["mean"]))


def slices(n):
    """P05 byte-identical: returns (early, mid, late) abs ranges of test half."""
    nt = int(n * 0.5)
    ntest = n - nt
    e = nt + int(ntest * 0.25)
    m = nt + int(ntest * 0.5)
    return (nt, e), (e, m), (m, n)


def gen_channel(N, f_g, sop_rate, snr_db, seed):
    """P05 byte-identical channel generation (one realization, one rng)."""
    set_seed(seed)
    rng = np.random.default_rng(seed)
    gamma = 10 ** (snr_db / 10.0)
    tau_c = CFG.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, ALPHA, BETA, tau_c, block=BLOCK,
                         t_s=mlsf.T_S, method='gar', seed=seed)
    sX, _ = mlsf.gen_qpsk(N, rng)
    sY, _ = mlsf.gen_qpsk(N, rng)
    theta = sop_rate * np.arange(N)
    ct, st = np.cos(theta), np.sin(theta)
    nv = 1.0 / (2 * gamma)
    rX = (np.sqrt(h) * (ct * sX + st * sY)
          + np.sqrt(nv) * (rng.standard_normal(N)
                           + 1j * rng.standard_normal(N)))
    rY = (np.sqrt(h) * (-st * sX + ct * sY)
          + np.sqrt(nv) * (rng.standard_normal(N)
                           + 1j * rng.standard_normal(N)))
    return rX, rY, sX, sY


def run_cell(label, N, f_g, snr_db, sop_rate, seeds, ckpt):
    """Run both experts on each seed for one cell; return per-seed rows + agg."""
    cached = ckpt.get(label, {}).get("rows", [])
    done = {r["seed"] for r in cached}
    rows = list(cached)
    for seed in seeds:
        if seed in done:
            continue
        t0 = time.time()
        rX, rY, sX, sY = gen_channel(N, f_g, sop_rate, snr_db, seed)
        # frozen ML: train prefix, forward full
        model = train_ml(rX, rY, sX, sY, seed)
        mlzX, mlzY = ml_forward(model, rX, rY)
        # corrected StandardCMA same realization (no compress)
        cma = p19.StandardCMA2x2(n_tap=N_TAP, mu=MU, R2=R2)
        cres = cma.equalize(rX, rY)
        czX, czY = cres["zX"], cres["zY"]
        (_, _), (_, _), (ls, le) = slices(N)
        # late slice
        ml_pi_late, ml_fx_late = pi_and_fixed(mlzX[ls:le], mlzY[ls:le],
                                              sX[ls:le], sY[ls:le])
        cma_pi_late, cma_fx_late = pi_and_fixed(czX[ls:le], czY[ls:le],
                                                sX[ls:le], sY[ls:le])
        # co-degradation guard: CMA diverged before reaching late slice
        cma_div_before_late = bool(cres["diverged"]) and \
            cres.get("diverge_idx") is not None and \
            cres["diverge_idx"] < ls
        row = {
            "seed": seed,
            "ml_late_fixed": ml_fx_late, "cma_late_fixed": cma_fx_late,
            "ml_late_pi": ml_pi_late, "cma_late_pi": cma_pi_late,
            "ml_minus_cma_fixed": ml_fx_late - cma_fx_late,
            "ml_minus_cma_pi": ml_pi_late - cma_pi_late,
            "cma_diverged": bool(cres["diverged"]),
            "cma_div_before_late": cma_div_before_late,
            "cma_diverge_idx": cres.get("diverge_idx"),
            "elapsed_s": round(time.time() - t0, 1),
        }
        rows.append(row)
        rows.sort(key=lambda r: r["seed"])
        ckpt[label] = {"rows": rows}
        _save_ckpt(ckpt)
        print(f"  [{label}] seed={seed}: "
              f"ML_fx={ml_fx_late:.4f} CMA_fx={cma_fx_late:.4f} "
              f"D_fx={ml_fx_late - cma_fx_late:+.4f} | "
              f"ML_pi={ml_pi_late:.4f} CMA_pi={cma_pi_late:.4f} "
              f"D_pi={ml_pi_late - cma_pi_late:+.4f} | "
              f"cma_div={int(cres['diverged'])} "
              f"({row['elapsed_s']:.0f}s)", flush=True)

    # aggregate
    ml_fx = np.array([r["ml_late_fixed"] for r in rows])
    cma_fx = np.array([r["cma_late_fixed"] for r in rows])
    ml_pi = np.array([r["ml_late_pi"] for r in rows])
    cma_pi = np.array([r["cma_late_pi"] for r in rows])
    d_fx = ml_fx - cma_fx
    d_pi = ml_pi - cma_pi
    cma_div_frac = float(np.mean([r["cma_div_before_late"] for r in rows]))
    ml_wins_fx = int(np.sum(d_fx < 0))   # ML < CMA => ML better
    cma_wins_fx = int(np.sum(d_fx > 0))
    return {
        "config": {"N": N, "f_G": f_g, "SNR_dB": snr_db,
                   "SOP_RATE": sop_rate, "turb": "strong",
                   "alpha_beta": [ALPHA, BETA]},
        "rows": rows,
        "mean_ml_late_fixed": float(np.mean(ml_fx)),
        "mean_cma_late_fixed": float(np.mean(cma_fx)),
        "mean_ml_late_pi": float(np.mean(ml_pi)),
        "mean_cma_late_pi": float(np.mean(cma_pi)),
        "mean_delta_ml_minus_cma_fixed": float(np.mean(d_fx)),
        "mean_delta_ml_minus_cma_pi": float(np.mean(d_pi)),
        "ml_wins_count": ml_wins_fx,
        "cma_wins_count": cma_wins_fx,
        "cma_div_frac": cma_div_frac,
    }


def _save_ckpt(ckpt):
    CKPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CKPT_PATH, "w", encoding="utf-8") as f:
        json.dump(ckpt, f, indent=2, default=str)


def _load_ckpt():
    if CKPT_PATH.exists():
        try:
            with open(CKPT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def cell_pass(cdata, direction):
    """Apply frozen crossover judgment to one cell.

    direction = 'ML' means we EXPECT ML to win (ML - CMA < -MDE, ml_wins>=4).
    direction = 'CMA' means we EXPECT CMA to win (ML - CMA > +MDE, cma_wins>=4).
    Excluded if cma_div_frac > 0.5 (co-degradation, not crossover).
    """
    cma_div_frac = cdata["cma_div_frac"]
    co_degraded = cma_div_frac > CMA_DIV_FRAC_MAX
    d_fx = cdata["mean_delta_ml_minus_cma_fixed"]
    d_pi = cdata["mean_delta_ml_minus_cma_pi"]
    if direction == "ML":
        # expect ML < CMA => delta negative, ml_wins>=4, mean < -MDE
        fixed_pass = (d_fx < -MDE_FIXED_BER
                      and cdata["ml_wins_count"] >= N_SEEDS_MIN_WINS)
        pi_pass = d_pi < 0   # direction consistency only (no MDE on secondary)
    elif direction == "CMA":
        # expect CMA < ML => delta positive, cma_wins>=4, mean > +MDE
        fixed_pass = (d_fx > MDE_FIXED_BER
                      and cdata["cma_wins_count"] >= N_SEEDS_MIN_WINS)
        pi_pass = d_pi > 0
    else:
        raise ValueError(direction)
    if co_degraded:
        fixed_pass = False
        pi_pass = False
    return fixed_pass, pi_pass, co_degraded


def main():
    t0 = time.time()
    ckpt = _load_ckpt()
    print("=" * 78)
    print("P10 Phase A fresh crossover confirmation (dev seeds 13000-13005)")
    print(f"  device={DEVICE}  ALPHA,BETA=({ALPHA},{BETA})  "
          f"N_TAP={N_TAP} mu={MU} R2={R2}")
    print(f"  MDE_fixed_ber={MDE_FIXED_BER}  min_wins={N_SEEDS_MIN_WINS}/6  "
          f"cma_div_frac_max={CMA_DIV_FRAC_MAX}")
    print("=" * 78)

    cells_meta = [
        ("ML_favored_N2M_fg30_SOP1e-7", 2_000_000, 30.0, 20.0, 1e-7, "ML"),
        ("CMA_favored_N5M_fg1000_SOP4e-7", 5_000_000, 1000.0, 20.0, 4e-7, "CMA"),
    ]

    cells_out = {}
    cell_pass_flags = {}
    for (label, N, fg, snr, sop, direction) in cells_meta:
        print(f"\n--- cell {label} (expect {direction} favored) ---", flush=True)
        cdata = run_cell(label, N, fg, snr, sop, DEV_SEEDS, ckpt)
        fp, pp, cd = cell_pass(cdata, direction)
        cdata["expected_direction"] = direction
        cdata["crossover_pass"] = bool(fp)
        cdata["pi_direction_consistent"] = bool(pp)
        cdata["co_degraded_excluded"] = bool(cd)
        cells_out[label] = cdata
        cell_pass_flags[label] = (fp, pp, cd)
        print(f"  >>> {label}: mean_ML_fx={cdata['mean_ml_late_fixed']:.4f} "
              f"mean_CMA_fx={cdata['mean_cma_late_fixed']:.4f} "
              f"D_fx={cdata['mean_delta_ml_minus_cma_fixed']:+.4f} "
              f"ml_wins={cdata['ml_wins_count']}/6 "
              f"cma_wins={cdata['cma_wins_count']}/6 "
              f"cma_div_frac={cdata['cma_div_frac']:.2f} "
              f"-> crossover_pass={fp} pi_consistent={pp}", flush=True)
        print(f"      (PI: mean_ML_pi={cdata['mean_ml_late_pi']:.4f} "
              f"mean_CMA_pi={cdata['mean_cma_late_pi']:.4f} "
              f"D_pi={cdata['mean_delta_ml_minus_cma_pi']:+.4f})", flush=True)

    # global direction consistency: fixed-label and PI both flip as predicted
    directions_consistent = all(
        cell_pass_flags[l][0] and cell_pass_flags[l][1] for l in cells_out)
    phase_a_pass = all(cell_pass_flags[l][0] for l in cells_out) and \
        directions_consistent

    verdict = "PASS" if phase_a_pass else "FAIL"
    payload = {
        "experiment": "P10 Phase A fresh crossover confirmation",
        "device": DEVICE,
        "alpha_beta_strong": [ALPHA, BETA],
        "MDE_fixed_ber": MDE_FIXED_BER,
        "min_wins": N_SEEDS_MIN_WINS,
        "dev_seeds": DEV_SEEDS,
        "ml_params": {k: v for k, v in ML_PARAMS.items()},
        "cma_params": {"n_tap": N_TAP, "mu": MU, "R2": R2, "block": 64,
                       "method": "Godard 1980 with-z"},
        "cells": cells_out,
        "crossover_directions_consistent": bool(directions_consistent),
        "phase_a_verdict": verdict,
        "terminal_if_fail": "PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE",
        "elapsed_s": round(time.time() - t0, 1),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    # final stdout summary
    print("\n" + "=" * 78)
    print("Phase A summary")
    print("=" * 78)
    for label, cdata in cells_out.items():
        print(f"  [{label}] (expect {cdata['expected_direction']})")
        print(f"    FIXED-PRIMARY: ML={cdata['mean_ml_late_fixed']:.4f} "
              f"CMA={cdata['mean_cma_late_fixed']:.4f} "
              f"D(ML-CMA)={cdata['mean_delta_ml_minus_cma_fixed']:+.4f} "
              f"ml_wins={cdata['ml_wins_count']}/6 "
              f"cma_wins={cdata['cma_wins_count']}/6")
        print(f"    PI-SECONDARY : ML={cdata['mean_ml_late_pi']:.4f} "
              f"CMA={cdata['mean_cma_late_pi']:.4f} "
              f"D(ML-CMA)={cdata['mean_delta_ml_minus_cma_pi']:+.4f}")
        print(f"    cma_div_frac={cdata['cma_div_frac']:.2f} "
              f"crossover_pass={cdata['crossover_pass']} "
              f"pi_consistent={cdata['pi_direction_consistent']}")
    print(f"\n  crossover_directions_consistent = {directions_consistent}")
    print(f"  phase_a_verdict = {verdict}")
    if verdict == "FAIL":
        # one-line physics attribution
        ml_cell = cells_out["ML_favored_N2M_fg30_SOP1e-7"]
        cma_cell = cells_out["CMA_favored_N5M_fg1000_SOP4e-7"]
        if (ml_cell["mean_delta_ml_minus_cma_fixed"] > 0
                and cma_cell["mean_delta_ml_minus_cma_fixed"] > 0):
            attr = ("CMA wins both cells on fixed-label -> standard-CMA already "
                    "recovers swap everywhere (P05 old-path); no router room.")
        elif (ml_cell["mean_delta_ml_minus_cma_fixed"] < 0
              and cma_cell["mean_delta_ml_minus_cma_fixed"] < 0):
            attr = ("ML wins both cells on fixed-label -> no ranking crossover; "
                    "no router room.")
        else:
            attr = ("directions inconsistent between cells OR between fixed/PI "
                    "apertures -> crossover not cleanly reproducible.")
        print(f"  physics_attribution: {attr}")
    print(f"  terminal_if_fail = {payload['terminal_if_fail']}")
    print(f"  elapsed_s = {payload['elapsed_s']}")
    print(f"  results -> {OUT_PATH}")
    return payload


if __name__ == "__main__":
    main()
