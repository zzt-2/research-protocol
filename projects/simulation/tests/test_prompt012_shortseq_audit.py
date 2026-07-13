"""PROMPT-012 N=2M short-sequence audit tests."""
from pathlib import Path
import json
import sys


EXPLORE_DIR = Path(__file__).resolve().parents[1] / "explore" / "cma-fade-divergence"
sys.path.insert(0, str(EXPLORE_DIR))

from prompt012_shortseq_audit import (  # noqa: E402
    DEFAULT_F_G,
    DEFAULT_SEEDS,
    build_contract,
    evaluation_slices,
    filter_shortseq_trials,
    pending_cells,
    save_shortseq_results,
    summarize_grid,
    validate_shortseq_checkpoint,
)


def test_evaluation_slices_save_full_test_and_test_late():
    assert evaluation_slices(2_000_000) == {
        "test_full": (1_000_000, 2_000_000),
        "test_late": (1_750_000, 2_000_000),
    }


def test_pending_cells_skips_checkpointed_fg_seed_pairs():
    checkpoint = {"trials": [{"f_G": 30.0, "seed": 1000}]}
    cells = pending_cells((30.0, 100.0), (1000, 1001), checkpoint)
    assert cells == [(30.0, 1001), (100.0, 1000), (100.0, 1001)]


def test_grid_defaults_match_prompt012_contract():
    assert DEFAULT_F_G == (30.0, 100.0, 1000.0)
    assert DEFAULT_SEEDS == tuple(range(1000, 1010))


def test_contract_freezes_symbol_period_in_parameters_and_signature():
    parameters, signature = build_contract(
        alpha=1.5, beta=0.8, slices=evaluation_slices(2_000_000),
        f_g_values=DEFAULT_F_G, seeds=DEFAULT_SEEDS,
    )
    assert parameters["T_S"] == 4e-10
    assert signature["T_S"] == 4e-10


def test_summary_is_nested_by_fg_window_and_method():
    metric = lambda value: {"fixed_label_ber": {"mean": value},
                            "permutation_invariant_ber": {"mean": value / 2},
                            "classification": "normal", "diverged": False}
    trials = [
        {"f_G": 30.0, "windows": {"test_full": {"methods": {"ml": metric(0.2)}}}},
        {"f_G": 30.0, "windows": {"test_full": {"methods": {"ml": metric(0.4)}}}},
    ]
    summary = summarize_grid(trials, methods=("ml",))
    assert summary["30"]["test_full"]["ml"]["fixed_label_ber"] == {
        "mean": 0.30000000000000004, "std": 0.1, "values": [0.2, 0.4]
    }


def test_shortseq_saver_injects_metadata(tmp_path):
    output = tmp_path / "shortseq.json"
    save_shortseq_results({"trials": []}, output)
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["_meta"]["script"] == "prompt012_shortseq_audit"
    assert saved["_meta"]["git_commit"]
    assert len(saved["script_sha256"]) == 64


def test_shortseq_checkpoint_rejects_grid_mismatch():
    checkpoint = {"experiment_signature": {"f_G": [30.0]}, "script_sha256": "old"}
    requested = {"f_G": [100.0]}
    import pytest
    with pytest.raises(ValueError):
        validate_shortseq_checkpoint(checkpoint, requested, "new")


def test_shortseq_filter_deduplicates_and_removes_unrequested_cells():
    trials = [{"f_G": 30.0, "seed": 1000}, {"f_G": 30.0, "seed": 1000},
              {"f_G": 100.0, "seed": 1000}]
    assert filter_shortseq_trials(trials, {(30.0, 1000)}) == [trials[0]]
