# Step 015 — Q1 deterministic semantic smoke

> Status: DONE | no commit / no push | protected common/params/legacy paths untouched by this executor

## 事实与发现

- task-control validator: `PASS`; execution class `FORMAL_STEP4A_SEMANTIC_SMOKE_EXECUTION`, checkpoint `CP017`.
- Semantic gates: `{'identity': True, 'paired_realization': True, 'truth_isolation': True, 'score_comparability': True}`.
- Residual population: 75 cells/layer; stress population: 30 cells, separately reported.
- B1/C exact common-grid equivalence: `True`.
- B0 stable adjacent 2x2 wrong-basin region: `False`.
- Traversal audit: B0/B2 repeated visits persisted in `360` rows; residual B1/C full 735-candidate paths in `300` rows.
- Plot selector: `residual|minus6db|d=+8|tau=+0.0|cfo_hz=-100000000.0`, B0 final-decision top1-top2 margin `0.0051385603251201395`; truth and top1/wrong-basin markers are rendered.
- Residual exact separability by layer: `{'noiseless': False, 'minus6db': False}`.
- Residual maximum additive-interaction residual by layer: `{'noiseless': {'max_additive_interaction_residual': 0.4155313607311553, 'exact_separable': False, 'cell_count': 75}, 'minus6db': {'max_additive_interaction_residual': 0.6357717679002818, 'exact_separable': False, 'cell_count': 75}}`.
- Stress interaction diagnostic (excluded from reducer): `{'max_additive_interaction_residual': 0.04797495564091718, 'exact_separable': False, 'cell_count': 30, 'reducer_role': 'diagnostic_only_excluded'}`.

| Layer | Method | False locks | R_FL | Acquisition success |
|---|---:|---:|---:|---:|
| noiseless | B0 | 0/75 | 0.000000 | 1.000000 |
| noiseless | B1 | 0/75 | 0.000000 | 1.000000 |
| noiseless | B2 | 0/75 | 0.000000 | 1.000000 |
| noiseless | C | 0/75 | 0.000000 | 1.000000 |
| minus6db | B0 | 58/75 | 0.773333 | 0.226667 |
| minus6db | B1 | 59/75 | 0.786667 | 0.213333 |
| minus6db | B2 | 58/75 | 0.773333 | 0.226667 |
| minus6db | C | 59/75 | 0.786667 | 0.213333 |
| stress_noiseless | B0 | 0/30 | 0.000000 | 1.000000 |
| stress_noiseless | B1 | 0/30 | 0.000000 | 1.000000 |
| stress_noiseless | B2 | 0/30 | 0.000000 | 1.000000 |
| stress_noiseless | C | 0/30 | 0.000000 | 1.000000 |

## 改善与覆盖

- `noiseless`: G_C=0.0; coverage(B1)=None; coverage(B2)=None.
- `minus6db`: G_C=-0.017241379310344827; coverage(B1)=None; coverage(B2)=None.

`miss=N/A` for every method and layer. Stress cells are not pooled into these values.

## Compute ledger

- `residual_noiseless/B0`: visits=315, unique_score_calls=231, complex_MAC=43428, interpolation=231, FFT=0 [], median=0.026476s.
- `residual_noiseless/B1`: visits=735, unique_score_calls=735, complex_MAC=138180, interpolation=735, FFT=0 [], median=0.073506s.
- `residual_noiseless/B2`: visits=467, unique_score_calls=231, complex_MAC=43428, interpolation=231, FFT=0 [], median=0.021493s.
- `residual_noiseless/C`: visits=735, unique_score_calls=735, complex_MAC=138180, interpolation=735, FFT=0 [], median=0.084371s.
- `residual_minus6db/B0`: visits=315, unique_score_calls=231, complex_MAC=43428, interpolation=231, FFT=0 [], median=0.019883s.
- `residual_minus6db/B1`: visits=735, unique_score_calls=735, complex_MAC=138180, interpolation=735, FFT=0 [], median=0.071371s.
- `residual_minus6db/B2`: visits=467, unique_score_calls=231, complex_MAC=43428, interpolation=231, FFT=0 [], median=0.024300s.
- `residual_minus6db/C`: visits=735, unique_score_calls=735, complex_MAC=138180, interpolation=735, FFT=0 [], median=0.079694s.
- `stress_noiseless/B0`: visits=252, unique_score_calls=189, complex_MAC=35532, interpolation=189, FFT=0 [], median=0.019406s.
- `stress_noiseless/B1`: visits=525, unique_score_calls=525, complex_MAC=98700, interpolation=525, FFT=0 [], median=0.059066s.
- `stress_noiseless/B2`: visits=362, unique_score_calls=189, complex_MAC=35532, interpolation=189, FFT=0 [], median=0.018229s.
- `stress_noiseless/C`: visits=525, unique_score_calls=525, complex_MAC=98700, interpolation=525, FFT=0 [], median=0.060724s.

## Artifact SHA256

