# Task Brief: 解决 arXiv 1704.04618 并行全文竞态并重裁碰撞

> 来源: S001 / D008 / T028 / T030 | 产出位置: 更新 `papers/_read_notes/1704.04618.md` + `projects/thesis-fso/worker-logs/step-077-resolve-arxiv1704-fulltext-race.md`
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

修复 shared-worktree acquisition race：T028 在 `23:31:00` 因正文缺失写入 `UNRESOLVED_FULLTEXT`，但并行 T030 在 `23:31:26` 成功取得 `papers/arxiv/1704.04618/content.md`（143,913 bytes，SHA256 `7B8BBD75E0DF07BA7A971561BCA3C0781B8E11C681648102C7CAAF430615FDA1`，metadata=`arxiv_pdf/good`）。fresh 精读当前 canonical 正文，保留历史 debt chronology，但用全文 verdict 更新 read note 当前状态。

## 1. 纪律与竞态审计

1. 先读 gw-read/gw-supplement、topic-index、D008、T028/step-074、T030/step-076、OFC 2015 note；fresh validator PASS 后执行。
2. 先核当前 content/metadata bytes/hash/timestamp、title/author/section quality；不得把 T028 当时的无正文记录写成失职，也不得因现在有正文保留过期 scientific status。
3. 不再下载；精读 full chapter 的 system/slip model、modified differential decoder、LDPC/SC-LDPC/windowed schedule、complexity、experiments、conclusion与 references。
4. 更新既有 read note时保留 acquisition-race 历史段，新增 `T031 resolution` 并把顶层 current status/collision 改为全文裁决；不改中央 owner/治理/代码，不实验/提交/push/触碰 p05；15 分钟收口。

## 2. 必答

- random phase-slip model、state/transition、modified differential BCJR/action；
- LDPC/SC-LDPC window 的真实时间/码图粒度、是否由 slip boundary 触发、是否 selective local re-decode；
- 八字段、clean behavior、fallback、iterations/window/latency/cost、output；
- 与 OFC 2015 的正文 lineage 和增量；是否还隐藏 explicit boundary/local carrier correction；
- verdict=`EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE`。

## 3. 产出

- 更新 `papers/_read_notes/1704.04618.md`
- `projects/thesis-fso/worker-logs/step-077-resolve-arxiv1704-fulltext-race.md`

Terminal：`RACE_RESOLVED_FULLTEXT_READ` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `CONTENT_INVALID_AFTER_ALL`。worker log 含竞态 chronology、content gate、≤10事实、八字段、lineage、collision、保护检查。

聊天只回 terminal/collision、竞态根因、window/local verdict和路径；≤650 字。
