import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "explore"
    / "cma-fade-divergence"
    / "prompt015_unified_baseline.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("prompt015_unified_baseline", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _weight_bank(n_tap=11):
    center = n_tap // 2
    bank = {}
    for name in ("wxx", "wxy", "wyx", "wyy"):
        weights = np.zeros(n_tap, dtype=np.complex128)
        weights[center] = 1.0
        bank[name] = weights
    return bank


def _raw_metrics(pi, *, fixed=None, assignment=None, classification="normal", diverged=False):
    fixed = float(pi if fixed is None else fixed)
    assignment = ["sX", "sY"] if assignment is None else list(assignment)
    return {
        "fixed_label_ber": {
            "zX_sX": fixed,
            "zY_sY": fixed,
            "mean": fixed,
        },
        "permutation_invariant_ber": {
            "mean": float(pi),
            "per_output": [float(pi), float(pi)],
            "assignment": assignment,
        },
        "abs_corr": {
            "zX_sX": 0.9,
            "zX_sY": 0.1,
            "zY_sX": 0.1,
            "zY_sY": 0.9,
        },
        "abs_corr_zX_zY": 0.0,
        "classification": classification,
        "diverged": bool(diverged),
    }


def _annotated_summary_trials(m):
    trials = []
    for seed in range(1000, 1030):
        oracle_pi = 0.001
        methods = {
            "current-CMA": _raw_metrics(0.05, fixed=0.15, assignment=["sY", "sX"]),
            "standard-CMA": _raw_metrics(0.04, fixed=0.14, assignment=["sY", "sX"]),
            "ML-original": _raw_metrics(0.01, fixed=0.11, assignment=["sY", "sX"]),
            "ML-aligned": _raw_metrics(0.012, fixed=0.112, assignment=["sY", "sX"]),
            "oracle": _raw_metrics(oracle_pi),
        }
        for name, metrics in methods.items():
            if name != "oracle":
                metrics["excess_pi_ber_vs_oracle"] = (
                    metrics["permutation_invariant_ber"]["mean"] - oracle_pi
                )
        trials.append(m._annotate_trial({
            "seed": seed,
            "shared_realization_seed": seed,
            "late_slice": [m.LATE_START, m.LATE_END],
            "elapsed_s": 0.1,
            "methods": methods,
        }))
    return trials


def test_script_exists_and_ml_variants_have_auditable_centers(monkeypatch):
    assert SCRIPT.is_file()
    m = load_module()

    class FakeModel:
        def __init__(self, n_tap):
            center = n_tap // 2
            def branch():
                return type("Branch", (), {
                    "conv_RR": type("Weight", (), {"weight": np.zeros((1, 1, n_tap))})(),
                    "conv_RI": type("Weight", (), {"weight": np.zeros((1, 1, n_tap))})(),
                })()

            self.wxx = branch()
            self.wxy = branch()
            self.wyx = branch()
            self.wyy = branch()
            for branch in (self.wxx, self.wxy, self.wyx, self.wyy):
                branch.conv_RR.weight[0, 0, center] = 1.0

    class FakeML:
        def __init__(self, n_tap, **kwargs):
            self.model = FakeModel(n_tap)
            self.kwargs = kwargs

    monkeypatch.setattr(m, "MLChannelEqualizer", FakeML)

    original = m._make_ml_trial(seed=1000, variant="ML-original", n_tap=11)
    aligned = m._make_ml_trial(seed=1000, variant="ML-aligned", n_tap=11)

    assert original["variant"] == "ML-original"
    assert aligned["variant"] == "ML-aligned"

    assert original["init_summary"]["wxx_center_real"] == 1.0
    assert original["init_summary"]["wyy_center_real"] == 1.0
    assert original["init_summary"]["wxy_center_real"] == 1.0
    assert original["init_summary"]["wyx_center_real"] == 1.0
    assert aligned["init_summary"]["wxx_center_real"] == 1.0
    assert aligned["init_summary"]["wyy_center_real"] == 1.0
    assert aligned["init_summary"]["wxy_center_real"] == 0.0
    assert aligned["init_summary"]["wyx_center_real"] == 0.0
    assert aligned["init_summary"]["filters"]["wxy"]["conv_RI"]["center_real"] == 0.0
    assert aligned["init_summary"]["filters"]["wyx"]["conv_RI"]["center_real"] == 0.0
    assert original["init_summary"]["total_l2_norm"] == pytest.approx(2.0)
    assert aligned["init_summary"]["total_l2_norm"] == pytest.approx(np.sqrt(2.0))


