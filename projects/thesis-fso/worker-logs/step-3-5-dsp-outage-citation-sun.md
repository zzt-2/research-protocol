# Step 3.5 citation chain and Sun 2019 legal evidence

> Task: T012 | Date: 2026-08-11 | Scope: GW Step 3.5 citation/acquisition only

## 1. Scope and execution discipline

- Only citation-chain retrieval, title/abstract screening, Sun availability/acquisition receipts, and a targeted citation-context check in an already-existing later primary fulltext were performed.
- No newly acquired fulltext was read, no method was designed, no experiment was run, and no Step 3.5/Step 4a terminal was assigned.
- `MUST/SHOULD` below means next acquisition/fresh-reading priority, not method validity, novelty, Go/Kill, or terminal status.

## 2. Citation receipts and screening coverage

All commands used repository `tools/search`, `--top 100`, and the requested citation source/direction. Forward-chain publication-year checks found no impossible pre-anchor results. Wang `both` produced no S2-only item (`S2_ONLY=0`), so no result in that union needs the `UNVERIFIED_CITATION` label solely because of source provenance.

| Raw receipt | Direction/source | Results | Abstract present | Abstract missing |
|---|---|---:|---:|---:|
| `search-archive/2026-08-11/step3-5-dsp-cite-wang-forward.json` | Wang forward / both | 8 | 5 | 3 |
| `search-archive/2026-08-11/step3-5-dsp-cite-wang-backward.json` | Wang backward / OpenAlex | 30 | 26 | 4 |
| `search-archive/2026-08-11/step3-5-dsp-cite-liu-forward.json` | Liu forward / OpenAlex | 19 | 12 | 7 |
| `search-archive/2026-08-11/step3-5-dsp-cite-liu-backward.json` | Liu backward / OpenAlex | 19 | 14 | 5 |
| `search-archive/2026-08-11/step3-5-dsp-cite-johst-backward.json` | Johst backward / OpenAlex | 20 | 18 | 2 |
| `search-archive/2026-08-11/step3-5-dsp-cite-sun-forward.json` | Sun forward / OpenAlex | 14 | 11 | 3 |
| `search-archive/2026-08-11/step3-5-dsp-cite-sun-backward.json` | Sun backward / OpenAlex | 24 | 20 | 4 |

Aggregate: **134 chain records, 121 unique DOI/title identities, 106 abstracts present, 28 abstract-missing records**. Every available abstract was screened. Abstract-missing records were not assigned an exact action from title wording; direct identities are retained as acquisition debts where warranted.

Known items rediscovered but not counted as new: Geisler 2016 foundational digital MRC, OE.448956 branch block phase correction, Ju 2024 real-valued MIMO combining (`10.1364/OL.511941`), and Johst OFC 2024 X-MRC/SDC (`10.1364/OFC.2024.W2A.31`).

## 3. New MUST/SHOULD shortlist (current Q001 topic)

