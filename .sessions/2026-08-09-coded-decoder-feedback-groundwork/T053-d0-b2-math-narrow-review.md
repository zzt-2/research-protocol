# Task Brief: D0 B2 IC-01–IC-08 数学与 P08 约定窄审

> 来源: step-095 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-099-d0-b2-math-narrow-review.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：step-095 的 IC-01–IC-08 在 source identity、P08 positive-for-bit-1 LLR、噪声方差和 16QAM moment-match 上自洽，能成为确定性实现 receipt。
- 否决条件：若任何选择改变 OFC17 baseline 身份、使用 truth/decoder feedback、使 single-state hard decision 与 P08 不一致，或 P08 `sigma2` 的 complex/per-real 定义导致不可消除的 2 倍歧义，则判 `B2_MATH_CONTRACT_AMBIGUITY`。

## 任务

1. 完整读取 step-095、D0 YAML、OFC2017 本地全文、P08 constellation/demapper 与 prefix sigma estimator。
2. 独立复算 4-state T/q、distance power、pilot emission、nearest-pilot local smoothing、16QAM Gaussian mixture LLR 与 sign。
3. 专门审查 IC-02/IC-03：`estimate_sigma2_from_prefix=mean|resid|^2` 与 P08 demapper `/ (2*sigma2)` 的语义；给唯一的变量命名/公式/identity test，禁止含混写“per-real”或“complex”。
4. 审查 state-permutation、global pi/2 covariance、single-state collapse、uniform-state null、p_s=0 的预期是否正确。
5. 给 verdict=`IC_SET_ACCEPTED / IC_SET_ACCEPTED_WITH_CORRECTIONS / B2_MATH_CONTRACT_AMBIGUITY / BUDGET_BLOCKER`；如需修正，逐条给替换公式，不改 owner。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-099-d0-b2-math-narrow-review.md`。
- 只读；禁止 import/pytest/D0/仿真、web/search/download、owner/源码/治理修改、commit/push、p05 触碰。
- 12 分钟目标，15 分钟硬上限。

