"""PROMPT-013 Q2: diagnose why CMA swaps are less clean than ML swaps.

The six predeclared trials are run in batches of at most three.  Each trial
uses one shared dual-polarization realization for ML, oracle, the repository's
scalar-error CMA, and a diagnostic standard CMA whose gradient includes z.
The diagnostic CMA is copied here deliberately: Q2 must not change common/.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
from scipy.stats import spearmanr, wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common._config import BLOCK
from common._experiment import save_results
from common._ml_equalizer import ButterflyCNNEqualizer2x2
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
from prompt012_longseq_audit import evaluate_outputs, ml_diverged, seed_ml
from prompt013_swap_quality_q1 import source_sha256s as q1_source_sha256s


N_SYMBOLS = 5_000_000
TURBULENCE = "strong"
LATE_START = 4_375_000
LATE_END = 5_000_000
WINDOW_SIZE = 50_000
HIGH_GAP_SEEDS = (1006, 1017, 1011)
LOW_GAP_SEEDS = (1024, 1028, 1029)
TARGET_SEEDS = HIGH_GAP_SEEDS + LOW_GAP_SEEDS
OUTLIER_SEED = 1004
EXPECTED_Q1_GAPS = {
    1006: 0.0330536,
    1017: 0.0321632,
    1011: 0.0248056,
    1024: 0.0000456,
    1028: 0.0000496,
    1029: 0.0000524,
}

Q1_RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt013_swap_quality.json"
)
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt013_swap_mechanism.json"
)
LOCK_PATH = RESULT_PATH.with_suffix(".lock")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_sha256s(contents=None):
    """Hash all code/data dependencies capable of changing a Q2 trial."""
    if contents is not None:
        return {name: hashlib.sha256(data).hexdigest() for name, data in contents.items()}
    paths = {
        "prompt013_swap_mechanism_q2.py": Path(__file__),
        "prompt013_swap_quality_q1.py": Path(__file__).with_name("prompt013_swap_quality_q1.py"),
        "prompt013_swap_quality.json": Q1_RESULT_PATH,
        "prompt012_longseq_audit.py": Path(__file__).with_name("prompt012_longseq_audit.py"),
        "ml_long_seq_failure.py": Path(__file__).with_name("ml_long_seq_failure.py"),
        "common/_cma.py": SIM_DIR / "common" / "_cma.py",
        "common/_ml_equalizer.py": SIM_DIR / "common" / "_ml_equalizer.py",
        "common/_experiment.py": SIM_DIR / "common" / "_experiment.py",
        "common/_gg_time.py": SIM_DIR / "common" / "_gg_time.py",
        "common/_config.py": SIM_DIR / "common" / "_config.py",
        "common/_equalizer.py": SIM_DIR / "common" / "_equalizer.py",
        "params.py": SIM_DIR / "params.py",
    }
    return {name: _sha256(path) for name, path in paths.items()}


def window_slices(start: int, end: int, size: int):
    if size <= 0 or start >= end:
        raise ValueError("window contract requires size>0 and start<end")
    return [(left, min(left + size, end)) for left in range(start, end, size)]


def _q1_gap(trial):
    methods = trial["methods"]
    return float(methods["current_cma"]["excess_pi_ber_vs_oracle"]) - float(
        methods["ml"]["excess_pi_ber_vs_oracle"]
    )


def validate_q1_gate(payload):
    """Q2 may start only from the complete, provenance-valid Q1 PASS result."""
    trials = payload.get("trials", [])
    summary = payload.get("summary", {})
    if summary.get("q1_gate", {}).get("status") != "pass":
        raise ValueError("Q1 gate must be PASS before Q2")
    seeds = [int(row.get("seed", -1)) for row in trials]
    if len(trials) != 30 or set(seeds) != set(range(1000, 1030)) or len(set(seeds)) != 30:
        raise ValueError("Q1 must contain exactly 30 complete seeds 1000--1029")
    integrity_keys = (
        "duplicate_seeds", "missing_target_seeds", "unexpected_seeds", "nonfinite_pairs"
    )
    integrity = summary.get("integrity")
    if not isinstance(integrity, dict) or any(key not in integrity for key in integrity_keys):
        raise ValueError("Q1 integrity schema missing one or more required fields")
    if any(not isinstance(integrity[key], list) or integrity[key] for key in integrity_keys):
        raise ValueError("Q1 paired-data integrity is not clean")

    recorded_sha = payload.get("source_sha256")
    expected_sha = q1_source_sha256s()
    if not isinstance(recorded_sha, dict) or recorded_sha != expected_sha:
        raise ValueError("Q1 dependency SHA map mismatch")

    by_seed = {int(row["seed"]): row for row in trials}
    cma_pi, ml_pi, gaps = [], [], []
    for seed in range(1000, 1030):
        try:
            methods = by_seed[seed]["methods"]
            oracle_pi = float(methods["oracle"]["permutation_invariant_ber"]["mean"])
            cma_value = float(methods["current_cma"]["permutation_invariant_ber"]["mean"])
            ml_value = float(methods["ml"]["permutation_invariant_ber"]["mean"])
            cma_excess = float(methods["current_cma"]["excess_pi_ber_vs_oracle"])
            ml_excess = float(methods["ml"]["excess_pi_ber_vs_oracle"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Q1 trial {seed} schema is incomplete") from exc
        values = np.asarray([oracle_pi, cma_value, ml_value, cma_excess, ml_excess])
        if not np.all(np.isfinite(values)):
            raise ValueError(f"Q1 trial {seed} contains a nonfinite metric")
        if not np.isclose(cma_excess, cma_value - oracle_pi, rtol=0.0, atol=1e-12):
            raise ValueError(f"Q1 trial {seed} CMA excess is inconsistent")
        if not np.isclose(ml_excess, ml_value - oracle_pi, rtol=0.0, atol=1e-12):
            raise ValueError(f"Q1 trial {seed} ML excess is inconsistent")
        cma_pi.append(cma_value)
        ml_pi.append(ml_value)
        gaps.append(float(np.round(cma_value - ml_value, 12)))

    differences = np.asarray(gaps, dtype=float)
    ml_wins = int(np.sum(differences > 0))
    cma_wins = int(np.sum(differences < 0))
    ties = int(np.sum(differences == 0))
    nonzero = differences != 0
    effective_n = int(np.sum(nonzero))
    absolute = np.abs(differences[nonzero])
    rank_ties = len(np.unique(absolute)) != len(absolute)
    method = "exact" if ties == 0 and not rank_ties else "asymptotic"
    if effective_n == 0:
        statistic, pvalue = 0.0, 1.0
    else:
        result = wilcoxon(
            differences, alternative="two-sided", zero_method="wilcox",
            correction=False, method=method, nan_policy="raise",
        )
        statistic, pvalue = float(result.statistic), float(result.pvalue)
    independent_pass = pvalue < 0.05 and ml_wins >= 25
    if not independent_pass:
        raise ValueError("Q1 independently recomputed gate does not pass")

    comparison = summary.get("paired_comparison")
    if not isinstance(comparison, dict):
        raise ValueError("Q1 summary paired comparison is missing")
    recorded_wilcoxon = comparison.get("wilcoxon", {})
    summary_matches = (
        summary.get("n_trials") == 30
        and summary.get("seeds") == list(range(1000, 1030))
        and comparison.get("ml_wins") == ml_wins
        and comparison.get("cma_wins") == cma_wins
        and comparison.get("ties") == ties
        and np.allclose(comparison.get("differences", []), differences, rtol=0.0, atol=1e-12)
        and recorded_wilcoxon.get("effective_n") == effective_n
        and recorded_wilcoxon.get("method") == method
        and np.isclose(float(recorded_wilcoxon.get("statistic", float("nan"))), statistic)
        and np.isclose(float(recorded_wilcoxon.get("pvalue", float("nan"))), pvalue)
    )
    if not summary_matches:
        raise ValueError("Q1 summary does not match independently recomputed trials")

    ranked_desc = [seed for seed, _ in sorted(zip(range(1000, 1030), gaps), key=lambda item: item[1], reverse=True)]
    ranked_asc = [seed for seed, _ in sorted(zip(range(1000, 1030), gaps), key=lambda item: item[1])]
    if ranked_desc[0] != OUTLIER_SEED or tuple(ranked_desc[1:4]) != HIGH_GAP_SEEDS:
        raise ValueError("Q1 high-gap ranking no longer matches the predeclaration")
    if tuple(ranked_asc[:3]) != LOW_GAP_SEEDS:
        raise ValueError("Q1 low-gap ranking no longer matches the predeclaration")

    selected = []
    for seed in TARGET_SEEDS:
        gap = differences[seed - 1000]
        if not np.isclose(gap, EXPECTED_Q1_GAPS[seed], rtol=0.0, atol=1e-12):
            raise ValueError(f"Q1 selected seed {seed} gap mismatch")
        row = dict(by_seed[seed])
        row["q1_gap_cma_minus_ml"] = gap
        selected.append(row)
    return selected


def validate_batch(seeds):
    values = [int(seed) for seed in seeds]
    if not 1 <= len(values) <= 3:
        raise ValueError("each Q2 batch must contain 1--3 seeds")
    if len(set(values)) != len(values) or not set(values) <= set(TARGET_SEEDS):
        raise ValueError("Q2 batch seeds must be unique members of the fixed six")
    return values


@contextmanager
def exclusive_run_lock(path=LOCK_PATH):
    lock = Path(path)
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(f"PROMPT-013 Q2 is already running: {lock}") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
        yield
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def save_q2_results(payload, path=RESULT_PATH):
    """Use standard metadata in a same-directory temp, then atomic replace."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    temp_path = Path(temp_name)
    try:
        save_results(payload, str(temp_path), "prompt013_swap_mechanism_q2")
        os.replace(temp_path, destination)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def serialize_weights(weights):
    return {
        name: {"real": np.asarray(value).real.tolist(), "imag": np.asarray(value).imag.tolist()}
        for name, value in weights.items()
    }


