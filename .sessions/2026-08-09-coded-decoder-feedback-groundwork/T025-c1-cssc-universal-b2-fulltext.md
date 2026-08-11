# Task Brief: Step 3.5 CSSC-CPE 与 universal CS-DC B2 全文精读

> 来源: S001 / D008 / step-069 | 产出位置: `papers/_read_notes/10.1109_access.2019.2934224.md` + `papers/_read_notes/10.1364_oe.22.031167.md` + `projects/thesis-fso/worker-logs/step-071-c1-cssc-universal-b2-fulltext.md`
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

获取并精读 provisional strongest B2 CSSC-CPE（DOI `10.1109/ACCESS.2019.2934224`）和通用 cycle-slip detector/corrector（DOI `10.1364/OE.22.031167`）。目标是冻结 receiver-only local-slip traditional comparator 的真实算法、参数、failure/fallback 和成本，并检查它是否已经完全吸收 Q1。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、`domain-comms.md` 相关段、topic-index、D008、step-069；fresh validator PASS 后执行。
2. 优先 OA/DOI/arXiv 合规通道，用 `tools/download` / `tools/blit`；所有 Python/搜索命令设置 `PYTHONDONTWRITEBYTECODE=1`。单篇最多三通道，失败如实留债。
3. 全文核 identity/method/equations/algorithm/experiment/conclusion；提取可用于 Step 4a 的有来源参数，不把作者仿真 slip law 自动冒充自然 FSO 分布。
4. 不改中央 owner/治理/代码，不实验，不提交/push，不触碰 p05；15 分钟收口。

## 2. 必答

- CSSC 的 cumulative-sum/cumulative-average 定义、window/threshold、peak position/sign、correction range、single/multiple-slip behavior、clean false action、latency/complexity、输入是否只依赖 receiver-visible CPE output。
- universal CS-DC 的 detector statistic、window/threshold、primary/secondary correction、modulation/CPE independence、残余 slip 概率、failure condition 与复杂度。
- 每篇完整八字段；是否需要 decoder interaction，是否只修 suffix/segment，是否有 abstain/fallback。
- 可直接复现参数与必须 dev-tune 的参数分开；给 B2 implementability verdict 与预计 effort。
- Q1 collision：只有同时覆盖 decoder-evidence trigger/localization/re-evaluation/fallback 且预算相当才可 exact；纯 receiver CPE local correction应作为 strongest B2，不自动碰撞 decoder-guided extension。

## 3. 产出

- `papers/_read_notes/10.1109_access.2019.2934224.md`
- `papers/_read_notes/10.1364_oe.22.031167.md`
- `projects/thesis-fso/worker-logs/step-071-c1-cssc-universal-b2-fulltext.md`

Terminal：`B2_PAIR_FULLTEXT_READ` / `B2_PAIR_PARTIAL_WITH_DEBT` / `B2_ABSORBS_Q1` / `B2_PAIR_UNRESOLVED_FULLTEXT`。worker log 含 acquisition/identity/正文质量、参数表、八字段、collision、Step 4a usable/not-usable、成本和保护检查。

聊天只回 terminal、两篇状态、provisional B2 冻结建议、是否吸收 Q1、路径；≤700 字。
