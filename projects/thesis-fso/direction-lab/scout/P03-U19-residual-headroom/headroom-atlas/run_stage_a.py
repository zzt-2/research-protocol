"""Drive the Stage A Headroom Atlas through the gate.

Usage:
    python run_stage_a.py \\
        --contract headroom-atlas/stage-a-contract.v1.yaml \\
        --assessment headroom-atlas/atlas-pre-run-assessment.v1.yaml \\
        --receipt headroom-atlas/atlas-pre-run-receipt.v1.yaml \\
        --audit artifacts/headroom-atlas-v1/atlas-audit.jsonl \\
        --batch-plan ../../batch-plan.v2.yaml \\
        --output-dir artifacts/headroom-atlas-v1

The assessment + receipt MUST be freshly issued (re-run
``tools/validate_claim_scope.py <assessment> --receipt <receipt>`` immediately
before invoking this driver). The gate re-checks the receipt hashes and
re-runs the validator on the exact assessment bytes; a stale or hand-written
receipt is rejected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve()
SCOUT_ROOT = HERE.parent.parent              # .../P03-U19-residual-headroom
DIRECTION_LAB_ROOT = SCOUT_ROOT.parents[1]   # .../direction-lab (parents[0]=scout)


def _load_module(path: Path, name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _aggregate_stage_a(cells: list[dict[str, Any]], contract: dict[str, Any]) -> dict[str, Any]:
    """Roll per-cell verdicts up into the Stage A exits."""
    runnable_cells = [c for c in cells if c.get("decision")]
    n_cells = len(runnable_cells)
    decisions = [c["decision"] for c in runnable_cells]
    headroom_cells = [d for d in decisions if d["visible_headroom"] > 0.0]
    above_mde_cells = [d for d in decisions if d["visible_headroom"] >= float(contract["statistical_sensitivity"]["minimum_detectable_effect"]["value"])]
    advance_cells = [d for d in decisions if d["decision_class"] == "ADVANCE"]
    insufficient_cells = [d for d in decisions if d["status"] == "INSUFFICIENT_SENSITIVITY"]
    local_negative_cells = [d for d in decisions if d["decision_class"] == "LOCAL_NEGATIVE"]
    # a cell is "sensitivity-limited" if it observed zero errors yet its rule-of-three
    # upper bound exceeds MDE (we literally cannot see an effect that small)
    mde = float(contract["statistical_sensitivity"]["minimum_detectable_effect"]["value"])
    sensitivity_limited_cells = [
        d for d in decisions
        if d["n_error_events"] == 0 and d["zero_error_upper_bound"] > mde
    ]

    blocked_axes = []
    for axis, spec in contract["representative_axes"].items():
        blocked = spec.get("blocked") or []
        if blocked:
            blocked_axes.append({"axis": axis, "blocked_values": [b.get("value") if isinstance(b, dict) else b for b in blocked]})

    # Stage A exit decision (ordered):
    # 1. HEADROOM_REGION_FOUND: at least one runnable cell has visible headroom >= MDE
    # 2. NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE: no runnable cell
    #    reaches MDE; the strongest legal non-ML baseline is at-or-below the
    #    preregistered detection threshold across the runnable representative
    #    domain. This is a representative-domain LOCAL_NEGATIVE; CANDIDATE-level
    #    retirement still requires a scope certificate that dispositions the
    #    INFRASTRUCTURE_BLOCKED axes.
    # 3. INSUFFICIENT_SENSITIVITY: every runnable cell observed zero errors AND
    #    the rule-of-three upper bound exceeds MDE (we cannot tell whether an
    #    effect exists).
    # 4. INFRASTRUCTURE_BLOCKED: no runnable cells and at least one axis blocked.
    if above_mde_cells:
        exit_state = "HEADROOM_REGION_FOUND"
    elif not sensitivity_limited_cells:
        # no cell is sensitivity-limited and no cell reaches MDE -> the
        # runnable representative domain has no mechanism-relevant headroom
        exit_state = "NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE"
    elif all(d in sensitivity_limited_cells for d in decisions):
        exit_state = "INSUFFICIENT_SENSITIVITY"
    elif not runnable_cells and blocked_axes:
        exit_state = "INFRASTRUCTURE_BLOCKED"
    else:
        # mixed: some cells sensitivity-limited, others measured-negative;
        # the measured-negative cells dominate the call but we flag the limit
        exit_state = "NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE"

    return {
        "stage": "A",
        "exit_state": exit_state,
        "n_runnable_cells": n_cells,
        "n_advance_cells": len(advance_cells),
        "n_local_negative_cells": len(local_negative_cells),
        "n_insufficient_sensitivity_cells": len(insufficient_cells),
        "n_headroom_cells": len(headroom_cells),
        "n_cells_above_mde": len(above_mde_cells),
        "n_sensitivity_limited_cells": len(sensitivity_limited_cells),
        "max_visible_headroom": max((d["visible_headroom"] for d in decisions), default=0.0),
        "blocked_axes": blocked_axes,
        "minimum_detectable_effect": mde,
        "summary_note": (
            "Stage A is baseline-only; cells with visible_headroom >= MDE flag a "
            "measurable same-information headroom that justifies a Stage B confirmation "
            "(still no ML training). When no runnable cell reaches MDE, the runnable "
            "representative domain has no mechanism-relevant headroom for the strongest "
            "legal non-ML baseline; CANDIDATE-level retirement still requires a scope "
            "certificate that dispositions the INFRASTRUCTURE_BLOCKED axes (16QAM, "
            "receiver-estimated CSI, coded metrics)."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--assessment", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--batch-plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--validator", type=Path, default=DIRECTION_LAB_ROOT / "tools/validate_claim_scope.py")
    args = parser.parse_args()

    gate = _load_module(HERE.parent / "atlas_gate.py", "atlas_stage_a_gate")
    cell_runner_module = _load_module(HERE.parent / "stage_a_cell_runner.py", "atlas_stage_a_cell_runner")

    contract = yaml.safe_load(Path(args.contract).read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # 1. authorize through the gate
    token = gate.authorize(
        assessment_path=args.assessment,
        receipt_path=args.receipt,
        audit_path=args.audit,
        batch_plan_path=args.batch_plan,
        validator_path=args.validator,
    )
    if not token.authorized:
        print(f"BLOCKED: {token.reason}", file=sys.stderr)
        return 2

    # 2. materialize the frozen closure (context keeps temp source tree alive)
    cell_results = []
    closure_sha_record = None
    with cell_runner_module.materialize_closure(contract) as closure:
        closure_sha_record = closure["closure_sha"]

        # 3. run every cell behind the gate
        runner = gate.AtlasRunner(
            cell_runner=lambda cell_id, **_: cell_runner_module.run_cell(
                next(c for c in contract["covering_design"]["cells"] if c["id"] == cell_id),
                contract,
                generator=closure["generator"],
                runner=closure["runner"],
                adapter=closure["adapter"],
                evaluator=closure["evaluator"],
                run_b001_path=closure["run_b001_path"],
            )
        )
        t0 = time.time()
        for cell in contract["covering_design"]["cells"]:
            result = runner.run_cell(cell_id=cell["id"], payload={}, token=token, audit_path=args.audit)
            cell_results.append(result)
            runner.write_summary(
                token=token,
                audit_path=args.audit,
                summary={"cell_id": cell["id"], "decision": result["decision"]},
            )
        elapsed = time.time() - t0

    # 4. aggregate Stage A exit
    aggregation = _aggregate_stage_a(cell_results, contract)

    atlas = {
        "schema_version": "direction-lab.headroom-atlas.stage-a.v1",
        "contract_id": contract["contract_id"],
        "gate": {
            "assessment_sha256": token.assessment_sha256,
            "validator_sha256": token.validator_sha256,
            "receipt_id": token.receipt_id,
            "authorized_at_nonce": token.nonce,
            "token_type": token.token_type,
        },
        "closure_sha": closure_sha_record,
        "cells": cell_results,
        "aggregation": aggregation,
        "elapsed_seconds": elapsed,
        "interpretation_limit": (
            "Stage A baseline-only Scout diagnostic. No ML trained, no B004, no "
            "Queue/Registry, no paper claim. ADVANCE cells justify a Stage B "
            "confirmation but do not authorize ML training."
        ),
    }
    atlas_path = args.output_dir / "stage-a-atlas.json"
    atlas_path.write_text(
        json.dumps(atlas, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "stage-a-atlas-summary.yaml").write_text(
        yaml.safe_dump(aggregation, sort_keys=False), encoding="utf-8"
    )
    print(yaml.safe_dump(aggregation, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
