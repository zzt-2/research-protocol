# V003 Final Audit — AMC GW Step1 Repair + Step2 Acquisition

> Independent verifier (fresh context). Worktree `rdl-method-production-v2` @ branch `codex/rdl-method-production-v2`. Recompute env `~/.venvs/torch/Scripts/python.exe`. No producer summary trusted; all numbers recomputed or re-read from disk.

## Verdict: PASS (10/12) + 2 PARTIAL

Substantive content is sound and reproducible. Two PARTIALs are governance/persistence gaps, not scientific errors: (a) R001's body was never edited to carry the D002 4→3 supersede inline, and (b) the receipt and papers were never force-added/committed (the receipt itself promises a force-add that was not executed). Neither affects the reproducibility of the search facts.

## Per-check

1. **[PASS]** — Phase A counts recomputable from raw JSON. Ran `python tools/amc_step1_recompute.py` (deterministic, no network). Output: 32 raw JSON / 17 unique queries / 16 nonzero / published 115+3 preprint+91 unknown = 209 unique / priority {必读10, 建议读17, 待确认4, 备选57, 排除121} / duplicate_query_groups 15. Every field matches `_step1_receipt.json` `search_facts` exactly. Result-bearing source union recomputed = {cnki, openalex, serpapi_scholar, openalex+openalex} — matches receipt's caveat that exa contributed digest items but no result-level tag.

2. **[PASS]** — dup-abstract groups fully recomputable. The recompute script's Phase A2 independently groups `_alldigest.json` by normalized abstract (len≥40) and prints exactly **6 groups / 18 items** (group sizes 7/3/2/2/2/2). L124 (group5, 6G-roadmap, with L005), L020/L038/L090 (group1, OWC-survey) all present. Matches receipt `duplicate_abstract_groups` verbatim.

3. **[PASS]** — L124 identity vs local mismatch both evidenced. Receipt `l124_identity_resolution.official_identity` = Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557 (publisher Optica, ISSN 1094-4087). `local_abstract_status = MISMATCHED (generic 6G-roadmap, shared with L005)`. Verification sources listed as Semantic Scholar Graph API + Crossref /works/10.1364/oe.595557 — both plausible standard scholarly APIs. Spot-check: `_alldigest.json` L124 abstract starts with "6G and beyond will fulfill the requirements of a fully connected world" — confirmed (python check returns `startswith('6G and beyond') = True`).

4. **[PARTIAL]** — R001/topic-index no longer claim 4 families or "0 confirmed". **topic-index.md is fully clean** (PASS for topic-index): L49–50 actively use `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`, A_MCS_POWER_CONTROL, B_HARQ_IR_RATE_ADAPTATION, C_COHERENT_TX_ADAPTATION_UNVERIFIED, and explicitly say "候选族从 4（F1-F4）修订为 3（A/B/C）" / "原 F4 不再算机制不同的第 4 族" (correct historical framing). **R001 is NOT clean** (FAIL for R001): R001 carries no D002 supersede banner anywhere; §2 SLA table L42 still lists "F1…F4…共 4 机制不同族 | PASS" as an active gate verdict, and §4 keeps live family headers `### F1 …`, `### F2 …`, `### F3 …`, `### F4 …` (L292/311/330/349) with family_id F1/F2/F3/F4 rows (L298/317/336/355) and "4 族机制真不同" (L373). topic-index L91 calls R001 "原始 F1-F4 候选问题族" and notes "candidate-family 计数已被 D002 修订", but R001 itself was never edited to reflect this, so an R001-only reader still sees 4 active families. Note: V002 check A3 claimed this PASS but only verified topic-index, not R001 body — V002 was over-optimistic here.

5. **[PASS]** — receipt hashes match disk. Recomputed SHA256 of 7 sampled `raw_file_hashes` entries + all 4 alias files (`coherent-fso-acm-modcod-satellite`, `optical-feeder-link-variable-rate-fec`, `fso-rate-compatible-ldpc-puncturing`, `satellite-optical-dvbs2x-acm`). All 11 MATCH. (e.g. alias `98bab8f18434…`, `1cf66fde5b41…`, `4fa6901cee51…`, `a408b9d0c593…`).

6. **[PASS]** — per-paper path/metadata/hash/content for 6 success papers. All 6 exist with `content.md` (≥50 non-blank lines: 226/208/242/338/245/132), a `source.pdf`, and a `metadata.json` with a success status. Note status field is inconsistent: L165/L023 = `"success"`, L096/L146/L075/L090 = `"ok"` — both denote success and content_quality=good; minor schema drift, not a failure. Title spot-check: L096 content.md L3 = "On the Design of FSO-Based Satellite Systems Using Incremental Redundancy Hybrid ARQ Protocols With…" (exact shortlist match); L023 content.md starts with author/copyright boilerplate but `metadata.title` carries the correct shortlist title. L146 metadata note records the Crossref-resolved DOI 10.1109/jiot.2025.3600439.

