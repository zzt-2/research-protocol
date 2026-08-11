# Step 081 — C1 OFC 2017 slip-state candidate fulltext adjudication

> 2026-08-10 | T035 / CP009 / Groundwork Step 3.5 | `FULLTEXT_READ_NO_EXACT`

## 1. Control、scope 与 acquisition

- Fresh task-control validator：`PASS`；binding=`epoch 9 / CP009 / FULLTEXT_READ`。
- 只处理 DOI `10.1364/OFC.2017.W2A.56`；未扩搜、未改中央 owner/治理/代码、未实验、未提交/push。
- Channel 1：`tools/download --doi` -> `all_failed`，规范化目录为 `papers/doi/10.1364_ofc.2017.w2a.56/`。
- Channel 2：`tools/blit` 精确题名 + IEEE -> document `7937400`，PDF 879,835 bytes，成功后停止；未启用第三通道。
- Identity：download meta `title_overlap=1.0`；`pdfinfo` title/venue一致。PDF 3页，逐页 3/3 目视 QA 通过。
- `tools/convert --quality fast`：137行 / 14,758 bytes；PDF SHA=`B5602E048B5197394CA6A63E4762E7DF8996508AFAD4934F009C4F9B7CDA2178`，正文 SHA=`190F9884CB626190F0850D4A38CBBA27EBC7B4C5E6081BDA1CB9AC883C69B403`。

## 2. 全文事实（10 条）

1. 输入是 blind fourth-power CPE 后的 QPSK symbols、known pilots、demodulator LLR，以及统计 `p_s/sigma_e^2`；不是 actual slip truth。
2. “soft decision” 是 pilot observation 对 4 个 QPSK slip states 的软概率；正文明确 no decision feedback / no sequential update，因此不是 FEC decoder extrinsic。
3. residual phase 先经 moment-matched LLR scaling；slip states 再以 4-state Markov transition `T[q]` 建模，`q=1-sqrt(1-p_s)`。
4. 最近 `M` 个 pilots 的 state probability 经 `T^m` 传播到每个 data symbol，并行修改其 bit LLR。
5. localization 是 per-symbol soft state occupancy；不输出 onset/boundary、持续 range、affected suffix 或 transition direction。
6. action 是 4-state likelihood/LLR marginalization；不旋转 samples、不重映射局部 segment/suffix、不选择 decoder-ranked carrier candidate。
7. FEC decoder只在下游消费一次 modified LLR；论文没有 decoder feedback、selective restart/redecode 或 decode-call账本。
8. 主设置为 `L=31, M=2, N=100`，另用 `M=3` 扫 `N={10,20,100,200}`；只称 fully parallel，未给 op/memory/absolute latency。
9. 无 event trigger、clean abstention/no-op、failure-conditioned fallback 或 false-trigger/failure ledger；hard-decision recovery只是 comparator。
10. 结果仅为 AWGN + Wiener phase-noise GMI：`sigma_p^2=10^-3` 时约0.5–0.8 dB gain，soft vs hard约0.3–0.6 dB；不是 coded FER 或 FSO验证。

## 3. 八字段签名

| field | fulltext verdict |
|---|---|
| input | CPE-output symbols + known pilots + demodulator LLR + `p_s/sigma_e^2`；无 decoder extrinsic/truth |
| trigger | periodic-pilot always-on refinement；无 anomaly trigger |
| localization | 每个 data symbol 的4-state soft probability；无 explicit boundary/range |
| candidate action | 4-state LLR marginalization；无 local sample rotation/remap/reprocess |
| decoder interaction | one-way modified LLR -> downstream FEC；无 feedback/redecode |
| fallback | `NOT_STATED` |
| budget | parallel；`M=2/3`、`N=10/20/100/200`、`L=31`；无 op/latency/decode-call数字 |
| output | refined bit LLR / GMI；无 boundary、corrected samples或local-repair outcome |

## 4. Collision 与 lineage

- PAPU：同为 pilot-aided、receiver-only B2 邻近；PAPU做 unwrap/interpolation/sample correction，本论文做 Markov soft-state LLR refinement。
- CSSC/CS-DC：仍为 `UNRESOLVED_FULLTEXT`；本论文不能替它们补算法/参数或替其裁碰撞。
- OFC 2014：本文显式引用；2014 是 Markov trellis + LDPC feedback whole-codeword turbo，本文是 no-feedback pilot-parallel LLR modifier。
- OFC 2015 HTDD/SC-LDPC/arXiv1704：differential/LDPC graph-tolerance家族；本文无 differential decoder、LDPC loop或graph window。

`collision = STRONG_NEIGHBOR`：本文占用 `pilots -> soft slip-state -> parallel LLR refinement`，但缺 decoder evidence、event trigger、explicit boundary、bounded local carrier action、selective re-decode、clean/fallback 和量化 local cost，故不是 `EXACT_COMPLETE_CHAIN`。

## 5. Claim ceiling 与 round-3 debt disposition

- 可声称：OFC 2017 已给出无 decoder feedback 的 pilot soft-state、fully-parallel LLR mitigation；它应作为 B2-relevant prior art/cheap alternative 处置。
- 不可声称：它定位并输出 slip boundary、局部旋转/修复 samples、调用 decoder重评候选，或已吸收 Q1完整链。
- Round-3 candidate fulltext debt：`CLOSED_NO_EXACT`；acquisition debt=`NONE`；不再保留该篇的 unresolved blocker。
- Step 4a / defect / method contribution：`NOT_ADJUDICATED`。

## 6. Protection terminal（写入后 fresh recheck）

- p05 frozen SHA256：fresh `4/4 MATCH`（`p05_run.log`=`7843B048...F11`；`p05_run2.log`=`735E4650...38B`；`p05_run3.log`=`C76887C6...34D`；`p05_run4.log`=`95A1D184...1DE`）。
- Git staging：fresh `EMPTY`（`STAGED_COUNT=0`）。

`FULLTEXT_READ_NO_EXACT`
