# Task Brief: TWC 2004 iterative decoder-aided CPR 全文精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1109_twc.2004.837407.md` + `projects/thesis-fso/worker-logs/step-064-c1-twc2004-fulltext-read.md`
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

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 获取并精读 **Iterative carrier phase recovery suited to turbo-coded systems**（DOI `10.1109/TWC.2004.837407`）。它是 decoder extrinsic→iterative ML phase estimation 的奠基 direct comparator；任务是从全文确定其相位状态粒度、更新时序、局部 slip 能力、计算预算及与 C1 局部 repair 完整链的真实重合范围。

## 1. 纪律与执行

1. 读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1`，先运行 validator。
2. 优先用 `tools/download --doi 10.1109/TWC.2004.837407`；已知 OA 候选只能通过工具下载/归档。三轮合法通道止损，全文失败写 `UNRESOLVED_FULLTEXT`。
3. title self-check 后精读方法、公式、实验、结论；摘要不承担 collision。
4. 不改中央 owner、治理、代码、artifact/p05；不提交；15 分钟。

## 2. 必答与完整链

回答：decoder extrinsic 的精确定义和时点；phase estimator 的状态/窗口/更新粒度；outer iterations 与 decoder/estimator calls；global ambiguity 与 local/time-varying slip 能力；是否定位 boundary 或只做全局/连续估计；clean/no-slip 行为；fallback；复杂度；失效条件；实验编码/调制/信道；与 B1/B2/C1-ext 的可比性。

逐项写 `receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`，并给 `collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`。

## 3. 产出

- `papers/_read_notes/10.1109_twc.2004.837407.md`
- `projects/thesis-fso/worker-logs/step-064-c1-twc2004-fulltext-read.md`

worker-log 含 validator、获取通道、title check、内容行数、正文定位、≤10 条事实、缺口、耗时、git status 保护检查。

