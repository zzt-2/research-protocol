import copy
import hashlib
import importlib.util
import inspect
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


SEAM = Path(__file__).resolve().parents[1]
SCIENTIFIC_SHA = "417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079"
ROLES = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1")


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


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _lock():
    return {
        "schema_version": "t087.ch4-formal-execution-lock.v1",
        "authority": "T087/D066/V041",
        "action_class": "CH4_FORMAL_EXECUTION_SEAM",
        "mission_checkpoint": "CP028",
        "control_epoch": 28,
        "base_commit": "d3d98c6fc92642e4d6b964d086c1f3bea2018d1d",
        "scientific_manifest_sha256": SCIENTIFIC_SHA,
        "execution_hashes": {
            "formal_runner_sha256": _sha("runner"),
            "formal_reducer_sha256": _sha("reducer"),
            "formal_reducer_entry_sha256": _sha("entry"),
            "formal_tests_sha256": _sha("tests"),
        },
        "frozen_dependency_hashes": {
            "production_core.py": "c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60",
            "common/_modulation.py": "bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10",
            "scaled_unitary.py": "868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2",
            "projects/simulation/params.py": "0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9",
        },
        "environment_snapshot": {
            "python": "3.test",
            "numpy": "2.test",
            "platform": "test-platform",
        },
        "allowed_populations": {
            "smoke": [29999],
            "formal": {"start": 30000, "stop_inclusive": 30127},
        },
    }


def _metrics(errors=12):
    bits = 32768
    return {
        "bit_errors": errors,
        "payload_bits": bits,
        "ber": errors / bits,
        "channel_nmse": 0.01,
        "inverse_residual": 0.02,
        "rho": 1.1,
        "public_scale": 0.9,
        "psc_scale": 1.0,
        "channel_nmse_semantics": "pre_calibration_inherited",
    }


def _synthetic_smoke_raw():
    runner = _load("run_ch4_formal_production")
    manifest = _json("ch4_scientific_manifest.json")
    scene_records = []
    primary_by_id = {}
    component_names = (
        "payload_bits", "channel_q", "gg_gain", "pilot_noise",
        "payload_noise", "mismatch_left", "mismatch_right",
    )
    for scenario_code, scene in enumerate(("weak", "moderate", "strong")):
        latent_hashes = {
            name: _sha(f"{scene}-{name}")
            for name in component_names
        }
        cells = []
        for spec in runner.formal_cell_specs(manifest):
            if spec["kind"] == "reference" or spec.get("scene") != scene:
                continue
            delta = spec.get("delta")
            suffix = "primary" if delta is None else f"delta-{delta}"
            payload_basis = f"{scene}-{spec['snr_db']}-payload"
            if delta is not None:
                payload_basis += f"-{delta}"
            observation_hashes = {
                "x_pilots": _sha(f"np-{spec['n_pilots']}"),
                "y_pilots": _sha(f"{scene}-{spec['snr_db']}-{spec['n_pilots']}-{suffix}"),
                "y_payload": _sha(payload_basis),
            }
            tau = manifest["tuned_tau_by_scene_np"][f"{scene}_np{spec['n_pilots']}"]
            rows = []
            for index, role in enumerate(ROLES):
                runtime = manifest["runtime_roles"][role]["runtime_arm"]
                parameter = tau if role == "B2_TUNED" else manifest["runtime_roles"][role]["parameter"]
                metrics = _metrics(12 + index)
                if role != "B3_PSC":
                    metrics["channel_nmse_semantics"] = "direct_estimate"
                rows.append({
                    "public_role": role,
                    "runtime_arm": runtime,
                    "parameter": parameter,
                    "metrics": metrics,
                    "validity": "VALID",
                    "action_sha256": _sha(f"{scene}-{spec['cell_id']}-{role}"),
                })
            cell = {
                **spec,
                "latent_id": 29999,
                "h_true_sha256": _sha(f"{scene}-{suffix}-h"),
                "latent_hashes": latent_hashes,
                "observation_hashes": observation_hashes,
                "rows": rows,
            }
            cells.append(cell)
            primary_by_id[spec["cell_id"]] = cell
        scene_records.append({
            "scene": scene,
            "latent_id": 29999,
            "rng_namespace": {
                name: {
                    "bit_generator": "PCG64",
                    "entropy": 20260830,
                    "spawn_key": [84, 1, scenario_code, 29999, component_code],
                }
                for component_code, name in enumerate(component_names)
            },
            "latent_hashes": latent_hashes,
            "turbulence": {**manifest["params_authority"]["resolved_scenes"][scene], "scenario": scene},
            "cells": cells,
        })
    primary = primary_by_id["moderate_np2_snr25_primary"]
    reference = {
        "cell_id": "mismatch_delta0_reference",
        "kind": "reference",
        "delta": 0.0,
        "references_cell_id": primary["cell_id"],
        "latent_id": 29999,
        "h_true_sha256": primary["h_true_sha256"],
        "reference_observation_hashes": dict(primary["observation_hashes"]),
    }
    lock = _lock()
    return {
        "schema_version": "t087.ch4-formal-raw.v1",
        "purpose": "formal_smoke_non_thesis",
        "authority": "T087/D066/V041",
        "base_commit": lock["base_commit"],
        "control_epoch": 28,
        "mission_checkpoint": "CP028",
        "scientific_manifest_sha256": SCIENTIFIC_SHA,
        "execution_lock_sha256": _sha("lock-file"),
        "execution_hashes": dict(lock["execution_hashes"]),
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "latent_ids": [29999],
        "latents": [{
            "latent_id": 29999,
            "scenes": scene_records,
            "delta_zero_reference": reference,
        }],
    }, lock


