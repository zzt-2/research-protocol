from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "tools" / "u25_action_contract.py"
spec = importlib.util.spec_from_file_location("direction_lab_u25_action_contract", MODULE_PATH)
assert spec and spec.loader
u25 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u25)

RUN_B001_PATH = Path(__file__).parents[1] / "tools" / "run_b001.py"
run_spec = importlib.util.spec_from_file_location("direction_lab_run_b001_for_u25", RUN_B001_PATH)
assert run_spec and run_spec.loader
run_b001 = importlib.util.module_from_spec(run_spec)
run_spec.loader.exec_module(run_b001)


def _event(*, step: int = 0, trigger: str = "NONE") -> dict:
    return {
        "sequence_id": "cell-001",
        "step": step,
        "available_at_step": step,
        "trigger": trigger,
        "observables": {"lock_score": 0.9, "cma_error": 0.1},
        "source_pointers": {
            "sequence_id": {"source": "test", "field": "sequence_id"},
            "step": {"source": "test", "field": "step"},
            "available_at_step": {"source": "test", "field": "step"},
            "trigger": {"source": "test", "field": "trigger"},
            "observables.lock_score": {"source": "test", "field": "lock_score"},
            "observables.cma_error": {"source": "test", "field": "cma_error"},
        },
    }


def test_validate_event_rejects_future_information() -> None:
    event = _event(step=2)
    event["available_at_step"] = 3
    with pytest.raises(ValueError, match="future information"):
        u25.validate_event(event)


def test_fixed_safe_policy_is_deterministic_and_causal() -> None:
    event = _event(trigger="LOCK_LOSS")
    first = u25.fixed_safe_policy(event)
    second = u25.fixed_safe_policy(copy.deepcopy(event))
    assert first == second
    assert first["action"] == "SAFE_BASELINE"
    assert first["reason"] == "LOCK_LOSS"


def test_no_op_preserves_receiver_state() -> None:
    state = {"mode": "standard_cma", "reset_count": 2}
    decision = {"action": "NO_OP", "reason": "NONE"}
    assert u25.apply_action(state, decision) == state
    assert state == {"mode": "standard_cma", "reset_count": 2}


def test_replay_is_deterministic_and_has_no_future_dependency() -> None:
    events = [_event(step=0), _event(step=1, trigger="LOCK_LOSS")]
    first = u25.replay_events(events, u25.fixed_safe_policy)
    second = u25.replay_events(copy.deepcopy(events), u25.fixed_safe_policy)
    assert first == second
    assert [item["action"] for item in first] == ["NO_OP", "SAFE_BASELINE"]


def test_action_set_and_fingerprint_are_explicit_and_stable() -> None:
    assert u25.ACTIONS == {"NO_OP", "SAFE_BASELINE", "RESET"}
    assert u25.fingerprint() == u25.fingerprint()


def test_unknown_action_is_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported action"):
        u25.apply_action({"mode": "standard_cma"}, {"action": "ORACLE"})


def _actual_standard_cma_trace() -> list[dict]:
    runner, config_factory = run_b001._default_runner(run_b001.DEFAULT_SOURCE_ROOT)
    n = 256
    cfg = config_factory(mu=0.001, taps=11, r2=1.0, block_size=64,
                         eval_start=0, eval_end=n)
    s = __import__("numpy").ones(n, dtype=complex)
    output = runner({"rX": s, "rY": s}, cfg, variant="baseline", return_blind_trace=True)
    return output["blind_trace"]


def test_adapter_consumes_real_standard_cma_trace_fields() -> None:
    trace = _actual_standard_cma_trace()
    events = u25.adapt_standard_cma_trace(
        trace,
        sequence_id="smoke-standard-cma",
        source_id="run_b001._default_runner.blind_trace",
        lock_score_threshold=0.90,
        divergence_error_threshold=0.20,
    )
    assert len(events) == len(trace)
    assert all(event["source_pointers"]["observables.cma_error"]["field"] == "cm_error" for event in events)
    assert all(event["source_pointers"]["observables.lock_score"]["derived_from"] == "cm_error" for event in events)
    assert all(event["source_pointers"]["observables.output_power"]["field"] == "output_power" for event in events)
    assert all(event["source_pointers"]["observables.update_norm"]["field"] == "update_norm" for event in events)
    assert all(event["source_pointers"]["step"]["aligned_sample_start"] == trace[index]["output_start"] for index, event in enumerate(events))
    assert all(event["source_pointers"]["step"]["aligned_sample_end"] == trace[index]["output_end"] for index, event in enumerate(events))
    assert all(not {"h", "true_h", "true_jones", "fixed_label_ber", "pi_ber"}.intersection(event) for event in events)


@pytest.mark.parametrize(
    "forbidden",
    ["h", "true_h", "true_jones", "fixed_label_ber", "pi_ber", "theta", "bitsX", "bitsY", "oracle", "post_hoc", "future_state"],
)
def test_adapter_rejects_oracle_or_posthoc_trace_fields(forbidden: str) -> None:
    trace = _actual_standard_cma_trace()
    trace[0][forbidden] = 1.0
    with pytest.raises(ValueError, match="forbidden"):
        u25.adapt_standard_cma_trace(
            trace,
            sequence_id="smoke-standard-cma",
            source_id="run_b001._default_runner.blind_trace",
            lock_score_threshold=0.90,
            divergence_error_threshold=0.20,
        )


def test_adapter_rejects_future_window_field() -> None:
    trace = _actual_standard_cma_trace()
    trace[0]["future_window"] = [1.0]
    with pytest.raises(ValueError, match="forbidden"):
        u25.adapt_standard_cma_trace(
            trace,
            sequence_id="smoke-standard-cma",
            source_id="run_b001._default_runner.blind_trace",
            lock_score_threshold=0.90,
            divergence_error_threshold=0.20,
        )


@pytest.mark.parametrize("forbidden", ["oracle", "post_hoc_ber", "future_state"])
def test_event_validator_rejects_extra_runtime_observable(forbidden: str) -> None:
    event = _event()
    event["observables"][forbidden] = 1.0
    with pytest.raises(ValueError, match="unsupported observables"):
        u25.validate_event(event)
