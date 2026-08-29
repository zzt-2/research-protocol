# Task Brief: 修复 Ch5 residual bridge 的 provenance 与连续 scalar 时序

> 来源: S028 / D046 / T060 / T061 | 产出位置: `projects/simulation/explore/ch5-apsk-structured-covariance/` 与唯一对应测试
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 8
  action_class: TARGET_RESIDUAL_BRIDGE_CORRECTNESS
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格修复 T061 的两个 P1 与一个随附 P2：把 frozen Ch4 arm 的完整 canonical 数值快照纳入 deployable bundle/hash；把 Ch4 acquisition preamble 与 observation 放入同一个连续 shared-scalar→Jones→AWGN realization。只做 correctness 修复与回归测试，不运行 occurrence、性能、调参，不选择最优 Ch4 arm，不改 Ch4 方法、不新增损伤。

## 启动门与边界

1. 先运行 task-control validator；完整读取 T060、T061 报告、本 brief、现有 bridge/contract/tests/correctness smoke。
2. 本任务触发 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、`test-driven-development` 与 `verification-before-completion`。
3. 只允许改：`post_ch4_ch3_bridge.py`、`run_occurrence_smoke.py`、`occurrence_contract.yaml`、bridge tests、bridge correctness receipt/README（若直接语义受影响）和必要 usage log。不得改 `common/`、`params.py`、Ch4 core、Skill/controller、治理 owner 或论文正文。
4. 旧代码必失败的测试先行；不得先改实现再补绿测试。

## 修复 A：完整 frozen-arm provenance

1. Canonical snapshot 必须显式包含 `arm_id`、`mode`、`mu`、`ring_threshold`、`decision_threshold`，包括显式 `null`，不能只靠 `arm_id` 或 `ch4_gate_summary`。
2. Snapshot 必须进入 deployable bundle、`bundle_hash` 和 receipt required-field audit；改变任一数值配置必须改变 `bundle_hash`。
3. `realization_hash` 继续只表示物理 realization：相同接收 realization、不同 arm 参数时必须保持不变。
4. 新增同 `arm_id`、不同 `mu/threshold` 的直接回归；并验证 bundle snapshot 与实际调用参数一致、hash 覆盖 gate summary/canonical snapshot。

## 修复 B：连续 acquisition/observation scalar 时序

1. 将 `Ch4 acquisition preamble + observation window` 构造成一个明确连续的发送序列；在整个拼接序列上一次生成 shared GG/CFO/ramp/Wiener scalar，随后统一经过同一个固定 unitary Jones 和同一规则的 circular AWGN，再按冻结边界切回 `ch4_pilot_rx` 与 observation `rx`。
2. 不允许再用 `jones @ ch4_tx + independent_noise` 绕开 scalar；不得把 true scalar/Jones 暴露给 deployable bridge。
3. 必须保存或 hash 足够的 receiver-visible/realization provenance，使 preamble 长度、split 和连续时序可审计；offline truth 可保存完整 trace 供测试，但不得进入 deployable输入。
4. 新增非零 GG/CFO/Wiener sentinel：改变 scalar realization 时，`ch4_pilot_rx` 与 Ch4 `W` 必须按预期改变；零损伤/identity 控制仍保持精确；future-window mutation、truth mutation、polarization swap、8-fold rotation 全部继续成立。
5. 不引入新的 scene、SNR、pilot budget、filter/IQ/FIR/PDL/PMD/CD；fixture 参数仍是 correctness-only，不能升级成 occurrence authority。

## Fresh 验证与交付

- validator fresh PASS。
- 先证明新增测试在旧实现上 RED，再最小修复至 GREEN。
- fresh 跑原 Ch5 tests + bridge tests；运行 `run_occurrence_smoke.py --mode correctness`；argparse 仍必须拒绝 occurrence。
- `git diff --check`，确认没有超范围文件。
- 更新 receipt 必须继续写 `CORRECTNESS_ONLY / TARGET_OCCURRENCE_NOT_RUN / NO_METHOD_SIGNAL`。

最终回报：commit、RED/GREEN 证据、测试数、完整 arm snapshot/hash 性质、连续时序 sentinel 数字、truth/future/pol-swap/8-fold 结果，以及唯一 blocker“等待独立复验；此前 occurrence 禁止”。一次 commit、不 push。
