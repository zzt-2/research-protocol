# C1 finite phase-hypothesis re-evaluation — Step 1 route search

> 2026-08-09 | T005 | terminal: `C1_EXACT_COLLISION_FOUND`
> Claim ceiling: C1 route-level novelty falsifier only; **not** Groundwork Step 1 PASS, not Q#, not Go/Kill for the whole coded-decoder-feedback topic.

## Findings first

1. **C1 的通用动作签名已发生 exact collision。** arXiv:2511.21340 的官方摘要逐项给出：decoder extrinsic 作为 model-evidence metric、由 PSK 对称性生成有限候选模型、decoder 选择最可能候选、初始化后只调用一次。它与 C1 的 `decoder evidence → frozen finite bank → one selection` 相同；差别主要是 OFDM blind channel-estimation 场景，而不是动作身份。
2. 2006 年 IEEE TSP `10.1109/TSP.2006.874844` 已系统比较 code-aided phase-ambiguity hypothesis-testing 算法；2005 年 `10.1155/ASP.2005.981`、2007 年 `10.1109/IDC.2007.374550`、2010 年 `10.1109/TSP.2010.2068291` 又覆盖 iterative ML、local-check-node 与 free-energy 路线。故不能把“decoder feedback”或“FSO 中少见”写成 C1 空白。
3. 2025 FCN `10.1109/FCN66513.2025.11296777` 的 S2 摘要确认 WNSSP 将 soft-LDPC syndrome belief 融入 ML carrier recovery；它不是有限 one-switch，但构成 decoder-syndrome 直接强邻居。
4. strongest receiver-only comparator 至少应包含 pilot/front-end cycle-slip mitigation（SPIE `10.1117/12.3107192`）、blind phase/CFO estimator（`10.1155/2010/293572`）和 phase-equivariant coded modulation；本轮未取得一个同时冻结公式、公开实现和 matched latency/BP/front-end budget 的单一 comparator。
5. 当前证据足以触发 C1 的“exact-action competitor” falsifier，但不足以宣称整个 Step 1 质量门 PASS：去重后 19 篇（门槛 20）、`必读` 2 篇（门槛 5）。

## 执行与时间纪律

- fresh task-control validator：`PASS`；control epoch 2 / CP002 / `GROUNDWORK_STEP1_SEARCH`。
- 上一轮实际约 30 分钟，**违反任务书单次 ≤15 分钟硬上限**。主要时间消耗在聚合 `tools/search` 的逐条摘要补全、S2 限速、OpenAlex timeout 与 SerpAPI enrichment；收到硬时限提醒后才停止。此违规不因本报告收口而消失。
- 本轮只收口，不再检索或联网；未下载全文、未实现、未实验、未恢复 C3、未修改 P08/P08-R/P08-R2 或四个 `p05_run*.log`。
- `tools/search` 自动生成了非 `coded-decoder-c1-*` 的镜像存档并增量更新 `search-archive/_index/all-papers.jsonl`；这是工具副作用，未手工清理，列为路径独立性异常。

## Query / command / source receipt

| round | query / command | actual source | result | output |
|---|---|---|---:|---|
| R1-Q1 | `tools/search` 超窄 finite-hypothesis query；先聚合后 S2-only | aggregate enrichment timeout；S2 429 | 0 | `coded-decoder-c1-r1q1-code-aided-finite-hypothesis.json` |
| R1-Q2 | `tools/search` syndrome/cycle-slip query | OpenAlex | timeout before usable write | `coded-decoder-c1-r1q2-syndrome-cycle-slip.json` |
| R1-Q3 | `tools/search "code aided carrier synchronization phase estimation LDPC" ... --sources arxiv` | arXiv | 0 | `coded-decoder-c1-r1q3-broad-code-aided-sync-arxiv.json` |
| R1-Q4 | `tools/search "cycle slip correction FEC coherent optical" ... --sources exa` | Exa | 0; HTTP 402 credits | `coded-decoder-c1-r1q4-broad-cycle-slip-exa.json` |
| R1-Q5 | `tools/search "code aided phase ambiguity resolution LDPC" ... --sources serpapi` | SerpAPI Scholar | 15 | `coded-decoder-c1-r1q5-broad-phase-ambiguity-serpapi.json` |
| R1 fallback | 3 contracted broad web queries | web search + arXiv/SPIE/Springer/IEEE metadata | 6 retained | `coded-decoder-c1-r1-web-fallback.json` |
| R2-Q1 | finite-bank trigger→action / once-after-initialization | web search + arXiv + Crossref + S2 | 3 | `coded-decoder-c1-r2q1-finite-bank-action.json` |
| R2-Q2 | same-frame timing / pilot-likelihood-DD comparator | web search + S2 + SPIE + patent metadata | 4 | `coded-decoder-c1-r2q2-timing-comparator.json` |

