from fractions import Fraction
from dataclasses import replace
from functools import partial
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
OWNER = (
    PROJECT_ROOT
    / "projects"
    / "thesis-fso"
    / "coded-decoder-feedback-groundwork"
    / "d0-defect-smoke-contract.yaml"
)
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))


def _benchmark_module():
    """Import inside the test so the absent I16 module is a valid RED."""
    importlib.invalidate_caches()
    return importlib.import_module("benchmark")


class _FakeWorker:
    def __init__(self) -> None:
        self.decoder_calls = []
        self.waveform_calls = 0
        self.waveform = b"one-engineering-waveform"
        self.bps_waveform_ids = []
        self.b2_freeze_ids = []
        self.rows = (
            {"record_id": "io-2", "kind": "engineering", "value": 2},
            {"record_id": "io-1", "kind": "engineering", "value": 1},
        )

    def decoder_batch(self, cw_batch, *, resolved_freeze):
        self.decoder_calls.append((cw_batch, resolved_freeze.freeze_id))
        return {"cw_batch": cw_batch, "fresh_restart": True}

    def build_waveform(self, *, root_seed):
        assert root_seed == 900000001
        self.waveform_calls += 1
        return self.waveform

    def bps_pair(self, waveform, *, B, Nw):
        self.bps_waveform_ids.append(id(waveform))
        return {"B": B, "Nw": Nw, "result": f"{B}:{Nw}"}

    def b2_view(self, view_index, *, resolved_freeze):
        self.b2_freeze_ids.append(resolved_freeze.freeze_id)
        return f"unique-b2-view-{view_index}".encode("ascii")

    def hmm_primitive_scores(self, *, resolved_freeze):
        return (0.1, -0.25, 0.5, 1.0 / 3.0)

    def atomic_rows(self):
        return self.rows


@pytest.fixture
def d0_contract():
    return importlib.import_module("contract").load_contract(OWNER)


@pytest.fixture
def d0_owner_authority():
    return importlib.import_module("contract").load_owner_identity_authority(OWNER)


@pytest.fixture
def synthetic_freeze():
    contract = importlib.import_module("contract")
    return contract.ResolvedDevFreeze(
        "f" * 64,
        {"synthetic_engineering_only": True},
        {"owner_sha256": "e" * 64},
    )


@pytest.fixture
def benchmark_run(tmp_path, d0_owner_authority, synthetic_freeze):
    benchmark = _benchmark_module()
    worker = _FakeWorker()
    output = tmp_path / "engineering-slice.jsonl"
    run = benchmark.run_engineering_benchmark(
        d0_owner_authority,
        synthetic_freeze,
        worker=worker,
        output=output,
    )
    return benchmark, worker, output, run


def _one_second_watchdog_operation(finished_marker):
    time.sleep(1.0)
    Path(finished_marker).write_text("escaped", encoding="ascii")
    return "late-value"


def test_eb01_manifest_is_engineering_only_with_unregistered_seed_and_synthetic_freeze(
    benchmark_run, d0_contract
):
    benchmark, _worker, _output, run = benchmark_run
    assert run.manifest.benchmark_class == "ENGINEERING_THROUGHPUT_V1"
    assert run.manifest.root_seed == 900000001
    assert run.manifest.synthetic_resolved_freeze is True
    assert run.manifest.dev_freeze_sha256 == "f" * 64
    with pytest.raises(ValueError, match="outside every registered"):
        d0_contract.seed_registry.label_for(run.manifest.root_seed)
    assert run.manifest.required_slices == benchmark.REQUIRED_SLICES
    forbidden = {"estimand", "scientific_verdict", "gate_conjunction", "raw_s1", "raw_s4"}
    assert forbidden.isdisjoint(run.manifest.__dataclass_fields__)


def test_eb02_decoder_batches_cover_4_8_12_16_with_fresh_restarts(benchmark_run):
    _benchmark, worker, _output, run = benchmark_run
    assert tuple(item.cw_batch for item in run.decoder_batches) == (4, 8, 12, 16)
    assert all(item.fresh_restart for item in run.decoder_batches)
    assert tuple(size for size, _freeze_id in worker.decoder_calls) == (4, 8, 12, 16)
    assert len(worker.decoder_calls) == len(run.decoder_batches)


