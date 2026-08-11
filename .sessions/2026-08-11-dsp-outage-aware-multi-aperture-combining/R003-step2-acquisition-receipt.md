# [R003] Step 2 acquisition receipt

> 2026-08-11 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D002

## 调研问题

为冻结九篇优先池提供可机械复核的 identity、provenance、source/content 路径、字节数、SHA-256、有效行数与 qualified 结论。

## 发现

### Qualified fulltext

| 类别 | title / authors / year / venue / DOI | source provenance 与路径 | source bytes / SHA-256 | content 路径 | content bytes / lines（有效）/ SHA-256 | identity / qualified |
|---|---|---|---|---|---|---|
| optical CORE | *Data-Aided Multi-Format DSP for Robust Free-Space Coherent Optical Communication*；A. Johst, L. Molle, N. Perlot, M. Rothe, M. Rohde, M. Nölle；2024；IEEE WiSEE；`10.1109/WISEE61249.2024.10850117` | existing canonical；`papers/doi/10.1109_wisee61249.2024.10850117/source.pdf`；metadata=`blit_ieee_provenance_repair` | 1,185,870 / `87222b75547f88c038c43739c616865853787ca5b4fe5336de145c061dd340ce` | `papers/doi/10.1109_wisee61249.2024.10850117/content.md` | 35,131 / 268（131）/ `214343f9705ada66a469102bd72035761cd3cf235c1171ef7334946ce5ecc14e` | confirmed / YES |
| optical CORE | *Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication*；Liqian Wang, Jichen Wang, Xinyu Tang；2023；IEEE Photonics Journal；`10.1109/JPHOT.2023.3265847` | shared-root existing `firecrawl_scrape` HTML fulltext；无保留 source；content-only | N/A / N/A | `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md` | 55,349 / 455（251）/ `e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f` | confirmed / YES |
| RF comparator | *Reliability Analysis of MRC Diversity Reception System Based on LS and MMSE Channel Estimation*；Yongjian Yang, Hong Jiang, Ying Luo；2022；IEEE ICCC；`10.1109/ICCC56324.2022.10065885` | `tools/blit --source ieee`；`papers/doi/10.1109_iccc56324.2022.10065885/source.pdf` | 5,057,185 / `fa9a600aaa5719562832002f63882203bd2153c9db69a6584339e554b842dd28` | `papers/doi/10.1109_iccc56324.2022.10065885/content.md` | 25,920 / 267（113）/ `db204928db89aa7e0eb90b0dee609d6473d7dfd361fea504c5bba783abeb8403` | confirmed / YES |
| optical neighbor | *Phase Alignment With Minimum Complexity for Equal Gain Combining in Multi-Aperture Free-Space Digital Coherent Optical Communication Receivers*；Yicong Tu, Sheng Cui, Keji Zhou, Deming Liu；2020；IEEE Photonics Journal；`10.1109/JPHOT.2020.2977955` | `tools/blit --source ieee`；`papers/doi/10.1109_jphot.2020.2977955/source.pdf` | 3,725,840 / `acf0182a4900401b7e3c8aa61847f546f48b81bf6fa3eab17c50ab7a19c7b5af` | `papers/doi/10.1109_jphot.2020.2977955/content.md` | 29,389 / 308（121）/ `c7e5af6f7279e50f13d01df7705c77acbfa4f64091cde3fae5915e26ed8353db` | confirmed / YES；39 个 replacement char 局限于公式符号 |

> 本轮 Windows worktree 的 `tools/convert` shell wrapper 含 CRLF，Git Bash 无法解析；未改工具代码，直接调用同一 wrapper 的 `tools/pdf_convert.py` backend 完成两份 PDF 转换，并在 metadata 中登记这一 bounded runtime fact。

### Unavailable fulltext

| priority | title / authors / year / venue / DOI | identity provenance | source/content/bytes/hash/lines | qualified / 原因 |
|---|---|---|---|---|
| P0 optical CORE | *Adaptive digital combining for coherent free space optical communications with spatial diversity reception*；Jing Sun, Puming Huang, Zhoushi Yao, Jingzhong Guo；2019；Optics Communications；`10.1016/j.optcom.2019.03.069` | Semantic Scholar + OpenAlex title/author/year/venue/DOI 一致 | absent / N/A | NO；非 OA、无 arXiv/PDF URL，DOI/OA 下载失败 |
| P1 optical CORE | *Multi-aperture digital coherent combining for free-space optical communication receivers*；D. J. Geisler, T. Yarnall, M. Stevens, C. M. Schieler, B. Robinson, S. Hamilton；2016；Optics Express；`10.1364/OE.24.012661` | Semantic Scholar + OpenAlex + Step 1 Optica result identity consistent | absent / N/A | NO；OA metadata 的 DOI/viewmedia 合法入口均失败 |
| P1 optical CORE | *Experimental demonstration of robust spatial-diversity combining for coherent free-space optical transmission*；A. Johst, M. Nölle, L. Molle, N. Perlot, M. Rohde, R. Freund；2024；OFC；`10.1364/OFC.2024.W2A.31` | Semantic Scholar + OpenAlex identity；错配 abstract 未使用 | absent / N/A | NO；非 OA、无 arXiv/PDF URL |
| P2 optical neighbor | *Toward Practical Digital Phase Alignment for Coherent Beam Combining in Multi-Aperture Free Space Coherent Optical Receivers*；Chenjie Rao, Sheng Cui, Yicong Tu, Keji Zhou, Deming Liu；2020；IEEE Access；`10.1109/ACCESS.2020.3035748` | OpenAlex + IEEE search identity consistent | absent / N/A | NO；默认/OA 失败，IEEE PDF 流式读取两次 30 s 超时 |
| P2 optical neighbor | *Real-time demonstration of two-aperture coherent digital combining free-space optical transmission with a real-valued MIMO adaptive equalizer*；Cheng Ju, Na Liu, Dongdong Wang, Danshi Wang, Jingze Yu, Yue Qiu；2024；Optics Letters；`10.1364/OL.511941` | Semantic Scholar identity confirmed | absent / N/A | NO；非 OA、无 arXiv/PDF URL |

### Acquisition evidence

- dry-run：九篇均执行；WiSEE 2024 命中 cache，其余映射到 canonical DOI 目录。
- first round：`tools/download --doi`；P0 与六篇缺失项均 `all_failed`。
- second round：Step 1 OA result/精确标题 S2+OpenAlex；P0/OFC/OL 无 OA 文件；Geisler 的 DOI/viewmedia 与两篇 2020 IEEE OA URL 均未由 `tools/download` 取得。
- third round：`tools/blit --source ieee`；ICCC/JPHOT 成功，Access 两次 timeout。
- C26：仅现有截断 title 与 URL `10.1109/TWC.2006.1687731`，authors/year/venue/DOI 字段未闭合，identity=`UNKNOWN`；未计入全文或 CORE。

## 结论

九篇中 fulltext available/content qualified=`4/9`；冻结 optical CORE qualified=`2/5`。P0 fulltext unavailable。

## 对决策的影响

支撑 R002 的 `STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`；不构成全文方法结论、collision verdict、Q#、Go/Kill 或 METHOD_SIGNAL。
