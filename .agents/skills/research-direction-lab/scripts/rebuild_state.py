from collections.abc import Iterable, Mapping


def rebuild_state(events: Iterable[Mapping[str, object]]) -> dict[str, object]:
    completed: set[str] = set()
    stale: set[str] = set()
    seen_event_ids: set[str] = set()
    last_event_head: object = None
    recorded_next_action: str | None = None

    for event in events:
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("event_id must be a non-empty string")
        if event_id in seen_event_ids:
            raise ValueError("event_id has already been recorded")
        seen_event_ids.add(event_id)

        event_type = event.get("event_type")
        if event_type in {"COMPLETED", "STALE"}:
            subject_id = event.get("subject_id")
            if not isinstance(subject_id, str) or not subject_id.strip():
                raise ValueError("subject_id must be a non-empty string")
            if event_type == "COMPLETED":
                completed.add(subject_id)
            else:
                stale.add(subject_id)

        next_action = event.get("next_action")
        if isinstance(next_action, str) and next_action.strip():
            recorded_next_action = next_action
        last_event_head = event.get("event_hash")

    return {
        "completed_ids": sorted(completed),
        "stale_ids": sorted(stale),
        "last_event_head": last_event_head,
        "recorded_next_action": recorded_next_action,
    }
