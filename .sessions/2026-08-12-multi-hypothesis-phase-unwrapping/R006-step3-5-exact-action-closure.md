# [R006] Step 3.5 exact-action 与 claim-ceiling 闭合

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D006

## 调研问题

冻结 Q001/D1 后，系统闭合 multi-hypothesis、fixed-lag、mixture/sequence tracker、coherent optical/FSO carrier-recovery 四类 prior：完整 D1 task/resource/output 合同是否仍无 exact/cheap absorption，还是只剩标准算法截断与任务重标？

## 发现

### 检索、引用链与收敛

- Round 1：10 个系统 query；36 raw、35 title/DOI unique；实际贡献源为 Semantic Scholar 与 SerpAPI Scholar，OpenAlex 本轮 query 返回 0。四条方法路线和四类场景/资源词均覆盖。
- Round 1 citation：C02 forward 21/21 records 完成语义筛查；新增 MUST/SHOULD=`5/5`。C01/C09/C12 因外部 API 长超时转入 Round 2，未把空调用写成覆盖。
- Round 2：C01/C09/C12 forward 实得 26 条 S2 records，全部筛查；backward 与 OpenAlex forward 为合法空结果，故只证明 forward 邻域，不假装完整双向召回。新增 MUST/SHOULD=`4/8`。
- Round 3：四个 Round-2 MUST 的 OpenAlex forward 为 14 raw/13 unique；全部筛查，new MUST/SHOULD=`0/0`。达到“最后一轮新增为 0”的检索收敛门。
- 三轮 citation records 实际语义筛查 `21+26+13=60`（轮间未声称全局去重）。machine receipt 见 `projects/thesis-fso/multi-hypothesis-phase-unwrapping/step3-5-search-receipt.json`。
- 逐条 semantic decision/reason ledger 见 R007；Round 3 工具未保存逐条 archive，R007 对其使用 stable ledger ID 并明确该轮只承担 new=0 收敛审计，不承担 terminal。

### 承重 primary fulltext

本轮最小必要精读 9 篇新全文，并复用 C02/C09/C10/C11/C12：

| primary | action signature 摘要 | Q001 disposition |
|---|---|---|
| Ulvog ICASSP 2023, `10.1109/ICASSP49357.2023.10095456` | wrapped single-tone → integer-cycle Viterbi paths → causal LMMSE/Gaussian branch score → fixed S survivor cap → iterative GLS → unwrapped sequence | `DIRECT_SAME_ACTION_FAMILY / CHEAP_ABSORPTION` |
| Tikhonov DPLL 2024, `10.1109/LSP.2024.3432048` | pure carrier → one Tikhonov state → causal H=1 wrapped phase | `CHEAP_ALTERNATIVE / STRONG_NEIGHBOR` |
| TCOM EP 2025, `10.1109/TCOMM.2025.3538847` | coded/pilot block → local mixture projection → fwd/bwd EP + rejection/damping → LLR | `FULL_GENERAL_COMPARATOR / COMPONENT_SOURCE` |
| GLOBECOM BCJR 2022, `10.1109/GLOBECOM48099.2022.10001274` | oversampled modulated block → L-grid discrete phase BCJR → APP/extrinsic | `FULL_GENERAL_BENCHMARK / TASK_MISMATCHED` |
| EP 2020, arXiv:2005.01844 | QAM+pilots → moment-matched one-Tikhonov fwd/bwd EP → LLR | `STRONG_NEIGHBOR` |
| PAPU 2019, `10.3390/app9132749` | QPSK+pilots → forward pilot-referenced unwrap/cycle-slip correction | `PILOT CHEAP ALTERNATIVE` |
| Ding TSP 2024, `10.1109/TSP.2024.3421374` | already-unwrapped chirp phase → joint ML/MAP + unknown PN variance | `ESTIMATOR/PHYSICAL_MODEL_NEIGHBOR` |
| WCNC 2024, `10.1109/WCNC57260.2024.10570836` | MPSK Mth-power → ML/MAP phase vector；unwrap uses truth/genie | `ORACLE_UNWRAP_REFERENCE` |
| OptCom 2024, `10.1016/j.optcom.2024.130326` | 64QAM ring/orientation candidates → window threshold → ordinary unwrap | `CHEAP_ESTIMATOR_CHANGING_NEIGHBOR` |

`10.1109/ACCESS.2026.3701043` 仅身份闭合，publisher 路径 HTTP 418、无全文；其动作保持 `UNRESOLVED`，不承担 terminal。C01/C02/C09/C10/C11/C12 的既有 primary contract 继续有效。

### 关键裁决

ICASSP 2023 的动作不是 Q001 完整字段逐字一致：其端到端是 lidar batch/iterative，未给 fixed traceback depth、irrevocable commit、confidence/fallback flag 或固定 worst latency。因此不写 `EXACT_ACTION_COLLISION`。

但冻结 gate 不是“只要少一个字段就活”。该全文已经占据 D1 的承重机制：single-tone integer-wrap hypotheses、receiver likelihood、bounded survivor prune、unwrapped-sequence output。把 survivor cap 设为 3，以及把标准 Viterbi traceback 截成 fixed lag，都只是参数选择/标准截断；若没有新的 score、commit、fallback 或可量化性能—复杂度机制，D1 正是 gate 3 所禁止的 task adaptation 包装。

因此 `confidence/fallback` 不能在 Step 3.5 事后变成救方向的空占位符；其具体动作尚未由 published defect/reference method 导出，也没有冻结、可区分的机制。D2 trigger 已在 D005 降为可选 ablation，更不能作为第二 Q 复活。

## 结论

唯一 terminal：`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`。

更精确地说，是 `CHEAP_ABSORPTION`：已确认 direct same-action family，D1 当前差异只剩标准 fixed-lag truncation 和未定义的 confidence/fallback。Q001 不进入 Step 4a；本专题停止在 Step 3.5，不实现、不仿真、不冻结参数。

## 对决策的影响

- D006 收口为上述 terminal；D005 的 Step 3 可证伪问题仍是历史有效证据，但其 D1 入口被 Step 3.5 prior-art gate 截断。
- claim ceiling 降为：Wang suffix-pollution problem evidence、Ulvog same-action-family prior、Tikhonov/BCJR/EP/full-mixture 与 optical cheap comparators 的结构化比较资产。不得形成 Ch4 算法主张。
- Step 4a 无合法入口；未来若有新的 published defect 导出非平凡 commit/fallback 机制，应作为新的 research object 重新走入口，不得在本专题内补字段重开。