def deserialize_weights(payload):
    return {
        name: np.asarray(value["real"], dtype=float) + 1j * np.asarray(value["imag"], dtype=float)
        for name, value in payload.items()
    }


def _weights_norm(weights):
    return float(np.sqrt(sum(np.sum(np.abs(value) ** 2) for value in weights.values())))


def _relative_displacement(weights, fork_weights):
    denom = _weights_norm(fork_weights)
    delta = {
        name: np.asarray(weights[name]) - np.asarray(fork_weights[name]) for name in weights
    }
    return _weights_norm(delta) / denom if denom else float("nan")


def _cma_deltas(r_x, r_y, z_x, z_y, r2, mu):
    e_x = r2 - np.abs(z_x) ** 2
    e_y = r2 - np.abs(z_y) ** 2
    scalar = {
        "wxx": mu * np.mean(e_x[:, None] * np.conj(r_x), axis=0),
        "wxy": mu * np.mean(e_x[:, None] * np.conj(r_y), axis=0),
        "wyx": mu * np.mean(e_y[:, None] * np.conj(r_x), axis=0),
        "wyy": mu * np.mean(e_y[:, None] * np.conj(r_y), axis=0),
    }
    # Standard complex CMA for z=w^T r: delta w ∝ (R-|z|²) z r*.
    standard = {
        "wxx": mu * np.mean((e_x * z_x)[:, None] * np.conj(r_x), axis=0),
        "wxy": mu * np.mean((e_x * z_x)[:, None] * np.conj(r_y), axis=0),
        "wyx": mu * np.mean((e_y * z_y)[:, None] * np.conj(r_x), axis=0),
        "wyy": mu * np.mean((e_y * z_y)[:, None] * np.conj(r_y), axis=0),
    }
    return scalar, standard