所有 `tools/search` 成功调用均带 `PYTHONDONTWRITEBYTECODE=1`、`--mode academic --preset problem-driven --max-per-source 15 --top 40 --format json`。可用证据的实际 source 家族 ≥3：SerpAPI Scholar、web search、Crossref、Semantic Scholar、arXiv、publisher abstract。

## 去重、AI 标注与质量门

| item | observed | gate | status |
|---|---:|---:|---|
| 原始 annotated rows | 28 | — | PASS |
| title-normalized unique | 19 | ≥20 | **FAIL** |
| 每条 `priority` + `priority_reason` | 28/28 | 100% | PASS |
| actual source families | ≥6 | ≥3 | PASS |
| `必读` | 2 | ≥5 | **FAIL** |
| 正式发表 | 16/19 = 84.21% | ≥50% | PASS |
| 技术路线 | finite-bank/code-aided ambiguity；iterative continuous recovery；pilot/NDA/structural baseline | ≥2 | PASS |
| R2 targeted groups | 2 | ≥2 | PASS |

Priority distribution（unique）：`必读=2`、`待确认=2`、`备选=14`、`排除=1`。年代较早但承重的直接论文按 gw-search 规则标为“备选”，没有为了凑门而改成“必读”。

## Direct competitors

| candidate | evidence → action | causal timing | relation | abstract-level verification |
|---|---|---|---|---|
| Chen et al., arXiv:2511.21340 (2025) | decoder extrinsic model evidence → select one of finite symmetry-derived models | once after EM initialization | **EXACT_COLLISION** | official arXiv abstract |
| Wymeersch et al., TSP 2006 | code-aided hypothesis metric → phase-ambiguity hypothesis selection | frame receiver；split-BP timing 未给 | **EXACT_COLLISION** | DOI/S2 metadata + search abstract；精确 budget 未验证 |
| Karuppasami & Cowley, IDC 2007 | local parity checks → resolve sub-block ambiguity | same coded block；switch timestamp 未给 | STRONG_NEIGHBOR | DOI/S2 metadata；细节超出摘要者标 `AI推断，未验证` |
| Chen et al., FCN 2025 | WNSSP soft-LDPC belief → parallel phase compensation / ML recovery | joint iterative receiver | STRONG_NEIGHBOR | S2 DOI abstract |
| Wymeersch & Moeneclaey, 2005 | soft decoder information → iterative ML phase/ambiguity update | iterative | STRONG_NEIGHBOR | Springer official abstract |

## Conventional baselines / strongest cheap alternatives

| baseline | role | unresolved item |
|---|---|---|
| SPIE 2026 phase-pilot aided cycle-slip mitigation | recent coherent-optical pilot/front-end comparator | matched latency/front-end-call formula not frozen |
| `10.1155/2010/293572` blind phase/CFO estimator | receiver-only NDA likelihood comparator | implementation identity/tuning not frozen |
| Phase-Equivariant Polar Coded Modulation (2023) | structural ambiguity-removal alternative | task/net-rate parity not frozen |
| US20170126328A1 pilot-based cycle-slip correction | concrete causal receiver architecture | patent, not sufficient paper comparator alone |
| P05 corrected CMA continuation | local repository cheap alternative for dual-pol swap only | cannot generalize to coded CPR slice |

