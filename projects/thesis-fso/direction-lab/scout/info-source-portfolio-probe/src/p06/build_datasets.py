"""P06 batched dataset builder — resumable, incremental per (phase, fg, snr) chunk.

Run chunks from the worktree root:
  python projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/src/p06/build_datasets.py \
      --phase train --fg 30 --snr 15
Writes one JSON per chunk to results/p06_causal_cross_frame_history/chunks/.
Skips chunks whose output already exists (resumable).
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import run_p06 as P  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=["train", "dev", "test"])
    ap.add_argument("--fg", type=float, required=True)
    ap.add_argument("--snr", type=float, required=True)
    args = ap.parse_args()

    seeds = {"train": P.FROZEN["train_seeds"],
             "dev": P.FROZEN["dev_seeds"],
             "test": P.FROZEN["test_seeds"]}[args.phase]
    out_dir = P.RESULTS_DIR / "chunks"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{args.phase}_fg{int(args.fg)}_snr{int(args.snr)}"
    out_path = out_dir / f"chunk_{tag}.json"
    if out_path.exists():
        print(f"[skip] {out_path} exists", flush=True)
        return

    t0 = time.time()
    print(f"[build] {tag}: {len(seeds)} trajectories...", flush=True)
    rows = P.build_dataset(seeds, args.fg, args.snr, args.phase)
    payload = {"phase": args.phase, "fg_hz": args.fg, "snr_db": args.snr,
               "seeds": seeds, "n_frames": len(rows), "rows": rows}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, default=str)
    # quick stats
    sers = [r["next_fixed_ser"] for r in rows
            if r.get("next_fixed_ser") is not None and r["next_fixed_ser"] == r["next_fixed_ser"]]
    fails = [r["next_fail"] for r in rows if r.get("next_fail") is not None]
    import numpy as np
    print(f"[done] {tag}: {len(rows)} frames in {time.time()-t0:.1f}s "
          f"mean_next_ser={float(np.nanmean(sers)):.4f} "
          f"n_fail={int(np.nansum(fails))}/{len(fails)} "
          f"frac_fail={float(np.nanmean(fails)):.3f}", flush=True)


if __name__ == "__main__":
    main()
