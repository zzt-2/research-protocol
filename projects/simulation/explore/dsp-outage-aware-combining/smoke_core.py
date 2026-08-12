"""Receiver-only Q001 defect-smoke channel, estimator, and fixed comparators.

The module separates receiver inputs from evaluator truth, implements only
conventional B0/B1/B2 arms plus a truth-aware scoring oracle, and contains no
candidate soft-validity method. Gamma-Gamma values and the four-branch
heterogeneity construction remain bounded MVE inputs marked
``UNVERIFIED_RANGE``.
"""

from __future__ import annotations

from dataclasses import dataclass
import ast
import hashlib
import inspect
import itertools
import json
from pathlib import Path
import textwrap
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]
UIntArray = NDArray[np.uint8]
COMPLEX_NOISE_VARIANCE = 1.0  # E[|n|^2]; I/Q variance is 0.5 each for every branch.


@dataclass(frozen=True)
class CellSpec:
    turbulence: str
    gg_alpha: float
    gg_beta: float
    n_branches: int
    heterogeneity: str
    branch_snr_db: tuple[float, ...]
    parameter_status: str = "UNVERIFIED_RANGE"

    def __post_init__(self) -> None:
        if self.n_branches != len(self.branch_snr_db):
            raise ValueError("n_branches must match branch_snr_db")

    @property
    def cell_id(self) -> str:
        return f"{self.turbulence}-K{self.n_branches}-{self.heterogeneity}"


@dataclass(frozen=True)
class ReceiverFrame:
    """All and only information available to a deployable receiver."""

    branches: tuple[ComplexArray, ...]
    fsts: ComplexArray
    pilot_mask: BoolArray
    pilot_symbols: ComplexArray
    payload_mask: BoolArray
    ts: float
    max_search_offset: int


@dataclass(frozen=True)
class TruthRecord:
    """Evaluator-only fields; never accepted by receiver algorithms."""

    payload_bits: UIntArray
    payload_symbols: ComplexArray
    offsets: tuple[int, ...]
    branch_gains: ComplexArray
    nominal_snr_offset_db: tuple[float, ...]
    instantaneous_snr_db: FloatArray
    turbulence: str
    shared_phase: FloatArray
    unscaled_branch_gains: ComplexArray | None = None
    noise_variance_complex: float = COMPLEX_NOISE_VARIANCE


@dataclass(frozen=True, eq=False)
class BranchEstimate:
    """Branch-local quantities derived from received samples and known symbols."""

    estimated_offset: int
    sync_peak: float
    sync_margin: float
    estimated_channel: complex
    estimated_snr_db: float
    estimated_power: float
    pilot_ls_residual: float
    pilot_coherence: float
    cpe_increment_rms: float
    cpe_coherence: float
    phase_corrected_payload: ComplexArray

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BranchEstimate):
            return NotImplemented
        scalar_names = tuple(
            name for name in self.__dataclass_fields__ if name != "phase_corrected_payload"
        )
        return all(getattr(self, name) == getattr(other, name) for name in scalar_names) and np.array_equal(
            self.phase_corrected_payload, other.phase_corrected_payload
        )


@dataclass(frozen=True, eq=False)
class ArmOutput:
    subset: tuple[int, ...]
    no_valid: bool
    combined: ComplexArray | None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArmOutput):
            return NotImplemented
        arrays_equal = self.combined is None and other.combined is None
        if self.combined is not None and other.combined is not None:
            arrays_equal = np.array_equal(self.combined, other.combined)
        return self.subset == other.subset and self.no_valid == other.no_valid and arrays_equal


@dataclass(frozen=True)
class OracleOutput:
    subset: tuple[int, ...]
    ber: float
    combined: ComplexArray


def _readonly(array: NDArray) -> NDArray:
    result = np.ascontiguousarray(array)
    result.flags.writeable = False
    return result


def _qpsk(bits: UIntArray) -> ComplexArray:
    if bits.ndim != 2 or bits.shape[1] != 2:
        raise ValueError("QPSK bits must have shape (symbols, 2)")
    real = 1.0 - 2.0 * bits[:, 0].astype(np.float64)
    imag = 1.0 - 2.0 * bits[:, 1].astype(np.float64)
    return (real + 1j * imag) / np.sqrt(2.0)


