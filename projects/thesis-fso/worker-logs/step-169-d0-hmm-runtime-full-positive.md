# Step 169 — D0 HMM runtime + authenticated FULL positive

> 2026-08-11 | T123 | INCOMPLETE

## Scope

本切片只修改 `schemas.py`、`test_d0_schemas_statistics.py` 与本记录；其他 code/tests、owner、session、P05 与 cache 只读。未运行 benchmark、science、MVE 或五文件回归。

## RED

先加入 HMM runtime/owner compiler/authenticated FULL focused API gate，production 尚无相应 API 时运行：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_schemas_statistics.py::test_authenticated_hmm_runtime_and_full_api_surface

结果：

    1 failed in 0.82s
    RED_EXIT_CODE=1
    RED_STDOUT_SHA256=05c551e33eb9a010153bbc088a27b939cb479d5dce7ca3ebbfcca2afd8e11a8f

失败一次性列出 8 个缺失 API：resolved member、runtime aggregate build/assert、owner HMM plan build/assert、authenticated FULL build/assert；不是 import、syntax 或 fixture 错误。

## 已落可运行增量

- `ResolvedMemberContent` 与 factory-only `HmmRuntimeAggregateContent`：role 精确约束 10/90 members，ordinal 从 0 连续；binary64 用 `Fraction.from_float` lossless 转 exact rational sum；payload-only canonical SHA256。
- owner-only HMM compiler：从 final `D0OwnerIdentityAuthority` 生成并认证 22,800 trajectory logical identities，实际枚举 9,600 EXECUTED / 13,200 CACHE_READ；direct EXECUTED source leaf、732 logical/materialized score 与 X-owner dual-pol cost逐项生成。
- 263,520 chunk group identity set按 owner tuple/grid/role/cell/pol 顺序实际枚举并流式绑定；没有物化 16,689,600 parameter-pair ledger。
- clean10/target90/sentinel90/M3_N100 四组 chunk/member/computation manifest owner goldens在 production compiler 内复算并命中。
- 最小 authenticated FULL wrapper 已写：绑定 T122 ordinary bundle、owner HMM plan、四组代表 runtime content、raw-table authority 与 27,487+22,800=50,287 ledger counts；但完整 positive public assertion 未在时间盒内跑完，故不宣称 ready。

## HMM focused GREEN

所有命令设置 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，使用 Python 3.11、`-B` 与 `-p no:cacheprovider`。

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_schemas_statistics.py::test_authenticated_hmm_runtime_and_full_api_surface projects/simulation/tests/test_d0_schemas_statistics.py::test_hmm_runtime_exact_sum_owner_golden projects/simulation/tests/test_d0_schemas_statistics.py::test_owner_hmm_plan_full_counts_and_representative_goldens

结果：

    3 passed in 6.04s
    FOCUSED_EXIT_CODE=0
    FOCUSED_STDOUT_SHA256=20b835e5bc2d65387c547081a760ecaaac9266bd8ecf9b6f6672d9ba95a070de

该 run 实际断言：

| 项 | 数量/结果 |
|---|---:|
| HMM trajectory ledger | 22,800 |
| HMM chunk identity set | 263,520 |
| HMM EXECUTED / CACHE_READ | 9,600 / 13,200 |
| ordinary + HMM ledger | 50,287 |
| runtime synthetic exact sum | `123456789 / 2^42` |
| runtime golden content root | `9cf9e195...a0c2` |
| HMM preexecution goldens | 4/4 |

## FULL positive timeout / 未完成边界

真实 FULL node：

    C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_schemas_statistics.py::test_authenticated_full_positive_actual_50287_ledger_authority

该 node 实际构造 T122 全量 ordinary graph、owner HMM plan、四类代表 runtime content，并调用 factory + public assertion；但 factory/assertion当前会重复 fresh recompile 全量 ordinary graph，命令在 364.1 秒被 harness timeout（exit 124），无 PASS stdout、无可引用 positive authority hash。按 T123 明示规则停止，不缩 counts、不跳 public assertion、不把 timeout 写成 PASS。

因此尚未完成：

- authenticated FULL positive public assertion 的新鲜 PASS；
- 新 API 至少 18 项 mutation matrix；
- 最终整份 `test_d0_schemas_statistics.py` GREEN。

建议后续只做一个窄修复：消除 FULL factory/assertion 对已认证 ordinary bundle 的重复全量重编译，同时保留 root/count/source fail-closed；随后重跑该 single node、18 mutations、整文件。不要重做 HMM compiler。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| schemas.py | `be8c249a1d39b6089d970acc4a04e2c08ba8bba1e799f0e09e470ae1d0e7ec37` |
| test_d0_schemas_statistics.py | `14a8dcb7f979ebbd0186032d2c157bd3e288bacb7aa2c8ab1b59caf8056146fc` |
| codec.py (read-only) | `5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331` |
| ordinary tests (read-only) | `ef0b2b7e7b70d1add0fc0e45180455a857cf5d38f9eb58b7ce06d4ea4d04d234` |
| step-168 (read-only) | `ac90a6476e4a61cf02c3b8e1ff84e640c0743ac300c00f64685c9a7d41b7f551` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 四日志 SHA 保持 `7843b048...` / `735e4650...` / `c76887c...` / `95a1d184...`。
- 测试命令禁止 bytecode 与 pytest cache；未 install、stage、commit、push。

## Terminal

`INCOMPLETE — HMM_RUNTIME_OWNER_COMPILER_GREEN; AUTHENTICATED_FULL_POSITIVE_TIMEOUT`

P0/P1/P2=0/1/0

P1 是性能/验证闭环缺口，不是 HMM counts 或 goldens 失败；本切片不得作为 I05 author closure PASS。
