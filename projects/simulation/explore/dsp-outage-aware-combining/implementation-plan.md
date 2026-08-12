# Q001 Defect-Only Smoke Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use test-driven-development. Do not commit; the controller owns the two frozen chronology commits.

**Goal:** Build and execute a receiver-only, paired, held-out defect smoke for Q001 without implementing any candidate method.

**Architecture:** An isolated sandbox separates receiver inputs from truth, implements corrected estimated-channel MRC plus fixed threshold and top-L comparators, and writes normalized raw rows. A deterministic raw-to-aggregate path computes G1–G4 and the unique terminal.

**Tech Stack:** Python 3, NumPy, SciPy, standard-library CSV/JSON/hashlib, pytest.

## Global Constraints

- Do not modify historical b3, `common/`, `params.py`, formal thesis text, coded C1 or unrelated dirty files.
- Primary events are natural stochastic outcomes; no injected invalid/slip flag may enter G1–G4.
- Deployable arms read only receiver samples and known training/pilots.
- All arms share one realization and are exact-invariant to truth-only metadata mutation.
- Dev freezes thresholds, diagnostic coefficients, grid, seeds, MDE and sample size before held-out.
- O1 is evaluator-only; no soft reliability/abstention method is implemented.

---

### Task 1: Receiver/truth firewall and corrected combining core

**Files:**
- Create: `projects/simulation/explore/dsp-outage-aware-combining/test_smoke.py`
- Create: `projects/simulation/explore/dsp-outage-aware-combining/smoke_core.py`

**Interfaces:**
- `Cell(turbulence: str, n_branches: int, heterogeneity: str, branch_snr_db: tuple[float,...])`
- `ReceiverFrame(branches, fsts, pilot_mask, pilot_symbols, payload_mask, ts)`
- `TruthRecord(payload_bits, payload_symbols, offsets, branch_gains, branch_snr_db, turbulence)`
- `generate_realization(seed: int, cell: Cell, payload_symbols: int=30720) -> tuple[ReceiverFrame, TruthRecord, str]`
- `estimate_branches(frame: ReceiverFrame) -> tuple[BranchEstimate,...]`
- `run_b0(estimates)`, `run_b1(estimates,tau_db)`, `run_b2(estimates,top_l) -> ArmOutput`
- `evaluate_subsets(estimates, truth) -> OracleOutput`

- [ ] Write tests first for deterministic replay, DTO truth exclusion, physical offset recovery, pilot residual reduction, noiseless unequal-gain MRC recovery, no-valid behavior, method-order invariance, and truth-metadata metamorphism.
- [ ] Run `python -m pytest projects/simulation/explore/dsp-outage-aware-combining/test_smoke.py -q` and record the expected import/attribute failures.
- [ ] Implement the minimal dataclasses, seeded natural channel, normalized FSTS, pilot-LS branch estimator, pilot-only phase correction and subset MRC required by those tests.
- [ ] Re-run the same pytest command; require zero failures and no RuntimeWarning/NaN.

### Task 2: Dev tuning, raw schema, aggregation and freeze receipt

**Files:**
- Modify: `projects/simulation/explore/dsp-outage-aware-combining/test_smoke.py`
- Create: `projects/simulation/explore/dsp-outage-aware-combining/run_smoke.py`
- Create at runtime: `projects/simulation/explore/dsp-outage-aware-combining/artifacts/dev/raw.csv`
- Create at runtime: `projects/simulation/explore/dsp-outage-aware-combining/artifacts/dev/aggregate.json`
- Create at runtime: `projects/simulation/explore/dsp-outage-aware-combining/freeze_receipt.json`

**Interfaces:**
- `run_split(split: str, seeds: list[int], output_dir: Path, frozen: dict|None) -> None`
- `tune_dev(raw_rows) -> dict` selects `tau_db`, `top_l_by_k`, strongest cheap arm and diagnostic logistic parameters.
- `aggregate_from_raw(path: Path, frozen: dict) -> dict` computes G1–G4 inputs and deterministic seed-cluster bootstrap CIs.
- `write_freeze_receipt(...)` writes hashes, frozen values and `test_started=false`.

- [ ] Add failing tests that reconstruct aggregates from synthetic raw rows, reject truth columns in arm inputs, verify seed-disjointness, and detect any freeze hash mismatch.
- [ ] Run the targeted pytest command and record the expected failures.
- [ ] Implement CSV/JSON writers, dev threshold/top-L selection, NumPy/SciPy logistic diagnostic, rank AUC, deterministic cluster bootstrap and freeze validation.
- [ ] Run all sandbox tests, then run the 18-cell dev split on seeds `0..19`.
- [ ] Freeze threshold grid, selected B1/B2 parameters, diagnostic coefficients, primary grid, payload size, dev/test seeds, G1–G4/MDE definitions and every contract/source hash.
- [ ] Recompute dev aggregate from raw only and require byte-stable JSON on a second run.

### Task 3: Held-out batches and raw merge

**Files:**
- Create at runtime: `artifacts/test/part-00..04/raw.csv` and metadata.
- Create at runtime: `artifacts/test/raw.csv`, `aggregate.json`, `terminal.json`.

- [ ] For each 20-seed batch from frozen `10000..10099`, validate the receipt has `test_started=false`, then run without tuning.
- [ ] Merge parts in deterministic seed/cell/frame/branch/method order and verify no duplicate/missing seed-cell pairs.
- [ ] Recompute all headline values only from merged raw; evaluate G1→G2→G3→G4 in fail-stop order.
- [ ] Write exactly one allowed scientific terminal and preserve novelty debt regardless of result.

### Task 4: Independent science and code verification

**Files:**
- Create: `projects/thesis-fso/worker-logs/step-4a-dsp-outage-defect-smoke.md`
- Create/update topic `R006`, `V005`, `H005`, topic/master/registry/voice.

- [ ] Fresh verifier checks the AST caller graph and runtime truth metamorphic gate.
- [ ] Fresh verifier independently recomputes G1–G4 and CIs from raw, checks physical/source limitations, method absence and unique terminal.
- [ ] Controller records verifier findings, performs one bounded repair only if it does not change the frozen test contract, and re-verifies.
- [ ] Commit held-out results and final governance as Commit 2 without squash or push.

