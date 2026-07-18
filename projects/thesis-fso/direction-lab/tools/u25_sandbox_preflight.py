"""P01 Sandbox-readiness preflight.

This is a governance smoke only.  It executes one tiny in-memory call through
the existing standard-CMA adapter to inspect real blind-trace fields, but it
does not create a result artifact, performance cell, receipt, or ledger entry.
"""

from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
LAB_ROOT = HERE.parents[1]
REPO_ROOT = HERE.parents[4]
SIM_ROOT = REPO_ROOT / "projects" / "simulation"
B003_ARTIFACT = LAB_ROOT / "batches" / "B003-20260718-live" / "artifacts" / "result.json"


def _load_sibling(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_first_b003_trace() -> list[dict[str, Any]]:
    """Stream only the first immutable B003 cell trace from the large artifact."""

    trace_lines = ["["]
    started = False
    key_indent = -1
    with B003_ARTIFACT.open(encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip(" "))
            if not started:
                if stripped == '"trace": [':
                    started = True
                    key_indent = indent
                continue
            if indent == key_indent and stripped in {"]", "],"}:
                trace_lines.append("]")
                break
            trace_lines.append(line)
    if not started or trace_lines[-1] != "]":
        raise RuntimeError("B003 artifact does not contain a complete first-cell trace")
    value = json.loads("".join(trace_lines))
    if not isinstance(value, list) or not value:
        raise RuntimeError("B003 first-cell trace is empty")
    return value


def evaluate_u25_readiness() -> dict[str, Any]:
    """Return a deterministic A/B decision without creating Sandbox output."""

    contract = _load_sibling(LAB_ROOT / "tools" / "u25_action_contract.py", "u25_contract_preflight")
    run_b001 = _load_sibling(LAB_ROOT / "tools" / "run_b001.py", "run_b001_preflight")
    runner, config_factory = run_b001._default_runner(run_b001.DEFAULT_SOURCE_ROOT)
    del config_factory
    trace = _load_first_b003_trace()
    source_id = str(B003_ARTIFACT.relative_to(REPO_ROOT)).replace("\\", "/") + "::cells[0].trace"
    events = contract.adapt_standard_cma_trace(
        trace,
        sequence_id="u25-preflight-standard-cma",
        source_id=source_id,
        lock_score_threshold=0.90,
        divergence_error_threshold=0.20,
    )

    runner_parameters = set(inspect.signature(runner).parameters)
    source_text = (LAB_ROOT / "tools" / "run_v3.py").read_text(encoding="utf-8")
    has_state_snapshot = any("state_snapshot" in row for row in trace)
    has_action_hook = "action" in runner_parameters or "action_hook" in runner_parameters
    generic_dispatch = "candidate_adapter_registry" in source_text and "action_registry" in source_text
    blockers: list[str] = []
    if not has_state_snapshot:
        blockers.append("STATE_SNAPSHOT_MISSING")
    if not has_action_hook:
        blockers.append("ACTION_EFFECT_NOT_OBSERVABLE")
    if "component.ml_degradation_detector.batch-v3" in source_text or not generic_dispatch:
        blockers.append("RUNNER_U24_HARDCODED")

    return {
        "status": "P01_SANDBOX_READY" if not blockers else "P01_BLOCKED",
        "blockers": blockers,
        "trace_adapter": {
            "status": "PASS",
            "trace_rows": len(trace),
            "event_rows": len(events),
            "input_source": source_id,
            "runtime_fields": ["output_start", "output_end", "cm_error", "output_power", "update_norm"],
            "training_or_evaluation_only": ["sX", "sY", "h", "theta", "bitsX", "bitsY", "fixed_label_ber", "pi_ber"],
        },
        "fork_replay": {
            "status": "BLOCKED",
            "same_realization": "NOT_REACHED",
            "same_pre_trigger_state": False,
            "no_op_bit_exact": "NOT_REACHED",
            "fixed_safe_policy": "NOT_REACHED",
            "single_action": "NOT_REACHED",
            "reason": "standard-CMA runner exposes online/frozen diagnostic branches but no per-decision action hook or receiver state snapshot",
        },
        "runner": {
            "signature": str(inspect.signature(runner)),
            "has_action_hook": has_action_hook,
            "generic_candidate_dispatch": generic_dispatch,
            "source_file": str(Path(runner._source_files[0]).resolve()),
        },
        "formal_performance_run": False,
        "sandbox_queue_created": False,
        "reusable_assets": [
            "standard_cma_blind_trace",
            "u25_event_schema_and_source_pointers",
            "fixed_safe_policy_contract",
            "deterministic_replay_contract",
            "prompt013_online_frozen_diagnostic_branch",
        ],
        "next_candidate": "P02/U10 event-library Scout (or P03/U19 residual-headroom Scout)",
    }


def main() -> int:
    report = evaluate_u25_readiness()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "P01_SANDBOX_READY" else 2


if __name__ == "__main__":  # pragma: no cover - exercised by the command gate
    raise SystemExit(main())