def test_aligned_cross_centers_use_torch_no_grad_for_both_real_imag_filters():
    torch = pytest.importorskip("torch")
    m = load_module()
    rr = torch.nn.Parameter(torch.full((1, 1, 3), 1.0))
    ri = torch.nn.Parameter(torch.full((1, 1, 3), 2.0))
    branch = SimpleNamespace(
        conv_RR=SimpleNamespace(weight=rr),
        conv_RI=SimpleNamespace(weight=ri),
    )

    m._set_cross_filter_centers_zero(branch)

    assert rr.detach().cpu().numpy()[0, 0, 1] == 0.0
    assert ri.detach().cpu().numpy()[0, 0, 1] == 0.0


def test_annotate_trial_uses_one_oracle_pi_baseline_for_all_non_oracle_methods():
    m = load_module()
    trial = {
        "seed": 1006,
        "methods": {
            "current-CMA": _raw_metrics(0.045, fixed=0.145, assignment=["sY", "sX"]),
            "standard-CMA": _raw_metrics(0.015, fixed=0.115, assignment=["sY", "sX"]),
            "ML-original": _raw_metrics(0.011, fixed=0.111, assignment=["sY", "sX"]),
            "ML-aligned": _raw_metrics(0.0105, fixed=0.1105, assignment=["sY", "sX"]),
            "oracle": _raw_metrics(0.005),
        },
    }

    annotated = m._annotate_trial(trial)

    assert annotated["methods"]["current-CMA"]["excess_pi_ber_vs_oracle"] == pytest.approx(0.04)
    assert annotated["methods"]["standard-CMA"]["excess_pi_ber_vs_oracle"] == pytest.approx(0.01)
    assert annotated["methods"]["ML-original"]["excess_pi_ber_vs_oracle"] == pytest.approx(0.006)
    assert annotated["methods"]["ML-aligned"]["excess_pi_ber_vs_oracle"] == pytest.approx(0.0055)
    assert "excess_pi_ber_vs_oracle" not in annotated["methods"]["oracle"]
    assert annotated["methods"]["current-CMA"]["descriptive_swap_quality"] == {
        "pi_ber_le_0.05": "clean-swap",
        "pi_ber_lt_0.01": "degraded-swap",
    }


def test_experiment_signature_freezes_formal_parameters_and_relevant_slice():
    m = load_module()
    signature = m._experiment_signature(list(range(1000, 1030)))

    assert signature["N"] == 5_000_000
    assert signature["n_symbols"] == 5_000_000
    assert signature["T_S"] == pytest.approx(1 / 2.5e9)
    assert signature["block"] == 100
    assert signature["sop_rate"] == pytest.approx(4e-7)
    assert signature["gamma_bar"] == pytest.approx(100.0)
    assert signature["f_G"] == pytest.approx(30.0)
    assert signature["modulation"] == "QPSK"
    assert signature["cma_n_tap"] == 11
    assert signature["cma_mu"] == pytest.approx(1e-3)
    assert signature["cma_r2"] == pytest.approx(1.0)
    assert signature["cma_block_size"] == 64
    assert signature["ml_n_tap"] == 11
    assert signature["ml_lr"] == pytest.approx(0.005)
    assert signature["ml_batch_size"] == 1024
    assert signature["ml_n_epochs"] == 20
    assert signature["ml_patience"] == 5
    assert signature["ml_train_fraction"] == pytest.approx(0.5)
    assert signature["ml_device_requested"] == "cuda"
    assert signature["late_slice"] == [m.LATE_START, m.LATE_END]


