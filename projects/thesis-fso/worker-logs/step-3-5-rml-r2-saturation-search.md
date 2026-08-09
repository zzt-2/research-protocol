# Step 3.5 RML-FSTS R2 新术语饱和检索

> Task: `.sessions/2026-08-08-rml-fsts-groundwork/T008-step3-5-r2-saturation-search.md`
> Date: 2026-08-09
> Boundary: 仅执行 4 个冻结 query、known/new 去重与 abstract/metadata 初筛；不做 exact-action 终判。

## R2 query execution

4/4 冻结 query 均实际启动。Q1–Q3 在 120 秒单 query 上限内完成；Q4 达到 120 秒上限后终止其 `bash/wsl` 子进程，且自动 raw 尚未落盘，因此以 error placeholder 记录。Q4 的 `0` 不是零命中，不能用于饱和结论。

| ID | frozen query | raw path | SHA256 | status | result count | actual result-level sources / errors |
|---|---|---|---|---|---:|---|
| Q1 | `single-tone training sequence FSO frequency offset estimation lag block length adaptive` | `search-archive/2026-08-09/rml-fsts-r2-q1.json` | `f05030837dee4f68c9c257b77a4e1f860e2f27ee7cc2019d51d252752c573107` | COMPLETE | 8 | `serpapi_scholar`；Exa keyword/neural 402；S2 abstract batch 400 |
| Q2 | `short symbol block training sequence coherent FSO frequency offset adaptive length selection` | `search-archive/2026-08-09/rml-fsts-r2-q2.json` | `439736e756bc631696efa8a871e2b283bed17162252a97b2c43a7c21b01ecc74` | COMPLETE | 25 | `serpapi_scholar`, `openalex`, `semantic_scholar`；Exa keyword/neural 402；S2 enrichment rate limit |
| Q3 | `low received optical power joint frame frequency synchronization lag window selection satellite optical` | `search-archive/2026-08-09/rml-fsts-r2-q3.json` | `b99d47943b9dd3d3a69785dab0ef3939b109f9713dd20eb1a69c67ab2d28651f` | COMPLETE | 30 | `serpapi_scholar`, `openalex`；Exa keyword/neural 402 |
| Q4 | `short-time spectrum coarse frequency offset FSO adaptive window correlation distance` | `search-archive/2026-08-09/rml-fsts-r2-q4.json` | `c960dd0f4d8bf2cfebc69012fd46c602da73a966564b8393c54379aa0b47425a` | TIMEOUT | N/A | 120 秒 bounded timeout；无自动 raw、无 retained source；placeholder 不代表零结果 |

已完成 raw 的 63 条记录保留逐结果 `source_api` provenance；实际 retained source family 合计为 SerpAPI、OpenAlex、Semantic Scholar 三类，满足“至少 2 类”的要求。

## Known guard

known guard 由以下冻结输入联合生成：Step 1 canonical ledger（121 unique）、R1 八候选、Step 3 五篇精读身份、T004/T005/T006/T007 receipts。规范化规则为 title 小写后移除非字母数字字符，DOI 小写；联合去重后得到 **128 个 title keys + 77 个 DOI keys**。

- title-key sorted-set SHA256：`acb52d811c8c7e0c0a6c46245e749502bbdc54eee99d175619f1f73f7dd9b09a`
- DOI-key sorted-set SHA256：`bd8d6b542b9b84b5cb9e438e2f744a267e6f73b20ea1aba19c4accda28e6ecda`
- Q1–Q3 共命中 known guard 15 次，对应 12 个 unique titles；其中 3 条同时有 DOI 命中。
- 已知命中覆盖 R1 的 2025 single-tone、2024 short-block、SSRN low-power joint FS/FOE、2024 short-time spectrum，以及 Step 1/3 的 Enhanced、Tang STSB、Yu joint-frame 等；均不计新增。

## New candidate screening

Q1–Q3 的 63 条结果减去 15 次 known 命中后，得到 **48 个 new unique titles**。按 T008 的窄门槛逐条检查 title + available abstract/snippet：

- `new_must = 0`
- `new_should = 0`
- `new_exclude = 48`

