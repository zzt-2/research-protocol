"""Frozen D0 contract control, population, and seed identities.

This leaf module performs no I/O at import time.  The only file read happens
through :func:`load_contract`, so callers choose the owner explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping

import numpy as np
import yaml


class ContractError(ValueError):
    """Raised when the machine-owned D0 contract is malformed."""


_EXPECTED_CODE_IDENTITY = ("5g_ldpc_bg2", 1024, 1536, 16, 384, 6144, 20)
_EXPECTED_WAVEFORM_IDENTITIES = {
    10: (684, 6860),
    20: (325, 6501),
    100: (64, 6240),
    200: (32, 6208),
}


class _StrictLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _StrictLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ContractError(f"unhashable YAML key: {key!r}") from exc
        if duplicate:
            raise ContractError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True, slots=True)
class ControlContract:
    topic: str
    epoch: int
    checkpoint: str
    action_class: str
    decision: str
    verification: str
    implementation_authorized: bool
    unit_test_authorized: bool
    engineering_benchmark_authorized: bool
    execution_authorized: bool
    scientific_experiment_authorized: bool


@dataclass(frozen=True, slots=True)
class CodeLayout:
    family: str
    information_bits_per_cw: int
    transmitted_bits_per_cw: int
    codewords_per_polarization: int
    data_symbols_per_cw: int
    data_symbols_per_polarization: int
    decoder_iterations: int


@dataclass(frozen=True, slots=True)
class WaveformLayout:
    prefix_symbols: int
    pilot_period_symbols: int
    data_symbols_per_polarization: int
    total_symbols_per_polarization: int

    def __post_init__(self) -> None:
        values = (
            self.prefix_symbols,
            self.pilot_period_symbols,
            self.data_symbols_per_polarization,
            self.total_symbols_per_polarization,
        )
        if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in values):
            raise ContractError("waveform layout values must be positive integers")


@dataclass(frozen=True, slots=True)
class Float64Literal:
    """An indexed canonical binary64 literal used by owner identity anchors."""

    index: int
    float64_hex: str


def _assert_plain_ndarray(value: np.ndarray) -> None:
    dtype = value.dtype
    if (
        dtype.hasobject
        or dtype.fields is not None
        or not (np.issubdtype(dtype, np.number) or np.issubdtype(dtype, np.bool_))
    ):
        raise ContractError("ndarray must use a plain numeric or bool dtype")


class _FrozenDict(tuple, Mapping[str, Any]):
    """Tuple-backed immutable mapping used only for already-frozen trees."""

    def __new__(cls, items: Any) -> _FrozenDict:
        return tuple.__new__(cls, tuple(items))

    def __iter__(self):
        return (key for key, _ in tuple.__iter__(self))

    def __getitem__(self, key: str) -> Any:
        for item_key, value in tuple.__iter__(self):
            if item_key == key:
                return value
        raise KeyError(key)

    def __len__(self) -> int:
        return tuple.__len__(self)

    def __contains__(self, key: object) -> bool:
        return any(item_key == key for item_key, _ in tuple.__iter__(self))


def _deep_freeze(value: Any, active: set[int] | None = None) -> Any:
    """Detach a plain immutable tree and reject opaque object references."""

    value_type = type(value)
    if value_type in (CodeLayout, WaveformLayout, Float64Literal):
        return value
    if value_type is np.ndarray:
        _assert_plain_ndarray(value)
        frozen = np.array(value, copy=True)
        frozen.setflags(write=False)
        return frozen
    if isinstance(value, np.generic):
        scalar = np.asarray(value)
        _assert_plain_ndarray(scalar)
        return _deep_freeze(value.item(), active)
    if value_type in (str, bytes, int, float, complex, bool, type(None)):
        return value

    if active is None:
        active = set()
    is_container = value_type in (dict, list, tuple, set, frozenset, _FrozenDict)
    if is_container:
        identity = id(value)
        if identity in active:
            raise ContractError("cyclic receipt/container values are not allowed")
        active.add(identity)
        try:
            if value_type in (dict, _FrozenDict):
                frozen_items = []
                for key, item in value.items():
                    if type(key) is not str:
                        raise ContractError(
                            "closed-world mapping keys must be exact strings"
                        )
                    frozen_items.append((key, _deep_freeze(item, active)))
                return _FrozenDict(frozen_items)
            if value_type in (list, tuple):
                return tuple(_deep_freeze(item, active) for item in value)
            return frozenset(
                _deep_freeze(item, active) for item in value
            )
        finally:
            active.remove(identity)

    raise ContractError(
        f"closed-world immutable tree rejects type {value_type.__name__}"
    )


_TRUTH_ALIASES = frozenset(
    {
        "truth",
        "truth_view",
        "tx_payload",
        "tx_bits",
        "information_bits",
        "coded_bits",
        "transmitted_bits",
        "transmitted_symbols",
        "true_phase",
        "true_cfo",
        "h",
        "channel_h",
        "snr",
        "true_snr",
        "physical_snr",
        "physical_snr_db",
        "physical_noise",
        "physical_noise_power",
        "complex_noise_power",
        "noise_power",
        "noise_variance",
        "fade",
        "true_fade",
        "slip",
        "slip_boundary",
        "true_rotation",
        "event",
        "event_label",
        "event_fixture",
        "injected_event_label",
        "natural_event_label",
        "correctness",
        "final_correctness",
        "final_codeword_correctness",
    }
)


def _normalized_name(value: str) -> str:
    separated = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", value.strip())
    separated = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", separated)
    separated = re.sub(r"(?<=[A-Za-z])(?=[0-9])|(?<=[0-9])(?=[A-Za-z])", "_", separated)
    return re.sub(r"[^a-z0-9]+", "_", separated.lower()).strip("_")


_SAFE_RECEIVER_NAMES = frozenset(
    {
        "received_samples",
        "equalized_samples",
        "known_prefix",
        "periodic_pilots",
        "receiver_noise_estimate",
        "receiver_noise_estimator_id",
        "receiver_noise_estimate_per_pol",
        "common_cpr_phase_trace",
        "global_rotation_state",
        "bps_state",
        "source_sha256",
        "code_sha256",
        "content_sha256",
        "channel_source_sha256",
    }
)


def _is_truth_alias_name(value: str) -> bool:
    normalized = _normalized_name(value)
    if normalized in _SAFE_RECEIVER_NAMES:
        return False
    if normalized in _TRUTH_ALIASES:
        return True
    tokens = frozenset(token for token in normalized.split("_") if token)
    compact = "".join(tokens)

    # TX payload/data taxonomy.
    bits = {"bit", "bits"}
    symbols = {"symbol", "symbols"}
    if "payload" in tokens:
        return True
    if tokens.intersection({"info", "information"}) and tokens.intersection(bits):
        return True
    if "coded" in tokens and tokens.intersection(bits):
        return True
    if "data" in tokens and tokens.intersection(symbols):
        return True
    if tokens.intersection({"tx", "transmitted"}) and tokens.intersection(
        bits | symbols | {"info", "information", "coded", "data", "payload"}
    ):
        return True

    # Physical-truth taxonomy.
    if tokens.intersection(
        {
            "physical",
            "true",
            "actual",
            "oracle",
            "snr",
            "cfo",
            "fade",
            "noise",
            "awgn",
            "variance",
            "sample",
            "samples",
        }
    ) or compact.startswith("n0"):
        return True
    if "noise" in tokens and tokens.intersection(
        {"physical", "true", "actual", "oracle", "power", "variance"}
    ):
        return True
    if normalized == "h":
        return True
    if "channel" in tokens and tokens.intersection(
        {
            "true",
            "physical",
            "actual",
            "oracle",
            "realization",
            "gain",
            "coefficient",
            "response",
            "state",
            "fade",
            "h",
        }
    ):
        return True
    if "phase" in tokens and tokens.intersection(
        {"truth", "true", "physical", "channel", "oracle", "actual"}
    ):
        return True

    # Injected/natural event and slip taxonomy.
    if tokens.intersection({"slip", "event"}):
        return True
    if tokens.intersection({"injected", "injection", "natural"}) and tokens.intersection(
        {"label", "fixture", "boundary", "rotation", "event"}
    ):
        return True

    # Final correctness taxonomy.
    if tokens.intersection({"correct", "correctness"}):
        return True
    if "final" in tokens and tokens.intersection(
        {"cw", "codeword", "frame", "bit", "bits"}
    ) and tokens.intersection(
        {"error", "errors", "status", "correct", "correctness"}
    ):
        return True
    return False


def _assert_receiver_truth_free(value: Any, path: str, seen: set[int] | None = None) -> None:
    if seen is None:
        seen = set()
    if type(value) in (CodeLayout, WaveformLayout):
        return
    has_slots = any("__slots__" in cls.__dict__ for cls in type(value).__mro__)
    has_dict = hasattr(value, "__dict__")
    if isinstance(value, (Mapping, list, tuple, set, frozenset)) or (
        is_dataclass(value) and not isinstance(value, type)
    ) or has_slots or has_dict:
        identity = id(value)
        if identity in seen:
            return
        seen.add(identity)
    if isinstance(value, np.ndarray):
        _assert_plain_ndarray(value)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and _is_truth_alias_name(key):
                raise ContractError(f"receiver truth alias rejected at {path}.{key}")
            _assert_receiver_truth_free(item, f"{path}.{key}", seen)
    elif is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            if _is_truth_alias_name(field.name):
                raise ContractError(
                    f"receiver truth alias rejected at {path}.{field.name}"
                )
            _assert_receiver_truth_free(
                getattr(value, field.name), f"{path}.{field.name}", seen
            )
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            _assert_receiver_truth_free(item, f"{path}[{index}]", seen)
    else:
        slot_names: list[str] = []
        for cls in type(value).__mro__:
            slots = cls.__dict__.get("__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            slot_names.extend(name for name in slots if isinstance(name, str))
        for name in dict.fromkeys(slot_names):
            if name in {"__dict__", "__weakref__"} or not hasattr(value, name):
                continue
            if _is_truth_alias_name(name):
                raise ContractError(f"receiver truth alias rejected at {path}.{name}")
            _assert_receiver_truth_free(getattr(value, name), f"{path}.{name}", seen)
        if has_dict:
            for name, item in vars(value).items():
                if isinstance(name, str) and _is_truth_alias_name(name):
                    raise ContractError(f"receiver truth alias rejected at {path}.{name}")
                _assert_receiver_truth_free(item, f"{path}.{name}", seen)


def _exact_binary_uint8(value: Any, shape: tuple[int, ...], name: str) -> np.ndarray:
    if type(value) is not np.ndarray or value.dtype != np.dtype(np.uint8):
        raise ContractError(f"{name} must be an exact uint8 ndarray")
    if value.shape != shape:
        raise ContractError(f"{name} must have shape {shape}")
    if not np.all((value == 0) | (value == 1)):
        raise ContractError(f"{name} must be binary")
    return _deep_freeze(value)


def _finite_array(value: Any, shape: tuple[int, ...], name: str) -> np.ndarray:
    if type(value) is not np.ndarray:
        raise ContractError(f"{name} must be an exact ndarray")
    _assert_plain_ndarray(value)
    if value.shape != shape or not np.issubdtype(value.dtype, np.number):
        raise ContractError(f"{name} must be numeric with shape {shape}")
    if not np.all(np.isfinite(value)):
        raise ContractError(f"{name} must contain only finite values")
    return _deep_freeze(value)


def _assert_exact_code_layout(value: Any) -> None:
    if type(value) is not CodeLayout:
        raise ContractError("code layout must be the exact CodeLayout type")
    observed = tuple(getattr(value, field.name) for field in fields(CodeLayout))
    if observed != _EXPECTED_CODE_IDENTITY or any(
        type(item) is not expected
        for item, expected in zip(observed, (str, int, int, int, int, int, int), strict=True)
    ):
        raise ContractError("code layout is not the frozen D0 identity")


@dataclass(frozen=True, slots=True)
class PayloadTruth:
    information_bits: np.ndarray
    coded_bits: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "information_bits",
            _exact_binary_uint8(self.information_bits, (2, 16, 1024), "information_bits"),
        )
        object.__setattr__(
            self, "coded_bits",
            _exact_binary_uint8(self.coded_bits, (2, 16, 1536), "coded_bits"),
        )


@dataclass(frozen=True, slots=True)
class CostLedger:
    decoder_batches: int
    codeword_decodes: int
    bp_iterations: int
    receipts: Mapping[str, Any]

    def __post_init__(self) -> None:
        counts = (self.decoder_batches, self.codeword_decodes, self.bp_iterations)
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in counts):
            raise ContractError("cost ledger counts must be non-negative integers")
        object.__setattr__(self, "receipts", _deep_freeze(self.receipts))


@dataclass(frozen=True, slots=True)
class ResolvedDevFreeze:
    freeze_id: str
    parameters: Mapping[str, Any]
    receipts: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.freeze_id, str) or not self.freeze_id:
            raise ContractError("resolved dev freeze id must be non-empty")
        object.__setattr__(self, "parameters", _deep_freeze(self.parameters))
        object.__setattr__(self, "receipts", _deep_freeze(self.receipts))


@dataclass(frozen=True, slots=True)
class ReceiverView:
    received_samples: np.ndarray
    equalized_samples: np.ndarray
    common_cpr_phase_trace: np.ndarray
    known_prefix: np.ndarray
    periodic_pilots: np.ndarray
    receiver_noise_estimate: np.ndarray = field(init=False)
    code_layout: CodeLayout
    waveform_layout: WaveformLayout
    b2_parameters: Mapping[str, Any]
    receipts: Mapping[str, Any]

    def __post_init__(self) -> None:
        _assert_exact_code_layout(self.code_layout)
        if type(self.waveform_layout) is not WaveformLayout:
            raise ContractError("receiver waveform_layout must be WaveformLayout")
        layout = self.waveform_layout
        expected = _EXPECTED_WAVEFORM_IDENTITIES.get(layout.pilot_period_symbols)
        if (
            layout.prefix_symbols != 32
            or layout.data_symbols_per_polarization != 6144
            or expected is None
            or layout.total_symbols_per_polarization != expected[1]
        ):
            raise ContractError("receiver waveform layout is not a registered D0 identity")
        total = layout.total_symbols_per_polarization
        array_shapes = {
            "received_samples": (2, total),
            "equalized_samples": (2, total),
            "common_cpr_phase_trace": (2, total),
            "known_prefix": (2, 32),
            "periodic_pilots": (2, expected[0]),
        }
        for name, shape in array_shapes.items():
            frozen = _finite_array(getattr(self, name), shape, name)
            object.__setattr__(self, name, frozen)

        prefix_noise = np.empty(2, dtype=np.float64)
        for pol in range(2):
            known = self.known_prefix[pol]
            received = self.received_samples[pol, :32]
            denominator = np.sum(np.abs(known) ** 2)
            if not np.isfinite(denominator) or denominator <= 0.0:
                raise ContractError("known prefix must have positive finite energy")
            gain = np.sum(np.conj(known) * received) / denominator
            residual = received - gain * known
            prefix_noise[pol] = float(np.sum(np.abs(residual) ** 2) / 31.0)
        if not np.all(np.isfinite(prefix_noise)) or np.any(prefix_noise < 0.0):
            raise ContractError("derived receiver noise estimate must be finite")
        prefix_noise.setflags(write=False)
        object.__setattr__(self, "receiver_noise_estimate", prefix_noise)

        for field in fields(self):
            _assert_receiver_truth_free(getattr(self, field.name), field.name)
        object.__setattr__(self, "b2_parameters", _deep_freeze(self.b2_parameters))
        receipts = dict(self.receipts)
        receipts["receiver_noise_estimator_id"] = "known_prefix_ls_rss_over_31_v1"
        receipts["receiver_noise_estimate_per_pol"] = prefix_noise
        object.__setattr__(self, "receipts", _deep_freeze(receipts))


@dataclass(frozen=True, slots=True)
class TruthView:
    information_bits: np.ndarray
    coded_bits: np.ndarray
    transmitted_symbols: np.ndarray
    true_phase: np.ndarray
    channel_h: np.ndarray
    physical_snr_db: float
    fade: np.ndarray
    noise_receipt: Mapping[str, Any]
    event_label: str
    final_codeword_correctness: np.ndarray | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        object.__setattr__(self, "information_bits", _exact_binary_uint8(
            self.information_bits, (2, 16, 1024), "information_bits"
        ))
        object.__setattr__(self, "coded_bits", _exact_binary_uint8(
            self.coded_bits, (2, 16, 1536), "coded_bits"
        ))
        if type(self.transmitted_symbols) is not np.ndarray or self.transmitted_symbols.ndim != 2:
            raise ContractError("transmitted_symbols must be a two-dimensional ndarray")
        physical_shape = self.transmitted_symbols.shape
        if physical_shape[0] != 2 or physical_shape[1] <= 0:
            raise ContractError("truth physical arrays must have shape (2, positive length)")
        for name in ("transmitted_symbols", "true_phase", "channel_h", "fade"):
            object.__setattr__(self, name, _finite_array(getattr(self, name), physical_shape, name))
        if isinstance(self.physical_snr_db, (bool, np.bool_)) or not isinstance(
            self.physical_snr_db, (int, float, np.integer, np.floating)
        ) or not math.isfinite(float(self.physical_snr_db)):
            raise ContractError("physical_snr_db must be a finite numeric truth scalar")
        if not isinstance(self.noise_receipt, Mapping) or "samples" not in self.noise_receipt:
            raise ContractError("noise_receipt must contain exact noise samples")
        _finite_array(self.noise_receipt["samples"], physical_shape, "noise_receipt.samples")
        if type(self.event_label) is not str or not self.event_label:
            raise ContractError("event_label must be a non-empty string")
        object.__setattr__(self, "noise_receipt", _deep_freeze(self.noise_receipt))


@dataclass(frozen=True, slots=True)
class EvaluatedTruthView:
    truth: TruthView
    decoded_information_bits: np.ndarray

    def __post_init__(self) -> None:
        if type(self.truth) is not TruthView:
            raise TypeError("truth must be the exact pending TruthView type")
        if self.truth.final_codeword_correctness is not None:
            raise ContractError("truth must remain pending before evaluation")
        decoded = _exact_binary_uint8(
            self.decoded_information_bits,
            (2, 16, 1024),
            "decoded_information_bits",
        )
        object.__setattr__(self, "decoded_information_bits", decoded)

    @property
    def final_codeword_correctness(self) -> np.ndarray:
        correctness = np.all(
            self.decoded_information_bits == self.truth.information_bits,
            axis=-1,
        ).astype(np.bool_)
        correctness.setflags(write=False)
        return correctness


def finalize_truth_view(
    truth: TruthView, *, decoded_information_bits: np.ndarray
) -> EvaluatedTruthView:
    """Evaluator-only transition from pending payload truth to correctness."""

    if type(truth) is not TruthView:
        raise TypeError("truth must be the exact TruthView type")
    if truth.final_codeword_correctness is not None:
        raise ContractError("truth correctness is already finalized")
    return EvaluatedTruthView(
        truth=truth,
        decoded_information_bits=decoded_information_bits,
    )


@dataclass(frozen=True, slots=True)
class PhysicalCell:
    cell_id: str
    snr_db: int
    linewidth_hz: int

    def __post_init__(self) -> None:
        if type(self.cell_id) is not str or not self.cell_id:
            raise ContractError("physical cell_id must be a non-empty exact string")
        if type(self.snr_db) is not int:
            raise ContractError("physical snr_db must be an exact integer")
        if type(self.linewidth_hz) is not int or self.linewidth_hz <= 0:
            raise ContractError("physical linewidth_hz must be a positive exact integer")


@dataclass(frozen=True, slots=True)
class PopulationContract:
    modulation: str
    polarizations: tuple[str, ...]
    code: CodeLayout
    symbol_rate_baud: float
    snr_db: tuple[int, ...]
    linewidth_hz: tuple[int, ...]

    @property
    def cells(self) -> tuple[PhysicalCell, ...]:
        return tuple(
            PhysicalCell(
                cell_id=f"snr_{snr_db}db__linewidth_{linewidth_hz}hz",
                snr_db=snr_db,
                linewidth_hz=linewidth_hz,
            )
            for snr_db, linewidth_hz in product(self.snr_db, self.linewidth_hz)
        )


@dataclass(frozen=True, slots=True)
class InclusiveSeedRange:
    first: int
    last: int

    def __post_init__(self) -> None:
        if type(self.first) is not int or type(self.last) is not int:
            raise ContractError("seed range endpoints must be exact integers")
        if self.first < 0 or self.last > 2**63 - 1:
            raise ContractError("seed range endpoints must fit non-negative int64")
        if self.first > self.last:
            raise ContractError(
                f"invalid inclusive seed range: {self.first}..{self.last}"
            )

    @property
    def values(self) -> tuple[int, ...]:
        return tuple(range(self.first, self.last + 1))

    def __contains__(self, seed: object) -> bool:
        return isinstance(seed, int) and not isinstance(seed, bool) and self.first <= seed <= self.last


@dataclass(frozen=True, slots=True)
class SeedRegistry:
    entries: tuple[tuple[str, InclusiveSeedRange], ...]
    first_stage_natural: InclusiveSeedRange

    def __post_init__(self) -> None:
        labels = tuple(label for label, _ in self.entries)
        if len(labels) != len(set(labels)):
            raise ContractError("duplicate seed registry label")
        for (left_label, left), (right_label, right) in combinations(self.entries, 2):
            if max(left.first, right.first) <= min(left.last, right.last):
                raise ContractError(
                    f"overlapping seed ranges: {left_label} and {right_label}"
                )
        natural = self.range_for("natural_occurrence")
        if not (
            natural.first <= self.first_stage_natural.first
            <= self.first_stage_natural.last
            <= natural.last
        ):
            raise ContractError("natural first-stage range is not a subset of maximum")

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(label for label, _ in self.entries)

    def range_for(self, label: str) -> InclusiveSeedRange:
        for registered_label, seed_range in self.entries:
            if registered_label == label:
                return seed_range
        raise KeyError(f"unknown seed label: {label}")

    def assert_member(self, label: str, seed: int) -> None:
        seed_range = self.range_for(label)
        if seed not in seed_range:
            raise ValueError(f"seed {seed} does not belong to seed label {label}")

    def label_for(self, seed: int) -> str:
        for label, seed_range in self.entries:
            if seed in seed_range:
                return label
        raise ValueError(f"seed {seed} is outside every registered seed range")


@dataclass(frozen=True, slots=True)
class D0Contract:
    schema_version: str
    control: ControlContract
    population: PopulationContract
    seed_registry: SeedRegistry

    @property
    def population_manifest(self) -> tuple[PhysicalCell, ...]:
        return self.population.cells


@dataclass(frozen=True, slots=True)
class IdentityBindingContract:
    """Exact immutable view of the thirteen owner identity sections."""

    schema_version: str
    decision_ref: str
    scientific_contract_change: str
    canonical_serialization: Mapping[str, Any]
    grid_authority: Mapping[str, Any]
    payload_schemas: Mapping[str, Any]
    hmm_authority: Mapping[str, Any]
    ledger_accounting: Mapping[str, Any]
    cache_source: Mapping[str, Any]
    consumer_bindings: Mapping[str, Any]
    runtime_content: Mapping[str, Any]
    golden_vectors: Mapping[str, Any]
    validator_obligations: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class OrdinaryDomainAuthority:
    """Narrow typed projection of full-owner ordinary enumeration domains."""

    controlled_cell_aliases: tuple[str, ...]
    polarizations: tuple[str, ...]
    fixtures: tuple[str, ...]
    candidates: tuple[str, ...]
    s2_methods: tuple[str, ...]
    s4_checks: tuple[str, ...]
    tuple_ids: tuple[str, ...]
    b_values: tuple[int, ...]
    nw_values: tuple[int, ...]
    s2_record_types: tuple[str, ...]
    s3_record_types: tuple[str, ...]
    s4_record_types: tuple[str, ...]
    bps_record_types: tuple[str, ...]
    b2_clean_record_types: tuple[str, ...]
    b2_controlled_record_types: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class D0OwnerIdentityAuthority:
    """Authenticated D0 scientific contract plus its additive identity view."""

    contract: D0Contract
    identity_binding: IdentityBindingContract
    ordinary_domain: OrdinaryDomainAuthority
    owner_sha256: str
    scientific_projection_sha256: str
    identity_binding_sha256: str
    ordinary_domain_sha256: str


def assert_frozen_d0_identity(contract: D0Contract) -> None:
    """Reject dataclass-replaced or loosely equal variants of the v3 owner."""

    if type(contract) is not D0Contract or type(contract.control) is not ControlContract:
        raise ContractError("exact frozen D0 contract types required")
    control = contract.control
    observed_control = tuple(getattr(control, field.name) for field in fields(ControlContract))
    expected_control = (
        ".sessions/2026-08-09-coded-decoder-feedback-groundwork",
        12, "CP012", "D0_TESTBED_IMPLEMENTATION", "D011", "V005",
        True, True, True, False, False,
    )
    expected_control_types = (str, int, str, str, str, str, bool, bool, bool, bool, bool)
    if observed_control != expected_control or any(
        type(value) is not expected_type
        for value, expected_type in zip(observed_control, expected_control_types, strict=True)
    ):
        raise ContractError("control identity is not the frozen CP012 owner")
    if type(contract.schema_version) is not str or contract.schema_version != "coded_decoder_feedback.d0.v3":
        raise ContractError("schema identity is not the frozen D0 v3 owner")

    population = contract.population
    if type(population) is not PopulationContract:
        raise ContractError("population must be the exact PopulationContract type")
    _assert_exact_code_layout(population.code)
    if (
        type(population.modulation) is not str
        or population.modulation != "gray_square_16qam"
        or type(population.polarizations) is not tuple
        or population.polarizations != ("X", "Y")
        or any(type(item) is not str for item in population.polarizations)
        or type(population.symbol_rate_baud) is not float
        or population.symbol_rate_baud != 2.5e9
        or type(population.snr_db) is not tuple
        or population.snr_db != (10, 14, 18, 22)
        or any(type(item) is not int for item in population.snr_db)
        or type(population.linewidth_hz) is not tuple
        or population.linewidth_hz != (10000, 20000, 80000)
        or any(type(item) is not int for item in population.linewidth_hz)
    ):
        raise ContractError("population identity is not the frozen D0 owner")

    registry = contract.seed_registry
    if type(registry) is not SeedRegistry:
        raise ContractError("seed registry must be the exact SeedRegistry type")
    expected_ranges = (
        ("common_cpr_and_b2_dev", 8000, 8009),
        ("observability_fusion_dev", 8050, 8059),
        ("natural_occurrence", 8100, 8149),
        ("controlled_damage_recovery", 8150, 8159),
        ("controlled_observability", 8160, 8169),
        ("clean_diagnostic", 8170, 8179),
        ("post_d0_c1_dev", 8200, 8219),
        ("post_d0_fresh_heldout", 8300, 8349),
    )
    observed_ranges = tuple(
        (label, seed_range.first, seed_range.last) for label, seed_range in registry.entries
    )
    if (
        type(registry.entries) is not tuple
        or observed_ranges != expected_ranges
        or any(
            type(label) is not str or type(seed_range) is not InclusiveSeedRange
            for label, seed_range in registry.entries
        )
        or type(registry.first_stage_natural) is not InclusiveSeedRange
        or (registry.first_stage_natural.first, registry.first_stage_natural.last) != (8100, 8119)
    ):
        raise ContractError("seed registry identity is not the frozen D0 owner")


_ACTION_PERMISSION_FIELD: Mapping[str, str | None] = {
    "D0_TESTBED_IMPLEMENTATION": "implementation_authorized",
    "D0_UNIT_TEST": "unit_test_authorized",
    "ENGINEERING_THROUGHPUT_BENCHMARK": "engineering_benchmark_authorized",
    "SOURCE_AUDIT": None,
    "CONTRACT_STATIC_CHECK": None,
}


def authorized_action_classes(contract: D0Contract) -> frozenset[str]:
    """Return the exact engineering-only CP012 action set, or fail closed."""

    if not isinstance(contract, D0Contract):
        return frozenset()
    control = contract.control
    identity_is_frozen_cp012 = (
        contract.schema_version == "coded_decoder_feedback.d0.v3"
        and control.epoch == 12
        and control.checkpoint == "CP012"
        and control.action_class == "D0_TESTBED_IMPLEMENTATION"
        and control.decision == "D011"
        and control.verification == "V005"
        and control.execution_authorized is False
        and control.scientific_experiment_authorized is False
    )
    if not identity_is_frozen_cp012:
        return frozenset()
    authorized = {"SOURCE_AUDIT", "CONTRACT_STATIC_CHECK"}
    for action, permission_field in _ACTION_PERMISSION_FIELD.items():
        if permission_field is not None and getattr(control, permission_field) is True:
            authorized.add(action)
    return frozenset(authorized)


def assert_action_authorized(action: str, contract: D0Contract) -> None:
    """Fail closed unless ``action`` is explicitly authorized by CP012."""

    if action not in authorized_action_classes(contract):
        raise PermissionError(f"action {action} is not authorized under CP012")


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{name} must be a YAML mapping")
    return value


def _integer(mapping: Mapping[str, Any], key: str, scope: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ContractError(f"{scope}.{key} must be an integer")
    return value


def _boolean(mapping: Mapping[str, Any], key: str, scope: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ContractError(f"{scope}.{key} must be a boolean")
    return value


def _string(mapping: Mapping[str, Any], key: str, scope: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"{scope}.{key} must be a non-empty string")
    return value


def _integer_tuple(value: Any, name: str) -> tuple[int, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, int) or isinstance(item, bool) for item in value
    ):
        raise ContractError(f"{name} must be a list of integers")
    return tuple(value)


def _positive_number(mapping: Mapping[str, Any], key: str, scope: str) -> float:
    value = mapping.get(key)
    if isinstance(value, bool):
        raise ContractError(f"{scope}.{key} must be a positive finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{scope}.{key} must be a positive finite number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ContractError(f"{scope}.{key} must be a positive finite number")
    return number


def _seed_range(mapping: Mapping[str, Any], scope: str) -> InclusiveSeedRange:
    return InclusiveSeedRange(
        first=_integer(mapping, "first", scope),
        last=_integer(mapping, "last", scope),
    )


def load_contract(path: str | Path) -> D0Contract:
    """Load the v3 machine owner with duplicate-key and type checks."""

    owner_path = Path(path)
    try:
        with owner_path.open("r", encoding="utf-8") as stream:
            document = yaml.load(stream, Loader=_StrictLoader)
    except yaml.YAMLError as exc:
        raise ContractError(f"invalid YAML contract: {exc}") from exc

    root = _mapping(document, "contract")
    schema_version = _string(root, "schema_version", "contract")
    control_raw = _mapping(root.get("control"), "control")
    control = ControlContract(
        topic=_string(control_raw, "topic", "control"),
        epoch=_integer(control_raw, "epoch", "control"),
        checkpoint=_string(control_raw, "checkpoint", "control"),
        action_class=_string(control_raw, "action_class", "control"),
        decision=_string(control_raw, "decision", "control"),
        verification=_string(control_raw, "verification", "control"),
        implementation_authorized=_boolean(
            control_raw, "implementation_authorized", "control"
        ),
        unit_test_authorized=_boolean(control_raw, "unit_test_authorized", "control"),
        engineering_benchmark_authorized=_boolean(
            control_raw, "engineering_benchmark_authorized", "control"
        ),
        execution_authorized=_boolean(control_raw, "execution_authorized", "control"),
        scientific_experiment_authorized=_boolean(
            control_raw, "scientific_experiment_authorized", "control"
        ),
    )

    population_raw = _mapping(root.get("population"), "population")
    code_raw = _mapping(population_raw.get("code"), "population.code")
    physical_raw = _mapping(population_raw.get("physical"), "population.physical")
    polarizations_raw = population_raw.get("polarizations")
    if not isinstance(polarizations_raw, list) or any(
        not isinstance(item, str) or not item for item in polarizations_raw
    ):
        raise ContractError("population.polarizations must be a list of strings")
    population = PopulationContract(
        modulation=_string(population_raw, "modulation", "population"),
        polarizations=tuple(polarizations_raw),
        code=CodeLayout(
            family=_string(code_raw, "family", "population.code"),
            information_bits_per_cw=_integer(
                code_raw, "information_bits_per_cw", "population.code"
            ),
            transmitted_bits_per_cw=_integer(
                code_raw, "transmitted_bits_per_cw", "population.code"
            ),
            codewords_per_polarization=_integer(
                code_raw, "codewords_per_polarization", "population.code"
            ),
            data_symbols_per_cw=_integer(
                code_raw, "data_symbols_per_cw", "population.code"
            ),
            data_symbols_per_polarization=_integer(
                code_raw, "data_symbols_per_polarization", "population.code"
            ),
            decoder_iterations=_integer(
                code_raw, "decoder_iterations", "population.code"
            ),
        ),
        symbol_rate_baud=_positive_number(
            physical_raw, "symbol_rate_baud", "population.physical"
        ),
        snr_db=_integer_tuple(
            physical_raw.get("snr_db"), "population.physical.snr_db"
        ),
        linewidth_hz=_integer_tuple(
            physical_raw.get("linewidth_hz"), "population.physical.linewidth_hz"
        ),
    )

    seed_raw = _mapping(root.get("seed_plan"), "seed_plan")
    natural_raw = _mapping(seed_raw.get("natural_occurrence"), "seed_plan.natural_occurrence")
    maximum_raw = natural_raw.get("maximum")
    first_stage_raw = natural_raw.get("first_stage")
    maximum = _integer_tuple(maximum_raw, "seed_plan.natural_occurrence.maximum")
    first_stage = _integer_tuple(
        first_stage_raw, "seed_plan.natural_occurrence.first_stage"
    )
    if len(maximum) != 2 or len(first_stage) != 2:
        raise ContractError("natural seed ranges must contain exactly two endpoints")

    simple_labels = (
        "common_cpr_and_b2_dev",
        "observability_fusion_dev",
        "controlled_damage_recovery",
        "controlled_observability",
        "clean_diagnostic",
        "post_d0_c1_dev",
        "post_d0_fresh_heldout",
    )
    parsed = {
        label: _seed_range(
            _mapping(seed_raw.get(label), f"seed_plan.{label}"),
            f"seed_plan.{label}",
        )
        for label in simple_labels
    }
    entries = (
        ("common_cpr_and_b2_dev", parsed["common_cpr_and_b2_dev"]),
        ("observability_fusion_dev", parsed["observability_fusion_dev"]),
        ("natural_occurrence", InclusiveSeedRange(*maximum)),
        ("controlled_damage_recovery", parsed["controlled_damage_recovery"]),
        ("controlled_observability", parsed["controlled_observability"]),
        ("clean_diagnostic", parsed["clean_diagnostic"]),
        ("post_d0_c1_dev", parsed["post_d0_c1_dev"]),
        ("post_d0_fresh_heldout", parsed["post_d0_fresh_heldout"]),
    )
    seed_registry = SeedRegistry(
        entries=entries,
        first_stage_natural=InclusiveSeedRange(*first_stage),
    )

    return D0Contract(
        schema_version=schema_version,
        control=control,
        population=population,
        seed_registry=seed_registry,
    )


_IDENTITY_KEYS = (
    "schema_version",
    "decision_ref",
    "scientific_contract_change",
    "canonical_serialization",
    "grid_authority",
    "payload_schemas",
    "hmm_authority",
    "ledger_accounting",
    "cache_source",
    "consumer_bindings",
    "runtime_content",
    "golden_vectors",
    "validator_obligations",
)
_IDENTITY_SECTION_KEYS = _IDENTITY_KEYS[3:]
_ANCHOR_PATHS = {
    ("grid_authority", "p_s", "anchors"),
    ("golden_vectors", "grid_commitments", "p_s_anchors"),
}
_FROZEN_OWNER_SHA256 = (
    "f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b"
)
_FROZEN_SCIENTIFIC_PROJECTION_SHA256 = (
    "c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d"
)
_FROZEN_IDENTITY_BINDING_SHA256 = (
    "08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e"
)
_ORDINARY_DOMAIN_SCHEMA = "coded_decoder_feedback.d0.ordinary_domain_authority.v1"
_FROZEN_ORDINARY_DOMAIN_SHA256 = (
    "15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69"
)
_FROZEN_GRID_SHA256 = {
    "p_s": "bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864",
    "sigma_e2": "0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca",
    "combined": "0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf",
}
_FROZEN_LEDGER_COUNTS = {
    "chunks": 263520,
    "logical_trajectory_rows": 22800,
    "logical_primitive_scores": 16689600,
    "executed_trajectory_rows": 9600,
    "materialized_primitive_scores": 7027200,
    "cache_trajectory_rows": 13200,
}


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError("identity value is not canonical-JSON encodable") from exc


def _ordinary_domain_payload(domain: OrdinaryDomainAuthority) -> dict[str, Any]:
    if type(domain) is not OrdinaryDomainAuthority:
        raise ContractError("exact OrdinaryDomainAuthority type required")
    string_fields = (
        "controlled_cell_aliases", "polarizations", "fixtures", "candidates",
        "s2_methods", "s4_checks", "tuple_ids", "s2_record_types",
        "s3_record_types", "s4_record_types", "bps_record_types",
        "b2_clean_record_types", "b2_controlled_record_types",
    )
    for name in string_fields:
        values = getattr(domain, name)
        if (type(values) is not tuple or not values
                or any(type(item) is not str or not item for item in values)
                or len(set(values)) != len(values)):
            raise ContractError(f"ordinary domain {name} must be an exact unique string tuple")
    for name in ("b_values", "nw_values"):
        values = getattr(domain, name)
        if (type(values) is not tuple or not values
                or any(type(item) is not int or type(item) is bool for item in values)
                or len(set(values)) != len(values)):
            raise ContractError(f"ordinary domain {name} must be an exact unique integer tuple")
    return {
        "schema": _ORDINARY_DOMAIN_SCHEMA,
        "controlled_cell_aliases": list(domain.controlled_cell_aliases),
        "polarizations": list(domain.polarizations),
        "fixtures": list(domain.fixtures),
        "candidates": list(domain.candidates),
        "s2_methods": list(domain.s2_methods),
        "s4_checks": list(domain.s4_checks),
        "tuple_ids": list(domain.tuple_ids),
        "b_values": list(domain.b_values),
        "nw_values": list(domain.nw_values),
        "record_type_domains": {
            "s2_method": list(domain.s2_record_types),
            "s3_candidate": list(domain.s3_record_types),
            "s4_check": list(domain.s4_record_types),
            "bps_dev_score": list(domain.bps_record_types),
            "b2_tuple_clean_dev": list(domain.b2_clean_record_types),
            "b2_tuple_controlled_dev": list(domain.b2_controlled_record_types),
        },
    }


def _reject_identity_json_floats(value: Any, path: str = "identity_binding_contract") -> None:
    if type(value) is float:
        raise ContractError(f"JSON float forbidden in {path}")
    if type(value) is dict:
        for key, item in value.items():
            _reject_identity_json_floats(item, f"{path}.{key}")
    elif type(value) is list:
        for index, item in enumerate(value):
            _reject_identity_json_floats(item, f"{path}[{index}]")


def _normalize_identity_tree(value: Any, path: tuple[str, ...]) -> Any:
    """Normalize the two legal integer-key anchor maps, changing no values."""

    if path in _ANCHOR_PATHS:
        if type(value) is not dict:
            raise ContractError("identity anchor table must be an exact mapping")
        literals = []
        for index, float64_hex in value.items():
            if type(index) is not int or type(float64_hex) is not str:
                raise ContractError("identity anchor entries must be int-to-string")
            literals.append(Float64Literal(index=index, float64_hex=float64_hex))
        return literals
    if type(value) is dict:
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise ContractError(
                    f"unexpected non-string identity mapping key at {'.'.join(path)}"
                )
            normalized[key] = _normalize_identity_tree(item, path + (key,))
        return normalized
    if type(value) is list:
        return [
            _normalize_identity_tree(item, path + (str(index),))
            for index, item in enumerate(value)
        ]
    return value


def _identity_tree_to_plain(value: Any, path: tuple[str, ...]) -> Any:
    if path in _ANCHOR_PATHS:
        if type(value) is not tuple or any(
            type(item) is not Float64Literal for item in value
        ):
            raise ContractError("identity anchor view must be a typed tuple")
        result: dict[int, str] = {}
        for literal in value:
            if (
                type(literal.index) is not int
                or type(literal.float64_hex) is not str
                or literal.index in result
            ):
                raise ContractError("invalid identity anchor literal")
            result[literal.index] = literal.float64_hex
        return result
    if type(value) is _FrozenDict:
        return {
            key: _identity_tree_to_plain(item, path + (key,))
            for key, item in value.items()
        }
    if type(value) is tuple:
        return [
            _identity_tree_to_plain(item, path + (str(index),))
            for index, item in enumerate(value)
        ]
    if type(value) in (str, int, bool, type(None)):
        return value
    raise ContractError(
        f"identity view contains non-frozen type {type(value).__name__}"
    )


def _identity_binding_to_plain(binding: IdentityBindingContract) -> dict[str, Any]:
    if type(binding) is not IdentityBindingContract:
        raise ContractError("exact IdentityBindingContract type required")
    if (
        type(binding.schema_version) is not str
        or type(binding.decision_ref) is not str
        or type(binding.scientific_contract_change) is not str
    ):
        raise ContractError("identity headers must be exact strings")
    result: dict[str, Any] = {
        "schema_version": binding.schema_version,
        "decision_ref": binding.decision_ref,
        "scientific_contract_change": binding.scientific_contract_change,
    }
    for section in _IDENTITY_SECTION_KEYS:
        value = getattr(binding, section)
        if type(value) is not _FrozenDict:
            raise ContractError(f"identity section {section} must be an exact frozen mapping")
        result[section] = _identity_tree_to_plain(value, (section,))
    return result


def _assert_grid_commitments(identity: Mapping[str, Any]) -> None:
    grid = identity["grid_authority"]
    p_s = grid["p_s"]["standalone_payload"]
    sigma_e2 = grid["sigma_e2"]["standalone_payload"]
    combined = grid["combined"]["payload"]
    observed = {
        "p_s": _sha256(_canonical_json_bytes(p_s)),
        "sigma_e2": _sha256(_canonical_json_bytes(sigma_e2)),
        "combined": _sha256(_canonical_json_bytes(combined)),
    }
    if observed != _FROZEN_GRID_SHA256:
        raise ContractError("identity grid commitment roots do not match frozen owner")
    if (
        grid["p_s"]["sha256"] != observed["p_s"]
        or grid["sigma_e2"]["sha256"] != observed["sigma_e2"]
        or grid["combined"]["sha256"] != observed["combined"]
        or combined.get("p_s") != p_s
        or combined.get("sigma_e2") != sigma_e2
        or len(p_s.get("values", ())) != 122
        or len(sigma_e2.get("values", ())) != 6
    ):
        raise ContractError("identity grid payloads are not the exact frozen view")


def assert_frozen_owner_identity_authority(
    authority: D0OwnerIdentityAuthority,
) -> None:
    """Revalidate a wrapper before use; never trust replaceable hash fields."""

    if type(authority) is not D0OwnerIdentityAuthority:
        raise ContractError("exact D0OwnerIdentityAuthority type required")
    assert_frozen_d0_identity(authority.contract)
    if (
        type(authority.owner_sha256) is not str
        or authority.owner_sha256 != _FROZEN_OWNER_SHA256
        or type(authority.scientific_projection_sha256) is not str
        or authority.scientific_projection_sha256
        != _FROZEN_SCIENTIFIC_PROJECTION_SHA256
        or type(authority.identity_binding_sha256) is not str
        or authority.identity_binding_sha256 != _FROZEN_IDENTITY_BINDING_SHA256
        or type(authority.ordinary_domain_sha256) is not str
        or authority.ordinary_domain_sha256 != _FROZEN_ORDINARY_DOMAIN_SHA256
    ):
        raise ContractError("owner identity wrapper hashes are not frozen")
    domain_payload = _ordinary_domain_payload(authority.ordinary_domain)
    if _sha256(_canonical_json_bytes(domain_payload)) != _FROZEN_ORDINARY_DOMAIN_SHA256:
        raise ContractError("ordinary domain projection does not match frozen owner")
    identity = _identity_binding_to_plain(authority.identity_binding)
    if tuple(identity) != _IDENTITY_KEYS:
        raise ContractError("identity view field order is not frozen")
    if (
        identity["schema_version"]
        != "coded_decoder_feedback.d0.identity_binding.v1"
        or identity["decision_ref"] != "D015"
        or identity["scientific_contract_change"] != "none"
    ):
        raise ContractError("identity headers are not frozen")
    _reject_identity_json_floats(identity)
    if _sha256(_canonical_json_bytes(identity)) != _FROZEN_IDENTITY_BINDING_SHA256:
        raise ContractError("identity view canonical seal does not match frozen owner")
    _assert_grid_commitments(identity)
    formulas = identity["ledger_accounting"]["formulas"]
    if {
        key: formulas[key]["expected"] for key in _FROZEN_LEDGER_COUNTS
    } != _FROZEN_LEDGER_COUNTS:
        raise ContractError("identity ledger counts do not match frozen owner")


def _scientific_projection_sha256(raw: bytes) -> str:
    identity_markers = list(
        re.finditer(rb"(?m)^identity_binding_contract:\r?$", raw)
    )
    strata_markers = list(re.finditer(rb"(?m)^strata:\r?$", raw))
    if (
        len(identity_markers) != 1
        or len(strata_markers) != 1
        or identity_markers[0].start() >= strata_markers[0].start()
    ):
        raise ContractError("owner identity block placement is not exact")
    projected = (
        raw[: identity_markers[0].start()] + raw[strata_markers[0].start() :]
    )
    return _sha256(projected)


def _string_domain(value: Any, scope: str) -> tuple[str, ...]:
    if (type(value) is not list or not value
            or any(type(item) is not str or not item for item in value)
            or len(set(value)) != len(value)):
        raise ContractError(f"{scope} must be an exact unique string list")
    return tuple(value)


def _integer_domain(value: Any, scope: str) -> tuple[int, ...]:
    if (type(value) is not list or not value
            or any(type(item) is not int or type(item) is bool for item in value)
            or len(set(value)) != len(value)):
        raise ContractError(f"{scope} must be an exact unique integer list")
    return tuple(value)


def _record_type_domain(table: Mapping[str, Any], scope: str) -> tuple[str, ...]:
    record = _mapping(table.get("record_type"), f"{scope}.record_type")
    if "const" in record and "enum" not in record:
        value = record["const"]
        if type(value) is not str or not value:
            raise ContractError(f"{scope}.record_type.const must be a string")
        return (value,)
    if "enum" in record and "const" not in record:
        return _string_domain(record["enum"], f"{scope}.record_type.enum")
    raise ContractError(f"{scope}.record_type must have exactly const or enum")


def _load_ordinary_domain(root: Mapping[str, Any]) -> OrdinaryDomainAuthority:
    fixture = _mapping(root.get("controlled_fixture"), "controlled_fixture")
    cells = _mapping(fixture.get("cells"), "controlled_fixture.cells")
    if any(type(key) is not str or not key for key in cells):
        raise ContractError("controlled_fixture.cells keys must be strings")
    repair = _mapping(
        root.get("statistical_contract_repair"), "statistical_contract_repair"
    )
    enums = _mapping(repair.get("enums"), "statistical_contract_repair.enums")
    tables = _mapping(repair.get("tables"), "statistical_contract_repair.tables")
    freeze = _mapping(
        repair.get("dev_freeze_artifact_contract"),
        "statistical_contract_repair.dev_freeze_artifact_contract",
    )
    freeze_tables = _mapping(
        freeze.get("tables"),
        "statistical_contract_repair.dev_freeze_artifact_contract.tables",
    )
    domain = OrdinaryDomainAuthority(
        controlled_cell_aliases=tuple(cells),
        polarizations=_string_domain(enums.get("polarization"), "enums.polarization"),
        fixtures=_string_domain(enums.get("fixture_id"), "enums.fixture_id"),
        candidates=_string_domain(enums.get("candidate_id"), "enums.candidate_id"),
        s2_methods=_string_domain(enums.get("s2_method_id"), "enums.s2_method_id"),
        s4_checks=_string_domain(enums.get("s4_check_id"), "enums.s4_check_id"),
        tuple_ids=_string_domain(
            freeze.get("tuple_ids_in_legal_order"), "dev_freeze.tuple_ids_in_legal_order"
        ),
        b_values=_integer_domain(freeze.get("B_values"), "dev_freeze.B_values"),
        nw_values=_integer_domain(freeze.get("Nw_values"), "dev_freeze.Nw_values"),
        s2_record_types=_record_type_domain(
            _mapping(tables.get("s2_method"), "tables.s2_method"), "tables.s2_method"
        ),
        s3_record_types=_record_type_domain(
            _mapping(tables.get("s3_candidate"), "tables.s3_candidate"),
            "tables.s3_candidate",
        ),
        s4_record_types=_record_type_domain(
            _mapping(tables.get("s4_check"), "tables.s4_check"), "tables.s4_check"
        ),
        bps_record_types=_record_type_domain(
            _mapping(freeze_tables.get("bps_dev_score"), "freeze.tables.bps_dev_score"),
            "freeze.tables.bps_dev_score",
        ),
        b2_clean_record_types=_record_type_domain(
            _mapping(
                freeze_tables.get("b2_tuple_clean_dev"),
                "freeze.tables.b2_tuple_clean_dev",
            ),
            "freeze.tables.b2_tuple_clean_dev",
        ),
        b2_controlled_record_types=_record_type_domain(
            _mapping(
                freeze_tables.get("b2_tuple_controlled_dev"),
                "freeze.tables.b2_tuple_controlled_dev",
            ),
            "freeze.tables.b2_tuple_controlled_dev",
        ),
    )
    if _sha256(_canonical_json_bytes(_ordinary_domain_payload(domain))) != _FROZEN_ORDINARY_DOMAIN_SHA256:
        raise ContractError("ordinary domain projection SHA256 does not match frozen owner")
    return domain


def load_owner_identity_authority(path: str | Path) -> D0OwnerIdentityAuthority:
    """Explicitly load and authenticate the additive D015 identity authority."""

    owner_path = Path(path)
    raw_before = owner_path.read_bytes()
    try:
        document = yaml.load(raw_before.decode("utf-8"), Loader=_StrictLoader)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ContractError(f"invalid YAML owner identity: {exc}") from exc
    root = _mapping(document, "owner")
    ordinary_domain = _load_ordinary_domain(root)
    identity_raw = _mapping(
        root.get("identity_binding_contract"), "identity_binding_contract"
    )
    if tuple(identity_raw) != _IDENTITY_KEYS:
        raise ContractError("identity owner must contain the exact thirteen keys")
    if (
        type(identity_raw["schema_version"]) is not str
        or identity_raw["schema_version"]
        != "coded_decoder_feedback.d0.identity_binding.v1"
        or type(identity_raw["decision_ref"]) is not str
        or identity_raw["decision_ref"] != "D015"
        or type(identity_raw["scientific_contract_change"]) is not str
        or identity_raw["scientific_contract_change"] != "none"
    ):
        raise ContractError("identity owner headers do not match D015")
    for section in _IDENTITY_SECTION_KEYS:
        _mapping(identity_raw[section], f"identity_binding_contract.{section}")
    _reject_identity_json_floats(identity_raw)

    owner_sha256 = _sha256(raw_before)
    identity_sha256 = _sha256(_canonical_json_bytes(identity_raw))
    projection_sha256 = _scientific_projection_sha256(raw_before)
    if owner_sha256 != _FROZEN_OWNER_SHA256:
        raise ContractError("owner bytes SHA256 does not match frozen D015 owner")
    if identity_sha256 != _FROZEN_IDENTITY_BINDING_SHA256:
        raise ContractError("identity canonical SHA256 does not match frozen D015 owner")
    if projection_sha256 != _FROZEN_SCIENTIFIC_PROJECTION_SHA256:
        raise ContractError("scientific projection SHA256 does not match frozen owner")

    contract = load_contract(owner_path)
    raw_after = owner_path.read_bytes()
    if raw_after != raw_before:
        raise ContractError("owner bytes changed while identity authority was loading")
    assert_frozen_d0_identity(contract)

    normalized_sections = {
        section: _deep_freeze(
            _normalize_identity_tree(identity_raw[section], (section,))
        )
        for section in _IDENTITY_SECTION_KEYS
    }
    binding = IdentityBindingContract(
        schema_version=identity_raw["schema_version"],
        decision_ref=identity_raw["decision_ref"],
        scientific_contract_change=identity_raw["scientific_contract_change"],
        **normalized_sections,
    )
    authority = D0OwnerIdentityAuthority(
        contract=contract,
        identity_binding=binding,
        ordinary_domain=ordinary_domain,
        owner_sha256=owner_sha256,
        scientific_projection_sha256=projection_sha256,
        identity_binding_sha256=identity_sha256,
        ordinary_domain_sha256=_FROZEN_ORDINARY_DOMAIN_SHA256,
    )
    assert_frozen_owner_identity_authority(authority)
    return authority