def test_summarize_trials_rejects_missing_duplicate_and_out_of_range_seed_sets():
    m = load_module()

    def trial(seed):
        return _annotated_summary_trials(m)[seed - 1000]

    with pytest.raises(ValueError, match="30"):
        m._summarize_trials([trial(seed) for seed in range(1000, 1029)])

    duplicate = [trial(seed) for seed in range(1000, 1030)]
    duplicate[-1]["seed"] = 1000
    with pytest.raises(ValueError, match="duplicate|unique"):
        m._summarize_trials(duplicate)

    out_of_range_trial = trial(1000)
    out_of_range_trial["seed"] = 1030
    out_of_range = [trial(seed) for seed in range(1000, 1029)] + [out_of_range_trial]
    with pytest.raises(ValueError, match="1000|1029|range"):
        m._summarize_trials(out_of_range)


def test_summary_exposes_exact_per_pair_gates_and_overall_primary_gate():
    m = load_module()

    summary = m._summarize_trials(_annotated_summary_trials(m))
    core = summary["paired_comparisons"]["standard-CMA_vs_ML-original"]
    aligned = summary["paired_comparisons"]["standard-CMA_vs_ML-aligned"]
    control = summary["paired_comparisons"]["current-CMA_vs_ML-original"]

    for pair in (core, aligned):
        assert pair["method"] == "exact"
        assert pair["gate"]["p_lt_0_05"] is True
        assert pair["gate"]["ml_wins_at_least_25_of_30"] is True
        assert pair["gate"]["passes_primary_gate"] is True
    assert control["method"] == "exact"
    assert control["gate"]["is_primary"] is False
    assert summary["overall_gate"]["required_pair_keys"] == [
        "standard-CMA_vs_ML-original",
        "standard-CMA_vs_ML-aligned",
    ]
    assert summary["overall_gate"]["passes"] is True
    assert summary["overall_gate"]["status"] == "GO"
    assert summary["overall_gate"]["classification_is_descriptive_only"] is True


def test_summary_validates_raw_metric_schema_and_finite_values():
    m = load_module()
    trials = _annotated_summary_trials(m)

    nonfinite = deepcopy(trials)
    nonfinite[0]["methods"]["ML-original"]["fixed_label_ber"]["mean"] = np.nan
    with pytest.raises(ValueError, match="finite"):
        m._summarize_trials(nonfinite)

    missing = deepcopy(trials)
    del missing[0]["methods"]["ML-original"]["permutation_invariant_ber"]
    with pytest.raises(ValueError, match="schema|missing"):
        m._summarize_trials(missing)