7. **[PASS]** — ≥5 quality-gate papers real. Counted 15 content.md with ≥50 non-blank lines repo-wide; the 6 AMC success papers (L165/L023/L096/L146/L075/L090) all qualify (132–338 lines). Threshold ≥5 MET.

8. **[PASS]** — stop-loss honored. `_step2_download_log.md` shows exactly 3 rounds (Round 1 `tools/download` → Round 2 OpenAlex/S2/Crossref → Round 3 `tools/blit --source ieee/cnki`). No WebReader/Scholar/ResearchGate scraping. Outcome: 6 success / 5 download-fail (L124 Optica bot-block, L126/L073 MDPI bot-block, L018 no OA, L020 identity-uncertain) / 2 manual_required (L050/L206 CNKI). All 7 metadata-only dirs exist on disk with `download_status=failed`/`manual_required` and detailed `failure_reason` (verified each metadata.json). No Round 4.

9. **[PASS]** — no Step 3 / full-read / method design / simulation / METHOD_SIGNAL / Go-NoGo. No `literature_notes*.md` exists in the AMC topic. All `METHOD_SIGNAL` occurrences are prohibitions ("不产生 METHOD_SIGNAL" in R001 L430, voice L11, topic-index L27, mission-log L11/L21, R002 L95, master-state "METHOD_SIGNAL=0" zero-state). All `Go/No-Go`/`Go/Kill` occurrences are prohibitions or "Step 1 无 Go/Kill" honest boundaries. All `过四判据` are "未过四判据" (candidate, not passed). Shortlist papers were identity + content-quality checked only, not fully read (no per-paper notes/summary produced).

10. **[PASS]** — 4 p05_run*.log unmodified & unstaged. `git status --porcelain projects/simulation/explore/cma-fade-divergence/` shows all 4 as `??`; `git diff --cached --name-only` on that path is empty (not staged).

11. **[PASS]** — YAML/JSON parseable. `yaml.safe_load(_registry.yaml)` OK (AMC topic found, status=active). `json.load` OK for `_step1_receipt.json`, `_manifest.json`, `_alldigest.json`, `_step2_shortlist.json`, and all 6 success `metadata.json`.

12. **[PARTIAL]** — `git diff --check` PASS, but path-scope/force-add promise UNMET. `git diff --check` and `git diff --cached --check` both exit 0 (only benign LF→CRLF autocrlf hints, no whitespace errors). However: (a) the entire Phase A repair + Phase B acquisition is **UNCOMMITTED** — last commit `007a7c4` is the original pre-D002 Step 1; decisions/topic-index/verifications/mission-log/voice/registry/master-state have unstaged edits, and H001/R002/S002/tools are untracked `??`. (b) `search-archive/` and `papers/` are gitignored (`.gitignore:3,5`); the receipt text explicitly promises "Force-added to git so a clean clone can reconstruct the search contract", but `git ls-files search-archive/2026-08-02/_step1_receipt.json` returns nothing — **the receipt was never `git add -f`-ed**. A clean clone cannot reconstruct the search contract, contradicting the receipt's stated purpose. All changed/added paths are within expected scope (no Skill/stages/source-code drift); the gap is persistence, not scope.

## Issues found

- **Issue 1 (PARTIAL, check 4)** — R001 body still actively presents 4 families (§2 L42 "4 机制不同族" PASS verdict; §4 live F1/F2/F3/F4 headers L292/311/330/349; "4 族机制真不同" L373) with NO D002 supersede banner. topic-index correctly carries A/B/C + CURRENT_SEARCH_DID_NOT_CONFIRM; R001 does not. V002 check A3 over-claimed PASS by only inspecting topic-index. **Fix**: add a D002 banner at R001 top and re-label §4 family headers "原 F1–F4（D002 合并为 A/B/C）".

- **Issue 2 (PARTIAL, check 12)** — All Phase A/B work is uncommitted; `_step1_receipt.json` (gitignored) was never force-added despite the receipt text promising it. A clean clone cannot rebuild the search contract. **Fix**: stage/commit the working-tree changes; `git add -f search-archive/2026-08-02/_step1_receipt.json`; decide policy on force-adding papers/ (currently fully gitignored, so the 6 acquired content.md are also clone-invisible).

- **Issue 3 (minor, checks 6/8)** — `metadata.json` `download_status` schema drift: `"success"` (L165/L023) vs `"ok"` (L096/L146/L075/L090). Both denote success; normalize if a downstream consumer key requires exact match.

## Notes

- All scientific/reproducibility claims in the receipt are independently verified correct (checks 1, 2, 3, 5, 7, 9, 10, 11 fully PASS; 6/8 substantively PASS). The receipt is a faithful, deterministic, network-free artifact.
- The two PARTIALs are documentation/persistence hygiene, not data-integrity failures. They are quick to close before commit: (1) edit R001 header + family-section banners, (2) `git add -f` the receipt and commit.
- V002 is otherwise reliable; its only blind spot was treating "R001 口径已被 D002 修订" (a topic-index assertion) as equivalent to "R001 body edited" — they are not the same.
