from collections.abc import Iterable, Mapping


def rebuild_state(events: Iterable[Mapping[str, object]]) -> dict[str, object]:
    completed: set[str] = set()
    stale: set[str] = set()
    seen_event_ids: set[str] = set()
    last_event_head: object = None
    recorded_next_action: str | None = None
    dispositions: dict[str, dict[str, dict[str, str]]] = {}

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
                stale.discard(subject_id)
            else:
                stale.add(subject_id)
                completed.discard(subject_id)

        if event_type == "DISPOSITION":
            required = {}
            for field in ("entity_kind", "entity_id", "status", "reason"):
                value = event.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{field} must be a non-empty string")
                required[field] = value.strip()
            current = {
                "status": required["status"],
                "reason": required["reason"],
                "event_id": event_id,
            }
            replaces = event.get("replaces_event_id")
            if replaces is not None:
                if not isinstance(replaces, str) or not replaces.strip():
                    raise ValueError("replaces_event_id must be a non-empty string")
                replaces = replaces.strip()

            entities = dispositions.setdefault(required["entity_kind"], {})
            previous = entities.get(required["entity_id"])
            if previous is None and replaces is not None:
                raise ValueError(
                    f"{required['entity_kind']}/{required['entity_id']} "
                    "does not have a current disposition to replace"
                )
            if previous is not None:
                previous_event_id = previous["event_id"]
                if replaces is None:
                    raise ValueError(
                        "subsequent disposition must declare "
                        f"replaces_event_id={previous_event_id}"
                    )
                if replaces != previous_event_id:
                    raise ValueError(
                        "replaces_event_id must replace current disposition "
                        f"{previous_event_id}"
                    )
            if replaces is not None:
                current["replaces_event_id"] = replaces
            entities[required["entity_id"]] = current

        next_action = event.get("next_action")
        if isinstance(next_action, str) and next_action.strip():
            recorded_next_action = next_action
        last_event_head = event.get("event_hash")

    return {
        "completed_ids": sorted(completed),
        "stale_ids": sorted(stale),
        "entity_dispositions": {
            kind: {entity_id: entities[entity_id] for entity_id in sorted(entities)}
            for kind, entities in sorted(dispositions.items())
        },
        "last_event_head": last_event_head,
        "recorded_next_action": recorded_next_action,
    }
