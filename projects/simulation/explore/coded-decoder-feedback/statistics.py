"""Pure D0 statistics kernels; no owner, artifact, or global-RNG access."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Sequence, TypeVar

import numpy as np

from schemas import (
    CANDIDATES, FIXTURES, POL, S2_METHODS, S1TrajectoryRow, S2MethodRow,
    S3CandidateRow, S3LambdaFreezeRow, SchemaError, row_from_mapping,
)


S3_LAMBDAS = (0.25, 0.5, 1.0, 2.0, 4.0)


@dataclass(frozen=True, slots=True)
class S1Point:
    event_count: int
    trajectory_count: int
    event_rate: float
    seed_count: int
    cell_count: int


@dataclass(frozen=True, slots=True)
class S2CellPoint:
    cell_id: str
    b1_on_errors: int
    b1_on_total: int
    b1_off_errors: int
    b1_off_total: int
    o1_on_errors: int
    o1_on_total: int
    b2_on_errors: int
    b2_on_total: int
    damage: float
    recoverability: float | None
    coverage: float | None


@dataclass(frozen=True, slots=True)
class S2Point:
    cells: tuple[S2CellPoint, ...]
    damage: float
    recoverability: float | None
    coverage: float | None
    terminals: tuple[str, ...]
    physical_off_computations: int


@dataclass(frozen=True, slots=True)
class BootstrapCI:
    lower: float | None
    upper: float | None
    valid_replicates: int
    invalid_replicates: int
    invalid_fraction: float
    terminal: str | None


@dataclass(frozen=True, slots=True)
class S3CasePoint:
    seed: int
    cell_id: str
    target_polarization: str
    fixture_id: str
    pilot_rank_truth: int
    fused_rank_truth: int
    pilot_rr: float
    fused_rr: float
    pilot_top1: float
    fused_top1: float
    paired_rr_delta: float
    changed_cw_decodes: int
    cached_unchanged_cw_nll_reads: int


@dataclass(frozen=True, slots=True)
class S3CellPoint:
    cell_id: str
    pilot_mrr: float
    fused_mrr: float
    pilot_top1: float
    fused_top1: float
    paired_rr_delta: float


@dataclass(frozen=True, slots=True)
class S3Point:
    cases: tuple[S3CasePoint, ...]
    cells: tuple[S3CellPoint, ...]
    pilot_mrr: float
    fused_mrr: float
    pilot_top1: float
    fused_top1: float
    paired_rr_delta: float
    case_count: int
    candidate_row_count: int
    bootstrap_seed_blocks: tuple[int, ...]


def _fail(message: str) -> None:
    raise SchemaError(f"statistics: {message}")


def reduce_s1(rows: Sequence[S1TrajectoryRow]) -> S1Point:
    rows = tuple(rows)
    if len(rows) not in (480, 1200):
        _fail("S1 requires exactly 480 or 1200 rows")
    if any(type(row) is not S1TrajectoryRow for row in rows):
        _fail("S1 requires exact typed rows")
    seeds = tuple(sorted({row.seed for row in rows}))
    cells = tuple(sorted({row.cell_id for row in rows}))
    polarizations = tuple(sorted({row.target_polarization for row in rows}))
    expected_seed_count = 20 if len(rows) == 480 else 50
    if len(seeds) != expected_seed_count or len(cells) != 12 or set(polarizations) != set(POL):
        _fail("S1 seed/cell/polarization domains mismatch")
    keys = [(row.seed, row.cell_id, row.target_polarization) for row in rows]
    expected = set(product(seeds, cells, POL))
    if len(set(keys)) != len(rows) or set(keys) != expected:
        _fail("S1 exact Cartesian coverage mismatch")
    for row in rows:
        if row.event_present != (row.persistent_transition_count > 0):
            _fail("S1 event/count mismatch")
        if len(row.persistent_transition_after_symbol) != row.persistent_transition_count:
            _fail("S1 transition array length mismatch")
    events = sum(row.event_present for row in rows)
    return S1Point(events, len(rows), events / len(rows), len(seeds), len(cells))


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        _fail("non-positive integer denominator")
    return numerator / denominator


def reduce_s2(rows: Sequence[S2MethodRow]) -> S2Point:
    rows = tuple(rows)
    if len(rows) != 2160 or any(type(row) is not S2MethodRow for row in rows):
        _fail("S2 requires exactly 2160 typed rows")
    seeds = tuple(sorted({row.seed for row in rows}))
    cells = tuple(sorted({row.cell_id for row in rows}))
    if len(seeds) != 10 or set(cells) != {"hard", "mid", "clean"}:
        _fail("S2 seed/cell domains mismatch")
    if {row.target_polarization for row in rows} != set(POL):
        _fail("S2 polarization domain mismatch")

    groups: dict[tuple[int, str, str], list[S2MethodRow]] = {}
    for row in rows:
        groups.setdefault((row.seed, row.cell_id, row.target_polarization), []).append(row)
    if set(groups) != set(product(seeds, cells, POL)):
        _fail("S2 exact seed/cell/polarization coverage mismatch")

    physical_off_ids: set[tuple[int, str, str, str]] = set()
    for key, group in groups.items():
        identities = [(r.fixture_id, r.jump_present, r.method_id) for r in group]
        expected = {
            *((fixture, True, method) for fixture in FIXTURES for method in S2_METHODS),
            *((fixture, False, S2_METHODS[0]) for fixture in FIXTURES),
        }
        if len(group) != 36 or len(set(identities)) != 36 or set(identities) != expected:
            _fail("S2 group requires nine fixtures with B1/B2/O1 on and B1 off")
        off = [row for row in group if not row.jump_present]
        owners = {(r.physical_case_id, r.computation_id, r.result_receipt_sha256) for r in off}
        if len(owners) != 1:
            _fail("S2 nine off projections must share physical/computation/content owner")
        physical_off_ids.add((*key, off[0].computation_id))

    cell_points = []
    for cell in ("hard", "mid", "clean"):
        cell_rows = [row for row in rows if row.cell_id == cell]
        selected: dict[str, list[S2MethodRow]] = {
            "b1_on": [r for r in cell_rows if r.jump_present and r.method_id == S2_METHODS[0]],
            "b1_off": [r for r in cell_rows if not r.jump_present],
            "b2_on": [r for r in cell_rows if r.jump_present and r.method_id == S2_METHODS[1]],
            "o1_on": [r for r in cell_rows if r.jump_present and r.method_id == S2_METHODS[2]],
        }
        sums = {
            name: (sum(r.affected_cw_errors for r in values),
                   sum(r.affected_cw_total for r in values))
            for name, values in selected.items()
        }
        b1e, b1t = sums["b1_on"]
        offe, offt = sums["b1_off"]
        b2e, b2t = sums["b2_on"]
        o1e, o1t = sums["o1_on"]
        damage = _ratio(b1e, b1t) - _ratio(offe, offt)
        recovery_denominator = b1e
        headroom = b1e - o1e
        recoverability = None if recovery_denominator <= 0 else headroom / recovery_denominator
        coverage = None if headroom <= 0 else (b1e - b2e) / headroom
        cell_points.append(S2CellPoint(
            cell, b1e, b1t, offe, offt, o1e, o1t, b2e, b2t,
            damage, recoverability, coverage,
        ))

    terminals = []
    if any(point.recoverability is None for point in cell_points):
        terminals.append("ZERO_PRACTICAL_CODED_DAMAGE")
    if any(point.coverage is None for point in cell_points):
        terminals.append("ZERO_RECOVERABLE_HEADROOM")
    recovery_values = [point.recoverability for point in cell_points]
    coverage_values = [point.coverage for point in cell_points]
    return S2Point(
        tuple(cell_points),
        sum(point.damage for point in cell_points) / 3,
        None if any(value is None for value in recovery_values) else sum(recovery_values) / 3,
        None if any(value is None for value in coverage_values) else sum(coverage_values) / 3,
        tuple(terminals), len(physical_off_ids),
    )


Block = TypeVar("Block")


def bootstrap_paired(
    blocks: Sequence[Block],
    reducer: Callable[[tuple[Block, ...]], float | None],
    *,
    seed: int = 2026081001,
    draws: int = 10000,
    invalid_terminal: str | None = None,
) -> BootstrapCI:
    blocks = tuple(blocks)
    if not blocks or type(seed) is not int or type(draws) is not int or draws <= 0:
        _fail("invalid bootstrap inputs")
    rng = np.random.Generator(np.random.PCG64(seed))
    valid = []
    invalid = 0
    for _ in range(draws):
        indices = rng.integers(0, len(blocks), size=len(blocks))
        value = reducer(tuple(blocks[int(index)] for index in indices))
        if value is None or isinstance(value, (bool, np.bool_)) or not np.isfinite(value):
            invalid += 1
        else:
            valid.append(float(value))
    valid_minimum = int(np.ceil(0.95 * draws))
    invalid_maximum = int(np.floor(0.05 * draws))
    unstable = invalid > invalid_maximum or len(valid) < valid_minimum
    terminal = (invalid_terminal or "UNSTABLE_BOOTSTRAP") if unstable else None
    if unstable:
        lower = upper = None
    else:
        lower, upper = (float(value) for value in np.percentile(
            np.asarray(valid, dtype=np.float64), (2.5, 97.5), method="linear"
        ))
    return BootstrapCI(lower, upper, len(valid), invalid, invalid / draws, terminal)


def _sha256(value: object) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def _validate_s3_rows(rows: Sequence[S3CandidateRow], record_type: str):
    rows = tuple(rows)
    if len(rows) != 5400 or any(type(row) is not S3CandidateRow for row in rows):
        _fail("S3 requires exactly 5400 typed candidate rows")
    if any(row.record_type != record_type for row in rows):
        _fail(f"S3 requires {record_type} rows only")
    seeds = tuple(sorted({row.seed for row in rows}))
    if len(seeds) != 10 or {row.cell_id for row in rows} != {"hard", "mid", "clean"}:
        _fail("S3 seed/cell domains mismatch")
    if {row.target_polarization for row in rows} != set(POL):
        _fail("S3 polarization domain mismatch")
    groups: dict[tuple[int, str, str, str], list[S3CandidateRow]] = {}
    computation_ids = []
    for row in rows:
        groups.setdefault((row.seed, row.cell_id, row.target_polarization,
                           row.fixture_id), []).append(row)
        computation_ids.append(row.computation_id)
    expected_keys = set(product(seeds, ("hard", "mid", "clean"), POL, FIXTURES))
    if set(groups) != expected_keys or len(groups) != 540:
        _fail("S3 exact case coverage mismatch")
    if len(set(computation_ids)) != len(computation_ids):
        _fail("S3 computation may not be shared across candidates or cases")
    expected_changed = tuple(16 - (0 if candidate == "NOOP" else int(candidate[1:3]))
                             for candidate in CANDIDATES)
    expected_cached = tuple(16 - changed for changed in expected_changed)
    for group in groups.values():
        by_candidate = {row.candidate_id: row for row in group}
        if len(group) != 10 or len(by_candidate) != 10 or tuple(
                candidate for candidate in CANDIDATES if candidate in by_candidate
        ) != CANDIDATES:
            _fail("S3 case requires exact ten candidates")
        truth = {row.truth_candidate_id for row in group}
        if (len(truth) != 1 or next(iter(truth)) not in by_candidate
                or any(row.truth_candidate_id != row.fixture_id for row in group)):
            _fail("S3 truth candidate is not uniquely present in case")
        if any(not np.isfinite(row.pilot_score) or not np.isfinite(row.decoder_score)
               for row in group):
            _fail("S3 scores must be finite")
        changed = tuple(by_candidate[candidate].changed_cw_decodes for candidate in CANDIDATES)
        cached = tuple(by_candidate[candidate].cached_unchanged_cw_nll_reads
                       for candidate in CANDIDATES)
        if changed != expected_changed or cached != expected_cached:
            _fail("S3 exact changed-CW/cache vector mismatch")
        if sum(changed) != 88 or sum(cached) != 72:
            _fail("S3 exact per-case cost totals mismatch")
    return rows, seeds, groups


def _rank(group: Sequence[S3CandidateRow], score: Callable[[S3CandidateRow], float]) -> int:
    order = {candidate: index for index, candidate in enumerate(CANDIDATES)}
    ranked = sorted(group, key=lambda row: (-score(row), order[row.candidate_id]))
    truth = group[0].truth_candidate_id
    return next(index for index, row in enumerate(ranked, 1) if row.candidate_id == truth)


def _reduce_s3(rows: Sequence[S3CandidateRow], lambda_frozen: float,
               record_type: str) -> S3Point:
    rows, seeds, groups = _validate_s3_rows(rows, record_type)
    cases = []
    for key in product(seeds, ("hard", "mid", "clean"), POL, FIXTURES):
        group = groups[key]
        pilot_rank = _rank(group, lambda row: row.pilot_score)
        fused_rank = _rank(
            group, lambda row: row.pilot_score + lambda_frozen * row.decoder_score,
        )
        pilot_rr = 1.0 / pilot_rank
        fused_rr = 1.0 / fused_rank
        cases.append(S3CasePoint(
            *key, pilot_rank, fused_rank, pilot_rr, fused_rr,
            float(pilot_rank == 1), float(fused_rank == 1), fused_rr - pilot_rr,
            sum(row.changed_cw_decodes for row in group),
            sum(row.cached_unchanged_cw_nll_reads for row in group),
        ))
    cell_points = []
    for cell in ("hard", "mid", "clean"):
        selected = [case for case in cases if case.cell_id == cell]
        mean = lambda field: sum(getattr(case, field) for case in selected) / len(selected)
        cell_points.append(S3CellPoint(
            cell, mean("pilot_rr"), mean("fused_rr"), mean("pilot_top1"),
            mean("fused_top1"), mean("paired_rr_delta"),
        ))
    macro = lambda field: sum(getattr(cell, field) for cell in cell_points) / 3
    return S3Point(
        tuple(cases), tuple(cell_points), macro("pilot_mrr"), macro("fused_mrr"),
        macro("pilot_top1"), macro("fused_top1"), macro("paired_rr_delta"),
        len(cases), len(rows), seeds,
    )


def select_s3_lambda(
    dev_rows: Sequence[S3CandidateRow], *, dev_rows_sha256: str,
    freeze_receipt_sha256: str,
) -> S3LambdaFreezeRow:
    if not _sha256(dev_rows_sha256) or not _sha256(freeze_receipt_sha256):
        _fail("S3 freeze hashes must be canonical SHA256")
    scored = [(_reduce_s3(dev_rows, value, "S3_CANDIDATE_DEV"), value)
              for value in S3_LAMBDAS]
    _, selected = max(scored, key=lambda item: (
        item[0].fused_mrr, item[0].fused_top1, -item[1],
    ))
    return row_from_mapping("s3_lambda_freeze", {
        "record_type": "S3_LAMBDA_FREEZE", "lambda_frozen": selected,
        "dev_rows_sha256": dev_rows_sha256,
        "objective": "macro_MRR_then_macro_top1_then_smaller_lambda",
        "test_rows_read_during_selection": False,
        "freeze_receipt_sha256": freeze_receipt_sha256,
    })


def reduce_s3(test_rows: Sequence[S3CandidateRow], freeze: S3LambdaFreezeRow) -> S3Point:
    if type(freeze) is not S3LambdaFreezeRow:
        _fail("S3 requires exact typed lambda freeze")
    if (freeze.record_type != "S3_LAMBDA_FREEZE"
            or freeze.lambda_frozen not in S3_LAMBDAS
            or freeze.objective != "macro_MRR_then_macro_top1_then_smaller_lambda"
            or freeze.test_rows_read_during_selection is not False
            or not _sha256(freeze.dev_rows_sha256)
            or not _sha256(freeze.freeze_receipt_sha256)):
        _fail("S3 lambda freeze is invalid")
    return _reduce_s3(test_rows, freeze.lambda_frozen, "S3_CANDIDATE_TEST")


__all__ = [
    "S1Point", "S2CellPoint", "S2Point", "BootstrapCI", "S3CasePoint",
    "S3CellPoint", "S3Point", "reduce_s1", "reduce_s2", "bootstrap_paired",
    "select_s3_lambda", "reduce_s3",
]
