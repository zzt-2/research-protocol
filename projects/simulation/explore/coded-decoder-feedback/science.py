"""Minimal checkpointable runner for frozen D0 S1 natural occurrence only."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np

SIMULATION_ROOT = Path(__file__).resolve().parents[2]
LOCAL_D0_ROOT = Path(__file__).resolve().parent
for module_root in (LOCAL_D0_ROOT, SIMULATION_ROOT):
    try:
        sys.path.remove(str(module_root))
    except ValueError:
        pass
sys.path.insert(0, str(LOCAL_D0_ROOT))
sys.path.insert(1, str(SIMULATION_ROOT))

import artifacts
import channel
import codec
import contract as contract_module
import receiver
import schemas
import statistics
import waveform
import methods
import verify


D0_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONTRACT_PATH = (
    D0_ROOT / "projects" / "thesis-fso" / "coded-decoder-feedback-groundwork"
    / "d0-defect-smoke-contract.yaml"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "artifacts" / "science" / "s1-natural-occurrence"
_ROW_KEY = ("record_type", "seed", "cell_id", "target_polarization")
S2_FIXTURES = (
    ("B04_K1", 4, 1), ("B04_K2", 4, 2), ("B04_K3", 4, 3),
    ("B08_K1", 8, 1), ("B08_K2", 8, 2), ("B08_K3", 8, 3),
    ("B12_K1", 12, 1), ("B12_K2", 12, 2), ("B12_K3", 12, 3),
)


def load_science_contract(path: str | os.PathLike[str]) -> contract_module.D0Contract:
    return contract_module.load_contract(path)


def s1_plan(owner: contract_module.D0Contract, *, extent: str) -> tuple[tuple[int, contract_module.PhysicalCell], ...]:
    if extent != "FIRST_STAGE":
        raise ValueError("S1 extent must be FIRST_STAGE")
    return tuple(
        (seed, cell)
        for seed in owner.seed_registry.first_stage_natural.values
        for cell in owner.population_manifest
    )


def s2_plan(owner: contract_module.D0Contract) -> tuple[tuple[int, str, str], ...]:
    seeds = owner.seed_registry.range_for("controlled_damage_recovery").values
    return tuple((seed, cell, pol) for seed in seeds
                 for cell in ("hard", "mid", "clean")
                 for pol in owner.population.polarizations)


def _nearest_quarter_turn_state(residual: np.ndarray) -> np.ndarray:
    candidates = np.arange(4, dtype=np.float64) * (np.pi / 2.0)
    wrapped = np.angle(np.exp(1j * (residual[:, None] - candidates[None, :])))
    return np.argmin(np.abs(wrapped), axis=1).astype(np.int8)


def persistent_transition_boundaries(residual: np.ndarray) -> tuple[int, ...]:
    value = np.asarray(residual, dtype=np.float64)
    if value.ndim != 1 or not np.all(np.isfinite(value)):
        raise ValueError("residual must be a finite one-dimensional phase trace")
    states = _nearest_quarter_turn_state(value)
    candidates: list[int] = []
    for boundary in np.flatnonzero(states[1:] != states[:-1]) + 1:
        boundary = int(boundary)
        if boundary < 32 or boundary + 32 > states.size:
            continue
        left_state, right_state = int(states[boundary - 1]), int(states[boundary])
        if left_state == right_state:
            continue
        if (np.count_nonzero(states[boundary - 32:boundary] == left_state) >= 28
                and np.count_nonzero(states[boundary:boundary + 32] == right_state) >= 28):
            candidates.append(boundary)
    merged: list[int] = []
    for boundary in candidates:
        if not merged or boundary - merged[-1] > 32:
            merged.append(boundary)
    return tuple(merged)


def detect_persistent_transitions(true_phase: np.ndarray, common_cpr_phase: np.ndarray) -> tuple[int, ...]:
    truth = np.asarray(true_phase, dtype=np.float64)
    estimate = np.asarray(common_cpr_phase, dtype=np.float64)
    if truth.ndim != 1 or estimate.shape != truth.shape:
        raise ValueError("true/common phase traces must have the same one-dimensional shape")
    return persistent_transition_boundaries(truth - estimate)


def _canonical_line(row: Mapping[str, Any]) -> bytes:
    return artifacts.canonical_json_bytes(dict(row)) + b"\n"


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".tmp.{os.getpid()}")
    with temp.open("wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    for attempt in range(100):
        try:
            os.replace(temp, path)
            break
        except PermissionError:
            if attempt == 99:
                raise
            time.sleep(0.05)


def load_checkpoint_rows(path: str | os.PathLike[str], *,
                         key_fields: Sequence[str] = _ROW_KEY) -> tuple[dict[str, Any], ...]:
    target = Path(path)
    if not target.exists():
        return ()
    rows = tuple(json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line)
    by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(row[name] for name in key_fields)
        if key in by_key and by_key[key] != row:
            raise ValueError("conflicting checkpoint row")
        by_key[key] = row
    return tuple(by_key[key] for key in sorted(by_key))


def append_checkpoint_frame(path: str | os.PathLike[str], frame_rows: Sequence[Mapping[str, Any]], *,
                            key_fields: Sequence[str] = _ROW_KEY) -> None:
    target = Path(path)
    existing = {tuple(row[name] for name in key_fields): row
                for row in load_checkpoint_rows(target, key_fields=key_fields)}
    for source in frame_rows:
        row = dict(source)
        key = tuple(row[name] for name in key_fields)
        if key in existing and existing[key] != row:
            raise ValueError("conflicting checkpoint row")
        existing[key] = row
    payload = b"".join(_canonical_line(existing[key]) for key in sorted(existing))
    _atomic_bytes(target, payload)


def typed_s1_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[schemas.S1TrajectoryRow, ...]:
    fields = schemas.TABLE_FIELDS["s1_trajectory"]
    return tuple(
        schemas.row_from_mapping("s1_trajectory", {name: row[name] for name in fields})
        for row in rows
    )


_S2_ROW_KEY = (
    "record_type", "seed", "cell_id", "target_polarization", "fixture_id",
    "jump_present", "method_id",
)
_S2_ARTIFACT_SORT_KEY = (
    "record_type", "seed", "cell_id", "target_polarization", "fixture_id",
    "projection_role", "method_id", "physical_case_id", "computation_id",
)


def typed_s2_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[schemas.S2MethodRow, ...]:
    fields = schemas.TABLE_FIELDS["s2_method"]
    return tuple(schemas.row_from_mapping("s2_method", {name: row[name] for name in fields})
                 for row in rows)


def _payload(seed: int, owner: contract_module.D0Contract, d0_codec: codec.D0Codec):
    streams = channel.spawn_named_streams(seed)
    information = np.stack((
        streams.payload_x.integers(0, 2, size=(16, 1024), dtype=np.uint8),
        streams.payload_y.integers(0, 2, size=(16, 1024), dtype=np.uint8),
    ))
    coded = d0_codec.encode(information.reshape(32, 1024)).reshape(2, 16, 1536)
    truth = contract_module.PayloadTruth(information, coded)
    data = codec.gray16_map(coded.reshape(2, 6144, 4))
    return truth, waveform.build_waveform(data, N=100), streams


def _run_frame(seed: int, cell: contract_module.PhysicalCell, owner: contract_module.D0Contract,
               built: waveform.WaveformBuild, streams: channel.NamedStreams) -> tuple[dict[str, Any], ...]:
    physical = channel.realize_supplied_waveform(
        built.waveform, streams=streams, snr_db=cell.snr_db,
        linewidth_hz=cell.linewidth_hz, symbol_rate_baud=owner.population.symbol_rate_baud,
    )
    rows = []
    for pol_index, pol in enumerate(owner.population.polarizations):
        calibration = receiver.estimate_prefix_calibration(
            physical.received[pol_index, :32], built.known_symbols[pol_index, :32]
        )
        equalized, _ = receiver.scalar_visible_power_equalize(
            physical.received[pol_index], c_pre_cplx=calibration.c_pre_cplx
        )
        bps = receiver.run_common_bps(equalized, B=32, Nw=31)
        boundaries = detect_persistent_transitions(physical.phase[pol_index], bps.phase_trace)
        receipt_payload = {
            "seed": seed, "cell_id": cell.cell_id, "polarization": pol,
            "true_phase_sha256": hashlib.sha256(physical.phase[pol_index].tobytes()).hexdigest(),
            "common_cpr_phase_sha256": hashlib.sha256(bps.phase_trace.tobytes()).hexdigest(),
            "event_definition": "persistent_quarter_turn_v1",
        }
        rows.append({
            "record_type": "S1_TRAJECTORY", "seed": seed, "cell_id": cell.cell_id,
            "target_polarization": pol, "persistent_transition_count": len(boundaries),
            "persistent_transition_after_symbol": list(boundaries),
            "event_present": bool(boundaries),
            "trajectory_receipt_sha256": hashlib.sha256(
                artifacts.canonical_json_bytes(receipt_payload)
            ).hexdigest(),
        })
    return tuple(rows)


def run_s1(*, contract_path: Path, output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    owner = load_science_contract(contract_path)
    plan = s1_plan(owner, extent="FIRST_STAGE")
    checkpoint = output / "checkpoint.jsonl"
    existing = load_checkpoint_rows(checkpoint)
    completed_frames = {(row["seed"], row["cell_id"]) for row in existing}
    resume_count = len(completed_frames)
    d0_codec = codec.D0Codec(owner)
    payload_cache: dict[int, tuple[Any, waveform.WaveformBuild]] = {}
    for seed, cell in plan:
        if (seed, cell.cell_id) in completed_frames:
            continue
        if seed not in payload_cache:
            truth, built, _ = _payload(seed, owner, d0_codec)
            payload_cache[seed] = (truth, built)
        _, built = payload_cache[seed]
        streams = channel.spawn_named_streams(seed)
        streams.payload_x.integers(0, 2, size=(16, 1024), dtype=np.uint8)
        streams.payload_y.integers(0, 2, size=(16, 1024), dtype=np.uint8)
        append_checkpoint_frame(checkpoint, _run_frame(seed, cell, owner, built, streams))
    mappings = load_checkpoint_rows(checkpoint)
    typed = typed_s1_rows(mappings)
    point = statistics.reduce_s1(typed)
    event_rows = tuple(row for row in typed if row.event_present)
    event_seeds = len({row.seed for row in event_rows})
    event_cells = len({row.cell_id for row in event_rows})
    verdict = "PASS" if point.event_count >= 12 and event_seeds >= 4 and event_cells >= 2 else "FAIL"
    output.mkdir(parents=True, exist_ok=True)
    raw_receipt = artifacts.write_jsonl_atomic(
        output / "s1-raw.jsonl", mappings, sort_key=_ROW_KEY, logical_name="s1-raw.jsonl"
    )
    summary = {
        "schema": "coded_decoder_feedback.d0.s1.summary.v1",
        "observed_trajectories": point.trajectory_count, "event_count": point.event_count,
        "event_rate": point.event_rate, "distinct_event_seed_clusters": event_seeds,
        "distinct_event_physical_cells": event_cells, "S1_VERDICT": verdict,
        "formal_science_disposition": (
            "S1_NATURAL_OCCURRENCE_ESTABLISHED" if verdict == "PASS"
            else "NATURAL_DEFECT_NOT_ESTABLISHED"
        ),
        "mission_method_delta": "NONE", "thesis_method_disposition": "NONE",
    }
    summary_bytes = artifacts.canonical_json_bytes(summary) + b"\n"
    _atomic_bytes(output / "summary.json", summary_bytes)
    source_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    contract_sha = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=D0_ROOT).decode().strip()
    receipt = {
        "schema": "coded_decoder_feedback.d0.s1.receipt.v1", "contract_sha256": contract_sha,
        "source_sha256": source_sha, "git_head": head, "seed_domain": [8100, 8119],
        "cell_domain": [cell.cell_id for cell in owner.population_manifest],
        "row_count": point.trajectory_count, "event_count": point.event_count,
        "event_rate": point.event_rate, "distinct_event_seed_clusters": event_seeds,
        "distinct_event_physical_cells": event_cells, "gate_verdict": verdict,
        "wall_time_seconds": None,
        "wall_time_status": "NOT_CAPTURED_ACROSS_PRE_REPAIR_RESUMES",
        "final_invocation_wall_time_seconds": time.perf_counter() - started,
        "resume_count": None,
        "resume_count_status": "NOT_PERSISTED_ACROSS_PRE_REPAIR_ATTEMPTS",
        "resumed_completed_frame_count": resume_count,
        "raw_sha256": raw_receipt.sha256,
        "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
    }
    _atomic_bytes(output / "receipt.json", artifacts.canonical_json_bytes(receipt) + b"\n")
    return {
        **summary,
        "wall_time_seconds": receipt["wall_time_seconds"],
        "final_invocation_wall_time_seconds": receipt["final_invocation_wall_time_seconds"],
    }


def _s2_alias_cells(owner: contract_module.D0Contract) -> dict[str, contract_module.PhysicalCell]:
    wanted = {"hard": (10, 80000), "mid": (14, 20000), "clean": (22, 10000)}
    return {alias: next(cell for cell in owner.population_manifest
                        if (cell.snr_db, cell.linewidth_hz) == identity)
            for alias, identity in wanted.items()}


def _science_resolved_freeze() -> contract_module.ResolvedDevFreeze:
    identity = "5" * 64
    return contract_module.ResolvedDevFreeze(
        identity,
        {"common_bps": ({"tuple_id": "M2_N100", "winner": {"B": 32, "Nw": 31}},),
         "final_b2_tuple": {"tuple_id": "M2_N100"}},
        {"dev_freeze_sha256": identity},
    )


def _deployment_seal(owner: contract_module.D0Contract,
                     receiver_view: contract_module.ReceiverView):
    resolved = _science_resolved_freeze()
    receipts = tuple({"phase": phase, "dev_freeze_sha256": resolved.freeze_id}
                     for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4"))
    return verify.DeploymentBoundary(verify.deployment_callable_registry()).seal(
        owner, receiver_view, resolved, phase="D0_UNIT_TEST", phase_receipts=receipts,
    )


def _result_hash(value: Any) -> str:
    return hashlib.sha256(np.ascontiguousarray(value.info_bits).tobytes()).hexdigest()


def _s2_row(*, seed: int, alias: str, pol: str, fixture_id: str, boundary: int,
            rotation: int, jump: bool, method_id: str, decoded: Any,
            truth_bits: np.ndarray, physical_case_id: str, computation_id: str,
            total_symbols: int) -> dict[str, Any]:
    errors = np.asarray(decoded.info_bits) != truth_bits
    affected = errors[boundary:]
    return {
        "record_type": "S2_METHOD", "seed": seed, "cell_id": alias,
        "target_polarization": pol, "fixture_id": fixture_id,
        "boundary_after_cw": boundary, "rotation_k": rotation,
        "jump_present": jump,
        "projection_role": "DIRECT_ON" if jump else "CACHED_OFF_PROJECTION",
        "physical_case_id": physical_case_id, "computation_id": computation_id,
        "method_id": method_id,
        "affected_cw_errors": int(np.count_nonzero(np.any(affected, axis=1))),
        "affected_cw_total": 16 - boundary,
        "information_bit_errors": int(np.count_nonzero(errors)),
        "information_bit_total": 16384,
        "total_transmitted_symbols_per_polarization": total_symbols,
        "result_receipt_sha256": _result_hash(decoded),
    }


def _s2_boot_metric(blocks: Sequence[Sequence[schemas.S2MethodRow]], metric: str) -> float | None:
    rows = tuple(row for block in blocks for row in block)
    values: list[float] = []
    for alias in ("hard", "mid", "clean"):
        cell = tuple(row for row in rows if row.cell_id == alias)
        b1e = sum(r.affected_cw_errors for r in cell if r.jump_present and r.method_id == schemas.S2_METHODS[0])
        b1t = sum(r.affected_cw_total for r in cell if r.jump_present and r.method_id == schemas.S2_METHODS[0])
        offe = sum(r.affected_cw_errors for r in cell if not r.jump_present)
        offt = sum(r.affected_cw_total for r in cell if not r.jump_present)
        o1e = sum(r.affected_cw_errors for r in cell if r.jump_present and r.method_id == schemas.S2_METHODS[2])
        if metric == "damage":
            values.append(b1e / b1t - offe / offt)
        else:
            if b1e <= 0:
                return None
            values.append((b1e - o1e) / b1e)
    return sum(values) / 3


def run_s2(*, contract_path: Path, output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    owner = load_science_contract(contract_path)
    aliases = _s2_alias_cells(owner)
    checkpoint = output / "checkpoint.jsonl"
    mappings = load_checkpoint_rows(checkpoint, key_fields=_S2_ROW_KEY)
    completed = {(r["seed"], r["cell_id"], r["target_polarization"]) for r in mappings}
    resumed = len(completed)
    d0_codec = codec.D0Codec(owner)
    payload_cache: dict[int, tuple[Any, waveform.WaveformBuild]] = {}
    for seed, alias, pol in s2_plan(owner):
        if (seed, alias, pol) in completed:
            continue
        if seed not in payload_cache:
            truth_payload, built, _ = _payload(seed, owner, d0_codec)
            payload_cache[seed] = (truth_payload, built)
        truth_payload, built = payload_cache[seed]
        receiver_view, truth_view = channel.build_views(
            owner, built, root_seed=seed, physical_cell=aliases[alias],
            payload_truth=truth_payload,
        )
        pol_index = owner.population.polarizations.index(pol)
        truth_bits = truth_view.information_bits[pol_index]
        clean_data = receiver_view.equalized_samples[:, built.data_to_time]
        noise = float(receiver_view.receipts["c_post_cplx_per_pol"][pol_index])
        cw_ids = tuple(f"S2-{seed}-{alias}-{pol}-CW{i:02d}" for i in range(16))
        off = methods.run_b1(d0_codec, clean_data[pol_index],
                             complex_noise_power=noise, cw_ids=cw_ids)
        off_owner = f"S2-OFF-{seed}-{alias}-{pol}"
        seal = _deployment_seal(owner, receiver_view)
        cluster_rows: list[dict[str, Any]] = []
        for fixture_id, boundary, rotation in S2_FIXTURES:
            fixture = methods.inject_controlled_fixture(
                clean_data, target_polarization=pol_index,
                boundary_after_data=boundary * 384, rotation_k=rotation,
            )
            b0 = methods.run_b0(d0_codec, fixture.samples[pol_index],
                                complex_noise_power=noise, cw_ids=cw_ids)
            b1 = methods.run_b1(d0_codec, fixture.samples[pol_index],
                                complex_noise_power=noise, cw_ids=cw_ids)
            frozen = methods.freeze_deployable_outputs(
                b0=b0, b1=b1, deployment_seal=seal, fixture=fixture,
            )
            o1 = methods.evaluate_o1_inverse(
                d0_codec, fixture, frozen_outputs=frozen,
                complex_noise_power=noise, cw_ids=cw_ids,
            )
            case = f"S2-ON-{seed}-{alias}-{pol}-{fixture_id}"
            cluster_rows.extend((
                _s2_row(seed=seed, alias=alias, pol=pol, fixture_id=fixture_id,
                        boundary=boundary, rotation=rotation, jump=True,
                        method_id=schemas.S2_METHODS[0], decoded=b1.decoded,
                        truth_bits=truth_bits, physical_case_id=case,
                        computation_id=case + "-B1", total_symbols=built.waveform.shape[1]),
                _s2_row(seed=seed, alias=alias, pol=pol, fixture_id=fixture_id,
                        boundary=boundary, rotation=rotation, jump=True,
                        method_id=schemas.S2_METHODS[2], decoded=o1.decoded,
                        truth_bits=truth_bits, physical_case_id=case,
                        computation_id=case + "-O1", total_symbols=built.waveform.shape[1]),
                _s2_row(seed=seed, alias=alias, pol=pol, fixture_id=fixture_id,
                        boundary=boundary, rotation=rotation, jump=False,
                        method_id=schemas.S2_METHODS[0], decoded=off.decoded,
                        truth_bits=truth_bits, physical_case_id=off_owner,
                        computation_id=off_owner, total_symbols=built.waveform.shape[1]),
            ))
        append_checkpoint_frame(checkpoint, cluster_rows, key_fields=_S2_ROW_KEY)
    mappings = load_checkpoint_rows(checkpoint, key_fields=_S2_ROW_KEY)
    rows = typed_s2_rows(mappings)
    point = statistics.reduce_s2_damage_headroom(rows)
    blocks = tuple(tuple(row for row in rows if row.seed == seed)
                   for seed in range(8150, 8160))
    damage_ci = statistics.bootstrap_paired(
        blocks, lambda sample: _s2_boot_metric(sample, "damage"), draws=10000,
    )
    recovery_ci = statistics.bootstrap_paired(
        blocks, lambda sample: _s2_boot_metric(sample, "recoverability"), draws=10000,
        invalid_terminal="UNSTABLE_DAMAGE_DENOMINATOR",
    )
    damage_positive = sum(float(cell[7]) > 0 for cell in point.cells)
    recovery_positive = sum(cell[8] is not None and float(cell[8]) > 0 for cell in point.cells)
    damage_pass = point.damage >= 0.10 and damage_ci.lower is not None and damage_ci.lower > 0 and damage_positive >= 2
    recovery_pass = (point.recoverability is not None and point.recoverability >= 0.10
                     and recovery_ci.lower is not None and recovery_ci.lower > 0
                     and recovery_positive >= 2)
    verdict = "PASS" if damage_pass and recovery_pass else "FAIL"
    raw_receipt = artifacts.write_jsonl_atomic(
        output / "s2-raw.jsonl", mappings, sort_key=_S2_ARTIFACT_SORT_KEY,
        logical_name="s2-raw.jsonl",
    )
    summary = {
        "schema": "coded_decoder_feedback.d0.s2.damage_headroom.summary.v1",
        "row_count": len(rows), "base_cluster_count": 60, "b2_disposition": "NOT_RUN",
        "damage": {"point": point.damage, "ci_lower": damage_ci.lower,
                   "ci_upper": damage_ci.upper, "positive_cells": damage_positive,
                   "valid_replicates": damage_ci.valid_replicates,
                   "invalid_replicates": damage_ci.invalid_replicates,
                   "terminal": damage_ci.terminal, "verdict": "PASS" if damage_pass else "FAIL"},
        "recoverability": {"point": point.recoverability, "ci_lower": recovery_ci.lower,
                            "ci_upper": recovery_ci.upper, "positive_cells": recovery_positive,
                            "valid_replicates": recovery_ci.valid_replicates,
                            "invalid_replicates": recovery_ci.invalid_replicates,
                            "terminal": recovery_ci.terminal,
                            "verdict": "PASS" if recovery_pass else "FAIL"},
        "S2_VERDICT": verdict,
        "formal_science_disposition": "S2_DAMAGE_HEADROOM_ESTABLISHED" if verdict == "PASS" else "S2_DAMAGE_OR_HEADROOM_FAILED",
        "mission_method_delta": "NONE", "thesis_method_disposition": "NONE",
    }
    summary_bytes = artifacts.canonical_json_bytes(summary) + b"\n"
    _atomic_bytes(output / "summary.json", summary_bytes)
    receipt = {
        "schema": "coded_decoder_feedback.d0.s2.damage_headroom.receipt.v1",
        "contract_sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=D0_ROOT).decode().strip(),
        "row_count": len(rows), "base_cluster_count": 60, "b2_disposition": "NOT_RUN",
        "raw_sha256": raw_receipt.sha256,
        "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
        "resumed_completed_cluster_count": resumed,
        "wall_time_seconds": None if resumed else time.perf_counter() - started,
        "wall_time_status": "NOT_CAPTURED_ACROSS_RESUMES" if resumed else "COMPLETE_SINGLE_INVOCATION",
    }
    _atomic_bytes(output / "receipt.json", artifacts.canonical_json_bytes(receipt) + b"\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stage", choices=("S1", "S2"), default="S1")
    args = parser.parse_args()
    runner = run_s1 if args.stage == "S1" else run_s2
    print(json.dumps(runner(contract_path=args.contract, output=args.output), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
