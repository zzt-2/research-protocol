# T088 Ch4 formal execution lock repair 独立终态复核

> 日期：2026-08-30  
> 范围：T088 final-state test repair、invalid lock replacement 与最终绑定  
> 审查纪律：未修改或移动 code/tests/lock，未调用 freezer/runner，未运行 smoke 或 formal IDs

## 终态

**`CH4_FORMAL_EXECUTION_LOCK_REPAIR_READY`**。

问题分级：**P0/P1/P2 = `0/0/3`**。T087 留下的 post-lock test inconsistency 已消除；replacement lock 在最终存在态可用它绑定的 focused tests fresh 复验为 `19/19 PASS`。三个既有 P2 保留，不影响本次 lock-repair 终态。

本结论只关闭 T088。formal IDs `30000..30127` 仍不得运行，必须等待主控另行建立下一 checkpoint；本报告本身不构成 formal production 授权。

## 控制与血缘

- T088 task-control fresh validator：PASS。
- 当前任务控制：`CP029 / epoch 29 / CH4_FORMAL_EXECUTION_LOCK_REPAIR`。
- 作废的首个 lock：`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`。
- replacement lock：`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`，长度 `1674` bytes。
- replacement payload 继续绑定 T087 冻结的 formal seam 合同：`T087/D066/V041 / CP028 / epoch 28`。这与 T088 的修复任务控制分属两层，不是错配。

## 两态测试闭环

### RED 与 invalid-lock 存在态 GREEN

独立 reviewer 在 T087 终态已用旧 tests SHA `f7085ace191041628f2dac84269f06d2e1ce6add50cff326813502697fe42848` 现场复现 `17 passed, 2 failed`；当时 invalid lock SHA exact 为 `3942883a...a45a492`。失败仅来自两个测试永久断言 canonical lock 不存在。

修复后 tests SHA 为 `cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1`。在 invalid lock 仍存在时，独立 reviewer fresh focused suite 为 `19/19 PASS`，且 invalid lock SHA、runner/reducer/entry/manifest 均保持 exact。

### 缺锁态与 replacement-lock 存在态

- worker log 记录在删除前再次核对 invalid lock 的 exact SHA 和 `1674` bytes，仅删除该已登记 invalid artifact；缺锁态 focused suite=`19/19 PASS`，随后 freezer 只调用一次并 exit `0`。
- 独立 reviewer 审查了两个修复测试的实际控制流：pure builder test 对调用前后的 canonical 存在性和 bytes 做快照等同检查；direct-CLI test 只隔离 canonical `Path.exists()` 前置门，必须到达 `projects.simulation.common` import，并在 `save_results` 写入调用处以 sentinel 截断；父进程再次检查 canonical 状态/bytes 与 `.tmp`。
- 无测试删除，无 skip/xfail。独立 reviewer 在不删除 replacement lock 的条件下复放两个测试的受控缺锁分支，结果 `2/2 PASS`，replacement lock 前后 SHA exact 不变且无 `.tmp`。
- replacement lock 最终存在态的独立 fresh focused suite：`19 passed in 2.92s`。

因此，两个被修测试均覆盖 canonical lock 缺失与存在分支，不再通过永久要求 lock 缺失制造 pre-freeze-only 绿灯。

## Replacement lock 现场绑定

基础合同全部匹配：

- schema：`t087.ch4-formal-execution-lock.v1`
- authority/action：`T087/D066/V041` / `CH4_FORMAL_EXECUTION_SEAM`
- checkpoint/epoch：`CP028 / 28`
- base commit 与现场 HEAD：`d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`
- scientific manifest：`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`
- environment：Python `3.11.9`、NumPy `2.4.3`、`Windows-10-10.0.26200-SP0`
- populations：smoke=`[29999]`；formal=`30000..30127`

execution hashes 与实际 bytes 全部一致：

| 绑定项 | SHA-256 |
|---|---|
| runner | `ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784` |
| reducer core | `f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327` |
| reducer entry | `da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0` |
| focused tests | `cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1` |

frozen dependencies 与实际 bytes 全部一致：

| 绑定项 | SHA-256 |
|---|---|
| `production_core.py` | `c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60` |
| `common/_modulation.py` | `bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10` |
| `scaled_unitary.py` | `868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2` |
| `projects/simulation/params.py` | `0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9` |

## Fresh 检查汇总

| 检查 | 结果 |
|---|---|
| replacement lock 存在态 focused pytest | PASS，`19/19` |
| 两个修复测试的受控缺锁分支复放 | PASS，`2/2` |
| 5 个 seam 文件隔离 `py_compile` | PASS |
| T088 task-control validator | PASS |
| targeted `git diff --check` | PASS |
| skip/xfail 扫描 | `0` 命中 |
| `ch4_formal_execution_lock.json.tmp` | 不存在 |
| `ch4_formal_checkpoint.json` | 不存在 |
| `ch4_formal_raw.json` | 不存在 |
| `ch4_formal_aggregate.json` | 不存在 |
| `ch4_formal_receipt.json` | 不存在 |

## P2（保留 3 项）

1. checkpoint 采用 self-digest，而非确定性重建。
2. future aggregate/receipt 使用 sequential replace，崩溃恢复仍有窗口。
3. 缺少直接的数值 bootstrap regression test。

T088 没有修改上述机制；它们继续限制未来执行与恢复保证，但不构成本次 final-state lock repair 的 P0/P1。

## 最终判定

T088 的唯一缺口已经关闭：同一 tests payload 在 canonical lock 缺失和存在两种状态下均验证“不产生或改写 canonical lock、无 stale `.tmp`”，replacement lock 又绑定当前 tests 与全部 frozen execution bytes。故终态为 `CH4_FORMAL_EXECUTION_LOCK_REPAIR_READY`；在主控正式推进 checkpoint 前，formal production 仍保持关闭。
