# Task Brief: ACCESS 2026 LDPC partial-metric iterative synchronization 全文精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1109_access.2026.3653159.md` + `projects/thesis-fso/worker-logs/step-065-c1-access2026-fulltext-read.md`
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

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 获取并精读 **Pilotless Iterative Carrier Synchronization With LDPC Partial Decision Metrics in Satellite Communications at Low SNRs**（DOI `10.1109/ACCESS.2026.3653159`），用于关闭近期 decoder-metric→phase/frequency update 的完整链碰撞与 B2 边界；不得从摘要推断局部 repair。

## 1. 纪律与执行

1. 读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1`，先运行 validator。
2. 用 `tools/download --doi 10.1109/ACCESS.2026.3653159` 获取并 title-check；三轮合法通道止损，失败写 `UNRESOLVED_FULLTEXT`。
3. 完整精读方法、算法、实验、结论，正文定位所有关键断言。
4. 不改中央 owner、治理、代码、artifact/p05；不提交；15 分钟。

## 2. 必答与完整链

回答：partial decision metric 定义与 receiver-visible 信息；phase/frequency state 和更新时间粒度；Costas loop 与 decoder 反馈时序；trigger/localization；是否显式处理 local cycle slip/boundary；修复全帧还是局部 segment/suffix；iteration/call/candidate/latency；clean/no-slip；fallback；失效条件；可复现 B2 形态；是否覆盖拟议 C1 完整链。

逐项写 `receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`，并给 `collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`。

## 3. 产出

- `papers/_read_notes/10.1109_access.2026.3653159.md`
- `projects/thesis-fso/worker-logs/step-065-c1-access2026-fulltext-read.md`

worker-log 含 validator、获取通道、title check、内容行数、正文定位、≤10 条事实、缺口、耗时与 git status 保护检查。

