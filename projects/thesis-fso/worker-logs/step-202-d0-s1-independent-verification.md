# Step 202 — D0 S1 natural-occurrence independent verification

VERDICT=PASS

P0=0
P1=0
P2=0

## Scope and method

- Read-only verification of T129 final files only. No production repair and no S2–S4/C1 work.
- Did not rerun the 480-row physical simulation. Fresh work consisted of parsing/reducing the final raw rows, hashing final files, source/contract review, and one focused test run.
- Verification HEAD: `4e126c7fed28b0f3226f8b674c568dbc760a89fc`.

## Fresh commands and results

1. A fresh Python process loaded `s1-raw.jsonl`, the frozen owner through `contract.load_contract`, and each row through `schemas.row_from_mapping("s1_trajectory", ...)`; `statistics.reduce_s1` returned:
   - `trajectory_count=480`
   - `event_count=262`
   - `event_rate=0.5458333333333333`
   - independent event clusters: `17` seeds and `12` physical cells
2. Focused test command:

   ```powershell
   $env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest 'projects/simulation/tests/test_d0_science_s1.py' -q
   ```

   Fresh result: `6 passed in 3.68s`, exit code 0.
3. `git status --short -- <owner> <common/> <science.py> <focused-test>` showed only the two expected untracked T129 files, `science.py` and `test_d0_science_s1.py`; owner YAML and `common/` were clean. `git diff --cached --name-only` was empty.

## Independent coverage and numbers

- Raw line count = 480; unique `(seed, cell_id, target_polarization)` count = 480.
- Exact coverage equals `8100..8119 × 12 owner population cells × {X,Y}`. There are 20 seeds, 12 cells, and both polarizations with no missing or duplicate key.
- Event count by physical cell is `[34,34,34,24,24,25,16,17,18,12,12,12]` in owner cell order, so all 12 cells contain events.
- Event-bearing seed count is 17; event-bearing physical-cell count is 12.
- Frozen gate checks are all true: `262 >= 12`, `17 >= 4`, `12 >= 2`.
- Summary and receipt numeric fields exactly match the independent reduction.

## Artifact, hash, checkpoint, and HEAD checks

| Item | Fresh SHA-256 | Check |
|---|---|---|
| owner contract | `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b` | equals receipt |
| current `science.py` | `51ac70046ee901ca672937fe2dce9b1d479c2c24c406042cc819c5a25613093f` | equals receipt |
| `s1-raw.jsonl` | `e9a5f2ad3e8ebea9d238ecfdac54b88160d4fbe4273314c9a1dcfd39fa5e75ad` | equals receipt |
| `checkpoint.jsonl` | `e9a5f2ad3e8ebea9d238ecfdac54b88160d4fbe4273314c9a1dcfd39fa5e75ad` | byte-identical to raw |
| `summary.json` | `51acd5afeb37507f0ffe6f60f24ec1f6df0e9d11eb79e60a7d15d4b5dda592b4` | equals receipt |
| `receipt.json` | `318b80f75fa7707d2a34f8bb5a3be5977bd9ec7cef55bb100bdce02ab558be56` | equals author log |

- Receipt `git_head` equals fresh `git rev-parse HEAD` (`4e126c7f...89fc`). The S1 source/artifacts remain untracked, consistent with the recorded HEAD being the frozen pre-S1 base rather than a claim that S1 is committed.
- Checkpoint and raw contain every dual-pol frame exactly once in final state. The plan has 240 unique `(seed,cell)` frames and each has X/Y, yielding 480 unique rows.

## Persistent-transition and truth-boundary review

- State computation implements the owner definition: nearest of four residual phase states modulo `pi/2` using wrapped angular distance.
- A candidate boundary requires a 32-symbol window on each side, at least 28/32 samples in the respective same state, and different left/right states. Candidate transitions at distance `<=32` are merged.
- The focused test covers no event, one event, a transition exactly 32 symbols later being merged, shape fail-closed behavior, exact first-stage plan, and checkpoint deduplication/conflict rejection.
- `true_phase` is passed only to `detect_persistent_transitions` in the evaluator row-generation path. `receiver.estimate_prefix_calibration`, `receiver.scalar_visible_power_equalize`, and `receiver.run_common_bps` receive only received/known-prefix or receiver-derived data. The raw row exposes only the event result and a receipt hash, not truth arrays. No deployable/channel receiver interface was expanded by T129.

## RED/GREEN evidence

- Author log records initial missing-runner RED `4 failed` followed by `4 passed`.
- It records repo-root CLI import RED followed by the full file at `5 passed`.
- It records transient Windows `os.replace` RED followed by the full file at `6 passed`.
- The final current bytes independently reproduce `6 passed in 3.68s`.

## Runtime accounting

- Receipt does not misreport finalization as complete execution cost:
  - `wall_time_seconds=null`
  - `wall_time_status=NOT_CAPTURED_ACROSS_PRE_REPAIR_RESUMES`
  - `resume_count=null`
  - `resume_count_status=NOT_PERSISTED_ACROSS_PRE_REPAIR_ATTEMPTS`
  - `resumed_completed_frame_count=240`
  - `final_invocation_wall_time_seconds=0.2974536000401713`
- The author log uses the same distinctions and states that the filesystem-observed 12.7518845 s checkpoint span is not a complete wall-time claim. Therefore the missing across-attempt total is disclosed rather than replaced with a false precise total.

## Scope and protection checks

- Owner YAML and `common/` were not modified by T129. `science.py` contains only S1 execution; no S2–S4 or C1 implementation is present.
- No staged files were found. The branch has no upstream marker, and the S1 files are untracked; no commit/push claim is made.
- Protected P05 SHA-256 values remain 4/4 equal to their anchors.

## Disposition

- `formal_science_disposition=S1_NATURAL_OCCURRENCE_ESTABLISHED`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`

S1 proves only natural occurrence under the frozen event definition. It is not a method signal or thesis contribution. The next legal scientific action is the frozen S2 B1-damage/O1-headroom gate.

## Findings

None.
