import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest


SEAM = Path(__file__).resolve().parents[1]


def _load(name):
    if str(SEAM) not in sys.path:
        sys.path.insert(0, str(SEAM))
    path = SEAM / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _json(name):
    return json.loads((SEAM / name).read_text(encoding="utf-8"))


def test_tuning_manifest_freezes_disjoint_grid_role_mapping_and_hashes():
    manifest = _json("b2_tuning_manifest.json")
    assert manifest["schema_version"] == "t086.b2-tuning-manifest.v1"
    assert (manifest["control_epoch"], manifest["mission_checkpoint"]) == (27, "CP027")
    assert manifest["grid"] == {
        "scenes": ["weak", "moderate", "strong"],
        "pilot_symbols_per_polarization": [2, 4, 8, 16],
        "snr_db": [15.0, 25.0, 35.0],
        "tau_candidates": [0.0, 0.25, 0.5, 0.75, 1.0],
        "windows_per_scene": 32,
        "payload_symbols_per_polarization": 4096,
        "max_pilots": 16,
    }
    population = manifest["population"]
    partitions = [
        {population["tuning_preflight_smoke_id"]},
        set(range(21000, 21032)),
        {population["formal_structure_smoke_id"]},
        {19999, *range(20000, 20064)},
        set(range(30000, 30128)),
    ]
    assert all(a.isdisjoint(b) for i, a in enumerate(partitions) for b in partitions[i + 1 :])
    assert {role: value["runtime_arm"] for role, value in manifest["runtime_roles"].items()} == {
        "B0": "B0", "B2_TUNED": "B2", "C4_FWD": "C4",
        "B3_PSC": "B3_PSC", "O1": "O1_TRUTH_ONLY",
    }
    assert manifest["runtime_roles"]["B3_PSC"]["parameter"] == 1.0
    assert manifest["base_commit"] == subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert manifest["t085_bindings"]["raw_sha256"] == hashlib.sha256(
        (SEAM / "corrected_anchor_raw.json").read_bytes()
    ).hexdigest()


def test_scientific_schema_freezes_cells_mismatch_statistics_grade_and_future_lock():
    schema = _json("ch4_scientific_manifest_schema.json")
    assert schema["snr_grid_db"] == [float(value) for value in range(5, 42, 2)]
    assert schema["formal_population"] == {
        "latent_ids": {"start": 30000, "stop_inclusive": 30127},
        "clusters": 128,
        "cluster_key": "latent_id",
        "shared_across_all_slices_snr_np_and_mismatch": True,
    }
    mismatch = schema["slices"]["mismatch"]
    assert mismatch["delta"] == [0.0, 0.05, 0.1, 0.2, 0.3, 0.4]
    assert mismatch["component_usage"] == {
        "Q": "channel_q", "R": "mismatch_right", "gain": "gg_gain",
        "unused_but_retained": "mismatch_left",
    }
    assert schema["whole_curve_bootstrap"]["seed"] == 2026083007
    assert schema["whole_curve_bootstrap"]["valid_gain_replicates_minimum"] == 4500
    assert list(schema["grade"]) == ["A", "B", "C", "F", "invalid", "chapter_gate"]
    lock = schema["execution_lock_interface"]
    assert lock["status"] == "PENDING_T087_IMPLEMENTATION"
    assert lock["future_code_hash_values"] is None
    assert set(lock["required_bindings_before_first_formal_cell"]) == {
        "scientific_manifest_sha256", "formal_runner_sha256", "formal_reducer_sha256",
        "formal_tests_sha256", "base_commit", "environment_snapshot",
    }
    assert schema["base_commit"] == _json("b2_tuning_manifest.json")["base_commit"]
    assert set(schema["frozen_code_hashes"]) == {
        "production_core.py", "common/_modulation.py", "scaled_unitary.py"
    }
    assert schema["params_authority"]["path"] == "projects/simulation/params.py"
    assert schema["cell_level_bootstrap"] == {
        "rng": "PCG64", "seed": 2026083008, "resamples": 5000, "confidence": 0.95,
        "stream_rule": "reset seed for each named (scene,Np,SNR,variant) comparison",
        "cluster_rule": "128 paired latent_id clusters within one (scene,Np) slice",
        "estimand": "per-latent BER_variant minus BER_B2_TUNED",
        "scope": "grade C only; never pooled across scene",
    }


