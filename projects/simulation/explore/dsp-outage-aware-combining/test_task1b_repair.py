"""Targeted RED/GREEN checks independent of concurrently implemented Task 2."""

import numpy as np

from smoke_core import (
    TruthRecord,
    audit_deployable_information_boundary,
    evaluate_subsets,
    guarded_sync_peak_margin,
    run_b0,
)


def _unsafe_evaluator_leaf():
    truth_type = TruthRecord
    return evaluate_subsets, truth_type


def _innocent_named_deployable_root():
    return _unsafe_evaluator_leaf()


def test_recursive_audit_follows_indirect_sandbox_call() -> None:
    violations = audit_deployable_information_boundary((_innocent_named_deployable_root,))

    assert any("TruthRecord" in item for item in violations)
    assert any("evaluate_subsets" in item for item in violations)
    assert any("_unsafe_evaluator_leaf" in item for item in violations)


def test_recursive_audit_ignores_unreachable_evaluator() -> None:
    assert audit_deployable_information_boundary((run_b0,)) == ()


def test_sync_margin_excludes_adjacent_peak_with_guard_one() -> None:
    scores = np.asarray([0.20, 0.91, 0.99, 0.94, 0.30, 0.60])

    peak, margin = guarded_sync_peak_margin(scores, winner=2)

    assert peak == 0.99
    assert margin == 0.39
