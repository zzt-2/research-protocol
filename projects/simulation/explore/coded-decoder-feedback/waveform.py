"""Registered D0 prefix, pilots, waveform layout, and controlled rotation.

This module is deliberately pure: importing it performs no I/O and consumes no
global random state.  Every returned array is a defensive, read-only copy.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
import math

import numpy as np


_PREFIX_SYMBOLS = 32
_DATA_SYMBOLS = 6144
_REGISTERED_PILOT_PERIODS = frozenset({10, 20, 100, 200})
_CONTROLLED_BOUNDARIES = frozenset({1536, 3072, 4608})
_GRAY_AXIS = np.array([-3.0, -1.0, 3.0, 1.0], dtype=np.float64)
_LABEL_WEIGHTS = np.array([8, 4, 2, 1], dtype=np.uint8)
_ROTATIONS = (
    np.complex128(1.0 + 0.0j),
    np.complex128(0.0 + 1.0j),
    np.complex128(-1.0 + 0.0j),
    np.complex128(0.0 - 1.0j),
)


def _readonly_copy(value: np.ndarray, *, dtype: np.dtype | type | None = None) -> np.ndarray:
    result = np.array(value, dtype=dtype, order="C", copy=True)
    result.setflags(write=False)
    return result


class WaveformError(ValueError):
    """Raised when a registered waveform contract is violated."""


@dataclass(frozen=True, slots=True)
class PrefixAsset:
    bits: np.ndarray
    labels: np.ndarray
    symbols: np.ndarray
    even_symbols: np.ndarray
    odd_symbols: np.ndarray
    sample_mean_energy: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "bits", _readonly_copy(self.bits, dtype=np.uint8))
        object.__setattr__(self, "labels", _readonly_copy(self.labels, dtype=np.uint8))
        object.__setattr__(self, "symbols", _readonly_copy(self.symbols, dtype=np.complex128))
        object.__setattr__(
            self, "even_symbols", _readonly_copy(self.even_symbols, dtype=np.complex128)
        )
        object.__setattr__(
            self, "odd_symbols", _readonly_copy(self.odd_symbols, dtype=np.complex128)
        )


@dataclass(frozen=True, slots=True)
class PilotAsset:
    N: int
    cycle: np.ndarray
    expanded: np.ndarray
    pilot_count: int
    total_symbols: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "cycle", _readonly_copy(self.cycle, dtype=np.complex128))
        object.__setattr__(
            self, "expanded", _readonly_copy(self.expanded, dtype=np.complex128)
        )


def _registered_layout_references(
    N: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Build the owner-derived known schedule and exact rank/time maps."""

    _validate_pilot_period(N)
    prefix = registered_prefix()
    pilots = registered_pilots(N)
    total = pilots.total_symbols
    known_symbols = np.zeros((2, total), dtype=np.complex128)
    known_mask = np.zeros(total, dtype=np.bool_)
    data_to_time = np.empty(_DATA_SYMBOLS, dtype=np.int64)
    time_to_data = np.full(total, -1, dtype=np.int64)

    known_symbols[:, :_PREFIX_SYMBOLS] = prefix.symbols
    known_mask[:_PREFIX_SYMBOLS] = True
    time_index = _PREFIX_SYMBOLS
    data_rank = 0
    pilot_rank = 0
    while data_rank < _DATA_SYMBOLS:
        known_symbols[:, time_index] = pilots.expanded[pilot_rank]
        known_mask[time_index] = True
        time_index += 1
        pilot_rank += 1
        take = min(N - 1, _DATA_SYMBOLS - data_rank)
        stop_rank = data_rank + take
        stop_time = time_index + take
        data_to_time[data_rank:stop_rank] = np.arange(
            time_index, stop_time, dtype=np.int64
        )
        time_to_data[time_index:stop_time] = np.arange(
            data_rank, stop_rank, dtype=np.int64
        )
        data_rank = stop_rank
        time_index = stop_time

    known_symbols[:, time_index] = pilots.expanded[pilot_rank]
    known_mask[time_index] = True
    time_index += 1
    pilot_rank += 1
    if time_index != total or pilot_rank != pilots.pilot_count:
        raise AssertionError("registered pilot layout cardinality drift")
    return known_symbols, known_mask, data_to_time, time_to_data