def test_eb03_one_waveform_exercises_all_six_bps_pairs(benchmark_run):
    benchmark, worker, _output, run = benchmark_run
    assert tuple(item.pair for item in run.bps_slices) == benchmark.BPS_PAIRS
    assert len({item.waveform_sha256 for item in run.bps_slices}) == 1
    assert run.bps_slices[0].waveform_sha256 == hashlib.sha256(worker.waveform).hexdigest()
    assert worker.waveform_calls == 1
    assert len(set(worker.bps_waveform_ids)) == 1


def test_eb04_one_tuple_uses_ten_unique_b2_views_without_fit(benchmark_run):
    _benchmark, worker, _output, run = benchmark_run
    assert len(run.b2_view_sha256) == 10
    assert len(set(run.b2_view_sha256)) == 10
    assert worker.b2_freeze_ids == ["f" * 64] * 10


def test_eb05_hmm_keeps_primitive_scores_and_exact_binary64_aggregate(benchmark_run):
    _benchmark, _worker, _output, run = benchmark_run
    assert run.hmm.primitive_count == 4
    exact = sum((Fraction.from_float(value) for value in run.hmm.primitive_scores), Fraction())
    assert run.hmm.aggregate.numerator_decimal == str(exact.numerator)
    assert run.hmm.aggregate.denominator_power2 == exact.denominator.bit_length() - 1
    assert run.hmm.aggregate.count == 4


def test_eb06_real_atomic_jsonl_io_returns_landed_receipt(benchmark_run):
    _benchmark, worker, output, run = benchmark_run
    artifacts = importlib.import_module("artifacts")
    expected = artifacts.canonical_jsonl_bytes(worker.rows, sort_key="record_id")
    assert output.read_bytes() == expected
    assert run.atomic_io.record_count == 2
    assert run.atomic_io.byte_count == len(expected)
    assert run.atomic_io.sha256 == hashlib.sha256(expected).hexdigest()
    assert run.atomic_io.directory_fsync_status in {"SUPPORTED", "UNSUPPORTED"}


def _complete_record(*, projected_d0_days=4.5):
    return {
        "device": "fake-cpu",
        "dependency_versions": {"python": "3.11"},
        "physical_api_invocations": 21,
        "logical_batches": 4,
        "cache_hits": 3,
        "wall_time": 12.5,
        "peak_memory": {
            "process_rss_peak_bytes": 4096,
            "accelerator_backend": "not_applicable",
            "accelerator_peak_bytes": None,
        },
        "projected_full_D0_time": projected_d0_days * 86400.0,
    }


def _work_partition(*, projected_d0_days=4.5):
    completed_ids = (
        "contract_source_and_asset_closure",
        "receiver_truth_views_and_carrier_realization",
        "B0_B1_O1_mapping_and_controlled_fixture",
    )
    remaining_ids = (
        "source_explicit_B2_adaptation_and_dev_freeze",
        "strata_tests_statistics_and_cost_ledger",
        "bounded_runs_raw_rows_ci_and_receipts",
    )
    consumed = dict.fromkeys(completed_ids, 0.5)
    remaining_total = projected_d0_days - sum(consumed.values())
    remaining = dict.fromkeys(remaining_ids, remaining_total / len(remaining_ids))
    return consumed, remaining


