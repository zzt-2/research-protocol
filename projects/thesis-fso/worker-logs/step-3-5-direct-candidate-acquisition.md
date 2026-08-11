# Step 3.5 direct-candidate acquisition receipt

> Task: T013 | Date: 2026-08-11 | Scope: asset/acquisition/quality gate only | Timebox: 15 min

## 1. Boundary and environment

- Read `T013-step3-5-direct-candidate-acquisition.md` and `stages/gw-acquire.md` before acquisition.
- The prescribed Python imports (`requests`, `pymupdf`, `pymupdf4llm`, `serpapi`, `tavily`) were available.
- The `tools/download` Bash wrapper is CRLF-broken in this worktree. The documented backend target, `~/.venvs/torch/bin/python tools/paper_download.py`, was therefore used without modifying the wrapper.
- Repository and shared-root asset checks found no qualified primary fulltext for any of the nine candidates. The shared root held only metadata for `10.1016/j.optlastec.2025.113235`; no `source.pdf` or `content.md` was present.
- No method fulltext was read and no exact-action/collision judgment was made.

## 2. MUST candidates

All four passed a backend dry-run, then received one legal DOI/OA/Unpaywall acquisition attempt. Every attempt returned `[FAIL] all_failed`; therefore source SHA/bytes/content lines are `N/A / 0 / 0`, and `qualified=false`.

| Title | DOI | Result | Source provenance and path | Source SHA256 / bytes / effective lines | Qualified | Failure receipt / limitation |
|---|---|---|---|---|---|---|
| *Performance investigation of multi-aperture digital combining algorithm for satellite-to-ground coherent optical communication* | `10.1016/j.optcom.2023.129722` | failed; metadata newly written | legal repository DOI/OA/Unpaywall backend; no source file; metadata `papers/doi/10.1016_j.optcom.2023.129722/metadata.json` | source `N/A / 0 / 0`; metadata SHA256 `06006a1352859dc05d1f74bd9e07a82537a74f102fb3cc853a9f6e276a607c72`, 406 B | false | Round 1 `all_failed`; Round 2 exact-title arXiv query timed out after 124 s and emitted no receipt/result. Primary action remains unavailable. |
| *Frequency-domain 4N×2 MIMO adaptive equalizer for multi-aperture coherent digital combining FSO communication* | `10.1016/j.optlastec.2025.113235` | failed; metadata refreshed | legal repository DOI/OA/Unpaywall backend; no source file; metadata `papers/doi/10.1016_j.optlastec.2025.113235/metadata.json` | source `N/A / 0 / 0`; metadata SHA256 `d2e32f79da610b9788e2619b496b8493e29c3dd50a387201ee804f5875dcd080`, 412 B | false | Round 1 `all_failed`; queued arXiv query did not start before the preceding query timeout. Primary action remains unavailable. |
| *Dynamic channel tracking algorithm in satellite-to-ground distributed-aperture MIMO coherent digital combining system* | `10.1016/j.optcom.2025.132812` | failed; metadata newly written | legal repository DOI/OA/Unpaywall backend; no source file; metadata `papers/doi/10.1016_j.optcom.2025.132812/metadata.json` | source `N/A / 0 / 0`; metadata SHA256 `60b295cb9e65bae953e694d8b48dca996eb6aa54fc2da5af2595ed6392a86f3a`, 406 B | false | Round 1 `all_failed`; queued arXiv query did not start before the preceding query timeout. Primary action remains unavailable. |
| *Multi-aperture 4N×2 MIMO adaptive coherent digital combining with non-circular symmetric CMA algorithm in FSO communication system* | `10.1016/j.optcom.2026.133153` | failed; metadata newly written | legal repository DOI/OA/Unpaywall backend; no source file; metadata `papers/doi/10.1016_j.optcom.2026.133153/metadata.json` | source `N/A / 0 / 0`; metadata SHA256 `8d24d25780189fb3fc5855ea96234a36e2a03e03da3f4115416e3ef7e80df974`, 406 B | false | Round 1 `all_failed`; queued arXiv query did not start before the preceding query timeout. Primary action remains unavailable. |

## 3. SHOULD candidates

Timebox priority was the four MUST papers. The five SHOULD papers received repository/shared-root asset checks and backend dry-runs only; no actual download round was started. All remain source-absent, with source SHA/bytes/effective lines `N/A / 0 / 0` and `qualified=false`.

| Title | DOI | Existing / new / failed | Provenance/path | Qualified | Limitation |
|---|---|---|---|---|---|
| *Robust multifunctional single-tone training sequence for multi-aperture coherent optical receivers* | `10.1364/OE.561252` | no existing fulltext; actual acquisition not started | dry-run target `papers/doi/10.1364_oe.561252/` | false | deferred at 15-min MUST-first stop |
| *Statistical Model of Combining Efficiency for Digital Phase Alignment in Multi-Aperture ...* | `10.1109/ICECE54449.2021.9674283` | no existing fulltext; actual acquisition not started | dry-run target `papers/doi/10.1109_icece54449.2021.9674283/` | false | deferred at 15-min MUST-first stop; IEEE blit round not reached |
| *Low-complexity parallel real-valued weight adaptive digital combining ... modes diversity reception* | `10.1016/j.optcom.2020.126078` | no existing fulltext; actual acquisition not started | dry-run target `papers/doi/10.1016_j.optcom.2020.126078/` | false | deferred at 15-min MUST-first stop |
| *A shared local oscillator spatial diversity PM-CO-OFDM system based on group timing synchronization and diversity branch phase correction ...* | `10.1016/j.optcom.2020.126468` | no existing fulltext; actual acquisition not started | dry-run target `papers/doi/10.1016_j.optcom.2020.126468/` | false | deferred at 15-min MUST-first stop |
| *Optimal Combining for Optical Wireless Systems With Amplification: the chi-square Noise Regime* | `10.1109/LPT.2017.2777908` | no existing fulltext; actual acquisition not started | dry-run target `papers/doi/10.1109_lpt.2017.2777908/` | false | deferred at 15-min MUST-first stop; IEEE blit round not reached |

## 4. Coverage result

- Qualified new fulltexts: **0/9**.
- MUST primary fulltexts: **0/4 available** after asset check and the first legal acquisition round.
- The one attempted arXiv fallback query produced no result before timeout; the remaining arXiv/IEEE fallback rounds were intentionally not expanded past the task timebox.
- These are acquisition limitations only. They do not establish an exact collision, non-collision, Step 3.5 terminal, or Step 4a entry.
