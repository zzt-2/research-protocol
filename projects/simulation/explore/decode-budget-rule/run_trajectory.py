"""decode-budget-rule trajectory acquisition (contract.yaml v1, frozen).

Runs NOMS(0.75,0) fresh cap=200 decodes with full per-iteration syndrome
logging on the dev batches (--split dev, rule design data) or the three
confirm batches (--split confirm, single post-freeze run).

Implementation gates enforced BEFORE any analytic result is read:
  G1: first 20 syndrome weights match raw_*{batch}.json B0.syndrome_weights
      (all batches, 0-tolerance).
  G2: confirm batches additionally match raw_capability.json NOMS200 arm
      (converged_at and final info_errors, per frame, 0-tolerance).

Also measures accepted-iterate correctness (converged_wrong under acceptance
semantics) via grouped fresh decodes stopped at converged_at -- closes the
codeword-oscillation gap noted in R036 N6.

Usage:
    python run_trajectory.py --split dev
    python run_trajectory.py --split confirm
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
RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"
CAPAB_DIR = SIM_ROOT / "results" / "decode-capability-audit"
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"

if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))
if str(RESCUE_DIR) not in sys.path:
    sys.path.insert(0, str(RESCUE_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402
from _common import CAP  # noqa: E402

BATCHES = {
    "dev": {
        "dev": ("dev", "raw_dev.json"),
        "dev_M14": ("dev_M14_snr14_turb4x1.9", "raw_dev_M14.json"),
        "dev_W12": ("dev_W12_snr12_turb11.6x10.1", "raw_dev_W12.json"),
        "dev_S16": ("dev_S16_snr16_turb4.2x1.4", "raw_dev_S16.json"),
    },
    "confirm": {
        "M15": ("confirm2048", "raw_confirm2048.json"),
        "W12": ("confirm_W12_snr12_turb11.6x10.1", "raw_confirm_W12.json"),
        "S16": ("confirm_S16_snr16_turb4.2x1.4", "raw_confirm_S16.json"),
    },
}

ALPHA, OFFSET = 0.75, 0.0
CHUNK = 256


def load_batch(cache_dir: Path) -> dict[str, np.ndarray]:
    seeds = sorted(int(p.stem.split("_")[1]) for p in cache_dir.glob("frame_*.npz"))
    n = len(seeds)
    llr = np.empty((n, 1536), dtype=np.float32)
    truth_info = np.empty((n, 1024), dtype=np.uint8)
    for i, seed in enumerate(seeds):
        f = np.load(cache_dir / f"frame_{seed}.npz")
        llr[i] = f["llr"]
        truth_info[i] = f["truth_info"]
    return {"seeds": np.array(seeds), "llr": llr, "truth_info": truth_info}


def decode_full(decoder: RescueDecoder, data: dict) -> dict:
    """Fresh cap=200 NOMS decode with full trajectory -> per-frame arrays."""
    llr, truth = data["llr"], data["truth_info"]
    n = llr.shape[0]
    sw = np.empty((n, CAP), dtype=np.int32)
    conv = np.empty(n, dtype=np.int64)
    ie200 = np.empty(n, dtype=np.int64)
    for start in range(0, n, CHUNK):
        chunk = llr[start:start + CHUNK]
        tchunk = truth[start:start + CHUNK]
        res = decoder.decode(
            chunk, num_iter=CAP, alpha=ALPHA, offset=OFFSET, trajectory=True
        )
        b = chunk.shape[0]
        sw[start:start + b] = np.array(res["syndrome_weights"], dtype=np.int32)
        conv[start:start + b] = [
            -1 if c is None else c for c in res["converged_at"]
        ]
        ie200[start:start + b] = (res["info_bits"] != tchunk).sum(axis=1)
    return {"sw": sw, "conv": conv, "ie200": ie200}


def accepted_info_check(decoder: RescueDecoder, data: dict, conv: np.ndarray) -> np.ndarray:
    """Correctness of the accepted (first-syndrome-0) iterate per frame.

    Frames grouped by converged_at value; a fresh decode stopped exactly at
    converged_at has its final iterate = the accepted iterate (flooding
    statelessness). Never-converged frames get True (unused).
    """
    n = conv.shape[0]
    ok = np.ones(n, dtype=bool)
    for v in np.unique(conv[conv > 0]):
        idx = np.flatnonzero(conv == v)
        for start in range(0, idx.size, CHUNK):
            sub = idx[start:start + CHUNK]
            res = decoder.decode(
                data["llr"][sub], num_iter=int(v),
                alpha=ALPHA, offset=OFFSET, trajectory=False,
            )
            ok[sub] = (res["info_bits"] == data["truth_info"][sub]).all(axis=1)
    return ok


def gate_g1(sw: np.ndarray, seeds: np.ndarray, raw_path: Path) -> list[int]:
    raw = json.load(open(raw_path))
    ref = {fr["seed"]: fr["B0"]["syndrome_weights"] for fr in raw["frames"]}
    mism = []
    for i, seed in enumerate(seeds):
        if list(sw[i, :20]) != list(ref[int(seed)]):
            mism.append(int(seed))
    return mism


def gate_g2(conv: np.ndarray, ie200: np.ndarray, seeds: np.ndarray,
            cond: str) -> list[int]:
    cap = json.load(open(CAPAB_DIR / "raw_capability.json"))
    cdata = cap["conditions"][cond]
    arm = cdata["arms"]["NOMS200"]
    ref_conv = np.array(arm["converged_at"], dtype=np.int64)
    ref_ie = np.array(arm["info_errors"], dtype=np.int64)
    ref_seeds = np.array(cdata["seeds"])
    pos = {int(s): i for i, s in enumerate(ref_seeds)}
    mism = []
    for i, seed in enumerate(seeds):
        j = pos[int(seed)]
        if int(conv[i]) != int(ref_conv[j]) or int(ie200[i]) != int(ref_ie[j]):
            mism.append(int(seed))
    return mism


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=["dev", "confirm"])
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    decoder = RescueDecoder(make_encoder())

    out: dict = {"schema_version": f"decode-budget-rule.traj.{args.split}.v1",
                 "contract": "explore/decode-budget-rule/contract.yaml (v1, frozen)",
                 "alpha": ALPHA, "offset": OFFSET, "cap": CAP,
                 "batches": {}}
    gate_report: dict = {}

    t_all = time.perf_counter()
    for name, (cache, raw_name) in BATCHES[args.split].items():
        t0 = time.perf_counter()
        data = load_batch(RESULTS_ROOT / "llr_cache" / cache)
        run = decode_full(decoder, data)
        # G1 (before anything downstream is read)
        g1 = gate_g1(run["sw"], data["seeds"], RESULTS_ROOT / raw_name)
        if g1:
            raise SystemExit(f"G1 FAIL [{name}]: {len(g1)} frames, e.g. {g1[:5]}")
        # G2 (confirm only)
        g2: list[int] = []
        if args.split == "confirm":
            g2 = gate_g2(run["conv"], run["ie200"], data["seeds"], name)
            if g2:
                raise SystemExit(f"G2 FAIL [{name}]: {len(g2)} frames, e.g. {g2[:5]}")
        acc_ok = accepted_info_check(decoder, data, run["conv"])
        conv_wrong = int(((run["conv"] > 0) & ~acc_ok).sum())

        gate_report[name] = {"G1_first20_mismatch": len(g1),
                             "G2_nomos200_mismatch": len(g2)}
        out["batches"][name] = {
            "seeds": data["seeds"].tolist(),
            "syndrome_weights": run["sw"].tolist(),
            "converged_at": run["conv"].tolist(),
            "info_errors_at_200": run["ie200"].tolist(),
            "accepted_info_ok": acc_ok.tolist(),
        }
        dt = time.perf_counter() - t0
        print(f"[{name}] n={len(data['seeds'])} conv_rate={(run['conv'] > 0).mean():.3f} "
              f"fer200={(run['ie200'] > 0).mean():.4f} conv_wrong={conv_wrong} "
              f"G1=0 G2={len(g2)} ({dt:.0f}s)", flush=True)

    out["gates"] = gate_report
    out_path = OUT_DIR / f"raw_traj_{args.split}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"written: {out_path} ({time.perf_counter() - t_all:.0f}s total)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
