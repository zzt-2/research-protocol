# C2 Groundwork Step 1 路由检索报告

> 2026-08-09 | T004 | `GROUNDWORK_STEP1_SEARCH`
> Terminal: `C2_EXACT_COLLISION_FOUND`
> 边界：只裁 C2 route；不代表 Step 1 总门 PASS，不形成 Q#、Go、METHOD_SIGNAL、adapter 或实验授权。

## 1. 检索对象与结论口径

C2 合同为：`decoder L_post/L_apriori -> true L_ext -> on-air soft-symbol expectation/reliability -> one bounded continuous phase/CFO update -> re-demap/re-decode under matched total BP/front-end/latency budget`。

本轮只用 title、abstract、venue、year、citation、publication status 判读。摘要不支持的动作细节均标为“AI推断，未验证”；没有下载或精读全文。

## 2. Query / command / source receipt

| round | query focus | command/source | actual | result |
|---|---|---|---:|---|
| R1-Q1 | decoder-aided/turbo CPR + LDPC extrinsic soft symbol | `PYTHONDONTWRITEBYTECODE=1 bash tools/search ... --sources s2 --max-per-source 15 --top 40 --format json` | S2 15 | `coded-decoder-c2-r1-direct-s2.json` |
| R1-Q2 | iterative demap/decode synchronization + residual CFO/CPE | 同上，`--sources arxiv` | arXiv 0 | `coded-decoder-c2-r1-sync-arxiv.json` |
| R1-Q3 | coherent optical/FSO decoder feedback + pilot/DD/turbo baseline | 同上，`--sources exa --exa-mode keyword` | Exa 0（HTTP 402，额度耗尽） | `coded-decoder-c2-r1-optical-exa.json` |
| R2-Q1 | L001 的 APPA/extrinsic→ML phase-estimation action | IEEE `tools/blit.py`, query=`a priori probability aided phase estimation extrinsic turbo carrier phase`, `--max 15` | IEEE 3 | `coded-decoder-c2-r2-ieee-appa.json` |
| R2-Q2 | L005 的 hard/soft-DD comparator identity | IEEE `tools/blit.py`, query=`Performance analysis code aided iterative hard soft decision directed carrier phase recovery`, `--max 15` | IEEE 1 | `coded-decoder-c2-r2-ieee-hard-soft.json` |
| fallback | direct code-aided CPR DOI/venue coverage | Crossref REST `/works?query.bibliographic=...&rows=15` | Crossref 15 | `coded-decoder-c2-r1-direct-crossref.json` |
| local seed | mandated DOI/arXiv seeds | `search-archive/_index/all-papers.jsonl` exact DOI lookup | 3 unique | `coded-decoder-c2-local-seeds.json` |

实际有结果来源为 **S2、Crossref、IEEE，共 3 个**；arXiv/Exa 的 0-result 不计来源覆盖。每个 API/source 请求目标为 15。

执行异常：首次多源 `tools/search` 在 64 s 外部 timeout 前未写 JSON；根因是聚合后的逐条 OpenAlex 摘要补全/退避超过外部 deadline，不是 wrapper 本体失常。OpenAlex 单源诊断又遇 3/6/12/24 s rate-limit 退避。`tools/blit` 的 CRLF wrapper 在 WSL 报 `$'\r'`，未修改共享工具，改由相同 torch venv 直接调用 `tools/blit.py`，且未传 `--download`。S2 batch 交叉验证另遇 HTTP 429，失败 receipt 保存在 `coded-decoder-c2-abstract-verification-s2.json`，未当作成功证据。

## 3. Corpus、去重与质量统计

- raw entries：37；按规范化 title 去重后：30。
- 正式发表：26/30 = **86.67%**。
- unique priority：必读 5、建议读 1、待确认 4、备选 14、排除 6。
- raw priority：必读 5、建议读 2、待确认 4、备选 20、排除 6。
- 有可用摘要的 unique records：8/30；其余只允许元数据级候选判断。

| duplicate title | merged receipts |
|---|---|
| Iterative carrier phase recovery suited to turbo-coded systems | S2 + IEEE |
| Novel iterative APPA carrier phase recovery and detection for turbo-coded systems | S2 + IEEE |
| Performance analysis of code-aided iterative hard/soft decision-directed CPR | S2 + IEEE |
| Non-binary LDPC-CPM code-aided phase synchronization | S2 + Crossref |
| Decision-directed phase/timing recovery for LDPC-coded systems | S2 + Crossref |
| Simplified iterative timing/phase recovery for LDPC-coded systems | S2 + Crossref |
| Iterative LDPC-Hadamard code-aided phase synchronization | S2 + Crossref |

