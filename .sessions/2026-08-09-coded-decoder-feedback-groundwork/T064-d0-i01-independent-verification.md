# Task Brief: D0 I01 fresh independent verification

> 来源: T063 / step-109 / I01 candidate | 产出位置: `projects/thesis-fso/worker-logs/step-110-d0-i01-independent-verification.md`
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

## Hypothesis / 否决条件

- 假设：I01 candidate 在未改 owner/test 的情况下真实闭合 CV01–CV03，接口是 leaf/no-import-I/O/fail-closed，且没有提前实现后续 scientific/runtime 行为。
- 否决条件：fresh tests 非 3/3；test tautology/漏 exact owner identity；duplicate/overlap/unknown/wrong membership 可通过；action 默认开放；numeric parsing 接受非有限/非正；import 改 repo；代码含 receiver/science/benchmark runner；RED receipt 顺序不可证；或保护项变化，均 FAIL。

## 冻结输入

```text
contract.py=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
test_d0_contract_views.py=3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
step-109=c85d1a2e2fd52750519a3cf8bf48c869fa4e9f5614ea53f546aa46ca0c0d430b
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 任务

1. 完整读取 T064、I01 plan、step-106 CV01–03、owner control/population/seed、contract/test/step-109；核 frozen hashes、branch/HEAD/staging、p05、cache census。
2. 静态审查：exact three test names/claims；测试不是从 implementation 派生 expected；strict duplicate loader；frozen/value semantics；12-cell unique product；八 ranges inclusive/disjoint + natural first-stage proper subset；unknown/wrong/out-of-range fail closed；CP012 action deny-by-default；`load_contract` 是唯一 I/O；无 sys.path mutation/import-time construction/runner/science/benchmark。
3. fresh run 完整 `test_d0_contract_views.py`，必须 `3 passed / 0 skip/xfail/warning`：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

4. 在 OS temp 目录做不写 repo 的 mutation probes：duplicate nested key拒绝；overlap registry 构造拒绝；unknown action拒绝；`nan/inf/0/negative` symbol-rate 拒绝；owner原样 `2.5e9` 可加载且恰为 `2500000000.0`。记录 exact command/output SHA。
5. 重建 step-109 chronology：test SHA 与 RED receipt 一致、production 当时 ABSENT 的日志证据内部一致、GREEN test SHA 未变；若只能证文档一致须明确 evidence level，不把 self-report 升格。
6. 终检 frozen input SHA、仅本日志新增、p05 4/4、staging=0、cache census不增；不修改任何 candidate/owner/test/governance（除本任务文件已由主控创建）。

## 边界与返回

- 只写 `projects/thesis-fso/worker-logs/step-110-d0-i01-independent-verification.md`。
- 禁止修 code/test、benchmark/science、web/search/download、commit/push、p05/pycache触碰。
- 目标 8 分钟，15 分钟硬上限。
- 返回 `PASS/FAIL/INCOMPLETE, P0/P1/P2`；只有 `0/0/0` 可写 `I01_VERIFIED_READY_FOR_I02`。
