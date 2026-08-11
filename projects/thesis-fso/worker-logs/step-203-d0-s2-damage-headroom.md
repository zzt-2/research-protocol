# Step 203 — D0 S2 B1 damage / O1 headroom

STATUS=BLOCKED

## 结论先行

S2 未运行。冻结 owner/schema/reducer 不能在“不执行、不裁决 B2”的同时合法表示和归约 B1 damage / O1 headroom；T131 明确规定此情况必须报告真实 blocker、不得改指标。因此没有 PID、checkpoint、raw、summary 或 receipt，也没有任何 damage/headroom 数字。

- `S2_VERDICT=INVALID`
- `formal_science_disposition=S2_NOT_RUN_OWNER_SCHEMA_BLOCKER`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`

## Blocker 证据

冻结 workload 的 B1/O1-only 合法行数是：

- 10 seeds × 3 cells × 2 polarizations × 9 fixtures × (`B1-on` + `O1-on` + fixture-aligned `B1-off`) = **1620 typed rows**。

但 `statistics.reduce_s2` 的固定合同是：

- 精确要求 **2160 typed rows**；
- 每个 seed/cell/polarization group 精确要求 36 rows；
- 每个 fixture 必须同时存在 `B1/B2/O1 on` 和 `B1 off`；
- reducer 无条件读取 B2 error counts 并计算 coverage/`ZERO_RECOVERABLE_HEADROOM` terminal。

fresh probe 输出：

```text
full_rows 2160 no_b2_rows 1620
reduce_no_b2 SchemaError statistics: S2 requires exactly 2160 typed rows
status_placeholder SchemaError s2_method: exact fields/order required; missing=[] extra=['evaluation_status']
null_placeholder SchemaError s2_method.affected_cw_errors: must be an exact int (bool/coercion forbidden)
```

即：

- `S2MethodRow` 没有 `NOT_EVALUATED`/status 字段，额外字段 fail-closed；
- `affected_cw_errors` 必须是 exact int，不能用 `null` 表示未评估；
- 填入任何整数 B2 placeholder 都会制造 B2 数字，并被 reducer 实际用于 coverage/terminal，违反 T131“不得制造 B2 数字、不得执行或裁 B2”。

## TDD RED

按期望接口写了临时 focused test：1620 个 typed B1/O1 rows 调用 `statistics.reduce_s2_damage_headroom(rows)`。命令：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest 'projects/simulation/tests/test_d0_science_s2_blocker.py' -q
```

结果：

```text
1 failed in 0.38s
AttributeError: module 'statistics' has no attribute 'reduce_s2_damage_headroom'
```

该 RED 证明当前没有 owner-authorized 的 B1/O1-only reducer。根据 T131 明示 blocker 条款，没有实现新的 reducer、没有改 `statistics.py`/schema/owner；临时 RED test 已删除，避免给工作树留下永久失败测试。无 GREEN，因为合法修复需要先修改冻结 owner/schema，而这超出本任务授权。

## 未执行项

- PID：无
- checkpoint/raw/summary/receipt：无
- exact workload：未启动，0/60 base clusters
- damage point/CI/positive cells：NOT_EVALUATED
- recoverability point/CI/positive cells：NOT_EVALUATED
- invalid replicate counts/terminals：NOT_EVALUATED
- B2：未调用、未生成 row、未裁决

## 解阻条件

需要新的显式 owner/schema 决策，二选一：

1. 冻结一个 B1/O1-only typed projection及对应 reducer/cardinality；或
2. 给 S2 row 增加不会进入 coverage 的显式 `NOT_EVALUATED` B2 语义，并同步修改 reducer。

两者都会改变当前冻结统计/serialization contract，不能由本 worker 在 T131 内自行决定。

## 保护核验

- owner YAML：未修改。
- `projects/simulation/common/`：未修改。
- S1 artifacts：未修改。
- S2以后代码：未创建或修改。
- 未 stage/commit/push。
- P05：未触碰；4/4 SHA protection 由本轮 fresh verification 复核。
