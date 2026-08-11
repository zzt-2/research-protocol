# Step 147 — D0 I05 fresh authority graph independent reverification

> 2026-08-10 | T101 / D014 | fresh non-author, final-byte verification
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## Findings first

`VERDICT=PASS`，`P0/P1/P2=0/0/0`。

- T100 两个 exact nodes 为 2/2 PASS，完整 schemas 为 15/15 PASS，显式展开的全部 `test_d0_*.py` 为 48/48 PASS；三组均以 warnings-as-errors 运行，0 fail/error/skip/xfail/warning。
- 精确重放 step-145 共享实例反例：改变一次 factory 输出的 authority SHA、首张表 identity 与 nested projection count 后，该对象被 authority gate 拒绝；随后同 spec 连续 10 轮 factory/validator 输出均恢复 canonical，保存 digest 与独立重算一致。
- FIRST_STAGE/MAXIMUM × 两套合法 HMM/computation plan 共四组输入，递归检查 700 对输出图中的非 primitive 对象；跨 compile 身份共享为 0。caller authority inputs 不被输出 spec 直接保留。
- 全部 memoization 审计只发现 `_compile_full_relational_manifest_primitives` 一个 `lru_cache`；其返回值为递归 immutable primitive tuple，不包含 dataclass、list/dict/set、ndarray 或自定义对象。正确性不依赖 `cache_clear` 或调用顺序。
- 56 个预标 accept/reject 的代表性 authority cases 为 5 accept、51 reject、mismatch=0，保留 PARTIAL/FULL structural controls，并覆盖 owner/spec、extent、两类 plan、cell/seed、全部十张表与 projection/digest 变化。

因此 step-145 的 shared canonical reference P1 已由 fresh object graph 与独立重算证据关闭。PASS 只覆盖 authority-only slice；raw legal FULL positive path 仍为 NOT_RUN，typed HMM per-group/member binding 与 consumer-to-ledger binding 仍为 OPEN，未授权 benchmark、science、MVE 或 held-out experiment。

## Frozen inputs and boundary

完整读取了 T100/T101、D014、step-145/146 与 final source/tests。验证前后冻结输入保持：

```text
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
test_d0_schemas_statistics.py=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
step-146=e39b7f2b3c548c3200ac46ae65a400821f4270e82729e92c9163e247f71729b7
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
```

本 verifier 只创建本日志；未修改 source、tests、governance 或其他日志，未 install/commit/push/stage，未运行 raw FULL bundle、benchmark/science/MVE/web。

## Fresh final-byte pytest

固定环境为 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11 `-B -m pytest -p no:cacheprovider -W error`。

| scope | result | fail/error/skip/xfail/warning | output SHA256 |
|---|---:|---:|---|
| T100 两个 exact nodes | 2 passed in 23.95s | 0/0/0/0/0 | `c3e261c1ea9092204c15fcd59fd9c1940bbc6cd9d3e9e4a2def29ccbc9403cd2` |
| 完整 schema test file | 15 passed in 24.09s | 0/0/0/0/0 | `ccd0066e89209c82fe6dc82eb5c60e1d5a913d7b99a09dedfe36dfcbb5691da5` |
| 显式 current `test_d0_*.py` aggregate | 48 passed in 31.74s | 0/0/0/0/0 | `7159f53ab09de91ad4f872ce2147a8b2db89f0fdc5eeaa7ed70bd219d2179a1a` |

aggregate 显式包含 `test_d0_contract_views.py`、`test_d0_receiver_codec_methods.py`、`test_d0_schemas_statistics.py` 与 `test_d0_waveform_channel.py`。

## Shared-instance replay and ten-round stability

独立 stdin 程序不导入 test helpers。它从冻结 owner 构造两套合法 plan，并对 factory 输出执行以下次序：

1. 保存未改变 FIRST_STAGE 输出的 authority/coverage/table/projection receipts。
2. 另建 factory 输出，以低层属性赋值分别改变 authority SHA、首张表 identity 与 nested projection count。
3. 确认 authority gate 拒绝该对象。
4. 连续 10 次以相同 authority inputs 调用 factory 与 gate；每轮独立调用 `_full_authority_sha256` 与 `full_coverage_sha256` 重算，并与输出保存值比较。
5. 每轮递归比较前后输出图的非 primitive 对象 identities。

```text
REPLAY_CHANGED_REJECTED=True
REPLAY_10_ROUNDS_CANONICAL=True
BASE_AUTHORITY=339e948a115a7d33ba6d5fd586a99bd2d99306384261d93d1750827c1b91aef2
BASE_COVERAGE=cede04072e816d55bfbc7687dc3677c047f51f1e5ec31b4bc506a89a76fc0f32
TEN_ROUND_ISOLATION_OBJECT_PAIRS=500
TEN_ROUND_SHARED_NONPRIMITIVE_OBJECTS=0
```

该 receipt 使用 verifier 自建 computation IDs `p1-hmm` / `p1-s4`，因此 authority/coverage 值不要求等于 step-145 使用另一套合法 computation IDs 的历史值；承重检查是同一 authority inputs 下保存值、独立重算与后续 fresh outputs 三者一致。

