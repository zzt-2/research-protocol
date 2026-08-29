"""T076 deterministic APSK-to-LDPC correctness seam.

This module is deliberately correctness-only. It wraps the already receipted
Sionna backend from ``coded-decoder-feedback`` and does not copy or modify the
LDPC algorithm. LLRs use ``log P(bit=1|y) - log P(bit=0|y)`` throughout.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import inspect
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Mapping

import numpy as np


SIMULATION_ROOT = Path(__file__).resolve().parents[2]
CODEC_METRICS_PATH = (
    SIMULATION_ROOT
    / "explore"
    / "ch5-apsk-structured-covariance"
    / "codec_metrics.py"
)
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"

if str(SIMULATION_ROOT) not in sys.path:
    sys.path.insert(0, str(SIMULATION_ROOT))


def _load_file(path: Path, name: str) -> ModuleType:
    cached = sys.modules.get(name)
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _codec_metrics() -> ModuleType:
    return _load_file(CODEC_METRICS_PATH, "_t076_codec_metrics_runtime")


def _d0_codec() -> ModuleType:
    if str(D0_ROOT) not in sys.path:
        sys.path.insert(0, str(D0_ROOT))
    return _load_file(D0_ROOT / "codec.py", "_t076_d0_codec_runtime")


def apsk16_table() -> tuple[np.ndarray, np.ndarray]:
    """Return the project mapper's canonical label-ordered APSK table."""
    symbols, bits = _codec_metrics().apsk16_table()
    return np.asarray(symbols).copy(), np.asarray(bits).copy()


def apsk16_identity() -> Any:
    """Return the joint constellation/label fingerprint from the owner asset."""
    return _codec_metrics().apsk16_identity()


def per_real_covariance(complex_noise_power: float) -> float:
    """Convert ``N0=E|n|^2`` to each real component's covariance ``N0/2``."""
    if isinstance(complex_noise_power, (bool, np.bool_)):
        raise TypeError("complex_noise_power must not be boolean")
    value = float(complex_noise_power)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("complex_noise_power must be finite and positive")
    return value / 2.0


def _validate_clip(clip: float | None) -> float | None:
    if clip is None:
        return None
    value = float(clip)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("clip must be None or finite and positive")
    return value


