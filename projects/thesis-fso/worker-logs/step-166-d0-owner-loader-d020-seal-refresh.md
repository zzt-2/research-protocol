# Step 166 — D0 owner loader D020 seal refresh

> 2026-08-10 | T120 | PASS

## Scope

本切片只修改 contract.py、test_d0_contract_views.py 与本记录。owner、session、其他code/tests、P05与cache只读；未运行benchmark、science、MVE或broad discovery。

## RED

先更新test-side final owner/identity seals，新增focused D020 typed-view test，并把public-loader owner mutation矩阵从28扩到42；production常量尚未修改。

命令：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_authority_exact_frozen_view projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_d020_runtime_content_exact_frozen_view

结果：

    2 failed in 0.61s
    RED_EXIT_CODE=1
    RED_STDOUT_SHA256=8b5db8f71e5129d7a2794314d78c8f9c02bf5515461a732a73b3728f33d12e5d

两项均在 contract.py:1497 因 production _FROZEN_OWNER_SHA256 仍为旧seal而失败；不是语法、fixture或断言错误。

## Minimal production change

只替换两个字符串常量：

- _FROZEN_OWNER_SHA256：02d471a... → f159efae...
- _FROZEN_IDENTITY_BINDING_SHA256：68d21b4a... → 08a90d7e...

未改dataclass、loader逻辑、13-key顺序、science/domain/grid seal、函数签名或其他production行。

## GREEN

所有命令均设置 PYTHONDONTWRITEBYTECODE=1、PYTHONHASHSEED=0，使用Python 3.11、-B与-p no:cacheprovider。

### Selected owner-loader nodes

覆盖exact frozen view、focused D020 view及42项public-loader mutation。

    3 passed in 12.18s
    GREEN_SELECTED_EXIT_CODE=0
    GREEN_SELECTED_STDOUT_SHA256=522a4ce27c6c86294c54412a70416f6c21910932643a9c5811747daf6739170d

Focused view逐项验证11个新增payload schema版本/字段序、hard-output常量、runtime hard/provenance/group/source/count/sidecar/write-anchor、20个golden组及10个新增literal roots；新runtime/golden嵌套不可变，fresh load无alias。

Mutation矩阵=42/42 fail closed，包含此前漏测的 decoder_hard_output.version，以及field order/base64/provenance entry/source/count/sidecar/write order/golden input+root/validator obligations。

### Full contract views

    16 passed in 14.03s
    GREEN_CONTRACT_EXIT_CODE=0
    GREEN_CONTRACT_STDOUT_SHA256=fec1f55876c5dc7fad7963e82ddb51bf7b7cc2d46cc5539fc2ef0c3d6fd2bf50

### Explicit five-file regression

文件为contract views、ordinary identity、schemas statistics、receiver codec methods、waveform channel；未做broad discovery。

    62 passed in 188.99s (0:03:08)
    GREEN_REGRESSION_EXIT_CODE=0
    GREEN_REGRESSION_STDOUT_SHA256=c139641d00831a47c66156e3f1ae2362eecb22af9549c3bfb35e64311f00e6c2

## Static / protection gate

独立AST/static oracle确认当前production恰含两个final seal常量；把这两个literal逆替换为pre-state后，contract.py SHA精确还原 cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a，因此production diff恰为两常量。

| Artifact | SHA-256 / value |
|---|---|
| owner | f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b |
| scientific projection | c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d |
| identity seal | 08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e |
| ordinary domain seal | 15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69 |
| contract.py | f6e000dcddd8661d2b52ea08de6c2a137cf7fd8f661d2ca415e9b56227ff1aaa |
| test_d0_contract_views.py | 8fa721a984f83b89c410dad93a6e061d381562268a2a72f57f42b20d5035ac8f |
| step-165 | a0346cef7f4a5189501f35a3b174d20a2c802e973f624e8b5c91dea0cbbe747b |

- HEAD=715a65884b988ee737f21982f3bbf372860a1da8；staging entries=0。
- P05四日志SHA保持7843b048... / 735e4650... / c76887c... / 95a1d184...。
- owner/science/domain均与T120 frozen input一致。
- 未install、stage、commit、push；未写pytest cache或Python bytecode。

## Terminal

D0_OWNER_LOADER_D020_SEAL_REFRESH_READY_FOR_INDEPENDENT_VERIFICATION

P0/P1/P2=0/0/0

该PASS只关闭T120 author seal refresh，不代表owner独立终验、sidecar实现或I05完成。
