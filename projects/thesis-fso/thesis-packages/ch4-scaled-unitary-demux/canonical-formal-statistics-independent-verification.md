# T091 Ch4 canonical formal statistics 独立终验

> 日期：2026-08-30  
> 范围：canonical aggregate/receipt、raw-only 统计复算、冻结 grade 与终态绑定  
> 审查纪律：未导入或运行 runner、`ch4_formal_reducer.py`、canonical entry；未调用 canonical 命令；全部统计直接从 immutable raw counts 独立计算

## 终态

**`CH4_CANONICAL_FORMAL_STATISTICS_READY`**。

问题分级：**P0/P1/P2 = `0/0/3`**。独立程序从 raw 重算 570 个 pooled Jeffreys BER、4 个 whole-curve headline comparisons、76 个 paired cell comparisons、A/B/C/F grade 及四类 descriptive summaries；与 canonical aggregate/receipt 的 757 个结构和数值节点逐项一致，最大绝对数值差为 **`0.0`**。

冻结结果为 **grade `A`，chapter gate=`true`**。C4_FWD 自身在 moderate Np2 和 Np4 均满足相对 B2_TUNED 的 required-SNR gain CI lower `>0`，无需借 B3_PSC 才获得 A。

## Publication 与 artifact 身份

worker log 记录 T091 corrected invocation 只运行一次：exit=`0`、wall time=`5.0 s`、stdout terminal=`CH4_FORMAL_REDUCTION_ACCEPTED`、grade=`A`；没有第三次 publication、formal 或 smoke 调用。

| Artifact | SHA-256 | Size |
|---|---|---:|
| canonical raw | `642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b` | 89,419,500 bytes |
| scientific manifest | `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079` | 7,737 bytes |
| execution lock | `095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987` | 1,674 bytes |
| canonical aggregate | `916c4ba5f75703a5a63bc40931e74d161ad3e61ac0b72baa918b77de95c55602` | 22,404 bytes |
| canonical receipt | `0fac1304f9aa8a4a4463c14ed5a43059a04b5c1de031b69c1d7fa9f03376e697` | 1,364 bytes |

Receipt 中 raw、manifest、lock 与 aggregate 的四项 artifact hash 均与现场 bytes exact；aggregate terminal=`CH4_FORMAL_REDUCTION_COMPLETE`，receipt terminal=`CH4_FORMAL_REDUCTION_ACCEPTED`。两份 `_meta` 的 script、`common_md5=49acdfa4`、`git_commit=d3d98c6`、ISO timestamp 八个字段全部通过，timestamp 同为 `2026-08-30T17:14:20`。

## 独立 raw-only 统计方法

独立程序只使用 Python 标准库与 NumPy，先完整读取 raw 并生成自己的 counts，再在计算完成后加载 aggregate/receipt 作被动比对：

1. 对 exact IDs `30000..30127`，按 `(scene,Np,SNR,role)` 汇总整数 bit errors 和 payload bits；每组 BER 使用 `(errors+0.5)/(bits+1)` Jeffreys 口径。
2. 570 个 pooled groups 覆盖 weak/Np2、moderate/Np2/4/8/16、strong/Np2 的 19 个 SNR 与 5 个固定角色。完整 canonical serialization digest 为 `16084bbdac62e4df725fc8d7c05f1aa172347924b4fd773be033eed20b700119`。
3. required-SNR 严格按冻结的 log10(BER) 线性插值和 crossing 状态机计算。
4. 每个 named whole-curve comparison 都重新初始化 PCG64 seed=`2026083007`，5000 次抽样；每个 sampled latent 携带完整 19-SNR slice，不跨 scene pooling。
5. 每个 `(moderate,Np,SNR,variant)` cell comparison 都重新初始化 PCG64 seed=`2026083008`，5000 次抽取 128 个 paired latent clusters。
6. grade 只检查 C4_FWD/B3_PSC 相对 B2_TUNED 的 moderate Np2/Np4；C4-vs-B3 不参与 admission gate。

raw census 独立复核为 `128/384/15232/76160/ref128`，所有 primary denominators 为 32,768 bits。delta-zero 仍是无 rows 的 exact reference；O1 保持 truth-only 身份，不进入 deployable baseline 解释。

## Headline 正式结果

工程参考 BER 为 uncoded pre-FEC `3.8e-3`。四项 crossing 均为 `STABLE`，whole-curve bootstrap 有效重复数均为 `5000/5000`。