## Independent object-isolation matrix

四组输入覆盖：

- FIRST_STAGE + plan-1
- MAXIMUM + plan-1
- FIRST_STAGE + plan-2
- MAXIMUM + plan-2

两套 HMM plan 使用相同冻结 axes/counts 但不同合法 namespace digests；两套 computation plan 均为合法 HMM/S4 standalone entries，但使用不同 computation identities。每组分别 compile 两次并校验 gate，再递归收集 manifest、spec、owner contract、HMM/computation plan 及 entries、cell domains、seed sets、十张 tables、十一项 projections 等所有 dataclass/list/dict/set/custom nodes。

```text
INPUT_SETS=4
BASE_ISOLATION_OBJECT_PAIRS=200
TEN_ROUND_ISOLATION_OBJECT_PAIRS=500
ISOLATION_OBJECT_PAIRS_TOTAL=700
SHARED_NONPRIMITIVE_OBJECTS=0
CALLER_OWNER_SHARED_WITH_OUTPUT=False
CALLER_HMM_PLAN_SHARED_WITH_OUTPUT=False
CALLER_COMPUTATION_PLAN_SHARED_WITH_OUTPUT=False
MEMOIZED_RETURN_RECURSIVELY_PRIMITIVE=True
CACHE_CLEAR_USED=False
```

递归 primitive 定义仅包括 exact `str/bytes/int/float/bool/None` 及完全由这些元素构成的 tuple/frozenset；这些不可变值允许共享，不计对象隔离失败。

## Representative authority matrix

每例在执行前注册唯一名称和 `EXPECT_ACCEPT` / `EXPECT_REJECT`；合法 case 抛异常或应拒绝 case 返回均计 mismatch。

| category | representative coverage | result |
|---|---|---:|
| structural controls | PARTIAL structure；FIRST/MAX；alternate plan；fresh FULL | 5 accept |
| generic/FULL construction | direct、replace、低层 scope change、cross-gate | reject |
| spec/owner | schema、owner SHA、extent、owner identity、FIRST/MAX spec crossing、wrong type | reject |
| HMM plan | p/sigma axes、roles、cells、polarizations、counts、scheme、namespace | reject |
| computation plan | empty、duplicate、phase/operation、orphan source | reject |
| manifest/domain/seed | scope、coverage、authority、drop/name/value/type | reject |
| tables/projections | 十张表逐一 drop、add/reorder/substitute、projection empty/count/key/multiplicity、public digest recompute | reject |

```text
AUTHORITY_CASES=56
AUTHORITY_ACCEPTED=5
AUTHORITY_REJECTED=51
AUTHORITY_MISMATCH=0
AUTHORITY_CASE_RECEIPT_SHA256=ff5fbca949ed25b3782d4c00b6b4570702a1cb5c1e5cb7d86e05a73b7e504776
ISOLATION_AND_AUTHORITY_OUTPUT_SHA256=e6660945de3f5d9856c1db159df9e1bcd835faecffa27442ee744a60eba7bb0b
```

## Memoization and code review

- `_hmm_expectation` 不再缓存对象；每次构造新的 table 与两个 projections。
- `_compile_full_relational_manifest_primitives` 是唯一带 `lru_cache` 的函数。AST 确认其唯一 return 调用 `_freeze_full_components`；后者只投影为嵌套 primitive tuples 与 digest strings。
- `_compile_full_relational_manifest` 每次 fresh 构造 `FullManifestSpec`，deep-copy caller owner/plans，再由 primitive receipt 重新物化所有 domain/seed/table/projection dataclasses。
- factory 对 compile 输出再 clone；validator 独立 compile 并逐字段 equality compare。两条路径不共享 canonical object graph。
- source 中 `cache_clear` reference 为 0，正确性不依赖清理时序、token 或 secret。
- generic `RelationalManifest` 仍为 PARTIAL-only；owner identity、FIRST/MAX 与 plan drift 均保持 fail closed。

## Static, hashes, and protection

AST/import 检查确认 source 可解析、可导入；object-returning cache=0，source 内无 `sys.path` mutation、global RNG convenience call 或 I/O call。

```text
static_import=PASS
cached_functions=_compile_full_relational_manifest_primitives
cached_function_count=1
object_returning_cache_count=0
cache_clear_refs=0
static_output_sha256=ed23118efdda38905dd7159049e622840edb0d7da5ef609213917b61658eb4b6
git_diff_check_exit=0
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
test_d0_schemas_statistics.py=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
step-146=e39b7f2b3c548c3200ac46ae65a400821f4270e82729e92c9163e247f71729b7
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
commit=none
push=none
```

`git diff --check` exit=0；仅打印工作树既有 LF→CRLF 提示，无 whitespace error。source/tests/owner/step-145/146、HEAD、staging、P05 与 cache 均未漂移。

## Open boundaries

- Raw legal FULL positive oracle: `OPEN / NOT_RUN`。
- Typed HMM per-group/member binding: `OPEN`。
- Consumer-PK to computation-ledger binding: `OPEN`。

## Terminal

`terminal=FULL_AUTHORITY_VERIFIED_POSITIVE_AND_BINDINGS_PENDING`
