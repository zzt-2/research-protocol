# Task 1A brief: receiver/truth firewall and deterministic paired generator

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. Do not commit. Write files only with `apply_patch`.

Read first:

- `projects/simulation/explore/dsp-outage-aware-combining/design.md`
- `projects/simulation/explore/dsp-outage-aware-combining/implementation-plan.md`
- `code-quality.md`
- `reference/sim-template/` only as needed for local testing conventions

Scope: implement only the receiver/truth DTO firewall and deterministic paired natural-channel generator in the new isolated sandbox. Do not implement estimators, combiners, dev/test runner, soft weighting, or any proposed method.

Required TDD chronology:

1. Create `test_smoke.py` first with focused tests for the DTO firewall, deterministic replay, the 18-cell grid, physical offset insertion, and absence of explicit defect-injection controls.
2. Run the focused tests and capture the expected RED result.
3. Implement `smoke_core.py` minimally until those tests are GREEN.
4. Re-run the focused tests and report exact commands/results.

Required implementation shape:

- Frozen receiver-visible `ReceiverFrame` and truth-only `TruthRecord` dataclasses. Receiver-visible fields may include received complex samples, known FSTS/pilots and positions, sample time, maximum search offset, and immutable cell identity. They must not expose true channel, true phase/CFO/SNR/turbulence, TX payload bits/symbols, or true offsets.
- Frozen `CellSpec`; `build_primary_cells()` returns exactly 18 natural physical cells: weak/moderate/strong Gamma-Gamma × K in {2,4} × heterogeneity in {H0,H1,H2}.
- Gamma-Gamma triples are the current repository scan values `(11.6,10.1)`, `(4.0,1.9)`, `(4.2,1.4)` and must be labeled `UNVERIFIED_RANGE` in metadata/comments, not claimed as uniquely authoritative.
- H0/H1/H2 branch mean-SNR offsets: 0/0 dB, 0/-1 dB, 0/-6 dB; for K=4 replicate the strong/weak classes deterministically. Mark the K=4 construction `UNVERIFIED_RANGE`.
- 10 GBd, 50 kHz linewidth, 320-symbol deterministic QPSK FSTS, 30,720-symbol post-FSTS block with known pilots every 100 symbols. Fixed payload scoring later excludes known pilots.
- Natural generation only: independent per-branch Gamma-Gamma irradiance, shared Wiener laser phase plus branch static phase, receiver AWGN, and actual integer branch-prefix offsets in 0..7. No forced slips, outage flags, BER corruption, or defect injection.
- Use explicit local `numpy.random.Generator`/`SeedSequence`; never global SciPy/NumPy RNG. Same `(cell, seed)` must reproduce receiver samples and truth exactly. All future arms will consume the same generated frame.
- Provide a receiver-only realization hash that excludes truth metadata.
- Local QPSK mapping is acceptable; do not modify/import-edit `common/`, `params.py`, old b3 code, formal project code, or governance files.

Tests should also establish that changing/copied truth metadata cannot alter the receiver frame/hash, without yet testing method outputs.

Do not touch unrelated dirty files, `p05`, coded artifacts, `.sessions/profile.md`, or paper indexes.

At completion write `projects/simulation/explore/dsp-outage-aware-combining/task-1a-report.md` with: files changed, RED evidence, GREEN evidence, design deviations, and remaining risks. Then send the parent a concise summary.
