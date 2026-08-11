from collections import Counter
from dataclasses import fields, is_dataclass, replace
import hashlib
import inspect
import json
from pathlib import Path
import sys

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))

import contract
import schemas


OWNER = (
    SIMULATION_ROOT.parent
    / "thesis-fso"
    / "coded-decoder-feedback-groundwork"
    / "d0-defect-smoke-contract.yaml"
)
EXPECTED = {
    "S2_off": (540, 60),
    "S2_on": (1620, 1620),
    "S3": (10800, 10800),
    "BPS": (7200, 3600),
    "B2_clean": (1200, 600),
    "B2_controlled": (21600, 10800),
    "S4": (7, 7),
}


def _authority():
    return contract.load_owner_identity_authority(OWNER)


def _canonical_sha(value):
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _field_payload(field):
    return {"name": field.name, "atom": {"type": field.atom_type, "value": field.value}}


def _pk_payload(key):
    return {
        "schema": key.schema,
        "table": key.table,
        "fields": [_field_payload(field) for field in key.fields],
    }


def _work_payload(key):
    return {
        "schema": key.schema,
        "kind": key.kind,
        "fields": [_field_payload(field) for field in key.fields],
    }


def _field_map(key):
    return {field.name: field.value for field in key.fields}


def _clone_plan(plan, **changes):
    clone = object.__new__(type(plan))
    for field in fields(plan):
        object.__setattr__(clone, field.name, changes.get(field.name, getattr(plan, field.name)))
    return clone


def _unsafe_replace(value, **changes):
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(clone, field.name, changes.get(field.name, getattr(value, field.name)))
    return clone


def _nonprimitive_ids(value):
    found = set()

    def walk(item):
        if is_dataclass(item):
            found.add(id(item))
            for field in fields(item):
                walk(getattr(item, field.name))
        elif type(item) is tuple:
            found.add(id(item))
            for child in item:
                walk(child)

    walk(value)
    return found


def _ordinary_outputs(plan):
    zero_bits = np.zeros((16, 1024), dtype=np.uint8)
    first_bits = zero_bits.copy()
    first_bits[0, 0] = 1
    zero = schemas.build_decoder_hard_output_ref(zero_bits)
    first = schemas.build_decoder_hard_output_ref(first_bits)
    outputs = {}
    evidence = "69b9dd696310d530323e4e23dc50c4f98663f3f0c8cbc490e795717f8ed164f7"
    for binding in plan.bindings:
        values = _field_map(binding.consumer_primary_key)
        projection = binding.projection
        if projection == "S2_off":
            output = schemas.S2OffConsumerOutput(zero)
        elif projection == "S2_on":
            output = schemas.S2OnConsumerOutput(zero)
        elif projection == "S3":
            output = schemas.S3ConsumerOutput(zero, 0.0, 0.0)
        elif projection == "BPS":
            output = schemas.BpsConsumerOutput(
                zero if values["polarization"] == "X" else first, 0, 0.0
            )
        elif projection == "B2_clean":
            output = schemas.B2CleanConsumerOutput(
                zero if values["polarization"] == "X" else first
            )
        elif projection == "B2_controlled":
            output = schemas.B2ControlledConsumerOutput(
                zero if values["row_polarization"] == "X" else first
            )
        else:
            output = schemas.S4ConsumerOutput(1, 0, True, evidence)
        outputs[binding.consumer_primary_key] = output
    return outputs, zero, first


def test_ordinary_runtime_api_surface_is_complete():
    expected = (
        "S2OffConsumerOutput", "S2OnConsumerOutput", "S3ConsumerOutput",
        "BpsConsumerOutput", "B2CleanConsumerOutput",
        "B2ControlledConsumerOutput", "S4ConsumerOutput",
        "build_ordinary_runtime_bundle", "assert_ordinary_runtime_bundle",
    )
    assert [name for name in expected if not hasattr(schemas, name)] == []


