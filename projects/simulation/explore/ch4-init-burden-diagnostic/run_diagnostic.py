"""Phase-1 front-end initialization burden diagnostic (R031 task ②, D055/D056).

Question (contract.yaml): does replacing the current front-end initialization
(4-Walsh-preamble LS Jones estimate) with a truth initialization improve full-chain
FER/BER?  Oracle arms are Kill tools only (FR-21/TL-32); truth never enters any
deployable action, the B0 arm, the DA CPR, the LLR builder, or the decoder.

Discipline: this module is self-contained; it does not modify any frozen module.
Truth is recovered by replaying the frozen generator's RNG stream and is verified
bit-exactly against the frozen receiver inputs on every frame.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

RESULTS_ROOT = SIM_ROOT / "results" / "ch4-init-burden-diagnostic"
T077_RAW_PATH = (
    SIM_ROOT / "explore" / "ch5-apsk-llr-calibration" / "single_cell_evaluation_raw.json"
)

BOOTSTRAP_SEED = 2026092301
BOOTSTRAP_RESAMPLES = 10000
ARMS_EVAL = ("B0", "O1", "O1S", "O2")
CONTRACT_SPLITS: dict[str, dict[str, int]] = {
    "smoke": {"start": 2900, "stop_inclusive": 2907},
    "anchor_replay": {"start": 4000, "stop_inclusive": 4511},
    "eval": {"start": 60000, "stop_inclusive": 60511},
    "confirm": {"start": 61000, "stop_inclusive": 63047},
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SC = _load_module(
    "ibd_single_cell", HERE.parent / "ch5-apsk-llr-calibration" / "single_cell.py"
)
BR = SC._bridge()
CH4 = BR.CH4


def _array_sha256(value: np.ndarray) -> str:
    array = np.ascontiguousarray(value)
    digest = sha256()
    digest.update(str(array.shape).encode("ascii"))
    digest.update(array.dtype.str.encode("ascii"))
    digest.update(array.tobytes())
    return digest.hexdigest()


# ── truth extraction (RNG-stream replay + per-frame bit-exact verify) ────────


def extract_truth(seed: int, physical: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    """Recover jones/gg/phase by replaying the frozen generator's RNG order.

    Order (single_cell.generate_coded_physical_frame:244-266): legacy global RNG
    seeds gg_block then doppler_phase; PCG64(seed) draws random_su2 then the
    circular noise.  Verification reconstructs `received` bit-exactly.
    """
    cell = manifest["cell"]
    total = int(cell["continuous_total_symbols"])
    np.random.seed(int(seed))
    sampled_gg = BR.gg_block(
        total,
        cell["turbulence_alpha"],
        cell["turbulence_beta"],
        bs=cell["gamma_gamma_block"],
    )
    sampled_phase = BR.doppler_phase(
        total,
        f_res=cell["residual_frequency_hz"],
        f_dot=cell["frequency_slope_hz_per_s"],
        lw=cell["linewidth_hz"],
    )
    rng = np.random.default_rng(int(seed))
    jones = CH4.random_su2(rng)
    scalar = np.sqrt(sampled_gg) * np.exp(1j * sampled_phase)
    receiver = physical["receiver"]
    transmitted = np.concatenate(
        (receiver.ch4_pilot_tx, physical["truth_symbols"]), axis=1
    )
    pre_noise = jones @ (transmitted * scalar[None, :])
    noise_var = 10.0 ** (-cell["snr_db"] / 10.0)
    noise = np.sqrt(noise_var / 2.0) * (
        rng.standard_normal(pre_noise.shape) + 1j * rng.standard_normal(pre_noise.shape)
    )
    recon = pre_noise + noise
    received = np.concatenate((receiver.ch4_pilot_rx, receiver.rx), axis=1)
    if not np.array_equal(recon, received):
        raise RuntimeError(f"INVALID_TESTBED: truth replay mismatch at seed {seed}")
    return {
        "jones": jones,
        "scalar": scalar,
        "gg": sampled_gg,
        "noise": noise,
        "pre_noise": pre_noise,
    }


# ── arm construction ─────────────────────────────────────────────────────────


def _arm_frozen_spec(manifest: dict[str, Any]) -> Any:
    return BR.FrozenCh4Arm(
        arm_id=manifest["ch4"]["arm_id"],
        mode=manifest["ch4"]["mode"],
        mu=manifest["ch4"]["mu"],
    )


def make_init_runner(w_init: np.ndarray, *, freeze: bool) -> Callable:
    """ch4_runner override: start (or hold) the RDE at the injected matrix."""

    def runner(rx: np.ndarray, w0_ignored: np.ndarray, frozen_arm: Any) -> dict[str, Any]:
        del w0_ignored
        if freeze:
            z = w_init @ np.asarray(rx, dtype=np.complex128)
            return {
                "z": z,
                "W": np.array(w_init, dtype=np.complex128, copy=True),
                "gates": np.ones(z.shape, dtype=bool),
            }
        return CH4.run_plain_rde(rx, w_init, mu=frozen_arm.mu)

    return runner


def run_frame(
    codec: Any,
    *,
    seed: int,
    frame_index: int,
    manifest: dict[str, Any],
    arms: tuple[str, ...] = ARMS_EVAL,
) -> dict[str, Any]:
    cell = manifest["cell"]
    n0 = 10.0 ** (-cell["snr_db"] / 10.0)
    info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
    info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
    coded = np.asarray(codec.encode(info), dtype=np.uint8)
    physical = SC.generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
    receiver = physical["receiver"]
    truth = extract_truth(seed, physical, manifest)

    w0_b0 = CH4.pilot_ls_demux(receiver.ch4_pilot_rx, receiver.ch4_pilot_tx)
    noiseless_preamble = truth["jones"] @ (
        receiver.ch4_pilot_tx * truth["scalar"][: receiver.ch4_pilot_tx.shape[1]]
    )
    w_ideal = CH4.pilot_ls_demux(noiseless_preamble, receiver.ch4_pilot_tx)
    w_jones = truth["jones"].conj().T

    frozen_spec = _arm_frozen_spec(manifest)
    runners: dict[str, Callable | None] = {
        "B0": None,  # frozen path
        "O1": make_init_runner(w_jones, freeze=False),
        "O1S": make_init_runner(w_ideal, freeze=False),
        "O2": make_init_runner(w_ideal, freeze=True),
    }
    finals: dict[str, np.ndarray] = {}
    arm_records: dict[str, Any] = {}
    for name in arms:
        if runners[name] is None:
            result = SC.run_coded_receiver(receiver)
            compensated = result["compensated"]
            finals[name] = result["bundle"].ch4_W
        else:
            bundle, compensated = BR.run_bridge_with_observation(
                receiver, frozen_spec, ch4_runner=runners[name]
            )
            finals[name] = bundle.ch4_W
        if compensated.shape != (2, 256) or not np.all(np.isfinite(compensated)):
            raise RuntimeError(f"INVALID_TESTBED: arm {name} observation invalid")
        llr = SC.build_b0_llr(compensated, nominal_complex_noise_power=n0)
        decoded, _receipt = codec.decode_fresh(llr["llr"])
        errors = int(np.count_nonzero(decoded != info))
        arm_records[name] = {
            "bit_errors": errors,
            "fer": int(errors > 0),
            "decoder_input_sha256": llr["llr_sha256"],
        }

    frob = lambda a, b: float(np.linalg.norm(np.asarray(a) - np.asarray(b)))
    gg = truth["gg"]
    jones_metrics: dict[str, Any] = {
        "frob_w0_b0_vs_ideal": frob(w0_b0, w_ideal),
        "frob_w0_b0_vs_jonesH": frob(w0_b0, w_jones),
        "frob_ideal_vs_jonesH": frob(w_ideal, w_jones),
    }
    if "B0" in finals:
        jones_metrics["frob_Wfin_B0_vs_ideal"] = frob(finals["B0"], w_ideal)
    if "O1" in finals:
        jones_metrics["frob_Wfin_O1_vs_ideal"] = frob(finals["O1"], w_ideal)
        jones_metrics["frob_Wfin_O1_vs_jonesH"] = frob(finals["O1"], w_jones)
    if "O1S" in finals:
        jones_metrics["frob_Wfin_O1S_vs_ideal"] = frob(finals["O1S"], w_ideal)
    if "O2" in finals:
        jones_metrics["frob_Wfin_O2_vs_ideal"] = frob(finals["O2"], w_ideal)
    frame = {
        "frame_index": frame_index,
        "seed": int(seed),
        "arms": arm_records,
        "jones_metrics": jones_metrics,
        "gg_stats": {
            "obs_mean": float(np.mean(gg[4:])),
            "block1": float(gg[0]),
            "block2": float(gg[256]) if gg.size > 256 else None,
            "abs_scalar_pre_mean": float(np.mean(np.abs(truth["scalar"][:4]))),
        },
        "physical": {
            "received_observation_sha256": physical["physical_receipt"][
                "received_observation_sha256"
            ],
            "codeword_sha256": physical["physical_receipt"]["codeword_sha256"],
        },
        "truth_verified": True,
    }
    return frame


# ── statistics ───────────────────────────────────────────────────────────────


def exact_binomial_two_sided(wins: int, losses: int) -> tuple[float, float]:
    d = wins + losses
    if d == 0:
        return 1.0, 1.0
    lo = min(wins, losses)
    tail = sum(math.comb(d, i) for i in range(0, lo + 1)) / 2**d
    return min(1.0, 2 * tail), tail


def paired_fer_contrast(
    frames: list[dict[str, Any]], arm_hi: str, arm_lo: str
) -> dict[str, Any]:
    """Δ = FER(arm_hi) − FER(arm_lo); for B0_minus_O1 positive means O1 improves."""
    a = np.array([f["arms"][arm_hi]["fer"] for f in frames], dtype=np.int64)
    b = np.array([f["arms"][arm_lo]["fer"] for f in frames], dtype=np.int64)
    n = len(frames)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    diffs = np.empty(BOOTSTRAP_RESAMPLES)
    for k in range(BOOTSTRAP_RESAMPLES):
        idx = rng.integers(0, n, size=n)
        diffs[k] = a[idx].mean() - b[idx].mean()
    wins = int(np.sum((a == 1) & (b == 0)))  # arm_hi fails where arm_lo passes
    losses = int(np.sum((a == 0) & (b == 1)))
    p2, p1 = exact_binomial_two_sided(wins, losses)
    return {
        "contrast": f"{arm_hi}_minus_{arm_lo}",
        "n": n,
        "point": float(a.mean() - b.mean()),
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "wins_hi": wins,
        "losses_hi": losses,
        "discordant": wins + losses,
        "exact_two_sided_p": p2,
        "exact_one_sided_p": p1,
        "resamples": BOOTSTRAP_RESAMPLES,
        "seed": BOOTSTRAP_SEED,
    }


def paired_ber_contrast(
    frames: list[dict[str, Any]], arm_hi: str, arm_lo: str
) -> dict[str, Any]:
    a = np.array([f["arms"][arm_hi]["bit_errors"] for f in frames], dtype=np.int64)
    b = np.array([f["arms"][arm_lo]["bit_errors"] for f in frames], dtype=np.int64)
    n = len(frames)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    diffs = np.empty(BOOTSTRAP_RESAMPLES)
    for k in range(BOOTSTRAP_RESAMPLES):
        idx = rng.integers(0, n, size=n)
        diffs[k] = (a[idx].sum() - b[idx].sum()) / (n * 1024.0)
    return {
        "contrast": f"{arm_hi}_minus_{arm_lo}",
        "n": n,
        "point_ber_diff": float((a.sum() - b.sum()) / (n * 1024.0)),
        "bit_diff_total": int(a.sum() - b.sum()),
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "resamples": BOOTSTRAP_RESAMPLES,
        "seed": BOOTSTRAP_SEED,
    }


def stratified_fer(frames: list[dict[str, Any]]) -> dict[str, Any]:
    gg = np.array([f["gg_stats"]["obs_mean"] for f in frames])
    q25, q50, q75 = np.quantile(gg, [0.25, 0.5, 0.75])
    edges = [-np.inf, q25, q50, q75, np.inf]
    out = {"quantile_edges": [float(q25), float(q50), float(q75)], "strata": []}
    for i in range(4):
        mask = (gg > edges[i]) & (gg <= edges[i + 1])
        sub = [f for f, m in zip(frames, mask) if m]
        if not sub:
            continue
        row = {
            "stratum": f"Q{i+1}_deep_to_shallow",
            "n": len(sub),
            "gg_range": [float(np.min(gg[mask])), float(np.max(gg[mask]))],
        }
        for arm in ARMS_EVAL:
            row[f"fer_{arm}"] = float(np.mean([f["arms"][arm]["fer"] for f in sub]))
        if len(sub) >= 8:
            row["B0_minus_O1"] = paired_fer_contrast(sub, "B0", "O1")
            row["B0_minus_O1S"] = paired_fer_contrast(sub, "B0", "O1S")
        out["strata"].append(row)
    return out


def summarize(frames: list[dict[str, Any]], *, batch: str) -> dict[str, Any]:
    contrasts = {
        "B0_minus_O1": paired_fer_contrast(frames, "B0", "O1"),
        "B0_minus_O1S": paired_fer_contrast(frames, "B0", "O1S"),
        "B0_minus_O2": paired_fer_contrast(frames, "B0", "O2"),
        "O1S_minus_O2": paired_fer_contrast(frames, "O1S", "O2"),
        "O1S_minus_O1": paired_fer_contrast(frames, "O1S", "O1"),
    }
    ber = {
        "B0_minus_O1": paired_ber_contrast(frames, "B0", "O1"),
        "B0_minus_O1S": paired_ber_contrast(frames, "B0", "O1S"),
        "B0_minus_O2": paired_ber_contrast(frames, "B0", "O2"),
        "O1S_minus_O2": paired_ber_contrast(frames, "O1S", "O2"),
    }
    arm_rates = {}
    for arm in ARMS_EVAL:
        arm_rates[arm] = {
            "fer": float(np.mean([f["arms"][arm]["fer"] for f in frames])),
            "fer_count": int(sum(f["arms"][arm]["fer"] for f in frames)),
            "bit_errors": int(sum(f["arms"][arm]["bit_errors"] for f in frames)),
            "ber": float(
                sum(f["arms"][arm]["bit_errors"] for f in frames) / (len(frames) * 1024)
            ),
        }
    jones_summary = {}
    for key in frames[0]["jones_metrics"]:
        values = [f["jones_metrics"][key] for f in frames if f["jones_metrics"][key] is not None]
        if values:
            jones_summary[key] = {
                "mean": float(np.mean(values)),
                "median": float(np.median(values)),
                "q90": float(np.quantile(values, 0.9)),
            }
    decision = apply_decision(contrasts)
    return {
        "batch": batch,
        "n_frames": len(frames),
        "arm_rates": arm_rates,
        "fer_contrasts": contrasts,
        "ber_contrasts": ber,
        "stratified": stratified_fer(frames),
        "jones_error_summary": jones_summary,
        "preregistered_decision": decision,
    }


def apply_decision(contrasts: dict[str, Any]) -> dict[str, Any]:
    def status(c: dict[str, Any]) -> str:
        lo, hi = c["ci95"]
        if lo > 0:
            return "alive"
        if hi < 0:
            return "significantly_worse"
        return "flat" if c["point"] < 0.005 else "gray"

    s1 = status(contrasts["B0_minus_O1"])
    ss = status(contrasts["B0_minus_O1S"])
    if "alive" in (s1, ss):
        verdict = "ALIVE"
    elif s1 == "flat" and ss == "flat":
        verdict = "DEAD"
    else:
        verdict = "GRAY"
    return {
        "verdict": verdict,
        "O1_status": s1,
        "O1S_status": ss,
        "rule": "DEAD iff both flat (CI95 contains 0 and point<0.005); ALIVE iff either CI95 lower bound>0; else GRAY->confirm batch, same rule, gray again->DEAD",
    }


# ── runners with checkpoint/resume ──────────────────────────────────────────


def _save(data: dict[str, Any], name: str) -> None:
    from common import save_results

    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    save_results(data, str(RESULTS_ROOT / name), f"init-burden-diagnostic:{name}")


def run_batch(
    *,
    batch: str,
    arms: tuple[str, ...],
    raw_name: str,
    summary_name: str | None,
    checkpoint_every: int = 16,
    expect_frames: int | None = None,
) -> dict[str, Any]:
    manifest = SC.load_manifest()
    codec = SC._correctness().TargetApskCodec()
    split = CONTRACT_SPLITS[batch]
    seeds = list(range(split["start"], split["stop_inclusive"] + 1))
    raw_path = RESULTS_ROOT / raw_name
    raw: dict[str, Any] = {
        "schema_version": f"init-burden-diagnostic.{batch}.raw.v1",
        "contract": "explore/ch4-init-burden-diagnostic/contract.yaml (FROZEN_BEFORE_EXECUTION)",
        "manifest_hash": SC.manifest_sha256(),
        "batch": batch,
        "arms": list(arms),
        "frames": [],
    }
    if raw_path.exists():
        prior = json.loads(raw_path.read_text(encoding="utf-8"))
        prior.pop("_meta", None)
        if prior.get("manifest_hash") != raw["manifest_hash"] or prior.get("batch") != batch:
            raise RuntimeError("checkpoint does not match the frozen batch")
        prior_seeds = [int(f["seed"]) for f in prior.get("frames", [])]
        if prior_seeds != seeds[: len(prior_seeds)]:
            raise RuntimeError("checkpoint is not the frozen seed prefix")
        raw = prior
    t0 = time.time()
    for frame_index in range(len(raw["frames"]), len(seeds)):
        seed = seeds[frame_index]
        raw["frames"].append(
            run_frame(codec, seed=seed, frame_index=frame_index, manifest=manifest, arms=arms)
        )
        done = frame_index + 1
        if done % checkpoint_every == 0 or done == len(seeds):
            _save(raw, raw_name)
            elapsed = time.time() - t0
            print(
                f"[{batch}] {done}/{len(seeds)} frames, {elapsed:.0f}s elapsed",
                flush=True,
            )
    if summary_name is not None:
        summary = summarize(raw["frames"], batch=batch)
        summary["manifest_hash"] = raw["manifest_hash"]
        _save(summary, summary_name)
        print(json.dumps(summary["preregistered_decision"], indent=2))
        print(json.dumps(summary["arm_rates"], indent=2))
        return summary
    return raw


def cmd_anchor() -> int:
    manifest = SC.load_manifest()
    codec = SC._correctness().TargetApskCodec()
    split = CONTRACT_SPLITS["anchor_replay"]
    seeds = list(range(split["start"], split["stop_inclusive"] + 1))
    t077 = json.loads(T077_RAW_PATH.read_text(encoding="utf-8"))
    t077.pop("_meta", None)
    by_seed = {int(f["seed"]): f for f in t077["frames"]}
    mismatches: list[dict[str, Any]] = []
    t0 = time.time()
    report: dict[str, Any] = {
        "schema_version": "init-burden-diagnostic.anchor-replay.v1",
        "manifest_hash": SC.manifest_sha256(),
        "seeds": [split["start"], split["stop_inclusive"]],
        "frames": [],
    }
    for frame_index, seed in enumerate(seeds):
        frame = run_frame(codec, seed=seed, frame_index=frame_index, manifest=manifest, arms=("B0",))
        ref = by_seed[seed]["arms"]["B0"]
        match = frame["arms"]["B0"]["bit_errors"] == int(ref["bit_errors"])
        report["frames"].append(
            {
                "seed": int(seed),
                "bit_errors": frame["arms"]["B0"]["bit_errors"],
                "t077_bit_errors": int(ref["bit_errors"]),
                "match": bool(match),
            }
        )
        if not match:
            mismatches.append(report["frames"][-1])
        if (frame_index + 1) % 32 == 0 or frame_index + 1 == len(seeds):
            print(f"[anchor] {frame_index+1}/{len(seeds)} mismatches={len(mismatches)}", flush=True)
    fer = sum(f["bit_errors"] > 0 for f in report["frames"]) / len(seeds)
    report["aggregate"] = {
        "frames": len(seeds),
        "matched": len(seeds) - len(mismatches),
        "fer_this_run": fer,
        "fer_t077_anchor": 132 / 512,
        "elapsed_s": time.time() - t0,
    }
    report["gate"] = "PASS" if (not mismatches and len(seeds) == 512) else "FAIL"
    _save(report, "anchor_replay.json")
    print(json.dumps(report["aggregate"], indent=2))
    print("anchor gate:", report["gate"])
    return 0 if report["gate"] == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor", action="store_true", help="replay T077 seeds, B0 only")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--run-eval", action="store_true")
    parser.add_argument("--run-confirm", action="store_true")
    parser.add_argument("--summarize-eval", action="store_true")
    args = parser.parse_args()
    if args.anchor:
        return cmd_anchor()
    if args.smoke:
        run_batch(
            batch="smoke",
            arms=ARMS_EVAL,
            raw_name="smoke_raw.json",
            summary_name="smoke_summary.json",
            checkpoint_every=4,
        )
        return 0
    if args.run_eval:
        run_batch(
            batch="eval",
            arms=ARMS_EVAL,
            raw_name="eval512_raw.json",
            summary_name="eval512_summary.json",
        )
        return 0
    if args.run_confirm:
        run_batch(
            batch="confirm",
            arms=ARMS_EVAL,
            raw_name="confirm2048_raw.json",
            summary_name="confirm2048_summary.json",
            checkpoint_every=32,
        )
        return 0
    if args.summarize_eval:
        raw = json.loads((RESULTS_ROOT / "eval512_raw.json").read_text(encoding="utf-8"))
        raw.pop("_meta", None)
        summary = summarize(raw["frames"], batch="eval")
        summary["manifest_hash"] = raw.get("manifest_hash")
        _save(summary, "eval512_summary.json")
        print(json.dumps(summary["preregistered_decision"], indent=2))
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
