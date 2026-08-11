from __future__ import annotations

import ast
import dataclasses
import copy
import hashlib
import inspect
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest
import numpy as np


D0_ROOT = Path(__file__).resolve().parents[1] / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))
OWNER = (Path(__file__).resolve().parents[3] / "projects" / "thesis-fso"
         / "coded-decoder-feedback-groundwork" / "d0-defect-smoke-contract.yaml")
H = "a" * 64


def _api():
    import freeze
    return freeze


def _authority():
    import contract
    return contract.load_owner_identity_authority(OWNER)


def test_df01_manifest_binds_float_hex_grids_domains_and_membership():
    manifest = _api().build_dev_manifest(_authority())
    assert manifest["schema"] == "coded_decoder_feedback.d0.dev_manifest.v1"
    assert manifest["dev_seeds"] == list(range(8000, 8010))
    assert len(manifest["cells"]) == 12
    assert [item["tuple_id"] for item in manifest["tuples"]] == [
        "M2_N100", "M3_N10", "M3_N20", "M3_N100", "M3_N200"
    ]
    assert len(manifest["p_s_grid"]) == 122
    assert len(manifest["sigma_e2_grid"]) == 6
    for grid in (manifest["p_s_grid"], manifest["sigma_e2_grid"]):
        assert [item["index"] for item in grid] == list(range(len(grid)))
        assert all(float.fromhex(item["float64_hex"]).hex() == item["float64_hex"] for item in grid)
    assert manifest["membership_per_cell_pol"] == {
        "CLEAN_INCLUDED": 10,
        "CONTROLLED_TARGET_INCLUDED": 90,
        "CONTROLLED_SENTINEL_EXCLUDED": 90,
    }


def test_df02_manifest_has_7200_bps_keys_and_keeps_n100_logical_duplicates():
    api = _api()
    keys = api.expected_bps_primary_keys(api.build_dev_manifest(_authority()))
    assert len(keys) == len(set(keys)) == 7200
    n100 = [key for key in keys if key[1] in {"M2_N100", "M3_N100"}]
    assert len(n100) == 2880
    assert {(key[1], key[2], key[3]) for key in n100} == {
        (tuple_id, B, Nw)
        for tuple_id in ("M2_N100", "M3_N100")
        for B in (32, 64) for Nw in (31, 61, 127)
    }


def _bps_rows(manifest):
    rows = []
    for key in _api().expected_bps_primary_keys(manifest):
        _, tuple_id, B, Nw, seed, cell, pol = key
        winner = (B, Nw) == (32, 31)
        successful = 15 if winner else 14
        rows.append({
            "record_type": "BPS_DEV_SCORE", "tuple_id": tuple_id,
            "B": B, "Nw": Nw, "seed": seed, "cell_id": cell,
            "polarization": pol, "successful_cw_count": successful,
            "delivered_information_bits": 1024 * successful,
            "full_frame_cw_errors": 16 - successful, "full_frame_cw_total": 16,
            "total_transmitted_symbols_per_polarization":
                next(item["total_symbols"] for item in manifest["tuples"]
                     if item["tuple_id"] == tuple_id),
        })
    return rows


def test_df03_bps_selection_uses_cw_goodput_cwer_then_lower_b_and_nw():
    api = _api()
    manifest = api.build_dev_manifest(_authority())
    rows = _bps_rows(manifest)
    winner = api.select_bps_pair(rows, tuple_id="M2_N100", manifest=manifest)
    assert (winner.B, winner.Nw) == (32, 31)
    base = api.BpsSelection("M2_N100", 64, 127, Fraction(1, 2), Fraction(1, 8))
    assert api.bps_selection_key(api.BpsSelection(
        "M2_N100", 64, 127, Fraction(3, 4), Fraction(1, 4))) < api.bps_selection_key(base)
    assert api.bps_selection_key(api.BpsSelection(
        "M2_N100", 64, 127, Fraction(1, 2), Fraction(1, 16))) < api.bps_selection_key(base)
    assert api.bps_selection_key(api.BpsSelection(
        "M2_N100", 32, 127, Fraction(1, 2), Fraction(1, 8))) < api.bps_selection_key(base)
    assert api.bps_selection_key(api.BpsSelection(
        "M2_N100", 64, 31, Fraction(1, 2), Fraction(1, 8))) < api.bps_selection_key(base)
    bad = dict(rows[0], delivered_information_bits=rows[0]["delivered_information_bits"] - 1)
    with pytest.raises(api.FreezeError, match="1024"):
        api.select_bps_pair([bad, *rows[1:]], tuple_id="M2_N100", manifest=manifest)
    bad_bool = dict(rows[0], full_frame_cw_errors=True)
    with pytest.raises(api.FreezeError, match="exact integer"):
        api.select_bps_pair([bad_bool, *rows[1:]], tuple_id="M2_N100", manifest=manifest)


