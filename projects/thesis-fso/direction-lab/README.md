# Direction Lab：双偏振星地 OSL 研究探索入口

Direction Lab 用共享地基批量筛查“ML 在双偏振星地 OSL 接收链上是否有真实信息增量”。它分为 Scout、Sandbox 和 Promotion 三层；这里的结果不会自动修改 canonical baseline、正式 Groundwork 或论文材料。

## 当前状态

- 正式研究：`BLOCKED`，唯一正式入口为 [`../master-state.md`](../master-state.md)。
- Sandbox 历史：B003 已完成并独立验证；批次事实见 [`state/completion-events.jsonl`](state/completion-events.jsonl) 与 [`state/projections/`](state/projections/)。
- 当前 Scout：P03/U19 residual-aware detection。
- P03 状态：`P03_SCOUT_CONTRACT_READY`；只证明 CSI_NONE 接口、同信息量 comparator、residual artifact 与 deterministic interface smoke 已闭合，Sandbox 仍 `NOT_ENTERED`。
- B004：不存在，也不允许启动。

`canonical-state.yaml` 只物化 Direction Lab Sandbox 的机器投影，不代表正式研究授权，也不能单独充当批次历史证据。其 `BOARD_READY` 仅表示全局 board/controller 基础设施可用，不授予当前 P03 创建 Queue、Registry 或执行 Sandbox batch；批次 provenance 以 completion events 和不可变 projection 为准，正式状态与研究入口始终以 `../master-state.md` 为准。

## 已完成批次

- B001：历史 sandbox，存在协议偏差，只保留探索证据。
- B002：sandbox verified。
- B003：sandbox verified；主要价值是治理链验证，与 B002 的 U24 exact contract 研究信息重复。

B001–B003 的任何数字都不能进入论文、正式 Groundwork 或 canonical baseline。

## 当前阻断

P03 还没有回答“同信息量解析对手之后是否存在稳定 residual headroom”。因此没有 ML 训练许可、没有 PASS Queue、没有新 Registry，也没有 Sandbox 批次许可。receiver-estimated CSI 仍为 `DECLARED_NOT_BOUND`。

## 下一唯一合法动作

执行 P03 residual headroom probe：

`真实 standard-CMA 输出 → 同信息量 analytic comparator → residual headroom`

- 解析对手覆盖可见 headroom ≥90%：停止 P03，不训练 ML。
- residual mismatch 稳定存在：才设计新的 Sandbox batch。
- residual artifact 不稳定：P03 退回，不继续加模型。

这一步不是 B004，也不是正式性能实验。

## 入口文件

- 正式项目状态：[`../master-state.md`](../master-state.md)
- Direction Lab 机器投影（非授权、非批次历史事实源）：[`canonical-state.yaml`](canonical-state.yaml)
- 批次状态事实源：[`state/completion-events.jsonl`](state/completion-events.jsonl) 与 [`state/projections/`](state/projections/)
- 当前 Scout 分诊：[`scout/capability-triage.v1.yaml`](scout/capability-triage.v1.yaml)
- P03 当前合同：[`scout/P03-U19-residual-headroom/scout-contract.v2.yaml`](scout/P03-U19-residual-headroom/scout-contract.v2.yaml)
- P03 readiness：[`scout/P03-U19-residual-headroom/readiness-report.yaml`](scout/P03-U19-residual-headroom/readiness-report.yaml)
- 详细流程规范：[`process.md`](process.md)
- 当前实施摘要：[`implementation-plan.md`](implementation-plan.md)
- 工作树只读审计：[`worktree-audit-20260718.md`](worktree-audit-20260718.md)
