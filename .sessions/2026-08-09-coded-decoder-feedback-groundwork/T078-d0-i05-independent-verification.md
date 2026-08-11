# Task Brief: D0 I05 independent schema verification

> 来源: step-119 executor PASS / frozen schemas source+test | 产出位置: `projects/thesis-fso/worker-logs/step-124-d0-i05-independent-verification.md`
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

## 审查问题 / fail 条件

- 问题：独立上下文能否逐字段/逐关系证明 11 类 owner rows、PK/FK/cardinality 和 S4 seven schema fail closed，而非只通过现有 47 个 mutation？
- FAIL：任何 P0/P1；owner 字段/enum/cross-field identity 遗漏；整个 group/table 删除、extra orphan/reverse binding 或 cross-stratum 污染仍通过；schema import/I/O/selection/reduction；或 fresh tests 不全 GREEN。

## 冻结输入

```text
schemas.py=c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68
test=ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d
step-119=4c47783657870a762d620c54e8c70fcec15d13d81490641119695788df4b3f86
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-096=projects/thesis-fso/worker-logs/step-096-d0-contract-test-stat-map.md
step-097=projects/thesis-fso/worker-logs/step-097-d0-stat-contract-repair-design.md
step-102=projects/thesis-fso/worker-logs/step-102-d0-dev-freeze-artifact-audit.md
step-103=projects/thesis-fso/worker-logs/step-103-d0-dev-freeze-reverifier.md
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

Create only `projects/thesis-fso/worker-logs/step-124-d0-i05-independent-verification.md`。production/tests/step-119 只读，不修复。

## 独立验证

1. 核冻结 SHA/保护；读 owner、step-096/097/102/103/105/106、schemas/test/log。建立 owner→field/type/enum/local invariant/PK/FK/cardinality 对照，findings-first，P0/P1/P2。
2. fresh 跑 SS01/02/11 exact nodes、完整 schema 文件、I02 contract 回归；记录 commands/count/duration/output SHA/skip/xfail/warning。
3. 临时 one-shot mutation matrix（不落 repo），至少：
   - 每表 missing/extra/reordered、bool-as-int、numeric/string coercion、NaN/Inf、bad SHA/decimal/hex、wrong const/enum/min/max；roundtrip 不别名；frozen+slots；
   - 所有 owner cross-field identities：S1 count/event/positions，fixture↔boundary/k，error≤total，projection/method，S3 truth/candidate/cost，S4 pass/count，ledger BP/cache/source/content，tuple↔M/N，pilot-count/N、transmitted-symbol/N、delivered bits/errors、controlled target/sentinel/objective inclusion等。仅在 owner 明确归属本 schema 层时判缺陷；
   - PK duplicate、cell/seed FK、computation forward+reverse FK、cache source reverse binding；删除单行、删除整个 group、删除整张已声明 table、额外 orphan ledger/row、跨 seed/cell/method/role；S2 9 fixtures×(on3/off1)、S3每 case十 candidate、B2 target+sentinel bijection。判断 partial-bundle 是否 owner 允许，不能凭猜测；
   - S4 7/7 identity/order、6/8/dup/unknown/wrong type、contract/receipt/evidence FK、passed iff failed0，且 entry 不得含 seed/cell/boundary。
4. 静态扫描 I/O/RNG/selection/reduction/science、loose kwargs/coercion、test-specific constants 无 owner 来源。每 finding 给精确复现、owner 指针、影响和最小修复方向；若 owner 对 completeness 允许 partial bundle，明确记录 why，不误报。
5. 终检只 step-124 新增；p05/cache/staging/HEAD 不变；不 benchmark/science/web/install/commit/push。≤15 分钟，不足 INCOMPLETE。

## 返回

P0/P1/P2 counts；fresh unit/mutation counts；log SHA；terminal=`I05_VERIFIED_READY_FOR_BATCH1`、`I05_VERIFICATION_FAIL` 或 `INCOMPLETE`。
