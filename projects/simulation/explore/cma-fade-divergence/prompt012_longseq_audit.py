"""PROMPT-012 audits D014 and D015 with fixed-label and PI BER.

The channel and algorithm paths are reused unchanged from PROMPT-010.  For
each seed, current CMA, supervised ML (first 50% training), and oracle consume
the same generated realization.  The evaluation interval is the last quarter
of the test half, i.e. [87.5%, 100%) of the complete sequence.
"""
from __future__ import annotations

import argparse
from itertools import permutations
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))

from common._experiment import save_results
from common._config import BLOCK
from ml_long_seq_failure import (
    F_G,
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    T_S,
    compute_ber_phase_corrected,
    gen_channel,
    oracle_equalize,
    run_ml_trial,
)
from common._cma import CMAEqualizer2x2
from params import SimulationConfig


N_SYMBOLS = 5_000_000
TURBULENCE = "strong"
DEFAULT_SEEDS = tuple(range(1000, 1010))
CORR_THRESHOLD = 0.5
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt012_longseq_audit.json"
)
CLASSIFICATIONS = (
    "diverged", "same-source", "normal", "clean-swap", "degraded-swap",
    "non-swap-collapse", "mixed"
)


def test_late_slice(n_total: int, train_frac: float = 0.5, late_frac: float = 0.25):
    """Return the last ``late_frac`` of the test segment, as absolute indices."""
    n_train = int(n_total * train_frac)
    n_test = n_total - n_train
    return n_train + int(n_test * (1.0 - late_frac)), n_total


def _abs_corr(a, b):
    a = np.asarray(a) - np.mean(a)
    b = np.asarray(b) - np.mean(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(abs(np.vdot(a, b)) / denom) if denom else 0.0


def classify_failure(corr, diverged: bool, threshold: float = CORR_THRESHOLD,
                     dominance_ratio: float = 1.5, fixed_ber=None, pi_ber=None):
    """Classify in the PROMPT-012 mandated precedence order."""
    if diverged:
        return "diverged"
    corr = np.asarray(corr, dtype=float)
    winners = np.argmax(corr, axis=1)
    maxima = np.max(corr, axis=1)
    losers = np.min(corr, axis=1)
    dominant = (maxima >= threshold) & (maxima >= dominance_ratio * np.maximum(losers, 1e-15))
    if np.all(dominant) and winners[0] == winners[1]:
        return "same-source"
    if np.all(dominant):
        if tuple(winners) == (0, 1):
            return "normal"
        if tuple(winners) == (1, 0):
            pi_confirms = (
                fixed_ber is not None and pi_ber is not None
                and pi_ber <= 0.2 and fixed_ber - pi_ber >= 0.05
            )
            if not pi_confirms:
                return "mixed"
            return "clean-swap" if pi_ber <= 0.05 else "degraded-swap"
    if np.all(corr < threshold):
        return "non-swap-collapse"
    return "mixed"


def evaluate_outputs(z_x, z_y, s_x, s_y, diverged: bool):
    """Compute dual-stream fixed BER, full 2!x4x4 PI BER, and correlations."""
    outputs = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))
    fixed_per_output = [
        compute_ber_phase_corrected(outputs[0], sources[0]),
        compute_ber_phase_corrected(outputs[1], sources[1]),
    ]
    candidates = []
    for assignment in permutations((0, 1)):
        bers = [
            compute_ber_phase_corrected(outputs[i], sources[assignment[i]])
            for i in range(2)
        ]
        candidates.append((float(np.mean(bers)), assignment, bers))
    pi_mean, assignment, pi_per_output = min(candidates, key=lambda item: item[0])
    corr = np.array([
        [_abs_corr(outputs[0], sources[0]), _abs_corr(outputs[0], sources[1])],
        [_abs_corr(outputs[1], sources[0]), _abs_corr(outputs[1], sources[1])],
    ])
    return {
        "fixed_label_ber": {
            "zX_sX": float(fixed_per_output[0]),
            "zY_sY": float(fixed_per_output[1]),
            "mean": float(np.mean(fixed_per_output)),
        },
        "permutation_invariant_ber": {
            "mean": pi_mean,
            "per_output": [float(x) for x in pi_per_output],
            "assignment": ["sX" if i == 0 else "sY" for i in assignment],
        },
        "abs_corr": {
            "zX_sX": float(corr[0, 0]), "zX_sY": float(corr[0, 1]),
            "zY_sX": float(corr[1, 0]), "zY_sY": float(corr[1, 1]),
        },
        "abs_corr_zX_zY": _abs_corr(outputs[0], outputs[1]),
        "classification": classify_failure(
            corr, diverged, fixed_ber=float(np.mean(fixed_per_output)), pi_ber=pi_mean
        ),
        "diverged": bool(diverged),
    }