def run_cma_diagnostic(r_x, r_y, mode="current", mu=MU_SAFE, n_tap=N_TAP,
                       r2=R2_QPSK, block_size=64,
                       late_slice=(LATE_START, LATE_END), fork_at=LATE_START):
    """Local CMA copy with full 4xL fork state and online/frozen branches.

    ``current`` is operation-for-operation identical to common._cma for its
    online branch.  ``standard`` changes only the applied gradient by adding z.
    The fork is placed at the first complete repository-CMA block whose output
    starts at or after ``fork_at``; any earlier late prefix is identical in both
    branches.
    """
    if mode not in {"current", "standard"}:
        raise ValueError("mode must be current or standard")
    r_x = np.asarray(r_x)
    r_y = np.asarray(r_y)
    if len(r_x) != len(r_y):
        raise ValueError("polarizations must have equal length")
    n_total = len(r_x)
    late_start, late_end = map(int, late_slice)
    if not 0 <= late_start < late_end <= n_total:
        raise ValueError("invalid late slice")
    if not late_start <= int(fork_at) <= late_end or (int(fork_at) - late_start) % block_size:
        raise ValueError("fork boundary must be block-aligned relative to the late slice")
    half = n_tap // 2
    center = half
    weights = {name: np.zeros(n_tap, dtype=complex) for name in ("wxx", "wxy", "wyx", "wyy")}
    weights["wxx"][center] = 1.0
    weights["wyy"][center] = 1.0
    init_norm = _weights_norm(weights)
    n_valid = n_total - n_tap + 1
    n_blocks = max(0, n_valid // block_size)
    fork_block = min(n_blocks, max(0, math.ceil((int(fork_at) - half) / block_size)))
    fork_output_start = fork_block * block_size + half

    from numpy.lib.stride_tricks import sliding_window_view
    r_x_win = sliding_window_view(r_x, n_tap)
    r_y_win = sliding_window_view(r_y, n_tap)
    late_n = late_end - late_start
    online_x = np.zeros(late_n, dtype=complex)
    online_y = np.zeros(late_n, dtype=complex)
    frozen_x = np.zeros(late_n, dtype=complex)
    frozen_y = np.zeros(late_n, dtype=complex)
    traces = []
    fork_weights = None
    frozen_weights = None

    def copy_overlap(target_x, target_y, z_x, z_y, output_start):
        output_end = output_start + len(z_x)
        left = max(output_start, late_start)
        right = min(output_end, late_end)
        if left < right:
            src = slice(left - output_start, right - output_start)
            dst = slice(left - late_start, right - late_start)
            target_x[dst] = z_x[src]
            target_y[dst] = z_y[src]

    for block in range(n_blocks):
        start = block * block_size
        end = start + block_size
        output_start = start + half
        x_block = r_x_win[start:end]
        y_block = r_y_win[start:end]

        if block == fork_block:
            fork_weights = {name: value.copy() for name, value in weights.items()}
            frozen_weights = {name: value.copy() for name, value in weights.items()}

        z_x = x_block @ weights["wxx"] + y_block @ weights["wxy"]
        z_y = x_block @ weights["wyx"] + y_block @ weights["wyy"]
        copy_overlap(online_x, online_y, z_x, z_y, output_start)

        scalar_delta, standard_delta = _cma_deltas(x_block, y_block, z_x, z_y, r2, mu)
        applied = scalar_delta if mode == "current" else standard_delta
        if output_start + block_size > late_start:
            if fork_weights is None:
                displacement = 0.0
            else:
                displacement = _relative_displacement(weights, fork_weights)
            traces.append({
                "output_start": int(output_start),
                "output_end": int(output_start + block_size),
                "scalar_error_update_norm": _weights_norm(scalar_delta),
                "standard_with_z_update_norm": _weights_norm(standard_delta),
                "applied_update_norm": _weights_norm(applied),
                "relative_weight_displacement": float(displacement),
            })

        for name in weights:
            weights[name] += applied[name]

        if block < fork_block:
            copy_overlap(frozen_x, frozen_y, z_x, z_y, output_start)
        else:
            fz_x = x_block @ frozen_weights["wxx"] + y_block @ frozen_weights["wxy"]
            fz_y = x_block @ frozen_weights["wyx"] + y_block @ frozen_weights["wyy"]
            copy_overlap(frozen_x, frozen_y, fz_x, fz_y, output_start)

    if fork_weights is None:
        fork_weights = {name: value.copy() for name, value in weights.items()}
        frozen_weights = {name: value.copy() for name, value in weights.items()}
        frozen_x[:] = online_x
        frozen_y[:] = online_y
        fork_output_start = late_end

    return {
        "mode": mode,
        "online": {
            "zX": online_x,
            "zY": online_y,
            "final_weights": serialize_weights(weights),
            "relative_weight_displacement": float(_relative_displacement(weights, fork_weights)),
        },
        "frozen": {
            "zX": frozen_x,
            "zY": frozen_y,
            "final_weights": serialize_weights(frozen_weights),
            "relative_weight_displacement": 0.0,
        },
        "fork": {
            "requested_index": int(fork_at),
            "block_index": int(fork_block),
            "output_start": int(fork_output_start),
            "late_offset": int(max(0, min(late_n, fork_output_start - late_start))),
            "weights": serialize_weights(fork_weights),
            "weight_norm": _weights_norm(fork_weights),
            "complete_block": True,
        },
        "trace": traces,
        "init_weight_norm": init_norm,
    }


def _safe_ratio(numerator, denominator):
    numerator = float(numerator)
    denominator = float(denominator)
    if denominator > 0:
        return numerator / denominator
    return 0.0 if numerator == 0 else float("inf")


def compute_method_metrics(z_x, z_y, s_x, s_y):
    """PI-aware BER, alignment errors, CM cost, and dual-source LS leakage."""
    z = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))
    base = evaluate_outputs(z[0], z[1], sources[0], sources[1], False)
    assignment_indices = [0 if name == "sX" else 1 for name in base["permutation_invariant_ber"]["assignment"]]
    phase_nmse, scalar_nmse, radial, leak_ratios, target_ratios = [], [], [], [], []
    per_output = []
    for index, target_index in enumerate(assignment_indices):
        output = z[index]
        target = sources[target_index]
        other = sources[1 - target_index]
        target_power = float(np.mean(np.abs(target) ** 2))
        cross = np.vdot(output, target)
        phase_scalar = cross / abs(cross) if abs(cross) else 1.0 + 0j
        denom = np.vdot(output, output)
        complex_scalar = cross / denom if abs(denom) else 0.0 + 0j
        p_nmse = float(np.mean(np.abs(phase_scalar * output - target) ** 2) / target_power)
        c_nmse = float(np.mean(np.abs(complex_scalar * output - target) ** 2) / target_power)
        r_error = float(np.mean((np.abs(output) - np.abs(target)) ** 2) / target_power)
        design = np.column_stack([target, other])
        coefficients, *_ = np.linalg.lstsq(design, output, rcond=None)
        target_component = float(abs(coefficients[0]) ** 2 * np.mean(np.abs(target) ** 2))
        leakage_component = float(abs(coefficients[1]) ** 2 * np.mean(np.abs(other) ** 2))
        leak_ratio = _safe_ratio(leakage_component, target_component)
        target_ratio = _safe_ratio(target_component, leakage_component)
        phase_nmse.append(p_nmse)
        scalar_nmse.append(c_nmse)
        radial.append(r_error)
        leak_ratios.append(leak_ratio)
        target_ratios.append(target_ratio)
        per_output.append({
            "output": "zX" if index == 0 else "zY",
            "target": "sX" if target_index == 0 else "sY",
            "phase_only_nmse": p_nmse,
            "complex_scalar_nmse": c_nmse,
            "radial_error": r_error,
            "target_power": target_component,
            "leakage_power": leakage_component,
            "leakage_power_ratio": leak_ratio,
            "target_to_leakage_power_ratio": target_ratio,
        })
    corr = base["abs_corr"]
    return {
        "fixed_label_ber": float(base["fixed_label_ber"]["mean"]),
        "permutation_invariant_ber": float(base["permutation_invariant_ber"]["mean"]),
        "assignment": list(base["permutation_invariant_ber"]["assignment"]),
        "corr": [
            [float(corr["zX_sX"]), float(corr["zX_sY"])],
            [float(corr["zY_sX"]), float(corr["zY_sY"])],
        ],
        "phase_only_nmse": float(np.mean(phase_nmse)),
        "complex_scalar_nmse": float(np.mean(scalar_nmse)),
        "radial_error": float(np.mean(radial)),
        "leakage_power_ratio": float(np.mean(leak_ratios)),
        "target_to_leakage_power_ratio": float(np.mean(target_ratios)),
        "j_cm": float(np.mean(np.concatenate([
            (1.0 - np.abs(z[0]) ** 2) ** 2,
            (1.0 - np.abs(z[1]) ** 2) ** 2,
        ]))),
        "per_output": per_output,
    }