def test_jeffreys_objective_and_exact_tie_select_smaller_tau():
    reducer = _load("b2_tuning_reducer")
    counts = {
        0.0: {15.0: (10, 1000), 25.0: (2, 1000), 35.0: (0, 1000)},
        0.25: {15.0: (10, 1000), 25.0: (2, 1000), 35.0: (0, 1000)},
        0.5: {15.0: (20, 1000), 25.0: (4, 1000), 35.0: (1, 1000)},
        0.75: {15.0: (30, 1000), 25.0: (6, 1000), 35.0: (2, 1000)},
        1.0: {15.0: (40, 1000), 25.0: (8, 1000), 35.0: (3, 1000)},
    }
    objectives = {tau: reducer.mean_log10_jeffreys(rows) for tau, rows in counts.items()}
    assert reducer.select_tau(objectives) == 0.0
    expected = np.mean([np.log10((e + 0.5) / (b + 1)) for e, b in counts[0.0].values()])
    assert objectives[0.0] == pytest.approx(expected, abs=0.0)
    with pytest.raises(ValueError, match="exactly"):
        reducer.select_tau(dict(list(objectives.items())[:-1]))


@pytest.mark.parametrize("bad", [{15.0: (1, 0)}, {15.0: (-1, 100)}, {15.0: (101, 100)}, {15.0: (1, 100), 25.0: (1, 100)}])
def test_objective_fails_closed_instead_of_dropping_or_assigning_infinity(bad):
    reducer = _load("b2_tuning_reducer")
    with pytest.raises(ValueError):
        reducer.mean_log10_jeffreys(bad)


def test_development_dominance_terminal_uses_all_twelve_cells_and_one_strict_comparison():
    reducer = _load("b2_tuning_reducer")
    cells = {}
    for scene in ("weak", "moderate", "strong"):
        for n_pilots in (2, 4, 8, 16):
            cells[(scene, n_pilots)] = {"B2_TUNED": -3.0, "C4_FWD": -2.9, "B3_PSC": -3.0}
    assert reducer.development_terminal(cells) == "TUNED_BASELINE_DOMINATES_DEVELOPMENT"
    cells[("strong", 16)]["C4_FWD"] = -3.1
    assert reducer.development_terminal(cells) == "CH4_FAMILY_PRODUCTION_FREEZE_READY"
    with pytest.raises(ValueError):
        reducer.development_terminal(dict(list(cells.items())[:-1]))


@pytest.mark.parametrize(
    ("errors", "expected_status", "expected_snr"),
    [
        ([1, 2, 8], "BELOW_RANGE", None),
        ([20, 4, 1], "STABLE", "between"),
        ([20, 3, 1], "EXACT", 7.0),
        ([20, 15, 10], "UNREACHED", None),
        ([20, 2, 12], "CROSSING_UNSTABLE", None),
        ([20, 2, 12, 1], "CROSSING_UNSTABLE", None),
    ],
)
def test_crossing_contract_covers_bracket_exact_ranges_and_instability(errors, expected_status, expected_snr):
    contract = _load("family_freeze_contract")
    snr = list(range(5, 5 + 2 * len(errors), 2))
    result = contract.required_snr(snr, errors, [1000] * len(errors), threshold=3.5 / 1001)
    assert result["status"] == expected_status
    if expected_snr == "between":
        assert 7.0 < result["snr_db"] < 9.0
    elif expected_snr is not None:
        assert result["snr_db"] == pytest.approx(expected_snr)


