# Ch4 production-seam bridge independent raw verification

> 2026-08-30 | T085 / D064 / V039 / CP026 | raw-only science recomputation

## Verdict

- Artifact P0/P1/P2=`0/0/0`。
- Science terminal=`CHEAP_COMPARATOR_NOT_CLEARED`。
- Generator binding=`PARTIAL`：raw 对 scientific population、manifest、核心算法代码和 base commit 的绑定闭合，但 raw 本身不绑定 runner/reducer/tests，不能单独证明生成调用链；该边界不改变本次从 raw 复算出的科学 terminal。

C4 在四格及 pooled Np2 上均显著优于 B2；但 pooled Np2 的 `C4−B3_PSC` 95% CI 跨零，因此没有通过预注册的廉价替代门。按 T085，Task5/full production 必须停止，不能调参、扩样或换 cell。

## Independent method

本验证没有导入或调用 T085 runner/reducer，也没有运行仿真。独立内联脚本只解析：

- `corrected_anchor_manifest.json`；
- `corrected_anchor_raw.json`；
- manifest 绑定的核心代码字节与只读 AST。

统计按 T085 冻结合同重建：每个 named comparison 重新初始化 PCG64 seed=`2026083006`，bootstrap=`5000`，window/latent 为 paired unit。逐 cell 使用 64 个 latent；pooled Np2 使用 64 个 cluster，每个 cluster 同时携带该 latent 的 14 dB 与 18 dB 两行，没有把 128 行当独立样本。

## Population, pairing and hashes

- canonical latent IDs：`20000..20063`，exact `64/64`；
- cells：`14/18 dB × Np=2/4`，exact `4/4`；
- arms：`B0/B2/B3_PSC/C4/O1`，总计 `64×4×5=1280` rows；
- 七路 namespace：`448/448` metadata identity PASS；每个 component 的 64 个 latent hashes 均唯一；
- same-SNR Np2/Np4 payload observation pairing：`128/128` PASS；
- O1 Np2/Np4 metrics 与 action hash：`128/128` bit-exact PASS；
- 所有 BER 均从 total `bit_errors/payload_bits` 独立复算；每 cell bits=`2097152`，pooled Np2 bits=`4194304`。

Hashes：

| object | SHA-256 / identity |
|---|---|
| manifest | `d3ed6c7d887a7127850e310e2a6887eed5c99ec957f1a4b577282e1fbc518fde` |
| raw | `4ef32e16d4ce252634686e8e3dc6e0f94dbff4daad18ef12691b491c875e33ed` |
| base commit | `5ec190ad8c8da14b5dba3b353bd23977b7429d8a`，等于验证时 HEAD |
| `production_core.py` | manifest/raw/current bytes 三方一致 |
| `common/_modulation.py` | manifest/raw/current bytes 三方一致 |
| `scaled_unitary.py` | manifest/raw/current bytes 三方一致 |

## Frozen-gate recomputation

`D=BER_C4−BER_comparator`；CI 为 paired 2.5%/97.5% quantiles。

### C4 versus B2

| cell | C4 errors / BER | B2 errors / BER | mean D | 95% CI | C4 window wins |
|---|---:|---:|---:|---:|---:|
| 14 dB / Np2 | 192106 / 0.0916032791 | 208143 / 0.0992503166 | -0.0076470375 | [-0.0109622836, -0.0044870377] | 45/64 |
| 14 dB / Np4 | 164829 / 0.0785965919 | 171860 / 0.0819492340 | -0.0033526421 | [-0.0051222205, -0.0017430782] | 45/64 |
| 18 dB / Np2 | 81910 / 0.0390577316 | 89302 / 0.0425825119 | -0.0035247803 | [-0.0061722159, -0.0012578368] | 36/64 |
| 18 dB / Np4 | 67580 / 0.0322246552 | 71221 / 0.0339608192 | -0.0017361641 | [-0.0030212879, -0.0006335735] | 30/64 |
| pooled Np2 | 274016 / 0.0653305054 | 297445 / 0.0709164143 | -0.0055859089 | [-0.0083591759, -0.0030578673] | 46/64 clusters |

### C4 versus B3_PSC

| cell | C4 errors / BER | B3 errors / BER | mean D | 95% CI | C4 window wins |
|---|---:|---:|---:|---:|---:|
| 14 dB / Np2 | 192106 / 0.0916032791 | 192425 / 0.0917553902 | -0.0001521111 | [-0.0009999871, +0.0007058024] | 28/64 |
| 14 dB / Np4 | 164829 / 0.0785965919 | 167614 / 0.0799245834 | -0.0013279915 | [-0.0025754333, -0.0000490785] | 36/64 |
| 18 dB / Np2 | 81910 / 0.0390577316 | 82117 / 0.0391564369 | -0.0000987053 | [-0.0006623507, +0.0004301071] | 19/64 |
| 18 dB / Np4 | 67580 / 0.0322246552 | 68617 / 0.0327191353 | -0.0004944801 | [-0.0011544347, +0.0002294064] | 21/64 |
| pooled Np2 | 274016 / 0.0653305054 | 274542 / 0.0654559135 | -0.0001254082 | [-0.0008006513, +0.0005495608] | 29/64 clusters |

