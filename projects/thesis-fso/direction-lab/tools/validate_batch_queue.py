"""Static gate for replacement Direction Lab batch queues.

This validator reads governance and source files only.  It never imports the
runner or executes a batch.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


class ValidationReport:
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors

    @property
    def passed(self) -> bool:
        return not self.errors


def load_queue(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("batch queue root must be a mapping")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _repo_root(path: Path) -> Path:
    for parent in (path.parent, *path.parents):
        if (parent / ".git").exists():
            return parent
    for parent in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
        if (parent / ".git").exists():
            return parent
    return path.parents[3]


def _resolve(queue_path: Path, reference: str) -> Path:
    path = Path(reference)
    if path.is_absolute():
        return path
    local = queue_path.parent / path
    if local.exists() or len(path.parts) == 1:
        return local
    return _repo_root(queue_path) / path


def _validate_bound_file(
    errors: list[str], queue_path: Path, lineage: Mapping[str, Any], *,
    file_key: str, sha_key: str, label: str,
) -> tuple[Path | None, dict[str, Any] | None]:
    reference = lineage.get(file_key)
    if not reference:
        errors.append(f"{label} file binding is missing")
        return None, None
    path = _resolve(queue_path, str(reference))
    if not path.is_file():
        errors.append(f"{label} file not found: {path}")
        return path, None
    actual = _sha256(path)
    if lineage.get(sha_key) != actual:
        errors.append(f"{label} SHA mismatch: recorded={lineage.get(sha_key)}, actual={actual}")
    try:
        return path, load_queue(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"{label} file is invalid: {exc}")
        return path, None


def _validate_bindings(data: Mapping[str, Any], queue_path: Path) -> list[str]:
    errors: list[str] = []
    lineage = data.get("lineage")
    if not isinstance(lineage, Mapping):
        return ["queue lineage must be a mapping"]

    _validate_bound_file(
        errors, queue_path, lineage, file_key="v1_file", sha_key="v1_file_sha256", label="v1 queue"
    )
    _, universe = _validate_bound_file(
        errors, queue_path, lineage,
        file_key="candidate_universe_v2_file", sha_key="candidate_universe_v2_sha256",
        label="universe",
    )
    _, candidate_map = _validate_bound_file(
        errors, queue_path, lineage,
        file_key="candidate_map_v2_file", sha_key="candidate_map_v2_sha256",
        label="map",
    )
    if universe is not None and data.get("universe_id") != universe.get("universe_id"):
        errors.append(
            f"universe ID mismatch: queue={data.get('universe_id')}, universe={universe.get('universe_id')}"
        )
    if candidate_map is not None:
        if data.get("map_id") != candidate_map.get("map_id"):
            errors.append(f"map ID mismatch: queue={data.get('map_id')}, map={candidate_map.get('map_id')}")
        if data.get("universe_id") != candidate_map.get("universe_id"):
            errors.append("map/universe ID mismatch")
        map_gate = candidate_map.get("map_gate", {})
        if candidate_map.get("status") != "PASS" or not isinstance(map_gate, Mapping) or map_gate.get("verdict") != "PASS":
            errors.append("candidate Map PASS is required")
    return errors


def _required_contract_from_runner(data: Mapping[str, Any], queue_path: Path) -> set[str]:
    queue_gate = data.get("queue_gate", {})
    runner_ref = str(queue_gate.get("runner", "")) if isinstance(queue_gate, Mapping) else ""
    runner_file = runner_ref.rsplit(":", 1)[0]
    runner_path = _resolve(queue_path, runner_file)
    if not runner_path.is_file():
        return set()
    for node in ast.parse(runner_path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "REQUIRED_CONTRACT" for target in node.targets
        ):
            required = set(ast.literal_eval(node.value))
            # v3 adds an explicit physical/channel contract.  Keep the v2
            # validator behavior immutable while making the new snapshot gate
            # enforce the additional fields instead of merely documenting them.
            if str(data.get("schema_version", "")).endswith(".v3"):
                for candidate in ast.parse(runner_path.read_text(encoding="utf-8")).body:
                    if isinstance(candidate, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == "EXPLICIT_RUNTIME_CONTRACT"
                        for target in candidate.targets
                    ):
                        required.update(ast.literal_eval(candidate.value))
                        break
            return required
    return set()


def _validate_batch(data: Mapping[str, Any], queue_path: Path) -> list[str]:
    errors: list[str] = []
    batches = data.get("batches")
    if not isinstance(batches, list):
        return ["batches must be a list"]
    if str(data.get("schema_version", "")).endswith(".v3") and not data.get("batch_id"):
        return ["v3 queue requires an explicit top-level batch_id; implicit first-batch selection is forbidden"]
    target_batch_id = str(data.get("batch_id") or (batches[0].get("batch_id") if batches else "B002"))
    matches = [batch for batch in batches if isinstance(batch, Mapping) and batch.get("batch_id") == target_batch_id]
    if len(matches) != 1:
        return [f"queue must contain exactly one {target_batch_id} batch"]
    batch = matches[0]
    if batch.get("sandbox_only") is not True:
        errors.append("sandbox_only must be true")
    if batch.get("promotion_allowed") is not False:
        errors.append("promotion_allowed must be false")
    if batch.get("state") != "QUEUED_NOT_RUN":
        errors.append("state must be QUEUED_NOT_RUN")

    map_matches = False
    lineage = data.get("lineage", {})
    if isinstance(lineage, Mapping) and lineage.get("candidate_map_v2_file"):
        map_path = _resolve(queue_path, str(lineage["candidate_map_v2_file"]))
        if map_path.is_file():
            candidate_map = load_queue(map_path)
            family = next(
                (item for item in candidate_map.get("families", []) if item.get("id") == "F05"), {}
            )
            candidate = next(
                (item for item in candidate_map.get("ranked_shortlist", []) if item.get("id") == "U24"), {}
            )
            map_matches = "U24" in family.get("members", []) and candidate.get("classification") == "BATCH_1_FAMILY"
    if batch.get("family_id") != "F05" or batch.get("archetype_id") != "U24" or not map_matches:
        errors.append(f"{target_batch_id} must bind U24 in F05 with BATCH_1_FAMILY")
    candidates = batch.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 3:
        errors.append(f"{target_batch_id} must contain exactly three candidates")
        candidates = candidates if isinstance(candidates, list) else []
    candidate_ids = [str(item.get("candidate_id")) for item in candidates if isinstance(item, Mapping)]
    mechanisms = [str(item.get("mechanism", "")).strip() for item in candidates if isinstance(item, Mapping)]
    if len(set(candidate_ids)) != len(candidate_ids) or len(set(mechanisms)) != len(mechanisms):
        errors.append(f"{target_batch_id} requires three distinct mechanisms and candidate IDs")
    if "C24-SSL-AE-UNLABELED" not in candidate_ids:
        errors.append(f"{target_batch_id} must include C24-SSL-AE-UNLABELED")
    else:
        index = candidate_ids.index("C24-SSL-AE-UNLABELED")
        if "unlabeled" not in mechanisms[index].lower():
            errors.append("C24-SSL-AE-UNLABELED mechanism must be truly unlabeled")

    shared = batch.get("shared_contract")
    if not isinstance(shared, Mapping):
        errors.append(f"{target_batch_id} shared_contract must be a mapping")
        shared = {}
    required_contract = _required_contract_from_runner(data, queue_path)
    missing_contract = sorted(required_contract - set(shared))
    if not required_contract or missing_contract:
        label = "runner contract (including explicit runtime)" if str(data.get("schema_version", "")).endswith(".v3") else "run_v2.REQUIRED_CONTRACT"
        errors.append(f"shared contract must contain {label}: missing={missing_contract}")
    if str(data.get("schema_version", "")).endswith(".v3"):
        effects = shared.get("runtime_field_effects")
        expected_effects = {
            "channel_block": "operative",
            "r2": "operative",
            "fade_threshold_h": "audit_only",
            "clip_norm": "audit_only",
            "t_s": "operative",
            "method": "operative",
        }
        if not isinstance(effects, Mapping):
            errors.append("v3 runtime_field_effects must be a mapping")
        else:
            for field, expected_effect in expected_effects.items():
                declaration = effects.get(field)
                actual_effect = declaration.get("effect") if isinstance(declaration, Mapping) else None
                consumer = declaration.get("consumer") if isinstance(declaration, Mapping) else None
                if actual_effect != expected_effect or not str(consumer or "").strip():
                    errors.append(
                        "v3 runtime_field_effects mismatch for "
                        f"{field}: expected={expected_effect}, actual={actual_effect}, consumer={consumer}"
                    )
    try:
        numeric_positive = (
            int(shared.get("n_symbols", 0)) > 0
            and int(shared.get("block_size", 0)) > 0
            and int(shared.get("cma_taps", 0)) > 0
            and float(shared.get("cma_mu", 0)) > 0
            and all(
                math.isfinite(float(shared.get(key)))
                for key in ("alpha", "beta", "f_g_hz", "snr_db")
            )
        )
    except (TypeError, ValueError):
        numeric_positive = False
    if str(shared.get("modulation", "")).upper() != "QPSK" or not numeric_positive or not shared.get("rates"):
        errors.append("shared contract is invalid")
    if shared.get("baseline_id") != "baseline.standard_cma.godard_z":
        errors.append("standard-CMA Godard-Z baseline is required; current-CMA/no-Z is forbidden")
    train_seeds = list(shared.get("train_seeds", []))
    test_seeds = list(shared.get("test_seeds", []))
    if not train_seeds or not test_seeds:
        errors.append("shared train/test seeds are required")
    overlap = sorted(set(train_seeds) & set(test_seeds))
    if overlap:
        errors.append(f"train/test seed overlap is forbidden: {overlap}")
    if len(set(train_seeds)) != len(train_seeds) or len(set(test_seeds)) != len(test_seeds):
        errors.append("shared train/test seeds must be unique")
    metrics = batch.get("metrics")
    if not isinstance(metrics, Mapping) or not metrics.get("primary") or not metrics.get("required_signal_metrics"):
        errors.append("shared metrics are required")
    if not shared.get("resource_budget"):
        errors.append("shared resource budget is required")
    override_keys = set(shared) | {"metrics", "resource_budget", "train_seeds", "test_seeds", "baseline_id"}
    for candidate in candidates:
        if isinstance(candidate, Mapping):
            override = sorted(set(candidate) & override_keys)
            if override:
                errors.append(
                    f"candidate-level shared-contract override is forbidden for {candidate.get('candidate_id')}: {override}"
                )
        if not isinstance(candidate, Mapping) or not str(candidate.get("hypothesis", "")).strip():
            errors.append("every candidate hypothesis must be preregistered")

    outcomes = batch.get("preregistered_outcomes")
    required_outcomes = {
        "minimum_information", "advance_specific_mechanism", "retire_specific_mechanism",
        "otherwise", "no_family_wide_kill",
    }
    if not isinstance(outcomes, Mapping) or not required_outcomes.issubset(outcomes):
        errors.append("Go/Kill and minimum-information outcomes must be preregistered")
    if isinstance(outcomes, Mapping):
        for rule in (
            "minimum_information", "advance_specific_mechanism",
            "retire_specific_mechanism", "otherwise",
        ):
            if not str(outcomes.get(rule, "")).strip():
                errors.append(f"preregistered outcome must be non-empty: {rule}")
        if outcomes.get("no_family_wide_kill") is not True:
            errors.append("no_family_wide_kill must be true")
    if not str(batch.get("valid_domain", "")).strip():
        errors.append("valid_domain must be explicit")
    required_signal_metrics = {"fixed_label_ber", "permutation_invariant_ber"}
    required_primary_metrics = {"cell_recall_before_or_at_oracle", "control_cell_false_alarm_rate"}
    if not isinstance(metrics, Mapping) or not required_signal_metrics.issubset(metrics.get("required_signal_metrics", [])):
        errors.append("required signal metrics must include fixed_label_ber and permutation_invariant_ber")
    if not isinstance(metrics, Mapping) or not required_primary_metrics.issubset(metrics.get("primary", [])):
        errors.append("primary metrics must include recall and control false-alarm")

    controller = batch.get("controller", {})
    expected_controller = {
        "action": "RUN", "state": "BATCH_READY", "evidence_status": "EXPLORATORY",
        "destination": "evidence_ledger",
    }
    for field, expected in expected_controller.items():
        if not isinstance(controller, Mapping) or controller.get(field) != expected:
            errors.append(
                f"controller contract mismatch for {field}: expected={expected}, "
                f"actual={controller.get(field) if isinstance(controller, Mapping) else None}"
            )
    return errors


def _registry_components(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    components = registry.get("components", [])
    return {
        str(component["id"]): component
        for component in components
        if isinstance(component, Mapping) and component.get("id")
    }


def _validate_runtime(data: Mapping[str, Any], queue_path: Path) -> list[str]:
    errors: list[str] = []
    queue_gate = data.get("queue_gate")
    if not isinstance(queue_gate, Mapping):
        return ["queue_gate must be a mapping"]
    runner_ref = str(queue_gate.get("runner", ""))
    if ":" not in runner_ref:
        errors.append("runner must declare path:entrypoint")
        runner_file_ref, entrypoint = runner_ref, ""
    else:
        runner_file_ref, entrypoint = runner_ref.rsplit(":", 1)
    runner_path = _resolve(queue_path, runner_file_ref)
    runner_sha = None
    if not runner_path.is_file():
        errors.append(f"runner file not found: {runner_path}")
    else:
        runner_sha = _sha256(runner_path)
        if queue_gate.get("runner_sha256") != runner_sha:
            errors.append(
                f"runner SHA mismatch: recorded={queue_gate.get('runner_sha256')}, actual={runner_sha}"
            )
        functions = {
            node.name for node in ast.parse(runner_path.read_text(encoding="utf-8")).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if entrypoint not in functions:
            errors.append(f"runner entrypoint not found: {entrypoint}")

    registry_ref = str(queue_gate.get("registry", ""))
    registry_path = _resolve(queue_path, registry_ref)
    if not registry_path.is_file():
        errors.append(f"registry file not found: {registry_path}")
        return errors
    registry_sha = _sha256(registry_path)
    if queue_gate.get("registry_sha256") != registry_sha:
        errors.append(
            f"registry SHA mismatch: recorded={queue_gate.get('registry_sha256')}, actual={registry_sha}"
        )
    registry = load_queue(registry_path)
    components = _registry_components(registry)
    runner_version = "v3" if str(data.get("schema_version", "")).endswith(".v3") else "v2"
    runner_component = components.get(f"runner.direction_lab.replacement-{runner_version}")
    if runner_sha is not None and (
        runner_component is None
        or runner_component.get("fingerprint") != runner_sha
        or runner_component.get("entrypoint") != runner_ref
    ):
        errors.append("registry runner fingerprint mismatch")

    detector_component = components.get(f"component.ml_degradation_detector.batch-{runner_version}")
    tool_dir = queue_path.parent / "tools"
    detector_files = [tool_dir / "ml_detector_batch.py", tool_dir / "unlabeled_control_reconstruction.py"]
    if all(path.is_file() for path in detector_files):
        detector_fp = hashlib.sha256("".join(_sha256(path) for path in detector_files).encode()).hexdigest()
        if detector_component is None or detector_component.get("fingerprint") != detector_fp:
            errors.append("registry detector fingerprint mismatch")
    else:
        errors.append("detector source file not found")
    if runner_version == "v3":
        helper_bindings = {
            "runner.direction_lab.replacement-v2-helper": "projects/thesis-fso/direction-lab/tools/run_v2.py",
            "runner.direction_lab.legacy-b001-helper": "projects/thesis-fso/direction-lab/tools/run_b001.py",
            "controller.direction_lab.pilot-v3": "projects/simulation/verify/direction_lab_pilot/controller.py",
            "validator.direction_lab.queue-gate-v3": "projects/thesis-fso/direction-lab/tools/validate_batch_queue.py",
        }
        for component_id, reference in helper_bindings.items():
            component = components.get(component_id)
            helper_path = _resolve(queue_path, reference)
            if component is None or not helper_path.is_file() or component.get("fingerprint") != _sha256(helper_path):
                errors.append(f"registry helper fingerprint mismatch: {component_id}")
    return errors


def validate_queue(data: Mapping[str, Any], *, queue_path: str | Path | None = None) -> ValidationReport:
    if queue_path is None:
        return ValidationReport(["queue_path is required for binding validation"])
    path = Path(queue_path)
    errors = _validate_bindings(data, path)
    errors.extend(_validate_batch(data, path))
    errors.extend(_validate_runtime(data, path))
    queue_gate = data.get("queue_gate", {})
    required_flags = {
        "candidate_universe_v2_bound", "candidate_map_v2_bound", "map_gate_required",
        "multiple_distinct_mechanisms", "shared_baseline_seed_metrics_budget",
        "hypotheses_and_exit_rules_preregistered", "valid_domain_explicit",
        "standard_cma_godard_z_only", "current_cma_no_z_forbidden", "source_snapshot_frozen",
    }
    if not isinstance(queue_gate, Mapping) or any(queue_gate.get(flag) is not True for flag in required_flags):
        errors.append("all queue gate declarations must be true")
    pending_state = (
        data.get("status") == "GATE_PENDING"
        and isinstance(queue_gate, Mapping)
        and queue_gate.get("independent_review") == "PENDING"
        and queue_gate.get("verdict") == "PENDING"
    )
    pass_state = (
        data.get("status") == "PASS"
        and isinstance(queue_gate, Mapping)
        and queue_gate.get("independent_review") == "PASS"
        and queue_gate.get("verdict") == "PASS"
    )
    if not pending_state and not pass_state:
        errors.append("queue lifecycle state is inconsistent")
    elif pass_state:
        evidence_anchor = "V012" if str(data.get("schema_version", "")).endswith(".v3") else "V010"
        expected_evidence = (
            ".sessions/2026-07-17-direction-lab-governance-pilot/"
            f"verifications.md#{evidence_anchor}"
        )
        if not str(queue_gate.get("verifier_scope", "")).strip() or queue_gate.get(
            "verifier_evidence"
        ) != expected_evidence:
            errors.append(f"PASS lifecycle requires verifier_scope and {evidence_anchor} evidence")
    return ValidationReport(errors)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue_path", type=Path)
    args = parser.parse_args(argv)
    report = validate_queue(load_queue(args.queue_path), queue_path=args.queue_path)
    if report.passed:
        print(f"PASS: {args.queue_path}")
        return 0
    print(f"FAIL: {args.queue_path}")
    for error in report.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
