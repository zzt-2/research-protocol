from argparse import ArgumentParser
from collections.abc import Mapping
from pathlib import Path

import yaml


CONTROL_START = "<!-- RDL-CONTROL:START -->"
CONTROL_END = "<!-- RDL-CONTROL:END -->"
TASK_START = "<!-- RDL-TASK-CONTROL:START -->"
TASK_END = "<!-- RDL-TASK-CONTROL:END -->"

CONTROL_FIELDS_V1 = {
    "schema_version",
    "control_epoch",
    "role",
    "mission",
    "active_lane",
    "authority_pointer",
    "decision_gate",
    "allowed_actions",
    "forbidden_actions",
    "next_legal_action",
}
CONTROL_FIELDS_V2 = CONTROL_FIELDS_V1 | {
    "mission_log_ref",
    "mission_checkpoint",
}
TASK_FIELDS_V1 = {
    "schema_version",
    "control_ref",
    "control_epoch",
    "action_class",
}
TASK_FIELDS_V2 = TASK_FIELDS_V1 | {"mission_checkpoint"}


def _extract_marked_mapping(
    path: Path,
    start_marker: str,
    end_marker: str,
    root_key: str,
    label: str,
) -> tuple[Mapping[str, object] | None, list[str]]:
    text = path.read_text(encoding="utf-8")
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        return None, [f"{label}_marker_count"]

    body = text.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    if body.startswith("```yaml"):
        body = body[len("```yaml") :].strip()
    if body.endswith("```"):
        body = body[: -len("```")].strip()

    try:
        parsed = yaml.safe_load(body)
    except yaml.YAMLError:
        return None, [f"{label}_yaml_invalid"]
    if not isinstance(parsed, Mapping):
        return None, [f"{label}_document_not_mapping"]
    if root_key not in parsed:
        return None, [f"{label}_root_missing:{root_key}"]
    payload = parsed[root_key]
    if not isinstance(payload, Mapping):
        return None, [f"{label}_root_not_mapping:{root_key}"]
    return payload, []


def _schema_errors(
    payload: Mapping[str, object],
    required_fields: set[str],
    label: str,
) -> list[str]:
    actual = set(payload)
    errors = [
        *(f"{label}_missing_field:{field}" for field in required_fields - actual),
        *(f"{label}_unknown_field:{field}" for field in actual - required_fields),
    ]
    return sorted(errors)


def validate_task_control(repo_root: Path, task_path: Path) -> list[str]:
    repo_root = repo_root.resolve()
    task_path = task_path.resolve()

    task, errors = _extract_marked_mapping(
        task_path,
        TASK_START,
        TASK_END,
        "rdl_task_control",
        "task",
    )
    if errors:
        return errors
    task_schema = task.get("schema_version")
    if task_schema == "rdl.task-control.v1":
        task_fields = TASK_FIELDS_V1
    elif task_schema == "rdl.task-control.v2":
        task_fields = TASK_FIELDS_V2
    else:
        return [f"task_schema_unsupported:{task_schema}"]
    errors = _schema_errors(task, task_fields, "task")
    if errors:
        return errors

    control_ref = task["control_ref"]
    if not isinstance(control_ref, str):
        return ["task_field_type:control_ref"]
    relative_ref = Path(control_ref)
    if relative_ref.is_absolute():
        return ["control_ref_outside_repo"]
    control_path = (repo_root / relative_ref).resolve()
    try:
        control_path.relative_to(repo_root)
    except ValueError:
        return ["control_ref_outside_repo"]
    if not control_path.is_file():
        return [f"missing_control_ref:{control_ref}"]

    control, errors = _extract_marked_mapping(
        control_path,
        CONTROL_START,
        CONTROL_END,
        "rdl_control",
        "control",
    )
    if errors:
        return errors
    control_schema = control.get("schema_version")
    if control_schema == "rdl.foreground-control.v1":
        control_fields = CONTROL_FIELDS_V1
        expected_task_schema = "rdl.task-control.v1"
    elif control_schema == "rdl.foreground-control.v2":
        control_fields = CONTROL_FIELDS_V2
        expected_task_schema = "rdl.task-control.v2"
    else:
        return [f"control_schema_unsupported:{control_schema}"]
    errors = _schema_errors(control, control_fields, "control")
    if errors:
        return errors
    if task_schema != expected_task_schema:
        return ["control_task_schema_mismatch"]

    task_epoch = task["control_epoch"]
    control_epoch = control["control_epoch"]
    if (
        not isinstance(task_epoch, int)
        or isinstance(task_epoch, bool)
        or not isinstance(control_epoch, int)
        or isinstance(control_epoch, bool)
    ):
        return ["control_epoch_type"]
    if task_epoch != control_epoch:
        return ["stale_control_epoch"]

    action_class = task["action_class"]
    allowed = control["allowed_actions"]
    forbidden = control["forbidden_actions"]
    if not isinstance(action_class, str):
        return ["task_field_type:action_class"]
    if not isinstance(allowed, list) or not all(
        isinstance(item, str) for item in allowed
    ):
        return ["control_field_type:allowed_actions"]
    if not isinstance(forbidden, list) or not all(
        isinstance(item, str) for item in forbidden
    ):
        return ["control_field_type:forbidden_actions"]
    if action_class in forbidden:
        return [f"forbidden_action:{action_class}"]
    if action_class not in allowed:
        return [f"action_not_allowed:{action_class}"]

    if control_schema == "rdl.foreground-control.v2":
        mission_log_ref = control["mission_log_ref"]
        if not isinstance(mission_log_ref, str):
            return ["control_field_type:mission_log_ref"]
        relative_log = Path(mission_log_ref)
        if relative_log.is_absolute():
            return ["mission_log_ref_outside_repo"]
        mission_log_path = (repo_root / relative_log).resolve()
        try:
            mission_log_path.relative_to(repo_root)
        except ValueError:
            return ["mission_log_ref_outside_repo"]
        if not mission_log_path.is_file():
            return [f"missing_mission_log:{mission_log_ref}"]

        task_checkpoint = task["mission_checkpoint"]
        control_checkpoint = control["mission_checkpoint"]
        if (
            not isinstance(task_checkpoint, str)
            or not task_checkpoint.strip()
            or not isinstance(control_checkpoint, str)
            or not control_checkpoint.strip()
        ):
            return ["mission_checkpoint_type"]
        if task_checkpoint != control_checkpoint:
            return ["stale_mission_checkpoint"]
    return []


def _main() -> int:
    parser = ArgumentParser(
        description="Validate an RDL task against its foreground control block."
    )
    parser.add_argument("task_path", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    errors = validate_task_control(args.repo_root, args.task_path)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
