# T089 Ch4 canonical formal raw 独立验收

> 日期：2026-08-30  
> 范围：canonical formal raw 的结构、provenance、pairing、truth firewall 与冻结绑定  
> 审查纪律：未导入 runner，未调用 formal 或 reducer entry，未生成 aggregate/receipt，未计算或报告 BER、crossing、bootstrap 或 grade

## 终态

**`CH4_CANONICAL_FORMAL_RAW_READY`**。

问题分级：**P0/P1/P2 = `0/0/3`**。canonical raw 的完整 census、双锁 header、RNG namespace、角色与参数、same-scene/cross-Np pairing、delta-zero identity、hash 字段和 post-run immutable bindings 全部通过独立 raw-only 检查。

本结论只接收 raw artifact；不授权 canonical reduction、grade、作图、正文或第二次 formal 运行。

## Canonical artifact

- 路径：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_raw.json`
- SHA-256：`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`
- 文件大小：`89,419,500` bytes
- schema：`t087.ch4-formal-raw.v1`
- purpose：`canonical_formal_production`
- ID：exact `30000..30127`，共 128 个，顺序正确且无重复
- truth marker：`O1_SEPARATE_TRUTH_ONLY_PATH`

worker log 记录唯一命令 exit=`0`、wall time=`409.5 s`、stdout terminal=`CH4_FORMAL_PRODUCTION_COMPLETE`，没有第二次 formal、smoke 或 reducer 调用。独立 reviewer 未复跑该进程。

## 独立结构复核

完整 census：

| 项目 | 实际值 | 冻结值 |
|---|---:|---:|
| top-level latents | 128 | 128 |
| scene-latents | 384 | 384 |
| actual cells | 15,232 | 15,232 |
| arm rows | 76,160 | 76,160 |
| delta-zero references | 128 | 128 |

每个 latent 均为 `weak/moderate/strong` 三个 scene；scene cell 数精确为 `19/81/19`，合计 119 个 actual cells。每个 actual cell 恰有五行：

| Public role | Runtime arm | Parameter contract |
|---|---|---|
| `B0` | `B0` | `null` |
| `B2_TUNED` | `B2` | frozen scene/Np tau；仅 moderate/Np2=`0.5`，其余=`1.0` |
| `C4_FWD` | `C4` | `null` |
| `B3_PSC` | `B3_PSC` | `1.0` |
| `O1` | `O1_TRUTH_ONLY` | `null` |

全部 76,160 行的 payload-bit denominator 均为 `32,768`，role/runtime/parameter/validity 与冻结合同一致。O1 只存在于独立 truth-only runtime；其余 deployable runtime 均不带 truth 身份。

## RNG、pairing 与 hash 检查

- 384 个 scene-latent 的七个组件 namespace 全部精确匹配 `PCG64 / entropy=20260830 / spawn_key=[84,1,scene_code,latent_id,component_code]`，共核验 2,688 个 namespace。
- 七个 component code 精确覆盖 payload bits、channel Q、GG gain、pilot noise、payload noise、mismatch-left 与 mismatch-right；scene code 精确为 weak/moderate/strong=`0/1/2`。
- 每个 cell 的 latent-hash map 与所属 scene-latent exact 相同，共完成 106,624 个字段一致性检查。
- moderate scene 的每个 latent、每个 SNR 下，Np=`2/4/8/16` 的 payload observation hash exact 相同；共核验 2,432 个 cross-Np pairing groups。
- 每个 scene 内全部 primary cells 的 channel hash exact 相同；不同 Np/SNR 没有偷偷换 channel realization。
- 每个 latent 的 delta-zero reference 精确引用 `moderate_np2_snr25_primary` 的 channel hash与三项 observation hashes，且 reference 不含 rows；128/128 通过。
- 所有 SHA 字段均为合法 lowercase SHA-256，并完成以下逐项扫描：scene latent hashes 2,688 个、cell channel hashes 15,232 个、observation hashes 45,696 个、action hashes 76,160 个。

上述检查只核结构、标识和等同关系；没有汇总任何性能数值。

## 双锁与 post-run immutable bindings

- scientific manifest SHA：`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`
- replacement execution lock SHA：`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`
- HEAD/base：`d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`
- environment：Python `3.11.9`、NumPy `2.4.3`、`Windows-10-10.0.26200-SP0`

raw header 的 scientific manifest、execution lock、authority、base、checkpoint/epoch 与 execution hashes 全部和现场双锁 exact match。下列实际文件在 raw 检查前后均保持冻结 SHA：

| 绑定项 | SHA-256 |
|---|---|
| runner | `ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784` |
| reducer core | `f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327` |
| reducer entry | `da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0` |
| focused tests | `cfdba30dc8ef3f12be43667dc298e325f4cf15f0f6c94a031c599c4e613eb3c1` |
| production core | `c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60` |
| common demapper | `bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10` |
| scaled-unitary | `868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2` |
| params | `0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9` |

## Fresh verification

| 检查 | 结果 |
|---|---|
| focused tests | PASS，`19/19` |
| 5 个 seam 文件隔离 `py_compile` | PASS |
| T089 task-control（CP030/epoch30） | PASS |
| targeted `git diff --check` | PASS |
| raw SHA 在检查前后 | exact 不变 |
| manifest/lock/bound files 在检查前后 | exact 不变 |
| `ch4_formal_checkpoint.json` | 不存在 |
| `ch4_formal_aggregate.json` | 不存在 |
| `ch4_formal_receipt.json` | 不存在 |
| raw/lock `.tmp` | 不存在 |

## P2（保留 3 项）

1. checkpoint 采用 self-digest，而非确定性重建。
2. future aggregate/receipt 使用 sequential replace，崩溃恢复仍有窗口。
3. 缺少直接的数值 bootstrap regression test。

这些是 T087/T088 已登记并延续到未来 reduction/recovery 的限制；本次 successful raw 不消除它们，但它们不构成 raw artifact 的 P0/P1。

## 最终判定

canonical raw 的结构、provenance、truth 与 pairing 合同成立，且 post-run 所有冻结 binding 保持不变，故终态为 `CH4_CANONICAL_FORMAL_RAW_READY`。下一步若获新 checkpoint，只能做 canonical reduction 与独立统计复算；本报告不预判其科学 grade。
