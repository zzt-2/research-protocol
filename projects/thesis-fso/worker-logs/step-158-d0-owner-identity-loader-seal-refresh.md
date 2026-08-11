# Step 158 — D0 owner identity loader seal refresh

> 2026-08-10 | T112 | `PASS`

## Strict RED（production仍为D016 seals）

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_authority_exact_frozen_view `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_grid_commitments_recompute_exact `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_d017_descriptors_and_hmm_reference_exact `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_loader_preserves_existing_contract_runtime
```

- collected `4`; `4 failed`; exit `1`
- 四项均在旧 production owner seal 处 fail closed：`owner bytes SHA256 does not match frozen D015 owner`
- stdout SHA256（UTF-8，含末尾换行）：`2262e840adf5604dcca503b7068a0b1abed2262c4dd1c0414b7c7e970916e4d1`

## GREEN / regression / protection

### Exact GREEN

```text
collected 4 items
projects\simulation\tests\test_d0_contract_views.py ....                 [100%]
============================== 4 passed in 1.73s ==============================
GREEN_EXIT_CODE=0
GREEN_STDOUT_SHA256=796432ed2bd8a09bb06aeffed8df472dc017285a3f2de140378d6377bf56d649
```

D017 exact node独立断言：七类ordinary加一类HMM、work/ordinary-PK/含HMM-PK descriptors=`32/41/49`、8 signatures、S4七项顺序、HMM无LOGICAL binding且manifest reference exact，全部PASS。

### Mutation gate

现有16项加D017 fresh 12项，总计`28/28` fail closed。D017覆盖ordinary kind/phase/operation/source/atom/order、method map、split map、B2 same-type swap、S4、HMM reference kind/rule。

```text
collected 1 item
projects\simulation\tests\test_d0_contract_views.py .                    [100%]
============================== 1 passed in 6.11s ==============================
MUTATION_EXIT_CODE=0
MUTATION_STDOUT_SHA256=2e2ed4b67eff543b4c4c958afa6c390015e484489d422984458db9823c80aa0d
```

### 显式四文件回归

```text
collected 53 items
projects\simulation\tests\test_d0_contract_views.py ..............       [ 26%]
projects\simulation\tests\test_d0_waveform_channel.py .................  [ 58%]
projects\simulation\tests\test_d0_receiver_codec_methods.py .......      [ 71%]
projects\simulation\tests\test_d0_schemas_statistics.py ...............  [100%]
============================= 53 passed in 38.52s =============================
REGRESSION_EXIT_CODE=0
REGRESSION_STDOUT_SHA256=16435b9edeb25fd6dd77ead58d2a9781aca5c2c2f443ae0e6c66b413b7133b56
```

结果为0 fail/error/skip/xfail/warning。所有pytest设置`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用Python3.11 `-B`和`-p no:cacheprovider`。

### Production diff proof

- `contract.py`中两个新seal各exact出现1次；把这两个值在内存替回old owner/identity seal后，SHA256精确恢复pre-contract `0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94`。故production diff仅两处常量值。
- AST确认`D0Contract`仍exact四字段：`schema_version/control/population/seed_registry`。
- channel SHA仍`af32b357...`，其contract入口仍注解/消费`D0Contract`；loader public signatures与import-time I/O结构未改。

### Hashes / protection

| 项目 | SHA256 / 结果 |
|---|---|
| `contract.py` | `50ae149a77588c34cedd2a2e8aab5078b6b4e3d4ea310ba85fe577f76f5ca170` |
| `test_d0_contract_views.py` | `3da14d85a9a743726f985897ac65cd70f331069dcecdfefbd6d09296cba272be` |
| final owner | `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140` MATCH |
| schemas / channel | `a42ffa18...` / `af32b357...` MATCH |
| decisions / verifications / R001 / topic-index / master-state | `b20e8ffc...` / `beaa8046...` / `1882c9d5...` / `bb95bb1c...` / `92e800b4...` MATCH |
| step157 | `bfab0aac3434a9aae22adb7b5e0d5e3963b2b5c534d3fb18ef85db7311057b78` MATCH |
| P05 four logs | `7843b048...` / `735e4650...` / `c76887c6...` / `95a1d184...` MATCH |
| HEAD / staging / diff-check | `715a65884b988ee737f21982f3bbf372860a1da8` / empty / exit `0` |

未修改owner/schemas/channel/session/P05/tracked pycache；未install/stage/commit/push，未运行benchmark/science/MVE。

## Terminal

`D017_OWNER_IDENTITY_LOADER_SEAL_REFRESH_READY_FOR_INDEPENDENT_VERIFICATION / P0/P1/P2=0/0/0`

该PASS仅关闭T112 author seal refresh，不等于I05完成。
