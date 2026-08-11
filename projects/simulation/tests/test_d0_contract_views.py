import copy
from dataclasses import dataclass, fields, replace
import hashlib
import importlib
from itertools import combinations
import json
from pathlib import Path
import sys
from types import MappingProxyType
from collections.abc import Mapping

import numpy as np
import pytest
import yaml


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))

import contract as contract_module
from contract import ContractError, assert_action_authorized, load_contract


OWNER = (
    SIMULATION_ROOT.parent
    / "thesis-fso"
    / "coded-decoder-feedback-groundwork"
    / "d0-defect-smoke-contract.yaml"
)


@pytest.fixture(scope="module")
def d0_contract():
    return load_contract(OWNER)


_OWNER_SHA256 = "f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b"
_SCIENTIFIC_PROJECTION_SHA256 = (
    "c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d"
)
_IDENTITY_BINDING_SHA256 = (
    "08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e"
)
_GRID_ROOTS = {
    "p_s": "bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864",
    "sigma_e2": "0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca",
    "combined": "0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf",
}
_D020_ROOTS = {
    "ordinary_hard_output_zero": "1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960",
    "ordinary_hard_output_first_bit": "9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e",
    "ordinary_S2_off_nine_to_one": "e8ca16c947e87e35313907beb207fb1d0f913955f60279dff24b07c505f0ee06",
    "ordinary_S2_on_singleton": "ee5f608c2a166fa2859c1db4badd4262376de7080d27c54e0eea37f8ce83e71a",
    "ordinary_S3_singleton": "8caf721a1f822b2beccab3e44c060a1c076fa1be05c47dc49e72af5ec388e61d",
    "ordinary_BPS_M2_source": "bb50e568db252417ec5542136f5ea8280edd816dee2c065e3c49d32228460145",
    "ordinary_BPS_M3_cache": "580d6d10ced5455e48945c57c109e2345e3281678943b55c514fa8d8fd4670bd",
    "ordinary_B2_clean": "5ab4e4d9b4dd7e249a8eb6ee6a2608de1e76d7dff1ef36cb74df11c81c3cba18",
    "ordinary_B2_controlled_target_and_sentinel": "25966bd9ae311efd0b7c22aa90965f7b9833877c92da7dfccda075282d7dc553",
    "ordinary_S4_singleton": "cbe018c55b8d850546ae7ac5e2ff239dabacff168c2f134404db956daa1dccc5",
}


