"""decode-capability-audit: PROMPT-026 任务二（译码块两个未测轴的缓存上诊断）。

Diagnostic A (capability): SPA(boxplus-phi) x {20,50,200} vs NOMS(0.75,0) x 20
    (+ NOMS x {50,200} iteration controls) on the three frozen confirm LLR
    caches (M15/W12/S16, 2048 frames each).
Diagnostic B (grid): NOMS (alpha, beta) 4x4 grid, 20 iters fresh, same caches.

Zero modification of decode-failure-rescue/ originals: this module only
*imports* rescue_decoder (read-only reuse) and reads the llr_cache npz files.
Truth (truth_info/truth_coded) is used exclusively for scoring (info_errors,
e0 stratification) after decoding -- never inside any decode arm.

LLR sign convention (rescue_decoder.final_llr_tx): positive = bit 1.

Usage:
    python run_audit.py --diagnostic capability
    python run_audit.py --diagnostic grid
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sionna.phy.fec.ldpc import LDPC5GDecoder
from sionna.phy.fec.ldpc.decoding import LDPCBPDecoder, cn_update_phi

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
RESCUE_DIR = SIM_ROOT / "explore" / "decode-failure-rescue"
RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"
OUT_DIR = SIM_ROOT / "results" / "decode-capability-audit"

if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))
if str(RESCUE_DIR) not in sys.path:
    sys.path.insert(0, str(RESCUE_DIR))

from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402

CONDITIONS = {
    "M15": RESULTS_ROOT / "llr_cache" / "confirm2048",
    "W12": RESULTS_ROOT / "llr_cache" / "confirm_W12_snr12_turb11.6x10.1",
    "S16": RESULTS_ROOT / "llr_cache" / "confirm_S16_snr16_turb4.2x1.4",
}
RAW_ANCHOR = {
    "M15": RESULTS_ROOT / "raw_confirm2048.json",
    "W12": RESULTS_ROOT / "raw_confirm_W12.json",
    "S16": RESULTS_ROOT / "raw_confirm_S16.json",
}

CAPABILITY_ARMS = {
    "B0": dict(cn="nomos", alpha=0.75, beta=0.0, iters=20),
    "SPA20": dict(cn="spa", iters=20),
    "SPA50": dict(cn="spa", iters=50),
    "SPA200": dict(cn="spa", iters=200),
    "NOMS50": dict(cn="nomos", alpha=0.75, beta=0.0, iters=50),
    "NOMS200": dict(cn="nomos", alpha=0.75, beta=0.0, iters=200),
}
GRID_ALPHA = [0.75, 0.8125, 0.875, 0.9375]
GRID_BETA = [0.0, 0.05, 0.1, 0.15]
GRID_ITERS = 20
BATCH = 256


def make_spa_engine(decoder: RescueDecoder) -> LDPC5GDecoder:
    """Same plumbing as rescue_decoder._engine, only the CN update swapped."""
    return LDPC5GDecoder(
        decoder.encoder,
        num_iter=1,
        cn_update=cn_update_phi,
        hard_out=True,
        return_infobits=True,
        llr_max=decoder.llr_max,
        return_state=True,
        device=decoder.device,
    )


def spa_stepped(
    decoder: RescueDecoder,
    spa_engine: LDPC5GDecoder,
    llr: np.ndarray,
    iters: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Stepped SPA decode -> (info_bits, syndrome_first_zero_iter or -1, final_syndrome)."""
    n = llr.shape[0]
    conv = np.full(n, -1, dtype=np.int64)
    llr_5g = decoder.to_internal(llr)
    state = None
    x_int = None
    for it in range(1, iters + 1):
        with torch.no_grad():
            x_int, state = LDPCBPDecoder.call(
                spa_engine, llr_5g, num_iter=1, msg_v2c=state
            )
        s = decoder.syndrome(x_int)
        fresh = (conv < 0) & (s == 0)
        conv[fresh] = it
    info, _ = decoder._hard_views(x_int)
    return info, conv, decoder.syndrome(x_int)