def summarize_trials(trials, methods=("current_cma", "ml", "oracle")):
    summaries = {}
    for method in methods:
        summary = {}
        for output_key, metric_key in (
            ("fixed_label_ber", "fixed_label_ber"),
            ("permutation_invariant_ber", "permutation_invariant_ber"),
        ):
            values = [float(t["methods"][method][metric_key]["mean"]) for t in trials]
            summary[output_key] = {
                "mean": float(np.mean(values)), "std": float(np.std(values)), "values": values
            }
        counts = {
            label: sum(t["methods"][method]["classification"] == label for t in trials)
            for label in CLASSIFICATIONS
        }
        summary["classification_count"] = counts
        summary["classification_fraction"] = {
            label: count / len(trials) for label, count in counts.items()
        }
        summary["diverged_count"] = sum(
            bool(t["methods"][method]["diverged"]) for t in trials
        )
        summaries[method] = summary
    return summaries


def save_audit_results(payload, path=RESULT_PATH):
    payload["script_sha256"] = script_sha256()
    save_results(payload, str(path), "prompt012_longseq_audit")


def script_sha256(script_bytes=None, helper_bytes=None):
    if script_bytes is None:
        script_bytes = Path(__file__).read_bytes()
    if helper_bytes is None:
        helper_bytes = Path(__file__).with_name("ml_long_seq_failure.py").read_bytes()
    return hashlib.sha256(script_bytes + b"\0" + helper_bytes).hexdigest()


def pending_seeds(seeds, checkpoint):
    completed = {int(trial["seed"]) for trial in checkpoint.get("trials", [])}
    return [int(seed) for seed in seeds if int(seed) not in completed]


def seed_ml(seed):
    import torch
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.manual_seed(int(seed))
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(int(seed))


def seed_fields(seed):
    return {"seed": int(seed), "torch_seed": int(seed)}


def ml_diverged(ml_result, z_x, z_y):
    return bool(ml_result.get("diverged", False)) or not (
        np.all(np.isfinite(z_x)) and np.all(np.isfinite(z_y))
    )


def validate_checkpoint(checkpoint, requested_signature, expected_script_sha):
    if checkpoint.get("experiment_signature") != requested_signature:
        raise ValueError("checkpoint experiment signature mismatch")
    if checkpoint.get("script_sha256") != expected_script_sha:
        raise ValueError("checkpoint script SHA256 mismatch")


def filter_trials(trials, allowed_keys, key_fn):
    kept, seen = [], set()
    for trial in trials:
        key = key_fn(trial)
        if key in allowed_keys and key not in seen:
            kept.append(trial)
            seen.add(key)
    return kept


def build_contract(alpha, beta, late_slice, seeds=DEFAULT_SEEDS):
    seed_list = [int(seed) for seed in seeds]
    parameters = {
        "N": N_SYMBOLS, "T_S": T_S, "SOP": SOP_RATE, "f_G": F_G,
        "turbulence": TURBULENCE, "snr_db": 20, "modulation": "QPSK",
        "ml_train_fraction": 0.5, "test_late_slice": list(late_slice),
        "cma_mu": MU_SAFE, "cma_n_tap": N_TAP, "cma_R2": R2_QPSK,
        "seeds": seed_list,
    }
    signature = {
        "N": N_SYMBOLS, "T_S": T_S, "SOP": SOP_RATE, "f_G": F_G,
        "turbulence": TURBULENCE, "alpha": alpha, "beta": beta,
        "gamma_bar": GAMMA_BAR, "modulation": "QPSK", "train_fraction": 0.5,
        "evaluation_slice": list(late_slice), "cma_mu": MU_SAFE,
        "cma_n_tap": N_TAP, "cma_R2": R2_QPSK, "block": BLOCK,
        "seeds": seed_list,
    }
    return parameters, signature