def _metric_with_excess(z_x, z_y, s_x, s_y, oracle_pi):
    metrics = compute_method_metrics(z_x, z_y, s_x, s_y)
    metrics["excess_pi_ber_vs_oracle"] = float(
        metrics["permutation_invariant_ber"] - float(oracle_pi)
    )
    return metrics


def _summarize_outputs(z_x, z_y, s_x, s_y, oracle_x, oracle_y):
    full_oracle = compute_method_metrics(oracle_x, oracle_y, s_x, s_y)
    full = _metric_with_excess(
        z_x, z_y, s_x, s_y, full_oracle["permutation_invariant_ber"]
    )
    windows = []
    for start, end in window_slices(LATE_START, LATE_END, WINDOW_SIZE):
        left, right = start - LATE_START, end - LATE_START
        oracle = compute_method_metrics(
            oracle_x[left:right], oracle_y[left:right], s_x[left:right], s_y[left:right]
        )
        metric = _metric_with_excess(
            z_x[left:right], z_y[left:right], s_x[left:right], s_y[left:right],
            oracle["permutation_invariant_ber"],
        )
        metric.update({"start": start, "end": end})
        windows.append(metric)
    return {"full_late": full, "windows": windows}


def _trace_summary(trace, start=LATE_START, end=LATE_END):
    rows = [row for row in trace if row["output_end"] > start and row["output_start"] < end]
    keys = (
        "scalar_error_update_norm", "standard_with_z_update_norm",
        "applied_update_norm", "relative_weight_displacement",
    )
    if not rows:
        return {key: None for key in keys}
    return {key: float(np.mean([row[key] for row in rows])) for key in keys}