def _deterministic_fsts() -> ComplexArray:
    """Build a 320-symbol single-pol Park/FSTS proxy (BN=16, BL=20).

    Wang's FSTS is dual-polarization.  This bounded MVE uses an explicit
    single-polarization proxy: eight deterministic QPSK blocks followed by
    their block-order-reversed, within-block-reversed conjugates.  It preserves
    the BN/BL and front/back conjugate symmetry needed by a Park timing metric;
    it is not claimed as an exact PM-FSTS reproduction.
    """

    bl = 20
    front_blocks = []
    base_index = np.asarray(
        [0, 1, 3, 2, 1, 0, 2, 3, 3, 2, 0, 1, 2, 3, 1, 0, 1, 2, 3, 0],
        dtype=np.int64,
    )
    constellation = np.asarray((1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j)) / np.sqrt(2.0)
    for block_index in range(8):
        shifted = np.roll(base_index, (3 * block_index) % bl)
        front_blocks.append(constellation[(shifted + block_index) % 4])
    front = np.asarray(front_blocks, dtype=np.complex128)
    back = np.conj(front[::-1, ::-1])
    return _readonly(np.concatenate((front.reshape(-1), back.reshape(-1))))


def build_primary_cells() -> tuple[CellSpec, ...]:
    """Return the frozen 3 x 2 x 3 primary grid (18 physical cells)."""

    # Repository-scan values conflict with an older formula source.  They are
    # therefore scanned as UNVERIFIED_RANGE, not asserted as authoritative.
    gamma_gamma = {
        "weak": (11.6, 10.1),
        "moderate": (4.0, 1.9),
        "strong": (4.2, 1.4),
    }
    two_branch = {
        "H0": (0.0, 0.0),
        "H1": (0.0, -1.0),
        "H2": (0.0, -6.0),
    }
    cells: list[CellSpec] = []
    for turbulence, (alpha, beta) in gamma_gamma.items():
        for n_branches in (2, 4):
            for heterogeneity, pair in two_branch.items():
                # K=4 duplicates each strong/weak class deterministically.  This
                # construction is also an UNVERIFIED_RANGE MVE input.
                snr = pair if n_branches == 2 else (pair[0], pair[0], pair[1], pair[1])
                cells.append(
                    CellSpec(
                        turbulence=turbulence,
                        gg_alpha=alpha,
                        gg_beta=beta,
                        n_branches=n_branches,
                        heterogeneity=heterogeneity,
                        branch_snr_db=snr,
                    )
                )
    return tuple(cells)


def _cell_seed_key(cell: CellSpec) -> int:
    digest = hashlib.sha256(cell.cell_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], byteorder="little", signed=False)


