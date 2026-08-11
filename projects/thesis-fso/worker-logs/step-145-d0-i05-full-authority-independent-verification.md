# Step 145 — D0 I05 FULL authority independent verification

> 2026-08-10 | T099 | fresh non-author, authority-only verification
> evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

## Findings first

`VERDICT=FAIL`，`P0/P1/P2=0/1/0`。

- 三组 fresh pytest 均为绿色：T098 三个 exact nodes 为 3/3 PASS，完整 schemas 为 13/13 PASS，显式展开的全部 `test_d0_*.py` 为 46/46 PASS；均为 0 fail/error/skip/xfail/warning。
- 88 个预标 accept/reject 的常规独立 robustness cases 全部符合预期，mismatch=0。generic PARTIAL、普通 FULL factory、owner identity、FIRST/MAX、plan、table/projection/digest 等常规路径未发现偏差。
- 但是，`_compile_full_relational_manifest` 使用 `@lru_cache(maxsize=4)` 返回共享 canonical 对象。该共享对象经低层属性赋值改变 `authority_sha256` 后，factory 从同一缓存对象生成 digest 不一致的结果；validator 又从同一缓存取回已改变的 canonical，因而接受了该结果。独立重算确认保存的 authority digest 与结构内容不一致。
- 因此“validator 从保存的 authority spec 重新编译独立 canonical 并逐字段比较”的承重要求没有成立。tests GREEN 与常规矩阵 GREEN 不能覆盖此共享状态缺口，按 T099 门控计一个 P1，必须 FAIL。

本结论只针对 authority-only slice。raw FULL positive path 未运行；typed HMM per-group/member binding 与 consumer-to-ledger binding 仍为 OPEN；没有授权 benchmark、science、MVE 或 held-out experiment。

## Frozen inputs and boundary

完整读取了 T098/T099、step-134/144、current schemas/tests 与 owner coverage/identity 段。冻结输入在验证前匹配：

```text
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_d0_schemas_statistics.py=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
step-134=81e94ed47c2ac46c7bc9d8b1056f569d8edb5ca17f9661b9e3282d8d6ca6e04c
step-144=05446c08a37258c84de4c53028219eb34805d08f5bc53d3c62442306e8e8b0f4
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
```

本 verifier 只创建本日志；未修改 source、tests、governance 或其他日志，未 install/commit/push/stage，未运行 raw FULL bundle、benchmark/science/MVE/web。

## Fresh pytest

固定环境为 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11 `-B -m pytest -p no:cacheprovider`。

| scope | result | fail/error/skip/xfail/warning | output SHA256 |
|---|---:|---:|---|
| T098 三个 exact nodes | 3 passed in 8.68s | 0/0/0/0/0 | `7f248073e1f29f76f22daae9eb10750cced94bc9545ced2f3627e7d5a1d78c9c` |
| 完整 schema test file | 13 passed in 8.70s | 0/0/0/0/0 | `625ca2780d983a9ea95115cb6cb220241ea0e813cb1150e61179881907f8865a` |
| 显式 current `test_d0_*.py` aggregate | 46 passed in 14.27s | 0/0/0/0/0 | `2ea4b579855c264eac0885aba6c90914fea2a9f6566439e8828f50e11fad4a9d` |

aggregate 显式包含 `test_d0_contract_views.py`、`test_d0_receiver_codec_methods.py`、`test_d0_schemas_statistics.py` 与 `test_d0_waveform_channel.py`。

## Independent regular robustness matrix

每例执行前均预标 accept/reject；只有期望拒绝却返回，或合法 control 被拒绝，才计 mismatch。

| category | total | accepted | rejected | mismatch |
|---|---:|---:|---:|---:|
| legal controls | 8 | 8 | 0 | 0 |
| generic PARTIAL/FULL construction | 9 | 0 | 9 | 0 |
| owner/control/code/population/seed identity | 16 | 0 | 16 | 0 |
| extent/HMM/computation plans | 22 | 0 | 22 | 0 |
| manifest/table/projection/digest/seal | 33 | 0 | 33 | 0 |
| **total** | **88** | **8** | **80** | **0** |

覆盖 generic direct/replace/object-field change、opaque FULL direct construction、owner/control/code/population/seed、extent、HMM 与 computation plan axes/entry、十张表的 drop/add/reorder/substitute、projection count/key/multiplicity、coverage/seal、改表后重算公开 digest、FIRST/MAX crossing；合法 PARTIAL 与 factory canonical FULL authority 结构作为 controls。

