# Task Brief: D0 HMM runtime + authenticated FULL positive

> 来源: D015 / D020–D022 / T122 / I05 closure map | 产出位置: `projects/thesis-fso/worker-logs/step-169-d0-hmm-runtime-full-positive.md`
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

- 实际代码片C。只改`schemas.py`、`test_d0_schemas_statistics.py`与step-169；其他code/tests/owner/session/P05/cache只读。
- 12分钟目标、15分钟硬停；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_HMM_RUNTIME_FULL_POSITIVE_READY_FOR_BATCH_VERIFICATION`；这是I05 author closure候选，仍需唯一fresh batch verifier。

## Frozen input

```text
schemas=a344a299ee07aa603408ccd9c2f9cad78a9b4f56b64a1b29ccb62a421058aa4e
ordinary_tests=ef0b2b7e7b70d1add0fc0e45180455a857cf5d38f9eb58b7ce06d4ea4d04d234
schemas_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step168=ac90a6476e4a61cf02c3b8e1ff84e640c0743ac300c00f64685c9a7d41b7f551
```

## Required implementation

1. TDD RED first：focused nodes必须因HMM runtime content与authenticated FULL positive APIs缺失而真实失败。
2. 新增frozen typed `ResolvedMemberContent` 与 `HmmRuntimeAggregateContent`（或等价）：exact owner schema/field order；ordinal从0连续；member count按role=10/90；`computation_ids_manifest_sha256`与ordered content SHA均绑定；binary64输入lossless转exact rational，输出canonical numerator decimal + denominator power2；content root只hashpayload。至少复算owner clean/target/sentinel runtime goldens或等价代表向量。
3. 新增owner-authenticated HMM logical/preexecution compiler：只消费`D0OwnerIdentityAuthority`，按owner tuple/seed/cell/pol/fixture/role顺序生成22,800 trajectory identities与263,520 chunk bindings；cache规则为M3_N100→M2_N100、sentinel→matching clean、M3_N100 sentinel→M2 clean direct leaf；counts=9600 executed/13200 cache，禁止caller-supplied namespace/plan冒充final authority。
4. 新增final authenticated FULL authority/factory（可保持旧factory作兼容但不得作为final runtime入口）：输入final owner authority + T122 `OrdinaryRuntimeBundle` + canonical HMM plan/runtime content manifest；由factory生成而非caller提供两个preexecution plans。它必须绑定raw/table authority、ordinary27487、HMM22800与总ledger50287，ordinary ledger content=root，HMM source/content/cache/cost规则闭合。
5. deterministic positive gate必须实际构造一个final FULL authority并通过public assertion：ordinary graph用T122全量bundle；HMM identity/ledger全量22,800枚举；runtime aggregate至少逐role/EXECUTED/CACHE_READ/source normalization代表项真实构造并验证，263,520 chunk count/identity集合由canonical plan exact绑定。不得仅断言硬编码数字或把`EXPLICIT_PARTIAL`改名为FULL。
6. 保留旧FULL tests兼容或明确降为legacy schema authority；final public assertion必须拒绝caller-forged old plans、owner/ordinary/HMM swap、missing/extra identity、source chain/content mismatch、ledger total/content/status/cost drift、runtime ordinal/member/sum/root reseal、partial masquerade。至少18 fresh mutations，wrong accept/reject=0/0。

## Test/protection gate

- GREEN先跑新增focused nodes，再整份`test_d0_schemas_statistics.py`；不跑五文件回归（留给唯一batch verifier）。0 fail/error/skip/xfail/warning。
- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python3.11 `-B -p no:cacheprovider`。
- step-169记录RED/GREEN、HMM/chunk/ledger counts、positive authority hash、goldens/mutations、elapsed/stdout SHA、file hashes与HEAD/staging/P05/cache保护。
- 若15分钟内full positive无法闭合，保留可运行的HMM runtime/owner compiler增量并诚实INCOMPLETE；禁止造假FULL或再开设计审查。
