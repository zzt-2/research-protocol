# [S002] CCISP 当前工作树扩展稿重新编译与版面复核

> 2026-07-14 | 阶段：VERIFY / 当前工作树重建 | 状态：PARTIAL（可编译，但存在范围与词数债务）

## 目标

在不修改 W001–W003、不运行仿真、不修改绘图脚本的前提下，重新核对刚更新的写作源与当前 `ccisp2026` 工程，强制重建 PDF，确认实际页数、版面和当前扩展稿是否已经同步。

## 记录

### 源与目标身份

- W001–W003 当前工作树的变化是小范围措辞/精度更新：W001/W003 将 `1.85 dB` 改为“about 1.9 dB”，W002 补充多导频措辞并继续保留旧的 crossover/阈值叙述。
- 当前 `projects/simulation/paper/ccisp2026/sections/*.tex` 已经是后续 `CCE-CC-002` 扩展预览，不是 W001–W003 的逐字抽取版。当前目标中的 `sqrt(h)`、100-symbol/256-sample 分离、multi-pilot DA-LS、两层 CV/effective-SNR 选择、data-BER 和 BER-ratio 口径依据 D004/V003，不应被旧 W 正文直接覆盖。
- 本轮没有修改 W001、W002、W003；也没有修改仿真、结果 JSON 或绘图脚本。

### Fresh build 与页数

- 构建目录：`projects/simulation/paper/ccisp2026/`。
- 命令：`latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`。
- 结果：exit 0，`main.pdf` 7 页，Letter 纸张，IEEE conference 双栏；字体检查显示全部嵌入。
- 日志未检出 LaTeX error、undefined citation/reference 或 overfull box；存在 1 个 `Underfull \\hbox`（`main.log` 第 337 行）。
- 逐页渲染到 `tmp/pdfs/ccisp2026/page-1.png`–`page-7.png` 后，未见裁切、重叠或公式越界；第 6–7 页有大图浮动导致的明显留白。

### 当前内容量与范围债务

- `texcount` 结果为纯 text 3,241 词、headers 42、captions/其他 222、8 个 displayed equation groups、5 个 floats。把非正文项计入后的总和约 3,505，不能混报为纯正文词数；D001 的 3,500 词验收口径仍需明确。
- 当前工程实际嵌入用户最新导出的 `fig1_system_model_v5.pdf` 和 `fig2_adaptive_cpr.pdf`，两者都使用 `figure* [t]`。这与原 CCISP 首轮“Fig.1/Fig.2 只放显式占位框”的硬边界不一致；本轮不把图形视觉验收默认为完成。
- 用户给定新标题：`Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links`。本轮只更新 `main.tex` 标题，不改正文论证。
- 用户已更新 `fig1_system_model_v5.drawio` 与 `fig2_adaptive_cpr.drawio`，并同步产生当前构建实际使用的 PDF 导出。
- 当前 7 个正文引用 key 均可在 `references.bib` 找到，构建未产生未定义引用；`oracle` 图例语义、`DA-ML/NDA-ML` 术语和图轴/扩展范围说明仍需收口。

### 标题版增量构建（2026-07-14）

- 仅更新 `main.tex:13` 标题为 `Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links`，没有替换图资产或改正文。
- 最新图资产版 fresh build：`latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`，exit 0；`main.pdf` 8 页、Letter，输出 1029955 bytes。该构建使用了用户随后更新的 Fig.1/Fig.2 PDF 导出。
- 标题在第 1 页自然分为两行；未检出 LaTeX error、undefined citation/reference 或 overfull box；有 1 个 `Underfull \\hbox`（`main.log:337`，badness 3158）和 1 个 `Underfull \\vbox`（`main.log:361`，badness 1895）。
- 当前 Fig.1 落在第 3 页，Fig.2 落在第 4 页，BER 图落在第 6 页，结论/参考文献落在第 8 页。虽然 Fig.1 已用 `figure*` + `[t]`，但声明位于 `system_model.tex` 的 section 之后；若要真正浮到第 2 页页顶，需要把该浮动声明移到 `main.tex` 的 introduction 之后、system model 之前。

### 结论

本轮已完成“把当前工作树版本重新编译并看页数”的实测，但没有把旧 W 文本覆盖回 CCE 扩展版。标题版结果是一个可读、可编译的 8 页版面探针，不是已解除全部债务的最终投稿稿。

独立 verifier 的 V003 结论为 BLOCKED：构建、字体、引用闭合和基本可读性通过；Fig.1/Fig.2 越过原首轮占位边界，`DA-ML/NDA-ML/oracle` 定义、缩写首次展开、数字逐项溯源和 float 留白仍未收口。

## 决策引用

- D004（跨专题）：恢复 data-BER 口径和 26/29 的确定性证据，解除 CCE-CC-002 WRITE 暂停。
- V003（跨专题）：确认 1.9 dB 应归 NDA-vs-DA，Fig.3 不称 equal-BER SNR gain，crossover 与固定 13 dB 分离。
- CCE-CC-002（跨专题）：允许扩展预览进入 WRITE，但不覆盖本专题原始 Fig.1/Fig.2 占位硬边界。

## 范围确认

- 本轮是否在 scope boundary 内：是。本轮只做当前目标工程的重建、渲染和债务登记；没有新扩大正文、没有改源稿、没有跑实验。
- 当前工作树已有的 CCE 扩展正文和实际 Fig.1/Fig.2 属于本轮开始前的未提交状态，已在 `issues.md` 的 B-08/B-09 中单独标记，不能据此宣称原始首轮骨架边界已满足。

## 后续

- 独立 verifier 完成当前 7 页 PDF、数字/公式/引用、逐页版面和 C1–C10 复核。
- 用户决定是否保留 CCE 扩展预览作为下一版正文；若继续，先锁 D001 词数口径、Fig.1/Fig.2 是否允许实际图、Oracle/DA-ML/NDA-ML 语义和 CCISP 页数口径。
- 下一轮版式约束：按用户当前编号将图 3 缩小为单栏宽；图 1/图 2 暂缓，待用户先微调后再重新对齐图注、交叉引用和正文文字。
- 图 1 版式候选：当前已验证 `figure* [t]` 仍落第 3 页；下一步若用户确认，单独移动其浮动声明位置，不改图内容。