def test_ordinary_runtime_full_counts_and_eight_owner_goldens():
    authority = _authority()
    plan = schemas.build_ordinary_identity_plan(owner_authority=authority)
    outputs, zero, first = _ordinary_outputs(plan)
    bundle = schemas.build_ordinary_runtime_bundle(
        plan=plan, owner_authority=authority, outputs_by_pk=outputs
    )
    assert dict(bundle.counts) == {
        "records": 27487, "entries": 42967, "executed_entries": 30247,
        "cache_read_entries": 12720, "s2_cache_edges": 480,
        "bps_cache_edges": 1440, "b2_cache_edges": 10800,
        "singleton_groups": 12427, "nine_entry_groups": 60,
        "two_entry_groups": 15000, "aggregate_executed": 26767,
        "aggregate_cache_read": 720,
    }
    assert len(bundle.records) == len(bundle.aggregate_ledger) == 27487
    assert len(bundle.hard_output_store) == 2
    assert {record.decoder_hard_output_sha256 for record in bundle.hard_output_store} == {
        zero.decoder_hard_output_sha256, first.decoder_hard_output_sha256
    }
    roots = {
        record.logical_computation_id: record.ordinary_consumer_provenance_manifest_sha256
        for record in bundle.records
    }
    expected = {
        "d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c": "e8ca16c947e87e35313907beb207fb1d0f913955f60279dff24b07c505f0ee06",
        "d0c1-bc7a3fa786ae125635dde06ae2987ebb9ab9936ea31522ad3acac44f50e113bb": "ee5f608c2a166fa2859c1db4badd4262376de7080d27c54e0eea37f8ce83e71a",
        "d0c1-42693a3970da884f507e8ab1a38233976978d326ef7e03cf07dc0c46a4451794": "8caf721a1f822b2beccab3e44c060a1c076fa1be05c47dc49e72af5ec388e61d",
        "d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb": "bb50e568db252417ec5542136f5ea8280edd816dee2c065e3c49d32228460145",
        "d0c1-7703ccf594fb2612e265b2f91204f437a8ce3bb87f97667e0f634b236839f797": "580d6d10ced5455e48945c57c109e2345e3281678943b55c514fa8d8fd4670bd",
        "d0c1-8f3f427b58e7b955a479f5364d3dd41dd2adde5e11fffff0730a8145bfdefd76": "5ab4e4d9b4dd7e249a8eb6ee6a2608de1e76d7dff1ef36cb74df11c81c3cba18",
        "d0c1-90218d05d733f0813ee9f5cd068c59af07c06d3ef970bb058673e860e24034ba": "25966bd9ae311efd0b7c22aa90965f7b9833877c92da7dfccda075282d7dc553",
        "d0c1-3a242617007121cf1e2e7b5f4a34d8330525b42236eb6b5f7ef8d5da5511ffe7": "cbe018c55b8d850546ae7ac5e2ff239dabacff168c2f134404db956daa1dccc5",
    }
    assert {key: roots[key] for key in expected} == expected
    schemas.assert_ordinary_runtime_bundle(
        bundle, plan=plan, owner_authority=authority
    )
    missing = dict(outputs)
    missing.pop(next(iter(missing)))
    extra = dict(outputs)
    extra[object()] = next(iter(outputs.values()))
    for mutant in (missing, extra):
        with pytest.raises(schemas.SchemaError):
            schemas.build_ordinary_runtime_bundle(
                plan=plan, owner_authority=authority, outputs_by_pk=mutant
            )


