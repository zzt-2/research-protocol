# Task Brief: D0 ordinary canonical identity compiler — independent verification

> 来源: D017–D018 / V014 / T114 / step-160 | 产出位置: `projects/thesis-fso/worker-logs/step-161-d0-ordinary-canonical-identity-independent-verification.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_UNIT_TEST
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Independence / terminal

- 独立验收T114 final bytes；禁止用author helper、author PASS或author mutation作为oracle。
- 只写step-161，其他文件只读。目标10分钟、12分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_ORDINARY_CANONICAL_IDENTITY_COMPILER_INDEPENDENTLY_VERIFIED`；不等于I05/FULL完成。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
contract=50ae149a77588c34cedd2a2e8aab5078b6b4e3d4ea310ba85fe577f76f5ca170
schemas=e0770fb935b1a9fdfb822addf5cbecc94a148c1c6b28f312a7960298091906ec
ordinary_tests=cda5bd2027a664136670b14f91715be3eea0d3826ce9f4f140823711a0dff485
step160=b6c671ffac63d2ab874d49a2dcc511d0af288e7599ba9781ba0e68b8ca973538
old_schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step159=9821f06edf897412cac04ed8db69389b5ce20e7e4985120295f9d04fb701d762
```

## Fresh matrix

1. 从public owner view独立枚举七类raw PK，不调用author tests/helper；复算每个typed work payload与`d0c1-*`，逐条比对plan。精确 counts：per projection=`540/60,1620/1620,10800/10800,7200/3600,1200/600,21600/10800,7/7`，总=`42967/27487`。
2. 独立复算owner S2-off/BPS既有logical IDs和binding-manifest roots；抽核S2-on三operation、S3两phase、B2 shared pairs、S4七项。
3. Fresh mutations至少32项，覆盖missing/extra/duplicate/orphan/same-phase exchange、PK/work atom type/value/order/source、schema/kind/phase/operation/binding kind、owner/seal spoof、dataclass/graph tamper；wrong accept/reject=0/0。
4. 两次build递归nonprimitive sharing=0；tamper左图不影响右图；public assert fresh-recompile拒绝伪造。new API拒绝D0Contract/dict/旧plan。
5. 静态scope：新ordinary dataclass/API不得含cache/source/HMM/raw FULL；旧FULL factory/types行为未改；source相对old_schemas仅additive ordinary identity slice。
6. Fresh pytest：新文件4/4、显式旧四文件53/53，0 fail/error/skip/xfail/warning。
7. begin/end owner/source/tests、HEAD/staging、P05/cache/frozen artifacts/diff-check保护。

要求 independent assertions>=300、mutations>=32、all counts/goldens/pytest exact、P0/P1/P2=0/0/0；否则FAIL或INCOMPLETE。step-161记录命令、exit/stdout SHA、耗时和final log SHA。
