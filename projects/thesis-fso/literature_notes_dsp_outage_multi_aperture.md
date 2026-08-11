# Literature Notes — DSP-outage-aware multi-aperture combining

> Owner: `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/`
> Groundwork status: Step 1 complete; Step 2 accepted with 2019 fulltext limitation; Step 3 complete and independently verified.

## Progress

| Step | Status | Evidence |
|---|---|---|
| 1 search | COMPLETE / VERIFIED | `R001-step1-synthesis.md`, V001 |
| 2 acquire | ACCEPTED WITH LIMITATION | `R002-step2-acquisition-coverage.md`, `R003-step2-acquisition-receipt.md`, D003 |
| 3 read | COMPLETE / VERIFIED | T007–T010 worker logs, five global read notes, R004, V003 |
| 3.5+ | NOT AUTHORIZED | 2019 P0 debt only if Q001 survives verification |

## Five fulltext reads

| ID | Identity | Role | Full read note | Core finding |
|---|---|---|---|---|
| L1 | Johst et al., WiSEE 2024, `10.1109/WISEE61249.2024.10850117` | defect + hard discard | `papers/_read_notes/10.1109_wisee61249.2024.10850117.md` | branch DSP outage appears around `-1 dB`; invalid branches should be discarded, but no combining policy is tested |
| L2 | Wang et al., JPHOT 2023, `10.1109/JPHOT.2023.3265847` | post-DSP MRC reference | `papers/_read_notes/10.1109_jphot.2023.3265847.md` | FSTS performs FS/alignment; branch phase correction then MRC; no validity weight/drop |
| L3 | Liu et al., JLT 2023, `10.1109/JLT.2023.3276637` | strongest estimator-changing optical competitor | `papers/_read_notes/10.1109_jlt.2023.3276637.md` | 2N×2 blind CMA/RDE FIR jointly estimates/equalizes/combines; no validity output or abstention |
| L4 | Tu et al., JPHOT 2020, `10.1109/JPHOT.2020.2977955` | phase/admission cheap alternative | `papers/_read_notes/10.1109_jphot.2020.2977955.md` | OSNR-driven minimum phase window and positive-net-gain recursive EGC; assumes ideal time alignment/known OSNR |
| L5 | Yang et al., ICCC 2022, `10.1109/ICCC56324.2022.10065885` | RF soft-weight neighbor | `papers/_read_notes/10.1109_iccc56324.2022.10065885.md` | pilot attenuation genuinely drives continuous MRC weights; no FS/CE/CPE validity or abstention |

All five passed title gates and contain 15 standard fields, seven structured sections, communication parameters and experimental-completeness audits. Extraction evidence is in `projects/thesis-fso/worker-logs/step-3-dsp-outage-read-l1-l2.md`, `step-3-dsp-outage-read-l3-l4.md`, and `step-3-dsp-outage-read-l5-p0-boundary.md`.

## Competitor action matrix

| Method | Receiver-visible input | Trigger / action | Output | Coverage of current narrow action |
|---|---|---|---|---|
| Sun 2019 broad adaptive combining | abstract only: multiple coherent-FSO aperture signals | adaptive digital combining; exact weight/update/ordering unknown | combined signal | collision risk only; exact action unresolved without fulltext |
| Wang 2023 FSTS/MRC | shared-LO branch samples + FSTS | threshold FS/alignment → phase correction → MRC → pol-demux/FOE | aligned combined symbols + FO estimate | no validity weight/drop |
| Liu 2023 JLT 2N×2 | post-IQ/clock N×H/V streams | CMA/RDE SGD updates 4N FIRs and jointly equalizes/combines | two demultiplexed combined polarization streams | strongest estimator-changing alternative; no explicit admission/abstention |
| Johst 2024 | known-sequence DSP estimates + SNR/BER outcome | data-aided DSP; outage label; roughly `<-1 dB` hard discard recommendation | valid branch stream or outage marker | covers defect shape and hard comparator, not soft policy |
| Tu 2020 | ideal-time-aligned fields, OSNR, loss target | choose M; phase rotate; add only on positive net EGC gain | recursive EGC field | covers known-OSNR hard/conditional admission, not DSP validity |
| Yang 2022 ICCC | pilots, attenuation `alpha`, LS/MMSE `Hhat` | attenuation-derived continuous `gamma` modifies MRC | weighted MRC decision stream | covers generic pilot-derived soft weight in RF, not multi-source post-DSP validity |
| SC/GSC / fixed SNR discard | branch SNR/rank/threshold | select top/qualified branches | selected or combined stream | mandatory cheap comparators, not proposed contribution |

## Canonical problem list

### Q001 — branch-local-DSP validity-constrained combining