def _safe_spearman(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3 or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        return None
    if np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    value = float(spearmanr(x, y).statistic)
    return value if np.isfinite(value) else None


def _synchrony_state(rho):
    """Three-state oracle synchrony: unknown, asynchronous, or synchronous."""
    if rho is None:
        return None
    try:
        value = float(rho)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(value):
        return None
    return bool(abs(value) >= 0.7)


def capacity_evidence(n_tap=N_TAP):
    """H_c code evidence; record the existing ML cross-init mismatch, do not fix it."""
    import torch.nn as nn
    model = ButterflyCNNEqualizer2x2(n_tap=n_tap)
    center = n_tap // 2
    actual = {
        "wxy": float(model.wxy.conv_RR.weight.detach().cpu().numpy()[0, 0, center]),
        "wyx": float(model.wyx.conv_RR.weight.detach().cpu().numpy()[0, 0, center]),
    }
    ml_parameters = int(sum(parameter.numel() for parameter in model.parameters()))
    has_bias = any(module.bias is not None for module in model.modules() if isinstance(module, nn.Conv1d))
    has_nonlinearity = any(isinstance(module, (nn.ReLU, nn.Sigmoid, nn.Tanh, nn.GELU)) for module in model.modules())
    cma_parameters = 4 * n_tap * 2
    return {
        "four_complex_firs": True,
        "n_tap": int(n_tap),
        "cma_real_parameters": int(cma_parameters),
        "ml_real_parameters": int(ml_parameters),
        "bias": bool(has_bias),
        "nonlinearity": bool(has_nonlinearity),
        "capacity_isomorphic": bool(cma_parameters == ml_parameters and not has_bias and not has_nonlinearity),
        "ml_cross_center_actual": actual,
        "ml_cross_center_comment_claim": 0.0,
        "initialization_mismatch_confound": bool(any(value != 0.0 for value in actual.values())),
        "note": "Existing code initializes wxy/wyx real center to 1 although comments say 0; recorded as confound, not repaired.",
    }


def _median_ratio(high, low):
    if not high or not low:
        return None
    return _safe_ratio(float(np.median(high)), float(np.median(low)))


def evaluate_hypothesis_a(trials):
    if not trials:
        return {"verdict": "unknown", "reason": "no Q2 trials"}
    by_seed = {int(row["seed"]): row for row in trials}
    if not set(TARGET_SEEDS) <= set(by_seed):
        return {"verdict": "unknown", "reason": "incomplete fixed six"}
    variants = {}
    for variant in ("current", "standard"):
        metric_results = {}
        for metric in ("complex_scalar_nmse", "leakage_power_ratio"):
            high_cma = [by_seed[s]["mechanism"][variant]["online"]["full_late"][metric] for s in HIGH_GAP_SEEDS]
            low_cma = [by_seed[s]["mechanism"][variant]["online"]["full_late"][metric] for s in LOW_GAP_SEEDS]
            high_ml = [by_seed[s]["methods"]["ml"]["full_late"][metric] for s in HIGH_GAP_SEEDS]
            per_seed = [_safe_ratio(cma, ml) for cma, ml in zip(high_cma, high_ml)]
            metric_results[metric] = {
                "high_vs_ml_at_least_3x_count": int(sum(value >= 3.0 for value in per_seed)),
                "high_median_vs_low_median_ratio": _median_ratio(high_cma, low_cma),
            }
        j_ratio = _median_ratio(
            [by_seed[s]["mechanism"][variant]["online"]["full_late"]["j_cm"] for s in HIGH_GAP_SEEDS],
            [by_seed[s]["mechanism"][variant]["online"]["full_late"]["j_cm"] for s in LOW_GAP_SEEDS],
        )
        grad_key = "scalar_error_update_norm" if variant == "current" else "standard_with_z_update_norm"
        grad_ratio = _median_ratio(
            [by_seed[s]["mechanism"][variant]["gradient"]["full_late"][grad_key] for s in HIGH_GAP_SEEDS],
            [by_seed[s]["mechanism"][variant]["gradient"]["full_late"][grad_key] for s in LOW_GAP_SEEDS],
        )
        metric_pass = any(
            item["high_vs_ml_at_least_3x_count"] >= 2
            and item["high_median_vs_low_median_ratio"] is not None
            and item["high_median_vs_low_median_ratio"] >= 3.0
            for item in metric_results.values()
        )
        passes = metric_pass and j_ratio is not None and j_ratio <= 1.5 and grad_ratio is not None and grad_ratio <= 1.5
        variants[variant] = {
            "supported": bool(passes),
            "metrics": metric_results,
            "high_vs_low_j_cm_ratio": j_ratio,
            "high_vs_low_cm_gradient_ratio": grad_ratio,
        }
    supported = all(item["supported"] for item in variants.values())
    return {
        "verdict": "supported" if supported else "falsified",
        "variants": variants,
        "direction_consistent": bool(supported),
    }


def evaluate_hypothesis_b(trials):
    if not trials:
        return {"verdict": "unknown", "reason": "no Q2 trials"}
    by_seed = {int(row["seed"]): row for row in trials}
    if not set(TARGET_SEEDS) <= set(by_seed):
        return {"verdict": "unknown", "reason": "incomplete fixed six"}
    variants = {}
    for variant in ("current", "standard"):
        high_support = 0
        rho_support = 0
        high_details = []
        low_changes = []
        try:
            for seed in HIGH_GAP_SEEDS:
                branch = by_seed[seed]["mechanism"][variant]
                online = branch["online"]["full_late"]
                frozen = branch["frozen"]["full_late"]
                required = np.asarray([
                    online["excess_pi_ber_vs_oracle"], frozen["excess_pi_ber_vs_oracle"],
                    online["complex_scalar_nmse"], frozen["complex_scalar_nmse"],
                    online["leakage_power_ratio"], frozen["leakage_power_ratio"],
                    branch["fork"]["spearman_online_displacement_vs_excess"],
                    branch["fork"]["spearman_online_displacement_vs_oracle_pi"],
                ], dtype=float)
                oracle_sync = branch["fork"]["oracle_synchronous"]
                oracle_rho = required[-1]
                if (
                    not np.all(np.isfinite(required))
                    or not isinstance(oracle_sync, bool)
                    or _synchrony_state(oracle_rho) is not oracle_sync
                ):
                    return {
                        "verdict": "unknown",
                        "reason": f"missing/nonfinite H_b metric for {variant} seed {seed}",
                    }
                online_excess, frozen_excess, online_nmse, frozen_nmse, online_leak, frozen_leak, rho, _ = required
                absolute = float(online_excess - frozen_excess)
                fractional = _safe_ratio(absolute, online_excess)
                quality_ratio = max(
                    _safe_ratio(online_nmse, frozen_nmse),
                    _safe_ratio(online_leak, frozen_leak),
                )
                passes = absolute >= 0.01 and fractional >= 0.5 and quality_ratio >= 2.0
                high_support += int(passes)
                rho_support += int(rho >= 0.7 and oracle_sync is False)
                high_details.append({
                    "seed": seed, "absolute_excess_reduction": absolute,
                    "fractional_excess_reduction": fractional,
                    "quality_improvement_ratio": quality_ratio, "supported": passes,
                })
            for seed in LOW_GAP_SEEDS:
                branch = by_seed[seed]["mechanism"][variant]
                online = float(branch["online"]["full_late"]["excess_pi_ber_vs_oracle"])
                frozen = float(branch["frozen"]["full_late"]["excess_pi_ber_vs_oracle"])
                if not np.isfinite(online) or not np.isfinite(frozen):
                    return {
                        "verdict": "unknown",
                        "reason": f"missing/nonfinite H_b metric for {variant} seed {seed}",
                    }
                low_changes.append(abs(online - frozen))
        except (KeyError, TypeError, ValueError, IndexError):
            return {
                "verdict": "unknown",
                "reason": f"missing/nonfinite H_b preregistered metric for {variant}",
            }
        passes = high_support >= 2 and all(value < 0.001 for value in low_changes) and rho_support >= 2
        variants[variant] = {
            "supported": bool(passes),
            "high_support_count": high_support,
            "low_absolute_changes": low_changes,
            "rho_and_oracle_nonsync_count": rho_support,
            "high_details": high_details,
        }
    supported = all(item["supported"] for item in variants.values())
    return {
        "verdict": "supported" if supported else "falsified",
        "variants": variants,
        "direction_consistent": bool(supported),
    }


def _run_methods_on_shared(shared, seed):
    r_x, r_y, s_x, s_y, h, theta = shared
    late = slice(LATE_START, LATE_END)
    seed_ml(seed)
    ml_x, ml_y, n_train, ml_result = run_ml_trial(r_x, r_y, s_x, s_y)
    oracle_x, oracle_y = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)
    current = run_cma_diagnostic(r_x, r_y, mode="current")
    standard = run_cma_diagnostic(r_x, r_y, mode="standard")

    source_x, source_y = s_x[late], s_y[late]
    oracle_late_x, oracle_late_y = oracle_x[late], oracle_y[late]
    methods = {
        "ml": _summarize_outputs(
            ml_x[late], ml_y[late], source_x, source_y, oracle_late_x, oracle_late_y
        ),
        "oracle": _summarize_outputs(
            oracle_late_x, oracle_late_y, source_x, source_y, oracle_late_x, oracle_late_y
        ),
    }
    methods["ml"]["n_train"] = int(n_train)
    methods["ml"]["diverged"] = ml_diverged(ml_result, ml_x, ml_y)

    mechanism = {}
    for variant, raw in (("current", current), ("standard", standard)):
        online = _summarize_outputs(
            raw["online"]["zX"], raw["online"]["zY"], source_x, source_y,
            oracle_late_x, oracle_late_y,
        )
        frozen = _summarize_outputs(
            raw["frozen"]["zX"], raw["frozen"]["zY"], source_x, source_y,
            oracle_late_x, oracle_late_y,
        )
        methods[f"{variant}_cma_online"] = online
        methods[f"{variant}_cma_frozen"] = frozen
        gradient_windows = []
        for start, end in window_slices(LATE_START, LATE_END, WINDOW_SIZE):
            item = _trace_summary(raw["trace"], start, end)
            item.update({"start": start, "end": end})
            gradient_windows.append(item)
        displacement = [row["relative_weight_displacement"] for row in gradient_windows]
        online_excess = [row["excess_pi_ber_vs_oracle"] for row in online["windows"]]
        oracle_pi = [row["permutation_invariant_ber"] for row in methods["oracle"]["windows"]]
        rho = _safe_spearman(displacement, online_excess)
        oracle_rho = _safe_spearman(displacement, oracle_pi)
        mechanism[variant] = {
            "online": online,
            "frozen": frozen,
            "gradient": {
                "full_late": _trace_summary(raw["trace"]),
                "windows": gradient_windows,
            },
            "fork": {
                **raw["fork"],
                "online_final_weights": raw["online"]["final_weights"],
                "frozen_final_weights": raw["frozen"]["final_weights"],
                "online_relative_weight_displacement": raw["online"]["relative_weight_displacement"],
                "frozen_relative_weight_displacement": raw["frozen"]["relative_weight_displacement"],
                "spearman_online_displacement_vs_excess": rho,
                "spearman_online_displacement_vs_oracle_pi": oracle_rho,
                "oracle_synchronous": _synchrony_state(oracle_rho),
            },
        }

    channel_windows = []
    for start, end in window_slices(LATE_START, LATE_END, WINDOW_SIZE):
        hs = np.asarray(h[start:end])
        ts = np.asarray(theta[start:end])
        oracle_metric = methods["oracle"]["windows"][len(channel_windows)]
        channel_windows.append({
            "start": start, "end": end,
            "h": {"mean": float(np.mean(hs)), "std": float(np.std(hs)),
                  "min": float(np.min(hs)), "max": float(np.max(hs))},
            "theta": {"start": float(ts[0]), "end": float(ts[-1]),
                      "span": float(ts[-1] - ts[0])},
            "oracle": oracle_metric,
        })
    return {
        "seed": int(seed),
        "methods": methods,
        "mechanism": mechanism,
        "windows": channel_windows,
    }


