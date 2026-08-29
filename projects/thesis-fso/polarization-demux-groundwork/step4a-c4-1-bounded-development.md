# C4-1 scaled-unitary pilot-LS 有界开发

> 2026-08-30 | T069 / D049 / T068 / V023 | CP011 / epoch 11
> 结论上限：PROVISIONAL；本报告不是 source reproduction、fresh confirmation 或最终论文结论。

## 1. 事实与审计边界

- task-control validator：`PASS`；base=`9a31d5d73e87c37417840a66767a20d8df0f8e36`，epoch=`11`，checkpoint=`CP011`。
- 独立 seam：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls/`；未改 `common/`、`params.py`、Ch3/Ch5、Skill/controller 或论文正文。
- RED：核心 C0–C5 在实现文件缺失时 `6 failed`；GREEN：实现后 `6 passed`。最终 seam 测试为 `13 passed`。
- C0–C5 receipt：六门全部 `PASS`，correctness 局部修复轮数 `0`；因此才运行 BER。
- 首次 BER runner 在生成任何 window/raw 前因既有 `common` 包的顶层 `params` 导入路径失败；增加独立脚本上下文 RED 测试后，只补 `SIM_ROOT` 路径，最终 `13/13` 通过。冻结参数与测试设计未改变。
- raw-only reducer 检查 manifest hash、正确性前提、四 cell/种子/split、paired realization hash、arm/参数网格、tune/evaluation 隔离、finiteness 与 truth firewall，全部 `PASS`。

## 2. 冻结实现与开发设计

候选严格实现

\[
\hat H_{LS}=Y_pX_p^H(X_pX_p^H)^{-1}=U\operatorname{diag}(s_1,s_2)V^H,
\quad \hat g=(s_1+s_2)/2,
\]

\[
P(\hat H_{LS})=\hat gUV^H,
\qquad W=VU^H/\hat g.
\]

`rho=s1/s2` 只记录诊断，不触发 guard。C0–C5 分别验证无噪 exact recovery、balanced direct/post-LS 等价、双酉与复尺度恒等式、paired PDL 理论、truth firewall，以及 exact-zero/rank-deficient/NaN/Inf fail-closed；near-zero 非零输入没有另设阈值。

开发轴在结果前冻结为 `SNR={14,18} dB × Np={2,4}`，每格 64 windows，其中前 32 tune、后 32 evaluation；每 window 每偏振 4096 个 `(8,8)-16APSK` payload symbols。四格 seed base 依次为 6000、6100、6200、6300。所有 arms 共享同一 window 的 `Q/g/noise/pilots/payload`。

## 3. Tune-only 选择

| cell | B1 normalized-ridge `eta` | B2 SV-floor `tau` | evaluation 最强 B1/B2 |
|---|---:|---:|---|
| 14 dB, Np=2 | 0.01 | 1.0 | B2 |
| 14 dB, Np=4 | 0.001 | 1.0 | B2 |
| 18 dB, Np=2 | 0.001 | 1.0 | B2 |
| 18 dB, Np=4 | 0.01 | 1.0 | B2 |

选择只使用 tune payload BER；精确并列选更强 regularization。evaluation 没有参与调参。

## 4. Evaluation 结果

每个 arm/cell 的 BER 分母均为 `1,048,576` bits（32 evaluation windows）。NMSE 是 window 均值。

| cell | arm | BER | bit errors | mean channel NMSE | mean inverse residual |
|---|---|---:|---:|---:|---:|
| 14 dB, Np=2 | B0 | 0.1066360474 | 111816 | 0.11387841 | 0.15938969 |
|  | B1 | 0.1066913605 | 111874 | 0.11228928 | 0.16287131 |
|  | B2 | 0.0998287201 | 104678 | 0.12928955 | 0.09251792 |
|  | C4 | 0.0944595337 | 99048 | 0.07942523 | 0.09410115 |
|  | O1 | 0.0652208328 | 68389 | 0 | 0 |
| 14 dB, Np=4 | B0 | 0.0763111115 | 80018 | 0.04531257 | 0.03930940 |
|  | B1 | 0.0763292313 | 80037 | 0.04518873 | 0.03934767 |
|  | B2 | 0.0713415146 | 74807 | 0.05879940 | 0.03580306 |
|  | C4 | 0.0693206787 | 72688 | 0.03140878 | 0.02583193 |
|  | O1 | 0.0585327148 | 61376 | 0 | 0 |
| 18 dB, Np=2 | B0 | 0.0689544678 | 72304 | 0.13148411 | 0.18152671 |
|  | B1 | 0.0689573288 | 72307 | 0.13125451 | 0.18191307 |
|  | B2 | 0.0600614548 | 62979 | 0.17334650 | 0.06575734 |
|  | C4 | 0.0572195053 | 59999 | 0.08157085 | 0.06315162 |
|  | O1 | 0.0431299210 | 45225 | 0 | 0 |
| 18 dB, Np=4 | B0 | 0.0349607468 | 36659 | 0.02237518 | 0.03009650 |
|  | B1 | 0.0351352692 | 36842 | 0.02234993 | 0.03120399 |
|  | B2 | 0.0282335281 | 29605 | 0.01948761 | 0.01623512 |
|  | C4 | 0.0284452438 | 29827 | 0.01315503 | 0.01405671 |
|  | O1 | 0.0214834213 | 22527 | 0 | 0 |

### Paired window bootstrap 95% CI

差值方向均为 candidate BER minus baseline BER，负值更好；PCG64 seed=`2026083003`，2000 resamples，cluster=`evaluation window`。

| cell | comparison | mean diff | 95% CI |
|---|---|---:|---:|
| 14 dB, Np=2 | C4 − strongest(B2) | -0.0053691864 | [-0.0106374741, -0.0004005194] |
| 14 dB, Np=4 | C4 − strongest(B2) | -0.0020208359 | [-0.0038831949, -0.0003260136] |
| 18 dB, Np=2 | C4 − strongest(B2) | -0.0028419495 | [-0.0063127518, -0.0000006914] |
| 18 dB, Np=4 | C4 − strongest(B2) | +0.0002117157 | [-0.0007823706, +0.0011769772] |
| 14 dB, Np=2 | B2 − B0 | -0.0068073273 | [-0.0125336885, -0.0015764236] |
| 14 dB, Np=4 | B2 − B0 | -0.0049695969 | [-0.0088287830, -0.0020188093] |
| 18 dB, Np=2 | B2 − B0 | -0.0088930130 | [-0.0183649540, -0.0013474703] |
| 18 dB, Np=4 | B2 − B0 | -0.0067272186 | [-0.0118503809, -0.0029294491] |

四格 O1 BER 均低于最强 deployable BER；对应最强 deployable 的绝对 oracle headroom 为 0.02923870、0.01078796、0.01408958、0.00675011/0.00696182 量级，故不是“oracle 无 headroom”。C4 的 mean `rho` 依次为 1.4361、1.2240、1.4155、1.1880。

## 5. 终点判定

```text
terminal = C4_STRUCTURED_SIGNAL
grade = PROVISIONAL_A
winner = C4
only_next_step = fresh confirmation of frozen C4 recipe
```

判据事实：C4 相对每格 strongest(B1,B2) 在两个 `Np=2` cell 的 CI upper 都 `<0`；两个 `Np=4` cell 中一格显著改善，另一格 CI 跨 0 且 lower `<0`，没有显著回归。四格均有限且 correctness/hash/split/firewall 检查通过。

不得隐藏的 comparator 事实：B2（四格都选 `tau=1`）相对 B0 在四格的 BER CI 都闭合为改善。因此本次证据同时说明 cheap SV-floor comparator 真实有效；只是预注册 terminal ladder 先检查且满足了 C4 对 strongest(B1,B2) 的门，故 provisional winner 仍是 C4，而不是把 B2 的结果删除或改写成无效。

## 6. 限制与未满足项

- `18 dB,Np=2` 的 C4 CI upper 仅为 `-6.91e-7`，虽按冻结严格不等式通过，但边界很窄，必须由 fresh confirmation 检验稳定性。
- 每格 bootstrap 独立 cluster 只有 32 个 evaluation windows；大量 payload bits 不替代独立 window 数。
- 未运行 fresh confirmation、LDPC/FER、额外 SNR/pilot、时变 SOP、PDL/PMD/FIR/IQ、CFO/CPR 或其他损伤；这些不属于 T069。
- 本结果不构成最终方法、最终章节声称或 source reproduction。

## 7. 证据指针

- manifest：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls/development_manifest.json`
- correctness：`correctness_receipt.json`，manifest SHA256=`ad8361f7624a6fed66b8954bcba92efcbdd4dfff1f844746bd2d70feb33ea2b2`
- raw：`development_raw.json`，SHA256=`cee1a881c26e20d90f1412cb886d8b67300dcf1e22d7d98bc6c59c6189f8bf0b`
- aggregate：`development_aggregate.json`，SHA256=`9c236830edc29c96edbe6698a048c910c4d6775486bc51ec2d82b460a2cc2ccb`
- reducer receipt：`development_receipt.json`
