# Task Brief: Ch4 formal execution lock final-state repair

> 来源: S028 / D067 / V042 / T087 | 产出: final-state-safe tests、replacement execution lock、独立终态验收
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 29
  action_class: CH4_FORMAL_EXECUTION_LOCK_REPAIR
  mission_checkpoint: CP029
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

修复T087两项pre-freeze测试在tracked lock存在时必失败的终态语义，精确作废SHA=`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`的首个canonical lock，并在runner/reducer/entry/scientific manifest字节不变的前提下生成、独立复核一个replacement lock。不得重跑ID29999或任何formal ID。

## 必读与不可变事实

1. sim-preflight全文、T087、D067、V042、step-087 worker log与T087 independent report；
2. scientific manifest SHA=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；
3. 已PASS smoke绑定的execution SHA：runner=`ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784`、reducer=`f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327`、entry=`da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0`；三者必须exact不变。
4. 首个tracked lock内容绑定未发现错误，但post-lock tests=`17/19`，故该SHA已由V042判INVALID，不得用于formal。

## 文件白名单

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_ch4_formal_production.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_execution_lock.json`（只允许exact删除已登记invalid SHA，并在最终freeze时唯一重建）
- `projects/thesis-fso/worker-logs/step-088-ch4-formal-execution-lock-repair.md`
- 独立reviewer写 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/formal-execution-lock-repair-independent-verification.md`

freezer、runner、reducer、entry、manifest、core/common/scaled/params均只读；若发现必须改其中任一项，立即INVALID并回D067，不扩大白名单。

## Stage A：在invalid lock仍存在时修测试

1. 先现场核canonical lock exact SHA、无`.tmp`、无formal raw/aggregate/receipt；fresh focused必须真实复现`17/19` RED。
2. 最小改两项测试，不删测试、不skip/xfail：
   - pure builder test不再永久要求canonical lock不存在，而是快照测试前canonical lock的存在性与字节，调用builder后要求状态和字节exact不变、无`.tmp`；
   - direct-CLI bootstrap test在subprocess内只对canonical lock存在性前置门做受控隔离，仍必须真实到达`projects.simulation.common` import并在`save_results`写入点前拦截；父进程要求canonical lock字节exact不变且无`.tmp`。
3. focused suite在invalid lock存在时必须`19/19 PASS`；pycompile、task-control、diff-check PASS；runner/reducer/entry与scientific manifest SHA exact不变。
4. 独立reviewer复放两项测试语义，P0/P1=0后才允许Stage B。

## Stage B：exact作废与replacement freeze

1. 删除前再次核canonical lock SHA exact等于已登记invalid SHA；不匹配立即停机。删除只针对该一个未提交invalid artifact，不触碰任何其他文件。
2. lock缺失状态重新跑同一focused suite，必须`19/19 PASS`；五文件pycompile、task-control、bindings PASS。
3. 只运行一次 `python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/freeze_ch4_formal_execution_lock.py`。若非0、出现stale tmp或任何拒绝，立即停机，不重签。
4. replacement lock生成后不得再改tests或任何bound文件；在lock存在的最终仓库状态fresh focused必须仍`19/19 PASS`，actual hashes必须与lock一致，无`.tmp`、无formal artifacts。
5. 独立reviewer现场复核并给P0/P1/P2；只有P0/P1=0才可terminal=`CH4_FORMAL_EXECUTION_LOCK_REPAIR_READY`。

## 禁止

- 不重跑ID29999，不运行IDs`30000..30127`，不生成formal raw/aggregate/receipt；
- 不修改scientific manifest、runner/reducer/entry/freezer/core/common/scaled/params；
- 不检索、补Groundwork、恢复Ch5、作图、写正式正文或修改Skill/controller；
- 不通过删除断言、skip、xfail或仅在lock缺失时跑测试制造假绿。

## 终态

- `CH4_FORMAL_EXECUTION_LOCK_REPAIR_READY`：absent/present两种状态19/19、replacement lock actual bindings与独立final P0/P1=0；
- `CH4_FORMAL_EXECUTION_LOCK_REPAIR_INVALID`：任一不可变SHA变化、测试非全绿、replacement失败或final binding不自洽；formal IDs继续禁止。
