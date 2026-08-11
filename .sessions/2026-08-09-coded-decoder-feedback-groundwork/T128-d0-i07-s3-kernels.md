# Task Brief: D0 I07 slice B — S3 reduction and lambda chronology

> 来源: d0-implementation-plan I07 / SS08–SS10 / T126 | 产出位置: `projects/thesis-fso/worker-logs/step-174-d0-i07-s3-kernels.md`
> 日期: 2026-08-11

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

## Scope / terminal

- 继续只改 `statistics.py`、`test_d0_schemas_statistics.py`、step-174；其他只读。
- 先写并跑SS08–10真实RED，再最小GREEN。15分钟硬停；禁止整份statistics FULL、I/O/YAML/scientific rows/benchmark/science/MVE/install/stage/commit/push。
- PASS=`D0_I07_STATISTICS_KERNELS_GREEN`；随后I07+I08只做一次fresh batch verifier。

## SS08–SS10 exact acceptance

1. 每个S3 case必须恰10 candidates，exact tie order=`NOOP,B04_K1,B04_K2,B04_K3,B08_K1,B08_K2,B08_K3,B12_K1,B12_K2,B12_K3`；truth candidate由frozen row给出。score降序、tie按该顺序。
2. exact changed-CW vector=`16,12,12,12,8,8,8,4,4,4`总和88；cached reads=`0,4,4,4,8,8,8,12,12,12`总和72。不得把cache read计成decode，不得跨case共享。
3. `select_s3_lambda(dev_rows,*,dev_rows_sha256,freeze_receipt_sha256)`只接受`S3_CANDIDATE_DEV`；枚举`0.25,0.5,1.0,2.0,4.0`，词典序 maximize macro MRR → macro top1 → smaller lambda；全平局冻结`0.25`。返回现有I05 typed `S3LambdaFreezeRow`，`test_rows_read_during_selection=false`。
4. `reduce_s3(test_rows, freeze)`只接受TEST与已冻结lambda；先10 candidate→case metrics，再case→cell mean，再hard/mid/clean等权macro。paired RR delta必须同case内`fused_rr-pilot_rr`，bootstrap cluster=seed，禁止按5400 candidate rows或pol聚类。
5. 金标：全score tie且truth=`B08_K2`时rank=6、RR=`1/6`、top1=0；三cell fused_top1=`1,.5,0`=>macro `.5`；paired delta=`.5,0,-.5`=>macro `0`。
6. frozen/slotted result dataclasses；复用T126 `bootstrap_paired`，每stratum独立PCG64。纯函数，无文件、全局RNG、truth-view或scientific verdict。
7. fresh negatives至少10项：candidate缺失/重复/unknown；truth不在case；cost vector偏离；DEV/TEST混用与TEST leakage；freeze hash/type/lambda错误；跨case source/cache；candidate/pol聚类哨兵。wrong accept/reject=0/0。

## Commands / receipt

- RED：SS08、SS09、SS10三个节点。
- GREEN：SS08–10，再显式SS01–11局部门；不要运行`test_authenticated_full_positive_actual_50287_ledger_authority`或整文件。
- 固定`PYTHONDONTWRITEBYTECODE=1`,`PYTHONHASHSEED=0`。step-174记录RED/GREEN、tests/time/stdout SHA、goldens/negative、files SHA、HEAD/staging/P05、P0/P1/P2。