def test_eb07_watchdog_hard_terminates_worker_near_deadline_and_preserves_old_receipt(
    benchmark_run, d0_owner_authority, tmp_path
):
    benchmark, _worker, _output, run = benchmark_run
    finished_marker = tmp_path / "operation-finished"
    started = time.monotonic()
    watchdog = benchmark.watchdog_call(
        partial(_one_second_watchdog_operation, str(finished_marker)),
        watchdog_seconds=0.20,
    )
    wall_elapsed = time.monotonic() - started
    assert watchdog.status == "INCOMPLETE"
    assert 0.15 <= watchdog.elapsed_seconds < 0.80
    assert wall_elapsed < 0.80
    assert watchdog.value is None
    assert not finished_marker.exists()

    consumed, remaining = _work_partition()
    receipt = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(),
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=720.0,
        watchdog_seconds=720,
    )
    assert receipt.status == "INCOMPLETE"
    target = tmp_path / "benchmark-receipt.jsonl"
    target.write_bytes(b"old-complete-receipt\n")
    with pytest.raises(benchmark.BenchmarkError, match="incomplete"):
        benchmark.write_benchmark_receipt(target, receipt)
    assert target.read_bytes() == b"old-complete-receipt\n"


def test_eb08_full_frozen_work_projection_rejects_missing_axis():
    benchmark = _benchmark_module()
    projection = benchmark.build_full_work_projection()
    assert dict(projection.logical_counts.items()) == {
        "decoder_batches": 69360,
        "cw_decodes": 1032000,
        "bp_iterations": 20640000,
        "hmm_dual_pol_frame_parameter_pair_scores": 8344800,
        "hmm_primitive_pol_trajectory_parameter_pair_scores": 16689600,
        "materialized_hmm_primitive_pol_trajectory_parameter_pair_scores": 7027200,
    }
    assert projection.logical_manifest_sha256 == hashlib.sha256(
        importlib.import_module("artifacts").canonical_json_bytes(
            dict(projection.logical_counts.items())
        )
    ).hexdigest()
    missing = dict(projection.logical_counts.items())
    missing.pop("bp_iterations")
    with pytest.raises(benchmark.BenchmarkError, match="axes"):
        benchmark.build_full_work_projection(logical_counts=missing)


def test_eb09_allowed_adjustments_preserve_logical_manifest_and_forbid_state_reuse():
    benchmark = _benchmark_module()
    original = benchmark.build_full_work_projection()
    adjusted = benchmark.apply_engineering_adjustments(
        original,
        adjustments=("vectorization", "batch_size", "content_addressed_cache"),
        materialized_counts={
            "decoder_batches": 40000,
            "cw_decodes": 600000,
            "bp_iterations": 12000000,
            "hmm_primitive_pol_trajectory_parameter_pair_scores": 6000000,
        },
    )
    assert adjusted.logical_counts == original.logical_counts
    assert adjusted.logical_manifest_sha256 == original.logical_manifest_sha256
    assert adjusted.materialized_counts != original.materialized_counts
    with pytest.raises(benchmark.BenchmarkError, match="forbidden"):
        benchmark.apply_engineering_adjustments(
            original,
            adjustments=("reuse_decoder_message_state",),
            materialized_counts={},
        )


