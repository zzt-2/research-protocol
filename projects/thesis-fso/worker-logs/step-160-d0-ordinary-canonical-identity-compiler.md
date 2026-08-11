# Step 160 — D0 ordinary canonical identity compiler

> 2026-08-10 | T114 | `PASS`

## Strict RED

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_ordinary_identity.py
```

- collected `4`; `4 failed`; exit `1`
- 四项均因 public API `build_ordinary_identity_plan` 缺失而真实RED。
- stdout SHA256：`9a0ae76bc731d39edfd04be984aa4acbc430ea77aeca8bb191ff21bae6a82ccc`

## GREEN / regression / protection

### 实现边界

- additive新增typed frozen/slots identity field、consumer PK、work key、logical identity、ordinary binding及不可直接构造plan。
- public build/assert唯一authority参数为exact `D0OwnerIdentityAuthority`；入口重验证owner，assert每次fresh recompile exact compare，不信任plan seals。
- 只编译七类ordinary identity/binding；未增加`cache_status/source_computation_id`，未实现HMM/provenance/raw FULL，旧FULL API签名与实现保留。

### Exact GREEN

```text
collected 4 items
projects\simulation\tests\test_d0_ordinary_identity.py ....              [100%]
======================== 4 passed in 142.34s (0:02:22) ========================
GREEN_EXIT_CODE=0
GREEN_STDOUT_SHA256=b764c5157f97b5ac4cd07500e4fb03345bc87c7d968f10966c59d07274a072e9
```

- binding/logical counts：S2-off `540/60`、S2-on `1620/1620`、S3 `10800/10800`、BPS `7200/3600`、B2-clean `1200/600`、B2-controlled `21600/10800`、S4 `7/7`；总计`42967/27487`。
- S2-off九对一、BPS/B2 clean/B2 controlled双pol共享、S2-on三operation、S3双phase、S4七项：PASS。
- owner golden：S2 logical/root=`d0c1-c9ced...`/`ed1a721...`；BPS logical/root=`d0c1-354328...`/`51d43e...`，均exact。
- two fresh builds递归nonprimitive sharing=`0`；unsafe tamper left不影响right，tampered plan被assert拒绝。
- mutations=`24/24` fail closed；独立mutation节点`1 passed in 103.04s`，stdout SHA256=`3115744c5951462bf73e651dcdb78a2ed96c7ad883f529c171891d6a6de6e7c6`。

### 既有四文件回归

```text
collected 53 items
projects\simulation\tests\test_d0_contract_views.py ..............       [ 26%]
projects\simulation\tests\test_d0_waveform_channel.py .................  [ 58%]
projects\simulation\tests\test_d0_receiver_codec_methods.py .......      [ 71%]
projects\simulation\tests\test_d0_schemas_statistics.py ...............  [100%]
============================= 53 passed in 40.08s =============================
REGRESSION_EXIT_CODE=0
REGRESSION_STDOUT_SHA256=d03699011db0e2f9571372219bca21990d1fae5c4c07fe55e5f12e51af81dd68
```

全部0 fail/error/skip/xfail/warning；命令均设置`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用Python3.11 `-B`及`-p no:cacheprovider`。

### Hash / protection

| 文件/保护项 | SHA256 / 结果 |
|---|---|
| `schemas.py` | `e0770fb935b1a9fdfb822addf5cbecc94a148c1c6b28f312a7960298091906ec` |
| `test_d0_ordinary_identity.py` | `cda5bd2027a664136670b14f91715be3eea0d3826ce9f4f140823711a0dff485` |
| owner / contract / channel | `02d471a2...` / `50ae149a...` / `af32b357...` unchanged |
| old contract/waveform/codec/schema tests | `3da14d85...` / `f14cac81...` / `4045a688...` / `a94731c3...` unchanged |
| step159 | `9821f06edf897412cac04ed8db69389b5ce20e7e4985120295f9d04fb701d762` MATCH |
| P05 four logs | `7843b048...` / `735e4650...` / `c76887c6...` / `95a1d184...` unchanged |
| HEAD / staging / diff-check | `715a65884b988ee737f21982f3bbf372860a1da8` / empty / exit `0` |

只改授权三文件；未install/stage/commit/push，未运行benchmark/science/MVE。

## Terminal

`D0_ORDINARY_CANONICAL_IDENTITY_COMPILER_READY_FOR_INDEPENDENT_VERIFICATION / P0/P1/P2=0/0/0`

该PASS仅关闭ordinary identity compiler author边界，不等于I05/FULL完成；consumer provenance与HMM仍未实现。
