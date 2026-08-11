# Task Brief: Step 3.5 phase-slip-tolerant FEC conference 两篇全文裁决

> 来源: S001 / D008 / step-067 | 产出位置: `papers/_read_notes/10.1109_ecoc.2014.6963875.md` + `papers/_read_notes/10.1364_ofc.2015.th3e.6.md` + `projects/thesis-fso/worker-logs/step-076-c1-slip-tolerant-fec-conference-pair.md`
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

获取并精读两个无摘要但题名命中 phase-slip-tolerant FEC / differential decoding 的 conference 候选：DOI `10.1109/ECOC.2014.6963875` 与 DOI `10.1364/OFC.2015.TH3E.6`。同时核它们与 arXiv `1704.04618`、ICTON 2016、OFC 2014 的作者/方法/版本关系，避免重复计数；只以正文裁八字段碰撞。

## 1. 纪律

1. 先读 gw-acquire/gw-read/gw-supplement、topic-index、D008、step-067、OFC 2014/ICTON 2016 notes；fresh validator PASS 后执行。
2. 使用 `tools/download` / `tools/blit`，设置 `PYTHONDONTWRITEBYTECODE=1`；每篇最多三合法通道，失败保留债。
3. 正文核 identity、slip model、FEC/differential action、decoder schedule、complexity、experiments和结论；题名不可承担 action 断言。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- 每篇完整八字段；是否 detect/localize slip boundary、只 repair/redecode segment/suffix、clean no-op/fallback；
- differential/FEC tolerance 与真正 carrier correction 的边界；iterations、window/interleaver/pilot/overhead与成本；
- 与 arXiv 1704.04618 / ICTON 2016 / OFC 2014 的 identity/predecessor/extension 关系；
- verdict=`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`。

## 3. 产出

- `papers/_read_notes/10.1109_ecoc.2014.6963875.md`
- `papers/_read_notes/10.1364_ofc.2015.th3e.6.md`
- `projects/thesis-fso/worker-logs/step-076-c1-slip-tolerant-fec-conference-pair.md`

Terminal：`PAIR_FULLTEXT_READ` / `PAIR_PARTIAL_WITH_DEBT` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `PAIR_UNRESOLVED_FULLTEXT`。worker log 含 acquisition/quality、≤10事实/篇、八字段、identity chain、collision与保护检查。

聊天只回 terminal、两篇状态/collision、版本关系和路径；≤700 字。
