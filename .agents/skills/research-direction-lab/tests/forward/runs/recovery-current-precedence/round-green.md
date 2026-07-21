# GREEN fresh-agent run — recovery-current-precedence

- agent_id: `green_recovery_fresh2` (collaboration canonical task `/root/green_recovery_fresh2`)
- skill_access: current revised Skill loaded before response
- recording: verbatim final response

## Blind prompt

项目有旧 synthesis/handoff 说 candidate CLOSED 且有 thesis-grade negative，旧 raw artifact 可复现；之后 semantic review 用显式 amendment/invalidates 事件撤回解释并把 candidate 恢复为 UNRESOLVED；旧 handoff 的 mtime 比 amendment 更新。项目提供 STATUS、adapter、state/current、portfolio/current、harvest/current 和 append-only ledger。请说明恢复当前事实、读文件顺序、旧 artifact/旧结论如何处理、下一动作。只给你的实际回答，不修改文件，不描述评分标准。

## Raw response

恢复时先走当前事实热路径：

1. `STATUS.md`：确认规范入口、当前模式和指针。
2. 项目 adapter：恢复正式目标、授权、anchor/baseline、指标契约、受保护历史、命令与预算。
3. `state/current`：读取已应用 `amends / invalidates / restores` 后的机器当前状态。
4. `portfolio/current`：确认 candidate 当前为 `UNRESOLVED`，而非 `CLOSED`。
5. `harvest/current`：确认旧的 thesis-grade negative 已退出当前论文材料视图。

若这些 current projections 一致，就不做全历史考古。只有为核对修订链或处理冲突时，才定向读取 append-only ledger 中相关事件、semantic review、旧 synthesis/handoff 及其引用的 raw artifact。事实优先级由显式 disposition 决定，文件 mtime、篇幅和文风均不构成优先级；因此即使旧 handoff 更新时间更晚，也不能覆盖 amendment。

当前事实应拆开表述：

- 旧 raw artifact 仍可复现，其数值事实和 provenance pointer 保留，可归为 `VALID`。
- 旧的“candidate 已关闭”“形成 thesis-grade negative”属于已被 semantic review 明确 `invalidates` 的解释，归为 `INVALID`，不能继续进入当前 claim 或 thesis harvest。
- candidate 经 `restores` 后保持 `UNRESOLVED`。
- append-only ledger 不删除、不改写旧记录；保留 `CLOSED → INVALIDATED → UNRESOLVED` 血缘。`harvest/current` 只呈现修订后的当前消费状态。
- 当前 claim ceiling 仅为 `DIAGNOSTIC`：历史运行可复现，但其旧解释无效。

下一动作是在 adapter 预算和合法信息边界内做一个最小 semantic Probe，直接检查导致撤回的任务语义，例如 objective、label、output、metric 是否一致，trivial/no-op 是否会虚假通过，以及 comparator 是否合法且充分。Probe 只能决定是否值得重新进入 Scout，不能恢复旧 negative；若该语义问题无法在原科学契约内修复，则轮转到 `portfolio/current` 中另一个 READY candidate。

## Behavior scorer output

Post-hoc scorer verdict: PASS. Current-view order, explicit-lineage precedence, artifact/interpretation split, bounded history, and continuation checks passed.
