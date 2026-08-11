# Step 155 — D0 owner identity typed loader independent verification

> 2026-08-10 | T109 | `PASS`

## Scope / terminal

- 只读审查 T108 final bytes；未采用 step-154 的 PASS、作者 mutation helper 或作者 expected 派生作为结论。
- 唯一写入为本 step-155；未 install/stage/commit/push，未运行 benchmark/science/MVE。
- terminal：`OWNER_IDENTITY_TYPED_LOADER_INDEPENDENTLY_VERIFIED`
- 本 PASS 仅接收 additive typed loader 并 fresh 重封 I06；I05 bindings 仍 open。

## Frozen bytes / static boundary

- HEAD：`715a65884b988ee737f21982f3bbf372860a1da8`；staged files=`0`。
- `D0Contract` exact fields：`schema_version, control, population, seed_registry`；`load_contract(path)` 保持单参数及既有四字段返回。
- `IdentityBindingContract`、`D0OwnerIdentityAuthority`、`load_owner_identity_authority`、public revalidation 为 additive；全仓新 identity API 引用仅在 `contract.py` 与 `test_d0_contract_views.py`。
- `channel.py` 仍只接 `D0Contract`，不引用/触发新 loader；`schemas.py` 亦不引用新 loader。import fresh 执行无 I/O；通用 `_deep_freeze` 仍要求 exact string mapping keys，两处 owner integer-key anchors 在 loader 前 typed-normalize。
- begin/end hashes一致；owner/session/schema/source/test/step153/step154均无漂移。

## Fresh public-boundary oracle

不调用 production private canonical/hash helper；从 public immutable view 自行转为 canonical JSON，独立使用 `json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)` 与 SHA-256。

```text
AUTHORITY_ORACLE_PASS assertions=430 literals=128 roots=3 anchors=8 sections=13
MUTATIONS_PASS rejected=31/31 wrong_accept=0 wrong_reject=0
SEALS=owner:ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535,science:c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d,identity:29d1fc77bc3028861df04e3442de07ffabc0d72a68a2e4666f3b318b98b48ec6
ORACLE_EXIT=0
ORACLE_STDOUT_SHA256=fefaf1eb83a20ae5c27e5bfd192d24f1b0cfb05c047f47931324fbd7e2f5f109
```

- 122 `p_s` + 6 `sigma_e2` literals：连续 exact-int index；canonical finite nonnegative binary64 hex；仅两个 index 0 为 canonical `+0.0`，其余 126 个严格正值。
- roots：`p_s=bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864`；`sigma_e2=0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca`；`combined=0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf`。
- 两处 integer-key anchor 均为 `tuple[Float64Literal,...]`，各 4 项，exact indices=`0,1,61,121` 与 exact hex。
- exact 13-key structure/header、无 nested mutable state、两个 fresh load 的 root/nested view 分离、外部 mapping/dataclass/anchor assignment 全拒绝。
- ledger exact：chunks `263520`、logical trajectory `22800`、logical primitive `16689600`、executed trajectory `9600`、materialized primitive `7027200`、cache trajectory `13200`。

Fresh rejection names：

```text
omitted,extra,top_order,section_type,header_type,anchor_index,anchor_hex,
gold_anchor_index,bool_index,negative_zero,noncanonical,duplicate_literal,
literal_order,literal_count,p_root,s_root,c_root,combined_drift,payload_order,
binding_kind,ledger_count,cache_source,canonical_rule,json_float,duplicate_key,
owner_hash,science_hash,identity_hash,binding_header,nested_replace,contract_replace
```

首次 verifier-only oracle 因未锚定 `bytes.find("strata:")` 命中嵌套字段而 exit 1（stdout SHA `a48067f940bdec4b486453bb7378ab865d3b2e1727ab81bfa664729f5cc8e4ee`）；定位为 verifier marker 缺陷后，仅改为独立的行首唯一 marker，并完整重跑得到上述 PASS。该失败未进入被测 public boundary，不计产品缺陷。

## Fresh pytest

环境：`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11 `-B -m pytest -p no:cacheprovider`。

四个 T108 exact nodes：

```text
collected 4 items
projects\simulation\tests\test_d0_contract_views.py ....                 [100%]
============================== 4 passed in 5.54s ==============================
EXACT_EXIT=0
EXACT_STDOUT_SHA256=8f40c3f7555a64d770add1a5e23c3f50b26de979515e71ad522de36874f012e0
```

显式四文件全量：

```text
collected 52 items
projects\simulation\tests\test_d0_contract_views.py .............        [ 25%]
projects\simulation\tests\test_d0_receiver_codec_methods.py .......      [ 38%]
projects\simulation\tests\test_d0_schemas_statistics.py ...............  [ 67%]
projects\simulation\tests\test_d0_waveform_channel.py .................  [100%]
============================= 52 passed in 34.48s =============================
FULL_EXIT=0
FULL_STDOUT_SHA256=76af7f8dfcf575fc8263547f5adcb2d8b18050a6707030e2ebb6287b901c4499
```

fail/error/skip/xfail/warning=`0/0/0/0/0`。

## I06 additive reseal

使用独立构造的 owner/receiver receipt/truth cases，不调用测试 helper：

```text
I06_MATRIX cases=34 accept=5 reject=29 mismatch=0 static_assertions=7
CHANNEL_BOUNDARY=PASS
I06_EXIT=0
I06_STDOUT_SHA256=f09115eb95bc48d1d9dd263524fb9ad4aaea93c2b13bb776418245197d3bdc19
```

覆盖 frozen owner 合法/伪造、plain closed-world receipt 合法、opaque/generic/cyclic/non-string-key/truth-alias receipt 非法、TruthView 合法及 shape/finite/finalization 非法变体。

## Final reseal / protection

| Artifact | SHA256 |
|---|---|
| owner | `ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535` |
| `contract.py` | `0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94` |
| `test_d0_contract_views.py` | `745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6` |
| `schemas.py` | `a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401` |
| `test_d0_schemas_statistics.py` | `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9` |
| `channel.py` | `af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6` |
| `test_d0_waveform_channel.py` | `f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1` |
| `test_d0_receiver_codec_methods.py` | `4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348` |
| R001 / decisions / verifications | `ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd` / `ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7` / `848ea9e3e97e6937ceb1dbcecf98350b09cfea135447d35f4815a607dfd785ea` |
| step153 / step154 | `39ded7d15e32bd43e625782b143406e45e8390ef451279d1c05ed239491b8443` / `0a33ec8011faf929a56956cc6d13b6e9f77f02fc6281f2bd81a923c08a850a7a` |

- P05：`7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11` / `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b` / `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d` / `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`，全部 MATCH。
- relevant cache census：1 个既存 `__pycache__` 目录、11 个 `.pyc`；全仓 tracked pycache status 仍为既存 10 项，测试使用 no-bytecode，未新增漂移。
- `git diff --check` exit `0`；staged files=`0`。

## Counts / severity

- independent oracle assertions=`430`；I06 cases/static checks=`34+7`；fresh mutations=`31`；pytest nodes=`52`（其中 exact=`4`）。
- `P0/P1/P2=0/0/0`。

## Terminal

`OWNER_IDENTITY_TYPED_LOADER_INDEPENDENTLY_VERIFIED`
