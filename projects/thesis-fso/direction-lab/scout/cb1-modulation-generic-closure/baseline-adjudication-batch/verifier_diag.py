"""Diagnostic: trace MMA divergence dynamics and test remediations.

Hypotheses to test:
 (A) The divergence is a genuine MMA block-end instability with center-tap
     init under the specific channel. Look at w_norm trajectory over blocks
     for a divergent seed (11).
 (B) A smaller mu (e.g. 1e-4) prevents divergence. Compare CMA vs MMA at
     matched mu.
 (C) A tighter norm_thresh (e.g. 3x init) just declares divergence earlier
     but doesn't change the underlying instability — i.e. the weights are
     genuinely running away, not just crossing an arbitrary threshold.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
WORKTREE = HERE.parents[6]
SIM_DIR = WORKTREE / "projects" / "simulation"
ATLAS_DIR = WORKTREE / "projects" / "thesis-fso" / "direction-lab" / "scout" / "cb1-modulation-generic-closure" / "baseline-atlas"
BATCH_DIR = WORKTREE / "projects" / "thesis-fso" / "direction-lab" / "scout" / "cb1-modulation-generic-closure" / "baseline-adjudication-batch"

for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import cb1_evaluator as evaluator
from cb1_cell_runner import standard_cma_godard_with_z
from verifier_mma import mma_yang_werner_dumont_cleanroom
from common._dual_pol_channel import generate_shared_realization_dp

N = 32768


def channel(seed):
    return generate_shared_realization_dp(
        N, alpha=4.2, beta=1.4, f_g=30.0, sop_rate=4e-5,
        seed=seed, gamma_bar=100.0, block=100, t_s=4e-10,
        method="gar", modulation="qam16",
    )


print("=" * 78)
print("(A) w_norm trajectory over blocks for seed=11 (divergent) and seed=13 (ok)")
print("=" * 78)
for seed in (11, 13):
    rz = channel(seed)
    out = mma_yang_werner_dumont_cleanroom(rz["rX"], rz["rY"], mu=1e-3)
    tr = out["trace"]
    print(f"\nseed={seed}  diverged={out['diverged']}  final_w_norm={out['final_w_norm']:.3f}  n_blocks={len(tr)}")
    print("  block |   w_norm  |   z_amp_max  |   mma_cost")
    for i in range(0, min(len(tr), 60), 5):
        b = tr[i]
        print(f"  {i:5d} | {b['w_norm']:9.4f} | {b['z_amp_max']:12.4f} | {b['mma_cost']:10.4f}")
    # also show the last few
    print("  ... tail:")
    for i in range(max(0, len(tr) - 4), len(tr)):
        b = tr[i]
        print(f"  {i:5d} | {b['w_norm']:9.4f} | {b['z_amp_max']:12.4f} | {b['mma_cost']:10.4f}")


print()
print("=" * 78)
print("(B) Effect of mu: does a smaller mu prevent divergence for seed=11?")
print("=" * 78)
rz = channel(11)
print(f"\n{'mu':>10} | {'diverged':>10} | {'final_w_norm':>14} | {'diverge_block':>14}")
for mu in (1e-3, 5e-4, 2e-4, 1e-4, 5e-5, 1e-5):
    out = mma_yang_werner_dumont_cleanroom(rz["rX"], rz["rY"], mu=mu)
    # find divergence block
    if out["diverged"]:
        db = None
        for i, b in enumerate(out["trace"]):
            if b["w_norm"] > 10.0:
                db = i
                break
    else:
        db = "-"
    print(f"{mu:>10.0e} | {str(out['diverged']):>10} | {out['final_w_norm']:>14.4f} | {str(db):>14}")


print()
print("=" * 78)
print("(C) Same mu sweep but eval PI-SER if it converges (seeds 11, 12, 14)")
print("=" * 78)
from cb1_cell_runner import eval_window_for
eval_start, calibration_end, eval_end, _ = eval_window_for(N, 11, window_symbols=256, block_size=64)

def pi_ser(rz, out):
    if out["diverged"]:
        return None
    zX, zY = out["zX"], out["zY"]
    z_eval = np.column_stack((zX[calibration_end:eval_end], zY[calibration_end:eval_end]))
    truth_eval = np.column_stack((
        rz["sX"][calibration_end:eval_end], rz["sY"][calibration_end:eval_end],
    ))
    bx = rz["bitsX"][calibration_end * 4:eval_end * 4]
    by = rz["bitsY"][calibration_end * 4:eval_end * 4]
    nearest = evaluator.hard_16qam(z_eval)
    m = evaluator.evaluate_dual_16qam(
        nearest[:, 0], nearest[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bx, by,
    )
    return float(m["pi_ser"])

print(f"\n{'mu':>10} | {'seed=11 pi_ser':>16} | {'seed=12 pi_ser':>16} | {'seed=14 pi_ser':>16} | {'mean (non-div only)':>20}")
for mu in (1e-3, 5e-4, 2e-4, 1e-4, 5e-5, 1e-5):
    vals = []
    cells_str = []
    for seed in (11, 12, 14):
        rz = channel(seed)
        out = mma_yang_werner_dumont_cleanroom(rz["rX"], rz["rY"], mu=mu)
        v = pi_ser(rz, out)
        vals.append(v)
        cells_str.append("DIVERGED" if v is None else f"{v:.4f}")
    valid = [v for v in vals if v is not None]
    mean_v = f"{np.mean(valid):.4f} (n={len(valid)})" if valid else "all diverged"
    print(f"{mu:>10.0e} | {cells_str[0]:>16} | {cells_str[1]:>16} | {cells_str[2]:>16} | {mean_v:>20}")


print()
print("=" * 78)
print("(D) Compare CMA at same mu=1e-3 vs mu=1e-4 on seeds 11,12,14 — is CMA also unstable?")
print("=" * 78)
print(f"\n{'mu':>10} | {'seed=11 CMA pi_ser':>20} | {'seed=12 CMA pi_ser':>20} | {'seed=14 CMA pi_ser':>20}")
for mu in (1e-3, 1e-4):
    cells_str = []
    for seed in (11, 12, 14):
        rz = channel(seed)
        out = standard_cma_godard_with_z(rz["rX"], rz["rY"], n_tap=11, mu=mu, R2=1.32, block_size=64)
        v = pi_ser(rz, out)
        cells_str.append("DIVERGED" if v is None else f"{v:.4f} (w={out['final_w_norm']:.2f})")
    print(f"{mu:>10.0e} | {cells_str[0]:>20} | {cells_str[1]:>20} | {cells_str[2]:>20}")
