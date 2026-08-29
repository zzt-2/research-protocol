from __future__ import annotations

import importlib.util
import copy
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest


SEAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SEAM))


def _load(name: str):
    path = SEAM / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"t085_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _manifest() -> dict:
    return json.loads((SEAM / "corrected_anchor_manifest.json").read_text(encoding="utf-8"))


def _synthetic_raw(manifest: dict) -> dict:
    components = {
        "payload_bits": 0, "channel_q": 1, "gg_gain": 2,
        "pilot_noise": 3, "payload_noise": 4,
        "mismatch_left": 5, "mismatch_right": 6,
    }
    latents = []
    for i, latent_id in enumerate(range(20000, 20064)):
        namespace = {
            name: {"bit_generator": "PCG64", "entropy": 20260830,
                   "spawn_key": [84, 1, 1, latent_id, code]}
            for name, code in components.items()
        }
        cells = []
        for cell in manifest["cells"]:
            rows = []
            base = 1000 + i + int(cell["snr_db"])
            for arm, offset in (("B0", 100), ("B2", 50), ("B3_PSC", 40), ("C4", 0), ("O1", -100)):
                errors = base + offset
                rows.append({
                    "arm": arm,
                    "parameter": manifest["arms"][arm]["parameter"],
                    "metrics": {
                        "bit_errors": errors, "payload_bits": 32768,
                        "ber": errors / 32768,
                        "channel_nmse": 0.1, "inverse_residual": 0.1, "rho": 1.1,
                    },
                    "public_scale": None if arm == "B0" else 1.0,
                    "psc_scale": 1.0,
                    "validity": "VALID",
                    "action_sha256": f"{latent_id:064x}"[-64:],
                    "runtime_ns": 1,
                })
            cells.append({
                **cell,
                "observation_hashes": {
                    "x_pilots": f"x{cell['pilot_symbols_per_polarization']}",
                    "y_pilots": f"yp{cell['cell_id']}{latent_id}",
                    "y_payload": f"y{int(cell['snr_db'])}{latent_id}",
                },
                "rows": rows,
            })
        latents.append({
            "latent_id": latent_id,
            "rng_namespace": namespace,
            "latent_hashes": {name: f"{code + latent_id:064x}"[-64:] for name, code in components.items()},
            "turbulence": {
                "scenario": "moderate", "alpha": 4.0, "beta": 1.9,
                "scintillation_index": 1 / 4.0 + 1 / 1.9 + 1 / (4.0 * 1.9),
                "authority": manifest["scene"]["authority"],
            },
            "cells": cells,
        })
    return {
        "schema_version": "t085.corrected-anchor-raw.v1",
        "purpose": "a2_bridge_non_thesis",
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": "synthetic-manifest-hash",
        "code_hashes": manifest["code_hashes"],
        "scene": manifest["scene"],
        "cells": manifest["cells"],
        "payload_symbols_per_polarization": 4096,
        "max_pilots": 4,
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "latents": latents,
    }


def test_manifest_freezes_a2_population_hashes_and_strict_gate():
    manifest = _manifest()
    assert manifest["schema_version"] == "t085.corrected-anchor.v1"
    assert manifest["authority"] == "T085/D064/V039"
    assert manifest["mission_checkpoint"] == "CP026"
    assert manifest["control_epoch"] == 26
    assert [(c["snr_db"], c["pilot_symbols_per_polarization"]) for c in manifest["cells"]] == [
        (14.0, 2), (14.0, 4), (18.0, 2), (18.0, 4)
    ]
    assert manifest["population"] == {
        "windows_per_cell": 64,
        "canonical_latent_ids": {"start": 20000, "stop_inclusive": 20063},
        "smoke_latent_id": 19999,
        "shared_across_cells": True,
    }
    assert manifest["payload_symbols_per_polarization"] == 4096
    assert manifest["max_pilots"] == 4
    assert manifest["arms"] == {
        "B0": {"parameter": None, "access": "receiver-visible"},
        "B2": {"parameter": 1.0, "access": "receiver-visible"},
        "B3_PSC": {"parameter": 1.0, "access": "receiver-visible pilots only"},
        "C4": {"parameter": None, "access": "receiver-visible"},
        "O1": {"parameter": None, "access": "truth-only runner path; never receiver_action"},
    }
    assert manifest["bootstrap"]["seed"] == 2026083006
    assert manifest["bootstrap"]["resamples"] == 5000
    assert manifest["gate"]["pooled_np2_comparators"] == ["B2", "B3_PSC"]


