from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import sys
from types import MappingProxyType
from pathlib import Path

import pytest


D0_ROOT = Path(__file__).resolve().parents[1] / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))


def _api():
    import artifacts

    return artifacts


def _verify_api():
    import verify

    return verify


def test_seven_dev_artifacts_named():
    assert _api().DEV_ARTIFACT_NAMES == (
        "dev_manifest.json",
        "raw_bps_dev.jsonl",
        "hmm_grid_dev_chunks.jsonl",
        "raw_b2_tuple_clean_dev.jsonl",
        "raw_b2_tuple_controlled_dev.jsonl",
        "dev_freeze.json",
        "dev_freeze_receipt.json",
    )


def test_canonical_json_and_jsonl_are_strict_stable_bytes():
    api = _api()
    assert api.canonical_json_bytes({"z": "雪", "a": [True, None, 3]}) == (
        '{"a":[true,null,3],"z":"雪"}'.encode("utf-8")
    )
    rows_a = [
        MappingProxyType({"pk": "b", "value": 2}),
        MappingProxyType({"value": 1, "pk": "a"}),
    ]
    rows_b = list(reversed(rows_a))
    expected = b'{"pk":"a","value":1}\n{"pk":"b","value":2}\n'
    assert api.canonical_jsonl_bytes(rows_a, sort_key="pk") == expected
    assert api.canonical_jsonl_bytes(rows_b, sort_key="pk") == expected
    assert hashlib.sha256(expected).hexdigest() == hashlib.sha256(
        api.canonical_jsonl_bytes(rows_b, sort_key="pk")
    ).hexdigest()


@pytest.mark.parametrize(
    "bad",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
        {1: "non-string-key"},
        b"bytes",
        Path("opaque-path"),
        object(),
    ],
)
def test_canonical_json_rejects_non_json_or_non_finite_values(bad):
    with pytest.raises((TypeError, ValueError)):
        _api().canonical_json_bytes({"bad": bad})


def test_canonical_json_rejects_cycles_and_bad_sort_keys():
    api = _api()
    cycle = []
    cycle.append(cycle)
    negatives = [
        lambda: api.canonical_json_bytes(cycle),
        lambda: api.canonical_jsonl_bytes([{"id": 1}, {"id": 1}], sort_key="id"),
        lambda: api.canonical_jsonl_bytes([{"id": 1}], sort_key=""),
        lambda: api.canonical_jsonl_bytes([{"other": 1}], sort_key="id"),
        lambda: api.canonical_jsonl_bytes([{"id": None}], sort_key="id"),
        lambda: api.canonical_jsonl_bytes([{"id": []}], sort_key="id"),
    ]
    for operation in negatives:
        with pytest.raises((TypeError, ValueError, KeyError)):
            operation()


def test_validation_precedes_every_filesystem_write(tmp_path, monkeypatch):
    api = _api()
    target = tmp_path / "rows.jsonl"
    target.write_bytes(b"OLD\n")
    calls = []

    def forbidden_mkstemp(*args, **kwargs):
        calls.append("mkstemp")
        raise AssertionError("filesystem write started before validation")

    monkeypatch.setattr(api.tempfile, "mkstemp", forbidden_mkstemp)
    schema = {
        "sort_key": ("id",),
        "required_fields": ("id", "parent", "value"),
        "exact_cardinality": 2,
        "foreign_keys": ({"field": "parent", "values": ("p0",)},),
        "validator": lambda rows: (_ for _ in ()).throw(ValueError("manifest")),
    }
    with pytest.raises(ValueError):
        api.write_jsonl_atomic(target, [{"id": "a", "parent": "p0", "value": 1}], schema)
    assert calls == []
    assert target.read_bytes() == b"OLD\n"


