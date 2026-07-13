"""PROMPT-012 long-sequence dual-metric audit tests."""
from pathlib import Path
import json
import sys

import numpy as np


EXPLORE_DIR = Path(__file__).resolve().parents[1] / "explore" / "cma-fade-divergence"
sys.path.insert(0, str(EXPLORE_DIR))

from prompt012_longseq_audit import (  # noqa: E402
    build_contract,
    classify_failure,
    filter_trials,
    evaluate_outputs,
    ml_diverged,
    pending_seeds,
    seed_ml,
    script_sha256,
    validate_checkpoint,
    save_audit_results,
    seed_fields,
    summarize_trials,
    test_late_slice as compute_test_late_slice,
)


def _qpsk(n=256, seed=0):
    rng = np.random.default_rng(seed)
    return (
        (2 * rng.integers(0, 2, n) - 1)
        + 1j * (2 * rng.integers(0, 2, n) - 1)
    ) / np.sqrt(2)


def test_test_late_is_last_quarter_of_test_half():
    assert compute_test_late_slice(5_000_000) == (4_375_000, 5_000_000)


def test_long_contract_freezes_symbol_period_in_parameters_and_signature():
    parameters, signature = build_contract(
        alpha=1.5, beta=0.8, late_slice=(4_375_000, 5_000_000),
        seeds=tuple(range(1000, 1010)),
    )
    assert parameters["T_S"] == 4e-10
    assert signature["T_S"] == 4e-10


def test_long_source_hash_changes_when_helper_bytes_change():
    first = script_sha256(script_bytes=b"script", helper_bytes=b"helper-v1")
    second = script_sha256(script_bytes=b"script", helper_bytes=b"helper-v2")
    assert first != second


def test_pi_ber_searches_both_permutations_and_both_qpsk_phases():
    sx, sy = _qpsk(seed=1), _qpsk(seed=2)
    metrics = evaluate_outputs(1j * sy, -sx, sx, sy, diverged=False)

    assert metrics["fixed_label_ber"]["mean"] > 0.4
    assert metrics["permutation_invariant_ber"]["mean"] == 0.0
    assert metrics["permutation_invariant_ber"]["assignment"] == ["sY", "sX"]
    assert metrics["classification"] == "clean-swap"
    assert set(metrics["abs_corr"]) == {"zX_sX", "zX_sY", "zY_sX", "zY_sY"}


def test_classification_precedence_and_thresholds():
    assert classify_failure([[1, 0], [0, 1]], diverged=True) == "diverged"
    assert classify_failure([[0.8, 0.1], [0.7, 0.2]], diverged=False) == "same-source"
    assert classify_failure([[0.8, 0.1], [0.1, 0.9]], diverged=False) == "normal"
    assert classify_failure([[0.1, 0.8], [0.9, 0.1]], diverged=False,
                            fixed_ber=0.5, pi_ber=0.01) == "clean-swap"
    assert classify_failure([[0.1, 0.8], [0.9, 0.1]], diverged=False,
                            fixed_ber=0.5, pi_ber=0.10) == "degraded-swap"
    assert classify_failure([[0.3, 0.4], [0.2, 0.49]], diverged=False) == "non-swap-collapse"
    assert classify_failure([[0.6, 0.55], [0.2, 0.3]], diverged=False) == "mixed"
    assert classify_failure([[0.49, 0.51], [0.51, 0.49]], diverged=False,
                            fixed_ber=0.5, pi_ber=0.01) == "mixed"
    assert classify_failure([[0.1, 0.8], [0.9, 0.1]], diverged=False,
                            fixed_ber=0.25, pi_ber=0.24) == "mixed"


def test_summary_reports_mean_std_values_and_type_fractions():
    trials = [
        {"methods": {"ml": {"fixed_label_ber": {"mean": 0.5},
                              "permutation_invariant_ber": {"mean": 0.1},
                              "classification": "clean-swap", "diverged": False}}},
        {"methods": {"ml": {"fixed_label_ber": {"mean": 0.3},
                              "permutation_invariant_ber": {"mean": 0.2},
                              "classification": "mixed", "diverged": False}}},
    ]
    summary = summarize_trials(trials, ("ml",))["ml"]

    assert summary["fixed_label_ber"] == {"mean": 0.4, "std": 0.1, "values": [0.5, 0.3]}
    assert summary["permutation_invariant_ber"] == {
        "mean": 0.15000000000000002, "std": 0.05, "values": [0.1, 0.2]
    }
    assert summary["classification_fraction"]["clean-swap"] == 0.5
    assert summary["classification_fraction"]["mixed"] == 0.5


def test_result_saver_injects_repository_metadata(tmp_path):
    output = tmp_path / "prompt012.json"
    save_audit_results({"trials": []}, output)

    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["_meta"]["script"] == "prompt012_longseq_audit"
    assert saved["_meta"]["git_commit"]
    assert saved["_meta"]["timestamp"]
    assert len(saved["script_sha256"]) == 64


def test_pending_seeds_skips_completed_checkpoint_trials():
    checkpoint = {"trials": [{"seed": 1000}, {"seed": 1002}]}
    assert pending_seeds((1000, 1001, 1002), checkpoint) == [1001]


def test_seed_ml_makes_torch_initialization_reproducible():
    import torch
    seed_ml(123)
    first = torch.rand(4)
    seed_ml(123)
    assert torch.equal(first, torch.rand(4))
    assert torch.are_deterministic_algorithms_enabled()
    assert torch.backends.cudnn.deterministic
    assert not torch.backends.cudnn.benchmark


def test_trial_seed_fields_record_channel_and_torch_seed_explicitly():
    assert seed_fields(1003) == {"seed": 1003, "torch_seed": 1003}


def test_ml_diverged_uses_model_flag_or_nonfinite_outputs():
    assert ml_diverged({"diverged": True}, np.ones(2), np.ones(2))
    assert ml_diverged({"diverged": False}, np.array([np.nan]), np.ones(1))
    assert not ml_diverged({"diverged": False}, np.ones(2), np.ones(2))


def test_checkpoint_contract_rejects_parameter_mismatch():
    checkpoint = {"experiment_signature": {"N": 1}, "script_sha256": "old"}
    with np.testing.assert_raises(ValueError):
        validate_checkpoint(checkpoint, {"N": 2}, "new")


def test_checkpoint_contract_rejects_script_hash_mismatch():
    checkpoint = {"experiment_signature": {"N": 2}, "script_sha256": "old"}
    with np.testing.assert_raises(ValueError):
        validate_checkpoint(checkpoint, {"N": 2}, "new")


def test_filter_trials_deduplicates_and_removes_unrequested_seeds():
    trials = [{"seed": 1000, "v": 1}, {"seed": 999, "v": 2},
              {"seed": 1000, "v": 3}, {"seed": 1001, "v": 4}]
    assert filter_trials(trials, {1000, 1001}, lambda t: t["seed"]) == [
        {"seed": 1000, "v": 1}, {"seed": 1001, "v": 4}
    ]
