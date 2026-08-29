"""T077 frozen single-cell mapping and experiment core.

The deployable receiver path is truth-free.  Scorer-only payload truth is kept
behind separate functions as the implementation grows through RED/GREEN gates.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

import numpy as np
import yaml


HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

MANIFEST_PATH = HERE / "single_cell_manifest.yaml"
PILOT_INDICES = np.arange(0, 256, 4, dtype=np.int64)
NONPILOT_INDICES = np.setdiff1d(np.arange(256, dtype=np.int64), PILOT_INDICES)
AUDIT_PAIR_FIELD_ORDER = (
    "manifest_hash",
    "frame_index",
    "seed",
    "info_bits_sha256",
    "coded_bits_sha256",
    "mapping_sha256",
    "physical.codeword_sha256",
    "physical.mapping_sha256",
    "physical.receiver_input_sha256",
    "physical.received_observation_sha256",
    "realization_hash",
    "bundle_hash",
    "pair_hash",
)


def _load_file(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


@lru_cache(maxsize=1)
def _correctness():
    return _load_file(HERE / "correctness.py", "t077_correctness")


@lru_cache(maxsize=1)
def _bridge():
    directory = HERE.parent / "ch5-apsk-structured-covariance"
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
    return _load_file(directory / "post_ch4_ch3_bridge.py", "t077_t066_bridge")


@lru_cache(maxsize=1)
def _reducer():
    return _load_file(HERE / "single_cell_reducer.py", "t077_single_cell_reducer")


def gate1_metrics(*args, **kwargs) -> dict[str, Any]:
    return _reducer().gate1_metrics(*args, **kwargs)


def paired_rate_difference_ci(*args, **kwargs) -> dict[str, Any]:
    return _reducer().paired_rate_difference_ci(*args, **kwargs)


def gate2_decision(*args, **kwargs) -> dict[str, Any]:
    return _reducer().gate2_decision(*args, **kwargs)


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def manifest_sha256() -> str:
    return sha256(MANIFEST_PATH.read_bytes()).hexdigest()


def audit_pair_receipt(frame: dict[str, Any], *, manifest_hash: str) -> dict[str, Any]:
    """Hash only persisted raw summaries in one frozen, reviewer-visible order."""
    values = (
        manifest_hash,
        int(frame["frame_index"]),
        int(frame["seed"]),
        frame["info_bits_sha256"],
        frame["coded_bits_sha256"],
        frame["mapping_sha256"],
        frame["physical"]["codeword_sha256"],
        frame["physical"]["mapping_sha256"],
        frame["physical"]["receiver_input_sha256"],
        frame["physical"]["received_observation_sha256"],
        frame["realization_hash"],
        frame["bundle_hash"],
        frame["pair_hash"],
    )
    ordered = [[name, value] for name, value in zip(AUDIT_PAIR_FIELD_ORDER, values)]
    canonical = json.dumps(ordered, ensure_ascii=True, separators=(",", ":"))
    return {
        "schema_version": "t077.audit-pair.persisted-summaries.v1",
        "serialization": "canonical_json_ordered_name_value_pairs",
        "field_order": list(AUDIT_PAIR_FIELD_ORDER),
        "values": list(values),
        "audit_pair_sha256": sha256(canonical.encode("utf-8")).hexdigest(),
    }


def _binary_groups(bits: np.ndarray) -> np.ndarray:
    coded = np.asarray(bits)
    if coded.shape != (1536,) or not np.all((coded == 0) | (coded == 1)):
        raise ValueError("one physical frame requires one binary (1536,) codeword")
    return coded.astype(np.uint8, copy=False).reshape(384, 4)


def build_dp_symbol_frame(coded_bits: np.ndarray) -> dict[str, Any]:
    """Fill the 384 DP non-pilot slots in frozen pol-major order."""
    from common._modulation import m16apsk_mod

    groups = _binary_groups(coded_bits)
    symbols, bits_by_label = _correctness().apsk16_table()
    weights = np.array([8, 4, 2, 1], dtype=np.uint8)
    payload_labels = (groups @ weights).astype(np.int64)

    labels = np.empty((2, 256), dtype=np.int64)
    balanced = np.tile(np.arange(16, dtype=np.int64), 4)
    labels[0, PILOT_INDICES] = balanced
    labels[1, PILOT_INDICES] = np.roll(balanced, 3)
    labels[0, NONPILOT_INDICES] = payload_labels[:192]
    labels[1, NONPILOT_INDICES] = payload_labels[192:]
    frame_symbols = symbols[labels]

    owner_payload = np.asarray(m16apsk_mod(np.asarray(coded_bits).reshape(-1)))
    mapped_payload = np.concatenate(
        (frame_symbols[0, NONPILOT_INDICES], frame_symbols[1, NONPILOT_INDICES])
    )
    if not np.array_equal(owner_payload, mapped_payload):
        raise RuntimeError("project m16apsk_mod and frozen pol-major table disagree")

    known_mask = np.zeros((2, 256), dtype=bool)
    known_mask[:, PILOT_INDICES] = True
    digest = sha256()
    for value in (
        np.asarray(coded_bits, dtype=np.uint8),
        labels,
        frame_symbols.view(np.float64),
        known_mask,
    ):
        array = np.ascontiguousarray(value)
        digest.update(str(array.shape).encode("ascii"))
        digest.update(array.dtype.str.encode("ascii"))
        digest.update(array.tobytes())
    return {
        "symbols": frame_symbols,
        "point_labels": labels,
        "bits_by_label": bits_by_label,
        "known_mask": known_mask,
        "pilot_indices": PILOT_INDICES.copy(),
        "nonpilot_indices": NONPILOT_INDICES.copy(),
        "mapping_receipt": {
            "coded_bits": 1536,
            "apsk_symbols": 384,
            "pilot_slots": 128,
            "nonpilot_slots": 384,
            "mapping": "pol-major:pol0[192],pol1[192]",
            "mapping_sha256": digest.hexdigest(),
        },
    }


def extract_coded_bits(point_labels: np.ndarray) -> np.ndarray:
    labels = np.asarray(point_labels)
    if labels.shape != (2, 256) or np.any(labels < 0) or np.any(labels >= 16):
        raise ValueError("point_labels must be a valid (2,256) APSK label frame")
    _, bits_by_label = _correctness().apsk16_table()
    groups = np.concatenate(
        (bits_by_label[labels[0, NONPILOT_INDICES]], bits_by_label[labels[1, NONPILOT_INDICES]])
    )
    return groups.reshape(1536).astype(np.uint8, copy=False)


def _array_sha256(value: np.ndarray) -> str:
    array = np.ascontiguousarray(value)
    digest = sha256()
    digest.update(str(array.shape).encode("ascii"))
    digest.update(array.dtype.str.encode("ascii"))
    digest.update(array.tobytes())
    return digest.hexdigest()


def generate_coded_physical_frame(*, seed: int, coded_bits: np.ndarray) -> dict[str, Any]:
    """Generate the frozen T066 physical chain with a mapped target codeword."""
    manifest = load_manifest()
    cell = manifest["cell"]
    ch3 = manifest["ch3"]
    ch4 = manifest["ch4"]
    bridge = _bridge()
    mapping = build_dp_symbol_frame(coded_bits)
    config = bridge.BridgeConfig.correctness_fixture(
        seed=int(seed),
        n_symbols=cell["observation_symbols_per_polarization"],
        observation_stop=cell["observation_symbols_per_polarization"],
        snr_db=cell["snr_db"],
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

    # Preserve the T066 structural call order and RNG ownership: legacy global
    # RNG for GG/CFO/Wiener, PCG64 for Jones and circular AWGN. T066 raw is not
    # treated as a bit-exact seed oracle; timing/cell invariants are the contract.
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
        rx=received[:, config.ch4_pilot_count :],
        ch4_pilot_rx=received[:, : config.ch4_pilot_count],
        ch4_pilot_tx=ch4_tx,
        pilot_indices=PILOT_INDICES.copy(),
        pilot_symbols=mapping["symbols"][:, PILOT_INDICES].copy(),
        pilot_labels=mapping["point_labels"][:, PILOT_INDICES].copy(),
        known_mask=mapping["known_mask"].copy(),
        observation_stop=config.observation_stop,
        config=config,
    )
    receiver_hash = sha256()
    for value in (
        receiver.rx,
        receiver.ch4_pilot_rx,
        receiver.ch4_pilot_tx,
        receiver.pilot_symbols,
        receiver.known_mask,
    ):
        receiver_hash.update(_array_sha256(np.asarray(value)).encode("ascii"))
    receipt = {
        "seed": int(seed),
        "preamble_symbols": config.ch4_pilot_count,
        "observation_symbols_per_polarization": config.n_symbols,
        "continuous_total_symbols": int(transmitted.shape[1]),
        "gamma_gamma_block": config.gamma_gamma_block,
        "observation_first_block_symbols": config.gamma_gamma_block - config.ch4_pilot_count,
        "observation_next_block_symbols": (
            transmitted.shape[1] - config.gamma_gamma_block
        ),
        "receiver_input_sha256": receiver_hash.hexdigest(),
        "received_observation_sha256": _array_sha256(receiver.rx),
        "codeword_sha256": _array_sha256(np.asarray(coded_bits, dtype=np.uint8)),
        "mapping_sha256": mapping["mapping_receipt"]["mapping_sha256"],
        "gg_sha256": _array_sha256(np.asarray(sampled_gg)),
        "phase_sha256": _array_sha256(np.asarray(sampled_phase)),
    }
    return {
        "receiver": receiver,
        "mapping": mapping,
        "truth_symbols": mapping["symbols"].copy(),
        "physical_receipt": receipt,
    }


def run_coded_receiver(receiver: Any) -> dict[str, Any]:
    manifest = load_manifest()
    bridge = _bridge()
    arm = bridge.FrozenCh4Arm(
        arm_id=manifest["ch4"]["arm_id"],
        mode=manifest["ch4"]["mode"],
        mu=manifest["ch4"]["mu"],
        ring_threshold=None,
        decision_threshold=None,
    )
    bundle, compensated = bridge.run_bridge_with_observation(receiver, arm)
    if compensated.shape != (2, 256) or not np.all(np.isfinite(compensated)):
        raise RuntimeError("INVALID_TESTBED: coded receiver observation is invalid")
    return {"bundle": bundle, "compensated": compensated}


def _pooled_unbiased_complex_variance(
    observed: np.ndarray, reference: np.ndarray
) -> float:
    values = np.asarray(observed, dtype=np.complex128)
    truth = np.asarray(reference, dtype=np.complex128)
    if values.shape != truth.shape or values.ndim != 2 or values.shape[0] != 2:
        raise ValueError("variance inputs must be aligned [two polarizations,N]")
    if values.shape[1] < 2 or not np.all(np.isfinite(values)) or not np.all(np.isfinite(truth)):
        raise ValueError("variance inputs need finite samples per polarization")
    residual = values - truth
    demeaned = residual - residual.mean(axis=1, keepdims=True)
    estimate = float(np.sum(np.abs(demeaned) ** 2) / (2 * (values.shape[1] - 1)))
    if not np.isfinite(estimate) or estimate <= 0.0:
        raise RuntimeError("residual variance must be finite and positive")
    return estimate


def estimate_receiver_pilot_n0(
    compensated: np.ndarray, pilot_reference: np.ndarray, known_mask: np.ndarray
) -> float:
    z = np.asarray(compensated, dtype=np.complex128)
    mask = np.asarray(known_mask, dtype=bool)
    pilots = np.asarray(pilot_reference, dtype=np.complex128)
    if z.shape != (2, 256) or mask.shape != z.shape:
        raise ValueError("receiver observation and known mask must be (2,256)")
    if np.count_nonzero(mask, axis=1).tolist() != [64, 64] or pilots.shape != (2, 64):
        raise ValueError("frozen frame needs exactly 64 aligned pilots per polarization")
    observed = np.stack((z[0, mask[0]], z[1, mask[1]]))
    return _pooled_unbiased_complex_variance(observed, pilots)


def estimate_scorer_payload_n0(
    compensated: np.ndarray, transmitted_symbols: np.ndarray
) -> float:
    z = np.asarray(compensated, dtype=np.complex128)
    truth = np.asarray(transmitted_symbols, dtype=np.complex128)
    if z.shape != (2, 256) or truth.shape != z.shape:
        raise ValueError("payload scorer needs aligned (2,256) observation and truth")
    return _pooled_unbiased_complex_variance(
        z[:, NONPILOT_INDICES], truth[:, NONPILOT_INDICES]
    )


def _llr_clip_diagnostics(unclipped: np.ndarray, post_scale: np.ndarray) -> dict[str, int]:
    return {
        "demapper_clip30": int(np.count_nonzero(np.abs(unclipped) > 30.0)),
        "decode_clip30": int(np.count_nonzero(np.abs(post_scale) > 30.0)),
        "backend_clip20": int(np.count_nonzero(np.abs(np.clip(post_scale, -30.0, 30.0)) > 20.0)),
        "total_llrs": int(post_scale.size),
    }


def build_b0_llr(
    compensated: np.ndarray, *, nominal_complex_noise_power: float
) -> dict[str, Any]:
    z = np.asarray(compensated, dtype=np.complex128)
    nominal_n0 = float(nominal_complex_noise_power)
    if z.shape != (2, 256) or not np.all(np.isfinite(z)):
        raise ValueError("B0 receiver observation must be finite (2,256)")
    if not np.isfinite(nominal_n0) or nominal_n0 <= 0.0:
        raise ValueError("nominal noise power must be finite and positive")
    payload = np.concatenate((z[0, NONPILOT_INDICES], z[1, NONPILOT_INDICES]))
    raw = _correctness().exact_app_llr(
        payload, complex_noise_power=nominal_n0, clip=None
    ).reshape(1, 1536)
    llr = np.clip(raw, -30.0, 30.0)
    return {
        "llr": llr,
        "unclipped": raw,
        "payload_samples": payload,
        "llr_sha256": _array_sha256(llr),
        "clip": _llr_clip_diagnostics(raw, llr),
    }


def build_receiver_arms(
    compensated: np.ndarray,
    pilot_reference: np.ndarray,
    known_mask: np.ndarray,
    *,
    nominal_complex_noise_power: float,
    b1_scalar: float,
) -> dict[str, Any]:
    """Build receiver-visible B0/B1/B2/B3; no scorer truth is accepted."""
    z = np.asarray(compensated, dtype=np.complex128)
    mask = np.asarray(known_mask, dtype=bool)
    pilots = np.asarray(pilot_reference, dtype=np.complex128)
    if z.shape != (2, 256) or mask.shape != z.shape:
        raise ValueError("receiver observation and known mask must be (2,256)")
    if np.count_nonzero(mask, axis=1).tolist() != [64, 64] or pilots.shape != (2, 64):
        raise ValueError("frozen frame needs exactly 64 aligned pilots per polarization")
    estimated_n0 = estimate_receiver_pilot_n0(z, pilots, mask)
    nominal_n0 = float(nominal_complex_noise_power)
    fixed = float(b1_scalar)
    if not np.isfinite(nominal_n0) or nominal_n0 <= 0.0:
        raise ValueError("nominal noise power must be finite and positive")
    if not np.isfinite(fixed) or fixed <= 0.0:
        raise ValueError("B1 scalar must be finite and positive")
    b0_result = build_b0_llr(z, nominal_complex_noise_power=nominal_n0)
    payload = b0_result["payload_samples"]
    correctness = _correctness()
    b0_unclipped = b0_result["unclipped"]
    b0 = b0_result["llr"]
    scalar = nominal_n0 / estimated_n0
    b1 = fixed * b0
    b2 = scalar * b0
    b3_unclipped = correctness.exact_app_llr(
        payload, complex_noise_power=estimated_n0, clip=None
    ).reshape(1, 1536)
    b3 = np.clip(b3_unclipped, -30.0, 30.0)
    llrs = {"B0": b0, "B1": b1, "B2": b2, "B3": b3}
    return {
        "llrs": llrs,
        "receiver_hashes": {name: _array_sha256(value) for name, value in llrs.items()},
        "estimated_n0_pilot": estimated_n0,
        "b1_scalar": fixed,
        "b2_scalar": scalar,
        "physical_frame_scalars": 1,
        "payload_samples": payload,
        "clip": {
            "B0": _llr_clip_diagnostics(b0_unclipped, b0),
            "B1": _llr_clip_diagnostics(b0_unclipped, b1),
            "B2": _llr_clip_diagnostics(b0_unclipped, b2),
            "B3": _llr_clip_diagnostics(b3_unclipped, b3),
        },
    }


def build_payload_oracle(
    compensated: np.ndarray, transmitted_symbols: np.ndarray
) -> dict[str, Any]:
    """Scorer-only O1 payload-truth auxiliary variance and exact-APP LLR."""
    z = np.asarray(compensated, dtype=np.complex128)
    truth = np.asarray(transmitted_symbols, dtype=np.complex128)
    if z.shape != (2, 256) or truth.shape != z.shape:
        raise ValueError("O1 scorer needs aligned (2,256) observation and truth")
    z_payload = z[:, NONPILOT_INDICES]
    x_payload = truth[:, NONPILOT_INDICES]
    n0_payload = estimate_scorer_payload_n0(z, truth)
    payload = np.concatenate((z_payload[0], z_payload[1]))
    raw = _correctness().exact_app_llr(
        payload, complex_noise_power=n0_payload, clip=None
    ).reshape(1, 1536)
    llr = np.clip(raw, -30.0, 30.0)
    return {
        "llr": llr,
        "estimated_n0_payload": n0_payload,
        "llr_sha256": _array_sha256(llr),
        "clip": _llr_clip_diagnostics(raw, llr),
    }


def _frame_pair_hash(
    *, physical: dict[str, Any], bundle: Any, info_bits: np.ndarray, coded_bits: np.ndarray
) -> str:
    digest = sha256()
    for value in (
        manifest_sha256(),
        _physical_pair_identity(physical, coded_bits),
        bundle.realization_hash,
        bundle.bundle_hash,
        _array_sha256(info_bits),
    ):
        digest.update(str(value).encode("ascii"))
    return digest.hexdigest()


def _physical_pair_identity(physical: dict[str, Any], coded_bits: np.ndarray) -> str:
    """Bind one codeword to the complete receiver-visible physical realization."""
    receiver = physical["receiver"]
    digest = sha256()
    for value in (
        np.asarray(coded_bits, dtype=np.uint8),
        receiver.rx,
        receiver.ch4_pilot_rx,
        receiver.ch4_pilot_tx,
        receiver.pilot_symbols,
        receiver.known_mask,
    ):
        digest.update(_array_sha256(np.asarray(value)).encode("ascii"))
    digest.update(
        physical["mapping"]["mapping_receipt"]["mapping_sha256"].encode("ascii")
    )
    return digest.hexdigest()


def run_live_integration_point_check(*, write: bool, seed: int = 2900) -> dict[str, Any]:
    """Exercise one real encoder/physical frame/five-arm fresh decoder chain."""
    codec = _correctness().TargetApskCodec()
    info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
    info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
    coded = np.asarray(codec.encode(info), dtype=np.uint8)
    physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
    receiver_result = run_coded_receiver(physical["receiver"])
    nominal_n0 = 10.0 ** (-load_manifest()["cell"]["snr_db"] / 10.0)
    receiver_arms = build_receiver_arms(
        receiver_result["compensated"],
        physical["receiver"].pilot_symbols,
        physical["receiver"].known_mask,
        nominal_complex_noise_power=nominal_n0,
        b1_scalar=1.0,
    )
    oracle = build_payload_oracle(
        receiver_result["compensated"], physical["truth_symbols"]
    )
    arms = dict(receiver_arms["llrs"])
    arms["O1"] = oracle["llr"]
    pair_hash = _frame_pair_hash(
        physical=physical,
        bundle=receiver_result["bundle"],
        info_bits=info,
        coded_bits=coded,
    )
    arm_records = {}
    for name, llr in arms.items():
        decoded, decode_receipt = codec.decode_fresh(llr)
        errors = int(np.count_nonzero(decoded != info))
        arm_records[name] = {
            "pair_hash": pair_hash,
            "decoder_input_sha256": _array_sha256(llr),
            "bit_errors": errors,
            "fer": int(errors > 0),
            "restart": bool(decode_receipt["restart"]),
            "configured_iterations": int(decode_receipt["configured_iterations"]),
        }
    raw = {
        "schema_version": "t077.c5-0-single-cell.live-point.raw.v1",
        "manifest_hash": manifest_sha256(),
        "frames": [
            {
                "seed": int(seed),
                "physical": physical["physical_receipt"],
                "pair_hash": pair_hash,
                "arms": arm_records,
            }
        ],
    }
    fresh = all(
        arm["restart"] and arm["configured_iterations"] == 20
        for arm in arm_records.values()
    )
    receipt = {
        "schema_version": "t077.c5-0-single-cell.live-point.receipt.v1",
        "manifest_hash": manifest_sha256(),
        "completed_frames": 1,
        "seed": int(seed),
        "codec": "TargetApskCodec",
        "fresh_live_decode": "PASS" if fresh else "FAIL",
        "physical_pair_hash": (
            "PASS"
            if len({arm["pair_hash"] for arm in arm_records.values()}) == 1
            else "FAIL"
        ),
        "scientific_use": False,
    }
    if write:
        from common import save_results

        save_results(raw, str(HERE / "single_cell_live_point_raw.json"), "t077:live-point-raw")
        save_results(
            receipt,
            str(HERE / "single_cell_live_point_receipt.json"),
            "t077:live-point-receipt",
        )
    return {"raw": raw, "receipt": receipt}


def run_correctness_smoke(*, write: bool, codec_factory=None) -> dict[str, Any]:
    manifest = load_manifest()
    split = manifest["splits"]["smoke"]
    seeds = list(range(split["seeds"]["start"], split["seeds"]["stop_inclusive"] + 1))
    if len(seeds) != 8:
        raise RuntimeError("smoke manifest must freeze exactly eight seeds")
    injected_codec = codec_factory is not None
    if write and injected_codec:
        raise ValueError("an injected codec is test-only and cannot write live artifacts")
    if codec_factory is None:
        codec_factory = _correctness().TargetApskCodec
    codec = codec_factory()
    codec_name = type(codec).__name__
    frames = []
    mapping_ok = True
    receiver_api_truth_exclusion_ok = True
    paired_ok = True
    fresh_ok = True
    pair_hashes = []
    nominal_n0 = 10.0 ** (-manifest["cell"]["snr_db"] / 10.0)
    for frame_index, seed in enumerate(seeds):
        info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
        info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
        coded = np.asarray(codec.encode(info), dtype=np.uint8)
        physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
        receiver_result = run_coded_receiver(physical["receiver"])
        receiver_arms = build_receiver_arms(
            receiver_result["compensated"],
            physical["receiver"].pilot_symbols,
            physical["receiver"].known_mask,
            nominal_complex_noise_power=nominal_n0,
            b1_scalar=1.0,
        )
        oracle = build_payload_oracle(
            receiver_result["compensated"], physical["truth_symbols"]
        )
        arms = dict(receiver_arms["llrs"])
        arms["O1"] = oracle["llr"]
        pair_hash = _frame_pair_hash(
            physical=physical,
            bundle=receiver_result["bundle"],
            info_bits=info,
            coded_bits=coded,
        )
        pair_hashes.append(pair_hash)
        arm_records = {}
        for arm_name, llr in arms.items():
            decoded, decode_receipt = codec.decode_fresh(llr)
            bit_errors = int(np.count_nonzero(decoded != info))
            arm_records[arm_name] = {
                "pair_hash": pair_hash,
                "decoder_input_sha256": _array_sha256(llr),
                "bit_errors": bit_errors,
                "fer": int(bit_errors > 0),
                "restart": bool(decode_receipt["restart"]),
                "configured_iterations": int(decode_receipt["configured_iterations"]),
            }
            fresh_ok &= arm_records[arm_name]["restart"]
            fresh_ok &= arm_records[arm_name]["configured_iterations"] == 20
        mapping_ok &= np.array_equal(
            extract_coded_bits(physical["mapping"]["point_labels"]), coded[0]
        )
        # Mutating scorer-only truth cannot reach the receiver-arm API.
        truth_mutant = physical["truth_symbols"].copy()
        truth_mutant[:, NONPILOT_INDICES] *= -1
        receiver_repeat = build_receiver_arms(
            receiver_result["compensated"],
            physical["receiver"].pilot_symbols,
            physical["receiver"].known_mask,
            nominal_complex_noise_power=nominal_n0,
            b1_scalar=1.0,
        )
        receiver_api_truth_exclusion_ok &= (
            receiver_arms["receiver_hashes"] == receiver_repeat["receiver_hashes"]
        )
        receiver_api_truth_exclusion_ok &= not np.array_equal(
            truth_mutant, physical["truth_symbols"]
        )
        paired_ok &= len({entry["pair_hash"] for entry in arm_records.values()}) == 1
        frames.append(
            {
                "frame_index": frame_index,
                "seed": seed,
                "manifest_hash": manifest_sha256(),
                "mapping": physical["mapping"]["mapping_receipt"],
                "physical": physical["physical_receipt"],
                "realization_hash": receiver_result["bundle"].realization_hash,
                "bundle_hash": receiver_result["bundle"].bundle_hash,
                "pair_hash": pair_hash,
                "estimated_n0_pilot": receiver_arms["estimated_n0_pilot"],
                "estimated_n0_payload": oracle["estimated_n0_payload"],
                "b2_scalar": receiver_arms["b2_scalar"],
                "arms": arm_records,
            }
        )
    raw = {
        "schema_version": "t077.c5-0-single-cell.smoke.raw.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "codec": codec_name,
        "live_backend": not injected_codec,
        "frames": frames,
    }
    receipt = {
        "schema_version": "t077.c5-0-single-cell.smoke.receipt.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "codec": codec_name,
        "live_backend": not injected_codec,
        "completed_frames": len(frames),
        "seeds": seeds,
        "mapping_firewall": "PASS" if mapping_ok else "FAIL",
        "receiver_api_truth_exclusion": (
            "PASS" if receiver_api_truth_exclusion_ok else "FAIL"
        ),
        "truth_exclusion_evidence": (
            "receiver_api_signature_and_identical_input_replay"
        ),
        "paired_hashes": "PASS" if paired_ok else "FAIL",
        "fresh_decode_lifecycle": "PASS" if fresh_ok else "FAIL",
        "unique_pair_hashes": len(set(pair_hashes)),
        "scientific_use": False,
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["receipt_hash"] = sha256(canonical.encode("utf-8")).hexdigest()
    if write:
        from common import save_results

        save_results(raw, str(HERE / "single_cell_smoke_raw.json"), "t077:smoke-raw")
        save_results(
            receipt, str(HERE / "single_cell_smoke_receipt.json"), "t077:smoke-receipt"
        )
    return {"raw": raw, "receipt": receipt}


def b1_scalar_grid() -> np.ndarray:
    spec = load_manifest()["splits"]["calibration"]["scalar_exponent_grid"]
    exponents = np.arange(
        spec["start"], spec["stop_inclusive"] + 1, spec["step"], dtype=np.float64
    )
    return 2.0 ** (exponents / 2.0)


def select_b1_scalar(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply the frozen FER/BER/log-distance/numeric calibration tie-break."""
    if not records:
        raise ValueError("calibration records cannot be empty")
    ordered = sorted(
        records,
        key=lambda row: (
            int(row["fer"]),
            int(row["bit_errors"]),
            abs(float(np.log(float(row["scalar"])))),
            float(row["scalar"]),
        ),
    )
    winner = dict(ordered[0])
    winner["tie_break"] = ["fer", "ber", "abs_log_scalar", "scalar"]
    return winner