def test_run_single_seed_executes_both_ml_variants_on_one_shared_realization(monkeypatch):
    m = load_module()
    n = 32
    shared = (
        np.ones(n, dtype=np.complex128) * (1 + 1j),
        np.ones(n, dtype=np.complex128) * (2 + 2j),
        np.ones(n, dtype=np.complex128) * (3 + 3j),
        np.ones(n, dtype=np.complex128) * (4 + 4j),
        np.ones(n, dtype=float),
        np.zeros(n, dtype=float),
    )
    calls = []
    gen_calls = []

    class FakeCfg:
        class Turb:
            @staticmethod
            def as_dict():
                return {m.TURBULENCE: (1.0, 1.0)}

        turbulence = Turb()

    monkeypatch.setattr(m, "SimulationConfig", lambda: FakeCfg())
    monkeypatch.setattr(m, "LATE_START", 4)
    monkeypatch.setattr(m, "LATE_END", 12)
    monkeypatch.setattr(m, "gen_channel", lambda *args: (gen_calls.append(args) or shared))
    monkeypatch.setattr(m, "run_cma_diagnostic", lambda *args, **kwargs: {
        "online": {"zX": np.ones(8, dtype=np.complex128), "zY": np.ones(8, dtype=np.complex128)}
    })
    monkeypatch.setattr(m, "oracle_equalize", lambda *args: (np.ones(n, dtype=np.complex128), np.ones(n, dtype=np.complex128)))
    monkeypatch.setattr(m, "evaluate_outputs", lambda *args, **kwargs: {
        "fixed_label_ber": {"mean": 0.2},
        "permutation_invariant_ber": {"mean": 0.1},
        "classification": "normal",
        "diverged": False,
    })
    monkeypatch.setattr(m, "seed_ml", lambda seed: calls.append(("seed_ml", seed)))
    monkeypatch.setattr(m, "ml_diverged", lambda result, z_x, z_y: bool(result["diverged"]))

    def fake_variant_runner(seed, variant, r_x, r_y, s_x, s_y):
        calls.append(("variant", variant, seed, r_x is shared[0], r_y is shared[1], s_x is shared[2], s_y is shared[3]))
        value = 0.25 if variant == "ML-original" else 0.125
        return {
            "variant": variant,
            "zX": np.full(n, value, dtype=np.complex128),
            "zY": np.full(n, value, dtype=np.complex128),
            "diverged": False,
            "n_train": 16,
            "init_summary": {"variant": variant},
            "device": {"requested": "cuda", "actual": "cpu"},
            "execution": {"constructed": True, "trained": True, "inferred": True},
        }

    monkeypatch.setattr(m, "_run_ml_variant", fake_variant_runner)

    trial = m._run_single_seed(1006)

    assert ("variant", "ML-original", 1006, True, True, True, True) in calls
    assert ("variant", "ML-aligned", 1006, True, True, True, True) in calls
    assert len(gen_calls) == 1
    assert gen_calls[0][-1] == 1006
    assert trial["methods"]["ML-original"]["classification"] != "not-run"
    assert trial["methods"]["ML-aligned"]["classification"] != "not-run"
    assert trial["methods"]["ML-original"]["fixed_label_ber"]["mean"] == pytest.approx(0.2)
    assert trial["methods"]["ML-aligned"]["permutation_invariant_ber"]["mean"] == pytest.approx(0.1)
    assert trial["methods"]["ML-original"]["shared_realization_seed"] == 1006
    assert trial["methods"]["ML-aligned"]["shared_realization_seed"] == 1006
    assert trial["artifacts"]["ML-aligned"]["execution"]["trained"] is True
    assert trial["artifacts"]["ML-aligned"]["device"] == {
        "requested": "cuda",
        "actual": "cpu",
    }
    assert trial["elapsed_s"] >= 0.0


def test_main_dry_run_never_calls_long_trial_and_keeps_trials_empty(monkeypatch, tmp_path):
    assert SCRIPT.is_file()
    m = load_module()
    saved = []
    calls = {"run": 0}

    def fake_run_seed(*args, **kwargs):
        calls["run"] += 1
        raise AssertionError("_run_single_seed must not be called in dry-run")

    monkeypatch.setattr(m, "_run_single_seed", fake_run_seed)
    monkeypatch.setattr(m, "_save_payload_atomic", lambda payload, path: saved.append((payload, Path(path))))

    output = tmp_path / "prompt015.json"
    payload = m.main([
        "--seeds", "1002", "1000",
        "--dry-run",
        "--max-seeds", "1",
        "--output", str(output),
    ])

    assert calls["run"] == 0
    assert payload["trials"] == []
    assert payload["checkpoint"]["requested_seeds"] == [1000, 1002]
    assert payload["checkpoint"]["completed_seeds"] == []
    assert payload["checkpoint"]["pending_seeds"] == [1000]
    assert payload["checkpoint"]["dry_run"] is True
    assert saved[-1][1] == output


