# Step 051 — C1 finite phase-hypothesis Step 1 route search

> 2026-08-09 | T005 | action class: `GROUNDWORK_STEP1_SEARCH`
> task-control validator: `PASS`
> terminal: `C1_EXACT_COLLISION_FOUND`

## Scope and integrity

- 仅执行检索、AI 逐条标注、摘要/DOI/S2 交叉验证和 C1 route 判读。
- 未下载全文、未实现、未实验、未恢复 C3 独立卡、未修改 owner/source/artifact 或 `p05_run*.log`。
- `tools/search` 使用 `PYTHONDONTWRITEBYTECODE=1` 与任务书参数；聚合 enrichment、S2 429、OpenAlex timeout、arXiv 0、Exa 402 均按实际记录。
- 上一轮约 30 分钟，违反单任务 ≤15 分钟硬上限；收到提醒后停止搜索。本轮只用已有证据收口。

## Outputs

- 标注 JSON：`search-archive/2026-08-09/coded-decoder-c1-*.json`（8 files；28 annotated rows，19 unique）。
- route report：`projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c1-search-report.md`。
- 本 log：`projects/thesis-fso/worker-logs/step-051-c1-step1-search.md`。

## Gate receipt

| gate | observed | verdict |
|---|---:|---|
| R1 query groups | 3 contracted groups + short-term retries/fallback | PASS |
| R2 targeted groups | 2 | PASS |
| actual source families | ≥6 | PASS |
| annotations | 28/28 | PASS |
| direct-action abstract pointers | exact/strong claims have arXiv/S2/DOI/publisher pointer；unsupported timing explicitly marked | PASS WITH LIMITATION |
| unique candidates | 19/20 | FAIL |
| `必读` | 2/5 | FAIL |
| published ratio | 16/19 = 84.21% | PASS |

因此没有宣称 Step 1 总门 PASS。

## Scientific route verdict

The official abstract of arXiv:2511.21340 already implements the same generic action signature as C1: decoder extrinsic model evidence scores a finite symmetry-derived candidate set and selects the most likely candidate once after initialization. IEEE TSP 2006 `10.1109/TSP.2006.874844` independently establishes code-aided phase-ambiguity hypothesis testing as an older formal family. C1's novelty falsifier is therefore triggered even though matched FSO/BP/front-end/latency details remain unclosed.

## Anomalies for master review

1. Time-contract violation: ~30 min vs 15 min.
2. `tools/search` auto-created generic mirror archives and updated `search-archive/_index/all-papers.jsonl`, despite explicit C1 output naming; not manually reverted because the index is shared/concurrent.
3. Aggregate search has no global deadline across abstract enrichment; single-source search still suffered S2 rate limit/SerpAPI 74 s latency.
4. Candidate count and `必读` count are below gw-search quality thresholds; this route verdict must not be lifted into integrated Step 1 PASS.

## Terminal

`C1_EXACT_COLLISION_FOUND`