def run_b1_calibration(*, write: bool = True, resume: bool = True) -> dict[str, Any]:
    """Run/resume the disjoint 64-frame calibration and freeze one B1 scalar."""
    manifest = load_manifest()
    split = manifest["splits"]["calibration"]
    seeds = list(range(split["seeds"]["start"], split["seeds"]["stop_inclusive"] + 1))
    if len(seeds) != 64:
        raise RuntimeError("calibration manifest must freeze exactly 64 frames")
    raw_path = HERE / "single_cell_calibration_raw.json"
    raw: dict[str, Any] = {
        "schema_version": "t077.c5-0-single-cell.calibration.raw.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "codec": "TargetApskCodec",
        "live_backend": True,
        "seeds": seeds,
        "scalar_grid": b1_scalar_grid().tolist(),
        "frames": [],
    }
    if resume and raw_path.exists():
        prior = json.loads(raw_path.read_text(encoding="utf-8"))
        prior.pop("_meta", None)
        if prior.get("manifest_hash") != manifest_sha256() or prior.get("seeds") != seeds:
            raise RuntimeError("calibration checkpoint does not match the frozen manifest")
        prior_seeds = [int(frame["seed"]) for frame in prior.get("frames", [])]
        if prior_seeds != seeds[: len(prior_seeds)]:
            raise RuntimeError("calibration checkpoint is not a frozen seed prefix")
        raw = prior
    codec = _correctness().TargetApskCodec()
    nominal_n0 = 10.0 ** (-manifest["cell"]["snr_db"] / 10.0)
    grid = b1_scalar_grid()
    for frame_index in range(len(raw["frames"]), len(seeds)):
        seed = seeds[frame_index]
        info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
        info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
        coded = np.asarray(codec.encode(info), dtype=np.uint8)
        physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
        receiver_result = run_coded_receiver(physical["receiver"])
        receiver_arms = build_receiver_arms(
            receiver_result["compensated"],
            physical["receiver"].pilot_symbols,
            physical["receiver"].known_mask,
            nominal_complex_noise_power=nominal_n0,
            b1_scalar=1.0,
        )
        b0 = receiver_arms["llrs"]["B0"]
        pair_hash = _frame_pair_hash(
            physical=physical,
            bundle=receiver_result["bundle"],
            info_bits=info,
            coded_bits=coded,
        )
        candidates = []
        for scalar in grid:
            decoder_input = float(scalar) * b0
            decoded, decode_receipt = codec.decode_fresh(decoder_input)
            errors = int(np.count_nonzero(decoded != info))
            if not decode_receipt["restart"] or decode_receipt["configured_iterations"] != 20:
                raise RuntimeError("calibration decode was not a fresh 20-iteration call")
            candidates.append(
                {
                    "scalar": float(scalar),
                    "bit_errors": errors,
                    "fer": int(errors > 0),
                    "decoder_input_sha256": _array_sha256(decoder_input),
                }
            )
        raw["frames"].append(
            {
                "frame_index": frame_index,
                "seed": seed,
                "pair_hash": pair_hash,
                "physical": physical["physical_receipt"],
                "realization_hash": receiver_result["bundle"].realization_hash,
                "bundle_hash": receiver_result["bundle"].bundle_hash,
                "mapping_sha256": physical["mapping"]["mapping_receipt"]["mapping_sha256"],
                "estimated_n0_pilot": receiver_arms["estimated_n0_pilot"],
                "b0_clip": receiver_arms["clip"]["B0"],
                "candidates": candidates,
            }
        )
        if write and ((frame_index + 1) % 8 == 0 or frame_index + 1 == len(seeds)):
            from common import save_results

            save_results(raw, str(raw_path), "t077:calibration-checkpoint")
    aggregate = []
    for candidate_index, scalar in enumerate(grid):
        errors = sum(
            int(frame["candidates"][candidate_index]["bit_errors"])
            for frame in raw["frames"]
        )
        frame_errors = sum(
            int(frame["candidates"][candidate_index]["fer"])
            for frame in raw["frames"]
        )
        aggregate.append(
            {
                "scalar": float(scalar),
                "bit_errors": errors,
                "fer": frame_errors,
                "ber_rate": errors / (len(seeds) * 1024),
                "fer_rate": frame_errors / len(seeds),
            }
        )
    selected = select_b1_scalar(aggregate)
    receipt = {
        "schema_version": "t077.c5-0-single-cell.calibration.receipt.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "codec": "TargetApskCodec",
        "live_backend": True,
        "completed_frames": len(raw["frames"]),
        "seeds": seeds,
        "aggregate": aggregate,
        "b1_frozen_scalar": selected["scalar"],
        "selected": selected,
        "tie_break": ["fer", "ber", "abs_log_scalar", "scalar"],
        "scientific_use": "calibration_only",
    }
    if write:
        from common import save_results

        save_results(raw, str(raw_path), "t077:calibration-raw")
        save_results(
            receipt,
            str(HERE / "single_cell_calibration_receipt.json"),
            "t077:calibration-receipt",
        )
    return {"raw": raw, "receipt": receipt}