def run(seeds=DEFAULT_SEEDS):
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    late_start, late_end = test_late_slice(N_SYMBOLS)
    parameters, signature = build_contract(alpha, beta, (late_start, late_end), seeds)
    initial_payload = {
        "experiment": "PROMPT-012 D014+D015 long-sequence dual-metric audit",
        "parameters": parameters,
        "classification_rule": {
            "precedence": list(CLASSIFICATIONS), "main_correlation_threshold": CORR_THRESHOLD
        },
        "pi_ber_note": "2!x4x4 ambiguity removal requires pilot/frame-header overhead",
        "experiment_signature": signature,
        "trials": [],
    }
    if RESULT_PATH.exists():
        with open(RESULT_PATH, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_checkpoint(payload, signature, script_sha256())
    else:
        payload = initial_payload
    payload["parameters"] = initial_payload["parameters"]
    payload["parameters"]["seeds"] = [int(seed) for seed in seeds]
    payload["experiment_signature"] = signature
    payload["trials"] = filter_trials(
        payload.get("trials", []), set(map(int, seeds)), lambda trial: int(trial["seed"])
    )
    for seed in pending_seeds(seeds, payload):
        started = time.time()
        r_x, r_y, s_x, s_y, h, theta = gen_channel(
            N_SYMBOLS, alpha, beta, F_G, SOP_RATE, int(seed)
        )
        methods = {}

        cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
        cma_result = cma.equalize(r_x, r_y)
        methods["current_cma"] = evaluate_outputs(
            cma_result["zX"][late_start:late_end],
            cma_result["zY"][late_start:late_end],
            s_x[late_start:late_end], s_y[late_start:late_end],
            bool(cma_result["diverged"]),
        )
        methods["current_cma"]["diverge_idx"] = cma_result["diverge_idx"]
        methods["current_cma"]["final_w_norm"] = float(cma_result["final_w_norm"])
        methods["current_cma"]["init_w_norm"] = float(cma_result["init_w_norm"])
        del cma_result, cma

        seed_ml(seed)
        z_x_ml, z_y_ml, n_train, ml_result = run_ml_trial(r_x, r_y, s_x, s_y)
        ml_has_diverged = ml_diverged(ml_result, z_x_ml, z_y_ml)
        methods["ml"] = evaluate_outputs(
            z_x_ml[late_start:late_end], z_y_ml[late_start:late_end],
            s_x[late_start:late_end], s_y[late_start:late_end], ml_has_diverged,
        )
        methods["ml"]["n_train"] = int(n_train)
        del z_x_ml, z_y_ml, ml_result

        z_x_or, z_y_or = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)
        methods["oracle"] = evaluate_outputs(
            z_x_or[late_start:late_end], z_y_or[late_start:late_end],
            s_x[late_start:late_end], s_y[late_start:late_end], False,
        )
        del z_x_or, z_y_or, r_x, r_y, s_x, s_y, h, theta

        payload["trials"].append({
            **seed_fields(seed), "methods": methods, "elapsed_s": time.time() - started
        })
        payload["summaries"] = summarize_trials(payload["trials"])
        save_audit_results(payload)
        print(
            f"seed={seed} " + " ".join(
                f"{name}:fixed={metrics['fixed_label_ber']['mean']:.4f},"
                f"pi={metrics['permutation_invariant_ber']['mean']:.4f},"
                f"class={metrics['classification']}"
                for name, metrics in methods.items()
            ), flush=True,
        )
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=10)
    args = parser.parse_args()
    if not 1 <= args.seeds <= len(DEFAULT_SEEDS):
        parser.error("--seeds must be between 1 and 10")
    run(DEFAULT_SEEDS[:args.seeds])
