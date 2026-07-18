"""P01 contract-only primitives for U25 causal safe-fallback exploration.

This module deliberately does not run a receiver, train a model, or score
performance.  It freezes the smallest causal action interface that a future
Sandbox runner may consume.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Callable, Mapping, Sequence
from typing import Any


SCHEMA_VERSION = "direction-lab.u25-action-contract.v1"
ACTIONS = {"NO_OP", "SAFE_BASELINE", "RESET"}
TRIGGERS = {"NONE", "LOCK_LOSS", "CYCLE_SLIP", "DIVERGENCE", "PERFORMANCE_DEGRADATION"}
REQUIRED_EVENT_FIELDS = (
    "sequence_id",
    "step",
    "available_at_step",
    "trigger",
    "observables",
    "source_pointers",
)
REQUIRED_OBSERVABLES = ("lock_score", "cma_error")
ALLOWED_OBSERVABLES = {"lock_score", "cma_error", "output_power", "update_norm"}
STANDARD_CMA_TRACE_FIELDS = {
    "output_start": {"shape": "scalar", "dtype": "int", "unit": "symbol_index", "time_index": "block_start"},
    "output_end": {"shape": "scalar", "dtype": "int", "unit": "symbol_index", "time_index": "block_end"},
    "cm_error": {"shape": "scalar", "dtype": "float64", "unit": "power_squared", "time_index": "block"},
    "output_power": {"shape": "scalar", "dtype": "float64", "unit": "normalized_power", "time_index": "block"},
    "update_norm": {"shape": "scalar", "dtype": "float64", "unit": "weight_norm", "time_index": "block"},
}
FORBIDDEN_TRACE_FIELDS = {
    "h", "true_h", "true_jones", "jones", "tx_bits", "sX", "sY", "fixed_label_ber", "pi_ber",
    "permutation_invariant_ber", "future_window", "future_label", "post_hoc_ber",
}

# This is an explicit comparator contract, not a learned policy and not an
# oracle.  A future candidate must declare a different policy to be distinct.
FIXED_POLICY_ACTIONS = {
    "NONE": "NO_OP",
    "LOCK_LOSS": "SAFE_BASELINE",
    "CYCLE_SLIP": "SAFE_BASELINE",
    "DIVERGENCE": "SAFE_BASELINE",
    "PERFORMANCE_DEGRADATION": "SAFE_BASELINE",
}

ACTION_CONTRACT = {
    "schema_version": SCHEMA_VERSION,
    "candidate_id": "U25",
    "required_event_fields": list(REQUIRED_EVENT_FIELDS),
    "required_observables": list(REQUIRED_OBSERVABLES),
    "trigger_action_map": dict(FIXED_POLICY_ACTIONS),
    "actions": sorted(ACTIONS),
    "standard_cma_trace_fields": STANDARD_CMA_TRACE_FIELDS,
    "forbidden_trace_fields": sorted(FORBIDDEN_TRACE_FIELDS),
    "allowed_observables": sorted(ALLOWED_OBSERVABLES),
    "input_key_policy": "strict-whitelist",
    "lock_score_proxy": {"formula": "1/(1+cm_error)", "status": "receiver-proxy-only"},
    "source_pointer_rule": "source_id plus trace field/index or explicit causal transform",
    "causal_rule": "available_at_step <= step; policy receives current event only",
    "shared_runtime_contract_fields": [
        "channel_block",
        "r2",
        "fade_threshold_h",
        "clip_norm",
        "t_s",
        "method",
    ],
}


def validate_event(event: Mapping[str, Any]) -> None:
    """Validate one online event and reject post-hoc/oracle information."""

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")
    missing = [key for key in REQUIRED_EVENT_FIELDS if key not in event]
    if missing:
        raise ValueError(f"event missing required fields: {missing}")
    if not isinstance(event["sequence_id"], str) or not event["sequence_id"]:
        raise ValueError("sequence_id must be a non-empty string")
    step = event["step"]
    available_at_step = event["available_at_step"]
    if not isinstance(step, int) or step < 0:
        raise ValueError("step must be a non-negative integer")
    if not isinstance(available_at_step, int) or available_at_step < 0:
        raise ValueError("available_at_step must be a non-negative integer")
    if available_at_step > step:
        raise ValueError("future information is not causal")
    if event["trigger"] not in TRIGGERS:
        raise ValueError(f"unsupported trigger: {event['trigger']}")
    observables = event["observables"]
    if not isinstance(observables, Mapping):
        raise ValueError("observables must be a mapping")
    missing_observables = [key for key in REQUIRED_OBSERVABLES if key not in observables]
    if missing_observables:
        raise ValueError(f"observables missing required fields: {missing_observables}")
    unsupported_observables = sorted(set(observables).difference(ALLOWED_OBSERVABLES))
    if unsupported_observables:
        raise ValueError(f"unsupported observables: {unsupported_observables}")
    source_pointers = event["source_pointers"]
    if not isinstance(source_pointers, Mapping):
        raise ValueError("source_pointers must be a mapping")
    required_pointers = {
        "sequence_id", "step", "available_at_step", "trigger",
        *(f"observables.{key}" for key in observables),
    }
    missing_pointers = sorted(required_pointers.difference(source_pointers))
    if missing_pointers:
        raise ValueError(f"source_pointers missing fields: {missing_pointers}")
    forbidden = set(event).intersection({"oracle", "post_hoc", "future_label", "future_state"})
    if forbidden:
        raise ValueError(f"post-hoc/oracle fields are forbidden: {sorted(forbidden)}")


def fixed_safe_policy(event: Mapping[str, Any]) -> dict[str, Any]:
    """Return the deterministic fixed-policy comparator decision."""

    validate_event(event)
    trigger = str(event["trigger"])
    return {
        "sequence_id": event["sequence_id"],
        "step": event["step"],
        "action": FIXED_POLICY_ACTIONS[trigger],
        "reason": trigger,
        "policy_id": "fixed-safe-policy.v1",
    }


def adapt_standard_cma_trace(
    trace: Sequence[Mapping[str, Any]],
    *,
    sequence_id: str,
    source_id: str,
    lock_score_threshold: float,
    divergence_error_threshold: float,
) -> list[dict[str, Any]]:
    """Adapt the actual standard-CMA blind trace into causal U25 events.

    The input schema mirrors ``run_b001._default_runner``'s
    ``blind_trace`` rows.  Labels, channel truth, TX symbols, and future
    windows are rejected before any event is emitted.  ``lock_score`` is an
    explicit receiver-visible transform of the current block's ``cm_error``;
    it is not a channel or BER oracle.
    """

    if not isinstance(sequence_id, str) or not sequence_id:
        raise ValueError("sequence_id must be a non-empty string")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("source_id must be a non-empty string")
    if not math.isfinite(float(lock_score_threshold)):
        raise ValueError("lock_score_threshold must be finite")
    if not math.isfinite(float(divergence_error_threshold)) or float(divergence_error_threshold) < 0:
        raise ValueError("divergence_error_threshold must be finite and non-negative")

    events: list[dict[str, Any]] = []
    for step, row in enumerate(trace):
        if not isinstance(row, Mapping):
            raise ValueError("standard-CMA trace rows must be mappings")
        forbidden = sorted(set(row).difference(STANDARD_CMA_TRACE_FIELDS))
        if forbidden:
            raise ValueError(f"forbidden or unregistered trace fields: {forbidden}")
        missing = sorted(set(STANDARD_CMA_TRACE_FIELDS).difference(row))
        if missing:
            raise ValueError(f"standard-CMA trace missing fields: {missing}")
        start = row["output_start"]
        end = row["output_end"]
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            raise ValueError("output_start/output_end must be ordered integer symbol indices")
        values: dict[str, float] = {}
        for key in ("cm_error", "output_power", "update_norm"):
            value = float(row[key])
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"standard-CMA trace field {key} must be finite and non-negative")
            values[key] = value
        lock_score = 1.0 / (1.0 + values["cm_error"])
        if lock_score <= float(lock_score_threshold):
            trigger = "LOCK_LOSS"
        elif values["cm_error"] >= float(divergence_error_threshold):
            trigger = "DIVERGENCE"
        else:
            trigger = "NONE"
        event = {
            "sequence_id": sequence_id,
            "step": step,
            "available_at_step": step,
            "trigger": trigger,
            "observables": {
                "lock_score": lock_score,
                "cma_error": values["cm_error"],
                "output_power": values["output_power"],
                "update_norm": values["update_norm"],
            },
            "source_pointers": {
                "sequence_id": {"source": "adapter_argument", "source_id": source_id, "field": "sequence_id", "dtype": "str"},
                "step": {
                    "source": "standard_cma_trace", "source_id": source_id, "field": "trace_index",
                    "index": step, "dtype": "int", "aligned_sample_start": start,
                    "aligned_sample_end": end, "sample_end_exclusive": True,
                },
                "available_at_step": {"source": "standard_cma_trace", "source_id": source_id, "field": "trace_index", "index": step, "dtype": "int"},
                "trigger": {"source": "causal_rule", "source_id": source_id, "derived_from": "cm_error", "index": step},
                "observables.lock_score": {
                    "source": "causal_transform", "source_id": source_id, "derived_from": "cm_error", "index": step,
                    "formula": "1/(1+cm_error)", "dtype": "float64", "unit": "unitless",
                },
                "observables.cma_error": {
                    "source": "standard_cma_trace", "source_id": source_id, "field": "cm_error", "index": step,
                    "dtype": "float64", "unit": "power_squared",
                },
                "observables.output_power": {
                    "source": "standard_cma_trace", "source_id": source_id, "field": "output_power", "index": step,
                    "dtype": "float64", "unit": "normalized_power",
                },
                "observables.update_norm": {
                    "source": "standard_cma_trace", "source_id": source_id, "field": "update_norm", "index": step,
                    "dtype": "float64", "unit": "weight_norm",
                },
            },
        }
        validate_event(event)
        events.append(event)
    return events


def apply_action(state: Mapping[str, Any], decision: Mapping[str, Any]) -> dict[str, Any]:
    """Apply a contract action without mutating the input state."""

    action = decision.get("action")
    if action not in ACTIONS:
        raise ValueError(f"unsupported action: {action}")
    next_state = copy.deepcopy(dict(state))
    if action == "NO_OP":
        return next_state
    if action == "SAFE_BASELINE":
        next_state["mode"] = "standard_cma"
        next_state["fallback_count"] = int(next_state.get("fallback_count", 0)) + 1
        return next_state
    next_state["mode"] = "standard_cma"
    next_state["reset_count"] = int(next_state.get("reset_count", 0)) + 1
    return next_state


def replay_events(
    events: Sequence[Mapping[str, Any]],
    policy: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Replay a finite causal event stream deterministically.

    The policy receives only the current validated event.  No future event or
    post-hoc label is made available through this interface.
    """

    replay: list[dict[str, Any]] = []
    previous_step = -1
    sequence_id: str | None = None
    for event in events:
        validate_event(event)
        if sequence_id is None:
            sequence_id = str(event["sequence_id"])
        elif event["sequence_id"] != sequence_id:
            raise ValueError("replay contains multiple sequence_id values")
        if int(event["step"]) != previous_step + 1:
            raise ValueError("replay steps must be contiguous and ordered")
        decision = dict(policy(event))
        if decision.get("action") not in ACTIONS:
            raise ValueError(f"unsupported action: {decision.get('action')}")
        replay.append(decision)
        previous_step = int(event["step"])
    return replay


def fingerprint() -> str:
    """Return the stable fingerprint of this explicit contract."""

    payload = json.dumps(
        ACTION_CONTRACT,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


__all__ = [
    "ACTION_CONTRACT",
    "ACTIONS",
    "STANDARD_CMA_TRACE_FIELDS",
    "adapt_standard_cma_trace",
    "apply_action",
    "fingerprint",
    "fixed_safe_policy",
    "replay_events",
    "validate_event",
]
