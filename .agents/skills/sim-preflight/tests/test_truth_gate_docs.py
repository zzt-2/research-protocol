"""Structural contract test; independent agent pressure tests verify behavior."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((Path(__file__).parent / "truth-gate-cases.json").read_text(encoding="utf-8"))


def require(text: str, needle: str, where: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"{where}: missing {needle!r}")


def main() -> int:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    write = (ROOT / "scenarios" / "write.md").read_text(encoding="utf-8")
    tech = (ROOT / "rules" / "tech.md").read_text(encoding="utf-8")
    failures: list[str] = []

    for field in ("information_access", "metric_signature", "state_lifecycle"):
        require(skill, field, "SKILL.md", failures)
        require(write, field, "scenarios/write.md", failures)
        require(tech, field, "rules/tech.md", failures)

    require(write, "paper line -> caller -> callee -> metric/state", "scenarios/write.md", failures)

    joined = "\n".join((skill, write, tech))
    for case in CASES:
        require(joined, case["id"], "truth-gate policy", failures)
        if case["expected"] != "BLOCKED":
            failures.append(f"fixture {case['id']}: expected verdict must remain BLOCKED")

    if failures:
        print("TRUTH-GATE STRUCTURAL CONTRACT TEST: FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("TRUTH-GATE STRUCTURAL CONTRACT TEST: PASS (3 regression anchors)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