def _plain_identity(value):
    """Independent test-side conversion of the immutable public view."""

    if isinstance(value, contract_module.Float64Literal):
        return {"index": value.index, "float64_hex": value.float64_hex}
    if isinstance(value, Mapping):
        return {key: _plain_identity(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain_identity(item) for item in value]
    return value


def _canonical_sha256(value):
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _owner_document():
    return yaml.safe_load(OWNER.read_text(encoding="utf-8"))


def _write_mutated_owner(tmp_path, name, document):
    path = tmp_path / f"{name}.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


def test_owner_identity_authority_exact_frozen_view():
    authority = contract_module.load_owner_identity_authority(OWNER)
    binding = authority.identity_binding

    assert tuple(field.name for field in fields(binding)) == (
        "schema_version",
        "decision_ref",
        "scientific_contract_change",
        "canonical_serialization",
        "grid_authority",
        "payload_schemas",
        "hmm_authority",
        "ledger_accounting",
        "cache_source",
        "consumer_bindings",
        "runtime_content",
        "golden_vectors",
        "validator_obligations",
    )
    assert binding.schema_version == "coded_decoder_feedback.d0.identity_binding.v1"
    assert binding.decision_ref == "D015"
    assert binding.scientific_contract_change == "none"
    assert authority.owner_sha256 == _OWNER_SHA256
    assert authority.scientific_projection_sha256 == _SCIENTIFIC_PROJECTION_SHA256
    assert authority.identity_binding_sha256 == _IDENTITY_BINDING_SHA256
    assert type(binding.grid_authority).__name__ == "_FrozenDict"
    assert tuple(item.index for item in binding.grid_authority["p_s"]["anchors"]) == (
        0,
        1,
        61,
        121,
    )

    with pytest.raises(TypeError):
        binding.grid_authority["new"] = "forbidden"
    with pytest.raises((AttributeError, TypeError)):
        binding.grid_authority["p_s"]["anchors"][0].index = 99

    detached = _plain_identity(binding.grid_authority)
    detached["p_s"]["count"] = -1
    assert binding.grid_authority["p_s"]["count"] == 122

    fresh = contract_module.load_owner_identity_authority(OWNER)
    assert fresh == authority
    assert fresh.identity_binding.grid_authority is not binding.grid_authority
    assert fresh.identity_binding.grid_authority["p_s"] is not binding.grid_authority["p_s"]

    forged_hash = replace(authority, identity_binding_sha256="0" * 64)
    with pytest.raises(ContractError):
        contract_module.assert_frozen_owner_identity_authority(forged_hash)
    forged_view = replace(binding, scientific_contract_change="changed")
    with pytest.raises(ContractError):
        contract_module.assert_frozen_owner_identity_authority(
            replace(authority, identity_binding=forged_view)
        )


def test_owner_identity_grid_commitments_recompute_exact():
    authority = contract_module.load_owner_identity_authority(OWNER)
    grid = authority.identity_binding.grid_authority

    p_s = _plain_identity(grid["p_s"]["standalone_payload"])
    sigma = _plain_identity(grid["sigma_e2"]["standalone_payload"])
    combined = _plain_identity(grid["combined"]["payload"])
    assert len(p_s["values"]) == 122
    assert len(sigma["values"]) == 6
    assert [entry["index"] for entry in p_s["values"]] == list(range(122))
    assert [entry["index"] for entry in sigma["values"]] == list(range(6))
    assert _canonical_sha256(p_s) == _GRID_ROOTS["p_s"] == grid["p_s"]["sha256"]
    assert _canonical_sha256(sigma) == _GRID_ROOTS["sigma_e2"] == grid["sigma_e2"]["sha256"]
    assert combined["p_s"] == p_s
    assert combined["sigma_e2"] == sigma
    assert _canonical_sha256(combined) == _GRID_ROOTS["combined"] == grid["combined"]["sha256"]


def test_owner_identity_d017_descriptors_and_hmm_reference_exact():
    binding = contract_module.load_owner_identity_authority(OWNER).identity_binding
    projections = _plain_identity(binding.consumer_bindings)["projections"]
    ordinary_names = (
        "S2_off",
        "S2_on",
        "S3",
        "BPS",
        "B2_clean",
        "B2_controlled",
        "S4",
    )
    assert tuple(projections) == ordinary_names[:-1] + ("HMM_chunk", "S4")

    expected_signatures = {
        "S2_off": (
            {"kind": "literal", "value": "S2"},
            {"kind": "literal", "value": "B1_DECODE"},
            "S2_B1_OFF_CANONICAL_B04",
        ),
        "S2_on": (
            {"kind": "literal", "value": "S2"},
            {
                "kind": "enum_map",
                "source": "raw.method_id",
                "values": {
                    "GLOBAL_FOUR_ROTATION_DECODER_SELECTION": "B1_DECODE",
                    "OFC17_16QAM_EXTFRAME_V1": "B2_DECODE",
                    "TRUTH_BOUNDARY_ROTATION_CORRECTION": "O1_DECODE",
                },
            },
            "S2_ON_METHOD_DECODE",
        ),
        "S3": (
            {
                "kind": "enum_map",
                "source": "raw.record_type",
                "values": {
                    "S3_CANDIDATE_DEV": "S3_DEV",
                    "S3_CANDIDATE_TEST": "S3_TEST",
                },
            },
            {"kind": "literal", "value": "CANDIDATE_DECODE"},
            "S3_CANDIDATE_DECODE",
        ),
        "BPS": (
            {"kind": "literal", "value": "BPS_DEV"},
            {"kind": "literal", "value": "B1_DECODE"},
            "BPS_DUAL_POL_SHARED",
        ),
        "B2_clean": (
            {"kind": "literal", "value": "B2_DEV"},
            {"kind": "literal", "value": "B2_DECODE"},
            "B2_CLEAN_DUAL_POL_SHARED",
        ),
        "B2_controlled": (
            {"kind": "literal", "value": "B2_DEV"},
            {"kind": "literal", "value": "B2_DECODE"},
            "B2_CONTROLLED_DUAL_POL_SHARED",
        ),
        "S4": (
            {"kind": "literal", "value": "S4"},
            {"kind": "literal", "value": "OTHER_S4_CHECK"},
            "S4_STANDALONE_CHECK",
        ),
    }
    assert len(expected_signatures) + 1 == 8
    for name, signature in expected_signatures.items():
        projection = projections[name]
        assert projection["exact_binding_kind"] == "LOGICAL_COMPUTATION_ID"
        assert (
            projection["phase_rule"],
            projection["operation_rule"],
            projection["work_key_kind"],
        ) == signature

    descriptor_keys = ("name", "source", "atom_type")
    consumer_descriptors = [
        descriptor
        for name in ordinary_names
        for descriptor in projections[name]["consumer_pk_fields"]
    ]
    work_descriptors = [
        descriptor
        for name in ordinary_names
        for descriptor in projections[name]["work_key_fields"]
    ]
    hmm_descriptors = projections["HMM_chunk"]["consumer_pk_fields"]
    assert (len(work_descriptors), len(consumer_descriptors), len(consumer_descriptors) + len(hmm_descriptors)) == (32, 41, 49)
    for descriptor in consumer_descriptors + work_descriptors + hmm_descriptors:
        assert tuple(descriptor) == descriptor_keys
        assert descriptor["atom_type"] in {"str", "int", "bool"}

    assert projections["S4"]["exact_check_ids"] == [
        "no_slip_noiseless_B0_B1_O1_identity",
        "all_rotation_boundary_noiseless_O1_zero_error",
        "mapping_rotation_truth_metamorphic_pass",
        "candidate_isolation_and_empty_decoder_state_pass",
        "all_scores_finite_and_deterministic",
        "no_truth_field_reaches_receiver_view",
        "diagnostic_cost_ledger_complete",
    ]
    hmm = projections["HMM_chunk"]
    assert "exact_binding_kind" not in hmm
    assert all(key not in hmm for key in ("phase_rule", "operation_rule", "work_key_kind", "work_key_fields"))
    assert hmm["reference"] == {
        "kind": "COMPUTATION_IDS_MANIFEST_SHA256",
        "raw_field": "computation_ids_manifest_sha256",
        "payload_schema": "coded_decoder_feedback.d0.computation_id_manifest.v1",
        "rule": "exact_typed_chunk_primary_key_equals_group_consumer_primary_key",
        "logical_member_authority": "hmm_authority.logical_computation",
    }


def test_owner_identity_d020_runtime_content_exact_frozen_view():
    authority = contract_module.load_owner_identity_authority(OWNER)
    binding = authority.identity_binding
    payloads = _plain_identity(binding.payload_schemas)
    expected_versions = {
        "decoder_hard_output": "coded_decoder_feedback.d0.decoder_hard_output.v1",
        "decoder_hard_output_store_record": "coded_decoder_feedback.d0.decoder_hard_output_store_record.v1",
        "consumer_output_S2_off": "coded_decoder_feedback.d0.consumer_output.s2_off.v1",
        "consumer_output_S2_on": "coded_decoder_feedback.d0.consumer_output.s2_on.v1",
        "consumer_output_S3": "coded_decoder_feedback.d0.consumer_output.s3.v1",
        "consumer_output_BPS": "coded_decoder_feedback.d0.consumer_output.bps.v1",
        "consumer_output_B2_clean": "coded_decoder_feedback.d0.consumer_output.b2_clean.v1",
        "consumer_output_B2_controlled": "coded_decoder_feedback.d0.consumer_output.b2_controlled.v1",
        "consumer_output_S4": "coded_decoder_feedback.d0.consumer_output.s4.v1",
        "ordinary_consumer_provenance": "coded_decoder_feedback.d0.ordinary_consumer_provenance.v1",
        "ordinary_consumer_provenance_store_record": "coded_decoder_feedback.d0.ordinary_consumer_provenance_store_record.v1",
    }
    expected_orders = {
        "decoder_hard_output": [
            "schema", "cw_count", "information_bits_per_cw", "cw_order",
            "bit_packing", "decoded_information_bits_base64",
        ],
        "decoder_hard_output_store_record": [
            "schema", "decoder_hard_output_sha256", "payload",
        ],
        "consumer_output_S2_off": ["schema", "decoder_hard_output_sha256"],
        "consumer_output_S2_on": ["schema", "decoder_hard_output_sha256"],
        "consumer_output_S3": [
            "schema", "decoder_hard_output_sha256", "pilot_score_float64_hex",
            "decoder_score_float64_hex",
        ],
        "consumer_output_BPS": [
            "schema", "decoder_hard_output_sha256", "selected_global_rotation_k",
            "selected_normalized_reencode_nll_float64_hex",
        ],
        "consumer_output_B2_clean": ["schema", "decoder_hard_output_sha256"],
        "consumer_output_B2_controlled": ["schema", "decoder_hard_output_sha256"],
        "consumer_output_S4": [
            "schema", "tested_instances", "failed_instances", "passed",
            "evidence_sha256",
        ],
        "ordinary_consumer_provenance": [
            "schema", "logical_computation_id", "entries",
        ],
        "ordinary_consumer_provenance_store_record": [
            "schema", "ordinary_consumer_provenance_manifest_sha256", "payload",
        ],
    }
    assert {
        name: payloads[name]["version"] for name in expected_versions
    } == expected_versions
    assert {
        name: payloads[name]["exact_object_field_order"] for name in expected_orders
    } == expected_orders
    assert payloads["ordinary_consumer_provenance"]["entry_exact_object_field_order"] == [
        "ordinal", "consumer_primary_key", "consumer_output", "cache_status",
        "source_computation_id", "source_consumer_primary_key",
    ]
    assert payloads["decoder_hard_output"]["constants"] == {
        "cw_count": 16,
        "information_bits_per_cw": 1024,
        "cw_order": "TRANSMITTED_CW_INDEX_0_THROUGH_15",
        "bit_packing": "CW_MAJOR_MSB_FIRST_RFC4648_BASE64",
    }
    assert payloads["decoder_hard_output"]["total_information_bits"] == 16384
    assert payloads["decoder_hard_output"]["decoded_bytes"] == 2048
    assert payloads["decoder_hard_output"]["base64"] == {
        "alphabet": "RFC4648_standard",
        "encoded_length": 2732,
        "padding": "exactly_one_equals",
        "whitespace": "forbidden",
        "round_trip": "exact",
    }

    runtime = _plain_identity(binding.runtime_content)
    assert runtime["ordinary_decoder_hard_output"] == {
        "payload_schema": "coded_decoder_feedback.d0.decoder_hard_output.v1",
        "store_record_schema": "coded_decoder_feedback.d0.decoder_hard_output_store_record.v1",
        "filename": "decoder_hard_outputs.jsonl",
        "typed_ref_factory": "D0Codec.decode_fresh_binary_bits_immediately_canonicalized",
        "arbitrary_hash_string_input": "forbidden",
        "record_sort": "decoder_hard_output_sha256_lowercase_lexicographic",
        "record_encoding": "canonical_JSON_then_exact_LF_including_final_record",
        "cardinality": "distinct_referenced_decoder_hard_output_sha256",
        "forward_FK": "every_non_S4_consumer_output_root_exists_exactly_once",
        "reverse_FK": "every_store_root_is_referenced",
    }
    provenance = runtime["ordinary_consumer_provenance"]
    assert {
        key: provenance[key]
        for key in (
            "payload_schema", "store_record_schema", "filename",
            "one_record_per_logical_computation_id", "record_sort",
            "record_encoding", "entry_ordinals", "output_forbidden_fields",
        )
    } == {
        "payload_schema": "coded_decoder_feedback.d0.ordinary_consumer_provenance.v1",
        "store_record_schema": "coded_decoder_feedback.d0.ordinary_consumer_provenance_store_record.v1",
        "filename": "ordinary_consumer_provenance.jsonl",
        "one_record_per_logical_computation_id": True,
        "record_sort": "logical_computation_id_lowercase_lexicographic",
        "record_encoding": "canonical_JSON_then_exact_LF_including_final_record",
        "entry_ordinals": "zero_based_contiguous_in_exact_group_order",
        "output_forbidden_fields": [
            "consumer_primary_key", "receipt", "truth", "cost", "ledger",
            "provenance_root",
        ],
    }
    assert provenance["groups"] == {
        "S2_off": {
            "entry_order": [
                "B04_K1", "B04_K2", "B04_K3", "B08_K1", "B08_K2",
                "B08_K3", "B12_K1", "B12_K2", "B12_K3",
            ],
            "B04_K1": {
                "cache_status": "EXECUTED",
                "source_computation_id": None,
                "source_consumer_primary_key": None,
            },
            "other_eight": "direct_CACHE_READ_to_same_logical_id_B04_K1_PK",
        },
        "S2_on": {"entry_order": "singleton", "cache_status": "EXECUTED"},
        "S3": {"entry_order": "singleton", "cache_status": "EXECUTED"},
        "BPS": {
            "entry_order": ["X", "Y"],
            "M3_N100": "direct_CACHE_READ_to_M2_N100_same_polarization",
            "all_other_tuples": "EXECUTED",
        },
        "B2_clean": {"entry_order": ["X", "Y"], "cache_status": "EXECUTED"},
        "B2_controlled": {
            "entry_order": ["TARGET_INCLUDED", "SENTINEL_EXCLUDED"],
            "TARGET_INCLUDED": {
                "row_relation": "row_polarization_equals_target_polarization",
                "cache_status": "EXECUTED",
            },
            "SENTINEL_EXCLUDED": {
                "row_relation": "row_polarization_is_opposite_target_polarization",
                "cache_status": "CACHE_READ",
                "direct_source": "same_tuple_seed_cell_row_polarization_B2_clean_PK",
            },
        },
        "S4": {"entry_order": "singleton", "cache_status": "EXECUTED"},
    }
    assert provenance["source_gate"] == {
        "direction": "CACHE_READ_consumer_to_direct_EXECUTED_source",
        "source_leaf": "EXECUTED_with_both_source_fields_null",
        "source_computation_id_and_consumer_primary_key": "exact",
        "consumer_output": "canonical_deep_equal_to_source_output",
        "cache_chain": "forbidden",
    }
    assert runtime["ordinary_static_counts"] == {
        "manifests_and_ledger_rows": 27487,
        "entries": 42967,
        "executed_entries": 30247,
        "cache_read_entries": 12720,
        "cache_edges": {
            "S2_off": 480, "BPS_M3_N100": 1440,
            "B2_controlled_sentinel": 10800, "total": 12720,
        },
        "groups": {"singleton": 12427, "nine_entry": 60, "two_entry": 15000},
        "group_equation": "12427_plus_60_times_9_plus_15000_times_2_equals_42967",
        "aggregate_ledger": {"EXECUTED": 26767, "CACHE_READ": 720, "total": 27487},
        "ordinary_plus_HMM_total_ledger_rows": 50287,
        "non_S4_entries_with_hard_output_FK": 42960,
    }
    assert runtime["ordinary_aggregate_ledger"] == {
        "row_per_logical_computation_id": "exactly_one",
        "any_entry_EXECUTED": {
            "cache_status": "EXECUTED", "source_computation_id": None,
        },
        "all_entries_CACHE_READ_one_unique_source": {
            "cache_status": "CACHE_READ", "source_computation_id": "unique_source",
        },
        "mixed_or_multiple_cache_sources_without_execution": "reject",
        "content_sha256": "ordinary_consumer_provenance_payload_root",
        "HMM_path": "separate_manifest_without_this_sidecar",
    }
    assert runtime["ordinary_sidecars"] == {
        "required_files": [
            "decoder_hard_outputs.jsonl", "ordinary_consumer_provenance.jsonl",
        ],
        "final_receipt_required_hash_fields": [
            "decoder_hard_outputs_sha256",
            "ordinary_consumer_provenance_sha256",
        ],
        "final_receipt_also_binds": [
            "owner_sha256", "source_bundle_sha256", "code_bundle_sha256",
            "dev_freeze_sha256", "seed_manifest_sha256",
            "every_raw_file_sha256", "computation_ledger_sha256",
        ],
        "provenance_forward_reverse": "all_42967_consumer_PKs_exactly_once_no_orphan",
        "hard_output_forward_reverse": "all_42960_non_S4_entries_resolve_and_no_store_orphan",
    }
    assert runtime["ordinary_write_anchor"] == {
        "exact_order": [
            "hard_output_temp", "provenance_raw_ledger_temp",
            "full_bundle_validation", "unified_atomic_publish", "final_receipt",
        ],
        "partial_publish": "forbidden",
        "partial_artifact_cannot_be_FULL": True,
    }

    goldens = _plain_identity(binding.golden_vectors)
    assert len(goldens) == 20
    assert tuple(goldens)[-10:] == tuple(_D020_ROOTS)
    observed_roots = {
        name: (
            golden["decoder_hard_output_sha256"]
            if name.startswith("ordinary_hard_output_")
            else golden["ordinary_consumer_provenance_manifest_sha256"]
        )
        for name, golden in goldens.items()
        if name in _D020_ROOTS
    }
    assert observed_roots == _D020_ROOTS
    for name in ("ordinary_hard_output_zero", "ordinary_hard_output_first_bit"):
        payload = json.loads(goldens[name]["inputs"]["canonical_payload_json"])
        assert len(payload["decoded_information_bits_base64"]) == 2732
        assert payload["decoded_information_bits_base64"].count("=") == 1
        assert _canonical_sha256(payload) == _D020_ROOTS[name]
    assert goldens["ordinary_B2_controlled_target_and_sentinel"]["inputs"][
        "entry_order"
    ] == ["TARGET_INCLUDED", "SENTINEL_EXCLUDED"]
    assert goldens["ordinary_S4_singleton"]["inputs"]["consumer_output"][
        "evidence_sha256"
    ] == "69b9dd696310d530323e4e23dc50c4f98663f3f0c8cbc490e795717f8ed164f7"

    with pytest.raises(TypeError):
        binding.runtime_content["ordinary_static_counts"]["entries"] = 0
    with pytest.raises(TypeError):
        binding.golden_vectors["ordinary_B2_clean"]["inputs"]["raw_shared"][
            "tuple_id"
        ] = "M3_N100"
    fresh = contract_module.load_owner_identity_authority(OWNER)
    assert fresh == authority
    assert fresh.identity_binding.runtime_content is not binding.runtime_content
    assert (
        fresh.identity_binding.runtime_content["ordinary_consumer_provenance"]["groups"]
        is not binding.runtime_content["ordinary_consumer_provenance"]["groups"]
    )


def test_owner_identity_mutations_fail_closed(tmp_path):
    original = _owner_document()
    mutations = []

    def add(name, mutate):
        document = copy.deepcopy(original)
        mutate(document["identity_binding_contract"])
        mutations.append((name, _write_mutated_owner(tmp_path, name, document)))

    add("omitted", lambda identity: identity.pop("runtime_content"))
    add("extra", lambda identity: identity.__setitem__("extra", {}))
    add("schema_header", lambda identity: identity.__setitem__("schema_version", 1))
    add("decision_header", lambda identity: identity.__setitem__("decision_ref", "D014"))
    add("science_header", lambda identity: identity.__setitem__("scientific_contract_change", True))
    add("section_nonmapping", lambda identity: identity.__setitem__("cache_source", []))
    add(
        "literal_index",
        lambda identity: identity["grid_authority"]["p_s"]["standalone_payload"]["values"][1].__setitem__("index", 2),
    )
    add(
        "literal_hex",
        lambda identity: identity["grid_authority"]["sigma_e2"]["standalone_payload"]["values"][1].__setitem__("float64_hex", "0x0.0p+0"),
    )
    add(
        "literal_order",
        lambda identity: identity["grid_authority"]["p_s"]["standalone_payload"]["values"].reverse(),
    )
    add(
        "grid_root",
        lambda identity: identity["grid_authority"]["p_s"].__setitem__("sha256", "0" * 64),
    )
    add(
        "combined_deep_equality",
        lambda identity: identity["grid_authority"]["combined"]["payload"]["p_s"].__setitem__("name", "changed"),
    )
    add(
        "golden_root",
        lambda identity: identity["golden_vectors"]["grid_commitments"].__setitem__("p_s_sha256", "0" * 64),
    )
    add(
        "consumer_binding_kind",
        lambda identity: identity["consumer_bindings"]["projections"]["S2_off"].__setitem__("exact_binding_kind", "OTHER"),
    )
    add(
        "ledger_count",
        lambda identity: identity["ledger_accounting"]["formulas"]["chunks"].__setitem__("expected", 0),
    )
    add(
        "cache_source",
        lambda identity: identity["cache_source"].__setitem__("canonical_N100_executed_owner", "M3_N100"),
    )
    add(
        "d017_ordinary_kind",
        lambda identity: identity["consumer_bindings"]["projections"]["BPS"].__setitem__("work_key_kind", "B2_CLEAN_DUAL_POL_SHARED"),
    )
    add(
        "d017_ordinary_phase",
        lambda identity: identity["consumer_bindings"]["projections"]["S2_off"]["phase_rule"].__setitem__("value", "S3_DEV"),
    )
    add(
        "d017_ordinary_operation",
        lambda identity: identity["consumer_bindings"]["projections"]["B2_clean"]["operation_rule"].__setitem__("value", "B1_DECODE"),
    )
    add(
        "d017_descriptor_source",
        lambda identity: identity["consumer_bindings"]["projections"]["S2_on"]["work_key_fields"][0].__setitem__("source", "raw.cell_id"),
    )
    add(
        "d017_descriptor_atom",
        lambda identity: identity["consumer_bindings"]["projections"]["S3"]["consumer_pk_fields"][1].__setitem__("atom_type", "str"),
    )
    add(
        "d017_descriptor_order",
        lambda identity: identity["consumer_bindings"]["projections"]["BPS"]["work_key_fields"].reverse(),
    )
    add(
        "d017_method_map",
        lambda identity: identity["consumer_bindings"]["projections"]["S2_on"]["operation_rule"]["values"].__setitem__("OFC17_16QAM_EXTFRAME_V1", "B1_DECODE"),
    )
    add(
        "d017_split_map",
        lambda identity: identity["consumer_bindings"]["projections"]["S3"]["phase_rule"]["values"].__setitem__("S3_CANDIDATE_TEST", "S3_DEV"),
    )
    add(
        "d017_b2_same_type_swap",
        lambda identity: identity["consumer_bindings"]["projections"]["B2_controlled"]["work_key_fields"].__setitem__(0, identity["consumer_bindings"]["projections"]["B2_controlled"]["work_key_fields"][3]),
    )
    add(
        "d017_s4_check",
        lambda identity: identity["consumer_bindings"]["projections"]["S4"]["exact_check_ids"].pop(),
    )
    add(
        "d017_hmm_reference_kind",
        lambda identity: identity["consumer_bindings"]["projections"]["HMM_chunk"]["reference"].__setitem__("kind", "LOGICAL_COMPUTATION_ID"),
    )
    add(
        "d017_hmm_reference_rule",
        lambda identity: identity["consumer_bindings"]["projections"]["HMM_chunk"]["reference"].__setitem__("rule", "other"),
    )
    add(
        "d020_hard_version",
        lambda identity: identity["payload_schemas"]["decoder_hard_output"].__setitem__(
            "version", "coded_decoder_feedback.d0.decoder_hard_output.v2"
        ),
    )
    add(
        "d020_hard_field_order",
        lambda identity: identity["payload_schemas"]["decoder_hard_output"][
            "exact_object_field_order"
        ].reverse(),
    )
    add(
        "d020_hard_base64_length",
        lambda identity: identity["payload_schemas"]["decoder_hard_output"]["base64"].__setitem__(
            "encoded_length", 2731
        ),
    )
    add(
        "d020_provenance_entry_order",
        lambda identity: identity["payload_schemas"]["ordinary_consumer_provenance"][
            "entry_exact_object_field_order"
        ].reverse(),
    )
    add(
        "d020_provenance_source_direction",
        lambda identity: identity["runtime_content"]["ordinary_consumer_provenance"][
            "source_gate"
        ].__setitem__("direction", "REVERSED"),
    )
    add(
        "d020_static_count",
        lambda identity: identity["runtime_content"]["ordinary_static_counts"].__setitem__(
            "entries", 42966
        ),
    )
    add(
        "d020_hard_sidecar_filename",
        lambda identity: identity["runtime_content"]["ordinary_decoder_hard_output"].__setitem__(
            "filename", "other.jsonl"
        ),
    )
    add(
        "d020_provenance_sidecar_filename",
        lambda identity: identity["runtime_content"]["ordinary_consumer_provenance"].__setitem__(
            "filename", "other.jsonl"
        ),
    )
    add(
        "d020_write_order",
        lambda identity: identity["runtime_content"]["ordinary_write_anchor"][
            "exact_order"
        ].reverse(),
    )
    add(
        "d020_hard_golden_input",
        lambda identity: identity["golden_vectors"]["ordinary_hard_output_zero"][
            "inputs"
        ].__setitem__("canonical_payload_json", "{}"),
    )
    add(
        "d020_provenance_golden_root",
        lambda identity: identity["golden_vectors"]["ordinary_BPS_M3_cache"].__setitem__(
            "ordinary_consumer_provenance_manifest_sha256", "0" * 64
        ),
    )
    add(
        "d020_required_obligation",
        lambda identity: identity["validator_obligations"]["required"].remove(
            "hard_output_bits_base64_roundtrip_exact"
        ),
    )
    add(
        "d020_reject_obligation",
        lambda identity: identity["validator_obligations"]["reject_mutations"].remove(
            "hard_output_bit_or_base64_mutation"
        ),
    )
    add(
        "d020_controlled_entry_order",
        lambda identity: identity["runtime_content"]["ordinary_consumer_provenance"][
            "groups"
        ]["B2_controlled"]["entry_order"].reverse(),
    )

    duplicate = tmp_path / "duplicate.yaml"
    duplicate.write_bytes(
        OWNER.read_bytes()
        + b"\nidentity_binding_contract:\n  schema_version: duplicate\n"
    )
    mutations.append(("duplicate_key", duplicate))

    assert len(mutations) == 42
    for name, path in mutations:
        with pytest.raises(ContractError, match="owner|identity|duplicate|mapping"):
            contract_module.load_owner_identity_authority(path)


def test_owner_identity_loader_preserves_existing_contract_runtime():
    before = load_contract(OWNER)
    actions = contract_module.authorized_action_classes(before)
    authority = contract_module.load_owner_identity_authority(OWNER)

    assert authority.contract == before
    assert authority.contract is not before
    assert contract_module.authorized_action_classes(authority.contract) == actions
    assert actions == frozenset(
        {
            "D0_TESTBED_IMPLEMENTATION",
            "D0_UNIT_TEST",
            "ENGINEERING_THROUGHPUT_BENCHMARK",
            "SOURCE_AUDIT",
            "CONTRACT_STATIC_CHECK",
        }
    )
    contract_module.assert_frozen_d0_identity(authority.contract)
    contract_module.assert_frozen_owner_identity_authority(authority)


def test_owner_ordinary_domain_authority_exact_frozen_view():
    authority = contract_module.load_owner_identity_authority(OWNER)
    domain = authority.ordinary_domain
    assert tuple(field.name for field in fields(domain)) == (
        "controlled_cell_aliases", "polarizations", "fixtures", "candidates",
        "s2_methods", "s4_checks", "tuple_ids", "b_values", "nw_values",
        "s2_record_types", "s3_record_types", "s4_record_types",
        "bps_record_types", "b2_clean_record_types", "b2_controlled_record_types",
    )
    assert domain.controlled_cell_aliases == ("hard", "mid", "clean")
    assert domain.polarizations == ("X", "Y")
    assert domain.fixtures == (
        "B04_K1", "B04_K2", "B04_K3", "B08_K1", "B08_K2", "B08_K3",
        "B12_K1", "B12_K2", "B12_K3",
    )
    assert domain.candidates == ("NOOP",) + domain.fixtures
    assert domain.s2_methods == (
        "GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
        "OFC17_16QAM_EXTFRAME_V1",
        "TRUTH_BOUNDARY_ROTATION_CORRECTION",
    )
    assert domain.s4_checks == schemas_expected_s4_checks()
    assert domain.tuple_ids == ("M2_N100", "M3_N10", "M3_N20", "M3_N100", "M3_N200")
    assert domain.b_values == (32, 64)
    assert domain.nw_values == (31, 61, 127)
    assert domain.s2_record_types == ("S2_METHOD",)
    assert domain.s3_record_types == ("S3_CANDIDATE_DEV", "S3_CANDIDATE_TEST")
    assert domain.s4_record_types == ("S4_CHECK",)
    assert domain.bps_record_types == ("BPS_DEV_SCORE",)
    assert domain.b2_clean_record_types == ("B2_TUPLE_CLEAN_DEV",)
    assert domain.b2_controlled_record_types == ("B2_TUPLE_CONTROLLED_DEV",)
    projection = {
        "schema": "coded_decoder_feedback.d0.ordinary_domain_authority.v1",
        "controlled_cell_aliases": list(domain.controlled_cell_aliases),
        "polarizations": list(domain.polarizations),
        "fixtures": list(domain.fixtures),
        "candidates": list(domain.candidates),
        "s2_methods": list(domain.s2_methods),
        "s4_checks": list(domain.s4_checks),
        "tuple_ids": list(domain.tuple_ids),
        "b_values": list(domain.b_values),
        "nw_values": list(domain.nw_values),
        "record_type_domains": {
            "s2_method": list(domain.s2_record_types),
            "s3_candidate": list(domain.s3_record_types),
            "s4_check": list(domain.s4_record_types),
            "bps_dev_score": list(domain.bps_record_types),
            "b2_tuple_clean_dev": list(domain.b2_clean_record_types),
            "b2_tuple_controlled_dev": list(domain.b2_controlled_record_types),
        },
    }
    assert authority.ordinary_domain_sha256 == _canonical_sha256(projection)
    assert authority.ordinary_domain_sha256 == "15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69"
    with pytest.raises((AttributeError, TypeError)):
        domain.candidates += ("FORGED",)


def schemas_expected_s4_checks():
    return (
        "no_slip_noiseless_B0_B1_O1_identity",
        "all_rotation_boundary_noiseless_O1_zero_error",
        "mapping_rotation_truth_metamorphic_pass",
        "candidate_isolation_and_empty_decoder_state_pass",
        "all_scores_finite_and_deterministic",
        "no_truth_field_reaches_receiver_view",
        "diagnostic_cost_ledger_complete",
    )


def test_contract_control_is_cp012_implementation_only(d0_contract, tmp_path):
    assert d0_contract.schema_version == "coded_decoder_feedback.d0.v3"
    assert d0_contract.control.epoch == 12
    assert d0_contract.control.checkpoint == "CP012"
    assert d0_contract.control.decision == "D011"
    assert d0_contract.control.verification == "V005"
    assert d0_contract.control.implementation_authorized is True
    assert d0_contract.control.unit_test_authorized is True
    assert d0_contract.control.engineering_benchmark_authorized is True
    assert d0_contract.control.execution_authorized is False
    assert d0_contract.control.scientific_experiment_authorized is False

    for action in {
        "D0_TESTBED_IMPLEMENTATION",
        "D0_UNIT_TEST",
        "ENGINEERING_THROUGHPUT_BENCHMARK",
        "SOURCE_AUDIT",
        "CONTRACT_STATIC_CHECK",
    }:
        assert_action_authorized(action, d0_contract)

    for action in {"DEFECT_SMOKE", "S1_NATURAL_OCCURRENCE", "C1_EXTENSION"}:
        with pytest.raises(PermissionError, match="not authorized under CP012"):
            assert_action_authorized(action, d0_contract)

    duplicate_owner = tmp_path / "duplicate-owner.yaml"
    duplicate_owner.write_text(
        "schema_version: coded_decoder_feedback.d0.v3\n"
        "schema_version: duplicate\n",
        encoding="utf-8",
    )
    with pytest.raises(ContractError, match="duplicate YAML key: schema_version"):
        load_contract(duplicate_owner)


def test_population_manifest_has_exact_twelve_cells(d0_contract):
    population = d0_contract.population
    code = population.code
    assert population.modulation == "gray_square_16qam"
    assert population.symbol_rate_baud == 2.5e9
    assert population.snr_db == (10, 14, 18, 22)
    assert population.linewidth_hz == (10000, 20000, 80000)
    assert code.information_bits_per_cw == 1024
    assert code.transmitted_bits_per_cw == 1536
    assert code.codewords_per_polarization == 16
    assert code.data_symbols_per_cw == 384
    assert code.data_symbols_per_polarization == 6144
    assert code.decoder_iterations == 20

    cells = d0_contract.population_manifest
    expected_pairs = {
        (snr_db, linewidth_hz)
        for snr_db in (10, 14, 18, 22)
        for linewidth_hz in (10000, 20000, 80000)
    }
    assert len(cells) == 12
    assert len({cell.cell_id for cell in cells}) == 12
    assert {(cell.snr_db, cell.linewidth_hz) for cell in cells} == expected_pairs


def test_seed_registry_exact_and_pairwise_disjoint(d0_contract):
    registry = d0_contract.seed_registry
    expected = {
        "common_cpr_and_b2_dev": (8000, 8009),
        "observability_fusion_dev": (8050, 8059),
        "natural_occurrence": (8100, 8149),
        "controlled_damage_recovery": (8150, 8159),
        "controlled_observability": (8160, 8169),
        "clean_diagnostic": (8170, 8179),
        "post_d0_c1_dev": (8200, 8219),
        "post_d0_fresh_heldout": (8300, 8349),
    }
    assert registry.labels == tuple(expected)

    materialized = {}
    for label, (first, last) in expected.items():
        seed_range = registry.range_for(label)
        assert (seed_range.first, seed_range.last) == (first, last)
        assert seed_range.values == tuple(range(first, last + 1))
        materialized[label] = set(seed_range.values)
        assert registry.label_for(first) == label
        assert registry.label_for(last) == label
        registry.assert_member(label, first)
        registry.assert_member(label, last)

    assert registry.first_stage_natural.values == tuple(range(8100, 8120))
    assert set(registry.first_stage_natural.values) < materialized["natural_occurrence"]
    for left, right in combinations(expected, 2):
        assert materialized[left].isdisjoint(materialized[right])

    with pytest.raises(ValueError, match="does not belong"):
        registry.assert_member("controlled_damage_recovery", 8100)
    with pytest.raises(ValueError, match="outside every registered seed range"):
        registry.label_for(7999)
    with pytest.raises(KeyError, match="unknown seed label"):
        registry.range_for("unknown")


def _minimal_receiver(module, code_layout, *, b2_parameters=None, receipts=None):
    total = 6240
    return module.ReceiverView(
        received_samples=np.ones((2, total), dtype=np.complex128),
        equalized_samples=np.ones((2, total), dtype=np.complex128),
        common_cpr_phase_trace=np.zeros((2, total), dtype=np.float64),
        known_prefix=np.ones((2, 32), dtype=np.complex128),
        periodic_pilots=np.ones((2, 64), dtype=np.complex128),
        code_layout=code_layout,
        waveform_layout=module.WaveformLayout(
            prefix_symbols=32,
            pilot_period_symbols=100,
            data_symbols_per_polarization=6144,
            total_symbols_per_polarization=total,
        ),
        b2_parameters=b2_parameters or {"p_s": [0.01, 0.02]},
        receipts=receipts or {"source_sha256": "a" * 64},
    )


def test_receiver_truth_frozen_disjoint(d0_contract):
    required = (
        "ReceiverView",
        "TruthView",
        "PayloadTruth",
        "WaveformLayout",
        "CostLedger",
        "ResolvedDevFreeze",
    )
    assert all(hasattr(contract_module, name) for name in required), (
        "immutable receiver/truth value types are not implemented"
    )

    source_rx = np.ones((2, 6240), dtype=np.complex128)
    source_b2 = {"grid": [{"p_s": [0.01, 0.02]}]}
    source_receipts = {
        "source_sha256": "a" * 64,
        "code_sha256": "b" * 64,
        "content_sha256": "c" * 64,
        "notes": ["receiver-only"],
    }
    receiver = contract_module.ReceiverView(
        received_samples=source_rx,
        equalized_samples=np.ones((2, 6240), dtype=np.complex128),
        common_cpr_phase_trace=np.zeros((2, 6240), dtype=np.float64),
        known_prefix=np.ones((2, 32), dtype=np.complex128),
        periodic_pilots=np.ones((2, 64), dtype=np.complex128),
        code_layout=d0_contract.population.code,
        waveform_layout=contract_module.WaveformLayout(32, 100, 6144, 6240),
        b2_parameters=source_b2,
        receipts=source_receipts,
    )
    truth_bits = np.zeros((2, 16, 1024), dtype=np.uint8)
    truth = contract_module.TruthView(
        information_bits=truth_bits,
        coded_bits=np.zeros((2, 16, 1536), dtype=np.uint8),
        transmitted_symbols=np.ones((2, 6240), dtype=np.complex128),
        true_phase=np.zeros((2, 6240), dtype=np.float64),
        channel_h=np.ones((2, 6240), dtype=np.complex128),
        physical_snr_db=14.0,
        fade=np.ones((2, 6240), dtype=np.float64),
        noise_receipt={"samples": np.zeros((2, 6240), dtype=np.complex128)},
        event_label="clean",
    )
    ledger_source = {"work_ids": ["decoder-0"]}
    ledger = contract_module.CostLedger(1, 16, 320, ledger_source)
    freeze_source = {"candidates": [{"B": 32, "Nw": [31, 61]}]}
    freeze = contract_module.ResolvedDevFreeze(
        "freeze-001", freeze_source, {"artifact_sha256": "d" * 64}
    )

    for value_type in (
        contract_module.ReceiverView,
        contract_module.TruthView,
        contract_module.PayloadTruth,
        contract_module.CodeLayout,
        contract_module.WaveformLayout,
        contract_module.CostLedger,
        contract_module.ResolvedDevFreeze,
    ):
        assert value_type.__dataclass_params__.frozen is True
        assert "__slots__" in value_type.__dict__

    receiver_fields = {field.name for field in fields(contract_module.ReceiverView)}
    truth_fields = {field.name for field in fields(contract_module.TruthView)}
    assert receiver_fields.isdisjoint(truth_fields)
    assert receiver_fields == {
        "received_samples",
        "equalized_samples",
        "common_cpr_phase_trace",
        "known_prefix",
        "periodic_pilots",
        "receiver_noise_estimate",
        "code_layout",
        "waveform_layout",
        "b2_parameters",
        "receipts",
    }

    stored_rx_bytes = receiver.received_samples.tobytes()
    source_rx[0] = 99 + 99j
    source_b2["grid"][0]["p_s"].append(0.99)
    source_receipts["notes"].append("mutated")
    truth_bits[0, 0, 0] = 1
    ledger_source["work_ids"].append("mutated")
    freeze_source["candidates"][0]["Nw"].append(127)
    assert receiver.received_samples.tobytes() == stored_rx_bytes
    assert receiver.received_samples.flags.writeable is False
    assert truth.information_bits.flags.writeable is False
    assert tuple(receiver.b2_parameters["grid"][0]["p_s"]) == (0.01, 0.02)
    assert receiver.receipts["notes"] == ("receiver-only",)
    assert ledger.receipts["work_ids"] == ("decoder-0",)
    assert freeze.parameters["candidates"][0]["Nw"] == (31, 61)
    assert not hasattr(receiver.b2_parameters, "__setitem__")
    with pytest.raises(ValueError):
        receiver.received_samples[0] = 0
    with pytest.raises(TypeError):
        receiver.receipts["new"] = "forbidden"


@dataclass(frozen=True)
class _NestedTruthLeak:
    event_label: str


def test_receiver_rejects_truth_and_extra_fields(d0_contract):
    assert hasattr(contract_module, "ReceiverView"), (
        "ReceiverView truth guard is not implemented"
    )
    aliases = (
        "truth",
        "tx_payload",
        "information_bits",
        "coded_bits",
        "transmitted_symbols",
        "true_phase",
        "h",
        "snr",
        "fade",
        "slip",
        "event_label",
        "correctness",
    )
    for alias in aliases:
        with pytest.raises(ContractError, match="truth alias"):
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                b2_parameters={"safe": {alias: 1}},
            )

    repair_failures = []
    equivalent_aliases = (
        "payload",
        "payload_bits",
        "tx_information_bits",
        "snr_db",
        "channel_gain",
        "phase_truth",
        "cfo",
        "slip_rotation",
        "final_cw_correctness",
    )
    for alias in equivalent_aliases:
        try:
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                b2_parameters={"outer": [{"inner": {alias: 1}}]},
            )
        except ContractError:
            pass
        else:
            repair_failures.append(f"equivalent_alias:{alias}=accepted")

    step114_categories = (
        "info_bits",
        "data_symbols",
        "true_channel",
        "physical_channel_receipt",
        "channel_realization",
        "injected_label",
        "natural_label",
        "final_cw_errors",
    )
    taxonomy_variants = tuple(
        variant
        for category in step114_categories
        for variant in (
            category,
            category.upper(),
            category.replace("_", "-"),
        )
    )
    unseen_taxonomy_combinations = (
        "info_bit_vector",
        "coded_bit_vector",
        "data_symbol_vector",
        "actual_channel",
        "oracle_channel_gain",
        "injection_fixture",
        "natural_event_fixture",
        "codeword_final_status",
    )
    for alias in taxonomy_variants + unseen_taxonomy_combinations:
        try:
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                b2_parameters={
                    "level_1": [{"level_2": {"level_3": {alias: 1}}}]
                },
            )
        except ContractError:
            pass
        else:
            repair_failures.append(f"owner_taxonomy:{alias}=accepted")

    object_truth = np.empty(1, dtype=object)
    object_truth[0] = {"true_phase": 0.25}
    structured_truth = np.empty(1, dtype=[("metadata", object)])
    structured_truth["metadata"][0] = {"true_phase": 0.25}
    object_mutable = np.empty(1, dtype=object)
    object_mutable[0] = [1, 2, 3]
    structured_mutable = np.empty(1, dtype=[("metadata", object)])
    structured_mutable["metadata"][0] = [1, 2, 3]
    for label, unsafe_array in (
        ("object_array_truth_dict", object_truth),
        ("structured_array_truth_dict", structured_truth),
        ("object_array_mutable_list", object_mutable),
        ("structured_array_mutable_list", structured_mutable),
    ):
        try:
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                b2_parameters={"safe": unsafe_array},
            )
        except ContractError:
            pass
        else:
            repair_failures.append(f"{label}=accepted")
    assert repair_failures == [], f"truth-container repair missing: {repair_failures}"

    safe_control_names = (
        "received_samples",
        "equalized_samples",
        "known_prefix",
        "periodic_pilots",
        "receiver_noise_estimate",
        "common_cpr_phase_trace",
        "global_rotation_state",
        "bps_state",
        "source_sha256",
        "code_sha256",
        "content_sha256",
        "channel_source_sha256",
    )
    safe_controls = {
        name: ("a" * 64 if name.endswith("sha256") else [0.0, 0.25])
        for name in safe_control_names
    }
    safe_receiver = _minimal_receiver(
        contract_module,
        d0_contract.population.code,
        b2_parameters={"level_1": [{"level_2": {"level_3": safe_controls}}]},
    )
    stored_safe = safe_receiver.b2_parameters["level_1"][0]["level_2"][
        "level_3"
    ]
    assert set(stored_safe) == set(safe_control_names)

    numeric_source = np.array([1.0, 2.0], dtype=np.float64)
    bool_source = np.array([True, False], dtype=np.bool_)
    safe_receiver = _minimal_receiver(
        contract_module,
        d0_contract.population.code,
        b2_parameters={
            "numeric": numeric_source,
            "boolean": bool_source,
            "common_cpr_phase_trace": [0.0, 0.25],
            "source_sha256": "a" * 64,
            "code_sha256": "b" * 64,
            "content_sha256": "c" * 64,
        },
    )
    numeric_source[0] = 99.0
    bool_source[0] = False
    assert safe_receiver.b2_parameters["numeric"].tolist() == [1.0, 2.0]
    assert safe_receiver.b2_parameters["boolean"].tolist() == [True, False]
    assert safe_receiver.b2_parameters["numeric"].flags.writeable is False
    assert safe_receiver.b2_parameters["boolean"].flags.writeable is False
    with pytest.raises(ContractError, match="truth alias"):
        _minimal_receiver(
            contract_module,
            d0_contract.population.code,
            receipts={"nested": _NestedTruthLeak("controlled")},
        )

    kwargs = dict(
        received_samples=np.ones((2, 6240), dtype=np.complex128),
        equalized_samples=np.ones((2, 6240), dtype=np.complex128),
        common_cpr_phase_trace=np.zeros((2, 6240), dtype=np.float64),
        known_prefix=np.ones((2, 32), dtype=np.complex128),
        periodic_pilots=np.ones((2, 64), dtype=np.complex128),
        code_layout=d0_contract.population.code,
        waveform_layout=contract_module.WaveformLayout(32, 100, 6144, 6240),
        b2_parameters={"safe": True},
        receipts={"source_sha256": "a", "code_sha256": "b", "content_sha256": "c"},
    )
    contract_module.ReceiverView(**kwargs)
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        contract_module.ReceiverView(**kwargs, extra_field="forbidden")


