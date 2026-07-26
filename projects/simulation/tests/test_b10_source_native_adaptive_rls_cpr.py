"""Phase-A contract tests for T010.

Scientific source smoke and method behavior are intentionally deferred to
Phase B/C and remain explicitly skipped below.
"""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
from pathlib import Path

import numpy as np
import pytest
import yaml


SIM_ROOT = Path(__file__).resolve().parents[1]
PKG = SIM_ROOT / "explore" / "b10-source-native-adaptive-rls-cpr"


def _load_run_all():
    spec = importlib.util.spec_from_file_location("t010_run_all", PKG / "run_all.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _load_package_module(filename, name):
    spec = importlib.util.spec_from_file_location(name, PKG / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_phase_a_source_contract_encodes_pdf_identity():
    source = yaml.safe_load((PKG / "source-contract.yaml").read_text(encoding="utf-8"))
    rls = source["source_native_identity"]["rls"]
    assert rls["pilot_symbols"] == 128
    assert rls["indexing"] == "k=1..128 training; k>128 decision-directed"
    assert rls["h0"] == [0.0, 0.0]
    assert rls["p0"] == [[0.5, 0.0], [0.0, 0.5]]
    assert rls["delta"] == 2.0
    assert rls["units"] == "radians"
    assert rls["freeze_period_formula"] == "F=2*pi/h1_at_k128"
    assert (
        source["source_native_identity"]["phase_b_status"]
        == "SOURCE_IDENTITY_PASS_ACCEPTED"
    )
    assert source["authority"]["formal_decision"].endswith("decisions.md#D021")
    confirm = source["source_identity_smoke"]["current_confirm"]
    assert confirm["status"] == "PASS_AWAITING_SCIENCE_REVIEW"
    assert confirm["seed"] == 130003
    assert confirm["forgetting_factor"] == {
        "value": 0.99,
        "type": "IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN",
    }
    assert confirm["phase_c_authorized"] is False
    assert confirm["invocation_count"] == 1


def test_phase_a_rejects_proxy_db_without_actual_pooled_ber_crossings():
    contract = yaml.safe_load((PKG / "contract.yaml").read_text(encoding="utf-8"))
    assert (
        "Positive evidence relies on proxy dB without actual pooled-BER crossings."
        in contract["rejection_conditions"]
    )


def test_phase_a_pilot_manifest_sha_mapping_and_length():
    manifest = json.loads((PKG / "pilot-manifest.json").read_text(encoding="utf-8"))
    contract = yaml.safe_load((PKG / "contract.yaml").read_text(encoding="utf-8"))
    assert len(manifest["bits"]) == 512
    assert len(manifest["symbols"]) == 128
    assert manifest["mapping"] == "Gray 16-QAM: 00=-3,01=-1,11=+1,10=+3 per axis; /sqrt(10)"
    axis = {(0, 0): -3, (0, 1): -1, (1, 1): 1, (1, 0): 3}
    recomputed = []
    for offset in range(0, 512, 4):
        nibble = manifest["bits"][offset : offset + 4]
        recomputed.append(
            [
                axis[tuple(nibble[:2])] / np.sqrt(10),
                axis[tuple(nibble[2:])] / np.sqrt(10),
            ]
        )
    np.testing.assert_allclose(manifest["symbols"], recomputed, rtol=0.0, atol=1e-15)
    payload = {"bits": manifest["bits"], "symbols": manifest["symbols"]}
    digest = hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert digest == manifest["sha256"]
    assert digest == contract["pilot"]["manifest_sha256"]
    assert manifest["runtime_data_rng_independent"] is True


def test_phase_a_seed_census_is_elementwise_closed_and_disjoint():
    census = yaml.safe_load((PKG / "seed-census.yaml").read_text(encoding="utf-8"))
    current = census["t010"]
    assert current["invalid_development"] == [130001]
    assert current["canonical_only"] == [130002]
    assert current["source_smoke"] == [130003]
    assert current["validation"] == list(range(131001, 131006))
    assert current["test"] == list(range(132001, 132011))
    pools = [
        current["source_smoke"],
        current["validation"],
        current["test"],
        census["historical"]["t006"]["validation"],
        census["historical"]["t006"]["test"],
        census["historical"]["t008"]["validation"],
        census["historical"]["t008"]["test"],
        census["historical"]["t009"]["validation"],
        census["historical"]["t009"]["test"],
    ]
    for i, left in enumerate(pools):
        for right in pools[i + 1 :]:
            assert set(left).isdisjoint(right)


def test_phase_a_seed_census_reparses_historical_facts_and_contract():
    run_all = _load_run_all()
    checked = run_all.verify_seed_census()
    assert checked["source_smoke"] == [130003]
    assert checked["validation"] == list(range(131001, 131006))
    assert checked["test"] == list(range(132001, 132011))


def test_phase_a_t006_worker_log_seed_parser_requires_explicit_facts():
    run_all = _load_run_all()
    parsed = run_all.parse_t006_worker_log_seed_pools()
    assert parsed == {
        "validation": list(range(7600, 7605)),
        "test": list(range(7700, 7710)),
    }


def test_phase_a_t006_worker_log_seed_parser_rejects_arbitrary_numbers():
    run_all = _load_run_all()
    with pytest.raises(ValueError, match="exactly one explicit"):
        run_all.parse_t006_worker_log_seed_pools(
            "validation seeds 7600 7601 7602 7603 7604; "
            "test seeds 7700 7701 7702 7703 7704 7705 7706 7707 7708 7709"
        )


def test_phase_a_metric_contract_data_only_and_q2_boundaries():
    run_all = _load_run_all()
    row = run_all.make_metric_row(bit_errors=7, denominator=4 * (25_000 - 128))
    assert row["ber"] == pytest.approx(7 / (4 * (25_000 - 128)))
    zero = run_all.make_metric_row(bit_errors=0, denominator=100)
    assert zero["ber_bound"] == 0.005
    assert np.isfinite(zero["q2_db"])
    collapsed = run_all.make_metric_row(bit_errors=50, denominator=100)
    assert collapsed["q2_db"] is None


def test_phase_a_q2_conversion_exact_zero_bound_and_above_half_boundary():
    run_all = _load_run_all()
    denominator = 100
    q2 = run_all.ber_to_q2_db(0.0, denominator=denominator)
    expected = 20.0 * np.log10(np.sqrt(2.0) * run_all.erfcinv(2.0 * (0.5 / denominator)))
    assert np.isfinite(q2)
    assert q2 == pytest.approx(expected, rel=0.0, abs=1e-12)
    assert run_all.ber_to_q2_db(0.500001, denominator=denominator) is None


def test_phase_b_shared_realization_manifest_rng_and_canonical_limit():
    shared_mod = _load_package_module("shared_realization.py", "t010_shared")
    from common._dual_pol_channel import generate_shared_realization_dp
    from common._modulation import qam16_mod

    kwargs = dict(
        n_symbols=4096,
        symbol_rate=2.5e9,
        esn0_db=20.0,
        linewidth_hz=0.0,
        cfo_hz=0.0,
        alpha=11.6,
        beta=10.1,
        greenwood_hz=100.0,
    )
    first = shared_mod.generate_shared_b10_realization(seed=130001, **kwargs)
    second = shared_mod.generate_shared_b10_realization(seed=130002, **kwargs)
    np.testing.assert_array_equal(first["tx"][:128], second["tx"][:128])
    assert not np.array_equal(first["data_bits"], second["data_bits"])
    assert first["pilot_symbols_source"] == "pilot-manifest.json"
    assert first["single_pol"] is True
    assert first["data_mask"].sum() == 4096 - 128
    np.testing.assert_allclose(first["tx"][128:], qam16_mod(first["data_bits"]))

    local = shared_mod.generate_shared_b10_realization(
        seed=777,
        n_symbols=4096,
        symbol_rate=2.5e9,
        esn0_db=20.0,
        linewidth_hz=0.0,
        cfo_hz=0.0,
        alpha=11.6,
        beta=10.1,
        greenwood_hz=100.0,
        pilot_enabled=False,
    )
    canonical = generate_shared_realization_dp(
        N=4096,
        alpha=11.6,
        beta=10.1,
        f_g=100.0,
        sop_rate=0.0,
        seed=777,
        gamma_bar=100.0,
        t_s=1 / 2.5e9,
        modulation="qam16",
    )
    np.testing.assert_array_equal(local["bits"], canonical["bitsX"])
    np.testing.assert_allclose(local["tx"], canonical["sX"])
    np.testing.assert_allclose(local["gg_envelope"], canonical["h"])
    assert np.mean(np.abs(local["noise"]) ** 2) == pytest.approx(0.01, rel=0.08)
    np.testing.assert_allclose(local["noiseless_rx"], np.sqrt(local["gg_envelope"]) * local["tx"])


def test_phase_b_source_native_rls_lifecycle_noiseless_positive_cfo():
    shared_mod = _load_package_module("shared_realization.py", "t010_shared_rls")
    rls_mod = _load_package_module("source_native_rls.py", "t010_rls")
    shared = shared_mod.generate_shared_b10_realization(
        seed=130001,
        n_symbols=4096,
        symbol_rate=28e9,
        esn0_db=120.0,
        linewidth_hz=0.0,
        cfo_hz=1e9,
        use_gg=False,
    )
    result = rls_mod.run_source_native_rls(shared["rx"], forgetting_factor=0.999)
    assert result["training_symbols"] == 128
    assert result["switch_index_zero_based"] == 128
    assert result["period_freeze_count"] == 1
    assert result["h_initial"] == [0.0, 0.0]
    np.testing.assert_allclose(result["p_initial"], np.eye(2) * 0.5)
    assert result["units"] == "radians"
    assert result["state_finite"] is True
    assert result["estimated_cfo_hz"] > 0
    assert abs(result["estimated_cfo_hz"] / 1e9 - 1.0) < 0.01
    assert len(result["errors"]) == len(shared["rx"])
    assert len(result["corrected"]) == len(shared["rx"])


def test_phase_b_source_smoke_contract_is_exact_and_source_only():
    run_all = _load_run_all()
    assert run_all.SOURCE_SMOKE_CONFIG == {
        "symbol_rate": 28e9,
        "n_symbols": 25_000,
        "esn0_db": 26.0,
        "linewidth_hz": 50e3,
        "cfo_hz": [1e9, 10e9],
        "seed": 130003,
    }
    assert run_all.SOURCE_SMOKE_FORGETTING_FACTOR == 0.99
    assert (
        run_all.SOURCE_SMOKE_FORGETTING_FACTOR_TYPE
        == "IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN"
    )
    assert callable(run_all.run_source_smoke)


def test_phase_b_synthetic_residual_direction_operational_sign():
    rls_mod = _load_package_module("source_native_rls.py", "t010_rls_residual")
    decision = 1.0 + 1.0j
    true_positive_residual = 0.2
    derotated = decision * np.exp(1j * true_positive_residual)
    old_literal = np.angle(decision) - np.angle(derotated)
    operational = rls_mod.operational_residual(derotated, decision)
    assert old_literal < 0.0
    assert operational == pytest.approx(true_positive_residual)
    predicted = 0.1
    assert predicted + operational > predicted


def test_phase_b_confirm_artifact_1_10ghz_ber_gate_is_read_only():
    run_all = _load_run_all()
    run_all.run_source_smoke = lambda: (_ for _ in ()).throw(
        AssertionError("artifact gate must never invoke the smoke runner")
    )
    payload = run_all.read_source_smoke_gate()
    assert payload["config"]["seed"] == 130003
    assert payload["forgetting_factor"]["value"] == 0.99
    assert payload["verdict"] == "PASS"
    assert {cell["cfo_hz"] for cell in payload["cells"]} == {1e9, 10e9}
    for cell in payload["cells"]:
        assert cell["p1"]["ber"] < 3.8e-3
        assert cell["pass"] is True


def test_phase_c2_authorization_migration_preserves_confirm_and_c1_history():
    source = yaml.safe_load((PKG / "source-contract.yaml").read_text(encoding="utf-8"))
    assert source["authority"]["formal_decision"].endswith("decisions.md#D021")
    assert source["source_native_identity"]["phase_b_status"] == "SOURCE_IDENTITY_PASS_ACCEPTED"
    confirm = source["source_identity_smoke"]["current_confirm"]
    assert confirm["status"] == "PASS_AWAITING_SCIENCE_REVIEW"
    assert confirm["phase_c_authorized"] is False
    assert confirm["invocation_count"] == 1
    assert source["current_authorization"] == {
        "formal_decision": ".sessions/2026-07-06-step4a-mve-execution/decisions.md#D021",
        "phase_c_status": "C2_AUTHORIZED_VALIDATION_ONLY",
        "validation_authorized": True,
        "heldout_authorized": False,
        "mission_method_delta": "NONE",
    }
    assert source["phase_c1_acceptance"]["legacy_debt"] == (
        "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT"
    )
    freeze = source["phase_c1_method_contract"]["candidate_arm_freeze"]
    assert freeze["arms"] == ["P2_INNOVATION_FREEZE", "P3_BOUNDED_ADAPTIVE_FORGETTING"]
    assert freeze["separate_global_freeze_required"] is True
    assert freeze["per_cell_or_per_seed_best_of_prohibited"] is True


def test_phase_c1_source_smoke_is_sealed_before_realization(monkeypatch):
    run_all = _load_run_all()
    monkeypatch.setattr(
        run_all,
        "_load_local",
        lambda *_: (_ for _ in ()).throw(AssertionError("realization must not load")),
    )
    with pytest.raises(RuntimeError, match="sealed"):
        run_all.run_source_smoke()


def test_phase_c1_source_gate_recomputes_only_persisted_fields():
    run_all = _load_run_all()
    audit = run_all.recompute_source_smoke_gate()
    assert audit["mode"] == "READ_ONLY_RECOMPUTATION"
    assert "verdict" not in audit
    assert audit["evidence_audit_status"] == "RECOMPUTABLE_FIELDS_MATCH"
    assert audit["scientific_verdict"] == "NOT_RECOMPUTED"
    assert audit["stored_verdict"] == "PASS"
    assert audit["stored_closure_verified"] is True
    assert audit["recomputable_fields"] == [
        "bit_errors",
        "denominator",
        "ber",
        "q2_db",
        "cfo_relative_error",
        "positive_cfo",
        "cfo_relative_error_le_5pct",
        "ber_improved",
        "q2_improved",
        "ber_below_hd_fec",
    ]
    assert audit["legacy_non_recomputable"] == {
        "finite_state": "LEGACY_NON_RECOMPUTABLE_PHASE_B_P2",
        "switch_at_128": "LEGACY_NON_RECOMPUTABLE_PHASE_B_P2",
        "period_frozen_once": "LEGACY_NON_RECOMPUTABLE_PHASE_B_P2",
        "positive_phase_slope": "LEGACY_NON_RECOMPUTABLE_PHASE_B_P2",
    }


def test_phase_c1_p2_p3_and_cheap_have_direct_information_increment():
    methods = _load_package_module("methods.py", "t010_methods_direct")
    n = 512
    base = np.ones(n, dtype=complex) * (1 + 1j) / np.sqrt(2)
    burst = base.copy()
    burst[200:240] *= np.exp(1j * 0.7)
    faded = base.copy()
    faded[200:240] *= 0.05

    p2_base = methods.run_innovation_freeze(base, forgetting_factor=0.99, threshold=0.11)
    p2_burst = methods.run_innovation_freeze(burst, forgetting_factor=0.99, threshold=0.11)
    assert not np.array_equal(p2_base["update_mask"], p2_burst["update_mask"])

    p3_base = methods.run_adaptive_forgetting(
        base, lambda_min=0.95, lambda_max=0.999, ema_alpha=0.2, innovation_scale=2.0
    )
    p3_burst = methods.run_adaptive_forgetting(
        burst, lambda_min=0.95, lambda_max=0.999, ema_alpha=0.2, innovation_scale=2.0
    )
    assert not np.array_equal(p3_base["lambda_path"], p3_burst["lambda_path"])
    assert np.all((p3_burst["lambda_path"] >= 0.95) & (p3_burst["lambda_path"] <= 0.999))
    assert p3_burst["lambda_path"][200] == pytest.approx(p3_base["lambda_path"][200])
    assert p3_burst["lambda_path"][201] != pytest.approx(p3_base["lambda_path"][201])

    cheap_base = methods.run_amplitude_freeze(base, forgetting_factor=0.99, threshold=0.2)
    cheap_faded = methods.run_amplitude_freeze(faded, forgetting_factor=0.99, threshold=0.2)
    assert not np.array_equal(cheap_base["update_mask"], cheap_faded["update_mask"])
    assert not np.array_equal(p2_burst["update_mask"], cheap_faded["update_mask"])


def test_phase_c1_deployable_methods_have_no_truth_or_future_inputs():
    methods = _load_package_module("methods.py", "t010_methods_boundary")
    for name in ("run_innovation_freeze", "run_adaptive_forgetting", "run_amplitude_freeze"):
        signature = inspect.signature(getattr(methods, name))
        forbidden = {"tx", "bits", "true_phase", "true_cfo", "future", "seed"}
        assert forbidden.isdisjoint(signature.parameters)


def test_phase_c1_conventional_arms_share_4opm_frequency_responsibility():
    baselines = _load_package_module("baselines.py", "t010_baselines")
    n = 4096
    k = np.arange(n)
    fs = 2.5e9
    tx = np.tile(np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2), n // 4)
    rx = tx * np.exp(1j * 2 * np.pi * 10e6 * k / fs)
    bps = baselines.run_4opm_bps(rx, symbol_rate=fs, test_phases=32, window=31)
    dpll = baselines.run_4opm_dd_dpll(rx, symbol_rate=fs, omega_n=8e6)
    assert bps["coarse_frequency_hz"] == pytest.approx(dpll["coarse_frequency_hz"])
    assert abs(bps["coarse_frequency_hz"] - 10e6) < 1e6
    assert np.all(np.isfinite(bps["corrected"]))
    assert np.all(np.isfinite(dpll["corrected"]))


def test_phase_c1_clean_noiseless_shared_realization_sanity():
    shared_mod = _load_package_module("shared_realization.py", "t010_shared_c1")
    methods = _load_package_module("methods.py", "t010_methods_clean")
    shared = shared_mod.generate_shared_b10_realization(
        seed=130002,
        n_symbols=1024,
        symbol_rate=2.5e9,
        esn0_db=120.0,
        linewidth_hz=0.0,
        cfo_hz=1e6,
        use_gg=False,
    )
    outputs = [
        methods.run_innovation_freeze(shared["rx"], forgetting_factor=0.99, threshold=10.0),
        methods.run_adaptive_forgetting(
            shared["rx"], lambda_min=0.99, lambda_max=0.999, ema_alpha=0.1, innovation_scale=1.0
        ),
        methods.run_amplitude_freeze(shared["rx"], forgetting_factor=0.99, threshold=0.01),
    ]
    assert all(result["shared_rx_identity"] is shared["rx"] for result in outputs)
    assert all(result["state_finite"] for result in outputs)


def test_v019_nonfinite_input_cannot_report_finite_state():
    methods = _load_package_module("methods.py", "t010_methods_nonfinite")
    shared_mod = _load_package_module("shared_realization.py", "t010_shared_nonfinite")
    shared = shared_mod.generate_shared_b10_realization(
        seed=130002,
        n_symbols=512,
        symbol_rate=2.5e9,
        esn0_db=120.0,
        linewidth_hz=0.0,
        cfo_hz=1e6,
        use_gg=False,
    )
    poisoned = shared["rx"].copy()
    poisoned[300] = complex(np.nan, 0.0)
    result = methods.run_innovation_freeze(
        poisoned, forgetting_factor=0.99, threshold=0.0
    )
    assert result["state_finite"] is False
    assert not np.all(np.isfinite(result["corrected"]))
    assert not np.all(np.isfinite(result["normalized_innovation"]))


@pytest.mark.parametrize(
    ("name", "kwargs"),
    [
        ("run_innovation_freeze", {"forgetting_factor": 0.99, "threshold": -1.0}),
        ("run_innovation_freeze", {"forgetting_factor": 0.99, "threshold": np.nan}),
        ("run_amplitude_freeze", {"forgetting_factor": 0.99, "threshold": np.inf}),
        (
            "run_adaptive_forgetting",
            {
                "lambda_min": 0.95,
                "lambda_max": 0.999,
                "ema_alpha": 0.0,
                "innovation_scale": 1.0,
            },
        ),
        (
            "run_adaptive_forgetting",
            {
                "lambda_min": 0.95,
                "lambda_max": 0.999,
                "ema_alpha": 0.1,
                "innovation_scale": np.nan,
            },
        ),
        (
            "run_adaptive_forgetting",
            {
                "lambda_min": np.nan,
                "lambda_max": 0.999,
                "ema_alpha": 0.1,
                "innovation_scale": 1.0,
            },
        ),
    ],
)
def test_v019_method_parameter_domains_reject_nonfinite_or_illegal(name, kwargs):
    methods = _load_package_module("methods.py", f"t010_methods_domain_{name}")
    with pytest.raises(ValueError):
        getattr(methods, name)(np.ones(256, dtype=complex), **kwargs)


def test_v019_conventional_identity_rejects_nonfrozen_parameters():
    baselines = _load_package_module("baselines.py", "t010_baselines_identity")
    rx = np.ones(512, dtype=complex)
    with pytest.raises(ValueError, match="exactly 32"):
        baselines.run_4opm_bps(rx, symbol_rate=2.5e9, test_phases=16, window=31)
    with pytest.raises(ValueError, match="symbol_rate"):
        baselines.run_4opm_dd_dpll(rx, symbol_rate=28e9, omega_n=8e6)


def test_v019_all_c1_arms_share_nontrivial_clean_realization_and_mask():
    from common._modulation import qam16_demod

    shared_mod = _load_package_module("shared_realization.py", "t010_shared_all_arms")
    source = _load_package_module("source_native_rls.py", "t010_source_all_arms")
    methods = _load_package_module("methods.py", "t010_methods_all_arms")
    baselines = _load_package_module("baselines.py", "t010_baselines_all_arms")
    shared = shared_mod.generate_shared_b10_realization(
        seed=130002,
        n_symbols=2048,
        symbol_rate=2.5e9,
        esn0_db=120.0,
        linewidth_hz=0.0,
        cfo_hz=1e6,
        use_gg=False,
    )
    rx = shared["rx"]
    arms = {
        "P1": source.run_source_native_rls(
            rx, forgetting_factor=0.99, symbol_rate=2.5e9
        ),
        "P2": methods.run_innovation_freeze(
            rx, forgetting_factor=0.99, threshold=10.0
        ),
        "P3": methods.run_adaptive_forgetting(
            rx,
            lambda_min=0.99,
            lambda_max=0.999,
            ema_alpha=0.1,
            innovation_scale=1.0,
        ),
        "cheap": methods.run_amplitude_freeze(
            rx, forgetting_factor=0.99, threshold=0.01
        ),
        "BPS": baselines.run_4opm_bps(
            rx, symbol_rate=2.5e9, test_phases=32, window=31
        ),
        "DPLL": baselines.run_4opm_dd_dpll(
            rx, symbol_rate=2.5e9, omega_n=8e6
        ),
    }
    assert shared["data_mask"].sum() == 2048 - 128
    denominator = 4 * int(shared["data_mask"].sum())
    for name, result in arms.items():
        corrected = result["corrected"]
        assert len(corrected) == len(rx), name
        assert np.all(np.isfinite(corrected)), name
        errors = int(
            np.count_nonzero(qam16_demod(corrected[shared["data_mask"]]) != shared["data_bits"])
        )
        assert errors / denominator <= 0.01, name
    assert arms["BPS"]["coarse_frequency_hz"] == pytest.approx(
        arms["DPLL"]["coarse_frequency_hz"]
    )
    for func in (
        source.run_source_native_rls,
        methods.run_innovation_freeze,
        methods.run_adaptive_forgetting,
        methods.run_amplitude_freeze,
        baselines.run_4opm_bps,
        baselines.run_4opm_dd_dpll,
    ):
        assert {"tx", "bits", "true_phase", "true_cfo", "future"}.isdisjoint(
            inspect.signature(func).parameters
        )


def test_v025_contract_is_c2_validation_only_and_preserves_c1_acceptance():
    contract = yaml.safe_load((PKG / "contract.yaml").read_text(encoding="utf-8"))
    assert contract["phase"] == "C2"
    assert contract["execution_status"] == "C2_VALIDATION_AUTHORIZED"
    assert contract["authorization"]["validation"] is True
    assert contract["authorization"]["heldout"] is False
    assert contract["authorization"]["performance_conclusion"] is False
    assert contract["phase_c1_acceptance"]["legacy_debt"] == (
        "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT"
    )


def test_c2_expected_keys_and_setting_index_mapping_are_canonical():
    run_all = _load_run_all()
    settings = run_all.c2_setting_grid()
    assert [len(family) for family in settings] == [3, 9, 3, 9, 3, 3]
    assert settings[1][0] == {
        "forgetting_factor": 0.98,
        "threshold": 0.05,
    }
    assert settings[1][-1] == {
        "forgetting_factor": 0.999,
        "threshold": 0.20,
    }
    keys = run_all.expected_row_keys()
    assert len(keys) == 2250
    assert len({tuple(key) for key in keys}) == 2250
    assert keys[0] == [0, 0, 0, 0, 0]
    assert keys[29] == [0, 0, 0, 5, 2]
    assert keys[30] == [0, 0, 1, 0, 0]
    assert keys[-1] == [2, 4, 4, 5, 2]


def test_c2_checkpoint_requires_complete_strict_prefix_cells():
    run_all = _load_run_all()
    keys = run_all.expected_row_keys()
    rows = [{"row_key": key} for key in keys[:30]]
    assert run_all.validate_checkpoint_rows(rows) == 30
    with pytest.raises(run_all.StaleCheckpointError):
        run_all.validate_checkpoint_rows(rows[:-1])
    duplicate = [dict(row) for row in rows]
    duplicate[-1]["row_key"] = duplicate[-2]["row_key"]
    with pytest.raises(run_all.StaleCheckpointError):
        run_all.validate_checkpoint_rows(duplicate)
    gap = [dict(row) for row in rows]
    gap[10]["row_key"] = keys[31]
    with pytest.raises(run_all.StaleCheckpointError):
        run_all.validate_checkpoint_rows(gap)


def test_c2_hash_bundle_has_exact_17_contract_paths():
    run_all = _load_run_all()
    bundle = run_all.source_hash_bundle()
    assert len(bundle) == 17
    assert list(bundle) == run_all.C2_HASH_PATHS
    assert all(len(value) == 64 for value in bundle.values())


def test_c2_exact_tie_selects_bps_independent_of_iteration_order():
    run_all = _load_run_all()
    score = (0, 0, 0, 123, 0)
    forward = {"4OPM_BPS": score, "4OPM_CONTINUOUS_DD_DPLL": score}
    reverse = dict(reversed(list(forward.items())))
    assert run_all.select_bstar(forward) == "4OPM_BPS"
    assert run_all.select_bstar(reverse) == "4OPM_BPS"


def test_c2_atomic_checkpoint_replace_failure_preserves_old_target(tmp_path, monkeypatch):
    run_all = _load_run_all()
    target = tmp_path / "validation-raw.json"
    target.write_bytes(b"old-target-bytes")
    monkeypatch.setattr(
        run_all.os,
        "replace",
        lambda *_: (_ for _ in ()).throw(OSError("simulated replace failure")),
    )
    with pytest.raises(OSError, match="simulated replace failure"):
        run_all.atomic_save_validation({"rows": []}, target)
    assert target.read_bytes() == b"old-target-bytes"
    assert list(tmp_path.glob("*.tmp")) == []


def test_c2_setting_score_and_primary_freeze_use_full_lexicographic_chain():
    run_all = _load_run_all()
    rows = [
        {"state_finite": True, "ber": 0.1, "bit_errors": 10, "setting_index": 0},
        {"state_finite": False, "ber": 0.0, "bit_errors": 0, "setting_index": 1},
        {"state_finite": True, "ber": 0.0038, "bit_errors": 3, "setting_index": 0},
    ]
    assert run_all.setting_score(rows[:1], 0) == (0, 0, 1, 10, 0)
    assert run_all.setting_score(rows[1:2], 1) == (1, 0, 0, 0, 1)
    assert run_all.setting_score(rows[2:], 0) == (0, 0, 0, 3, 0)
    assert run_all.select_primary({"P2": (0, 0, 0, 10, 0), "P3": (0, 0, 0, 10, 0)}) == "P2"


def test_c2_pooled_zero_error_bound_and_common_window_equality_rule():
    run_all = _load_run_all()
    assert run_all.pooled_ber([{"bit_errors": 0, "denominator": 1000}]) == {
        "bit_errors": 0,
        "denominator": 1000,
        "pooled_raw_ber": 0.0,
        "effective_ber": 0.0005,
    }
    curves = {
        arm: [0.02, 0.0038, 0.001, 0.0005, 0.0001]
        for arm in ("PRIMARY_METHOD", "P1_FIXED", "CHEAP_AMPLITUDE_FREEZE", "BSTAR")
    }
    frozen = run_all.freeze_snr_window(curves)
    assert frozen["common_bracket"] == [0, 1]
    assert frozen["window_indices"] == [0, 1, 2]
    assert frozen["marker"] == "COMMON_VALIDATION_CROSSING"


def test_c2_no_common_crossing_marks_boundary_only():
    run_all = _load_run_all()
    curves = {
        "PRIMARY_METHOD": [0.02, 0.01, 0.006, 0.004, 0.003],
        "P1_FIXED": [0.03, 0.02, 0.01, 0.006, 0.004],
        "CHEAP_AMPLITUDE_FREEZE": [0.02, 0.01, 0.006, 0.003, 0.001],
        "BSTAR": [0.03, 0.02, 0.01, 0.004, 0.003],
    }
    frozen = run_all.freeze_snr_window(curves)
    assert frozen["common_bracket"] is None
    assert frozen["marker"] == "NO_COMMON_VALIDATION_CROSSING"
    assert len(frozen["window_indices"]) == 3


def test_c2_resume_rejects_stale_hash_and_preserves_existing_prefix():
    run_all = _load_run_all()
    keys = run_all.expected_row_keys()
    rows = [{"row_key": key, "value": index} for index, key in enumerate(keys[:30])]
    bundle = run_all.source_hash_bundle()
    assert run_all.validate_checkpoint_payload({"rows": rows, "source_hashes": bundle}) == 30
    stale = dict(bundle)
    stale[next(iter(stale))] = "0" * 64
    with pytest.raises(run_all.StaleCheckpointError):
        run_all.validate_checkpoint_payload({"rows": rows, "source_hashes": stale})
    prefix_sha = run_all.canonical_rows_sha256(rows)
    combined = run_all.append_complete_cell(rows, [
        {"row_key": key, "value": index + 30}
        for index, key in enumerate(keys[30:60])
    ])
    assert combined[:30] == rows
    assert run_all.canonical_rows_sha256(combined[:30]) == prefix_sha


def test_c2_aggregate_gate_rejects_partial_matrix():
    run_all = _load_run_all()
    with pytest.raises(ValueError, match="2250"):
        run_all.aggregate_validation([])


def test_c2_validation_cell_runner_emits_one_complete_canonical_cell():
    from common._modulation import qam16_mod

    run_all = _load_run_all()
    data_bits = np.tile([0, 0, 0, 0], 4)
    corrected = np.concatenate((np.ones(128, dtype=complex), qam16_mod(data_bits)))
    shared = {
        "rx": corrected.copy(),
        "data_bits": data_bits,
        "data_mask": np.arange(len(corrected)) >= 128,
    }
    identities = []

    def fake_runner(shared_arg, arm_index, setting):
        identities.append(shared_arg is shared)
        return {
            "corrected": corrected,
            "state_finite": True,
            "update_rate": 1.0,
            "freeze_rate": 0.0,
            "innovation_stats": {},
        }

    rows = run_all.validation_cell_rows(
        shared,
        gg_index=0,
        snr_index=0,
        seed_index=0,
        arm_runner=fake_runner,
    )
    assert len(rows) == 30
    assert all(identities)
    assert [row["row_key"] for row in rows] == run_all.expected_row_keys()[:30]
    assert all(row["denominator"] == len(data_bits) for row in rows)
    assert all(row["bit_errors"] == 0 for row in rows)


def test_c2_complete_aggregate_freezes_settings_bstar_primary_and_three_gg_windows():
    run_all = _load_run_all()
    rows = []
    for key in run_all.expected_row_keys():
        gg, snr, seed, arm, setting = key
        errors = max(0, 30 - 7 * snr) + setting
        rows.append({
            "row_key": key,
            "state_finite": True,
            "bit_errors": errors,
            "denominator": 1000,
            "ber": errors / 1000,
        })
    result = run_all.aggregate_validation(rows)
    assert result["primary_method"] == "P2"
    assert result["bstar"] == "4OPM_BPS"
    assert set(result["snr_freeze"]) == {"weak", "moderate", "strong"}
    assert all(len(item["window_indices"]) == 3 for item in result["snr_freeze"].values())
    assert result["legacy_debt"] == "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT"


def test_c2_validation_runner_checkpoints_only_after_one_complete_cell(tmp_path, monkeypatch):
    run_all = _load_run_all()
    calls = []
    fake_shared_module = type("Shared", (), {
        "generate_shared_b10_realization": staticmethod(
            lambda **kwargs: calls.append(kwargs) or {"fake": True}
        )
    })
    monkeypatch.setattr(run_all, "_load_local", lambda *_: fake_shared_module)
    monkeypatch.setattr(
        run_all,
        "validation_cell_rows",
        lambda shared, gg_index, snr_index, seed_index: [
            {
                "row_key": key,
                "state_finite": True,
                "bit_errors": 0,
                "denominator": 100,
                "ber": 0.0,
            }
            for key in run_all.expected_row_keys()[:30]
        ],
    )
    target = tmp_path / "validation-raw.json"
    result = run_all.run_validation(max_cells=1, artifact_path=target)
    assert result["row_count"] == 30
    assert len(calls) == 1
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert len(payload["rows"]) == 30
    assert payload["legacy_debt"] == "PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT"


def test_v020_pi_over_2_clean_ambiguity_is_pilot_only_and_phase_consistent():
    from common._modulation import qam16_demod

    shared_mod = _load_package_module("shared_realization.py", "t010_shared_v020")
    baselines = _load_package_module("baselines.py", "t010_baselines_v020")
    shared = shared_mod.generate_shared_b10_realization(
        seed=130002,
        n_symbols=2048,
        symbol_rate=2.5e9,
        esn0_db=120.0,
        linewidth_hz=0.0,
        cfo_hz=1e6,
        use_gg=False,
    )
    rx = shared["rx"] * np.exp(1j * np.pi / 2.0)
    arms = {
        "BPS": baselines.run_4opm_bps(
            rx, symbol_rate=2.5e9, test_phases=32, window=31
        ),
        "DPLL": baselines.run_4opm_dd_dpll(
            rx, symbol_rate=2.5e9, omega_n=8e6
        ),
    }
    denominator = 4 * int(shared["data_mask"].sum())
    for name, result in arms.items():
        errors = int(
            np.count_nonzero(
                qam16_demod(result["corrected"][shared["data_mask"]])
                != shared["data_bits"]
            )
        )
        assert errors == 0, name
        coarse_omega = (
            2.0 * np.pi * result["coarse_frequency_hz"] / 2.5e9
        )
        coarse = rx * np.exp(-1j * coarse_omega * np.arange(len(rx)))
        np.testing.assert_allclose(
            result["corrected"],
            coarse * np.exp(-1j * result["phase_estimate"]),
            rtol=0.0,
            atol=1e-12,
            err_msg=name,
        )
    assert arms["BPS"]["coarse_frequency_hz"] == pytest.approx(
        arms["DPLL"]["coarse_frequency_hz"]
    )
    for func in (baselines.run_4opm_bps, baselines.run_4opm_dd_dpll):
        assert {"tx", "bits", "true_phase", "true_cfo", "future"}.isdisjoint(
            inspect.signature(func).parameters
        )
