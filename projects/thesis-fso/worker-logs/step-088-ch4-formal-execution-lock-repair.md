# Step 088 Stage A：Ch4 formal execution lock 终态测试修复

> 2026-08-30 | T088 / D067 / V042 / CP029 | 仅完成 Stage A，等待独立审查

## 权限与范围

- 已完整读取 sim-preflight、T088、T087、D067、V042、step-087 worker log 与 T087 独立终态报告。
- fresh task-control validator=`PASS`，控制面为 epoch 29 / CP029 / `CH4_FORMAL_EXECUTION_LOCK_REPAIR`。
- 本阶段只修改 `tests/test_ch4_formal_production.py` 并写本日志；未修改 freezer、runner、reducer、entry、scientific manifest、core/common/scaled/params。
- 未删除、移动、覆盖或重签 invalid lock；未运行 ID29999 smoke 或 formal IDs `30000..30127`，未生成 formal raw/aggregate/receipt。

## Fresh RED

在 canonical invalid lock 保持存在时运行 focused suite，真实复现：

- `17 passed, 2 failed`；
- 失败项恰为 pure builder test 与 direct-CLI bootstrap test；
- 两项均只因永久断言 `ch4_formal_execution_lock.json` 不存在而失败。

RED 前 canonical lock 长度=`1674` bytes，SHA-256=`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`；无 `.tmp` 和 formal artifacts。

## 最小修复

1. pure builder test 在调用前快照 canonical lock 的存在性与原始 bytes；调用 `build_execution_lock()` 后要求存在性相同，若原先存在则 bytes exact 相同，并要求无 `.tmp`。
2. direct-CLI probe 的父进程同样快照并复核 canonical lock 存在性与 bytes。子进程只把该 canonical 路径的 `Path.exists()` 前置门受控隔离为 false，其他路径检查保持真实；随后必须真实导入 `projects.simulation.common`，并在 `save_results` 写入点前以 `WRITE_PREVENTED_AFTER_COMMON_IMPORT` 截断。
3. 未删除测试、断言，未使用 skip/xfail，也未放宽 common import 与 prevent-write 条件。

## Stage A 验证

| 检查 | 结果 |
|---|---|
| 两项目标测试 | `2 passed, 17 deselected` |
| invalid lock 存在态 focused suite | `19 passed in 2.94s` |
| 五文件隔离 `py_compile` | PASS |
| T088 task-control | PASS |
| canonical lock | 仍为 `1674` bytes / `3942883a...a45a492` |
| stale `.tmp` / formal artifacts | 均不存在 |
| 当前 tests SHA-256 | `cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1` |

不可变 SHA-256 现场复核：

- runner=`ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784`
- reducer=`f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327`
- entry=`da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0`
- scientific manifest=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`

## 约定变更

无。未改变参数、公式、信号模型、评估口径、执行网格或科学方法身份。

## 当前停点

Stage A 实现结果为 `READY_FOR_INDEPENDENT_STAGE_A_REVIEW`。invalid lock 必须继续原样存在；P0/P1 独立审查关闭前，不得进入 Stage B、删除 lock 或调用 freezer。

## Stage B：exact 作废与 replacement freeze

> 独立 Stage A review 已由主控确认 P0/P1=`0/0` 并明确开放 Stage B。

### 旧 lock 精确作废

删除前再次现场确认：

- canonical lock 存在且长度=`1674` bytes；
- SHA-256 exact=`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`；
- `.tmp` 不存在，formal raw/aggregate/receipt/checkpoint 数量为 0。

随后只用 `apply_patch` 删除这一个已登记 invalid artifact，未删除或移动任何其他文件。

### Lock 缺失态门禁

- fresh focused suite：`19 passed in 2.83s`；
- 五文件隔离 `py_compile`：PASS；
- T088 task-control：PASS；
- runner/reducer/entry、scientific manifest 与四项 frozen dependency SHA：全部 exact；
- tests SHA-256=`cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1`；
- 环境=`Python 3.11.9 / NumPy 2.4.3 / Windows-10-10.0.26200-SP0`；
- 无 `.tmp` 或 formal artifacts。

### 唯一 replacement freeze

只调用一次：

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/freeze_ch4_formal_execution_lock.py`

命令 exit=`0`，生成 replacement canonical lock：

- 长度=`1674` bytes；
- SHA-256=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`；
- tests binding=`cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1`。

调用没有重试，也没有运行 runner、smoke 或 formal production。

### Replacement lock 存在态门禁

- fresh focused suite：`19 passed in 2.96s`；
- 五文件隔离 `py_compile`：PASS；
- T088 task-control：PASS；
- lock 内 execution hashes 与 runner/reducer/entry/tests 现场 bytes 全部 exact；
- lock 内 environment、HEAD、scientific manifest、四项 frozen dependencies 与现场全部 exact；
- schema/authority/action/checkpoint/epoch/populations 保持 T087 冻结合同；
- `.tmp` 不存在，formal raw/aggregate/receipt/checkpoint 数量为 0。

## Stage B 当前停点

实现者侧 Stage B 为 `READY_FOR_INDEPENDENT_FINAL_LOCK_VERIFICATION`。replacement lock 生成后未再修改任何 bound code/tests。只有独立终态 reviewer 给出 P0/P1=`0/0` 后，主控才可接收 T088；本日志不授权 smoke、formal IDs 或 CP030。
