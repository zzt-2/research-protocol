# Step 080 — C1 Step 3.5 convergence round 3（final cap）

> 2026-08-10 | T034 / CP009 / epoch 9 | `ROUND3_CAP_REACHED_WITH_NEW`

## 1. 范围与证据边界

- 本 salvage 只读取已落盘的 `coded-decoder-c1-step3_5-convergence-r3-*` receipts 并离线复算；没有新网络、搜索、下载或全文获取。
- 没有修改中央 owner、治理、代码或 `pyc`，没有提交/push，也没有触碰四个受保护 `p05` 日志。
- 前一执行 agent 超时，记为操作债；其聊天回报未作为计数或候选裁决依据。

## 2. 八组 query / source receipts

| ID | requested query | Crossref receipt | arXiv effective submitted query | arXiv count |
|---|---|---:|---|---:|
| q01 | `"Gilbert-Elliott" "bursty differential phase noise" LDPC local repair` | `q01-crossref.json`: 10 | `all:"bursty phase noise" AND all:LDPC AND all:"channel estimation"` | 1 |
| q02 | `"windowed BCJR" "channel-state estimation" LDPC phase boundary` | `q02-crossref.json`: 10 | `all:"windowed BCJR" AND all:"channel state" AND all:LDPC` | 0 |
| q03 | `"burst-aware" LDPC "channel estimation" segment reprocessing` | `q03-crossref.json`: 10 | `all:"burst-aware" AND all:LDPC AND all:"channel estimation"` | 1 |
| q04 | `"decoder LLR" "channel-state posterior" cycle slip localization` | `q04-crossref.json`: 10 | `all:"decoder LLR" AND all:"channel state" AND all:"cycle slip"` | 0 |
| q05 | `"hybrid turbo differential decoding" cycle slip localization repair` | `q05-crossref.json`: 10 | `all:"hybrid turbo differential decoding" AND all:"cycle slip"` | 0 |
| q06 | `"differential encoding aware" soft-decision FEC cycle slip correction` | `q06-crossref.json`: 10 | `all:"differential encoding" AND all:"soft decision FEC" AND all:"cycle slip"` | 0 |
| q07 | `syndrome parity-check cycle-slip boundary suffix re-decode` | `q07-crossref.json`: 10 | `all:syndrome AND all:"parity check" AND all:"cycle slip"` | 0 |
| q08 | `decoder-aided phase-slip change-point bounded local phase hypotheses` | `q08-crossref.json`: 10 | `all:"decoder aided" AND all:"phase slip" AND all:"change point"` | 0 |

Crossref receipts 不回显 submitted query，表中该列忠实记录 T034 requested string；每组 receipt 均为成功结构化响应、10 items。arXiv 采用 source-syntax contraction，完整记录在 `...r3-arxiv-effective.json`；q01 早期 exact-string receipt 为 0，effective q01/q03 各召回同一已知 `arXiv:2604.07004`。有效来源为 Crossref + arXiv。S2/OpenAlex exact calls 只作 OFC 2017 身份/摘要交叉核验，不计 raw。

## 3. 离线复算计数

| count | value | 复算口径 |
|---|---:|---|
| raw | **82** | Crossref `8×10=80` + arXiv `1+1=2` |
| identity unique | **79** | DOI 优先；否则去版本 arXiv id；否则 normalized title |
| known / family merged | **7** | T033 已读身份及 HTDD/layered-LDPC 已知谱系合并 |
| metadata-new unique | **72** | `79−7` |
| actionable new MUST / SHOULD | **0 / 1** | 八字段摘要门控 |

三个去重减项均可从 receipts 复现：`arXiv:2604.07004` 在 q01/q03 重复；DOI `10.1109/APCC.2006.255801` 与 `10.1109/LCOMM.2010.091710.101062` 均在 q02/q03 重复。另一个“同题名、不同 DOI”的 1993 RLS 记录按 DOI 规则保留为两个身份，故 unique 是 79 而不是 78。