class _SlotLeakBase:
    __slots__ = "event_label"

    def __init__(self):
        self.event_label = "controlled"


class _SlotLeak(_SlotLeakBase):
    __slots__ = ("safe",)

    def __init__(self):
        super().__init__()
        self.safe = self


class _SafeSingleSlot:
    __slots__ = "contents"

    def __init__(self, contents):
        self.contents = contents


class _SafeInheritedSlotBase:
    __slots__ = ("base_contents",)

    def __init__(self, contents):
        self.base_contents = contents


class _SafeInheritedSlot(_SafeInheritedSlotBase):
    __slots__ = ("child_contents",)

    def __init__(self, contents):
        super().__init__(contents)
        self.child_contents = {"safe": contents}


class _SafeDictObject:
    def __init__(self, contents):
        self.contents = contents


def test_i06_generic_receipt_objects_fail_closed(d0_contract):
    generic_sources = (
        _SafeSingleSlot({"safe": [1, 2]}),
        _SafeInheritedSlot({"safe": [3, 4]}),
        _SafeDictObject({"safe": [5, 6]}),
        _SafeSingleSlot(_SafeDictObject({"nested": [7, 8]})),
    )
    for source in generic_sources:
        with pytest.raises(ContractError, match="generic|plain|allow|closed"):
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                receipts={"safe_object": source},
            )
        if hasattr(source, "contents"):
            source.contents = {"true_phase": np.ones(2)}
        with pytest.raises(ContractError):
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                receipts={"safe_object": source},
            )

    with pytest.raises(ContractError):
        _minimal_receiver(
            contract_module,
            d0_contract.population.code,
            receipts={"nested": [_SafeDictObject({"event_label": "leak"})]},
        )

    plain_source = {
        "safe": [{"value": np.array([1.0, 2.0])}],
        "labels": {"alpha", "beta"},
    }
    receiver = _minimal_receiver(
        contract_module,
        d0_contract.population.code,
        receipts=plain_source,
    )
    plain_source["safe"][0]["value"][0] = 99.0
    plain_source["labels"].add("gamma")
    assert receiver.receipts["safe"][0]["value"].tolist() == [1.0, 2.0]
    assert receiver.receipts["labels"] == frozenset({"alpha", "beta"})

    cyclic = {}
    cyclic["self"] = cyclic
    with pytest.raises(ContractError, match="cyclic|cycle"):
        _minimal_receiver(
            contract_module,
            d0_contract.population.code,
            receipts=cyclic,
        )