def test_grade_contract_is_exhaustive_and_invalid_is_not_scientific_f():
    contract = _load("family_freeze_contract")
    neutral = {2: (-0.1, -0.2, 0.1), 4: (-0.1, -0.2, 0.1)}
    a = {
        "artifact_valid": True,
        "variants": {"C4_FWD": {2: (0.2, 0.1, 0.3), 4: (0.1, 0.01, 0.2)}, "B3_PSC": neutral},
        "cell_ci_uppers": {"C4_FWD": [], "B3_PSC": []},
    }
    assert contract.assign_grade(a) == "A"
    b = copy.deepcopy(a); b["variants"]["C4_FWD"][4] = (0.0, -0.1, 0.1)
    assert contract.assign_grade(b) == "B"
    c = copy.deepcopy(a)
    c["variants"]["C4_FWD"] = copy.deepcopy(neutral)
    c["cell_ci_uppers"]["C4_FWD"] = [-0.001]
    assert contract.assign_grade(c) == "C"
    f = copy.deepcopy(c); f["cell_ci_uppers"]["C4_FWD"] = [0.001]
    assert contract.assign_grade(f) == "F"
    assert contract.assign_grade({"artifact_valid": False}) == "CH4_FORMAL_INVALID"
    extra = copy.deepcopy(a); extra["variants"]["UNREGISTERED"] = neutral
    assert contract.assign_grade(extra) == "CH4_FORMAL_INVALID"
    missing = copy.deepcopy(a); missing["variants"]["C4_FWD"].pop(4)
    assert contract.assign_grade(missing) == "CH4_FORMAL_INVALID"


def test_mismatch_axis_delta_zero_is_byte_exact_and_positive_delta_uses_q_r_d_rh():
    smoke = _load("run_family_structure_smoke")
    core = _load("production_core")
    latent = core.make_latent_window("moderate", 21999, 8, 16)
    h0 = smoke.mismatch_channel(latent, 0.0)
    assert h0.tobytes() == latent["h_true"].tobytes()
    h = smoke.mismatch_channel(latent, 0.4)
    d = np.diag([1.4, 0.6]) / np.sqrt(1.0 + 0.4**2)
    expected = latent["gain"] * latent["q"] @ latent["mismatch_right"] @ d @ latent["mismatch_right"].conj().T
    assert np.allclose(h, expected, atol=2e-12)
    assert np.linalg.norm(h, "fro") == pytest.approx(np.linalg.norm(latent["h_true"], "fro"))
    primary = core.observe_latent(latent, 25.0, 2)
    zero = smoke.observe_mismatch(latent, 25.0, 2, 0.0)
    assert zero["h_true"].tobytes() == latent["h_true"].tobytes()
    assert zero["observation_hashes"] == primary["observation_hashes"]
    positive = smoke.observe_mismatch(latent, 25.0, 2, 0.4)
    noise_scale = primary["noise_scale"]
    assert np.allclose(positive["y_pilots"], h @ primary["x_pilots"] + noise_scale * latent["pilot_noise"][:, :2])
    assert np.allclose(positive["y_payload"], h @ latent["x_payload"] + noise_scale * latent["payload_noise"])
    assert positive["latent_hashes"] == latent["latent_hashes"]


def test_formal_smoke_cells_are_exact_and_delta_zero_is_reference_only():
    smoke = _load("run_family_structure_smoke")
    cells = smoke.formal_smoke_cells()
    observed = {(c["scene"], c["n_pilots"], c["snr_db"], c.get("delta")) for c in cells if c["kind"] != "reference"}
    assert observed == {
        ("moderate", 2, 5.0, None), ("moderate", 2, 41.0, None),
        ("moderate", 4, 5.0, None), ("moderate", 4, 41.0, None),
        ("moderate", 8, 25.0, None), ("moderate", 16, 25.0, None),
        ("weak", 2, 25.0, None), ("strong", 2, 25.0, None),
        ("moderate", 2, 25.0, None), ("moderate", 2, 25.0, 0.4),
    }
    references = [c for c in cells if c["kind"] == "reference"]
    assert references == [{
        "cell_id": "mismatch_delta0_reference", "kind": "reference", "delta": 0.0,
        "references_cell_id": "moderate_np2_snr25_primary",
    }]


