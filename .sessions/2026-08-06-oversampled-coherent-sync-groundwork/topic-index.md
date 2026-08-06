# Topic Index: 过采样相干 FSO 联合同步前端 Groundwork

> 状态: closed | 创建: 2026-08-06 | 最后更新: 2026-08-06（D005/V004/H001：Step 3 无 canonical survivor，验收与交接完成）

## 专题信息

- **slug**: `2026-08-06-oversampled-coherent-sync-groundwork`
- **title**: 过采样相干 FSO 联合同步前端 Groundwork
- **性质**: 承接 RDL system D028 的正式 Groundwork 专题；执行 GW Step 1，只有硬门通过才执行
  Step 2，并停在用户覆盖面确认门。

## 范围边界

### 原始目标（冻结）

判断“含脉冲成形、过采样、分数定时偏差、采样钟偏差/漂移、帧偏移、频偏和相位噪声的
相干 FSO 接收机同步前端”能否形成至少两个机制有区别、物理量级可溯源、具有 2019+ 合法
baseline 且不与既有 CCISP 动作碰撞的候选研究问题。

### 当前范围

- Phase 0：依据 D023 与 T004/T005 commit/产物修订当前 inventory，不改历史；
- GW Step 1：优先复用本地索引/全文，新增 query 最多 6 组，覆盖 timing/SCO、frame+CFO、
  turbulence/fade 下同步维护三类；
- 静态评估新增 testbed 的最小模块与工程量，不写代码、不运行仿真；
- 只有 Step 1 未触发停止条件且至少两个机制不同 Q# 预卡存活，才执行 Step 2；
- Step 2 至少 5 篇 CORE 全文，逐篇完成 identity/provenance/SHA256/≥50 行质量门，随后停在
  `STEP2_READY_FOR_USER_CONFIRMATION`；用户已接受该覆盖面并授权进入 Step 3。
- GW Step 3：通过子 agent 精读 7 篇 CORE，Q1/Q2 分别形成 M-C-A 与 canonical 四判据；只有至少一个
  Q# 全过，才进入 Step 3.5。
- GW Step 3.5：只针对 Step 3 survivor 做最多三轮定向补检索、最高相关竞品双向引用链筛查，以及
  JOCN 2026 全文有界重试；完成后停止。

### 明确不含

- 不进入 Step 4a、Contract、方法实现、testbed、MVE 或仿真；
- 不预设所有 impairment 必须同时进入最终问题，不以标题联想或场景换名造 Q#；
- 不使用 TX payload truth 作部署决策；pilot/preamble 仅作为显式开销的 receiver-known 信息；
- 不以极端参数制造问题，不用“旧 caller 没有该问题”直接否决新 testbed；
- 不修改 `projects/simulation/common/`、`params.py`、旧 raw/result 或四个 `p05_run*.log`；
- 不 push；本对话只做一次最终 commit。

### 范围变更记录

- **[2026-08-06] D004**：接受当前 7 篇 CORE 覆盖面，解除 Step 3 禁令，并仅在至少一个 Q# 通过
  canonical 四判据时进入 Step 3.5。
  - 原因：用户明确接受 JOCN 2026 全文缺口作为 Q1 的 `HIGH_RISK` novelty/collision blocker，要求按
    Step 3→条件式 Step 3.5 推进。
  - 新范围：精读 7 篇 CORE；Q1/Q2 分开裁决；survivor 存在时执行最多三轮 Step 3.5；随后停止。
  - 影响的未决项：JOCN 2026 若 Step 3.5 后仍无全文，Q1 不得声称 exact-action novelty closure。

## 已确认结论

### 不变量

- 调制优先 QPSK/16QAM；waveform 包含 RRC pulse shaping 与至少 2 samples/symbol。
- impairment 候选包括 fractional timing offset、sampling-clock offset/drift、frame offset、CFO、
  Wiener phase noise 与 Gamma-Gamma fading；最终问题可只保留其中经证据支持的子集。
