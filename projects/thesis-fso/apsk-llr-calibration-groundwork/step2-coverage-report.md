# C5-0 reliability-aware LLR calibration — GW Step 2 覆盖报告

> 2026-08-30 | base `9a31d5d73e87c37417840a66767a20d8df0f8e36` | epoch `11` | checkpoint `CP011`
> terminal: `STEP2_READY_FOR_STEP3`

## 1. 事实与池算术

- 本轮严格停在 Groundwork Step 2 acquisition；没有实现、仿真、Q#、Step 3 精读结论或论文正文改动。
- 启动时 `papers/index.json` 只有 56 条记录（16 success、40 failed），且没有覆盖 Layton、VTC 等若干已存在全文；`search-archive/_index/all-papers.jsonl` 当时不存在。因此“索引未命中”没有被解释为“没有文献”。
- 本地候选审计 3 篇：Layton 与 VTC 保留，Baldi 因只有 APSK 系统/软比特框图、没有 receiver LLR/demapper 公式而剔除。
- 新取得 4 篇有效 arXiv HTML 全文：`0805.1327`、`1111.7265v1`、`1709.10393`、`1911.01585v3`。
- Layton 的旧 `track/pdf` 端点曾把纯文本误存为 `source.pdf`；本轮以同 DOI 的 Springer 官方 PDF 端点经 `tools/download --force` 重取，得到 12 页 `%PDF-1.4`，再经 `tools/convert --quality standard` 生成 `source.md`。VTC 的 IEEE BLIT 原始物仍是完整全文纯文本而非 PDF，保留明确的 source-format caveat。
- 唯一 qualified fulltext=`3 - 1 + 4 = 6`。A/B/C 计数允许同一篇跨桶，不相加：A=`4`，B=`3`，C=`4`。

## 2. Query / acquisition usage log

检索式达到任务书上限 8 个，不再扩展。所有显式结果保存在 `search-archive/2026-08-30/c5-0-q*.json`。

| # | 检索式 | 源 | 返回 | 审计说明 |
|---|---|---|---:|---|
| Q1 | `mismatched BICM LLR scaling GMI optimal correction` | S2/OpenAlex/arXiv | 0 | S2/OpenAlex 限速；arXiv 0。源故障不等于无文献。 |
| Q2 | `LLR correction mismatched BICM receivers` | SerpAPI | 0 | 无 API key，跳过。 |
| Q3 | `Linear correction of mismatched L-values in BICM receivers` | Exa/Tavily/Firecrawl | 0 | 均无 API key，跳过。 |
| Q4 | `noise variance estimation LLR demodulation` | arXiv | 0 | 无命中。 |
| Q5 | `pilot aided SNR estimation soft demodulation` | OpenAlex | 0 | 同源再次限速后按时限规则截断。 |
| Q6 | `mismatched L-values` | arXiv | 2 | 命中并取得 `1111.7265v1`、`1911.01585v3`。 |
| Q7 | `pilot noise variance estimation demapper` | arXiv | 0 | 无命中。 |
| Q8 | `pilot SNR estimation LLR` | arXiv | 0 | 无命中。 |

在查询预算用尽后只做已知标识精确取得：`1709.10393`、`0805.1327` 成功；APSK scalar Zhang DOI `10.7840/KICS.2013.38C.10.858` 与 simplified APSK demapper DOI `10.1109/TWC.2012.051412.112055` 均未取得全文，不能以摘要入池。

## 3. Qualified fulltext ledger

### QF1 — Martinez et al., *Bit-Interleaved Coded Modulation Revisited: A Mismatched Decoding Perspective*

- identity/source：arXiv `0805.1327`；`papers/arxiv/0805.1327/metadata.json` 为 `success/arxiv_html/good`，正文题名见 `content.md:63`。metadata 的空 title / `unverifiable` 由正文题名与 arXiv ID 补强，不冒充 title-check pass。
- evidence bucket：A；同时提供 correct matched bit-metric baseline。
- executable entry：式(58)–(59)在 `content.md:576-585`，对公共 `s>0` 最大化 mismatched metric 的 GMI；BICM 分解式(61)在 `content.md:600-609`，max-log 特化式(69)在 `content.md:671-684`。
- input → action → output：真实 `(B,Y)` 样本/分布与 mismatched bit metric `q_j` → 一维优化 `q^s`（等价于 log-metric/LLR 乘公共 `s`）→ `s*` 与对应 GMI。
- baseline / cheap：精确 bit metric 式(7)（`content.md:174-183`）是 matched baseline；matched 时 `s=1`（`content.md:662-668`）。cheap alternative 是单一全局 `s*`。
- boundary：memoryless、均匀输入；各 bit 共用一个 `s`；没有 pilot/在线估计，也不保证有限长 decoder 增益。
- truth / metric / relation / Step 3 question：样本化求解需要真实 bits/联合样本（理论形式可直接给分布）；指标为 GMI；与 C5-0 是通用 scalar primitive。Step 3 核对公共 `s` 与逐 bit `s_j` 的 canonical estimator 及有限样本输入契约。

