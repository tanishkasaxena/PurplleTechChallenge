from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS_BY_EVENT_TYPE: dict[str, set[str]] = {
    "entry": {
        "event_type",
        "id_token",
        "store_code",
        "camera_id",
        "event_timestamp",
        "is_staff",
    },
    "exit": {
        "event_type",
        "id_token",
        "store_code",
        "camera_id",
        "event_timestamp",
        "is_staff",
    },
    "zone_entered": {
        "event_type",
        "track_id",
        "store_id",
        "camera_id",
        "zone_id",
        "zone_name",
        "zone_type",
        "event_time",
    },
    "zone_exited": {
        "event_type",
        "track_id",
        "store_id",
        "camera_id",
        "zone_id",
        "zone_name",
        "zone_type",
        "event_time",
    },
    "queue_completed": {
        "queue_event_id",
        "event_type",
        "track_id",
        "store_id",
        "camera_id",
        "zone_id",
        "zone_name",
        "zone_type",
        "queue_join_ts",
        "queue_exit_ts",
        "wait_seconds",
        "queue_position_at_join",
        "abandoned",
    },
    "queue_abandoned": {
        "queue_event_id",
        "event_type",
        "track_id",
        "store_id",
        "camera_id",
        "zone_id",
        "zone_name",
        "zone_type",
        "queue_join_ts",
        "queue_exit_ts",
        "wait_seconds",
        "queue_position_at_join",
        "abandoned",
    },
}


def validate_event(event: dict[str, Any], line_number: int) -> list[str]:
    errors: list[str] = []
    event_type = event.get("event_type")

    if not isinstance(event_type, str):
        return [f"line {line_number}: missing or invalid event_type"]

    required_fields = REQUIRED_FIELDS_BY_EVENT_TYPE.get(event_type)
    if required_fields is None:
        return [f"line {line_number}: unsupported event_type {event_type!r}"]

    missing = sorted(field for field in required_fields if field not in event)
    if missing:
        errors.append(f"line {line_number}: missing required fields: {', '.join(missing)}")

    if "is_staff" in event and not isinstance(event["is_staff"], bool):
        errors.append(f"line {line_number}: is_staff must be boolean")

    if "abandoned" in event and not isinstance(event["abandoned"], bool):
        errors.append(f"line {line_number}: abandoned must be boolean")

    if "wait_seconds" in event and not isinstance(event["wait_seconds"], (int, float)):
        errors.append(f"line {line_number}: wait_seconds must be numeric")

    return errors


def validate_jsonl(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"{path} does not exist"]

    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                errors.append(f"line {line_number}: blank lines are not valid JSONL events")
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue

            if not isinstance(event, dict):
                errors.append(f"line {line_number}: JSONL row must be an object")
                continue

            errors.extend(validate_event(event, line_number))

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_event_log.py submission/event_log.jsonl")
        return 2

    path = Path(sys.argv[1])
    errors = validate_jsonl(path)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"OK: {path} is valid JSONL for the provided sample schema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
