# -*- coding: utf-8 -*-
"""P01 Phase A.1 — reproduction check vs frozen anchor.

Runs run_case_mismatch with delta=0 on a dev-subset of the anchor grid and
compares selected_errors / n_select_da / n_select_nda per seed against
ccisp_family1_selector_a_30seed.json. Must match EXACTLY.
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_EXP = _HERE
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _EXP]

from _p01_cpr_snr_mismatch_probe import run_case_mismatch  # noqa: E402

ANCHOR = Path(_SIM_ROOT) / "results" / "ccisp_family1_selector_a_30seed.json"

# Reproduce a focused but representative subset: 3 scenes x {5,9,13,25} dB x seeds 0-9
# (covers low/mid/high SNR and all 3 scenes; 12 cells x 10 seeds = 120 repro cells)
REPRO_SCENES = ["weak", "moderate", "strong"]
REPRO_SNRS = [5.0, 9.0, 13.0, 25.0]
REPRO_SEEDS = list(range(10))   # dev seeds


def main():
    with open(ANCHOR) as f:
        anchor = json.load(f)
    # index anchor by (scene, snr_db, seed_index)
    aidx = {(r["scene"], float(r["snr_db"]), int(r["seed_index"])): r
            for r in anchor["raw"]}

    t0 = time.time()
    n_match = 0
    n_mismatch = 0
    mismatches = []
    for scene in REPRO_SCENES:
        for snr in REPRO_SNRS:
            for seed in REPRO_SEEDS:
                got = run_case_mismatch(scene, snr, delta=0.0, seed_index=seed)
                key = (scene, float(snr), int(seed))
                ref = aidx[key]
                # compare the three load-bearing fields
                fields = ("selected_errors", "n_select_da", "n_select_nda",
                          "fixed_nda_errors", "fixed_da_errors",
                          "lower_count_bound_errors",
                          "true_oracle_errors", "true_oracle_bits")
                ok = all(got[f] == ref[f] for f in fields)
                if ok:
                    n_match += 1
                else:
                    n_mismatch += 1
                    diffs = {f: (got[f], ref[f]) for f in fields if got[f] != ref[f]}
                    mismatches.append((key, diffs))
                if (n_match + n_mismatch) % 10 == 0:
                    print(f"  ...{n_match + n_mismatch} checked "
                          f"({time.time() - t0:.0f}s)", flush=True)

    print("\n=== Reproduction summary ===")
    print(f"matched:   {n_match}")
    print(f"mismatched:{n_mismatch}")
    if mismatches:
        print("\nMISMATCHES (first 10):")
        for key, diffs in mismatches[:10]:
            print(f"  {key}: {diffs}")
    return n_mismatch == 0


if __name__ == "__main__":
    ok = main()
    print("\nRESULT:", "PASS — exact reproduction" if ok else "FAIL — debug before continuing")
    sys.exit(0 if ok else 1)
