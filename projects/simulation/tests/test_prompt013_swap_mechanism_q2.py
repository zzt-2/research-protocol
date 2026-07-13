"""PROMPT-013 Q2 mechanism experiment contract tests."""
from contextlib import nullcontext
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "explore"
    / "cma-fade-divergence"
    / "prompt013_swap_mechanism_q2.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("prompt013_swap_mechanism_q2", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_q2_script_exists_and_seed_contract_excludes_outlier():
    assert SCRIPT.is_file()
    m = _load_module()
    assert m.HIGH_GAP_SEEDS == (1006, 1017, 1011)
    assert m.LOW_GAP_SEEDS == (1024, 1028, 1029)
    assert m.TARGET_SEEDS == (1006, 1017, 1011, 1024, 1028, 1029)
    assert 1004 not in m.TARGET_SEEDS
    assert m.OUTLIER_SEED == 1004
    assert m.validate_batch((1006, 1017, 1011)) == [1006, 1017, 1011]
    with pytest.raises(ValueError):
        m.validate_batch((1006, 1017, 1011, 1024))
    with pytest.raises(ValueError):
        m.validate_batch((1004,))


def test_q1_gate_requires_pass_complete_30_and_exact_selected_gaps():
    m = _load_module()
    payload = json.loads(m.Q1_RESULT_PATH.read_text(encoding="utf-8"))
    selected = m.validate_q1_gate(payload)
    assert [row["seed"] for row in selected] == list(m.TARGET_SEEDS)

    bad_gate = json.loads(json.dumps(payload))
    bad_gate["summary"]["q1_gate"]["status"] = "fail"
    with pytest.raises(ValueError, match="gate"):
        m.validate_q1_gate(bad_gate)

    missing = json.loads(json.dumps(payload))
    missing["trials"] = missing["trials"][:-1]
    with pytest.raises(ValueError, match="30"):
        m.validate_q1_gate(missing)

    drift = json.loads(json.dumps(payload))
    row = next(item for item in drift["trials"] if int(item["seed"]) == 1006)
    row["methods"]["current_cma"]["excess_pi_ber_vs_oracle"] += 0.01
    with pytest.raises(ValueError, match="gap|inconsistent"):
        m.validate_q1_gate(drift)


def test_q1_gate_independently_rejects_summary_schema_trial_and_dependency_tampering():
    m = _load_module()
    payload = json.loads(m.Q1_RESULT_PATH.read_text(encoding="utf-8"))

    summary = json.loads(json.dumps(payload))
    summary["summary"]["paired_comparison"]["ml_wins"] = 29
    with pytest.raises(ValueError, match="summary"):
        m.validate_q1_gate(summary)

    no_integrity = json.loads(json.dumps(payload))
    del no_integrity["summary"]["integrity"]
    with pytest.raises(ValueError, match="integrity"):
        m.validate_q1_gate(no_integrity)

    changed_trial = json.loads(json.dumps(payload))
    changed_trial["trials"][0]["methods"]["current_cma"]["permutation_invariant_ber"]["mean"] += 0.1
    with pytest.raises(ValueError, match="trial|gap|summary"):
        m.validate_q1_gate(changed_trial)

    bad_dependency = json.loads(json.dumps(payload))
    bad_dependency["source_sha256"]["common/_cma.py"] = "bad"
    with pytest.raises(ValueError, match="dependency.*SHA"):
        m.validate_q1_gate(bad_dependency)


def test_window_contract_covers_fixed_late_slice_with_partial_tail():
    m = _load_module()
    assert (m.LATE_START, m.LATE_END, m.WINDOW_SIZE) == (4_375_000, 5_000_000, 50_000)
    windows = m.window_slices(m.LATE_START, m.LATE_END, m.WINDOW_SIZE)
    assert windows[0] == (4_375_000, 4_425_000)
    assert windows[-1] == (4_975_000, 5_000_000)
    assert len(windows) == 13


def test_lock_and_atomic_save_preserve_checkpoint_on_failure(tmp_path, monkeypatch):
    m = _load_module()
    lock = tmp_path / "q2.lock"
    with m.exclusive_run_lock(lock):
        assert lock.exists()
        with pytest.raises(RuntimeError):
            with m.exclusive_run_lock(lock):
                pass
    assert not lock.exists()

    output = tmp_path / "q2.json"
    output.write_text('{"old": true}', encoding="utf-8")

    def failing_save(data, filepath, script_name):
        Path(filepath).write_text('{"partial": true}', encoding="utf-8")
        raise RuntimeError("injected")

    monkeypatch.setattr(m, "save_results", failing_save)
    with pytest.raises(RuntimeError, match="injected"):
        m.save_q2_results({"new": True}, output)
    assert json.loads(output.read_text(encoding="utf-8")) == {"old": True}
    assert list(tmp_path.glob("*.tmp")) == []