def test_df04_binary64_aggregate_is_lossless_and_rejects_ordinary_sum():
    api = _api()
    values = [float.fromhex("0x1.0000000000001p+0"), 1.0, -1.0]
    aggregate = api.exact_binary64_aggregate(values)
    exact = sum((Fraction.from_float(value) for value in values), Fraction())
    assert Fraction(int(aggregate.numerator_decimal), 1 << aggregate.denominator_power2) == exact
    assert aggregate.count == 3
    with pytest.raises(api.FreezeError, match="ordinary float"):
        api.exact_binary64_aggregate(values, ordinary_float_sum=sum(values))


def _hmm_chunks(manifest, *, authority, tuple_id="M2_N100", values=(1.0, 2.0)):
    import schemas

    chunks = []
    contents = []
    layout = next(item for item in manifest["tuples"] if item["tuple_id"] == tuple_id)
    roles = manifest["membership_per_cell_pol"]
    for p_index, value in enumerate(values):
        for cell in (item["cell_id"] for item in manifest["cells"]):
            for pol in ("X", "Y"):
                for role, count in roles.items():
                    exact = Fraction.from_float(value) * count
                    denominator_power2 = exact.denominator.bit_length() - 1
                    binding = schemas.hmm_chunk_authority_binding(
                        owner_authority=authority, tuple_id=tuple_id,
                        stratum_role=role, cell_id=cell, polarization=pol,
                        p_s_index=p_index, sigma_e2_index=0,
                    )
                    members = tuple(
                        schemas.ResolvedMemberContent(
                            ordinal=index,
                            content_sha256=hashlib.sha256(
                                f"{binding['computation_root']}:{index}".encode()
                            ).hexdigest(),
                            normalized_nll=float(value),
                        )
                        for index in range(count)
                    )
                    content = schemas.build_hmm_runtime_aggregate_content(
                        stratum_role=role,
                        computation_ids_manifest_sha256=binding["computation_root"],
                        resolved_members=members,
                    )
                    contents.append(content)
                    chunks.append(schemas.row_from_mapping("b2_hmm_grid_chunk", {
                        "record_type": "B2_HMM_GRID_CHUNK",
                        "tuple_id": tuple_id, "M": layout["M"], "N": layout["N"],
                        "p_s_index": p_index,
                        "p_s_float64_hex": manifest["p_s_grid"][p_index]["float64_hex"],
                        "sigma_e2_index": 0,
                        "sigma_e2_float64_hex": manifest["sigma_e2_grid"][0]["float64_hex"],
                        "stratum_role": role, "cell_id": cell, "polarization": pol,
                        "chunk_id": binding["chunk_id"],
                        "pilot_count": layout["periodic_pilot_count"],
                        "member_count": count,
                        "member_key_manifest_sha256": binding["member_root"],
                        "normalized_nll_exact_sum_numerator_decimal": str(exact.numerator),
                        "normalized_nll_exact_sum_denominator_power2": denominator_power2,
                        "objective_included": role != "CONTROLLED_SENTINEL_EXCLUDED",
                        "computation_ids_manifest_sha256": binding["computation_root"],
                        "content_sha256": content.content_sha256,
                    }))
    return chunks, tuple(contents)


def test_df05_hmm_requires_complete_members_and_excludes_costed_sentinel():
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    chunks, contents = _hmm_chunks(manifest, authority=authority, values=(1.0,))
    result = api.select_hmm_pair(
        chunks, tuple_id="M2_N100", manifest=manifest,
        owner_authority=authority, runtime_contents=contents)
    assert result.objective == Fraction(1, 1)
    assert result.receipted_primitive_scores == 24 * (10 + 90 + 90)
    assert result.objective_primitive_scores == 24 * (10 + 90)
    assert result.sentinel_primitive_scores == 24 * 90
    broken = list(chunks)
    broken[0] = dataclasses.replace(broken[0], member_count=9)
    with pytest.raises(api.FreezeError, match="member completeness"):
        api.select_hmm_pair(broken, tuple_id="M2_N100", manifest=manifest,
                            owner_authority=authority, runtime_contents=contents)


