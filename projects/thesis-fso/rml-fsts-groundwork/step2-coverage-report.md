# RML-FSTS Groundwork Step 2 覆盖面报告

> 2026-08-08 | terminal: `STEP2_READY_FOR_USER_CONFIRMATION`

## 获取结果

shortlist 共 12 篇，全部为正式发表身份。独立全文核验后，5 篇满足 identity、provenance、正文质量与有效行数不少于 50 的 CORE 门：

| 论文 | CORE | 全文与质量 |
|---|---|---|
| Wang 2023 FSTS, `10.1109/JPHOT.2023.3265847` | C1/C2/C4 | 共享 `content.md`，251 有效行，PASS |
| Wang 2024 enhanced frame/carrier recovery, `10.1364/OE.520452` | C2/C4 | 共享 `content.md`，497 有效行；公式转换有限，仍为正文 |
| Morelli 2009 practical MIMO-OFDM CFO, `10.1155/2009/821819` | C3 | 本轮 Unpaywall PDF，192 有效行；title match |
| Paillier 2020 AO+DPLL, `10.1109/JLT.2020.3003561` | C4 | 共享 arXiv LaTeX 正文，110 有效行 |
| Yu 2023 stepwise carrier synchronization, `10.1109/TVT.2022.3218937` | C3 | 共享 PDF/`source.md`，318 有效行；公式/图缺省但主体完整 |

receipt 中逐篇记录 absolute path、source/content SHA256、bytes、总行数、有效行数、identity 与 provenance。

## 内容质量不合格

- Tang 2022 STSB（`10.1109/JPHOT.2022.3161795`）：正文身份与 119 有效行通过，但现有 metadata 写 `failed/all_failed` 且 `content_file` 为空，与 PDF/正文矛盾；不计入合格 CORE。
- WiSEE 2024 data-aided DSP（`10.1109/WiSEE61249.2024.10850117`）：正文身份与 112 有效行通过，但 metadata 同样与现有 PDF/正文矛盾；不用于凑足五篇。

## 三轮后失败与人工补件

| DOI | 重要性 | 三轮结果 | 用户动作 |
|---|---|---|---|
| `10.1016/J.OPTCOM.2020.126046` | 低 OSNR task-matched comparator | OA/Unpaywall 失败；无正式稿身份；非 IEEE 专用项 | 合法取得 PDF 后用 `tools/convert` |
| `10.1109/CHINACOM.2009.5339877` | exact-title multi-correlation-lag prior art | OA 失败；无正式稿；IEEE exact identity 命中但下载因本地 GBK 错误失败 | 手动下载 IEEE PDF 后转换 |
| `10.3390/electronics10232942` | multi-pilot correlation comparator | OA/Unpaywall 失败；无正式稿 | 合法取得 publisher PDF 后转换 |
| `10.1364/OE.505931` | 实时低 SNR diversity/CPR transfer | OA/Unpaywall 失败；无正式稿 | 合法取得 Optica PDF 后转换 |
| `10.1364/OE.448956` | branch phase-asynchrony transfer | OA/Unpaywall 失败；无正式稿 | 合法取得 Optica PDF 后转换 |

Tang 的 IEEE exact identity 也在专用轮命中但 0/1 下载；因已有正文却 provenance 矛盾，归入内容不合格而非缺失项。下载工具在 Windows 下的 Bash wrapper 因 CRLF 不能 dispatch，本轮使用同一项目底层 `paper_download.py`；未改工具、未绕付费墙、未用 WebReader/ResearchGate。

## 发表身份与系统性偏差

- shortlist：正式发表 12 / 预印本 0 / unknown 0。
- 合格 CORE：正式发表 5 / 预印本 0 / unknown 0。
- 当前 C1/C2 主要来自 Wang 团队的 coherent-FSO training-sequence 谱系；C3 两篇来自无线/卫星场景，只能约束 prior-art ceiling 与 correlation 机制，不能证明目标 FSO defect。
- C4 有三篇合格全文，但缺失的两篇 Optica direct transfer 仍限制对实时 diversity/branch phase 的覆盖深度。

## 四类覆盖门

| 类别 | 合格全文 | 结论 |
|---|---|---|
| C1 Wang 2023 source baseline | Wang 2023 | PASS |
| C2 至少一篇 2019+ task-matched comparator | Wang 2023、Enhanced 2024 | PASS |
| C3 multi-lag/stepwise 或 strongest single-lag alternative | Morelli 2009、Yu 2023 | PASS |
| C4 coherent-FSO transfer | Wang 2023、Enhanced 2024、Paillier 2020 | PASS |

5 篇合格 CORE 且四类齐全，因此 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。这只表示覆盖面可交用户确认；不证明 target lag-ranking crossover、conditioned single-lag failure 或 novelty，不授权 Step 3/3.5/4a、smoke、实现或仿真。

## 用户确认动作

请用户二选一确认覆盖面：接受当前 5 篇合格 CORE 作为未来 Step 3 的输入边界；或先补上述关键失败全文/修复 Tang、WiSEE provenance。未收到确认前保持硬停止。