### QF2 — Szczecinski, *Linear Correction of Mismatched L-values in BICM receivers*

- identity/source：arXiv `1111.7265v1`；`metadata.json` 为 `success/arxiv_html/good/title_check=match`，正文题名见 `content.md:59`。
- evidence bucket：A；直接 scalar-calibration 原子。
- executable entry：式(12)在 `content.md:231-245`：
  \[
  \alpha^*=\arg\min_\alpha\;\mathbb E_{\widetilde L\mid C=0}
  \left[\log_2\!\left(1+e^{\alpha\widetilde L}\right)\right],
  \qquad L^{c}=\alpha^*\widetilde L .
  \]
  另有 PEP/CGF 标量规则式(37)（`content.md:519-523`）。
- input → action → output：带真实 bit 标签或条件分布的 mismatched L-value 样本 → 一维优化 `alpha` → calibrated L-values。
- baseline / cheap：B0 是同一 mismatched L-value 产生链、未经额外校准的 `alpha=1`；式(1) matched LLR/真实统计单列为 `B_match/O1` reference。cheap alternative 是一个乘法标量。
- boundary：需标签/条件分布；不是 pilot estimator；未量化 ML 判决对全局正比例不敏感，收益不能无条件外推到所有 decoder。
- truth / metric / relation / Step 3 question：需要 bit 标签或条件 L-value 分布；指标为 GMI/PEP；与 C5-0 是直接 scalar primitive、非 target-scene exact recipe。Step 3 核对式(12)/(37)各自的数据要求、符号约定和适用 decoder。

### QF3 — Alvarado et al., *Achievable Information Rates for Fiber Optics: Applications and Computations*

- identity/source：arXiv `1709.10393`；`metadata.json` 为 `success/arxiv_html/good`，`real_title` 与正文题名 `content.md:69` 一致。
- evidence bucket：A+B+C（coherent-fiber 通用邻居）。
- executable entry：式(34)在 `content.md:768-777`，用按 bit/bit-value 分组的 LLR 样本一维优化 GMI scalar `s`；matched likelihood LLR 见式(23)/(25)，`content.md:622-647`。
- input → action → output：已知发送 symbols/bits 与接收样本 → 先用 `z=y-x` 估噪声方差，再形成 LLR 样本并一维优化 `s`（实验三步法见 `content.md:789-794`）→ noise-aware LLR/GMI-optimal scalar。
- baseline / cheap：使用正确噪声方差的 matched likelihood LLR；cheap alternative 是式(34)的公共 `s`。
- boundary：uniform signaling、memoryless bitwise receiver；非线性有记忆光纤下为可能松的下界；没有规定因果 pilot 窗口，不是 APSK/FSO 直接证据。
- truth / metric / relation / Step 3 question：噪声估计需要 known transmitted symbols，经验 GMI 还需要真实 bits；指标为 AIR/GMI；与 C5-0 是 A/B primitive、C 的 coherent-optical direct context。Step 3 核对 residual 方差估计、`s` 优化和数据复用边界。

### QF4 — Yoshida et al., *Post-FEC BER Benchmarking for BICM with Probabilistic Shaping*