def test_smoke_build_has_one_shared_latent_four_cells_and_truth_separation(tmp_path):
    runner = _load("run_corrected_anchor")
    manifest = _manifest()
    raw = runner.build_raw(manifest, [19999], purpose="smoke_non_thesis", checkpoint_path=tmp_path / "smoke.checkpoint.json")
    assert raw["schema_version"] == "t085.corrected-anchor-raw.v1"
    assert raw["purpose"] == "smoke_non_thesis"
    assert [x["latent_id"] for x in raw["latents"]] == [19999]
    latent = raw["latents"][0]
    assert len(latent["rng_namespace"]) == len(latent["latent_hashes"]) == 7
    assert len(latent["cells"]) == 4
    by_id = {cell["cell_id"]: cell for cell in latent["cells"]}
    assert by_id["snr14_np2"]["observation_hashes"]["y_payload"] == by_id["snr14_np4"]["observation_hashes"]["y_payload"]
    assert by_id["snr18_np2"]["observation_hashes"]["y_payload"] == by_id["snr18_np4"]["observation_hashes"]["y_payload"]
    for cell in latent["cells"]:
        assert [row["arm"] for row in cell["rows"]] == ["B0", "B2", "B3_PSC", "C4", "O1"]
        assert all(row["validity"] == "VALID" for row in cell["rows"])
    for snr in (14, 18):
        a, b = by_id[f"snr{snr}_np2"], by_id[f"snr{snr}_np4"]
        assert next(r for r in a["rows"] if r["arm"] == "O1")["metrics"] == next(r for r in b["rows"] if r["arm"] == "O1")["metrics"]
    assert runner.truth_firewall_passes()


