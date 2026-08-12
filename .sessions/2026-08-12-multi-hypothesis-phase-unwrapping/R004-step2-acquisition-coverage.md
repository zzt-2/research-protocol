# [R004] Groundwork Step 2 acquisition 与 coverage

> 2026-08-12 | 关联：2026-08-12-multi-hypothesis-phase-unwrapping / D003

## 调研问题

R003 的 reference、full-mixture/fixed-order、recent coherent optical/FSO 与 cheap comparator 承重项是否有身份可信、内容合格的一手全文，使下一步不必根据摘要猜动作？

## 发现

### Acquisition pool 与质量门

本轮在授权的 8–12 篇范围内审计 12 篇：先查 worktree/shared canonical，再对缺失项执行 `tools/download --dry-run` 与正式获取；IEEE 缺口转 `tools/blit`；PDF 只用 `tools/convert` 底层脚本转换。仓库 bash wrapper 因 CRLF 不能执行，因此调用同一仓库脚本 `paper_download.py` / `blit.py` / `pdf_convert.py`，未修改工具或平台代码。

| ID | 角色 / 路线 | 全文状态 | Identity / content gate | Canonical owner |
|---|---|---|---|---|
| C01 Wang TSP 2022 | A reference | reused | CONFIRMED / QUALIFIED | shared DOI |
| C02 Shayovitz–Raphaeli TCOM 2016 | B full mixture | reused arXiv source | CONFIRMED_MANUAL_GATE / QUALIFIED | worktree arXiv |
| C05 Nature Communications 2024 | C recent optical | OA PDF + fast convert | CONFIRMED / QUALIFIED_WITH_GLYPH_LIMITATION | worktree DOI |
| C06 Optics Communications 2024 | C recent optical | unavailable | CONFIRMED_METADATA_ONLY / UNAVAILABLE | worktree stub |
| C07 SPIE 2026 | A/C recent slip | unavailable | CONFIRMED_METADATA_ONLY / UNAVAILABLE | worktree stub |
| C08 JLT 2020 | C space-ground | reused arXiv source | CONFIRMED_MANUAL_GATE / QUALIFIED | worktree DOI |
| C09 IEEE Access 2019 CSSC-CPE | A/C cheap optical | IEEE PDF + fast convert | CONFIRMED / QUALIFIED_WITH_GLYPH_LIMITATION | worktree DOI |
| C10 Scientific Reports 2021 | C complexity | OA PDF + fast convert | CONFIRMED / QUALIFIED_WITH_GLYPH_LIMITATION | worktree DOI |
| C11 Photonics 2023 | C satellite implementation | reused publisher HTML | CONFIRMED / QUALIFIED_WITH_PAGE_CHROME | shared DOI |
| C12 Electronics 2025 | C recent task baseline | reused OA PDF | CONFIRMED / QUALIFIED | shared DOI |
| C13 J. Optical Fiber Technology 2020 | cheap pilot reset | unavailable | CONFIRMED_METADATA_ONLY / UNAVAILABLE | worktree stub |
| C14 Fu–Kam TIT 2013 | A cheap improved unwrap | IEEE PDF + fast convert | CONFIRMED / QUALIFIED | worktree DOI |

计数：`12 selected / 9 qualified / 8 qualified CORE`。12/12 都有正式发表身份；10/12 是 2019+。9 篇合格全文中 C02 与 C08 以 arXiv 源包承载正式论文身份，preprint-source share=`2/9=22.22%`。C05/C09/C10 的正文含少量公式 glyph loss，但标题、DOI、章节、图表说明与主体正文可读；涉及公式的 Step 3 声称必须回看 source PDF。C11 含 publisher page chrome，但正文、身份与引用区齐全，不是反爬页或目录页。

### 三路线 coverage

- A reference defect / unwrap：C01 + C09 + C14 均有合格全文。
- B full mixture / fixed-order tracker：C02 合格全文，P0 full-mixture blocker 已闭合。
- C recent coherent optical/FSO task baseline：C05、C08、C10、C11、C12 合格；其中 C12 是 2025 inter-satellite baseline，故缺 C06/C07 不迫使下一步猜唯一近期动作。

### 失败项与止损

- C06 `10.1016/j.optcom.2024.130326`：DOI/OA/Unpaywall + arXiv lookup 后 `all_failed`。
- C07 `10.1117/12.3107192`：DOI/OA/Unpaywall + arXiv lookup 后 `all_failed`。
- C13 `10.1016/j.yofte.2020.102208`：DOI/OA/Unpaywall + arXiv lookup 后 `all_failed`。

三项都只保留 metadata-level identity，不计全文、不替代为 RF/coded/general phase tracker。C06/C07 是 recent competitor limitation，C13 是 pilot-reset cheap-comparator limitation；它们不构成当前唯一承重 recent baseline，因为 C05/C08/C10/C11/C12 已覆盖 recent coherent optical/FSO 路线。

### Step 2 边界

本报告只确认 fulltext available/unavailable、identity 与内容质量及 coverage。没有抽取完整 input→decision→action→output，没有判 D1/D2 exact collision、Q#、Go、方法或贡献。

## 结论

`STEP2_READY_FOR_USER_CONFIRMATION`。

原因：qualified CORE=`8≥5`；A/B/C 三路线都有全文；P0 reference C01 与 full-mixture C02 均闭合；近期 task baseline C12 及四个 task/complexity neighbors 可读。C06/C07/C13 明确保留为 coverage limitation，但不会迫使 Step 3 对唯一承重 baseline 猜动作。

## 对决策的影响

D003 的 Step 2 acquisition 已完成，可等待 Step 3 的另行授权。当前不能从 acquisition 结果推出 non-collision、新颖性、Q#、Go、方法或 `METHOD_SIGNAL`。逐项 hash、bytes、有效行数、provenance 和失败原因见 `projects/thesis-fso/multi-hypothesis-phase-unwrapping/step2-acquisition-receipt.json`。
