# Task Brief: GLOBECOM 2012 hard/soft DD CPR 全文获取与 conventional comparator 精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1109_glocom.2012.6503711.md` + `projects/thesis-fso/worker-logs/step-062-c1-glocom2012-fulltext-read.md`
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

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 获取并精读 **Performance analysis of code-aided iterative hard/soft decision-directed carrier phase recovery**（DOI `10.1109/GLOCOM.2012.6503711`），用于冻结 B2 strongest conventional hard/soft DD CPR 的信息、更新、预算和失效边界。摘要不足以完成任务。

## 1. 纪律

1. 读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1`，先运行 validator。
2. 使用仓库 `tools/download --doi 10.1109/GLOCOM.2012.6503711`；CRLF 时可 `cd tools && tr -d '\r' < download | bash -s -- --doi ...`。三轮通道止损后仍无全文则写 `UNRESOLVED_FULLTEXT`，不得用摘要补公式。
3. title self-check 后完整读 method/algorithm/experiment/conclusion；只按正文陈述。
4. 不改中央 owner、治理、代码、artifact/p05，不提交；15 分钟内完成。

## 2. 必答

除 Groundwork read-note 标准字段外，回答：hard 与 soft decision 的精确定义；decoder information 的因果时点；phase state/更新的时间粒度；是否显式检测/定位 cycle slip；全帧还是局部 segment/suffix；outer iteration、decoder/estimator 调用数；clean/no-slip 行为；调谐参数与成本；失效条件；能否作为 B2 同信息同预算 comparator；是否已覆盖 `trigger→localize→bounded local repair→fallback` 完整链。

完整链必须逐项填写 `receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`，并给 `collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`。

## 3. 产出

- `papers/_read_notes/10.1109_glocom.2012.6503711.md`
- `projects/thesis-fso/worker-logs/step-062-c1-glocom2012-fulltext-read.md`

worker-log 记录获取命令/通道、title check、内容行数、正文 pointer、≤10 条关键事实、缺口、耗时与 git status 保护检查。

