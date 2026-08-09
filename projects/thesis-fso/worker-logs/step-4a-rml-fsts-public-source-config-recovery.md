# RML-FSTS public source-config recovery

## Verdict

`SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`

本次 15 分钟有界恢复覆盖了 publisher/DOI metadata、author identity/institutional、code/data repository 三类独立 surface。没有取得 supplementary code、dataset、repository、学位论文附录或可证明属于 Wang 2023 同一 executable source chain 的 artifact。公开一手证据只重复闭合论文正文中的少量平台参数，仍不能唯一执行 phase-screen/SMF channel，也不能计算 `P_rx[dBm] -> E[|w[k]|^2]`。因此 D012 `SC1` 不成立；不得据此恢复 performance grid、diagnostic structural run 或 bounded MVE。

本结论是 bounded public-source exhaustion，不是“相关材料在世界上不存在”的全称断言，也不是 paper/source identity 无效。

## Control validation and search ledger

### Control validation

- command: `python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions\2026-08-08-rml-fsts-groundwork\T020-step4a-public-source-config-recovery.md --repo-root D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- result: `PASS`
- binding: epoch `37`, checkpoint `CP024`, action class `NEW_TOPIC_RECOVERY`
- interpretation: 只证明任务授权一致，不证明 scientific/source closure。

### Search ledger

| surface | authoritative query / endpoint | observed result | stop interpretation |
|---|---|---|---|
| Publisher / DOI metadata | `https://api.crossref.org/works/10.1109%2FJPHOT.2023.3265847` | Crossref 精确返回 DOI、三名作者 ORCID、IEEE document URL `10097873`；`relation={}`，唯一 `link` 是 version-of-record PDF metadata，没有 supplement/data/code relation | exact paper identity CLOSED；executable attachment NOT FOUND |
| Publisher page/media | `https://ieeexplore.ieee.org/document/10097873/`; Fig.4/Fig.10 `mediastore` large-GIF URLs | IEEE document REST 请求返回 HTTP 418；Fig.4、Fig.10 原图请求均 HTTP 403；现有 canonical HTML 已含正文与 media URL，但无附件清单 | 正文镜像可审计；原图/附件未取得，且图本身不能闭合 SC1 1–7 |
| Data DOI registry | `https://api.datacite.org/dois?query=doi%3A10.1109%2FJPHOT.2023.3265847&page%5Bsize%5D=10` | total `0` | 未发现以该 DOI 登记的 DataCite dataset/software record |
| Author identity / institution | ORCID public API for `0000-0002-2512-2851`, `0009-0008-3197-0196`, `0000-0002-4992-666X` | 三个 ORCID person identity 与 Crossref 一致；Liqian Wang 的 public employment 为 Beijing University of Posts and Telecommunications / State Key Laboratory of Information Photonics and Optical Communications；三人的 public researcher-url 列表为空 | author identity CLOSED；公开 code/data landing page NOT FOUND |
| Code repository | GitHub repository API exact DOI；exact title + `FSTS` | exact DOI count `0`; exact title count `0` | 无 exact-identity repository；GitHub repository-level bounded query结束 |
| Data/software repository | Zenodo API exact DOI；exact title | 两项 count 均 `0` | 无 exact-identity Zenodo record |
| General exact search | exact title、DOI、`10097873`/`10101698` + supplement/code/data/DataPort/Code Ocean/GitHub/Gitee/Zenodo/Figshare/OSF | 返回 exact-paper ResearchGate 镜像、相关/引用论文与大量 `10101698` 假阳性；没有 exact executable artifact | 第三方正文镜像不提升 source closure；按三类 surface 止损 |

连续 publisher/author 两类只得到正文/身份而无附件后，已完成 repository 第三类；满足 T020 止损条件，未继续扩大检索。

## Exact-paper artifacts

1. Canonical local IEEE HTML-derived content:
   - official identity URL: `https://ieeexplore.ieee.org/document/10097873/`
   - local path: `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`
   - SHA-256: `e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f`
   - bytes: `55349`
   - source identity: IEEE Xplore OA article scrape, DOI `10.1109/JPHOT.2023.3265847`; local metadata says `firecrawl_scrape`, `content_type=html`, quality `good`
   - license: article page declares Creative Commons Attribution 4.0 (`https://creativecommons.org/licenses/by/4.0/`)
   - executable status: **not executable config**;正文没有 supplement/code/data link。

2. Canonical metadata:
   - local path: `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/metadata.json`
   - SHA-256: `b9236f0ff4fece29bf6b6df3358b8eb29e5e781d8f99e86556a0075cb123dce0`
   - bytes: `514`
   - source identity: project acquisition metadata for the exact DOI
   - executable status: no source PDF, code, dataset or supplementary artifact recorded。

3. Official Fig.10 URL (auxiliary only):
   - `https://ieeexplore.ieee.org/mediastore/IEEE/content/media/4563994/10101698/10097873/wang10-3265847-large.gif`
   - HTTP result: `403 Forbidden`
   - hash: `N/A (bytes not acquired)`
   - source identity: URL embedded by IEEE in canonical article content at `content.md:301`
   - executable status: 即使取得也只能补图轴/曲线，不闭合 SC1 1–7。