def test_formal_grid_and_population_are_exact_and_have_no_delta_zero_rows():
    runner = _load("run_ch4_formal_production")
    manifest = _json("ch4_scientific_manifest.json")
    specs = runner.formal_cell_specs(manifest)
    actual = [item for item in specs if item["kind"] != "reference"]
    reference = [item for item in specs if item["kind"] == "reference"]
    assert len(actual) == 119
    assert len(reference) == 1
    assert sum(item["scene"] == "moderate" for item in actual) == 81
    assert sum(item["scene"] == "weak" for item in actual) == 19
    assert sum(item["scene"] == "strong" for item in actual) == 19
    assert sum(item["kind"] == "mismatch" for item in actual) == 5
    assert runner.registered_latent_ids(manifest, "smoke") == [29999]
    assert runner.registered_latent_ids(manifest, "formal") == list(range(30000, 30128))
    assert runner.expected_census("smoke") == {
        "top_level_latents": 1, "scene_latents": 3, "actual_cells": 119,
        "arm_rows": 595, "delta_zero_references": 1,
    }
    assert runner.expected_census("formal") == {
        "top_level_latents": 128, "scene_latents": 384, "actual_cells": 15232,
        "arm_rows": 76160, "delta_zero_references": 128,
    }


def test_runner_has_no_scientific_overrides_and_keeps_truth_out_of_deployable_receiver():
    runner = _load("run_ch4_formal_production")
    source = inspect.getsource(runner)
    for forbidden in ("--latent-id", "--snr", "--scene", "--np", "--delta", "--tau", "--arm"):
        assert forbidden not in source
    assert runner.truth_firewall_passes()
    with pytest.raises(ValueError, match="truth-only"):
        runner.deployable_action(
            "O1", _json("ch4_scientific_manifest.json")["runtime_roles"], 1.0,
            object(), object(), object(), receiver=lambda *args: {},
        )


def test_smoke_requires_temp_lock_while_formal_forbids_lock_override():
    runner = _load("run_ch4_formal_production")
    candidate = Path(tempfile.gettempdir()) / "t087-static-test-lock.json"
    assert runner.resolve_execution_lock_path(
        smoke=True, temporary_lock=candidate, worktree_roots=[]
    ) == candidate.resolve()
    with pytest.raises(RuntimeError, match="smoke requires"):
        runner.resolve_execution_lock_path(smoke=True, temporary_lock=None, worktree_roots=[])
    with pytest.raises(RuntimeError, match="formal production forbids"):
        runner.resolve_execution_lock_path(
            smoke=False, temporary_lock=candidate, worktree_roots=[]
        )
    assert runner.resolve_execution_lock_path(
        smoke=False, temporary_lock=None, worktree_roots=[]
    ) == runner.LOCK_PATH


