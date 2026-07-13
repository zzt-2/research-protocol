"""PROMPT-012 N=2M audit of the historical ML-vs-CMA claim.

Both the full test half and the last quarter of that test half are saved so
the S009 whole-test interpretation and PROMPT-012 test-late interpretation can
be compared without silently changing the evaluation window.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))

from common._cma import CMAEqualizer2x2
from common._config import BLOCK
from common._experiment import save_results
from ml_long_seq_failure import (
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    T_S,
    gen_channel,
    oracle_equalize,
    run_ml_trial,
)
from params import SimulationConfig
from prompt012_longseq_audit import (
    evaluate_outputs, ml_diverged, script_sha256 as long_script_sha256, seed_fields, seed_ml,
    summarize_trials, validate_checkpoint,
)


N_SYMBOLS = 2_000_000
TURBULENCE = "strong"
DEFAULT_F_G = (30.0, 100.0, 1000.0)
DEFAULT_SEEDS = tuple(range(1000, 1010))
METHODS = ("current_cma", "ml", "oracle")
WINDOWS = ("test_full", "test_late")
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt012_shortseq_audit.json"
)


def evaluation_slices(n_total: int):
    n_train = int(n_total * 0.5)
    n_test = n_total - n_train
    return {
        "test_full": (n_train, n_total),
        "test_late": (n_train + int(0.75 * n_test), n_total),
    }


def build_contract(alpha, beta, slices, f_g_values=DEFAULT_F_G, seeds=DEFAULT_SEEDS):
    frozen_slices = {key: list(value) for key, value in slices.items()}
    seed_list = [int(seed) for seed in seeds]
    parameters = {
        "N": N_SYMBOLS, "T_S": T_S, "SOP": SOP_RATE, "f_G": list(f_g_values),
        "turbulence": TURBULENCE, "snr_db": 20, "modulation": "QPSK",
        "ml_train_fraction": 0.5, "evaluation_slices": frozen_slices,
        "seeds": seed_list, "cma_mu": MU_SAFE, "cma_n_tap": N_TAP,
        "cma_R2": R2_QPSK,
    }
    signature = {
        "N": N_SYMBOLS, "T_S": T_S, "SOP": SOP_RATE, "f_G": list(f_g_values),
        "turbulence": TURBULENCE, "alpha": alpha, "beta": beta,
        "gamma_bar": GAMMA_BAR, "modulation": "QPSK", "train_fraction": 0.5,
        "evaluation_slices": frozen_slices, "cma_mu": MU_SAFE,
        "cma_n_tap": N_TAP, "cma_R2": R2_QPSK, "block": BLOCK,
        "seeds": seed_list,
        "requested_cells": [[float(f_g), int(seed)] for f_g in f_g_values for seed in seeds],
    }
    return parameters, signature


def pending_cells(f_g_values, seeds, checkpoint):
    completed = {
        (float(trial["f_G"]), int(trial["seed"]))
        for trial in checkpoint.get("trials", [])
    }
    return [
        (float(f_g), int(seed))
        for f_g in f_g_values for seed in seeds
        if (float(f_g), int(seed)) not in completed
    ]


def summarize_grid(trials, methods=METHODS):
    summary = {}
    for f_g in sorted({float(trial["f_G"]) for trial in trials}):
        f_key = f"{f_g:g}"
        summary[f_key] = {}
        selected = [trial for trial in trials if float(trial["f_G"]) == f_g]
        for window in WINDOWS:
            if not all(window in trial["windows"] for trial in selected):
                continue
            adapted = [
                {"methods": trial["windows"][window]["methods"]} for trial in selected
            ]
            summary[f_key][window] = summarize_trials(adapted, methods)
    return summary


def save_shortseq_results(payload, path=RESULT_PATH):
    payload["script_sha256"] = composite_script_sha256()
    save_results(payload, str(path), "prompt012_shortseq_audit")


def composite_script_sha256():
    own = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return hashlib.sha256((own + long_script_sha256()).encode("ascii")).hexdigest()


def validate_shortseq_checkpoint(checkpoint, requested_signature, expected_script_sha):
    validate_checkpoint(checkpoint, requested_signature, expected_script_sha)


def filter_shortseq_trials(trials, allowed_cells):
    kept, seen = [], set()
    for trial in trials:
        key = (float(trial["f_G"]), int(trial["seed"]))
        if key in allowed_cells and key not in seen:
            kept.append(trial)
            seen.add(key)
    return kept


def _window_metrics(outputs, sources, slices, diverged):
    result = {}
    for name, (start, end) in slices.items():
        result[name] = evaluate_outputs(
            outputs[0][start:end], outputs[1][start:end],
            sources[0][start:end], sources[1][start:end], diverged,
        )
    return result


def run(f_g_values=DEFAULT_F_G, seeds=DEFAULT_SEEDS, max_cells=None):
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    slices = evaluation_slices(N_SYMBOLS)
    parameters, signature = build_contract(alpha, beta, slices, f_g_values, seeds)
    initial_payload = {
        "experiment": "PROMPT-012 S009 N=2M dual-metric audit",
        "parameters": parameters,
        "pi_ber_note": "2!x4x4 ambiguity removal requires pilot/frame-header overhead",
        "experiment_signature": signature,
        "trials": [],
    }
    if RESULT_PATH.exists():
        with open(RESULT_PATH, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_shortseq_checkpoint(payload, signature, composite_script_sha256())
    else:
        payload = initial_payload
    payload["parameters"] = initial_payload["parameters"]
    payload["experiment_signature"] = signature
    allowed_cells = {(float(f_g), int(seed)) for f_g in f_g_values for seed in seeds}
    payload["trials"] = filter_shortseq_trials(payload.get("trials", []), allowed_cells)
    cells = pending_cells(f_g_values, seeds, payload)
    if max_cells is not None:
        cells = cells[:max_cells]

    for f_g, seed in cells:
        started = time.time()
        r_x, r_y, s_x, s_y, h, theta = gen_channel(
            N_SYMBOLS, alpha, beta, f_g, SOP_RATE, seed
        )
        source_pair = (s_x, s_y)

        cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
        cma_result = cma.equalize(r_x, r_y)
        per_method = {
            "current_cma": _window_metrics(
                (cma_result["zX"], cma_result["zY"]), source_pair, slices,
                bool(cma_result["diverged"]),
            )
        }
        cma_extra = {
            "diverge_idx": cma_result["diverge_idx"],
            "final_w_norm": float(cma_result["final_w_norm"]),
            "init_w_norm": float(cma_result["init_w_norm"]),
        }
        del cma_result, cma

        seed_ml(seed)
        z_x_ml, z_y_ml, n_train, ml_result = run_ml_trial(r_x, r_y, s_x, s_y)
        ml_has_diverged = ml_diverged(ml_result, z_x_ml, z_y_ml)
        per_method["ml"] = _window_metrics(
            (z_x_ml, z_y_ml), source_pair, slices, ml_has_diverged
        )
        del z_x_ml, z_y_ml, ml_result

        z_x_or, z_y_or = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)
        per_method["oracle"] = _window_metrics(
            (z_x_or, z_y_or), source_pair, slices, False
        )
        del z_x_or, z_y_or, r_x, r_y, s_x, s_y, h, theta

        windows = {}
        for window in WINDOWS:
            methods = {method: per_method[method][window] for method in METHODS}
            methods["current_cma"].update(cma_extra)
            methods["ml"]["n_train"] = int(n_train)
            windows[window] = {"slice": list(slices[window]), "methods": methods}
        payload["trials"].append({
            "f_G": f_g, **seed_fields(seed), "windows": windows,
            "elapsed_s": time.time() - started,
        })
        payload["summaries"] = summarize_grid(payload["trials"])
        save_shortseq_results(payload)
        print(
            f"f_G={f_g:g} seed={seed} " + " ".join(
                f"{method}:test(f={windows['test_full']['methods'][method]['fixed_label_ber']['mean']:.4f},"
                f"pi={windows['test_full']['methods'][method]['permutation_invariant_ber']['mean']:.4f});"
                f"late(f={windows['test_late']['methods'][method]['fixed_label_ber']['mean']:.4f},"
                f"pi={windows['test_late']['methods'][method]['permutation_invariant_ber']['mean']:.4f})"
                for method in METHODS
            ), flush=True,
        )
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cells", type=int)
    args = parser.parse_args()
    run(max_cells=args.max_cells)