没有发现新的 exact executable artifact，因此没有新的 artifact URL/hash/license 可报告。

## Author/same-platform evidence

- Crossref authoritative metadata将三名作者绑定到给定 ORCID，并把 primary resource 指向 IEEE document `10097873`。Crossref `relation` 为空，不能从 DOI metadata 推导 supplement/data/code。
- ORCID public record只提供身份与有限 affiliation。Liqian Wang 的公开 employment 指向 BUPT State Key Laboratory；三人的 public researcher URLs 均为空。该结果不能证明作者从未公开代码，只说明 ORCID 未给出可跟随的代码/数据入口。
- exact search 命中同团队/同领域后续论文（例如 Liqian Wang 参与的 2024 Photonics TTQP FOE 论文），但它是不同算法/不同 paper identity；未发现其中有明确声明复用 Wang 2023 的同一 phase-screen/SMF/noise executable chain。因此依 T020 只能记 `RELATED_ONLY`，不能迁移参数。
- ResearchGate 命中是 exact-paper 正文镜像，属于第三方镜像；没有可验证 supplement identity，未用于技术闭合。

## SC1 field closure matrix

状态只使用 T020 允许的 `EXACT_CLOSED / RELATED_ONLY / NOT_FOUND / CONTRADICTED`。同一行出现论文的部分参数不代表整行 executable closure。

| # | SC1 field | status | exact/author evidence and location | remaining executable gap |
|---:|---|---|---|---|
| 1 | carrier wavelength；input field / beam geometry | `NOT_FOUND` | canonical paper `content.md:231` 只给 ECL linewidth `50 kHz` 与 DP-IQ optical chain；全文无 wavelength、waist、wavefront curvature、plane/spherical/Gaussian field 数值。Crossref/ORCID/repository surfaces未给补件 | `lambda`、`U_0(x,y)`、beam waist/curvature/launch aperture 全缺 |
| 2 | phase-screen spectrum/normalization；screen count/spacing；FFT grid/extent；subharmonics；propagator | `RELATED_ONLY` | `content.md:241` 只明确 Fourier-transform phase-screen、`z=10 km`、outer scale→infinity、inner scale→0、两档 `C_n^2`。短摘录：`Fourier transform-based phase screen model` | spectrum constant/PSD normalization、screens/`Delta z`、grid size/pitch/extent、low-frequency compensation/subharmonics、Fresnel/split-step convention 均缺 |
| 3 | aperture 与 SMF mode/overlap；branch independence/covariance；per-frame/state lifecycle | `RELATED_ONLY` | `content.md:243` 给 receiver aperture `0.2 m`、multiple telescope signals labeled independent、SMF coupling、弱/强 mean coupling `67.3012%/4.8395%` | SMF mode-field radius与 overlap equation、complex coupling distribution、phase/intensity/coupling joint law、branch spatial separation/covariance、realization reset/continuity/frame lifecycle 均缺 |
| 4 | received optical-power reference plane；per-pol/per-branch accounting | `RELATED_ONLY` | `content.md:160` 的 sample model含 `sqrt(eta I P_LO)`；`content.md:279,309,319,339` 使用 received/average received optical power axes | 未说明 telescope 前/后、coupling 前/后、single branch/per-pol/total/MRC 后；没有 hybrid splitting 与 accounting rule |
| 5 | BPD/optical-hybrid/TIA gains；shot/thermal/background/dark；temperature/load/noise density | `RELATED_ONLY` | `content.md:243` 给 BPD、shared LO `15 dBm`、responsivity `0.8 A/W`，并仅称考虑 shot/thermal noise。短摘录：`Shot noise and thermal noise are also considered here` | 90° hybrid/BPD splitting、TIA gain/noise、temperature/load、dark/background current、shot/thermal PSD/variance 全缺 |
| 6 | equivalent noise/filter bandwidth；sample/matched-filter convention；ADC scaling/quantization | `RELATED_ONLY` | `content.md:183` 的 FOE 推导采用 one sample/symbol；`content.md:231` 给 10 GBaud；`content.md:243` 只称 ADC digitizes signals | NEB、analog/digital filter、matched pulse、sample integration、ADC full-scale/gain/bits/quantizer、complex-noise normalization 全缺 |
| 7 | 从明确方程和数值唯一计算 `P_rx[dBm] -> E[|w[k]|^2]` | `NOT_FOUND` | `content.md:160` 仅把 `N_x,N_y` 定义为 coherent-receiver Gaussian noise；第 5–6 行所需量没有补件。没有 repository/source backend mapping | 同一 `P_rx` 可对应多组 bandwidth/gain/noise accounting；不存在唯一数值映射，禁止典型值或结果反标 |
| 8 | Fig.10 source power/action ticks；B0 numeric tolerance | `RELATED_ONLY` | `content.md:299` 闭合 x-axis=`B_L`、trend 与四个 paper design points：320 4QAM `(16,20)`、320 16QAM `(8,40)`、960 4QAM `(24,40)`、960 16QAM `(16,60)`；official large GIF URL 403 | 各 panel source power、完整 action ticks、pointwise NMSE/uncertainty与 preregisterable numeric tolerance 未恢复；且无法替代 1–7 |

