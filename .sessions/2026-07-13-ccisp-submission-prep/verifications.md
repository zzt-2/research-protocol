# CCISP 2026 投稿骨架验证记录

## V001: 首轮骨架与 PDF 独立复核

> 2026-07-13 | 关联：S001 | 结论：PARTIAL

### 验证范围

由独立只读 verifier 对 `projects/simulation/paper/ccisp2026/`、W001–W003、`main.pdf`、`main.log` 和 `external-output` C1–C10 进行复核；未跑仿真，未修改绘图脚本、W001–W003 或工程文件。

### 结论

- **正文保真：PASS（就实质正文而言）**。未发现 W001–W003 的实质段落、主要公式或结论被遗漏/擅改；HTML TBD 被省略并登记到 `issues.md`。由于 Fig.1/Fig.2 占位，源文档中的 Figure 2 在目标 PDF 中按 LaTeX 自动编号为 Fig.3，这是预期结构性变化。
- **数字/公式/引用：PARTIAL**。3 条已核验引用一致，4 组 unresolved 引用完整暴露；D008 阈值语义、crossover 数字、`1.9/1.85 dB`、DA 公式与 `N_p` 文字、SNR 扫描范围与图轴范围仍有债务。仿真未运行，因此不对数字真实性作新验证。
- **图形：PASS（首轮策略）**。Fig.1/Fig.2 为显式占位框，三张既有 PDF 图成功嵌入并自动编号为 Fig.3–Fig.5；未发现缺图、裁切或重叠。
- **PDF：PASS（当前产物）**。`main.pdf` 为 6 页 Letter 双栏，字体全部嵌入，当前 PDF 可读；`main.log` 无 LaTeX error、未定义引用/交叉引用、overfull/underfull box。独立 verifier 未再次运行 latexmk，最新编译证据以本轮主线程命令和日志为准。
- **external-output：PARTIAL**。C8、C9 PASS（C9 为 N/A）；C1、C5、C6、C7、C10 PARTIAL；C2、C3、C4 DEBT。`naive`、缩写首次展开、baseline 口径、阈值语义和正式引用仍未关闭。

### 阻塞项与非阻塞债务

- 阻塞项：`issues.md` B-01–B-07（语义/数字/引用/格式口径待决）。
- 非阻塞债务：`issues.md` D-01–D-07（术语、TBD/Table I、图形验收、工具路径、float 留白、caption 和 C1–C10 收口）。

### 证据指针

- 目标工程：`projects/simulation/paper/ccisp2026/main.tex`、`sections/*.tex`、`references.bib`、`issues.md`。
- 构建证据：`projects/simulation/paper/ccisp2026/main.log`、`main.pdf`。
- 源文档：`.sessions/2026-07-09-thesis-writing/W001-intro-system-model.md`、`W002-method-results.md`、`W003-conclusion-abstract.md`。

## V002: D008 阈值语义修正 delta 复核

> 2026-07-13 | 关联：S001、V001 | 结论：PASS

### 验证范围

只读复核 V001 之后的 `sections/method.tex`、最新版 `main.pdf`/`main.log` 和 Fig.1/Fig.2 占位；未跑仿真，未修改绘图脚本或源写作文件。

### 结论

- `method.tex:34,38` 明确 `gamma_th` 为固定 effective-SNR switching threshold；observed、regime-dependent BER crossover 仅作为观测现象，且不用于重新估计阈值，符合 D008。
- 最新 `main.pdf` 为 6 页；独立 delta verifier 确认 PDF 可读、字体嵌入，`main.log` 未检出 LaTeX error、undefined citation/reference、overfull 或 underfull。
- Fig.1/Fig.2 仍为 `system_model.tex` 与 `method.tex` 中的显式占位框，未被正式图替换。

### 残余范围

V002 只覆盖 D008 语义修正，不关闭 W002 源文档本身、crossover 数字、引用、`naive`、Table I 或版面留白等 `issues.md` B/D 项。

## V003: 当前 CCE 扩展预览 fresh build 与独立版面复核

> 2026-07-14 | 关联：S002、D004（跨专题）、V003（跨专题） | 结论：BLOCKED

### 验证范围

独立 verifier 只读检查当前 `projects/simulation/paper/ccisp2026/`、fresh `main.pdf`/`main.log`、7 页 PNG、W001–W003 与 CCE-CC-002/D004/V003；未修改文件、未跑仿真、未调用网络、未修改绘图脚本。

### 验证项

- [x] 构建与新鲜度：主线程执行 `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`，exit 0；PDF/PNG 时间晚于正文源。
- [x] PDF 属性：`main.pdf` 为 7 页、Letter（612 x 792 pt）、PDF 1.7、未加密；`pdffonts` 共 34 条字体记录，全部 `emb=yes`。
- [x] LaTeX 诊断：未发现 fatal/error、undefined citation/reference 或 overfull；发现 1 个 `Underfull \\hbox`，badness 3158，位于 `main.log:337`。
- [x] 逐页版面：7 页无裁切/重叠/公式越界；第 6–7 页存在 float displacement 和明显留白。
- [x] 数字/公式/引用：`sqrt(h)`、100/256 分离、NDA 1024/DA 768、13 dB 与 crossover 分离、18.0/16.9/10.7、BER-ratio、26/29 和 1.9 dB 的 NDA-vs-DA 归属均与当前 LaTeX 一致；7 个 BibTeX key 闭合。
- [x] 原始范围边界：`system_model.tex:5` 和 `method.tex:8` 实际嵌入 Fig.1/Fig.2，独立 verifier 确认这不是占位图，违反原首轮硬边界，列为 BLOCKING。
- [x] external-output C1–C10：C1/C5/C6/C7/C8/C9 PASS；C2/C3/C4/C10 PARTIAL，主要债务为 `DA-ML/NDA-ML/oracle` 定义、缩写首次展开、数字逐项溯源。

