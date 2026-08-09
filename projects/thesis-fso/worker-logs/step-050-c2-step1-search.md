# Step 050 — C2 Groundwork Step 1 search

> 2026-08-09 | T004 | `GROUNDWORK_STEP1_SEARCH`
> task-control validator: `PASS`
> Terminal: `C2_EXACT_COLLISION_FOUND`

## Boundary

只执行检索、AI 逐条标注、摘要级交叉验证与 C2 route 判读。未下载/精读全文，未实现、未实验，未修改 formal owner、源码、scientific artifact 或四个既有 `p05_run*.log`。

## Execution facts

- 一轮 3 query groups：S2 direct=15；arXiv sync=0；Exa optical=0（402 credits）。
- 二轮 2 targeted groups：IEEE APPA/extrinsic=3；IEEE hard/soft-DD exact-title=1。
- Crossref fallback=15；local mandatory seeds=3。
- actual result sources：S2 / Crossref / IEEE = 3。
- raw 37；title-normalized unique 30；formal 26/30=86.67%。
- raw priority：必读5 / 建议读2 / 待确认4 / 备选20 / 排除6；所有 37 条均写回 `priority` 与 `priority_reason`，并附 `c2_relation`/`evidence_pointer`。
- unique priority：必读5 / 建议读1 / 待确认4 / 备选14 / 排除6。

### Query/source receipt

| round | focus | actual source/result | JSON |
|---|---|---|---|
| R1-Q1 | decoder-aided/turbo CPR + LDPC extrinsic soft symbol | S2 15 | `coded-decoder-c2-r1-direct-s2.json` |
| R1-Q2 | iterative demap/decode + residual CFO/CPE | arXiv 0 | `coded-decoder-c2-r1-sync-arxiv.json` |
| R1-Q3 | coherent optical/FSO feedback + pilot/DD baseline | Exa 0 (402) | `coded-decoder-c2-r1-optical-exa.json` |
| R2-Q1 | APPA/extrinsic→ML phase action | IEEE 3 | `coded-decoder-c2-r2-ieee-appa.json` |
| R2-Q2 | hard/soft-DD CPR comparator | IEEE 1 | `coded-decoder-c2-r2-ieee-hard-soft.json` |
| fallback | direct code-aided CPR DOI/venue | Crossref 15 | `coded-decoder-c2-r1-direct-crossref.json` |
| local seed | mandated three DOI/arXiv seeds | local index 3 | `coded-decoder-c2-local-seeds.json` |

去重：raw 37 → title-normalized unique 30；7 个重复组来自 S2↔IEEE/Crossref 交叉命中。正式发表 26/30（86.67%）。实际非空来源为 S2/Crossref/IEEE 共 3。

## Scientific findings

1. S2 摘要对 DOI `10.1109/TWC.2004.837407` 明确写出 turbo decoder extrinsic LLR 被用于 iterative maximum-likelihood phase estimation；这是 C2 核心 `true-extrinsic → continuous phase action` 的 action-signature collision。
2. 2025 FCN WNSSP 使用 soft LDPC belief 做 ML carrier recovery；2026 IEEE Access 使用 LDPC partial decision metrics 经随机梯度联合 phase/frequency convergence，并连接 Costas tracking 与 decoder feedback。该动作族并非孤立老文。
3. 2012 hard/soft decision-directed iterative CPR（DOI `10.1109/GLOCOM.2012.6503711`）是最贴近的 conventional comparator；公式和 matched-budget 细节需后续合法全文阶段确认。
4. 2023 adjustable-range CA synchronization（DOI `10.1109/IWCMC58020.2023.10182805`）提供 CMF coarse correction + candidate-list conventional baseline。
5. 未找到摘要支持的 optical/FSO decoder-feedback direct hit；只有 pilot-tone optical CPR baseline。把成熟 code-aided/turbo action 迁到 FSO 当前只是场景迁移。

### Must-read / competitor / baseline routing