def test_ordinary_runtime_fresh_negatives_fail_closed():
    zero = schemas.build_decoder_hard_output_ref(np.zeros((16, 1024), dtype=np.uint8))
    invalid_calls = (
        lambda: schemas.S2OffConsumerOutput("0" * 64),
        lambda: schemas.S2OnConsumerOutput("0" * 64),
        lambda: schemas.S3ConsumerOutput("0" * 64, 0.0, 0.0),
        lambda: schemas.BpsConsumerOutput("0" * 64, 0, 0.0),
        lambda: schemas.B2CleanConsumerOutput("0" * 64),
        lambda: schemas.B2ControlledConsumerOutput("0" * 64),
        lambda: schemas.S3ConsumerOutput(zero, float("nan"), 0.0),
        lambda: schemas.S3ConsumerOutput(zero, 0, 0.0),
        lambda: schemas.S3ConsumerOutput(zero, 0.0, "0x0.0p+0"),
        lambda: schemas.BpsConsumerOutput(zero, True, 0.0),
        lambda: schemas.BpsConsumerOutput(zero, 4, 0.0),
        lambda: schemas.BpsConsumerOutput(zero, 0, float("inf")),
        lambda: schemas.S4ConsumerOutput(0, 0, True, "0" * 64),
        lambda: schemas.S4ConsumerOutput(1, 2, False, "0" * 64),
        lambda: schemas.S4ConsumerOutput(1, 0, False, "0" * 64),
        lambda: schemas.S4ConsumerOutput(1, 0, True, "x" * 64),
    )
    assert len(invalid_calls) == 16
    for call in invalid_calls:
        with pytest.raises((TypeError, ValueError)):
            call()


def test_ordinary_identity_exact_counts_and_domains():
    plan = schemas.build_ordinary_identity_plan(owner_authority=_authority())
    binding_counts = Counter(binding.projection for binding in plan.bindings)
    computation_counts = Counter(item.projection for item in plan.computations)
    assert binding_counts == {name: counts[0] for name, counts in EXPECTED.items()}
    assert computation_counts == {name: counts[1] for name, counts in EXPECTED.items()}
    assert (len(plan.bindings), len(plan.computations)) == (42967, 27487)
    assert len({binding.consumer_primary_key for binding in plan.bindings}) == 42967
    assert len({item.computation_id for item in plan.computations}) == 27487
    assert {item.operation for item in plan.computations if item.projection == "S2_on"} == {
        "B1_DECODE", "B2_DECODE", "O1_DECODE"
    }
    assert {item.phase for item in plan.computations if item.projection == "S3"} == {
        "S3_DEV", "S3_TEST"
    }
    assert all(not hasattr(item, "cache_status") for item in plan.computations)
    assert all(not hasattr(item, "source_computation_id") for item in plan.computations)
    schemas.assert_ordinary_identity_plan(plan, owner_authority=_authority())


def test_ordinary_identity_many_to_one_and_golden_roots():
    plan = schemas.build_ordinary_identity_plan(owner_authority=_authority())
    s2 = [
        binding for binding in plan.bindings
        if binding.projection == "S2_off"
        and _field_map(binding.consumer_primary_key)["seed"] == 8150
        and _field_map(binding.consumer_primary_key)["cell_id"] == "hard"
        and _field_map(binding.consumer_primary_key)["target_polarization"] == "X"
    ]
    assert len(s2) == 9
    assert len({binding.logical_computation_id for binding in s2}) == 1
    assert s2[0].logical_computation_id == "d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c"
    s2_manifest = {
        "schema": "coded_decoder_feedback.d0.consumer_binding_manifest.v1",
        "binding_kind": "LOGICAL_COMPUTATION_ID",
        "bindings": [
            {"consumer_primary_key": _pk_payload(binding.consumer_primary_key),
             "logical_computation_id": binding.logical_computation_id}
            for binding in s2
        ],
    }
    assert _canonical_sha(s2_manifest) == "ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6"

    bps = [
        binding for binding in plan.bindings
        if binding.projection == "BPS"
        and _field_map(binding.consumer_primary_key) | {} == {
            "record_type": "BPS_DEV_SCORE", "tuple_id": "M2_N100", "B": 32,
            "Nw": 31, "seed": 8000, "cell_id": "snr_10db__linewidth_10000hz",
            "polarization": _field_map(binding.consumer_primary_key)["polarization"],
        }
    ]
    assert len(bps) == 2
    assert [ _field_map(binding.consumer_primary_key)["polarization"] for binding in bps] == ["X", "Y"]
    assert len({binding.logical_computation_id for binding in bps}) == 1
    assert bps[0].logical_computation_id == "d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb"
    bps_manifest = {
        "schema": "coded_decoder_feedback.d0.consumer_binding_manifest.v1",
        "binding_kind": "LOGICAL_COMPUTATION_ID",
        "bindings": [
            {"consumer_primary_key": _pk_payload(binding.consumer_primary_key),
             "logical_computation_id": binding.logical_computation_id}
            for binding in bps
        ],
    }
    assert _canonical_sha(bps_manifest) == "51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f"

    for projection, expected_group in (("B2_clean", 2), ("B2_controlled", 2)):
        grouped = Counter(binding.logical_computation_id for binding in plan.bindings
                          if binding.projection == projection)
        assert set(grouped.values()) == {expected_group}