def test_single_file_atomic_trace_and_pre_replace_failure_preserves_old(tmp_path):
    api = _api()
    target = tmp_path / "rows.jsonl"
    target.write_bytes(b"OLD\n")
    trace = []
    receipt = api.write_jsonl_atomic(
        target,
        [{"id": "b", "x": 2}, {"id": "a", "x": 1}],
        {"sort_key": "id", "exact_cardinality": 2},
        event_hook=lambda event, path: trace.append((event, Path(path).name)),
        logical_name="rows.jsonl",
    )
    assert target.read_bytes() == b'{"id":"a","x":1}\n{"id":"b","x":2}\n'
    assert [event for event, _ in trace] == [
        "temp_created", "written", "flushed", "file_fsynced", "closed",
        "replaced", "directory_fsync_attempted", "directory_fsync_recorded",
    ]
    assert receipt.sha256 == hashlib.sha256(target.read_bytes()).hexdigest()
    assert (receipt.byte_count, receipt.record_count) == (34, 2)
    assert receipt.logical_name == "rows.jsonl"
    assert receipt.directory_fsync_status in {"SUPPORTED", "UNSUPPORTED"}

    for failure_event in ("written", "flushed", "file_fsynced", "closed"):
        target.write_bytes(b"OLD-AGAIN\n")

        def fail(event, _path, selected=failure_event):
            if event == selected:
                raise OSError(f"injected-{selected}")

        with pytest.raises(OSError, match="injected"):
            api.write_jsonl_atomic(
                target, [{"id": "a"}], {"sort_key": "id"}, event_hook=fail
            )
        assert target.read_bytes() == b"OLD-AGAIN\n"
        assert list(tmp_path.glob(f".{target.name}.*.tmp")) == []


BINDINGS = {
    "owner_sha256": "0" * 64,
    "contract_sha256": "1" * 64,
    "source_sha256": "2" * 64,
    "code_sha256": "3" * 64,
    "manifest_sha256": "4" * 64,
    "raw_sha256": "5" * 64,
    "chunk_sha256": "6" * 64,
    "freeze_sha256": "7" * 64,
    "selection_sha256": "8" * 64,
    "seed_sha256": "9" * 64,
    "summary_sha256": "a" * 64,
    "ledger_sha256": "b" * 64,
}


def _bundle_files():
    return {
        "dev_manifest.json": {"schema": "manifest", "count": 2},
        "raw_bps_dev.jsonl": [{"tuple_id": "M3", "seed": 2}, {"tuple_id": "M2", "seed": 1}],
        "hmm_grid_dev_chunks.jsonl": [{"tuple_id": "M2", "chunk_id": "c0"}],
        "raw_b2_tuple_clean_dev.jsonl": [{"tuple_id": "M2", "seed": 1, "polarization": "X"}],
        "raw_b2_tuple_controlled_dev.jsonl": [{"tuple_id": "M2", "seed": 1, "target_polarization": "X", "fixture_id": "f", "row_polarization": "X"}],
        "dev_freeze.json": {"schema": "freeze", "winner": "M2"},
    }


def test_bundle_receipt_lands_last_and_validates_exact_landed_bytes(tmp_path):
    api = _api()
    trace = []
    receipt = api.write_bundle_atomic(
        tmp_path / "bundle",
        _bundle_files(),
        bindings=BINDINGS,
        receipt_name="dev_freeze_receipt.json",
        required_names=api.DEV_ARTIFACT_NAMES,
        event_hook=lambda event, path: trace.append((event, Path(path).name)),
    )
    assert receipt.complete is True
    assert tuple(item.logical_name for item in receipt.artifacts) == api.DEV_ARTIFACT_NAMES[:-1]
    assert [name for event, name in trace if event == "bundle_artifact_committed"][-1] == (
        "dev_freeze_receipt.json"
    )
    checked = api.validate_complete_bundle(
        tmp_path / "bundle",
        required_names=api.DEV_ARTIFACT_NAMES,
        receipt_name="dev_freeze_receipt.json",
    )
    assert checked.receipt_sha256 == receipt.receipt_sha256
    generation = tmp_path / "bundle" / ".generations" / receipt.generation
    for item in receipt.artifacts:
        landed = (generation / item.logical_name).read_bytes()
        assert item.sha256 == hashlib.sha256(landed).hexdigest()
        assert item.byte_count == len(landed)


