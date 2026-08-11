# Task Brief: IWCMC 2023 adjustable-range code-aided synchronization 全文精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1109_iwcmc58020.2023.10182805.md` + `projects/thesis-fso/worker-logs/step-063-c1-iwcmc2023-fulltext-read.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 6
  action_class: FULLTEXT_READ
  mission_checkpoint: CP006
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 获取并精读 **Code-Aided Carrier Synchronization with Adjustable Operating Ranges for Satellite Communications**（DOI `10.1109/IWCMC58020.2023.10182805`），判断 CMF coarse correction + candidate list 是否是 C1 defect 的 strongest cheap/conventional alternative，以及是否已覆盖局部 slip 定位和 bounded repair。摘要只可筛选。

## 1. 纪律

1. 读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1`，先运行 validator。
2. 使用 `tools/download --doi 10.1109/IWCMC58020.2023.10182805`；三轮合法通道止损。全文不可得时写 `UNRESOLVED_FULLTEXT`，不得把摘要扩成方法事实。
3. title self-check 后读 method/algorithm/experiment/conclusion；公式、图表与关键数字给定位。
4. 不改中央 owner、治理、代码、artifact/p05，不提交；15 分钟内完成。

## 2. 必答

除标准 read-note 字段外，回答：CMF 的 receiver-visible input；coarse correction/candidate list 的动作与搜索粒度；是否使用 decoder soft/hard/syndrome evidence；是否 iteration-wise；是否检测/定位局部 slip boundary；整帧/segment/suffix 修正；candidate 数、同步器/decoder 调用与可调 operating range；clean/no-slip 行为；失效条件；与 B1 finite decoder-selection 的关系；作为 B2 的可复现实例和预算；是否覆盖完整局部 repair 链。

逐项比较 `receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`，并给 `collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`。

## 3. 产出

- `papers/_read_notes/10.1109_iwcmc58020.2023.10182805.md`
- `projects/thesis-fso/worker-logs/step-063-c1-iwcmc2023-fulltext-read.md`

worker-log 记录 validator、获取命令/通道、title check、内容行数、≤10 条关键事实、未决项、耗时与 git status 保护检查。

