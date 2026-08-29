"""Write the T085 raw-only aggregate and provenance receipt exactly once."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from corrected_anchor_reducer import reduce_raw
from run_corrected_anchor import truth_firewall_passes


SEAM = Path(__file__).resolve().parent
MANIFEST_PATH = SEAM / "corrected_anchor_manifest.json"
RAW_PATH = SEAM / "corrected_anchor_raw.json"
AGGREGATE_PATH = SEAM / "corrected_anchor_aggregate.json"
RECEIPT_PATH = SEAM / "corrected_anchor_receipt.json"
ACTUAL_GENERATOR_RUNNER_SHA256 = "871ec566744cc678eb83c13aaf472609ecc0b77ce8f8e131ac2eaa063d30e91b"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_save(data: dict, target: Path, script_name: str) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), script_name)
    os.replace(temporary, target)


def _test_hash() -> str:
    return file_sha256(SEAM / "tests/test_corrected_anchor.py")


def _code_path(relative: str) -> Path:
    return SEAM.parents[1] / relative if relative.startswith("common/") else SEAM / relative


def verify_provenance(manifest: dict, raw: dict) -> None:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if manifest.get("base_commit") != commit or raw.get("base_commit") != commit:
        raise RuntimeError("base commit provenance mismatch")
    expected_keys = {"production_core.py", "common/_modulation.py", "scaled_unitary.py"}
    hashes = manifest.get("code_hashes")
    if not isinstance(hashes, dict) or set(hashes) != expected_keys:
        raise RuntimeError("frozen code hash key set mismatch")
    for relative, expected in hashes.items():
        if file_sha256(_code_path(relative)) != expected:
            raise RuntimeError(f"frozen code hash mismatch: {relative}")
    if raw.get("code_hashes") != hashes:
        raise RuntimeError("raw code hash binding mismatch")


def main() -> int:
    if AGGREGATE_PATH.exists() or RECEIPT_PATH.exists():
        raise RuntimeError("canonical reduction artifacts already exist; refusing rerun")
    manifest = load_json(MANIFEST_PATH)
    raw = load_json(RAW_PATH)
    verify_provenance(manifest, raw)
    manifest_hash = file_sha256(MANIFEST_PATH)
    aggregate = reduce_raw(raw, manifest, manifest_hash)
    if not truth_firewall_passes():
        raise RuntimeError("deployable truth firewall failed")
    _atomic_save(aggregate, AGGREGATE_PATH, "t085_corrected_anchor_raw_only_reducer")
    receipt = {
        "schema_version": "t085.corrected-anchor-receipt.v1",
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "checks": {
            "raw_only_reduction": "PASS",
            "schema_and_counts": "PASS",
            "shared_latent_pairing": "PASS",
            "pooled_np2_64_clusters": "PASS",
            "truth_firewall": "PASS",
            "raw_and_frozen_code_hash_binding": "PASS",
            "reproducible_generation_binding": "PARTIAL",
            "post_run_runner_change_scope": "AUTHORITY_VALIDATION_ONLY"
        },
        "census": aggregate["census"],
        "bootstrap": manifest["bootstrap"],
        "decision": aggregate["decision"],
        "hashes": {
            "manifest_sha256": manifest_hash,
            "raw_sha256": file_sha256(RAW_PATH),
            "aggregate_sha256": file_sha256(AGGREGATE_PATH),
            "actual_generator_runner_sha256": ACTUAL_GENERATOR_RUNNER_SHA256,
            "post_run_validation_runner_sha256": file_sha256(SEAM / "run_corrected_anchor.py"),
            "reducer_core_sha256": file_sha256(SEAM / "corrected_anchor_reducer.py"),
            "reducer_entry_sha256": file_sha256(Path(__file__)),
            "tests_sha256": _test_hash(),
            "production_core_sha256": file_sha256(SEAM / "production_core.py"),
            "common_demapper_sha256": file_sha256(SEAM.parents[1] / "common/_modulation.py"),
            "scaled_unitary_sha256": file_sha256(SEAM / "scaled_unitary.py")
        }
    }
    _atomic_save(receipt, RECEIPT_PATH, "t085_corrected_anchor_receipt")
    print(json.dumps(receipt["decision"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
