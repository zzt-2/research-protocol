"""Deterministic Q1 semantic smoke core.

This module is an isolated Groundwork Step 4a Probe.  It is intentionally not
part of ``projects.simulation.common`` and is not a production testbed.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


SCORE_FORMULA = "abs(x^H r)^2/(||x||^2||r||^2)"
SCORE_IDENTITY = "normalized-profiled-complex-gain-glrt-v1"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return _sha256_bytes(payload)


def _readonly_complex(values: np.ndarray | Sequence[complex]) -> np.ndarray:
    result = np.ascontiguousarray(values, dtype=np.complex128)
    result.flags.writeable = False
    return result


@dataclass(frozen=True)
class SmokeConfig:
    symbol_rate_hz: float = 56e9
    sps: int = 2
    modulation: str = "QPSK"
    rrc_beta: float = 0.1
    rrc_span_symbols: int = 10
    preamble_symbols: int = 64
    preamble_seed: int = 20260807
    awgn_master_seed: int = 20260808
    diagnostic_snr_db: float = -6.0
    frame_guard_samples: int = 10
    d_truth: tuple[int, ...] = (-8, 0, 8)
    tau_truth: tuple[float, ...] = (-0.4, -0.2, 0.0, 0.2, 0.4)
    residual_cfo_truth_hz: tuple[float, ...] = (-100e6, -50e6, 0.0, 50e6, 100e6)
    stress_cfo_truth_hz: tuple[float, ...] = (-5e9, 5e9)
    d_hypotheses: tuple[int, ...] = tuple(range(-10, 11))
    tau_hypotheses: tuple[float, ...] = (-0.4, -0.2, 0.0, 0.2, 0.4)
    residual_cfo_hypotheses_hz: tuple[float, ...] = (-150e6, -100e6, -50e6, 0.0, 50e6, 100e6, 150e6)
    stress_cfo_hypotheses_hz: tuple[float, ...] = (-5e9, -2.5e9, 0.0, 2.5e9, 5e9)
    b2_max_iterations: int = 8

    def __post_init__(self) -> None:
        if self.sps != 2 or self.modulation != "QPSK":
            raise ValueError("T015 freezes 2-sps QPSK")
        if self.rrc_beta != 0.1 or self.rrc_span_symbols != 10:
            raise ValueError("T015 freezes beta=0.1 and the span-10 sentinel")
        if self.frame_guard_samples < max(abs(x) for x in self.d_hypotheses):
            raise ValueError("frame guard must contain every frame hypothesis")

    @property
    def sample_rate_hz(self) -> float:
        return self.symbol_rate_hz * self.sps

    @property
    def rrc_tap_count(self) -> int:
        return self.rrc_span_symbols * self.sps + 1

    @property
    def aggregate_group_delay_samples(self) -> int:
        return self.rrc_tap_count - 1

    @property
    def tx_shaped_length(self) -> int:
        return self.preamble_symbols * self.sps + self.rrc_tap_count - 1

    @property
    def observation_length(self) -> int:
        return self.tx_shaped_length + 2 * self.frame_guard_samples + self.rrc_tap_count - 1

    @property
    def tie_tolerance(self) -> float:
        return float(64 * np.finfo(np.float64).eps * self.observation_length)


@dataclass(frozen=True)
class ReceiverVisible:
    cell_id: str
    realization_id: str
    rx_sha256: str
    rx_samples: np.ndarray = field(compare=False, repr=False)
    known_preamble: np.ndarray = field(compare=False, repr=False)
    layer: str
    population: str
    snr_db: float | None
    sample_rate_hz: float
    d_hypotheses: tuple[int, ...]
    tau_hypotheses: tuple[float, ...]
    cfo_hypotheses_hz: tuple[float, ...]
    grid_hash: str
    score_hash: str


@dataclass(frozen=True)
class TruthMetadata:
    cell_id: str
    true_d: int
    true_tau: float
    true_cfo_hz: float
    noise_seed: int | None
    tx_waveform: np.ndarray = field(compare=False, repr=False)


@dataclass(frozen=True)
class Selection:
    estimate: tuple[int, float, float]
    score: float
    trace_scores: tuple[float, ...]
    iterations: int
    visited: tuple[tuple[int, int, int], ...]
    terminal_candidates: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class EstimateResult:
    method: str
    estimate: tuple[int, float, float]
    score: float
    trace_scores: tuple[float, ...]
    iterations: int
    realization_id: str
    rx_sha256: str
    grid_hash: str
    score_hash: str
    surface_hash: str
    compute: dict[str, Any]
    visited_candidate_indices: tuple[tuple[int, int, int], ...]
    top1_top2_margin: float

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "estimate": list(self.estimate),
            "score": self.score,
            "trace_scores": list(self.trace_scores),
            "iterations": self.iterations,
            "realization_id": self.realization_id,
            "rx_sha256": self.rx_sha256,
            "grid_hash": self.grid_hash,
            "score_hash": self.score_hash,
            "surface_hash": self.surface_hash,
            "compute": self.compute,
            "visited_candidate_indices": [list(index) for index in self.visited_candidate_indices],
            "visited_candidate_count": len(self.visited_candidate_indices),
            "top1_top2_margin": self.top1_top2_margin,
        }


def make_rrc_taps(beta: float, span_symbols: int, sps: int) -> np.ndarray:
    """Return an odd, unit-energy root-raised-cosine FIR."""
    t = np.arange(-span_symbols * sps // 2, span_symbols * sps // 2 + 1, dtype=float) / sps
    taps = np.empty_like(t)
    for index, value in enumerate(t):
        if abs(value) < 1e-15:
            taps[index] = 1.0 + beta * (4.0 / np.pi - 1.0)
        elif beta > 0 and abs(abs(value) - 1.0 / (4.0 * beta)) < 1e-12:
            taps[index] = (beta / np.sqrt(2.0)) * (
                (1.0 + 2.0 / np.pi) * np.sin(np.pi / (4.0 * beta))
                + (1.0 - 2.0 / np.pi) * np.cos(np.pi / (4.0 * beta))
            )
        else:
            numerator = np.sin(np.pi * value * (1.0 - beta)) + 4.0 * beta * value * np.cos(
                np.pi * value * (1.0 + beta)
            )
            denominator = np.pi * value * (1.0 - (4.0 * beta * value) ** 2)
            taps[index] = numerator / denominator
    taps /= np.linalg.norm(taps)
    return taps


def make_preamble(config: SmokeConfig) -> np.ndarray:
    rng = np.random.default_rng(config.preamble_seed)
    indices = rng.integers(0, 4, size=config.preamble_symbols)
    return np.exp(1j * (np.pi / 4.0 + indices * np.pi / 2.0)).astype(np.complex128)


def _fractional_delay(values: np.ndarray, tau: float) -> np.ndarray:
    """Delay by tau samples using the frozen linear diagnostic interpolator."""
    if tau == 0.0:
        return values.copy()
    n = np.arange(values.size, dtype=float)
    source = n - tau
    real = np.interp(source, n, values.real, left=0.0, right=0.0)
    imag = np.interp(source, n, values.imag, left=0.0, right=0.0)
    return real + 1j * imag


def _tx_shaped(config: SmokeConfig, preamble: np.ndarray) -> np.ndarray:
    upsampled = np.zeros(config.preamble_symbols * config.sps, dtype=np.complex128)
    upsampled[:: config.sps] = preamble
    return np.convolve(upsampled, make_rrc_taps(config.rrc_beta, config.rrc_span_symbols, config.sps), mode="full")


def synthesize_template(config: SmokeConfig, preamble: np.ndarray, d: int, tau: float, cfo_hz: float) -> np.ndarray:
    tx = _tx_shaped(config, preamble)
    delayed = _fractional_delay(tx, tau)
    placed = np.zeros(tx.size + 2 * config.frame_guard_samples, dtype=np.complex128)
    start = config.frame_guard_samples + int(d)
    placed[start : start + delayed.size] = delayed
    n = np.arange(placed.size, dtype=float)
    placed *= np.exp(1j * 2.0 * np.pi * float(cfo_hz) * n / config.sample_rate_hz)
    received = np.convolve(
        placed,
        make_rrc_taps(config.rrc_beta, config.rrc_span_symbols, config.sps),
        mode="full",
    )
    if received.size != config.observation_length:
        raise RuntimeError("observation length drift")
    return received


def derive_cell_seed(master_seed: int, cell_id: str) -> int:
    digest = hashlib.sha256(f"{master_seed}|{cell_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def _cell_id(population: str, layer: str, d: int, tau: float, cfo_hz: float) -> str:
    return f"{population}|{layer}|d={d:+d}|tau={tau:+.1f}|cfo_hz={cfo_hz:+.1f}"


def _grid_hash(config: SmokeConfig, cfo_grid: Sequence[float]) -> str:
    return _canonical_hash(
        {
            "d": list(config.d_hypotheses),
            "tau": list(config.tau_hypotheses),
            "cfo_hz": [float(x) for x in cfo_grid],
        }
    )


def _score_hash(config: SmokeConfig) -> str:
    return _canonical_hash(
        {
            "identity": SCORE_IDENTITY,
            "formula": SCORE_FORMULA,
            "observation_length": config.observation_length,
            "tie_tolerance": config.tie_tolerance,
            "normalization": "template-energy times received-window-energy",
        }
    )


def generate_cell(
    config: SmokeConfig,
    d: int,
    tau: float,
    cfo_hz: float,
    layer: str,
    population: str,
) -> tuple[ReceiverVisible, TruthMetadata]:
    if layer not in {"noiseless", "minus6db"}:
        raise ValueError(f"unknown layer: {layer}")
    if population not in {"residual", "stress"}:
        raise ValueError(f"unknown population: {population}")
    cfo_grid = config.residual_cfo_hypotheses_hz if population == "residual" else config.stress_cfo_hypotheses_hz
    cell_id = _cell_id(population, layer, d, tau, cfo_hz)
    preamble = make_preamble(config)
    signal = synthesize_template(config, preamble, d, tau, cfo_hz)
    noise_seed: int | None = None
    snr_db: float | None = None
    rx = signal.copy()
    if layer == "minus6db":
        snr_db = config.diagnostic_snr_db
        noise_seed = derive_cell_seed(config.awgn_master_seed, cell_id)
        rng = np.random.default_rng(noise_seed)
        signal_power = float(np.mean(np.abs(signal) ** 2))
        noise_power = signal_power / (10.0 ** (snr_db / 10.0))
        rx += np.sqrt(noise_power / 2.0) * (
            rng.standard_normal(signal.size) + 1j * rng.standard_normal(signal.size)
        )
    rx = _readonly_complex(rx)
    preamble = _readonly_complex(preamble)
    rx_hash = _sha256_bytes(rx.tobytes())
    realization_id = _canonical_hash({"cell_id": cell_id, "rx_sha256": rx_hash})
    visible = ReceiverVisible(
        cell_id=cell_id,
        realization_id=realization_id,
        rx_sha256=rx_hash,
        rx_samples=rx,
        known_preamble=preamble,
        layer=layer,
        population=population,
        snr_db=snr_db,
        sample_rate_hz=config.sample_rate_hz,
        d_hypotheses=config.d_hypotheses,
        tau_hypotheses=config.tau_hypotheses,
        cfo_hypotheses_hz=tuple(float(x) for x in cfo_grid),
        grid_hash=_grid_hash(config, cfo_grid),
        score_hash=_score_hash(config),
    )
    truth = TruthMetadata(
        cell_id=cell_id,
        true_d=int(d),
        true_tau=float(tau),
        true_cfo_hz=float(cfo_hz),
        noise_seed=noise_seed,
        tx_waveform=_readonly_complex(_tx_shaped(config, preamble)),
    )
    return visible, truth


def normalized_glrt(template: np.ndarray, received: np.ndarray) -> float:
    template_energy = float(np.vdot(template, template).real)
    received_energy = float(np.vdot(received, received).real)
    denominator = template_energy * received_energy
    if denominator <= 0.0:
        return 0.0
    value = float(abs(np.vdot(template, received)) ** 2 / denominator)
    return float(np.clip(value, 0.0, 1.0))


class _ScoreAccessor:
    def __init__(self, visible: ReceiverVisible, config: SmokeConfig, cfo_grid: Sequence[float]):
        self.visible = visible
        self.config = config
        self.cfo_grid = tuple(float(x) for x in cfo_grid)
        self.cache: dict[tuple[int, int, int], float] = {}
        self.calls = 0

    def score(self, index: tuple[int, int, int]) -> float:
        if index not in self.cache:
            di, ti, ci = index
            template = synthesize_template(
                self.config,
                self.visible.known_preamble,
                self.config.d_hypotheses[di],
                self.config.tau_hypotheses[ti],
                self.cfo_grid[ci],
            )
            self.cache[index] = normalized_glrt(template, self.visible.rx_samples)
            self.calls += 1
        return self.cache[index]

    def surface(self) -> np.ndarray:
        cube = np.empty(
            (len(self.config.d_hypotheses), len(self.config.tau_hypotheses), len(self.cfo_grid)),
            dtype=np.float64,
        )
        for index in np.ndindex(cube.shape):
            cube[index] = self.score(index)
        return cube


def _candidate(index: tuple[int, int, int], d_grid: Sequence[int], tau_grid: Sequence[float], cfo_grid: Sequence[float]) -> tuple[int, float, float]:
    return (int(d_grid[index[0]]), float(tau_grid[index[1]]), float(cfo_grid[index[2]]))


def argmax_lexicographic(
    scores: Sequence[float] | np.ndarray,
    candidates: Sequence[tuple[int, float, float]],
    tolerance: float,
) -> tuple[tuple[int, float, float], float, int]:
    values = np.asarray(scores, dtype=np.float64).reshape(-1)
    if values.size != len(candidates) or values.size == 0:
        raise ValueError("scores and candidates must be non-empty and aligned")
    maximum = float(np.max(values))
    eligible = [index for index, value in enumerate(values) if maximum - float(value) <= tolerance]
    chosen = min(eligible, key=lambda index: candidates[index])
    return candidates[chosen], float(values[chosen]), chosen


def _choose_indices(
    indices: Iterable[tuple[int, int, int]],
    get_score,
    d_grid: Sequence[int],
    tau_grid: Sequence[float],
    cfo_grid: Sequence[float],
    tolerance: float,
) -> tuple[tuple[int, int, int], float, tuple[tuple[int, int, int], ...]]:
    visited = tuple(indices)
    candidates = [_candidate(index, d_grid, tau_grid, cfo_grid) for index in visited]
    values = [get_score(index) for index in visited]
    _, score, selected = argmax_lexicographic(values, candidates, tolerance)
    return visited[selected], score, visited


def _select_b0_get(get_score, d_grid, tau_grid, cfo_grid, tolerance) -> Selection:
    zero_t = min(range(len(tau_grid)), key=lambda index: abs(float(tau_grid[index])))
    first, first_score, visit1 = _choose_indices(
        ((di, zero_t, ci) for di in range(len(d_grid)) for ci in range(len(cfo_grid))),
        get_score, d_grid, tau_grid, cfo_grid, tolerance,
    )
    selected_c = first[2]
    second, second_score, visit2 = _choose_indices(
        ((di, ti, selected_c) for di in range(len(d_grid)) for ti in range(len(tau_grid))),
        get_score, d_grid, tau_grid, cfo_grid, tolerance,
    )
    selected_t = second[1]
    c_indices = range(max(0, selected_c - 1), min(len(cfo_grid), selected_c + 2))
    third, third_score, visit3 = _choose_indices(
        ((di, selected_t, ci) for di in range(len(d_grid)) for ci in c_indices),
        get_score, d_grid, tau_grid, cfo_grid, tolerance,
    )
    return Selection(
        estimate=_candidate(third, d_grid, tau_grid, cfo_grid),
        score=third_score,
        trace_scores=(first_score, second_score, third_score),
        iterations=3,
        visited=visit1 + visit2 + visit3,
        terminal_candidates=visit3,
    )


def select_b0(cube: np.ndarray, d_grid, tau_grid, cfo_grid, tolerance: float) -> Selection:
    return _select_b0_get(lambda index: float(cube[index]), d_grid, tau_grid, cfo_grid, tolerance)


def _select_global_get(get_score, d_grid, tau_grid, cfo_grid, tolerance) -> Selection:
    chosen, score, visited = _choose_indices(
        np.ndindex((len(d_grid), len(tau_grid), len(cfo_grid))),
        get_score, d_grid, tau_grid, cfo_grid, tolerance,
    )
    return Selection(
        estimate=_candidate(chosen, d_grid, tau_grid, cfo_grid),
        score=score,
        trace_scores=(score,),
        iterations=1,
        visited=visited,
        terminal_candidates=visited,
    )


def select_b1(cube: np.ndarray, d_grid, tau_grid, cfo_grid, tolerance: float) -> Selection:
    return _select_global_get(lambda index: float(cube[index]), d_grid, tau_grid, cfo_grid, tolerance)


def select_c_grid(cube: np.ndarray, d_grid, tau_grid, cfo_grid, tolerance: float) -> Selection:
    return _select_global_get(lambda index: float(cube[index]), d_grid, tau_grid, cfo_grid, tolerance)


def _index_for_estimate(estimate, d_grid, tau_grid, cfo_grid) -> tuple[int, int, int]:
    return (list(d_grid).index(estimate[0]), list(tau_grid).index(estimate[1]), list(cfo_grid).index(estimate[2]))


def _select_b2_get(get_score, d_grid, tau_grid, cfo_grid, tolerance, initial: Selection, max_iterations: int = 8) -> Selection:
    current = _index_for_estimate(initial.estimate, d_grid, tau_grid, cfo_grid)
    current_score = get_score(current)
    trace = [current_score]
    visited: list[tuple[int, int, int]] = list(initial.visited)
    terminal_candidates = initial.terminal_candidates
    iterations = 0
    for _ in range(max_iterations):
        iterations += 1
        before = current
        tau_choice, tau_score, tau_visited = _choose_indices(
            ((current[0], ti, current[2]) for ti in range(len(tau_grid))),
            get_score, d_grid, tau_grid, cfo_grid, tolerance,
        )
        visited.extend(tau_visited)
        if tau_score >= current_score - tolerance:
            if tau_score > current_score + tolerance or _candidate(tau_choice, d_grid, tau_grid, cfo_grid) < _candidate(current, d_grid, tau_grid, cfo_grid):
                current, current_score = tau_choice, tau_score
        trace.append(current_score)
        joint_choice, joint_score, joint_visited = _choose_indices(
            ((di, current[1], ci) for di in range(len(d_grid)) for ci in range(len(cfo_grid))),
            get_score, d_grid, tau_grid, cfo_grid, tolerance,
        )
        visited.extend(joint_visited)
        terminal_candidates = joint_visited
        if joint_score >= current_score - tolerance:
            if joint_score > current_score + tolerance or _candidate(joint_choice, d_grid, tau_grid, cfo_grid) < _candidate(current, d_grid, tau_grid, cfo_grid):
                current, current_score = joint_choice, joint_score
        trace.append(current_score)
        if current == before:
            break
    return Selection(
        estimate=_candidate(current, d_grid, tau_grid, cfo_grid),
        score=current_score,
        trace_scores=tuple(trace),
        iterations=iterations,
        visited=tuple(visited),
        terminal_candidates=terminal_candidates,
    )


def select_b2(cube: np.ndarray, d_grid, tau_grid, cfo_grid, tolerance: float, initial: Selection) -> Selection:
    return _select_b2_get(lambda index: float(cube[index]), d_grid, tau_grid, cfo_grid, tolerance, initial)


def score_cube(visible: ReceiverVisible, config: SmokeConfig, cfo_grid: Sequence[float]) -> tuple[np.ndarray, list[tuple[int, float, float]], dict[str, Any]]:
    accessor = _ScoreAccessor(visible, config, cfo_grid)
    cube = accessor.surface()
    candidates = [
        _candidate(index, config.d_hypotheses, config.tau_hypotheses, cfo_grid)
        for index in np.ndindex(cube.shape)
    ]
    ledger = {
        "candidate_score_calls": accessor.calls,
        "unique_candidate_score_calls": accessor.calls,
        "complex_macs": accessor.calls * config.observation_length,
        "fft_calls": 0,
        "fft_sizes": [],
        "interpolation_calls": accessor.calls,
    }
    return cube, candidates, ledger


def _estimate_method(visible: ReceiverVisible, config: SmokeConfig, cfo_grid: Sequence[float], method: str) -> EstimateResult:
    accessor = _ScoreAccessor(visible, config, cfo_grid)
    d_grid, tau_grid = config.d_hypotheses, config.tau_hypotheses
    if method == "B0":
        selection = _select_b0_get(accessor.score, d_grid, tau_grid, cfo_grid, config.tie_tolerance)
    elif method in {"B1", "C"}:
        selection = _select_global_get(accessor.score, d_grid, tau_grid, cfo_grid, config.tie_tolerance)
    elif method == "B2":
        initial = _select_b0_get(accessor.score, d_grid, tau_grid, cfo_grid, config.tie_tolerance)
        selection = _select_b2_get(
            accessor.score,
            d_grid,
            tau_grid,
            cfo_grid,
            config.tie_tolerance,
            initial,
            config.b2_max_iterations,
        )
    else:
        raise ValueError(method)
    surface = accessor.surface() if method in {"B1", "C"} else np.array(
        sorted((index, value) for index, value in accessor.cache.items()), dtype=object
    )
    surface_hash = _sha256_bytes(
        np.ascontiguousarray(surface, dtype=np.float64).tobytes()
        if surface.dtype != object
        else json.dumps([(list(index), value) for index, value in sorted(accessor.cache.items())]).encode("utf-8")
    )
    compute = {
        "candidate_score_calls": accessor.calls,
        "unique_candidate_score_calls": accessor.calls,
        "complex_macs": accessor.calls * config.observation_length,
        "fft_calls": 0,
        "fft_sizes": [],
        "interpolation_calls": accessor.calls,
    }
    selected_index = _index_for_estimate(selection.estimate, d_grid, tau_grid, cfo_grid)
    competing_scores = [
        accessor.score(index)
        for index in dict.fromkeys(selection.terminal_candidates)
        if index != selected_index
    ]
    top1_top2_margin = (
        max(0.0, selection.score - max(competing_scores))
        if competing_scores
        else float("inf")
    )
    return EstimateResult(
        method=method,
        estimate=selection.estimate,
        score=selection.score,
        trace_scores=selection.trace_scores,
        iterations=selection.iterations,
        realization_id=visible.realization_id,
        rx_sha256=visible.rx_sha256,
        grid_hash=visible.grid_hash,
        score_hash=visible.score_hash,
        surface_hash=surface_hash,
        compute=compute,
        visited_candidate_indices=selection.visited,
        top1_top2_margin=top1_top2_margin,
    )


def estimate_all(visible: ReceiverVisible, config: SmokeConfig, cfo_grid: Sequence[float]) -> dict[str, EstimateResult]:
    return {method: _estimate_method(visible, config, cfo_grid, method) for method in ("B0", "B1", "B2", "C")}


def estimate_method(visible: ReceiverVisible, config: SmokeConfig, cfo_grid: Sequence[float], method: str) -> EstimateResult:
    """Run one standalone method with its own lazy common-score evaluator."""
    return _estimate_method(visible, config, cfo_grid, method)


def acquisition_metrics(
    truth: Sequence[tuple[int, float, float]],
    estimates: dict[str, Sequence[tuple[int, float, float]]],
) -> dict[str, Any]:
    count = len(truth)
    if count == 0 or any(len(values) != count for values in estimates.values()):
        raise ValueError("complete aligned population required")
    methods: dict[str, Any] = {}
    false_counts: dict[str, int] = {}
    for method, values in estimates.items():
        false_count = sum(tuple(estimate) != tuple(target) for estimate, target in zip(values, truth))
        false_counts[method] = int(false_count)
        rate = false_count / count
        methods[method] = {
            "population": count,
            "false_lock_count": int(false_count),
            "false_lock_rate": rate,
            "acquisition_success": 1.0 - rate,
            "miss": None,
        }
    b0 = false_counts["B0"]
    c = false_counts["C"]
    if b0 == 0:
        g_c = 0.0
        coverage = {"B1": None, "B2": None}
    else:
        g_c = (b0 - c) / b0
        denominator = b0 - c
        coverage = {
            method: None if denominator <= 0 else (b0 - false_counts[method]) / denominator
            for method in ("B1", "B2")
        }
    return {"methods": methods, "g_c": g_c, "coverage": coverage}


def find_stable_2x2(records: Sequence[dict[str, Any]], tau_grid: Sequence[float], cfo_grid: Sequence[float]) -> dict[str, Any]:
    regions: list[dict[str, Any]] = []
    groups = sorted({(record["d"], record["layer"]) for record in records})
    by_key = {(record["d"], record["layer"], record["tau"], record["cfo_hz"]): record for record in records}
    for d, layer in groups:
        for ti in range(len(tau_grid) - 1):
            for ci in range(len(cfo_grid) - 1):
                cells = [
                    by_key.get((d, layer, tau_grid[tj], cfo_grid[cj]))
                    for tj, cj in ((ti, ci), (ti + 1, ci), (ti, ci + 1), (ti + 1, ci + 1))
                ]
                if any(cell is None for cell in cells):
                    continue
                labels = [tuple(cell["estimate"]) for cell in cells]
                targets = [(d, float(cell["tau"]), float(cell["cfo_hz"])) for cell in cells]
                if len(set(labels)) == 1 and all(label != target for label, target in zip(labels, targets)):
                    regions.append(
                        {
                            "d": d,
                            "layer": layer,
                            "tau": [float(tau_grid[ti]), float(tau_grid[ti + 1])],
                            "cfo_hz": [float(cfo_grid[ci]), float(cfo_grid[ci + 1])],
                            "wrong_basin": list(labels[0]),
                        }
                    )
    return {"found": bool(regions), "regions": regions}


def additive_interaction_residual(surface: np.ndarray) -> float:
    values = np.asarray(surface, dtype=np.float64)
    fitted = values.mean(axis=1, keepdims=True) + values.mean(axis=0, keepdims=True) - values.mean()
    residual = np.linalg.norm(values - fitted)
    denominator = max(np.linalg.norm(values - values.mean()), np.finfo(float).eps)
    return float(residual / denominator)


def reduce_terminal(
    *,
    semantic_gates_pass: bool,
    complete_population: bool,
    b0_false_locks: int,
    b1_c_equivalent: bool,
    exact_separable: bool,
    analytic_nonseparable: bool,
    surface_nonseparable: bool,
    stable_region: bool,
    g_c: float | None,
    coverage_b1: float | None,
    coverage_b2: float | None,
) -> str:
    if not semantic_gates_pass:
        return "SEMANTIC_INVALID"
    if not complete_population:
        return "STEP4A_PREFLIGHT_EVIDENCE_GAP"
    if (
        b0_false_locks == 0
        or b1_c_equivalent
        or exact_separable
        or not stable_region
        or g_c is None
        or g_c < 0.05
        or (coverage_b1 is not None and coverage_b1 >= 0.95)
        or (coverage_b2 is not None and coverage_b2 >= 0.95)
    ):
        return "STEP4A_PREFLIGHT_KILL_OR_PIVOT"
    if (
        analytic_nonseparable
        and surface_nonseparable
        and stable_region
        and g_c >= 0.05
        and coverage_b1 is not None
        and coverage_b2 is not None
        and coverage_b1 < 0.95
        and coverage_b2 < 0.95
    ):
        return "STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE"
    return "STEP4A_PREFLIGHT_EVIDENCE_GAP"


def reduce_residual_layers(
    layer_inputs: dict[str, dict[str, Any]],
    *,
    stress_diagnostic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Reduce residual layers only; stress is accepted solely as an audit sentinel."""
    _ = stress_diagnostic
    per_layer = {layer: reduce_terminal(**values) for layer, values in layer_inputs.items()}
    if "SEMANTIC_INVALID" in per_layer.values():
        terminal = "SEMANTIC_INVALID"
    elif "STEP4A_PREFLIGHT_KILL_OR_PIVOT" in per_layer.values():
        terminal = "STEP4A_PREFLIGHT_KILL_OR_PIVOT"
    elif set(per_layer.values()) == {"STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE"}:
        terminal = "STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE"
    else:
        terminal = "STEP4A_PREFLIGHT_EVIDENCE_GAP"
    return {"terminal": terminal, "per_layer_terminals": per_layer}


