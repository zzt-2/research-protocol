import argparse
from collections.abc import Mapping
import json
from pathlib import Path
import sys

import yaml


MAX_INLINE_BYTES = 360
MAX_IDENTIFIER_BYTES = 96
MAX_FINDING_BYTES = 180
MAX_POINTER_BYTES = 220
MAX_AXIS_ITEMS = 12
MAX_HARVEST_ITEMS = 9


def _bounded_text(value: object, max_bytes: int = MAX_INLINE_BYTES) -> str:
    text = str(value)
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    marker = "..."
    prefix = encoded[: max_bytes - len(marker)]
    while prefix:
        try:
            return prefix.decode("utf-8") + marker
        except UnicodeDecodeError:
            prefix = prefix[:-1]
    return marker


def _bounded_structure(value: object) -> object:
    if isinstance(value, str):
        return _bounded_text(value)
    if isinstance(value, Mapping):
        items = list(value.items())
        bounded = {
            _bounded_text(key, MAX_IDENTIFIER_BYTES): _bounded_structure(item)
            for key, item in items[:12]
        }
        if len(items) > 12:
            bounded["..."] = f"{len(items) - 12} more entries"
        return bounded
    if isinstance(value, (list, tuple)):
        bounded = [_bounded_structure(item) for item in value[:12]]
        if len(value) > 12:
            bounded.append(f"... {len(value) - 12} more items")
        return bounded
    return value


