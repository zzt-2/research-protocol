"""Reproduce key cell 16qam-snr20-sop40e-N32768 with seeds 11-15.

Runs three equalizers on identical shared channel realizations:
  - CMA anchor (standard_cma_godard_with_z, R2=1.32)
  - Main-dialog MMA (mma_comparator.mma_yang_werner_dumont)  [read-only]
  - Clean-room MMA (verifier_mma.mma_yang_werner_dumont_cleanroom)

Reports per-seed near-PI-SER and final_w_norm for each.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
WORKTREE = HERE.parents[8]  # verifier_run.py -> batch -> closure -> scout -> direction-lab -> thesis-fso -> projects -> worktree
# verifier_run.py path:
#   worktree/projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/baseline-adjudication-batch/verifier_run.py
# parents[0]=baseline-adjudication-batch
# parents[1]=cb1-modulation-generic-closure
# parents[2]=scout
# parents[3]=direction-lab
# parents[4]=thesis-fso
# parents[5]=projects
# parents[6]=worktree
WORKTREE = HERE.parents[6]

SIM_DIR = WORKTREE / "projects" / "simulation"
ATLAS_DIR = WORKTREE / "projects" / "thesis-fso" / "direction-lab" / "scout" / "cb1-modulation-generic-closure" / "baseline-atlas"
BATCH_DIR = WORKTREE / "projects" / "thesis-fso" / "direction-lab" / "scout" / "cb1-modulation-generic-closure" / "baseline-adjudication-batch"

for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import cb1_cell_runner as runner
import cb1_evaluator as evaluator
from cb1_cell_runner import standard_cma_godard_with_z, eval_window_for
from verifier_mma import mma_yang_werner_dumont_cleanroom

# Read-only import of main dialog's MMA for side-by-side comparison
import mma_comparator as main_mma


def run_one(seed: int) -> dict:
    N = 32768
    realization = main_mma.generate_shared_realization_dp if hasattr(main_mma, "generate_shared_realization_dp") else None
    # Use the same generator the cell runner uses
    from common._dual_pol_channel import generate_shared_realization_dp
    rz = generate_shared_realization_dp(
        N, alpha=4.2, beta=1.4, f_g=30.0, sop_rate=4e-5,
        seed=seed, gamma_bar=100.0, block=100, t_s=4e-10,
        method="gar", modulation="qam16",
    )
    rX, rY = rz["rX"], rz["rY"]

    eval_start, calibration_end, eval_end, half_taps = eval_window_for(
        N, 11, window_symbols=256, block_size=64,
    )

    out: dict[str, dict] = {}

    # --- CMA anchor ---
    cma = standard_cma_godard_with_z(rX, rY, n_tap=11, mu=1e-3, R2=1.32, block_size=64)
    out["cma"] = _eval(rz, cma, eval_start, calibration_end, eval_end)

    # --- Main-dialog MMA ---
    mma_main = main_mma.mma_yang_werner_dumont(rX, rY, n_tap=11, mu=1e-3, block_size=64)
    out["mma_main"] = _eval(rz, mma_main, eval_start, calibration_end, eval_end)

    # --- Clean-room MMA ---
    mma_clean = mma_yang_werner_dumont_cleanroom(
        rX, rY, n_tap=11, mu=1e-3, R_R2=0.82, R_I2=0.82, block_size=64,
    )
    out["mma_clean"] = _eval(rz, mma_clean, eval_start, calibration_end, eval_end)

    return out


def _eval(rz, raw, eval_start, calibration_end, eval_end) -> dict:
    zX = np.asarray(raw["zX"])
    zY = np.asarray(raw["zY"])
    z_calib = np.column_stack((zX[eval_start:calibration_end], zY[eval_start:calibration_end]))
    z_eval = np.column_stack((zX[calibration_end:eval_end], zY[calibration_end:eval_end]))
    truth_calib = np.column_stack((
        rz["sX"][eval_start:calibration_end], rz["sY"][eval_start:calibration_end],
    ))
    truth_eval = np.column_stack((
        rz["sX"][calibration_end:eval_end], rz["sY"][calibration_end:eval_end],
    ))
    bits_x_calib = rz["bitsX"][eval_start * 4:calibration_end * 4]
    bits_y_calib = rz["bitsY"][eval_start * 4:calibration_end * 4]
    bits_x_eval = rz["bitsX"][calibration_end * 4:eval_end * 4]
    bits_y_eval = rz["bitsY"][calibration_end * 4:eval_end * 4]

    res: dict = {
        "diverged": bool(raw["diverged"]),
        "final_w_norm": float(raw["final_w_norm"]),
        "init_w_norm": float(raw["init_w_norm"]),
        "divergence_symbol": raw.get("divergence_symbol"),
    }

    if raw["diverged"]:
        res["near_pi_ser"] = None
        return res

    nearest_predicted = evaluator.hard_16qam(z_eval)
    nearest_m = evaluator.evaluate_dual_16qam(
        nearest_predicted[:, 0], nearest_predicted[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    res["near_pi_ser"] = float(nearest_m["pi_ser"])
    return res


def main():
    rows = []
    for seed in (11, 12, 13, 14, 15):
        print(f"\n=== seed {seed} ===")
        out = run_one(seed)
        row = {"seed": seed}
        for k, v in out.items():
            row[k] = v
            print(f"  {k:12s} diverged={v['diverged']} final_w_norm={v['final_w_norm']:.3f} near_pi_ser={v['near_pi_ser']}")
        rows.append(row)

    print("\n=== summary ===")
    print(f"{'seed':>6} | {'CMA pi_ser':>12} | {'main MMA pi_ser / w_norm':>28} | {'clean MMA pi_ser / w_norm':>28}")
    for r in rows:
        def fmt(v):
            if v["diverged"]:
                return f"DIVERGED (w={v['final_w_norm']:.2f})"
            return f"{v['near_pi_ser']:.4f} (w={v['final_w_norm']:.2f})"
        print(f"{r['seed']:>6} | {fmt(r['cma']):>12} | {fmt(r['mma_main']):>28} | {fmt(r['mma_clean']):>28}")

    # Save raw
    out_path = BATCH_DIR / "verifier_repro.json"
    json.dump({"rows": rows}, open(out_path, "w"), indent=2, default=str)
    print(f"\nSaved raw to {out_path}")


if __name__ == "__main__":
    main()