def _execute_seed(seed, alpha, beta, generator=None, method_runner=None):
    generator = generator or generate_shared_dual_pol_realization
    method_runner = method_runner or _run_methods_on_shared
    started = time.time()
    shared = generator(N_SYMBOLS, alpha, beta, F_G, SOP_RATE, int(seed))
    trial = method_runner(shared, int(seed))
    trial["seed"] = int(seed)
    trial["shared_realization_seed"] = int(seed)
    trial["q1_group"] = "high-gap" if int(seed) in HIGH_GAP_SEEDS else "low-gap"
    trial["q1_gap_cma_minus_ml"] = EXPECTED_Q1_GAPS[int(seed)]
    trial["elapsed_s"] = time.time() - started
    return trial


def _experiment_signature(alpha, beta, q1_sha):
    return {
        "question": "PROMPT-013 Q2 swap-quality mechanism",
        "N": N_SYMBOLS, "T_S": T_S, "SOP": SOP_RATE, "f_G": F_G,
        "turbulence": TURBULENCE, "alpha": float(alpha), "beta": float(beta),
        "gamma_bar": GAMMA_BAR, "block": BLOCK, "late_slice": [LATE_START, LATE_END],
        "window_size": WINDOW_SIZE, "fork_requested": LATE_START,
        "cma_mu": MU_SAFE, "cma_n_tap": N_TAP, "cma_R2": R2_QPSK,
        "high_gap_seeds": list(HIGH_GAP_SEEDS), "low_gap_seeds": list(LOW_GAP_SEEDS),
        "outlier_record_only": OUTLIER_SEED, "q1_result_sha256": q1_sha,
        "batch_limit": 3,
    }


