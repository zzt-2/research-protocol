"""PROMPT-013 Q1: resumable swap-quality significance experiment.

This script only answers whether the CMA/ML PI-BER gap is reproducible.  It
imports seeds 1000--1009 from PROMPT-012, then appends seeds 1010--1029 in
batches of at most five.  Every method in a new trial consumes the same dual-
polarization realization.  Q2 mechanism experiments are intentionally absent.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
from scipy.stats import wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common._cma import CMAEqualizer2x2
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
    gen_channel as generate_shared_dual_pol_realization,
    oracle_equalize,
    run_ml_trial,
)
from params import SimulationConfig
from prompt012_longseq_audit import (
    build_contract as build_prompt012_contract,
    evaluate_outputs,
    ml_diverged,
    seed_fields,
    seed_ml,
    script_sha256 as prompt012_composite_sha256,
    test_late_slice,
)


N_SYMBOLS = 5_000_000
TURBULENCE = "strong"
SOURCE_SEEDS = tuple(range(1000, 1010))
NEW_SEEDS = tuple(range(1010, 1030))
TARGET_SEEDS = SOURCE_SEEDS + NEW_SEEDS
SOURCE_RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt012_longseq_audit.json"
)
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt013_swap_quality.json"
)
LOCK_PATH = RESULT_PATH.with_suffix(".lock")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_sha256s(contents=None):
    """Hash every implementation dependency that can alter a Q1 trial."""
    if contents is not None:
        return {name: hashlib.sha256(data).hexdigest() for name, data in contents.items()}
    paths = {
        "prompt013_swap_quality_q1.py": Path(__file__),
        "prompt012_longseq_audit.py": Path(__file__).with_name("prompt012_longseq_audit.py"),
        "ml_long_seq_failure.py": Path(__file__).with_name("ml_long_seq_failure.py"),
        "common/_cma.py": SIM_DIR / "common" / "_cma.py",
        "common/_ml_equalizer.py": SIM_DIR / "common" / "_ml_equalizer.py",
        "common/_gg_time.py": SIM_DIR / "common" / "_gg_time.py",
        "common/_config.py": SIM_DIR / "common" / "_config.py",
        "common/_equalizer.py": SIM_DIR / "common" / "_equalizer.py",
        "params.py": SIM_DIR / "params.py",
    }
    return {name: _sha256(path) for name, path in paths.items()}


def _swap_quality(method, threshold: float, inclusive: bool) -> str:
    pi = float(method["permutation_invariant_ber"]["mean"])
    fixed = float(method["fixed_label_ber"]["mean"])
    assignment = method["permutation_invariant_ber"].get("assignment")
    is_swap = assignment == ["sY", "sX"] and pi <= 0.2 and fixed - pi >= 0.05
    if not is_swap:
        return str(method.get("classification", "mixed"))
    clean = pi <= threshold if inclusive else pi < threshold
    return "clean-swap" if clean else "degraded-swap"


def annotate_trial(trial, origin: str):
    """Add Q1 continuous and descriptive metrics without dropping raw metrics."""
    annotated = deepcopy(trial)
    annotated["origin"] = origin
    annotated["shared_realization_seed"] = int(annotated["seed"])
    oracle = float(
        annotated["methods"]["oracle"]["permutation_invariant_ber"]["mean"]
    )
    for name in ("current_cma", "ml", "oracle"):
        method = annotated["methods"][name]
        pi = float(method["permutation_invariant_ber"]["mean"])
        method["excess_pi_ber_vs_oracle"] = round(pi - oracle, 15)
        if name != "oracle":
            method["descriptive_swap_quality"] = {
                "pi_ber_le_0.05": _swap_quality(method, 0.05, True),
                "pi_ber_lt_0.01": _swap_quality(method, 0.01, False),
            }
    return annotated


def import_prompt012_trials(source_payload):
    trials = source_payload.get("trials", [])
    by_seed = {int(trial["seed"]): trial for trial in trials}
    if set(by_seed) != set(SOURCE_SEEDS) or len(trials) != len(SOURCE_SEEDS):
        raise ValueError("PROMPT-012 source must contain exactly seeds 1000--1009")
    return [annotate_trial(by_seed[seed], "prompt012") for seed in SOURCE_SEEDS]


def validate_prompt012_source(source_payload, alpha, beta):
    """Fail before import if PROMPT-012 code provenance or contract drifted."""
    if source_payload.get("script_sha256") != prompt012_composite_sha256():
        raise ValueError("PROMPT-012 source composite SHA256 mismatch")
    _, expected_signature = build_prompt012_contract(
        alpha, beta, test_late_slice(N_SYMBOLS), SOURCE_SEEDS
    )
    if source_payload.get("experiment_signature") != expected_signature:
        raise ValueError("PROMPT-012 source experiment signature mismatch")


def validate_checkpoint_trials(trials):
    """Validate completed checkpoint rows; new seeds may be partially absent."""
    seeds = [int(trial["seed"]) for trial in trials]
    counts = Counter(seeds)
    duplicates = sorted(seed for seed, count in counts.items() if count > 1)
    unexpected = sorted(set(seeds) - set(TARGET_SEEDS))
    missing_source = sorted(set(SOURCE_SEEDS) - set(seeds))
    if duplicates:
        raise ValueError(f"checkpoint duplicate seeds: {duplicates}")
    if unexpected:
        raise ValueError(f"checkpoint unexpected seeds: {unexpected}")
    if missing_source:
        raise ValueError(f"checkpoint missing PROMPT-012 source seeds: {missing_source}")
    for trial in trials:
        for name in ("current_cma", "ml", "oracle"):
            try:
                value = float(
                    trial["methods"][name]["permutation_invariant_ber"]["mean"]
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(
                    f"checkpoint seed {trial.get('seed')} missing {name} PI-BER"
                ) from exc
            if not np.isfinite(value):
                raise ValueError(
                    f"checkpoint seed {trial['seed']} has nonfinite {name} PI-BER"
                )


def _stats(values):
    array = np.asarray(values, dtype=float)
    if len(array) == 0:
        return {"mean": None, "std": None, "median": None, "values": []}
    return {
        "mean": float(np.mean(array)),
        "std": float(np.std(array)),
        "median": float(np.median(array)),
        "values": [float(value) for value in array],
    }


def _summarize_core(ordered):
    continuous = {}
    for name in ("current_cma", "ml", "oracle"):
        pi_values = [
            trial["methods"][name]["permutation_invariant_ber"]["mean"]
            for trial in ordered
        ]
        excess_values = [
            trial["methods"][name]["excess_pi_ber_vs_oracle"] for trial in ordered
        ]
        continuous[name] = {
            "permutation_invariant_ber": _stats(pi_values),
            "excess_pi_ber_vs_oracle": _stats(excess_values),
        }

    cma_pi = np.asarray(
        continuous["current_cma"]["permutation_invariant_ber"]["values"]
    )
    ml_pi = np.asarray(continuous["ml"]["permutation_invariant_ber"]["values"])
    differences = np.round(cma_pi - ml_pi, 12)
    finite = np.isfinite(cma_pi) & np.isfinite(ml_pi)
    nonzero = differences[finite] != 0
    effective_n = int(np.sum(nonzero))
    abs_nonzero = np.abs(differences[finite][nonzero])
    has_rank_ties = len(np.unique(abs_nonzero)) != len(abs_nonzero)
    has_zeros = bool(np.any(~nonzero)) if len(differences) else False
    if len(differences) == 0:
        statistic, pvalue, method = None, None, "not-run"
    elif not np.all(finite):
        statistic, pvalue, method = None, None, "not-run-nonfinite"
    elif effective_n == 0:
        statistic, pvalue, method = 0.0, 1.0, "asymptotic"
    else:
        method = "exact" if not has_zeros and not has_rank_ties else "asymptotic"
        result = wilcoxon(
            differences,
            alternative="two-sided",
            zero_method="wilcox",
            correction=False,
            method=method,
            nan_policy="raise",
        )
        statistic, pvalue = float(result.statistic), float(result.pvalue)
    ml_wins = int(np.sum((ml_pi < cma_pi) & finite))
    cma_wins = int(np.sum((cma_pi < ml_pi) & finite))
    ties = int(np.sum((differences == 0) & finite))

    descriptive = {}
    for threshold_key in ("pi_ber_le_0.05", "pi_ber_lt_0.01"):
        descriptive[threshold_key] = {}
        for name in ("current_cma", "ml"):
            counts = Counter(
                trial["methods"][name]["descriptive_swap_quality"][threshold_key]
                for trial in ordered
            )
            descriptive[threshold_key][name] = dict(counts)

    return {
        "n_trials": len(ordered),
        "seeds": [int(trial["seed"]) for trial in ordered],
        "continuous": continuous,
        "paired_comparison": {
            "metric": "CMA excess PI-BER minus ML excess PI-BER (paired by seed)",
            "differences": [float(value) for value in differences],
            "ml_wins": ml_wins,
            "cma_wins": cma_wins,
            "ties": ties,
            "wilcoxon": {
                "statistic": statistic,
                "pvalue": pvalue,
                "alternative": "two-sided",
                "zero_method": "wilcox",
                "correction": False,
                "nan_policy": "raise",
                "method": method,
                "effective_n": effective_n,
                "has_zero_differences": has_zeros,
                "has_absolute_rank_ties": has_rank_ties,
            },
        },
        "descriptive_thresholds": descriptive,
        "descriptive_note": (
            "Threshold classifications are descriptive only; conclusions use "
            "paired continuous excess PI-BER. 0.05 is inclusive; 0.01 is strict."
        ),
    }


def summarize_q1(trials):
    ordered = sorted(trials, key=lambda trial: int(trial["seed"]))
    summary = _summarize_core(ordered)
    seed_counts = Counter(int(trial["seed"]) for trial in ordered)
    duplicate_seeds = sorted(seed for seed, count in seed_counts.items() if count > 1)
    missing_target = sorted(set(TARGET_SEEDS) - set(seed_counts))
    unexpected = sorted(set(seed_counts) - set(TARGET_SEEDS))
    nonfinite_pairs = []
    for trial in ordered:
        values = [
            trial["methods"][name]["permutation_invariant_ber"]["mean"]
            for name in ("current_cma", "ml", "oracle")
        ]
        if not np.all(np.isfinite(np.asarray(values, dtype=float))):
            nonfinite_pairs.append(int(trial["seed"]))
    integrity = {
        "duplicate_seeds": duplicate_seeds,
        "missing_target_seeds": missing_target,
        "unexpected_seeds": unexpected,
        "nonfinite_pairs": sorted(set(nonfinite_pairs)),
    }
    summary["integrity"] = integrity
    holdout = [trial for trial in ordered if int(trial["seed"]) in NEW_SEEDS]
    summary["holdout_1010_1029"] = _summarize_core(holdout)

    n_trials = len(ordered)
    integrity_failure = bool(duplicate_seeds or unexpected or nonfinite_pairs)
    if n_trials >= 30 and missing_target:
        integrity_failure = True
    pvalue = summary["paired_comparison"]["wilcoxon"]["pvalue"]
    ml_wins = summary["paired_comparison"]["ml_wins"]
    if integrity_failure:
        gate = {
            "status": "fail",
            "reason": "paired-data integrity failure",
            "p_lt_0.05": False if pvalue is None else bool(pvalue < 0.05),
            "ml_wins_at_least_25_of_30": bool(ml_wins >= 25),
        }
    elif n_trials < 30:
        gate = {
            "status": "pending",
            "reason": f"requires exactly seeds 1000--1029; currently {n_trials}",
            "p_lt_0.05": False if pvalue is None else bool(pvalue < 0.05),
            "ml_wins_at_least_25_of_30": False,
        }
    else:
        passed = pvalue is not None and pvalue < 0.05 and ml_wins >= 25
        gate = {
            "status": "pass" if passed else "fail",
            "reason": "PROMPT-013 Q1 predeclared continuous-metric gate",
            "p_lt_0.05": bool(pvalue is not None and pvalue < 0.05),
            "ml_wins_at_least_25_of_30": bool(ml_wins >= 25),
        }
    summary["q1_gate"] = gate
    return summary


def build_experiment_signature(alpha, beta, source_result_sha256):
    late_start, late_end = test_late_slice(N_SYMBOLS)
    return {
        "question": "PROMPT-013 Q1 swap-quality gap reproducibility",
        "N": N_SYMBOLS,
        "T_S": T_S,
        "SOP": SOP_RATE,
        "f_G": F_G,
        "turbulence": TURBULENCE,
        "alpha": float(alpha),
        "beta": float(beta),
        "gamma_bar": GAMMA_BAR,
        "snr_db": 20,
        "modulation": "QPSK",
        "block": BLOCK,
        "ml_train_fraction": 0.5,
        "evaluation_slice": [late_start, late_end],
        "cma_mu": MU_SAFE,
        "cma_n_tap": N_TAP,
        "cma_R2": R2_QPSK,
        "target_seeds": list(TARGET_SEEDS),
        "source_result_sha256": source_result_sha256,
        "new_seed_batches_do_not_change_signature": True,
    }


def validate_checkpoint(checkpoint, requested_signature, requested_source_sha):
    if checkpoint.get("experiment_signature") != requested_signature:
        raise ValueError("checkpoint experiment signature mismatch")
    if checkpoint.get("source_sha256") != requested_source_sha:
        raise ValueError("checkpoint source SHA256 mismatch")


def validate_batch(seeds):
    seed_list = [int(seed) for seed in seeds]
    if not 1 <= len(seed_list) <= 5:
        raise ValueError("each batch must contain 1--5 seeds")
    if len(set(seed_list)) != len(seed_list) or not set(seed_list) <= set(NEW_SEEDS):
        raise ValueError("batch seeds must be unique and within 1010--1029")
    return seed_list


def pending_seeds(seeds, checkpoint):
    completed = {int(trial["seed"]) for trial in checkpoint.get("trials", [])}
    return [int(seed) for seed in seeds if int(seed) not in completed]


@contextmanager
def exclusive_run_lock(path=LOCK_PATH):
    """Hold a cross-process atomic lock for the complete read/modify/write run."""
    lock_path = Path(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY
        )
    except FileExistsError as exc:
        raise RuntimeError(f"PROMPT-013 Q1 is already running: {lock_path}") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def save_q1_results(payload, path=RESULT_PATH):
    """Inject standard metadata into a same-directory temp, then atomically replace."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    temp_path = Path(temp_name)
    try:
        save_results(payload, str(temp_path), "prompt013_swap_quality_q1")
        os.replace(temp_path, destination)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _load_or_initialize():
    if not SOURCE_RESULT_PATH.exists():
        raise FileNotFoundError(f"PROMPT-012 source missing: {SOURCE_RESULT_PATH}")
    source_result_sha = _sha256(SOURCE_RESULT_PATH)
    source_payload = json.loads(SOURCE_RESULT_PATH.read_text(encoding="utf-8"))
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    validate_prompt012_source(source_payload, alpha, beta)
    signature = build_experiment_signature(alpha, beta, source_result_sha)
    sha_map = source_sha256s()
    if RESULT_PATH.exists():
        payload = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        validate_checkpoint(payload, signature, sha_map)
        validate_checkpoint_trials(payload.get("trials", []))
    else:
        payload = {
            "experiment": "PROMPT-013 Q1 swap-quality continuous-metric confirmation",
            "scope": "Q1 only; Q2 mechanism experiments excluded",
            "experiment_signature": signature,
            "source_sha256": sha_map,
            "source_result": str(SOURCE_RESULT_PATH.relative_to(SIM_DIR)),
            "source_result_sha256": source_result_sha,
            "shared_realization_contract": (
                "For each seed, one ml_long_seq_failure.gen_channel realization "
                "is reused by CMA, ML, and oracle."
            ),
            "pi_ber_note": "Permutation removal requires pilot/frame-header overhead",
            "trials": import_prompt012_trials(source_payload),
        }
    payload["trials"] = sorted(
        [annotate_trial(trial, trial.get("origin", "prompt013")) for trial in payload["trials"]],
        key=lambda trial: int(trial["seed"]),
    )
    validate_checkpoint_trials(payload["trials"])
    payload["summary"] = summarize_q1(payload["trials"])
    save_q1_results(payload)
    return payload, alpha, beta


