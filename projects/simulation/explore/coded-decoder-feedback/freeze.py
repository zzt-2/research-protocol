"""Deterministic D0 development manifest and dev-only selection reducers.

This module is engineering-only: it freezes no scientific result and performs
no I/O.  Every domain is derived from the authenticated YAML owner.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

import artifacts
import contract
import schemas


class FreezeError(ValueError):
    """Raised when dev evidence is incomplete, ambiguous, or non-canonical."""


_TUPLE_LAYOUT = {
    "M2_N100": (2, 100, 64, 6240),
    "M3_N10": (3, 10, 684, 6860),
    "M3_N20": (3, 20, 325, 6501),
    "M3_N100": (3, 100, 64, 6240),
    "M3_N200": (3, 200, 32, 6208),
}
_MEMBERSHIP = {
    "CLEAN_INCLUDED": 10,
    "CONTROLLED_TARGET_INCLUDED": 90,
    "CONTROLLED_SENTINEL_EXCLUDED": 90,
}


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if type(value) is tuple:
        return [_plain(item) for item in value]
    return value


def build_dev_manifest(authority: contract.D0OwnerIdentityAuthority) -> dict[str, Any]:
    """Build the canonical dev-only manifest from an authenticated owner."""

    contract.assert_frozen_owner_identity_authority(authority)
    domain = authority.ordinary_domain
    grids = authority.identity_binding.grid_authority
    p_s = _plain(grids["p_s"]["standalone_payload"])["values"]
    sigma = _plain(grids["sigma_e2"]["standalone_payload"])["values"]
    tuples = []
    for tuple_id in domain.tuple_ids:
        try:
            M, N, pilot_count, total_symbols = _TUPLE_LAYOUT[tuple_id]
        except KeyError as exc:
            raise FreezeError(f"unknown owner tuple {tuple_id}") from exc
        tuples.append({
            "tuple_id": tuple_id, "M": M, "N": N,
            "periodic_pilot_count": pilot_count, "total_symbols": total_symbols,
        })
    return {
        "schema": "coded_decoder_feedback.d0.dev_manifest.v1",
        "owner_sha256": authority.owner_sha256,
        "dev_seeds": list(authority.contract.seed_registry.range_for(
            "common_cpr_and_b2_dev").values),
        "cells": [
            {"cell_id": cell.cell_id, "snr_db": cell.snr_db,
             "linewidth_hz": cell.linewidth_hz}
            for cell in authority.contract.population_manifest
        ],
        "tuples": tuples,
        "B_values": list(domain.b_values), "Nw_values": list(domain.nw_values),
        "polarizations": list(domain.polarizations),
        "fixtures": list(domain.fixtures),
        "p_s_grid": p_s, "sigma_e2_grid": sigma,
        "membership_per_cell_pol": dict(_MEMBERSHIP),
        "expected_cardinalities": {
            "BPS_DEV_SCORE": 7200,
            "B2_TUPLE_CLEAN_DEV": 1200,
            "B2_TUPLE_CONTROLLED_DEV": 21600,
        },
    }


def expected_bps_primary_keys(manifest: Mapping[str, Any]) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        ("BPS_DEV_SCORE", item["tuple_id"], B, Nw, seed, cell["cell_id"], pol)
        for item in manifest["tuples"]
        for B in manifest["B_values"] for Nw in manifest["Nw_values"]
        for seed in manifest["dev_seeds"] for cell in manifest["cells"]
        for pol in manifest["polarizations"]
    )


@dataclass(frozen=True, slots=True)
class BpsSelection:
    tuple_id: str
    B: int
    Nw: int
    macro_net_goodput: Fraction
    macro_full_frame_cwer: Fraction


def bps_selection_key(item: BpsSelection) -> tuple[Fraction, Fraction, int, int]:
    """Owner-ordered key: goodput, CWER, B, then Nw."""

    return (-item.macro_net_goodput, item.macro_full_frame_cwer, item.B, item.Nw)


def _bps_candidates(rows: Sequence[Mapping[str, Any]], *, tuple_id: str,
                    manifest: Mapping[str, Any]) -> tuple[BpsSelection, ...]:

    expected = {key for key in expected_bps_primary_keys(manifest) if key[1] == tuple_id}
    selected = [row for row in rows if row.get("tuple_id") == tuple_id]
    keys = [(
        row.get("record_type"), row.get("tuple_id"), row.get("B"), row.get("Nw"),
        row.get("seed"), row.get("cell_id"), row.get("polarization"),
    ) for row in selected]
    if len(keys) != len(set(keys)) or set(keys) != expected:
        raise FreezeError("BPS primary-key coverage/duplicate mismatch")
    totals: dict[tuple[int, int, str, str], list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for row in selected:
        successful = row.get("successful_cw_count")
        delivered = row.get("delivered_information_bits")
        errors = row.get("full_frame_cw_errors")
        cw_total = row.get("full_frame_cw_total")
        symbols = row.get("total_transmitted_symbols_per_polarization")
        if (type(successful) is not int or type(delivered) is not int
                or type(errors) is not int or type(cw_total) is not int
                or type(symbols) is not int or not 0 <= successful <= 16
                or delivered != 1024 * successful or errors != 16 - successful
                or cw_total != 16 or symbols <= 0):
            raise FreezeError(
                "CW goodput fields must be exact integers obeying the 1024-bit definition")
        bucket = totals[(row["B"], row["Nw"], row["cell_id"], row["polarization"])]
        bucket[0] += delivered; bucket[1] += symbols
        bucket[2] += errors; bucket[3] += cw_total
    candidates = []
    cell_ids = [item["cell_id"] for item in manifest["cells"]]
    for B in manifest["B_values"]:
        for Nw in manifest["Nw_values"]:
            per_cell = []
            for cell in cell_ids:
                pol_values = []
                for pol in manifest["polarizations"]:
                    delivered, symbols, errors, cw_total = totals[(B, Nw, cell, pol)]
                    pol_values.append((Fraction(delivered, symbols), Fraction(errors, cw_total)))
                per_cell.append((sum((v[0] for v in pol_values), Fraction()) / 2,
                                 sum((v[1] for v in pol_values), Fraction()) / 2))
            goodput = sum((v[0] for v in per_cell), Fraction()) / len(per_cell)
            cwer = sum((v[1] for v in per_cell), Fraction()) / len(per_cell)
            candidates.append(BpsSelection(tuple_id, B, Nw, goodput, cwer))
    return tuple(candidates)


def select_bps_pair(rows: Sequence[Mapping[str, Any]], *, tuple_id: str,
                    manifest: Mapping[str, Any]) -> BpsSelection:
    """Select one BPS pair using integer-ratio CW goodput and CWER."""

    return min(_bps_candidates(rows, tuple_id=tuple_id, manifest=manifest),
               key=bps_selection_key)


@dataclass(frozen=True, slots=True)
class ExactBinary64Aggregate:
    numerator_decimal: str
    denominator_power2: int
    count: int


def exact_binary64_aggregate(values: Sequence[float], *,
                             ordinary_float_sum: float | None = None
                             ) -> ExactBinary64Aggregate:
    if ordinary_float_sum is not None:
        raise FreezeError("ordinary float chunk summation is forbidden")
    if not values:
        raise FreezeError("binary64 aggregate requires at least one value")
    if any(type(value) is not float or not math.isfinite(value) for value in values):
        raise FreezeError("aggregate values must be finite exact binary64 floats")
    total = sum((Fraction.from_float(value) for value in values), Fraction())
    denominator = total.denominator
    if denominator & (denominator - 1):
        raise AssertionError("binary64 denominator must be a power of two")
    return ExactBinary64Aggregate(str(total.numerator), denominator.bit_length() - 1, len(values))


@dataclass(frozen=True, slots=True)
class HmmSelection:
    tuple_id: str
    p_s_index: int
    sigma_e2_index: int
    objective: Fraction
    receipted_primitive_scores: int
    objective_primitive_scores: int
    sentinel_primitive_scores: int


def _hmm_candidates(chunks: Sequence[schemas.B2HmmGridChunkRow], *, tuple_id: str,
                    manifest: Mapping[str, Any], owner_authority: Any,
                    runtime_contents: Sequence[schemas.HmmRuntimeAggregateContent]
                    ) -> tuple[HmmSelection, ...]:

    try:
        contract.assert_frozen_owner_identity_authority(owner_authority)
    except (contract.ContractError, TypeError, ValueError) as exc:
        raise FreezeError(f"authenticated HMM owner mismatch: {exc}") from exc
    if _plain(manifest) != build_dev_manifest(owner_authority):
        raise FreezeError("authenticated HMM manifest mismatch: fit API is dev-only")
    if any(type(row) is not schemas.B2HmmGridChunkRow for row in chunks):
        raise FreezeError("HMM chunks must be exact typed owner-schema rows")
    if (type(runtime_contents) not in (tuple, list)
            or any(type(item) is not schemas.HmmRuntimeAggregateContent
                   for item in runtime_contents)):
        raise FreezeError("authenticated HMM runtime contents are required")
    content_by_computation: dict[str, schemas.HmmRuntimeAggregateContent] = {}
    for content in runtime_contents:
        try:
            schemas.assert_hmm_runtime_aggregate_content(
                content, stratum_role=content.stratum_role)
        except (schemas.SchemaError, TypeError, ValueError) as exc:
            raise FreezeError(f"authenticated HMM runtime content mismatch: {exc}") from exc
        root = content.computation_ids_manifest_sha256
        if root in content_by_computation:
            raise FreezeError("authenticated HMM runtime content is duplicated")
        content_by_computation[root] = content
    for row in chunks:
        try:
            canonical = schemas.row_from_mapping(
                "b2_hmm_grid_chunk", schemas.row_to_mapping(row))
        except (schemas.SchemaError, TypeError, ValueError) as exc:
            raise FreezeError(f"invalid typed HMM chunk: {exc}") from exc
        if row != canonical:
            raise FreezeError("typed HMM chunk canonical reconstruction mismatch")
        try:
            expected = schemas.hmm_chunk_authority_binding(
                owner_authority=owner_authority, tuple_id=row.tuple_id,
                stratum_role=row.stratum_role, cell_id=row.cell_id,
                polarization=row.polarization, p_s_index=row.p_s_index,
                sigma_e2_index=row.sigma_e2_index,
            )
        except (schemas.SchemaError, TypeError, ValueError) as exc:
            raise FreezeError(f"authenticated HMM group mismatch: {exc}") from exc
        if (row.chunk_id != expected["chunk_id"]
                or row.member_key_manifest_sha256 != expected["member_root"]
                or row.computation_ids_manifest_sha256 != expected["computation_root"]):
            raise FreezeError(
                "authenticated HMM chunk/member identity/computation binding mismatch")
        if row.member_count != _MEMBERSHIP.get(row.stratum_role):
            raise FreezeError("HMM member completeness mismatch")
        content = content_by_computation.get(row.computation_ids_manifest_sha256)
        if (content is None or content.stratum_role != row.stratum_role
                or content.content_sha256 != row.content_sha256
                or content.member_count != row.member_count
                or content.normalized_nll_exact_sum_numerator_decimal
                != row.normalized_nll_exact_sum_numerator_decimal
                or content.normalized_nll_exact_sum_denominator_power2
                != row.normalized_nll_exact_sum_denominator_power2):
            raise FreezeError("authenticated HMM runtime aggregate/content mismatch")
    if set(content_by_computation) != {
            row.computation_ids_manifest_sha256 for row in chunks}:
        raise FreezeError("authenticated HMM runtime content coverage mismatch")
    selected = [row for row in chunks if row.tuple_id == tuple_id]
    group_keys = [(
        row.p_s_index, row.sigma_e2_index, row.stratum_role,
        row.cell_id, row.polarization,
    ) for row in selected]
    if len(group_keys) != len(set(group_keys)):
        raise FreezeError("duplicate HMM chunk group")
    cells = tuple(item["cell_id"] for item in manifest["cells"])
    pols = tuple(manifest["polarizations"])
    candidate_ids = sorted({(key[0], key[1]) for key in group_keys})
    if not candidate_ids:
        raise FreezeError("no HMM candidates")
    expected_groups = {
        (p, s, role, cell, pol)
        for p, s in candidate_ids for role in _MEMBERSHIP for cell in cells for pol in pols
    }
    if set(group_keys) != expected_groups:
        raise FreezeError("HMM group completeness mismatch")
    member_roots = [row.member_key_manifest_sha256 for row in selected]
    computation_roots = [row.computation_ids_manifest_sha256 for row in selected]
    if len(member_roots) != len(set(member_roots)):
        raise FreezeError("cross-group duplicate HMM member identity")
    if len(computation_roots) != len(set(computation_roots)):
        raise FreezeError("cross-group duplicate HMM computation identity")
    values_by_group: dict[tuple[Any, ...], Fraction] = {}
    counts_by_candidate: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0, 0])
    for key, row in zip(group_keys, selected):
        role = key[2]
        expected_count = _MEMBERSHIP[role]
        if row.member_count != expected_count:
            raise FreezeError("HMM member completeness mismatch")
        included = role != "CONTROLLED_SENTINEL_EXCLUDED"
        if row.objective_included is not included:
            raise FreezeError("HMM sentinel objective inclusion mismatch")
        try:
            p_literal = manifest["p_s_grid"][row.p_s_index]
            sigma_literal = manifest["sigma_e2_grid"][row.sigma_e2_index]
        except (IndexError, TypeError) as exc:
            raise FreezeError("HMM grid index outside owner manifest") from exc
        if (row.p_s_float64_hex != p_literal["float64_hex"]
                or row.sigma_e2_float64_hex != sigma_literal["float64_hex"]):
            raise FreezeError("HMM grid index/float64 literal mismatch")
        numerator = int(row.normalized_nll_exact_sum_numerator_decimal)
        values_by_group[key] = Fraction(
            numerator, 1 << row.normalized_nll_exact_sum_denominator_power2
        ) / row.member_count
        candidate_counts = counts_by_candidate[(row.p_s_index, row.sigma_e2_index)]
        candidate_counts[0] += row.member_count
        if included:
            candidate_counts[1] += row.member_count
        else:
            candidate_counts[2] += row.member_count
    results = []
    for p, s in candidate_ids:
        role_means = {}
        for role in _MEMBERSHIP:
            per_cell = []
            for cell in cells:
                per_pol = [values_by_group[(p, s, role, cell, pol)] for pol in pols]
                per_cell.append(sum(per_pol, Fraction()) / len(per_pol))
            role_means[role] = sum(per_cell, Fraction()) / len(per_cell)
        objective = (role_means["CLEAN_INCLUDED"]
                     + role_means["CONTROLLED_TARGET_INCLUDED"]) / 2
        receipted, objective_count, sentinel_count = counts_by_candidate[(p, s)]
        results.append(HmmSelection(
            tuple_id, p, s, objective, receipted, objective_count, sentinel_count))
    return tuple(results)


def select_hmm_pair(chunks: Sequence[schemas.B2HmmGridChunkRow], *, tuple_id: str,
                    manifest: Mapping[str, Any], owner_authority: Any,
                    runtime_contents: Sequence[schemas.HmmRuntimeAggregateContent]
                    ) -> HmmSelection:
    """Validate complete HMM chunks and select with exact 0.5/0.5 weighting."""

    return min(_hmm_candidates(
        chunks, tuple_id=tuple_id, manifest=manifest,
        owner_authority=owner_authority, runtime_contents=runtime_contents),
               key=lambda item: (item.objective, item.p_s_index,
                                 item.sigma_e2_index))


@dataclass(frozen=True, slots=True)
class CommonBpsFreeze:
    by_tuple: tuple[tuple[str, BpsSelection, tuple[BpsSelection, ...]], ...]
    raw_sha256: str


@dataclass(frozen=True, slots=True)
class B2StatisticFreeze:
    by_tuple: tuple[tuple[str, HmmSelection, tuple[HmmSelection, ...]], ...]
    raw_sha256: str


@dataclass(frozen=True, slots=True)
class B2TupleSelection:
    tuple_id: str
    combined_macro_net_goodput: Fraction
    periodic_pilot_fraction: Fraction
    macro_controlled_target_affected_cwer: Fraction
    M: int
    legal_order: int


@dataclass(frozen=True, slots=True)
class B2TupleFreeze:
    winner: B2TupleSelection
    candidates: tuple[B2TupleSelection, ...]
    clean_raw_sha256: str
    controlled_raw_sha256: str


def _assert_sha256(value: Any, label: str) -> str:
    if (type(value) is not str or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)):
        raise FreezeError(f"{label} must be lowercase SHA256")
    return value


def _assert_dev_seeds(values: Sequence[Any], manifest: Mapping[str, Any]) -> None:
    expected = tuple(manifest["dev_seeds"])
    actual = tuple(values)
    if (len(actual) != len(set(actual)) or set(actual) != set(expected)
            or any(type(value) is not int for value in actual)):
        raise FreezeError("fit API is dev-only and accepts exactly seeds 8000-8009")


def _observed_row_seeds(rows: Sequence[Mapping[str, Any]],
                        manifest: Mapping[str, Any]) -> None:
    values = tuple(row.get("seed") for row in rows)
    if any(type(value) is not int for value in values):
        raise FreezeError("fit API is dev-only and accepts exactly seeds 8000-8009")
    _assert_dev_seeds(tuple(sorted(set(values))), manifest)


def fit_common_bps(rows: Sequence[Mapping[str, Any]], *,
                   manifest: Mapping[str, Any], raw_sha256: str) -> CommonBpsFreeze:
    """Fit the five common-BPS pairs from the frozen dev population only."""

    _assert_sha256(raw_sha256, "raw_bps_dev_sha256")
    _observed_row_seeds(rows, manifest)
    fitted = []
    for item in manifest["tuples"]:
        tuple_id = item["tuple_id"]
        candidates = _bps_candidates(rows, tuple_id=tuple_id, manifest=manifest)
        fitted.append((tuple_id, min(candidates, key=bps_selection_key), candidates))
    return CommonBpsFreeze(tuple(fitted), raw_sha256)


def fit_b2_statistics(chunks: Sequence[schemas.B2HmmGridChunkRow], *,
                      manifest: Mapping[str, Any], owner_authority: Any,
                      runtime_contents: Sequence[schemas.HmmRuntimeAggregateContent],
                      raw_sha256: str) -> B2StatisticFreeze:
    """Fit the five HMM statistic pairs from explicitly bound dev members."""

    _assert_sha256(raw_sha256, "hmm_grid_dev_chunks_sha256")
    fitted = []
    for item in manifest["tuples"]:
        tuple_id = item["tuple_id"]
        candidates = _hmm_candidates(
            chunks, tuple_id=tuple_id, manifest=manifest,
            owner_authority=owner_authority, runtime_contents=runtime_contents)
        winner = min(candidates, key=lambda value: (
            value.objective, value.p_s_index, value.sigma_e2_index))
        fitted.append((tuple_id, winner, candidates))
    return B2StatisticFreeze(tuple(fitted), raw_sha256)


def _tuple_domains(manifest: Mapping[str, Any]) -> tuple[tuple[str, ...], tuple[int, ...],
                                                        tuple[str, ...], tuple[str, ...]]:
    return (
        tuple(item["tuple_id"] for item in manifest["tuples"]),
        tuple(manifest["dev_seeds"]),
        tuple(item["cell_id"] for item in manifest["cells"]),
        tuple(manifest["polarizations"]),
    )


def validate_b2_tuple_rows(clean_rows: Sequence[Mapping[str, Any]],
                           controlled_rows: Sequence[Mapping[str, Any]], *,
                           manifest: Mapping[str, Any]) -> dict[str, int]:
    """Validate exact 1,200 clean and 21,600 target+sentinel tuple rows."""

    tuples, seeds, cells, pols = _tuple_domains(manifest)
    _observed_row_seeds((*clean_rows, *controlled_rows), manifest)
    fixtures = tuple(manifest["fixtures"])
    clean_keys = [(
        row.get("record_type"), row.get("tuple_id"), row.get("seed"),
        row.get("cell_id"), row.get("polarization"),
    ) for row in clean_rows]
    expected_clean = {
        ("B2_TUPLE_CLEAN_DEV", tuple_id, seed, cell, pol)
        for tuple_id in tuples for seed in seeds for cell in cells for pol in pols
    }
    if len(clean_keys) != len(set(clean_keys)) or set(clean_keys) != expected_clean:
        raise FreezeError("clean tuple primary-key/cardinality mismatch")
    controlled_keys = [(
        row.get("record_type"), row.get("tuple_id"), row.get("seed"),
        row.get("cell_id"), row.get("target_polarization"),
        row.get("fixture_id"), row.get("row_polarization"),
    ) for row in controlled_rows]
    expected_controlled = {
        ("B2_TUPLE_CONTROLLED_DEV", tuple_id, seed, cell, target, fixture, row_pol)
        for tuple_id in tuples for seed in seeds for cell in cells
        for target in pols for fixture in fixtures for row_pol in pols
    }
    if (len(controlled_keys) != len(set(controlled_keys))
            or set(controlled_keys) != expected_controlled):
        raise FreezeError("controlled tuple primary-key/cardinality mismatch")
    target_count = sentinel_count = 0
    for row in controlled_rows:
        is_target = row.get("row_polarization") == row.get("target_polarization")
        expected_role = "TARGET_INCLUDED" if is_target else "SENTINEL_EXCLUDED"
        if row.get("row_role") != expected_role:
            raise FreezeError("controlled target/sentinel role mismatch")
        has_affected = "affected_cw_errors" in row or "affected_cw_total" in row
        if is_target:
            target_count += 1
            boundary = row.get("boundary_after_cw")
            if (not has_affected or type(row.get("affected_cw_errors")) is not int
                    or row.get("affected_cw_total") != 16 - boundary
                    or not 0 <= row["affected_cw_errors"] <= row["affected_cw_total"]):
                raise FreezeError("affected counts are required on target rows only")
        else:
            sentinel_count += 1
            if has_affected:
                raise FreezeError("affected counts are forbidden on sentinel rows")
    return {
        "clean": len(clean_rows), "controlled": len(controlled_rows),
        "controlled_target": target_count, "controlled_sentinel": sentinel_count,
    }


def b2_tuple_selection_key(item: B2TupleSelection) -> tuple[Fraction, Fraction,
                                                              Fraction, int, int]:
    return (-item.combined_macro_net_goodput, item.periodic_pilot_fraction,
            item.macro_controlled_target_affected_cwer, item.M, item.legal_order)


def _ratio_sum(rows: Sequence[Mapping[str, Any]], numerator: str,
               denominator: str) -> Fraction:
    top = sum(row[numerator] for row in rows)
    bottom = sum(row[denominator] for row in rows)
    if type(top) is not int or type(bottom) is not int or bottom <= 0:
        raise FreezeError("tuple objective requires positive exact integer ratios")
    return Fraction(top, bottom)


def select_b2_tuple(clean_rows: Sequence[Mapping[str, Any]],
                    controlled_rows: Sequence[Mapping[str, Any]], *,
                    manifest: Mapping[str, Any], bps_freeze: CommonBpsFreeze | None,
                    statistic_freeze: B2StatisticFreeze | None,
                    clean_raw_sha256: str,
                    controlled_raw_sha256: str) -> B2TupleFreeze:
    """Fit the final tuple after both per-tuple freezes already exist."""

    validate_b2_tuple_rows(clean_rows, controlled_rows, manifest=manifest)
    if type(bps_freeze) is not CommonBpsFreeze or type(statistic_freeze) is not B2StatisticFreeze:
        raise FreezeError("BPS and statistic freeze refs must preexist before tuple fit")
    clean_hash = _assert_sha256(clean_raw_sha256, "raw_b2_tuple_clean_dev_sha256")
    controlled_hash = _assert_sha256(
        controlled_raw_sha256, "raw_b2_tuple_controlled_dev_sha256")
    bps_ids = {item[0] for item in bps_freeze.by_tuple}
    statistic_ids = {item[0] for item in statistic_freeze.by_tuple}
    candidates = []
    for legal_order, layout in enumerate(manifest["tuples"]):
        tuple_id = layout["tuple_id"]
        if tuple_id not in bps_ids or tuple_id not in statistic_ids:
            raise FreezeError("per-tuple BPS/statistic freeze reference is missing")
        clean = [row for row in clean_rows if row["tuple_id"] == tuple_id]
        target = [row for row in controlled_rows
                  if row["tuple_id"] == tuple_id and row["row_role"] == "TARGET_INCLUDED"]
        for row in (*clean, *target):
            if (row.get("bps_freeze_ref") != f"bps:{tuple_id}"
                    or row.get("statistic_freeze_ref") != f"stat:{tuple_id}"):
                raise FreezeError("tuple row freeze refs do not bind the preexisting fit")
            successful = row.get("successful_cw_count")
            if (type(successful) is not int or row.get("delivered_information_bits") != 1024 * successful
                    or row.get("full_frame_cw_errors") != 16 - successful):
                raise FreezeError("tuple row CW goodput identity mismatch")
        clean_goodput = []
        target_goodput = []
        target_affected = []
        for cell in (item["cell_id"] for item in manifest["cells"]):
            clean_pol = []
            target_pol = []
            affected_pol = []
            for pol in manifest["polarizations"]:
                clean_group = [row for row in clean
                               if row["cell_id"] == cell and row["polarization"] == pol]
                target_group = [row for row in target
                                if row["cell_id"] == cell and row["target_polarization"] == pol]
                clean_pol.append(_ratio_sum(
                    clean_group, "delivered_information_bits",
                    "total_transmitted_symbols_per_polarization"))
                target_pol.append(_ratio_sum(
                    target_group, "delivered_information_bits",
                    "total_transmitted_symbols_per_polarization"))
                affected_pol.append(_ratio_sum(
                    target_group, "affected_cw_errors", "affected_cw_total"))
            clean_goodput.append(sum(clean_pol, Fraction()) / len(clean_pol))
            target_goodput.append(sum(target_pol, Fraction()) / len(target_pol))
            target_affected.append(sum(affected_pol, Fraction()) / len(affected_pol))
        macro_clean = sum(clean_goodput, Fraction()) / len(clean_goodput)
        macro_target = sum(target_goodput, Fraction()) / len(target_goodput)
        candidates.append(B2TupleSelection(
            tuple_id=tuple_id,
            combined_macro_net_goodput=(macro_clean + macro_target) / 2,
            periodic_pilot_fraction=Fraction(
                layout["periodic_pilot_count"], layout["total_symbols"]),
            macro_controlled_target_affected_cwer=(
                sum(target_affected, Fraction()) / len(target_affected)),
            M=layout["M"], legal_order=legal_order,
        ))
    frozen = tuple(candidates)
    return B2TupleFreeze(min(frozen, key=b2_tuple_selection_key), frozen,
                         clean_hash, controlled_hash)


def fit_b2_tuple(clean_rows: Sequence[Mapping[str, Any]],
                 controlled_rows: Sequence[Mapping[str, Any]], *,
                 manifest: Mapping[str, Any], bps_freeze: CommonBpsFreeze | None,
                 statistic_freeze: B2StatisticFreeze | None,
                 clean_raw_sha256: str,
                 controlled_raw_sha256: str) -> B2TupleFreeze:
    """Named fit boundary used by no-refit call-graph enforcement."""

    return select_b2_tuple(
        clean_rows,
        controlled_rows,
        manifest=manifest,
        bps_freeze=bps_freeze,
        statistic_freeze=statistic_freeze,
        clean_raw_sha256=clean_raw_sha256,
        controlled_raw_sha256=controlled_raw_sha256,
    )


def _fraction_document(value: Fraction) -> dict[str, Any]:
    return {"numerator_decimal": str(value.numerator), "denominator": value.denominator}


def _fraction_from_document(value: Any, label: str) -> Fraction:
    if (type(value) is not dict
            or set(value) != {"numerator_decimal", "denominator"}
            or type(value["numerator_decimal"]) is not str
            or type(value["denominator"]) is not int
            or value["denominator"] <= 0):
        raise FreezeError(f"{label} must be an exact rational document")
    try:
        numerator = int(value["numerator_decimal"])
    except ValueError as exc:
        raise FreezeError(f"{label} numerator must be a decimal integer") from exc
    result = Fraction(numerator, value["denominator"])
    if value != _fraction_document(result):
        raise FreezeError(f"{label} rational must be reduced and canonical")
    return result


def _validate_bps_candidate_document(value: Any, raw_sha256: str) -> tuple[Any, ...]:
    required = {
        "B", "Nw", "macro_net_goodput", "macro_full_frame_cwer",
        "exact_lexicographic_key", "raw_sha256",
    }
    if type(value) is not dict or set(value) != required:
        raise FreezeError("BPS candidate has non-exact fields")
    if value["B"] not in (32, 64) or value["Nw"] not in (31, 61, 127):
        raise FreezeError("BPS candidate is outside the owner grid")
    goodput = _fraction_from_document(value["macro_net_goodput"], "BPS goodput")
    cwer = _fraction_from_document(value["macro_full_frame_cwer"], "BPS CWER")
    expected = [_fraction_document(-goodput), _fraction_document(cwer),
                value["B"], value["Nw"]]
    if value["exact_lexicographic_key"] != expected:
        raise FreezeError("BPS candidate exact key mismatch")
    if value["raw_sha256"] != raw_sha256:
        raise FreezeError("BPS candidate raw hash binding mismatch")
    return (-goodput, cwer, value["B"], value["Nw"])


def _validate_hmm_candidate_document(value: Any, raw_sha256: str) -> tuple[Any, ...]:
    required = {
        "p_s_index", "sigma_e2_index", "objective", "exact_lexicographic_key",
        "receipted_primitive_scores", "objective_primitive_scores",
        "sentinel_primitive_scores", "raw_sha256",
    }
    if type(value) is not dict or set(value) != required:
        raise FreezeError("statistic candidate has non-exact fields")
    p_index = value["p_s_index"]
    sigma_index = value["sigma_e2_index"]
    if (type(p_index) is not int or not 0 <= p_index <= 121
            or type(sigma_index) is not int or not 0 <= sigma_index <= 5):
        raise FreezeError("statistic candidate is outside the owner grid")
    objective = _fraction_from_document(value["objective"], "statistic objective")
    expected = [_fraction_document(objective), p_index, sigma_index]
    if value["exact_lexicographic_key"] != expected:
        raise FreezeError("statistic candidate exact key mismatch")
    counts = (value["receipted_primitive_scores"],
              value["objective_primitive_scores"], value["sentinel_primitive_scores"])
    if (any(type(count) is not int or count < 0 for count in counts)
            or counts[0] != counts[1] + counts[2]):
        raise FreezeError("statistic candidate primitive counts mismatch")
    if value["raw_sha256"] != raw_sha256:
        raise FreezeError("statistic candidate raw hash binding mismatch")
    return (objective, p_index, sigma_index)


def _validate_tuple_candidate_document(value: Any, *, tuple_id: str,
                                       legal_order: int, clean_hash: str,
                                       controlled_hash: str) -> tuple[Any, ...]:
    required = {
        "tuple_id", "combined_macro_net_goodput", "periodic_pilot_fraction",
        "macro_controlled_target_affected_cwer", "M", "legal_order",
        "exact_lexicographic_key", "raw_sha256",
    }
    if type(value) is not dict or set(value) != required or value["tuple_id"] != tuple_id:
        raise FreezeError("tuple candidate identity/fields mismatch")
    M, _N, pilot_count, total_symbols = _TUPLE_LAYOUT[tuple_id]
    if value["M"] != M or value["legal_order"] != legal_order:
        raise FreezeError("tuple candidate owner order/M mismatch")
    goodput = _fraction_from_document(
        value["combined_macro_net_goodput"], "tuple goodput")
    pilot_fraction = _fraction_from_document(
        value["periodic_pilot_fraction"], "tuple pilot fraction")
    affected = _fraction_from_document(
        value["macro_controlled_target_affected_cwer"], "tuple affected CWER")
    if pilot_fraction != Fraction(pilot_count, total_symbols):
        raise FreezeError("tuple candidate pilot fraction mismatch")
    expected = [_fraction_document(-goodput), _fraction_document(pilot_fraction),
                _fraction_document(affected), M, legal_order]
    if value["exact_lexicographic_key"] != expected:
        raise FreezeError("tuple candidate exact key mismatch")
    raw = value["raw_sha256"]
    if (type(raw) is not dict or set(raw) != {"clean", "controlled"}
            or raw["clean"] != clean_hash or raw["controlled"] != controlled_hash):
        raise FreezeError("tuple candidate raw hash binding mismatch")
    return (-goodput, pilot_fraction, affected, M, legal_order)


def _validate_resolved_document_content(plain: dict[str, Any]) -> None:
    """Revalidate the fit outputs at the immutable load boundary."""

    raw = plain["raw_hashes"]
    tuple_ids = tuple(_TUPLE_LAYOUT)
    common = plain["common_bps"]
    statistics = plain["b2_statistics"]
    tuple_candidates = plain["b2_tuple_candidates"]
    if (type(common) is not list or type(statistics) is not list
            or type(tuple_candidates) is not list
            or len(common) != 5 or len(statistics) != 5 or len(tuple_candidates) != 5):
        raise FreezeError("dev freeze requires exactly five BPS, five statistic, and five tuple candidates")
    if ([item.get("tuple_id") if type(item) is dict else None for item in common] != list(tuple_ids)
            or [item.get("tuple_id") if type(item) is dict else None
                for item in statistics] != list(tuple_ids)):
        raise FreezeError("per-tuple freeze entries must follow the five unique owner tuples")
    for entry in common:
        if type(entry) is not dict or set(entry) != {"tuple_id", "winner", "candidates"}:
            raise FreezeError("BPS tuple freeze has non-exact fields")
        candidates = entry["candidates"]
        if type(candidates) is not list or len(candidates) != 6:
            raise FreezeError("BPS tuple freeze requires all six candidates")
        keys = [_validate_bps_candidate_document(
            candidate, raw["raw_bps_dev_sha256"]) for candidate in candidates]
        identities = [(candidate["B"], candidate["Nw"]) for candidate in candidates]
        if len(set(identities)) != 6 or set(identities) != {
                (B, Nw) for B in (32, 64) for Nw in (31, 61, 127)}:
            raise FreezeError("BPS candidate grid is incomplete or duplicated")
        if entry["winner"] not in candidates or keys[candidates.index(entry["winner"])] != min(keys):
            raise FreezeError("BPS winner is not bound to the exact candidate minimum")
    for entry in statistics:
        if type(entry) is not dict or set(entry) != {"tuple_id", "winner", "candidates"}:
            raise FreezeError("statistic tuple freeze has non-exact fields")
        candidates = entry["candidates"]
        if type(candidates) is not list or not candidates:
            raise FreezeError("statistic tuple freeze candidates may not be empty")
        keys = [_validate_hmm_candidate_document(
            candidate, raw["hmm_grid_dev_chunks_sha256"]) for candidate in candidates]
        identities = [(candidate["p_s_index"], candidate["sigma_e2_index"])
                      for candidate in candidates]
        if len(identities) != len(set(identities)):
            raise FreezeError("statistic candidate grid contains duplicates")
        if entry["winner"] not in candidates or keys[candidates.index(entry["winner"])] != min(keys):
            raise FreezeError("statistic winner is not bound to the exact candidate minimum")
    tuple_keys = []
    for legal_order, (tuple_id, candidate) in enumerate(zip(tuple_ids, tuple_candidates)):
        tuple_keys.append(_validate_tuple_candidate_document(
            candidate, tuple_id=tuple_id, legal_order=legal_order,
            clean_hash=raw["raw_b2_tuple_clean_dev_sha256"],
            controlled_hash=raw["raw_b2_tuple_controlled_dev_sha256"]))
    final = plain["final_b2_tuple"]
    if final not in tuple_candidates or tuple_keys[tuple_candidates.index(final)] != min(tuple_keys):
        raise FreezeError("final tuple is not bound to the exact five-candidate minimum")


def _bps_candidate_document(value: BpsSelection, raw_sha256: str) -> dict[str, Any]:
    return {
        "B": value.B, "Nw": value.Nw,
        "macro_net_goodput": _fraction_document(value.macro_net_goodput),
        "macro_full_frame_cwer": _fraction_document(value.macro_full_frame_cwer),
        "exact_lexicographic_key": [
            _fraction_document(-value.macro_net_goodput),
            _fraction_document(value.macro_full_frame_cwer), value.B, value.Nw,
        ],
        "raw_sha256": raw_sha256,
    }


def _hmm_candidate_document(value: HmmSelection, raw_sha256: str) -> dict[str, Any]:
    return {
        "p_s_index": value.p_s_index, "sigma_e2_index": value.sigma_e2_index,
        "objective": _fraction_document(value.objective),
        "exact_lexicographic_key": [
            _fraction_document(value.objective), value.p_s_index, value.sigma_e2_index,
        ],
        "receipted_primitive_scores": value.receipted_primitive_scores,
        "objective_primitive_scores": value.objective_primitive_scores,
        "sentinel_primitive_scores": value.sentinel_primitive_scores,
        "raw_sha256": raw_sha256,
    }


def _tuple_candidate_document(value: B2TupleSelection, clean_hash: str,
                              controlled_hash: str) -> dict[str, Any]:
    return {
        "tuple_id": value.tuple_id,
        "combined_macro_net_goodput": _fraction_document(value.combined_macro_net_goodput),
        "periodic_pilot_fraction": _fraction_document(value.periodic_pilot_fraction),
        "macro_controlled_target_affected_cwer": _fraction_document(
            value.macro_controlled_target_affected_cwer),
        "M": value.M, "legal_order": value.legal_order,
        "exact_lexicographic_key": [
            _fraction_document(-value.combined_macro_net_goodput),
            _fraction_document(value.periodic_pilot_fraction),
            _fraction_document(value.macro_controlled_target_affected_cwer),
            value.M, value.legal_order,
        ],
        "raw_sha256": {
            "clean": clean_hash, "controlled": controlled_hash,
        },
    }


def resolve_dev_freeze(bps_freeze: CommonBpsFreeze,
                       statistic_freeze: B2StatisticFreeze,
                       tuple_freeze: B2TupleFreeze, *,
                       owner_sha256: str) -> contract.ResolvedDevFreeze:
    """Resolve the immutable five-plus-five-plus-one development freeze."""

    if (type(bps_freeze) is not CommonBpsFreeze
            or type(statistic_freeze) is not B2StatisticFreeze
            or type(tuple_freeze) is not B2TupleFreeze):
        raise FreezeError("exact fitted freeze components are required")
    owner_hash = _assert_sha256(owner_sha256, "owner_sha256")
    if len(bps_freeze.by_tuple) != 5 or len(statistic_freeze.by_tuple) != 5:
        raise FreezeError("resolved freeze requires exactly five BPS and five statistic fits")
    common = [{
        "tuple_id": tuple_id,
        "winner": _bps_candidate_document(winner, bps_freeze.raw_sha256),
        "candidates": [_bps_candidate_document(value, bps_freeze.raw_sha256)
                       for value in candidates],
    } for tuple_id, winner, candidates in bps_freeze.by_tuple]
    statistics = [{
        "tuple_id": tuple_id,
        "winner": _hmm_candidate_document(winner, statistic_freeze.raw_sha256),
        "candidates": [_hmm_candidate_document(value, statistic_freeze.raw_sha256)
                       for value in candidates],
    } for tuple_id, winner, candidates in statistic_freeze.by_tuple]
    tuple_candidates = [
        _tuple_candidate_document(value, tuple_freeze.clean_raw_sha256,
                                  tuple_freeze.controlled_raw_sha256)
        for value in tuple_freeze.candidates
    ]
    if len(tuple_candidates) != 5:
        raise FreezeError("resolved freeze requires exactly five tuple candidates")
    document = {
        "schema": "coded_decoder_feedback.d0.dev_freeze.v1",
        "owner_sha256": owner_hash,
        "raw_hashes": {
            "raw_bps_dev_sha256": bps_freeze.raw_sha256,
            "hmm_grid_dev_chunks_sha256": statistic_freeze.raw_sha256,
            "raw_b2_tuple_clean_dev_sha256": tuple_freeze.clean_raw_sha256,
            "raw_b2_tuple_controlled_dev_sha256": tuple_freeze.controlled_raw_sha256,
        },
        "common_bps": common, "b2_statistics": statistics,
        "b2_tuple_candidates": tuple_candidates,
        "final_b2_tuple": _tuple_candidate_document(
            tuple_freeze.winner, tuple_freeze.clean_raw_sha256,
            tuple_freeze.controlled_raw_sha256),
        "test_rows_read": False,
    }
    return resolved_freeze_from_document(document)


def resolved_freeze_from_document(document: Mapping[str, Any]) -> contract.ResolvedDevFreeze:
    plain = _plain(document)
    required = {
        "schema", "owner_sha256", "raw_hashes", "common_bps", "b2_statistics",
        "b2_tuple_candidates", "final_b2_tuple", "test_rows_read",
    }
    if type(plain) is not dict or set(plain) != required:
        raise FreezeError("dev freeze document has non-exact fields")
    if (plain["schema"] != "coded_decoder_feedback.d0.dev_freeze.v1"
            or plain["test_rows_read"] is not False):
        raise FreezeError("dev freeze schema/chronology marker mismatch")
    owner_hash = _assert_sha256(plain["owner_sha256"], "owner_sha256")
    raw_hashes = plain["raw_hashes"]
    expected_raw = {
        "raw_bps_dev_sha256", "hmm_grid_dev_chunks_sha256",
        "raw_b2_tuple_clean_dev_sha256", "raw_b2_tuple_controlled_dev_sha256",
    }
    if type(raw_hashes) is not dict or set(raw_hashes) != expected_raw:
        raise FreezeError("dev freeze raw hash bindings are incomplete")
    for name, value in raw_hashes.items():
        _assert_sha256(value, name)
    _validate_resolved_document_content(plain)
    exact_bytes = artifacts.canonical_json_bytes(plain)
    # Normalize mapping insertion order to the canonical byte order before the
    # contract's tuple-backed immutable mapping captures it.
    plain = json.loads(exact_bytes.decode("utf-8"))
    raw_hashes = plain["raw_hashes"]
    digest = hashlib.sha256(exact_bytes).hexdigest()
    parameters = {
        "schema": plain["schema"], "owner_sha256": owner_hash,
        "common_bps": plain["common_bps"],
        "b2_statistics": plain["b2_statistics"],
        "b2_tuple_candidates": plain["b2_tuple_candidates"],
        "final_b2_tuple": plain["final_b2_tuple"],
        "test_rows_read": False,
    }
    receipts = {
        "owner_sha256": owner_hash, "raw_hashes": raw_hashes,
        "dev_freeze_sha256": digest,
    }
    return contract.ResolvedDevFreeze(digest, parameters, receipts)


def _document_from_resolved(resolved: contract.ResolvedDevFreeze) -> dict[str, Any]:
    if type(resolved) is not contract.ResolvedDevFreeze:
        raise FreezeError("exact ResolvedDevFreeze required")
    document = {
        "schema": resolved.parameters["schema"],
        "owner_sha256": resolved.parameters["owner_sha256"],
        "raw_hashes": resolved.receipts["raw_hashes"],
        "common_bps": resolved.parameters["common_bps"],
        "b2_statistics": resolved.parameters["b2_statistics"],
        "b2_tuple_candidates": resolved.parameters["b2_tuple_candidates"],
        "final_b2_tuple": resolved.parameters["final_b2_tuple"],
        "test_rows_read": resolved.parameters["test_rows_read"],
    }
    rebuilt = resolved_freeze_from_document(document)
    if rebuilt != resolved:
        raise FreezeError("resolved freeze does not match its canonical document")
    return document


def write_resolved_freeze(path: str | os.PathLike[str],
                          resolved: contract.ResolvedDevFreeze) -> str:
    """Write canonical bytes once; an existing freeze is immutable."""

    target = Path(path)
    document = _document_from_resolved(resolved)
    payload = artifacts.canonical_json_bytes(document)
    try:
        with target.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as exc:
        raise FreezeError("dev freeze path is immutable and already exists") from exc
    return resolved.freeze_id


def load_resolved_freeze(path: str | os.PathLike[str]) -> contract.ResolvedDevFreeze:
    payload = Path(path).read_bytes()
    try:
        document = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FreezeError("dev freeze is not canonical UTF-8 JSON") from exc
    if artifacts.canonical_json_bytes(document) != payload:
        raise FreezeError("dev freeze bytes are not canonical")
    return resolved_freeze_from_document(document)


def assert_phase_freeze_chronology(
        resolved: contract.ResolvedDevFreeze,
        phase_receipts: Sequence[Mapping[str, Any]]) -> str:
    """Require S1/S2/S3-dev/S3-test/S4 to bind the same frozen bytes."""

    if type(resolved) is not contract.ResolvedDevFreeze:
        raise FreezeError("exact ResolvedDevFreeze required")
    expected_phases = {"S1", "S2", "S3_DEV", "S3_TEST", "S4"}
    phases = [receipt.get("phase") for receipt in phase_receipts]
    if len(phases) != 5 or len(set(phases)) != 5 or set(phases) != expected_phases:
        raise FreezeError("exactly five phase receipts are required")
    hashes = {receipt.get("dev_freeze_sha256") for receipt in phase_receipts}
    if hashes != {resolved.freeze_id}:
        raise FreezeError("all phases must bind the same dev freeze SHA256")
    return resolved.freeze_id
