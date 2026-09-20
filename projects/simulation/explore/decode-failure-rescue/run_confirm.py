"""Confirmation round for decode-failure-rescue (confirm_contract.yaml).

Fixes carried into this round (R030 audit):
  * R2 index mapping fixed in rescue_decoder.internal_positions_to_tx
    (raw -> channel order via out_int_inv); verified by ``--verify-mapping``.
    R2 itself is NOT a scientific arm this round.
  * Unified final-output rule: a two-stage arm adopts the stage-2 output iff
    the stage-2 output passes the parity check (syndrome==0, incl. the early-
    stop iterate); otherwise it keeps the stage-1 output and its failure flag.
    All headline metrics are computed on the FINAL output.  Truth is used for
    scoring only.

Arms on the fresh confirm2048 split (seeds 30000..32047, 15 dB frozen cell):
  B0  NOMS(0.75,0) 20 it
  R1  stage1=B0; on B0 syndrome!=0 hot-continue same config +20 it early stop
  R3  stage1=B0; on B0 syndrome!=0 hot-continue switched (0.875,0.1) +20 it
  F   stage1=fresh (0.875,0.1) 20 it on every frame (stage-1 results kept);
      on its own syndrome!=0 hot-continue same config +20 it early stop

Subcommands (mutually exclusive):
  --verify-mapping   unit checks for the R2 fix (no frame decoding)
  --anchor           rebuild eval seed 4000 in memory, compare llr sha256
                     against the cached frame (no writes to old caches)
  --regress-dev      rerun the OLD arm set on cached dev 64 via
                     run_experiment.run_arms and require B0/R1/R3/O1 records
                     to match raw_dev.json bit-exactly (decode logic
                     unchanged); R2 differences are counted, not interpreted
  --generate         generate the confirm2048 frame cache (reuses
                     generate_llrs.main with an added split entry)
  --run              run B0/R1/R3/F on confirm2048 -> raw + summary

Determinism: decoder has no RNG; bootstrap seeded PCG64(20260921), 10k
resamples.  Old artifacts are never written by this file.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from rescue_decoder import (  # noqa: E402
    B0_CONFIG,
    R3_CONFIG,
    RescueDecoder,
    classify_failure,
    make_encoder,
)

CONFIRM_TAG = "confirm2048"
CONFIRM_SEEDS = {"start": 30000, "stop_inclusive": 32047, "count": 2048}
BOOTSTRAP_SEED = 20260921
BOOTSTRAP_RESAMPLES = 10_000
CHECKPOINT = RESULTS_ROOT / "raw_confirm2048.checkpoint.jsonl"


# ---------------------------------------------------------------------- #
# small helpers
# ---------------------------------------------------------------------- #
def _arm_frame_fields(decoder: RescueDecoder, llr: np.ndarray, *, alpha: float,
                      offset: float) -> dict[str, Any]:
    """One 20-iteration stage-1 decode with trajectory (fresh start)."""
    out = decoder.decode(
        llr, num_iter=20, alpha=alpha, offset=offset,
        trajectory=True, return_final_llr=False,
    )
    info = out["info_bits"][0]
    coded = out["coded_hat"][0]
    # truth NOT consulted here; info/coded errors filled by the caller.
    return {
        "syndrome_weights": out["syndrome_weights"][0],
        "final_syndrome": int(out["final_syndrome"][0]),
        "converged_at": out["converged_at"][0],
        "_info_bits": info,
        "_coded_hat": coded,
        "_state": out["state"],
    }


def _stage2_fields(result: dict[str, Any], truth_info: np.ndarray) -> dict[str, Any]:
    info = result["info_bits"][0]
    return {
        "iterations_run": int(result["iterations_run"]),
        "syndrome_weights": result["syndrome_weights"][0],
        "final_syndrome": int(result["final_syndrome"][0]),
        "accepted": bool(result["final_syndrome"][0] == 0),
        "stage2_info_errors": int(np.count_nonzero(info != truth_info)),
    }


# ---------------------------------------------------------------------- #
# --verify-mapping
# ---------------------------------------------------------------------- #
def verify_mapping(decoder: RescueDecoder) -> None:
    out_int = decoder._out_int
    out_int_inv = decoder._out_int_inv
    n = out_int.size
    assert n == 1536, out_int.size
    # inverse permutations of each other
    assert np.array_equal(out_int_inv[out_int], np.arange(n))
    assert np.array_equal(out_int[out_int_inv], np.arange(n))
    # closed form from the R030 reviewer (Sionna BG2 z=104 interleaver)
    t = np.arange(n)
    closed = (t % 4) * 384 + t // 4
    assert np.array_equal(out_int, closed), "out_int closed form mismatch"
    # R030 worked example: internal VN 209 -> raw 1 -> channel 4 (not 1)
    assert decoder._internal_to_tx[209] == 1
    mapped = decoder.internal_positions_to_tx(np.array([209]))
    assert mapped.tolist() == [4], mapped.tolist()
    assert decoder._out_int[1] == 384 and decoder._out_int_inv[384] == 1

    # end-to-end: zeroing channel position t must land on the right internal VN
    rng = np.random.default_rng(7)
    llr = rng.normal(size=(1, 1536)).astype(np.float32)
    for t_probe in (0, 1, 4, 383, 384, 1000, 1535):
        # channel t carries raw out_int[t]; raw q sits at internal tx_to_internal[q]
        v = int(decoder._tx_to_internal[out_int[t_probe]])
        tx_positions = decoder.internal_positions_to_tx(np.array([v]))
        assert tx_positions.tolist() == [t_probe], (t_probe, tx_positions)
        modified = llr.copy()
        modified[0, t_probe] = 0.0
        internal = decoder.to_internal(modified).numpy()[0]
        reference = decoder.to_internal(llr).numpy()[0]
        diff = np.flatnonzero(internal != reference)
        assert diff.tolist() == [v], (t_probe, v, diff.tolist())

    print("verify-mapping: PASS (permutation inverse, closed form, VN209->tx4, "
          "8 end-to-end zero probes)")


# ---------------------------------------------------------------------- #
# --anchor (generation determinism on THIS interpreter)
# ---------------------------------------------------------------------- #
def anchor() -> None:
    import generate_llrs as gl

    sc = gl._load_single_cell()
    codec = sc._correctness().TargetApskCodec()
    seed = 4000
    cached = RESULTS_ROOT / "llr_cache" / "eval" / f"frame_{seed}.npz"
    with np.load(cached) as data:
        cached_sha = str(data["llr_sha256"])
    frame = gl.build_frame(sc, codec, seed=seed, snr_db_override=None)
    assert frame["llr_sha256"] == cached_sha, (
        f"anchor mismatch: fresh {frame['llr_sha256']} vs cached {cached_sha}")
    print(f"anchor: PASS (eval seed {seed} llr_sha256 reproduced bit-exactly)")


# ---------------------------------------------------------------------- #
# --regress-dev
# ---------------------------------------------------------------------- #
def regress_dev() -> None:
    import run_experiment as rx

    frames, _ = rx.load_split("dev")
    old = json.loads((RESULTS_ROOT / "raw_dev.json").read_text(encoding="utf-8"))
    old_by_seed = {f["seed"]: f for f in old["frames"]}
    assert len(frames) == 64 and set(old_by_seed) == {f["seed"] for f in frames}

    encoder = make_encoder()
    decoder = RescueDecoder(encoder)
    raw_frames, _ = rx.run_arms(
        decoder, frames, ["B0", "R1_EXT", "R2_ERASE", "R3_CONF", "O1_ORACLE"], [16]
    )

    report = {
        "schema_version": "dfr.confirm.regress-dev.v1",
        "frames": len(raw_frames),
        "b0_mismatch_frames": 0,
        "arm_mismatch": {},
        "r2_k16_changed_frames": 0,
        "r2_k16_changed_detail": [],
        "pass": True,
    }
    b0_keys = ("syndrome_weights", "final_syndrome", "converged_at",
               "info_errors", "coded_errors", "classification")
    s2_keys = ("iterations_run", "final_syndrome", "accepted", "info_errors",
               "rescued_to_correct", "rescued_to_wrong")
    for rec in raw_frames:
        old_rec = old_by_seed[rec["seed"]]
        for key in b0_keys:
            if rec["B0"][key] != old_rec["B0"][key]:
                report["b0_mismatch_frames"] += 1
                report["pass"] = False
                break
        for arm in ("R1_EXT", "R3_CONF", "O1_ORACLE"):
            mism = report["arm_mismatch"].setdefault(arm, 0)
            new_s2 = rec["arms"].get(arm)
            old_s2 = old_rec["arms"].get(arm)
            if (new_s2 is None) != (old_s2 is None):
                report["arm_mismatch"][arm] = mism + 1
                report["pass"] = False
                continue
            if new_s2 is None:
                continue
            if any(new_s2[k] != old_s2[k] for k in s2_keys):
                report["arm_mismatch"][arm] = mism + 1
                report["pass"] = False
        new_r2 = rec["arms"].get("R2_ERASE_k16")
        old_r2 = old_rec["arms"].get("R2_ERASE_k16")
        if (new_r2 is None) != (old_r2 is None) or (
            new_r2 is not None
            and any(new_r2[k] != old_r2[k] for k in s2_keys)
        ):
            report["r2_k16_changed_frames"] += 1
            report["r2_k16_changed_detail"].append({
                "seed": rec["seed"],
                "old": {k: old_r2[k] for k in s2_keys} if old_r2 else None,
                "new": {k: new_r2[k] for k in s2_keys} if new_r2 else None,
            })

    out = RESULTS_ROOT / "confirm_regress_dev.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items()
                      if k != "r2_k16_changed_detail"}, indent=2))
    print(f"regress-dev -> {out}")
    if not report["pass"]:
        raise SystemExit("REGRESSION FAILED: B0/R1/R3/O1 must be bit-identical")


# ---------------------------------------------------------------------- #
# --generate
# ---------------------------------------------------------------------- #
def generate() -> None:
    import generate_llrs as gl

    gl.SPLITS[CONFIRM_TAG] = dict(CONFIRM_SEEDS)
    sys.argv = ["generate_llrs.py", "--split", CONFIRM_TAG]
    gl.main()


# ---------------------------------------------------------------------- #
# --run (confirm arms with the unified output rule)
# ---------------------------------------------------------------------- #
def load_confirm_frames() -> list[dict[str, Any]]:
    directory = RESULTS_ROOT / "llr_cache" / CONFIRM_TAG
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
    expected = CONFIRM_SEEDS["count"]
    if len(frames) != expected:
        raise RuntimeError(f"confirm cache incomplete: {len(frames)}/{expected}")
    return frames


def run_one_frame(decoder: RescueDecoder, frame: dict[str, Any]) -> dict[str, Any]:
    llr = frame["llr"][None, :]
    truth_info = frame["truth_info"]
    truth_coded = frame["truth_coded"]

    b0f = _arm_frame_fields(decoder, llr, alpha=B0_CONFIG.alpha,
                            offset=B0_CONFIG.offset)
    f1f = _arm_frame_fields(decoder, llr, alpha=R3_CONFIG.alpha,
                            offset=R3_CONFIG.offset)

    def stage1_block(fields: dict[str, Any]) -> dict[str, Any]:
        info_errors = int(np.count_nonzero(fields["_info_bits"] != truth_info))
        coded_errors = int(np.count_nonzero(fields["_coded_hat"] != truth_coded))
        classification = (
            classify_failure(fields["syndrome_weights"], info_errors)
            if fields["final_syndrome"] != 0 or info_errors > 0 else None
        )
        return {
            "syndrome_weights": fields["syndrome_weights"],
            "final_syndrome": fields["final_syndrome"],
            "converged_at": fields["converged_at"],
            "info_errors": info_errors,
            "coded_errors": coded_errors,
            "classification": classification,
        }

    record: dict[str, Any] = {
        "seed": frame["seed"],
        "frame_index": frame["frame_index"],
        "llr_sha256": frame["llr_sha256"],
        "B0": stage1_block(b0f),
        "F1": stage1_block(f1f),   # F stage-1 only result (fresh 0.875/0.1 x20)
        "arms": {},
    }

    def two_stage(name: str, fields: dict[str, Any], block: dict[str, Any], *,
                  alpha: float, offset: float) -> None:
        arm: dict[str, Any] = {"trigger": bool(fields["final_syndrome"] != 0)}
        if arm["trigger"]:
            out = decoder.decode(
                llr, num_iter=20, alpha=alpha, offset=offset,
                state=fields["_state"], early_stop=True,
                trajectory=True, return_final_llr=False,
            )
            s2 = _stage2_fields(out, truth_info)
            arm["stage2"] = s2
            if s2["accepted"]:
                arm["final"] = {
                    "info_errors": s2["stage2_info_errors"],
                    "final_syndrome": 0,
                    "source": "stage2",
                }
            else:
                arm["final"] = {
                    "info_errors": block["info_errors"],
                    "final_syndrome": block["final_syndrome"],
                    "source": "stage1_fallback",
                }
        else:
            arm["stage2"] = None
            arm["final"] = {
                "info_errors": block["info_errors"],
                "final_syndrome": block["final_syndrome"],
                "source": "stage1_not_triggered",
            }
        record["arms"][name] = arm

    b0_block = record["B0"]
    f1_block = record["F1"]
    two_stage("R1", b0f, b0_block, alpha=B0_CONFIG.alpha, offset=B0_CONFIG.offset)
    two_stage("R3", b0f, b0_block, alpha=R3_CONFIG.alpha, offset=R3_CONFIG.offset)
    two_stage("F", f1f, f1_block, alpha=R3_CONFIG.alpha, offset=R3_CONFIG.offset)
    return record


def run_confirm() -> None:
    frames = load_confirm_frames()
    encoder = make_encoder()
    decoder = RescueDecoder(encoder)

    done_seeds: set[int] = set()
    if CHECKPOINT.exists():
        for line in CHECKPOINT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done_seeds.add(json.loads(line)["seed"])
    todo = [f for f in frames if f["seed"] not in done_seeds]
    print(f"confirm run: {len(frames)} frames, {len(done_seeds)} checkpointed, "
          f"{len(todo)} to go", flush=True)

    t0 = time.perf_counter()
    with CHECKPOINT.open("a", encoding="utf-8") as cp:
        for i, frame in enumerate(todo):
            record = run_one_frame(decoder, frame)
            cp.write(json.dumps(record) + "\n")
            cp.flush()
            if (i + 1) % 256 == 0:
                print(f"  {i + 1}/{len(todo)} frames "
                      f"({time.perf_counter() - t0:.1f}s)", flush=True)

    records = [
        json.loads(line) for line in
        CHECKPOINT.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    records.sort(key=lambda r: r["seed"])
    raw = {
        "schema_version": "dfr.confirm.raw.v1",
        "rules": {
            "output": "stage2 accepted (syndrome==0, early-stop iterate) -> "
                      "stage2 output; else stage1 output with failure flag",
            "trigger": "per-arm own stage-1 syndrome!=0 (R1/R3 stage1 = B0)",
            "truth_access": "scoring only",
        },
        "frames": records,
    }
    raw_path = RESULTS_ROOT / f"raw_{CONFIRM_TAG}.json"
    raw_path.write_text(json.dumps(raw, indent=1), encoding="utf-8")

    summary = summarize_confirm(records)
    summary["decode_wall_seconds"] = time.perf_counter() - t0
    summary_path = RESULTS_ROOT / f"summary_{CONFIRM_TAG}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"raw -> {raw_path}\nsummary -> {summary_path}")


# ---------------------------------------------------------------------- #
# statistics on final outputs
# ---------------------------------------------------------------------- #
def exact_binomial_two_sided(wins: int, losses: int) -> tuple[float, float]:
    """Two-sided and one-sided exact p for discordant paired events."""
    d = wins + losses
    if d == 0:
        return 1.0, 1.0
    lo = min(wins, losses)
    tail = sum(math.comb(d, i) for i in range(0, lo + 1)) / 2 ** d
    return min(1.0, 2 * tail), tail


def bootstrap_paired(records: list[dict[str, Any]], arm_a: str, arm_b: str,
                     *, resamples: int = BOOTSTRAP_RESAMPLES,
                     seed: int = BOOTSTRAP_SEED) -> dict[str, Any]:
    a = np.array([1 if r["arms"][arm_a]["final"]["info_errors"] > 0 else 0
                  for r in records])
    b = np.array([1 if r["arms"][arm_b]["final"]["info_errors"] > 0 else 0
                  for r in records])
    n = len(records)
    rng = np.random.default_rng(seed)
    diffs = np.empty(resamples)
    for k in range(resamples):
        idx = rng.integers(0, n, size=n)
        diffs[k] = a[idx].mean() - b[idx].mean()
    wins = int(np.sum((a == 0) & (b == 1)))
    losses = int(np.sum((a == 1) & (b == 0)))
    p2, p1 = exact_binomial_two_sided(wins, losses)
    return {
        "arm_a": arm_a, "arm_b": arm_b, "n": n,
        "point_estimate": float(a.mean() - b.mean()),
        "ci95": [float(np.percentile(diffs, 2.5)),
                 float(np.percentile(diffs, 97.5))],
        "wins_a": wins, "losses_a": losses,
        "discordant": wins + losses,
        "exact_two_sided_p": p2,
        "exact_one_sided_p": p1,
        "resamples": resamples, "seed": seed,
    }


def summarize_confirm(records: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(records)
    bit_total = n * 1024
    summary: dict[str, Any] = {
        "schema_version": "dfr.confirm.summary.v1",
        "split": CONFIRM_TAG,
        "frames": n,
        "metric_note": "all metrics on FINAL outputs (unified rule); "
                       "check_fail = final syndrome!=0; accepted_but_wrong = "
                       "final syndrome==0 yet info bits wrong",
        "stage1": {},
        "arms": {},
        "paired": {},
    }

    # stage-1-only views (B0 vs F1): config-alone effect at 20 iterations
    for name in ("B0", "F1"):
        errs = [r[name]["info_errors"] for r in records]
        summary["stage1"][name] = {
            "info_error_frames": sum(1 for e in errs if e > 0),
            "bit_errors": sum(errs),
            "fer": sum(1 for e in errs if e > 0) / n,
            "ber": sum(errs) / bit_total,
            "syndrome_fail_frames": sum(1 for r in records
                                        if r[name]["final_syndrome"] != 0),
        }

    for arm in ("B0", "R1", "R3", "F"):
        if arm == "B0":
            finals = [{"info_errors": r["B0"]["info_errors"],
                       "final_syndrome": r["B0"]["final_syndrome"]}
                      for r in records]
            iters = [20] * n
            triggered = [r["B0"]["final_syndrome"] != 0 for r in records]
        else:
            finals = [r["arms"][arm]["final"] for r in records]
            iters = [20 + (r["arms"][arm]["stage2"]["iterations_run"]
                           if r["arms"][arm]["stage2"] else 0)
                     for r in records]
            triggered = [r["arms"][arm]["trigger"] for r in records]
        err_frames = sum(1 for f in finals if f["info_errors"] > 0)
        bits = sum(f["info_errors"] for f in finals)
        check_fail = sum(1 for f in finals if f["final_syndrome"] != 0)
        accepted_wrong = sum(1 for f in finals
                             if f["final_syndrome"] == 0 and f["info_errors"] > 0)
        summary["arms"][arm] = {
            "info_error_frames": err_frames,
            "fer": err_frames / n,
            "bit_errors": bits,
            "ber": bits / bit_total,
            "check_fail_frames": check_fail,
            "check_fail_rate": check_fail / n,
            "accepted_but_wrong_frames": accepted_wrong,
            "triggered_frames": sum(triggered),
            "mean_total_iterations": float(np.mean(iters)),
            "p95_total_iterations": float(np.percentile(iters, 95)),
            "mean_stage2_iterations_on_triggered": float(np.mean(
                [r["arms"][arm]["stage2"]["iterations_run"]
                 for r in records if r["arms"][arm]["stage2"]])) if arm != "B0" else None,
        }

    for a, b in (("R3", "R1"), ("F", "R1"), ("R3", "F")):
        summary["paired"][f"{a}_vs_{b}"] = bootstrap_paired(records, a, b)

    # stage-1 config-alone pairing (F1 vs B0 at 20 iterations)
    a = np.array([1 if r["F1"]["info_errors"] > 0 else 0 for r in records])
    b = np.array([1 if r["B0"]["info_errors"] > 0 else 0 for r in records])
    wins = int(np.sum((a == 0) & (b == 1)))
    losses = int(np.sum((a == 1) & (b == 0)))
    p2, p1 = exact_binomial_two_sided(wins, losses)
    summary["paired"]["F1_vs_B0_stage1only"] = {
        "arm_a": "F1", "arm_b": "B0", "n": n,
        "point_estimate": float(a.mean() - b.mean()),
        "wins_a": wins, "losses_a": losses, "discordant": wins + losses,
        "exact_two_sided_p": p2, "exact_one_sided_p": p1,
    }

    # paired BER diff (R3 vs R1), point + bootstrap CI
    ea = np.array([r["arms"]["R3"]["final"]["info_errors"] for r in records])
    eb = np.array([r["arms"]["R1"]["final"]["info_errors"] for r in records])
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    m = len(records)
    bd = np.empty(BOOTSTRAP_RESAMPLES)
    for k in range(BOOTSTRAP_RESAMPLES):
        idx = rng.integers(0, m, size=m)
        bd[k] = ea[idx].mean() - eb[idx].mean()
    summary["paired_ber_R3_vs_R1"] = {
        "point_bit_diff": int(ea.sum() - eb.sum()),
        "point_ber_diff": float(ea.mean() - eb.mean()) / 1024,
        "ci95_ber_diff": [float(np.percentile(bd, 2.5)) / 1024,
                          float(np.percentile(bd, 97.5)) / 1024],
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify-mapping", action="store_true")
    group.add_argument("--anchor", action="store_true")
    group.add_argument("--regress-dev", action="store_true")
    group.add_argument("--generate", action="store_true")
    group.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.verify_mapping:
        verify_mapping(RescueDecoder(make_encoder()))
    elif args.anchor:
        anchor()
    elif args.regress_dev:
        regress_dev()
    elif args.generate:
        generate()
    elif args.run:
        run_confirm()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
