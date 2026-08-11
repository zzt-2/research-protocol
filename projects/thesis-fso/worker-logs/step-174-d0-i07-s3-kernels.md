# Step 174 — D0 I07 slice B S3 kernels

> 2026-08-11 | T128 | PASS

## Scope

仅继续修改 `statistics.py`、`test_d0_schemas_statistics.py` 并写本记录。未读写 owner/YAML/artifact，未运行整份 statistics FULL、science、benchmark、MVE、install、stage、commit 或 push。

## RED

先新增 SS08–SS10 三个 node 与 typed 5400-row DEV/TEST fixtures，再在 S3 production API 不存在时真实运行：

    3 failed in 0.86s
    AttributeError: ... has no attribute 'reduce_s3'
    AttributeError: ... has no attribute 'select_s3_lambda'
    RED_EXIT_CODE=1

三个失败均来自预期的 S3 API 缺失；fixtures 已成功构造，不是语法、import 或 row-schema 错误。

## Minimal GREEN

- 每 case exact 10-candidate frozen order；score 降序、exact tie order；truth 由 frozen fixture row 给出。
- 每 case 强制 changed-CW vector=`16,12,12,12,8,8,8,4,4,4`、sum=`88`；cached vector=`0,4,4,4,8,8,8,12,12,12`、sum=`72`；computation ID 禁止跨 candidate/case 共享。
- `select_s3_lambda` 只接受 5400 DEV rows，枚举五个 lambda，词典序 maximize macro fused MRR → macro fused top1 → smaller lambda，返回 I05 typed `S3LambdaFreezeRow`。
- `reduce_s3` 只接受 5400 TEST rows 与 exact typed freeze；case → cell mean → hard/mid/clean equal macro；paired delta 始终同 case `fused_rr-pilot_rr`；bootstrap block 明确为 10 seeds。
- 新结果均为 frozen/slotted dataclass；纯函数、无 I/O/global RNG/truth-view/scientific verdict。

## GREEN / goldens / negatives

固定 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11、`-B`、`-p no:cacheprovider`。

SS08–SS10：

    3 passed in 0.91s

显式 SS01–SS11 局部门（10个 nodes；排除 FULL）：

    10 passed in 1.58s
    GREEN_EXIT_CODE=0
    GREEN_STDOUT_SHA256=483d3b3e8676604ee5b663a6b4a175c57994a54c13160b3ee29d7e78abae3100

Exact goldens：全 score tie、truth=`B08_K2` 时 rank=`6`、RR=`1/6`、top1=`0`；全 lambda 平局冻结 `0.25`；cell fused top1=`1,.5,0` 得 macro=`.5`；paired RR delta=`.5,0,-.5` 得 macro=`0`；candidate rows/cases/seed blocks=`5400/540/10`。

Fresh negatives=13/13 fail closed：candidate missing/duplicate/unknown、truth absent、changed/cache vector drift、DEV/TEST mixed、TEST leakage、freeze hash/type/lambda、cross-case computation reuse；candidate/pol cluster sentinel由 exact `bootstrap_seed_blocks=(8160..8169)` 排除。wrong accept/reject=`0/0`。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| statistics.py | `21723eed90dd6edf2a972f4c785bb0f6952a5bf98eef0e7661612191304c886b` |
| test_d0_schemas_statistics.py | `60261ed4efb54577d0aefbd5468c7de9efdc1c47a969b3383e8e4f50b80f3514` |
| T128 | `f74edcc1be2026912a247762dc4a84ef30a152915c0f18f8fdedd871b8a0aeed` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 SHA 4/4 保持：`7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`、`735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`、`c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`、`95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`。
- 未创建 bytecode/pytest cache；既有 tracked pycache dirty 未扩展。

## Terminal

`D0_I07_STATISTICS_KERNELS_GREEN`

P0/P1/P2=`0/0/0`

该 PASS 关闭 I07 author slices；D0 science 仍为 `NOT_RUN`，下一步只做 I07+I08 一次 fresh batch verifier。