def run_gate1(*, write: bool = True, resume: bool = True) -> dict[str, Any]:
    """Generate only the frozen 128-frame pilot/payload reliability gate."""
    manifest = load_manifest()
    split = manifest["splits"]["evaluation"]
    seeds = list(
        range(
            split["gate1_seeds"]["start"],
            split["gate1_seeds"]["stop_inclusive"] + 1,
        )
    )
    if len(seeds) != 128 or split["evaluation_frames"] != 512:
        raise RuntimeError("Gate 1/fixed evaluation dimensions do not match manifest")
    calibration_path = HERE / "single_cell_calibration_receipt.json"
    if not calibration_path.exists():
        raise RuntimeError("Gate 1 requires the completed disjoint calibration receipt")
    calibration = json.loads(calibration_path.read_text(encoding="utf-8"))
    if (
        calibration.get("manifest_hash") != manifest_sha256()
        or calibration.get("completed_frames") != 64
    ):
        raise RuntimeError("calibration receipt does not match the frozen manifest")
    b1_scalar = float(calibration["b1_frozen_scalar"])
    raw_path = HERE / "single_cell_evaluation_raw.json"
    raw: dict[str, Any] = {
        "schema_version": "t077.c5-0-single-cell.evaluation.raw.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "codec": "TargetApskCodec",
        "live_backend": True,
        "observation_symbols_per_polarization": 256,
        "fixed_evaluation_frames": 512,
        "gate1_frames": 128,
        "fixed_seeds": [split["fixed_seeds"]["start"], split["fixed_seeds"]["stop_inclusive"]],
        "b1_frozen_scalar": b1_scalar,
        "stage": "gate1_statistics_only",
        "frames": [],
    }
    if resume and raw_path.exists():
        prior = json.loads(raw_path.read_text(encoding="utf-8"))
        prior.pop("_meta", None)
        if (
            prior.get("manifest_hash") != manifest_sha256()
            or prior.get("fixed_evaluation_frames") != 512
            or prior.get("b1_frozen_scalar") != b1_scalar
        ):
            raise RuntimeError("evaluation checkpoint does not match the frozen manifest")
        prior_seeds = [int(frame["seed"]) for frame in prior.get("frames", [])]
        if prior_seeds != seeds[: len(prior_seeds)] or len(prior_seeds) > 128:
            raise RuntimeError("Gate 1 checkpoint is not the frozen seed prefix")
        if any(frame.get("arms") for frame in prior.get("frames", [])):
            raise RuntimeError("Gate 1 checkpoint must not contain decoded arms")
        raw = prior
    codec = _correctness().TargetApskCodec()
    nominal_n0 = 10.0 ** (-manifest["cell"]["snr_db"] / 10.0)
    for frame_index in range(len(raw["frames"]), len(seeds)):
        seed = seeds[frame_index]
        info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
        info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
        coded = np.asarray(codec.encode(info), dtype=np.uint8)
        physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
        receiver_result = run_coded_receiver(physical["receiver"])
        n0_pilot = estimate_receiver_pilot_n0(
            receiver_result["compensated"],
            physical["receiver"].pilot_symbols,
            physical["receiver"].known_mask,
        )
        n0_payload = estimate_scorer_payload_n0(
            receiver_result["compensated"], physical["truth_symbols"]
        )
        pair_hash = _frame_pair_hash(
            physical=physical,
            bundle=receiver_result["bundle"],
            info_bits=info,
            coded_bits=coded,
        )
        raw["frames"].append(
            {
                "frame_index": frame_index,
                "seed": seed,
                "pair_hash": pair_hash,
                "mapping_sha256": physical["mapping"]["mapping_receipt"]["mapping_sha256"],
                "info_bits_sha256": _array_sha256(info),
                "coded_bits_sha256": _array_sha256(coded),
                "physical": physical["physical_receipt"],
                "realization_hash": receiver_result["bundle"].realization_hash,
                "bundle_hash": receiver_result["bundle"].bundle_hash,
                "estimated_n0_pilot": n0_pilot,
                "estimated_n0_payload": n0_payload,
                "b2_scalar": nominal_n0 / n0_pilot,
                "arms": {},
            }
        )
        if write and ((frame_index + 1) % 16 == 0 or frame_index + 1 == len(seeds)):
            from common import save_results

            save_results(raw, str(raw_path), "t077:evaluation-gate1-checkpoint")
    bootstrap = manifest["bootstrap"]
    metrics = gate1_metrics(
        np.array([frame["estimated_n0_pilot"] for frame in raw["frames"]]),
        np.array([frame["estimated_n0_payload"] for frame in raw["frames"]]),
        seed=bootstrap["seed"],
        resamples=bootstrap["resamples"],
    )
    raw["stage"] = "gate1_pass" if metrics["pass"] else "gate1_fail_terminal"
    receipt = {
        "schema_version": "t077.c5-0-single-cell.gate1.receipt.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "completed_frames": len(raw["frames"]),
        "decoded_arms": [],
        "metrics": metrics,
        "gate1": "PASS" if metrics["pass"] else "FAIL",
        "terminal": None if metrics["pass"] else "SINGLE_CELL_NO_RELIABILITY_SIGNAL",
        "next_stage": "append_same_manifest_to_512_and_decode_B0_O1" if metrics["pass"] else None,
    }
    if write:
        from common import save_results

        save_results(raw, str(raw_path), "t077:evaluation-gate1-raw")
        save_results(
            receipt,
            str(HERE / "single_cell_gate1_receipt.json"),
            "t077:gate1-receipt",
        )
    return {"raw": raw, "receipt": receipt}


