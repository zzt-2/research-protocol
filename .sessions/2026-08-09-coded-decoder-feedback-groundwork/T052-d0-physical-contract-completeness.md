# Task Brief: D0 physical/testbed 参数唯一性独立审计

> 来源: step-094 / D010 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-098-d0-physical-contract-completeness.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: SOURCE_AUDIT
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：D0 的 source closure 与 params 单一源已经能唯一确定 supplied-waveform channel 的全部必要输入；遗漏只需在 YAML 显式投影，不改变 population 身份。
- 否决条件：若 `f_G/block/method`、Wiener 相位、SOP、噪声、prefix/equalizer 或注入时序存在两个以上科学上不等价且无法从冻结来源选择的方案，则判 `PHYSICAL_CONTRACT_AMBIGUITY`，不得让实现者猜。

## 任务

1. 从 D0 YAML、adaptive-phase-window source closure、params、P08-R2 与 common channel 反向列出一个 supplied-waveform D0 realization 的全部 constructor inputs。
2. 对 `f_G`、GG block/method/tau、Wiener variance/initial phase/combined linewidth、CFO、SOP/cross-pol mixing、AWGN variance、shared/independent axes、prefix sequences、pre/post equalization noise semantics、BPS edge handling逐项判 `FROZEN / IMPLIED_BUT_NEEDS_PROJECTION / AMBIGUOUS / OUT_OF_SCOPE`，附来源行号。
3. 针对 step-094 的同前缀 2×2 LS 秩亏，比较最小合法出口：distinct prefixes+rank4 2×2 LS，或 no-SOP scalar per-pol estimator；判断哪一个与当前 D0 population 单义一致。
4. 给最小 owner 字段树、source receipt 与单测清单；不改任何 owner。
5. verdict=`PHYSICAL_CONTRACT_COMPLETE / MINIMAL_PROJECTION_REQUIRED / PHYSICAL_CONTRACT_AMBIGUITY / >7D_HARD_BLOCKER`。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-098-d0-physical-contract-completeness.md`。
- 只读；禁止 import/pytest/D0/仿真、web/search/download、源码/owner/治理修改、commit/push、p05 触碰。
- 12 分钟目标，15 分钟硬上限。

