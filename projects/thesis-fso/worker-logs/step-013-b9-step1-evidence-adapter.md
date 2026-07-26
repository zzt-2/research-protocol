# Step 013 — B9 Step 1 evidence adapter

## Status

- task_control: PASS
- phase: A4
- final_status: BLOCKED_SEARCH_COVERAGE
- phase_disposition: A4_COMPLETE_AWAITING_MASTER_ACCEPTANCE
- formal_science_disposition: BLOCKED_SEARCH_COVERAGE
- mission_method_delta: NONE
- simulation_or_seed_run: false

## Exact commands and exits

1. Task-control validator

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py --repo-root . .sessions\2026-07-23-research-direction-lab-longitudinal-test\T013-b9-step1-evidence-adapter.md
```

- exit: `0`
- output: `PASS`

2. Clean-tree and active-owner gate

```powershell
git status --short
rg -n -A 6 "^## D026:|^## D015:|^> status: active" .sessions\2026-07-06-step4a-mve-execution\decisions.md .sessions\2026-07-23-research-direction-lab-longitudinal-test\decisions.md
Test-Path -LiteralPath 'search-archive\2026-07-27'
```

- exits: `0`, `0`, `0`
- result: initial `git status --short` empty; formal D026 active; live D015 active;
  archive directory returned `False`.

3. Local ignored index seed

```powershell
New-Item -ItemType Directory -Force 'search-archive\_index' | Out-Null
Copy-Item -LiteralPath 'D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl' -Destination 'search-archive\_index\all-papers.jsonl'
```

- exit: `0`
- source lines: `20747`
- destination lines immediately after copy: `20747`

4. Broad search 1

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'virtual carrier self coherent free space optical digital resolution enhancer' --mode academic --preset problem-driven --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/virtual-carrier-self-coherent-free-space-optical-digital-res.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\virtual-carrier-self-coherent-free-space-optical-digital-res.json`
- source returns: OpenAlex `20` raw, `13` after filtering; S2 rate-limited;
  SerpAPI/Tavily/Firecrawl/Exa skipped for absent API keys.
- index update: `[索引] +4 新 / 9 更新 → all-papers.jsonl（总 20751）`

5. Broad search 2

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'low resolution DAC quantization noise shaping coherent optical DRE' --mode academic --preset problem-driven --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/low-resolution-dac-quantization-noise-shaping-coherent-optic.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\low-resolution-dac-quantization-noise-shaping-coherent-optic.json`
- source returns: OpenAlex `10` raw, `8` after filtering; S2 rate-limited;
  SerpAPI/Tavily/Firecrawl/Exa skipped for absent API keys.
- index update: `[索引] +6 新 / 2 更新 → all-papers.jsonl（总 20757）`

6. Broad search 3

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'Kramers Kronig DC Value self coherent FSO virtual carrier' --mode academic --preset scenario-method --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/kramers-kronig-dc-value-self-coherent-fso-virtual-carrier.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\kramers-kronig-dc-value-self-coherent-fso-virtual-carrier.json`
- source returns: three OpenAlex subqueries returned `20 + 8 + 20 = 48` raw,
  `45` after deduplication and `26` after filtering; all three S2 subqueries were
  rate-limited; SerpAPI/Exa skipped for absent API keys.
- index update: `[索引] +24 新 / 2 更新 → all-papers.jsonl（总 20781）`

7. A1 verification and generated-side-effect cleanup

```powershell
Get-ChildItem -LiteralPath 'search-archive\2026-07-27' -File | Sort-Object Name
Get-Content -Raw -LiteralPath <each-of-three-archives> | ConvertFrom-Json
git status --short
```

- exit: `0`
- result: exactly three A1 archives; all three JSON parses PASS; local index
  has `20781` lines.
- anomaly handled: `tools/search` refreshed five tracked
  `tools/litsearch/__pycache__/*.cpython-312.pyc` files. Their exact HEAD blobs
  were extracted with `git archive`, hash-checked, and copied back. Final
  tracked diff before adding this worker log was empty.