- `ambiguity_surface.png`: `4d9c9c08f9232c4dde1397ff4592109b78f2eb3dd55c84718facea830b615ce3`
- `ambiguity_surfaces.npz`: `483fa92dd7c55cc2cf5c62ad49ef15c79bf3744ea34944ebf4f65bc36a8d88ca`
- `focused-pytest-green.txt`: `cb9de6713d94e14366a8d8977ef484aa14034a8fdfb7b69aae05358225c8e09f`
- `manifest.json`: `aaa60458d56aabc7696cc69ec348913859117ee51f02f10b8298072fcc463695`
- `method_results.jsonl`: `69c43139f65a55ccab990ecd0b56b05aea1e2b7f59cb699b8639e842dc52db5b`
- `observations.jsonl`: `ba8a1ef6557f2fa69eed92c585a64e76f6f4511b883a830d057f3ec8d632d961`
- `provenance.json`: `1a9f907e6129199634d7196400ddcaa59d7931abf87591f95a9830587710660f`
- `summary.json`: `e0204cddebb2a3ff47fa647612191704f378a457184ebb7d04c08b4030d97eaa`
- `surface_index.json`: `0d5b138b1594dd853dc135fe3138fb31f341444eaff1849fda5c94e462bd7797`
- `tdd-evidence.jsonl`: `ef6f9c1052a51319353bfc16a4a69e68278ee9d7b083f26c470587f955479831`
- `terminal.json`: `dc36ca65759218b315aa6dfc46329af121ca1040b4807d9f24bc2be45d3bdfcc`
- `truth.jsonl`: `b1bd861df59bf326d0405549d05ad39888b80c94be9e26e33d81c322f5f2eecb`

## Warnings / claim ceiling

- The fixed-seed QPSK preamble and RRC span 10 are diagnostic sentinels because the exact literature sequence is unavailable.
- The -6 dB AWGN layer is a numerical-stress anchor, not an occurrence distribution.
- False-lock rates are exhaustive frequencies on the frozen grid, not field probabilities and not paper-ready numbers.
- B1/C equivalence is structural under the same finite candidate set, score, normalization, window and tie-break; it does not establish continuous-estimator equivalence.
- Historical RED/GREEN rows in `tdd-evidence.jsonl` are executor-report-only and are not independently verifiable; only `GREEN_FRESH` is bound to captured subprocess output by SHA256.


## TDD evidence

- Historical RED/GREEN claims are retained only as `executor_report_only`; they are not independent proof.
- T016 repair RED: focused pytest reported `4 failed, 24 passed` before the concentrated fix (`executor_report_only`).
- Fresh GREEN: subprocess output is saved as `artifacts/focused-pytest-green.txt`; its SHA256 is bound in `tdd-evidence.jsonl` and provenance.

## T016 concentrated repair evidence

- Traversal ledger now persists ordered `visited_candidate_indices` and its true length; unique cache-miss score calls and complex MAC remain separate.
- Plot selection is the residual B0 false-lock with maximum final-decision top1-top2 margin, with deterministic cell-id tie-break and identity fallback.
- Separability is reduced independently per residual layer; stress interaction is recorded only as `diagnostic_only_excluded` and cannot enter the residual terminal reducer.

## Exact execution commands

- `python .agents/skills/research-direction-lab/scripts/validate_task_control.py --repo-root . .sessions/2026-08-06-oversampled-coherent-sync-groundwork/T015-q1-semantic-smoke-execution.md`
- `python -m pytest projects/simulation/tests/test_oversampled_coherent_sync_q1.py -q`
- `python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --identity-only`
- `python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --run-grid --output-dir projects/simulation/explore/oversampled-coherent-sync-q1/artifacts`

## Actual changed-file allowlist

- `projects/simulation/explore/oversampled-coherent-sync-q1/README.md`
- `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py`
- `projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/manifest.json`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/observations.jsonl`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/truth.jsonl`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/method_results.jsonl`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/ambiguity_surfaces.npz`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/ambiguity_surface.png`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/surface_index.json`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/summary.json`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/terminal.json`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/provenance.json`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/tdd-evidence.jsonl`
- `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/focused-pytest-green.txt`
- `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`
- `projects/thesis-fso/worker-logs/step-015-q1-semantic-smoke.md`
- `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-report.md`

## Run terminal

`STEP4A_PREFLIGHT_KILL_OR_PIVOT` — B1_C_EXACT_COMMON_GRID_EQUIVALENCE, NO_STABLE_B0_ADJACENT_2X2_WRONG_BASIN, B0_ZERO_FALSE_LOCKS_noiseless, G_C_BELOW_5_PERCENT_noiseless, G_C_BELOW_5_PERCENT_minus6db.

## Provenance

- HEAD: `9af2280b083d636902514ec1065ca74b423bec36`
- Python: `3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]`
- NumPy/SciPy/Matplotlib: `2.4.3` / `1.17.1` / `3.10.8`
- Core SHA256: `de2dfd608f2d5cd41a289607868846d7d3cddbd1182c1220d6c995636e3b4489`
- Runner SHA256: `1a04f80f0c0b41cfbc23c885879ac95c453d06a45b466614a5ecce0ca4abbf35`