def test_public_roles_are_mapped_before_receiver_action_and_o1_is_separate():
    smoke = _load("run_family_structure_smoke")
    manifest = _json("b2_tuning_manifest.json")
    calls = []
    def receiver(arm, x, yp, y, parameter):
        calls.append((arm, parameter)); return {"arm": arm}
    for role in ("B0", "B2_TUNED", "C4_FWD", "B3_PSC"):
        smoke.deployable_action(role, manifest["runtime_roles"], 0.25, None, None, None, receiver=receiver)
    assert calls == [("B0", None), ("B2", 0.25), ("C4", None), ("B3_PSC", 1.0)]
    with pytest.raises(ValueError, match="truth-only"):
        smoke.deployable_action("O1", manifest["runtime_roles"], 0.25, None, None, None, receiver=receiver)


def test_scientific_manifest_builder_requires_all_twelve_taus_and_never_invents_t087_hashes():
    contract = _load("family_freeze_contract")
    selections = {f"{scene}_np{n}": 0.25 for scene in ("weak", "moderate", "strong") for n in (2, 4, 8, 16)}
    built = contract.build_scientific_manifest(
        _json("ch4_scientific_manifest_schema.json"), selections,
        tuning_manifest_sha256="a" * 64, tuning_raw_sha256="b" * 64,
        tuning_aggregate_sha256="c" * 64, tuning_receipt_sha256="d" * 64,
        tuning_terminal="CH4_B2_TUNING_ACCEPTED",
    )
    assert built["schema_version"] == "t086.ch4-scientific-manifest.v1"
    assert built["tuned_tau_by_scene_np"] == selections
    assert built["execution_lock_interface"]["future_code_hash_values"] is None
    assert "formal_runner_sha256" not in built
    with pytest.raises(ValueError, match="12"):
        contract.build_scientific_manifest(
            _json("ch4_scientific_manifest_schema.json"), dict(list(selections.items())[:-1]),
            tuning_manifest_sha256="a" * 64, tuning_raw_sha256="b" * 64,
            tuning_aggregate_sha256="c" * 64, tuning_receipt_sha256="d" * 64,
            tuning_terminal="CH4_B2_TUNING_ACCEPTED",
        )
    with pytest.raises(ValueError, match="accepted"):
        contract.build_scientific_manifest(
            _json("ch4_scientific_manifest_schema.json"), selections,
            tuning_manifest_sha256="a" * 64, tuning_raw_sha256="b" * 64,
            tuning_aggregate_sha256="c" * 64, tuning_receipt_sha256="d" * 64,
            tuning_terminal="NOT_ACCEPTED",
        )


