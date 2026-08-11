# Step 154 — D0 owner identity typed loader

> 2026-08-10 | T108 | `PASS`

## Strict RED receipt（生产源码未改）

命令：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_authority_exact_frozen_view `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_grid_commitments_recompute_exact `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_mutations_fail_closed `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_loader_preserves_existing_contract_runtime
```

- 收集：`4`
- 结果：`4 failed`
- exit code：`1`
- stdout SHA256（UTF-8，含末尾换行）：`56a07c407b8bfc406bf1cc0aab161ec75848acef22464b9d264ca842697372c6`
- 四项均因 public API `load_owner_identity_authority` 缺失而失败（`AttributeError`），符合 strict RED。

完整 stdout：

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
plugins: anyio-4.12.1
collected 4 items

projects\simulation\tests\test_d0_contract_views.py FFFF                 [100%]

================================== FAILURES ===================================
_______________ test_owner_identity_authority_exact_frozen_view _______________
E       AttributeError: module 'contract' has no attribute 'load_owner_identity_authority'
____________ test_owner_identity_grid_commitments_recompute_exact _____________
E       AttributeError: module 'contract' has no attribute 'load_owner_identity_authority'
__________________ test_owner_identity_mutations_fail_closed __________________
E       AttributeError: module 'contract' has no attribute 'load_owner_identity_authority'
_______ test_owner_identity_loader_preserves_existing_contract_runtime ________
E       AttributeError: module 'contract' has no attribute 'load_owner_identity_authority'
=========================== short test summary info ===========================
FAILED projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_authority_exact_frozen_view
FAILED projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_grid_commitments_recompute_exact
FAILED projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_mutations_fail_closed
FAILED projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_loader_preserves_existing_contract_runtime
============================== 4 failed in 1.55s ==============================
```

## GREEN / 保护核验

### 最小实现

- 保持 `D0Contract` 四字段及 `load_contract` 行为不变，additive 新增 `Float64Literal`、`IdentityBindingContract`、`D0OwnerIdentityAuthority`、`load_owner_identity_authority` 与显式重验证入口。
- loader 在显式调用时 strict duplicate-key parse；前后读取 owner bytes 并比较；复用 `load_contract` 和 `assert_frozen_d0_identity`。
- exact 13-key owner 子树转为 detached recursive immutable view；仅两处合法整数键 anchors 规范化为 `tuple[Float64Literal, ...]`，未放宽 `_deep_freeze` 的通用 mapping-key 边界。
- 复算 final owner bytes SHA、移除 identity block 后的 scientific projection SHA、identity canonical diagnostic seal、三个 grid roots及六项 ledger 静态 count。golden payload 仅闭世界保存，未复制 schema compiler 或补造 work-key/phase/operation。
- public revalidation 从 view 反向重建 canonical identity 并复算 seal，拒绝 dataclass replacement/伪造 hash。

### Exact GREEN

同 RED 的四个 exact nodes：

```text
collected 4 items
projects\simulation\tests\test_d0_contract_views.py ....                 [100%]
============================== 4 passed in 5.59s ==============================
GREEN_EXIT_CODE=0
GREEN_STDOUT_SHA256=677e891f4d61825bf59d00447b56e23a0a0925a898c74eb9018dbe0db78be592
```

- exact authority/frozen/detachment/forgery：PASS
- 122 + 6 literals及 3 roots独立复算：PASS
- fresh owner mutations：`16/16` fail closed（覆盖 omitted/extra、3 headers、section type、duplicate key、literal index/hex/order/root、combined deep equality、golden root、binding kind、ledger count、cache source）
- runtime preservation：PASS

### 回归

```text
collected 30 items
projects\simulation\tests\test_d0_contract_views.py .............        [ 43%]
projects\simulation\tests\test_d0_waveform_channel.py .................  [100%]
============================= 30 passed in 25.05s =============================
REGRESSION_EXIT_CODE=0
REGRESSION_STDOUT_SHA256=ba2c29cd01c276554b8e4c75429f34c9fb7acce9934099bf1ae25502359ccd87
```

所有 pytest 命令均设置 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用 Python 3.11 `-B` 与 `-p no:cacheprovider`；未运行 benchmark/science。

### Final hashes / protection

| 文件 | SHA256 / 结果 |
|---|---|
| `contract.py` | `0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94` |
| `test_d0_contract_views.py` | `745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6` |
| final owner | `ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535` MATCH |
| `schemas.py` | `a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401` MATCH |
| R001 / decisions / verifications / step153 | `ff229de3...` / `ca4b7098...` / `848ea9e3...` / `39ded7d1...` MATCH |
| P05 four logs | `7843b048...` / `735e4650...` / `c76887c6...` / `95a1d184...` MATCH |
| `git diff --check` | exit `0` |

未修改 owner、schemas、session 治理、P05 日志或 tracked pycache；未 install/stage/commit/push。

## Terminal

`OWNER_IDENTITY_TYPED_LOADER_READY_FOR_INDEPENDENT_VERIFICATION / P0/P1/P2=0/0/0`

该 PASS 仅关闭 T108 author 边界；I05 binding 仍 open，不开放 benchmark/science。