8. A2 fresh resume gate (the initial A1 clean-tree gate was not rerun)

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py --repo-root . .sessions\2026-07-23-research-direction-lab-longitudinal-test\T013-b9-step1-evidence-adapter.md
```

- exit: `0`
- output: `PASS`
- control check: topic control contains epoch `32` and checkpoint `CP012`.
- A1 archive check: all three parse; result counts `13 / 8 / 26`.
- A2 absence check: none of the four directional-query archive patterns existed.
- resume state: exactly three query archives; local index `20781` lines; the
  only non-ignored status was this expected partial worker log.

9. Directional deep search 1

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'error feedback noise shaping EFNS low resolution DAC coherent optical' --mode academic --preset comparison --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/error-feedback-noise-shaping-efns-low-resolution-dac-coheren.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\error-feedback-noise-shaping-efns-low-resolution-dac-coheren.json`
- source returns: OpenAlex `0` raw and `0` returned; S2 rate-limited;
  SerpAPI/Exa skipped for absent API keys.
- index update: no `[索引]` line because the archive had zero results; local
  index remained `20781` lines.

10. Directional deep search 2

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'trellis quantization noise shaping low resolution optical DAC digital resolution enhancement' --mode academic --preset comparison --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/trellis-quantization-noise-shaping-low-resolution-optical-da.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\trellis-quantization-noise-shaping-low-resolution-optical-da.json`
- source returns: OpenAlex `7` raw, `6` after deduplication, `2` after
  filtering; S2 rate-limited; SerpAPI/Exa skipped for absent API keys.
- index update: `[索引] +1 新 / 1 更新 → all-papers.jsonl（总 20782）`

11. Directional deep search 3

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'satellite ground self coherent FSO turbulence virtual carrier CSPR' --mode academic --preset comparison --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/satellite-ground-self-coherent-fso-turbulence-virtual-carrie.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\satellite-ground-self-coherent-fso-turbulence-virtual-carrie.json`
- source returns: OpenAlex `0` raw and `0` returned; S2 rate-limited;
  SerpAPI/Exa skipped for absent API keys.
- index update: no `[索引]` line because the archive had zero results; local
  index remained `20782` lines.

12. Directional deep search 4

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'free space optical turbulence self coherent detection low complexity phase reconstruction' --mode academic --preset comparison --max-per-source 20 --top 30"
```

- exit: `0`
- `[存档]`:
  `search-archive/2026-07-27/free-space-optical-turbulence-self-coherent-detection-low-co.json`
- absolute archive:
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-27\free-space-optical-turbulence-self-coherent-detection-low-co.json`
- source returns: OpenAlex `20` raw, `20` after deduplication, `12` after
  filtering; S2 rate-limited; SerpAPI/Exa skipped for absent API keys.
- index update: `[索引] +7 新 / 5 更新 → all-papers.jsonl（总 20789）`

13. A2 verification and generated-side-effect cleanup

```powershell
Get-ChildItem -LiteralPath 'search-archive\2026-07-27' -File | Sort-Object Name
Get-Content -Raw -LiteralPath <each-of-seven-query-archives> | ConvertFrom-Json
git status --short
git diff --check
```

- exit: `0`
- result: exactly seven T013 query archives; all seven JSON parses PASS; no
  candidate view exists; local index has `20789` lines.
- anomaly handled: A2 again refreshed the same five tracked
  `tools/litsearch/__pycache__/*.cpython-312.pyc` files. Their exact HEAD blobs
  were extracted with `git archive`, copied back, and verified by
  `git rev-parse HEAD:<path>` versus `git hash-object <path>`. Final
  non-ignored status is only this worker log.

14. Phase A3-1 manual semantic review

- reviewed only:
  - `search-archive/2026-07-27/virtual-carrier-self-coherent-free-space-optical-digital-res.json`
    — `13/13` results annotated; priority counts:
    `必读=1, 建议读=1, 待确认=0, 备选=1, 排除=10`.
  - `search-archive/2026-07-27/low-resolution-dac-quantization-noise-shaping-coherent-optic.json`
    — `8/8` results annotated; priority counts:
    `必读=4, 建议读=3, 待确认=0, 备选=0, 排除=1`.
- combined: `21/21` results annotated; priority counts:
  `必读=5, 建议读=4, 待确认=0, 备选=1, 排除=11`.
- evidence basis: existing `title/abstract/venue/year/citation_count/publication_status`
  only; DOI/title were used only to identify the exact B9 anchor.
- parse check: both JSON files PASS; required semantic fields missing=`0`.
- evidence-scope check: only exact B9 title/DOI
  `10.1109/jlt.2023.3270673` is `EXISTING_FULLTEXT`; all other reviewed results
  are `METADATA_ONLY`.
- no other archive was reviewed; A4 was not started.

15. Phase A3-2 manual semantic review

- reviewed only:
  - `search-archive/2026-07-27/kramers-kronig-dc-value-self-coherent-fso-virtual-carrier.json`
    — `26/26` results annotated; priority counts:
    `必读=4, 建议读=7, 待确认=0, 备选=1, 排除=14`.
