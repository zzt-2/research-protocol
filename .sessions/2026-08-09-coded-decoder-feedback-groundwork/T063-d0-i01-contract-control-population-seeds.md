# Task Brief: D0 I01 contract control, population and seed registry (TDD)

> 来源: step-108 PASS / d0-implementation-plan I01 / step-106 CV01–CV03 | 产出位置: `projects/thesis-fso/worker-logs/step-109-d0-i01-contract-control-population-seeds.md`
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

- 假设：owner 的 CP012 control、12-cell population 和八个 inclusive/disjoint seed ranges 可由一个无 import-I/O 的 leaf `contract.py` 精确表示，并用 CV01–CV03 在 Windows Sionna 环境下先 RED 后 GREEN。
- 否决条件：需要改 owner/common/legacy；必须运行 scientific seed/benchmark；测试只能靠 skip/tolerance；seed ranges 有重叠/遗漏；population 不是精确 4×3；或单任务到 15 分钟仍未形成有效 RED/GREEN receipt，则停止并写 `INCOMPLETE`，不得扩大范围。

## 冻结输入

```text
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-108=fdca38d0f52822c10d5debcedc11880ea04e0fe5f2da1e2156de1c32f0507955
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
v3 owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. `projects/simulation/explore/coded-decoder-feedback/contract.py`
2. `projects/simulation/tests/test_d0_contract_views.py`
3. `projects/thesis-fso/worker-logs/step-109-d0-i01-contract-control-population-seeds.md`

不得创建 `__init__.py`、runner、artifact/result/cache；不得修改其他文件。

## TDD 任务

1. 完整读取本任务、plan I01、step-106 CV01–CV03、step-105 的 `contract.py` interface、owner control/population/seed_plan/H004 action classes。先核冻结 hash、branch/HEAD/staging、p05 4/4、三目标初态、pycache/pytest-cache census。
2. **先写测试，不写 production**，测试名必须恰为：
   - `test_contract_control_is_cp012_implementation_only`（CV01）：schema v3；epoch12/CP012/D011/V005；implementation/unit/engineering benchmark true，execution/science false；显式 action-class gate 不得凭 owner 当前单一 `action_class` 推断 science 权限。
   - `test_population_manifest_has_exact_twelve_cells`（CV02）：cross product `snr_db=[10,14,18,22]` × `linewidth_hz=[10000,20000,80000]` 恰 12 唯一 cells；1024/1536/16/384/6144/20、2.5e9、Gray square 16QAM exact。
   - `test_seed_registry_exact_and_pairwise_disjoint`（CV03）：八个主范围 exact/inclusive/disjoint：8000–8009、8050–8059、8100–8149（且 first_stage=8100–8119 是其 subset）、8150–8159、8160–8169、8170–8179、8200–8219、8300–8349；错归属、越界和未知 label 拒绝。
3. 测试仅把 D0 root 加入 `sys.path`；production 不改 global path。运行三个 exact node/file，取得有效 RED（新模块首次 `ModuleNotFoundError` 可接受；syntax/fixture/path/collection/dependency error 不接受）。在写 `contract.py` **之前**把 exact command/cwd/env、exit code、test SHA、production ABSENT、原始输出 SHA 与关键 failure 原文写入 step-109。
4. 最小实现：strict duplicate-key YAML loader；frozen dataclass/value types；`load_contract(path) -> D0Contract`；deterministic 12-cell manifest；inclusive seed registry with membership/label validation and pairwise-disjoint assertion；CP012 control/action gate。不得提前实现 CV04–CV09 的 ReceiverView/TruthView/recursive denylist/freeze 类型。
5. 不改 tests，以同一 exact command取得 GREEN；再跑整个 `test_d0_contract_views.py`。记录 source/test/owner SHA、exact outputs SHA、counts/duration；无 skip/xfail/warning 隐藏。
6. 终检只允许三目标变化；无 import-I/O；无 science runner/seed/estimand；无新 `.pyc`/`.pytest_cache`；p05 4/4 exact、staging=0、未 commit/push。

## 环境与命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact-node-or-file> -q
```

禁止 WSL Python、自动安装、隐式 skip、实际 D0/benchmark/science、web/search/download。目标 10 分钟，15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；CV01–CV03 RED/GREEN counts；三文件 SHA；唯一写入/protection receipt；terminal 只能是 `I01_READY_FOR_INDEPENDENT_VERIFICATION` 或 named blocker。
