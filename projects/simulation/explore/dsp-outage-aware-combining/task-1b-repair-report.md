# Task 1B repair report

## Scope and files

- `smoke_core.py`: recursive caller-to-callee information-boundary audit, guarded sync margin helper, estimator integration, and corrected module description.
- `test_smoke.py`: integrated regression tests without changing concurrent Task 2 tests.
- `test_task1b_repair.py`: targeted TDD tests independent of Task 2 collection timing.
- `design.md`: froze one phase-processing order: branch-local receiver-visible pilot correction before MRC, with no second post-combine correction.

## Root cause and repair

The previous AST check scanned a fixed flat tuple. A harmlessly named helper could therefore hide a reachable evaluator/truth reference. The replacement starts from `estimate_branches`, `run_b0`, `run_b1`, and `run_b2`, discovers sandbox-local function calls recursively, tracks visited functions, and reports forbidden symbols with the full call path. Evaluator functions that are not reachable from a root are not scanned.

The previous sync margin used the second-largest score even when it was an adjacent sample from the same peak. The frozen definition is now `score[winner] - max(score outside [winner-1,winner+1])`; if the guard covers the entire vector, the comparison peak is zero.

## RED evidence

Because concurrent Task 2 temporarily made `test_smoke.py` import a not-yet-created `run_smoke.py`, a targeted file was used rather than touching Task 2. Its first run failed at collection with:

```text
ImportError: cannot import name 'guarded_sync_peak_margin' from 'smoke_core'
```

After the initial implementation, the indirect-audit test failed `assert any("TruthRecord"...)`. Investigation showed the fixture returned a helper object instead of calling it, so no caller edge existed. The fixture was corrected to make a real root→helper call; production audit behavior was unchanged for that correction.

## GREEN evidence

After Task 2 appeared, the merged command was run:

```text
python -m pytest test_smoke.py test_task1b_repair.py -q
python -m py_compile smoke_core.py run_smoke.py test_smoke.py test_task1b_repair.py
```

Result: `33 passed in 0.22s`; both commands exited 0. The default recursive audit independently returned `()`.

## Residual boundaries

- Recursion deliberately follows direct sandbox-local `ast.Call(Name(...))` edges. Dynamic dispatch, aliases, closures returned without invocation, and attribute-based calls are outside this bounded audit; runtime truth-metamorphic tests remain the second line of defense.
- Guard width one is now part of the frozen scientific contract and must not be tuned on held-out data.
- No Task 2 runner behavior, scientific sample, candidate method, or governance file was changed by this repair.
