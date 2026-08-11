# Step 068 — C1 Step 3.5 前后向引文链

> 日期：2026-08-09  
> 任务：T022 / CP009 / epoch 9  
> terminal：`CITATION_CHAIN_COMPLETE`  
> 范围：仅 abstract/citation-chain analysis；未下载或精读新全文，未改中央 owner/治理/代码，未实验、提交或 push。

## 1. Task-control 与边界

`python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T022-c1-step3_5-citation-chain.md` fresh 输出 `PASS`。`CITATION_CHAIN_ANALYSIS` 在 CP009 allowed actions 内；adapter、defect smoke、MVE、Contract/Execute、experiment 与 thesis claim 保持冻结。

执行前已读取 `gw-supplement.md`、`tools-guide.md` §1–2、topic-index、D008、`literature_notes_coded_decoder_feedback.md`、L02/L05 read notes 与 mission-log。所有判断以 Q1 八字段完整链为筛选合同；摘要不承担 exact collision。

## 2. Seed 选择证据

| 候选 | S2 paper ID | citation count | reference count | 同源可比 |
|---|---|---:|---:|---|
| L02 / TSP 2006 | `c72b0dc7f9172850fbd356cd02d58a3902b0e4fb` | 37 | 42 | 是 |
| L05 / TWC 2004 | `1479f3d6ed7acace12e7e0c0f1ab475207d07874` | **58** | 22 | 是 |

选择 **L05**。两计数来自同一 S2 paper endpoint 和同一字段，故没有触发“不可比/并列时选 finite-hypothesis L02”的 fallback。receipt：`coded-decoder-c1-step3_5-citation-seed-counts.json`。

## 3. Forward / backward receipts

| 方向/来源 | 返回 | 有 abstract | 结果 |
|---|---:|---:|---|
| forward / S2 citations | 58 | 11 | 5 个技术相关 DOI 的 Crossref references 均独立命中 seed DOI；其余 S2-only 边不作为引用事实承重 |
| backward / S2 references | 21 | 1 | 唯一有摘要者是 2002 turbo-coded QPSK APPA predecessor |
| backward / OpenAlex fallback | — | — | `RATE_LIMITED`，daily budget 0、retryAfter≈32943 s；保留失败 receipt，未等待/重试 |
| backward / Crossref supplement | 5 direct predecessor titles | 0 | 补出 4 个 DOI；Lottici–Luise proceedings identity 未解析；Crossref 均无摘要 |

有摘要总筛查=`11 forward + 1 backward = 12`，两方向均非空。raw/structured receipts：

- `search-archive/2026-08-09/coded-decoder-c1-step3_5-citation-forward-s2.json`
- `search-archive/2026-08-09/coded-decoder-c1-step3_5-citation-backward-crosscheck.json`
- `search-archive/2026-08-09/coded-decoder-c1-step3_5-citation-screening.json`

## 4. ≥10 abstract screening

| # | dir | 论文 / abstract pointer | 摘要支持的动作 | disposition |
|---:|---|---|---|---|
| 1 | F | ACCESS 2026, DOI `10.1109/ACCESS.2026.3653159`; S2 `432824...` | LDPC PDM→global phase/frequency gradient ICS + hybrid ambiguity/Costas | `KNOWN_UNRESOLVED_FULLTEXT_DEBT`（U02） |
| 2 | F | TCOM, DOI `10.1109/TCOMM.2015.2506553`, arXiv `1306.3693`; S2 `c87a7e...` | bounded-order Tikhonov-mixture SPA 做 dynamic phase-noise tracking + joint decoding | **`NEW_SHOULD_FULLTEXT`** |
| 3 | F | TVT 2024, DOI `10.1109/TVT.2024.3383891`; S2 `bd0bd9...` | wide-range global CFO estimator + EM embedded decoder | `STRONG_NEIGHBOR` |
| 4 | F | ICECAI 2023, DOI `10.1109/ICECAI58670.2023.10176829`; S2 `7b0919...` | rough CFO + posterior-aided global EM fine estimator | `NEIGHBOR` |
| 5 | F | FCN 2025, DOI `10.1109/FCN66513.2025.11296777`; S2 `8f2fa7...` | WNSSP soft belief→parallel global phase compensation/joint reconstruction | `KNOWN_STRONG_NEIGHBOR` |
| 6 | F | JCIS 2005, DOI `10.14209/jcis.2005.22`; S2 `780099...` | decoder LLR→iterative symbol-timing APPA | `NOT_COMPARABLE_TIMING` |
| 7 | B | *A Novel Carrier Phase Recovery...QPSK*; S2 `326d70...` | turbo extrinsic→whole-block ML phase；four global ambiguity branches | `HISTORICAL_CORE_PREDECESSOR` |
| 8 | F | TSP 2009, DOI `10.1109/TSP.2009.2021452`; S2 `64f060...` | two-PLL fixed-interval dynamic phase smoother | `CONVENTIONAL_DYNAMIC_BASELINE`；decoder interaction absent |
| 9 | F | EURASIP 2013, DOI `10.1186/1687-1499-2013-1`; S2 `46f3ef...` | transmitter power/phase coordination | `NOT_COMPARABLE` |
| 10 | F | OCEANS 2025, DOI `10.23919/OCEANS59106.2025.11244949`; S2 `59b616...` | underwater OCDM cross-domain equalization | `NOT_COMPARABLE` |
| 11 | F | MILCOM 2021, DOI `10.1109/MILCOM52596.2021.9652967`; S2 `37c17d...` | anti-jamming DSSS + rotated constellation | `NOT_COMPARABLE` |
| 12 | F | FHSS 2015, DOI `10.7251/els1519003s`; S2 `ca37f8...` | DDS/Costas hardware acquisition | `NOT_COMPARABLE` |

