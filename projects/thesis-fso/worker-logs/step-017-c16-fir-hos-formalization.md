# T017 Phase A — C16-open full-complex FIR HOS formalization

> 2026-07-27 | executor | Groundwork Step 1 only | terminal

## Control validation

Executed from
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T017-c16-fir-hos-formalization.md
```

Raw output:

```text
PASS
```

Validated binding: `control_epoch=42`,
`mission_checkpoint=CP016`,
`action_class=CANDIDATE_FORMALIZATION`.

Process check found no simulation, MVE, Probe, seed, or prior `tools/search`
process. The current control lane was
`C16_FIR_HOS_FORMALIZATION_PREP`.

`tools/search` EOL and object preflight:

```text
git ls-files --eol tools/search
i/lf    w/lf    attr/                  tools/search

git hash-object tools/search
b7e449705acde41efa41b1b67c81b6d13aa28438

git rev-parse HEAD:tools/search
b7e449705acde41efa41b1b67c81b6d13aa28438

git status --short -- tools/search
<empty>
```

The original checkout was `w/lf`; no EOL conversion was performed.

## Protected-file baseline

Starting `git status --short`:

```text
 M .sessions/2026-07-06-step4a-mve-execution/decisions.md
 M .sessions/2026-07-06-step4a-mve-execution/topic-index.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/H002-goal-mode-campaign-recovery.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/S001-live-test-activation.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md
 M .sessions/_registry.yaml
 M projects-overview.md
 M projects/thesis-fso/direction-lab/harvest/current.yaml
 M projects/thesis-fso/direction-lab/portfolio/current.yaml
 M projects/thesis-fso/direction-lab/state/current.yaml
 M projects/thesis-fso/master-state.md