```text
matrix_output_sha256=1c4291079373559e74c9bfaa79905cfec6be1a994121ee8bf5a6f8f15d352753
FIRST_STAGE_coverage_sha256=a66aa0abd6705db2d8ac837f65c7d2d30165a01a6f006040de2c0221fe263edf
FIRST_STAGE_authority_sha256=56462d6f6f80b343b909f340c20a8825c88379e4b39b4b03bfc98353126797c7
MAXIMUM_coverage_sha256=9e5ccc56215575700cdfd69a15a51572981b95d6be752c91e56baecf8de7ac21
MAXIMUM_authority_sha256=050b2832916b1988fcd50d92ff545c6909868620ce1306cb609be8bc28a736a2
```

上述常规矩阵为 GREEN，但不改变下述共享 canonical 一致性 finding。

## P1 — shared cached canonical consistency

静态路径如下：

1. `_compile_full_relational_manifest` 带 `@lru_cache(maxsize=4)`，其返回值是进程内共享的 `FullRelationalManifest` canonical 对象。
2. `build_full_relational_manifest` 调用该 compiler，再 clone 返回值。
3. `assert_full_manifest_authority` 使用 manifest 保存的 spec 调用同一个 cached compiler，并以 `manifest != canonical` 作为最终一致性门。
4. `frozen=True` 阻止普通赋值，但不能使共享对象免于低层 `object.__setattr__`；一旦 cached canonical 本身被改变，factory 与 validator 会共同采用同一已改变参照。

独立最小复现只改变缓存 canonical 的 `authority_sha256`，随后走公开 factory 与 validator：

```text
ORIGINAL_AUTHORITY=56462d6f6f80b343b909f340c20a8825c88379e4b39b4b03bfc98353126797c7
FORGED_AUTHORITY=1111111111111111111111111111111111111111111111111111111111111111
FORGED_EQUALS_RECOMPUTED_DIGEST=False
CACHE_POISON_FORGED_ACCEPTED=True
INNER_EXIT=1
output_sha256=7b7f4bb3e1b3a6c87f07612170c06b0da0448467ee3ece52a6baff6d5a32a796
```

这里 `INNER_EXIT=1` 表示预期拒绝的 digest 不一致对象被接受。该现象不是普通 table mutation 后仅重算公开 coverage digest；它直接证明 validator 的 recompilation reference 并非独立、未改变的 canonical authority。因此 T099 第 3、4 项的承重不变量未满足。

## Code review disposition

- generic `RelationalManifest` 的正常 constructor/replace/field-change paths 保持 `EXPLICIT_PARTIAL`，常规 cross-validator cases 均 fail closed。
- `FullRelationalManifest` direct constructor 不可用；factory 未依赖 module token/secret。
- owner exact identity assertion、FIRST/MAX、HMM/computation plan drift 与 table/projection/digest drift 在常规新鲜对象路径均 fail closed。
- 但 compiler cache 使 factory 与 validator 共享可改变的 canonical reference，推翻“重新编译即独立权威比较”的核心前提；故前述正常路径证据不足以 PASS。
- raw FULL positive=`NOT_RUN`；typed HMM binding=`OPEN`；consumer-ledger binding=`OPEN`。

## Static, hashes, and protection

AST/import 检查确认 source 可解析、可导入，`FullRelationalManifest` 为 `dataclass(frozen=True, slots=True, init=False)`；同时明确确认 compiler 为 `lru_cache(maxsize=4)`，factory 与 validator 均调用该 cached compiler，validator 使用 equality gate。source 内无 `sys.path` mutation、global RNG convenience call 或 I/O call。

```text
static_import=PASS_WITH_P1_FINDING
static_output_sha256=f71780a1b43ac92e944e500b5986be703d1cb585a06c4e96145033d355674d17
git_diff_check_exit=0
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_d0_schemas_statistics.py=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
step-134=81e94ed47c2ac46c7bc9d8b1056f569d8edb5ca17f9661b9e3282d8d6ca6e04c
step-144=05446c08a37258c84de4c53028219eb34805d08f5bc53d3c62442306e8e8b0f4
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
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

`git diff --check` exit=0；仅有工作树既有 LF→CRLF 提示，无 whitespace error。保护核验未发现 source/tests/owner/step-134/144、HEAD、staging、P05 或 cache 漂移。

## Terminal

`terminal=FULL_AUTHORITY_VERIFICATION_FAIL`
