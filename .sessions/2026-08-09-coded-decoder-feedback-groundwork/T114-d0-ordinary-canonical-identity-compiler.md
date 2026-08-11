# Task Brief: D0 ordinary canonical identity compiler

> 来源: D017–D018 / V013 / T112–T113 | 产出位置: `projects/thesis-fso/worker-logs/step-160-d0-ordinary-canonical-identity-compiler.md`
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

## 前置与范围

- 只有 T113 terminal=`D017_OWNER_IDENTITY_LOADER_SEAL_INDEPENDENTLY_VERIFIED` 后才可开始 GREEN。
- 只改 `projects/simulation/explore/coded-decoder-feedback/schemas.py`，新增 `projects/simulation/tests/test_d0_ordinary_identity.py`，写 step-160。owner/contract/channel/旧 tests/session/P05 只读。
- additive identity-only：不得改/删旧 FULL factory 与 caller-forgeable plan；不得实现 cache/materialization provenance、HMM、raw FULL positive。
- 目标 12 分钟、15 分钟硬停止；禁止 install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_ORDINARY_CANONICAL_IDENTITY_COMPILER_READY_FOR_INDEPENDENT_VERIFICATION`，不等于 I05/FULL 完成。

## 唯一输入与最小 API

- public build/assert API 唯一 authority 参数必须是 exact `D0OwnerIdentityAuthority`；入口先调用 `assert_frozen_owner_identity_authority`，拒绝 `D0Contract`、dict 与旧 preexecution plan。
- 新 typed frozen/slots 值对象至少表达：`TypedIdentityField(name, atom_type, value)`、typed consumer PK、logical identity payload/ID、ordinary binding（含 projection/table/binding kind）、不可直接构造的 ordinary plan（含 owner/identity seals、computations、bindings）。具体命名可调整，但不得包含 `cache_status/source_computation_id`。
- build 两次必须生成递归 nonprimitive sharing=`0` 的 fresh graph；assert 必须 fresh recompile exact compare，不信任对象自带 seal/digest。

## Strict RED → GREEN

1. 先只写新 tests；缺 API 时至少 4 个目标节点真实 RED，记录 exit/stdout SHA。禁止用故意错误断言造 RED。
2. canonical bytes严格按 owner 1066–1112、1413–1501；logical ID=`d0c1-`+canonical logical-computation payload SHA256。所有 domain/schema/kind/phase/operation/type/field order从 authenticated owner view读取并验证，不由 raw caller提供。
3. 编译七 projection：S2_off、S2_on、S3、BPS、B2_clean、B2_controlled、S4。exact binding/logical counts：`540/60, 1620/1620, 10800/10800, 7200/3600, 1200/600, 21600/10800, 7/7`；总计 `42967/27487`。
4. S2-off 必须九 fixture→同 ID；BPS 两 pol→同 ID；B2 clean 两 pol→同 ID；B2 controlled 两 row-pol→同 ID。S2-on 三 operation、S3 两 phase、S4 七项 exact。
5. 从 plan 独立复算 owner 既有 S2-off/BPS logical ID 与 binding-manifest golden；不得改 golden。
6. fail closed：missing/extra/duplicate/orphan、same-phase ID exchange、typed atom/value/source/order、kind/phase/operation/schema/binding kind、owner/seal spoof、wrong input type；至少 24 个 mutation。
7. fresh/nonalias：两次 build 递归 nonprimitive sharing=0；unsafe tamper 左图不影响右图，assert 拒绝 tampered plan。
8. GREEN：新文件全量 + 显式既有四文件回归，0 fail/error/skip/xfail/warning；P0/P1/P2=`0/0/0`。

## 保护与返回

- begin/end SHA：owner/contract/channel/schemas/old tests/session governance/HEAD/staging/P05/cache；只允许 scope 三文件变化。
- step-160记录 RED/GREEN 命令、exit/stdout SHA、counts/mutations/nonalias、source/test/log SHA与未运行项。
- 只返回 PASS terminal、FAIL 或 INCOMPLETE；遇首个不可在时间盒内关闭的 blocker 立即收口。
