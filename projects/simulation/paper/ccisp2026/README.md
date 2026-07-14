# CCISP 2026 LaTeX 投稿骨架 / CCE-CC-002 版面探针

这是第一轮可编译版面探针，不是最终投稿稿。当前工作树中的正文已经是获批 `CCE-CC-002` 的扩展预览，不再是旧的 6 页占位骨架；因此不得把当前文件误读为 W001–W003 的逐字抽取版。工程使用 CCISP 官方投稿页提供的 `IEEE-Conference-LaTeX-template_7-9-18.zip` 中的 `IEEEtran.cls`；官方 ZIP SHA256：

`64CD0E9BD91A909530A9BD65F41622959CCD5D57A6344200FA70F967AF8A7ECD`

## 内容范围

- 当前 `sections/*.tex` 采用 D004/V003 修正后的 `sqrt(h)` 接收模型、100-symbol channel block / 256-sample DSP window、multi-pilot DA-LS、两层选择器、data-BER 和 BER-ratio 口径；旧 W 文件只读，不能直接覆盖回去。
- 当前工作树引用最新的 `fig1_system_model_v5.pdf`、`fig2_adaptive_cpr.pdf` 以及三张已有数据图；两张 PDF/SVG/PNG 已从当前 draw.io 编辑源重新导出。原 CCISP 首轮合同要求 Fig.1/Fig.2 使用显式占位框，这个偏离仍是阻塞债务，详见 `issues.md`，不表示图形方案已最终验收。
- 当前 7 个 BibTeX 条目均被正文引用；引用解析与构建已通过，但 `oracle` 图例语义、来源同步和投稿口径仍需独立收口。
- 当前作者栏为 `Anonymous Submission`，标题为工作标题；这不是最终作者/单位信息，也不等于已完成投稿元数据。

## 构建

在仓库根目录执行：

```powershell
$env:Path = "C:\\Program Files\\Git\\usr\\bin;C:\\Users\\zzt\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64;$env:Path"
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

如果当前环境优先解析到 Codex 的 `pdftoppm`/`pdfinfo` wrapper，逐页渲染和 PDF 检查使用 MiKTeX 路径中的同名可执行文件。不要把 `毕设/论文/ccisp/` 的示例正文复制进来；它只是同源模板样例。

## 当前状态

- 首轮目标：测量双栏版式页数、公式/图表溢出和引用债务；上一版扩展预览为 7 页，最新标题与图资产版 fresh build 为 `latexmk` exit 0、`main.pdf` 为 8 页（1,029,955 bytes）。
- 当前标题为 `Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links`；第 1 页标题自然换为两行。
- 当前日志无 LaTeX error、未定义引用、overfull box；有 1 个 `Underfull \\hbox`（`main.log:337`）和 1 个 `Underfull \\vbox`（`main.log:361`）。字体检查显示全部嵌入，PDF 为 Letter 纸张。
- 已使用 MiKTeX 绝对路径渲染并逐页检查最新标题/图资产版 PDF；公式、图表和参考文献未发现裁切或重叠。当前 Fig.1 在第 3 页、Fig.2 在第 4 页、BER 图在第 6 页、结论/参考文献在第 8 页；图浮动造成的留白仍记录在 `issues.md`，暂不把排版回收计入正文增量。
- 当前 Fig.3 仍为双栏宽图；此前“缩小到单栏”的版式约束尚未实施。
- 当前不锁定 CCISP 页数口径：官方投稿页写 5–10 页，既有任务口径写 4–6 页。
- 当前不运行仿真、不修改绘图脚本、不处理 Fig.1/Fig.2 最终视觉方案。
