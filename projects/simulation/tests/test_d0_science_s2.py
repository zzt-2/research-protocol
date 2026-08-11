import dataclasses
import importlib
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest


TEST_ROOT = Path(__file__).resolve().parent
D0_ROOT = TEST_ROOT.parent / "explore" / "coded-decoder-feedback"
for path in (TEST_ROOT, D0_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def _inputs():
    fixtures = importlib.import_module("test_d0_schemas_statistics")
    schemas = importlib.import_module("schemas")
    full = fixtures._s2_rows()
    narrow = tuple(row for row in full if row.method_id != schemas.S2_METHODS[1])
    return schemas, full, narrow


def test_damage_headroom_reducer_is_exactly_equivalent_to_full_reducer():
    statistics = importlib.import_module("statistics")
    _, full, narrow = _inputs()
    assert len(full) == 2160 and len(narrow) == 1620
    expected = statistics.reduce_s2(full)
    observed = statistics.reduce_s2_damage_headroom(narrow)
    assert observed.damage == expected.damage
    assert observed.recoverability == expected.recoverability
    assert observed.cells == tuple(
        (p.cell_id, p.b1_on_errors, p.b1_on_total, p.b1_off_errors,
         p.b1_off_total, p.o1_on_errors, p.o1_on_total, p.damage, p.recoverability)
        for p in expected.cells
    )
    assert observed.physical_off_computations == expected.physical_off_computations


def test_damage_headroom_reducer_rejects_b2_missing_duplicate_and_extra():
    statistics = importlib.import_module("statistics")
    schemas, full, narrow = _inputs()
    b2 = next(row for row in full if row.method_id == schemas.S2_METHODS[1])
    for bad in ((b2, *narrow), narrow[:-1], (*narrow, narrow[0]), (*narrow, dataclasses.replace(narrow[0], seed=9999))):
        with pytest.raises(schemas.SchemaError):
            statistics.reduce_s2_damage_headroom(bad)


def test_s2_plan_is_exact_60_clusters_and_nine_fixtures():
    science = importlib.import_module("science")
    owner = science.load_science_contract(science.DEFAULT_CONTRACT_PATH)
    plan = science.s2_plan(owner)
    assert len(plan) == 60
    assert {seed for seed, _, _ in plan} == set(range(8150, 8160))
    assert {cell for _, cell, _ in plan} == {"hard", "mid", "clean"}
    assert {pol for _, _, pol in plan} == {"X", "Y"}
    assert science.S2_FIXTURES == (
        ("B04_K1", 4, 1), ("B04_K2", 4, 2), ("B04_K3", 4, 3),
        ("B08_K1", 8, 1), ("B08_K2", 8, 2), ("B08_K3", 8, 3),
        ("B12_K1", 12, 1), ("B12_K2", 12, 2), ("B12_K3", 12, 3),
    )


def test_science_binds_local_d0_verify_module_not_simulation_verify_package():
    science = importlib.import_module("science")
    assert hasattr(science.verify, "DeploymentBoundary")
    assert Path(science.verify.__file__).parent == D0_ROOT


@pytest.mark.parametrize(("boundary", "affected_total"), ((4, 12), (8, 8), (12, 4)))
def test_s2_row_counts_affected_codewords_with_any_error(boundary, affected_total):
    science = importlib.import_module("science")
    truth = np.zeros((16, 1024), dtype=np.uint8)
    decoded = truth.copy()
    decoded[boundary - 1, 0] = 1
    decoded[boundary, 0:2] = 1
    decoded[15, 0] = 1

    row = science._s2_row(
        seed=8150,
        alias="hard",
        pol="X",
        fixture_id=f"B{boundary:02d}_K1",
        boundary=boundary,
        rotation=1,
        jump=True,
        method_id="B1",
        decoded=SimpleNamespace(info_bits=decoded),
        truth_bits=truth,
        physical_case_id="case",
        computation_id="computation",
        total_symbols=6200,
    )

    assert row["affected_cw_errors"] == 2
    assert row["affected_cw_total"] == affected_total
    assert row["information_bit_errors"] == 4


def test_s2_raw_artifact_sort_key_uses_supported_scalars_and_is_total(tmp_path):
    science = importlib.import_module("science")
    artifact_module = importlib.import_module("artifacts")
    base = {
        "record_type": "S2_METHOD",
        "seed": 8150,
        "cell_id": "hard",
        "target_polarization": "X",
        "fixture_id": "B04_K1",
        "method_id": "B1",
    }
    rows = (
        dict(base, projection_role="DIRECT_ON", physical_case_id="on", computation_id="on-B1"),
        dict(base, projection_role="CACHED_OFF_PROJECTION", physical_case_id="off", computation_id="off"),
    )

    artifact_module.write_jsonl_atomic(
        tmp_path / "s2-raw.jsonl",
        rows,
        sort_key=science._S2_ARTIFACT_SORT_KEY,
        logical_name="s2-raw.jsonl",
    )

    assert len((tmp_path / "s2-raw.jsonl").read_text(encoding="utf-8").splitlines()) == 2