| Priority | Identity and chain | Abstract-supported fact | Qualified local fulltext | Provisional action signature | Relative Q001 category |
|---|---|---|---|---|---|
| **MUST** | Xie et al., *Performance investigation of multi-aperture digital combining algorithm for satellite-to-ground coherent optical communication*, Optics Communications 2023, `10.1016/j.optcom.2023.129722`; Liu forward | `ABSTRACT_MISSING`; no exact action inferred | No | `UNKNOWN_PENDING_PRIMARY` | Direct multi-aperture combining identity; must close before collision judgment |
| **MUST** | Chen et al., *Frequency-domain 4N×2 MIMO adaptive equalizer for multi-aperture coherent digital combining FSO communication*, Optics & Laser Technology 2025, `10.1016/j.optlastec.2025.113235`; Liu forward | `ABSTRACT_MISSING`; no exact action inferred | No (canonical metadata says `failed/all_failed`) | `UNKNOWN_PENDING_PRIMARY` | Newer direct estimator-changing/combining competitor |
| **MUST** | Qiu et al., *Dynamic channel tracking algorithm in satellite-to-ground distributed-aperture MIMO coherent digital combining system*, Optics Communications 2025, `10.1016/j.optcom.2025.132812`; Liu forward | `ABSTRACT_MISSING`; no exact action inferred | No | `UNKNOWN_PENDING_PRIMARY` | Direct dynamic distributed-aperture competitor; highest semantic collision risk from identity only |
| **MUST** | Li et al., *Multi-aperture 4N×2 MIMO adaptive coherent digital combining with non-circular symmetric CMA algorithm in FSO communication system*, Optics Communications 2026, `10.1016/j.optcom.2026.133153`; Liu forward | `ABSTRACT_MISSING`; no exact action inferred | No | `UNKNOWN_PENDING_PRIMARY` | Direct adaptive equalizer/combiner; likely estimator-changing class, exact boundary unknown |
| **MUST** | Zhang, Tan, Ma, *Flexible Phase Synchronization ... Adaptive Fractionally-Spaced Blind Equalization Combined With Adaptive Kalman Filter*, IEEE Photonics Journal 2023, `10.1109/JPHOT.2023.3328423`; Sun forward | Abstract: adaptive fractionally-spaced blind equalization + adaptive KF jointly mitigate amplitude/phase noise and combine spatial diversity; 1–2 dB over EGC+VVPE | **Yes**, existing `papers/downloads/2026-07-08/10301506.md` (identity at file start) | Four-aperture FSE-MCMA+DD → MEKF/AKF, estimator-changing rather than post-DSP reliability admission | Direct fulltext neighbor plus later-primary Sun evidence carrier |
| **SHOULD** | Liu, Wang, Chen, *Robust multifunctional single-tone training sequence...*, Optics Express 2025, `10.1364/OE.561252`; Wang/Liu forward | Abstract: one training sequence performs FOE and branch phase correction before diversity combining under strong turbulence | No | Training-sequence FOE + pre-combining branch phase correction | Architecture/boundary neighbor; abstract shows no validity-triggered admission |
| **SHOULD** | Bian et al., *Low-complexity parallel real-valued weight adaptive digital combining...modes diversity reception*, Optics Communications 2020, `10.1016/j.optcom.2020.126078`; Sun forward | `ABSTRACT_MISSING`; no exact action inferred | No | `UNKNOWN_PENDING_PRIMARY` | Cross-mechanism adaptive-weight neighbor (mode diversity, not yet multi-aperture Q001) |
| **SHOULD** | Xiang, Lyu, *Statistical Model of Combining Efficiency for Digital Phase Alignment in Multi-Aperture...*, ICECE 2021, `10.1109/ICECE54449.2021.9674283`; Sun forward | Abstract derives combining-efficiency statistics under per-aperture phase-alignment error and compares EGC with/without aperture selection | No | Statistical model + aperture-selection comparison; selection rule not disclosed | Phase-alignment reliability/hard-selection neighbor |
| **SHOULD** | Yiannopoulos et al., *Optimal Combining for Optical Wireless Systems With Amplification: the chi-square Noise Regime*, IEEE PTL 2017, `10.1109/LPT.2017.2777908`; Sun backward | Abstract: optimal branch gain depends on branch energy until beating noise becomes detrimental; outperforms MRC/EGC by <1 dB in stated implementations | No | Energy/noise-regime-dependent optimal weights | Theoretical soft-weight comparator; impairment differs from DSP-outage |
| **SHOULD** | Chen et al., *A shared local oscillator spatial diversity PM-CO-OFDM system based on group timing synchronization and diversity branch phase correction...*, Optics Communications 2020, `10.1016/j.optcom.2020.126468`; Wang/Liu backward | `ABSTRACT_MISSING`; no exact action inferred | No | `UNKNOWN_PENDING_PRIMARY` | Defines the synchronization/phase-correction-before-combining boundary; no validity action proven |

New priority count: **5 MUST + 5 SHOULD = 10**. None is promoted to an exact Q001 collision on citation metadata/abstract alone.

## 4. Sun 2019 availability and legal acquisition receipt

