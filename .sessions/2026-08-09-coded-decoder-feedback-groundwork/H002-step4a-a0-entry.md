# Handoff: C1 进入 Step 4a A0 分析预检

> 来源: S001 | 交接目标: 围绕 canonical Q1 完成 A0 §0–§6，冻结假设、否决条件、物理/B2/testbed 合同后再决定是否开放 defect smoke
> 文件名: H002-step4a-a0-entry.md
> 日期: 2026-08-10

## 已完成边界

- D009/V003 已接收 Step 3.5：query matrix、双向引用链、physical/B2 补检与 3 轮上限均完成；两个 fresh-context verifier 均 `PASS, P0/P1/P2=0/0/0`。
- 正式 prior-art 上限为 `NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE`；Round 3 是 `0 MUST / 1 SHOULD`，形式终态 `ROUND3_CAP_REACHED_WITH_NEW`，唯一 OFC2017 已全文闭为 `STRONG_NEIGHBOR`。
- Q1 仍为 canonical 4/4；Step 3.5=`COMPLETE / VERIFIED_WITH_COVERAGE_LIMITS`。这不证明 defect occurrence、O1 recoverability、decoder observability、B2 未吸收或方法贡献。
- 当前控制面为 CP010/epoch 10，只开放 `GROUNDWORK_STEP4A_A0_PREFLIGHT` 的分析型动作；尚无 adapter、defect smoke、MVE 或 performance rows。

## 不要做什么

- 不把“未确认 exact collision”写成领域级 novelty，不把局部 repair 写成已成立方法。
- A0 §0–§6 未完成前，不跑 defect smoke/MVE，不写 adapter，不建通用 coded receiver 平台。
- 不把 OFC2014/ICTON synthetic slip rate 直接当 coherent-FSO 自然分布；不声称 JLT2020 turbulence/fading 导致 discrete slip。
- 不用 truth SNR、true phase/CFO/h/slip boundary、TX payload 或最终 correctness 驱动 deployable action。
- 不修改/暂存四个 `p05_run*.log`，不 push。

> 用户原话：“若没有 exact complete-chain collision，带限制进入 Step 4a；不得因仍有一两篇全文不可得自动 NO ENTRY。”

## 必读

1. `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`（CP010、不变量、未决项）
2. `decisions.md` D009 与 `verifications.md` V003
3. `projects/thesis-fso/master-state.md` 当前 bridge/GW Progress
4. `projects/thesis-fso/literature_notes_coded_decoder_feedback.md`
5. `projects/thesis-fso/coded-decoder-feedback-groundwork/step3_5-supplement-report.md`
6. `stages/gw-feasibility.md` A0 §0–§6、A'/A/B/D；进入 MVE 前必须再次重读维度 D
7. `thesis-lessons.md` 速查表与 TL-20/TL-22/TL-23/TL-25/TL-26/TL-27
8. `projects/thesis-fso/worker-logs/step-061-p08r2-coded-chain-fresh-audit.md`、step-070、075、081–083

## 接口变更（如有代码改动）

无。Step 3.5 只有文献、receipts、read notes、中央 owner 与治理文件；未改任何 simulator/decoder/caller/callee 接口。

## 失败数据附录（如涉及路线失败）

- 科学路线尚未失败；Step 4a 关键事实仍 UNKNOWN。
- 操作债：T034 首个 Round-3 agent 完成搜索 receipts 后超过 15 分钟且未落盘，已中断；salvage agent 只读 receipts 独立复算 `82→79→72, 0/1` 并写 step-080。该操作失败不作为科学证据，也未丢失 receipts。
- arXiv1704 初次 `UNRESOLVED` 是 downloader/read 竞态；后续正文 143,913 bytes、SHA receipt 已关闭，chronology 保留在 step-077。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| CSSC/CS-DC、U01/U02 全文不可得 | exact collision 必须以全文裁 | fail-closed；不能冻结算法/参数或吸收结论 | 若 Step 4a 发现 B2/链字段依赖其未知机制，先补来源或按未知上限裁 |
| PAPU exact equations 欠 2013 predecessor | baseline 实现必须身份/公式诚实 | 只允许 topology-matched independent implementation | 冻结 B2 代码合同前明确公式来源与偏差，不称 exact reproduction |
| coherent-FSO 自然 slip occurrence 未证 | 物理条件必须可溯源且不可为方法调参 | 只有 optical order 与 FSO fading/AO 参数锚 | A0/defect contract 必须分离 fading 与 injected discrete slip；无合法 slice 则 Kill |
| P08-R2 缺 carrier/action/local rollback | method adapter 必须有可调用合法 action | fresh audit 估计 5–6.5 日，`>7D_BLOCKER` 未成立 | A0 通过后重审 BOM；>7 日且无复用价值才 hard terminal |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| A0 §0 | Q1 对应 literature owner 且四判据 4/4 | `gw-feasibility.md` §0 / D008 | 当前 1/1 PASS |
| A0 §1/§6 | 给出带来源类型的 B0/B1→O1 headroom 与 strongest simple-prior 覆盖；无来源数字不得承重 | `gw-feasibility.md` A0 §1/§6 | 未执行 |
| A0 §2–§5 | 非 ML method-type 下逐项给出适配/跳过理由、相邻先例与负面证据；任一真实致命信号即 STOP | `gw-feasibility.md` A0 | 未执行 |
| 控制晋级 | A0 §0–§6 全部审计、假设/否决条件/testbed/B2合同冻结，且独立审查无 P0/P1 | D009/FR-22/P6 | 未执行 |
| 保护边界 | p05 SHA 4/4、staging 不含 p05、无 truth-leakage action | 用户合同/V003 | 历史检查均 4/4；Step4a 未执行 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
  - 声称 1：V003 两路 verifier 均 `PASS 0/0/0` → 验证结果：待接收方填写
  - 声称 2：Round 3=`82→79→72, 0/1` 且 OFC2017 全文闭债 → 验证结果：待接收方填写
  - 声称 3：当前未运行 adapter/defect smoke/MVE/performance experiment → 验证结果：待接收方填写
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

先完成 Step 4a A0 §0–§6 的书面预检：以 Q1 的 M/C/A 为唯一对象，建立理论可恢复性上界、strongest B2/先验覆盖、physical/testbed factorization、receiver-visible decoder observability 假设与量化否决条件。只有该包通过独立审查，才建立下一 CP 开放最小 defect smoke；否则按 A0 直接 Pivot/Kill。