def _evaluation_statistics_frame(
    codec: Any, *, seed: int, frame_index: int, nominal_n0: float
) -> dict[str, Any]:
    info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
    info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
    coded = np.asarray(codec.encode(info), dtype=np.uint8)
    physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
    receiver_result = run_coded_receiver(physical["receiver"])
    n0_pilot = estimate_receiver_pilot_n0(
        receiver_result["compensated"],
        physical["receiver"].pilot_symbols,
        physical["receiver"].known_mask,
    )
    n0_payload = estimate_scorer_payload_n0(
        receiver_result["compensated"], physical["truth_symbols"]
    )
    pair_hash = _frame_pair_hash(
        physical=physical,
        bundle=receiver_result["bundle"],
        info_bits=info,
        coded_bits=coded,
    )
    return {
        "frame_index": frame_index,
        "seed": seed,
        "pair_hash": pair_hash,
        "mapping_sha256": physical["mapping"]["mapping_receipt"]["mapping_sha256"],
        "info_bits_sha256": _array_sha256(info),
        "coded_bits_sha256": _array_sha256(coded),
        "physical": physical["physical_receipt"],
        "realization_hash": receiver_result["bundle"].realization_hash,
        "bundle_hash": receiver_result["bundle"].bundle_hash,
        "estimated_n0_pilot": n0_pilot,
        "estimated_n0_payload": n0_payload,
        "b2_scalar": nominal_n0 / n0_pilot,
        "arms": {},
    }