def test_bundle_fail_closed_tamper_and_old_generation_survives_failure(tmp_path):
    api = _api()
    root = tmp_path / "bundle"
    first = api.write_bundle_atomic(
        root,
        _bundle_files(),
        bindings=BINDINGS,
        receipt_name="dev_freeze_receipt.json",
        required_names=api.DEV_ARTIFACT_NAMES,
    )
    pointer_before = (root / "CURRENT.json").read_bytes()

    def fail_before_pointer(event, _path):
        if event == "bundle_before_pointer":
            raise OSError("injected-bundle-stop")

    newer = _bundle_files()
    newer["dev_manifest.json"] = {"schema": "manifest", "count": 999}
    with pytest.raises(OSError, match="injected-bundle-stop"):
        api.write_bundle_atomic(
            root,
            newer,
            bindings=BINDINGS,
            receipt_name="dev_freeze_receipt.json",
            required_names=api.DEV_ARTIFACT_NAMES,
            event_hook=fail_before_pointer,
        )
    assert (root / "CURRENT.json").read_bytes() == pointer_before
    assert api.validate_complete_bundle(
        root, required_names=api.DEV_ARTIFACT_NAMES,
        receipt_name="dev_freeze_receipt.json",
    ).generation == first.generation

    generation = root / ".generations" / first.generation
    victim = generation / "raw_bps_dev.jsonl"
    original = victim.read_bytes()
    victim.write_bytes(original + b"x")
    with pytest.raises(ValueError, match="hash|byte"):
        api.validate_complete_bundle(
            root, required_names=api.DEV_ARTIFACT_NAMES,
            receipt_name="dev_freeze_receipt.json",
        )


def test_bundle_post_replace_failure_keeps_current_generation_readable(tmp_path, monkeypatch):
    api = _api()
    root = tmp_path / "bundle"
    first = api.write_bundle_atomic(
        root,
        _bundle_files(),
        bindings=BINDINGS,
        receipt_name="dev_freeze_receipt.json",
        required_names=api.DEV_ARTIFACT_NAMES,
    )

    original_fsync_directory = api._fsync_directory

    def fail_after_pointer_replace(path):
        if Path(path) == root:
            raise OSError("injected-post-pointer-replace")
        return original_fsync_directory(path)

    monkeypatch.setattr(api, "_fsync_directory", fail_after_pointer_replace)

    newer = _bundle_files()
    newer["dev_manifest.json"] = {"schema": "manifest", "count": 999}
    with pytest.raises(OSError, match="injected-post-pointer-replace"):
        api.write_bundle_atomic(
            root,
            newer,
            bindings=BINDINGS,
            receipt_name="dev_freeze_receipt.json",
            required_names=api.DEV_ARTIFACT_NAMES,
        )

    current = api.validate_complete_bundle(
        root,
        required_names=api.DEV_ARTIFACT_NAMES,
        receipt_name="dev_freeze_receipt.json",
    )
    assert current.generation != first.generation


def test_d020_sidecars_use_exact_canonical_order_and_mappingproxy():
    api = _api()
    hard = [
        MappingProxyType({"decoder_hard_output_sha256": "b" * 64, "payload": {"x": 2}}),
        MappingProxyType({"decoder_hard_output_sha256": "a" * 64, "payload": {"x": 1}}),
    ]
    provenance = [
        MappingProxyType({"payload": MappingProxyType({"logical_computation_id": "d0c1-b"})}),
        MappingProxyType({"payload": MappingProxyType({"logical_computation_id": "d0c1-a"})}),
    ]
    hard_bytes = api.canonical_jsonl_bytes(hard, sort_key="decoder_hard_output_sha256")
    provenance_bytes = api.canonical_jsonl_bytes(
        provenance, sort_key="payload.logical_computation_id"
    )
    assert hard_bytes.splitlines()[0].startswith(b'{"decoder_hard_output_sha256":"aaa')
    assert b'"logical_computation_id":"d0c1-a"' in provenance_bytes.splitlines()[0]


def _ledger_row(computation_id, *, status="EXECUTED", source=None, content="c" * 64,
                logical=(1, 16, 320), materialized=(1, 16, 320),
                hmm=(0, 0, 0)):
    return {
        "computation_id": computation_id,
        "cache_status": status,
        "source_computation_id": source,
        "content_sha256": content,
        "logical_decoder_batches": logical[0],
        "logical_cw_decodes": logical[1],
        "logical_bp_iterations": logical[2],
        "materialized_decoder_batches": materialized[0],
        "materialized_cw_decodes": materialized[1],
        "materialized_bp_iterations": materialized[2],
        "hmm_dual_pol_frame_parameter_pair_scores": hmm[0],
        "hmm_primitive_pol_trajectory_parameter_pair_scores": hmm[1],
        "materialized_hmm_primitive_pol_trajectory_parameter_pair_scores": hmm[2],
    }


