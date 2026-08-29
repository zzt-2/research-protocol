"""Run the preregistered correctness-only smoke and write its receipt."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

import core


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
RECEIPT = HERE / "smoke_receipt.json"
SEED = 53002
N_PAYLOAD = 256
N_PILOTS = 16
HIGH_SNR_DB = 30.0
MU = 1e-4
RING_THRESHOLD = 0.2
DECISION_THRESHOLD = 0.2


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=REPO, text=True, capture_output=True, check=True
    )
    return completed.stdout.strip()


def _ls_error(realization: dict) -> float:
    return float(np.max(np.abs(realization["W0"] @ realization["J"] - np.eye(2))))


def main() -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    test_path = REPO / "projects" / "simulation" / "tests" / "test_ch4_apsk_ring_gated_rde.py"
    test = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_path), "-q"],
        cwd=REPO,
        text=True,
        capture_output=True,
        env=env,
    )
    if test.returncode != 0:
        sys.stdout.write(test.stdout)
        sys.stderr.write(test.stderr)
        return test.returncode

    identity = core.generate_shared_correctness_realization(
        seed=SEED,
        n_payload=N_PAYLOAD,
        n_pilots=N_PILOTS,
        snr_db=HIGH_SNR_DB,
        identity_jones=True,
        noiseless=True,
    )
    random_noiseless = core.generate_shared_correctness_realization(
        seed=SEED + 1,
        n_payload=N_PAYLOAD,
        n_pilots=N_PILOTS,
        snr_db=HIGH_SNR_DB,
        noiseless=True,
    )
    high_snr = core.generate_shared_correctness_realization(
        seed=SEED,
        n_payload=N_PAYLOAD,
        n_pilots=N_PILOTS,
        snr_db=HIGH_SNR_DB,
    )
    arms = core.run_all_arms(
        high_snr,
        mu=MU,
        ring_threshold=RING_THRESHOLD,
        decision_threshold=DECISION_THRESHOLD,
    )
    hashes = {name: arm["realization_hash"] for name, arm in arms.items()}
    if len(set(hashes.values())) != 1:
        raise AssertionError("arms did not share one paired realization")
    if not all(np.all(np.isfinite(arm["z"])) for arm in arms.values()):
        raise AssertionError("non-finite arm output")

    receipt = {
        "schema_version": "ch4.gated-rde.smoke-receipt.v1",
        "verdict": "CORRECTNESS_ONLY",
        "method_signal": "NO_METHOD_SIGNAL",
        "formula_authority": {
            "primary": "Di Rosa-Richter JLT 2021 Section II-A Eq.(1)-(3)",
            "origin": "Ready-Gooch ICASSP 1990 Section 3",
            "status": "VERIFIED_BY_T056",
        },
        "parameters": {
            "seed": SEED,
            "n_payload": N_PAYLOAD,
            "n_pilots": N_PILOTS,
            "high_snr_db": HIGH_SNR_DB,
            "mu": MU,
            "ring_threshold": RING_THRESHOLD,
            "decision_threshold": DECISION_THRESHOLD,
        },
        "git_state": {
            "head": _git("rev-parse", "HEAD"),
            "status_short": _git(
                "status",
                "--short",
                "--",
                str(HERE.relative_to(REPO)),
                str(test_path.relative_to(REPO)),
            ).splitlines(),
        },
        "pytest": {
            "command": f"{sys.executable} -m pytest {test_path.relative_to(REPO)} -q",
            "returncode": test.returncode,
            "stdout": test.stdout.strip(),
        },
        "cells": {
            "identity_noiseless": {
                "seed": SEED,
                "ls_max_abs_error": _ls_error(identity),
                "realization_hash": identity["realization_hash"],
            },
            "random_J_noiseless": {
                "seed": SEED + 1,
                "ls_max_abs_error": _ls_error(random_noiseless),
                "realization_hash": random_noiseless["realization_hash"],
            },
            "high_snr_correctness": {
                "seed": SEED,
                "snr_db": HIGH_SNR_DB,
                "realization_hash": high_snr["realization_hash"],
                "paired_arm_hashes": hashes,
                "accepted_updates": {
                    name: int(np.count_nonzero(arm["flags"])) for name, arm in arms.items()
                },
                "finite_outputs": True,
            },
        },
        "blockers": [],
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"CORRECTNESS_ONLY / NO_METHOD_SIGNAL receipt={RECEIPT.relative_to(REPO)}")
    print(f"pytest={test.stdout.strip()}")
    print(f"identity_ls_max_abs_error={receipt['cells']['identity_noiseless']['ls_max_abs_error']:.3e}")
    print(f"random_J_ls_max_abs_error={receipt['cells']['random_J_noiseless']['ls_max_abs_error']:.3e}")
    print(f"realization_hash={high_snr['realization_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
