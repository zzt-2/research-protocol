# Task Brief: Step 3.5 Tikhonov-mixture joint phase tracking 全文精读

> 来源: S001 / D008 / step-068 | 产出位置: `papers/_read_notes/1306.3693.md` + `projects/thesis-fso/worker-logs/step-072-c1-tikhonov-joint-decoding-fulltext.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: FULLTEXT_READ
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

获取并精读 arXiv `1306.3693` / DOI `10.1109/TCOMM.2015.2506553` 的 dynamic Tikhonov-mixture phase tracking + joint decoding。目标是判定 per-symbol multi-modal phase posterior 是否已隐式覆盖 local cycle-slip localization/repair，还是只属于连续 joint tracking strong neighbor。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index、D008、step-068 和 L05 read note；fresh validator PASS 后执行。
2. 优先 `tools/download --arxiv 1306.3693`，核 DOI/title/author/version identity；所有 Python命令设置 `PYTHONDONTWRITEBYTECODE=1`。
3. 精读 system model、factor graph/message approximation、mixture reduction、pilot/code interaction、complexity、experiments与结论；不能由 abstract 判 local repair。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- phase state/model 是否含 discrete slip/change point，还是 Wiener phase-noise trajectory；mixture modes 是否保留 ambiguity branches；
- receiver-visible input、trigger、localization granularity、candidate/action、decoder interaction、fallback、complexity/latency budget、output；
- per-symbol dynamic tracking 是否等价于 `detect boundary → bounded segment/suffix rollback/redecode`；若不等价，精确指出缺字段；
- clean/no-slip behavior、pilot usage、decoder iterations、mixture order、pruning/merge、cycle-slip failure；
- verdict：`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`，附正文指针。

## 3. 产出

- `papers/_read_notes/1306.3693.md`
- `projects/thesis-fso/worker-logs/step-072-c1-tikhonov-joint-decoding-fulltext.md`

Terminal：`FULLTEXT_READ` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `UNRESOLVED_FULLTEXT`。worker log 含 identity、正文质量、≤10事实、八字段、collision、claim ceiling、耗时和保护检查。

聊天只回 terminal/collision、最关键 local-vs-dynamic 事实和路径；≤600 字。