?? .sessions/2026-07-23-research-direction-lab-longitudinal-test/R007-post-c15-mechanism-carrier-remap.md
?? .sessions/2026-07-23-research-direction-lab-longitudinal-test/T017-c16-fir-hos-formalization.md
```

The complete protected baseline was hashed before search:

| Path | Starting SHA256 |
|---|---|
| `.sessions/2026-07-06-step4a-mve-execution/decisions.md` | `255db8ede7cdd5e6f0a0c3ffe4c8a1361a66952b5655a4083d7478dc1b9834ac` |
| `.sessions/2026-07-06-step4a-mve-execution/topic-index.md` | `2f57fb1ab18a5053d898fdc545c540002258f06b6fccc2cf8e791bc56d393f95` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/H002-goal-mode-campaign-recovery.md` | `4027533fbefecb914771d6671403811c873d1c9057b03ffa31352bfab1718cd1` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/S001-live-test-activation.md` | `f7a4a84be898baf86ff4c5504f8b39c21828d768aeabf50dcf7b3ad4bf0b7a2f` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md` | `aeef9ac4ae093af685addb72729a3d87cebc1b467eae43eea7147a1ad256232e` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md` | `63a824e016b9fce6cefbfffda88da075b2822f42bfdd0384d24d55b194967992` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md` | `bebf9bfeb8f4d10ddaeab138dcc48ca3974f25d8b8270ec35759c91bf64cc1d9` |
| `.sessions/_registry.yaml` | `79504467c1e796561bf6130827a43ae1910686c320585b0656a5a1ed12733193` |
| `projects-overview.md` | `6c4c32d82b0b12b7eec1faff4a395f9bb25935fda3b3388106c1f68fde2377b0` |
| `projects/thesis-fso/direction-lab/harvest/current.yaml` | `87ff12aa9f946ca4641c69819e898fd181d11ef99d8ced7bfc37bb2b257e1cc0` |
| `projects/thesis-fso/direction-lab/portfolio/current.yaml` | `d08b7af3644df35443ec882c3e4e49ddffc331932e7b22e7bc69729b1be9efc5` |
| `projects/thesis-fso/direction-lab/state/current.yaml` | `1bbe39bf5f8bce61e7568fb0c2abad9edeb13324213943e46691e04f1cd99637` |
| `projects/thesis-fso/master-state.md` | `ac04217a8692409e3e0b1ccbf065bfeeb29ff256f4c5514b95455d98bb214e65` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/R007-post-c15-mechanism-carrier-remap.md` | `5c4ee9f1c4f4b9e5299d4444320be78af3eff925884f19f67265f9a245468d9a` |
| `.sessions/2026-07-23-research-direction-lab-longitudinal-test/T017-c16-fir-hos-formalization.md` | `6025df57efd1a3eeb6aa88ab2864980d0cd793513672f73db14146e8f03a9d2a` |

All hashes were identical at closure.

## Phase A receipts

Exactly five frozen queries were run. No sixth query was issued.

| # | Query/output | Exit | Wall clock | Search receipt |
|---|---|---:|---:|---|
| A1 | `blind equalization complex convolutive MIMO QAM higher order statistics` → `c16-a1-convolutive-hos.json` | 0 | 11.124 s | OpenAlex found 411, returned 20; arXiv 0; S2 rate-limited; 16 retained JSON rows |
| A2 | `polarization multiplexed coherent optical blind FIR equalizer higher order statistics ICA` → `c16-a2-coherent-optical-fir.json` | 0 | 7.970 s | OpenAlex found/returned 8; arXiv 0; S2 rate-limited; 8 retained JSON rows |
| A3 | `non constant modulus blind equalization PM-16QAM complex FIR` → `c16-a3-nonmodulus-pmqam.json` | 0 | 27.350 s | OpenAlex found 46, returned 20; arXiv 0; S2 rate-limited; 11 retained JSON rows |
| D1 | `convolutive independent component analysis complex QAM MIMO FIR blind equalization` → `c16-d1-complex-convolutive-bss.json` | 0 | 9.207 s | OpenAlex found 190, returned 20; arXiv 0; S2 rate-limited; 17 retained JSON rows |
| D2 | `coherent optical PM-QAM blind source separation cumulant joint diagonalization equalizer` → `c16-d2-optical-cumulant-fir.json` | 0 | 8.339 s | OpenAlex found/returned 1; arXiv 0; S2 rate-limited; 1 retained JSON row |

The query configuration named `s2 openalex arxiv`, but singleton provenance in
the 53 retained rows was only `openalex`. Empty arXiv returns and S2
rate-limit messages were not counted as actual sources.

Primary artifacts:

| Bytes | SHA256 | Path |
|---:|---|---|
| 39,288 | `e0979a5e606df1dc6f7d44a26ff9df07d6f95081bdfd85f5aba4e38fef502a2f` | `search-archive/2026-07-27/c16-a1-convolutive-hos.json` |
| 24,247 | `1bceb5a5dfc297665494d287ee22f4032a38596f397558cc3b743d1450346038` | `search-archive/2026-07-27/c16-a2-coherent-optical-fir.json` |
| 34,287 | `201cd8c90223b7c197991883c08963d2f1eab34c32950d04362b56f43b01da73` | `search-archive/2026-07-27/c16-a3-nonmodulus-pmqam.json` |
| 42,256 | `eb3c91e1f3e26792a07408f8897bbf7f852fa4691efec04f588eacb8c5d1f32f` | `search-archive/2026-07-27/c16-d1-complex-convolutive-bss.json` |
| 4,197 | `588f2b122fbdee155942eaa2f3232cd7980ab0840a462e1a685f9f16187f36c0` | `search-archive/2026-07-27/c16-d2-optical-cumulant-fir.json` |
| 165,912 | `2d167ec74759a2f460b923cbf516e627a18003843f47729f5689d5a1da20e2d8` | `search-archive/2026-07-27/c16-fir-hos-candidate-view.json` |

Automatic `tools/search` archive/index side effects, retained as authorized
search artifacts:

| Bytes | SHA256 | Path |
|---:|---|---|
| 34,361 | `b061cc8c2e088db9367e79d8735416d144bb4ac4fdb43aa0e92443366ec40cab` | `search-archive/2026-07-27/blind-equalization-complex-convolutive-mimo-qam-higher-order.json` |
| 21,744 | `70c6ea5f89d51f385bf4861974d0b78d0eb6b3272d3ea803407fc09cbf7e873a` | `search-archive/2026-07-27/polarization-multiplexed-coherent-optical-blind-fir-equalize.json` |
| 30,888 | `d68e7ed783c3d7797156602ef1c44664704374bed1485e12e639bb7e571a89f1` | `search-archive/2026-07-27/non-constant-modulus-blind-equalization-pm-16qam-complex-fir.json` |
| 37,047 | `dfc8febf2ad2a8291ff45441b8b9da938bcd996e255afdbf0d554d6cb15b55d6` | `search-archive/2026-07-27/convolutive-independent-component-analysis-complex-qam-mimo-.json` |
| 3,878 | `819497850ced4e26479e2a5cc1e8915212dae8c230354e078172823d65eaa01e` | `search-archive/2026-07-27/coherent-optical-pm-qam-blind-source-separation-cumulant-joi.json` |
| 39,219,007 | `356f6627b581e87ae63394af9cf91d67eaa110fdfbcbbf5bd4ebe9041125c7f7` | `search-archive/_index/all-papers.jsonl` |

## AI review and identity

All 53 retained rows were reviewed from title, abstract, venue, year,
citations, and publication status. Every row has `priority`,
`priority_reason`, `route`, `task_fit`, and `exclusion_reason`; deterministic
closure found `53/53` complete and no excluded row lacked a reason.

Identity rules applied:

- DOI lowercased and DOI URL/prefix removed;
- title normalized with Unicode NFKC, lowercase, and non-alphanumeric removal;
- identical DOI rows merged;
- no-DOI rows merged only under normalized-title, year ±1, and first-author
  agreement;
- same normalized title with multiple nonempty DOI would be quarantined.

Counts:

```text
raw retained rows = 53
unique non-quarantine candidates = 44
identity quarantine groups = 0
published/preprint/unknown = 42/2/0
published ratio = 42/44 = 0.9545454545
priority: 必读=2, 建议读=4, 待确认=1, 备选=12, 排除=25
R1 direct/adjacent = 1/3
R2 direct/adjacent = 3/1
R3 direct/adjacent = 2/9
OUT_OF_SCOPE none = 25
```

The 10-paper downloader view is at top-level `results` in
`c16-fir-hos-candidate-view.json`; all entries have stable IDs
`c16-p001` through `c16-p010`, identity fields, route/priority reasons, and
complete raw retrieval locators. Top-level `candidates` contains all 44
non-quarantine candidates. `identity_quarantine` is empty.

Acquisition pool:

1. Blind Equalization in Optical Communications Using Independent Component Analysis
2. Blind Polarization Demultiplexing of Shaped QAM Signals Assisted by Temporal Correlations
3. Widely Linear Filtering for Multiimpairment Compensation in Dispersion Managed mQAM Modulated Optical Systems
4. Blind I/Q Signal Separation-Based Solutions for Receiver Signal Processing
5. DSP for Coherent Single-Carrier Receivers
6. Robust Blind Equalization for NB-IoT Driven by QAM Signals
7. A Simplified Constant Modulus Algorithm for Blind Recovery of MIMO QAM and PSK Signals: A Criterion with Convergence Analysis
8. Advanced DSP for Coherent Optical Fiber Communication
9. Experimental Investigation on Low-Complexity Adaptive Equalizer Including RSOP Tracking and Phase Recovery for 112 Gb/s PDM-QPSK Transmission System
10. Blind Fractionally Spaced Channel Equalization for Shallow Water PPM Digital Communications Links

## Step 1 gate

| Gate | Value | Required | Result |
|---|---:|---:|---|
| actual source families | 1 (`openalex`) | ≥3 | **FAIL** |
| unique non-quarantine count | 44 | ≥20 | PASS |
| published ratio | 0.9545454545 | ≥0.50 | PASS |
| must-read count | 2 | ≥5 | **FAIL** |
| direct R1 | 1 | ≥1 | PASS |
| direct R2 | 3 | ≥1 | PASS |
| acquisition pool | 10 | 8–12 | PASS |
| pool candidates in quarantine | 0 | 0 | PASS |

A6 failed on actual-source coverage and must-read density. Per the frozen
contract, terminal status is `BLOCKED_SEARCH_OR_IDENTITY`. Phase B is not
authorized. No query, source repair, download, conversion, or threshold change
was added.

## Phase B receipts

Not run. `PHASE_B_AUTHORIZED=FALSE`.

No fulltext census, download, conversion, or acquisition receipt exists.

## Coverage-gap report

Not applicable because A6 failed and Phase B was not authorized.

The Step 1 gap is explicit:

- only one actual source family appeared in raw singleton provenance;
- only two candidates met the frozen AI-review `必读` bar;
- quantity, publication ratio, both direct routes, pool size, and identity
  quarantine gates otherwise passed.

`valid_fulltext_count=0` means “not entered,” not a fulltext failure.

## Stop discipline

- Stopped at A6.
- Did not run Phase B.
- Did not download or convert any paper.
- Did not perform fulltext close reading.
- Did not write Q# or modify `literature_notes.md`.
- Did not enter Step 3 or Step 5.
- Did not run old C16 code or use seeds 71–80.
- Did not implement FIR/HOS.
- Did not run simulation, Probe, MVE, seed, or collision-check.
- Did not modify `.sessions`, live/formal owner, mission-log, current
  projections, registry, common, params, Skill, or controller.

## Git and artifact closure

After the searches, WSL-side Python changed five tracked `.pyc` files despite
the PowerShell-side `PYTHONDONTWRITEBYTECODE=1`. The five files were clean in
the starting status and therefore execution-created pollution. Each was
restored byte-for-byte from its HEAD blob and independently checked:

```text
tools/litsearch/__pycache__/__init__.cpython-312.pyc
  worktree=HEAD=cfcaa84d481c5081d06a93f99aaa82a0040f577b
