# Step 162 — D0 ordinary domain authority repair

> 2026-08-10 | T116 | `PASS`

## Strict RED

四个exact节点在production未改时真实RED：typed domain view缺失、module-global替换改变/阻断plan、raw enumeration存在parallel authority、domain/seal tamper边界缺失。

```text
collected 4 items
projects\simulation\tests\test_d0_contract_views.py F                    [ 25%]
projects\simulation\tests\test_d0_ordinary_identity.py FFF               [100%]
============================== 4 failed in 9.08s ==============================
RED_EXIT_CODE=1
RED_STDOUT_SHA256=9cccb7fde5e4a33bfdee313ee88c966e14173d24992c0cf316aadef6838dc09b
```

## GREEN / regression / protection

### Repair

- loader在同一次显式full-owner认证读取中提取frozen/slots `OrdinaryDomainAuthority`，只暴露aliases、pol/fixture/candidate/S2-method/S4顺序、tuple/B/Nw与六类table record-type domains。
- projection schema固定为`coded_decoder_feedback.d0.ordinary_domain_authority.v1`；test侧独立canonical encoder与production均命中seal `15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69`。
- `D0OwnerIdentityAuthority`新增typed domain与seal；public assertion从dataclass重建projection并复算seal，不信任可替换seal。
- `_ordinary_raw_records`只消费authenticated domain、identity view及contract seed/population；不再引用`CANDIDATES/S2_METHODS/TUPLES/S4_CHECK_IDS`或local aliases/B/Nw/record-type literals。
- owner YAML bytes与原owner/scientific/identity三seal不变；未改旧FULL API，未实现provenance/HMM/raw FULL。

### Exact GREEN

```text
collected 4 items
projects\simulation\tests\test_d0_contract_views.py .                    [ 25%]
projects\simulation\tests\test_d0_ordinary_identity.py ...               [100%]
============================= 4 passed in 13.57s ==============================
GREEN_EXIT_CODE=0
GREEN_STDOUT_SHA256=b5dfbb16a4ae17ef8d53651624917c33a8fae61dc821caaa35b94e59ed38b0b1
```

### 两文件全量

```text
collected 22 items
projects\simulation\tests\test_d0_contract_views.py ...............      [ 68%]
projects\simulation\tests\test_d0_ordinary_identity.py .......           [100%]
======================= 22 passed in 161.26s (0:02:41) ========================
GREEN_FULL_EXIT_CODE=0
GREEN_FULL_STDOUT_SHA256=8d3d9d7bed49111f8794b33c30f133b5448aafef2a67794a1e10994cb1e1c244
```

- ordinary counts/goldens/grouping仍exact `42967/27487`。
- mutations=`32/32` fail closed（既有24 + domain replace/seal 8）。
- module globals四类等基数/非法替换前后plan逐对象相同；public assert不依赖globals。
- fresh sharing=`0`；wrong accept/reject=`0/0`。

### 显式旧四文件回归

```text
collected 54 items
projects\simulation\tests\test_d0_contract_views.py ...............      [ 27%]
projects\simulation\tests\test_d0_waveform_channel.py .................  [ 59%]
projects\simulation\tests\test_d0_receiver_codec_methods.py .......      [ 72%]
projects\simulation\tests\test_d0_schemas_statistics.py ...............  [100%]
============================= 54 passed in 40.85s =============================
REGRESSION_EXIT_CODE=0
REGRESSION_STDOUT_SHA256=e8ceca89ebd0329c1d63aa18d7abcaa98283cb9470f07c1ad2670ca22d8732e8
```

54项=原53项加本任务新增domain-view test；0 fail/error/skip/xfail/warning。所有pytest设置`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用Python3.11 `-B`与`-p no:cacheprovider`。

### Hash / protection

| 文件/保护项 | SHA256 / 结果 |
|---|---|
| `contract.py` | `cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a` |
| `schemas.py` | `1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20` |
| `test_d0_contract_views.py` | `ea37c7707db3f8a22ba0a6a9b97a6a88a7b458e474b906b001a0751f3b7ee4e5` |
| `test_d0_ordinary_identity.py` | `fdf9d8c1454d748d8b6eb681abc5f2ef2b783cf361f3610ce81c490542a7c19e` |
| owner / channel | `02d471a2...` / `af32b357...` unchanged |
| old waveform/codec/schema tests | `f14cac81...` / `4045a688...` / `a94731c3...` unchanged |
| step161 | `8014dbbcdd93bbfdc63b7f2c5a3afff50fbfcf4eb725ffc3deab7683e2e80071` unchanged |
| P05 four logs | `7843b048...` / `735e4650...` / `c76887c6...` / `95a1d184...` unchanged |
| HEAD / staging / diff-check | `715a65884b988ee737f21982f3bbf372860a1da8` / empty / exit `0` |

只改授权五文件；未install/stage/commit/push，未运行benchmark/science/MVE。

## Terminal

`D0_ORDINARY_DOMAIN_AUTHORITY_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION / P0/P1/P2=0/0/0`

该PASS仅关闭T116 author repair；I05/FULL、provenance、HMM与raw positive仍open。