## 4. 必读候选与 direct competitors

| paper | abstract-supported input → action → output | timing / true extrinsic | C2 relation | pointer |
|---|---|---|---|---|
| Zhang & Burr, 2004, *Iterative carrier phase recovery suited to turbo-coded systems* | turbo decoder **extrinsic LLR** → a-priori-probability-aided iterative ML phase estimation → phase estimate + decoded output | decoder/estimator joint iteration；摘要明确 extrinsic | **EXACT_COLLISION（核心动作级）** | DOI `10.1109/TWC.2004.837407`; S2 JSON L001 |
| 2025 FCN, *Error-Threshold Based Joint Phase Estimation and Decoding* | soft LDPC belief/WNSSP → ML carrier recovery/parallel phase compensation → synchronized reconstruction | joint factor graph；未证明 `L_post-L_apriori` | STRONG_NEIGHBOR | DOI `10.1109/FCN66513.2025.11296777`; S2 L002 |
| 2026 IEEE Access, *Pilotless Iterative Carrier Synchronization With LDPC PDMs* | LDPC partial decision metrics → approximate-stochastic-gradient joint phase/frequency convergence + Costas feedback → synchronized coded QPSK | after a few decoding iterations；PDM ≠ 已证 true extrinsic | STRONG_NEIGHBOR | DOI `10.1109/ACCESS.2026.3653159`; local-seed S002 |
| 2025 TVT, *Code-Aided CFOs and CPOs Estimation in Cooperative Satellite Communication* | code-aided objective → ICE/CTEOF iterative joint CFO/CPO estimation → coherent combining/BER | decoder message contract 未在摘要说明 | STRONG_NEIGHBOR | DOI `10.1109/TVT.2025.3600028`; arXiv `2309.12828`; local-seed S001 |
| 2023 EURASIP, *Carrier phase recovery of LDPC-coded systems based on likelihood difference* | 题名显示 LDPC-coded CPR；当前无摘要 | action/timing/true extrinsic 均未验证 | STRONG_NEIGHBOR 候选 | DOI `10.1186/s13634-023-00975-7`; Crossref X007 |
| 2023 IWCMC, *Code-Aided Carrier Synchronization with Adjustable Operating Ranges* | CMF coarse correction + candidate list → expanded carrier-recovery range | conventional CA；不以 decoder true extrinsic 为核心 | BASELINE | DOI `10.1109/IWCMC58020.2023.10182805`; local-seed S003 |

补强邻居：2020 non-binary LDPC-CPM 论文摘要明确 decoding soft information 进入 synchronization parameter estimation，并联合迭代 synchronizer/demodulator/decoder（DOI `10.1117/12.2557492`）。题名近乎精确的 “Information-reduced ... Soft Decision (Extrinsic) Feedback” 因无 DOI/venue/abstract，仅列 `UNKNOWN / AI推断，未验证`。

## 5. Conventional baselines 与公式可得性

1. **2012 hard/soft decision-directed iterative CPR**（DOI `10.1109/GLOCOM.2012.6503711`）：最贴近“同一次 update、同额外 front-end、同总 BP/latency” comparator；IEEE/S2 元数据已交叉命中，公式需 Step 2/3 全文确认。
2. **2010 decision-directed phase + timing recovery for LDPC-coded systems**（DOI `10.1109/VETECF.2010.5594466`）：hard-DD cheap comparator；当前只有元数据。
3. **2023 adjustable-range CA synchronization**（DOI `10.1109/IWCMC58020.2023.10182805`）：摘要支持 CMF coarse correction + candidate list，可作 problem-bearing conventional CA baseline。
4. **2011 pilot-aided carrier recovery under phase noise**（DOI `10.1109/TCOMM.2011.051311.100047`）：pilot baseline；仅元数据。
5. 本地历史要求仍成立：P08-R2 B2、hard-DD/Costas 与场景适用时的 corrected standard-CMA continuation 必须进入 cheap-alternative ladder；本轮没有运行这些 baseline。

## 6. 两轮方向变化与 optical/FSO transfer

一轮从宽泛的 decoder-aided/iterative/optical 三角检索，迅速暴露出成熟的 **APPA/extrinsic→iterative phase-estimation** 族。二轮因此不再换同义词，而分别追查：