- identity/source：arXiv `1911.01585v3`，DOI `10.1109/JLT.2020.2990620`；有效 arXiv HTML，正文题名见 `content.md:62`。metadata 的 `real_title=[I Introduction]` 是抽取器误取，故 title-check 只记 `unverifiable`。
- evidence bucket：A+B+C（coherent-fiber QAM 邻居）。
- executable entry：式(1)在 `content.md:148-168` 给出 `L_po=L_pr+s L_ex`；仅 SNR mismatch 时的最优比例式(23)在 `content.md:291-294` 给出 `s_o=SNR/SNRhat`。
- input → action → output：4% QPSK pilots → auxiliary-channel SNR estimate → 式(22)的噪声尺度/高斯 likelihood → soft LLR → SD-FEC；pilot-to-soft-demapper 事实见 `content.md:787,852-853`。
- baseline / cheap：matched auxiliary channel、`s=1`；cheap alternative 是只缩放 extrinsic LLR 的 `s_o`。
- boundary：没有给 pilot residual→SNR 的具体估计式；PS prior 不随 `s` 缩放；严格等价只在未量化且 mismatch 仅为 SNR 时成立（`content.md:540-544`）。
- truth / metric / relation / Step 3 question：在线 SNR 入口需要 pilots，离线 benchmark 使用发送 bits；指标为 post-FEC BER/GMI 系指标；与 C5-0 是 A/B primitive、C 的 coherent-optical direct context。Step 3 核对 pilot estimator、式(23)的纯 SNR-mismatch 假设及 prior/extrinsic 分离。

### QF5 — Layton et al., *Improved demapping for channels with data-dependent noise*

- identity/source：DOI `10.1186/s13638-018-1136-z`；canonical `source.pdf` 为 2,261,353 B、12 页 `%PDF-1.4`，`metadata.json` 为 `success/oa_pdf/good/title_check=match`；`tools/convert` 产出 `source.md`。
- evidence bucket：B+C-direct（APSK/satellite soft demapper）。
- executable entry：APP LLR Eq.(6)（`source.md:121-128`）、extrinsic LLR Eq.(9)（`source.md:134-140`）、逐星座点二维 Gaussian likelihood Eq.(10)（`source.md:142-148`）、pilot 样本均值/无偏协方差 Eq.(11)–(12)（`source.md:150-162`）。
- input → action → output：known APSK pilots → 按 constellation point 估计 `mu_k,Sigma_k` → Gaussian APP demapper → bit L-values/decoder soft input。
- baseline / cheap：正确未校准 baseline 是同样使用估计 centroid、但所有点共用恒定圆对称 covariance 的 standard demapper（`source.md:199`）；centroid-only/constant-covariance 是低成本 comparator。
- boundary：主实验每点 120 pilots、64 阶约 6% 开销；这是高维逐点 covariance primitive，不是 C5-0 的低维 scalar，也不授权重开 C5-1。
- truth / metric / relation / Step 3 question：需要按 constellation point 标识的 known pilots；指标含 covariance estimation error 与 soft-decoder performance；与 C5-0 是 B/C-direct neighbor、不是 exact scalar recipe。Step 3 核对 standard demapper 的固定 covariance 定义、pilot 开销和因果性。

### QF6 — Xie et al., *Bit-Interleaved LDPC-Coded Modulation with Iterative Demapping and Decoding*

- identity/source：DOI `10.1109/VETECS.2009.5073425`；IEEE Xplore BLIT 取得的原始全文是 5 页完整纯文本（标题、作者、摘要、正文、结论、参考文献齐全），但文件错误命名为 `source.pdf`，不能声称 canonical PDF。`metadata.json` 的 `content_type=pdf` 因而是 source-format caveat。
- evidence bucket：C-related（APSK soft-demapping 邻居），不作为 scalar/mismatch 公式权威。
- executable entry：原始 BLIT 全文保留 Eq.(4) 的 APP/LLR 求和式；转换后的 `content.md:120-124` 明确 `L_a=0` 时退化为传统独立 demapper。
- input → action → output：接收 `y`、AWGN likelihood 与 decoder a-priori LLR → APSK soft demap/迭代反馈 → 更新 bit LLR。
- baseline / cheap：`L_a=0` 的 one-shot independent BICM demapper；它支持冻结的未反馈 baseline，但不是全局 scalar cheap alternative。
- boundary：16/32-APSK、AWGN；高成本 iterative demapping；不含 noise/reliability estimator 或 LLR calibration。公式图在 `content.md` 中被遗漏，因此 Step 3 应同时核对 BLIT 原始全文。
- truth / metric / relation / Step 3 question：运行时不提供校准 truth，而依赖 AWGN likelihood 与 decoder a-priori；指标为 BER；与 C5-0 仅 C-related。Step 3 核对原始 BLIT Eq.(4)、`L_a=0` one-shot baseline 和反馈复杂度边界。

## 4. 三个证据桶与最小门

