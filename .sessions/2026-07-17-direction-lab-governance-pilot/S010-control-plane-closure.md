# [S010] Direction Lab 控制面收口

> 2026-07-18 | 治理里程碑 | COMPLETE / topic 转 dormant

## 目标

消除 formal、sandbox 和 Scout 三层状态冲突；修复入口文档和重复 session 编号；盘点 dirty worktree；明确下一唯一合法研究动作。不开 B004、不新增候选、不扩展框架。

## 记录

- formal research 保持 `BLOCKED`，由 `projects/thesis-fso/master-state.md` 作为唯一入口；Direction Lab 不产生 formal promotion。
- `canonical-state.yaml` 与 completion event 一致指向 B003；B002/B003 历史 hash guard 保持 PASS。
- P03 当前唯一状态为 `P03_SCOUT_CONTRACT_READY`；v1 合同保留旧 blocker lineage 并指向 current v2，capability triage、BatchPlan 和 readiness 已对齐。
- 后创建的重复 `S005-mechanism-coverage-and-batch-plan.md` 重编号为 S009；较早 `S005-process-spec-freeze.md` 保留。引用经确定性扫描修正。
- governance pilot 完成控制器、EvidenceGate、state reducer、恢复和真实 sandbox 压测；恢复阈值覆盖仍为 PARTIAL，因此 lifecycle 收口为 `dormant` 而不是 closed。
- dirty worktree 仅盘点，不清理、不 stage、不批量提交；并行对话修改仍保留在工作树。

## 决策引用

- D013：治理专题转 dormant，研究当前态回归项目目录；`.sessions` 以后只记里程碑、决策和交接（新建）。
- V019：控制面、P03 状态、历史保护、session 编号与 dirty worktree 只读审计均 PASS。

## 范围确认

- 本轮是否在 scope boundary 内：是。属于 governance pilot 的最终控制面收口，不是新的研究 Scout 微步骤。

## 后续

下一唯一合法研究动作由项目目录声明：P03 residual headroom probe。治理专题除非专门恢复未完成的恢复阈值验证，不再承载研究推进。
