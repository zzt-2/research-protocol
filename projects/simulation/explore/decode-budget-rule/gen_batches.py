"""Round-2 batch generation (contract_r2.yaml, D063 authorization).

Generates all new LLR caches by read-only import of the frozen T077 chain
(decode-failure-rescue/generate_llrs.build_frame) with SNR/turbulence
overrides -- identical mechanism to the round-1 conditions batches.
Resume-safe: existing npz frames are skipped.

Usage:
    python gen_batches.py --only dev2_W12        # one batch
    python gen_batches.py                        # all, in contract order
    python gen_batches.py --smoke                # 2 frames per batch, no meta
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
RESCUE_DIR = SIM_ROOT / "explore" / "decode-failure-rescue"
OUT_ROOT = SIM_ROOT / "results" / "decode-budget-rule"
sys.path.insert(0, str(RESCUE_DIR))

import generate_llrs as gl  # noqa: E402  (read-only import)

MOD, WEAK, STRG = (4.0, 1.9), (11.6, 10.1), (4.2, 1.4)

BATCHES: dict[str, dict] = {
    "dev2_W12": dict(seeds=(46000, 47023), snr=12.0, turb=WEAK, role="dev_ext"),
    "c2_M15":   dict(seeds=(60000, 62047), snr=15.0, turb=MOD,  role="confirm"),
    "c2_W12":   dict(seeds=(70000, 72047), snr=12.0, turb=WEAK, role="confirm"),
    "c2_S16":   dict(seeds=(80000, 82047), snr=16.0, turb=STRG, role="confirm"),
}
# 14 sweep points, seeds 90000 + 3000*k (disjoint, k = enumeration order)
_SWEEP = (
    [("mod", s, MOD) for s in (11, 12, 13, 14, 16, 17)]
    + [("weak", s, WEAK) for s in (10, 11, 13, 14)]
    + [("strg", s, STRG) for s in (14, 15, 17, 18)]
)
for _k, (_tier, _snr, _turb) in enumerate(_SWEEP):
    BATCHES[f"sw_{_tier}_{_snr}"] = dict(
        seeds=(90000 + 3000 * _k, 90000 + 3000 * _k + 2047),
        snr=float(_snr), turb=_turb, role="sweep")


def gen_batch(name: str, spec: dict, smoke: bool = False) -> None:
    sc = gl._load_single_cell()
    codec = sc._correctness().TargetApskCodec()
    target = OUT_ROOT / "llr_cache" / name
    target.mkdir(parents=True, exist_ok=True)
    seeds = list(range(spec["seeds"][0], spec["seeds"][1] + 1))
    if smoke:
        seeds = seeds[:2]
    ta, tb = spec["turb"]
    generated = skipped = 0
    t0 = time.perf_counter()
    timings = []
    for fi, seed in enumerate(seeds):
        out = target / f"frame_{seed}.npz"
        if out.exists():
            skipped += 1
            continue
        t1 = time.perf_counter()
        frame = gl.build_frame(
            sc, codec, seed=seed, snr_db_override=spec["snr"],
            turb_alpha_override=ta, turb_beta_override=tb)
        timings.append(time.perf_counter() - t1)
        np.savez_compressed(
            out,
            llr=frame["llr"], truth_info=frame["truth_info"],
            truth_coded=frame["truth_coded"], llr_sha256=frame["llr_sha256"],
            received_observation_sha256=frame["received_observation_sha256"],
            seed=np.int64(seed), frame_index=np.int64(fi),
            split=f"r2_{name}", snr_db=spec["snr"],
            snr_db_manifest=float(sc.load_manifest()["cell"]["snr_db"]),
            snr_db_override=np.float64(spec["snr"]),
            turbulence_alpha=ta, turbulence_beta=tb,
            turbulence_alpha_override=np.float64(ta),
            turbulence_beta_override=np.float64(tb),
            source_refs=json.dumps(gl.SOURCE_REFS),
        )
        generated += 1
        if generated % 256 == 0:
            print(f"[{name}] {generated} frames "
                  f"({time.perf_counter() - t0:.0f}s)", flush=True)
    if not smoke:
        import sionna, torch
        meta = {
            "schema_version": "decode-budget-rule.llr-cache.gen-r2.v1",
            "batch": name, "role": spec["role"],
            "snr_db": spec["snr"], "turbulence": list(spec["turb"]),
            "seeds": {"start": seeds[0], "stop_inclusive": seeds[-1],
                      "count": len(seeds)},
            "generated": generated, "skipped_existing": skipped,
            "mean_frame_seconds": (float(np.mean(timings)) if timings else None),
            "contract": "explore/decode-budget-rule/contract_r2.yaml (v1, frozen)",
            "versions": {"python": sys.version.split()[0],
                         "sionna": sionna.__version__, "torch": torch.__version__,
                         "numpy": np.__version__},
        }
        mdir = OUT_ROOT / "generation_meta_r2"
        mdir.mkdir(parents=True, exist_ok=True)
        (mdir / f"{name}.json").write_text(json.dumps(meta, indent=2),
                                           encoding="utf-8")
    print(f"[{name}] done: generated={generated} skipped={skipped} "
          f"({time.perf_counter() - t0:.0f}s)", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="single batch name")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    names = [args.only] if args.only else list(BATCHES)
    for n in names:
        gen_batch(n, BATCHES[n], smoke=args.smoke)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
