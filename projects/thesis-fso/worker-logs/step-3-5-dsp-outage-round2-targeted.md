# Step 3.5 Round 2 targeted search

> Task: T015 | Date: 2026-08-11 | Evidence boundary: title / abstract / metadata only

## 1. Scope and query receipt

This worker executed the six contracted targeted query groups with repository `tools/search`. No paper was downloaded or read in full, and no Step 3.5 terminal was assigned.

```text
bash tools/search "<query>" --sources s2 openalex --mode academic \
  --max-per-source 20 --top 40 --year-from 2000 \
  --output search-archive/2026-08-11/step3-5-dsp-r2-qNN.json
```

| Query | Targeted action/scenario | Provider raw | JSON retained | Output |
|---|---|---:|---:|---|
| q01 | branch validity / lock-aware / synchronization confidence + optical MRC | 0 | 0 | `step3-5-dsp-r2-q01.json` |
| q02 | frame-sync confidence / phase validity / cycle-slip + branch admission | 0 | 0 | `step3-5-dsp-r2-q02.json` |
| q03 | abstaining / bounded / robust / invalid-branch MRC | 0 | 0 | `step3-5-dsp-r2-q03.json` |
| q04 | DSP/receiver outage + multi/distributed aperture coherent combining | 5 | 3 | `step3-5-dsp-r2-q04.json` |
| q05 | dynamic channel tracking + distributed-aperture MIMO + validity/selection | 1 | 1 | `step3-5-dsp-r2-q05.json` |
| q06 | aperture selection / phase-alignment error / modulus-normalized adaptive cost | 0 | 0 | `step3-5-dsp-r2-q06.json` |
| **Total** | six matrix cells | **6** | **4 unique** | **6/6 receipts** |

The tool attempted both S2 and OpenAlex for all six cells. In this round, OpenAlex was rate-limited and contributed no retained result; S2 contributed all four. A bounded Exa fallback (`q07`) returned zero because both modes reported exhausted credits. A later OpenAlex-only attempt was stopped during repeated rate-limit waits and is not counted as a completed query. Therefore Round 2 alone has one actual contributing source. The overall Step 3.5 search evidence still has two actual contributing sources because Round 1 recorded S2=17 and OpenAlex=28 unique retained results. This limitation is stated rather than relabeling a zero-result source as a contributor.

## 2. Per-result semantic screening

All four JSON-retained records were screened from title and available abstract, independent of the tool relevance score.

| Identity | Abstract-visible input | Trigger | Action | Output | Priority / reason |
|---|---|---|---|---|---|
| *Free-Space Optics Communications Employing Elliptical-Aperture Multimode Diversity Reception Under Anisotropic Turbulence*, JLT 2022, `10.1109/JLT.2021.3130250` | received modes / multi-aperture coherent signals | no receiver-visible validity trigger; experiment varies anisotropic turbulence | elliptical-aperture multimode reception plus digital coherent combining; exact branch weight/admission not stated | combined 30-Gbaud DP-QPSK and outage result | **REJECT** for Q001 collision: receiver architecture/turbulence mitigation, not validity-driven bounded weight/admission/abstention |
| *Performance analysis of coherent DPSK SIMO laser-based satellite-to-ground communication link...*, OQE 2023, `10.1007/s11082-023-04630-1` | modeled SIMO branch signals under Málaga turbulence | none | conventional MRC/EGC used for analysis | analytical/simulated BER, outage probability, ergodic capacity | **REJECT**: performance analysis and conventional comparator only; no DSP-validity input or branch admission |
| *Review of key vertical-cavity laser and modulator advances enabled by advanced MBE technology*, JVST 2021, `10.1116/6.0000574` | mixed review material; no task-matched branch input | none | no multi-aperture validity action | device/link review outputs | **REJECT**: abstract contamination / cross-topic false positive |
| *Dynamic channel tracking algorithm in satellite-to-ground distributed-aperture MIMO coherent digital combining system*, Optics Communications 2026, `10.1016/j.optcom.2025.132812` | **UNKNOWN** (`abstract=null`) | **UNKNOWN** | **UNKNOWN**; title alone cannot establish tracking update or branch action | **UNKNOWN** | Existing citation-chain **MUST**, not new. `UNRESOLVED_ACQUISITION_DEBT`; direct identity requires primary fulltext and is not promoted to collision from title |

No retained abstract shows the complete Q001 coupling:

```text
receiver-visible branch-local validity
  -> bounded reliability / admission / abstention
  -> combined sequence + no-valid flag
```

The one semantically direct identity is exactly the already-listed Qiu 2025 acquisition debt. The three remaining results add no action-level evidence.

## 3. De-duplication against Round 1 and citation shortlist

- Qiu 2025 (`10.1016/j.optcom.2025.132812`) is already one of T012's five MUST identities; it is not counted again.
- None of the other three retained records satisfies MUST or SHOULD for Q001 after semantic screening.
- Round 2 **new MUST = 0** and **new SHOULD = 0**.
- Existing unresolved acquisition/read debts from T012 remain unchanged; this round creates no new debt.

## 4. Round result

`ROUND2_SEARCH_CONVERGED`

This label means only that the last completed targeted search round added zero new MUST/SHOULD identities after de-duplication. It does not resolve the existing direct-paper acquisition debts, does not adjudicate exact-action collision, and is not a Step 3.5 terminal.
