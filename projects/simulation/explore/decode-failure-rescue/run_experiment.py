"""Run decode-failure-rescue arms and correctness gates (contract.yaml).

Modes:
    --split smoke|dev|eval   run arms over the cached split
                             (smoke = identity/consistency point-check only)
    --gates                  run contract decoder.correctness_gates 1-3
                             (uses smoke 8 + dev 32 cached frames) and the
                             timing measurements / extrapolations

Arms (contract.yaml `arms`):
    B0        instrumented 20-iteration NOMS(0.75,0) baseline (trajectory on)
    R1_EXT    failed frames -> hot continuation +20 same config, syndrome-0
              early stop
    R2_ERASE  failed frames -> unsatisfied-check-connected transmitted
              positions, k smallest |channel LLR| erased (LLR->0), hot +20;
              k from --k-erase (dev selects; contract default 16)
    R3_CONF   failed frames -> hot +20 with config switched to (0.875,0.1)
    O1_ORACLE failed frames -> genie: positions where B0 hard decision
              differs from the true codeword are erased; hot +20

Information access (contract info_access_triple): R1/R2/R3 use only decoder
internal signals (syndrome, messages); truth enters only scoring (FER/BER)
and the O1 genie arm.  Acceptance = syndrome 0 of the stage-2 output;
rescued-to-correct vs rescued-to-wrong are reported separately.

All randomness: none in the decoder; bootstrap (summary only) is seeded
PCG64(20260920) with 10k resamples per the frozen metrics block.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from rescue_decoder import (
    B0_CONFIG,
    R3_CONFIG,
    RescueDecoder,
    classify_failure,
    make_encoder,
)

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"

DEFAULT_ARMS = ("B0", "R1_EXT", "R2_ERASE", "R3_CONF", "O1_ORACLE")


# ---------------------------------------------------------------------- #
# cache access
# ---------------------------------------------------------------------- #
def load_split(split: str, snr_override_tag: str | None = None, limit: int | None = None):
    tag = split if snr_override_tag is None else f"{split}_{snr_override_tag}"
    directory = RESULTS_ROOT / "llr_cache" / tag
    frames = []
    for path in sorted(directory.glob("frame_*.npz")):
        with np.load(path) as data:
            frames.append(
                {
                    "seed": int(data["seed"]),
                    "frame_index": int(data["frame_index"]),
                    "llr": data["llr"].astype(np.float32),
                    "truth_info": data["truth_info"].astype(np.uint8),
                    "truth_coded": data["truth_coded"].astype(np.uint8),
                    "llr_sha256": str(data["llr_sha256"]),
                }
            )
    frames.sort(key=lambda f: f["seed"])
    if limit is not None:
        frames = frames[:limit]
    if not frames:
        raise RuntimeError(f"no cached frames under {directory}")
    return frames, tag


# ---------------------------------------------------------------------- #
# arm execution
# ---------------------------------------------------------------------- #
def run_arms(
    decoder: RescueDecoder,
    frames: list[dict[str, Any]],
    arms: list[str],
    k_erase: list[int],
) -> tuple[dict[str, Any], dict[str, Any]]:
    raw_frames: list[dict[str, Any]] = []
    stats = {
        "frames": len(frames),
        "b0_failures": 0,
        "arm_totals": {},
        "class_counts": {},
    }

    for frame in frames:
        llr = frame["llr"][None, :]
        truth_info = frame["truth_info"]
        truth_coded = frame["truth_coded"]

        b0 = decoder.decode(llr, num_iter=20, alpha=0.75, offset=0.0,
                            trajectory=True, return_final_llr=False)
        b0_info = b0["info_bits"][0]
        b0_coded = b0["coded_hat"][0]
        b0_info_errors = int(np.count_nonzero(b0_info != truth_info))
        b0_coded_errors = int(np.count_nonzero(b0_coded != truth_coded))
        failed = bool(b0["final_syndrome"][0] != 0)
        classification = (
            classify_failure(b0["syndrome_weights"][0], b0_info_errors)
            if failed or b0_info_errors > 0
            else None
        )
        record = {
            "seed": frame["seed"],
            "frame_index": frame["frame_index"],
            "llr_sha256": frame["llr_sha256"],
            "B0": {
                "syndrome_weights": b0["syndrome_weights"][0],
                "final_syndrome": int(b0["final_syndrome"][0]),
                "converged_at": b0["converged_at"][0],
                "info_errors": b0_info_errors,
                "coded_errors": b0_coded_errors,
                "classification": classification,
            },
            "arms": {},
        }
        stats["class_counts"][classification or "clean"] = (
            stats["class_counts"].get(classification or "clean", 0) + 1
        )

        if failed:
            stats["b0_failures"] += 1
            state = b0["state"]
            base = {
                "k": None,
                "trigger": "syndrome!=0",
            }

            def stage2(result) -> dict[str, Any]:
                info = result["info_bits"][0]
                accepted = bool(result["final_syndrome"][0] == 0)
                return {
                    "iterations_run": int(result["iterations_run"]),
                    "syndrome_weights": result["syndrome_weights"][0],
                    "final_syndrome": int(result["final_syndrome"][0]),
                    "accepted": accepted,
                    "info_errors": int(np.count_nonzero(info != truth_info)),
                    "rescued_to_correct": bool(
                        accepted and np.array_equal(info, truth_info)
                    ),
                    "rescued_to_wrong": bool(
                        accepted and not np.array_equal(info, truth_info)
                    ),
                }

            if "R1_EXT" in arms:
                out = decoder.decode(
                    llr, num_iter=20, alpha=B0_CONFIG.alpha, offset=B0_CONFIG.offset,
                    state=state, early_stop=True,
                )
                record["arms"]["R1_EXT"] = {**base, "stage2": "continue_same_config",
                                           **stage2(out)}
            if "R2_ERASE" in arms:
                candidates = decoder.internal_positions_to_tx(
                    b0["unsat_check_variables"][0]
                )
                magnitudes = np.abs(frame["llr"])[candidates]
                order = np.argsort(magnitudes, kind="stable")
                for k in k_erase:
                    positions = candidates[order[:k]]
                    out = decoder.decode(
                        llr, num_iter=20, alpha=B0_CONFIG.alpha, offset=B0_CONFIG.offset,
                        reset_positions=positions, state=state, early_stop=True,
                    )
                    record["arms"][f"R2_ERASE_k{k}"] = {
                        **base, "k": int(k), "stage2": "targeted_erase_then_continue",
                        "k_ranking": "channel_llr_magnitude_asc",
                        "candidate_count": int(candidates.size),
                        **stage2(out),
                    }
            if "R3_CONF" in arms:
                out = decoder.decode(
                    llr, num_iter=20, alpha=R3_CONFIG.alpha, offset=R3_CONFIG.offset,
                    state=state, early_stop=True,
                )
                record["arms"]["R3_CONF"] = {
                    **base, "config": [R3_CONFIG.alpha, R3_CONFIG.offset],
                    "stage2": "continue_switched_config", **stage2(out),
                }
            if "O1_ORACLE" in arms:
                positions = np.flatnonzero(b0_coded != truth_coded)
                out = decoder.decode(
                    llr, num_iter=20, alpha=B0_CONFIG.alpha, offset=B0_CONFIG.offset,
                    reset_positions=positions, state=state, early_stop=True,
                )
                record["arms"]["O1_ORACLE"] = {
                    **base, "stage2": "truth_reset_then_continue",
                    "information_access": "genie_diagnostic_only",
                    "reset_count": int(positions.size), **stage2(out),
                }
        raw_frames.append(record)

    return raw_frames, stats


def summarize(raw_frames: list[dict[str, Any]], stats: dict[str, Any],
              split: str) -> dict[str, Any]:
    n = stats["frames"]
    failures = stats["b0_failures"]
    bit_total = n * 1024
    b0_info_errors = sum(f["B0"]["info_errors"] for f in raw_frames)
    summary: dict[str, Any] = {
        "schema_version": "dfr.summary.v1",
        "split": split,
        "frames": n,
        "B0": {
            "fer": failures / n if n else None,  # trigger rate (syndrome!=0)
            "fer_info": sum(1 for f in raw_frames if f["B0"]["info_errors"] > 0) / n,
            "ber": b0_info_errors / bit_total if n else None,
            "class_counts": stats["class_counts"],
        },
    }
    arm_names = sorted({name for f in raw_frames for name in f["arms"]})
    for arm in arm_names:
        records = [f["arms"][arm] for f in raw_frames if arm in f["arms"]]
        accepted = sum(1 for r in records if r["accepted"])
        correct = sum(1 for r in records if r["rescued_to_correct"])
        wrong = sum(1 for r in records if r["rescued_to_wrong"])
        iters = [r["iterations_run"] for r in records]
        summary[arm] = {
            "triggered": len(records),
            "accepted": accepted,
            "rescued_to_correct": correct,
            "rescued_to_wrong": wrong,
            "rescue_rate_on_trigger": (accepted / len(records)) if records else None,
            "mean_extra_iterations": float(np.mean(iters)) if iters else None,
            "p95_extra_iterations": (
                float(np.percentile(iters, 95)) if iters else None
            ),
            "is_oracle_headroom_only": arm.startswith("O1"),
        }
    stats["arm_totals"] = {arm: summary.get(arm, {}).get("triggered", 0)
                           for arm in arm_names}
    return summary


def bootstrap_paired_fer_diff(raw_frames, arm_a: str, arm_b: str, *,
                              resamples: int = 10_000, seed: int = 20260920):
    """Frame-level seed-cluster bootstrap of paired FER(A)-FER(B) (contract metrics.primary)."""
    frames = [f for f in raw_frames if arm_a in f["arms"] and arm_b in f["arms"]]
    if not frames:
        return None
    a = np.array([1 if f["arms"][arm_a]["info_errors"] > 0 else 0 for f in frames])
    b = np.array([1 if f["arms"][arm_b]["info_errors"] > 0 else 0 for f in frames])
    rng = np.random.default_rng(seed)
    n = len(frames)
    diffs = np.empty(resamples)
    for r in range(resamples):
        idx = rng.integers(0, n, size=n)
        diffs[r] = a[idx].mean() - b[idx].mean()
    point = float(a.mean() - b.mean())
    return {
        "arm_a": arm_a,
        "arm_b": arm_b,
        "n": n,
        "point_estimate": point,
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "resamples": resamples,
        "seed": seed,
    }


def run_split(split: str, snr_tag: str | None, arms: list[str], k_erase: list[int],
              limit: int | None) -> None:
    frames, tag = load_split(split, snr_tag, limit)
    encoder = make_encoder()
    decoder = RescueDecoder(encoder)
    t0 = time.perf_counter()
    raw_frames, stats = run_arms(decoder, frames, arms, k_erase)
    elapsed = time.perf_counter() - t0
    summary = summarize(raw_frames, stats, tag)
    summary["decode_wall_seconds"] = elapsed
    if split == "eval":
        for arm in ("R2_ERASE_k16", "R3_CONF"):
            ci = bootstrap_paired_fer_diff(raw_frames, arm, "R1_EXT")
            if ci:
                summary.setdefault("paired_bootstrap", {})[f"{arm}_vs_R1_EXT"] = ci
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    raw_path = RESULTS_ROOT / f"raw_{tag}.json"
    summary_path = RESULTS_ROOT / f"summary_{tag}.json"
    raw_path.write_text(
        json.dumps({"schema_version": "dfr.raw.v1", "frames": raw_frames}, indent=1),
        encoding="utf-8",
    )
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"raw -> {raw_path}")
    print(f"summary -> {summary_path}")


# ---------------------------------------------------------------------- #
# correctness gates (contract decoder.correctness_gates) + timing
# ---------------------------------------------------------------------- #
def run_gates() -> dict[str, Any]:
    import torch
    import sionna

    smoke, _ = load_split("smoke")
    dev, _ = load_split("dev", limit=32)
    if len(smoke) < 8:
        raise RuntimeError("smoke cache incomplete (need 8 frames)")
    if len(dev) < 32:
        raise RuntimeError(f"dev cache incomplete for gates (need 32, have {len(dev)})")

    encoder = make_encoder()
    decoder = RescueDecoder(encoder)
    gate_frames = smoke + dev

    # ---- Gate 1: B0 instrumented final decisions vs Sionna num_iter=20 ----
    mismatches_info = 0
    mismatches_coded = 0
    codewords = 0
    for chunk_start in range(0, len(gate_frames), 8):
        chunk = gate_frames[chunk_start : chunk_start + 8]
        llr = np.stack([f["llr"] for f in chunk])
        result = decoder.decode(llr, num_iter=20, trajectory=False)
        ref_info, ref_coded = decoder.sionna_reference(llr, num_iter=20)
        mismatches_info += int(np.count_nonzero(
            result["info_bits"] != ref_info))
        mismatches_coded += int(np.count_nonzero(
            result["coded_hat"] != ref_coded))
        codewords += llr.shape[0]
    gate1 = {
        "n_codewords": codewords,
        "info_bit_mismatches": mismatches_info,
        "coded_bit_mismatches": mismatches_coded,
        "pass": mismatches_info == 0 and mismatches_coded == 0,
    }

    # ---- Gate 2: hot 20+20 == fresh 40 ----
    hot_mismatch = 0
    fresh_mismatch = 0
    codewords2 = 0
    for chunk_start in range(0, len(dev), 8):
        chunk = dev[chunk_start : chunk_start + 8]
        llr = np.stack([f["llr"] for f in chunk])
        b0 = decoder.decode(llr, num_iter=20, trajectory=False)
        hot = decoder.decode(llr, num_iter=20, state=b0["state"], trajectory=False)
        fresh = decoder.decode(llr, num_iter=40, trajectory=False)
        ref_info, ref_coded = decoder.sionna_reference(llr, num_iter=40)
        hot_mismatch += int(np.count_nonzero(hot["info_bits"] != fresh["info_bits"]))
        hot_mismatch += int(np.count_nonzero(hot["coded_hat"] != fresh["coded_hat"]))
        fresh_mismatch += int(np.count_nonzero(fresh["info_bits"] != ref_info))
        fresh_mismatch += int(np.count_nonzero(fresh["coded_hat"] != ref_coded))
        codewords2 += llr.shape[0]
    gate2 = {
        "n_codewords": codewords2,
        "hot_vs_instrumented_fresh_mismatches": hot_mismatch,
        "instrumented_fresh_vs_sionna_fresh_mismatches": fresh_mismatch,
        "pass": hot_mismatch == 0 and fresh_mismatch == 0,
    }

    # ---- Gate 3: (0.875,0.1) fresh 40 instrumented vs Sionna cn_update construct ----
    gate3_mismatch = 0
    codewords3 = 0
    for chunk_start in range(0, 8, 8):
        chunk = dev[chunk_start : chunk_start + 8]
        llr = np.stack([f["llr"] for f in chunk])
        result = decoder.decode(
            llr, num_iter=40, alpha=R3_CONFIG.alpha, offset=R3_CONFIG.offset,
            trajectory=False,
        )
        ref_info, ref_coded = decoder.sionna_reference(
            llr, num_iter=40, config=R3_CONFIG
        )
        gate3_mismatch += int(np.count_nonzero(result["info_bits"] != ref_info))
        gate3_mismatch += int(np.count_nonzero(result["coded_hat"] != ref_coded))
        codewords3 += llr.shape[0]
    gate3 = {
        "n_codewords": codewords3,
        "bit_mismatches": gate3_mismatch,
        "pass": gate3_mismatch == 0,
    }

    # ---- Timing: single-codeword B0 40-iteration decode ----
    llr32 = np.stack([f["llr"] for f in dev])
    t0 = time.perf_counter()
    decoder.decode(llr32, num_iter=40, trajectory=False)
    t40 = time.perf_counter() - t0
    per_cw_40it = t40 / llr32.shape[0]
    t0 = time.perf_counter()
    decoder.decode(llr32, num_iter=20, trajectory=False)
    per_cw_20it = (time.perf_counter() - t0) / llr32.shape[0]

    gen_meta_path = RESULTS_ROOT / "generation_meta_smoke.json"
    gen_seconds = None
    gen_seconds_steady = None
    if gen_meta_path.exists():
        meta = json.loads(gen_meta_path.read_text(encoding="utf-8"))
        timings = meta.get("per_frame_seconds") or []
        gen_seconds = meta.get("mean_frame_seconds")
        if len(timings) > 1:
            gen_seconds_steady = float(np.mean(timings[1:]))  # excl. import warmup

    # extrapolation with the T077-anchored failure fraction (FER ~132/512);
    # steady-state generation + one-off process warmup (~5 s measured)
    fail_fraction = 132 / 512
    steady_gen = gen_seconds_steady if gen_seconds_steady is not None else 0.0
    warmup_seconds = 5.0

    def extrapolate(n_frames: float) -> dict[str, Any]:
        stage2_seconds = per_cw_20it * 4.3  # R1 + 3x R2-k + R3 + O1 mix, worst ~5 arms
        per_frame = steady_gen + per_cw_20it + fail_fraction * stage2_seconds
        return {
            "frames": n_frames,
            "total_seconds_estimate": n_frames * per_frame + warmup_seconds,
            "total_minutes_estimate": (n_frames * per_frame + warmup_seconds) / 60.0,
        }

    report = {
        "schema_version": "dfr.correctness-gates.v1",
        "versions": {
            "python": __import__("sys").version.split()[0],
            "sionna": sionna.__version__,
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
        "gate1_b0_vs_sionna20": gate1,
        "gate2_hot_20_20_vs_fresh40": gate2,
        "gate3_r3config_vs_sionna_construct": gate3,
        "timing": {
            "mean_frame_generation_seconds_smoke_warmup_inclusive": gen_seconds,
            "steady_state_frame_generation_seconds": gen_seconds_steady,
            "per_codeword_b0_20it_seconds": per_cw_20it,
            "per_codeword_b0_40it_seconds": per_cw_40it,
            "extrapolation": {
                "dev64": extrapolate(64),
                "eval512": extrapolate(512),
            },
        },
    }
    out_path = RESULTS_ROOT / "correctness_gates.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"gates -> {out_path}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("smoke", "dev", "eval"))
    parser.add_argument("--snr-db-override", type=float, default=None,
                        help="use the _snrX override cache (contract diag17)")
    parser.add_argument("--arms", default=",".join(DEFAULT_ARMS))
    parser.add_argument("--k-erase", default="8,16,32",
                        help="candidate k values for R2 (dev selects one)")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--gates", action="store_true")
    args = parser.parse_args()

    if args.gates:
        run_gates()
        return 0
    if not args.split:
        parser.error("either --split or --gates is required")
    snr_tag = None if args.snr_db_override is None else f"snr{args.snr_db_override:g}"
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    k_erase = sorted({int(k) for k in args.k_erase.split(",")})
    run_split(args.split, snr_tag, arms, k_erase, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