def _inline(value: object, max_bytes: int = MAX_INLINE_BYTES) -> str:
    if isinstance(value, str):
        return _bounded_text(value, max_bytes)
    serialized = json.dumps(
        _bounded_structure(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _bounded_text(serialized, max_bytes)


def _nonempty(value: object, fallback: str = "Not recorded.") -> str:
    if isinstance(value, str) and value.strip():
        return _bounded_text(value.strip())
    if value not in (None, "", [], {}):
        return _inline(value)
    return _bounded_text(fallback)


def _candidate_summary(portfolio: Mapping) -> list[str]:
    explicit = portfolio.get("current_focus")
    if isinstance(explicit, Mapping):
        candidate_id = _bounded_text(
            explicit.get("candidate_id", "unknown"), MAX_IDENTIFIER_BYTES
        )
        status = _bounded_text(explicit.get("status", "status not recorded"), 160)
        ceiling = explicit.get("claim_ceiling")
        suffix = (
            f"; claim ceiling={_bounded_text(ceiling, MAX_IDENTIFIER_BYTES)}"
            if ceiling
            else ""
        )
        return [f"- Current focus: {candidate_id} — {status}{suffix}"]

    candidates = portfolio.get("candidates", [])
    if not isinstance(candidates, list):
        return []
    summaries = []
    for candidate in candidates[:5]:
        if not isinstance(candidate, Mapping):
            continue
        candidate_id = _bounded_text(
            candidate.get("candidate_id", candidate.get("id", "unknown")),
            MAX_IDENTIFIER_BYTES,
        )
        status = _bounded_text(candidate.get("status", "status not recorded"), 160)
        summaries.append(f"- {candidate_id} — {status}")
    if len(candidates) > 5:
        summaries.append(f"- ... {len(candidates) - 5} more candidates; see portfolio pointer.")
    return summaries


def _harvest_summary(harvest: Mapping) -> list[str]:
    entries = harvest.get("entries", harvest.get("items", []))
    if not isinstance(entries, list):
        return []
    summaries = []
    for entry in entries[:MAX_HARVEST_ITEMS]:
        if not isinstance(entry, Mapping):
            continue
        item_id = _bounded_text(
            entry.get("id", entry.get("item_id", "unknown")), MAX_IDENTIFIER_BYTES
        )
        category = _bounded_text(
            entry.get("category", entry.get("kind", "uncategorized")),
            MAX_IDENTIFIER_BYTES,
        )
        finding = _bounded_text(
            entry.get("finding", "No summary recorded."), MAX_FINDING_BYTES
        )
        summaries.append(f"- {item_id} — {category}: {finding}")
    if len(entries) > MAX_HARVEST_ITEMS:
        summaries.append(
            f"- ... {len(entries) - MAX_HARVEST_ITEMS} more harvest entries; see ledger pointer."
        )
    return summaries


def _detail_pointers(adapter: Mapping) -> list[str]:
    paths = adapter.get("paths", {})
    if not isinstance(paths, Mapping):
        return []
    labels = (
        ("Current state", "current_state"),
        ("Portfolio", "candidates"),
        ("Batch plan", "batches"),
        ("Harvest ledger", "harvest_ledger"),
        ("Thesis spines", "thesis_spines"),
    )
    return [
        f"- {label}: `{_bounded_text(paths[key], MAX_POINTER_BYTES)}`"
        for label, key in labels
        if paths.get(key)
    ]


def _blocked_axis_summary(adapter: Mapping) -> str | None:
    axes = adapter.get("blocked_axes", [])
    if not isinstance(axes, list) or not axes:
        return None
    axis_ids = [
        _bounded_text(axis.get("axis_id", "unknown"), MAX_IDENTIFIER_BYTES)
        for axis in axes[:MAX_AXIS_ITEMS]
        if isinstance(axis, Mapping)
    ]
    if len(axes) > MAX_AXIS_ITEMS:
        axis_ids.append(f"... {len(axes) - MAX_AXIS_ITEMS} more axes")
    return _bounded_text(", ".join(axis_ids), 1200)


def _bounded_list_summary(value: object) -> object:
    if not isinstance(value, list):
        return value
    items = [_bounded_text(item, MAX_IDENTIFIER_BYTES) for item in value[:12]]
    if len(value) > 12:
        items.append(f"... {len(value) - 12} more items")
    return _bounded_text(", ".join(items))


def render_status(
    adapter: Mapping,
    state: Mapping,
    portfolio: Mapping,
    harvest: Mapping,
) -> str:
    formal_goal = adapter.get("formal_goal", {})
    if not isinstance(formal_goal, Mapping):
        formal_goal = {}
    anchor = adapter.get("anchor", {})
    if not isinstance(anchor, Mapping):
        anchor = {}

    recorded_next_action = state.get("recorded_next_action")
    if not isinstance(recorded_next_action, str) or not recorded_next_action.strip():
        next_action_text = "None recorded."
    else:
        next_action_text = _bounded_text(recorded_next_action.strip())

    formal_status = state.get("formal_authorization")
    currently_allowed = _bounded_list_summary(formal_goal.get("authorized_actions", []))

    portfolio_lines = _candidate_summary(portfolio)
    portfolio_summary = state.get("portfolio_and_blocked_axes")
    if portfolio_summary not in (None, "", [], {}):
        portfolio_lines.append(f"- Portfolio/blocked-axis summary: {_inline(portfolio_summary)}")
    blocked_axis_ids = _blocked_axis_summary(adapter)
    if blocked_axis_ids:
        portfolio_lines.append(f"- Blocked axis IDs: {blocked_axis_ids}")
    if not portfolio_lines:
        portfolio_lines = ["- No portfolio summary recorded."]

    latest_lines = []
    latest = state.get("latest_completed_batch")
    if latest not in (None, "", [], {}):
        latest_lines.append(f"- Latest completed batch: {_inline(latest)}")
    latest_scout = state.get("latest_scout_result")
    if latest_scout not in (None, "", [], {}):
        latest_lines.append(f"- Latest scout result: {_inline(latest_scout)}")
    if not latest_lines and state.get("completed_ids"):
        latest_lines.append(f"- Completed IDs: {_inline(state['completed_ids'])}")
    if state.get("last_event_head") not in (None, ""):
        latest_lines.append(f"- Last event head: {_inline(state['last_event_head'])}")
    if not latest_lines:
        latest_lines = ["- No completed scientific result recorded."]

    harvest_lines = _harvest_summary(harvest)
    if not harvest_lines:
        harvested_ids = state.get("harvested_material")
        harvest_lines = [f"- Harvest IDs: {_nonempty(harvested_ids)}"]

    no_experiment = state.get("no_new_experiment_running")
    experiment_line = (
        "- No new experiment is running."
        if no_experiment is True
        else f"- Experiment-running fact: {_nonempty(no_experiment)}"
    )

    sections = [
        "# Research Direction Lab Status",
        "## 1. Formal Goal and Authorization",
        f"- Goal: {_nonempty(state.get('formal_goal', formal_goal.get('statement')))}\n"
        f"- Formal status: {_nonempty(formal_status)}\n"
        f"- Currently allowed: {_nonempty(currently_allowed)}\n"
        f"- Prohibited actions: {_nonempty(formal_goal.get('prohibited_actions'))}",
        "## 2. Anchor or Baseline",
        f"- Scenario: {_nonempty(anchor.get('scenario'))}\n"
        f"- Baseline: {_nonempty(state.get('anchor_baseline', anchor.get('baseline_component')))}\n"
        f"- Metrics: {_nonempty(state.get('metric_contract', anchor.get('metrics')))}",
        "## 3. Portfolio and Blocked Axes",
        "\n".join(portfolio_lines),
        "## 4. Latest Completed Scientific Result",
        "\n".join(latest_lines),
        "## 5. Current Mode",
        f"- Mode: {_nonempty(state.get('current_mode'))}\n{experiment_line}",
        "## 6. Thesis Harvest",
        "\n".join(harvest_lines),
        "## 7. Next Automatic Action (Recorded Next Action)",
        next_action_text,
        "## 8. Strategy Escalation Condition",
        _nonempty(state.get("strategy_required_when")),
        "## Detail Pointers",
        "\n".join(_detail_pointers(adapter)) or "- None recorded.",
    ]
    return "\n\n".join(sections) + "\n"


def _load_mapping(spec: str) -> Mapping:
    path_text, separator, selector = spec.partition("#")
    path = Path(path_text)
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError(f"input is not a mapping: {path}")
    if separator:
        if not selector:
            raise ValueError(f"empty mapping selector: {spec}")
        for key in selector.split("."):
            value = value.get(key)
            if not isinstance(value, Mapping):
                raise ValueError(f"selector does not resolve to a mapping: {spec}")
    return value


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a bounded read-only project status to stdout.")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--portfolio", required=True)
    parser.add_argument("--harvest", required=True)
    args = parser.parse_args(argv)
    try:
        output = render_status(
            _load_mapping(args.adapter),
            _load_mapping(args.state),
            _load_mapping(args.portfolio),
            _load_mapping(args.harvest),
        )
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"render_status: {exc}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(output.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
