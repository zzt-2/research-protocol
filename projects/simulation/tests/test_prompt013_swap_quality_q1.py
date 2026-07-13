"""PROMPT-013 Q1 resumable experiment tests."""
import importlib.util
import json
import os
from contextlib import nullcontext
from pathlib import Path

import numpy as np


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "explore"
    / "cma-fade-divergence"
    / "prompt013_swap_quality_q1.py"
)


def test_prompt013_q1_script_exists():
    assert SCRIPT.is_file()


def _load_module():
    spec = importlib.util.spec_from_file_location("prompt013_swap_quality_q1", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _method(pi_ber, assignment=("sY", "sX"), fixed=0.5):
    return {
        "fixed_label_ber": {"mean": fixed},
        "permutation_invariant_ber": {
            "mean": pi_ber,
            "assignment": list(assignment),
        },
        "classification": "clean-swap",
        "diverged": False,
    }


def _trial(seed, cma, ml, oracle):
    return {
        "seed": seed,
        "torch_seed": seed,
        "methods": {
            "current_cma": _method(cma),
            "ml": _method(ml),
            "oracle": _method(oracle, assignment=("sX", "sY"), fixed=oracle),
        },
    }


def test_annotate_trial_adds_per_seed_excess_and_both_descriptive_thresholds():
    m = _load_module()
    trial = m.annotate_trial(_trial(1000, cma=0.03, ml=0.009, oracle=0.004), "prompt012")

    assert trial["origin"] == "prompt012"
    assert trial["shared_realization_seed"] == 1000
    assert trial["methods"]["current_cma"]["excess_pi_ber_vs_oracle"] == 0.026
    assert trial["methods"]["ml"]["excess_pi_ber_vs_oracle"] == 0.005
    assert trial["methods"]["current_cma"]["descriptive_swap_quality"] == {
        "pi_ber_le_0.05": "clean-swap",
        "pi_ber_lt_0.01": "degraded-swap",
    }
    assert trial["methods"]["ml"]["descriptive_swap_quality"]["pi_ber_lt_0.01"] == "clean-swap"


def test_summary_uses_two_sided_wilcoxon_wins_and_continuous_excess():
    m = _load_module()
    trials = [
        m.annotate_trial(_trial(1000 + i, 0.03 + i * 1e-3, 0.005, 0.004), "prompt012")
        for i in range(10)
    ]
    summary = m.summarize_q1(trials)

    assert summary["n_trials"] == 10
    assert summary["paired_comparison"]["ml_wins"] == 10
    assert summary["paired_comparison"]["ties"] == 0
    assert summary["paired_comparison"]["wilcoxon"]["alternative"] == "two-sided"
    assert summary["paired_comparison"]["wilcoxon"]["zero_method"] == "wilcox"
    assert summary["paired_comparison"]["wilcoxon"]["correction"] is False
    assert summary["paired_comparison"]["wilcoxon"]["nan_policy"] == "raise"
    assert summary["paired_comparison"]["wilcoxon"]["effective_n"] == 10
    assert summary["paired_comparison"]["wilcoxon"]["method"] == "exact"
    assert np.isclose(summary["paired_comparison"]["wilcoxon"]["pvalue"], 0.001953125)
    assert summary["continuous"]["current_cma"]["excess_pi_ber_vs_oracle"]["values"][0] == 0.026
    assert summary["q1_gate"]["status"] == "pending"


def test_summary_dual_threshold_counts_match_prompt012_baseline():
    m = _load_module()
    source = json.loads(m.SOURCE_RESULT_PATH.read_text(encoding="utf-8"))
    trials = m.import_prompt012_trials(source)
    summary = m.summarize_q1(trials)

    le = summary["descriptive_thresholds"]["pi_ber_le_0.05"]
    lt = summary["descriptive_thresholds"]["pi_ber_lt_0.01"]
    assert le["current_cma"] == {"clean-swap": 8, "degraded-swap": 2}
    assert le["ml"] == {"clean-swap": 10}
    assert lt["current_cma"] == {"clean-swap": 6, "degraded-swap": 4}
    assert lt["ml"] == {"clean-swap": 9, "degraded-swap": 1}
    assert np.isclose(summary["paired_comparison"]["wilcoxon"]["pvalue"], 0.001953125)
    assert summary["holdout_1010_1029"]["n_trials"] == 0


def test_wilcoxon_uses_asymptotic_when_rounded_differences_have_zero_or_ties():
    m = _load_module()
    trials = [
        m.annotate_trial(_trial(1000, 0.01, 0.01, 0.001), "prompt012"),
        m.annotate_trial(_trial(1001, 0.02, 0.01, 0.001), "prompt012"),
        m.annotate_trial(_trial(1002, 0.03, 0.02, 0.001), "prompt012"),
    ]
    comparison = m.summarize_q1(trials)["paired_comparison"]
    assert comparison["differences"] == [0.0, 0.01, 0.01]
    assert comparison["ties"] == 1
    assert comparison["wilcoxon"]["method"] == "asymptotic"
    assert comparison["wilcoxon"]["effective_n"] == 2


def test_completed_30_seed_integrity_failure_blocks_q1_gate():
    m = _load_module()
    trials = [
        m.annotate_trial(_trial(1000 + i, 0.03, 0.005, 0.004), "prompt013")
        for i in range(30)
    ]
    trials[-1]["seed"] = 1028
    summary = m.summarize_q1(trials)
    assert summary["q1_gate"]["status"] == "fail"
    assert summary["integrity"]["duplicate_seeds"] == [1028]
    assert summary["integrity"]["missing_target_seeds"] == [1029]


def test_nonfinite_metric_blocks_q1_gate_instead_of_being_omitted():
    m = _load_module()
    trials = [
        m.annotate_trial(_trial(1000 + i, 0.03, 0.005, 0.004), "prompt013")
        for i in range(30)
    ]
    trials[-1]["methods"]["ml"]["permutation_invariant_ber"]["mean"] = float("nan")
    summary = m.summarize_q1(trials)
    assert summary["q1_gate"]["status"] == "fail"
    assert summary["integrity"]["nonfinite_pairs"] == [1029]


def _gate_trials(module, differences):
    trials = []
    for index, difference in enumerate(differences):
        ml = 0.11 if difference < 0 else 0.01
        cma = ml + difference
        trials.append(module.annotate_trial(
            _trial(1000 + index, cma, ml, 0.0),
            "prompt012" if index < 10 else "prompt013",
        ))
    return trials


def test_30_seed_gate_passes_only_when_both_predeclared_conditions_pass():
    m = _load_module()
    differences = [0.001 + i * 1e-5 for i in range(30)]
    summary = m.summarize_q1(_gate_trials(m, differences))
    assert summary["q1_gate"]["status"] == "pass"
    assert summary["paired_comparison"]["ml_wins"] == 30
    assert summary["paired_comparison"]["wilcoxon"]["pvalue"] < 0.05


def test_30_seed_gate_fails_when_only_p_condition_fails():
    m = _load_module()
    differences = [1e-13] * 25 + [-0.1] * 3 + [0.0] * 2
    summary = m.summarize_q1(_gate_trials(m, differences))
    assert summary["paired_comparison"]["ml_wins"] == 25
    assert summary["paired_comparison"]["wilcoxon"]["pvalue"] >= 0.05
    assert summary["q1_gate"]["status"] == "fail"


def test_30_seed_gate_fails_when_only_win_condition_fails():
    m = _load_module()
    differences = [0.1] * 24 + [-0.001] * 6
    summary = m.summarize_q1(_gate_trials(m, differences))
    assert summary["paired_comparison"]["ml_wins"] == 24
    assert summary["paired_comparison"]["wilcoxon"]["pvalue"] < 0.05
    assert summary["q1_gate"]["status"] == "fail"


def test_descriptive_threshold_boundaries_are_inclusive_005_strict_001():
    m = _load_module()
    at_005 = m.annotate_trial(_trial(1000, 0.05, 0.05, 0.0), "prompt012")
    at_001 = m.annotate_trial(_trial(1001, 0.01, 0.01, 0.0), "prompt012")
    assert at_005["methods"]["current_cma"]["descriptive_swap_quality"] == {
        "pi_ber_le_0.05": "clean-swap",
        "pi_ber_lt_0.01": "degraded-swap",
    }
    assert at_001["methods"]["current_cma"]["descriptive_swap_quality"]["pi_ber_lt_0.01"] == "degraded-swap"


def test_run_lock_is_mutually_exclusive_and_released_after_failure(tmp_path):
    m = _load_module()
    lock = tmp_path / "prompt013.lock"
    with m.exclusive_run_lock(lock):
        assert lock.exists()
        with np.testing.assert_raises(RuntimeError):
            with m.exclusive_run_lock(lock):
                pass
    assert not lock.exists()
    with np.testing.assert_raises(RuntimeError):
        with m.exclusive_run_lock(lock):
            raise RuntimeError("body failed")
    assert not lock.exists()


def test_atomic_save_preserves_old_checkpoint_when_temp_write_fails(tmp_path, monkeypatch):
    m = _load_module()
    output = tmp_path / "prompt013.json"
    output.write_text('{"old": true}', encoding="utf-8")

    def failing_save(data, filepath, script_name):
        Path(filepath).write_text('{"partial": true}', encoding="utf-8")
        raise RuntimeError("injected write failure")

    monkeypatch.setattr(m, "save_results", failing_save)
    with np.testing.assert_raises(RuntimeError):
        m.save_q1_results({"new": True}, output)
    assert json.loads(output.read_text(encoding="utf-8")) == {"old": True}
    assert list(tmp_path.glob("*.tmp")) == []


def test_prompt012_source_validation_rejects_provenance_or_contract_mismatch():
    m = _load_module()
    cfg = m.SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[m.TURBULENCE]
    source = json.loads(m.SOURCE_RESULT_PATH.read_text(encoding="utf-8"))
    m.validate_prompt012_source(source, alpha, beta)
    bad_sha = json.loads(json.dumps(source))
    bad_sha["script_sha256"] = "bad"
    with np.testing.assert_raises(ValueError):
        m.validate_prompt012_source(bad_sha, alpha, beta)
    bad_contract = json.loads(json.dumps(source))
    bad_contract["experiment_signature"]["N"] = 1
    with np.testing.assert_raises(ValueError):
        m.validate_prompt012_source(bad_contract, alpha, beta)


def test_checkpoint_trial_validation_rejects_missing_source_duplicate_unexpected_or_nonfinite():
    m = _load_module()
    source = json.loads(m.SOURCE_RESULT_PATH.read_text(encoding="utf-8"))
    trials = m.import_prompt012_trials(source)
    m.validate_checkpoint_trials(trials)
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint_trials(trials[1:])
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint_trials(trials + [trials[0]])
    unexpected = json.loads(json.dumps(trials))
    unexpected.append(json.loads(json.dumps(trials[0])))
    unexpected[-1]["seed"] = 2000
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint_trials(unexpected)
    nonfinite = json.loads(json.dumps(trials))
    nonfinite[0]["methods"]["ml"]["permutation_invariant_ber"]["mean"] = float("nan")
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint_trials(nonfinite)


def test_execute_seed_generates_one_shared_realization(monkeypatch):
    m = _load_module()
    monkeypatch.setattr(m, "N_SYMBOLS", 16)
    calls = {"channel": 0}
    arrays = tuple(np.ones(16, dtype=complex) for _ in range(4)) + (
        np.ones(16), np.zeros(16),
    )

    def channel(*args, **kwargs):
        calls["channel"] += 1
        return arrays

    class FakeCMA:
        def __init__(self, **kwargs):
            pass

        def equalize(self, rx, ry):
            return {"zX": rx, "zY": ry, "diverged": False, "diverge_idx": None,
                    "final_w_norm": 1.0, "init_w_norm": 1.0}

    def fake_metrics(*args, **kwargs):
        return _method(0.01)

    monkeypatch.setattr(m, "generate_shared_dual_pol_realization", channel)
    monkeypatch.setattr(m, "CMAEqualizer2x2", FakeCMA)
    monkeypatch.setattr(m, "seed_ml", lambda seed: None)
    monkeypatch.setattr(m, "run_ml_trial", lambda *args: (arrays[0], arrays[1], 8, {"diverged": False}))
    monkeypatch.setattr(m, "ml_diverged", lambda *args: False)
    monkeypatch.setattr(m, "oracle_equalize", lambda *args: (arrays[0], arrays[1]))
    monkeypatch.setattr(m, "evaluate_outputs", fake_metrics)
    trial = m._execute_seed(1010, 1.0, 1.0)
    assert calls["channel"] == 1
    assert trial["shared_realization_seed"] == 1010


def test_run_batch_checkpoints_after_each_seed(monkeypatch):
    m = _load_module()
    source = json.loads(m.SOURCE_RESULT_PATH.read_text(encoding="utf-8"))
    payload = {"trials": m.import_prompt012_trials(source)}
    monkeypatch.setattr(m, "_load_or_initialize", lambda: (payload, 1.0, 1.0))
    monkeypatch.setattr(
        m, "_execute_seed",
        lambda seed, a, b: m.annotate_trial(_trial(seed, 0.03, 0.005, 0.004), "prompt013"),
    )
    saved_lengths = []
    monkeypatch.setattr(m, "save_q1_results", lambda data: saved_lengths.append(len(data["trials"])))
    monkeypatch.setattr(m, "exclusive_run_lock", lambda path: nullcontext())
    m.run_batch((1010, 1011))
    assert saved_lengths == [11, 12]


def test_import_requires_exact_prompt012_baseline_seeds():
    m = _load_module()
    source = {"trials": [_trial(seed, 0.03, 0.005, 0.004) for seed in range(1000, 1009)]}
    with np.testing.assert_raises(ValueError):
        m.import_prompt012_trials(source)


def test_contract_is_fixed_to_all_30_seeds_not_the_current_batch():
    m = _load_module()
    signature = m.build_experiment_signature(
        alpha=1.2, beta=0.8, source_result_sha256="abc"
    )
    assert signature["target_seeds"] == list(range(1000, 1030))
    assert signature["new_seed_batches_do_not_change_signature"] is True
    assert signature["source_result_sha256"] == "abc"
    assert signature["N"] == 5_000_000


def test_checkpoint_rejects_signature_or_source_sha_mismatch():
    m = _load_module()
    checkpoint = {"experiment_signature": {"N": 5}, "source_sha256": {"script": "a"}}
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint(checkpoint, {"N": 6}, {"script": "a"})
    with np.testing.assert_raises(ValueError):
        m.validate_checkpoint(checkpoint, {"N": 5}, {"script": "b"})


def test_batch_validation_limits_new_seeds_to_five_and_skips_completed():
    m = _load_module()
    assert m.validate_batch(range(1010, 1015)) == list(range(1010, 1015))
    with np.testing.assert_raises(ValueError):
        m.validate_batch(range(1010, 1016))
    with np.testing.assert_raises(ValueError):
        m.validate_batch((1009,))
    assert m.pending_seeds((1010, 1011), {"trials": [{"seed": 1010}]}) == [1011]


def test_source_sha_map_covers_all_q1_dependencies_and_detects_changes():
    m = _load_module()
    names = set(m.source_sha256s())
    assert names == {
        "prompt013_swap_quality_q1.py",
        "prompt012_longseq_audit.py",
        "ml_long_seq_failure.py",
        "common/_cma.py",
        "common/_ml_equalizer.py",
        "common/_gg_time.py",
        "common/_config.py",
        "common/_equalizer.py",
        "params.py",
    }
    first = m.source_sha256s(contents={"a": b"one"})
    second = m.source_sha256s(contents={"a": b"two"})
    assert first != second


def test_result_saver_uses_save_results_metadata(tmp_path):
    m = _load_module()
    output = tmp_path / "prompt013.json"
    m.save_q1_results({"trials": []}, output)

    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["_meta"]["script"] == "prompt013_swap_quality_q1"
    assert saved["_meta"]["git_commit"]
    assert saved["_meta"]["timestamp"]
