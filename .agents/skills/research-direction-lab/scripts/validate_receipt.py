from collections.abc import Mapping


def validate_receipt(
    receipt: Mapping[str, object], expected: Mapping[str, str]
) -> list[str]:
    errors: list[str] = []
    for key in sorted(expected):
        if key not in receipt:
            errors.append(f"missing:{key}")
        elif receipt[key] != expected[key]:
            errors.append(f"mismatch:{key}")
    return errors
