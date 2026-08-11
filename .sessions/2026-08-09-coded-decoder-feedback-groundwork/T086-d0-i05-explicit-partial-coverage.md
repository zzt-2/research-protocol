# Task Brief: D0 I05 P1-1a — explicit partial manifest and exact coverage gate

> 来源: step-124 P1-1 + independent completeness design / P1-2/P1-3 closed | 产出位置: `projects/thesis-fso/worker-logs/step-132-d0-i05-explicit-partial-coverage.md`
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

## Review disposition / slice boundary

- 接受 P1-1；拒绝仅 count、`require_complete` bool、observed-rows自生成manifest。
- 本切片只建立显式 `EXPLICIT_PARTIAL` 类型/factory/validator与 exact table/key/multiplicity coverage，关闭 synthetic/partial bundle 的 vacuous PASS；FULL factory/formulas另拆下一任务，因此仍不得宣称 I05 READY。
- 不把 artifact filenames/atomic I/O 塞进 schemas。

## 冻结输入

```text
schemas.py=7f8ae88dfc141f5259a1b2c3753aeea4071af907a024267575a5d396f1fee60b
test=5a9b255654b8460009dc2e5f69a67598887d660697ec53d9dc70c0a9b97d3728
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
step-131=86e4b831e5195c97562d3c16dc8b8fd1c2f1d75e209a6af77274526b040abca8
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
3. Create `projects/thesis-fso/worker-logs/step-132-d0-i05-explicit-partial-coverage.md`

## Test-first scope

1. production 前新增：
   - `test_partial_manifest_exact_coverage_fail_closed`
   - `test_full_validator_rejects_partial_manifest`
   并把现有 miniature `_relational_dataset` 改成由**测试常量/owner axes**显式声明 expected identities，调用 `validate_partial_relations`；禁止从 produced rows反推期望。
2. regression 至少覆盖：partial factory拒绝 zero table/zero projection；baseline接受；`{}`、delete/empty declared table、extra undeclared table拒绝；S2整36-row group、S3整10-row case、controlled整2-row group做 count-preserving identity substitution仍拒绝；删除一 expected identity再补一个合法enum但未声明identity拒绝；FULL validator接PARTIAL拒绝。
3. old production跑新 nodes取得目标 RED，**先写 step-132 receipt** 后改 production。
4. 最小 API（命名可等价但语义不可弱化）：
   - frozen/slotted `CellDomain(name, exact_values)`、`SeedSet(record_type, exact_values)`；不再只有 first/last；
   - `IdentityProjection(fields, expected_key_count, expected_keys_sha256, multiplicity_by_key_sha256)`；canonical key encoding稳定、混合类型无序歧义；
   - `TableExpectation(table, projections)`；`RelationalManifest(scope, cell_domains, seed_sets, tables, coverage_sha256)`，scope不可由默认bool降级；
   - `build_partial_relational_manifest(...)` 只接受非空显式 expectations并校验coverage digest；helper可从**caller-supplied expected keys**构造projection，但绝不能接 observed rows；
   - `validate_partial_relations(rows, manifest)` 先 exact table set + 每projection Counter/key/multiplicity hash，再跑现有 row/PK/FK/group relations；
   - 现名 `validate_relations` 改为 `FULL_D0_ARTIFACT`-only，PARTIAL必拒绝；FULL factory下一切片实现。
5. 保持 row models/row_from_mapping API、P1-2 ledger与P1-3 overhead tests；跑新 nodes、全部既有 schema tests、full file、I02。无 I/O/RNG/selection/reduction。
6. 日志明确 `P1-1a closed / P1-1b FULL factory pending`；终检三目标保护；≤15分钟，无 benchmark/science/web/install/commit/push。

## 返回

RED/GREEN/mutation counts/SHA；terminal=`I05_PARTIAL_COVERAGE_CLOSED_FULL_FACTORY_PENDING`、`INCOMPLETE` 或 blocker。