def _execute_seed(seed, alpha, beta):
    started = time.time()
    late_start, late_end = test_late_slice(N_SYMBOLS)
    # One shared realization, then three consumers. Do not regenerate per method.
    r_x, r_y, s_x, s_y, h, theta = generate_shared_dual_pol_realization(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, int(seed)
    )
    methods = {}

    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    cma_result = cma.equalize(r_x, r_y)
    methods["current_cma"] = evaluate_outputs(
        cma_result["zX"][late_start:late_end],
        cma_result["zY"][late_start:late_end],
        s_x[late_start:late_end],
        s_y[late_start:late_end],
        bool(cma_result["diverged"]),
    )
    methods["current_cma"].update({
        "diverge_idx": cma_result["diverge_idx"],
        "final_w_norm": float(cma_result["final_w_norm"]),
        "init_w_norm": float(cma_result["init_w_norm"]),
    })
    del cma_result, cma

    seed_ml(seed)
    z_x_ml, z_y_ml, n_train, ml_result = run_ml_trial(r_x, r_y, s_x, s_y)
    methods["ml"] = evaluate_outputs(
        z_x_ml[late_start:late_end], z_y_ml[late_start:late_end],
        s_x[late_start:late_end], s_y[late_start:late_end],
        ml_diverged(ml_result, z_x_ml, z_y_ml),
    )
    methods["ml"]["n_train"] = int(n_train)
    del z_x_ml, z_y_ml, ml_result

    z_x_or, z_y_or = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)
    methods["oracle"] = evaluate_outputs(
        z_x_or[late_start:late_end], z_y_or[late_start:late_end],
        s_x[late_start:late_end], s_y[late_start:late_end], False,
    )
    del z_x_or, z_y_or, r_x, r_y, s_x, s_y, h, theta

    return annotate_trial({
        **seed_fields(seed),
        "methods": methods,
        "elapsed_s": time.time() - started,
    }, "prompt013")