def test_eb10_budget_equation_partition_and_threshold_records(
    benchmark_run, d0_owner_authority
):
    benchmark, _worker, _output, run = benchmark_run
    consumed, remaining = _work_partition(projected_d0_days=4.5)
    receipt = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(),
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
        watchdog_seconds=720,
    )
    assert receipt.status == "ENGINEERING_THROUGHPUT_PASS"
    assert receipt.consumed_engineering_days == pytest.approx(1.5)
    assert receipt.projected_remaining_D0_days == pytest.approx(3.0)
    assert receipt.projected_D0_days == pytest.approx(4.5)
    assert receipt.post_D0_C1_days == 2.0
    assert receipt.contingency_consumed_days == 0.0
    assert receipt.required_remaining_contingency_days == 0.5
    assert receipt.projected_mission_days == 7.0
    assert len(receipt.engineering_record) + 1 == 9  # owner SHA + owner record

    consumed_5, remaining_5 = _work_partition(projected_d0_days=5.0)
    exact_ceiling = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(projected_d0_days=5.0),
        consumed_work_days=consumed_5,
        remaining_work_days=remaining_5,
        elapsed_seconds=719.0,
    )
    assert exact_ceiling.status == "ENGINEERING_THROUGHPUT_PASS"
    assert exact_ceiling.required_remaining_contingency_days == 0.0
    assert exact_ceiling.projected_mission_days == 7.0

    consumed_over, remaining_over = _work_partition(projected_d0_days=5.1)
    over = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(projected_d0_days=5.1),
        consumed_work_days=consumed_over,
        remaining_work_days=remaining_over,
        elapsed_seconds=719.0,
    )
    assert over.status == "INCOMPLETE"
    assert "MISSING_ALLOWED_ADJUSTMENT_EVIDENCE" in over.incomplete_reasons
    assert over.required_remaining_contingency_days < 0.0

    missing_record = _complete_record()
    missing_record.pop("peak_memory")
    incomplete = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=missing_record,
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
    )
    assert incomplete.status == "INCOMPLETE"

    inconsistent = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(projected_d0_days=100.0),
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
    )
    assert inconsistent.status == "INCOMPLETE"
    assert "PROJECTED_FULL_D0_TIME_MISMATCH" in inconsistent.incomplete_reasons

    micro_perturbed_record = _complete_record()
    micro_perturbed_record["projected_full_D0_time"] += 5e-7
    micro_perturbed = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=micro_perturbed_record,
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
    )
    assert micro_perturbed.status == "INCOMPLETE"
    assert "PROJECTED_FULL_D0_TIME_MISMATCH" in micro_perturbed.incomplete_reasons

    fake_authority = replace(d0_owner_authority, owner_sha256="a" * 64)
    with pytest.raises(Exception, match="owner|authority|SHA256"):
        benchmark.build_benchmark_receipt(
            run,
            owner_authority=fake_authority,
            engineering_record=_complete_record(),
            consumed_work_days=consumed,
            remaining_work_days=remaining,
            elapsed_seconds=719.0,
        )
    assert receipt.owner_budget_sha256 == d0_owner_authority.owner_sha256


@pytest.mark.parametrize(
    ("field", "invalid"),
    (
        ("device", ""),
        ("device", 7),
        ("dependency_versions", []),
        ("dependency_versions", {"python": 3.11}),
        ("physical_api_invocations", -1),
        ("physical_api_invocations", True),
        ("logical_batches", "4"),
        ("cache_hits", -1),
        ("wall_time", float("nan")),
        ("wall_time", float("inf")),
        ("wall_time", True),
        ("peak_memory", -1),
        ("peak_memory", True),
        ("projected_full_D0_time", -1.0),
        ("projected_full_D0_time", float("nan")),
        ("projected_full_D0_time", float("inf")),
        ("projected_full_D0_time", False),
    ),
)
def test_eb10_owner_record_values_are_exact_finite_nonnegative(
    benchmark_run, d0_owner_authority, field, invalid
):
    benchmark, _worker, _output, run = benchmark_run
    consumed, remaining = _work_partition()
    record = _complete_record()
    record[field] = invalid
    receipt = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=record,
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
    )
    assert receipt.status == "INCOMPLETE"
    assert "INVALID_OWNER_RECORD" in receipt.incomplete_reasons


def test_eb11_cli_and_receipt_have_no_science_writer_or_verdict_path(
    benchmark_run, d0_owner_authority
):
    benchmark, _worker, _output, run = benchmark_run
    args = benchmark.parse_cli_args(
        [
            "--class", "ENGINEERING_THROUGHPUT_V1",
            "--root-seed", "900000001",
            "--watchdog-seconds", "720",
            "--synthetic-resolved-freeze",
            "--output", "engineering-output",
        ]
    )
    assert args.benchmark_class == "ENGINEERING_THROUGHPUT_V1"
    assert args.root_seed == 900000001
    assert args.watchdog_seconds == 720
    assert args.synthetic_resolved_freeze is True
    assert args.output == Path("engineering-output")
    assert not any("science" in action.dest for action in benchmark.build_cli_parser()._actions)

    consumed, remaining = _work_partition()
    receipt = benchmark.build_benchmark_receipt(
        run,
        owner_authority=d0_owner_authority,
        engineering_record=_complete_record(),
        consumed_work_days=consumed,
        remaining_work_days=remaining,
        elapsed_seconds=719.0,
    )
    document = benchmark.benchmark_receipt_document(receipt)
    forbidden = {
        "raw_s1", "raw_s2", "raw_s3", "raw_s4", "estimand", "ci",
        "gate_conjunction", "c1_terminal", "scientific_verdict",
    }
    assert forbidden.isdisjoint(document)
    assert forbidden.isdisjoint(receipt.__dataclass_fields__)


