# Task Brief: Ch4 canonical formal reduction and independent statistics

> 来源: S028 / D069 / V044 / T089 | 产出: canonical aggregate/receipt、独立raw-only统计复算与grade裁决
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 31
  action_class: CH4_CANONICAL_FORMAL_REDUCTION
  mission_checkpoint: CP031
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对SHA=`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`的immutable canonical raw唯一运行一次冻结reducer，生成aggregate/receipt；随后由独立reviewer不导入runner/reducer、直接从raw重算所有承重统计与A/B/C/F grade。不得改口径、补实验、作图或写正文。

## 冻结输入与预期

- raw size=`89,419,500` bytes，census=`128/384/15232/76160/ref128`；
- manifest SHA=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；lock SHA=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`；
- whole-curve bootstrap PCG64 seed=`2026083007`、5000 resamples、named comparison reset、valid min4500；cell bootstrap seed=`2026083008`、5000、128 paired latent clusters；
- grade只允许C4_FWD/B3_PSC相对B2_TUNED，primary仅moderate Np2/Np4；C4-vs-B3不作gate。

## 文件白名单

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_aggregate.json`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_receipt.json`
- 上述两文件的`.tmp`仅运行中允许，成功后必须消失
- `projects/thesis-fso/worker-logs/step-090-ch4-canonical-formal-reduction.md`
- 独立reviewer写 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/canonical-formal-statistics-independent-verification.md`

raw、代码、tests、manifest、lock及历史artifacts均只读。

## 执行前门

1. 完整读sim-preflight、T090、D069/V044、manifest/lock、step-089与raw independent report；task-control CP031/epoch31 PASS。
2. raw/manifest/lock/bound hashes、HEAD/environment exact；fresh focused=`19/19`、pycompile5 PASS。
3. aggregate、receipt及其tmp必须全部不存在；任一存在立即停机。
4. reducer source不得导入runner或读取历史aggregate作科学输入；entry environment/binding fail-close仍在。

## 唯一canonical reduction

仅运行一次：

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_ch4_formal_production.py`

不得加参数。若exit非0或留下tmp，立即停机，不重跑、不删除tmp。成功后记录exit、wall time、stdout terminal、aggregate/receipt SHA/size/terminal/grade；不得在实现者上下文另跑第二套统计或调整grade。

## 独立raw-only统计复算

reviewer不得导入runner、`ch4_formal_reducer.py`或canonical entry；可写OS-temp独立脚本，但不得修改仓库。必须直接从raw counts复算：

1. 每个scene/Np/SNR/role pooled counts与Jeffreys BER；
2. C4/B3相对B2的moderate Np2/Np4 required-SNR、crossing状态、point gain、5000 whole-curve cluster bootstrap CI与valid replicate数；
3. grade C 所需moderate Np2/Np4每SNR paired BER-diff及5000 cell bootstrap CI；
4. A/B/C/F穷尽grade，严格使用frozen条件；
5. mechanism、scene、pilot、mismatch summary的raw-derived counts/means；
6. aggregate/receipt/raw/manifest/lock hashes、census、terminal与所有数值字段的一致性，报告最大绝对差。

独立复算必须每个named comparison重置注册seed，不跨scene pooling；whole-curve每个sampled latent携完整19-SNR slice。P0/P1非0则不接收任何结果。

## 禁止

- 不改threshold/SNR/Np/tau/bootstrap/resamples/grade/comparator，不补seed或重跑formal；
- 不从aggregate反推raw，不选择性省略B3、不把O1当deployable baseline；
- 不作图、写正文、检索、改Groundwork/Skill/controller、恢复Ch5或新方向。

## 终态

- `CH4_CANONICAL_FORMAL_STATISTICS_READY`：canonical artifacts + 独立raw复算P0/P1=0，按frozen grade如实进入下一裁决；
- `CH4_FORMAL_REDUCTION_INVALID`：任一hash/schema/statistics/grade不一致；禁止重跑、作图与解释性能。