def _synthetic_tuning_raw(manifest):
    errors = {
        ("B2_TUNED_CANDIDATE", 0.0): 20,
        ("B2_TUNED_CANDIDATE", 0.25): 10,
        ("B2_TUNED_CANDIDATE", 0.5): 30,
        ("B2_TUNED_CANDIDATE", 0.75): 40,
        ("B2_TUNED_CANDIDATE", 1.0): 50,
        ("C4_FWD", None): 12,
        ("B3_PSC", 1.0): 15,
    }
    latents = []
    for scene in manifest["grid"]["scenes"]:
        for latent_id in range(21000, 21032):
            cells = []
            for n_pilots in manifest["grid"]["pilot_symbols_per_polarization"]:
                for snr_db in manifest["grid"]["snr_db"]:
                    rows = []
                    for (role, parameter), bit_errors in errors.items():
                        rows.append({
                            "public_role": role,
                            "runtime_arm": "B2" if role == "B2_TUNED_CANDIDATE" else manifest["tuning_rows"][role]["runtime_arm"],
                            "parameter": parameter,
                            "metrics": {
                                "bit_errors": bit_errors,
                                "payload_bits": 32768,
                                "ber": bit_errors / 32768,
                                "channel_nmse": 0.1,
                                "inverse_residual": 0.1,
                                "rho": 1.1,
                            },
                            "validity": "VALID",
                            "action_sha256": "a" * 64,
                        })
                    cells.append({
                        "cell_id": f"{scene}_np{n_pilots}_snr{int(snr_db)}",
                        "scene": scene,
                        "snr_db": snr_db,
                        "pilot_symbols_per_polarization": n_pilots,
                        "observation_hashes": {key: "b" * 64 for key in ("x_pilots", "y_pilots", "y_payload")},
                        "rows": rows,
                    })
            latents.append({
                "scene": scene,
                "latent_id": latent_id,
                "rng_namespace": {"synthetic": True},
                "latent_hashes": {key: "c" * 64 for key in (
                    "payload_bits", "channel_q", "gg_gain", "pilot_noise", "payload_noise",
                    "mismatch_left", "mismatch_right",
                )},
                "turbulence": {
                    "scenario": scene,
                    "alpha": manifest["resolved_scenes"][scene]["alpha"],
                    "beta": manifest["resolved_scenes"][scene]["beta"],
                    "authority": manifest["turbulence_authority"],
                },
                "cells": cells,
            })
    return {
        "schema_version": "t086.b2-tuning-raw.v1",
        "purpose": "canonical_tuning_non_thesis",
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": "d" * 64,
        "code_hashes": manifest["code_hashes"],
        "params_authority": {"path": "projects/simulation/params.py", "sha256": "e" * 64},
        "grid": manifest["grid"],
        "truth_firewall": "O1_ABSENT_FROM_TUNING_DEPLOYABLE_ROWS",
        "latents": latents,
    }


def test_tuning_runner_authority_and_full_raw_reduction_are_fail_closed():
    runner = _load("run_b2_tuning")
    reducer = _load("b2_tuning_reducer")
    manifest = _json("b2_tuning_manifest.json")
    runner.verify_authority(manifest)
    raw = _synthetic_tuning_raw(manifest)
    aggregate = reducer.reduce_raw(raw, manifest, "d" * 64)
    assert aggregate["census"] == {"scene_latents": 96, "observation_cells": 1152, "arm_rows": 8064}
    assert set(aggregate["selected_tau_by_scene_np"].values()) == {0.25}
    assert aggregate["decision"]["terminal"] == "TUNED_BASELINE_DOMINATES_DEVELOPMENT"
    broken = copy.deepcopy(raw)
    broken["latents"][0]["cells"][0]["rows"].pop()
    with pytest.raises(ValueError, match="rows"):
        reducer.reduce_raw(broken, manifest, "d" * 64)
    smoke = copy.deepcopy(raw)
    smoke["purpose"] = "tuning_preflight_smoke_non_thesis"
    smoke["latents"] = [next(row for row in raw["latents"] if row["scene"] == scene) for scene in ("weak", "moderate", "strong")]
    for row in smoke["latents"]:
        row["latent_id"] = 20999
    assert reducer.reduce_raw(smoke, manifest, "d" * 64)["census"] == {
        "scene_latents": 3, "observation_cells": 36, "arm_rows": 252,
    }


def test_tuning_checkpoint_binding_carries_runner_core_params_and_exact_ids():
    runner = _load("run_b2_tuning")
    manifest = _json("b2_tuning_manifest.json")
    binding = runner.checkpoint_binding(
        manifest, "canonical_tuning_non_thesis", list(range(21000, 21032))
    )
    assert binding["latent_ids"] == list(range(21000, 21032))
    assert set(binding["frozen_hashes"]) == {
        "manifest", "runner", "production_core.py", "common/_modulation.py",
        "scaled_unitary.py", "projects/simulation/params.py",
    }
    with pytest.raises(RuntimeError, match="IDs"):
        runner.checkpoint_binding(manifest, "canonical_tuning_non_thesis", [21000])