@dataclass(frozen=True, slots=True)
class WaveformBuild:
    waveform: np.ndarray
    known_symbols: np.ndarray
    known_mask: np.ndarray
    data_to_time: np.ndarray
    time_to_data: np.ndarray
    N: int

    def __post_init__(self) -> None:
        dtype_by_name = {
            "waveform": np.complex128,
            "known_symbols": np.complex128,
            "known_mask": np.bool_,
            "data_to_time": np.int64,
            "time_to_data": np.int64,
        }
        for field in fields(self):
            if field.name in dtype_by_name:
                object.__setattr__(
                    self,
                    field.name,
                    _readonly_copy(getattr(self, field.name), dtype=dtype_by_name[field.name]),
                )
        expected_known, expected_mask, expected_data_to_time, expected_time_to_data = (
            _registered_layout_references(self.N)
        )
        total = expected_time_to_data.size
        if self.waveform.shape != (2, total):
            raise WaveformError(f"waveform must have shape (2, {total})")
        if self.known_symbols.shape != (2, total):
            raise WaveformError(f"known_symbols must have shape (2, {total})")
        if self.known_mask.shape != (total,):
            raise WaveformError(f"known_mask must have shape ({total},)")
        if self.data_to_time.shape != (_DATA_SYMBOLS,):
            raise WaveformError("data_to_time must have shape (6144,)")
        if self.time_to_data.shape != (total,):
            raise WaveformError(f"time_to_data must have shape ({total},)")
        if not np.all(np.isfinite(self.waveform)):
            raise WaveformError("waveform must contain only finite samples")
        if not np.all(np.isfinite(self.known_symbols)):
            raise WaveformError("known_symbols must contain only finite samples")
        if not np.array_equal(self.data_to_time, expected_data_to_time):
            raise WaveformError("data_to_time is not the registered 6144-rank map")
        if not np.array_equal(self.time_to_data, expected_time_to_data):
            raise WaveformError("time_to_data is not the registered inverse map")
        if not np.array_equal(self.known_mask, expected_mask):
            raise WaveformError("known_mask is not the registered known schedule")
        if not np.array_equal(self.known_symbols, expected_known):
            raise WaveformError("known_symbols do not match registered references")


def registered_prefix() -> PrefixAsset:
    """Generate the owner-registered 32-symbol Gray-16QAM prefix."""

    generator = np.random.Generator(np.random.PCG64(987654321))
    bits = generator.integers(0, 2, size=(_PREFIX_SYMBOLS, 4), dtype=np.int64).astype(
        np.uint8
    )
    labels = (bits @ _LABEL_WEIGHTS).astype(np.uint8)
    symbols = (
        _GRAY_AXIS[labels >> np.uint8(2)]
        + 1j * _GRAY_AXIS[labels & np.uint8(3)]
    ).astype(np.complex128) / np.sqrt(10.0)
    return PrefixAsset(
        bits=bits,
        labels=labels,
        symbols=symbols,
        even_symbols=symbols[0::2],
        odd_symbols=symbols[1::2],
        sample_mean_energy=float(np.mean(np.abs(symbols) ** 2)),
    )


def _validate_pilot_period(N: int) -> None:
    if not isinstance(N, int) or isinstance(N, bool) or N not in _REGISTERED_PILOT_PERIODS:
        raise WaveformError(f"N must be one of {sorted(_REGISTERED_PILOT_PERIODS)}")


def registered_pilots(N: int) -> PilotAsset:
    """Generate the registered unit-energy QPSK pilot cycle and expansion."""

    _validate_pilot_period(N)
    cycle = np.array(
        [1.0 + 1.0j, 1.0 - 1.0j, -1.0 + 1.0j, -1.0 - 1.0j],
        dtype=np.complex128,
    ) / np.sqrt(2.0)
    pilot_count = 1 + math.ceil(_DATA_SYMBOLS / (N - 1))
    expanded = cycle[np.arange(pilot_count, dtype=np.int64) % cycle.size]
    return PilotAsset(
        N=N,
        cycle=cycle,
        expanded=expanded,
        pilot_count=pilot_count,
        total_symbols=_PREFIX_SYMBOLS + _DATA_SYMBOLS + pilot_count,
    )


