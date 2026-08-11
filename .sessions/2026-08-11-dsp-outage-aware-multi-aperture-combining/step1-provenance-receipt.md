# Step 1 Identity / Provenance Receipt

> 只绑定本轮开始前已存在的仓库索引证据；不是新增 query，不下载，不全文精读。

## P01 — 2019 closest direct competitor

- 全局索引定位：`search-archive/_index/all-papers.jsonl:10860`（当前文件行号；key=`doi:10.1016/j.optcom.2019.03.069`）。
- DOI：`10.1016/j.optcom.2019.03.069`
- title：*Adaptive digital combining for coherent free space optical communications with spatial diversity reception*
- year / venue：2019 / Optics Communications
- source APIs：`semantic_scholar`, `openalex`, `openalex+semantic_scholar`
- 摘要动作事实：
  1. 研究对象为 coherent FSO spatial diversity reception；
  2. 明确动机是避免 random and time-varying channel fading 的耗时、复杂估计过程；
  3. 提出 adaptive digital combining algorithm；
  4. 验证对象为 BPSK/QPSK four-aperture receiver，与 EGC 比较。
- 本轮 direct hit：`dsp-outage-multi-aperture-q2.json` 的 L009（Tavily/ADS 镜像，title 截断）。
- 仍未闭合：摘要没有给 validity input、trigger、weight update 或 abstention 语义，故 exact collision=`UNRESOLVED`。

## P02 — Geisler 2016 foundational identity

- 全局索引定位：`search-archive/_index/all-papers.jsonl:15493`（当前文件行号；key=`doi:10.1364/oe.24.012661`）。
- DOI：`10.1364/OE.24.012661`
- title：*Multi-aperture digital coherent combining for free-space optical communication receivers*
- year / venue：2016 / Optics Express
- source APIs：`semantic_scholar`, `openalex`
- 摘要动作事实：各小孔径后 coherent detection 与 digitization，随后在 DSP chain 中 combining；实验为 four lasercom signals lossless coherent combining。
- 本轮 direct hit：Q2 L008 与 Q6 L004/L014（Tavily/Optica 页面摘录）。
- 边界：该文是 reference M / phase-alignment 基础，不含 DSP-outage validity admission。

## P03 — 可复算性与时间边界

- 既有索引为 ignored local evidence，不存在 tracked commit。为避免把它伪装成版本化证据，本专题固定两条记录的 UTF-8 SHA-256：P01=`9c35292e34513a4b04289c44aa6b0a22358522a0ff6a9fc458b95a219651e4e8`；P02=`3d26dd2f1e15b9cd3791185b36cd3bf7d4827158a97c079a4560c66f7bddfab4`。
- verifier 应以 DOI key、title、year、venue、source APIs、摘要动作事实与行哈希复核；不得将全局索引的 relevance 或自动 publication label 当证据，也不得声称该 ignored 索引由本次 commit 版本化。
