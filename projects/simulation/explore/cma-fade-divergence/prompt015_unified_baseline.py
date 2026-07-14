"""PROMPT-015: unified legal baseline re-audit for Q-CMA-FADE.

This script is intentionally isolated from common/ and params.py changes.
It reuses:
  - PROMPT-012 evaluate_outputs() for fixed/PI dual-metric evaluation
  - PROMPT-013 Q2 run_cma_diagnostic() for current/standard CMA branches
  - common._experiment.save_results() for result persistence with metadata

The heavy 30-seed / 5M-symbol experiment is not run in unit tests.  Tests only
exercise pure helpers and the dry-run checkpoint path.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from typing import Iterable

import numpy as np
from scipy.stats import wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Must be set before torch is imported by common._ml_equalizer.  The formal
# run records the requested and actual device in each ML artifact.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

from common._config import BLOCK
from common._experiment import save_results
from common._ml_equalizer import MLChannelEqualizer
from ml_long_seq_failure import (
    F_G,
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    SOP_RATE,
    T_S,
    gen_channel,
    oracle_equalize,
)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs, ml_diverged, seed_ml
from prompt013_swap_mechanism_q2 import (
    LATE_END,
    LATE_START,
    N_SYMBOLS,
    R2_QPSK,
    TURBULENCE,
    run_cma_diagnostic,
)


RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt015_unified_baseline.json"
)
EXPECTED_SEEDS = tuple(range(1000, 1030))
ML_TRAIN_FRACTION = 0.5
ML_CONFIG = {
    "n_tap": N_TAP,
    "lr": 0.005,
    "batch_size": 1024,
    "n_epochs": 20,
    "device": "cuda",
    "patience": 5,
}
METHOD_ORDER = ("current-CMA", "standard-CMA", "ML-original", "ML-aligned", "oracle")
PAIRWISE_PREDECLARED = (
    ("standard-CMA", "ML-original"),
    ("standard-CMA", "ML-aligned"),
    ("current-CMA", "ML-original"),
)
DESCRIPTIVE_ONLY = (("current-CMA", "standard-CMA"),)


def _kernel_center(branch, kernel_name: str) -> float:
    weight = getattr(branch, kernel_name).weight
    if hasattr(weight, "detach"):
        data = weight.detach().cpu().numpy()
    else:
        data = np.asarray(weight)
    center = data.shape[-1] // 2
    return float(data[0, 0, center])


def _conv_center_real(branch) -> float:
    return _kernel_center(branch, "conv_RR")


def _conv_center_imag(branch) -> float:
    return _kernel_center(branch, "conv_RI")


def _set_kernel_center(branch, kernel_name: str, value: float):
    weight = getattr(branch, kernel_name).weight
    if hasattr(weight, "detach"):
        import torch

        with torch.no_grad():
            center = weight.shape[-1] // 2
            weight[0, 0, center] = float(value)
    else:
        data = np.asarray(weight)
        center = data.shape[-1] // 2
        data[0, 0, center] = float(value)


def _set_center_real(branch, value: float):
    _set_kernel_center(branch, "conv_RR", value)


def _set_cross_center_zero(branch):
    # Explicitly set both real and imaginary kernels.  conv_RI is zero in the
    # current constructor, but recording the operation makes the alignment
    # contract auditable if that constructor changes later.
    _set_kernel_center(branch, "conv_RR", 0.0)
    _set_kernel_center(branch, "conv_RI", 0.0)


# Descriptive alias used by the initialization audit/tests.
_set_cross_filter_centers_zero = _set_cross_center_zero


def _model_weight_norm(model) -> float:
    if hasattr(model, "weights_norm"):
        return float(model.weights_norm())
    total = 0.0
    for branch_name in ("wxx", "wxy", "wyx", "wyy"):
        branch = getattr(model, branch_name)
        for kernel_name in ("conv_RR", "conv_RI"):
            weight = getattr(branch, kernel_name).weight
            if hasattr(weight, "detach"):
                values = weight.detach().cpu().numpy()
            else:
                values = np.asarray(weight)
            total += float(np.sum(np.asarray(values, dtype=float) ** 2))
    return float(np.sqrt(total))


def _init_summary(model, variant: str) -> dict:
    filters = {}
    for name in ("wxx", "wxy", "wyx", "wyy"):
        branch = getattr(model, name)
        filters[name] = {
            "conv_RR": {"center_real": _conv_center_real(branch)},
            "conv_RI": {"center_real": _conv_center_imag(branch)},
        }
    actual_norm = _model_weight_norm(model)
    return {
        "variant": variant,
        "wxx_center_real": _conv_center_real(model.wxx),
        "wxx_center_imag": _conv_center_imag(model.wxx),
        "wxy_center_real": _conv_center_real(model.wxy),
        "wxy_center_imag": _conv_center_imag(model.wxy),
        "wyx_center_real": _conv_center_real(model.wyx),
        "wyx_center_imag": _conv_center_imag(model.wyx),
        "wyy_center_real": _conv_center_real(model.wyy),
        "wyy_center_imag": _conv_center_imag(model.wyy),
        "actual_init_weight_norm": actual_norm,
        "total_l2_norm": actual_norm,
        "filters": filters,
    }


def _make_ml_trial(seed: int, variant: str, n_tap: int = N_TAP, **ml_kwargs):
    if variant not in {"ML-original", "ML-aligned"}:
        raise ValueError("variant must be ML-original or ML-aligned")
    ml = MLChannelEqualizer(n_tap=n_tap, **ml_kwargs)
    if variant == "ML-aligned":
        _set_cross_center_zero(ml.model.wxy)
        _set_cross_center_zero(ml.model.wyx)
    return {
        "seed": int(seed),
        "variant": variant,
        "equalizer": ml,
        "init_summary": _init_summary(ml.model, variant),
    }


def _run_ml_variant(seed: int, variant: str, r_x, r_y, s_x, s_y, **ml_kwargs):
    if not ml_kwargs:
        ml_kwargs = dict(ML_CONFIG)
    else:
        config = dict(ML_CONFIG)
        config.update(ml_kwargs)
        ml_kwargs = config
    seed_ml(seed)
    trial = _make_ml_trial(seed=seed, variant=variant, **ml_kwargs)
    equalizer = trial["equalizer"]
    n_train = int(len(r_x) * ML_TRAIN_FRACTION)
    train_summary = equalizer.train(
        r_x[:n_train],
        r_y[:n_train],
        s_x[:n_train],
        s_y[:n_train],
        val_split=0.2,
        verbose=False,
    )
    result = equalizer.equalize(r_x, r_y)
    return {
        "variant": variant,
        "zX": np.asarray(result["zX"]).flatten(),
        "zY": np.asarray(result["zY"]).flatten(),
        "diverged": bool(result["diverged"]),
        "n_train": int(n_train),
        "init_summary": trial["init_summary"],
        "train_summary": {
            "epochs_run": int(train_summary["epochs_run"]),
            "best_val_loss": float(train_summary["best_val_loss"]),
            "converged": bool(train_summary["converged"]),
        },
        "device_requested": str(ml_kwargs.get("device", "cuda")),
        "device_actual": str(equalizer.device),
        "device": {
            "requested": str(ml_kwargs.get("device", "cuda")),
            "actual": str(equalizer.device),
        },
        "final_weight_norm": float(result["w_norm"]),
        "max_z_amp": float(result["max_z_amp"]),
        "execution": {"constructed": True, "trained": True, "inferred": True},
    }


def _annotate_trial(trial: dict) -> dict:
    trial = copy.deepcopy(trial)
    methods = trial["methods"]
    oracle_pi = float(methods["oracle"]["permutation_invariant_ber"]["mean"])
    for name, metrics in methods.items():
        if name == "oracle":
            continue
        pi = float(metrics["permutation_invariant_ber"]["mean"])
        metrics["excess_pi_ber_vs_oracle"] = pi - oracle_pi
        metrics["descriptive_swap_quality"] = {
            "pi_ber_le_0.05": _swap_quality_label(metrics, threshold=0.05, inclusive=True),
            "pi_ber_lt_0.01": _swap_quality_label(metrics, threshold=0.01, inclusive=False),
        }
    return trial


def _swap_quality_label(metrics: dict, threshold: float, inclusive: bool) -> str:
    """Return the Q1 descriptive swap label at one frozen PI-BER threshold."""
    pi = float(metrics["permutation_invariant_ber"]["mean"])
    fixed = float(metrics["fixed_label_ber"]["mean"])
    assignment = metrics["permutation_invariant_ber"].get("assignment")
    is_swap = assignment == ["sY", "sX"] and pi <= 0.2 and fixed - pi >= 0.05
    if not is_swap:
        return str(metrics.get("classification", "mixed"))
    clean = pi <= threshold if inclusive else pi < threshold
    return "clean-swap" if clean else "degraded-swap"


def _validate_metric_schema(trials: list[dict]):
    expected_methods = set(METHOD_ORDER)
    expected_late_slice = [int(LATE_START), int(LATE_END)]
    for row in trials:
        seed = int(row["seed"])
        if int(row.get("shared_realization_seed", -1)) != seed:
            raise ValueError(f"trial {seed} shared realization seed mismatch")
        if row.get("late_slice") != expected_late_slice:
            raise ValueError(f"trial {seed} late slice mismatch")
        elapsed = float(row.get("elapsed_s", float("nan")))
        if not np.isfinite(elapsed) or elapsed <= 0:
            raise ValueError(f"trial {seed} elapsed_s must be finite and positive")
        methods = row.get("methods")
        if not isinstance(methods, dict) or set(methods) != expected_methods:
            raise ValueError(f"trial {seed} method schema mismatch")
        try:
            oracle_pi = float(methods["oracle"]["permutation_invariant_ber"]["mean"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"trial {seed} metric schema is incomplete") from exc
        if not np.isfinite(oracle_pi):
            raise ValueError(f"trial {seed} oracle PI-BER is nonfinite")
        for name in METHOD_ORDER:
            metrics = methods[name]
            try:
                pi = float(metrics["permutation_invariant_ber"]["mean"])
                fixed = float(metrics["fixed_label_ber"]["mean"])
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"trial {seed} {name} metric schema is incomplete") from exc
            if not np.all(np.isfinite([pi, fixed])):
                raise ValueError(f"trial {seed} {name} raw BER is nonfinite")
            if name != "oracle":
                excess = float(metrics["excess_pi_ber_vs_oracle"])
                if not np.isfinite(excess) or not np.isclose(excess, pi - oracle_pi, atol=1e-12, rtol=0):
                    raise ValueError(f"trial {seed} {name} oracle excess is inconsistent")


def _validate_seed_set(trials: Iterable[dict]):
    seeds = [int(row["seed"]) for row in trials]
    if len(seeds) != 30:
        raise ValueError("expected exactly 30 seeds")
    if len(set(seeds)) != len(seeds):
        raise ValueError("seed schedule must contain unique seeds without duplicate entries")
    expected = set(EXPECTED_SEEDS)
    actual = set(seeds)
    if actual != expected:
        if actual - expected:
            raise ValueError("seed schedule contains seeds outside the allowed range 1000-1029")
        raise ValueError("seed schedule is missing one or more required seeds 1000-1029")
    return sorted(seeds)


def _paired_wilcoxon(values_a: list[float], values_b: list[float]) -> dict:
    diffs = np.asarray(values_a, dtype=float) - np.asarray(values_b, dtype=float)
    wins_a = int(np.sum(diffs < 0))
    wins_b = int(np.sum(diffs > 0))
    ties = int(np.sum(diffs == 0))
    effective = diffs[diffs != 0]
    if len(effective) == 0:
        statistic = 0.0
        pvalue = 1.0
        method = "exact"
    else:
        result = wilcoxon(
            diffs,
            alternative="two-sided",
            zero_method="wilcox",
            correction=False,
            method="exact",
            nan_policy="raise",
        )
        statistic = float(result.statistic)
        pvalue = float(result.pvalue)
        method = "exact"
    return {
        "method": method,
        "statistic": statistic,
        "pvalue": pvalue,
        "effective_n": int(len(effective)),
        "wins_first": wins_a,
        "wins_second": wins_b,
        "ties": ties,
        "differences": diffs.tolist(),
    }


def _method_values(trials: list[dict], method: str) -> list[float]:
    return [
        float(row["methods"][method]["excess_pi_ber_vs_oracle"])
        for row in sorted(trials, key=lambda item: int(item["seed"]))
    ]


def _summarize_trials(trials: list[dict]) -> dict:
    ordered_seeds = _validate_seed_set(trials)
    trials = sorted(trials, key=lambda row: int(row["seed"]))
    _validate_metric_schema(trials)
    pairwise = {}
    for first, second in PAIRWISE_PREDECLARED:
        comparison = _paired_wilcoxon(
            _method_values(trials, first), _method_values(trials, second)
        )
        comparison["gate"] = {
            "pvalue_lt_0_05": bool(comparison["pvalue"] < 0.05),
            "p_lt_0_05": bool(comparison["pvalue"] < 0.05),
            "ml_wins_at_least_25_of_30": bool(comparison["wins_second"] >= 25),
            "passes_primary_gate": bool(comparison["pvalue"] < 0.05 and comparison["wins_second"] >= 25),
            "pass": bool(comparison["pvalue"] < 0.05 and comparison["wins_second"] >= 25),
            "first_method": first,
            "second_method_ml": second,
            "is_primary": (first, second) in PAIRWISE_PREDECLARED[:2],
        }
        pairwise[f"{first}_vs_{second}"] = comparison
    descriptive = {}
    for first, second in DESCRIPTIVE_ONLY:
        descriptive[f"{first}_vs_{second}"] = _paired_wilcoxon(
            _method_values(trials, first), _method_values(trials, second)
        )
    pair_1 = pairwise["standard-CMA_vs_ML-original"]["gate"]["pass"]
    pair_2 = pairwise["standard-CMA_vs_ML-aligned"]["gate"]["pass"]
    if pair_1 and pair_2:
        interpretive_status = "GO"
    elif pair_1 and not pair_2:
        interpretive_status = "INTERMEDIATE"
    else:
        interpretive_status = "NO-GO"
    overall_gate = {
        "required_pair_keys": [
            "standard-CMA_vs_ML-original",
            "standard-CMA_vs_ML-aligned",
        ],
        "passes": bool(pair_1 and pair_2),
        "status": "GO" if pair_1 and pair_2 else "NO-GO",
        "classification_is_descriptive_only": True,
    }
    return {
        "n_trials": len(trials),
        "seeds": ordered_seeds,
        "paired_comparisons": pairwise,
        "descriptive_only": descriptive,
        "preregistered_test": "two-sided exact Wilcoxon on excess_pi_ber_vs_oracle",
        "preregistered_gate": {
            "criterion": "both standard-CMA comparisons require p<0.05 and ML wins >=25/30",
            "go": bool(pair_1 and pair_2),
            "interpretive_status": interpretive_status,
        },
        "overall_gate": overall_gate,
    }


def _seed_list(seeds: Iterable[int] | None) -> list[int]:
    if seeds is None:
        return list(EXPECTED_SEEDS)
    parsed = sorted(int(seed) for seed in seeds)
    if len(set(parsed)) != len(parsed):
        raise ValueError("requested seeds contain duplicate values")
    if any(seed < 1000 or seed > 1029 for seed in parsed):
        raise ValueError("requested seeds must stay within 1000-1029")
    return parsed


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_sha256s():
    paths = {
        "prompt015_unified_baseline.py": Path(__file__),
        "prompt012_longseq_audit.py": Path(__file__).with_name("prompt012_longseq_audit.py"),
        "prompt013_swap_mechanism_q2.py": Path(__file__).with_name("prompt013_swap_mechanism_q2.py"),
        "ml_long_seq_failure.py": Path(__file__).with_name("ml_long_seq_failure.py"),
        "common/_ml_equalizer.py": SIM_DIR / "common" / "_ml_equalizer.py",
        "common/_experiment.py": SIM_DIR / "common" / "_experiment.py",
        "common/_config.py": SIM_DIR / "common" / "_config.py",
        "common/_gg_time.py": SIM_DIR / "common" / "_gg_time.py",
        "common/_equalizer.py": SIM_DIR / "common" / "_equalizer.py",
        "params.py": SIM_DIR / "params.py",
    }
    return {name: _sha256(path) for name, path in paths.items()}


def _experiment_signature(requested_seeds: list[int]) -> dict:
    return {
        "experiment": "PROMPT-015 unified legal baseline",
        "requested_seeds": list(requested_seeds),
        "N": int(N_SYMBOLS),
        "n_symbols": int(N_SYMBOLS),
        "late_slice": [int(LATE_START), int(LATE_END)],
        "evaluation_slice_semantics": "Q1 test-late = final quarter of full sequence",
        "turbulence": TURBULENCE,
        "f_G": float(F_G),
        "modulation": "QPSK",
        "T_S": float(T_S),
        "block": int(BLOCK),
        "sop_rate": float(SOP_RATE),
        "gamma_bar": float(GAMMA_BAR),
        "cma_mu": float(MU_SAFE),
        "cma_n_tap": int(N_TAP),
        "cma_r2": float(R2_QPSK),
        "cma_block_size": 64,
        "ml": dict(ML_CONFIG),
        "ml_n_tap": int(ML_CONFIG["n_tap"]),
        "ml_lr": float(ML_CONFIG["lr"]),
        "ml_batch_size": int(ML_CONFIG["batch_size"]),
        "ml_n_epochs": int(ML_CONFIG["n_epochs"]),
        "ml_patience": int(ML_CONFIG["patience"]),
        "ml_device_requested": str(ML_CONFIG["device"]),
        "ml_train_fraction": float(ML_TRAIN_FRACTION),
        "methods": list(METHOD_ORDER),
    }


def _method_metric(z_x, z_y, s_x, s_y, diverged: bool) -> dict:
    return evaluate_outputs(z_x, z_y, s_x, s_y, diverged)


def _ml_artifact(result: dict) -> dict:
    device = result.get("device")
    if not isinstance(device, dict):
        device = {
            "requested": str(result.get("device_requested", ML_CONFIG["device"])),
            "actual": str(result.get("device_actual", "unknown")),
        }
    execution = result.get("execution")
    if not isinstance(execution, dict):
        execution = {"constructed": True, "trained": True, "inferred": True}
    return {
        "n_train": int(result["n_train"]),
        "init_summary": result["init_summary"],
        "device": device,
        "execution": execution,
        "train_summary": result.get("train_summary", {}),
        "final_weight_norm": result.get("final_weight_norm"),
        "max_z_amp": result.get("max_z_amp"),
    }


def _run_single_seed(seed: int, output_path: str | Path | None = None) -> dict:
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    shared = gen_channel(N_SYMBOLS, alpha, beta, F_G, SOP_RATE, int(seed))
    r_x, r_y, s_x, s_y, h, theta = shared
    late = slice(LATE_START, LATE_END)
    source_x = s_x[late]
    source_y = s_y[late]

    current = run_cma_diagnostic(r_x, r_y, mode="current")
    standard = run_cma_diagnostic(r_x, r_y, mode="standard")
    oracle_x, oracle_y = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)

    ml_original = _run_ml_variant(seed=seed, variant="ML-original", r_x=r_x, r_y=r_y, s_x=s_x, s_y=s_y)
    ml_aligned = _run_ml_variant(seed=seed, variant="ML-aligned", r_x=r_x, r_y=r_y, s_x=s_x, s_y=s_y)

    trial = {
        "seed": int(seed),
        "shared_realization_seed": int(seed),
        "late_slice": [LATE_START, LATE_END],
        "elapsed_s": time.time() - started,
        "methods": {
            "current-CMA": _method_metric(
                current["online"]["zX"], current["online"]["zY"], source_x, source_y, False
            ),
            "standard-CMA": _method_metric(
                standard["online"]["zX"], standard["online"]["zY"], source_x, source_y, False
            ),
            "ML-original": _method_metric(
                ml_original["zX"][late], ml_original["zY"][late], source_x, source_y,
                ml_diverged(ml_original, ml_original["zX"], ml_original["zY"]),
            ),
            "ML-aligned": _method_metric(
                ml_aligned["zX"][late], ml_aligned["zY"][late], source_x, source_y,
                ml_diverged(ml_aligned, ml_aligned["zX"], ml_aligned["zY"]),
            ),
            "oracle": _method_metric(
                oracle_x[late], oracle_y[late], source_x, source_y, False
            ),
        },
        "artifacts": {
            "ML-original": _ml_artifact(ml_original),
            "ML-aligned": _ml_artifact(ml_aligned),
        },
    }
    trial = _annotate_trial(trial)
    for name in trial["methods"]:
        trial["methods"][name]["shared_realization_seed"] = int(seed)
    return trial


def _checkpoint_payload(
    requested_seeds: list[int],
    completed_trials: list[dict],
    output_path: Path,
    dry_run: bool,
) -> dict:
    completed = sorted(int(row["seed"]) for row in completed_trials)
    pending = [seed for seed in requested_seeds if seed not in completed]
    payload = {
        "experiment": "PROMPT-015 unified legal baseline",
        "checkpoint": {
            "requested_seeds": requested_seeds,
            "completed_seeds": completed,
            "pending_seeds": pending,
            "complete": len(pending) == 0 and requested_seeds == list(EXPECTED_SEEDS),
            "dry_run": bool(dry_run),
            "output_path": str(output_path),
        },
        "trials": completed_trials,
    }
    if payload["checkpoint"]["complete"]:
        payload["summary"] = _summarize_trials(completed_trials)
    return payload


def _save_payload_atomic(payload: dict, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=output_path.parent,
    )
    os.close(descriptor)
    temp_path = Path(temp_name)
    try:
        save_results(payload, str(temp_path), "prompt015_unified_baseline")
        os.replace(temp_path, output_path)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _empty_payload(requested_seeds: list[int], output_path: Path, dry_run: bool, *, signature=None, sha_map=None):
    return {
        "experiment": "PROMPT-015 unified legal baseline",
        "experiment_signature": signature if signature is not None else _experiment_signature(requested_seeds),
        "source_sha256": sha_map if sha_map is not None else source_sha256s(),
        "checkpoint": {
            "requested_seeds": list(requested_seeds),
            "completed_seeds": [],
            "pending_seeds": list(requested_seeds),
            "complete": False,
            "dry_run": bool(dry_run),
            "output_path": str(output_path),
        },
        "trials": [],
    }


def _load_checkpoint(output_path: Path, expected_signature: dict, expected_sha: dict):
    if not output_path.exists():
        return None
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    if payload.get("experiment_signature") != expected_signature:
        raise ValueError("checkpoint experiment signature mismatch")
    if payload.get("source_sha256") != expected_sha:
        raise ValueError("checkpoint source SHA mismatch")
    trials = payload.get("trials", [])
    trial_seeds = [int(row["seed"]) for row in trials]
    requested = [int(seed) for seed in payload.get("checkpoint", {}).get("requested_seeds", [])]
    expected_requested = [int(seed) for seed in expected_signature.get("requested_seeds", [])]
    if requested != expected_requested:
        raise ValueError("checkpoint requested seed set mismatch")
    if len(trial_seeds) != len(set(trial_seeds)):
        raise ValueError("checkpoint contains duplicate trial seeds")
    if len(requested) != len(set(requested)):
        raise ValueError("checkpoint requested seeds contain duplicates")
    if any(seed < 1000 or seed > 1029 for seed in requested + trial_seeds):
        raise ValueError("checkpoint contains out-of-range seeds")
    if set(trial_seeds) - set(requested):
        raise ValueError("checkpoint trials exceed requested seed set")
    completed_recorded = [
        int(seed) for seed in payload.get("checkpoint", {}).get("completed_seeds", [])
    ]
    pending_recorded = [
        int(seed) for seed in payload.get("checkpoint", {}).get("pending_seeds", [])
    ]
    if completed_recorded != sorted(trial_seeds):
        raise ValueError("checkpoint completed seed list disagrees with trials")
    if pending_recorded != [seed for seed in requested if seed not in set(trial_seeds)]:
        raise ValueError("checkpoint pending seed list disagrees with trials")
    return payload


def _parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", nargs="*", type=int, default=None)
    parser.add_argument("--output", type=str, default=str(RESULT_PATH))
    parser.add_argument("--max-seeds", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    args = _parse_args(argv)
    requested = _seed_list(args.seeds)
    output_path = Path(args.output)
    signature = _experiment_signature(requested)
    sha_map = source_sha256s()

    if args.dry_run:
        payload = _empty_payload(requested, output_path, True, signature=signature, sha_map=sha_map)
        if args.max_seeds is not None:
            if args.max_seeds <= 0:
                raise ValueError("--max-seeds must be positive")
            payload["checkpoint"]["pending_seeds"] = requested[: args.max_seeds]
        _save_payload_atomic(payload, output_path)
        return payload

    checkpoint = _load_checkpoint(output_path, signature, sha_map)
    payload = checkpoint if checkpoint is not None else _empty_payload(
        requested, output_path, False, signature=signature, sha_map=sha_map
    )

    completed = {int(row["seed"]) for row in payload["trials"]}
    pending = [seed for seed in requested if seed not in completed]
    if args.max_seeds is not None:
        if args.max_seeds <= 0:
            raise ValueError("--max-seeds must be positive")
        pending = pending[: args.max_seeds]

    for seed in pending:
        payload["trials"].append(_run_single_seed(seed))
        payload["trials"].sort(key=lambda row: int(row["seed"]))
        payload = _checkpoint_payload(requested, payload["trials"], output_path, dry_run=False)
        payload["experiment"] = "PROMPT-015 unified legal baseline"
        payload["experiment_signature"] = signature
        payload["source_sha256"] = sha_map
        _save_payload_atomic(payload, output_path)

    if not pending and "summary" not in payload:
        payload = _checkpoint_payload(requested, payload["trials"], output_path, dry_run=False)
        payload["experiment"] = "PROMPT-015 unified legal baseline"
        payload["experiment_signature"] = signature
        payload["source_sha256"] = sha_map
    return payload


if __name__ == "__main__":
    main()
