# Step 170 — D0 FULL positive redundant-recompile hotpath repair

> 2026-08-11 | T124 | PASS

## Scope

本切片只修改 `schemas.py`、`test_d0_schemas_statistics.py` 与本记录，修复 authenticated FULL wrapper 对已认证 ordinary bundle 的重复全量 canonical recompilation。未修改 public `assert_ordinary_runtime_bundle` 的 fresh canonical 深验；未修改 owner/session、其他 code/tests、P05 或 cache，未运行 benchmark、science、MVE、install、stage、commit 或 push。

## Root cause / RED

在真实 FULL positive node 内对 legacy public `assert_ordinary_runtime_bundle` 加调用计数，并用 no-op 替代其深编译主体，以隔离 wrapper 自身重复调用次数。production 修复前结果：

    ORDINARY_RECOMPILE_CALLS=2
    FULL_INCREMENTAL_SECONDS=29.757962
    FULL_AUTHORITY_SHA256=6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484
    1 failed in 177.15s
    RED_STDOUT_SHA256=9b785c727e99dbd1b6a06e7a6cb030498f177e97c6f1d2f673ea6d8c35924055

两次调用分别来自 `build_authenticated_full_authority` 与 `assert_authenticated_full_authority`；node 此前已经由 public factory 建好 ordinary bundle，因此旧路径在同一 positive node 内形成三次 ordinary graph 编译。

## Repair

- `OrdinaryRuntimeBundle` 由 public factory 签发后，在 bundle 外部保存 weak identity issuance record；记录绑定 exact object、owner SHA、identity binding SHA 与 current deep structural fingerprint。
- authenticated FULL build/assert 改用 factory-issued quick verifier：每次都重算 current structural fingerprint 并与外部 issuance record比对；unissued clone、deep mutation、hard-output root/payload mutation、counts 或 owner swap均 fail closed。
- caller 不能提供或注册 fingerprint；bundle 自带字段不作为 issuance 依据。
- public `assert_ordinary_runtime_bundle` 保持原 fresh canonical 深验实现，留给最终 batch verifier。
- FULL authority 另有外部 weak issuance fingerprint，继续逐项验证 owner、HMM plan/runtime、22,800 HMM plan counts与 FULL canonical payload/hash；没有跳过 owner/HMM/FULL authority 检查。

## FULL positive GREEN

环境固定为 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，Python 3.11、`-B -p no:cacheprovider`。最终 positive node同时执行 10 项 mutation rejection：

    python -B -m pytest -p no:cacheprovider -q -s projects/simulation/tests/test_d0_schemas_statistics.py::test_authenticated_full_positive_actual_50287_ledger_authority

结果：

    ORDINARY_RECOMPILE_CALLS=0
    FULL_INCREMENTAL_SECONDS=18.748960
    FULL_AUTHORITY_SHA256=6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484
    FULL_MUTATIONS_REJECTED=10
    1 passed in 219.28s
    FINAL_GREEN_EXIT_CODE=0
    FINAL_GREEN_STDOUT_SHA256=8f0d2ac9d2068853b4e57998539929455f5a55d1609e050ad59af22bc0b158e3

普通图 deep recompile call count `2 -> 0`；ordinary bundle ready 后 FULL build+assert增量 `18.748960s <= 30s`，整 node `219.28s <= 300s`。

| Authority population | Count |
|---|---:|
| ordinary ledger | 27,487 |
| HMM trajectory ledger | 22,800 |
| authenticated FULL ledger | 50,287 |
| HMM chunk identity set | 263,520 |
| HMM EXECUTED / CACHE_READ | 9,600 / 13,200 |

## Mutation matrix

同一真实 positive authority 上逐项突变并恢复，共 10 项；每项均由 public FULL assertion拒绝，wrong accept/reject=`0/0`：

1. unissued exact FULL clone；
2. provenance record root；
3. entry ordinal；
4. S3 output `pilot_score`；
5. aggregate ledger status；
6. aggregate ledger content；
7. hard-output ref `_root`；
8. ordinary counts；
9. FULL owner SHA；
10. FULL total ledger count。

## Focused HMM regression

    python -B -m pytest -p no:cacheprovider -q -s projects/simulation/tests/test_d0_schemas_statistics.py::test_authenticated_hmm_runtime_and_full_api_surface projects/simulation/tests/test_d0_schemas_statistics.py::test_hmm_runtime_exact_sum_owner_golden projects/simulation/tests/test_d0_schemas_statistics.py::test_owner_hmm_plan_full_counts_and_representative_goldens

结果：

    3 passed in 8.48s
    FOCUSED_EXIT_CODE=0
    FOCUSED_STDOUT_SHA256=412bbda474db55ae9ddc083869cdb2a84f6a11d86c923b009521b3e3715bafae

按 T124 时间盒未运行整份 statistics tests；该 fresh batch verification 明确保留给唯一 I05 batch verifier，不影响本切片 terminal。

## Protection / hashes

| Artifact | SHA-256 / value |
|---|---|
| schemas.py | `d5bb1bbc8e8bfeba1f057ea87f57b2fb4713fdd1f852bbe40df0a531f6cc29db` |
| test_d0_schemas_statistics.py | `ad8065661452fd1f130c191404e9495f4d9d990a2f66286a5fb977925f278510` |
| step-169 (read-only) | `7d64489ba178f2e46bd735f73a2a97f78f474162627032ce59a71c506b74cd5d` |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| staged entries | `0` |

- P05 四日志 SHA保持 `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11` / `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b` / `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d` / `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`。
- 测试命令禁止 bytecode 与 pytest cache；未 install、stage、commit、push。

## Terminal

`D0_AUTHENTICATED_FULL_POSITIVE_GREEN`

P0/P1/P2=0/0/0
