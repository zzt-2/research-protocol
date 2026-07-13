"""PROMPT-012 audit 1: re-audit S005 divergence with dual BER metrics.

This intentionally reuses the later S009 signal generator.  S005 used
``theta = 1e-4 * arange(N)`` while PROMPT-012 freezes the corrected historical
chain at ``SOP_RATE = 4e-7 rad/symbol``.  Both values are recorded in metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))

from common._cma import CMAEqualizer2x2
from common._experiment import save_results
from params import SimulationConfig
from r_lcr_ber_impact import (
    BLOCK,
    GAMMA_BAR,
    T_S,
    compute_ber_phase_corrected,
    gen_channel,
)


N_SYMBOLS = 5_000_000
N_TAP = 11
R2_QPSK = 1.0
TURBULENCE = "strong"
F_G_GRID = (100.0, 1000.0)
MU_GRID = (1e-3, 1e-2)
SOP_RATE = 4e-7
S005_ORIGINAL_SOP_RATE = 1e-4
SEEDS = tuple(range(1000, 1010))
DOMINANCE_RATIO = 1.5
COLLAPSE_CORR_THRESHOLD = 0.5
LATE_START_FRAC = 0.875
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence"
    / "prompt012_divergence_audit.json"
)


def _abs_corr(a, b):
    a = np.asarray(a) - np.mean(a)
    b = np.asarray(b) - np.mean(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(abs(np.vdot(a, b)) / denom) if denom else 0.0


def dual_ber_metrics(z_x, z_y, s_x, s_y):
    """Return fixed-label and permutation-invariant phase-corrected BER."""
    outputs = (z_x, z_y)
    sources = (s_x, s_y)
    pair = np.asarray([
        [compute_ber_phase_corrected(outputs[i], sources[j])[0]
         for j in range(2)]
        for i in range(2)
    ])
    fixed_values = [float(pair[0, 0]), float(pair[1, 1])]
    candidates = [
        (float(np.mean([pair[0, 0], pair[1, 1]])), (0, 1)),
        (float(np.mean([pair[0, 1], pair[1, 0]])), (1, 0)),
    ]
    pi_mean, assignment = min(candidates, key=lambda item: item[0])
    pi_values = [float(pair[i, assignment[i]]) for i in range(2)]
    return {
        "fixed_ber": {"per_output": fixed_values,
                      "mean": float(np.mean(fixed_values))},
        "pi_ber": {"per_output": pi_values, "mean": pi_mean,
                   "assignment": ["X" if source == 0 else "Y"
                                  for source in assignment]},
        "pairwise_ber": pair.tolist(),
    }


def classify_outputs(z_x, z_y, s_x, s_y):
    """Classify a stable trial without confusing output permutation with failure."""
    corr = np.asarray([
        [_abs_corr(z_x, s_x), _abs_corr(z_x, s_y)],
        [_abs_corr(z_y, s_x), _abs_corr(z_y, s_y)],
    ])
    if float(np.max(corr)) < COLLAPSE_CORR_THRESHOLD:
        classification = "collapse"
    else:
        choices = []
        dominant = True
        for row in corr:
            order = np.argsort(row)
            dominant &= row[order[-1]] >= DOMINANCE_RATIO * max(row[order[-2]], 1e-15)
            choices.append(int(order[-1]))
        if not dominant:
            classification = "mixed"
        elif choices == [0, 1]:
            classification = "normal"
        elif choices == [1, 0]:
            classification = "swap"
        else:
            classification = "same-source"
    return {
        "classification": classification,
        "abs_corr_output_source": {
            "zX": {"sX": float(corr[0, 0]), "sY": float(corr[0, 1])},
            "zY": {"sX": float(corr[1, 0]), "sY": float(corr[1, 1])},
        },
        "abs_corr_zX_zY": _abs_corr(z_x, z_y),
    }


def divergence_reasons(final_norm, init_norm, max_zamp):
    """Infer threshold causes only; BER and output permutation are never causes."""
    if not np.all(np.isfinite([final_norm, init_norm, max_zamp])):
        return ["nonfinite"]
    reasons = []
    if final_norm > 10.0 * init_norm:
        reasons.append("norm>10x")
    if max_zamp > 1e3:
        reasons.append("zamp>1e3")
    return reasons


def validate_divergence_consistency(diverged, reasons):
    """Fail closed if the equalizer flag disagrees with independent thresholds."""
    if bool(diverged) != bool(reasons):
        raise RuntimeError(
            f"divergence inconsistency: equalizer={bool(diverged)}, reasons={reasons}"
        )


def _stats(values):
    if not values:
        return None
    return {"mean": float(np.mean(values)), "std": float(np.std(values)),
            "values": [float(value) for value in values]}


def summarize_grid(trials):
    stable = [trial for trial in trials if not trial["diverged"]]
    reason_counts = Counter(
        reason for trial in trials for reason in trial["divergence_reasons"]
    )
    class_counts = Counter(trial["classification"] for trial in stable)
    n = len(trials)
    return {
        "n_trials": n,
        "n_diverged": n - len(stable),
        "p_div": (n - len(stable)) / n if n else float("nan"),
        "n_ber_trials": len(stable),
        "divergence_reason_counts": {
            reason: int(reason_counts.get(reason, 0))
            for reason in ("norm>10x", "zamp>1e3", "nonfinite")
        },
        "classification_counts": {
            label: int(class_counts.get(label, 0))
            for label in ("normal", "swap", "same-source", "collapse", "mixed")
        },
        "swap_rate_among_stable": (
            class_counts.get("swap", 0) / len(stable) if stable else None
        ),
        "fixed_ber": _stats([trial["fixed_ber"]["mean"] for trial in stable]),
        "pi_ber": _stats([trial["pi_ber"]["mean"] for trial in stable]),
    }


def run_trial(alpha, beta, f_g, mu, seed, n_symbols=N_SYMBOLS):
    started = time.time()
    r_x, r_y, s_x, s_y, _h, _theta = gen_channel(
        n_symbols, alpha, beta, f_g, SOP_RATE, int(seed)
    )
    equalizer = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
    result = equalizer.equalize(r_x, r_y)
    final_norm = float(result["final_w_norm"])
    init_norm = float(result["init_w_norm"])
    z_traj = np.asarray(result["z_amp_traj"])
    max_zamp = float(np.max(z_traj)) if z_traj.size else 0.0
    reasons = divergence_reasons(final_norm, init_norm, max_zamp)
    diverged = bool(result["diverged"])
    validate_divergence_consistency(diverged, reasons)
    trial = {
        "seed": int(seed),
        "diverged": diverged,
        "diverge_idx": (int(result["diverge_idx"])
                        if result["diverge_idx"] is not None else None),
        "final_norm": final_norm,
        "init_norm": init_norm,
        "final_norm_over_init_norm": final_norm / init_norm,
        "max_zamp": max_zamp,
        "divergence_reasons": reasons,
        "classification": None,
        "fixed_ber": None,
        "pi_ber": None,
        "elapsed_s": None,
    }
    if not diverged:
        start = int(n_symbols * LATE_START_FRAC)
        metrics = dual_ber_metrics(
            result["zX"][start:], result["zY"][start:],
            s_x[start:], s_y[start:],
        )
        classification = classify_outputs(
            result["zX"][start:], result["zY"][start:],
            s_x[start:], s_y[start:],
        )
        trial.update(metrics)
        trial.update(classification)
    trial["elapsed_s"] = time.time() - started
    return trial


def run_grid(alpha, beta, f_g, mu, seeds, n_symbols, trial_fn=run_trial):
    """Run one grid with an explicit shared seed list and summarize it."""
    trials = [
        trial_fn(alpha, beta, f_g, mu, seed, n_symbols)
        for seed in seeds
    ]
    return {"f_g_hz": f_g, "mu": mu, "trials": trials,
            "summary": summarize_grid(trials)}


def build_payload(grids, seeds, n_symbols, alpha, beta):
    """Build the auditable result payload independently of expensive execution."""
    return {
        "experiment": "PROMPT-012 audit 1: S005 divergence",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parameters": {
            "N": n_symbols,
            "turbulence": TURBULENCE,
            "alpha": alpha,
            "beta": beta,
            "modulation": "QPSK",
            "n_tap": N_TAP,
            "R2": R2_QPSK,
            "gamma_bar": float(GAMMA_BAR),
            "T_S": float(T_S),
            "channel_block": int(BLOCK),
            "f_g_hz": list(F_G_GRID),
            "mu": list(MU_GRID),
            "seeds": list(map(int, seeds)),
            "sop_rate_rad_per_symbol": SOP_RATE,
            "s005_original_sop_rate_rad_per_symbol": S005_ORIGINAL_SOP_RATE,
            "sop_difference_note": (
                "PROMPT-012 freezes r_lcr/S009 SOP=4e-7; original S005 used 1e-4"
            ),
            "late_slice": [LATE_START_FRAC, 1.0],
        },
        "definitions": {
            "divergence": "norm>10x init OR zamp>1e3 OR nonfinite",
            "ber_scope": "computed only for non-diverged trials",
            "pi_note": "PI-BER removes blind X/Y permutation but needs pilot/header overhead",
            "classification": (
                "collapse if all output-source |corr|<0.5; otherwise normal/swap/"
                "same-source when each output has >=1.5x dominant source; else mixed"
            ),
        },
        "grids": grids,
    }


def run_audit(seeds=SEEDS, n_symbols=N_SYMBOLS):
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    grids = []
    total = len(F_G_GRID) * len(MU_GRID) * len(seeds)
    count = 0
    for f_g in F_G_GRID:
        for mu in MU_GRID:
            grid = run_grid(alpha, beta, f_g, mu, seeds, n_symbols)
            grids.append(grid)
            for trial in grid["trials"]:
                count += 1
                print(
                    f"[{count}/{total}] f_G={f_g:g} mu={mu:g} seed={trial['seed']} "
                    f"div={trial['diverged']} reason={trial['divergence_reasons']} "
                    f"class={trial['classification']} "
                    f"fixed={None if trial['fixed_ber'] is None else trial['fixed_ber']['mean']} "
                    f"pi={None if trial['pi_ber'] is None else trial['pi_ber']['mean']} "
                    f"elapsed={trial['elapsed_s']:.1f}s",
                    flush=True,
                )

    payload = build_payload(grids, seeds, n_symbols, alpha, beta)
    save_results(payload, str(RESULT_PATH), "prompt012_divergence_audit")
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-symbols", type=int, default=N_SYMBOLS)
    parser.add_argument("--n-seeds", type=int, default=len(SEEDS))
    args = parser.parse_args()
    run_audit(SEEDS[:args.n_seeds], args.n_symbols)