def test_execution_authority_fails_closed_on_manifest_lock_hash_or_population_change():
    runner = _load("run_ch4_formal_production")
    manifest = _json("ch4_scientific_manifest.json")
    lock = _lock()
    actual = dict(lock["execution_hashes"])
    runner.verify_execution_authority(
        manifest, lock, purpose="smoke", scientific_manifest_sha256=SCIENTIFIC_SHA,
        actual_execution_hashes=actual, git_head=lock["base_commit"],
        current_environment_snapshot=lock["environment_snapshot"],
    )
    bad = copy.deepcopy(lock)
    bad["execution_hashes"]["formal_runner_sha256"] = _sha("wrong")
    with pytest.raises(RuntimeError, match="execution hash"):
        runner.verify_execution_authority(
            manifest, bad, purpose="smoke", scientific_manifest_sha256=SCIENTIFIC_SHA,
            actual_execution_hashes=actual, git_head=lock["base_commit"],
            current_environment_snapshot=lock["environment_snapshot"],
        )
    with pytest.raises(RuntimeError, match="scientific manifest"):
        runner.verify_execution_authority(
            manifest, lock, purpose="smoke", scientific_manifest_sha256=_sha("changed"),
            actual_execution_hashes=actual, git_head=lock["base_commit"],
            current_environment_snapshot=lock["environment_snapshot"],
        )
    bad = copy.deepcopy(lock)
    bad["allowed_populations"]["smoke"] = [29998]
    with pytest.raises(RuntimeError, match="population"):
        runner.verify_execution_authority(
            manifest, bad, purpose="smoke", scientific_manifest_sha256=SCIENTIFIC_SHA,
            actual_execution_hashes=actual, git_head=lock["base_commit"],
            current_environment_snapshot=lock["environment_snapshot"],
        )
    with pytest.raises(RuntimeError, match="environment"):
        runner.verify_execution_authority(
            manifest, lock, purpose="smoke", scientific_manifest_sha256=SCIENTIFIC_SHA,
            actual_execution_hashes=actual, git_head=lock["base_commit"],
            current_environment_snapshot={"python": "wrong", "numpy": "wrong", "platform": "wrong"},
        )


def test_reducer_is_raw_only_and_accepts_exact_595_row_synthetic_smoke():
    reducer = _load("ch4_formal_reducer")
    assert "run_ch4_formal_production" not in inspect.getsource(reducer)
    raw, lock = _synthetic_smoke_raw()
    result = reducer.reduce_raw(
        raw, _json("ch4_scientific_manifest.json"), lock,
        scientific_manifest_sha256=SCIENTIFIC_SHA,
        execution_lock_sha256=_sha("lock-file"),
    )
    assert result["terminal"] == "FORMAL_SMOKE_STRUCTURAL_PASS"
    assert result["grade"] is None
    assert result["census"] == {
        "top_level_latents": 1, "scene_latents": 3, "actual_cells": 119,
        "arm_rows": 595, "delta_zero_references": 1,
    }


@pytest.mark.parametrize(
    "mutation,match",
    [
        ("missing", "cell census"),
        ("duplicate", "cell census"),
        ("wrong_role", "role"),
        ("wrong_tau", "parameter"),
        ("truth", "truth firewall"),
        ("hash", "hash"),
        ("scene_pool", "payload observation"),
        ("cross_scene_rng", "RNG namespace"),
        ("delta0", "delta-zero"),
    ],
)
def test_raw_validator_fails_closed(mutation, match):
    reducer = _load("ch4_formal_reducer")
    raw, lock = _synthetic_smoke_raw()
    moderate = raw["latents"][0]["scenes"][1]["cells"]
    if mutation == "missing":
        moderate.pop()
    elif mutation == "duplicate":
        moderate.append(copy.deepcopy(moderate[-1]))
    elif mutation == "wrong_role":
        moderate[0]["rows"][0]["public_role"] = "WRONG"
    elif mutation == "wrong_tau":
        moderate[0]["rows"][1]["parameter"] = 0.75
    elif mutation == "truth":
        raw["truth_firewall"] = "TRUTH_IN_DEPLOYABLE_PATH"
    elif mutation == "hash":
        moderate[0]["action_sha256"] = "bad"
        moderate[0]["rows"][0]["action_sha256"] = "bad"
    elif mutation == "scene_pool":
        np4 = next(cell for cell in moderate if cell["cell_id"] == "moderate_np4_snr5_primary")
        np4["observation_hashes"]["y_payload"] = _sha("different-payload")
    elif mutation == "cross_scene_rng":
        raw["latents"][0]["scenes"][2]["rng_namespace"] = copy.deepcopy(
            raw["latents"][0]["scenes"][0]["rng_namespace"]
        )
    elif mutation == "delta0":
        raw["latents"][0]["delta_zero_reference"]["h_true_sha256"] = _sha("wrong-h")
    with pytest.raises(ValueError, match=match):
        reducer.reduce_raw(
            raw, _json("ch4_scientific_manifest.json"), lock,
            scientific_manifest_sha256=SCIENTIFIC_SHA,
            execution_lock_sha256=_sha("lock-file"),
        )