SC1 1–7 中 `EXACT_CLOSED=0/7`；因此不满足 `SC1=PASS` 的“同一 executable source chain、无需典型值/结果拟合”条件。

## B0 calibration consequence

- 可保留的 exact-paper anchor：10 GBaud；Tx/LO linewidth 50 kHz；LO 15 dBm；responsivity 0.8 A/W；10 km；`C_n^2={1e-16,1e-14} m^(-2/3)`；0.2 m aperture；两档 mean coupling；Fig.10 四个 design points与先升后可能下降的定性趋势；4QAM `-43 dBm`、16QAM `-37 dBm` 的 B2B CFO-sweep condition（`content.md:309,319`）。
- 这些 anchor 不能形成 B0 numeric gate：source power reference plane、phase-screen/SMF realization、noise equation、Fig.10 panel powers/ticks和 tolerance 不能同时冻结。
- `P_rx[dBm]` 不得转换为项目中的 dimensionless `gamma_bar`，不得以 synthetic SNR 反调到 Fig.11/12 的量级，不得用 Fig.10 digitization替代 receiver/noise closure。
- B0 consequence: `NOT_EXECUTABLE`; B0/B1/B2/O1/C1 performance numerics继续 `N/A (NOT_RUN)`。

## Dead ends and stop rule

1. `10101698` 作为 exact article number 搜索产生大量完全无关结果。Crossref/IEEE identity表明 paper document/arnumber 是 `10097873`；`10101698` 是 IEEE Photonics Journal issue identifier，paper另有 article sequence number `7302313`。后续检索必须以 DOI/title/`10097873` 为主。
2. exact-title 搜索得到 ResearchGate mirror；第三方正文镜像无 source-code/config provenance，不提升 SC1。
3. publisher metadata只有 version-of-record PDF link且 `relation={}`；未发现 supplement relation。正文/PDF不等于 executable config。
4. ORCID闭合身份/机构但无 researcher URL；不应从机构相同推断同一仿真链。
5. GitHub、Zenodo exact DOI/title count均为 0；零结果仅支持本次 bounded stop，不支持全网不存在断言。
6. IEEE Fig.4/Fig.10 media URL再次返回 403。图轴恢复是 auxiliary gap，不是 SC1 closure。
7. 已覆盖三类独立 surface，满足 T020 止损；没有联系作者、提交表单、绕过访问控制、clone仓库、下载PDF、运行 estimator/grid/MVE或修改任何 owner/protected artifact。

## Artifact/provenance ledger

| artifact / endpoint | identity | local hash / remote result | license / authority | use ceiling |
|---|---|---|---|---|
| `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md` | exact IEEE paper HTML-derived content | SHA-256 `e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f` | IEEE page; CC BY 4.0 | exact prose/formula/platform facts only；not executable config |
| `.../metadata.json` | exact DOI local acquisition metadata | SHA-256 `b9236f0ff4fece29bf6b6df3358b8eb29e5e781d8f99e86556a0075cb123dce0` | project provenance record | source identity/acquisition only |
| `https://api.crossref.org/works/10.1109%2FJPHOT.2023.3265847` | exact DOI registry record | live response: DOI/title/authors/document `10097873`; `relation={}` | Crossref authoritative metadata | identity/link relation only |
| `https://api.datacite.org/dois?query=doi%3A10.1109%2FJPHOT.2023.3265847&page%5Bsize%5D=10` | exact DOI data-registry query | total `0` | DataCite authoritative registry | bounded absence only |
| ORCID public records for three task-listed IDs | author identity | person identity match；Liqian affiliation；researcher URLs empty | ORCID authoritative identity | identity/institution only |
| GitHub repository search exact DOI/title | public code repository query | `0 / 0` | GitHub API | bounded absence only |
| Zenodo record search exact DOI/title | public data/software repository query | `0 / 0` | Zenodo API | bounded absence only |
| IEEE Fig.10 large GIF URL | exact-paper figure URL | HTTP `403`; SHA-256 `N/A` | IEEE embedded media URL; article CC BY 4.0 | no bytes acquired；no calibration authority |

## Next legal action

向主控回传 `SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`。本 worker 不修改 D/S/V/topic/master/contract。主控在接收 T020 与 T021 后按 D012 reducer 裁决；只要 SC1 保持未闭合，就必须得到 `REOPEN_INPUTS_NOT_CLOSED`、恢复专题 dormant并保持 D011 terminal 5。若未来用户另行授权外部沟通，最小缺件应是作者/source backend 的同一链 configuration/code：完整 phase-screen/SMF realization加上明确 reference-plane 的 `per-branch P_rx[dBm] -> post-filter/post-ADC E[|w[k]|^2]`；本次未联系作者。