@pytest.mark.parametrize(("field", "value"), [
    ("p_s_index", 122), ("sigma_e2_index", 6),
    ("p_s_index", True), ("sigma_e2_index", "0"),
])
def test_df05_hmm_revalidates_typed_grid_indices(field, value):
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    chunks, contents = _hmm_chunks(manifest, authority=authority, values=(1.0,))
    broken = list(chunks)
    broken[0] = dataclasses.replace(broken[0], **{field: value})
    with pytest.raises(api.FreezeError):
        api.select_hmm_pair(broken, tuple_id="M2_N100", manifest=manifest,
                            owner_authority=authority, runtime_contents=contents)


@pytest.mark.parametrize("mutation", [
    {"record_type": None}, {"member_keys": (1,)},
    {"logical_primitive_scores": 10.0},
])
def test_df05_hmm_rejects_untyped_or_legacy_chunks(mutation):
    import schemas

    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    chunks, contents = _hmm_chunks(manifest, authority=authority, values=(1.0,))
    bad = schemas.row_to_mapping(chunks[0])
    if mutation.get("record_type", "present") is None:
        bad.pop("record_type")
    else:
        bad.update(mutation)
    with pytest.raises(api.FreezeError):
        api.select_hmm_pair([bad, *chunks[1:]], tuple_id="M2_N100", manifest=manifest,
                            owner_authority=authority, runtime_contents=contents)


def test_df05_hmm_rejects_cross_group_duplicate_member_identity():
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    chunks, contents = _hmm_chunks(manifest, authority=authority, values=(1.0,))
    broken = list(chunks)
    broken[1] = dataclasses.replace(
        broken[1], member_key_manifest_sha256=broken[0].member_key_manifest_sha256)
    with pytest.raises(api.FreezeError, match="member identity"):
        api.select_hmm_pair(broken, tuple_id="M2_N100", manifest=manifest,
                            owner_authority=authority, runtime_contents=contents)


def test_df06_row_and_chunk_order_do_not_change_objective_or_winner():
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    bps = _bps_rows(manifest)
    hmm, contents = _hmm_chunks(manifest, authority=authority)
    expected_bps = api.select_bps_pair(bps, tuple_id="M2_N100", manifest=manifest)
    expected_hmm = api.select_hmm_pair(
        hmm, tuple_id="M2_N100", manifest=manifest,
        owner_authority=authority, runtime_contents=contents)
    assert (expected_hmm.receipted_primitive_scores,
            expected_hmm.objective_primitive_scores,
            expected_hmm.sentinel_primitive_scores) == (4560, 2400, 2160)
    random.Random(17).shuffle(bps)
    random.Random(23).shuffle(hmm)
    assert api.select_bps_pair(bps, tuple_id="M2_N100", manifest=manifest) == expected_bps
    assert api.select_hmm_pair(
        hmm, tuple_id="M2_N100", manifest=manifest,
        owner_authority=authority, runtime_contents=contents) == expected_hmm
    assert (expected_hmm.p_s_index, expected_hmm.sigma_e2_index) == (0, 0)


@pytest.mark.parametrize("attack", [
    "numerator", "content", "chunk", "member_nondev", "computation",
])
def test_df06_hmm_selection_rejects_detached_or_nondev_authority(attack):
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    chunks, contents = _hmm_chunks(
        manifest, authority=authority, values=(1.0, 2.0))
    broken = list(chunks)
    if attack == "numerator":
        broken[0] = dataclasses.replace(
            broken[0], normalized_nll_exact_sum_numerator_decimal="6253")
    elif attack == "content":
        broken[0] = dataclasses.replace(broken[0], content_sha256="f" * 64)
    elif attack == "chunk":
        broken[0] = dataclasses.replace(broken[0], chunk_id=broken[1].chunk_id)
    elif attack == "member_nondev":
        nondev_root = hashlib.sha256(
            json.dumps(list(range(8100, 8110)), separators=(",", ":")).encode()
        ).hexdigest()
        broken[0] = dataclasses.replace(
            broken[0], member_key_manifest_sha256=nondev_root)
    else:
        broken[0] = dataclasses.replace(
            broken[0], computation_ids_manifest_sha256="e" * 64)
    with pytest.raises(api.FreezeError, match="authenticated HMM"):
        api.select_hmm_pair(
            broken, tuple_id="M2_N100", manifest=manifest,
            owner_authority=authority, runtime_contents=contents)


