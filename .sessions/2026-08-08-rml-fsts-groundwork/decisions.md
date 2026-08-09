# Decisions — RML-FSTS Groundwork

## D001: 冻结独立 Groundwork 专题范围与证据语义

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：调研: 上游 R002 + 决策: 上游 D004 + handoff: 上游 H003 + 任务合同: T003
> 触发原话: 无（技术推导）

### 决策

在独立专题 `2026-08-08-rml-fsts-groundwork` 中仅执行 Groundwork Step 1–2，并在 Step 2 覆盖面报告后停止等待用户确认。

### 理由

上游只把 RML-FSTS 选为 defect-reproduction Groundwork 入口，未证明目标星地 defect、未形成 Q# 或方法；正式 Step 1–2 是建立文献池和全文覆盖的最小合法动作。

### 排除的替代方案

- 不从上游 entry screening 直接运行 smoke、实现、仿真或进入 Step 3/3.5/4a。
- 不把 source-domain fixed-lag condition-dependence 偷换成目标 FSO lag-ranking crossover 已成立。
- 不削弱未来 comparator：保留 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。
- 不并行 BUM-CMA，不补新 research object，不复活 exact historical object。

### 影响范围

创建本专题 topic-index/S/R/D/V/H、RML-FSTS literature owner、Step 1/2 receipts 与 coverage report；同步 thesis-fso master-state；上游控制专题转 dormant current-view owner。科学代码、仿真参数、正式论文、旧 dormant topic 与 protected history不变。

### 来源

S001 / T003 / 上游 D004、R002、H003。

## D002: Step 1 PASS 与 Step 2 覆盖终态

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：R001 + R002 + Step 1 search receipt + Step 2 acquisition receipt + coverage report
> 触发原话: 无（技术推导）

### 决策

冻结 Step 1 terminal=`STEP1_PASS`，Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。当前在覆盖面用户确认关口硬停止；Step 3 保持 `NOT_STARTED`。

### 理由

Step 1 的 7/7 query、121 unique、4 actual sources、58.68% 正式发表比例和路线门均通过；Step 2 有 5 篇合格 CORE，C1–C4 四类齐全。READY 仅是获取覆盖门，不是 target defect、Q#、方法或 novelty 判断。

### 排除的替代方案

- 不因 5 篇失败全文关闭 research object，也不把下载缺口计作 object/package failure。
- 不把 metadata/abstract 或 C3 无线场景结论外推为 coherent-FSO target fact。
- 不自动进入 Step 3/3.5/4a，不运行 smoke、实现或仿真。

### 影响范围

更新新专题 current view、RML-FSTS literature owner 与 thesis-fso master-state；上游专题只保留 current-view 交接。object/package failure 仍为 `0/0`。

### 来源

S001 / R001 / R002 / coverage report / T003。

## D003: 用户确认覆盖面后仅授权 Groundwork Step 3

> status: active
> date: 2026-08-09
> 取代：无（执行 D002 用户确认关口通过后的合法分支；不改写 Step 1/2 历史事实）
> 被取代：无
> 依据：调研: R002 + 决策: D002 + 用户确认: 2026-08-09 对当前 5 篇 CORE 覆盖面回复“行”（零信息应答，按 voice 规范不收录）
> 触发原话: 无（用户以零信息“行”确认覆盖面与进入 Step 3，按 voice 规范不收录）

### 决策

将本专题当前范围从正式 Groundwork Step 1–2 扩大到 **仅执行 Step 3**：以当前 5 篇合格 CORE 为冻结输入完成全文精读；到 Step 3 完成或阻塞状态停止，不进入 Step 3.5。

### 理由

D002 要求的 Step 2 用户覆盖面确认已经满足。当前五篇全文达到 Step 3 的最低数量门并覆盖 C1–C4；用户接受其已披露的谱系偏斜与缺失竞品债务，因此下一合法动作是按 `stages/gw-read.md` 完成事实提取和 canonical 问题清单，而不是补跑 smoke 或提前做 novelty/可行性裁决。

### 排除的替代方案

- 不把用户确认解释为 target lag-ranking crossover、conditioned single-lag failure、novelty、Q#、Go 或方法已成立。
- 不在同一任务进入 Step 3.5、Step 4a、smoke、future action 设计/实现、仿真、MVE、Contract 或 Execute。
- 不用 `problem_truth/actionability/novelty/thesis_fit` 取代 glossary canonical 四判据。
- 不从缺失论文的标题/摘要推导公式、失效机制或实现细节；Tang/WiSEE provenance 修复前不计 CORE。
- 不在无 canonical Q# 全过时自造 Step 3 terminal；保持 `BLOCKED/IN_PROGRESS` 并返回框架规定的搜索恢复路径。

### 影响范围

新建 S002/T001；更新本专题 topic-index、registry、`projects/thesis-fso/master-state.md` 与 `literature_notes_rml_fsts.md` 到 `STEP3_DISPATCH_READY`。不修改论文正文、科学代码、仿真参数、旧专题或四个 `p05_run*.log`。

### 来源

S002；用户在 Step 2 覆盖面确认关口的回复；R002/D002/coverage report。

## D004: Groundwork Step 3 completed 并在边界停止

> status: active
> date: 2026-08-09
> 取代：无
> 被取代：无
> 依据：调研: R003 + 验证: V002 + 全文证据: 五篇 fresh reader logs + receipt
> 触发原话: 无（技术推导；本轮用户消息为纯操作指令，按 voice 规范不收录）

### 决策

Groundwork Step 3 标为 `✅ completed`：五篇冻结 CORE 全文完成，canonical target-relevant Q# 共 1 条且四判据 4/4；本轮在 Step 3 边界停止。

### 理由

5/5 source preflight、标准字段、7 子表、通信参数、实验完备性、三篇写作架构和 owner/read-note/read-log/receipt 均闭合。Q1 的 M/C/A、方法产出形态、近期 baseline 与量化对标同时满足 glossary canonical 四判据；A 保持可证伪的 target inference，不要求 Step 3 已用 MVE 证明。

### 排除的替代方案

- 不增加 `problem_truth/novelty/actionability/thesis_fit` 语义门。
- 不把 Q1 通过写成 target defect、novelty、Go、METHOD_SIGNAL 或方法成立。
- 不以 Morelli/Yu/Paillier 证明 coherent-FSO target defect。
- 不进入 Step 3.5/4a，不运行 smoke、实现、仿真、MVE、Contract 或 Execute。

### 影响范围

更新 R003、literature owner、五篇全局 read-note、read-log、receipt、topic-index、registry、master-state、V002 与 H002。Step 3.5 保持 `NOT_STARTED`；object/package failure 保持 `0/0`。

### 来源

S002 / R003 / V002 / T001。
