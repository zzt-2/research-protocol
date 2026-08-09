# Task Brief: RML-FSTS Step 4a action-before protocol closure

> 来源: D011-D012 / V007 / H006 / S005 | 日期: 2026-08-09
> 时间上限: 15 分钟；到点必须冻结最小结论，不得转成系统设计扩张
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-action-before-protocol.md`

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 37
  action_class: NEW_TOPIC_RECOVERY
  mission_checkpoint: CP024
```
<!-- RDL-TASK-CONTROL:END -->

## 任务

只回答 D012 `AB1`：在不使用当前 action-specific FSTS 样值倒置决定当前动作、也不使用 hidden truth 的前提下，能否冻结一个最小 receiver-visible action-before structural-FSTS protocol。并排审计 `previous-frame` 与 `action-independent common probe`，只推荐/冻结一个 primary；另一个只作为 rejected/fallback 方案记录。不得实现 controller、运行 grid/MVE、改 owner/代码/合同，或把协议本身包装成方法贡献。

开始前完整读取并遵守：

1. `using-superpowers`、`research-direction-lab`、`session-governance` skills；
2. 本 T、D009-D012、V006-V007、H006、S005；
3. Wang canonical fulltext，特别是 FSTS construction、Eq. (7)–(11)、receiver chain 与 slow-varying statements；
4. `step-4a-rml-fsts-source-calibration.md` 的 `B2 action-before observability` 与 paired-latent contract；
5. 已有 turbulence/coherence 一手来源（先做本地 `rg`；若需 web，只读 primary source并给 DOI/公式/页码交叉验证）。

先运行并记录：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  .sessions/2026-08-08-rml-fsts-groundwork/T021-step4a-action-before-protocol-closure.md `
  --repo-root D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
```

非 PASS 立即停止并只写 setup blocker。

## 必做审计

### 1. 两方案比较

对 previous-frame 与 common-probe 分别给：

- observation source 与 action invariance；
- causal timeline；
- channel continuity/coherence 要求；
- feedback path、latency、ACK/reconfiguration；
- first-frame、drop、stale、bin-boundary与out-of-range处理；
- explicit symbols/control bits/latency/duty-cycle cost；
- same-realization/paired unit；
- 对 Wang source object 与 target FSO transfer 的适用边界。

不得用“coherence 通常很长”闭合；若无可移植数字，必须把 freshness 写成可执行、dev-frozen、receiver-visible 判据并说明需要什么 time-series source。不得假设零延迟反馈。

### 2. 冻结唯一 primary protocol

若能闭合，给精确 caller→callee contract：

```text
receiver samples at t_obs
  -> power estimator + normalization
  -> dev-frozen bin/key
  -> feedback message {frame_id, measurement_age, action_id, validity}
  -> transmitter freshness/ACK gate
  -> build_fsts(B_L, B_N=320/B_L)
  -> transmit selected FSTS
  -> receiver decodes signaled action
  -> score; hidden truth only here
```

至少冻结：

- primary observation window/estimator/reference plane；
- `(modulation, TS_length, power_bin) -> single structural action` lookup 的 dev/test lifecycle；
- feedback payload bit accounting（action grid大小必须明确或参数化）、latency timestamp与 ACK；
- freshness/coherence MDE：使用何种 receiver-visible time-series统计、dev freeze、test invariant；
- initialization/update/reset、one-frame/probe delay、stale/drop fallback=`B1`；
- action signaling与 mismatched-action fail-closed；
- explicit overhead equation；
- hidden-truth metamorphic test 与 runtime metamorphic test；
- paired cluster 如何跨 B0/B1/B2/O1 公平共享外生 latent，而不是伪造 same-rx。

### 3. AB1 判据

`AB1=PASS` 需要 causal timeline、合法观测、反馈、freshness/state、overhead、fallback、caller→callee 与可证伪测试全部闭合。若仍需 truth condition、当前 FSTS observation、未定义 time-series source、零成本反馈或不可计算 overhead，则 `NOT_CLOSED`。

## 输出格式

```markdown
# RML-FSTS action-before protocol closure
## Verdict
## Evidence boundary
## Previous-frame option
## Common-probe option
## Frozen primary caller-to-callee contract
## Information-access table
## Lifecycle, freshness and fallback
## Overhead accounting
## Executable semantic tests
## AB1 closure matrix
## Rejected alternatives and next legal action
```

Verdict 只允许：

- `AB1_PASS_CAUSAL_PROTOCOL_FROZEN`
- `AB1_NOT_CLOSED`
- `SETUP_BLOCKED`

只写指定 worker log；不 commit/push。结论必须明确：协议是 conventional conditioned-lookup deployment wrapper，不是 C1、METHOD_SIGNAL 或 novelty claim。