def test_ledger_exec_cache_bp():
    api = _verify_api()
    rows = (
        _ledger_row("exec"),
        _ledger_row("cache", status="CACHE_READ", source="exec", materialized=(0, 0, 0)),
    )
    summary = api.reduce_cost_ledger(rows)
    assert summary.logical == (2, 32, 640)
    assert summary.materialized == (1, 16, 320)

    mutations = [
        rows + (rows[0],),
        (dict(rows[0], source_computation_id="cache"), rows[1]),
        (rows[0], dict(rows[1], source_computation_id="missing")),
        (rows[0], dict(rows[1], content_sha256="d" * 64)),
        (rows[0], dict(rows[1], materialized_cw_decodes=1,
                       materialized_bp_iterations=20)),
        (dict(rows[0], logical_bp_iterations=319), rows[1]),
    ]
    for bad in mutations:
        with pytest.raises(ValueError):
            api.reduce_cost_ledger(bad)


def test_ledger_frozen_totals():
    api = _verify_api()
    rows = (
        _ledger_row(
            "exec", logical=(48900, 704640, 14092800),
            materialized=(48900, 704640, 14092800),
            hmm=(3513600, 7027200, 7027200),
        ),
        _ledger_row(
            "cache", status="CACHE_READ", source="exec",
            logical=(20460, 327360, 6547200), materialized=(0, 0, 0),
            hmm=(4831200, 9662400, 0),
        ),
    )
    summary = api.reduce_cost_ledger(rows)
    api.assert_frozen_cost_totals(summary)
    assert summary.logical == (69360, 1032000, 20640000)
    assert summary.materialized == (48900, 704640, 14092800)
    assert summary.hmm == (8344800, 16689600, 7027200)
    with pytest.raises(ValueError, match="frozen"):
        api.assert_frozen_cost_totals(dataclasses.replace(
            summary, logical=(69359, 1032000, 20640000)
        ))


def test_s3_cache_no_exposure_drop():
    api = _verify_api()
    candidates = ("NOOP", "B04R1", "B04R2", "B04R3", "B08R1",
                  "B08R2", "B08R3", "B12R1", "B12R2", "B12R3")
    changed = (16, 12, 12, 12, 8, 8, 8, 4, 4, 4)
    rows = tuple(
        {
            "physical_case_id": case,
            "candidate_id": candidate,
            "computation_id": f"{case}-{candidate}",
            "changed_cw_decodes": count,
            "cached_unchanged_cw_nll_reads": 16 - count,
        }
        for case in ("case-a", "case-b")
        for candidate, count in zip(candidates, changed)
    )
    exposure = api.assert_s3_cache_exposure(rows)
    assert exposure == {"physical_cases": 2, "logical_computations": 20,
                        "changed_cw_decodes": 176,
                        "cached_unchanged_cw_nll_reads": 144}
    with pytest.raises(ValueError, match="ten|candidate|exposure"):
        api.assert_s3_cache_exposure(rows[:-1])
    with pytest.raises(ValueError, match="computation"):
        api.assert_s3_cache_exposure(rows[:-1] + (dict(rows[-1], computation_id=rows[0]["computation_id"]),))


def test_s3_cache_rejects_empty_rows():
    with pytest.raises(ValueError, match="non-empty"):
        _verify_api().assert_s3_cache_exposure(())


def test_s3_cache_rejects_fractional_counts_even_when_totals_balance():
    rows = list(_valid_s3_rows_for_negative_checks())
    rows[1] = dict(rows[1], changed_cw_decodes=12.5,
                   cached_unchanged_cw_nll_reads=3.5)
    rows[2] = dict(rows[2], changed_cw_decodes=11.5,
                   cached_unchanged_cw_nll_reads=4.5)
    with pytest.raises(ValueError, match="exact.*int"):
        _verify_api().assert_s3_cache_exposure(rows)


def test_s3_cache_rejects_negative_counts_even_when_totals_balance():
    rows = list(_valid_s3_rows_for_negative_checks())
    rows[1] = dict(rows[1], changed_cw_decodes=-1,
                   cached_unchanged_cw_nll_reads=17)
    rows[2] = dict(rows[2], changed_cw_decodes=25,
                   cached_unchanged_cw_nll_reads=-9)
    with pytest.raises(ValueError, match="non-negative"):
        _verify_api().assert_s3_cache_exposure(rows)


