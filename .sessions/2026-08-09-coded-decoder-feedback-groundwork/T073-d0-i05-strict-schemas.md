# Task Brief: D0 I05 strict schemas and relational guards (TDD)

> 来源: step-116 PASS / d0-implementation-plan I05 / step-106 SS01–SS02、SS11 | 产出位置: `projects/thesis-fso/worker-logs/step-119-d0-i05-strict-schemas.md`
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

## Hypothesis / 否决条件

- 假设：owner 七类 typed artifact/table 契约可由纯 value schemas 与 fail-closed relational validation 精确表达，严格拒绝 extra/NaN/PK-FK/bijection/S4 cardinality 变异，且 schema layer 无 I/O、selection 或 scientific reduction。
- 否决条件：字段需凭实现者猜测而 owner/step-105/106 无依据；需要宽松 `**kwargs`、NaN、silent coercion 或 unknown field；PK/FK 不能闭合；S4 不可证明 exactly seven；需改 owner/contract/其他模块；或 15 分钟仍无有效 RED/GREEN receipt，则写 `INCOMPLETE` 停止。

## 冻结输入

```text
contract.py(I02)=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_contract(I02)=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/schemas.py`
2. Create `projects/simulation/tests/test_d0_schemas_statistics.py`
3. Create `projects/thesis-fso/worker-logs/step-119-d0-i05-strict-schemas.md`

不得修改 `contract.py`、owner、plan、其他 tests；不得创建 statistics/artifacts/runner/result/cache/`__init__.py`。

## TDD 任务

1. 完整读取 T073、plan I05、step-106 SS01/SS02/SS11、step-105 schemas interface、step-096/097 table/stat contract、step-102/103 typed artifact closure、owner table/artifact/S4 contract、I02 candidate 与 step-116。先核冻结 hash、branch/HEAD/staging、p05 4/4、三目标初态和 cache census。
2. **先创建测试，不写 production**；测试名必须恰为：
   - `test_raw_tables_strict_fields`（SS01）：owner 定义的各 raw/manifest row exact required fields/types；missing/extra/unknown/non-finite NaN/Inf、bool-as-int、silent numeric/string coercion 全拒绝；valid rows lossless roundtrip；frozen+slots/immutable values。
   - `test_pk_fk_bijection_fail_closed`（SS02）：所有 owner PK 唯一、FK 存在、规定的一对一/一对多 cardinality exact；duplicate/orphan/cross-cell/cross-seed/cross-method/missing reverse binding 均 fail closed；不同 strata 不得意外合并。
   - `test_s4_schema_seven`（SS11）：S4 owner exactly-seven typed artifacts/entries、稳定 identity/order/key bindings；6/8、duplicate kind、unknown kind、wrong FK/receipt/contract identity 全拒绝。
3. 测试只把 D0 root 加入 `sys.path`。运行三个 exact nodes，取得有效 RED（首次 module absent 可接受；syntax/fixture/path/collection/dependency error 不接受）。在创建 `schemas.py` **之前**把 exact command/cwd/env、exit code、test SHA、production ABSENT、原始 output SHA 和关键 failure 原文写入 step-119。
4. 最小实现 typed frozen/slotted rows/manifests 与 pure validators。字段、PK/FK 和 seven-artifact taxonomy 必须逐项 source-bind owner/step-105/106，不得为了让测试易过缩减规范；严格 finite/type validation，拒绝 bool 充当 int。schema layer 禁止 I/O、artifact serialization、selection、statistics/reduction、RNG、runner/science。
5. 不改 tests，以同一 exact nodes 取得 GREEN；再跑完整新文件和 `test_d0_contract_views.py` 回归。记录 source/test/owner SHA、output SHA、mutation counts/duration；无 skip/xfail/warning 隐藏。
6. 终检只三目标变化；staging=0、HEAD 不变、无 commit/push；无新 `.pyc`/`.pytest_cache`；p05 四日志 hash 逐一不变。

## 环境与命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact nodes or file> -q
```

禁止 WSL Python、安装依赖、benchmark/scientific seed、web/search/download。目标 10 分钟，15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；SS01/SS02/SS11 RED/GREEN counts；三文件 SHA；唯一写入/protection receipt；terminal 只能是 `I05_READY_FOR_INDEPENDENT_VERIFICATION` 或 named blocker。
