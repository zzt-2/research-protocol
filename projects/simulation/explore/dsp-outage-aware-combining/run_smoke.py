"""Deterministic runner and raw-only analysis for the Q001 defect smoke.

The module is import-safe.  Deployable arms remain in :mod:`smoke_core`; the
truth-aware labels and O1 score are created only while emitting evaluation rows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np

from smoke_core import (
    build_primary_cells,
    combine_subset,
    estimate_branches,
    evaluate_subsets,
    generate_realization,
    payload_ber,
    run_b0,
    run_b1,
    run_b2,
)


B1_THRESHOLDS_DB = (-8, -6, -4, -2, -1, 0, 1, 2, 4, 6)
DEV_SEEDS = tuple(range(20))
TEST_SEEDS = tuple(range(10000, 10100))
PAYLOAD_SYMBOLS = 30720
OUTAGE_BER = 0.02
INVALID_BRANCH_BER = 0.44
BOOTSTRAP_SEED = 20260811
BOOTSTRAP_REPLICATES = 2000

POWER_FEATURES = ("estimated_snr_db",)
MULTI_FEATURES = (
    "estimated_snr_db",
    "sync_margin",
    "log_pilot_ls_residual",
    "pilot_coherence",
    "cpe_increment_rms",
    "cpe_coherence",
)

ALLOWED_TERMINALS = {
    "PROBLEM_ABSENT_OR_TOO_SMALL",
    "PROBLEM_RESOLVED_BY_CONVENTIONAL_RULE",
    "DEFECT_NOT_RECEIVER_OBSERVABLE",
    "DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT",
}
REQUIRED_HASH_KEYS = {
    "design", "implementation_plan", "smoke_core", "run_smoke", "test_smoke",
    "dev_raw", "dev_aggregate",
}
BRANCH_FIELDS = {
    "split", "seed", "cell", "turbulence", "K", "heterogeneity", "receiver_hash",
    "branch_index", "estimated_snr_db", "sync_peak", "sync_margin",
    "pilot_ls_residual", "pilot_coherence", "cpe_increment_rms", "cpe_coherence",
    "offset_match", "individual_ber", "dsp_invalid", "o1_inclusion",
}
METHOD_FIELDS = {
    "split", "seed", "cell", "turbulence", "K", "heterogeneity", "receiver_hash",
    "method", "candidate_parameter", "selected_subset", "no_valid",
    "pre_fec_ber_fixed", "outage", "n_payload_bits",
}


def _jsonable(value):
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value.resolve())
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_sorted_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), allow_nan=False)
    path.write_text(encoded + "\n", encoding="utf-8", newline="\n")


def write_raw_rows(path: Path, rows: Iterable[dict[str, object]]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite raw file: {path}")
    materialized = list(rows)
    if not materialized:
        raise ValueError("raw rows must not be empty")
    fields = sorted({key for row in materialized for key in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise", lineterminator="\n")
        writer.writeheader()
        writer.writerows(materialized)


def _read_raw(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _int(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def _branch_matrix(rows: Sequence[dict[str, object]], feature_names: Sequence[str]) -> np.ndarray:
    matrix = []
    for row in rows:
        values = []
        for name in feature_names:
            if name == "log_pilot_ls_residual":
                values.append(np.log(max(float(row["pilot_ls_residual"]), np.finfo(float).tiny)))
            else:
                values.append(float(row[name]))
        matrix.append(values)
    return np.asarray(matrix, dtype=np.float64)


def _fit_logistic(rows: Sequence[dict[str, object]], feature_names: Sequence[str]) -> dict:
    x = _branch_matrix(rows, feature_names)
    y = np.asarray([int(row["o1_inclusion"]) for row in rows], dtype=np.float64)
    mean = np.mean(x, axis=0)
    scale = np.std(x, axis=0)
    scale[scale < 1e-12] = 1.0
    z = (x - mean) / scale
    design = np.column_stack((np.ones(z.shape[0]), z))
    beta = np.zeros(design.shape[1], dtype=np.float64)
    ridge = np.diag([0.0] + [1e-6] * z.shape[1])
    for _ in range(50):
        linear = np.clip(design @ beta, -30.0, 30.0)
        probability = 1.0 / (1.0 + np.exp(-linear))
        weights = np.maximum(probability * (1.0 - probability), 1e-8)
        hessian = design.T @ (weights[:, None] * design) + ridge
        gradient = design.T @ (y - probability) - ridge @ beta
        step = np.linalg.solve(hessian, gradient)
        beta += step
        if float(np.max(np.abs(step))) < 1e-10:
            break
    return {
        "features": list(feature_names),
        "mean": mean.tolist(),
        "scale": scale.tolist(),
        "intercept": float(beta[0]),
        "coefficients": beta[1:].tolist(),
    }


def _diagnostic_scores(rows: Sequence[dict[str, object]], model: dict) -> np.ndarray:
    x = _branch_matrix(rows, model["features"])
    z = (x - np.asarray(model["mean"])) / np.asarray(model["scale"])
    linear = float(model["intercept"]) + z @ np.asarray(model["coefficients"])
    return 1.0 / (1.0 + np.exp(-np.clip(linear, -30.0, 30.0)))


def rank_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    labels = np.asarray(labels, dtype=np.int8)
    scores = np.asarray(scores, dtype=np.float64)
    positive = int(np.count_nonzero(labels == 1))
    negative = int(np.count_nonzero(labels == 0))
    if positive == 0 or negative == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(scores.size, dtype=np.float64)
    start = 0
    while start < scores.size:
        end = start + 1
        while end < scores.size and scores[order[end]] == scores[order[start]]:
            end += 1
        ranks[order[start:end]] = 0.5 * (start + 1 + end)
        start = end
    rank_sum = float(np.sum(ranks[labels == 1]))
    return (rank_sum - positive * (positive + 1) / 2.0) / (positive * negative)


def _validate_raw_rows(
    rows: Sequence[dict[str, object]], expected_split: str | None,
    validation_mode: str, expected_seeds: Iterable[int] | None = None,
    expected_cells: Iterable[str] | None = None,
) -> None:
    if validation_mode not in {"strict", "unit"}:
        raise ValueError("validation_mode must be strict or unit")
    if not rows:
        raise ValueError("raw rows are empty")
    for row in rows:
        required = BRANCH_FIELDS if row.get("row_type") == "branch" else METHOD_FIELDS if row.get("row_type") == "method" else set()
        if not required or any(key not in row or row[key] == "" for key in required - {"selected_subset"}):
            raise ValueError("raw schema is incomplete")
        if expected_split is not None and row["split"] != expected_split:
            raise ValueError(f"raw split must be {expected_split}")
    branch_keys = [(int(row["seed"]), str(row["cell"]), int(row["branch_index"])) for row in rows if row["row_type"] == "branch"]
    method_keys = [(int(row["seed"]), str(row["cell"]), str(row["method"]), str(row["candidate_parameter"])) for row in rows if row["row_type"] == "method"]
    if len(branch_keys) != len(set(branch_keys)) or len(method_keys) != len(set(method_keys)):
        raise ValueError("duplicate branch/method candidate row")
    split_values = {str(row["split"]) for row in rows}
    structural_split = expected_split if expected_split is not None else (next(iter(split_values)) if len(split_values) == 1 else None)
    pairs = {(int(row["seed"]), str(row["cell"])) for row in rows}
    canonical_cells = {cell.cell_id: cell for cell in build_primary_cells()}
    if validation_mode == "strict" and expected_seeds is not None and expected_cells is not None:
        expected = {(int(seed), str(cell)) for seed in expected_seeds for cell in expected_cells}
        if pairs != expected:
            raise ValueError("raw does not cover exact DEV_SEEDS/TEST_SEEDS x 18 cells")
    for pair in pairs:
        paired = [row for row in rows if (int(row["seed"]), str(row["cell"])) == pair]
        cell = canonical_cells.get(pair[1])
        if cell is None or any(
            str(row["turbulence"]) != cell.turbulence
            or int(row["K"]) != cell.n_branches
            or str(row["heterogeneity"]) != cell.heterogeneity
            for row in paired
        ):
            raise ValueError("canonical cell identity mismatch")
        hashes = {str(row["receiver_hash"]) for row in paired}
        if len(hashes) != 1:
            raise ValueError("receiver hash mismatch within seed-cell pair")
        metadata_fields = {"gg_alpha", "gg_beta", "branch_snr_db", "parameter_status"}
        if validation_mode == "strict" and any(not metadata_fields <= set(row) for row in paired):
            raise ValueError("frozen cell parameter metadata is missing")
        for row in paired:
            if metadata_fields <= set(row):
                branch_snr = row["branch_snr_db"]
                parsed_snr = json.loads(branch_snr) if isinstance(branch_snr, str) else list(branch_snr)
                if (
                    float(row["gg_alpha"]) != cell.gg_alpha
                    or float(row["gg_beta"]) != cell.gg_beta
                    or tuple(float(value) for value in parsed_snr) != cell.branch_snr_db
                    or str(row["parameter_status"]) != cell.parameter_status
                ):
                    raise ValueError("frozen cell parameter metadata mismatch")
        k_values = {int(row["K"]) for row in paired}
        if len(k_values) != 1:
            raise ValueError("inconsistent K within pair")
        k = next(iter(k_values))
        branches = [row for row in paired if row["row_type"] == "branch"]
        methods = [row for row in paired if row["row_type"] == "method"]
        if {int(row["branch_index"]) for row in branches} != set(range(k)):
            raise ValueError("pair-internal missing branch rows")
        signatures = {(str(row["method"]), str(row["candidate_parameter"])) for row in methods}
        required = {("B0", "all"), ("O1", "oracle")}
        if structural_split == "dev":
            required |= {("B1", str(tau)) for tau in B1_THRESHOLDS_DB}
            required |= {("B2", str(top_l)) for top_l in range(1, k + 1)}
        elif structural_split == "test":
            b1_signatures = {sig for sig in signatures if sig[0] == "B1"}
            b2_signatures = {sig for sig in signatures if sig[0] == "B2"}
            if len(b1_signatures) != 1 or len(b2_signatures) != 1:
                raise ValueError("pair-internal missing test comparator rows")
            required |= b1_signatures | b2_signatures
        if signatures != required or len(signatures) != len(methods):
            raise ValueError("pair-internal missing/duplicate method candidates")


def tune_dev(raw_rows: Sequence[dict[str, object]], validation_mode: str = "strict") -> dict:
    canonical_cell_ids = tuple(cell.cell_id for cell in build_primary_cells())
    _validate_raw_rows(
        raw_rows, "dev", validation_mode,
        DEV_SEEDS if validation_mode == "strict" else None,
        canonical_cell_ids if validation_mode == "strict" else None,
    )
    branches = [row for row in raw_rows if row.get("row_type") == "branch"]
    methods = [row for row in raw_rows if row.get("row_type") == "method"]
    if not branches or not methods:
        raise ValueError("dev tuning requires branch and method rows")

    b1_means = {}
    for tau in B1_THRESHOLDS_DB:
        selected = [row for row in methods if row.get("method") == "B1" and float(row["candidate_parameter"]) == tau]
        if selected:
            b1_means[tau] = float(np.mean([float(row["pre_fec_ber_fixed"]) for row in selected]))
    if not b1_means:
        raise ValueError("dev rows contain no frozen-grid B1 candidates")
    b1_tau = min(B1_THRESHOLDS_DB, key=lambda tau: (b1_means.get(tau, float("inf")), B1_THRESHOLDS_DB.index(tau)))

    top_l_by_k: dict[str, int] = {}
    b2_selected: list[dict[str, object]] = []
    for k in sorted({int(row["K"]) for row in methods if row.get("method") == "B2"}):
        candidates = {}
        for top_l in range(1, k + 1):
            selected = [row for row in methods if row.get("method") == "B2" and int(row["K"]) == k and int(float(row["candidate_parameter"])) == top_l]
            if selected:
                candidates[top_l] = float(np.mean([float(row["pre_fec_ber_fixed"]) for row in selected]))
        if candidates:
            chosen = min(candidates, key=lambda item: (candidates[item], item))
            top_l_by_k[str(k)] = chosen
            b2_selected.extend(row for row in methods if row.get("method") == "B2" and int(row["K"]) == k and int(float(row["candidate_parameter"])) == chosen)
    if not top_l_by_k:
        raise ValueError("dev rows contain no top-L candidates")
    selected_b1 = [row for row in methods if row.get("method") == "B1" and float(row["candidate_parameter"]) == b1_tau]
    family_means = {
        "B1": float(np.mean([float(row["pre_fec_ber_fixed"]) for row in selected_b1])),
        "B2": float(np.mean([float(row["pre_fec_ber_fixed"]) for row in b2_selected])),
    }
    strongest = min(("B1", "B2"), key=lambda family: (family_means[family], ("B1", "B2").index(family)))
    return {
        "b1_tau_db": float(b1_tau),
        "top_l_by_k": top_l_by_k,
        "strongest_cheap": strongest,
        "dev_mean_ber": {"B1": family_means["B1"], "B2": family_means["B2"]},
        "diagnostic_models": {
            "power_only": _fit_logistic(branches, POWER_FEATURES),
            "multi_source": _fit_logistic(branches, MULTI_FEATURES),
        },
    }


def _arm_ber(output, truth, payload_mask) -> float:
    if output.no_valid:
        return 0.5
    return payload_ber(output.combined, truth.payload_bits, payload_mask)


def _realization_rows(split: str, seed: int, cell, frozen: dict | None) -> list[dict[str, object]]:
    frame, truth, digest = generate_realization(seed, cell, payload_symbols=PAYLOAD_SYMBOLS)
    estimates = estimate_branches(frame)
    n_payload_bits = int(np.count_nonzero(frame.payload_mask) * 2)
    common = {
        "split": split, "seed": seed, "cell": cell.cell_id,
        "turbulence": cell.turbulence, "K": cell.n_branches,
        "heterogeneity": cell.heterogeneity, "receiver_hash": digest,
        "gg_alpha": cell.gg_alpha, "gg_beta": cell.gg_beta,
        "branch_snr_db": json.dumps(cell.branch_snr_db, separators=(",", ":")),
        "parameter_status": cell.parameter_status,
    }
    individual_bers = []
    for index, estimate in enumerate(estimates):
        individual_ber = payload_ber(
            combine_subset(estimates, (index,)), truth.payload_bits, frame.payload_mask
        )
        individual_bers.append(individual_ber)

    methods = [("B0", "all", run_b0(estimates))]
    if split == "dev" or frozen is None:
        methods.extend(("B1", str(tau), run_b1(estimates, tau)) for tau in B1_THRESHOLDS_DB)
        methods.extend(("B2", str(top_l), run_b2(estimates, top_l)) for top_l in range(1, cell.n_branches + 1))
    else:
        methods.append(("B1", str(frozen["b1_tau_db"]), run_b1(estimates, frozen["b1_tau_db"])))
        top_l = int(frozen["top_l_by_k"][str(cell.n_branches)])
        methods.append(("B2", str(top_l), run_b2(estimates, top_l)))
    # All deployable outputs exist before the evaluator-only O1 is invoked.
    oracle = evaluate_subsets(estimates, truth, frame.payload_mask)
    methods.append(("O1", "oracle", oracle))
    branch_rows = [{
        **common, "row_type": "branch", "branch_index": index,
        "estimated_snr_db": estimate.estimated_snr_db,
        "sync_peak": estimate.sync_peak, "sync_margin": estimate.sync_margin,
        "pilot_ls_residual": estimate.pilot_ls_residual,
        "pilot_coherence": estimate.pilot_coherence,
        "cpe_increment_rms": estimate.cpe_increment_rms,
        "cpe_coherence": estimate.cpe_coherence,
        "offset_match": int(estimate.estimated_offset == truth.offsets[index]),
        "individual_ber": individual_bers[index],
        "dsp_invalid": int(estimate.estimated_offset != truth.offsets[index] or individual_bers[index] >= INVALID_BRANCH_BER),
        "o1_inclusion": int(index in oracle.subset),
    } for index, estimate in enumerate(estimates)]
    method_rows = []
    for method, parameter, output in methods:
        ber = oracle.ber if method == "O1" else _arm_ber(output, truth, frame.payload_mask)
        method_rows.append({
            **common, "row_type": "method", "method": method,
            "candidate_parameter": parameter,
            "selected_subset": ",".join(str(item) for item in output.subset),
            "no_valid": int(getattr(output, "no_valid", False)),
            "pre_fec_ber_fixed": ber, "outage": int(ber > OUTAGE_BER),
            "n_payload_bits": n_payload_bits,
        })
    return branch_rows + method_rows


def run_split(split: str, seeds: Sequence[int], output_dir: Path, frozen: dict | None) -> None:
    if split not in {"dev", "test"}:
        raise ValueError("split must be dev or test")
    if split == "dev" and not set(seeds) <= set(DEV_SEEDS):
        raise ValueError("dev seed mismatch")
    raw_path = Path(output_dir) / "raw.csv"
    if raw_path.exists():
        raise FileExistsError(f"refusing to overwrite raw file: {raw_path}")
    if split == "test":
        if frozen is None or "freeze_receipt_path" not in frozen:
            raise ValueError("test requires a valid freeze receipt")
        receipt = validate_freeze_receipt(Path(frozen["freeze_receipt_path"]))
        if receipt["test_started"] is not False or not set(seeds) <= set(TEST_SEEDS):
            raise ValueError("test authorization mismatch")
        frozen = receipt["frozen"]
    rows = []
    for seed in seeds:
        for cell in build_primary_cells():
            rows.extend(_realization_rows(split, int(seed), cell, frozen))
    write_raw_rows(raw_path, rows)


def _ci(values: Sequence[float]) -> dict:
    valid = np.asarray([value for value in values if np.isfinite(value)], dtype=float)
    if valid.size == 0:
        return {"low": None, "high": None, "valid_replicates": 0}
    return {
        "low": float(np.quantile(valid, 0.025)),
        "high": float(np.quantile(valid, 0.975)),
        "valid_replicates": int(valid.size),
    }


def _bootstrap(rows: Sequence[dict[str, object]], replicates: int, seed: int, metric: Callable) -> dict:
    seeds = sorted({int(row["seed"]) for row in rows})
    rng = np.random.default_rng(seed)
    by_seed = {value: [row for row in rows if int(row["seed"]) == value] for value in seeds}
    values = []
    for _ in range(replicates):
        sampled = rng.choice(seeds, size=len(seeds), replace=True)
        sample = [
            {**row, "__bootstrap_copy": copy_index}
            for copy_index, value in enumerate(sampled)
            for row in by_seed[int(value)]
        ]
        values.append(metric(sample))
    return _ci(values)


def _method_key(row: dict[str, object]) -> tuple[int, str]:
    return int(row["seed"]), str(row["cell"])


def evaluate_terminal(gates: dict[str, bool]) -> str:
    if not gates["g1"] or not gates["g2"]:
        return "PROBLEM_ABSENT_OR_TOO_SMALL"
    if not gates["g3"]:
        return "PROBLEM_RESOLVED_BY_CONVENTIONAL_RULE"
    if not gates["g4"]:
        return "DEFECT_NOT_RECEIVER_OBSERVABLE"
    return "DEFECT_SMOKE_PASS_WITH_NOVELTY_DEBT"


def aggregate_from_raw(
    path: Path, frozen: dict, bootstrap_replicates: int = BOOTSTRAP_REPLICATES,
    bootstrap_seed: int = BOOTSTRAP_SEED, validation_mode: str = "strict",
) -> dict:
    raw = _read_raw(path)
    if validation_mode == "strict":
        _validate_frozen(frozen)
    _validate_raw_rows(
        raw, "test" if validation_mode == "strict" else None, validation_mode,
        TEST_SEEDS if validation_mode == "strict" else None,
        (cell.cell_id for cell in build_primary_cells()) if validation_mode == "strict" else None,
    )
    branches: list[dict[str, object]] = [dict(row) for row in raw if row["row_type"] == "branch"]
    methods: list[dict[str, object]] = [dict(row) for row in raw if row["row_type"] == "method"]
    hashes_by_pair: dict[tuple[int, str], set[str]] = {}
    for row in raw:
        hashes_by_pair.setdefault(_method_key(row), set()).add(str(row["receiver_hash"]))
    if any(len(hashes) != 1 for hashes in hashes_by_pair.values()):
        raise ValueError("receiver hash mismatch within seed-cell pair")
    tau = float(frozen["b1_tau_db"])
    event_pairs = {
        _method_key(row) for row in branches
        if _int(row, "dsp_invalid") and _float(row, "estimated_snr_db") >= tau
    }
    frame_pairs = {_method_key(row) for row in branches}
    event_rate = len(event_pairs) / max(len(frame_pairs), 1)
    event_cells = sorted({cell for _, cell in event_pairs})

    def event_rate_metric(sample):
        pairs = {(int(row["__bootstrap_copy"]),) + _method_key(row) for row in sample}
        events = {
            (int(row["__bootstrap_copy"]),) + _method_key(row) for row in sample
            if _int(row, "dsp_invalid") and _float(row, "estimated_snr_db") >= tau
        }
        return len(events) / max(len(pairs), 1)

    method_map: dict[tuple[int, str, str], dict[str, object]] = {}
    for row in methods:
        method = str(row["method"])
        include = method in {"B0", "O1"}
        if method == "B1":
            include = float(row["candidate_parameter"]) == tau
        if method == "B2":
            include = int(float(row["candidate_parameter"])) == int(frozen["top_l_by_k"][str(_int(row, "K"))])
        if include:
            method_map[(int(row["seed"]), str(row["cell"]), method)] = row

    cheap = str(frozen["strongest_cheap"])
    all_frames = []
    for seed, cell in sorted(frame_pairs):
        b0 = method_map[(seed, cell, "B0")]
        o1 = method_map[(seed, cell, "O1")]
        cheap_row = method_map[(seed, cell, cheap)]
        all_frames.append({
            "seed": seed, "cell": cell, "event": (seed, cell) in event_pairs,
            "B0": b0, "cheap": cheap_row, "O1": o1,
        })
    paired = [item for item in all_frames if item["event"]]

    def paired_metric(sample, arm, kind):
        sample = [item for item in sample if item["event"]]
        if not sample:
            return float("nan")
        if kind == "outage":
            return float(np.mean([_int(item[arm], "outage") - _int(item["O1"], "outage") for item in sample]))
        values = []
        for item in sample:
            method_ber = _float(item[arm], "pre_fec_ber_fixed")
            oracle_ber = _float(item["O1"], "pre_fec_ber_fixed")
            n_bits = _int(item[arm], "n_payload_bits")
            values.append((method_ber - oracle_ber) / max(method_ber, 1.0 / n_bits))
        return float(np.mean(values))

    def pair_bootstrap(arm, kind, offset):
        return _bootstrap(all_frames, bootstrap_replicates, bootstrap_seed + offset,
                          lambda sample: paired_metric(sample, arm, kind)) if all_frames else _ci([])

    labels = np.asarray([_int(row, "o1_inclusion") for row in branches])
    power_scores = _diagnostic_scores(branches, frozen["diagnostic_models"]["power_only"])
    multi_scores = _diagnostic_scores(branches, frozen["diagnostic_models"]["multi_source"])
    power_auc = rank_auc(labels, power_scores)
    multi_auc = rank_auc(labels, multi_scores)
    auc_delta = multi_auc - power_auc

    def auc_bootstrap(which):
        def metric(sample):
            y = np.asarray([_int(row, "o1_inclusion") for row in sample])
            power = _diagnostic_scores(sample, frozen["diagnostic_models"]["power_only"])
            multi = _diagnostic_scores(sample, frozen["diagnostic_models"]["multi_source"])
            if which == "power":
                return rank_auc(y, power)
            if which == "multi":
                return rank_auc(y, multi)
            return rank_auc(y, multi) - rank_auc(y, power)
        return _bootstrap(branches, bootstrap_replicates, bootstrap_seed + {"power": 5, "multi": 6, "delta": 7}[which], metric)

    g1_ci = _bootstrap(branches, bootstrap_replicates, bootstrap_seed + 1, event_rate_metric)
    def point(arm, kind):
        value = paired_metric(paired, arm, kind)
        return 0.0 if not np.isfinite(value) else value
    b0_regret = point("B0", "regret")
    b0_outage = point("B0", "outage")
    cheap_regret = point("cheap", "regret")
    cheap_outage = point("cheap", "outage")
    g2_regret_ci = pair_bootstrap("B0", "regret", 2)
    g2_outage_ci = pair_bootstrap("B0", "outage", 3)
    g3_regret_ci = pair_bootstrap("cheap", "regret", 4)
    g3_outage_ci = pair_bootstrap("cheap", "outage", 5)
    power_ci, multi_ci, delta_ci = auc_bootstrap("power"), auc_bootstrap("multi"), auc_bootstrap("delta")
    low = lambda ci: float("-inf") if ci["low"] is None else float(ci["low"])
    gates = {
        "g1": event_rate >= 0.10 and len(event_cells) >= 3,
        "g2": (b0_regret >= 0.10 and low(g2_regret_ci) > 0) or (b0_outage >= 0.05 and low(g2_outage_ci) > 0),
        "g3": (cheap_regret >= 0.05 and low(g3_regret_ci) > 0) or (cheap_outage >= 0.02 and low(g3_outage_ci) > 0),
        "g4": multi_auc >= 0.65 and auc_delta >= 0.05 and low(multi_ci) > 0.50 and low(delta_ci) > 0,
    }
    result = {
        "g1": {"event_rate": event_rate, "ci": g1_ci, "event_frames": len(event_pairs), "total_frames": len(frame_pairs), "event_cells": event_cells, "pass": gates["g1"]},
        "g2": {"relative_ber_regret": b0_regret, "regret_ci": g2_regret_ci, "outage_excess": b0_outage, "outage_ci": g2_outage_ci, "pass": gates["g2"]},
        "g3": {"family": cheap, "relative_ber_regret": cheap_regret, "regret_ci": g3_regret_ci, "outage_excess": cheap_outage, "outage_ci": g3_outage_ci, "pass": gates["g3"]},
        "g4": {"multi_source_auc": multi_auc, "multi_ci": multi_ci, "power_only_auc": power_auc, "power_ci": power_ci, "auc_delta": auc_delta, "delta_ci": delta_ci, "pass": gates["g4"]},
        "bootstrap": {"seed": bootstrap_seed, "replicates": bootstrap_replicates, "cluster": "seed"},
        "terminal": evaluate_terminal(gates),
    }
    if result["terminal"] not in ALLOWED_TERMINALS:
        raise AssertionError("invalid terminal")
    return _jsonable(result)


def merge_raw(
    parts: Sequence[Path], output: Path, expected_seeds: Iterable[int],
    expected_cells: Iterable[str], validation_mode: str = "strict",
) -> None:
    all_rows: list[dict[str, str]] = []
    seen_pairs: set[tuple[int, str]] = set()
    for part in parts:
        rows = _read_raw(part)
        split_values = {row["split"] for row in rows}
        if len(split_values) != 1:
            raise ValueError("mixed split within raw part")
        _validate_raw_rows(rows, next(iter(split_values)), validation_mode)
        part_pairs = {(int(row["seed"]), row["cell"]) for row in rows}
        if seen_pairs & part_pairs:
            raise ValueError("duplicate seed-cell pair across raw parts")
        seen_pairs |= part_pairs
        all_rows.extend(rows)
    expected = {(int(seed), str(cell)) for seed in expected_seeds for cell in expected_cells}
    if seen_pairs != expected:
        missing = sorted(expected - seen_pairs)
        extra = sorted(seen_pairs - expected)
        raise ValueError(f"missing/extra seed-cell pairs: missing={missing}, extra={extra}")
    all_rows.sort(key=lambda row: (
        int(row["seed"]), row["cell"], row["row_type"],
        int(float(row.get("branch_index") or -1)), row.get("method", ""),
        row.get("candidate_parameter", ""),
    ))
    write_raw_rows(output, all_rows)


def _canonical_contract(bootstrap_replicates: int) -> dict:
    return {
        "payload_symbols": PAYLOAD_SYMBOLS,
        "dev_seeds": list(DEV_SEEDS),
        "test_seeds": list(TEST_SEEDS),
        "b1_thresholds_db": list(B1_THRESHOLDS_DB),
        "b2_top_l_by_k_candidates": {"2": [1, 2], "4": [1, 2, 3, 4]},
        "cells": [_jsonable(cell.__dict__) | {"cell_id": cell.cell_id} for cell in build_primary_cells()],
        "bootstrap": {"seed": BOOTSTRAP_SEED, "replicates": int(bootstrap_replicates), "cluster": "seed"},
        "metrics": {
            "ber": "payload bit errors / fixed non-pilot payload-bit denominator; no dropped trials; pi/2 scoring",
            "outage": "pre_fec_ber_fixed > 0.02",
            "invalid": "estimated offset mismatch OR individual branch BER >= 0.44",
            "relative_regret": "(BER_method-BER_O1)/max(BER_method,1/N_payload_bits)",
        },
        "gates": {
            "G1": {"event_rate": 0.10, "minimum_cells": 3},
            "G2": {"relative_ber_regret": 0.10, "outage_excess": 0.05, "ci_low": 0.0},
            "G3": {"relative_ber_regret": 0.05, "outage_excess": 0.02, "ci_low": 0.0},
            "G4": {"multi_auc": 0.65, "auc_delta": 0.05, "auc_ci_low": 0.50, "delta_ci_low": 0.0},
        },
        "parameter_limitations": [
            "Gamma-Gamma triples conflict with older formulas-master and remain UNVERIFIED_RANGE",
            "K=4 heterogeneity replication remains UNVERIFIED_RANGE",
            "integer offset 0..7 is an MVE search-window range",
            "single-polarization QPSK and hybrid periodic pilots are MVE proxies, not Wang reproduction",
        ],
    }


def write_freeze_receipt(
    path: Path, source_paths: dict[str, Path], dev_raw_path: Path,
    dev_aggregate_path: Path, frozen: dict, bootstrap_replicates: int = BOOTSTRAP_REPLICATES,
) -> dict:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite freeze receipt: {path}")
    hash_paths = {**source_paths, "dev_raw": dev_raw_path, "dev_aggregate": dev_aggregate_path}
    if set(hash_paths) != REQUIRED_HASH_KEYS or any(not Path(item).is_file() for item in hash_paths.values()):
        raise ValueError("freeze hash manifest must contain every required file")
    _validate_frozen(frozen)
    receipt = {
        "schema": "q001-defect-smoke-freeze-v1",
        "test_started": False,
        "hashed_files": {name: {"path": str(Path(item).resolve()), "sha256": _sha256(Path(item))} for name, item in sorted(hash_paths.items())},
        "contract": _canonical_contract(bootstrap_replicates),
        "frozen": _jsonable(frozen),
    }
    write_sorted_json(path, receipt)
    return receipt


def validate_freeze_receipt(path: Path) -> dict:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("schema") != "q001-defect-smoke-freeze-v1" or receipt.get("test_started") is not False:
        raise ValueError("invalid or already-started freeze receipt")
    contract = receipt.get("contract")
    if not isinstance(contract, dict) or not isinstance(contract.get("bootstrap"), dict) or "replicates" not in contract["bootstrap"]:
        raise ValueError("freeze config/seed mismatch")
    if contract != _canonical_contract(contract["bootstrap"]["replicates"]):
        raise ValueError("freeze config/seed mismatch")
    manifest = receipt.get("hashed_files")
    if not isinstance(manifest, dict) or set(manifest) != REQUIRED_HASH_KEYS:
        raise ValueError("freeze hash manifest is incomplete")
    for name, entry in manifest.items():
        target = Path(entry["path"])
        if not target.is_file() or _sha256(target) != entry["sha256"]:
            raise ValueError(f"hash mismatch: {name}")
    frozen = receipt.get("frozen", {})
    _validate_frozen(frozen)
    return receipt


def _validate_frozen(frozen: dict) -> None:
    required = {"b1_tau_db", "top_l_by_k", "strongest_cheap", "dev_mean_ber", "diagnostic_models"}
    if not isinstance(frozen, dict) or not required <= set(frozen):
        raise ValueError("frozen configuration is incomplete")
    if float(frozen["b1_tau_db"]) not in B1_THRESHOLDS_DB:
        raise ValueError("frozen B1 threshold is illegal")
    tops = frozen["top_l_by_k"]
    if set(tops) != {"2", "4"} or not (1 <= int(tops["2"]) <= 2 and 1 <= int(tops["4"]) <= 4):
        raise ValueError("frozen top_l_by_k is illegal")
    if frozen["strongest_cheap"] not in {"B1", "B2"}:
        raise ValueError("frozen strongest cheap family is illegal")
    means = frozen["dev_mean_ber"]
    if set(means) != {"B1", "B2"} or not all(np.isfinite(float(value)) for value in means.values()):
        raise ValueError("frozen dev mean BER is incomplete or non-finite")
    for name, features in (("power_only", POWER_FEATURES), ("multi_source", MULTI_FEATURES)):
        model = frozen["diagnostic_models"].get(name, {})
        if model.get("features") != list(features):
            raise ValueError("frozen diagnostic feature schema is illegal")
        values = [model.get("intercept"), *model.get("mean", []), *model.get("scale", []), *model.get("coefficients", [])]
        if len(model.get("mean", [])) != len(features) or len(model.get("scale", [])) != len(features) or len(model.get("coefficients", [])) != len(features) or not all(np.isfinite(float(value)) for value in values):
            raise ValueError("frozen diagnostic model is incomplete or non-finite")


def _main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    aggregate = sub.add_parser("aggregate")
    aggregate.add_argument("raw", type=Path)
    aggregate.add_argument("frozen", type=Path)
    aggregate.add_argument("output", type=Path)
    validate = sub.add_parser("validate-freeze")
    validate.add_argument("receipt", type=Path)
    args = parser.parse_args()
    if args.command == "aggregate":
        frozen = json.loads(args.frozen.read_text(encoding="utf-8"))
        write_sorted_json(args.output, aggregate_from_raw(args.raw, frozen))
    elif args.command == "validate-freeze":
        validate_freeze_receipt(args.receipt)


if __name__ == "__main__":
    _main()
