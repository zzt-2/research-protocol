# Task Brief: Ch4 canonical reduction publication repair

> 来源: S028 / D070 / V045 / T090 | 产出: canonical aggregate/receipt与独立raw-only统计复算
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 32
  action_class: CH4_CANONICAL_REDUCTION_PUBLICATION_REPAIR
  mission_checkpoint: CP032
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

不修改任何bound code/raw/manifest/lock，以独立验证过的显式PYTHONPATH再次运行同一canonical reducer entry一次，发布aggregate/receipt；随后按T090合同由独立reviewer直接从immutable raw复算全部承重统计与grade。

## 冻结事实

- T090 exit=1发生于内存`reduce_raw()`完成后的首次`projects.simulation.common` publication import；无artifact/tmp，不能使用或比较T090内存数字。
- raw SHA=`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`，manifest SHA=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`，lock SHA=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`。
- reducer/entry与全部bound bytes必须保持lock exact；不允许用代码修复import。

## 文件白名单

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_aggregate.json`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_receipt.json`
- 上述两文件`.tmp`仅运行中允许，成功后必须消失
- `projects/thesis-fso/worker-logs/step-091-ch4-canonical-reduction-publication-repair.md`
- 独立reviewer写 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/canonical-formal-statistics-independent-verification.md`

其余全部只读。

## 执行前门

1. 读sim-preflight、T091、D070/V045、T090 log、raw report与双锁；task-control CP032/epoch32 PASS。
2. aggregate/receipt与二者tmp absent；raw/manifest/lock/11项authority bytes exact；fresh19/pycompile5 PASS。
3. 无写入probe再次确认下述PYTHONPATH可import common、pure reducer与entry，且entry environment snapshot与lock exact。

## 唯一corrected invocation

在一个新的PowerShell进程内原样执行：

```powershell
$repo=(Resolve-Path '.').Path
$env:PYTHONPATH="$repo;$(Join-Path $repo 'projects\simulation');$(Join-Path $repo 'projects\simulation\explore\ch4-scaled-unitary-pilot-ls')"
python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_ch4_formal_production.py
```

不得增加其他环境变量或参数。若exit非0、stdout无正式terminal或留下tmp，立即停机，不再尝试、不删tmp。成功后实现者只记录wall、artifact SHA/size/terminal/grade与hash bindings，不另跑统计。

## 独立raw-only复算

完全继承T090合同。reviewer不得导入runner/reducer/entry，直接从raw counts独立重算pooled Jeffreys BER、required-SNR/crossing、seed2026083007 whole-curve bootstrap、seed2026083008 cell bootstrap、A/B/C/F grade以及mechanism/scene/pilot/mismatch summaries；每named comparison重置seed，不跨scene pooling。逐字段核aggregate/receipt并报告最大绝对差。

## 禁止

- 不修改entry/freezer/runner/reducer/tests/raw/manifest/lock，不重跑formal或添加seed；
- 不以T090内存计算作证据，不调threshold/grid/tau/bootstrap/grade，不隐藏B3；
- 不作图、写正文、检索、补实验、改Skill/controller或恢复Ch5。

## 终态

- `CH4_CANONICAL_FORMAL_STATISTICS_READY`：publication exit0、artifacts clean、独立P0/P1=0并按frozen grade接收；
- `CH4_CANONICAL_REDUCTION_PUBLICATION_INVALID`：任一失败；禁止第三次尝试、作图与解释性能。
