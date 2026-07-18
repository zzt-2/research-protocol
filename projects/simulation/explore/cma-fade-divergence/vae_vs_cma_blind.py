"""PROMPT-014 blind VQ-VAE versus CMA on shared dual-pol realizations.

The VQ-VAE sees only the first-half received samples.  Transmitted symbols are
used only by the explicitly supervised ML reference and by post-hoc metrics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

import numpy as np

# Required by deterministic CUDA matrix products used by the supervised
# reference; set before importing modules that may import torch.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import generate_shared_realization_dp
from common._cma import CMAEqualizer2x2
from common._config import BLOCK
from common._experiment import save_results
from common._vae_equalizer import VQVAEEqualizer2x2
from ml_long_seq_failure import (
    GAMMA_BAR, ML_PARAMS, MU_SAFE, N_TAP, R2_QPSK, SOP_RATE, T_S,
)
from ml_long_seq_failure import oracle_equalize, run_ml_trial
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs, ml_diverged, seed_ml


N_SYMBOLS = 2_000_000
TURBULENCE = "strong"
SNR_DB = 20.0
DEFAULT_F_G = (30.0, 100.0, 1000.0)
DEFAULT_SEEDS = tuple(range(1000, 1010))
TRAIN_FRACTION = 0.5
VQ_N_TAP = 29
VQ_LR = 0.01
VQ_RHO = 1.0
VQ_BATCH_SIZE = 128
VQ_CHUNK_SIZE = 4096
CMA_BLOCK_SIZE = 64
ML_VAL_SPLIT = 0.2
# The outer 50% training split is split again by the supervised reference:
# 20% validation must contain at least one 1024-symbol chunk.
MIN_N_SYMBOLS = 10_240
METHODS = ("raw_naive", "cma", "vqvae", "ml", "oracle")
RESULT_PATH = SIM_DIR / "results" / "cma-fade-divergence" / "vae_vs_cma_blind.json"


def _component_paths():
    return (
        Path(__file__),
        SIM_DIR / "common" / "_vae_equalizer.py",
        SIM_DIR / "common" / "_dual_pol_channel.py",
        Path(__file__).with_name("prompt012_longseq_audit.py"),
        SIM_DIR / "common" / "_cma.py",
        SIM_DIR / "common" / "_ml_equalizer.py",
        Path(__file__).with_name("ml_long_seq_failure.py"),
    )


def composite_sha256(paths=None):
    """Hash the driver and all channel/equalizer/evaluation dependencies."""
    digest = hashlib.sha256()
    for path in paths or _component_paths():
        path = Path(path)
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _parameters(f_g_values, seeds, n_symbols, device, updates, batch_size, chunk_size):
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    n_train = int(n_symbols * TRAIN_FRACTION)
    actual_updates = int(updates) if updates is not None else math.ceil(n_train / batch_size)
    ml_params = dict(ML_PARAMS)
    ml_params["device"] = device
    ml_signature = dict(ml_params)
    ml_signature["val_split"] = ML_VAL_SPLIT
    return {
        "N": int(n_symbols), "train_fraction": TRAIN_FRACTION,
        "evaluation_slice": [n_train, int(n_symbols)],
        "T_S": T_S, "SOP": SOP_RATE, "f_G": [float(x) for x in f_g_values],
        "seeds": [int(x) for x in seeds], "turbulence": TURBULENCE,
        "alpha": float(alpha), "beta": float(beta), "snr_db": SNR_DB,
        "gamma_bar": GAMMA_BAR, "block": BLOCK, "modulation": "QPSK",
        "dp_method": cfg.gg_time.AR1_METHOD,
        "cma": {"mu": MU_SAFE, "n_tap": N_TAP, "R2": R2_QPSK,
                "block_size": CMA_BLOCK_SIZE},
        "vqvae": {
            "n_tap": VQ_N_TAP, "lr": VQ_LR, "rho": VQ_RHO,
            "batch_size": int(batch_size), "chunk_size": int(chunk_size),
            "updates": actual_updates,
            "updates_source": "explicit" if updates is not None else "ceil(train_symbols/batch_size)",
            "device": str(device), "fixed_codebook": "QPSK",
        },
        "supervised_ml": ml_signature,
        "requested_cells": [
            [float(f_g), int(seed)] for f_g in f_g_values for seed in seeds
        ],
    }


def build_signature(parameters):
    return {"parameters": parameters, "composite_sha256": composite_sha256()}


def validate_checkpoint(checkpoint, requested_signature, expected_script_sha):
    if checkpoint.get("experiment_signature") != requested_signature:
        raise ValueError("checkpoint experiment signature mismatch")
    if checkpoint.get("script_sha256") != expected_script_sha:
        raise ValueError("checkpoint script SHA256 mismatch")


def validate_internal_contract(checkpoint):
    """Reject a checkpoint whose duplicated contract fields disagree."""
    signature = checkpoint.get("experiment_signature")
    if not isinstance(signature, dict):
        raise ValueError("checkpoint internal contract lacks experiment_signature")
    if checkpoint.get("parameters") != signature.get("parameters"):
        raise ValueError("checkpoint internal contract experiment signature parameters mismatch")
    if checkpoint.get("script_sha256") != signature.get("composite_sha256"):
        raise ValueError("checkpoint internal contract script SHA256 mismatch")


def _validate_grid_axes(f_g_values, seeds):
    normalized_f_g = [float(value) for value in f_g_values]
    normalized_seeds = [int(value) for value in seeds]
    if len(set(normalized_f_g)) != len(normalized_f_g):
        raise ValueError("f_g_values contains duplicate values")
    if len(set(normalized_seeds)) != len(normalized_seeds):
        raise ValueError("seeds contains duplicate values")
    return normalized_f_g, normalized_seeds


def _positive_integer(name, value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be a positive integer")
    if int(value) <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _validate_runtime(n_symbols, batch_size, chunk_size, updates=None, max_cells=None):
    _positive_integer("n_symbols", n_symbols)
    if int(n_symbols) < MIN_N_SYMBOLS:
        raise ValueError(
            f"n_symbols must be at least {MIN_N_SYMBOLS} for the ML train/validation split"
        )
    _positive_integer("batch_size", batch_size)
    _positive_integer("chunk_size", chunk_size)
    if updates is not None:
        _positive_integer("updates", updates)
    if max_cells is not None:
        _positive_integer("max_cells", max_cells)


def _select_cells(ordered_grid, cell_indices):
    if cell_indices is None:
        return list(ordered_grid)
    indices = list(cell_indices)
    for index in indices:
        if (isinstance(index, (bool, np.bool_))
                or not isinstance(index, (int, np.integer))):
            raise ValueError("cell_indices must contain integers")
    normalized = [int(index) for index in indices]
    if len(set(normalized)) != len(normalized):
        raise ValueError("cell_indices must not contain duplicates")
    if any(index < 0 or index >= len(ordered_grid) for index in normalized):
        raise ValueError("cell_indices contains an out-of-range index")
    return [ordered_grid[index] for index in normalized]


def _metric(outputs, shared, n_train, diverged=False):
    return evaluate_outputs(
        outputs[0][n_train:], outputs[1][n_train:],
        shared["sX"][n_train:], shared["sY"][n_train:], bool(diverged),
    )


def run_cell(
    f_g, seed, *, n_symbols=N_SYMBOLS, device="cuda", updates=None,
    batch_size=VQ_BATCH_SIZE, chunk_size=VQ_CHUNK_SIZE,
):
    """Run one fair-comparison cell from exactly one channel realization."""
    _validate_runtime(n_symbols, batch_size, chunk_size, updates)
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    shared = generate_shared_realization_dp(
        int(n_symbols), alpha, beta, float(f_g), SOP_RATE, int(seed),
        gamma_bar=GAMMA_BAR, block=BLOCK, t_s=T_S,
        method=cfg.gg_time.AR1_METHOD,
    )
    n_train = int(n_symbols * TRAIN_FRACTION)
    n_updates = int(updates) if updates is not None else math.ceil(n_train / batch_size)

    methods = {
        "raw_naive": _metric((shared["rX"], shared["rY"]), shared, n_train),
    }

    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    cma_result = cma.equalize(
        shared["rX"], shared["rY"], block_size=CMA_BLOCK_SIZE
    )
    methods["cma"] = _metric(
        (cma_result["zX"], cma_result["zY"]), shared, n_train,
        cma_result.get("diverged", False),
    )
    methods["cma"]["diagnostics"] = {
        "diverge_idx": (None if cma_result.get("diverge_idx") is None
                         else int(cma_result["diverge_idx"])),
        "final_w_norm": float(cma_result.get("final_w_norm", float("nan"))),
        "init_w_norm": float(cma_result.get("init_w_norm", float("nan"))),
    }

    vq = VQVAEEqualizer2x2(
        n_tap=VQ_N_TAP, lr=VQ_LR, batch_size=int(batch_size), rho=VQ_RHO,
        device=device, seed=int(seed),
    )
    # Blindness boundary: fit receives received samples only; no s/bits/labels.
    fit = vq.fit(
        shared["rX"][:n_train], shared["rY"][:n_train],
        n_iterations=n_updates, verbose=False,
    )
    vq_result = vq.equalize(shared["rX"], shared["rY"], chunk_size=int(chunk_size))
    methods["vqvae"] = _metric((vq_result["zX"], vq_result["zY"]), shared, n_train)

    losses = fit.get("total_loss", fit.get("loss", []))
    finite = bool(fit.get("finite", False)) and bool(np.isfinite(losses).all())
    loss_decreased = bool(n_updates == 1 or (losses and losses[-1] < losses[0]))
    usage = float(fit.get("usage", fit.get("codebook_usage", {}).get("fraction", 0.0)))
    non_collapse = (
        methods["vqvae"]["classification"] not in {"same-source", "non-swap-collapse"}
        and float(methods["vqvae"].get("abs_corr_zX_zY", 1.0)) < 0.99
    )
    sanity = {
        "finite": finite, "loss_decreased": loss_decreased,
        "usage_gt_half": usage > 0.5, "non_collapse": bool(non_collapse),
    }
    sanity["all"] = all(sanity.values())

    import torch
    old_deterministic = torch.are_deterministic_algorithms_enabled()
    old_warn_only = torch.is_deterministic_algorithms_warn_only_enabled()
    old_cudnn_deterministic = torch.backends.cudnn.deterministic
    old_cudnn_benchmark = torch.backends.cudnn.benchmark
    try:
        seed_ml(seed)
        ml_params = dict(ML_PARAMS)
        ml_params["device"] = device
        z_x_ml, z_y_ml, ml_n_train, ml_result = run_ml_trial(
            shared["rX"], shared["rY"], shared["sX"], shared["sY"],
            ml_params=ml_params,
        )
    finally:
        torch.use_deterministic_algorithms(old_deterministic, warn_only=old_warn_only)
        torch.backends.cudnn.deterministic = old_cudnn_deterministic
        torch.backends.cudnn.benchmark = old_cudnn_benchmark
    if int(ml_n_train) != n_train:
        raise RuntimeError("supervised ML training split differs from frozen 50% split")
    methods["ml"] = _metric(
        (z_x_ml, z_y_ml), shared, n_train, ml_diverged(ml_result, z_x_ml, z_y_ml)
    )

    z_x_or, z_y_or = oracle_equalize(
        shared["rX"], shared["rY"], shared["h"], shared["theta"], GAMMA_BAR
    )
    methods["oracle"] = _metric((z_x_or, z_y_or), shared, n_train)
    return {
        "f_G": float(f_g), "seed": int(seed), "methods": methods,
        "vqvae": {
            "updates": n_updates,
            "updates_source": "explicit" if updates is not None else "ceil(train_symbols/batch_size)",
            "fit": fit, "sanity": sanity,
        },
        "evaluation_slice": [n_train, int(n_symbols)],
        "elapsed_s": time.time() - started,
    }


def summarize_and_gate(trials):
    """Apply the frozen gate only to the exact default 3x10 grid."""
    keys = [(float(t["f_G"]), int(t["seed"])) for t in trials]
    by_key = {key: trial for key, trial in zip(keys, trials)}
    required = {(float(f), int(s)) for f in DEFAULT_F_G for s in DEFAULT_SEEDS}
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    extras = sorted(set(keys) - required)
    if duplicates or extras:
        return {
            "status": "INVALID",
            "duplicate_cells": [list(x) for x in duplicates],
            "extra_cells": [list(x) for x in extras],
            "missing_cells": [list(x) for x in sorted(required - set(keys))],
            "by_f_G": {},
        }
    missing = sorted(required - set(by_key))
    by_f_g = {}
    for f_g in DEFAULT_F_G:
        selected = [by_key[(float(f_g), seed)] for seed in DEFAULT_SEEDS
                    if (float(f_g), seed) in by_key]
        if not selected:
            continue
        vq = [t["methods"]["vqvae"]["permutation_invariant_ber"]["mean"] for t in selected]
        cma = [t["methods"]["cma"]["permutation_invariant_ber"]["mean"] for t in selected]
        by_f_g[f"{f_g:g}"] = {
            "n": len(selected), "vqvae_pi_mean": float(np.mean(vq)),
            "cma_pi_mean": float(np.mean(cma)),
            "paired_wins": int(sum(a < b for a, b in zip(vq, cma))),
        }
    if missing:
        return {"status": "INCOMPLETE", "missing_cells": [list(x) for x in missing],
                "by_f_G": by_f_g}
    failed_sanity = [
        list(key) for key in sorted(required)
        if by_key[key].get("vqvae", {}).get("sanity", {}).get("all") is not True
    ]
    if failed_sanity:
        return {"status": "INVALID", "missing_cells": [], "by_f_G": by_f_g,
                "failed_sanity_cells": failed_sanity}
    passed = all(row["vqvae_pi_mean"] < row["cma_pi_mean"] for row in by_f_g.values())
    return {"status": "PASS" if passed else "FAIL", "missing_cells": [],
            "by_f_G": by_f_g,
            "criterion": "for every f_G, 10-seed mean VQ-VAE PI BER < CMA PI BER"}


def merge_checkpoints(inputs, output):
    """Strictly merge disjoint default-grid checkpoints and save the result."""
    paths = [Path(path) for path in inputs]
    if not paths:
        raise ValueError("merge inputs must contain at least one checkpoint")
    checkpoints = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            checkpoints.append(json.load(handle))

    first = checkpoints[0]
    signature = first.get("experiment_signature")
    script_sha = first.get("script_sha256")
    if not isinstance(signature, dict) or not isinstance(script_sha, str):
        raise ValueError("merge checkpoint is missing signature or SHA")
    validate_checkpoint(first, signature, script_sha)
    expected_cells = [
        [float(f_g), int(seed)] for f_g in DEFAULT_F_G for seed in DEFAULT_SEEDS
    ]
    if first.get("parameters", {}).get("requested_cells") != expected_cells:
        raise ValueError("merge signature requested_cells is not the default 30-cell grid")

    merged = {}
    allowed = {tuple(cell) for cell in expected_cells}
    for checkpoint in checkpoints:
        validate_internal_contract(checkpoint)
        validate_checkpoint(checkpoint, signature, script_sha)
        if checkpoint.get("parameters") != first.get("parameters"):
            raise ValueError("checkpoint parameters differ despite matching signature")
        for trial in checkpoint.get("trials", []):
            key = (float(trial["f_G"]), int(trial["seed"]))
            if key not in allowed:
                raise ValueError(f"merge contains extra cell {key}")
            if key in merged:
                raise ValueError(f"merge contains duplicate cell {key}")
            merged[key] = trial

    trials = [merged[tuple(cell)] for cell in expected_cells if tuple(cell) in merged]
    payload = {
        "experiment": "PROMPT-014 blind VQ-VAE fair comparison (merged)",
        "parameters": first["parameters"],
        "experiment_signature": signature,
        "script_sha256": script_sha,
        "trials": trials,
    }
    payload["gate"] = summarize_and_gate(trials)
    save_results(payload, str(Path(output)), "vae_vs_cma_blind_merge")
    return payload


def run(
    *, f_g_values=DEFAULT_F_G, seeds=DEFAULT_SEEDS, n_symbols=N_SYMBOLS,
    device="cuda", output=RESULT_PATH, updates=None, resume=True,
    batch_size=VQ_BATCH_SIZE, chunk_size=VQ_CHUNK_SIZE, max_cells=None,
    cell_indices=None,
):
    f_g_values, seeds = _validate_grid_axes(f_g_values, seeds)
    _validate_runtime(n_symbols, batch_size, chunk_size, updates, max_cells)
    output = Path(output)
    parameters = _parameters(
        f_g_values, seeds, n_symbols, device, updates, batch_size, chunk_size
    )
    signature = build_signature(parameters)
    script_sha = composite_sha256()
    payload = {
        "experiment": "PROMPT-014 blind VQ-VAE fair comparison",
        "parameters": parameters, "experiment_signature": signature,
        "script_sha256": script_sha, "trials": [],
    }
    if resume and output.exists():
        with output.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_checkpoint(payload, signature, script_sha)

    allowed = {(float(f), int(s)) for f in f_g_values for s in seeds}
    unique = {}
    for trial in payload.get("trials", []):
        key = (float(trial["f_G"]), int(trial["seed"]))
        if key in allowed and key not in unique:
            unique[key] = trial
    payload["trials"] = list(unique.values())

    ordered_grid = [
        (float(f_g), int(seed)) for f_g in f_g_values for seed in seeds
    ]
    selected = _select_cells(ordered_grid, cell_indices)
    pending = [cell for cell in selected if cell not in unique]
    if max_cells is not None:
        pending = pending[:int(max_cells)]
    for f_g, seed in pending:
        trial = run_cell(
            f_g, seed, n_symbols=n_symbols, device=device, updates=updates,
            batch_size=batch_size, chunk_size=chunk_size,
        )
        payload["trials"].append(trial)
        unique[(f_g, seed)] = trial
        payload["gate"] = summarize_and_gate(payload["trials"])
        payload["script_sha256"] = script_sha
        save_results(payload, str(output), "vae_vs_cma_blind")
    payload["gate"] = summarize_and_gate(payload["trials"])
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f-g", type=float, nargs="+", default=list(DEFAULT_F_G))
    parser.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    parser.add_argument("--n-symbols", type=int, default=N_SYMBOLS)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--updates", type=int)
    parser.add_argument("--batch-size", type=int, default=VQ_BATCH_SIZE)
    parser.add_argument("--chunk-size", type=int, default=VQ_CHUNK_SIZE)
    parser.add_argument("--max-cells", type=int)
    parser.add_argument("--cell-indices", type=int, nargs="+")
    parser.add_argument("--merge-inputs", type=Path, nargs="+")
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()
    if args.merge_inputs is not None:
        if args.output is None:
            parser.error("--merge-inputs requires --output")
        merge_checkpoints(args.merge_inputs, args.output)
        return
    run(f_g_values=args.f_g, seeds=args.seeds, n_symbols=args.n_symbols,
        device=args.device, output=args.output or RESULT_PATH, updates=args.updates,
        resume=args.resume, batch_size=args.batch_size, chunk_size=args.chunk_size,
        max_cells=args.max_cells, cell_indices=args.cell_indices)


if __name__ == "__main__":
    main()
