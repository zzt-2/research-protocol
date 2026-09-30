"""Round-2 trajectory acquisition (contract_r2.yaml, frozen).

Per batch: (a) NOMS(0.75,0) cap=200 full-syndrome-trajectory decode;
(b) B0 fixed-20 decode (ie20 for all frames = semantics-a FER/BER baseline).

Implementation gates (before any analytic result is read):
  GN1_meta: frame count/seeds/npz fields match the contract manifest.
  GN2_determinism: (i) full-batch: cap200 trajectory prefix s_1..s_20 equals
      the B0x20 run's syndrome weights frame-by-frame (stepped==fresh);
      (ii) 32 sampled frames: B0x20 re-decoded twice, info bits bit-identical.
  GN3_report_only: c2 batches' B0x20 FER vs round-1 same-condition batch
      within +-25% (report item, NOT a gate).

Usage:
    python run_trajectory_r2.py --role dev2
    python run_trajectory_r2.py --role confirm
    python run_trajectory_r2.py --role sweep
    python run_trajectory_r2.py --role single --batch sw_mod_11
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
sys.path.insert(0, str(HERE))

from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402
from gen_batches import BATCHES  # noqa: E402
from _common import CAP  # noqa: E402

ROLES = {
    "dev2": ["dev2_W12"],
    "confirm": ["c2_M15", "c2_W12", "c2_S16"],
    "sweep": [n for n, s in BATCHES.items() if s["role"] == "sweep"],
}
ROUND1_B0_FER = {"c2_M15": 0.2446, "c2_W12": 0.2817, "c2_S16": 0.2515}
ALPHA, OFFSET = 0.75, 0.0
CHUNK = 256


def load_batch(name: str) -> dict:
    d = OUT_ROOT / "llr_cache" / name
    seeds = sorted(int(p.stem.split("_")[1]) for p in d.glob("frame_*.npz"))
    llr = np.empty((len(seeds), 1536), dtype=np.float32)
    truth = np.empty((len(seeds), 1024), dtype=np.uint8)
    for i, s in enumerate(seeds):
        f = np.load(d / f"frame_{s}.npz")
        llr[i] = f["llr"]
        truth[i] = f["truth_info"]
    return {"seeds": np.array(seeds), "llr": llr, "truth": truth}


def decode_full(decoder, data):
    llr, truth = data["llr"], data["truth"]
    n = llr.shape[0]
    sw = np.empty((n, CAP), dtype=np.int32)
    conv = np.empty(n, dtype=np.int64)
    ie200 = np.empty(n, dtype=np.int64)
    for st in range(0, n, CHUNK):
        c, t = llr[st:st + CHUNK], truth[st:st + CHUNK]
        res = decoder.decode(c, num_iter=CAP, alpha=ALPHA, offset=OFFSET,
                             trajectory=True)
        b = c.shape[0]
        sw[st:st + b] = np.array(res["syndrome_weights"], dtype=np.int32)
        conv[st:st + b] = [-1 if x is None else x for x in res["converged_at"]]
        ie200[st:st + b] = (res["info_bits"] != t).sum(axis=1)
    return sw, conv, ie200


def decode_b020(decoder, data):
    llr, truth = data["llr"], data["truth"]
    n = llr.shape[0]
    sw20 = np.empty((n, 20), dtype=np.int32)
    ie20 = np.empty(n, dtype=np.int64)
    for st in range(0, n, CHUNK):
        c, t = llr[st:st + CHUNK], truth[st:st + CHUNK]
        res = decoder.decode(c, num_iter=20, alpha=ALPHA, offset=OFFSET,
                             trajectory=True)
        b = c.shape[0]
        sw20[st:st + b] = np.array(res["syndrome_weights"], dtype=np.int32)
        ie20[st:st + b] = (res["info_bits"] != t).sum(axis=1)
    return sw20, ie20


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", default=None,
                    choices=list(ROLES) + ["single"])
    ap.add_argument("--batch", default=None)
    args = ap.parse_args()
    names = ([args.batch] if args.role == "single" else ROLES[args.role])
    out_name = {"dev2": "raw_traj_r2_dev.json", "confirm": "raw_traj_r2_confirm.json",
                "sweep": "raw_traj_r2_sweep.json", "single": f"raw_traj_r2_{args.batch}.json"}[args.role]

    decoder = RescueDecoder(make_encoder())
    out = {"schema_version": "decode-budget-rule.traj-r2.v1",
           "contract": "explore/decode-budget-rule/contract_r2.yaml (v1, frozen)",
           "alpha": ALPHA, "offset": OFFSET, "cap": CAP, "batches": {}}
    gate_report = {}
    t_all = time.perf_counter()
    for name in names:
        t0 = time.perf_counter()
        # GN1 meta
        spec = BATCHES[name]
        data = load_batch(name)
        want = spec["seeds"][1] - spec["seeds"][0] + 1
        gn1 = len(data["seeds"]) == want and data["seeds"][0] == spec["seeds"][0]
        if not gn1:
            raise SystemExit(f"GN1 FAIL [{name}]: {len(data['seeds'])} frames")

        sw, conv, ie200 = decode_full(decoder, data)
        sw20, ie20 = decode_b020(decoder, data)
        # GN2(i): full-batch prefix equality
        gn2a = int((sw[:, :20] != sw20).any(axis=1).sum())
        if gn2a:
            raise SystemExit(f"GN2 FAIL prefix [{name}]: {gn2a} frames")
        # GN2(ii): 32 sampled frames, B0x20 twice bit-identical
        idx = np.arange(0, len(data["seeds"]), max(len(data["seeds"]) // 32, 1))[:32]
        _, ie20b = decode_b020(decoder, {"llr": data["llr"][idx],
                                         "truth": data["truth"][idx]})
        gn2b = int((ie20[idx] != ie20b).sum())
        if gn2b:
            raise SystemExit(f"GN2 FAIL determinism [{name}]: {gn2b} frames")

        fer20 = float((ie20 > 0).mean())
        gn3 = None
        if name in ROUND1_B0_FER:
            ref = ROUND1_B0_FER[name]
            gn3 = {"b0_fer_this": fer20, "b0_fer_round1": ref,
                   "within_25pct": bool(abs(fer20 - ref) <= 0.25 * ref)}

        # accepted-iterate correctness (grouped by conv)
        acc_ok = np.ones(sw.shape[0], dtype=bool)
        for v in np.unique(conv[conv > 0]):
            gi = np.flatnonzero(conv == v)
            for st in range(0, gi.size, CHUNK):
                sub = gi[st:st + CHUNK]
                res = decoder.decode(data["llr"][sub], num_iter=int(v),
                                     alpha=ALPHA, offset=OFFSET, trajectory=False)
                acc_ok[sub] = (res["info_bits"] == data["truth"][sub]).all(axis=1)

        gate_report[name] = {"GN1": bool(gn1), "GN2_prefix_mismatch": gn2a,
                             "GN2_determinism_mismatch": gn2b, "GN3": gn3}
        out["batches"][name] = {
            "seeds": data["seeds"].tolist(),
            "syndrome_weights": sw.tolist(),
            "converged_at": conv.tolist(),
            "info_errors_at_200": ie200.tolist(),
            "info_errors_at_20": ie20.tolist(),
            "accepted_info_ok": acc_ok.tolist(),
        }
        print(f"[{name}] n={len(data['seeds'])} conv={(conv > 0).mean():.3f} "
              f"fer200={(ie200 > 0).mean():.4f} fer20={fer20:.4f} "
              f"conv_wrong={int(((conv > 0) & ~acc_ok).sum())} "
              f"gates=OK ({time.perf_counter() - t0:.0f}s)", flush=True)

    out["gates"] = gate_report
    path = OUT_ROOT / out_name
    if args.role == "sweep":
        # append mode for sweep (resume across separate invocations)
        existing = {}
        if path.exists():
            existing = json.load(open(path))["batches"]
        existing.update(out["batches"])
        out["batches"] = existing
        g = json.load(open(path))["gates"] if path.exists() else {}
        g.update(gate_report)
        out["gates"] = g
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"written: {path} ({time.perf_counter() - t_all:.0f}s total)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
