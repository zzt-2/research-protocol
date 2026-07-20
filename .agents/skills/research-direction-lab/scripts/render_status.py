from collections.abc import Mapping
import json


def _json_block(value: object) -> str:
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return f"```json\n{serialized}\n```"


def render_status(
    adapter: Mapping,
    state: Mapping,
    portfolio: Mapping,
    harvest: Mapping,
) -> str:
    recorded_next_action = state.get("recorded_next_action")
    if not isinstance(recorded_next_action, str) or not recorded_next_action.strip():
        next_action_text = "None recorded."
    else:
        next_action_text = recorded_next_action

    sections = [
        "# Research Direction Lab Status",
        "## Formal Goal and Authorization",
        _json_block(adapter.get("formal_goal", {})),
        "## Anchor",
        _json_block(adapter.get("anchor", {})),
        "## Current State",
        _json_block(dict(state)),
        "## Portfolio",
        _json_block(dict(portfolio)),
        "## Harvest",
        _json_block(dict(harvest)),
        "## Recorded Next Action",
        next_action_text,
    ]
    return "\n\n".join(sections) + "\n"
