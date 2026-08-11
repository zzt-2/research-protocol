# Task Brief: C1 Step 3.5 fresh-context 完整链 verifier

> 来源: S001 / D008 / step-067–081 | 产出位置: `projects/thesis-fso/worker-logs/step-082-c1-step3_5-collision-verifier.md`
> 日期: 2026-08-10

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

## 0. 审查目标

从 fresh context 独立判断中央报告的 `NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE` 是否被本地全文支持。不得继承主线程或 read note 的裁决；read note 只作索引，关键结论必须回到 `papers/**/content.md` 或已 QA 的本地 PDF/markdown spot-check。

## 1. 必读与抽核

1. topic-index、D005–D008、canonical Q1、`step3_5-supplement-report.md`、literature owner。
2. worker logs step-070、072、073、076、077、079、081。
3. 至少独立 spot-check 六个承重全文：C1 reference M（arXiv2511 或 TSP2006 至少一篇）；OFC2014；arXiv1704；arXiv2604；OFC2017；再从 Tikhonov/HTDD/PAPU 中选一篇。
4. 对每篇按八字段复判，特别防止把 per-symbol hidden state、code-graph window、localized error event、parallel LLR refinement 误写成 explicit boundary + bounded local carrier repair。

## 2. 必答

- 是否存在同 receiver-visible input、event trigger、explicit boundary/range、finite local phase action、decoder re-evaluation、fallback、bounded cost、repair output 的 exact complete chain；
- OFC2017 的 soft decision 是否来自 FEC decoder；2604 的 burst 是否为 discrete slip；1704 的 window 是否是 detected slip-local window；
- unresolved CSSC/CS-DC/U01/U02 是否被正确 fail-closed，而非被写成 no collision；
- Q1 是否仍只是假设，未把 defect occurrence/observability/recoverability 预设为事实；
- 中央 report/literature owner 是否有 P0/P1/P2 语义缺陷。

## 3. 终态与产出

写 `projects/thesis-fso/worker-logs/step-082-c1-step3_5-collision-verifier.md`，含逐篇八字段差异、证据路径/行号、P0/P1/P2 数量、verdict=`PASS` / `FAIL`。PASS 只接受 bounded-slice claim，不得作领域级 novelty closure。FAIL 必须给最小修复，不得改文件。

只读；不得 web/下载/改任何文件（除指定 verifier log）、不得实验/提交/push/触碰 p05。hard cap 15 分钟，fresh p05 4/4 与 staging 检查后收口。