def test_required_snr_covers_below_unreached_exact_stable_and_unstable():
    reducer = _load("ch4_formal_reducer")
    threshold = 0.0038
    snr = [5.0, 7.0, 9.0, 11.0]
    assert reducer.required_snr(snr, [0.003, 0.002, 0.001, 0.0005], threshold)["status"] == "BELOW_RANGE"
    assert reducer.required_snr(snr, [0.1, 0.05, 0.02, 0.01], threshold)["status"] == "UNREACHED"
    exact = reducer.required_snr(snr, [0.1, 0.02, threshold, 0.001], threshold)
    assert exact == {"status": "EXACT_HIT", "snr_required_db": 9.0}
    assert reducer.required_snr(snr, [threshold, 0.002, 0.001, 0.0005], threshold) == {
        "status": "BELOW_RANGE", "snr_required_db": None,
    }
    stable = reducer.required_snr(snr, [0.1, 0.01, 0.003, 0.001], threshold)
    assert stable["status"] == "STABLE"
    assert 7.0 < stable["snr_required_db"] < 9.0
    unstable = reducer.required_snr(snr, [0.1, 0.003, 0.01, 0.002], threshold)
    assert unstable["status"] == "CROSSING_UNSTABLE"
    assert reducer.required_snr(snr, [0.003, 0.01, 0.002, 0.001], threshold)["status"] == "CROSSING_UNSTABLE"
    assert reducer.required_snr(snr, [0.1, 0.003, 0.002, 0.01], threshold)["status"] == "CROSSING_UNSTABLE"


def _curve(ci2, ci4, point2=0.4, point4=0.3):
    return {
        "C4_FWD": {
            2: {"status": "VALID", "point_gain_db": point2, "ci_lower_db": ci2[0], "ci_upper_db": ci2[1]},
            4: {"status": "VALID", "point_gain_db": point4, "ci_lower_db": ci4[0], "ci_upper_db": ci4[1]},
        },
        "B3_PSC": {
            2: {"status": "VALID", "point_gain_db": -0.1, "ci_lower_db": -0.2, "ci_upper_db": 0.1},
            4: {"status": "VALID", "point_gain_db": -0.1, "ci_lower_db": -0.2, "ci_upper_db": 0.1},
        },
    }


def test_grade_is_exhaustive_and_only_uses_named_variants_and_moderate_np2_np4():
    reducer = _load("ch4_formal_reducer")
    assert reducer.grade_ch4(_curve((0.1, 0.7), (0.05, 0.6)), []) == "A"
    assert reducer.grade_ch4(_curve((0.1, 0.7), (-0.1, 0.6)), []) == "B"
    cell = [{"scene": "moderate", "n_pilots": 2, "variant": "C4_FWD", "ci_upper": -1e-5}]
    assert reducer.grade_ch4(_curve((-0.2, 0.4), (-0.2, 0.3), -0.1, -0.1), cell) == "C"
    assert reducer.grade_ch4(_curve((-0.2, 0.4), (-0.2, 0.3), -0.1, -0.1), []) == "F"
    bad = _curve((0.1, 0.7), (0.05, 0.6))
    bad["UNREGISTERED"] = bad.pop("B3_PSC")
    with pytest.raises(ValueError, match="variant"):
        reducer.grade_ch4(bad, [])


