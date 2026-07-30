# -*- coding: utf-8 -*-
"""P01 Phase A.4 — semantic smoke + multidelta equivalence check.

Two checks before scaling to the full dev scan:
  (1) multidelta runner == run_case_mismatch for each delta (correctness of fast path).
  (2) Semantic smoke:
      - delta=0 → selection error rate vs delta=0 baseline == 0, gain retention == 0.
      - delta→+inf → CV boundary pushes MORE windows to NDA (n_select_nda monotone
        non-decreasing in delta). Equivalently n_select_da non-increasing as delta rises.
      - delta→-inf → opposite (more DA).
"""
import os
import sys
import time
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

from _p01_cpr_snr_mismatch_probe import (  # noqa: E402
    run_case_mismatch, run_case_multidelta, DELTAS, N_WINDOWS,
)
import _a4_switch_common768_30seed as A  # noqa: E402

EXTREME_POS = (+8.0, +15.0, +30.0)   # delta→+inf proxy
EXTREME_NEG = (-8.0, -15.0, -30.0)   # delta→-inf proxy


def main():
    t0 = time.time()
    # ---- (1) equivalence: 1 scene x 1 snr x 1 seed x all 7 deltas ----
    scene, snr, seed = "weak", 9.0, 3
    md = run_case_multidelta(scene, snr, seed, deltas=DELTAS)
    print("=== (1) multidelta == run_case_mismatch, per delta ===")
    n_eq = 0
    for delta in DELTAS:
        single = run_case_mismatch(scene, snr, delta, seed)
        per = md["per_delta_orig"][delta]
        ok = (per["n_select_da"] == single["n_select_da"]
              and per["n_select_nda"] == single["n_select_nda"]
              and per["selected_errors"] == single["selected_errors"]
              and md["base"]["fixed_nda_errors"] == single["fixed_nda_errors"]
              and md["base"]["fixed_da_errors"] == single["fixed_da_errors"])
        n_eq += ok
        print(f"  delta={delta:+.0f}: multidelta(sel={per['selected_errors']},"
              f" da={per['n_select_da']}, nda={per['n_select_nda']}) "
              f"== single(sel={single['selected_errors']},"
              f" da={single['n_select_da']}, nda={single['n_select_nda']}): {ok}")
    print(f"equivalence: {n_eq}/{len(DELTAS)} deltas exact match")
    assert n_eq == len(DELTAS), "multidelta fast path mismatch!"

    # ---- (2) semantic smoke ----
    print("\n=== (2) semantic smoke ===")
    # delta=0 identity: choices under delta=0 are the baseline → selection error rate 0
    base_choices = md["per_delta_orig"][0.0]["choices"]
    # gain retention at delta=0 must be exactly 0 (selector == itself)
    sel0 = md["per_delta_orig"][0.0]["selected_errors"]
    nda0 = md["base"]["fixed_nda_errors"]
    gain0 = 10 * np.log10(nda0 / sel0) if sel0 > 0 else 0.0
    print(f"  delta=0: selected_errors={sel0}, nda_common768={nda0}, gain_db={gain0:+.4f}")
    print(f"           (gain retention vs delta=0 = 0 by construction: identity OK)")

    # selection error rate vs delta=0 baseline (fraction of windows that flip)
    print("  selection error rate (windows differing from delta=0 baseline):")
    for delta in DELTAS:
        ch = md["per_delta_orig"][delta]["choices"]
        flips = sum(1 for a, b in zip(base_choices, ch) if a != b)
        print(f"    delta={delta:+.0f}: {flips}/{N_WINDOWS} = {flips/N_WINDOWS:.3f}")

    # monotonicity: as delta → +inf, CV boundary rises → more windows pass CV test → more NDA
    all_deltas_extreme = sorted(set(DELTAS) | set(EXTREME_POS) | set(EXTREME_NEG))
    md_ext = run_case_multidelta(scene, snr, seed, deltas=all_deltas_extreme)
    print("\n  branch occupancy vs delta (weak@9dB, seed 3):")
    print(f"    {'delta':>7}{'n_da':>6}{'n_nda':>7}{'sel_err':>9}")
    for delta in all_deltas_extreme:
        per = md_ext["per_delta_orig"][delta]
        print(f"    {delta:+7.0f}{per['n_select_da']:>6}{per['n_select_nda']:>7}"
              f"{per['selected_errors']:>9}")

    n_da_seq = [md_ext["per_delta_orig"][d]["n_select_da"] for d in all_deltas_extreme]
    monotone_da = all(n_da_seq[i] >= n_da_seq[i+1]
                      for i in range(len(n_da_seq) - 1))
    print(f"  n_select_da non-increasing in delta (monotone): {monotone_da}")
    print(f"  (delta→+inf should push → NDA, so DA count falls; "
          f"delta→-inf should push → DA, so DA count rises)")

    print(f"\nelapsed {time.time()-t0:.0f}s")
    return monotone_da


if __name__ == "__main__":
    ok = main()
    print("\nSMOKE RESULT:", "PASS" if ok else "FAIL — investigate before scaling")
    sys.exit(0 if ok else 1)
