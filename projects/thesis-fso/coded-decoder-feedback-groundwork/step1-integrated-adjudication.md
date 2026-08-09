# Coded decoder-feedback Step 1 integrated adjudication

> 2026-08-09 | T006 | fresh task-control validator: `PASS`
> Terminal: `STEP1_NO_METHOD_ACTION_SURVIVOR`

## Collision adjudication

| route | independent verdict | load-bearing receipt | limitation |
|---|---|---|---|
| C2 continuous soft-information CPR | `CORE_ACTION_EXACT` | DOI `10.1109/TWC.2004.837407` 的 S2 完整摘要明确：turbo decoder extrinsic LLR 用于 iterative maximum-likelihood phase estimation | 不声称公式、单次更新或 matched budget 逐项等价 |
| C2 recent lineage | `STRONG_NEIGHBOR` | FCN 2025 摘要支持 soft-LDPC belief/WNSSP→ML carrier recovery；ACCESS 2026 摘要支持 LDPC PDM→joint phase/frequency update + Costas/decoder feedback | 二者未证明 true `L_post-L_apriori` |
| C1 finite-candidate selection | `CORE_ACTION_EXACT` | 官方 arXiv API 摘要对 `2511.21340` 明确给出 decoder extrinsic model evidence→PSK 对称有限候选→decoder 选择最可能候选，且初始化后只调用一次 | 场景为 OFDM blind channel estimation；不声称同 FSO/BP/预算 |
| TSP 2006 | `STRONG_NEIGHBOR` | DOI `10.1109/TSP.2006.874844` 支持 code-aided phase-ambiguity hypothesis-testing family | 现有摘要 receipt 不足以独立证明 C1 精确时点/预算，故不列 exact |

两张原卡的核心 carrier-recovery action 均已碰撞；场景、trigger、soft-symbol mapping、一次/多次、阈值或公平账本差异都不足以形成新的动作身份。

## T006 v1 corpus receipt（历史，已由 T008 v2.1 取代）

> 以下 65→46 / 39 published 是 T006 首次整合的历史口径，不是当前 authority。当前口径见本报告后文 T008 receipt：93→66 / 50 published；机器可读 authority 为 integrated v2.1。

- 输入：全部 `coded-decoder-c1-*.json` 与 `coded-decoder-c2-*.json`，共 65 条 annotated rows。
- DOI→arXiv→normalized title 合并后：**46 unique**。
- 实际外部来源族：**7**（S2、Crossref、IEEE、arXiv、publisher abstract、SerpAPI Scholar、web search）；local index 不另算独立来源。
- `必读`：**6**；正式发表：**39/46 = 84.78%**；技术路线：**2**。
- C1/C2 二轮定向检索组：**2/2**；本报告保留的 exact/strong action claim 均有摘要级 pointer。
- 质量门：`PASS`。它只证明 corpus 足以裁候选，不证明存在 survivor。

这组 v1 数字只为审计保留；当前 `search-archive/2026-08-09/coded-decoder-step1-integrated.json` 已升级为 v2.1，不再承载 v1 records。

## Must-read / comparator freeze

Step 2 shortlist（年代早但承重者保持“备选”，未改 priority）：arXiv `2511.21340`；DOI `10.1109/TSP.2006.874844`、`10.1109/TWC.2004.837407`、`10.1109/FCN66513.2025.11296777`、`10.1109/ACCESS.2026.3653159`、`10.1109/GLOCOM.2012.6503711`、`10.1109/IWCMC58020.2023.10182805`、`10.1117/12.3107192`。

- C1 strongest comparator：receiver-only pilot/front-end phase-hypothesis/cycle-slip correction，候选锚点为 `10.1117/12.3107192`；直接竞品为 arXiv `2511.21340` 与 TSP 2006 family。
- C2 strongest conventional comparator：同信息、同 update/front-end/BP/latency 预算的 iterative hard/soft decision-directed CPR，身份锚点 `10.1109/GLOCOM.2012.6503711`；direct competitor 为 `10.1109/TWC.2004.837407`。
- cheap alternatives：P08-R2 B2/no-feedback；对应 dual-pol swap slice 才加入 corrected standard-CMA continuation。P05 的 `0.00018/0.00117` 不能跨场景外推。

## Replacement sketch gate