def test_checkpoint_is_removed_only_after_atomic_raw_save_succeeds(tmp_path, monkeypatch):
    runner = _load("run_b2_tuning")
    checkpoint = tmp_path / "checkpoint.json"
    checkpoint.write_text("{}", encoding="utf-8")
    def fail(*_args):
        raise OSError("synthetic save failure")
    monkeypatch.setattr(runner, "_atomic_save", fail)
    with pytest.raises(OSError, match="save failure"):
        runner.save_raw_and_clear_checkpoint({}, tmp_path / "raw.json", checkpoint, "test")
    assert checkpoint.exists()
    monkeypatch.setattr(runner, "_atomic_save", lambda *_args: None)
    runner.save_raw_and_clear_checkpoint({}, tmp_path / "raw.json", checkpoint, "test")
    assert not checkpoint.exists()


def test_smoke_output_must_be_outside_repository(tmp_path):
    runner = _load("run_b2_tuning")
    assert runner.REPO_ROOT == SEAM.parents[3]
    with pytest.raises(RuntimeError, match="temporary"):
        runner.validated_temporary_output_dir(runner.REPO_ROOT / "arbitrary" / "nested")
    assert runner.validated_temporary_output_dir(tmp_path) == tmp_path.resolve()


def test_tuning_receipt_accepts_only_valid_raw_only_aggregate_and_binds_four_artifacts():
    entry = _load("reduce_b2_tuning")
    manifest = _json("b2_tuning_manifest.json")
    raw = _synthetic_tuning_raw(manifest)
    raw["manifest_sha256"] = "a" * 64
    aggregate = _load("b2_tuning_reducer").reduce_raw(raw, manifest, "a" * 64)
    receipt = entry.build_receipt(
        manifest, raw, aggregate,
        artifact_hashes={
            "manifest_sha256": "a" * 64, "raw_sha256": "b" * 64,
            "aggregate_sha256": "c" * 64, "receipt_inputs_sha256": "d" * 64,
        },
    )
    assert receipt["terminal"] == "CH4_B2_TUNING_ACCEPTED"
    assert receipt["selected_tau_by_scene_np"] == aggregate["selected_tau_by_scene_np"]
    assert set(receipt["artifact_hashes"]) >= {
        "manifest_sha256", "raw_sha256", "aggregate_sha256", "receipt_inputs_sha256"
    }
    invalid = copy.deepcopy(aggregate)
    invalid["census"]["arm_rows"] -= 1
    with pytest.raises(ValueError, match="census"):
        entry.build_receipt(manifest, raw, invalid, artifact_hashes=receipt["artifact_hashes"])
    with pytest.raises(RuntimeError, match="manifest SHA"):
        entry.verify_provenance(manifest, raw)


def test_tuning_authority_verifier_rejects_any_nested_frozen_contract_change():
    runner = _load("run_b2_tuning")
    manifest = _json("b2_tuning_manifest.json")
    mutations = []
    changed = copy.deepcopy(manifest); changed["population"]["formal_structure_smoke_id"] = 22000; mutations.append(changed)
    changed = copy.deepcopy(manifest); changed["runtime_roles"]["B3_PSC"]["parameter"] = 0.75; mutations.append(changed)
    changed = copy.deepcopy(manifest); changed["tuning_rows"]["C4_FWD"]["runtime_arm"] = "B0"; mutations.append(changed)
    changed = copy.deepcopy(manifest); changed["resolved_scenes"]["weak"]["alpha"] = 11.5; mutations.append(changed)
    for changed in mutations:
        with pytest.raises(RuntimeError):
            runner.verify_authority(changed)