def test_eb12_authorized_cli_runs_real_engineering_slices_and_receipt(tmp_path):
    benchmark = _benchmark_module()
    output = tmp_path / "real-engineering"
    exit_code = benchmark.main(
        [
            "--class", "ENGINEERING_THROUGHPUT_V1",
            "--root-seed", "900000001",
            "--watchdog-seconds", "720",
            "--synthetic-resolved-freeze",
            "--output", str(output),
        ]
    )
    assert exit_code in (0, 2)

    slice_path = output / "engineering-slices.jsonl"
    receipt_path = output / "benchmark-receipt.jsonl"
    rows = [json.loads(line) for line in slice_path.read_text("utf-8").splitlines()]
    receipt = json.loads(receipt_path.read_text("utf-8"))
    by_kind = {
        kind: [row for row in rows if row["kind"] == kind]
        for kind in {row["kind"] for row in rows}
    }
    assert [row["cw_batch"] for row in by_kind["decoder"]] == [4, 8, 12, 16]
    assert len(by_kind["bps"]) == 6
    assert len({row["waveform_sha256"] for row in by_kind["bps"]}) == 1
    assert len(by_kind["b2"]) == 10
    assert len({row["result_sha256"] for row in by_kind["b2"]}) == 10
    assert len(by_kind["hmm"]) == 1
    assert by_kind["hmm"][0]["primitive_count"] == by_kind["hmm"][0]["aggregate_count"]
    assert receipt["status"] in {
        "ENGINEERING_THROUGHPUT_PASS",
        "GREATER_THAN_7D_HARD_BLOCKER",
    }
    assert exit_code == (
        0 if receipt["status"] == "ENGINEERING_THROUGHPUT_PASS" else 2
    )
    assert receipt["owner_budget_sha256"] == hashlib.sha256(OWNER.read_bytes()).hexdigest()
    assert set(receipt["engineering_record"]) == set(benchmark.OWNER_RECORD_FIELDS)
    assert receipt["completed_work_ids"]
    assert receipt["remaining_work_ids"]
    assert not set(receipt["completed_work_ids"]) & set(receipt["remaining_work_ids"])
    adjustments = receipt["adjustment_receipts"]
    assert {item["name"] for item in adjustments} == {
        "vectorization",
        "batch_size",
        "content_addressed_cache",
        "checkpoint_chunk_size",
    }
    assert all(item["logical_manifest_sha256_before"] == receipt["workload_manifest_sha256"] for item in adjustments)
    assert all(item["logical_manifest_sha256_after"] == receipt["workload_manifest_sha256"] for item in adjustments)
    assert all(item["before_elapsed_seconds"] > 0.0 for item in adjustments)
    assert all(item["after_elapsed_seconds"] > 0.0 for item in adjustments)
    assert all(item["before_unit_count"] > 0 for item in adjustments)
    assert all(item["after_unit_count"] > 0 for item in adjustments)
    assert all(item["output_equivalent_to_scalar"] is True for item in adjustments)
    assert receipt["selected_adjustment_name"] in {
        "vectorization", "batch_size", "checkpoint_chunk_size"
    }
    assert receipt["selected_hmm_seconds_per_trajectory"] > 0.0
    forbidden = {
        "raw_s1", "raw_s2", "raw_s3", "raw_s4", "estimand", "ci",
        "gate_conjunction", "c1_terminal", "scientific_verdict",
    }
    assert forbidden.isdisjoint(receipt)