- L001 的 information contract 与连续 ML phase action lineage；
- L005 的 hard/soft-DD conventional comparator 身份。

IEEE 二轮同时回收 APPA 2009/2010 扩展和 2012 hard/soft-DD comparator。光学/FSO 一轮没有返回 decoder-feedback direct hit；Crossref 只补到 optical pilot-tone CPR baseline。因此，把既有 code-aided/turbo CPR 移到 coherent optical/FSO，当前最多是**场景迁移**，不能单独构成 C2 方法动作。

## 7. C2 falsifier 判读

`C2_EXACT_COLLISION_FOUND`，但严格限定为**摘要支持的核心 action signature**：

- L001 已明确实现 `decoder extrinsic LLR → iterative continuous ML phase estimation → re-decoding`，与 C2 的“true-extrinsic 驱动连续 CPR 更新”核心重合。
- L002（2025）与 ACCESS 2026 又表明该 lineage 仍在用 soft LDPC belief/PDM 驱动 phase 或 phase+frequency recovery；不是只存在一篇孤立老文。
- C2 当前剩余差异只有 on-air 16QAM expectation、一次 bounded update、matched total budget 与 FSO 场景；这些是实现/公平合同或场景迁移，摘要层没有形成新的具体 M-C-A。

因此，**按当前 C2 文字合同不应进入 Step 2**。若整合审查仍想保留，必须先重写为一个不被 L001/L002/ACCESS 2026 覆盖的具体 problem/action，并在后续合法全文阶段证明差异承重；不能只用 “true extrinsic”、soft-symbol mapping 或 FSO 标签重命名。

## 8. Claim limitations

- 没有全文，不能断言 L001 与 C2 的公式、单次更新时点、BP/front-end/latency budget 完全同构；这里的 `EXACT_COLLISION` 是 input→continuous-phase-action 核心签名，不是逐行实现等价。
- 22/30 unique records 无可用摘要；其方法细节均未作为事实。
- S2 batch 429、OpenAlex rate-limit、Exa 402、arXiv 0-result 均限制了近期长尾召回；但不削弱 L001/L002/ACCESS 三条承重摘要证据。
- 没有证明“FSO 中无人做过”，也没有证明传统 baseline 已解决目标 defect；后者只能在 Step 4a 裁决。
- 本报告不裁 C1，不裁 integrated Step 1 总门。

## 9. Machine-readable candidate table

```yaml
- candidate_id: C2-D01
  doi: 10.1109/TWC.2004.837407
  year: 2004
  relation: EXACT_COLLISION
  input: turbo_decoder_extrinsic_LLR
  action: iterative_ML_phase_estimation
  output: phase_estimate_and_decoded_bits
  true_extrinsic: abstract_explicit
  evidence: coded-decoder-c2-r1-direct-s2.json#L001
- candidate_id: C2-D02
  doi: 10.1109/FCN66513.2025.11296777
  year: 2025
  relation: STRONG_NEIGHBOR
  input: soft_LDPC_belief_WNSSP
  action: ML_carrier_recovery_parallel_phase_compensation
  true_extrinsic: not_abstract_verified
  evidence: coded-decoder-c2-r1-direct-s2.json#L002
- candidate_id: C2-D03
  doi: 10.1109/ACCESS.2026.3653159
  year: 2026
  relation: STRONG_NEIGHBOR
  input: LDPC_partial_decision_metrics
  action: stochastic_gradient_joint_phase_frequency_update
  true_extrinsic: no
  evidence: coded-decoder-c2-local-seeds.json#S002
- candidate_id: C2-D04
  doi: 10.1109/TVT.2025.3600028
  year: 2025
  relation: STRONG_NEIGHBOR
  input: code_aided_objective
  action: iterative_joint_CFO_CPO_estimation
  true_extrinsic: unknown
  evidence: coded-decoder-c2-local-seeds.json#S001
- candidate_id: C2-B01
  doi: 10.1109/GLOCOM.2012.6503711
  relation: BASELINE
  action: iterative_hard_soft_DD_CPR
  formula_access: fulltext_required
  evidence: coded-decoder-c2-r2-ieee-hard-soft.json
- candidate_id: C2-B02
  doi: 10.1109/IWCMC58020.2023.10182805
  relation: BASELINE
  action: CMF_coarse_correction_plus_candidate_list
  evidence: coded-decoder-c2-local-seeds.json#S003
```

## Terminal

`C2_EXACT_COLLISION_FOUND`