def build_manifest(config: SmokeConfig) -> dict[str, Any]:
    manifest = {
        "schema_version": "oversampled-sync-q1.semantic-smoke.v1",
        "classification": "GROUNDWORK_STEP4A_SEMANTIC_SMOKE",
        "evidence_ceiling": "DIAGNOSTIC_ONLY_NOT_PAPER_NUMBER",
        "waveform": {
            "symbol_rate_hz": config.symbol_rate_hz,
            "sps": config.sps,
            "sample_rate_hz": config.sample_rate_hz,
            "modulation": config.modulation,
            "rrc_beta": config.rrc_beta,
            "rrc_span_symbols": config.rrc_span_symbols,
            "rrc_span_status": "implementation_sentinel",
            "preamble_symbols": config.preamble_symbols,
            "preamble_status": "fixed_seed_diagnostic_exact_literature_sequence_unavailable",
            "tx_filtering": "full_convolution",
            "rx_matched_filtering": "full_convolution",
        },
        "reference_plane": {
            "aggregate_group_delay_samples": config.aggregate_group_delay_samples,
            "d_zero": "TX-shaped waveform starts at frame_guard before RX matched filtering",
            "fractional_delay_sign": "positive tau delays y[n]=x[n-tau]",
            "cfo_sign": "positive CFO multiplies exp(+j2*pi*f*n/Fs)",
        },
        "observation_window": {
            "length": config.observation_length,
            "frame_guard_samples_each_side": config.frame_guard_samples,
            "crop": "none_after_full_RX_convolution",
        },
        "truth_population": {
            "d_samples": list(config.d_truth),
            "tau_samples": list(config.tau_truth),
            "residual_cfo_hz": list(config.residual_cfo_truth_hz),
            "stress_cfo_hz": list(config.stress_cfo_truth_hz),
            "residual_cells_per_layer": len(config.d_truth) * len(config.tau_truth) * len(config.residual_cfo_truth_hz),
            "stress_cells": len(config.d_truth) * len(config.tau_truth) * len(config.stress_cfo_truth_hz),
        },
        "hypotheses": {
            "d_samples": list(config.d_hypotheses),
            "tau_samples": list(config.tau_hypotheses),
            "residual_cfo_hz": list(config.residual_cfo_hypotheses_hz),
            "stress_cfo_hz": list(config.stress_cfo_hypotheses_hz),
        },
        "layers": {
            "noiseless": "semantic identity/surface",
            "minus6db": "deterministic AWGN numerical-stress sentinel, not occurrence distribution",
            "minus6db_snr_db": config.diagnostic_snr_db,
        },
        "seeds": {"preamble": config.preamble_seed, "awgn_master": config.awgn_master_seed, "cell_derivation": "first64bits(SHA256(master_seed|cell_id))"},
        "score": {
            "identity": SCORE_IDENTITY,
            "formula": SCORE_FORMULA,
            "complex_gain": "profiled",
            "normalization": "template-energy times received-window-energy",
            "tie_tolerance": config.tie_tolerance,
            "tie_break": "lexicographically smallest (d,tau,cfo) inside tolerance",
            "score_hash": _score_hash(config),
        },
        "methods": {
            "B0": "coarse-CFO then timing then frame/adjacent-fine-CFO; discarded tau branches not revisited",
            "B1": "complete timing bank over the complete common (d,CFO) grid and global terminal score",
            "B2": "B0 initialization; tau then joint (d,CFO) non-decreasing coordinate updates; fixed point or 8 iterations",
            "C": "receiver-visible complete common 3-D grid global argmax; no truth and no continuous refinement",
        },
        "information_contract": {
            "receiver_visible": ["rx_samples", "known_preamble", "sample_rate_and_rrc", "frozen_search_grid", "common_score", "tie_break", "B2_stop_rule"],
            "truth_scoring_only": ["true_d", "true_tau", "true_cfo_hz", "noise_seed", "tx_waveform"],
            "forbidden_in_method": ["payload_truth", "true_alignment", "oracle_rotation", "truth_selected_grid_or_branch"],
        },
        "metric": {"primary": "wrong_basin_false_lock_rate", "success": "1-R_FL", "miss": None, "stress_pooling": False},
        "compute": {
            "candidate_score_calls": "unique cache-miss candidate evaluations; not traversal visits",
            "visited_candidate_indices": "ordered traversal ledger with repeated visits preserved",
            "complex_macs": "one complex inner-product MAC per observation sample per newly scored candidate",
            "fft": "calls/sizes separate; none used",
            "interpolation": "one diagnostic fractional-delay interpolation per newly scored candidate",
            "wall_time": "warm-up then five same-process calls; median plus raw",
        },
    }
    manifest["manifest_sha256"] = _canonical_hash(manifest)
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    required = {
        "schema_version", "classification", "evidence_ceiling", "waveform", "reference_plane",
        "observation_window", "truth_population", "hypotheses", "layers", "seeds", "score",
        "methods", "information_contract", "metric", "compute", "manifest_sha256",
    }
    missing = required - manifest.keys()
    if missing:
        raise ValueError(f"manifest missing {sorted(missing)}")
    copy = dict(manifest)
    claimed = copy.pop("manifest_sha256")
    if claimed != _canonical_hash(copy):
        raise ValueError("manifest hash mismatch")
    if set(manifest["methods"]) != {"B0", "B1", "B2", "C"}:
        raise ValueError("method identity drift")


