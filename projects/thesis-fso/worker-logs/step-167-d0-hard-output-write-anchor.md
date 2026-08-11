# Step 167 — D0 typed decoder hard-output write anchor

> 2026-08-10 | T121 | PASS

## Scope

本切片只修改 `schemas.py`、`codec.py`、`test_d0_receiver_codec_methods.py` 与本记录。owner、contract、session、其他 tests、P05 与 cache 只读；未运行 benchmark、science、MVE 或 broad discovery。

## RED

先加入两个 owner hard-output golden、opaque typed ref、base64/shape/binary/store fail-closed、`decode_fresh` typed anchor 与 16-CW runtime fixture，再在 production 尚无 factory/typed field 时运行：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_receiver_codec_methods.py::test_decoder_hard_output_owner_goldens_and_opaque_authority projects/simulation/tests/test_d0_receiver_codec_methods.py::test_decoder_hard_output_factory_and_store_fail_closed projects/simulation/tests/test_d0_receiver_codec_methods.py::test_ldpc_noiseless_roundtrip_one_cw

结果：

    3 failed in 4.13s
    RED_EXIT_CODE=1
    RED_STDOUT_SHA256=b9f61b2eefea85fd8fdc80f1f10a6a4994f86787c350eef83cab5a153abe5731

失败原因精确为两个缺少 `build_decoder_hard_output_ref`、一个 `DecodeBatch` 缺少 `hard_output`，不是语法或导入夹具错误。

## Minimal GREEN

- `schemas.py`：新增 factory-only、issued-instance gate 的 `DecoderHardOutputRef`；16×1024 binary bits 按 CW-major/MSB-first pack 为 2048 bytes 和 RFC4648 base64；payload-only canonical JSON SHA256；fresh `info_bits` materialization；exact store record 与双向 exact-set validator。
- `codec.py`：`DecodeBatch` 持有 typed `hard_output`，兼容 `info_bits` 每次 fresh materialization；`decode_fresh` 收紧为 exact `(16,1536)`，backend hard output完成 shape/dtype/finiteness/binary gate 后立即只以 `info_bits` 调 factory。
- unit fixture：noiseless/fresh/negative 路径统一 16 CW。首次 GREEN 唯一失败是测试 mutation 把全零 base64 首字符 `A` 改成同一个 `A`；按任务允许的一次 fixture 修正改为 `B`，未修改 production 行为。

## GREEN / negative

所有命令均设置 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用 Python 3.11、`-B` 与 `-p no:cacheprovider`。

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_receiver_codec_methods.py

结果：

    9 passed in 4.21s
    GREEN_EXIT_CODE=0
    GREEN_STDOUT_SHA256=f4c84b2d2694b18e33bb2dd3c11c9d58cd5168663d25492f805a62838902d8bb

Fresh hard-output negative/mutation cases=16/16 fail closed：shape 3、nonbinary/nonfinite/dtype 6、factory-only/copy-forgery 2、store duplicate/missing/orphan/wrong-root/changed-payload 5；wrong accept/reject=0/0。既有 backend-output negatives 6/6 亦通过。两个 owner golden 精确为：

- all-zero: `1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960`
- first-bit: `9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e`

AST 静态检查：`codec.py` 恰有 1 次 `build_decoder_hard_output_ref(info_bits)`，1 个 positional bits 参数、0 keyword、0 caller hash 参数。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| schemas.py | `80e69a63ded7f7385c6aef8c4806ec53bc51bdcc2f86743e1cdc124a49dcb1cc` |
| codec.py | `5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331` |
| test_d0_receiver_codec_methods.py | `28401d747ff13143ca828753cf910aac88974f52e0d672edc96d2916767a6d6e` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 四日志 SHA 保持 `7843b048...` / `735e4650...` / `c76887c...` / `95a1d184...`。
- 测试命令禁止 bytecode 与 pytest cache；首次状态中已有的 tracked cache dirty 列表未扩展，未创建 `.pytest_cache`。
- 未 install、stage、commit、push；未修改 owner、contract、session、其他 tests。

## Terminal

`D0_TYPED_HARD_OUTPUT_WRITE_ANCHOR_READY_FOR_BATCH_VERIFICATION`

P0/P1/P2=0/0/0

该 PASS 只关闭 T121 author slice；独立验收按任务约束推迟到 I05 三代码片完成后的单次 batch verifier。