def test_execution_lock_builder_binds_dual_lock_inputs_without_writing():
    freezer = _load("freeze_ch4_formal_execution_lock")
    source = inspect.getsource(freezer)
    assert "30000" not in source and "30127" not in source
    lock_path = SEAM / "ch4_formal_execution_lock.json"
    temporary_path = lock_path.with_suffix(lock_path.suffix + ".tmp")
    existed_before = lock_path.exists()
    bytes_before = lock_path.read_bytes() if existed_before else None
    lock = freezer.build_execution_lock(
        scientific_manifest_sha256=SCIENTIFIC_SHA,
        execution_hashes=_lock()["execution_hashes"],
        frozen_dependency_hashes=_lock()["frozen_dependency_hashes"],
        base_commit=_lock()["base_commit"],
        environment_snapshot=_lock()["environment_snapshot"],
    )
    assert lock["scientific_manifest_sha256"] == SCIENTIFIC_SHA
    assert set(lock["execution_hashes"]) == {
        "formal_runner_sha256", "formal_reducer_sha256",
        "formal_reducer_entry_sha256", "formal_tests_sha256",
    }
    assert lock["allowed_populations"] == {
        "smoke": [29999], "formal": {"start": 30000, "stop_inclusive": 30127},
    }
    assert lock_path.exists() is existed_before
    if existed_before:
        assert lock_path.read_bytes() == bytes_before
    assert not temporary_path.exists()


def test_freezer_direct_cli_bootstraps_common_import_without_writing():
    script = SEAM / "freeze_ch4_formal_execution_lock.py"
    repo_root = SEAM.parents[3]
    lock_path = SEAM / "ch4_formal_execution_lock.json"
    temporary_path = lock_path.with_suffix(lock_path.suffix + ".tmp")
    existed_before = lock_path.exists()
    bytes_before = lock_path.read_bytes() if existed_before else None
    assert not temporary_path.exists()

    probe = f"""
import builtins
import pathlib
import sys

script = pathlib.Path({str(script)!r})
repo_root = pathlib.Path({str(repo_root)!r}).resolve()
lock_path = pathlib.Path({str(lock_path)!r}).resolve()
sys.path[:] = [str(script.parent)] + [
    item for item in sys.path
    if item and pathlib.Path(item).resolve() != repo_root
]
original_import = builtins.__import__
original_exists = pathlib.Path.exists
common_imported = False

def controlled_exists(path):
    if path.resolve() == lock_path:
        return False
    return original_exists(path)

def guarded_import(name, *args, **kwargs):
    global common_imported
    module = original_import(name, *args, **kwargs)
    if name == "projects.simulation.common":
        common_imported = True
        def prevent_write(*args, **kwargs):
            raise RuntimeError("WRITE_PREVENTED_AFTER_COMMON_IMPORT")
        module.save_results = prevent_write
    return module

builtins.__import__ = guarded_import
pathlib.Path.exists = controlled_exists
try:
    source = script.read_bytes()
    exec(
        compile(source, str(script), "exec"),
        {{"__name__": "__main__", "__file__": str(script)}},
    )
except RuntimeError as exc:
    if str(exc) != "WRITE_PREVENTED_AFTER_COMMON_IMPORT":
        raise
else:
    raise AssertionError("freezer reached a real write")
assert common_imported
print("COMMON_IMPORT_REACHED_WRITE_PREVENTED")
"""
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "COMMON_IMPORT_REACHED_WRITE_PREVENTED" in completed.stdout
    assert lock_path.exists() is existed_before
    if existed_before:
        assert lock_path.read_bytes() == bytes_before
    assert not temporary_path.exists()


def test_reducer_entry_fails_closed_when_runtime_environment_differs_from_lock():
    entry = _load("reduce_ch4_formal_production")
    lock = _lock()
    entry.verify_environment_authority(
        lock, current_environment_snapshot=lock["environment_snapshot"]
    )
    with pytest.raises(RuntimeError, match="environment"):
        entry.verify_environment_authority(
            lock,
            current_environment_snapshot={
                "python": "changed", "numpy": "changed", "platform": "changed"
            },
        )
    assert "verify_environment_authority" in inspect.getsource(entry.verify_provenance)
