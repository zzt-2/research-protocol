# Task Brief: D0 I05 P1-3 repair — tuple/N overhead identities

> 来源: step-124 independent FAIL P1-3 | 产出位置: `projects/thesis-fso/worker-logs/step-129-d0-i05-overhead-identity-repair.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Review disposition / narrow scope

- 接受 P1-3：独立 enum 不能证明 tuple/N 与 pilot/total-symbol denominator一致，step-124 四类复现均直接影响 goodput/NLL。
- 本任务只修单一 N→(pilot,total) identity owner，不碰 completeness 或 ledger（另拆任务）。
- 否决：修改 owner/其他模块、硬编码只针对 M2_N100、放宽 schema，或 15 分钟不收敛。

## 冻结输入

```text
schemas.py=c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68
test=ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d
step-119=4c47783657870a762d620c54e8c70fcec15d13d81490641119695788df4b3f86
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
3. Create `projects/thesis-fso/worker-logs/step-129-d0-i05-overhead-identity-repair.md`

## Test-first repair

1. production 前追加 `test_tuple_overhead_identities_fail_closed`。用 owner mapping exact：N10→pilot684,total6860；N20→325,6501；N100→64,6240；N200→32,6208。覆盖：
   - `bps_dev_score` tuple/M/N 与 total；
   - `b2_hmm_grid_chunk` tuple/M/N 与 pilot_count；
   - `b2_tuple_clean_dev`/`controlled_dev` 从 tuple_id 推 N 后与 total；
   - 四 N valid cases；每类 wrong-but-enum-valid mutation拒绝。
2. old production 上跑新 exact node，必须目标 RED；**先把** command/test/source/output SHA 与 step-124复现写 step-129，再改 production。
3. 单一 immutable N map 驱动全部四表 `_local_invariants`；不得复制四套漂移条件。保持 B/Nw 等 dev grid维度不受影响。
4. 跑新 GREEN、原 SS01/02/11、full schema、I02 regression；记录 counts/output，无 skip/xfail/warning。
5. 日志保留 P1-1/P1-2=`PENDING`，不得宣称 I05 READY。终检三目标/保护；无 benchmark/science/web/install/commit/push。≤15 分钟。

## 返回

RED/GREEN/counts/SHA；terminal=`I05_P1_3_REPAIRED_P1_1_P1_2_PENDING`、`INCOMPLETE` 或 blocker。
