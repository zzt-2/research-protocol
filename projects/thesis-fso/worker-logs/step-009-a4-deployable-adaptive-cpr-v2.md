# Step 009 — A4 deployable adaptive CPR v2

## Status

- `formal_science_disposition`: `BLOCKED_IDENTITY`
- `mission_method_delta`: `NONE`
- `primary_run`: false
- `bounded_repairs_used`: 1

## Fresh evidence

- Task control: PASS; HEAD baseline `220e477`; formal owner D015/A4.
- TDD: RED 5/5 failed because `a4_v2.py` was absent; GREEN 5/5 passed after implementation.
- S011 smoke: continuous BER `0.0036458333`; reset BER `0.0065364583`; ratio `1.792857`.
- Mechanism gate: DA won 9/9 validation conditions. NDA never won under the causal
  pilot ambiguity rule and common data mask. Therefore T009 §4.6 failed.
- FEC discipline: no proxy dB was produced; unresolved crossings remain
  `UNRESOLVED_NO_CROSSING`.

## Boundary and artifacts

- Raw validation rows: `projects/simulation/results/a4-deployable-adaptive-cpr-v2/raw.json`
- Adjudication: `projects/simulation/results/a4-deployable-adaptive-cpr-v2/result.json`
- Source closure/contract/method card/synthesis are in the isolated v2 directory.
- Old A4, common, params, paper, owner, mission, and master files were not modified.

## Recommendation to master

- same-axis streak: increment once for A4.
- repair streak: one bounded repair consumed; do not open a second A4 repair package.
- no-method streak: increment.
- drift: aligned; the contract stopped at identity rather than manufacturing a method verdict.