def _synthetic_structure_raw(smoke, selections):
    rows = []
    for role, runtime, parameter in (
        ("B0", "B0", None), ("B2_TUNED", "B2", 0.25),
        ("C4_FWD", "C4", None), ("B3_PSC", "B3_PSC", 1.0),
        ("O1", "O1_TRUTH_ONLY", None),
    ):
        rows.append({
            "public_role": role, "runtime_arm": runtime, "parameter": parameter,
            "metrics": {"bit_errors": 1, "payload_bits": 32768, "ber": 1 / 32768,
                        "channel_nmse": 0.1, "inverse_residual": 0.1, "rho": 1.1},
            "validity": "VALID", "action_sha256": "a" * 64,
        })
    cells = []
    for spec in smoke.formal_smoke_cells():
        if spec["kind"] == "reference":
            cells.append({**spec, "h_true_sha256": "b" * 64,
                          "reference_observation_hashes": {key: "c" * 64 for key in ("x_pilots", "y_pilots", "y_payload")}})
            continue
        cell_rows = copy.deepcopy(rows)
        cell_rows[1]["parameter"] = selections[f"{spec['scene']}_np{spec['n_pilots']}"]
        cells.append({
            **spec, "latent_id": 21999, "h_true_sha256": "b" * 64,
            "latent_hashes": {key: "d" * 64 for key in (
                "payload_bits", "channel_q", "gg_gain", "pilot_noise", "payload_noise",
                "mismatch_left", "mismatch_right",
            )},
            "observation_hashes": {key: "c" * 64 for key in ("x_pilots", "y_pilots", "y_payload")},
            "rows": cell_rows,
        })
    return {
        "schema_version": "t086.family-structure-smoke-raw.v1",
        "purpose": "formal_structure_smoke_non_thesis",
        "authority": "T086/D065/V040", "latent_id": 21999,
        "binding": {"schema_sha256": "e" * 64, "tuning_receipt_sha256": "f" * 64},
        "selected_tau_by_scene_np": selections,
        "cells": cells,
    }


def test_structure_smoke_binding_and_raw_validator_are_fail_closed(tmp_path):
    smoke = _load("run_family_structure_smoke")
    schema = _json("ch4_scientific_manifest_schema.json")
    selections = {f"{scene}_np{n}": 0.25 for scene in ("weak", "moderate", "strong") for n in (2, 4, 8, 16)}
    aggregate = {"decision": {"terminal": "CH4_FAMILY_PRODUCTION_FREEZE_READY"},
                 "selected_tau_by_scene_np": selections}
    receipt = {"terminal": "CH4_B2_TUNING_ACCEPTED", "selected_tau_by_scene_np": selections}
    binding = smoke.structure_binding(schema, aggregate, receipt, schema_sha256="e" * 64, receipt_sha256="f" * 64)
    assert binding["latent_id"] == 21999
    raw = _synthetic_structure_raw(smoke, selections)
    assert smoke.validate_structure_raw(raw, binding)["actual_cells"] == 10
    duplicated = copy.deepcopy(raw)
    duplicated["cells"].append(copy.deepcopy(duplicated["cells"][-1]))
    with pytest.raises(ValueError, match="census"):
        smoke.validate_structure_raw(duplicated, binding)
    assert smoke.validated_temporary_output_dir(tmp_path) == tmp_path.resolve()
    with pytest.raises(RuntimeError, match="temporary"):
        smoke.validated_temporary_output_dir(smoke.REPO_ROOT / "nested")


def test_final_manifest_entry_requires_actual_four_artifacts_and_three_way_tau_identity():
    freeze = _load("freeze_ch4_scientific_manifest")
    aggregate = _json("b2_tuning_aggregate.json")
    selections = aggregate["selected_tau_by_scene_np"]
    supplied = [f"{key}={value}" for key, value in selections.items()]
    parsed = freeze.parse_tau_arguments(supplied)
    assert parsed == selections
    lineage = freeze.verify_actual_tuning_lineage(parsed)
    assert set(lineage) == {
        "b2_tuning_manifest_sha256", "b2_tuning_raw_sha256",
        "b2_tuning_aggregate_sha256", "b2_tuning_receipt_sha256",
    }
    changed = copy.deepcopy(parsed); changed["moderate_np2"] = 0.25
    with pytest.raises(RuntimeError, match="three-way"):
        freeze.verify_actual_tuning_lineage(changed)
    built = freeze.build_final_manifest(parsed)
    assert built["tuning_lineage"]["selected_tau_by_scene_np"] == selections
    assert built["tuning_lineage"]["receipt_terminal"] == "CH4_B2_TUNING_ACCEPTED"
    assert built["execution_lock_interface"]["future_code_hash_values"] is None
    assert "scientific_manifest_sha256" in built["execution_lock_interface"]["required_bindings_before_first_formal_cell"]
