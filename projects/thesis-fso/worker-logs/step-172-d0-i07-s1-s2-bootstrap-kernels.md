# Step 172 — D0 I07 slice A S1/S2/bootstrap kernels

> 2026-08-11 | T126 | PASS

## Scope

本切片只新建 `statistics.py`、修改 `test_d0_schemas_statistics.py` 并写本记录。未读取 owner/YAML，未执行 I/O、scientific seed/artifact、整份 statistics FULL、benchmark、science、MVE、install、stage、commit 或 push。

## RED

先新增按绝对文件位置加载模块的 SS03 与 480-row typed fixture；production 文件尚不存在时真实运行指定 node：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_schemas_statistics.py::test_s1_coverage_event

结果为预期 bootstrap RED：

    1 failed in 0.41s
    FileNotFoundError: ...\coded-decoder-feedback\statistics.py
    RED_EXIT_CODE=1

失败来自目标模块尚不存在，不是测试语法、fixture 或 import 污染。

## Minimal GREEN

- `reduce_s1`：只接受 exact typed `480/1200` rows，验证 `20/50 seeds × 12 cells × 2 pol` 笛卡尔覆盖、PK 唯一、event/count/array 一致；hand point=`2/480=1/240`。
- `reduce_s2`：验证 `10 seeds × hard/mid/clean × 2 pol × 9 fixtures × (B1/B2/O1 on + B1 off)`；每组九个 off projection 共享 physical/computation/content owner；先按 cell 汇总 integer numerator/denominator，再三 cell 等权 macro。
- `bootstrap_paired`：每次调用独立 `Generator(PCG64(seed))`，seed-block paired resample；`method='linear'` valid-only percentile；500/501 invalid 边界 fail closed；不触碰 global RNG、不裁剪 ratio。
- 所有 result 为 frozen/slotted dataclass；模块仅依赖 NumPy 与 I05 typed rows/constants/`SchemaError`，无 I/O/owner/YAML。

## GREEN / goldens / negatives

环境固定 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11、`-B`、`-p no:cacheprovider`。

SS03–SS07 核心：

    4 passed in 0.89s

显式 SS01/SS02/SS11 + SS03–SS07（未运行 219s FULL node）：

    7 passed in 0.79s
    GREEN_EXIT_CODE=0
    GREEN_STDOUT_SHA256=957d8195687b04b9545144c7ada9d82e58d74cf078f288e25f8935dd394d7855

Exact goldens：

- S1 event rate=`1/240`。
- S2 hard/mid/clean `(B1on,off,O1,B2)` points=`(9,3,3,5)/12`、`(4,0,2,3)/8`、`(1,0,0,0)/4`。
- cell-equal macro：damage=`5/12`、recoverability=`13/18`、coverage=`13/18`；明确不等于 global-pool sentinels `11/24`、`9/14`、`2/3`。
- PCG64 前两 draw indices exact；500 invalid=`9500 valid + CI 1.2/1.2`，501 invalid=`UNSTABLE_DAMAGE_DENOMINATOR` 且无 CI。

Fresh structural negatives=11/11 fail closed：S1 少行、duplicate、seed/cell/pol 缺失或重复、event mismatch、array mismatch；S2 off computation/content owner 拆分、wrong on/off method。global RNG state unchanged；wrong accept/reject=`0/0`。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| statistics.py | `f12c2d61e90e158fa4046abbd0bd753f0815916370a7bfe5c2184067a09419e2` |
| test_d0_schemas_statistics.py | `4632622906a8980a1d24645c507ca27453349598ef09b1849847b9a1cc6a15e5` |
| T126 | `f8a069a1364cbbc0a609ab92070009ffa699c5f718ee37edfa4b2de7f77b61d5` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 SHA 4/4 保持：`7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`、`735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`、`c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`、`95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`。
- 未创建 bytecode/pytest cache；既有 tracked pycache dirty 未扩展。

## Terminal

`D0_I07_S1_S2_BOOTSTRAP_GREEN`

P0/P1/P2=`0/0/0`

该 PASS 只关闭 I07 slice A；SS08–SS10 留给同一 production/test 文件的串行 slice B。D0 science 仍为 `NOT_RUN`，不形成方法信号或科学结论。