def test_current_diagnostic_matches_common_cma_outputs_and_full_late_pi():
    m = _load_module()
    from common._cma import CMAEqualizer2x2

    rng = np.random.default_rng(9)
    r_x = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    r_y = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    s_x = np.sign(r_x.real) + 1j * np.sign(r_x.imag)
    s_y = np.sign(r_y.real) + 1j * np.sign(r_y.imag)
    s_x /= np.sqrt(2)
    s_y /= np.sqrt(2)

    common = CMAEqualizer2x2(n_tap=11, mu=1e-4, R2=1.0).equalize(r_x, r_y)
    diagnostic = m.run_cma_diagnostic(
        r_x, r_y, mode="current", mu=1e-4, n_tap=11,
        late_slice=(128, 1024), fork_at=1024,
    )
    assert np.allclose(diagnostic["online"]["zX"], common["zX"][128:1024])
    assert np.allclose(diagnostic["online"]["zY"], common["zY"][128:1024])
    got = m.compute_method_metrics(
        diagnostic["online"]["zX"], diagnostic["online"]["zY"],
        s_x[128:1024], s_y[128:1024],
    )
    expected = m.compute_method_metrics(
        common["zX"][128:1024], common["zY"][128:1024],
        s_x[128:1024], s_y[128:1024],
    )
    assert got["permutation_invariant_ber"] == expected["permutation_invariant_ber"]


def test_fork_online_and_frozen_share_full_weight_state_and_frozen_does_not_move():
    m = _load_module()
    rng = np.random.default_rng(3)
    r_x = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    r_y = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    result = m.run_cma_diagnostic(
        r_x, r_y, mode="current", mu=1e-4, n_tap=11,
        late_slice=(256, 1024), fork_at=256,
    )
    fork = m.deserialize_weights(result["fork"]["weights"])
    frozen_final = m.deserialize_weights(result["frozen"]["final_weights"])
    assert set(fork) == {"wxx", "wxy", "wyx", "wyy"}
    assert all(weights.shape == (11,) for weights in fork.values())
    assert all(np.array_equal(fork[name], frozen_final[name]) for name in fork)
    assert result["frozen"]["relative_weight_displacement"] == 0.0
    start = result["fork"]["late_offset"]
    assert np.allclose(
        result["online"]["zX"][start:start + 64],
        result["frozen"]["zX"][start:start + 64],
    )
    first_fork_trace = next(
        row for row in result["trace"]
        if row["output_start"] >= result["fork"]["output_start"]
    )
    assert first_fork_trace["relative_weight_displacement"] == 0.0

    with pytest.raises(ValueError, match="block-aligned"):
        m.run_cma_diagnostic(
            r_x, r_y, mode="current", mu=1e-4, n_tap=11,
            late_slice=(256, 1024), fork_at=257,
        )


def test_standard_one_tap_delta_matches_direct_formula_and_finite_difference():
    m = _load_module()
    r_x = np.array([[0.3 + 0.7j], [-0.2 + 0.4j], [0.8 - 0.1j]])
    r_y = np.array([[0.1 - 0.2j], [0.5 + 0.3j], [-0.4 + 0.2j]])
    w_xx = 0.6 - 0.25j
    w_xy = -0.1 + 0.2j
    z_x = r_x[:, 0] * w_xx + r_y[:, 0] * w_xy
    z_y = np.array([0.2 + 0.1j, -0.3 + 0.4j, 0.1 - 0.5j])
    mu = 2e-4
    _, standard = m._cma_deltas(r_x, r_y, z_x, z_y, 1.0, mu)
    direct = mu * np.mean((1.0 - np.abs(z_x) ** 2) * z_x * np.conj(r_x[:, 0]))
    assert np.allclose(standard["wxx"][0], direct)

    def cost(weight):
        output = r_x[:, 0] * weight + r_y[:, 0] * w_xy
        return 0.5 * np.mean((1.0 - np.abs(output) ** 2) ** 2)

    eps = 1e-6
    d_real = (cost(w_xx + eps) - cost(w_xx - eps)) / (2 * eps)
    d_imag = (cost(w_xx + 1j * eps) - cost(w_xx - 1j * eps)) / (2 * eps)
    finite_difference_update = -mu * 0.5 * (d_real + 1j * d_imag)
    assert np.allclose(standard["wxx"][0], finite_difference_update, rtol=1e-6, atol=1e-10)


