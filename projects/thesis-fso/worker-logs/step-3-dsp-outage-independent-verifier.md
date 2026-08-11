# Fresh-context Step 3 independent verification

> Task: T010 | Date: 2026-08-11 | Mode: independent read-only verification

## Verdict

- verdict=`PASS`
- critical/major/minor=`0/0/0`
- scope violation count=`0`
- accepted terminal: `STEP3_Q_SURVIVES_READY_FOR_STEP3_5`; Q001 `4/4 PASS` is supported at the repaired branch-local Wang boundary. The broader post-all-FS/CE/CPE position remains an explicit Step 3.5 debt and is not included in this PASS.

## Checks that passed

1. **Step 2 narrow repair — PASS.** JLT 2023 source is `1,803,926 B`, SHA-256 `5fe81376e5ba14beaf9576cf4223316812dc98512d0cdd7daf1f573a2646acbc`; content is `39,481 B`, `270/114` total/nonempty lines, SHA-256 `6bb3451d37ec4c821ee357b5130004d19759b89cc55813a0d5bf147766bc31c8`. Title and DOI identity match. The five qualified reads are Johst 2024, Wang 2023, Liu 2023, Tu 2020 and Yang 2022; Sun 2019 remains metadata/abstract only and is not counted as fulltext.
2. **Read structure — PASS.** T007–T009 and the five local read notes each provide title gate, at least 15 standard fields, seven explicit structured sections, communication parameters and experimental-completeness extraction. Wang, Liu and Johst provide three writing-architecture summaries.
3. **Action matrix — PASS.** The evidence supports: Sun 2019 broad action unknown; Liu estimator-changing 2N×2 CMA/RDE; Johst defect plus hard-discard boundary; Tu known-OSNR/window/positive-gain admission; Yang pilot-attenuation continuous weight; Wang FSTS/alignment then MRC before downstream pol-demux/FOE. Evidence anchors: `R004-step3-direct-competitor-synthesis.md` action matrix and worker logs `step-3-dsp-outage-read-l1-l2.md:86-115`, `step-3-dsp-outage-read-l3-l4.md` exact signatures, `step-3-dsp-outage-read-l5-p0-boundary.md` §§1.3/2.
4. **2019 limitation — PASS.** All current owners retain exact action=`UNRESOLVED`; the P0 entry is not presented as a sixth fulltext. Debt is conditioned on Q001 survival and deferred to an unapproved Step 3.5.
5. **Scope/control — PASS.** No Step 3.5/4a execution, algorithm formula, implementation, simulation, Go/Kill or METHOD_SIGNAL was produced. Topic/master/registry/D003/D004 agree that verification is pending and Step 3.5=`NOT_AUTHORIZED`. `git diff --check` produced no errors and staging is empty.

## Findings

### Major 1 — Q001 criterion 3 overstates baseline task alignment

- **Evidence:** `projects/thesis-fso/literature_notes_dsp_outage_multi_aperture.md:43-45,52` defines C as heterogeneous independently completed FS/CE/CPE lock states and calls Wang 2023 a recent post-DSP MRC baseline. However the same file's action matrix at `:32`, R004 at `R004-step3-direct-competitor-synthesis.md:20,28`, and the primary worker audit at `projects/thesis-fso/worker-logs/step-3-dsp-outage-read-l1-l2.md:86-115,163` place Wang's MRC **before** polarization demultiplexing, FOE and phase-noise estimation. Liu likewise combines inside an estimator-changing equalizer before downstream FOC/CPR, while Johst does not execute combining.
- **Impact:** The five-paper set supports the narrow collision question and a provisional candidate, but does not yet establish a recent task-matched `post-independent-DSP MRC` baseline for the exact C stated by Q001. Glossary criterion 3 should be `PARTIAL/UNRESOLVED`, so the current unconditional Q001 `4/4 PASS` is not fully supported.
- **Mechanical repair:** Either (a) revise Q001 M/C/A to the actually evidenced pre-FOE Wang ordering and re-run all four criteria, or (b) keep the post-independent-DSP C but change criterion 3 to `PARTIAL` and make Step 3.5 retrieve/verify a genuine recent post-independent-DSP MRC baseline before restoring `4/4 PASS`. Update R004, literature notes, D004 and control projections consistently; do not enter 4a meanwhile.

### Major 2 — Read-note source/persistence/casing chain is not mechanically closed

- **Evidence:** `papers/_read_notes/10.1109_jphot.2023.3265847.md:6` points to relative `papers/doi/10.1109_jphot.2023.3265847/content.md`, which does not exist in this worktree; the valid source is the shared absolute path recorded by `projects/thesis-fso/read-log.md:78` and `step-3-dsp-outage-read-l1-l2.md:81`. Four newly created read notes (WiSEE, JLT 2023, JPHOT 2020, ICCC 2022) are ignored by `.gitignore:5` and absent from `git status`/`git ls-files`. Shared-root pre-existing WiSEE/JLT notes use uppercase DOI casing while the worktree notes/read-log targets use lowercase, creating two note identities across roots.
- **Impact:** Current local evidence is readable, but the required global read-note chain can disappear from the eventual patch or resolve to a nonexistent source after handoff/merge.
- **Mechanical repair:** Correct Wang's source pointer to `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`; select one canonical casing/path for WiSEE and JLT, merge the new Step 3 increments into those canonical notes, update read-log/literature-note pointers, and explicitly force-add any intended new files under the ignored `papers/` tree. Then verify `git ls-files` contains all five canonical notes and every source/read-note path resolves.

## Terminal assessment

Initial verification was `PARTIAL 0/2/0`. After the bounded repairs verified below, `STEP3_Q_SURVIVES_READY_FOR_STEP3_5` is supported for the narrowed branch-local Q001. This remains a Step 3 problem-survival result, not novelty closure, Go/Kill, METHOD_SIGNAL or authorization to enter Step 3.5/4a.

## Repair verification — 2026-08-11

### Major 1 closure — PASS

- R004 and the canonical literature owner now define M as Wang 2023's evidenced ordering: per-branch FSTS FS/alignment plus branch phase correction → MRC → shared polarization demultiplexing/FOE (`R004-step3-direct-competitor-synthesis.md:28-35`; `literature_notes_dsp_outage_multi_aperture.md:41-53`).
- C/A and the output shape are restricted to branch-local synchronization/phase/available-estimation validity at that pre-MRC boundary. Wang 2023 is recent, optical, multi-aperture and contains the exact branch-local-DSP→MRC ordering, so glossary criterion 3 is now supported.
- The broader position after all independent FS/CE/CPE stages is explicitly criterion-3 `UNRESOLVED` and retained only as Step 3.5 baseline-alignment debt; it is not smuggled into Q001's PASS (`R004:35`; literature owner `:47`).

### Major 2 closure — PASS

- Wang's read note now points to the existing shared source `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`.
- `git ls-files --error-unmatch` succeeds for all five canonical read notes: WiSEE 2024, Wang 2023, JLT 2023, JPHOT 2020 and ICCC 2022.
- `Test-Path` is true for every source path recorded by those five notes. Canonical note names use one lowercase DOI path in this worktree; the force-added files are visible to Git.
- Fresh `git diff --check` and `git diff --cached --check` return no errors.

### Final disposition

- final verdict=`PASS`
- final critical/major/minor=`0/0/0`
- final scope violation count=`0`