- 必读 5：`10.1109/ACCESS.2026.3653159`、`10.1109/FCN66513.2025.11296777`、`10.1109/TVT.2025.3600028`（arXiv `2309.12828`）、`10.1109/IWCMC58020.2023.10182805`、`10.1186/s13634-023-00975-7`。
- direct action collision：`10.1109/TWC.2004.837407`（摘要明确 turbo-decoder extrinsic LLR → iterative ML phase estimation）。
- conventional baselines：`10.1109/GLOCOM.2012.6503711`（hard/soft-DD iterative CPR）、`10.1109/VETECF.2010.5594466`（DD phase/timing）、`10.1109/IWCMC58020.2023.10182805`（CMF coarse correction + candidate list）、`10.1109/TCOMM.2011.051311.100047`（pilot-aided CPR）。
- 两轮变化：由宽泛 decoder-aided/optical 检索收敛到 APPA/extrinsic action lineage 与 hard/soft-DD comparator identity；不是同义词重搜。

## Anomalies and limitations

- 首次聚合 `tools/search` 被 64 s 外部 timeout 截断；根因是结果后的 OpenAlex 摘要补全与退避无全局 deadline。OpenAlex 单源另遇 rate-limit。
- `tools/blit` CRLF wrapper 在 WSL 解析失败；未修改共享工具，使用其同一 Python entrypoint/torch venv，且未下载。
- S2 batch DOI 交叉验证 HTTP 429；保存 failure receipt，未计成功证据。
- 22/30 unique 无摘要，相关动作均标 `AI推断，未验证` 或 `UNKNOWN`。
- `EXACT_COLLISION` 只到 abstract-supported core action，不声称公式、single-update 或总预算逐项等价。
- `tools/search` 自动生成的 3 个非前缀冗余 archive 已在确认本轮时间戳与独立 coded 输出后移除；保留的所有任务输出均为 `coded-decoder-c2-*`。

## Outputs

- `search-archive/2026-08-09/coded-decoder-c2-*.json`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c2-search-report.md`
- `projects/thesis-fso/worker-logs/step-050-c2-step1-search.md`

## Route disposition

当前 C2 文字合同只剩 soft-symbol mapping、一次 bounded update、matched budget 与 FSO 场景差异；摘要层没有形成新的具体 M-C-A。建议 integrated reviewer 将 C2 判为 action-collision，不授权 Step 2；若保留，必须先重写为与 L001/L002/ACCESS 2026 不同且承重的 problem/action。

### Machine-readable integration list

```yaml
terminal: C2_EXACT_COLLISION_FOUND
route: C2
step1_total_gate: NOT_JUDGED
corpus:
  raw: 37
  unique: 30
  formal: 26
  formal_ratio: 0.8667
  actual_sources: [s2, crossref, ieee]
candidates:
  - {id: C2-D01, doi: 10.1109/TWC.2004.837407, relation: EXACT_COLLISION, input: turbo_decoder_extrinsic_LLR, action: iterative_ML_phase_estimation, pointer: coded-decoder-c2-r1-direct-s2.json#L001}
  - {id: C2-D02, doi: 10.1109/FCN66513.2025.11296777, relation: STRONG_NEIGHBOR, input: soft_LDPC_belief, action: ML_carrier_recovery, pointer: coded-decoder-c2-r1-direct-s2.json#L002}
  - {id: C2-D03, doi: 10.1109/ACCESS.2026.3653159, relation: STRONG_NEIGHBOR, input: LDPC_partial_decision_metrics, action: joint_phase_frequency_update, pointer: coded-decoder-c2-local-seeds.json#S002}
  - {id: C2-D04, doi: 10.1109/TVT.2025.3600028, relation: STRONG_NEIGHBOR, action: iterative_joint_CFO_CPO_estimation, pointer: coded-decoder-c2-local-seeds.json#S001}
  - {id: C2-B01, doi: 10.1109/GLOCOM.2012.6503711, relation: BASELINE, action: iterative_hard_soft_DD_CPR, pointer: coded-decoder-c2-r2-ieee-hard-soft.json}
  - {id: C2-B02, doi: 10.1109/IWCMC58020.2023.10182805, relation: BASELINE, action: CMF_coarse_correction_candidate_list, pointer: coded-decoder-c2-local-seeds.json#S003}
report_path: projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c2-search-report.md
json_glob: search-archive/2026-08-09/coded-decoder-c2-*.json
```

## Terminal

`C2_EXACT_COLLISION_FOUND`
