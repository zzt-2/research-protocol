from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
QUEUE_PATH = ROOT / "batch-queue.v2.yaml"
MODULE_PATH = ROOT / "tools" / "validate_batch_queue.py"
spec = importlib.util.spec_from_file_location("validate_batch_queue", MODULE_PATH)
gate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gate)


def _queue():
    return gate.load_queue(QUEUE_PATH)


def _validate(data):
    return gate.validate_queue(data, queue_path=QUEUE_PATH)


def test_current_v2_queue_passes_static_gate_without_running_batch():
    report = _validate(_queue())

    assert report.errors == []


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    (
        ("universe_id", "wrong-universe", "universe ID mismatch"),
        ("map_id", "wrong-map", "map ID mismatch"),
        ("candidate_universe_v2_sha256", "0" * 64, "universe SHA mismatch"),
        ("candidate_map_v2_sha256", "0" * 64, "map SHA mismatch"),
    ),
)
def test_universe_and_map_binding_mutations_fail(field, value, expected):
    data = _queue()
    if field in data:
        data[field] = value
    else:
        data["lineage"][field] = value

    report = _validate(data)

    assert any(expected in error for error in report.errors)


def test_v1_queue_sha_lineage_drift_fails():
    data = _queue()
    data["lineage"]["v1_file_sha256"] = "0" * 64

    report = _validate(data)

    assert any("v1 queue SHA mismatch" in error for error in report.errors)


def test_b002_requires_three_distinct_mechanisms_and_true_unlabeled_candidate():
    duplicate = _queue()
    duplicate["batches"][0]["candidates"][1]["mechanism"] = duplicate["batches"][0]["candidates"][0]["mechanism"]
    replaced = _queue()
    replaced["batches"][0]["candidates"][2]["candidate_id"] = "C24-SSL-AE"

    assert any("distinct mechanisms" in error for error in _validate(duplicate).errors)
    assert any("C24-SSL-AE-UNLABELED" in error for error in _validate(replaced).errors)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("baseline", "standard-CMA"),
        ("seed_overlap", "train/test seed overlap"),
        ("metrics", "shared metrics"),
        ("budget", "shared resource budget"),
    ),
)
def test_shared_baseline_seeds_metrics_and_budget_are_enforced(mutation, expected):
    data = _queue()
    batch = data["batches"][0]
    if mutation == "baseline":
        batch["shared_contract"]["baseline_id"] = "baseline.current_cma.no_z"
    elif mutation == "seed_overlap":
        batch["shared_contract"]["test_seeds"].append(batch["shared_contract"]["train_seeds"][0])
    elif mutation == "metrics":
        batch["metrics"] = {}
    else:
        batch["shared_contract"].pop("resource_budget")

    report = _validate(data)

    assert any(expected in error for error in report.errors)


def test_candidate_level_contract_overrides_are_forbidden():
    data = _queue()
    data["batches"][0]["candidates"][0]["test_seeds"] = [999]

    report = _validate(data)

    assert any("candidate-level shared-contract override" in error for error in report.errors)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("hypothesis", "candidate hypothesis"),
        ("go_kill", "Go/Kill"),
        ("valid_domain", "valid_domain"),
    ),
)
def test_hypotheses_go_kill_and_valid_domain_are_preregistered(mutation, expected):
    data = _queue()
    batch = data["batches"][0]
    if mutation == "hypothesis":
        batch["candidates"][0]["hypothesis"] = ""
    elif mutation == "go_kill":
        batch["preregistered_outcomes"].pop("retire_specific_mechanism")
    else:
        batch["valid_domain"] = ""

    report = _validate(data)

    assert any(expected in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("runner_sha256", "runner SHA mismatch"),
        ("registry_sha256", "registry SHA mismatch"),
    ),
)
def test_runner_and_registry_fingerprint_mutations_fail(field, expected):
    data = _queue()
    data["queue_gate"][field] = "0" * 64

    report = _validate(data)

    assert any(expected in error for error in report.errors)


def test_registry_runner_component_fingerprint_matches_actual_runner():
    data = _queue()
    data["queue_gate"]["runner"] = "projects/thesis-fso/direction-lab/tools/missing.py:run_governed"

    report = _validate(data)

    assert any("runner file not found" in error for error in report.errors)


def test_pending_lifecycle_triad_is_consistent():
    data = _queue()
    data["status"] = "GATE_PENDING"
    data["queue_gate"]["independent_review"] = "PENDING"
    data["queue_gate"]["verdict"] = "PENDING"
    data["queue_gate"].pop("verifier_scope", None)
    data["queue_gate"].pop("verifier_evidence", None)

    report = _validate(data)

    assert report.errors == []