def _tuple_rows(manifest):
    clean = []
    controlled = []
    tuple_layout = {item["tuple_id"]: item for item in manifest["tuples"]}
    fixtures = tuple(manifest["fixtures"])
    for tuple_id, layout in tuple_layout.items():
        for seed in manifest["dev_seeds"]:
            for cell in (item["cell_id"] for item in manifest["cells"]):
                for pol in manifest["polarizations"]:
                    clean.append({
                        "record_type": "B2_TUPLE_CLEAN_DEV", "tuple_id": tuple_id,
                        "seed": seed, "cell_id": cell, "polarization": pol,
                        "bps_freeze_ref": f"bps:{tuple_id}",
                        "statistic_freeze_ref": f"stat:{tuple_id}",
                        "successful_cw_count": 15,
                        "delivered_information_bits": 15 * 1024,
                        "full_frame_cw_errors": 1, "information_bit_errors": 1,
                        "total_transmitted_symbols_per_polarization": layout["total_symbols"],
                        "computation_id": f"clean:{tuple_id}:{seed}:{cell}:{pol}",
                        "result_receipt_sha256": H,
                    })
                for target in manifest["polarizations"]:
                    sentinel = "Y" if target == "X" else "X"
                    for fixture in fixtures:
                        boundary = int(fixture[1:3])
                        rotation = int(fixture[-1])
                        for row_pol, role in ((target, "TARGET_INCLUDED"),
                                              (sentinel, "SENTINEL_EXCLUDED")):
                            row = {
                                "record_type": "B2_TUPLE_CONTROLLED_DEV",
                                "tuple_id": tuple_id, "seed": seed, "cell_id": cell,
                                "target_polarization": target, "row_polarization": row_pol,
                                "row_role": role, "fixture_id": fixture,
                                "boundary_after_cw": boundary, "rotation_k": rotation,
                                "bps_freeze_ref": f"bps:{tuple_id}",
                                "statistic_freeze_ref": f"stat:{tuple_id}",
                                "successful_cw_count": 14,
                                "delivered_information_bits": 14 * 1024,
                                "full_frame_cw_errors": 2,
                                "total_transmitted_symbols_per_polarization": layout["total_symbols"],
                                "computation_id": (
                                    f"control:{tuple_id}:{seed}:{cell}:{target}:{fixture}:{row_pol}"
                                ),
                                "cache_status": "EXECUTED" if role == "TARGET_INCLUDED" else "CACHE_READ",
                                "source_computation_id": None if role == "TARGET_INCLUDED" else (
                                    f"clean:{tuple_id}:{seed}:{cell}:{sentinel}"
                                ),
                                "result_receipt_sha256": H,
                            }
                            if role == "TARGET_INCLUDED":
                                row.update(affected_cw_errors=1, affected_cw_total=16 - boundary)
                            controlled.append(row)
    return clean, controlled


def test_df07_tuple_tables_have_exact_clean_target_and_sentinel_roles():
    api = _api()
    manifest = api.build_dev_manifest(_authority())
    clean, controlled = _tuple_rows(manifest)
    result = api.validate_b2_tuple_rows(clean, controlled, manifest=manifest)
    assert result == {
        "clean": 1200, "controlled": 21600,
        "controlled_target": 10800, "controlled_sentinel": 10800,
    }
    broken = list(controlled)
    broken[0] = dict(broken[0], row_role="SENTINEL_EXCLUDED")
    with pytest.raises(api.FreezeError, match="role"):
        api.validate_b2_tuple_rows(clean, broken, manifest=manifest)
    broken = list(controlled)
    broken[1] = dict(broken[1], affected_cw_errors=1, affected_cw_total=12)
    with pytest.raises(api.FreezeError, match="affected"):
        api.validate_b2_tuple_rows(clean, broken, manifest=manifest)