| Variant vs B2_TUNED | Np | B2 required SNR | Variant required SNR | Gain | 95% CI |
|---|---:|---:|---:|---:|---:|
| C4_FWD | 2 | 24.963859 dB | 24.093385 dB | **0.870474 dB** | **[0.618162, 1.088274] dB** |
| C4_FWD | 4 | 23.710083 dB | 23.589133 dB | **0.120949 dB** | **[0.018893, 0.239227] dB** |
| B3_PSC | 2 | 24.963859 dB | 24.089128 dB | **0.874731 dB** | **[0.628859, 1.078428] dB** |
| B3_PSC | 4 | 23.710083 dB | 23.602049 dB | **0.108033 dB** | **[0.025752, 0.202565] dB** |

因此两项预命名 variant 均各自满足 A：在 moderate Np2 和 Np4 上相对 tuned B2 的 CI lower 都严格大于 0。76 个 cell-level comparisons 也全部复算；CI upper `<0` 的格数为 C4 Np2/Np4=`15/11`、B3 Np2/Np4=`15/10`，但 grade 已在 A 停止，不能把这些格数另算成额外 grade。

## Raw-derived descriptive summaries

这些数值与 aggregate exact，但混合了不同 SNR、scene、Np 或 mismatch 条件，只作描述，不承担 headline 因果结论。

### Mechanism

| Role | Mean window BER | Rows |
|---|---:|---:|
| B0 | 0.0528791572 | 15,232 |
| B2_TUNED | 0.0509667036 | 15,232 |
| C4_FWD | 0.0497484688 | 15,232 |
| B3_PSC | 0.0508225585 | 15,232 |
| O1 truth-only | 0.0386491643 | 15,232 |

### Scene 与 pilot

| Scene | Mean window BER | Rows |
|---|---:|---:|
| weak | 0.0442698730 | 12,160 |
| moderate | 0.0462560230 | 51,840 |
| strong | 0.0630056105 | 12,160 |

| Np | Mean window BER | Rows |
|---:|---:|---:|
| 2 | 0.0514714172 | 39,680 |
| 4 | 0.0485517627 | 12,160 |
| 8 | 0.0449199651 | 12,160 |
| 16 | 0.0430411238 | 12,160 |

### Mismatch

| Delta | Mean window BER | Rows |
|---:|---:|---:|
| 0.05 | 0.0030743122 | 640 |
| 0.10 | 0.0040411949 | 640 |
| 0.20 | 0.0119376183 | 640 |
| 0.30 | 0.0296833992 | 640 |
| 0.40 | 0.0525204659 | 640 |

delta=0 没有复制 rows，而是 exact reference，因此不应在此 summary 中伪造第六个独立 cell。

## 逐字段一致性

| 检查 | 结果 |
|---|---|
| aggregate/receipt scientific nodes | 757 个节点全部一致 |
| 最大绝对数值差 | `0.0` |
| aggregate/receipt metadata | 8/8 字段通过 |
| paired cell comparisons | 76/76 exact |
| grade / chapter gate | `A` / `true` exact |
| artifact hashes | 5 项现场 hash exact；receipt 内 4 项 binding exact |

## Fresh 终态门禁

| 检查 | 结果 |
|---|---|
| T091 task-control | PASS，CP032/epoch32 |
| focused tests | PASS，`19/19` |
| 五文件隔离 `py_compile` | PASS |
| raw/双锁/execution/dependencies/aggregate/receipt | 13 项 SHA exact |
| HEAD | exact `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d` |
| aggregate/receipt/raw/lock `.tmp` | 4 项均不存在 |

## P2 与 claim ceiling

1. **Np4 增益幅度小**：C4 的点增益为 0.120949 dB，虽 CI lower 仍为正，但文字应称“统计上稳定的小幅优势”，不能包装成大幅工程增益。
2. **强廉价邻居限制独特性**：B3_PSC 同样为 grade A，且四项 headline 中与 C4 极接近。本证据不支持“C4 优于 B3”；它支持的是 direction/scale family 相对 tuned B2 的 bounded chapter claim。
3. **混合 summary 不承重**：mechanism/scene/pilot/mismatch 的 mean-window BER 混合不同条件，不能直接证明 pilot efficiency、scene robustness 或某一方法的 mismatch 因果优势；相应图表必须回到 matched cell/pooled curve 数据。

## 最终判定

canonical publication、provenance、统计与 grade 已由 immutable raw 独立闭合，P0/P1 均为零。因此终态为 **`CH4_CANONICAL_FORMAL_STATISTICS_READY`**，正式接收 grade `A`。本报告只授权按 D070 后续另立 checkpoint；它不自行授权作图、论文正文、补实验、再次 publication 或恢复 Ch5。
