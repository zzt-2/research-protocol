# [S003] 5 个真实 shadow 工作循环观察

> 2026-07-17 | 观察与独立复核 | PARTIAL

## 目标

在冻结的 pilot v1（提交 `44adff7`）上完成 H003 要求的 5 个真实 shadow 工作循环，记录主动路由、证据状态、负担、误拦/漏拦、STALE/ORPHAN 传播及正式材料边界；观察期内不修改 controller、schema 或提示词护栏。

## 记录

- 隔离目录：`projects/simulation/verify/direction_lab_pilot/runs/stage3-2026-07-17-shadow/`。
- 5 个主循环依次覆盖：`RUN → GO → KILL → PROMOTE（应阻断）→ REUSE_RESULT（组件漂移后应 STALE）`；另加一个缺失 receipt 的 ORPHAN probe。
- 每个主循环均带 `run_id`，读取 2 个输入文件、14 个 manifest 字段；未经提醒的 controller 路由为 5/5 = 100%。
- 进入 trusted evidence：evidence ledger 2 条、promotion board 1 条；PROMOTE 被 BLOCKED，STALE/ORPHAN 均拒收，P0 违规进入证据链为 0。
- 未发现新型绕过、目录越界写入或正式材料/性能数字泄漏；结果摘要均为 `metric_summary=omitted`。
- `recovery-check.json` 证明新 controller 实例可重载 audit 并完成一次 trusted RUN，但不是跨上下文恢复样本；H003 要求的至少 3 次恢复仍未覆盖。

因此本轮结论为 `PARTIAL`：核心 5-cycle 行为、P0 隔离和材料边界 PASS，恢复能力未达阈值。

## 决策引用

- D001：采用审计账本背书的最小 decision receipt 与 evidence gate
- D002：execute 结果必须有审计 execution 记录并防止 replay

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

保持 pilot v1 冻结，不改 controller/schema。后续若继续观察，应专门补足至少 3 次跨上下文恢复样本，再评估是否进入正式 registry/schema 设计。