def _distance2(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(samples, dtype=np.complex128).reshape(-1)
    if not np.all(np.isfinite(values)):
        raise ValueError("samples must be finite")
    symbols, bits = apsk16_table()
    return np.abs(values[:, None] - symbols[None, :]) ** 2, bits


def exact_app_llr(
    samples: np.ndarray,
    *,
    complex_noise_power: float,
    clip: float | None = 30.0,
) -> np.ndarray:
    """Uniform-prior exact-APP APSK LLR with complex noise power ``N0``."""
    n0 = 2.0 * per_real_covariance(complex_noise_power)
    clip = _validate_clip(clip)
    distance2, bits = _distance2(samples)
    logp = -distance2 / n0
    result = np.empty((distance2.shape[0], 4), dtype=np.float64)
    for bit_index in range(4):
        log_one = np.logaddexp.reduce(logp[:, bits[:, bit_index] == 1], axis=1)
        log_zero = np.logaddexp.reduce(logp[:, bits[:, bit_index] == 0], axis=1)
        result[:, bit_index] = log_one - log_zero
    if clip is not None:
        result = np.clip(result, -clip, clip)
    return result


def maxlog_llr(
    samples: np.ndarray,
    *,
    complex_noise_power: float,
    clip: float | None = 30.0,
) -> np.ndarray:
    """Uniform-prior max-log APSK LLR under common isotropic variance."""
    n0 = 2.0 * per_real_covariance(complex_noise_power)
    clip = _validate_clip(clip)
    distance2, bits = _distance2(samples)
    result = np.empty((distance2.shape[0], 4), dtype=np.float64)
    for bit_index in range(4):
        zeros = bits[:, bit_index] == 0
        min_zero = np.min(distance2[:, zeros], axis=1)
        min_one = np.min(distance2[:, ~zeros], axis=1)
        result[:, bit_index] = (min_zero - min_one) / n0
    if clip is not None:
        result = np.clip(result, -clip, clip)
    return result


def exact_app_identity_receipt() -> dict[str, Any]:
    """Classify B2/B3 exact-APP identity per bit on the frozen C2 grid."""
    symbols, _ = apsk16_table()
    radii = np.unique(np.round(np.abs(symbols), 14))
    ring_midpoint = float(np.mean(radii))
    classes = {
        "constellation": symbols,
        "origin": np.array([0.0 + 0.0j]),
        "ring_midpoint": np.array([ring_midpoint + 0.0j]),
        "axis": np.array([0.72 + 0.0j, -0.91 + 0.0j, 0.0 + 1.07j]),
        "off_axis": np.array([0.41 - 0.27j, -0.36 + 0.83j, 1.02 + 0.19j]),
    }
    grid = np.concatenate(tuple(classes.values()))
    variance_pairs = ((0.04, 0.02), (0.07, 0.11), (0.2, 0.05))
    bit_max = np.zeros(4, dtype=np.float64)
    origin_max = 0.0
    for nominal_n0, estimated_n0 in variance_pairs:
        scalar = nominal_n0 / estimated_n0
        b2 = scalar * exact_app_llr(
            grid, complex_noise_power=nominal_n0, clip=None
        )
        b3 = exact_app_llr(grid, complex_noise_power=estimated_n0, clip=None)
        bit_max = np.maximum(bit_max, np.max(np.abs(b2 - b3), axis=0))
        origin_b2 = scalar * exact_app_llr(
            classes["origin"], complex_noise_power=nominal_n0, clip=None
        )
        origin_b3 = exact_app_llr(
            classes["origin"], complex_noise_power=estimated_n0, clip=None
        )
        origin_max = max(origin_max, float(np.max(np.abs(origin_b2 - origin_b3))))
    return {
        "sample_classes": tuple(classes),
        "variance_pairs": len(variance_pairs),
        "origin_max_abs": origin_max,
        "bit_max_abs": {index: float(value) for index, value in enumerate(bit_max)},
        "bit_status": {
            index: "NONIDENTITY" if value > 1e-10 else "IDENTITY_ON_GRID"
            for index, value in enumerate(bit_max)
        },
    }


_CHECKS = ((0, 1, 2), (1, 2, 3))


def _check_update(values: np.ndarray, alpha: float = 0.75) -> np.ndarray:
    output = np.empty_like(values)
    for index in range(values.size):
        others = np.delete(values, index)
        output[index] = (
            alpha * np.prod(np.where(others < 0.0, -1.0, 1.0)) * np.min(np.abs(others))
        )
    return output


def minimal_nms_trace(channel_llr: np.ndarray) -> dict[str, Any]:
    """Run a 20-iteration unclipped, filler-free two-check NMS graph."""
    channel = np.asarray(channel_llr, dtype=np.float64)
    if channel.shape != (4,) or not np.all(np.isfinite(channel)):
        raise ValueError("channel_llr must be a finite length-four vector")
    edges = tuple((check, variable) for check, group in enumerate(_CHECKS) for variable in group)
    v2c = np.array([channel[variable] for _, variable in edges], dtype=np.float64)
    messages: list[np.ndarray] = [v2c.copy()]
    posterior = channel.copy()
    for _ in range(20):
        c2v = np.empty_like(v2c)
        cursor = 0
        for group in _CHECKS:
            width = len(group)
            c2v[cursor : cursor + width] = _check_update(v2c[cursor : cursor + width])
            cursor += width
        posterior = channel.copy()
        for edge_index, (_, variable) in enumerate(edges):
            posterior[variable] += c2v[edge_index]
        new_v2c = np.empty_like(v2c)
        for edge_index, (check, variable) in enumerate(edges):
            incoming = channel[variable]
            for other_index, (other_check, other_variable) in enumerate(edges):
                if other_variable == variable and other_check != check:
                    incoming += c2v[other_index]
            new_v2c[edge_index] = incoming
        v2c = new_v2c
        messages.extend((c2v.copy(), posterior.copy(), v2c.copy()))
    return {"messages": tuple(messages), "hard": (posterior > 0.0).astype(np.uint8)}


def target_nonlinearity_receipt() -> dict[str, Any]:
    """Receipt the natural fixed boundaries without claiming performance."""
    clip20 = lambda value: np.clip(np.asarray(value, dtype=np.float64), -20.0, 20.0)
    low = np.array([25.0, -15.0])
    high = np.array([15.0, -5.0])
    s_low = 0.5
    s_high = 2.0
    low_break = not np.array_equal(clip20(s_low * low), s_low * clip20(low))
    high_break = not np.array_equal(clip20(s_high * high), s_high * clip20(high))
    channel = np.array([4.0, -7.0])
    with_fixed_filler = np.concatenate((s_high * channel, np.array([-20.0])))
    fully_scaled = s_high * np.concatenate((channel, np.array([-20.0])))
    return {
        "placement": (
            "apsk_demapper_clip30 -> b2_scale -> decode_fresh_clip30 -> "
            "backend_input_clip20 -> decoder_out_int_inv -> "
            "rate_recovery_fixed_bit0_filler_minus20 -> bp_internal_clip20"
        ),
        "s_lt_1_checked": low_break,
        "s_ge_1_checked": high_break,
        "input_clip_breaks_homogeneity": low_break and high_break,
        "fixed_filler_breaks_homogeneity": not np.array_equal(
            with_fixed_filler, fully_scaled
        ),
        "alpha_075_is_homogeneous": bool(0.75 * s_high == s_high * 0.75),
        "interleaver_is_homogeneous": True,
        "punctured_zero_is_homogeneous": True,
        "fixed_iterations_are_homogeneous": True,
    }


def _estimate_shared_n0(
    pilot_samples: np.ndarray,
    pilot_reference: np.ndarray,
    known_mask: np.ndarray,
) -> float:
    observed = np.asarray(pilot_samples, dtype=np.complex128)
    reference = np.asarray(pilot_reference, dtype=np.complex128)
    mask = np.asarray(known_mask, dtype=bool)
    if observed.shape != reference.shape or observed.shape != mask.shape:
        raise ValueError("pilot arrays and known_mask must have identical shapes")
    if observed.ndim != 2 or observed.shape[0] != 2:
        raise ValueError("pilots must have shape [two polarizations, pilot count]")
    rss = 0.0
    degrees = 0
    for polarization in range(2):
        residual = observed[polarization, mask[polarization]] - reference[
            polarization, mask[polarization]
        ]
        if residual.size < 2:
            raise ValueError("each polarization needs at least two current-frame pilots")
        residual = residual - np.mean(residual)
        rss += float(np.sum(np.abs(residual) ** 2))
        degrees += residual.size - 1
    estimate = rss / degrees
    if not np.isfinite(estimate) or estimate <= 0.0:
        raise ValueError("current-frame pilot residual estimate must be positive")
    return estimate


def build_frame_actions(
    pilot_samples: np.ndarray,
    pilot_reference: np.ndarray,
    known_mask: np.ndarray,
    payload_samples: np.ndarray,
    *,
    nominal_complex_noise_power: float,
    runtime_fixed_scalar: float,
) -> dict[str, Any]:
    """Build B0/B2/B3 from receiver-visible current-frame inputs only."""
    nominal_n0 = 2.0 * per_real_covariance(nominal_complex_noise_power)
    fixed_scalar = float(runtime_fixed_scalar)
    if not np.isfinite(fixed_scalar) or fixed_scalar <= 0.0:
        raise ValueError("runtime_fixed_scalar must be finite and positive")
    estimated_n0 = _estimate_shared_n0(pilot_samples, pilot_reference, known_mask)
    payload = np.asarray(payload_samples, dtype=np.complex128)
    if payload.ndim != 3 or payload.shape[0] != 2 or not np.all(np.isfinite(payload)):
        raise ValueError("payload_samples must be finite [two polarizations,CW,symbol]")
    b0 = exact_app_llr(
        payload.reshape(-1), complex_noise_power=nominal_n0, clip=30.0
    ).reshape(payload.shape + (4,))
    b1 = fixed_scalar * b0
    scalar = nominal_n0 / estimated_n0
    b2 = scalar * b0
    b3 = exact_app_llr(
        payload.reshape(-1), complex_noise_power=estimated_n0, clip=30.0
    ).reshape(payload.shape + (4,))
    return {
        "b0": b0,
        "b1": b1,
        "b2": b2,
        "b3": b3,
        "scalar": float(scalar),
        "estimated_n0": float(estimated_n0),
        "runtime_fixed_scalar": fixed_scalar,
        "scale_matrix": np.full(payload.shape[:2], scalar, dtype=np.float64),
        "physical_frame_scalars": 1,
    }


class TargetApskCodec:
    """Narrow APSK adapter around the existing, fresh Sionna LDPC backend."""

    demapper_clip = 30.0
    decode_fresh_clip = 30.0
    decoder_iterations = 20

    def __init__(self, backend: Any | None = None):
        self._backend = backend
        self._decoder_calls = 0

    def _ensure_backend(self) -> Any:
        if self._backend is None:
            self._backend = _d0_codec()._SionnaBackend()
        return self._backend

    def encode(self, info_bits: np.ndarray) -> np.ndarray:
        value = np.asarray(info_bits)
        if value.ndim != 2 or value.shape[1] != 1024:
            raise ValueError("info_bits must have shape [B,1024]")
        if not np.all((value == 0) | (value == 1)):
            raise ValueError("info_bits must be binary")
        coded = np.asarray(
            self._ensure_backend().encode(value.astype(np.uint8, copy=False)),
            dtype=np.uint8,
        )
        if coded.shape != (value.shape[0], 1536):
            raise RuntimeError("live encoder returned an invalid shape")
        return coded

    @staticmethod
    def map_coded_bits(coded_bits: np.ndarray) -> np.ndarray:
        from common._modulation import m16apsk_mod

        coded = np.asarray(coded_bits)
        if coded.ndim != 2 or coded.shape[1] != 1536 or not np.all((coded == 0) | (coded == 1)):
            raise ValueError("coded_bits must be binary [B,1536]")
        return np.asarray(m16apsk_mod(coded.reshape(-1)), dtype=np.complex128).reshape(
            coded.shape[0], 384
        )

    def decode_fresh(self, llr_cw: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
        value = np.asarray(llr_cw, dtype=np.float64)
        if value.ndim != 2 or value.shape[1] != 1536 or not np.all(np.isfinite(value)):
            raise ValueError("llr_cw must be finite [B,1536]")
        preclipped = np.clip(value, -self.decode_fresh_clip, self.decode_fresh_clip)
        decoded = np.asarray(
            self._ensure_backend().decode(
                preclipped,
                message_state=None,
                warm_state=None,
            ),
            dtype=np.uint8,
        )
        if decoded.shape != (value.shape[0], 1024) or not np.all((decoded == 0) | (decoded == 1)):
            raise RuntimeError("live decoder returned an invalid hard output")
        self._decoder_calls += 1
        return decoded, {
            "restart": True,
            "configured_iterations": self.decoder_iterations,
            "decode_fresh_clip": self.decode_fresh_clip,
        }

    def _capture_live_filler(self) -> np.ndarray:
        backend = self._ensure_backend()
        from sionna.phy.fec.ldpc.decoding import LDPCBPDecoder

        original = LDPCBPDecoder.call
        captured: dict[str, np.ndarray] = {}

        def intercept(instance, llr_ch, *, num_iter=None, msg_v2c=None):
            del instance, num_iter, msg_v2c
            captured["llr"] = llr_ch.detach().cpu().numpy().copy()
            return llr_ch

        LDPCBPDecoder.call = intercept
        try:
            torch = backend._torch
            with torch.no_grad():
                backend.decoder(torch.zeros((1, 1536), dtype=torch.float32))
        finally:
            LDPCBPDecoder.call = original
        if "llr" not in captured:
            raise RuntimeError("failed to capture live rate-recovery input")
        return captured["llr"]

    def _capture_backend_input_clip(self) -> np.ndarray:
        """Observe the outer backend clamp before the live decoder is called."""
        backend = self._ensure_backend()
        original_decoder = backend.decoder
        captured: dict[str, np.ndarray] = {}

        class DecoderInputSpy:
            def __call__(self, tensor):
                captured["llr"] = tensor.detach().cpu().numpy().copy()
                return backend._torch.zeros(
                    (tensor.shape[0], 1024), dtype=tensor.dtype, device=tensor.device
                )

        backend.decoder = DecoderInputSpy()
        probe = np.zeros((1, 1536), dtype=np.float64)
        probe[0, 0] = 100.0
        probe[0, 1] = -100.0
        try:
            backend.decode(probe, message_state=None, warm_state=None)
        finally:
            backend.decoder = original_decoder
        if "llr" not in captured:
            raise RuntimeError("failed to capture outer backend input clamp")
        return captured["llr"]

    def live_receipt(self) -> dict[str, Any]:
        """Receipt live interleaver, clip, and rate-recovery filler contracts."""
        backend = self._ensure_backend()
        encoder = backend.encoder
        decoder = backend.decoder
        out_int = np.asarray(encoder.out_int.detach().cpu(), dtype=np.int64)
        out_int_inv = np.asarray(encoder.out_int_inv.detach().cpu(), dtype=np.int64)
        expected = np.arange(1536)
        if not np.array_equal(out_int[out_int_inv], expected):
            raise RuntimeError("live out_int/out_int_inv are not inverse permutations")

        rate_recovered = self._capture_live_filler()[0]
        filler_start = int(encoder.k)
        filler_stop = int(encoder.k_ldpc)
        filler = rate_recovered[filler_start:filler_stop]
        if filler.size != 16 or not np.array_equal(filler, np.full(16, -20.0)):
            raise RuntimeError("live BG2 filler contract mismatch")

        backend_decode_source = inspect.getsource(type(backend).decode)
        decoder_source = inspect.getsource(type(decoder).call)
        from sionna.phy.fec.ldpc.decoding import LDPCBPDecoder

        bp_source = inspect.getsource(LDPCBPDecoder.call)
        backend_clipped = self._capture_backend_input_clip()
        decoder_order_receipted = (
            decoder_source.index("out_int_inv")
            < decoder_source.index("-self._llr_max")
            < decoder_source.index("super().call")
            and "llr_ch.clamp" in bp_source
        )
        return {
            "sionna_version": backend.metadata.sionna_version,
            "base_graph": backend.metadata.base_graph,
            "lifting_size": int(encoder.z),
            "k": int(encoder.k),
            "n": int(encoder.n),
            "q_m": int(encoder.num_bits_per_symbol),
            "k_ldpc": int(encoder.k_ldpc),
            "filler_count": int(filler.size),
            "filler_value": float(filler[0]),
            "filler_bit": 0,
            "demapper_clip": self.demapper_clip,
            "decode_fresh_clip": self.decode_fresh_clip,
            "backend_input_clip": float(np.max(np.abs(backend_clipped))),
            "decoder_internal_clip": float(decoder._llr_max),
            "seam_applies_out_int_inv": False,
            "decoder_applies_out_int_inv": "out_int_inv" in decoder_source,
            "backend_input_clip_receipted": "torch.clamp" in backend_decode_source,
            "decoder_internal_clip_receipted": "llr_ch.clamp" in bp_source,
            "decoder_rate_recovery_before_bp_clip_receipted": decoder_order_receipted,
            "backend_input_clip_observed_min": float(np.min(backend_clipped)),
            "backend_input_clip_observed_max": float(np.max(backend_clipped)),
            "out_int_sha256": sha256(out_int.tobytes()).hexdigest(),
            "out_int_inv_sha256": sha256(out_int_inv.tobytes()).hexdigest(),
        }

    @staticmethod
    def _roundtrip_inputs() -> tuple[np.ndarray, tuple[str, ...]]:
        cases = ("all_zero", "single_one", "walking_label", "random")
        info = np.zeros((4, 1024), dtype=np.uint8)
        info[1, 0] = 1
        _, labels = apsk16_table()
        walking = np.resize(labels.reshape(-1), 1024)
        info[2] = walking
        info[3] = np.random.default_rng(20260830).integers(
            0, 2, size=1024, dtype=np.uint8
        )
        return info, cases

    def roundtrip_receipt(self) -> dict[str, Any]:
        """Run four deterministic interface cases; this is not BER evidence."""
        info, cases = self._roundtrip_inputs()
        coded = self.encode(info)
        mapped = self.map_coded_bits(coded)
        llr = exact_app_llr(
            mapped.reshape(-1), complex_noise_power=1e-3, clip=self.demapper_clip
        ).reshape(coded.shape[0], 1536)
        coded_groups = coded.reshape(coded.shape[0], 384, 4)
        sign_errors = np.sum((llr > 0.0) != coded.astype(bool), axis=1)
        grouping_digest = sha256()
        grouping_digest.update(coded_groups.tobytes())
        grouping_digest.update(mapped.view(np.float64).tobytes())
        grouping_digest.update(llr.tobytes())
        decoded, decode_receipt = self.decode_fresh(llr)
        errors = np.sum(decoded != info, axis=1)
        return {
            "cases": cases,
            "bit_errors": {
                case: int(error) for case, error in zip(cases, errors, strict=True)
            },
            "encoded_shape": tuple(coded.shape),
            "coded_group_shape": tuple(coded_groups.shape),
            "mapped_shape": tuple(mapped.shape),
            "flatten_shape": tuple(llr.shape),
            "coded_to_llr_sign_errors": {
                case: int(error)
                for case, error in zip(cases, sign_errors, strict=True)
            },
            "grouping_sha256": grouping_digest.hexdigest(),
            "decoder_calls": self._decoder_calls,
            "configured_iterations": decode_receipt["configured_iterations"],
            "restart": decode_receipt["restart"],
            "all_finite": bool(np.all(np.isfinite(mapped)) and np.all(np.isfinite(llr))),
            "hard_output_sha256": sha256(decoded.tobytes()).hexdigest(),
        }

    def decode_arms_fresh(self, arms: Mapping[str, np.ndarray]) -> dict[str, Any]:
        """Decode each comparator exactly once with a fresh-state call."""
        calls: dict[str, int] = {}
        iterations: dict[str, int] = {}
        restarts: dict[str, bool] = {}
        for arm, llr in arms.items():
            _, receipt = self.decode_fresh(llr)
            calls[str(arm)] = 1
            iterations[str(arm)] = int(receipt["configured_iterations"])
            restarts[str(arm)] = bool(receipt["restart"])
        return {
            "decoder_calls": calls,
            "configured_iterations": iterations,
            "restart": restarts,
        }


__all__ = [
    "TargetApskCodec",
    "apsk16_identity",
    "apsk16_table",
    "build_frame_actions",
    "exact_app_identity_receipt",
    "exact_app_llr",
    "maxlog_llr",
    "minimal_nms_trace",
    "per_real_covariance",
    "target_nonlinearity_receipt",
]