def test_df08_final_tuple_uses_the_complete_exact_lexicographic_chain():
    api = _api()
    F = Fraction
    base = api.B2TupleSelection("M3_N100", F(3, 4), F(64, 6240), F(1, 8), 3, 3)
    assert api.b2_tuple_selection_key(api.B2TupleSelection(
        "M3_N100", F(4, 5), F(64, 6240), F(1, 4), 3, 3)) < api.b2_tuple_selection_key(base)
    assert api.b2_tuple_selection_key(api.B2TupleSelection(
        "M3_N200", F(3, 4), F(32, 6208), F(1, 4), 3, 4)) < api.b2_tuple_selection_key(base)
    assert api.b2_tuple_selection_key(api.B2TupleSelection(
        "M3_N100", F(3, 4), F(64, 6240), F(1, 16), 3, 3)) < api.b2_tuple_selection_key(base)
    assert api.b2_tuple_selection_key(api.B2TupleSelection(
        "M2_N100", F(3, 4), F(64, 6240), F(1, 8), 2, 0)) < api.b2_tuple_selection_key(base)
    assert api.b2_tuple_selection_key(api.B2TupleSelection(
        "M3_N10", F(3, 4), F(64, 6240), F(1, 8), 3, 1)) < api.b2_tuple_selection_key(base)


def test_df09_freeze_persists_five_five_one_and_every_candidate_key_and_raw_hash(tmp_path):
    api = _api()
    authority = _authority()
    manifest = api.build_dev_manifest(authority)
    bps = api.fit_common_bps(_bps_rows(manifest), manifest=manifest, raw_sha256="1" * 64)
    hmm = []
    contents = []
    for layout in manifest["tuples"]:
        tuple_chunks, tuple_contents = _hmm_chunks(
            manifest, authority=authority, tuple_id=layout["tuple_id"],
            values=(1.0, 2.0))
        hmm.extend(tuple_chunks)
        contents.extend(tuple_contents)
    statistics = api.fit_b2_statistics(
        hmm, manifest=manifest, owner_authority=authority,
        runtime_contents=tuple(contents),
        raw_sha256="2" * 64)
    clean, controlled = _tuple_rows(manifest)
    tuples = api.select_b2_tuple(
        clean, controlled, manifest=manifest, bps_freeze=bps,
        statistic_freeze=statistics, clean_raw_sha256="3" * 64,
        controlled_raw_sha256="4" * 64,
    )
    resolved = api.resolve_dev_freeze(
        bps, statistics, tuples, owner_sha256=manifest["owner_sha256"])
    assert len(resolved.parameters["common_bps"]) == 5
    assert len(resolved.parameters["b2_statistics"]) == 5
    assert resolved.parameters["final_b2_tuple"]["tuple_id"] in {
        item["tuple_id"] for item in manifest["tuples"]
    }
    assert all(item["candidates"] for item in resolved.parameters["common_bps"])
    assert all(item["candidates"] for item in resolved.parameters["b2_statistics"])
    assert len(resolved.parameters["b2_tuple_candidates"]) == 5
    assert dict(resolved.receipts["raw_hashes"].items()) == {
        "raw_bps_dev_sha256": "1" * 64,
        "hmm_grid_dev_chunks_sha256": "2" * 64,
        "raw_b2_tuple_clean_dev_sha256": "3" * 64,
        "raw_b2_tuple_controlled_dev_sha256": "4" * 64,
    }
    path = tmp_path / "dev_freeze.json"
    api.write_resolved_freeze(path, resolved)
    loaded = api.load_resolved_freeze(path)
    assert loaded == resolved
    with pytest.raises(api.FreezeError, match="immutable"):
        api.write_resolved_freeze(path, resolved)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == resolved.freeze_id
    assert json.loads(path.read_text(encoding="utf-8"))["schema"] == (
        "coded_decoder_feedback.d0.dev_freeze.v1")


@pytest.mark.parametrize("bad_seed", [None, 7999, 8010, 8100, 900000001])
def test_df10_all_fit_apis_reject_nondev_seeds(bad_seed):
    api = _api()
    manifest = api.build_dev_manifest(_authority())
    bps_rows = _bps_rows(manifest)
    bps_rows[0] = dict(bps_rows[0], seed=bad_seed)
    with pytest.raises(api.FreezeError, match="dev-only"):
        api.fit_common_bps(bps_rows, manifest=manifest, raw_sha256="1" * 64)
    with pytest.raises(api.FreezeError, match="dev-only"):
        api.fit_b2_statistics(
            (), manifest=dict(manifest, dev_seeds=[*manifest["dev_seeds"][:-1], bad_seed]),
            owner_authority=_authority(), runtime_contents=(), raw_sha256="2" * 64)
    clean, controlled = _tuple_rows(manifest)
    clean[0] = dict(clean[0], seed=bad_seed)
    with pytest.raises(api.FreezeError, match="dev-only"):
        api.select_b2_tuple(
            clean, controlled, manifest=manifest, bps_freeze=None,
            statistic_freeze=None, clean_raw_sha256="3" * 64,
            controlled_raw_sha256="4" * 64,
        )