摘要筛选结果：`new MUST=0`，`new SHOULD=1`。ACCESS 2026 是既有 U02 全文债，不重复计为新增。没有 abstract 同时声称 `local boundary + bounded segment/suffix action + decoder interaction`，故没有 `MUST_FULLTEXT` 或 exact-chain candidate。

## 5. Shortlist 八字段（≤10）

`U=摘要未说明，必须全文才可裁`。

| 候选 | input | trigger | localization | action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|---|
| ACCESS 2026（known U02） | LDPC PDM + samples | fixed iterative | global phase/CFO | gradient ICS + Costas | few LDPC iterations feedback | two-stage ambiguity hybrid；failure branch U | moderate increment，数值 U | global phase/CFO + bits |
| **TCOM 2015 Tikhonov** | samples + coded SPA messages | fixed joint tracking | per-symbol/dynamic phase posterior；boundary U | Tikhonov-mixture message update/reduction | joint SPA decode/estimate | mixture reduction，不是 failure fallback | bounded mixture order；runtime U | phase trajectory posterior + bits |
| TVT 2024 CFO | coded samples/posterior | fixed EM | whole-signal CFO | global frequency update | iterative embedded decoder | acquisition/fine framework；failure U | moderate，数值 U | CFO + decoded bits |
| ICECAI 2023 | samples + LDPC posterior | rough→fine fixed flow | global residual CFO | EM analytic update | iterative posterior feedback | rough stage；failure U | reduced cost function，数值 U | global CFO + bits |
| FCN 2025 | soft LDPC/WNSSP | fixed joint graph | global residual phase | parallel phase compensation | joint iterative reconstruction | U | U | global phase + bits |
| QPSK 2002 predecessor | extrinsic LLR | fixed outer iteration | whole block | ML phase; 4 global branches | turbo iterative | four-branch ambiguity handling | LUT + four chains；数值 U | global phase + bits |
| TSP 2009 smoother | BPSK samples | fixed smoother | dynamic phase trajectory | forward/backward PLL smoothing | abstract未说明 | none stated | two low-complexity PLLs | smoothed phase |
| JCIS 2005 timing | decoder LLR | fixed outer iteration | global/fixed timing | APPA timing estimate | turbo iterative | no acquisition；failure U | U | timing + bits |

最强新候选是 **TCOM 2015 / arXiv 1306.3693**：它是唯一把 dynamic phase trajectory、mixture ambiguity 与 joint decoding 同时放进摘要的方法，因此升为 `NEW_SHOULD_FULLTEXT`；但摘要不支持 boundary、bounded segment/suffix re-decoding、clean no-op 或 B1/B2 fallback，不能标 MUST 或 exact collision。

## 6. 未解析身份、全文债与下一轮 terms

- 新全文债：`10.1109/TCOMM.2015.2506553` / arXiv `1306.3693`（SHOULD）。本任务按合同不下载全文。
- 既有债：ACCESS 2026 DOI `10.1109/ACCESS.2026.3653159`（U02）仍 `UNRESOLVED_FULLTEXT`；本轮只确认其摘要与 Crossref citation edge。
- backward debt：Lottici–Luise 2002 proceedings DOI 未由 Crossref 正确解析；Morlet/Langlais/Mielczarek/Oh–Cheun DOI 已补但无 abstract。
- OpenAlex 当日限额失败已 fail-closed；无需等待。S2-only unrelated rows不用于方法断言。
- 下一轮定向 terms：`Tikhonov mixture cycle slip recovery LDPC`; `phase trajectory ambiguity branch loss decoder`; `joint phase-noise decoding local change point`; `bounded re-decoding after phase slip`。

## 7. 保护与 terminal

- 只新增四个 `search-archive/2026-08-09/coded-decoder-c1-step3_5-citation-*.json` receipts 与本 worker log。
- 未修改 literature owner、topic-index、D008、mission-log、master-state、registry、代码或 p05；未 stage/commit/push。
- `terminal=CITATION_CHAIN_COMPLETE`；`exact_chain_candidate_found=false`；`new MUST=0`；`new SHOULD=1`。