## 两轮方向变化

- 一轮起点把 syndrome/CRC cycle-slip repair 当成主要空白风险。
- 初筛后，最承重信号转为更早、更直接的 **code-aided phase-ambiguity hypothesis testing**；CRC final relabel 反而是已知 dead end。
- 二轮不再扩同义词，而是核 `trigger → finite-bank selection`、一次调用时点和 receiver-only comparator。结果确认 generic C1 action 已被覆盖；尚未确认的只剩项目特定的 matched budget/FSO testbed，而这不能单独支撑方法新颖性。

## C1 falsifier 判读

| falsifier | verdict | evidence |
|---|---|---|
| 等价 `decoder evidence → finite current-frame phase hypothesis selection` 竞品存在 | **TRIGGERED** | arXiv:2511.21340；TSP 2006 |
| decoder evidence 相对 receiver-only likelihood 的承重增量 | UNKNOWN | 未运行实验；comparator identity 尚未冻结 |
| 退化为 final-correctness / post-hoc best-of | AVOIDABLE, NOT A NOVELTY DELTA | direct papers use receiver code evidence；本地 CRC final relabel dead end 保持 |
| stale-state rollback | NOT INVOLVED | C1/current competitors operate on current initialization/frame hypotheses |

因此 C1 不能以“有限相位 bank + decoder consistency + 一次选择”作为新的核心方法动作继续；只有明确新增且可区分的 deployable action（而非换 syndrome trigger、换 FSO 场景或加公平账本）才可能重开。C3 仍只作 C1 evidence/ablation，不恢复独立卡。

## Claim limitations

- 未下载/精读全文；不声称算法公式、精确 BP 分配、front-end 调用次数或公开实现已闭合。
- S2 对若干 IEEE 老论文的 abstract 被 publisher elide；超出 title/摘要片段/DOI metadata 的 timing 细节均标 `AI推断，未验证`。
- 19 unique 与 2 `必读` 未过 Step 1 总门；本报告只裁 C1 route falsifier。
- `EXACT_COLLISION` 是 deployable action identity 判断，不是“同一 FSO channel/同一 code/同一 implementation”的声称。

## Machine-readable candidate table

```json
[
  {"id":"C1-X1","pointer":"arXiv:2511.21340","evidence":"decoder_extrinsic_model_evidence","action":"finite_candidate_select_once","relation":"EXACT_COLLISION","status":"preprint","claim_ceiling":"abstract"},
  {"id":"C1-X2","pointer":"10.1109/TSP.2006.874844","evidence":"code_aided_hypothesis_metric","action":"phase_ambiguity_hypothesis_selection","relation":"EXACT_COLLISION","status":"published","claim_ceiling":"abstract_metadata; budget_unknown"},
  {"id":"C1-N1","pointer":"10.1109/IDC.2007.374550","evidence":"local_parity_checks","action":"subblock_phase_ambiguity_resolution","relation":"STRONG_NEIGHBOR","status":"published","claim_ceiling":"abstract_metadata"},
  {"id":"C1-N2","pointer":"10.1109/FCN66513.2025.11296777","evidence":"WNSSP_soft_LDPC","action":"parallel_phase_compensation_ML","relation":"STRONG_NEIGHBOR","status":"published","claim_ceiling":"S2_abstract"},
  {"id":"C1-B1","pointer":"10.1117/12.3107192","evidence":"phase_pilot_labels","action":"cycle_slip_mitigation","relation":"BASELINE","status":"published","claim_ceiling":"publisher_abstract"}
]
```

## Terminal

`C1_EXACT_COLLISION_FOUND`

这不是 Step 1 总门 PASS；integrated reviewer 应把 C1 generic action 从 survivor 中移除或要求真正不同的 action identity，而不是把查询数量不足误当成 novelty 未被证伪。