def test_main_loads_valid_checkpoint_and_resumes_only_missing_requested_seed(monkeypatch, tmp_path):
    m = load_module()
    output = tmp_path / "resume.json"
    existing = {
        "experiment": "PROMPT-015 unified legal baseline",
        "experiment_signature": {"name": "sig", "version": 1},
        "source_sha256": {"prompt015_unified_baseline.py": "abc"},
        "checkpoint": {
            "requested_seeds": [1000, 1001],
            "completed_seeds": [1000],
            "pending_seeds": [1001],
            "complete": False,
            "dry_run": False,
            "output_path": str(output),
        },
        "trials": [{
            "seed": 1000,
            "methods": {
                "current-CMA": {"excess_pi_ber_vs_oracle": 0.03},
                "standard-CMA": {"excess_pi_ber_vs_oracle": 0.02},
                "ML-original": {"excess_pi_ber_vs_oracle": 0.01},
                "ML-aligned": {"excess_pi_ber_vs_oracle": 0.009},
                "oracle": {"permutation_invariant_ber": {"mean": 0.001}},
            },
        }],
    }
    output.write_text(json.dumps(existing), encoding="utf-8")

    existing["experiment_signature"]["requested_seeds"] = [1000, 1001]
    output.write_text(json.dumps(existing), encoding="utf-8")
    monkeypatch.setattr(m, "_experiment_signature", lambda requested: {
        "name": "sig", "version": 1, "requested_seeds": list(requested)
    })
    monkeypatch.setattr(m, "source_sha256s", lambda: {"prompt015_unified_baseline.py": "abc"})
    executed = []

    def fake_run(seed):
        executed.append(seed)
        return {
            "seed": seed,
            "methods": {
                "current-CMA": {"excess_pi_ber_vs_oracle": 0.04},
                "standard-CMA": {"excess_pi_ber_vs_oracle": 0.03},
                "ML-original": {"excess_pi_ber_vs_oracle": 0.02},
                "ML-aligned": {"excess_pi_ber_vs_oracle": 0.01},
                "oracle": {"permutation_invariant_ber": {"mean": 0.001}},
            },
        }

    saved = []
    monkeypatch.setattr(m, "_run_single_seed", fake_run)
    monkeypatch.setattr(m, "_save_payload_atomic", lambda payload, path: saved.append((json.loads(json.dumps(payload)), Path(path))))

    payload = m.main(["--seeds", "1001", "1000", "--output", str(output)])

    assert executed == [1001]
    assert [row["seed"] for row in payload["trials"]] == [1000, 1001]
    assert payload["checkpoint"]["completed_seeds"] == [1000, 1001]
    assert payload["checkpoint"]["pending_seeds"] == []
    assert saved[-1][1] == output


def test_checkpoint_validation_fails_closed_on_signature_duplicate_and_out_of_range(tmp_path):
    m = load_module()
    output = tmp_path / "bad.json"
    payload = {
        "experiment": "PROMPT-015 unified legal baseline",
        "experiment_signature": {"name": "sig", "version": 0},
        "source_sha256": {"prompt015_unified_baseline.py": "bad"},
        "checkpoint": {
            "requested_seeds": [1000, 1030],
            "completed_seeds": [1000, 1000],
            "pending_seeds": [],
            "complete": False,
            "dry_run": False,
            "output_path": str(output),
        },
        "trials": [{"seed": 1000}, {"seed": 1000}],
    }
    output.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="signature|duplicate|range|SHA"):
        m._load_checkpoint(output, expected_signature={"name": "sig", "version": 1}, expected_sha={"prompt015_unified_baseline.py": "abc"})


def test_checkpoint_validation_rejects_extra_seed_lists_even_with_matching_signature(tmp_path):
    m = load_module()
    output = tmp_path / "extra-seed.json"
    signature = {"name": "sig", "version": 1, "requested_seeds": [1000, 1001]}
    payload = {
        "experiment": "PROMPT-015 unified legal baseline",
        "experiment_signature": signature,
        "source_sha256": {"prompt015_unified_baseline.py": "abc"},
        "checkpoint": {
            "requested_seeds": [1000, 1001, 1002],
            "completed_seeds": [1000],
            "pending_seeds": [1001, 1002],
            "complete": False,
            "dry_run": False,
            "output_path": str(output),
        },
        "trials": [{"seed": 1000}],
    }
    output.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="requested|extra|seed"):
        m._load_checkpoint(output, expected_signature=signature, expected_sha={"prompt015_unified_baseline.py": "abc"})