def test_metrics_recover_swap_scalars_and_leakage_on_synthetic_data():
    m = _load_module()
    rng = np.random.default_rng(4)
    alphabet = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j], dtype=complex) / np.sqrt(2)
    s_x = rng.choice(alphabet, 512)
    s_y = rng.choice(alphabet, 512)
    z_x = 2j * s_y
    z_y = -0.5 * s_x
    metrics = m.compute_method_metrics(z_x, z_y, s_x, s_y)
    assert metrics["assignment"] == ["sY", "sX"]
    assert metrics["permutation_invariant_ber"] == 0.0
    assert metrics["phase_only_nmse"] > 0.1
    assert metrics["complex_scalar_nmse"] < 1e-12
    assert metrics["radial_error"] > 0.1
    assert metrics["leakage_power_ratio"] < 1e-12
    assert metrics["j_cm"] > 0.1


def _ha_trial(seed, cma_nmse, ml_nmse, j_cm, grad, leakage=None):
    leakage = cma_nmse if leakage is None else leakage
    return {
        "seed": seed,
        "methods": {"ml": {"full_late": {
            "complex_scalar_nmse": ml_nmse,
            "leakage_power_ratio": ml_nmse,
        }}},
        "mechanism": {
            variant: {
                "online": {"full_late": {
                    "complex_scalar_nmse": cma_nmse,
                    "leakage_power_ratio": leakage,
                    "j_cm": j_cm,
                }},
                "gradient": {"full_late": {
                    "scalar_error_update_norm": grad,
                    "standard_with_z_update_norm": grad,
                }},
            }
            for variant in ("current", "standard")
        },
    }


def test_hypothesis_a_support_falsify_and_unknown():
    m = _load_module()
    trials = [
        _ha_trial(seed, 0.12, 0.01, 1.0, 1.0)
        for seed in m.HIGH_GAP_SEEDS
    ] + [
        _ha_trial(seed, 0.02, 0.01, 0.9, 0.9)
        for seed in m.LOW_GAP_SEEDS
    ]
    assert m.evaluate_hypothesis_a(trials)["verdict"] == "supported"

    falsified = json.loads(json.dumps(trials))
    for trial in falsified:
        trial["mechanism"]["standard"]["online"]["full_late"]["complex_scalar_nmse"] = 0.011
        trial["mechanism"]["standard"]["online"]["full_late"]["leakage_power_ratio"] = 0.011
    assert m.evaluate_hypothesis_a(falsified)["verdict"] == "falsified"
    assert m.evaluate_hypothesis_a([])["verdict"] == "unknown"


def _hb_trial(seed, high, online=0.04, frozen=0.01, rho=0.8):
    if not high:
        online, frozen, rho = 0.001, 0.0015, 0.0
    return {
        "seed": seed,
        "methods": {"oracle": {"full_late": {"permutation_invariant_ber": 0.0}}},
        "mechanism": {
            variant: {
                "online": {"full_late": {
                    "excess_pi_ber_vs_oracle": online,
                    "complex_scalar_nmse": 0.04 if high else 0.001,
                    "leakage_power_ratio": 0.04 if high else 0.001,
                }},
                "frozen": {"full_late": {
                    "excess_pi_ber_vs_oracle": frozen,
                    "complex_scalar_nmse": 0.01 if high else 0.001,
                    "leakage_power_ratio": 0.01 if high else 0.001,
                }},
                "fork": {
                    "spearman_online_displacement_vs_excess": rho,
                    "spearman_online_displacement_vs_oracle_pi": 0.1,
                    "oracle_synchronous": False,
                },
            }
            for variant in ("current", "standard")
        },
    }


def test_hypothesis_b_support_falsify_and_unknown():
    m = _load_module()
    trials = [
        _hb_trial(seed, True) for seed in m.HIGH_GAP_SEEDS
    ] + [
        _hb_trial(seed, False) for seed in m.LOW_GAP_SEEDS
    ]
    assert m.evaluate_hypothesis_b(trials)["verdict"] == "supported"

    falsified = json.loads(json.dumps(trials))
    for trial in falsified:
        trial["mechanism"]["standard"]["frozen"]["full_late"]["excess_pi_ber_vs_oracle"] = 0.039
    assert m.evaluate_hypothesis_b(falsified)["verdict"] == "falsified"
    assert m.evaluate_hypothesis_b([])["verdict"] == "unknown"


