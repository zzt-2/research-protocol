# GW Step 3.5：Q1 定向补检索、引用链与竞争闭包

> 日期：2026-08-06
> 入口：formal D006，Q1=`STEP3_SURVIVOR`
> 边界：只完成 Step 3.5；未进入 Step 4a、方法实现、testbed、MVE 或仿真。

## 1. 检索轮次与收敛

Round 1 按 3 类方法变体×2 个问题组合完成 6/6 query，得到 100 archive rows / 80 cross-query
unique，筛出 must=5、should=6。Round 2 只针对“同一 objective 输出 frame/burst position、fractional
sample timing/phase 与 CFO”的缺口执行 3/3 focused query，得到 27 rows / 25 unique；相对 Round 1、
引用链与已读 guard 的真正新增 must=0、should=0。满足 `gw-supplement.md` 的收敛判据，未启动 Round 3。

证据：`step-3-5-sync-search.md`、`step-3-5-sync-search-r2.md` 与 9 个 `step35-r{1,2}-*.json`。

## 2. Sun 2025 双向引用链

- 前向 8、后向 35，共 43 条；43/43 含 OpenAlex strict citation graph，S2-only=0。
- 前向最高风险项：JOCN 2026 `10.1364/JOCN.587273`。
- 后向新增最直接候选：JLT 2025 `10.1109/JLT.2025.3528909` / arXiv `2410.10080v1`。
- 技术血缘：CAZAC/周期相关序列 → burst FOE → training-aided CE → FS/SOP/FOE preamble →
  fast-convergence burst DSP → multi-action shared preamble。

证据：`step-3-5-sync-citations-jocn.md` 与 `sun-2025-{forward,backward}-citations.json`。

## 3. 新高相关论文 acquire→read

| 论文 | 全文门 | action-level 结论 | 对 Q1 的影响 |
|---|---|---|---|
| Zhou et al., JLT 2025, `10.1109/JLT.2025.3528909`, arXiv `2410.10080v1` | PASS；555 行；SHA `a767b560...3ffe5` | `Preamble A burst detect/coarse CFO → SOP → SPO init+fine CFO → Preamble B frame → CE`；分区 preamble 的顺序模块链 | 当前最强直接顺序 comparator；不构成 exact joint `(frame, fractional τ, CFO)` collision |
| LPT 2017, `10.1109/LPT.2017.2759584`, arXiv `1801.01598` | PASS；156 行；SHA `5e4d7832...9aae7` | 两条 chirp FRFT peak + 2×2 coupled solve，真 joint `(integer frame offset,CFO)`；入口已 1 sps，无 fractional τ/SCO | 强方法近邻；占用 joint frame/CFO，不占三参数 exact action |
| Du et al., JLT 2021, `10.1109/JLT.2020.3042546` | PASS；712 行；SHA `6a0c5a20...b84731` | joint ML `(τ,CFO,CPO)`；无 frame output，输入为 CP-removed OFDM symbol，τ 为 circular integer-sample TO | 真 joint 方法先验；Q1 不得声称 generic first joint timing/CFO，但无 exact collision |
| JLT 2025 IQ-skew, `10.1109/JLT.2025.3581618` | 三路径后无全文 | 摘要多动作列表不能裁单一 objective 或 fractional τ | `UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`，高风险 blocker |
| JOCN 2026, `10.1364/JOCN.587273` | downloader FAIL；arXiv exact 0；blit 对 Optica N/A | 摘要只支持 single preamble 的 frequency-domain clock 与 time-domain frame/FOE/SOP，多动作耦合未决 | `UNRESOLVED_HIGH_RISK`，exact-action blocker |
| OE 2025 `10.1364/OE.566136` / JOCN 2021 `10.1364/JOCN.402591` / OQE 2024 `10.1007/s11082-024-06850-5` | 合法路径后无全文 | 不用摘要作 positive/negative exact-action 裁决 | coverage gaps；不改变当前 claim ceiling |

全文精读证据见 `papers/_read_notes/2410.10080v1.md`、`1801.01598.md`、
`10.1109_jlt.2020.3042546.md`；acquisition/read receipts 见 T008–T010 worker logs。

## 4. 三类语义边界与 collision

1. **generic shared-preamble/resource reuse**：同一 training unit 支持多个模块，但不同字段、域、metric 或
   output。Sun 2025、Zhou 2025 与 JOCN 2026 摘要级信息属于此类或待全文细分。
2. **sequential timing/frame/CFO**：模块按顺序估计和补偿。Zhou 2025 与 Le Bidan 2023 是当前最强
   task-matched 顺序链。
3. **真正 joint estimator**：单一 objective/search 耦合多个参数。LPT 2017 提供 `(integer frame,CFO)`，
   JLT 2021 提供 `(integer τ,CFO,CPO)`；当前全文池没有同信息、同动作、同任务的
   `(frame index,fractional τ,CFO)` estimator。

因此，本轮**未发现已确认的 exact-action collision**；但 JOCN 2026 与 JLT 2025 IQ-skew 全文缺失，
exact-action novelty closure 仍 blocked，不能声称“首次”或“无竞品”。

## 5. 最强廉价 comparator closure

Q1 的最低合法 comparator 冻结为：

`polyphase/Farrow fractional-delay bank → Zhou 2025 Preamble-A burst detect/coarse CFO/SPO init/fine CFO →`
`Le Bidan timing/interpolation/FSE/downsample → Zhou/Sun CAZAC frame+FOE/CE`，并以 FSTS/STSB 作为
FSO frame/FOE 子链替代实现。

该 composite 是公平对照合同，不是某一篇论文的虚构身份。它关闭了“共享 preamble、模块调序、简单
timing phase bank 就足以解释收益”的廉价替代；并未证明 Q1 的 A 为真，problem-truth 仍属于 Step 4a。

Q2 的 shared-freeze+fixed-restart 同样只是公平 comparator contract。7 CORE + 三源补检索未找到 2019+
integrated timing+carrier maintenance/reacquisition baseline，故 Q2 判据 3 仍 FAIL。

## 6. Survivor、collision 与 terminal

- Q1：保留 `STEP3_SURVIVOR`；Step 3.5 未发现确认的 exact collision，但存在两个 primary-fulltext blocker。
- Q2：判据 1/2/4 PASS、判据 3 FAIL；非 survivor。
- terminal：`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`。
- claim ceiling：可说“Q1 是完成 Step 3.5 的问题候选，当前全文池无 exact-action collision”；不可说
  exact-action novelty 已闭合、METHOD_SIGNAL、Go、论文方法成立或 Step 4a problem truth 已证实。

## 7. 下一合法动作

优先由用户提供或通过新合法 OA/preprint 入口取得 `10.1364/JOCN.587273` 与
`10.1109/JLT.2025.3581618` 全文并完成 action-contract 精读；或由用户显式接受这两个 primary-fulltext
缺口。只有该覆盖面门被处理后，另起会话重读 `stages/gw-feasibility.md`，才可讨论是否进入 Step 4a。