def run_arm(
    decoder: RescueDecoder,
    spa_engine: LDPC5GDecoder,
    llr: np.ndarray,
    truth_info: np.ndarray,
    *,
    cn: str,
    iters: int,
    alpha: float = 1.0,
    beta: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Fresh decode of [N,1536] LLR -> (info_errors[N], converged_at[N], -1=never)."""
    n = llr.shape[0]
    info_errors = np.empty(n, dtype=np.int64)
    conv_out = np.empty(n, dtype=np.int64)
    for start in range(0, n, BATCH):
        chunk = llr[start : start + BATCH]
        truth_chunk = truth_info[start : start + BATCH]
        if cn == "nomos":
            res = decoder.decode(
                chunk, num_iter=iters, alpha=alpha, offset=beta, trajectory=True
            )
            info = res["info_bits"]
            conv = np.array(
                [c if c is not None else -1 for c in res["converged_at"]],
                dtype=np.int64,
            )
        elif cn == "spa":
            info, conv, _ = spa_stepped(decoder, spa_engine, chunk, iters)
        else:
            raise ValueError(cn)
        info_errors[start : start + BATCH] = (info != truth_chunk).sum(axis=1)
        conv_out[start : start + BATCH] = conv
    return info_errors, conv_out


def load_condition(cond: str) -> dict[str, np.ndarray]:
    d = CONDITIONS[cond]
    seeds = sorted(int(p.stem.split("_")[1]) for p in d.glob("frame_*.npz"))
    llr = np.empty((len(seeds), 1536), dtype=np.float32)
    truth_info = np.empty((len(seeds), 1024), dtype=np.uint8)
    truth_coded = np.empty((len(seeds), 1536), dtype=np.uint8)
    for i, seed in enumerate(seeds):
        f = np.load(d / f"frame_{seed}.npz")
        llr[i] = f["llr"]
        truth_info[i] = f["truth_info"]
        truth_coded[i] = f["truth_coded"]
    if llr.shape[0] != 2048:
        raise RuntimeError(f"{cond}: expected 2048 frames, got {llr.shape[0]}")
    return {"seeds": np.array(seeds), "llr": llr, "truth_info": truth_info,
            "truth_coded": truth_coded}


def e0_per_frame(llr: np.ndarray, truth_coded: np.ndarray) -> np.ndarray:
    """Pre-decode hard-decision error count per frame (LLR>0 -> bit 1)."""
    hard = (llr > 0).astype(np.int64)
    return (hard != truth_coded.astype(np.int64)).sum(axis=1)


def anchor_gate(decoder, data) -> tuple[dict, list[int]]:
    raw = json.load(open(RAW_ANCHOR_COND))
    raw_map = {fr["seed"]: fr["B0"]["info_errors"] for fr in raw["frames"]}
    ie, conv = run_arm(
        decoder, None, data["llr"], data["truth_info"],
        cn="nomos", iters=20, alpha=0.75, beta=0.0,
    )
    mism = [int(s) for s, e in zip(data["seeds"], ie) if e != raw_map[int(s)]]
    return {"info_errors": ie, "converged_at": conv}, mism


RAW_ANCHOR_COND: str = ""  # set per condition in main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diagnostic", required=True, choices=["capability", "grid"])
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    decoder = RescueDecoder(make_encoder())
    spa_engine = make_spa_engine(decoder)

    global RAW_ANCHOR_COND

    # ---- gates (before any result is read) -------------------------------
    probe = load_condition("M15")
    # gate 1: B0 reproduces raw anchor on first 256 frames of M15
    # (full-batch anchor gate runs inside the capability loop below)
    RAW_ANCHOR_COND = str(RAW_ANCHOR["M15"])
    _, mism = anchor_gate(decoder, {**probe, "llr": probe["llr"][:256],
                                    "truth_info": probe["truth_info"][:256],
                                    "seeds": probe["seeds"][:256]})
    if mism:
        raise SystemExit(f"IMPLEMENTATION GATE FAIL (M15 first 256): {mism[:5]}")
    # gate 2: SPA stepped == SPA single-shot fresh call (flooding statelessness)
    single = LDPC5GDecoder(
        decoder.encoder, num_iter=20, cn_update=cn_update_phi, hard_out=True,
        return_infobits=True, llr_max=decoder.llr_max, return_state=False,
        device="cpu",
    )
    # single-shot reference consumes the transmitted-order LLR (its own 5G
    # wrapper rebuilds the internal vector); stepped path consumes the same
    # frames through to_internal + state chaining.
    ref_llr = torch.as_tensor(
        np.clip(probe["llr"][:16], -decoder.backend_input_clip,
                decoder.backend_input_clip),
        dtype=torch.float32,
    )
    with torch.no_grad():
        ref = single(ref_llr).detach().cpu().numpy()
    stepped, _, _ = spa_stepped(decoder, spa_engine, probe["llr"][:16], 20)
    if not np.array_equal(ref.astype(np.uint8), stepped.astype(np.uint8)):
        raise SystemExit("SPA GATE FAIL: stepped != single-shot fresh call")
    # gate 3 (contract spa_sanity_gate): SPA200 zero errors on 4 B0-clean frames
    raw = json.load(open(RAW_ANCHOR["M15"]))
    clean_seeds = [fr["seed"] for fr in raw["frames"]
                   if fr["B0"]["info_errors"] == 0][:4]
    idx = [int(np.flatnonzero(probe["seeds"] == s)[0]) for s in clean_seeds]
    ie200, _ = run_arm(decoder, spa_engine, probe["llr"][idx],
                       probe["truth_info"][idx], cn="spa", iters=200)
    if int(ie200.sum()) != 0:
        raise SystemExit(f"SPA SANITY GATE FAIL: info_errors={ie200.tolist()}")
    print("gates passed (B0 anchor 256, SPA stepped==fresh, SPA200 sanity 4 frames)",
          flush=True)
    del probe

    all_out: dict[str, dict] = {}
    strat_out: dict[str, dict] = {}
    gate_report: dict[str, dict] = {}

    t_start = time.perf_counter()
    for cond in CONDITIONS:
        data = load_condition(cond)
        e0 = e0_per_frame(data["llr"], data["truth_coded"])
        qs = np.quantile(e0, [0.25, 0.5, 0.75])
        band = np.digitize(e0, qs)  # 0=Q1 best ... 3=Q4 worst(deep fade)
        strat_out[cond] = {
            "e0_quartile_edges": qs.tolist(),
            "band_counts": np.bincount(band, minlength=4).tolist(),
            "e0_mean": float(e0.mean()),
            "e0_q90": float(np.quantile(e0, 0.9)),
        }

        if args.diagnostic == "capability":
            RAW_ANCHOR_COND = str(RAW_ANCHOR[cond])
            gate, mism = anchor_gate(decoder, data)
            gate_report[cond] = {"gate_pass": not mism,
                                 "n_mismatch": len(mism)}
            if mism:
                raise SystemExit(
                    f"IMPLEMENTATION GATE FAIL [{cond}]: {len(mism)} mismatches, "
                    f"e.g. {mism[:5]}"
                )
            arms_out = {"B0": {"info_errors": gate["info_errors"].tolist(),
                               "converged_at": gate["converged_at"].tolist()}}
            for name, spec in CAPABILITY_ARMS.items():
                if name == "B0":
                    continue
                t0 = time.perf_counter()
                ie, conv = run_arm(
                    decoder, spa_engine, data["llr"], data["truth_info"],
                    cn=spec["cn"], iters=spec["iters"],
                    alpha=spec.get("alpha", 1.0), beta=spec.get("beta", 0.0),
                )
                arms_out[name] = {"info_errors": ie.tolist(),
                                  "converged_at": conv.tolist()}
                print(f"[{cond}] {name}: FER={(ie > 0).mean():.4f} "
                      f"conv_med={np.median(conv[conv > 0]) if (conv > 0).any() else None} "
                      f"({time.perf_counter() - t0:.1f}s)", flush=True)
            all_out[cond] = {"seeds": data["seeds"].tolist(),
                             "bands": band.tolist(), "arms": arms_out}
        else:  # grid
            grid_out: dict[str, dict] = {}
            for alpha in GRID_ALPHA:
                for beta in GRID_BETA:
                    key = f"a{alpha:g}_b{beta:g}"
                    t0 = time.perf_counter()
                    ie, _ = run_arm(
                        decoder, spa_engine, data["llr"], data["truth_info"],
                        cn="nomos", iters=GRID_ITERS, alpha=alpha, beta=beta,
                    )
                    grid_out[key] = {"info_errors": ie.tolist()}
                    print(f"[{cond}] {key}: FER={(ie > 0).mean():.4f} "
                          f"({time.perf_counter() - t0:.1f}s)", flush=True)
            all_out[cond] = {"seeds": data["seeds"].tolist(),
                             "bands": band.tolist(), "grid": grid_out}

    raw_path = OUT_DIR / (
        "raw_capability.json" if args.diagnostic == "capability" else "raw_grid.json"
    )
    payload = {"schema_version": f"decode-capability-audit.{args.diagnostic}.v1",
               "contract": "explore/decode-capability-audit/contract.yaml (v1, frozen)",
               "conditions": all_out, "stratification": strat_out}
    if gate_report:
        payload["anchor_gates"] = gate_report
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    print(f"raw written: {raw_path} ({time.perf_counter() - t_start:.0f}s total)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