def _validate_checkpoint(payload, signature, sha_map):
    if payload.get("experiment_signature") != signature:
        raise ValueError("Q2 checkpoint experiment signature mismatch")
    if payload.get("source_sha256") != sha_map:
        raise ValueError("Q2 checkpoint dependency SHA mismatch")
    seeds = [int(row["seed"]) for row in payload.get("trials", [])]
    if len(seeds) != len(set(seeds)) or not set(seeds) <= set(TARGET_SEEDS):
        raise ValueError("Q2 checkpoint seed integrity failure")


def _load_or_initialize():
    q1_payload = json.loads(Q1_RESULT_PATH.read_text(encoding="utf-8"))
    selected = validate_q1_gate(q1_payload)
    q1_sha = _sha256(Q1_RESULT_PATH)
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    signature = _experiment_signature(alpha, beta, q1_sha)
    sha_map = source_sha256s()
    if RESULT_PATH.exists():
        payload = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        _validate_checkpoint(payload, signature, sha_map)
    else:
        payload = {
            "experiment": "PROMPT-013 Q2 swap-quality mechanism",
            "experiment_signature": signature,
            "source_sha256": sha_map,
            "q1_selected_trials": selected,
            "outlier_fact": {
                "seed": OUTLIER_SEED,
                "q1_gap_cma_minus_ml": 0.1745968,
                "action": "record-only; excluded from Q2 by predeclaration",
            },
            "shared_realization_contract": "one generator call per seed, reused by every method",
            "hypothesis_thresholds": {
                "H_a": "2/3 high >=3x ML; high median >=3x low; J_CM and CM-gradient <=1.5x; both CMA modes",
                "H_b": "2/3 high freeze reduction >=50% and >=0.01 plus quality >=2x; low <0.001; 2 rho>=0.7; both modes",
            },
            "h_c_code_evidence": capacity_evidence(),
            "trials": [],
        }
    return payload, alpha, beta


