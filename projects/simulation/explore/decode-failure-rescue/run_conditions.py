"""Applicability-condition exploration for decode-failure-rescue
(conditions_contract.yaml; user prompt 2026-09-20, conditions round).

Runs the SAME four arms and unified rules as the confirmation round
(run_confirm.py) at NEW working conditions (SNR and/or sourced Gamma-Gamma
turbulence level), each on its own fresh seed block through the real signal
generation chain (generate_llrs with snr/turbulence overrides):

  B0  NOMS(0.75,0) 20 it
  R1  stage1=B0; hot-continue same config +20 it early stop
  R3  stage1=B0; hot-continue switched (0.875,0.1) +20 it early stop
  F   stage1=fresh (0.875,0.1) 20 it; own-failure hot-continue +20 it

Per condition this writes (old artifacts untouched):
  llr_cache/{tag}/frame_*.npz, generation_meta_{tag}.json,
  raw_{tag}.json, summary_{tag}.json (includes composition band table).

The composition band table is the mechanism lens frozen from the 15 dB
anchor analysis (analysis_confirm2048_features.json): channel hard-decision
error bands [0,100) / [100,140) / [140,160) / [160,220) / [220,320) / [320,+)
with per-band R1/R3 rescue counts.  ch_hd_errors is truth-based and used for
EXPLANATION ONLY (never as a deployment signal).

Usage:
    python run_conditions.py --tag dev_W13 --seeds 40000:40511 \
        --snr-db 13.0 --turb-alpha 11.6 --turb-beta 10.1
    python run_conditions.py --tag dev_W13 --analyze-only   # bands on existing raw
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "results" / "decode-failure-rescue"

from rescue_decoder import RescueDecoder, make_encoder          # noqa: E402
from run_confirm import run_one_frame, summarize_confirm        # noqa: E402

BANDS = [(0, 100), (100, 140), (140, 160), (160, 220), (220, 320), (320, 10**9)]


def cache_tag(tag: str, snr_db: float, turb: tuple[float, float]) -> str:
    """Replicates generate_llrs.cache_dir naming: {tag}_snr{X}_turb{A}x{B}."""
    return f"{tag}_snr{snr_db:g}_turb{turb[0]:g}x{turb[1]:g}"


def generate_condition(tag: str, seeds: list[int], snr_db: float,
                       turb: tuple[float, float]) -> None:
    import generate_llrs as gl

    gl.SPLITS[tag] = {"start": seeds[0], "stop_inclusive": seeds[-1]}
    argv = ["generate_llrs.py", "--split", tag, "--snr-db-override", str(snr_db),
            "--turb-alpha-override", str(turb[0]), "--turb-beta-override", str(turb[1])]
    sys.argv = argv
    gl.main()


def load_frames(tag: str, expected: int, *, cache_name: str | None = None) -> list[dict[str, Any]]:
    directory = RESULTS / "llr_cache" / (cache_name or tag)
    frames = []
    for path in sorted(directory.glob("frame_*.npz")):
        with np.load(path) as data:
            frames.append({
                "seed": int(data["seed"]),
                "frame_index": int(data["frame_index"]),
                "llr": data["llr"].astype(np.float32),
                "truth_info": data["truth_info"].astype(np.uint8),
                "truth_coded": data["truth_coded"].astype(np.uint8),
                "llr_sha256": str(data["llr_sha256"]),
            })
    frames.sort(key=lambda f: f["seed"])
    if len(frames) != expected:
        raise RuntimeError(f"condition cache incomplete: {len(frames)}/{expected}")
    return frames


def channel_hd_errors(frames: list[dict[str, Any]]) -> dict[int, int]:
    out = {}
    for f in frames:
        hd = (f["llr"] > 0).astype(np.uint8)  # llr>0 -> bit1 (probed convention)
        out[f["seed"]] = int(np.count_nonzero(hd != f["truth_coded"]))
    return out


def composition_table(records: list[dict[str, Any]],
                      ch_err: dict[int, int]) -> dict[str, Any]:
    b0_wrong = [r for r in records if r["B0"]["info_errors"] > 0]
    rows = []
    for r in b0_wrong:
        r1 = r["arms"]["R1"]["final"]["info_errors"] == 0
        r3 = r["arms"]["R3"]["final"]["info_errors"] == 0
        rows.append((ch_err[r["seed"]], r1, r3))
    bands = {}
    for lo, hi in BANDS:
        band = [x for x in rows if lo <= x[0] < hi]
        bands[f"[{lo},{hi if hi < 10**9 else 'inf'})"] = {
            "n": len(band),
            "r1_rescued": sum(1 for x in band if x[1]),
            "r3_rescued": sum(1 for x in band if x[2]),
        }
    errs = np.array([x[0] for x in rows], dtype=float)
    return {
        "b0_failed": len(b0_wrong),
        "ch_hd_err_quantiles": ({q: float(np.percentile(errs, q))
                                 for q in (10, 25, 50, 75)} if len(errs) else {}),
        "bands": bands,
        "marginal_band_fraction_of_failures": (
            (bands["[100,140)"]["n"] / len(b0_wrong)) if b0_wrong else None),
        "note": "ch_hd_errors is truth-based, explanation only",
    }


def run_condition(tag: str, seeds: list[int], snr_db: float,
                  turb: tuple[float, float]) -> None:
    cname = cache_tag(tag, snr_db, turb)
    t0 = time.perf_counter()
    generate_condition(tag, seeds, snr_db, turb)
    t_gen = time.perf_counter() - t0

    frames = load_frames(tag, len(seeds), cache_name=cname)
    decoder = RescueDecoder(make_encoder())

    ckpt = RESULTS / f"raw_{tag}.checkpoint.jsonl"
    done: set[int] = set()
    if ckpt.exists():
        for line in ckpt.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["seed"])
    todo = [f for f in frames if f["seed"] not in done]
    t1 = time.perf_counter()
    with ckpt.open("a", encoding="utf-8") as cp:
        for i, frame in enumerate(todo):
            cp.write(json.dumps(run_one_frame(decoder, frame)) + "\n")
            cp.flush()
            if (i + 1) % 128 == 0:
                print(f"  {i + 1}/{len(todo)} frames ({time.perf_counter() - t1:.1f}s)",
                      flush=True)
    t_dec = time.perf_counter() - t1

    records = [json.loads(line) for line in
               ckpt.read_text(encoding="utf-8").splitlines() if line.strip()]
    records.sort(key=lambda r: r["seed"])
    raw = {
        "schema_version": "dfr.condition.raw.v1",
        "condition": {"tag": tag, "snr_db": snr_db,
                      "turbulence_alpha": turb[0], "turbulence_beta": turb[1],
                      "seeds": {"start": seeds[0], "stop_inclusive": seeds[-1],
                                "count": len(seeds)}},
        "rules": {
            "output": "stage2 accepted (syndrome==0, early-stop iterate) -> "
                      "stage2 output; else stage1 output with failure flag",
            "trigger": "per-arm own stage-1 syndrome!=0 (R1/R3 stage1 = B0)",
            "truth_access": "scoring only",
        },
        "frames": records,
    }
    (RESULTS / f"raw_{tag}.json").write_text(json.dumps(raw, indent=1), encoding="utf-8")

    summary = summarize_confirm(records)
    summary["split"] = tag
    summary["condition"] = raw["condition"]
    summary["composition"] = composition_table(records, channel_hd_errors(frames))
    summary["wall_seconds"] = {"generate": t_gen, "decode": t_dec}
    (RESULTS / f"summary_{tag}.json").write_text(json.dumps(summary, indent=2),
                                                 encoding="utf-8")
    print(json.dumps({
        "tag": tag,
        "b0_fer": summary["arms"]["B0"]["fer"],
        "r1": summary["arms"]["R1"]["info_error_frames"],
        "r3": summary["arms"]["R3"]["info_error_frames"],
        "f": summary["arms"]["F"]["info_error_frames"],
        "r3_vs_r1": summary["paired"]["R3_vs_R1"],
        "composition_marginal_frac":
            summary["composition"]["marginal_band_fraction_of_failures"],
    }, indent=1))


def analyze_only(tag: str, seeds: list[int], snr_db: float,
                 turb: tuple[float, float]) -> None:
    raw = json.loads((RESULTS / f"raw_{tag}.json").read_text(encoding="utf-8"))
    frames = load_frames(tag, len(seeds), cache_name=cache_tag(tag, snr_db, turb))
    summary = json.loads((RESULTS / f"summary_{tag}.json").read_text(encoding="utf-8"))
    summary["composition"] = composition_table(raw["frames"], channel_hd_errors(frames))
    (RESULTS / f"summary_{tag}.json").write_text(json.dumps(summary, indent=2),
                                                 encoding="utf-8")
    print(json.dumps(summary["composition"], indent=1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True,
                        help="condition tag, e.g. dev_W13 (also the cache/raw suffix)")
    parser.add_argument("--seeds", required=True,
                        help="inclusive range start:stop, e.g. 40000:40511")
    parser.add_argument("--snr-db", type=float, required=True)
    parser.add_argument("--turb-alpha", type=float, required=True)
    parser.add_argument("--turb-beta", type=float, required=True)
    parser.add_argument("--analyze-only", action="store_true",
                        help="only (re)compute the composition table on existing raw")
    args = parser.parse_args()

    start, stop = (int(x) for x in args.seeds.split(":"))
    seeds = list(range(start, stop + 1))
    if args.analyze_only:
        analyze_only(args.tag, seeds, args.snr_db, (args.turb_alpha, args.turb_beta))
    else:
        run_condition(args.tag, seeds, args.snr_db, (args.turb_alpha, args.turb_beta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
