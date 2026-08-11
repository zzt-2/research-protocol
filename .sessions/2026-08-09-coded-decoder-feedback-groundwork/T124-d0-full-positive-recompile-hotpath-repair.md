# Task Brief: D0 FULL positive redundant-recompile hotpath repair

> 来源: T123 timeout / D023 | 产出位置: `projects/thesis-fso/worker-logs/step-170-d0-full-positive-recompile-hotpath-repair.md`
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

- 只修已定位的重复canonical recompilation hotpath；改`schemas.py`、`test_d0_schemas_statistics.py`、step-170。其他只读。
- 10分钟目标、15分钟硬停；禁止新抽象体系、owner/session其他文件、install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_AUTHENTICATED_FULL_POSITIVE_GREEN`；随后进入唯一fresh I05 batch verifier。

## Frozen failure

```text
schemas=be8c249a1d39b6089d970acc4a04e2c08ba8bba1e799f0e09e470ae1d0e7ec37
tests=14a8dcb7f979ebbd0186032d2c157bd3e288bacb7aa2c8ab1b59caf8056146fc
step169=7d64489ba178f2e46bd735f73a2a97f78f474162627032ce59a71c506b74cd5d
observed=focused_HMM_3_passed_6.04s; FULL_positive_timeout_364.1s
```

## Root-cause constrained repair

1. 先用instrumented focused test证明：正向node已先build一次ordinary bundle；`build_authenticated_full_authority`又调用`assert_ordinary_runtime_bundle`重建全量graph，`assert_authenticated_full_authority`再重复第三次。记录call count/分段时间，不能猜。
2. 保留public `assert_ordinary_runtime_bundle`的fresh canonical深验供最终batch verifier；只在authenticated FULL wrapper中改用factory-issued capability + external immutable fingerprint快验：
   - bundle必须是本进程public factory签发的exact object；copy/object.__new__/unissued拒绝；
   - issuance记录绑定owner_sha/identity seal与对records roots、aggregate fields、hard roots/payload、counts的current structural fingerprint；
   - FULL build/assert每次重算current fingerprint并与external issuance record比对，deep mutation/reseal/owner swap拒绝；
   - 不信任bundle内自带hash字段，不允许caller注册或提供fingerprint。
3. 可用identity registry+weak cleanup或等价最小机制；不得跳过owner `assert_frozen_owner_identity_authority`、HMM plan/runtime检查或FULL authority canonical hash。
4. 新负例至少8项：unissued clone、deep record/entry/output/root、ledger status/content、hard store、counts、owner mismatch；wrong accept/reject=0/0。
5. FULL positive node必须实际完成并产出64-hex authority；counts=`27487/22800/50287`。在ordinary bundle已建好后，FULL build+assert incremental wall time目标`<=30s`；整node硬上限300s。
6. 跑focused HMM 3 nodes + FULL positive +新增hotpath/negative nodes；随后整份statistics tests若时间允许，否则留给唯一batch verifier。不得第三次语义重试。

## Receipt

- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python3.11 `-B -p no:cacheprovider`。
- step-170记录pre/post call count与分段elapsed、RED/GREEN、authority hash、counts、mutations、stdout SHA、file hashes、保护、P0/P1/P2。
- 若fingerprint不能防deep mutation或仍超时，FAIL/INCOMPLETE；不得用放宽assert换PASS。
