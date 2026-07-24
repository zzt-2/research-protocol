"""Cross-process fingerprint helper for the determinism regression (T005 Phase A.2
+ Phase B). Invoked as a subprocess with PYTHONHASHSEED set differently to prove:

  - T004 (hash(model_id)): two subprocesses with DIFFERENT PYTHONHASHSEED ->
    DIFFERENT fingerprints (non-determinism reproduced).
  - T005 (fixed integer seed): two subprocesses with DIFFERENT PYTHONHASHSEED ->
    IDENTICAL fingerprints (determinism proven).

Usage (called by the pytest regression; not meant for direct interactive use):

    python _crossproc_fingerprint.py <which> <seed> <model_id> <pdl_db>

  which in {"t004", "t005"}
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SIM / "explore" / "pilot-jones-complex-repair"))


def main():
    which, seed, model_id, pdl_db = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    if which == "t004":
        import run_probe
        out = run_probe.t004_fingerprint_in_process(seed=seed, model_id=model_id)
    elif which == "t005":
        import run_probe
        out = run_probe.t005_fingerprint_in_process(seed=seed, model_id=model_id)
    else:
        raise ValueError(which)
    # J00 is complex -> serialize deterministically (real,imag) so two
    # subprocesses can be compared by string equality.
    if "J00" in out and isinstance(out["J00"], complex):
        out["J00"] = {"re": out["J00"].real, "imag": out["J00"].imag}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