def test_i06_receipt_closed_world_rejects_opaque_builtins(d0_contract):
    backing = bytearray(b"mutable")
    opaque_values = (
        backing,
        memoryview(backing),
        range(3),
        object(),
        MappingProxyType({"safe": 1}),
        (item for item in (1, 2)),
        iter([1, 2]),
    )
    for value in opaque_values:
        with pytest.raises(ContractError, match="closed|plain|exact|allowed"):
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                receipts={"opaque": value},
            )
    backing[0] = ord("M")

    class DictSubclass(dict):
        pass

    class ListSubclass(list):
        pass

    class SetSubclass(set):
        pass

    for value in (DictSubclass(safe=1), ListSubclass([1]), SetSubclass({1})):
        with pytest.raises(ContractError, match="closed|exact|allowed"):
            _minimal_receiver(
                contract_module,
                d0_contract.population.code,
                b2_parameters={"opaque": value},
            )

    with pytest.raises(ContractError, match="key"):
        _minimal_receiver(
            contract_module,
            d0_contract.population.code,
            receipts={1: "non-string-key"},
        )

    source = {
        "metadata": [None, True, 3, 2.5, 1 + 2j, "text", b"bytes"],
        "set_values": {1, 2},
        "array": np.array([1.0, 2.0]),
        "scalar": np.float64(3.5),
    }
    receiver = _minimal_receiver(
        contract_module,
        d0_contract.population.code,
        receipts=source,
    )
    source["metadata"].append("mutated")
    source["array"][0] = 99.0
    assert receiver.receipts["metadata"][-1] == b"bytes"
    assert receiver.receipts["array"].tolist() == [1.0, 2.0]
    assert type(receiver.receipts["scalar"]) is float