def run_gate2(*, write: bool = True, resume: bool = True) -> dict[str, Any]:
    """Append the fixed evaluation to 512 and decode only B0/O1."""
    manifest = load_manifest()
    gate1_path = HERE / "single_cell_gate1_receipt.json"
    raw_path = HERE / "single_cell_evaluation_raw.json"
    if not gate1_path.exists() or not raw_path.exists():
        raise RuntimeError("Gate 2 requires Gate 1 receipt and evaluation raw")
    gate1 = json.loads(gate1_path.read_text(encoding="utf-8"))
    if gate1.get("manifest_hash") != manifest_sha256() or gate1.get("gate1") != "PASS":
        raise RuntimeError("Gate 1 did not open Gate 2")
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    raw.pop("_meta", None)
    if raw.get("manifest_hash") != manifest_sha256() or raw.get("fixed_evaluation_frames") != 512:
        raise RuntimeError("evaluation raw does not match the frozen manifest")
    split = manifest["splits"]["evaluation"]
    seeds = list(
        range(split["fixed_seeds"]["start"], split["fixed_seeds"]["stop_inclusive"] + 1)
    )
    if len(seeds) != 512:
        raise RuntimeError("fixed evaluation must contain exactly 512 frames")
    stored_seeds = [int(frame["seed"]) for frame in raw["frames"]]
    if stored_seeds != seeds[: len(stored_seeds)]:
        raise RuntimeError("evaluation raw is not an append-only frozen seed prefix")
    if len(stored_seeds) < 128:
        raise RuntimeError("Gate 1 raw is incomplete")
    codec = _correctness().TargetApskCodec()
    nominal_n0 = 10.0 ** (-manifest["cell"]["snr_db"] / 10.0)
    for frame_index in range(len(raw["frames"]), len(seeds)):
        raw["frames"].append(
            _evaluation_statistics_frame(
                codec,
                seed=seeds[frame_index],
                frame_index=frame_index,
                nominal_n0=nominal_n0,
            )
        )
        if write and ((frame_index + 1) % 16 == 0 or frame_index + 1 == len(seeds)):
            from common import save_results

            save_results(raw, str(raw_path), "t077:evaluation-append-512-checkpoint")
    raw["stage"] = "fixed_512_statistics"
    decoded_prefix = 0
    for frame in raw["frames"]:
        names = set(frame.get("arms", {}))
        if names == {"B0", "O1"}:
            decoded_prefix += 1
        elif names:
            raise RuntimeError("Gate 2 raw contains an unopened arm")
        else:
            break
    if any(frame.get("arms") for frame in raw["frames"][decoded_prefix:]):
        raise RuntimeError("Gate 2 decoded frames are not an append-only prefix")
    for frame_index in range(decoded_prefix, len(seeds)):
        seed = seeds[frame_index]
        info_rng = np.random.default_rng(np.random.SeedSequence([seed, 77, 5]))
        info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
        coded = np.asarray(codec.encode(info), dtype=np.uint8)
        physical = generate_coded_physical_frame(seed=seed, coded_bits=coded[0])
        receiver_result = run_coded_receiver(physical["receiver"])
        replay_pair_hash = _frame_pair_hash(
            physical=physical,
            bundle=receiver_result["bundle"],
            info_bits=info,
            coded_bits=coded,
        )
        stored = raw["frames"][frame_index]
        replay_checks = {
            "pair_hash": replay_pair_hash == stored["pair_hash"],
            "mapping_sha256": (
                physical["mapping"]["mapping_receipt"]["mapping_sha256"]
                == stored["mapping_sha256"]
            ),
            "received_observation_sha256": (
                physical["physical_receipt"]["received_observation_sha256"]
                == stored["physical"]["received_observation_sha256"]
            ),
            "codeword_sha256": (
                physical["physical_receipt"]["codeword_sha256"]
                == stored["physical"]["codeword_sha256"]
            ),
        }
        if not all(replay_checks.values()):
            raise RuntimeError("INVALID_TESTBED: replay changed a frozen physical frame")
        b0 = build_b0_llr(
            receiver_result["compensated"], nominal_complex_noise_power=nominal_n0
        )
        o1 = build_payload_oracle(
            receiver_result["compensated"], physical["truth_symbols"]
        )
        arms = {}
        for name, result in (("B0", b0), ("O1", o1)):
            decoded, decode_receipt = codec.decode_fresh(result["llr"])
            errors = int(np.count_nonzero(decoded != info))
            if not decode_receipt["restart"] or decode_receipt["configured_iterations"] != 20:
                raise RuntimeError("Gate 2 decode was not a fresh 20-iteration call")
            arms[name] = {
                "pair_hash": replay_pair_hash,
                "decoder_input_sha256": _array_sha256(result["llr"]),
                "bit_errors": errors,
                "fer": int(errors > 0),
                "restart": True,
                "configured_iterations": 20,
                "clip": result["clip"],
            }
        stored["replay_hash_checks"] = replay_checks
        stored["arms"] = arms
        if write and ((frame_index + 1) % 16 == 0 or frame_index + 1 == len(seeds)):
            from common import save_results

            save_results(raw, str(raw_path), "t077:evaluation-B0-O1-checkpoint")
    bootstrap = manifest["bootstrap"]
    decision = gate2_decision(
        np.array([frame["arms"]["B0"]["bit_errors"] for frame in raw["frames"]]),
        np.array([frame["arms"]["B0"]["fer"] for frame in raw["frames"]]),
        np.array([frame["arms"]["O1"]["bit_errors"] for frame in raw["frames"]]),
        np.array([frame["arms"]["O1"]["fer"] for frame in raw["frames"]]),
        seed=bootstrap["seed"],
        resamples=bootstrap["resamples"],
    )
    raw["stage"] = "gate2_pass" if decision["gate2"] == "PASS" else "gate2_terminal"
    receipt = {
        "schema_version": "t077.c5-0-single-cell.gate2.receipt.v1",
        "authority": manifest["authority"],
        "manifest_hash": manifest_sha256(),
        "completed_frames": len(raw["frames"]),
        "decoded_arms": ["B0", "O1"],
        "replayed_gate1_frames": 128,
        "all_replay_hash_checks": all(
            all(frame["replay_hash_checks"].values()) for frame in raw["frames"]
        ),
        "decision": decision,
        "gate2": decision["gate2"],
        "terminal": decision["terminal"],
        "next_stage": "decode_B1_B2_B3" if decision["gate2"] == "PASS" else None,
    }
    if write:
        from common import save_results

        save_results(raw, str(raw_path), "t077:evaluation-gate2-raw")
        save_results(
            receipt,
            str(HERE / "single_cell_gate2_receipt.json"),
            "t077:gate2-receipt",
        )
    return {"raw": raw, "receipt": receipt}


