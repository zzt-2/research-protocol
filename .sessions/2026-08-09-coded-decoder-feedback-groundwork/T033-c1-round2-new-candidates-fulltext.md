# Task Brief: Step 3.5 round-2 两个新增 SHOULD 全文裁决

> 来源: S001 / D008 / T032 | 产出位置: `papers/_read_notes/2604.07004.md` + `papers/_read_notes/10.1364_ofc.2015.tu3b.2.md` + `projects/thesis-fso/worker-logs/step-079-c1-round2-new-candidates-fulltext.md`
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

获取并精读 round 2 新增的两个 `SHOULD_FULLTEXT`：arXiv `2604.07004`（摘要称 burst-aware LDPC + iterative channel estimation）与 OFC 2015 DOI `10.1364/OFC.2015.TU3B.2`（题名命中 cycle-slip-tolerant differential-encoding-aware SD-FEC、摘要缺失）。只用全文判它们是否覆盖 Q1 的 explicit local boundary + bounded carrier repair + decoder re-evaluation 完整链。

## 1. 纪律

1. 先读 gw-acquire/gw-read/gw-supplement、topic-index、D008、T032/现有 receipts、step-070–077关键 notes；fresh validator PASS 后执行。
2. 优先 `tools/download --arxiv 2604.07004`；OFC 用 DOI pipeline + `tools/blit`，设置 `PYTHONDONTWRITEBYTECODE=1`；单篇最多三合法通道，失败保留债。
3. 核 identity、system/impairment、burst/slip state、algorithm、decoder/channel-estimator timing、complexity、experiments、conclusion；不以摘要/题名裁 exact。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- arXiv 2604.07004 的 “burst-aware” 是 burst error model、boundary localization、code structure，还是 carrier phase segment action；iterative channel estimation 是否含 slip hypotheses/local reprocessing；
- OFC 2015 的 differential-encoding-aware SD-FEC 只是 tolerance/code design，还是 detect/localize/correct carrier samples；
- 每篇八字段、clean/fallback、budget、output、与 OFC 2014/2015/ECOC/arXiv1704 的 identity/机制重合；
- verdict=`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`。

## 3. 产出

- `papers/_read_notes/2604.07004.md`
- `papers/_read_notes/10.1364_ofc.2015.tu3b.2.md`
- `projects/thesis-fso/worker-logs/step-079-c1-round2-new-candidates-fulltext.md`

Terminal：`PAIR_FULLTEXT_READ` / `PAIR_PARTIAL_WITH_DEBT` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `PAIR_UNRESOLVED_FULLTEXT`。worker log 含 acquisition/quality、≤10事实/篇、八字段、collision、claim ceiling与保护检查。

聊天只回 terminal、两篇状态/collision、burst真实语义和路径；≤700 字。