def validate_output_dir(output_dir: Path | str, probe_dir: Path | str) -> Path:
    output = Path(output_dir).resolve()
    root = Path(probe_dir).resolve()
    if output != root and root not in output.parents:
        raise ValueError("output path must be inside the Probe directory")
    return output


def validate_artifact_references(observations: Sequence[dict[str, Any]], truth: Sequence[dict[str, Any]], methods: Sequence[dict[str, Any]]) -> None:
    obs_by_cell = {row["cell_id"]: row for row in observations}
    truth_cells = {row["cell_id"] for row in truth}
    if set(obs_by_cell) != truth_cells:
        raise ValueError("observation/truth cell mismatch")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in methods:
        grouped.setdefault(row["cell_id"], []).append(row)
    if set(grouped) != set(obs_by_cell):
        raise ValueError("method cell mismatch")
    for cell_id, rows in grouped.items():
        if {row["method"] for row in rows} != {"B0", "B1", "B2", "C"}:
            raise ValueError(f"method cardinality mismatch for {cell_id}")
        obs = obs_by_cell[cell_id]
        for row in rows:
            if row["realization_id"] != obs["realization_id"] or row["rx_sha256"] != obs["rx_sha256"]:
                raise ValueError(f"paired realization mismatch for {cell_id}")
            if not row.get("grid_hash") or not row.get("score_hash"):
                raise ValueError(f"missing grid/score hash for {cell_id}")


def config_as_jsonable(config: SmokeConfig) -> dict[str, Any]:
    return dataclasses.asdict(config)
