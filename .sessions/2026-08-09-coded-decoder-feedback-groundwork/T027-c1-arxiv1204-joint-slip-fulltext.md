# Task Brief: Step 3.5 arXiv 1204.2660 joint phase/LDPC slip 全文精读

> 来源: S001 / D008 / step-067 | 产出位置: `papers/_read_notes/1204.2660.md` + `projects/thesis-fso/worker-logs/step-073-c1-arxiv1204-joint-slip-fulltext.md`
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

获取并精读 arXiv `1204.2660`。Round 1 abstract 称其用 directional-statistics clustering / Bayesian message passing 联合做 phase-noise 与 LDPC inference，并处理 phase slips；本任务必须判断这种 per-symbol joint inference 是否已覆盖 Q1 的 explicit boundary、bounded segment/suffix repair、selective re-decode 与 fallback。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index、D008、step-067 和 OFC 2014 read note；fresh validator PASS 后执行。
2. 优先 `tools/download --arxiv 1204.2660`；核 title/author/DOI/版本，所有 Python命令设置 `PYTHONDONTWRITEBYTECODE=1`。
3. 精读 phase/channel model、factor graph、clustering/mixture reduction、slip state、decoder interaction、complexity、experiments与结论；摘要不能承担 collision。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- slip/change-point 的物理与数学定义；global/local/multiple-slip 粒度；是否输出 boundary/direction；
- 八字段：input、trigger、localization、candidate/action、decoder interaction、fallback、budget、output；
- 是 whole-codeword unconditional joint inference，还是 event-triggered bounded local repair；
- clean/no-slip behavior、iterations、mixture/cluster order、pruning、pilot/known-symbol使用、failure条件；
- 与 OFC 2014、Q1 B1/C1-ext 的差异；verdict=`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`。

## 3. 产出

- `papers/_read_notes/1204.2660.md`
- `projects/thesis-fso/worker-logs/step-073-c1-arxiv1204-joint-slip-fulltext.md`

Terminal：`FULLTEXT_READ` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `UNRESOLVED_FULLTEXT`。worker log 含 identity/质量、≤10事实、八字段、collision、claim ceiling、成本与保护检查。

聊天只回 terminal/collision、最关键 local-vs-joint 事实和路径；≤600 字。