### 证据

```text
latexmk: exit 0
Output written on main.pdf (7 pages, 491208 bytes)
PDF: Letter, 612 x 792 pt, PDF 1.7, not encrypted
pdffonts: 34 records, all emb=yes sub=yes uni=yes
Overfull: 0
Underfull: 1, main.log:337, badness 3158
BibTeX keys cited: 7; missing cited keys: none
Rendered pages: 7; no clipping/overlap; page 6-7 float displacement
Independent total gate: BLOCKED
```

### 结论

BLOCKED

### 后续（FAIL/PARTIAL 时）

- 用户需明确当前 CCE 扩展预览是否可以替代原始首轮占位骨架；若不能，恢复 Fig.1/Fig.2 占位框和 DRAFT 元数据。
- 先定义 `DA-ML`、`NDA-ML`、`oracle`，补全缩写首次展开和代表数字的 source/data/code 溯源。
- 另开版面优化轮处理第 6–7 页 float 留白和 1 个 Underfull；不通过新增图、参考文献或留白补足正文。

## V004: 新标题与用户更新图资产的 fresh build 局部复核

> 2026-07-14 | 关联：S002 | 结论：PARTIAL

### 验证项

- [x] 标题源与渲染：检查 `main.tex:13` 和第 1 页 PNG；标题按用户给定内容渲染为两行，未见溢出。
- [x] 最新图资产：检查 `system_model.tex`、`method.tex` 和构建日志；当前使用 `fig1_system_model_v5.pdf`、`fig2_adaptive_cpr.pdf`，两张系统图均为 `figure* [t]`。
- [x] 构建：使用 MiKTeX `latexmk` fresh build；exit 0，PDF 为 8 页 Letter。
- [x] 逐页局部版面：渲染并检查 8 页；Fig.1 在第 3 页、Fig.2 在第 4 页、BER 图在第 6 页、Fig.4/Fig.5 在第 7 页、结论/参考文献在第 8 页，未见裁切或重叠。
- [ ] 独立复核：另行派发的只读 verifier 未在等待窗口内返回，随后关闭；本条不把主线程观察升级为独立验证结论。

### 证据

```text
main.tex:13 = Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links
latexmk: exit 0
Output written on main.pdf (8 pages, 1029955 bytes)
main.log:337 Underfull \\hbox (badness 3158)
main.log:361 Underfull \\vbox (badness 1895)
LaTeX error/fatal: none detected
Undefined citation/reference: none detected
Overfull box: none detected
Rendered pages: 8; no clipping/overlap observed
Fig.1 source: sections/system_model.tex uses figure* [t] and fig1_system_model_v5.pdf
Fig.3 source: sections/results.tex still uses figure* and ccisp_fig2_ber.pdf
Independent verifier: no result returned before timeout; not counted as PASS
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

- 若用户确认“图 1 放第 2 页开头”，把 Fig.1 的 `figure*` 声明从 `system_model.tex` 移到 `main.tex` 的 introduction 之后、system model 之前，再 fresh build 验证实际页位。
- 将 Fig.3 的 BER 总览由双栏改为单栏，重新检查坐标、图例和页数。
- 继续保留 V003 的总 gate BLOCKED；本次没有关闭 Fig.1/Fig.2 视觉验收、external-output 或词数债务。

## V005: 用户指定图位与单栏 Fig.3 独立复核

> 2026-07-14 | 关联：S002 | 结论：PARTIAL

### 验证范围

独立 verifier 只读检查当前 `projects/simulation/paper/ccisp2026/` 的 `main.tex`、`sections/*.tex`、fresh `main.pdf`/`main.log` 和逐页渲染结果；未修改文件、未提交、未运行仿真或绘图脚本。

### 验证项

- [x] Fig.1 页位：`main.log` 的图形输出记录与 PDF caption/渲染均显示 Fig.1 在第 2 页。
- [x] Fig.2 页位：`main.log` 的图形输出记录与 PDF caption/渲染均显示 Fig.2 在第 3 页。
- [x] BER Fig.3 单栏：`sections/results.tex:4--8` 使用 `\\begin{figure}`、`width=\\columnwidth` 和 `fig:ber-overview`；第 5 页右栏图、坐标轴、图例和 caption 完整可读，无裁切或重叠。
- [x] PDF/build：`main.log:435` 为 7 pages；PDF MediaBox 为 `612 x 792 pt`（Letter）；`IEEEtran` conference 双栏渲染；`pdffonts` 显示全部字体 `emb=yes`、`sub=yes`。
- [x] 错误诊断：未发现 LaTeX Error、undefined citation/reference 或 overfull box。
- [ ] Underfull/分页：`main.log:344` 有 Underfull hbox badness 3158，`:362` 有 Underfull vbox badness 4634；第 7 页参考文献尾部大面积留白，第 6 页浮动图与正文分布仍偏松散。

### 结论

PARTIAL：本轮用户指定的三项版式改动均通过独立核验；剩余 underfull 和末页留白属于后续正式版面优化债务，不影响当前 PDF 可编译和可读，但当前版本仍不等于最终投稿稿。