| 桶 | qualified fulltext | 门槛 | 结果 |
|---|---|---:|---|
| A — mismatched BICM / L-value / GMI scalar | QF1、QF2、QF3、QF4 | ≥2，且 ≥1 可执行式 | PASS：4 篇；QF2 式(12)、QF3 式(34)均可执行。 |
| B — receiver-visible known/pilot residual → reliability/noise → soft metric | QF3、QF4、QF5 | ≥2 | PASS：3 篇；known-symbol residual、pilot SNR、pilot covariance 三种入口。 |
| C — APSK / coherent optical / FSO soft-demapping neighbor | QF3、QF4、QF5、QF6 | ≥1 | PASS：Layton 为 APSK direct；QF3/QF4 为 coherent-fiber direct context；VTC 为 APSK related。 |

唯一全文总数为 6，位于要求的 `6..10`。没有用 Baldi、Zhang 或 simplified APSK demapper 的标题/摘要补足计数。

## 5. Baseline、廉价替代与 claim ceiling

- **正确未校准 baseline B0**：同一 one-shot max-log/APP demapper、同一估计或假设的 auxiliary-channel 参数，输出未经额外校准的 mismatched LLR，即 `s=1`/`alpha=1`。匹配 likelihood/真实噪声统计单列为 `B_match/O1` reference；target-scene 最近的可执行对照是 Layton 的 centroid-corrected、恒定圆对称 covariance standard APSK demapper。VTC 的 `L_a=0` independent demapper只补 one-shot 边界。
- **廉价替代**：单一全局 scalar `L^c=sL`；QF1/QF2/QF3 均给一维目标或等价 `q^s` 解释。clip/offline LUT 可留作后续 comparator，但本轮没有拆成新方法。
- **可执行原子**：known symbols/pilots 产生 residual/noise/reliability estimate；同一 demapper 产出 uncalibrated LLR；只对 extrinsic/channel LLR 应用低维 scalar；输出进入冻结 LDPC decoder。
- **不得外推**：没有 FSO 直接全文；没有取得 Zhang 的 APSK scalar 原文；Layton 是逐星座点高维 covariance，不是 C5-0 scalar；QF3/QF4 的光纤结果也不能直接证明 APSK/FSO decoder gain。
- 因此 Step 3 的 claim ceiling 是“通信通用 scalar atom + receiver-visible reliability atom 向 APSK/FSO 的受限迁移”；完整 recipe collision 留给 mandatory Step 3.5。

## 6. Step 3 read pool 与唯一下一步

Step 3 精读顺序：QF2（直接标量式）→ QF3（known-symbol residual 与实验 GMI）→ QF4（pilot SNR 与 PS prior 边界）→ QF1（mismatch/GMI baseline）→ QF5（APSK direct 与正确 standard demapper）→ QF6（APSK one-shot/iterative 边界，带 source-format caveat）。

**唯一下一步**：另派 GW Step 3 精读任务，对上述 6 篇形成 canonical extraction；在此之前继续禁止实现、仿真、Q#、Step 3.5 collision 结论或论文正文写作。

## 7. 取得与文件完整性验证

- task-control validator：`PASS`；`base=9a31d5d73e87c37417840a66767a20d8df0f8e36`、`epoch=11`、`checkpoint=CP011`。
- 六篇证据均有本地全文与 `metadata.json`；四篇 arXiv HTML、Layton canonical PDF、VTC 原始 BLIT 全文分别保留来源形态，不把纯文本冒充 PDF。
- Layton canonical PDF 独立校验：magic=`%PDF-1.4`、2,261,353 B、12 页、SHA-256=`b53c96bd24de33c978febb65ea0f9e374e0420332a4d3aba8ec40ab0582b84df`；Markdown 由项目 `tools/convert` 生成。
- 八个检索式均有结构化归档；只有 Q6 返回 2 条，其余 0 条。OpenAlex 限流、部分源缺凭据均只记为 source failure，不解释为“无文献”。
- authored report、metadata、索引及检索 JSON 的 `git diff --check` 通过。由项目工具原样取得/转换的 arXiv HTML、全文 Markdown 自带行尾空格，Layton 二进制 PDF又受仓库 `.gitattributes` 的 `diff=astextplain` 影响；两类机械产物不做手工净化，分别以 source/metadata 身份审计和上述 PDF magic/page/hash 验真。

## 8. Terminal

`STEP2_READY_FOR_STEP3`

理由：A/B/C 三桶达到最小篇数，唯一 qualified fulltext=`6`，且正确未校准 baseline、全局 scalar cheap alternative、直接可执行校准公式均有真实全文。保留 FSO direct 与 APSK scalar 原文缺口，但它们收窄 target-scene claim ceiling，不构成本任务定义的 Step 2 blocker。