### 4.1 Actual availability

- Worktree path `papers/doi/10.1016_j.optcom.2019.03.069/` contains only `metadata.json`; no `source.pdf`, `source.html`, or `content.md`.
- Metadata after the current legal attempt: `download_status=failed`, `download_method=all_failed`, empty `content_file`, timestamp `2026-08-11T22:00:26.442139+08:00`.
- Canonical/shared root `D:/code/study/research-protocol/papers/doi/10.1016_j.optcom.2019.03.069/` does not exist. Repository-wide DOI search found no Sun primary fulltext; the only paper fulltext carrying the DOI is a later citing paper, `papers/downloads/2026-07-08/10301506.md`.
- Therefore Sun primary availability is **FULLTEXT_UNAVAILABLE_AFTER_CURRENT_LEGAL_ATTEMPT**. This is an evidence limitation, not by itself a terminal/blocker judgment.

### 4.2 Acquisition commands and receipts

1. Repository wrapper dry-run:
   - Command: `bash tools/download --doi 10.1016/j.optcom.2019.03.069 --dry-run`
   - Result: failed before network because CRLF was interpreted as `$'\r'`; syntax error at wrapper `elif`.
2. Same repository backend, documented wrapper target (`tools/paper_download.py`), dry-run:
   - Result: planned the DOI target directory successfully.
3. Same backend, one actual DOI/OA acquisition attempt:
   - Result: `[FAIL] all_failed`; metadata updated as above.

No ResearchGate, Google Scholar, webReader, access-control bypass, or non-repository downloader was used.

## 5. Sun confirmed/unknown boundary and later-primary evidence

### Confirmed from Sun metadata/abstract

- Identity: J. Sun, P. Huang, Z. Yao, J. Guo, *Adaptive digital combining for coherent free space optical communications with spatial diversity reception*, Optics Communications 444 (2019) 32–38, DOI `10.1016/j.optcom.2019.03.069`.
- Four-aperture coherent FSO receiver, BPSK/QPSK, adaptive digital combining compared with traditional EGC.
- Motivation is avoiding time-consuming estimation of random/time-varying channel fading; abstract reports 3–10 dB required-transmit-power reduction versus EGC at the same BER under different turbulence conditions.

### Later-primary evidence (targeted citation context, not a substitute for Sun fulltext)

Zhang et al. 2023 is a later primary algorithm paper that cites Sun as reference [28]. In the existing fulltext at `papers/downloads/2026-07-08/10301506.md:129`, it explicitly states that Sun eases a time-varying channel by **dividing input signals by their modulus in the cost function**, with added derivative-computation complexity. This supports one bounded Sun action fragment:

`received/input signal -> modulus normalization inside adaptive cost -> weight adaptation under time-varying channel`

It does **not** establish Sun's exact tap/weight update equation, update order, branch-local input set, lock/outage trigger, clipping/abstention behavior, output contract, or no-valid-branch behavior. Zhang's own four-aperture `FSE-MCMA+DD -> MEKF/AKF` chain must not be projected backward onto Sun.

### Still unknown

- Exact per-branch input and whether any FS/CE/CPE validity statistic is used.
- Exact weight formula/update recursion, normalization order, temporal window, convergence/trigger condition, and whether weights can be zeroed/frozen.
- Whether combining happens before or after the same branch-local DSP boundary as Q001.
- Any abstention/no-valid-branch output or explicit DSP-outage action.

Sun exact action therefore remains **UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE**, narrowed by the later-primary modulus-normalized-cost fragment. No terminal judgment is made here.

## 6. Handoff facts

- Citation scale: **134 raw / 121 unique**, with seven requested raw receipts saved.
- Sun availability: no qualified primary fulltext; legal backend attempt returned `all_failed`; one later-primary citation context narrows, but does not close, its adaptive action.
- New current-topic priority: **5 MUST / 5 SHOULD**.
- Authorized next consumer action is fresh acquisition/reading and unified exact-action adjudication by the main thread; this worker log does not perform it.