def _valid_s3_rows_for_negative_checks():
    candidates = ("NOOP", "B04R1", "B04R2", "B04R3", "B08R1",
                  "B08R2", "B08R3", "B12R1", "B12R2", "B12R3")
    changed = (16, 12, 12, 12, 8, 8, 8, 4, 4, 4)
    return tuple({
        "physical_case_id": "case",
        "candidate_id": candidate,
        "computation_id": f"case-{candidate}",
        "changed_cw_decodes": count,
        "cached_unchanged_cw_nll_reads": 16 - count,
    } for candidate, count in zip(candidates, changed))


def _s4_rows_and_evidence():
    verify_api = _verify_api()
    artifact_api = _api()
    rows = []
    evidence = {}
    for index, check_id in enumerate(verify_api.S4_CHECK_IDS):
        receipt = artifact_api.build_evidence_receipt(
            f"{check_id}.json", f"evidence-{index}".encode("ascii")
        )
        evidence[check_id] = receipt
        rows.append({
            "check_id": check_id,
            "tested_instances": 1,
            "failed_instances": 0,
            "passed": True,
            "evidence_sha256": receipt.sha256,
        })
    return tuple(rows), evidence


def test_s4_evidence_one_to_one():
    api = _verify_api()
    rows, evidence = _s4_rows_and_evidence()
    assert api.assert_independent_s4_evidence(rows, evidence) == api.S4_CHECK_IDS
    shared = dict(evidence)
    shared[api.S4_CHECK_IDS[-1]] = evidence[api.S4_CHECK_IDS[0]]
    with pytest.raises(ValueError, match="independent|one-to-one"):
        api.assert_independent_s4_evidence(rows, shared)


def test_s4_rejects_seven_caller_forged_receipts():
    api = _verify_api()
    rows, evidence = _s4_rows_and_evidence()
    receipt_type = _api().EvidenceReceipt
    forged = {}
    for check_id, real in evidence.items():
        fake = object.__new__(receipt_type)
        object.__setattr__(fake, "logical_name", real.logical_name)
        object.__setattr__(fake, "sha256", real.sha256)
        object.__setattr__(fake, "byte_count", real.byte_count)
        forged[check_id] = fake
    with pytest.raises(ValueError, match="issued|exact bytes"):
        api.assert_independent_s4_evidence(rows, forged)


def test_s4_reducer_fail_closed():
    api = _verify_api()
    rows, evidence = _s4_rows_and_evidence()
    ledger = api.CostLedgerSummary(
        logical=(69360, 1032000, 20640000),
        materialized=(48900, 704640, 14092800),
        hmm=(8344800, 16689600, 7027200),
        executed_rows=1,
        cache_read_rows=1,
    )
    result = api.reduce_s4_engineering(rows, evidence=evidence, ledger=ledger)
    assert result.status == "ENGINEERING_DIAGNOSTIC_PASS"
    assert result.scientific_verdict is None
    assert "PASS" not in dataclasses.asdict(result).keys()

    bad_sets = [
        rows[:-1],
        rows + (rows[-1],),
        rows[:-1] + (dict(rows[-1], failed_instances=1, passed=False),),
        rows[:-1] + (dict(rows[-1], evidence_sha256="f" * 64),),
    ]
    for bad in bad_sets:
        with pytest.raises(ValueError):
            api.reduce_s4_engineering(bad, evidence=evidence, ledger=ledger)


def test_no_common_p05_paths():
    api = _verify_api()
    allowed = (
        "projects/simulation/explore/coded-decoder-feedback/verify.py",
        "projects/simulation/explore/coded-decoder-feedback/artifacts.py",
        "projects/simulation/tests/test_d0_artifacts_cost_s4.py",
    )
    assert api.assert_i11_source_scope(allowed) == allowed
    for forbidden in (
        "projects/simulation/common/codec.py",
        "projects/simulation/explore/cma-fade-divergence/p05_run.log",
        "projects/simulation/explore/p08/adapter.py",
        "projects/simulation/explore/coded-decoder-feedback/source.py",
    ):
        with pytest.raises(ValueError, match="scope"):
            api.assert_i11_source_scope(allowed + (forbidden,))
