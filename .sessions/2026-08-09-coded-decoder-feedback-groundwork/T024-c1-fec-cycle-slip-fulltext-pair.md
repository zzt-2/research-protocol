# Task Brief: Step 3.5 FEC-assisted cycle-slip 两篇全文裁决

> 来源: S001 / D008 / step-069 | 产出位置: `papers/_read_notes/10.1364_ofc.2014.m3a.3.md` + `papers/_read_notes/10.1109_icton.2016.7550341.md` + `projects/thesis-fso/worker-logs/step-070-c1-fec-cycle-slip-fulltext-pair.md`
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

获取并精读两个摘要缺失、题名高度命中 FEC-assisted cycle-slip mitigation 的短篇候选：OFC 2014 DOI `10.1364/OFC.2014.M3A.3` 与 ICTON 2016 DOI `10.1109/ICTON.2016.7550341`。只回答它们是否覆盖 Q1 的完整 local repair 链；题名不能承担碰撞裁决。

## 1. 纪律

1. 在唯一证据 worktree 执行；先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index、D008、step-069，并 fresh 运行 task-control validator。
2. 只用 `tools/download` / `tools/blit` 的合规通道；每个 Python/搜索命令设置 `PYTHONDONTWRITEBYTECODE=1`。单篇最多三条合法通道，失败保留 receipt，不能改写为 irrelevant/no collision。
3. 正文必须核 title/author/DOI、方法、算法/图、实验与结论；若只是 3–4 页 conference paper，仍要逐字段提取，不只看摘要。
4. 不改中央 owner/治理/代码，不实验，不 stage/commit/push，不触碰 p05；15 分钟收口。

## 2. 必答与八字段

对每篇回答：

- cycle slip 是物理注入、differential ambiguity 还是 decoder error propagation；global/local、多 slip 与 boundary 粒度；
- input、trigger、localization、candidate/correction action、decoder interaction、fallback、complexity/latency budget、output；
- 是否只做 differential coding/turbo demod，还是明确 detect/localize boundary 并只 reprocess segment/suffix；
- clean/no-slip behavior、candidate/decode iterations、failure condition；
- 与 Q1 complete-chain 的裁决：`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT`。

如裁 exact，必须逐项给正文页/行证据且所有八字段均同粒度；缺 fallback/budget/local action 任一项不得判 exact。

## 3. 产出

- `papers/_read_notes/10.1364_ofc.2014.m3a.3.md`
- `papers/_read_notes/10.1109_icton.2016.7550341.md`
- `projects/thesis-fso/worker-logs/step-070-c1-fec-cycle-slip-fulltext-pair.md`

worker log 含 validator、每条获取 receipt/正文质量、每篇≤10条事实、八字段、collision、claim ceiling、保护检查。Terminal：`PAIR_FULLTEXT_READ` / `PAIR_PARTIAL_WITH_DEBT` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `PAIR_UNRESOLVED_FULLTEXT`。

聊天只回 terminal、两篇状态/collision、最关键完整链事实和路径；≤700 字。
