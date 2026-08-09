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