def _fraction_document(value):
    value = Fraction(value)
    return {"numerator_decimal": str(value.numerator), "denominator": value.denominator}


def _legal_freeze_document():
    manifest = _api().build_dev_manifest(_authority())
    bps = []
    statistics = []
    tuples = []
    for legal_order, layout in enumerate(manifest["tuples"]):
        tuple_id = layout["tuple_id"]
        bps_candidates = []
        for B in manifest["B_values"]:
            for Nw in manifest["Nw_values"]:
                goodput = Fraction(15 * 1024, layout["total_symbols"])
                cwer = Fraction(1, 16)
                bps_candidates.append({
                    "B": B, "Nw": Nw,
                    "macro_net_goodput": _fraction_document(goodput),
                    "macro_full_frame_cwer": _fraction_document(cwer),
                    "exact_lexicographic_key": [
                        _fraction_document(-goodput), _fraction_document(cwer), B, Nw,
                    ],
                    "raw_sha256": "1" * 64,
                })
        bps.append({"tuple_id": tuple_id, "winner": copy.deepcopy(bps_candidates[0]),
                    "candidates": bps_candidates})
        statistic_candidates = []
        for index, objective in enumerate((Fraction(1), Fraction(2))):
            statistic_candidates.append({
                "p_s_index": index, "sigma_e2_index": 0,
                "objective": _fraction_document(objective),
                "exact_lexicographic_key": [_fraction_document(objective), index, 0],
                "receipted_primitive_scores": 4560,
                "objective_primitive_scores": 2400,
                "sentinel_primitive_scores": 2160,
                "raw_sha256": "2" * 64,
            })
        statistics.append({
            "tuple_id": tuple_id, "winner": copy.deepcopy(statistic_candidates[0]),
            "candidates": statistic_candidates,
        })
        goodput = Fraction(1, 2)
        pilot_fraction = Fraction(
            layout["periodic_pilot_count"], layout["total_symbols"])
        affected = Fraction(1, 8)
        tuples.append({
            "tuple_id": tuple_id,
            "combined_macro_net_goodput": _fraction_document(goodput),
            "periodic_pilot_fraction": _fraction_document(pilot_fraction),
            "macro_controlled_target_affected_cwer": _fraction_document(affected),
            "M": layout["M"], "legal_order": legal_order,
            "exact_lexicographic_key": [
                _fraction_document(-goodput), _fraction_document(pilot_fraction),
                _fraction_document(affected), layout["M"], legal_order,
            ],
            "raw_sha256": {"clean": "3" * 64, "controlled": "4" * 64},
        })
    return {
        "schema": "coded_decoder_feedback.d0.dev_freeze.v1",
        "owner_sha256": manifest["owner_sha256"],
        "raw_hashes": {
            "raw_bps_dev_sha256": "1" * 64,
            "hmm_grid_dev_chunks_sha256": "2" * 64,
            "raw_b2_tuple_clean_dev_sha256": "3" * 64,
            "raw_b2_tuple_controlled_dev_sha256": "4" * 64,
        },
        "common_bps": bps, "b2_statistics": statistics,
        "b2_tuple_candidates": tuples, "final_b2_tuple": copy.deepcopy(tuples[4]),
        "test_rows_read": False,
    }