def generate_realization(
    seed: int,
    cell: CellSpec,
    payload_symbols: int = 30_720,
) -> tuple[ReceiverFrame, TruthRecord, str]:
    """Generate one paired multi-branch frame using only explicit local RNGs."""

    if payload_symbols <= 0:
        raise ValueError("payload_symbols must be positive")

    symbol_rate = 10.0e9
    ts = 1.0 / symbol_rate
    linewidth_hz = 50.0e3
    max_search_offset = 7
    root = np.random.SeedSequence([int(seed), _cell_seed_key(cell)])
    streams = root.spawn(2 + cell.n_branches)
    payload_rng = np.random.default_rng(streams[0])
    phase_rng = np.random.default_rng(streams[1])
    branch_rngs = [np.random.default_rng(stream) for stream in streams[2:]]

    payload_bits = payload_rng.integers(0, 2, size=(payload_symbols, 2), dtype=np.uint8)
    transmitted_bits = payload_bits.copy()
    pilot_mask = np.zeros(payload_symbols, dtype=np.bool_)
    pilot_mask[::100] = True
    pilot_positions = np.flatnonzero(pilot_mask)
    pilot_bits = np.column_stack(
        ((pilot_positions // 100) % 2, ((pilot_positions // 100) // 2) % 2)
    ).astype(np.uint8)
    transmitted_bits[pilot_positions] = pilot_bits
    payload_block = _qpsk(transmitted_bits)
    pilot_symbols_array = payload_block[pilot_mask].copy()
    payload_mask = ~pilot_mask

    fsts = _deterministic_fsts()
    tx_symbols = np.concatenate((fsts, payload_block))
    phase_step_std = np.sqrt(2.0 * np.pi * linewidth_hz * ts)
    shared_phase = np.cumsum(
        phase_rng.normal(0.0, phase_step_std, size=tx_symbols.size)
    )
    phase_rotated = tx_symbols * np.exp(1j * shared_phase)

    branches: list[ComplexArray] = []
    offsets: list[int] = []
    gains: list[complex] = []
    unscaled_gains: list[complex] = []
    for snr_db, rng in zip(cell.branch_snr_db, branch_rngs):
        irradiance = rng.gamma(cell.gg_alpha, 1.0 / cell.gg_alpha) * rng.gamma(
            cell.gg_beta, 1.0 / cell.gg_beta
        )
        static_phase = rng.uniform(-np.pi, np.pi)
        unscaled_gain = np.sqrt(irradiance) * np.exp(1j * static_phase)
        gain = unscaled_gain * 10.0 ** (snr_db / 20.0)
        offset = int(rng.integers(0, max_search_offset + 1))
        noise_sigma = np.sqrt(COMPLEX_NOISE_VARIANCE / 2.0)
        samples = noise_sigma * (
            rng.normal(size=tx_symbols.size + max_search_offset)
            + 1j * rng.normal(size=tx_symbols.size + max_search_offset)
        )
        samples[offset : offset + tx_symbols.size] += gain * phase_rotated
        branches.append(_readonly(samples.astype(np.complex128, copy=False)))
        offsets.append(offset)
        gains.append(gain)
        unscaled_gains.append(unscaled_gain)

    frame = ReceiverFrame(
        branches=tuple(branches),
        fsts=fsts,
        pilot_mask=_readonly(pilot_mask),
        pilot_symbols=_readonly(pilot_symbols_array),
        payload_mask=_readonly(payload_mask),
        ts=ts,
        max_search_offset=max_search_offset,
    )
    gains_array = np.asarray(gains, dtype=np.complex128)
    instantaneous_snr_db = 10.0 * np.log10(
        np.maximum(np.abs(gains_array) ** 2 / COMPLEX_NOISE_VARIANCE, np.finfo(float).tiny)
    )
    truth = TruthRecord(
        payload_bits=_readonly(transmitted_bits),
        payload_symbols=_readonly(payload_block),
        offsets=tuple(offsets),
        branch_gains=_readonly(gains_array),
        nominal_snr_offset_db=cell.branch_snr_db,
        instantaneous_snr_db=_readonly(instantaneous_snr_db),
        turbulence=cell.turbulence,
        shared_phase=_readonly(shared_phase),
        unscaled_branch_gains=_readonly(np.asarray(unscaled_gains, dtype=np.complex128)),
        noise_variance_complex=COMPLEX_NOISE_VARIANCE,
    )
    return frame, truth, receiver_realization_hash(frame)


def receiver_realization_hash(frame: ReceiverFrame) -> str:
    """Hash receiver-visible data only; truth records cannot affect it."""

    digest = hashlib.sha256()
    metadata = {
        "ts": frame.ts,
        "max_search_offset": frame.max_search_offset,
        "n_branches": len(frame.branches),
    }
    digest.update(json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    for array in (
        *frame.branches,
        frame.fsts,
        frame.pilot_mask,
        frame.pilot_symbols,
        frame.payload_mask,
    ):
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.dtype).encode("ascii"))
        digest.update(np.asarray(contiguous.shape, dtype=np.int64).tobytes())
        digest.update(contiguous.tobytes(order="C"))
    return digest.hexdigest()


def _normalized_sync_scores(
    branch: ComplexArray, training_length: int, max_offset: int
) -> FloatArray:
    """Return a phase-invariant Park metric for conjugate-symmetric halves."""

    if training_length <= 0 or training_length % 2:
        raise ValueError("Park training length must be positive and even")
    half = training_length // 2
    scores = []
    for offset in range(max_offset + 1):
        candidate = branch[offset : offset + training_length]
        front = candidate[:half]
        mirrored_back = np.conj(candidate[half:][::-1])
        front_energy = float(np.vdot(front, front).real)
        back_energy = float(np.vdot(mirrored_back, mirrored_back).real)
        denominator = np.sqrt(front_energy * back_energy) + np.finfo(float).eps
        scores.append(float(abs(np.vdot(front, mirrored_back)) / denominator))
    return np.asarray(scores, dtype=np.float64)


def guarded_sync_peak_margin(
    scores: FloatArray, winner: int, guard: int = 1
) -> tuple[float, float]:
    """Return winner and margin over peaks outside frozen ±1 guard.

    The default and scientific-contract guard is one candidate offset on each
    side. If no unguarded candidate exists, the second peak is defined as zero.
    """

    if scores.ndim != 1 or scores.size == 0:
        raise ValueError("sync scores must be a non-empty vector")
    if winner < 0 or winner >= scores.size:
        raise ValueError("winner is outside sync score vector")
    if guard < 0:
        raise ValueError("guard must be non-negative")
    unguarded = np.ones(scores.size, dtype=np.bool_)
    lower = max(0, winner - guard)
    upper = min(scores.size, winner + guard + 1)
    unguarded[lower:upper] = False
    peak = float(scores[winner])
    second = float(np.max(scores[unguarded])) if np.any(unguarded) else 0.0
    return peak, peak - second


def estimate_branches(frame: ReceiverFrame) -> tuple[BranchEstimate, ...]:
    """Estimate synchronization, channel, and pilot phase using receiver data only."""

    estimates: list[BranchEstimate] = []
    n_payload = frame.pilot_mask.size
    pilot_positions = np.flatnonzero(frame.pilot_mask)
    all_positions = np.arange(n_payload)
    fsts_energy = float(np.vdot(frame.fsts, frame.fsts).real)
    for branch in frame.branches:
        scores = _normalized_sync_scores(branch, frame.fsts.size, frame.max_search_offset)
        offset = int(np.argmax(scores))
        sync_peak, sync_margin = guarded_sync_peak_margin(scores, offset, guard=1)
        training_rx = branch[offset : offset + frame.fsts.size]
        channel = complex(np.vdot(frame.fsts, training_rx) / fsts_energy)
        training_error = training_rx - channel * frame.fsts
        noise_power = float(np.mean(np.abs(training_error) ** 2))
        power = float(abs(channel) ** 2)
        snr_linear = power / max(noise_power, np.finfo(float).tiny)
        payload_rx = branch[
            offset + frame.fsts.size : offset + frame.fsts.size + n_payload
        ]
        pilot_ratio = payload_rx[pilot_positions] / (
            channel * frame.pilot_symbols + np.finfo(float).eps
        )
        pilot_phase = np.unwrap(np.angle(pilot_ratio))
        phase_curve = np.interp(all_positions, pilot_positions, pilot_phase)
        corrected = payload_rx * np.exp(-1j * phase_curve)
        pilot_error = corrected[pilot_positions] - channel * frame.pilot_symbols
        residual = float(np.mean(np.abs(pilot_error) ** 2))
        unit_phasors = np.exp(1j * pilot_phase)
        pilot_coherence = float(abs(np.mean(unit_phasors)))
        increments = np.diff(pilot_phase)
        increment_rms = float(np.sqrt(np.mean(increments**2))) if increments.size else 0.0
        cpe_coherence = float(abs(np.mean(np.exp(1j * increments)))) if increments.size else 1.0
        estimates.append(
            BranchEstimate(
                estimated_offset=offset,
                sync_peak=sync_peak,
                sync_margin=sync_margin,
                estimated_channel=channel,
                estimated_snr_db=float(10.0 * np.log10(max(snr_linear, np.finfo(float).tiny))),
                estimated_power=power,
                pilot_ls_residual=residual,
                pilot_coherence=pilot_coherence,
                cpe_increment_rms=increment_rms,
                cpe_coherence=cpe_coherence,
                phase_corrected_payload=_readonly(corrected.astype(np.complex128, copy=False)),
            )
        )
    return tuple(estimates)


def combine_subset(
    estimates: tuple[BranchEstimate, ...], subset: tuple[int, ...]
) -> ComplexArray:
    """Apply equal-noise estimated-channel MRC to a non-empty subset."""

    if not subset:
        raise ValueError("MRC subset must be non-empty")
    selected = tuple(estimates[index] for index in subset)
    numerator = sum(
        np.conj(item.estimated_channel) * item.phase_corrected_payload for item in selected
    )
    denominator = sum(abs(item.estimated_channel) ** 2 for item in selected)
    return _readonly(np.asarray(numerator / (denominator + np.finfo(float).eps), dtype=np.complex128))


def _arm_output(estimates: tuple[BranchEstimate, ...], subset: tuple[int, ...]) -> ArmOutput:
    if not subset:
        return ArmOutput(subset=(), no_valid=True, combined=None)
    return ArmOutput(subset=subset, no_valid=False, combined=combine_subset(estimates, subset))


def run_b0(estimates: tuple[BranchEstimate, ...]) -> ArmOutput:
    return _arm_output(estimates, tuple(range(len(estimates))))


def run_b1(estimates: tuple[BranchEstimate, ...], tau_db: float) -> ArmOutput:
    subset = tuple(index for index, item in enumerate(estimates) if item.estimated_snr_db >= tau_db)
    return _arm_output(estimates, subset)


def run_b2(estimates: tuple[BranchEstimate, ...], top_l: int) -> ArmOutput:
    if top_l <= 0:
        return _arm_output(estimates, ())
    ranked = sorted(
        range(len(estimates)), key=lambda index: (-estimates[index].estimated_snr_db, index)
    )
    return _arm_output(estimates, tuple(sorted(ranked[: min(top_l, len(ranked))])))


def payload_ber(
    received: ComplexArray, payload_bits: UIntArray, payload_mask: BoolArray
) -> float:
    """Fixed-denominator payload BER with deterministic pi/2 ambiguity scoring."""

    if received.size != payload_bits.shape[0] or payload_mask.size != received.size:
        raise ValueError("received, payload_bits, and payload_mask lengths must match")
    expected = payload_bits[payload_mask]
    denominator = int(expected.size)
    if denominator == 0:
        raise ValueError("payload mask selects no bits")
    best_errors = denominator
    for quarter_turn in range(4):
        candidate = received[payload_mask] * (1j**quarter_turn)
        decided = np.column_stack((candidate.real < 0.0, candidate.imag < 0.0)).astype(np.uint8)
        best_errors = min(best_errors, int(np.count_nonzero(decided != expected)))
    return best_errors / denominator


def evaluate_subsets(
    estimates: tuple[BranchEstimate, ...], truth: TruthRecord, payload_mask: BoolArray
) -> OracleOutput:
    """Truth-channel best-subset/weight oracle, isolated from deployable arms.

    Branch payloads already contain receiver-visible pilot phase correction.
    The oracle replaces only the estimated static complex-channel weights with
    the actual branch gains.  It deliberately does not de-rotate
    ``truth.shared_phase`` a second time; any residual common time-varying phase
    remains common to every subset and is handled by the fixed BER scorer.
    """

    candidates: list[OracleOutput] = []
    for size in range(1, len(estimates) + 1):
        for subset in itertools.combinations(range(len(estimates)), size):
            gains = np.asarray([truth.branch_gains[index] for index in subset])
            numerator = sum(
                np.conj(gain) * estimates[index].phase_corrected_payload
                for gain, index in zip(gains, subset)
            )
            denominator = float(np.sum(np.abs(gains) ** 2))
            combined = _readonly(np.asarray(
                numerator / (denominator + np.finfo(float).eps), dtype=np.complex128
            ))
            ber = payload_ber(combined, truth.payload_bits, payload_mask)
            candidates.append(OracleOutput(subset=subset, ber=ber, combined=combined))
    return min(candidates, key=lambda item: (item.ber, len(item.subset), item.subset))


def audit_deployable_information_boundary(
    functions: tuple[Callable, ...] | None = None,
) -> tuple[str, ...]:
    """Recursively reject truth/evaluator symbols reachable from deployable roots."""

    deployable = functions or (estimate_branches, run_b0, run_b1, run_b2)
    forbidden = {"TruthRecord", "truth", "evaluate_subsets", "payload_ber", "OracleOutput"}
    violations: list[str] = []
    visited: set[Callable] = set()
    queue: list[tuple[Callable, tuple[str, ...]]] = [
        (function, (function.__name__,)) for function in deployable
    ]
    sandbox_dir = str(Path(inspect.getfile(audit_deployable_information_boundary)).resolve().parent)
    while queue:
        function, call_path = queue.pop(0)
        if function in visited:
            continue
        visited.add(function)
        tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
        referenced = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        } | {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        for name in sorted(referenced & forbidden):
            violations.append(f"{'->'.join(call_path)}:{name}")
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            callee_name = node.func.id
            callee = function.__globals__.get(callee_name)
            if not inspect.isfunction(callee) or callee in visited:
                continue
            source_file = inspect.getsourcefile(callee)
            if source_file is None:
                continue
            callee_dir = str(Path(source_file).resolve().parent)
            if callee_dir == sandbox_dir:
                queue.append((callee, (*call_path, callee_name)))
    return tuple(violations)