def test_checkpoint_resume_is_idempotent_and_binding_mismatch_fails_closed(tmp_path):
    runner = _load("run_corrected_anchor")
    manifest = _manifest()
    checkpoint = tmp_path / "resume.checkpoint.json"
    first = runner.build_raw(manifest, [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)
    before = checkpoint.read_bytes()
    second = runner.build_raw(manifest, [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)
    assert first["latents"] == second["latents"]
    assert len(second["latents"]) == 1
    assert checkpoint.read_bytes() == before
    corrupted = json.loads(checkpoint.read_text(encoding="utf-8"))
    corrupted["binding"]["base_commit"] = "wrong"
    checkpoint.write_text(json.dumps(corrupted), encoding="utf-8")
    with pytest.raises(RuntimeError, match="checkpoint binding"):
        runner.build_raw(manifest, [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)


def test_checkpoint_binds_runner_hash_and_rejects_runner_identity_mismatch(tmp_path):
    runner = _load("run_corrected_anchor")
    checkpoint = tmp_path / "runner-binding.checkpoint.json"
    runner.build_raw(_manifest(), [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)
    saved = json.loads(checkpoint.read_text(encoding="utf-8"))
    expected = hashlib.sha256((SEAM / "run_corrected_anchor.py").read_bytes()).hexdigest()
    assert saved["binding"]["runner_sha256"] == expected
    saved["binding"]["runner_sha256"] = "0" * 64
    checkpoint.write_text(json.dumps(saved), encoding="utf-8")
    with pytest.raises(RuntimeError, match="checkpoint binding"):
        runner.build_raw(_manifest(), [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)


@pytest.mark.parametrize("mutation", ["namespace", "latent_hash", "observation_hash", "arm_metric"])
def test_checkpoint_revalidates_every_completed_record_before_reuse(tmp_path, mutation):
    runner = _load("run_corrected_anchor")
    checkpoint = tmp_path / f"record-{mutation}.checkpoint.json"
    runner.build_raw(_manifest(), [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)
    saved = json.loads(checkpoint.read_text(encoding="utf-8"))
    corrupted = copy.deepcopy(saved)
    record = corrupted["latents"][0]
    if mutation == "namespace":
        record["rng_namespace"]["payload_bits"]["spawn_key"][3] = 20000
    elif mutation == "latent_hash":
        record["latent_hashes"]["payload_bits"] = "0" * 64
    elif mutation == "observation_hash":
        record["cells"][0]["observation_hashes"]["y_payload"] = "0" * 64
    else:
        record["cells"][0]["rows"][0]["metrics"]["bit_errors"] += 1
    checkpoint.write_text(json.dumps(corrupted), encoding="utf-8")
    with pytest.raises(RuntimeError, match="checkpoint record"):
        runner.build_raw(_manifest(), [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint, retain_checkpoint=True)


def test_pooled_np2_bootstrap_uses_exactly_64_latent_clusters_and_resets_rng():
    reducer = _load("corrected_anchor_reducer")
    latent_ids = list(range(20000, 20064))
    differences = {
        latent_id: {14.0: -(i + 1) / 10000.0, 18.0: -(64 - i) / 20000.0}
        for i, latent_id in enumerate(latent_ids)
    }
    got = reducer.pooled_np2_bootstrap(differences, seed=2026083006, resamples=5000)
    matrix = np.asarray([[differences[i][14.0], differences[i][18.0]] for i in latent_ids])
    rng = np.random.Generator(np.random.PCG64(2026083006))
    indices = rng.integers(0, 64, size=(5000, 64), dtype=np.int64)
    draws = matrix[indices].mean(axis=(1, 2))
    lo, hi = np.quantile(draws, [0.025, 0.975])
    assert got == {
        "mean_diff": float(matrix.mean()),
        "ci_lower": float(lo),
        "ci_upper": float(hi),
        "clusters": 64,
        "rows_per_cluster": 2,
        "candidate_cluster_wins": int(np.count_nonzero(matrix.mean(axis=1) < 0)),
    }
    assert got == reducer.pooled_np2_bootstrap(differences, seed=2026083006, resamples=5000)


def test_raw_only_reducer_uses_total_counts_and_strict_b2_b3_gate():
    reducer = _load("corrected_anchor_reducer")
    raw = _synthetic_raw(_manifest())
    aggregate = reducer.reduce_raw(raw, _manifest(), manifest_sha256=raw["manifest_sha256"])
    assert aggregate["schema_version"] == "t085.corrected-anchor-aggregate.v1"
    assert aggregate["census"] == {"latents": 64, "cell_rows": 256, "arm_rows": 1280}
    first = aggregate["cells"][0]
    assert first["arms"]["B2"]["ber"] == first["arms"]["B2"]["bit_errors"] / first["arms"]["B2"]["payload_bits"]
    assert set(first["comparisons"]) == {"B2", "B3_PSC"}
    assert aggregate["pooled_np2"]["B2"]["clusters"] == 64
    assert aggregate["pooled_np2"]["B3_PSC"]["clusters"] == 64
    assert aggregate["decision"]["terminal"] == "PRODUCTION_SEAM_BRIDGE_PASS"


@pytest.mark.parametrize(("field", "bad"), [("control_epoch", 999), ("mission_checkpoint", "CP999")])
def test_raw_reducer_rejects_control_identity_mutations(field, bad):
    reducer = _load("corrected_anchor_reducer")
    raw = _synthetic_raw(_manifest())
    raw[field] = bad
    with pytest.raises(ValueError, match="raw/manifest mismatch"):
        reducer.reduce_raw(raw, _manifest(), manifest_sha256=raw["manifest_sha256"])


def test_reduce_entry_verifies_actual_head_and_all_frozen_code_hashes():
    entry = _load("reduce_corrected_anchor")
    manifest = _manifest()
    raw = _synthetic_raw(manifest)
    assert entry.verify_provenance(manifest, raw) is None

    wrong_base = copy.deepcopy(manifest)
    wrong_base["base_commit"] = "0" * 40
    with pytest.raises(RuntimeError, match="base commit"):
        entry.verify_provenance(wrong_base, raw)

    wrong_code = copy.deepcopy(manifest)
    wrong_code["code_hashes"]["production_core.py"] = "0" * 64
    with pytest.raises(RuntimeError, match="frozen code hash"):
        entry.verify_provenance(wrong_code, raw)

    wrong_raw = copy.deepcopy(raw)
    wrong_raw["code_hashes"]["scaled_unitary.py"] = "0" * 64
    with pytest.raises(RuntimeError, match="raw code hash"):
        entry.verify_provenance(manifest, wrong_raw)


@pytest.mark.parametrize(
    ("mutation", "value"),
    [
        ("bootstrap_rng", "MT19937"),
        ("bootstrap_confidence", 0.90),
        ("bootstrap_stream", "continue one stream"),
        ("bootstrap_pooling", "128 independent rows"),
        ("b0_parameter", 1.0),
        ("o1_parameter", 1.0),
        ("o1_access", "receiver-visible"),
        ("missing_code_hash", None),
    ],
)
def test_runner_authority_rejects_every_frozen_manifest_contract_mutation(mutation, value):
    runner = _load("run_corrected_anchor")
    manifest = copy.deepcopy(_manifest())
    if mutation == "bootstrap_rng":
        manifest["bootstrap"]["rng"] = value
    elif mutation == "bootstrap_confidence":
        manifest["bootstrap"]["confidence"] = value
    elif mutation == "bootstrap_stream":
        manifest["bootstrap"]["stream_rule"] = value
    elif mutation == "bootstrap_pooling":
        manifest["bootstrap"]["pooled_np2_cluster"] = value
    elif mutation == "b0_parameter":
        manifest["arms"]["B0"]["parameter"] = value
    elif mutation == "o1_parameter":
        manifest["arms"]["O1"]["parameter"] = value
    elif mutation == "o1_access":
        manifest["arms"]["O1"]["access"] = value
    else:
        manifest["code_hashes"].pop("scaled_unitary.py")
    with pytest.raises(RuntimeError, match="manifest"):
        runner.verify_authority(manifest)


def test_receipt_distinguishes_actual_generator_from_post_run_validation_runner():
    receipt = json.loads((SEAM / "corrected_anchor_receipt.json").read_text(encoding="utf-8"))
    assert receipt["checks"]["raw_and_frozen_code_hash_binding"] == "PASS"
    assert receipt["checks"]["reproducible_generation_binding"] == "PARTIAL"
    assert receipt["hashes"]["actual_generator_runner_sha256"] == (
        "871ec566744cc678eb83c13aaf472609ecc0b77ce8f8e131ac2eaa063d30e91b"
    )
    assert receipt["hashes"]["post_run_validation_runner_sha256"] == hashlib.sha256(
        (SEAM / "run_corrected_anchor.py").read_bytes()
    ).hexdigest()
    assert "runner_sha256" not in receipt["hashes"]