def test_df11_real_evaluator_and_benchmark_cannot_reach_any_fit_api(monkeypatch):
    api = _api()
    import benchmark
    import contract

    forbidden = {
        "fit_common_bps", "fit_b2_statistics", "fit_b2_tuple", "select_b2_tuple"
    }
    assert callable(api.fit_common_bps)
    assert callable(api.fit_b2_statistics)
    assert callable(api.fit_b2_tuple)

    benchmark_tree = ast.parse(Path(benchmark.__file__).read_text(encoding="utf-8"))
    evaluator_tree = ast.parse(inspect.getsource(contract.finalize_truth_view))
    for tree in (benchmark_tree, evaluator_tree):
        names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        attributes = {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        assert forbidden.isdisjoint(names | attributes)
        assert not any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and any(alias.name == "importlib" for alias in node.names)
            for node in ast.walk(tree)
        )
        assert not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"__import__", "eval", "exec"}
            for node in ast.walk(tree)
        )

    calls = []

    def forbidden_fit(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("fit API became reachable")

    for name in ("fit_common_bps", "fit_b2_statistics", "fit_b2_tuple"):
        monkeypatch.setattr(api, name, forbidden_fit)

    resolved = api.resolved_freeze_from_document(_legal_freeze_document())
    receipts = tuple(
        {"phase": phase, "dev_freeze_sha256": resolved.freeze_id}
        for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4")
    )
    binding = benchmark.bind_resolved_freeze(
        resolved, receipts, benchmark_freeze_sha256=resolved.freeze_id
    )
    assert binding.dev_freeze_sha256 == resolved.freeze_id
    benchmark.build_full_work_projection()

    truth = contract.TruthView(
        information_bits=np.zeros((2, 16, 1024), dtype=np.uint8),
        coded_bits=np.zeros((2, 16, 1536), dtype=np.uint8),
        transmitted_symbols=np.ones((2, 6240), dtype=np.complex128),
        true_phase=np.zeros((2, 6240), dtype=np.float64),
        channel_h=np.ones((2, 6240), dtype=np.complex128),
        physical_snr_db=14.0,
        fade=np.ones((2, 6240), dtype=np.float64),
        noise_receipt={"samples": np.zeros((2, 6240), dtype=np.complex128)},
        event_label="df11-runtime-tripwire",
    )
    evaluated = contract.finalize_truth_view(
        truth,
        decoded_information_bits=np.zeros((2, 16, 1024), dtype=np.uint8),
    )
    assert evaluated.final_codeword_correctness.all()
    assert calls == []


def test_df12_all_phase_receipts_bind_one_resolved_freeze_hash(tmp_path):
    api = _api()
    resolved = api.resolved_freeze_from_document(_legal_freeze_document())
    receipts = [{"phase": phase, "dev_freeze_sha256": resolved.freeze_id}
                for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4")]
    assert api.assert_phase_freeze_chronology(resolved, receipts) == resolved.freeze_id
    with pytest.raises(api.FreezeError, match="same dev freeze"):
        api.assert_phase_freeze_chronology(
            resolved, [*receipts[:-1], {"phase": "S4", "dev_freeze_sha256": H}])
    with pytest.raises(api.FreezeError, match="five phase"):
        api.assert_phase_freeze_chronology(resolved, receipts[:-1])


@pytest.mark.parametrize("mutation", [
    "missing_bps_pair", "empty_statistics", "too_many_tuples",
    "duplicate_bps_tuple", "wrong_final_binding", "candidate_raw_hash",
    "candidate_exact_key",
])
def test_df12_loader_rejects_non_five_five_one_or_unbound_candidates(mutation, tmp_path):
    api = _api()
    import artifacts

    document = _legal_freeze_document()
    if mutation == "missing_bps_pair":
        document["common_bps"] = document["common_bps"][:-1]
    elif mutation == "empty_statistics":
        document["b2_statistics"] = []
    elif mutation == "too_many_tuples":
        document["b2_tuple_candidates"].append(
            copy.deepcopy(document["b2_tuple_candidates"][0]))
    elif mutation == "duplicate_bps_tuple":
        document["common_bps"][-1]["tuple_id"] = document["common_bps"][0]["tuple_id"]
    elif mutation == "wrong_final_binding":
        document["final_b2_tuple"]["tuple_id"] = "M2_N100"
    elif mutation == "candidate_raw_hash":
        document["b2_statistics"][0]["candidates"][0]["raw_sha256"] = H
    elif mutation == "candidate_exact_key":
        document["common_bps"][0]["candidates"][0]["exact_lexicographic_key"][-1] = 999
    with pytest.raises(api.FreezeError):
        api.resolved_freeze_from_document(document)
    path = tmp_path / f"{mutation}.json"
    path.write_bytes(artifacts.canonical_json_bytes(document))
    with pytest.raises(api.FreezeError):
        api.load_resolved_freeze(path)
