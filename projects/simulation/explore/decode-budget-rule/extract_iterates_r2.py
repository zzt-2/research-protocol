"""Round-2 iterate extraction (contract_r2): metric completion only.

Per batch (confirm + sweep):
  - ie@{10,15,30,50,100} for ALL frames (ie@20/ie@200 already in traj files);
  - ie@stop for A1(C1)/A2(OSC) ablation cut frames at their (arbitrary) stop
    iterates, grouped by iterate value.
Frozen rule RD family cuts at checkpoints only -> covered by the cap set.
Writes raw_iterates_r2.json (append mode for sweep).
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
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"
sys.path.insert(0, str(RESCUE_DIR))
sys.path.insert(0, str(HERE))

from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402
from gen_batches import BATCHES  # noqa: E402
from run_trajectory_r2 import load_batch  # noqa: E402
from _common import (  # noqa: E402
    CAP, CUT_CORRECT, CUT_WRONG, simulate_rule_r2,
)

ALPHA, OFFSET = 0.75, 0.0
CHUNK = 256
CAPS = (10, 15, 30, 50, 100)


def ie_at(decoder, data, k: int, idx: np.ndarray) -> np.ndarray:
    out = np.empty(idx.size, dtype=np.int64)
    for st in range(0, idx.size, CHUNK):
        sub = idx[st:st + CHUNK]
        res = decoder.decode(data["llr"][sub], num_iter=int(k),
                             alpha=ALPHA, offset=OFFSET, trajectory=False)
        out[st:st + CHUNK] = (res["info_bits"] != data["truth"][sub]).sum(axis=1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True,
                    choices=["confirm", "sweep", "single"])
    ap.add_argument("--batch", default=None)
    args = ap.parse_args()
    if args.role == "single":
        names = [args.batch]
    elif args.role == "confirm":
        names = ["c2_M15", "c2_W12", "c2_S16"]
    else:
        names = [n for n, s in BATCHES.items() if s["role"] == "sweep"]

    decoder = RescueDecoder(make_encoder())
    frozen = json.load(open(OUT_DIR / "frozen_rule_r2.json"))
    abl = frozen["ablation_rules"]

    out = {"schema_version": "decode-budget-rule.iterates-r2.v1",
           "contract": "contract_r2 (v1 frozen) -- metric completion, rules read-only",
           "batches": {}}
    t0 = time.perf_counter()
    for name in names:
        data = load_batch(name)
        traj = json.load(open(OUT_DIR / (
            "raw_traj_r2_confirm.json" if args.role == "confirm" else
            "raw_traj_r2_sweep.json")))["batches"]
        if name not in traj and args.role == "single":
            traj = json.load(open(OUT_DIR / f"raw_traj_r2_{name}.json"))["batches"]
        b = traj[name]
        sw = np.array(b["syndrome_weights"], dtype=np.int32)
        conv = np.array(b["converged_at"], dtype=np.int64)
        n = sw.shape[0]
        assert np.array_equal(np.array(b["seeds"]), data["seeds"])

        rec = {f"ie_at_{c}": ie_at(decoder, data, c, np.arange(n)).tolist()
               for c in CAPS}
        # ablation cut-frame stop iterates + ie at those iterates
        for tag, spec in (("A1", abl["A1_gclrpc1"]), ("A2", abl["A2_osc3"])):
            stop, outcome = simulate_rule_r2(sw, conv, spec)
            cut = np.flatnonzero((outcome == CUT_CORRECT) | (outcome == CUT_WRONG))
            rec[f"{tag}_cut_index"] = cut.tolist()
            rec[f"{tag}_cut_stop"] = stop[cut].tolist()
            ie = np.empty(cut.size, dtype=np.int64)
            for v in np.unique(stop[cut]):
                sub = cut[stop[cut] == v]
                ie[stop[cut] == v] = ie_at(decoder, data, int(v), sub)
            rec[f"{tag}_cut_ie_at_stop"] = ie.tolist()
        out["batches"][name] = rec
        print(f"[{name}] extracted ({time.perf_counter() - t0:.0f}s)", flush=True)

    path = OUT_DIR / "raw_iterates_r2.json"
    if args.role == "sweep":
        if path.exists():
            prev = json.load(open(path))
            prev["batches"].update(out["batches"])
            out["batches"] = prev["batches"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"written: {path} ({time.perf_counter() - t0:.0f}s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