def test_ordinary_identity_authority_type_and_fresh_nonalias():
    authority = _authority()
    left = schemas.build_ordinary_identity_plan(owner_authority=authority)
    right = schemas.build_ordinary_identity_plan(owner_authority=authority)
    assert left == right
    assert _nonprimitive_ids(left).isdisjoint(_nonprimitive_ids(right))
    object.__setattr__(left.bindings[0], "logical_computation_id", "d0c1-" + "0" * 64)
    assert left != right
    schemas.assert_ordinary_identity_plan(right, owner_authority=authority)
    with pytest.raises(schemas.SchemaError):
        schemas.assert_ordinary_identity_plan(left, owner_authority=authority)
    for wrong in (authority.contract, {}, schemas.ComputationPreexecutionPlan):
        with pytest.raises((schemas.SchemaError, TypeError)):
            schemas.build_ordinary_identity_plan(owner_authority=wrong)
    with pytest.raises(schemas.SchemaError):
        schemas.OrdinaryIdentityPlan()


def test_ordinary_identity_mutations_fail_closed():
    authority = _authority()
    plan = schemas.build_ordinary_identity_plan(owner_authority=authority)
    b0 = plan.bindings[0]
    b1 = next(item for item in plan.bindings if item.logical_computation_id != b0.logical_computation_id)
    c0, c1 = plan.computations[0], plan.computations[1]
    pk = b0.consumer_primary_key
    pk_fields = pk.fields
    work = c0.work_key
    work_fields = work.fields
    mutations = [
        _clone_plan(plan, bindings=plan.bindings[:-1]),
        _clone_plan(plan, bindings=plan.bindings + (b0,)),
        _clone_plan(plan, bindings=(b0,) + plan.bindings),
        _clone_plan(plan, bindings=(replace(b0, logical_computation_id="d0c1-" + "f" * 64),) + plan.bindings[1:]),
        _clone_plan(plan, bindings=(replace(b0, logical_computation_id=b1.logical_computation_id),) + plan.bindings[1:]),
        _clone_plan(plan, owner_sha256="0" * 64),
        _clone_plan(plan, identity_binding_sha256="0" * 64),
        _clone_plan(plan, computations=plan.computations[:-1]),
        _clone_plan(plan, computations=plan.computations + (c0,)),
        _clone_plan(plan, computations=(c0,) + plan.computations),
        _clone_plan(plan, computations=(replace(c0, computation_id="d0c1-" + "0" * 64),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, phase="S3_DEV"),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, operation="O1_DECODE"),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, schema="wrong"),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, work_key=replace(work, kind="wrong")),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, work_key=replace(work, fields=(replace(work_fields[0], name="wrong"),) + work_fields[1:])),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, work_key=replace(work, fields=(_unsafe_replace(work_fields[0], atom_type="str"),) + work_fields[1:])),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, work_key=replace(work, fields=(replace(work_fields[0], value=999),) + work_fields[1:])),) + plan.computations[1:]),
        _clone_plan(plan, computations=(replace(c0, work_key=replace(work, fields=tuple(reversed(work_fields)))),) + plan.computations[1:]),
        _clone_plan(plan, bindings=(replace(b0, binding_kind="OTHER"),) + plan.bindings[1:]),
        _clone_plan(plan, bindings=(replace(b0, projection="S3"),) + plan.bindings[1:]),
        _clone_plan(plan, bindings=(_unsafe_replace(b0, table="other"),) + plan.bindings[1:]),
        _clone_plan(plan, bindings=(replace(b0, consumer_primary_key=replace(pk, schema="wrong")),) + plan.bindings[1:]),
        _clone_plan(plan, bindings=(replace(b0, consumer_primary_key=replace(pk, fields=(replace(pk_fields[0], value="wrong"),) + pk_fields[1:])),) + plan.bindings[1:]),
    ]
    assert len(mutations) == 24
    for mutation in mutations:
        with pytest.raises(schemas.SchemaError):
            schemas.assert_ordinary_identity_plan(mutation, owner_authority=authority)