- **M**: Wang 2023's recent, actually evidenced ordering: per-branch FSTS frame synchronization/alignment and branch phase correction → MRC → shared polarization demultiplexing/FOE. Liu 2023 2N×2 CMA/RDE is the strongest estimator-changing alternative and must be reported beside it.
- **C**: at that pre-MRC boundary, coherent-FSO branches have heterogeneous received power and branch-local FS/phase-correction validity; some are near or beyond a local DSP-outage state while others remain usable.
- **A**: channel-amplitude/phase correction is not a validity test. Wang's MRC boundary has no admission variable and can give a nonzero contribution to a systematically invalid branch-local stream; Johst explicitly reports that outage branches can worsen combining and must be discarded. This is falsifiable: corrected MRC may show no harm, or fixed discard/SC/GSC may absorb all headroom.
- **Method output shape only**: receiver-visible branch-local synchronization/phase/available estimation validity → bounded branch reliability/abstention action → combined sequence plus no-valid-branch flag. No formula, state machine or feature fusion is authorized in Step 3.
- **Claim boundary**: the broader action after all independent FS/CE/CPE stages is not yet baseline-aligned by the five-paper set and remains a Step 3.5 question, not part of Q001's current four-criterion PASS.

| Glossary criterion | Result | Evidence |
|---|---|---|
| 1. specific M-C-A contradiction | PASS | Wang has no validity action at its branch-local pre-MRC boundary; Johst gives explicit invalid-branch harm/discard evidence |
| 2. reusable method output | PASS | bounded branch-local weight/admission output is deployable without changing transmitter |
| 3. recent task-matched baseline | PASS | Wang 2023 provides the exact branch-local-DSP→MRC ordering; Liu 2023 is the strongest estimator-changing competitor; Johst 2024 supplies hard discard |
| 4. quantitative comparison | PASS | paired BER/outage versus estimated-channel MRC, fixed SNR discard, SC/GSC and applicable Liu 2N×2; failure can terminate quickly |

## Collision and dead-end boundaries

- Broad “adaptive coherent-FSO combining” is already occupied by Sun 2019 and is not claimed.
- Pilot-amplitude soft weighting is already occupied by ICCC 2022 and is not claimed.
- Known-OSNR phase-window adaptation and positive-gain branch admission are already occupied by Tu 2020 and are not claimed.
- Joint raw-waveform adaptive equalization/combining is occupied by Liu 2023 and is not claimed.
- The surviving Q001 is the narrower branch-local-DSP validity-to-bounded-weight/abstention action at Wang's evidenced pre-MRC position. Exact novelty remains limited by missing Sun 2019 fulltext; the broader post-all-FS/CE/CPE position is also a Step 3.5 baseline debt, not a Step 3 claim.

## Experimental-completeness cross-check

| Paper | Main completeness strengths | Main limitations |
|---|---|---|
| Johst 2024 | 100 MC/condition + multi-day 3.15 km field data | no combining experiment, CI or task-matched DSP comparison |
| Wang 2023 | 6400 FS and 800 FOE trials; modulation/turbulence/branch sweeps | simulation only; no CI/seeds or runtime/hardware |
| Liu 2023 | simulation + offline hardware; 100 turbulence experiments | ATT-emulated rather than atmospheric path; no algorithm comparator matrix |
| Tu 2020 | analytic/MC agreement over OSNR/loss/branch cases | no hardware/field or alternative estimator |
| Yang 2022 | same-estimator MRC comparison and antenna sweep | unspecified MC volume; idealized Rayleigh/AWGN; qualitative complexity |

## Writing architectures

1. **Wang 2023**: training design → FS → FOE equations → operation counts → system simulation → FS/FOE/BER progression. Useful for modular receiver-method exposition.
2. **Liu 2023**: problem funnel → compact competitor paragraph → system/2N×2 equations → boundary figures → receiver sanity check → turbulence gain. Useful for separating mechanism from outcome.
3. **Johst 2024**: frame/DSP chain → controlled impairment simulation → field setup → outage distribution/boundary → bounded operational conclusion. Useful for defect-to-deployment evidence, while avoiding an untested method claim.

## Step 3 disposition

`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`, independently verified after bounded repair. This is a problem-survival result only: no Go/Kill, METHOD_SIGNAL, algorithm design or experimental evidence has been produced.

If verified, Step 3.5 search must target: `post-DSP branch reliability`, `lock-aware coherent combining`, `frame-sync confidence combining`, `channel-estimation residual MRC`, `cycle-slip metric branch admission`, `bounded/abstaining diversity combining`, plus primary retrieval of DOI `10.1016/j.optcom.2019.03.069`.
