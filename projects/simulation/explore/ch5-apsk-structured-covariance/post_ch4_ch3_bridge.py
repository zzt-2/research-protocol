"""T060 receiver-visible Ch4 -> per-polarization Ch3 residual bridge.

Correctness only.  The deployable path consumes received samples and known
pilots; transmitted payload truth is kept in a separate offline object.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import importlib.util
from pathlib import Path
from typing import Callable

import numpy as np

from codec_metrics import apsk16_table
from common._channel import doppler_phase, gg_block
from common._recovery import da_ml_recovery


SCOPE = (
    "BRIDGE_CORRECTNESS_ONLY",
    "TARGET_OCCURRENCE_NOT_RUN",
    "NO_METHOD_SIGNAL",
)


def _load_ch4_core():
    path = Path(__file__).resolve().parents[1] / "ch4-apsk-ring-gated-rde" / "core.py"
    spec = importlib.util.spec_from_file_location("t060_ch4_core", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load Ch4 core from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CH4 = _load_ch4_core()


@dataclass(frozen=True)
class BridgeConfig:
    seed: int
    n_symbols: int
    observation_stop: int
    snr_db: float
    turbulence_alpha: float
    turbulence_beta: float
    gamma_gamma_block: int
    f_residual_hz: float
    f_dot_hz_per_s: float
    linewidth_hz: float
    ch4_pilot_count: int = 16
    pilot_indices: tuple[int, ...] = tuple(range(32))
    pilot_label_shift: int = 3
    scope: tuple[str, ...] = SCOPE
    cell_id: str = "t060-correctness-cell"
    window_id: str = "observation-0"
    config_id: str = "t060.bridge-correctness.v1"
    source_id: str = "T060/D046"

    @classmethod
    def correctness_fixture(cls, **kwargs) -> "BridgeConfig":
        return cls(**kwargs)

    def __post_init__(self) -> None:
        if self.n_symbols < 32 or not 32 <= self.observation_stop <= self.n_symbols:
            raise ValueError("need n_symbols >= observation_stop >= 32")
        if self.gamma_gamma_block <= 0:
            raise ValueError("gamma_gamma_block must be positive")
        indices = np.asarray(self.pilot_indices, dtype=np.int64)
        if indices.ndim != 1 or indices.size < 32 or indices.size % 16:
            raise ValueError("pilot_indices must contain a positive multiple of 16 pilots")
        if np.any(indices < 0) or np.any(indices >= self.observation_stop):
            raise ValueError("pilot_indices must stay inside the observation window")
        if np.any(np.diff(indices) <= 0):
            raise ValueError("pilot_indices must be strictly increasing")


@dataclass(frozen=True)
class FrozenCh4Arm:
    arm_id: str
    mode: str
    mu: float
    ring_threshold: float | None = None
    decision_threshold: float | None = None

    @classmethod
    def fixture_plain(cls, *, mu: float) -> "FrozenCh4Arm":
        return cls("fixture-plain-mu0", "plain", float(mu))

    def canonical_snapshot(self) -> dict:
        return {
            "arm_id": self.arm_id,
            "mode": self.mode,
            "mu": float(self.mu),
            "ring_threshold": None
            if self.ring_threshold is None
            else float(self.ring_threshold),
            "decision_threshold": None
            if self.decision_threshold is None
            else float(self.decision_threshold),
        }


@dataclass(frozen=True)
class ReceiverVisibleInput:
    rx: np.ndarray
    ch4_pilot_rx: np.ndarray
    ch4_pilot_tx: np.ndarray
    pilot_indices: np.ndarray
    pilot_symbols: np.ndarray
    pilot_labels: np.ndarray
    known_mask: np.ndarray
    observation_stop: int
    config: BridgeConfig

    def with_future_rx(self, future: np.ndarray) -> "ReceiverVisibleInput":
        expected = self.rx[:, self.observation_stop :].shape
        value = np.asarray(future, dtype=np.complex128)
        if value.shape != expected:
            raise ValueError(f"future shape must be {expected}")
        rx = self.rx.copy()
        rx[:, self.observation_stop :] = value
        return replace(self, rx=rx)

    def with_visible_rx_delta(self, *, pol: int, index: int, delta: complex) -> "ReceiverVisibleInput":
        rx = self.rx.copy()
        rx[pol, index] += delta
        return replace(self, rx=rx)


@dataclass
class OfflineTruth:
    payload_labels: np.ndarray
    payload_bits: np.ndarray
    true_jones: np.ndarray
    true_phase: np.ndarray
    true_snr_db: float


@dataclass(frozen=True)
class ResidualBridgeBundle:
    z_pilot: np.ndarray
    x_pilot: np.ndarray
    e: np.ndarray
    pilot_indices: np.ndarray
    point_labels: np.ndarray
    ring_labels: np.ndarray
    per_pol_point_counts: np.ndarray
    per_point_counts: np.ndarray
    known_mask: np.ndarray
    cpr_mode: str
    estimated_phase: np.ndarray
    estimated_frequency_hz: np.ndarray
    ambiguity_index: np.ndarray
    frozen_ch4_snapshot: dict
    ch4_summary: dict
    ch4_W: np.ndarray
    realization_timing: dict
    scope: tuple[str, ...]
    cell_id: str
    seed: int
    window_id: str
    config_id: str
    source_id: str
    realization_hash: str
    bundle_hash: str
    cpr_state_scope: str = "per-polarization/observation-window-only"
    cross_polarization_pooling: bool = False

    def deployable_dict(self) -> dict:
        return {
            "z_pilot": self.z_pilot,
            "x_pilot": self.x_pilot,
            "e": self.e,
            "pilot_indices": self.pilot_indices,
            "point_labels": self.point_labels,
            "ring_labels": self.ring_labels,
            "per_pol_point_counts": self.per_pol_point_counts,
            "per_point_counts": self.per_point_counts,
            "known_mask": self.known_mask,
            "cpr_mode": self.cpr_mode,
            "estimated_phase": self.estimated_phase,
            "estimated_frequency_hz": self.estimated_frequency_hz,
            "ambiguity_index": self.ambiguity_index,
            "ch4_arm": self.ch4_summary["arm_id"],
            "frozen_ch4_snapshot": self.frozen_ch4_snapshot,
            "ch4_W": self.ch4_W,
            "ch4_gate_summary": self.ch4_summary,
            "realization_timing": self.realization_timing,
            "scope": self.scope,
            "cell_id": self.cell_id,
            "seed": self.seed,
            "window_id": self.window_id,
            "config_id": self.config_id,
            "source_id": self.source_id,
            "realization_hash": self.realization_hash,
            "bundle_hash": self.bundle_hash,
        }


def _hash_receiver_visible(metadata: tuple, *arrays: np.ndarray) -> str:
    digest = sha256(repr(metadata).encode("utf-8"))
    for value in arrays:
        array = np.ascontiguousarray(value)
        digest.update(str(array.shape).encode("ascii"))
        digest.update(array.dtype.str.encode("ascii"))
        digest.update(array.tobytes())
    return digest.hexdigest()


def generate_correctness_fixture(
    config: BridgeConfig, *, identity_jones: bool, noiseless: bool
) -> tuple[ReceiverVisibleInput, OfflineTruth]:
    """Generate one DP receiver input with shared scalar GG/CFO/Wiener state."""
    np.random.seed(config.seed)
    rng = np.random.default_rng(config.seed)
    symbols, bits_by_label = apsk16_table()
    labels = rng.integers(0, 16, size=(2, config.n_symbols), dtype=np.int64)
    pilot_indices = np.asarray(config.pilot_indices, dtype=np.int64)
    balanced = np.tile(
        np.arange(16, dtype=np.int64), pilot_indices.size // 16
    )
    labels[:, pilot_indices] = np.stack(
        (balanced, np.roll(balanced, config.pilot_label_shift))
    )
    tx = symbols[labels]

    ch4_tx = CH4.orthogonal_pilots(config.ch4_pilot_count)
    transmitted = np.concatenate((ch4_tx, tx), axis=1)
    total_length = transmitted.shape[1]
    sampled_gg = gg_block(
        total_length,
        config.turbulence_alpha,
        config.turbulence_beta,
        bs=config.gamma_gamma_block,
    )
    sampled_phase = doppler_phase(
        total_length,
        f_res=config.f_residual_hz,
        f_dot=config.f_dot_hz_per_s,
        lw=config.linewidth_hz,
    )
    identity_scalar = (
        noiseless
        and config.turbulence_alpha >= 1.0e11
        and config.turbulence_beta >= 1.0e11
        and config.f_residual_hz == 0.0
        and config.f_dot_hz_per_s == 0.0
        and config.linewidth_hz == 0.0
    )
    scalar = (
        np.ones(total_length, dtype=np.complex128)
        if identity_scalar
        else np.sqrt(sampled_gg) * np.exp(1j * sampled_phase)
    )
    jones = np.eye(2, dtype=np.complex128) if identity_jones else CH4.random_su2(rng)
    pre_noise = jones @ (transmitted * scalar[None, :])
    noise_var = 0.0 if noiseless else 10.0 ** (-config.snr_db / 10.0)
    noise = np.sqrt(noise_var / 2.0) * (
        rng.standard_normal(pre_noise.shape) + 1j * rng.standard_normal(pre_noise.shape)
    )
    received = pre_noise + noise
    ch4_rx = received[:, : config.ch4_pilot_count]
    rx = received[:, config.ch4_pilot_count :]
    pilot_labels = labels[:, pilot_indices].copy()
    pilot_symbols = symbols[pilot_labels]
    known_mask = np.zeros((2, config.n_symbols), dtype=bool)
    known_mask[:, pilot_indices] = True
    receiver = ReceiverVisibleInput(
        rx=rx,
        ch4_pilot_rx=ch4_rx,
        ch4_pilot_tx=ch4_tx,
        pilot_indices=pilot_indices,
        pilot_symbols=pilot_symbols,
        pilot_labels=pilot_labels,
        known_mask=known_mask,
        observation_stop=config.observation_stop,
        config=config,
    )
    truth = OfflineTruth(
        payload_labels=labels.copy(),
        payload_bits=bits_by_label[labels].copy(),
        true_jones=jones.copy(),
        true_phase=sampled_phase.copy(),
        true_snr_db=config.snr_db,
    )
    return receiver, truth


def swap_polarizations(receiver: ReceiverVisibleInput) -> ReceiverVisibleInput:
    return replace(
        receiver,
        rx=receiver.rx[::-1].copy(),
        ch4_pilot_rx=receiver.ch4_pilot_rx[::-1].copy(),
        ch4_pilot_tx=receiver.ch4_pilot_tx[::-1].copy(),
        pilot_symbols=receiver.pilot_symbols[::-1].copy(),
        pilot_labels=receiver.pilot_labels[::-1].copy(),
        known_mask=receiver.known_mask[::-1].copy(),
    )


def run_frozen_ch4_arm(rx: np.ndarray, w0: np.ndarray, frozen_arm: FrozenCh4Arm) -> dict:
    if frozen_arm.mode == "plain":
        return CH4.run_plain_rde(rx, w0, mu=frozen_arm.mu)
    if frozen_arm.mode == "cheap":
        return CH4.run_cheap_rde(
            rx, w0, mu=frozen_arm.mu, ring_threshold=float(frozen_arm.ring_threshold)
        )
    if frozen_arm.mode == "candidate":
        return CH4.run_candidate_rde(
            rx,
            w0,
            mu=frozen_arm.mu,
            ring_threshold=float(frozen_arm.ring_threshold),
            decision_threshold=float(frozen_arm.decision_threshold),
        )
    raise ValueError("frozen Ch4 arm must be explicitly injected")


def resolve_pilot_only_ambiguity(
    z: np.ndarray, known_pilots: np.ndarray, pilot_indices: np.ndarray
) -> tuple[np.ndarray, int, np.ndarray]:
    values = np.asarray(z, dtype=np.complex128)
    pilots = np.asarray(known_pilots, dtype=np.complex128)
    indices = np.asarray(pilot_indices, dtype=np.int64)
    scores = np.empty(8, dtype=np.float64)
    candidates = []
    for index in range(8):
        candidate = values * np.exp(-1j * 2.0 * np.pi * index / 8.0)
        candidates.append(candidate)
        scores[index] = float(np.sum(np.abs(candidate[indices] - pilots) ** 2))
    selected = int(np.argmin(scores))
    return candidates[selected], selected, scores


def _run_bridge_with_observation(
    receiver: ReceiverVisibleInput,
    frozen_arm: FrozenCh4Arm,
    *,
    ch4_runner: Callable = run_frozen_ch4_arm,
    da_runner: Callable = da_ml_recovery,
) -> tuple[ResidualBridgeBundle, np.ndarray]:
    """Run Ch4 demux/RDE, then independent per-pol DA CPR, then pilot resolve."""
    stop = receiver.observation_stop
    rx = np.asarray(receiver.rx[:, :stop], dtype=np.complex128)
    w0 = CH4.pilot_ls_demux(receiver.ch4_pilot_rx, receiver.ch4_pilot_tx)
    ch4 = ch4_runner(rx, w0, frozen_arm)

    compensated = np.empty_like(ch4["z"])
    phase = np.empty(2, dtype=np.float64)
    frequency = np.empty(2, dtype=np.float64)
    ambiguity = np.empty(2, dtype=np.int64)
    for pol in range(2):
        da, phase[pol], frequency[pol] = da_runner(
            ch4["z"][pol],
            receiver.pilot_indices,
            receiver.pilot_symbols[pol],
            mod="m16apsk",
        )
        compensated[pol], ambiguity[pol], _ = resolve_pilot_only_ambiguity(
            da, receiver.pilot_symbols[pol], receiver.pilot_indices
        )

    z_pilot = compensated[:, receiver.pilot_indices]
    x_pilot = receiver.pilot_symbols.copy()
    residual = z_pilot - x_pilot
    counts = np.stack(
        [np.bincount(receiver.pilot_labels[pol], minlength=16) for pol in range(2)]
    )
    frozen_snapshot = frozen_arm.canonical_snapshot()
    realization_timing = {
        "continuous_scalar": True,
        "preamble_length": receiver.config.ch4_pilot_count,
        "observation_length": receiver.config.n_symbols,
        "observation_start": receiver.config.ch4_pilot_count,
        "total_length": receiver.config.ch4_pilot_count + receiver.config.n_symbols,
    }
    gate_summary = {
        "arm_id": frozen_arm.arm_id,
        "mode": frozen_arm.mode,
        "frozen_arm_snapshot": frozen_snapshot,
        "gate_open_count_per_pol": np.count_nonzero(ch4["gates"], axis=1).tolist(),
        "gate_total_per_pol": [int(stop), int(stop)],
    }
    realization_hash = _hash_receiver_visible(
        (
            receiver.config.seed,
            receiver.config.cell_id,
            receiver.config.window_id,
            stop,
            tuple(realization_timing.items()),
        ),
        rx,
        receiver.ch4_pilot_rx,
        receiver.ch4_pilot_tx,
        receiver.pilot_indices,
        receiver.pilot_symbols,
        receiver.pilot_labels,
        receiver.known_mask[:, :stop],
    )
    bundle_hash = _hash_receiver_visible(
        (
            tuple(frozen_snapshot.items()),
            tuple(gate_summary["gate_open_count_per_pol"]),
            tuple(gate_summary["gate_total_per_pol"]),
            receiver.config.config_id,
            receiver.config.source_id,
            realization_hash,
            "DA",
        ),
        z_pilot,
        x_pilot,
        residual,
        phase,
        frequency,
        ambiguity,
        ch4["W"],
        counts,
    )
    bundle = ResidualBridgeBundle(
        z_pilot=z_pilot,
        x_pilot=x_pilot,
        e=residual,
        pilot_indices=receiver.pilot_indices.copy(),
        point_labels=receiver.pilot_labels.copy(),
        ring_labels=receiver.pilot_labels >= 8,
        per_pol_point_counts=counts,
        per_point_counts=counts.sum(axis=0),
        known_mask=receiver.known_mask[:, :stop].copy(),
        cpr_mode="DA",
        estimated_phase=phase,
        estimated_frequency_hz=frequency,
        ambiguity_index=ambiguity,
        frozen_ch4_snapshot=frozen_snapshot,
        ch4_summary=gate_summary,
        ch4_W=ch4["W"].copy(),
        realization_timing=realization_timing,
        scope=receiver.config.scope,
        cell_id=receiver.config.cell_id,
        seed=receiver.config.seed,
        window_id=receiver.config.window_id,
        config_id=receiver.config.config_id,
        source_id=receiver.config.source_id,
        realization_hash=realization_hash,
        bundle_hash=bundle_hash,
    )
    return bundle, compensated.copy()


def run_bridge(
    receiver: ReceiverVisibleInput,
    frozen_arm: FrozenCh4Arm,
    *,
    ch4_runner: Callable = run_frozen_ch4_arm,
    da_runner: Callable = da_ml_recovery,
) -> ResidualBridgeBundle:
    """Return the receiver-visible pilot bundle for the frozen bridge."""
    bundle, _ = _run_bridge_with_observation(
        receiver, frozen_arm, ch4_runner=ch4_runner, da_runner=da_runner
    )
    return bundle


def run_bridge_with_observation(
    receiver: ReceiverVisibleInput,
    frozen_arm: FrozenCh4Arm,
    *,
    ch4_runner: Callable = run_frozen_ch4_arm,
    da_runner: Callable = da_ml_recovery,
) -> tuple[ResidualBridgeBundle, np.ndarray]:
    """Return the same bridge bundle plus its receiver-visible observation."""
    return _run_bridge_with_observation(
        receiver, frozen_arm, ch4_runner=ch4_runner, da_runner=da_runner
    )


def circular_control_pilots(symbols: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    offsets = np.array([0.02, -0.02, 0.02j, -0.02j], dtype=np.complex128)
    labels = np.repeat(np.arange(16, dtype=np.int64), 4)
    return np.repeat(np.asarray(symbols), 4) + np.tile(offsets, 16), labels


__all__ = [
    "BridgeConfig",
    "FrozenCh4Arm",
    "OfflineTruth",
    "ReceiverVisibleInput",
    "ResidualBridgeBundle",
    "circular_control_pilots",
    "da_ml_recovery",
    "generate_correctness_fixture",
    "resolve_pilot_only_ambiguity",
    "run_bridge",
    "run_bridge_with_observation",
    "run_frozen_ch4_arm",
    "swap_polarizations",
]
