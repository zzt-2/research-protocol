# Task Brief: Ch4 Q-C4-2 GW Step 3.5 exact-recipe closure

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-front-end-groundwork/step3-5-supplement-report.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 5
  action_class: TARGETED_SUPPLEMENT_SEARCH
  mission_checkpoint: CP005
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只对 T048 的 `Q-C4-2` 做 mandatory Step 3.5 exact-recipe closure。目标完整 recipe 固定为：有限 pilot 的 2×2 LS 初始化 + 已知 `(8,8)-16APSK` ring identity + payload receiver residual/decision distance → 对均衡更新做逐样本 reliability gate/weight → 输出 semi-blind refined 2×2 demultiplexer。公平 comparator 是同 LS 初值、pilot、样本、更新次数和调参预算的 LS-only、tuned RDE 与 tuned DD-LMS/RLS。

## 检索切片

- 预注册最多 6 个 task-matched queries，必须覆盖 2019+：`pilot initialized reliability gated APSK equalization`、`ring aware weighted RDE APSK`、`soft decision gated blind equalization APSK`、`semi blind dual polarization APSK equalizer`、`decision confidence weighted LMS coherent receiver`、`pilot aided radius directed equalization`。
- 以 RDE canonical、Fatadin 2009 coherent comparator、Baldi 2012 direct APSK 与 Roudas 2010 constrained demux 做有限 citation/alias closure；最多三轮，某轮 new MUST/SHOULD=0 即停。
- 只有同 receiver-visible inputs、同 pilot-init、ring-aware error、reliability gate/weight、2×2 equalizer output 的完整组合相同才记 `EXACT_RECIPE_COLLISION`。
- 通用 confidence-weighted LMS、soft decision equalization、RDE、pilot initialization 或不同调制/场景只记 `STRONG_NEIGHBOR/PRIMITIVE_COLLISION`，限制 claim ceiling，不自动关闭硕士级 target-scene extension。

## 边界与验收

- 使用项目 `tools/search`/citation 与合规下载；只下载可能 exact collision 的少量全文。不得原始 WebSearch。
- 不做 Step 4a、实现、实验，不改仿真/Skill/controller/论文正文或 `papers/index.json`。
- 产出 query archives/receipt、少量必要 read notes、唯一 supplement report；报告必须给轮次新增计数、exact-action ledger、fulltext/abstract 边界与 `Q-C4-2 SURVIVES` 或 `EXACT_RECIPE_COLLISION`。
- 最终回报 commit、query/record/fulltext 数、最强邻居、唯一 blocker；15 分钟内完成一轮 bounded closure。
