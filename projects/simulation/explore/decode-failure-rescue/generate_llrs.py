"""Per-frame exact-APP LLR cache for decode-failure-rescue.

Replays the frozen T077 physical chain
(``../ch5-apsk-llr-calibration/single_cell.py``) frame by frame:

1. info bits: T077 rule ``np.random.default_rng(np.random.SeedSequence(
   [seed, 77, 5]))`` -> ``integers(0,2,(1,1024),uint8)``
   (single_cell.py:518-519, 617-618, 1107-1108).  NOTE: this inherits the
   T077 rule on purpose instead of minting a new one -- the contract's
   ``llr_cache.consistency_anchor`` requires the regenerated eval 512 +
   B0(20 it) to reproduce the T077 numbers exactly
   (BER=0.04929351806640625, FER=132/512), which is only possible with the
   identical info-bit seed rule and physical seed.
2. coded bits: ``TargetApskCodec().encode`` (correctness.py:339).
3. physical frame: ``single_cell.generate_coded_physical_frame`` (:208).
4. receiver: ``single_cell.run_coded_receiver`` (:313).
5. LLR: ``single_cell.build_b0_llr`` (:381) with
   ``nominal_complex_noise_power = 10 ** (-snr_db/10)`` taken from the
   frozen manifest cell (single_cell.py:523, 615, 1079 -- the T077
   evaluation call sites; snr_db=15.0 -> nominal_n0 = 10^-1.5).

SNR override (contract addendum v1.1, diag17): ``--snr-db-override``
replicates the ``generate_coded_physical_frame`` construction path
(single_cell.py:208-310) field-by-field from the same manifest with the
single field ``snr_db`` replaced; the override value propagates to every
place the manifest snr_db enters the chain (noise realization
single_cell.py:263 and the nominal LLR noise power :523).  Cache directory
gets a ``_snrX`` suffix; npz metadata records the override and the copied
source line ranges.

Usage:
    python generate_llrs.py --split smoke|dev|eval [--snr-db-override 17.0]
                            [--limit N] [--force]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

RESULTS_ROOT = SIM_ROOT / "results" / "decode-failure-rescue"

# contract.yaml splits (FROZEN_BEFORE_EXECUTION)
SPLITS: dict[str, dict[str, int]] = {
    "smoke": {"start": 2900, "stop_inclusive": 2907},
    "dev": {"start": 5000, "stop_inclusive": 5063},
    "eval": {"start": 4000, "stop_inclusive": 4511},
}

SOURCE_REFS = {
    "info_bits_rule": "ch5-apsk-llr-calibration/single_cell.py:518-519,617-618,1107-1108",
    "encode": "ch5-apsk-llr-calibration/correctness.py:339-351",
    "physical_frame": "ch5-apsk-llr-calibration/single_cell.py:208-310",
    "receiver": "ch5-apsk-llr-calibration/single_cell.py:313-326",
    "nominal_n0_rule": "ch5-apsk-llr-calibration/single_cell.py:523,615,1079",
    "b0_llr": "ch5-apsk-llr-calibration/single_cell.py:381-401",
    "snr_override_copy": "ch5-apsk-llr-calibration/single_cell.py:208-310 (replicated with single snr_db field replaced)",
}


def _load_single_cell():
    path = HERE.parent / "ch5-apsk-llr-calibration" / "single_cell.py"
    spec = importlib.util.spec_from_file_location("dfr_single_cell", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["dfr_single_cell"] = module
    spec.loader.exec_module(module)
    return module


def _array_sha256(value: np.ndarray) -> str:
    array = np.ascontiguousarray(value)
    digest = sha256()
    digest.update(str(array.shape).encode("ascii"))
    digest.update(array.dtype.str.encode("ascii"))
    digest.update(array.tobytes())
    return digest.hexdigest()


def _generate_physical_frame_snr_override(sc, *, seed: int, coded_bits: np.ndarray,
                                          snr_db_override: float) -> dict[str, Any]:
    """Copy of single_cell.generate_coded_physical_frame (:208-310), one field overridden.

    Every config field is read from the same frozen manifest; only
    ``snr_db`` takes the override value.  RNG ownership and call order are
    preserved verbatim (legacy global seed for GG/CFO/Wiener, PCG64 for
    Jones/circular AWGN).
    """
    manifest = sc.load_manifest()
    cell = manifest["cell"]
    ch3 = manifest["ch3"]
    ch4 = manifest["ch4"]
    bridge = sc._bridge()
    mapping = sc.build_dp_symbol_frame(coded_bits)
    config = bridge.BridgeConfig.correctness_fixture(
        seed=int(seed),
        n_symbols=cell["observation_symbols_per_polarization"],
        observation_stop=cell["observation_symbols_per_polarization"],
        snr_db=float(snr_db_override),  # <-- the single overridden field
        turbulence_alpha=cell["turbulence_alpha"],
        turbulence_beta=cell["turbulence_beta"],
        gamma_gamma_block=cell["gamma_gamma_block"],
        f_residual_hz=cell["residual_frequency_hz"],
        f_dot_hz_per_s=cell["frequency_slope_hz_per_s"],
        linewidth_hz=cell["linewidth_hz"],
        ch4_pilot_count=ch4["acquisition_pilots"],
        pilot_indices=tuple(ch3["pilot_indices"]),
        pilot_label_shift=ch3["polarization_1_label_shift"],
        scope=(
            "SINGLE_PREREGISTERED_CELL",
            "NATURAL_HEADROOM_ONLY",
            "NO_PARAMETER_TUNING",
        ),
        cell_id=cell["cell_id"],
        window_id=f"frame-{int(seed)}",
        config_id=manifest["schema_version"],
        source_id=manifest["authority"],
    )
    np.random.seed(config.seed)
    rng = np.random.default_rng(config.seed)
    ch4_tx = bridge.CH4.orthogonal_pilots(config.ch4_pilot_count)
    transmitted = np.concatenate((ch4_tx, mapping["symbols"]), axis=1)
    sampled_gg = bridge.gg_block(
        transmitted.shape[1],
        config.turbulence_alpha,
        config.turbulence_beta,
        bs=config.gamma_gamma_block,
    )
    sampled_phase = bridge.doppler_phase(
        transmitted.shape[1],
        f_res=config.f_residual_hz,
        f_dot=config.f_dot_hz_per_s,
        lw=config.linewidth_hz,
    )
    scalar = np.sqrt(sampled_gg) * np.exp(1j * sampled_phase)
    jones = bridge.CH4.random_su2(rng)
    pre_noise = jones @ (transmitted * scalar[None, :])
    nominal_n0 = 10.0 ** (-config.snr_db / 10.0)
    noise = np.sqrt(nominal_n0 / 2.0) * (
        rng.standard_normal(pre_noise.shape) + 1j * rng.standard_normal(pre_noise.shape)
    )
    received = pre_noise + noise
    receiver = bridge.ReceiverVisibleInput(
        rx=received[:, config.ch4_pilot_count:],
        ch4_pilot_rx=received[:, : config.ch4_pilot_count],
        ch4_pilot_tx=ch4_tx,
        pilot_indices=sc.PILOT_INDICES.copy(),
        pilot_symbols=mapping["symbols"][:, sc.PILOT_INDICES].copy(),
        pilot_labels=mapping["point_labels"][:, sc.PILOT_INDICES].copy(),
        known_mask=mapping["known_mask"].copy(),
        observation_stop=config.observation_stop,
        config=config,
    )
    return {"receiver": receiver, "mapping": mapping}


def build_frame(sc, codec, *, seed: int, snr_db_override: float | None):
    """One full frame -> (llr, truth_info, truth_coded, receipt)."""
    info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
    info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
    coded = np.asarray(codec.encode(info), dtype=np.uint8)
    if snr_db_override is None:
        physical = sc.generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
        receiver = physical["receiver"]
    else:
        physical = _generate_physical_frame_snr_override(
            sc, seed=seed, coded_bits=coded[0], snr_db_override=snr_db_override
        )
        receiver = physical["receiver"]
    receiver_result = sc.run_coded_receiver(receiver)
    snr_db = (
        float(sc.load_manifest()["cell"]["snr_db"])
        if snr_db_override is None
        else float(snr_db_override)
    )
    nominal_n0 = 10.0 ** (-snr_db / 10.0)
    b0 = sc.build_b0_llr(
        receiver_result["compensated"], nominal_complex_noise_power=nominal_n0
    )
    llr = np.asarray(b0["llr"], dtype=np.float32).reshape(1536)
    return {
        "llr": llr,
        "truth_info": info[0].astype(np.uint8, copy=True),
        "truth_coded": coded[0].astype(np.uint8, copy=True),
        "llr_sha256": str(b0["llr_sha256"]),
        "received_observation_sha256": physical["physical_receipt"][
            "received_observation_sha256"
        ]
        if snr_db_override is None
        else _array_sha256(np.asarray(receiver.rx)),
    }


def cache_dir(split: str, snr_db_override: float | None) -> Path:
    tag = split if snr_db_override is None else f"{split}_snr{snr_db_override:g}"
    return RESULTS_ROOT / "llr_cache" / tag


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", required=True, choices=sorted(SPLITS))
    parser.add_argument("--snr-db-override", type=float, default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="generate only the first N frames of the split")
    parser.add_argument("--force", action="store_true",
                        help="regenerate frames even if the npz exists")
    args = parser.parse_args()

    sc = _load_single_cell()
    codec = sc._correctness().TargetApskCodec()
    manifest = sc.load_manifest()
    manifest_snr = float(manifest["cell"]["snr_db"])

    seeds = list(
        range(SPLITS[args.split]["start"], SPLITS[args.split]["stop_inclusive"] + 1)
    )
    if args.limit is not None:
        seeds = seeds[: args.limit]

    target = cache_dir(args.split, args.snr_db_override)
    target.mkdir(parents=True, exist_ok=True)
    meta_path = RESULTS_ROOT / f"generation_meta_{target.name}.json"

    timings: list[float] = []
    generated = skipped = 0
    for frame_index, seed in enumerate(seeds):
        out_path = target / f"frame_{seed}.npz"
        if out_path.exists() and not args.force:
            skipped += 1
            continue
        t0 = time.perf_counter()
        frame = build_frame(
            sc, codec, seed=seed, snr_db_override=args.snr_db_override
        )
        elapsed = time.perf_counter() - t0
        timings.append(elapsed)
        np.savez_compressed(
            out_path,
            llr=frame["llr"],
            truth_info=frame["truth_info"],
            truth_coded=frame["truth_coded"],
            llr_sha256=frame["llr_sha256"],
            received_observation_sha256=frame["received_observation_sha256"],
            seed=np.int64(seed),
            frame_index=np.int64(frame_index),
            split=args.split,
            snr_db=(manifest_snr if args.snr_db_override is None
                    else float(args.snr_db_override)),
            snr_db_manifest=manifest_snr,
            snr_db_override=(np.float64(args.snr_db_override)
                             if args.snr_db_override is not None else np.float64(np.nan)),
            source_refs=json.dumps(SOURCE_REFS),
        )
        generated += 1
        print(f"[{args.split}] frame seed={seed} done in {elapsed:.2f}s", flush=True)

    import sionna
    import torch

    meta = {
        "schema_version": "dfr.llr-cache.generation-meta.v1",
        "split": args.split,
        "snr_db_override": args.snr_db_override,
        "cache_dir": str(target),
        "seeds": {"start": seeds[0], "stop_inclusive": seeds[-1], "count": len(seeds)},
        "generated": generated,
        "skipped_existing": skipped,
        "per_frame_seconds": timings,
        "mean_frame_seconds": (float(np.mean(timings)) if timings else None),
        "versions": {
            "python": sys.version.split()[0],
            "sionna": sionna.__version__,
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
        "source_refs": SOURCE_REFS,
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "per_frame_seconds"},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