tools/litsearch/__pycache__/search_config.cpython-312.pyc
  worktree=HEAD=928f1060dfe7efe038e211f8cdb76495a39cc2a0
tools/litsearch/__pycache__/search_output.cpython-312.pyc
  worktree=HEAD=d37e865a7a3cb2be083091657d92908715dad702
tools/litsearch/__pycache__/search_pipeline.cpython-312.pyc
  worktree=HEAD=12698dc4c003eedd2afc58a1ff63d59389c17b85
tools/litsearch/__pycache__/search_sources.cpython-312.pyc
  worktree=HEAD=5465c461e7b463ac7c4f216aa07adb1ecc570164
```

`tools/search` remained `w/lf`, clean, and object-identical to HEAD:
`b7e449705acde41efa41b1b67c81b6d13aa28438`.

All fifteen protected baseline SHA256 values remained identical. Final status
adds only this authorized worker log to the starting visible status; search
artifacts remain ignored under `search-archive/`.

```text
 M .sessions/2026-07-06-step4a-mve-execution/decisions.md
 M .sessions/2026-07-06-step4a-mve-execution/topic-index.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/H002-goal-mode-campaign-recovery.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/S001-live-test-activation.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
 M .sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md
 M .sessions/_registry.yaml
 M projects-overview.md
 M projects/thesis-fso/direction-lab/harvest/current.yaml
 M projects/thesis-fso/direction-lab/portfolio/current.yaml
 M projects/thesis-fso/direction-lab/state/current.yaml
 M projects/thesis-fso/master-state.md
