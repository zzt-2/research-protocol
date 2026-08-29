# Task Brief: Ch5 legitimate post-Ch3/post-Ch4 residual authority audit

> 来源: S028 / D045 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/post-ch4-residual-authority.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 7
  action_class: LOCAL_PARAMETER_AUTHORITY_AUDIT
  mission_checkpoint: CP007
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只读审计现有 Ch3 CPR、Ch4 demultiplexing、共同平台、仿真配置与历史结果，判断哪一个已有且可诚实溯源的 receiver residual 能成为 Ch5 structured covariance 的首个 target-platform headroom cell。不得检索/下载、实现或运行任何仿真。

## 核心问题

1. Ch3 已录用方法的输出端是否有正式定义/数字可支持 residual phase error、cycle-slip-free phase jitter 或其他合法后 CPR residual；其单位、分布、SNR/linewidth/block 等参数来源是什么？
2. Ch4 memoryless Jones + pilot-LS/RDE 后，已有资产能输出哪些 receiver-visible residual 或 effective covariance；equal-white-noise 下是否理论上保持 circular，从而无法给 R/T 方法 headroom？
3. 是否存在已经实现且通过 correctness 的 receiver-local filter/IQ skew、nonlinear distortion、colored noise 或其他机制，可在不迁移 fiber PMD、不制造参数的前提下产生 APSK point/ring-dependent covariance？
4. 给出唯一首选 cell、最多一个后备 cell；逐字段写清生成链、参数 authority、与 Ch3/Ch4 章节的接口、是否会重复 Ch3 claim。
5. 若没有合法 cell，明确 `NO_AUTHORIZED_TARGET_RESIDUAL`，并指出解除它所需的最小外部 authority 或 testbed 改动；不得用 synthetic anisotropy 填空。

## 必读输入

- `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md` 与共同平台 authority。
- Ch3/CCISP 的当前 method/result/evidence bundle、现有 phase-noise/channel 参数与 verified worker logs。
- Ch4 T052 report、现有 Jones/LS/RDE assets 与 readiness audit 中指出的 seams。
- Ch5 T051 report，尤其 failure modes、oracle/headroom 与接口字段。

## 交付格式

唯一报告必须 findings-first，含：

- `AUTHORIZED / CONDITIONAL / NO_AUTHORIZED_TARGET_RESIDUAL` 总裁决；
- 已核文件与行号/字段证据表；
- circular-control 理论判断；
- primary/backup cell 的完整生成链与每个关键参数 authority；
- Ch3→Ch4→Ch5 因果归属和 claim firewall；
- 仍为 UNKNOWN 的字段、对后续 headroom 是否 blocking；
- 最小下一动作（只描述，不派任务）。

只新增报告，`git diff --check` 后提交一次。最终回报 commit、裁决、首选 cell、唯一 blocker。
