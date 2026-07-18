# Direction Lab 实施摘要

> 2026-07-18 | 控制面收口；暂停新增候选、B004、新仿真和框架扩展

详细执行规范见 [process.md](process.md)。本文件只记录已完成里程碑、当前候选和下一动作。

## 已完成里程碑

- Candidate Universe、CandidateMap 和共享合同批次机制已建立；现有地图是开放索引，不是候选全集证明。
- B001–B003 已在隔离目录完成；B003 已通过 completion event + reducer 写入 canonical projection。
- B001–B003 均为 sandbox/exploratory evidence，不产生 formal promotion 或论文资格。
- P03 Interface Closure 已完成：真实 standard-CMA z-window、CSI_NONE、同信息量 analytic comparator、residual artifact、deterministic smoke 与 source closure 均通过。

## 当前候选状态

- P01/U25：`DEFERRED_ARCHITECTURE`。缺 receiver state/action hook/fork replay，不修补 U24 runner。
- P02/U10：`NOT_RUNNABLE`。缺双偏振 carrier impairment → CPR → receiver event chain。
- P03/U19：`P03_SCOUT_CONTRACT_READY`，Sandbox `NOT_ENTERED`。当前唯一研究主线。

## 下一唯一合法动作

P03 residual headroom probe：

`真实 standard-CMA 输出 → 同信息量 analytic comparator → residual headroom`

退出规则：

- analytic comparator 覆盖 ≥90% 可见 headroom：停止 P03，不训练 ML；
- residual mismatch 稳定存在：才建立新的 Sandbox batch；
- residual artifact 不稳定：P03 退回，不增加模型。

## 当前禁止

- 不启动 B004，不创建正式性能 cell；
- 不修改或重跑 B001/B002/B003；
- 不新增候选、不训练 ML、不继续扩展框架；
- 不创建 PASS Queue 或把 candidate component 伪装成 canonical；
- 不把 B001–B003 或 smoke 数字写入论文、正式 Groundwork 或 evidence ledger。
