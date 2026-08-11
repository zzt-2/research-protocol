# step-124 — D0 I05 independent schema verification

> 2026-08-10 | verifier: `/root/i04_codec`（未参与 I05 实现） | task: T078
> Verdict: **FAIL** | terminal: `I05_VERIFICATION_FAIL`

## 1. Findings first

```text
P0=0
P1=3
P2=0
TERMINAL=I05_VERIFICATION_FAIL
```

### P1-1 — required table/group completeness is vacuous under deletion

**Owner oracle**：owner `:1060-1061` 声明全部 raw/dev/ledger 文件必需，写前必须经过
`exact_cardinality` 与 `complete_seed_manifest`；S2 每 group 需 9 fixtures×(on B1/B2/O1 +
off B1)（`:590-592`），S3 每 case 恰好十 candidate（`:611-612`），controlled B2 每
fixture 恰好 target+sentinel（`:979`），dev tables 另有 exact rows `7200/1200/21600`
（`:988,:1005`）。T078 明确要求整个 group/table 删除必须 fail closed。

**Source cause**：`validate_relations` 在 `schemas.py:434-458` 只遍历调用方提交的 table；
S2/S3/controlled 在 `:473/:495/:504` 用 `.get(table, ())`。不存在或空 table 产生零 group，
没有任何 required-table/cardinality check 被触发。

**Fresh reproductions**：下列均 `ACCEPTED`：

- `{}` empty bundle；
- 删除或置空 `s2_method`；
- 删除或置空 `s3_candidate`；
- 删除或置空 `b2_tuple_controlled_dev`。

**Impact**：完整 raw table/group 可消失而 relational gate 仍返回成功，无法支持 artifact
“complete”或后续 equal-cell/seed reduction。定为 P1。

**Minimum repair direction**：给完整 artifact validator 一个明确 required-table/cardinality/
manifest contract；若确需 partial bundle，应另设显式 mode/type，不能让默认 validator 对空集
vacuous PASS。

### P1-2 — computation/cache relations are only partially one-way

**Owner oracle**：owner computation ledger 要求 cache source/content binding（`:640-671`），
S2 projection 只由合法 computation materialize；T078 要求 forward+reverse FK、extra orphan
ledger/row 和 cache source reverse binding 均 fail closed。

**Source cause**：`schemas.py:460-466` 只检查 raw row `computation_id → ledger`；`:468-471`
只检查 ledger cache row `source_computation_id → ledger source/content`。它没有核 raw row 的
`cache_status/source_computation_id` 与其 ledger row一致，也没有核 S2-phase decoder ledger
是否被合法 S2 row 反向消费。

**Fresh reproductions**（均 `ACCEPTED`）：

1. 在 baseline bundle 追加一个 `phase=S2 / operation=B1_DECODE / computation_id=orphan-s2-extra`
   的 EXECUTED ledger，无任何 S2 row 引用；
2. 把合法 controlled B2 row 改为 `cache_status=CACHE_READ /
   source_computation_id=ghost-source`，其 `computation_id` 仍指向一个 EXECUTED ledger。

**Impact**：raw row 可伪报 cache provenance，或 ledger 可多计 materialized S2 cost，却仍过
schema/relations，破坏 owner 的 cost/source/content ledger。定为 P1。S4 的
`OTHER_S4_CHECK` 可无 raw-row consumer；修复须 phase/operation-aware，不能机械禁止所有
无消费者 ledger。

### P1-3 — tuple N is not bound to pilot count / transmitted-symbol count

**Owner oracle**：owner `:273-274` 冻结 N→pilot count：`10→684, 20→325, 100→64,
200→32`；`:841-842` 冻结 `total=32+6144+pilot_count(N)`，并在 `:1007` 后按 tuple
冻结 periodic-pilot fraction。T078 明确要求 pilot-count/N 与 transmitted-symbol/N identity。

**Source cause**：`schemas.py:145/:159/:175/:193` 只分别检查 enum；`_local_invariants`
只做 tuple→M/N（`:336`），没有把 N 绑定到 pilot/total count。

**Fresh reproductions**（均 `ACCEPTED`）：

- `bps_dev_score`: `M2_N100, N=100, total_transmitted=6208`（应为 6240）；
- `b2_hmm_grid_chunk`: `M2_N100, N=100, pilot_count=32`（应为 64）；
- clean/controlled B2 tuple：`M2_N100, total_transmitted=6208`（应为 6240）。

**Impact**：row 的 tuple identity 与 overhead/denominator 可互相矛盾，导致 goodput/NLL
normalization 和 freeze comparison失真。定为 P1。

