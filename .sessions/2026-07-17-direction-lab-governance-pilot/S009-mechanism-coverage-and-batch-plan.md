# [S009] B003 状态对账、机制覆盖审计与后续 BatchPlan

> 2026-07-18 | Scout/状态治理 | COMPLETE（B004 禁止启动）

## 目标

用 append-only completion event + reducer 对账 B003，修正 canonical-state 的循环 provenance；对 Candidate Universe 做机制级覆盖审计；一次生成 3–5 个后续机制族 BatchPlan，但不启动 B004。

## 记录

### 1. 状态对账

B003 的旧 canonical bytes SHA=`821415346437f47de064966fdaa768242c63d2d660ea189e88a4a0dfb51995b0` 已保存为内容寻址 pre-state。新增 `state/completion-events.jsonl` 的首条事件绑定 B003 的 manifest/result/artifact/execution-status/ledger/verifier/synthesis；reducer 通过严格 sequence、prev hash、event hash、证据指针和 immutable-section 检查，生成 projection SHA=`5967ea38e676b46cb092c98060bec5b470b5a03625f21e65218cf3b2ae3a88af`。canonical-state 现为该投影视图，last completed 为 B003，completion history 保留 B002；B002/B003 历史文件没有改写。

循环根因是 `run_v3 → run_v2._source_files → canonical-state.yaml` 把可变状态投影当运行源码。未来 runner 必须把 pre-state projection/head 作为输入元数据，不把 mutable top-level projection 纳入 source closure；B004 暂不运行。

### 2. 机制级覆盖审计

v2 的 34/34 只说明 archetype 被分区到 8 个 family，不说明 application point × mechanism × information interface 完整。现有 archetype 缺 input source、causal timing、label/oracle boundary、output action、runtime IO 和 fingerprint；AP method tags 与实例 mechanisms 有差集，U10/U15 存反向不一致。审计新增 U35–U44 retained-neutral interface 候选，并定义四轴机制分类：监督、结构先验、适应控制、部署。

主要重复归并：U05/U11/pilot-Jones（若同一 pilot→Jones→inverse）；U12/U26（若只调步长/窗口）；U17/U30（deployment）；U19/U20（hard symbol vs calibrated LLR）；U23/U24（共享 backbone、不同输出 head）；U25/U31（safe recovery vs resource scheduling）。D031–D039 历史负证据缺口列为下一版 lineage 修正，不修改 v2。

### 3. 五批计划

| 计划批次 | 层级 | 当前状态 | 关键阻断 |
|---|---|---|---|
| P01 U25 action-contract | Scout | NOT_RUNNABLE | 无 action/replay/safety contract 与 fingerprint |
| P02 U10 event-library | Scout | NOT_RUNNABLE | 当前地基无 carrier phase/FOE/CPR 事件链，Map evidence 误映射为 SOP failure |
| P03 U19 residual headroom | Scout | NOT_RUNNABLE | residual evidence、legal CSI、analytic comparator 缺失 |
| P04 U20 coded LLR | Scout | NOT_RUNNABLE | LLR/coding/interleaver/decoder/GMI/FER 合同缺失 |
| P05 U25 safe fallback | Sandbox | BLOCKED_PENDING_P01 | 依赖 P01 通过及新 runner/registry/queue |

没有候选被 Go/Kill；U25/U10/U19/U20 均没有被默认标记为可运行。

## 决策引用

- D007：Direction Lab 三层机制族批量流程
- D008：completion event 事实源与 reducer 投影视图（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

下一轮只能在不启动 B004 的前提下补 P01 action/replay 接口和测试，或根据依赖状态切换到 P02/P03 Scout；未完成新候选的真实实现、输入合同、指标和 fingerprint 前，不得创建 PASS Queue。
