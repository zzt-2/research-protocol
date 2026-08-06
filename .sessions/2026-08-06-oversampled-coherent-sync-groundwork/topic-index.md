# Topic Index: 过采样相干 FSO 联合同步前端 Groundwork

> 状态: active | 创建: 2026-08-06 | 最后更新: 2026-08-06（D003：最近直接竞品补齐；Step 2 等待用户确认）

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
  `STEP2_READY_FOR_USER_CONFIRMATION`。

### 明确不含

- 不进入 Step 3、Step 3.5、Step 4a、Contract、方法实现、MVE 或仿真；
- 不预设所有 impairment 必须同时进入最终问题，不以标题联想或场景换名造 Q#；
- 不使用 TX payload truth 作部署决策；pilot/preamble 仅作为显式开销的 receiver-known 信息；
- 不以极端参数制造问题，不用“旧 caller 没有该问题”直接否决新 testbed；
- 不修改 `projects/simulation/common/`、`params.py`、旧 raw/result 或四个 `p05_run*.log`；
- 不 push；本对话只做一次最终 commit。

### 范围变更记录

- 无。

## 已确认结论

### 不变量

- 调制优先 QPSK/16QAM；waveform 包含 RRC pulse shaping 与至少 2 samples/symbol。
- impairment 候选包括 fractional timing offset、sampling-clock offset/drift、frame offset、CFO、
  Wiener phase noise 与 Gamma-Gamma fading；最终问题可只保留其中经证据支持的子集。
- 参数量级与星地/相干 FSO 相关性必须有真实文献依据。
- Step 1 只做问题预判，不声称 glossary 四判据已由全文精读闭合。
- Step 1 terminal 是硬门；无至少两个机制不同候选 Q# 时不得进入 Step 2。
- Step 2 后必须停在用户覆盖面确认门，不得自动进入 Step 3。

### 其他结论

- Step 1 共 6 组 query、140 raw / 130 unique、2019+ 39 unique；Q1 acquisition 与 Q2
  maintenance/reacquisition 两张机制不同预卡存活，但都未完成四判据闭合。
- Step 2 核验 7 篇 CORE 全文。JLT 2025 最近直接竞品已补齐：其 clock recovery 与 frame/FOE 是
  TS-A/TS-B 顺序分区动作，无 SCO；泛化 preamble claim 已占用，但未证实 sample-level 联合动作碰撞。
  JOCN 2026 三路径获取失败，保留为用户必须确认的高风险全文缺口。
- Q2 有真实 SCO/timing/carrier/fade 物理动机，但双环共同失锁、恢复时间与联合动作增益仍是量化缺口。
- 完整 testbed 约 11–14 日；Q1/Q2 最小切片分别约 5.5–7.5 日和 7–9 日，均非完整平台重建，
  不触发 `TESTBED_SCOPE_EXCESSIVE`。
- 当前 terminal：`STEP2_READY_FOR_USER_CONFIRMATION`。

## 进展线索

- **S001**：专题建立、范围冻结、Phase 0 authority reconciliation 与 GW Step 1–2 执行入口。
- **D001**：冻结研究对象、Step 1 停止条件、条件式 Step 2 与禁止边界。
- **D002**：首次 6-CORE 接收结论，已由 V001 否决并被 D003 取代。
- **D003**：补入 JLT 2025 最近直接竞品后，以 7 CORE 重裁 Step 2；JOCN 2026 缺口显式留给用户确认。
- **V001–V003**：独立验收从 FAIL→PARTIAL→PASS；最终只剩 JOCN 2026 全文缺口需用户确认。
- 项目证据：`literature_notes_oversampled_sync.md`、Step 1 report/receipt、Step 2 coverage/receipt、
  `testbed-bom.md`。

## 未决项

- 用户是否确认当前 7 篇 CORE 覆盖面，并接受 JOCN 2026 三路径失败这一高风险缺口；
- 是否补取 Gu 2019、OE 2022 timing baseline 与 JOCN 2026 全文；
- Q1 的 fractional timing/frame offset 分布与 Q2 的真实 fade 事件/SCO/双环失锁量化证据。

## 当前位置

Phase 0、GW Step 1 与 Step 2 已完成；terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。下一合法动作仅为
用户确认、补充或替换 CORE 文献。未经确认，Step 3 及以后禁止。