def test_i06_view_contract_mutations_fail_closed(d0_contract):
    receiver = _minimal_receiver(contract_module, d0_contract.population.code)
    info = np.zeros((2, 16, 1024), dtype=np.uint8)
    coded = np.zeros((2, 16, 1536), dtype=np.uint8)
    truth = contract_module.TruthView(
        information_bits=info,
        coded_bits=coded,
        transmitted_symbols=np.ones((2, 6240), dtype=np.complex128),
        true_phase=np.zeros((2, 6240), dtype=np.float64),
        channel_h=np.ones((2, 6240), dtype=np.complex128),
        physical_snr_db=14.0,
        fade=np.ones((2, 6240), dtype=np.float64),
        noise_receipt={"samples": np.zeros((2, 6240), dtype=np.complex128)},
        event_label="none",
    )
    receiver_mutations = (
        {"received_samples": np.ones((1, 6240), dtype=np.complex128)},
        {"equalized_samples": np.ones((2, 6239), dtype=np.complex128)},
        {"common_cpr_phase_trace": np.full((2, 6240), np.nan)},
        {"known_prefix": np.ones((2, 31), dtype=np.complex128)},
        {"periodic_pilots": np.ones((2, 63), dtype=np.complex128)},
        {"receiver_noise_estimate": np.array([0.1, np.nan])},
        {"waveform_layout": contract_module.WaveformLayout(31, 100, 6144, 6240)},
        {"code_layout": replace(d0_contract.population.code, information_bits_per_cw=2048)},
        {"receipts": {"safe": _SlotLeak()}},
    )
    for changes in receiver_mutations:
        with pytest.raises((TypeError, ValueError)):
            replace(receiver, **changes)

    truth_mutations = (
        {"information_bits": np.zeros((2, 16, 1023), np.uint8)},
        {"coded_bits": np.zeros((2, 16, 1535), np.uint8)},
        {"true_phase": np.zeros((1, 6240), np.float64)},
        {"channel_h": np.full((2, 6240), np.nan + 0j)},
        {"fade": np.full((2, 6240), np.inf)},
        {"noise_receipt": {"samples": np.zeros((1, 6240), np.complex128)}},
        {"final_codeword_correctness": np.empty((2, 0), np.bool_)},
    )
    for changes in truth_mutations:
        with pytest.raises((TypeError, ValueError)):
            replace(truth, **changes)