- evidence basis: existing `title/abstract/venue/year/citation_count/publication_status`
  only; no metadata was added or inferred.
- parse check: JSON PASS; required semantic fields missing=`0`;
  invalid `priority/route/collision_role/evidence_scope` enum values=`0`.
- evidence-scope check: `EXISTING_FULLTEXT=1`, only exact B9 title/DOI
  `10.1109/jlt.2023.3270673`; all other results are `METADATA_ONLY`.
- final status remains `PARTIAL_A3_REVIEW_IN_PROGRESS`;
  `mission_method_delta=NONE`; `simulation_or_seed_run=false`.
- no other archive was reviewed; A4 was not started.

16. Phase A3-3 manual semantic review

- reviewed only:
  - `search-archive/2026-07-27/error-feedback-noise-shaping-efns-low-resolution-dac-coheren.json`
    — `0` results; archive reviewed with no result object available to annotate;
    no candidate was fabricated; priority counts:
    `必读=0, 建议读=0, 待确认=0, 备选=0, 排除=0`.
  - `search-archive/2026-07-27/trellis-quantization-noise-shaping-low-resolution-optical-da.json`
    — `2/2` results annotated; priority counts:
    `必读=0, 建议读=0, 待确认=0, 备选=0, 排除=2`.
- combined: `2/2` available results annotated; priority counts:
  `必读=0, 建议读=0, 待确认=0, 备选=0, 排除=2`.
- evidence basis: existing `title/abstract/venue/year/citation_count/publication_status`
  only; no metadata was added or inferred.
- evidence-scope check: both annotated results are `METADATA_ONLY`; neither is
  the exact B9 title/DOI anchor.
- parse check: both JSON files PASS; required semantic fields missing=`0`;
  invalid `priority/route/collision_role/evidence_scope` enum values=`0`.
- final status remains `PARTIAL_A3_REVIEW_IN_PROGRESS`;
  `mission_method_delta=NONE`; `simulation_or_seed_run=false`.
- no other archive was reviewed; A4 was not started.

17. Phase A3-4 manual semantic review

- reviewed only:
  - `search-archive/2026-07-27/satellite-ground-self-coherent-fso-turbulence-virtual-carrie.json`
    — `0` results; archive reviewed with no result object available to annotate;
    no candidate was fabricated; priority counts:
    `必读=0, 建议读=0, 待确认=0, 备选=0, 排除=0`.
  - `search-archive/2026-07-27/free-space-optical-turbulence-self-coherent-detection-low-co.json`
    — `12/12` results annotated; priority counts:
    `必读=0, 建议读=1, 待确认=0, 备选=1, 排除=10`.
- combined: `12/12` available results annotated; priority counts:
  `必读=0, 建议读=1, 待确认=0, 备选=1, 排除=10`.
- evidence basis: existing `title/abstract/venue/year/citation_count/publication_status`
  only; no metadata was added or inferred.
- evidence-scope check: all 12 annotated results are `METADATA_ONLY`; none is
  the exact B9 title/DOI anchor.
- full A3 integrity check: all seven archives parse PASS; all `61/61` nonempty
  result objects contain nonempty
  `priority/priority_reason/route/collision_role/evidence_scope`; invalid
  `priority/route/collision_role/evidence_scope` enum values=`0`.
- exact B9 title/DOI is marked `EXISTING_FULLTEXT` in two archives because the
  same anchor appears in both query result sets; no other result has that scope.
- final status remains `PARTIAL_A3_REVIEW_IN_PROGRESS`; phase disposition is
  `A3_COMPLETE_AWAITING_A4`; `mission_method_delta=NONE`;
  `simulation_or_seed_run=false`.
- A4 was not started; no candidate view was created.

18. Phase A4 synthesis and Step 1 gate

- inputs: seven A3-annotated archives plus the worktree-local ignored index.
- deduplication: DOI and normalized-title union; `61` raw records became `58`
  unique results. The exact B9 DOI/title and FSO-survey duplicates were merged.
  The two `100G FSO...` records were merged by normalized title while retaining
  both DOI identifiers and both archive pointers.
- local-index handling: `source_apis` strings are retained verbatim as
  historical provenance only; merged strings were not split into artificial
  source families.
- output:
  `search-archive/2026-07-27/b9-step1-candidate-view.json`.
- Step 1: `BLOCKED_SEARCH_COVERAGE` because the search run has only one actual
  source family, Route A has zero nonexcluded deep-search records, and no deep
  search positively supports an uncovered candidate-specific problem.
