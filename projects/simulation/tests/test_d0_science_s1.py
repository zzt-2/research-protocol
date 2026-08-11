import importlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))


def _science():
    return importlib.import_module("science")


def test_persistent_transitions_none_single_and_merge():
    science = _science()
    zero = np.zeros(160)
    assert science.persistent_transition_boundaries(zero) == ()

    one = zero.copy()
    one[80:] = np.pi / 2
    assert science.persistent_transition_boundaries(one) == (80,)

    close = one.copy()
    close[112:] = np.pi
    assert science.persistent_transition_boundaries(close) == (80,)


def test_checkpoint_resume_deduplicates_and_rejects_conflicts(tmp_path):
    science = _science()
    checkpoint = tmp_path / "checkpoint.jsonl"
    row = {
        "record_type": "S1_TRAJECTORY", "seed": 8100,
        "cell_id": "snr_10db__linewidth_10000hz", "target_polarization": "X",
        "persistent_transition_count": 0,
        "persistent_transition_after_symbol": [], "event_present": False,
        "trajectory_receipt_sha256": "0" * 64,
    }
    science.append_checkpoint_frame(checkpoint, [row, {**row, "target_polarization": "Y"}])
    science.append_checkpoint_frame(checkpoint, [row, {**row, "target_polarization": "Y"}])
    loaded = science.load_checkpoint_rows(checkpoint)
    assert len(loaded) == 2
    assert len(science.typed_s1_rows(loaded)) == 2
    with pytest.raises(ValueError, match="conflicting checkpoint row"):
        science.append_checkpoint_frame(
            checkpoint, [{**row, "event_present": True, "persistent_transition_count": 1,
                          "persistent_transition_after_symbol": [80]}]
        )


def test_first_stage_plan_is_exact_and_wrong_extent_rejected():
    science = _science()
    contract = science.load_science_contract(science.DEFAULT_CONTRACT_PATH)
    plan = science.s1_plan(contract, extent="FIRST_STAGE")
    assert len(plan) == 240
    assert len({(seed, cell.cell_id) for seed, cell in plan}) == 240
    assert {seed for seed, _ in plan} == set(range(8100, 8120))
    assert len({cell.cell_id for _, cell in plan}) == 12
    with pytest.raises(ValueError, match="extent"):
        science.s1_plan(contract, extent="DEV")


def test_phase_shapes_are_fail_closed():
    science = _science()
    with pytest.raises(ValueError, match="shape"):
        science.detect_persistent_transitions(np.zeros(100), np.zeros(99))


def test_cli_imports_from_repository_root():
    result = subprocess.run(
        [sys.executable, "-B", str(D0_ROOT / "science.py"), "--help"],
        cwd=SIMULATION_ROOT.parents[1], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_atomic_writer_retries_transient_windows_replace_lock(tmp_path, monkeypatch):
    science = _science()
    target = tmp_path / "checkpoint.jsonl"
    real_replace = science.os.replace
    calls = 0

    def transient(source, destination):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise PermissionError(5, "transient reader lock")
        real_replace(source, destination)

    monkeypatch.setattr(science.os, "replace", transient)
    science._atomic_bytes(target, b"one\n")
    assert calls == 2
    assert target.read_bytes() == b"one\n"