def _i17a_truth(*, bit, event_label):
    return contract_module.TruthView(
        information_bits=np.full((2, 16, 1024), bit, dtype=np.uint8),
        coded_bits=np.full((2, 16, 1536), bit, dtype=np.uint8),
        transmitted_symbols=np.full((2, 6240), 1 + bit * 1j, dtype=np.complex128),
        true_phase=np.full((2, 6240), float(bit), dtype=np.float64),
        channel_h=np.full((2, 6240), 1 + bit * 0.25j, dtype=np.complex128),
        physical_snr_db=14.0 + bit,
        fade=np.full((2, 6240), 1.0 + bit, dtype=np.float64),
        noise_receipt={
            "samples": np.full((2, 6240), bit * 0.01j, dtype=np.complex128)
        },
        event_label=event_label,
    )


def _i17a_resolved_freeze():
    return contract_module.ResolvedDevFreeze(
        "5" * 64,
        {
            "common_bps": (
                {"tuple_id": "M2_N100", "winner": {"B": 32, "Nw": 31}},
            ),
            "final_b2_tuple": {"tuple_id": "M2_N100"},
        },
        {"dev_freeze_sha256": "5" * 64},
    )


def _i17a_phase_receipts(freeze_id="5" * 64):
    return tuple(
        {"phase": phase, "dev_freeze_sha256": freeze_id}
        for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4")
    )


