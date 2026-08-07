from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "recompute_ccisp_single_branch_evidence.py"
SOURCE_COMMIT = "67970307a051dd8149e1a750498a20674dfcfe6f"


def _load_tool():
    assert TOOL.exists(), "deterministic CCISP evidence recompute tool is missing"
    spec = importlib.util.spec_from_file_location("ccisp_single_branch_recompute", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recomputes_historical_single_branch_evidence_from_raw_git_objects():
    module = _load_tool()

    result = module.recompute_from_commit(ROOT, SOURCE_COMMIT)

    assert result["scope"] == {
        "cells": 990,
        "performance_shards": 990,
        "timing_shards": 990,
        "windows_per_cell": 400,
        "total_windows": 396_000,
        "seed_clusters": 30,
    }
    assert result["identity"]["command_mismatches"] == 0
    assert result["identity"]["selected_output_mismatches"] == 0
    assert result["identity"]["command_hash_mismatched_shards"] == 0
    assert result["identity"]["selected_output_hash_mismatched_shards"] == 0
    assert result["identity"]["ber_count_mismatched_cells"] == 0
    assert result["identity"]["performance_timing_receipt_mismatched_cells"] == 0
    assert result["identity"]["ber_equal"] is True
    assert result["identity"]["A-F"] == result["identity"]["B-F"]
    assert result["timing"]["bf_over_af_cluster_mean"] == pytest.approx(
        0.5424435601792953, abs=1e-12
    )
    assert result["timing"]["bf_over_af_one_sided95_upper"] == pytest.approx(
        0.5472819331515957, abs=1e-12
    )
    assert result["branch_calls"]["A-F"] == {"da": 396_000, "nda": 396_000}
    assert result["branch_calls"]["B-F"] == {"da": 144_286, "nda": 251_714}
    assert result["operations"]["A-F"]["complex_multiply"] == 1_140_480_000
    assert result["operations"]["B-F"]["complex_multiply"] == 690_559_360
    assert result["timing_contract"]["contended_samples"] == 0
    assert result["timing_contract"]["affinity_values"] == [[2]]
    assert result["timing_contract"]["warmups_per_method_values"] == [3]
    assert result["timing_contract"]["measured_repetitions_values"] == [5]
    assert result["timing_contract"]["post_timing_cpu_load_ge_60_count"] == 3
    assert result["timing_contract"]["post_timing_load_is_non_gating"] is True


import pytest
