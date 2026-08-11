# Task Brief: Step 3.5 pilot B2 与 coherent-FSO 物理全文包

> 来源: S001 / D008 / step-069 | 产出位置: `papers/_read_notes/10.3390_app9132749.md` + `papers/_read_notes/10.1109_jlt.2020.3003561.md` + `projects/thesis-fso/worker-logs/step-075-c1-pilot-physical-b2-fulltext.md`
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

获取并精读 pilot-assisted phase-unwrapping B2（DOI `10.3390/APP9132749`）与 satellite-ground coherent optical phase-noise/DPLL 物理来源（DOI `10.1109/JLT.2020.3003561`）。CSSC/CS-DC 正文不可得，本包要给 Step 4a 一个可全文冻结的 conventional B2/物理参数锚；不强求两篇都成功，失败保留债。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、`domain-comms.md` 相关段、topic-index、D008、step-069、step-071；fresh validator PASS 后执行。
2. 用 `tools/download` / `tools/blit` 合规通道，设置 `PYTHONDONTWRITEBYTECODE=1`；单篇最多三通道，不抓 publisher HTML 替代正文。
3. 全文核 identity/method/equations/parameters/experiments/conclusion；区分作者 synthetic/VOA 条件与自然 FSO 分布。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

### PAPU / pilot B2

- VVPE + pilot-aided phase unwrapping 的输入、trigger、slip localization/correction、pilot spacing/overhead、filter lengths、clean behavior、fallback、cost/latency；
- 是否只用 receiver/pilot information，能否作为可实现 B2；完整八字段与 collision。

### JLT physical source

- turbulence/AO/laser linewidth/frequency mismatch/phase-noise model及可引用数值；DPLL topology/loop参数/lock/slip behavior；
- 哪些参数可用于 coherent-FSO Step 4a stress slice，哪些不能映射成离散 local slip；完整八字段与 B2 role。

## 3. 产出

- `papers/_read_notes/10.3390_app9132749.md`
- `papers/_read_notes/10.1109_jlt.2020.3003561.md`
- `projects/thesis-fso/worker-logs/step-075-c1-pilot-physical-b2-fulltext.md`

Terminal：`PAIR_FULLTEXT_READ` / `PAIR_PARTIAL_WITH_DEBT` / `PAIR_UNRESOLVED_FULLTEXT`。worker log 含 acquisition/quality、每篇≤10事实、参数、八字段、B2 freeze recommendation、collision、claim ceiling与保护检查。

聊天只回 terminal、两篇状态、B2/物理可冻结项和路径；≤700 字。