def test_cv06_real_deployable_seal_is_truth_invariant(d0_contract):
    verify = importlib.import_module("verify")
    artifacts = importlib.import_module("artifacts")
    receiver = _minimal_receiver(contract_module, d0_contract.population.code)
    resolved = _i17a_resolved_freeze()
    boundary = verify.DeploymentBoundary(verify.deployment_callable_registry())

    truth_zero = _i17a_truth(bit=0, event_label="clean")
    truth_one = _i17a_truth(bit=1, event_label="controlled")
    decoded = np.zeros((2, 16, 1024), dtype=np.uint8)
    seal_zero = boundary.seal(
        d0_contract,
        receiver,
        resolved,
        phase="D0_UNIT_TEST",
        phase_receipts=_i17a_phase_receipts(),
    )
    evaluated_zero = boundary.evaluate_after_seal(
        seal_zero, truth_zero, decoded_information_bits=decoded
    )
    seal_one = boundary.seal(
        d0_contract,
        receiver,
        resolved,
        phase="D0_UNIT_TEST",
        phase_receipts=tuple(reversed(_i17a_phase_receipts())),
    )
    evaluated_one = boundary.evaluate_after_seal(
        seal_one, truth_one, decoded_information_bits=decoded
    )

    assert seal_zero.output_sha256 == seal_one.output_sha256
    assert seal_zero.bps_choice == seal_one.bps_choice == (32, 31)
    assert seal_zero.score == seal_one.score
    assert seal_zero.receipt_bytes == seal_one.receipt_bytes
    assert seal_zero.receipt_sha256 == seal_one.receipt_sha256
    assert hashlib.sha256(seal_zero.receipt_bytes).hexdigest() == seal_zero.receipt_sha256
    assert artifacts.canonical_json_bytes(seal_zero.receipt_document) == seal_zero.receipt_bytes
    assert evaluated_zero.final_codeword_correctness.all()
    assert not evaluated_one.final_codeword_correctness.any()