def _update_summary(payload):
    trials = payload.get("trials", [])
    payload["summary"] = {
        "n_trials": len(trials),
        "seeds": sorted(int(row["seed"]) for row in trials),
        "complete": set(int(row["seed"]) for row in trials) == set(TARGET_SEEDS),
        "H_a": evaluate_hypothesis_a(trials),
        "H_b": evaluate_hypothesis_b(trials),
        "H_c": payload.get("h_c_code_evidence", capacity_evidence()),
    }


def pending_seeds(seeds, payload):
    completed = {int(row["seed"]) for row in payload.get("trials", [])}
    return [int(seed) for seed in seeds if int(seed) not in completed]


def _run_batch_locked(seeds):
    payload, alpha, beta = _load_or_initialize()
    for seed in pending_seeds(validate_batch(seeds), payload):
        payload["trials"].append(_execute_seed(seed, alpha, beta))
        payload["trials"].sort(key=lambda row: TARGET_SEEDS.index(int(row["seed"])))
        _update_summary(payload)
        save_q2_results(payload)
        print(f"seed={seed} checkpoint={len(payload['trials'])}/6", flush=True)
    return payload


def run_batch(seeds):
    with exclusive_run_lock(LOCK_PATH):
        return _run_batch_locked(seeds)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    args = parser.parse_args()
    run_batch(args.seeds)


if __name__ == "__main__":
    main()
