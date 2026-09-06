# T087 Ch4 formal execution seam 独立终态复核

> 日期：2026-08-30  
> 范围：T087 tracked execution lock 生成后的只读现场复核  
> 审查约束：未修改 code/tests/lock，未运行 formal IDs `30000..30127`，未生成任何论文数字

## 终态结论

**`CH4_FORMAL_EXECUTION_SEAM_INVALID`**。

问题分级为 **P0/P1/P2 = `0/1/3`**。execution lock 本身的字节、schema、authority、绑定哈希、环境和 population 均与现场一致；但 tracked lock 存在后，fresh focused suite 只能通过 `17/19`。两个 freezer 测试硬编码要求 tracked lock 不存在，导致冻结后的最终仓库态不能通过它自己绑定的测试文件。该终态自洽性缺口为 P1，阻断 `CH4_FORMAL_EXECUTION_SEAM_READY`。

因此，当前 SHA 为 `3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492` 的 execution lock **不得用于 formal 执行**；不得自动重签，formal IDs 继续禁止。

## 现场绑定复核

tracked lock：

- 路径：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_execution_lock.json`
- 文件长度：`1674` bytes
- SHA-256：`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`
- schema：`t087.ch4-formal-execution-lock.v1`
- authority/action：`T087/D066/V041` / `CH4_FORMAL_EXECUTION_SEAM`
- checkpoint/epoch：`CP028` / `28`
- base commit 与现场 HEAD：均为 `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`
- scientific manifest：锁内与现场均为 `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`
- 环境：Python `3.11.9`、NumPy `2.4.3`、`Windows-10-10.0.26200-SP0`，锁内与现场一致
- population：smoke 仅 `[29999]`；formal 精确为 `30000..30127`（含端点，共 128 个 ID）
- `_meta.git_commit=d3d98c6` 是现场 HEAD 的有效短前缀

execution hashes 均与实际文件一致：

| 绑定项 | 现场 SHA-256 |
|---|---|
| runner | `ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784` |
| reducer core | `f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327` |
| reducer entry | `da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0` |
| focused tests | `f7085ace191041628f2dac84269f06d2e1ce6add50cff326813502697fe42848` |

frozen dependency hashes 也全部一致：

| 绑定项 | 现场 SHA-256 |
|---|---|
| `production_core.py` | `c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60` |
| `common/_modulation.py` | `bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10` |
| `scaled_unitary.py` | `868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2` |
| `projects/simulation/params.py` | `0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9` |

## Fresh verification

| 检查 | 结果 |
|---|---|
| focused pytest（禁 cache/pyc） | **FAIL：17 passed, 2 failed** |
| 5 个 seam 文件隔离 `py_compile` | PASS |
| T087 task-control validator | PASS |
| targeted `git diff --check` | PASS |
| `ch4_formal_execution_lock.json.tmp` | 不存在 |
| `ch4_formal_checkpoint.json` | 不存在 |
| `ch4_formal_raw.json` | 不存在 |
| `ch4_formal_aggregate.json` | 不存在 |
| `ch4_formal_receipt.json` | 不存在 |

两个失败用例为：

1. `test_execution_lock_builder_binds_dual_lock_inputs_without_writing`
2. `test_freezer_direct_cli_bootstraps_common_import_without_writing`

两者均在测试开始处断言 `ch4_formal_execution_lock.json` 不存在。这在 pre-freeze 阶段成立，在 lock 已作为最终产物生成后必然失败。它们没有证明 lock 内容错误，却证明当前冻结终态无法用其绑定测试进行 fresh 全绿复验。

## 已完成但不改变终态的证据

在 lock freeze 之前，独立审查已经完成唯一一次 ID29999 OS-temp structural smoke：实际 census 为 1 个 top record、3 个 scene record、119 个 actual cell、595 行、1 个 delta-zero reference；三场景 cell 数为 `19/81/19`，五个 public roles、tau、truth-only O1、PCG64 namespace、同场景跨 Np payload pairing、delta-zero identity 与 raw-only reducer 均通过，reducer 终止于 `FORMAL_SMOKE_STRUCTURAL_PASS`，未定 grade、未报告科学数字。该 smoke 没有重跑。

这些证据说明 runner/reducer 的既有结构性 smoke 成立，但不能覆盖本次新发现的 post-lock test inconsistency，因而不能把终态提升为 READY。

## 分级明细

### P1（1）

- **冻结后的测试闭环不自洽**：tracked lock 是 T087 必需最终产物，但两个被 lock 自身哈希绑定的 focused tests 要求该产物不存在。final reviewer 无法在不删除/移动 lock 或修改测试的情况下取得 fresh `19/19`，违反终态复验要求。

### P2（保留 3 项）

- checkpoint 采用 self-digest，而非确定性重建。
- future aggregate/receipt 使用 sequential replace，崩溃恢复仍有窗口。
- 缺少直接的数值 bootstrap regression test。

这三项不替代 P1，也不成为运行 formal 的理由。

## 解除阻断条件

只允许在新的、明确授权的 seam 修复任务中处理 post-lock 测试语义，使测试在 tracked lock 存在时仍验证“builder/CLI 的被测调用不产生或改写 lock”，而不是要求仓库中永久没有 lock。修复会改变 tests SHA，因此当前 lock 随即失效；必须重新走 fresh tests、独立 hash review，并在明确授权下生成新的唯一 lock。完成这些步骤前，formal 执行持续禁止。
