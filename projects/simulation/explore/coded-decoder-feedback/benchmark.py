"""Engineering-only D0 throughput slice orchestration and authorized CLI."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import ctypes
from dataclasses import dataclass
from functools import partial
import hashlib
import importlib
import math
import multiprocessing
from pathlib import Path
import platform
import sys
import time
from types import MappingProxyType
from typing import Any

import numpy as np

from artifacts import ArtifactReceipt, canonical_json_bytes, write_jsonl_atomic
import b2 as b2_module
import codec as codec_module
from contract import (
    D0OwnerIdentityAuthority,
    ResolvedDevFreeze,
    assert_frozen_owner_identity_authority,
    load_owner_identity_authority,
)
import freeze as freeze_module
from freeze import ExactBinary64Aggregate, exact_binary64_aggregate
import waveform as waveform_module


ENGINEERING_ROOT_SEED = 900_000_001
DECODER_BATCH_CW_SIZES = (4, 8, 12, 16)
BPS_PAIRS = ((32, 31), (32, 61), (32, 127), (64, 31), (64, 61), (64, 127))
REQUIRED_SLICES = (
    "one_unique_waveform_all_six_BPS_grid_pairs",
    "one_B2_tuple_ten_unique_polarization_views",
    "one_HMM_grid_chunk_with_primitive_and_aggregate_units",
    "representative_atomic_JSONL_and_receipt_write",
)
OWNER_RECORD_FIELDS = (
    "device",
    "dependency_versions",
    "physical_api_invocations",
    "logical_batches",
    "cache_hits",
    "wall_time",
    "peak_memory",
    "projected_full_D0_time",
)
D0_WORK_DAYS = MappingProxyType({
    "contract_source_and_asset_closure": 0.25,
    "receiver_truth_views_and_carrier_realization": 0.75,
    "B0_B1_O1_mapping_and_controlled_fixture": 0.50,
    "source_explicit_B2_adaptation_and_dev_freeze": 2.00,
    "strata_tests_statistics_and_cost_ledger": 0.50,
    "bounded_runs_raw_rows_ci_and_receipts": 0.50,
})
FROZEN_LOGICAL_COUNTS = MappingProxyType({
    "decoder_batches": 69_360,
    "cw_decodes": 1_032_000,
    "bp_iterations": 20_640_000,
    "hmm_dual_pol_frame_parameter_pair_scores": 8_344_800,
    "hmm_primitive_pol_trajectory_parameter_pair_scores": 16_689_600,
    "materialized_hmm_primitive_pol_trajectory_parameter_pair_scores": 7_027_200,
})
FROZEN_MATERIALIZED_COUNTS = MappingProxyType({
    "decoder_batches": 48_900,
    "cw_decodes": 704_640,
    "bp_iterations": 14_092_800,
    "hmm_primitive_pol_trajectory_parameter_pair_scores": 7_027_200,
})
ALLOWED_ADJUSTMENTS = (
    "vectorization",
    "batch_size",
    "content_addressed_cache",
    "checkpoint_chunk_size",
)
HMM_STRICT_ATOL = 1e-12
HMM_MEASUREMENT_REPEATS = 3


class BenchmarkError(ValueError):
    """The injected engineering worker violated the frozen I16 manifest."""


@dataclass(frozen=True, slots=True)
class EngineeringManifest:
    benchmark_class: str
    root_seed: int
    dev_freeze_sha256: str
    owner_sha256: str
    synthetic_resolved_freeze: bool
    decoder_batch_cw_sizes: tuple[int, ...]
    bps_pairs: tuple[tuple[int, int], ...]
    b2_view_count: int
    required_slices: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DecoderBatchSlice:
    cw_batch: int
    fresh_restart: bool
    result_sha256: str


@dataclass(frozen=True, slots=True)
class BpsSlice:
    pair: tuple[int, int]
    waveform_sha256: str
    result_sha256: str


@dataclass(frozen=True, slots=True)
class HmmSlice:
    primitive_scores: tuple[float, ...]
    primitive_count: int
    aggregate: ExactBinary64Aggregate
    primitive_sha256: str


@dataclass(frozen=True, slots=True)
class EngineeringBenchmarkRun:
    manifest: EngineeringManifest
    decoder_batches: tuple[DecoderBatchSlice, ...]
    bps_slices: tuple[BpsSlice, ...]
    b2_view_sha256: tuple[str, ...]
    hmm: HmmSlice
    atomic_io: ArtifactReceipt


@dataclass(frozen=True, slots=True)
class WatchdogResult:
    status: str
    elapsed_seconds: float
    value: Any | None


@dataclass(frozen=True, slots=True)
class FullWorkProjection:
    logical_counts: Mapping[str, int]
    materialized_counts: Mapping[str, int]
    adjustments: tuple[str, ...]
    logical_manifest_sha256: str


@dataclass(frozen=True, slots=True)
class EngineeringAdjustmentReceipt:
    name: str
    applicability: str
    config: Mapping[str, Any]
    before_elapsed_seconds: float
    after_elapsed_seconds: float
    before_unit_count: int
    after_unit_count: int
    before_output_sha256: str
    after_output_sha256: str
    actual_cache_reads: int
    logical_manifest_sha256_before: str
    logical_manifest_sha256_after: str
    materialized_projection_before: Mapping[str, int]
    materialized_projection_after: Mapping[str, int]
    materialized_projection_change_source: str
    output_equivalent_to_scalar: bool
    max_abs_error: float


@dataclass(frozen=True, slots=True)
class BenchmarkReceipt:
    status: str
    owner_budget_sha256: str
    seconds_per_day: int
    engineering_record: Mapping[str, Any]
    workload_manifest_sha256: str
    completed_work_ids: tuple[str, ...]
    remaining_work_ids: tuple[str, ...]
    consumed_work_days: Mapping[str, float]
    remaining_work_days: Mapping[str, float]
    consumed_engineering_days: float
    projected_remaining_D0_days: float
    projected_D0_days: float
    post_D0_C1_days: float
    contingency_consumed_days: float
    required_remaining_contingency_days: float
    projected_mission_days: float
    elapsed_seconds: float
    watchdog_seconds: int
    incomplete_reasons: tuple[str, ...]
    adjustment_receipts: tuple[EngineeringAdjustmentReceipt, ...] = ()
    selected_adjustment_name: str | None = None
    selected_hmm_seconds_per_trajectory: float | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkFreezeBinding:
    dev_freeze_sha256: str
    phases: tuple[str, ...]
    receipt_bytes: bytes
    receipt_sha256: str


def bind_resolved_freeze(
    resolved: ResolvedDevFreeze,
    phase_receipts: Sequence[Mapping[str, Any]],
    *,
    benchmark_freeze_sha256: str,
) -> BenchmarkFreezeBinding:
    """Bind the engineering entry point to the one five-phase dev freeze."""

    if type(resolved) is not ResolvedDevFreeze:
        raise BenchmarkError("exact ResolvedDevFreeze required for benchmark binding")
    if type(benchmark_freeze_sha256) is not str or benchmark_freeze_sha256 != resolved.freeze_id:
        raise BenchmarkError("benchmark manifest and ResolvedDevFreeze hashes differ")
    try:
        freeze_id = freeze_module.assert_phase_freeze_chronology(
            resolved, tuple(phase_receipts)
        )
    except (TypeError, ValueError) as exc:
        raise BenchmarkError("benchmark phase freeze binding is incomplete") from exc
    phases = ("S1", "S2", "S3_DEV", "S3_TEST", "S4")
    document = {
        "schema": "coded_decoder_feedback.d0.benchmark_freeze_binding.v1",
        "dev_freeze_sha256": freeze_id,
        "phases": phases,
    }
    receipt_bytes = canonical_json_bytes(document)
    return BenchmarkFreezeBinding(
        dev_freeze_sha256=freeze_id,
        phases=phases,
        receipt_bytes=receipt_bytes,
        receipt_sha256=hashlib.sha256(receipt_bytes).hexdigest(),
    )


def _worker_method(worker: Any, name: str):
    method = getattr(worker, name, None)
    if not callable(method):
        raise BenchmarkError(f"engineering worker requires callable {name}")
    return method


def _exact_count_mapping(value: Mapping[str, Any], expected: set[str], label: str) -> dict[str, int]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise BenchmarkError(f"{label} axes must be exact and complete")
    result = dict(value)
    if any(type(item) is not int or item < 0 for item in result.values()):
        raise BenchmarkError(f"{label} counts must be non-negative exact integers")
    return result


def build_full_work_projection(
    *,
    logical_counts: Mapping[str, Any] | None = None,
    materialized_counts: Mapping[str, Any] | None = None,
) -> FullWorkProjection:
    """Bind every frozen logical axis before any throughput extrapolation."""

    logical = _exact_count_mapping(
        FROZEN_LOGICAL_COUNTS if logical_counts is None else logical_counts,
        set(FROZEN_LOGICAL_COUNTS),
        "logical workload",
    )
    if logical != dict(FROZEN_LOGICAL_COUNTS):
        raise BenchmarkError("logical workload counts differ from the frozen owner")
    materialized = _exact_count_mapping(
        FROZEN_MATERIALIZED_COUNTS if materialized_counts is None else materialized_counts,
        set(FROZEN_MATERIALIZED_COUNTS),
        "materialized workload",
    )
    digest = hashlib.sha256(canonical_json_bytes(logical)).hexdigest()
    return FullWorkProjection(
        MappingProxyType(logical),
        MappingProxyType(materialized),
        (),
        digest,
    )


def apply_engineering_adjustments(
    projection: FullWorkProjection,
    *,
    adjustments: Sequence[str],
    materialized_counts: Mapping[str, Any],
) -> FullWorkProjection:
    """Allow implementation tuning while preserving the logical manifest."""

    if type(projection) is not FullWorkProjection:
        raise TypeError("exact FullWorkProjection required")
    names = tuple(adjustments)
    if (
        any(type(name) is not str or name not in ALLOWED_ADJUSTMENTS for name in names)
        or len(set(names)) != len(names)
    ):
        raise BenchmarkError("forbidden or duplicate engineering adjustment")
    materialized = dict(projection.materialized_counts)
    if not isinstance(materialized_counts, Mapping):
        raise BenchmarkError("materialized adjustment counts must be a mapping")
    for key, value in materialized_counts.items():
        if key not in materialized or type(value) is not int or value < 0:
            raise BenchmarkError("materialized adjustment axes/counts are invalid")
        materialized[key] = value
    return FullWorkProjection(
        projection.logical_counts,
        MappingProxyType(materialized),
        names,
        projection.logical_manifest_sha256,
    )


def _watchdog_worker(operation, sender) -> None:
    try:
        sender.send(("VALUE", operation()))
    except BaseException as exc:
        sender.send(("ERROR", type(exc).__name__, str(exc)))
    finally:
        sender.close()


def watchdog_call(operation, *, watchdog_seconds: int | float = 720) -> WatchdogResult:
    """Run an operation behind a spawn-process hard termination boundary."""

    if not callable(operation):
        raise TypeError("operation must be callable")
    if (
        type(watchdog_seconds) not in (int, float)
        or not math.isfinite(float(watchdog_seconds))
        or watchdog_seconds <= 0
    ):
        raise BenchmarkError("watchdog_seconds must be a positive finite number")
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_watchdog_worker, args=(operation, sender))
    started = time.monotonic()
    try:
        process.start()
        sender.close()
        process.join(float(watchdog_seconds))
        elapsed = time.monotonic() - started
        if process.is_alive():
            process.terminate()
            process.join()
            if process.is_alive():
                process.kill()
                process.join()
            return WatchdogResult("INCOMPLETE", elapsed, None)
        if elapsed >= float(watchdog_seconds):
            return WatchdogResult("INCOMPLETE", elapsed, None)
        if not receiver.poll():
            raise BenchmarkError(
                f"watchdog worker exited without a result (exitcode={process.exitcode})"
            )
        message = receiver.recv()
        if message[0] == "ERROR":
            raise BenchmarkError(f"watchdog operation failed: {message[1]}: {message[2]}")
        return WatchdogResult("COMPLETE", elapsed, message[1])
    finally:
        receiver.close()
        if process.is_alive():
            process.terminate()
            process.join()


def _finite_days(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise BenchmarkError(f"{label} must be a finite non-negative day count")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise BenchmarkError(f"{label} must be a finite non-negative day count") from exc
    if not math.isfinite(result) or result < 0.0:
        raise BenchmarkError(f"{label} must be a finite non-negative day count")
    return result


def _work_days(value: Mapping[str, Any], label: str) -> dict[str, float]:
    if not isinstance(value, Mapping):
        raise BenchmarkError(f"{label} must be a mapping")
    return {key: _finite_days(item, f"{label}.{key}") for key, item in value.items()}


def _owner_record_is_valid(record: Mapping[str, Any]) -> bool:
    """Validate the eight owner runtime fields without numeric coercion."""

    device = record["device"]
    versions = record["dependency_versions"]
    if type(device) is not str or not device:
        return False
    if (
        not isinstance(versions, Mapping)
        or not versions
        or any(
            type(key) is not str
            or not key
            or type(value) is not str
            or not value
            for key, value in versions.items()
        )
    ):
        return False
    for name in (
        "physical_api_invocations",
        "logical_batches",
        "cache_hits",
    ):
        value = record[name]
        if type(value) is not int or value < 0:
            return False
    peak = record["peak_memory"]
    if (
        not isinstance(peak, Mapping)
        or set(peak) != {
            "process_rss_peak_bytes",
            "accelerator_backend",
            "accelerator_peak_bytes",
        }
        or type(peak["process_rss_peak_bytes"]) is not int
        or peak["process_rss_peak_bytes"] <= 0
        or type(peak["accelerator_backend"]) is not str
        or not peak["accelerator_backend"]
    ):
        return False
    accelerator_peak = peak["accelerator_peak_bytes"]
    if peak["accelerator_backend"] == "not_applicable":
        if accelerator_peak is not None:
            return False
    elif type(accelerator_peak) is not int or accelerator_peak < 0:
        return False
    for name in ("wall_time", "projected_full_D0_time"):
        value = record[name]
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            return False
    return True


def _slices_complete(run: Any) -> bool:
    return (
        type(run) is EngineeringBenchmarkRun
        and tuple(item.cw_batch for item in run.decoder_batches) == DECODER_BATCH_CW_SIZES
        and all(item.fresh_restart for item in run.decoder_batches)
        and tuple(item.pair for item in run.bps_slices) == BPS_PAIRS
        and len({item.waveform_sha256 for item in run.bps_slices}) == 1
        and len(run.b2_view_sha256) == 10
        and len(set(run.b2_view_sha256)) == 10
        and run.hmm.primitive_count == run.hmm.aggregate.count > 0
        and run.atomic_io.record_count > 0
    )


def build_benchmark_receipt(
    run: EngineeringBenchmarkRun,
    *,
    owner_authority: D0OwnerIdentityAuthority,
    engineering_record: Mapping[str, Any],
    consumed_work_days: Mapping[str, Any],
    remaining_work_days: Mapping[str, Any],
    elapsed_seconds: float,
    watchdog_seconds: int = 720,
    adjustment_receipts: Sequence[EngineeringAdjustmentReceipt] = (),
    selected_adjustment_name: str | None = None,
    selected_hmm_seconds_per_trajectory: float | None = None,
) -> BenchmarkReceipt:
    """Close the owner partition and apply the sole frozen budget equation."""

    assert_frozen_owner_identity_authority(owner_authority)
    if run.manifest.owner_sha256 != owner_authority.owner_sha256:
        raise BenchmarkError("benchmark manifest is not bound to authoritative owner bytes")
    elapsed = _finite_days(elapsed_seconds, "elapsed_seconds")
    if type(watchdog_seconds) is not int or watchdog_seconds <= 0:
        raise BenchmarkError("watchdog_seconds must be a positive exact integer")
    consumed = _work_days(consumed_work_days, "consumed_work_days")
    remaining = _work_days(remaining_work_days, "remaining_work_days")
    completed_ids = tuple(sorted(consumed))
    remaining_ids = tuple(sorted(remaining))
    reasons = []
    if not _slices_complete(run):
        reasons.append("MISSING_REQUIRED_SLICE")
    record_valid = False
    if not isinstance(engineering_record, Mapping) or set(engineering_record) != set(OWNER_RECORD_FIELDS):
        reasons.append("MISSING_OWNER_RECORD")
        record = dict(engineering_record) if isinstance(engineering_record, Mapping) else {}
    else:
        record = dict(engineering_record)
        record_valid = _owner_record_is_valid(record)
        if not record_valid:
            reasons.append("INVALID_OWNER_RECORD")
    all_ids = set(D0_WORK_DAYS)
    partition_valid = not (set(completed_ids) & set(remaining_ids)) and (
        set(completed_ids) | set(remaining_ids) == all_ids
    )
    if not partition_valid:
        reasons.append("INVALID_WORK_PARTITION")
    if elapsed >= watchdog_seconds:
        reasons.append("WATCHDOG_TIMEOUT")

    consumed_days = math.fsum(consumed.values())
    remaining_days = math.fsum(remaining.values())
    projected_d0_days = consumed_days + remaining_days
    contingency_consumed_days = max(0.0, projected_d0_days - 4.50)
    required_remaining_contingency_days = 0.50 - contingency_consumed_days
    projected_mission_days = (
        consumed_days
        + remaining_days
        + 2.00
        + required_remaining_contingency_days
    )
    projection = build_full_work_projection()
    adjustments = tuple(adjustment_receipts)
    adjustment_evidence_valid = (
        tuple(item.name for item in adjustments) == ALLOWED_ADJUSTMENTS
        and all(
            type(item) is EngineeringAdjustmentReceipt
            and item.before_elapsed_seconds > 0.0
            and item.after_elapsed_seconds > 0.0
            and item.before_unit_count > 0
            and item.after_unit_count > 0
            and item.output_equivalent_to_scalar
            and item.max_abs_error <= HMM_STRICT_ATOL
            and item.logical_manifest_sha256_before == projection.logical_manifest_sha256
            and item.logical_manifest_sha256_after == projection.logical_manifest_sha256
            for item in adjustments
        )
        and selected_adjustment_name in {
            item.name for item in adjustments if item.applicability == "APPLICABLE"
        }
        and type(selected_hmm_seconds_per_trajectory) is float
        and math.isfinite(selected_hmm_seconds_per_trajectory)
        and selected_hmm_seconds_per_trajectory > 0.0
    )
    if (
        required_remaining_contingency_days < 0.0 or projected_mission_days > 7.00
    ) and not adjustment_evidence_valid:
        reasons.append("MISSING_ALLOWED_ADJUSTMENT_EVIDENCE")
    if record_valid and partition_valid and (
        float(record["projected_full_D0_time"]).hex()
        != float(projected_d0_days * 86_400.0).hex()
    ):
        reasons.append("PROJECTED_FULL_D0_TIME_MISMATCH")
    if reasons:
        status = "INCOMPLETE"
    elif required_remaining_contingency_days < 0.0 or projected_mission_days > 7.00:
        status = "GREATER_THAN_7D_HARD_BLOCKER"
    else:
        status = "ENGINEERING_THROUGHPUT_PASS"
    return BenchmarkReceipt(
        status=status,
        owner_budget_sha256=owner_authority.owner_sha256,
        seconds_per_day=86_400,
        engineering_record=MappingProxyType(record),
        workload_manifest_sha256=projection.logical_manifest_sha256,
        completed_work_ids=completed_ids,
        remaining_work_ids=remaining_ids,
        consumed_work_days=MappingProxyType(consumed),
        remaining_work_days=MappingProxyType(remaining),
        consumed_engineering_days=consumed_days,
        projected_remaining_D0_days=remaining_days,
        projected_D0_days=projected_d0_days,
        post_D0_C1_days=2.00,
        contingency_consumed_days=contingency_consumed_days,
        required_remaining_contingency_days=required_remaining_contingency_days,
        projected_mission_days=projected_mission_days,
        elapsed_seconds=elapsed,
        watchdog_seconds=watchdog_seconds,
        incomplete_reasons=tuple(reasons),
        adjustment_receipts=adjustments,
        selected_adjustment_name=selected_adjustment_name,
        selected_hmm_seconds_per_trajectory=selected_hmm_seconds_per_trajectory,
    )


def _adjustment_receipt_document(receipt: EngineeringAdjustmentReceipt) -> dict[str, Any]:
    return {
        "name": receipt.name,
        "applicability": receipt.applicability,
        "config": dict(receipt.config),
        "before_elapsed_seconds": receipt.before_elapsed_seconds,
        "after_elapsed_seconds": receipt.after_elapsed_seconds,
        "before_unit_count": receipt.before_unit_count,
        "after_unit_count": receipt.after_unit_count,
        "before_output_sha256": receipt.before_output_sha256,
        "after_output_sha256": receipt.after_output_sha256,
        "actual_cache_reads": receipt.actual_cache_reads,
        "logical_manifest_sha256_before": receipt.logical_manifest_sha256_before,
        "logical_manifest_sha256_after": receipt.logical_manifest_sha256_after,
        "materialized_projection_before": dict(receipt.materialized_projection_before),
        "materialized_projection_after": dict(receipt.materialized_projection_after),
        "materialized_projection_change_source": receipt.materialized_projection_change_source,
        "output_equivalent_to_scalar": receipt.output_equivalent_to_scalar,
        "max_abs_error": receipt.max_abs_error,
    }


def benchmark_receipt_document(receipt: BenchmarkReceipt) -> dict[str, Any]:
    if type(receipt) is not BenchmarkReceipt:
        raise TypeError("exact BenchmarkReceipt required")
    return {
        "schema": "coded_decoder_feedback.d0.engineering_benchmark_receipt.v1",
        "status": receipt.status,
        "owner_budget_sha256": receipt.owner_budget_sha256,
        "seconds_per_day": receipt.seconds_per_day,
        "engineering_record": dict(receipt.engineering_record),
        "workload_manifest_sha256": receipt.workload_manifest_sha256,
        "completed_work_ids": list(receipt.completed_work_ids),
        "remaining_work_ids": list(receipt.remaining_work_ids),
        "consumed_work_days": dict(receipt.consumed_work_days),
        "remaining_work_days": dict(receipt.remaining_work_days),
        "consumed_engineering_days": receipt.consumed_engineering_days,
        "projected_remaining_D0_days": receipt.projected_remaining_D0_days,
        "projected_D0_days": receipt.projected_D0_days,
        "post_D0_C1_days": receipt.post_D0_C1_days,
        "contingency_consumed_days": receipt.contingency_consumed_days,
        "required_remaining_contingency_days": receipt.required_remaining_contingency_days,
        "projected_mission_days": receipt.projected_mission_days,
        "elapsed_seconds": receipt.elapsed_seconds,
        "watchdog_seconds": receipt.watchdog_seconds,
        "incomplete_reasons": list(receipt.incomplete_reasons),
        "adjustment_receipts": [
            _adjustment_receipt_document(item) for item in receipt.adjustment_receipts
        ],
        "selected_adjustment_name": receipt.selected_adjustment_name,
        "selected_hmm_seconds_per_trajectory": receipt.selected_hmm_seconds_per_trajectory,
    }


def write_benchmark_receipt(path: str | Path, receipt: BenchmarkReceipt) -> ArtifactReceipt:
    """Land only complete receipt states, preserving any prior file on timeout."""

    if type(receipt) is not BenchmarkReceipt:
        raise TypeError("exact BenchmarkReceipt required")
    if receipt.status == "INCOMPLETE":
        raise BenchmarkError("incomplete benchmark receipt cannot replace prior evidence")
    return write_jsonl_atomic(
        path,
        (benchmark_receipt_document(receipt),),
        sort_key="schema",
        logical_name=Path(path).name,
    )


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="D0 engineering throughput gate")
    parser.add_argument("--class", dest="benchmark_class", required=True)
    parser.add_argument("--root-seed", type=int, required=True)
    parser.add_argument("--watchdog-seconds", type=int, required=True)
    parser.add_argument("--synthetic-resolved-freeze", action="store_true", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def parse_cli_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    args = build_cli_parser().parse_args(argv)
    if args.benchmark_class != "ENGINEERING_THROUGHPUT_V1":
        raise BenchmarkError("unsupported engineering benchmark class")
    if args.root_seed != ENGINEERING_ROOT_SEED or args.watchdog_seconds != 720:
        raise BenchmarkError("CLI seed/watchdog differ from the frozen I20 command")
    return args


def main(argv: Sequence[str] | None = None, *, runner=None) -> int:
    """Run the frozen I20 CLI, retaining injection only for unit seams."""

    args = parse_cli_args(argv)
    selected = _run_authorized_cli if runner is None else runner
    if not callable(selected):
        raise TypeError("runner must be callable")
    return int(selected(args))


def _exact_bytes(value: Any, label: str) -> bytes:
    if type(value) is bytes:
        if not value:
            raise BenchmarkError(f"{label} bytes cannot be empty")
        return value
    if not isinstance(value, Mapping):
        raise BenchmarkError(f"{label} must return bytes or a mapping")
    try:
        payload = canonical_json_bytes(value)
    except ValueError as exc:
        raise BenchmarkError(f"{label} is not canonical engineering output") from exc
    if not payload:
        raise BenchmarkError(f"{label} bytes cannot be empty")
    return payload


def _manifest(
    owner: D0OwnerIdentityAuthority,
    resolved: ResolvedDevFreeze,
    *,
    root_seed: int,
) -> EngineeringManifest:
    assert_frozen_owner_identity_authority(owner)
    contract = owner.contract
    if type(resolved) is not ResolvedDevFreeze:
        raise TypeError("resolved_freeze must be exact ResolvedDevFreeze")
    if type(root_seed) is not int or root_seed != ENGINEERING_ROOT_SEED:
        raise BenchmarkError("I16 requires the frozen engineering root seed 900000001")
    try:
        contract.seed_registry.label_for(root_seed)
    except ValueError:
        pass
    else:
        raise BenchmarkError("engineering root seed must remain outside every registry range")
    if resolved.parameters.get("synthetic_engineering_only") is not True:
        raise BenchmarkError("I16 requires an explicit synthetic engineering freeze")
    if (
        type(resolved.freeze_id) is not str
        or len(resolved.freeze_id) != 64
        or any(character not in "0123456789abcdef" for character in resolved.freeze_id)
    ):
        raise BenchmarkError("resolved freeze ID must be lowercase SHA256")
    return EngineeringManifest(
        benchmark_class="ENGINEERING_THROUGHPUT_V1",
        root_seed=root_seed,
        dev_freeze_sha256=resolved.freeze_id,
        owner_sha256=owner.owner_sha256,
        synthetic_resolved_freeze=True,
        decoder_batch_cw_sizes=DECODER_BATCH_CW_SIZES,
        bps_pairs=BPS_PAIRS,
        b2_view_count=10,
        required_slices=REQUIRED_SLICES,
    )


def run_engineering_benchmark(
    contract: D0OwnerIdentityAuthority,
    freeze: ResolvedDevFreeze,
    *,
    worker: Any,
    output: str | Path,
    root_seed: int = ENGINEERING_ROOT_SEED,
) -> EngineeringBenchmarkRun:
    """Execute only the injected I16 unit slices and land representative I/O."""

    manifest = _manifest(contract, freeze, root_seed=root_seed)

    decode = _worker_method(worker, "decoder_batch")
    decoder_slices = []
    for size in DECODER_BATCH_CW_SIZES:
        result = decode(size, resolved_freeze=freeze)
        if (
            not isinstance(result, Mapping)
            or result.get("cw_batch") != size
            or result.get("fresh_restart") is not True
        ):
            raise BenchmarkError("decoder batch must bind its size and a fresh restart")
        decoder_slices.append(
            DecoderBatchSlice(
                size,
                True,
                hashlib.sha256(_exact_bytes(result, "decoder_batch")).hexdigest(),
            )
        )

    waveform = _worker_method(worker, "build_waveform")(root_seed=root_seed)
    waveform_bytes = _exact_bytes(waveform, "build_waveform")
    waveform_sha256 = hashlib.sha256(waveform_bytes).hexdigest()
    run_bps = _worker_method(worker, "bps_pair")
    bps_slices = tuple(
        BpsSlice(
            pair=(B, Nw),
            waveform_sha256=waveform_sha256,
            result_sha256=hashlib.sha256(
                _exact_bytes(run_bps(waveform, B=B, Nw=Nw), "bps_pair")
            ).hexdigest(),
        )
        for B, Nw in BPS_PAIRS
    )

    run_b2_view = _worker_method(worker, "b2_view")
    b2_hashes = tuple(
        hashlib.sha256(
            _exact_bytes(
                run_b2_view(index, resolved_freeze=freeze),
                "b2_view",
            )
        ).hexdigest()
        for index in range(10)
    )
    if len(set(b2_hashes)) != 10:
        raise BenchmarkError("B2 slice requires ten unique polarization views")

    scores_value = _worker_method(worker, "hmm_primitive_scores")(
        resolved_freeze=freeze
    )
    if type(scores_value) not in (tuple, list):
        raise BenchmarkError("HMM primitive scores must be a finite float sequence")
    primitive_scores = tuple(scores_value)
    aggregate = exact_binary64_aggregate(primitive_scores)
    primitive_bytes = canonical_json_bytes({
        "primitive_scores_float_hex": [value.hex() for value in primitive_scores]
    })
    hmm = HmmSlice(
        primitive_scores=primitive_scores,
        primitive_count=len(primitive_scores),
        aggregate=aggregate,
        primitive_sha256=hashlib.sha256(primitive_bytes).hexdigest(),
    )

    rows = _worker_method(worker, "atomic_rows")()
    if not isinstance(rows, Sequence) or not rows:
        raise BenchmarkError("atomic I/O slice requires representative rows")
    atomic_receipt = write_jsonl_atomic(
        output,
        rows,
        sort_key="record_id",
        logical_name=Path(output).name,
    )
    return EngineeringBenchmarkRun(
        manifest=manifest,
        decoder_batches=tuple(decoder_slices),
        bps_slices=bps_slices,
        b2_view_sha256=b2_hashes,
        hmm=hmm,
        atomic_io=atomic_receipt,
    )


def _owner_path() -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "projects"
        / "thesis-fso"
        / "coded-decoder-feedback-groundwork"
        / "d0-defect-smoke-contract.yaml"
    )


def _synthetic_engineering_freeze(
    owner: D0OwnerIdentityAuthority, *, root_seed: int
) -> ResolvedDevFreeze:
    parameters = {
        "schema": "coded_decoder_feedback.d0.synthetic_engineering_freeze.v1",
        "owner_sha256": owner.owner_sha256,
        "root_seed": root_seed,
        "synthetic_engineering_only": True,
    }
    freeze_id = hashlib.sha256(canonical_json_bytes(parameters)).hexdigest()
    return ResolvedDevFreeze(
        freeze_id,
        parameters,
        {"owner_sha256": owner.owner_sha256},
    )


def _array_sha256(value: Any) -> str:
    array = np.ascontiguousarray(np.asarray(value))
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


def _hmm_output_sha256(scores: Any) -> str:
    values = np.asarray(scores, dtype=np.float64).reshape(-1)
    return hashlib.sha256(canonical_json_bytes({
        "scores_float64_hex": [float(value).hex() for value in values]
    })).hexdigest()


def _vectorized_hmm_posteriors(
    query_time: int,
    pilot_times: np.ndarray,
    observed: np.ndarray,
    known: np.ndarray,
    *,
    p_s: float,
    mu: float,
    n0_hat_cplx: float,
    checkpoint_chunk_size: int,
) -> np.ndarray:
    """NumPy-equivalent production formula, batched only over independent trajectories."""

    times = np.asarray(pilot_times, dtype=np.int64)
    observations = np.asarray(observed, dtype=np.complex128)
    symbols = np.asarray(known, dtype=np.complex128)
    if observations.ndim != 2 or symbols.shape != observations.shape:
        raise BenchmarkError("batched HMM inputs must be aligned trajectory matrices")
    if observations.shape[1] != times.size:
        raise BenchmarkError("batched HMM pilot axis differs from pilot times")
    if type(checkpoint_chunk_size) is not int or checkpoint_chunk_size <= 0:
        raise BenchmarkError("checkpoint chunk size must be a positive integer")
    nodes = [(int(value), index) for index, value in enumerate(times)]
    nodes.append((int(query_time), -1))
    nodes.sort(key=lambda item: item[0])
    query_index = next(index for index, (_, source) in enumerate(nodes) if source == -1)
    node_by_source = {source: index for index, (_, source) in enumerate(nodes) if source >= 0}
    emissions = np.zeros((observations.shape[0], len(nodes), 4), dtype=np.float64)
    for start in range(0, times.size, checkpoint_chunk_size):
        stop = min(times.size, start + checkpoint_chunk_size)
        destinations = [node_by_source[index] for index in range(start, stop)]
        for state in range(4):
            emissions[:, destinations, state] = b2_module.emission_log_weight(
                observations[:, start:stop], state=state, x=symbols[:, start:stop],
                mu=mu, n0_hat_cplx=n0_hat_cplx,
            )
    alpha = np.full_like(emissions, -np.inf)
    alpha[:, 0, :] = math.log(0.25) + emissions[:, 0, :]
    alpha[:, 0, :] -= b2_module._logsumexp(alpha[:, 0, :], axis=1)[:, None]
    for index in range(1, len(nodes)):
        distance = nodes[index][0] - nodes[index - 1][0]
        transition = b2_module.log_transition_matrix(p_s, distance=distance)
        alpha[:, index, :] = emissions[:, index, :] + b2_module._logsumexp(
            alpha[:, index - 1, :, None] + transition[None, :, :], axis=1
        )
        alpha[:, index, :] -= b2_module._logsumexp(alpha[:, index, :], axis=1)[:, None]
    beta = np.zeros_like(emissions)
    for index in range(len(nodes) - 2, -1, -1):
        distance = nodes[index + 1][0] - nodes[index][0]
        transition = b2_module.log_transition_matrix(p_s, distance=distance)
        beta[:, index, :] = b2_module._logsumexp(
            transition[None, :, :]
            + emissions[:, index + 1, None, :]
            + beta[:, index + 1, None, :],
            axis=2,
        )
        beta[:, index, :] -= b2_module._logsumexp(beta[:, index, :], axis=1)[:, None]
    log_posterior = alpha[:, query_index, :] + beta[:, query_index, :]
    log_posterior -= b2_module._logsumexp(log_posterior, axis=1)[:, None]
    return np.exp(log_posterior)


def _hmm_scores_from_posteriors(posteriors: np.ndarray) -> np.ndarray:
    values = np.asarray(posteriors, dtype=np.float64)
    active = values > 0.0
    terms = np.zeros_like(values)
    terms[active] = values[active] * np.log(values[active])
    return np.sum(terms, axis=1)


class _RealEngineeringWorker:
    """Small production-kernel slices used only by the authorized benchmark."""

    def __init__(self, owner: D0OwnerIdentityAuthority, *, root_seed: int) -> None:
        simulation_root = str(Path(__file__).resolve().parents[2])
        inserted = simulation_root not in sys.path
        if inserted:
            sys.path.insert(0, simulation_root)
        try:
            self._receiver = importlib.import_module("receiver")
            self._waveform = waveform_module
        finally:
            if inserted:
                sys.path.remove(simulation_root)
        self._codec = codec_module.D0Codec(owner.contract)
        setup_started = time.monotonic()
        self._codec._ensure_backend()
        self.setup_seconds = time.monotonic() - setup_started
        self._root_seed = root_seed
        self._rows: list[dict[str, Any]] = []
        self._waveform_document: Mapping[str, Any] | None = None
        self._waveform_build: Any | None = None
        self._waveform_samples: np.ndarray | None = None
        self.physical_api_invocations = 0
        self.decoder_seconds = 0.0
        self.bps_seconds = 0.0
        self.b2_seconds = 0.0
        self.hmm_seconds = 0.0
        self.hmm_trajectory_units = 0
        self.cache_hits = 0
        self.adjustment_receipts: tuple[EngineeringAdjustmentReceipt, ...] = ()
        self.hmm_best_seconds_per_trajectory = 0.0
        self.hmm_best_output_sha256 = ""
        self.selected_adjustment_name = ""

    def decoder_batch(self, cw_batch: int, *, resolved_freeze: ResolvedDevFreeze):
        started = time.monotonic()
        backend = self._codec._ensure_backend()
        llr = np.full((cw_batch, 1536), 8.0, dtype=np.float32)
        decoded = np.asarray(
            backend.decode(llr, message_state=None, warm_state=None), dtype=np.uint8
        )
        elapsed = time.monotonic() - started
        if decoded.shape != (cw_batch, 1024):
            raise BenchmarkError("live decoder returned the wrong engineering batch shape")
        result_sha256 = _array_sha256(decoded)
        self.decoder_seconds += elapsed
        self.physical_api_invocations += 1
        self._rows.append({
            "record_id": f"decoder-{cw_batch:02d}",
            "kind": "decoder",
            "cw_batch": cw_batch,
            "fresh_restart": True,
            "result_sha256": result_sha256,
            "elapsed_seconds": elapsed,
            "dev_freeze_sha256": resolved_freeze.freeze_id,
        })
        return {
            "cw_batch": cw_batch,
            "fresh_restart": True,
            "result_sha256": result_sha256,
        }

    def build_waveform(self, *, root_seed: int):
        if root_seed != self._root_seed:
            raise BenchmarkError("waveform root seed differs from the engineering manifest")
        generator = np.random.Generator(np.random.PCG64(root_seed))
        bits = generator.integers(0, 2, size=(2, 6144, 4), dtype=np.uint8)
        data_symbols = np.asarray(
            codec_module.gray16_map(bits), dtype=np.complex128
        )
        build = self._waveform.build_waveform(data_symbols, N=10)
        samples = np.asarray(build.waveform, dtype=np.complex128)
        pilot_count = int(np.count_nonzero(build.known_mask[32:]))
        document = {
            "schema": "coded_decoder_feedback.d0.engineering_waveform.v1",
            "root_seed": root_seed,
            "data_symbols_per_polarization": 6144,
            "prefix_symbols_per_polarization": 32,
            "periodic_pilot_symbols_per_polarization": pilot_count,
            "sample_count_per_polarization": int(samples.shape[1]),
            "samples_sha256": _array_sha256(samples),
        }
        self._waveform_document = document
        self._waveform_build = build
        self._waveform_samples = samples
        return document

    def bps_pair(self, waveform: Mapping[str, Any], *, B: int, Nw: int):
        if waveform is not self._waveform_document or self._waveform_samples is None:
            raise BenchmarkError("BPS slices must reuse the one materialized waveform")
        started = time.monotonic()
        results = tuple(
            self._receiver.run_common_bps(
                self._waveform_samples[pol_index], B=B, Nw=Nw
            )
            for pol_index in range(2)
        )
        elapsed = time.monotonic() - started
        result_sha256 = hashlib.sha256(
            canonical_json_bytes({
                "samples_sha256_by_polarization": tuple(
                    _array_sha256(result.samples) for result in results
                ),
                "phase_sha256_by_polarization": tuple(
                    _array_sha256(result.phase_trace) for result in results
                ),
                "receipt_by_polarization": tuple(
                    dict(result.receipt) for result in results
                ),
            })
        ).hexdigest()
        self.bps_seconds += elapsed
        self.physical_api_invocations += len(results)
        self.cache_hits = getattr(self, "cache_hits", 0)
        self._rows.append({
            "record_id": f"bps-{B:02d}-{Nw:03d}",
            "kind": "bps",
            "B": B,
            "Nw": Nw,
            "waveform_sha256": waveform["samples_sha256"],
            "result_sha256": result_sha256,
            "elapsed_seconds": elapsed,
            "input_shape_by_polarization": tuple(
                int(self._waveform_samples.shape[1]) for _ in range(2)
            ),
            "production_api_invocations": len(results),
        })
        return {"B": B, "Nw": Nw, "result_sha256": result_sha256}

    def b2_view(self, view_index: int, *, resolved_freeze: ResolvedDevFreeze):
        if self._waveform_samples is None or self._waveform_build is None:
            raise BenchmarkError("B2 slice requires the engineering waveform")
        started = time.monotonic()
        observations = np.asarray(
            self._waveform_samples[:, self._waveform_build.data_to_time]
            * np.exp(0.017j * view_index)
            + complex(0.001 * view_index, -0.0005 * view_index),
            dtype=np.complex128,
        )
        weights = np.array(
            [1.0 + view_index, 2.0, 3.0, 4.0], dtype=np.float64
        )
        posterior = np.broadcast_to(
            weights / weights.sum(), (2, 6144, 4)
        ).copy()
        cw_ids = tuple(
            tuple(
                f"engineering-b2-{view_index:02d}-{pol_name}-{cw_index:02d}"
                for cw_index in range(16)
            )
            for pol_name in ("X", "Y")
        )
        result = b2_module.run_b2(
            observations,
            posterior,
            codec=self._codec,
            cw_ids_by_polarization=cw_ids,
            mu=0.98,
            n0_hat_cplx=0.05,
            candidate_id=f"engineering-b2-{view_index:02d}",
        )
        elapsed = time.monotonic() - started
        result_sha256 = hashlib.sha256(canonical_json_bytes({
            "llr_sha256": _array_sha256(result.llr_by_polarization),
            "decode_sha256_by_polarization": tuple(
                _array_sha256(batch.info_bits) for batch in result.decode_batches
            ),
        })).hexdigest()
        self.b2_seconds += elapsed
        self.physical_api_invocations += 3
        self._rows.append({
            "record_id": f"b2-{view_index:02d}",
            "kind": "b2",
            "view_index": view_index,
            "result_sha256": result_sha256,
            "elapsed_seconds": elapsed,
            "dev_freeze_sha256": resolved_freeze.freeze_id,
            "samples_shape": (2, 6144),
            "posterior_shape": (2, 6144, 4),
            "cw_ids_per_polarization": 16,
            "fresh_decodes_per_polarization": 1,
        })
        return {
            "view_index": view_index,
            "result_sha256": result_sha256,
            "dev_freeze_sha256": resolved_freeze.freeze_id,
        }

    def hmm_primitive_scores(self, *, resolved_freeze: ResolvedDevFreeze):
        if self._waveform_samples is None or self._waveform_build is None:
            raise BenchmarkError("HMM slice requires the engineering waveform")
        pilot_times = np.flatnonzero(self._waveform_build.known_mask)[32:]
        query_time = int(self._waveform_build.data_to_time[0])
        known = np.asarray(
            self._waveform_build.known_symbols[:, pilot_times], dtype=np.complex128
        )
        observed = np.asarray(
            self._waveform_samples[:, pilot_times]
            * np.exp(0.03j * np.arange(1, 3, dtype=np.float64))[:, None],
            dtype=np.complex128,
        )

        def scalar_once() -> np.ndarray:
            result = []
            for pol_index in range(observed.shape[0]):
                posterior = b2_module.pilot_state_posterior(
                    query_time, pilot_times, observed[pol_index], known[pol_index],
                    M=int(pilot_times.size), p_s=0.01, mu=0.98,
                    n0_hat_cplx=0.05,
                )
                result.append(_hmm_scores_from_posteriors(posterior[None, :])[0])
            return np.asarray(result, dtype=np.float64)

        def measured(operation, repeats: int) -> tuple[np.ndarray, float, int]:
            started = time.perf_counter()
            output = None
            for _ in range(repeats):
                output = operation()
            return np.asarray(output), time.perf_counter() - started, repeats * 2

        scalar, scalar_elapsed, scalar_units = measured(
            scalar_once, HMM_MEASUREMENT_REPEATS
        )
        full_chunk = int(pilot_times.size)

        def vector_once(batch_size: int, chunk_size: int) -> np.ndarray:
            parts = []
            for start in range(0, observed.shape[0], batch_size):
                posterior = _vectorized_hmm_posteriors(
                    query_time, pilot_times, observed[start:start + batch_size],
                    known[start:start + batch_size], p_s=0.01, mu=0.98,
                    n0_hat_cplx=0.05, checkpoint_chunk_size=chunk_size,
                )
                parts.append(_hmm_scores_from_posteriors(posterior))
            return np.concatenate(parts)

        vector, vector_elapsed, vector_units = measured(
            lambda: vector_once(1, full_chunk), HMM_MEASUREMENT_REPEATS
        )
        batch_candidates = []
        for size in (1, 2):
            output, elapsed, units = measured(
                lambda size=size: vector_once(size, full_chunk),
                HMM_MEASUREMENT_REPEATS,
            )
            batch_candidates.append((elapsed / units, size, output, elapsed, units))
        _, best_batch, batch_output, batch_elapsed, batch_units = min(batch_candidates)
        chunk_candidates = []
        for size in (32, 128, full_chunk):
            output, elapsed, units = measured(
                lambda size=size: vector_once(best_batch, size),
                HMM_MEASUREMENT_REPEATS,
            )
            chunk_candidates.append((elapsed / units, size, output, elapsed, units))
        _, best_chunk, chunk_output, chunk_elapsed, chunk_units = min(chunk_candidates)

        content_keys = tuple(
            hashlib.sha256(
                np.ascontiguousarray(np.concatenate((observed[index], known[index]))).tobytes()
                + np.ascontiguousarray(pilot_times).tobytes()
                + canonical_json_bytes({"query_time": query_time, "p_s": 0.01, "mu": 0.98,
                                        "n0_hat_cplx": 0.05})
            ).hexdigest()
            for index in range(2)
        )
        cache: dict[str, float] = {}
        cache_scores = []
        cache_reads = 0
        cache_compute_units = 0
        cache_started = time.perf_counter()
        for index, key in enumerate(content_keys):
            if key in cache:
                cache_reads += 1
            else:
                miss_output = vector_once(1, best_chunk)
                cache_compute_units += int(miss_output.size)
                cache[key] = float(miss_output[index])
            cache_scores.append(cache[key])
        cache_elapsed = time.perf_counter() - cache_started
        cache_output = np.asarray(cache_scores, dtype=np.float64)

        projection = build_full_work_projection()
        before_materialized = dict(projection.materialized_counts)
        after_materialized = dict(before_materialized)
        before_digest = _hmm_output_sha256(scalar)

        def receipt(name: str, config: Mapping[str, Any], output: np.ndarray,
                    elapsed: float, units: int, *, cache_reads_value: int = 0,
                    applicability: str = "APPLICABLE",
                    source: str = "kernel scheduling changed; materialized unit counts unchanged"):
            error = float(np.max(np.abs(np.asarray(output) - scalar)))
            return EngineeringAdjustmentReceipt(
                name=name, applicability=applicability,
                config=MappingProxyType(dict(config)),
                before_elapsed_seconds=scalar_elapsed,
                after_elapsed_seconds=elapsed,
                before_unit_count=scalar_units, after_unit_count=units,
                before_output_sha256=before_digest,
                after_output_sha256=_hmm_output_sha256(output),
                actual_cache_reads=cache_reads_value,
                logical_manifest_sha256_before=projection.logical_manifest_sha256,
                logical_manifest_sha256_after=projection.logical_manifest_sha256,
                materialized_projection_before=MappingProxyType(dict(before_materialized)),
                materialized_projection_after=MappingProxyType(dict(after_materialized)),
                materialized_projection_change_source=source,
                output_equivalent_to_scalar=bool(np.allclose(
                    output, scalar, rtol=0.0, atol=HMM_STRICT_ATOL
                )),
                max_abs_error=error,
            )

        self.adjustment_receipts = (
            receipt("vectorization", {"backend": "numpy", "batch_size": 1,
                    "checkpoint_chunk_size": full_chunk}, vector,
                    vector_elapsed, vector_units),
            receipt("batch_size", {"candidates": [1, 2], "selected": best_batch,
                    "candidate_seconds_per_unit": {
                        str(size): elapsed / units
                        for _rate, size, _output, elapsed, units in batch_candidates
                    }}, batch_output, batch_elapsed, batch_units),
            receipt("content_addressed_cache", {
                    "key_schema": "exact_observed_known_times_and_parameters_sha256",
                    "distinct_content_count": len(set(content_keys)),
                    "actual_miss_compute_units": cache_compute_units,
                    "trajectory_count": len(content_keys)}, cache_output,
                    cache_elapsed, cache_compute_units, cache_reads_value=cache_reads,
                    applicability=("APPLICABLE" if cache_reads else "NOT_APPLICABLE"),
                    source=("exact repeated content only" if cache_reads else
                            "no exact repeated owner trajectory content; zero materialized change")),
            receipt("checkpoint_chunk_size", {
                    "candidates": [32, 128, full_chunk], "selected": best_chunk,
                    "candidate_seconds_per_unit": {
                        str(size): elapsed / units
                        for _rate, size, _output, elapsed, units in chunk_candidates
                    }}, chunk_output, chunk_elapsed, chunk_units),
        )
        if not all(item.output_equivalent_to_scalar for item in self.adjustment_receipts):
            raise BenchmarkError("allowed HMM adjustment output differs from scalar reference")
        applicable = [item for item in self.adjustment_receipts if item.applicability == "APPLICABLE"]
        selected = min(applicable, key=lambda item: item.after_elapsed_seconds / item.after_unit_count)
        self.selected_adjustment_name = selected.name
        self.hmm_best_seconds_per_trajectory = (
            selected.after_elapsed_seconds / selected.after_unit_count
        )
        self.hmm_best_output_sha256 = selected.after_output_sha256
        scores = tuple(float(value) for value in scalar)
        elapsed = scalar_elapsed / HMM_MEASUREMENT_REPEATS
        aggregate = exact_binary64_aggregate(scores)
        self.hmm_seconds += elapsed
        self.hmm_trajectory_units = getattr(self, "hmm_trajectory_units", 0) + len(scores)
        self.cache_hits += cache_reads
        self.physical_api_invocations += scalar_units + vector_units + sum(
            item[4] for item in batch_candidates
        ) + sum(item[4] for item in chunk_candidates) + cache_compute_units
        self._rows.append({
            "record_id": "hmm-00",
            "kind": "hmm",
            "primitive_count": len(scores),
            "aggregate_count": aggregate.count,
            "aggregate_numerator_decimal": aggregate.numerator_decimal,
            "aggregate_denominator_power2": aggregate.denominator_power2,
            "elapsed_seconds": elapsed,
            "dev_freeze_sha256": resolved_freeze.freeze_id,
            "polarization_trajectory_count": len(scores),
            "pilot_count_per_trajectory": int(pilot_times.size),
            "parameter_pair": {"p_s": 0.01, "mu": 0.98, "n0_hat_cplx": 0.05},
            "allowed_adjustments": [item.name for item in self.adjustment_receipts],
            "best_seconds_per_trajectory": self.hmm_best_seconds_per_trajectory,
        })
        for item in self.adjustment_receipts:
            self._rows.append({
                "record_id": f"hmm-adjustment-{item.name}",
                "kind": "hmm_adjustment",
                **_adjustment_receipt_document(item),
            })
        return scores

    def atomic_rows(self):
        return tuple(self._rows)

    def projected_compute_seconds(self, atomic_elapsed_seconds: float) -> float:
        decoder_per_cw = self.decoder_seconds / math.fsum(DECODER_BATCH_CW_SIZES)
        bps_per_waveform_grid = self.bps_seconds
        b2_per_view = self.b2_seconds / 10.0
        if self.hmm_trajectory_units <= 0:
            raise BenchmarkError("HMM projection requires measured trajectory units")
        hmm_per_primitive = (
            self.hmm_best_seconds_per_trajectory
            if self.hmm_best_seconds_per_trajectory > 0.0
            else self.hmm_seconds / self.hmm_trajectory_units
        )
        io_per_row = atomic_elapsed_seconds / max(1, len(self._rows))
        return math.fsum((
            self.setup_seconds,
            decoder_per_cw * FROZEN_MATERIALIZED_COUNTS["cw_decodes"],
            bps_per_waveform_grid * 480,
            b2_per_view * 11_400,
            hmm_per_primitive
            * FROZEN_MATERIALIZED_COUNTS[
                "hmm_primitive_pol_trajectory_parameter_pair_scores"
            ],
            io_per_row * 50_287,
        ))


def _dependency_versions(worker: _RealEngineeringWorker) -> dict[str, str]:
    metadata = worker._codec.live_metadata
    try:
        import torch
        torch_version = str(torch.__version__)
    except ImportError:
        torch_version = "unavailable"
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "sionna": metadata.sionna_version,
        "torch": torch_version,
    }


def _process_rss_peak_bytes() -> int:
    """Return the operating-system process peak, including native allocations."""

    if sys.platform == "win32":
        class ProcessMemoryCounters(ctypes.Structure):
            _fields_ = (
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
                ("PrivateUsage", ctypes.c_size_t),
            )

        counters = ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        get_current_process = ctypes.windll.kernel32.GetCurrentProcess
        get_current_process.restype = ctypes.c_void_p
        get_process_memory_info = ctypes.windll.psapi.GetProcessMemoryInfo
        get_process_memory_info.argtypes = (
            ctypes.c_void_p,
            ctypes.POINTER(ProcessMemoryCounters),
            ctypes.c_ulong,
        )
        get_process_memory_info.restype = ctypes.c_int
        handle = get_current_process()
        ok = get_process_memory_info(
            handle, ctypes.byref(counters), counters.cb
        )
        if not ok:
            raise BenchmarkError("GetProcessMemoryInfo failed")
        return int(counters.PeakWorkingSetSize)

    import resource

    peak = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform != "darwin":
        peak *= 1024
    return peak


def _measure_peak_memory(operation):
    """Execute one slice while recording process RSS and applicable device peak."""

    if not callable(operation):
        raise TypeError("operation must be callable")
    accelerator_backend = "not_applicable"
    accelerator_peak: int | None = None
    torch_module = None
    try:
        import torch

        if torch.cuda.is_available():
            torch_module = torch
            accelerator_backend = "torch.cuda"
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
    except (ImportError, RuntimeError):
        torch_module = None

    value = operation()
    process_peak = _process_rss_peak_bytes()
    if torch_module is not None:
        torch_module.cuda.synchronize()
        accelerator_peak = int(torch_module.cuda.max_memory_allocated())
    return value, {
        "process_rss_peak_bytes": process_peak,
        "accelerator_backend": accelerator_backend,
        "accelerator_peak_bytes": accelerator_peak,
    }


def _run_authorized_operation(*, output: str, root_seed: int, watchdog_seconds: int):
    owner = load_owner_identity_authority(_owner_path())
    resolved = _synthetic_engineering_freeze(owner, root_seed=root_seed)
    worker = _RealEngineeringWorker(owner, root_seed=root_seed)
    output_root = Path(output)
    slice_path = output_root / "engineering-slices.jsonl"
    receipt_path = output_root / "benchmark-receipt.jsonl"
    def measured_operation():
        started = time.monotonic()
        measured_run = run_engineering_benchmark(
            owner,
            resolved,
            worker=worker,
            output=slice_path,
            root_seed=root_seed,
        )
        return measured_run, time.monotonic() - started

    (run, elapsed), peak_memory = _measure_peak_memory(measured_operation)
    projected_compute_seconds = worker.projected_compute_seconds(elapsed)
    completed_ids = tuple(D0_WORK_DAYS)[:-1]
    remaining_id = tuple(D0_WORK_DAYS)[-1]
    consumed = {name: D0_WORK_DAYS[name] for name in completed_ids}
    remaining = {remaining_id: projected_compute_seconds / 86_400.0}
    projected_d0_days = math.fsum(consumed.values()) + math.fsum(remaining.values())
    engineering_record = {
        "device": platform.platform(),
        "dependency_versions": _dependency_versions(worker),
        "physical_api_invocations": worker.physical_api_invocations,
        "logical_batches": len(run.decoder_batches),
        "cache_hits": worker.cache_hits,
        "wall_time": elapsed,
        "peak_memory": peak_memory,
        "projected_full_D0_time": projected_d0_days * 86_400.0,
    }
    receipt = build_benchmark_receipt(
        run,
        owner_authority=owner,
        engineering_record=engineering_record,
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=elapsed,
        watchdog_seconds=watchdog_seconds,
        adjustment_receipts=worker.adjustment_receipts,
        selected_adjustment_name=worker.selected_adjustment_name,
        selected_hmm_seconds_per_trajectory=worker.hmm_best_seconds_per_trajectory,
    )
    landed = write_benchmark_receipt(receipt_path, receipt)
    return {
        "status": receipt.status,
        "slice_counts": {
            "decoder_batches": len(run.decoder_batches),
            "bps_pairs": len(run.bps_slices),
            "b2_views": len(run.b2_view_sha256),
            "hmm_primitive_aggregate": 1,
            "atomic_jsonl": 1,
            "atomic_receipt": 1,
        },
        "slice_sha256": run.atomic_io.sha256,
        "receipt_sha256": landed.sha256,
        "owner_sha256": owner.owner_sha256,
        "elapsed_seconds": elapsed,
    }


def _run_authorized_cli(args: argparse.Namespace) -> int:
    operation = partial(
        _run_authorized_operation,
        output=str(args.output),
        root_seed=args.root_seed,
        watchdog_seconds=args.watchdog_seconds,
    )
    result = watchdog_call(operation, watchdog_seconds=args.watchdog_seconds)
    if result.status != "COMPLETE" or not isinstance(result.value, Mapping):
        print(canonical_json_bytes({
            "status": "INCOMPLETE",
            "elapsed_seconds": result.elapsed_seconds,
            "watchdog_seconds": args.watchdog_seconds,
        }).decode("utf-8"))
        return 1
    document = dict(result.value)
    print(canonical_json_bytes(document).decode("utf-8"))
    if document.get("status") == "ENGINEERING_THROUGHPUT_PASS":
        return 0
    if document.get("status") == "GREATER_THAN_7D_HARD_BLOCKER":
        return 2
    return 1


__all__ = [
    "BPS_PAIRS",
    "DECODER_BATCH_CW_SIZES",
    "ENGINEERING_ROOT_SEED",
    "REQUIRED_SLICES",
    "BenchmarkError",
    "BenchmarkFreezeBinding",
    "BenchmarkReceipt",
    "EngineeringBenchmarkRun",
    "EngineeringManifest",
    "FullWorkProjection",
    "WatchdogResult",
    "apply_engineering_adjustments",
    "bind_resolved_freeze",
    "benchmark_receipt_document",
    "build_benchmark_receipt",
    "build_cli_parser",
    "build_full_work_projection",
    "main",
    "parse_cli_args",
    "run_engineering_benchmark",
    "watchdog_call",
    "write_benchmark_receipt",
]


if __name__ == "__main__":
    raise SystemExit(main())
