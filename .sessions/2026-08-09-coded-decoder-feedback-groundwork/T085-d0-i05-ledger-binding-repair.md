# Task Brief: D0 I05 P1-2 repair — bidirectional computation/cache binding

> 来源: step-124 independent FAIL P1-2 + step-129 P1-3 closed | 产出位置: `projects/thesis-fso/worker-logs/step-131-d0-i05-ledger-binding-repair.md`
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

- 接受 P1-2：forward raw→ledger 不足；raw cache fields可与其 ledger矛盾，且额外 S2 decoder materialization可无消费者。
- 本任务只修 phase/operation-aware bidirectional ledger/cache binding；P1-1 completeness仍 pending。不得机械拒绝合法无直接 row consumer 的 `HMM_GRID_SCORE`/`OTHER_S4_CHECK`。
- 否决：改 artifacts/statistics/owner、把所有 ledger 强制一对一（off projections合法 many→one）、或15分钟不收敛。

## 冻结输入

```text
schemas.py=c07eb027a4a3fd8efa7d49d5885800f9cc55986b6b4e56e6feb4bde3db22e3fb
test=0a02fb25cfda4271293e7f964092fc8b0b85e90268e4e26f9a9b93d919592895
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
3. Create `projects/thesis-fso/worker-logs/step-131-d0-i05-ledger-binding-repair.md`

## Test-first repair

1. production 前追加 `test_ledger_bidirectional_binding_fail_closed`，覆盖 step-124 两 exact repro，并至少：
   - extra unreferenced `phase=S2,operation=B1_DECODE` ledger拒绝；
   - BPS/controlled raw `cache_status/source_computation_id` 与其 ledger mismatch拒绝；ghost source/content mismatch拒绝；
   - S2 method↔expected B1/B2/O1 operation/phase，S3↔CANDIDATE_DECODE，BPS_DEV↔B1，B2 tuple↔B2；wrong mapping拒绝；
   - 合法九 off rows many→one computation接受；同 computation跨不兼容 rows拒绝；
   - owner允许的 standalone `HMM_GRID_SCORE` 与 `OTHER_S4_CHECK` 明确正例，不因机械 reverse FK 被杀。
2. old production跑 exact node RED；先写 step-131 receipt（test/source/command/output SHA）再改 production。
3. 最小实现 consumer index + phase/operation mapping：所有有 `computation_id` raw先 forward FK；有 cache fields者与 ledger exact一致；需消费的 decoder ledger至少一个且仅由兼容 rows消费；many→one按 owner合法；cache source/content反向保持。exception必须枚举具体 operation，deny-by-default，不用模糊 phase prefix。
4. 新 GREEN后跑原 SS01/02/11、overhead regression、full schema、I02；记录 mutation counts，无 skip/xfail/warning。
5. P1-1显式 pending，不宣称 I05 READY。终检三目标/保护；无 benchmark/science/web/install/commit/push。≤15分钟。

## 返回

RED/GREEN/counts/SHA；terminal=`I05_P1_2_P1_3_REPAIRED_P1_1_PENDING`、`INCOMPLETE` 或 blocker。