- `formal_science_disposition=BLOCKED_SEARCH_COVERAGE`;
  `mission_method_delta=NONE`; `simulation_or_seed_run=false`.

## Input-anchor audit

| asset | identity/title/DOI check | allowed evidence scope |
|---|---|---|
| `papers/doi/10.1109_jlt.2023.3270673/metadata.json` | title=`Simplified Self-Coherent FSO Transmission Boosted by Digital Resolution Enhancer`; DOI=`10.1109/jlt.2023.3270673` | metadata identity only in A1 |
| `papers/doi/10.1109_jlt.2023.3270673/content.md` | exists; not read in A1 | existing fulltext anchor, not consumed in A1 |
| `papers/_read_notes/_B9-virtual-carrier-dre-increment.md` | exists; not read in A1 | prior internal anchor only |
| shared `search-archive/_index/all-papers.jsonl` | exists; copied at `20747` lines | local index seed/provenance only |
| shared `papers/index.json` | exists; unchanged | identity/provenance only |
| two specified old `.sessions` extracts | both exist; unchanged | prior internal anchor only |
| `projects/thesis-fso/literature_notes.md` | exists; unchanged | prior internal anchor only |

## Search-source audit

| archive | query | actual source family | returned | parse |
|---|---|---|---:|---|
| `virtual-carrier-self-coherent-free-space-optical-digital-res.json` | virtual carrier self coherent free space optical digital resolution enhancer | OpenAlex | 13 | PASS |
| `low-resolution-dac-quantization-noise-shaping-coherent-optic.json` | low resolution DAC quantization noise shaping coherent optical DRE | OpenAlex | 8 | PASS |
| `kramers-kronig-dc-value-self-coherent-fso-virtual-carrier.json` | Kramers Kronig DC Value self coherent FSO virtual carrier | OpenAlex | 26 | PASS |
| `error-feedback-noise-shaping-efns-low-resolution-dac-coheren.json` | error feedback noise shaping EFNS low resolution DAC coherent optical | none (OpenAlex returned zero) | 0 | PASS |
| `trellis-quantization-noise-shaping-low-resolution-optical-da.json` | trellis quantization noise shaping low resolution optical DAC digital resolution enhancement | OpenAlex | 2 | PASS |
| `satellite-ground-self-coherent-fso-turbulence-virtual-carrie.json` | satellite ground self coherent FSO turbulence virtual carrier CSPR | none (OpenAlex returned zero) | 0 | PASS |
| `free-space-optical-turbulence-self-coherent-detection-low-co.json` | free space optical turbulence self coherent detection low complexity phase reconstruction | OpenAlex | 12 | PASS |

Configured source names are not counted as successful source families. S2
returned no records because of rate limiting; sources without API keys returned
no records. `openalex+openalex` in two deduplicated result records is one actual
OpenAlex family, not two families.

## Deduplicated coverage

- raw_results: `61`
- deduplicated_unique: `58`
- nonexcluded_unique: `21`
- excluded_unique: `37`
- actual_source_families: `1` (`OpenAlex`)
- route_A_count: `8` inclusive (`4` A-only + `4` BOTH); deep nonexcluded=`0`
- route_B_count: `17` inclusive (`13` B-only + `4` BOTH); deep nonexcluded=`2`
- must_read: `8`
- formally_published: `21`
- published_ratio: `100%`
- all `61/61` raw items retain human
  `priority/priority_reason/route/collision_role/evidence_scope`.

## Candidate table

The candidate view contains all `58` deduplicated records with required
metadata, abstract, identifiers, source provenance, archive/line pointers, and
semantic fields. The nonexcluded portfolio is:

| class | unique | key roles |
|---|---:|---|
| 必读 | 8 | DRE/B9/100G canonical, EFNS direct competitor, KK/DC comparators |
| 建议读 | 10 | FSO task-fit, adjacent shaping, KK/DC lineage |
| 备选 | 3 | adjacent/task-fit context |
| 排除 | 37 | false positives retained for audit |

## Route A — low-resolution DAC/noise shaping

- `8` inclusive unique candidates: `4` A-only and `4` BOTH.
- Broad evidence contains DRE canonical papers, EFNS, joint shaping, and
  task-linked carrier+DRE records. The two deep archives contribute `0`
  nonexcluded candidates.