def test_pass_lifecycle_triad_requires_v010_evidence():
    data = _queue()
    data["status"] = "PASS"
    data["queue_gate"]["independent_review"] = "PASS"
    data["queue_gate"]["verdict"] = "PASS"
    data["queue_gate"]["verifier_scope"] = "independent Queue v2 static gate review"
    data["queue_gate"]["verifier_evidence"] = (
        ".sessions/2026-07-17-direction-lab-governance-pilot/verifications.md#V010"
    )

    report = _validate(data)

    assert report.errors == []


@pytest.mark.parametrize(
    ("status", "review", "verdict"),
    (
        ("PASS", "PENDING", "PENDING"),
        ("GATE_PENDING", "PASS", "PASS"),
        ("PASS", "PASS", "PENDING"),
        ("GATE_PENDING", "PENDING", "PASS"),
    ),
)
def test_inconsistent_lifecycle_combinations_fail(status, review, verdict):
    data = _queue()
    data["status"] = status
    data["queue_gate"]["independent_review"] = review
    data["queue_gate"]["verdict"] = verdict

    report = _validate(data)

    assert any("queue lifecycle state is inconsistent" in error for error in report.errors)


@pytest.mark.parametrize("field", ("verifier_scope", "verifier_evidence"))
def test_pass_lifecycle_rejects_missing_or_wrong_v010_metadata(field):
    data = _queue()
    data["status"] = "PASS"
    data["queue_gate"]["independent_review"] = "PASS"
    data["queue_gate"]["verdict"] = "PASS"
    data["queue_gate"]["verifier_scope"] = "independent Queue v2 static gate review"
    data["queue_gate"]["verifier_evidence"] = (
        ".sessions/2026-07-17-direction-lab-governance-pilot/verifications.md#V010"
    )
    data["queue_gate"][field] = ""

    report = _validate(data)

    assert any("PASS lifecycle requires verifier_scope and V010 evidence" in error for error in report.errors)


def test_current_queue_records_independent_v010_pass():
    data = _queue()

    assert data["status"] == "PASS"
    assert data["queue_gate"]["independent_review"] == "PASS"
    assert data["queue_gate"]["verdict"] == "PASS"
    assert data["queue_gate"]["verifier_evidence"].endswith("verifications.md#V010")


def test_no_family_wide_kill_must_be_true():
    data = _queue()
    data["batches"][0]["preregistered_outcomes"]["no_family_wide_kill"] = False

    report = _validate(data)

    assert any("no_family_wide_kill must be true" in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    (
        ("sandbox_only", False, "sandbox_only must be true"),
        ("promotion_allowed", True, "promotion_allowed must be false"),
        ("state", "RUNNING", "state must be QUEUED_NOT_RUN"),
    ),
)
def test_b002_sandbox_and_pre_run_state_are_enforced(field, value, expected):
    data = _queue()
    data["batches"][0][field] = value

    report = _validate(data)

    assert any(expected in error for error in report.errors)


@pytest.mark.parametrize(("field", "value"), (("family_id", "F04"), ("archetype_id", "U10")))
def test_b002_must_match_map_u24_f05_batch1_relationship(field, value):
    data = _queue()
    data["batches"][0][field] = value

    report = _validate(data)

    assert any("B002 must bind U24 in F05 with BATCH_1_FAMILY" in error for error in report.errors)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("missing_required", "run_v2.REQUIRED_CONTRACT"),
        ("bad_modulation", "shared contract is invalid"),
    ),
)
def test_shared_contract_matches_run_v2_required_contract_and_is_valid(mutation, expected):
    data = _queue()
    contract = data["batches"][0]["shared_contract"]
    if mutation == "missing_required":
        contract.pop("snr_db")
    else:
        contract["modulation"] = "16QAM"

    report = _validate(data)

    assert any(expected in error for error in report.errors)


@pytest.mark.parametrize(
    "rule",
    ("minimum_information", "advance_specific_mechanism", "retire_specific_mechanism", "otherwise"),
)
def test_each_preregistered_go_kill_rule_must_be_nonempty(rule):
    data = _queue()
    data["batches"][0]["preregistered_outcomes"][rule] = ""

    report = _validate(data)

    assert any("preregistered outcome must be non-empty" in error and rule in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    (
        ("required_signal_metrics", ["fixed_label_ber"], "required signal metrics"),
        ("primary", ["junk"], "primary metrics"),
    ),
)
def test_metrics_require_both_signal_and_both_primary_metrics(field, value, expected):
    data = _queue()
    data["batches"][0]["metrics"][field] = value

    report = _validate(data)

    assert any(expected in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("action", "WAIT"),
        ("state", "RUNNING"),
        ("evidence_status", "CANONICAL"),
        ("destination", "other"),
    ),
)
def test_controller_contract_is_exact(field, value):
    data = _queue()
    data["batches"][0]["controller"][field] = value

    report = _validate(data)

    assert any("controller contract mismatch" in error and field in error for error in report.errors)


def test_cli_passes_current_queue():
    result = subprocess.run(
        [sys.executable, str(MODULE_PATH), str(QUEUE_PATH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
