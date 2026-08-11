# Step 168 — D0 ordinary provenance runtime bundle

> 2026-08-10 | T122 | PASS

## Scope

本切片只修改 `schemas.py`、`test_d0_ordinary_identity.py` 与本记录；`test_d0_schemas_statistics.py` 只读并纳入 GREEN。codec、owner、contract、session、其他 tests、P05 与 cache 只读；未运行 benchmark、science、MVE 或 broad discovery。

## RED

先加入 focused API gate，production 尚无 7 类 typed consumer output 及 build/assert API 时运行：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_ordinary_identity.py::test_ordinary_runtime_api_surface_is_complete

结果：

    1 failed in 0.26s
    RED_EXIT_CODE=1
    RED_STDOUT_SHA256=c6a3856c1b5514e10d756d3adc11d20e40981585d2cec4424c61c07539c69766

失败详情一次性列出 `S2Off/S2On/S3/Bps/B2Clean/B2Controlled/S4ConsumerOutput` 与 `build/assert_ordinary_runtime_bundle` 共 9 项缺失；不是 import、syntax 或 fixture 错误。

## Minimal implementation

- 7 类 frozen typed output；6 个 non-S4 variant 只接收 T121 已签发 `DecoderHardOutputRef`，不接收 caller hash。S3/BPS 只接收 finite exact Python float 并在序列化边界生成 float64 hex；rotation、S4 count/pass/evidence fail closed。
- typed provenance entry/payload/store record、aggregate-ledger binding 与 opaque runtime bundle；builder 对 final owner 与 canonical plan 重新认证，要求 outputs_by_pk 42,967 项 exact set。
- 从 plan 实际分组并逐 entry 推导 S2-off/BPS/B2 source、status、ordinal 与 direct EXECUTED leaf；B2 controlled 按 TARGET→SENTINEL 重排，cache 端逐项校验 source computation/PK 与 decoded content。
- 每个 payload root 为 canonical payload-only SHA256；aggregate content 绑定同 root；non-S4 hard roots 汇总后调用 T121 exact forward/reverse store gate，无 orphan。
- `assert_ordinary_runtime_bundle` 从 bundle entries 重建 outputs mapping，再对 owner/plan 重新认证并 fresh canonical recompilation，不信任 bundle 自带 count/root/status/source。

## GREEN

所有命令均设置 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用 Python 3.11、`-B` 与 `-p no:cacheprovider`。

初次 focused 全量枚举：

    3 passed in 106.82s
    FOCUSED_EXIT_CODE=0
    FOCUSED_STDOUT_SHA256=7d77c97ffc9b0419cb08987a37ec4ac96c5b8ead7b8f2930942e2e2965e98f17

两个指定完整测试文件：

    25 passed in 287.09s
    GREEN_EXIT_CODE=0
    GREEN_STDOUT_SHA256=47a688bb1c8e0db9c1ad1a86870584eef4ba29f020a9ca7b3f15753c5de83325

随后只补足 missing/extra output PK 两个负向（production 未变），按主线“本 run 后立即收口”指令仅重跑受影响 focused nodes：

    2 passed in 124.05s
    FINAL_FOCUSED_EXIT_CODE=0
    FINAL_FOCUSED_STDOUT_SHA256=b82f7b5dae17eb58e17ee4b5834d1efc560a4291c55002ce0da6c9708c4cec5f

三次均为 0 fail/error/skip/xfail/warning。

## Exact graph / goldens / negatives

实际图枚举结果：

| 项 | 数量 |
|---|---:|
| provenance records / aggregate rows | 27,487 |
| entries | 42,967 |
| EXECUTED / CACHE_READ entries | 30,247 / 12,720 |
| S2 / BPS / B2 cache edges | 480 / 1,440 / 10,800 |
| singleton / nine-entry / two-entry groups | 12,427 / 60 / 15,000 |
| aggregate EXECUTED / CACHE_READ | 26,767 / 720 |
| non-S4 hard-output references | 42,960 |

8/8 owner provenance goldens 精确命中：S2-off `e8ca16c9...`、S2-on `ee5f608c...`、S3 `8caf721a...`、BPS M2 `bb50e568...`、BPS M3 `580d6d10...`、B2 clean `5ab4e4d9...`、B2 controlled `25966bd9...`、S4 `cbe018c5...`。

Fresh negative/mutation=18/18 fail closed，wrong accept/reject=0/0：arbitrary string/ref variant 6、S3 float field 3、BPS rotation/NLL 3、S4 count/pass/evidence 4、missing/extra output PK 2。bundle assertion 的 fresh canonical recompilation同时覆盖 entry order/ordinal/status/source/root/count/hard-store 任一偏移；具体攻击矩阵留给 I05 唯一 batch verifier，未另派审查。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| schemas.py | `a344a299ee07aa603408ccd9c2f9cad78a9b4f56b64a1b29ccb62a421058aa4e` |
| test_d0_ordinary_identity.py | `ef0b2b7e7b70d1add0fc0e45180455a857cf5d38f9eb58b7ce06d4ea4d04d234` |
| test_d0_schemas_statistics.py (read-only) | `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9` |
| codec.py (read-only) | `5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331` |
| codec tests (read-only) | `28401d747ff13143ca828753cf910aac88974f52e0d672edc96d2916767a6d6e` |
| step-167 (read-only) | `cac69b021dd06cbaee7ab353b94b4170b4fab17bf0405095e49439cf97296810` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 四日志 SHA 保持 `7843b048...` / `735e4650...` / `c76887c...` / `95a1d184...`。
- 测试命令禁止 bytecode 与 pytest cache；未创建新 cache。
- 未 install、stage、commit、push；未修改 owner、codec、contract、session 或其他 tests。

## Terminal

`D0_ORDINARY_PROVENANCE_RUNTIME_BUNDLE_READY_FOR_BATCH_VERIFICATION`

P0/P1/P2=0/0/0

该 PASS 只关闭 T122 author slice；独立验收按 D022 留给 I05 三代码片后的唯一 batch verifier。