- EFNS is a direct competitor: its metadata reports similar DRE performance at
  PNoB ≥ 4 plus lower complexity, no processing latency, and no channel-response
  requirement. Generic DRE/noise-shaping novelty is materially collided, while
  the targeted deep evidence remains insufficient.

## Route B — self-coherent/FSO task fit

- `17` inclusive unique candidates: `13` B-only and `4` BOTH.
- Broad evidence covers B9/100G FSO, KK/DC-Value comparators, and FSO task-fit
  records. Deep evidence contributes `2` general task-fit/adjacent FSO records.
- The satellite-ground self-coherent directional archive returned `0` results;
  therefore current metadata cannot positively establish a star-ground
  turbulence-specific problem.

## Direct-competition and gap adjudication

Route A is directly collided by EFNS and adjacent shaping work. Route B has no
result proving complete direct-competition coverage of satellite-ground
turbulent FSO, but the targeted search also returned no supporting evidence.
Absence is not promoted to a gap. This is a coverage/remap block, not a B9
family Kill and not a method signal.

## Acquisition debt

| role | exact title/id | why Step 2 needs it | current availability |
|---|---|---|---|
| DRE canonical | Digital Resolution Enhancer Employing Clipping for High-Speed Optical Transmission / `10.1109/jlt.2020.2988377` | recover original DRE construct and boundary | METADATA_ONLY |
| DRE canonical | Kramers-Kronig Receiver With Digitally Added Carrier Combined With Digital Resolution Enhancer / `10.1109/jlt.2022.3142353` | separate carrier reconstruction from DRE | METADATA_ONLY |
| DRE canonical | Simplified Self-Coherent FSO Transmission Boosted by Digital Resolution Enhancer / `10.1109/jlt.2023.3270673` | exact B9 scenario and claim ceiling | EXISTING_FULLTEXT |
| DC-Value/virtual-carrier lineage | DC Component Recovery in Kramers-Kronig Receiver Utilizing AC-Coupled Photo-Detector / `10.1109/jlt.2020.2990905` | recover DC-component assumptions | METADATA_ONLY |
| DC-Value/virtual-carrier lineage | Comparison of DC-Value Method and Kramers–Kronig Receiver in Optical OFDM SSB-DD Transmission / `10.1109/jphot.2022.3192263` | compare DC-Value and KK tasks | METADATA_ONLY |
| traditional noise-shaping comparator | Performance Investigation of Error-Feedback Noise Shaping in Low-Resolution High-Speed IM/DD and Coherent Transmission Systems / `10.1109/jlt.2022.3153387` | audit direct EFNS comparator | METADATA_ONLY |
| traditional noise-shaping comparator | Low-resolution optical transmission using joint shaping technique of signal probability and quantization noise / `10.3788/col202321.050602` | cover non-DRE shaping comparator | METADATA_ONLY |
| traditional noise-shaping comparator | Real-Time Experimental Demonstration of Hybrid FSO/Wireless Transmission Based on Coherent Detection and Delta-Sigma Modulation / `10.1109/jphot.2022.3219558` | distinguish delta-sigma from transmitter DRE | METADATA_ONLY |
| self-coherent/FSO task-fit | 100G FSO Transmission Using 3-Bit DAC and Self-Coherent Detection / `10.23919/ofc49934.2023.10116945` | closest 3-bit self-coherent FSO task lineage | METADATA_ONLY |
| self-coherent/FSO task-fit | Revolutionizing Free-Space Optics: A Survey of Enabling Technologies, Challenges, Trends, and Prospects of Beyond 5G Free-Space Optical (FSO) Communication Systems / `10.3390/s24248036` | define FSO deployment constraints without projecting satellite evidence | METADATA_ONLY |

## Integrity boundaries

- A4 used only the seven annotated archives and worktree-local index; no web,
  download, conversion, new fulltext reading, simulation, seed, MVE, or test
  matrix was run.
- Only the exact B9 DOI/title is `EXISTING_FULLTEXT`; all other unique results
  are `METADATA_ONLY`.
- Index labels such as `semantic_scholar+exa` and `openalex+openalex` remain
  unsplit historical provenance and do not increase the actual source-family
  count.
- No `.sessions/**`, master/current owner, shared papers/index, tool, Skill,
  Step 2/3, Contract, or Execute artifact was modified.
- Candidate view remains ignored and is not force-added; only this worker log
  is eligible for the task commit.
- formal_science_disposition: `BLOCKED_SEARCH_COVERAGE`.
- mission_method_delta: `NONE`.
- simulation_or_seed_run: `false`.

## Next gate

等待主控独立验收；未进入 Step 2。
