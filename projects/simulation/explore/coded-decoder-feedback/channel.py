"""Deterministic D0 physical channel and receiver/truth split.

The channel consumes a supplied dual-polarization waveform.  It owns six
independent SeedSequence/PCG64 streams, a shared Gamma-Gamma intensity and
Wiener phase process, and independent polarization AWGN.  Import is pure.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from functools import lru_cache
import math
from typing import Any, Mapping

import numpy as np
from scipy.special import gammaincinv, ndtr

from contract import (
    D0Contract,
    PayloadTruth,
    PhysicalCell,
    ReceiverView,
    TruthView,
    WaveformLayout,
    assert_action_authorized,
    assert_frozen_d0_identity,
    finalize_truth_view,
)
from codec import D0Codec, gray16_map
import receiver as receiver_module
from waveform import WaveformBuild


STREAM_NAMES = (
    "payload_x",
    "payload_y",
    "gamma_gamma",
    "wiener",
    "awgn_x",
    "awgn_y",
)


class ChannelError(ValueError):
    """Raised when the frozen D0 physical contract is violated."""


def _readonly(value: np.ndarray, *, dtype: np.dtype | type | None = None) -> np.ndarray:
    result = np.array(value, dtype=dtype, order="C", copy=True)
    result.setflags(write=False)
    return result


def _positive_finite(value: Any, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be a finite positive number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a finite positive number") from exc
    if not math.isfinite(result) or result <= 0.0:
        raise ChannelError(f"{name} must be a finite positive number")
    return result


@dataclass(frozen=True, slots=True)
class SeedChildReceipt:
    name: str
    root_entropy: int
    numpy_version: str
    child_spawn_key: tuple[int, ...]
    pool_size: int
    child_generate_state_4_uint32: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class NamedStreams:
    root_seed: int
    names: tuple[str, ...]
    receipts: tuple[SeedChildReceipt, ...]
    payload_x: np.random.Generator
    payload_y: np.random.Generator
    gamma_gamma: np.random.Generator
    wiener: np.random.Generator
    awgn_x: np.random.Generator
    awgn_y: np.random.Generator


def _exact_root_seed(root_seed: Any) -> int:
    if type(root_seed) is not int:
        raise TypeError("root_seed must be an exact Python integer")
    if root_seed < 0 or root_seed > 2**63 - 1:
        raise ChannelError("root_seed must fit non-negative int64")
    return root_seed


def spawn_named_streams(root_seed: int) -> NamedStreams:
    """Spawn the six owner-named, consumption-isolated PCG64 streams."""

    root_seed = _exact_root_seed(root_seed)
    root = np.random.SeedSequence(root_seed)
    children = root.spawn(len(STREAM_NAMES))
    receipts = tuple(
        SeedChildReceipt(
            name=name,
            root_entropy=root_seed,
            numpy_version=np.__version__,
            child_spawn_key=tuple(int(item) for item in child.spawn_key),
            pool_size=int(child.pool_size),
            child_generate_state_4_uint32=tuple(
                int(item) for item in child.generate_state(4, dtype=np.uint32)
            ),
        )
        for name, child in zip(STREAM_NAMES, children, strict=True)
    )
    generators = tuple(np.random.Generator(np.random.PCG64(child)) for child in children)
    return NamedStreams(root_seed, STREAM_NAMES, receipts, *generators)


def gamma_gamma_tau_c(f_g_hz: float) -> float:
    return 1.0 / (2.0 * math.pi * _positive_finite(f_g_hz, "f_g_hz"))


def gamma_gamma_rho(
    block_symbols: int, symbol_period_s: float, tau_c_s: float
) -> float:
    if not isinstance(block_symbols, (int, np.integer)) or isinstance(
        block_symbols, (bool, np.bool_)
    ) or int(block_symbols) <= 0:
        raise ChannelError("block_symbols must be a positive integer")
    period = _positive_finite(symbol_period_s, "symbol_period_s")
    tau = _positive_finite(tau_c_s, "tau_c_s")
    return float(np.exp(-int(block_symbols) * period / tau))


def wiener_innovation_variance(
    linewidth_hz: float, symbol_period_s: float
) -> float:
    return float(
        2.0
        * math.pi
        * _positive_finite(linewidth_hz, "linewidth_hz")
        * _positive_finite(symbol_period_s, "symbol_period_s")
    )


def awgn_variances(snr_db: float) -> tuple[float, float]:
    if isinstance(snr_db, (bool, np.bool_)):
        raise TypeError("snr_db must be finite")
    try:
        snr = float(snr_db)
    except (TypeError, ValueError) as exc:
        raise TypeError("snr_db must be finite") from exc
    if not math.isfinite(snr):
        raise ChannelError("snr_db must be finite")
    gamma = 10.0 ** (snr / 10.0)
    return float(1.0 / (2.0 * gamma)), float(1.0 / gamma)


def generate_wiener_phase(
    length: int,
    *,
    rng: np.random.Generator,
    linewidth_hz: float,
    symbol_period_s: float,
) -> np.ndarray:
    if not isinstance(length, (int, np.integer)) or isinstance(
        length, (bool, np.bool_)
    ) or int(length) <= 0:
        raise ChannelError("length must be a positive integer")
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be numpy.random.Generator")
    variance = wiener_innovation_variance(linewidth_hz, symbol_period_s)
    innovations = rng.standard_normal(int(length)) * math.sqrt(variance)
    return _readonly(np.cumsum(innovations, dtype=np.float64), dtype=np.float64)


def _gamma_ar1_exact(
    n_blocks: int, shape: float, rho: float, rng: np.random.Generator
) -> np.ndarray:
    z0 = rng.standard_normal()
    innovations = math.sqrt(max(0.0, 1.0 - rho * rho)) * rng.standard_normal(
        n_blocks
    )
    z = np.empty(n_blocks, dtype=np.float64)
    current = z0
    for index in range(n_blocks):
        current = rho * current + innovations[index]
        z[index] = current
    probabilities = np.clip(ndtr(z), np.finfo(np.float64).tiny, 1.0 - np.finfo(np.float64).eps)
    return gammaincinv(shape, probabilities) / shape


def _gamma_gamma_intensity(
    length: int,
    *,
    rng: np.random.Generator,
    alpha: float,
    beta: float,
    rho: float,
    block_symbols: int,
) -> np.ndarray:
    n_blocks = (length + block_symbols - 1) // block_symbols
    large = _gamma_ar1_exact(n_blocks, alpha, rho, rng)
    small = _gamma_ar1_exact(n_blocks, beta, rho, rng)
    return np.repeat(large * small, block_symbols)[:length]


@dataclass(frozen=True, slots=True)
class PhysicalRealization:
    received: np.ndarray
    intensity: np.ndarray
    field_fade: np.ndarray
    phase: np.ndarray
    noise: np.ndarray
    per_real_noise_variance: float
    complex_noise_power: float
    tau_c_s: float
    rho_block: float
    innovation_variance: float

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, np.ndarray):
                object.__setattr__(self, field.name, _readonly(value))


def realize_supplied_waveform(
    supplied_waveform: np.ndarray,
    *,
    streams: NamedStreams,
    snr_db: float,
    linewidth_hz: float,
    symbol_rate_baud: float = 2.5e9,
    alpha: float = 1.0,
    beta: float = 0.7,
    f_g_hz: float = 100.0,
    block_symbols: int = 100,
) -> PhysicalRealization:
    samples = np.asarray(supplied_waveform)
    if samples.ndim != 2 or samples.shape[0] != 2 or samples.shape[1] <= 0:
        raise ChannelError("supplied_waveform must have shape (2, positive length)")
    if not np.issubdtype(samples.dtype, np.number) or not np.all(np.isfinite(samples)):
        raise ChannelError("supplied_waveform must contain finite numeric samples")
    if not isinstance(streams, NamedStreams):
        raise TypeError("streams must be NamedStreams")
    if not isinstance(block_symbols, (int, np.integer)) or isinstance(
        block_symbols, (bool, np.bool_)
    ) or int(block_symbols) <= 0:
        raise ChannelError("block_symbols must be a positive integer")
    alpha = _positive_finite(alpha, "alpha")
    beta = _positive_finite(beta, "beta")
    symbol_period = 1.0 / _positive_finite(symbol_rate_baud, "symbol_rate_baud")
    tau = gamma_gamma_tau_c(f_g_hz)
    rho = gamma_gamma_rho(int(block_symbols), symbol_period, tau)
    variance = wiener_innovation_variance(linewidth_hz, symbol_period)
    per_real, complex_power = awgn_variances(snr_db)
    length = samples.shape[1]
    intensity_1d = _gamma_gamma_intensity(
        length,
        rng=streams.gamma_gamma,
        alpha=alpha,
        beta=beta,
        rho=rho,
        block_symbols=int(block_symbols),
    )
    field_1d = np.sqrt(intensity_1d)
    phase_1d = generate_wiener_phase(
        length,
        rng=streams.wiener,
        linewidth_hz=linewidth_hz,
        symbol_period_s=symbol_period,
    )
    intensity = np.vstack((intensity_1d, intensity_1d))
    field_fade = np.vstack((field_1d, field_1d))
    phase = np.vstack((phase_1d, phase_1d))
    noise = math.sqrt(per_real) * np.vstack(
        (
            streams.awgn_x.standard_normal(length)
            + 1j * streams.awgn_x.standard_normal(length),
            streams.awgn_y.standard_normal(length)
            + 1j * streams.awgn_y.standard_normal(length),
        )
    )
    received = field_fade * np.asarray(samples, dtype=np.complex128) * np.exp(
        1j * phase
    ) + noise
    return PhysicalRealization(
        received=received,
        intensity=intensity,
        field_fade=field_fade,
        phase=phase,
        noise=noise,
        per_real_noise_variance=per_real,
        complex_noise_power=complex_power,
        tau_c_s=tau,
        rho_block=rho,
        innovation_variance=variance,
    )


def _event_label(event_fixture: Any) -> str:
    if event_fixture is None:
        return "none"
    if isinstance(event_fixture, str) and event_fixture:
        return event_fixture
    if isinstance(event_fixture, Mapping):
        label = event_fixture.get("label")
        if isinstance(label, str) and label:
            return label
    raise ChannelError("event_fixture must be None, a label, or a mapping with label")


@lru_cache(maxsize=1)
def _canonical_codec(contract: D0Contract) -> D0Codec:
    return D0Codec(contract)


def _assert_payload_waveform_binding(
    contract: D0Contract, payload_truth: PayloadTruth, waveform: WaveformBuild
) -> None:
    encoder_input = np.array(
        payload_truth.information_bits.reshape(32, 1024),
        dtype=np.uint8,
        order="C",
        copy=True,
    )
    encoded = _canonical_codec(contract).encode(encoder_input).reshape(2, 16, 1536)
    if not np.array_equal(encoded, payload_truth.coded_bits):
        raise ChannelError("payload coded bits do not match canonical codec encode")
    expected_data = gray16_map(payload_truth.coded_bits.reshape(2, 6144, 4))
    actual_data = waveform.waveform[:, waveform.data_to_time]
    if not np.array_equal(expected_data, actual_data):
        raise ChannelError("coded bits do not match supplied waveform data positions")


def build_views(
    contract: D0Contract,
    waveform: WaveformBuild,
    *,
    root_seed: int,
    physical_cell: PhysicalCell,
    payload_truth: PayloadTruth,
    event_fixture: Any = None,
) -> tuple[ReceiverView, TruthView]:
    """Build disjoint immutable receiver and evaluator truth views."""

    root_seed = _exact_root_seed(root_seed)
    assert_action_authorized("D0_TESTBED_IMPLEMENTATION", contract)
    assert_frozen_d0_identity(contract)
    if not isinstance(waveform, WaveformBuild):
        raise TypeError("waveform must be WaveformBuild")
    if type(payload_truth) is not PayloadTruth:
        raise TypeError("payload_truth must be the exact PayloadTruth type")
    if type(physical_cell) is not PhysicalCell or physical_cell not in contract.population_manifest:
        raise ChannelError("physical_cell must be an exact registered population cell")
    _assert_payload_waveform_binding(contract, payload_truth, waveform)
    streams = spawn_named_streams(root_seed)
    physical = realize_supplied_waveform(
        waveform.waveform,
        streams=streams,
        snr_db=physical_cell.snr_db,
        linewidth_hz=physical_cell.linewidth_hz,
        symbol_rate_baud=contract.population.symbol_rate_baud,
    )
    known_indices = np.flatnonzero(waveform.known_mask)
    periodic_indices = known_indices[known_indices >= 32]
    equalized_rows: list[np.ndarray] = []
    phase_rows: list[np.ndarray] = []
    c_post_rows: list[float] = []
    global_states: list[int] = []
    for pol in range(2):
        calibration = receiver_module.estimate_prefix_calibration(
            physical.received[pol, :32], waveform.known_symbols[pol, :32]
        )
        scalar_equalized, _ = receiver_module.scalar_visible_power_equalize(
            physical.received[pol], c_pre_cplx=calibration.c_pre_cplx
        )
        bps = receiver_module.run_common_bps(
            scalar_equalized, B=32, Nw=31
        )
        resolved = receiver_module.resolve_global_symmetry(
            bps.samples, waveform.known_symbols[pol, :32]
        )
        equalized_rows.append(resolved.samples)
        phase_rows.append(bps.phase_trace)
        global_states.append(resolved.state)
        c_post_rows.append(
            receiver_module.estimate_post_bps_residual(
                resolved.samples, waveform.known_symbols[pol, :32]
            )
        )
    receipt_rows = tuple(
        {
            "name": receipt.name,
            "root_entropy": receipt.root_entropy,
            "numpy_version": receipt.numpy_version,
            "child_spawn_key": receipt.child_spawn_key,
            "pool_size": receipt.pool_size,
            "child_generate_state_4_uint32": receipt.child_generate_state_4_uint32,
        }
        for receipt in streams.receipts
    )
    receiver = ReceiverView(
        received_samples=physical.received,
        equalized_samples=np.stack(equalized_rows),
        common_cpr_phase_trace=np.stack(phase_rows),
        known_prefix=waveform.known_symbols[:, :32],
        periodic_pilots=waveform.known_symbols[:, periodic_indices],
        code_layout=contract.population.code,
        waveform_layout=WaveformLayout(
            prefix_symbols=32,
            pilot_period_symbols=waveform.N,
            data_symbols_per_polarization=6144,
            total_symbols_per_polarization=waveform.waveform.shape[1],
        ),
        b2_parameters={},
        receipts={
            "channel_model_id": "supplied_waveform_flat_dual_pol_v1",
            "named_rng_children": receipt_rows,
            "receiver_front_end_id": "scalar_per_pol_receiver_only_v1",
            "prefix_calibration_estimator_id": "known_prefix_ls_rss_over_31_v1",
            "scalar_equalizer_id": "scalar_visible_power_mmse_v1",
            "common_bps": {"B": 32, "Nw": 31},
            "global_symmetry_state_per_pol": tuple(global_states),
            "c_post_cplx_per_pol": tuple(c_post_rows),
        },
    )
    channel_h = physical.field_fade * np.exp(1j * physical.phase)
    truth = TruthView(
        information_bits=payload_truth.information_bits,
        coded_bits=payload_truth.coded_bits,
        transmitted_symbols=waveform.waveform,
        true_phase=physical.phase,
        channel_h=channel_h,
        physical_snr_db=float(physical_cell.snr_db),
        fade=physical.intensity,
        noise_receipt={
            "samples": physical.noise,
            "per_real_variance": physical.per_real_noise_variance,
            "complex_power": physical.complex_noise_power,
            "root_entropy": root_seed,
        },
        event_label=_event_label(event_fixture),
    )
    return receiver, truth


__all__ = [
    "ChannelError",
    "NamedStreams",
    "PhysicalRealization",
    "SeedChildReceipt",
    "STREAM_NAMES",
    "awgn_variances",
    "build_views",
    "finalize_truth_view",
    "gamma_gamma_rho",
    "gamma_gamma_tau_c",
    "generate_wiener_phase",
    "realize_supplied_waveform",
    "spawn_named_streams",
    "wiener_innovation_variance",
]
