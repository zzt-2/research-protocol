"""Behavior scorer for the pragmatic baseline-adjudication forward case."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _has(text: str, *patterns: str) -> bool:
    return all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)


def score_response(path: Path) -> dict:
    transcript = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Raw response\s*$\n(?P<response>.*?)(?=^## Pre-registered scorer output\s*$)",
        transcript,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"missing closed Raw response section: {path}")
    text = match.group("response")
    checks = {
        "bounded_claim": _has(text, r"DIAGNOSTIC", r"SLICE"),
        "ml_gate": _has(text, r"PROBLEM_SURVIVES_CONVENTIONAL_BASELINE"),
        "oracle_not_go": bool(
            re.search(r"oracle", text, re.IGNORECASE)
            and re.search(r"(?:not|never|不能|只作|scoring|bound|Kill)", text, re.IGNORECASE)
        ),
        "pragmatic_stop": bool(
            re.search(r"SOTA", text, re.IGNORECASE)
            and re.search(r"(?:not|no |不追|无需|非必要|default)", text, re.IGNORECASE)
            and re.search(r"(?:one|一个).{0,80}(?:comparator|baseline|传统)", text, re.IGNORECASE | re.DOTALL)
        ),
        "fair_conventional_baseline": bool(
            re.search(r"(?:convergence|收敛)", text, re.IGNORECASE)
            and re.search(r"(?:task.appropriate|任务适配|conventional|传统)", text, re.IGNORECASE)
        ),
        "portfolio_continues": bool(
            re.search(r"(?:parallel|并行)", text, re.IGNORECASE)
            and re.search(r"(?:candidate|候选|portfolio)", text, re.IGNORECASE)
        ),
    }
    return {
        "case_id": "pragmatic-baseline-adjudication",
        "response": str(path),
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("responses", nargs="+", type=Path)
    args = parser.parse_args()
    results = [score_response(path) for path in args.responses]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(result["verdict"] == "PASS" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