?? .sessions/2026-07-23-research-direction-lab-longitudinal-test/R007-post-c15-mechanism-carrier-remap.md
?? .sessions/2026-07-23-research-direction-lab-longitudinal-test/T017-c16-fir-hos-formalization.md
?? projects/thesis-fso/worker-logs/step-017-c16-fir-hos-formalization.md
```

## Terminal report

```text
terminal_status_allowed=BLOCKED_PREFLIGHT|BLOCKED_EXECUTION_TIMEBOX|BLOCKED_SEARCH_OR_IDENTITY|BLOCKED_FULLTEXT_COVERAGE|AWAITING_COVERAGE_CONFIRMATION
terminal_status=BLOCKED_SEARCH_OR_IDENTITY
execution_phase=A
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
actual_source_families=1
unique_nonquarantine_count=44
published_ratio=0.9545454545
must_read_count=2
direct_route_R1=1
direct_route_R2=3
acquisition_pool_count=10
valid_fulltext_count=0
PHASE_B_AUTHORIZED=FALSE
STEP3_AUTHORIZED=FALSE
same_axis_streak_proposed=1
repair_streak_proposed=0
no_method_streak_proposed=17
anomaly=S2 rate-limited and arXiv empty on all five frozen queries, leaving only OpenAlex singleton provenance; WSL search also rewrote five tracked pyc files despite the parent PowerShell environment flag, and those files were restored exactly to HEAD.
```
