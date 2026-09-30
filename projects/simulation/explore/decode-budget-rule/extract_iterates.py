"""decode-budget-rule iterate extraction (contract amend v1.1 + task 2).

One additional deterministic decode pass per confirm batch, metric completion
only -- the frozen rule is read, never modified:
  - info_errors at iterate 10 and 15 for ALL frames (task-2 fixed-cap points);
  - info_errors at the rule's cut iterate for CUT frames (semantics-a FER).

No design feedback: outputs feed scoring only.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
RESCUE_DIR = SIM_ROOT / "explore" / "decode-failure-rescue"
RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"

if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))
if str(RESCUE_DIR) not in sys.path:
    sys.path.insert(0, str(RESCUE_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402
from _common import CAP, CUT_CORRECT, CUT_WRONG, simulate_rule  # noqa: E402

CONFIRM = {
    "M15": "confirm2048",
    "W12": "confirm_W12_snr12_turb11.6x10.1",
    "S16": "confirm_S16_snr16_turb4.2x1.4",
}
ALPHA, OFFSET = 0.75, 0.0
CHUNK = 256


def load_batch(cache_dir: Path) -> dict:
    seeds = sorted(int(p.stem.split("_")[1]) for p in cache_dir.glob("frame_*.npz"))
    llr = np.empty((len(seeds), 1536), dtype=np.float32)
    truth = np.empty((len(seeds), 1024), dtype=np.uint8)
    for i, s in enumerate(seeds):
        f = np.load(cache_dir / f"frame_{s}.npz")
        llr[i] = f["llr"]
        truth[i] = f["truth_info"]
    return {"seeds": np.array(seeds), "llr": llr, "truth": truth}


def ie_at(decoder, data, k: int, idx: np.ndarray) -> np.ndarray:
    """info_errors at exactly iterate k for frames idx (fresh decode, bit-exact prefix)."""
    out = np.empty(idx.size, dtype=np.int64)
    for start in range(0, idx.size, CHUNK):
        sub = idx[start:start + CHUNK]
        res = decoder.decode(data["llr"][sub], num_iter=k,
                             alpha=ALPHA, offset=OFFSET, trajectory=False)
        out[start:start + CHUNK] = (res["info_bits"] != data["truth"][sub]).sum(axis=1)
    return out


def main() -> int:
    decoder = RescueDecoder(make_encoder())
    raw = json.load(open(OUT_DIR / "raw_traj_confirm.json"))
    frozen = json.load(open(OUT_DIR / "frozen_rule.json"))
    spec = frozen["selected_rule"]

    out = {"schema_version": "decode-budget-rule.iterates.v1",
           "contract_amend": "v1.1 (FER semantics clarification; rule untouched)",
           "batches": {}}
    t0 = time.perf_counter()
    for cond, cache in CONFIRM.items():
        b = raw["batches"][cond]
        data = load_batch(RESULTS_ROOT / "llr_cache" / cache)
        seeds = np.array(b["seeds"])
        assert np.array_equal(seeds, data["seeds"]), f"{cond}: seed order mismatch"
        sw = np.array(b["syndrome_weights"], dtype=np.int32)
        conv = np.array(b["converged_at"], dtype=np.int64)
        stop, outcome = simulate_rule(sw, conv, spec)
        cut = (outcome == CUT_CORRECT) | (outcome == CUT_WRONG)
        n = sw.shape[0]
        rec = {
            "ie_at_10": ie_at(decoder, data, 10, np.arange(n)).tolist(),
            "ie_at_15": ie_at(decoder, data, 15, np.arange(n)).tolist(),
            "cut_frame_index": np.flatnonzero(cut).tolist(),
            "cut_stop_iter": stop[cut].tolist(),
        }
        # cut-frame ie at their stop iterates (grouped by stop value)
        cut_idx = np.flatnonzero(cut)
        ie_stop = np.empty(cut_idx.size, dtype=np.int64)
        for v in np.unique(stop[cut]):
            sub = cut_idx[stop[cut] == v]
            ie_stop[stop[cut] == v] = ie_at(decoder, data, int(v), sub)
        rec["cut_ie_at_stop"] = ie_stop.tolist()
        out["batches"][cond] = rec
        print(f"[{cond}] ie@10 FER={(np.array(rec['ie_at_10']) > 0).mean():.4f} "
              f"ie@15 FER={(np.array(rec['ie_at_15']) > 0).mean():.4f} "
              f"cut_frames={cut_idx.size} "
              f"cut_ie>0={int((ie_stop > 0).sum())}", flush=True)
    path = OUT_DIR / "raw_iterates_confirm.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"written: {path} ({time.perf_counter() - t0:.0f}s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