- 参数量级与星地/相干 FSO 相关性必须有真实文献依据。
- Step 1 只做问题预判，不声称 glossary 四判据已由全文精读闭合。
- Step 1 terminal 是硬门；无至少两个机制不同候选 Q# 时不得进入 Step 2。
- Step 2 后必须停在用户覆盖面确认门，不得自动进入 Step 3。
- D004 已满足该用户确认门；本轮唯一允许的推进为 Step 3 与条件式 Step 3.5，终态不得越过 Step 4a 入口。

### 其他结论

- Step 1 共 6 组 query、140 raw / 130 unique、2019+ 39 unique；Q1 acquisition 与 Q2
  maintenance/reacquisition 两张机制不同预卡存活，但都未完成四判据闭合。
- Step 2 核验 7 篇 CORE 全文。JLT 2025 最近直接竞品已补齐：其 clock recovery 与 frame/FOE 是
  TS-A/TS-B 顺序分区动作，无 SCO；泛化 preamble claim 已占用，但未证实 sample-level 联合动作碰撞。
  JOCN 2026 三路径获取失败；用户已接受该缺口进入 Step 3，当前继续保留为高风险全文缺口。
- Q2 有真实 SCO/timing/carrier/fade 物理动机，但双环共同失锁、恢复时间与联合动作增益仍是量化缺口。
- 完整 testbed 约 11–14 日；Q1/Q2 最小切片分别约 5.5–7.5 日和 7–9 日，均非完整平台重建，
  不触发 `TESTBED_SCOPE_EXCESSIVE`。
- 用户接受 7 篇 CORE 覆盖面；JOCN 2026 全文缺失保留为 Q1 `HIGH_RISK` blocker，不阻止 Step 3，
  但禁止用摘要作全文裁决或宣称 exact-action novelty closure。
- Step 3 的 7 篇全文均完成身份/方法/实验/问题结构化提取；Q1 判据 1 FAIL，Q2 判据 1/3 FAIL。
- Step 3 survivor=0；Step 3.5 条件门未触发，JOCN 2026 未新一轮获取。
- 当前 terminal：`STEP3_NO_VALID_PROBLEM`；唯一 survivor：无。

## 进展线索

- **S001**：专题建立、范围冻结、Phase 0 authority reconciliation 与 GW Step 1–2 执行入口。
- **D001**：冻结研究对象、Step 1 停止条件、条件式 Step 2 与禁止边界。
- **D002**：首次 6-CORE 接收结论，已由 V001 否决并被 D003 取代。
- **D003**：补入 JLT 2025 最近直接竞品后，以 7 CORE 重裁 Step 2；JOCN 2026 缺口显式留给用户确认。
- **D004**：用户接受 7 CORE 与 JOCN 缺口条件，授权 Step 3→条件式 Step 3.5，并冻结本轮终止边界。
- **D005**：Q1/Q2 均未通过 canonical 四判据；Step 3.5 不触发，本专题停在 Step 3。
- **V001–V003**：Step 1–2 独立验收从 FAIL→PARTIAL→PASS。
- **V004**：Step 3 初审 4 阻断项，最小修复后完整复验 PASS；科学裁决与状态链均通过。
- **H001**：交接 `STEP3_NO_VALID_PROBLEM`、Q1/Q2 失败机制、JOCN 债务和唯一合法恢复条件。
- 项目证据：`literature_notes_oversampled_sync.md`、Step 1 report/receipt、Step 2 coverage/receipt、
  `testbed-bom.md`。

## 未决项

- 若未来由用户显式扩大/重启范围，是否从扩关键词重新检索以寻找顺序链失效或双环共同失锁证据；
- JOCN 2026 全文仍未取得，但当前不触发继续获取。

## 当前位置

Phase 0、GW Step 1–3 已完成；terminal=`STEP3_NO_VALID_PROBLEM`。Step 3.5 未触发，无 Step 4a 入口。
专题已验收并交接后关闭。没有自动科学动作；任何新检索、问题重构或重启都需要用户在后续对话
显式 scope-change 授权。
