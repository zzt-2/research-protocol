# Task Brief: D0 owner consumer binding-kind authority repair

> 来源: D016 / V010 / T105 step-151 | 产出位置: `projects/thesis-fso/worker-logs/step-152-d0-owner-binding-kind-authority-repair.md`
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

## Scope / terminal

- 只修T105两项P1的同一根因；只写owner与step-152，不改session/source/tests/schemas。
- PASS上限`OWNER_BINDING_KIND_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION`；不得据此接收D015或实施schema。
- 不跑pytest/benchmark/science/MVE；目标8分钟、10分钟硬停止。

## Frozen receipt

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d
R001=ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd
decisions=ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7
verifications=7f76040ffe3e9ca0d21abda03f72b8bcdd3ba3e5cc14d950051a892e55485bcb
step151=c1b0f39ed0903735387d6d12aaf5963c6a400215da81fa649a4f0e9b9459e535
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
```

## Mandatory RED before owner edit

Strict duplicate-key parse并断言以下11个exact authority位置均缺失；必须非零后先把RED命令语义/output/SHA写step-152：

1. `payload_schemas.consumer_binding_manifest.exact_binding_kind`
2. `consumer_bindings.projections.{S2_off,S2_on,S3,BPS,B2_clean,B2_controlled,HMM_chunk,S4}.exact_binding_kind`（8项）
3. `golden_vectors.S2_off_nine_to_one.inputs.binding_kind`
4. `golden_vectors.BPS_dual_pol_shared.inputs.binding_kind`

若RED不红或任一位置已有冲突值，停止不改owner。

## Exact additive repair

上述11个位置全部写同一exact YAML scalar：

```yaml
exact_binding_kind: LOGICAL_COMPUTATION_ID
```

golden inputs字段名固定为`binding_kind`：

```yaml
binding_kind: LOGICAL_COMPUTATION_ID
```

不得改字段顺序schema、consumer PK projection、logical IDs、bindings、golden roots或任何其他owner内容。尤其两个roots必须保持：

```text
S2=ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6
BPS=51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f
```

## Fresh author verification

- strict duplicate YAML；11/11位置exact且无其他`binding_kind` authority值。
- 从golden保存inputs（包括新增literal）独立重建S2/BPS manifest，logical IDs与roots 2/2 exact。
- 重跑最终owner全量静态门：128/128 literals、3/3 roots、全部owner goldens、>=12 mutations、6/6 counts、projection/permission/approved aliases/protection；mismatch=0。
- 将新增11项从parsed owner投影删除后，与prechange owner deep-equal；science/permission/count/root drift none。
- owner/source/tests/session frozen hashes、HEAD/staging/P05/cache与diff-check；不得用step-151旧FAIL当新PASS。

## Environment / return

Windows Python 3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；不得install/commit/push/stage。返回terminal、RED、full totals、root复算、drift/protection、owner与step152 SHA。