7 个 known/family：`arXiv:2604.07004`；`10.1109/ECOC.2014.6964037`；`10.1109/ECOC.2015.7341656`；`10.1364/ECEOC.2012.MO.1.A.5`；`10.1109/ICTON.2016.7550341`；`10.1109/SPA.2015.7365145`；`10.1364/OFC.2015.TU3B.2`。其余 72 个 metadata-new 中，71 个为普通编码/估计、全局 FEC、异域 slip 或词义假阳性，未命中 actionable 门控。

## 4. 唯一 actionable new：OFC 2017（fail-closed）

身份：T. Koike-Akino et al., *Fully-Parallel Soft-Decision Cycle Slip Recovery*, DOI `10.1364/OFC.2017.W2A.56`，`SHOULD_FULLTEXT`。

Optica publisher abstract（`...r3-ofc2017-abstract.json`）只支持：**pilots 上 soft-decision slip-state estimation + parallel recovery**；并报告 frequent cycle slips / strong phase noise 下 0.6 dB gain。Crossref 与 S2 身份一致但 abstract null；OpenAlex exact receipt 为 HTTP 429。

| receiver-visible input | trigger | localization | candidate action | decoder interaction | fallback | complexity/latency | output |
|---|---|---|---|---|---|---|---|
| pilots；soft-decision 来源 `UNKNOWN` | `UNKNOWN` | pilot-position slip state；explicit boundary/segment `UNKNOWN` | parallel recovery；候选/区间/有界数 `UNKNOWN` | “soft-decision”可证；decoder feedback/re-evaluation `UNKNOWN` | `UNKNOWN` | parallel 可证；候选数/decode calls/latency `UNKNOWN` | MI 与 0.6 dB 可证；repair object/corrected samples `UNKNOWN` |

裁决：身份新、摘要直接邻接 slip-state estimation/recovery，故 `SHOULD_FULLTEXT`；但摘要不支持 explicit boundary、decoder re-evaluation、bounded local carrier action、fallback 或明确 repair output。`collision=UNKNOWN_FAIL_CLOSED_NOT_EXACT_COMPLETE_CHAIN`，不得按题名晋为 MUST 或 exact collision。

## 5. 三轮累计与终态

| round/package | raw/unique | new MUST/SHOULD | 后续裁决 |
|---|---|---:|---|
| R1 query matrix | 70/63 | 2/5 | 后续全文均未形成 exact complete chain |
| R1 citation chain | 58 forward + 21 backward；12 abstracts | 0/1 | TCOM 2015 为 strong neighbor |
| R1 physical/B2 | shortlist 9 | 2/4 | 提供物理/B2 邻居；无 exact chain |
| R2 | 101/97 | 0/2 | 两篇 T033 全文均无 exact chain |
| R3 | 82/79 | **0/1** | OFC 2017 尚需全文 |

R1 三个包存在身份/用途重叠，保留分包计数，不作无依据相加。第 3 轮新增 SHOULD 非零，因此不满足 `ROUND3_CONVERGED_ZERO_NEW`；同时 `gw-supplement` 三轮上限已到，终态必须是：

`ROUND3_CAP_REACHED_WITH_NEW`

这只表示覆盖上限内仍有一篇全文债，不等于发现 exact collision，也不能自行开启第 4 轮。

## 6. Coverage limitations / protection

- Crossref 每组仅 10 条且长交叉查询假阳性高；metadata-new 不等于方法新。
- arXiv 仅 q01/q03 召回同一已知身份；零召回不证明不存在。
- OFC 2017 未获取全文，关键八字段必须保持 `UNKNOWN`；S2 abstract 被 publisher elide，OpenAlex daily budget exhausted。
- 前 agent 超时是操作债；本 salvage 没有用其未落盘判断填补证据。
- 四个 `p05` SHA256 逐一 fresh 核对为：`7843b048...f11`、`735e4650...38b`、`c76887c...34d`、`95a1d184...1de`，与保护基线 **4/4 相同**。
- `git diff --cached --name-only` fresh 输出为空，`staging_count=0`。

结构化审计：`search-archive/2026-08-09/coded-decoder-c1-step3_5-convergence-r3-annotated.json`。