def finalize_terminal_outputs(*, independent_review: dict[str, Any]) -> dict[str, Any]:
    """Assemble the immutable terminal aggregate from completed receipts/raw."""
    paths = {
        "smoke": HERE / "single_cell_smoke_receipt.json",
        "live": HERE / "single_cell_live_point_receipt.json",
        "calibration": HERE / "single_cell_calibration_receipt.json",
        "gate1": HERE / "single_cell_gate1_receipt.json",
        "gate2": HERE / "single_cell_gate2_receipt.json",
        "raw": HERE / "single_cell_evaluation_raw.json",
    }
    data = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()}
    if any(value.get("manifest_hash") != manifest_sha256() for value in data.values()):
        raise RuntimeError("terminal inputs do not share the frozen manifest")
    if data["gate2"].get("terminal") != "SINGLE_CELL_NO_HEADROOM":
        raise RuntimeError("terminal finalizer only accepts the observed frozen terminal")
    frames = data["raw"]["frames"]
    if len(frames) != 512 or any(set(frame["arms"]) != {"B0", "O1"} for frame in frames):
        raise RuntimeError("terminal raw must contain exactly 512 B0/O1-only frames")
    clip = {}
    for arm in ("B0", "O1"):
        values = [frame["arms"][arm]["clip"] for frame in frames]
        totals = {
            key: int(sum(value[key] for value in values))
            for key in ("demapper_clip30", "decode_clip30", "backend_clip20", "total_llrs")
        }
        totals["demapper_clip30_rate"] = totals["demapper_clip30"] / totals["total_llrs"]
        totals["backend_clip20_rate"] = totals["backend_clip20"] / totals["total_llrs"]
        totals["frames_with_demapper_clip30"] = int(
            sum(value["demapper_clip30"] > 0 for value in values)
        )
        clip[arm] = totals
    b2_scalars = np.asarray([frame["b2_scalar"] for frame in frames], dtype=np.float64)
    q25, median, q75 = np.quantile(b2_scalars, [0.25, 0.5, 0.75])
    gate2_decision_data = data["gate2"]["decision"]
    aggregate = {
        "schema_version": "t077.c5-0-single-cell.aggregate.v1",
        "authority": load_manifest()["authority"],
        "manifest_hash": manifest_sha256(),
        "terminal": "SINGLE_CELL_NO_HEADROOM",
        "dimensions": {
            "observation_symbols_per_polarization": 256,
            "evaluation_frames": 512,
        },
        "splits": {
            "smoke": [2900, 2907, 8],
            "calibration": [3000, 3063, 64],
            "gate1": [4000, 4127, 128],
            "evaluation": [4000, 4511, 512],
        },
        "b1_calibration": {
            "frozen_scalar": data["calibration"]["b1_frozen_scalar"],
            "selected": data["calibration"]["selected"],
        },
        "gate1": data["gate1"]["metrics"],
        "gate2": gate2_decision_data,
        "arms": {
            "B0": gate2_decision_data["arms"]["B0"],
            "O1": gate2_decision_data["arms"]["O1"],
            "B1": {"status": "N/A", "reason": "Gate_2_FAIL_not_opened"},
            "B2": {"status": "N/A", "reason": "Gate_2_FAIL_not_opened"},
            "B3": {"status": "N/A", "reason": "Gate_2_FAIL_not_opened"},
        },
        "diagnostics": {
            "clip": clip,
            "b1_scalar": data["calibration"]["b1_frozen_scalar"],
            "b2_scalar_unopened_diagnostic": {
                "min": float(np.min(b2_scalars)),
                "q25": float(q25),
                "median": float(median),
                "q75": float(q75),
                "max": float(np.max(b2_scalars)),
                "mean": float(np.mean(b2_scalars)),
            },
        },
        "identity": {
            "unique_pair_hashes": len({frame["pair_hash"] for frame in frames}),
            "unique_mapping_hashes": len({frame["mapping_sha256"] for frame in frames}),
            "all_replay_hash_checks": all(
                all(frame["replay_hash_checks"].values()) for frame in frames
            ),
            "decoded_arm_sets": sorted({tuple(sorted(frame["arms"])) for frame in frames}),
        },
        "truth_and_live_evidence": {
            "receiver_api_truth_exclusion": data["smoke"]["receiver_api_truth_exclusion"],
            "truth_exclusion_evidence": data["smoke"]["truth_exclusion_evidence"],
            "smoke_codec": data["smoke"]["codec"],
            "smoke_live_backend": data["smoke"]["live_backend"],
            "live_point_fresh_decode": data["live"]["fresh_live_decode"],
        },
        "independent_review": independent_review,
    }
    receipt = {
        "schema_version": "t077.c5-0-single-cell.receipt.v1",
        "authority": load_manifest()["authority"],
        "manifest_hash": manifest_sha256(),
        "terminal": aggregate["terminal"],
        "gate1": data["gate1"]["gate1"],
        "gate2": data["gate2"]["gate2"],
        "gate3": "NOT_OPENED",
        "completed_evaluation_frames": 512,
        "decoded_arms": ["B0", "O1"],
        "unopened_arms": ["B1", "B2", "B3"],
        "all_replay_hash_checks": aggregate["identity"]["all_replay_hash_checks"],
        "independent_review": independent_review,
    }
    from common import save_results

    save_results(aggregate, str(HERE / "single_cell_aggregate.json"), "t077:aggregate")
    save_results(receipt, str(HERE / "single_cell_receipt.json"), "t077:receipt")
    return {"aggregate": aggregate, "receipt": receipt}


