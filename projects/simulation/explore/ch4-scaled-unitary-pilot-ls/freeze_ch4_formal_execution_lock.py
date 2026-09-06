"""Build and, only from ``main``, freeze the T087 formal execution lock."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import numpy as np


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
REPO_ROOT = SEAM.parents[3]
MANIFEST_PATH = SEAM / "ch4_scientific_manifest.json"
LOCK_PATH = SEAM / "ch4_formal_execution_lock.json"
TESTS_PATH = SEAM / "tests/test_ch4_formal_production.py"

FROZEN_SCIENTIFIC_MANIFEST_SHA256 = (
    "417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079"
)
BASE_COMMIT = "d3d98c6fc92642e4d6b964d086c1f3bea2018d1d"
FORMAL_START = 3 * (10 ** 4)
FORMAL_STOP = FORMAL_START + 127
_SHA_CHARS = set("0123456789abcdef")

_EXECUTION_PATHS = {
    "formal_runner_sha256": SEAM / "run_ch4_formal_production.py",
    "formal_reducer_sha256": SEAM / "ch4_formal_reducer.py",
    "formal_reducer_entry_sha256": SEAM / "reduce_ch4_formal_production.py",
    "formal_tests_sha256": TESTS_PATH,
}
_FROZEN_DEPENDENCY_HASHES = {
    "production_core.py": "c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60",
    "common/_modulation.py": "bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10",
    "scaled_unitary.py": "868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2",
    "projects/simulation/params.py": "0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9",
}


def _bootstrap_import_paths() -> None:
    """Make direct script execution independent of the caller's import path."""
    for root in (SIM_ROOT, REPO_ROOT):
        path = str(root)
        if path not in sys.path:
            sys.path.insert(0, path)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _valid_sha(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and set(value).issubset(_SHA_CHARS)
    )


def _validated_hash_map(
    value: Mapping[str, str], expected_keys: set[str], label: str
) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != expected_keys:
        raise ValueError(f"{label} key set mismatch")
    result = dict(value)
    for name, digest in result.items():
        if not _valid_sha(digest):
            raise ValueError(f"{label} contains invalid SHA-256: {name}")
    return result


def build_execution_lock(
    *,
    scientific_manifest_sha256: str,
    execution_hashes: Mapping[str, str],
    frozen_dependency_hashes: Mapping[str, str],
    base_commit: str,
    environment_snapshot: Mapping[str, str],
) -> dict[str, object]:
    """Return the immutable dual-lock payload without touching the filesystem."""
    if scientific_manifest_sha256 != FROZEN_SCIENTIFIC_MANIFEST_SHA256:
        raise ValueError("scientific manifest SHA mismatch")
    if base_commit != BASE_COMMIT:
        raise ValueError("base commit mismatch")
    checked_execution = _validated_hash_map(
        execution_hashes, set(_EXECUTION_PATHS), "execution hash"
    )
    checked_frozen = _validated_hash_map(
        frozen_dependency_hashes, set(_FROZEN_DEPENDENCY_HASHES),
        "frozen dependency hash",
    )
    if checked_frozen != _FROZEN_DEPENDENCY_HASHES:
        raise ValueError("frozen dependency hash mismatch")
    if not isinstance(environment_snapshot, Mapping) or set(environment_snapshot) != {
        "python", "numpy", "platform"
    }:
        raise ValueError("environment snapshot key set mismatch")
    checked_environment = dict(environment_snapshot)
    if any(not isinstance(value, str) or not value for value in checked_environment.values()):
        raise ValueError("environment snapshot contains an invalid value")

    return {
        "schema_version": "t087.ch4-formal-execution-lock.v1",
        "authority": "T087/D066/V041",
        "action_class": "CH4_FORMAL_EXECUTION_SEAM",
        "mission_checkpoint": "CP028",
        "control_epoch": 28,
        "base_commit": base_commit,
        "scientific_manifest_sha256": scientific_manifest_sha256,
        "execution_hashes": checked_execution,
        "frozen_dependency_hashes": checked_frozen,
        "environment_snapshot": checked_environment,
        "allowed_populations": {
            "smoke": [29_999],
            "formal": {"start": FORMAL_START, "stop_inclusive": FORMAL_STOP},
        },
    }


def _dependency_path(relative: str) -> Path:
    if relative == "projects/simulation/params.py":
        return SIM_ROOT / "params.py"
    if relative.startswith("common/"):
        return SIM_ROOT / relative
    return SEAM / relative


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=SEAM,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def main() -> int:
    _bootstrap_import_paths()
    if LOCK_PATH.exists():
        raise RuntimeError("formal execution lock already exists; refusing refreeze")
    manifest_sha = file_sha256(MANIFEST_PATH)
    if manifest_sha != FROZEN_SCIENTIFIC_MANIFEST_SHA256:
        raise RuntimeError("scientific manifest on-disk SHA mismatch")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("base_commit") != BASE_COMMIT or _git_head() != BASE_COMMIT:
        raise RuntimeError("formal execution lock base authority mismatch")

    expected_manifest_frozen = dict(manifest.get("frozen_code_hashes", {}))
    params_authority = manifest.get("params_authority")
    if not isinstance(params_authority, Mapping):
        raise RuntimeError("scientific manifest params authority missing")
    expected_manifest_frozen["projects/simulation/params.py"] = params_authority.get(
        "sha256"
    )
    if expected_manifest_frozen != _FROZEN_DEPENDENCY_HASHES:
        raise RuntimeError("scientific manifest frozen dependency map mismatch")
    for relative, expected in _FROZEN_DEPENDENCY_HASHES.items():
        if file_sha256(_dependency_path(relative)) != expected:
            raise RuntimeError(f"actual frozen dependency SHA mismatch: {relative}")

    execution_hashes = {
        name: file_sha256(path) for name, path in _EXECUTION_PATHS.items()
    }
    lock = build_execution_lock(
        scientific_manifest_sha256=manifest_sha,
        execution_hashes=execution_hashes,
        frozen_dependency_hashes=_FROZEN_DEPENDENCY_HASHES,
        base_commit=BASE_COMMIT,
        environment_snapshot={
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
    )

    from projects.simulation.common import save_results

    temporary = LOCK_PATH.with_suffix(LOCK_PATH.suffix + ".tmp")
    if temporary.exists():
        raise RuntimeError("stale formal execution lock temporary exists")
    save_results(lock, str(temporary), "t087_ch4_formal_execution_lock_freeze")
    os.replace(temporary, LOCK_PATH)
    print(f"CH4_FORMAL_EXECUTION_LOCK_FROZEN sha256={file_sha256(LOCK_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
