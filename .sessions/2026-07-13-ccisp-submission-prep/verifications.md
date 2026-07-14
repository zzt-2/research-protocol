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