def build_waveform(data_symbols: np.ndarray, *, N: int) -> WaveformBuild:
    """Extend two 6144-symbol polarizations without replacing coded data."""

    _validate_pilot_period(N)
    data = np.asarray(data_symbols)
    if data.shape != (2, _DATA_SYMBOLS):
        raise WaveformError("data_symbols must have shape (2, 6144)")
    if not np.issubdtype(data.dtype, np.number) or not np.all(np.isfinite(data)):
        raise WaveformError("data_symbols must be finite numeric values")
    data = np.array(data, dtype=np.complex128, order="C", copy=True)

    prefix = registered_prefix()
    pilots = registered_pilots(N)
    total = pilots.total_symbols
    samples = np.empty((2, total), dtype=np.complex128)
    known_symbols = np.zeros((2, total), dtype=np.complex128)
    known_mask = np.zeros(total, dtype=np.bool_)
    data_to_time = np.empty(_DATA_SYMBOLS, dtype=np.int64)
    time_to_data = np.full(total, -1, dtype=np.int64)

    samples[:, :_PREFIX_SYMBOLS] = prefix.symbols
    known_symbols[:, :_PREFIX_SYMBOLS] = prefix.symbols
    known_mask[:_PREFIX_SYMBOLS] = True

    time_index = _PREFIX_SYMBOLS
    data_rank = 0
    pilot_rank = 0
    while data_rank < _DATA_SYMBOLS:
        pilot = pilots.expanded[pilot_rank]
        samples[:, time_index] = pilot
        known_symbols[:, time_index] = pilot
        known_mask[time_index] = True
        time_index += 1
        pilot_rank += 1

        take = min(N - 1, _DATA_SYMBOLS - data_rank)
        stop_rank = data_rank + take
        stop_time = time_index + take
        samples[:, time_index:stop_time] = data[:, data_rank:stop_rank]
        absolute_times = np.arange(time_index, stop_time, dtype=np.int64)
        data_to_time[data_rank:stop_rank] = absolute_times
        time_to_data[time_index:stop_time] = np.arange(
            data_rank, stop_rank, dtype=np.int64
        )
        data_rank = stop_rank
        time_index = stop_time

    terminal = pilots.expanded[pilot_rank]
    samples[:, time_index] = terminal
    known_symbols[:, time_index] = terminal
    known_mask[time_index] = True
    time_index += 1
    pilot_rank += 1
    if time_index != total or pilot_rank != pilots.pilot_count:
        raise AssertionError("registered pilot layout cardinality drift")

    return WaveformBuild(
        waveform=samples,
        known_symbols=known_symbols,
        known_mask=known_mask,
        data_to_time=data_to_time,
        time_to_data=time_to_data,
        N=N,
    )


def apply_persistent_rotation(
    build: WaveformBuild,
    *,
    target_pol: int,
    boundary_after_data: int,
    k: int,
) -> WaveformBuild:
    """Copy and rotate one physical suffix, including all later pilots."""

    if not isinstance(build, WaveformBuild):
        raise TypeError("build must be a WaveformBuild")
    if not isinstance(target_pol, int) or isinstance(target_pol, bool) or target_pol not in (0, 1):
        raise WaveformError("target_pol must be 0 or 1")
    if (
        not isinstance(boundary_after_data, int)
        or isinstance(boundary_after_data, bool)
        or boundary_after_data not in _CONTROLLED_BOUNDARIES
    ):
        raise WaveformError("boundary_after_data must be 1536, 3072, or 4608")
    if not isinstance(k, int) or isinstance(k, bool) or k not in (0, 1, 2, 3):
        raise WaveformError("k must be an integer state in {0,1,2,3}")

    boundary_time = int(build.data_to_time[boundary_after_data])
    rotated = np.array(build.waveform, dtype=np.complex128, order="C", copy=True)
    rotated[target_pol, boundary_time:] *= _ROTATIONS[k]
    return WaveformBuild(
        waveform=rotated,
        known_symbols=build.known_symbols,
        known_mask=build.known_mask,
        data_to_time=build.data_to_time,
        time_to_data=build.time_to_data,
        N=build.N,
    )
