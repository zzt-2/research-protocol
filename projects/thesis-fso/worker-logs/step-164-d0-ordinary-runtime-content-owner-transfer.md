# Step 164 — D0 ordinary runtime-content owner transfer

> 2026-08-10 | T118 | `IN PROGRESS`

## Strict RED（owner尚未修改）

独立只读oracle检查payload/store/provenance/output variants/sidecars/write anchor/group-source/count/golden/obligation矩阵：`43`项真实缺失，满足`>=32`。

```text
verdict=RED missing_count=43
RED_EXIT_CODE=23
RED_STDOUT_SHA256=08cd85099d1f7a31fe0097d14ce4ebbf6e6a6d68ce3bd30c300e4800206daedd
```

## Owner patch

只在现有 identity_binding_contract 内新增：

- decoder hard-output payload/store、七类consumer-output、ordinary provenance/store exact schema；
- S2/BPS/B2/S4 group/order/source、aggregate ledger、sidecar、write-anchor与静态计数；
- 10个concrete-input golden及literal roots；
- required/reject mutation obligations。

第一次原子patch因patch行前缀构造错误被工具整体拒绝，owner保持pre-SHA。第二次原子patch写入后，strict parser暴露4个父key少一个空格；仅修复这4处缩进后进入语义oracle，之后未再修改owner。

## Canonical roots

### Decoder hard output

| golden | root |
|---|---|
| zero 16384-bit payload | 1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960 |
| first-bit-only 16384-bit payload | 9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e |

两者均保存完整2732字符RFC4648 base64 literal；解析后为2048 bytes、恰一个等号，round-trip exact。

### Ordinary provenance

| golden | root |
|---|---|
| S2-off 9→1 | e8ca16c947e87e35313907beb207fb1d0f913955f60279dff24b07c505f0ee06 |
| S2-on singleton | ee5f608c2a166fa2859c1db4badd4262376de7080d27c54e0eea37f8ce83e71a |
| S3 singleton | 8caf721a1f822b2beccab3e44c060a1c076fa1be05c47dc49e72af5ec388e61d |
| BPS M2 source | bb50e568db252417ec5542136f5ea8280edd816dee2c065e3c49d32228460145 |
| BPS M3 cache | 580d6d10ced5455e48945c57c109e2345e3281678943b55c514fa8d8fd4670bd |
| B2 clean | 5ab4e4d9b4dd7e249a8eb6ee6a2608de1e76d7dff1ef36cb74df11c81c3cba18 |
| B2 controlled target→sentinel | 25966bd9ae311efd0b7c22aa90965f7b9833877c92da7dfccda075282d7dc553 |
| S4 singleton | cbe018c55b8d850546ae7ac5e2ff239dabacff168c2f134404db956daa1dccc5 |

S4 output明确包含 evidence_sha256=69b9dd696310d530323e4e23dc50c4f98663f3f0c8cbc490e795717f8ed164f7；B2-controlled order为 TARGET_INCLUDED,SENTINEL_EXCLUDED。

## Static counts

manifests/ledger=27487，entries=42967，EXECUTED=30247，CACHE_READ=12720；cache edges=480+1440+10800；groups=12427 singleton + 60×9 + 15000×2；aggregate ledger=26767 EXECUTED + 720 CACHE_READ；ordinary+HMM总ledger=50287。

## Author oracle

### Baseline

strict duplicate-key YAML parse通过；13个identity key及顺序exact；旧122+6 literals、3 grid roots、旧10 goldens、6个HMM counts通过；新增10 goldens存在；scientific/domain projection保持。

    OWNER_SHA256=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
    IDENTITY_SHA256=08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e
    SCIENTIFIC_PROJECTION_SHA256=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
    ORDINARY_DOMAIN_SHA256=15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69

### Fresh mutation gate

39/40 isolated mutations fail closed；decoder_hard_output.version mutation被fresh oracle错误接受。原因是本次inline oracle遗漏该version exact断言；owner本身已有version literal和既有 all_payload_domain_versions_and_field_orders_exact obligation，但author gate要求wrong-accept为0，不能把oracle缺陷包装成PASS。

    AUTHOR_ORACLE_EXIT=1
    MUTATIONS_REJECTED=39/40
    WRONG_ACCEPT=1
    WRONG_ACCEPT_PATH=payload_schemas.decoder_hard_output.version

按时间盒与“失败后不做第二轮owner修复”要求，未修改owner继续追绿，也未重跑美化结果。

## Protection

- contract.py=cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a
- schemas.py=1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20
- step-163=1e0c25214e4fb2d69862dfb5da858492c788831430de01def21ec994779a31fa
- HEAD=715a65884b988ee737f21982f3bbf372860a1da8；staging entries=0
- P05四日志SHA保持7843b048... / 735e4650... / c76887c... / 95a1d184...
- 未运行pytest、benchmark、science、MVE；未install/stage/commit/push

## Terminal

FAIL / P0/P1/P2=0/1/0

未达到 D0_ORDINARY_RUNTIME_CONTENT_OWNER_READY_FOR_INDEPENDENT_VERIFICATION；阻塞项仅为author oracle的1个wrong-accept，不能宣称owner transfer已通过。