def test_ordinary_identity_is_invariant_to_schema_module_domains(monkeypatch):
    authority = _authority()
    baseline = schemas.build_ordinary_identity_plan(owner_authority=authority)
    monkeypatch.setattr(schemas, "CANDIDATES", ("NOOP",) * 10)
    monkeypatch.setattr(schemas, "S2_METHODS", ("FORGED",) * 3)
    monkeypatch.setattr(schemas, "S4_CHECK_IDS", ("FORGED",) * 7)
    monkeypatch.setattr(schemas, "TUPLES", ("FORGED",) * 5)
    forged_environment = schemas.build_ordinary_identity_plan(owner_authority=authority)
    assert forged_environment == baseline
    schemas.assert_ordinary_identity_plan(baseline, owner_authority=authority)


def test_ordinary_raw_enumeration_has_no_parallel_domain_authority():
    source = inspect.getsource(schemas._ordinary_raw_records)
    for forbidden in (
        "CANDIDATES", "S2_METHODS", "S4_CHECK_IDS", "TUPLES",
        'aliases = ("hard", "mid", "clean")', "(32, 64)", "(31, 61, 127)",
        '"S2_METHOD"', '"S3_CANDIDATE_DEV"', '"S4_CHECK"',
        '"BPS_DEV_SCORE"', '"B2_TUPLE_CLEAN_DEV"',
        '"B2_TUPLE_CONTROLLED_DEV"',
    ):
        assert forbidden not in source


def test_ordinary_domain_and_seal_tamper_fail_closed():
    authority = _authority()
    domain = authority.ordinary_domain
    mutations = (
        replace(authority, ordinary_domain=replace(domain, controlled_cell_aliases=("hard", "mid", "forged"))),
        replace(authority, ordinary_domain=replace(domain, candidates=domain.candidates[:-1] + ("FORGED",))),
        replace(authority, ordinary_domain=replace(domain, s2_methods=("FORGED",) + domain.s2_methods[1:])),
        replace(authority, ordinary_domain=replace(domain, b_values=(32, 128))),
        replace(authority, ordinary_domain=replace(domain, nw_values=(31, 61, 255))),
        replace(authority, ordinary_domain=replace(domain, s3_record_types=("S3_CANDIDATE_DEV", "FORGED"))),
        replace(authority, ordinary_domain_sha256="0" * 64),
        replace(authority, ordinary_domain={}),
    )
    assert len(mutations) == 8
    for mutation in mutations:
        with pytest.raises(contract.ContractError):
            contract.assert_frozen_owner_identity_authority(mutation)
        with pytest.raises(schemas.SchemaError):
            schemas.build_ordinary_identity_plan(owner_authority=mutation)