def _run_batch_locked(seeds=()):
    payload, alpha, beta = _load_or_initialize()
    if not seeds:
        return payload
    requested = validate_batch(seeds)
    for seed in pending_seeds(requested, payload):
        trial = _execute_seed(seed, alpha, beta)
        payload["trials"].append(trial)
        payload["trials"].sort(key=lambda item: int(item["seed"]))
        payload["summary"] = summarize_q1(payload["trials"])
        save_q1_results(payload)
        comparison = payload["summary"]["paired_comparison"]
        print(
            f"seed={seed} CMA_PI={trial['methods']['current_cma']['permutation_invariant_ber']['mean']:.6f} "
            f"ML_PI={trial['methods']['ml']['permutation_invariant_ber']['mean']:.6f} "
            f"oracle_PI={trial['methods']['oracle']['permutation_invariant_ber']['mean']:.6f} "
            f"ML_wins={comparison['ml_wins']}/{payload['summary']['n_trials']}",
            flush=True,
        )
    return payload


def run_batch(seeds=()):
    with exclusive_run_lock(LOCK_PATH):
        return _run_batch_locked(seeds)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int)
    parser.add_argument("--seed-end", type=int)
    args = parser.parse_args()
    if (args.seed_start is None) != (args.seed_end is None):
        parser.error("--seed-start and --seed-end must be supplied together")
    seeds = () if args.seed_start is None else range(args.seed_start, args.seed_end + 1)
    run_batch(seeds)


if __name__ == "__main__":
    main()