def test_hypothesis_b_constant_oracle_missing_or_nan_is_unknown_not_a_vote():
    m = _load_module()
    assert m._synchrony_state(None) is None
    assert m._synchrony_state(float("nan")) is None
    assert m._synchrony_state(0.69) is False
    assert m._synchrony_state(-0.7) is True

    trials = [
        _hb_trial(seed, True) for seed in m.HIGH_GAP_SEEDS
    ] + [
        _hb_trial(seed, False) for seed in m.LOW_GAP_SEEDS
    ]
    constant_oracle = json.loads(json.dumps(trials))
    constant_oracle[0]["mechanism"]["current"]["fork"]["oracle_synchronous"] = None
    assert m.evaluate_hypothesis_b(constant_oracle)["verdict"] == "unknown"

    missing = json.loads(json.dumps(trials))
    del missing[0]["mechanism"]["current"]["online"]["full_late"]["complex_scalar_nmse"]
    assert m.evaluate_hypothesis_b(missing)["verdict"] == "unknown"

    missing_oracle_rho = json.loads(json.dumps(trials))
    del missing_oracle_rho[0]["mechanism"]["current"]["fork"]["spearman_online_displacement_vs_oracle_pi"]
    assert m.evaluate_hypothesis_b(missing_oracle_rho)["verdict"] == "unknown"

    nonfinite = json.loads(json.dumps(trials))
    nonfinite[0]["mechanism"]["standard"]["fork"]["spearman_online_displacement_vs_excess"] = float("nan")
    assert m.evaluate_hypothesis_b(nonfinite)["verdict"] == "unknown"


def test_hypothesis_c_reports_isomorphic_capacity_and_cross_init_mismatch():
    m = _load_module()
    evidence = m.capacity_evidence(n_tap=11)
    assert evidence["cma_real_parameters"] == 88
    assert evidence["ml_real_parameters"] == 88
    assert evidence["four_complex_firs"] is True
    assert evidence["bias"] is False
    assert evidence["nonlinearity"] is False
    assert evidence["capacity_isomorphic"] is True
    assert evidence["ml_cross_center_actual"] == {"wxy": 1.0, "wyx": 1.0}
    assert evidence["ml_cross_center_comment_claim"] == 0.0
    assert evidence["initialization_mismatch_confound"] is True


def test_execute_seed_uses_generator_once_and_run_batch_checkpoints_each_seed(monkeypatch):
    m = _load_module()
    calls = {"generator": 0}
    arrays = tuple(np.ones(16, dtype=complex) for _ in range(4)) + (
        np.ones(16), np.zeros(16),
    )

    def generator(*args, **kwargs):
        calls["generator"] += 1
        return arrays

    def method_runner(shared, seed):
        assert shared == arrays
        return {"seed": seed, "methods": {}, "mechanism": {}}

    trial = m._execute_seed(1006, 1.0, 1.0, generator=generator, method_runner=method_runner)
    assert calls["generator"] == 1
    assert trial["shared_realization_seed"] == 1006

    payload = {"trials": []}
    monkeypatch.setattr(m, "_load_or_initialize", lambda: (payload, 1.0, 1.0))
    monkeypatch.setattr(
        m, "_execute_seed",
        lambda seed, a, b: {"seed": seed, "shared_realization_seed": seed},
    )
    saved = []
    monkeypatch.setattr(m, "save_q2_results", lambda data: saved.append(len(data["trials"])))
    monkeypatch.setattr(m, "exclusive_run_lock", lambda path: nullcontext())
    m.run_batch((1006, 1017, 1011))
    assert saved == [1, 2, 3]


def test_source_sha_map_covers_at_least_nine_dependencies():
    m = _load_module()
    names = set(m.source_sha256s())
    assert len(names) >= 9
    assert {
        "prompt013_swap_mechanism_q2.py",
        "prompt013_swap_quality_q1.py",
        "prompt013_swap_quality.json",
        "ml_long_seq_failure.py",
        "common/_cma.py",
        "common/_ml_equalizer.py",
        "common/_experiment.py",
        "common/_gg_time.py",
        "params.py",
    } <= names