下表列出最接近任务的 10 条 new exclude；其余 38 条为更明显的跨域、通用综述、IM/DD timing、equalization/combining、adaptive modulation 或非 carrier-FOE 项，不进入候选表。

| # | new title | disposition | abstract/metadata-supported reason |
|---:|---|---|---|
| 1 | Two efficient blind carrier frequency offset estimation algorithms for APSK signals | EXCLUDE | 通用 APSK blind CFO；reliability weighting/aggregation length 是 estimator 内部复杂度权衡，不是 coherent-FSO receiver condition→lag/`B_L` selector。 |
| 2 | Spatio-temporal mutualism enabled ultrashort pulse coherent FSO transmission for turbulent resilience | EXCLUDE | coherent-FSO 相邻，但检索片段指向 ultrashort-pulse/AO 时空设计，未支持 carrier FOE lag/window selection。 |
| 3 | Frequency-domain 4N×2 MIMO adaptive equalizer for multi-aperture coherent digital combining FSO communication | EXCLUDE | adaptive equalization/combining；FO compensation 位于 combining 后，未支持目标 lag/`B_L` 动作。 |
| 4 | Training sequence design for frequency offset and frequency-selective channel estimation | EXCLUDE | 通用 2003 offline TS/CRB 设计，不是 coherent FSO，也没有 receiver-condition selector。 |
| 5 | Hybrid Time-Frequency Domain Frequency Offset Compensation Under GHz Doppler Shift for LEO Satellite-to-Ground Coherent Free-Space Optical Communication | EXCLUDE | title task-adjacent，但 raw abstract enrichment 明显错配为 OAM survey；可用 metadata 只支持 hybrid FO compensation，未支持 adaptive lag/window/cheap lookup，不足以升 must/should。 |
| 6 | High-capacity coherent FSO | EXCLUDE | 根据 abstract，动态动作是 transmitter symbol-rate + PCS，目标是 Doppler tolerance/throughput；不是 receiver FOE lag/window。 |
| 7 | Multi-aperture coherent digital combining based on complex-valued MIMO 2N×2 adaptive equalizer for FSO communication | EXCLUDE | CMA adaptive combining/equalization，处理 branch gain/phase/SOP；没有 FOE lag/`B_L` selector。 |
| 8 | Timing synchronization and channel estimation in free-space optical OOK communication systems | EXCLUDE | IM/DD OOK timing/channel estimation；sliding correlator 不等于 coherent carrier-FOE lag selector。 |
| 9 | Synchronization for variable data rate LEO direct-to-earth optical links | EXCLUDE | snippet 支持 variable-rate optical timing synchronization；未支持 coherent FOE 或 condition→lag/window action。 |
| 10 | Flexible phase synchronization for wireless optical coherent communication system with adaptive fractionally-spaced blind equalization | EXCLUDE | phase synchronization + adaptive equalization，不是 training-aided FOE lag/`B_L` selection。 |

所有排除均停留在 metadata/abstract claim ceiling；没有把 abstract 当全文，也没有据此裁决 exact collision。

## Convergence

最后一个**成功完成**的 query（Q3）新增 must/should 为 0；但 Q4 超时且没有可筛查 raw，因此本任务的最终状态为：

- `new_must/new_should = 0/0`
- `converged = false`
- reason：`Q4_TIMEOUT_PREVENTS_TERMINAL_SATURATION_CLAIM`

本 worker 不自跑 R3，也不重跑 Q4。是否授权一次 bounded Q4 retry 由主线根据完整 Step 3.5 债务决定。

## Boundaries

- 未下载全文，未调用 `tools/download` 或 PDF 转换。
- 未进入 Step 4a，未设计/实现方法，未做仿真、MVE、Go/Kill 或 novelty closure。
- 未修改 topic/current views、`papers/index.json`、p05 logs 或任何 `.pyc`。这些路径在任务开始时已有并发/既存 dirty 状态，本任务未写入。
- 本任务只新增 4 个指定 raw（Q4 为明确 timeout placeholder）、本 worker-log 与指定 receipt；`tools/search` 自身按既定行为维护 search archive/global search index，不构成 canonical `papers/index.json` 修改。
