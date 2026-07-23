from pathlib import Path
import sys

import yaml


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_task_control import validate_task_control


CONTROL_START = "<!-- RDL-CONTROL:START -->"
CONTROL_END = "<!-- RDL-CONTROL:END -->"
TASK_START = "<!-- RDL-TASK-CONTROL:START -->"
TASK_END = "<!-- RDL-TASK-CONTROL:END -->"


def write_marked_yaml(path, start, end, root_key, payload):
    body = yaml.safe_dump(
        {root_key: payload},
        allow_unicode=True,
        sort_keys=False,
    ).strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"{start}\n```yaml\n{body}\n```\n{end}\n",
        encoding="utf-8",
    )


def valid_control():
    return {
        "schema_version": "rdl.foreground-control.v1",
        "control_epoch": 1,
        "role": "SYSTEM_DESIGN",
        "mission": "design and validate the long-horizon protocol",
        "active_lane": "PROTOCOL_IMPLEMENTATION",
        "authority_pointer": ".sessions/example/decisions.md#D001",
        "decision_gate": "implementation not verified",
        "allowed_actions": [
            "PROTOCOL_IMPLEMENTATION",
            "PROTOCOL_VERIFICATION",
        ],
        "forbidden_actions": ["SCIENTIFIC_DISPATCH"],
        "next_legal_action": "implement and verify the minimal guard",
    }


def write_control(repo_root, payload=None, relative=".sessions/example/topic-index.md"):
    path = repo_root / relative
    write_marked_yaml(
        path,
        CONTROL_START,
        CONTROL_END,
        "rdl_control",
        valid_control() if payload is None else payload,
    )
    return path


def write_task(repo_root, payload=None):
    task = {
        "schema_version": "rdl.task-control.v1",
        "control_ref": ".sessions/example/topic-index.md",
        "control_epoch": 1,
        "action_class": "PROTOCOL_IMPLEMENTATION",
    }
    if payload:
        task.update(payload)
    path = repo_root / ".sessions/example/T001-example.md"
    write_marked_yaml(path, TASK_START, TASK_END, "rdl_task_control", task)
    return path


def test_matching_epoch_and_allowed_action_passes(tmp_path):
    write_control(tmp_path)
    task_path = write_task(tmp_path)

    assert validate_task_control(tmp_path, task_path) == []


def test_stale_epoch_is_rejected(tmp_path):
    write_control(tmp_path)
    task_path = write_task(tmp_path, {"control_epoch": 0})

    assert validate_task_control(tmp_path, task_path) == ["stale_control_epoch"]


def test_forbidden_action_is_rejected_even_if_listed_allowed(tmp_path):
    control = valid_control()
    control["allowed_actions"].append("SCIENTIFIC_DISPATCH")
    write_control(tmp_path, control)
    task_path = write_task(tmp_path, {"action_class": "SCIENTIFIC_DISPATCH"})

    assert validate_task_control(tmp_path, task_path) == [
        "forbidden_action:SCIENTIFIC_DISPATCH"
    ]


def test_missing_control_reference_is_rejected(tmp_path):
    task_path = write_task(
        tmp_path,
        {"control_ref": ".sessions/example/missing.md"},
    )

    assert validate_task_control(tmp_path, task_path) == [
        "missing_control_ref:.sessions/example/missing.md"
    ]


def test_control_block_rejects_unknown_or_missing_fields(tmp_path):
    control = valid_control()
    del control["mission"]
    control["candidate"] = "must-not-live-here"
    write_control(tmp_path, control)
    task_path = write_task(tmp_path)

    assert validate_task_control(tmp_path, task_path) == [
        "control_missing_field:mission",
        "control_unknown_field:candidate",
    ]


def test_task_reference_cannot_escape_repo_root(tmp_path):
    outside = tmp_path.parent / "outside-topic-index.md"
    write_marked_yaml(
        outside,
        CONTROL_START,
        CONTROL_END,
        "rdl_control",
        valid_control(),
    )
    task_path = write_task(tmp_path, {"control_ref": "../outside-topic-index.md"})

    assert validate_task_control(tmp_path, task_path) == [
        "control_ref_outside_repo"
    ]