接受数：**0**。现有 corpus 没有同时具备 problem/action evidence、且动作不同于 C1/C2、D047 relock/state-switch、D028 historical rollback、F4-C relabel、P08 scalar、P05 CMA、CCISP/Ch5 selection/scheduling 的对象。为继续而把 trigger、阈值、场景、一次/多次、mapping、账本或调度重命名，均不通过 replacement 门。

## Current Step 1 disposition and limitations

- terminal：`STEP1_NO_METHOD_ACTION_SURVIVOR`
- framework disposition：`STEP1_CANDIDATE_SET_EXHAUSTED`
- problem disposition：`NOT_EVALUATED_NO_Q_FORMED`；本轮未进入 Step 2/3、未形成 canonical M-C-A Q#，因此不授权 `NO_VALID_PROBLEM` 判定。
- adapter：不建设；Step 2 不授权。
- D028 只否决 stale historical rollback；D047 是 observation-only 动作族记录；F4-C 只证明 final relabel=PI-BER；P05 只解决其 dual-pol swap slice。它们不被扩大为领域负面。
- 未下载/精读全文，未验证公式、实现、总预算或 baseline 是否已解决未来 defect；本裁决只到摘要支持的核心动作身份与 Step 1 corpus 充分性。

## T006 master verification list（历史 v1）

- [x] fresh validator `PASS`
- [x] 65 rows 全量合并，46 unique，39 published，6 must-read
- [x] C1 official arXiv abstract 与 C2 S2 full abstract 独立核证
- [x] TSP 2006 从 route exact 降为 `STRONG_NEIGHBOR`
- [x] replacement 门允许并实际输出 0
- [x] 无 broad search、全文、实现、实验或 owner 更新

## T007 evidence repair / T008 current v2.1 receipt

> 2026-08-09 | T008 + D004 semantic correction | mirror coverage: `28/28` | integrated schema: `coded-decoder-step1-integrated.v2.1`

- 原始 28-result 自动镜像未覆盖写回；reviewed copy 保存为 `search-archive/2026-08-09/coded-decoder-c1-r1q0-aggregate-mirror-reviewed.json`。与 v1 integrated 的 exact overlap 为 **4**；另外 4 条截断题名/镜像页由本地 index 或摘要指纹解析为既有 alias，alias 与 provenance 均保留。Row 14 只有 possible-alias 线索，不满足冻结去重键，故保留为独立记录。
- 逐条 disposition：`DUPLICATE=8`、`IRRELEVANT=10`、`CORE_ACTION_EXACT=0`、`STRONG_NEIGHBOR=4`、`BASELINE=2`、`UNKNOWN=4`。UNKNOWN 为 row 12/19/24/27；现有 metadata/abstract 均不足以识别一个 carrier-recovery action，因此它们没有形成 corpus-backed replacement，但未被强行标为 irrelevant。
- integrated v2.1 合并全部 C1/C2 prefixed route JSON 与 reviewed mirror：**93 raw annotated → 66 hierarchical unique**；正式发表 **50/66=75.76%**；必读 **6**；source families **7**；C1/C2 R2 coverage 均为 **2/2**。完整 raw rows、canonical keys、aliases、route membership、priority、publication/source、collision/replacement relevance 与 provenance 均保留在 JSON。
- 镜像新增的可行动线索只有 row 13/14/20/22，分别落在 LDPC-feedback/message-passing/soft-decision PLL/iterative synchronization 的 C2 同动作邻域；row 7/17 只支持 conventional/code-assisted baseline。未发现与 C1/C2/C3/D047/P08/P05/CCISP/Ch5 不同且有 corpus evidence 的 carrier-recovery action。
- C1/C2 collision 继续成立；replacement 仍为 **0**。D003 的 local terminal 保持 `STEP1_NO_METHOD_ACTION_SURVIVOR`；D004 撤销其 `NO_VALID_PROBLEM` 映射，改记 `problem disposition=NOT_EVALUATED_NO_Q_FORMED`。本 receipt 未授权 Step 2、全文、adapter、实现或实验。

## D004 semantic correction

Step 1 的证据只支持“两张候选动作均 collision、replacement=0、候选集耗尽”。`stages/glossary.md` 的 Problem 必须是 Step 3 形成并逐项审查的 M-C-A 四判据对象；本轮没有 Q#，不能把 action survivor=0 改写为 problem invalid。当前唯一科学 terminal 仍为 `STEP1_NO_METHOD_ACTION_SURVIVOR`，问题层结论为 `NOT_EVALUATED_NO_Q_FORMED`。