def test_eb13_direct_script_cli_bootstraps_simulation_imports(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            str(D0_ROOT / "benchmark.py"),
            "--help",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "D0 engineering throughput gate" in completed.stdout


def _bare_real_worker(benchmark, *, receiver=None, codec=None):
    worker = benchmark._RealEngineeringWorker.__new__(benchmark._RealEngineeringWorker)
    worker._receiver = receiver
    worker._waveform = importlib.import_module("waveform")
    worker._codec = codec
    worker._root_seed = 900000001
    worker._rows = []
    worker._waveform_document = None
    worker._waveform_build = None
    worker._waveform_samples = None
    worker.physical_api_invocations = 0
    worker.decoder_seconds = 0.0
    worker.bps_seconds = 0.0
    worker.b2_seconds = 0.0
    worker.hmm_seconds = 0.0
    worker.hmm_trajectory_units = 0
    worker.cache_hits = 0
    worker.adjustment_receipts = ()
    return worker


def test_eb14_real_bps_slice_uses_owner_sized_registered_waveform():
    benchmark = _benchmark_module()

    class ReceiverSpy:
        def __init__(self):
            self.calls = []

        def run_common_bps(self, samples, *, B, Nw):
            value = np.asarray(samples)
            self.calls.append((value.shape, B, Nw))
            return SimpleNamespace(
                samples=value,
                phase_trace=np.zeros(value.shape, dtype=np.float64),
                receipt={"implementation": "receiver-spy"},
            )

    receiver = ReceiverSpy()
    worker = _bare_real_worker(benchmark, receiver=receiver, codec=SimpleNamespace())
    document = worker.build_waveform(root_seed=900000001)
    worker.bps_pair(document, B=32, Nw=31)

    assert document["data_symbols_per_polarization"] == 6144
    assert document["prefix_symbols_per_polarization"] == 32
    assert document["periodic_pilot_symbols_per_polarization"] in (32, 64, 325, 684)
    expected_total = 6144 + 32 + document["periodic_pilot_symbols_per_polarization"]
    assert document["sample_count_per_polarization"] == expected_total
    assert receiver.calls == [((expected_total,), 32, 31)] * 2


def test_eb15_real_b2_slice_calls_production_run_b2_with_owner_shapes(monkeypatch):
    benchmark = _benchmark_module()
    decode_calls = []
    run_calls = []

    class CodecSpy:
        def decode_fresh(self, llr, *, cw_ids, candidate_id):
            decode_calls.append((np.asarray(llr).shape, tuple(cw_ids), candidate_id))
            return SimpleNamespace(info_bits=np.zeros((16, 1024), dtype=np.uint8))

    real_run_b2 = benchmark.b2_module.run_b2

    def run_b2_spy(samples, posterior, **kwargs):
        run_calls.append((np.asarray(samples).shape, np.asarray(posterior).shape))
        return real_run_b2(samples, posterior, **kwargs)

    monkeypatch.setattr(benchmark.b2_module, "run_b2", run_b2_spy)
    worker = _bare_real_worker(
        benchmark, receiver=SimpleNamespace(), codec=CodecSpy()
    )
    worker.build_waveform(root_seed=900000001)
    worker.b2_view(0, resolved_freeze=SimpleNamespace(freeze_id="f" * 64))

    assert run_calls == [((2, 6144), (2, 6144, 4))]
    assert [call[0] for call in decode_calls] == [(16, 1536), (16, 1536)]
    assert all(len(ids) == len(set(ids)) == 16 for _shape, ids, _candidate in decode_calls)


def test_eb16_hmm_times_two_real_owner_pilot_trajectories_and_projects_units():
    benchmark = _benchmark_module()
    worker = _bare_real_worker(
        benchmark, receiver=SimpleNamespace(), codec=SimpleNamespace()
    )
    worker.setup_seconds = 0.0
    worker.build_waveform(root_seed=900000001)
    scores = worker.hmm_primitive_scores(
        resolved_freeze=SimpleNamespace(freeze_id="f" * 64)
    )

    row = next(row for row in worker._rows if row["kind"] == "hmm")
    assert len(scores) == worker.hmm_trajectory_units == 2
    assert row["polarization_trajectory_count"] == 2
    assert row["pilot_count_per_trajectory"] in (32, 64, 325, 684)
    assert row["elapsed_seconds"] > 0.0
    expected = (
        worker.hmm_best_seconds_per_trajectory
        * benchmark.FROZEN_MATERIALIZED_COUNTS[
            "hmm_primitive_pol_trajectory_parameter_pair_scores"
        ]
    )
    assert worker.projected_compute_seconds(0.0) == pytest.approx(expected)


def test_eb17_peak_memory_is_process_rss_with_explicit_accelerator_record():
    benchmark = _benchmark_module()
    value, peak = benchmark._measure_peak_memory(lambda: "measured")

    assert value == "measured"
    assert set(peak) == {
        "process_rss_peak_bytes",
        "accelerator_backend",
        "accelerator_peak_bytes",
    }
    assert type(peak["process_rss_peak_bytes"]) is int
    assert peak["process_rss_peak_bytes"] > 0
    if peak["accelerator_backend"] == "not_applicable":
        assert peak["accelerator_peak_bytes"] is None
    else:
        assert type(peak["accelerator_peak_bytes"]) is int
        assert peak["accelerator_peak_bytes"] >= 0


def test_eb18_real_worker_counts_only_actual_cache_reads():
    benchmark = _benchmark_module()

    class ReceiverSpy:
        def run_common_bps(self, samples, *, B, Nw):
            value = np.asarray(samples)
            return SimpleNamespace(
                samples=value,
                phase_trace=np.zeros(value.shape, dtype=np.float64),
                receipt={"implementation": "receiver-spy"},
            )

    worker = _bare_real_worker(
        benchmark, receiver=ReceiverSpy(), codec=SimpleNamespace()
    )
    document = worker.build_waveform(root_seed=900000001)
    for B, Nw in benchmark.BPS_PAIRS:
        worker.bps_pair(document, B=B, Nw=Nw)

    assert worker.cache_hits == 0


def test_eb19_allowed_adjustments_are_real_hmm_measurements_not_synthetic_counts():
    benchmark = _benchmark_module()
    worker = _bare_real_worker(
        benchmark, receiver=SimpleNamespace(), codec=SimpleNamespace()
    )
    worker.setup_seconds = 0.0
    worker.build_waveform(root_seed=900000001)
    scalar_scores = worker.hmm_primitive_scores(
        resolved_freeze=SimpleNamespace(freeze_id="f" * 64)
    )

    projection = benchmark.build_full_work_projection()
    receipts = worker.adjustment_receipts
    assert tuple(item.name for item in receipts) == benchmark.ALLOWED_ADJUSTMENTS
    assert worker.hmm_best_seconds_per_trajectory > 0.0
    assert worker.hmm_best_output_sha256
    for item in receipts:
        assert item.config
        assert item.before_elapsed_seconds > 0.0
        assert item.after_elapsed_seconds > 0.0
        assert item.before_unit_count > 0
        assert item.after_unit_count > 0
        assert len(item.before_output_sha256) == 64
        assert len(item.after_output_sha256) == 64
        assert item.actual_cache_reads >= 0
        assert item.logical_manifest_sha256_before == projection.logical_manifest_sha256
        assert item.logical_manifest_sha256_after == projection.logical_manifest_sha256
        assert dict(item.materialized_projection_before) == dict(projection.materialized_counts)
        assert set(item.materialized_projection_after) == set(projection.materialized_counts)
        assert item.materialized_projection_change_source
        assert item.output_equivalent_to_scalar is True
        assert item.max_abs_error <= benchmark.HMM_STRICT_ATOL

    cache = next(item for item in receipts if item.name == "content_addressed_cache")
    assert cache.actual_cache_reads == 0
    assert cache.applicability == "NOT_APPLICABLE"
    assert cache.config["distinct_content_count"] == 2
    assert cache.config["actual_miss_compute_units"] == cache.after_unit_count == 4
    assert dict(cache.materialized_projection_after) == dict(cache.materialized_projection_before)
    assert worker.cache_hits == 0
    assert worker.physical_api_invocations == 46
    assert len(scalar_scores) == 2