Gate decomposition：

- pooled Np2 C4−B2 CI upper=`-0.0030578673 < 0`：PASS；
- pooled Np2 C4−B3 CI upper=`+0.0005495608 < 0`：FAIL；
- 两个 Np4 cell 相对 B2/B3 的 CI lower 全部 `<=0`：PASS；
- measurement/schema/hash/pairing/raw arithmetic：PASS。

唯一合法 science terminal 因此是 `CHEAP_COMPARATOR_NOT_CLEARED`。

## Exploratory B3 evidence — explicitly non-thesis and non-gate

下列比较不属于 T085 gate，是为后续战略讨论附加的探索性 raw 复算。A2 明确是 non-thesis stop-gate，这些数字不能直接写入论文、不能自动授权 Task5，也不能把 B3 宣布为已成立论文方法。

### B3_PSC versus B2

| cell | B3 errors / BER | B2 errors / BER | mean D | 95% CI | B3 window wins |
|---|---:|---:|---:|---:|---:|
| 14 dB / Np2 | 192425 / 0.0917553902 | 208143 / 0.0992503166 | -0.0074949265 | [-0.0101556778, -0.0049345613] | 48/64 |
| 14 dB / Np4 | 167614 / 0.0799245834 | 171860 / 0.0819492340 | -0.0020246506 | [-0.0032172441, -0.0009202600] | 46/64 |
| 18 dB / Np2 | 82117 / 0.0391564369 | 89302 / 0.0425825119 | -0.0034260750 | [-0.0055900216, -0.0015519977] | 37/64 |
| 18 dB / Np4 | 68617 / 0.0327191353 | 71221 / 0.0339608192 | -0.0012416840 | [-0.0020642996, -0.0005750060] | 31/64 |
| pooled Np2 | 274542 / 0.0654559135 | 297445 / 0.0709164143 | -0.0054605007 | [-0.0076873302, -0.0034259140] | 47/64 clusters |

### B3_PSC versus B0

| cell | B3 errors / BER | B0 errors / BER | mean D | 95% CI | B3 window wins |
|---|---:|---:|---:|---:|---:|
| 14 dB / Np2 | 192425 / 0.0917553902 | 221581 / 0.1056580544 | -0.0139026642 | [-0.0173446059, -0.0106510639] | 62/64 |
| 14 dB / Np4 | 167614 / 0.0799245834 | 180147 / 0.0859007835 | -0.0059762001 | [-0.0081315279, -0.0038971066] | 54/64 |
| 18 dB / Np2 | 82117 / 0.0391564369 | 98797 / 0.0471100807 | -0.0079536438 | [-0.0103709459, -0.0057535172] | 63/64 |
| 18 dB / Np4 | 68617 / 0.0327191353 | 75180 / 0.0358486176 | -0.0031294823 | [-0.0044895053, -0.0019721031] | 57/64 |
| pooled Np2 | 274542 / 0.0654559135 | 320378 / 0.0763840675 | -0.0109281540 | [-0.0137181580, -0.0082797766] | 62/64 clusters |

四格中 B3−B2 与 B3−B0 的 CI upper 均 `<0`。这构成强烈的“B3 可进入升格讨论”信号：它是 receiver-visible、同导频预算的完整 action，并在当前 A2 population 中稳定改善 B0/B2。但当前证据等级仍是 `PROMOTION_SIGNAL_ONLY / NON_THESIS`；若要升格，必须显式返回方法身份与证据合同讨论，不能把 T085 的 stop failure 改写成自动换主角。

## Truth-firewall evidence boundary

Raw 可直接观察和交叉验证的证据：

1. `truth_firewall=O1_SEPARATE_TRUTH_ONLY_PATH`；
2. manifest 将 B0/B2/B3/C4 标为 receiver-visible，将 O1 标为 truth-only runner path；
3. raw 绑定的 `production_core.py` 经 AST 检查，deployable `receiver_action` 恰有五个参数 `(arm,x_pilots,y_pilots,y_payload,parameter)`，函数源码不含 `h_true/bits/decision/truth`；
4. O1 在同 SNR 的 Np2/Np4 上 metrics 与 action hash bit-exact，而 deployable rows 保持独立 action hashes。

证据上限：raw marker 和 manifest access label 是结构声明，raw 本身不能证明 runner 在运行时从未绕过 API，也不能证明 O1 是如何构造的；由于 raw 没有绑定 runner 字节，generator binding 只能记 `PARTIAL`。完整 truth-firewall closure 需要结合 T084 core review，以及 T085 receipt 对 runner/tests/hash 的独立验证。这里不把结构证据夸大成 raw-only 的完整调用链证明。

## Scope

本验证只新增本报告文件。未修改治理、实现、测试或 artifacts；未运行仿真，未 commit/push。
