"""Deterministic CandidateMap score and ordering validation.

Scores are compared with an explicit absolute tolerance. Ranking uses the
unrounded weighted sum and Python's stable sort, so equal scores retain their
original shortlist order.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


DEFAULT_TOLERANCE = 1e-9


class ValidationReport:
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors

    @property
    def passed(self) -> bool:
        return not self.errors


def load_map(path: str | Path) -> dict[str, Any]:
    """Load a CandidateMap YAML document as UTF-8."""
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("candidate map root must be a mapping")
    return data


def _compute_decimal_score(
    candidate: Mapping[str, Any], weights: Mapping[str, Any]
) -> Decimal:
    factors = candidate.get("factors")
    if not isinstance(factors, Mapping):
        raise ValueError(f"candidate {candidate.get('id', '<missing>')} has no factors mapping")
    missing = [name for name in weights if name not in factors]
    extra = [name for name in factors if name not in weights]
    if missing or extra:
        raise ValueError(
            f"factor keys differ from weights: missing={missing or []}, extra={extra or []}"
        )
    return sum(
        (Decimal(str(factors[name])) * Decimal(str(weight)) for name, weight in weights.items()),
        Decimal("0"),
    )


def compute_score(candidate: Mapping[str, Any], weights: Mapping[str, Any]) -> float:
    """Return the exact-decimal factors x declared-weights sum as a float."""
    return float(_compute_decimal_score(candidate, weights))


def _duplicate_errors(ids: Sequence[str], label: str) -> list[str]:
    return [f"duplicate {label} ID: {candidate_id}" for candidate_id, count in Counter(ids).items() if count > 1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_universe_binding(
    data: Mapping[str, Any], map_path: Path | None, family_ids: list[str], partition_ids: set[str]
) -> list[str]:
    lineage = data.get("lineage")
    if not isinstance(lineage, Mapping) or "candidate_universe_file" not in lineage:
        return []
    if map_path is None:
        return ["map_path is required to validate candidate universe binding"]

    errors: list[str] = []
    v1_file = lineage.get("v1_file")
    v1_sha = lineage.get("v1_file_sha256")
    if v1_file and v1_sha:
        v1_path = map_path.parent / str(v1_file)
        if not v1_path.is_file():
            errors.append(f"v1 source file not found: {v1_path}")
        else:
            actual_v1_sha = _sha256(v1_path)
            if str(v1_sha) != actual_v1_sha:
                errors.append(
                    "v1 file SHA mismatch: "
                    f"recorded={v1_sha}, actual={actual_v1_sha}"
                )
    universe_path = map_path.parent / str(lineage["candidate_universe_file"])
    if not universe_path.is_file():
        return [f"candidate universe file not found: {universe_path}"]
    actual_universe_sha = _sha256(universe_path)
    if lineage.get("candidate_universe_file_sha256") != actual_universe_sha:
        errors.append(
            "candidate universe SHA mismatch: "
            f"recorded={lineage.get('candidate_universe_file_sha256')}, actual={actual_universe_sha}"
        )
    universe = load_map(universe_path)
    if data.get("universe_id") != universe.get("universe_id"):
        errors.append(
            f"candidate universe ID mismatch: map={data.get('universe_id')}, "
            f"universe={universe.get('universe_id')}"
        )

    universe_lineage = universe.get("lineage")
    if not isinstance(universe_lineage, Mapping):
        errors.append("candidate universe lineage must be a mapping")
        return errors
    base_name = str(universe_lineage.get("base_file", ""))
    base_path = universe_path.parent / base_name
    if lineage.get("candidate_universe_base_file") != base_name:
        errors.append("candidate universe base file mismatch")
    if not base_path.is_file():
        errors.append(f"candidate universe base file not found: {base_path}")
        return errors
    actual_base_sha = _sha256(base_path)
    declared_base_sha = universe_lineage.get("base_file_sha256")
    if declared_base_sha != actual_base_sha or lineage.get("candidate_universe_base_file_sha256") != actual_base_sha:
        errors.append(
            "candidate universe base SHA mismatch: "
            f"map={lineage.get('candidate_universe_base_file_sha256')}, "
            f"universe={declared_base_sha}, actual={actual_base_sha}"
        )

    base = load_map(base_path)
    base_candidates = base.get("candidate_archetypes", [])
    added_candidates = universe.get("candidate_archetypes_added", [])
    expected_ids = {
        str(candidate.get("id"))
        for candidate in [*base_candidates, *added_candidates]
        if isinstance(candidate, Mapping) and candidate.get("id") is not None
    }
    family_set = set(family_ids)
    if family_set != expected_ids:
        errors.append(
            "universe coverage mismatch in families: "
            f"missing={sorted(expected_ids - family_set)}, extra={sorted(family_set - expected_ids)}"
        )
    if partition_ids != expected_ids:
        errors.append(
            "universe coverage mismatch in shortlist/retained: "
            f"missing={sorted(expected_ids - partition_ids)}, extra={sorted(partition_ids - expected_ids)}"
        )
    return errors


def validate_map(
    data: Mapping[str, Any], *, tolerance: float = DEFAULT_TOLERANCE, map_path: str | Path | None = None
) -> ValidationReport:
    """Validate score semantics, deterministic order, partition, and universe binding."""
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    weights = data.get("weights")
    shortlist = data.get("ranked_shortlist")
    if not isinstance(weights, Mapping):
        return ValidationReport(["weights must be a mapping"])
    if not isinstance(shortlist, list):
        return ValidationReport(["ranked_shortlist must be a list"])

    errors: list[str] = []
    try:
        weight_total = sum((Decimal(str(value)) for value in weights.values()), Decimal("0"))
        if abs(weight_total - Decimal("1")) > Decimal(str(tolerance)):
            errors.append(f"weights must sum to 1: actual={weight_total}")
    except (ArithmeticError, ValueError):
        errors.append("weights must contain finite numeric values")

    shortlist_ids = [str(candidate.get("id", "<missing>")) for candidate in shortlist]
    errors.extend(_duplicate_errors(shortlist_ids, "candidate"))
    families = data.get("families", [])
    family_ids = [
        str(candidate_id)
        for family in families
        if isinstance(family, Mapping)
        for candidate_id in family.get("members", [])
    ]
    errors.extend(_duplicate_errors(family_ids, "family member"))
    retained_section = data.get("unranked_but_retained", {})
    retained_ids = (
        [str(candidate_id) for candidate_id in retained_section.get("ids", [])]
        if isinstance(retained_section, Mapping)
        else []
    )
    errors.extend(_duplicate_errors(retained_ids, "retained candidate"))
    overlap = set(shortlist_ids) & set(retained_ids)
    if overlap:
        errors.append(f"shortlist/retained overlap: {sorted(overlap)}")
    partition_ids = set(shortlist_ids) | set(retained_ids)
    if set(family_ids) != partition_ids:
        errors.append(
            "family/shortlist/retained coverage mismatch: "
            f"family_only={sorted(set(family_ids) - partition_ids)}, "
            f"partition_only={sorted(partition_ids - set(family_ids))}"
        )
    errors.extend(
        _validate_universe_binding(
            data, Path(map_path) if map_path is not None else None, family_ids, partition_ids
        )
    )

    computed: list[Decimal] = []
    decimal_tolerance = Decimal(str(tolerance))
    for candidate in shortlist:
        candidate_id = str(candidate.get("id", "<missing>"))
        factors = candidate.get("factors", {})
        if isinstance(factors, Mapping):
            for factor_name, factor_value in factors.items():
                try:
                    numeric_value = Decimal(str(factor_value))
                    if not Decimal("1") <= numeric_value <= Decimal("5"):
                        errors.append(
                            f"factor out of range for {candidate_id}.{factor_name}: {factor_value}"
                        )
                except (ArithmeticError, ValueError):
                    errors.append(
                        f"factor out of range for {candidate_id}.{factor_name}: {factor_value}"
                    )
        try:
            expected = _compute_decimal_score(candidate, weights)
            recorded = Decimal(str(candidate["score"]))
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"invalid candidate {candidate_id}: {exc}")
            computed.append(Decimal("-Infinity"))
            continue
        computed.append(expected)
        if abs(recorded - expected) > decimal_tolerance:
            errors.append(
                f"score mismatch for {candidate_id}: "
                f"recorded={recorded:.2f}, recomputed={expected:.2f}, "
                f"tolerance={tolerance:g}"
            )

    actual_ids = shortlist_ids
    reference_rank = {candidate_id: index for index, candidate_id in enumerate(actual_ids)}
    tie_break_label = "current shortlist"
    if map_path is not None and isinstance(data.get("lineage"), Mapping):
        v1_file = data["lineage"].get("v1_file")
        if v1_file:
            v1_path = Path(map_path).parent / str(v1_file)
            if v1_path.is_file():
                v1_shortlist = load_map(v1_path).get("ranked_shortlist", [])
                reference_rank = {
                    str(candidate.get("id")): index
                    for index, candidate in enumerate(v1_shortlist)
                    if isinstance(candidate, Mapping)
                }
                tie_break_label = "v1 shortlist"
    expected_indices = sorted(
        range(len(shortlist)),
        key=lambda index: (
            -computed[index],
            reference_rank.get(actual_ids[index], len(reference_rank)),
            actual_ids[index],
        ),
    )
    expected_ids = [actual_ids[index] for index in expected_indices]
    if actual_ids != expected_ids:
        errors.append(
            f"ordering mismatch: ranking must use unrounded score and {tie_break_label} "
            f"tie-break; actual={actual_ids}, expected={expected_ids}"
        )
    return ValidationReport(errors)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_path", type=Path)
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = validate_map(load_map(args.map_path), tolerance=args.tolerance, map_path=args.map_path)
    if report.passed:
        print(f"PASS: {args.map_path}")
        return 0
    print(f"FAIL: {args.map_path}")
    for error in report.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