**Minimum repair direction**：由单一 frozen N→pilot/total map 同时驱动所有四表 local
invariants；不得仅保留独立 enum。

## 2. Frozen inputs / protection preflight

| input | expected SHA256 | observed | result |
|---|---|---|---|
| `schemas.py` | `c183d1d0e5a8844e0a7baf6add5c4334056935cb6e7c888ca9126d6e14e4ad68` | same | MATCH |
| frozen test | `ed4a9239d6f87a16c6f30d841288d9ee878ea4b66201483b0d4d27f77d4a579d` | same | MATCH |
| step-119 | `4c47783657870a762d620c54e8c70fcec15d13d81490641119695788df4b3f86` | same | MATCH |
| contract | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | same | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | same | MATCH |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | same | MATCH |
| staging | `0` | `0` | MATCH |

step-124 初始为 `ABSENT`；schemas/tests/step-119 只读。

## 3. Fresh unit receipts

Common environment/cwd：

```text
D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider
```

| command/node | result | wall | output SHA256 |
|---|---|---:|---|
| SS01 `test_raw_tables_strict_fields` | 1 passed | 0.595s | `d124f9696ed40502b4b30c0104e7d254a7e35a3d854991f72025ba67c7e5c805` |
| SS02 `test_pk_fk_bijection_fail_closed` | 1 passed | 0.506s | `a23e4e23ff133452cbbea2116bde11299e8cd6492bc70e3d90b69afbfa735e28` |
| SS11 `test_s4_schema_seven` | 1 passed | 0.483s | `a23e4e23ff133452cbbea2116bde11299e8cd6492bc70e3d90b69afbfa735e28` |
| full schema file | 3 passed | 0.633s | `5b581b8146eb94de21ac38ae754c4decbb7c1318ce5c8295dbbc36c62bd0ed63` |
| I02 regression | 6 passed | 0.847s | `32612694a0ec4989aac5b372e3e5cdeedd051e5b825283e86e07d34d6b96638a` |

Fresh executions=`12 passed`；unique tests=`9/9 GREEN`；skip/xfail/warning=`0/0/0`。
冻结 tests 内 47 个既有 mutation 均按预期拒绝，但未覆盖本报告三个边界族。

## 4. Independent one-shot mutation matrix

Windows Python `-B` inline matrix，不落 repo 文件：

```text
baseline_relational_bundle=PASS
new_expected_rejections=14
accepted_fail_open=14
rejected=0
exit=0
wall=0.363s
output_sha256=611ed122edca6198db1b80aa47e34139c9ede2bcbd2ad5d383b6b1e1d9bb47fe
```

14 项组成：7 个 empty/delete table cases、1 个 extra S2 ledger、1 个 raw cache-source
ghost、4 个 N/count identity、1 个 controlled-sentinel affected-count probe。最后一项因 owner
只明确“affected counts 不得被 sentinel 消费”，未明确 sentinel raw value 必须为零，故记录为
`NOT_COUNTED / reducer-boundary needs explicit owner`；其余 13 项形成上面 3 个 P1。

字段级 missing/extra/order/coercion/finite/SHA/decimal/hex、PK duplicate、forward FK、单行
group deletion、S4 7/7 identity/order/FK 已由 frozen tests + source audit闭合。S4 entry exact
model也排除 seed/cell/boundary extra fields。

## 5. Import / static audit

Fresh import probe：

```text
global_np_random_state_unchanged=True
filesystem_unchanged=True
sys_path_unchanged=True
dynamic_import=False
import_roots=[__future__, dataclasses, math, re, typing]
I/O_calls=[]
RNG_tokens=[]
selection_or_reduction_tokens=[]
output_sha256=d283b64d61c10663a0da51575f0e071ae11a86ce75662ebf741522f0861ec6ad
```

因此 schemas 保持 pure validator：无 I/O/RNG/selection/reduction/science/runner。缺陷位于
relational completeness 与 cross-field guards，不是职责越界。

## 6. Terminal

```text
VERDICT=FAIL
P0=0
P1=3
P2=0
FRESH_UNIQUE_TESTS=9/9 GREEN
FROZEN_MUTATIONS=47/47 REJECTED
NEW_MUTATIONS=0/14 REJECTED (14/14 FAIL-OPEN)
TERMINAL=I05_VERIFICATION_FAIL
NEXT_LEGAL_ACTION=test-first bounded repair of completeness, bidirectional ledger binding, and N/count identities
```

未运行 benchmark/science/web/install，未 commit/push，未修改 schemas/tests/step-119。
