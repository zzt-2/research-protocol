from collections.abc import Mapping, Sequence
from pathlib import Path

from hash_bundle import hash_bundle


EXECUTION_RECEIPT_SCHEMA = "rdl.execution-receipt.v1"
EXECUTION_RECEIPT_FIELDS = {
    "schema_version",
    "contract_hashes",
    "source_hashes",
    "test_started",
    "seed_ledger",
    "pre_test_state",
    "post_test_state",
}


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


def _copy_seed_ledger(seed_ledger: Mapping[str, Sequence[int]]) -> dict[str, list[int]]:
    if not isinstance(seed_ledger, Mapping):
        raise ValueError("seed ledger must be a mapping")
    if not seed_ledger:
        raise ValueError("seed ledger must not be empty")
    copied: dict[str, list[int]] = {}
    seen: set[int] = set()
    for group, seeds in seed_ledger.items():
        if not isinstance(group, str) or not group:
            raise ValueError("seed group must be a non-empty string")
        if isinstance(seeds, (str, bytes)) or not isinstance(seeds, Sequence):
            raise ValueError("seed group must be a sequence")
        copied[group] = []
        for seed in seeds:
            if isinstance(seed, bool) or not isinstance(seed, int):
                raise ValueError("seed must be an integer")
            if seed in seen:
                raise ValueError(f"duplicate seed: {seed}")
            seen.add(seed)
            copied[group].append(seed)
    if not seen:
        raise ValueError("seed ledger must contain a seed")
    return copied


def _require_nonempty_paths(name: str, paths: Sequence[Path]) -> None:
    if not paths:
        raise ValueError(f"{name} paths must not be empty")


def _copy_state(name: str, state: Mapping[str, object] | None) -> dict[str, object] | None:
    if state is None:
        return None
    if not isinstance(state, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return dict(state)


def build_execution_receipt(
    root: Path,
    contract_paths: Sequence[Path],
    source_paths: Sequence[Path],
    *,
    test_started: bool,
    seed_ledger: Mapping[str, Sequence[int]],
    pre_test_state: Mapping[str, object],
    post_test_state: Mapping[str, object] | None,
) -> dict[str, object]:
    if not isinstance(test_started, bool):
        raise ValueError("test_started must be boolean")
    _require_nonempty_paths("contract", contract_paths)
    _require_nonempty_paths("source", source_paths)
    pre_state = _copy_state("pre-test state", pre_test_state)
    if pre_state is None:
        raise ValueError("pre-test state is required")
    post_state = _copy_state("post-test state", post_test_state)
    if not test_started and post_state is not None:
        raise ValueError("post-test state requires test_started")
    if test_started and post_state is None:
        raise ValueError("test_started requires post-test state")

    return {
        "schema_version": EXECUTION_RECEIPT_SCHEMA,
        "contract_hashes": hash_bundle(Path(root), contract_paths),
        "source_hashes": hash_bundle(Path(root), source_paths),
        "test_started": test_started,
        "seed_ledger": _copy_seed_ledger(seed_ledger),
        "pre_test_state": pre_state,
        "post_test_state": post_state,
    }


def _hash_map_errors(
    name: str,
    observed: object,
    expected: Mapping[str, str],
) -> list[str]:
    if not isinstance(observed, Mapping):
        return [f"invalid:{name}"]
    errors: list[str] = []
    observed_keys = set(observed)
    expected_keys = set(expected)
    for path in sorted(expected_keys - observed_keys):
        errors.append(f"missing:{name}:{path}")
    for path in sorted(observed_keys - expected_keys):
        errors.append(f"unexpected:{name}:{path}")
    for path in sorted(expected_keys & observed_keys):
        if observed[path] != expected[path]:
            errors.append(f"mismatch:{name}:{path}")
    return errors


def validate_execution_receipt(
    receipt: Mapping[str, object],
    root: Path,
    contract_paths: Sequence[Path],
    source_paths: Sequence[Path],
) -> list[str]:
    errors: list[str] = []
    for field in sorted(EXECUTION_RECEIPT_FIELDS - set(receipt)):
        errors.append(f"missing:{field}")
    for field in sorted(set(receipt) - EXECUTION_RECEIPT_FIELDS):
        errors.append(f"unexpected:{field}")
    if errors:
        return errors

    if receipt["schema_version"] != EXECUTION_RECEIPT_SCHEMA:
        errors.append("mismatch:schema_version")
    if not contract_paths:
        errors.append("invalid:contract_paths:must_not_be_empty")
    else:
        expected_contracts = hash_bundle(Path(root), contract_paths)
        errors.extend(
            _hash_map_errors(
                "contract_hashes", receipt["contract_hashes"], expected_contracts
            )
        )
    if not source_paths:
        errors.append("invalid:source_paths:must_not_be_empty")
    else:
        expected_sources = hash_bundle(Path(root), source_paths)
        errors.extend(
            _hash_map_errors("source_hashes", receipt["source_hashes"], expected_sources)
        )

    started = receipt["test_started"]
    if not isinstance(started, bool):
        errors.append("invalid:test_started")
    try:
        _copy_seed_ledger(receipt["seed_ledger"])
    except ValueError as exc:
        errors.append(f"invalid:seed_ledger:{exc}")
    if not isinstance(receipt["pre_test_state"], Mapping):
        errors.append("invalid:pre_test_state")
    post_state = receipt["post_test_state"]
    if started is False and post_state is not None:
        errors.append("invalid:post_test_state_before_start")
    if started is True and not isinstance(post_state, Mapping):
        errors.append("invalid:post_test_state_after_start")
    return errors
