"""T010 metric primitives and phase-scoped runner entry point."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import uuid

import numpy as np
from scipy.special import erfcinv
import yaml

SIMULATION_ROOT = Path(__file__).resolve().parents[2]
if str(SIMULATION_ROOT) not in sys.path:
    sys.path.insert(0, str(SIMULATION_ROOT))

from common._experiment import save_results
from common._modulation import qam16_demod


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[4]
SEED_PLAN = {
    "invalid_development": [130001],
    "canonical_only": [130002],
    "source_smoke": [130003],
    "validation": list(range(131001, 131006)),
    "test": list(range(132001, 132011)),
}
SOURCE_SMOKE_CONFIG = {
    "symbol_rate": 28e9,
    "n_symbols": 25_000,
    "esn0_db": 26.0,
    "linewidth_hz": 50e3,
    "cfo_hz": [1e9, 10e9],
    "seed": 130003,
}
SOURCE_SMOKE_FORGETTING_FACTOR = 0.99
SOURCE_SMOKE_FORGETTING_FACTOR_TYPE = (
    "IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN"
)
C2_HASH_PATHS = [
    ".sessions/2026-07-23-research-direction-lab-longitudinal-test/T010-b10-source-native-adaptive-rls-cpr.md",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/source-contract.yaml",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/contract.yaml",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/pilot-manifest.json",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/seed-census.yaml",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/shared_realization.py",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/source_native_rls.py",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/methods.py",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/baselines.py",
    "projects/simulation/explore/b10-source-native-adaptive-rls-cpr/run_all.py",
    "projects/simulation/params.py",
    "projects/simulation/common/_config.py",
    "projects/simulation/common/_modulation.py",
    "projects/simulation/common/_gg_time.py",
    "projects/simulation/common/_channel.py",
    "projects/simulation/common/_recovery.py",
    "projects/simulation/common/_experiment.py",
]


class StaleCheckpointError(RuntimeError):
    """The existing validation checkpoint is not the frozen canonical prefix."""


def c2_setting_grid() -> list[list[dict]]:
    """Return the six preregistered arm-family grids in canonical index order."""
    factors = [0.98, 0.99, 0.999]
    return [
        [{"forgetting_factor": value} for value in factors],
        [
            {"forgetting_factor": factor, "threshold": threshold}
            for factor in factors
            for threshold in [0.05, 0.11, 0.20]
        ],
        [
            {
                "lambda_min": lo,
                "lambda_max": hi,
                "ema_alpha": alpha,
                "innovation_scale": scale,
            }
            for lo, hi, alpha, scale in [
                (0.95, 0.999, 0.20, 2.0),
                (0.98, 0.995, 0.10, 1.0),
                (0.99, 0.999, 0.10, 1.0),
            ]
        ],
        [
            {"forgetting_factor": factor, "threshold": threshold}
            for factor in factors
            for threshold in [0.10, 0.20, 0.40]
        ],
        [{"test_phases": 32, "window": window} for window in [31, 63, 127]],
        [{"omega_n": omega_n} for omega_n in [4e6, 8e6, 20e6]],
    ]


def expected_row_keys() -> list[list[int]]:
    """Build all 2250 integer keys without string or result-dependent sorting."""
    sizes = [len(family) for family in c2_setting_grid()]
    return [
        [gg_index, snr_index, seed_index, arm_index, setting_index]
        for gg_index in range(3)
        for snr_index in range(5)
        for seed_index in range(5)
        for arm_index, size in enumerate(sizes)
        for setting_index in range(size)
    ]


def validate_checkpoint_rows(rows: list[dict]) -> int:
    """Accept only complete 30-row cells forming the exact canonical prefix."""
    if len(rows) % 30:
        raise StaleCheckpointError("checkpoint row count is not a 30-row boundary")
    expected = expected_row_keys()
    keys = [row.get("row_key") for row in rows]
    if len({tuple(key) for key in keys if isinstance(key, list)}) != len(keys):
        raise StaleCheckpointError("checkpoint row keys are missing or duplicated")
    if keys != expected[: len(keys)]:
        raise StaleCheckpointError("checkpoint rows are not the canonical strict prefix")
    return len(rows)


def source_hash_bundle() -> dict[str, str]:
    """Hash the exact 17-file dispatch bundle from original bytes."""
    return {
        path: hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
        for path in C2_HASH_PATHS
    }


def canonical_rows_sha256(rows: list[dict]) -> str:
    raw = json.dumps(
        rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def atomic_save_validation(payload: dict, target: str | Path) -> str:
    """Save through common metadata injection, fsync, then atomic replacement."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    directory_fsync = "SUPPORTED"
    try:
        save_results(payload, str(temp), "t010_b10_c2_validation")
        with temp.open("r+b") as handle:
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, target)
        try:
            descriptor = os.open(str(target.parent), os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        except OSError:
            directory_fsync = "UNSUPPORTED_PLATFORM"
    except Exception:
        if temp.exists():
            temp.unlink()
        raise
    return directory_fsync


def select_bstar(scores: dict[str, tuple]) -> str:
    """Select the conventional arm; exact score ties always resolve to BPS."""
    required = {"4OPM_BPS", "4OPM_CONTINUOUS_DD_DPLL"}
    if set(scores) != required:
        raise ValueError("B* selection requires exactly the frozen BPS and DPLL scores")
    return min(required, key=lambda arm: (tuple(scores[arm]), 0 if arm == "4OPM_BPS" else 1))


def select_primary(scores: dict[str, tuple]) -> str:
    """Select P2/P3 globally; an exact full-score tie resolves to P2."""
    if set(scores) != {"P2", "P3"}:
        raise ValueError("primary selection requires exactly P2 and P3")
    return min(("P2", "P3"), key=lambda arm: (tuple(scores[arm]), 0 if arm == "P2" else 1))


def setting_score(rows: list[dict], setting_index: int) -> tuple[int, int, int, int, int]:
    """Compute the preregistered global validation score for one setting."""
    if not rows:
        raise ValueError("setting score requires validation rows")
    return (
        sum(not bool(row["state_finite"]) for row in rows),
        sum(float(row["ber"]) >= 0.2 for row in rows),
        sum(float(row["ber"]) > 0.0038 for row in rows),
        sum(int(row["bit_errors"]) for row in rows),
        int(setting_index),
    )


def pooled_ber(rows: list[dict]) -> dict:
    """Pool integer errors/denominators and apply only the registered zero bound."""
    errors = sum(int(row["bit_errors"]) for row in rows)
    denominator = sum(int(row["denominator"]) for row in rows)
    if denominator <= 0:
        raise ValueError("pooled BER requires positive denominator")
    raw = errors / denominator
    return {
        "bit_errors": errors,
        "denominator": denominator,
        "pooled_raw_ber": raw,
        "effective_ber": raw if errors else 0.5 / denominator,
    }


def _curve_values(curve: list) -> tuple[list[float], list[float]]:
    raw = [
        float(point["pooled_raw_ber"]) if isinstance(point, dict) else float(point)
        for point in curve
    ]
    effective = [
        float(point["effective_ber"]) if isinstance(point, dict) else float(point)
        for point in curve
    ]
    if len(raw) != 5 or any(value <= 0 for value in effective):
        raise ValueError("each SNR curve requires five positive effective BER values")
    return raw, effective


def freeze_snr_window(curves: dict[str, list]) -> dict:
    """Freeze one three-point SNR window using the exact common/no-common rule."""
    required = {
        "PRIMARY_METHOD",
        "P1_FIXED",
        "CHEAP_AMPLITUDE_FREEZE",
        "BSTAR",
    }
    if set(curves) != required:
        raise ValueError("SNR freeze requires the four preregistered arms")
    values = {arm: _curve_values(curve) for arm, curve in curves.items()}

    def objective(indices: list[int]) -> float:
        return max(
            abs(math.log10(values[arm][1][index] / 0.0038))
            for arm in required
            for index in indices
        )

    common = [
        lower
        for lower in range(4)
        if all(
            values[arm][0][lower] > 0.0038
            and values[arm][0][lower + 1] <= 0.0038
            for arm in required
        )
    ]
    if common:
        lower = min(common, key=lambda index: (objective([index, index + 1]), index))
        starts = [start for start in range(3) if start <= lower and start + 2 >= lower + 1]
        start = min(starts, key=lambda index: (objective([index, index + 1, index + 2]), index))
        marker = "COMMON_VALIDATION_CROSSING"
        bracket = [lower, lower + 1]
    else:
        start = min(
            range(3),
            key=lambda index: (objective([index, index + 1, index + 2]), index),
        )
        marker = "NO_COMMON_VALIDATION_CROSSING"
        bracket = None
    return {
        "common_bracket": bracket,
        "window_indices": [start, start + 1, start + 2],
        "marker": marker,
        "objective": objective([start, start + 1, start + 2]),
    }


def validate_checkpoint_payload(payload: dict) -> int:
    """Validate strict rows and exact current 17-file source bundle."""
    count = validate_checkpoint_rows(payload.get("rows", []))
    if payload.get("source_hashes") != source_hash_bundle():
        raise StaleCheckpointError("checkpoint source hash bundle is stale")
    return count


def append_complete_cell(existing: list[dict], new_rows: list[dict]) -> list[dict]:
    """Append one complete cell while proving the existing prefix is unchanged."""
    validate_checkpoint_rows(existing)
    if len(new_rows) != 30:
        raise StaleCheckpointError("append must contain exactly one 30-row cell")
    before = json.loads(json.dumps(existing))
    before_sha = canonical_rows_sha256(existing)
    combined = existing + new_rows
    validate_checkpoint_rows(combined)
    if combined[: len(existing)] != before:
        raise StaleCheckpointError("existing prefix changed during append")
    if canonical_rows_sha256(combined[: len(existing)]) != before_sha:
        raise StaleCheckpointError("existing prefix SHA changed during append")
    return combined


def _execute_validation_arm(shared: dict, arm_index: int, setting: dict) -> dict:
    """Execute one frozen-grid arm using only the shared receiver realization."""
    rx = shared["rx"]
    if arm_index == 0:
        module = _load_local("source_native_rls.py", "t010_c2_source")
        result = module.run_source_native_rls(
            rx,
            forgetting_factor=setting["forgetting_factor"],
            symbol_rate=shared["symbol_rate"],
        )
    elif arm_index in (1, 2, 3):
        module = _load_local("methods.py", "t010_c2_methods")
        if arm_index == 1:
            result = module.run_innovation_freeze(rx, **setting)
        elif arm_index == 2:
            result = module.run_adaptive_forgetting(rx, **setting)
        else:
            result = module.run_amplitude_freeze(rx, **setting)
    else:
        module = _load_local("baselines.py", "t010_c2_baselines")
        if arm_index == 4:
            result = module.run_4opm_bps(
                rx, symbol_rate=shared["symbol_rate"], **setting
            )
        else:
            result = module.run_4opm_dd_dpll(
                rx, symbol_rate=shared["symbol_rate"], **setting
            )
    update_mask = result.get("update_mask")
    innovation = result.get("normalized_innovation")
    return {
        "corrected": result["corrected"],
        "state_finite": bool(
            result.get("state_finite", np.all(np.isfinite(result["corrected"])))
        ),
        "update_rate": (
            float(np.mean(update_mask[128:])) if update_mask is not None else None
        ),
        "freeze_rate": (
            float(1.0 - np.mean(update_mask[128:])) if update_mask is not None else None
        ),
        "innovation_stats": (
            {
                "mean": float(np.mean(innovation[128:])),
                "max": float(np.max(innovation[128:])),
            }
            if innovation is not None
            else {}
        ),
    }


def validation_cell_rows(
    shared: dict,
    *,
    gg_index: int,
    snr_index: int,
    seed_index: int,
    arm_runner=None,
) -> list[dict]:
    """Evaluate all 30 settings against one and the same shared object."""
    runner = arm_runner or _execute_validation_arm
    rows = []
    data_mask = np.asarray(shared["data_mask"], dtype=bool)
    truth = np.asarray(shared["data_bits"], dtype=int)
    denominator = int(len(truth))
    for arm_index, settings in enumerate(c2_setting_grid()):
        for setting_index, setting in enumerate(settings):
            result = runner(shared, arm_index, setting)
            estimated = qam16_demod(np.asarray(result["corrected"])[data_mask])
            errors = int(np.count_nonzero(estimated != truth))
            metric = make_metric_row(bit_errors=errors, denominator=denominator)
            rows.append({
                "row_key": [
                    int(gg_index),
                    int(snr_index),
                    int(seed_index),
                    int(arm_index),
                    int(setting_index),
                ],
                **metric,
                "condition": ["weak", "moderate", "strong"][gg_index],
                "snr_db": [14.0, 17.0, 20.0, 23.0, 26.0][snr_index],
                "seed": SEED_PLAN["validation"][seed_index],
                "arm": [
                    "P1_FIXED",
                    "P2_INNOVATION_FREEZE",
                    "P3_BOUNDED_ADAPTIVE_FORGETTING",
                    "CHEAP_AMPLITUDE_FREEZE",
                    "4OPM_BPS",
                    "4OPM_CONTINUOUS_DD_DPLL",
                ][arm_index],
                "setting_index": setting_index,
                "setting": setting,
                "update_rate": result["update_rate"],
                "freeze_rate": result["freeze_rate"],
                "innovation_stats": result["innovation_stats"],
                "state_finite": bool(result["state_finite"]),
            })
    return rows


def aggregate_validation(rows: list[dict]) -> dict:
    """Freeze settings and SNR windows only after the complete 2250-row matrix."""
    if len(rows) != 2250:
        raise ValueError("validation aggregate requires exactly 2250 rows")
    validate_checkpoint_rows(rows)
    arm_names = [
        "P1_FIXED",
        "P2_INNOVATION_FREEZE",
        "P3_BOUNDED_ADAPTIVE_FORGETTING",
        "CHEAP_AMPLITUDE_FREEZE",
        "4OPM_BPS",
        "4OPM_CONTINUOUS_DD_DPLL",
    ]
    frozen: dict[str, dict] = {}
    for arm_index, (arm, settings) in enumerate(zip(arm_names, c2_setting_grid())):
        candidates = {}
        for setting_index in range(len(settings)):
            selected = [
                row
                for row in rows
                if row["row_key"][3:] == [arm_index, setting_index]
            ]
            candidates[setting_index] = setting_score(selected, setting_index)
        winner = min(candidates, key=lambda index: candidates[index])
        frozen[arm] = {"setting_index": winner, "score": candidates[winner]}
    primary = select_primary({
        "P2": frozen["P2_INNOVATION_FREEZE"]["score"],
        "P3": frozen["P3_BOUNDED_ADAPTIVE_FORGETTING"]["score"],
    })
    bstar = select_bstar({
        "4OPM_BPS": frozen["4OPM_BPS"]["score"],
        "4OPM_CONTINUOUS_DD_DPLL": frozen["4OPM_CONTINUOUS_DD_DPLL"]["score"],
    })
    chosen = {
        "PRIMARY_METHOD": (
            1 if primary == "P2" else 2,
            frozen[
                "P2_INNOVATION_FREEZE"
                if primary == "P2"
                else "P3_BOUNDED_ADAPTIVE_FORGETTING"
            ]["setting_index"],
        ),
        "P1_FIXED": (0, frozen["P1_FIXED"]["setting_index"]),
        "CHEAP_AMPLITUDE_FREEZE": (
            3,
            frozen["CHEAP_AMPLITUDE_FREEZE"]["setting_index"],
        ),
        "BSTAR": (
            4 if bstar == "4OPM_BPS" else 5,
            frozen[bstar]["setting_index"],
        ),
    }
    snr_freeze = {}
    for gg_index, gg_name in enumerate(("weak", "moderate", "strong")):
        curves = {}
        for label, (arm_index, setting_index) in chosen.items():
            curves[label] = [
                pooled_ber([
                    row
                    for row in rows
                    if row["row_key"][0] == gg_index
                    and row["row_key"][1] == snr_index
                    and row["row_key"][3:] == [arm_index, setting_index]
                ])
                for snr_index in range(5)
            ]
        snr_freeze[gg_name] = freeze_snr_window(curves)
    return {
        "legacy_debt": "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT",
        "frozen_settings": frozen,
        "primary_method": primary,
        "bstar": bstar,
        "snr_freeze": snr_freeze,
    }


def run_validation(
    *,
    max_cells: int | None = None,
    artifact_path: str | Path | None = None,
) -> dict:
    """Run/resume C2 in canonical cells; never consumes held-out seeds."""
    if max_cells is not None and (not isinstance(max_cells, int) or max_cells < 0):
        raise ValueError("max_cells must be a nonnegative integer or None")
    target = Path(artifact_path) if artifact_path else PACKAGE_DIR / "artifacts/validation-raw.json"
    hashes = source_hash_bundle()
    if target.exists():
        payload = json.loads(target.read_text(encoding="utf-8"))
        validate_checkpoint_payload(payload)
        rows = payload["rows"]
    else:
        rows = []
    start_cell = len(rows) // 30
    stop_cell = 75 if max_cells is None else min(75, start_cell + max_cells)

    from params import B5Params, SimulationConfig

    config = SimulationConfig()
    symbol_rate = float(B5Params().R_SYM_B5)
    turbulence = config.turbulence
    gg_values = [
        (turbulence.turb_weak_alpha, turbulence.turb_weak_beta),
        (turbulence.turb_moderate_alpha, turbulence.turb_moderate_beta),
        (turbulence.turb_strong_alpha, turbulence.turb_strong_beta),
    ]
    shared_module = _load_local("shared_realization.py", "t010_c2_shared")
    directory_fsync = "UNSUPPORTED_PLATFORM" if os.name == "nt" else "SUPPORTED"
    for cell_index in range(start_cell, stop_cell):
        gg_index = cell_index // 25
        remainder = cell_index % 25
        snr_index = remainder // 5
        seed_index = remainder % 5
        alpha, beta = gg_values[gg_index]
        shared = shared_module.generate_shared_b10_realization(
            seed=SEED_PLAN["validation"][seed_index],
            n_symbols=25_000,
            symbol_rate=symbol_rate,
            esn0_db=[14.0, 17.0, 20.0, 23.0, 26.0][snr_index],
            linewidth_hz=float(config.system.LASER_LW),
            cfo_hz=float(config.doppler.F_RESIDUAL),
            alpha=float(alpha),
            beta=float(beta),
            greenwood_hz=float(config.gg_time.GREENWOOD_FREQ_DEFAULT),
            block=100,
            gg_method="gar",
            pilot_enabled=True,
            use_gg=True,
        )
        cell_rows = validation_cell_rows(
            shared,
            gg_index=gg_index,
            snr_index=snr_index,
            seed_index=seed_index,
        )
        rows = append_complete_cell(rows, cell_rows)
        payload = {
            "schema": "t010.c2-validation-raw.v1",
            "phase": "C2_VALIDATION_ONLY",
            "legacy_debt": "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT",
            "mission_method_delta": "NONE",
            "heldout_consumed": False,
            "directory_fsync": directory_fsync,
            "source_hashes": hashes,
            "row_count": len(rows),
            "expected_row_count": 2250,
            "rows": rows,
        }
        directory_fsync = atomic_save_validation(payload, target)

    result = {
        "row_count": len(rows),
        "complete": len(rows) == 2250,
        "artifact": str(target),
        "directory_fsync": directory_fsync,
    }
    if len(rows) == 2250:
        aggregate = aggregate_validation(rows)
        aggregate_payload = {
            "schema": "t010.c2-validation-aggregate.v1",
            "phase": "C2_VALIDATION_ONLY",
            "legacy_debt": "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT",
            "mission_method_delta": "NONE",
            "heldout_consumed": False,
            "source_hashes": hashes,
            **aggregate,
        }
        aggregate_path = target.with_name("validation-aggregate.json")
        atomic_save_validation(aggregate_payload, aggregate_path)
        result["aggregate_artifact"] = str(aggregate_path)
    return result


def _load_local(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, PACKAGE_DIR / filename)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def ber_to_q2_db(ber: float, *, denominator: int | None = None) -> float | None:
    """Convert BER to Q² dB using the registered row-local zero-error bound."""
    if not 0.0 <= ber <= 1.0:
        raise ValueError("ber must lie in [0, 1]")
    if ber >= 0.5:
        return None
    q_input = ber
    if ber == 0.0:
        if denominator is None or denominator <= 0:
            raise ValueError("positive denominator is required for zero BER")
        q_input = 0.5 / denominator
    q = math.sqrt(2.0) * float(erfcinv(2.0 * q_input))
    return 20.0 * math.log10(q)


def make_metric_row(*, bit_errors: int, denominator: int) -> dict:
    """Build the single authoritative BER/Q² row representation."""
    if not isinstance(bit_errors, int) or not isinstance(denominator, int):
        raise TypeError("bit_errors and denominator must be integers")
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if bit_errors < 0 or bit_errors > denominator:
        raise ValueError("bit_errors must lie in [0, denominator]")

    ber = bit_errors / denominator
    ber_bound = 0.5 / denominator if bit_errors == 0 else None
    q2_db = ber_to_q2_db(ber, denominator=denominator)
    return {
        "bit_errors": bit_errors,
        "denominator": denominator,
        "ber": ber,
        "ber_bound": ber_bound,
        "q2_db": q2_db,
    }


def parse_t006_worker_log_seed_pools(text: str | None = None) -> dict:
    """Parse the single explicit T006 seed-disjointness fact statement."""
    if text is None:
        worker_log = (
            REPO_ROOT
            / "projects/thesis-fso/worker-logs/step-006-high-order-cpr-combination-method.md"
        )
        text = worker_log.read_text(encoding="utf-8")
    pattern = re.compile(
        r"seeds disjoint：val\{(?P<v0>\d+)-(?P<v1>\d+)\}"
        r"\s*∩\s*test\{(?P<t0>\d+)-(?P<t1>\d+)\}"
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(
            "T006 worker-log must contain exactly one explicit "
            "'seeds disjoint：val{a-b} ∩ test{c-d}' fact"
        )
    values = {key: int(value) for key, value in matches[0].groupdict().items()}
    if values["v1"] < values["v0"] or values["t1"] < values["t0"]:
        raise ValueError("T006 worker-log seed ranges are descending")
    return {
        "validation": list(range(values["v0"], values["v1"] + 1)),
        "test": list(range(values["t0"], values["t1"] + 1)),
    }


def verify_seed_census() -> dict:
    """Reparse every historical fact source and close it against T010 files."""
    census = yaml.safe_load((PACKAGE_DIR / "seed-census.yaml").read_text(encoding="utf-8"))
    contract = yaml.safe_load((PACKAGE_DIR / "contract.yaml").read_text(encoding="utf-8"))
    t006 = yaml.safe_load(
        (
            REPO_ROOT
            / "projects/simulation/explore/high-order-cpr-combination/contract.yaml"
        ).read_text(encoding="utf-8")
    )
    t008 = yaml.safe_load(
        (
            REPO_ROOT
            / "projects/simulation/explore/b1-adaptive-phase-window-v2/seed-census.yaml"
        ).read_text(encoding="utf-8")
    )
    t009 = yaml.safe_load(
        (
            REPO_ROOT
            / "projects/simulation/explore/a4-deployable-adaptive-cpr-v2/seed-census.yaml"
        ).read_text(encoding="utf-8")
    )

    historical = {
        "t006": {
            "validation": t006["seed_plan"]["method_validation_seeds"],
            "test": t006["seed_plan"]["method_test_seeds"],
        },
        "t008": {
            "validation": t008["fresh_pools"]["bstar_validation_seeds"],
            "test": t008["fresh_pools"]["test_seeds"],
        },
        "t009": {
            "validation": t009["validation_seeds"],
            "test": t009["test_seeds"],
        },
    }
    if parse_t006_worker_log_seed_pools() != historical["t006"]:
        raise ValueError("T006 worker-log seed facts disagree with T006 contract")
    if historical != census["historical"]:
        raise ValueError("seed census does not match reparsed historical sources")
    for key, values in SEED_PLAN.items():
        if values != census["t010"][key] or values != contract["seed_contract"][key]:
            raise ValueError(f"T010 seed mismatch for {key}")

    pools = list(SEED_PLAN.values())
    for prior in historical.values():
        pools.extend((prior["validation"], prior["test"]))
    for i, left in enumerate(pools):
        for right in pools[i + 1 :]:
            if not set(left).isdisjoint(right):
                raise ValueError("seed pools are not pairwise disjoint")
    return {key: list(value) for key, value in SEED_PLAN.items()}


def run_source_smoke() -> dict:
    """Run only the preregistered P1 source-identity smoke."""
    if (PACKAGE_DIR / "artifacts/source-smoke.json").exists():
        raise RuntimeError(
            "source smoke is sealed after the accepted confirm; realization was not generated"
        )
    shared_mod = _load_local("shared_realization.py", "t010_shared_smoke")
    rls_mod = _load_local("source_native_rls.py", "t010_rls_smoke")
    cells = []
    for cfo_hz in SOURCE_SMOKE_CONFIG["cfo_hz"]:
        shared = shared_mod.generate_shared_b10_realization(
            seed=SOURCE_SMOKE_CONFIG["seed"],
            n_symbols=SOURCE_SMOKE_CONFIG["n_symbols"],
            symbol_rate=SOURCE_SMOKE_CONFIG["symbol_rate"],
            esn0_db=SOURCE_SMOKE_CONFIG["esn0_db"],
            linewidth_hz=SOURCE_SMOKE_CONFIG["linewidth_hz"],
            cfo_hz=cfo_hz,
            use_gg=False,
        )
        result = rls_mod.run_source_native_rls(
            shared["rx"],
            forgetting_factor=SOURCE_SMOKE_FORGETTING_FACTOR,
            symbol_rate=SOURCE_SMOKE_CONFIG["symbol_rate"],
        )
        data_rx = shared["rx"][128:]
        corrected = result["corrected"][128:]
        data_bits = shared["data_bits"]
        raw_bits = qam16_demod(data_rx)
        corrected_bits = qam16_demod(corrected)
        denominator = int(len(data_bits))
        raw = make_metric_row(
            bit_errors=int(np.count_nonzero(raw_bits != data_bits)),
            denominator=denominator,
        )
        recovered = make_metric_row(
            bit_errors=int(np.count_nonzero(corrected_bits != data_bits)),
            denominator=denominator,
        )
        relative_error = abs(result["estimated_cfo_hz"] - cfo_hz) / cfo_hz
        gates = {
            "positive_cfo": bool(result["estimated_cfo_hz"] > 0.0),
            "cfo_relative_error_le_5pct": bool(relative_error <= 0.05),
            "finite_state": bool(result["state_finite"]),
            "switch_at_128": bool(result["switch_index_zero_based"] == 128),
            "period_frozen_once": bool(result["period_freeze_count"] == 1),
            "positive_phase_slope": bool(result["training_slope"] > 0.0),
            "ber_improved": bool(recovered["ber"] < raw["ber"]),
            "q2_improved": bool(
                recovered["q2_db"] is not None
                and (raw["q2_db"] is None or recovered["q2_db"] > raw["q2_db"])
            ),
            "ber_below_hd_fec": bool(recovered["ber"] < 3.8e-3),
        }
        cells.append(
            {
                "cfo_hz": cfo_hz,
                "estimated_cfo_hz": result["estimated_cfo_hz"],
                "cfo_relative_error": relative_error,
                "training_slope_rad_per_symbol": result["training_slope"],
                "raw": raw,
                "p1": recovered,
                "gates": gates,
                "pass": bool(all(gates.values())),
            }
        )

    payload = {
        "schema": "t010.source-smoke.v1",
        "scope": "source_identity_smoke_only",
        "performance_claim": "NONE",
        "config": SOURCE_SMOKE_CONFIG,
        "forgetting_factor": {
            "value": SOURCE_SMOKE_FORGETTING_FACTOR,
            "type": SOURCE_SMOKE_FORGETTING_FACTOR_TYPE,
        },
        "cells": cells,
        "verdict": "PASS" if all(cell["pass"] for cell in cells) else "BLOCKED_IDENTITY",
    }
    save_results(
        payload,
        str(PACKAGE_DIR / "artifacts/source-smoke.json"),
        "t010_b10_source_identity_smoke",
    )
    return payload


def read_source_smoke_gate() -> dict:
    """Read and validate the already-written confirm artifact; never execute it."""
    path = PACKAGE_DIR / "artifacts/source-smoke.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["config"]["seed"] != SOURCE_SMOKE_CONFIG["seed"]:
        raise ValueError("source smoke seed does not match the clean-confirm contract")
    if payload["forgetting_factor"] != {
        "value": SOURCE_SMOKE_FORGETTING_FACTOR,
        "type": SOURCE_SMOKE_FORGETTING_FACTOR_TYPE,
    }:
        raise ValueError("source smoke forgetting factor does not match the contract")
    cells = payload.get("cells", [])
    if {cell.get("cfo_hz") for cell in cells} != set(SOURCE_SMOKE_CONFIG["cfo_hz"]):
        raise ValueError("source smoke must contain exactly the 1/10 GHz cells")
    return payload


def recompute_source_smoke_gate() -> dict:
    """Recompute only fields persisted by the legacy Phase-B artifact.

    State finiteness, switch index and period-freeze count were persisted only
    as booleans, not as their source state. They are therefore explicitly
    non-recomputable rather than reconstructed after the fact.
    """
    payload = read_source_smoke_gate()
    recomputable = [
        "bit_errors",
        "denominator",
        "ber",
        "q2_db",
        "cfo_relative_error",
        "positive_cfo",
        "cfo_relative_error_le_5pct",
        "ber_improved",
        "q2_improved",
        "ber_below_hd_fec",
    ]
    stored_closure_verified = True
    for cell in payload["cells"]:
        for arm in ("raw", "p1"):
            stored = cell[arm]
            rebuilt = make_metric_row(
                bit_errors=int(stored["bit_errors"]),
                denominator=int(stored["denominator"]),
            )
            for field in ("ber", "q2_db"):
                if rebuilt[field] != stored[field]:
                    raise ValueError(f"source smoke {arm}.{field} does not recompute")
        relative = abs(cell["estimated_cfo_hz"] - cell["cfo_hz"]) / cell["cfo_hz"]
        gates = {
            "positive_cfo": cell["estimated_cfo_hz"] > 0.0,
            "cfo_relative_error_le_5pct": relative <= 0.05,
            "ber_improved": cell["p1"]["ber"] < cell["raw"]["ber"],
            "q2_improved": (
                cell["p1"]["q2_db"] is not None
                and (
                    cell["raw"]["q2_db"] is None
                    or cell["p1"]["q2_db"] > cell["raw"]["q2_db"]
                )
            ),
            "ber_below_hd_fec": cell["p1"]["ber"] < 3.8e-3,
        }
        if relative != cell["cfo_relative_error"]:
            raise ValueError("source smoke CFO relative error does not recompute")
        if any(bool(cell["gates"][key]) != bool(value) for key, value in gates.items()):
            raise ValueError("source smoke recomputable gate mismatch")
        if bool(cell["pass"]) != bool(all(cell["gates"].values())):
            raise ValueError("stored cell pass does not close over stored gates")
        stored_closure_verified &= bool(cell["pass"])
    if payload["verdict"] != ("PASS" if stored_closure_verified else "BLOCKED_IDENTITY"):
        raise ValueError("stored verdict does not close over stored cell pass fields")
    legacy = {
        key: "LEGACY_NON_RECOMPUTABLE_PHASE_B_P2"
        for key in (
            "finite_state",
            "switch_at_128",
            "period_frozen_once",
            "positive_phase_slope",
        )
    }
    return {
        "mode": "READ_ONLY_RECOMPUTATION",
        "evidence_audit_status": "RECOMPUTABLE_FIELDS_MATCH",
        "scientific_verdict": "NOT_RECOMPUTED",
        "stored_verdict": payload["verdict"],
        "stored_closure_verified": stored_closure_verified,
        "recomputable_fields": recomputable,
        "legacy_non_recomputable": legacy,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-smoke",
        action="store_true",
        help="run only the Phase-B P1 source-identity smoke",
    )
    args = parser.parse_args()
    if not args.source_smoke:
        parser.error("only --source-smoke is authorized in Phase B")
    result = run_source_smoke()
    print(f"source_identity_verdict={result['verdict']}")


if __name__ == "__main__":
    main()