def add_raw_audit_pair_receipts() -> dict[str, Any]:
    """Add reviewer-recomputable summary hashes without rerunning any frame."""
    raw_path = HERE / "single_cell_evaluation_raw.json"
    gate2_path = HERE / "single_cell_gate2_receipt.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    raw.pop("_meta", None)
    if raw.get("manifest_hash") != manifest_sha256() or len(raw.get("frames", [])) != 512:
        raise RuntimeError("audit receipt requires the completed frozen evaluation raw")
    for frame in raw["frames"]:
        if frame["mapping_sha256"] != frame["physical"]["mapping_sha256"]:
            raise RuntimeError("raw mapping summaries disagree")
        frame["audit_pair_receipt"] = audit_pair_receipt(
            frame, manifest_hash=raw["manifest_hash"]
        )
    raw["audit_pair_schema"] = {
        "schema_version": "t077.audit-pair.persisted-summaries.v1",
        "field_order": list(AUDIT_PAIR_FIELD_ORDER),
        "scope": "persisted_summary_integrity_not_underlying_array_reconstruction",
    }
    unique = len(
        {frame["audit_pair_receipt"]["audit_pair_sha256"] for frame in raw["frames"]}
    )
    gate2 = json.loads(gate2_path.read_text(encoding="utf-8"))
    gate2.pop("_meta", None)
    gate2["audit_pair_receipts"] = {
        "frames": len(raw["frames"]),
        "unique_hashes": unique,
        "field_order": list(AUDIT_PAIR_FIELD_ORDER),
        "raw_only_recomputable": True,
        "scope": "persisted_summary_integrity_not_underlying_array_reconstruction",
    }
    from common import save_results

    save_results(raw, str(raw_path), "t077:evaluation-raw-audit-pair-receipts")
    save_results(gate2, str(gate2_path), "t077:gate2-receipt-audit-pair")
    return gate2["audit_pair_receipts"]


__all__ = [
    "MANIFEST_PATH",
    "NONPILOT_INDICES",
    "PILOT_INDICES",
    "build_dp_symbol_frame",
    "build_b0_llr",
    "b1_scalar_grid",
    "audit_pair_receipt",
    "AUDIT_PAIR_FIELD_ORDER",
    "build_payload_oracle",
    "build_receiver_arms",
    "estimate_receiver_pilot_n0",
    "estimate_scorer_payload_n0",
    "finalize_terminal_outputs",
    "add_raw_audit_pair_receipts",
    "extract_coded_bits",
    "generate_coded_physical_frame",
    "load_manifest",
    "manifest_sha256",
    "run_coded_receiver",
    "run_correctness_smoke",
    "run_b1_calibration",
    "run_gate1",
    "run_gate2",
    "run_live_integration_point_check",
    "select_b1_scalar",
]
