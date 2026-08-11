# Task Brief: Step 3.5 arXiv 1704.04618 windowed LDPC slip 全文精读

> 来源: S001 / D008 / step-067 | 产出位置: `papers/_read_notes/1704.04618.md` + `projects/thesis-fso/worker-logs/step-074-c1-arxiv1704-windowed-slip-fulltext.md`
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

获取并精读 arXiv `1704.04618` 的 modified differential decoder + LDPC/SC-LDPC windowed decoding under cycle slips。判定其“windowed”是否只是 code graph 调度，还是已经实现 Q1 所需的 slip boundary/local segment repair；同时核与 ICTON 2016 是否同一工作/扩展版，避免重复计数。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index、D008、step-067 和 ICTON 2016 read note；fresh validator PASS 后执行。
2. 优先 `tools/download --arxiv 1704.04618`，核 title/authors/DOI/version 与 ICTON identity；设置 `PYTHONDONTWRITEBYTECODE=1`。
3. 精读 channel/slip model、differential metric、LDPC/SC-LDPC window、iteration/fallback、complexity、实验与结论。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- 八字段完整链；slip boundary 是否显式定位，window 是否等于 affected segment/suffix，是否只 selective re-decode；
- modified differential decoder 的 slip state/action、decoder evidence timing、clean/fallback；
- `windowed SC-LDPC` 的 window length/latency/iterations 与 full-codeword baselines；
- 与 ICTON 2016 的身份/机制关系；verdict=`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`。

## 3. 产出

- `papers/_read_notes/1704.04618.md`
- `projects/thesis-fso/worker-logs/step-074-c1-arxiv1704-windowed-slip-fulltext.md`

Terminal：`FULLTEXT_READ` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `UNRESOLVED_FULLTEXT`。worker log 含 identity、≤10事实、八字段、collision、重复/扩展关系、成本与保护检查。

聊天只回 terminal/collision、window 真实语义、与 ICTON 关系和路径；≤600 字。