def test_cv06_registry_evaluator_rejects_truth_before_authenticated_seal():
    verify = importlib.import_module("verify")
    truth = _i17a_truth(bit=0, event_label="preseal-denied")
    decoded = np.zeros((2, 16, 1024), dtype=np.uint8)
    evaluator = verify.deployment_callable_registry()["evaluator"]
    with pytest.raises(PermissionError, match="authenticated DeploymentSeal"):
        evaluator(truth, decoded_information_bits=decoded)


def test_cv07_recursive_callable_truth_scan_covers_real_signatures_annotations_and_closures():
    verify = importlib.import_module("verify")
    registry = verify.deployment_callable_registry()
    boundary = verify.DeploymentBoundary(registry)
    for name, callable_value in registry.items():
        if name != "evaluator":
            boundary.assert_truth_free_callable(callable_value)

    def nested_annotation(value: tuple[list[dict[str, contract_module.TruthView]], ...]):
        return value

    hidden = {"nested": ({"payload": contract_module.TruthView},)}

    def closure_leak():
        return hidden

    with pytest.raises(ValueError, match="truth"):
        boundary.assert_truth_free_callable(nested_annotation)
    with pytest.raises(ValueError, match="truth"):
        boundary.assert_truth_free_callable(closure_leak)


def test_cv08_phase_freeze_and_registry_binding_fail_closed(d0_contract, monkeypatch):
    verify = importlib.import_module("verify")
    benchmark = importlib.import_module("benchmark")
    receiver_module = importlib.import_module("receiver")
    resolved = _i17a_resolved_freeze()
    receipts = _i17a_phase_receipts()
    binding = benchmark.bind_resolved_freeze(
        resolved, receipts, benchmark_freeze_sha256=resolved.freeze_id
    )
    reordered = benchmark.bind_resolved_freeze(
        resolved, tuple(reversed(receipts)), benchmark_freeze_sha256=resolved.freeze_id
    )
    assert binding.receipt_bytes == reordered.receipt_bytes
    assert binding.receipt_sha256 == reordered.receipt_sha256

    for invalid in (
        receipts[:-1],
        (*receipts[:-1], {"phase": "S3test", "dev_freeze_sha256": resolved.freeze_id}),
        (*receipts[:-1], {"phase": "S4", "dev_freeze_sha256": "6" * 64}),
    ):
        with pytest.raises(ValueError):
            benchmark.bind_resolved_freeze(
                resolved, invalid, benchmark_freeze_sha256=resolved.freeze_id
            )
    wrong = contract_module.ResolvedDevFreeze(
        "6" * 64, resolved.parameters, resolved.receipts
    )
    with pytest.raises(ValueError):
        benchmark.bind_resolved_freeze(
            wrong, receipts, benchmark_freeze_sha256=resolved.freeze_id
        )

    receiver = _minimal_receiver(contract_module, d0_contract.population.code)
    with pytest.raises(ValueError, match="phase"):
        verify.DeploymentBoundary(verify.deployment_callable_registry()).seal(
            d0_contract, receiver, resolved, phase="", phase_receipts=receipts
        )
    with pytest.raises(ValueError, match="registry"):
        verify.DeploymentBoundary({}).seal(
            d0_contract, receiver, resolved,
            phase="D0_UNIT_TEST", phase_receipts=receipts,
        )
    missing = dict(verify.deployment_callable_registry())
    missing.pop("B2")
    with pytest.raises(ValueError, match="registry"):
        verify.DeploymentBoundary(missing).seal(
            d0_contract, receiver, resolved,
            phase="D0_UNIT_TEST", phase_receipts=receipts,
        )
    noncallable = dict(verify.deployment_callable_registry())
    noncallable["B2"] = None
    with pytest.raises(ValueError, match="callable"):
        verify.DeploymentBoundary(noncallable).seal(
            d0_contract, receiver, resolved,
            phase="D0_UNIT_TEST", phase_receipts=receipts,
        )
    monkeypatch.delitem(sys.modules, "receiver")
    with pytest.raises(ValueError, match="module"):
        verify.DeploymentBoundary(verify.deployment_callable_registry()).seal(
            d0_contract, receiver, resolved,
            phase="D0_UNIT_TEST", phase_receipts=receipts,
        )
    assert receiver_module.__name__ == "receiver"


def test_cv08_forged_object_new_and_tampered_seals_are_rejected(d0_contract):
    verify = importlib.import_module("verify")
    receiver = _minimal_receiver(contract_module, d0_contract.population.code)
    resolved = _i17a_resolved_freeze()
    receipts = _i17a_phase_receipts()
    boundary = verify.DeploymentBoundary(verify.deployment_callable_registry())
    truth = _i17a_truth(bit=0, event_label="authenticated-evaluator")
    decoded = np.zeros((2, 16, 1024), dtype=np.uint8)
    real = boundary.seal(
        d0_contract, receiver, resolved,
        phase="D0_UNIT_TEST", phase_receipts=receipts,
    )
    assert boundary.evaluate_after_seal(
        real, truth, decoded_information_bits=decoded
    ).final_codeword_correctness.all()

    with pytest.raises(PermissionError, match="controlled"):
        verify.DeploymentSeal(
            phase="D0_UNIT_TEST",
            dev_freeze_sha256="0" * 64,
            callable_ids=(),
            output_sha256="0" * 64,
            bps_choice=(32, 31),
            score=0.0,
            receipt_bytes=b"{}",
            receipt_sha256="0" * 64,
        )

    forged = object.__new__(verify.DeploymentSeal)
    for field in fields(verify.DeploymentSeal):
        object.__setattr__(forged, field.name, getattr(real, field.name))
    with pytest.raises(PermissionError, match="authenticated DeploymentSeal"):
        boundary.evaluate_after_seal(
            forged, truth, decoded_information_bits=decoded
        )

    object.__setattr__(real, "receipt_sha256", "0" * 64)
    with pytest.raises(PermissionError, match="tampered DeploymentSeal"):
        boundary.evaluate_after_seal(
            real, truth, decoded_information_bits=decoded
        )


def test_scientific_actions_disabled_cp012(d0_contract):
    assert hasattr(contract_module, "authorized_action_classes"), (
        "deterministic CP012 action-set API is not implemented"
    )
    expected = frozenset(
        {
            "D0_TESTBED_IMPLEMENTATION",
            "D0_UNIT_TEST",
            "ENGINEERING_THROUGHPUT_BENCHMARK",
            "SOURCE_AUDIT",
            "CONTRACT_STATIC_CHECK",
        }
    )
    assert contract_module.authorized_action_classes(d0_contract) == expected
    denied = {
        "DEFECT_SMOKE",
        "S1_NATURAL_OCCURRENCE",
        "S2_CONTROLLED_DAMAGE",
        "S3DEV_OBSERVABILITY",
        "S3TEST_OBSERVABILITY",
        "S4_ENGINEERING_GATE",
        "C1_EXTENSION",
        "MVE",
        "HELDOUT_FAIR_COMPARISON",
        "CONTRACT",
        "EXECUTE",
        "UNKNOWN",
    }
    for action in denied:
        with pytest.raises(PermissionError, match="not authorized under CP012"):
            assert_action_authorized(action, d0_contract)

    identity_mutations = {
        "schema_version": replace(d0_contract, schema_version="coded_decoder_feedback.d0.v4"),
        "epoch": replace(d0_contract, control=replace(d0_contract.control, epoch=13)),
        "checkpoint": replace(d0_contract, control=replace(d0_contract.control, checkpoint="CP013")),
        "decision": replace(d0_contract, control=replace(d0_contract.control, decision="D012")),
        "verification": replace(d0_contract, control=replace(d0_contract.control, verification="V006")),
    }
    for mutated in identity_mutations.values():
        assert contract_module.authorized_action_classes(mutated) == frozenset()
        with pytest.raises(PermissionError, match="not authorized under CP012"):
            assert_action_authorized("SOURCE_AUDIT", mutated)

    permission_cases = (
        ("implementation_authorized", "D0_TESTBED_IMPLEMENTATION"),
        ("unit_test_authorized", "D0_UNIT_TEST"),
        ("engineering_benchmark_authorized", "ENGINEERING_THROUGHPUT_BENCHMARK"),
    )
    for field_name, action in permission_cases:
        mutated = replace(
            d0_contract,
            control=replace(d0_contract.control, **{field_name: False}),
        )
        assert contract_module.authorized_action_classes(mutated) == expected - {
            action
        }
        with pytest.raises(PermissionError, match="not authorized under CP012"):
            assert_action_authorized(action, mutated)
    for field_name in ("execution_authorized", "scientific_experiment_authorized"):
        mutated = replace(
            d0_contract,
            control=replace(d0_contract.control, **{field_name: True}),
        )
        assert contract_module.authorized_action_classes(mutated) == frozenset()
